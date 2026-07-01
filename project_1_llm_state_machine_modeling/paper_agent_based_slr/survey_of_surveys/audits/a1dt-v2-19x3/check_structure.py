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
TEXT_HYGIENE_SUFFIXES = {".md", ".tsv", ".py", ".json", ".log"}
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
    new_header = "| 年份 | 论文 | 类型 | venue/source | CCF 大类/等级 | CCF 复核状态 | 样本单位 | 样本数量 | 原生树类型 | 字段来源 | 统计池资格 | v2 审计状态 | review 链接 |"
    old_header = "| 年份 | 论文 | 类型 | venue/source | CCF 大类/等级 | 样本单位 | 样本数量 | 原生树类型 | 字段来源 | 统计池资格 | v2 审计状态 | review 链接 |"
    if new_header not in text:
        add_error(errors, "SUMMARY missing required v2 ledger header with CCF 复核状态 column")
    if old_header in text:
        add_error(errors, "SUMMARY still contains old v2 ledger header without CCF 复核状态 column")


def check_text_hygiene(root: Path, repo: Path, errors: list[str]) -> None:
    """Require LF endings and no trailing spaces in audit text artifacts."""
    if not root.exists():
        return
    for path in sorted(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in TEXT_HYGIENE_SUFFIXES):
        data = path.read_bytes()
        rel = path.relative_to(repo)
        if b"\r" in data:
            add_error(errors, f"text hygiene CR character found: {rel}")
        for lineno, line in enumerate(data.splitlines(), start=1):
            if line.endswith((b" ", b"\t")):
                add_error(errors, f"text hygiene trailing whitespace: {rel}:{lineno}")
                break




def extract_section(text: str, start_marker: str, end_marker: str | None = None) -> str:
    """Extract a markdown section by an exact heading line.

    A1-DT v2 review files also preserve historical draft blocks such as
    ``#### A.2 维度树证据账本草案``.  A plain substring search would match those
    draft headings and then incorrectly validate stale EV-* examples instead of
    the formal ``### A.2`` / ``### A.3`` appendix.  Match heading lines exactly
    enough to keep the structure gate tied to the current claim map.
    """
    start_re = re.compile(rf"^\s*{re.escape(start_marker)}.*$", re.M)
    start_match = start_re.search(text)
    if not start_match:
        return ""
    start = start_match.start()
    if end_marker is None:
        return text[start:]
    end_re = re.compile(rf"^\s*{re.escape(end_marker)}.*$", re.M)
    end_match = end_re.search(text, start_match.end())
    return text[start:] if not end_match else text[start:end_match.start()]


def parse_markdown_table(section: str) -> tuple[list[str], list[list[str]]]:
    """Parse the first markdown table in a section with conservative rules."""
    header: list[str] = []
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols:
            continue
        if all(re.fullmatch(r":?-{3,}:?", c or "") for c in cols):
            continue
        if not header:
            header = cols
            continue
        rows.append(cols)
    return header, rows


def normalize_boolish(value: str) -> str:
    return value.strip().lower().replace(" ", "")


def split_source_ids(value: str) -> list[str]:
    """Extract source ids from a markdown cell.

    A.2 rows may use semicolon-separated source ids.  Links are not expected in
    this cell, but regex extraction is intentionally tolerant so Chinese prose
    around the ids does not break the gate.
    """
    return re.findall(r"src-[A-Za-z0-9-]+", value)


