"""填写块（FILL block）的格式定义、提取与再注入。

工作单是**机器生成 + 人工填写**混合的文件，所以必须能在不丢失人工内容的前提下重跑
生成器。做法是把每个待填区包在一对 HTML 注释哨兵之间：

    <!-- FILL:BEGIN key=EIS-0000-01 kind=ledger -->
    ~~~
    裁决: [ ] 保留  ...
    ~~~
    <!-- FILL:END key=EIS-0000-01 -->

重跑时先把旧文件里所有 `key -> 块内容` 抽出来，重新渲染骨架，再把旧内容按 key 注回。
⭐ 因此**生成器是幂等的**：材料变了就更新材料，人工填写原样保留。

⚠️ 围栏用 `~~~` 而不是 ``` —— 作者在理由里贴代码时通常用 ```，用同一种围栏会截断。
"""

from __future__ import annotations

import re

import newfields as NF

FENCE = "~~~"
_RE_BEGIN = re.compile(r"^<!--\s*FILL:BEGIN\s+key=(?P<key>\S+)\s+kind=(?P<kind>\S+)\s*-->\s*$")
_RE_END = re.compile(r"^<!--\s*FILL:END\s+key=(?P<key>\S+)\s*-->\s*$")

# ------------------------------------------------------------------ 勾选记号
#
# ⭐ **本仓库唯一的勾选记号真源。** ⛔ [collect.py](./collect.py) 的三个解析器、
# 本文件的 `is_untouched`、[generate.py](./generate.py) 渲染的「怎么填」一节都必须读它 ——
# ⛔ 四处各写一份字符集的后果很具体：解析器认 `[✓]` 而 `is_untouched` 只认 `[x]`，
# 于是一份**只用 ✓ 勾选**的工作单会被报成「原样未填」，⚠️ 而它明明填了。
#
# ⚠️ 收哪些记号是**刻意划的**：只收无歧义的**肯定**记号。⛔ 不收 `[v]` / `[是]` / `[o]` /
# `[1]`（不是通行的勾选写法，且 `v` 会与真实标签首字母混淆），⛔ 更不收 `[*]` ——
# 那是 PlantUML 伪状态的写法，⛔ 收了它会让 `[*] --> Final` 这种值被读成勾选行。
# ⛔ 也不收 `[☒]` / `[✗]`：那两个记号在不同人手里一半表示「选中」一半表示「否」。
CHECK_MARKS = "xX✓√✔☑"

# ⭐ 勾选框：`[x]` `[ x ]` `[xx]` `[✓]` 都算勾上；`[ ]` 与 `[]` 算没勾。
RE_CHECKED_BOX = re.compile(r"\[\s*[" + CHECK_MARKS + r"]+\s*\]")


def _template_fields(tpl):
    """从模板逐字推出 (全部字段名, 其中的勾选字段名)。

    ⛔ 这两张表**必须从模板算**，不许另抄一份字面量 —— 模板一改，抄件就对不上，
    ⚠️ 而对不上的后果是静默的：解析器不认某个字段名时，那一行会被并进**上一个**字段，
    ⛔ 没有任何报错。判据同样是逐字的：带 `[ ]` 的行是勾选行，其余是自由文本行。
    """
    names, choices = [], []
    for line in tpl.splitlines():
        m = re.match(r"^([^:：]+)[:：]", line)
        if not m:
            continue
        name = m.group(1).strip()
        names.append(name)
        if "[ ]" in line:
            choices.append(name)
    return names, choices

# 裁决块只问三件事：裁成什么、为什么、改成什么。
# 「深度」一栏 2026-08-13 删除：它是本目录自造的三分（台账没有这个字段），
# 判据「读懂它需要看几个地方」要人做语义判断，却被摆成一个必填勾选行 ——
# 判读者的注意力被从「这一条成不成立」拉到「它算中层还是深层」上。
LEDGER_TEMPLATE = """裁决: [ ] 保留  [ ] 修正  [ ] 删除  [ ] 拆分
理由:
修正后的 statement:"""

CANDIDATE_TEMPLATE = """裁决: [ ] 采纳(补入台账)  [ ] 不采纳  [ ] 待议  [ ] 并入现有条目
并入到:
理由:
补入后的 statement:"""

