## Goal

Create the first trustworthy manifest for a supplied VCF/BCF input.

## Procedure

1. Identify the file kind: `vcf`, `vcf.gz`, or `bcf`.
2. Check for the expected index (`.tbi` or `.csi`) where relevant.
3. Extract sample names and header metadata without modifying the raw input.
4. Hash the input files and record them in `run_manifest.json`.
5. Create a minimal `sample_summary.json` with unresolved fields set to `null`.

## Guardrails

- Never rewrite the source file in place.
- Do not guess the reference build from chromosome names alone if the evidence is weak.
- Multi-sample files require explicit sample-selection logic.

## Escalate when

- the file has no samples
- the header is malformed
- the file is compressed but unindexed
