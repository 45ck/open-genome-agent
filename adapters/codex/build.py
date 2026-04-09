import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_shared import build_codex_runtime, remove_tree  # noqa: E402


def main() -> None:
    dist = ROOT / "adapters" / "codex" / "dist"
    if dist.exists():
        remove_tree(dist)
    build_codex_runtime(dist)
    plugin_dir = dist / ".codex-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "README.md").write_text(
        "# Codex plugin placeholder\n\n"
        "Package the repo-local skills into a formal plugin here once the workflow stabilizes.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
