"""机械核验外部引用是否真实存在：解析 DOI / arXiv ID，比对标题与年份。

⛔ 本工具**只做存在性与题录比对，不做内容裁定**（仓库纪律〈机械代理只能定位不能裁定〉）。
它回答「这篇论文存不存在、题录对不对得上」，⛔ **不回答**「原文里真有那句话吗」——
后者必须人取原文核（伞 PR §4.1 层 4 的 C1）。

三种标识符：

- **DOI** → `https://doi.org/api/handles/<doi>` 与 Crossref `https://api.crossref.org/works/<doi>`
- **arXiv** → `http://export.arxiv.org/api/query?id_list=<id>`
- **裸 URL** → 只做可达性检查，⛔ 拿不到题录，一律记 `UNVERIFIED_URL`

标题比对用**归一化后的词集合 Jaccard**，⛔ 不做精确匹配 —— 检索结果里的标题常有
大小写、连字符、副标题截断的差异，精确匹配会把真引用判成假的。⚠️ 反过来，阈值过低
会放过「标题相似但其实是另一篇」的幻觉，故默认 0.6 并把分数一并输出供人工复核。

用法：

    python verify_citations.py --findings external.json --out citation_report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

_DOI = re.compile(r"\b(10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+)\b")
_ARXIV = re.compile(r"(?:arxiv[:\s/]*)?(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_UA = "research-ideas-l2-citation-check/1.0 (mailto:hansbug@buaa.edu.cn)"


def _norm_words(title: str) -> set[str]:
    title = re.sub(r"[^0-9a-z\s]+", " ", title.lower())
    stop = {"a", "an", "the", "of", "for", "and", "in", "on", "to", "with", "using", "via"}
    return {w for w in title.split() if w and w not in stop}


def _jaccard(a: str, b: str) -> float:
    wa, wb = _norm_words(a), _norm_words(b)
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _get(url: str, timeout: float = 20.0) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
        return None


def _resolve_crossref(doi: str) -> dict | None:
    raw = _get(f"https://api.crossref.org/works/{urllib.parse.quote(doi)}")
    if raw is None:
        return None
    try:
        msg = json.loads(raw)["message"]
    except (ValueError, KeyError):
        return None
    parts = (msg.get("issued") or {}).get("date-parts") or [[None]]
    return {
        "title": (msg.get("title") or [""])[0],
        "year": parts[0][0] if parts and parts[0] else None,
        "venue": (msg.get("container-title") or [""])[0] or msg.get("publisher", ""),
        "type": msg.get("type", ""),
        "registry": "crossref",
    }


def _resolve_datacite(doi: str) -> dict | None:
    """DataCite 注册的 DOI（arXiv 的 `10.48550/*` 全在这里，⛔ Crossref 查不到）。"""
    raw = _get(f"https://api.datacite.org/dois/{urllib.parse.quote(doi, safe='')}")
    if raw is None:
        return None
    try:
        attrs = json.loads(raw)["data"]["attributes"]
    except (ValueError, KeyError):
        return None
    titles = attrs.get("titles") or [{}]
    return {
        "title": titles[0].get("title", ""),
        "year": attrs.get("publicationYear"),
        "venue": (attrs.get("publisher") or ""),
        "type": (attrs.get("types") or {}).get("resourceTypeGeneral", ""),
        "registry": "datacite",
    }


def resolve_doi(doi: str) -> dict | None:
    """先 Crossref 再 DataCite。⚠️ 两家分工不同，⛔ 只查一家会把真论文判成不存在。"""
    return _resolve_crossref(doi) or _resolve_datacite(doi)


def resolve_arxiv(arxiv_id: str) -> dict | None:
    raw = _get(f"http://export.arxiv.org/api/query?id_list={urllib.parse.quote(arxiv_id)}")
    if raw is None:
        return None
    text = raw.decode("utf-8", "replace")
    if "<entry>" not in text:
        return None
    m_title = re.search(r"<entry>.*?<title>(.*?)</title>", text, re.S)
    m_pub = re.search(r"<entry>.*?<published>(\d{4})", text, re.S)
    if not m_title:
        return None
    return {
        "title": re.sub(r"\s+", " ", m_title.group(1)).strip(),
        "year": int(m_pub.group(1)) if m_pub else None,
        "venue": "arXiv",
        "type": "preprint",
    }


def check(finding: dict, threshold: float) -> dict:
    ident = (finding.get("identifier") or "").strip()
    claimed_title = finding.get("title", "")
    claimed_year = finding.get("year")
    out = {
        "predicate": finding.get("predicate"),
        "claimed_title": claimed_title,
        "claimed_year": claimed_year,
        "identifier": ident,
        "read_level": finding.get("read_level"),
        "status": None,
        "resolved_title": None,
        "resolved_year": None,
        "title_similarity": None,
    }

    # 本地文库条目不走网络：identifier 是目录 slug
    if ident and "/" not in ident and "." not in ident:
        out["status"] = "LOCAL_CORPUS"
        return out

    # ⚠️ 标识符字段常是复合串（"arXiv:2508.00630v2 / DOI 10.48550/arXiv.2508.00630 / https://…"）。
    # ⛔ 首版按「DOI 优先」取，于是对 arXiv 论文拿到 10.48550 前缀去查 Crossref —— 那是 DataCite
    # 的地盘，必然查不到，真论文被判成 NOT_RESOLVED。⭐ 改为 arXiv 优先，DOI 兜底。
    m_arxiv = _ARXIV.search(ident) if ("arxiv" in ident.lower() or _ARXIV.fullmatch(ident.strip())) else None
    m_doi = _DOI.search(ident)

    meta = None
    tried = []
    if m_arxiv:
        tried.append("arxiv")
        meta = resolve_arxiv(m_arxiv.group(1))
    if meta is None and m_doi:
        tried.append("doi")
        meta = resolve_doi(m_doi.group(1))
    if meta is None:
        urls = re.findall(r"https?://\S+", ident)
        if not tried and urls:
            out["status"] = "REACHABLE_URL" if _get(urls[0].rstrip(".,;")) is not None else "URL_UNREACHABLE"
            return out
        if not tried:
            out["status"] = "NO_USABLE_IDENTIFIER"
            return out
        out["status"] = "ARXIV_NOT_RESOLVED" if tried == ["arxiv"] else "DOI_NOT_RESOLVED"
        # ⭐ 解析不到时退一步只测可达性，⛔ 免得把「我们的解析器不认」报成「这篇不存在」
        if urls and _get(urls[0].rstrip(".,;")) is not None:
            out["status"] += "_BUT_URL_REACHABLE"
        return out

    out["resolved_title"] = meta["title"]
    out["resolved_year"] = meta["year"]
    sim = _jaccard(claimed_title, meta["title"])
    out["title_similarity"] = round(sim, 3)

    if sim < threshold:
        out["status"] = "TITLE_MISMATCH"
    elif claimed_year and meta["year"] and abs(int(claimed_year) - int(meta["year"])) > 1:
        # 容 1 年：会议论文的 online-first 与正式出版常跨年
        out["status"] = "YEAR_MISMATCH"
    else:
        out["status"] = "OK"
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--findings", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--delay", type=float, default=0.4, help="每次请求之间的间隔，别把 API 打爆")
    args = parser.parse_args(argv)

    findings = json.loads(args.findings.read_text(encoding="utf-8"))
    # 同一 identifier 只查一次
    seen: dict[str, dict] = {}
    reports = []
    for f in findings:
        key = (f.get("identifier") or "").strip()
        if key in seen:
            rep = dict(seen[key])
            rep["predicate"] = f.get("predicate")
            reports.append(rep)
            continue
        rep = check(f, args.threshold)
        seen[key] = rep
        reports.append(rep)
        if rep["status"] not in ("LOCAL_CORPUS", "NO_USABLE_IDENTIFIER"):
            time.sleep(args.delay)

    from collections import Counter

    counts = Counter(r["status"] for r in reports)
    print(f"核验 {len(reports)} 条引用（去重后实查 {len(seen)} 个标识符）")
    for k, v in counts.most_common():
        print(f"  {k}: {v}")

    bad = [r for r in reports if r["status"] not in ("OK", "LOCAL_CORPUS", "REACHABLE_URL")]
    for r in bad[:40]:
        print(f"  ⛔ {r['status']:22s} sim={r['title_similarity']} | {r['claimed_title'][:70]}")
        if r["resolved_title"]:
            print(f"      解析到：{r['resolved_title'][:80]}（{r['resolved_year']}）")

    if args.out:
        args.out.write_text(json.dumps(reports, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
