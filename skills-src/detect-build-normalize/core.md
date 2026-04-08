## Goal

Resolve build and representation issues before downstream tools disagree.

## Procedure

1. Inspect contig style (`chr1` vs `1`) and obvious build indicators.
2. If build is still uncertain, mark it ambiguous rather than guessing.
3. Create a derived normalized file in a run-specific output directory.
4. Preserve raw input hashes and link the derived file back to them.
5. Record every normalization step in machine-readable notes.

## Guardrails

- Derived files belong under `runs/<run_id>/derived/`.
- Do not overwrite source inputs.
- If a liftover or reference swap would be needed, stop and surface that requirement.

## Escalate when

- the build is ambiguous
- contig naming is mixed
- normalization would drop or alter records unexpectedly