def parse_formal_a1_a2_a3(
    review_path: Path, errors: list[str] | None = None, repo: Path | None = None
) -> tuple[set[str], set[str], dict[str, str], dict[str, list[str]], dict[str, list[str]], dict[str, str]]:
    text = review_path.read_text(encoding="utf-8", errors="ignore")
    a1 = extract_section(text, "### A.1 论文与本地文件来源", "### A.2 维度树证据账本")
    a2 = extract_section(text, "### A.2 维度树证据账本", "### A.3 结论-证据映射")
    a3 = extract_section(text, "### A.3 结论-证据映射", "### A.4 本地复验命令")

    source_ids: set[str] = set()
    evidence_ids: set[str] = set()
    evidence_sources: dict[str, list[str]] = {}
    evidence_strengths: dict[str, str] = {}
    claim_types: dict[str, str] = {}
    claim_evidence: dict[str, list[str]] = {}

    rel = review_path.relative_to(repo) if repo is not None else review_path

    a1_header, a1_rows = parse_markdown_table(a1)
    if a1_header and "来源标识" not in a1_header and errors is not None:
        add_error(errors, f"{rel} A.1 table header must include 来源标识")
    for cols in a1_rows:
        if cols and cols[0].startswith("src-"):
            source_ids.add(cols[0])

    a2_header, a2_rows = parse_markdown_table(a2)
    if errors is not None:
        if not a2_header:
            add_error(errors, f"{rel} missing formal A.2 table")
        elif "来源标识" not in a2_header:
            add_error(errors, f"{rel} formal A.2 table missing 来源标识 column")
    a2_index = {name: i for i, name in enumerate(a2_header)}
    source_idx = a2_index.get("来源标识")
    strength_idx = a2_index.get("证据强度")
    page_idx = a2_index.get("原文页码")
    range_idx = a2_index.get("段落或行号范围")
    visual_idx = a2_index.get("需要原文版面核验")

    for cols in a2_rows:
        if not cols or not cols[0].startswith("ev-"):
            continue
        evidence_id = cols[0]
        evidence_ids.add(evidence_id)
        if source_idx is not None and source_idx < len(cols):
            refs = split_source_ids(cols[source_idx])
        else:
            refs = []
        evidence_sources[evidence_id] = refs
        if strength_idx is not None and strength_idx < len(cols):
            evidence_strengths[evidence_id] = cols[strength_idx]

        if errors is not None:
            if not refs:
                add_error(errors, f"{rel} A.2 evidence {evidence_id} has empty/unparseable 来源标识")
            for sid in refs:
                if sid not in source_ids:
                    add_error(errors, f"{rel} A.2 evidence {evidence_id} references unknown A.1 source {sid}")
            joined = " | ".join(cols)
            page_value = cols[page_idx] if page_idx is not None and page_idx < len(cols) else ""
            range_value = cols[range_idx] if range_idx is not None and range_idx < len(cols) else ""
            visual_value = cols[visual_idx] if visual_idx is not None and visual_idx < len(cols) else ""
            needs_a2a = "待 A2a" in joined
            needs_visual = normalize_boolish(visual_value) in {"是", "true", "yes", "y", "需", "需要"}
            strength = evidence_strengths.get(evidence_id, "")
            if (needs_a2a or needs_visual) and ("文本已核验" in strength or "text_verified" in strength):
                add_error(
                    errors,
                    f"{rel} A.2 evidence {evidence_id} still claims text_verified while pending A2a/visual check "
                    f"(page={page_value!r}, range={range_value!r}, visual={visual_value!r})",
                )

    a3_header, a3_rows = parse_markdown_table(a3)
    if errors is not None and not a3_header:
        add_error(errors, f"{rel} missing formal A.3 table")
    a3_index = {name: i for i, name in enumerate(a3_header)}
    claim_strength_idx = a3_index.get("结论强度")
    for cols in a3_rows:
        if len(cols) >= 6 and cols[1].startswith("A1DT-"):
            claim_id = cols[1]
            claim_types[claim_id] = cols[3]
            evs = [x.strip() for x in re.split(r"[,，]", cols[5]) if x.strip() and x.strip() != "--"]
            claim_evidence[claim_id] = evs
            if errors is not None and claim_strength_idx is not None and claim_strength_idx < len(cols):
                claim_strength = cols[claim_strength_idx]
                relies_on_not_verified = any("not_verified" in evidence_strengths.get(ev, "") for ev in evs)
                if relies_on_not_verified and "adjudicated" not in claim_strength and "not_verified" not in claim_strength:
                    add_error(
                        errors,
                        f"{rel} A.3 claim {claim_id} relies on not_verified A.2 evidence but has strength {claim_strength!r}",
                    )
                if "not_verified" in claim_strength and ("文本已核验" in claim_strength or "text_verified" in claim_strength):
                    add_error(errors, f"{rel} A.3 claim {claim_id} mixes not_verified with text_verified: {claim_strength!r}")
    return source_ids, evidence_ids, claim_types, claim_evidence, evidence_sources, evidence_strengths


