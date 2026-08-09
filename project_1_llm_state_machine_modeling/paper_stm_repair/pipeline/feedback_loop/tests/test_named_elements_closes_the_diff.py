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


def test_a_row_may_not_carry_a_conjunction() -> None:
    """一行一个要素——否则制品的融合命名会反过来决定句子被切成几个要素。

    v41 实测：`0020` 两个格都把「human steering cmd, brake pressed」抄成一行，它匹配上了
    制品的融合事件，`declared_match` 非空 → 不生成义务 → 该台账条目六格全灭、跨三代零命中。
    这正是这张表要防的那件事，只是上移了一层：表原本防「让制品决定绑哪个元素」，
    这里是「让制品决定句子里有几个元素」。

    做成 validator 而非 prompt 措辞，理由与这张表本身相同：typed 约束遵守率 96–100%，
    散文 25–38%。
    """

    import pytest
    from pydantic import ValidationError

    from paper_stm_feedback_loop.discover.schemas import NamedElement

    ok = NamedElement(
        kind="event", name_in_sentence="the lid is opened", proposed_path="Sys.lid_opened"
    )
    assert ok.declared_match is None

    for wording in (
        "lid opened, tray removed",
        "lid opened and tray removed",
        "lid opened or tray removed",
        "开盖、取盘",
        "开盖 和 取盘",
    ):
        with pytest.raises(ValidationError):
            NamedElement(kind="event", name_in_sentence=wording, proposed_path="Sys.x")


def test_the_rejection_says_the_fused_name_is_not_a_match() -> None:
    """报错必须把「融合名不算任何单个要素的 declared_match」讲出来。

    只说「拆开」会让生产者拆成两行、再把两行都指向同一个融合名——`declared_match` 仍非空，
    义务仍然不生成，缺陷仍然报不出来。指令必须同时给出拆分与判空两件事。
    """

    import pytest
    from pydantic import ValidationError

    from paper_stm_feedback_loop.discover.schemas import NamedElement

    with pytest.raises(ValidationError) as caught:
        NamedElement(kind="event", name_in_sentence="a, b", proposed_path="Sys.x")
    message = str(caught.value)
    assert "declared_match" in message
    assert "null" in message


def test_the_prompt_states_the_same_rule_as_the_validator() -> None:
    """约束与 prompt 必须同源——只有约束没解释，生产者只会反复撞门耗光预算。"""

    from paper_stm_feedback_loop.discover import prompts

    # 对空白不敏感：prompt 是硬换行的散文，断言原样子串会被行宽截断。
    splitter = " ".join(prompts.REQUIREMENT_SPLITTER_PROMPT.split())
    assert "One element per row" in splitter
    assert "fused model name matches none of them" in splitter
    assert "both rows stay `null`" in splitter
    assert "the collapsing is itself the defect" in splitter
