from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import validate  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]


class ProofProgramScaffoldTest(unittest.TestCase):
    def load_json(self, rel: str):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def test_required_manifests_exist(self) -> None:
        required = [
            ROOT / "benchmarks" / "hg002" / "manifest.json",
            ROOT / "benchmarks" / "cmrg" / "manifest.json",
            ROOT / "benchmarks" / "public-demos" / "harvard-pgp-manifest.json",
            ROOT / "benchmarks" / "1000g" / "manifest.json",
            ROOT / "evals" / "interpretation" / "manifest.json",
            ROOT / "evals" / "reasoning" / "manifest.json",
            ROOT / "scripts" / "bootstrap_beads_backlog.py",
        ]
        for path in required:
            self.assertTrue(path.exists(), f"Missing proof-program scaffold: {path}")

    def test_manifests_follow_schema(self) -> None:
        schema = self.load_json("schemas/asset-manifest.schema.json")
        manifests = [
            "benchmarks/hg002/manifest.json",
            "benchmarks/cmrg/manifest.json",
            "benchmarks/public-demos/harvard-pgp-manifest.json",
            "benchmarks/1000g/manifest.json",
            "evals/interpretation/manifest.json",
            "evals/reasoning/manifest.json",
        ]
        for rel in manifests:
            validate(self.load_json(rel), schema)


if __name__ == "__main__":
    unittest.main()
