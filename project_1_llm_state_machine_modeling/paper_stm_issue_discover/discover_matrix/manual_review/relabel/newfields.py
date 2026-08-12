"""§5 新增 issue 的**字段定义、填写模板、填写指引与脚本推导**。

⭐ 字段分三层，⛔ 人工只填第一层：

| 层 | 字段 |
| :-- | :-- |
| ⭐ 人工必填（5） | `statement` · `generated_side` · `nl_evidence` · `direction` · `depth` |
| ⚠️ 人工可选（3） | `reference_side` · `primary_predicate` · `layer` |
| ⭐ 脚本推导（其余） | `id` · `pair` · `group` · `llm` · `in_scope` · `element_of_M` · `expressible_with_closed_vocabulary` · `assertions` · `assertion_count` · `upstream` · `homogeneity_*` · `automatable` … |

⛔ **为什么不让人填 `element_of_M`**：它是对 `generated_side` 已经点到的那一处做**分类**，
不带新信息。实测台账里同一个 `direction` 会落到 3 到 5 种不同的 `element_of_M`
（`guard` 方向就横跨 `Tr` / `A` / `S` / `E` / `V` 五种），说明手填只会引入噪声。
本模块的 `derive()` 改从**作者源行号**反查那一行是状态声明、迁移还是状态动作，
⭐ 那是确定性的。

⛔ **为什么 `direction` / `depth` / `layer` 的取值不许自造**：它们是台账现有条目已经在用的
分类轴，新增条目若另起一套取值，重标结果就无法与既有 98 条并表统计。
枚举来源是台账实际用过的取值（见 `direction_counts()`），⛔ 不是拍脑袋定的。

⚠️ **样例全部取自 [expected_issue_set.json](../expected_issue_set.json) 的真实条目**，
⛔ 一条都没有编。⭐ 但选样例时会**避开当前 pair 所属的 NL 组** —— 同一份 NL 生成 6 个制品，
拿兄弟 pair 的缺陷当格式样例等于把答案先告诉作者。见 `exemplar()`。
"""

from __future__ import annotations

import re

import sources as S

# ------------------------------------------------------------------ 枚举

# ⭐ 取值来自台账 REPORTABLE 98 条实际用过的 `direction`（见 `direction_counts()`）。
# ⚠️ 全 126 条里还有第 9 个取值 `pseudostate`（9 条），但它**全部落在 `00x8` 越界 pair**
# 上 —— 那 6 个 pair 的 fork/join 伪状态不在 $M$ 内，故本轮不设该取值。
# ⭐ 实在归不进这 8 类的写 `unclassified`，⛔ 不要造新取值。
DIRECTIONS = [
    "reachability", "hierarchy", "guard", "entry",
    "effect_action", "event", "cardinality", "unclassified",
]

DEPTHS = ["表层", "中层", "深层"]

LAYERS = list(S.LAYERS)          # wellformedness / nl_named / over_specification / nl_contradiction

REQUIRED_FIELDS = ["statement", "generated_side", "nl_evidence", "direction", "depth"]
OPTIONAL_FIELDS = ["reference_side", "primary_predicate", "layer"]

# ⭐ 只有这些名字能在填写块里起一个新字段。⛔ 其余带冒号的行一律并进当前字段 ——
# 否则作者在 `statement` 里写「NL 第 3 句：…」就会被解析器当成新字段名而截断。
FIELD_NAMES = REQUIRED_FIELDS + OPTIONAL_FIELDS

# ⭐ 只有这三个是勾选行；其余一律读成自由文本。
# ⛔ 这条是硬的：`generated_side` 的值里几乎必然出现 `[*]`（PlantUML 的伪状态写法），
# 若把它当勾选行解析，值会变成空的零选项勾选行 —— 入口类缺陷会整类丢失。
CHOICE_FIELDS = ["direction", "depth", "layer"]

# ⭐ 显式的「已判定为无」标记。⛔ 留空 = 没填；写 `无` = 判过了，结论是没有。
NONE_MARKS = ("无", "none", "None", "N/A", "n/a", "—", "-")

SEPARATOR = "--- 以上 5 项必填 · 以下 3 项可留空 ---"


def is_none_mark(text):
    return (text or "").strip() in NONE_MARKS


