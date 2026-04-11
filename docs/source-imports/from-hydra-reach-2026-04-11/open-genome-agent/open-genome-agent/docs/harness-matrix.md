# Harness matrix

| Concern | Claude Code | Codex CLI |
|---|---|---|
| Durable project guidance | `CLAUDE.md` or `.claude/CLAUDE.md` | `AGENTS.md` |
| Project skills | `.claude/skills/<name>/SKILL.md` | `.agents/skills/<name>/SKILL.md` |
| Custom agents | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| Project config | `.claude/settings.json` | `.codex/config.toml` |
| Hooks | in settings or frontmatter | `.codex/hooks.json` |
| Local overrides | `.claude/settings.local.json` | user config or profiles |

## Design choice

This repo keeps:

- one source of truth in `skills-src/` and `agents-src/`
- generated runtime files for each harness
- adapter scripts that can copy those outputs into another repository
