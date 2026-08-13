"""`pyfcstm inspect` 诊断：装载、**按根因归一化**、到新座标系的映射。

真源是同目录的 [inspect_findings.json](./inspect_findings.json)，工作单 §3.6 从它渲染。

这一族与 §3.1–§3.5 的候选**不是同一个物种**
----------------------------------------------
§3.1–§3.5 的线索全部出自 **LLM 产出**（两臂的 issue、审阅 agent 的 diff、多报簇），
所以它们带采样噪声，同一个格重跑一次可能就没了。本节的 454 条出自
`pyfcstm inspect --format json --enable-verify` —— **确定性检查**，不采样、不过 LLM，
同一份 `model.fcstm` 永远给同一批诊断。⛔ 呈现时必须让判读者看出这个差别：
「模型没提」对前者是采样问题，对后者说明的是**检查器本身看不到那类东西**。

⚠️ 但**确定性不等于正确**：`model.fcstm` 是从作者源 PlantUML **投影**来的，
投影会合成元素（root 复合态、`UnspecifiedInitial` 之类）。故每条诊断都经过
「内生 / 投影产物 / 不确定」分拣加一轮对抗性复核，结论落在 `verdict` 上。

归并与去重**不在本文件里算** —— 见下面「归并与去重：人判，不算」那一节
--------------------------------------------------------------
⭐ **454 条诊断作为 inspect 输出是正常的，作为待裁决的 issue 条目不合理。**
`0007` 一个 pair 就有 34 条确认内生，判读者要对同一件事按 14 次。所以必须先按根因归一化、
再与台账 / 候选比对去重 —— ⛔ 但这两步都是**判断**，不是脚本能算的，理由与形态见下。

⚠️ 复核方自己已经撞到归并这件事：它在 `0000` 上标注 `W_DEADLOCK_LEAF` 与
`W_TOPOLOGICAL_NOEXIT`（`counterexample_kind = deadlock`）是「同一作者缺陷的两个诊断码」，
并明写「下游若做能力统计应注意二者非独立证据」。⭐ 那是一条**判断**，不是一条规则。

代码 → 座标的映射
-----------------
见 `CODE_MAP`。每一档都写了**为什么是这一格**；`other` 一档按类型学 §3.7.1
一律带说明（`other_note`）。
"""

from __future__ import annotations

import functools
import json
import os
import re
from collections import defaultdict

import newfields as NF

HERE = os.path.dirname(os.path.abspath(__file__))
FINDINGS_FILE = os.path.join(HERE, "inspect_findings.json")

SCHEMA = "paper1.relabel.inspect_findings.v1"

#: 判定桶。⛔ 只有前两个进工作单：`projection_artifact` 与 `refuted` 已被查明不是
#: 作者制品的问题，印出来只会稀释判读者的注意力（两者的条数仍在 §3.6 导语里报）。
SHOWN_VERDICTS = ("intrinsic", "uncertain")

#: ⛔ 整类排除、**不进 §3.6 主体**的两个 code。理由不是嫌多，是**内生率为 0**：
#: 反应式控制器本来就该有非平凡 SCC、本来就不该终止，这两条对本语料不构成缺陷主张。
#: ⚠️ 但它们里落在 `uncertain` 的那些仍出现在折叠区 —— 整类排除说的是「不当主张看」，
#: ⛔ 不是「从材料里删掉」。
EXCLUDED_CLASSES = ("I_NONTRIVIAL_SCC", "I_TOPOLOGICAL_NON_TERMINATING")

#: ⚠️⚠️ **本码有系统性假阳性风险，必须原样呈现给判读者。**
#: 复核时读了 pyfcstm 的 `analyzers/structural.py:75-93`：它**完全不做外层检查**，
#: 只数叶态自身的出边。于是对**嵌在复合态里、而外层有成组迁移**的叶态，本码是假阳性
#: —— 那条外层边对该叶态同样可用，它不是终止态。顶层态不受影响（没有外层可言）。
#: ⛔ 判读者不知道这一点就没法正确裁决这一族。
DEADLOCK_LEAF_CAVEAT = (
    "该码有**系统性假阳性**：pyfcstm 的 `analyzers/structural.py:75-93` 只数叶态自身的"
    "出边，**完全不做外层检查**。所以对**嵌在复合态里、而外层复合态有成组迁移**的叶态，"
    "本码报的「无出边」是假阳性 —— 那条外层边对该叶态同样可用，它不是终止态"
    "（顶层态没有外层，不受影响）。这也正是类型学 §3.5 `unintended_terminal` "
    "判定测试里写的那类最常见假阳性。裁决前请先数一遍该叶态各级祖先的出边。"
)


