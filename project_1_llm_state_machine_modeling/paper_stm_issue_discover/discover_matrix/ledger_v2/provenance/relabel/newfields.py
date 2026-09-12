"""§5 新增 issue 的**字段定义、填写模板、判定测试与脚本推导**。

登记一条新增缺陷只回答三件事：

| 项 | 字段 | 形态 |
| :-- | :-- | :-- |
| ① 它是哪一类错 | `defect_locus` + 分支轴 + `defect_reference` | 可枚举，勾选 |
| ② 错在哪、错成什么样 | `statement` | 自由文本 |
| ③ 修好之后怎样才算 ok | `expected_after_fix` | 自由文本（Dwyer 句式骨架可选） |

① 是一套**条件式座标系**：先答「定位范围」`defect_locus`，它决定后面问哪些轴。
走 `element` 支问构件与限定词（A + B），走逻辑支问逻辑类型（D）；两支都要答参照物（C）。
判读者面对的从来不是 28 个取值，而是一次 4 选 1 加两三次不超过 9 选 1。

**取值与判定测试的唯一真源是**
[defect_taxonomy.md](../../../../discover_matrix/docs/protocol/defect_taxonomy.md)。
本文件逐条内联它的取值、中文名与判定测试，不另立定义；每个取值在那份文档里都挂着
一条可查证的外部依据（Chow / Lackner & Schmidt / ODC / Heimdahl & Leveson /
Baier & Katoen / UML 2.5.1 / Dwyer 等）。

为什么类型学必须从外部来：本轮重标要回答的是「台账有没有漏掉我们框架表达不了的缺陷」。
若取值是从我们自己的谓词词表、四层 `layer` 或台账已有条目归纳出来的，判读者能选出来的
类型按构造就等于框架已经能说的东西 —— 问题本身被答案定义掉了。旧的 `direction` 字段
正是这样：它的取值明写是「台账 98 条实际用过的 8 类」，没被用过的类不在选项里。
它与新的 `defect_element` / `defect_logic_kind` 语义有重叠但取值不同，本轮**直接删除、
不做映射** —— 旧值是自家词表，新值有文献出处，混用会污染出处链。

样例全部取自 [expected_issue_set.json](../expected_issue_set.json) 的真实条目，一条都没有编。
但选样例时会避开当前 pair 所属的 NL 组 —— 同一份 NL 生成 6 个制品，拿兄弟 pair 的缺陷
当格式样例等于把答案先告诉作者。见 `exemplar()`。
"""

from __future__ import annotations

import sources as S

# ------------------------------------------------------------------ ① 座标系

# 每张表的元素是 (取值, 中文名, 判定测试)。三列都要内联进工作单 ——
# 判读者不该为了选一个类型去翻别的文件。

#: 维度 0 · 定位范围。判定测试：要把这条缺陷说清楚，你最少得指出制品里的几处？
LOCI = [
    ("element", "单元素",
     "**一处**就够：能指着作者源的一行说「就是它」"),
    ("pair", "元素间关系",
     "**两处或少数几处**，而且**单看每一处都合法** —— 缺陷在它们的关系里"),
    ("global", "全图性质",
     "指不出具体处，必须说「整张图」或「所有执行」"),
    ("other", "其他",
     "以上都不是。必须在 `other_note` 里写清它是什么形状"),
]

