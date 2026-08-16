"""三层判定：A 层可靠不完备，C 层拦住无论证的人工命中。

## 这套测试钉的是什么

1. **A 层的可靠性**（假阳 0）。这是它的输出可以被直接采信的唯一理由。v35 实测 A ⊆ 人工，
   28 条全部落在人工判的 89 条之内。
2. **A 层的不完备性必须被承认**。31% 不是覆盖率主张，是审计下界。一个把 A 层当全部判定的
   读法会把 hit@1 报成 21%。
3. **C 层的两道闸都要真的拦得住**：人工判命中而 A 层未确认 → 必须点名 `docs/protocol/hit_criterion.md` §3
   的四种形态之一并给出论证；A 层确认而人工判未命中 → 不得并存。
   v35 那两处作用域误判（`EIS-0032-01`、`EIS-0029-05`）正是第一道闸的形状。
4. **未判位不得静默通过**。一个只判了一半的审计文件与判完的在形状上无从区分。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

MATRIX = Path(__file__).resolve().parent.parent / "discover_matrix"
if str(MATRIX) not in sys.path:
    sys.path.insert(0, str(MATRIX))

import verdict_tiers as V  # noqa: E402


# ---------------------------------------------------------------- 解析与归一化

def test_ledger_measured_is_a_string_and_must_be_normalised() -> None:
    """⭐ 台账写的是 `"False"`，不是 `False`。

    不归一化会让每一条都判不等 —— 实测踩过：一次复测把 91 条全报成「台账与实现不一致」，
    而真实答案是 0 条。
    """

    assert V._as_bool("False") is False
    assert V._as_bool("True") is True
    assert V._as_bool(False) is False
    assert V._as_bool("") is None
    assert V._as_bool("false") is None  # 大小写不同不猜
    assert V._as_bool(0) is None


def test_composite_expressions_are_not_mechanically_judgeable() -> None:
    """`all`/`any` 与位置参数返回 None —— 这些位只能进 B 层。"""

    assert V._parse_call('containment(parent="A", child="A.B")') == (
        "containment",
        (("child", "A.B"), ("parent", "A")),
    )
    assert V._parse_call('any([initial_target(composite="A", child="A.B")])') is None
    assert V._parse_call('containment("A", "A.B")') is None
    assert V._parse_call("not a call") is None


def test_binding_order_does_not_matter() -> None:
    left = V._parse_call('f(a="1", b="2")')
    right = V._parse_call('f(b="2", a="1")')
    assert left == right


# ---------------------------------------------------------------- A 层

def _record(**over):
    base = {
        "pair": "0000",
        "layer": "wellformedness",
        "statement": "s",
        "primary_expression": 'f(x="1")',
        "primary_predicate": "f",
        "in_scope": True,
        "expressible": True,
        "claims": {("f", (("x", "1"),)): False},
    }
    base.update(over)
    return base


def _evidence(*calls):
    return {"published_assertion_ids": [], "calls": list(calls)}


def _call(**over):
    base = {
        "assertion_id": "AST-1",
        "published": True,
        "predicate": "f",
        "bindings": (("x", "1"),),
        "result": False,
        "assertion_truth": False,
    }
    base.update(over)
    return base


def test_exact_match_on_a_published_assertion_confirms() -> None:
    verdict = V.tier_a(_record(), _evidence(_call()))
    assert verdict["matched"] is True
    assert verdict["assertion_id"] == "AST-1"
    assert verdict["bindings"] == {"x": "1"}


def test_an_unpublished_assertion_does_not_confirm() -> None:
    """⭐ 被排除的发现不算命中 —— 它没有进入产物。

    v35 的 `EIS-0000-02` 正是这个形状：`stays_in` 取到了正确的 False，但被归因门排除，
    所以那一位是未命中。
    """

    assert V.tier_a(_record(), _evidence(_call(published=False)))["matched"] is False


def test_the_wrong_truth_value_does_not_confirm() -> None:
    assert V.tier_a(_record(), _evidence(_call(result=True)))["matched"] is False


def test_a_different_scope_does_not_confirm() -> None:
    """⭐ 这就是 `EIS-0032-01` 的形状：同谓词、不同 composite。

    台账说三个 Region 各缺初始伪态，产出说根的初始去向错了 —— 作用域不同、缺陷不同。
    人工那次按邻近性判成了命中；A 层给 0，分歧即警报。
    """

    assert V.tier_a(_record(), _evidence(_call(bindings=(("x", "2"),))))["matched"] is False


def test_a_different_predicate_does_not_confirm() -> None:
    """`EIS-0029-05` 的形状：台账 `containment`，产出 `state_declared`。"""

    assert V.tier_a(_record(), _evidence(_call(predicate="g")))["matched"] is False


def test_a_record_with_no_machine_judgeable_claim_never_confirms() -> None:
    assert V.tier_a(_record(claims={}), _evidence(_call()))["matched"] is False


# ---------------------------------------------------------------- B 层对照

def test_the_comparison_names_which_item_differs() -> None:
    """人只判「是不是同一命题」，所以差异必须被逐项列出来，不能让人自己找。"""

    diff = V._diff(_record(), _call(predicate="g", bindings=(("x", "2"),), result=True))
    joined = " ".join(diff)
    assert "谓词 f vs g" in joined
    assert "x: '1' vs '2'" in joined
    assert "真值 期望 False vs 实测 True" in joined


# ---------------------------------------------------------------- C 层分歧闸

def _built(*entries):
    return {"base": "b", "grid": ["0000"], "records": [], "positions": list(entries)}


def _position(record_id="EIS-0000-01", cell="run1/0000-claude", matched=False):
    return {
        "record_id": record_id,
        "cell": cell,
        "layer": "wellformedness",
        "expressible_with_closed_vocabulary": True,
        "tier_a": {"matched": matched},
    }


GOOD_ARGUMENT = "台账要求该边目标为 X，产出证明该状态根本未声明，无状态则不可能有正确目标"


def test_tier_a_hits_are_recorded_as_decided_by_tier_a() -> None:
    result = V.apply_human(_built(_position(matched=True)), {})
    assert result["hits"] == 1
    assert result["hits_by_decider"] == {"tier_a": 1}
    assert result["gate_problems"] == []
    assert result["audit"][0]["decided_by"] == "tier_a"


def test_a_human_hit_needs_a_named_equivalence_form() -> None:
    """⭐ 第一道闸。无形态名的「等价性论证」就是没有论证。"""

    result = V.apply_human(
        _built(_position()),
        {"EIS-0000-01|run1/0000-claude": {"hit": True, "equivalence_form": "看起来一样", "argument": GOOD_ARGUMENT}},
    )
    assert any("不在 docs/protocol/hit_criterion.md §3 的四种形态内" in p for p in result["gate_problems"])


def test_a_human_hit_needs_a_written_argument() -> None:
    """⭐ 同一道闸的另一半。v35 那两处误判在被要求写论证时就站不住了。"""

    result = V.apply_human(
        _built(_position()),
        {"EIS-0000-01|run1/0000-claude": {"hit": True, "equivalence_form": "直接对应", "argument": "同一件事"}},
    )
    assert any("等价性论证过短" in p for p in result["gate_problems"])


def test_a_well_argued_human_hit_passes() -> None:
    result = V.apply_human(
        _built(_position()),
        {
            "EIS-0000-01|run1/0000-claude": {
                "hit": True,
                "equivalence_form": "蕴含更根本的原因",
                "argument": GOOD_ARGUMENT,
            }
        },
    )
    assert result["gate_problems"] == []
    assert result["hits_by_decider"] == {"human": 1}
    assert result["audit"][0]["human"]["equivalence_form"] == "蕴含更根本的原因"


def test_human_miss_needs_no_argument() -> None:
    result = V.apply_human(
        _built(_position()), {"EIS-0000-01|run1/0000-claude": {"hit": False}}
    )
    assert result["hits"] == 0
    assert result["gate_problems"] == []


def test_a_contradiction_with_tier_a_is_refused() -> None:
    """⭐ 第二道闸：A 层确认而人工判未命中 —— 两者之一必错，不得并存。"""

    result = V.apply_human(
        _built(_position(matched=True)), {"EIS-0000-01|run1/0000-claude": {"hit": False}}
    )
    assert any("不得并存" in p for p in result["gate_problems"])


def test_an_unjudged_position_is_a_problem_not_a_miss() -> None:
    """⭐ 未判不等于未命中。一个只判了一半的审计文件与判完的在形状上无从区分。"""

    result = V.apply_human(_built(_position()), {})
    assert any("该位未判" in p for p in result["gate_problems"])
    assert result["positions_audited"] == 0


def test_equivalence_forms_are_the_four_from_the_criterion_document() -> None:
    """闭集是这道闸的全部力量所在。逐字取自 `docs/protocol/hit_criterion.md` §3。"""

    assert V.EQUIVALENCE_FORMS == (
        "直接对应",
        "合取项之一",
        "负向命题的正向对偶",
        "蕴含更根本的原因",
    )
    criterion = MATRIX / "docs/protocol/hit_criterion.md"
    if criterion.is_file():
        text = criterion.read_text()
        for form in V.EQUIVALENCE_FORMS:
            assert form in text, form


# ---------------------------------------------------------------- 端到端

def test_v35_tier_a_is_sound_against_the_recorded_human_verdicts() -> None:
    """⭐ 这是「与 v35 结果一致」的检验：不是数字相等，是 A 层从不与人工冲突。

    实测：132 判定位、A 层确认 28、假阳 **0**、假阴 61。假阳 0 是 A 层输出可被直接采信的
    唯一理由；31% 是审计下界而不是覆盖率主张。
    """

    base = V.RUNS / "matrix-v35"
    if not base.is_dir():
        pytest.skip("v35 运行目录不在此 checkout 中")
    built = V.build(base)
    assert built["positions"], "空结果不得当成通过"
    assert len(built["positions"]) == built["tier_a_confirmed"] + built["needs_human"]
    # A 层只可能在有台账断言且真值吻合时确认，所以确认数必须远小于总位数 —— 若它接近总数，
    # 说明匹配放松了，那时「假阳 0」这个性质不再有保证。
    assert 0 < built["tier_a_confirmed"] < len(built["positions"]) // 2


def test_an_empty_generation_refuses(tmp_path) -> None:
    empty = tmp_path / "matrix-empty"
    empty.mkdir()
    with pytest.raises(SystemExit, match="没有可判定位"):
        V.main(["--base", str(empty)])


# ---------------------------------------------------------------- 视界约定

def test_a_horizon_binding_the_ledger_omitted_does_not_block_the_match() -> None:
    """台账不写 `within_cycles`，产出写了 —— 同一主张，应当匹配。

    这不是本模块新造的放宽：`test_ledger_expectations_survive_predicate_changes.py` 早就对台账
    未写明 `within_cycles` 的断言扫 1..5 并要求全部一致。实测收益（v35）：A 层 28 → 34 位，
    **假阳仍为 0**。
    """

    verdict = V.tier_a(
        _record(claims={("f", (("x", "1"),)): False}),
        _evidence(_call(bindings=(("within_cycles", 1), ("x", "1")))),
    )
    assert verdict["matched"] is True
    assert verdict["horizon_bindings_ignored"] == ["within_cycles"]


def test_an_exact_match_records_no_ignored_bindings() -> None:
    verdict = V.tier_a(_record(), _evidence(_call()))
    assert verdict["horizon_bindings_ignored"] == []


def test_a_non_horizon_extra_binding_still_blocks() -> None:
    """⭐ 负控：放宽只对视界参数生效，不是「多出的键都忽略」。"""

    assert (
        V.tier_a(
            _record(claims={("f", (("x", "1"),)): False}),
            _evidence(_call(bindings=(("target", "T"), ("x", "1")))),
        )["matched"]
        is False
    )


def test_a_ledger_binding_the_product_omitted_blocks() -> None:
    """⭐ 负控：台账写了而产出没写 —— 那是在问一个更宽的问题，不算同一主张。"""

    assert (
        V.tier_a(
            _record(claims={("f", (("x", "1"), ("y", "2"))): False}),
            _evidence(_call(bindings=(("x", "1"),))),
        )["matched"]
        is False
    )


def test_horizon_relaxation_does_not_let_a_value_mismatch_through() -> None:
    """⭐ 负控：台账写了 `within_cycles=3` 而产出写 1 —— 值不同就是不同。"""

    assert (
        V.tier_a(
            _record(claims={("f", (("within_cycles", 3), ("x", "1"))): False}),
            _evidence(_call(bindings=(("within_cycles", 1), ("x", "1")))),
        )["matched"]
        is False
    )


# ---------------------------------------------------------------- 人工判定工作表

def test_the_worksheet_groups_by_record_not_by_cell() -> None:
    """按记录分组：判「是不是同一命题」需要 statement 在眼前，而 statement 是按记录的。

    按格分组会让同一条 statement 被重复读 6 次，每次都要重建上下文 —— v35 那两处作用域误判
    正是在上下文切换中发生的。
    """

    built = {
        "base": "/x/matrix-vtest",
        "grid": ["0000"],
        "records": [],
        "positions": [
            {**_position(cell="run1/0000-claude", matched=True), "tier_a": {"matched": True, "assertion_id": "A1", "horizon_bindings_ignored": []}},
            {
                **_position(cell="run1/0000-gpt"),
                "comparison": {
                    "ledger_primary": 'f(x="1")',
                    "candidates": [
                        {"assertion_id": "A2", "predicate": "g", "result": False, "differs_in": ["谓词 f vs g"]}
                    ],
                },
            },
        ],
        "tier_a_confirmed": 1,
        "needs_human": 1,
    }
    ledger = {"EIS-0000-01": {"layer": "wellformedness", "statement": "台账原文在此", "primary_expression": 'f(x="1")'}}
    text = V.worksheet(built, ledger)
    assert text.count("## `EIS-0000-01`") == 1, "同一记录只应出现一次"
    assert "台账原文在此" in text
    assert "[A] run1/0000-claude" in text
    assert "[?] run1/0000-gpt" in text
    # A 层已确认的位不列候选 —— 人的注意力应全部落在 [?] 上
    assert "谓词 f vs g" in text
    for form in V.EQUIVALENCE_FORMS:
        assert form in text


def test_a_fully_confirmed_record_says_so_and_lists_nothing() -> None:
    built = {
        "base": "/x/m",
        "grid": [],
        "records": [],
        "positions": [
            {**_position(cell=f"run{i}/0000-claude"), "tier_a": {"matched": True, "assertion_id": "A", "horizon_bindings_ignored": []}}
            for i in (1, 2)
        ],
        "tier_a_confirmed": 2,
        "needs_human": 0,
    }
    text = V.worksheet(built, {"EIS-0000-01": {"layer": "l", "statement": "s", "primary_expression": "e"}})
    assert "六格全部由 A 层确认" in text


def test_a_cell_with_no_published_assertion_is_stated() -> None:
    """⭐ 零 issue 的格必须显式说「无已发布断言」，不能只是空着。

    空着与「我忘了列」在工作表上无从区分，而零 issue 恰是最需要被看见的情形 ——
    v36 run1/0000-claude 就是这样丢掉整句 NL 的义务的。
    """

    built = {
        "base": "/x/m",
        "grid": [],
        "records": [],
        "positions": [{**_position(), "comparison": {"ledger_primary": "e", "candidates": []}}],
        "tier_a_confirmed": 0,
        "needs_human": 1,
    }
    text = V.worksheet(built, {"EIS-0000-01": {"layer": "l", "statement": "s", "primary_expression": "e"}})
    assert "该格无已发布断言" in text
