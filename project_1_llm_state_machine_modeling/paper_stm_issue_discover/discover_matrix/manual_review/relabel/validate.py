#!/usr/bin/env python3
"""校验人工重标的完整性与去重，并刷新 `PROGRESS.md`。

用法：

    python3 validate.py                  # 校验 + 打印报告
    python3 validate.py --pairs 0000
    python3 validate.py --write-progress # 顺便重写 PROGRESS.md
    python3 validate.py --json           # 机器可读输出

退出码：有 `E` 级问题 → 1；只有 `W` 级 → 0。

两类检查：

1. **完整性** —— 每条台账记录都裁了没、每个候选都裁了没、勾了「修正 / 拆分」有没有
   写出修正后的 statement、新增条目的必填项齐不齐。新增条目这一侧只做两件事，
   两件都能**只看字段值**判定（[CLAUDE.md](../../../../../CLAUDE.md) §11 对「门」的准入要求）：

   - **枚举取值合法性** —— 五个座标轴的取值必须落在
     [newfields.py](./newfields.py) `ENUMS` 里，且是单值。
   - **`other` 必须附说明** —— 五个轴里任意一个取 `other`，`other_note` 就必须非空。
     判据只看字段值（哪几个轴逐字等于 `other`、说明空不空），不读文意。
     ⛔ 「这句说明写得对不对」是语义判断，不查。见类型学
     [§3.7.1](../../docs/protocol/defect_taxonomy.md)。
   - **条件式分支的必填一致性** —— `defect_locus = element` 必须给出维度 A
     （`defect_element`）与维度 B（`defect_qualifier`）；`defect_locus` 取
     `pair` / `global` / `other` 必须给出维度 D（`defect_logic_kind`）。
     填了**另一支**的轴只报 `W`：那多半是选完 locus 忘了删，而「填多了」
     不像「填少了」那样让记录不可用。

   自由文本三项（`statement` / `expected_after_fix` / `nl_evidence`）只查非空，
   同样是确定性判据。`nl_evidence` 写 `无` 是合法答案，留空不是。

2. **去重** —— 新增条目之间、新增条目与本 pair 现有台账条目之间的近重复。
   判据是归一化文本 Jaccard 与命中同一批模型元素名。
   ⚠️ 只报 `W` —— 「是不是同一个缺陷」是语义判断，不能做成确定性门，也不自动判重。

**这里不做语义判断。** 「这条主张需不需要时钟语义」「这两条是不是同一个缺陷」
「这条 `defect_reference` 选对了没有」都要读文意，做成 `E` 会把正确答案挡在门外；
判据在判读者手里（工作单 §5.2 逐取值内联了判定测试），不在校验器手里。

⛔ **边界（时钟 / 不变式 / 并发）不再由校验器过问。** 判读者只判「这是不是缺陷」，
不判「它属于我们框架的哪一格」；界外发现照常写在 `statement` 里，
回收后由主 session 从自由文本人工分拣。理由见 [README.md](./README.md) §二.1。
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

# 新增条目的必填 / 可选 / 枚举取值口径唯一真源是 [newfields.py](./newfields.py)，
# 不要在本文件里另抄一份 —— 抄了就会与模板走偏。本文件一律经 `NF.` 前缀引用。
DECISION_FIELD = "裁决"

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


def _enum_check(rep, pair, nid, fields, name, allowed, required, why=""):
    """检查枚举字段。返回唯一取值（没有 / 非法时返回 `None`）。

    三条判据都是**确定性**的（有没有、是不是单值、在不在集合内），故一律报 `E`。
    `why` 只在必填缺失时附上一句「为什么这一条要回答它」。
    """
    vals = _enum_values(fields.get(name))
    if not vals:
        if required:
            rep.E(pair, nid,
                  f"必填项 `{name}` 未选 —— 取值只能是 "
                  + "、".join(f"`{a}`" for a in allowed)
                  + (f"。{why}" if why else ""))
        return None
    if len(vals) > 1:
        rep.E(pair, nid, f"`{name}` 是单值字段，却给了 {vals}")
        return None
    if vals[0] not in allowed:
        rep.E(pair, nid,
              f"`{name} = {vals[0]}` 不在枚举内。允许取值："
              + "、".join(f"`{a}`" for a in allowed)
              + "。归不进就选 `other`，不要造新取值")
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
        if chosen[0] == "并入现有条目" and not _text(cand.get("并入到")):
            rep.E(pair, cand["key"], "候选判为并入但未写「并入到」")

    if data["summary"] is None:
        rep.W(pair, "PAIR", "无 §0 结论块")
    else:
        if not _chosen(data["summary"].get("本 pair 整体判断")):
            rep.W(pair, "PAIR", "§0 未给整体判断")

    # ---------------------------------------------------------- 新增条目
    #
    # 这一段只做两件事，两件都只看字段值：枚举取值合法性、条件式分支的必填一致性。
    # 语义判断不进这里 —— 判据逐取值内联在工作单 §5.2，由判读者执行。
    vocab = _model_vocabulary(pair) if data["new_issues"] else set()
    new_sigs = []
    for rec in data["new_issues"]:
        nid = rec["id"]
        f = rec["fields"]

        # ---- ① 座标系：先判 locus，它决定后面问哪些轴
        locus = _enum_check(rep, pair, nid, f, "defect_locus",
                            NF.ENUMS["defect_locus"], required=True)
        for axis in NF.required_axes_for(locus):
            _enum_check(rep, pair, nid, f, axis, NF.ENUMS[axis], required=True,
                        why=f"`defect_locus = {locus}` 走的这一支必须回答它")
        for axis in NF.forbidden_axes_for(locus):
            if NF.field_value(f, axis):
                rep.W(pair, nid,
                      f"`defect_locus = {locus}` 不问 `{axis}`，但它被填了 "
                      f"`{NF.field_value(f, axis)}` —— 多半是选完 locus 忘了删。"
                      f"本条只需回答 {'、'.join('`%s`' % a for a in NF.required_axes_for(locus))}")
            else:
                # 没填是对的，但取值若非法仍要报 —— 否则错拼的取值会静默留在盘上
                _enum_check(rep, pair, nid, f, axis, NF.ENUMS[axis], required=False)
        # locus 未填时两支都还没定，此时只校验取值合法性，不要求任何一支
        if locus is None:
            for axis in NF.ELEMENT_BRANCH_FIELDS + NF.LOGIC_BRANCH_FIELDS:
                _enum_check(rep, pair, nid, f, axis, NF.ENUMS[axis], required=False)
        _enum_check(rep, pair, nid, f, "defect_reference",
                    NF.ENUMS["defect_reference"], required=True)

        # ---- ①b 任一轴选了 `other` → 必须附一句说明（类型学 §3.7.1）
        #
        # ⭐ 判据只看字段值：「哪几个轴逐字等于 `other`」与「说明字段空不空」，
        # 两问都不需要读文意，故按 CLAUDE.md §11 允许做成 `E`。
        # ⛔ 「这句说明写得对不对」是语义判断，**不查** —— 查了就会把正确答案挡在门外。
        #
        # 只数**这一条真要回答的轴**：locus + 参照物 + 该分支的轴。
        # ⛔ 不数另一支那些「填多了忘了删」的轴 —— 它们本来就只报 `W`，
        # 让它们连带触发一条 `E` 会把提醒升级成阻塞。
        asked = ["defect_locus", "defect_reference"] + NF.required_axes_for(locus)
        picked = [a for a in asked if NF.field_value(f, a) == "other"]
        if picked and not _text(f.get(NF.OTHER_NOTE_FIELD)):
            rep.E(pair, nid,
                  "、".join(f"`{a}`" for a in picked)
                  + f" 选了 `other`，但 `{NF.OTHER_NOTE_FIELD}` 是空的。"
                    "`other` 是出口，出口不写清等于没分类：请写一句说清**它到底是什么**，"
                    "或说清**这一条涉及多个取值、一格装不下**（是哪几个）。两种都是合法答案，"
                    "但必须说出是哪一种")

        # ---- ② 错的描述 · ③ 修好算什么：两项自由文本，只查非空
        stmt = _text(f.get("statement"))
        if not stmt:
            rep.E(pair, nid, "必填项 `statement` 为空 —— 没写出错在哪、错成什么样")
        if not _text(f.get("expected_after_fix")):
            rep.E(pair, nid,
                  "必填项 `expected_after_fix` 为空 —— 没写出**修好之后怎样才算 ok**。"
                  "写成一句可判定的期望结果（「从 X 施加 Y 后应当到达 Z」），"
                  "不要写「应该修好」")

        # ---- NL 依据：留空 ≠ 写 `无`
        nle = _text(f.get("nl_evidence"))
        if not nle:
            rep.E(pair, nid,
                  "必填项 `nl_evidence` 为空。留空 ≠ 写 `无`："
                  "NL 未明说就**显式写 `无`**（那表示本条不靠 NL 判定，是合法答案）；"
                  "留空只能表示还没判")
        cited = _known_seg_ids(pair) & _seg_refs(nle)
        if nle and not NF.is_none_mark(nle) and not cited:
            rep.W(pair, nid,
                  f"`nl_evidence` 里没认出本 pair 的段 id（本 pair 的段 id 形如 "
                  f"`{sorted(_known_seg_ids(pair))[0]}`）—— 写段 id 才能机械回链到 "
                  f"§1.1 的段 id 表（同组共用 `nl_XXXX/{S.NL_DOC}`）")
        for bad in _seg_refs(nle) - _known_seg_ids(pair):
            rep.E(pair, nid, f"`nl_evidence` 引用了本 pair 不存在的段 id `{bad}`")
        if (NF.field_value(f, "defect_reference") == "requirement"
                and NF.is_none_mark(nle)):
            rep.W(pair, nid,
                  "`defect_reference = requirement` 的判定测试是「**必须引用 NL 的某一句**"
                  "才能判定」，而 `nl_evidence` 写的是「无」。"
                  "两者多半有一个要改：依据真在 NL 上就补段 id，不在就把参照物改成 "
                  "`language`（只靠建模语言规则）或 `other`。"
                  "只报提醒不报错 —— 「这一条到底靠不靠某句 NL」要读文意")

        new_sigs.append({
            "id": nid, "stmt": stmt,
            "locus": locus,
            "tokens": _norm_tokens(stmt),
            "elements": _norm_tokens(stmt) & vocab,
        })

    # ---------------------------------------------------------- 去重
    #
    # 三条判据全部只报 `W`：「是不是同一个缺陷」是语义判断，做成门会把
    # 「两条相邻但确实不同的缺陷」挡在外面。
    for i in range(len(new_sigs)):
        for j in range(i + 1, len(new_sigs)):
            a, b = new_sigs[i], new_sigs[j]
            key = f"{a['id']}~{b['id']}"
            shared = a["elements"] & b["elements"]
            if a["locus"] and a["locus"] == b["locus"] and shared:
                rep.W(pair, key,
                      f"两条新增条目同 `defect_locus = {a['locus']}` 且都点到 "
                      f"{sorted(shared)} —— 是不是同一缺陷？")
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
            sim = _jaccard(sig["tokens"], led_tokens)
            why = None
            # 只点到同一个元素名**不足以**提示重复：一个 pair 的几条台账记录常常
            # 围着同一个状态转，那样每条新增都会被标一次，提示就成了噪声。
            # 故要求元素重合**且**文本也有一定重合；纯文本高度相似另算一条。
            if hit and sim >= 0.2:
                why = f"都点到 {sorted(hit)}，且词 Jaccard {sim:.2f}"
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


def pair_progress(pair, data):
    ledger_total = len(S.ledger_records(pair))
    ledger_done = sum(1 for r in data["ledger"] if _chosen(r.get(DECISION_FIELD)))
    cand_total = len(data["candidates"])
    cand_done = sum(1 for r in data["candidates"] if _chosen(r.get(DECISION_FIELD)))
    chk_total = sum(len(c["items"]) for c in data["checklist"])
    chk_done = sum(1 for c in data["checklist"] for i in c["items"] if i["checked"])
    findings = sum(1 for c in data["checklist"] for i in c["items"] if i["finding"])
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
        "new": len(data["new_issues"]),
        "overall": overall, "minutes": minutes,
    }


PROGRESS_HEADER = """# 人工重标进度看板

