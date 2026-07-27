"""S2/S3 regression: isolation must survive a producer that rewrites its text.

In the pair-0029 runs the no-progress signature hashed the *expression source*
together with the error string, so a converter that reworded its failing FBMCQ
query every revision presented a brand-new signature each round.  GPT-5.5 hit a
byte-identical repeat once in twelve revisions; Claude never did.  Nothing was
ever quarantined and both runs had to be killed by hand.

These tests drive exactly that behaviour -- a permanently broken assertion whose
text (and sometimes whose failure mode) changes every round -- and require that
the run still terminates, isolates only the broken item, and publishes the rest.
"""

from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import nodes  # noqa: E402
from paper_stm_feedback_loop.discover.graph import run_discover_state  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionReview,
    AssertionScript,
    DiscoverAdjudication,
    DiscoverInput,
    RequirementReview,
    RequirementSet,
)

MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : /go;
}
"""

# Each entry is broken, but in a different way, so neither the expression text
# nor the error type is stable across revisions.
CHURNING_BROKEN_EXPRESSIONS = [
    "len(states(",
    "len(states((",
    "len(states(((",
    "len(states((((",
    "len(states(((((",
    "len(states((((((",
    "len(states(((((((",
    "len(states((((((((",
]


def _requirements() -> RequirementSet:
    return RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-GOOD",
                "statement": "Done must exist in the model.",
                "verification_kind": "structure",
                "coverage_obligation": {"domain": "state:Done", "aggregation": "all"},
            },
            {
                "requirement_id": "REQ-BAD",
                "statement": "An obligation whose check never becomes executable.",
                "verification_kind": "structure",
                "coverage_obligation": {"domain": "state:Idle", "aggregation": "all"},
            },
        ),
        segment_disposition={"NL-L001": "covered"},
    )


def _script(
    revision: int, broken_expression: str, bad_family: str = "structure"
) -> AssertionScript:
    return AssertionScript(
        revision=revision,
        assertions=(
            {
                "assertion_id": "AST-GOOD",
                "requirement_id": "REQ-GOOD",
                "description": "A permanently executable check.",
                "expression": 'transition_exists(source="Root.Idle", event="Root.go", target="Root.Done")',
                "failure_message": "[REQ-GOOD][AST-GOOD] Idle does not reach Done on go.",
                "evidence_family": "relation",
                "role": "primary",
                "coverage_key": "edge:Idle-go-Done",
                "aggregation_group": "REQ-GOOD:all",
            },
            {
                "assertion_id": "AST-BAD",
                "requirement_id": "REQ-BAD",
                "description": "A check that never becomes executable.",
                "expression": broken_expression,
                "failure_message": "[REQ-BAD][AST-BAD] never executable",
                "evidence_family": bad_family,
                "role": "primary",
                "coverage_key": "state:Idle",
                "aggregation_group": "REQ-BAD:all",
            },
        ),
        requirement_mapping={"REQ-GOOD": ("AST-GOOD",), "REQ-BAD": ("AST-BAD",)},
    )


def _run_with_churn() -> dict:
    revision = 0

    def responder(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        nonlocal revision
        if schema is RequirementSet:
            return _requirements()
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept", reviewed_revision=1, rationale="Faithful."
            )
        if schema is AssertionScript:
            expression = CHURNING_BROKEN_EXPRESSIONS[
                min(revision, len(CHURNING_BROKEN_EXPRESSIONS) - 1)
            ]
            revision += 1
            return _script(revision, expression)
        if schema is AssertionReview:
            return AssertionReview(
                decision="accept",
                reviewed_script_hash="TO_BE_PATCHED",
                rationale="Remaining assertions are adequate.",
            )
        if schema is DiscoverAdjudication:
            return DiscoverAdjudication(
                has_confirmed_issues=False,
                satisfied_requirement_ids=("REQ-GOOD",),
                rationale="The released assertion passed.",
            )
        raise TypeError(f"unsupported schema {schema}")

    return run_discover_state(
        DiscoverInput(
            run_id="s2-churn",
            natural_language="Idle shall reach Done on go.",
            stm_text=MODEL,
            language="en-US",
        ),
        responder,
    )


def test_expression_churn_no_longer_evades_isolation() -> None:
    state = _run_with_churn()
    assert "failure" not in state, "a single broken item must not fail the run"

    published = state["final_output"]
    assert published.status == "completed"
    assert published.coverage_status == "partial"

    gaps = {gap.assertion_ids[0]: gap for gap in published.coverage_gaps}
    assert set(gaps) == {"AST-BAD"}
    assert gaps["AST-BAD"].reason_code in {
        "no_progress",
        "revision_budget_exhausted",
    }
    assert gaps["AST-BAD"].blocks_full_coverage is True

    released_ids = {r.assertion_id for r in state["released_assertion_results"].results}
    assert released_ids == {"AST-GOOD"}, "the healthy assertion must still be released"


def test_isolation_happens_within_the_item_budget() -> None:
    """Termination must be bounded, not merely eventual."""

    state = _run_with_churn()
    converter_calls = [
        record
        for record in state["node_execution_records"]
        if record.node_name == "convert_assertions"
    ]
    assert len(converter_calls) <= nodes.MAX_ASSERTION_PRECHECK_REPAIRS + 1, (
        f"expected isolation within the per-item budget, saw {len(converter_calls)} "
        "converter revisions"
    )


def test_quarantine_event_is_written_to_the_revision_ledger() -> None:
    state = _run_with_churn()
    events = [
        event
        for event in state["_assertion_revision_ledger"]
        if event.event == "artifact_quarantined"
    ]
    assert events, "isolation must leave an append-only ledger event"
    assert "AST-BAD" in events[-1].item_ids
    assert state["_quarantined_assertion_ids"] == ("AST-BAD",)


def test_semantic_key_ignores_expression_text_but_splits_on_error_type() -> None:
    same_a = nodes._semantic_invalid_key(
        "AST-1", "{'error': {'type': 'FBMCQUnsupportedEvidence'}}", "ck"
    )
    same_b = nodes._semantic_invalid_key(
        "AST-1", "{'error': {'type': 'FBMCQUnsupportedEvidence', 'message': 'other'}}", "ck"
    )
    other = nodes._semantic_invalid_key(
        "AST-1", "{'error': {'type': 'UnsupportedEvidence'}}", "ck"
    )
    assert same_a == same_b, "message churn must not create a fresh identity"
    assert same_a != other, "a genuinely different failure mode is new information"
    assert nodes._semantic_invalid_key("AST-1", None, "ck").endswith("|unknown|ck")


def test_contract_repair_budget_is_not_reset_by_an_intervening_success() -> None:
    """A fail/succeed/fail producer must not buy unlimited contract repairs."""

    source = (SRC / "paper_stm_feedback_loop" / "discover" / "nodes.py").read_text()
    assert '"_assertion_contract_repair_count": 0,' not in source, (
        "resetting the contract budget on success re-opens the pair-0029 loop"
    )


# --------------------------------------------------------------------------
# Harder: the failure *mode* churns too, so only the per-item budget can bite
# --------------------------------------------------------------------------

ALTERNATING_BROKEN_EXPRESSIONS = [
    "len(states(",            # syntax error
    "undefined_helper()",     # unregistered name -> audit rejection
    "42",                     # non-bool terminal
    "len(states((",           # syntax error again, different text
    "another_unknown()",      # unregistered name again, different text
    "3.5",                    # non-bool again
    "len(states(((",
    "yet_another_unknown()",
]


def test_alternating_failure_modes_are_bounded_by_the_item_budget() -> None:
    """Semantic-key churn must still terminate: the per-item budget backstops it."""

    revision = 0

    def responder(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        nonlocal revision
        if schema is RequirementSet:
            return _requirements()
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept", reviewed_revision=1, rationale="Faithful."
            )
        if schema is AssertionScript:
            expression = ALTERNATING_BROKEN_EXPRESSIONS[
                min(revision, len(ALTERNATING_BROKEN_EXPRESSIONS) - 1)
            ]
            revision += 1
            return _script(revision, expression)
        if schema is AssertionReview:
            return AssertionReview(
                decision="accept",
                reviewed_script_hash="TO_BE_PATCHED",
                rationale="Remaining assertions are adequate.",
            )
        if schema is DiscoverAdjudication:
            return DiscoverAdjudication(
                has_confirmed_issues=False,
                satisfied_requirement_ids=("REQ-GOOD",),
                rationale="The released assertion passed.",
            )
        raise TypeError(f"unsupported schema {schema}")

    state = run_discover_state(
        DiscoverInput(
            run_id="s3-alternating",
            natural_language="Idle shall reach Done on go.",
            stm_text=MODEL,
            language="en-US",
        ),
        responder,
    )
    assert "failure" not in state
    published = state["final_output"]
    assert published.status == "completed"
    assert published.coverage_status == "partial"
    assert {gap.assertion_ids[0] for gap in published.coverage_gaps} == {"AST-BAD"}
    assert {
        r.assertion_id for r in state["released_assertion_results"].results
    } == {"AST-GOOD"}

    converter_calls = [
        record
        for record in state["node_execution_records"]
        if record.node_name == "convert_assertions"
    ]
    assert len(converter_calls) <= nodes.MAX_ASSERTION_PRECHECK_REPAIRS + 1


# --------------------------------------------------------------------------
# S2c: an unresolved *review* finding must isolate, not fail the run
# --------------------------------------------------------------------------


def test_unresolved_assertion_review_isolates_instead_of_failing_the_run() -> None:
    """Issue #167 §3: a local review finding must not escalate to RUN_FAILED."""

    revision = 0

    def responder(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        nonlocal revision
        if schema is RequirementSet:
            return _requirements()
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept", reviewed_revision=1, rationale="Faithful."
            )
        if schema is AssertionScript:
            revision += 1
            return _script(
                revision,
                'transition_exists(source="Root.Idle", event="Root.go", target="Root.Idle")',
                bad_family="relation",
            )
        if schema is AssertionReview:
            return AssertionReview(
                decision="revise",
                reviewed_script_hash="TO_BE_PATCHED",
                rationale="AST-BAD still does not operationalize REQ-BAD.",
                findings=(
                    {
                        "assertion_id": "AST-BAD",
                        "severity": "critical",
                        "message": "The check does not test the stated obligation.",
                        "required_change": "Assert the obligation REQ-BAD actually states.",
                    },
                ),
            )
        if schema is DiscoverAdjudication:
            return DiscoverAdjudication(
                has_confirmed_issues=False,
                satisfied_requirement_ids=("REQ-GOOD",),
                rationale="The released assertion passed.",
            )
        raise TypeError(f"unsupported schema {schema}")

    state = run_discover_state(
        DiscoverInput(
            run_id="s2c-review",
            natural_language="Idle shall reach Done on go.",
            stm_text=MODEL,
            language="en-US",
        ),
        responder,
    )
    assert "failure" not in state, "an unresolved review finding must not fail the run"
    published = state["final_output"]
    assert published.status == "completed"
    assert published.coverage_status == "partial"
    review_gaps = [
        gap for gap in published.coverage_gaps if gap.reason_code == "review_unresolved"
    ]
    assert review_gaps, "the isolated assertion must leave a review_unresolved gap"
    assert review_gaps[0].assertion_ids == ("AST-BAD",)
    assert {
        r.assertion_id for r in state["released_assertion_results"].results
    } == {"AST-GOOD"}
