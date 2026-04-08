from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

BLOCKED_PATTERNS = [
    "curl ",
    "wget ",
    "scp ",
    "rsync ",
    "nc ",
    "netcat ",
]

def read_json_stdin() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_raw": raw}

def repo_root_from_cwd(payload: dict) -> Path:
    cwd = payload.get("cwd")
    if cwd:
        return Path(cwd)
    return Path.cwd()

def append_jsonl(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def log_event(channel: str, payload: dict, extra: dict | None = None) -> None:
    root = repo_root_from_cwd(payload)
    log_path = root / "runs" / "hook-events.jsonl"
    data = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "channel": channel,
        "hook_event_name": payload.get("hook_event_name"),
        "tool_name": payload.get("tool_name"),
        "cwd": payload.get("cwd"),
    }
    if extra:
        data.update(extra)
    append_jsonl(log_path, data)

def bash_command(payload: dict) -> str:
    tool_input = payload.get("tool_input") or {}
    if isinstance(tool_input, dict):
        return tool_input.get("command", "") or ""
    return ""

def blocked_reason(command: str) -> str | None:
    normalized = f" {command.strip().lower()} "
    for pat in BLOCKED_PATTERNS:
        if pat in normalized:
            return f"Blocked potentially unsafe network or copy command: {pat.strip()}"
    return None
