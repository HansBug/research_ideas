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

CONFLICT_EXPR = 'guard_distinguishable(source="Root.Hub.Entry", trigger="Root.pick")'

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
        {"guard_distinguishable"}
    )
    assert "invariant" in called_evidence_functions('invariant(scope="R", condition="x", bound=1)')
    assert called_evidence_functions("len(states(") == frozenset()


def test_decisive_static_procedure_waives_property_mandatory_family() -> None:
    waiver = mandatory_waiver("property", (CONFLICT_EXPR,))
    assert waiver is not None
    function_name, justification = waiver
    assert function_name == "guard_distinguishable"
    assert justification, "a waiver must carry an auditable justification"


def test_witness_evidence_never_waives_anything() -> None:
    assert mandatory_waiver("property", ('simulate(cycles=[["Root.pick"]])',)) is None
    assert mandatory_waiver("property", ('edge_declared(source="Root.Hub.Entry", trigger="Root.pick", target="Root.Hub.Alpha")',)) is None


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
                    "rationale": "Fixture assertion; rationale not under test here.",
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
    assert [issue.requirement_ids for issue in published.issues] == [("REQ-001",)]

    waivers = [
        detail
        for record in state["node_execution_records"]
        for detail in (record.details or {}).get("mandatory_evidence_waivers", [])
    ]
    assert len(waivers) == 1, "the waiver must be recorded for audit"
    assert waivers[0]["requirement_id"] == "REQ-001"
    assert waivers[0]["waived_families"] == ["fbmcq"]
    assert waivers[0]["decisive_function"] == "guard_distinguishable"


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
                        "expression": 'edge_declared(source="Root.Hub.Entry", trigger="Root.pick", target="Root.Hub.Alpha")',
                        "failure_message": "[REQ-001][AST-REQ-001-01] missing edge",
                        "evidence_family": "relation",
                        "role": "primary",
                        "coverage_key": "distinguishability:Entry-pick",
                        "aggregation_group": "REQ-001:all",
                        "rationale": "Fixture assertion; rationale not under test here.",
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
                    "expression": 'edge_declared(source="Root.Hub.Entry", trigger="Root.pick", target="Root.Hub.Alpha")',
                    "failure_message": "[REQ-001][AST-REQ-001-01] the edge is absent",
                    "evidence_family": "relation",
                    "role": "primary",
                    "coverage_key": "distinguishability:Entry-pick",
                    "aggregation_group": "REQ-001:all",
                    "rationale": "Fixture assertion; rationale not under test here.",
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

    # The FBMCQ query language is intentionally withheld from the assertion
    # stages: bounded queries are constructed inside the predicates, so there is
    # no function an assertion could hand a query string to.  Showing a producer
    # a language it cannot reach only invites it to write one -- pair 0006's
    # hand-rolled `exists_always <= 1` tautology is what that produced.
    for marker in ("must_reach", "exists_always", "forbid", "havoc"):
        assert marker not in prompts.ASSERTION_CONVERTER_PROMPT, marker
        assert marker not in prompts.ASSERTION_REVIEWER_PROMPT, marker
    # The grammar guide stays: assertions still name model paths, and
    # `invariant(condition=...)` takes an FCSTM expression.
    assert "FCSTM grammar guide" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "FCSTM grammar guide" in prompts.REQUIREMENT_SPLITTER_PROMPT

    provenance = prompts.guide_provenance()
    for key in ("fbmcq_language_guide", "fcstm_grammar_guide"):
        assert provenance[key]["sha256"] == provenance[key]["expected_sha256"], key


def test_capability_boundary_tells_the_producer_what_the_evidence_cannot_see() -> None:
    from paper_stm_feedback_loop.discover import prompts

    boundary = prompts.PREDICATE_EVIDENCE_BOUNDARY
    assert "cannot observe guard expressions" in boundary
    assert "guard_distinguishable" in boundary
    assert "exponential in the bound" in boundary
    for name in ("ASSERTION_CONVERTER_PROMPT", "ASSERTION_REVIEWER_PROMPT"):
        assert boundary in getattr(prompts, name), name


