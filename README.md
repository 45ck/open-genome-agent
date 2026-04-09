# open-genome-agent

<p align="center">
  <img src="assets/banner.svg" alt="open-genome-agent banner" width="100%" />
</p>

[![CI](https://github.com/45ck/open-genome-agent/actions/workflows/ci.yml/badge.svg)](https://github.com/45ck/open-genome-agent/actions/workflows/ci.yml)
[![CodeQL](https://github.com/45ck/open-genome-agent/actions/workflows/codeql.yml/badge.svg)](https://github.com/45ck/open-genome-agent/actions/workflows/codeql.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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

The current delivery direction is a **proof program**:

- benchmark correctness first on public truth data
- demonstrate end-to-end reporting on public genomes
- keep interpretation modules evidence-bound and separately evaluated
- preserve portability across Claude Code and Codex CLI

See [ROADMAP.md](ROADMAP.md) and [DEMO_BACKLOG.md](DEMO_BACKLOG.md).

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
  benchmarks/       # benchmark and public-data proof-program assets
  evals/            # interpretation and reasoning evaluation packs
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
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
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

## Open source baseline

This repository ships with:

- MIT licensing
- contribution and support docs
- a code of conduct
- security reporting guidance
- issue and pull request templates
- CI, dependency review, Dependabot, and CodeQL workflows

If you publish derivative workflows, keep the safety constraints, provenance expectations, and non-diagnostic framing intact.

## Near-term direction

The repo should prove capability in this order:

1. synthetic smoke tests for CI stability
2. HG002 benchmark mode for hard correctness metrics
3. CMRG mode for difficult medically relevant regions
4. one public-genome walkthrough on openly shared data
5. interpretation evaluation packs with explicit confidence and evidence rules

The backlog for that work lives in [ROADMAP.md](ROADMAP.md) and [DEMO_BACKLOG.md](DEMO_BACKLOG.md).

## License

MIT

See `LICENSE`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, and `SUPPORT.md` for repository governance details.
