---
name: nextflow-runner
description: Run or prepare reproducible Nextflow workflows for heavy genomics jobs.
  Use only for explicit workflow execution, not routine question answering.
---
# Nextflow runner

Run or prepare reproducible Nextflow workflows for heavy genomics jobs. Use only for explicit workflow execution, not routine question answering.

## When to use
- raw-read or heavy pipeline execution is explicitly requested
- the environment is ready for Nextflow

## Do not use when
- a VCF-first local analysis is sufficient

## Expected outputs
- `workflow_run.json`
- `pipeline_logs/`

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

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

