from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import json

from hooks.common import bash_command, blocked_reason, log_event, read_json_stdin

def main() -> None:
    payload = read_json_stdin()
    command = bash_command(payload)
    reason = blocked_reason(command)
    log_event("codex-pre-tool", payload, {"command": command, "blocked_hint": bool(reason)})

    if reason:
        print(json.dumps({
            "systemMessage": reason
        }))

if __name__ == "__main__":
    main()