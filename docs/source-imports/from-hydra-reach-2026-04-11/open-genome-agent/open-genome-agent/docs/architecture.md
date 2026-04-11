# Architecture

## Core idea

The repository is built around a **shared source layer** and **generated harness adapters**.

### Shared source layer

- `policy/` holds durable rules and evaluation rubrics
- `schemas/` defines machine-readable outputs
- `skills-src/` holds reusable workflow definitions
- `agents-src/` holds reusable role definitions

### Generated harness layers

- `.claude/` and `CLAUDE.md` for Claude Code
- `.agents/`, `.codex/`, and `AGENTS.md` for Codex CLI
- `adapters/*/dist/` for exportable bundles

## Data flow

```text
source genome files
  -> ingest / validation
  -> normalization / build detection
  -> annotation
  -> prioritization
  -> report synthesis
  -> structured artifacts + human-readable report
```

## Why the repo is VCF-first

VCF-centered workflows are the fastest route to a useful open-source agent system because they avoid:

- expensive raw-read alignment
- huge storage and compute requirements
- unnecessary pipeline complexity in the first milestone

The scaffold still leaves room for BAM/CRAM validation and Nextflow-based raw-read workflows later.

## Output philosophy

Every run should emit both:

1. **structured artifacts** for downstream automation
2. **human-readable reports** for review

The system should never rely on a prose-only answer.

## Non-goals for the MVP

- cloud-hosted genome analysis
- one-click clinical diagnosis
- automatic internet upload of personal genomes
- hidden prompting without provenance
