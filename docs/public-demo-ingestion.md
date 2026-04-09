# Public Demo Ingestion

Use the public-demo flow only with explicitly open Harvard PGP profiles.

The first selected sample is `huFE0257`:

- profile: `https://my.pgp-hms.org/profile/huFE0257`
- preferred input: 2018-11-26 Veritas Genetics VCF
- reference build: `b37`

## Ingestion rules

1. Verify the public profile and reuse language before downloading anything.
2. Download the genome file manually to a local path outside the repository or into an ignored workspace path.
3. Keep the raw file read-only.
4. Generate repo artifacts from the local copy rather than moving or rewriting the source file.

## Recommended local layout

```text
runs/
  2026-04-09-huFE0257-demo/
    raw/
      huFE0257.veritas.vcf.gz
      huFE0257.veritas.vcf.gz.tbi
    intake/
      run_manifest.json
      sample_summary.json
      walkthrough.md
      commands.jsonl
```

## Walkthrough bootstrap

Use the repo-local helper to create the intake pack:

```bash
python scripts/public_demo_walkthrough.py \
  --sample-manifest benchmarks/public-demos/huFE0257-manifest.json \
  --input-path /absolute/path/to/huFE0257.veritas.vcf.gz \
  --output-dir runs/2026-04-09-huFE0257-demo/intake \
  --harness codex
```

The helper writes:

- `run_manifest.json`
- `sample_summary.json`
- `report.md`
- `walkthrough.md`
- `commands.jsonl`

## Next-stage work after intake

After the intake pack exists, continue with the local-first workflow:

1. validate the file and index state
2. detect build and normalize a derived copy
3. answer a few targeted queries on known genes or variants
4. only then move on to annotation and report assembly

If build or sample identity is ambiguous, stop and record the ambiguity in the run notes.
