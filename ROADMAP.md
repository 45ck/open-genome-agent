# Roadmap

This repository should mature as a proof program, not as a vague genomics demo.

The near-term objective is to prove four things separately:

1. Technical correctness on public truth datasets
2. Interpretation discipline with explicit evidence and caveats
3. End-to-end usefulness on openly shared public genomes
4. Portability across Claude Code, Codex CLI, and future harnesses

The guiding rule is simple:

> Benchmark first, public genome second, private genome last.

## North Star

Ship an open-source genomics agent repo that can:

1. ingest a public genome or VCF locally and produce a structured, evidence-bound report;
2. score itself against public truth sets and publish reproducible metrics;
3. run the same logical workflow through Claude Code and Codex CLI with the same policy, skill source, and output contracts.

## Proof Pillars

### 1. Technical correctness

Use GIAB / NIST HG002 as the first hard benchmark.

Why:

- GIAB exists to benchmark variant calling against public truth data
- HG002 is the most reused and practical starting point
- `hap.py` and GA4GH-style benchmarking guidance provide a standard comparison path

Success looks like:

- reproducible HG002 benchmark runs
- machine-readable precision, recall, and F1 outputs
- explicit benchmark-region accounting
- stable commands and provenance logs

### 2. Hard-region competence

Add the NIST Challenging Medically Relevant Genes benchmark after HG002 is stable.

Why:

- easy-region metrics are not enough
- medically relevant hard regions are where many pipelines fail silently

Success looks like:

- a dedicated CMRG evaluation mode
- per-gene scorecards
- explicit "supported" and "not yet trusted" boundaries

### 3. Interpretation discipline

Evaluation for interpretation modules should come from public, reviewable resources rather than ad hoc examples.

Primary sources:

- ClinVar for clinically relevant variant assertions, filtered to stronger review status first
- CPIC and PharmVar for pharmacogenomics
- PGS Catalog for reproducible PRS demonstrations
- MaveDB for experimentally measured functional effect examples

Success looks like:

- every claim linked to evidence
- every claim labeled with confidence
- limitations placed close to high-impact claims
- zero unsupported clinical-sounding claims in public demos

### 4. Real public-genome workflow

Use one Harvard Personal Genome Project participant as the first public end-to-end showcase.

Why:

- it demonstrates a real person-style workflow
- the data is openly shared for public reuse
- trait and health context makes the report easier to evaluate than a truth genome alone

Success looks like:

- one-command public sample walkthrough
- readable HTML and JSON outputs
- a provenance trail visible from CLI to report

### 5. Scale and population handling

Use 1000 Genomes after the single-sample workflow is solid.

Why:

- it tests ingestion and querying across many samples
- it exposes assumptions that only appear at batch scale
- it supports ancestry, frequency, and PRS plumbing demonstrations on public data

Success looks like:

- stable batch processing
- clear population-aware caveats
- throughput and storage measurements

### 6. Cross-harness portability

The same proof artifacts should work across Claude Code and Codex CLI.

Success looks like:

- one shared skill source
- one shared policy surface
- matching structured outputs across harnesses
- backend comparison runs that show where behavior diverges

## Recommended Dataset Order

Use datasets in this order:

1. tiny synthetic fixtures in-repo for smoke tests
2. GIAB / NIST HG002 for hard benchmark metrics
3. NIST CMRG for difficult medically relevant regions
4. one Harvard PGP public sample for the full showcase report
5. 1000 Genomes for scale and population-aware testing
6. ClinVar, CPIC, PharmVar, PGS Catalog, and MaveDB for interpretation modules
7. VariantBench or an equivalent internal harness for LLM-specific reasoning evaluation

## Phases

## Phase 1: Synthetic smoke-test layer

Focus:

- keep CI fast and deterministic
- prove schema compliance and core command wiring
- avoid internet-sized datasets in routine tests

Deliverables:

