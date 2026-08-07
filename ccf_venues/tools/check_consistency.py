#!/usr/bin/env python3
"""ccf_venues 结构一致性不变量校验。

用途
----
`GUIDE.md` §12.4 第 13 步要求每轮常态化刷新后校验一组结构不变量。此前每轮 review
都由 reviewer 各自重写等价脚本，既浪费时间也导致口径分歧（例如 2026-08 那轮出现过
「2027 表 50 还是 63 行」的两轮争论）。本脚本把这些不变量固化下来。

⚠️ **边界（必读）**
本脚本只能校验**结构**。它抓不到散文中的旧事实——`GUIDE.md` §12.4 第 11 步的
「用旧值对全库 grep」是唯一能覆盖那个盲区的手段，**不得用本脚本通过来替代它**。
2026-08 那轮的多数缺陷、以及轮次 9 的 MSR 年度页缺口，都是本脚本查不出来的。

防假阴性设计
------------
一个静默通过的校验器比没有校验器更危险，因为它给出虚假信心。本脚本引入当天的故障
注入测试就实测到一处真实假阴性：`| 日期时间 | Venue |` 这个表头与**各年度表完全同名**，
一旦 §3 表头被改动，`str.index` 会回落到年度表的同名表头；该偏移落在 `### 3.1` 之后，于是
`text[head_end : text.index("### 3.1")]` 成为**反向切片**、结果为空，§3 解析出 0 行，
**一个检查都没执行**却打印「通过」并返回 0。因此：

* 所有结构标记都经 :func:`locate` 定位，该函数断言标记**恰好出现一次**；
  缺失或歧义都**报错而非跳过**。
* §3 先按章节标题收窄范围，再在范围内找表头。
* 解析出 0 行 / 0 日期 / 0 表格一律视为失败，而不是「没有违规」。
* 章节相对顺序（表格 < Mermaid < 下一节）也纳入断言。

用法
----
    cd ccf_venues && python3 tools/check_consistency.py [--today YYYY-MM-DD]

退出码：0 全部通过；1 存在不变量违规；2 运行环境不对。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import glob
import os
import re
import sys
from collections import Counter
from typing import Optional

TIMELINE = "TIMELINE.md"
ENTRY_FILES = ["TIMELINE.md", "SUMMARY.md", "GUIDE.md", "README.md", "01-venue-scope.md"]

# (年份, 表格章节标题, Mermaid 章节标题, 下一节标题)
# 标题必须写完整。只写前缀会让「章节改名」这类结构变更悄悄通过 locate() 的唯一性断言。
YEAR_SECTIONS = [
    ("2028", "### 7.1 2028 投稿事件总表", "### 7.2 2028 Mermaid 可视化", "## 8. 2027 时间线"),
    ("2027", "### 8.1 2027 投稿事件总表", "### 8.2 2027 Mermaid 可视化", "## 9. 2026 时间线"),
    ("2026", "### 9.1 2026 投稿事件总表", "### 9.2 2026 Mermaid 可视化", "## 10. 2025 时间线"),
    ("2025", "### 10.1 2025 投稿事件总表", "### 10.2 2025 Mermaid 可视化", "## 11. 2024 时间线"),
    ("2024", "### 11.1 2024 投稿事件总表", "### 11.2 2024 Mermaid 可视化", "## 12. 2023 时间线"),
    ("2023", "### 12.1 2023 投稿事件总表", "### 12.2 2023 Mermaid 可视化", "## 13. 2022 时间线"),
    ("2022", "### 13.1 2022 投稿事件总表", "### 13.2 2022 Mermaid 可视化",
     "## 14. 期刊滚动投稿 / 未定日期"),
]

SECTION3_HEADING = "## 3. 近期投稿窗口速览"
SECTION3_END = "### 3.1 索引入口列说明"
YEARS_START = "## 7. 2028 时间线"
S3_TABLE_HEADER = "| 日期时间 | Venue |"

DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
MERMAID_ID_RE = re.compile(r"^  \S+ \S+ :(?:milestone, )?([a-z0-9_]+),", re.M)
SEP_RE = re.compile(r"^\|[\s:|-]+\|$")
ESCAPED_PIPE_RE = re.compile(r"\\\|")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")
NON_WINDOW_TYPES = {"Notification", "Camera-ready", "Conference", "Rebuttal"}

failures: list[str] = []
notes: list[str] = []
stats: list[str] = []


def fail(msg: str) -> None:
    failures.append(msg)


def read(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def n_cols(line: str) -> int:
    r"""统计一行的单元格分隔符数。

    ``\|`` 是 Markdown 标准转义，GitHub 渲染为单元格内的字面竖线而非分隔符，因此计数前
    必须先剔除。早期版本漏了这一步，对合法的转义竖线误报——引入当天就在 ``GUIDE.md`` 的
    更新日志行上产生了假阳性。
    """
    return ESCAPED_PIPE_RE.sub("", line).count("|")


def locate(text: str, marker: str, what: str) -> Optional[int]:
    """定位一个结构标记，并断言它恰好出现一次。

    这是防假阴性的关键：标记缺失（章节改名 / 删除）或出现多次（与其他表重名）时必须
    报错，而不是静默拿错位置去校验——后者会让结构变更悄悄通过。
    """
    n = text.count(marker)
    if n == 0:
        fail(f"[anchor-missing] 找不到{what}：`{marker}`。章节可能已改名或删除；"
             f"请同步更新本脚本的定位常量，不要让校验静默跳过。")
        return None
    if n > 1:
        fail(f"[anchor-ambiguous] {what} `{marker}` 在文中出现 {n} 次，无法唯一定位，"
             f"校验可能作用于错误的表格。请改用更具体的标记。")
        return None
    return text.index(marker)


def check_year_tables(text: str) -> None:
    """年度表 ↔ Mermaid **全部日期** multiset 相等；年度表严格日期升序。

    日期口径：逐行取「日期时间」列中出现的**所有** ``YYYY-MM-DD``，因此
    ``2026-12-04..2026-12-08`` 这类区间行的**起止两端都参与比对**，Mermaid 侧同理取该
    行全部日期。早期版本只取首个日期，导致把区间的结束日期改错也能通过（轮次 9 M-1）。
    """
    for year, tbl_head, mer_head, nxt in YEAR_SECTIONS:
        i = locate(text, tbl_head, f"{year} 年度表章节标题")
        k = locate(text, mer_head, f"{year} Mermaid 章节标题")
        e = locate(text, nxt, f"{year} 之后的下一节标题")
        if i is None or k is None or e is None:
            continue
        if not i < k < e:
            fail(f"[year-section] {year} 章节顺序异常：表格({i}) / Mermaid({k}) / 下一节({e})")
            continue

        rows = [x for x in text[i:k].split("\n") if x.startswith(f"| {year}-")]
        if not rows:
            fail(f"[year-empty] {year} 年度表解析出 0 行；章节标记或行格式可能已变更")
            continue

        tbl: Counter = Counter()
        for r in rows:
            tbl.update(DATE_RE.findall(cells(r)[0]))

        mer: Counter = Counter()
        n_mer_lines = 0
        for line in text[k:e].split("\n"):
            if line.startswith("  ") and ":" in line:
                found = DATE_RE.findall(line)
                if found:
                    mer.update(found)
                    n_mer_lines += 1
        if not mer:
            fail(f"[mermaid-empty] {year} Mermaid 区块解析出 0 个日期；格式可能已变更")
            continue

        if tbl != mer:
            fail(f"[table-vs-mermaid] {year} 日期 multiset 不等；"
                 f"仅表: {sorted((tbl - mer).items())}；仅图: {sorted((mer - tbl).items())}")

        starts = [DATE_RE.search(r).group(0) for r in rows]
        for idx in range(1, len(starts)):
            if starts[idx] < starts[idx - 1]:
                fail(f"[year-order] {year} 年度表乱序：{starts[idx - 1]} 之后出现 {starts[idx]}")
                break

        ranges = sum(1 for r in rows if len(DATE_RE.findall(cells(r)[0])) > 1)
        stats.append(f"{year}: 数据行 {len(rows)} + 区间行 {ranges} = 日期 {len(rows) + ranges} 次"
                     f"（Mermaid {n_mer_lines} 行 / {sum(mer.values())} 个日期）")


def section3_rows(text: str) -> Optional[list[str]]:
    """定位 §3 表格体。

    不能直接 ``text.index(S3_TABLE_HEADER)`` —— 该表头与各年度表**完全同名**。一旦 §3
    表头被改动，index 会回落到年度表，切片反向为空、§3 零检查通过（本脚本引入当天由故障注入
    实测到的真实假阴性，退出码 0）。因此先按章节标题收窄范围。
    """
    h = locate(text, SECTION3_HEADING, "§3 章节标题")
    end = locate(text, SECTION3_END, "§3 结束标记")
    if h is None or end is None:
        return None
    if not h < end:
        fail(f"[s3-section] §3 章节标题({h}) 位于结束标记({end}) 之后")
        return None

    seg = text[h:end]
    if S3_TABLE_HEADER not in seg:
        fail(f"[s3-header] §3 章节内找不到表头 `{S3_TABLE_HEADER}`；表头可能已改动。"
             f"注意该表头与各年度表同名，绝不能退回全文搜索。")
        return None
    i = seg.index(S3_TABLE_HEADER)
    head_end = seg.index("\n", seg.index("| --- |", i)) + 1
    rows = [x for x in seg[head_end:].split("\n") if x.startswith("| 20")]
    if not rows:
        fail("[s3-empty] §3 解析出 0 行；表头或行格式可能已变更")
        return None
    return rows


def check_section3(text: str, today: str) -> None:
    """§3 是年度表的筛选视图，不是独立事实源。

    校验：每行在年度表有同日期 / 同 venue / 同 track 的对应事件，且「日期时间」列
    **逐字一致**；无重复行；无已过期行；不含 Notification / Camera-ready /
    Conference / Rebuttal 类型。
    """
    rows = section3_rows(text)
    if rows is None:
        return
    y = locate(text, YEARS_START, "年度时间线起始标题")
    if y is None:
        return
    all_years = text[y:]

    seen: Counter = Counter()
    for row in rows:
        c = cells(row)
        if len(c) < 5:
            fail(f"[s3-format] §3 行字段不足（{len(c)} 列）：{row[:70]}")
            continue
        dt, track, dtype = c[0], c[3], c[4]
        m_ven = re.search(r"\[(.+?)\]", c[1])
        if not m_ven:
            fail(f"[s3-format] §3 行缺 venue 链接：{row[:70]}")
            continue
        venue = m_ven.group(1)
        day = DATE_RE.search(dt)
        if not day:
            fail(f"[s3-format] §3 行日期列无法解析：{dt}")
            continue
        day = day.group(0)
        seen[(day, venue, track)] += 1

        if day < today:
            fail(f"[s3-expired] §3 含已过期行：{day} {venue} / {track}")
        if track in NON_WINDOW_TYPES or dtype in NON_WINDOW_TYPES:
            fail(f"[s3-type] §3 含非投稿窗口类型行：{venue} / {track} / {dtype}")

        pat = re.compile(r"^\| (" + re.escape(day) + r"[^|]*)\| \[" + re.escape(venue)
                         + r"\][^\n]*\| " + re.escape(track) + r" \|", re.M)
        m = pat.search(all_years)
        if not m:
            fail(f"[s3-orphan] §3 行在年度表无对应事件：{day} {venue} / {track}")
        elif m.group(1).strip() != dt:
            fail(f"[s3-datecol] §3 与年度表「日期时间」列不一致：{venue} / {track}"
                 f"｜§3: {dt}｜年度表: {m.group(1).strip()}")

    for key, n in seen.items():
        if n > 1:
            fail(f"[s3-dup] §3 重复行 ×{n}：{key}")
    stats.append(f"§3: {len(rows)} 行")


def check_mermaid(text: str) -> None:
    """Mermaid id 唯一；块内不含 URL 与 emoji（GUIDE §11.3）。"""
    blocks = re.findall(r"```mermaid\n(.*?)```", text, re.S)
    if not blocks:
        fail("[mermaid-none] 未找到任何 ```mermaid 代码块；格式可能已变更")
        return
    ids = MERMAID_ID_RE.findall(text)
    if not ids:
        fail("[mermaid-none] 未解析到任何 Mermaid 事件 id；行格式可能已变更")
        return
    dups = [k for k, v in Counter(ids).items() if v > 1]
    if dups:
        fail(f"[mermaid-id] 重复 id {len(dups)} 个：{dups[:5]}")

    bad = [line.strip()[:60] for block in blocks for line in block.split("\n")
           if "http" in line or EMOJI_RE.search(line)]
    if bad:
        fail(f"[mermaid-content] Mermaid 内含 URL 或 emoji：{bad[:3]}")
    stats.append(f"Mermaid: {len(blocks)} 块 / {len(ids)} 事件 id，{len(set(ids))} 唯一")


def check_table_columns() -> None:
    """全库 Markdown 表格列数一致：表头行、分隔行、数据行三者列数必须相同。

    早期版本只用分隔行确定基准，表头行本身从不参与比对（轮次 9 M-3）。
    扫描范围含 ``templates/*.md``——它们是新建 venue 页的模板源，破损会扩散。
    """
    files = sorted(set(glob.glob("**/README.md", recursive=True))
                   | set(glob.glob("templates/*.md"))
                   | {f for f in ENTRY_FILES if os.path.exists(f)})
    bad, total = [], 0
    for path in files:
        lines = read(path).split("\n")
        for lineno, line in enumerate(lines, 1):
            if not (line.startswith("|") and line.endswith("|") and SEP_RE.match(line)):
                continue
            total += 1
            n = n_cols(line)
            head = lines[lineno - 2] if lineno >= 2 else ""
            if head.startswith("|") and head.endswith("|") and n_cols(head) != n:
                bad.append(f"{path}:{lineno - 1} 表头列数 {n_cols(head) - 1} != 分隔行 {n - 1}")
            for off, row in enumerate(lines[lineno:], lineno + 1):
                if not (row.startswith("|") and row.endswith("|")):
                    break
                if n_cols(row) != n:
                    bad.append(f"{path}:{off} 列数 {n_cols(row) - 1} != 表头 {n - 1}")
    if not total:
        fail("[table-none] 未解析到任何表格；运行目录可能不对")
    if bad:
        fail(f"[table-cols] {len(bad)} 行列数不匹配：{bad[:5]}")
    stats.append(f"表格: {total} 张（含 templates/），列数不匹配 {len(bad)}")


