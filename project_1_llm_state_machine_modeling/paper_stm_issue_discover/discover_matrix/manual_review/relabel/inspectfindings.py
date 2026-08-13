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

#: ⚠️ **2026-08-13 更正**：本注释此前断言本码有「系统性假阳性」，⛔ **那半句是错的**，已删。
#: 前提（`analyzers/structural.py` 只数叶态自身出边、不做祖先遍历）为真；⛔ 但由它推出
#: 「因此会误报」为假 —— **FCSTM 里根本不存在可供子态使用的祖先边**。
#: `pyfcstm/verify/topology.py` 模块注释逐字：「Parent-level transitions **are followed only
#: when a descendant leaf explicitly exits to that parent; they are not copied onto every
#: active descendant leaf.**」即父态出边**不下传**，子态须自己显式 `-> [*]` 才接得上。
#: 两侧实测同向：语料侧 57 条真实诊断中「祖先有出边」的为 **0 条**；语义侧最小模型上
#: `W_DEADLOCK_LEAF` 与拓扑层的 `W_TOPOLOGICAL_NOEXIT`（`counterexample_kind=deadlock`）
#: **两套独立分析一致**。完整证据见 docs/findings/inspect_capability_boundary.md §一。
#:
#: ⭐ 但**祖先检查仍然要做**，只是它回答的是另一个问题，且结论落在另一个桶里：
#: 作者源读作 UML，UML 的成组迁移**成立**，故同一个叶态在 UML 下**不是** terminal。
#: 于是「IR 上为真、作者源上为假」—— ⭐ 这正是 `projection_artifact` 的定义
#: （见 docs/findings/representation_debt.md 的操作化判据），⛔ 不是「码报错了」。
DEADLOCK_LEAF_CAVEAT = (
    "本码在 FCSTM 上是**健全的**：FCSTM 的父态出边**不下传**给活动子态"
    "（`pyfcstm/verify/topology.py` 逐字：「Parent-level transitions are followed only when a "
    "descendant leaf explicitly exits to that parent; they are not copied onto every active "
    "descendant leaf.」），子态须自己显式 `-> [*]` 才接得上。故**不要**用「外层有出边」"
    "去推翻本码的诊断。但仍请做一次归属判定：作者源读作 UML，UML 的成组迁移**成立**，"
    "故若该叶态在 `stm0.puml` 里的某级祖先有出边，则它在作者源上并非终止态 —— 此时应判 "
    "`projection_artifact`（IR 上为真、作者源上为假），**而不是** `refuted`。"
    "本语料实测该情形为 0/57，故这一步大概率不改变结论，但仍须留痕。"
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
# 脚本只负责装载校验、渲染与对拍。** ⭐ 2026-08-13 判断已产出，落在**三份**文件里：
#
# | 文件 | 谁产出 | 每条要有 |
# | :-- | :-- | :-- |
# | [inspect_issues.json](./inspect_issues.json) | 逐 pair 读诊断集合 + 作者源 PlantUML 的判定者 | 归一化后的 `statement` · 底层 `diag_indices` · **合并理由**（为什么判为同根因，指着制品说）· 未合并说明 · 五轴座标 |
# | [inspect_overlap.json](./inspect_overlap.json) | 拿归一化结果读台账 / 候选原文的判定者 | `overlap_kind`：`ledger` / `candidate` / `suspect` / `none` · **判断依据**（引双方原文的对应处） |
# | [inspect_rulings.json](./inspect_rulings.json) | 对被挑战的座标出终局裁定的判定者 | `final_coord` · `final_evidence`（逐字引证）· `ruling_basis`（引类型学的判定测试与行号） |
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
RULINGS_FILE = os.path.join(HERE, "inspect_rulings.json")

ISSUES_SCHEMA = "paper1.relabel.inspect_issues.v1"
OVERLAP_SCHEMA = "paper1.relabel.inspect_overlap.v1"
RULINGS_SCHEMA = "paper1.relabel.inspect_rulings.v1"

#: issue id 的形态。⛔ 逐字钉住：`INS-<pair>-<两位序号>`，pair 必须与 id 里的四位一致。
RE_ISSUE_ID = re.compile(r"^INS-(\d{4})-(\d{2})$")

#: 判重结论的四个桶。⛔ 只有后两个新建填写块。
OVERLAP_KINDS = ("ledger", "candidate", "suspect", "none")

#: 新建填写块的两个桶。⭐ `ledger` / `candidate` 那些**并入既有条目**、不新建块 ——
#: ⛔ 判读者对同一个问题只裁决一次，重复摆一遍会让两处裁决可能互相矛盾。
NEW_BLOCK_KINDS = ("suspect", "none")

AXES = ["defect_locus", "defect_element", "defect_qualifier",
        "defect_logic_kind", "defect_reference"]


def _squash(text):
    return re.sub(r"\s+", "", text or "")


def coord_display(rec):
    """五轴 → 规范写法。⛔ 只有这一处算它，⛔ 不许在渲染器里另拼一份。

    ⚠️ 写法必须归一（`a / b + c / d`，`+` 与 `/` 两侧各一个空格）：上游三份判定产物里
    同一格出现过 `global + other`、`global / other · other`、`global／other（…）/ other`
    等十几种写法，⛔ 靠肉眼比对根本发现不了「这两条其实是同一格」。
    """
    if rec["defect_locus"] == ELEMENT_LOCUS:
        return (f"{rec['defect_locus']} / {rec['defect_element']} + "
                f"{rec['defect_qualifier']} / {rec['defect_reference']}")
    return (f"{rec['defect_locus']} / {rec['defect_logic_kind']} / "
            f"{rec['defect_reference']}")


ELEMENT_LOCUS = NF.ELEMENT_LOCUS


def _check_axes(rec, what):
    """条件式座标系的五轴校验。⛔ 与 `ledger_mapping._check_one` 是同一套判据。"""
    for axis in AXES:
        val = rec.get(axis)
        if val is not None and val not in NF.ENUMS[axis]:
            raise FindingsError(f"{what} 的 `{axis} = {val}` 不在枚举内")
    locus = rec.get("defect_locus")
    if not locus:
        raise FindingsError(f"{what} 没给 `defect_locus`")
    if not rec.get("defect_reference"):
        raise FindingsError(f"{what} 没给 `defect_reference`")
    for axis in NF.required_axes_for(locus):
        if not rec.get(axis):
            raise FindingsError(f"{what} 走 `{locus}` 支却没给 `{axis}`")
    for axis in NF.forbidden_axes_for(locus):
        if rec.get(axis):
            raise FindingsError(f"{what} 走 `{locus}` 支却给了 `{axis}`")
    # ⭐ 任一**该答的**轴取 `other` 必须附说明（类型学 §3.7.1）。⛔ 判据只看字段值，
    # ⛔ 与 [validate.py](./validate.py) 给判读者的那条门、与两个 mapping 装载器的门是同一条 ——
    # ⚠️ 三处口径不一致，等于我方可以留空出口而判读者不许。
    answered = ["defect_locus", "defect_reference"] + NF.required_axes_for(locus)
    picked = [a for a in answered if rec.get(a) == "other"]
    if picked and not (rec.get(NF.OTHER_NOTE_FIELD) or "").strip():
        raise FindingsError(
            f"{what} 的 " + "、".join(f"`{a}`" for a in picked)
            + f" 取了 `other`，却没写 `{NF.OTHER_NOTE_FIELD}` —— 出口不写清等于没分类")
    want = coord_display(rec)
    if rec.get("coord") != want:
        raise FindingsError(
            f"{what} 的 `coord = {rec.get('coord')!r}` 与五轴算出来的 {want!r} 不一致 —— "
            "座标写法必须归一，见 `coord_display`")


_ISSUES_CACHE = {}


def load_issues():
    """读并校验归一化 issue 表，返回整份 payload。⛔ 校验不过直接抛。

    装载期机械门（⛔ 全是**防伪造**手段，⛔ 一条都不替判定者做判断）：

    1. schema 对得上；id 形态合法、不重复、`pair` 与 id 里的四位一致、`group` 与该 pair 的
       工作单目录一致。
    2. `diag_indices` 非空、每个都在 `inspect_findings.json` 里存在，且**全局不重复分配** ——
       ⛔ 一条诊断落进两条 issue 等于把同一件事摆给判读者按两次。
    3. **覆盖完整**：`SHOWN_VERDICTS`（intrinsic + uncertain）的 336 条必须被恰好覆盖一次。
       ⛔ 少一条就是有诊断被静默丢掉，而工作单会照常渲染、看不出缺了什么。
    4. `verdict_class` 与成员诊断的 `verdict` 一致；⭐ 例外是 `recovered_from_refuted` 的条目 ——
       它们的成员是 `refuted`，`verdict_class` 是本轮恢复时判的，故另要求 `recovery_basis` 非空。
    5. 五轴合法 + 条件式一致 + `other` 带说明 + `coord` 与五轴算出来的规范写法逐字相等。
    6. `statement` / `merge_reason` / `puml_evidence` 非空，且 `puml_evidence` 里**至少有一段**
       反引号片段是该 pair 作者源的逐字子串（按去空白比对）。⚠️ 这一条对应
       `ledger_mapping` 的 `evidence` 子串门：改写过的「证据」看起来同样通顺，⛔ 但它证明不了
       判定者真的打开过作者源。
    """
    import sources as S
    if ISSUES_FILE in _ISSUES_CACHE:
        return _ISSUES_CACHE[ISSUES_FILE]
    if not os.path.exists(ISSUES_FILE):
        raise FindingsError(
            "缺 inspect_issues.json —— 工作单 §3.6 从它渲染。⛔ 没有它不许退化成"
            "「按脚本猜着分组」或「把 454 条原样摆出来」，见本文件「归并与去重：人判，不算」")
    with open(ISSUES_FILE, encoding="utf-8") as fh:
        payload = json.load(fh)
    if payload.get("schema") != ISSUES_SCHEMA:
        raise FindingsError(f"inspect_issues.json 的 schema 不对：{payload.get('schema')}")
    rows = payload.get("issues") or []
    index = {(r["pair"], r["diag_index"]): r for r in all_findings()}
    seen_ids, owner = set(), {}
    for rec in rows:
        iid = rec.get("issue_id")
        m = RE_ISSUE_ID.match(iid or "")
        if not m:
            raise FindingsError(f"issue id 形态不合法：{iid!r}")
        if iid in seen_ids:
            raise FindingsError(f"{iid} 出现了两次")
        seen_ids.add(iid)
        if m.group(1) != rec.get("pair"):
            raise FindingsError(f"{iid} 的 `pair = {rec.get('pair')}` 与 id 里的四位不一致")
        if rec["pair"] not in S.IN_SCOPE_PAIRS:
            raise FindingsError(f"{iid} 的 pair 不在 54 个在评 pair 内")
        if rec.get("group") != S.nl_dir(rec["pair"]):
            raise FindingsError(
                f"{iid} 的 `group = {rec.get('group')}` 与该 pair 的工作单目录 "
                f"{S.nl_dir(rec['pair'])} 不一致")
        diags = rec.get("diag_indices") or []
        if not diags:
            raise FindingsError(f"{iid} 没给 `diag_indices` —— 一条 issue 至少要有一条底层诊断")
        for d in diags:
            key = (rec["pair"], d)
            if key not in index:
                raise FindingsError(f"{iid} 引的诊断 {key} 在 inspect_findings.json 里不存在")
            if key in owner:
                raise FindingsError(
                    f"诊断 {key} 被 {owner[key]} 与 {iid} 同时认领 —— ⛔ 不许重复分配")
            owner[key] = iid
        verdicts = {index[(rec["pair"], d)]["verdict"] for d in diags}
        if rec.get("recovered_from_refuted"):
            if verdicts != {"refuted"}:
                raise FindingsError(f"{iid} 标了恢复，成员却不全是 refuted：{verdicts}")
            if not (rec.get("recovery_basis") or "").strip():
                raise FindingsError(f"{iid} 标了恢复却没写 `recovery_basis`")
            if rec.get("verdict_class") not in SHOWN_VERDICTS:
                raise FindingsError(f"{iid} 恢复后的 `verdict_class` 必须是 {SHOWN_VERDICTS}")
        elif verdicts != {rec.get("verdict_class")}:
            raise FindingsError(
                f"{iid} 的 `verdict_class = {rec.get('verdict_class')}` 与成员诊断的 "
                f"{verdicts} 对不上")
        _check_axes(rec, iid)
        for field in ("statement", "merge_reason", "puml_evidence"):
            if not (rec.get(field) or "").strip():
                raise FindingsError(f"{iid} 的 `{field}` 是空的")
        src = _squash(S.puml_text(rec["pair"]))
        spans = [s for s in re.findall(r"`([^`]+)`", rec["puml_evidence"])
                 if len(_squash(s)) >= 8]
        if not any(_squash(s) in src for s in spans):
            raise FindingsError(
                f"{iid} 的 `puml_evidence` 里没有任何一段反引号片段是作者源的逐字子串 —— "
                "给不出逐字引证就是在猜")
    shown = {(r["pair"], r["diag_index"]) for r in all_findings()
             if r["verdict"] in SHOWN_VERDICTS}
    missing = sorted(shown - set(owner))
    if missing:
        raise FindingsError(
            f"{len(missing)} 条待呈现诊断没有归属：{missing[:5]}… ⛔ 每条都必须落进某条 issue")
    _ISSUES_CACHE[ISSUES_FILE] = payload
    return payload


_OVERLAP_CACHE = {}


def load_overlap():
    """读并校验判重表，返回 {issue_id: 判重记录}。

    机械门：schema 对得上 · 与 issue 表**一一对应**（不多不少）· `overlap_kind` 在四个桶内 ·
    `ledger` / `candidate` / `suspect` 必须给 `overlap_target` 且该 id **真的存在**
    （台账 99 条 / 候选 141 个键里查得到）· `none` 不许给 target · `basis` 非空。

    ⚠️ 「target 真的存在」这条门不是形式主义：判重结论是「并入那一条」，⛔ target 打错一个字
    就会让并入的证据渲染不出来，⛔ 而工作单照样生成、看不出少了什么。
    """
    import candidate_mapping as CM
    import ledger_mapping as LM
    if OVERLAP_FILE in _OVERLAP_CACHE:
        return _OVERLAP_CACHE[OVERLAP_FILE]
    if not os.path.exists(OVERLAP_FILE):
        raise FindingsError("缺 inspect_overlap.json —— 没有它就不知道哪些该并入、哪些该新建")
    with open(OVERLAP_FILE, encoding="utf-8") as fh:
        payload = json.load(fh)
    if payload.get("schema") != OVERLAP_SCHEMA:
        raise FindingsError(f"inspect_overlap.json 的 schema 不对：{payload.get('schema')}")
    rows = payload.get("decisions") or []
    issues = {r["issue_id"] for r in load_issues()["issues"]}
    ledger_ids = set(LM.load())
    cand_keys = set(CM.load())
    out = {}
    for rec in rows:
        iid = rec.get("issue_id")
        if iid not in issues:
            raise FindingsError(f"判重表里的 `{iid}` 不在 issue 表里")
        if iid in out:
            raise FindingsError(f"{iid} 在判重表里出现了两次")
        kind = rec.get("overlap_kind")
        if kind not in OVERLAP_KINDS:
            raise FindingsError(f"{iid} 的 `overlap_kind = {kind}` 不在 {OVERLAP_KINDS} 内")
        target = rec.get("overlap_target")
        if kind == "none":
            if target:
                raise FindingsError(f"{iid} 判了 `none` 却给了 target `{target}`")
        else:
            if not target:
                raise FindingsError(f"{iid} 判了 `{kind}` 却没给 `overlap_target`")
            known = ledger_ids if kind == "ledger" else cand_keys
            if kind == "suspect":
                known = ledger_ids | cand_keys
            if target not in known:
                raise FindingsError(
                    f"{iid} 的 target `{target}` 在{'台账' if kind == 'ledger' else '既有条目'}"
                    "里查不到 —— 打错一个字就会让并入的证据静默渲染不出来")
        if not (rec.get("basis") or "").strip():
            raise FindingsError(f"{iid} 没写判重依据 —— 给不出双方原文的对应处就是在猜")
        out[iid] = rec
    missing = sorted(issues - set(out))
    if missing:
        raise FindingsError(f"{len(missing)} 条 issue 没有判重结论：{missing[:5]}…")
    _OVERLAP_CACHE[OVERLAP_FILE] = out
    return out


_RULINGS_CACHE = {}


def load_rulings():
    """读并校验终局裁定表，返回 {issue_id: [裁定…]}。

    机械门：schema 对得上 · `issue_id` 在 issue 表里 · 五轴合法 · `final_coord` 与五轴一致 ·
    `final_evidence` / `ruling_basis` 非空 · **裁定的五轴与该 issue 的五轴逐轴相等**。

    ⚠️ 最后一条是把两份文件钉在一起：`inspect_issues.json` 里凡 `coord_source = ruling` 的，
    ⛔ 座标就必须是这里定的那一格，⛔ 不许两份文件各说一套。
    """
    if RULINGS_FILE in _RULINGS_CACHE:
        return _RULINGS_CACHE[RULINGS_FILE]
    if not os.path.exists(RULINGS_FILE):
        raise FindingsError("缺 inspect_rulings.json —— 43 条座标改判的依据在它里面")
    with open(RULINGS_FILE, encoding="utf-8") as fh:
        payload = json.load(fh)
    if payload.get("schema") != RULINGS_SCHEMA:
        raise FindingsError(f"inspect_rulings.json 的 schema 不对：{payload.get('schema')}")
    by_id = {r["issue_id"]: r for r in load_issues()["issues"]}
    out = defaultdict(list)
    for rec in payload.get("rulings") or []:
        iid = rec.get("issue_id")
        if iid not in by_id:
            raise FindingsError(f"裁定表里的 `{iid}` 不在 issue 表里")
        _check_axes({**rec, "coord": rec.get("final_coord")}, f"{iid} 的裁定")
        for field in ("final_evidence", "ruling_basis"):
            if not (rec.get(field) or "").strip():
                raise FindingsError(f"{iid} 的裁定没写 `{field}`")
        issue = by_id[iid]
        for axis in AXES:
            if (rec.get(axis) or None) != (issue.get(axis) or None):
                raise FindingsError(
                    f"{iid} 的裁定给的 `{axis} = {rec.get(axis)}` 与 issue 表里的 "
                    f"{issue.get(axis)} 不一致 —— 两份文件不许各说一套")
        out[iid].append(rec)
    _RULINGS_CACHE[RULINGS_FILE] = dict(out)
    return _RULINGS_CACHE[RULINGS_FILE]


def has_judged_issues():
    """判定者产出的三份文件在不在。⛔ 不在就**什么都不渲染**。

    ⛔ 不许退化成「那就按脚本分组先渲染着」—— 那正是被撤掉的那版做的事。
    ⚠️ 也不许退化成「那就把 454 条原样摆出来」：`0007` 会出现 34 个填写块，
    判读者要对同一件事按 14 次。
    """
    return all(os.path.exists(f) for f in (ISSUES_FILE, OVERLAP_FILE, RULINGS_FILE))


def _member(rec):
    index = {(r["pair"], r["diag_index"]): r for r in all_findings()}
    return [index[(rec["pair"], d)] for d in rec["diag_indices"]]


def issues_of(pair, verdict=None, new_block_only=False, merged_only=False):
    """取某个 pair 的归一化 issue，按 id 排序，每条附 `members` / `overlap` / `rulings`。

    - `verdict`：`intrinsic` / `uncertain`，不给就两族都要。
    - `new_block_only`：只要**新建填写块**的那些（判重结论 `suspect` / `none`）。
    - `merged_only`：只要**并入既有条目**的那些（`ledger` / `candidate`）。
    """
    if not has_judged_issues():
        return []
    overlap = load_overlap()
    rulings = load_rulings()
    out = []
    for rec in load_issues()["issues"]:
        if rec["pair"] != pair:
            continue
        if verdict is not None and rec["verdict_class"] != verdict:
            continue
        kind = overlap[rec["issue_id"]]["overlap_kind"]
        if new_block_only and kind not in NEW_BLOCK_KINDS:
            continue
        if merged_only and kind in NEW_BLOCK_KINDS:
            continue
        out.append(dict(rec, members=_member(rec),
                        overlap=overlap[rec["issue_id"]],
                        rulings=rulings.get(rec["issue_id"]) or []))
    out.sort(key=lambda r: r["issue_id"])
    return out


def merged_into(target):
    """取判重结论为「并入 `target`」的 issue（`target` 是台账 id 或候选键）。

    ⛔ 只认 `ledger` / `candidate` 两个桶 —— `suspect` 那 24 条**新建自己的块**，
    ⚠️ 它们只是在块里点名「疑似与某条重合，请判读者确认」，⛔ 不并进被点名那条里。
    """
    if not has_judged_issues():
        return []
    overlap = load_overlap()
    out = []
    for rec in load_issues()["issues"]:
        d = overlap[rec["issue_id"]]
        if d["overlap_kind"] in NEW_BLOCK_KINDS or d.get("overlap_target") != target:
            continue
        out.append(dict(rec, members=_member(rec), overlap=d,
                        rulings=load_rulings().get(rec["issue_id"]) or []))
    out.sort(key=lambda r: r["issue_id"])
    return out


def compression(pair):
    """该 pair 的归一化压缩比：`(原始待呈现诊断数, issue 数)`。

    ⚠️ 判读者必须知道他看到的一条 issue 背后有几条诊断 —— `0007` 是 35 → 7。
    ⛔ 分子只数**待呈现**的那些（intrinsic + uncertain）加上本轮恢复的，
    ⛔ 不含 `projection_artifact` 与仍然维持 refuted 的那些。
    """
    rows = issues_of(pair)
    return sum(len(r["diag_indices"]) for r in rows), len(rows)


def verdict_class_of(issue_id):
    """某条 issue 的分拣族。⛔ 找不到就抛 —— 静默返回 None 会让两个物种混在一起统计。"""
    for rec in load_issues()["issues"]:
        if rec["issue_id"] == issue_id:
            return rec["verdict_class"]
    raise FindingsError(f"`{issue_id}` 不在 issue 表里")


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
