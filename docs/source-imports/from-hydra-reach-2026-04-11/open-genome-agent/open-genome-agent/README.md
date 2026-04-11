# open-genome-agent

Local-first, evidence-bound genomics workflows for coding agents.

This repository is a **cross-harness scaffold** for building reusable genome-analysis skills, agents, hooks, and reporting pipelines that work across:

- **Claude Code**
- **Codex CLI**
- future **MCP / SDK / app-server** harnesses

The design principle is simple:

> **LLM orchestrates. Deterministic bioinformatics tools compute. Structured evidence drives every claim.**

## Status

This is a **repo scaffold / starter kit**, not a finished clinical pipeline.

Version 0.1 focuses on:

- a single source of truth for skills and agent definitions
- generated runtime folders for Claude and Codex
- schemas for manifests, findings, and evidence
- safety and reporting rules
- synthetic fixtures and build tests
- hook stubs and MCP server stubs

## Why this shape

The repo separates three concerns:

1. **Policy** — durable operating rules and output requirements
2. **Source definitions** — skill and agent specs that stay harness-agnostic
3. **Adapters** — generated runtime layouts for each coding harness

That lets you maintain one workflow definition and emit the files that each agent runner expects.

## Repository layout

```text
open-genome-agent/
  policy/           # shared operating rules and rubrics
  schemas/          # machine-readable output contracts
  skills-src/       # harness-agnostic skill source definitions
  agents-src/       # harness-agnostic agent source definitions
  adapters/         # Claude and Codex generators + templates
  .claude/          # generated Claude runtime files
  .agents/          # generated Codex skill runtime files
  .codex/           # generated Codex config + custom agents
  hooks/            # deterministic lifecycle hook scripts
  mcp/              # local-first MCP server stubs
  examples/         # synthetic demo data and reports
  tests/            # build + schema validation tests
```

## Quick start

### 1. Clone and create a virtualenv

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
```

### 2. Regenerate harness outputs

```bash
python scripts/build_all.py
```

That rebuilds:

- `CLAUDE.md`
- `AGENTS.md`
- `.claude/skills/*`
- `.claude/agents/*`
- `.claude/settings.json`
- `.agents/skills/*`
- `.codex/agents/*`
- `.codex/config.toml`
- `.codex/hooks.json`
- `adapters/*/dist/*`

### 3. Run tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Using with Claude Code

This repo already contains a project-scoped `.claude/` folder.

You can open the repository directly in Claude Code, or copy `adapters/claude/dist/.claude/` plus `CLAUDE.md` into another repo with:

```bash
python adapters/claude/install.py /path/to/target-repo
```

## Using with Codex CLI

This repo already contains project-scoped:

- `AGENTS.md`
- `.agents/skills/`
- `.codex/config.toml`
- `.codex/agents/`
- `.codex/hooks.json`

To copy that layout into another repository:

```bash
python adapters/codex/install.py /path/to/target-repo
```

## What the first milestone covers

The default workflow is **VCF-first**, not raw FASTQ-first.

Included starter skills:

- `setup-workstation`
- `ingest-vcf`
- `detect-build-normalize`
- `query-variants`
- `annotate-variants`
- `prioritize-findings`
- `pharmacogenomics`
- `polygenic-risk`
- `generate-report`
- `nextflow-runner`

Included starter agents:

- `orchestrator`
- `explorer`
- `qc-worker`
- `annotation-worker`
- `evidence-reviewer`
- `report-writer`
- `workflow-ops`

## Safety model

This scaffold is intentionally strict:

- raw inputs are read-only
- no default upload of genome data
- no medical diagnosis output
- no mixing of strong variant evidence with weak PRS-style output
- every finding must have provenance and caveats
- every report must separate:
  - high-confidence findings
  - probabilistic findings
  - exploratory leads
  - unknowns / limitations

See `docs/safety-model.md` and `policy/`.

## Next steps after upload

1. Replace synthetic examples with a larger validated toy dataset
2. Wire real VEP / bcftools / PLINK / Nextflow commands into the skill scripts
3. Decide whether to keep the repo VCF-first or add BAM/CRAM validation in the MVP
4. Add one local MCP server for evidence storage
5. Build HTML report rendering from the JSON schemas

## License

MIT
