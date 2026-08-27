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
from pipeline.evidence_discovery.structural_rebind_replay import (
    STRUCTURAL_PREDICATES,
    _saved_selected_structural_contract,
    _summary as structural_rebind_summary,
)
from pipeline.evidence_discovery.route_replay import merge_saved_frontier_contracts

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

_RUNTIME_SOURCE = """
state Root {
    state A;
    state B;
    state C;
    [*] -> A;
    A -> B : Go;
}
"""

_EVENT_SELECTOR_SOURCE = """
state Root {
    event ModeShift;
    state A;
    state B;
    state C;
    [*] -> A;
    A -> B : ModeShift;
    A -> C : ModeShift;
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


def test_preselected_s2_rebuilds_legacy_projection_refs_before_native_execution() -> None:
    """An already-labelled S2 cannot send audit refs to the native backend."""

    model = parse_fcstm(_RUNTIME_SOURCE)
    pair = PairInput(
        pair_id="fixture-s2-native-rebind",
        pair_dir=Path("fixture-s2-native-rebind"),
        nl_text="A must transition to B.",
        fcstm_text=_RUNTIME_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    root = model.state("Root")
    source = model.state("A")
    target = model.state("B")
    assert root is not None and source is not None and target is not None
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-PRESELECTED-S2-1",
        segment_id="NL1",
        quote="A must transition to B.",
        normative_statement="A transition from A to B must exist.",
        locus_kind="transition",
        locus_names=("A", "B"),
        property="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "transition_fact"),
        binding_hints=(_hint("source", "A"), _hint("target", "B")),
        scope="A-to-B transition",
        source_refs=("NL1",),
        reason="The fixture supplies one exact endpoint obligation.",
        basis="S2 native rebinding regression fixture",
    )
    selected = _candidate(contract, [source.ref, target.ref]).model_copy(
        update={
            "predicate_id": "S2",
            "predicate_inputs": {
                "source": source.ref,
                "target": target.ref,
                "scope": root.ref,
            },
        }
    )

    projection = route_primary_candidates(pair, {contract.contract_id: contract}, (), [selected])
    routed = projection.candidates[0]
    assert routed.predicate_id == "S2"
    assert routed.predicate_inputs == {
        "source": source.canonical_path,
        "target": target.canonical_path,
        "scope": root.canonical_path,
    }

    binding = bind_candidate(routed, pair.model)
    plan = compile_plan(
        routed,
        binding,
        load_registry(),
        obligation_id="fixture:s2:native-rebind",
        round_index=1,
        model=pair.model,
    )
    receipt = run_backend(plan, pair.model, "fixture:s2:native-rebind:receipt")
    assert receipt.terminal_state == "completed"
    assert receipt.verdict == "true"


def test_native_event_selector_cannot_be_rebound_as_guard_predicate() -> None:
    """Native events remain event/trigger inputs rather than guard AST inputs."""

    model = parse_fcstm(_EVENT_SELECTOR_SOURCE)
    pair = PairInput(
        pair_id="fixture-event-selector-role",
        pair_dir=Path("fixture-event-selector-role"),
        nl_text="ModeShift selects two alternatives.",
        fcstm_text=_EVENT_SELECTOR_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    source = model.state("A")
    first = next(
        item for item in model.transitions if item.source == "A" and item.target == "B"
    )
    second = next(
        item for item in model.transitions if item.source == "A" and item.target == "C"
    )
    assert source is not None

    guard_contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-EVENT-AS-GUARD-1",
        segment_id="NL1",
        quote="ModeShift selects the A-to-B alternative.",
        normative_statement="The A-to-B transition must use ModeShift as a guard.",
        locus_kind="transition",
        locus_names=("A", "B"),
        property="guard",
        expected_direction="must_equal",
        violation_direction="wrong_guard",
        evidence_types=("source_identity", "guard_fact"),
        binding_hints=(
            _hint("source", "A"),
            _hint("target", "B"),
            _hint("transition", first.ref),
            _hint("guard", "ModeShift"),
        ),
        scope="A-to-B selector",
        source_refs=("NL1",),
        reason="The fixture deliberately assigns a declared FCSTM event the wrong guard role.",
        basis="native Event-versus-guard routing regression fixture",
    )
    guard_candidate = _candidate(guard_contract, [source.ref, first.ref]).model_copy(
        update={"predicate_id": "S5", "predicate_inputs": {"transition": first.ref, "guard": "ModeShift"}}
    )

    guard_projection = route_primary_candidates(
        pair, {guard_contract.contract_id: guard_contract}, (), [guard_candidate]
    )
    assert guard_projection.candidates[0].predicate_id is None
    assert guard_projection.candidates[0].predicate_inputs == {}
    assert "native FCSTM Event" in guard_projection.telemetry[0].reason

    choice_contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-EVENT-AS-V1-GUARD-1",
        segment_id="NL1",
        quote="ModeShift keeps A's alternatives distinct.",
        normative_statement="The A alternatives must have disjoint ModeShift guards.",
        locus_kind="transition",
        locus_names=("A", "B", "C"),
        property="guard_disjointness",
        expected_direction="must_remain",
        violation_direction="wrong_guard",
        evidence_types=("source_identity", "guard_fact"),
        binding_hints=(
            _hint("source", "A"),
            _hint("guard", "ModeShift"),
            _hint("domain", '{"x": [0]}'),
        ),
        scope="A selector group",
        source_refs=("NL1",),
        reason="The fixture keeps an event selector out of V1 guard-domain inputs.",
        basis="native Event-versus-V1 routing regression fixture",
    )
    choice_candidate = _candidate(choice_contract, [source.ref, first.ref, second.ref])

    choice_projection = route_primary_candidates(
        pair, {choice_contract.contract_id: choice_contract}, (), [choice_candidate]
    )
    assert choice_projection.candidates[0].predicate_id is None
    assert "native FCSTM Events" in choice_projection.telemetry[0].reason


def test_candidate_route_telemetry_never_inherits_sibling_contract_route() -> None:
    """A contract-level S3 success cannot close a sibling's two-carrier claim."""

    model = parse_fcstm(_EVENT_SELECTOR_SOURCE)
    pair = PairInput(
        pair_id="fixture-candidate-route-telemetry",
        pair_dir=Path("fixture-candidate-route-telemetry"),
        nl_text="The A-to-B transition must use ModeShift.",
        fcstm_text=_EVENT_SELECTOR_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    first = next(
        item for item in model.transitions if item.source == "A" and item.target == "B"
    )
    second = next(
        item for item in model.transitions if item.source == "A" and item.target == "C"
    )
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-CANDIDATE-TELEMETRY-1",
        segment_id="NL1",
        quote="The A-to-B transition must use ModeShift.",
        normative_statement="The exact A-to-B transition must have the ModeShift trigger set.",
        locus_kind="transition",
        locus_names=("A", "B"),
        property="trigger_set",
        expected_direction="must_equal",
        violation_direction="mismatched",
        evidence_types=("source_identity", "trigger_fact"),
        binding_hints=(_hint("trigger", "ModeShift"),),
        scope="A-to-B exact transition",
        source_refs=("NL1",),
        reason="The fixture declares one exact transition trigger obligation.",
        basis="candidate-level route telemetry regression fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [
            _candidate(contract, [first.ref, second.ref]),
            _candidate(contract, [first.ref]),
        ],
    )

    assert projection.candidates[0].predicate_id is None
    assert projection.candidates[1].predicate_id == "S3"
    assert projection.telemetry[0].selected_predicate == "S3"
    assert projection.candidate_telemetry[0].candidate_index == 0
    assert projection.candidate_telemetry[0].selected_predicate is None
    assert projection.candidate_telemetry[1].candidate_index == 1
    assert projection.candidate_telemetry[1].selected_predicate == "S3"


