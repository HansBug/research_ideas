"""Regression tests for deterministic typed-contract primary predicate routing."""

from __future__ import annotations

from pathlib import Path

from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.inputs import PairInput, load_pair, parse_fcstm
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import (
    CandidateIssue,
    ContractBindingHint,
    NLContract,
    bind_candidate,
)
from pipeline.evidence_discovery.semantics.predicate_routing import (
    route_primary_candidates,
)


PAPER_ROOT = Path(__file__).parents[3]
REPORT_ROOT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"

_CHOICE_SOURCE = """
def int x = 0;
state Root {
    state Disjoint;
    state B;
    state C;
    [*] -> Disjoint;
    Disjoint -> B : Choice + [x < 0];
    Disjoint -> C : Choice + [x >= 0];
}
"""

_LIFECYCLE_EFFECT_SOURCE = """
def int x = 0;
state Root {
    state A {
        enter abstract Start;
    }
    state B;
    [*] -> A;
    A -> B effect { x = 1; };
}
"""


def _hint(role: str, value: str) -> ContractBindingHint:
    """Build one source-side contract hint with complete audit rationale."""

    return ContractBindingHint(
        role=role,
        value=value,
        source_ref="NL1",
        reason="The fixture supplies one typed source-side argument.",
        basis="primary route regression fixture",
    )


def _candidate(contract: NLContract, refs: list[str]) -> CandidateIssue:
    """Build one exact predicate-null candidate preserving contract identity."""

    return CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Typed primary route fixture",
        requirement_quote=contract.quote,
        predicate_id=None,
        predicate_inputs={},
        element_refs=refs,
        source_refs=list(contract.source_refs),
        expected=contract.normative_statement,
        observed="The closed model is evaluated only after exact typed route closure.",
        strongest_rebuttal="An incomplete route must preserve this candidate as W1.",
        reason="The fixture preserves a precise semantic candidate before deterministic predicate routing.",
        basis="typed primary route regression fixture",
    )


def test_initial_entry_routes_to_owner_local_s2() -> None:
    """Initial-entry routing keeps owner scope distinct from target state."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0002")
    owner = next(item for item in pair.model.states if item.name == "PumpControl")
    target = next(item for item in pair.model.states if item.name == "PumpState")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-INITIAL-1",
        segment_id="NL1",
        quote="PumpControl must enter PumpState by its local default entry.",
        normative_statement="PumpControl must have an owner-local default entry to PumpState.",
        locus_kind="composite",
        locus_names=("PumpControl", "PumpState"),
        property="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        evidence_types=("source_identity", "closed_model_inventory", "initial_entry_fact"),
        binding_hints=(_hint("owner", owner.name), _hint("target", target.name)),
        scope="PumpControl local initial pseudostate",
        source_refs=("NL1",),
        reason="The requirement establishes a local default-entry obligation.",
        basis="NL1 fixture",
    )

    projection = route_primary_candidates(
        pair, {contract.contract_id: contract}, (), [_candidate(contract, [owner.ref, target.ref])]
    )

    routed = projection.candidates[0]
    assert routed.predicate_id == "S2"
    assert routed.predicate_inputs == {
        "source": "[*]",
        "target": target.canonical_path,
        "scope": owner.canonical_path,
    }
    telemetry = projection.telemetry[0]
    assert telemetry.applicable_predicates == ("S2",)
    assert telemetry.selected_predicate == "S2"
    assert telemetry.binding_complete is True


def test_deadlock_route_requires_one_reachable_state_scope() -> None:
    """V4 never receives an aggregate or unreachable deadlock carrier."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    state = next(item for item in pair.model.states if item.name == "PumpState")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-DEADLOCK-1",
        segment_id="NL2",
        quote="PumpState must continue operating.",
        normative_statement="PumpState must retain progress in the closed model.",
        locus_kind="state",
        locus_names=("PumpState",),
        property="deadlock_freedom",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("closed_model_inventory", "deadlock_frontier_fact"),
        binding_hints=(_hint("state", state.name),),
        scope="PumpState progress",
        source_refs=("NL2",),
        reason="The requirement establishes one state-local progress obligation.",
        basis="NL2 fixture",
    )

    projection = route_primary_candidates(
        pair, {contract.contract_id: contract}, (), [_candidate(contract, [state.ref])]
    )

    routed = projection.candidates[0]
    assert routed.predicate_id == "V4"
    assert routed.predicate_inputs == {"initial_scope": state.canonical_path}
    assert projection.telemetry[0].selected_predicate == "V4"


