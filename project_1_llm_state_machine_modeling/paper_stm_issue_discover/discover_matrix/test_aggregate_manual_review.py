"""The `assertable` gate, pinned on the shapes it was written for.

Every case below was first found by hand *after* the review had been published and its
numbers quoted in an issue -- which is the whole argument for gating: each one is
mechanically detectable, and none of them was detected.

The false-positive test matters as much as the true-positive ones.  The first version of
this gate read call names out of the raw text and so flagged `active(...)` and `in(...)`
inside the fbmcq condition *strings* that `invariant` and `persists_until` take, adding
12 bogus complaints on the real corpus.  A gate that cries wolf teaches the next reader
to skip it.
"""

from __future__ import annotations

import pytest

from aggregate_manual_review import _predicate_complaints


def review(*diffs: dict, case: str = "0000") -> dict:
    return {"case": case, "diffs": list(diffs)}


def diff(**kw) -> dict:
    base = {"verdict": "problem", "reason": "r", "assertable": "", "predicate_exists": None}
    return base | kw


def only(complaints: list[str]) -> str:
    assert len(complaints) == 1, complaints
    return complaints[0]


class TestFlagsWhatItShould:
    def test_legacy_primitive_named_as_if_it_were_a_predicate(self):
        """`transition_exists` is a facade primitive, not one of the 19; 9 diffs named it."""
        c = _predicate_complaints([review(diff(
            assertable="transition_exists(source='A', target='B')", predicate_exists=True))])
        assert "transition_exists" in only(c)
        assert "19 个封闭谓词" in c[0]

    @pytest.mark.parametrize("name", ["transitions", "states", "initial_child", "effect_deltas"])
    def test_other_primitives_too(self, name: str):
        c = _predicate_complaints([review(diff(assertable=f"{name}(path='X')"))])
        assert name in only(c)

    def test_any_over_a_bool_returning_predicate_cannot_run(self):
        """`edge_declared` returns bool; `any(bool)` raises TypeError, so the assertion
        was never executable at all.  3 diffs carried it, all marked as expressible."""
        c = _predicate_complaints([review(diff(
            assertable="not any(edge_declared(source='[*]', trigger='t', target='X'))",
            predicate_exists=True))])
        assert "TypeError" in only(c)

    def test_problem_without_an_assertable_at_all(self):
        c = _predicate_complaints([review(diff(assertable=""))])
        assert "缺 assertable" in only(c)

    def test_extra_claiming_a_predicate_exists_but_naming_none(self):
        """Reads in the rollup as a vocabulary gap that is not one."""
        c = _predicate_complaints([review(diff(
            verdict="extra", assertable="", predicate_exists=True))])
        assert "会被汇总读成词表缺口" in only(c)


class TestStaysQuietWhenItShould:
    @pytest.mark.parametrize("expr", [
        "initial_target(composite='A', child='A.B')",
        "not reaches(source='A', target='B', within_cycles=5)",
        "cardinality(scope='A', count=3)",
        "all([edge_declared(source='[*]', trigger='t', target='X') is False])",
        "terminates(scope='[*]')",
    ])
    def test_closed_predicates_and_safe_builtins(self, expr: str):
        assert _predicate_complaints([review(diff(assertable=expr, predicate_exists=True))]) == []

    @pytest.mark.parametrize("expr", [
        "invariant(condition='active(Root.Mode) && x > 0')",
        'persists_until(occurrence="active(A)", release="in(B)")',
        "invariant(condition='!active(HD)')",
    ])
    def test_fbmcq_calls_inside_condition_strings_are_not_predicate_names(self, expr: str):
        """`active` / `in` belong to the condition language, not the predicate table."""
        assert _predicate_complaints([review(diff(assertable=expr, predicate_exists=True))]) == []

    @pytest.mark.parametrize("verdict", ["correct", "similar", "uncertain"])
    def test_only_counted_verdicts_are_gated(self, verdict: str):
        """A blank `assertable` on a non-problem is not a defect -- those verdicts are
        not required to be expressible."""
        assert _predicate_complaints([review(diff(verdict=verdict, assertable=""))]) == []

    def test_extra_without_a_predicate_exists_claim(self):
        assert _predicate_complaints([review(diff(verdict="extra", assertable=""))]) == []


def test_reports_case_and_diff_index_so_a_complaint_is_actionable():
    c = _predicate_complaints([review(
        diff(assertable="ok", predicate_exists=True),
        diff(assertable="transition_exists(source='A')"),
        case="0042")])
    assert only(c).startswith("0042 diff[1]:")
