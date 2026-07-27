"""S1 regression: decisive static evidence may close a `property` requirement.

Worked case this pins down (pair 0029, PR #169):
``enter_hwy`` has two guardless transitions on the same event to ``cruise`` and
``lane_change``.  Both GPT-5.5 and Claude froze the distinguishability
requirement as ``property`` -- defensible, since it quantifies over variable
valuations -- and both wrote the correct check
``not conflicting_targets(source=..., event=...)``.  The v2 contract then
demanded an additional ``fbmcq`` primary that FBMCQ cannot express (it observes
executions, not guard syntax) and that does not even compile on that model.
Both runs burned out without publishing anything.

``FIXTURE_MODEL`` below reproduces exactly that shape in nine lines, so the
whole regression runs offline in milliseconds with no LLM and no pair data.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import (  # noqa: E402
    AssertionChecker,
    build_eval_environment,
)
from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    EVIDENCE_CAPABILITY,
    called_evidence_functions,
    mandatory_waiver,
)
from paper_stm_feedback_loop.discover.graph import run_discover_state  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionReview,
    AssertionScript,
    DiscoverAdjudication,
    DiscoverInput,
    RequirementReview,
    RequirementSet,
)

# Same shape as pair 0029: one source, one event, two guardless targets.
FIXTURE_MODEL = """state Root {
    event pick;
    state Hub {
        state Entry;
        state Alpha;
        state Beta;
        [*] -> Entry;
        Entry -> Alpha : /pick;
        Entry -> Beta : /pick;
    }
    state Done;
    [*] -> Hub;
    Hub -> Done : /pick;
}
"""

CONFLICT_EXPR = 'not conflicting_targets(source="Root.Hub.Entry", event="Root.pick")'

# Minimal author-level trace so the False result can bind to a safe attribution,
# mirroring the real pair traces where these two edges are author-authored.
SOURCE_TRACE = {
    "entries": [
        {
            "trace_id": "trace:transition:Entry-pick",
            "intermediate_elements": ["transition:3", "transition:4"],
            "source_elements": ["puml:line:8", "puml:line:9"],
            "attribution_boundary": {
                "source_level_claim_allowed": True,
                "representation_related": False,
                "conversion_or_lowering_related": False,
            },
        }
    ],
    "attribution_exclusions": [],
}


# --------------------------------------------------------------------------
# The ground truth the whole pipeline exists to reach
# --------------------------------------------------------------------------


def test_conflicting_targets_decides_the_shared_event_conflict_offline() -> None:
    """The relation check settles pair 0029's proposition without any LLM."""

    environment = build_eval_environment(
        model_text=FIXTURE_MODEL,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=10,
    )
    checker = AssertionChecker(environment=environment)
    result = checker.check(
        f'assert {CONFLICT_EXPR}, "[REQ-001][AST-001] targets are indistinguishable"',
        "offline probe",
        required_function_families=("relation",),
    )
    assert result.outcome == "sealed_false"
    assert result.value is False


# --------------------------------------------------------------------------
# Capability metadata
# --------------------------------------------------------------------------


def test_called_evidence_functions_reads_plain_and_attribute_calls() -> None:
    assert called_evidence_functions(CONFLICT_EXPR) == frozenset(
        {"conflicting_targets"}
    )
    assert "fbmcq" in called_evidence_functions('fbmcq("check reach <= 1: x;").holds')
    assert called_evidence_functions("len(states(") == frozenset()


def test_decisive_static_procedure_waives_property_mandatory_family() -> None:
    waiver = mandatory_waiver("property", (CONFLICT_EXPR,))
    assert waiver is not None
    function_name, justification = waiver
    assert function_name == "conflicting_targets"
    assert justification, "a waiver must carry an auditable justification"


def test_witness_evidence_never_waives_anything() -> None:
    assert mandatory_waiver("property", ('simulate(cycles=[["Root.pick"]])',)) is None
    assert mandatory_waiver("property", ('transition_exists(event="Root.pick")',)) is None


