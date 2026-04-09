from __future__ import annotations

import argparse
import json

TOOLS = [
    "run_workflow",
    "workflow_status",
    "tail_logs",
    "cancel_workflow",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Workflow MCP")
    parser.add_argument("--describe", action="store_true")
    args = parser.parse_args()

    if args.describe:
        print(
            json.dumps(
                {
                    "server": "workflow",
                    "tools": TOOLS,
                    "status": "stub",
                },
                indent=2,
            )
        )
    else:
        print("Stub MCP server. Run with --describe for a machine-readable summary.")


if __name__ == "__main__":
    main()