#: 维度 A · 构件。**仅** `defect_locus = element` 时填。判定测试指着作者源那一行问。
ELEMENTS = [
    ("state", "状态",
     "那一处是（或本应是）一个**状态节点**，包括它挂在哪个父态之下"),
    ("transition", "迁移",
     "那一处是**一条边本身**：边在不在、从哪个源态出发、指向哪个目标态"),
    ("trigger", "触发事件",
     "那一处是边标签上 `/` **之前、方括号之外**的**事件名**"),
    ("guard", "守卫条件",
     "那一处是边标签上**方括号 `[...]` 内**的布尔表达式"),
    ("effect", "效应与状态动作",
     "那一处是边标签上 `/` **之后**的内容，或状态体内的 `entry` / `exit` / `do` 动作"),
    ("variable", "变量",
     "守卫或效应**引用了**某个量，而该量在模型里没有独立声明"),
    ("region", "正交区域（界外·记录用）",
     "那一处是 PlantUML 的**正交区分隔符 `--`**，或它划出的一个并发区槽位"
     "（含「区应当有几个」这类数量断言）。只需数 `--` 有几条、划出几个区，"
     "**不需要判断并发语义本身**。本档 `counts_as_defect = false`：**可记录、不计分**"),
    ("other", "其他",
     "以上都不是。必须在 `other_note` 里写清它是什么；"
     "若一格装不下（涉及多个取值），同样落这里并写清是哪几个"),
]

#: 界外取值：**可记录、不计入缺陷统计**（`counts_as_defect = false`）。
#:
#: ⚠️⚠️ 这不是把边界放宽了。[CLAUDE.md](../../../../../../CLAUDE.md) 的建模对象边界要求
#: **两条同时成立** —— ⛔ 既不得把并发 / 时间类问题记为「方法未能检出」，
#: ⛔ 也不得反过来声称「这些模型没有并发 / 时间问题」。给它一个可记录、但不计分的槽位，
#: ⭐ 是唯一能同时满足这两条的做法。⛔ 把 `region` 计入命中率、覆盖率或缺陷数都是错的。
#:
#: 为什么只给正交区域开槽位、时钟与不变式没开：判据是「有没有一条只看制品就能唯一判定的
#: 测试」。正交区在 PlantUML 里有**逐字的语法载体**（`--`），数它是纯词法操作；
#: 时钟与不变式在本语料的作者源里根本没有语法载体，判读者只能从散文语义推断。
#: 详见类型学 [§3.7](../../../../discover_matrix/docs/protocol/defect_taxonomy.md)。
OUT_OF_SCOPE_VALUES = {
    ("defect_element", "region"):
        "正交区并发语义在 $M = (S, E, V, Tr, A)$ 之外。本取值只为**记录**存在，"
        "不承载缺陷类型学主张，故不计入任何缺陷统计。",
}


def counts_as_defect(axis, value):
    """该取值算不算一条缺陷。⛔ 界外取值一律 `False`。"""
    return (axis, value) not in OUT_OF_SCOPE_VALUES

#: 维度 B · 限定词。**仅** `defect_locus = element` 时填。
QUALIFIERS = [
    ("missing", "缺失",
     "条数**变多**（新增一个构件，已有构件内容不变）"),
    ("incorrect", "错值",
     "条数**不变**（只改动某个已有构件的一个属性值）—— 事件名拼错、边接到错的目标态、"
     "子态挂错父态都在这一档"),
    ("extraneous", "多余",
     "条数**变少**（删掉一个已有构件）"),
    ("other", "其他",
     "一次编辑改不完。例如三个检测事件被塌缩成一个泛化事件（要删一条、加三条）。"
     "在 `other_note` 里写清要改哪几步"),
]

#: 维度 B 的统一判定测试。放在表头，不逐行重复。
QUALIFIER_TEST = (
    "设想把这条缺陷改对，且**只做一次编辑**；改完之后，作者源里该类构件的**声明条数**"
    "是变多、不变，还是变少？"
)