# ⭐ 新增 issue 的字段与模板由 [newfields.py](./newfields.py) 定义 —— 那里同时放着
# 枚举、填写指引和脚本推导，⛔ 不要在本文件里另开一份，两处会立刻走偏。
def new_template(pair, count=2):
    return NF.template(pair, count)


# 历史模板，按代次冻结成**字面量**。留着只为识别「原样未填的旧模板」——
# 幂等注回是按 key 做的，若不认出旧模板，字段表改版后旧骨架会被当成「人工内容」
# 永久保留，新字段永远出不来（实测：改版后重跑 54 份，§5 全部还是旧的 10 字段表）。
# ⚠️ 只做**逐字全等**匹配：作者若已经在旧模板上填了任何东西，就不算旧模板，原样保留。
#
# 为什么是字面量而不是「用旧常量重建」：旧代次的枚举（`DIRECTIONS` / `LAYERS` /
# `BASES` / `SCOPES` / `DEPTHS`）与三层小标题已经在 [newfields.py](./newfields.py) 里删掉了。
# 一份历史快照本来就该被冻住 —— 它要匹配的是**当年那一批字节**，
# 跟着现行常量变的「历史模板」根本认不出历史文件。
LEGACY_NEW_TEMPLATES = ["""### NEW-{pair}-01
statement:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction
direction:
element_of_M: [ ] S  [ ] E  [ ] V  [ ] Tr  [ ] A
nl_evidence:
depth: [ ] 表层  [ ] 中层  [ ] 深层
primary_predicate:
证据(作者源行号):
来源: [ ] §3候选  [ ] §4清单  [ ] 自行发现

### NEW-{pair}-02
statement:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction
direction:
element_of_M: [ ] S  [ ] E  [ ] V  [ ] Tr  [ ] A
nl_evidence:
depth: [ ] 表层  [ ] 中层  [ ] 深层
primary_predicate:
证据(作者源行号):
来源: [ ] §3候选  [ ] §4清单  [ ] 自行发现"""]

# 第二代：8 字段平铺、无分层小标题。
LEGACY_NEW_TEMPLATES.append("""### NEW-{pair}-01
statement:
generated_side:
nl_evidence:
direction: [ ] reachability  [ ] hierarchy  [ ] guard  [ ] entry  [ ] effect_action  [ ] event  [ ] cardinality  [ ] unclassified
depth: [ ] 表层  [ ] 中层  [ ] 深层
--- 以上 5 项必填 · 以下 3 项可留空 ---
reference_side:
primary_predicate:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction

### NEW-{pair}-02
statement:
generated_side:
nl_evidence:
direction: [ ] reachability  [ ] hierarchy  [ ] guard  [ ] entry  [ ] effect_action  [ ] event  [ ] cardinality  [ ] unclassified
depth: [ ] 表层  [ ] 中层  [ ] 深层
--- 以上 5 项必填 · 以下 3 项可留空 ---
reference_side:
primary_predicate:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction""")

