from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def kind_from_path(path: Path) -> str:
    suffixes = [suffix.lower() for suffix in path.suffixes]
    if suffixes[-2:] == [".vcf", ".gz"] or suffixes[-1:] == [".vcf"]:
        return "vcf"
    if suffixes[-1:] == [".bcf"]:
        return "bcf"
    if suffixes[-1:] == [".bam"]:
        return "bam"
    if suffixes[-1:] == [".cram"]:
        return "cram"
    return "unknown"


def index_path_for_input(path: Path) -> Path | None:
    if path.name.endswith(".vcf.gz"):
        for suffix in [".tbi", ".csi"]:
            candidate = Path(f"{path}{suffix}")
            if candidate.exists():
                return candidate
        return None
    if path.suffix.lower() == ".bcf":
        for suffix in [".csi", ".tbi"]:
            candidate = Path(f"{path}{suffix}")
            if candidate.exists():
                return candidate
        return None
    return None


def render_report(template: str, substitutions: dict[str, str]) -> str:
    rendered = template
    for key, value in substitutions.items():
        rendered = rendered.replace(f"{{{{ {key} }}}}", value)
    return rendered


def render_walkthrough(
    *,
    sample_manifest: dict[str, Any],
    input_path: Path,
    output_dir: Path,
    harness: str,
) -> str:
    sample_id = sample_manifest["sample_id"]
    profile_url = sample_manifest["source_profile_url"]
    return f"""# Public Demo Walkthrough

Sample: `{sample_id}`

Profile: `{profile_url}`

Input path: `{input_path}`

Output directory: `{output_dir}`

Harness: `{harness}`

## What this intake pack proves

- the public sample was selected explicitly
- the local genome file path is recorded without mutating the source file
- the first run artifacts are reproducible and easy to diff

## Next steps

1. confirm the local file and index state
2. detect or verify the reference build before interpretation
3. keep direct findings, PGx, and probabilistic sections separated
4. carry limitations into the final report

## Boundaries

- do not upload the genome file by default
- do not commit the raw file into the repository
- do not treat participant-supplied survey data as deterministic truth
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a local-first intake pack for a public genome demo."
    )
    parser.add_argument(
        "--sample-manifest",
        required=True,
        help="Pinned JSON manifest for the selected public demo sample.",
    )
    parser.add_argument(
        "--input-path",
        required=True,
        help="Absolute path to the local public-genome file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where the intake pack should be written.",
    )
    parser.add_argument(
        "--harness",
        default="manual",
        choices=["claude", "codex", "mcp", "manual", "unknown"],
        help="Harness value recorded in the run manifest.",
    )
    parser.add_argument(
        "--report-template",
        default=str(ROOT / "examples" / "reports" / "public_demo_template.md"),
        help="Markdown template used to generate the report stub.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    sample_manifest_path = Path(args.sample_manifest).resolve()
    input_path = Path(args.input_path).resolve()
    output_dir = Path(args.output_dir).resolve()
    report_template_path = Path(args.report_template).resolve()

    if not sample_manifest_path.exists():
        raise FileNotFoundError(f"Missing sample manifest: {sample_manifest_path}")
    if not input_path.exists():
        raise FileNotFoundError(f"Missing input path: {input_path}")
    if not report_template_path.exists():
        raise FileNotFoundError(f"Missing report template: {report_template_path}")

    sample_manifest = load_json(sample_manifest_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    run_id = f"public-demo-{sample_manifest['sample_id']}"
    index_path = index_path_for_input(input_path)
    reference_build = (
        sample_manifest.get("preferred_demo_input", {}).get("reference_build") or None
    )

    run_manifest = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "harness": args.harness,
        "reference_build": reference_build,
        "inputs": [
            {
                "path": str(input_path),
                "kind": kind_from_path(input_path),
                "sha256": sha256_file(input_path),
                "index_path": str(index_path) if index_path is not None else None,
            }
        ],
        "tool_versions": {
            "python": sys.version.split()[0],
            "public_demo_walkthrough": "0.1.0",
        },
        "notes": (
            f"Public demo intake for {sample_manifest['sample_id']}. "
            "Raw source file remains external to the repository."
        ),
    }

    sample_summary = {
        "sample_id": sample_manifest["sample_id"],
        "sex_call": None,
        "sample_count": 1,
        "contig_style": None,
        "coverage_summary": None,
        "notes": [
            f"Selected from {sample_manifest['source_profile_url']}.",
            "Public profile context is participant-supplied and should remain separate from deterministic findings.",
            "No automated build detection or variant interpretation has been performed yet.",
        ],
    }

    report_template = report_template_path.read_text(encoding="utf-8")
    report_text = render_report(
        report_template,
        {
            "sample_id": sample_manifest["sample_id"],
            "source_profile_url": sample_manifest["source_profile_url"],
            "input_path": str(input_path),
            "harness": args.harness,
        },
    )
    walkthrough_text = render_walkthrough(
        sample_manifest=sample_manifest,
        input_path=input_path,
        output_dir=output_dir,
        harness=args.harness,
    )

    (output_dir / "run_manifest.json").write_text(
        json.dumps(run_manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "sample_summary.json").write_text(
        json.dumps(sample_summary, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "report.md").write_text(report_text, encoding="utf-8")
    (output_dir / "walkthrough.md").write_text(walkthrough_text, encoding="utf-8")
    (output_dir / "commands.jsonl").write_text(
        json.dumps(
            {
                "tool": "public_demo_walkthrough",
                "command": [
                    "python",
                    "scripts/public_demo_walkthrough.py",
                    "--sample-manifest",
                    str(sample_manifest_path),
                    "--input-path",
                    str(input_path),
                    "--output-dir",
                    str(output_dir),
                    "--harness",
                    args.harness,
                ],
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "outputs": {
                    "run_manifest": str(output_dir / "run_manifest.json"),
                    "sample_summary": str(output_dir / "sample_summary.json"),
                    "report_md": str(output_dir / "report.md"),
                    "walkthrough_md": str(output_dir / "walkthrough.md"),
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
