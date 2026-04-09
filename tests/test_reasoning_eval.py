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

from scripts.reasoning_eval import build_summary  # noqa: E402


class ReasoningEvalTest(unittest.TestCase):
    def test_results_schema_validates_rows(self) -> None:
        schema = json.loads(
            (ROOT / "evals" / "reasoning" / "results.schema.json").read_text(
                encoding="utf-8"
            )
        )
        row = {
            "case_id": "vb-lite-clinvar-pathogenic",
            "backend": "codex",
            "evidence_alignment_score": 0.9,
            "unsupported_claims": 0,
            "contradictions": 0,
            "source_class_correct": True,
        }
        validate(row, schema)

    def test_build_summary_compares_backends(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            results_path = temp_root / "results.jsonl"
            results_path.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "case_id": "vb-lite-clinvar-pathogenic",
                                "backend": "codex",
                                "evidence_alignment_score": 0.9,
                                "unsupported_claims": 0,
                                "contradictions": 0,
                                "source_class_correct": True,
                            }
                        ),
                        json.dumps(
                            {
                                "case_id": "vb-lite-prs-boundary",
                                "backend": "claude",
                                "evidence_alignment_score": 0.7,
                                "unsupported_claims": 1,
                                "contradictions": 0,
                                "source_class_correct": True,
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            summary = build_summary([results_path])
            self.assertEqual(summary["backend_count"], 2)
            self.assertEqual(summary["backends"]["codex"]["failure_count"], 0)
            self.assertEqual(summary["backends"]["claude"]["failure_count"], 1)

    def test_cli_writes_reasoning_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = Path(tmpdir)
            results_path = temp_root / "results.jsonl"
            output_dir = temp_root / "out"
            results_path.write_text(
                json.dumps(
                    {
                        "case_id": "vb-lite-clinvar-pathogenic",
                        "backend": "codex",
                        "evidence_alignment_score": 0.95,
                        "unsupported_claims": 0,
                        "contradictions": 0,
                        "source_class_correct": True,
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            subprocess.run(
                [
                    sys.executable,
                    "scripts/reasoning_eval.py",
                    "--results-jsonl",
                    str(results_path),
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                check=True,
            )
            summary = json.loads(
                (output_dir / "summary.json").read_text(encoding="utf-8")
            )
            comparison = (output_dir / "comparison.md").read_text(encoding="utf-8")
            self.assertEqual(summary["pack_id"], "reasoning-eval-pack")
            self.assertIn("Reasoning Evaluation", comparison)


if __name__ == "__main__":
    unittest.main()