- synthetic VCF fixtures for ingest, build detection, query, and report smoke tests
- test coverage for required output artifacts
- clear separation between smoke tests and full benchmarks

Exit criteria:

- CI passes from synthetic data alone
- no schema drift across required artifacts

## Phase 2: HG002 benchmark mode

Focus:

- establish the first hard proof of correctness

Deliverables:

- `benchmarks/hg002/` scaffold
- GIAB asset manifest
- `hap.py` wrapper or integration layer
- benchmark metrics JSON
- benchmark README and HTML summary

Exit criteria:

- reproducible HG002 small-variant benchmark run
- documented commands, versions, and reference build
- benchmark output suitable for a repo screenshot

## Phase 3: Hard-region benchmark mode

Focus:

- prove performance in difficult medically relevant regions

Deliverables:

- CMRG asset manifest
- CMRG evaluation mode
- per-gene scorecard output
- supported challenging genes page

Exit criteria:

- CMRG run produces explicit supported and unsupported regions
- public-facing scorecard is understandable without reading raw logs

## Phase 4: Public genome showcase

Focus:

- prove the repo is useful on a real public human genome, not only benchmarks

Deliverables:

- one selected Harvard PGP sample with clear reuse terms
- public ingestion guide
- public-demo report template
- CLI walkthrough script
- privacy and consent explainer page

Exit criteria:

- one public-sample walkthrough can be reproduced locally
- every reported claim is evidence-bound and caveated

## Phase 5: Interpretation evaluation pack

Focus:

- test whether the agent interprets rather than merely parses

Deliverables:

- ClinVar higher-review-status dataset builder
- CPIC and PharmVar example packs
- PGS Catalog and MaveDB demo packs
- evidence-grading rubric

Exit criteria:

- each interpretation module has a reproducible test pack
- confidence buckets remain separated and auditable

## Phase 6: Scale and population workflows

Focus:

- prove the repo behaves predictably across many public genomes

Deliverables:

- 1000 Genomes sample manifest
- batch query mode
- population-aware summary page
- throughput benchmark page

Exit criteria:

- batch runs complete reliably on public samples
- ancestry and PRS caveats are explicit in outputs

## Phase 7: Reasoning and backend comparison

Focus:

- compare reasoning quality and claim discipline across LLM harnesses

Deliverables:

- VariantBench harness or equivalent internal evaluator
- unsupported-claim scorer
- side-by-side backend evaluation mode

Exit criteria:

- reasoning runs can be compared by evidence alignment, contradiction rate, and unsupported-claim rate
- harness differences are visible rather than hand-waved away

## Phase 8: Raw-data path

Focus:

- add heavy compute only after the VCF-first proof stack is stable

Deliverables:

- optional Nextflow or nf-core/sarek integration
- BAM/CRAM or FASTQ entry path
- long-running workflow provenance capture

Exit criteria:

- raw-data workflows remain optional
- local-first and provenance rules still hold

## Public Showcase Artifacts

The strongest public showcase should include three visible artifacts:

1. a benchmark page showing HG002 metrics, ideally with region stratification
2. a public genome walkthrough on a Harvard PGP sample with a readable evidence-bound report
3. a live CLI demo that answers genome questions on public data and exposes the provenance trail

## What Not To Do

Do not:

- lead with a private genome
- lead with raw FASTQ or HPC complexity
- make PRS or trait inference the headline
- mix benchmark truth, public-demo data, and speculative interpretation into one score
- claim diagnostic certainty
- hide ambiguity around build, sample identity, or annotation state

## Near-Term Repo Targets

The first public release should aim to include:

1. HG002 benchmark mode
2. CMRG challenge mode
3. one Harvard PGP end-to-end demo report
4. ClinVar and CPIC-backed interpretation evaluation
5. a landing page with benchmark and report screenshots

These five artifacts create a balanced proof stack:

- one correctness proof
- one hard-region proof
- one human-style workflow demo
- one interpretation-discipline proof
- one public-facing showcase