def check_stats() -> None:
    """venue / 年度 README 数量与目录树一致，且入口文档声明与实际相符。"""
    venues = [v for v in sorted(glob.glob("conf-*") + glob.glob("journal-*")) if os.path.isdir(v)]
    years = glob.glob("*/[12][0-9][0-9][0-9]/README.md")
    if not venues:
        fail("[stats-none] 未发现任何 venue 目录；运行目录可能不对")
        return
    confs = sum(1 for v in venues if v.startswith("conf-"))
    stats.append(f"venue: {len(venues)}（{confs} 会议 / {len(venues) - confs} 期刊）；"
                 f"年度 README: {len(years)}")

    entry = "".join(read(f) for f in ENTRY_FILES if os.path.exists(f))
    if f"{len(venues)} 个 venue" not in entry:
        fail(f"[stats] 入口文档未声明当前 venue 数 {len(venues)}")
    if f"{len(years)} 个年度 README" not in entry:
        fail(f"[stats] 入口文档未声明当前年度 README 数 {len(years)}")


def check_changelog_desc() -> None:
    """更新日志按时间降序。

    表头必须逐字为 ``| 时间 | 更新内容 |``；匹配张数一并输出，避免「匹配 0 张也打印
    全部降序」的误导（轮次 9 M-4）。
    """
    n_tables = n_stamps = 0
    for path in sorted(glob.glob("**/*.md", recursive=True)):
        for m in re.finditer(r"\| 时间 \| 更新内容 \|\n\|[-\s|]+\|\n((?:\|[^\n]*\n)+)", read(path)):
            n_tables += 1
            ss = re.findall(r"^\| `([0-9][^`]*)`", m.group(1), re.M)
            n_stamps += len(ss)
            for i in range(1, len(ss)):
                if ss[i] > ss[i - 1]:
                    fail(f"[changelog-order] {path} 更新日志非降序：{ss[i - 1]} 之后是 {ss[i]}")
                    break
    if not n_tables:
        fail("[changelog-none] 未匹配到任何更新日志表；表头格式可能已变更")
    stats.append(f"更新日志: {n_tables} 张表 / {n_stamps} 个时间戳，降序校验完成")


