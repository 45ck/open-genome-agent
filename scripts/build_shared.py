from __future__ import annotations

import json
import os
import stat
import shutil
import time
from pathlib import Path
from typing import Any

import yaml  # type: ignore[import-untyped]

ROOT = Path(__file__).resolve().parents[1]
SKILLS_SRC = ROOT / "skills-src"
AGENTS_SRC = ROOT / "agents-src"
POLICY_DIR = ROOT / "policy"


def remove_tree(path: Path) -> None:
    if not path.exists():
        return

    def onerror(
        func: Any, target: str, exc_info: tuple[type[BaseException], BaseException, Any]
    ) -> None:
        os.chmod(target, stat.S_IWRITE)
        func(target)

    for attempt in range(3):
        try:
            shutil.rmtree(path, onerror=onerror)
            return
        except OSError:
            if attempt == 2:
                raise
            time.sleep(0.1)


def ensure_clean_dir(path: Path) -> None:
    if path.exists():
        remove_tree(path)
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        remove_tree(dst)
    shutil.copytree(src, dst)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    _, raw_frontmatter, body = parts
    frontmatter = yaml.safe_load(raw_frontmatter) or {}
    return frontmatter, body.lstrip()


def yaml_frontmatter(data: dict[str, Any]) -> str:
    dumped = yaml.safe_dump(data, sort_keys=False, allow_unicode=True).strip()
    return f"---\n{dumped}\n---\n"


def render_skill_body(meta: dict[str, Any], core: str) -> str:
    when = "\n".join(f"- {item}" for item in meta.get("when_to_use", []))
    not_when = "\n".join(f"- {item}" for item in meta.get("not_when_to_use", []))
    outputs = "\n".join(f"- `{item}`" for item in meta.get("outputs", []))
    title = meta.get("title") or meta["name"].replace("-", " ").title()
    sections = [
        f"# {title}",
        "",
        meta["description"].strip(),
        "",
        "## When to use",
        when or "- This skill is available when its description matches the task.",
        "",
        "## Do not use when",
        not_when or "- There is no explicit exclusion.",
        "",
        "## Expected outputs",
        outputs or "- No fixed outputs declared.",
        "",
        core.strip(),
        "",
        "## References",
        "See `references/README.md` for durable notes and `scripts/` for deterministic helpers.",
        "",
    ]
    return "\n".join(sections)


def build_claude_skill(skill_dir: Path, out_root: Path) -> None:
    meta = load_yaml(skill_dir / "skill.yaml")
    core = (skill_dir / "core.md").read_text(encoding="utf-8")
    out_dir = out_root / ".claude" / "skills" / meta["name"]
    out_dir.mkdir(parents=True, exist_ok=True)

    frontmatter: dict[str, Any] = {
        "name": meta["name"],
        "description": meta["description"],
    }
    if meta.get("allowed_tools"):
        frontmatter["allowed-tools"] = meta["allowed_tools"]
    if meta.get("context"):
        frontmatter["context"] = meta["context"]
    if meta.get("agent"):
        frontmatter["agent"] = meta["agent"]
    if meta.get("disable_model_invocation"):
        frontmatter["disable-model-invocation"] = True

    body = render_skill_body(meta, core)
    write_text(out_dir / "SKILL.md", yaml_frontmatter(frontmatter) + body + "\n")

    copy_tree(skill_dir / "refs", out_dir / "references")
    copy_tree(skill_dir / "scripts", out_dir / "scripts")


def build_codex_skill(skill_dir: Path, out_root: Path) -> None:
    meta = load_yaml(skill_dir / "skill.yaml")
    core = (skill_dir / "core.md").read_text(encoding="utf-8")
    out_dir = out_root / ".agents" / "skills" / meta["name"]
    out_dir.mkdir(parents=True, exist_ok=True)

    frontmatter = {
        "name": meta["name"],
        "description": meta["description"],
    }
    body = render_skill_body(meta, core)
    write_text(out_dir / "SKILL.md", yaml_frontmatter(frontmatter) + body + "\n")

    copy_tree(skill_dir / "refs", out_dir / "references")
    copy_tree(skill_dir / "scripts", out_dir / "scripts")