def test_state_action_without_legal_lifecycle_inputs_stays_predicate_null() -> None:
    """S4 must not coerce business wording into a lifecycle phase or action."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0024")
    state = next(item for item in pair.model.states if item.name == "Accelerating")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-ACTION-1",
        segment_id="NL1",
        quote="Accelerating performs an action while operating.",
        normative_statement="Accelerating must own the stated action in a lifecycle slot.",
        locus_kind="state",
        locus_names=("Accelerating",),
        property="state_action",
        expected_direction="must_occur",
        violation_direction="wrong_effect",
        evidence_types=("source_identity", "action_fact"),
        binding_hints=(_hint("state", state.name), _hint("phase", "operating")),
        scope="Accelerating lifecycle",
        source_refs=("NL1",),
        reason="The fixture intentionally lacks a legal FCSTM lifecycle phase/action closure.",
        basis="S4 strict phase regression fixture",
    )

    projection = route_primary_candidates(
        pair, {contract.contract_id: contract}, (), [_candidate(contract, [state.ref])]
    )

    assert projection.candidates[0].predicate_id is None
    telemetry = projection.telemetry[0]
    assert telemetry.selected_predicate is None
    assert telemetry.binding_complete is False
    assert "entry/do/exit" in telemetry.reason


def test_preselected_s4_is_rebuilt_or_downgraded_by_strict_primary_inputs() -> None:
    """An S4 label cannot bypass the lifecycle binder with state-name phases."""

    model = parse_fcstm(_LIFECYCLE_EFFECT_SOURCE)
    pair = PairInput(
        pair_id="fixture-lifecycle",
        pair_dir=Path("fixture-lifecycle"),
        nl_text="A enters with Start.",
        fcstm_text=_LIFECYCLE_EFFECT_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    state = next(item for item in model.states if item.name == "A")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-PRESELECTED-S4-1",
        segment_id="NL1",
        quote="A performs Start on entry.",
        normative_statement="A must own Start in its entry lifecycle slot.",
        locus_kind="state",
        locus_names=("A",),
        property="state_action",
        expected_direction="must_occur",
        violation_direction="wrong_effect",
        evidence_types=("source_identity", "action_fact"),
        binding_hints=(_hint("state", "A"), _hint("phase", "entry"), _hint("action", "Start")),
        scope="A lifecycle",
        source_refs=("NL1",),
        reason="The fixture supplies all three distinct S4 arguments.",
        basis="S4 strict preselection fixture",
    )
    selected = _candidate(contract, [state.ref]).model_copy(
        update={
            "predicate_id": "S4",
            "predicate_inputs": {"state": state.ref, "phase": "A", "action": "Start"},
        }
    )

    projection = route_primary_candidates(pair, {contract.contract_id: contract}, (), [selected])

    assert projection.candidates[0].predicate_id == "S4"
    assert projection.candidates[0].predicate_inputs == {
        "state": state.canonical_path,
        "phase": "entry",
        "action": "Start",
    }

    invalid_contract = contract.model_copy(
        update={
            "binding_hints": (_hint("state", "A"), _hint("phase", "operating"), _hint("action", "Start")),
        }
    )
    invalid_projection = route_primary_candidates(
        pair, {invalid_contract.contract_id: invalid_contract}, (), [selected]
    )
    assert invalid_projection.candidates[0].predicate_id is None
    assert invalid_projection.candidates[0].predicate_inputs == {}
    assert "strict primary rebinding" in invalid_projection.candidates[0].reason


def test_preselected_s6_requires_a_native_effect_operation() -> None:
    """A natural-language action phrase cannot be executed as an S6 effect."""

    model = parse_fcstm(_LIFECYCLE_EFFECT_SOURCE)
    pair = PairInput(
        pair_id="fixture-effect",
        pair_dir=Path("fixture-effect"),
        nl_text="A to B sends the Stop signal.",
        fcstm_text=_LIFECYCLE_EFFECT_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    transition = next(item for item in model.transitions if item.source == "A" and item.target == "B")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-PRESELECTED-S6-1",
        segment_id="NL1",
        quote="A to B performs timer stops.",
        normative_statement="The exact A-to-B transition must contain the timer stops effect.",
        locus_kind="transition",
        locus_names=("A", "B"),
        property="effect",
        expected_direction="must_occur",
        violation_direction="wrong_effect",
        evidence_types=("source_identity", "effect_fact"),
        binding_hints=(_hint("transition", transition.ref), _hint("effect", "timer stops")),
        scope="A-to-B transition",
        source_refs=("NL1",),
        reason="The fixture deliberately supplies prose rather than an FCSTM operation.",
        basis="S6 strict preselection fixture",
    )
    selected = _candidate(contract, [transition.ref]).model_copy(
        update={
            "predicate_id": "S6",
            "predicate_inputs": {"transition": transition.ref, "effect": "timer stops"},
        }
    )

    projection = route_primary_candidates(pair, {contract.contract_id: contract}, (), [selected])

    assert projection.candidates[0].predicate_id is None
    assert projection.candidates[0].predicate_inputs == {}
    assert "native FCSTM operation" in projection.telemetry[0].reason


def test_event_consumption_routes_to_a_native_cold_runtime_scenario() -> None:
    """R1 primary routing requires a unique FCSTM cold-start macrostep."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0010")
    transition = next(
        item for item in pair.model.transitions if item.triggers == ("Power_On",)
    )
    event = next(item for item in pair.model.events if item.name == "Power_On")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-R1-1",
        segment_id="NL1",
        quote="Power_On must be consumed by the selected macrostep.",
        normative_statement="The exact Power_On event must be consumed in the declared transition macrostep.",
        locus_kind="scenario",
        locus_names=(transition.source, event.name),
        property="event_consumption",
        expected_direction="must_occur",
        violation_direction="unconsumed",
        evidence_types=("source_identity", "transition_fact", "trigger_fact", "trace_fact"),
        binding_hints=(_hint("event", event.name),),
        scope="unique cold-start event consumption",
        source_refs=("NL1",),
        reason="The fixture supplies one exact event-consumption obligation.",
        basis="R1 native route regression fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [_candidate(contract, [transition.ref, event.ref])],
    )

    routed = projection.candidates[0]
    assert routed.predicate_id == "R1"
    assert routed.predicate_inputs["event"] == event.canonical_path
    assert routed.predicate_inputs["scenario"]["selected_transition_ref"] == transition.ref
    assert projection.telemetry[0].selected_predicate == "R1"


