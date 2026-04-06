#!/usr/bin/env python3
"""Build venue submission timeline notes for frontier_index/ccf_history.

This tool maintains a companion document for the retained CCF SE venues:

1. conference venues: best-effort 2021-2025 submission milestones
2. journal venues: regular submission rhythm / rolling-review notes

Source priority:
1. official archived dates pages on `conf.researchr.org`
2. official venue / series pages for special cases
3. `WikiCFP` fallback when official yearly archives are not easy to recover
"""

from __future__ import annotations

import argparse
import io
import json
import re
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser


ROOT = Path(__file__).resolve().parent.parent
YEAR_DIR = ROOT / "frontier_index" / "ccf_history" / "2025"
METADATA_DIR = YEAR_DIR / "metadata"
YEAR_README = YEAR_DIR / "README.md"
OUTPUT_MD = ROOT / "frontier_index" / "ccf_history" / "SUBMISSION_TIMELINES.md"
YEARS = [2025, 2024, 2023, 2022, 2021]

USER_AGENT = "Mozilla/5.0 (compatible; Codex timeline builder)"
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": USER_AGENT})


@dataclass(frozen=True)
class VenueRecord:
    stem: str
    abbr: str
    full_name: str
    rank: str
    kind: str
    index_url: str


@dataclass
class TimelineEntry:
    year: int
    abstract_deadline: str = "未检出"
    submission_deadline: str = "未检出"
    rebuttal_window: str = "未检出公开作者回应窗口"
    notification: str = "未检出"
    camera_ready: str = "未检出"
    conference_dates: str = "未检出"
    source_label: str = "待补"
    source_url: str = ""
    homepage_url: str = ""
    notes: str = ""


RESEARCHR_CONFIG: Dict[str, Dict[str, object]] = {
    "apsec_conf_c": {"slug": "apsec", "track_patterns": [r"^Technical Track$"]},
    "ase_conf_a": {"slug": "ase", "track_patterns": [r"^Research Papers$"]},
    "ease_conf_c": {
        "slug": "ease",
        "track_patterns": [r"^Research Papers$", r"^Research \(Full Papers\)$", r"^Research$"],
    },
    "ecoop_conf_b": {
        "slug": "ecoop",
        "track_patterns": [r"^Technical Papers$", r"^Research Papers$", r"^ECOOP Technical Papers$"],
    },
    "esem_conf_b": {
        "slug": "esem",
        "track_patterns": [r"^ESEM - Technical Track$", r"^ESEM Technical Papers$", r"^Technical Papers$"],
    },
    "fse_conf_a": {"slug": "fse", "track_patterns": [r"^Research Papers$"]},
    "icpc_conf_b": {"slug": "icpc", "track_patterns": [r"^Research Track$", r"^Research$"]},
    "icse_conf_a": {"slug": "icse", "track_patterns": [r"^Research Track$", r"^Technical Track$", r"^Technical Papers$"]},
    "icsme_conf_b": {"slug": "icsme", "track_patterns": [r"^Research Papers Track$", r"^Research Track$", r"^Research Papers$"]},
    "icsr_conf_c": {"slug": "icsr", "track_patterns": [r"^ICSR$"]},
    "icst_conf_c": {"slug": "icst", "track_patterns": [r"^Research Papers$"]},
    "internetware_conf_c": {"slug": "internetware", "track_patterns": [r"^Research Track$", r"^Main Track$"]},
    "issta_conf_a": {"slug": "issta", "track_patterns": [r"^Research Papers$", r"^Technical Papers$"]},
    "models_conf_b": {"slug": "models", "track_patterns": [r"^Research Papers$", r"^Technical Track$", r"^Technical Papers$", r"^MODELS$"]},
    "msr_conf_c": {"slug": "msr", "track_patterns": [r"^Technical Papers$"]},
    "pldi_conf_a": {"slug": "pldi", "track_patterns": [r"^PLDI Research Papers$", r"^PLDI$"]},
    "re_conf_b": {"slug": "re", "track_patterns": [r"^Research Papers$"]},
    "refsq_conf_c": {"slug": "refsq", "track_patterns": [r"^Research Track$", r"^Research Papers$"]},
    "saner_conf_b": {"slug": "saner", "track_patterns": [r"^Research Papers$"]},
    "scam_conf_c": {"slug": "scam", "track_patterns": [r"^Research Track$", r"^Research Papers$"]},
    "vmcai_conf_b": {"slug": "vmcai", "track_patterns": [r"^VMCAI(?:\s+\d{4})?$"]},
}


WIKICFP_CONFIG: Dict[str, Dict[str, object]] = {
    "caise_conf_b": {
        "query": "CAiSE",
        "title_patterns": [r"^CAiSE\s+{year}$"],
    },
    "fm_conf_a": {
        "query": "FM",
        "title_patterns": [r"^FM\s+{year}$"],
    },
    "iceccs_conf_c": {
        "query": "ICECCS",
        "title_patterns": [r"^ICECCS\s+{year}$"],
    },
    "icfem_conf_c": {
        "query": "ICFEM",
        "title_patterns": [r"^ICFEM\s+{year}$"],
    },
    "icsoc_conf_b": {
        "query": "ICSOC",
        "title_patterns": [r"^ICSOC\s+{year}$"],
    },
    "icws_conf_b": {
        "query": "ICWS web services",
        "title_patterns": [r"^ICWS\s+{year}$"],
    },
    "issre_conf_b": {
        "query": "ISSRE",
        "title_patterns": [r"^ISSRE\s+{year}$"],
    },
    "oopsla_conf_a": {
        "query": "OOPSLA",
        "title_patterns": [
            r"^OOPSLA.*{year}$",
        ],
        "multi_page": True,
    },
    "qrs_conf_c": {
        "query": "QRS",
        "title_patterns": [r"^QRS\s+{year}$"],
    },
    "rv_conf_c": {
        "query": "RV runtime verification",
        "title_patterns": [r"^RV\s+{year}$"],
    },
    "seke_conf_c": {
        "query": "SEKE",
        "title_patterns": [r"^SEKE\s+{year}$"],
    },
    "saner_conf_b": {
        "query": "SANER",
        "title_patterns": [r"^SANER\s+{year}$"],
    },
    "scam_conf_c": {
        "query": "SCAM",
        "title_patterns": [r"^SCAM\s+{year}$"],
    },
    "icsr_conf_c": {
        "query": "ICSR",
        "title_patterns": [r"^ICSR\s+{year}$"],
    },
    "spin_conf_c": {
        "query": "SPIN conference",
        "title_patterns": [r"^SPIN\s+{year}$"],
    },
    "tase_conf_c": {
        "query": "TASE",
        "title_patterns": [r"^TASE\s+{year}$"],
    },
}


