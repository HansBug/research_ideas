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


def test_the_one_element_rule_is_not_a_validator() -> None:
    """这条纪律**不许**做成 schema 约束（CLAUDE.md §11）。

    它曾经是一条 `model_validator`：`name_in_sentence` 含逗号/and/or 即拒。后果是把语义判断
    实现成了词法判断，在 `0014` 上打死一个**完全正确**的回答——规范逐字引用的信号名
    `"Arrived/Stop, Send Arrived"` 天然含逗号，其 `declared_match` 非 null 且正确。
    v41 全量 2928 行里 190 行被误拒（`0020`/`0039` 的若干臂 100%），该 pair 18/18 撞死、
    5 格耗尽、约 16 万 output token 白烧，而模型没有任何合法写法能通过——拆开写反而是错的。

    确定性门一票否决且没有出路，所以只放能完美判定的约束。这条测试锁住它不被重新加回来。
    """

    from paper_stm_feedback_loop.discover.schemas import NamedElement

    # 规范把带标点的整体引成一个信号名——这是正确回答，必须被接受
    ok = NamedElement(
        kind="event",
        name_in_sentence="Arrived/Stop, Send Arrived",
        proposed_path="Sys.Arrived_Stop_SendArrived",
        declared_match="Sys.Arrived_Stop_SendArrived",
    )
    assert ok.declared_match is not None

    # 守卫表达式里的 and 是布尔算子，不是并列连接词
    NamedElement(
        kind="event",
        name_in_sentence="dist_to_front<25 and extra_lane=true",
        proposed_path="Sys.dist_to_front_25_extra_lane_true",
    )

    # 真正的融合形态也不再被 schema 拒——它交给评审端判断
    NamedElement(
        kind="event",
        name_in_sentence="human steering cmd, brake pressed",
        proposed_path="Sys.x",
    )


def test_the_discipline_lives_in_description_and_both_prompts() -> None:
    """撤掉门之后，纪律必须在三处都在：字段说明、生成端、评审端。

    当初加门的起点是「reviewer prompt 里根本没有 `named_elements` 的审查条款」——
    缺的是评审条款，却用 validator 去顶，这才是根本错误。
    """

    from paper_stm_feedback_loop.discover import prompts
    from paper_stm_feedback_loop.discover.schemas import NamedElement

    desc = NamedElement.model_fields["name_in_sentence"].description or ""
    assert "一行只放一个要素" in desc
    assert "逐字优先" in desc, "必须写明规范引号框住的整体算一个要素，否则又会误拆"

    match_desc = NamedElement.model_fields["declared_match"].description or ""
    assert "融合本身是缺陷" in match_desc

    splitter = " ".join(prompts.REQUIREMENT_SPLITTER_PROMPT.split())
    assert "One element per row" in splitter

    reviewer = " ".join(prompts.REQUIREMENT_REVIEWER_PROMPT.split())
    assert "Check `named_elements` row by row" in reviewer
    assert "punctuation does not decide this" in reviewer
    assert "A fused declared name matches none of the elements it fuses" in reviewer
    assert "Request revision" in reviewer


def test_the_prompt_states_the_generator_side_rule() -> None:
    """约束与 prompt 必须同源——只有约束没解释，生产者只会反复撞门耗光预算。"""

    from paper_stm_feedback_loop.discover import prompts

    # 对空白不敏感：prompt 是硬换行的散文，断言原样子串会被行宽截断。
    splitter = " ".join(prompts.REQUIREMENT_SPLITTER_PROMPT.split())
    assert "One element per row" in splitter
    assert "fused model name matches none of them" in splitter
    assert "both rows stay `null`" in splitter
    assert "the collapsing is itself the defect" in splitter


# --------------------------------------------------------------------------
# v45：报错必须给出**两条**出路，否则「填错表」这一支无解


class _V45Elem:
    def __init__(self, name, kind, path, match=None):
        self.name_in_sentence = name
        self.kind = kind
        self.proposed_path = path
        self.declared_match = match


class _V45Set:
    def __init__(self, elements):
        self.named_elements = tuple(elements)
        self.requirements = ()


_KNOWN = frozenset({"m.HumanDriving", "m.Autonomous", "m.Power_On"})


def test_the_finding_offers_the_tabulation_fix_as_well() -> None:
    """只给「补存在性需求」一条出路时，pair 0030 在这里空转了十轮。

    生产者把 `'human driving mode'` 的 `declared_match` 填成 null，而模型声明了
    `HumanDriving`。旧报错要求它断言这个状态缺失；它正确地拒绝了，因为那不是真的。
    两边都没错，但没有一方能动——真正的缺陷是**表填错了**，而报错没提这条路。
    """

    from paper_stm_feedback_loop.discover.capability import (
        unmatched_named_element_findings,
    )

    finding = unmatched_named_element_findings(
        _V45Set([_V45Elem("human driving mode", "state", "m.human_driving_mode")]), _KNOWN
    )[0]
    assert "Two exits" in finding
    assert "set `declared_match`" in finding
    # 候选必须指名道姓，否则生产者仍要自己猜是哪一个。
    assert "'m.HumanDriving'" in finding


def test_the_candidate_hint_is_a_hint_and_not_a_gate() -> None:
    """没有近似候选时不得凭空造提示；有候选时也只是提示，判定条件不变。

    「这个短语指的是不是那个已声明元素」是语义判断，按 §11 不许进门；
    所以候选只出现在文案里，`declared_match` 非空才是唯一的免除条件。
    """

    from paper_stm_feedback_loop.discover.capability import (
        unmatched_named_element_findings,
    )

    absent = unmatched_named_element_findings(
        _V45Set([_V45Elem("emergency brake", "state", "m.emergency_brake")]), _KNOWN
    )[0]
    assert "declared vocabulary contains" not in absent

    # 填了 declared_match 就没有 finding —— 判定条件仍然只看这一个字段。
    assert (
        unmatched_named_element_findings(
            _V45Set(
                [
                    _V45Elem(
                        "human driving mode",
                        "state",
                        "m.human_driving_mode",
                        "m.HumanDriving",
                    )
                ]
            ),
            _KNOWN,
        )
        == ()
    )


def test_known_paths_is_optional_so_existing_callers_keep_working() -> None:
    finding = unmatched_named_element_findings_default()
    assert "Two exits" in finding


def unmatched_named_element_findings_default() -> str:
    from paper_stm_feedback_loop.discover.capability import (
        unmatched_named_element_findings,
    )

    return unmatched_named_element_findings(
        _V45Set([_V45Elem("human driving mode", "state", "m.human_driving_mode")])
    )[0]
