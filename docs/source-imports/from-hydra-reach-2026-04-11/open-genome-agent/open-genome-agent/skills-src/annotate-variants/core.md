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
