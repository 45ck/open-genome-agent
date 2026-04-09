# Interpretation evaluation

Interpretation should be tested separately from parser correctness.

This directory defines the public source packs for:

- ClinVar-backed variant assertions
- CPIC and PharmVar pharmacogenomics cases
- PGS Catalog score demonstrations
- MaveDB functional evidence examples

Each pack should stay evidence-bound and versioned.

Included packs:

- `clinvar/cases.json`
- `pgx/cases.json`
- `prs/cases.json`
- `functional/cases.json`
- `evidence-grading-rubric.md`

Build the combined pack index with:

```bash
python scripts/interpretation_eval_pack.py \
  --output-dir runs/2026-04-09-demo/evals/interpretation
```
