from __future__ import annotations

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_shared import remove_tree

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python adapters/claude/install.py /path/to/target-repo")
        raise SystemExit(2)

    target = Path(sys.argv[1]).resolve()
    dist = ROOT / "adapters" / "claude" / "dist"

    if not dist.exists():
        raise SystemExit("Run `python adapters/claude/build.py` first.")

    target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(dist / "CLAUDE.md", target / "CLAUDE.md")

    dst_claude = target / ".claude"
    if dst_claude.exists():
        remove_tree(dst_claude)
    shutil.copytree(dist / ".claude", dst_claude)

    print(f"Installed Claude adapter into {target}")

if __name__ == "__main__":
    main()
