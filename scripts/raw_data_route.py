from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
RAW_INPUT_SCHEMA = json.loads(
    (ROOT / "schemas" / "raw-input-manifest.schema.json").read_text(encoding="utf-8")
)


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    validate(manifest, RAW_INPUT_SCHEMA)
    return manifest


def build_command(
    *,
    pipeline: str,
    profile: str,
    manifest_path: Path,
    output_dir: Path,
    reference_build: str,
) -> list[str]:
    return [
        "nextflow",
        "run",
        pipeline,
        "-profile",
        profile,
        "--input",
        str(manifest_path),
        "--outdir",
        str(output_dir / "pipeline_out"),
        "--genome",
        reference_build,
    ]


def write_outputs(
    *,
    output_dir: Path,
    manifest: dict[str, Any],
    command: list[str],
    executed: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    workflow_run = {
        "workflow_id": f"raw-route-{manifest['sample_id']}",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "pipeline": command[2],
        "executed": executed,
        "sample_id": manifest["sample_id"],
        "input_kind": manifest["input_kind"],
        "reference_build": manifest["reference_build"],
        "command": command,
        "notes": [
            "This workflow route is optional and should not replace the VCF-first path.",
            "A workflow launch is not equivalent to a successful completed run.",
        ],
    }
    (output_dir / "workflow_run.json").write_text(
        json.dumps(workflow_run, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "commands.jsonl").write_text(
        json.dumps(
            {
                "tool": "nextflow",
                "command": command,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "executed": executed,
                "outputs": {
                    "workflow_run": str(output_dir / "workflow_run.json"),
                    "pipeline_logs": str(output_dir / "pipeline_logs"),
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    logs_dir = output_dir / "pipeline_logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    (logs_dir / "README.md").write_text(
        "# Pipeline logs\n\n"
        "Store Nextflow logs, trace files, and provenance notes for long-running jobs here.\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare or optionally execute the guarded raw-data workflow route."
    )
    parser.add_argument(
        "--manifest",
        required=True,
        help="Path to a raw-input manifest JSON file.",
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where workflow provenance outputs should be written.",
    )
    parser.add_argument(
        "--pipeline",
        default="nf-core/sarek",
        help="Nextflow pipeline identifier.",
    )
    parser.add_argument(
        "--profile",
        default="docker",
        help="Nextflow profile string.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the composed Nextflow command instead of only preparing it.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    manifest_path = Path(args.manifest).resolve()
    output_dir = Path(args.output_dir).resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing raw-input manifest: {manifest_path}")

    manifest = load_manifest(manifest_path)
    command = build_command(
        pipeline=args.pipeline,
        profile=args.profile,
        manifest_path=manifest_path,
        output_dir=output_dir,
        reference_build=manifest["reference_build"],
    )
    if args.execute:
        subprocess.run(command, check=True)
    write_outputs(
        output_dir=output_dir,
        manifest=manifest,
        command=command,
        executed=args.execute,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
