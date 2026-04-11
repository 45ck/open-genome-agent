---
name: generate-report
description: Assemble structured findings and evidence into a human-readable report
  plus machine-readable index. Use after prioritization is finished.
---
# Generate report

Assemble structured findings and evidence into a human-readable report plus machine-readable index. Use after prioritization is finished.

## When to use
- findings.json and evidence.jsonl exist
- a human-readable deliverable is required

## Do not use when
- upstream analysis is still missing

## Expected outputs
- `report.md`
- `report.html`
- `report-index.json`

## Goal

Turn structured artifacts into a concise report with a clear evidence ladder.

## Procedure

1. Load the manifest, summary, findings, and evidence artifacts.
2. Group findings by confidence and category.
3. Put strong items first, then probabilistic items, then exploratory leads.
4. End with limitations and required human review.
5. Emit `report.md`, optional `report.html`, and a machine-readable report index.

## Guardrails

- Do not invent missing evidence.
- Do not hide ambiguity.
- If upstream artifacts are missing, stop and state which ones are missing.

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

