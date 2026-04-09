from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import TypedDict, cast

ROOT = Path(__file__).resolve().parents[1]


class IssueRecord(TypedDict, total=False):
    id: str
    title: str
    depends_on_id: str


class EpicDefinition(TypedDict):
    title: str
    labels: list[str]
    priority: str
    description: str
    acceptance: str
    tasks: list[str]


def run_bd_text(*args: str) -> str:
    cmd = ["bd", *args]
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


def run_bd_json(*args: str) -> list[IssueRecord]:
    output = run_bd_text(*args)
    data = json.loads(output or "[]")
    if not isinstance(data, list):
        raise TypeError("Expected Beads JSON output to be a list.")
    return cast(list[IssueRecord], data)


def get_existing_by_title() -> dict[str, IssueRecord]:
    issues = run_bd_json("list", "--all", "--json")
    return {issue["title"]: issue for issue in issues}


def ensure_issue(
    existing: dict[str, IssueRecord],
    *,
    title: str,
    issue_type: str,
    description: str,
    acceptance: str,
    labels: list[str],
    priority: str,
    parent: str | None = None,
) -> str:
    if title in existing:
        return existing[title]["id"]

    args = [
        "create",
        "--title",
        title,
        "--type",
        issue_type,
        "--description",
        description,
        "--acceptance",
        acceptance,
        "--labels",
        ",".join(labels),
        "--priority",
        priority,
        "--silent",
    ]
    if parent:
        args.extend(["--parent", parent])

    issue_id = run_bd_text(*args)
    existing[title] = {"id": issue_id, "title": title}
    return issue_id


def add_dep(blocked: str, blocker: str) -> None:
    deps = run_bd_json("dep", "list", blocked, "--json")
    if any(dep.get("depends_on_id") == blocker for dep in deps):
        return
    run_bd_text("dep", "add", blocked, blocker)


def export_issues() -> None:
    run_bd_text("export", "--no-memories", "-o", ".beads/issues.jsonl")


