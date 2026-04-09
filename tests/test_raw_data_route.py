from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.raw_data_route import build_command  # noqa: E402


class RawDataRouteTest(unittest.TestCase):
    def test_raw_input_manifest_schema(self) -> None:
        schema = json.loads(
            (ROOT / "schemas" / "raw-input-manifest.schema.json").read_text(
                encoding="utf-8"
            )
        )
        manifest = json.loads(
            (ROOT / "examples" / "raw-data" / "demo_raw_input_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        validate(manifest, schema)

    def test_build_command_targets_optional_nextflow_route(self) -> None:
        command = build_command(
            pipeline="nf-core/sarek",
            profile="docker",
            manifest_path=Path("D:/demo/input.json"),
            output_dir=Path("D:/demo/out"),
            reference_build="GRCh38",
        )
        self.assertEqual(command[:3], ["nextflow", "run", "nf-core/sarek"])
        self.assertIn("--input", command)
        self.assertIn("--outdir", command)

    def test_cli_writes_workflow_provenance_without_executing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/raw_data_route.py",
                    "--manifest",
                    "examples/raw-data/demo_raw_input_manifest.json",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                check=True,
            )
            workflow_run = json.loads(
                (output_dir / "workflow_run.json").read_text(encoding="utf-8")
            )
            commands = (output_dir / "commands.jsonl").read_text(encoding="utf-8")
            self.assertFalse(workflow_run["executed"])
            self.assertIn("nf-core/sarek", commands)
            self.assertTrue((output_dir / "pipeline_logs" / "README.md").exists())


if __name__ == "__main__":
    unittest.main()
