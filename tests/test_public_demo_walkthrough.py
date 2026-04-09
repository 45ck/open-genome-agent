from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


class PublicDemoWalkthroughTest(unittest.TestCase):
    def load_json(self, rel: str) -> dict:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_walkthrough_script_writes_schema_valid_intake_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            input_path = temp_root / "huFE0257.vcf.gz"
            output_dir = temp_root / "out"
            input_path.write_bytes(b"##fileformat=VCFv4.2\n")
            (temp_root / "huFE0257.vcf.gz.tbi").write_bytes(b"index")

            subprocess.run(
                [
                    sys.executable,
                    "scripts/public_demo_walkthrough.py",
                    "--sample-manifest",
                    "benchmarks/public-demos/huFE0257-manifest.json",
                    "--input-path",
                    str(input_path),
                    "--output-dir",
                    str(output_dir),
                    "--harness",
                    "codex",
                ],
                cwd=ROOT,
                check=True,
            )

            run_manifest = json.loads(
                (output_dir / "run_manifest.json").read_text(encoding="utf-8")
            )
            sample_summary = json.loads(
                (output_dir / "sample_summary.json").read_text(encoding="utf-8")
            )
            report_text = (output_dir / "report.md").read_text(encoding="utf-8")
            walkthrough_text = (output_dir / "walkthrough.md").read_text(
                encoding="utf-8"
            )

            validate(run_manifest, self.load_json("schemas/run-manifest.schema.json"))
            validate(
                sample_summary, self.load_json("schemas/sample-summary.schema.json")
            )
            self.assertEqual(sample_summary["sample_id"], "huFE0257")
            self.assertEqual(run_manifest["harness"], "codex")
            self.assertEqual(run_manifest["run_id"], "public-demo-huFE0257")
            self.assertIn("huFE0257", report_text)
            self.assertIn("What this intake pack proves", walkthrough_text)
            self.assertTrue((output_dir / "commands.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