MANUAL_CONFERENCE_NOTES: Dict[str, Dict[int, Dict[str, str]]] = {
    "fm_conf_a": {
        2025: {
            "notes": "截至 `2026-04-06` 未检出 `FM 2025` standalone 主会次；当前可公开核对的相邻主会次为 `FM 2024` 与 `FM 2026`。",
            "homepage_url": "未检出 standalone 2025 年主页",
            "source_label": "FME series observation",
            "source_url": "https://www.fmeurope.org/",
        },
        2022: {
            "notes": "当前未检出 `FM 2022` standalone 主会次；当前公开主会次序列在该窗口内可核对到 `FM 2021` 与 `FM 2023`。",
            "homepage_url": "未检出 standalone 2022 年主页",
            "source_label": "FME series observation",
            "source_url": "https://www.fmeurope.org/",
        },
    },
    "compsac_conf_c": {
        year: {
            "notes": "官方 `COMPSAC` 采用多 symposium / workshop 并行征稿，单年内部 deadline 并不完全统一；应以当年总 CFP 与目标 symposium 页面为准。",
        }
        for year in YEARS
    },
    "icsr_conf_c": {
        2023: {
            "notes": "当前未检出 `ICSR 2023` standalone 主会次；当前公开可核对的近邻主会次为 `ICSR 2022`、`ICSR 2024` 与 `ICSR 2025`。",
            "homepage_url": "未检出 standalone 2023 年主页",
            "source_label": "ICSR series cadence",
            "source_url": "https://dblp.org/db/conf/icsr/index.html",
        },
        2021: {
            "notes": "当前未检出 `ICSR 2021` standalone 主会次；当前公开可核对的近邻主会次为 `ICSR 2020`、`ICSR 2022` 与 `ICSR 2024`。",
            "homepage_url": "未检出 standalone 2021 年主页",
            "source_label": "ICSR series cadence",
            "source_url": "https://dblp.org/db/conf/icsr/index.html",
        },
    },
    "paste_conf_c": {
        year: {
            "notes": "未检出 `2021-2025` 的独立 `PASTE` CFP / dates 归档；`DBLP` series 页显示该系列为历史 workshop，当前窗口内未见稳定独立举办。",
            "source_label": "DBLP series",
            "source_url": "https://dblp.org/db/conf/paste/index.html",
            "homepage_url": "无近 5 年 standalone 年主页",
        }
        for year in YEARS
    },
    "sse_conf_c": {
        year: {
            "notes": "当前未稳定检出可公开核对的近 `5` 年独立 CFP 归档；该 venue 建议优先通过 IEEE 服务计算系列主页与当年 CFP 聚合页确认。",
            "source_label": "IEEE SCC series",
            "source_url": "https://ieee-scc.org/",
        }
        for year in YEARS
    },
    "tase_conf_c": {
        year: {
            "notes": "当前未稳定检出完整近 `5` 年公开归档；投稿前需优先核对当年官方 CFP 页。",
        }
        for year in YEARS
    },
    "wicsa_conf_c": {
        year: {
            "notes": "官方 `ICSA` history 页表明 `WICSA` 已并入 `ICSA` 系列；`2021-2025` 未见 standalone `WICSA` CFP，应改跟踪 `ICSA`。",
            "source_label": "ICSA/WICSA history",
            "source_url": "https://2024.ieee-icsa.org/history/",
            "homepage_url": "已并入 ICSA，请改跟踪 ICSA 年主页",
        }
        for year in YEARS
    },
}


