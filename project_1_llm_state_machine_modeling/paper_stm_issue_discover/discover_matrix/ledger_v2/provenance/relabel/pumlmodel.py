"""PlantUML 状态图的轻量解析器 —— 供人工重标材料生成使用。

⛔ 这里**只读作者源 `stm0.puml`**，不读 `model.fcstm`、不读 `fcstm_meta.json`。
理由：台账现有条目里有相当一部分是「读了 fcstm 投影」写出来的，而投影会合成
`UnspecifiedInitial` / `InvalidInitial*` / `FinalWait*` / `R45RouteToken` 这些
作者从未写过的元素。人工重标要判的是**作者写了什么**，所以结构摘要与检查清单
必须锚在作者源上。若某条判断确实需要投影视角，作者在裁决理由里自行注明。

解析目标是 $M = (S, E, V, Tr, A)$：状态、事件、变量、迁移、动作。
⛔ 不解析时钟与不变式（project_1 建模对象边界之外）。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


PSEUDO = "[*]"

# `state "Long" as X` / `state ""Long"" as X` / `state X as "Long"` / `state X`
_RE_STATE_HEAD = (
    r'^state\s+(?:'
    r'"{1,2}(?P<alias>[^"]*)"{1,2}\s+as\s+(?P<asname>[\w.]+)'
    r'|(?P<name2>[\w.]+)\s+as\s+"{1,2}(?P<alias2>[^"]*)"{1,2}'
    r'|(?P<name>[\w.]+)'
    r')'
)
_RE_STATE_OPEN = re.compile(_RE_STATE_HEAD + r'\s*(?P<stereo><<[^>]*>>)?\s*\{\s*$')
_RE_STATE_DECL = re.compile(
    _RE_STATE_HEAD + r'\s*(?P<stereo><<[^>]*>>)?\s*(?::\s*(?P<desc>.*?))?\s*$'
)
_RE_TRANS = re.compile(
    r'^(?P<src>\[\*\]|"[^"]+"|[\w.]+)\s*'
    r'(?P<arrow>-{1,2}(?:up|down|left|right|u|d|l|r)?(?:\[[^\]]*\])?-{0,2}>)\s*'
    r'(?P<dst>\[\*\]|"[^"]+"|[\w.]+)\s*'
    r'(?::\s*(?P<label>.*?))?\s*$'
)
_RE_DESC = re.compile(r'^(?P<name>[\w.]+)\s*:\s*(?P<desc>.*?)\s*$')

_SKIP_PREFIX = (
    "@startuml", "@enduml", "note", "end note", "hide", "skinparam", "title",
    "legend", "end legend", "scale", "!", "caption", "footer", "header",
)

# 出现在守卫 / 效应里的比较与赋值算子，用来抽变量名
_RE_IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')
_RE_COMPARISON = re.compile(
    r'(?P<lhs>[A-Za-z_][A-Za-z0-9_.]*)\s*(?P<op>>=|<=|==|!=|=|>|<)\s*(?P<rhs>[^\s&|,\]]+)'
)


@dataclass
class State:
    name: str
    parent: Optional[str]
    depth: int
    decl_line: Optional[int] = None       # `state X` / `state X { ` 出现的行
    open_block: bool = False              # 是否写成 `state X { ... }`
    stereotype: Optional[str] = None
    descriptions: list = field(default_factory=list)   # [(line, text)]
    implicit: bool = False                # 仅作为迁移端点出现，从未 `state X` 声明
    children: list = field(default_factory=list)
    regions: int = 1                      # `--` 分隔出的区数


@dataclass
class Transition:
    line: int
    src: str
    dst: str
    label: str
    scope: Optional[str]                  # 该行所在的复合态（None = 顶层）
    trigger: str = ""
    guard: str = ""
    effect: str = ""
    raw_arrow: str = ""


def _unquote(tok: str) -> str:
    tok = tok.strip()
    if len(tok) >= 2 and tok[0] == '"' and tok[-1] == '"':
        return tok[1:-1]
    return tok


def split_label(label: str) -> tuple:
    """把迁移标签拆成 (trigger, guard, effect)。

    ⚠️ 这是**词法**拆分，不是语义裁定。PlantUML 的标签槽位很松，作者常把守卫写进
    trigger 槽（`dist_to_front > 10`），也常把动作写进状态描述。拆分结果只用于
    生成提问线索，⛔ 不作为任何判据。
    """
    if not label:
        return "", "", ""
    s = label.strip()
    s = re.sub(r'<<[^>]*>>', '', s).strip()
    s = re.sub(r'\{[^}]*\}', '', s).strip()

    guard = ""
    m = re.search(r'\[(?P<g>[^\]]*)\]', s)
    if m:
        guard = m.group('g').strip()
        s = (s[:m.start()] + " " + s[m.end():]).strip()

    effect = ""
    depth = 0
    cut = -1
    for i, ch in enumerate(s):
        if ch == '[':
            depth += 1
        elif ch == ']':
            depth -= 1
        elif ch == '/' and depth == 0:
            cut = i
            break
    if cut >= 0:
        effect = s[cut + 1:].strip()
        s = s[:cut].strip()

    trigger = s.strip()
    if not guard and trigger and _RE_COMPARISON.search(trigger) and not effect:
        # 作者把守卫写进了 trigger 槽 —— 记为 trigger，但在检查清单里点名
        pass
    return trigger, guard, effect


class PumlModel:
    def __init__(self, text: str, pair: str = ""):
        self.pair = pair
        self.raw = text
        self.lines = text.splitlines()
        self.states: dict = {}
        self.transitions: list = []
        self.parse_warnings: list = []
        self.unparsed_lines: list = []
        self.region_separators: list = []   # [(line, scope)]
        self._parse()

    # ---------- 解析 ----------

    def _ensure(self, name: str, parent, depth: int, implicit=True) -> State:
        if name == PSEUDO:
            return None
        st = self.states.get(name)
        if st is None:
            st = State(name=name, parent=parent, depth=depth, implicit=implicit)
            self.states[name] = st
            if parent and parent in self.states:
                self.states[parent].children.append(name)
        return st

    def _parse(self):
        stack = []           # 复合态名字栈
        in_note = False
        for no, raw in enumerate(self.lines, start=1):
            line = raw.strip()
            if not line:
                continue
            if line.startswith("'") or line.startswith("/'"):
                continue
            low = line.lower()
            if in_note:
                if low.startswith("end note"):
                    in_note = False
                continue
            if low.startswith("note") and not low.startswith("note "):
                continue
            if low.startswith("note"):
                if ":" not in line:
                    in_note = True
                continue
            if any(low.startswith(p) for p in _SKIP_PREFIX):
                continue

            scope = stack[-1] if stack else None
            depth = len(stack)

            if line == "}":
                if stack:
                    stack.pop()
                else:
                    self.parse_warnings.append(f"L{no}: 多余的 `}}`")
                continue

            if re.fullmatch(r'-{2,}', line) or line == "--" or re.fullmatch(r'\|{2,}', line):
                self.region_separators.append((no, scope))
                if scope and scope in self.states:
                    self.states[scope].regions += 1
                continue

            m = _RE_STATE_OPEN.match(line)
            if m:
                name = m.group('asname') or m.group('name2') or m.group('name')
                st = self._ensure(name, scope, depth, implicit=False)
                st.implicit = False
                st.open_block = True
                st.decl_line = st.decl_line or no
                st.stereotype = st.stereotype or m.group('stereo')
                if st.parent is None and scope is not None:
                    st.parent = scope
                    st.depth = depth
                    if scope in self.states and name not in self.states[scope].children:
                        self.states[scope].children.append(name)
                stack.append(name)
                continue

            m = _RE_TRANS.match(line)
            if m:
                src = _unquote(m.group('src'))
                dst = _unquote(m.group('dst'))
                label = (m.group('label') or "").strip()
                tr = Transition(line=no, src=src, dst=dst, label=label, scope=scope,
                                raw_arrow=m.group('arrow'))
                tr.trigger, tr.guard, tr.effect = split_label(label)
                self.transitions.append(tr)
                for endpoint in (src, dst):
                    if endpoint != PSEUDO:
                        self._ensure(endpoint, scope, depth, implicit=True)
                continue

            m = _RE_STATE_DECL.match(line)
            if m:
                name = m.group('asname') or m.group('name2') or m.group('name')
                st = self._ensure(name, scope, depth, implicit=False)
                st.implicit = False
                st.decl_line = st.decl_line or no
                st.stereotype = st.stereotype or m.group('stereo')
                if m.group('desc'):
                    st.descriptions.append((no, m.group('desc').strip()))
                if st.parent is None and scope is not None:
                    st.parent = scope
                    st.depth = depth
                    if scope in self.states and name not in self.states[scope].children:
                        self.states[scope].children.append(name)
                continue

            m = _RE_DESC.match(line)
            if m:
                name = m.group('name')
                st = self._ensure(name, scope, depth, implicit=True)
                if st is not None:
                    st.descriptions.append((no, m.group('desc').strip()))
                continue

            self.unparsed_lines.append((no, line))

        if stack:
            self.parse_warnings.append(f"未闭合的复合态: {stack}")

    # ---------- 派生视图 ----------

    def initial_edges(self, scope=None):
        return [t for t in self.transitions if t.src == PSEUDO and t.scope == scope]

    def final_edges(self, scope=None):
        return [t for t in self.transitions if t.dst == PSEUDO and t.scope == scope]

    def composites(self):
        return [n for n, s in self.states.items() if s.children or s.open_block]

    def leaves(self):
        return [n for n, s in self.states.items() if not s.children]

    def max_depth(self):
        return max([s.depth for s in self.states.values()] + [0])

    def ancestors(self, name):
        out = []
        cur = self.states.get(name)
        while cur is not None and cur.parent:
            out.append(cur.parent)
            cur = self.states.get(cur.parent)
        return out

    def descendants(self, name):
        out = []
        stack = list(self.states.get(name).children) if name in self.states else []
        while stack:
            n = stack.pop()
            out.append(n)
            if n in self.states:
                stack.extend(self.states[n].children)
        return out

    def triggers(self):
        """出现过的触发词（事件名近似）。PlantUML 没有事件声明段，故这是唯一来源。"""
        out = {}
        for t in self.transitions:
            if t.trigger:
                out.setdefault(t.trigger, []).append(t.line)
        return out

    def guards(self):
        out = {}
        for t in self.transitions:
            if t.guard:
                out.setdefault(t.guard, []).append(t.line)
        return out

    def effects(self):
        out = {}
        for t in self.transitions:
            if t.effect:
                out.setdefault(t.effect, []).append(t.line)
        return out

    def state_actions(self):
        """状态描述行里形如 `entry/...` `do/...` `exit/...` 的动作。"""
        out = []
        for n, s in self.states.items():
            for no, d in s.descriptions:
                if re.match(r'^(entry|do|exit|during)\s*/', d, flags=re.I):
                    out.append((n, no, d))
        return out

    def variable_candidates(self):
        """从守卫 / 效应文本里抽出的变量候选（左值优先）。

        ⚠️ 词法启发式：PlantUML 不声明变量，这里只能从 `x = v` / `x > v` 的左值猜。
        ⛔ 不作为「变量已声明」的判据，只作为提问线索。
        """
        lhs = {}
        for t in self.transitions:
            for blob, slot in ((t.guard, "guard"), (t.effect, "effect"), (t.trigger, "trigger")):
                if not blob:
                    continue
                for m in _RE_COMPARISON.finditer(blob):
                    v = m.group('lhs')
                    lhs.setdefault(v, []).append((t.line, slot, m.group(0)))
        return lhs

    # ---------- 结构性检查（供 §4 清单点名用） ----------

    def _entry_targets(self, name):
        """进入状态 name 时会实际占据的叶态集合（近似：跟随区域初始边）。"""
        st = self.states.get(name)
        if st is None or not st.children:
            return {name}
        out = set()
        inits = [t for t in self.initial_edges(scope=name)]
        if not inits:
            return {name}           # 复合态无默认进入点 —— 由 no_initial 检查单独报
        for t in inits:
            if t.dst == PSEUDO:
                continue
            out |= self._entry_targets(t.dst)
        return out or {name}

    def reachable(self):
        """从根初始边出发的可达配置（叶态集合），近似 UML run-to-completion。

        近似点（⛔ 都必须在报告里说明，不得当成判定）：
        1. 复合态的出边被视为其全部后代共享（UML 的外层迁移下推）。
        2. 守卫一律视为可满足（不做约束求解）。
        3. 不区分并发区 —— project_1 建模对象无正交区。
        """
        roots = [t.dst for t in self.initial_edges(scope=None) if t.dst != PSEUDO]
        if not roots:
            # 无顶层初始边：退化为「所有顶层态都可能是起点」，并单独报缺陷
            roots = [n for n, s in self.states.items() if s.parent is None]
        seen = set()
        frontier = set()
        for r in roots:
            frontier |= self._entry_targets(r)
        while frontier:
            cur = frontier.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for t in self.outgoing_including_inherited(cur):
                if t.dst == PSEUDO:
                    continue
                frontier |= self._entry_targets(t.dst)
        return seen

    def outgoing_including_inherited(self, name):
        """以 name 为源的边 + 其祖先复合态的出边（UML 下推）。"""
        chain = [name] + self.ancestors(name)
        return [t for t in self.transitions if t.src in chain]

    def unreachable_states(self):
        reach = self.reachable()
        expanded = set(reach)
        for n in list(reach):
            expanded |= set(self.ancestors(n))
        return sorted(n for n in self.states if n not in expanded)

    def absorbing_states(self):
        """吸收态：自身与全部祖先都无出边，且不是终态伪状态。"""
        out = []
        for n, s in self.states.items():
            if s.children:
                continue
            outs = self.outgoing_including_inherited(n)
            if not outs:
                out.append(n)
        return sorted(out)

    def implicit_states(self):
        return sorted(n for n, s in self.states.items() if s.implicit)

    def composites_without_initial(self):
        out = []
        for n, s in self.states.items():
            if not s.children:
                continue
            if not self.initial_edges(scope=n):
                out.append(n)
        return sorted(out)

    def initial_edges_with_trigger(self):
        return [t for t in self.transitions
                if t.src == PSEUDO and (t.trigger or t.guard)]

    def nondet_groups(self):
        """同源同触发的多条出边（含「全部无触发」的完成迁移组）。"""
        buckets = {}
        for t in self.transitions:
            if t.src == PSEUDO:
                continue
            buckets.setdefault((t.src, t.trigger.strip().lower()), []).append(t)
        return {k: v for k, v in buckets.items() if len(v) > 1}

    def guardless_in_group(self):
        out = []
        for (src, trig), ts in self.nondet_groups().items():
            missing = [t for t in ts if not t.guard]
            if missing:
                out.append((src, trig, ts, missing))
        return out

    def cross_scope_targets(self):
        """迁移目标不在本作用域也不在祖先 / 后代链上 —— 越界引用候选。"""
        out = []
        for t in self.transitions:
            if t.dst == PSEUDO:
                continue
            dst = self.states.get(t.dst)
            if dst is None:
                continue
            if t.scope is None:
                continue
            allowed = {t.scope} | set(self.descendants(t.scope)) | set(self.ancestors(t.scope))
            allowed |= {n for n, s in self.states.items() if s.parent is None}
            if t.dst not in allowed:
                out.append(t)
        return out

    def forward_references(self):
        """迁移在 L_a 引用了某个名字，而该名字直到 L_b > L_a 才在某复合态内被声明。

        这是 PlantUML 的一个真实陷阱：先出现的引用会把该名字**钉在当时的作用域**，
        后面的 `state X { }` 未必能把它拉回预期层级。
        """
        first_use = {}
        for t in self.transitions:
            for endpoint in (t.src, t.dst):
                if endpoint == PSEUDO:
                    continue
                first_use.setdefault(endpoint, (t.line, t.scope))
        out = []
        for n, s in self.states.items():
            if s.decl_line is None:
                continue
            fu = first_use.get(n)
            # ⛔ 只在**作用域不同**时才算陷阱。同一作用域内的前向引用是 PlantUML 的
            # 常规写法，报出来只会淹没真正的层级错位。
            if fu and fu[0] < s.decl_line and fu[1] != s.parent:
                out.append((n, fu[0], fu[1], s.decl_line, s.parent))
        return out

    def empty_composites(self):
        """写成 `state X { }` 但体内零子态、零迁移的壳。

        ⚠️ 这**不一定是缺陷** —— UML 里空体仍是 simple state（X1 侧对 0000 的同一
        主张被判为 `FALSE_POSITIVE`）。列出来是因为它常常意味着作者本想填内容。
        """
        out = []
        for n, s in self.states.items():
            if not s.open_block or s.children:
                continue
            if any(t.scope == n for t in self.transitions):
                continue
            out.append(n)
        return sorted(out)

    def summary(self):
        comps = self.composites()
        return {
            "states_total": len(self.states),
            "states_composite": len(comps),
            "states_leaf": len(self.states) - len(comps),
            "states_implicit": len(self.implicit_states()),
            "transitions": len(self.transitions),
            "initial_edges_root": len(self.initial_edges(None)),
            "initial_edges_all": len([t for t in self.transitions if t.src == PSEUDO]),
            "final_edges": len([t for t in self.transitions if t.dst == PSEUDO]),
            "depth_max": self.max_depth(),
            "triggers": len(self.triggers()),
            "guards": len(self.guards()),
            "effects": len(self.effects()),
            "state_actions": len(self.state_actions()),
            "variable_candidates": len(self.variable_candidates()),
            "region_separators": len(self.region_separators),
            "unparsed_lines": len(self.unparsed_lines),
        }
