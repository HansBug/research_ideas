#!/usr/bin/env python3
"""Materialize already-discovered open PDFs for the A2a corpus.

This script does not bypass paywalls and does not scrape publisher pages.  It only
uses repository-local PDFs that already exist or downloads explicit open-access
PDF URLs recorded in the frozen candidate snapshot, then regenerates
``paper_content.txt`` using the repository PDF extractor.  Absolute local paths
from earlier audit snapshots are audit-only and are never copied by default.
Failures remain in ``corpus/manual-download-needed.bib``.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import urllib.request
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
SURVEY = Path(__file__).resolve().parents[1]
TABLES = SURVEY / "corpus" / "tables"
RAW = SURVEY / "corpus" / "raw"
PAPERS = SURVEY / "papers"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def bibtex_for(row: pd.Series) -> str:
    cite = str(row.get("cite_key") or row.get("slug"))
    title = str(row.get("title") or "待补")
    year = str(row.get("year") or "待补") if "year" in row else "待补"
    authors = " and ".join(x.strip() for x in str(row.get("authors") or "待补").split(";") if x.strip()) or "待补"
    journal = str(row.get("venue") or "待补")
    doi = str(row.get("doi") or "")
    url = str(row.get("doi_url") or row.get("landing_page_url") or row.get("openalex_url") or "")
    fields = [
        f"  title = {{{title}}}",
        f"  author = {{{authors}}}",
        f"  journal = {{{journal}}}",
        f"  year = {{{year}}}",
    ]
    if doi:
        fields.append(f"  doi = {{{doi}}}")
    if url:
        fields.append(f"  url = {{{url}}}")
    fields.append("  note = {A2a candidate metadata generated from corpus tables; full review not started in A2a}")
    return f"@article{{{cite},\n" + ",\n".join(fields) + "\n}\n"


def load_oa_pdf_urls() -> dict[str, str]:
    path = RAW / "candidates.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path).fillna("")
    urls = {}
    for _, row in df.iterrows():
        doi = str(row.get("doi", "")).lower().strip()
        url = str(row.get("oa_pdf_url_openalex", "")).strip()
        if doi and url:
            urls[doi] = url
    return urls


def try_download_pdf(url: str, dest: Path) -> tuple[bool, str]:
    if not url:
        return False, "no_url"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (A2a corpus PDF acquisition; contact repository owner)"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read(60 * 1024 * 1024)
            ctype = resp.headers.get("content-type", "")
    except Exception as e:  # network/provider failures are recorded, not fatal
        return False, f"download_error:{type(e).__name__}:{e}"
    if not data.startswith(b"%PDF"):
        return False, f"not_pdf:content_type={ctype};prefix={data[:20]!r}"
    dest.write_bytes(data)
    return True, "downloaded_from_oa_pdf_url"


def load_metadata_rows() -> dict[str, pd.Series]:
    rows = {}
    for name in ["core-corpus.csv", "reserve-corpus.csv", "boundary-pool.csv"]:
        path = TABLES / name
        if not path.exists():
            continue
        df = pd.read_csv(path).fillna("")
        for _, row in df.iterrows():
            rows[str(row["slug"])] = row
    return rows


def main() -> None:
    status_path = TABLES / "pdf-status.csv"
    df = pd.read_csv(status_path).fillna("")
    meta_rows = load_metadata_rows()
    oa_pdf_urls = load_oa_pdf_urls()
    copied = 0
    skipped_existing = 0
    failed = []
    for _, row in df.iterrows():
        if row["final_status"] not in {"downloaded", "manual_needed"}:
            continue
        slug = str(row["slug"])
        dest_dir = PAPERS / slug
        pdf_dest = dest_dir / "paper.pdf"
        text_dest = dest_dir / "paper_content.txt"
        meta_row = meta_rows.get(slug)
        # A1 assets already exist and must not be overwritten.
        if pdf_dest.exists() and text_dest.exists():
            skipped_existing += 1
            df.at[_, "final_status"] = "downloaded"
            continue
        dest_dir.mkdir(parents=True, exist_ok=True)
        ok, msg = try_download_pdf(oa_pdf_urls.get(str(row.get("doi", "")).lower().strip(), ""), pdf_dest)
        if not ok:
            # Rows that remain manual-needed are not fatal.  External absolute
            # paths recorded in source_pdf_path are audit-only and deliberately
            # ignored here to keep A2a reproducible in a clean clone.
            if row["final_status"] == "downloaded":
                failed.append((slug, "open_access_download_failed", msg))
            try:
                pdf_dest.unlink()
            except FileNotFoundError:
                pass
            continue
        df.at[_, "final_status"] = "downloaded"
        df.at[_, "failure_type"] = ""
        df.at[_, "manual_priority"] = "--"
        df.at[_, "notes"] = msg
        # Generate bibtex and metadata, but do not create review.md/evidence_chain.md.
        if meta_row is not None:
            (dest_dir / "bibtex.bib").write_text(bibtex_for(meta_row), encoding="utf-8")
            metadata = {
                "slug": slug,
                "title": str(meta_row.get("title", "")),
                "authors": str(meta_row.get("authors", "")),
                "year": str(meta_row.get("year", "")),
                "doi": str(meta_row.get("doi", "")),
                "doi_url": str(meta_row.get("doi_url", "")),
                "journal": str(meta_row.get("venue", "")),
                "ccf_official_category": str(meta_row.get("ccf_category", "")),
                "ccf_official_rank": str(meta_row.get("ccf_rank", "")),
                "review_type": str(meta_row.get("review_kind", "")),
                "a2a_corpus_tier": str(meta_row.get("corpus_tier", "")),
                "a2a_review_status": "not_started",
                "eligible_for_statistical_synthesis": None,
                "source_note": "A2a candidate PDF obtained via OpenAlex/open-access URL recorded in the frozen fulltext-audit snapshot; no A2b deep review yet.",
            }
            (dest_dir / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        cmd = [
            sys.executable,
            "-m",
            "tools.pdf_extractor",
            "-i",
            str(pdf_dest),
            "-o",
            str(text_dest),
            "-m",
            "text",
        ]
        res = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if res.returncode != 0 or not text_dest.exists() or text_dest.stat().st_size == 0:
            failed.append((slug, "text_extraction_failed", res.stderr[-500:]))
        else:
            copied += 1
    # Update pdf-status with actual repo paths and hashes for copied rows.
    for idx, row in df.iterrows():
        slug = str(row["slug"])
        pdf_dest = PAPERS / slug / "paper.pdf"
        text_dest = PAPERS / slug / "paper_content.txt"
        if pdf_dest.exists():
            df.at[idx, "pdf_path"] = str(pdf_dest.relative_to(SURVEY))
            df.at[idx, "pdf_sha256"] = sha256(pdf_dest)
        if text_dest.exists():
            df.at[idx, "text_path"] = str(text_dest.relative_to(SURVEY))
            df.at[idx, "text_extraction_status"] = "ok"
    df.to_csv(status_path, index=False, lineterminator="\n")
    result = {
        "copied_and_extracted": copied,
        "skipped_existing": skipped_existing,
        "failed": failed[:20],
        "failed_count": len(failed),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failed:
        # Do not fail the whole run; failures remain visible for manual handling.
        return


if __name__ == "__main__":
    main()
