## Goal

Handle heavy pipeline execution in a reproducible way.

## Procedure

1. Confirm that pipeline execution is explicitly requested.
2. Validate environment assumptions before running anything expensive.
3. Prefer schema-driven configuration and captured manifests over handwritten one-off commands.
4. Save pipeline commands, params, and logs into the run directory.

## Guardrails

- Do not run large workflows implicitly.
- Do not treat a pipeline launch as success; monitor completion and surface failures.
- Keep this skill separate from lightweight local questioning.
