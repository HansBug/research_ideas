"""Parse signed markdown pack → parquet rows.

Each row carries:
- ``case_id`` / ``condition`` / ``component_kind`` / ``row_id``
- ``ref_id`` / ``pred_id`` (parsed from header line)
- ``claude_status`` / ``codex_status`` (from the two annotator bullets)
- ``user_choice``: one of ``"accept_claude" / "accept_codex" / "amend" / "reject" / "unsigned"``
- ``user_final_status``: TP / FP / FN / "" (only filled when amend/reject)
- ``user_note``: free text (备注 line)
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Optional


_HEADER_RE = re.compile(
    r"^##\s*#(?P<idx>\d+)(?:\s+(?P<flag>[^\n]*?))?\s+ref\s+`(?P<ref>[^`]*)`\s+↔\s+pred\s+`(?P<pred>[^`]*)`"
    r"\s*<!--\s*(?P<rowid>row\d+)\s*-->\s*$"
)
_ANNOT_LINE_RE = re.compile(
    r"^- \*\*(?P<who>Claude|gpt-5\.5) 提案\*\*：\*\*(?P<status>TP|FP|FN)（.*?\)"
)
_ANNOT_LINE_RE2 = re.compile(
    r"^- \*\*(?P<who>Claude|gpt-5\.5) 提案\*\*：\*\*(?P<statuszh>TP（命中）|FP（假阳）|FN（漏报）)\*\*"
)
_ZH_TO_STATUS = {"TP（命中）": "TP", "FP（假阳）": "FP", "FN（漏报）": "FN"}


def _norm_ref(s: str) -> Optional[str]:
    s = s.strip()
    if s == "∅" or not s:
        return None
    return s


def _checked(line: str) -> bool:
    return bool(re.search(r"^- \[[xX]\]", line.strip()))


def _extract_final_status(line: str) -> str:
    """From a `- [x] 修改 → final_status: TP` style line, get TP/FP/FN if present."""
    m = re.search(r"final_status:\s*([A-Za-z_]+)", line)
    if not m:
        return ""
    s = m.group(1).strip().upper()
    return s if s in {"TP", "FP", "FN"} else ""


def _extract_note(line: str) -> str:
    m = re.match(r"-\s*备注：\s*(.*)$", line.strip())
    return m.group(1).strip() if m else ""


def parse_pack(md_path: Path, *, case_id: str, condition: str, component_kind: str) -> list[dict[str, Any]]:
    text = Path(md_path).read_text(encoding="utf-8")
    rows: list[dict[str, Any]] = []
    blocks = text.split("\n## #")  # split on row headers
    # First block is header / instructions; skip until we see row headers
    for raw in blocks[1:]:
        block = "## #" + raw
        # Header
        header_match = _HEADER_RE.search(block.splitlines()[0]) if block.splitlines() else None
        if not header_match:
            continue
        row_id = header_match.group("rowid")
        flag = (header_match.group("flag") or "").strip()
        if flag.startswith("✅"):
            auto_marked = True
        else:
            auto_marked = False
        ref_id = _norm_ref(header_match.group("ref"))
        pred_id = _norm_ref(header_match.group("pred"))
        # Annotator statuses
        claude_status = ""
        codex_status = ""
        for line in block.splitlines():
            m = _ANNOT_LINE_RE2.match(line)
            if m:
                who = m.group("who")
                statuszh = m.group("statuszh")
                status = _ZH_TO_STATUS.get(statuszh, "")
                if who == "Claude":
                    claude_status = status
                elif who == "gpt-5.5":
                    codex_status = status
        # User choice
        user_choice = "unsigned"
        user_final_status = ""
        user_note = ""
        for line in block.splitlines():
            sline = line.strip()
            if sline.startswith("- 备注"):
                user_note = _extract_note(line)
                continue
            if not _checked(line):
                continue
            if "采纳 Claude" in line:
                user_choice = "accept_claude"
                user_final_status = claude_status
            elif "采纳 gpt-5.5" in line:
                user_choice = "accept_codex"
                user_final_status = codex_status
            elif "修改" in line:
                user_choice = "amend"
                user_final_status = _extract_final_status(line)
            elif "否决" in line:
                user_choice = "reject"
                user_final_status = _extract_final_status(line)
        rows.append({
            "case_id": case_id,
            "condition": condition,
            "component_kind": component_kind,
            "row_id": row_id,
            "ref_id": ref_id,
            "pred_id": pred_id,
            "claude_status": claude_status,
            "codex_status": codex_status,
            "auto_marked": auto_marked,  # heading 标 ✅ → 两 annotator 一致默认勾选
            "user_choice": user_choice,
            "user_final_status": user_final_status,
            "user_note": user_note,
        })
    return rows


def load_packs(packs_root: Path, *, out_parquet: Path) -> "pd.DataFrame":
    """Walk packs/{case}/{condition}/{kind}.md, return one big DataFrame and write parquet."""
    import pandas as pd
    rows: list[dict[str, Any]] = []
    for case_dir in sorted(Path(packs_root).iterdir()):
        if not case_dir.is_dir():
            continue
        case_id = case_dir.name
        for cond_dir in sorted(case_dir.iterdir()):
            if not cond_dir.is_dir():
                continue
            condition = cond_dir.name
            for md in sorted(cond_dir.glob("*.md")):
                kind = md.stem
                rows.extend(parse_pack(md, case_id=case_id, condition=condition, component_kind=kind))
    df = pd.DataFrame(rows)
    Path(out_parquet).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_parquet, index=False)
    return df
