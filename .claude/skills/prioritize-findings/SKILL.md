---
name: prioritize-findings
description: Convert raw annotations into ranked, evidence-linked findings. Use after
  annotation when building a structured report.
allowed-tools:
- Read
- Glob
- Grep
- Bash(python *)
- Bash(python3 *)
context: fork
---
# Prioritize findings

Convert raw annotations into ranked, evidence-linked findings. Use after annotation when building a structured report.

## When to use
- annotations are complete and need triage
- a user wants a ranked output instead of raw tables

## Do not use when
- annotation has not been completed

## Expected outputs
- `findings.json`
- `evidence.jsonl`

## Goal

Turn raw annotations into ranked findings with confidence labels and evidence refs.

## Procedure

1. Group candidate findings by category.
2. Assign one of the approved confidence labels:
   - `verified`
   - `strong`
   - `plausible`
   - `hypothesis`
   - `unsupported`
3. Attach at least one evidence ref to every kept finding.
4. Keep caveats adjacent to the finding instead of hiding them at the end.
5. Flag anything high-impact for human review.

## Guardrails

- Do not let a finding through without evidence.
- Do not over-rank exploratory trait signals.
- Separate deterministic QC findings from interpretation findings.

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