def test_behavior_is_never_waived_by_static_evidence() -> None:
    """The 0000 cold-start regression must keep being caught.

    A static relation query does not witness a runtime response, so it must not
    stand in for the mandatory simulation of a ``behavior`` requirement.
    """

    assert mandatory_waiver("behavior", (CONFLICT_EXPR,)) is None
    assert mandatory_waiver("behavior", ('initial_child("Root.Hub")',)) is None


def test_every_waiving_capability_is_decisive_and_justified() -> None:
    for name, capability in EVIDENCE_CAPABILITY.items():
        if not capability.waives_mandatory_for:
            continue
        assert capability.completeness == "decisive", name
        assert capability.justification.strip(), name
        assert "behavior" not in capability.waives_mandatory_for, name


# --------------------------------------------------------------------------
# End-to-end: the 0029 shape must now publish instead of dying on contract
# --------------------------------------------------------------------------


def _responder_property_closed_by_relation(
    _role: str, schema: type[BaseModel], _system: str, _payload: str
) -> BaseModel:
    if schema is RequirementSet:
        return RequirementSet(
            revision=1,
            requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": (
                        "Alpha and Beta must be distinguishable under the shared pick condition."
                    ),
                    "verification_kind": "property",
                    "quantifier": "for every variable valuation",
                    "coverage_obligation": {
                        "domain": "Root.Hub.Entry target distinguishability",
                        "aggregation": "all",
                    },
                },
            ),
            segment_disposition={"NL-L001": "covered"},
        )
    if schema is RequirementReview:
        return RequirementReview(
            decision="accept",
            reviewed_revision=1,
            rationale="The distinguishability obligation is faithful to the source.",
        )
    if schema is AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": "Shared-event targets must not be indistinguishable.",
                    "expression": CONFLICT_EXPR,
                    "failure_message": (
                        "[REQ-001][AST-REQ-001-01] Entry reaches Alpha and Beta "
                        "under one event with no discriminating guard."
                    ),
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "distinguishability:Entry-pick",
                    "aggregation_group": "REQ-001:all",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )
    if schema is AssertionReview:
        return AssertionReview(
            decision="accept",
            reviewed_script_hash="TO_BE_PATCHED",
            rationale="The relation check operationalizes the obligation exactly.",
        )
    if schema is DiscoverAdjudication:
        return DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-001",
                    "requirement_id": "REQ-001",
                    "assertion_ids": ("AST-REQ-001-01",),
                    "title": "Shared-condition targets are indistinguishable",
                    "rationale": "The released primary assertion is False.",
                    "attribution_status": "safe",
                },
            ),
            rationale="One primary False with safe attribution.",
        )
    raise TypeError(f"unsupported schema {schema}")


def test_property_requirement_closes_on_decisive_relation_evidence() -> None:
    """Before S1 this raised `missing mandatory primary ... ['fbmcq']`."""

    state = run_discover_state(
        DiscoverInput(
            run_id="s1-waiver",
            natural_language=(
                "From Entry the system may go to Alpha or Beta based on pick; "
                "the choice must be distinguishable."
            ),
            stm_text=FIXTURE_MODEL,
            language="en-US",
            source_trace=SOURCE_TRACE,
        ),
        _responder_property_closed_by_relation,
    )
    assert "failure" not in state
    published = state["final_output"]
    assert published.status == "completed"
    assert [issue.requirement_id for issue in published.issues] == ["REQ-001"]

    waivers = [
        detail
        for record in state["node_execution_records"]
        for detail in (record.details or {}).get("mandatory_evidence_waivers", [])
    ]
    assert len(waivers) == 1, "the waiver must be recorded for audit"
    assert waivers[0]["requirement_id"] == "REQ-001"
    assert waivers[0]["waived_families"] == ["fbmcq"]
    assert waivers[0]["decisive_function"] == "conflicting_targets"


