## Goal

Validate that the local machine is ready for safe, reproducible genome analysis.

## Procedure

1. Detect the OS, shell, Python version, and writable workspace.
2. Check whether expected tools are present:
   - `python3`
   - `samtools`
   - `bcftools`
   - `vep`
   - `plink2`
   - `nextflow` (optional in the MVP)
3. Record versions and missing tools into a workstation report.
4. Verify that `runs/` exists and that raw genome paths are not inside `.git/`.
5. Confirm hook scripts are executable where relevant.

## Output contract

Emit a compact machine-readable report and a plain-language summary.
Missing tools should be reported explicitly instead of guessed around.

## Escalate when

- required tools are missing
- the repo is not trusted
- permissions or sandbox settings are unexpectedly broad