def check_summary_semantics(base: Path, repo: Path, errors: list[str]) -> None:
    summary_path = base / "SUMMARY.md"
    if not summary_path.exists():
        return
    summary = summary_path.read_text(encoding="utf-8", errors="ignore")
    papers = base / "papers"
    all_claim_types: dict[str, str] = {}
    all_claim_evidence: dict[str, tuple[Path, list[str]]] = {}
    for review in sorted(papers.glob("*/review.md")):
        _source_ids, evidence_ids, claim_types, claim_evidence, _evidence_sources, _evidence_strengths = parse_formal_a1_a2_a3(review, errors, repo)
        for cid, ctype in claim_types.items():
            all_claim_types[cid] = ctype
            all_claim_evidence[cid] = (review, claim_evidence.get(cid, []))
            for ev in claim_evidence.get(cid, []):
                if ev not in evidence_ids:
                    add_error(errors, f"{review.relative_to(repo)} A.3 claim {cid} references missing formal A.2 evidence {ev}")

    for cid in sorted(set(re.findall(r"A1DT-[A-Za-z0-9-]+-C\d+", summary))):
        if cid not in all_claim_types:
            add_error(errors, f"SUMMARY references missing A.3 claim id: {cid}")

    tree_section = extract_section(summary, "## 6.1 维度树模式总览", "## 6.2 维度树类型")
    for cid in re.findall(r"A1DT-[A-Za-z0-9-]+-C\d+", tree_section):
        if not cid.endswith("-C03"):
            add_error(errors, f"SUMMARY §6.1 tree overview should cite C03 tree claims, got {cid}")
        elif "树类型" not in all_claim_types.get(cid, "") and "tree_type" not in all_claim_types.get(cid, ""):
            add_error(errors, f"SUMMARY §6.1 cites {cid} but its A.3 type is {all_claim_types.get(cid)!r}, not tree_type")

    expected = {
        "sum-A1DT-tree-types": "-C03",
        "sum-A1DT-statistical-pool": "-C04",
        "sum-A1DT-boundary-anchor": "-C04",
    }
    for marker, suffix in expected.items():
        m = re.search(rf"^\| \[{re.escape(marker)}\].*$", summary, flags=re.M)
        if not m:
            add_error(errors, f"SUMMARY missing row {marker}")
            continue
        row = m.group(0)
        for cid in re.findall(r"A1DT-[A-Za-z0-9-]+-C\d+", row):
            if not cid.endswith(suffix):
                add_error(errors, f"SUMMARY row {marker} should cite {suffix} claims, got {cid}")
            if suffix == "-C03" and "树类型" not in all_claim_types.get(cid, "") and "tree_type" not in all_claim_types.get(cid, ""):
                add_error(errors, f"SUMMARY row {marker} cites non-tree claim {cid}: {all_claim_types.get(cid)!r}")
            if suffix == "-C04" and "eligibility" not in all_claim_types.get(cid, ""):
                add_error(errors, f"SUMMARY row {marker} cites non-eligibility claim {cid}: {all_claim_types.get(cid)!r}")


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
    if strict:
        check_text_hygiene(batch, repo, errors)
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
    check_summary_semantics(base, repo, errors)
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