def check_timezone_suffix() -> None:
    """同一 venue-year 的时区标注形态必须三方一致：年度页 / venue 根 README / TIMELINE。

    背景（轮次 11-12）：库内多处把官方 ``Timezone: AoE (UTC-12h)`` 只写成 ``AoE``，而**同一
    venue-year 的另一处**写了完整时区——即本库已持有更高等级的证据，派生视图却降级了。
    一次修 2 个 venue、下一轮再冒出 5 个，是因为此前一直**按 venue 枚举**而不是按不变量枚举。

    时区标注分三类，同一 venue-year 只允许出现一种：

    ==========================  ====================================================
    ``UTC``                     ``AoE / UTC-12h`` 或 ``AoE (UTC-12h)`` / ``AoE (UTC-12)``
    ``NAMED``                   ``AoE (Anywhere on Earth)``
    ``BARE``                    只有 ``AoE``
    ==========================  ====================================================

    ⚠️ **括号形态与斜杠形态是同一类**。轮次 12 实测到：早期版本只认 ``AoE / UTC-\d``，把全库
    90 处规范官方写法 ``AoE (UTC-12h)`` 判成 BARE，于是修复脚本把 ICFEM 的官方引文改成了
    ``AoE / UTC-12 (UTC-12)`` —— 校验器逼着作者去破坏官方逐字才能变绿。

    ⚠️ **NAMED 必须自成一类**，不能只在 BARE 里用否定环视排除。否则给 APSEC（官方逐字
    ``AoE (Anywhere on Earth)``）的日期格注入 ``/ UTC-12h`` 时，BARE 计数为 0、混用不成立，
    校验静默通过——那正是本库已两次明确「不得连坐」的 venue。

    日期格的判别（轮次 12 实测标定）：含 ``AoE`` 且含日期、长度 ≤140、不含句号 ``。``，
    且剥掉日期 / 时间 / 时区 / ``待补时刻`` / 标点后**残余不含中文**。前两条不足以排除备注列
    —— ICFEM 那处回归的第一层根因，正是一句中文备注被当成日期格。允许残余为 ASCII 标签
    （``Round 1`` / ``major revision`` / ``second round``），因为复合日期格合法存在。
    """
    has_date = re.compile(r"\d{4}-\d{2}-\d{2}")
    strip = re.compile(r"\d{4}-\d{2}-\d{2}|\d\d:\d\d(:\d\d)?|AoE|UTC-\d+h?"
                       r"|Anywhere on Earth|待补时刻|至|\.\."
                       # ⚠️ 不能用 \w —— Python 的 \w 在 Unicode 模式下连中文一起匹配，
                       # 会把散文格的中文剥光、残余变空，于是备注列被判成日期格（轮次 12 实测）。
                       r"|[\sA-Za-z0-9_.,;:()/（）；，、=\-—…*`+]")
    cjk = re.compile(r"[\u4e00-\u9fff]")

    # 日期格必须**以日期开头**，或以 ASCII 标签 + 冒号开头（`Round 1: 2023-12-15 …`）。
    # 仅「含日期」不够：纯 ASCII 英文备注若恰好含日期 + AoE 会被误判（轮次 13 M-2 实测）。
    # 但也不能只允许「以日期开头」——那会漏掉 ISSTA 2024 的 `Round 1: … ；Round 2: …`
    # 复合格（轮次 11 实测的召回缺口）。两条约束必须同时存在。
    starts_date = re.compile(r"^(?:\*\*)?(?:[A-Za-z][A-Za-z ]{0,24}\d?\s*[:：]\s*)?\d{4}-\d{2}-\d{2}")

    def is_datecell(c: str) -> bool:
        return ("AoE" in c and starts_date.match(c) is not None and len(c) <= 140
                and "。" not in c and cjk.search(strip.sub("", c)) is None)

    def forms(text: str, keep) -> set:
        out = set()
        for line in text.split("\n"):
            if not line.startswith("|") or re.match(r"\| `20\d\d-", line) or not keep(line):
                continue
            for c in (x.strip() for x in line.split("|")):
                if not is_datecell(c):
                    continue
                # 逐个 AoE 出现位置分类，复合格内混用也能发现。
                #
                # ⚠️ tail **必须截断在下一个 AoE 处**。用固定窗口会越界读到下一段的后缀：
                # `Round 1: … AoE；Round 2: … AoE / UTC-12h` 中首个裸 AoE 会被冒认成 UTC，
                # 于是格内混用检不出来（轮次 13 实测，一度让复合格召回归零）。
                #
                # ⚠️ 两种标记要**各自独立判定**，且不要求紧跟 AoE：
                # `AoE (Anywhere on Earth) / UTC-12h` 里 UTC 并不紧邻 AoE，
                # 若沿用「UTC 必须紧跟 AoE」的模式会漏判成纯 NAMED 而静默通过。
                pos = [m.start() for m in re.finditer(r"AoE", c)]
                for idx, st in enumerate(pos):
                    tail = c[st:pos[idx + 1] if idx + 1 < len(pos) else len(c)]
                    hit = set()
                    if re.search(r"UTC-\d", tail):
                        hit.add("UTC")
                    if "Anywhere on Earth" in tail:
                        hit.add("NAMED")
                    out |= hit or {"BARE"}
        return out

    tl = read(TIMELINE)
    bad, n_ok = [], 0
    for yp in sorted(glob.glob("*/[12][0-9][0-9][0-9]/README.md")):
        ven, yr = yp.split("/")[0], yp.split("/")[1]
        rp = f"{ven}/README.md"
        rt = read(rp) if os.path.exists(rp) else ""
        seen = (forms(read(yp), lambda l: True)
                | forms(rt, lambda l, y=yr: re.match(rf"\| \[`?{y}`?\]", l) is not None)
                | forms(tl, lambda l, p=f"/{ven}/{yr}/README.md": p in l))
        if len(seen) > 1:
            bad.append(f"{ven}/{yr}：{sorted(seen)}")
        elif seen:
            n_ok += 1
    if bad:
        fail(f"[tz-suffix] {len(bad)} 个 venue-year 的时区标注形态三方不一致："
             f"{bad[:5]}。同一 venue-year 不得混用 UTC / NAMED / BARE 三类标注。")
    stats.append(f"时区标注三方一致性: {n_ok} 个 venue-year 单一形态，{len(bad)} 个违规")