def _axes(locus, element=None, qualifier=None, logic_kind=None,
          reference=None, other_note=None, why=""):
    return {"defect_locus": locus, "defect_element": element,
            "defect_qualifier": qualifier, "defect_logic_kind": logic_kind,
            "defect_reference": reference, "other_note": other_note, "why": why}


#: 每个 inspect code 到新座标系的一格。⛔ `why` 不许省 —— 它是判读者判断
#: 「我们这一格判对了没有」的唯一依据，而映射本身是我方推断。
CODE_MAP = {
    "W_UNREACHABLE_STATE": _axes(
        "global", logic_kind="unreachable", reference="language",
        why="判定测试逐字对上：「从初始态出发的图遍历到不了它」。不引用 NL 任何一句即可判定，"
            "且工具规约侧有成文条款（itemis CREATE `vertex.MustBeReachable`「Node is not reachable.」），"
            "故参照物取 `language`。"),
    "W_DEADLOCK_LEAF": _axes(
        "global", logic_kind="unintended_terminal", reference="requirement",
        why="锚在 Baier & Katoen Definition 2.4 的 terminal state 上。"
            "「是不是**有意**的终态」要回 NL 判（SDMetrics `NoOutgoing` 逐字："
            "「Check if this is merely an oversight or the actually intended behavior.」），"
            "故参照物取 `requirement`。"),
    "W_TOPOLOGICAL_NOEXIT@deadlock": _axes(
        "global", logic_kind="unintended_terminal", reference="requirement",
        why="`counterexample_kind = deadlock` 说的就是「有一个态出不去」，"
            "与 `W_DEADLOCK_LEAF` 是同一件事的第二个观察角度，故落同一格。"),
    "W_TOPOLOGICAL_NOEXIT@trap_cycle": _axes(
        "global", logic_kind="nontermination", reference="requirement",
        why="`counterexample_kind = trap_cycle` 说的是「有一圈执行永远出不去」。"
            "⚠️ 类型学 §3.5 明写本档**只能挂在 NL 的终止义务上** —— 活锁没有与标注无关的"
            "形式定义，所以这一条要成立，必须先在 NL 里找到「终会到达某终止条件」那句话。"),
    "I_TOPOLOGICAL_NON_TERMINATING": _axes(
        "global", logic_kind="nontermination", reference="requirement",
        why="同上：拓扑上不强制到达终止态。⛔ 本类内生率 0/52，见 `EXCLUDED_CLASSES`。"),
    "I_NONTRIVIAL_SCC": _axes(
        "global", logic_kind="other", reference="other",
        other_note="拓扑上存在非平凡强连通分量。座标系没有对应取值，因为它**在反应式控制器里"
                   "是常态而不是缺陷**（本类内生率 0/54）；参照物同样落 `other` —— "
                   "既没有禁止环的建模语言条款，NL 侧也没有对应义务，判定只能靠人裁。",
        why="两处 `other` 都不是兜底，是如实标注：这条诊断在本座标系里没有正当取值。"),
    "W_INITIAL_UNCONDITIONAL_MISSING": _axes(
        "element", element="transition", qualifier="missing", reference="language",
        why="缺的是一条**无条件默认入口边**（`[*] -->`），构件是边本身、编辑是新增一条，"
            "故 element + transition + missing。UML 2.5.1 明写初始伪状态的出边不得带 trigger / guard，"
            "itemis CREATE 亦有 `region.MustNotHaveMultipleDefaultEntries` 一族成文条款，"
            "不引用 NL 即可判定，故参照物取 `language`。"),
    "W_EVENT_UNREACHABLE_EMIT": _axes(
        "global", logic_kind="unreachable", reference="language",
        why="事件本身不是图上的节点，但它的**全部消费源状态都不可达** —— "
            "即消费该事件的那些迁移永远不可能触发（itemis CREATE 的 "
            "`Dead transition. This transition can not be taken…` 是同一族的成文条款）。"
            "落点与 `W_UNREACHABLE_STATE` 同格，主体换成事件。"),
    "I_TRANSITION_TO_SELF_VIA_PARENT": _axes(
        "pair", logic_kind="hierarchy_entry", reference="requirement",
        why="判定测试逐字对上：迁移的目标是**复合态本身**而非某个子态，于是每次进入都会"
            "重跑内部初始、把内部阶段重置。「这是不是想要的」要回 NL 判，故取 `requirement`。"),
    "I_TRANSITION_NEVER_EVENT_TRIGGERED": _axes(
        "element", element="trigger", qualifier="missing", reference="requirement",
        why="那条边上既没有事件也没有守卫。缺的是标签上 `/` 之前、方括号之外的**事件名**，"
            "改对是给它补一个触发词（条数变多），故 element + trigger + missing。"
            "⚠️ 参照物取 `requirement` 而不是 `language`：UML 允许无触发的完成迁移，"
            "「这条边该不该有触发词」只能回 NL 判。"),
    "W_REDUNDANT_TRANSITION": _axes(
        "element", element="transition", qualifier="extraneous", reference="language",
        why="同源同目标同标签的边被声明了两次以上，改对是删掉重复的那几行（条数变少）。"
            "重复声明不需要引用 NL 即可判定，故取 `language`。"),
    "W_DEAD_NAMED_ACTION": _axes(
        "element", element="effect", qualifier="extraneous", reference="language",
        why="声明了一个具名动作却从没有任何地方引用它。动作属维度 A 的 `effect` 一档"
            "（状态体内的 entry / exit / do 与边上 `/` 之后的内容），改对是删掉该声明。"),
}


