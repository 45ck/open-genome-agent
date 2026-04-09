from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from hooks.common import log_event, read_json_stdin, repo_root_from_cwd  # noqa: E402


def main() -> None:
    payload = read_json_stdin()
    root = repo_root_from_cwd(payload)
    findings = list((root / "runs").glob("**/findings.json"))
    log_event("codex-stop", payload, {"findings_seen": len(findings)})

    if not findings:
        print(
            json.dumps(
                {
                    "continue": True,
                    "systemMessage": "No findings artifact was detected. If this was a planning or setup session, state that clearly in the final output.",
                }
            )
        )


if __name__ == "__main__":
    main()
