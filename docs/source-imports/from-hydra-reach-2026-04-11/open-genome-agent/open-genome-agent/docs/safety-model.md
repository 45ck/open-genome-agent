# Safety model

## Threat model

A genome-analysis repo creates risks in four directions:

1. privacy leakage
2. overclaiming / false certainty
3. accidental execution or exfiltration
4. irreproducible results

The scaffold is designed to reduce all four.

## Rules

### Data handling

- Treat source genomes as read-only.
- Prefer local analysis.
- Do not upload genome files by default.
- Do not commit genome files to git.

### Reporting

- Separate strong findings from exploratory findings.
- Call out limitations before conclusions for high-impact categories.
- Always include provenance for each finding.
- Mark uncertain items explicitly.

### Medical boundary

- Do not present output as diagnosis.
- Do not tell a user they definitely have or will get a disease.
- Do not collapse research-grade PRS output into clinical-grade evidence.

### Agent behavior

- One writer at a time for shared outputs.
- Read-heavy parallelism is preferred.
- Hooks should log and harden, but schemas must also enforce quality.

## Confidence buckets

Recommended buckets:

- `verified`
- `strong`
- `plausible`
- `hypothesis`
- `unsupported`

Only the first two should appear in any top summary section.
