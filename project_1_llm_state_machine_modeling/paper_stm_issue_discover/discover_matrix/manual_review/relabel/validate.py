#!/usr/bin/env python3
"""校验人工重标的完整性、边界与去重，并刷新 `PROGRESS.md`。

用法：

    python3 validate.py                  # 校验 + 打印报告
    python3 validate.py --pairs 0000
    python3 validate.py --write-progress # 顺便重写 PROGRESS.md
    python3 validate.py --json           # 机器可读输出

退出码：有 `E` 级问题 → 1；只有 `W` 级 → 0。

三类检查：

1. **完整性** —— 每条台账记录都裁了没、每个候选都裁了没、勾了「修正 / 拆分」有没有
   写出修正后的 statement、新增条目的**必填项**齐不齐、
   `basis` / `scope` / `direction` / `depth` / `layer` / `primary_predicate` 的取值
   在不在枚举内。⭐ 这一类**全部是确定性判据**（枚举成员、非空、字段间的定值一致性），
   故一律报 `E`。⭐ 标了「越界」的条目只要求事实层三项（见 `NF.REQUIRED_WHEN_OUT_OF_SCOPE`）。
2. **⛔ 建模对象边界（③ 边界层）** —— 新增条目不许**作为缺陷**落在 $M = (S, E, V, Tr, A)$
   之外：⛔ 无时钟 / 计时 / 秒级约束，⛔ 无不变式，⛔ 无正交区并发。
   ⭐ 主判据是判读者自己勾的 `scope`：勾了越界的条目 `in_scope = False`、
   **不计入缺陷统计**（`pair_progress` 单列一栏）。
   ⭐ 词法关键词只作**补网**：`statement` 命中越界词却仍勾 `界内` 时报 `W` 让人复核。
   ⚠️ 它**会误伤**（元素恰好叫 `Timer` / `fork`），故只提醒，⛔ 不自动改判、⛔ 不删。
   ⛔ 只有两处报 `E`：`00x8` 越界 pair 出现了工作单；枚举取值非法。
   ⚠️ ⛔ 词法门**不扫 `generated_side`** —— 那是定位串，引用一行叫 `Timer` 的状态
   不使主张越界。越界与否看的是主张要不要时钟 / 并发语义，⛔ 不是名字里有没有那些词。
3. **去重** —— 新增条目之间、新增条目与本 pair 现有台账条目之间的近重复。三条判据：
   同一作者源行号；同 `direction` + 命中同一批模型元素名；归一化文本 Jaccard。
   ⚠️ 三条都只报 `W` —— 「是不是同一个缺陷」是语义判断，⛔ 不能做成确定性门，
   ⛔ 也不自动判重，只提示人工确认。
4. **⭐ 依据自洽（② 依据层）** —— `basis` 与 `nl_evidence` / `layer` / `statement`
   必须说同一件事。确定性的部分报 `E`：
   ⛔ 勾了 `NL显式义务` / `NL欠指定` 却给不出本 pair 的段 id；
   ⛔ 勾了 `NL欠指定` 或 `参考模型` 却把 `layer` 记成 `nl_contradiction`
   （⚠️ 后者正是 `EIS-0005-02` 的病灶，见 [README.md](./README.md) §7.1）；
   ⛔ 勾了 `模型自身` 却把 `layer` 记成 `nl_named` / `nl_contradiction`。
   ⭐ 需要读文意的部分只报 `W`：勾了 `NL欠指定` 却在 `statement` 里写「违反」
   （欠指定的句子不构成显式义务，谈不上违反）；勾了 `参考模型`（依据强度不足）。

⛔ **为什么第 2、3 类与第 4 类的一半只报 `W`**：按 [CLAUDE.md](../../../../../CLAUDE.md) §11，
只有能被完美判定的约束才允许做成会一票否决的门。「这条主张需不需要时钟语义」
「这两条是不是同一个缺陷」「这句 statement 算不算在说违反」都要语义解释，
做成 `E` 会把正确答案挡在门外。⭐ 反过来，「勾了 A 就不能同时勾 B」只看两个枚举字段的值，
⛔ 不需要任何语义解释，故报 `E`。
"""