MANUAL_CONFERENCE_ROWS: Dict[str, Dict[int, Dict[str, str]]] = {
    "compsac_conf_c": {
        2025: {
            "homepage_url": "https://ieeecompsac.computer.org/2025/",
            "submission_deadline": "2025-03-05 23:59",
            "notification": "2025-04-17 23:59",
            "camera_ready": "2025-06-01 23:59",
            "conference_dates": "2025-07-08 00:00 ~ 2025-07-11 23:59",
            "source_label": "Official CFP",
            "source_url": "https://ieeecompsac.computer.org/2025/call-for-papers/",
            "notes": "按 `full symposium papers` 最终延长期限整理。",
        },
        2024: {
            "homepage_url": "https://ieeecompsac.computer.org/2024/",
            "submission_deadline": "2024-02-28 23:59",
            "notification": "2024-04-14 23:59",
            "camera_ready": "2024-05-25 23:59",
            "conference_dates": "2024-07-02 00:00 ~ 2024-07-04 23:59",
            "source_label": "Official symposia page",
            "source_url": "https://ieeecompsac.computer.org/2024/symposia/",
            "notes": "按 `Important Dates – Symposia` 的最终延长期限整理。",
        },
        2023: {
            "homepage_url": "https://ieeecompsac.computer.org/2023/",
            "submission_deadline": "2023-02-15 23:59",
            "notification": "2023-04-07 23:59",
            "camera_ready": "2023-05-18 23:59",
            "conference_dates": "2023-06-26 00:00 ~ 2023-06-30 23:59",
            "source_label": "Official CFP",
            "source_url": "https://ieeecompsac.computer.org/2023/call-for-papers/",
            "notes": "按 `Main conference/symposium` 最终延长期限整理。",
        },
        2022: {
            "homepage_url": "https://ieeecompsac.computer.org/2022/",
            "submission_deadline": "2022-02-18 23:59",
            "notification": "2022-04-01 23:59",
            "camera_ready": "2022-05-15 23:59",
            "conference_dates": "2022-06-27 00:00 ~ 2022-07-01 23:59",
            "source_label": "Official important dates",
            "source_url": "https://ieeecompsac.computer.org/2022/important-dates/",
            "notes": "按 `Main conference papers` 最终延长期限整理；会期来自当年官方 program/virtual conference 资料。",
        },
        2021: {
            "homepage_url": "https://ieeecompsac.computer.org/2021/",
            "submission_deadline": "2021-02-18 23:59",
            "notification": "2021-04-15 23:59",
            "camera_ready": "2021-05-31 23:59",
            "conference_dates": "2021-07-12 00:00 ~ 2021-07-16 23:59",
            "source_label": "Official important dates",
            "source_url": "https://ieeecompsac.computer.org/2021/important-dates/",
            "notes": "按 `Main conference papers` 更新后的主会口径整理。",
        },
    },
    "caise_conf_b": {
        2025: {
            "homepage_url": "https://conferences.big.tuwien.ac.at/caise2025/",
            "abstract_deadline": "2024-11-30 19:59",
            "submission_deadline": "2024-12-07 19:59",
            "notification": "2025-02-28 23:59",
            "camera_ready": "2025-04-14 23:59",
            "conference_dates": "2025-06-16 00:00 ~ 2025-06-20 23:59",
            "source_label": "Official CFP",
            "source_url": "https://conferences.big.tuwien.ac.at/caise2025/cfp_full.php",
            "notes": "摘要/投稿原文标为 `AoE`，已换算为北京时间。",
        },
        2021: {
            "homepage_url": "https://caise21.org/",
            "abstract_deadline": "2020-12-01 23:59",
            "submission_deadline": "2020-12-08 23:59",
            "notification": "2021-02-25 23:59",
            "camera_ready": "2021-03-19 23:59",
            "conference_dates": "2021-06-28 00:00 ~ 2021-07-02 23:59",
            "source_label": "OpenResearch",
            "source_url": "https://www.openresearch.org/wiki/CAiSE_2021",
            "notes": "OpenResearch 汇总页可直接核对该年主页与重要日期。",
        },
    },
    "ease_conf_c": {
        2022: {
            "homepage_url": "https://conf.researchr.org/home/ease-2022",
            "abstract_deadline": "2022-01-24 23:59",
            "submission_deadline": "2022-01-31 23:59",
            "notification": "2022-03-14 23:59",
            "camera_ready": "2022-04-24 23:59",
            "conference_dates": "2022-06-13 00:00 ~ 2022-06-15 23:59",
            "source_label": "EasyChair CFP",
            "source_url": "https://easychair.org/cfp/ease22",
            "notes": "按 full papers 研究主轨口径整理。",
        },
        2021: {
            "homepage_url": "https://www.ntnu.edu/ease2021",
            "abstract_deadline": "2021-03-05 23:59",
            "submission_deadline": "2021-03-12 23:59",
            "notification": "2021-04-19 23:59",
            "camera_ready": "2021-04-30 23:59",
            "conference_dates": "2021-06-21 00:00 ~ 2021-06-23 23:59",
            "source_label": "EasyChair CFP",
            "source_url": "https://easychair.org/cfp/EASE2021",
            "notes": "按 full research track 口径整理。",
        },
    },
    "icsme_conf_b": {
        2022: {
            "homepage_url": "https://cyprusconferences.org/icsme2022/",
            "abstract_deadline": "2022-03-26 19:59",
            "submission_deadline": "2022-04-02 19:59",
            "notification": "2022-06-11 19:59",
            "camera_ready": "2022-07-02 19:59",
            "conference_dates": "2022-10-03 00:00 ~ 2022-10-07 23:59",
            "source_label": "EasyChair CFP",
            "source_url": "https://easychair.org/cfp/ICSME2022",
            "notes": "摘要/投稿/通知/终稿原文标为 `23:59 AoE`，已换算为北京时间。",
        },
        2021: {
            "homepage_url": "https://icsme2021.github.io/",
            "abstract_deadline": "2021-04-27 19:59",
            "submission_deadline": "2021-04-30 19:59",
            "notification": "2021-06-15 19:59",
            "camera_ready": "2021-07-31 19:59",
            "conference_dates": "2021-09-27 00:00 ~ 2021-10-01 23:59",
            "source_label": "Official important dates",
            "source_url": "https://icsme2021.github.io/cfp/ImportantDates.html",
            "notes": "Research Track 原文标为 `23:59 AoE`，已换算为北京时间。",
        },
    },
    "icse_conf_a": {
        2025: {
            "homepage_url": "https://conf.researchr.org/home/icse-2025",
            "abstract_deadline": "R1 2024-03-15 23:59；R2 2024-07-26 23:59",
            "submission_deadline": "R1 2024-03-22 23:59；R2 2024-08-02 23:59",
            "rebuttal_window": "R1 2024-06-10 00:00 ~ 2024-06-13 23:59；R2 2024-10-07 00:00 ~ 2024-10-10 23:59",
            "notification": "初轮 R1 2024-07-05 23:59；初轮 R2 2024-11-01 23:59；最终 R1 2024-11-01 23:59；最终 R2 2025-01-22 23:59",
            "camera_ready": "R1 2024-08-16 23:59；R1 大修 2024-12-13 23:59；R2 大修 2025-02-12 23:59",
            "source_label": "Official dates page",
            "source_url": "https://conf.researchr.org/dates/icse-2025",
            "notes": "按官方 `Research Track` 两轮制主流程整理。",
        },
    },
    "icfem_conf_c": {
        2025: {
            "homepage_url": "https://icfem2025.github.io/",
            "abstract_deadline": "2025-06-12 19:59",
            "submission_deadline": "2025-07-21 19:59",
            "notification": "2025-08-02 19:59",
            "camera_ready": "2025-08-31 19:59",
            "conference_dates": "2025-11-10 00:00 ~ 2025-11-13 23:59",
            "source_label": "Official homepage",
            "source_url": "https://icfem2025.github.io/",
            "notes": "重要日期原文标为 `23:59 AoE`，按最终延长期限换算为北京时间。",
        },
        2021: {
            "homepage_url": "未检出 standalone 2021 年主页",
            "source_label": "ICFEM 2020 official page",
            "source_url": "https://formal-analysis.com/icfem/2020/",
            "notes": "当前未检出 `ICFEM 2021` standalone edition；`2021` 年实际公开举办的是延期后的 `ICFEM 2020`，因此不将其作为 `2021` edition 年主页。",
        },
    },
    "icssp_conf_c": {
        2025: {
            "homepage_url": "未检出独立 2025 年主页",
            "source_label": "ISSPA series events",
            "source_url": "https://isspa-process.org/events/",
            "notes": "官方 `ISSPA` events 页当前未给出 `2025` 年独立 `ICSSP` 事件条目；投稿前需先核对 series 页是否补发当年会议信息。",
        },
        2024: {
            "homepage_url": "https://icssp2024.events.isspa-process.org/",
            "submission_deadline": "2024-03-29 23:59",
            "notification": "2024-05-07 23:59",
            "camera_ready": "2024-06-14 23:59",
            "conference_dates": "2024-09-04 00:00 ~ 2024-09-06 23:59",
            "source_label": "Official important dates",
            "source_url": "https://icssp2024.events.isspa-process.org/important-dates/",
            "notes": "按官方 `important dates` 页中的最终延长期限整理。",
        },
        2023: {
            "homepage_url": "https://conf.researchr.org/home/icssp-2023",
            "abstract_deadline": "2023-01-06 23:59",
            "submission_deadline": "2023-01-20 23:59",
            "notification": "2023-02-21 23:59",
            "camera_ready": "2023-03-27 23:59",
            "conference_dates": "2023-05-14 00:00 ~ 2023-05-15 23:59",
            "source_label": "Official dates page",
            "source_url": "https://conf.researchr.org/dates/icssp-2023",
        },
        2022: {
            "homepage_url": "https://isspa-process.org/event/icssp-icgse-2022-virtual-event-pittsburgh-pa-usa-virtual/",
            "conference_dates": "2022-05-19 00:00 ~ 2022-05-20 23:59",
            "source_label": "ISSPA event page",
            "source_url": "https://isspa-process.org/event/icssp-icgse-2022-virtual-event-pittsburgh-pa-usa-virtual/",
            "notes": "当前仅稳定检出该年官方 event page 与会期，未稳定检出可公开核对的独立 CFP / important-dates 归档页。",
        },
        2021: {
            "homepage_url": "https://conf.researchr.org/home/icssp-icgse-2021",
            "abstract_deadline": "2021-01-05 23:59",
            "submission_deadline": "2021-01-19 23:59",
            "notification": "2021-02-22 23:59",
            "camera_ready": "2021-03-22 23:59",
            "conference_dates": "2021-05-18 00:00 ~ 2021-05-19 23:59",
            "source_label": "Official dates page",
            "source_url": "https://conf.researchr.org/dates/icssp-icgse-2021",
        },
    },
    "oopsla_conf_a": {
        2025: {
            "homepage_url": "https://2025.splashcon.org/track/oopsla",
            "submission_deadline": "R1 2024-10-16 19:59；R2 2025-03-26 19:59",
            "rebuttal_window": "R1 2024-12-03 20:00 ~ 2024-12-07 19:59；R2 2025-05-26 20:00 ~ 2025-05-30 19:59",
            "notification": "R1 2024-12-19 19:59；R2 2025-06-19 19:59；大修 R1 2025-02-19 19:59；大修 R2 2025-08-13 19:59",
            "camera_ready": "R1 2025-03-01 19:59；R2 2025-08-23 19:59",
            "conference_dates": "2025-10-12 00:00 ~ 2025-10-18 23:59",
            "source_label": "Official track page",
            "source_url": "https://2025.splashcon.org/track/oopsla",
            "notes": "重要日期原文标为 `AoE`，已换算为北京时间。",
        },
        2024: {
            "homepage_url": "https://2024.splashcon.org/track/splash-2024-oopsla",
            "submission_deadline": "R1 2023-10-21 19:59；R2 2024-04-06 19:59",
            "rebuttal_window": "R1 2023-12-11 20:00 ~ 2023-12-14 19:59；R2 2024-06-03 20:00 ~ 2024-06-06 19:59",
            "notification": "R1 2023-12-23 19:59；R2 2024-06-22 19:59；大修 R1 2024-02-25 19:59；大修 R2 2024-08-19 19:59",
            "camera_ready": "R1 2024-03-09 19:59；R2 2024-09-02 19:59",
            "conference_dates": "2024-10-20 00:00 ~ 2024-10-25 23:59",
            "source_label": "Official track page",
            "source_url": "https://2024.splashcon.org/track/splash-2024-oopsla",
            "notes": "重要日期原文标为 `AoE`，已换算为北京时间。",
        },
        2023: {
            "homepage_url": "https://2023.splashcon.org/track/splash-2023-oopsla",
            "submission_deadline": "R1 2022-10-29 19:59；R2 2023-04-15 19:59",
            "rebuttal_window": "R1 2022-12-12 20:00 ~ 2022-12-15 19:59；R2 2023-06-14 20:00 ~ 2023-06-17 19:59",
            "notification": "R1 2022-12-24 19:59；R2 2023-07-01 19:59；大修 R1 2023-02-26 19:59；大修 R2 2023-08-28 19:59",
            "camera_ready": "R1 2023-03-11 19:59；R2 2023-09-11 19:59",
            "conference_dates": "2023-10-22 00:00 ~ 2023-10-27 23:59",
            "source_label": "Official track page",
            "source_url": "https://2023.splashcon.org/track/splash-2023-oopsla",
            "notes": "重要日期原文标为 `AoE`，已换算为北京时间。",
        },
        2022: {
            "homepage_url": "https://2022.splashcon.org/track/splash-2022-oopsla",
            "submission_deadline": "R1 2021-10-13 19:59；R2 2022-04-16 19:59",
            "rebuttal_window": "R1 2021-12-01 08:00 ~ 2021-12-04 08:00；R2 2022-06-12 20:00 ~ 2022-06-17 19:59",
            "notification": "初轮 R1 2021-12-17 19:59；初轮 R2 2022-07-01 19:59；最终 R1 2022-02-26 19:59；最终 R2 2022-09-02 19:59",
            "camera_ready": "R1 2022-03-12 19:59；R2 2022-09-17 19:59",
            "conference_dates": "2022-12-05 00:00 ~ 2022-12-10 23:59",
            "source_label": "Official track page",
            "source_url": "https://2022.splashcon.org/track/splash-2022-oopsla",
            "notes": "重要日期原文标为 `AoE`，已换算为北京时间。",
        },
        2021: {
            "homepage_url": "https://2021.splashcon.org/track/splash-2021-oopsla",
            "submission_deadline": "R1 2021-04-17 19:59；R2 2021-08-14 19:59",
            "rebuttal_window": "2021-06-14 20:00 ~ 2021-06-17 19:59",
            "notification": "初轮 2021-07-03 19:59；最终 2021-08-31 19:59",
            "camera_ready": "2021-09-14 19:59",
            "conference_dates": "2021-10-17 00:00 ~ 2021-10-22 23:59",
            "source_label": "Official track page",
            "source_url": "https://2021.splashcon.org/track/splash-2021-oopsla",
            "notes": "重要日期原文标为 `AoE`，已换算为北京时间。",
        },
    },
}


