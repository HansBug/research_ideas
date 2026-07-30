"""Tests for merging the manual passes onto the lexical stratification.

This script decides the headline number, so its dangerous failure is silence: a review
batch that never landed, or a verdict it did not understand, must not quietly leave the
count at the lexical bound while the output claims a point value.
"""

from __future__ import annotations

import json
import pathlib

import pytest

import merge_manual_stratification as m


def row(case="0000", index=0, verdict="problem", stratum="nl_named", e1=False):
    return {
        "case": case, "group": "NL08", "llm": "GPT-4o", "diff_index": index,
        "verdict": verdict, "lexical_stratum": stratum, "lexical_trigger": "NL 第",
        "stratum": stratum, "decided_by": "lexical", "assertable": "reaches(...)",
        "case_has_ledger_e1": e1, "reason_head": "…",
    }


def write(tmp_path, name, payload):
    (tmp_path / name).write_text(json.dumps(payload, ensure_ascii=False))


@pytest.fixture
def nlcheck(tmp_path, monkeypatch):
    monkeypatch.setattr(m, "NLCHECK", tmp_path)
    return tmp_path


class TestReviewPrecedence:
    def test_confirmed_leaves_the_row_where_it_was(self, nlcheck):
        rows = [row()]
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "confirmed",
             "nl_evidence": "NL 第 5 句逐字"}]})
        m.apply_nl_review(rows, [])
        assert rows[0]["stratum"] == "nl_named"
        assert rows[0]["decided_by"] == "nl_review"
        assert rows[0]["nl_evidence"]

    def test_reference_only_moves_the_row_out_of_admissible(self, nlcheck):
        rows = [row()]
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "reference_only"}]})
        m.apply_nl_review(rows, [])
        assert rows[0]["stratum"] == "reference_only"
        assert rows[0]["stratum"] not in m.ADMISSIBLE

    @pytest.mark.parametrize("verdict", ["wellformedness", "nl_contradiction"])
    def test_reclassification_within_admissible_keeps_it_admissible(self, nlcheck, verdict):
        rows = [row()]
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": verdict}]})
        m.apply_nl_review(rows, [])
        assert rows[0]["stratum"] == verdict
        assert verdict in m.ADMISSIBLE

    def test_manual_overrules_lexical_never_the_other_way(self, nlcheck):
        """The lexical pass exists to make the manual pass finite, not to overrule it."""
        rows = [row(stratum="wellformedness")]
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "reference_only"}]})
        m.apply_nl_review(rows, [])
        assert rows[0]["stratum"] == "reference_only"


class TestItComplainsRatherThanAbsorbs:
    def test_a_missing_batch_is_reported_and_leaves_rows_at_the_bound(self, nlcheck):
        rows = [row()]
        complaints: list[str] = []
        m.apply_nl_review(rows, complaints)
        assert len(complaints) == 4, "四批全缺就该有四条抱怨"
        assert rows[0]["decided_by"] == "lexical"

    def test_an_unknown_review_verdict_is_reported_not_applied(self, nlcheck):
        rows = [row()]
        complaints: list[str] = []
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "looks_fine_to_me"}]})
        m.apply_nl_review(rows, complaints)
        assert any("未知复核判定" in c for c in complaints)
        assert rows[0]["decided_by"] == "lexical"

    def test_a_row_not_in_the_baseline_is_reported(self, nlcheck):
        complaints: list[str] = []
        write(nlcheck, "result1.json", {"items": [
            {"case": "9999", "diff_index": 7, "verdict": "confirmed"}]})
        m.apply_nl_review([row()], complaints)
        assert any("不在基线里" in c for c in complaints)

    def test_missing_harm_file_is_reported_as_an_upper_bound(self, nlcheck):
        complaints: list[str] = []
        m.apply_harm([row(verdict="extra", stratum="over_specification")], complaints)
        assert any("这是上界" in c for c in complaints)


