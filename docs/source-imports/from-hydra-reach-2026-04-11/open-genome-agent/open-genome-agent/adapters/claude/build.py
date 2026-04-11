import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_shared import build_claude_runtime

def main() -> None:
    dist = ROOT / "adapters" / "claude" / "dist"
    if dist.exists():
        shutil.rmtree(dist)
    build_claude_runtime(dist)

if __name__ == "__main__":
    main()
