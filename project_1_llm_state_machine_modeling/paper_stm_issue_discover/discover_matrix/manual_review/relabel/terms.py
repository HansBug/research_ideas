"""术语英中对照 —— ⭐ 工作单「自包含」的唯一真源。

为什么要有这一份
----------------
工作单是给**人**填的。⛔ 而它此前把 `layer` / `direction` / `element_of_M` /
`decided_by` / `primary_predicate` / `verdict` / `replay` 这些字段的值直接印成裸英文
标识符，判据则写成「见 HOWTO.md §D.4」——⚠️ 于是判读者要填一张表得先翻两个文件，
⛔ 而最需要判据的那一栏恰恰是跳转最远的那一栏。

⛔ **每一条中文都必须能指到仓库里的出处（文件 + 行号），⛔ 指不到的一律标「仓库未定义」。**
⚠️ 这不是格式洁癖：中文名一旦是编的，判读者就会按编出来的语义去判，
⛔ 而那个语义与台账字段的真实定义之间的偏差**不会有任何报错**。

出处分两类，⛔ 不要混：

1. **仓库已有中文常量** —— 直接引用，⛔ 不重译。
   `LAYER_ZH` / `DIRECTION_ZH` / `ROLE_ZH` 抄自
   `discover_matrix/render_eis_bundle.py`（分别在第 40、47、52 行起）。
2. **仓库只有英文定义** —— 中文是**对该英文原话的翻译**，⛔ 英文原话同时保留在表里，
   判读者可自行复核。19 个谓词的 `meaning` 属这一类，出处是
   `pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/predicates.py`。

⭐ 「判据原话」一律取**逐字原文**，⛔ 不改写：`layer` 的判据取每条台账记录自己的
`layer_basis` 字段（那是分层判据的真源，见 `newfields.layer_basis_table()`）。
"""

from __future__ import annotations

# ==================================================================== ① 台账展示值
# ⭐ 这一组是「已经填好、只需读懂」的值 —— 按用户口径**只内联该条自己那一个取值**，
# ⛔ 不在每条记录下面把四层 / 八方向全列一遍。

#: `layer` 四层的中文名。⭐ 出处：`discover_matrix/render_eis_bundle.py:40-46` 的 `LAYER_ZH`。
#: ⚠️ `checklist.py:571` 另用过「合式性层」指 `wellformedness`，⭐ 本文件统一取 `render_eis_bundle`
#: 的「良构性」——⛔ 两个词指同一层，⛔ 不是两个概念。
LAYER_ZH = {
    "wellformedness": "良构性",
    "nl_named": "NL 点名",
    "nl_contradiction": "与 NL 矛盾",
    "over_specification": "过度指定且有害",
}

#: `element_of_M` 的中文名。⭐ 出处：仓库根 `CLAUDE.md`「核心技术概念 · 状态机形式化」——
#: $M = (S, E, V, Tr, A)$ 其中 S=状态集合 E=事件集合 V=变量集合 Tr=迁移集合 A=动作集合。
#: ⭐ `多个` 是台账里的实际取值（1 条），本身已是中文。
ELEMENT_ZH = {
    "S": "状态集合",
    "E": "事件集合",
    "V": "变量集合",
    "Tr": "迁移集合",
    "A": "动作集合",
    "多个": "跨多个分量",
}

#: `decided_by` 六个取值：中文名 + 判据。
#: ⭐ 出处全部是 `discover_matrix/merge_manual_stratification.py`，⛔ 该文件是这个字段的**唯一**写入方：
#: `lexical` L66 · `batch5_reclassify` L103 · `batch5_spotcheck` L122 ·
#: `nl_review` L159 · `harm_test` L192 · `parent_ruling` L242。
#: ⚠️ 该文件的注释与 docstring 是英文的，⭐ 下面的中文是对那些注释的翻译，⛔ 不是新定义。
DECIDED_BY_ZH = {
    "lexical": (
        "词法分层",
        "基线分层：由 `stratify_candidates.classify` 按**措辞正则**给出，"
        "⛔ 从未经人工二读。词法层存在的意义只是让人工那一遍变得有限，⛔ 不是用来压过人工判定的。",
    ),
    "nl_review": (
        "NL 逐条复核",
        "审阅者把该行**逐条对着 NL 原文**读过之后给出的归层（批 1 至 4）。",
    ),
    "harm_test": (
        "有害性判定",
        "只用于 `extra` 档：逐条判 harmful（有害）/ benign（无害）/ uncertain（未定）—— "
        "⛔ 被模型凭空造出只说明可归因，⛔ 不自动等于缺陷。",
    ),
    "batch5_reclassify": (
        "批 5 重新归层",
        "批 5 覆盖前四批没覆盖的行（词法完全分不了类的、以及被词法排除的），重新归层。",
    ),
    "batch5_spotcheck": (
        "批 5 抽验改判",
        "批 5 对无人全量复核的两层做抽验，⛔ 抽验结论与原判**不一致**，故按抽验改判。",
    ),
    "parent_ruling": (
        "主裁定",
        "两轮复核彼此冲突、或报告的测量无法复现时，由主 session 裁定；"
        "⭐ 逐条附证据单独存档，⛔ 使「推翻一位复核者」本身也可审计。",
    ),
}