def test_state_retention_distinguishes_generic_window_from_runtime_control() -> None:
    """Generic temporal prose cannot block a separately closed native fragment."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    root = next(item for item in pair.model.states if item.parent is None)
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-R4-1",
        segment_id="NL1",
        quote="At cold start the root remains active for two macrosteps.",
        normative_statement="The root state must remain active during the explicit cold-start window.",
        locus_kind="state",
        locus_names=(root.name,),
        property="state_retention",
        expected_direction="must_remain",
        violation_direction="not_retained",
        evidence_types=("source_identity", "trace_fact"),
        binding_hints=(
            _hint("state", root.name),
            _hint("scenario", "cold"),
            _hint("window", "cold_macrosteps=2"),
        ),
        scope="cold-start bounded retention",
        source_refs=("NL1",),
        reason="The fixture explicitly declares the only admissible runtime window.",
        basis="R4 native route regression fixture",
    )

    projection = route_primary_candidates(
        pair, {contract.contract_id: contract}, (), [_candidate(contract, [root.ref])]
    )

    routed = projection.candidates[0]
    assert routed.predicate_id == "R4"
    assert routed.predicate_inputs["interval"] == [0, 1]
    assert routed.predicate_inputs["scenario"]["event_queue"] == []

    generic_window_contract = contract.model_copy(
        update={
            "binding_hints": (_hint("state", root.name), _hint("window", "while ready")),
        }
    )
    generic_window_projection = route_primary_candidates(
        pair,
        {generic_window_contract.contract_id: generic_window_contract},
        (),
        [_candidate(generic_window_contract, [root.ref])],
    )
    generic_window_route = generic_window_projection.candidates[0]
    assert generic_window_route.predicate_id == "R4"
    assert generic_window_route.predicate_inputs["scenario"]["event_queue"] == []
    assert "native cold-entry" in generic_window_route.predicate_inputs["scenario"]["reason"]

    incomplete_control_contract = contract.model_copy(
        update={
            "binding_hints": (
                _hint("state", root.name),
                _hint("scenario", "cold"),
                _hint("window", "while ready"),
            ),
        }
    )
    incomplete_control_projection = route_primary_candidates(
        pair,
        {incomplete_control_contract.contract_id: incomplete_control_contract},
        (),
        [_candidate(incomplete_control_contract, [root.ref])],
    )
    assert incomplete_control_projection.candidates[0].predicate_id is None
    assert "input_contract_missing/out_of_fragment" in incomplete_control_projection.telemetry[0].basis


def test_state_retention_closes_unique_native_cold_entry_quiescence() -> None:
    """R4 builds and replays only one unique native cold-entry retention path."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0024")
    state = next(item for item in pair.model.states if item.name == "Approaching")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-R4-NATIVE-ENTRY-1",
        segment_id="NL10",
        quote="Approaching remains active until the train is ready to stop or decelerate.",
        normative_statement="Approaching must be retained before a later stop/deceleration input.",
        locus_kind="state",
        locus_names=("Approaching",),
        property="state_retention",
        expected_direction="must_remain",
        violation_direction="not_retained",
        evidence_types=("source_identity", "trace_fact"),
        binding_hints=(_hint("state", "Approaching"),),
        scope="Approaching retention",
        source_refs=("NL10",),
        reason="The requirement establishes state retention before a later input.",
        basis="R4 native cold-entry regression fixture",
    )

    projection = route_primary_candidates(
        pair, {contract.contract_id: contract}, (), [_candidate(contract, [state.ref])]
    )
    routed = projection.candidates[0]
    assert routed.predicate_id == "R4"
    scenario = routed.predicate_inputs["scenario"]
    assert scenario["event_queue"] == [
        "llms_emp_feedback_final_0024.Closed_SendDeparted",
        "llms_emp_feedback_final_0024.Approached_Decelerate",
    ]
    assert scenario["schedule"][-1]["event_paths"] == []
    assert routed.predicate_inputs["interval"] == [2, 3]

    binding = bind_candidate(routed, pair.model)
    plan = compile_plan(
        routed,
        binding,
        load_registry(),
        obligation_id="fixture:r4-native-entry",
        round_index=1,
        model=pair.model,
    )
    receipt = run_backend(plan, pair.model, "fixture:r4-native-entry:receipt")
    assert receipt.terminal_state == "completed"
    assert receipt.verdict == "true"
    assert len(receipt.trace) == 4


