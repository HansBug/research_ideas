#!/usr/bin/env python3
"""Validate the A2a survey corpus contract."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd

SURVEY = Path(__file__).resolve().parents[1]
CORPUS = SURVEY / "corpus"
TABLES = CORPUS / "tables"
PAPERS = SURVEY / "papers"

REQUIRED_DOCS = [
    CORPUS / "README.md",
    CORPUS / "selection.md",
    CORPUS / "source-audit.md",
    CORPUS / "pdf-acquisition.md",
    CORPUS / "handoff-to-next-stage.md",
    CORPUS / "manual-download-needed.bib",
    CORPUS / "manual-download-needed.md",
]
REQUIRED_TABLES = [
    TABLES / "full-candidate-ledger.csv",
    TABLES / "systematic-candidates.csv",
    TABLES / "core-corpus.csv",
    TABLES / "reserve-corpus.csv",
    TABLES / "boundary-pool.csv",
    TABLES / "pdf-status.csv",
]
REQUIRED_RAW = [
    CORPUS / "raw" / "candidates.csv",
    CORPUS / "raw" / "fulltext-audit.csv",
    CORPUS / "raw" / "selection-seed.csv",
]


def fail(msg: str) -> None:
    raise AssertionError(msg)


def keyset(df: pd.DataFrame) -> set[str]:
    keys = set()
    for _, row in df.fillna("").iterrows():
        key = str(row.get("normalized_doi") or row.get("normalized_title") or row.get("slug"))
        if key:
            keys.add(key)
    return keys


def main() -> None:
    for path in REQUIRED_DOCS + REQUIRED_TABLES + REQUIRED_RAW:
        if not path.exists():
            fail(f"missing required file: {path}")

    selection_seed = pd.read_csv(CORPUS / "raw" / "selection-seed.csv").fillna("")
    if len(selection_seed) != 100:
        fail(f"selection seed expected 100 rows, got {len(selection_seed)}")
    if (selection_seed["doi"].astype(str).str.len() == 0).any():
        fail("selection seed contains rows without DOI")

    full = pd.read_csv(TABLES / "full-candidate-ledger.csv").fillna("")
    systematic = pd.read_csv(TABLES / "systematic-candidates.csv").fillna("")
    core = pd.read_csv(TABLES / "core-corpus.csv").fillna("")
    reserve = pd.read_csv(TABLES / "reserve-corpus.csv").fillna("")
    boundary = pd.read_csv(TABLES / "boundary-pool.csv").fillna("")
    pdf = pd.read_csv(TABLES / "pdf-status.csv").fillna("")

    if len(full) != 438:
        fail(f"full candidate ledger expected 438 rows, got {len(full)}")
    if len(systematic) != 293:
        fail(f"systematic candidate pool expected 293 rows, got {len(systematic)}")
    if len(core) != 120:
        fail(f"core corpus expected 120 rows, got {len(core)}")
    if len(reserve) != 40:
        fail(f"reserve corpus expected 40 rows, got {len(reserve)}")
    if len(boundary) != 145:
        fail(f"boundary pool expected 145 rows, got {len(boundary)}")

    core_keys, reserve_keys, boundary_keys = keyset(core), keyset(reserve), keyset(boundary)
    if core_keys & reserve_keys:
        fail("core and reserve are not mutually exclusive")
    if core_keys & boundary_keys:
        fail("core and boundary are not mutually exclusive")
    if reserve_keys & boundary_keys:
        fail("reserve and boundary are not mutually exclusive")

    required_core_cols = {"selection_reason", "slug", "title", "doi", "review_kind", "corpus_tier"}
    if not required_core_cols.issubset(core.columns):
        fail(f"core missing columns: {required_core_cols - set(core.columns)}")
    if (core["selection_reason"].astype(str).str.len() == 0).any():
        fail("some core rows lack selection_reason")
    if (reserve["reserve_reason"].astype(str).str.len() == 0).any():
        fail("some reserve rows lack reserve_reason")
    if len(boundary) and (boundary["boundary_reason"].astype(str).str.len() == 0).any():
        fail("some boundary rows lack boundary_reason")

    a1_core = core[core["already_a1_inpool"].astype(str).str.lower() == "true"]
    if len(a1_core) != 13:
        fail(f"expected 13 A1 in-pool rows in core, got {len(a1_core)}")
    for slug in a1_core["slug"]:
        paper_dir = PAPERS / slug
        for name in ["review.md", "evidence_chain.md", "paper.pdf", "paper_content.txt", "bibtex.bib", "metadata.json"]:
            if not (paper_dir / name).exists():
                fail(f"A1 core row {slug} missing protected asset {name}")

    core_reserve_slugs = set(core["slug"]) | set(reserve["slug"])
    pdf_core_reserve = pdf[pdf["corpus_tier"].isin(["core", "reserve"])]
    if set(pdf_core_reserve["slug"]) != core_reserve_slugs:
        fail("pdf-status does not exactly cover core+reserve slugs")
    if (pdf_core_reserve["attempted"].astype(str).str.len() == 0).any():
        fail("some core/reserve pdf-status rows lack attempted")
    if not set(pdf_core_reserve["final_status"]).issubset({"downloaded", "manual_needed"}):
        fail("core/reserve final_status contains unsupported values")

    manual_rows = pdf_core_reserve[pdf_core_reserve["final_status"] == "manual_needed"]
    bib_text = (CORPUS / "manual-download-needed.bib").read_text(encoding="utf-8")
    bib_entries = len(re.findall(r"^@", bib_text, flags=re.M))
    if bib_entries != len(manual_rows):
        fail(f"manual bib entries {bib_entries} != manual_needed rows {len(manual_rows)}")

    for _, row in pdf_core_reserve[pdf_core_reserve["final_status"] == "downloaded"].iterrows():
        pdf_path = SURVEY / str(row["pdf_path"])
        text_path = SURVEY / str(row["text_path"])
        if not pdf_path.exists():
            fail(f"downloaded row missing pdf file: {row['slug']} -> {pdf_path}")
        if not text_path.exists():
            fail(f"downloaded row missing text file: {row['slug']} -> {text_path}")
        # New A2a directories must not pretend to have completed review/evidence chain.
        if str(row["slug"]) not in set(a1_core["slug"]):
            if (PAPERS / str(row["slug"]) / "review.md").exists():
                fail(f"A2a new downloaded row unexpectedly has review.md: {row['slug']}")
            if (PAPERS / str(row["slug"]) / "evidence_chain.md").exists():
                fail(f"A2a new downloaded row unexpectedly has evidence_chain.md: {row['slug']}")

    result = {
        "status": "passed",
        "full_candidate_ledger": len(full),
        "systematic_candidates": len(systematic),
        "core": len(core),
        "reserve": len(reserve),
        "boundary": len(boundary),
        "manual_needed_core_reserve": len(manual_rows),
        "downloaded_core_reserve": int((pdf_core_reserve["final_status"] == "downloaded").sum()),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(json.dumps({"status": "failed", "error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)
