from __future__ import annotations

import argparse
import json

TOOLS = [
    "list_inputs",
    "query_region",
    "list_samples",
    "coverage_summary",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Genome files MCP")
    parser.add_argument("--describe", action="store_true")
    args = parser.parse_args()

    if args.describe:
        print(
            json.dumps(
                {
                    "server": "genome-files",
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