#: 维度 D · 逻辑层类型。**仅** `defect_locus ≠ element` 时填。判定测试可手算，除非另注。
LOGIC_KINDS = [
    ("nondeterminism", "非确定性",
     "取某状态在**同一事件**下的全部出边守卫，存在一个变量赋值使**其中两条同时为真**"),
    ("incompleteness", "守卫不完备",
     "同一组守卫，存在一个变量赋值使**全部为假**（即其析取不是永真式）"),
    ("unreachable", "不可达",
     "从初始态出发的图遍历到不了它"),
    ("unintended_terminal", "非预期终止",
     "某状态**及其所有祖先**都没有可用出边，而它不是有意的终态。"
     "⚠️ **判定时必须把祖先的成组迁移数进去**：一个叶态自己画不出出边，"
     "若它的**外层复合态**有出边，那条边对该叶态同样可用 —— 它**不是**终止态。"
     "这是本取值最常见的假阳性。「是不是有意的终态」要回 NL 判，故本档几乎总配 "
     "`defect_reference = requirement`"),
    ("nontermination", "不终止",
     "NL 要求终会到达某终止条件，而模型存在一条永不到达它的执行。"
     "⚠️ **本档只能挂在 NL 的终止义务上**：活锁 / non-progress cycle 在标准文献里"
     "**没有与标注无关的形式定义**（唯一成文定义相对用户手工标注的 progress label 给出），"
     "所以不得写成「模型自身即可判定它活锁了」"),
    ("property_violation", "时序性质违反",
     "NL 要求一条时序性质，模型存在一条反例执行。一般需要模型检查器；"
     "用 `expected_after_fix` 的 Dwyer 句式把那条性质写出来"),
    ("priority_conflict", "优先级冲突",
     "存在一个状态配置与事件，使**内层与外层各有一条使能出边**，"
     "而哪条先发取决于语义约定（UML 给内层、经典 statechart 给外层）。"
     "只判「存不存在这种局面」，**不判「谁对」**"),
    ("hierarchy_entry", "层次进入语义",
     "存在一条迁移，其目标是**复合态本身**而非其某个子态，且该复合态有默认入口 —— "
     "于是每次进入都会重跑内部初始，把内部阶段重置"),
    ("other", "其他",
     "以上都不是。必须在 `other_note` 里写清它是什么"),
]

#: 维度 C · 参照物。两支都要填。判定测试：判定这条缺陷成立，你需不需要引用 NL 的某一句？
REFERENCES = [
    ("language", "语言规则",
     "**不引用 NL 任何一句**就能判定；依据是建模语言 / 元模型的良构性规则"),
    ("requirement", "需求文本",
     "**必须引用 NL 的某一句**才能判定"),
    ("other", "其他",
     "两者都不是。典型落点：只能靠参考模型对照（参考模型不是正确答案，"
     "故这类等于「本条待裁定」）；或依据是「人读不懂」。在 `other_note` 里写清是哪一种"),
]

#: 维度 E（可选）· Dwyer 性质模式 × 作用域，供 `expected_after_fix` 套句式。
PROPERTY_PATTERNS = [
    ("Absence", "不出现", "在〈scope〉内，〈P〉**始终不发生**"),
    ("Universality", "恒成立", "在〈scope〉内，〈P〉**始终成立**"),
    ("Existence", "必出现", "在〈scope〉内，〈P〉**至少发生一次**"),
    ("Bounded Existence", "有界出现", "在〈scope〉内，〈P〉**至多发生 k 次**"),
    ("Precedence", "先于", "在〈scope〉内，〈P〉之前**必须先有** 〈Q〉"),
    ("Response", "响应", "在〈scope〉内，〈P〉之后**终将有** 〈Q〉"),
    ("Precedence Chain", "先于链", "〈P〉之前必须依次有〈Q〉、〈R〉"),
    ("Response Chain", "响应链", "〈P〉之后终将依次有〈Q〉、〈R〉"),
]

PROPERTY_SCOPES = [
    ("Globally", "全程", "整条执行"),
    ("Before", "某事件之前", "执行开头到〈E〉**首次**出现为止"),
    ("After", "某事件之后", "〈E〉**首次**出现之后的执行"),
    ("Between", "两事件之间", "从〈E1〉到〈E2〉之间的每一段"),
    ("After-Until", "某事件后直到", "同 Between，但〈E2〉可以不出现"),
]

#: Dwyer 采用时必须一并带上的两条口径。
PROPERTY_CAVEATS = [
    "作用域本身是**可选**的：分隔事件在某条执行里不出现，该性质在那条执行上自动为真。",
    "`Before` / `After` 相对分隔事件的**首次**出现解释。",
]

