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
from scripts.hg002_benchmark import (  # noqa: E402
    build_happy_command,
    parse_happy_summary,
    require_path,
    summary_csv_path,
)

GENE_NUMERIC_FIELDS = {
    "RegionSize",
    "CoveredBases",
    "CoveragePct",
    "Recall",
    "Precision",
    "F1_Score",
}

STATUS_ALIASES = {
    "supported": "supported",
    "pass": "supported",
    "trusted": "supported",
    "partial": "partial",
    "partial_support": "partial",
    "review": "partial",
    "not_yet_trusted": "not_yet_trusted",
    "not-yet-trusted": "not_yet_trusted",
    "unsupported": "not_yet_trusted",
    "untrusted": "not_yet_trusted",
}

STATUS_ORDER = ["supported", "partial", "not_yet_trusted"]
STATUS_LABELS = {
    "supported": "Supported genes",
    "partial": "Partial support",
    "not_yet_trusted": "Not yet trusted",
}


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


def detect_dialect(path: Path) -> type[csv.Dialect]:
    sample = path.read_text(encoding="utf-8")[:4096]
    return csv.Sniffer().sniff(sample, delimiters=",\t")


def normalize_status(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "_")
    if normalized not in STATUS_ALIASES:
        raise ValueError(
            "Unsupported CMRG status "
            f"{value!r}. Expected one of: {', '.join(sorted(STATUS_ALIASES))}."
        )
    return STATUS_ALIASES[normalized]


def normalize_gene_row(row: dict[str, str]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in row.items():
        clean_key = key.strip()
        if clean_key in GENE_NUMERIC_FIELDS:
            normalized[clean_key] = coerce_value(value)
        else:
            normalized[clean_key] = value.strip()

    gene = str(normalized.get("Gene", "")).strip()
    if not gene:
        raise ValueError("Each CMRG gene row must include a Gene value.")

    status = str(normalized.get("Status", "")).strip()
    if not status:
        raise ValueError(f"CMRG gene row for {gene} is missing Status.")

    normalized["Gene"] = gene
    normalized["Status"] = normalize_status(status)
    return normalized


def load_gene_rows(path: Path) -> list[dict[str, Any]]:
    dialect = detect_dialect(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, dialect=dialect)
        rows = [normalize_gene_row(row) for row in reader]
    rows.sort(key=lambda row: (STATUS_ORDER.index(row["Status"]), row["Gene"]))
    return rows


def grouped_gene_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {status: [] for status in STATUS_ORDER}
    for row in rows:
        grouped[row["Status"]].append(row)
    return grouped


def parse_cmrg_scorecard(
    *,
    gene_results_path: Path,
    label: str,
    summary_path: Path | None = None,
) -> dict[str, Any]:
    gene_rows = load_gene_rows(gene_results_path)
    groups = grouped_gene_rows(gene_rows)
    counts = {status: len(rows) for status, rows in groups.items()}
    metrics: dict[str, Any] = {
        "benchmark_id": "cmrg-medically-relevant-genes",
        "label": label,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "gene_results": str(gene_results_path),
        "counts": counts,
        "rows": gene_rows,
        "groups": groups,
        "limitations": [
            "Only genes listed as supported should be treated as inside the current proof surface.",
            "Partial and not-yet-trusted genes need manual review before any public-facing claim.",
        ],
    }
    if summary_path is not None:
        metrics["benchmark_summary"] = parse_happy_summary(summary_path, label=label)
    return metrics


def render_gene_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return '<p class="empty">No genes in this bucket.</p>'

    columns = ["Gene", "CoveragePct", "Recall", "Precision", "F1_Score", "Notes"]
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
        "<table><thead><tr>"
        + table_head
        + "</tr></thead><tbody>"
        + "".join(table_rows)
        + "</tbody></table>"
    )


