#!/usr/bin/env python3
"""Build yearly CCF SE/Systems/PL venue indexes.

This script focuses on the CCF category documented in
`frontier_index/CCF_SE_A_B_C.md` and currently targets the yearly
metadata index workflow under `frontier_index/ccf_history/<year>/`.

The generated artifacts are:

1. `README.md`
2. `verification.json`
3. `metadata/<venue>.json`
4. `bib/<venue>.bib`

The script is intentionally cache-aware so repeated runs can refine the
result without re-fetching every remote resource from scratch.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests
from lxml import etree as ET


ROOT = Path(__file__).resolve().parents[1]
CCF_MD = ROOT / "frontier_index" / "CCF_SE_A_B_C.md"


JOURNAL_HOMEPAGES: Dict[str, str] = {
    "TOPLAS": "https://dl.acm.org/journal/toplas",
    "TOSEM": "https://dl.acm.org/journal/tosem",
    "TSE": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=32",
    "TSC": "https://ieeexplore.ieee.org/xpl/RecentIssue.jsp?punumber=4629386",
    "ASE": "https://link.springer.com/journal/10515",
    "ESE": "https://link.springer.com/journal/10664",
    "IETS": "https://ietresearch.onlinelibrary.wiley.com/journal/1751880x",
    "IST": "https://www.sciencedirect.com/journal/information-and-software-technology",
    "JFP": "https://www.cambridge.org/core/journals/journal-of-functional-programming",
    "JSEP": "https://onlinelibrary.wiley.com/journal/20477481",
    "JSS": "https://www.sciencedirect.com/journal/journal-of-systems-and-software",
    "RE": "https://link.springer.com/journal/766",
    "SCP": "https://www.sciencedirect.com/journal/science-of-computer-programming",
    "SoSyM": "https://link.springer.com/journal/10270",
    "STVR": "https://onlinelibrary.wiley.com/journal/10991689",
    "SPE": "https://onlinelibrary.wiley.com/journal/1097024x",
    "CL": "https://www.sciencedirect.com/journal/computer-languages-systems-and-structures",
    "IJSEKE": "https://www.worldscientific.com/worldscinet/ijseke",
    "STTT": "https://link.springer.com/journal/10009",
    "JLAMP": "https://www.sciencedirect.com/journal/journal-of-logical-and-algebraic-methods-in-programming",
    "JWE": "https://www.rintonpress.com/journals/jwe.html",
    "SOCA": "https://link.springer.com/journal/11761",
    "SQJ": "https://link.springer.com/journal/11219",
    "TPLP": "https://www.cambridge.org/core/journals/theory-and-practice-of-logic-programming",
    "PACM PL": "https://dl.acm.org/journal/pacmpl",
}


CONFERENCE_HOME_INFO: Dict[str, Dict[str, str]] = {
    "ICSE": {
        "homepage": "https://conf.researchr.org/home/icse-2025",
    },
    "ASE": {
        "homepage": "https://conf.researchr.org/home/ase-2025",
    },
    "FSE": {
        "homepage": "https://conf.researchr.org/home/fse-2025",
    },
    "ISSTA": {
        "homepage": "https://conf.researchr.org/home/issta-2025",
    },
}


SPECIAL_CONFERENCE_SOURCES: Dict[str, Dict[str, Any]] = {
    "FSE": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/sigsoft: year:{year}:",
        "venue_label": "Proc. ACM Softw. Eng.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmse",
    },
    "ISSTA": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/issta: year:{year}:",
        "venue_label": "Proc. ACM Softw. Eng.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmse",
    },
    "PLDI": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/pldi: year:{year}:",
        "venue_label": "Proc. ACM Program. Lang.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmpl",
    },
    "POPL": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/popl: year:{year}:",
        "venue_label": "Proc. ACM Program. Lang.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmpl",
    },
    "ICFP": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/icfp: year:{year}:",
        "venue_label": "Proc. ACM Program. Lang.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmpl",
    },
    "OOPSLA": {
        "mode": "stream_venue",
        "query_template": "streamid:conf/oopsla: year:{year}:",
        "venue_label": "Proc. ACM Program. Lang.",
        "carrier_homepage": "https://dl.acm.org/journal/pacmpl",
    },
    "SANER": {
        "mode": "venue_query",
        "query_template": 'venue:"SANER" year:{year}:',
    },
    "FM": {
        "mode": "fm_special",
    },
    "ETAPS": {
        "mode": "empty",
        "reason": "ETAPS 作为 umbrella venue，在 2025 年未检出直接归属 ETAPS 主论文条目；其学术产出主要分散在子会议和附属 workshop 中。",
    },
}


BAD_CONFERENCE_HINTS = (
    "COMPANION",
    "WORKSHOP",
    "WORKSHOPS",
    "POSTER",
    "POSTERS",
    "DEMO",
    "DEMOS",
    "DOCTORAL",
    "NIER",
    "SEIP",
    "SEET",
    "SRC",
    "INDUSTRY",
    "JOURNALFIRST",
    "TUTORIAL",
    "WIP",
    "@",
)


TAG_RULES = [
    ("LLM/AI for SE", ("llm", "large language model", "code model", "neural", "foundation model", "ai-powered")),
    ("需求工程", ("requirement", "requirements", "specification", "goal model")),
    ("测试与验证", ("test", "testing", "validation", "verification", "fuzz", "oracle")),
    ("形式化方法", ("formal", "theorem", "proof", "logic", "model checking", "symbolic", "synthesis")),
    ("程序分析", ("static analysis", "dynamic analysis", "program analysis", "taint", "dataflow", "pointer analysis")),
    ("程序修复", ("repair", "patch", "debug", "fault localization", "bug fixing")),
    ("维护与演化", ("maintenance", "evolution", "reengineering", "repository", "technical debt", "change")),
    ("建模/模型驱动", ("model", "model-driven", "state machine", "statechart", "behavior tree")),
    ("可靠性/安全", ("reliability", "security", "vulnerability", "fault", "bug", "privacy")),
    ("系统软件", ("operating system", "middleware", "distributed system", "cloud", "kernel")),
    ("程序设计语言/编译", ("compiler", "type system", "programming language", "semantics", "optimization")),
    ("经验软件工程", ("empirical", "user study", "mining", "repository mining", "developer")),
    ("运行时监测", ("runtime verification", "runtime", "monitoring")),
]

OFFICIAL_HOST_HINTS = (
    "dl.acm.org",
    "ieeexplore.ieee.org",
    "link.springer.com",
    "link.springeropen.com",
    "sciencedirect.com",
    "onlinelibrary.wiley.com",
    "usenix.org",
    "cambridge.org",
    "worldscientific.com",
    "rintonpress.com",
)
PROCEEDINGS_KEY_RE = re.compile(r"^conf/[^/]+/\d{4}(-\d+)?$")

GREEN_PATTERNS = (
    "state machine",
    "statechart",
    "automata",
    "timed automata",
    "model checking",
    "formal verification",
    "formal method",
    "runtime verification",
    "specification",
    "requirements engineering",
    "requirement",
    "repair",
    "fault localization",
    "synthesis",
    "temporal logic",
    "ltl",
    "ctl",
    "model-driven",
    "symbolic execution",
)

YELLOW_PATTERNS = (
    "test",
    "testing",
    "verification",
    "program analysis",
    "static analysis",
    "dynamic analysis",
    "reliability",
    "safety",
    "security",
    "maintenance",
    "evolution",
    "mining",
    "developer",
    "repository",
    "empirical",
)

RELEVANT_TAGS = {
    "需求工程",
    "测试与验证",
    "形式化方法",
    "程序分析",
    "程序修复",
    "维护与演化",
    "建模/模型驱动",
    "可靠性/安全",
    "运行时监测",
}


@dataclass
class Venue:
    abbr: str
    full_name: str
    rank: str
    kind: str
    index_url: str


class Builder:
    def __init__(self, year: int, target_dir: Path):
        self.year = year
        self.target_dir = target_dir
        self.cache_dir = target_dir / "_cache"
        self.metadata_dir = target_dir / "metadata"
        self.bib_dir = target_dir / "bib"

    @staticmethod
    def new_session() -> requests.Session:
        session = requests.Session()
        session.headers["User-Agent"] = "research-ideas-ccf-index-builder/0.1"
        session.trust_env = False
        return session

    def ensure_dirs(self) -> None:
        for path in [self.target_dir, self.cache_dir, self.metadata_dir, self.bib_dir]:
            path.mkdir(parents=True, exist_ok=True)
        for path in self.metadata_dir.glob("*.json"):
            path.unlink()
        for path in self.bib_dir.glob("*.bib"):
            path.unlink()

    def cache_path(self, namespace: str, key: str, suffix: str) -> Path:
        digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
        path = self.cache_dir / namespace
        path.mkdir(parents=True, exist_ok=True)
        return path / f"{digest}{suffix}"

    @staticmethod
    def cache_alias_keys(key: str) -> List[str]:
        aliases = []
        if "https://dblp.org" in key:
            aliases.append(key.replace("https://dblp.org", "http://dblp.uni-trier.de"))
            aliases.append(key.replace("https://dblp.org", "https://dblp.uni-trier.de"))
        if "http://dblp.uni-trier.de" in key:
            aliases.append(key.replace("http://dblp.uni-trier.de", "https://dblp.org"))
        if "https://dblp.uni-trier.de" in key:
            aliases.append(key.replace("https://dblp.uni-trier.de", "https://dblp.org"))
        deduped = []
        for item in aliases:
            if item != key and item not in deduped:
                deduped.append(item)
        return deduped

    def http_get_text(self, url: str) -> str:
        cache = self.cache_path("http_text", url, ".txt")
        if cache.exists():
            return cache.read_text(encoding="utf-8")
        aliases = self.cache_alias_keys(url)
        for alias in aliases:
            alias_cache = self.cache_path("http_text", alias, ".txt")
            if alias_cache.exists():
                text = alias_cache.read_text(encoding="utf-8")
                cache.write_text(text, encoding="utf-8")
                return text
        last_err: Optional[Exception] = None
        for idx in range(6):
            try:
                with self.new_session() as session:
                    resp = session.get(url, timeout=40)
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise RuntimeError(f"temporary status {resp.status_code}")
                resp.raise_for_status()
                text = resp.text
                cache.write_text(text, encoding="utf-8")
                time.sleep(0.15)
                return text
            except Exception as exc:  # pragma: no cover - network retries
                last_err = exc
                time.sleep(1.5 * (idx + 1))
        for alias in aliases:
            alias_cache = self.cache_path("http_text", alias, ".txt")
            for idx in range(4):
                try:
                    with self.new_session() as session:
                        resp = session.get(alias, timeout=40)
                    if resp.status_code in (429, 500, 502, 503, 504):
                        raise RuntimeError(f"temporary status {resp.status_code}")
                    resp.raise_for_status()
                    text = resp.text
                    alias_cache.write_text(text, encoding="utf-8")
                    cache.write_text(text, encoding="utf-8")
                    time.sleep(0.15)
                    return text
                except Exception as exc:  # pragma: no cover - network retries
                    last_err = exc
                    time.sleep(1.2 * (idx + 1))
        raise RuntimeError(f"GET failed for {url}: {last_err}")

    def http_head_location(self, doi_url: str) -> str:
        cache = self.cache_path("doi_loc", doi_url, ".json")
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))["location"]
        location = doi_url
        last_err: Optional[Exception] = None
        for idx in range(6):
            try:
                with self.new_session() as session:
                    resp = session.head(doi_url, allow_redirects=False, timeout=25)
                if resp.status_code in (301, 302, 303, 307, 308):
                    location = resp.headers.get("location") or doi_url
                else:
                    location = doi_url
                cache.write_text(json.dumps({"location": location}, ensure_ascii=False), encoding="utf-8")
                time.sleep(0.05)
                return location
            except Exception as exc:  # pragma: no cover - network retries
                last_err = exc
                time.sleep(1.2 * (idx + 1))
        cache.write_text(json.dumps({"location": location, "error": str(last_err)}, ensure_ascii=False), encoding="utf-8")
        return location

    def dblp_search(self, query: str, h: int = 1000) -> Dict[str, Any]:
        url = f"https://dblp.org/search/publ/api?q={requests.utils.quote(query)}&h={h}&format=json"
        cache = self.cache_path("dblp_search", url, ".json")
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        text = self.http_get_text(url)
        data = json.loads(text)
        cache.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return data

    def openalex_batch(self, dois: List[str]) -> Dict[str, Dict[str, Any]]:
        if not dois:
            return {}
        normalized = sorted({doi.lower() for doi in dois})
        key = "|".join(normalized)
        cache = self.cache_path("openalex", key, ".json")
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        filt = "doi:" + "|".join(normalized)
        params = {
            "filter": filt,
            "per-page": str(max(len(normalized), 1)),
            "mailto": "example@example.com",
        }
        last_err: Optional[Exception] = None
        for idx in range(6):
            try:
                with self.new_session() as session:
                    resp = session.get("https://api.openalex.org/works", params=params, timeout=40)
                if resp.status_code in (429, 500, 502, 503, 504):
                    raise RuntimeError(f"temporary status {resp.status_code}")
                resp.raise_for_status()
                payload = resp.json()
                mapping: Dict[str, Dict[str, Any]] = {}
                for item in payload.get("results", []):
                    doi_url = item.get("doi") or ""
                    doi = doi_url.replace("https://doi.org/", "").lower()
                    if doi:
                        mapping[doi] = item
                cache.write_text(json.dumps(mapping, ensure_ascii=False), encoding="utf-8")
                time.sleep(0.2)
                return mapping
            except Exception as exc:  # pragma: no cover - network retries
                last_err = exc
                time.sleep(1.5 * (idx + 1))
        raise RuntimeError(f"OpenAlex batch failed: {last_err}")

    def dblp_bibtex(self, key: str) -> str:
        url = f"https://dblp.org/rec/{key}.bib"
        text = self.http_get_text(url)
        return self.normalize_bibtex(text)

    @staticmethod
    def normalize_bibtex(text: str) -> str:
        return (
            text.replace("â€“", "--")
            .replace("â€”", "---")
            .replace("\u2013", "--")
            .replace("\u2014", "---")
            .replace("\xa0", " ")
        )

    @staticmethod
    def parse_ccf_venues() -> List[Venue]:
        text = CCF_MD.read_text(encoding="utf-8")
        venues: List[Venue] = []
        rank = ""
        kind = ""
        for line in text.splitlines():
            m = re.match(r"##\s+\d+\.\s+([ABC])\s+类(会议|期刊)", line)
            if m:
                rank, kind = m.groups()
                continue
            if not line.startswith("| `"):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) != 4:
                continue
            abbr = parts[0].strip("`")
            full_name = parts[1]
            match = re.search(r"\((https?://[^)]+)\)", parts[3])
            if not match:
                continue
            index_url = match.group(1)
            venues.append(Venue(abbr=abbr, full_name=full_name, rank=rank, kind=kind, index_url=index_url))
        return venues

    @staticmethod
    def slug_from_index(index_url: str) -> Optional[tuple[str, str]]:
        match = re.search(r"/db/(conf|journals)/([^/]+)/", index_url)
        if not match:
            match = re.search(r"/db/(conf|journals)/([^/]+)$", index_url)
        if not match:
            return None
        return match.group(1), match.group(2)

    @staticmethod
    def normalize_token(text: str) -> str:
        return re.sub(r"[^A-Z0-9]+", "", text.upper())

    @staticmethod
    def choose_tags(text: str) -> List[str]:
        lowered = text.lower()
        tags: List[str] = []
        for label, patterns in TAG_RULES:
            if any(p in lowered for p in patterns):
                tags.append(label)
            if len(tags) >= 3:
                break
        if not tags:
            tags.append("待人工细分")
        return tags[:3]

    @staticmethod
    def clean_text(text: str) -> str:
        if not text:
            return ""
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    @staticmethod
    def ensure_list(value: Any) -> List[str]:
        if not value:
            return []
        if isinstance(value, list):
            items = value
        else:
            items = [value]
        cleaned = [Builder.clean_text(str(item)) for item in items if str(item).strip()]
        return [item for item in cleaned if item]

    @staticmethod
    def looks_like_pdf(url: str) -> bool:
        lowered = url.lower()
        return lowered.endswith(".pdf") or "/pdf" in lowered or "download" in lowered

    def prefer_official_url(self, urls: Iterable[str]) -> str:
        candidates = []
        for url in urls:
            cleaned = self.clean_text(url)
            if not cleaned or "dblp.org" in cleaned:
                continue
            score = 0
            if any(host in cleaned for host in OFFICIAL_HOST_HINTS):
                score += 10
            if not self.looks_like_pdf(cleaned):
                score += 5
            if cleaned.startswith("https://"):
                score += 2
            candidates.append((score, cleaned))
        if not candidates:
            return ""
        candidates.sort(key=lambda item: (-item[0], item[1]))
        return candidates[0][1]

    @staticmethod
    def matched_patterns(text: str, patterns: Iterable[str]) -> List[str]:
        lowered = text.lower()
        return [pattern for pattern in patterns if pattern in lowered]

    def classify_screening(self, title: str, abstract: str, tags: List[str]) -> Dict[str, str]:
        combined = " ".join([title, abstract]).lower()
        green_hits = self.matched_patterns(combined, GREEN_PATTERNS)
        yellow_hits = self.matched_patterns(combined, YELLOW_PATTERNS)
        tag_hits = [tag for tag in tags if tag in RELEVANT_TAGS]

        if green_hits:
            reason = "命中高相关信号：" + " / ".join(green_hits[:3])
            if tag_hits:
                reason += "；方向标签：" + " / ".join(tag_hits[:2])
            return {
                "initial_screening": "🟢 优先跟进",
                "screening_reason": reason,
                "pdf_followup": "🟢 建议获取 PDF",
            }

        if tag_hits and abstract:
            reason = "命中相关方向标签：" + " / ".join(tag_hits[:3])
            if yellow_hits:
                reason += "；并含一般相关线索：" + " / ".join(yellow_hits[:2])
            return {
                "initial_screening": "🟡 保留观察",
                "screening_reason": reason,
                "pdf_followup": "🟡 可选获取",
            }

        if yellow_hits and abstract:
            return {
                "initial_screening": "🟡 保留观察",
                "screening_reason": "命中一般相关线索：" + " / ".join(yellow_hits[:3]),
                "pdf_followup": "🟡 可选获取",
            }

        if not abstract:
            reason = "摘要暂缺，需结合标题、venue 与官方页人工复核。"
            if tag_hits:
                reason = "摘要暂缺，但方向标签提示相关：" + " / ".join(tag_hits[:2])
            return {
                "initial_screening": "⏳ 待补信息",
                "screening_reason": reason,
                "pdf_followup": "⏳ 未判断",
            }

        return {
            "initial_screening": "⚪ 暂不跟进",
            "screening_reason": "当前未命中高相关信号，优先级低于形式化建模/验证/修复主线。",
            "pdf_followup": "⚪ 暂不获取",
        }

    def xml_url(self, index_url: str) -> str:
        index_url = index_url.replace("http://", "https://").replace("dblp.uni-trier.de", "dblp.org")
        if index_url.endswith("index.html"):
            return index_url[:-5] + ".xml"
        if index_url.endswith(".html"):
            return index_url[:-5] + ".xml"
        if index_url.endswith("/"):
            return index_url + "index.xml"
        return index_url.rstrip("/") + "/index.xml"

    def parse_proceedings(self, xml_text: str) -> List[Dict[str, Any]]:
        root = ET.fromstring(("<root>" + xml_text + "</root>").encode("utf-8"))
        rows: List[Dict[str, Any]] = []
        for proc in root.findall(".//proceedings"):
            rows.append(
                {
                    "key": proc.get("key") or "",
                    "title": self.clean_text(proc.findtext("title") or ""),
                    "booktitle": self.clean_text(proc.findtext("booktitle") or ""),
                    "year": proc.findtext("year") or "",
                    "url": proc.findtext("url") or "",
                    "ee": [self.clean_text(node.text or "") for node in proc.findall("ee")],
                }
            )
        for article in root.findall(".//article"):
            # Used for journal volume pages only.
            rows.append(
                {
                    "kind": "article",
                    "key": article.get("key") or "",
                    "title": self.clean_text(article.findtext("title") or ""),
                    "journal": self.clean_text(article.findtext("journal") or ""),
                    "year": article.findtext("year") or "",
                    "url": article.findtext("url") or "",
                    "ee": [self.clean_text(node.text or "") for node in article.findall("ee")],
                }
            )
        return rows

    def choose_conference_source(self, venue: Venue) -> Dict[str, Any]:
        if venue.abbr in SPECIAL_CONFERENCE_SOURCES:
            override = dict(SPECIAL_CONFERENCE_SOURCES[venue.abbr])
            override["override"] = True
            return override

        xml_text = self.http_get_text(self.xml_url(venue.index_url))
        proceedings = [p for p in self.parse_proceedings(xml_text) if p.get("year") == str(self.year) and "booktitle" in p]
        abbr = self.normalize_token(venue.abbr)
        exact_booktitle = [
            row
            for row in proceedings
            if self.normalize_token(row["booktitle"]) == abbr
            and not any(marker in self.normalize_token(" ".join([row["booktitle"], row["title"], row["url"]])) for marker in BAD_CONFERENCE_HINTS)
        ]
        if exact_booktitle:
            exact_booktitle = sorted(exact_booktitle, key=lambda item: item["url"])
            return {
                "mode": "toc_multi",
                "toc_urls": [item["url"] for item in exact_booktitle],
                "proceedings_meta": exact_booktitle,
            }
        scored: List[tuple[int, Dict[str, Any]]] = []
        for row in proceedings:
            combined = " ".join([row["booktitle"], row["title"], row["url"]])
            token = self.normalize_token(combined)
            bad = any(marker in token for marker in BAD_CONFERENCE_HINTS)
            score = 0
            if self.normalize_token(row["booktitle"]) == abbr:
                score += 10
            if abbr in self.normalize_token(row["title"]):
                score += 6
            if abbr in self.normalize_token(row["url"]):
                score += 4
            if "PARTI" in token or "PARTII" in token:
                score += 2
            if bad:
                score -= 20
            scored.append((score, row))
        positive = [row for score, row in scored if score > 0]
        if positive:
            positive = sorted(positive, key=lambda item: item["url"])
            return {
                "mode": "toc_multi",
                "toc_urls": [item["url"] for item in positive],
                "proceedings_meta": positive,
            }

        slug = self.slug_from_index(venue.index_url)
        if slug:
            stream_query = f"streamid:{slug[0]}/{slug[1]}: year:{self.year}:"
            data = self.dblp_search(stream_query)
            hits = data["result"]["hits"].get("hit", [])
            if isinstance(hits, dict):
                hits = [hits]
            if hits:
                counts: Counter[str] = Counter()
                for hit in hits:
                    label = hit["info"].get("venue")
                    if isinstance(label, list):
                        label = " / ".join(label)
                    counts[label] += 1
                dominant_label = counts.most_common(1)[0][0]
                return {
                    "mode": "stream_venue",
                    "query_template": stream_query,
                    "venue_label": dominant_label,
                }

        return {
            "mode": "venue_query",
            "query_template": f'venue:"{venue.abbr}" year:{self.year}:',
        }

    def search_hits(self, query: str) -> List[Dict[str, Any]]:
        data = self.dblp_search(query)
        hits = data["result"]["hits"].get("hit", [])
        if isinstance(hits, dict):
            hits = [hits]
        return hits

    def filter_conference_hits(self, hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = []
        for hit in hits:
            key = hit.get("info", {}).get("key", "")
            if PROCEEDINGS_KEY_RE.match(key):
                continue
            filtered.append(hit)
        return filtered

    def collect_entries_for_venue(self, venue: Venue) -> Dict[str, Any]:
        if venue.kind == "期刊":
            slug = self.slug_from_index(venue.index_url)
            if not slug:
                raise RuntimeError(f"cannot parse journal slug for {venue.abbr}")
            query = f"streamid:{slug[0]}/{slug[1]}: year:{self.year}:"
            hits = self.search_hits(query)
            return {
                "mode": "journal_stream",
                "source_query": query,
                "hits": hits,
                "expected_total": len(hits),
                "key_pages": {
                    "journal_homepage": JOURNAL_HOMEPAGES.get(venue.abbr, ""),
                    "index_page": venue.index_url,
                },
            }

        source = self.choose_conference_source(venue)
        mode = source["mode"]

        if mode == "empty":
            return {
                "mode": "empty",
                "source_query": "",
                "hits": [],
                "expected_total": 0,
                "key_pages": {
                    "homepage": CONFERENCE_HOME_INFO.get(venue.abbr, {}).get("homepage", ""),
                    "index_page": venue.index_url,
                    "note": source["reason"],
                },
            }

        if mode == "venue_query":
            query = source["query_template"].format(year=self.year)
            hits = self.filter_conference_hits(self.search_hits(query))
            return {
                "mode": mode,
                "source_query": query,
                "hits": hits,
                "expected_total": len(hits),
                "key_pages": {
                    "homepage": CONFERENCE_HOME_INFO.get(venue.abbr, {}).get("homepage", ""),
                    "index_page": venue.index_url,
                },
            }

        if mode == "stream_venue":
            query = source["query_template"].format(year=self.year)
            all_hits = self.search_hits(query)
            selected = []
            for hit in all_hits:
                label = hit["info"].get("venue")
                if isinstance(label, list):
                    label = " / ".join(label)
                if label == source["venue_label"]:
                    selected.append(hit)
            selected = self.filter_conference_hits(selected)
            return {
                "mode": mode,
                "source_query": query,
                "hits": selected,
                "expected_total": len(selected),
                "key_pages": {
                    "homepage": CONFERENCE_HOME_INFO.get(venue.abbr, {}).get("homepage", ""),
                    "carrier_homepage": source.get("carrier_homepage", ""),
                    "index_page": venue.index_url,
                },
            }

        if mode == "toc_multi":
            all_hits: List[Dict[str, Any]] = []
            proceedings_pages: List[str] = []
            for url in source["toc_urls"]:
                query = f"toc:{url.replace('.html', '.bht')}:"
                hits = self.search_hits(query)
                hits = self.filter_conference_hits(hits)
                meta = None
                for item in source.get("proceedings_meta", []):
                    if item["url"] == url:
                        meta = item
                        break
                if meta:
                    for hit in hits:
                        hit["__container_title"] = meta.get("title", "")
                        hit["__container_booktitle"] = meta.get("booktitle", "")
                        hit["__container_ee"] = meta.get("ee", [])
                all_hits.extend(hits)
            for meta in source.get("proceedings_meta", []):
                proceedings_pages.extend(meta.get("ee", []))
            return {
                "mode": mode,
                "source_query": "; ".join(source["toc_urls"]),
                "hits": all_hits,
                "expected_total": len(all_hits),
                "key_pages": {
                    "homepage": CONFERENCE_HOME_INFO.get(venue.abbr, {}).get("homepage", ""),
                    "index_page": venue.index_url,
                    "proceedings_pages": proceedings_pages,
                },
            }

        if mode == "fm_special":
            xml_text = self.http_get_text(self.xml_url(venue.index_url))
            proceedings = [
                p
                for p in self.parse_proceedings(xml_text)
                if p.get("year") == str(self.year) and p.get("booktitle", "").startswith("FM")
            ]
            toc_urls = [p["url"] for p in proceedings]
            all_hits: List[Dict[str, Any]] = []
            for url in toc_urls:
                query = f"toc:{url.replace('.html', '.bht')}:"
                hits = self.search_hits(query)
                hits = self.filter_conference_hits(hits)
                meta = None
                for item in proceedings:
                    if item["url"] == url:
                        meta = item
                        break
                if meta:
                    for hit in hits:
                        hit["__container_title"] = meta.get("title", "")
                        hit["__container_booktitle"] = meta.get("booktitle", "")
                        hit["__container_ee"] = meta.get("ee", [])
                all_hits.extend(hits)
            return {
                "mode": mode,
                "source_query": "; ".join(toc_urls),
                "hits": all_hits,
                "expected_total": len(all_hits),
                "key_pages": {
                    "homepage": CONFERENCE_HOME_INFO.get(venue.abbr, {}).get("homepage", ""),
                    "index_page": venue.index_url,
                    "proceedings_pages": [ee for p in proceedings for ee in p.get("ee", [])],
                },
            }

        raise RuntimeError(f"unsupported mode {mode} for {venue.abbr}")

    def enrich_hits(self, hits: List[Dict[str, Any]], venue: Venue, source_mode: str) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        dois: List[str] = []
        for hit in hits:
            info = hit["info"]
            authors = info.get("authors", {}).get("author", [])
            if isinstance(authors, dict):
                authors = [authors]
            author_names = []
            for author in authors:
                if isinstance(author, dict):
                    author_names.append(author.get("text") or "")
                else:
                    author_names.append(str(author))
            doi = (info.get("doi") or "").lower()
            ee_urls = self.ensure_list(info.get("ee"))
            record = {
                "key": info.get("key", ""),
                "title": self.clean_text(info.get("title", "")).rstrip("."),
                "authors": author_names,
                "venue": info.get("venue"),
                "year": info.get("year"),
                "pages": info.get("pages", ""),
                "doi": doi,
                "doi_url": f"https://doi.org/{doi}" if doi else "",
                "dblp_url": info.get("url", ""),
                "ee_urls": ee_urls,
                "container_title_hint": hit.get("__container_title", ""),
                "container_booktitle_hint": hit.get("__container_booktitle", ""),
                "container_ee_hint": hit.get("__container_ee", []),
            }
            if doi:
                dois.append(doi)
            records.append(record)

        openalex_map: Dict[str, Dict[str, Any]] = {}
        for idx in range(0, len(dois), 25):
            batch = dois[idx : idx + 25]
            openalex_map.update(self.openalex_batch(batch))

        # Resolve official landing pages concurrently.
        unique_doi_urls = sorted({record["doi_url"] for record in records if record["doi_url"]})
        official_map: Dict[str, str] = {}
        if unique_doi_urls:
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
                future_map = {executor.submit(self.http_head_location, doi_url): doi_url for doi_url in unique_doi_urls}
                for future in concurrent.futures.as_completed(future_map):
                    doi_url = future_map[future]
                    try:
                        official_map[doi_url] = future.result()
                    except Exception:
                        official_map[doi_url] = doi_url

        enriched: List[Dict[str, Any]] = []
        for record in records:
            doi = record["doi"]
            oa = openalex_map.get(doi, {})
            abstract = self.rebuild_openalex_abstract(oa.get("abstract_inverted_index") or {})
            summary = self.first_sentence(abstract)
            if not summary:
                summary = f"围绕《{record['title']}》开展研究。"
            combined_text = " ".join([record["title"], abstract])
            tags = self.choose_tags(combined_text)
            official_url = official_map.get(record["doi_url"], record["doi_url"])
            ee_fallback = self.prefer_official_url(record["ee_urls"])
            if not official_url or official_url == record["doi_url"]:
                official_url = ee_fallback or official_url
            container = self.resolve_container_title(record, oa, venue, source_mode)
            bibtex = self.synthesize_bibtex(record, oa, container, venue, source_mode)
            screening = self.classify_screening(record["title"], abstract, tags)
            enriched.append(
                {
                    **record,
                    "official_url": official_url,
                    "abstract": abstract,
                    "summary": summary,
                    "tags": tags,
                    "container_title": container,
                    "bibtex": bibtex,
                    "bibtex_key": self.extract_bibtex_key(bibtex),
                    **screening,
                }
            )
        return enriched

    def resolve_container_title(
        self,
        record: Dict[str, Any],
        openalex_item: Dict[str, Any],
        venue: Venue,
        source_mode: str,
    ) -> str:
        source = ((openalex_item.get("primary_location") or {}).get("source") or {}).get("display_name") or ""
        if source:
            return self.clean_text(source)
        if record.get("container_title_hint"):
            return self.clean_text(record["container_title_hint"])
        if venue.kind == "期刊":
            return venue.full_name
        if source_mode in {"stream_venue", "journal_stream"}:
            label = record.get("venue")
            if isinstance(label, list):
                label = " / ".join(label)
            return self.clean_text(label or venue.abbr)
        if record.get("container_booktitle_hint"):
            return self.clean_text(record["container_booktitle_hint"])
        return f"{venue.abbr} {self.year}"

    @staticmethod
    def bibtex_escape(text: str) -> str:
        return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}").replace('"', '\\"')

    def synthesize_bibtex(
        self,
        record: Dict[str, Any],
        openalex_item: Dict[str, Any],
        container_title: str,
        venue: Venue,
        source_mode: str,
    ) -> str:
        key = "CCF2025:" + re.sub(r"[^A-Za-z0-9:_-]+", "_", record["key"] or record["title"])[:120]
        authors = " and ".join(record["authors"])
        biblio = openalex_item.get("biblio") or {}
        volume = str(biblio.get("volume") or "")
        issue = str(biblio.get("issue") or "")
        first_page = str(biblio.get("first_page") or "")
        last_page = str(biblio.get("last_page") or "")
        pages = record.get("pages") or ""
        if not pages and first_page and last_page:
            pages = f"{first_page}--{last_page}"
        if not pages and first_page:
            pages = first_page

        entry_type = "article" if venue.kind == "期刊" or source_mode == "stream_venue" else "inproceedings"
        fields = [
            f'  title = "{self.bibtex_escape(record["title"])}"',
            f'  author = "{self.bibtex_escape(authors)}"',
            f'  year = "{self.year}"',
        ]
        if entry_type == "article":
            fields.append(f'  journal = "{self.bibtex_escape(container_title)}"')
            if volume:
                fields.append(f'  volume = "{self.bibtex_escape(volume)}"')
            if issue:
                fields.append(f'  number = "{self.bibtex_escape(issue)}"')
        else:
            fields.append(f'  booktitle = "{self.bibtex_escape(container_title)}"')
        if pages:
            fields.append(f'  pages = "{self.bibtex_escape(pages)}"')
        if record.get("doi"):
            fields.append(f'  doi = "{self.bibtex_escape(record["doi"])}"')
            fields.append(f'  url = "{self.bibtex_escape(record["doi_url"])}"')
        elif record.get("official_url"):
            fields.append(f'  url = "{self.bibtex_escape(record["official_url"])}"')
        return "@{entry}{{{key},\n{fields}\n}}".format(entry=entry_type, key=key, fields=",\n".join(fields))

    @staticmethod
    def rebuild_openalex_abstract(inverted_index: Dict[str, List[int]]) -> str:
        if not inverted_index:
            return ""
        max_pos = max(pos for positions in inverted_index.values() for pos in positions)
        words = [""] * (max_pos + 1)
        for word, positions in inverted_index.items():
            for pos in positions:
                words[pos] = word
        return Builder.clean_text(" ".join(words))

    @staticmethod
    def first_sentence(text: str) -> str:
        if not text:
            return ""
        parts = re.split(r"(?<=[.!?。！？])\s+", text.strip())
        if not parts:
            return ""
        sentence = parts[0].strip()
        return sentence[:260]

    @staticmethod
    def extract_bibtex_key(bibtex: str) -> str:
        match = re.search(r"@\w+\{([^,]+),", bibtex)
        return match.group(1) if match else ""

    @staticmethod
    def safe_filename(text: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
        return slug or "venue"

    def venue_stem(self, venue: Venue) -> str:
        kind_token = "conf" if venue.kind == "会议" else "journal"
        return self.safe_filename(f"{venue.abbr}_{kind_token}_{venue.rank}")

    @staticmethod
    def display_abbr(venue: Venue, duplicated: bool) -> str:
        if not duplicated:
            return venue.abbr
        return f"{venue.abbr} / {venue.kind} / {venue.rank}"

    @staticmethod
    def md_escape(text: str) -> str:
        text = text.replace("|", "\\|")
        text = text.replace("\n", " ")
        return text

    def write_venue_files(self, venue: Venue, payload: Dict[str, Any]) -> Dict[str, str]:
        stem = self.venue_stem(venue)
        metadata_path = self.metadata_dir / f"{stem}.json"
        bib_path = self.bib_dir / f"{stem}.bib"
        metadata_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        bib_text = "\n\n".join(entry["bibtex"].strip() for entry in payload["papers"])
        if bib_text:
            bib_text += "\n"
        bib_path.write_text(bib_text, encoding="utf-8")
        return {
            "metadata": metadata_path.relative_to(self.target_dir).as_posix(),
            "bib": bib_path.relative_to(self.target_dir).as_posix(),
        }

    def build(self) -> Dict[str, Any]:
        self.ensure_dirs()
        venues = self.parse_ccf_venues()
        all_payloads: List[Dict[str, Any]] = []
        verification: Dict[str, Any] = {"year": self.year, "venues": []}

        for venue in venues:
            print(f"[build] {venue.abbr}", file=sys.stderr)
            collected = self.collect_entries_for_venue(venue)
            enriched = self.enrich_hits(collected["hits"], venue, collected["mode"])
            enriched.sort(key=lambda item: (item["title"].lower(), item["key"]))

            files = self.write_venue_files(
                venue,
                {
                    "venue": venue.__dict__,
                    "source": {
                        "mode": collected["mode"],
                        "query": collected["source_query"],
                        "expected_total": collected["expected_total"],
                        "key_pages": collected["key_pages"],
                    },
                    "papers": enriched,
                },
            )

            payload = {
                "venue": venue,
                "mode": collected["mode"],
                "expected_total": collected["expected_total"],
                "actual_total": len(enriched),
                "key_pages": collected["key_pages"],
                "papers": enriched,
                "files": files,
            }
            all_payloads.append(payload)
            verification["venues"].append(
                {
                    "abbr": venue.abbr,
                    "full_name": venue.full_name,
                    "rank": venue.rank,
                    "kind": venue.kind,
                    "mode": collected["mode"],
                    "expected_total": collected["expected_total"],
                    "actual_total": len(enriched),
                    "status": "ok" if collected["expected_total"] == len(enriched) else "mismatch",
                    "files": files,
                }
            )

        verification["total_expected"] = sum(item["expected_total"] for item in all_payloads)
        verification["total_actual"] = sum(item["actual_total"] for item in all_payloads)
        verification_path = self.target_dir / "verification.json"
        verification_path.write_text(json.dumps(verification, ensure_ascii=False, indent=2), encoding="utf-8")

        readme_text = self.render_readme(all_payloads, verification)
        (self.target_dir / "README.md").write_text(readme_text, encoding="utf-8")
        return verification

    def render_readme(self, payloads: List[Dict[str, Any]], verification: Dict[str, Any]) -> str:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        venue_count = len(payloads)
        total_papers = verification["total_actual"]
        abbr_counts = Counter(payload["venue"].abbr for payload in payloads)

        rank_kind_counts: Dict[tuple[str, str], int] = Counter()
        for payload in payloads:
            rank_kind_counts[(payload["venue"].rank, payload["venue"].kind)] += payload["actual_total"]

        lines: List[str] = []
        lines.append(f"# `{self.year}` 年度汇总")
        lines.append("")
        lines.append("## 1. 年份说明")
        lines.append("")
        lines.append(f"- 年份：`{self.year}`")
        lines.append("- 覆盖范围：`CCF` 软件工程/系统软件/程序设计语言方向 `A/B/C` 类期刊会议")
        lines.append(f"- 当前覆盖的 venue 数量：`{venue_count}`")
        lines.append(f"- 当前已入表论文数量：`{total_papers}`")
        lines.append(f"- 更新时间：`{ts}`")
        lines.append("- 说明：本页由 `tools/ccf_se_index_builder.py` 自动生成，并以逐 venue 计数复核结果为准。")
        lines.append("")
        lines.append("## 2. 年度汇总统计")
        lines.append("")
        for rank in ["A", "B", "C"]:
            for kind in ["会议", "期刊"]:
                lines.append(f"- {rank} 类{kind}：`{rank_kind_counts.get((rank, kind), 0)}`")
        lines.append(f"- 期望总条目数：`{verification['total_expected']}`")
        lines.append(f"- 实际总条目数：`{verification['total_actual']}`")
        lines.append("")
        lines.append("## 3. 覆盖 venue 列表")
        lines.append("")
        lines.append("| venue | 全称 | 等级 | 类型 | 论文数 | 数据文件 | 备注 |")
        lines.append("|---|---|---|---|---:|---|---|")
        for payload in payloads:
            venue = payload["venue"]
            files = payload["files"]
            note = "计数一致" if payload["expected_total"] == payload["actual_total"] else "计数需复核"
            display_abbr = self.display_abbr(venue, abbr_counts[venue.abbr] > 1)
            lines.append(
                "| `{abbr}` | {full} | `{rank}` | `{kind}` | {count} | [metadata]({meta}) / [bib]({bib}) | {note} |".format(
                    abbr=self.md_escape(display_abbr),
                    full=self.md_escape(venue.full_name),
                    rank=venue.rank,
                    kind=venue.kind,
                    count=payload["actual_total"],
                    meta=self.md_escape(files["metadata"]),
                    bib=self.md_escape(files["bib"]),
                    note=note,
                )
            )
        lines.append("")
        lines.append("## 4. Venue Sections")
        lines.append("")

        for payload in payloads:
            venue = payload["venue"]
            key_pages = payload["key_pages"]
            files = payload["files"]
            display_abbr = self.display_abbr(venue, abbr_counts[venue.abbr] > 1)
            lines.append("---")
            lines.append("")
            lines.append(f"## `{display_abbr}`")
            lines.append("")
            lines.append("### 4.1 基本信息")
            lines.append("")
            lines.append(f"- 全称：{venue.full_name}")
            lines.append(f"- `CCF` 等级：`{venue.rank}`")
            lines.append(f"- 类型：`{venue.kind}`")
            lines.append(f"- 年份：`{self.year}`")
            lines.append(f"- 条目数：`{payload['actual_total']}`")
            lines.append(f"- 数据文件：[metadata]({files['metadata']}) / [bib]({files['bib']})")
            lines.append("")
            lines.append("### 4.2 关键信息页面")
            lines.append("")
            if venue.kind == "期刊":
                homepage = key_pages.get("journal_homepage") or "待补"
                lines.append(f"- 期刊主页：{homepage}")
                lines.append(f"- 学术索引页：{venue.index_url}")
                lines.append("- 2025 年官方 article page：见下表 `官方落地页` 列")
            else:
                homepage = key_pages.get("homepage") or "待补"
                lines.append(f"- 年主页：{homepage}")
                lines.append(f"- 学术索引页：{venue.index_url}")
                carrier = key_pages.get("carrier_homepage")
                if carrier:
                    lines.append(f"- 正式发布载体页：{carrier}")
                procs = key_pages.get("proceedings_pages") or []
                if procs:
                    joined = " / ".join(procs[:3])
                    lines.append(f"- 官方论文集页：{joined}")
                if key_pages.get("note"):
                    lines.append(f"- 说明：{key_pages['note']}")
                lines.append("- `CFP`：待补")
            lines.append("")
            lines.append("### 4.3 论文名录")
            lines.append("")
            lines.append("- 说明：完整摘要、初筛理由与可直接引用的完整 `BibTeX` 已写入对应 `metadata` / `bib` 文件。")
            lines.append("")
            lines.append("| 序号 | 标题 | 作者 | 一句话说明 | DOI | 官方落地页 | 方向标签 | 初筛 | `PDF` 跟进 | `BibTeX` key | 备注 |")
            lines.append("|---|---|---|---|---|---|---|---|---|---|---|")
            for idx, paper in enumerate(payload["papers"], start=1):
                authors = ", ".join(paper["authors"])
                tags = " / ".join(paper["tags"])
                doi_cell = f"[{paper['doi']}](https://doi.org/{paper['doi']})" if paper["doi"] else ""
                official_cell = f"[link]({paper['official_url']})" if paper["official_url"] else ""
                lines.append(
                    "| {idx} | {title} | {authors} | {summary} | {doi} | {official} | {tags} | {screening} | {pdf} | `{bib}` | {note} |".format(
                        idx=idx,
                        title=self.md_escape(paper["title"]),
                        authors=self.md_escape(authors),
                        summary=self.md_escape(paper["summary"]),
                        doi=doi_cell,
                        official=official_cell,
                        tags=self.md_escape(tags),
                        screening=self.md_escape(paper["initial_screening"]),
                        pdf=self.md_escape(paper["pdf_followup"]),
                        bib=self.md_escape(paper["bibtex_key"] or paper["key"]),
                        note="",
                    )
                )
            lines.append("")
            lines.append("### 4.4 本 venue 年度观察")
            lines.append("")
            if payload["papers"]:
                common_tags = Counter(tag for paper in payload["papers"] for tag in paper["tags"]).most_common(5)
                tag_text = " / ".join(f"{name} ({count})" for name, count in common_tags)
                screening_counts = Counter(paper["initial_screening"] for paper in payload["papers"])
                green_titles = [
                    f"`{paper['title']}`"
                    for paper in payload["papers"]
                    if paper["initial_screening"] == "🟢 优先跟进"
                ][:5]
                lines.append(f"- 主题倾向：{tag_text}")
                lines.append(
                    "- 初筛分布："
                    + " / ".join(f"{name} ({count})" for name, count in screening_counts.most_common())
                )
                lines.append("- 与博士研究的相关性：请结合 `一句话说明`、`方向标签` 与伴随 `metadata` 文件中的摘要进一步判断。")
                if green_titles:
                    lines.append("- 建议优先获取 `PDF` 的论文：" + "；".join(green_titles))
            else:
                lines.append("- 主题倾向：本年度未检出直接归属该 venue 的主论文条目。")
                lines.append("- 与博士研究的相关性：无。")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## 5. 本年度总体观察")
        lines.append("")
        top_tags = Counter(tag for payload in payloads for paper in payload["papers"] for tag in paper["tags"]).most_common(12)
        screening_totals = Counter(
            paper["initial_screening"] for payload in payloads for paper in payload["papers"]
        )
        if top_tags:
            lines.append("- 高频方向标签：" + " / ".join(f"{tag} ({count})" for tag, count in top_tags))
        if screening_totals:
            lines.append("- 初筛分布：" + " / ".join(f"{tag} ({count})" for tag, count in screening_totals.most_common()))
        lines.append("- 复核状态：以 [verification.json](./verification.json) 为准；默认要求 `expected_total == actual_total`。")
        lines.append("- 后续若需继续扩年份，优先参考 [../README.md](../README.md) 与 `tools/ccf_se_index_builder.py`。")
        lines.append("")
        return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build yearly CCF SE venue index.")
    parser.add_argument("--year", type=int, required=True, help="Target year, e.g. 2025")
    parser.add_argument(
        "--target-dir",
        type=Path,
        default=None,
        help="Output directory. Defaults to frontier_index/ccf_history/<year>/",
    )
    args = parser.parse_args()

    target_dir = args.target_dir or (ROOT / "frontier_index" / "ccf_history" / str(args.year))
    builder = Builder(year=args.year, target_dir=target_dir)
    verification = builder.build()
    ok = verification["total_expected"] == verification["total_actual"] and all(
        item["status"] == "ok" for item in verification["venues"]
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
