#!/usr/bin/env python3
"""Build A2a survey-of-surveys corpus tables.

The script is deterministic and intentionally conservative: it builds a candidate
corpus from the frozen raw CSV snapshots under ``corpus/raw/`` and the already
reviewed A1 paper metadata.  It does not download PDFs and does not create
``review.md`` files.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "corpus"
RAW = CORPUS / "raw"
TABLES = CORPUS / "tables"
PAPERS = ROOT / "papers"

CORE_TARGET = 120
RESERVE_TARGET = 40


def norm_text(value: object) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""
    return str(value).strip()


def norm_doi(value: object) -> str:
    text = norm_text(value).lower()
    text = re.sub(r"^https?://(dx\.)?doi\.org/", "", text)
    return text.strip().rstrip(".")


def norm_title(value: object) -> str:
    text = norm_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def slugify(title: str, fallback: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not base:
        base = fallback.lower()
    words = [w for w in base.split("-") if w]
    return "-".join(words[:9])[:90].strip("-") or fallback.lower()


def cite_key_from(title: str, year: str, authors: str = "") -> str:
    first_author = "survey"
    if authors:
        first_author = re.split(r";|,| and ", authors)[0].strip().split()[-1].lower()
        first_author = re.sub(r"[^a-z0-9]", "", first_author) or "survey"
    words = re.findall(r"[A-Za-z0-9]+", title.lower())[:4]
    return f"{first_author}{year or 'na'}{'_'.join(words)}"[:80]


def review_kind(row: pd.Series) -> str:
    title = norm_text(row.get("title_en"))
    auto = norm_text(row.get("auto_type_issue_table"))
    hay = f"{title} {auto}".lower()
    if "multivocal" in hay or "多声" in auto:
        return "MLR"
    if "tertiary" in hay or "review of reviews" in hay or "三级" in auto:
        return "tertiary"
    if "mapping" in hay or "映射" in auto:
        return "SMS"
    if "systematic" in hay or "系统综述" in auto:
        return "SLR"
    if any(x in hay for x in ["roadmap", "vision", "taxonomy", "agenda"]):
        return "boundary"
    if "review" in hay or "survey" in hay or "综述" in auto:
        return "review_candidate"
    return "other"


def is_systematic(row: pd.Series) -> bool:
    kind = review_kind(row)
    title = norm_text(row.get("title_en")).lower()
    auto = norm_text(row.get("auto_type_issue_table"))
    explicit = any(
        token in title
        for token in [
            "systematic",
            "systematic literature review",
            "systematic mapping",
            "mapping study",
            "mapping studies",
            "multivocal",
            "tertiary",
            "review of reviews",
        ]
    )
    auto_explicit = any(token in auto for token in ["系统综述", "系统映射"])
    return kind in {"SLR", "SMS", "MLR", "tertiary"} or explicit or auto_explicit


def is_boundary(row: pd.Series) -> bool:
    auto = norm_text(row.get("auto_type_issue_table")).lower()
    title = norm_text(row.get("title_en")).lower()
    return any(token in auto for token in ["taxonomy", "roadmap", "边界", "愿景"]) or any(
        token in title for token in ["roadmap", "vision", "agenda", "taxonomy", "challenges"]
    ) and not is_systematic(row)


def topic_tags(title: str, abstract: str) -> str:
    hay = f"{title} {abstract}".lower()
    tags = []
    patterns = [
        ("AI/LLM/agent", ["large language model", "llm", "generative ai", "agent", "artificial intelligence", "machine learning"]),
        ("测试/质量/验证", ["test", "testing", "quality", "verification", "validation", "vulnerability", "security", "safety"]),
        ("需求/人因/生产力", ["requirement", "developer", "productivity", "human", "education", "user"]),
        ("模型/架构/DevOps", ["model", "modeling", "architecture", "devops", "technical debt", "maintenance"]),
        ("证据/复现/工件", ["artifact", "replication", "dataset", "repository", "evidence", "empirical"]),
    ]
    for label, keys in patterns:
        if any(k in hay for k in keys):
            tags.append(label)
    return ";".join(tags) or "通用SE综述"


def load_a1_records() -> List[Dict[str, str]]:
    records: List[Dict[str, str]] = []
    for meta_path in sorted(PAPERS.glob("*/metadata.json")):
        data = json.loads(meta_path.read_text(encoding="utf-8"))
        if not data.get("eligible_for_statistical_synthesis"):
            continue
        slug = data.get("slug") or meta_path.parent.name
        title = data.get("title") or slug
        year = str(data.get("year") or "")
        doi = norm_doi(data.get("doi"))
        records.append(
            {
                "source_layer": "A1已精核入池候选",
                "corpus_tier": "core",
                "slug": slug,
                "cite_key": cite_key_from(title, year, data.get("authors", "")),
                "title": title,
                "year": year,
                "publication_date": norm_text(data.get("publication_date")),
                "authors": norm_text(data.get("authors")),
                "venue": norm_text(data.get("journal")),
                "venue_short": norm_text(data.get("venue_short_link")),
                "ccf_rank": (lambda r: f"CCF-{r}" if r in {"A", "B", "C"} else r)(norm_text(data.get("ccf_official_rank") or data.get("ccf_rank"))),
                "ccf_category": norm_text(data.get("ccf_official_category") or data.get("ccf_category")),
                "review_kind": norm_text(data.get("review_type")) or "A1入池样本",
                "topic_tags": norm_text(data.get("se_subfield")) or "A1入池样本",
                "doi": doi,
                "doi_url": f"https://doi.org/{doi}" if doi else "",
                "landing_page_url": norm_text(data.get("doi_url") or data.get("pdf_url")),
                "openalex_url": norm_text(data.get("openalex_url")),
                "oa_status": norm_text(data.get("oa_status")),
                "ref_count": "",
                "selection_reason": "A1 已完成全文文本级 review/evidence_chain，且 eligible_for_statistical_synthesis=true；默认纳入 A2a 主候选并保护既有证据链。",
                "reserve_reason": "",
                "boundary_reason": "",
                "already_a1_inpool": "true",
                "normalized_doi": doi,
                "normalized_title": norm_title(title),
            }
        )
    return records


def candidate_to_record(row: pd.Series, tier: str, reason: str) -> Dict[str, str]:
    title = norm_text(row.get("title_en") or row.get("title_issue_table"))
    year = norm_text(row.get("publication_year_metadata") or row.get("year_issue_table"))
    doi = norm_doi(row.get("doi"))
    slug = slugify(title, f"candidate-{row.name}")
    boundary_reason = ""
    reserve_reason = ""
    selection_reason = ""
    if tier == "core":
        selection_reason = reason
    elif tier == "reserve":
        reserve_reason = reason
    elif tier == "boundary":
        boundary_reason = reason
    return {
        "source_layer": "issue95候选快照",
        "corpus_tier": tier,
        "slug": slug,
        "cite_key": cite_key_from(title, year, norm_text(row.get("authors_metadata"))),
        "title": title,
        "year": year,
        "publication_date": norm_text(row.get("publication_date_metadata")),
        "authors": norm_text(row.get("authors_metadata")),
        "venue": norm_text(row.get("journal_metadata") or row.get("journal_issue_table")),
        "venue_short": norm_text(row.get("journal_issue_table")),
        "ccf_rank": norm_text(row.get("ccf_rank")),
        "ccf_category": "软件工程 / 系统软件 / 程序设计语言（工作口径；正式写作前需按 CCF 官方复核）",
        "review_kind": review_kind(row),
        "topic_tags": topic_tags(title, norm_text(row.get("abstract_en_metadata"))),
        "doi": doi,
        "doi_url": norm_text(row.get("doi_url")) or (f"https://doi.org/{doi}" if doi else ""),
        "landing_page_url": norm_text(row.get("landing_page_url")),
        "openalex_url": norm_text(row.get("openalex_url")),
        "oa_status": norm_text(row.get("oa_status_openalex")),
        "ref_count": norm_text(row.get("ref_count_metadata")),
        "selection_reason": selection_reason,
        "reserve_reason": reserve_reason,
        "boundary_reason": boundary_reason,
        "already_a1_inpool": "false",
        "normalized_doi": doi,
        "normalized_title": norm_title(title),
    }


def sort_key(row: pd.Series) -> tuple:
    rank_weight = {"CCF-A": 0, "CCF-B": 1, "CCF-C": 2}.get(norm_text(row.get("ccf_rank")), 9)
    year = int(float(row.get("publication_year_metadata") or row.get("year_issue_table") or 0))
    refs = int(float(row.get("ref_count_metadata") or 0))
    ok = 0 if norm_text(row.get("download_status")) in {"ok", "exists_old"} else 1
    return (rank_weight, -year, ok, -refs, norm_title(row.get("title_en")))


def write_csv(path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    TABLES.mkdir(parents=True, exist_ok=True)
    candidates = pd.read_csv(RAW / "candidates.csv")
    audit = pd.read_csv(RAW / "fulltext-audit.csv")
    zotero_failed_path = RAW / "zotero-import-failed-2026-07-07.csv"
    zotero_failed = {}
    if zotero_failed_path.exists():
        failed_df = pd.read_csv(zotero_failed_path).fillna("")
        zotero_failed = {str(row.get("slug", "")): row for _, row in failed_df.iterrows() if str(row.get("slug", ""))}
    audit["normalized_doi"] = audit["doi"].map(norm_doi)
    audit_map = {row["normalized_doi"]: row for _, row in audit.iterrows() if row["normalized_doi"]}

    candidates["normalized_doi"] = candidates["doi"].map(norm_doi)
    candidates["normalized_title"] = candidates["title_en"].map(norm_title)
    candidates["review_kind"] = candidates.apply(review_kind, axis=1)
    candidates["is_systematic_candidate"] = candidates.apply(is_systematic, axis=1)
    candidates["is_boundary_candidate"] = candidates.apply(is_boundary, axis=1)
    candidates["topic_tags"] = candidates.apply(lambda r: topic_tags(norm_text(r.get("title_en")), norm_text(r.get("abstract_en_metadata"))), axis=1)

    for col in ["download_status", "pdf_local_path", "pdf_sha256", "text_local_path", "text_sha256"]:
        candidates[col] = candidates["normalized_doi"].map(lambda d: norm_text(audit_map.get(d, {}).get(col)) if d else "")

    ledger_rows: List[Dict[str, str]] = []
    for idx, row in candidates.iterrows():
        rec = candidate_to_record(row, "candidate", "")
        rec.update(
            {
                "corpus_id": f"L0-{idx+1:04d}",
                "is_systematic_candidate": "true" if row["is_systematic_candidate"] else "false",
                "is_boundary_candidate": "true" if row["is_boundary_candidate"] else "false",
                "download_status": norm_text(row.get("download_status")),
                "pdf_local_path_source": norm_text(row.get("pdf_local_path")),
                "text_local_path_source": norm_text(row.get("text_local_path")),
            }
        )
        ledger_rows.append(rec)

    systematic_df = candidates[candidates["is_systematic_candidate"] & ~candidates["is_boundary_candidate"]].copy()
    systematic_df = systematic_df.sort_values(by=list(systematic_df.columns), key=lambda s: s)  # stable no-op before custom below
    systematic_sorted = sorted([row for _, row in systematic_df.iterrows()], key=sort_key)

    seen = set()
    core: List[Dict[str, str]] = []
    reserve: List[Dict[str, str]] = []

    def add_record(rec: Dict[str, str], dest: List[Dict[str, str]]) -> bool:
        key = rec["normalized_doi"] or rec["normalized_title"]
        if not key or key in seen:
            return False
        seen.add(key)
        dest.append(rec)
        return True

    for rec in load_a1_records():
        rec["corpus_id"] = f"CORE-{len(core)+1:03d}"
        add_record(rec, core)

    selection_seed_path = RAW / "selection-seed.csv"
    if not selection_seed_path.exists():
        raise FileNotFoundError(f"missing required A2a selection seed: {selection_seed_path}")
    selection_seed = pd.read_csv(selection_seed_path)
    selection_seed["normalized_doi"] = selection_seed["doi"].map(norm_doi)
    selection_seed_dois = set(selection_seed["normalized_doi"].dropna())
    seeded_rows = [row for _, row in candidates[candidates["normalized_doi"].isin(selection_seed_dois)].iterrows()]
    for row in sorted(seeded_rows, key=sort_key):
        rec = candidate_to_record(row, "core", "A2a 选择种子子集；按 CCF 等级、年份、主题和综述类型分层，作为主候选基础。")
        rec["corpus_id"] = f"CORE-{len(core)+1:03d}"
        add_record(rec, core)
        if len(core) >= CORE_TARGET:
            break

    for row in systematic_sorted:
        if len(core) >= CORE_TARGET:
            break
        rec = candidate_to_record(row, "core", "系统化候选池分层补齐；优先 CCF-A/新近年份/主题多样性/可得全文。")
        rec["corpus_id"] = f"CORE-{len(core)+1:03d}"
        add_record(rec, core)

    for row in systematic_sorted:
        if len(reserve) >= RESERVE_TARGET:
            break
        rec = candidate_to_record(row, "reserve", "与主候选同分布的替补/留出条目；用于替换 A2b 深读排除或全文失败条目。")
        rec["corpus_id"] = f"RESERVE-{len(reserve)+1:03d}"
        add_record(rec, reserve)

    boundary: List[Dict[str, str]] = []
    for _, row in candidates[candidates["is_boundary_candidate"] | ~candidates["is_systematic_candidate"]].iterrows():
        rec = candidate_to_record(row, "boundary", "普通综述、路线图、taxonomy、愿景或系统性不足；只作方法启发/边界样本，不进入主候选统计池。")
        rec["corpus_id"] = f"BOUNDARY-{len(boundary)+1:03d}"
        key = rec["normalized_doi"] or rec["normalized_title"]
        if key not in seen:
            seen.add(key)
            boundary.append(rec)

    common_fields = [
        "corpus_id",
        "source_layer",
        "corpus_tier",
        "slug",
        "cite_key",
        "title",
        "year",
        "publication_date",
        "authors",
        "venue",
        "venue_short",
        "ccf_rank",
        "ccf_category",
        "review_kind",
        "topic_tags",
        "doi",
        "doi_url",
        "landing_page_url",
        "openalex_url",
        "oa_status",
        "ref_count",
        "selection_reason",
        "reserve_reason",
        "boundary_reason",
        "already_a1_inpool",
        "normalized_doi",
        "normalized_title",
    ]
    ledger_fields = common_fields + ["is_systematic_candidate", "is_boundary_candidate", "download_status", "pdf_local_path_source", "text_local_path_source"]
    write_csv(TABLES / "full-candidate-ledger.csv", ledger_rows, ledger_fields)
    systematic_rows = [r for r in ledger_rows if r["is_systematic_candidate"] == "true" and r["is_boundary_candidate"] == "false"]
    write_csv(TABLES / "systematic-candidates.csv", systematic_rows, ledger_fields)
    write_csv(TABLES / "core-corpus.csv", core, common_fields)
    write_csv(TABLES / "reserve-corpus.csv", reserve, common_fields)
    write_csv(TABLES / "boundary-pool.csv", boundary, common_fields)

    status_rows: List[Dict[str, str]] = []
    for rec in core + reserve + boundary:
        doi = rec["normalized_doi"]
        audit_row = audit_map.get(doi, {}) if doi else {}
        source_pdf = norm_text(audit_row.get("pdf_local_path"))
        source_text = norm_text(audit_row.get("text_local_path"))
        source_status = norm_text(audit_row.get("download_status"))
        existing_pdf = PAPERS / rec["slug"] / "paper.pdf"
        existing_text = PAPERS / rec["slug"] / "paper_content.txt"
        metadata_path = PAPERS / rec["slug"] / "metadata.json"
        metadata = {}
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            except Exception:
                metadata = {}
        if existing_pdf.exists():
            final_status = "downloaded"
            failure_type = ""
            pdf_path = str(existing_pdf.relative_to(ROOT))
            text_path = str(existing_text.relative_to(ROOT)) if existing_text.exists() else ""
            text_status = "ok" if existing_text.exists() else "not_attempted"
            attempted = True
            pdf_sha256 = sha256(existing_pdf)
        elif rec["corpus_tier"] == "boundary":
            final_status = "not_applicable"
            failure_type = ""
            pdf_path = ""
            text_path = ""
            text_status = "not_attempted"
            attempted = False
            pdf_sha256 = ""
        else:
            final_status = "manual_needed"
            raw_failure = source_status or "no_public_pdf_url_discovered"
            if source_status in {"ok", "exists_old"} and source_pdf:
                # 旧全文审计中的本地绝对路径只保留为来源线索，不能作为
                # clean clone 下的已获取事实；只有仓库内 paper.pdf 才能计为 downloaded。
                raw_failure = "local_snapshot_not_materialized"
            if rec["slug"] in zotero_failed:
                failure_type = "broken_pdf"
            elif "no_public" in raw_failure:
                failure_type = "paywall"
            elif "local_snapshot_not_materialized" in raw_failure:
                failure_type = "local_snapshot_only"
            elif "source_pdf_missing" in raw_failure:
                failure_type = "broken_pdf"
            elif "fail" in raw_failure:
                failure_type = "broken_pdf"
            else:
                failure_type = "metadata_missing"
            pdf_path = ""
            text_path = ""
            text_status = "not_attempted"
            attempted = True
            pdf_sha256 = ""
        manual_priority = "--"
        if final_status == "manual_needed":
            manual_priority = "P0" if rec["corpus_tier"] == "core" and rec["ccf_rank"] == "CCF-A" else ("P1" if rec["corpus_tier"] == "core" else "P2")
        status_rows.append(
            {
                "corpus_id": rec["corpus_id"],
                "cite_key": rec["cite_key"],
                "slug": rec["slug"],
                "title": rec["title"],
                "doi": rec["doi"],
                "corpus_tier": rec["corpus_tier"],
                "attempted": attempted,
                "attempt_sources": (
                    "A1 仓库内全文资产"
                    if rec["source_layer"].startswith("A1")
                    else (
                        "用户本地 Zotero 导出 PDF 已显式复制入仓库并提取文本"
                        if metadata.get("a2a_pdf_source") == "user_zotero_export" and existing_pdf.exists()
                        else "OpenAlex/DOI 开放获取线索；只有仓库内 paper.pdf 才能计为 downloaded，外部临时路径仅作审计线索"
                    )
                ),
                "final_status": final_status,
                "failure_type": failure_type,
                "pdf_path": pdf_path,
                "pdf_sha256": pdf_sha256,
                "text_path": text_path,
                "text_extraction_status": text_status,
                "manual_priority": manual_priority,
                "source_pdf_path": source_pdf,
                "source_text_path": source_text,
                "notes": (
                    "A1 已有全文"
                    if rec["source_layer"].startswith("A1")
                    else (
                        norm_text(metadata.get("source_note"))
                        if metadata.get("a2a_pdf_source") == "user_zotero_export" and existing_pdf.exists()
                        else (
                            "用户本地 Zotero 附件存在，但 PDF 结构损坏或文本提取失败；已清理半成品并继续列入人工下载清单"
                            if rec["slug"] in zotero_failed
                            else norm_text(audit_row.get("download_error_or_source"))
                        )
                    )
                ),
            }
        )
    status_fields = [
        "corpus_id",
        "cite_key",
        "slug",
        "title",
        "doi",
        "corpus_tier",
        "attempted",
        "attempt_sources",
        "final_status",
        "failure_type",
        "pdf_path",
        "pdf_sha256",
        "text_path",
        "text_extraction_status",
        "manual_priority",
        "source_pdf_path",
        "source_text_path",
        "notes",
    ]
    write_csv(TABLES / "pdf-status.csv", status_rows, status_fields)

    manual_rows = [r for r in status_rows if r["final_status"] == "manual_needed" and r["corpus_tier"] in {"core", "reserve"}]
    with (CORPUS / "manual-download-needed.bib").open("w", encoding="utf-8") as f:
        f.write("% A2a 自动生成：core/reserve 中未自动取得 PDF 的条目。可导入 Zotero 后批量人工下载。\n")
        for r in manual_rows:
            rec = next(x for x in core + reserve if x["slug"] == r["slug"])
            entry_type = "article"
            f.write(f"\n@{entry_type}{{{rec['cite_key']},\n")
            f.write(f"  title = {{{rec['title']}}},\n")
            f.write(f"  author = {{{rec['authors'] or '待补'}}},\n")
            f.write(f"  year = {{{rec['year'] or '待补'}}},\n")
            if rec["venue"]:
                f.write(f"  journal = {{{rec['venue']}}},\n")
            if rec["doi"]:
                f.write(f"  doi = {{{rec['doi']}}},\n")
                f.write(f"  url = {{{rec['doi_url'] or 'https://doi.org/' + rec['doi']}}},\n")
            elif rec["landing_page_url"]:
                f.write(f"  url = {{{rec['landing_page_url']}}},\n")
            f.write(f"  keywords = {{A2a, {rec['corpus_tier']}, {r['manual_priority']}}},\n")
            f.write(f"  note = {{A2a manual download needed; tier={rec['corpus_tier']}; priority={r['manual_priority']}; reason={r['failure_type']}}},\n")
            f.write("}\n")

    with (CORPUS / "manual-download-needed.md").open("w", encoding="utf-8") as f:
        f.write("# A2a 人工下载清单\n\n")
        f.write("本文件由 `scripts/build_corpus_tables.py` 生成，列出主候选 / 替补中自动获取 PDF 失败、需要人工导入 Zotero 下载的条目。\n\n")
        f.write(f"- 当前需人工下载：{len(manual_rows)} 篇。\n")
        f.write("- BibTeX 汇总：[manual-download-needed.bib](./manual-download-needed.bib)。\n\n")
        f.write("| 优先级 | 层级 | 年份 | CCF | 标题 | DOI / URL | 失败类型 |\n")
        f.write("|---|---|---:|---|---|---|---|\n")
        for r in sorted(manual_rows, key=lambda x: (x["manual_priority"], x["corpus_tier"], x["title"])):
            rec = next(x for x in core + reserve if x["slug"] == r["slug"])
            url = rec["doi_url"] or rec["landing_page_url"] or rec["openalex_url"] or "--"
            title_md = rec["title"].replace("|", " / ")
            f.write(f"| {r['manual_priority']} | {rec['corpus_tier']} | {rec['year']} | {rec['ccf_rank'] or '--'} | {title_md} | {url} | {r['failure_type']} |\n")

    print(json.dumps({
        "full_candidate_ledger": len(ledger_rows),
        "systematic_candidates": len(systematic_rows),
        "core": len(core),
        "reserve": len(reserve),
        "boundary": len(boundary),
        "manual_needed_core_reserve": len(manual_rows),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
