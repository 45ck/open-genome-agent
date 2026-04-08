---
name: annotate-variants
description: Annotate variants with deterministic tools such as VEP and preserve exact
  tool versions and command provenance. Use after normalization and before prioritization.
allowed-tools:
- Read
- Glob
- Grep
- Bash(python *)
- Bash(python3 *)
- Bash(vep *)
- Bash(bcftools *)
context: fork
---
# Annotate variants

Annotate variants with deterministic tools such as VEP and preserve exact tool versions and command provenance. Use after normalization and before prioritization.

## When to use
- gene/transcript consequences are needed
- you need a structured annotation file for later ranking

## Do not use when
- you only need simple file QC

## Expected outputs
- `annotations.tsv`
- `tool_versions.json`
- `commands.jsonl`

## Goal

Produce a structured annotation layer that downstream agents can rank and report.

## Procedure

1. Confirm build and normalization state first.
2. Run the selected annotation tool with explicit version capture.
3. Preserve raw command lines and output paths in `commands.jsonl`.
4. Emit a stable tabular or JSON annotation artifact.
5. Keep tool failures visible and non-silent.

## Guardrails

- Annotation is not interpretation.
- Do not collapse multiple transcripts into a single unqualified claim.
- Record exact tool and cache versions when available.

## Escalate when

- required annotation caches are missing
- reference build does not match tool expectations
- command output suggests truncation or partial failure

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

