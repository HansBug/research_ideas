#!/usr/bin/env python3
"""生成 54 个在评 pair 的人工重标工作单，⭐ 按 NL 组分目录。

用法：

    python3 generate.py                 # 生成 / 刷新全部 54 份（保留已填内容）
    python3 generate.py --pairs 0000 0009 0044
    python3 generate.py --sample 5      # 只做前 5 份样例
    python3 generate.py --check         # 只检查是否需要重新生成，不写盘

产物三类：

    HOWTO.md                # ⭐ 54 份共用的填写说明（⛔ 与具体 pair 无关）
    nl_XXXX/NL.md           # ⭐ 同一份 NL 的 6 个 pair 共用的 NL 材料
    nl_XXXX/<pair>.md       # 54 份工作单（⭐ 唯一有填写区的文件）

⭐ 目录名 `nl_XXXX` 取该 NL 组**最小的 pair id**，⛔ 分组判据是 NL 全文的 sha8 而
**不是** pair id 的末位数字 —— 两者在 `0002` / `0003` 这一对上**不一致**，
详见 [sources.py](./sources.py) 的 `_nl_dir_index()`。

⭐ **幂等**：重跑只更新材料部分，人工填写的内容按 key 原样保留（见 `fillblocks.py`）。
若某个 key 在新材料里消失（例如台账条目被改名），旧内容会被搬到文末的「孤儿填写区」，
⛔ 不会静默丢弃。⭐ `HOWTO.md` 与 `NL.md` 没有填写区，故整份重算。

⛔ 本脚本只读既有数据，**不写** `expected_issue_set.json`、不写任何 verdict、
不写任何 run record。产物只有上面三类 `.md` 与 `relabel/PROGRESS.md`。
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import candidate_mapping as CM                      # noqa: E402
import checklist                                    # noqa: E402
import dtier as DT                                  # noqa: E402
import fillblocks as fb                             # noqa: E402
import inspectfindings as IF                       # noqa: E402
import ledger_mapping as LM                         # noqa: E402
import newfields as NF                              # noqa: E402
import nl_zh                                        # noqa: E402
import sources as S                                 # noqa: E402
import terms as T                                   # noqa: E402
from pumlmodel import PumlModel                     # noqa: E402

SCHEMA = "paper1.relabel.worksheet.v1"
NL_SCHEMA = "paper1.relabel.nldoc.v1"
HOWTO_SCHEMA = "paper1.relabel.howto.v1"


# ------------------------------------------------------------------ 小工具

def numbered(text, start=1):
    out = []
    for i, line in enumerate(text.splitlines(), start=start):
        out.append(f"{i:3d} | {line}")
    return "\n".join(out)


def esc(text):
    """把可能破坏表格的字符转义，并压掉换行（表格单元格内不能有换行）。"""
    if text is None:
        return "—"
    t = re.sub(r"\s+", " ", str(text)).strip()
    return t.replace("|", "\\|")


def clip(text, n):
    t = esc(text)
    return t if len(t) <= n else t[: n - 1] + "…"


def codespan(text):
    """把一段文本包成 code span，⭐ 文本里**含反引号**时自动加长围栏。

    ⛔ 不这么做会静默炸掉：`response_within` 的官方 `meaning` 里就带着一对反引号
    （`` `response` is the state path … ``），用单反引号包起来渲染出的是三段错位的
    行内代码，⛔ 而源码看上去毫无问题。
    """
    t = str(text)
    if "`" not in t:
        return f"`{t}`"
    return f"`` {t} ``"


def oneline(text):
    """压成一行，⛔ 但**不**转义 `|` —— 用在列表项里，那里的竖线不撕表格。

    ⚠️ 与 `esc()` 的差别只在这一点上；⛔ 别拿 `esc()` 顶替，
    它会把 `dist_to_rear<5 & vel>30` 里的竖线换成 `\\|`，读者看到的就不是原文了。
    """
    return re.sub(r"\s+", " ", str(text or "")).strip()


def as_paragraphs(text):
    """把多行文本铺成「一行一段、段间空行」。

    ⛔ 目的不是排版好看，是**过 `tools/unwrap_markdown --check`**：CommonMark 把段内
    软换行渲染成一个空格，两个汉字之间折行就会多出一个空格。译者写的
    `translator_notes` 是按逻辑块换行的，⭐ 每块之间补一个空行即可，⛔ 不许直接原样塞进去。

    ⚠️ 行首的 `#` 会被降级成加粗：工作单本身用 `##`/`###` 组织，
    ⛔ 让译者的小标题参与进来会把文档大纲搅乱。

    ⭐ 连续的列表项之间**不**插空行 —— unwrap 把每个列表项当独立逻辑行，
    ⛔ 硬插空行只会把紧凑列表变成松散列表，多出一堆无谓的段落间距。
    """
    listish = re.compile(r"^([-*+]|\d{1,9}[.)])\s+")
    kept = []
    for raw in str(text or "").splitlines():
        ln = raw.strip()
        if not ln:
            continue
        m = re.match(r"^#{1,6}\s+(.*)$", ln)
        if m:
            ln = f"**{m.group(1).strip()}**"
        kept.append(ln)
    out = []
    for i, ln in enumerate(kept):
        out.append(ln)
        nxt = kept[i + 1] if i + 1 < len(kept) else None
        if nxt is not None and listish.match(ln) and listish.match(nxt):
            continue
        out.append("")
    return out




def regroup_unmatched(entries, model):
    """把去重组再按「所指的模型元素」并一层。

    ⚠️ `export_unmatched.py` 的去重只按逐字文本，同一主张换个说法就分成两组
    （实测 0000 的 X1 侧 12 组里有 6 组都在说 `HumanDrivingMode` 的空状态体）。
    这里再并一次：

    - X1 侧有多报桶回链的，直接按**簇**并 —— 那是人工判过的同一主张。
    - 否则按「该 issue 文本里点到的模型元素集合」并 —— 元素集合相同的多半同根。
    - 都没有就退回逐字。

    ⛔ 并组只影响**展示**，每组仍逐条列出成员原文，不丢信息。
    """
    element_tokens = set()
    for name in model.states:
        element_tokens.add(name.lower())
    for trig in model.triggers():
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", trig):
            element_tokens.add(tok.lower())
    for var in model.variable_candidates():
        element_tokens.add(var.lower())

    groups = {}
    for e in entries:
        adj = e.get("adjudicated") or {}
        if adj.get("cluster"):
            key = ("cluster", adj["cluster"])
        else:
            blob = f"{e.get('issue') or ''} {e.get('where') or ''}"
            # ⛔ 必须用**有序**元组而不是 frozenset —— `str(frozenset)` 的元素顺序
            # 随 PYTHONHASHSEED 变，会让同一份材料每次生成出不同的行序，幂等直接失效
            # （实测：54 份里有 16 份每跑一次就变一次）。
            hit = tuple(sorted({t.lower() for t in
                                re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", blob)
                                if t.lower() in element_tokens}))
            key = ("elem", hit) if hit else ("text", e.get("key"))
        g = groups.setdefault(key, {
            "key": key, "arm": e["arm"], "cells": set(), "members": [],
            "adjudicated": adj or None,
        })
        g["cells"] |= set(e.get("cells") or [])
        g["members"].append(e)
        if adj and not g["adjudicated"]:
            g["adjudicated"] = adj
    out = list(groups.values())
    for g in out:
        g["cell_count"] = len(g["cells"])
        g["members"].sort(key=lambda m: -m.get("cell_count", 0))
    out.sort(key=lambda g: (-g["cell_count"], str(g["key"])))
    return out


# ------------------------------------------------------------------ 怎么填

def _howto_inline(pair):
    """⭐ 工作单**最开头**的「怎么填」——⛔ 每一条都是 `collect.py` 的一处真实解析行为。

    ⚠️ **这一节不许凭想象写。** 它规定的是「怎么写才会被回收」，⛔ 说明与实现一旦不符，
    判读者会照着说明填、⛔ 而内容被静默丢掉 —— ⭐ 那比没有说明更坏。
    因此每一条都有一个对应的 parser 行为测试（`test_relabel.py` 的
    「怎么填 · 逐条钉住 parser 行为」一组），⛔ 改这里必须同时改那里。

    ⭐ 记号集合读的是 [fillblocks.py](./fillblocks.py) 的 `CHECK_MARKS`，⛔ 不在这里写死 ——
    ⚠️ 写死就会与解析器分叉，而那正是本节要防的事。

    ⛔ 刻意**不**放长篇 rationale（为什么这么分层、`basis` 与 `layer` 的关系之类）：
    那些在 [HOWTO.md](./HOWTO.md)。⭐ 本节只回答「手该怎么动」。
    """
    marks = "  ".join(f"`[{m}]`" for m in fb.CHECK_MARKS if m != "x")
    lines = []
    lines.append("## 怎么填（先读这 8 条 —— 写法不对会被**静默丢掉**）")
    lines.append("")
    lines.append(
        "回收脚本是 [collect.py](../collect.py)；下面每一条都是它的一处**真实解析行为**，"
        "不是礼貌约定。逐字段的取值含义与判据在 "
        f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO})，本节只讲手该怎么动。"
    )
    lines.append("")
    lines.append(
        "1. **只在 `~~~` 围栏里写。** `<!-- FILL:BEGIN … -->` 与 `<!-- FILL:END … -->` "
        "两行是回收锚点，不许改、不许删。围栏**外**写的字，重跑生成器就没了。"
    )
    lines.append(
        f"2. **勾选写 `[x]`。** {marks} 同样认（大小写都行）。⚠️ 别写 `[v]` `[是]` "
        "`[o]` `[1]` `[*]` —— 不认的记号会让**那一个选项连同它的文字一起消失**，"
        "看起来就像你没勾。"
    )
    lines.append(
        "3. **勾完别删掉后面的选项文字。** ⚠️ 取值就是**框后面那段文字**，不是框的位置："
        "只留 `裁决: [x]` 等于**没勾**。"
    )
    lines.append(
        "4. **单选就只勾一个。** 勾两个不是「两个都算」，"
        "是 [validate.py](../validate.py) 报「该字段是单值」。"
    )
    lines.append(
        "5. **自由文本写在 `字段名:` 的冒号后面**（半角 `:` 与全角 `：` 都认），"
        "可以换行接着往下写，续行里带冒号也不会被截断。"
        "但**别改字段名** —— 改了那一行会被并进上一个字段。"
    )
    lines.append(
        "6. **§4 清单**：勾在行首那个 `[ ]` 里（前面有缩进或 `-` 都行，id 别动），"
        "发现写在它下面的 `发现:` 后面 —— 直接写在下一行也收。"
        "唯一不回收的是 `·` 开头那行：那是机器给的机械判据。"
    )
    lines.append(
        f"7. **§5 每条新增以 `### NEW-{pair}-01` 这样的标题单独起头**，"
        "别把两条挤在一个标题下，也别漏掉 `NEW-` 前缀。"
    )
    lines.append(
        "8. **不适用就留空**（回收成 `null`）；查过了、结论是「没有」，"
        "写 `无`（`none` / `N/A` / `-` 同义）。「留空」与「写 `无`」在校验时是两件事。"
    )
    lines.append("")
    return lines


# ------------------------------------------------------------------ §1 原料

def _nl_verbatim_block(pair, segs):
    """⭐ §1.1：NL 原文 + 中文严格翻译三列表，⭐ 放在**第一屏**。

    ⚠️ **本函数的输出在同组 6 份工作单里必须逐字节相同** —— 它只允许读组级事实
    （原文、译文、段 id），⛔ 一个 pair 级数字都不许进来。
    `test_nl_verbatim_block_is_byte_identical_across_siblings` 钉住这一点。

    ⛔ **只搬原文与译文。** 逐段判读提示（`note`）与整份观察（`translator_notes`）留在
    `NL.md`：⭐ 它们更长，⛔ 且历史上出过「提示里写了制品断言、于是对同组另外 5 份为假」
    的事故（[README.md](./README.md) §十）。⭐ 原文与译文不谈制品，故复制零风险。

    ⚠️ **2026-08-13 删掉了表前的三段前言**（共用 NL / sha8 与分段口径、译文纪律、
    两种方括号标注的图例）：⛔ 用户要的是「表直接跟在标题后面」。⭐ 三段里那两样
    **不能凭空消失**的信息（分段口径含段 id 范围、译文口径与方括号含义）搬到了
    `nl_XXXX/NL.md` 的开头与 §1，⛔ 且这里**不留**指向它们的说明段 —— 工作单头部
    已经写着「开工前两份必读」，⭐ 再加一句就又是一段前言。
    """
    sibs = S.nl_siblings(pair)
    lines = []
    lines.append("### §1.1 NL 规约原文与中文严格翻译（判读起点，先读这一节）")
    lines.append("")
    lines.append("| 段 id | 原文 | 中文严格翻译 |")
    lines.append("| :-- | :-- | :-- |")
    for sid, txt in segs:
        zh = nl_zh.translate(pair, sid)
        lines.append(f"| `{sid}` | {esc(txt)} | "
                     f"{esc(zh) if zh else '缺译文 —— 见 nl_zh.py'} |")
    lines.append("")
    lines.append(
        f"**还有两样材料在同组共用的 [{S.NL_DOC}](./{S.NL_DOC}) 里**，"
        f"篇幅关系不搬进来：**逐段判读提示**（该段约束了哪个元素 · 歧义点在哪）与"
        f"**整份 NL 层面的观察**（术语表 · 跨句反复出现的歧义 · 原文质量问题）。"
        f"⚠️ 那些提示**不含任何关于被测制品的断言** —— 一份 NL 服务 {len(sibs)} 个制品，"
        f"讲制品的话必然对其中 {len(sibs) - 1} 份为假。所以「这个状态在不在」"
        f"「这条边有没有」一律到本页 §1.2（作者源，带行号）与 §4（按本 pair 现算的清单）自己核。"
    )
    lines.append("")
    return lines


def section_material(pair, model):
    # ⚠️ `records` 参数 2026-08-13 随结构摘要一并去掉 —— 它只被那张表的
    # 「台账现有条目」一格用到。⛔ 留着一个没人读的参数，下一个人会以为本节还依赖台账。
    segs, _ = S.nl_segments(pair)
    puml = S.puml_text(pair)
    ref, ref_note = S.reference_puml(pair)
    meta = S.source_meta(pair)
    su = model.summary()

    lines = []
    lines.append("## §1 判断所需的全部原料")
    lines.append("")
    lines.append(
        # ⛔ 全部走 esc()：`model_name` 等字段里有真实换行，直接插进段落会造成
        # Markdown 段内硬折行（CommonMark 把软换行渲染成一个空格，中文段落会多出空格）。
        f"生成方 LLM **{esc(meta.get('llm'))}**；来源系统 **{esc(meta.get('model_source'))} / "
        f"{esc(meta.get('model_name'))}**；被测制品取自作者 workbook 的 "
        f"`{esc(meta.get('selected_stage_column'))}`（单元格 `{esc(meta.get('selected_stage_cell'))}`）。"
        f"NL 与 5 个兄弟 pair 共用（同一份规约生成 6 个制品）。"
    )
    lines.append("")

    # ---- NL 原文与译文：⭐ **第一屏**。
    # ⛔ 这一节的字节在同组 6 份工作单里**完全相同** —— 它只用到组级事实
    # （NL 原文、译文、sha8、段 id、兄弟列表），⛔ 一个 pair 级的数字都没有。
    # ⚠️ 复制的边界是刻意划的：**只搬原文与译文**，逐段判读提示与整份观察留在 `NL.md`。
    # ⛔ 提示更长，且历史上出过跨 pair 污染事故（README §十）—— 一份 NL 服务 6 个制品，
    # 提示里只要出现一句制品断言，对其中 5 份就是假的。原文与译文不谈制品，故复制零风险。
    lines += _nl_verbatim_block(pair, segs)

    # ---- 作者源
    #
    # ⚠️ **结构摘要（旧 §1.2）2026-08-13 整节删除**，含它下面那段「作者源口径 vs 谓词层
    # `cardinality` 口径」的脚注 —— ⛔ 用户判定它不需要，⭐ 要的是「干净清爽」。
    # ⭐ 后续小节顺次上移（作者源 由 §1.3 变 §1.2、参考模型 由 §1.4 变 §1.3），⛔ 不留空号。
    # ⭐ 两段**条件性告警**（区分隔符、解析告警）不是摘要的一部分，只是当年顺手挂在那里的，
    # ⛔ 删掉它们会真的丢信息（越界判据 / 解析可靠性），故移到本节 —— ⭐ 它们讲的正是
    # 下面这份作者源。⛔ 那段双口径脚注则按用户要求随摘要一并删除，其长版仍在
    # `HOWTO.md` §A.1（该节已改锚到本节）。
    lines.append("### §1.2 作者源 PlantUML（被测制品，带行号）")
    lines.append("")
    lines.append(
        "行号就是引用锚点 —— 裁决理由里写 `:12` 即指这里的第 12 行。"
    )
    lines.append("")
    if su["region_separators"]:
        lines.append(
            f"⚠️ 作者源含 **{su['region_separators']} 个 `--` 区分隔符**。"
            "正交区并发不在 project_1 的建模对象内（$M$ 无区分量）—— "
            "但**这不等于不许记**：维度 A 有一个界外取值 `region`，"
            "凡「这两个区是否同时活跃」「区应当有几个」类主张照常登记并勾它，"
            "它会被**记录但不计入缺陷统计**（`counts_as_defect = false`）。"
            "同一段文本里的**顺序结构**主张（可达性、边声明、层次）在范围内，照常计分。"
        )
        lines.append("")
    if model.parse_warnings:
        lines.append("解析告警：" + "；".join(model.parse_warnings))
        lines.append("")
    lines.append("```text")
    lines.append(numbered(puml))
    lines.append("```")
    lines.append("")

    # ---- 参考模型
    lines.append("### §1.3 参考模型 PlantUML")
    lines.append("")
    if ref:
        lines.append(
            f"来源：作者 workbook `{ref_note}`。"
            "**参考模型不是正确答案**，只作对照、不作判据 —— "
            "语料里多处出现**参考侧比生成侧更差**的情形（例如 `0000` 的参考模型压根没声明 "
            "`autonomous_mode` 的状态体）。它只是「另一个人怎么建的」（更长的说明见 "
            f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §A.2）。"
        )
        lines.append("")
        lines.append("```text")
        lines.append(numbered(ref))
        lines.append("```")
    else:
        lines.append(f"不可用：{ref_note}")
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ NL 材料页

def build_nl_doc(dirname):
    """渲染 `nl_XXXX/NL.md` —— ⭐ 同一份 NL 的 6 个 pair 共用一份材料。

    ⭐ 这是本次目录重构的核心收益：NL 原文、译文、逐段判读提示、整份观察此前被逐字
    复制进 6 份工作单（实测每份 44 到 125 行），⛔ 而它们**逐字节相同**。
    ⚠️ 更要紧的不是行数：一份 NL 服务 6 个不同制品，材料若复制六份，
    「这段提示对哪一份为真」就变成了六个独立的问题，⛔ 而 [README.md](../README.md) §十
    记的那起事故正是这么发生的。⭐ 只留一份，问题就只有一个。
    """
    pairs = S.pairs_of_dir(dirname)
    pair = pairs[0]                    # ⭐ 组内任一 pair 的 NL 材料逐字节相同
    segs, seg_mode = S.nl_segments(pair)
    nl = S.nl_text(pair)
    src = nl_zh.source_file(pair)

    lines = []
    lines.append(f"<!-- RELABEL schema={NL_SCHEMA} nl_dir={dirname} -->")
    lines.append(f"# NL 规约材料 · `{dirname}`")
    lines.append("")
    lines.append(
        "本文件由 [generate.py](../generate.py) 生成，**没有任何填写区** —— "
        "它是只读材料。判读要填的东西全在同目录的 `<pair>.md` 里。"
    )
    lines.append("")
    lines.append(
        f"本页服务同目录的 **{len(pairs)}** 份工作单："
        + "、".join(f"[`{p}`](./{p}.md)" for p in pairs)
        + f"。它们由**同一份 NL 规约**（sha8 `{S.nl_sha8(pair)}`）生成 "
          f"{len(pairs)} 个不同制品，所以 NL 侧材料只有一份，制品侧各不相同。"
    )
    lines.append("")
    # ⭐ **段 id 范围（`NL-M001` … `NL-M006` 这一段）2026-08-13 从工作单搬到这里。**
    # ⛔ 工作单表前的三段前言被整段删掉了（用户要「干净」），⚠️ 而分段口径与段 id 范围
    # 是判读者填 `nl_evidence` 时必须知道的两样东西 —— ⛔ 不能凭空消失，故落在本页。
    mode_zh, mode_what = T.SEG_MODE_ZH.get(
        seg_mode, ("该分段口径的语义仓库未定义", "仓库未定义"))
    # ⭐ `mode_what` 里那个路径在 `terms.py` 里是代码样式，⛔ 这里换成可点击链接 ——
    # ⚠️ 不要另加一句「人工标注取自 …」，⛔ 那会把同一件事说两遍（实测出过一次）。
    what = mode_what.replace(
        "`corpora/nl_segmentation/overrides.json`",
        "[corpora/nl_segmentation/overrides.json]"
        "(../../../../corpora/nl_segmentation/overrides.json)")
    lines.append(
        f"分段口径 {T.bi(seg_mode, mode_zh)}：{what}"
        f"，共 **{len(segs)}** 段（`{segs[0][0]}` … `{segs[-1][0]}`）。"
        "台账里的「NL 第 N 句」与你要在工作单 §5 填的 `nl_evidence` 都按这套段 id 读。"
    )
    lines.append("")

    lines.append("## §1 译文纪律（先读这三段再看表）")
    lines.append("")
    lines.append(
        "**译文是给人判缺陷用的，不是给人读着舒服用的。** 它严格直译，"
        "不意译、不润色、不补原文没有的信息（含不补主语、不补量词、"
        "不补逻辑连接词）；状态名 / 事件名 / 变量名 / 守卫表达式一律**保留英文原样**，"
        "建模术语保留英文并在紧跟的括号里给中文。"
        "⚠️ 原文含糊的地方译文**照样含糊** —— 替它消歧就等于替你做了本轮要你自己做的判断。"
        "⚠️ 译文是**辅助**，判据仍以英文原文为准；两者不一致时以原文为准并请回报。"
    )
    lines.append("")
    lines.append(
        "两种方括号标注的含义：`〔原文如此：…〕` 指**原文自身**有语法 / 拼写 / 数格错误，"
        "译文照直译并说明错在哪 —— 它不是译文的错，也不构成模型的缺陷；"
        "`〔译者存疑：…〕` 指**原文这里没说清**（谁是主语、并列项是「且」还是「或」、"
        "源状态是哪个），它直接决定判缺陷时这一句**能不能**用来说模型「违反」了什么。"
    )
    lines.append("")
    lines.append(
        "口径与验收依据："
        "[translations/TRANSLATION_SPEC.md](../translations/TRANSLATION_SPEC.md)；"
        f"本份译文的原始 JSON：[translations/{src}](../translations/{src})；"
        "装载与对拍：[nl_zh.py](../nl_zh.py)。"
    )
    lines.append("")

    lines.append("## §2 逐段：原文与中文严格翻译")
    lines.append("")
    lines.append("| 段 id | 原文 | 中文严格翻译 |")
    lines.append("| :-- | :-- | :-- |")
    for sid, txt in segs:
        zh = nl_zh.translate(pair, sid)
        lines.append(f"| `{sid}` | {esc(txt)} | "
                     f"{esc(zh) if zh else '缺译文 —— 见 nl_zh.py'} |")
    lines.append("")

    lines.append("## §3 逐段判读提示（该段约束了哪个元素 · 歧义点 · 边界外部分）")
    lines.append("")
    lines.append(
        "提示只陈述「原文这一句说了什么、没说什么」，不含任何裁决 —— "
        "「所以模型应该怎样」是本轮要你自己填的，材料不替你填。"
    )
    lines.append("")
    lines.append(
        "**提示里也不含任何关于被测制品的断言** —— 一份 NL 服务 "
        f"{len(pairs)} 个 pair，这一页是 {len(pairs)} 份工作单共用的，"
        "讲制品的话必然对其中 5 份为假。"
        "因此「这个状态在不在」「这条边有没有」一律请自己到各份工作单的 §1.2"
        "（作者源，带行号）与 §4（按该 pair 现算的清单）核对，不要指望提示替你回答。"
        "2026-08-13 之前的旧版工作单**违反过这一条**，"
        "若你读过旧版，见 [README.md](../README.md) §十。"
    )
    lines.append("")
    for sid, _txt in segs:
        nt = nl_zh.note(pair, sid)
        lines.append(f"- `{sid}`：{oneline(nt) if nt else '译者未给提示'}")
    lines.append("")

    tn = nl_zh.translator_notes(pair)
    if tn:
        lines.append("## §4 整份 NL 层面的观察（术语表 · 跨句反复出现的歧义 · 原文质量问题）")
        lines.append("")
        lines += as_paragraphs(tn)

    lines.append("## §5 NL 原始字节（带物理行号）")
    lines.append("")
    lines.append("```text")
    lines.append(numbered(nl))
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ §2 台账逐条

#: 映射块的抬头。⛔ 每一处映射都必须带着它 —— 见 `_fmt_mapping()` 的 docstring。
MAPPING_CAVEAT = (
    "**我方到新座标系的映射（推断，供参考）** —— "
    "这是我们读该条正文后自己判的，不是已经定下来的事实。"
    "你不同意就按你自己的判断填下面的裁决与理由，**你的裁决优先**。"
)

#: 候选侧映射块的抬头。⚠️ 比台账侧多一层保留：候选本身尚未被认定。
CANDIDATE_MAPPING_CAVEAT = (
    "**我方到新座标系的映射（推断，供参考）** —— "
    "映射的是「**若这条线索成立**，它属于哪一格」，"
    "**不代表它成立**；它是不是一条真缺陷，正是要你判的。"
    "你不同意就按你自己的判断填下面的裁决与理由，**你的裁决优先**。"
)


def _fmt_mapping(rec, caveat=MAPPING_CAVEAT):
    """把一条映射渲染成工作单里的一小节。

    ⛔⛔ **`caveat` 不许省。** 这一整块是**我方推断**，而它印在裁决块正上方 ——
    判读者动笔前读到的最后一样东西。⚠️ 不写明它是推断，判读者会把它当成已经定下来的
    分类，于是「裁决」退化成对我方判断的复读，⛔ 而本轮要的恰恰是他独立的那一份。

    映射不上时印出卡点类别与理由原话，⛔ 不留空白：判读者需要知道
    「这一条我们也没判出来」，⭐ 那本身就是要他重点看的信号。
    """
    out = [caveat, ""]
    if not rec:
        out += ["（本条尚无映射记录。）", ""]
        return out
    if not rec.get("mappable"):
        blocker = rec.get("blocker")
        zh = CM.BLOCKER_ZH.get(blocker)
        head = f"**我方没能映射**（卡点：{zh[0]}）" if zh else "**我方没能映射**"
        out += [head, "", f"- {esc(rec.get('note'))}", ""]
        if zh:
            out += [f"- 这类卡点的含义：{zh[1]}", ""]
        return out
    out += ["| 轴 | 我方判的取值 |", "| :-- | :-- |"]
    out_of_scope = []
    for axis in ("defect_locus", "defect_element", "defect_qualifier",
                 "defect_logic_kind", "defect_reference"):
        val = rec.get(axis)
        if not val:
            continue
        out.append(f"| `{axis}` | {T.bi(val, NF.ZH[axis].get(val))} |")
        if not NF.counts_as_defect(axis, val):
            out_of_scope.append((axis, val))
    out.append("")
    # ⭐ 界外取值必须当场写明它不计分 —— ⛔ 只印一个 `region` 而不说它不计入统计，
    # 判读者会把它当成一条普通缺陷，⛔ 而那正好是 CLAUDE.md 边界禁止的两种误读之一。
    for axis, val in out_of_scope:
        out.append(f"- **界外取值、不计分** —— `{axis} = {val}`：{NF.OUT_OF_SCOPE_VALUES[(axis, val)]}")
    if out_of_scope:
        out.append("")
    # ⭐ 任一轴取 `other` 时的说明。⛔ 不许省：出口不写清等于没分类，
    # 而判读者要判的正是「我们这一格判对了没有」。
    if (rec.get(NF.OTHER_NOTE_FIELD) or "").strip():
        out.append(f"- `other` 说明：{esc(rec.get(NF.OTHER_NOTE_FIELD))}")
        out.append("")
    out.append(f"- 依据（原文逐字片段）：{esc(rec.get('evidence'))}")
    if (rec.get("note") or "").strip():
        out.append(f"- 判定说明：{esc(rec.get('note'))}")
    out.append("")
    return out


def section_ledger(pair, records, saved):
    lines = []
    lines.append("## §2 现有 expected issue 逐条裁决")
    lines.append("")
    if not records:
        lines.append(
            "**本 pair 台账 0 条。** 这不等于「本 pair 没问题」—— 请直接从 §3 与 §4 "
            f"开始，把发现登记到 §5；理由见 [{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.1。"
        )
        lines.append("")
        return "\n".join(lines), []

    keys = []
    lines.append(
        f"本 pair 共 **{len(records)}** 条。裁决区已按三方判读与人工 meta review 预填"
        f"（同意就删掉理由末尾那个括号，不同意直接改写）；自动风险标记只是**提示** —— "
        "**打了标记不等于该条不成立，没打标记也不等于它成立**（标记怎么打出来的见 "
        f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.1）。"
    )
    lines.append("")
    for rec in records:
        rid = rec["id"]
        keys.append(rid)
        flags = S.risk_flags(rec)
        lines.append(f"### {rid}{DT.mark(rid)}")
        lines.append("")
        # ⛔⛔ 这里**只印三样**：statement 原文、参考侧 / 生成侧证据行、以及我方到新座标
        # 系的映射。2026-08-13 剥掉的十项（`layer` / `direction` / `element_of_M` /
        # `decided_by` / `primary_predicate` / `nl_evidence` / `verdict` / `replay` /
        # 同质组 / 上游）与整节断言组都**不再呈现**。
        #
        # ⚠️ 剥掉的理由不是嫌长，是**锚定**：那十项里有七项是我们自家框架给这一条贴的标签
        # （四层归因、八方向、$M$ 分量、分层判定来源、主谓词……），⛔ 而本轮要判读者回答的
        # 恰恰是「这套框架有没有漏掉东西」。⛔ 先把框架的答案印在题面上，判读者就只会在
        # 那些格子之间挑一个。⛔ `verdict` / `replay` 更直接：它们是流水线的判定与复算结论，
        # ⛔ 印出来等于先告诉判读者「标准答案」。
        lines.append("**statement 原文**")
        lines.append("")
        lines.append("> " + (rec.get("statement") or "").replace("\n", "\n> "))
        lines.append("")
        if rec.get("reference_side") or rec.get("generated_side"):
            lines.append(f"- 参考侧：{esc(rec.get('reference_side'))}")
            lines.append(f"- 生成侧：{esc(rec.get('generated_side'))}")
            lines.append("")
        lines.extend(_fmt_mapping(LM.for_record(rid)))
        # ⭐ 三方独立 D 档判读。⛔ 摆在映射之后、裁决区之前：它是判读材料，不是我方结论。
        lines.extend(DT.block(rid))
        # ⭐ 判为「与本条是同一个问题」的 inspect 发现挂在这里。⛔ 上面的 statement 与证据行
        # 一个字都没改 —— 它们是**被判对象**；补充证据只进一个独立折叠区，且**不另设裁决区**。
        lines.extend(inspect_supplement(rid))
        if flags:
            lines.append("**自动风险标记**")
            lines.append("")
            for _, msg in flags:
                lines.append(f"- {msg}")
            lines.append("")
        lines.append(fb.render(rid, "ledger",
                               DT.prefill(rid, "ledger") or fb.LEDGER_TEMPLATE,
                               saved.get(rid)))
        lines.append("")
    return "\n".join(lines), keys


# ------------------------------------------------------------------ §3 候选

_DIFF_VERDICT_NOTE = {
    "problem": "判定者当年**判为 problem**，却仍未进台账 —— 最值得优先看的一类。",
    "extra": "判为 `extra`（生成方凭空新增）。台账的 8 类分类学**没有 `extra` 的槽位**，"
             "整类 31 条 / 20% 被结构性漏掉（见 `docs/protocol/ground_truth_limitations.md` §3）。",
    "uncertain": "判为 `uncertain`（当年未决）。",
    "correct": "判为 `correct`（生成方在该点上正确）。",
    "similar": "判为 `similar`（与参考侧等价）。",
}


def section_candidates(pair, model, records, saved):
    lines = []
    keys = []
    lines.append("## §3 候选 issue 逐条裁决")
    lines.append("")
    lines.append(
        "本节把**已知但未入账**的线索集中在一处。它们都没有经过人工确认；"
        "裁决区已按三方判读与人工 meta review 预填，你同意就删掉理由末尾那个括号 —— "
        f"六个来源的优先级与读法见 [{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.2。"
    )
    lines.append("")

    # ---- §3.1 真漏记
    vu = S.valid_unrecorded(pair)
    lines.append("**§3.1 两臂多报侧判定的「真漏记」（`VALID_UNRECORDED`）**")
    lines.append("")
    if not vu:
        lines.append("本 pair 无。（全语料 X1 侧 13 条、主臂侧 2 条。）")
        lines.append("")
    else:
        lines.append(
            f"**本 pair {len(vu)} 条 —— 最高优先级**（已过一轮独立复核）。"
        )
        lines.append("")
        for i, r in enumerate(vu, 1):
            key = f"VU-{pair}-{i:02d}"
            keys.append(key)
            lines.append(f"### {key}{DT.mark(key)} · 簇 `{r.get('cluster')}`（{r.get('_arm')} 臂，"
                         f"子类 `{r.get('subclass')}`）")
            lines.append("")
            if r.get("claim"):
                lines.append("**主张**：" + esc(r["claim"]))
                lines.append("")
            lines.append("**复核认定的事实**")
            lines.append("")
            lines.append("> " + (r.get("fact") or "").replace("\n", "\n> "))
            lines.append("")
            if r.get("nl"):
                lines.append("**NL 侧说明**")
                lines.append("")
                lines.append("> " + (r.get("nl") or "").replace("\n", "\n> "))
                lines.append("")
            if r.get("note"):
                lines.append("**备注**：" + esc(r["note"]))
                lines.append("")
            if r.get("members"):
                lines.append(f"**出现在**：{len(r['members'])} 个格 —— "
                             + "、".join(f"`{m}`" for m in r["members"][:8])
                             + (" …" if len(r["members"]) > 8 else ""))
                lines.append("")
            lines.extend(_fmt_mapping(CM.for_candidate(key), CANDIDATE_MAPPING_CAVEAT))
            lines.extend(inspect_supplement(key))
            lines.extend(DT.block(key))
            lines.append(fb.render(key, "candidate",
                                   DT.prefill(key, "candidate") or fb.CANDIDATE_TEMPLATE,
                                   saved.get(key)))
            lines.append("")

    # ---- §3.2 审阅 agent 未采纳的 diff
    unadopted = S.unadopted_diffs(pair)
    adopted = S.adopted_diff_ids(pair)
    rv = S.review_json(pair)
    total_diffs = len(rv.get("diffs") or []) if rv else 0
    lines.append("**§3.2 审阅 agent 产出但未进台账的 diff**")
    lines.append("")
    if rv is None:
        lines.append(f"无 `{pair}-review.json`。")
        lines.append("")
    else:
        lines.append(
            f"本 pair 审阅 agent 共产出 **{total_diffs}** 条 diff，进台账 **{len(adopted)}** 条，"
            f"未进 **{len(unadopted)}** 条。当年没有单独记录「为什么不收」 —— "
            f"证据缺口见 [{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.2。"
        )
        lines.append("")
        priority = [(i, d) for i, d in unadopted
                    if d.get("verdict") in ("problem", "extra", "uncertain")]
        rest = [(i, d) for i, d in unadopted
                if d.get("verdict") not in ("problem", "extra", "uncertain")]
        # ⚠️⚠️ 这两族**不是同一个物种**，⛔ 故分成两节印，⛔ 不混在一张表里。
        # 判据是字面的、可在页面上自行核对（就是下面那行「生成侧：—」），
        # 定义与理由见 `sources.denies_artifact_defect()`。
        claims = [(i, d) for i, d in priority if not S.denies_artifact_defect(d)]
        denials = [(i, d) for i, d in priority if S.denies_artifact_defect(d)]

        def _render_diff(i, d):
            key = f"DIFF-{pair}-{i:02d}"
            keys.append(key)
            lines.append(f"### {key}{DT.mark(key)} · diff #{i} · `{d.get('verdict')}`")
            lines.append("")
            lines.append(f"- 参考侧：{esc(d.get('ref'))}")
            lines.append(f"- 生成侧：{esc(d.get('gen'))}")
            lines.append("")
            lines.append("**判定者理由**")
            lines.append("")
            lines.append("> " + (d.get("reason") or "").replace("\n", "\n> "))
            lines.append("")
            aux = []
            if d.get("assertable") is not None:
                aux.append(f"`assertable` = `{d.get('assertable')}`")
            if d.get("predicate_exists") is not None:
                aux.append(f"`predicate_exists` = `{d.get('predicate_exists')}`")
            if d.get("out_of_scope") is not None:
                aux.append(f"`out_of_scope` = `{d.get('out_of_scope')}`")
            if aux:
                lines.append("排除相关字段：" + "；".join(aux))
                lines.append("")
            lines.extend(_fmt_mapping(CM.for_candidate(key), CANDIDATE_MAPPING_CAVEAT))
            lines.extend(inspect_supplement(key))
            lines.extend(DT.block(key))
            lines.append(fb.render(key, "candidate",
                                   DT.prefill(key, "candidate") or fb.CANDIDATE_TEMPLATE,
                                   saved.get(key)))
            lines.append("")

        if claims:
            lines.append(f"**§3.2a 判为 problem / extra / uncertain 的 {len(claims)} 条（设裁决区）**")
            lines.append("")
            for i, d in claims:
                _render_diff(i, d)
        if denials:
            lines.append(f"**§3.2a-2 生成侧写「—」或「不可能生成」的 {len(denials)} 条"
                         f"（另一个物种，设裁决区）")
            lines.append("")
            lines.append(
                "这几条的**生成侧逐字否认作者制品在该处有东西**。它们真正主张的是"
                "**参考模型 / 真值本身的有效性**（「参考侧含 NL 推不出的内容，"
                "任何 LLM 都无法复现，却会被计成漏检」），而不是一种缺陷形态。"
            )
            lines.append("")
            lines.append(
                "分出来是因为它们与上面那些不可比：缺陷座标系的判定测试全部落在"
                "**作者源 PlantUML** 上，而这类在制品内指不出任何一处。"
                "所以它们映射不上**不能**算作「新座标系覆盖不到」—— "
                "它们本来就不在座标系要描述的对象集合里。"
            )
            lines.append("")
            lines.append(
                "它们仍然值得判：若你认为某条其实指出了制品的真问题，照常走「采纳」；"
                "若你认为它是对参考模型的质疑，那是另一回事，请在理由里写清楚。"
            )
            lines.append("")
            for i, d in denials:
                _render_diff(i, d)
        if rest:
            lines.append(f"**§3.2b 判为 correct / similar 的 {len(rest)} 条（备查，不设裁决区）**")
            lines.append("")
            lines.append(
                f"<details><summary>展开 {len(rest)} 条备查 diff —— "
                f"不是候选，只在 §4 发现同一处时用来查「是否已被判过没问题」"
                f"（读法见 {S.WORKSHEET_HOWTO} §D.2）</summary>")
            lines.append("")
            lines.append("| # | 判定 | 参考侧 | 生成侧 | 理由（截断） |")
            lines.append("| --: | :-- | :-- | :-- | :-- |")
            for i, d in rest:
                lines.append(f"| {i} | `{d.get('verdict')}` | {clip(d.get('ref'), 60)} | "
                             f"{clip(d.get('gen'), 60)} | {clip(d.get('reason'), 140)} |")
            lines.append("")
            lines.append("</details>")
            lines.append("")

    # ---- §3.3 机械未匹配
    um = S.unmatched_issues(pair)
    lines.append("**§3.3 两臂产出中机械未匹配任何台账条目的 issue**")
    lines.append("")
    if um is None:
        lines.append(
            "**未导出。** 先跑 `python3 export_unmatched.py`（它读 `runs/` 下的原始 run "
            "record；主臂 v46 的记录在姊妹 clone `research_ideas/` 里）。"
        )
        lines.append("")
    elif not um:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        x1 = regroup_unmatched([e for e in um if e["arm"] == "X1"], model)
        v46 = regroup_unmatched([e for e in um if e["arm"] == "v46"], model)
        raw_x1 = sum(e["cell_count"] for e in um if e["arm"] == "X1")
        raw_v46 = sum(e["cell_count"] for e in um if e["arm"] == "v46")
        lines.append(
            f"X1 臂 **{raw_x1}** 条未认领 issue 并成 **{len(x1)}** 组；"
            f"主臂 **{raw_v46}** 条机械未匹配 issue 并成 **{len(v46)}** 组。"
            "**出现格数越多越值得看**；两臂既有裁定都可以推翻 —— 读法见 "
            f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.2。"
        )
        lines.append("")
        if x1:
            lines.append(f"**§3.3a X1 臂未认领 {len(x1)} 组**")
            lines.append("")
            lines.append(f"<details><summary>展开 {len(x1)} 组（已有的多报侧裁定"
                         f"是另一轮判定者做的，你可以推翻）</summary>")
            lines.append("")
            lines.append("| 格数 | 裁定 | 子类 | 簇 | issue（组内各说法） |")
            lines.append("| --: | :-- | :-- | :-- | :-- |")
            for g in x1:
                adj = g.get("adjudicated") or {}
                texts = []
                seen = set()
                for m in g["members"]:
                    t = clip(m.get("issue"), 110)
                    if t not in seen:
                        seen.add(t)
                        texts.append(t)
                body = "<br>".join(texts[:3]) + ("<br>…" if len(texts) > 3 else "")
                lines.append(
                    f"| {g['cell_count']} | `{adj.get('verdict') or '—'}` | "
                    f"`{adj.get('subclass') or '—'}` | `{adj.get('cluster') or '—'}` | "
                    f"{body} |")
            lines.append("")
            lines.append("</details>")
            lines.append("")
        if v46:
            shown = v46[:30]
            lines.append(f"**§3.3b 主臂 v46 机械未匹配 {len(v46)} 组"
                         + (f"（列出出现格数最多的 {len(shown)} 组）"
                            if len(v46) > len(shown) else ""))
            lines.append("")
            lines.append(f"<details><summary>展开 {len(shown)} 组（主臂多报簇没有逐条"
                         f"回链到格，故这里标不出哪些已被裁定 —— 自行对照 §3.4）</summary>")
            lines.append("")
            lines.append("| 格数 | issue（组内各说法） | 需求 | rationale（截断） |")
            lines.append("| --: | :-- | :-- | :-- |")
            for g in shown:
                texts, seen = [], set()
                for m in g["members"]:
                    t = clip(m.get("issue"), 100)
                    if t not in seen:
                        seen.add(t)
                        texts.append(t)
                body = "<br>".join(texts[:3]) + ("<br>…" if len(texts) > 3 else "")
                rid = sorted({r for m in g["members"]
                              for r in (m.get("requirement_ids") or [])})
                lines.append(
                    f"| {g['cell_count']} | {body} | {clip(','.join(rid), 30)} | "
                    f"{clip(g['members'][0].get('reason'), 160)} |")
            lines.append("")
            lines.append("</details>")
            lines.append("")
        key = f"UM-{pair}"
        keys.append(key)
        # ⭐ §3 拉平后每个可裁决对象都要有自己的 `###` 抬头 —— ⛔ `UM-` 块此前只有小节标题，
        # ⚠️ 于是它在目录里找不到，而它恰恰是一律需要人裁的一族。
        lines.append(f"### {key}{DT.mark(key)} · 机械未匹配任何台账条目的多报簇（整表一块）")
        lines.append("")
        lines.append("上表里值得补入台账的，在这里点名（写行内的 issue 文本或格数+关键词即可）：")
        lines.append("")
        # ⚠️ 这一个填写块对应的是**整张表**，⛔ 不是一条线索 —— 与上面 `DIFF-` / `VU-`
        # 那种「一条 = 一个主张」不同构。所以它的映射多数标「没能映射」，
        # ⛔ 且卡点是**登记单位**而非座标系。不写明这一点，读者会把它读成覆盖度缺口。
        lines.append(
            f"注意这一块与上面的 `DIFF-` / `VU-` **不同构**：那些一条对应一个主张，"
            f"而 `{key}` 一块对应上面**整张表**（本 pair 共 {len(x1) + len(v46)} 组）。"
            "所以下面的映射多数是「没能映射」，卡点在**登记单位**（一格座标代表不了一整张表），"
            "**不是**座标系给不出取值 —— 逐组拆开后各组基本都能落格。"
        )
        lines.append("")
        lines.extend(_fmt_mapping(CM.for_candidate(key), CANDIDATE_MAPPING_CAVEAT))
        lines.extend(inspect_supplement(key))
        # ⭐ `UM-` 块也预填。⛔ 它无三方 D 判定（不在判读包内），故 `DT.prefill()` 走的是
        # 「只有人工 meta review」那条分支 —— ⚠️ 一律人工裁决，但推荐与理由照样给。
        lines.extend(DT.block(key))
        lines.append(fb.render(key, "candidate",
                               DT.prefill(key, "candidate") or fb.CANDIDATE_TEMPLATE,
                               saved.get(key)))
        lines.append("")

    # ---- §3.4 已裁定为非缺陷的多报簇
    other = S.other_unexpected(pair)
    lines.append("**§3.4 本 pair 已被判为「非缺陷」的多报簇（备查）**")
    lines.append("")
    if not other:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append(
            f"<details><summary>展开 {len(other)} 簇 —— 它们**不是**候选，"
            f"只用于在 §4 撞到同一形状时查既有裁定"
            f"（读法见 {S.WORKSHEET_HOWTO} §D.2）</summary>")
        lines.append("")
        lines.append("| 簇 | 臂 | 裁定 | 子类 | 事实 / 理由（截断） |")
        lines.append("| :-- | :-- | :-- | :-- | :-- |")
        for r in other:
            lines.append(
                f"| `{r.get('cluster')}` | {r.get('_arm')} | `{r.get('verdict')}` | "
                f"`{r.get('subclass') or '—'}` | "
                f"{clip((r.get('claim') or '') + ' ‖ ' + (r.get('fact') or ''), 200)} |")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    # ---- §3.5 同根但未归并
    la = S.ledger_accounted().get(pair) or []
    lines.append("**§3.5 与台账同根、但匹配器未归并的簇（「台账偏浅」的直接证据）**")
    lines.append("")
    if not la:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append(
            f"共 {len(la)} 簇 —— **同一个缺陷**换了谓词或措辞，台账那一条就没能覆盖，"
            f"故对应条目适合走「修正」而不是「保留」（见 "
            f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.2）。"
        )
        lines.append("")
        for r in la:
            lines.append(f"- **`{r.get('cluster')}`**（{r.get('_arm')}）：{esc(r.get('fact'))}")
            if r.get("note"):
                lines.append(f"  - {esc(r.get('note'))}")
        lines.append("")

    return "\n".join(lines), keys


# ------------------------------------------------------------------ §3.6 inspect 确定性发现

#: ⛔⛔ **这一族与 §3.1–§3.5 不是同一个物种，抬头不许省。** 前者出自 LLM 产出（两臂的 issue、
#: 审阅 agent 的 diff、多报簇），带采样噪声，同一个格重跑一次可能就没了；本节出自
#: `pyfcstm inspect --format json --enable-verify`，是**确定性检查**，同一份 `model.fcstm`
#: 永远给同一批诊断。⚠️ 这个差别直接改变「模型没提」这句话的含义：对前者是采样问题，
#: ⛔ 对后者说明的是**检查器本身看不到那类东西**。
INSPECT_SPECIES_CAVEAT = (
    "**这一节与 §3.1–§3.5 不是同一个物种。** 上面五节的线索全部出自 **LLM 产出**"
    "（两臂的 issue、审阅 agent 的 diff、多报簇），所以它们带采样噪声 —— 同一个格重跑一次"
    "可能就没有了。本节出自 `pyfcstm inspect --format json --enable-verify`，是**确定性检查**："
    "不采样、不过 LLM，同一份 `model.fcstm` 永远给同一批诊断。"
    "⚠️ 这个差别会改变你的读法：上面那些「模型没提到」是采样问题，"
    "本节的「检查器没报」说明的是**检查器本身看不到那类东西**。"
)

#: ⚠️ 确定性**不等于正确**。这一句同样不许省 —— 判读者若把「工具报的」当成「事实」，
#: 整节的裁决都会失真。
INSPECT_PROJECTION_CAVEAT = (
    "**但确定性不等于正确。** `model.fcstm` 是从作者源 PlantUML **投影**来的，"
    "投影会合成元素（root 复合态、缺初始时的占位态 `UnspecifiedInitial` 之类）。"
    "所以每条诊断都先过了一轮「内生 / 投影产物 / 不确定」分拣加一轮对抗性复核："
    "查明是投影产物的已经不在这里，本节只有**确认内生**与**分拣未能确定**两族。"
)

#: 整类排除的说明。⛔ 不写会让判读者以为这两类被漏掉了。
INSPECT_EXCLUDED_NOTE = (
    "**两个 code 整类不进本节主体**：`I_NONTRIVIAL_SCC`（内生率 **0/54**）与 "
    "`I_TOPOLOGICAL_NON_TERMINATING`（内生率 **0/52**）。"
    "理由不是嫌多，是它们对本语料不构成缺陷主张：反应式控制器本来就该有非平凡强连通分量、"
    "本来就不该终止。⚠️ 但落在「不确定」那一族里的仍然摆在下面 —— "
    "整类排除说的是「不当缺陷主张看」，不是「从材料里删掉」。"
)


def _flow(text):
    r"""把一段判定文字压成一行（段内不许硬折行，见 CLAUDE.md §2.2.1b）。

    ⛔ 与 `esc()` 不同：**不转义 `|`**，因为这些文字印在引用块与 bullet 里而不是表格单元格里。
    ⚠️ 转了反而会让「渲染结果与 audit json 逐字一致」这条对拍失效（`esc` 会把 `|` 变成 `\|`）。
    """
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _inspect_codes(rec):
    """一条 issue 底层诊断的 code 集合，按出现顺序去重。"""
    out = []
    for m in rec["members"]:
        key = m["code"]
        if key == "W_TOPOLOGICAL_NOEXIT":
            key += "@" + ((m.get("refs") or {}).get("counterexample_kind") or "?")
        if key not in out:
            out.append(key)
    return out


def _inspect_axes_lines(rec):
    """我方座标映射块。⛔ 抬头与 §2 / §3 用同一句 —— 这也是我方推断，判读者的裁决优先。"""
    out = [CANDIDATE_MAPPING_CAVEAT, ""]
    out += ["| 轴 | 我方判的取值 |", "| :-- | :-- |"]
    for axis in ("defect_locus", "defect_element", "defect_qualifier",
                 "defect_logic_kind", "defect_reference"):
        val = rec.get(axis)
        if not val:
            continue
        out.append(f"| `{axis}` | {T.bi(val, NF.ZH[axis].get(val))} |")
    out.append("")
    if (rec.get(NF.OTHER_NOTE_FIELD) or "").strip():
        out.append(f"- `other` 说明：{_flow(rec[NF.OTHER_NOTE_FIELD])}")
        out.append("")
    # ⭐ 座标被改判过的，把终局裁定的**完整**依据印出来 —— 判读者要判的正是「我们这一格判对了
    # 没有」，⛔ 只印结论不印依据他没法判。⛔ 也不许截断：这些依据里指着类型学的行号与逐字判定
    # 测试，⚠️ 截一半等于把「凭什么」删掉，所以整段放进折叠区而不是砍长度。
    for r in rec.get("rulings") or []:
        # ⚠️ 恢复来的条目**没有原判座标**（它整条都不曾进过判读材料），故换一句抬头 ——
        # ⛔ 印成「原判 — → 终局 X」会让人以为原判是空的，而事实是**根本没有原判**。
        if rec.get("recovered_from_refuted"):
            out.append(f"<details><summary>本条座标由**一份专门裁定**给出（`{rec['coord']}`；"
                       f"本条是从 refuted 恢复的，没有原判座标）—— 展开裁定依据与逐字引证</summary>")
        else:
            before = rec.get("coord_before_ruling") or "（原判原文见 `inspect_issues.json`）"
            out.append(f"<details><summary>本条座标**经过一轮改判**：原判 `{esc(before)}` → "
                       f"终局 `{rec['coord']}` —— 展开裁定依据与逐字引证</summary>")
        out.append("")
        out.append(f"- 判定依据（引类型学的判定测试与行号）：{_flow(r['ruling_basis'])}")
        out.append(f"- 逐字引证（回作者源 / NL / fcstm 核过）：{_flow(r['final_evidence'])}")
        out.append("")
        out.append("</details>")
        out.append("")
    return out


def _inspect_diag_details(rec):
    """底层诊断的折叠区。⭐ 归一化把 N 条诊断压成一条，⛔ 但原始诊断必须可查。"""
    out = [f"<details><summary>展开底层 {len(rec['members'])} 条 inspect 诊断"
           f"（工具原文 message 与结构化 refs）</summary>", ""]
    out += ["| diag | code | severity | 作者源行 | 工具原文 message |",
            "| --: | :-- | :-- | :-- | :-- |"]
    for m in rec["members"]:
        out.append(f"| {m['diag_index']} | `{m['code']}` | `{m['severity']}` | "
                   f"{clip(m.get('puml_line'), 40)} | {clip(m.get('message'), 150)} |")
    out.append("")
    for m in rec["members"]:
        out.append(f"- diag {m['diag_index']} 的 `refs`：{clip(json.dumps(m.get('refs') or {}, ensure_ascii=False), 400)}")
        if (m.get("synthesized_names") or "none") != "none":
            out.append(f"  - 涉及的投影合成名：{esc(m.get('synthesized_names'))}")
    out.append("")
    out.append("</details>")
    out.append("")
    return out


def _inspect_body(rec, with_deadlock_caveat=True):
    """一条 issue 的正文（不含填写块）。⛔ 并入既有条目时复用同一段，两处口径必须一致。"""
    out = []
    out.append("**归一化后的事实陈述**")
    out.append("")
    out.append("> " + _flow(rec["statement"]))
    out.append("")
    out.append(f"- 作者源逐字证据：{_flow(rec['puml_evidence'])}")
    out.append(f"- 归并理由（{len(rec['diag_indices'])} 条诊断 → 本条）：{_flow(rec['merge_reason'])}")
    if (rec.get("nl_evidence") or "").strip():
        out.append(f"- NL 侧依据：{_flow(rec['nl_evidence'])}")
    if rec.get("recovered_from_refuted"):
        out.append(f"- ⚠️ 本条是从「初判内生、被对抗复核推翻」里**恢复**的，恢复依据："
                   f"{_flow(rec['recovery_basis'])}")
    out.append("")
    if with_deadlock_caveat and any(m["code"] == "W_DEADLOCK_LEAF" for m in rec["members"]):
        out.append(f"- **`W_DEADLOCK_LEAF` 的语义归属须知**：{IF.DEADLOCK_LEAF_CAVEAT}")
        out.append("")
    out.extend(_inspect_diag_details(rec))
    return out


def _inspect_suspect_note(rec):
    """`suspect` 那一族的点名提示。⛔ 不许省 —— 它是「拿不准就新建块」这条口径的另一半。"""
    d = rec["overlap"]
    if d["overlap_kind"] != "suspect":
        return []
    return [f"- ⚠️ **疑似与 `{d['overlap_target']}` 重合，请你确认**：判重方拿不准，"
            f"按「拿不准就新建、不许判成重合」的口径单列在这里（错判重合会把一条真发现"
            f"藏进既有条目）。判重方的比对依据：{_flow(d['basis'])}",
            ""]


def _inspect_block(rec, saved):
    """一条 issue 的完整块（正文 + 点名提示 + 座标映射 + 填写块）。"""
    key = rec["issue_id"]
    codes = "、".join(f"`{c}`" for c in _inspect_codes(rec))
    out = [f"### {key}{DT.mark(key)} · {codes}", ""]
    out += _inspect_body(rec)
    out += _inspect_suspect_note(rec)
    out += _inspect_axes_lines(rec)
    out += DT.block(key)
    out.append(fb.render(key, "candidate",
                         DT.prefill(key, "candidate") or fb.CANDIDATE_TEMPLATE,
                         saved.get(key)))
    out.append("")
    return out


def inspect_supplement(target):
    """并入 `target`（台账 id 或候选键）的 inspect 补充证据。⛔ 不设裁决区。

    ⛔⛔ **被并入那条既有条目的 `statement` 与证据行一个字都不许改** —— 它们是**被判对象**。
    所以补充证据放在一个独立的折叠小节里，并逐字写明「来源是确定性检查」。
    ⚠️ 也**不给**它自己的填写块：判读者对同一个问题只裁决一次，裁决落在既有条目自己的块里；
    ⛔ 摆两个块会让同一个问题出现两份可能互相矛盾的裁决。
    """
    rows = IF.merged_into(target)
    if not rows:
        return []
    out = [f"<details><summary>{len(rows)} 条 `pyfcstm inspect` 的补充证据"
           f"（**确定性检查**，判重方判定与本条是同一个问题；⚠️ 上面的 statement 与证据行"
           f"未作任何改动，本节只是把工具侧的独立证据挂在这里）</summary>", ""]
    for rec in rows:
        codes = "、".join(f"`{c}`" for c in _inspect_codes(rec))
        out.append(f"**{rec['issue_id']}**{DT.mark(rec['issue_id'])} · {codes} · 分拣结论 "
                   f"`{rec['verdict_class']}` · 我方座标 `{rec['coord']}`")
        out.append("")
        # ⭐ 三方判读只给一行摘要。⛔ 不展开成完整区块：本条没有自己的裁决区，
        # ⚠️ 摆一整块「需你裁决」却没有可勾的地方，会让判读者以为漏了一个块。
        out.extend(DT.compact(rec["issue_id"]))
        out += _inspect_body(rec)
        out.append(f"- 判为同一个问题的依据：{_flow(rec['overlap']['basis'])}")
        # ⭐ 并入的这些也要留改判痕迹 —— ⛔ 只印终局座标而不说它被改过，
        # ⚠️ 事后看不出「我方这一格换过一次」。⛔ 但依据全文不在这里展开：
        # 本条的裁决落在宿主条目自己的块里，⭐ 详细依据在 inspect_rulings.json。
        for r in rec.get("rulings") or []:
            out.append(
                f"- 本条座标**经过一轮改判**：原判 `{esc(rec.get('coord_before_ruling') or '—')}` → "
                f"终局 `{rec['coord']}`（逐字依据与判定测试见 "
                f"[inspect_rulings.json](../inspect_rulings.json) 里 `{rec['issue_id']}` 那条）")
        out.append("")
    out.append("</details>")
    out.append("")
    return out


def section_inspect(pair, saved):
    """§3.6：`pyfcstm inspect` 的确定性检查发现。

    ⛔ 三件事必须同时成立，缺一条判读者就会误判整节：
      ① 让他一眼看出这是**确定性检查**而不是 LLM 产出（`INSPECT_SPECIES_CAVEAT`）；
      ② 把**归一化压缩比**摆出来 —— 他看到的一条 issue 背后有几条诊断（`0007` 是 35 → 7）；
      ③ `W_DEADLOCK_LEAF` 的**系统性假阳性**与两个 code 的**整类排除**都要写明。
    """
    lines, keys = [], []
    lines.append("**§3.6 `pyfcstm inspect` 的确定性检查发现**")
    lines.append("")
    if not IF.has_judged_issues():
        lines.append("**尚未入册。** 归一化与判重是判断、不是脚本能算的，"
                     "等判定者产出 `inspect_issues.json` / `inspect_overlap.json` / "
                     "`inspect_rulings.json` 之后本节才渲染。")
        lines.append("")
        return "\n".join(lines), keys

    rows = IF.issues_of(pair)
    diags, n_issues = IF.compression(pair)
    new_rows = IF.issues_of(pair, new_block_only=True)
    merged_rows = IF.issues_of(pair, merged_only=True)
    tot = IF.load_issues()["totals"]

    lines.append(INSPECT_SPECIES_CAVEAT)
    lines.append("")
    lines.append(INSPECT_PROJECTION_CAVEAT)
    lines.append("")
    lines.append(
        f"**本 pair：{diags} 条原始诊断归一化成 {n_issues} 条 issue**"
        f"（全语料 {tot['diagnostics_covered']} 条 → {tot['issues']} 条；压缩最狠的是 `0007`，"
        f"35 → 7）。⚠️ 你看到的一条 issue 背后往往是**好几条诊断**，"
        f"每条下面的折叠区里都能展开原始 message 与 `refs`。"
    )
    lines.append("")
    lines.append(INSPECT_EXCLUDED_NOTE)
    lines.append("")
    # ⛔ 假阳性说明**每份都印**，不只在命中该 code 的 pair 上印 —— 判读者在 §4 自己数出边时
    # 同样会踩这个坑（一个叶态自己没有出边，不等于它是终止态）。
    lines.append(f"**一个必须先知道的工具缺陷**：{IF.DEADLOCK_LEAF_CAVEAT}")
    lines.append("")
    if merged_rows:
        # ⛔ 去重：多条 issue 可以并进**同一条**既有条目（`EIS-0032-01` 就吃了三条），
        # ⚠️ 不去重会把同一个 id 在这句话里印两遍。
        targets = []
        for r in merged_rows:
            t = r["overlap"]["overlap_target"]
            if t not in targets:
                targets.append(t)
        lines.append(
            f"**本 pair 另有 {len(merged_rows)} 条判为与既有条目是同一个问题**，已并入对应条目"
            f"（{'、'.join('`' + t + '`' for t in targets)}）"
            f"作补充证据，**本节不再重复设裁决区** —— 同一个问题只裁一次。"
        )
        lines.append("")

    intrinsic = [r for r in new_rows if r["verdict_class"] == "intrinsic"]
    uncertain = [r for r in new_rows if r["verdict_class"] == "uncertain"]

    lines.append(f"**§3.6a 确认内生、且与既有条目不重合的 {len(intrinsic)} 条**")
    lines.append("")
    if not intrinsic:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append("这些的事实部分已回作者源逐字核过，且确认**不是投影产物**。"
                     "要你判的是：它算不算一条该进台账的缺陷。")
        lines.append("")
        for rec in intrinsic:
            keys.append(rec["issue_id"])
            lines.extend(_inspect_block(rec, saved))

    lines.append(f"**§3.6b 分拣未能确定是内生还是投影产物的 {len(uncertain)} 条**")
    lines.append("")
    if not uncertain:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append(
            f"⚠️ **这一族的事实成不成立本身还没定**：分拣未能确定它是作者制品的问题、"
            f"还是投影阶段造出来的。摆出来是因为**不许静默丢掉** —— 全语料 142 条不确定诊断"
            f"归一化成 {tot['uncertain']} 条，而它们恰好集中在那些没有确认内生发现的 pair 上，"
            f"正是最需要人判的地方。每条的正文默认折叠，展开后照常有裁决区。"
        )
        lines.append("")
        for rec in uncertain:
            keys.append(rec["issue_id"])
            codes = "、".join(f"`{c}`" for c in _inspect_codes(rec))
            lines.append(f"### {rec['issue_id']}{DT.mark(rec['issue_id'])} · {codes}")
            lines.append("")
            lines.append(f"<details><summary>展开这一条（分拣结论 `uncertain`，"
                         f"我方座标 `{rec['coord']}`）</summary>")
            lines.append("")
            lines.extend(_inspect_body(rec))
            lines.extend(_inspect_suspect_note(rec))
            lines.extend(_inspect_axes_lines(rec))
            lines.append("</details>")
            lines.append("")
            lines.extend(DT.block(rec["issue_id"]))
            lines.append(fb.render(rec["issue_id"], "candidate",
                                   DT.prefill(rec["issue_id"], "candidate")
                                   or fb.CANDIDATE_TEMPLATE,
                                   saved.get(rec["issue_id"])))
            lines.append("")

    return "\n".join(lines), keys


# ------------------------------------------------------------------ §4 清单

def section_checklist(pair, model, segs, records, saved):
    lines = []
    keys = []
    lines.append("## §4 深度检查清单（本节引导挖深）")
    lines.append("")
    lines.append(
        "每条都是**待核问句**，不是结论；勾 `[x]` = 已看过，「发现:」留空 = 看过但无发现。"
        "**时钟 / 计时 / 不变式 / 正交区并发不计入缺陷统计，但照常记** —— 读法与边界见 "
        f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.3。"
    )
    lines.append("")

    cats = checklist.build(model, segs, records, pair)
    if not cats:
        lines.append("机械分析没有产出任何线索 —— 该模型结构非常简单，"
                     "请直接对照 NL 逐段核。")
        lines.append("")
        return "\n".join(lines), keys

    for title, note, items in cats:
        slug = re.sub(r"[^A-Z]", "", items[0].iid.split("-")[0].upper()) or "X"
        key = f"CHK-{pair}-{slug}"
        keys.append(key)
        lines.append(f"### §4.{len(keys)} {title}")
        lines.append("")
        lines.append(note)
        lines.append("")
        body = []
        for it in items:
            body.append(f"[ ] {it.iid} {it.text}")
            if it.basis:
                body.append(f"    · {it.basis}")
            body.append("    发现:")
            body.append("")
        lines.append(fb.render(key, "checklist", "\n".join(body).rstrip(), saved.get(key)))
        lines.append("")
    return "\n".join(lines), keys


# ------------------------------------------------------------------ §5 新增登记

def _ex(slot, pair, field=None, limit=300):
    """渲染一条真实台账样例。⛔ 取不到就返回 None，⛔ 不编。"""
    rec = NF.exemplar(slot, pair)
    if rec is None:
        return None
    val = rec.get(field) if field else None
    return rec, (clip(val, limit) if val else None)


def _fill_enum_legend():
    """§5.2 登记块**紧邻处**的座标系图例：每个取值的英文名、中文名与判定测试。

    与 §2 的展示值走的是**相反**的口径，不要混：§2 是「已经填好、只需读懂」，
    故只内联该条自己那一个取值；这里是「要你选」，所以必须把选项**全部**列出 ——
    判读者看不到全集就没法选，而为了选一个类型去翻别的文件，他多半就不翻。

    条件式在这里是**分节**体现的：先一张 `defect_locus` 表，然后按分支各起一节。
    走 element 支的人只读 A + B 两张表，走逻辑支的人只读 D 一张表；
    没有人需要一次面对 28 个取值。

    勾选行里的取值必须保持英文原样，不许在方括号里加中文：
    [validate.py](./validate.py) 的 `_enum_check` 拿勾中的那串文本与
    `newfields.ENUMS` **逐字**比对，写成 `[x] state（状态）` 会被判成非法取值。
    所以英中双写落在下面这几张表里，不落在方括号里。

    ⚠️ 本节只渲染进**工作单**（在 `nl_XXXX/` 下，比共用页深一层），故文内链接一律按
    工作单的深度写：到 `discover_matrix/` 是三层 `../../../`。
    """
    lines = []
    lines.append(
        "每个取值的判定测试都写在下面表里，填表不必再翻别的文件。取值与判定测试出自 "
        + "[defect_taxonomy.md](../../../docs/protocol/defect_taxonomy.md)"
        + "，每一条在那份文档里都挂着一条可查证的外部依据。"
        "**勾选行里的取值请保持英文原样**：校验器逐字比对，在方括号里加中文会被判成非法取值。"
    )
    lines.append("")

    lines.append("#### 先答这一项：`defect_locus` 定位范围（4 选 1，必填）")
    lines.append("")
    lines.append("判定测试：**要把这条缺陷说清楚，你最少得指出制品里的几处？**")
    lines.append("")
    lines.append("| 取值 | 中文 | 判定测试 | 接着填什么 |")
    lines.append("| :-- | :-- | :-- | :-- |")
    nxt = {"element": "A + B（下一节）", "pair": "D（再下一节）",
           "global": "D（再下一节）", "other": "D（再下一节）"}
    for v, zh, test in NF.LOCI:
        lines.append(f"| `{v}` | {zh} | {esc(test)} | {nxt[v]} |")
    lines.append("")
    lines.append(
        "两处最容易混：`element` 与 `pair` 的分界是**单看你点到的那一处，它自己有毛病吗** —— "
        "有就是 `element`，每一处单看都合法、毛病在它们凑一起就是 `pair`；"
        "`pair` 与 `global` 的分界是**涉及的处所能不能列举出来** —— "
        "能列举（这两条边、这条边和那个复合态）是 `pair`，只能说「从初始态出发走不到」"
        "「存在一条执行」是 `global`。"
    )
    lines.append("")
    lines.append(
        "座标系里**没有** `cross`（跨制品）这一档，这是有意的：「NL 要求恒真的性质、"
        "模型允许其反例」在模型内的定位就是 `global`（一条违反的执行路径），"
        "它的跨制品性由 `defect_reference = requirement` 承载。合成一档会让"
        "「NL 点名的某个状态缺失」这种既跨制品又单元素的缺陷无处可去。"
    )
    lines.append("")

    lines.append(f"#### 走 element 支：`defect_element` 构件（{len(NF.ELEMENTS)} 选 1）"
                 f"+ `defect_qualifier` 限定词（{len(NF.QUALIFIERS)} 选 1）")
    lines.append("")
    lines.append("`defect_element` 判定测试：指着作者源那一行问 ——")
    lines.append("")
    lines.append("| 取值 | 中文 | 判定测试 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, test in NF.ELEMENTS:
        lines.append(f"| `{v}` | {zh} | {esc(test)} |")
    lines.append("")
    lines.append(
        "分界提示：一条边接到了**错的目标态**落 `transition` + `incorrect`，不落 `state`；"
        "「Y 应当是 X 的子态而不是兄弟」落 `state` + `incorrect`（父容器是状态的一个属性）；"
        "缺的是**整个条件表达式**落 `guard`，条件在、但它引用的量没有声明落 `variable`。"
    )
    lines.append("")
    lines.append(
        "⚠️ **`region` 这一档与其余七个不是同一种东西**：正交区并发语义在 "
        "$M = (S, E, V, Tr, A)$ **之外**，所以它 `counts_as_defect = false` —— "
        "**照常记，但不计入任何缺陷统计**。给它一个槽位是为了同时满足两条要求："
        "既不把这类发现记成「方法没检出」，也不反过来声称这些模型没有并发问题。"
        "时钟 / 计时 / 不变式**没有**对应取值（PlantUML 状态图里没有它们的语法载体），"
        "撞上了就照常写进 `statement` 自由文本，回收后由主 session 人工分拣。"
    )
    lines.append("")
    lines.append(f"`defect_qualifier` 判定测试（统一一句）：{NF.QUALIFIER_TEST}")
    lines.append("")
    lines.append("| 取值 | 中文 | 改完之后的条数 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, test in NF.QUALIFIERS:
        lines.append(f"| `{v}` | {zh} | {esc(test)} |")
    lines.append("")
    lines.append(
        "「事件名拼错 / 用了别的写法」落 `incorrect`（改一个属性值，条数不变），"
        "不要记成 `missing` + `extraneous`。"
        "⚠️ 反过来，很多「一次编辑改不完」的情形**根本不是** `element` —— "
        "先回上一节重判 `defect_locus`，把逻辑层缺陷塞进 `element` + `other` "
        "是本座标系最需要防的一种误填。"
    )
    lines.append("")

    lines.append(f"#### 走逻辑支（`pair` / `global` / `other`）："
                 f"`defect_logic_kind` 逻辑类型（{len(NF.LOGIC_KINDS)} 选 1）")
    lines.append("")
    lines.append(
        "这一轴承担 A×B 结构上表达不了的那一半：非确定性、不完备、可达性、终止性、"
        "层次语义交互 —— 它们单看任何一个元素都完全合法。"
        "判定测试可手算，除非另注。"
    )
    lines.append("")
    lines.append("| 取值 | 中文 | 判定测试 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, test in NF.LOGIC_KINDS:
        lines.append(f"| `{v}` | {zh} | {esc(test)} |")
    lines.append("")
    lines.append(
        "分界提示：`nondeterminism` 与 `incompleteness` 是同一组守卫的**两个相反方向**"
        "（有赋值让两条同时真 / 有赋值让全部假），一组守卫可以同时犯这两个错，那就拆成两条；"
        "进不去是 `unreachable`、进得去出不来是 `unintended_terminal`、"
        "一直在动却到不了终点是 `nontermination`；"
        "两条使能出边在**同一个状态**上是 `nondeterminism`，分处**内层与外层**、"
        "靠层次优先级消解是 `priority_conflict`。"
    )
    lines.append("")
    lines.append(
        "⚠️ **非确定性与不完备性不是并发问题** —— 它们在 $M = (S, E, V, Tr, A)$ **界内**，"
        "是这一轴的正当取值，不要按「无正交区」的边界规则把它们排除掉。"
    )
    lines.append("")

    lines.append("#### 两支都要填：`defect_reference` 参照物（3 选 1）")
    lines.append("")
    lines.append("判定测试：**判定这条缺陷成立，你需不需要引用 NL 的某一句？**")
    lines.append("")
    lines.append("| 取值 | 中文 | 判定测试 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, test in NF.REFERENCES:
        lines.append(f"| `{v}` | {zh} | {esc(test)} |")
    lines.append("")
    lines.append(
        "⚠️ 两处已知陷阱：「多条出边守卫不互斥」**不能**判 `language` —— "
        "UML 2.5.1 明写允许迁移冲突且优先级只给出偏序；"
        "「复合态缺默认入口」同样**不能**判 `language` —— UML 把它留作语义变异点。"
        "这两条要判成缺陷，必须走 `requirement` 并给出 NL 逐字依据。"
    )
    lines.append("")

    lines.append(f"#### 任一轴勾了 `other`：`{NF.OTHER_NOTE_FIELD}` 必填")
    lines.append("")
    lines.append(
        f"上面五个轴里**任意一个**勾了 `other`，就必须在 `{NF.OTHER_NOTE_FIELD}` 里写一句话。"
        "写清两件事之一即可：**它到底是什么**，或者**这一条涉及多个取值、一格装不下**"
        "（是哪几个）。两种都是合法答案，但必须说出是哪一种。"
    )
    lines.append("")
    lines.append(
        "留空会被 [validate.py](../validate.py) 报 `E`。"
        "这道门只看「有没有 `other`」与「说明空不空」两件事，**不判你这句写得对不对** —— "
        "后者要读文意，做成门会把正确答案挡在外面。"
    )
    lines.append("")
    lines.append(
        "为什么值得单立一条：`other` 是出口，出口不写清等于没分类。事后回看只剩一个 "
        "`other`，既不知道它是什么，也分不出它是「真的都不是」还是「涉及多个」—— "
        "而这两种情形对「座标系还缺什么」这个问题给出的答案完全不同。"
    )
    lines.append("")

    lines.append("#### 已知表达缺口（撞上它不是你选错了）")
    lines.append("")
    lines.append("| 缺口 | 落哪 | 为什么没有取值 |")
    lines.append("| :-- | :-- | :-- |")
    for gap, where, why in NF.KNOWN_GAPS:
        lines.append(f"| {gap} | {where} | {esc(why)} |")
    lines.append("")
    return lines


def _expected_after_fix_legend():
    """§5.2 里 `expected_after_fix` 的句式骨架（Dwyer pattern × scope）。

    刻意**不**做成必填枚举：40 个组合、且要先把 NL 句子形式化，
    这不是「不查手册就能选对」的负担。但它填得起来时同时给出缺陷描述与验收判据，
    正是三件事里「修好算什么」那一项的现成语言，所以以**模板**形态给出。
    """
    lines = []
    lines.append(
        "写成一句**可判定的期望结果**：读的人拿着它能回到模型上判成立与否。"
        "例如「从 `HumanDrivingMode` 施加 `Power Off` 后应当到达终态」，"
        "而不是「应该修好」「补上这条边」。"
    )
    lines.append("")
    lines.append(
        "下面是可选的句式骨架，套用与否随你 —— 直接写自然语言同样合法。"
        "把这条义务改写成一句「**在〈作用域〉内，〈模式〉〈对象〉**」；改写不出来就别套。"
    )
    lines.append("")
    lines.append("| 模式 | 中文 | 句式 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, shape in NF.PROPERTY_PATTERNS:
        lines.append(f"| `{v}` | {zh} | {shape} |")
    lines.append("")
    lines.append("| 作用域 | 中文 | 指哪一段执行 |")
    lines.append("| :-- | :-- | :-- |")
    for v, zh, what in NF.PROPERTY_SCOPES:
        lines.append(f"| `{v}` | {zh} | {what} |")
    lines.append("")
    lines.append("套用时一并带上两条口径：" + "".join(NF.PROPERTY_CAVEATS))
    lines.append("")
    lines.append(
        "套用了就把那对组合记进可留空的 `property_pattern`（例如 `Response × After`），"
        "没套用就留空 —— 留空不扣分。"
    )
    lines.append("")
    return lines


def section_new(pair, saved):
    """§5 新增登记。**只留**「本 pair 独有的东西 + 要填的块」。

    登记一条只回答三件事：① 它是哪一类错（条件式座标系，勾选）、
    ② 错在哪错成什么样（`statement`）、③ 修好之后怎样才算 ok（`expected_after_fix`）。

    座标系为什么这么设、每一档的文献出处、旧字段表为什么撤掉 —— 这些**逐字节相同**的
    长说明在 [HOWTO.md](../HOWTO.md) 与
    [defect_taxonomy.md](../../../docs/protocol/defect_taxonomy.md)，
    不在 54 份工作单里各印一遍。留在这里的是：两道登记门、真实台账样例
    （按 NL 组回避，故 9 组各不相同，不能上移到共用页）、逐取值的判定测试、以及登记区本身。
    """
    lines = []
    lines.append("## §5 新增 issue 登记")
    lines.append("")
    lines.append(
        "把 §3 采纳的、§4 查出的、以及你自行发现的缺陷登记在这里。"
        "登记区默认给两条，不够就照格式往下加（`NEW-" + pair + "-03`、`-04` …，编号连续即可）。"
    )
    lines.append("")
    lines.append(
        "**一条登记只回答三件事**："
        "**① 它是哪一类错** —— 一套条件式座标系，全是勾选："
        "先答 `defect_locus`（定位范围，4 选 1），它决定后面问哪些轴 —— "
        "选 `element` 就答 `defect_element` + `defect_qualifier`，"
        "选 `pair` / `global` / `other` 就答 `defect_logic_kind`；"
        "两支都要答 `defect_reference`（参照物，3 选 1）。"
        "**② 错在哪、错成什么样** —— `statement`，自由文本，写清是哪一处、运行时会怎样。"
        "**③ 修好之后怎样才算 ok** —— `expected_after_fix`，自由文本，"
        "写成一句能回到模型上判成立与否的期望结果。"
    )
    lines.append("")
    lines.append(
        "所以你实际面对的不是 28 个取值，而是**一次 4 选 1 加两三次不超过 9 选 1**，"
        "每一步都有一句判定测试（就在下面 §5.2 的表里），加上两段自由文本。"
        "边界（时钟 / 不变式 / 并发）**不再由你分类**：你只判「这是不是缺陷」，"
        "撞上界外的东西照常写进 `statement`，回收后由主 session 统一分拣。"
    )
    lines.append("")
    lines.append("登记前先过两道门：")
    lines.append("")
    lines.append(
        "1. 它在**作者源**上成立吗？只在 `plantuml_source_lowering.py` 的投影上成立的不算 —— "
        "判据是能不能回答「这条主张在 §1.2 的作者源上怎么表述」。"
    )
    lines.append(
        "2. 它和 §2 已有条目是同一个缺陷吗？是则回 §2 对那一条走「修正」，"
        "不要在这里新开一条。"
    )
    lines.append("")

    # ------------------------------------------------------ §5.1 真实台账样例
    # 这一节**不能**上移到共用的 HOWTO.md：`NF.exemplar()` 按 `S.nl_group(pair)`
    # 回避同组条目，所以 9 个 NL 组看到的样例各不相同。共用一份等于把兄弟 pair
    # 的缺陷当格式样例摆在读者眼前 —— 那正是本轮要判读者自己做的判断。
    lines.append("### §5.1 真实台账样例（已按 NL 组回避）")
    lines.append("")
    lines.append(
        "以下样例全部取自现有台账 "
        "[expected_issue_set.json](../../expected_issue_set.json) 的**真实条目**，"
        "一条都没有编。且已避开本 pair 所属的 NL 组（本目录 `"
        + S.nl_dir(pair) + "`，上游 `<pair>-review.json` 里记作 `"
        + str(S.nl_group(pair)) + "` —— 两个名字指同一组，"
        "上游那套编号不是本目录的排序）—— 同一份 NL 生成 6 个制品，"
        "拿兄弟 pair 的缺陷当格式样例等于把答案先告诉你。"
    )
    lines.append("")
    lines.append(
        "⚠️ 样例给的是**写作密度**，不是**归类答案**：台账用的是另一套字段"
        "（`layer` / `direction` 那套，见 §2），本轮的座标轴该怎么勾要你自己判。"
    )
    lines.append("")
    lines.append("| 字段 | 真实样例（台账条目 id） |")
    lines.append("| :-- | :-- |")
    for slot, field, limit in (("statement", "statement", 320),
                               ("nl_evidence", "nl_evidence", 200)):
        got = _ex(slot, pair, field, limit)
        if not got:
            continue
        rec, val = got
        lines.append(f"| `{slot}` | `{rec['id']}`：{val} |")
    got = _ex("nl_evidence_empty", pair, None)
    if got:
        rec, _ = got
        lines.append(f"| `nl_evidence` 写 `无` | `{rec['id']}`：{clip(rec['statement'], 160)} |")
    lines.append("")
    lines.append(
        f"`nl_evidence` 要写的是本页 §1.1 那套段 id（本 pair 的第一段是 "
        f"`{segs_hint(pair)}`），多个用逗号分隔，后面可以再跟一句逐字引文。"
        "⚠️ **留空与写 `无` 不是一回事**：写 `无` 表示「NL 未明说，本条不靠 NL 判定」，"
        f"那是有意义的答案（台账 {'{} / {}'.format(*NF.nl_evidence_empty_count())} "
        "条正是这种情况）；而留空会被校验判成没填。"
    )
    lines.append("")

    # ---------------------------------------------------------- §5.2 登记区
    lines.append("### §5.2 登记区")
    lines.append("")
    lines.append(
        "直接在下面的块里填。只有 `FILL:BEGIN` / `FILL:END` 之间的内容会被 "
        "[collect.py](../collect.py) 收走，块外写的东西重跑生成器就没了。"
        "模板里 `--- … ---` 那几行是分支提示，不是字段，回收时会被剔除。"
    )
    lines.append("")
    lines += _fill_enum_legend()
    lines.append("#### `statement` 与 `expected_after_fix` 怎么写")
    lines.append("")
    lines.append(
        "`statement` 写**错在哪、错成什么样、因此运行时会怎样**。判据：读完这一句，"
        "另一个人能不能独立回到 §1.2 的作者源上复核它成立与否 —— "
        "所以请把位置写进去（写行号如 `:12` 最省事，再附那一行的原文片段）。"
        "缺失类缺陷写「（无此边）」这类否定描述也算合法。"
    )
    lines.append("")
    lines += _expected_after_fix_legend()
    key = f"NEW-{pair}"
    lines.append(fb.render(key, "new", fb.new_template(pair), saved.get(key)))
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ 共用填写说明

def build_howto():
    """渲染 `HOWTO.md` —— ⭐ 54 份工作单共用的填写说明。

    ⛔ 这里只放**与 pair 无关**的内容。判据很硬：函数签名里没有 `pair`，
    ⛔ 所以任何依赖具体 pair / NL 组的东西（真实样例、段 id、结构摘要）都进不来 ——
    ⚠️ 那正是要的：一份共用页若掺进某一份制品的事实，就会对另外 53 份为假，
    ⛔ 而这正是 [README.md](./README.md) §十那起事故的形状。
    """
    lines = []
    lines.append(f"<!-- RELABEL schema={HOWTO_SCHEMA} -->")
    lines.append("# 工作单填写说明（54 份共用）")
    lines.append("")
    lines.append(
        "本文件由 [generate.py](./generate.py) 生成，**没有任何填写区** —— 它是只读说明。"
        "要填的东西全在 `nl_XXXX/<pair>.md` 的 `FILL` 块里。"
        "本页只放**与具体 pair 无关**的口径：凡是依赖某一份制品的事实，"
        "都留在各自的工作单里。"
    )
    lines.append("")
    lines.append("| 节 | 内容 | 工作单里从哪里跳过来 |")
    lines.append("| :-- | :-- | :-- |")
    lines.append("| §A | 两处只读材料的口径提醒 | §1.2 · §1.3 |")
    lines.append("| §B | §5 登记的三件事与逐字段怎么填 | §5 开头 · §5.1 |")
    lines.append("| §C | 座标系为什么长这样（背景，填表时可跳过） | §5.2 登记区 |")
    lines.append("| §D | §2 / §3 / §4 三节的通用读法 | §2 · §3 · §4 开头 |")
    lines.append("")

    # ============================================================ §A 材料口径
    lines.append("## §A 只读材料的口径提醒")
    lines.append("")
    # ⚠️ 本节 2026-08-13 改锚：原文写的是「工作单 §1.2 结构摘要的数字来自作者源」，
    # ⛔ 而结构摘要那一节已整节删除。⭐ 但双口径本身**没有失效** —— 判读者写 `cardinality`
    # 类主张时照样会数错，故本节改成锚在 §1.2 作者源本身，⛔ 不是跟着摘要一起删。
    lines.append("### §A.1 ⚠️ 作者源与谓词层是两套计数口径，不能混用")
    lines.append("")
    lines.append(
        "各份工作单 §1.2 给的是**作者源 PlantUML 原文**，其中不含 "
        "`plantuml_source_lowering.py` 投影合成的 "
        "`UnspecifiedInitial` / `InvalidInitial*` / `FinalWait*` / `R45RouteToken`。"
        "谓词层的 `cardinality` 会把它们算进去，所以「作者写了 3 个子态」在谓词层可能是 4 或 7 —— "
        "两个口径都对，但**不能混用**。你数元素个数时数的是作者源那一套。"
    )
    lines.append("")
    lines.append("### §A.2 参考模型不是正确答案")
    lines.append("")
    lines.append(
        "⚠️ 各份工作单 §1.3 给的参考模型来自作者 workbook 的 `STM Results!D` 列。"
        "它**不是**正确答案 —— 语料里多处出现参考侧比生成侧更差的情形"
        "（例如 `0000` 的参考模型压根没声明 `autonomous_mode` 的状态体）。"
        "它只是「另一个人怎么建的」，用作对照，不作为判据。"
    )
    lines.append("")

    # ============================================================ §B 三件事
    lines.append("## §B §5 新增登记：三件事与逐字段怎么填")
    lines.append("")
    lines.append("### §B.1 一条登记回答三件事")
    lines.append("")
    lines.append("| 项 | 字段 | 形态 |")
    lines.append("| :-- | :-- | :-- |")
    lines.append("| ① 它是哪一类错 | `defect_locus` + 分支轴 + `defect_reference` | 可枚举，勾选 |")
    lines.append("| ② 错在哪、错成什么样 | `statement` | 自由文本 |")
    lines.append("| ③ 修好之后怎样才算 ok | `expected_after_fix` | 自由文本 |")
    lines.append("")
    lines.append(
        "① 是一套**条件式座标系**：先答 `defect_locus`（定位范围），它决定后面问哪些轴。"
        "五个轴的**全部取值与判定测试**内联在每份工作单的 §5.2 登记块紧邻处，"
        "填表不必翻本页；本节只给必填口径与两段自由文本怎么写。"
    )
    lines.append("")
    lines.append("| 字段 | 何时必填 | 一句话 | 留空的含义 |")
    lines.append("| :-- | :-- | :-- | :-- |")
    lines.append("| `defect_locus` | 总是 | ① 定位范围，4 选 1 | 不许留空 |")
    lines.append("| `defect_element` | 仅 `defect_locus = element` | ① 落在哪类构件上，7 选 1 | "
                 "走逻辑支时**就该**留空 |")
    lines.append("| `defect_qualifier` | 仅 `defect_locus = element` | ① 改对它要做哪种编辑，4 选 1 | "
                 "走逻辑支时**就该**留空 |")
    lines.append("| `defect_logic_kind` | 仅 `defect_locus ≠ element` | ① 哪一种逻辑层缺陷，9 选 1 | "
                 "走 element 支时**就该**留空 |")
    lines.append("| `defect_reference` | 总是 | ① 凭什么说它错，3 选 1 | 不许留空 |")
    lines.append("| `statement` | 总是 | ② 错在哪、错成什么样、运行时会怎样 | 不许留空 |")
    lines.append("| `expected_after_fix` | 总是 | ③ 修好之后怎样才算 ok | 不许留空 |")
    lines.append("| `nl_evidence` | 总是 | NL 段 id；NL 未明说就写 `无` | "
                 "不许留空（写 `无` 才算判过） |")
    lines.append("| `property_pattern` | 可选 | ③ 若套了 Dwyer 句式，记下那对组合 | "
                 "留空 = 没套用，不扣分 |")
    lines.append("| 脚本推导 | | `id` `pair` `group` `llm` `element_of_M` `upstream` | "
                 "由 [newfields.py](./newfields.py) 的 `derive()` 算出，**一律不填** |")
    lines.append("| 合并时补 | | `assertions` `replay` `verdict` `layer` `homogeneity_*` "
                 "`decided_by` `in_scope` | 要跑断言器 / 要全库重算 / 要主裁定，**一律不填** |")
    lines.append("")
    lines.append(
        "所以每条实际要动的是**一次 4 选 1 加两三次不超过 9 选 1**，加两段自由文本，"
        "外加一个段 id。走 element 支时候选面是 4+7+4+3 = 18，走逻辑支时是 4+9+3 = 16 —— "
        "**没有人需要一次面对 28 个取值**。"
    )
    lines.append("")
    lines.append(
        "填了**另一支**的轴不报错，只报 `W` 提醒你多半是选完 `defect_locus` 忘了删；"
        "该支必填的轴缺了则报 `E`。这两条是 [validate.py](./validate.py) 在座标系上做的"
        "**全部**判断，加上「取值在不在枚举内」—— 其余一律不由校验器管，"
        "因为其余都要读文意（[CLAUDE.md](../../../../../CLAUDE.md) §11：只有能被完美判定的"
        "约束才允许做成会一票否决的门）。"
    )
    lines.append("")

    lines.append("### §B.2 ② `statement`：错在哪、错成什么样")
    lines.append("")
    lines.append(
        "写**你看到了什么、因此运行时会怎样**，不是写「哪里不一样」。判据：读完这一句，"
        "另一个人能不能独立回到作者源上复核它成立与否。所以位置要写进去 —— "
        "优先写工作单 §1.2 的行号（`:12` 或「第 12 行」），再附那一行的元素名或原文片段。"
        "缺失类缺陷写「（无此边）」这类否定描述也算合法，台账里就有。"
    )
    lines.append("")
    lines.append(
        "撞上**界外**的东西（时钟 / 不变式 / 正交区并发）也写在这里，照常登记。"
        "本轮**不再要求你判它在不在 $M = (S, E, V, Tr, A)$ 内** —— "
        "你只判「这是不是缺陷」，分拣由主 session 回收后统一做。"
        "理由见 [README.md](./README.md) §二.1。"
    )
    lines.append("")
    lines.append(
        "⚠️ **写成一段，不要换行**。回收器只把 `" + "` / `".join(NF.FIELD_NAMES)
        + "` 这几个名字当作新字段起点，其余行都会并进当前字段 —— "
        "所以你可以在 `statement` 里放冒号、放引文，但请别自己起一个像字段名的行。"
    )
    lines.append("")

    lines.append("### §B.3 ③ `expected_after_fix`：修好之后怎样才算 ok")
    lines.append("")
    lines.append(
        "写成一句**可判定的期望结果**：读的人拿着它能回到模型上判成立与否。"
        "「从 `HumanDrivingMode` 施加 `Power Off` 后应当到达终态」是合格的；"
        "「应该修好」「补上这条边」不合格 —— 前者不可判定，后者只说了改法、没说改对的标准。"
    )
    lines.append("")
    lines.append(
        "工作单 §5.2 给了 Dwyer 的 pattern × scope 句式骨架（`Absence` / `Existence` / "
        "`Universality` / `Precedence` / `Response` … × `Globally` / `Before` / `After` / "
        "`Between` / `After-Until`）。**它是模板不是分类**：套得上就套、套上了把组合记进 "
        "`property_pattern`，套不上直接写自然语言，留空不扣分。"
    )
    lines.append("")

    lines.append("### §B.4 `nl_evidence`")
    lines.append("")
    empty_n, total_n = NF.nl_evidence_empty_count()
    lines.append(
        "写本 pair 工作单 §1.1 那套**段 id**（同组 6 份共用一套编号，"
        f"见各组的 `nl_XXXX/{S.NL_DOC}`），多个用逗号分隔，后面可以再跟一句逐字引文。"
    )
    lines.append("")
    lines.append(
        "⚠️ **写 `无` 是有意义的答案，不是偷懒** —— 它表示「NL 未明说，本条不靠 NL 判定」，"
        f"与 `defect_reference = language` 相配。现台账 **{empty_n} / {total_n}** "
        "条正是这种情况。但**留空**不等于 `无`：留空会被校验判成没填。"
    )
    lines.append("")
    lines.append(
        "`defect_reference = requirement` 而 `nl_evidence` 写 `无` 会报一条 `W`："
        "那一档的判定测试就是「必须引用 NL 的某一句才能判定」，两者多半有一个要改。"
        "只报提醒不报错 —— 「这一条到底靠不靠某句 NL」要读文意。"
    )
    lines.append("")

    # ============================================================ §C 背景
    lines.append("## §C 座标系为什么长这样（背景，填表时可跳过）")
    lines.append("")
    lines.append("### §C.1 取值为什么必须来自外部文献")
    lines.append("")
    lines.append(
        "本轮重标要回答的是：**现有缺陷台账是不是偏浅，有没有漏掉我们框架表达不了的缺陷。**"
        "如果类型学的取值是从我们自己的 19 条谓词、四层 `layer` 或台账已有条目归纳出来的，"
        "那么判读者能选出来的类型，按构造就等于框架已经能说的东西 —— "
        "**问题本身被答案定义掉了**。"
    )
    lines.append("")
    lines.append(
        "这不是假想风险。上一版工作单的 `direction` 字段明写取值就是「台账 98 条 "
        "`REPORTABLE` 实际用过的 8 类」—— 用它复核台账内部一致性没问题，"
        "用它发现台账的盲区则不可能：**没被用过的类不在选项里**。"
        "本轮的五个轴每一个取值都挂着一条可查证的外部依据"
        "（Chow 的 FSM 故障模型 · Lackner & Schmidt 的变异算子 · ODC 的 Qualifier · "
        "Heimdahl & Leveson 的不确定性 / 不完备判据 · Baier & Katoen 的可达与终止定义 · "
        "UML 2.5.1 的层次与优先级条款 · Dwyer 的性质模式），"
        "逐条出处见 [defect_taxonomy.md](../../docs/protocol/defect_taxonomy.md)。"
    )
    lines.append("")
    lines.append(
        "⚠️ 旧 `direction` 与新的 `defect_element` / `defect_logic_kind` 语义有重叠但取值不同，"
        "本轮**直接删除、不做映射**：旧值是自家词表，新值有文献出处，混用会污染出处链。"
        "台账既有条目在数据里仍然带着它们自己的 `layer` / `direction`，"
        "但 §2 **不再把它们印出来**（理由见 §D.1）—— 那是**台账的**字段，"
        "不是这一轮要你填的，也不该成为你归类时的锚。"
    )
    lines.append("")
    lines.append("### §C.2 为什么是条件式，而不是几个平行维度")
    lines.append("")
    lines.append(
        "`defect_element`（构件）与 `defect_qualifier`（限定词）的**定义域就是单元素** —— "
        "它们出自变异算子与 Chow 故障模型，而那两支来自测试领域，"
        "「缺陷」在那里按定义就是**一次语法编辑**。"
        "一个非确定性缺陷没有「哪个元素错了」这回事：两条出边单看都合法，缺陷在**这一对**上；"
        "它也既不 missing、又不 incorrect、又不 extraneous。"
        "逼判读者为它选一个构件和一个限定词，产出的不是数据，是噪声。"
    )
    lines.append("")
    lines.append(
        "所以改成先答定位范围、再按分支问轴。这不是新发明的组织方式：ODC 自己就这么组织，"
        "它的 `Qualifier` 属性明写 \"applies to\" 另一个属性。"
    )
    lines.append("")
    lines.append("### §C.3 被撤掉的旧字段")
    lines.append("")
    lines.append("| 撤掉的 | 为什么 |")
    lines.append("| :-- | :-- |")
    lines.append("| `direction` | 取值来自台账自己用过的 8 类 —— 见 §C.1 |")
    lines.append("| `depth`（表层 / 中层 / 深层） | 本目录自造的三分，台账没有这个字段；"
                 "判据「读懂它需要看几个地方」要人做语义判断，却被摆成必填勾选行 |")
    lines.append("| `layer`（台账四层） | 与新座标系不同构，且它同时被当成「缺陷种类」与"
                 "「依据来源」两个轴在用；并表时由裁定套写，不由判读者勾 |")
    lines.append("| `basis`（四种依据来源） | 与 `defect_reference` 重合。"
                 "后者有文献出处（模型质量的 syntactic / semantic 两层），前者没有 |")
    lines.append("| `scope`（界内 / 越界三档） | 边界分拣改为回收后由主 session 做 —— "
                 "判读者判「这是不是缺陷」，不判「它属于我们框架的哪一格」 |")
    lines.append("| `primary_predicate` | 19 谓词是我们自己的词表，让判读者按它归类"
                 "会把「框架说不出的东西」挤出选项 |")
    lines.append("| `generated_side` | 与 `statement` 重复。位置直接写进 `statement` |")
    lines.append("| `reference_side` | 参考模型不是正确答案（§A.2），单列一栏会诱导对照它判缺陷 |")
    lines.append("")

    # ============================================================ §D 三节读法
    # ============================================================ §D 三节读法
    lines.append("## §D §2 / §3 / §4 的通用读法")
    lines.append("")
    lines.append("### §D.1 §2 现有 expected issue 逐条裁决")
    lines.append("")
    lines.append(
        "每条只印四样：`statement` 原文、参考侧 / 生成侧证据行、我方到新座标系的映射、"
        "以及自动风险标记。裁决区留空由你填；自动风险标记只是**提示**，"
        "打了标记不等于该条不成立，没打标记也不等于它成立。"
    )
    lines.append("")
    lines.append(
        "**为什么台账那一条自己的元数据不印给你看。** §2 此前还印着这一条的 "
        "`layer`（四层归因）、`direction`（八方向）、`element_of_M`（$M$ 分量）、"
        "`decided_by`（分层判定来源）、`primary_predicate`（主谓词）、`nl_evidence`、"
        "`verdict`、`replay`、同质组与上游，外加整节断言组。2026-08-13 全部撤掉，"
        "理由不是嫌长：本轮要你回答的是**我们这套框架有没有漏掉东西**，"
        "而那十项里有七项正是框架给这一条贴的标签。先把框架的答案印在题面上，"
        "你就只会在既有格子之间挑一个 —— 问题被答案定义掉了。`verdict` 与 `replay` "
        "更直接：那是流水线的判定与复算结论，印出来等于先给标准答案。"
    )
    lines.append("")
    lines.append(
        "同样的理由，读那些已隐藏字段的风险标记也一并撤了"
        "（`lexical` / `no_primary` / `no_assertion` / `no_nl_evidence` / `replay`）。"
        "留下的两类只指向你**能在页面上自己核对**的东西：读了投影、以及已有边界裁定。"
    )
    lines.append("")
    lines.append(
        "**「我方映射」这一块该怎么用。** 它是我们读完该条正文后自己判的一格座标，"
        "**不是已经定下来的事实**。给它的目的是省你一遍通读，不是替你判。"
        "你不同意就按自己的判断填裁决与理由，**你的裁决优先**。"
        "我们没判出来的，那一块会写「我方没能映射」并说明卡在哪 —— "
        "那不是留白，是提示你这一条我们也拿不准。"
    )
    lines.append("")
    lines.append(
        "若某份工作单的 §2 是 **0 条**，那不等于「本 pair 没问题」—— "
        "60 个 pair 里台账只覆盖 48 个，且覆盖了的也未必覆盖全。"
        "请直接从该份的 §3 与 §4 开始，把发现登记到 §5。"
    )
    lines.append("")
    lines.append("### §D.2 §3 候选新增 issue 的六个来源")
    lines.append("")
    lines.append(
        "本节把**已知但未入账**的线索集中在一处。它们都没有经过人工确认，"
        "列在那里只是因为「有人说过这件事而台账没记」。裁决区留空。"
    )
    lines.append("")
    lines.append("| 小节 | 来源 | 优先级 |")
    lines.append("| :-- | :-- | :-- |")
    lines.append("| §3.1 | 两臂多报侧判为 `VALID_UNRECORDED` 的「真漏记」 | "
                 "最高 —— 已过一轮独立复核，事实部分通常可直接采信 |")
    lines.append("| §3.2a | 审阅 agent 判为 `problem` / `extra` / `uncertain` 却没进台账的 diff | 高 |")
    lines.append("| §3.2a-2 | 上述 diff 里**生成侧写「—」或「不可能生成」**的那一族 | "
                 "另一个物种，见下 |")
    lines.append("| §3.2b | 判为 `correct` / `similar` 的 diff | 备查，不设裁决区 |")
    lines.append("| §3.3 | 两臂产出中机械未匹配任何台账条目的 issue | 中 —— 量大，按出现格数排序 |")
    lines.append("| §3.4 | 已被判为「非缺陷」的多报簇 | 备查 —— 避免与既有裁定撞车 |")
    lines.append("| §3.6 | `pyfcstm inspect` 的**确定性检查**发现（归一化后） | "
                 "**另一个物种** —— 见下，不是 LLM 产出，没有采样噪声 |")
    lines.append("| §3.5 | 与台账同根、但匹配器未归并的簇 | "
                 "**「台账偏浅」的直接证据** —— 对应条目适合走「修正」 |")
    lines.append("")
    lines.append(
        "**§3 的每一条也带一块「我方映射」**，读法同 §D.1，但多一层保留："
        "候选**本身尚未被认定**，所以映射的是「**若这条线索成立**，它属于座标系的哪一格」，"
        "**不代表它成立**。它是不是一条真缺陷，正是要你判的。"
    )
    lines.append("")
    lines.append(
        "**三类候选的粒度不同构，别当成同一种东西。** `VU-` 与 `DIFF-` 是"
        "「一条 = 一个主张」，映射成一格座标是有意义的。`UM-` 不是："
        "一个 `UM-<pair>` 填写块对应 §3.3 **整张表**（全语料 619 组，中位 11 组/桶）。"
        "所以它的映射多数写「我方没能映射」，而卡点是**登记单位**"
        "（一格代表不了一整张表），**不是**座标系给不出取值 —— "
        "逐组拆开后各组基本都能落格。"
    )
    lines.append("")
    lines.append(
        "**§3.2a-2 是另一个物种，不要跟 §3.2a 混算。** 这一族的生成侧"
        "**逐字否认作者制品在该处有东西**（写的就是「—」或「(不可能生成)」）。"
        "它们真正主张的是**参考模型 / 真值本身的有效性**"
        "（「参考侧含 NL 推不出的内容，任何 LLM 都无法复现，却会被计成漏检」），"
        "而不是一种缺陷形态。缺陷座标系的判定测试全部落在**作者源 PlantUML** 上，"
        "而这类在制品内指不出任何一处。所以它们映射不上**不能**算作"
        "「新座标系覆盖不到」—— 它们本来就不在座标系要描述的对象集合里。"
        "它们仍然值得判：若你认为某条其实指出了制品的真问题，照常走「采纳」；"
        "若你认为它是对参考模型的质疑，请在理由里写清楚。"
    )
    lines.append("")
    lines.append(
        "**§3.2 的已知证据缺口**：当年**没有单独记录「为什么不收」**，"
        "只留下了该 diff 被判成什么。所以「排除理由」给的是它的 `verdict` "
        "与判定者写的 `reason`，不是一条真正的排除论证。"
    )
    lines.append("")
    lines.append("| 判定 | 怎么读 |")
    lines.append("| :-- | :-- |")
    for verdict, note in _DIFF_VERDICT_NOTE.items():
        lines.append(f"| `{verdict}` | {esc(note)} |")
    lines.append("")
    lines.append(
        "§3.2b 的 `correct` / `similar` 列在工作单里是为了**自包含**：若你在 §4 发现某处确有问题，"
        "可以先查它是不是已经被人看过并判过没问题。要推翻的话，直接在 §5 登记新条目。"
    )
    lines.append("")
    lines.append(
        "§3.3 的 X1 侧**全部已有多报侧裁定**（已归入 X1 的多报桶并给了 verdict）。"
        "那些裁定是**另一轮**判定者做的，你可以推翻 —— "
        "尤其 `NO_NL_BASIS`：它只说「NL 没有逐字依据」，"
        "而合式性层的缺陷本来就不要求 NL 依据（台账自己有 30 条这样的记录）。"
        "**出现格数越多越值得看** —— 六格里出现五六次的主张，不太可能是单次采样噪声。"
    )
    lines.append("")
    lines.append(
        "§3.3 的**主臂多报簇没有逐条回链到格**（`G*.jsonl` 只给 `cells_of_6` 计数、"
        "不给成员清单），所以那一栏**无法**标出哪些已被裁定 —— 需自行对照同一份工作单的 §3.4。"
        "全语料有 **102 条**主臂未匹配 issue 落在 6 个 pair"
        "（`0005` `0015` `0025` `0035` `0042` `0045`）上却**零多报簇**，"
        "即那 6 个 pair 的这一栏完全没有被裁定过。"
    )
    lines.append("")
    lines.append(
        "§3.4 列的是两臂报过、但复核判为不成立的主张。它们**不是**候选 —— "
        "列出来是为了让你在 §4 发现同一形状时，能立刻看到「这条已经被判过，理由是这个」，"
        "避免重复劳动或与既有裁定冲突。"
    )
    lines.append("")
    # ⭐ §3.6 的读法必须写在这里 —— ⚠️ 它是六个来源里**唯一**不带采样噪声的那个，
    # ⛔ 判读者若拿它跟前五个同样对待，会把「工具没报」当成「不存在」。
    lines.append(
        "**§3.6 与前五个来源不是同一个物种。** 前五个全部出自 **LLM 产出**（两臂的 issue、"
        "审阅 agent 的 diff、多报簇），带采样噪声 —— 同一个格重跑一次可能就没了。"
        "§3.6 出自 `pyfcstm inspect --format json --enable-verify`，是**确定性检查**："
        "同一份 `model.fcstm` 永远给同一批诊断。于是「没报」这件事的含义也不同："
        "前五个的沉默是采样问题，§3.6 的沉默说明**检查器本身看不到那类东西**。"
    )
    lines.append("")
    lines.append(
        "**§3.6 的四条读法。** ① 全语料 454 条原始诊断先经「内生 / 投影产物 / 不确定」分拣加"
        "一轮对抗性复核，查明是**投影产物**的 84 条不在工作单里；② 余下的按**根因归一化**（360 条"
        "诊断 → 189 条 issue，`0007` 一份就是 35 → 7），所以你看到的一条背后常常是好几条诊断，"
        "折叠区里能展开原始 message；③ 判重后**与既有台账 / 候选是同一个问题的那 61 条不在 §3.6**，"
        "它们作为补充证据挂在 §2 / §3 对应条目下面，同一个问题只裁一次；④ `§3.6b` 是"
        "「分拣未能确定是内生还是投影产物」的一族，**事实本身还没定**，摆出来是因为不许静默丢掉。"
    )
    lines.append("")
    lines.append(
        "**§3.6 有一个必须先知道的工具缺陷**：`W_DEADLOCK_LEAF` 有**系统性假阳性** —— "
        "pyfcstm 的 `analyzers/structural.py:75-93` 只数叶态自身的出边、完全不查外层，"
        "于是「嵌在复合态里、而外层复合态有成组迁移」的叶态一律被误报成终止态"
        "（顶层态没有外层，不受影响）。裁决这一族之前请先数一遍该叶态各级祖先的出边。"
    )
    lines.append("")
    lines.append(
        "§3.5 这类最能说明问题：**同一个缺陷**，两臂用了另一种谓词或另一种措辞表述，"
        "台账那一条就没能覆盖。它们不算新增缺陷，但**它们说明台账那一条的 statement "
        "写窄了** —— 对应的台账条目适合走「修正」而不是「保留」。"
    )
    lines.append("")
    lines.append("### §D.3 §4 深度检查清单")
    lines.append("")
    lines.append(
        "清单里的每一条都是**待核问句**，不是结论。机械判据写在每条下方，"
        "判错了就直接在「发现」里写「机械判错，理由 X」。"
        "勾选 `[x]` 表示**已看过**；「发现:」留空表示看过但无发现。"
    )
    lines.append("")
    lines.append(
        "**界外的东西照常记，但落点不同**。project_1 的建模对象是 $M = (S, E, V, Tr, A)$，"
        "没有 $C$、没有 $Inv$、没有区分量，所以下面两族不计入缺陷统计："
        "① **正交区并发**（fork/join、区域同时活跃、区应当有几个）—— 维度 A 有专属取值 "
        "`region`，勾它即表示界外，`counts_as_defect = false`；"
        "② **时钟 / 计时 / 秒级约束 / 不变式** —— 没有专属取值，写进 `statement` 自由文本，"
        "回收后由主 session 人工分拣。"
        "⚠️ 一律不记是**旧口径**，2026-08-13 已撤销：不记会让这批发现既进不了记录、"
        "也进不了统计，等于反过来声称这些模型没有并发问题 —— 那同样是错的。"
    )
    lines.append("")
    return "\n".join(lines)

def segs_hint(pair):
    """给出本 pair 真实存在的第一个段 id，供 `nl_evidence` 的填写示例用。"""
    segs, _ = S.nl_segments(pair)
    return segs[0][0] if segs else "NL-L001"


# ------------------------------------------------------------------ 组装

def build_doc(pair, saved):
    model = PumlModel(S.puml_text(pair), pair)
    records = S.ledger_records(pair)
    segs, _ = S.nl_segments(pair)

    keys = []
    head = []
    head.append(f"<!-- RELABEL schema={SCHEMA} pair={pair} -->")
    head.append(f"# 人工重标工作单 · pair `{pair}`")
    head.append("")
    head.append(
        "本文件由 [generate.py](../generate.py) 生成，**只有 `FILL:BEGIN`/`FILL:END` "
        "之间的内容是给人填的**。其余部分重跑生成器会被覆盖；填写内容会按 key 保留。"
    )
    head.append("")
    head.append(
        f"开工前两份必读：同目录的 [{S.NL_DOC}](./{S.NL_DOC})（本 pair 的 NL 规约与译文，"
        f"同组 {len(S.nl_siblings(pair))} 份共用）与 "
        f"[{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO})（填写说明，54 份共用）。"
        "回收用 [collect.py](../collect.py)，校验用 [validate.py](../validate.py)，"
        "口径见 [README.md](../README.md)。"
    )
    head.append("")

    head += _howto_inline(pair)

    pair_key = f"PAIR-{pair}"
    keys.append(pair_key)
    head.append("## §0 本 pair 结论（做完再填）")
    head.append("")
    head.append(fb.render(pair_key, "pair", fb.PAIR_TEMPLATE, saved.get(pair_key)))
    head.append("")
    # ⭐ 待处理速览摆在 §0 之后：先让人知道这份要花多少工夫，再进正文。
    head += DT.pair_overview(pair)

    body = [section_material(pair, model)]

    s2, k2 = section_ledger(pair, records, saved)
    body.append(s2)
    keys += k2

    s3, k3 = section_candidates(pair, model, records, saved)
    body.append(s3)
    keys += k3

    s36, k36 = section_inspect(pair, saved)
    body.append(s36)
    keys += k36

    # ⛔⛔ **§4 深度检查清单与 §5 新增登记于 2026-08-14 整体拆除。**
    #
    # 用户裁定：本轮工作单只做一件事 —— **对现有台账 + 候选逐条裁决**。⭐ 拆除的理由不是
    # 嫌长，是**任务边界**：清单在引导判读者去「挖新的」，新增登记在收「挖出来的」，
    # ⛔ 而本轮要的是「已有这 380 条哪些站得住」。两件事混在一份工作单里，注意力会被
    # 从裁决拉到发掘上，而发掘那一路的产物（`NEW-` 块）本轮没有下游消费者。
    #
    # ⚠️ 代码没删：`section_checklist()` / `section_new()` / `checklist.py` / `newfields.py`
    # 仍在，⭐ 因为下一轮若要重开「挖深」，它们连同 27 个取值的枚举图例可以整段接回来 ——
    # 删掉等于把那批口径连同 Dwyer 句式骨架一起丢了。⛔ 只是不再装进 `build_doc`。
    # 已填过的 `CHK-` / `NEW-` 内容不会丢：它们会落进 §9 孤儿填写区（下面那段）。
    doc = "\n".join(head) + "\n" + "\n".join(body)

    # 孤儿填写区：旧文件里有、新骨架里没有的 key。
    #
    # ⛔ **原样未填的块不算孤儿，直接丢。** ⚠️ 它按定义不含任何人工内容，留着只会在 §9
    # 堆出一批空模板 —— 实测：inspect 发现改成「与既有条目重合的并入、不新建 `INS-` 块」
    # 之后，上一版渲染过的 51 个空 `INS-` 块全部落进了 §9，而它们一个字都没填过。
    # ⭐ 判据仍是 `fb.is_untouched`（勾选记号与冒号后有没有写东西），⛔ 只要填过就保留。
    # ⚠️ 判据必须按 key 的种类选。⛔ 清单块走通用 `is_untouched` 会被误判成「填过了」——
    # 它的模板含逐条 id 与机械判据行，一个字没填也与空模板不字面相等。这个坑 `collect.py`
    # 里已经栽过一次（`0039` 五个未填清单块里四个被误报），⭐ 这里读同一份判据真源。
    # ⚠️ 2026-08-14 §4/§5 拆除后这条立刻要紧：54 份的 `CHK-` 块全部变成待判孤儿，
    # ⛔ 若判错，六个空清单块会逐份堆进 §9。
    def _orphan_kept(k, v):
        if k.startswith("CHK-"):
            return not fb.checklist_is_untouched(v)
        return not fb.is_untouched(v, "candidate", pair, key=k)

    orphans = {k: v for k, v in saved.items()
               if k not in set(keys) and _orphan_kept(k, v)}
    if orphans:
        tail = ["## §9 孤儿填写区（材料变动导致这些 key 不再出现在正文）", ""]
        tail.append(
            "这里的内容**不会丢**，但也不会被 `collect.py` 当作正文裁决计入。"
            "请把它们并回对应的新条目后删掉。"
        )
        tail.append("")
        for k, v in sorted(orphans.items()):
            tail.append(fb.render(k, "orphan", v))
            tail.append("")
        doc += "\n" + "\n".join(tail)

    return doc, keys


def _write_if_changed(path, doc, check):
    """⭐ 返回 `True` 表示内容与盘上不同。⛔ `check` 为真时只判不写。

    ⚠️ 只在**内容真的变了**时写盘 —— ⛔ 无条件重写会把 mtime 全刷一遍，
    于是「哪些工作单这一轮真的变了」再也看不出来。
    """
    old = None
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as fh:
            old = fh.read()
    if doc == old:
        return False
    if not check:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(doc)
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pairs", nargs="*", default=None)
    ap.add_argument("--sample", type=int, default=None,
                    help="只生成前 N 个在评 pair（用于先给作者过目格式）")
    ap.add_argument("--check", action="store_true", help="只报告差异，不写盘")
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args()

    pairs = args.pairs or list(S.IN_SCOPE_PAIRS)
    if args.sample:
        pairs = pairs[: args.sample]

    changed, unchanged = [], []
    shared = []

    # ⭐ 共用页先写：54 份工作单都靠链接指过来，⛔ 缺了它们工作单就不自包含。
    # ⚠️ 只写**本轮涉及的** NL 组 —— `--pairs 0000` 不该顺手重写另外 8 组。
    if _write_if_changed(S.howto_path(args.out), build_howto(), args.check):
        shared.append(S.WORKSHEET_HOWTO)
    for dirname in sorted({S.nl_dir(p) for p in pairs
                           if p not in S.OUT_OF_SCOPE_PAIRS}):
        path = os.path.join(args.out, dirname, S.NL_DOC)
        if _write_if_changed(path, build_nl_doc(dirname), args.check):
            shared.append(f"{dirname}/{S.NL_DOC}")

    for pair in pairs:
        if pair in S.OUT_OF_SCOPE_PAIRS:
            print(f"跳过 {pair}：`00x8` 越界 pair，不在评测网格内")
            continue
        path = S.worksheet_path(args.out, pair)
        old = ""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fh:
                old = fh.read()
        saved = fb.extract(old)
        doc, _ = build_doc(pair, saved)
        if doc == old:
            unchanged.append(pair)
            continue
        changed.append(pair)
        if not args.check:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(doc)

    print(json.dumps({
        "schema": SCHEMA,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "pairs": len(pairs),
        "written" if not args.check else "would_write": len(changed),
        "unchanged": len(unchanged),
        "shared_written" if not args.check else "shared_would_write": shared,
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
