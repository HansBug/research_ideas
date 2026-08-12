"""§4 深度检查清单的生成 —— ⛔ 逐 pair 点名真实元素，不给通用模板。

设计原则：

1. **每一条都点名本 pair 的具体元素与行号。** 通用模板（「有没有不可达状态？」）
   在 54 份文件里重复 54 遍等于没写；作者需要的是「`CollisionAvoidance`（:37）
   没有任何入边，它可达吗」。
2. **⛔ 清单给的是问题，不是答案。** 机械分析会误判（守卫互斥性需要语义、外层
   出边的下推需要 UML 语义、PlantUML 作用域规则有陷阱），所以每一条都写成待核问句，
   且注明机械判据是什么。作者可以直接判「机械判错了」。
3. **不重复台账已覆盖的。** 若某条线索点名的元素恰好已被本 pair 的台账条目覆盖，
   标注 `↺ 台账 EIS-xxxx-yy 已涉及`，让作者优先看没被覆盖的。
4. **⛔ 不含时钟 / 不变式 / 并发的检查项** —— 建模对象边界之外（$M$ 无 $C$、无 $Inv$、
   无正交区）。唯一例外是 NL 侧的「持续 / 时限」义务：那一条问的是**结构上有没有
   对应承载**，不是要求建时钟。
"""

from __future__ import annotations

import re

from pumlmodel import PSEUDO

# NL 侧的义务关键词。命中只说明「这句话可能带一条结构义务」，⛔ 不是缺陷判据。
NL_CUES = [
    ("持续 / 保持", r"\b(until|as long as|continues?|remains?|keeps?|persist\w*|while)\b"),
    ("时限 / 之内", r"\b(within|before|after|by the time|timeout|immediately|then)\b"),
    ("全称 / 任意时刻", r"\b(always|never|any time|at all times|whenever|each time|every time|must not|shall not|cannot)\b"),
    ("数量断言", r"\b(one|two|three|four|five|six|seven|eight|nine|ten|single|only|exactly|both|all of|three main|two main)\b"),
    ("默认 / 起点", r"\b(initial\w*|begins?|starts?|default|first|entry point)\b"),
    ("终止 / 完成", r"\b(final|terminat\w*|complete[ds]?|finish\w*|end[s]?|shut\s?down|power off)\b"),
    ("互斥 / 条件分支", r"\b(either|otherwise|else|unless|only if|if and only if|mutually)\b"),
    ("返回 / 复位", r"\b(returns? to|back to|resets?|reverts?|restores?)\b"),
    ("变量 / 计数", r"\b(increment\w*|decrement\w*|counter|count|set to|becomes|value of|equals?)\b"),
]

_EXISTENCE_PREDICATES = {
    "state_declared", "event_declared", "variable_declared", "effect_declared",
    "action_declared", "edge_declared", "containment",
}


def _elements_named_by_ledger(records):
    named = set()
    for r in records:
        for a in r.get("assertions") or []:
            for e in a.get("elements") or []:
                named.add(e.split(".")[-1])
        blob = (r.get("statement") or "") + " " + (r.get("generated_side") or "")
        for tok in re.findall(r"[A-Za-z_][A-Za-z0-9_]{2,}", blob):
            named.add(tok)
    return named


def _covered_note(names, records):
    """若某些元素名已被台账条目点到，回一条提示串。"""
    hits = []
    for r in records:
        blob = (r.get("statement") or "") + " " + (r.get("generated_side") or "") + " " \
            + " ".join(str(a.get("expression") or "") for a in (r.get("assertions") or []))
        for n in names:
            if n and re.search(r"\b" + re.escape(n) + r"\b", blob):
                hits.append(r["id"])
                break
    if not hits:
        return ""
    uniq = sorted(set(hits))
    return f"  ↺ 台账 {' / '.join(uniq)} 已涉及该元素 —— 请判它是否**已经说到位**。"


class Item:
    __slots__ = ("iid", "text", "basis")

    def __init__(self, iid, text, basis=""):
        self.iid = iid
        self.text = text
        self.basis = basis


