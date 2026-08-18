#!/usr/bin/env python3
"""Build sources_path2.parquet from selection.json + expansions/.

PATH2 §3.3 schema:
  - case_id: str  (paper_slug)
  - source_dir: str  (sources/<slug>/)
  - nl_text: str  (expanded_nl with [En] markers stripped; clean NL only)
  - stm_md_path: str  (sources/<slug>/STM.md)
  - bucket: str  ("FSM-basic" | "EFSM-interlock" | "HSM-layered")
  - rating: str  ("🟢")
  - time_level: str  ("T0")
  - meta: dict  ({domain, paper_num, scale, axis_scores, ...})

Only candidates (15) are written to the main parquet for sprint;
backup pool is written separately for reference.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
SELECTION = ROOT / "selection.json"
EXPANSIONS = ROOT / "expansions"
RESULTS = ROOT / "results"
OUT_MAIN = ROOT.parent / "sources_path2.parquet"
OUT_BACKUP = ROOT.parent / "sources_path2_backup.parquet"


def strip_markers(text: str) -> str:
    """Remove [En] / [E12] inline citation markers; collapse extra whitespace."""
    s = re.sub(r"\s*\[E\d+\]", "", text)
    # Collapse runs of whitespace introduced by marker removal
    s = re.sub(r"\s{2,}", " ", s)
    # Tidy comma/period boundaries
    s = re.sub(r"\s+([,.;:])", r"\1", s)
    return s.strip()


def build_rows(ids: list[str], pool_rows: dict, kind: str) -> list[dict]:
    rows = []
    for cid in ids:
        pr = pool_rows[cid]
        slug = pr["paper_slug"]
        exp_path = EXPANSIONS / f"{cid}.json"
        if not exp_path.exists():
            raise FileNotFoundError(f"expansion missing for {cid}")
        exp = json.loads(exp_path.read_text())

        # Strip markers, validate
        raw = exp["expanded_nl"]
        clean = strip_markers(raw)
        if "[E" in clean:
            raise ValueError(f"{cid}: marker stripping failed, residual: {clean[:200]}")
        wc_after = len(clean.split())
        wc_before = len(raw.split())

        # Pull review result for axis scores + verdict
        rev_path = RESULTS / f"{cid}.json"
        rev = json.loads(rev_path.read_text()) if rev_path.exists() else {}

        meta = {
            "id": cid,
            "domain": pr.get("domain", "?"),
            "paper_num": pr.get("paper_num", ""),
            "case_name": pr["case_name"],
            "scale": exp.get("_meta", {}),
            "review_scale": rev.get("scale", {}),
            "axis_scores": {
                "C1": rev.get("axes", {}).get("C1_dead_end_potential", {}).get("score", "⚪"),
                "C2": rev.get("axes", {}).get("C2_numerical_guard_richness", {}).get("score", "⚪"),
                "C3": rev.get("axes", {}).get("C3_forced_fault_recovery", {}).get("score", "⚪"),
                "C4": rev.get("axes", {}).get("C4_hardware_decoupling", {}).get("score", "⚪"),
            },
            "verdict": rev.get("verdict", "?"),
            "expansion_word_count_with_markers": wc_before,
            "expansion_word_count_clean": wc_after,
            "expansion_provenance_count": len(exp.get("provenance", [])),
            "selection_kind": kind,
        }

        rows.append({
            "case_id": slug,
            "source_dir": f"sources/{slug}/",
            "nl_text": clean,
            "stm_md_path": f"sources/{slug}/STM.md",
            "bucket": pr["bucket"],
            "rating": "🟢",
            "time_level": "T0",
            "meta": meta,
        })
    return rows


def main():
    manifest = json.loads(SELECTION.read_text())
    # pool ids -> pool row
    import csv
    pool_rows = {}
    with open(ROOT / "pool.tsv") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pool_rows[row["id"]] = row

    cand_ids = [r["id"] for r in manifest["candidates"]]
    back_ids = [r["id"] for r in manifest["backup"]]

    cand_rows = build_rows(cand_ids, pool_rows, "candidate")
    back_rows = build_rows(back_ids, pool_rows, "backup")

    df_main = pd.DataFrame(cand_rows)
    df_back = pd.DataFrame(back_rows)

    OUT_MAIN.parent.mkdir(parents=True, exist_ok=True)
    df_main.to_parquet(OUT_MAIN, index=False)
    df_back.to_parquet(OUT_BACKUP, index=False)

    print(f"Wrote {OUT_MAIN}  ({len(df_main)} rows)")
    print(f"Wrote {OUT_BACKUP}  ({len(df_back)} rows)")
    print()
    print("=== schema ===")
    print(df_main.dtypes)
    print()
    print("=== candidate sample (first row) ===")
    r = cand_rows[0]
    print(f"  case_id      : {r['case_id']}")
    print(f"  bucket       : {r['bucket']}")
    print(f"  rating       : {r['rating']}")
    print(f"  time_level   : {r['time_level']}")
    print(f"  source_dir   : {r['source_dir']}")
    print(f"  stm_md_path  : {r['stm_md_path']}")
    print(f"  nl_text [first 250 chars]: {r['nl_text'][:250]}...")
    print(f"  meta keys    : {list(r['meta'].keys())}")
    print()
    print("=== marker-stripping check ===")
    for r in cand_rows + back_rows:
        if "[E" in r["nl_text"]:
            print(f"  ❌ {r['case_id']}: residual marker found!")
            break
    else:
        print(f"  ✅ 30/30 rows: no [En] marker residue")


if __name__ == "__main__":
    main()