def test_preselected_s5_rebuilds_legacy_guard_field_before_native_execution() -> None:
    """A selected S5 uses the contract guard and exact native carrier only."""

    model = parse_fcstm(_CHOICE_SOURCE)
    pair = PairInput(
        pair_id="fixture-s5-native-rebind",
        pair_dir=Path("fixture-s5-native-rebind"),
        nl_text="Disjoint to B uses x < 0.",
        fcstm_text=_CHOICE_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    source = model.state("Disjoint")
    target = model.state("B")
    transition = next(
        item for item in model.transitions if item.source == "Disjoint" and item.target == "B"
    )
    assert source is not None and target is not None
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-PRESELECTED-S5-1",
        segment_id="NL1",
        quote="Disjoint to B uses x < 0.",
        normative_statement="The Disjoint-to-B transition must use guard x < 0.",
        locus_kind="transition",
        locus_names=("Disjoint", "B"),
        property="guard",
        expected_direction="must_equal",
        violation_direction="wrong_guard",
        evidence_types=("source_identity", "guard_fact"),
        binding_hints=(
            _hint("source", "Disjoint"),
            _hint("target", "B"),
            _hint("transition", transition.ref),
            _hint("guard", "x < 0"),
        ),
        scope="Disjoint-to-B transition",
        source_refs=("NL1",),
        reason="The fixture supplies one exact guard carrier and expression.",
        basis="S5 native rebinding regression fixture",
    )
    selected = _candidate(contract, [source.ref, target.ref, transition.ref]).model_copy(
        update={
            "predicate_id": "S5",
            "predicate_inputs": {
                "transition": transition.ref,
                "expected_guard": "x < 0",
            },
        }
    )

    projection = route_primary_candidates(pair, {contract.contract_id: contract}, (), [selected])
    routed = projection.candidates[0]
    assert routed.predicate_id == "S5"
    assert routed.predicate_inputs == {"transition": transition.ref, "guard": "x < 0"}

    binding = bind_candidate(routed, pair.model)
    plan = compile_plan(
        routed,
        binding,
        load_registry(),
        obligation_id="fixture:s5:native-rebind",
        round_index=1,
        model=pair.model,
    )
    receipt = run_backend(plan, pair.model, "fixture:s5:native-rebind:receipt")
    assert receipt.terminal_state == "completed"
    assert receipt.verdict == "true"