#: `verdict` 两个取值。⭐ 出处：`generate.py` 的 `_DIFF_VERDICT_NOTE`（§3 用的同一套上游词表）
#: 与 `discover_matrix/render_eis_bundle.py:301` 对 `over_specification` 的说明。
VERDICT_ZH = {
    "problem": (
        "判为问题",
        "当年的审阅 agent 逐条比对参考侧与生成侧后，把这一处判为「问题」。",
    ),
    "extra": (
        "生成方凭空新增",
        "判为「生成方凭空多出一个参考侧没有的元素」。"
        "⛔ 台账的 8 类分类学**没有 `extra` 的槽位**，⚠️ 故这类记录只能被硬塞进某一层。",
    ),
}

#: `replay.verdict` 取值。⭐ 出处：`discover_matrix/verify_assertions.py:158` 逐字
#: 「断言返回 **False** —— 缺陷可被现有谓词表述并捕获」；⭐ 未确认一档见
#: `manual_review/relabel/README.md:366`「主断言未被复算确认（`replay ≠ captured`）」。
REPLAY_ZH = {
    "captured": ("已捕获", "断言返回 `False` —— 缺陷可被现有谓词表述并捕获。"),
    None: ("未确认", "主断言未被复算确认 —— ⛔ 不等于该条不成立，⭐ 但它这一条没有实测证据。"),
}

#: 断言角色。⭐ 中文名出处：`discover_matrix/render_eis_bundle.py:52-57` 的 `ROLE_ZH`；
#: ⭐ 「应有实测值 + 作用」出处：`discover_matrix/render_eis_issue.py:937-945` 的角色表（逐字）。
ROLE_ZH = {
    "primary": (
        "主断言",
        "陈述缺陷本身，应实测 `False`。返回 `True` 说明断言不判别，返回 `None` 说明无法判定"
        "——⛔ 两者都不是证据。",
    ),
    "negative_control": (
        "负控",
        "证明主断言不是恒假，应实测 **`True`**。缺它就无法排除「正确模型也返回 `False`」。",
    ),
    "corroborating": (
        "佐证",
        "补第二个后果，⭐ 加固而非替代主断言。",
    ),
    "recovered_unverified": (
        "从文本恢复、未能验证",
        "从复核者散文里恢复但未能自动求值；记录在案供人工核对，⛔ **不计入证据**。",
    ),
}

#: 谓词三族。⭐ 出处：`discover/predicates.py` 模块 docstring 的 "Reading the family column"
#: 一节（第 19 至 30 行）；⭐ 三个族的中文名沿用 `newfields.py:317-318` 的「结构族 / 行为族 / 性质族」。
FAMILY_ZH = {
    "S": ("结构族", "主张关于制品**声明**了什么；一次结构性 / 关系性查询即可直接判定。"),
    "B": ("行为族", "主张关于模型**运行时做什么**；必须实跑仿真 —— "
                    "⛔ 声明存在不等于它可达、被使能、或就是真正触发的那一条。"),
    "P": ("性质族", "主张在状态 / 赋值 / 路径上被量化，⛔ 单次查询与单条有限运行都定不下来；"
                    "必须做有界模型检查。"),
}