def check_relative_links() -> None:
    """仓库内相对链接目标存在。"""
    bad = []
    for path in sorted(glob.glob("**/*.md", recursive=True)):
        base = os.path.dirname(path)
        for m in re.finditer(r"\]\((\.{1,2}/[^)#\s]+)", read(path)):
            if not os.path.exists(os.path.normpath(os.path.join(base, m.group(1)))):
                bad.append(f"{path} -> {m.group(1)}")
    if bad:
        fail(f"[links] {len(bad)} 个相对链接目标缺失：{bad[:5]}")
    else:
        stats.append("相对链接: 0 断裂")


BOUNDARY = ("⚠️ 本脚本只查结构，抓不到散文与年度页中的旧事实；仍须执行 GUIDE §12.4 第 11 步的旧值 grep。\n"
            "   轮次 9 的 MSR 年度页缺口正落在本脚本盲区内——脚本通过只代表这些结构不变量成立。")


def main() -> int:
    ap = argparse.ArgumentParser(description="ccf_venues 结构一致性不变量校验")
    ap.add_argument("--today", default=None,
                    help="判定 §3 是否含已过期行的基准日 YYYY-MM-DD。"
                         "默认取 Asia/Shanghai 当天（本库统一时间口径），"
                         "而非系统本地时区——跨时区运行时二者可能差一天。")
    args = ap.parse_args()
    if args.today is None:
        args.today = (_dt.datetime.now(_dt.timezone.utc)
                      + _dt.timedelta(hours=8)).date().isoformat()

    if not os.path.exists(TIMELINE):
        print("请在 ccf_venues/ 目录下运行本脚本。", file=sys.stderr)
        return 2

    text = read(TIMELINE)
    check_year_tables(text)
    check_section3(text, args.today)
    check_mermaid(text)
    check_table_columns()
    check_stats()
    check_changelog_desc()
    check_timezone_suffix()
    check_relative_links()

    print(f"基准日: {args.today}（Asia/Shanghai）\n")
    print("统计（供人工对照，非校验）：")
    for s in stats:
        print(f"  · {s}")
    for n in notes:
        print(f"  · {n}")
    print()
    if failures:
        print(f"✗ {len(failures)} 项不变量违规：\n")
        for f in failures:
            print(f"  - {f}")
        print(f"\n{BOUNDARY}")
        return 1
    print("✓ 全部结构不变量通过。")
    print(BOUNDARY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
