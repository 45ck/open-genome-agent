# 1000 Genomes scale workflow

Use the 1000 Genomes scaffold after the single-sample public-demo flow is stable.

This directory covers:

- a pinned starter cohort manifest
- a batch-summary script that rolls up local sample summaries
- a population-aware HTML summary
- throughput accounting for public cohort runs

## Batch summary command

```bash
python scripts/public_cohort_batch.py \
  --sample-manifest benchmarks/1000g/sample-manifest.json \
  --sample-summary runs/demo/HG00096/sample_summary.json \
  --sample-summary runs/demo/NA18522/sample_summary.json \
  --sample-summary runs/demo/HG02408/sample_summary.json \
  --output-dir runs/2026-04-09-demo/benchmarks/1000g \
  --elapsed-seconds 90
```

The script writes:

- `summary.json`
- `index.html`

Keep the generated page explicit about:

- which populations appear in the selected cohort
- what was and was not actually measured
- why population labels are context rather than destiny