class TestHarmTestOwnsTheExtraRows:
    def test_an_nl_review_touching_an_extra_row_is_refused(self, nlcheck):
        """`extra` is decided by consequence, not by whether the NL names it."""
        rows = [row(verdict="extra", stratum="over_specification")]
        complaints: list[str] = []
        write(nlcheck, "result1.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "reference_only"}]})
        m.apply_nl_review(rows, complaints)
        assert rows[0]["stratum"] == "over_specification", "NL 复核不得改动 extra 的归属"
        assert any("由有害性判定决定" in c for c in complaints)

    def test_benign_moves_it_out_of_admissible(self, nlcheck):
        rows = [row(verdict="extra", stratum="over_specification")]
        write(nlcheck, "extra_harm.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "benign",
             "consequence": "写不出后果"}]})
        m.apply_harm(rows, [])
        assert rows[0]["stratum"] == "over_specification_benign"
        assert rows[0]["stratum"] not in m.ADMISSIBLE

    def test_harmful_keeps_it_admissible_and_records_the_assertion(self, nlcheck):
        rows = [row(verdict="extra", stratum="over_specification")]
        write(nlcheck, "extra_harm.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "harmful",
             "consequence": "死代码", "assertion": "reaches(...) = False",
             "verified": "实跑返回 False"}]})
        m.apply_harm(rows, [])
        assert rows[0]["stratum"] == "over_specification"
        assert rows[0]["harm_assertion"] and rows[0]["harm_verified"]

    def test_uncertain_is_parked_not_admitted(self, nlcheck):
        rows = [row(verdict="extra", stratum="over_specification")]
        m_complaints: list[str] = []
        write(nlcheck, "extra_harm.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "uncertain"}]})
        m.apply_harm(rows, m_complaints)
        assert rows[0]["stratum"] == "uncertain_stratum"
        assert rows[0]["stratum"] not in m.ADMISSIBLE

    def test_harm_test_on_a_problem_row_is_refused(self, nlcheck):
        rows = [row(verdict="problem")]
        complaints: list[str] = []
        write(nlcheck, "extra_harm.json", {"items": [
            {"case": "0000", "diff_index": 0, "verdict": "benign"}]})
        m.apply_harm(rows, complaints)
        assert rows[0]["stratum"] == "nl_named"
        assert any("不是 extra 档" in c for c in complaints)


class TestPointValueClaim:
    def test_not_a_point_value_while_any_row_sits_at_the_lexical_verdict(self):
        s = m.summarise([row(), row(case="0001")])
        assert s["is_point_value"] is False
        assert s["still_at_lexical_bound"] == 2

    def test_a_reviewed_but_parked_row_does_not_block_the_point_value(self):
        """`uncertain_stratum` means someone looked and the current predicate surface gives
        no positive judgement -- a *known* exclusion, reported separately and left out of
        the admissible count. What blocks the claim is a stratum nobody examined, which is
        an unknown."""
        r = row() | {"decided_by": "nl_review", "stratum": "uncertain_stratum"}
        s = m.summarise([r])
        assert s["is_point_value"] is True
        assert s["uncertain"] == 1
        assert s["admissible"] == 0, "搁置的不得计入可入"

    def test_an_unexamined_stratum_still_blocks_it(self):
        s = m.summarise([row(), row(case="0001")])
        assert s["is_point_value"] is False
        assert s["unreviewed"] == 2

    def test_a_point_value_needs_every_row_decided(self):
        rows = [row() | {"decided_by": "nl_review"},
                row(case="0001", verdict="extra", stratum="over_specification")
                | {"decided_by": "harm_test"}]
        s = m.summarise(rows)
        assert s["is_point_value"] is True
        assert s["admissible"] == 2

    def test_admissible_excludes_every_non_admissible_stratum(self):
        rows = [
            row() | {"decided_by": "nl_review"},
            row(case="0001", stratum="reference_only") | {"decided_by": "nl_review"},
            row(case="0002", verdict="extra", stratum="over_specification_benign")
            | {"decided_by": "harm_test"},
        ]
        s = m.summarise(rows)
        assert s["admissible"] == 1
        assert s["is_point_value"] is True

    def test_counts_admissible_rows_on_cases_the_ledger_missed(self):
        rows = [row(e1=True) | {"decided_by": "nl_review"},
                row(case="0001", e1=False) | {"decided_by": "nl_review"}]
        assert m.summarise(rows)["admissible_on_cases_without_ledger_e1"] == 1


class TestDuplicateHarmfulExtrasAreNotDoubleBooked:
    """A harmful `extra` whose consequence a sibling `problem` already carries would be
    reported as two expected issues for one defect. `0056`#3 binds identically to
    `0056`#1 -- same predicate, same arguments."""

    def test_a_flagged_duplicate_leaves_the_admissible_set(self, nlcheck):
        rows = [row(case="0056", index=3, verdict="extra", stratum="over_specification")]
        write(nlcheck, "extra_harm.json", {
            "items": [{"case": "0056", "diff_index": 3, "verdict": "harmful",
                       "assertion": "guard_distinguishable(...) = False"}],
            "harmful_but_duplicate_of_an_existing_problem": [
                "0056#3 (dup of 0056#1 guard_distinguishable, identical binding)"],
        })
        m.apply_harm(rows, [])
        assert rows[0]["stratum"] == "over_specification_duplicate"
        assert rows[0]["stratum"] not in m.ADMISSIBLE
        assert rows[0]["duplicate_of"].startswith("0056#3")

    def test_dedup_runs_after_the_harm_verdict_so_it_wins(self, nlcheck):
        """The row is harmful *and* a duplicate; the duplicate flag must be what sticks."""
        rows = [row(case="0046", index=5, verdict="extra", stratum="over_specification")]
        write(nlcheck, "extra_harm.json", {
            "items": [{"case": "0046", "diff_index": 5, "verdict": "harmful"}],
            "harmful_but_duplicate_of_an_existing_problem": ["0046#5 (dup of 0046#2)"],
        })
        m.apply_harm(rows, [])
        assert rows[0]["stratum"] == "over_specification_duplicate"

    def test_an_unparseable_duplicate_marker_is_reported(self, nlcheck):
        complaints: list[str] = []
        write(nlcheck, "extra_harm.json", {
            "items": [], "harmful_but_duplicate_of_an_existing_problem": ["看不懂的标记"]})
        m.apply_harm([row()], complaints)
        assert any("无法解析的重复标记" in c for c in complaints)

    def test_a_duplicate_marker_for_an_unknown_row_is_reported(self, nlcheck):
        complaints: list[str] = []
        write(nlcheck, "extra_harm.json", {
            "items": [], "harmful_but_duplicate_of_an_existing_problem": ["9999#9 (dup)"]})
        m.apply_harm([row()], complaints)
        assert any("不在基线里" in c for c in complaints)