def build_claude_agent(agent_file: Path, out_root: Path) -> None:
    frontmatter, body = split_frontmatter(agent_file.read_text(encoding="utf-8"))
    claude_meta = frontmatter.get("claude", {})
    out_frontmatter: dict[str, Any] = {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
    }

    if claude_meta.get("tools"):
        out_frontmatter["tools"] = claude_meta["tools"]
    if claude_meta.get("model"):
        out_frontmatter["model"] = claude_meta["model"]
    if claude_meta.get("permissionMode"):
        out_frontmatter["permissionMode"] = claude_meta["permissionMode"]
    if claude_meta.get("maxTurns"):
        out_frontmatter["maxTurns"] = claude_meta["maxTurns"]
    if claude_meta.get("skills"):
        out_frontmatter["skills"] = claude_meta["skills"]

    out_path = out_root / ".claude" / "agents" / agent_file.name
    write_text(out_path, yaml_frontmatter(out_frontmatter) + body.strip() + "\n")


def toml_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def build_codex_agent(agent_file: Path, out_root: Path) -> None:
    frontmatter, body = split_frontmatter(agent_file.read_text(encoding="utf-8"))
    codex_meta = frontmatter.get("codex", {})
    lines = [
        f'name = "{toml_escape(frontmatter["name"])}"',
        f'description = "{toml_escape(frontmatter["description"])}"',
    ]

    if codex_meta.get("model"):
        lines.append(f'model = "{toml_escape(codex_meta["model"])}"')
    if codex_meta.get("model_reasoning_effort"):
        lines.append(
            f'model_reasoning_effort = "{toml_escape(codex_meta["model_reasoning_effort"])}"'
        )
    if codex_meta.get("sandbox_mode"):
        lines.append(f'sandbox_mode = "{toml_escape(codex_meta["sandbox_mode"])}"')
    if codex_meta.get("nickname_candidates"):
        nicknames = ", ".join(
            f'"{toml_escape(item)}"' for item in codex_meta["nickname_candidates"]
        )
        lines.append(f"nickname_candidates = [{nicknames}]")

    dev = body.strip().replace('"""', '\\"\\"\\"')
    lines.append('developer_instructions = """')
    lines.append(dev)
    lines.append('"""')
    content = "\n".join(lines) + "\n"

    out_path = out_root / ".codex" / "agents" / f'{frontmatter["name"]}.toml'
    write_text(out_path, content)


def render_claude_guidance() -> str:
    core = (POLICY_DIR / "core-policy.md").read_text(encoding="utf-8").strip()
    analysis = (POLICY_DIR / "analysis-rubric.md").read_text(encoding="utf-8").strip()
    output = (POLICY_DIR / "output-rubric.md").read_text(encoding="utf-8").strip()
    return "\n\n".join(
        [
            "# CLAUDE.md",
            "Project guidance for Claude Code.",
            core,
            analysis,
            output,
            "## Quality gates",
            "- This repo uses `noslop` for repo-local and CI quality gates.",
            "- Run `noslop check --tier=fast --pack python --no-spell` before commit-sized changes.",
            "- Run `noslop check --tier=slow --pack python` before push-sized changes.",
            "",
            "## Issue tracking",
            "- Track delivery work in `bd` instead of markdown TODO lists.",
            "- Run `bd prime` for the Beads workflow reference.",
            "- Export the tracked backlog with `bd export --no-memories -o .beads/issues.jsonl` after backlog changes.",
            "",
            "## Repo commands",
            "- Build generated adapter output: `python scripts/build_all.py`",
            '- Run tests: `python -m unittest discover -s tests -p "test_*.py"`',
            "- Rebuild only Claude adapter: `python adapters/claude/build.py`",
            "",
        ]
    )


def render_codex_guidance() -> str:
    core = (POLICY_DIR / "core-policy.md").read_text(encoding="utf-8").strip()
    analysis = (POLICY_DIR / "analysis-rubric.md").read_text(encoding="utf-8").strip()
    output = (POLICY_DIR / "output-rubric.md").read_text(encoding="utf-8").strip()
    return "\n\n".join(
        [
            "# AGENTS.md",
            "Project guidance for Codex.",
            core,
            analysis,
            output,
            "## Quality gates",
            "- This repo uses `noslop` for repo-local and CI quality gates.",
            "- Run `noslop check --tier=fast --pack python --no-spell` before commit-sized changes.",
            "- Run `noslop check --tier=slow --pack python` before push-sized changes.",
            "",
            "## Beads issue tracker",
            "- Use `bd` for tracked work instead of markdown TODO lists.",
            "- Run `bd prime` for the Beads workflow reference.",
            "- Export the tracked backlog with `bd export --no-memories -o .beads/issues.jsonl` after backlog changes.",
            "",
            "## Repo commands",
            "- Build generated adapter output: `python scripts/build_all.py`",
            '- Run tests: `python -m unittest discover -s tests -p "test_*.py"`',
            "- Rebuild only Codex adapter: `python adapters/codex/build.py`",
            "",
        ]
    )


