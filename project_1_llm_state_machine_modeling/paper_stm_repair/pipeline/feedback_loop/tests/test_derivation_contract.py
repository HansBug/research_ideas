"""机械派生义务的申报契约：形状由 schema 保证，四条判据由门保证。

## 这套测试钉的是什么

v36 前，splitter 与 requirement reviewer 对机械派生的入口义务有一处**直接冲突**：

- splitter 侧写着「This trigger is mechanical: it does not depend on recognising a phrasing」
- reviewer 侧的常设指令是「不得因 FCSTM 暴露了方便的元素就添加语义区分」，而它**看不到**
  那条触发器（实测：该文本只在 splitter prompt 里，reviewer / converter / adjudicator 全 0 命中）

实测后果：reviewer 在 `0032` 删掉 3/4 格、`0047` 删掉 5/6 格的入口义务。**reviewer 是对的** ——
它无从分辨「凭 FCSTM 方便就加」与「从一条 NL-grounded 义务蕴含出来」。

消解方式是让派生**被申报**而非被推断，于是 reviewer 面对的问题从不可判定换成可判定。
本文件钉住两件不能退化的事：

1. **错形状不可表达**：派生的入口义务绑 `child` 会被 schema 拒。此前 prompt 已明写单绑定形
   「reports a defect on a correct model」，但只能靠模型自觉 —— v35 实测析取形只出现 2 次。
2. **申报不是免检通道**：四条判据任一不满足，门仍然出 finding，且点明是哪一条。
"""

from __future__ import annotations

import pytest

from paper_stm_feedback_loop.discover.capability import (
    _LICENSED_DERIVATIONS,
    derivation_contract_findings,
)
from paper_stm_feedback_loop.discover.schemas import Requirement


def _req(rid: str, predicate: str, bindings: dict[str, str], derivation=None) -> Requirement:
    return Requirement(
        requirement_id=rid,
        statement="s",
        predicate=predicate,
        predicate_bindings=bindings,
        derivation=derivation,
    )


ENTRY = "entry_follows_cardinality"
RESIDENCY = "activation_residency"


# ---------------------------------------------------------------- schema 侧：形状

def test_derived_entry_obligation_rejects_a_child_binding() -> None:
    """绑 `child` 就是挑了一个子态 —— 对正确进入的模型为 False，是另一个主张。"""

    with pytest.raises(ValueError, match="must not bind"):
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M", "child": "Sys.M.A"},
            {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
        )


def test_derived_entry_obligation_accepts_composite_alone() -> None:
    """`child` 从必填改为**禁填** —— 不是放宽，是换一套同样严格的形状。"""

    item = _req(
        "REQ-002",
        "initial_target",
        {"composite": "Sys.M"},
        {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
    )
    assert item.predicate_bindings == {"composite": "Sys.M"}
    assert item.derivation is not None and item.derivation.kind == ENTRY


def test_undeclared_initial_target_still_requires_a_child() -> None:
    """⭐ 负控：豁免只对申报了 `entry_follows_cardinality` 的那条生效。

    没有这条，上面那个「换一套形状」就可能实际上是「把 `child` 变成全局可选」。
    """

    with pytest.raises(ValueError, match="requires bindings"):
        _req("REQ-002", "initial_target", {"composite": "Sys.M"})


def test_residency_derivation_does_not_relax_its_bindings() -> None:
    """⭐ 负控：形状豁免不外溢到另一种 kind。"""

    with pytest.raises(ValueError, match="requires bindings"):
        _req(
            "REQ-002",
            "stays_in",
            {"source": "Sys.M"},  # 缺 trigger
            {"kind": RESIDENCY, "parent_requirement_id": "REQ-001"},
        )


def test_unlicensed_kind_is_refused_by_the_literal() -> None:
    """`kind` 是闭集 —— 派生不能退化成任意口子。"""

    with pytest.raises(ValueError):
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M"},
            {"kind": "whatever_i_want", "parent_requirement_id": "REQ-001"},
        )


def test_parent_id_must_look_like_a_requirement_id() -> None:
    with pytest.raises(ValueError):
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M"},
            {"kind": ENTRY, "parent_requirement_id": "not-an-id"},
        )