from __future__ import annotations

import argparse
import datetime
import functools
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import collect as C                                # noqa: E402
import newfields as NF                             # noqa: E402
import sources as S                                # noqa: E402
from pumlmodel import PumlModel                    # noqa: E402

# ⛔ 建模对象边界之外的词。命中只报 W —— 判据是词法，会误伤。
OUT_OF_SCOPE_CUES = [
    (r"\bfork\b|\bjoin\b|分叉|汇合", "并发伪状态（fork / join）"),
    (r"正交|并发|并行|同时活跃|orthogonal|concurrent|parallel|region.*同时", "正交区 / 并发语义"),
    (r"时钟|计时器|clock\b|timer\b|\btimeout\b", "时钟 / 计时器"),
    (r"\d+\s*(秒|毫秒|ms\b|s\b|second)|秒级|毫秒", "时间量"),
    (r"不变式|invariant\b(?!\s*\()", "不变式（$Inv$）"),
    (r"\bwithin\s+\d|在\s*\d+\s*(秒|毫秒)内", "时限约束"),
]

# ⭐ 新增条目的必填 / 可选 / 枚举取值口径唯一真源是 [newfields.py](./newfields.py)，
# ⛔ 不要在本文件里另抄一份 —— 抄了就会与模板走偏。本文件一律经 `NF.` 前缀引用。
DECISION_FIELD = "裁决"
DEPTH_FIELD = "深度"

_RE_ENUM_SPLIT = re.compile(r"[,，/、\s]+")


