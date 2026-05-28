"""Build pool.tsv + selection.json for PATH1 NL expansion.

Sources:
  - paper_v1/selection/candidates.jsonl    (323 sample metadata)
  - paper_v1/selection/SELECTION_REPORT.md (15 candidate + 15 backup picks)
  - paper_v1/selection/domain_emoji.json   (paper_slug → domain emoji)

Outputs (relative to this script):
  - pool.tsv         : tab-separated 30-row table consumed by run_expand.sh
  - selection.json   : {candidates: [...], backup: [...]} consumed by orchestrate_expand.sh

pool.tsv columns (matches path-2 schema):
  id  bucket  slug  casename  stm_path  pdf_path  txt_path  paper_num  domain
"""
from __future__ import annotations

import json
import re
from pathlib import Path

EXP_DIR = Path(__file__).resolve().parent
SEL_ROOT = EXP_DIR.parent
REPO_ROOT = SEL_ROOT.parents[2]

CANDIDATES_JSONL = SEL_ROOT / "candidates.jsonl"
REPORT_MD = SEL_ROOT / "SELECTION_REPORT.md"
DOMAIN_EMOJI = SEL_ROOT / "domain_emoji.json"

POOL_TSV = EXP_DIR / "pool.tsv"
SELECTION_JSON = EXP_DIR / "selection.json"


def load_candidates() -> dict[str, dict]:
    by_id: dict[str, dict] = {}
    with CANDIDATES_JSONL.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            by_id[row["sample_id"]] = row
    return by_id


def parse_section_ids(text: str, start_heading: str, end_heading: str) -> list[str]:
    """Pull sample_ids from a markdown table section bounded by headings."""
    m = re.search(rf"{re.escape(start_heading)}.*?{re.escape(end_heading)}", text, re.DOTALL)
    if not m:
        raise RuntimeError(f"section not found: {start_heading} → {end_heading}")
    block = m.group(0)
    ids: list[str] = []
    seen: set[str] = set()
    # Pattern: | <idx> | <emoji> | `<sample_id>` | ...
    for row_m in re.finditer(r"\|\s*\d+\s*\|\s*\S+\s*\|\s*`([^`]+)`", block):
        sid = row_m.group(1).strip()
        if sid not in seen:
            seen.add(sid)
            ids.append(sid)
    return ids


def normalize_bucket(stm_type: str) -> str:
    """Path-2 used buckets like 'HSM-layered', 'EFSM-interlock', 'FSM-basic'.
    Path-1 doesn't enforce sub-bucket labels; use bare type for now.
    """
    return stm_type or "?"


def main() -> None:
    cands = load_candidates()
    domain_emoji = json.loads(DOMAIN_EMOJI.read_text(encoding="utf-8"))
    text = REPORT_MD.read_text(encoding="utf-8")

    cand_ids = parse_section_ids(text, "## 候选池 — Top 15", "## 备选池 — Backup 15")
    backup_ids = parse_section_ids(text, "## 备选池 — Backup 15", "## 全量评审表")

    assert len(cand_ids) == 15, f"expected 15 candidates, got {len(cand_ids)}: {cand_ids}"
    assert len(backup_ids) == 15, f"expected 15 backups, got {len(backup_ids)}: {backup_ids}"

    def normalize_type(s: str) -> str:
        for k in ("HSM", "EFSM", "FSM"):
            if k in (s or ""):
                return k
        return "Other"

    # selection.json (manifest)
    sel = {"candidates": [], "backup": []}
    for sid in cand_ids:
        c = cands[sid]
        sel["candidates"].append({
            "id": sid,
            "bucket": normalize_type(c["entry_meta"].get("stm_type") or c["file_meta"].get("stm_type", "")),
            "domain": domain_emoji.get(c["paper_slug"], "❓"),
            "paper_slug": c["paper_slug"],
            "case_name": c["entry_title"],
        })
    for sid in backup_ids:
        c = cands[sid]
        sel["backup"].append({
            "id": sid,
            "bucket": normalize_type(c["entry_meta"].get("stm_type") or c["file_meta"].get("stm_type", "")),
            "domain": domain_emoji.get(c["paper_slug"], "❓"),
            "paper_slug": c["paper_slug"],
            "case_name": c["entry_title"],
        })
    SELECTION_JSON.write_text(json.dumps(sel, ensure_ascii=False, indent=2), encoding="utf-8")

    # pool.tsv — 9 cols matching run_expand.sh
    lines = ["id\tbucket\tslug\tcasename\tstm_path\tpdf_path\ttxt_path\tpaper_num\tdomain"]
    for sid in cand_ids + backup_ids:
        c = cands[sid]
        bucket = normalize_type(c["entry_meta"].get("stm_type") or c["file_meta"].get("stm_type", ""))
        slug = c["paper_slug"]
        casename = c["entry_title"].replace("\t", " ")
        stm_path = c["stm_md_path"]
        pdf_path = c.get("paper_pdf_path") or ""
        txt_path = c.get("paper_txt_path") or ""
        paper_num = ""  # PATH1 doesn't use the numeric paper_num convention
        domain = domain_emoji.get(slug, "❓")
        lines.append("\t".join([sid, bucket, slug, casename, stm_path, pdf_path, txt_path, paper_num, domain]))
    POOL_TSV.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"[build_pool] wrote {POOL_TSV.relative_to(REPO_ROOT)}  ({len(cand_ids)+len(backup_ids)} rows)")
    print(f"[build_pool] wrote {SELECTION_JSON.relative_to(REPO_ROOT)}  ({len(cand_ids)} candidates + {len(backup_ids)} backup)")


if __name__ == "__main__":
    main()
