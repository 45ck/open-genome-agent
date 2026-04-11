---
name: pharmacogenomics
description: Generate a clearly separated pharmacogenomics section with conservative
  language and explicit human-review flags. Use only when the user requests drug-response
  analysis.
---
# Pharmacogenomics

Generate a clearly separated pharmacogenomics section with conservative language and explicit human-review flags. Use only when the user requests drug-response analysis.

## When to use
- the user explicitly requests drug-response or medication-response clues

## Do not use when
- the user only wants ancestry or general variant analysis

## Expected outputs
- `pharmacogenomics.json`

## Goal

Produce a conservative drug-response section that remains clearly separate from diagnosis.

## Procedure

1. Start from already validated variant or haplotype inputs.
2. Present outputs as medication-response clues, not prescriptions.
3. Attach strong caveats and a human-review flag to every entry.
4. Keep the output in its own artifact and section.

## Guardrails

- Never tell the user to change medication directly from this output.
- Never mix pharmacogenomics entries into the same summary bucket as disease findings.
- If genotype-to-phenotype translation is incomplete, say so.

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