#: 已知表达缺口。判读者撞上它时不是自己选错了，据实落 `other` 即可。
KNOWN_GAPS = [
    ("entry / exit 动作的**执行次序**",
     "`defect_locus = pair` + `defect_logic_kind = other` + 在 `statement` 里写清",
     "UML 与经典 statechart 对跨层次迁移的 exit / entry 次序都有成文规定，"
     "但**两家不完全一致，而一份 PlantUML 制品并不声明它遵循哪一套** —— "
     "判「次序错了」要先有一个语义裁定，故本座标系不为它设取值"),
]

# 取值集合（供校验用）。⛔ 顺序即模板与图例的渲染顺序。
DEFECT_LOCI = [v for v, _zh, _t in LOCI]
DEFECT_ELEMENTS = [v for v, _zh, _t in ELEMENTS]
DEFECT_QUALIFIERS = [v for v, _zh, _t in QUALIFIERS]
DEFECT_LOGIC_KINDS = [v for v, _zh, _t in LOGIC_KINDS]
DEFECT_REFERENCES = [v for v, _zh, _t in REFERENCES]

#: 走 `element` 支时才问的两轴。
ELEMENT_BRANCH_FIELDS = ["defect_element", "defect_qualifier"]
#: 走逻辑支（`pair` / `global` / `other`）时才问的那一轴。
LOGIC_BRANCH_FIELDS = ["defect_logic_kind"]
#: `defect_locus` 取哪些值时走 element 支。
ELEMENT_LOCUS = "element"

#: 枚举字段 → 允许取值。校验只用这一张表，不在别处另抄。
ENUMS = {
    "defect_locus": DEFECT_LOCI,
    "defect_element": DEFECT_ELEMENTS,
    "defect_qualifier": DEFECT_QUALIFIERS,
    "defect_logic_kind": DEFECT_LOGIC_KINDS,
    "defect_reference": DEFECT_REFERENCES,
}

#: 中文名索引，供渲染与报错文案用。
ZH = {name: dict((v, zh) for v, zh, _t in table)
      for name, table in (("defect_locus", LOCI),
                          ("defect_element", ELEMENTS),
                          ("defect_qualifier", QUALIFIERS),
                          ("defect_logic_kind", LOGIC_KINDS),
                          ("defect_reference", REFERENCES))}

# ------------------------------------------------------------------ 字段清单

#: 两支都要填的项。分支轴另由 `required_axes_for()` 给出。
ALWAYS_REQUIRED_FIELDS = ["defect_locus", "defect_reference",
                          "statement", "expected_after_fix", "nl_evidence"]

#: **条件必填**：五个轴里任意一个取 `other` 时必须写，否则可留空。
#:
#: ⭐ 判据只看字段值（「有没有 `other`」「说明空不空」），故按
#: [CLAUDE.md](../../../../../../CLAUDE.md) §11 允许做成 `E` 级门，见 [validate.py](./validate.py)。
#: ⛔ 「这句说明写得对不对」是语义判断，**不做成门**。
#:
#: 为什么要有它：`other` 是出口，出口不写清等于没分类 —— 事后回看只剩一个 `other`，
#: 既不知道它是什么，也不知道它是「真的都不是」还是「涉及多个、一格装不下」。
#: ⭐ 两种情形都合法，但**必须说出是哪一种**。
OTHER_NOTE_FIELD = "other_note"
CONDITIONAL_FIELDS = [OTHER_NOTE_FIELD]

#: 可留空的项。
OPTIONAL_FIELDS = ["property_pattern"]


def other_axes(values):
    """给定 `{轴: 取值}`，返回其中取了 `other` 的轴名。⛔ 判据是逐字相等，不做语义推断。"""
    return [a for a in ENUMS if values.get(a) == "other"]

#: 只有这些名字能在填写块里起一个新字段。其余带冒号的行一律并进当前字段 ——
#: 否则作者在 `statement` 里写「NL 第 3 句：…」就会被解析器当成新字段名而截断。
FIELD_NAMES = (["defect_locus"] + ELEMENT_BRANCH_FIELDS + LOGIC_BRANCH_FIELDS
               + ["defect_reference"] + CONDITIONAL_FIELDS
               + ["statement", "expected_after_fix",
                  "nl_evidence"] + OPTIONAL_FIELDS)

