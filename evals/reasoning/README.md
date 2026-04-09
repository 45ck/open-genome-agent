# Reasoning evaluation

Reasoning evaluation measures whether the agent:

- cites the right evidence class
- preserves caveats
- avoids unsupported conclusions
- keeps benchmark truth and interpretation claims distinct

VariantBench or an equivalent internal harness should live behind the manifests in this directory.

This repo includes an internal `VariantBench-lite` scaffold:

- `cases/variantbench-lite.json`
- `results.schema.json`
- `scripts/reasoning_eval.py`

Build a comparison report with:

```bash
python scripts/reasoning_eval.py \
  --results-jsonl runs/demo/codex.jsonl \
  --results-jsonl runs/demo/claude.jsonl \
  --output-dir runs/2026-04-09-demo/evals/reasoning
```