def render_html_report(metrics: dict[str, Any]) -> str:
    groups = metrics["groups"]
    counts = metrics["counts"]
    benchmark_summary = metrics.get("benchmark_summary")

    cards = []
    for status in STATUS_ORDER:
        cards.append(f"""
  <div class="card">
    <h2>{html.escape(STATUS_LABELS[status])}</h2>
    <div class="metric">{counts[status]}</div>
    <div>genes</div>
  </div>
""")

    benchmark_section = '<p class="note">No aggregate hap.py summary attached to this scorecard yet.</p>'
    if benchmark_summary:
        headline = benchmark_summary["headline"]
        summary_rows = []
        for variant_type, row in headline.items():
            summary_rows.append(
                "<tr>"
                f"<td>{html.escape(variant_type)}</td>"
                f"<td>{html.escape(str(row.get('Filter', '')))}</td>"
                f"<td>{html.escape(str(row.get('Recall', '')))}</td>"
                f"<td>{html.escape(str(row.get('Precision', '')))}</td>"
                f"<td>{html.escape(str(row.get('F1_Score', '')))}</td>"
                "</tr>"
            )
        benchmark_section = (
            "<h2>Aggregate benchmark summary</h2>"
            "<table><thead><tr>"
            "<th>Type</th><th>Filter</th><th>Recall</th><th>Precision</th><th>F1_Score</th>"
            "</tr></thead><tbody>" + "".join(summary_rows) + "</tbody></table>"
        )

    sections = []
    for status in STATUS_ORDER:
        sections.append(
            f"<h2>{html.escape(STATUS_LABELS[status])}</h2>"
            + render_gene_table(groups[status])
        )

    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>CMRG Support Boundaries</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; color: #111; }}
    h1, h2 {{ margin-bottom: 0.5rem; }}
    .cards {{ display: flex; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0; }}
    .card {{ border: 1px solid #d0d7de; border-radius: 8px; padding: 1rem; min-width: 220px; }}
    .metric {{ font-size: 1.75rem; font-weight: 700; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; }}
    th, td {{ border: 1px solid #d0d7de; padding: 0.5rem; text-align: left; }}
    th {{ background: #f6f8fa; }}
    .note, .empty {{ color: #555; }}
  </style>
</head>
<body>
  <h1>CMRG support boundaries</h1>
  <p>Label: {html.escape(str(metrics["label"]))}</p>
  <div class="cards">{''.join(cards)}</div>
  {benchmark_section}
  <p class="note">Only supported genes are inside the current proof surface. Partial and not-yet-trusted genes stay close to the limitations boundary.</p>
  {''.join(sections)}
</body>
</html>
"""


def write_outputs(
    *,
    output_dir: Path,
    metrics: dict[str, Any],
    html_report: str,
    command: list[str] | None,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    scorecard_path = output_dir / "scorecard.json"
    report_path = output_dir / "index.html"
    scorecard_path.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    report_path.write_text(html_report, encoding="utf-8")

    if command is not None:
        outputs: dict[str, Any] = {
            "scorecard_json": str(scorecard_path),
            "summary_html": str(report_path),
        }
        if metrics.get("benchmark_summary"):
            outputs["summary_csv"] = metrics["benchmark_summary"]["summary_csv"]

        append_jsonl(
            output_dir / "commands.jsonl",
            {
                "tool": "hap.py",
                "command": command,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "outputs": outputs,
            },
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run or assemble a CMRG hard-region scorecard."
    )
    parser.add_argument(
        "--output-dir", required=True, help="Directory for CMRG benchmark outputs."
    )
    parser.add_argument("--label", default="cmrg", help="Label for output metadata.")
    parser.add_argument(
        "--gene-results",
        required=True,
        help="CSV or TSV file with Gene, Status, and optional metric columns.",
    )
    parser.add_argument(
        "--summary-csv",
        help="Existing hap.py summary CSV for the CMRG benchmark regions.",
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
    gene_results_path = Path(args.gene_results).resolve()
    require_path(gene_results_path, "gene results file")

    summary_path: Path | None = None
    command: list[str] | None = None

    if args.summary_csv:
        summary_path = Path(args.summary_csv).resolve()
        require_path(summary_path, "summary CSV")
    elif all(
        value
        for value in [
            args.truth_vcf,
            args.query_vcf,
            args.benchmark_bed,
            args.reference_fasta,
        ]
    ):
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

    metrics = parse_cmrg_scorecard(
        gene_results_path=gene_results_path,
        label=args.label,
        summary_path=summary_path,
    )
    html_report = render_html_report(metrics)
    write_outputs(
        output_dir=output_dir,
        metrics=metrics,
        html_report=html_report,
        command=command,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
