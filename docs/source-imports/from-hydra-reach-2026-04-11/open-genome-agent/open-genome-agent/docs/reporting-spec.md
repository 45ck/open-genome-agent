# Reporting spec

A completed run should create a folder like:

```text
runs/<timestamp>-<run-id>/
  run_manifest.json
  sample_summary.json
  findings.json
  evidence.jsonl
  commands.jsonl
  report.md
  report.html
```

## Required sections in `report.md`

1. Files analyzed
2. Tool versions and reference build
3. High-confidence findings
4. Probabilistic findings
5. Exploratory leads
6. Limitations
7. Human review required

## Required fields for each finding

See `schemas/finding.schema.json`.

At minimum, every finding must have:

- stable id
- category
- confidence
- evidence refs
- caveats
- human review flag
