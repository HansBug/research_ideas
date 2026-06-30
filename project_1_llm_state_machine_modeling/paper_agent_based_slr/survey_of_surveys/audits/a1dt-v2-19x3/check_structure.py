#!/usr/bin/env python3
"""A1-DT v2 结构门禁。

本脚本只检查 v2 审计骨架和 survey_of_surveys 文库结构，不判断论文内容真假。
可从仓库根目录运行，也可从本审计目录运行；不依赖本机绝对路径或仓库目录名。
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

EXPECTED_AGENTS = ("codex", "claude", "deepseek")
EXPECTED_PAPER_FILES = ("bibtex.bib", "metadata.json", "paper_content.txt", "review.md")
LIBRARY_REL = Path("project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys")
BATCH_REL = LIBRARY_REL / "audits/a1dt-v2-19x3"
V1_REL = LIBRARY_REL / "audits/a1dt-19x3"


def find_repo_root(start: Path) -> Path:
    """Locate repo root by walking upward from a file or directory path."""
    cur = start.resolve()
    if cur.is_file():
        cur = cur.parent
    for candidate in (cur, *cur.parents):
        if (candidate / ".git").exists() and (candidate / LIBRARY_REL).is_dir():
            return candidate
    raise SystemExit(f"cannot locate repository root from {start}")


def add_error(errors: list[str], message: str) -> None:
    errors.append(message)


def read_tasks(path: Path, errors: list[str]) -> list[dict[str, str]]:
    if not path.exists():
        add_error(errors, f"missing task file: {path}")
        return []
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    expected_fields = [
        "slug",
        "agent",
        "status",
        "prompt_path",
        "result_path",
        "log_path",
        "adjudication_path",
    ]
    if rows and rows[0].keys() != set(expected_fields):
        # DictReader preserves fieldnames separately; compare that for deterministic diagnostics.
        pass
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if reader.fieldnames != expected_fields:
            add_error(errors, f"TASKS.tsv header mismatch: {reader.fieldnames} != {expected_fields}")
    return rows


def check_markdown_links(summary_path: Path, errors: list[str]) -> None:
    if not summary_path.exists():
        return
    text = summary_path.read_text(encoding="utf-8", errors="ignore")
    required_markers = [
        "PR #135 A1-DT v2 抽取与审计口径",
        "A1-DT v2 统一总账表（按年份降序）",
        "A1-M0--M6 只作为跨论文投影",
        "audits/a1dt-v2-19x3/",
        "audits/a1dt-19x3/",
    ]
    for marker in required_markers:
        if marker not in text:
            add_error(errors, f"SUMMARY missing v2 marker: {marker}")
    if "| 年份 | 论文 | 类型 | venue/source | CCF 大类/等级 | 样本单位 | 样本数量 | 原生树类型 | 字段来源 | 统计池资格 | v2 审计状态 | review 链接 |" not in text:
        add_error(errors, "SUMMARY missing required v2 ledger header")




def check_ready_to_run(repo: Path, base: Path, batch: Path, rows: list[dict[str, str]], errors: list[str]) -> None:
    """Check v2 batch is executable, not only structurally present."""
    required_batch_files = [
        "generate_prompts.py",
        "run_tasks.py",
        "result-template.md",
        "adjudication-template.md",
    ]
    for rel in required_batch_files:
        if not (batch / rel).exists():
            add_error(errors, f"ready-to-run missing batch file: {rel}")

    prompt_markers = [
        "维度树 / 维度森林 = 这篇综述论文如何描述、编码、分类、统计它纳入的样本单位",
        "A1-M0--M6 只能作为跨论文投影提示",
        "禁止启动 subagent",
        "样本单位与字段来源判定",
        "原生样本编码维度树 / 维度森林",
        "对现有 `review.md` 的返修建议",
    ]
    for row in rows:
        prompt = batch / row.get("prompt_path", "")
        if not prompt.exists():
            add_error(errors, f"ready-to-run missing prompt: {row.get('prompt_path')}")
            continue
        text = prompt.read_text(encoding="utf-8", errors="ignore")
        for marker in prompt_markers:
            if marker not in text:
                add_error(errors, f"prompt {row.get('prompt_path')} missing marker: {marker}")

    audit_readme = base / "audits/README.md"
    if audit_readme.exists():
        audit_text = audit_readme.read_text(encoding="utf-8", errors="ignore")
        for marker in ["a1dt-v2-19x3", "v1-deprecated", "当前执行入口"]:
            if marker not in audit_text:
                add_error(errors, f"audits/README missing v2/v1 marker: {marker}")

    # Any review.md line that links v1 result must be guarded by a nearby v1-deprecated warning.
    for review in (base / "papers").glob("*/review.md"):
        text = review.read_text(encoding="utf-8", errors="ignore")
        for match in re.finditer(r"audits/a1dt-19x3/results", text):
            window = text[max(0, match.start() - 500): match.start() + 500]
            if "v1-deprecated" not in window:
                add_error(errors, f"{review.relative_to(repo)} has unguarded v1 audit result link")


def check_structure(strict: bool, ready_to_run: bool = False) -> int:
    repo = find_repo_root(Path(__file__).resolve())
    base = repo / LIBRARY_REL
    batch = repo / BATCH_REL
    papers = base / "papers"
    errors: list[str] = []

    for rel in [
        "README.md",
        "GUIDE.md",
        "SUMMARY.md",
        "papers",
        "audits/README.md",
        "audits/a1dt-v2-19x3/README.md",
        "audits/a1dt-v2-19x3/TASKS.tsv",
        "audits/a1dt-v2-19x3/check_structure.py",
        "audits/a1dt-v2-19x3/prompts/README.md",
        "audits/a1dt-v2-19x3/results/README.md",
        "audits/a1dt-v2-19x3/logs/README.md",
        "audits/a1dt-v2-19x3/adjudications/README.md",
    ]:
        if not (base / rel).exists():
            add_error(errors, f"missing library/audit path: {rel}")

    if not (repo / V1_REL).is_dir():
        add_error(errors, "missing v1 historical audit directory audits/a1dt-19x3")
    if (repo / V1_REL).resolve() == batch.resolve():
        add_error(errors, "v1 and v2 audit directories resolve to the same path")

    paper_dirs = sorted(p for p in papers.iterdir() if p.is_dir()) if papers.exists() else []
    if len(paper_dirs) != 19:
        add_error(errors, f"paper directory count should be 19, got {len(paper_dirs)}")
    paper_slugs = [p.name for p in paper_dirs]
    for d in paper_dirs:
        for name in EXPECTED_PAPER_FILES:
            if not (d / name).exists():
                add_error(errors, f"{d.name}: missing {name}")

    rows = read_tasks(batch / "TASKS.tsv", errors)
    if len(rows) != 57:
        add_error(errors, f"TASKS.tsv row count should be 57, got {len(rows)}")
    task_slugs = sorted({row.get("slug", "") for row in rows})
    if len(task_slugs) != 19:
        add_error(errors, f"TASKS.tsv slug count should be 19, got {len(task_slugs)}")
    if paper_slugs and task_slugs and task_slugs != paper_slugs:
        add_error(errors, f"TASKS slugs differ from paper dirs: tasks={task_slugs}, dirs={paper_slugs}")

    seen_pairs: set[tuple[str, str]] = set()
    for row in rows:
        slug = row.get("slug", "")
        agent = row.get("agent", "")
        status = row.get("status", "")
        pair = (slug, agent)
        if pair in seen_pairs:
            add_error(errors, f"duplicate task pair: {slug} {agent}")
        seen_pairs.add(pair)
        if slug not in paper_slugs:
            add_error(errors, f"task slug not found in papers/: {slug}")
        if agent not in EXPECTED_AGENTS:
            add_error(errors, f"{slug}: unexpected agent {agent}")
        if status not in {"planned", "completed", "blocked", "skipped"}:
            add_error(errors, f"{slug} {agent}: unexpected status {status}")
        for key in ("prompt_path", "result_path", "log_path", "adjudication_path"):
            value = row.get(key, "")
            if not value:
                add_error(errors, f"{slug} {agent}: empty {key}")
            if value.startswith("/") or ".." in Path(value).parts:
                add_error(errors, f"{slug} {agent}: {key} must be batch-relative: {value}")
            if "a1dt-19x3" in value and "a1dt-v2-19x3" not in value:
                add_error(errors, f"{slug} {agent}: {key} points to v1 path: {value}")
        if strict and status == "completed":
            for key in ("prompt_path", "result_path", "log_path"):
                target = batch / row.get(key, "")
                if not target.exists():
                    add_error(errors, f"{slug} {agent}: completed task missing {key}: {target}")
            adjudication = batch / row.get("adjudication_path", "")
            if not adjudication.exists():
                add_error(errors, f"{slug} {agent}: completed task missing adjudication: {adjudication}")

    for slug in paper_slugs:
        agents = sorted(row.get("agent", "") for row in rows if row.get("slug") == slug)
        if agents != sorted(EXPECTED_AGENTS):
            add_error(errors, f"{slug}: expected agents {EXPECTED_AGENTS}, got {agents}")

    check_markdown_links(base / "SUMMARY.md", errors)
    if ready_to_run:
        check_ready_to_run(repo, base, batch, rows, errors)

    if errors:
        print("A1-DT v2 structure check FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("A1-DT v2 structure check passed: library files, 19 paper dirs, 57 planned/completed tasks, v1/v2 separation and v2 audit skeleton are present. Ready-to-run checks also passed.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check A1-DT v2 audit skeleton and survey_of_surveys structure.")
    parser.add_argument("--strict", action="store_true", help="also require output files for tasks marked completed")
    parser.add_argument("--ready-to-run", action="store_true", help="also require materialized prompts, templates, and guarded v1 links")
    args = parser.parse_args(argv)
    return check_structure(strict=args.strict, ready_to_run=args.ready_to_run)


if __name__ == "__main__":
    raise SystemExit(main())