# ------------------------------------------------------------------ 填写模板

def _choice_line(name, options):
    return f"{name}: " + "  ".join(f"[ ] {o}" for o in options)


def entry_template(pair, index):
    return "\n".join([
        f"### NEW-{pair}-{index:02d}",
        "statement:",
        "generated_side:",
        "nl_evidence:",
        _choice_line("direction", DIRECTIONS),
        _choice_line("depth", DEPTHS),
        SEPARATOR,
        "reference_side:",
        "primary_predicate:",
        _choice_line("layer", LAYERS),
    ])


def template(pair, count=2):
    return "\n\n".join(entry_template(pair, i) for i in range(1, count + 1))


# ------------------------------------------------------------------ 台账统计（供指引正文用）

def direction_counts():
    from collections import Counter
    return Counter(r["direction"] for r in S.ledger_records(reportable_only=True))


def layer_counts():
    from collections import Counter
    return Counter(r["layer"] for r in S.ledger_records(reportable_only=True))


def layer_basis_table():
    """台账里每个 `layer` 对应的 `layer_basis` 原话。⭐ 这就是分层判据的真源。"""
    out = {}
    for r in S.ledger_records(reportable_only=True):
        out.setdefault(r["layer"], r["layer_basis"])
    return out


def nl_evidence_empty_count():
    recs = S.ledger_records(reportable_only=True)
    return sum(1 for r in recs if not (r.get("nl_evidence") or "").strip()), len(recs)


def no_primary_predicate_count():
    recs = S.ledger_records(reportable_only=True)
    return sum(1 for r in recs if not r.get("primary_predicate")), len(recs)


# ------------------------------------------------------------------ 样例挑选

# ⭐ 每个字段给一串候选台账 id，按序取**第一个不属于当前 pair 所在 NL 组**的。
# ⛔ 候选必须横跨至少两个 NL 组，否则某些 pair 会挑不到样例
# （`test_every_exemplar_slot_resolves_off_group` 钉住这一点）。
EXEMPLARS = {
    "statement": ["EIS-0040-01", "EIS-0029-01", "EIS-0002-03", "EIS-0009-01", "EIS-0036-02"],
    "generated_side": ["EIS-0042-01", "EIS-0034-01", "EIS-0035-02", "EIS-0029-01", "EIS-0046-01"],
    "nl_evidence": ["EIS-0046-02", "EIS-0014-04", "EIS-0035-03", "EIS-0024-01", "EIS-0009-01"],
    "nl_evidence_empty": ["EIS-0000-01", "EIS-0046-01", "EIS-0010-01", "EIS-0002-03"],
    "reference_side": ["EIS-0029-01", "EIS-0009-01", "EIS-0034-01", "EIS-0046-01"],
}


def _by_id():
    return {r["id"]: r for r in S.ledger_records(reportable_only=True)}


def exemplar(slot, pair):
    """取该 slot 的样例记录，⛔ 跳过与 `pair` 同一份 NL 的条目。取不到返回 `None`。"""
    mine = S.nl_group(pair)
    index = _by_id()
    for rid in EXEMPLARS.get(slot, []):
        rec = index.get(rid)
        if rec is None:
            continue
        if S.nl_group(rec["pair"]) == mine:
            continue
        return rec
    return None


# ------------------------------------------------------------------ 脚本推导

# 结构族（S 族）谓词到 $M$ 分量的确定性映射。
# ⛔ 行为族（B）与性质族（P）谓词**不在表内** —— `reaches` / `occupancy_after` 这类
# 说的是运行时落点，落在哪个分量上取决于主张本身，⛔ 不能由谓词名单独判定。
PREDICATE_TO_ELEMENT = {
    "state_declared": "S",
    "containment": "S",
    "cardinality": "S",
    "event_declared": "E",
    "variable_declared": "V",
    "edge_declared": "Tr",
    "initial_target": "Tr",
    "guard_distinguishable": "Tr",
    "effect_declared": "A",
    "action_declared": "A",
}

_RE_LINE_REF = re.compile(r"(?::|第\s*|行\s*|[Ll])\s*(\d{1,4})\s*(?:行)?")


