from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_shared import build_all, remove_tree

def main() -> None:
    # Build runtime files into the repository root
    build_all(ROOT)

    # Build exportable adapter bundles
    claude_dist = ROOT / "adapters" / "claude" / "dist"
    codex_dist = ROOT / "adapters" / "codex" / "dist"

    if claude_dist.exists():
        remove_tree(claude_dist)
    if codex_dist.exists():
        remove_tree(codex_dist)

    build_all(claude_dist)
    build_all(codex_dist)

    # Trim each adapter to its own surface
    codex_root = codex_dist
    for unwanted in [codex_root / ".claude", codex_root / "CLAUDE.md"]:
        if unwanted.exists():
            if unwanted.is_dir():
                remove_tree(unwanted)
            else:
                unwanted.unlink()

    claude_root = claude_dist
    for unwanted in [claude_root / ".codex", claude_root / ".agents", claude_root / "AGENTS.md"]:
        if unwanted.exists():
            if unwanted.is_dir():
                remove_tree(unwanted)
            else:
                unwanted.unlink()

    plugin_dir = codex_dist / ".codex-plugin"
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "README.md").write_text(
        "# Codex plugin placeholder\n\n"
        "Package the repo-local skills into a formal plugin here once the workflow stabilizes.\n",
        encoding="utf-8",
    )

if __name__ == "__main__":
    main()
