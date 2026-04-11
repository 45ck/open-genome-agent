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