def test_guard_disjointness_requires_native_group_and_independent_domain() -> None:
    """V1 reads guards from native FCSTM and rejects a missing source domain."""

    model = parse_fcstm(_CHOICE_SOURCE)
    pair = PairInput(
        pair_id="fixture-choice",
        pair_dir=Path("fixture-choice"),
        nl_text="The Choice alternatives must be disjoint over the declared x domain.",
        fcstm_text=_CHOICE_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    source = next(item for item in model.states if item.name == "Disjoint")
    rows = [item for item in model.transitions if item.source == "Disjoint"]
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-V1-1",
        segment_id="NL1",
        quote="Choice alternatives must be disjoint for x in {-1, 0, 1}.",
        normative_statement="The exact Choice guard alternatives must be pairwise disjoint over the declared finite x domain.",
        locus_kind="transition",
        locus_names=("Disjoint", "B", "C"),
        property="guard_disjointness",
        expected_direction="must_equal",
        violation_direction="wrong_guard",
        evidence_types=("source_identity", "guard_fact", "smt_fact"),
        binding_hints=(
            _hint("source", "Disjoint"),
            _hint("event", "Choice"),
            _hint("domain", '{"x":{"values":[-1,0,1]}}'),
        ),
        scope="Disjoint Choice group",
        source_refs=("NL1",),
        reason="The fixture declares both the exact choice group and an independent finite domain.",
        basis="V1 native route regression fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [_candidate(contract, [source.ref, *(row.ref for row in rows)])],
    )

    routed = projection.candidates[0]
    assert routed.predicate_id == "V1"
    assert routed.predicate_inputs["domain"] == {"x": {"values": [-1, 0, 1]}}
    assert routed.predicate_inputs["guards"] == ["x < 0", "x >= 0"]

    domainless_contract = contract.model_copy(
        update={"binding_hints": (_hint("source", "Disjoint"), _hint("event", "Choice"))}
    )
    domainless_projection = route_primary_candidates(
        pair,
        {domainless_contract.contract_id: domainless_contract},
        (),
        [_candidate(domainless_contract, [source.ref, *(row.ref for row in rows)])],
    )
    assert domainless_projection.candidates[0].predicate_id is None
    assert "finite domain" in domainless_projection.telemetry[0].basis