def line_kinds(model):
    """作者源每一行属于 $M$ 的哪个分量。⭐ 只覆盖能唯一判定的三类。"""
    kinds = {}
    for st in model.states.values():
        if st.decl_line:
            kinds[st.decl_line] = "S"
        for ln, _txt in st.descriptions:
            kinds[ln] = "A"
    for tr in model.transitions:
        kinds[tr.line] = "Tr"
    return kinds


def parse_line_refs(text):
    """从 `generated_side` 里抠出作者源行号。支持 `:12` / `第 12 行` / `L12`。"""
    if not text:
        return []
    return sorted({int(m.group(1)) for m in _RE_LINE_REF.finditer(text)})


def derive_element_of_M(pair, generated_side, primary_predicate=None):
    """推导 `element_of_M`。返回 `(值 或 None, 依据说明)`。

    ⭐ 顺序：① `generated_side` 给了作者源行号 → 查那一行是什么；
    ② 没给行号但有结构族 `primary_predicate` → 查映射表；
    ⛔ 都不成立就返回 `None` ——「推不出来」必须显形，⛔ 不许猜一个填上。
    """
    from pumlmodel import PumlModel

    refs = parse_line_refs(generated_side)
    if refs:
        model = PumlModel(S.puml_text(pair), pair)
        kinds = line_kinds(model)
        hit = {kinds[n] for n in refs if n in kinds}
        if len(hit) == 1:
            n = [x for x in refs if x in kinds]
            return hit.pop(), f"作者源第 {n} 行的行类型"
        if len(hit) > 1:
            return "多个", f"作者源第 {refs} 行横跨 {sorted(hit)}"
    if primary_predicate and primary_predicate in PREDICATE_TO_ELEMENT:
        return (PREDICATE_TO_ELEMENT[primary_predicate],
                f"结构族谓词 `{primary_predicate}` 的确定性映射")
    return None, (
        "⛔ 推不出 —— `generated_side` 未给作者源行号，"
        "且 `primary_predicate` 为空或属行为 / 性质族（其分量取决于主张本身）"
    )


# ⛔ 这些字段本轮**推不出来**，必须留到合并回台账那一步。
# ⭐ 列出来是为了让「脚本推导」是一句可核对的话，而不是一句托辞。
PENDING_AT_MERGE = {
    "assertions": "要由断言生成器对 statement 产出，本目录不产断言",
    "assertion_count": "同上，随 `assertions` 一起产生",
    "has_negative_control": "同上",
    "replay": "要真跑一遍谓词才有 verdict / value",
    "verdict": "合并时由裁定给出，⛔ 不由重标者自封",
    "homogeneity_group": "要在全库范围内重算同质组，单 pair 内算不了",
    "homogeneity_group_size": "同上",
    "homogeneity_groupable": "同上",
    "automatable": "取决于 `assertions` 是否可执行",
    "layer_basis": "由 `layer` 定值套写（见 `layer_basis_table()`），layer 留空则待定",
    "decided_by": "本轮固定为人工重标，合并时统一写入",
}


def derive(pair, nid, fields):
    """把人工填的 8 个字段补成一条**接近台账形态**的记录。

    ⛔ 这不是「合并回台账」—— 它只把当下能确定的部分算出来，
    剩下的列在 `pending` 里，⛔ 不留空白假装齐了。
    """
    def txt(name):
        v = fields.get(name)
        return v.strip() if isinstance(v, str) else ""

    def one(name):
        v = fields.get(name)
        ch = v.get("chosen") if isinstance(v, dict) else None
        return ch[0] if ch else None

    pp = txt("primary_predicate")
    pp = None if (not pp or is_none_mark(pp)) else pp
    elem, basis = derive_element_of_M(pair, txt("generated_side"), pp)
    layer = one("layer")
    return {
        "id": nid,
        "pair": pair,
        "group": S.nl_group(pair),
        "llm": S.source_meta(pair).get("llm"),
        "in_scope": True,
        "element_of_M": elem,
        "element_of_M_basis": basis,
        "expressible_with_closed_vocabulary": pp is not None,
        "layer_basis": layer_basis_table().get(layer) if layer else None,
        "upstream": {
            "source": "manual_relabel",
            "worksheet": f"{pair}.md",
            "fill_key": f"NEW-{pair}",
            "entry": nid,
        },
        "pending": dict(PENDING_AT_MERGE),
    }
