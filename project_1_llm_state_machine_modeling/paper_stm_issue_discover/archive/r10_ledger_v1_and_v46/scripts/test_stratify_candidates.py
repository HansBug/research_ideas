"""Tests for the candidate stratification.

The classifier is lexical, so its failure mode is silent misattribution -- a row lands in
`nl_named` when it belongs in `reference_only` and the admissible count inflates. Two of
these tests pin bugs that actually happened:

  * a literal `"NL 第"` needle missed `NL 3`, `NL 3/4`, `NL 逐句点名`, leaving 48 of 154
    rows unclassified when nearly all of them cited the NL
  * `"NL 未点名"` contains `"点名"`, so with `nl_named` ordered first the entire
    `reference_only` stratum collapsed to one row
"""

from __future__ import annotations

import pytest

from stratify_candidates import STRATA, classify


class TestWellformedness:
    """Needs no oracle, so it is the least contestable stratum and decides first."""

    @pytest.mark.parametrize("reason", [
        "ActiveState 无出边，成为吸收态",
        "该复合状态缺默认子状态，激活后三路控制全部不可达",
        "无标签 completion 边每周期即发，挤压了同源的带触发分支",
        "初始迁移带 trigger，UML 不允许初始迁移携带触发事件",
        "整棵子树无任何入边（死代码）",
        "同一非正交区里放了三条初始迁移（非确定初始）",
        "TurnOn 与全局终态不可达，相机永远拍不完",
    ])
    def test_recognised(self, reason: str):
        assert classify(reason)[0] == "wellformedness"

    def test_wins_over_an_nl_citation_in_the_same_reason(self):
        """A reason can cite the NL *and* describe a dead end; the dead end is the stronger
        ground because it needs no oracle at all."""
        assert classify("NL 第 3 句要求返回，而该状态无出边成吸收态")[0] == "wellformedness"


class TestNlCitationForms:
    """Reviewers cite the NL in several shapes; all of them must land in `nl_named`."""

    @pytest.mark.parametrize("reason", [
        "NL 第 8 句逐字点名了 exit_urban",
        "NL 3 明确 The system first transitions to the PumpState substate",
        "NL 4/5 的 dist_to_exit<2 是局部退出动作",
        "NL 逐句点名 fork/choice/junction/join",
        "NL 2 是显式枚举式数量断言",
        "NL 要求两个动作",
    ])
    def test_recognised(self, reason: str):
        assert classify(reason)[0] == "nl_named"


class TestExclusionDecidesBeforeAdmission:
    """`NL 未点名` contains `点名`; ordering must not let `nl_named` swallow it."""

    @pytest.mark.parametrize("reason", [
        "该状态 NL 未点名，只存在于参考",
        "NL 未提及这些元素，属参考独有",
        "参考侧存疑：该守卫在 NL 中无对应句",
        "NL 从未提到这个阈值",
        "NL 未把这些元素归属于 DetLight",
    ])
    def test_reference_only_wins(self, reason: str):
        assert classify(reason)[0] == "reference_only"

    def test_reference_only_precedes_nl_named_in_strata_order(self):
        order = [name for name, _d, _p in STRATA]
        assert order.index("reference_only") < order.index("nl_named"), (
            "把 nl_named 排在前面会让 reference_only 塌缩到 1 条——这个 bug 出现过")


class TestContradiction:
    @pytest.mark.parametrize("reason", [
        "brake_pressed 的方向写反，与 NL 第 4 句相反",
        "违反 NL 第 2 句对状态体的要求",
        "与 NL 显式义务矛盾",
    ])
    def test_recognised(self, reason: str):
        assert classify(reason)[0] == "nl_contradiction"


class TestUnclassified:
    @pytest.mark.parametrize("reason", ["", "命名风格差异", "写法不同但语义一致"])
    def test_no_pattern_means_unclassified(self, reason: str):
        assert classify(reason) == ("unclassified", "")

    def test_unclassified_is_not_silently_admitted(self):
        """It must be visible as its own bucket, not folded into an admissible stratum --
        otherwise the admissible count absorbs everything the classifier failed on."""
        assert classify("完全无法归类的理由")[0] not in {
            "wellformedness", "nl_contradiction", "nl_named"}