def test_structural_rebind_summary_rejects_unclosed_w2() -> None:
    """The isolated selected-candidate audit retains the W failure boundary."""

    record = {
        "pair_id": "0000",
        "baseline_predicate_id": "S2",
        "baseline_candidate": {"predicate_inputs": {"source": "A"}},
        "baseline_receipt": {"verdict": "false"},
        "route_status": "route_unclosed",
        "candidate": {"predicate_id": None, "predicate_inputs": {}},
        "receipt": None,
        "witness_level": "W2",
        "audit_bundle": {},
    }

    summary = structural_rebind_summary("a" * 32, "b" * 32, [record])
    assert STRUCTURAL_PREDICATES == frozenset({"S2", "S3", "S4", "S5", "S6"})
    assert summary["acceptance"]["no_unclosed_or_failed_row_claims_w2"] is False


def test_structural_rebind_reconstructs_saved_selected_probe_contract() -> None:
    """A post-primary S3 probe must not inherit a null primary route row."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0001")
    transition = next(item for item in pair.model.transitions if item.triggers)
    trigger = transition.triggers[0]
    contract = NLContract(
        contract_id="NL-CONTRACT-REPLAY-SAVED-S3-PROBE-1",
        segment_id="NL1",
        quote="The selected transition must retain its exact trigger.",
        normative_statement="The selected transition must use the declared trigger.",
        locus_kind="transition",
        locus_names=(transition.source, transition.target),
        property="trigger_set",
        expected_direction="must_equal",
        violation_direction="mismatched",
        evidence_types=("source_identity", "transition_fact", "trigger_fact"),
        binding_hints=(
            _hint("transition", transition.ref),
            _hint("event", trigger),
        ),
        scope="saved deterministic probe",
        source_refs=("NL1",),
        reason="The fixture records a post-primary selected structural probe.",
        basis="saved selected probe reconstruction regression fixture",
    )
    selected_probe = _candidate(contract, [transition.ref]).model_copy(
        update={
            "predicate_id": "S3",
            "predicate_inputs": {
                "transition": transition.ref,
                "triggers": [trigger],
            },
        }
    )

    reconstructed = _saved_selected_structural_contract(selected_probe)

    assert reconstructed is not None
    assert reconstructed.contract_id == selected_probe.contract_id
    assert reconstructed.segment_id == "NL1"
    assert reconstructed.expected_direction == "must_equal"
    assert [item.value for item in reconstructed.binding_hints if item.role == "event"] == [
        trigger
    ]
    assert {item.source_ref for item in reconstructed.binding_hints} == {"NL1"}
    projection = route_primary_candidates(
        pair,
        {reconstructed.contract_id: reconstructed},
        (),
        [selected_probe],
    )
    assert projection.candidates[0].predicate_id == "S3"
    assert projection.candidate_telemetry[0].selected_predicate == "S3"


def test_structural_rebind_rejects_ambiguous_saved_probe_segment() -> None:
    """A cross-segment saved probe cannot receive an invented replay segment."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0001")
    transition = next(item for item in pair.model.transitions if item.triggers)
    selected_probe = _candidate(
        NLContract(
            contract_id="NL-CONTRACT-NL1-NL2-REPLAY-SAVED-S3-PROBE-1",
            segment_id="NL1",
            quote="The selected transition must retain its exact trigger.",
            normative_statement="The selected transition must use the declared trigger.",
            locus_kind="transition",
            locus_names=(transition.source, transition.target),
            property="trigger_set",
            expected_direction="must_equal",
            violation_direction="mismatched",
            evidence_types=("source_identity", "transition_fact", "trigger_fact"),
            binding_hints=(
                _hint("transition", transition.ref),
                _hint("event", transition.triggers[0]),
            ),
            scope="cross-segment saved deterministic probe",
            source_refs=("NL1", "NL2"),
            reason="The fixture deliberately retains two source segments.",
            basis="ambiguous saved structural probe reconstruction regression fixture",
        ),
        [transition.ref],
    ).model_copy(
        update={
            "predicate_id": "S3",
            "predicate_inputs": {
                "transition": transition.ref,
                "triggers": [transition.triggers[0]],
            },
        }
    )

    assert _saved_selected_structural_contract(selected_probe) is None


