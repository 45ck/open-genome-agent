# Demo Backlog

This backlog turns the repo into a public proof stack with distinct deliverables for correctness, interpretation discipline, public-demo value, and cross-harness portability.

The priority rule is:

> Hard benchmark first. Public genome walkthrough second. Scale and raw-data workflows later.

## Release Goals

The first strong public showcase should ship these artifacts:

1. an HG002 benchmark page with reproducible metrics
2. a CMRG scorecard for difficult medically relevant genes
3. one public Harvard PGP walkthrough report
4. an interpretation evaluation pack backed by public sources
5. a CLI demo that exposes provenance rather than only polished prose

## Backlog Structure

Each epic below includes:

- why it exists
- the concrete outputs expected from it
- the acceptance checks that determine whether it is done

## Epic 1: Benchmark Core

Why:

- the repo needs hard numbers before it asks anyone to trust its outputs

Outputs:

- `benchmarks/hg002/` scaffold
- GIAB download manifest with pinned sources and checksums where available
- `hap.py` benchmark wrapper
- parsed metrics JSON
- HTML benchmark summary
- local run instructions

Acceptance checks:

- benchmark run is reproducible from documented commands
- metrics include SNP and indel precision, recall, and F1
- benchmark region and skipped region accounting are explicit
- run writes provenance artifacts alongside metric outputs

Suggested issue slices:

- `benchmark: add hg002 asset manifest`
- `benchmark: add hap.py wrapper`
- `benchmark: parse benchmark metrics into json`
- `benchmark: render hg002 html summary`
- `docs: add local hg002 benchmark instructions`

## Epic 2: Hard-Region Evaluation

Why:

- easy-region benchmark scores are insufficient for medically relevant claims

Outputs:

- CMRG asset manifest
- CMRG evaluation mode
- per-gene scorecard
- supported challenging genes page

Acceptance checks:

- output clearly distinguishes benchmarked vs unbenchmarked genes
- per-gene summaries link back to evidence and commands
- unsupported regions are called out rather than ignored

Suggested issue slices:

- `benchmark: add cmrg asset manifest`
- `benchmark: add cmrg evaluation mode`
- `report: emit per-gene cmrg scorecard`
- `docs: publish supported challenging genes page`

## Epic 3: Public Genome Walkthrough

Why:

- the repo needs one real public human-style workflow, not only benchmark harnesses

Outputs:

- selected Harvard PGP public sample manifest
- public-sample ingestion guide
- public-demo report template
- CLI walkthrough script
- privacy and consent explainer

Acceptance checks:

- a fresh clone can reproduce the walkthrough locally
- the report includes limitations and human-review boundaries
- every finding links to evidence and caveats
- the demo never relies on private or ambiguous sharing terms

Suggested issue slices:

- `demo: select first public pgp sample`
- `demo: add public genome ingestion guide`
- `report: add public-demo report template`
- `demo: script cli walkthrough on public sample`
- `docs: add privacy and consent explainer`

## Epic 4: Interpretation Evaluation Pack

Why:

- interpretation must be tested separately from file parsing and benchmark matching

Outputs:

- ClinVar higher-review-status dataset builder
- CPIC example pack
- PharmVar example pack
- PGS Catalog demo pack
- MaveDB example pack
- evidence-grading rubric

Acceptance checks:

- each example pack records source class and version date
- every evaluation case has an expected evidence type
- PRS outputs remain separated from direct variant findings
- unsupported claims are scored as failures, not softened into plausible prose

Suggested issue slices:

- `eval: build clinvar higher-review-status pack`
- `eval: add cpic pgx example cases`
- `eval: add pharmvar allele example cases`
- `eval: add pgs catalog demo pack`
- `eval: add mavedb functional example pack`
- `policy: add evidence-grading rubric`

## Epic 5: LLM Reasoning Evaluation

Why:

- the repo should measure claim discipline, not only parser correctness

Outputs:

- VariantBench harness or compatible internal evaluator
- reasoning result schema
- contradiction and unsupported-claim scorer
- backend comparison mode for Claude and Codex

Acceptance checks:

- runs can be compared by evidence alignment and unsupported-claim rate
- reasoning artifacts are saved separately from deterministic tool outputs
- final scores do not collapse correctness and fluency into one number

Suggested issue slices:

- `eval: add variantbench harness`
- `schemas: add reasoning-result schema`
- `eval: score unsupported claims and contradictions`
- `eval: compare claude and codex reasoning runs`

## Epic 6: Scale and Population Workflows

Why:

- a single polished sample can hide operational and population-context failures

Outputs:

- 1000 Genomes sample manifest
- batch query mode
- population-aware summary page
- throughput benchmark page

Acceptance checks:

- batch mode can run across a selected public cohort
- outputs keep sample identity and provenance unambiguous
- population labels are treated as context, not destiny
- PRS and ancestry caveats remain explicit in batch outputs

Suggested issue slices:

- `scale: add 1000 genomes sample manifest`
- `scale: add batch query mode`
- `report: add population-aware summary page`
- `benchmark: add throughput summary for public cohort`

## Epic 7: Landing Page and Demo Assets

Why:

- the repo needs a visible public proof surface, not only internal scripts

Outputs:

- benchmark screenshot card
- report screenshot
- terminal GIF or recorded CLI transcript
- "what we do not claim" panel
- README links to proof artifacts

Acceptance checks:

- the repo home page surfaces benchmark, demo, and safety evidence above the fold
- screenshot assets are generated from public or synthetic data only
- limitations are visible next to the strongest claims

Suggested issue slices:

- `docs: add proof-program links to readme`
- `assets: create benchmark screenshot card`
- `assets: create public report screenshot`
- `assets: capture cli demo transcript`
- `docs: add what-we-do-not-claim panel`

## Epic 8: Optional Raw-Data Path

Why:

- raw-read workflows matter, but they should not block the VCF-first proof stack

Outputs:

- optional Nextflow or nf-core/sarek route
- raw-input manifest format
- workflow provenance capture

Acceptance checks:

- the raw-data route is explicitly optional
- long-running workflow commands and versions are preserved
- benchmark and demo paths still work without heavy compute tooling

Suggested issue slices:

- `workflow: add optional nextflow raw-data route`
- `workflow: add raw-input manifest schema`
- `workflow: capture provenance for long-running jobs`

## Suggested Sprint Order

Sprint 1:

- synthetic fixtures cleanup
- HG002 benchmark wrapper
- metrics parser
- benchmark README

Sprint 2:

- CMRG mode
- HTML scorecard
- first Harvard PGP sample selection
- first public-demo report template

Sprint 3:

- ClinVar, CPIC, and PharmVar packs
- evidence-grading rubric
- first public walkthrough script

Sprint 4:

- 1000 Genomes manifest and batch mode
- PGS Catalog and MaveDB packs
- backend comparison harness

Sprint 5:

- VariantBench integration
- optional raw-data route
- repo landing page polish

## Definition Of Done For Public Demo Work

A demo-oriented task is not done unless:

- the output is reproducible from repository instructions
- provenance artifacts are preserved
- limitations are visible
- confidence buckets are explicit
- private genome data is not required

## Out Of Scope For The First Showcase

Do not prioritize these before the core proof stack is working:

- personal-genome marketing
- raw FASTQ-first onboarding
- mixed benchmark and interpretation leaderboards
- trait speculation without strong evidence
- any output that reads like diagnosis
