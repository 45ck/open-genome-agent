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

from scripts.cmrg_evaluation import (
    parse_cmrg_scorecard,
    render_html_report,
)  # noqa: E402

SUMMARY_CSV = """Type,Filter,TRUTH.TOTAL,TRUTH.TP,TRUTH.FN,QUERY.TOTAL,QUERY.FP,QUERY.UNK,Recall,Precision,F1_Score
SNP,PASS,90,88,2,91,1,0,0.977778,0.967033,0.972376
INDEL,ALL,40,35,5,39,2,0,0.875,0.897436,0.886076
"""

GENE_RESULTS = """Gene\tStatus\tCoveragePct\tRecall\tPrecision\tF1_Score\tNotes
SMN1\tsupported\t99.5\t0.99\t0.98\t0.985\tDirectly benchmarked in CMRG regions
PMS2\tpartial\t75.0\t0.82\t0.90\t0.858\tCoverage is incomplete in repetitive sequence
CYP2D6\tnot_yet_trusted\t25.0\t\t\t\tNeeds additional validation before claims
"""


class CmrgEvaluationTest(unittest.TestCase):
    def test_parse_cmrg_scorecard_groups_genes_by_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            gene_results_path = temp_root / "genes.tsv"
            summary_path = temp_root / "summary.csv"
            gene_results_path.write_text(GENE_RESULTS, encoding="utf-8")
            summary_path.write_text(SUMMARY_CSV, encoding="utf-8")

            metrics = parse_cmrg_scorecard(
                gene_results_path=gene_results_path,
                label="demo-cmrg",
                summary_path=summary_path,
            )

            self.assertEqual(metrics["counts"]["supported"], 1)
            self.assertEqual(metrics["counts"]["partial"], 1)
            self.assertEqual(metrics["counts"]["not_yet_trusted"], 1)
            self.assertEqual(metrics["groups"]["supported"][0]["Gene"], "SMN1")
            self.assertIn("benchmark_summary", metrics)

    def test_render_html_report_includes_supported_boundary_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            gene_results_path = temp_root / "genes.tsv"
            gene_results_path.write_text(GENE_RESULTS, encoding="utf-8")
            metrics = parse_cmrg_scorecard(
                gene_results_path=gene_results_path,
                label="demo-cmrg",
            )

            html_report = render_html_report(metrics)

            self.assertIn("CMRG support boundaries", html_report)
            self.assertIn("Supported genes", html_report)
            self.assertIn("Not yet trusted", html_report)
            self.assertIn(
                "Only supported genes are inside the current proof surface.",
                html_report,
            )

    def test_cli_writes_scorecard_and_supported_genes_page(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            gene_results_path = temp_root / "genes.tsv"
            summary_path = temp_root / "summary.csv"
            output_dir = temp_root / "out"
            gene_results_path.write_text(GENE_RESULTS, encoding="utf-8")
            summary_path.write_text(SUMMARY_CSV, encoding="utf-8")

            subprocess.run(
                [
                    sys.executable,
                    "scripts/cmrg_evaluation.py",
                    "--gene-results",
                    str(gene_results_path),
                    "--summary-csv",
                    str(summary_path),
                    "--output-dir",
                    str(output_dir),
                    "--label",
                    "ci-cmrg",
                ],
                cwd=ROOT,
                check=True,
            )

            scorecard = json.loads(
                (output_dir / "scorecard.json").read_text(encoding="utf-8")
            )
            report = (output_dir / "index.html").read_text(encoding="utf-8")

            self.assertEqual(scorecard["label"], "ci-cmrg")
            self.assertEqual(scorecard["counts"]["supported"], 1)
            self.assertIn("Aggregate benchmark summary", report)
            self.assertFalse((output_dir / "commands.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
