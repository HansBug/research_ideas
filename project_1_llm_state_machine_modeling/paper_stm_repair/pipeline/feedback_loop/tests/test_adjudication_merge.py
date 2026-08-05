"""One defect reported once, even when it broke several Requirements.

Requirements are split for checkability, not for root cause: `occupancy_after` has to name
a concrete `source`, so a specification sentence that leaves the source open ("on power off
the system shall reach the final state") becomes one Requirement per running mode. When the
model then hangs `Power_Off` off the initial pseudo-source, every one of those Requirements
fails -- for the same reason, at the same edge. The published result used to carry one issue
each, and the count of defects only came out right after a person deduplicated by hand.

So the adjudicator is allowed to group across Requirements. Two things keep that from turning
into a way to shrink the defect count by fiat. Structurally, `requirement_ids` must equal --
not merely intersect -- the Requirements owning the referenced assertions, so a group cannot
quietly drop a Requirement or claim one it never touched. Semantically, a group spanning more
than one Requirement has to say where the shared root cause is and name the model elements it
rests on; without those the merge is rejected rather than accepted on the model's say-so.

`excluded_findings` stays one Requirement per finding. It records evidence that could not be
attributed, and merging exclusions buys no accuracy while making them harder to trace back.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AdjudicatedIssue,
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    DiscoverAdjudication,
    DiscoverInput,
    ReleasedAssertionResults,
    RequirementSet,
)

# The defect this fixture stands in for: `power_off` reaches `Final` only from the
# pseudo-initial, so neither running mode can shut down.  Both Requirements below fail on
# that one missing pair of edges.
MODEL = """state Root {
    event power_off;
    state HumanDriving;
    state Autonomous;
    state Final;
    [*] -> HumanDriving;
    HumanDriving -> Autonomous : power_off;
}
"""


def _input(run_id: str = "merge") -> DiscoverInput:
    return DiscoverInput(
        run_id=run_id,
        natural_language="On power off the system shall reach the final state.",
        stm_text=MODEL,
        language="en-US",
    )


def _two_requirement_fixture() -> dict:
    """Two Requirements, both failing on the same missing `power_off` edge.

    This is pair 0000 reduced to its skeleton: one specification sentence that never says
    which running mode it applies to, split by the splitter into one Requirement per mode
    because `occupancy_after` cannot be written without a concrete `source`.
    """
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-006A-1",
                "requirement_id": "REQ-006A",
                "description": "Power off from human driving reaches the final state.",
                "expression": "False",
                "failure_message": "[REQ-006A][AST-REQ-006A-1] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-006A-1",
                "aggregation_group": "REQ-006A:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
            {
                "assertion_id": "AST-REQ-006B-1",
                "requirement_id": "REQ-006B",
                "description": "Power off from autonomous reaches the final state.",
                "expression": "False",
                "failure_message": "[REQ-006B][AST-REQ-006B-1] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-006B-1",
                "aggregation_group": "REQ-006B:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={
            "REQ-006A": ("AST-REQ-006A-1",),
            "REQ-006B": ("AST-REQ-006B-1",),
        },
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-006A-1",
                requirement_id="REQ-006A",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
            AssertionResult(
                assertion_id="AST-REQ-006B-1",
                requirement_id="REQ-006B",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-006A-1",
                "requirement_id": "REQ-006A",
                "status": "safe",
                "source_refs": ("state:Root.HumanDriving",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
            {
                "assertion_id": "AST-REQ-006B-1",
                "requirement_id": "REQ-006B",
                "status": "safe",
                "source_refs": ("state:Root.Autonomous",),
                "trace_entry_ids": ("trace-2",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-006A",
                "statement": "Power off from human driving reaches the final state.",
                "checkability": "structure",
            },
            {
                "requirement_id": "REQ-006B",
                "statement": "Power off from autonomous reaches the final state.",
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

    fx = _two_requirement_fixture()
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


MERGED = {
    "issue_id": "ISSUE-PowerOff-Misplaced",
    "requirement_ids": ("REQ-006A", "REQ-006B"),
    "assertion_ids": ("AST-REQ-006A-1", "AST-REQ-006B-1"),
    "title": "Power off is not reachable from any running mode",
    "rationale": "Both modes fail because the power_off edge leaves the pseudo-initial.",
    "attribution_status": "safe",
    "shared_root_cause": "The power_off edge is anchored at the initial pseudo-source.",
    "shared_elements": ("Root.power_off", "Root.Final"),
}


def test_one_defect_across_two_requirements_is_published_once() -> None:
    out = _run(
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(MERGED,),
            satisfied_requirement_ids=(),
            rationale="Both failures are the same misplaced edge.",
        )
    )
    assert "failure" not in out
    issues = out["adjudication"].issues
    assert len(issues) == 1
    assert issues[0].requirement_ids == ("REQ-006A", "REQ-006B")
    assert issues[0].assertion_ids == ("AST-REQ-006A-1", "AST-REQ-006B-1")


def test_unmerged_issues_still_pass() -> None:
    """Not merging stays the safe default -- the closure check must not force a group."""
    out = _run(
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-REQ-006A",
                    "requirement_ids": ("REQ-006A",),
                    "assertion_ids": ("AST-REQ-006A-1",),
                    "title": "Human driving cannot power off",
                    "rationale": "The assertion is False.",
                    "attribution_status": "safe",
                },
                {
                    "issue_id": "ISSUE-REQ-006B",
                    "requirement_ids": ("REQ-006B",),
                    "assertion_ids": ("AST-REQ-006B-1",),
                    "title": "Autonomous cannot power off",
                    "rationale": "The assertion is False.",
                    "attribution_status": "safe",
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Reported separately.",
        )
    )
    assert "failure" not in out
    assert len(out["adjudication"].issues) == 2


@pytest.mark.parametrize("missing", ["shared_root_cause", "shared_elements"])
def test_merge_without_its_justification_is_rejected(missing: str) -> None:
    """A group spanning Requirements must say why, or it is not a group.

    Without this the adjudicator could halve the defect count by emitting one issue over
    every False assertion, and nothing downstream would notice.
    """
    payload = dict(MERGED)
    payload[missing] = None if missing == "shared_root_cause" else ()
    out = _run(
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(payload,),
            satisfied_requirement_ids=(),
            rationale="Merged without saying why.",
        )
    )
    assert "failure" in out


def test_requirement_ids_must_equal_the_referenced_requirements() -> None:
    """Naming a Requirement whose assertions are not referenced is a fabrication."""
    payload = dict(MERGED)
    payload["requirement_ids"] = ("REQ-006A", "REQ-006B", "REQ-999")
    out = _run(
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(payload,),
            satisfied_requirement_ids=(),
            rationale="Claims a Requirement it never touched.",
        )
    )
    assert "failure" in out


def test_dropping_a_referenced_requirement_is_rejected() -> None:
    """The mirror case: two assertions merged but only one Requirement acknowledged."""
    payload = dict(MERGED)
    payload["requirement_ids"] = ("REQ-006A",)
    out = _run(
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(payload,),
            satisfied_requirement_ids=(),
            rationale="Silently drops REQ-006B.",
        )
    )
    assert "failure" in out


def test_excluded_findings_spanning_requirements_are_split_apart() -> None:
    """Exclusions stay one Requirement each -- but enforced by splitting, not by refusing.

    The rule is unchanged: an exclusion records that attribution could not support a claim,
    which is per-Requirement by construction, so a group carries nothing the split does not.
    What changed is the remedy. Rejecting the response ended the run, and `v2run1/0050-gpt`
    lost forty minutes to exactly this shape. See `tests/test_adjudication_misfiling.py` for
    the split itself.
    """
    from paper_stm_feedback_loop.discover import nodes

    fx = _two_requirement_fixture()
    attribution = AttributionProjection(
        bindings=tuple(
            {**b.model_dump(), "status": "representation_debt"}
            for b in fx["attribution"].bindings
        )
    )
    out = nodes.adjudicate_results(
        {
            "_input": _input(),
            "frozen_inputs": nodes._fallback_prepare(_input()),
            "requirement_set": fx["requirements"],
            "assertion_script": fx["script"],
            "released_assertion_results": fx["released"],
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: DiscoverAdjudication(
                has_confirmed_issues=False,
                issues=(),
                excluded_findings=(
                    {
                        "issue_id": "ISSUE-DEBT-MERGED",
                        "requirement_ids": ("REQ-006A", "REQ-006B"),
                        "assertion_ids": ("AST-REQ-006A-1", "AST-REQ-006B-1"),
                        "title": "Both are representation debt",
                        "rationale": "Merged exclusion.",
                        "attribution_status": "representation_debt",
                        "shared_root_cause": "Same projected node.",
                        "shared_elements": ("Root.power_off",),
                    },
                ),
                satisfied_requirement_ids=(),
                rationale="Exclusions merged.",
            )
        ),
    )
    assert "failure" not in out, out.get("failure")
    excluded = out["adjudication"].excluded_findings
    assert len(excluded) == 2
    assert all(len(e.requirement_ids) == 1 for e in excluded)


def test_historical_records_using_requirement_id_still_parse() -> None:
    """Baseline comparison reads run records written before the field was pluralised.

    `StrictBaseModel` forbids unknown keys, so without an explicit migration every
    `discover-completed.json` from v11-v18 would fail to load and the before/after
    comparison this change is measured by could not be run at all.
    """
    legacy = AdjudicatedIssue.model_validate(
        {
            "issue_id": "ISSUE-REQ-006a-PowerOff-Human",
            "requirement_id": "REQ-006A",
            "assertion_ids": ["AST-REQ-006A-1"],
            "title": "Human driving cannot power off",
            "rationale": "The assertion is False.",
            "attribution_status": "safe",
        }
    )
    assert legacy.requirement_ids == ("REQ-006A",)
    assert legacy.shared_root_cause is None


def test_both_spellings_at_once_is_an_error() -> None:
    """Accepting both would leave two answers to "which Requirement" in one record."""
    with pytest.raises(ValidationError):
        AdjudicatedIssue.model_validate(
            {
                "issue_id": "ISSUE-AMBIGUOUS",
                "requirement_id": "REQ-006A",
                "requirement_ids": ["REQ-006B"],
                "assertion_ids": ["AST-REQ-006A-1"],
                "title": "Ambiguous",
                "rationale": "Two spellings disagree.",
                "attribution_status": "safe",
            }
        )