def test_structural_rebind_preserves_initial_entry_direction() -> None:
    """Saved S2 initial-entry probes retain must_enter rather than must_exist."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0001")
    owner = pair.model.states[0]
    target = pair.model.states[1]
    selected_probe = _candidate(
        NLContract(
            contract_id="NL-CONTRACT-NL7-REPLAY-SAVED-INITIAL-1",
            segment_id="NL7",
            quote="The owner must enter the named state through its local initial edge.",
            normative_statement="The owner has one initial entry to the named state.",
            locus_kind="composite",
            locus_names=(owner.name, target.name),
            property="initial_entry",
            expected_direction="must_enter",
            violation_direction="missing",
            evidence_types=("source_identity", "initial_entry_fact"),
            binding_hints=(_hint("owner", owner.name), _hint("target", target.name)),
            scope="saved initial-entry deterministic probe",
            source_refs=("NL7",),
            reason="The fixture records one selected local initial-entry probe.",
            basis="saved initial-entry reconstruction regression fixture",
        ),
        [owner.ref, target.ref],
    ).model_copy(
        update={
            "predicate_id": "S2",
            "predicate_inputs": {"scope": owner.ref, "target": target.ref},
        }
    )

    reconstructed = _saved_selected_structural_contract(selected_probe)

    assert reconstructed is not None
    assert reconstructed.segment_id == "NL7"
    assert reconstructed.expected_direction == "must_enter"


def test_structural_rebind_replay_merges_saved_derived_frontier_contract() -> None:
    """Derived contracts are replay inputs, not absent-contract guesses."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0002")
    state = next(item for item in pair.model.states if item.name == "PumpState")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-SAVED-FRONTIER-1",
        segment_id="NL1",
        quote="PumpState must progress.",
        normative_statement="PumpState must retain progress.",
        locus_kind="state",
        locus_names=("PumpState",),
        property="deadlock_freedom",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("source_identity", "deadlock_frontier_fact"),
        binding_hints=(_hint("state", state.name),),
        scope="PumpState progress",
        source_refs=("NL1",),
        reason="The fixture defines one derived frontier obligation.",
        basis="saved frontier contract regression fixture",
    )
    candidate = _candidate(contract, [state.ref])
    cell = {
        "stage_outputs": {
            "execute_batch": {
                "frontier_batch": {
                    "obligations": [
                        {
                                "frontier_id": "fixture-frontier-1",
                                "kind": "reachable_dead_end",
                                "contract": contract.model_dump(mode="json"),
                                "candidate": candidate.model_dump(mode="json"),
                                "source_contract_ids": [contract.contract_id],
                            "reason": "The fixture persists a derived contract.",
                            "basis": "provider-free saved frontier fixture",
                        }
                    ],
                    "reason": "Saved fixture frontier.",
                    "basis": "saved frontier fixture",
                }
            }
        }
    }
    contracts: dict[str, NLContract] = {}

    exclusions = merge_saved_frontier_contracts(cell, contracts)

    assert contracts == {contract.contract_id: contract}
    assert exclusions == {}