DEFAULT_JOURNAL_NOTE = "常规稿默认全年滚动投稿；通常不存在 conference 式公开 rebuttal 窗口；若当年有专题/专刊，则以当年 special issue CFP 为准。"

BJT = timezone(timedelta(hours=8))
EXPLICIT_TZ_OFFSETS = {
    "AOE": timezone(timedelta(hours=-12)),
    "UTC": timezone.utc,
    "UTC-12": timezone(timedelta(hours=-12)),
    "UTC-11": timezone(timedelta(hours=-11)),
    "UTC-10": timezone(timedelta(hours=-10)),
    "UTC-09": timezone(timedelta(hours=-9)),
    "UTC-08": timezone(timedelta(hours=-8)),
    "UTC-07": timezone(timedelta(hours=-7)),
    "UTC-06": timezone(timedelta(hours=-6)),
    "UTC-05": timezone(timedelta(hours=-5)),
    "UTC-04": timezone(timedelta(hours=-4)),
    "UTC-03": timezone(timedelta(hours=-3)),
    "UTC-02": timezone(timedelta(hours=-2)),
    "UTC-01": timezone(timedelta(hours=-1)),
    "UTC+00": timezone.utc,
    "UTC+01": timezone(timedelta(hours=1)),
    "UTC+02": timezone(timedelta(hours=2)),
    "UTC+03": timezone(timedelta(hours=3)),
    "UTC+04": timezone(timedelta(hours=4)),
    "UTC+05": timezone(timedelta(hours=5)),
    "UTC+06": timezone(timedelta(hours=6)),
    "UTC+07": timezone(timedelta(hours=7)),
    "UTC+08": timezone(timedelta(hours=8)),
    "UTC+09": timezone(timedelta(hours=9)),
    "UTC+10": timezone(timedelta(hours=10)),
    "UTC+11": timezone(timedelta(hours=11)),
    "UTC+12": timezone(timedelta(hours=12)),
}

FIELD_DEFAULTS = {
    "abstract_deadline": "未检出",
    "submission_deadline": "未检出",
    "rebuttal_window": "未检出公开作者回应窗口",
    "notification": "未检出",
    "camera_ready": "未检出",
    "conference_dates": "未检出",
}


