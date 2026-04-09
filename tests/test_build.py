from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class BuildTest(unittest.TestCase):
    def test_build_outputs_exist(self) -> None:
        subprocess.run([sys.executable, "scripts/build_all.py"], cwd=ROOT, check=True)

        expected = [
            ROOT / "CLAUDE.md",
            ROOT / "AGENTS.md",
            ROOT / ".claude" / "settings.json",
            ROOT / ".claude" / "skills" / "ingest-vcf" / "SKILL.md",
            ROOT / ".claude" / "agents" / "orchestrator.md",
            ROOT / ".agents" / "skills" / "ingest-vcf" / "SKILL.md",
            ROOT / ".codex" / "config.toml",
            ROOT / ".codex" / "agents" / "orchestrator.toml",
            ROOT
            / "adapters"
            / "claude"
            / "dist"
            / ".claude"
            / "skills"
            / "ingest-vcf"
            / "SKILL.md",
            ROOT
            / "adapters"
            / "codex"
            / "dist"
            / ".codex"
            / "agents"
            / "orchestrator.toml",
        ]
        for path in expected:
            self.assertTrue(path.exists(), f"Missing expected file: {path}")


if __name__ == "__main__":
    unittest.main()
