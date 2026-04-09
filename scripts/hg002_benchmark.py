from __future__ import annotations

import argparse
import csv
import html
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hooks.common import append_jsonl  # noqa: E402

NUMERIC_FIELDS = {
    "TRUTH.TOTAL",
    "TRUTH.TP",
    "TRUTH.FN",
    "QUERY.TOTAL",
    "QUERY.FP",
    "QUERY.UNK",
    "FP.gt",
    "FP.al",
    "Recall",
    "Precision",
    "Frac_NA",
    "F1_Score",
}


def summary_csv_path(output_prefix: Path) -> Path:
    return output_prefix.parent / f"{output_prefix.name}.summary.csv"


def coerce_value(value: str) -> Any:
    text = value.strip()
    if not text:
        return None
    try:
        if any(char in text for char in [".", "e", "E"]):
            return float(text)
        return int(text)
    except ValueError:
        return text


def normalize_row(row: dict[str, str]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in row.items():
        if key in NUMERIC_FIELDS:
            normalized[key] = coerce_value(value)
        else:
            normalized[key] = value.strip()
    return normalized


def load_summary_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return [normalize_row(row) for row in reader]


def preferred_headline_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_type: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        variant_type = str(row.get("Type", "")).strip()
        if not variant_type:
            continue
        by_type.setdefault(variant_type, []).append(row)

    preferred: dict[str, dict[str, Any]] = {}
    for variant_type, candidates in by_type.items():
        preferred_row = next(
            (
                candidate
                for candidate in candidates
                if str(candidate.get("Filter", "")).upper() == "PASS"
            ),
            candidates[0],
        )
        preferred[variant_type] = preferred_row
    return preferred


def parse_happy_summary(summary_path: Path, *, label: str) -> dict[str, Any]:
    rows = load_summary_rows(summary_path)
    preferred = preferred_headline_rows(rows)
    return {
        "benchmark_id": "hg002-baseline",
        "label": label,
        "summary_csv": str(summary_path),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "headline": preferred,
        "rows": rows,
    }


def render_html_report(metrics: dict[str, Any]) -> str:
    headline = metrics["headline"]
    rows = metrics["rows"]
    header = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>HG002 Benchmark Summary</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; color: #111; }
    h1, h2 { margin-bottom: 0.5rem; }
    .cards { display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }
    .card { border: 1px solid #d0d7de; border-radius: 8px; padding: 1rem; min-width: 220px; }
    .metric { font-size: 1.5rem; font-weight: 700; }
    table { border-collapse: collapse; width: 100%; margin-top: 1.5rem; }
    th, td { border: 1px solid #d0d7de; padding: 0.5rem; text-align: left; }
    th { background: #f6f8fa; }
    .note { color: #555; margin-top: 1rem; }
  </style>
</head>
<body>
"""

    cards: list[str] = []
    for variant_type, row in headline.items():
        recall = row.get("Recall")
        precision = row.get("Precision")
        f1_score = row.get("F1_Score")
        cards.append(f"""
  <div class="card">
    <h2>{html.escape(variant_type)}</h2>
    <div class="metric">F1: {f1_score}</div>
    <div>Recall: {recall}</div>
    <div>Precision: {precision}</div>
    <div>Filter: {html.escape(str(row.get("Filter", "")))}</div>
  </div>
""")

    columns = [
        "Type",
        "Filter",
        "TRUTH.TOTAL",
        "TRUTH.TP",
        "TRUTH.FN",
        "QUERY.TOTAL",
        "QUERY.FP",
        "QUERY.UNK",
        "Recall",
        "Precision",
        "F1_Score",
    ]
    table_head = "".join(f"<th>{html.escape(column)}</th>" for column in columns)
    table_rows = []
    for row in rows:
        table_rows.append(
            "<tr>"
            + "".join(
                f"<td>{html.escape(str(row.get(column, '')))}</td>"
                for column in columns
            )
            + "</tr>"
        )

    return (
        header
        + f"<h1>HG002 Benchmark Summary</h1><p>Label: {html.escape(str(metrics['label']))}</p>"
        + f"<div class=\"cards\">{''.join(cards)}</div>"
        + "<table><thead><tr>"
        + table_head
        + "</tr></thead><tbody>"
        + "".join(table_rows)
        + "</tbody></table>"
        + '<p class="note">Headline cards prefer PASS rows when present. Review the full table and source CSV before making claims.</p>'
        + "</body></html>\n"
    )


def build_happy_command(
    *,
    truth_vcf: Path,
    query_vcf: Path,
    benchmark_bed: Path,
    reference_fasta: Path,
    output_prefix: Path,
    threads: int,
    extra_args: list[str],
) -> list[str]:
    command = [
        "hap.py",
        str(truth_vcf),
        str(query_vcf),
        "-f",
        str(benchmark_bed),
        "-r",
        str(reference_fasta),
        "-o",
        str(output_prefix),
        "--threads",
        str(threads),
    ]
    command.extend(extra_args)
    return command


def require_path(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing required {label}: {path}")


def write_outputs(
    *,
    output_dir: Path,
    metrics: dict[str, Any],
    html_report: str,
    command: list[str] | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "metrics.json"
    report_path = output_dir / "index.html"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(html_report, encoding="utf-8")

    if command is not None:
        append_jsonl(
            output_dir / "commands.jsonl",
            {
                "tool": "hap.py",
                "command": command,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "outputs": {
                    "metrics_json": str(metrics_path),
                    "summary_html": str(report_path),
                    "summary_csv": metrics["summary_csv"],
                },
            },
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run or parse an HG002 hap.py benchmark."
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory for benchmark outputs."
    )
    parser.add_argument(
        "--label", default="hg002", help="Label used in output metadata."
    )
    parser.add_argument(
        "--summary-csv",
        help="Parse an existing hap.py summary CSV instead of executing hap.py.",
    )
    parser.add_argument("--truth-vcf", help="Truth VCF for hap.py execution mode.")
    parser.add_argument("--query-vcf", help="Query VCF for hap.py execution mode.")
    parser.add_argument(
        "--benchmark-bed", help="Benchmark BED for hap.py execution mode."
    )
    parser.add_argument(
        "--reference-fasta", help="Reference FASTA for hap.py execution mode."
    )
    parser.add_argument(
        "--threads", type=int, default=1, help="Thread count passed to hap.py."
    )
    parser.add_argument(
        "--extra-arg",
        action="append",
        default=[],
        help="Extra argument passed through to hap.py. Repeat for multiple values.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print the hap.py command and exit."
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = Path(args.output_dir).resolve()

    if args.summary_csv:
        summary_path = Path(args.summary_csv).resolve()
        require_path(summary_path, "summary CSV")
        command: list[str] | None = None
    else:
        required = {
            "truth VCF": args.truth_vcf,
            "query VCF": args.query_vcf,
            "benchmark BED": args.benchmark_bed,
            "reference FASTA": args.reference_fasta,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise SystemExit(
                f"Missing required execution arguments: {', '.join(missing)}"
            )

        truth_vcf = Path(args.truth_vcf).resolve()
        query_vcf = Path(args.query_vcf).resolve()
        benchmark_bed = Path(args.benchmark_bed).resolve()
        reference_fasta = Path(args.reference_fasta).resolve()
        require_path(truth_vcf, "truth VCF")
        require_path(query_vcf, "query VCF")
        require_path(benchmark_bed, "benchmark BED")
        require_path(reference_fasta, "reference FASTA")

        output_prefix = output_dir / args.label
        command = build_happy_command(
            truth_vcf=truth_vcf,
            query_vcf=query_vcf,
            benchmark_bed=benchmark_bed,
            reference_fasta=reference_fasta,
            output_prefix=output_prefix,
            threads=args.threads,
            extra_args=args.extra_arg,
        )
        if args.dry_run:
            print(json.dumps({"command": command}, indent=2))
            return 0
        subprocess.run(command, check=True)
        summary_path = summary_csv_path(output_prefix)
        require_path(summary_path, "hap.py summary CSV")

    metrics = parse_happy_summary(summary_path, label=args.label)
    html_report = render_html_report(metrics)
    write_outputs(
        output_dir=output_dir, metrics=metrics, html_report=html_report, command=command
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