# 第三代：三层结构（① 事实 / ② 依据 / ③ 边界 / ④ 分类轴），字段 10 项。
# 2026-08-13 被条件式座标系取代，见 [newfields.py](./newfields.py) 模块 docstring。
LEGACY_NEW_TEMPLATES.append("""### NEW-{pair}-01
--- ① 事实层 · 看到了什么（⛔ 只写现象，不下判断） ---
statement:
generated_side:
--- ② 依据层 · 凭什么说它是缺陷（⭐ basis 决定 nl_evidence 怎么写） ---
basis: [ ] NL显式义务  [ ] NL欠指定  [ ] 模型自身  [ ] 参考模型
nl_evidence:
--- ③ 边界层 · 它在 M = (S, E, V, Tr, A) 内吗 ---
scope: [ ] 界内  [ ] 越界·时钟或不变式  [ ] 越界·并发或正交区  [ ] 越界·其他
--- ④ 分类轴 · 并表统计用（⛔ 越界条目可不填） ---
direction: [ ] reachability  [ ] hierarchy  [ ] guard  [ ] entry  [ ] effect_action  [ ] event  [ ] cardinality  [ ] unclassified
depth: [ ] 表层  [ ] 中层  [ ] 深层
--- ⑤ 以下三项可留空 ---
reference_side:
primary_predicate:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction

### NEW-{pair}-02
--- ① 事实层 · 看到了什么（⛔ 只写现象，不下判断） ---
statement:
generated_side:
--- ② 依据层 · 凭什么说它是缺陷（⭐ basis 决定 nl_evidence 怎么写） ---
basis: [ ] NL显式义务  [ ] NL欠指定  [ ] 模型自身  [ ] 参考模型
nl_evidence:
--- ③ 边界层 · 它在 M = (S, E, V, Tr, A) 内吗 ---
scope: [ ] 界内  [ ] 越界·时钟或不变式  [ ] 越界·并发或正交区  [ ] 越界·其他
--- ④ 分类轴 · 并表统计用（⛔ 越界条目可不填） ---
direction: [ ] reachability  [ ] hierarchy  [ ] guard  [ ] entry  [ ] effect_action  [ ] event  [ ] cardinality  [ ] unclassified
depth: [ ] 表层  [ ] 中层  [ ] 深层
--- ⑤ 以下三项可留空 ---
reference_side:
primary_predicate:
layer: [ ] wellformedness  [ ] nl_named  [ ] over_specification  [ ] nl_contradiction""")


# 第四代：条件式座标系的**首版**（`defect_element` 只有 7 个取值、没有 `other_note`）。
# 2026-08-13 同日被第五版取代：维度 A 加了界外取值 `region`，并新增条件必填的 `other_note`。
# ⚠️ 冻成字面量的理由与上面三代完全相同 —— 不认出旧模板，54 份工作单的 §5 会**永远**
# 印着七取值的旧表，而 `generate.py --check` 只会报 `unchanged`（实测就是这么发生的）。
LEGACY_NEW_TEMPLATES.append("""### NEW-{pair}-01
defect_locus: [ ] element  [ ] pair  [ ] global  [ ] other
--- 上一行选了 element：填下面两项，跳过 defect_logic_kind ---
defect_element: [ ] state  [ ] transition  [ ] trigger  [ ] guard  [ ] effect  [ ] variable  [ ] other
defect_qualifier: [ ] missing  [ ] incorrect  [ ] extraneous  [ ] other
--- 上一行选了 pair / global / other：跳过上面两项，填下面这一项 ---
defect_logic_kind: [ ] nondeterminism  [ ] incompleteness  [ ] unreachable  [ ] unintended_terminal  [ ] nontermination  [ ] property_violation  [ ] priority_conflict  [ ] hierarchy_entry  [ ] other
--- 以下四项两支都要填 ---
defect_reference: [ ] language  [ ] requirement  [ ] other
statement:
expected_after_fix:
nl_evidence:
--- 以下一项可留空 ---
property_pattern:

### NEW-{pair}-02
defect_locus: [ ] element  [ ] pair  [ ] global  [ ] other
--- 上一行选了 element：填下面两项，跳过 defect_logic_kind ---
defect_element: [ ] state  [ ] transition  [ ] trigger  [ ] guard  [ ] effect  [ ] variable  [ ] other
defect_qualifier: [ ] missing  [ ] incorrect  [ ] extraneous  [ ] other
--- 上一行选了 pair / global / other：跳过上面两项，填下面这一项 ---
defect_logic_kind: [ ] nondeterminism  [ ] incompleteness  [ ] unreachable  [ ] unintended_terminal  [ ] nontermination  [ ] property_violation  [ ] priority_conflict  [ ] hierarchy_entry  [ ] other
--- 以下四项两支都要填 ---
defect_reference: [ ] language  [ ] requirement  [ ] other
statement:
expected_after_fix:
nl_evidence:
--- 以下一项可留空 ---
property_pattern:""")


# 裁决块的历史模板（含已删除的「深度」一栏）。同样只为识别原样未填的旧块 ——
# 不认出来的话，54 份工作单的 99 个裁决区会**永远**印着一个不再存在的字段。
LEGACY_LEDGER_TEMPLATES = ["""裁决: [ ] 保留  [ ] 修正  [ ] 删除  [ ] 拆分
深度: [ ] 表层(单点存在性/拼写)  [ ] 中层(单点关系)  [ ] 深层(跨状态推理/隐含冲突/运行时后果)
理由:
修正后的 statement:"""]