P0029 = "llms_emp_feedback_final_0029"
REAL_QUERIES_THAT_PROVED_NOTHING = [
    # Claude revisions 3-6: sibling states of one sequential region.
    f'fbmcq(\'init state("{P0029}.HighwayMode.enter_hwy"); check invariant <= 3: '
    f'!(active("{P0029}.HighwayMode.lane_change") && active("{P0029}.HighwayMode.cruise"));\').holds is True',
    f'fbmcq(\'init state("{P0029}.HighwayMode.enter_hwy"); check reach <= 3: '
    f'active("{P0029}.HighwayMode.lane_change") && active("{P0029}.HighwayMode.cruise");\').holds is False',
]


#: The same vacuous claims, in the shape they can be written today.  The originals
#: were `fbmcq('...')` calls, which the closed vocabulary removed; the sibling
#: conjunction they encoded now travels in `invariant(condition=)` and
#: `persists_until(release=)`, so that is where the gate has to catch it.  The
#: unanchored `check reach` probes are not ported: `reaches` requires `source` and
#: `target`, so the anchorless shape no longer exists to reject.
VACUOUS_CONDITIONS_IN_TODAYS_SHAPE = [
    f'invariant(scope="{P0029}.HighwayMode", condition=\'!(active("{P0029}.HighwayMode.cruise") '
    f'&& active("{P0029}.HighwayMode.lane_change"))\', bound=4) is True',
    f'persists_until(scope="{P0029}.HighwayMode", condition=\'active("{P0029}.HighwayMode.cruise")\', '
    f'release=\'active("{P0029}.HighwayMode.cruise") && active("{P0029}.HighwayMode.lane_change")\', '
    f'bound=4) is True',
]


def test_real_non_evidential_queries_are_rejected_statically() -> None:
    """The gate looked for a call shape that no longer exists, so it caught nothing.

    `fbmcq(...)` left the assertion namespace when the vocabulary closed, and the
    gate's regex was keyed on it -- it ran on every script and returned empty every
    time, while the prompts went on describing the rule as enforced.  A vacuous
    `invariant` is a mandatory primary that cannot fail, so its requirement is
    reported satisfied and its expected issue is lost.
    """

    from paper_stm_feedback_loop.discover.capability import (
        condition_non_vacuity_findings,
    )

    for query in VACUOUS_CONDITIONS_IN_TODAYS_SHAPE:
        assert condition_non_vacuity_findings(query), query[:90]


def test_admissible_conditions_and_other_evidence_are_left_alone() -> None:
    from paper_stm_feedback_loop.discover.capability import (
        condition_non_vacuity_findings,
    )

    # A condition over one state says something the model can violate.
    admissible = (
        f'invariant(scope="{P0029}.HighwayMode", '
        f'condition=\'!active("{P0029}.HighwayMode.lane_change")\', bound=4) is True'
    )
    assert condition_non_vacuity_findings(admissible) == ()
    assert condition_non_vacuity_findings(CONFLICT_EXPR) == ()
    # A predicate with no condition binding is not this gate's business.
    assert condition_non_vacuity_findings(
        f'containment(parent="{P0029}.HighwayMode", child="{P0029}.HighwayMode.cruise") is True'
    ) == ()


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


# --------------------------------------------------------------------------
# A relation query over a non-existent element must not pass silently
# --------------------------------------------------------------------------


def test_unresolved_model_reference_is_detected() -> None:
    from paper_stm_feedback_loop.discover.capability import unresolved_model_references

    known = frozenset({"Root.Hub.Entry", "Root.pick"})
    # Exactly what Claude wrote on pair 0029: FCSTM transition syntax in place
    # of the event path, which made the guard-conflict check vacuously true.
    bad = 'guard_distinguishable(source="Root.Hub.Entry", trigger="/pick")'
    assert unresolved_model_references(bad, known) == ("trigger='/pick'",)
    assert unresolved_model_references(CONFLICT_EXPR, frozenset()) == ()
    good = 'guard_distinguishable(source="Root.Hub.Entry", trigger="Root.pick")'
    assert unresolved_model_references(good, known) == ()
    pseudo = 'edge_declared(source="[*]", trigger="Root.pick", target="Root.Hub.Alpha")'
    assert unresolved_model_references(pseudo, known) == ("target='Root.Hub.Alpha'",)