#: 19 个封闭谓词：族 · 中文一句判据 · 英文原话（⭐ 逐字）。
#: ⭐ 出处：`pipeline/feedback_loop/src/paper_stm_feedback_loop/discover/predicates.py` 每条
#: `Predicate(...)` 的第三个位置参数 `meaning`，行号逐条标在注释里。
#: ⚠️ 中文是**对该英文原话的翻译**，⛔ 不是另立定义 —— 故英文原话一并保留，判读者可自行复核。
PREDICATE_ZH = {
    # ---- S 族（结构族）
    "state_declared": ("S", "模型在该路径上声明了一个该种类的状态",
                       "the model declares a state at this path, of this kind"),          # L120
    "variable_declared": ("S", "模型以该名字声明了一个**作者自己的**变量",
                          "the model declares a variable of the author's own under this name"),  # L153
    "event_declared": ("S", "模型在该限定路径上声明了一个事件",
                       "the model declares an event at this qualified path"),              # L195
    "containment": ("S", "该子态是（或不是）该父态的子状态",
                    "this child is (or is not) a substate of this parent"),                # L229
    "initial_target": ("S", "进入该复合态时从该子态开始",
                       "entering this composite starts in this child"),                    # L266
    "edge_declared": ("S", "模型声明了一条以该源、该触发、该目标构成的迁移",
                      "the model declares an edge with this source, trigger and target"),  # L302
    "effect_declared": ("S", "该迁移声明了对该变量、朝该方向的效应",
                        "this transition declares an effect on this variable, in this direction"),  # L338
    "action_declared": ("S", "该状态声明了一个 `entry` / `exit` / `during` 阶段的动作",
                        "this state declares an entry, exit or during action"),            # L371
    "guard_distinguishable": ("S", "共享同一源与同一触发的两个目标，⛔ 不会无法区分地同时可达",
                              "a shared source and trigger cannot reach two targets indistinguishably"),  # L403
    "cardinality": ("S", "该作用域恰好声明了这么多个非伪状态",
                    "this scope declares exactly this many non-pseudo states"),            # L433
    # ---- B 族（行为族）
    "occupancy_after": ("B", "从该状态施加该触发之后，系统身处该目标态",
                        "after this trigger from this state, the system is in this target"),  # L465
    "event_consumed": ("B", "在该配置下该事件确实被消费",
                       "in this configuration the event is actually consumed"),            # L497
    "stays_in": ("B", "施加该触发之后系统仍留在同一状态",
                 "after this trigger the system remains in the same state"),               # L532
    "variable_delta_after": ("B", "运行该触发会使该变量朝该方向变化",
                             "running this trigger changes this variable in this direction"),  # L566
    "reaches": ("B", "在有界的周期数内，该目标从此处可达",
                "within a bounded number of cycles this target is reachable from here"),   # L600
    "terminates": ("B", "模型确实会结束",
                   "the model actually finishes"),                                         # L639
    # ---- P 族（性质族）
    "invariant": ("P", "在界内该条件始终成立",
                  "within the bound this condition always holds"),                         # L671
    "response_within": ("P", "该触发每次出现都在界内得到回应；`response` 填的是算作回应的**状态路径**，"
                             "⛔ 不是表达式",
                        "every occurrence of this trigger is answered within the bound; "
                        "`response` is the state path that counts as the answer, not an expression"),  # L708
    "persists_until": ("P", "该状态持续保持，直到该释放条件成立",
                       "this state holds continuously until this release condition"),      # L740
}

#: `direction` 八类：中文名 + 判据。
#: ⭐ 中文名出处：`discover_matrix/render_eis_bundle.py:47-52` 的 `DIRECTION_ZH`；
#: ⭐ 判据出处：HOWTO §D.1「指什么」列（本文件 `DIRECTION_MEANING`，⛔ 生成器与本表同读一份）。
#: ⚠️ `effect_action` 在 `render_eis_bundle` 里写作「动作与 effect」——⛔ 那半句仍是英文，
#: ⭐ 故本表取判据里的「效应与状态动作」，⛔ 语义相同。
DIRECTION_MEANING = [
    ("hierarchy", "层次归属", "层次归属：谁该是谁的子态、复合括号有没有打开"),
    ("reachability", "可达性与终止", "可达性与终止：进得去 / 出得来 / 停得下"),
    ("entry", "初始入口", "入口：初始边、初始目标、进入某状态时落到哪"),
    ("guard", "守卫与条件", "守卫：条件写没写、写对没写对、能不能区分多条出边"),
    ("effect_action", "效应与状态动作", "效应与状态动作：entry / exit / 迁移效应"),
    ("event", "事件与触发", "事件：触发词缺失、拼错、被并成一个复合名"),
    ("cardinality", "元素数量", "基数：NL 点名了 N 个而模型给了 M 个"),
    ("unclassified", "未归类", "以上都归不进（⭐ 归不进本身值得在 statement 里说明）"),
]

DIRECTION_ZH = {k: zh for k, zh, _what in DIRECTION_MEANING}
DIRECTION_WHAT = {k: what for k, _zh, what in DIRECTION_MEANING}

