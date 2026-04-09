from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_shared import remove_tree  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python adapters/codex/install.py /path/to/target-repo")
        raise SystemExit(2)

    target = Path(sys.argv[1]).resolve()
    dist = ROOT / "adapters" / "codex" / "dist"

    if not dist.exists():
        raise SystemExit("Run `python adapters/codex/build.py` first.")

    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dist / "AGENTS.md", target / "AGENTS.md")

    dst_agents = target / ".agents"
    if dst_agents.exists():
        remove_tree(dst_agents)
    shutil.copytree(dist / ".agents", dst_agents)

    dst_codex = target / ".codex"
    if dst_codex.exists():
        remove_tree(dst_codex)
    shutil.copytree(dist / ".codex", dst_codex)

    print(f"Installed Codex adapter into {target}")


if __name__ == "__main__":
    main()