# ---------------------------------------------------------------- 门侧：四条判据

def _valid_entry_pair() -> list[Requirement]:
    return [
        _req("REQ-001", "cardinality", {"scope": "Sys.M", "count": "3"}),
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M"},
            {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
        ),
    ]


def test_a_well_formed_derivation_passes_the_gate() -> None:
    assert derivation_contract_findings(_valid_entry_pair()) == ()


def test_requirements_without_derivation_are_untouched() -> None:
    """门只看申报了派生的那些 —— 普通需求仍走 reviewer 的原规则。"""

    plain = [
        _req("REQ-001", "cardinality", {"scope": "Sys.M", "count": "3"}),
        _req("REQ-002", "containment", {"parent": "Sys.M", "child": "Sys.M.A"}),
    ]
    assert derivation_contract_findings(plain) == ()


def test_condition_a_missing_parent() -> None:
    items = _valid_entry_pair()
    findings = derivation_contract_findings(items[1:])  # 去掉父
    assert len(findings) == 1
    assert "not a requirement in" in findings[0]
    assert "REQ-002" in findings[0]


def test_condition_a_parent_is_itself_derived() -> None:
    """派生之上再派生 → 整条链没有 NL 地板，正是 reviewer 原本担心的事。"""

    items = [
        _req("REQ-000", "event_consumed", {"source": "Sys.M", "trigger": "Sys.e"}),
        _req(
            "REQ-001",
            "cardinality",
            {"scope": "Sys.M", "count": "3"},
            {"kind": RESIDENCY, "parent_requirement_id": "REQ-000"},
        ),
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M"},
            {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
        ),
    ]
    findings = derivation_contract_findings(items)
    assert any("itself derived" in f and "REQ-002" in f for f in findings)


def test_condition_d_wrong_parent_predicate() -> None:
    items = [
        _req("REQ-001", "containment", {"parent": "Sys.M", "child": "Sys.M.A"}),
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.M"},
            {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
        ),
    ]
    findings = derivation_contract_findings(items)
    assert len(findings) == 1
    assert "only entailed by a `cardinality`" in findings[0]


