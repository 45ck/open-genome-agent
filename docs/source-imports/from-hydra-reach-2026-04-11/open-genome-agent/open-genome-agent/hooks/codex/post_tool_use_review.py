from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import json

from hooks.common import log_event, read_json_stdin

def main() -> None:
    payload = read_json_stdin()
    log_event("codex-post-tool", payload)
    # Placeholder: later this can inspect stdout/stderr summaries.
    if payload.get("tool_name") == "Bash":
        print(json.dumps({
            "systemMessage": "Remember to capture command provenance for any artifact you keep."
        }))

if __name__ == "__main__":
    main()