def format_dt_bjt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def format_now_bjt() -> str:
    return datetime.now(BJT).strftime("%Y-%m-%d %H:%M")


def strip_weekday_prefix(text: str) -> str:
    return re.sub(r"\b(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)\b", "", text, flags=re.I)


def extract_timezone(text: str) -> tuple[str, Optional[timezone]]:
    cleaned = text.strip()
    for marker, tzinfo in EXPLICIT_TZ_OFFSETS.items():
        if marker in cleaned.upper():
            cleaned = re.sub(re.escape(marker), "", cleaned, flags=re.I)
            return cleaned.strip(), tzinfo

    match = re.search(r"\bGMT([+-]\d{1,2})\b", cleaned, flags=re.I)
    if match:
        offset_hours = int(match.group(1))
        cleaned = re.sub(r"\bGMT[+-]\d{1,2}\b", "", cleaned, flags=re.I)
        return cleaned.strip(), timezone(timedelta(hours=offset_hours))
    return cleaned, None


def parse_point_datetime(text: str, end_of_day: bool) -> Optional[datetime]:
    raw = " ".join(text.split()).strip(" ,")
    if not raw:
        return None

    raw, tzinfo = extract_timezone(raw)
    raw = strip_weekday_prefix(raw)
    raw = re.sub(r"\s+", " ", raw).strip(" ,")
    if not raw:
        return None

    has_time = bool(re.search(r"\b\d{1,2}:\d{2}\b", raw))
    default = datetime(2000, 1, 1, 23 if end_of_day else 0, 59 if end_of_day else 0)
    try:
        parsed = date_parser.parse(raw, fuzzy=True, default=default)
    except (ValueError, OverflowError):
        return None

    if not has_time:
        parsed = parsed.replace(hour=23 if end_of_day else 0, minute=59 if end_of_day else 0)

    if tzinfo is not None:
        parsed = parsed.replace(tzinfo=tzinfo).astimezone(BJT).replace(tzinfo=None)
    return parsed


def enrich_left_range_fragment(left: str, right: str) -> str:
    enriched = left
    month_match = re.search(
        r"\b(Jan|January|Feb|February|Mar|March|Apr|April|May|Jun|June|Jul|July|Aug|August|Sep|September|Oct|October|Nov|November|Dec|December)\b",
        right,
        flags=re.I,
    )
    if month_match and not re.search(month_match.re.pattern, enriched, flags=re.I):
        enriched = f"{enriched} {month_match.group(1)}"
    year_match = re.search(r"\b20\d{2}\b", right)
    if year_match and not re.search(r"\b20\d{2}\b", enriched):
        enriched = f"{enriched} {year_match.group(0)}"
    return enriched


def normalize_datetime_expression(text: str, field_name: str) -> str:
    raw = " ".join(text.split()).strip()
    if not raw or raw.startswith("未检出"):
        return raw
    if re.fullmatch(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}( ~ \d{4}-\d{2}-\d{2} \d{2}:\d{2})?", raw):
        return raw

    compact_range = re.fullmatch(r"(\d{1,2})-(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{4})", raw)
    if compact_range:
        day_start, day_end, month, year = compact_range.groups()
        left_dt = parse_point_datetime(f"{day_start} {month} {year}", end_of_day=False)
        right_dt = parse_point_datetime(f"{day_end} {month} {year}", end_of_day=True)
        if left_dt and right_dt:
            left_dt = left_dt.replace(hour=0, minute=0)
            right_dt = right_dt.replace(hour=23, minute=59)
            return f"{format_dt_bjt(left_dt)} ~ {format_dt_bjt(right_dt)}"

    if " - " in raw:
        left, right = raw.split(" - ", 1)
        left = enrich_left_range_fragment(left.strip(), right.strip())
        left_dt = parse_point_datetime(left, end_of_day=False)
        right_dt = parse_point_datetime(right, end_of_day=True)
        if left_dt and right_dt:
            if field_name == "conference_dates":
                if not re.search(r"\b\d{1,2}:\d{2}\b", left):
                    left_dt = left_dt.replace(hour=0, minute=0)
                if not re.search(r"\b\d{1,2}:\d{2}\b", right):
                    right_dt = right_dt.replace(hour=23, minute=59)
            elif not re.search(r"\b\d{1,2}:\d{2}\b", left):
                left_dt = left_dt.replace(hour=0, minute=0)
            if not re.search(r"\b\d{1,2}:\d{2}\b", right):
                right_dt = right_dt.replace(hour=23, minute=59)
            return f"{format_dt_bjt(left_dt)} ~ {format_dt_bjt(right_dt)}"

    point_dt = parse_point_datetime(raw, end_of_day=(field_name != "conference_dates"))
    if point_dt:
        return format_dt_bjt(point_dt)
    return raw


def shorten_label(label: str) -> str:
    low = label.lower().strip()
    if "submission of revisions" in low or "revision submission" in low or "major-revision" in low:
        return "大修"
    if "additional" in low and "response" in low:
        return "补充回应"
    if "round 1" in low or "r1" in low or "first cycle" in low or "1st round" in low:
        return "R1"
    if "round 2" in low or "r2" in low or "second cycle" in low or "2nd round" in low:
        return "R2"
    if "submission open" in low:
        return "开放"
    if "paper submission -- 2nd" in low:
        return "R2"
    if "paper submissions - 1st round" in low or "paper submission -- 1st" in low:
        return "R1"
    if "paper deadline" in low or "submission deadline" in low:
        return "截止"
    if "paper submission" in low or "full paper submission" in low or low == "submission":
        return "投稿"
    if "abstract submission" in low or "abstract deadline" in low or "abstract due" in low:
        return "摘要"
    if "major revision" in low or "revised manuscript" in low:
        return "大修"
    if "notification of revisions" in low or "final notification" in low or "under shepherding" in low:
        return "最终"
    if "initial notification" in low or "early notification" in low or "1st round" in low:
        return "初轮"
    if ("initial" in low or "preliminary" in low) and "notification" in low:
        return "初轮"
    if ("final" in low and "notification" in low) or "final decis" in low:
        return "最终"
    if "author notification" in low:
        return "通知"
    if "notification" in low:
        return "通知"
    if "author response" in low or "response period" in low or "rebuttal" in low or "discussion" in low:
        return "回应"
    if "camera ready" in low or "camera-ready" in low or "final version" in low:
        return "终稿"
    if "conference" in low:
        return "会期"
    cleaned = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", " ", label).strip()
    return cleaned[:12]