def test_condition_d_scope_mismatch() -> None:
    """蕴含只关于父自己的 scope —— 换个 scope 就是新主张，需要自己的 NL 出处。"""

    items = [
        _req("REQ-001", "cardinality", {"scope": "Sys.M", "count": "3"}),
        _req(
            "REQ-002",
            "initial_target",
            {"composite": "Sys.Other"},
            {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
        ),
    ]
    findings = derivation_contract_findings(items)
    assert len(findings) == 1
    assert "same element" in findings[0]


def test_residency_derivation_checks_the_same_four_conditions() -> None:
    ok = [
        _req("REQ-001", "event_consumed", {"source": "Sys.M", "trigger": "Sys.e"}),
        _req(
            "REQ-002",
            "stays_in",
            {"source": "Sys.M", "trigger": "Sys.e"},
            {"kind": RESIDENCY, "parent_requirement_id": "REQ-001"},
        ),
    ]
    assert derivation_contract_findings(ok) == ()

    bad = [
        _req("REQ-001", "event_consumed", {"source": "Sys.M", "trigger": "Sys.e"}),
        _req(
            "REQ-002",
            "stays_in",
            {"source": "Sys.Elsewhere", "trigger": "Sys.e"},
            {"kind": RESIDENCY, "parent_requirement_id": "REQ-001"},
        ),
    ]
    assert len(derivation_contract_findings(bad)) == 1


def test_findings_name_the_condition_that_failed() -> None:
    """出口必须明确：reviewer 仍可删，但要说清是哪一条不满足。

    一条只说「派生无效」的 finding 会让生产者原样重交并烧掉修复预算 —— 与 `1ddc523d0`
    修的那三处契约反馈同一个病。
    """

    cases = [
        (
            [
                _req(
                    "REQ-002",
                    "initial_target",
                    {"composite": "Sys.M"},
                    {"kind": ENTRY, "parent_requirement_id": "REQ-404"},
                )
            ],
            "REQ-404",
        ),
        (
            [
                _req("REQ-001", "cardinality", {"scope": "Sys.A", "count": "2"}),
                _req(
                    "REQ-002",
                    "initial_target",
                    {"composite": "Sys.B"},
                    {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
                ),
            ],
            "Sys.B",
        ),
    ]
    for items, needle in cases:
        findings = derivation_contract_findings(items)
        assert findings and needle in findings[0], (needle, findings)


def test_licensed_table_is_closed_and_small() -> None:
    """闭集本身是这条规则的一部分：加项要过 review，否则「机械派生」就成了任意口子。"""

    assert set(_LICENSED_DERIVATIONS) == {ENTRY, RESIDENCY}
    for kind, (parent_predicate, parent_key, child_key) in _LICENSED_DERIVATIONS.items():
        assert parent_predicate and parent_key and child_key, kind


# ---------------------------------------------------------------- 析取占位符

from types import SimpleNamespace  # noqa: E402

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    entry_disjunction_findings,
)

_DECLARED = (
    'any([initial_target(composite="Sys.M", child="Sys.M.A"), '
    'initial_target(composite="Sys.M", child="Sys.M.B")]) is True'
)
_WITH_PLACEHOLDER = (
    'any([initial_target(composite="Sys.M", child="Sys.M.A"), '
    'initial_target(composite="Sys.M", child="Sys.M.UnspecifiedInitial")]) is True'
)


def _assertion(expression: str, requirement_id: str = "REQ-002"):
    return SimpleNamespace(
        assertion_id="AST-1", requirement_id=requirement_id, expression=expression
    )


def _derived_entry(requirement_id: str = "REQ-002"):
    return _req(
        requirement_id,
        "initial_target",
        {"composite": "Sys.M"},
        {"kind": ENTRY, "parent_requirement_id": "REQ-001"},
    )


def test_a_disjunction_over_declared_children_passes() -> None:
    assert entry_disjunction_findings(
        [_derived_entry()], [_assertion(_DECLARED)]
    ) == ()


def test_a_placeholder_in_the_disjunction_is_refused() -> None:
    """⭐ v36 `run1/0043-claude` 的形状，实测真值 True = 缺陷被自己的检查掩盖。

    converter prompt 已写这条并预言了后果，但只能靠自觉：17 条析取里 2 条违规。
    """

    findings = entry_disjunction_findings(
        [_derived_entry()], [_assertion(_WITH_PLACEHOLDER)]
    )
    assert len(findings) == 1
    assert "Sys.M.UnspecifiedInitial" in findings[0]
    assert "true exactly when entry has nowhere" in findings[0]


def test_all_three_inserted_name_families_are_caught() -> None:
    for name in ("UnspecifiedInitial", "InvalidInitialtr_0005", "FinalWaittr_0003"):
        expression = f'any([initial_target(composite="Sys.M", child="Sys.M.{name}")]) is True'
        assert entry_disjunction_findings(
            [_derived_entry()], [_assertion(expression)]
        ), name


def test_a_non_derived_requirement_is_not_checked() -> None:
    """⭐ 负控：这道门只管申报了 `entry_follows_cardinality` 的那些。

    一条 NL 点名了子态的合法单绑定 `initial_target` 不受此约束。
    """

    plain = _req("REQ-002", "initial_target", {"composite": "Sys.M", "child": "Sys.M.A"})
    assert entry_disjunction_findings([plain], [_assertion(_WITH_PLACEHOLDER)]) == ()


def test_a_single_binding_expression_is_not_this_gate() -> None:
    """⭐ 负控：非析取表达式不是这道门的对象（形状由 schema 管）。"""

    expression = 'initial_target(composite="Sys.M", child="Sys.M.UnspecifiedInitial") is True'
    assert entry_disjunction_findings([_derived_entry()], [_assertion(expression)]) == ()


def test_an_assertion_of_another_requirement_is_ignored() -> None:
    assert entry_disjunction_findings(
        [_derived_entry("REQ-002")], [_assertion(_WITH_PLACEHOLDER, "REQ-009")]
    ) == ()


def test_no_derived_requirements_means_no_work() -> None:
    plain = _req("REQ-001", "cardinality", {"scope": "Sys.M", "count": "2"})
    assert entry_disjunction_findings([plain], [_assertion(_WITH_PLACEHOLDER)]) == ()
