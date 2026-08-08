"""`named_elements` 把差集扫描从散文变成槽位，且 null 侧必须承重。

v40 实测：同一条规则写成散文后，`event_declared` 的形成格数从 4/36 涨到 23/35，
**但调用真值仍是 110 True / 17 False** —— 模型开始写它了，绑的却仍是制品已声明的名字，
那种检查按构造只能为真。`event_consumed` 更彻底：跨两代 102 次调用 False 恒为 0。

本仓库对这个现象有可复算的度量：typed 槽位 96–100%（`strategies` 11826/11842、
`nl_parent` 1489/1489），free-text 当协议 25–38%（`incumbent considered:` 305/803）。

所以枚举方向被做成结构：填 `named_elements` 就是在做「句子点名了什么 → 模型有没有」。
下面锁的是**这张表的 null 侧必须承重**，不是它的措辞。
"""

from __future__ import annotations

import pytest

from paper_stm_feedback_loop.discover.capability import unmatched_named_element_findings
from paper_stm_feedback_loop.discover.schemas import NamedElement


class _Requirement:
    def __init__(self, predicate: str, bindings: dict[str, str]) -> None:
        self.predicate = predicate
        self.predicate_bindings = bindings


class _Set:
    def __init__(self, named, requirements=()) -> None:
        self.named_elements = tuple(named)
        self.requirements = tuple(requirements)


@pytest.mark.parametrize(
    ("kind", "path", "predicate", "binding"),
    [
        ("event", "Sys.Arm", "event_declared", "event"),
        ("state", "Sys.Degraded", "state_declared", "state"),
        ("variable", "retry_limit", "variable_declared", "variable"),
    ],
)
def test_an_unmatched_name_owes_an_existence_requirement(kind, path, predicate, binding) -> None:
    element = NamedElement(kind=kind, name_in_sentence="x", proposed_path=path)
    assert len(unmatched_named_element_findings(_Set([element]))) == 1
    discharged = _Set([element], [_Requirement(predicate, {binding: path})])
    assert unmatched_named_element_findings(discharged) == ()


def test_a_matched_name_owes_nothing() -> None:
    """`declared_match` 非空表示模型确实声明了它——那不是发现，不该被要求写义务。"""

    element = NamedElement(
        kind="event",
        name_in_sentence="arm",
        proposed_path="Sys.Arm",
        declared_match="Sys.Arm",
    )
    assert unmatched_named_element_findings(_Set([element])) == ()


def test_the_wrong_predicate_does_not_discharge_it() -> None:
    """用 `occupancy_after` 绑同一个名字，不构成「断言了它存在」。"""

    element = NamedElement(kind="event", name_in_sentence="arm", proposed_path="Sys.Arm")
    wrong = _Set([element], [_Requirement("occupancy_after", {"trigger": "Sys.Arm"})])
    assert len(unmatched_named_element_findings(wrong)) == 1


def test_an_empty_table_is_not_an_error() -> None:
    """薄 NL 可能一个元素都不点名；空表不得被当成违规。"""

    assert unmatched_named_element_findings(_Set([])) == ()


def test_the_field_reaches_the_provider_as_a_typed_slot() -> None:
    """必须进 tool schema —— 这正是它区别于散文的地方。"""

    from paper_stm_feedback_loop.discover.schemas import RequirementSet

    schema = RequirementSet.model_json_schema()
    assert "named_elements" in schema["properties"]
    kind = schema["$defs"]["NamedElement"]["properties"]["kind"]
    assert kind["enum"] == ["state", "event", "variable"]
