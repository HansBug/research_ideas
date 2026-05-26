"""7 类组件的 IR dataclass — Umple / pyfcstm 两个 extractor 共用。

每个 component 一个 `kind` 字符串 + 一个 list of dict instances。每个 instance
至少含 ``id`` / ``text``（原文片段）/ 关键名字字段（如 state.name / transition.src
等），便于 annotator 引用与 user review 时定位证据。
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional


COMPONENT_KINDS = (
    "states",
    "transitions",
    "guards",
    "actions",
    "hierarchical_states",
)


@dataclass
class ComponentSet:
    """单个模型的 5 类组件抽取结果。

    每个 attribute 是 list[dict]，dict 字段约定见下：

    - ``states``: ``{id, name, parent, text}``
    - ``transitions``: ``{id, src, tgt, event, guard, action, is_forced, text}``
    - ``guards``: ``{id, transition_id, expr, text}``
    - ``actions``: ``{id, transition_id, code, text}``
    - ``hierarchical_states``: ``{id, name, children: list[str], text}``
    """

    states: list[dict[str, Any]] = field(default_factory=list)
    transitions: list[dict[str, Any]] = field(default_factory=list)
    guards: list[dict[str, Any]] = field(default_factory=list)
    actions: list[dict[str, Any]] = field(default_factory=list)
    hierarchical_states: list[dict[str, Any]] = field(default_factory=list)

    source: str = ""  # "umple" / "pyfcstm" / "mock"
    raw_text: str = ""  # 原始模型文本，供 annotator 看全貌

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "states": self.states,
            "transitions": self.transitions,
            "guards": self.guards,
            "actions": self.actions,
            "hierarchical_states": self.hierarchical_states,
        }

    def counts(self) -> dict[str, int]:
        return {k: len(getattr(self, k)) for k in COMPONENT_KINDS}

    def get(self, kind: str) -> list[dict[str, Any]]:
        if kind not in COMPONENT_KINDS:
            raise ValueError(f"unknown component kind: {kind!r}; expected one of {COMPONENT_KINDS}")
        return getattr(self, kind)
