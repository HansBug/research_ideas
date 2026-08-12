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
   写出修正后的 statement、新增条目的必填字段齐不齐。
2. **⛔ 建模对象边界** —— 新增条目不许落在 $M = (S, E, V, Tr, A)$ 之外：
   ⛔ 无时钟 / 计时 / 秒级约束，⛔ 无不变式，⛔ 无正交区并发（fork / join / 同时活跃）。
   判据是词法关键词命中，⚠️ **会误伤**（例如状态恰好叫 `fork`），所以命中报 `W` 让人复核，
   ⛔ 不自动删。只有 `00x8` 越界 pair 出现工作单才报 `E`。
3. **去重** —— 新增条目之间、新增条目与本 pair 现有台账条目之间的近重复。
   判据是元素名集合 + 归一化文本的 Jaccard，⚠️ 同样只报 `W`。
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

import collect as C                                # noqa: E402
import sources as S                                # noqa: E402

# ⛔ 建模对象边界之外的词。命中只报 W —— 判据是词法，会误伤。
OUT_OF_SCOPE_CUES = [
    (r"\bfork\b|\bjoin\b|分叉|汇合", "并发伪状态（fork / join）"),
    (r"正交|并发|并行|同时活跃|orthogonal|concurrent|parallel|region.*同时", "正交区 / 并发语义"),
    (r"时钟|计时器|clock\b|timer\b|\btimeout\b", "时钟 / 计时器"),
    (r"\d+\s*(秒|毫秒|ms\b|s\b|second)|秒级|毫秒", "时间量"),
    (r"不变式|invariant\b(?!\s*\()", "不变式（$Inv$）"),
    (r"\bwithin\s+\d|在\s*\d+\s*(秒|毫秒)内", "时限约束"),
]

REQUIRED_NEW_FIELDS = ["statement", "layer", "element_of_M", "depth"]
DECISION_FIELD = "裁决"
DEPTH_FIELD = "深度"


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
    new_sigs = []
    for rec in data["new_issues"]:
        nid = rec["id"]
        f = rec["fields"]
        stmt = _text(f.get("statement"))
        if not stmt:
            rep.E(pair, nid, "新增条目无 `statement`")
        for name in ("layer", "element_of_M", "depth"):
            if not _chosen(f.get(name)):
                rep.E(pair, nid, f"新增条目未选 `{name}`")
            elif len(_chosen(f.get(name))) > 1 and name != "element_of_M":
                rep.E(pair, nid, f"新增条目 `{name}` 多选：{_chosen(f.get(name))}")
        layer = (_chosen(f.get("layer")) or [""])[0]
        if layer and layer != "wellformedness" and not _text(f.get("nl_evidence")):
            rep.E(pair, nid,
                  f"`layer = {layer}` 需要 NL 逐字依据，但 `nl_evidence` 为空"
                  "（只有 `wellformedness` 层可以没有）")
        if not _text(f.get("证据(作者源行号)")) and not _text(f.get("证据")):
            rep.W(pair, nid, "未给作者源行号 —— 无行号的主张后续无法复核")
        pp = _text(f.get("primary_predicate"))
        if pp and pp not in S.ALL_PREDICATES:
            rep.E(pair, nid,
                  f"`primary_predicate = {pp}` 不在 19 谓词封闭词表内。"
                  "⭐ 写不出谓词就留空并在理由里写明词表缺口，⛔ 不要造新谓词名")

        # ⛔ 边界
        blob = " ".join([stmt, _text(f.get("nl_evidence")), _text(f.get("direction"))])
        for pattern, label in OUT_OF_SCOPE_CUES:
            if re.search(pattern, blob, flags=re.I):
                rep.W(pair, nid,
                      f"⛔ 疑似越界（{label}）—— project_1 的建模对象 "
                      "$M = (S, E, V, Tr, A)$ 无时钟、无不变式、无正交区。"
                      "⚠️ 词法判据会误伤（元素恰好叫 fork 之类），请人工确认")
                break
        new_sigs.append((nid, stmt, _norm_tokens(stmt)))

    # ---------------------------------------------------------- 去重
    for i in range(len(new_sigs)):
        for j in range(i + 1, len(new_sigs)):
            sim = _jaccard(new_sigs[i][2], new_sigs[j][2])
            if sim >= 0.6:
                rep.W(pair, f"{new_sigs[i][0]}~{new_sigs[j][0]}",
                      f"两条新增条目高度相似（元素/词 Jaccard {sim:.2f}）—— 是不是同一缺陷？")
    for nid, stmt, toks in new_sigs:
        for rid, rec in ledger.items():
            sim = _jaccard(toks, _norm_tokens(rec.get("statement")))
            if sim >= 0.5:
                rep.W(pair, nid,
                      f"与现有台账 `{rid}` 高度相似（Jaccard {sim:.2f}）—— "
                      "若是同一缺陷，应改成对 `" + rid + "` 走「修正」而不是新增")

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
    new_n = len(data["new_issues"])
    summary = data["summary"] or {}
    overall = (_chosen(summary.get("本 pair 整体判断")) or ["—"])[0]
    minutes = _text(summary.get("耗时(分钟)")) or "—"
    done = (ledger_done >= ledger_total and cand_done >= cand_total
            and chk_done >= chk_total and overall != "—")
    started = ledger_done or cand_done or chk_done or new_n or overall != "—"
    status = "🟢" if done else ("🟡" if started else "⚪")
    return {
        "pair": pair, "status": status,
        "ledger": f"{ledger_done}/{ledger_total}",
        "candidates": f"{cand_done}/{cand_total}",
        "checklist": f"{chk_done}/{chk_total}",
        "findings": findings, "new": new_n,
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
        f"校验：{counts['E']} 个 `E`、{counts['W']} 个 `W`。"
    )
    lines.append("")
    lines.append(f"最后刷新：`{datetime.datetime.now().isoformat(timespec='seconds')}`")
    lines.append("")
    lines.append("| pair | 状态 | 台账裁决 | 候选裁决 | 清单已过 | 清单发现 | 新增 | 整体判断 | 耗时(分) |")
    lines.append("| :-- | :-: | --: | --: | --: | --: | --: | :-- | --: |")
    for r in rows:
        lines.append(
            f"| [`{r['pair']}`](./{r['pair']}.md) | {r['status']} | {r['ledger']} | "
            f"{r['candidates']} | {r['checklist']} | {r['findings']} | {r['new']} | "
            f"{r['overall']} | {r['minutes']} |")
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
