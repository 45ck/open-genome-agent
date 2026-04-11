# Confidence Model

This page explains how `open-genome-agent` should talk about DNA results.

The goal is simple:

- stronger signals should be presented as stronger signals
- weaker signals should be presented as weaker signals
- unsupported claims should stay out of the report

## 1. Can often help with relatively stronger signals

These are the categories the repo should eventually handle best:

- known or well-characterized variant lookups
- carrier-style findings
- some pharmacogenomic findings
- ancestry and lineage clues
- some simpler trait-linked variants

These are not guaranteed to be clinically decisive, but they are usually more defensible than speculative summaries.

## 2. May help with weaker, probabilistic signals

These categories can still be useful, but they should be framed as probabilities or tendencies:

- polygenic risk scores
- trait tendencies
- performance or body predispositions
- exploratory leads worth following up

This repo should always present these as **probabilistic**, not deterministic.

## 3. Should not claim to tell you

The repo should not present itself as able to reliably tell you:

- exact future disease outcomes
- exact disease timing or severity
- exact personality, intelligence, or lifespan
- medication safety without clinician review
- one final answer with no ambiguity

## 4. Output buckets

Reports should separate at least four categories:

1. **higher-confidence findings**
2. **probabilistic findings**
3. **exploratory leads**
4. **unknowns / limitations**

That separation matters more than polished wording.

## 5. Human review rule

If the system surfaces something high-impact, the next step should be **human review**, not false certainty.

This repo is not a doctor, not a genetic counselor, and not a diagnosis engine.
