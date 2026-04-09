# CLI Provenance Demo

This transcript shows the intended shape of a local-first demo on a public genome file.

```text
$ python scripts/public_demo_walkthrough.py \
    --sample-manifest benchmarks/public-demos/huFE0257-manifest.json \
    --input-path /data/public/huFE0257.veritas.vcf.gz \
    --output-dir runs/2026-04-09-huFE0257-demo/intake \
    --harness codex

Wrote:
  runs/2026-04-09-huFE0257-demo/intake/run_manifest.json
  runs/2026-04-09-huFE0257-demo/intake/sample_summary.json
  runs/2026-04-09-huFE0257-demo/intake/report.md
  runs/2026-04-09-huFE0257-demo/intake/walkthrough.md
  runs/2026-04-09-huFE0257-demo/intake/commands.jsonl

$ python scripts/hg002_benchmark.py \
    --summary-csv fixtures/happy.example.summary.csv \
    --output-dir runs/2026-04-09-demo/benchmarks/hg002 \
    --label hg002

Wrote:
  runs/2026-04-09-demo/benchmarks/hg002/metrics.json
  runs/2026-04-09-demo/benchmarks/hg002/index.html

$ python scripts/cmrg_evaluation.py \
    --gene-results fixtures/cmrg_gene_results.tsv \
    --summary-csv fixtures/cmrg.summary.csv \
    --output-dir runs/2026-04-09-demo/benchmarks/cmrg \
    --label cmrg

Wrote:
  runs/2026-04-09-demo/benchmarks/cmrg/scorecard.json
  runs/2026-04-09-demo/benchmarks/cmrg/index.html
```

The point of the demo is provenance, not theatrics:

- every output is file-backed
- public-demo intake stays local
- benchmark and interpretation artifacts stay separate
- limitations remain visible in the generated reports
