"""Scan sources/ for T0+🟢 STM.md entries and emit candidates.jsonl.

Sample-level (per 条目), not file-level. One STM.md can yield multiple samples.

Output: paper_v1/selection/candidates.jsonl
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCES_DIR = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources"
OUT_PATH = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling"
    / "paper_v1"
    / "selection"
    / "candidates.jsonl"
)

# Match "## 条目 N: <title>" headings
ENTRY_HEADING = re.compile(r"^##\s*条目\s*(\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)


def parse_file_level(text: str) -> dict:
    """Pull file-level metadata from `## 盘点结论` block."""
    out: dict = {}
    m = re.search(r"##\s*盘点结论(.+?)(?=^##\s)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return out
    block = m.group(1)
    pairs = [
        ("rating", r"评级[:：]\s*(.+?)\s*$"),
        ("file_role", r"文件级角色[:：]\s*(.+?)\s*$"),
        ("stm_type", r"代表状态机类型[:：]\s*(.+?)\s*$"),
        ("time_level", r"代表时间级别[:：]\s*(.+?)\s*$"),
        ("structure_tags", r"结构标签概况[:：]\s*(.+?)\s*$"),
        ("entry_count", r"提取条目数[:：]\s*(\d+)"),
        ("brief", r"简要判断[:：]\s*(.+?)\s*$"),
    ]
    for key, pat in pairs:
        mm = re.search(pat, block, re.MULTILINE)
        if mm:
            out[key] = mm.group(1).strip()
    return out


def split_entries(text: str) -> list[tuple[int, str, int, int]]:
    """Return list of (entry_idx, title, start_offset, end_offset)."""
    headings = list(ENTRY_HEADING.finditer(text))
    out: list[tuple[int, str, int, int]] = []
    for i, m in enumerate(headings):
        start = m.start()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        out.append((int(m.group(1)), m.group(2).strip(), start, end))
    return out


def parse_entry_level(entry_text: str) -> dict:
    """Pull entry-level metadata from the entry block."""
    out: dict = {}
    pairs = [
        ("control_object", r"控制对象[:：]\s*(.+?)\s*$"),
        ("stm_type", r"状态机类型[:：]\s*(.+?)\s*$"),
        ("time_level", r"时间级别[:：]\s*(.+?)\s*$"),
        ("structure_tag", r"结构标签[:：]\s*(.+?)\s*$"),
        ("original_richness", r"原文细节充实度[:：]\s*(.+?)\s*$"),
        ("desc_richness", r"描述细节充实度[:：]\s*(.+?)\s*$"),
        ("dataset_role", r"数据集角色[:：]\s*(.+?)\s*$"),
        ("convergence_tag", r"趋同标签[:：]\s*(.+?)\s*$"),
    ]
    for key, pat in pairs:
        mm = re.search(pat, entry_text, re.MULTILINE)
        if mm:
            out[key] = mm.group(1).strip()
    return out


def extract_nl_description(entry_text: str) -> str:
    """Extract §2 基于原文整理后的自然语言描述."""
    m = re.search(
        r"###\s*2\.\s*基于原文整理后的自然语言描述\s*\n+(.+?)(?=^###\s|\Z)",
        entry_text,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1).strip() if m else ""


def is_t0_green_entry(file_meta: dict, entry_meta: dict) -> bool:
    """Filter rule. Entry-level beats file-level when both present."""
    time_level = entry_meta.get("time_level") or file_meta.get("time_level", "")
    rating = file_meta.get("rating", "")
    role = entry_meta.get("dataset_role") or file_meta.get("file_role", "")
    if "T0" not in time_level:
        return False
    if "🟢" not in rating and "🟢" not in role:
        return False
    return True


def is_structural_dropout(file_meta: dict, entry_meta: dict) -> tuple[bool, str]:
    """Hard exclusions from PATH1_HARD_COMPARISON_GUIDE §3.4."""
    tags = (entry_meta.get("structure_tag", "") + " " + file_meta.get("structure_tags", "")).lower()
    if "并行" in tags or "parallel" in tags:
        return True, "structure_tag_has_parallel"
    if "历史" in tags or "history" in tags:
        return True, "structure_tag_has_history"
    return False, ""


def main() -> None:
    SOURCES_DIR.parent  # sanity
    candidates: list[dict] = []
    skip_no_stm = 0
    skip_not_t0_green = 0
    skip_structural = 0
    skip_stub = 0

    for paper_dir in sorted(SOURCES_DIR.iterdir()):
        if not paper_dir.is_dir():
            continue
        stm_path = paper_dir / "STM.md"
        if not stm_path.exists():
            skip_no_stm += 1
            continue
        text = stm_path.read_text(encoding="utf-8")
        file_meta = parse_file_level(text)
        entries = split_entries(text)
        if not entries:
            skip_no_stm += 1
            continue
        for entry_idx, entry_title, start, end in entries:
            entry_text = text[start:end]
            entry_meta = parse_entry_level(entry_text)
            if not is_t0_green_entry(file_meta, entry_meta):
                skip_not_t0_green += 1
                continue
            dropped, reason = is_structural_dropout(file_meta, entry_meta)
            if dropped:
                skip_structural += 1
                continue
            nl_desc = extract_nl_description(entry_text)
            if len(nl_desc) < 200:  # too thin to be a real sample
                skip_stub += 1
                continue
            sample_id = f"{paper_dir.name}__{entry_idx:02d}"
            candidates.append(
                {
                    "sample_id": sample_id,
                    "paper_slug": paper_dir.name,
                    "entry_idx": entry_idx,
                    "entry_title": entry_title,
                    "file_meta": file_meta,
                    "entry_meta": entry_meta,
                    "nl_description": nl_desc,
                    "stm_md_path": str(stm_path.relative_to(REPO_ROOT)),
                    "paper_txt_path": str((paper_dir / "paper_content.txt").relative_to(REPO_ROOT))
                    if (paper_dir / "paper_content.txt").exists() else None,
                    "paper_pdf_path": str((paper_dir / "paper.pdf").relative_to(REPO_ROOT))
                    if (paper_dir / "paper.pdf").exists() else None,
                    "entry_text_offsets": {"start": start, "end": end},
                }
            )

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", encoding="utf-8") as f:
        for row in candidates:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    by_type: dict[str, int] = {}
    for c in candidates:
        t = (c["entry_meta"].get("stm_type") or c["file_meta"].get("stm_type", "?"))
        # normalize
        for k in ("FSM", "EFSM", "HSM", "Hybrid", "Protocol", "Resource"):
            if k in t:
                by_type[k] = by_type.get(k, 0) + 1
                break
        else:
            by_type["Other"] = by_type.get("Other", 0) + 1

    print(f"[build_candidates] total T0+🟢 samples: {len(candidates)}")
    print(f"  by stm_type: {by_type}")
    print(f"  skipped: no_stm={skip_no_stm} not_t0_green={skip_not_t0_green} "
          f"structural={skip_structural} stub={skip_stub}")
    print(f"  wrote: {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