本文件由 [validate.py](./validate.py) `--write-progress` 重写，**不要手改** —— 状态直接从 54 份工作单的勾选情况算出来。口径见 [README.md](./README.md)。

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
        f"校验：{counts['E']} 个 `E`、{counts['W']} 个 `W`。"
    )
    lines.append("")
    lines.append(f"最后刷新：`{datetime.datetime.now().isoformat(timespec='seconds')}`")
    lines.append("")
    lines.append("| NL 组 | pair | 状态 | 台账裁决 | 候选裁决 | 清单已过 | 清单发现 | 新增 | 整体判断 | 耗时(分) |")
    lines.append("| :-- | :-- | :-: | --: | --: | --: | --: | --: | :-- | --: |")
    for r in rows:
        d = S.nl_dir(r["pair"])
        lines.append(
            f"| [`{d}`](./{d}/{S.NL_DOC}) | [`{r['pair']}`](./{d}/{r['pair']}.md) | "
            f"{r['status']} | {r['ledger']} | "
            f"{r['candidates']} | {r['checklist']} | {r['findings']} | {r['new']} | "
            f"{r['overall']} | {r['minutes']} |")
    lines.append("")
    lines.append(
        "**「NL 组」栏**：同一组的 6 个 pair 由**同一份 NL 规约**生成 6 个不同制品，"
        f"共用一份 `nl_XXXX/{S.NL_DOC}`。想一次处理完同一份 NL 的模型，就按这一栏排着做。"
        f"分组判据是 NL 全文的 sha8，不是 pair id 的末位数字 —— `0002` 与 `0013` 同组、"
        f"`0003` 与 `0012` 同组。"
    )
    lines.append("")
    lines.append(
        "**「新增」栏**：判读者在 §5 登记的条目数，不分界内界外。"
        "边界（时钟 $C$ / 不变式 $Inv$ / 正交区）不再由判读者分类 —— "
        "判读者只判「这是不是缺陷」，界外的发现照常写在 `statement` 里，"
        "回收后由主 session 从自由文本人工分拣。理由见 [README.md](./README.md) §二.1。"
    )
    lines.append("")
    lines.append(
        "**`00x8` 六个 pair（`0008` `0018` `0028` `0038` `0048` `0058`）不在表内** —— "
        "它们的 NL 要求 fork/join 与秒级时间约束，忠实模型在 $M = (S, E, V, Tr, A)$ 中无法表示，"
        "按 [nl_scope_rule.md](../../docs/protocol/nl_scope_rule.md) 永久排除，不进网格也不进分母。"
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

    # ⛔ 递归扫：工作单已按 NL 组下沉一层，⚠️ 只看根目录会漏掉藏在子目录里的越界工作单。
    found = S.find_worksheets(args.dir)
    for p in S.OUT_OF_SCOPE_PAIRS:
        if p in found:
            rep.E(p, "SCOPE",
                  f"`00x8` 越界 pair 不该有工作单（发现于 "
                  f"`{os.path.relpath(found[p], args.dir)}`）—— 它不在评测网格内，"
                  "重标它会把分母改错")

    rows = []
    data_all = {}
    for pair in pairs:
        path = S.worksheet_path(args.dir, pair)
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
