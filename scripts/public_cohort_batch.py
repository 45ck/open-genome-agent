from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_sample_manifest(path: Path) -> dict[str, Any]:
    manifest = load_json(path)
    if "samples" not in manifest or not isinstance(manifest["samples"], list):
        raise TypeError("1000G sample manifest must contain a samples list.")
    return manifest


def load_sample_summaries(paths: list[Path]) -> list[dict[str, Any]]:
    return [load_json(path) for path in paths]


def build_summary(
    *,
    sample_manifest: dict[str, Any],
    sample_summaries: list[dict[str, Any]],
    elapsed_seconds: float | None,
) -> dict[str, Any]:
    manifest_samples = {
        item["sample_id"]: item
        for item in sample_manifest["samples"]
        if "sample_id" in item
    }
    seen_ids = [summary["sample_id"] for summary in sample_summaries]
    population_counts: Counter[str] = Counter()
    super_population_counts: Counter[str] = Counter()
    grouped: dict[str, list[str]] = defaultdict(list)
    missing = []

    for sample_id, sample in manifest_samples.items():
        if sample_id not in seen_ids:
            missing.append(sample_id)

    for summary in sample_summaries:
        sample_id = summary["sample_id"]
        manifest_entry = manifest_samples.get(sample_id)
        if manifest_entry is None:
            continue
        population = manifest_entry["population"]
        super_population = manifest_entry["super_population"]
        population_counts[population] += 1
        super_population_counts[super_population] += 1
        grouped[super_population].append(sample_id)

    throughput: dict[str, Any] | None = None
    if elapsed_seconds is not None and elapsed_seconds > 0:
        throughput = {
            "elapsed_seconds": elapsed_seconds,
            "sample_count": len(sample_summaries),
            "samples_per_minute": round(
                (len(sample_summaries) / elapsed_seconds) * 60, 2
            ),
        }

    return {
        "cohort_id": sample_manifest["cohort_id"],
        "reference_build": sample_manifest.get("reference_build"),
        "selected_sample_count": len(sample_manifest["samples"]),
        "processed_sample_count": len(sample_summaries),
        "missing_sample_ids": missing,
        "population_counts": dict(population_counts),
        "super_population_counts": dict(super_population_counts),
        "super_population_groups": dict(grouped),
        "throughput": throughput,
        "notes": [
            "Population labels are summary context only and should not be treated as phenotype truth.",
            "Batch runs should keep ancestry, PRS, and trait caveats explicit in downstream outputs.",
        ],
    }


def render_html(summary: dict[str, Any]) -> str:
    cards = []
    for label, value in [
        ("Processed samples", summary["processed_sample_count"]),
        ("Selected samples", summary["selected_sample_count"]),
        ("Missing samples", len(summary["missing_sample_ids"])),
    ]:
        cards.append(f"""
  <div class="card">
    <h2>{label}</h2>
    <div class="metric">{value}</div>
  </div>
""")

    population_rows = []
    for super_population, count in sorted(summary["super_population_counts"].items()):
        members = ", ".join(
            summary["super_population_groups"].get(super_population, [])
        )
        population_rows.append(
            "<tr>"
            f"<td>{super_population}</td>"
            f"<td>{count}</td>"
            f"<td>{members}</td>"
            "</tr>"
        )

    throughput_section = (
        '<p class="note">No elapsed runtime provided for throughput accounting.</p>'
    )
    if summary["throughput"] is not None:
        throughput = summary["throughput"]
        throughput_section = (
            "<h2>Throughput</h2>"
            f"<p><strong>Elapsed seconds:</strong> {throughput['elapsed_seconds']}</p>"
            f"<p><strong>Samples per minute:</strong> {throughput['samples_per_minute']}</p>"
        )

    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>1000 Genomes Batch Summary</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #111; }}
    .cards {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }}
    .card {{ border: 1px solid #d0d7de; border-radius: 8px; padding: 1rem; min-width: 220px; }}
    .metric {{ font-size: 1.75rem; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
    th, td {{ border: 1px solid #d0d7de; padding: 0.5rem; text-align: left; }}
    th {{ background: #f6f8fa; }}
    .note {{ color: #555; }}
  </style>
</head>
<body>
  <h1>1000 Genomes batch summary</h1>
  <p class="note">Population labels are context for summary pages and must stay separate from diagnostic or destiny-style claims.</p>
  <div class="cards">{''.join(cards)}</div>
  <h2>Population-aware summary</h2>
  <table>
    <thead>
      <tr><th>Super population</th><th>Count</th><th>Samples</th></tr>
    </thead>
    <tbody>
      {''.join(population_rows)}
    </tbody>
  </table>
  {throughput_section}
</body>
</html>
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a batch summary for a selected 1000 Genomes public cohort."
    )
    parser.add_argument(
        "--sample-manifest",
        required=True,
        help="Pinned 1000 Genomes sample manifest JSON.",
    )
    parser.add_argument(
        "--sample-summary",
        action="append",
        default=[],
        help="Path to a sample_summary.json file. Repeat for multiple samples.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where the batch summary should be written.",
    )
    parser.add_argument(
        "--elapsed-seconds",
        type=float,
        help="Optional elapsed runtime used to compute throughput metrics.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sample_manifest_path = Path(args.sample_manifest).resolve()
    output_dir = Path(args.output_dir).resolve()
    sample_summary_paths = [Path(path).resolve() for path in args.sample_summary]

    if not sample_manifest_path.exists():
        raise FileNotFoundError(f"Missing sample manifest: {sample_manifest_path}")
    for path in sample_summary_paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing sample summary: {path}")

    manifest = load_sample_manifest(sample_manifest_path)
    summaries = load_sample_summaries(sample_summary_paths)
    summary = build_summary(
        sample_manifest=manifest,
        sample_summaries=summaries,
        elapsed_seconds=args.elapsed_seconds,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "index.html").write_text(render_html(summary), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