#: 只有这些是勾选行；其余一律读成自由文本。
#: 这条是硬的：自由文本里几乎必然出现 `[*]`（PlantUML 伪状态写法），
#: 若把它当勾选行解析，值会变成空的零选项勾选行 —— 入口类缺陷会整类丢失。
CHOICE_FIELDS = list(ENUMS)


def required_axes_for(locus):
    """按 `defect_locus` 给出**这一条**还必须回答哪些轴。

    条件式的落点就在这里：选了 `element` 问 A 与 B，选了别的问 D。
    `locus` 还没填（`None`）时返回空表 —— 那时该报的是「`defect_locus` 未选」，
    不是「分支轴缺失」。
    """
    if locus is None:
        return []
    return list(ELEMENT_BRANCH_FIELDS) if locus == ELEMENT_LOCUS else list(LOGIC_BRANCH_FIELDS)


def forbidden_axes_for(locus):
    """按 `defect_locus` 给出**这一条不该填**的轴。

    填了另一支的轴不报错、只提醒：它多半是选完 locus 之后忘了删，
    而「填多了」不像「填少了」那样会让记录不可用。
    """
    if locus is None:
        return []
    return list(LOGIC_BRANCH_FIELDS) if locus == ELEMENT_LOCUS else list(ELEMENT_BRANCH_FIELDS)


#: 显式的「已判定为无」标记。留空 = 没填；写 `无` = 判过了，结论是没有。
NONE_MARKS = ("无", "none", "None", "N/A", "n/a", "—", "-")


def is_none_mark(text):
    return (text or "").strip() in NONE_MARKS


# ------------------------------------------------------------------ 填写模板

# 分支提示行。它们**不是字段** —— `collect.parse_fields` 按本清单逐字剔除，
# 否则紧跟在勾选行之后的那一行会被并进上一个字段的值里。
# 因此这里**不许出现半角冒号**：`fillblocks.is_untouched` 用 `":" in line` 判
# 「冒号后写了东西」，半角冒号会让空模板被误判成已填。
HINT_ELEMENT_BRANCH = "--- 上一行选了 element：填下面两项，跳过 defect_logic_kind ---"
HINT_LOGIC_BRANCH = "--- 上一行选了 pair / global / other：跳过上面两项，填下面这一项 ---"
HINT_BOTH = "--- 以下四项两支都要填 ---"
#: ⚠️ 这一行**不许出现半角冒号**，理由同上（`fillblocks.is_untouched` 的判据）。
HINT_OTHER_NOTE = "--- 上面任一轴勾了 other：下面这一项必填，写一句说清它是什么、或涉及哪几个取值 ---"
HINT_OPTIONAL = "--- 以下一项可留空 ---"

TEMPLATE_HINTS = [HINT_ELEMENT_BRANCH, HINT_LOGIC_BRANCH, HINT_BOTH,
                  HINT_OTHER_NOTE, HINT_OPTIONAL]


def _choice_line(name, options):
    return f"{name}: " + "  ".join(f"[ ] {o}" for o in options)


def entry_template(pair, index):
    return "\n".join([
        f"### NEW-{pair}-{index:02d}",
        _choice_line("defect_locus", DEFECT_LOCI),
        HINT_ELEMENT_BRANCH,
        _choice_line("defect_element", DEFECT_ELEMENTS),
        _choice_line("defect_qualifier", DEFECT_QUALIFIERS),
        HINT_LOGIC_BRANCH,
        _choice_line("defect_logic_kind", DEFECT_LOGIC_KINDS),
        HINT_BOTH,
        _choice_line("defect_reference", DEFECT_REFERENCES),
        HINT_OTHER_NOTE,
        f"{OTHER_NOTE_FIELD}:",
        "statement:",
        "expected_after_fix:",
        "nl_evidence:",
        HINT_OPTIONAL,
        "property_pattern:",
    ])


