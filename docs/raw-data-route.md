# Optional Raw-Data Route

The raw-data route is intentionally optional.

Use it only when:

- the user explicitly requests raw-read or alignment-based processing
- the environment is ready for Nextflow
- the VCF-first path is not sufficient for the task

## Workflow scaffold

```bash
python scripts/raw_data_route.py \
  --manifest examples/raw-data/demo_raw_input_manifest.json \
  --output-dir runs/2026-04-09-demo/raw-route \
  --pipeline nf-core/sarek \
  --profile docker
```

This writes:

- `workflow_run.json`
- `commands.jsonl`
- `pipeline_logs/README.md`

The script prepares the workflow command and provenance by default. It does not execute the pipeline unless `--execute` is provided.

## Guardrails

- keep raw inputs outside the repo
- keep the VCF-first path first-class
- capture command provenance before treating a workflow launch as meaningful progress
- do not present a launched workflow as completed analysis