LEGACY_CANDIDATE_TEMPLATES = ["""裁决: [ ] 采纳(补入台账)  [ ] 不采纳  [ ] 待议  [ ] 并入现有条目
深度: [ ] 表层  [ ] 中层  [ ] 深层
并入到:
理由:
补入后的 statement:"""]

_LEGACY_BY_KIND = {
    "new": LEGACY_NEW_TEMPLATES,
    "ledger": LEGACY_LEDGER_TEMPLATES,
    "candidate": LEGACY_CANDIDATE_TEMPLATES,
}


# §4 清单块的「原样未填」判据。清单块与别的块不同：它的**默认内容本身**就是材料
# （逐 pair 现算的检查项），所以材料一变就该重印 —— 而 `render` 默认保留旧内容，
# 于是清单文案的任何更新都到不了工作单里（实测：改了 `checklist.py` 的措辞，
# 54 份工作单一个字都不变，`generate.py --check` 还报 `unchanged`）。
#
# ⚠️ 判据必须比「有没有勾」严：`collect.parse_checklist` **收**清单项下面不带
# `发现:` 前缀的裸文本行，把那种行当成「未填」会**直接删掉人写的发现**。
# 故只在每一行都长成生成器自己会产出的形状时才判未填。
_RE_CHK_EMPTY_ITEM = re.compile(r"^\s*(?:[-*+]\s+)?\[\s*\]\s*[A-Za-z]+-\d+\b")
_RE_CHK_EMPTY_FINDING = re.compile(r"^\s*发现\s*[:：]\s*$")


def checklist_is_untouched(body):
    """清单块里有没有人工内容（勾选、发现、或任何一行生成器不会产出的文本）。"""
    if body is None:
        return False
    if RE_CHECKED_BOX.search(body):
        return False
    for line in body.splitlines():
        if not line.strip():
            continue
        if line.strip().startswith("·"):        # 机器给的机械判据行
            continue
        if _RE_CHK_EMPTY_ITEM.match(line):
            continue
        if _RE_CHK_EMPTY_FINDING.match(line):
            continue
        return False
    return True


def is_stale_template(body, kind, pair=""):
    """该块是不是**原样未填**（因而可以安全换成当前材料 / 当前模板）。

    ⚠️ 对模板类块只做**逐字全等**匹配：作者若已经在旧模板上填了任何东西，
    就不算旧模板，原样保留。
    """
    if body is None:
        return False
    if kind == "checklist":
        return checklist_is_untouched(body)
    return any(body.strip() == t.format(pair=pair).strip()
               for t in _LEGACY_BY_KIND.get(kind, ()))

PAIR_TEMPLATE = """本 pair 整体判断: [ ] 台账在本 pair 上够用  [ ] 偏浅但方向对  [ ] 有实质遗漏  [ ] 需推倒重写
台账现有条目是否偏浅（整体）: [ ] 否  [ ] 部分  [ ] 是
本轮新增条目数:
耗时(分钟):
备注:"""

# ⭐ §0 / §2 / §3 三种块的字段名与勾选字段，逐字从模板算出来（见 `_template_fields`）。
# ⛔ **必须传给 `collect.parse_fields`**，理由与 §5 传 `NF.FIELD_NAMES` 完全相同，
# ⚠️ 而这三种块此前漏了，实测两处静默丢内容：
#   ① `理由:` 的续行里写「NL 第 3 句：模型没有这条边」→ 那一行匹配字段名正则，
#      于是被当成新字段 `NL 第 3 句`，⛔ `理由` 就地截断且**不报错**。
#   ② `修正后的 statement: 缺 [ ] 初始边` → 值里的 `[ ]` 让它被读成勾选行，
#      整个值变成 `{"chosen": [], "options": ["初始边"]}`，⛔ 「缺」两个字连痕迹都没了。
# ⭐ 传了之后：非字段名的续行一律并进当前字段；非勾选字段一律读成文本。
LEDGER_FIELDS, LEDGER_CHOICES = _template_fields(LEDGER_TEMPLATE)
CANDIDATE_FIELDS, CANDIDATE_CHOICES = _template_fields(CANDIDATE_TEMPLATE)
PAIR_FIELDS, PAIR_CHOICES = _template_fields(PAIR_TEMPLATE)

