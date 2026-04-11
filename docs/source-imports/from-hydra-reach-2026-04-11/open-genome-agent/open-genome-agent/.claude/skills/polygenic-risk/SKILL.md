---
name: polygenic-risk
description: Run optional polygenic or trait-style scoring workflows and label all
  outputs as probabilistic. Use only when requested and keep results separate from
  direct variant findings.
allowed-tools:
- Read
- Glob
- Grep
- Bash(python *)
- Bash(python3 *)
- Bash(plink2 *)
context: fork
---
# Polygenic risk

Run optional polygenic or trait-style scoring workflows and label all outputs as probabilistic. Use only when requested and keep results separate from direct variant findings.

## When to use
- the user explicitly requests PRS or broad predisposition scoring

## Do not use when
- the user expects diagnosis-like certainty
- the toolchain or reference score set is not available

## Expected outputs
- `prs_scores.json`
- `prs_notes.md`

## Goal

Run optional PRS-style analysis without letting probabilistic signals look clinical.

## Procedure

1. Confirm that the user explicitly wants this class of output.
2. Record which score set or method was used.
3. Present results as relative or exploratory signals only.
4. Keep PRS outputs in their own file and summary block.

## Guardrails

- Never merge PRS output into `verified` findings.
- Never present a timeline or certainty.
- If score portability is unclear, say so explicitly.

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

