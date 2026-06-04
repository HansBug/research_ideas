#!/usr/bin/env python3
"""Health smoke for the repo-local ``agent_loop_skill`` workspace.

The PR-skill-fix branch intentionally keeps all fixes inside this directory.
This script is therefore both a lightweight regression test and a human-readable
audit helper for Codex / Claude Code agents: it checks that the skill entry
points, stage symlinks, E2 boundaries, and PR-E1 repair vocabulary still point
to the current workflow without requiring the full agent-loop runtime.

Usage from repository root:

```
python project_1_llm_state_machine_modeling/method/agent_loop_skill/health_check.py
python project_1_llm_state_machine_modeling/method/agent_loop_skill/health_check.py --format json
```
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKILL_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class CheckResult:
    """One skill-health check result."""

    name: str
    ok: bool
    detail: str


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _contains_all(text: str, terms: Iterable[str]) -> list[str]:
    return [term for term in terms if term not in text]


def _line_contains_any(text: str, needle: str, allowed_markers: Iterable[str]) -> list[str]:
    bad_lines: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        if needle not in line:
            continue
        if not any(marker in line for marker in allowed_markers):
            bad_lines.append(f"L{lineno}: {line.strip()}")
    return bad_lines


def _check_entry_symlinks(root: Path) -> CheckResult:
    target = root / "AGENT_LOOP_SKILL.md"
    if not target.is_file():
        return CheckResult("entry_symlinks", False, "missing AGENT_LOOP_SKILL.md")
    failures: list[str] = []
    for name in ["SKILL.md", "CLAUDE.md"]:
        link = root / name
        if not link.is_symlink():
            failures.append(f"{name} is not a symlink")
        elif link.resolve() != target.resolve():
            failures.append(f"{name} resolves to {link.resolve()}, expected {target.resolve()}")
    return CheckResult(
        "entry_symlinks",
        not failures,
        "SKILL.md / CLAUDE.md resolve to AGENT_LOOP_SKILL.md" if not failures else "; ".join(failures),
    )


def _check_stage_symlinks(root: Path) -> CheckResult:
    stage_dir = root / "stages"
    failures: list[str] = []
    for path in sorted(stage_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        if not path.is_symlink():
            failures.append(f"{path.name} is not a symlink")
            continue
        if not path.exists():
            failures.append(f"{path.name} target is broken: {path.readlink()}")
    return CheckResult(
        "stage_symlinks_resolve",
        not failures,
        "all stage symlinks resolve" if not failures else "; ".join(failures),
    )


def _check_stage_symlink_strategy(root: Path) -> CheckResult:
    readme = root / "stages" / "README.md"
    if not readme.is_file():
        return CheckResult("stage_symlink_strategy", False, "missing stages/README.md")
    text = _read(readme)
    required = ["只读", "method/stages/docs", "SD-10", "SL-10B", "legacy", "SL-10", "FixRequestBatch"]
    missing = _contains_all(text, required)
    return CheckResult(
        "stage_symlink_strategy",
        not missing,
        "stages/README.md documents read-only symlink and legacy-stage policy"
        if not missing
        else "missing terms: " + ", ".join(missing),
    )


def _check_forbidden_top_runner(root: Path) -> CheckResult:
    docs = {
        "AGENT_LOOP_SKILL.md": _read(root / "AGENT_LOOP_SKILL.md"),
        "e2e_ref_model_guide.md": _read(root / "e2e_ref_model_guide.md"),
    }
    required = ["method.loop.run_agent_loop", "PR-D representative runner", "一键 full staged runner"]
    failures: list[str] = []
    for name, text in docs.items():
        missing = _contains_all(text, required)
        if missing:
            failures.append(f"{name} missing explicit bans: {', '.join(missing)}")
    return CheckResult(
        "forbidden_top_runner",
        not failures,
        "skill docs explicitly ban top-level agent-loop / PR-D / one-shot runners"
        if not failures
        else "; ".join(failures),
    )


def _check_repair_chain_terms(root: Path) -> CheckResult:
    files = ["AGENT_LOOP_SKILL.md", "tools.md", "prompts.md", "e2e_ref_model_guide.md"]
    required = ["FixRequestBatch", "FixLog", "SL-9", "SL-10"]
    failures: list[str] = []
    for name in files:
        text = _read(root / name)
        missing = _contains_all(text, required)
        if missing:
            failures.append(f"{name} missing: {', '.join(missing)}")
    return CheckResult(
        "repair_chain_terms",
        not failures,
        "skill docs expose PR-E1 FixRequestBatch/FixLog/SL-9/SL-10 vocabulary"
        if not failures
        else "; ".join(failures),
    )


def _check_tools_no_misleading_legacy(root: Path) -> CheckResult:
    tools = _read(root / "tools.md")
    forbidden_phrases = [
        "PR-E1 runtime 会把它提升为",
        "FixPlan.suggested_fix_hints",
    ]
    present = [phrase for phrase in forbidden_phrases if phrase in tools]
    required_terms = [
        "PR-E1 已将默认 repair 主链提升为",
        "[prompts.md](./prompts.md)",
        "FixRequest.suggested_fix_hints",
    ]
    missing = _contains_all(tools, required_terms)
    ok = not present and not missing
    details: list[str] = []
    if present:
        details.append("misleading legacy phrases still present: " + ", ".join(present))
    if missing:
        details.append("missing updated terms: " + ", ".join(missing))
    return CheckResult(
        "tools_no_misleading_legacy",
        ok,
        "tools.md uses current FixRequestBatch/FixLog wording and points to prompts.md"
        if ok
        else "; ".join(details),
    )


def _check_e2e_input_grounding(root: Path) -> CheckResult:
    guide = _read(root / "e2e_ref_model_guide.md")
    required = ["NL 片段", "论文子路径", "paper_content.txt", "paper.pdf", "bibtex.bib"]
    missing = _contains_all(guide, required)
    return CheckResult(
        "e2e_input_grounding",
        not missing,
        "e2e guide requires NL fragment plus paper directory evidence"
        if not missing
        else "missing terms: " + ", ".join(missing),
    )


def _check_run_agent_loop_mentions_are_guarded(root: Path) -> CheckResult:
    allowed_markers = ["不得", "禁止", "不调用", "不要", "not", "不是", "默认入口", "PR-C config"]
    failures: list[str] = []
    for path in sorted(root.glob("*.md")):
        bad = _line_contains_any(_read(path), "run_agent_loop", allowed_markers)
        if bad:
            failures.append(f"{path.name}: " + " | ".join(bad[:3]))
    return CheckResult(
        "run_agent_loop_mentions_guarded",
        not failures,
        "run_agent_loop mentions are guarded by ban/boundary language"
        if not failures
        else "; ".join(failures),
    )




def _check_pr_e1_design_residue(root: Path) -> CheckResult:
    docs = {
        "AGENT_LOOP_SKILL.md": _read(root / "AGENT_LOOP_SKILL.md"),
        "e2e_ref_model_guide.md": _read(root / "e2e_ref_model_guide.md"),
        "stages/README.md": _read(root / "stages" / "README.md"),
    }
    required = [
        "FixRequestBatch",
        "FixLog",
        "waiver",
        "rework",
        "SL-10(NL + FixLog + local evidence)",
        "SD-10",
        "SL-10B",
        "local-evidence",
        "diagnostic_hot_start",
        "SD-6",
        "NFRR",
    ]
    missing: list[str] = []
    combined = "\n".join(docs.values())
    for term in required:
        if term not in combined:
            missing.append(term)
    return CheckResult(
        "pr_e1_design_residue",
        not missing,
        "skill docs carry PR-E1 repair/FixLog/SL-10/scenario-provenance residue policy"
        if not missing
        else "missing terms: " + ", ".join(missing),
    )


def _check_no_case_specific_optimization(root: Path) -> CheckResult:
    docs = {
        "AGENT_LOOP_SKILL.md": _read(root / "AGENT_LOOP_SKILL.md"),
        "e2e_ref_model_guide.md": _read(root / "e2e_ref_model_guide.md"),
    }
    combined = "\n".join(docs.values())
    required = ["禁止", "ABS", "Elevator", "CARA", "LNG", "特判"]
    missing = [term for term in required if term not in combined]
    return CheckResult(
        "no_case_specific_optimization_policy",
        not missing,
        "skill docs explicitly ban lexical special-cases for the four smoke samples"
        if not missing
        else "missing anti-overfit terms: " + ", ".join(missing),
    )

def run_checks(root: Path = SKILL_ROOT) -> list[CheckResult]:
    return [
        _check_entry_symlinks(root),
        _check_stage_symlinks(root),
        _check_stage_symlink_strategy(root),
        _check_forbidden_top_runner(root),
        _check_repair_chain_terms(root),
        _check_tools_no_misleading_legacy(root),
        _check_pr_e1_design_residue(root),
        _check_no_case_specific_optimization(root),
        _check_e2e_input_grounding(root),
        _check_run_agent_loop_mentions_are_guarded(root),
    ]


def _format_markdown(results: list[CheckResult]) -> str:
    status = "PASS" if all(item.ok for item in results) else "FAIL"
    lines = [
        "# agent_loop_skill health check",
        "",
        f"- overall: `{status}`",
        f"- skill_root: `{SKILL_ROOT}`",
        "",
        "| check | status | detail |",
        "|---|---|---|",
    ]
    for item in results:
        emoji = "✅" if item.ok else "❌"
        detail = item.detail.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{item.name}` | {emoji} | {detail} |")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = parser.parse_args()

    results = run_checks()
    if args.format == "json":
        print(json.dumps([asdict(item) for item in results], ensure_ascii=False, indent=2))
    else:
        print(_format_markdown(results))
    return 0 if all(item.ok for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
