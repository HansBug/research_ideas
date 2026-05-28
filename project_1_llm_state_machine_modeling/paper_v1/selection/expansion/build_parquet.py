"""Build sources_path1.parquet + sources_path1_backup.parquet from selection.json + expansions/.

PATH1 §3.3 schema (PATH1_HARD_COMPARISON_GUIDE.md):
  - case_id        : str   # sample_id (e.g. abs-fsm-brake-control__01)
  - paper_slug     : str   # sources/<slug>/
  - source_dir     : str   # sources/<slug>/ (path-2 convention)
  - nl_text        : str   # expanded_nl with [En] markers stripped; clean NL only
  - stm_md_path    : str   # sources/<slug>/STM.md
  - stm_type       : str   # HSM / EFSM / FSM (path-1 bucket)
  - rating         : str   # "🟢"
  - time_level     : str   # "T0"
  - meta           : dict  # {domain, entry_idx, case_name, axis_scores, ..., axis_coverage_supported}

Only candidates (15) are written to the main parquet for sprint;
backup pool is written separately for reference / fallback.

Marker-stripping: every `[En]` / `[E12]` is removed; surrounding spaces / punctuation
are tidied. Validate 0 residue before writing.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

import pandas as pd

EXP_DIR = Path(__file__).resolve().parent
SEL_ROOT = EXP_DIR.parent
# EXP_DIR.parents = [selection, paper_v1, project_1_llm_state_machine_modeling, research_ideas, ...]
REPO_ROOT = EXP_DIR.parents[3]

SELECTION = EXP_DIR / "selection.json"
POOL_TSV = EXP_DIR / "pool.tsv"
EXPANSIONS = EXP_DIR / "expansions"
REVIEWS = SEL_ROOT / "reviews"  # paper_v1/selection/reviews/<sample_id>.json

EVAL_DATA = REPO_ROOT / "project_1_llm_state_machine_modeling" / "eval" / "data"
OUT_MAIN = EVAL_DATA / "sources_path1.parquet"
OUT_BACKUP = EVAL_DATA / "sources_path1_backup.parquet"


AXIS_KEYS = ["H_hierarchical", "G_guards_arith", "A_actions_nontrivial",
             "F_fault_recovery", "bd_baseline_traps", "ft_fcstm_fit"]
NOT_SUPPORTED_KEYWORDS = ("未提供", "原文不支持", "原文无", "覆盖弱", "适用面窄", "不支持")


def strip_markers(text: str) -> str:
    """Remove [En] inline citation markers; tidy whitespace + punctuation boundaries."""
    s = re.sub(r"\s*\[E\d+\]", "", text)
    s = re.sub(r"\s{2,}", " ", s)
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    return s.strip()


def is_axis_supported(text: str) -> bool:
    return not any(kw in (text or "") for kw in NOT_SUPPORTED_KEYWORDS)


def build_rows(ids: list[str], pool_rows: dict, kind: str) -> list[dict]:
    rows: list[dict] = []
    for cid in ids:
        pr = pool_rows[cid]
        slug = pr["slug"]
        exp_path = EXPANSIONS / f"{cid}.json"
        if not exp_path.exists():
            raise FileNotFoundError(f"expansion missing for {cid}")
        exp = json.loads(exp_path.read_text(encoding="utf-8"))

        raw = exp["expanded_nl"]
        clean = strip_markers(raw)
        if "[E" in clean:
            raise ValueError(f"{cid}: marker stripping failed, residual: {clean[:200]}")
        wc_after = len(clean.split())
        wc_before = len(raw.split())

        # Pull review for selection scores (path-1 H/G/A/F + bd_final + ft + bd_raw)
        rev_path = REVIEWS / f"{cid}.json"
        rev = json.loads(rev_path.read_text(encoding="utf-8")) if rev_path.exists() else {}
        scores = rev.get("scores", {}) or {}
        def score(k: str) -> int:
            try:
                return int(scores.get(k, {}).get("score", 0))
            except Exception:
                return 0

        # Re-compute bd_final post-hoc (T2/T4/T5/T6, T6 auto-uplift to 3) — matches aggregate.py
        traps = rev.get("bd_trap_signals", {}) or {}
        def trap_on(prefix: str) -> bool:
            for k in traps:
                if k.startswith(prefix + "_"):
                    return bool((traps.get(k) or {}).get("present"))
            return False
        t2, t4, t5, t6 = trap_on("T2"), trap_on("T4"), trap_on("T5"), trap_on("T6")
        bd_content = sum([t2, t4, t5, t6])
        if t6:
            bd_final = 3
        elif bd_content >= 3:
            bd_final = 3
        else:
            bd_final = bd_content

        ax = exp.get("axis_coverage", {}) or {}
        axis_supported = {k: is_axis_supported(ax.get(k, "")) for k in AXIS_KEYS}

        # Parse entry_idx from sample_id <slug>__<NN>
        entry_idx = None
        m = re.match(r".+__(\d+)$", cid)
        if m:
            entry_idx = int(m.group(1))

        meta = {
            "sample_id": cid,
            "domain": pr.get("domain", "?"),
            "entry_idx": entry_idx,
            "case_name": pr.get("casename", ""),
            "selection_scores": {
                "H": score("H_hierarchical"),
                "G": score("G_guards_arith"),
                "A": score("A_actions_nontrivial"),
                "F": score("F_fault_recovery"),
                "bd_final": bd_final,
                "bd_raw_codex": int(rev.get("baseline_difficulty", 0) or 0),
                "ft": int(rev.get("fcstm_fit", 0) or 0),
            },
            "selection_verdict": rev.get("verdict", "?"),
            "expansion_word_count_with_markers": wc_before,
            "expansion_word_count_clean": wc_after,
            "expansion_marker_count": len(re.findall(r"\[E\d+\]", raw)),
            "expansion_provenance_count": len(exp.get("provenance", [])),
            "axis_coverage_supported": axis_supported,
            "selection_kind": kind,
        }

        rows.append({
            "case_id": cid,
            "paper_slug": slug,
            "source_dir": f"sources/{slug}/",
            "nl_text": clean,
            "stm_md_path": f"sources/{slug}/STM.md",
            "stm_type": pr.get("bucket", "?"),
            "rating": "🟢",
            "time_level": "T0",
            "meta": meta,
        })
    return rows


def main() -> None:
    manifest = json.loads(SELECTION.read_text(encoding="utf-8"))
    pool_rows: dict[str, dict] = {}
    with POOL_TSV.open("r", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pool_rows[row["id"]] = row

    cand_ids = [r["id"] for r in manifest["candidates"]]
    back_ids = [r["id"] for r in manifest["backup"]]

    cand_rows = build_rows(cand_ids, pool_rows, "candidate")
    back_rows = build_rows(back_ids, pool_rows, "backup")

    df_main = pd.DataFrame(cand_rows)
    df_back = pd.DataFrame(back_rows)

    EVAL_DATA.mkdir(parents=True, exist_ok=True)
    df_main.to_parquet(OUT_MAIN, index=False)
    df_back.to_parquet(OUT_BACKUP, index=False)

    print(f"wrote {OUT_MAIN.relative_to(REPO_ROOT)}  ({len(df_main)} rows)")
    print(f"wrote {OUT_BACKUP.relative_to(REPO_ROOT)}  ({len(df_back)} rows)")
    print()
    print("=== schema ===")
    print(df_main.dtypes)
    print()
    print("=== candidate first row ===")
    r = cand_rows[0]
    print(f"  case_id      : {r['case_id']}")
    print(f"  paper_slug   : {r['paper_slug']}")
    print(f"  stm_type     : {r['stm_type']}")
    print(f"  rating/time  : {r['rating']}/{r['time_level']}")
    print(f"  nl_text [first 200]: {r['nl_text'][:200]}...")
    print(f"  meta keys    : {list(r['meta'].keys())}")
    print(f"  selection_scores: {r['meta']['selection_scores']}")
    print(f"  axis supported: {r['meta']['axis_coverage_supported']}")
    print()
    print("=== marker residue check ===")
    bad = [r["case_id"] for r in cand_rows + back_rows if "[E" in r["nl_text"]]
    if bad:
        print(f"  ❌ residual markers in: {bad}")
    else:
        print(f"  ✅ {len(cand_rows)+len(back_rows)}/{len(cand_rows)+len(back_rows)} rows: no [En] marker residue")


if __name__ == "__main__":
    main()
