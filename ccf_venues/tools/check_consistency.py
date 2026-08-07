#!/usr/bin/env python3
"""ccf_venues 一致性不变量校验。

用途
----
`GUIDE.md` §12.4 第 13 步要求每轮常态化刷新后校验一组结构不变量。此前每轮 review
都由 reviewer 各自重写等价脚本，既浪费时间也导致口径分歧（例如 2026-08 那轮出现过
「2027 表 50 还是 63 行」的两轮争论）。本脚本把这些不变量固化下来。

⚠️ **重要边界**：本脚本只能校验**结构**。它抓不到散文中的旧事实——
`GUIDE.md` §12.4 第 11 步的「用旧值对全库 grep」是唯一能覆盖那个盲区的手段，
**不得用本脚本通过来替代它**。2026-08 那轮的多数缺陷都是本脚本查不出来的。

用法
----
    cd ccf_venues && python3 tools/check_consistency.py [--today YYYY-MM-DD]

退出码 0 表示全部通过，1 表示存在不变量违规。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import os
import re
import sys
from collections import Counter

TIMELINE = "TIMELINE.md"
ENTRY_FILES = ["TIMELINE.md", "SUMMARY.md", "GUIDE.md", "README.md", "01-venue-scope.md"]

# 年度章节定位：(年份, 表格标题前缀, Mermaid 标题前缀, 下一节标题)
YEAR_SECTIONS = [
    ("2028", "### 7.1 2028", "### 7.2 2028", "## 8. 2027"),
    ("2027", "### 8.1 2027", "### 8.2 2027", "## 9. 2026"),
    ("2026", "### 9.1 2026", "### 9.2 2026", "## 10. 2025"),
    ("2025", "### 10.1 2025", "### 10.2 2025", "## 11. 2024"),
    ("2024", "### 11.1 2024", "### 11.2 2024", "## 12. 2023"),
    ("2023", "### 12.1 2023", "### 12.2 2023", "## 13. 2022"),
    ("2022", "### 13.1 2022", "### 13.2 2022", "## 14. 期刊滚动投稿"),
]

DATE_RE = re.compile(r"\| (\d{4}-\d{2}-\d{2})")
MERMAID_DATE_RE = re.compile(r", (\d{4}-\d{2}-\d{2}),? ")
MERMAID_ID_RE = re.compile(r"^  \S+ \S+ :(?:milestone, )?([a-z0-9_]+),", re.M)
SEP_RE = re.compile(r"^\|[\s:|-]+\|$")
NON_WINDOW_TYPES = {"Notification", "Camera-ready", "Conference", "Rebuttal"}

failures: list[str] = []
notes: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def year_rows(text: str, year: str, start: str, end: str) -> list[str]:
    i, j = text.index(start), text.index(end)
    return [x for x in text[i:j].split("\n") if x.startswith(f"| {year}-")]


def mermaid_block(text: str, start: str, nxt: str) -> str:
    k = text.index(start)
    return text[k : text.index("\n" + nxt, k)]


def check_year_tables(text: str) -> None:
    """年度表 ↔ Mermaid 日期 multiset 相等；年度表严格日期升序。

    计数口径（GUIDE §12.4 第 13 步）：
        数据行数 + 日期区间行数 = 日期出现总次数
    两种口径下不变量都应成立；本函数用「数据行起始日期」口径。
    """
    for year, tbl_head, mer_head, nxt in YEAR_SECTIONS:
        try:
            rows = year_rows(text, year, tbl_head, mer_head)
            block = mermaid_block(text, mer_head, nxt)
        except ValueError:
            fail(f"[year-section] 无法定位 {year} 的表格或 Mermaid 章节")
            continue

        tbl = Counter(DATE_RE.match(r).group(1) for r in rows)
        mer = Counter(m.group(1) for line in block.split("\n")
                      if line.startswith("  ") and (m := MERMAID_DATE_RE.search(line)))

        if tbl != mer:
            only_t = sorted((tbl - mer).items())
            only_m = sorted((mer - tbl).items())
            fail(f"[table-vs-mermaid] {year} 日期 multiset 不等；仅表: {only_t}；仅图: {only_m}")

        for idx in range(1, len(rows)):
            prev = DATE_RE.match(rows[idx - 1]).group(1)
            cur = DATE_RE.match(rows[idx]).group(1)
            if cur < prev:
                fail(f"[year-order] {year} 年度表乱序：{prev} 之后出现 {cur}")
                break

        ranges = sum(1 for r in rows if " 至 " in cells(r)[0])
        notes.append(f"{year}: 数据行 {len(rows)} + 区间行 {ranges} = {len(rows) + ranges}"
                     f"（Mermaid {sum(mer.values())} 条）")


def section3(text: str) -> list[str]:
    i = text.index("| 日期时间 | Venue |")
    head_end = text.index("\n", text.index("| --- |", i)) + 1
    return [x for x in text[head_end : text.index("### 3.1")].split("\n") if x.startswith("| 20")]


def check_section3(text: str, today: str) -> None:
    """§3 是年度表的筛选视图，不是独立事实源。

    校验：每行在年度表有同日期同 venue 同 track 的对应事件、且「日期时间」列**逐字一致**；
    无重复行；无已过期行；不含 Notification / Camera-ready / Conference / Rebuttal。
    """
    rows = section3(text)
    all_years = text[text.index("## 7. 2028 时间线") :]
    seen: Counter = Counter()

    for row in rows:
        c = cells(row)
        dt, track = c[0], c[3]
        m_ven = re.search(r"\[(.+?)\]", c[1])
        if not m_ven:
            fail(f"[s3-format] §3 行缺 venue 链接：{row[:70]}")
            continue
        venue = m_ven.group(1)
        seen[(dt[:10], venue, track)] += 1

        if dt[:10] < today:
            fail(f"[s3-expired] §3 含已过期行：{dt[:10]} {venue} / {track}")
        if track in NON_WINDOW_TYPES or c[4] in NON_WINDOW_TYPES:
            fail(f"[s3-type] §3 含非投稿窗口类型行：{venue} / {track} / {c[4]}")

        pat = re.compile(r"^\| (" + re.escape(dt[:10]) + r"[^|]*)\| \[" + re.escape(venue)
                         + r"\][^\n]*\| " + re.escape(track) + r" \|", re.M)
        m = pat.search(all_years)
        if not m:
            fail(f"[s3-orphan] §3 行在年度表无对应事件：{dt[:10]} {venue} / {track}")
        elif m.group(1).strip() != dt:
            fail(f"[s3-datecol] §3 与年度表「日期时间」列不一致：{venue} / {track}\n"
                 f"            §3    : {dt}\n            年度表: {m.group(1).strip()}")

    for key, n in seen.items():
        if n > 1:
            fail(f"[s3-dup] §3 重复行 ×{n}：{key}")

    notes.append(f"§3: {len(rows)} 行")


def check_mermaid_ids(text: str) -> None:
    ids = MERMAID_ID_RE.findall(text)
    dups = [k for k, v in Counter(ids).items() if v > 1]
    if dups:
        fail(f"[mermaid-id] 重复 id {len(dups)} 个：{dups[:5]}")
    notes.append(f"Mermaid id: {len(ids)} 条，{len(set(ids))} 唯一")


def check_mermaid_content(text: str) -> None:
    """Mermaid 内不得出现 URL 或 emoji（GUIDE §11.3）。"""
    bad = []
    for block in re.findall(r"```mermaid\n(.*?)```", text, re.S):
        for line in block.split("\n"):
            if "http" in line or re.search(r"[\U0001F300-\U0001FAFF☀-➿]", line):
                bad.append(line.strip()[:60])
    if bad:
        fail(f"[mermaid-content] Mermaid 内含 URL 或 emoji：{bad[:3]}")


def check_table_columns() -> None:
    """全库 Markdown 表格列数与表头一致。"""
    files = sorted(set(glob.glob("**/README.md", recursive=True)) | set(ENTRY_FILES))
    bad, total = [], 0
    for path in files:
        if not os.path.exists(path):
            continue
        header_cols = None
        for lineno, line in enumerate(read(path).split("\n"), 1):
            if line.startswith("|") and line.endswith("|"):
                n = line.count("|")
                if SEP_RE.match(line):
                    header_cols, total = n, total + 1
                    continue
                if header_cols and n != header_cols:
                    bad.append(f"{path}:{lineno} 列数 {n - 1} != 表头 {header_cols - 1}")
            else:
                header_cols = None
    if bad:
        fail(f"[table-cols] {len(bad)} 行列数不匹配：{bad[:5]}")
    notes.append(f"表格: {total} 张，列数不匹配 {len(bad)}")


def check_stats() -> None:
    """42 venue / 年度 README 数量与目录树一致。"""
    venues = sorted(glob.glob("conf-*") + glob.glob("journal-*"))
    venues = [v for v in venues if os.path.isdir(v)]
    years = glob.glob("*/[12][0-9][0-9][0-9]/README.md")
    confs = [v for v in venues if v.startswith("conf-")]
    jours = [v for v in venues if v.startswith("journal-")]
    notes.append(f"venue: {len(venues)}（{len(confs)} 会议 / {len(jours)} 期刊）；年度 README: {len(years)}")

    entry = read("README.md") + read("SUMMARY.md") + read("GUIDE.md")
    if f"{len(venues)} 个 venue" not in entry:
        fail(f"[stats] 入口文档未声明当前 venue 数 {len(venues)}")
    if f"{len(years)} 个年度 README" not in entry:
        fail(f"[stats] 入口文档未声明当前年度 README 数 {len(years)}")


def check_changelog_desc() -> None:
    """更新日志按时间降序。"""
    files = sorted(set(glob.glob("**/*.md", recursive=True)))
    bad = 0
    for path in files:
        text = read(path)
        for m in re.finditer(r"\| 时间 \| 更新内容 \|\n\|[-\s|]+\|\n((?:\|[^\n]*\n)+)", text):
            stamps = re.findall(r"^\| `([0-9][^`]*)`", m.group(1), re.M)
            for i in range(1, len(stamps)):
                if stamps[i] > stamps[i - 1]:
                    fail(f"[changelog-order] {path} 更新日志非降序：{stamps[i-1]} 之后是 {stamps[i]}")
                    bad += 1
                    break
    if not bad:
        notes.append("更新日志: 全部降序")


def check_relative_links() -> None:
    """仓库内相对链接目标存在。"""
    bad = []
    for path in sorted(glob.glob("**/*.md", recursive=True)):
        base = os.path.dirname(path)
        for m in re.finditer(r"\]\((\.{1,2}/[^)#\s]+)", read(path)):
            target = os.path.normpath(os.path.join(base, m.group(1)))
            if not os.path.exists(target):
                bad.append(f"{path} -> {m.group(1)}")
    if bad:
        fail(f"[links] {len(bad)} 个相对链接目标缺失：{bad[:5]}")
    else:
        notes.append("相对链接: 0 断裂")


def main() -> int:
    ap = argparse.ArgumentParser(description="ccf_venues 一致性不变量校验")
    ap.add_argument("--today", default=_dt.date.today().isoformat(),
                    help="用于判定 §3 是否含已过期行的基准日（默认系统当天）")
    args = ap.parse_args()

    if not os.path.exists(TIMELINE):
        print("请在 ccf_venues/ 目录下运行本脚本。", file=sys.stderr)
        return 2

    text = read(TIMELINE)
    check_year_tables(text)
    check_section3(text, args.today)
    check_mermaid_ids(text)
    check_mermaid_content(text)
    check_table_columns()
    check_stats()
    check_changelog_desc()
    check_relative_links()

    print(f"基准日: {args.today}\n")
    for n in notes:
        print(f"  · {n}")
    print()
    if failures:
        print(f"✗ {len(failures)} 项不变量违规：\n")
        for f in failures:
            print(f"  - {f}")
        print("\n⚠️ 本脚本只查结构。散文中的旧事实必须另按 GUIDE §12.4 第 11 步用旧值 grep 排查。")
        return 1
    print("✓ 全部结构不变量通过。")
    print("⚠️ 本脚本只查结构，抓不到散文中的旧事实；仍须执行 GUIDE §12.4 第 11 步的旧值 grep。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
