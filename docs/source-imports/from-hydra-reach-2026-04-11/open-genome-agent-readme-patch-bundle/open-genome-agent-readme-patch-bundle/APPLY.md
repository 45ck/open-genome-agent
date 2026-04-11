# Apply guide

This bundle contains both:

- `open-genome-agent-readme-repositioning.patch` — unified diff
- `0001-docs-reposition-readme.patch` — git-style patch wrapper
- `files/` — full replacement files if you prefer copy/paste

## Option 1: apply the patch

From the repo root:

```bash
git apply /path/to/open-genome-agent-readme-repositioning.patch
git diff
git add README.md docs/README.md docs/confidence-model.md docs/what-we-do-not-claim.md
git commit -m "docs: reposition repo around user-facing DNA analysis confidence model"
```

If the patch does not apply cleanly because the repo has changed, use Option 2.

## Option 2: replace files manually

Copy these files into the repo:

- `files/README.md`
- `files/docs/README.md`
- `files/docs/confidence-model.md`
- `files/docs/what-we-do-not-claim.md`

Then:

```bash
git diff
git add README.md docs/README.md docs/confidence-model.md docs/what-we-do-not-claim.md
git commit -m "docs: reposition repo around user-facing DNA analysis confidence model"
```

## Why this patch exists

The repo currently reads as a scaffold/framework first.
This patch makes it read as a **local-first DNA analysis copilot** first, while keeping the proof-program and harness details lower in the README.

Main changes:

- README now leads with user value
- adds a simple confidence model
- adds a stronger “what this is not” framing
- adds `docs/confidence-model.md`
- refreshes the docs index for non-scientist readers
- expands `docs/what-we-do-not-claim.md`
