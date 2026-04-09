from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


class SchemaValidationTest(unittest.TestCase):
    def load_json(self, rel: str):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_run_manifest(self) -> None:
        validate(
            self.load_json("examples/reports/demo_run_manifest.json"),
            self.load_json("schemas/run-manifest.schema.json"),
        )

    def test_sample_summary(self) -> None:
        validate(
            self.load_json("examples/reports/demo_sample_summary.json"),
            self.load_json("schemas/sample-summary.schema.json"),
        )

    def test_findings(self) -> None:
        schema = self.load_json("schemas/finding.schema.json")
        findings = self.load_json("examples/reports/demo_findings.json")
        for item in findings:
            validate(item, schema)

    def test_report_index(self) -> None:
        validate(
            self.load_json("examples/reports/demo_report-index.json"),
            self.load_json("schemas/report-index.schema.json"),
        )


if __name__ == "__main__":
    unittest.main()
