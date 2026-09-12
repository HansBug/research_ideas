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
import itemblock as IB                              # noqa: E402
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
    lines.append("## 怎么填（先读这 6 条 —— 写法不对会被**静默丢掉**）")
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
    # ⛔ 原第 6、7 条讲的是 §4 深度检查清单与 §5 新增登记的填法 —— ⚠️ 那两节已整节拆除
    # （工作单现在只有 §0–§3），⭐ 说明也随之删掉。⛔ 留着会指向不存在的小节。
    lines.append(
        "6. **不适用就留空**（回收成 `null`）；查过了、结论是「没有」，"
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
        f"「这条边有没有」一律到本页 §1.2（作者源，带行号）与 §1.3（参考模型）自己核。"
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
        "(../../../../../corpora/nl_segmentation/overrides.json)")
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


def _flow(text):
    r"""把一段判定文字压成一行（段内不许硬折行，见 CLAUDE.md §2.2.1b）。

    ⛔ 与 `esc()` 不同：**不转义 `|`** —— 表格单元格里的转义由
    [dtier.py](./dtier.py) 的 `_cell()` 负责，⚠️ 这里的产物进的是普通段落。
    """
    return IB.safe_md(re.sub(r"\s+", " ", str(text or "")).strip())


#: UM- 撤出后失去宿主的 5 条 `INS-` 的重新归属裁定（逐条理由见该文件）。
REHOST = os.path.join(HERE, "um_orphan_rehost.json")


def _rehost():
    """读 UM- 孤儿的重新归属表。⭐ 缺文件返回空表，⛔ 不静默编造归属。"""
    if not os.path.exists(REHOST):
        return {}
    with open(REHOST, encoding="utf-8") as fh:
        return json.load(fh).get("decisions") or {}


def _merged_ins(pair):
    """本 pair 里**被并入别的条目**、因而不单独设裁决区的 `INS-` id → 宿主 id。

    ⭐ 判读者对同一个问题只裁一次：裁决落在宿主条目上，⛔ 被并入的那条不另设裁决区。
    ⚠️ 但它的事实**不许丢** —— 它作为「补充证据」印进宿主的问题描述里（见 `_desc_ledger`）。
    """
    out = {}
    hosts = [r["id"] for r in S.ledger_records(pair)]
    hosts += [k for k, v in CM.candidate_index().items() if v["pair"] == pair]
    for host in hosts:
        for rec in IF.merged_into(host):
            out[rec["issue_id"]] = (host, rec)
    # ⭐⭐ UM- 一族撤出后，原本并入 UM 桶的 5 条失去宿主。⛔ 那时的「重复」是相对 UM 桶成立的，
    # ⚠️ 而 UM 一条 = 整张表，故「与 UM-0050 重复」只表示「落在那张表的某一组里」——
    # ⛔ 不表示它与另一条独立候选重复。⭐ 真正要回答的是：这几条**彼此之间**有没有重复。
    # 逐条裁定在 [um_orphan_rehost.json](./um_orphan_rehost.json)，⭐ 判据是「一次修复是否
    # 同时消掉两条」。⛔ 本处只消费裁定，不自行推断。
    for rid, d in _rehost().items():
        if not rid.startswith(f"INS-{pair}-"):
            continue
        if d.get("role") == "merged":
            rec = next((x for x in IF.issues_of(pair) if x["issue_id"] == rid), None)
            if rec is not None:
                out[rid] = (d["into"], rec)
        else:                       # ⭐ role == "host"：自立门户，⛔ 从并入表里摘掉
            out.pop(rid, None)
    return out