def test_every_stratum_reports_the_phrase_that_decided_it():
    """Without the trigger phrase a reader cannot overrule the classification, and the
    whole point is that this is a proposal rather than a verdict."""
    stratum, trigger = classify("NL 第 5 句点名了 FinishState")
    assert stratum == "nl_named"
    assert trigger and trigger in "NL 第 5 句点名了 FinishState"


class TestOverSpecificationIsDecidedByVerdictNotPhrase:
    """`extra` and `problem` can carry the same phrase and mean opposite things.

    "NL 未要求 X" on a `problem` means the reference has X and the model lacks it -- not
    the model's fault. On an `extra` it means the model invented X -- squarely the model's
    fault. Keying on the phrase alone put `0049`#4 and `0056`#3, both inventions, into
    `reference_only` and struck them off as unattributable.
    """

    @pytest.mark.parametrize("reason", [
        "NL 未要求为拦截状态单独建区域，也没有『拦截解除』事件；属额外元素",
        "NL 未提到待机态或启动事件；额外增加了一个 Idle 态",
        "NL 全文没有 obstacle 清除事件；这是无 NL 依据的新增事件",
        "参考独有的写法，NL 从未提及",
    ])
    def test_extra_always_lands_in_over_specification(self, reason: str):
        assert classify(reason, "extra")[0] == "over_specification"

    @pytest.mark.parametrize("reason", [
        "该状态 NL 未点名，只存在于参考",
        "NL 未要求这个中间状态，参考却建了",
    ])
    def test_the_same_phrase_on_a_problem_stays_reference_only(self, reason: str):
        assert classify(reason, "problem")[0] == "reference_only"

    def test_extra_short_circuits_before_any_phrase_is_consulted(self):
        """Even a reason that would match wellformedness must not divert an `extra`."""
        assert classify("该状态无出边成吸收态", "extra")[0] == "over_specification"
        assert classify("该状态无出边成吸收态", "problem")[0] == "wellformedness"

    def test_over_specification_is_admissible(self):
        """It is attributable to the generated model, so it belongs in E1."""
        from stratify_candidates import STRATA
        assert "over_specification" in {name for name, _d, _p in STRATA}

    def test_trigger_records_that_the_verdict_decided(self):
        """A reader must be able to see *why* it landed there."""
        assert classify("任意理由", "extra")[1] == "verdict=extra"


class TestTriggerAccuracy:
    """The trigger is the audit trail: it tells a reader which phrase decided the stratum.
    A trigger that points at the wrong NL sentence is worse than none, because it looks
    checkable and is not."""

    @pytest.mark.parametrize(("reason", "expected"), [
        ("NL 12 逐字点名了该状态", "NL 12"),
        ("NL 1 说系统起始于此", "NL 1"),
        ("NL 06 全文没有命名事件", "NL 06"),
        ("NL06 全文没有命名事件", "NL06"),
    ])
    def test_multi_digit_nl_references_are_captured_whole(self, reason: str, expected: str):
        assert classify(reason)[1] == expected

    def test_a_two_digit_reference_is_not_truncated_to_one(self):
        """`r"NL\\s*\\d"` reported "NL 1" for every NL 10-13 citation."""
        assert classify("NL 12 逐字点名了该状态")[1] != "NL 1"


def test_json_floor_equals_printed_floor(tmp_path, capsys):
    """These disagreed once -- 35 in the JSON against 66 in the output -- because adding
    over_specification touched only the print path. A number in a JSON nobody re-derives
    is precisely the one that ends up quoted in a paper."""
    import json
    import sys
    import stratify_candidates as s

    out = tmp_path / "s.json"
    argv = sys.argv
    sys.argv = ["stratify_candidates.py", "--json", str(out)]
    try:
        s.main()
    finally:
        sys.argv = argv
    printed = capsys.readouterr().out
    payload = json.loads(out.read_text())
    floor = payload["totals"]["admissible_floor"]
    upper = payload["totals"]["admissible_upper"]
    assert f"可入 E1 的区间：{floor} – {upper}" in printed