def template(pair, count=2):
    return "\n\n".join(entry_template(pair, i) for i in range(1, count + 1))


# ------------------------------------------------------------------ 台账统计（供指引正文用）

def direction_counts():
    """台账每个 `direction` 的条数（REPORTABLE 98 条口径）。

    这是**台账自己**的字段统计，供 §4 清单的分类导语说明「台账在这一维有多空」。
    新增登记块**不再有** `direction` 字段（见模块 docstring），两者不要混。
    """
    from collections import Counter
    return Counter(r["direction"] for r in S.ledger_records(reportable_only=True))


def layer_counts():
    from collections import Counter
    return Counter(r["layer"] for r in S.ledger_records(reportable_only=True))


def primary_predicate_counts():
    """台账里每个谓词作为 `primary_predicate` 出现的次数（REPORTABLE 98 条口径）。

    存在的理由是防漂移：这些数字此前以字面量散在 [checklist.py](./checklist.py) 的
    分类导语里，且用的是**全 126 条**口径 —— 于是同一份工作单里 §4 说
    `initial_target` 做过 21 次 primary、而另一处按 98 条算是 14 次。
    两个数都对，但**混在一份文件里就是错的**：126 里含 `00x8` 六个永久越界 pair。
    """
    from collections import Counter
    return Counter(r.get("primary_predicate")
                   for r in S.ledger_records(reportable_only=True)
                   if r.get("primary_predicate"))


# ⛔ 2026-08-13 一并删除：`layer_basis_table()` 与 `NL_GROUNDED_LAYERS`。
# 两者的**唯一**消费者是 [sources.py](./sources.py) 的 `risk_flags`，
# 而那两条标记（逐条印出该记录的 `layer` 与 `layer_basis` 原话、催判读者补 `nl_evidence`）
# 随工作单 §2 剥掉十项旧元数据一起删了。
# ⛔ 留着不用的常量比删干净更糟：下一个人会以为那一栏还印着。

LAYERS = list(S.LAYERS)


def nl_evidence_empty_count():
    recs = S.ledger_records(reportable_only=True)
    return sum(1 for r in recs if not (r.get("nl_evidence") or "").strip()), len(recs)


# ------------------------------------------------------------------ 样例挑选

# 每个字段给一串候选台账 id，按序取**第一个不属于当前 pair 所在 NL 组**的。
# 候选必须横跨至少两个 NL 组，否则某些 pair 会挑不到样例
# （`test_every_exemplar_slot_resolves_off_group` 钉住这一点）。
EXEMPLARS = {
    "statement": ["EIS-0040-01", "EIS-0029-01", "EIS-0002-03", "EIS-0009-01", "EIS-0036-02"],
    "nl_evidence": ["EIS-0046-02", "EIS-0014-04", "EIS-0035-03", "EIS-0024-01", "EIS-0009-01"],
    "nl_evidence_empty": ["EIS-0000-01", "EIS-0046-01", "EIS-0010-01", "EIS-0002-03"],
}


def _by_id():
    return {r["id"]: r for r in S.ledger_records(reportable_only=True)}


def exemplar(slot, pair):
    """取该 slot 的样例记录，跳过与 `pair` 同一份 NL 的条目。取不到返回 `None`。"""
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

#: 维度 A 到 $M = (S, E, V, Tr, A)$ 分量的确定性映射，用于与既有台账并表。
#: 只在走 `element` 支时成立；逻辑支的缺陷按定义不落在单个分量上。
ELEMENT_TO_M = {
    "state": "S",
    "transition": "Tr",
    "trigger": "E",
    "guard": "Tr",
    "effect": "A",
    "variable": "V",
}