def build(model, nl_segs, records, pair):
    """返回 [(分类标题, 分类说明, [Item])]。"""
    cats = []
    R = records

    # ---------------------------------------------------------- 可达性
    items = []
    n = 0
    unreach = model.unreachable_states()
    for s in unreach:
        n += 1
        st = model.states[s]
        loc = f":{st.decl_line}" if st.decl_line else "（无声明行，仅作为迁移端点出现）"
        items.append(Item(
            f"REACH-{n:02d}",
            f"`{s}`{loc} 从根初始配置**不可达**。这是缺陷，还是机械判据没算到某条入边？",
            "机械判据：从顶层 `[*]` 出边出发，进入复合态时跟随其区域初始边，"
            "复合态出边视为其全部后代共享；守卫一律视为可满足。"
            + _covered_note([s], R),
        ))
    absorbing = [s for s in model.absorbing_states()
                 if not any(t.dst == PSEUDO for t in model.outgoing_including_inherited(s))]
    for s in absorbing:
        n += 1
        st = model.states[s]
        loc = f":{st.decl_line}" if st.decl_line else ""
        inbound = [t.line for t in model.transitions if t.dst == s]
        items.append(Item(
            f"REACH-{n:02d}",
            f"`{s}`{loc} 是**吸收态**：自身与全部祖先都没有出边"
            f"（入边在 {', '.join(':' + str(x) for x in inbound) or '无'}）。"
            f"NL 要求进入它之后还能出来吗？它是不是本该写成终态伪状态 `[*]`？",
            "机械判据：`src == s` 或 `src ∈ ancestors(s)` 的迁移为空集。"
            + _covered_note([s], R),
        ))
    root_inits = model.initial_edges(None)
    if not root_inits:
        n += 1
        items.append(Item(
            f"REACH-{n:02d}",
            "模型**没有顶层初始边**（全文无 `[*] --> X` 出现在顶层作用域）。"
            "整台机器的起点未定义 —— 台账记了吗？",
            "机械判据：`scope is None and src == '[*]'` 的迁移数为 0。",
        ))
    elif len(root_inits) > 1:
        n += 1
        desc = "、".join(f"`{t.src} --> {t.dst}"
                        + (f" : {t.label}" if t.label else "") + f"`（:{t.line}）"
                        for t in root_inits)
        items.append(Item(
            f"REACH-{n:02d}",
            f"顶层有 **{len(root_inits)} 条初始边**：{desc}。"
            "冷启动时进入哪一个是未定义的；其中有没有本该挂在某个运行态上的边？",
            "机械判据：顶层 `[*] -->` 边计数 > 1。"
            + _covered_note([t.dst for t in root_inits], R),
        ))
    finals = [t for t in model.transitions if t.dst == PSEUDO]
    if not finals:
        n += 1
        names = [s for s in model.states
                 if re.search(r"final|finish|end|complete|terminat|off|shut",
                              s, flags=re.I)]
        extra = ""
        if names:
            extra = ("⚠️ 但存在名字像终态的普通状态：" +
                     "、".join(f"`{x}`" for x in sorted(names)) +
                     " —— 名字像终态**不等于**是终态。")
        items.append(Item(
            f"REACH-{n:02d}",
            f"模型里**没有任何终态伪状态**（无 `--> [*]` 边）。机器永远不会 terminate。{extra}"
            "NL 有没有要求「结束 / 关机 / 完成」？",
            "机械判据：`dst == '[*]'` 的迁移数为 0。" + _covered_note(names, R),
        ))
    if items:
        cats.append((
            "可达性与终止",
            "⭐ 台账的 `reachability` 方向共 25 条，是最大的一类；"
            "但 X1 的真漏记里**吸收态 / 死端**反复出现，说明这一类仍有漏。",
            items,
        ))

    # ---------------------------------------------------------- 守卫与确定性
    items = []
    n = 0
    for (src, trig), ts in sorted(model.nondet_groups().items()):
        if src == PSEUDO:
            continue
        guards = [(t.line, t.guard or "（无守卫）", t.dst) for t in ts]
        trig_desc = f"触发 `{trig}`" if trig else "**无触发**（完成迁移）"
        body = "；".join(f":{ln} → `{dst}` 守卫 `{g}`" for ln, g, dst in guards)
        n += 1
        items.append(Item(
            f"GUARD-{n:02d}",
            f"`{src}` 上有 {len(ts)} 条同源同触发出边（{trig_desc}）：{body}。"
            "这些守卫两两互斥吗？有没有某个取值下**两条都成立**（非确定）"
            "或**一条都不成立**（覆盖缺口）？",
            "机械判据：按 `(src, trigger)` 分桶后桶内 > 1 条；"
            "⛔ 互斥性本身机械判不了，需要读守卫语义。"
            + _covered_note([src] + [d for _, _, d in guards], R),
        ))
    guardless = [t for t in model.transitions
                 if t.src != PSEUDO and not t.guard and not t.trigger]
    if guardless:
        n += 1
        body = "、".join(f"`{t.src} --> {t.dst}`（:{t.line}）" for t in guardless[:8])
        more = f" 等 {len(guardless)} 条" if len(guardless) > 8 else ""
        items.append(Item(
            f"GUARD-{n:02d}",
            f"以下迁移**既无触发也无守卫**：{body}{more}。"
            "它们在 UML 下是完成迁移，源态一进入就立刻离开 —— NL 是这个意思吗？",
            "机械判据：`trigger == '' and guard == ''`。",
        ))
    # 守卫被写进 trigger 槽
    misplaced = [t for t in model.transitions
                 if t.trigger and not t.guard
                 and re.search(r"(>=|<=|==|!=|=|>|<)", t.trigger)]
    if misplaced:
        n += 1
        body = "、".join(f":{t.line} `{t.label}`" for t in misplaced[:8])
        more = f" 等 {len(misplaced)} 条" if len(misplaced) > 8 else ""
        items.append(Item(
            f"GUARD-{n:02d}",
            f"以下标签把**比较表达式写在了触发槽**（没有方括号）：{body}{more}。"
            "作者是想写守卫还是想写事件名？这两种读法的后果不同 —— "
            "当事件名读，则它永远不会被外部触发；当守卫读，则它是完成迁移。",
            "机械判据：`trigger` 含比较算子且 `guard` 为空。⛔ 词法判据，可能误伤"
            "（真事件名里也可能有 `=`）。",
        ))
    guarded_only = [t for t in model.transitions
                    if t.guard and not t.trigger and t.src != PSEUDO]
    if guarded_only:
        n += 1
        body = "、".join(f":{t.line} `{t.src} --> {t.dst} : [{t.guard}]`"
                         for t in guarded_only[:6])
        more = f" 等 {len(guarded_only)} 条" if len(guarded_only) > 6 else ""
        items.append(Item(
            f"GUARD-{n:02d}",
            f"以下迁移**只有守卫、没有触发**：{body}{more}。"
            "若源态是复合态，UML 的守卫化完成迁移要等它**完成**（内部到达终态）才求值 —— "
            "该复合态里有终态吗？没有的话这条边永不触发。",
            "机械判据：`guard != '' and trigger == ''`。",
        ))
    if items:
        cats.append((
            "守卫与确定性",
            "⭐ 台账 `guard` 方向 22 条，但 `guard_distinguishable` 只做过 5 次 primary；"
            "⚠️ 且该谓词在单目标时空真返回 `True`，「这条边必须带区分条件」写不出来 —— "
            "这一类的**谓词承载本身就有缺口**。",
            items,
        ))

    # ---------------------------------------------------------- 层次语义
    items = []
    n = 0
    for s in model.composites_without_initial():
        n += 1
        st = model.states[s]
        kids = "、".join(f"`{k}`" for k in st.children)
        items.append(Item(
            f"HIER-{n:02d}",
            f"复合态 `{s}`（:{st.decl_line}）有 {len(st.children)} 个子态（{kids}）"
            f"但**没有区域初始边**。进入它之后活动子态未定义 —— "
            "是漏了 `[*] --> X`，还是它本来就不该是复合态？",
            "机械判据：该 scope 内无 `[*] -->` 边。" + _covered_note([s] + st.children, R),
        ))
    for t in model.cross_scope_targets():
        n += 1
        items.append(Item(
            f"HIER-{n:02d}",
            f":{t.line} `{t.src} --> {t.dst}` 的目标 `{t.dst}` 既不在本作用域 "
            f"`{t.scope}` 内，也不在它的祖先 / 后代链上。这是有意的跨层跳转，"
            "还是把某个名字**写在了错误的层级**？",
            "机械判据：`dst ∉ scope ∪ descendants(scope) ∪ ancestors(scope) ∪ 顶层态`。"
            + _covered_note([t.src, t.dst], R),
        ))
    for name, use_line, use_scope, decl_line, parent in model.forward_references():
        n += 1
        items.append(Item(
            f"HIER-{n:02d}",
            f"`{name}` 在 :{use_line}（作用域 `{use_scope or '顶层'}`）**先被引用**，"
            f"到 :{decl_line} 才在 `{parent or '顶层'}` 里被声明。"
            "PlantUML 会把它钉在首次出现的作用域 —— 作者想要的层级是哪个？"
            "这会不会把本该是兄弟的态变成了子态（或反过来）？",
            "机械判据：首次作为迁移端点出现的行号 < `state X` 声明行号。"
            + _covered_note([name], R),
        ))
    for s in sorted(model.implicit_states()):
        n += 1
        refs = [t.line for t in model.transitions if s in (t.src, t.dst)]
        items.append(Item(
            f"HIER-{n:02d}",
            f"`{s}` **从未被 `state` 声明**，只在 "
            f"{', '.join(':' + str(x) for x in refs)} 作为迁移端点出现。"
            "PlantUML 会隐式建它 —— 作者是有意省略，还是漏了它的子结构 / 描述 / 终态标记？",
            "机械判据：无 `state <name>` 行。⚠️ 「未声明」本身在 PlantUML 里不是错误，"
            "承重的是它**因此缺了什么**。" + _covered_note([s], R),
        ))
    # cardinality
    for s, st in sorted(model.states.items()):
        if len(st.children) >= 2:
            hint = _covered_note([s], R)
            n += 1
            items.append(Item(
                f"HIER-{n:02d}",
                f"复合态 `{s}` 直接子态 **{len(st.children)}** 个："
                + "、".join(f"`{k}`" for k in st.children)
                + "。NL 有没有对这里的数量给出显式断言（「三个子状态」之类）？数对得上吗？",
                "机械判据：直接子态计数（⛔ 作者源口径，不含投影合成的占位符 —— "
                "谓词层的 `cardinality` 会把它们算进去，两者可能不同）。" + hint,
            ))
    if items:
        cats.append((
            "层次语义",
            "⭐ 台账 `hierarchy` 21 条 + `entry` 23 条，主要靠 `initial_target`（21 次 primary）"
            "与 `containment`（12 次）。⚠️ 但 `initial_target` 看不到**带触发的初始边**，"
            "该族缺陷会被正向放过。",
            items,
        ))

    # ---------------------------------------------------------- 事件
    items = []
    n = 0
    trigs = model.triggers()
    once = {k: v for k, v in trigs.items() if len(v) == 1}
    if trigs:
        n += 1
        body = "、".join(f"`{k}`（{len(v)}×）" for k, v in sorted(trigs.items()))
        items.append(Item(
            f"EVT-{n:02d}",
            f"模型用到的触发词共 {len(trigs)} 个：{body}。"
            "NL 里点名的事件是不是都在这份表里？表里有没有 NL 从没提过的（过度规定）？",
            "机械判据：迁移标签触发槽的去重集合。⚠️ PlantUML 没有事件声明段，"
            "「声明」只能等同于「出现过」。",
        ))
    if once:
        n += 1
        body = "、".join(f"`{k}`（:{v[0]}）" for k, v in sorted(once.items())[:10])
        more = f" 等 {len(once)} 个" if len(once) > 10 else ""
        items.append(Item(
            f"EVT-{n:02d}",
            f"以下触发词**全模型只用了一次**：{body}{more}。"
            "NL 要求它在别的状态下也被响应吗？"
            "⭐ 「同一事件只在一个子态被消费、在兄弟态被静默丢弃」是 X1 真漏记里出现过的形态。",
            "机械判据：触发词出现次数 == 1。",
        ))
    # 同一事件在不同层级
    by_trig = {}
    for t in model.transitions:
        if t.trigger:
            by_trig.setdefault(t.trigger, []).append(t)
    for k, ts in sorted(by_trig.items()):
        scopes = {t.scope for t in ts}
        if len(scopes) > 1:
            n += 1
            body = "；".join(f":{t.line} 在 `{t.scope or '顶层'}` 上 "
                            f"`{t.src} --> {t.dst}`" for t in ts)
            items.append(Item(
                f"EVT-{n:02d}",
                f"触发词 `{k}` 在 **{len(scopes)} 个不同层级**上都有迁移：{body}。"
                "内层与外层同时使能时哪条胜出？UML 里内层优先 —— 那是 NL 想要的吗？",
                "机械判据：同一 trigger 的迁移分布在多个 scope。"
                + _covered_note([k], R),
            ))
    if items:
        cats.append((
            "事件",
            "⭐ 台账 `event` 方向只有 **4** 条，`event_declared` / `event_consumed` "
            "各只做过 4 次 primary —— ⛔ 这一维几乎是空的，最可能有漏。",
            items,
        ))

    # ---------------------------------------------------------- 变量与效应
    items = []
    n = 0
    vars_ = model.variable_candidates()
    effects = model.effects()
    if vars_:
        n += 1
        body = "、".join(
            f"`{v}`（{', '.join(sorted({s for _, s, _ in occ}))}；"
            f"{', '.join(':' + str(l) for l, _, _ in occ[:4])}）"
            for v, occ in sorted(vars_.items()))
        items.append(Item(
            f"VAR-{n:02d}",
            f"守卫 / 标签里出现的变量候选：{body}。"
            "这些变量有**任何一处被更新**吗？只读不写的变量意味着守卫永远停在初值。",
            "机械判据：从 `x op v` 的左值抽取。⛔ 词法启发式，可能把事件名误当变量。",
        ))
        written = set()
        for v in vars_:
            for occ_line, slot, _ in vars_[v]:
                if slot == "effect":
                    written.add(v)
        never_written = sorted(set(vars_) - written)
        if never_written:
            n += 1
            items.append(Item(
                f"VAR-{n:02d}",
                "以下变量候选**只在守卫 / 触发槽出现，从未在任何效应里被赋值**："
                + "、".join(f"`{v}`" for v in never_written)
                + "。NL 说过谁改它们吗？若 NL 要求某个动作改变它而模型没写，"
                "那就是一条 `V` 维缺陷。",
                "机械判据：变量候选未出现在任何 `/ effect` 段的左值位置。",
            ))
    if effects:
        n += 1
        body = "、".join(f"`{k}`（{', '.join(':' + str(x) for x in v)}）"
                         for k, v in sorted(effects.items())[:10])
        more = f" 等 {len(effects)} 条" if len(effects) > 10 else ""
        items.append(Item(
            f"VAR-{n:02d}",
            f"迁移效应（`/` 之后）共 {len(effects)} 处：{body}{more}。"
            "NL 要求的动作是不是都有对应？方向对吗（该增的没减、该发的没发）？",
            "机械判据：标签里第一个顶层 `/` 之后的文本。",
        ))
    acts = model.state_actions()
    if acts:
        n += 1
        body = "、".join(f"`{s}`:{ln} `{d}`" for s, ln, d in acts[:8])
        items.append(Item(
            f"VAR-{n:02d}",
            f"状态内动作（entry/do/exit）共 {len(acts)} 处：{body}。"
            "NL 要求的状态内行为是不是都落在了这里？"
            "有没有本该是动作、却被写成了独立事件或状态名的一部分？",
            "机械判据：状态描述行匹配 `^(entry|do|exit|during)\\s*/`。",
        ))
    else:
        descs = [(nm, ln, d) for nm, s in model.states.items()
                 for ln, d in s.descriptions]
        if descs:
            n += 1
            body = "、".join(f"`{nm}`:{ln} `{d}`" for nm, ln, d in descs[:8])
            more = f" 等 {len(descs)} 处" if len(descs) > 8 else ""
            items.append(Item(
                f"VAR-{n:02d}",
                f"模型**没有任何 entry/do/exit 动作**，但有 {len(descs)} 条状态描述行："
                f"{body}{more}。"
                "⭐ 这些描述里有没有本该是**动作**的内容被降级成了纯文本？"
                "（NL 要求「发出信号 X」而模型把 X 写进了状态名或描述串，是已知形态。）",
                "机械判据：无 entry/do/exit 匹配，但存在 `X : text` 描述行。",
            ))
    if items:
        cats.append((
            "变量与效应",
            "⛔ **台账的变量维几乎是空的**：`variable_declared` 与 `variable_delta_after` "
            "**从未作为 primary 出现过**，`effect_declared` 3 次、`action_declared` 6 次。"
            "⚠️ 已知原因之一：全语料唯一被投影声明的变量是 `R45RouteToken`，"
            "所以谓词层几乎无从验证 —— ⭐ 但那是**谓词的**缺口，不代表模型没有变量缺陷。",
            items,
        ))

    # ---------------------------------------------------------- 时序 / 持续义务
    items = []
    n = 0
    for cue_name, pattern in NL_CUES[:3]:
        rx = re.compile(pattern, flags=re.I)
        hits = [(sid, txt) for sid, txt in nl_segs if rx.search(txt)]
        if not hits:
            continue
        n += 1
        body = "；".join(f"**{sid}**「{txt.strip()[:160]}」" for sid, txt in hits[:4])
        more = f"（共 {len(hits)} 段命中）" if len(hits) > 4 else ""
        items.append(Item(
            f"TEMP-{n:02d}",
            f"NL 中带「{cue_name}」义务的句子：{body}{more}。"
            "模型里有没有**结构**承载这条义务？"
            "⛔ 注意不是要求建时钟 —— 问的是「持续到 X 之前不许离开」有没有对应的"
            "缺边 / 守卫 / 层次结构。",
            f"机械判据：正则 `{pattern}` 命中该 NL 段。⛔ 词法线索，不是缺陷判据。",
        ))
    if items:
        cats.append((
            "时序 / 持续义务",
            "⭐ `persists_until` 只做过 3 次 primary，`response_within` 与 `invariant` "
            "**从未作为 primary 出现** —— ⛔ 台账在这一维基本没有覆盖。"
            "⚠️ 建模对象无时钟，所以这里要找的是**结构性**承载，不是时间约束。",
            items,
        ))

    # ---------------------------------------------------------- 跨状态一致性
    items = []
    n = 0
    leaves = [s for s, st in model.states.items() if not st.children]
    resp = {}
    for t in model.transitions:
        if t.src == PSEUDO or not t.trigger:
            continue
        resp.setdefault(t.trigger, {}).setdefault(t.src, []).append(t)
    for trig, bysrc in sorted(resp.items()):
        if len(bysrc) < 2:
            continue
        dests = {t.dst for ts in bysrc.values() for t in ts}
        if len(dests) < 2:
            continue
        n += 1
        body = "；".join(f"`{src}` → " + "/".join(f"`{t.dst}`" for t in ts)
                         for src, ts in sorted(bysrc.items()))
        items.append(Item(
            f"XSTATE-{n:02d}",
            f"事件 `{trig}` 在不同状态下被导向**不同目标**：{body}。"
            "NL 是否要求它有统一后果？不同的目标彼此矛盾吗？",
            "机械判据：同一 trigger 有 ≥2 个不同源态且 ≥2 个不同目标。"
            + _covered_note([trig], R),
        ))
    # 没有任何出边消费事件的叶态
    silent = []
    for s in leaves:
        outs = model.outgoing_including_inherited(s)
        if outs and not any(t.trigger for t in outs):
            silent.append(s)
    if silent:
        n += 1
        items.append(Item(
            f"XSTATE-{n:02d}",
            "以下叶态的全部出边（含祖先下推）**都没有触发词**，即它们不响应任何事件："
            + "、".join(f"`{x}`" for x in sorted(silent)[:10])
            + "。NL 要求它们对某个事件有反应吗？",
            "机械判据：`outgoing_including_inherited(s)` 非空但全部 trigger 为空。",
        ))
    if items:
        cats.append((
            "跨状态一致性",
            "⭐ 这一类在台账里没有独立方向（`unclassified` 只有 7 条），"
            "而它恰好需要**跨状态推理** —— ⛔ 是「深层」缺陷最可能藏身的地方。",
            items,
        ))

    # ---------------------------------------------------------- NL 未明说但结构可疑
    items = []
    n = 0
    named_in_nl = set()
    nl_blob = " ".join(t for _, t in nl_segs)
    for s in model.states:
        norm = re.sub(r"[_\s]", "", s).lower()
        blob_norm = re.sub(r"[_\s]", "", nl_blob).lower()
        if norm and norm in blob_norm:
            named_in_nl.add(s)
    invented = sorted(set(model.states) - named_in_nl)
    if invented:
        n += 1
        items.append(Item(
            f"STRUCT-{n:02d}",
            "以下状态名在 NL 里**找不到对应词**（去下划线 / 空格后子串匹配）："
            + "、".join(f"`{x}`" for x in invented[:12])
            + (f" 等 {len(invented)} 个" if len(invented) > 12 else "")
            + "。它们是合理的实现细节，还是**过度规定**（模型凭空造出 NL 没要求的结构）？",
            "机械判据：状态名规范化后不是 NL 全文的子串。⛔ 词法判据，"
            "同义改写（`HumanDrivingMode` vs `human driving mode`）能匹配上，"
            "但语义改写匹配不上。" + _covered_note(invented[:12], R),
        ))
    invented_trigs = []
    for k in model.triggers():
        norm = re.sub(r"[_\s]", "", k).lower()
        blob_norm = re.sub(r"[_\s]", "", nl_blob).lower()
        if norm and norm not in blob_norm:
            invented_trigs.append(k)
    if invented_trigs:
        n += 1
        items.append(Item(
            f"STRUCT-{n:02d}",
            "以下触发词在 NL 里找不到对应："
            + "、".join(f"`{x}`" for x in sorted(invented_trigs)[:12])
            + "。是自造事件（过度规定），还是 NL 某句的合理形式化？",
            "机械判据：同上。" + _covered_note(invented_trigs[:12], R),
        ))
    for t in model.initial_edges_with_trigger():
        n += 1
        items.append(Item(
            f"STRUCT-{n:02d}",
            f":{t.line} `[*] --> {t.dst} : {t.label}` —— **初始伪状态的出边带了触发 / 守卫**。"
            "UML 2.5 §14.2.3.8 禁止这一点；后果是该事件到达前整机无活动状态。"
            "台账记了这一处吗？",
            "机械判据：`src == '[*]'` 且 trigger 或 guard 非空。"
            + _covered_note([t.dst], R),
        ))
    if items:
        cats.append((
            "NL 未明说但结构上可疑",
            "⭐ 这类在台账里占 30/98（`wellformedness` 层），⛔ 也正是 X1 强而主臂弱的地方 —— "
            "X1 的 13 条真漏记里 **9 条**被判为 `V1`/`V2`（合式性层，不要求 NL 逐字依据）。",
            items,
        ))

    return cats
