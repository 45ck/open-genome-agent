from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
RESULT_SCHEMA = json.loads(
    (ROOT / "evals" / "reasoning" / "results.schema.json").read_text(encoding="utf-8")
)


def load_results(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            row = json.loads(text)
            validate(row, RESULT_SCHEMA)
            rows.append(row)
    return rows


def summarize_backend(rows: list[dict[str, Any]]) -> dict[str, Any]:
    count = len(rows)
    if count == 0:
        return {
            "case_count": 0,
            "avg_evidence_alignment": 0.0,
            "unsupported_claims": 0,
            "contradictions": 0,
            "source_class_errors": 0,
            "failure_count": 0,
        }

    avg_alignment = sum(row["evidence_alignment_score"] for row in rows) / count
    unsupported_claims = sum(row["unsupported_claims"] for row in rows)
    contradictions = sum(row["contradictions"] for row in rows)
    source_class_errors = sum(0 if row["source_class_correct"] else 1 for row in rows)
    failure_count = sum(
        1
        for row in rows
        if row["unsupported_claims"] > 0
        or row["contradictions"] > 0
        or not row["source_class_correct"]
    )
    return {
        "case_count": count,
        "avg_evidence_alignment": round(avg_alignment, 3),
        "unsupported_claims": unsupported_claims,
        "contradictions": contradictions,
        "source_class_errors": source_class_errors,
        "failure_count": failure_count,
    }


def build_summary(paths: list[Path]) -> dict[str, Any]:
    by_backend: dict[str, list[dict[str, Any]]] = defaultdict(list)
    all_rows: list[dict[str, Any]] = []
    for path in paths:
        rows = load_results(path)
        for row in rows:
            by_backend[row["backend"]].append(row)
        all_rows.extend(rows)

    return {
        "pack_id": "reasoning-eval-pack",
        "backend_count": len(by_backend),
        "total_rows": len(all_rows),
        "backends": {
            backend: summarize_backend(rows)
            for backend, rows in sorted(by_backend.items())
        },
    }


def render_markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Reasoning Evaluation",
        "",
        f"Backends compared: `{summary['backend_count']}`",
        f"Total rows: `{summary['total_rows']}`",
        "",
        "## Backend comparison",
    ]
    for backend, metrics in summary["backends"].items():
        lines.extend(
            [
                f"### {backend}",
                f"- cases: {metrics['case_count']}",
                f"- average evidence alignment: {metrics['avg_evidence_alignment']}",
                f"- unsupported claims: {metrics['unsupported_claims']}",
                f"- contradictions: {metrics['contradictions']}",
                f"- source class errors: {metrics['source_class_errors']}",
                f"- failed cases: {metrics['failure_count']}",
                "",
            ]
        )
    lines.extend(
        [
            "Unsupported claims, contradictions, and source-class mistakes are first-class failures and should not be averaged away.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Score reasoning results and compare backends."
    )
    parser.add_argument(
        "--results-jsonl",
        action="append",
        default=[],
        help="Path to a JSONL file of reasoning results. Repeat for multiple files.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where summary outputs should be written.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    paths = [Path(path).resolve() for path in args.results_jsonl]
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing reasoning results file: {path}")
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = build_summary(paths)
    (output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "comparison.md").write_text(
        render_markdown(summary), encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
