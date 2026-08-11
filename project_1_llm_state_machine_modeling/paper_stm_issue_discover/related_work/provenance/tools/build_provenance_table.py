"""生成 19 行出处三类表。

⛔ **只吃经过对抗裁定的证据**，⛔ 不吃原始提取结果 —— 语料层裁定砍掉了 56%，
拿裁定前的数字建表会系统性高估。

三类的判定规则（⛔ 机械部分，⭐ 语义部分仍需人工确认）：

- ⭐ **② 元模型定义性**：⛔ 由人工在 `META_DEFINED` 里写死。⚠️ 这**不能**机械判定 ——
  「这条检查是不是元模型定义的直接后果」是语义判断，⛔ 按 §11 的准入边界，
  它不该做成 validator，只能由人给出并附理由。
- ⭐ **① 有领域证据**：裁定通过的独立来源数 ≥ 下限。
- ⛔ **③ 无外部依据**：既非①也非②。

⚠️ ①与②**可以同时成立**。⭐ 三类表里一条谓词记一类，⛔ 但当一条 ② 类谓词同时有
领域证据时，必须在备注里写出来 —— ⭐ 那让 claim 更硬。

用法：

    python build_provenance_table.py --corpus corpus_final.json --external cd.json \\
        --cd-verdicts cd_verdicts.json --out predicate_provenance.md
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

FAMILY = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S",
    "occupancy_after": "B", "event_consumed": "B", "stays_in": "B",
    "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}

FAMILY_CN = {"S": "结构", "B": "仿真", "P": "有界模型检查"}

#: 【v46 实测】台账断言 / 其中 primary / 已发布支撑 —— 由 `predicate_usage.py` 复算
LEDGER = {
    "event_declared": (7, 4, 490), "variable_declared": (2, 0, 197),
    "initial_target": (26, 14, 185), "state_declared": (15, 7, 131),
    "containment": (19, 10, 116), "action_declared": (6, 6, 114),
    "cardinality": (20, 5, 64), "edge_declared": (9, 7, 25),
    "guard_distinguishable": (13, 5, 15), "effect_declared": (3, 3, 9),
    "occupancy_after": (14, 7, 104), "reaches": (28, 7, 38),
    "event_consumed": (13, 3, 19), "terminates": (15, 4, 18),
    "variable_delta_after": (2, 0, 6), "stays_in": (1, 1, 2),
    "persists_until": (3, 3, 18), "invariant": (0, 0, 4), "response_within": (1, 0, 0),
}

#: ⭐ **② 元模型定义性**：⛔ 恰为 `method_provenance_policy.md` §一.4 点名的那 **6 条**。
#:
#: ⚠️ **⛔ 不得在此增删。** 该文档逐字写明这 6 条承载 966 / 1555 = 62.1% 的已发布支撑
#: （复算：490+197+131+25+114+9 = 966 ✓）。⛔ 静默加第 7 条等于改口径 —— ⭐ 尤其
#: `containment` 曾被归在另一组（「无出处或已被证伪 5 条」），⛔ 把它提到 ② 需要单独裁定。
#:
#: ⚠️ **判据只覆盖「声明性」那一半。** ⭐ 例如 `edge_declared` 的「该迁移是否被声明」由
#: 定义给出，⛔ 而「目标写没写对」是对着 NL 的语义判断 —— ⭐ 后者的正当性来自需求那一句，
#: ⛔ 不来自元模型。⚠️ 这条限定必须写进论文，⛔ 否则 ② 会被读成「这几条不需要任何依据」。
META_DEFINED = {
    "event_declared": "元模型说 Trigger 引用 Event；检查该引用是否有定义是定义的直接后果",
    "variable_declared": "元模型说变量是一类元素；检查模型里用到的量是否被声明是定义的直接后果",
    "state_declared": "元模型说状态是一类元素；检查模型里用到的状态是否被声明是定义的直接后果",
    "edge_declared": "元模型说迁移由 source / target / trigger 构成；检查这三者是否齐备并有定义是定义的直接后果",
    "action_declared": "元模型说状态可带 entry / exit / doActivity；检查动作是否声明并挂在合法相上是定义的直接后果",
    "effect_declared": "元模型说迁移可带 effect；检查效果是否声明是定义的直接后果",
}

MIN_SOURCES = 3
TARGET_SOURCES = 6


def _domain_diversity_ok(n_sources: int, n_domains: int) -> bool:
    return n_domains >= min(3, n_sources)


#: ⛔ 裁定者逐条点名的**扣分项**，⛔ 必须与数字同时出现 —— ⚠️ 否则读者会按面值读。
#: ⭐ 这些是**语义判断的产物**，⛔ 机械聚合看不到（它只会数不同的 identifier）。
KNOWN_CAVEATS = {
    "response_within": (
        "⛔ **对应关系有一处系统性缺口**：文献里的 Response 模式几乎一律是**无界** eventually "
        "（`G(p → F q)`），⛔ 而本谓词的界是**步数**。⚠️ 裁定者在多条上反复记「我方谓词的"
        "『有界步数』这一要素引文里没有」。⭐ 真正带步数界的只有少数几条（如「before the next "
        "tick is consumed」）。⛔ 论文里不得把无界 Response 的普遍性直接转给有界形式"
    ),
    "persists_until": (
        "⚠️ **同源折扣**：多条出自同一作者组的同一微波炉案例（SoSyM 论文与 Sismic 工具），"
        "⛔ 不算独立观测"
    ),
    "invariant": (
        "⚠️ **同源折扣**：Dwyer 系模式目录的多条已按 DOI 归一为一个来源；⛔ 另有若干条出自"
        "同一作者组。⭐ 但本条的量化工业证据（VTT 3923 条工业性质、Ford 三个量产控制器）确实互相独立"
    ),
    "terminates": (
        "⛔ **只硬证了谓词定义的一半**：17 条候选里 10 条用 **deadlock-freedom** 顶替，⛔ 已被裁定"
        "改判或拒收。⭐ 裁定者指出这暴露的是**词表缺一条进展类谓词**（决定性反证：RoboTool 把"
        " termination 与 deadlock freedom 做成**两条不同断言**，且对某些系统明确期望「不终止」"
        "而同时要求无死锁）。⛔ 见 [SUMMARY.md](./SUMMARY.md) §4.5.1"
    ),
    "containment": (
        "⛔ **文献侧 0/6，且失败是结构性的**：裁定者逐字「`containment` 的『正确』需要**外部规约"
        "作参照**，⛔ 而语言层良构性规则**天生给不出**『这个子态该挂在谁下面』」。⛔ 见 §4.5.2"
    ),
    "cardinality": (
        "⛔ **两轮 15 条全数不通过。** ⭐ 决定性判据：本谓词的特征在 **N 的出处是需求文本**，"
        "⛔ 而 15 条的 N 全部来自语言 / 元模型 / 作者策略。⭐ 可落稿的表述见 §4.1"
    ),
    "variable_declared": (
        "⚠️ **词表形状待确认**：`state_declared` 明写「缺失**或多余**」而本条没写，⛔ 而证据里有"
        "多条落在「已声明但未使用」方向。⭐ 是笔误还是设计选择，交 R1"
    ),
    "variable_delta_after": (
        "⚠️ **恰好 3 源，⛔ 踩在下限上**；⛔ 且**界内语料侧为 0** —— ⭐ 全部来自文献"
    ),
    "event_declared": (
        "⚠️ **仅 3 源，⛔ 踩在下限上**。⭐ 但它是 ② 类，⛔ 不靠这个成立"
    ),
}


_DOI = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
_ARXIV = re.compile(r"(?:arxiv[:\s/]*)?(\d{4}\.\d{4,5})", re.I)


def canonical_source(finding: dict) -> str:
    """一篇论文一个键。⛔ 与 `aggregate_evidence.canonical_source` 必须同口径 ——
    ⚠️ 两处不一致会让总账与逐条表报出不同的来源数。"""
    ident = finding.get("identifier") or ""
    m = _DOI.search(ident)
    if m:
        return "doi:" + m.group(0).rstrip(".,;)").lower()
    if "arxiv" in ident.lower():
        m = _ARXIV.search(ident)
        if m:
            return "arxiv:" + m.group(1)
    m = re.search(r"https?://([^\s?#]+)", ident)
    if m:
        return "url:" + m.group(1).rstrip("/.,;").lower()
    if ident.strip():
        return "raw:" + re.sub(r"\s+", " ", ident.strip()).lower()[:120]
    return "title:" + re.sub(r"[^a-z0-9]+", " ", (finding.get("title") or "").lower()).strip()


def _load(path: Path | None) -> list:
    if path and path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return []


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--corpus", type=Path, required=True, help="裁定后的语料层证据")
    p.add_argument("--external", type=Path, required=True, help="⭐ **已裁定通过**的外部证据（consolidate 的产物）")
    p.add_argument("--unjudged", type=int, default=0, help="尚未裁定、故未计入的外部证据条数（如实写进表注）")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args(argv)

    corpus = _load(args.corpus)
    kept_ext = _load(args.external)

    real: dict[str, dict[str, str]] = defaultdict(dict)
    for f in corpus:
        real[f["predicate"]][f["directory"]] = f.get("domain", "?")
    lit: dict[str, dict[str, dict]] = defaultdict(dict)
    for f in kept_ext:
        lit[f["predicate"]][canonical_source(f)] = f

    lines = [
        "# 19 条谓词的出处三类分级",
        "",
        "> ⛔ **本表只收经过对抗裁定的证据。** ⚠️ 语料层 315 → 143（**45%**）、文献层 269 → "
        f"{len(kept_ext)}（⛔ 另剔除 9 条自证式取证" + (f"，⚠️ 另有 {args.unjudged} 条尚未裁定、**未计入**" if args.unjudged else "") + "）"
        " —— ⛔ 拿裁定前的数字建表会系统性高估。裁定判据与可靠性审计见 [methodology.md](./methodology.md)。",
        "",
        "> **档位标记**：分类与来源数为【实测】；「② 的理由」列为【AI 建议·待确认】，⛔ 须人工确认。",
        "",
        "## ⛔ 三类的含义（⭐ 权威定义在 "
        "[method_provenance_policy.md](../../discover_matrix/docs/protocol/method_provenance_policy.md) §一.4）",
        "",
        "| 类 | 含义 | ⭐ 论文里怎么说 |",
        "| :-- | :-- | :-- |",
        "| ⭐ **①** | 有领域证据 —— 该检查在真实控制系统的建模实践与领域文献中**反复出现** | 「这类检查在 … 中反复出现，我们把主流的这些归纳成一套闭合词表」 |",
        "| ⭐ **②** | 元模型定义性 —— ⭐ **该检查在定义上就成立，⛔ 不需要外部出处** | 「其判据由元模型定义直接给出」 |",
        "| ⛔ **③** | 无外部依据 | ⛔ 在 Limitations 明写一句，⛔ 不隐瞒、⛔ 也不删谓词（588 冻结） |",
        "",
        "⛔ **三类不是强度序。** ① 与 ② 谁也不高于谁 —— ⭐ 它们回答的是不同问题。",
        "",
        "## 逐条表",
        "",
        "| 谓词 | 族 | 台账断言 | 其中 primary | 已发布支撑 | ⭐ 分类 | 界内真实系统 | 文献 | 语料领域 | 备注 |",
        "| :-- | :-- | --: | --: | --: | :-: | --: | --: | :-- | :-- |",
    ]

    counts = {"①": 0, "②": 0, "③": 0}
    rows_meta = []
    for pred, fam in sorted(FAMILY.items(), key=lambda kv: (kv[1], -LEDGER[kv[0]][2])):
        nr, nl = len(real.get(pred, {})), len(lit.get(pred, {}))
        total = nr + nl
        doms = sorted(set(real.get(pred, {}).values()))
        is_meta = pred in META_DEFINED
        has_domain = total >= MIN_SOURCES
        cls = "②" if is_meta else ("①" if has_domain else "③")
        counts[cls] += 1
        note = []
        if is_meta and has_domain:
            note.append(f"⭐ 同时有 **{total}** 个领域证据来源 —— ⭐ 让 claim 更硬，⛔ 但它**不必**靠这个成立")
        if not has_domain and not is_meta:
            note.append("⛔ 未达 3 源下限")
        elif total < TARGET_SOURCES and not is_meta:
            note.append(f"⚠️ **{total}** 源，⛔ 未达 6 源目标档")
        if not _domain_diversity_ok(nr, len(doms)):
            note.append(f"⚠️ 语料侧只覆盖 **{len(doms)}** 个领域，⛔ 主张须限定或靠文献侧补")
        if pred in KNOWN_CAVEATS:
            note.append(KNOWN_CAVEATS[pred])
        a, pri, pub = LEDGER[pred]
        lines.append(
            f"| `{pred}` | {FAMILY_CN[fam]} | {a} | {pri} | {pub} | **{cls}** | "
            f"{nr} | {nl} | {' '.join(doms) if doms else '—'} | {'；'.join(note) if note else '—'} |"
        )
        rows_meta.append({"predicate": pred, "cls": cls, "real": nr, "lit": nl, "total": total})

    lines += [
        "",
        f"**三类计数**：⭐ ① **{counts['①']}** 条 · ⭐ ② **{counts['②']}** 条 · ⛔ ③ **{counts['③']}** 条。",
        "",
        "⚠️ ⭐ **② 类谓词的「界内真实系统 / 文献」列不是它成立的依据** —— ⭐ 它由定义支撑。"
        "⛔ 那两列在此只说明「这类检查在领域里同样常见」，⭐ 是加分不是必需。",
        "",
        "## ⭐ ② 类的逐条理由（⛔ 人工判定，⚠️ 须确认）",
        "",
        "| 谓词 | ⭐ 为什么它由元模型定义直接给出 |",
        "| :-- | :-- |",
    ]
    for pred, why in META_DEFINED.items():
        lines.append(f"| `{pred}` | {why} |")

    lines += ["", "## 更新日志", "",
              "| 时间 | 内容 |", "| :-- | :-- |",
              "| 2026-08-12 | 建立。由 `build_provenance_table.py` 从**裁定后**的证据生成。 |", ""]

    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"写出 {args.out}")
    print(f"三类计数：① {counts['①']} · ② {counts['②']} · ③ {counts['③']}")
    for r in rows_meta:
        print(f"  {r['predicate']:24s} {r['cls']}  真实系统 {r['real']:>3}  文献 {r['lit']:>3}  合计 {r['total']:>3}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