def main() -> int:
    existing = get_existing_by_title()

    foundation_epic = ensure_issue(
        existing,
        title="Proof program: repository foundation",
        issue_type="epic",
        description="Bootstrap the repo with skill-harness tooling, reproducible backlog artifacts, and proof-program scaffolding.",
        acceptance=(
            "- skill-harness repo tooling is integrated without losing genome-specific policy\n"
            "- Beads issues are exported to .beads/issues.jsonl\n"
            "- benchmark and evaluation manifests exist and pass validation"
        ),
        labels=["proof-program", "foundation", "tooling"],
        priority="P1",
    )

    foundation_tasks = [
        "Integrate skill-harness project tooling into open-genome-agent",
        "Bootstrap Beads backlog and export .beads/issues.jsonl",
        "Add benchmark and evaluation manifest scaffolding",
        "Align noslop quality gates with repo build and test commands",
    ]
    foundation_ids: list[str] = []
    for title in foundation_tasks:
        foundation_ids.append(
            ensure_issue(
                existing,
                title=title,
                issue_type="task",
                description="Repository-foundation work required before the proof program can be executed reliably.",
                acceptance="- repo changes are committed, verified, and reflected in tracked backlog artifacts",
                labels=["proof-program", "foundation"],
                priority="P1",
                parent=foundation_epic,
            )
        )

    epics: list[EpicDefinition] = [
        {
            "title": "Proof program: benchmark core",
            "labels": ["proof-program", "benchmark", "hg002"],
            "priority": "P1",
            "description": "Establish the first hard proof layer with GIAB HG002 and reproducible benchmark outputs.",
            "acceptance": "- HG002 benchmark run is reproducible\n- metrics JSON is emitted\n- HTML summary is generated",
            "tasks": [
                "Scaffold benchmarks/hg002 workspace",
                "Pin GIAB HG002 asset manifest",
                "Add hap.py benchmark wrapper",
                "Parse HG002 benchmark metrics into JSON",
                "Render HG002 benchmark HTML summary",
                "Document local HG002 benchmark instructions",
            ],
        },
        {
            "title": "Proof program: hard-region evaluation",
            "labels": ["proof-program", "benchmark", "cmrg"],
            "priority": "P1",
            "description": "Add a difficult medically relevant genes proof layer that is separate from easy-region HG002 reporting.",
            "acceptance": "- CMRG evaluation mode exists\n- per-gene support output is emitted\n- unsupported genes are explicit",
            "tasks": [
                "Pin CMRG asset manifest",
                "Add CMRG evaluation mode",
                "Emit per-gene CMRG scorecard",
                "Publish supported challenging genes page",
            ],
        },
        {
            "title": "Proof program: public genome walkthrough",
            "labels": ["proof-program", "public-demo", "pgp"],
            "priority": "P1",
            "description": "Build the first real public human-style walkthrough on an openly shared genome.",
            "acceptance": "- public sample selection is documented\n- walkthrough is locally reproducible\n- report is evidence-bound and caveated",
            "tasks": [
                "Select first Harvard PGP public sample",
                "Write public genome ingestion guide",
                "Add public-demo report template",
                "Script CLI walkthrough on the public sample",
                "Document privacy and consent boundaries for public demos",
            ],
        },
        {
            "title": "Proof program: interpretation evaluation",
            "labels": ["proof-program", "interpretation"],
            "priority": "P1",
            "description": "Benchmark interpretation discipline separately from parser or benchmark correctness.",
            "acceptance": "- ClinVar, PGx, PRS, and functional example packs exist\n- source class and confidence remain explicit",
            "tasks": [
                "Build ClinVar higher-review-status evaluation pack",
                "Add CPIC pharmacogenomics example pack",
                "Add PharmVar allele example pack",
                "Add PGS Catalog demo score pack",
                "Add MaveDB functional example pack",
                "Write interpretation evidence-grading rubric",
            ],
        },
        {
            "title": "Proof program: reasoning evaluation",
            "labels": ["proof-program", "reasoning", "variantbench"],
            "priority": "P2",
            "description": "Compare reasoning quality and unsupported-claim rates across harnesses without mixing them into benchmark metrics.",
            "acceptance": "- reasoning harness exists\n- unsupported-claim scoring exists\n- backend comparison output is structured",
            "tasks": [
                "Add VariantBench or equivalent reasoning harness",
                "Define reasoning result schema",
                "Score unsupported claims and contradictions",
                "Compare Claude and Codex reasoning runs",
            ],
        },
        {
            "title": "Proof program: scale and population workflows",
            "labels": ["proof-program", "scale", "1000g"],
            "priority": "P2",
            "description": "Prove the repo behaves predictably across many public genomes with population-aware caveats.",
            "acceptance": "- 1000 Genomes manifest exists\n- batch mode exists\n- population-aware summary exists",
            "tasks": [
                "Pin 1000 Genomes sample manifest",
                "Add public-cohort batch query mode",
                "Add population-aware summary page",
                "Add throughput benchmark summary for public cohort runs",
            ],
        },
        {
            "title": "Proof program: landing page and demo assets",
            "labels": ["proof-program", "docs", "showcase"],
            "priority": "P2",
            "description": "Surface the proof stack clearly in the repo home page and demo assets.",
            "acceptance": "- README links to proof artifacts\n- benchmark and report screenshots are captured\n- limitations are visible next to headline claims",
            "tasks": [
                "Add proof-program links to README",
                "Create benchmark screenshot card",
                "Create public report screenshot asset",
                "Capture CLI provenance demo transcript",
                "Publish a what-we-do-not-claim panel",
            ],
        },
        {
            "title": "Proof program: optional raw-data path",
            "labels": ["proof-program", "workflow", "raw-data"],
            "priority": "P3",
            "description": "Add the raw-data entry path only after the VCF-first proof stack is stable.",
            "acceptance": "- raw-data route is optional\n- workflow provenance is captured\n- VCF-first path remains first-class",
            "tasks": [
                "Add optional Nextflow raw-data route",
                "Define raw-input manifest schema",
                "Capture provenance for long-running workflow jobs",
            ],
        },
    ]

    epic_ids: dict[str, str] = {}
    task_ids: dict[str, list[str]] = {}
    for epic in epics:
        epic_id = ensure_issue(
            existing,
            title=epic["title"],
            issue_type="epic",
            description=epic["description"],
            acceptance=epic["acceptance"],
            labels=epic["labels"],
            priority=epic["priority"],
        )
        epic_ids[epic["title"]] = epic_id
        child_ids: list[str] = []
        for task_title in epic["tasks"]:
            child_ids.append(
                ensure_issue(
                    existing,
                    title=task_title,
                    issue_type="task",
                    description=f"Deliver the scoped work for: {epic['title']}.",
                    acceptance="- work is implemented with reproducible commands, updated docs, and matching evidence artifacts where applicable",
                    labels=epic["labels"],
                    priority=epic["priority"],
                    parent=epic_id,
                )
            )
        task_ids[epic["title"]] = child_ids

    for task_group in task_ids.values():
        for blocked, blocker in zip(task_group[1:], task_group[:-1]):
            add_dep(blocked, blocker)

    export_issues()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
