# CMRG benchmark

Use the Challenging Medically Relevant Genes benchmark after HG002 is stable.

This directory scopes the medically difficult regions benchmark so the repo can distinguish:

- genes with explicit benchmark support
- genes with partial support
- genes that remain outside the supported proof surface

## Evaluation command

Use the repo-local CMRG wrapper to:

- optionally execute `hap.py` over the CMRG benchmark BED, and
- always render a per-gene scorecard plus supported-genes page from a structured gene results file.

The required gene results file should include:

- `Gene`
- `Status`
- optional metric columns such as `CoveragePct`, `Recall`, `Precision`, `F1_Score`, and `Notes`

Supported `Status` values are:

- `supported`
- `partial`
- `not_yet_trusted`

Offline parse/render mode:

```bash
python scripts/cmrg_evaluation.py \
  --gene-results /path/to/cmrg_gene_results.tsv \
  --summary-csv /path/to/cmrg.summary.csv \
  --output-dir runs/2026-04-09-demo/benchmarks/cmrg \
  --label cmrg
```

Execution mode:

```bash
python scripts/cmrg_evaluation.py \
  --gene-results /path/to/cmrg_gene_results.tsv \
  --truth-vcf /path/to/HG002.truth.vcf.gz \
  --query-vcf /path/to/query.vcf.gz \
  --benchmark-bed /path/to/cmrg_regions.bed \
  --reference-fasta /path/to/reference.fa \
  --output-dir runs/2026-04-09-demo/benchmarks/cmrg \
  --label cmrg
```

The wrapper writes:

- `scorecard.json`
- `index.html`
- `commands.jsonl` when `hap.py` is executed by the wrapper

Only genes in the `supported` bucket should be treated as inside the current public proof surface.