def test_slashed_event_path_would_have_passed_the_defect_and_is_now_rejected() -> None:
    """End-to-end: the vacuous form must never reach execution."""

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
                        "description": "Distinguishability, but with a mistyped event path.",
                        "expression": 'guard_distinguishable(source="Root.Hub.Entry", trigger="/pick")',
                        "failure_message": "[REQ-001][AST-REQ-001-01] indistinguishable",
                        "evidence_family": "relation",
                        "role": "primary",
                        "coverage_key": "distinguishability:Entry-pick",
                        "aggregation_group": "REQ-001:all",
                        "rationale": "Fixture assertion; rationale not under test here.",
                    },
                ),
                requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
            )
        return _responder_property_closed_by_relation(role, schema, system, payload)

    with pytest.raises(RuntimeError):
        run_discover_state(
            DiscoverInput(
                run_id="unresolved-ref",
                natural_language="Alpha or Beta must be distinguishable.",
                stm_text=FIXTURE_MODEL,
                language="en-US",
                source_trace=SOURCE_TRACE,
            ),
            responder,
        )


def test_source_blind_response_evidence_is_detected() -> None:
    """The gate must name a call that exists in the environment.

    It used to look for `transition_exists` and `transitions`, which the
    predicate vocabulary removed -- so it matched nothing and protected nothing
    while still reading as an active check.  `response_within` is the only
    predicate whose `source` is optional, so it is the only one that can still
    express pair 0000's mistake: from the initial configuration Power_Off does
    reach FinalState, and the requirement was reported satisfied while
    HumanDrivingMode could not reach it at all.
    """

    from paper_stm_feedback_loop.discover.capability import (
        source_omitting_response_calls,
    )

    blind = "response_within(trigger='Root.Power_Off', response='Root.FinalState', bound=5)"
    assert source_omitting_response_calls(blind) == ("response_within",)
    pinned = (
        "response_within(trigger='Root.Power_Off', response='Root.FinalState', "
        "bound=5, source='Root.HumanDrivingMode')"
    )
    assert source_omitting_response_calls(pinned) == ()
    assert source_omitting_response_calls(CONFLICT_EXPR) == ()
    assert source_omitting_response_calls("response_within(") == ()


