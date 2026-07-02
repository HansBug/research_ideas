#!/usr/bin/env python3
"""检查 survey_of_surveys 19 篇 review.md 的 S1--S8 schema 小节。"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "papers"
AUDIT_ROOT = ROOT / "audits" / "a1-s1s8-19x1"
REQUIRED = [f"S{i}" for i in range(1, 9)]
FOURWAY_HEADER = "| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |"
FORBIDDEN_AUTHORED = [
    "不是第 5 个主挑战",
    "5 + 7 = 12",
    "12 个 action point",
    "15 个期刊 ISSN",
    "三主干（上下文元数据 × 制品可获得性 × 统计建模）",
    "Cited 指南 × 质量 回归",
    "应当进入主统计池",
    "可入主统计池",
    "tertiary-like",
    "是否需要降级：不需要",
    "6 studies NASA-TLX",
    "3 改善 / 2 中性 / 1",
    "四个 RQ 直接对应四棵结果子树",
    "court record",
    "显式关系 schema",
    "开放编码 → 主题归并",
    "当前 review.md 缺失的部分",
    "Validation Research = 56",
    "中位数 = 26",
    "Table 3 字段数：12",
    "\\fkappa",
]


def check_review(d: Path, errors: list[str]) -> None:
    review = d / "review.md"
    if not review.exists():
        errors.append(f"{d.name}: missing review.md")
        return
    text = review.read_text(encoding="utf-8")
    if "## survey_of_surveys 自身 schema 抽取" not in text:
        errors.append(f"{d.name}: missing schema section")
    if "### S1--S8 四分栏证据拆分" not in text:
        errors.append(f"{d.name}: missing four-way S1--S8 section")
    if FOURWAY_HEADER not in text:
        errors.append(f"{d.name}: missing exact four-way header")
    for s in REQUIRED:
        if f"| {s} " not in text:
            errors.append(f"{d.name}: missing table row {s}")
    if "final quantitative finding" not in text and "最终定量" not in text:
        errors.append(f"{d.name}: missing A1/A2a non-final boundary wording")
    if "A2a" not in text:
        errors.append(f"{d.name}: missing A2a handoff wording")


def check_round3(paper_dirs: list[Path], errors: list[str]) -> None:
    round3 = AUDIT_ROOT / "round3"
    if not round3.exists():
        errors.append("missing round3 audit directory")
        return
    slugs = {d.name for d in paper_dirs}
    audits = {p.stem for p in round3.glob("*.md") if p.name not in {"README.md", "round3-main-adjudication.md"}}
    if audits != slugs:
        errors.append(f"round3 audit slug mismatch: missing={sorted(slugs-audits)}, extra={sorted(audits-slugs)}")
    for d in paper_dirs:
        audit = round3 / f"{d.name}.md"
        if not audit.exists():
            errors.append(f"{d.name}: missing round3 audit file")
            continue
        text = audit.read_text(encoding="utf-8")
        for token in ["S1", "S8", "原生维度", "统计池", "A2a", "C/I/M"]:
            if token not in text:
                errors.append(f"{d.name}: round3 audit missing {token}")
    task = round3 / "TASKS.tsv"
    if not task.exists():
        errors.append("round3: missing TASKS.tsv")
    else:
        lines = [ln for ln in task.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if len(lines) != len(paper_dirs) + 1:
            errors.append(f"round3 TASKS.tsv expected {len(paper_dirs)} tasks, got {max(0, len(lines)-1)}")
        for lineno, line in enumerate(lines[1:], start=2):
            cols = line.split("\t")
            if len(cols) < 4:
                errors.append(f"round3 TASKS.tsv line {lineno}: expected at least 4 columns")
                continue
            if cols[0] not in slugs:
                errors.append(f"round3 TASKS.tsv line {lineno}: unknown slug {cols[0]}")
            if cols[3] != "completed":
                errors.append(f"round3 TASKS.tsv line {lineno}: status is {cols[3]!r}, expected completed")
    if not (round3 / "round3-main-adjudication.md").exists():
        errors.append("round3: missing round3-main-adjudication.md")


def check_prior_audits(paper_dirs: list[Path], errors: list[str]) -> None:
    slugs = {d.name for d in paper_dirs}
    for subdir in ["results", "adjudications"]:
        path = AUDIT_ROOT / subdir
        if not path.exists():
            errors.append(f"missing audit {subdir}/ directory")
            continue
        got = {p.stem for p in path.glob("*.md")}
        if got != slugs:
            errors.append(f"{subdir} slug mismatch: missing={sorted(slugs-got)}, extra={sorted(got-slugs)}")


def check_evidence_chain(d: Path, errors: list[str]) -> None:
    ev = d / "evidence_chain.md"
    if not ev.exists():
        errors.append(f"{d.name}: missing evidence_chain.md")
        return
    text = ev.read_text(encoding="utf-8")
    for token in ["## 审计附录：证据链与结论-证据映射", "### A.1", "### A.2", "### A.3", "### A.4"]:
        if token not in text:
            errors.append(f"{d.name}: evidence_chain missing {token}")


def check_summary(errors: list[str]) -> None:
    summary = ROOT / "SUMMARY.md"
    if not summary.exists():
        errors.append("missing SUMMARY.md")
        return
    text = summary.read_text(encoding="utf-8")
    for token in ["## 1.2 A1 S1--S8 Round 3 独立审计状态", "round3-main-adjudication.md", "S1--S4 逐篇覆盖矩阵", "S5--S8 逐篇覆盖矩阵", "后续主统计池候选", "A2a"]:
        if token not in text:
            errors.append(f"SUMMARY.md missing {token}")


def check_forbidden(errors: list[str]) -> None:
    authored = [ROOT / "SUMMARY.md", ROOT / "GUIDE.md"]
    authored.extend(PAPERS.glob("*/review.md"))
    authored.extend(PAPERS.glob("*/evidence_chain.md"))
    for f in authored:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8")
        for bad in FORBIDDEN_AUTHORED:
            if bad in text:
                errors.append(f"{f.relative_to(ROOT)}: forbidden residual phrase: {bad}")


def main() -> int:
    errors: list[str] = []
    paper_dirs = sorted(p for p in PAPERS.iterdir() if p.is_dir())
    if len(paper_dirs) != 19:
        errors.append(f"expected 19 paper dirs, got {len(paper_dirs)}")
    for d in paper_dirs:
        check_review(d, errors)
        check_evidence_chain(d, errors)
    check_prior_audits(paper_dirs, errors)
    check_round3(paper_dirs, errors)
    check_summary(errors)
    check_forbidden(errors)
    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print(f"PASS: {len(paper_dirs)} papers contain S1--S8 schema rows, four-way split, round3 audits, and no forbidden authored residuals")
    return 0


if __name__ == "__main__":
    sys.exit(main())
