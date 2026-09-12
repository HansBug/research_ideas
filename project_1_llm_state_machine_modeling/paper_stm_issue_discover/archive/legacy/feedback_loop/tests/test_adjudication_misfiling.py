"""Putting a finding in the wrong basket should not cost the whole run.

Three of the adjudicator's checks reject a response the deterministic layer could simply
correct. Which basket a False belongs in is not a judgement -- it follows from the assertion's
role and its attribution status, both of which are already known here. When the model files
one wrongly, refusing the whole response discards a run that had the right answer in it,
filed under the wrong heading.

That is not hypothetical. `run3/0029-gpt` died on `excluded findings must not be
attribution-safe` after tens of minutes and a full round of API spend, because one safe
finding had been placed among the exclusions. `adjudicate_results` has no contract-feedback
retry -- its exception path goes straight to `_fail_state` -- so there was no second chance.

So a misfiled finding is moved to where it belongs and the move is written into the
reconciliation record. What still raises is anything the deterministic layer cannot repair:
an assertion id that does not exist, a group whose Requirements do not match its evidence, a
merge without its justification. Those are claims about the evidence, not filing errors.
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
        run_id="misfiling",
        natural_language="After go, Done shall become active.",
        stm_text=STM,
        language="en-US",
    )


def _fixture(statuses: dict[str, str]) -> dict:
    """Two Requirements, each with one primary False, attribution as given."""
    ids = sorted(statuses)
    script = AssertionScript(
        revision=1,
        assertions=tuple(
            {
                "assertion_id": f"AST-{rid}-1",
                "requirement_id": rid,
                "description": f"{rid} holds.",
                "expression": "False",
                "failure_message": f"[{rid}][AST-{rid}-1] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": f"AST-{rid}-1",
                "aggregation_group": f"{rid}:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            }
            for rid in ids
        ),
        requirement_mapping={rid: (f"AST-{rid}-1",) for rid in ids},
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=tuple(
            AssertionResult(
                assertion_id=f"AST-{rid}-1",
                requirement_id=rid,
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
                role="primary",
            )
            for rid in ids
        ),
    )
    attribution = AttributionProjection(
        bindings=tuple(
            {
                "assertion_id": f"AST-{rid}-1",
                "requirement_id": rid,
                "status": statuses[rid],
                "source_refs": ("state:Root.Done",) if statuses[rid] == "safe" else (),
                "trace_entry_ids": ("trace-1",) if statuses[rid] == "safe" else (),
                "source_level_claim_allowed": statuses[rid] == "safe",
                "rationale": "fixture binding",
            }
            for rid in ids
        )
    )
    requirements = RequirementSet(
        revision=1,
        requirements=tuple(
            {"requirement_id": rid, "statement": f"{rid}.", "checkability": "structure"}
            for rid in ids
        ),
    )
    return {
        "script": script,
        "released": released,
        "attribution": attribution,
        "requirements": requirements,
    }


def _run(fixture: dict, adjudication: DiscoverAdjudication) -> dict:
    from paper_stm_feedback_loop.discover import nodes

    return nodes.adjudicate_results(
        {
            "_input": _input(),
            "frozen_inputs": nodes._fallback_prepare(_input()),
            "requirement_set": fixture["requirements"],
            "assertion_script": fixture["script"],
            "released_assertion_results": fixture["released"],
            "attribution_projection": fixture["attribution"],
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: adjudication
        ),
    )


def _finding(rid: str, status: str) -> dict:
    return {
        "issue_id": f"ISSUE-{rid}",
        "requirement_ids": (rid,),
        "assertion_ids": (f"AST-{rid}-1",),
        "title": f"{rid} fails",
        "rationale": "The primary assertion is False.",
        "attribution_status": status,
    }



def _rejected(out: dict) -> tuple:
    """The C1 residue: findings the adjudicator produced that failed a structural check.

    These checks used to raise, killing the cell. Each keeps its exact semantics; only the
    consequence changed -- the offending finding is dropped and recorded, per issue #167 §3
    ("a defect localised to one finding must cost that finding, not the run"). Asserting on
    `"failure" in out` would pin the consequence, which is what these tests did before and
    what made `adjudicate_results` responsible for 13 dead cell-rounds across the run tree.
    """
    assert "failure" not in out, "a local structural defect must not kill the cell"
    recon = out.get("_adjudication_reconciliation") or {}
    return tuple(recon.get("rejected_issues") or ()) + tuple(
        recon.get("rejected_exclusions") or ()
    )

def test_a_safe_finding_filed_as_an_exclusion_is_moved_not_rejected() -> None:
    """The exact failure that killed run3/0029-gpt."""
    fx = _fixture({"REQ-001": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(_finding("REQ-001", "safe"),),
            satisfied_requirement_ids=(),
            rationale="Misfiled: this is attribution-safe.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    adjudication = out["adjudication"]
    assert [i.issue_id for i in adjudication.issues] == ["ISSUE-REQ-001"]
    assert adjudication.excluded_findings == ()
    assert adjudication.has_confirmed_issues is True


def test_an_unattributed_finding_filed_as_an_issue_is_moved_not_rejected() -> None:
    """The mirror direction -- and the more dangerous one if left uncorrected.

    A non-safe False presented as a confirmed issue is a claim the attribution layer refused
    to support. Moving it keeps that refusal visible instead of discarding the run.
    """
    fx = _fixture({"REQ-001": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(_finding("REQ-001", "unattributed"),),
            satisfied_requirement_ids=(),
            rationale="Misfiled: attribution is not safe.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    adjudication = out["adjudication"]
    assert adjudication.issues == ()
    assert [e.issue_id for e in adjudication.excluded_findings] == ["ISSUE-REQ-001"]
    assert adjudication.has_confirmed_issues is False


def test_every_move_is_written_into_the_reconciliation_record() -> None:
    """Silently relocating a published finding would be its own traceability problem."""
    fx = _fixture({"REQ-001": "safe", "REQ-002": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(_finding("REQ-002", "unattributed"),),
            excluded_findings=(_finding("REQ-001", "safe"),),
            satisfied_requirement_ids=(),
            rationale="Both baskets swapped.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    moves = out["_adjudication_reconciliation"]["misfiled_findings_moved"]
    assert {(m["issue_id"], m["from"], m["to"]) for m in moves} == {
        ("ISSUE-REQ-001", "excluded_findings", "issues"),
        ("ISSUE-REQ-002", "issues", "excluded_findings"),
    }


def test_a_correctly_filed_response_records_no_moves() -> None:
    fx = _fixture({"REQ-001": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(_finding("REQ-001", "safe"),),
            satisfied_requirement_ids=(),
            rationale="Correctly filed.",
        ),
    )
    assert "failure" not in out
    assert out["_adjudication_reconciliation"]["misfiled_findings_moved"] == ()


def test_a_merge_resting_on_one_shared_element_is_flagged_but_not_rejected() -> None:
    """The shape of the only questionable merge in three rounds.

    On `0006-gpt` the adjudicator merged `state_declared(Searching, composite)` with
    `cardinality(Searching, 3)` and named one shared element: `Searching`, which both
    Requirements merely bind to. Binding to the same state is not the same defect -- one says
    its type is wrong, the other that its contents are missing.

    Rejecting it outright would be wrong too: a genuine single-element merge is possible, and
    this layer cannot tell the two apart. So it is recorded for the reviewer rather than
    decided here.
    """
    fx = _fixture({"REQ-001": "safe", "REQ-002": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-THIN-MERGE",
                    "requirement_ids": ("REQ-001", "REQ-002"),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "Both fail at Root.Done",
                    "rationale": "Both rest on Root.Done.",
                    "attribution_status": "safe",
                    "shared_root_cause": "Root.Done is wrong.",
                    "shared_elements": ("Root.Done",),
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Merged on one element.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    thin = out["_adjudication_reconciliation"]["thin_merge_warnings"]
    assert [w["issue_id"] for w in thin] == ["ISSUE-THIN-MERGE"]
    assert thin[0]["shared_elements"] == ("Root.Done",)


def test_a_merge_naming_several_shared_elements_is_not_flagged() -> None:
    fx = _fixture({"REQ-001": "safe", "REQ-002": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-GOOD-MERGE",
                    "requirement_ids": ("REQ-001", "REQ-002"),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "The go edge is missing from both",
                    "rationale": "One missing edge explains both.",
                    "attribution_status": "safe",
                    "shared_root_cause": "The go edge is absent.",
                    "shared_elements": ("Root.go", "Root.Done", "Root.Idle"),
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Merged on a real shared cause.",
        ),
    )
    assert "failure" not in out
    assert out["_adjudication_reconciliation"]["thin_merge_warnings"] == ()


def test_unrepairable_errors_still_raise() -> None:
    """Filing is correctable; a claim that does not match its evidence is not."""
    fx = _fixture({"REQ-001": "safe", "REQ-002": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-WRONG-REQS",
                    "requirement_ids": ("REQ-001",),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "Claims one Requirement while citing two",
                    "rationale": "Mismatched.",
                    "attribution_status": "safe",
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Unrepairable.",
        ),
    )
    rejected = _rejected(out)
    assert rejected, "the offending finding must be recorded, not silently kept"
    assert not (out["adjudication"].issues or ()), "it must not survive into issues"


def test_a_wrong_label_on_a_correctly_filed_finding_is_also_repaired() -> None:
    """The half the first version of this sort missed.

    Sorting on the model's own `attribution_status` only repairs the case where the label is
    right and the basket wrong. They fail together though: a model that believes a finding is
    unattributed says so *and* files it as an exclusion. Pair 0029 happened to be the first
    kind; the second kind dies on `excluded finding attribution_status must match its
    bindings`, which is just as fatal.
    """
    fx = _fixture({"REQ-001": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(_finding("REQ-001", "representation_debt"),),
            satisfied_requirement_ids=(),
            rationale="Right basket, wrong label.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    excluded = out["adjudication"].excluded_findings
    assert [e.attribution_status for e in excluded] == ["unattributed"]
    moved = out["_adjudication_reconciliation"]["misfiled_findings_moved"]
    assert moved[0]["reported_status"] == "representation_debt"
    assert moved[0]["binding_status"] == "unattributed"


def test_a_mislabelled_merged_issue_survives_instead_of_dying_on_the_exclusion_rule() -> None:
    """The most expensive variant, because merges are what the experiment measures.

    A merged issue whose bindings are all safe but whose label says otherwise would, under a
    label-driven sort, be moved into `excluded_findings` -- where the single-Requirement rule
    for exclusions rejects it outright. Deriving the status from the bindings keeps it where
    the evidence says it belongs.
    """
    fx = _fixture({"REQ-001": "safe", "REQ-002": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-MERGED-MISLABELLED",
                    "requirement_ids": ("REQ-001", "REQ-002"),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "One cause, both Requirements",
                    "rationale": "A single missing edge explains both.",
                    "attribution_status": "representation_debt",
                    "shared_root_cause": "The go edge is absent.",
                    "shared_elements": ("Root.go", "Root.Done"),
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Merged but mislabelled.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    issues = out["adjudication"].issues
    assert [i.issue_id for i in issues] == ["ISSUE-MERGED-MISLABELLED"]
    assert issues[0].attribution_status == "safe"
    assert issues[0].requirement_ids == ("REQ-001", "REQ-002")


def test_a_relocated_finding_says_so_in_its_rationale() -> None:
    """Its prose was written to explain an exclusion; published as an issue it would mislead.

    `build_gist.py` prints this text into the review bundle, so a reader doing the manual pass
    of issue #175 §7.2 sees exactly this sentence and nothing about where it came from.
    """
    fx = _fixture({"REQ-001": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(_finding("REQ-001", "safe"),),
            satisfied_requirement_ids=(),
            rationale="Misfiled.",
        ),
    )
    assert "failure" not in out
    rationale = out["adjudication"].issues[0].rationale
    assert rationale.startswith("The primary assertion is False.")
    assert "relocated from excluded_findings" in rationale


def test_closure_still_holds_when_some_findings_move_and_others_do_not() -> None:
    """The mixed case. One finding per Requirement makes the closure check pass trivially."""
    fx = _fixture({"REQ-001": "safe", "REQ-002": "safe", "REQ-003": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(_finding("REQ-001", "safe"), _finding("REQ-003", "unattributed")),
            excluded_findings=(_finding("REQ-002", "safe"),),
            satisfied_requirement_ids=(),
            rationale="One correct, one misfiled each way.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    adjudication = out["adjudication"]
    assert {i.issue_id for i in adjudication.issues} == {"ISSUE-REQ-001", "ISSUE-REQ-002"}
    assert {e.issue_id for e in adjudication.excluded_findings} == {"ISSUE-REQ-003"}
    # Both closure invariants: every safe False accounted for in issues, every non-safe one
    # in exclusions. With three Requirements these are no longer trivially satisfied.
    assert {a for i in adjudication.issues for a in i.assertion_ids} == {
        "AST-REQ-001-1",
        "AST-REQ-002-1",
    }
    assert {a for e in adjudication.excluded_findings for a in e.assertion_ids} == {
        "AST-REQ-003-1"
    }


def test_the_moves_reach_the_published_artifact() -> None:
    """`_adjudication_reconciliation` is state; what a reader opens is the published file."""
    from paper_stm_feedback_loop.discover import nodes

    fx = _fixture({"REQ-001": "safe"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(_finding("REQ-001", "safe"),),
            satisfied_requirement_ids=(),
            rationale="Misfiled.",
        ),
    )
    published = nodes.publish(
        {
            "_input": _input(),
            "frozen_inputs": nodes._fallback_prepare(_input()),
            "requirement_set": fx["requirements"],
            "assertion_script": fx["script"],
            "released_assertion_results": fx["released"],
            "attribution_projection": fx["attribution"],
            **out,
        }
    )
    assert "failure" not in published, published.get("failure")
    completed = published["final_output"]
    moves = completed.adjudication_reconciliation["misfiled_findings_moved"]
    assert [m["issue_id"] for m in moves] == ["ISSUE-REQ-001"]
    assert completed.model_dump_json()  # the record has to serialise, not just exist


def test_a_merged_exclusion_is_split_rather_than_rejected() -> None:
    """Exclusions stay one Requirement each, but enforcing that by refusal costs the run.

    `v2run1/0050-gpt` died here: the adjudicator grouped two non-safe findings into one
    exclusion, which the single-Requirement rule rejects. The grouping carries no information
    the split does not -- an exclusion records that attribution could not support a claim, and
    that is per-Requirement by construction -- so the deterministic layer takes it apart
    instead of discarding forty minutes of run.
    """
    fx = _fixture({"REQ-001": "unattributed", "REQ-002": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(
                {
                    "issue_id": "ISSUE-MERGED-EXCLUSION",
                    "requirement_ids": ("REQ-001", "REQ-002"),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "Both are unattributed",
                    "rationale": "Neither has a safe binding.",
                    "attribution_status": "unattributed",
                    "shared_root_cause": "Same projected node.",
                    "shared_elements": ("Root.Done", "Root.go"),
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Merged exclusion.",
        ),
    )
    assert "failure" not in out, out.get("failure")
    excluded = out["adjudication"].excluded_findings
    assert len(excluded) == 2
    assert {e.requirement_ids for e in excluded} == {("REQ-001",), ("REQ-002",)}
    assert {a for e in excluded for a in e.assertion_ids} == {
        "AST-REQ-001-1",
        "AST-REQ-002-1",
    }
    # The split has to be visible: a reader comparing counts across rounds would otherwise
    # see one exclusion become two with nothing in the record to explain it.
    split = out["_adjudication_reconciliation"]["merged_exclusions_split"]
    assert [s["issue_id"] for s in split] == ["ISSUE-MERGED-EXCLUSION"]
    assert split[0]["into"] == 2


def test_splitting_an_exclusion_keeps_its_prose_and_says_where_it_came_from() -> None:
    fx = _fixture({"REQ-001": "unattributed", "REQ-002": "unattributed"})
    out = _run(
        fx,
        DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            excluded_findings=(
                {
                    "issue_id": "ISSUE-MERGED-EXCLUSION",
                    "requirement_ids": ("REQ-001", "REQ-002"),
                    "assertion_ids": ("AST-REQ-001-1", "AST-REQ-002-1"),
                    "title": "Both are unattributed",
                    "rationale": "Neither has a safe binding.",
                    "attribution_status": "unattributed",
                    "shared_root_cause": "Same projected node.",
                    "shared_elements": ("Root.Done", "Root.go"),
                },
            ),
            satisfied_requirement_ids=(),
            rationale="Merged exclusion.",
        ),
    )
    excluded = out["adjudication"].excluded_findings
    assert all(e.rationale.startswith("Neither has a safe binding.") for e in excluded)
    assert all("split from ISSUE-MERGED-EXCLUSION" in e.rationale for e in excluded)
    # Issue ids have to stay distinct or a reader keying on them silently loses one.
    assert len({e.issue_id for e in excluded}) == 2

