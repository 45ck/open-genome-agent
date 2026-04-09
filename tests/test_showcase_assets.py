from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ShowcaseAssetsTest(unittest.TestCase):
    def test_showcase_assets_exist(self) -> None:
        required = [
            ROOT / "assets" / "proof-program" / "hg002-benchmark-card.svg",
            ROOT / "assets" / "proof-program" / "public-demo-card.svg",
            ROOT / "docs" / "cli-provenance-demo.md",
            ROOT / "docs" / "what-we-do-not-claim.md",
        ]
        for path in required:
            self.assertTrue(path.exists(), f"Missing showcase asset: {path}")

    def test_readme_links_proof_assets(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("assets/proof-program/hg002-benchmark-card.svg", readme)
        self.assertIn("assets/proof-program/public-demo-card.svg", readme)
        self.assertIn("docs/cli-provenance-demo.md", readme)
        self.assertIn("docs/what-we-do-not-claim.md", readme)


if __name__ == "__main__":
    unittest.main()