def test_property_requirement_without_decisive_evidence_still_requires_fbmcq() -> None:
    """The waiver must be an allowlist, not a hole in the contract."""

    def responder(
        role: str, schema: type[BaseModel], system: str, payload: str
    ) -> BaseModel:
        if schema is AssertionScript:
            return AssertionScript(
                revision=1,
                assertions=(
                    {
                        "assertion_id": "AST-REQ-001-01",
                        "requirement_id": "REQ-001",
                        "description": "Presence-only locator offered as primary.",
                        "expression": 'transition_exists(event="Root.pick")',
                        "failure_message": "[REQ-001][AST-REQ-001-01] missing edge",
                        "evidence_family": "relation",
                        "role": "primary",
                        "coverage_key": "distinguishability:Entry-pick",
                        "aggregation_group": "REQ-001:all",
                    },
                ),
                requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
            )
        return _responder_property_closed_by_relation(role, schema, system, payload)

    with pytest.raises(RuntimeError):
        run_discover_state(
            DiscoverInput(
                run_id="s1-no-waiver",
                natural_language="Alpha or Beta must be distinguishable.",
                stm_text=FIXTURE_MODEL,
                language="en-US",
            ),
            responder,
        )


# --------------------------------------------------------------------------
# S4: a pair where bounded formal checking cannot run must not be held to it
# --------------------------------------------------------------------------


def _responder_property_with_locator_primary(
    role: str, schema: type[BaseModel], system: str, payload: str
) -> BaseModel:
    if schema is DiscoverAdjudication:
        # The locator assertion is True on this model, so there is nothing to
        # confirm; the point of the test is that the run reaches adjudication.
        return DiscoverAdjudication(
            has_confirmed_issues=False,
            satisfied_requirement_ids=("REQ-001",),
            rationale="The released primary assertion passed.",
        )
    if schema is AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": "Locator-strength evidence, not a decision procedure.",
                    "expression": 'transition_exists(source="Root.Hub.Entry", event="Root.pick", target="Root.Hub.Alpha")',
                    "failure_message": "[REQ-001][AST-REQ-001-01] the edge is absent",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "distinguishability:Entry-pick",
                    "aggregation_group": "REQ-001:all",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )
    return _responder_property_closed_by_relation(role, schema, system, payload)


def test_infeasible_fbmcq_canary_waives_the_unsatisfiable_mandatory_family() -> None:
    state = run_discover_state(
        DiscoverInput(
            run_id="s4-canary-infeasible",
            natural_language="Alpha or Beta must be distinguishable.",
            stm_text=FIXTURE_MODEL,
            language="en-US",
            source_trace=SOURCE_TRACE,
            manifest={
                "fbmcq_canary": {
                    "feasible": False,
                    "reason": "compile_timeout",
                    "bound": 3,
                    "elapsed_ms": 45016.79,
                }
            },
        ),
        _responder_property_with_locator_primary,
    )
    assert "failure" not in state
    waivers = [
        detail
        for record in state["node_execution_records"]
        for detail in (record.details or {}).get("mandatory_evidence_waivers", [])
    ]
    assert len(waivers) == 1
    assert waivers[0]["decisive_function"] == "fbmcq_canary"
    assert "compile_timeout" in waivers[0]["justification"]


def test_feasible_fbmcq_canary_keeps_the_strict_contract() -> None:
    """A pair where FBMCQ works must still be held to the mandatory family."""

    with pytest.raises(RuntimeError):
        run_discover_state(
            DiscoverInput(
                run_id="s4-canary-feasible",
                natural_language="Alpha or Beta must be distinguishable.",
                stm_text=FIXTURE_MODEL,
                language="en-US",
                source_trace=SOURCE_TRACE,
                manifest={"fbmcq_canary": {"feasible": True, "reason": "compiled"}},
            ),
            _responder_property_with_locator_primary,
        )


def test_fbmcq_canary_bound_must_be_discriminating() -> None:
    from paper_stm_feedback_loop.assertions.fbmcq import probe_fbmcq_feasibility

    with pytest.raises(ValueError):
        probe_fbmcq_feasibility(FIXTURE_MODEL, bound=1)


def test_fbmcq_structural_binding_rejects_unknown_paths_before_the_solver() -> None:
    """A hallucinated state path must die in microseconds, not in the solver."""

    import time as _time

    environment = build_eval_environment(
        model_text=FIXTURE_MODEL,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=10,
        fbmcq_process_wall_seconds=30.0,
    )
    checker = AssertionChecker(environment=environment)
    started = _time.perf_counter()
    result = checker.check(
        'assert fbmcq(\'check reach <= 3: active("Root.Hub.DoesNotExist");\').holds is True, '
        '"[REQ-001][AST-001] bogus"',
        "bind probe",
        required_function_families=("formal",),
    )
    elapsed = _time.perf_counter() - started
    assert result.outcome == "invalid"
    assert elapsed < 5.0, f"structural rejection took {elapsed:.2f}s"


