from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.public_cohort_batch import build_summary  # noqa: E402


class PublicCohortBatchTest(unittest.TestCase):
    def test_build_summary_groups_samples_by_population(self) -> None:
        manifest = json.loads(
            (ROOT / "benchmarks" / "1000g" / "sample-manifest.json").read_text(
                encoding="utf-8"
            )
        )
        sample_summaries = [
            {"sample_id": "HG00096"},
            {"sample_id": "NA18522"},
            {"sample_id": "HG02408"},
        ]
        summary = build_summary(
            sample_manifest=manifest,
            sample_summaries=sample_summaries,
            elapsed_seconds=90.0,
        )
        self.assertEqual(summary["processed_sample_count"], 3)
        self.assertEqual(summary["super_population_counts"]["EUR"], 1)
        self.assertEqual(summary["super_population_counts"]["AFR"], 1)
        self.assertEqual(summary["super_population_counts"]["EAS"], 1)
        self.assertEqual(summary["throughput"]["samples_per_minute"], 2.0)

    def test_cli_writes_batch_summary_and_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            output_dir = temp_root / "out"
            sample_paths = []
            for sample_id in ["HG00096", "NA18522", "HG02408"]:
                path = temp_root / f"{sample_id}.json"
                path.write_text(
                    json.dumps({"sample_id": sample_id}, indent=2) + "\n",
                    encoding="utf-8",
                )
                sample_paths.append(path)

            command = [
                sys.executable,
                "scripts/public_cohort_batch.py",
                "--sample-manifest",
                "benchmarks/1000g/sample-manifest.json",
                "--output-dir",
                str(output_dir),
                "--elapsed-seconds",
                "90",
            ]
            for path in sample_paths:
                command.extend(["--sample-summary", str(path)])

            subprocess.run(command, cwd=ROOT, check=True)

            summary = json.loads(
                (output_dir / "summary.json").read_text(encoding="utf-8")
            )
            html = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertEqual(summary["processed_sample_count"], 3)
            self.assertIn("1000 Genomes batch summary", html)
            self.assertIn("Population-aware summary", html)


if __name__ == "__main__":
    unittest.main()