def render_claude_settings() -> dict[str, Any]:
    return {
        "$schema": "https://json.schemastore.org/claude-code-settings.json",
        "permissions": {
            "allow": [
                "Read(*)",
                "Glob(*)",
                "Grep(*)",
                "Bash(python *)",
                "Bash(python3 *)",
                "Bash(samtools *)",
                "Bash(bcftools *)",
                "Bash(vep *)",
                "Bash(plink2 *)",
                "Bash(nextflow *)",
            ],
            "deny": [
                "Read(./.env)",
                "Read(./.env.*)",
                "Read(./secrets/**)",
                "Bash(curl *)",
                "Bash(wget *)",
                "Bash(scp *)",
                "Bash(rsync *)",
                "Bash(*--no-verify*)",
                "Bash(*--force*)",
                "Bash(git push -f*)",
                "Edit(.githooks/**)",
                "Edit(.github/workflows/**)",
                "Edit(.claude/settings.json)",
                "Edit(.claude/hooks/**)",
            ],
        },
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": 'sh "$(git rev-parse --show-toplevel)/.claude/hooks/pre-tool-use.sh"',
                            "timeout": 30,
                        },
                        {
                            "type": "command",
                            "command": 'python3 "$(git rev-parse --show-toplevel)/hooks/claude/pre_tool_policy.py"',
                            "timeout": 30,
                        },
                    ],
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": 'python3 "$(git rev-parse --show-toplevel)/hooks/claude/validate_stop.py"',
                            "timeout": 30,
                        }
                    ]
                }
            ],
        },
    }


def render_codex_config() -> str:
    return """\
model = "gpt-5.4"
approval_policy = "on-request"
sandbox_mode = "workspace-write"
project_root_markers = [".git", ".hg", ".sl"]

[features]
codex_hooks = true
multi_agent = true

[agents]
max_threads = 6
max_depth = 1
"""


def render_codex_hooks() -> dict[str, Any]:
    git_root_py = '/usr/bin/env python3 "$(git rev-parse --show-toplevel)/hooks/codex'
    return {
        "hooks": {
            "SessionStart": [
                {
                    "matcher": "startup|resume",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'{git_root_py}/session_start.py"',
                            "statusMessage": "Loading genome-agent context",
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'{git_root_py}/pre_tool_use_policy.py"',
                            "statusMessage": "Checking shell command",
                        }
                    ],
                }
            ],
            "PostToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'{git_root_py}/post_tool_use_review.py"',
                            "statusMessage": "Reviewing shell output",
                        }
                    ],
                }
            ],
            "UserPromptSubmit": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'{git_root_py}/user_prompt_submit_data_flywheel.py"',
                        }
                    ]
                }
            ],
            "Stop": [
                {
                    "hooks": [
                        {
                            "type": "command",
                            "command": f'{git_root_py}/stop_continue.py"',
                            "timeout": 30,
                        }
                    ]
                }
            ],
        }
    }


def build_claude_runtime(out_root: Path) -> None:
    (out_root / ".claude" / "skills").mkdir(parents=True, exist_ok=True)
    (out_root / ".claude" / "agents").mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if skill_dir.is_dir():
            build_claude_skill(skill_dir, out_root)

    for agent_file in sorted(AGENTS_SRC.glob("*.md")):
        build_claude_agent(agent_file, out_root)

    write_text(out_root / "CLAUDE.md", render_claude_guidance())
    write_text(
        out_root / ".claude" / "settings.json",
        json.dumps(render_claude_settings(), indent=2) + "\n",
    )
    write_text(
        out_root / ".claude" / "settings.local.example.json",
        '{\n  "$schema": "https://json.schemastore.org/claude-code-settings.json"\n}\n',
    )


def build_codex_runtime(out_root: Path) -> None:
    (out_root / ".agents" / "skills").mkdir(parents=True, exist_ok=True)
    (out_root / ".codex" / "agents").mkdir(parents=True, exist_ok=True)

    for skill_dir in sorted(SKILLS_SRC.iterdir()):
        if skill_dir.is_dir():
            build_codex_skill(skill_dir, out_root)

    for agent_file in sorted(AGENTS_SRC.glob("*.md")):
        build_codex_agent(agent_file, out_root)

    write_text(out_root / "AGENTS.md", render_codex_guidance())
    write_text(out_root / ".codex" / "config.toml", render_codex_config())
    write_text(
        out_root / ".codex" / "hooks.json",
        json.dumps(render_codex_hooks(), indent=2) + "\n",
    )


def build_all(root_target: Path) -> None:
    build_claude_runtime(root_target)
    build_codex_runtime(root_target)