# --------------------------------------------------------------------------
# S5: official guides are injected, and non-vacuity is enforced not advised
# --------------------------------------------------------------------------


def test_official_pyfcstm_guides_are_injected_with_provenance() -> None:
    from paper_stm_feedback_loop.discover import prompts

    for marker in ("must_reach", "exists_always", "forbid", "havoc"):
        assert marker in prompts.ASSERTION_CONVERTER_PROMPT, marker
        assert marker in prompts.ASSERTION_REVIEWER_PROMPT, marker
    assert "FCSTM grammar guide" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "FCSTM grammar guide" in prompts.REQUIREMENT_SPLITTER_PROMPT

    provenance = prompts.guide_provenance()
    for key in ("fbmcq_language_guide", "fcstm_grammar_guide"):
        assert provenance[key]["sha256"] == provenance[key]["expected_sha256"], key


def test_capability_boundary_tells_the_producer_what_fbmcq_cannot_see() -> None:
    from paper_stm_feedback_loop.discover import prompts

    boundary = prompts.FBMCQ_CAPABILITY_BOUNDARY
    assert "cannot observe guard expressions" in boundary
    assert "conflicting_targets" in boundary
    assert "exponential in the bound" in boundary


P0029 = "llms_emp_feedback_final_0029"
REAL_QUERIES_THAT_PROVED_NOTHING = [
    # Claude revisions 3-6: sibling states of one sequential region.
    f'fbmcq(\'init state("{P0029}.HighwayMode.enter_hwy"); check invariant <= 3: '
    f'!(active("{P0029}.HighwayMode.lane_change") && active("{P0029}.HighwayMode.cruise"));\').holds is True',
    f'fbmcq(\'init state("{P0029}.HighwayMode.enter_hwy"); check reach <= 3: '
    f'active("{P0029}.HighwayMode.lane_change") && active("{P0029}.HighwayMode.cruise");\').holds is False',
    # GPT revisions 6, 8/11, 12: unanchored reachability probes.
    f'fbmcq(\'check reach <= 5: active("{P0029}.HighwayMode.enter_hwy");\').holds is True',
    f'fbmcq(\'check reach <= 5: active("{P0029}.HighwayMode.cruise");\').holds is True',
    f'fbmcq(\'check reach <= 0: active("{P0029}.AutonomousMode");\').holds is True',
]


def test_real_non_evidential_queries_are_rejected_statically() -> None:
    from paper_stm_feedback_loop.discover.capability import fbmcq_non_vacuity_findings

    for query in REAL_QUERIES_THAT_PROVED_NOTHING:
        assert fbmcq_non_vacuity_findings(query), query[:90]


def test_anchored_queries_and_non_fbmcq_evidence_are_left_alone() -> None:
    from paper_stm_feedback_loop.discover.capability import fbmcq_non_vacuity_findings

    anchored = (
        f'fbmcq(\'init state("{P0029}.HighwayMode.enter_hwy"); check reach <= 3: '
        f'active("{P0029}.HighwayMode.cruise");\').holds is True'
    )
    assert fbmcq_non_vacuity_findings(anchored) == ()
    assert fbmcq_non_vacuity_findings(CONFLICT_EXPR) == ()


def test_published_artifact_carries_excluded_primary_findings() -> None:
    """A non-attributable primary False must remain visible after publication.

    On pair 0006 the adjudicator correctly filed EXP-0006-EA-001's False effect
    assertion under `excluded_findings / representation_debt`, but the published
    `DiscoverCompleted` had no such field, so the observation vanished from the
    only artifact a downstream audit reads.
    """

    from paper_stm_feedback_loop.discover.schemas import DiscoverCompleted

    assert "excluded_findings" in DiscoverCompleted.model_fields
    source = (
        SRC / "paper_stm_feedback_loop" / "discover" / "nodes.py"
    ).read_text()
    assert "excluded_findings=adjudication.excluded_findings" in source
