# Security Policy

## Scope

This repository is designed for local-first genomics workflows and may operate on highly sensitive personal data.

Treat all genome-derived files as sensitive.

## Supported use

The scaffold is intended for:

- local development
- reproducible research workflows
- evidence-bound reporting
- agent orchestration experiments

It is **not** intended to be used as a medical device or to produce unsupervised clinical diagnoses.

## Reporting vulnerabilities

Please report security issues privately to the repository maintainer rather than opening a public issue.

Include:

- steps to reproduce
- affected files or components
- impact assessment
- whether the issue could expose genome data, credentials, or host-system files

## Hardening expectations

Recommended defaults:

- run in a trusted local environment
- keep network off unless explicitly needed
- store genomes outside the git working tree when possible
- prefer read-only analysis of source data
- use hook logging for provenance
- review all generated reports before sharing