class FindingsError(RuntimeError):
    """诊断数据与代码 / 座标系对不上。⛔ 一律抛，不静默跳过。"""


@functools.lru_cache(maxsize=None)
def load():
    with open(FINDINGS_FILE, encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("schema") != SCHEMA:
        raise FindingsError(f"schema 不对：{data.get('schema')}")
    return data


def all_findings():
    return load()["findings"]


def axes_for(rec):
    """一条诊断的座标。⛔ 找不到就抛 —— 新 code 静默落空格等于整类丢失。"""
    key = rec["code"]
    if key == "W_TOPOLOGICAL_NOEXIT":
        kind = (rec.get("refs") or {}).get("counterexample_kind")
        key = f"W_TOPOLOGICAL_NOEXIT@{kind}"
    if key not in CODE_MAP:
        raise FindingsError(f"inspect code `{key}` 没有座标映射 —— 补 `CODE_MAP`，不要留空格")
    return CODE_MAP[key]


# ---------------------------------------------------------------- 归并与去重：人判，不算
#
# ⛔⛔ **本文件不做归并，也不做跨源去重。** 两者都是判断，⛔ 不许用脚本算：
#
# - 判「这 13 条 `W_UNREACHABLE_STATE` 是不是同一条错入边导致的」要理解**因果**；
# - 判「这条与 `EIS-0007-02` 是不是同一个问题」要比较两段描述的**语义**。
#
# 把这类判断做成模式匹配，正是 [CLAUDE.md](../../../../../CLAUDE.md) §11 划死的那条边界。
# ⚠️ 本仓库为此栽过一次：`named_elements` 的 validator 把语义判断（句子点名了几个要素）
# 实现成词法判断（字符串里有没有逗号），190 行被拒且绝大多数是误伤，对某个 pair 系统性
# 致命 —— 18/18 撞死、5 格耗尽、约 16 万 output token 白烧。
#
# ⛔ **2026-08-13 撤掉过一版自动实现**，原样存档在 `/tmp/g1trans/removed_automation.py`，
# ⚠️ 它当时确实在**决定**归并与判重结果，两处都越了线：
#   ① `normalize()` —— 按「主体元素路径 + 父态包含闭包 + 事件消费源 + counterexample_kind」
#      做并查集自动归组。虽然吃的是结构化 `refs` 而不是散文，⛔ 但「同一元素名就合并」
#      正是禁止项字面点名的那一条。
#   ② `match_one()` + `NATURE_WORDS` —— 拿一张中文关键词表（「不可达」「死端」「初始」…）
#      去扫台账 `statement` 判重合。⛔ 这就是词法冒充语义，与上面那次事故同型。
#
# ⭐ 正确形态照 [ledger_mapping.py](./ledger_mapping.py) 办：**判断产出数据文件，
# 脚本只负责装载校验、渲染与对拍。** 判断落在两份待产出的文件里：
#
# | 文件 | 谁产出 | 每条要有 |
# | :-- | :-- | :-- |
# | `inspect_issues.json` | 逐 pair 读诊断集合 + 作者源 PlantUML 的判定者 | 归一化后的 `statement`（说清根因是什么）· 底层 `diag_index` 列表 · **合并理由**（为什么判为同根因，要能指着制品说）· 未合并的说明 |
# | `inspect_overlap.json` | 拿归一化结果读台账 / 候选原文的判定者 | `overlap`：`ledger:EIS-xxxx-xx` / `candidate:DIFF-xxxx-xx` / `none` · **判断依据**（引双方原文的对应处） |
#
# 装载期机械门（照 `ledger_mapping.py` 的形态，⛔ 对不上就抛）：字段合法 ·
# `diag_index` 全部存在且**不重复分配** · 引用的原文片段是逐字子串 · 合并理由非空。
# ⭐ 这些门是**防伪造**的机械手段，⛔ 不是替判定者做判断。
#
# 两条代价不对称的口径，⛔ 判定者必须照办：
# - **归并**：拿不准就不合（错合会让判读者永远看不到其中一个问题）。
# - **去重**：拿不准就判 `none` 新建 `INS-` 块，并在 note 写「疑似与 `EIS-xxxx-xx` 重合，
#   请判读者确认」（错判重合会把真发现藏进既有条目）。

ISSUES_FILE = os.path.join(HERE, "inspect_issues.json")
OVERLAP_FILE = os.path.join(HERE, "inspect_overlap.json")


def has_judged_issues():
    """判定者产出的归一化结果在不在。⛔ 不在就**什么都不渲染**。

    ⛔ 不许退化成「那就按脚本分组先渲染着」—— 那正是被撤掉的那版做的事。
    ⚠️ 也不许退化成「那就把 454 条原样摆出来」：`0007` 会出现 34 个填写块，
    判读者要对同一件事按 14 次。
    """
    return os.path.exists(ISSUES_FILE)


def judged_issues(pair, verdict="intrinsic"):
    """读判定者产出的归一化 issue。⛔ 文件不在就返回空表，⛔ 不自己算。"""
    if not has_judged_issues():
        return []
    with open(ISSUES_FILE, encoding="utf-8") as fh:
        rows = json.load(fh).get("issues") or []
    index = {(r["pair"], r["diag_index"]): r for r in all_findings()}
    out = []
    for row in rows:
        if row.get("pair") != pair or row.get("verdict") != verdict:
            continue
        members = [index[(pair, i)] for i in row["diag_index"]]
        out.append(dict(row, members=members))
    return out


# ---------------------------------------------------------------- 统计

def stats():
    """⛔ 只统计**算得出来**的东西：诊断条数与分拣结论分布。

    ⛔ 归一化后的 issue 条数、与既有条目的重合数**不在这里** —— 它们要等判定者产出
    `inspect_issues.json` / `inspect_overlap.json`，⛔ 脚本算不出来。
    """
    findings = all_findings()
    by_verdict = defaultdict(int)
    by_code = defaultdict(int)
    for r in findings:
        by_verdict[r["verdict"]] += 1
        by_code[r["code"]] += 1
    return {
        "diagnostics": len(findings),
        "by_verdict": dict(by_verdict),
        "by_code": dict(by_code),
        "pairs_with_findings": len({r["pair"] for r in findings}),
        "judged_issues_available": has_judged_issues(),
    }
