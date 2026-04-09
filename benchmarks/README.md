# Benchmarks

This directory is the proof-program entrypoint for hard metrics and public demo assets.

The intended progression is:

1. synthetic fixtures in `examples/synthetic/` for CI smoke tests
2. [HG002](hg002/README.md) for baseline precision and recall
3. [CMRG](cmrg/README.md) for difficult medically relevant genes
4. [public demos](public-demos/README.md) for end-to-end walkthroughs on openly shared genomes
5. [1000 Genomes](1000g/manifest.json) for scale and population-aware testing

Each dataset or pack in this tree should be represented by a machine-readable `manifest.json` and a short README that explains why it exists.