def _norm_tokens(text):
    return set(re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", (text or "").lower()))


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _chosen(field):
    if isinstance(field, dict):
        return field.get("chosen") or []
    return []


def _text(field):
    if isinstance(field, str):
        return field.strip()
    return ""


def _enum_values(field):
    """勾选行取 `chosen`；自由文本行按分隔符切开。⭐ 两种写法都收。"""
    if isinstance(field, dict):
        return [v for v in (field.get("chosen") or []) if v]
    t = _text(field)
    if not t:
        return []
    return [x for x in _RE_ENUM_SPLIT.split(t) if x]


def _enum_check(rep, pair, nid, fields, name, allowed, required):
    """检查枚举字段。返回唯一取值（没有 / 非法时返回 `None`）。

    ⭐ 三条判据都是**确定性**的（有没有、是不是单值、在不在集合内），故一律报 `E`。
    """
    vals = _enum_values(fields.get(name))
    if not vals:
        if required:
            rep.E(pair, nid,
                  f"必填项 `{name}` 未选 —— 取值只能是 "
                  + "、".join(f"`{a}`" for a in allowed))
        return None
    if len(vals) > 1:
        rep.E(pair, nid, f"`{name}` 是单值字段，却给了 {vals}")
        return None
    if vals[0] not in allowed:
        rep.E(pair, nid,
              f"`{name} = {vals[0]}` 不在枚举内。允许取值："
              + "、".join(f"`{a}`" for a in allowed)
              + ("。⭐ 归不进就选 `unclassified`，⛔ 不要造新取值"
                 if "unclassified" in allowed else ""))
        return None
    return vals[0]


@functools.lru_cache(maxsize=None)
def _known_seg_ids(pair):
    return {sid for sid, _ in S.nl_segments(pair)[0]}


_RE_SEG_REF = re.compile(r"\bNL-[A-Z]\d{3}\b")


def _seg_refs(text):
    return set(_RE_SEG_REF.findall(text or ""))


@functools.lru_cache(maxsize=None)
def _model_vocabulary(pair):
    """本 pair 作者源里出现过的元素名（状态 / 触发词 / 变量），小写。

    ⭐ 去重判据用它把「点到同一个模型元素」与「只是用词雷同」区分开。
    """
    model = PumlModel(S.puml_text(pair), pair)
    out = set()
    for name in model.states:
        out.add(name.lower())
    for trig in model.triggers():
        out |= {t.lower() for t in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", trig)}
    for var in model.variable_candidates():
        out.add(var.lower())
    return out


# ⭐「声称模型违反了 NL」的措辞。⛔ 判据是词法、会误伤，故只报 `W`。
_RE_VIOLATION = re.compile(r"违反|违背|不符合\s*NL|与\s*NL\s*矛盾|contradict|violat", re.I)


def _check_basis(rep, pair, nid, basis, layer, nle, cited, stmt):
    """② 依据层的自洽检查。

    ⭐ 分两类，⛔ 不许混：**只看两个枚举字段的值**就能判定的报 `E`（确定性，
    符合 [CLAUDE.md](../../../../../CLAUDE.md) §11 对「门」的准入要求）；
    需要读文意才能判定的报 `W`。

    ⚠️ 这一层之所以单独存在，是因为台账的 `layer` 把四种强度不同的依据混在一个轴上，
    实测已经造成过一次归类错（`EIS-0005-02`：真正的依据是**参考模型**，
    却被记成 `nl_contradiction`，见 [README.md](./README.md) §7.1）。
    """
    if not basis:
        return

    # ---- E：NL 类依据必须落到具体某一段
    if basis in NF.NL_BASED_BASES and not cited:
        rep.E(pair, nid,
              f"`basis = {basis}` 却给不出本 pair 的 NL 段 id"
              f"（`nl_evidence` 现为 `{nle or '（空）'}`）。"
              "⛔ 依据在 NL 上，就必须指到**哪一段** —— 段 id 形如 "
              f"`{sorted(_known_seg_ids(pair))[0]}`，⭐ 后面可以再跟一句逐字引文。"
              "⭐ 若依据其实不在 NL 上，请把 `basis` 改成 `模型自身` 或 `参考模型`")

    # ---- E：`layer` 与 `basis` 的定值冲突
    if basis == "NL欠指定" and layer == "nl_contradiction":
        rep.E(pair, nid,
              "`basis = NL欠指定` 与 `layer = nl_contradiction` 不能并存 —— "
              "⛔ 欠指定的句子**不构成显式义务**，谈不上「与显式义务矛盾」。"
              "⭐ 要么改 `basis` 为 `NL显式义务`（并说明那一句到底把哪些槽位说清了），"
              "要么改 `layer`")
    if basis == "参考模型" and layer == "nl_contradiction":
        rep.E(pair, nid,
              "`basis = 参考模型` 与 `layer = nl_contradiction` 不能并存 —— "
              "⛔ 参考模型不是 NL。⚠️ 这正是 `EIS-0005-02` 的病灶："
              "它真正的依据是参考侧「六个状态全部平级」，却被记成了与 NL 显式义务矛盾"
              "（见 [README.md](./README.md) §7.1）")
    if basis == "模型自身" and layer in ("nl_named", "nl_contradiction"):
        rep.E(pair, nid,
              f"`basis = 模型自身` 与 `layer = {layer}` 不能并存 —— "
              "⛔ 那一层按台账定义要求 NL 逐字依据。"
              "⭐ 只读模型就能判定的走 `wellformedness`")

    # ---- W：要读文意才能判定的
    if basis == "NL欠指定" and _RE_VIOLATION.search(stmt):
        rep.W(pair, nid,
              "`basis = NL欠指定`，⛔ 但 `statement` 里出现了「违反」类措辞。"
              "⛔ 欠指定的意思是**原文没把这件事说清**（没写源状态 / 没写触发 / "
              "并列项无连接词），因此它支撑不起「模型违反了它」。"
              "⭐ 请改写成「原文未规定，模型自行选择了一种读法」这类表述，"
              "或改 `basis` 为 `NL显式义务` 并说明那一句说清了什么。"
              "⚠️ 判据是词法、会误伤（例如你写的是「不违反」）")
    if basis == "参考模型":
        rep.W(pair, nid,
              "`basis = 参考模型` —— ⚠️ 参考模型**不是正确答案**"
              "（语料里多处参考侧比生成侧更差，见 §1.4 与 README §二.3），"
              "⛔ 故这一种依据**单独不足以**支撑一条缺陷。"
              "⭐ 请在 `statement` 里写明还缺什么才站得住；⛔ 台账四层也没有它的槽位")
    if basis == "模型自身" and cited:
        rep.W(pair, nid,
              f"`basis = 模型自身` 却又引了 {sorted(cited)} —— ⭐ 两者不矛盾"
              "（NL 可以只作背景），⛔ 但若这一条其实是靠 NL 才成立的，"
              "`basis` 应改成 `NL显式义务` 或 `NL欠指定`")


class Report:
    def __init__(self):
        self.items = []

    def add(self, level, pair, key, msg):
        self.items.append({"level": level, "pair": pair, "key": key, "msg": msg})

    def E(self, *a):
        self.add("E", *a)

    def W(self, *a):
        self.add("W", *a)

    def counts(self):
        return {
            "E": sum(1 for i in self.items if i["level"] == "E"),
            "W": sum(1 for i in self.items if i["level"] == "W"),
        }


def validate_pair(pair, data, rep):
    ledger = {r["id"]: r for r in S.ledger_records(pair)}

    # ---------------------------------------------------------- 完整性
    seen = set()
    for rec in data["ledger"]:
        rid = rec["id"]
        seen.add(rid)
        chosen = _chosen(rec.get(DECISION_FIELD))
        if not chosen:
            rep.E(pair, rid, "台账条目未裁决（`裁决:` 一行没有任何 `[x]`）")
        elif len(chosen) > 1:
            rep.E(pair, rid, f"裁决多选：{chosen} —— 该字段是单值")
        depth = _chosen(rec.get(DEPTH_FIELD))
        if chosen and chosen[0] != "删除" and not depth:
            rep.E(pair, rid, "未判深度（`深度:` 没有任何 `[x]`）")
        elif len(depth) > 1:
            rep.E(pair, rid, f"深度多选：{depth}")
        if chosen and chosen[0] in ("修正", "拆分"):
            if not _text(rec.get("修正后的 statement")) and not _text(rec.get("修正后的statement")):
                rep.E(pair, rid, f"裁决为「{chosen[0]}」但未写出修正后的 statement")
        if chosen and not _text(rec.get("理由")):
            rep.W(pair, rid, "裁决无理由 —— 重标的价值一半在理由里")
    for rid in ledger:
        if rid not in seen:
            rep.E(pair, rid, "工作单里找不到该台账条目的裁决区（材料可能没重新生成）")

    for cand in data["candidates"]:
        chosen = _chosen(cand.get(DECISION_FIELD))
        if not chosen:
            rep.W(pair, cand["key"], "候选未裁决")
            continue
        if len(chosen) > 1:
            rep.E(pair, cand["key"], f"候选裁决多选：{chosen}")
        if chosen[0].startswith("采纳"):
            if not _text(cand.get("补入后的 statement")) and not _text(cand.get("补入后的statement")):
                rep.E(pair, cand["key"], "候选判为采纳但未写出补入后的 statement")
            if not _chosen(cand.get(DEPTH_FIELD)):
                rep.E(pair, cand["key"], "候选判为采纳但未判深度")
        if chosen[0] == "并入现有条目" and not _text(cand.get("并入到")):
            rep.E(pair, cand["key"], "候选判为并入但未写「并入到」")

    if data["summary"] is None:
        rep.W(pair, "PAIR", "无 §0 结论块")
    else:
        if not _chosen(data["summary"].get("本 pair 整体判断")):
            rep.W(pair, "PAIR", "§0 未给整体判断")

    # ---------------------------------------------------------- 新增条目
    vocab = _model_vocabulary(pair) if data["new_issues"] else set()
    new_sigs = []
    for rec in data["new_issues"]:
        nid = rec["id"]
        f = rec["fields"]

        # ---- ① 事实层：两项恒必填（⭐ 越界条目也要说清「看到了什么、在哪」）
        stmt = _text(f.get("statement"))
        if not stmt:
            rep.E(pair, nid, "必填项 `statement` 为空 —— 没写出看到了什么")
        gen = _text(f.get("generated_side"))
        if not gen:
            rep.E(pair, nid,
                  "必填项 `generated_side` 为空 —— 没指出模型里哪一处"
                  "（写 §1.3 的行号如 `:12`，或元素名）")

        # ---- ③ 边界层：先判它，因为**越界条目免填依据层与分类轴**
        scope = _enum_check(rep, pair, nid, f, "scope", NF.SCOPES, required=True)
        oos = NF.is_out_of_scope(scope)
        need = not oos          # ⭐ 越界 → 不是缺陷 → 谈依据强度与缺陷方向没有意义

        # ---- ② 依据层 + ④ 分类轴：完整性
        basis = _enum_check(rep, pair, nid, f, "basis", NF.BASES, required=need)
        nle = _text(f.get("nl_evidence"))
        if not nle and need:
            rep.E(pair, nid,
                  "必填项 `nl_evidence` 为空。⛔ 留空 ≠ 写 `无`："
                  "NL 未明说就**显式写 `无`**（那表示本条属模型内生问题，是合法答案）；"
                  "留空只能表示还没判")
        direction = _enum_check(rep, pair, nid, f, "direction", NF.DIRECTIONS,
                                required=need)
        _enum_check(rep, pair, nid, f, "depth", NF.DEPTHS, required=need)
        layer = _enum_check(rep, pair, nid, f, "layer", NF.LAYERS, required=False)
        pp = _text(f.get("primary_predicate"))
        if pp and not NF.is_none_mark(pp) and pp not in S.ALL_PREDICATES:
            rep.E(pair, nid,
                  f"`primary_predicate = {pp}` 不在 19 谓词封闭词表内。"
                  "⭐ 写不出谓词就写 `无` 并在 `statement` 末尾写明词表缺口，"
                  "⛔ 不要造新谓词名")

        # ---- 完整性：字段间的定值一致性（⭐ 确定性，故报 E）
        if layer and layer != "wellformedness" and NF.is_none_mark(nle):
            rep.E(pair, nid,
                  f"`layer = {layer}` 按台账定义要求 NL 逐字依据，"
                  "但 `nl_evidence` 写的是「无」。⛔ 二者不能并存："
                  "要么改 `layer` 为 `wellformedness`，要么给出 NL 段 id")
        cited = _known_seg_ids(pair) & _seg_refs(nle)
        if nle and not NF.is_none_mark(nle) and not cited:
            rep.W(pair, nid,
                  f"`nl_evidence` 里没认出本 pair 的段 id（本 pair 的段 id 形如 "
                  f"`{sorted(_known_seg_ids(pair))[0]}`）—— ⭐ 写段 id 才能机械回链到 §1.2")
        for bad in _seg_refs(nle) - _known_seg_ids(pair):
            rep.E(pair, nid, f"`nl_evidence` 引用了本 pair 不存在的段 id `{bad}`")

        # ---- ④ ⭐ 依据自洽（② 依据层内部，以及依据层与 `layer` / `statement` 之间）
        _check_basis(rep, pair, nid, basis, layer, nle, cited, stmt)

        # ---- 行号与 element_of_M 推导
        refs = NF.parse_line_refs(gen)
        n_lines = len(S.puml_text(pair).splitlines())
        for r in refs:
            if r > n_lines:
                rep.E(pair, nid,
                      f"`generated_side` 引用了作者源第 {r} 行，但该文件只有 {n_lines} 行")
        elem, basis = NF.derive_element_of_M(pair, gen, pp if pp not in ("",) else None)
        if elem is None:
            rep.W(pair, nid,
                  "推不出 `element_of_M` —— " + basis
                  + "。⭐ 在 `generated_side` 里加上作者源行号即可自动推出")

        # ---- ③ ⛔ 建模对象边界门（词法补网）
        # ⛔ 只扫 `statement`（主张本身）。`generated_side` 是定位串，
        # 引用一行叫 `Timer` 的状态不使主张越界。
        # ⭐ 已经自己勾了越界的**不再提醒** —— 它已经判过了，再报一遍只是噪声。
        if not oos:
            for pattern, label in OUT_OF_SCOPE_CUES:
                if re.search(pattern, stmt, flags=re.I):
                    rep.W(pair, nid,
                          f"⛔ 疑似越界（{label}）而 `scope` 勾的是 "
                          f"`{scope or '（未填）'}` —— project_1 的建模对象 "
                          "$M = (S, E, V, Tr, A)$ 无时钟 $C$、无不变式 $Inv$、无正交区。"
                          "⭐ 若确属越界，请把 `scope` 改成对应的「越界·…」档 ——"
                          "那样它仍会落盘，但**不计入缺陷统计**。"
                          "⚠️ 判据是词法，会误伤（元素恰好叫 `Timer` / `fork` 仍在范围内）："
                          "请自问「这条主张成立与否需不需要时钟或并发语义」，"
                          "不需要就忽略本条")
                    break

        new_sigs.append({
            "id": nid, "stmt": stmt, "gen": gen,
            "direction": direction,
            "tokens": _norm_tokens(stmt + " " + gen),
            "elements": _norm_tokens(stmt + " " + gen) & vocab,
            "lines": set(refs),
        })

    # ---------------------------------------------------------- ③-c 去重
    for i in range(len(new_sigs)):
        for j in range(i + 1, len(new_sigs)):
            a, b = new_sigs[i], new_sigs[j]
            key = f"{a['id']}~{b['id']}"
            shared_line = a["lines"] & b["lines"]
            if shared_line:
                rep.W(pair, key,
                      f"两条新增条目指向同一作者源行 {sorted(shared_line)} —— 是不是同一缺陷？")
            elif (a["direction"] and a["direction"] == b["direction"]
                    and a["elements"] & b["elements"]):
                rep.W(pair, key,
                      f"两条新增条目同 `direction = {a['direction']}` 且都点到 "
                      f"{sorted(a['elements'] & b['elements'])} —— 是不是同一缺陷？")
            else:
                sim = _jaccard(a["tokens"], b["tokens"])
                if sim >= 0.6:
                    rep.W(pair, key,
                          f"两条新增条目高度相似（词 Jaccard {sim:.2f}）—— 是不是同一缺陷？")

    for sig in new_sigs:
        for rid, rec in sorted(ledger.items()):
            led_tokens = _norm_tokens((rec.get("statement") or "")
                                      + " " + (rec.get("generated_side") or ""))
            hit = sig["elements"] & led_tokens & vocab
            same_dir = sig["direction"] and sig["direction"] == rec.get("direction")
            sim = _jaccard(sig["tokens"], led_tokens)
            why = None
            if same_dir and hit:
                why = (f"同 `direction = {sig['direction']}` 且都点到 {sorted(hit)}")
            elif sig["direction"] is None and hit:
                # ⭐ `direction` 空的（越界条目，或还没勾）也要比 —— ⛔ 否则「越界条目
                # 其实与某条台账记录说的是同一件事」这种最该被看见的撞车会整类漏掉。
                why = f"都点到 {sorted(hit)}（本条 `direction` 未填，故只按元素比对）"
            elif sim >= 0.5:
                why = f"词 Jaccard {sim:.2f}"
            if why:
                rep.W(pair, sig["id"],
                      f"与现有台账 `{rid}` 疑似重复（{why}）—— "
                      f"若是同一缺陷，应回 §2 对 `{rid}` 走「修正」而不是在 §5 新增")

    # ---------------------------------------------------------- 其他
    for key in data["orphans"]:
        rep.W(pair, key, "孤儿填写区仍有内容 —— 并回正文后请删除，否则不会被计入")
    if data["untouched_keys"] and len(data["untouched_keys"]) < _block_count(data):
        pass  # 部分完成，进度由 PROGRESS.md 反映，不在这里报


def _block_count(data):
    return (len(data["ledger"]) + len(data["candidates"]) + len(data["checklist"])
            + (1 if data["summary"] is not None else 0) + 1)


def new_issue_split(data):
    """新增条目按边界层拆成「计入缺陷统计」与「越界」两堆。

    ⛔ 越界条目**不得计入缺陷统计** —— 它不是缺陷，也不是漏判，而是「不在建模对象内」。
    ⭐ 但它必须仍然可见：那是关于**语料**的事实，丢掉它等于把边界问题伪装成「没人发现」。
    """
    counted, oos = [], []
    for rec in data["new_issues"]:
        scope = NF.field_value(rec.get("fields") or {}, "scope")
        (oos if NF.is_out_of_scope(scope) else counted).append(rec)
    return counted, oos


def pair_progress(pair, data):
    ledger_total = len(S.ledger_records(pair))
    ledger_done = sum(1 for r in data["ledger"] if _chosen(r.get(DECISION_FIELD)))
    cand_total = len(data["candidates"])
    cand_done = sum(1 for r in data["candidates"] if _chosen(r.get(DECISION_FIELD)))
    chk_total = sum(len(c["items"]) for c in data["checklist"])
    chk_done = sum(1 for c in data["checklist"] for i in c["items"] if i["checked"])
    findings = sum(1 for c in data["checklist"] for i in c["items"] if i["finding"])
    counted, oos = new_issue_split(data)
    summary = data["summary"] or {}
    overall = (_chosen(summary.get("本 pair 整体判断")) or ["—"])[0]
    minutes = _text(summary.get("耗时(分钟)")) or "—"
    done = (ledger_done >= ledger_total and cand_done >= cand_total
            and chk_done >= chk_total and overall != "—")
    started = (ledger_done or cand_done or chk_done or data["new_issues"]
               or overall != "—")
    status = "🟢" if done else ("🟡" if started else "⚪")
    return {
        "pair": pair, "status": status,
        "ledger": f"{ledger_done}/{ledger_total}",
        "candidates": f"{cand_done}/{cand_total}",
        "checklist": f"{chk_done}/{chk_total}",
        "findings": findings,
        # ⛔ `new` 只数计入缺陷统计的；越界条目单列在 `out_of_scope`。
        "new": len(counted), "out_of_scope": len(oos),
        "overall": overall, "minutes": minutes,
    }


PROGRESS_HEADER = """# 人工重标进度看板

⛔ 本文件由 [validate.py](./validate.py) `--write-progress` 重写，**不要手改** —— 状态直接从 54 份工作单的勾选情况算出来。口径见 [README.md](./README.md)。

| 记号 | 含义 |
| :-- | :-- |
| ⚪ | 未开始 |
| 🟡 | 进行中 |
| 🟢 | 已完成（台账全裁 + 候选全裁 + 清单全过 + §0 已给整体判断） |
"""


def write_progress(rows, path, counts):
    lines = [PROGRESS_HEADER, ""]
    done = sum(1 for r in rows if r["status"] == "🟢")
    doing = sum(1 for r in rows if r["status"] == "🟡")
    lines.append(
        f"**{done} / {len(rows)} 完成**，{doing} 进行中，"
        f"{len(rows) - done - doing} 未开始。"
        f"累计新增条目 **{sum(r['new'] for r in rows)}** 条，"
        f"清单发现 **{sum(r['findings'] for r in rows)}** 处。"
        f"另有 **{sum(r['out_of_scope'] for r in rows)}** 条被判读者标为越界 —— "
        f"⛔ 它们**不计入**上面的新增条目数。"
        f"校验：{counts['E']} 个 `E`、{counts['W']} 个 `W`。"
    )
    lines.append("")
    lines.append(f"最后刷新：`{datetime.datetime.now().isoformat(timespec='seconds')}`")
    lines.append("")
    lines.append("| pair | 状态 | 台账裁决 | 候选裁决 | 清单已过 | 清单发现 | 新增 | 越界 | 整体判断 | 耗时(分) |")
    lines.append("| :-- | :-: | --: | --: | --: | --: | --: | --: | :-- | --: |")
    for r in rows:
        lines.append(
            f"| [`{r['pair']}`](./{r['pair']}.md) | {r['status']} | {r['ledger']} | "
            f"{r['candidates']} | {r['checklist']} | {r['findings']} | {r['new']} | "
            f"{r['out_of_scope']} | {r['overall']} | {r['minutes']} |")
    lines.append("")
    lines.append(
        "⭐ **「越界」栏**：判读者在 §5 的**③ 边界层**勾了「越界·…」的条目数。"
        "⛔ 越界不是缺陷、也不是漏判，而是该主张需要时钟 $C$ / 不变式 $Inv$ / 正交区语义，"
        "⛔ 不在 project_1 的建模对象 $M = (S, E, V, Tr, A)$ 内。"
        "⭐ 它们照常落盘（那是关于语料的事实），⛔ 但不进缺陷统计。"
    )
    lines.append("")
    lines.append(
        "⛔ **`00x8` 六个 pair（`0008` `0018` `0028` `0038` `0048` `0058`）不在表内** —— "
        "它们的 NL 要求 fork/join 与秒级时间约束，忠实模型在 $M = (S, E, V, Tr, A)$ 中无法表示，"
        "按 [nl_scope_rule.md](../../docs/protocol/nl_scope_rule.md) 永久排除，⛔ 不进网格也不进分母。"
    )
    lines.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pairs", nargs="*", default=None)
    ap.add_argument("--dir", default=HERE)
    ap.add_argument("--write-progress", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    pairs = args.pairs or list(S.IN_SCOPE_PAIRS)
    rep = Report()

    for p in S.OUT_OF_SCOPE_PAIRS:
        if os.path.exists(os.path.join(args.dir, f"{p}.md")):
            rep.E(p, "SCOPE",
                  "⛔ `00x8` 越界 pair 不该有工作单 —— 它不在评测网格内，"
                  "重标它会把分母改错")

    rows = []
    data_all = {}
    for pair in pairs:
        path = os.path.join(args.dir, f"{pair}.md")
        if not os.path.exists(path):
            rep.E(pair, "FILE", "工作单不存在 —— 跑 `python3 generate.py`")
            continue
        data = C.collect_pair(pair, path)
        data_all[pair] = data
        validate_pair(pair, data, rep)
        rows.append(pair_progress(pair, data))

    counts = rep.counts()
    if args.write_progress:
        write_progress(rows, os.path.join(args.dir, "PROGRESS.md"), counts)

    if args.json:
        print(json.dumps({"counts": counts, "items": rep.items, "progress": rows},
                         ensure_ascii=False, indent=1))
    else:
        for it in rep.items:
            print(f"[{it['level']}] {it['pair']} {it['key']}: {it['msg']}")
        print(json.dumps({"E": counts["E"], "W": counts["W"],
                          "pairs_checked": len(rows)}, ensure_ascii=False))
    return 1 if counts["E"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
