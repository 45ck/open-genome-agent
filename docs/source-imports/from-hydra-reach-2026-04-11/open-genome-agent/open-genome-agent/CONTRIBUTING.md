# Contributing

## Principles

Contributions should strengthen one or more of these properties:

- deterministic behavior
- provenance and reproducibility
- safety around personal genomic data
- cross-harness portability
- clear separation between strong evidence and weak inference

## Before opening a pull request

1. Run the build:
   ```bash
   python scripts/build_all.py
   ```
2. Run tests:
   ```bash
   python -m unittest discover -s tests -p "test_*.py"
   ```
3. If you change schemas, update:
   - `examples/`
   - golden tests
   - docs that describe the output contract

## Contribution areas

High-value contributions include:

- real command wrappers for bcftools / VEP / PLINK / Nextflow
- stronger schema validation
- local MCP servers
- HTML report generation
- benchmark fixtures
- safety hooks and provenance logging
- adapter support for more agent harnesses

## Style rules

- Keep prompts and policies short, explicit, and testable.
- Prefer structured outputs over prose.
- Do not merge clinically strong findings and exploratory PRS findings into the same confidence bucket.
- Never add instructions that imply diagnosis certainty.
- When in doubt, fail closed and require human review.

## Security and privacy

Do not commit:

- real genomes
- personally identifying variant files
- API keys
- secret tokens
- medical reports belonging to real people

Use synthetic or publicly shareable test fixtures only.
