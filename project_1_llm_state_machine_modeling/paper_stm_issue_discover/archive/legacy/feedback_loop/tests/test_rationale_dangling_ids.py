"""A rationale must not cite an assertion the record does not list.

On pair 0029 the adjudicator put a supporting assertion into an issue's `assertion_ids` --
it was following the prompt, which said to retain every supporting id. The deterministic
layer trimmed it, correctly, but the trim only touched the id list. The published rationale
still read "AST-REQ-012-2's edge_declared also returns False", naming an assertion that no
longer appeared anywhere in the record. A reader auditing that issue had no way to check the
claim or even to find out what happened to it.

The trim is not the thing to change: supporting evidence genuinely cannot create an issue.
What was missing is that the record never said the trim occurred. So the id is annotated in
place rather than deleted -- the sentence keeps its shape, the reader learns the assertion
was removed and why, and the audit trail survives.

Raising instead was considered and rejected. `adjudicate_results` has no contract-feedback
retry, so its exception path is `_fail_state` -- one dangling id in a sentence would discard
the whole cell. Across the eight cells this fired once, which over a wider sweep would mean
losing runs to a wording slip in a field no check reads.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    DiscoverAdjudication,
    DiscoverInput,
    ReleasedAssertionResults,
    RequirementSet,
)

STM = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def _input() -> DiscoverInput:
    return DiscoverInput(
        run_id="dangling",
        natural_language="After go, Done shall become active.",
        stm_text=STM,
        language="en-US",
    )


def _fixture() -> dict:
    """One Requirement with a primary and a supporting assertion, both False.

    This is the shape of pair 0029's REQ-012: the supporting assertion is real evidence and
    really is False, which is why the adjudicator reached for it.
    """
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-012-1",
                "requirement_id": "REQ-012",
                "description": "The primary claim.",
                "expression": "False",
                "failure_message": "[REQ-012][AST-REQ-012-1] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-012-1",
                "aggregation_group": "REQ-012:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-012-2",
                "requirement_id": "REQ-012",
                "description": "Corroborating evidence.",
                "expression": "False",
                "failure_message": "[REQ-012][AST-REQ-012-2] requirement failed",
                "evidence_family": "structure",
                "role": "supporting",
                "coverage_key": "AST-REQ-012-2",
                "aggregation_group": "REQ-012:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-012": ("AST-REQ-012-1", "AST-REQ-012-2")},
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-012-1",
                requirement_id="REQ-012",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
                role="primary",
            ),
            AssertionResult(
                assertion_id="AST-REQ-012-2",
                requirement_id="REQ-012",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
                role="supporting",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-012-1",
                "requirement_id": "REQ-012",
                "status": "safe",
                "source_refs": ("state:Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-012",
                "statement": "After go, Done becomes active.",
                "checkability": "structure",
            },
        ),
    )
    return {
        "script": script,
        "released": released,
        "attribution": attribution,
        "requirements": requirements,
    }


def _run(adjudication: DiscoverAdjudication) -> dict:
    from paper_stm_feedback_loop.discover import nodes

    fx = _fixture()
    return nodes.adjudicate_results(
        {
            "_input": _input(),
            "frozen_inputs": nodes._fallback_prepare(_input()),
            "requirement_set": fx["requirements"],
            "assertion_script": fx["script"],
            "released_assertion_results": fx["released"],
            "attribution_projection": fx["attribution"],
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: adjudication
        ),
    )


def _cites_supporting() -> DiscoverAdjudication:
    return DiscoverAdjudication(
        has_confirmed_issues=True,
        issues=(
            {
                "issue_id": "ISSUE-REQ-012",
                "requirement_ids": ("REQ-012",),
                "assertion_ids": ("AST-REQ-012-1", "AST-REQ-012-2"),
                "title": "Done is not reachable",
                "rationale": (
                    "AST-REQ-012-1 is False, and AST-REQ-012-2's edge_declared "
                    "also returns False."
                ),
                "attribution_status": "safe",
            },
        ),
        satisfied_requirement_ids=(),
        rationale="The primary claim fails.",
    )


def test_the_trim_still_happens() -> None:
    """Supporting evidence cannot create an issue; that part was never wrong."""
    out = _run(_cites_supporting())
    assert "failure" not in out
    assert out["adjudication"].issues[0].assertion_ids == ("AST-REQ-012-1",)


def test_a_trimmed_id_is_annotated_rather_than_left_dangling() -> None:
    """The reader learns what became of the citation instead of hitting a dead name."""
    out = _run(_cites_supporting())
    rationale = out["adjudication"].issues[0].rationale
    assert "AST-REQ-012-1" in rationale, "the surviving citation must be untouched"
    assert "AST-REQ-012-2 [" in rationale, rationale
    assert "supporting" in rationale


def test_the_cell_is_not_discarded_over_a_dangling_id() -> None:
    """`adjudicate_results` has no retry, so raising here would cost the whole run."""
    assert "failure" not in _run(_cites_supporting())


def test_the_trim_is_recorded_for_audit() -> None:
    """A silent rewrite of a published rationale would be its own traceability problem."""
    out = _run(_cites_supporting())
    trimmed = out["_adjudication_reconciliation"]["rationale_citations_annotated"]
    assert trimmed == ({"issue_id": "ISSUE-REQ-012", "assertion_ids": ("AST-REQ-012-2",)},)


def test_a_clean_rationale_is_left_exactly_as_written() -> None:
    """No rewriting when there is nothing to annotate -- including the audit entry."""
    clean = DiscoverAdjudication(
        has_confirmed_issues=True,
        issues=(
            {
                "issue_id": "ISSUE-REQ-012",
                "requirement_ids": ("REQ-012",),
                "assertion_ids": ("AST-REQ-012-1",),
                "title": "Done is not reachable",
                "rationale": "AST-REQ-012-1 is False.",
                "attribution_status": "safe",
            },
        ),
        satisfied_requirement_ids=(),
        rationale="The primary claim fails.",
    )
    out = _run(clean)
    assert out["adjudication"].issues[0].rationale == "AST-REQ-012-1 is False."
    assert out["_adjudication_reconciliation"]["rationale_citations_annotated"] == ()