# ⭐ 字段名的宽容变体：`修正后的statement`（漏了空格）也得认。
# ⛔ 不认的后果不是「多一个字段」而是**丢内容**：它会被并进上一个字段，
# ⚠️ 而 [validate.py](./validate.py) 恰恰同时查 `修正后的 statement` 与 `修正后的statement`
# 两种写法 —— ⛔ 只认带空格的那种，等于把 validate 已有的宽容拆掉。
def name_variants(names):
    out = set()
    for n in names:
        out.add(n)
        out.add(n.replace(" ", ""))
        out.add(n.replace("(", "（").replace(")", "）"))
        out.add(n.replace("（", "(").replace("）", ")"))
    return out


def _pair_of(key):
    """从块 key 里取 pair —— §5 的 key 形如 `NEW-0000`。取不到返回空串。"""
    m = re.match(r"^NEW-(\d{4})$", key or "")
    return m.group(1) if m else ""


def extract(text):
    """从既有工作单里抽出 {key: 块内容（不含围栏）}。"""
    out = {}
    if not text:
        return out
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _RE_BEGIN.match(lines[i])
        if not m:
            i += 1
            continue
        key = m.group("key")
        j = i + 1
        body = []
        while j < len(lines) and not _RE_END.match(lines[j]):
            body.append(lines[j])
            j += 1
        # 去掉首尾围栏行
        while body and body[0].strip() == FENCE:
            body.pop(0)
        while body and body[-1].strip() == FENCE:
            body.pop()
        out[key] = "\n".join(body)
        i = j + 1
    return out


def render(key, kind, default_body, saved=None):
    """渲染一个填写块。`saved` 是上一版里同 key 的人工内容，原样注回。

    唯一的例外是**原样未填的历史模板**：它按定义不含任何人工内容，
    留着只会让旧字段表永远印在工作单上，故换成当前模板（见 `is_stale_template`）。
    """
    if is_stale_template(saved, kind, _pair_of(key)):
        saved = None
    body = saved if saved is not None and saved.strip() else default_body
    return "\n".join([
        f"<!-- FILL:BEGIN key={key} kind={kind} -->",
        FENCE,
        body.rstrip(),
        FENCE,
        f"<!-- FILL:END key={key} -->",
    ])


def is_untouched(body, kind, pair="", key=None):
    """块是否仍为模板原样（没有任何勾选、没有任何自由文本）。

    ⚠️ 勾选判据走 `RE_CHECKED_BOX`（即 `CHECK_MARKS` 那套记号），⛔ 不是字面 `"[x]"` ——
    ⛔ 后者会把**只用 `[✓]` 勾选**的块报成「原样未填」，而 `collect.py` 那边明明认了它。
    ⭐ 两边读同一份记号真源，这类分歧才不可能再出现。
    """
    # ⭐⭐ 预填体也算「原样未填」。⛔ 2026-08-14 起裁决区带我方预填（三方判读的决议），
    # ⚠️ 若不认它，380 条一上线进度统计立刻全变「已填」——⛔ 与 2026-08-13 栽过的
    # 「幂等注回把旧模板当人工内容」是同型 bug。⭐ 判据走**逐字全等**，同 `is_stale_template`。
    if key:
        try:
            import dtier as _DT
            pre = _DT.prefill(key, kind)
        except Exception:
            pre = None
        if pre is not None and body.strip() == pre.strip():
            return True
    defaults = {
        "ledger": LEDGER_TEMPLATE,
        "candidate": CANDIDATE_TEMPLATE,
        "new": new_template(pair),
        "pair": PAIR_TEMPLATE,
    }
    d = defaults.get(kind)
    if d is not None and body.strip() == d.strip():
        return True
    if RE_CHECKED_BOX.search(body):
        return False
    # 检查有没有在冒号后写了东西
    for line in body.splitlines():
        if ":" in line:
            tail = line.split(":", 1)[1].strip()
            if tail and not tail.startswith("["):
                return False
    return True
