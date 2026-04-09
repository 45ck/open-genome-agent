from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hooks.common import log_event, read_json_stdin  # noqa: E402


def main() -> None:
    payload = read_json_stdin()
    log_event("codex-session-start", payload)
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": "Genome analysis repo: keep raw inputs read-only, separate strong findings from PRS-style output, and keep evidence for every claim.",
                }
            }
        )
    )


if __name__ == "__main__":
    main()