# 这些字段本轮**推不出来**，必须留到合并回台账那一步。
# 列出来是为了让「脚本推导」是一句可核对的话，而不是一句托辞。
PENDING_AT_MERGE = {
    "assertions": "要由断言生成器对 statement 产出，本目录不产断言",
    "assertion_count": "同上，随 `assertions` 一起产生",
    "has_negative_control": "同上",
    "replay": "要真跑一遍谓词才有 verdict / value",
    "verdict": "合并时由裁定给出，不由重标者自封",
    "homogeneity_group": "要在全库范围内重算同质组，单 pair 内算不了",
    "homogeneity_group_size": "同上",
    "homogeneity_groupable": "同上",
    "automatable": "取决于 `assertions` 是否可执行",
    "layer": "台账四层与新座标系不同构，合并时按裁定套写，不由判读者勾",
    "layer_basis": "同上，随 `layer` 一起产生",
    "decided_by": "本轮固定为人工重标，合并时统一写入",
    "in_scope": "边界（时钟 / 不变式 / 并发）不再由判读者分类 —— "
                "回收后由主 session 从 `statement` 自由文本人工分拣",
    "counts_as_defect": "同上，随边界分拣一起裁定",
    "boundary_ruling": "同上，随边界分拣一起裁定",
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


def derive_element_of_M(defect_element):
    """由维度 A 推 `element_of_M`。返回 `(值 或 None, 依据说明)`。

    走逻辑支时返回 `None` —— 「推不出来」必须显形，不许猜一个填上。
    """
    if defect_element in ELEMENT_TO_M:
        return (ELEMENT_TO_M[defect_element],
                f"维度 A `{defect_element}` 到 $M$ 分量的确定性映射")
    if defect_element == "region":
        return None, ("维度 A 选了 `region` —— 正交区在 $M = (S, E, V, Tr, A)$ 里"
                      "**没有分量**（界外，`counts_as_defect = false`）")
    if defect_element == "other":
        return None, "维度 A 选了 `other` —— 分量取决于它到底是什么，见 `other_note`"
    return None, "本条走逻辑支，缺陷按定义不落在单个 $M$ 分量上"


def derive(pair, nid, fields):
    """把人工填的字段补成一条**接近台账形态**的记录。

    这不是「合并回台账」—— 它只把当下能确定的部分算出来，
    剩下的列在 `pending` 里，不留空白假装齐了。
    """
    locus = field_value(fields, "defect_locus")
    elem_axis = field_value(fields, "defect_element")
    elem, elem_basis = (derive_element_of_M(elem_axis) if locus == ELEMENT_LOCUS
                        else (None, "本条走逻辑支，缺陷按定义不落在单个 $M$ 分量上"))

    out = {
        "id": nid,
        "pair": pair,
        "group": S.nl_group(pair),
        "llm": S.source_meta(pair).get("llm"),
        "defect_locus": locus,
        "defect_element": elem_axis if locus == ELEMENT_LOCUS else None,
        "defect_qualifier": (field_value(fields, "defect_qualifier")
                             if locus == ELEMENT_LOCUS else None),
        "defect_logic_kind": (field_value(fields, "defect_logic_kind")
                              if locus and locus != ELEMENT_LOCUS else None),
        "defect_reference": field_value(fields, "defect_reference"),
        OTHER_NOTE_FIELD: field_value(fields, OTHER_NOTE_FIELD),
        "element_of_M": elem,
        "element_of_M_basis": elem_basis,
        "upstream": {
            "source": "manual_relabel",
            "worksheet": f"{pair}.md",
            "fill_key": f"NEW-{pair}",
            "entry": nid,
        },
        "pending": dict(PENDING_AT_MERGE),
    }
    # ⭐ 界外取值现在能**当场判定** `counts_as_defect`，不必留到合并那一步：
    # 勾了 `region` 就是界外、不计分。其余仍按边界分拣待定。
    if locus == ELEMENT_LOCUS and not counts_as_defect("defect_element", elem_axis):
        out["counts_as_defect"] = False
        out["counts_as_defect_basis"] = OUT_OF_SCOPE_VALUES[("defect_element", elem_axis)]
        out["pending"].pop("counts_as_defect", None)
    if locus is None:
        out["pending"]["defect_locus"] = "未选定位范围 —— 分支轴与 $M$ 分量都无从推起"
    return out
