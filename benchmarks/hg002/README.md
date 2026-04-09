# HG002 benchmark

Use HG002 as the first hard benchmark for correctness.

This directory defines the asset contract for:

- truth VCF inputs
- benchmark BED regions
- optional stratification files
- expected metric outputs such as precision, recall, and F1

The goal is to benchmark the repo against public truth data before any private genome workflow is considered complete.

## Benchmark command

Use the repo-local wrapper to either:

- execute `hap.py` against pinned HG002 truth inputs, or
- parse an existing `hap.py` `summary.csv` into repo-standard `metrics.json` and `index.html` outputs.

Execution mode:

```bash
python scripts/hg002_benchmark.py \
  --truth-vcf /path/to/HG002.truth.vcf.gz \
  --query-vcf /path/to/query.vcf.gz \
  --benchmark-bed /path/to/HG002.benchmark.bed \
  --reference-fasta /path/to/reference.fa \
  --output-dir runs/2026-04-09-demo/benchmarks/hg002 \
  --label hg002
```

Offline parse/render mode:

```bash
python scripts/hg002_benchmark.py \
  --summary-csv /path/to/happy.summary.csv \
  --output-dir runs/2026-04-09-demo/benchmarks/hg002 \
  --label hg002
```

The wrapper writes:

- `metrics.json`
- `index.html`
- `commands.jsonl` when `hap.py` is executed by the wrapper

Headline metrics prefer `PASS` rows when they exist. The full parsed summary table is preserved in `metrics.json`.