#: 字段名的中文。⭐ 出处是 HOWTO §B.1 的必填表与 §D 各节标题（同一份生成器渲染），
#: ⭐ `element_of_M` / `decided_by` / `verdict` / `replay` / `homogeneity_group` 的说明出处见上面各表。
FIELD_ZH = {
    "layer": "归因层",
    "direction": "缺陷方向",
    "element_of_M": "$M$ 分量",
    "decided_by": "分层判定来源",
    "primary_predicate": "主谓词",
    "nl_evidence": "NL 依据",
    "verdict": "上游判定",
    "replay": "复算",
    "statement": "缺陷陈述",
    "generated_side": "生成侧定位",
    "reference_side": "参考侧对应处",
    "basis": "依据来源",
    "scope": "边界",
    "depth": "深度",
}

#: NL 分段口径。⭐ 出处：`sources.nl_segments()` 的两个返回值（`sources.py:194` 与 `:202`）。
SEG_MODE_ZH = {
    "manual_override": ("人工标注分段",
                        "该份规约的编号无法机器判定，分段取自 "
                        "`corpora/nl_segmentation/overrides.json` 的人工标注"),
    "line_split": ("按物理行切", "按物理行切分，与 pipeline 同口径"),
}


# ==================================================================== ② 渲染helper

def bi(term, zh):
    """⭐ 渲染成 `` `term`（中文） ``。⛔ zh 为空时只出英文，⛔ 不编中文。"""
    return f"`{term}`（{zh}）" if zh else f"`{term}`（⛔ 该取值的中文名仓库未定义）"


def layer_cell(rec):
    """⭐ `layer` 的展示值：中文名 + **该条记录自己的** `layer_basis` 逐字原话。

    ⛔ 判据不从 HOWTO 抄，⛔ 也不从本文件抄 —— 取 `rec['layer_basis']`，
    ⭐ 那是台账里分层判据的真源（见 `newfields.layer_basis_table()` 的 docstring）。
    """
    layer = rec.get("layer")
    basis = (rec.get("layer_basis") or "").strip()
    cell = bi(layer, LAYER_ZH.get(layer))
    return f"{cell}——判据原话：{basis}" if basis else f"{cell}——⛔ 该条无 `layer_basis`"


def direction_cell(value):
    if value is None:
        return "⛔ 无"
    return f"{bi(value, DIRECTION_ZH.get(value))}——{DIRECTION_WHAT.get(value, '⛔ 该取值的判据仓库未定义')}"


def element_cell(value):
    if value is None:
        return "⛔ 无"
    zh = ELEMENT_ZH.get(value)
    if value == "多个":
        return f"`多个`（{zh}）"
    return bi(value, zh)


def decided_by_cell(value):
    if value is None:
        return "⛔ 无"
    got = DECIDED_BY_ZH.get(value)
    if not got:
        return f"`{value}`（⛔ 该取值的语义仓库未定义）"
    zh, what = got
    return f"{bi(value, zh)}——{what}"


def predicate_cell(value):
    if not value:
        return "⛔ 无"
    got = PREDICATE_ZH.get(value)
    if not got:
        return f"`{value}`（⛔ 该谓词不在 19 谓词词表内，语义仓库未定义）"
    fam, zh, en = got
    fam_zh = FAMILY_ZH[fam][0]
    return f"{bi(value, zh)}——{fam} {fam_zh}；官方原话 `{en}`"


def verdict_cell(rec):
    """⭐ `verdict` / `replay` 一行：两个取值各自内联中文 + 判据。"""
    v = rec.get("verdict")
    rp = rec.get("replay") or {}
    rv = rp.get("verdict")
    vz = VERDICT_ZH.get(v)
    rz = REPLAY_ZH.get(rv)
    left = f"{bi(v, vz[0])}——{vz[1]}" if vz else f"`{v}`（⛔ 该取值的语义仓库未定义）"
    right = (f"{bi(rv, rz[0])}——{rz[1]}" if rz and rv is not None
             else (f"`{rv}`（{rz[0]}）——{rz[1]}" if rz else f"`{rv}`（⛔ 语义仓库未定义）"))
    return f"{left} / {right}（实测 value `{rp.get('value')}`）"


def role_label(role):
    got = ROLE_ZH.get(role)
    return bi(role, got[0]) if got else f"`{role}`（⛔ 该角色的语义仓库未定义）"


def family_label(fam):
    got = FAMILY_ZH.get(fam)
    return f"{fam} {got[0]}" if got else f"{fam}（⛔ 该族的语义仓库未定义）"