def test_structural_rebind_replay_excludes_retired_frontier_kind_with_accounting() -> None:
    """Historical retired frontier rows cannot reopen the current production schema."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0002")
    state = next(item for item in pair.model.states if item.name == "PumpState")
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-RETIRED-FRONTIER-1",
        segment_id="NL1",
        quote="PumpState must progress.",
        normative_statement="PumpState must retain progress.",
        locus_kind="state",
        locus_names=("PumpState",),
        property="deadlock_freedom",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("source_identity", "deadlock_frontier_fact"),
        binding_hints=(_hint("state", state.name),),
        scope="PumpState progress",
        source_refs=("NL1",),
        reason="The fixture isolates one retired saved frontier row.",
        basis="historical frontier compatibility regression fixture",
    )
    candidate = _candidate(contract, [state.ref])
    live_row = {
        "frontier_id": "fixture-frontier-live",
        "kind": "reachable_dead_end",
        "contract": contract.model_dump(mode="json"),
        "candidate": candidate.model_dump(mode="json"),
        "source_contract_ids": [contract.contract_id],
        "reason": "A live saved frontier contract remains available.",
        "basis": "provider-free saved frontier fixture",
    }
    retired_row = {**live_row, "frontier_id": "fixture-frontier-retired", "kind": "wrong_scope_route"}
    cell = {
        "stage_outputs": {
            "execute_batch": {
                "frontier_batch": {
                    "obligations": [live_row, retired_row],
                    "checks": [retired_row],
                    "reason": "Saved fixture with one retired frontier kind.",
                    "basis": "historical frontier compatibility fixture",
                }
            }
        }
    }
    contracts: dict[str, NLContract] = {}

    exclusions = merge_saved_frontier_contracts(cell, contracts)

    assert contracts == {contract.contract_id: contract}
    assert exclusions == {"wrong_scope_route": 2}


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


def test_universal_reachability_routes_only_from_one_native_leaf() -> None:
    """G2 maps a composite only through one unique native initial descent."""

    model = parse_fcstm(_RUNTIME_SOURCE)
    pair = PairInput(
        pair_id="fixture-g2",
        pair_dir=Path("fixture-g2"),
        nl_text="Every execution from A must reach B.",
        fcstm_text=_RUNTIME_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    source = model.state("A")
    target = model.state("B")
    assert source is not None and target is not None
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-G2-1",
        segment_id="NL1",
        quote="Every execution from A must reach B.",
        normative_statement="Every bounded execution from exact state A must reach exact state B.",
        locus_kind="state",
        locus_names=("A", "B"),
        property="universal_reachability",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("source_identity", "closed_model_inventory", "reachability_fact"),
        binding_hints=(_hint("source", "A"), _hint("target", "B")),
        scope="A to B bounded execution",
        source_refs=("NL1",),
        reason="The requirement supplies exact universal-reachability endpoints.",
        basis="G2 native leaf route fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [_candidate(contract, [source.ref, target.ref])],
    )
    routed = projection.candidates[0]
    assert routed.predicate_id == "G2"
    assert routed.predicate_inputs == {
        "source": source.canonical_path,
        "target": target.canonical_path,
    }

    root = next(state for state in model.states if state.parent is None)
    composite_contract = contract.model_copy(
        update={
            "contract_id": "NL-CONTRACT-ROUTE-G2-COMPOSITE-1",
            "property": "termination",
            "binding_hints": (_hint("source", root.canonical_path), _hint("target", "B")),
        }
    )
    composite_projection = route_primary_candidates(
        pair,
        {composite_contract.contract_id: composite_contract},
        (),
        [_candidate(composite_contract, [root.ref, target.ref])],
    )
    composite = composite_projection.candidates[0]
    assert composite.predicate_id == "G2"
    assert composite.predicate_inputs == {
        "source": source.canonical_path,
        "target": target.canonical_path,
    }
    assert "State.init_transitions" in composite.basis


def test_g2_rejects_non_unique_native_initial_descent() -> None:
    source_text = """