def test_termination_requirement_rejects_source_blind_primary() -> None:
    """And the rejection must be *this* gate, named in the message.

    The fixture used `transition_exists`, which the predicate vocabulary removed.
    A bare `pytest.raises(RuntimeError)` then went on passing while a different
    gate did the rejecting -- so the source-blind rule had no integration cover at
    all, which is how it stayed dead through a whole redesign.
    """

    payloads: list[str] = []
    attempts = {"script": 0}

    def responder(
        role: str, schema: type[BaseModel], system: str, payload: str
    ) -> BaseModel:
        payloads.append(payload)
        if schema is RequirementSet:
            return RequirementSet(
                revision=1,
                requirements=(
                    {
                        "requirement_id": "REQ-001",
                        "statement": "On pick the system shall reach Done.",
                        "predicate": "response_within",
                        "predicate_bindings": {
                            "trigger": "Root.pick",
                            "response": "Root.Done",
                            "bound": "3",
                            "source": "Root.Idle",
                        },
                        "source_context": {
                            "basis": "explicit_nl",
                            "behavior_phase": "termination",
                        },
                        "coverage_obligation": {
                            "domain": "termination",
                            "aggregation": "all",
                        },
                    },
                ),
                segment_disposition={"NL-L001": "covered"},
            )
        if schema is AssertionScript:
            attempts["script"] += 1
            # First attempt omits `source`; later attempts pin it.  A responder
            # that never changes would end at the no-progress gate, and the
            # message under test would be buried behind that one.
            blind = attempts["script"] == 1
            return AssertionScript(
                revision=attempts["script"],
                assertions=(
                    {
                        "assertion_id": "AST-REQ-001-01",
                        "requirement_id": "REQ-001",
                        "description": "Bounded response.",
                        "expression": (
                            'response_within(trigger="Root.pick", '
                            'response="Root.Done", bound=3) is True'
                            if blind
                            else 'response_within(trigger="Root.pick", '
                            'response="Root.Done", bound=3, '
                            'source="Root.Idle") is True'
                        ),
                        "failure_message": "[REQ-001][AST-REQ-001-01] pick does not reach Done",
                        "evidence_family": "fbmcq",
                        "role": "primary",
                        "coverage_key": "termination:pick",
                        "aggregation_group": "REQ-001:all",
                        "rationale": "Fixture assertion; rationale not under test here.",
                    },
                ),
                requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
            )
        return _responder_property_closed_by_relation(role, schema, system, payload)

    try:
        run_discover_state(
            DiscoverInput(
                run_id="source-blind",
                natural_language="On pick the system shall reach Done.",
                stm_text=FIXTURE_MODEL,
                language="en-US",
                source_trace=SOURCE_TRACE,
            ),
            responder,
        )
    except RuntimeError:
        # Whether the run recovers depends on the rest of the fixture; what this
        # test owns is that the gate fired and said why.
        pass
    assert attempts["script"] >= 2, "the source-blind script was accepted"
    assert any("source-blind primary evidence" in text for text in payloads), (
        "the gate rejected the script but its reason never reached the producer"
    )


def test_a_qualified_call_is_still_recognised_as_the_predicate_it_names() -> None:
    """`env.occupancy_after(...)` is the same call with a prefix.

    Producers do write it that way.  Reading only bare names would leave the
    procedure gate seeing no predicate at all, and it would report "called nothing"
    for a script that called the right thing -- advice the producer cannot act on.
    """

    from paper_stm_feedback_loop.discover.capability import called_evidence_functions

    assert called_evidence_functions(
        'env.occupancy_after(source="Root.Idle", trigger="Root.go", target="Root.Busy")'
    ) == frozenset({"occupancy_after"})
    assert called_evidence_functions("occupancy_after()") == frozenset(
        {"occupancy_after"}
    )
    # Two of them, so the scan is exercised past the first qualified call.
    assert called_evidence_functions(
        'all([env.state_declared(state="Root.Idle", kind="leaf"), env.edge_declared()])'
    ) == frozenset({"all", "state_declared", "edge_declared"})
    assert called_evidence_functions("not python at all (") == frozenset()
    # A call whose callee is neither a name nor an attribute names no predicate.
    # It must yield nothing rather than raise: the procedure gate then reports
    # "called no predicate", which is the accurate and actionable message.
    assert called_evidence_functions("funcs[0]()") == frozenset()


def test_a_self_conjunction_and_a_cross_region_pair_are_not_vacuous() -> None:
    """Only two siblings of one region can never hold together.

    `active(A) && active(A)` is redundant but satisfiable, and two states in
    different regions can be active at once in a concurrent model.  Reporting
    either as vacuous would reject a query whose truth value does change when the
    defect is present.
    """

    from paper_stm_feedback_loop.discover.capability import (
        vacuous_sibling_conjunction,
    )

    assert vacuous_sibling_conjunction(
        'active("Root.R.A") && active("Root.R.B")'
    ) == ("Root.R.A", "Root.R.B")
    assert vacuous_sibling_conjunction('active("Root.R.A") && active("Root.R.A")') is None
    assert vacuous_sibling_conjunction('active("Alpha") && active("Beta")') is None
    assert vacuous_sibling_conjunction('active("Root.R.A")') is None
