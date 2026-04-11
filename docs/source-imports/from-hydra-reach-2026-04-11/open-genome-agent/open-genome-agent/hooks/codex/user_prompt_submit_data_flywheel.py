from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from hooks.common import log_event, read_json_stdin

def main() -> None:
    payload = read_json_stdin()
    log_event("codex-user-prompt", payload)

if __name__ == "__main__":
    main()