def _supplements(target, pair):
    """并入 `target` 的补充证据行。⭐ 只印事实，⛔ 不印工具名与诊断码。

    ⭐⭐ **必须印出被并入条目的 id。** ⚠️ 不印时那 56 条并入项在整份 md 里一个字都不出现，
    ⛔ 于是「按 id 搜不到」与「这条不存在」无法区分 —— 2026-08-16 用户就是这么发现
    `INS-0050-01` 失踪的。⭐ 印了 id，`grep` 就找得到、账也对得上，⛔ 而**不需要**给它
    另开裁决区（那会把去重掉的重复重新摆出来，实测一摆就是 56 条）。

    ⚠️ 若并入项自己的三方判读结论与宿主**不同**，在同一行点出来 —— ⭐ 这是判读者在这一个
    裁决点上唯一能看到该分歧的地方。⛔ 但仍然只裁一次：分歧是提示，不是第二个裁决区。
    """
    out = []
    rows = list(IF.merged_into(target))
    # ⭐ 宿主也可能是一条 `INS-`（UM- 撤出后重新归属的结果），⛔ 那种关系只在覆盖表里。
    for rid_, d in _rehost().items():
        if d.get("role") == "merged" and d.get("into") == target:
            rec_ = next((x for x in IF.issues_of(pair) if x["issue_id"] == rid_), None)
            if rec_ is not None:
                rows.append(rec_)
    for rec in rows:
        txt = _flow(rec.get("statement"))
        if not txt:
            continue
        rid = rec.get("issue_id")
        note = ""
        if rid:
            _, why = DT.merged_needs_own_block(rid, target)
            if why and not why.startswith("宿主已撤出"):
                note = f"　⚠️ **它的独立判读与本条不同**：{why}。"
        # ⭐ 必须是列表项：⛔ 两条并列的加粗段落挨在一起就是段内硬折行（CLAUDE.md §2.2.1b），
        # ⚠️ `tools.unwrap_markdown --check` 会直接报，实测栽过一次。
        out.append(f"- **补充证据（`{rid}`，与本条判为同一个问题）**：{txt}{note}")
    return out


def _desc_ledger(rec, pair):
    """台账条目的问题描述。⭐ 只取 `statement`，⛔ 不再印参考侧/生成侧两行。

    ⚠️ 那两行用的是流水线内部术语（「参考侧」「生成侧」），⛔ 且与 `statement` 高度重复 ——
    判读者要的是「这条主张的是什么」，不是「它是怎么被比出来的」。
    """
    return _flow(rec.get("statement"))


def _desc_vu(r):
    """`VU-` 的问题描述：主张 + 复核认定的事实（+ NL 侧说明）。"""
    bits = []
    if (r.get("claim") or "").strip():
        bits.append(_flow(r["claim"]))
    if (r.get("fact") or "").strip():
        bits.append("复核认定的事实：" + _flow(r["fact"]))
    if (r.get("nl") or "").strip():
        bits.append("NL 侧：" + _flow(r["nl"]))
    return "　".join(bits)


def _desc_diff(d):
    """`DIFF-` 的问题描述：两侧的差 + 当年判定者给的理由。"""
    bits = []
    ref, gen = _flow(d.get("ref")), _flow(d.get("gen"))
    if ref or gen:
        bits.append(f"参考模型里是「{ref or '—'}」，被判制品里是「{gen or '—'}」")
    if (d.get("reason") or "").strip():
        bits.append("差异说明：" + _flow(d["reason"]))
    return "　".join(bits)


def _desc_um(pair, x1, v46):
    """`UM-` 的问题描述 —— ⭐ 本轮重写的重点。

    ⛔⛔ **旧版只印一张原始表格，读者根本看不出问题是什么**（用户原话：「UM-0000 里面
    到底是啥问题你都没说清楚啊，我都没看懂」）。⚠️ 原因是那张表按「多报簇」组织，
    一行是一个簇、同一个底层事实按不同 `REQ-` id 出现好几行，⛔ 而表里没有任何一处
    告诉读者「这些行合起来在说几件事」。

    ⭐ 现在改成：**把同文的行去重后逐条列出，并标出各自出现在几个格里**。
    ⚠️ 归一化（哪几行其实是一件事）由人工 meta review 给出 —— ⛔ 脚本不做那个判断。
    """
    seen, rows = set(), []
    for g in x1 + v46:
        for m in g["members"]:
            t = _flow(m.get("issue"))
            if not t or t in seen:
                continue
            seen.add(t)
            reqs = sorted({r for r in (m.get("requirement_ids") or [])})  # 可能为空
            rows.append((g["cell_count"], t, reqs))
    rows.sort(key=lambda x: -x[0])
    head = (f"本 pair 有 **{len(x1) + len(v46)}** 组多报簇没能机械匹配到任何台账条目，"
            f"去重后共 **{len(rows)}** 种说法。⚠️ 其中不少是**同一个底层事实按不同需求 id "
            f"重复登记**，⛔ 照条数补入台账会把一个缺陷记成好几条 —— "
            f"归一化成几条事实由下面的 meta review 给出。")
    detail = ["", "逐条说法（按出现格数降序）：", ""]
    for n, t, reqs in rows[:24]:
        tag = f"（{'、'.join(f'`{r}`' for r in reqs[:3])}）" if reqs else ""
        detail.append(f"- **{n} 格**：{t}{tag}")
    if len(rows) > 24:
        detail.append(f"- …… 另有 {len(rows) - 24} 种说法，"
                      f"逐条见 [unmatched_issues.json](../unmatched_issues.json)")
    detail.append("")
    return head, detail


