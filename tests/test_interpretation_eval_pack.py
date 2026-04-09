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

from scripts.interpretation_eval_pack import build_index  # noqa: E402


class InterpretationEvalPackTest(unittest.TestCase):
    def load_json(self, rel: str) -> dict:
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_case_files_validate_against_schema(self) -> None:
        schema = self.load_json("schemas/interpretation-case.schema.json")
        for rel in [
            "evals/interpretation/clinvar/cases.json",
            "evals/interpretation/pgx/cases.json",
            "evals/interpretation/prs/cases.json",
            "evals/interpretation/functional/cases.json",
        ]:
            cases = self.load_json(rel)
            self.assertIsInstance(cases, list)
            for case in cases:
                validate(case, schema)

    def test_build_index_counts_cases_by_module(self) -> None:
        index = build_index()
        self.assertEqual(index["modules"]["clinvar"]["case_count"], 2)
        self.assertEqual(index["modules"]["pgx"]["case_count"], 2)
        self.assertEqual(index["modules"]["prs"]["case_count"], 1)
        self.assertEqual(index["modules"]["functional"]["case_count"], 1)
        self.assertGreaterEqual(index["confidence_counts"]["plausible"], 1)

    def test_cli_writes_interpretation_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "out"
            subprocess.run(
                [
                    sys.executable,
                    "scripts/interpretation_eval_pack.py",
                    "--output-dir",
                    str(output_dir),
                ],
                cwd=ROOT,
                check=True,
            )
            index = json.loads((output_dir / "index.json").read_text(encoding="utf-8"))
            markdown = (output_dir / "index.md").read_text(encoding="utf-8")
            self.assertEqual(index["pack_id"], "interpretation-eval-pack")
            self.assertIn("Interpretation Evaluation Pack", markdown)
            self.assertIn("Modules", markdown)


if __name__ == "__main__":
    unittest.main()
