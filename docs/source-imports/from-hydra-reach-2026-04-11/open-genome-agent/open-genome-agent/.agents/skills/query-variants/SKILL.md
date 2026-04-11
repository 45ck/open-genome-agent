---
name: query-variants
description: Answer targeted questions about genes, rsIDs, coordinates, or variant
  panels from local genome files. Use for focused exploration before full reporting.
---
# Query variants

Answer targeted questions about genes, rsIDs, coordinates, or variant panels from local genome files. Use for focused exploration before full reporting.

## When to use
- the user asks about a gene, variant, or coordinate range
- you need quick local evidence without running a full pipeline

## Do not use when
- a full end-to-end report is required

## Expected outputs
- `query_results.tsv`
- `query_notes.md`

## Goal

Answer targeted local questions quickly and with file-level provenance.

## Procedure

1. Convert the user request into a precise local query:
   - gene
   - rsID
   - coordinate interval
   - panel list
2. Prefer exact local evidence over speculative interpretation.
3. Return raw hits, file locations, and concise caveats.
4. If nothing matches, say so directly.

## Guardrails

- Keep scope narrow.
- Do not turn a simple query into a full report unless asked.
- If a query depends on annotation that is not yet available, state that dependency.

## Output contract

Emit query results plus a short note describing how the query was executed.

## References
See `references/README.md` for durable notes and `scripts/` for deterministic helpers.