def normalize_field_value(value: str, field_name: str) -> str:
    raw = " ".join(str(value).split()).strip()
    default = FIELD_DEFAULTS.get(field_name, "")
    if not raw or raw == default or raw.startswith("未检出"):
        return raw or default

    segments = [segment.strip() for segment in raw.split("；") if segment.strip()]
    if not segments:
        return default

    normalized_segments: List[str] = []
    multi_segment = len(segments) > 1
    for segment in segments:
        if re.fullmatch(
            r".+ \d{4}-\d{2}-\d{2} \d{2}:\d{2}( ~ \d{4}-\d{2}-\d{2} \d{2}:\d{2})?",
            segment,
        ):
            normalized_segments.append(segment)
            continue
        label = ""
        body = segment
        if ":" in segment:
            candidate_label, candidate_body = segment.split(":", 1)
            if (
                re.search(r"[A-Za-z\u4e00-\u9fff]", candidate_label)
                and not re.fullmatch(r"\d{4}-\d{2}-\d{2}\s+\d{2}", candidate_label.strip())
                and re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|\d{4})\b", candidate_body, flags=re.I)
            ):
                label = candidate_label.strip()
                body = candidate_body.strip()
        normalized_body = normalize_datetime_expression(body, field_name)
        if label and multi_segment:
            normalized_label = shorten_label(label)
            if normalized_label:
                normalized_segments.append(f"{normalized_label} {normalized_body}".strip())
                continue
        normalized_segments.append(normalized_body)
    deduped = []
    for segment in normalized_segments:
        if segment not in deduped:
            deduped.append(segment)
    return "；".join(deduped) if deduped else default


def entry_quality(entry: TimelineEntry) -> int:
    score = 0
    for field_name, default in FIELD_DEFAULTS.items():
        value = getattr(entry, field_name)
        if value and value != default and not value.startswith("未检出"):
            score += 1
    if entry.homepage_url:
        score += 1
    return score


