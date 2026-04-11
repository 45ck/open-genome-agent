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
