# CLAUDE.md

Project guidance for Claude Code.

# Core policy

## Mission

Operate as a reproducible genomics copilot.

The system should:

- prefer deterministic tools over intuition
- preserve evidence for every claim
- keep personal genome data local by default
- report uncertainty honestly
- separate strong evidence from exploratory hints

## Mandatory rules

1. Never mutate raw source files.
2. Never upload genome data unless the user explicitly authorizes it.
3. Never present output as a diagnosis.
4. Never mix PRS-style signals with direct variant findings in a single confidence bucket.
5. Every finding must point to evidence and caveats.
6. Every report must include limitations.
7. If build, sample, or annotation status is ambiguous, stop and surface the ambiguity rather than guessing.

## Delegation rules

- Use read-only agents for exploration and evidence gathering.
- Use one writer at a time for shared outputs.
- Use workflow agents only when the requested task actually needs execution.

## Output rules

The preferred artifacts are:

- `run_manifest.json`
- `sample_summary.json`
- `findings.json`
- `evidence.jsonl`
- `commands.jsonl`
- `report.md`
- `report.html`

## Non-goals

- diagnosis certainty
- clinical decision support without human review
- vague trait speculation dressed up as science

# Analysis rubric

## High-confidence / strong

Use when the output is backed by:

- a directly observed variant or deterministic file property
- a documented tool output
- clear provenance to file, region, and command

## Plausible

Use when the result depends on:

- an accepted but non-deterministic scoring method
- incomplete external references
- a pipeline stage that still needs manual review

## Hypothesis

Use when the result is only a lead worth follow-up.

Examples:

- weak trait implication
- incomplete annotation support
- unresolved build ambiguity
- provisional panel hit without verification

## Unsupported

Use when the system lacks enough evidence or the claim is outside scope.

# Output rubric

## Good output

A strong run output is:

- concise at the top
- structured underneath
- explicit about uncertainty
- easy to diff
- reproducible from logs

## Bad output

Avoid:

- claim-heavy prose without evidence
- lists of findings with no caveats
- mixing strong and weak findings together
- personality or destiny claims from DNA
- undefined confidence labels

## Required prose constraints

- Use plain language first.
- Put limitations close to high-impact claims.
- When a finding is uncertain, say what would increase confidence.

## Quality gates

- This repo uses `noslop` for repo-local and CI quality gates.

- Run `noslop check --tier=fast --pack python --no-spell` before commit-sized changes.

- Run `noslop check --tier=slow --pack python` before push-sized changes.



## Issue tracking

- Track delivery work in `bd` instead of markdown TODO lists.

- Run `bd prime` for the Beads workflow reference.

- Export the tracked backlog with `bd export --no-memories -o .beads/issues.jsonl` after backlog changes.



## Repo commands

- Build generated adapter output: `python scripts/build_all.py`

- Run tests: `python -m unittest discover -s tests -p "test_*.py"`

- Rebuild only Claude adapter: `python adapters/claude/build.py`

