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