def load_venues() -> List[VenueRecord]:
    venues: List[VenueRecord] = []
    for path in sorted(METADATA_DIR.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        venue = payload["venue"]
        venues.append(
            VenueRecord(
                stem=path.stem,
                abbr=venue["abbr"],
                full_name=venue["full_name"],
                rank=venue["rank"],
                kind=venue["kind"],
                index_url=venue["index_url"],
            )
        )
    return venues


def parse_2025_homepages() -> Dict[str, str]:
    text = YEAR_README.read_text(encoding="utf-8")
    sections = re.split(r"^### ", text, flags=re.M)
    mapping: Dict[str, str] = {}
    for section in sections[1:]:
        meta_match = re.search(r"\[metadata\]\(metadata/([^)]+)\.json\)", section)
        if not meta_match:
            continue
        stem = meta_match.group(1)
        homepage_match = re.search(r"- (?:年主页|期刊主页)：([^\n]+)", section)
        if homepage_match:
            mapping[stem] = homepage_match.group(1).strip()
    return mapping


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def fetch_html(url: str) -> Optional[str]:
    try:
        response = SESSION.get(url, timeout=(5, 10))
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


@lru_cache(maxsize=None)
def parse_researchr_page(url: str) -> Optional[pd.DataFrame]:
    html = fetch_html(url)
    if not html:
        return None
    try:
        return pd.read_html(io.StringIO(html))[0]
    except ValueError:
        return None
    except Exception:
        return None


def format_values(values: Iterable[str], empty_text: str) -> str:
    deduped: List[str] = []
    for value in values:
        value = " ".join(str(value).split()).strip()
        if value and value not in deduped:
            deduped.append(value)
    return "；".join(deduped) if deduped else empty_text


def classify_researchr_rows(df: pd.DataFrame, track_patterns: List[str]) -> Dict[str, List[str]]:
    track_regex = re.compile("|".join(track_patterns), re.I)
    filtered = df[df["Track"].astype(str).str.fullmatch(track_regex)]
    if filtered.empty:
        filtered = df[df["Track"].astype(str).str.contains(track_regex)]

    buckets = {
        "abstract": [],
        "submission": [],
        "rebuttal": [],
        "notification": [],
        "camera_ready": [],
        "conference_dates": [],
        "extra": [],
    }

    rows = list(filtered[["When", "What"]].itertuples(index=False, name=None))
    for when, what in reversed(rows):
        what_text = " ".join(str(what).split()).strip()
        when_text = " ".join(str(when).split()).strip()
        combined = f"{what_text}: {when_text}"
        low = what_text.lower()
        if "reviews for rebuttal" in low or "review notification" in low:
            continue
        if "abstract" in low or "title and abstract" in low or "title submission" in low:
            buckets["abstract"].append(combined)
        elif "response" in low or "rebuttal" in low or "discussion" in low:
            buckets["rebuttal"].append(combined)
        elif "camera" in low or "final version" in low:
            buckets["camera_ready"].append(combined)
        elif "notification" in low or "decision" in low:
            buckets["notification"].append(combined)
        elif (
            "submission" in low
            or "papers due" in low
            or ("deadline" in low and "paper" in low)
        ) and "artifact" not in low and "open" not in low:
            buckets["submission"].append(combined)
        elif "conference" in low:
            buckets["conference_dates"].append(combined)
        else:
            buckets["extra"].append(combined)
    return buckets


def fetch_researchr_entry(record: VenueRecord, year: int, config: Dict[str, object]) -> TimelineEntry:
    slug = str(config["slug"])
    url = f"https://conf.researchr.org/dates/{slug}-{year}"
    homepage_url = f"https://conf.researchr.org/home/{slug}-{year}"
    df = parse_researchr_page(url)
    if df is None:
        return TimelineEntry(
            year=year,
            source_label="Official dates page",
            source_url=url,
            homepage_url=homepage_url,
            notes="未检出对应 official dates 页或页面无法稳定解析。",
        )

    buckets = classify_researchr_rows(df, list(config["track_patterns"]))  # type: ignore[arg-type]
    return TimelineEntry(
        year=year,
        abstract_deadline=format_values(buckets["abstract"], "未检出"),
        submission_deadline=format_values(buckets["submission"], "未检出"),
        rebuttal_window=format_values(buckets["rebuttal"], "未检出公开作者回应窗口"),
        notification=format_values(buckets["notification"], "未检出"),
        camera_ready=format_values(buckets["camera_ready"], "未检出"),
        conference_dates=format_values(buckets["conference_dates"], "未检出"),
        source_label="Official dates page",
        source_url=url,
        homepage_url=homepage_url,
        notes="",
    )


@lru_cache(maxsize=None)
def wikicfp_search(query: str) -> List[tuple[str, str]]:
    try:
        response = SESSION.get(
            "http://www.wikicfp.com/cfp/servlet/tool.search",
            params={"q": query},
            timeout=(5, 10),
        )
    except requests.RequestException:
        return []
    if response.status_code != 200:
        return []
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    results: List[tuple[str, str]] = []
    for anchor in soup.find_all("a", href=True):
        href = anchor["href"]
        if "event.showcfp" not in href:
            continue
        title = " ".join(anchor.get_text(" ", strip=True).split())
        if not title:
            continue
        if href.startswith("/"):
            href = "http://www.wikicfp.com" + href
        results.append((title, href))
    return results


def extract_wikicfp_fields(html: str) -> Dict[str, str]:
    text = BeautifulSoup(html, "html.parser").get_text("\n")
    lines = [" ".join(line.split()) for line in text.splitlines() if line.split()]
    mapping: Dict[str, str] = {}
    for idx, line in enumerate(lines[:-1]):
        if line in {
            "When",
            "Where",
            "Abstract Registration Due",
            "Abstract Due",
            "Submission Deadline",
            "Notification Due",
            "Final Version Due",
            "Link:",
        }:
            mapping[line] = lines[idx + 1]

    full_text = " ".join(lines).lower()
    if "author response" in full_text or "rebuttal" in full_text:
        snippets: List[str] = []
        for idx, line in enumerate(lines):
            low = line.lower()
            if "author response" in low or "rebuttal" in low:
                snippets.append(line)
                if idx + 1 < len(lines):
                    snippets.append(lines[idx + 1])
        combined = "；".join(snippets[:4])
        if re.search(r"\b20\d{2}\b", combined):
            mapping["Rebuttal"] = combined
    return mapping


def fetch_wikicfp_entry(record: VenueRecord, year: int, config: Dict[str, object]) -> TimelineEntry:
    query = str(config["query"])
    title_patterns = [
        re.compile(pattern.format(year=year), re.I)
        for pattern in config.get("title_patterns", [])
    ]
    multi_page = bool(config.get("multi_page"))
    candidates = []
    for title, href in wikicfp_search(query):
        if not any(pattern.search(title) for pattern in title_patterns):
            continue
        candidates.append((title, href))
    if not candidates:
        return TimelineEntry(
            year=year,
            source_label="WikiCFP search",
            source_url=f"http://www.wikicfp.com/cfp/servlet/tool.search?q={requests.utils.quote(query)}",
            notes="未在 `WikiCFP` 检出匹配该年份的条目。",
        )

    selected = candidates if multi_page else candidates[:1]
    fields = {
        "abstract": [],
        "submission": [],
        "rebuttal": [],
        "notification": [],
        "camera": [],
        "conference": [],
        "notes": [],
        "sources": [],
    }

    for title, href in selected:
        html = fetch_html(href)
        if not html:
            fields["notes"].append(f"{title}: 页面抓取失败")
            continue
        mapping = extract_wikicfp_fields(html)
        label_prefix = title
        if multi_page:
            label_prefix = title
        if "Abstract Registration Due" in mapping:
            fields["abstract"].append(f"{label_prefix}: {mapping['Abstract Registration Due']}")
        elif "Abstract Due" in mapping:
            fields["abstract"].append(f"{label_prefix}: {mapping['Abstract Due']}")
        if "Submission Deadline" in mapping:
            fields["submission"].append(f"{label_prefix}: {mapping['Submission Deadline']}")
        if "Rebuttal" in mapping:
            fields["rebuttal"].append(mapping["Rebuttal"])
        if "Notification Due" in mapping:
            fields["notification"].append(f"{label_prefix}: {mapping['Notification Due']}")
        if "Final Version Due" in mapping:
            fields["camera"].append(f"{label_prefix}: {mapping['Final Version Due']}")
        if "When" in mapping:
            fields["conference"].append(f"{label_prefix}: {mapping['When']}")
        if "Link:" in mapping and not fields.get("homepage"):
            fields["homepage"] = mapping["Link:"]
        fields["sources"].append(f"[{md_escape(title)}]({href})")

    return TimelineEntry(
        year=year,
        abstract_deadline=format_values(fields["abstract"], "未检出"),
        submission_deadline=format_values(fields["submission"], "未检出"),
        rebuttal_window=format_values(fields["rebuttal"], "未检出公开作者回应窗口"),
        notification=format_values(fields["notification"], "未检出"),
        camera_ready=format_values(fields["camera"], "未检出"),
        conference_dates=format_values(fields["conference"], "未检出"),
        source_label="WikiCFP",
        source_url=selected[0][1],
        homepage_url=str(fields.get("homepage") or ""),
        notes=format_values(fields["notes"], "") or f"搜索结果：{' / '.join(fields['sources'])}",
    )


def apply_manual_note(entry: TimelineEntry, stem: str) -> TimelineEntry:
    overrides = MANUAL_CONFERENCE_NOTES.get(stem, {}).get(entry.year)
    if not overrides:
        return entry
    for key, value in overrides.items():
        setattr(entry, key, value)
    return entry


def canonicalize_entry(entry: TimelineEntry) -> TimelineEntry:
    entry.abstract_deadline = normalize_field_value(entry.abstract_deadline, "abstract_deadline")
    entry.submission_deadline = normalize_field_value(entry.submission_deadline, "submission_deadline")
    entry.rebuttal_window = normalize_field_value(entry.rebuttal_window, "rebuttal_window")
    entry.notification = normalize_field_value(entry.notification, "notification")
    entry.camera_ready = normalize_field_value(entry.camera_ready, "camera_ready")
    entry.conference_dates = normalize_field_value(entry.conference_dates, "conference_dates")
    if not entry.homepage_url.strip() or entry.homepage_url.strip() == "待补":
        entry.homepage_url = f"未检出 {entry.year} 年主页"
    return entry


def choose_best_entry(candidates: List[TimelineEntry]) -> TimelineEntry:
    ranked = sorted(
        candidates,
        key=lambda entry: (entry_quality(entry), entry.source_label.startswith("Official")),
        reverse=True,
    )
    return ranked[0]


def build_conference_timelines(venues: List[VenueRecord]) -> Dict[str, List[TimelineEntry]]:
    output: Dict[str, List[TimelineEntry]] = {}
    for venue in venues:
        if venue.kind != "会议":
            continue
        rows: List[TimelineEntry] = []
        for year in YEARS:
            manual_row = MANUAL_CONFERENCE_ROWS.get(venue.stem, {}).get(year)
            if manual_row:
                entry = TimelineEntry(year=year, **manual_row)
                entry = canonicalize_entry(apply_manual_note(entry, venue.stem))
                rows.append(entry)
                continue

            candidates: List[TimelineEntry] = []
            if venue.stem in RESEARCHR_CONFIG:
                candidates.append(fetch_researchr_entry(venue, year, RESEARCHR_CONFIG[venue.stem]))
            if venue.stem in WIKICFP_CONFIG:
                candidates.append(fetch_wikicfp_entry(venue, year, WIKICFP_CONFIG[venue.stem]))
            if candidates:
                entry = choose_best_entry(candidates)
            else:
                entry = TimelineEntry(
                    year=year,
                    notes="当前仅保留 series 级说明，尚未稳定抓到可批量核对的年度 CFP 归档。",
                )
            entry = canonicalize_entry(apply_manual_note(entry, venue.stem))
            rows.append(entry)
        output[venue.stem] = rows
    return output


def render_journal_table(venues: List[VenueRecord], homepages: Dict[str, str]) -> str:
    lines: List[str] = []
    lines.append("| venue | 全称 | 等级 | 常规投稿方式 | 公开 rebuttal | 近 5 年节奏判断 | 当前入口 | 说明 |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for venue in venues:
        if venue.kind != "期刊":
            continue
        homepage = homepages.get(venue.stem, venue.index_url)
        lines.append(
            "| `{abbr}` | {full} | `{rank}` | 全年滚动投稿 | 一般无公开 conference 式 rebuttal | `2021-2025` 默认按常规稿滚动；若当年出现 special issue / special section，需另跟当年 CFP | [official]({homepage}) | {note} |".format(
                abbr=md_escape(venue.abbr),
                full=md_escape(venue.full_name),
                rank=venue.rank,
                homepage=homepage,
                note=md_escape(DEFAULT_JOURNAL_NOTE),
            )
        )
    return "\n".join(lines)


def render_markdown(
    venues: List[VenueRecord],
    homepages: Dict[str, str],
    conference_timelines: Dict[str, List[TimelineEntry]],
) -> str:
    ts = format_now_bjt()
    conference_count = sum(1 for venue in venues if venue.kind == "会议")
    journal_count = sum(1 for venue in venues if venue.kind == "期刊")

    lines: List[str] = []
    lines.append("# `CCF` 保留 venue 投稿时间线与流程资料")
    lines.append("")
    lines.append("## 1. 文档用途")
    lines.append("")
    lines.append("- 本文档服务于 `frontier_index/ccf_history/` 下保留 `CCF` venue 的投稿节奏跟踪。")
    lines.append("- 会议 venue：默认整理 `2021-2025` 最近 `5` 个会次的 `CFP / important dates` 主流程。")
    lines.append("- 期刊 venue：由于大多数为常规稿全年滚动投稿，不存在 conference 式年度 `CFP + rebuttal` 节奏，因此改整理“常规投稿方式 + 公开 review/rebuttal 口径 + special issue 提醒”。")
    lines.append(f"- 更新时间：`{ts}`")
    lines.append("")
    lines.append("## 2. 使用说明")
    lines.append("")
    lines.append("- 会议优先看：`摘要截止 / 投稿截止 / rebuttal 或 author response / 录用通知 / camera-ready / 会期`。")
    lines.append("- 所有时间统一记为北京时间格式 `yyyy-mm-dd hh:mm`。")
    lines.append("- 若源页只给日期、不写具体时区或时刻，则统一按北京时间该日 `23:59` 记账；区间起点默认补 `00:00`，终点默认补 `23:59`。")
    lines.append("- 若源页明确写了 `AoE / UTC±x / GMT±x`，则按源页时区换算到北京时间。")
    lines.append("- 对存在多轮制或双轮制的会议，`投稿截止` 与 `rebuttal` 列会保留简写标签，如 `R1 / R2 / 初轮 / 最终 / 大修`。")
    lines.append("- 若某一年写为 `未检出`，含义是当前未稳定找到可公开核对的官方归档或可信回退源，不等于该 venue 当年一定停办。")
    lines.append("- 来源优先级：`official dates page / official series page > WikiCFP fallback`。")
    lines.append("- 每个年份行里的 `年主页` 必须指向该年 conference homepage；若该 venue 当年无 standalone 主会或已并入其他系列，会在该列和说明列写清楚。")
    lines.append("")
    lines.append("## 3. 会议 venue：近 5 年主流程时间线")
    lines.append("")
    lines.append(f"- 当前覆盖会议：`{conference_count}` 个。")
    lines.append("- 推荐使用方式：先在本页确定该 venue 的常见投稿窗口，再回到当年官方 CFP 页确认是否有延期、双轮制、分 track 截止或 `AoE` 约束。")
    lines.append("")

    for venue in venues:
        if venue.kind != "会议":
            continue
        lines.append(f'<a id="timeline-{venue.stem}"></a>')
        lines.append("")
        lines.append(f"### `{venue.abbr}`")
        lines.append("")
        lines.append(f"- 全称：{venue.full_name}")
        lines.append(f"- `CCF` 等级：`{venue.rank}`")
        lines.append(f"- 2025 年入口页：[venue](./2025/venues/{venue.stem}.md)")
        homepage = conference_timelines[venue.stem][0].homepage_url or homepages.get(venue.stem)
        if homepage:
            lines.append(f"- 2025 年主页：{homepage}")
        lines.append(f"- 学术索引页：{venue.index_url}")
        lines.append("")
        lines.append("| 年份 | 年主页 | 摘要截止 | 投稿截止 | rebuttal / author response | 录用通知 | 终稿 / camera-ready | 会期 | 来源 | 说明 |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for entry in conference_timelines[venue.stem]:
            source_text = entry.source_label
            if entry.source_url:
                source_text = f"[{md_escape(entry.source_label)}]({entry.source_url})"
            if entry.homepage_url.startswith("http://") or entry.homepage_url.startswith("https://"):
                homepage_text = f"[home]({entry.homepage_url})"
            else:
                homepage_text = entry.homepage_url or "待补"
            lines.append(
                "| `{year}` | {homepage} | {abstract} | {submission} | {rebuttal} | {notification} | {camera} | {conference} | {source} | {notes} |".format(
                    year=entry.year,
                    homepage=homepage_text,
                    abstract=md_escape(entry.abstract_deadline),
                    submission=md_escape(entry.submission_deadline),
                    rebuttal=md_escape(entry.rebuttal_window),
                    notification=md_escape(entry.notification),
                    camera=md_escape(entry.camera_ready),
                    conference=md_escape(entry.conference_dates),
                    source=source_text,
                    notes=md_escape(entry.notes or ""),
                )
            )
        lines.append("")

    lines.append("## 4. 期刊 venue：常规投稿节奏")
    lines.append("")
    lines.append(f"- 当前覆盖期刊：`{journal_count}` 个。")
    lines.append("- 口径：期刊默认不按 conference 式年度 `CFP / rebuttal` 追踪，而按“常规稿是否全年滚动 + 是否常见 special issue / special section”整理。")
    lines.append("- 需要冲特刊时，仍应以当年官方 `special issue CFP` 为准。")
    lines.append("")
    lines.append(render_journal_table(venues, homepages))
    lines.append("")
    lines.append("## 5. 维护规则")
    lines.append("")
    lines.append("- 若官方 venue 网站存在稳定的 archived important-dates 页，后续应优先补官方，不长期依赖 `WikiCFP`。")
    lines.append("- 若某个 venue 在近 `5` 年内实际上已并入其他系列、停办或长期不发独立 CFP，应在“说明”列明确写清，不要机械留空。")
    lines.append("- 期刊若后续要补 special issue 级时间线，建议新开专题表，不要把常规稿滚动节奏和特刊 CFP 混在一起。")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Build CCF venue submission timelines.")
    parser.add_argument("--output", type=Path, default=OUTPUT_MD)
    args = parser.parse_args()

    venues = load_venues()
    homepages = parse_2025_homepages()
    conference_timelines = build_conference_timelines(venues)
    markdown = render_markdown(venues, homepages, conference_timelines)
    args.output.write_text(markdown, encoding="utf-8")
    print(json.dumps({"output": str(args.output), "venues": len(venues)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
