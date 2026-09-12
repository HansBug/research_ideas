"""The two directions the precondition design must hold in (issue #170 §11.9).

Recall and precision are traded against each other here, so both need pinning
with real corpus data rather than toy models.

* **Recall.** Pair 0006's expected defect -- the NL requires the swarm count to
  drop after an attack and the model declares no variable that could -- must still
  be reported.  Requiring a proposed name and an NL citation makes the converter
  more careful, and a converter that becomes too careful stops reporting real
  gaps.

* **Precision.** Pair 0000's NL mentions no quantity anywhere.  A fabricated
  "some quantity must decrease" obligation must not produce a confirmed issue.
  Under the previous design it did: the predicate read the declaration table,
  found it empty -- as it is for all 60 pairs -- and sealed a false.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402
from paper_stm_feedback_loop.assertions.checker import AssertionChecker  # noqa: E402

REPORT = (
    ROOT.parent
    / "representation/reports/llms_emp_r45_java_60"
)


def _real_checker(pair: str) -> AssertionChecker:
    """A checker over the frozen pair, with its real source-trace exclusions."""

    model = (REPORT / f"pairs/{pair}/fcstm.fcstm").read_text()
    trace_path = REPORT / f"source_traces/llms_emp_feedback_final_{pair}.json"
    trace = json.loads(trace_path.read_text()) if trace_path.exists() else {}
    return AssertionChecker(
        environment=build_eval_environment(
            model_text=model,
            source_mappings=trace.get("entries", []),
            source_exclusions=trace.get("attribution_exclusions", []),
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=15_000,
            fbmcq_max_bound=4,
            fbmcq_process_wall_seconds=20.0,
        )
    )


def _check(pair: str, expression: str):
    script = f'assert {expression}, "[REQ-001][AST-REQ-001-1] m"'
    return _real_checker(pair).check(
        script, reason="bidirectional", required_function_families=()
    )


P6 = "llms_emp_feedback_final_0006"
P0 = "llms_emp_feedback_final_0000"


# --------------------------------------------------------------------------
# Recall: pair 0006's expected defect must still be reported
# --------------------------------------------------------------------------


def test_the_proposed_name_existence_check_reports_the_0006_gap():
    """`EXP-0006-EA-001`, expressed the new way.

    The only variable pair 0006 declares is the converter's `R45RouteToken`, which
    `variable_declared` does not count -- the effect facade drops it from every
    answer, so reporting it as declared would promise evidence no other call can
    deliver.  So the proposed `uav_count` comes back False, and that False rests on
    a real query over the declaration table rather than on a literal.
    """

    result = _check("0006", 'variable_declared(variable="uav_count") is True')
    assert result.sealed.outcome == "sealed_false", result.sealed.metadata
    assert result.sealed.value is False


def test_the_route_control_variable_is_not_offered_as_the_authors_own():
    """Naming it would let a producer close the requirement on the wrong evidence."""

    result = _check("0006", 'variable_declared(variable="R45RouteToken") is True')
    assert result.sealed.outcome == "sealed_false"
    assert result.sealed.value is False


def test_the_dependent_claim_is_refusable_but_not_answerable_on_that_model():
    """With no such variable there is no delta to judge.

    In a run this assertion is never executed -- the precondition's False blocks it
    -- but checked directly it must not quietly answer either, or a producer that
    forgets `depends_on` would get a verdict resting on nothing.
    """

    result = _check(
        "0006",
        f'variable_delta_after(source="{P6}.UAVSwarmStateMachine.Attack", '
        f'trigger="{P6}.Attack_Complete", variable="uav_count", sign="negative") is True',
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert result.sealed.value is None


def test_the_literal_itself_is_refused_on_the_same_model():
    """What used to seal a false here now names the replacement shape."""

    result = _check(
        "0006",
        f'variable_delta_after(source="{P6}.UAVSwarmStateMachine.Attack", '
        f'trigger="{P6}.Attack_Complete", variable="<undeclared>", sign="negative") is True',
    )
    assert result.sealed.outcome == "invalid"
    message = str((result.sealed.error or {}).get("message", ""))
    assert "placeholder, not a name" in message
    assert "precondition" in message


# --------------------------------------------------------------------------
# Precision: pair 0000's NL names no quantity, so none may be reported
# --------------------------------------------------------------------------


def test_a_fabricated_quantity_obligation_no_longer_seals_on_pair_0000():
    """The channel that made every pair a candidate for a false positive.

    Pair 0000's NL is about driving modes and power-off; it mentions no count, no
    amount, nothing that decreases.  Under the previous design
    `variable="<undeclared>"` sealed a false here off `declaration_table:variables:
    empty` -- a fact true of all 60 pairs and therefore discriminating nothing.
    """

    result = _check(
        "0000",
        f'variable_delta_after(source="{P0}.HumanDrivingMode", trigger="{P0}.Power_Off", '
        f'variable="<undeclared>", sign="negative") is True',
    )
    assert result.sealed.outcome == "invalid", result.sealed.metadata
    assert result.sealed.value is None
    assert result.sealed.metadata.get("verdict_basis") is None


def test_a_proposed_name_on_pair_0000_still_answers_but_needs_an_nl_citation():
    """The shape is available on any model, so precision now rests upstream.

    `variable_declared` answers False here too -- pair 0000 declares no
    author-owned variable either.  What stops that becoming a reported defect is
    the `rationale` requirement and the reviewer that checks it: there is no clause
    in pair 0000's NL to cite.  Recorded here so the boundary is explicit rather
    than assumed.
    """

    result = _check("0000", 'variable_declared(variable="some_count") is True')
    assert result.sealed.outcome == "sealed_false"
    assert result.sealed.value is False


def test_the_reviewer_is_the_stage_that_must_reject_it():
    """So the requirement it enforces has to be in its prompt, not just implied."""

    from paper_stm_feedback_loop.discover import prompts

    reviewer = prompts.ASSERTION_REVIEWER_PROMPT
    assert "rationale" in reviewer
    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert "Put the NL citation in" in converter
    assert "which clause, which words" in converter
