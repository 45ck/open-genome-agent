from __future__ import annotations

import argparse
import json

TOOLS = [
    "append_finding",
    "append_evidence",
    "get_run_index",
    "list_findings",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Evidence store MCP")
    parser.add_argument("--describe", action="store_true")
    args = parser.parse_args()

    if args.describe:
        print(
            json.dumps(
                {
                    "server": "evidence-store",
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