state Root {
    state A;
    state B;
    [*] -> A;
    [*] -> B;
}
"""
    model = parse_fcstm(source_text)
    pair = PairInput(
        pair_id="fixture-g2-ambiguous-initial",
        pair_dir=Path("fixture-g2-ambiguous-initial"),
        nl_text="Every execution from Root must reach B.",
        fcstm_text=source_text,
        plantuml_text="",
        model=model,
        hashes={},
    )
    root = model.state("Root")
    target = model.state("B")
    assert root is not None and target is not None
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-G2-AMBIGUOUS-1",
        segment_id="NL1",
        quote="Every execution from Root must reach B.",
        normative_statement="Every bounded execution from Root must reach B.",
        locus_kind="state",
        locus_names=("Root", "B"),
        property="universal_reachability",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("source_identity", "reachability_fact"),
        binding_hints=(_hint("source", "Root"), _hint("target", "B")),
        scope="Root bounded execution",
        source_refs=("NL1",),
        reason="The fixture supplies exact universal-reachability endpoints.",
        basis="G2 ambiguous native initial-descent regression fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [_candidate(contract, [root.ref, target.ref])],
    )

    assert projection.candidates[0].predicate_id is None
    assert "2 initial transitions" in projection.telemetry[0].basis


def test_route_avoidance_requires_three_exact_native_leaf_states() -> None:
    """G3 binds source, target, and forbidden identities without text topology."""

    model = parse_fcstm(_RUNTIME_SOURCE)
    pair = PairInput(
        pair_id="fixture-g3",
        pair_dir=Path("fixture-g3"),
        nl_text="A to B routes must avoid C.",
        fcstm_text=_RUNTIME_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    source = model.state("A")
    target = model.state("B")
    forbidden = model.state("C")
    assert source is not None and target is not None and forbidden is not None
    contract = NLContract(
        contract_id="NL-CONTRACT-ROUTE-G3-1",
        segment_id="NL1",
        quote="A to B routes must avoid C.",
        normative_statement="Every A-to-B route must avoid exact state C.",
        locus_kind="state",
        locus_names=("A", "B", "C"),
        property="route_avoidance",
        expected_direction="must_avoid",
        violation_direction="other",
        evidence_types=("source_identity", "closed_model_inventory", "reachability_fact"),
        binding_hints=(
            _hint("source", "A"),
            _hint("target", "B"),
            _hint("forbidden", "C"),
        ),
        scope="A to B route",
        source_refs=("NL1",),
        reason="The requirement supplies all three route-avoidance carriers.",
        basis="G3 native leaf route fixture",
    )

    projection = route_primary_candidates(
        pair,
        {contract.contract_id: contract},
        (),
        [_candidate(contract, [source.ref, target.ref, forbidden.ref])],
    )
    routed = projection.candidates[0]
    assert routed.predicate_id == "G3"
    assert routed.predicate_inputs == {
        "source": source.canonical_path,
        "target": target.canonical_path,
        "forbidden": [forbidden.canonical_path],
    }


def test_state_after_stimulus_uses_target_independent_native_scenario() -> None:
    """R2 scenario selection uses stimulus consumption, then backend checks target."""

    model = parse_fcstm(_RUNTIME_SOURCE)
    pair = PairInput(
        pair_id="fixture-r2",
        pair_dir=Path("fixture-r2"),
        nl_text="After Go the system must be in B.",
        fcstm_text=_RUNTIME_SOURCE,
        plantuml_text="",
        model=model,
        hashes={},
    )
    event = model.event("Go")
    target_b = model.state("B")
    target_c = model.state("C")
    assert event is not None and target_b is not None and target_c is not None

    def contract_for(target_name: str, suffix: str) -> NLContract:
        return NLContract(
            contract_id=f"NL-CONTRACT-ROUTE-R2-{suffix}",
            segment_id="NL1",
            quote=f"After Go the system must be in {target_name}.",
            normative_statement=f"The exact Go stimulus must leave the system in {target_name}.",
            locus_kind="scenario",
            locus_names=("Go", target_name),
            property="state_after_stimulus",
            expected_direction="must_reach",
            violation_direction="wrong_target",
            evidence_types=("source_identity", "trace_fact"),
            binding_hints=(_hint("event", "Go"), _hint("target", target_name)),
            scope="cold native stimulus scenario",
            source_refs=("NL1",),
            reason="The requirement supplies one exact event and post-stimulus target.",
            basis="R2 target-independent native scenario fixture",
        )

    contract_b = contract_for("B", "TRUE-1")
    contract_c = contract_for("C", "FALSE-1")
    routed_candidates = []
    for contract, target in ((contract_b, target_b), (contract_c, target_c)):
        projection = route_primary_candidates(
            pair,
            {contract.contract_id: contract},
            (),
            [_candidate(contract, [event.ref, target.ref])],
        )
        routed = projection.candidates[0]
        assert routed.predicate_id == "R2"
        routed_candidates.append(routed)

    assert routed_candidates[0].predicate_inputs["scenario"] == routed_candidates[1].predicate_inputs["scenario"]
    assert "independent" in routed_candidates[0].predicate_inputs["scenario"]["reason"]

    verdicts = []
    for index, routed in enumerate(routed_candidates, start=1):
        binding = bind_candidate(routed, pair.model)
        plan = compile_plan(
            routed,
            binding,
            load_registry(),
            obligation_id=f"fixture:r2:{index}",
            round_index=1,
            model=pair.model,
        )
        receipt = run_backend(plan, pair.model, f"fixture:r2:{index}:receipt")
        assert receipt.terminal_state == "completed"
        verdicts.append(receipt.verdict)
    assert verdicts == ["true", "false"]


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
