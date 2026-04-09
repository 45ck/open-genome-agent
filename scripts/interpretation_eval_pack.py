from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
CASE_SCHEMA = json.loads(
    (ROOT / "schemas" / "interpretation-case.schema.json").read_text(encoding="utf-8")
)
PACK_MODULES = {
    "clinvar": ROOT / "evals" / "interpretation" / "clinvar" / "cases.json",
    "pgx": ROOT / "evals" / "interpretation" / "pgx" / "cases.json",
    "prs": ROOT / "evals" / "interpretation" / "prs" / "cases.json",
    "functional": ROOT / "evals" / "interpretation" / "functional" / "cases.json",
}


def load_cases(path: Path) -> list[dict[str, Any]]:
    cases = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise TypeError(f"Expected list of cases in {path}")
    for case in cases:
        validate(case, CASE_SCHEMA)
    return cases


def build_index() -> dict[str, Any]:
    cases_by_module: dict[str, list[dict[str, Any]]] = {}
    all_cases: list[dict[str, Any]] = []
    for module, path in PACK_MODULES.items():
        module_cases = load_cases(path)
        cases_by_module[module] = module_cases
        all_cases.extend(module_cases)

    confidence_counts = Counter(case["confidence_bucket"] for case in all_cases)
    source_class_counts = Counter(case["source_class"] for case in all_cases)
    return {
        "pack_id": "interpretation-eval-pack",
        "case_count": len(all_cases),
        "modules": {
            module: {
                "case_count": len(cases),
                "path": str(PACK_MODULES[module]),
                "case_ids": [case["case_id"] for case in cases],
            }
            for module, cases in cases_by_module.items()
        },
        "confidence_counts": dict(confidence_counts),
        "source_class_counts": dict(source_class_counts),
        "cases": all_cases,
    }


def render_markdown(index: dict[str, Any]) -> str:
    lines = [
        "# Interpretation Evaluation Pack",
        "",
        f"Cases: `{index['case_count']}`",
        "",
        "## Modules",
    ]
    for module, module_data in index["modules"].items():
        lines.append(f"- `{module}`: {module_data['case_count']} cases")
    lines.extend(
        [
            "",
            "## Confidence buckets",
        ]
    )
    for bucket, count in sorted(index["confidence_counts"].items()):
        lines.append(f"- `{bucket}`: {count}")
    lines.extend(
        [
            "",
            "## Source classes",
        ]
    )
    for source_class, count in sorted(index["source_class_counts"].items()):
        lines.append(f"- `{source_class}`: {count}")
    return "\n".join(lines) + "\n"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the interpretation evaluation pack index."
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where the pack index should be written.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    index = build_index()
    (output_dir / "index.json").write_text(
        json.dumps(index, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "index.md").write_text(render_markdown(index), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
