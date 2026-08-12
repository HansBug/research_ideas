#!/usr/bin/env python3
"""生成 54 个在评 pair 的人工重标工作单。

用法：

    python3 generate.py                 # 生成 / 刷新全部 54 份（保留已填内容）
    python3 generate.py --pairs 0000 0009 0044
    python3 generate.py --sample 5      # 只做前 5 份样例
    python3 generate.py --check         # 只检查是否需要重新生成，不写盘

⭐ **幂等**：重跑只更新材料部分，人工填写的内容按 key 原样保留（见 `fillblocks.py`）。
若某个 key 在新材料里消失（例如台账条目被改名），旧内容会被搬到文末的「孤儿填写区」，
⛔ 不会静默丢弃。

⛔ 本脚本只读既有数据，**不写** `expected_issue_set.json`、不写任何 verdict、
不写任何 run record。产物只有 `relabel/*.md` 与 `relabel/PROGRESS.md`。
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

import checklist                                    # noqa: E402
import fillblocks as fb                             # noqa: E402
import newfields as NF                              # noqa: E402
import nl_zh                                        # noqa: E402
import sources as S                                 # noqa: E402
from pumlmodel import PumlModel                     # noqa: E402

SCHEMA = "paper1.relabel.worksheet.v1"


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


# ------------------------------------------------------------------ §1 原料

def section_material(pair, model, records):
    segs, seg_mode = S.nl_segments(pair)
    nl = S.nl_text(pair)
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

    # ---- 结构摘要
    lines.append("### §1.1 结构摘要（⭐ 先看这个判复杂度）")
    lines.append("")
    lines.append("| 量 | 值 | 量 | 值 |")
    lines.append("| :-- | --: | :-- | --: |")
    lines.append(f"| 状态总数 | {su['states_total']} | 迁移总数 | {su['transitions']} |")
    lines.append(f"| 其中复合态 | {su['states_composite']} | 顶层初始边 | {su['initial_edges_root']} |")
    lines.append(f"| 其中叶态 | {su['states_leaf']} | 初始边（含区域内） | {su['initial_edges_all']} |")
    lines.append(f"| 未 `state` 声明的 | {su['states_implicit']} | 终态边 `--> [*]` | {su['final_edges']} |")
    lines.append(f"| 最大层次深度 | {su['depth_max']} | 触发词（≈事件） | {su['triggers']} |")
    lines.append(f"| 守卫数 | {su['guards']} | 迁移效应数 | {su['effects']} |")
    lines.append(f"| 状态内动作数 | {su['state_actions']} | 变量候选数 | {su['variable_candidates']} |")
    lines.append(f"| NL 段数 | {len(segs)} | 台账现有条目 | {len(records)} |")
    lines.append("")
    if su["region_separators"]:
        lines.append(
            f"⚠️ 作者源含 **{su['region_separators']} 个 `--` 区分隔符**。"
            "⛔ 正交区并发不在 project_1 的建模对象内（$M$ 无区分量），"
            "凡「这两个区是否同时活跃」类主张一律**越界**，不得作为新增 issue。"
            "但同一段文本里的**顺序结构**主张（可达性、边声明、层次）仍在范围内。"
        )
        lines.append("")
    if model.parse_warnings:
        lines.append("⚠️ 解析告警：" + "；".join(model.parse_warnings))
        lines.append("")

    lines.append(
        "⛔ **口径提醒**：以上全部数字来自**作者源 PlantUML**，"
        "⛔ 不含 `plantuml_source_lowering.py` 投影合成的 "
        "`UnspecifiedInitial` / `InvalidInitial*` / `FinalWait*` / `R45RouteToken`。"
        "谓词层的 `cardinality` 会把它们算进去，所以「作者写了 3 个子态」在谓词层可能是 4 或 7 —— "
        "两个口径都对，但**不能混用**。"
    )
    lines.append("")

    # ---- NL
    lines.append("### §1.2 NL 规约全文")
    lines.append("")
    lines.append(
        f"分段口径：`{seg_mode}`"
        + ("（⭐ 该份规约的编号无法机器判定，分段来自 "
           "[corpora/nl_segmentation/overrides.json](../../../corpora/nl_segmentation/overrides.json) "
           "的人工标注）" if seg_mode == "manual_override" else "（按物理行切，与 pipeline 同口径）")
        + f"，共 {len(segs)} 段。台账里的「NL 第 N 句」按这套编号读。"
    )
    lines.append("")
    lines.append(
        "⛔ **译文是给人判缺陷用的，⛔ 不是给人读着舒服用的。** 它严格直译，"
        "⛔ 不意译、⛔ 不润色、⛔ 不补原文没有的信息；状态名 / 事件名 / 变量名一律保留英文原样，"
        "技术术语保留英文并在括号里给中文。"
        "⭐ 原文含糊的地方译文**照样含糊**，只用 `〔译者存疑：…〕` 点出这里没说清 —— "
        "⛔ 替它消歧就等于替你做了本轮要你自己做的判断。"
        "原文的语法 / 拼写错误照直译并加 `〔原文如此：…〕`。"
        "⭐ 译文是**辅助**，⛔ 判据仍以英文原文为准；两者不一致时以原文为准并请回报。"
        "口径见 [nl_zh.py](./nl_zh.py)。"
    )
    lines.append("")
    lines.append("| 段 id | 原文 | 中文严格翻译 |")
    lines.append("| :-- | :-- | :-- |")
    for sid, txt in segs:
        zh = nl_zh.translate(pair, sid)
        lines.append(f"| `{sid}` | {esc(txt)} | "
                     f"{esc(zh) if zh else '⛔ 缺译文 —— 见 nl_zh.py'} |")
    lines.append("")
    lines.append("<details><summary>NL 原始字节（带物理行号）</summary>")
    lines.append("")
    lines.append("```text")
    lines.append(numbered(nl))
    lines.append("```")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    # ---- 作者源
    lines.append("### §1.3 作者源 PlantUML（被测制品，带行号）")
    lines.append("")
    lines.append(
        "⭐ 行号就是引用锚点 —— 裁决理由里写 `:12` 即指这里的第 12 行。"
    )
    lines.append("")
    lines.append("```text")
    lines.append(numbered(puml))
    lines.append("```")
    lines.append("")

    # ---- 参考模型
    lines.append("### §1.4 参考模型 PlantUML")
    lines.append("")
    if ref:
        lines.append(
            f"来源：作者 workbook `{ref_note}`。"
            "⚠️ **参考模型不是正确答案** —— 语料里多处出现参考侧比生成侧更差的情形"
            "（例如 0000 的参考模型压根没声明 `autonomous_mode` 的状态体）。"
            "它只是「另一个人怎么建的」，用作对照，⛔ 不作为判据。"
        )
        lines.append("")
        lines.append("```text")
        lines.append(numbered(ref))
        lines.append("```")
    else:
        lines.append(f"⛔ 不可用：{ref_note}")
    lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------------ §2 台账逐条

def _fmt_assertions(rec):
    out = []
    for a in rec.get("assertions") or []:
        role = a.get("role")
        expr = a.get("expression")
        measured = a.get("measured")
        extra = []
        if a.get("families"):
            extra.append("族 " + "/".join(a["families"]))
        if measured is not None:
            extra.append(f"实测 `{measured}`")
        if a.get("demoted_because"):
            extra.append("⚠️ " + a["demoted_because"])
        suffix = f"（{'；'.join(extra)}）" if extra else ""
        out.append(f"  - `{role}` · `{expr}`{suffix}")
    return out or ["  - ⛔ **无任何断言表达式**"]


def section_ledger(pair, records, saved):
    lines = []
    lines.append("## §2 现有 expected issue 逐条裁决")
    lines.append("")
    if not records:
        lines.append(
            "⭐ **本 pair 台账 0 条。** ⛔ 这不等于「本 pair 没问题」—— "
            "60 个 pair 里台账只覆盖 48 个，且覆盖了的也未必覆盖全。"
            "请直接从 §3 与 §4 开始，把发现登记到 §5。"
        )
        lines.append("")
        return "\n".join(lines), []

    keys = []
    lines.append(
        f"本 pair 共 **{len(records)}** 条。⛔ 裁决区留空由你填；"
        "自动风险标记只是**提示**，打了标记不等于该条不成立，没打标记也不等于它成立。"
    )
    lines.append("")
    for rec in records:
        rid = rec["id"]
        keys.append(rid)
        flags = S.risk_flags(rec)
        shallow, depth_reasons = S.depth_hint(rec)
        lines.append(f"### {rid}")
        lines.append("")
        lines.append("| 字段 | 值 |")
        lines.append("| :-- | :-- |")
        lines.append(f"| `layer` | `{rec.get('layer')}` |")
        lines.append(f"| `layer_basis` | {esc(rec.get('layer_basis'))} |")
        lines.append(f"| `direction` | `{rec.get('direction')}` |")
        lines.append(f"| `element_of_M` | `{rec.get('element_of_M')}` |")
        lines.append(f"| `decided_by` | `{rec.get('decided_by')}` |")
        lines.append(f"| `primary_predicate` | "
                     f"{'`' + str(rec.get('primary_predicate')) + '`' if rec.get('primary_predicate') else '⛔ 无'} |")
        lines.append(f"| `nl_evidence` | {esc(rec.get('nl_evidence')) if (rec.get('nl_evidence') or '').strip() else '⛔ 空'} |")
        lines.append(f"| `verdict` / `replay` | `{rec.get('verdict')}` / "
                     f"`{(rec.get('replay') or {}).get('verdict')}`"
                     f"（value `{(rec.get('replay') or {}).get('value')}`） |")
        lines.append(f"| 同质组 | `{rec.get('homogeneity_group')}`（组大小 {rec.get('homogeneity_group_size')}） |")
        up = rec.get("upstream") or {}
        lines.append(f"| 上游 | `{up.get('review_file')}` diff #{up.get('diff_index')}"
                     f"；旧台账 {esc(up.get('ledger_e1_ids_on_this_pair')) if up.get('ledger_e1_ids_on_this_pair') else '无'} |")
        lines.append("")
        lines.append("**statement 原文**")
        lines.append("")
        lines.append("> " + (rec.get("statement") or "").replace("\n", "\n> "))
        lines.append("")
        if rec.get("reference_side") or rec.get("generated_side"):
            lines.append(f"- 参考侧：{esc(rec.get('reference_side'))}")
            lines.append(f"- 生成侧：{esc(rec.get('generated_side'))}")
            lines.append("")
        lines.append("**断言组**")
        lines.append("")
        lines.extend(_fmt_assertions(rec))
        lines.append("")
        if flags:
            lines.append("**⛔ 自动风险标记**")
            lines.append("")
            for _, msg in flags:
                lines.append(f"- {msg}")
            lines.append("")
        if shallow:
            lines.append(
                "**⚠️ 深度存疑**：" + "；".join(depth_reasons)
                + "。⭐ 这条**可能偏浅** —— 请判它是否只说到了「某元素不存在」而没说到"
                  "「因此运行时会怎样」。若能加深，走「修正」并写出更强的 statement。"
            )
            lines.append("")
        lines.append(fb.render(rid, "ledger", fb.LEDGER_TEMPLATE, saved.get(rid)))
        lines.append("")
    return "\n".join(lines), keys


# ------------------------------------------------------------------ §3 候选

_DIFF_VERDICT_NOTE = {
    "problem": "⭐ 判定者当年**判为 problem**，却仍未进台账 —— 最值得优先看的一类。",
    "extra": "⭐ 判为 `extra`（生成方凭空新增）。⛔ 台账的 8 类分类学**没有 `extra` 的槽位**，"
             "整类 31 条 / 20% 被结构性漏掉（见 `docs/protocol/ground_truth_limitations.md` §3）。",
    "uncertain": "⚠️ 判为 `uncertain`（当年未决）。",
    "correct": "判为 `correct`（生成方在该点上正确）。",
    "similar": "判为 `similar`（与参考侧等价）。",
}


def section_candidates(pair, model, records, saved):
    lines = []
    keys = []
    lines.append("## §3 候选新增 issue（⭐ 挖深的入口）")
    lines.append("")
    lines.append(
        "本节把**已知但未入账**的线索集中在一处。⛔ 它们都没有经过人工确认，"
        "列在这里只是因为「有人说过这件事而台账没记」。裁决区留空。"
    )
    lines.append("")

    # ---- §3.1 真漏记
    vu = S.valid_unrecorded(pair)
    lines.append("### §3.1 两臂多报侧判定的「真漏记」（`VALID_UNRECORDED`）")
    lines.append("")
    if not vu:
        lines.append("本 pair 无。（全语料 X1 侧 13 条、主臂侧 2 条。）")
        lines.append("")
    else:
        lines.append(
            f"⭐ **本 pair {len(vu)} 条。** 这是「台账没记、但复核判定确实成立」的缺陷 —— "
            "⛔ 最高优先级。它们已经过一轮独立复核，事实部分通常可直接采信。"
        )
        lines.append("")
        for i, r in enumerate(vu, 1):
            key = f"VU-{pair}-{i:02d}"
            keys.append(key)
            lines.append(f"#### {key} · 簇 `{r.get('cluster')}`（{r.get('_arm')} 臂，"
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
            lines.append(fb.render(key, "candidate", fb.CANDIDATE_TEMPLATE, saved.get(key)))
            lines.append("")

    # ---- §3.2 审阅 agent 未采纳的 diff
    unadopted = S.unadopted_diffs(pair)
    adopted = S.adopted_diff_ids(pair)
    rv = S.review_json(pair)
    total_diffs = len(rv.get("diffs") or []) if rv else 0
    lines.append("### §3.2 审阅 agent 产出但未进台账的 diff")
    lines.append("")
    if rv is None:
        lines.append(f"⛔ 无 `{pair}-review.json`。")
        lines.append("")
    else:
        lines.append(
            f"本 pair 审阅 agent 共产出 **{total_diffs}** 条 diff，进台账 **{len(adopted)}** 条，"
            f"未进 **{len(unadopted)}** 条。"
        )
        lines.append("")
        lines.append(
            "⚠️ **已知证据缺口**：当年**没有单独记录「为什么不收」**，"
            "只留下了该 diff 被判成什么。所以下面「排除理由」一列给的是它的 `verdict` "
            "与判定者写的 `reason`，⛔ 不是一条真正的排除论证。"
        )
        lines.append("")
        priority = [(i, d) for i, d in unadopted
                    if d.get("verdict") in ("problem", "extra", "uncertain")]
        rest = [(i, d) for i, d in unadopted
                if d.get("verdict") not in ("problem", "extra", "uncertain")]
        if priority:
            lines.append(f"#### §3.2a 判为 problem / extra / uncertain 的 {len(priority)} 条（设裁决区）")
            lines.append("")
            for i, d in priority:
                key = f"DIFF-{pair}-{i:02d}"
                keys.append(key)
                lines.append(f"##### {key} · diff #{i} · `{d.get('verdict')}`")
                lines.append("")
                lines.append(_DIFF_VERDICT_NOTE.get(d.get("verdict"), ""))
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
                lines.append(fb.render(key, "candidate", fb.CANDIDATE_TEMPLATE, saved.get(key)))
                lines.append("")
        if rest:
            lines.append(f"#### §3.2b 判为 correct / similar 的 {len(rest)} 条（备查，不设裁决区）")
            lines.append("")
            lines.append(
                "⭐ 这些当年被判为「生成方在该点上正确 / 与参考等价」。"
                "列在这里是为了**自包含**：若你在 §4 发现某处确有问题，可以先查它是不是"
                "已经被人看过并判过没问题。要推翻的话，直接在 §5 登记新条目。"
            )
            lines.append("")
            lines.append("| # | 判定 | 参考侧 | 生成侧 | 理由（截断） |")
            lines.append("| --: | :-- | :-- | :-- | :-- |")
            for i, d in rest:
                lines.append(f"| {i} | `{d.get('verdict')}` | {clip(d.get('ref'), 60)} | "
                             f"{clip(d.get('gen'), 60)} | {clip(d.get('reason'), 140)} |")
            lines.append("")

    # ---- §3.3 机械未匹配
    um = S.unmatched_issues(pair)
    lines.append("### §3.3 两臂产出中机械未匹配任何台账条目的 issue")
    lines.append("")
    if um is None:
        lines.append(
            "⛔ **未导出。** 先跑 `python3 export_unmatched.py`（它读 `runs/` 下的原始 run "
            "record；⚠️ 主臂 v46 的记录在姊妹 clone `research_ideas/` 里）。"
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
            "⭐ **出现格数越多越值得看** —— 六格里出现五六次的主张，不太可能是单次采样噪声。"
        )
        lines.append("")
        if x1:
            lines.append(f"#### §3.3a X1 臂未认领 {len(x1)} 组")
            lines.append("")
            lines.append(
                "⭐ 这些**全部已有多报侧裁定**（已归入 X1 的多报桶并给了 verdict）。"
                "⛔ 那些裁定是**另一轮**判定者做的，你可以推翻 —— "
                "尤其 `NO_NL_BASIS`：它只说「NL 没有逐字依据」，"
                "⭐ 而合式性层的缺陷本来就不要求 NL 依据（台账自己有 30 条这样的记录）。"
            )
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
        if v46:
            shown = v46[:30]
            lines.append(f"#### §3.3b 主臂 v46 机械未匹配 {len(v46)} 组"
                         + (f"（列出出现格数最多的 {len(shown)} 组）"
                            if len(v46) > len(shown) else ""))
            lines.append("")
            lines.append(
                "⛔ **主臂的多报簇没有逐条回链到格**（`G*.jsonl` 只给 `cells_of_6` 计数、"
                "不给成员清单），所以这里**无法**标出哪些已被裁定 —— "
                "本 pair 的多报侧裁定另见 §3.4，需自行对照。"
                "⚠️ 全语料有 **102 条**主臂未匹配 issue 落在 6 个 pair"
                "（`0005` `0015` `0025` `0035` `0042` `0045`）上却**零多报簇**，"
                "即那 6 个 pair 的这一栏完全没有被裁定过。"
            )
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
        key = f"UM-{pair}"
        keys.append(key)
        lines.append("上表里值得补入台账的，在这里点名（写行内的 issue 文本或格数+关键词即可）：")
        lines.append("")
        lines.append(fb.render(key, "candidate", fb.CANDIDATE_TEMPLATE, saved.get(key)))
        lines.append("")

    # ---- §3.4 已裁定为非缺陷的多报簇
    other = S.other_unexpected(pair)
    lines.append("### §3.4 本 pair 已被判为「非缺陷」的多报簇（备查）")
    lines.append("")
    if not other:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append(
            f"共 {len(other)} 簇。⭐ 这些是两臂报过、但复核判为不成立的主张。"
            "⛔ 它们**不是**候选 —— 列出来是为了让你在 §4 发现同一形状时，"
            "能立刻看到「这条已经被判过，理由是这个」，避免重复劳动或与既有裁定冲突。"
        )
        lines.append("")
        lines.append("| 簇 | 臂 | 裁定 | 子类 | 事实 / 理由（截断） |")
        lines.append("| :-- | :-- | :-- | :-- | :-- |")
        for r in other:
            lines.append(
                f"| `{r.get('cluster')}` | {r.get('_arm')} | `{r.get('verdict')}` | "
                f"`{r.get('subclass') or '—'}` | "
                f"{clip((r.get('claim') or '') + ' ‖ ' + (r.get('fact') or ''), 200)} |")
        lines.append("")

    # ---- §3.5 同根但未归并
    la = S.ledger_accounted().get(pair) or []
    lines.append("### §3.5 与台账同根、但匹配器未归并的簇（⭐ 「台账偏浅」的直接证据）")
    lines.append("")
    if not la:
        lines.append("本 pair 无。")
        lines.append("")
    else:
        lines.append(
            f"共 {len(la)} 簇。⭐ 这类最能说明问题：**同一个缺陷**，两臂用了另一种谓词或"
            "另一种措辞表述，台账那一条就没能覆盖。"
            "⛔ 它们不算新增缺陷，但**它们说明台账那一条的 statement 写窄了** —— "
            "对应的台账条目适合走「修正」而不是「保留」。"
        )
        lines.append("")
        for r in la:
            lines.append(f"- **`{r.get('cluster')}`**（{r.get('_arm')}）：{esc(r.get('fact'))}")
            if r.get("note"):
                lines.append(f"  - {esc(r.get('note'))}")
        lines.append("")

    return "\n".join(lines), keys


# ------------------------------------------------------------------ §4 清单

def section_checklist(pair, model, segs, records, saved):
    lines = []
    keys = []
    lines.append("## §4 深度检查清单（⭐ 本节引导挖深）")
    lines.append("")
    lines.append(
        "⛔ 清单里的每一条都是**待核问句**，不是结论。机械判据写在每条下方，"
        "判错了就直接在「发现」里写「机械判错，理由 X」。"
        "⭐ 勾选 `[x]` 表示**已看过**；「发现:」留空表示看过但无发现。"
    )
    lines.append("")
    lines.append(
        "⛔ **不在范围内的，一律不许记**：时钟 / 计时 / 秒级约束、不变式、正交区并发"
        "（fork/join、区域同时活跃）。project_1 的建模对象是 $M = (S, E, V, Tr, A)$，"
        "没有 $C$、没有 $Inv$、没有区分量。"
    )
    lines.append("")

    cats = checklist.build(model, segs, records, pair)
    if not cats:
        lines.append("⚠️ 机械分析没有产出任何线索 —— 该模型结构非常简单，"
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


def section_new(pair, saved):
    lines = []
    lines.append("## §5 新增 issue 登记")
    lines.append("")
    lines.append(
        "把 §3 采纳的、§4 查出的、以及你自行发现的缺陷登记在这里。"
        "⭐ 登记区默认给两条，不够就照格式往下加（`NEW-" + pair + "-03`、`-04` …，编号连续即可）。"
    )
    lines.append("")
    lines.append(
        "⛔ 登记前先过三道门：① 它在 $M = (S, E, V, Tr, A)$ 内吗（⛔ 无时钟 / 无并发）？"
        "② 它在**作者源**上成立吗（⛔ 不能只在投影上成立）？"
        "③ 它和 §2 已有条目是同一个缺陷吗（是则回 §2 走「修正」，⛔ 不要在这里新开一条）？"
    )
    lines.append("")
    lines.append(
        "⚠️ 下面所有样例都取自现有台账 "
        "[expected_issue_set.json](../expected_issue_set.json) 的**真实条目**，⛔ 一条都没有编。"
        "⭐ 但样例会**避开本 pair 所属的 NL 组**（本 pair 属 `"
        + str(S.nl_group(pair)) + "`）—— 同一份 NL 生成 6 个制品，"
        "拿兄弟 pair 的缺陷当格式样例等于把答案先告诉你。"
    )
    lines.append("")

    # ---------------------------------------------------------- §5.1 字段表
    lines.append("### §5.1 字段表（⭐ 你只填第一层）")
    lines.append("")
    lines.append("| 层 | 字段 | 一句话 | 留空的含义 |")
    lines.append("| :-- | :-- | :-- | :-- |")
    lines.append("| ⭐ 必填 | `statement` | 缺陷是什么 | ⛔ 不许留空 |")
    lines.append("| ⭐ 必填 | `generated_side` | 模型里哪一处（行号或元素名） | ⛔ 不许留空 |")
    lines.append("| ⭐ 必填 | `nl_evidence` | NL 段 id；NL 未明说就写 `无` | "
                 "⛔ 不许留空（⭐ 写 `无` 才算判过） |")
    lines.append("| ⭐ 必填 | `direction` | 8 类之一 | ⛔ 不许留空，归不进就选 `unclassified` |")
    lines.append("| ⭐ 必填 | `depth` | 表层 / 中层 / 深层 | ⛔ 不许留空 |")
    lines.append("| ⚠️ 可选 | `reference_side` | 参考模型对应处 | ⭐ 留空 = 没看 / 参考侧无对应 |")
    lines.append("| ⚠️ 可选 | `primary_predicate` | 19 谓词之一 | "
                 "⭐ 留空 = 未判；写 `无` = 判过了、词表覆盖不到 |")
    lines.append("| ⚠️ 可选 | `layer` | 4 层之一 | ⭐ 留空 = 未判 |")
    lines.append("| ⭐ 脚本推导 | `id` `pair` `group` `llm` `in_scope` `element_of_M` "
                 "`expressible_with_closed_vocabulary` `layer_basis` `upstream` | "
                 "由 [newfields.py](./newfields.py) 的 `derive()` 算出 | ⛔ **一律不填** |")
    lines.append("| ⭐ 合并时补 | `assertions` `assertion_count` `has_negative_control` "
                 "`replay` `verdict` `homogeneity_*` `automatable` `decided_by` | "
                 "要跑断言器 / 要全库重算，本目录做不了 | ⛔ **一律不填** |")
    lines.append("")
    lines.append(
        "⛔ **为什么不让你填 `element_of_M`**：它只是对 `generated_side` 已经点到的那一处做分类，"
        "不带新信息。台账里同一个 `direction` 会落到 3 到 5 种不同的 `element_of_M`"
        "（`guard` 方向就横跨 `Tr` / `A` / `S` / `E` / `V` 五种），手填只会引入噪声。"
        "⭐ `derive()` 改从你给的**作者源行号**反查那一行是状态声明、迁移还是状态动作 —— 那是确定性的。"
        "⭐ 所以 `generated_side` 里**带上行号**比写元素名更有用。"
    )
    lines.append("")

    # ---------------------------------------------------------- §5.2 逐字段
    lines.append("### §5.2 逐字段怎么填")
    lines.append("")

    got = _ex("statement", pair, "statement", 320)
    lines.append("#### `statement` ⭐ 必填")
    lines.append("")
    lines.append(
        "⭐ 写**缺陷是什么**，不是写「哪里不一样」。判据：读完这一句，"
        "另一个人能不能独立到作者源上复核它成立与否。"
        "⭐ 现有条目的写法是审阅 agent 的 `reason` 逐字，可以照那个密度写。"
    )
    lines.append("")
    if got:
        rec, val = got
        lines.append(f"真实样例（`{rec['id']}`，`{rec['direction']}` / `{rec['layer']}`）：")
        lines.append("")
        lines.append(f"> {val}")
        lines.append("")
    lines.append(
        "⚠️ **写成一段，⛔ 不要换行**。回收器只把 `" + "` / `".join(NF.FIELD_NAMES)
        + "` 这几个名字当作新字段起点，其余行都会并进当前字段 —— "
        "⭐ 所以你可以在 `statement` 里放冒号、放引文，⛔ 但请别自己起一个像字段名的行。"
    )
    lines.append("")

    got = _ex("generated_side", pair, "generated_side", 200)
    lines.append("#### `generated_side` ⭐ 必填")
    lines.append("")
    lines.append(
        "⭐ 指到**作者源 PlantUML 的具体一处**：优先写 §1.3 的行号（写 `:12` 或 `第 12 行`），"
        "再附上那一行的元素名或原文片段。⭐ 缺失类缺陷写「（无此边）」这类否定描述也算合法 —— "
        "台账里就有。"
    )
    lines.append("")
    if got:
        rec, val = got
        lines.append(f"真实样例（`{rec['id']}`）：`{val}`")
        lines.append("")
    lines.append(
        "⛔ 带行号才能让 `derive()` 推出 `element_of_M`；只写元素名时，"
        "只有你同时填了结构族 `primary_predicate` 才推得出来。"
    )
    lines.append("")

    lines.append("#### `nl_evidence` ⭐ 必填（⭐ 但「写 `无`」是合法答案）")
    lines.append("")
    empty_n, total_n = NF.nl_evidence_empty_count()
    lines.append(
        "⭐ 写本 pair §1.2 表里的**段 id**（如 `" + segs_hint(pair) + "`），多个用逗号分隔，"
        "后面可以再跟一句逐字引文。"
    )
    lines.append("")
    lines.append(
        "⛔⛔ **写 `无` 是有意义的答案，⛔ 不是偷懒** —— 它表示「NL 未明说，本条属模型内生问题」。"
        f"现台账 **{empty_n} / {total_n}** 条正是这种情况（合式性层按定义就不要求 NL 依据）。"
        "⛔ 但**留空**不等于 `无`：留空会被校验判成没填。"
    )
    lines.append("")
    got = _ex("nl_evidence", pair, "nl_evidence", 200)
    if got:
        rec, val = got
        lines.append(f"真实样例（`{rec['id']}`，有 NL 依据）：{val}")
        lines.append("")
    got = _ex("nl_evidence_empty", pair, None)
    if got:
        rec, _ = got
        lines.append(
            f"真实样例（`{rec['id']}`，`layer = {rec['layer']}`，`nl_evidence` 为空）："
            f"{clip(rec['statement'], 160)}"
        )
        lines.append("")

    lines.append("#### `direction` ⭐ 必填")
    lines.append("")
    dc = NF.direction_counts()
    lines.append(
        "⭐ 取值就是台账 98 条 `REPORTABLE` 实际用过的 8 类，⛔ 不要造新取值。"
        "括号里是台账现有条目数 —— ⭐ **数字越小的方向越可能是台账的盲区，越值得看**。"
    )
    lines.append("")
    lines.append("| 取值 | 台账条数 | 指什么 |")
    lines.append("| :-- | --: | :-- |")
    for d, what in DIRECTION_MEANING:
        lines.append(f"| `{d}` | {dc.get(d, 0)} | {what} |")
    lines.append("")
    lines.append(
        "⚠️ 全 126 条台账里还有第 9 个取值 `pseudostate`（9 条），"
        "但它**全部落在 `00x8` 越界 pair** 上 —— 那 6 个 pair 的 fork/join 伪状态不在 $M$ 内，"
        "⛔ 故本轮不设该取值。"
    )
    lines.append("")

    lines.append("#### `depth` ⭐ 必填")
    lines.append("")
    lines.append(
        "⭐ 判据是**读懂它需要看几个地方**：一处 = 表层，两处之间的关系 = 中层，"
        "需要沿执行路径推理或跨多个状态比对 = 深层。"
    )
    lines.append("")
    lines.append("| 档 | 判据 | 示意（⛔ 非台账原文） |")
    lines.append("| :-- | :-- | :-- |")
    lines.append("| 表层 | 单点存在性 / 拼写 | 「`FinishState` 没有 `state` 声明」 |")
    lines.append("| 中层 | 单点关系 | 「`InMotion` 有三个子态但没有区域初始边」 |")
    lines.append("| 深层 | 跨状态推理 / 隐含冲突 / 运行时后果 | "
                 "「接管迁移只挂在一个子态上，自动模式其余每一处都把接管信号静默丢弃」 |")
    lines.append("")
    lines.append(
        "⛔ **台账没有 `depth` 字段** —— 它是本轮新引入的，所以上面三行是判据示意，⛔ 不是台账原文。"
        "⭐ §2 每条下方的「⚠️ 深度存疑」只看断言形状（单存在性谓词 + 无佐证断言）机械提示，"
        "⛔ 同样不是裁决。"
    )
    lines.append("")

    lines.append("#### `reference_side` ⚠️ 可选")
    lines.append("")
    lines.append(
        "⭐ 参考模型（§1.4）里对应的那一处。⛔ **参考模型不是正确答案** —— "
        "语料里多处出现参考侧比生成侧更差的情形，填它只是为了让后续复核有个对照。"
        "⭐ 留空完全可以。"
    )
    lines.append("")
    got = _ex("reference_side", pair, "reference_side", 200)
    if got:
        rec, val = got
        lines.append(f"真实样例（`{rec['id']}`）：{val}")
        lines.append("")

    lines.append("#### `primary_predicate` ⚠️ 可选（⭐ 写 `无` 本身就是发现）")
    lines.append("")
    npp, total_n = NF.no_primary_predicate_count()
    lines.append(
        "⭐ 19 个封闭谓词里选一个能承载这条主张的。⛔⛔ **选不出来时写 `无`** —— "
        "那说明**现有词表覆盖不到这个缺陷**，⭐ 而那正是方法重构（M1）要吸收的输入，"
        f"⛔ 不是不登记的理由。现台账已有 **{npp} / {total_n}** 条没有 primary 谓词。"
        "⭐ 写 `无` 时请在 `statement` 末尾补一句缺口在哪。"
    )
    lines.append("")
    for fam, preds in S.PREDICATES.items():
        lines.append(f"- **{fam} 族**：" + "、".join(f"`{p}`" for p in preds))
    lines.append("")
    lines.append(
        "⚠️ 已知谓词缺口（选谓词时留意）："
        "`guard_distinguishable` 在单目标时空真返回 `True`；"
        "`initial_target` 看不到**带触发**的初始边；"
        "`variable_declared` 对投影的 `R45RouteToken` 按设计返回 `False`；"
        "「无事件、以 in-state 为守卫」的迁移形状**没有承载谓词**。"
    )
    lines.append("")

    lines.append("#### `layer` ⚠️ 可选")
    lines.append("")
    lc = NF.layer_counts()
    lines.append("| 取值 | 台账条数 | 判据（⭐ 台账 `layer_basis` 原话） |")
    lines.append("| :-- | --: | :-- |")
    for lay, basis in NF.layer_basis_table().items():
        lines.append(f"| `{lay}` | {lc.get(lay, 0)} | {esc(basis)} |")
    lines.append("")
    lines.append(
        "⛔ 若你勾了 `wellformedness` 之外的任何一层，`nl_evidence` 就**不能**是 `无` —— "
        "那三层按定义都要求 NL 逐字依据。[validate.py](./validate.py) 会把这种组合报成 `E`。"
    )
    lines.append("")

    # ---------------------------------------------------------- §5.3 登记区
    lines.append("### §5.3 登记区")
    lines.append("")
    lines.append(
        "⭐ 直接在下面的块里填。⛔ 只有 `FILL:BEGIN` / `FILL:END` 之间的内容会被 "
        "[collect.py](./collect.py) 收走，块外写的东西重跑生成器就没了。"
    )
    lines.append("")
    key = f"NEW-{pair}"
    kept = saved.get(key)
    if fb.is_stale_template(kept, "new", pair):
        # ⭐ 旧版空模板 —— 换成当前字段表。⛔ 只在**逐字全等**时才换，
        # 作者已经填过的旧模板照原样留住。
        kept = None
    lines.append(fb.render(key, "new", fb.new_template(pair), kept))
    lines.append("")
    return "\n".join(lines)


DIRECTION_MEANING = [
    ("hierarchy", "层次归属：谁该是谁的子态、复合括号有没有打开"),
    ("reachability", "可达性与终止：进得去 / 出得来 / 停得下"),
    ("entry", "入口：初始边、初始目标、进入某状态时落到哪"),
    ("guard", "守卫：条件写没写、写对没写对、能不能区分多条出边"),
    ("effect_action", "效应与状态动作：entry / exit / 迁移效应"),
    ("event", "事件：触发词缺失、拼错、被并成一个复合名"),
    ("cardinality", "基数：NL 点名了 N 个而模型给了 M 个"),
    ("unclassified", "以上都归不进（⭐ 归不进本身值得在 statement 里说明）"),
]


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
        "⛔ 本文件由 [generate.py](./generate.py) 生成，**只有 `FILL:BEGIN`/`FILL:END` "
        "之间的内容是给人填的**。其余部分重跑生成器会被覆盖；填写内容会按 key 保留。"
        "回收用 [collect.py](./collect.py)，校验用 [validate.py](./validate.py)，"
        "口径见 [README.md](./README.md)。"
    )
    head.append("")

    pair_key = f"PAIR-{pair}"
    keys.append(pair_key)
    head.append("## §0 本 pair 结论（做完再填）")
    head.append("")
    head.append(fb.render(pair_key, "pair", fb.PAIR_TEMPLATE, saved.get(pair_key)))
    head.append("")

    body = [section_material(pair, model, records)]

    s2, k2 = section_ledger(pair, records, saved)
    body.append(s2)
    keys += k2

    s3, k3 = section_candidates(pair, model, records, saved)
    body.append(s3)
    keys += k3

    s4, k4 = section_checklist(pair, model, segs, records, saved)
    body.append(s4)
    keys += k4

    body.append(section_new(pair, saved))
    keys.append(f"NEW-{pair}")

    doc = "\n".join(head) + "\n" + "\n".join(body)

    # 孤儿填写区：旧文件里有、新骨架里没有的 key
    orphans = {k: v for k, v in saved.items() if k not in set(keys)}
    if orphans:
        tail = ["## §9 孤儿填写区（⚠️ 材料变动导致这些 key 不再出现在正文）", ""]
        tail.append(
            "⛔ 这里的内容**不会丢**，但也不会被 `collect.py` 当作正文裁决计入。"
            "请把它们并回对应的新条目后删掉。"
        )
        tail.append("")
        for k, v in sorted(orphans.items()):
            tail.append(fb.render(k, "orphan", v))
            tail.append("")
        doc += "\n" + "\n".join(tail)

    return doc, keys


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
    for pair in pairs:
        if pair in S.OUT_OF_SCOPE_PAIRS:
            print(f"⛔ 跳过 {pair}：`00x8` 越界 pair，不在评测网格内")
            continue
        path = os.path.join(args.out, f"{pair}.md")
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
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(doc)

    print(json.dumps({
        "schema": SCHEMA,
        "generated_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "pairs": len(pairs),
        "written" if not args.check else "would_write": len(changed),
        "unchanged": len(unchanged),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
