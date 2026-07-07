#!/usr/bin/env python3
"""Import user-provided Zotero PDF attachments into the A2a corpus.

This helper is intentionally explicit: it only copies PDF attachments from a
BibTeX export whose entries match current ``manual-download-needed.bib`` rows by
DOI or normalized title.  It never treats the external Zotero path as a stable
fact source; after import, the repository-local ``papers/<slug>/paper.pdf`` and
``paper_content.txt`` are the only downloaded facts.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[4]
SURVEY = Path(__file__).resolve().parents[1]
CORPUS = SURVEY / "corpus"
TABLES = CORPUS / "tables"
PAPERS = SURVEY / "papers"


def norm_doi(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip().lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    return text.strip().rstrip(".")


def norm_title(value: object) -> str:
    if value is None:
        return ""
    text = re.sub(r"[{}]", "", str(value)).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_bib_value(value: object) -> str:
    return re.sub(r"[{}]", "", str(value or "")).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_bib(path: Path) -> List[Dict[str, str]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    entries: List[Dict[str, str]] = []
    i = 0
    n = len(text)
    while True:
        m = re.search(r"@\w+\s*\{", text[i:])
        if not m:
            break
        start = i + m.start()
        brace = text.find("{", start)
        entry_type = text[start + 1 : brace].strip()
        depth = 0
        end = None
        for j in range(brace, n):
            if text[j] == "{":
                depth += 1
            elif text[j] == "}":
                depth -= 1
                if depth == 0:
                    end = j + 1
                    break
        if end is None:
            raise ValueError(f"unclosed BibTeX entry starting at offset {start}")
        body = text[brace + 1 : end - 1]
        key, _, rest = body.partition(",")
        fields: Dict[str, str] = {"entry_type": entry_type, "key": key.strip()}
        k = 0
        while k < len(rest):
            while k < len(rest) and rest[k] in " \n\r\t,":
                k += 1
            fm = re.match(r"([A-Za-z][A-Za-z0-9_\-]*)\s*=\s*", rest[k:])
            if not fm:
                k += 1
                continue
            fname = fm.group(1).lower()
            k += fm.end()
            if k >= len(rest):
                break
            if rest[k] == "{":
                depth = 0
                val_start = k + 1
                for j in range(k, len(rest)):
                    if rest[j] == "{":
                        depth += 1
                    elif rest[j] == "}":
                        depth -= 1
                        if depth == 0:
                            fields[fname] = rest[val_start:j]
                            k = j + 1
                            break
                else:
                    raise ValueError(f"unclosed field {fname} in {path}")
            elif rest[k] == '"':
                val_start = k + 1
                j = k + 1
                while j < len(rest):
                    if rest[j] == '"' and rest[j - 1] != "\\":
                        break
                    j += 1
                fields[fname] = rest[val_start:j]
                k = j + 1
            else:
                j = k
                while j < len(rest) and rest[j] not in ",\n\r":
                    j += 1
                fields[fname] = rest[k:j].strip()
                k = j
        entries.append(fields)
        i = end
    return entries


def zotero_file_paths(file_field: str, export_dir: Path) -> List[Path]:
    paths: List[Path] = []
    if not file_field:
        return paths
    for part in re.split(r";\s*", file_field):
        bits = part.split(":")
        if len(bits) >= 3:
            raw = ":".join(bits[1:-1])
        elif len(bits) == 1:
            raw = bits[0]
        else:
            continue
        if not raw:
            continue
        path = Path(raw)
        if not path.is_absolute():
            path = export_dir / path
        paths.append(path)
    return paths


def load_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bibtex_for(row: Dict[str, str]) -> str:
    cite = row.get("cite_key") or row.get("slug") or "a2a_candidate"
    title = row.get("title") or "待补"
    authors = " and ".join(x.strip() for x in (row.get("authors") or "待补").split(";") if x.strip()) or "待补"
    year = row.get("year") or "待补"
    journal = row.get("venue") or "待补"
    doi = row.get("doi") or ""
    url = row.get("doi_url") or row.get("landing_page_url") or row.get("openalex_url") or ""
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
    fields.append("  note = {A2a candidate metadata generated from corpus tables; PDF imported from user-provided Zotero export; full review not started in A2a}")
    return f"@article{{{cite},\n" + ",\n".join(fields) + "\n}\n"


def metadata_for(row: Dict[str, str], source_bib_key: str, attachment_name: str) -> Dict[str, object]:
    return {
        "slug": row.get("slug", ""),
        "title": row.get("title", ""),
        "authors": row.get("authors", ""),
        "year": row.get("year", ""),
        "doi": row.get("doi", ""),
        "doi_url": row.get("doi_url", ""),
        "journal": row.get("venue", ""),
        "ccf_official_category": row.get("ccf_category", ""),
        "ccf_official_rank": row.get("ccf_rank", ""),
        "review_type": row.get("review_kind", ""),
        "a2a_corpus_tier": row.get("corpus_tier", ""),
        "a2a_pdf_source": "user_zotero_export",
        "a2a_zotero_bib_key": source_bib_key,
        "a2a_zotero_attachment_name": attachment_name,
        "a2a_review_status": "not_started",
        "eligible_for_statistical_synthesis": None,
        "source_note": "A2a PDF imported from user-provided Zotero BibTeX export after matching current manual-download-needed rows by DOI/title; no A2b deep review yet.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zotero-bib", required=True, type=Path, help="Zotero-exported .bib with file fields")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--retry-failures", action="store_true", help="Retry slugs already listed in the Zotero failure manifest")
    args = parser.parse_args()

    zotero_bib = args.zotero_bib.resolve()
    export_dir = zotero_bib.parent
    entries = parse_bib(zotero_bib)
    by_doi = {norm_doi(e.get("doi") or e.get("url")): e for e in entries if norm_doi(e.get("doi") or e.get("url"))}
    by_title = {norm_title(e.get("title")): e for e in entries if norm_title(e.get("title"))}

    corpus_rows = load_rows(TABLES / "core-corpus.csv") + load_rows(TABLES / "reserve-corpus.csv")
    manual_rows = load_rows(TABLES / "pdf-status.csv")
    manual_slugs = {r["slug"] for r in manual_rows if r.get("corpus_tier") in {"core", "reserve"} and r.get("final_status") == "manual_needed"}
    corpus_by_slug = {r["slug"]: r for r in corpus_rows}

    imported = []
    skipped_existing = []
    no_attachment = []
    unmatched = []
    extraction_failed = []
    known_failure_skipped = []
    existing_failure_manifest = CORPUS / "raw" / "zotero-import-failed-2026-07-07.csv"
    known_failed_slugs = set()
    if existing_failure_manifest.exists() and not args.retry_failures:
        with existing_failure_manifest.open(newline="", encoding="utf-8") as f:
            known_failed_slugs = {row.get("slug", "") for row in csv.DictReader(f) if row.get("slug", "")}

    for slug in sorted(manual_slugs):
        if slug in known_failed_slugs:
            known_failure_skipped.append(slug)
            continue
        row = corpus_by_slug[slug]
        doi = norm_doi(row.get("doi"))
        title = norm_title(row.get("title"))
        entry = by_doi.get(doi) if doi else None
        matched_by = "doi"
        if entry is None and title:
            entry = by_title.get(title)
            matched_by = "title"
        if entry is None:
            unmatched.append(slug)
            continue
        attachments = [p for p in zotero_file_paths(entry.get("file", ""), export_dir) if p.exists() and p.suffix.lower() == ".pdf"]
        if not attachments:
            no_attachment.append(slug)
            continue
        source_pdf = attachments[0]
        paper_dir = PAPERS / slug
        paper_dir.mkdir(parents=True, exist_ok=True)
        pdf_dest = paper_dir / "paper.pdf"
        text_dest = paper_dir / "paper_content.txt"
        import_status = "new_import"
        if pdf_dest.exists() and text_dest.exists():
            skipped_existing.append(slug)
            import_status = "already_present"
        elif not args.dry_run:
            shutil.copy2(source_pdf, pdf_dest)
            (paper_dir / "bibtex.bib").write_text(bibtex_for(row), encoding="utf-8")
            (paper_dir / "metadata.json").write_text(
                json.dumps(metadata_for(row, entry.get("key", ""), source_pdf.name), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            cmd = [sys.executable, "-m", "tools.pdf_extractor", "-i", str(pdf_dest), "-o", str(text_dest), "-m", "text"]
            res = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
            if res.returncode != 0 or not text_dest.exists() or text_dest.stat().st_size == 0:
                extraction_failed.append({"slug": slug, "stderr": res.stderr[-500:], "stdout": res.stdout[-500:]})
                # A2a 的 downloaded 必须同时具备仓库内 PDF 与可检索正文。
                # 如果文本提取失败，清理本轮半成品，让该条继续留在人工下载清单中。
                for path in [pdf_dest, text_dest, paper_dir / "bibtex.bib", paper_dir / "metadata.json"]:
                    try:
                        path.unlink()
                    except FileNotFoundError:
                        pass
                continue
        imported.append(
            {
                "slug": slug,
                "corpus_id": row.get("corpus_id", ""),
                "corpus_tier": row.get("corpus_tier", ""),
                "manual_priority": "P0" if row.get("corpus_tier") == "core" and row.get("ccf_rank") == "CCF-A" else ("P1" if row.get("corpus_tier") == "core" else "P2"),
                "matched_by": matched_by,
                "source_bib_key": entry.get("key", ""),
                "title": row.get("title", ""),
                "source_attachment_name": source_pdf.name,
                "pdf_sha256": sha256(source_pdf),
                "import_status": import_status,
            }
        )

    manifest_path = CORPUS / "raw" / "zotero-import-2026-07-07.csv"
    failure_manifest_path = CORPUS / "raw" / "zotero-import-failed-2026-07-07.csv"
    if imported and not args.dry_run:
        fieldnames = ["slug", "corpus_id", "corpus_tier", "manual_priority", "matched_by", "source_bib_key", "title", "source_attachment_name", "pdf_sha256", "import_status"]
        with manifest_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            writer.writerows(imported)
    if extraction_failed and not args.dry_run:
        fieldnames = ["slug", "error", "stdout_tail", "stderr_tail"]
        with failure_manifest_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for item in extraction_failed:
                writer.writerow({
                    "slug": item.get("slug", ""),
                    "error": "text_extraction_failed",
                    "stdout_tail": item.get("stdout", ""),
                    "stderr_tail": item.get("stderr", ""),
                })

    result = {
        "zotero_entries": len(entries),
        "manual_slugs_before_import": len(manual_slugs),
        "imported_or_importable": len(imported),
        "skipped_existing": len(skipped_existing),
        "no_attachment": len(no_attachment),
        "unmatched": len(unmatched),
        "known_failure_skipped": len(known_failure_skipped),
        "extraction_failed_count": len(extraction_failed),
        "manifest": str(manifest_path.relative_to(SURVEY)) if imported else "",
        "failure_manifest": str(failure_manifest_path.relative_to(SURVEY)) if extraction_failed else "",
        "dry_run": args.dry_run,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if extraction_failed:
        print(json.dumps({"extraction_failed": extraction_failed[:20]}, ensure_ascii=False, indent=2))
        sys.exit(2)


if __name__ == "__main__":
    main()
