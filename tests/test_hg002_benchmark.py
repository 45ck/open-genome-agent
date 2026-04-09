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

from scripts.hg002_benchmark import (
    parse_happy_summary,
    render_html_report,
)  # noqa: E402

SUMMARY_CSV = """Type,Filter,TRUTH.TOTAL,TRUTH.TP,TRUTH.FN,QUERY.TOTAL,QUERY.FP,QUERY.UNK,Recall,Precision,F1_Score
SNP,ALL,100,99,1,101,2,0,0.99,0.980198,0.985074
SNP,PASS,90,89,1,90,1,0,0.988889,0.988889,0.988889
INDEL,ALL,50,47,3,49,2,0,0.94,0.959184,0.949495
"""


class Hg002BenchmarkTest(unittest.TestCase):
    def test_parse_happy_summary_prefers_pass_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            summary_path = Path(tmpdir) / "example.summary.csv"
            summary_path.write_text(SUMMARY_CSV, encoding="utf-8")

            metrics = parse_happy_summary(summary_path, label="demo")

            self.assertEqual(metrics["headline"]["SNP"]["Filter"], "PASS")
            self.assertEqual(metrics["headline"]["INDEL"]["Filter"], "ALL")
            self.assertEqual(metrics["headline"]["SNP"]["TRUTH.TP"], 89)

    def test_render_html_report_includes_headline_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            summary_path = Path(tmpdir) / "example.summary.csv"
            summary_path.write_text(SUMMARY_CSV, encoding="utf-8")
            metrics = parse_happy_summary(summary_path, label="demo")

            html_report = render_html_report(metrics)

            self.assertIn("HG002 Benchmark Summary", html_report)
            self.assertIn("F1: 0.988889", html_report)
            self.assertIn("INDEL", html_report)

    def test_cli_parses_existing_summary_and_writes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            summary_path = temp_root / "example.summary.csv"
            output_dir = temp_root / "out"
            summary_path.write_text(SUMMARY_CSV, encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "scripts/hg002_benchmark.py",
                    "--summary-csv",
                    str(summary_path),
                    "--output-dir",
                    str(output_dir),
                    "--label",
                    "ci-demo",
                ],
                cwd=ROOT,
                check=True,
            )

            metrics = json.loads(
                (output_dir / "metrics.json").read_text(encoding="utf-8")
            )
            html_report = (output_dir / "index.html").read_text(encoding="utf-8")
            self.assertEqual(metrics["label"], "ci-demo")
            self.assertIn("SNP", metrics["headline"])
            self.assertIn("HG002 Benchmark Summary", html_report)
            self.assertFalse((output_dir / "commands.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