def section_ledger(pair, records, saved):
    """§2 现有 expected issue 逐条裁决。⭐ 版式由 [itemblock.py](./itemblock.py) 统一。"""
    lines = ["## §2 现有 expected issue 逐条裁决", ""]
    if not records:
        lines += ["**本 pair 台账 0 条。** 这不等于「本 pair 没问题」—— 请直接从 §3 开始；"
                  f"理由见 [{S.WORKSHEET_HOWTO}](../{S.WORKSHEET_HOWTO}) §D.1。", ""]
        return "\n".join(lines), []
    lines += [f"本 pair 共 **{len(records)}** 条。{IB.SECTION_NOTE}", ""]
    keys = []
    for rec in records:
        rid = rec["id"]
        keys.append(rid)
        lines += IB.render(rid, _desc_ledger(rec, pair), LM.for_record(rid), saved,
                           fb, DT, kind="ledger",
                           extra=_supplements(rid, pair))
    return "\n".join(lines), keys


def section_candidates(pair, model, records, saved):
    """§3 候选 issue 逐条裁决。

    ⚠️⚠️ **2026-08-14 重构：⛔ 按来源分的小节全部拆掉。** 此前分成 §3.1 真漏记 /
    §3.2 未采纳的 diff / §3.3 机械未匹配 / §3.4 已判非缺陷 / §3.5 同根未归并 /
    §3.6 inspect 确定性发现，⛔ 六个小节各有一套版式与导语。
    ⭐ 用户裁定：「这个 issue 是怎么来的是 inspect 还是什么统统不重要」——
    故现在**一个平铺列表**，所有候选条目同一版式，⛔ 不再标注来源。
    """
    lines = ["## §3 候选 issue 逐条裁决", ""]
    lines += ["本节是**已知但未入账**的线索，与 §2 同一版式、同一裁决口径。"
              f"{IB.SECTION_NOTE}", ""]
    keys = []
    merged = _merged_ins(pair)
    judged = DT.load_rulings()

    def _skip(key):
        """⭐ **只渲被三方判读过的条目。**

        ⚠️⚠️ 这条过滤替代了旧的「按 verdict 分 §3.2a 设裁决区 / §3.2b 只备查」——
        ⛔ 旧规则的判据是「当年判定者给了什么 verdict」，⚠️ 而那与「这一条现在该不该由你裁」
        没有关系。⭐ 新判据自洽：**工作单上有裁决区的，就是有三方判定 + 人工 meta review 的**，
        ⛔ 不会出现一个空白块让你对着它发呆（实测旧规则改版后一度渲出 374 个空白块）。
        ⭐ `UM-` 一族例外：它不在判读包内，但有人工 meta review，故照渲。
        """
        return key not in judged and not key.startswith("UM-")

    # ---- 真漏记
    for i, r in enumerate(S.valid_unrecorded(pair), 1):
        key = f"VU-{pair}-{i:02d}"
        if _skip(key):
            continue
        keys.append(key)
        lines += IB.render(key, _desc_vu(r), CM.for_candidate(key), saved, fb, DT,
                           extra=_supplements(key, pair))
    # ---- 未采纳的 diff
    adopted = S.adopted_diff_ids(pair)
    for i, d in S.unadopted_diffs(pair):
        key = f"DIFF-{pair}-{i:02d}"
        if _skip(key):
            continue
        keys.append(key)
        lines += IB.render(key, _desc_diff(d), CM.for_candidate(key), saved, fb, DT,
                           extra=_supplements(key, pair))
    # ⛔⛔ **`UM-` 一族于 2026-08-16 整批撤除。** 裁定与全部证据见
    # [docs/findings/um_residue_ruling.md](../../../../discover_matrix/docs/findings/um_residue_ruling.md)。三条理由：
    #   ① X1 那一半 333/334 条的簇号**精确**出现在 `sources.other_unexpected()` 的已裁定表里，
    #      而那些裁定 96% 判的是「不是作者制品的缺陷」——⛔ 把它们放进工作单等于重审已结案的东西；
    #      ⚠️ 其中 4% 真漏记早已提取成 `VU-` 系列，于是 UM 表与 VU 块**重复计数** 12 条。
    #   ② v46 那一半的主体是 `REPRESENTATION_DEBT`（投影债务）——`0029-1` 簇的 merge_reason 逐字：
    #      「损失通道唯一——R4.5 把整条标签压成一个原子事件名」。⛔ 按 P2 不算作者缺陷。
    #   ③ 登记单位从头不对：47/49 块是 `unit_of_record` 卡点，单块最多承载 35 组，
    #      ⚠️ 而 D 档判定程序判的是**一条可陈述的主张**，一张表没有单一 statement 可判。
    # ⭐ 残余 143 条归一化事实另存 [unmatched_residue.json](../unmatched_residue.json)，
    # ⛔ 不进工作单、不设裁决区、无 D 档判读。
    # ⚠️ `S.unmatched_issues()` 与 `regroup_unmatched()` **未删** —— 恢复时要从残余清单里
    # 逐条拆成独立候选再送三方判读，⛔ 一块对应一张表的形态不许再出现。
    # ---- 确定性检查发现（⛔ 不标来源；被并入别条的不单独设块）
    for rec in IF.issues_of(pair):
        rid = rec["issue_id"]
        if _skip(rid):
            continue
        # ⛔⛔ **被判定为重复的条目一律不出块** —— ⭐ 用户裁定（2026-08-16）：
        # 重复项不进台账、不进 md、**不拿去让人裁决**。
        #
        # ⚠️ 这里 2026-08-16 内来回改过两次，两次都错，记下来免得再犯：
        #
        #   ⛔ **第一版**：按「已并入宿主」跳过全部 61 条。⚠️ 漏了一种情况 —— `UM-` 一族
        #      整批撤出后，5 条并入它们的 `INS-` 连宿主一起消失，⛔ 于是既无块、也无宿主，
        #      在整份 md 里一个字都不出现；⚠️ 而速览行还点名说它们「需你处理」，
        #      用户按 id 去搜搜不到（`INS-0050-01`）。
        #   ⛔ **第二版**：改成「每条判读都出块」，让块数等于判读包的 380。⛔⛔ 那是把块数
        #      对到了一个**未去重**的数上 —— 按构造必然把 56 条真重复重新摆出来。实测
        #      `0010` 上同一个缺陷出现三次（`EIS-0010-03` + `INS-0010-01` + `INS-0010-02`，
        #      而后两条自己就写着「见 INS-0010-01」，补一条 `AutonomousFinal --> [*]`
        #      三条一起消失）。
        #
        # ⭐ **正确的分界：「找得到 / 对得上账」与「有独立裁决区」是两件事。**
        #   · 找得到 → 在宿主的补充证据行里印出被并入的 id（见 `_supplements`）
        #   · 对得上账 → 321 = 380 − 59（见 `test_the_dedup_is_not_undone`）
        #   · 有裁决区 → **只有去重后剩下的那 321 条**
        #
        # ⭐ 唯一例外是宿主已撤出的那 5 条：它们无处可并，**不是重复**，必须自己出块。
        if rid in merged:
            need, why = DT.merged_needs_own_block(rid, merged[rid][0])
            if not (need and why and why.startswith("宿主已撤出")):
                continue
        keys.append(rid)
        # ⭐ `INS-` 的五轴直接挂在记录上（不像台账/候选走 mapping 文件），⛔ 就地包一层。
        mp = {"mappable": True, "id": rid}
        mp.update({k: rec.get(k) for k in IB.AXES})
        mp[NF.OTHER_NOTE_FIELD] = rec.get(NF.OTHER_NOTE_FIELD)
        # ⭐ 走到这里的条目都是**宿主条目**，⛔ 不加任何「曾被判为重复」的说明 ——
        # ⚠️ 那种说明会让读者以为这一条的地位低于别的条目，而它并不低。
        #
        # ⭐⭐ 但**并入本条的事实必须印出来**：`INS-` 也可以当宿主（UM- 撤出后重新归属的
        # 结果，如 `INS-0050-02` 收下了 `INS-0050-03`）。⛔ 此前 `_supplements` 只接在台账
        # 描述上，⚠️ 于是 `INS-0050-03` 的事实在 md 里一个字都不剩 —— 那是把「不重复出块」
        # 做成了「把证据删掉」，⛔ 两件事必须分开。
        lines += IB.render(rid, _flow(rec.get("statement")), mp, saved, fb, DT,
                           extra=_supplements(rid, pair))
    if len(keys) == 0:
        lines += ["本 pair 无候选线索。", ""]
    return "\n".join(lines), keys


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
        + "[defect_taxonomy.md](../../../../../discover_matrix/docs/protocol/defect_taxonomy.md)"
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
    [defect_taxonomy.md](../../../../../discover_matrix/docs/protocol/defect_taxonomy.md)，
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
    # ⭐ 条目数口径放在最前面 —— ⛔ 填表的人第一眼就该看到正确的数，
    # ⚠️ 免得再有人拿未去重的 380 当条目总数（2026-08-16 实测代价见 DEDUP_ACCOUNTING.md）。
    lines.append(
        "**条目数口径：工作单共 321 个裁决区**（§2 台账 99 + §3 候选 222 ="
        " `VU` 15 + `DIFF` 77 + `INS` 130）。三方 D 档判读做过 **380** 条，"
        "**那个数没有去重** —— 其中 59 条被判定为「与另一条是同一个问题」，"
        "只作补充证据印在宿主条目的问题描述里、不设裁决区。"
        "完整账目见 [DEDUP_ACCOUNTING.md](./DEDUP_ACCOUNTING.md)。"
    )
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
    # ⛔ §4 深度检查清单与 §5 新增登记已**整节拆除**（用户裁定：只保留对现有台账 + 候选的
    # 裁决）。⚠️ 目录里再指它们就是把读者引向不存在的小节 —— 故 §B/§C 标注为背景材料。
    lines.append("| §B | ⚠️ **§5 登记已拆除**，本节保留为历史背景 | —（不再有跳转来源）|")
    lines.append("| §C | 座标系为什么长这样（背景，填表时可跳过） | —（不再有跳转来源）|")
    lines.append("| §D | §2 / §3 两节的通用读法 | §2 · §3 开头 |")
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
        "因为其余都要读文意（[CLAUDE.md](../../../../../../CLAUDE.md) §11：只有能被完美判定的"
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
        "逐条出处见 [defect_taxonomy.md](../../../../discover_matrix/docs/protocol/defect_taxonomy.md)。"
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
    lines.append("### §D.2 §3 候选 issue：与 §2 同一版式、同一口径")
    lines.append("")
    lines.append(
        "⚠️ **先记一条已知证据缺口**：候选里那批「审阅 agent 产出但未进台账」的线索，"
        "当年**没有单独记录「为什么不收」** —— 只留下了它被判成什么。 所以工作单里给的"
        "是两侧的差与当年判定者写的理由，**不是一条真正的排除论证**。换言之："
        "「它当年没被收」不构成「它不成立」的依据，️ 你可以直接推翻。"
    )
    lines.append("")
    lines.append(
        "️ **2026-08-14 本节整体重写， 旧的「六个来源」分节已拆除。** "
        "此前 §3 按线索的来源分成六个小节（真漏记 / 未采纳的 diff / 机械未匹配 / "
        "已判非缺陷 / 同根未归并 / 确定性检查发现）， 每节各有一套版式与导语。"
    )
    lines.append("")
    lines.append(
        "拆除的理由是**来源不影响判定**：一条主张成不成立，取决于它指的结构事实在不在、"
        "被违反的义务能不能陈述、反驳站不站得住 ——  与「它是哪个工具报的」无关。"
        "️ 而按来源分节的代价是实打实的：同一个问题在不同小节里长得不一样，"
        "读者得先学会六套版式才能开始判。"
    )
    lines.append("")
    lines.append(
        "现在 §2 与 §3 的每一条都是**同一个四段式**："
        "**问题类型 → 问题描述 → 三方判定 → meta review → 裁决区**。"
        " 顺序固定不许改：先知道这是什么问题，再看三方怎么判，再看我方推荐，最后才动笔。"
    )
    lines.append("")
    lines.append("| 段 | 内容 | 谁写的 |")
    lines.append("| :-- | :-- | :-- |")
    lines.append("| **问题类型** | 五轴座标（`defect_locus` 起的那套），中英双写；"
                 "界外取值当场标明不计分 | 我方推断， 不是定下来的分类 |")
    lines.append("| **问题描述** | 这条主张的是什么 —— 台账取 `statement`，"
                 "候选按各自材料成句 | 上游材料逐字 |")
    lines.append("| **三方判定** | `claude` / `codex` / `dsh` 三行，各自的档位与"
                 "**逐字理由**（含第二读法与设计意图主张） | 三个独立判读臂 |")
    lines.append("| **meta review** | 推荐档位 · 一句话理由 · 展开理由 · 分歧点 · 重点关注 | "
                 "**人工归纳**， 非计算结果 |")
    lines.append("| **裁决区** | `按 D2 采纳` / `按 D1 采纳` / `不采纳` 三选一 + 理由 | "
                 "你填（多数已预填） |")
    lines.append("")
    lines.append(
        "**`D2` 与 `D1` 都进台账，但必须分开记**：`D2` 是「有一条可陈述的被违反义务且"
        "拿不出站得住的反驳」；`D1` 是「两读并立」—— 后者入账时必须把那个第二读法一起记，"
        "️ 否则它会被后人读成一条确定的缺陷。"
    )
    lines.append("")
    lines.append(
        "**标记的含义**：✅ 已定采纳 · ❌ 已定不采纳 · ❓ 三臂一致判两读并立 —— "
        "这三种**不需你动**，裁决区已勾好且没有待填括号；"
        "🟡 两读并立待你选 · 🟠 有偏向待你认可 · 🔴 三方无偏向待你亲裁 —— "
        "这三种的裁决区留了一行待填理由，写一句话即可（哪怕一句）。"
    )
    lines.append("")
    lines.append(
        "⚠️ **`UM-` 一族（每 pair 一块的「机械未匹配多报簇」）已于 2026-08-16 整批撤出。** "
        "裁定与全部证据见 [um_residue_ruling.md](../../../../discover_matrix/docs/findings/um_residue_ruling.md)："
        "X1 那一半 333/334 条的簇号精确出现在已裁定表里（96% 判为非缺陷、4% 真漏记已提取成 `VU-`），"
        "v46 那一半的主体是投影债务（`REPRESENTATION_DEBT`）。残余 143 条归一化事实另存 "
        "[unmatched_residue.json](./unmatched_residue.json)，不进工作单。"
    )
    lines.append("")
    lines.append(
        " **被并入别条的确定性检查发现不单独设裁决区** —— 同一个问题只裁一次，"
        "裁决落在宿主条目上；它的事实作为「补充证据」印在宿主的问题描述之后。"
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

    # ⚠️ `section_inspect` 于 2026-08-14 拆除：⛔ 「这条是 inspect 报的」不影响它成不成立，
    # ⭐ 那些条目现在与其它候选同版式、平铺在 §3 里（见 `section_candidates`）。
    # ⛔ 函数本体保留未删 —— 它带着五条必须逐份印的限定（确定性 vs LLM、压缩比、假阳性、
    # 整类排除、不确定族也要给），⚠️ 若日后要恢复来源分节，那些文字还在。

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
        # ⛔⛔ **必须先问 `is_stale_template`。** ⚠️ `is_untouched` 会先试
        # `DT.prefill(key, kind)` 逐字比对，⛔ 而一旦某个 key 的判读记录 / meta review
        # 被撤掉（`UM-` 一族 2026-08-16 即此），`prefill()` 返回 `None`，
        # 于是它退回「有勾选记号 ⇒ 已填」——⭐ 把**我方预填、人从未动过**的块判成人工内容，
        # 49 个 `UM-` 块因此全部落进 §9 孤儿区。
        # ⭐ `is_stale_template` 走的是**结构判据**（行数 + 末行是占位或尾标），
        # ⛔ 不依赖 prefill 能否重建 —— 那才是「这块原样未填」的正确判据。
        if fb.is_stale_template(v, "candidate", pair):
            return False
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
