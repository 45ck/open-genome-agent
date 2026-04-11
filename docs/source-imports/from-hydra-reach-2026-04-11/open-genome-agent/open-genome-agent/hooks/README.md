# Hooks

These scripts are intentionally small and deterministic.

They serve three purposes:

- log lifecycle events
- block or warn on obviously unsafe shell behavior
- keep the report discipline visible to the agent

Both harnesses have their own hook entrypoints because their JSON I/O contracts differ.
