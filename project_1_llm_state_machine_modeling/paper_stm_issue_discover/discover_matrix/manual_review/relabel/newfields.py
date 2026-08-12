"""§5 新增 issue 的**字段定义、填写模板、填写指引与脚本推导**。

⭐ 登记块按**三层**组织。三层不是三种详略，是三个**互相独立、必须分开回答**的问题：

| 层 | 问题 | 字段 |
| :-- | :-- | :-- |
| ① 事实层 | ⭐ 你**看到了什么**（⛔ 只描述现象，不下判断），在**哪一处** | `statement` · `generated_side` |
| ② 依据层 | ⛔ **凭什么**说它是缺陷 | `basis` · `nl_evidence`（+ 可选 `reference_side` · `layer`） |
| ③ 边界层 | ⛔ 它在 $M = (S, E, V, Tr, A)$ **内**吗 | `scope` |
| ④ 分类轴 | 并表统计用（⛔ 不是新的一层） | `direction` · `depth`（+ 可选 `primary_predicate`） |

⛔ **为什么依据层要单列 `basis` 而不是复用 `layer`**：台账的 `layer` 是按**缺陷种类**分的
（缺失 / 凭空多出 / 与义务矛盾 / 良构性），却被同时当成**依据来源**的轴在用 —— ⚠️ 而这两件事
并不同构。看 `layer_basis()` 的原话就清楚：`wellformedness` 与 `over_specification` 一个字
不提 NL，`nl_named` 与 `nl_contradiction` 要求 NL 逐字依据；⛔ **而四层里没有任何一个槽位
对应「依据来自参考模型」**，尽管 [README.md](./README.md) §二.3 已声明参考模型**不是正确
答案**、这类依据单独不足以支撑一条缺陷。于是一条真实依据只在参考侧的记录，只能被硬塞进四层
中的某一层，⛔ 塞进哪一层全看写的人怎么想 —— **依据强度就此丢失，且丢得不留痕迹**。
四种依据的强度序：`模型自身` ≥ `NL显式义务` > `NL欠指定` > `参考模型`，
⭐ 分开记之后，「这条依据够不够硬」才第一次成为可查询的字段。

⚠️ **这段 rationale 2026-08-13 换过例子。** 旧版把 `EIS-0005-02` 立成「参考模型依据被误记成
`nl_contradiction`」的教科书案例，⛔ 而那个推论**不成立** —— 该记录的论证引的是 NL 第 4/5/6/8
句的互斥性，⛔ 「NL 零处提及包含关系」推不出「依据不在 NL 上」。⭐ 分层设计本身是对的，
⛔ 但它不需要、也不该靠一个立不住的案例来支撑。详见 [README.md](./README.md) §7.1。

⛔ **为什么边界层要单列 `scope` 而不是靠词法拦**：判读者发现的若是时钟 / 不变式 / 并发
问题，那**不是缺陷、也不是漏判**，而是**不在建模对象内**（CLAUDE.md「研究内容一的建模
对象边界」）。它必须能被登记下来（那本身是关于语料的事实），但**不得计入缺陷统计**。
⚠️ 词法关键词只能提醒，⛔ 不能代替这个判断：`generated_side` 里引用一行标签写着
`After (2 s)` 的迁移，不使主张越界；反过来一条不含任何关键词的主张也可能需要并发语义。

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

# ------------------------------------------------------------------ ② 依据层

# ⭐ 四种依据，⛔ **强度不同**，⛔ 不许合并成一个「有没有依据」的布尔。
# ⚠️ 取值里不许出现空格、`/`、`,`、`、` —— `validate._enum_values` 会按这些字符
# 切自由文本写法，取值含分隔符会被切成两个值而报「单值字段却给了两个」。
BASES = ["NL显式义务", "NL欠指定", "模型自身", "参考模型"]

BASIS_MEANING = [
    ("NL显式义务",
     "NL 里有一句**说清楚了**的义务（源状态 / 触发 / 目标 / 守卫 中该有的都有），"
     "而模型没做到。⭐ 这是最硬的 NL 依据，⛔ 必须给出段 id。"),
    ("NL欠指定",
     "NL 里**有**相关句子，⛔ 但那句话把关键槽位空着（不写源状态 / 不写触发 / "
     "并列项无连接词 / 无情态动词），因此它**支撑不起「模型违反了它」**。"
     "⭐ 仍然登记，⛔ 但结论只能写成「原文未规定，模型自行选择了一种读法」，"
     "⛔ 不得写成「违反」。见 [README.md](./README.md) §7.2 的七种欠指定形态。"),
    ("模型自身",
     "⭐ 不看 NL、不看参考模型，只读作者源就能判定（良构性）—— "
     "如引用了未声明的元素、复合态无区域初始边、吸收态。⭐ `nl_evidence` 写 `无` 即可。"),
    ("参考模型",
     "⛔ **只有**参考模型那样建、生成侧没那样建。⚠️ 参考模型**不是正确答案**"
     "（§1.4 与 README §二.3），⛔ 故这一种依据**单独不足以**支撑一条缺陷；"
     "⭐ 选它等于说「本条待裁定」，请在 `statement` 里写明还缺什么才站得住。"),
]

NL_BASED_BASES = ("NL显式义务", "NL欠指定")

# ⭐ **按台账自己的 `layer_basis` 原话**，需要 NL 逐字依据的只有这两层：
# `nl_named` = 「NL 点名了那个缺失或错位的元素」、`nl_contradiction` = 「与 NL 的显式义务矛盾」。
# ⛔ 另两层不需要：`wellformedness` = 「模型自身即可判定，不需要 NL 也不需要参考模型」，
# `over_specification` = 「生成方凭空多出，且造成可断言的负面后果」—— ⚠️ 后者一个字都没提 NL，
# 且 REPORTABLE 98 条里它的 6 条**有 5 条 `nl_evidence` 为空**，那是设计如此，不是漏填。
# ⛔ 把 `over_specification` 也当成需要 NL 依据，会造出一个**不可满足**的门（CLAUDE.md §13）。
NL_GROUNDED_LAYERS = ("nl_named", "nl_contradiction")

# ⭐ `basis` → `layer` 的**已知**对应。⛔ 不是双射：`NL显式义务` 既可能落 `nl_named`
# （NL 点名了缺失元素）也可能落 `nl_contradiction`（与显式义务矛盾），故只给提示。
BASIS_TO_LAYER = {
    "模型自身": (None, "⭐ 通常落 `wellformedness`（模型自身即可判定，不需要 NL 也不需要"
                      "参考模型）；⭐ 若主张的是「生成方凭空多出一个元素、且造成可断言的"
                      "负面后果」，则落 `over_specification` —— ⭐ 那一层同样**不要求** "
                      "NL 依据，`nl_evidence` 照写 `无`"),
    "NL显式义务": (None, "⭐ 视主张形态落 `nl_named`（NL 点名了那个缺失或错位的元素）"
                        "或 `nl_contradiction`（与 NL 的显式义务矛盾）"),
    "NL欠指定": (None, "⛔ **不得**落 `nl_contradiction` —— 欠指定的句子不构成显式义务，"
                      "谈不上与它矛盾"),
    "参考模型": (None, "⛔ 台账四层**没有**「参考模型依据」这一层 —— ⚠️ 这类记录只能被硬塞进"
                      "某一层，依据强度就此丢失。⭐ 建议把 `layer` 留空（等于「本条待裁定」），"
                      "⛔ 尤其**不得**记成 `nl_contradiction`：参考模型不是 NL"),
}

# ------------------------------------------------------------------ ③ 边界层

# ⭐ 越界不是缺陷、也不是漏判，而是「不在建模对象内」。⛔ 取值同样不许含分隔符。
IN_SCOPE_VALUE = "界内"
SCOPES = [IN_SCOPE_VALUE, "越界·时钟或不变式", "越界·并发或正交区", "越界·其他"]

SCOPE_MEANING = [
    (IN_SCOPE_VALUE,
     "⭐ 主张只涉及 $S$ / $E$ / $V$ / $Tr$ / $A$ —— 状态、事件、变量、迁移、动作与层次。"),
    ("越界·时钟或不变式",
     "⛔ 主张成立与否需要时钟变量 $C$ 或状态不变式 $Inv$："
     "「N 秒后应当迁移」「该状态最长驻留 T」「进入时须满足某不变式」。"),
    ("越界·并发或正交区",
     "⛔ 主张需要并发语义：fork / join 伪状态、「两个区域是否同时活跃」、区间同步。"),
    ("越界·其他",
     "⚠️ 确属 $M$ 之外但不属上面两类。⛔ 请在 `statement` 里写清越在哪里 —— "
     "这一档若堆积，说明边界定义本身需要复查。"),
]


def is_out_of_scope(value):
    """⭐ 该 `scope` 取值是不是「越界」。⛔ 判据是前缀，不是关键词命中。"""
    return bool(value) and str(value).startswith("越界")


# ------------------------------------------------------------------ 字段清单

# ⭐ 必填 7 项里有 **5 项是勾选**（`basis` `scope` `direction` `depth` 与可选的 `layer`），
# ⛔ 真正要动笔写的只有 `statement` / `generated_side` / `nl_evidence` 三项，
# 且 `nl_evidence` 在 `basis = 模型自身` 时写一个 `无` 就够。
REQUIRED_FIELDS = ["statement", "generated_side", "basis", "nl_evidence",
                   "scope", "direction", "depth"]
OPTIONAL_FIELDS = ["reference_side", "primary_predicate", "layer"]

# ⭐ 只有这些名字能在填写块里起一个新字段。⛔ 其余带冒号的行一律并进当前字段 ——
# 否则作者在 `statement` 里写「NL 第 3 句：…」就会被解析器当成新字段名而截断。
FIELD_NAMES = REQUIRED_FIELDS + OPTIONAL_FIELDS

# ⭐ 只有这些是勾选行；其余一律读成自由文本。
# ⛔ 这条是硬的：`generated_side` 的值里几乎必然出现 `[*]`（PlantUML 的伪状态写法），
# 若把它当勾选行解析，值会变成空的零选项勾选行 —— 入口类缺陷会整类丢失。
CHOICE_FIELDS = ["basis", "scope", "direction", "depth", "layer"]

# ⛔ **越界条目不要求填分类轴与依据层** —— 它不是缺陷，谈「缺陷方向」「依据强度」
# 没有意义，硬要求只会逼判读者瞎勾一个。⭐ 越界条目只需事实层 + `scope`。
REQUIRED_WHEN_OUT_OF_SCOPE = ["statement", "generated_side", "scope"]

# ⭐ 显式的「已判定为无」标记。⛔ 留空 = 没填；写 `无` = 判过了，结论是没有。
NONE_MARKS = ("无", "none", "None", "N/A", "n/a", "—", "-")


def is_none_mark(text):
    return (text or "").strip() in NONE_MARKS


# ------------------------------------------------------------------ 填写模板

# ⭐ 分层小标题。⛔ 它们**不是字段** —— `collect.parse_fields` 按本清单逐字剔除，
# 否则紧跟在 `generated_side:` 之后的那一行会被并进 `generated_side` 的值里。
# ⚠️ 因此这里**不许出现半角冒号**：`fillblocks.is_untouched` 用 `":" in line` 判
# 「冒号后写了东西」，半角冒号会让空模板被误判成已填。
SEP_FACT = "--- ① 事实层 · 看到了什么（⛔ 只写现象，不下判断） ---"
SEP_BASIS = "--- ② 依据层 · 凭什么说它是缺陷（⭐ basis 决定 nl_evidence 怎么写） ---"
SEP_SCOPE = "--- ③ 边界层 · 它在 M = (S, E, V, Tr, A) 内吗 ---"
SEP_AXIS = "--- ④ 分类轴 · 并表统计用（⛔ 越界条目可不填） ---"
SEP_OPTIONAL = "--- ⑤ 以下三项可留空 ---"

SEPARATORS = [SEP_FACT, SEP_BASIS, SEP_SCOPE, SEP_AXIS, SEP_OPTIONAL]


def _choice_line(name, options):
    return f"{name}: " + "  ".join(f"[ ] {o}" for o in options)


def entry_template(pair, index):
    return "\n".join([
        f"### NEW-{pair}-{index:02d}",
        SEP_FACT,
        "statement:",
        "generated_side:",
        SEP_BASIS,
        _choice_line("basis", BASES),
        "nl_evidence:",
        SEP_SCOPE,
        _choice_line("scope", SCOPES),
        SEP_AXIS,
        _choice_line("direction", DIRECTIONS),
        _choice_line("depth", DEPTHS),
        SEP_OPTIONAL,
        "reference_side:",
        "primary_predicate:",
        _choice_line("layer", LAYERS),
    ])


def template(pair, count=2):
    return "\n\n".join(entry_template(pair, i) for i in range(1, count + 1))


# ⛔ 历史模板（8 字段、无三层结构）。⭐ 留着**只为识别「原样未填的旧块」**：
# 幂等注回是按 key 做的，若不认出旧模板，字段表改版后旧骨架会被当成「人工内容」
# 永久保留，三层字段永远出不来。⚠️ 只做逐字全等匹配（见 `fillblocks.is_stale_template`）。
def template_v2(pair, count=2):
    def one(index):
        return "\n".join([
            f"### NEW-{pair}-{index:02d}",
            "statement:",
            "generated_side:",
            "nl_evidence:",
            _choice_line("direction", DIRECTIONS),
            _choice_line("depth", DEPTHS),
            "--- 以上 5 项必填 · 以下 3 项可留空 ---",
            "reference_side:",
            "primary_predicate:",
            _choice_line("layer", LAYERS),
        ])
    return "\n\n".join(one(i) for i in range(1, count + 1))


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


def field_value(fields, name):
    """取一个字段的**单值**：勾选行取第一个勾选项，自由文本行取整串。取不到返回 `None`。"""
    v = fields.get(name)
    if isinstance(v, dict):
        ch = v.get("chosen") or []
        return ch[0] if ch else None
    if isinstance(v, str):
        return v.strip() or None
    return None


def derive(pair, nid, fields):
    """把人工填的 10 个字段补成一条**接近台账形态**的记录。

    ⛔ 这不是「合并回台账」—— 它只把当下能确定的部分算出来，
    剩下的列在 `pending` 里，⛔ 不留空白假装齐了。
    """
    def txt(name):
        v = fields.get(name)
        return v.strip() if isinstance(v, str) else ""

    pp = txt("primary_predicate")
    pp = None if (not pp or is_none_mark(pp)) else pp
    elem, elem_basis = derive_element_of_M(pair, txt("generated_side"), pp)
    layer = field_value(fields, "layer")
    basis = field_value(fields, "basis")
    scope = field_value(fields, "scope")
    oos = is_out_of_scope(scope)

    # ⛔ 越界条目**不计入缺陷统计**。⭐ 它仍然落盘 —— 「这份语料要求了 $M$ 之外的东西」
    # 本身是关于语料的事实，⛔ 丢掉它等于把边界问题伪装成「没人发现」。
    out = {
        "id": nid,
        "pair": pair,
        "group": S.nl_group(pair),
        "llm": S.source_meta(pair).get("llm"),
        "in_scope": (not oos) if scope else None,
        "counts_as_defect": (not oos) if scope else None,
        "boundary_ruling": "out_of_scope" if oos else None,
        "boundary_effect": (f"⛔ 不计入缺陷统计（人工重标标为「{scope}」）"
                            if oos else None),
        "boundary_ruled_by": "manual_relabel" if oos else None,
        "basis": basis,
        "element_of_M": elem,
        "element_of_M_basis": elem_basis,
        "expressible_with_closed_vocabulary": pp is not None,
        "layer_basis": layer_basis_table().get(layer) if layer else None,
        "layer_hint_from_basis": BASIS_TO_LAYER.get(basis, (None, None))[1] if basis else None,
        "upstream": {
            "source": "manual_relabel",
            "worksheet": f"{pair}.md",
            "fill_key": f"NEW-{pair}",
            "entry": nid,
        },
        "pending": dict(PENDING_AT_MERGE),
    }
    if scope is None:
        out["pending"]["in_scope"] = "⛔ `scope` 未填 —— 边界层没判，不敢默认它在界内"
    return out
