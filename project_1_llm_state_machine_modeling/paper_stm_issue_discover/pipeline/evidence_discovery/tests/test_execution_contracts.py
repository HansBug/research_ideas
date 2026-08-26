from __future__ import annotations

import asyncio
import hashlib
import json
from datetime import date
from importlib import import_module
from pathlib import Path
from types import SimpleNamespace

import pytest
from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.backends.bounded_verification import (
    _terminal_states,
    run_bounded_verification,
)
from pipeline.evidence_discovery.backends.topology import _graph, run_topology
from pipeline.evidence_discovery.backends.trajectory import run_trajectory
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.compiler.inputs import (
    UnsupportedPredicateInputs,
    validate_predicate_inputs,
)
from pipeline.evidence_discovery.compiler.lowering import PredicatePlan
from pipeline.evidence_discovery.evidence.audit_bundle import (
    W2AuditBundle,
    validate_and_hash_w2_audit_bundle,
)
from pipeline.evidence_discovery.evidence.receipts import (
    RawReceipt,
    build_predicate_execution_receipt,
)
from pipeline.evidence_discovery.evidence.witness_levels import (
    build_evidence_record,
    calculate_witness_level,
)
from pipeline.evidence_discovery.inputs import load_pair, parse_fcstm
from pipeline.evidence_discovery.orchestration import runner as runner_module
from pipeline.evidence_discovery.orchestration import runtime as runtime_module
from pipeline.evidence_discovery.orchestration.contracts import (
    MethodCellReceipt,
    PairRunStatus,
    RunManifest,
    RunSummaryReceipt,
    SourceProvenance,
)
from pipeline.evidence_discovery.orchestration.cost_correction import (
    build_corrected_method_cost,
)
from pipeline.evidence_discovery.orchestration.runner import (
    _admit_grounding_unresolved,
    _admit_frontier_unresolved,
    _d_decision_consistency_errors,
    _deduplicate_release_issues,
    _enrich_candidate,
    _failure_method_cell,
    _finalize_w2_audit_links,
    _grounding_response_contract,
    _materialize_exact_s2_inventory_candidates,
    _materialize_deterministic_execution_probes,
    _merge_grounding_contracts,
    _normalize_d_decision_shape,
    _normalize_grounding_exact_facts,
    _normalize_state_retention_carriers,
    _preflight_existing_endpoint_candidates,
    _preflight_synthetic_root_wrapper_reachability,
    _prepare_candidate,
    _prepared_is_finding_candidate,
    _resolve_working_contract_refs,
    run_experiment,
)
from pipeline.evidence_discovery.orchestration.runtime import (
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    STRUCTURED_STAGE_DEADLINE_SECONDS,
    STRUCTURED_STAGE_FINALIZATION_GRACE_SECONDS,
    STRUCTURED_STAGE_WRAPPER_DEADLINE_SECONDS,
    STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS,
    FixtureStructuredRuntime,
    PublicStructuredRuntime,
    StructuredSchemaValidationBundle,
    StructuredStageTimeout,
    _annotate_usage_billing,
    _cost_for_usage,
    _is_provider_error,
    _provider_timeout_seconds,
    _schema_validation_failures,
    _structured_model_call_reservation_limit,
    _structured_stage_deadline_seconds,
    _usage_rows,
)
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import (
    CONTRACT_SYSTEM_PROMPT,
    D_SYSTEM_PROMPT,
    DISCOVERY_GROUNDING_SYSTEM_PROMPT,
    CandidateIssue,
    CardinalityDomainBinding,
    CardinalityRequirement,
    ContextBudgetReceipt,
    ContractBindingHint,
    GroundingResponse,
    FrontierBatch,
    FrontierCheckReceipt,
    GroundingUnresolved,
    MethodResponse,
    NLContract,
    NLContractResponse,
    NLTransitionAlternative,
    NLTransitionGroup,
    SemanticAdjudication,
    SemanticBinding,
    SourceTransitionClosureReceipt,
    adjudicate_disposition,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_grounding_prompt,
    build_method_prompt,
    canonicalize_grounding_response,
    endpoint_candidate_is_satisfied_by_macro,
    evaluate_source_transition_closure,
    fallback_grounding,
    normalize_contract_state_roles,
    resolve_state_ref,
    resolve_transition_ref,
    suppress_closed_route_controller_candidates,
    suppress_contradicted_ambiguous_source_candidates,
    suppress_satisfied_source_transition_candidates,
)
from pipeline.evidence_discovery.semantics.binding import BindingResult
from pipeline.semantic_judge.artifacts import adapt_evidence_discovery_release
from pydantic import BaseModel, ValidationError

from utils.agent import AgentError
from utils.llm.config import LLMPricing, LLMTokenPrices

PAPER_ROOT = Path(__file__).parents[3]
REPORT_ROOT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"


def _candidate(
    pair,
    *,
    predicate_id: str,
    inputs: dict,
    refs: list[str] | None = None,
    expected: str = "expected violation",
    observed: str = "observed violation",
) -> CandidateIssue:
    return CandidateIssue(
        contract_id="NL-CONTRACT-FIXTURE",
        locus_kind="transition",
        locus_names=("Synthetic.Source", "Synthetic.Target"),
        property="transition_endpoints",
        violation_direction="missing",
        evidence_types=("closed_model_inventory", "transition_fact"),
        title="candidate title",
        requirement_quote="requirement quote",
        predicate_id=predicate_id,
        predicate_inputs=inputs,
        element_refs=refs or [pair.model.transitions[0].ref],
        source_refs=["nl:line:1"],
        expected=expected,
        observed=observed,
        strongest_rebuttal="none",
        reason="candidate reason",
        basis="candidate basis",
    )


def test_source_gate_and_input_aliases_are_deterministic() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    registry = load_registry()
    candidate = _candidate(
        pair,
        predicate_id="S5",
        inputs={
            "expected_guard": "front_distance > 10",
            "transition_name": pair.model.transitions[0].ref,
        },
    )
    binding = bind_candidate(candidate, pair.model)
    plan = compile_plan(candidate, binding, registry, obligation_id="0000:test", round_index=1, model=pair.model)

    assert plan.supported is False
    assert plan.source_audit_status == "candidate"
    assert plan.inputs["guard"] == "front_distance > 10"
    assert plan.inputs["transition"] == pair.model.transitions[0].ref
    assert plan.executable is True
    assert "expected_guard" not in plan.inputs
    assert "transition_name" not in plan.inputs

    for predicate_id in ("G4", "R3", "V1", "V3", "V4"):
        candidate = _candidate(pair, predicate_id=predicate_id, inputs={})
        plan = compile_plan(
            candidate,
            bind_candidate(candidate, pair.model),
            registry,
            obligation_id=f"0000:{predicate_id}",
            round_index=1,
            model=pair.model,
        )
        assert plan.supported is False, predicate_id


def test_grounding_unresolved_with_exact_binding_is_admitted_as_predicate_null_candidate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    state = pair.model.states[0]
    contract = NLContract(
        contract_id="NL-CONTRACT-NL1-UNRESOLVED-ACTION",
        segment_id="NL1",
        quote="The state must continue its operation.",
        normative_statement="The state must provide the required operation.",
        locus_kind="state",
        locus_names=(state.name,),
        property="state_action",
        state_role="operating_state",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "action_fact"),
        binding_hints=(
            ContractBindingHint(
                role="state",
                value=state.name,
                source_ref="NL1",
                reason="The state is the exact normative locus.",
                basis="provider-free unresolved-admission fixture",
            ),
        ),
        scope=state.name,
        source_refs=("NL1",),
        reason="The fixture supplies one atomic state-action contract.",
        basis="provider-free unresolved-admission fixture",
    )
    response = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=[
            SemanticBinding(
                binding_id="BIND-UNRESOLVED-STATE",
                contract_id=contract.contract_id,
                role="state",
                concept_name=state.name,
                status="exact",
                source_element_ref=f"source:state:{state.name}",
                model_element_ref=state.ref,
                reason="The state resolves uniquely in ModelIR.",
                basis="provider-free exact state binding",
            ),
        ],
        unresolved=[
            GroundingUnresolved(
                contract_id=contract.contract_id,
                reason="The frozen registry cannot express this precise action obligation.",
                basis="exact state binding and action obligation from NL1",
            ),
        ],
        reason="The fixture retains one unresolved contract.",
        basis="provider-free unresolved-admission fixture",
    )

    admitted, dispositions = _admit_grounding_unresolved(
        pair,
        {contract.contract_id: contract},
        [response],
        [],
    )

    assert len(admitted) == 1
    assert admitted[0].predicate_id is None
    assert admitted[0].element_refs == [state.ref]
    assert dispositions[0]["status"] == "admitted_w1"
    assert "frozen registry" in admitted[0].reason


def test_frontier_unresolved_admission_preserves_exact_w1_w0_and_existing_candidate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    exact_state = pair.model.states[0]
    exact_contract = NLContract(
        contract_id="NL-CONTRACT-NL1-FRONTIER-EXACT",
        segment_id="NL1",
        quote="The exact state must retain its operational obligation.",
        normative_statement="The exact state must retain its operational obligation.",
        locus_kind="state",
        locus_names=(exact_state.name,),
        property="state_action",
        state_role="operating_state",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "closed_model_inventory"),
        binding_hints=(),
        scope=exact_state.name,
        source_refs=("NL1",),
        reason="The fixture supplies one typed frontier obligation.",
        basis="provider-free frontier unresolved admission fixture",
    )
    unresolved_contract = exact_contract.model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL2-FRONTIER-W0",
            "segment_id": "NL2",
            "scope": "unresolved scope",
            "source_refs": ("NL2",),
        }
    )
    frontier = FrontierBatch(
        checks=(
            FrontierCheckReceipt(
                check_id="FRONTIER-EXACT",
                kind="cardinality",
                source_contract_ids=(exact_contract.contract_id,),
                status="unresolved",
                model_refs=(exact_state.ref,),
                source_refs=("NL1",),
                reason="The owner and carrier are exact but the member domain remains unresolved.",
                basis="provider-free exact frontier check",
            ),
            FrontierCheckReceipt(
                check_id="FRONTIER-W0",
                kind="cardinality",
                source_contract_ids=(unresolved_contract.contract_id,),
                status="unresolved",
                model_refs=(),
                source_refs=("NL2",),
                reason="The identity cannot be closed from the supplied facts.",
                basis="provider-free unresolved identity frontier check",
            ),
        ),
        reason="The fixture retains both unresolved checks.",
        basis="provider-free frontier unresolved admission fixture",
    )
    admitted, dispositions = _admit_frontier_unresolved(
        pair,
        {
            exact_contract.contract_id: exact_contract,
            unresolved_contract.contract_id: unresolved_contract,
        },
        frontier,
        (),
    )

    assert [item.contract_id for item in admitted] == [
        exact_contract.contract_id,
        unresolved_contract.contract_id,
    ]
    assert admitted[0].predicate_id is None
    assert admitted[0].element_refs == [exact_state.ref]
    assert admitted[1].predicate_id is None
    assert admitted[1].element_refs == []
    assert [item["status"] for item in dispositions] == [
        "admitted_w1",
        "admitted_w0",
    ]
    assert all(item.reason and item.basis for item in admitted)

    retained, retained_dispositions = _admit_frontier_unresolved(
        pair,
        {exact_contract.contract_id: exact_contract},
        frontier.model_copy(update={"checks": (frontier.checks[0],)}),
        (admitted[0],),
    )
    assert retained == []
    assert retained_dispositions[0]["status"] == (
        "existing_candidate_preserved_with_frontier_audit"
    )


def test_state_retention_normalization_preserves_exact_hierarchical_carrier_chain() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0024")
    contract = NLContract(
        contract_id="NL-CONTRACT-NL3-RETENTION",
        segment_id="NL3",
        quote="Approaching must retain the required motion behavior.",
        normative_statement="Approaching must retain the required motion behavior.",
        locus_kind="state",
        locus_names=("Approaching",),
        property="state_retention",
        state_role="operating_state",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "transition_fact"),
        binding_hints=(
            ContractBindingHint(
                role="state",
                value="Approaching",
                source_ref="NL3",
                reason="The fixture names the exact retained state.",
                basis="provider-free retention carrier fixture",
            ),
        ),
        scope="InMotion",
        source_refs=("NL3",),
        reason="The fixture supplies one state-retention obligation.",
        basis="provider-free retention carrier fixture",
    )
    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Approaching loses retention behavior",
        requirement_quote=contract.quote,
        element_refs=[pair.model.state("Approaching").ref],
        source_refs=["NL3"],
        expected=contract.normative_statement,
        observed="The retained state does not preserve its source-level continuation.",
        strongest_rebuttal="The exact state-to-owner carrier can be checked in the closed model.",
        reason="provider-free retention candidate",
        basis="provider-free retention carrier fixture",
    )

    normalized, dispositions = _normalize_state_retention_carriers(
        pair,
        [candidate],
        {contract.contract_id: contract},
    )

    assert len(normalized) == 1
    assert {
        pair.model.transition("transition:line:18").ref,
        pair.model.transition("transition:line:29").ref,
    }.issubset(set(normalized[0].element_refs))
    assert "tr_0007" in normalized[0].basis
    assert dispositions[0]["status"] == "normalized_exact_retention_carrier"


def test_existing_ordinary_endpoint_suppresses_missing_transition_candidate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    transition = next(
        item
        for item in pair.model.transitions
        if resolve_state_ref(item.source, pair.model) is not None
        and resolve_state_ref(item.target, pair.model) is not None
    )
    contract = NLContract(
        contract_id="NL-CONTRACT-NL2-EXACT-ENDPOINT",
        segment_id="NL2",
        quote="The source enters the target.",
        normative_statement=f"A transition from {transition.source} to {transition.target} must exist.",
        locus_kind="transition",
        locus_names=(transition.source, transition.target),
        property="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "transition_fact"),
        binding_hints=(
            ContractBindingHint(
                role="source",
                value=transition.source,
                source_ref="NL2",
                reason="The source endpoint is explicit.",
                basis="provider-free endpoint preflight fixture",
            ),
            ContractBindingHint(
                role="target",
                value=transition.target,
                source_ref="NL2",
                reason="The target endpoint is explicit.",
                basis="provider-free endpoint preflight fixture",
            ),
        ),
        scope=f"{transition.source}->{transition.target}",
        source_refs=("NL2",),
        reason="The fixture supplies an exact endpoint contract.",
        basis="provider-free endpoint preflight fixture",
    )
    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="The required transition is missing",
        requirement_quote=contract.quote,
        predicate_id="S2",
        predicate_inputs={
            "source": transition.source,
            "target": transition.target,
        },
        element_refs=[],
        source_refs=["NL2"],
        expected=contract.normative_statement,
        observed="No transition was found.",
        strongest_rebuttal="The exact transition may exist.",
        reason="Provider-free missing-transition candidate.",
        basis="provider-free endpoint preflight fixture",
    )

    retained, dispositions = _preflight_existing_endpoint_candidates(
        pair,
        [candidate],
        {contract.contract_id: contract},
    )

    assert retained == []
    assert dispositions[0]["status"] == "suppressed_existing_endpoint"
    assert transition.ref in dispositions[0]["carrier_refs"]


def test_d_none_shape_is_normalized_without_changing_semantic_fields() -> None:
    decision = SemanticAdjudication(
        obligation_id="0000:r1:i1",
        grounding="established",
        violated_obligation="The typed obligation is under review.",
        strongest_defeater="spurious alternative",
        defeater_kind="none",
        defeater_disposition="survives",
        reason="The provider supplied a structurally inconsistent defeater row.",
        basis="provider-free D shape fixture",
    )
    log: list[dict[str, object]] = []

    normalized = _normalize_d_decision_shape(
        decision,
        stage="initial",
        normalization_log=log,
    )

    assert normalized.strongest_defeater is None
    assert normalized.defeater_disposition == "defeated"
    assert normalized.grounding == decision.grounding
    assert normalized.reason == decision.reason
    assert "D shape normalization" in normalized.basis
    assert log[0]["changes"] == [
        "strongest_defeater=null",
        "defeater_disposition=defeated",
    ]


def test_predicate_plan_projects_context_but_direct_strict_validation_rejects_extra() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    registry = load_registry()
    candidate = _candidate(
        pair,
        predicate_id="S5",
        inputs={
            "transition": pair.model.transitions[0].ref,
            "guard": "front_distance > 10",
            "not_a_registry_input": "must not enter backend",
        },
    )
    plan = compile_plan(
        candidate,
        bind_candidate(candidate, pair.model),
        registry,
        obligation_id="0000:invalid-typed-input",
        round_index=1,
        model=pair.model,
    )

    assert plan.inputs.predicate_id == "S5"
    assert "not_a_registry_input" not in plan.inputs.to_backend_dict()
    direct = validate_predicate_inputs(
        "S5",
        {
            "transition": pair.model.transitions[0].ref,
            "guard": "front_distance > 10",
            "not_a_registry_input": "must remain invalid without compiler projection",
        },
    )
    assert isinstance(direct, UnsupportedPredicateInputs)
    assert direct.claimed_predicate_id == "S5"
    assert direct.validation_errors
    schema = PredicatePlan.model_json_schema()
    discriminator = schema["properties"]["inputs"]["discriminator"]
    assert discriminator["propertyName"] == "predicate_id"
    assert set(discriminator["mapping"]) == {
        "S1", "S2", "S3", "S4", "S5", "S6",
        "G1", "G2", "G3", "G4",
        "R1", "R2", "R3", "R4",
        "V1", "V2", "V3", "V4", "V5",
        "unsupported",
    }


def test_s3_s5_projection_keeps_typed_carrier_and_drops_redundant_endpoints() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    registry = load_registry()
    transition = pair.model.transitions[0]
    fixtures = (
        ("S3", {"transition_ref": transition.ref, "triggers": ["Power On"]}),
        ("S5", {"transition_ref": transition.ref, "guard": transition.guard or "none"}),
    )

    for predicate_id, predicate_inputs in fixtures:
        candidate = _candidate(
            pair,
            predicate_id=predicate_id,
            inputs={
                **predicate_inputs,
                "source": transition.source,
                "target": transition.target,
            },
        )
        plan = compile_plan(
            candidate,
            bind_candidate(candidate, pair.model),
            registry,
            obligation_id=f"0000:{predicate_id}-projection",
            round_index=1,
            model=pair.model,
        )

        assert plan.inputs.predicate_id == predicate_id
        assert plan.inputs["transition"] == transition.ref
        assert "source" not in plan.inputs.to_backend_dict()
        assert "target" not in plan.inputs.to_backend_dict()
        assert candidate.predicate_inputs["source"] == transition.source
        assert candidate.predicate_inputs["target"] == transition.target


def test_present_guarded_initial_edge_is_w1_not_false_s2_satisfaction() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    transition = pair.model.transition("transition:line:24")
    assert transition is not None
    assert transition.guard is not None
    target = next(state for state in pair.model.states if state.name == "enter_hwy")
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL3-INITIAL-1",
        locus_kind="state",
        locus_names=("HighwayMode", "enter_hwy"),
        property="initial_entry",
        violation_direction="missing",
        evidence_types=("initial_entry_fact", "guard_fact"),
        title="HighwayMode lacks an unconditional default entry",
        requirement_quote="HighwayMode begins in enter_hwy.",
        predicate_id="S2",
        predicate_inputs={
            "source": "[*]",
            "target": "enter_hwy",
            "scope": "HighwayMode",
            "transition": transition.ref,
        },
        element_refs=[transition.ref, target.ref],
        source_refs=["NL3"],
        expected="The owner enters enter_hwy without a condition.",
        observed="The exact endpoint edge exists with a parsed guard.",
        strongest_rebuttal="The guarded edge has the requested endpoint pair.",
        reason="The supplied initial-entry fact identifies a conditional edge.",
        basis="0029 FCSTM and owned initial-entry fact fixture",
    )

    prepared = _prepare_candidate(pair, candidate, 1, 0)

    assert prepared["binding"].precise is True
    assert prepared["candidate"].predicate_id is None
    assert prepared["candidate"].predicate_inputs == {}
    assert prepared["plan"].supported is False
    assert prepared["receipt"].verdict == "unknown"
    assert calculate_witness_level(
        prepared["binding"],
        prepared["plan"],
        prepared["receipt"],
    ) == "W1"
    semantic = SemanticAdjudication(
        obligation_id=prepared["obligation_id"],
        grounding="established",
        violated_obligation="HighwayMode requires an unconditional default entry.",
        strongest_defeater=None,
        defeater_kind="none",
        defeater_disposition="defeated",
        reason="The exact guarded edge does not establish unconditional initial entry.",
        basis="typed initial-entry contract and parsed transition guard",
    )
    assert adjudicate_disposition(
        prepared["candidate"],
        prepared["binding"],
        semantic,
        receipt=prepared["receipt"],
    )["d_level"] == "D2"


def test_absent_exact_initial_edge_remains_an_s2_executable_claim() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0035")
    target = next(state for state in pair.model.states if state.name == "DoorShut")
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL1-INITIAL-1",
        locus_kind="state",
        locus_names=("DoorShut",),
        property="initial_entry",
        violation_direction="missing",
        evidence_types=("initial_entry_fact", "transition_fact"),
        title="DoorShut lacks the required exact initial edge",
        requirement_quote="The microwave begins in DoorShut.",
        predicate_id="S2",
        predicate_inputs={
            "source": "[*]",
            "target": "DoorShut",
            "scope": "closed_fcstm",
        },
        element_refs=[target.ref],
        source_refs=["NL1"],
        expected="An exact pseudo-state edge enters DoorShut.",
        observed="No such endpoint edge is present.",
        strongest_rebuttal="A textual stereotype may label DoorShut as initial.",
        reason="The exact state is bound and the expected edge can be checked.",
        basis="0035 FCSTM exact state inventory fixture",
    )

    prepared = _prepare_candidate(pair, candidate, 1, 0)

    assert prepared["binding"].precise is True
    assert prepared["candidate"].predicate_id == "S2"
    assert prepared["receipt"].terminal_state == "completed"
    assert prepared["receipt"].verdict == "false"


def test_w0_w1_and_unknown_are_mutually_exclusive() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    registry = load_registry()
    transition = pair.model.transitions[0]
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": transition.source, "target": transition.target, "scope": "closed_fcstm"},
    )
    precise_binding = bind_candidate(candidate, pair.model)
    executable_plan = compile_plan(
        candidate,
        precise_binding,
        registry,
        obligation_id="0000:w2",
        round_index=1,
        model=pair.model,
    )
    completed = RawReceipt(
        receipt_id="r1",
        backend="fixture",
        terminal_state="completed",
        verdict="true",
        reason="fixture completed",
        basis="fixture basis",
    )
    unknown = RawReceipt(
        receipt_id="r2",
        backend="fixture",
        terminal_state="timeout",
        verdict="unknown",
        reason="fixture timeout",
        basis="fixture basis",
    )

    assert precise_binding.precise is True
    assert calculate_witness_level(precise_binding, executable_plan, completed) == "W2"
    assert calculate_witness_level(precise_binding, executable_plan, unknown) == "UNKNOWN"

    unsupported_candidate = _candidate(
        pair,
        predicate_id="S5",
        inputs={"transition": transition.ref, "guard": transition.guard or "none"},
    )
    unsupported_binding = bind_candidate(unsupported_candidate, pair.model)
    unsupported_plan = compile_plan(
        unsupported_candidate,
        unsupported_binding,
        registry,
        obligation_id="0000:w1",
        round_index=1,
        model=pair.model,
    )
    assert calculate_witness_level(unsupported_binding, unsupported_plan, completed) == "W1"

    missing_input_candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": transition.source, "scope": "closed_fcstm"},
    )
    missing_input_binding = bind_candidate(missing_input_candidate, pair.model)
    missing_input_plan = compile_plan(
        missing_input_candidate,
        missing_input_binding,
        registry,
        obligation_id="0000:w1-missing-predicate-input",
        round_index=1,
        model=pair.model,
    )
    assert missing_input_binding.precise is True
    assert missing_input_plan.binding_complete is False
    assert (
        calculate_witness_level(
            missing_input_binding, missing_input_plan, completed
        )
        == "W1"
    )

    incomplete = BindingResult(
        precise=False,
        element_refs=(),
        source_refs=(),
        reason="fixture binding missing",
        basis="fixture binding basis",
    )
    assert calculate_witness_level(incomplete, executable_plan, completed) == "W0"


def test_binding_normalizes_display_refs_but_rejects_ambiguous_edges() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(
        pair,
        predicate_id="S5",
        inputs={
            "transition": "HumanDrivingMode -> AutonomousMode : /front_distance_10",
            "guard": "front_distance > 10",
        },
        refs=["transition:line:999", "state:HumanDrivingMode:line:999"],
    )
    binding = bind_candidate(candidate, pair.model)
    assert binding.precise is True
    assert "transition:line:20" in binding.element_refs
    assert resolve_transition_ref(candidate.predicate_inputs["transition"], pair.model) == "transition:line:20"

    ambiguous = parse_fcstm(
        "state A\nstate B\nA -> B : first\nA -> B : second\n"
    )
    assert resolve_transition_ref(None, ambiguous, source="A", target="B") is None

    invalid_kind = _candidate(
        pair,
        predicate_id="S1",
        inputs={"kind": "simple_state", "element": "HumanDrivingMode", "scope": "closed_fcstm"},
        refs=["state:HumanDrivingMode:line:999"],
    )
    invalid_binding = bind_candidate(invalid_kind, pair.model)
    invalid_plan = compile_plan(
        invalid_kind,
        invalid_binding,
        load_registry(),
        obligation_id="0000:invalid-kind",
        round_index=1,
        model=pair.model,
    )
    invalid_receipt = run_backend(invalid_plan, pair.model, "invalid-kind-receipt")
    assert invalid_receipt.verdict == "unknown"
    assert calculate_witness_level(invalid_binding, invalid_plan, invalid_receipt) == "UNKNOWN"


def test_enrich_candidate_replaces_typed_transition_endpoints_with_canonical_model_values() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    transition = next(
        item for item in pair.model.transitions
        if item.source == "Searching" and item.target == "FormationAdjustment"
    )
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={
            "transition": transition.ref,
            "transition_ref": transition.ref,
            "source": f"state:{transition.source}:line:13",
            "target": f"state:{transition.target}:line:14",
            "scope": "closed_fcstm",
        },
        refs=[transition.ref, f"state:{transition.source}:line:13", f"state:{transition.target}:line:14"],
    )
    binding = bind_candidate(candidate, pair.model)
    enriched = _enrich_candidate(candidate, binding, pair)

    assert enriched.predicate_inputs["transition"] == transition.ref
    assert enriched.predicate_inputs["transition_ref"] == transition.ref
    assert enriched.predicate_inputs["source"] == transition.source
    assert enriched.predicate_inputs["target"] == transition.target

    plan = compile_plan(
        enriched,
        binding,
        load_registry(),
        obligation_id="0046:canonical-s2",
        round_index=1,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    receipt = run_backend(plan, pair.model, "0046:canonical-s2:receipt")
    assert receipt.verdict == "true"
    assert receipt.terminal_state == "completed"


def test_enrich_candidate_preserves_required_s2_endpoints_when_supporting_edge_differs() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0035")
    initial_edge = next(item for item in pair.model.transitions if item.source == "[*]")
    required_target = pair.model.state("DoorShut")
    observed_target = pair.model.state(initial_edge.target)
    assert required_target is not None
    assert observed_target is not None
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={
            "source": "[*]",
            "target": "DoorShut",
            "scope": "closed_fcstm",
        },
        refs=[initial_edge.ref, observed_target.ref, required_target.ref],
    ).model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL1-INITIAL-1",
            "locus_kind": "scope",
            "locus_names": ("microwave", "DoorShut"),
            "property": "initial_entry",
            "violation_direction": "wrong_target",
        }
    )
    binding = bind_candidate(candidate, pair.model)
    enriched = _enrich_candidate(candidate, binding, pair)

    assert enriched.predicate_inputs["source"] == "[*]"
    assert enriched.predicate_inputs["target"] == "DoorShut"
    assert "transition" not in enriched.predicate_inputs
    assert "transition_ref" not in enriched.predicate_inputs

    plan = compile_plan(
        enriched,
        binding,
        load_registry(),
        obligation_id="0035:required-initial-s2",
        round_index=1,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    receipt = run_backend(plan, pair.model, "0035:required-initial-s2:receipt")
    assert receipt.verdict == "false"
    assert receipt.counterexample == [{"source": "[*]", "target": "DoorShut"}]


def test_w2_audit_contains_logic_hashes_backend_and_retry_records(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    registry = load_registry()
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": "[*]", "target": "Ready", "scope": "closed_fcstm"},
    )
    binding = bind_candidate(candidate, pair.model)
    plan = compile_plan(
        candidate,
        binding,
        registry,
        obligation_id="0000:audit",
        round_index=1,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    receipt = RawReceipt(
        receipt_id="receipt",
        backend="fixture",
        terminal_state="completed",
        verdict="false",
        reason="fixture counterexample",
        basis="fixture backend",
        counterexample=[{"source": "[*]", "target": "Ready"}],
        trace=[{"node": "[*]"}],
    )
    retry_records = [{"outer_attempt": 1, "retry_records": [{"operation": "scheduled"}]}]
    record = build_evidence_record(
        pair=pair,
        obligation_id="0000:audit",
        candidate=candidate,
        binding=binding,
        plan=plan,
        receipt=receipt,
        source_attribution={"requirement": {"path": "nl.txt"}, "model": {"hash": pair.hashes["fcstm"]}},
        retry_records=retry_records,
        semantic_adjudication=SemanticAdjudication(
            obligation_id="0000:audit",
            grounding="established",
            violated_obligation="The exact initial edge is required by the supplied obligation.",
            strongest_defeater=None,
            defeater_kind="none",
            defeater_disposition="defeated",
            reason="The semantic dossier establishes the supplied initial-edge obligation.",
            basis="fixture NL clause, exact binding, and backend receipt",
        ),
    )

    assert record["witness_level"] == "W2"
    assert record["audit_bundle"] is not None
    bundle = record["audit_bundle"]
    assert bundle["predicate_logic"]["semantics"]
    assert bundle["predicate_logic"]["source_ids"]
    assert bundle["predicate_logic"]["inputs"]["model_hash"] == bundle["model_hash"]
    assert bundle["compiled_program"]["source"]
    assert bundle["compiled_program"]["sha256"].startswith("sha256:")
    assert bundle["model_hash"] == pair.hashes["fcstm"]
    assert bundle["program_hash"] == bundle["compiled_program"]["sha256"]
    assert bundle["backend_result"]["terminal_state"] == "completed"
    assert bundle["execution_receipt"]["verdict"] == "violation"
    assert bundle["execution_receipt"]["typed_inputs_hash"].startswith("sha256:")
    assert bundle["execution_receipt"]["receipt_hash"].startswith("sha256:")
    assert bundle["generated_at"]
    assert bundle["execution_environment"]["python_version"]
    assert bundle["structured_run_summary"]["terminal_state"] == "completed"
    assert bundle["method_receipt"]["status"] == "pending_cell_finalization"
    assert bundle["judge_receipt"]["status"] == "pending_independent_judge"
    assert bundle["counterexample"]
    assert bundle["trace"]
    assert bundle["retry_records"] == retry_records
    assert bundle["source_attribution"]
    assert bundle["reason"]
    assert bundle["basis"]
    assert bundle["semantic_adjudication"]["reason"]
    pre_finalization_bundle = dict(bundle)
    audit_hash = bundle.pop("audit_hash")
    expected_hash = "sha256:" + hashlib.sha256(
        json.dumps(bundle, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert audit_hash == expected_hash

    audit_path = tmp_path / "audit_bundles" / "0000-audit.json"
    audit_path.parent.mkdir(parents=True)
    audit_path.write_text(
        json.dumps(pre_finalization_bundle, ensure_ascii=False),
        encoding="utf-8",
    )
    cell = {
        "schema": "evidence-discovery.method_cell.v8",
        "round": 1,
        "run_id": "1" * 32,
        "run_contract_hash": "sha256:" + "1" * 64,
        "pair_input_hash": "sha256:" + "2" * 64,
        "status": "completed",
        "eligible": True,
        "evidence_records": [
            {
                "obligation_id": "0000:audit",
                "witness_level": "W2",
                "audit_bundle_path": str(audit_path),
            }
        ],
    }
    _finalize_w2_audit_links(
        output_root=tmp_path,
        pair_id="0000",
        rounds_data=[cell],
    )
    finalized = json.loads(audit_path.read_text(encoding="utf-8"))
    assert finalized["pre_finalization_audit_hash"] == audit_hash
    assert finalized["audit_finalization"]["pre_finalization_audit_hash"] == audit_hash
    assert finalized["judge_receipt"]["status"] == "pending_independent_judge"
    assert finalized["audit_hash"] != audit_hash
    W2AuditBundle.model_validate(finalized)


def test_source_gate_keeps_w1_but_preserves_real_execution_receipt() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    transition = pair.model.transitions[0]
    candidate = _candidate(
        pair,
        predicate_id="S5",
        inputs={
            "transition": transition.ref,
            "guard": "front_distance > 10",
        },
        refs=[transition.ref],
    )
    binding = bind_candidate(candidate, pair.model)
    plan = compile_plan(
        candidate,
        binding,
        load_registry(),
        obligation_id="0000:source-gate-execution",
        round_index=1,
        model=pair.model,
    )
    receipt = run_backend(plan, pair.model, "0000:source-gate-execution:receipt")
    execution = build_predicate_execution_receipt(
        pair_id="0000",
        run_id="1" * 32,
        contract_id=candidate.contract_id,
        obligation_id="0000:source-gate-execution",
        plan=plan,
        receipt=receipt,
    )

    assert plan.source_gate_passed is False
    assert plan.executable is True
    assert plan.supported is False
    assert receipt.terminal_state == "completed"
    assert execution["execution_status"] == "executed"
    assert execution["verdict"] in {"pass", "violation"}
    assert execution["source_gate_passed"] is False


def _probe_contract(
    *,
    contract_id: str,
    property_name: str,
    locus_kind: str = "transition",
    locus_names: tuple[str, ...] = ("Source", "Target"),
    cardinality_requirement=None,
    binding_hints=(),
) -> NLContract:
    return NLContract(
        contract_id=contract_id,
        segment_id="NL1",
        quote="The supplied requirement establishes this typed obligation.",
        normative_statement="The supplied typed obligation must hold.",
        locus_kind=locus_kind,
        locus_names=locus_names,
        property=property_name,
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("source_identity", "closed_model_inventory"),
        binding_hints=binding_hints,
        cardinality_requirement=cardinality_requirement,
        scope="provider-free probe scope",
        source_refs=("NL1",),
        reason="The fixture establishes one atomic contract.",
        basis="provider-free deterministic execution-probe fixture",
    )


def _exact_binding(
    *,
    contract_id: str,
    role: str,
    model_ref: str,
    carrier_ref: str | None = None,
) -> SemanticBinding:
    return SemanticBinding(
        binding_id=f"BIND-{contract_id.rsplit('-', 1)[-1]}-{role}",
        contract_id=contract_id,
        role=role,
        concept_name=role,
        status="exact",
        source_element_ref=f"source:{model_ref}",
        model_element_ref=model_ref,
        carrier_transition_ref=carrier_ref,
        reason="The fixture supplies one exact closed-model reference.",
        basis="provider-free exact SemanticBinding fixture",
    )


def test_execution_probe_admission_requires_exact_carrier_and_keeps_s1_supporting(
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    transition = pair.model.transitions[0]
    contract = _probe_contract(
        contract_id="NL-CONTRACT-PROBE-ENDPOINT",
        property_name="transition_endpoints",
        locus_names=(transition.source, transition.target),
        binding_hints=(
            ContractBindingHint(
                role="source",
                value=transition.source,
                reason="The fixture identifies the exact transition source.",
                basis="provider-free transition endpoint fixture",
            ),
            ContractBindingHint(
                role="target",
                value=transition.target,
                reason="The fixture identifies the exact transition target.",
                basis="provider-free transition endpoint fixture",
            ),
        ),
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            _exact_binding(
                contract_id=contract.contract_id,
                role="transition",
                model_ref=transition.ref,
                carrier_ref=transition.ref,
            ),
        ),
        reason="The exact endpoint carrier is available.",
        basis="provider-free exact carrier probe fixture",
    )

    probes, probe_contracts, dispositions = _materialize_deterministic_execution_probes(
        pair,
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    assert len(probes) == 1
    assert probes[0].predicate_id == "S1"
    assert probes[0].property == "element_declaration"
    assert probes[0].element_refs == [transition.ref]
    assert probes[0].contract_id in probe_contracts
    assert dispositions[0]["status"] == "admitted_exact_carrier"

    prepared = _prepare_candidate(
        pair,
        probes[0],
        round_index=1,
        index=0,
        contracts_by_id=probe_contracts,
    )
    assert prepared["receipt"].terminal_state == "completed"
    assert prepared["receipt"].verdict == "true"
    assert _prepared_is_finding_candidate(prepared) is False


def test_execution_probe_maps_exact_trigger_binding_to_s3_execution() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0010")
    transition = next(
        item for item in pair.model.transitions if item.triggers == ("Power_On",)
    )
    event = next(item for item in pair.model.events if item.name == "Power_On")
    contract = _probe_contract(
        contract_id="NL-CONTRACT-PROBE-TRIGGER",
        property_name="trigger_set",
        locus_names=(transition.source, transition.target),
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            _exact_binding(
                contract_id=contract.contract_id,
                role="event",
                model_ref=event.ref,
                carrier_ref=transition.ref,
            ),
        ),
        reason="The fixture supplies an exact event and carrier transition.",
        basis="provider-free exact trigger-set probe fixture",
    )

    probes, probe_contracts, dispositions = _materialize_deterministic_execution_probes(
        pair,
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    s3_probe = next(item for item in probes if item.predicate_id == "S3")
    assert s3_probe.predicate_inputs == {
        "transition": transition.ref,
        "triggers": ["Power_On"],
    }
    assert any(item.predicate_id == "S1" for item in probes)
    assert any(
        item["status"] == "admitted_exact_trigger_carrier"
        for item in dispositions
    )

    prepared = _prepare_candidate(
        pair,
        s3_probe,
        round_index=1,
        index=0,
        contracts_by_id={contract.contract_id: contract, **probe_contracts},
    )
    assert prepared["plan"].source_gate_passed is False
    assert prepared["receipt"].terminal_state == "completed"
    assert prepared["receipt"].verdict == "true"
    assert _prepared_is_finding_candidate(prepared) is False


def test_working_contract_root_and_segment_join_to_unique_model_carrier() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0002")

    refs, unresolved = _resolve_working_contract_refs(
        pair,
        element_ids=(
            "source:transition:tr_0003",
            "compiler:transition_segment:tr_0003:segment:1",
        ),
    )

    assert refs == ["transition:line:10"]
    assert unresolved == []


def test_exact_grounding_binding_uses_working_contract_model_projection() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0002")
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            SemanticBinding(
                binding_id="BIND-WORKING-PUMPSTATE",
                contract_id="NL-CONTRACT-PROBE-STATE",
                role="state",
                concept_name="PumpState",
                status="exact",
                model_element_ref=(
                    "state:llms_emp_feedback_final_0002.PumpControl.PumpState"
                ),
                reason="The working contract provides one exact mapped state identity.",
                basis="provider-free working-contract projection fixture",
            ),
        ),
        reason="The fixture supplies one exact working-contract binding.",
        basis="provider-free working-contract projection fixture",
    )

    assert runner_module._exact_grounding_model_refs(
        pair,
        (grounding,),
        "NL-CONTRACT-PROBE-STATE",
    ) == ["state:PumpState:line:7"]


def test_working_contract_event_disambiguates_shared_endpoints_without_guessing() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0010")

    refs, unresolved = _resolve_working_contract_refs(
        pair,
        element_ids=("source:transition:tr_0002",),
    )
    assert refs == ["transition:line:14"]
    assert unresolved == []

    payload = json.loads(json.dumps(pair.working_contract.payload))
    root = next(
        item
        for item in payload["elements"]
        if item["element_id"] == "source:transition:tr_0002"
    )
    root["semantic_fields"].pop("raw_label", None)
    root["semantic_fields"].pop("event_interpretation", None)
    ambiguous_pair = pair.model_copy(
        update={
            "working_contract": pair.working_contract.model_copy(
                update={"payload": payload}
            )
        }
    )

    refs, unresolved = _resolve_working_contract_refs(
        ambiguous_pair,
        element_ids=("source:transition:tr_0002",),
    )
    assert refs == []
    assert unresolved == ["source:transition:tr_0002"]


def test_event_projection_never_adds_same_named_state_to_event_binding() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0056")
    event_ref = "event:Intercepted:line:3"
    records = runner_module._working_contract_records(pair)
    event_projection = next(
        item
        for item in records
        if item.get("kind") == "opaque_event_projection"
        and event_ref in runner_module._working_record_model_refs(
            pair, item, records
        )
    )

    assert runner_module._working_record_model_refs(
        pair, event_projection, records
    ) == [event_ref]


def test_transition_group_event_projection_admits_s3_or_blocks_ambiguity() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0010")
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL3-POWERON-FIXTURE",
        segment_id="NL3",
        source_name="system",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL3-POWERON-FIXTURE",
                target_name="human driving mode",
                event="power on",
                reason="The fixture supplies one typed event alternative.",
                basis="provider-free transition-group event fixture",
            ),
        ),
        reason="The fixture supplies one shared-source transition group.",
        basis="provider-free transition-group event fixture",
    )

    probes, probe_contracts, dispositions = (
        _materialize_deterministic_execution_probes(
            pair,
            {},
            (),
            (),
            (group,),
        )
    )
    s3_probe = next(item for item in probes if item.predicate_id == "S3")
    assert s3_probe.predicate_inputs == {
        "transition": "transition:line:14",
        "triggers": ["Power_On"],
    }
    assert s3_probe.contract_id in probe_contracts
    assert dispositions[-1]["status"] == (
        "admitted_transition_group_event_carrier"
    )

    ambiguous_group = group.model_copy(
        update={
            "group_id": "NL-GROUP-NL4-DISTANCE-FIXTURE",
            "segment_id": "NL4",
            "alternatives": (
                NLTransitionAlternative(
                    alternative_id="ALT-NL4-DISTANCE-FIXTURE",
                    target_name="autonomous state",
                    event="front_distance > 10",
                    reason="The fixture supplies one ambiguous event carrier.",
                    basis="provider-free ambiguous transition-group fixture",
                ),
            ),
        }
    )
    probes, _, _ = _materialize_deterministic_execution_probes(
        pair,
        {},
        (),
        (),
        (ambiguous_group,),
    )
    assert not any(item.predicate_id == "S3" for item in probes)


@pytest.mark.parametrize("property_name", ["containment", "cardinality", "initial_entry"])
def test_execution_probe_does_not_relabel_non_declaration_contracts_as_s1(
    property_name: str,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    state = pair.model.states[1]
    transition = pair.model.transitions[0]
    cardinality_requirement = None
    if property_name == "cardinality":
        from pipeline.evidence_discovery.semantics import CardinalityRequirement

        cardinality_requirement = CardinalityRequirement(
            required_count=1,
            member_domain="explicit_named_members",
            scope_concept=state.name,
            member_concept="member",
            reason="The fixture supplies a finite named domain.",
            basis="provider-free cardinality probe fixture",
        )
    contract = _probe_contract(
        contract_id=f"NL-CONTRACT-PROBE-{property_name.upper()}",
        property_name=property_name,
        locus_kind="state" if property_name != "containment" else "composite",
        locus_names=(state.name,),
        cardinality_requirement=cardinality_requirement,
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            _exact_binding(
                contract_id=contract.contract_id,
                role="state",
                model_ref=state.ref,
                carrier_ref=transition.ref,
            ),
        ),
        reason="The fixture has an exact state binding.",
        basis="provider-free non-declaration probe fixture",
    )

    probes, _, _ = _materialize_deterministic_execution_probes(
        pair,
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    assert probes == []


def test_g4_execution_probe_requires_exact_owner_and_marked_target() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    owner, target = pair.model.states[1:3]
    contract = _probe_contract(
        contract_id="NL-CONTRACT-PROBE-TERMINATION",
        property_name="termination",
        locus_kind="state",
        locus_names=(owner.name, target.name),
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            _exact_binding(
                contract_id=contract.contract_id,
                role="owner",
                model_ref=owner.ref,
            ),
            _exact_binding(
                contract_id=contract.contract_id,
                role="target",
                model_ref=target.ref,
            ),
        ),
        reason="The fixture supplies exact termination endpoints.",
        basis="provider-free exact termination probe fixture",
    )

    probes, probe_contracts, dispositions = _materialize_deterministic_execution_probes(
        pair,
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    assert len(probes) == 1
    assert probes[0].predicate_id == "G4"
    assert probes[0].predicate_inputs == {
        "roots": [owner.name],
        "marked": [target.name],
    }
    assert probes[0].contract_id == contract.contract_id
    assert probe_contracts == {}
    assert dispositions[0]["status"] == "admitted_exact_termination"

    missing_target = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=(
            _exact_binding(
                contract_id=contract.contract_id,
                role="owner",
                model_ref=owner.ref,
            ),
        ),
        reason="The target remains unresolved.",
        basis="provider-free incomplete termination fixture",
    )
    probes, _, _ = _materialize_deterministic_execution_probes(
        pair,
        {contract.contract_id: contract},
        (missing_target,),
        (),
    )
    assert probes == []


def test_trajectory_receipt_requires_closed_contract_and_checks_retention() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(
        pair,
        predicate_id="R4",
        inputs={
            "scenario": {
                "trace": [
                    {"step": 0, "active_states": ["Ready"]},
                    {"step": 1, "active_states": ["Ready"]},
                ]
            },
            "state": "Ready",
            "interval": [0, 1],
        },
        refs=[pair.model.states[0].ref],
    )
    plan = compile_plan(
        candidate,
        bind_candidate(candidate, pair.model),
        load_registry(),
        obligation_id="0000:r4-trajectory",
        round_index=1,
        model=pair.model,
    )
    receipt = run_trajectory(plan, pair.model, "0000:r4-trajectory:receipt")

    assert plan.executable is True
    assert receipt.terminal_state == "completed"
    assert receipt.verdict == "true"


def test_d_mapping_is_invariant_to_free_text_and_uses_typed_semantics() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": "[*]", "target": "Ready", "scope": "closed_fcstm"},
        expected="The requirement wording is one interpretation.",
        observed="The model prose uses completely different wording.",
    )
    binding = bind_candidate(candidate, pair.model)
    semantic = SemanticAdjudication(
        obligation_id="0000:typed-d",
        grounding="established",
        violated_obligation="The supplied exact transition obligation is grounded.",
        strongest_defeater=None,
        defeater_kind="none",
        defeater_disposition="defeated",
        reason="The typed semantic facts establish the first reading.",
        basis="fixture semantic dossier",
    )
    first = adjudicate_disposition(candidate, binding, semantic)
    altered = candidate.model_copy(
        update={
            "expected": "unrelated prose with a different surface form",
            "observed": "another unrelated prose fragment",
            "strongest_rebuttal": "a long alternative explanation",
        }
    )
    second = adjudicate_disposition(altered, binding, semantic)
    assert first["d_level"] == second["d_level"] == "D2"
    assert first["basis"] == second["basis"]

    unresolved = semantic.model_copy(update={"grounding": "unresolved"})
    assert adjudicate_disposition(candidate, binding, unresolved)["d_level"] == "D_UNRESOLVED"


def test_typed_defeater_protocol_distinguishes_undercutting_from_rebutting() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(
        pair,
        predicate_id=None,
        inputs={},
        refs=[pair.model.states[0].ref],
    )
    binding = bind_candidate(candidate, pair.model)
    undercutting = SemanticAdjudication(
        obligation_id="0000:undercutting",
        grounding="established",
        violated_obligation="The supplied facts establish one competent violation reading.",
        strongest_defeater="A second competent interpretation remains compatible with the same facts.",
        defeater_kind="undercutting",
        defeater_disposition="survives",
        reason="Two competent readings remain coextensive with the supplied facts.",
        basis="provider-free typed defeater fixture",
    )
    rebutting = undercutting.model_copy(
        update={
            "obligation_id": "0000:rebutting",
            "strongest_defeater": "A competent supplied fact rebuts the alleged violation.",
            "defeater_kind": "rebutting",
        }
    )

    assert adjudicate_disposition(candidate, binding, undercutting)["d_level"] == "D1"
    assert adjudicate_disposition(candidate, binding, rebutting)["d_level"] == "D0"
    unresolved_undercutting = undercutting.model_copy(
        update={"defeater_disposition": "unresolved"}
    )
    assert (
        adjudicate_disposition(candidate, binding, unresolved_undercutting)[
            "d_level"
        ]
        == "D_UNRESOLVED"
    )


def test_completed_true_backend_result_closes_candidate_as_d0() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": "[*]", "target": "Ready", "scope": "closed_fcstm"},
    )
    binding = bind_candidate(candidate, pair.model)
    semantic = SemanticAdjudication(
        obligation_id="0000:true-result",
        grounding="established",
        violated_obligation="The candidate claims an initial transition issue.",
        strongest_defeater=None,
        defeater_kind="none",
        defeater_disposition="defeated",
        reason="The fixture semantic call incorrectly proposed a violation.",
        basis="fixture typed semantic response",
    )
    receipt = RawReceipt(
        receipt_id="0000:true-result:receipt",
        backend="source_static:S2",
        terminal_state="completed",
        verdict="true",
        reason="The exact transition exists in the closed model.",
        basis="fixture exact transition membership",
    )
    disposition = adjudicate_disposition(candidate, binding, semantic, receipt=receipt)
    assert disposition["d_level"] == "D0"
    assert "verdict=true" in str(disposition["basis"])


def test_both_complementary_grounding_lenses_contribute_exact_candidates() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    transition = pair.model.transitions[0]
    source_candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": transition.source, "target": transition.target, "scope": "source"},
        refs=["source:transition:0000:1"],
    ).model_copy(update={"source_refs": ["nl:NL1"]})
    model_candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={"source": transition.source, "target": transition.target, "scope": "closed_fcstm"},
        refs=[transition.ref],
    ).model_copy(update={"source_refs": ["nl:NL1"]})
    joined = assemble_method_response(
        [
            GroundingResponse(
                lens="contract_structure_contrast",
                candidates=[source_candidate],
                reason="structure fixture",
                basis="structure fixture",
            ),
            GroundingResponse(
                lens="behavior_consequence",
                candidates=[model_candidate],
                reason="behavior fixture",
                basis="behavior fixture",
            ),
        ],
        reason="join fixture",
        basis="exact typed candidate keys",
    )
    assert len(joined.issues) == 2
    assert {tuple(issue.element_refs) for issue in joined.issues} == {
        ("source:transition:0000:1",),
        (transition.ref,),
    }


def test_report_dedup_uses_exact_typed_defect_key_only() -> None:
    base = {
        "issue_id": "0000:r1:issue:0",
        "contract_id": "NL-CONTRACT-NL1",
        "locus_kind": "state",
        "locus_names": ["Stopping"],
        "property": "deadlock_freedom",
        "violation_direction": "dead_end",
        "d_level": "D1",
        "witness_level": "W1",
    }
    duplicate = {
        **base,
        "issue_id": "0000:r1:issue:1",
        "contract_id": "NL-CONTRACT-NL2",
        "d_level": "D2",
    }
    distinct = {
        **base,
        "issue_id": "0000:r1:issue:2",
        "contract_id": "NL-CONTRACT-NL3",
        "violation_direction": "unreachable",
    }

    release = _deduplicate_release_issues([base, duplicate, distinct])

    assert len(release) == 2
    merged = next(item for item in release if item["violation_direction"] == "dead_end")
    assert merged["issue_id"] == duplicate["issue_id"]
    assert merged["facet_issue_ids"] == [base["issue_id"], duplicate["issue_id"]]
    assert merged["contract_ids"] == ["NL-CONTRACT-NL1", "NL-CONTRACT-NL2"]
    assert merged["deduplication"]["algorithm_version"] == "exact-typed-defect-key.v1"


def test_terminality_uses_exact_final_pseudostate_edges_not_state_names() -> None:
    named_model = parse_fcstm(
        "state terminal_named\nstate EndState\n[*] -> terminal_named\n"
    )
    assert _terminal_states(named_model) == set()

    formal_model = parse_fcstm(
        "state terminal_named\nstate EndState\nterminal_named -> [*]\n"
    )
    assert _terminal_states(formal_model) == {"terminal_named"}


def test_topology_preserves_outer_initial_edges_and_excludes_nested_initial_roots() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    graph = _graph(pair.model)
    assert "AutonomousMode" in graph["[*]"]
    assert "CollisionAvoidance" not in graph["[*]"]


def test_v4_uses_exact_leaf_scope_and_rejects_composite_or_unreachable_scope() -> None:
    registry = load_registry()
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    leaf_refs = [
        state.state_ref
        for state in pair.inspection_facts.states
        if state.name in {"PumpState", "WaterState", "MethaneState"}
    ]
    candidate = _candidate(
        pair,
        predicate_id="V4",
        inputs={"initial_scope": "closed_fcstm_initial_scope", "element_refs": leaf_refs},
        refs=leaf_refs,
    )
    binding = bind_candidate(candidate, pair.model)
    plan = compile_plan(
        candidate,
        binding,
        registry,
        obligation_id="0023:v4-scope",
        round_index=1,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    ).model_copy(update={"supported": True, "formal_program": "fixture", "formal_program_hash": "sha256:" + "0" * 64})
    receipt = run_bounded_verification(plan, pair.model, "0023:v4-receipt")
    assert receipt.verdict == "false"
    assert set(receipt.run_metadata["nonterminal_deadlock_state_refs"]) == set(leaf_refs)

    pair_0029 = load_pair(REPORT_ROOT / "pairs" / "0029")
    collision_ref = next(
        state.state_ref
        for state in pair_0029.inspection_facts.states
        if state.name == "CollisionAvoidance"
    )
    composite_candidate = _candidate(
        pair_0029,
        predicate_id="V4",
        inputs={"initial_scope": "closed_fcstm_initial_scope", "element_refs": [collision_ref]},
        refs=[collision_ref],
    )
    composite_binding = bind_candidate(composite_candidate, pair_0029.model)
    composite_plan = compile_plan(
        composite_candidate,
        composite_binding,
        registry,
        obligation_id="0029:v4-composite",
        round_index=1,
        model=pair_0029.model,
        model_hash=pair_0029.hashes["fcstm"],
    ).model_copy(update={"supported": True, "formal_program": "fixture", "formal_program_hash": "sha256:" + "0" * 64})
    composite_receipt = run_bounded_verification(composite_plan, pair_0029.model, "0029:v4-receipt")
    assert composite_receipt.verdict == "unknown"
    assert "not a deadlock verdict" in composite_receipt.basis


def test_method_prompt_has_no_frozen_ledger_payload() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger = json.loads(
        (
            PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json"
        ).read_text(encoding="utf-8")
    )
    prompt = build_method_prompt(pair, 1, [])
    first_ledger_item = next(iter(ledger["items"].values()))
    assert first_ledger_item["id"] not in prompt
    title = first_ledger_item.get("title")
    if title:
        assert title not in prompt
    assert "reviewer examples" in prompt
    assert "S2={source, target, scope}" in prompt
    assert "set predicate_id to null" in prompt


def test_failed_grounding_fallback_is_unresolved_and_never_fabricates_frontier_issue() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    contract = NLContract(
        contract_id="NL-CONTRACT-NL1",
        segment_id="NL1",
        quote=pair.nl_segments[0].text,
        normative_statement=pair.nl_segments[0].text,
        locus_kind="scope",
        locus_names=("supplied state-machine scope",),
        property="deadlock_freedom",
        state_role="operating_state",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("deadlock_frontier_fact", "verify_fact"),
        binding_hints=(),
        scope="supplied state-machine scope",
        source_refs=("nl:NL1",),
        reason="The fixture preserves the numbered NL segment.",
        basis="numbered NL input closure",
    )
    contracts = NLContractResponse(
        contracts=[contract],
        segment_disposition={"NL1": "covered"},
        reason="The fixture supplies one contract.",
        basis="provider-free contract fixture",
    )
    fallback = fallback_grounding(
        pair,
        lens="behavior_consequence",
        contracts=contracts,
        reason="provider-free fallback fixture",
    )
    assert fallback.candidates == []
    assert fallback.unresolved[0].contract_id == contract.contract_id
    assert fallback.unresolved[0].reason
    assert fallback.unresolved[0].basis
    assert "reachable non-final leaf" in D_SYSTEM_PROMPT
    assert "intentional-terminal alternative is competent only" in D_SYSTEM_PROMPT
    assert "`rebutting+survives`" in D_SYSTEM_PROMPT
    assert "Predicate/backend availability is a W question" in D_SYSTEM_PROMPT
    assert "different root-level initial edge" in D_SYSTEM_PROMPT
    assert "does not create a progress contract" in CONTRACT_SYSTEM_PROMPT
    assert "emit an independent `termination` contract" in CONTRACT_SYSTEM_PROMPT
    assert "covered segment accounting never licenses omission" in CONTRACT_SYSTEM_PROMPT
    assert "source `S` as a child of owner `P`" in CONTRACT_SYSTEM_PROMPT
    assert "complete source-and-alternative group" in CONTRACT_SYSTEM_PROMPT
    assert "first enter ModeA" in CONTRACT_SYSTEM_PROMPT
    assert '"the system begins in Controller" yields owner=root/system' in CONTRACT_SYSTEM_PROMPT
    assert "`system` is the grammatical actor" in CONTRACT_SYSTEM_PROMPT
    assert "an intermediate region or nested composite still satisfies" in CONTRACT_SYSTEM_PROMPT
    assert "broad capability context has not been converted" in CONTRACT_SYSTEM_PROMPT
    assert "common enclosing owner is not itself evidence" in CONTRACT_SYSTEM_PROMPT
    assert "independent `event` and `guard` fields" in CONTRACT_SYSTEM_PROMPT
    assert "Do not relabel that stimulus as a guard" in CONTRACT_SYSTEM_PROMPT
    assert "variable=`setpoint`" in CONTRACT_SYSTEM_PROMPT
    assert "owner-initial-to-ModeA, ModeA-to-ModeB, and ModeB-to-ModeC" in CONTRACT_SYSTEM_PROMPT
    assert "activity to be performed continuously or repeatedly" in CONTRACT_SYSTEM_PROMPT
    assert "segment already has a cardinality or structure contract" in CONTRACT_SYSTEM_PROMPT
    assert "Generic words such as area, section, or part" in CONTRACT_SYSTEM_PROMPT
    assert "simultaneously active partitions" in CONTRACT_SYSTEM_PROMPT
    hint_schema = ContractBindingHint.model_json_schema()
    assert "owns the required initial pseudostate edge" in hint_schema["properties"]["role"]["description"]
    assert "variable names only the data subject" in hint_schema["properties"]["role"]["description"]
    contract_schema = NLContract.model_json_schema()
    assert "grammatical actor" in contract_schema["properties"]["property"]["description"]
    response_schema = NLContractResponse.model_json_schema()
    assert "root-to-substate endpoint" in response_schema["properties"]["contracts"]["description"]
    assert "Emit a candidate only for a possible violated obligation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "treat its typed `owner` binding hint" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "does not satisfy a `Controller -> ModeA`" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "satisfied `root/system -> Controller`" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "already-satisfied owner-local contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Interpret containment at the depth stated by the contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Ground containment only from explicit typed containment contracts" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "synthetic placeholders are not author-specified operating-state" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "an unreachable state that" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "not a deadlock/dead-end violation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "do not by themselves establish `deadlock_freedom`" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "declared consumer with no consumer reachable" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "three independent frontier properties" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "For every supplied `termination` contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "For every transition group with multiple target alternatives" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "canonical author-source inventory" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "complete exact inventory" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "element_refs` contains" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Negative-property carrier example" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "must not emit a cardinality CandidateIssue" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Generic area, section, or part language is insufficient" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Respect protected compiler-macro boundaries" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "member digest, protected" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "not to a descendant action carrier" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    candidate_schema = CandidateIssue.model_json_schema()["properties"]
    assert "missing edge has no ref of its own" in candidate_schema["element_refs"]["description"]
    assert "exact existing carrier transition/state ref" in candidate_schema["element_refs"]["description"]
    grounding_prompt = build_grounding_prompt(
        pair,
        lens="behavior_consequence",
        round_index=1,
        contracts=contracts,
    )
    assert '"state_role": "operating_state"' in grounding_prompt
    assert "exact owner hint" in grounding_prompt
    assert "exact owner-local edge reaches the required target" in grounding_prompt
    assert "Return sparse structured output" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "additional_contracts" in grounding_prompt
    assert "need not predict the runner's canonical ID" in grounding_prompt
    assert "unique within this response" in " ".join(grounding_prompt.split())
    assert '["NL-CONTRACT-NL1"]' in grounding_prompt
    assert "missing edge -> exact endpoint state refs" in grounding_prompt
    assert "Predicate support controls" in grounding_prompt
    assert '"projection_version": "contract-grounding-projection.v2"' in grounding_prompt

    semantic_schema = SemanticAdjudication.model_json_schema()["properties"]
    assert "exact NL terminal clause" in semantic_schema["strongest_defeater"]["description"]
    assert "bare possibility" in semantic_schema["defeater_kind"]["description"]
    assert "survives does not mean merely conceivable" in semantic_schema["defeater_disposition"]["description"]
    assert "declared but unreachable event consumer" in semantic_schema["defeater_kind"]["description"]
    assert "complete exact inventory" in semantic_schema["grounding"]["description"]
    assert "declared event consumer does not rebut" in D_SYSTEM_PROMPT
    assert "Unreachability is not itself a wrong endpoint" in D_SYSTEM_PROMPT

    contract_schema = NLContract.model_json_schema()["properties"]
    assert "does not invent a separate progress contract" in contract_schema["state_role"]["description"]
    response_schema = NLContractResponse.model_json_schema()["properties"]
    assert "without manufacturing progress for every mentioned operating state" in response_schema["contracts"]["description"]
    assert "explicitly continuous or repeated task" in response_schema["contracts"]["description"]
    assert "Every segment marked covered" in response_schema["contracts"]["description"]
    assert "Mark a numbered segment covered only" in CONTRACT_SYSTEM_PROMPT
    assert "closed_model_inventory.states[].ref" in DISCOVERY_GROUNDING_SYSTEM_PROMPT


def test_contract_response_rejects_covered_segment_without_atomic_contract() -> None:
    contract = NLContract(
        contract_id="NL-CONTRACT-NL1",
        segment_id="NL1",
        quote="The controller remains operational.",
        normative_statement="The controller must remain operational.",
        locus_kind="state",
        locus_names=("Controller",),
        property="deadlock_freedom",
        state_role="operating_state",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("deadlock_frontier_fact",),
        binding_hints=(),
        scope="Controller",
        source_refs=("nl:NL1",),
        reason="NL1 states an operating-state progress obligation.",
        basis="provider-free numbered NL fixture",
    )

    with pytest.raises(ValidationError, match="NL2"):
        NLContractResponse(
            contracts=[contract],
            segment_disposition={"NL1": "covered", "NL2": "covered"},
            reason="The malformed correction claims both segments are covered.",
            basis="provider-free incomplete replacement fixture",
        )

    response = NLContractResponse(
        contracts=[contract],
        segment_disposition={"NL1": "covered", "NL2": "context"},
        reason="Only the normative segment is covered by a contract.",
        basis="provider-free exact segment accounting fixture",
    )
    assert response.segment_disposition["NL2"] == "context"


def test_grounding_response_uses_sparse_unresolved_without_full_disposition_table() -> None:
    response = GroundingResponse(
        lens="contract_structure_contrast",
        candidates=[],
        unresolved=[],
        reason="The fixture found no branch-local issue or uncertainty.",
        basis="provider-free sparse grounding fixture",
    )
    assert response.candidates == []
    assert response.unresolved == []
    assert "contract_dispositions" not in response.model_dump(mode="json")

    with pytest.raises(ValidationError, match="both a candidate and unresolved"):
        GroundingResponse(
            lens="contract_structure_contrast",
            candidates=[
                CandidateIssue(
                    contract_id="NL-CONTRACT-NL1",
                    locus_kind="state",
                    locus_names=("Controller",),
                    property="deadlock_freedom",
                    violation_direction="dead_end",
                    evidence_types=("deadlock_frontier_fact",),
                    title="Controller cannot progress",
                    requirement_quote="Controller must progress.",
                    predicate_id=None,
                    predicate_inputs={},
                    element_refs=[],
                    source_refs=["nl:NL1"],
                    expected="Controller progresses.",
                    observed="No exact continuation could be bound.",
                    strongest_rebuttal="The binding may be incomplete.",
                    reason="The fixture emits one candidate.",
                    basis="provider-free sparse accounting fixture",
                )
            ],
            unresolved=[
                GroundingUnresolved(
                    contract_id="NL-CONTRACT-NL1",
                    reason="The same contract was also marked unresolved.",
                    basis="provider-free malformed sparse accounting fixture",
                )
            ],
            reason="The fixture deliberately overlaps sparse rows.",
            basis="provider-free validation fixture",
        )


def test_grounding_runtime_schema_closes_contract_references() -> None:
    supplied_contract = NLContract(
        contract_id="NL-CONTRACT-NL1",
        segment_id="NL1",
        quote="The controller must remain operational.",
        normative_statement="The controller must remain operational.",
        locus_kind="state",
        locus_names=("Controller",),
        property="deadlock_freedom",
        state_role="operating_state",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=("deadlock_frontier_fact",),
        scope="Controller",
        source_refs=("nl:NL1",),
        reason="The numbered segment establishes an operating obligation.",
        basis="provider-free exact grounding schema fixture NL1",
    )
    action_contract = NLContract(
        contract_id="NL-CONTRACT-NL3-ACTION-1",
        segment_id="NL3",
        quote="The controller shall update the display.",
        normative_statement="The controller must update the display.",
        locus_kind="action",
        locus_names=("update display",),
        property="state_action",
        expected_direction="must_occur",
        violation_direction="missing",
        evidence_types=("action_fact",),
        scope="Controller",
        source_refs=("nl:NL3",),
        reason="The numbered segment establishes one action obligation.",
        basis="provider-free exact grounding schema fixture NL3",
    )
    schema = _grounding_response_contract(
        [supplied_contract, action_contract]
    )
    projected_schema = schema.model_json_schema()
    assert "supplied contract set" in projected_schema["description"]
    assert "never invent an *-UNDECLARED" in (
        projected_schema["properties"]["unresolved"]["description"]
    )

    valid = schema(
        lens="behavior_consequence",
        unresolved=[
            GroundingUnresolved(
                contract_id="NL-CONTRACT-NL3-ACTION-1",
                reason="The supplied action contract lacks an exact carrier.",
                basis="provider-free supplied-contract closure fixture",
            )
        ],
        reason="The fixture returns one supplied unresolved identity.",
        basis="provider-free exact grounding response schema",
    )
    assert valid.unresolved[0].contract_id == "NL-CONTRACT-NL3-ACTION-1"

    local_contract = NLContract(
        contract_id="NL-CONTRACT-NL2-DERIVED-LOCAL-REACHABILITY",
        segment_id="NL2",
        quote="The operating scope must perform its task.",
        normative_statement="The required operating scope must be reachable.",
        locus_kind="state",
        locus_names=("OperatingScope",),
        property="reachability",
        state_role="operating_state",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("reachability_fact",),
        binding_hints=(),
        scope="closed model root",
        source_refs=("nl:NL2",),
        reason="Cross-view facts expose one derived reachability obligation.",
        basis="provider-free same-response additional contract fixture",
    )
    local_candidate = CandidateIssue(
        contract_id=local_contract.contract_id,
        locus_kind="state",
        locus_names=("OperatingScope",),
        property="reachability",
        violation_direction="unreachable",
        evidence_types=("reachability_fact",),
        title="Operating scope is unreachable",
        requirement_quote=local_contract.quote,
        predicate_id=None,
        predicate_inputs={},
        element_refs=("state:OperatingScope",),
        source_refs=("nl:NL2",),
        expected="OperatingScope is reachable from root.",
        observed="The exact closed graph has no root path to OperatingScope.",
        strongest_rebuttal="No supplied alternative root satisfies this scope.",
        reason="The local candidate references its typed derived contract.",
        basis="provider-free same-response reference-closure fixture",
    )
    local_valid = schema(
        lens="behavior_consequence",
        additional_contracts=[local_contract],
        candidates=[local_candidate],
        reason="The fixture returns one valid branch-local derived candidate.",
        basis="provider-free exact grounding response schema",
    )
    assert local_valid.candidates[0].contract_id == local_contract.contract_id

    with pytest.raises(
        ValidationError,
        match=r"unresolved\[0\]\.contract_id='NL-CONTRACT-NL2-ACTION-UNDECLARED'",
    ):
        schema(
            lens="behavior_consequence",
            unresolved=[
                GroundingUnresolved(
                    contract_id="NL-CONTRACT-NL2-ACTION-UNDECLARED",
                    reason="No unresolved row should be emitted.",
                    basis="provider-free invented-ID negative fixture",
                )
            ],
            reason="The fixture reproduces the 0053 invented unresolved ID.",
            basis="provider-free exact grounding response schema",
        )


def test_grounding_runtime_schema_allows_empty_supplied_contract_set() -> None:
    schema = _grounding_response_contract([])
    empty = schema(
        lens="contract_structure_contrast",
        reason="The NL-only stage supplied no atomic contract to this lens.",
        basis="provider-free empty supplied-contract fixture",
    )
    assert empty.additional_contracts == []

    derived = NLContract(
        contract_id="NL-CONTRACT-NL1-DERIVED-REACHABILITY",
        segment_id="NL1",
        quote="The controller enters its operating mode.",
        normative_statement="The operating mode must be reachable.",
        locus_kind="state",
        locus_names=("OperatingMode",),
        property="reachability",
        state_role="operating_state",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("reachability_fact",),
        scope="closed model root",
        source_refs=("nl:NL1",),
        reason="Cross-view facts establish one implicit reachability obligation.",
        basis="provider-free empty supplied-contract fixture NL1",
    )
    accepted = schema(
        lens="behavior_consequence",
        additional_contracts=[derived],
        unresolved=[
            GroundingUnresolved(
                contract_id=derived.contract_id,
                reason="The derived obligation has no exact source binding.",
                basis="provider-free same-response identity closure",
            )
        ],
        reason="The lens derives and references one local contract.",
        basis="provider-free empty supplied-contract fixture",
    )
    assert accepted.unresolved[0].contract_id == derived.contract_id

    with pytest.raises(ValidationError, match="is not a supplied contract"):
        schema(
            lens="behavior_consequence",
            unresolved=[
                GroundingUnresolved(
                    contract_id="NL-CONTRACT-NL1-DERIVED-INVENTED",
                    reason="The fixture invents an undeclared identity.",
                    basis="provider-free negative identity fixture",
                )
            ],
            reason="The fixture must reject an invented identity.",
            basis="provider-free empty supplied-contract fixture",
        )


def test_grounding_runtime_schema_requires_explicit_cardinality_accounting() -> None:
    cardinality_contract = NLContract(
        contract_id="NL-CONTRACT-NL2-CARDINALITY-1",
        segment_id="NL2",
        quote="The model shall have three concurrent state areas.",
        normative_statement="The operating scope must have three concurrent UML regions.",
        locus_kind="composite",
        locus_names=("OperatingScope",),
        property="cardinality",
        expected_direction="must_cover",
        violation_direction="missing",
        evidence_types=("source_identity", "containment_fact", "semantic_comparison"),
        cardinality_requirement=CardinalityRequirement(
            required_count=3,
            member_domain="unresolved",
            scope_concept="OperatingScope",
            member_concept="concurrent state areas",
            reason="The NL fixes a count while leaving the primary typed domain for grounding.",
            basis="provider-free cardinality fixture NL2",
        ),
        scope="OperatingScope",
        source_refs=("nl:NL2",),
        reason="The numbered segment establishes one cardinality obligation.",
        basis="provider-free exact cardinality coverage fixture",
    )
    non_cardinality_contract = cardinality_contract.model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL3-ACTION-1",
            "segment_id": "NL3",
            "quote": "The operating scope shall perform its task.",
            "normative_statement": "The operating scope must perform its task.",
            "locus_kind": "action",
            "locus_names": ("perform task",),
            "property": "state_action",
            "expected_direction": "must_occur",
            "violation_direction": "missing",
            "evidence_types": ("action_fact",),
            "cardinality_requirement": None,
            "source_refs": ("nl:NL3",),
        }
    )
    schema = _grounding_response_contract(
        [cardinality_contract, non_cardinality_contract]
    )
    projected_schema = schema.model_json_schema()
    cardinality_description = projected_schema["properties"][
        "cardinality_bindings"
    ]["description"]
    assert "exhaustive" in cardinality_description
    assert cardinality_contract.contract_id in cardinality_description
    assert schema.expected_cardinality_contract_ids == (
        cardinality_contract.contract_id,
    )

    with pytest.raises(
        ValidationError,
        match=(
            "cardinality_bindings is missing one required exact/ambiguous/"
            "unbound row.*NL-CONTRACT-NL2-CARDINALITY-1"
        ),
    ):
        schema(
            lens="contract_structure_contrast",
            reason="The malformed fixture silently omits cardinality accounting.",
            basis="provider-free missing-cardinality-row fixture",
        )

    for status in ("ambiguous", "unbound"):
        response = schema(
            lens="behavior_consequence",
            cardinality_bindings=[
                CardinalityDomainBinding(
                    binding_id=f"CARD-BIND-{status.upper()}",
                    contract_id=cardinality_contract.contract_id,
                    status=status,
                    member_domain="unresolved",
                    owner_source_id=None,
                    owner_model_ref=None,
                    reason=f"The fixture records an explicit {status} reading.",
                    basis="provider-free explicit unresolved-domain fixture",
                )
            ],
            reason="The fixture explicitly accounts for the cardinality contract.",
            basis="provider-free exact cardinality coverage fixture",
        )
        assert response.cardinality_bindings[0].status == status

    exact = schema(
        lens="contract_structure_contrast",
        cardinality_bindings=[
            CardinalityDomainBinding(
                binding_id="CARD-BIND-EXACT",
                contract_id=cardinality_contract.contract_id,
                status="exact",
                member_domain="concurrent_regions",
                owner_source_id="source:OperatingScope",
                owner_model_ref="state:OperatingScope",
                alternative_reading="Three operating child states are a weaker reading.",
                reason="The supplied semantics selects UML structural regions under one exact owner.",
                basis="provider-free exact concurrent-region fixture",
            )
        ],
        reason="The fixture closes the cardinality member domain and owner.",
        basis="provider-free exact cardinality coverage fixture",
    )
    assert exact.cardinality_bindings[0].member_domain == "concurrent_regions"

    with pytest.raises(
        ValidationError,
        match="property is not cardinality.*NL-CONTRACT-NL3-ACTION-1",
    ):
        schema(
            lens="contract_structure_contrast",
            cardinality_bindings=[
                exact.cardinality_bindings[0].model_copy(
                    update={"contract_id": non_cardinality_contract.contract_id}
                )
            ],
            reason="The malformed fixture targets a non-cardinality contract.",
            basis="provider-free wrong-property cardinality fixture",
        )

    fixture_outcome = FixtureStructuredRuntime().call(
        kind="discovery_grounding",
        schema=schema,
        system_prompt=DISCOVERY_GROUNDING_SYSTEM_PROMPT,
        prompt="provider-free dynamic grounding schema fixture",
        artifact_id="method/0046/round-1/discovery-grounding/behavior_consequence",
    )
    assert fixture_outcome.succeeded
    assert len(fixture_outcome.response.cardinality_bindings) == 1
    assert fixture_outcome.response.cardinality_bindings[0].status == "unbound"
    assert fixture_outcome.response.candidates == []

    failed_lens = fallback_grounding(
        SimpleNamespace(),
        lens="contract_structure_contrast",
        contracts=NLContractResponse(
            contracts=[cardinality_contract],
            segment_disposition={"NL2": "covered"},
            reason="The fixture supplies one cardinality contract.",
            basis="provider-free fallback cardinality fixture",
        ),
        reason="provider-free simulated grounding failure",
    )
    assert len(failed_lens.cardinality_bindings) == 1
    assert failed_lens.cardinality_bindings[0].status == "unbound"
    assert failed_lens.candidates == []

    non_cardinality_schema = _grounding_response_contract(
        [non_cardinality_contract]
    )
    non_cardinality_response = non_cardinality_schema(
        lens="contract_structure_contrast",
        reason="No cardinality contract is supplied.",
        basis="provider-free non-cardinality fixture",
    )
    assert non_cardinality_response.cardinality_bindings == []


def test_branch_local_additional_contracts_merge_by_canonical_typed_identity() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    segment = pair.nl_segments[0]
    base_contract = NLContract(
        contract_id=f"NL-CONTRACT-{segment.segment_id}",
        segment_id=segment.segment_id,
        quote=segment.text,
        normative_statement=segment.text,
        locus_kind="state",
        locus_names=(pair.model.states[0].name,),
        property="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        evidence_types=("initial_entry_fact",),
        binding_hints=(),
        scope="closed model root",
        source_refs=(f"nl:{segment.segment_id}",),
        reason="The base fixture preserves one source obligation.",
        basis="provider-free numbered NL fixture",
    )
    contracts = NLContractResponse(
        contracts=[base_contract],
        segment_disposition={segment.segment_id: "covered"},
        reason="The fixture contains one base contract.",
        basis="provider-free contract fixture",
    )
    derived_id = (
        f"NL-CONTRACT-{segment.segment_id}-OPERATING-1-"
        "DERIVED-behavior_consequence-ROOT-REACHABILITY"
    )
    derived = NLContract(
        contract_id=derived_id,
        segment_id=segment.segment_id,
        quote=segment.text,
        normative_statement="The required operating scope must be reachable from root.",
        locus_kind="state",
        locus_names=(pair.model.states[-1].name,),
        property="reachability",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("reachability_fact", "verify_fact"),
        binding_hints=(
            ContractBindingHint(
                role="state",
                value=pair.model.states[-1].name,
                source_ref=f"nl:{segment.segment_id}",
                reason="The first lens binds the required operating state.",
                basis="provider-free first-lens rationale",
            ),
        ),
        scope="closed model root",
        source_refs=(f"nl:{segment.segment_id}",),
        reason="Cross-view facts expose a separate root-reachability obligation.",
        basis="provider-free exact source and ModelIR fixture",
    )
    first = GroundingResponse(
        lens="behavior_consequence",
        additional_contracts=[derived],
        candidates=[],
        reason="The behavior lens derives one causal contract.",
        basis="provider-free branch-local contract fixture",
    )
    normalized_first, first_receipts = canonicalize_grounding_response(first)
    canonical_id = normalized_first.additional_contracts[0].contract_id
    assert canonical_id != derived_id
    assert first_receipts[0].raw_contract_id == derived_id
    assert first_receipts[0].canonical_contract_id == canonical_id

    merged, diagnostics = _merge_grounding_contracts(
        pair, contracts, [normalized_first]
    )
    assert merged[canonical_id].property == "reachability"
    assert merged[base_contract.contract_id].property == "initial_entry"
    assert diagnostics == []

    agreeing_contract = derived.model_copy(
        update={
            "reason": "The second lens independently derives the same typed obligation.",
            "basis": "provider-free second-lens rationale",
            "binding_hints": (
                derived.binding_hints[0].model_copy(
                    update={
                        "reason": "The second lens explains the same exact state binding differently.",
                        "basis": "provider-free second-lens hint rationale",
                    }
                ),
            ),
        }
    )
    agreeing = first.model_copy(
        update={
            "lens": "contract_structure_contrast",
            "additional_contracts": [agreeing_contract],
        }
    )
    normalized_agreeing, agreeing_receipts = canonicalize_grounding_response(agreeing)
    assert normalized_agreeing.additional_contracts[0].contract_id == canonical_id
    assert agreeing_receipts[0].canonical_contract_id == canonical_id
    merged, diagnostics = _merge_grounding_contracts(
        pair, contracts, [normalized_first, normalized_agreeing]
    )
    assert merged[canonical_id].property == "reachability"
    assert diagnostics == []

    conflicting = derived.model_copy(
        update={
            "locus_names": (pair.model.states[0].name,),
            "reason": "The second lens assigns a different exact locus.",
        }
    )
    second = GroundingResponse(
        lens="contract_structure_contrast",
        additional_contracts=[conflicting],
        candidates=[],
        unresolved=[
            GroundingUnresolved(
                contract_id="NL-CONTRACT-NL999-DERIVED-UNKNOWN",
                reason="The fixture names an unavailable contract.",
                basis="provider-free unknown-ID fixture",
            )
        ],
        reason="The source lens deliberately conflicts for validation.",
        basis="provider-free conflict fixture",
    )
    normalized_second, second_receipts = canonicalize_grounding_response(second)
    conflicting_id = normalized_second.additional_contracts[0].contract_id
    assert conflicting_id != canonical_id
    assert second_receipts[0].raw_contract_id == derived_id
    merged, diagnostics = _merge_grounding_contracts(
        pair, contracts, [normalized_first, normalized_second]
    )
    assert canonical_id in merged
    assert conflicting_id in merged
    assert {item["class"] for item in diagnostics} == {
        "unknown_unresolved_contract_id",
    }


def test_g1_flattens_list_valued_source_and_target_inputs() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    target = next(
        item.name for item in pair.model.states if item.name == "CollisionAvoidance"
    )
    plan = PredicatePlan(
        plan_id="provider-free:g1:list-inputs",
        predicate_id="G1",
        registry_version="four-family-19-core.v1",
        inputs={"source": [["[*]"]], "target": [[target]]},
        soundness_fragment="finite closed-graph reachability",
        assumptions=("closed FCSTM",),
        formal_program="ASSERT G1",
        formal_program_hash="sha256:provider-free",
        supported=True,
        reason="The fixture exercises exact list-valued topology inputs.",
        basis="provider-free topology input-normalization regression",
        source_gate_passed=True,
    )

    receipt = run_topology(plan, pair.model, "provider-free:g1:list-inputs:receipt")

    assert receipt.terminal_state == "completed"
    assert receipt.verdict in {"true", "false"}
    if receipt.verdict == "false":
        assert receipt.counterexample == [
            {"sources": ["[*]"], "targets": [target]}
        ]


def test_unsupported_backend_does_not_turn_satisfied_semantics_into_d1() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(pair, predicate_id=None, inputs={})
    binding = bind_candidate(candidate, pair.model)
    semantic = SemanticAdjudication(
        obligation_id="0000:r1:i0",
        grounding="not_established",
        violated_obligation="The supplied property is under review.",
        strongest_defeater="The exact supplied facts satisfy the expected property.",
        defeater_kind="rebutting",
        defeater_disposition="survives",
        reason="The semantic facts satisfy the obligation; backend availability is irrelevant to D.",
        basis="provider-free exact semantic fixture",
    )
    receipt = RawReceipt(
        receipt_id="0000:r1:i0:receipt",
        backend="none",
        terminal_state="unsupported",
        verdict="unknown",
        reason="No frozen predicate expresses the claim.",
        basis="deterministic backend capability table",
    )

    decision = adjudicate_disposition(candidate, binding, semantic, receipt)

    assert binding.precise is True
    assert decision["d_level"] == "D0"


def test_d_validation_rejects_unreachability_recast_as_bound_state_dead_end() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0035")
    state = pair.model.state("DoorShut")
    assert state is not None
    outgoing_refs = [
        transition.ref
        for transition in pair.model.transitions
        if transition.source == state.name
    ]
    assert outgoing_refs
    candidate = _candidate(
        pair,
        predicate_id="V4",
        inputs={"initial_scope": "closed_fcstm_hierarchy"},
        refs=[state.ref, *outgoing_refs],
    ).model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL1-PROGRESS-1",
            "locus_kind": "state",
            "locus_names": ("DoorShut",),
            "property": "deadlock_freedom",
            "violation_direction": "dead_end",
        }
    )
    binding = bind_candidate(candidate, pair.model)
    established = SemanticAdjudication(
        obligation_id="0035:r1:i0",
        grounding="established",
        violated_obligation="DoorShut must not be a dead end.",
        strongest_defeater=None,
        defeater_kind="none",
        defeater_disposition="defeated",
        reason="The fixture intentionally recasts unreachability as a dead end.",
        basis="provider-free contradictory D fixture",
    )

    errors = _d_decision_consistency_errors(
        established,
        prepared={"candidate": candidate, "binding": binding},
        pair=pair,
    )

    assert any("outgoing-transition inventory" in error for error in errors)
    assert any("unreachability is not a local dead-end" in error for error in errors)


def test_d_validation_rejects_declared_but_unreachable_consumer_as_rebuttal() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    assert pair.inspection_facts is not None
    event_facts = [
        fact
        for fact in pair.inspection_facts.event_consumers
        if fact.declared_ref is not None
        and fact.consumer_transition_refs
        and not fact.reachable_consumer_transition_refs
    ][:2]
    assert len(event_facts) == 2
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL4-EVENT-CONSUMER",
        locus_kind="scope",
        locus_names=("UAV swarm operating scope",),
        property="event_consumer_coverage",
        violation_direction="unconsumed",
        evidence_types=("event_consumer_fact", "reachability_fact"),
        title="Required event has no reachable consumer",
        requirement_quote="The supplied event must be consumed during operation.",
        predicate_id=None,
        predicate_inputs={},
        element_refs=[
            ref
            for fact in event_facts
            for ref in (fact.declared_ref, *fact.consumer_transition_refs)
        ],
        source_refs=["NL4"],
        expected="At least one consumer is reachable in the required scope.",
        observed="All exact consumer transition sources for the aggregated events are unreachable.",
        strongest_rebuttal="The event declaration and consumer transitions exist.",
        reason="The fixture binds declaration separately from operational reachability.",
        basis="provider-free 0046 inspection-equivalent event-consumer facts",
    )
    binding = bind_candidate(candidate, pair.model)
    assert binding.precise is True
    invalid = SemanticAdjudication(
        obligation_id="0046:r1:i0",
        grounding="established",
        violated_obligation="The required event has no reachable consumer.",
        strongest_defeater="A declaration and unreachable consumer exist.",
        defeater_kind="rebutting",
        defeater_disposition="survives",
        reason="The fixture deliberately treats declaration as satisfaction.",
        basis="provider-free contradictory D fixture",
    )

    errors = _d_decision_consistency_errors(
        invalid,
        prepared={"candidate": candidate, "binding": binding},
        pair=pair,
    )

    assert any("declaration-only presence cannot rebut" in error for error in errors)


def test_structured_models_require_non_empty_audit_rationale_and_descriptions() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    candidate = _candidate(pair, predicate_id="S1", inputs={})
    invalid_candidate = candidate.model_dump(mode="json")
    invalid_candidate["reason"] = "   "
    with pytest.raises(ValidationError):
        CandidateIssue.model_validate(invalid_candidate)
    with pytest.raises(ValidationError):
        MethodResponse(issues=[], reason="   ", basis="valid basis")

    english_rationale = MethodResponse(
        issues=[],
        reason="The fixture has no reportable issue.",
        basis="Provider-free typed model fixture.",
    )
    assert english_rationale.reason == "The fixture has no reportable issue."
    assert english_rationale.basis == "Provider-free typed model fixture."

    candidate_schema = CandidateIssue.model_json_schema()
    method_schema = MethodResponse.model_json_schema()
    candidate_properties = candidate_schema["properties"]
    for field_name in (
        "contract_id", "locus_kind", "locus_names", "property",
        "violation_direction", "evidence_types", "title", "requirement_quote",
        "predicate_id", "predicate_inputs", "element_refs",
        "source_refs", "expected", "observed", "strongest_rebuttal", "reason", "basis",
    ):
        assert candidate_properties[field_name].get("description"), field_name
    for schema in (method_schema,):
        for field_name, field in schema["properties"].items():
            assert field.get("description"), field_name
    cardinality_schema = CardinalityDomainBinding.model_json_schema()
    assert "Do not descend to a deeper child composite" in cardinality_schema[
        "properties"
    ]["owner_source_id"]["description"]
    assert "contract's normative `scope_concept`" in (
        DISCOVERY_GROUNDING_SYSTEM_PROMPT
    )
    for model in (
        SourceProvenance,
        RunManifest,
        MethodCellReceipt,
        PairRunStatus,
        RunSummaryReceipt,
        ContextBudgetReceipt,
        ContractBindingHint,
        NLContract,
        NLTransitionAlternative,
        NLTransitionGroup,
        GroundingUnresolved,
        W2AuditBundle,
    ):
        schema = model.model_json_schema()
        assert model.__doc__ and model.__doc__.strip()
        for field_name, field in schema["properties"].items():
            assert field.get("description"), f"{model.__name__}.{field_name}"



def test_all_evidence_discovery_pydantic_models_have_docs_and_field_descriptions() -> None:
    module_names = (
        "pipeline.evidence_discovery.inputs.models",
        "pipeline.evidence_discovery.inputs.context",
        "pipeline.evidence_discovery.semantics.binding",
        "pipeline.evidence_discovery.semantics.obligations",
        "pipeline.evidence_discovery.semantics.adjudication",
        "pipeline.evidence_discovery.semantics.workflow",
        "pipeline.evidence_discovery.semantics.frontier",
        "pipeline.evidence_discovery.orchestration.contracts",
        "pipeline.evidence_discovery.orchestration.runtime",
        "pipeline.evidence_discovery.orchestration.runner",
        "pipeline.evidence_discovery.evidence.audit_bundle",
    )
    checked = 0
    for module_name in module_names:
        module = import_module(module_name)
        for value in vars(module).values():
            if (
                not isinstance(value, type)
                or value is BaseModel
                or not issubclass(value, BaseModel)
                or value.__module__ != module_name
            ):
                continue
            checked += 1
            assert value.__doc__ and value.__doc__.strip(), value.__name__
            for field_name, field in value.model_json_schema().get(
                "properties", {}
            ).items():
                assert field.get("description"), f"{value.__name__}.{field_name}"
    assert checked >= 50


def test_candidate_must_preserve_exact_typed_contract_semantic_key() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    transition = pair.model.transitions[0]
    contract = NLContract(
        contract_id="NL-CONTRACT-FIXTURE-TRANSITION",
        segment_id="NL1",
        quote="A synthetic controller shall transition from SourceA to TargetA.",
        normative_statement="The synthetic transition shall exist.",
        locus_kind="transition",
        locus_names=("SourceA", "TargetA"),
        property="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        evidence_types=("transition_fact",),
        binding_hints=(
            ContractBindingHint(
                role="source",
                value="SourceA",
                source_ref="NL1",
                reason="The fixture binds the exact normative transition source.",
                basis="provider-free synthetic source binding",
            ),
            ContractBindingHint(
                role="target",
                value="TargetA",
                source_ref="NL1",
                reason="The fixture binds the exact normative transition target.",
                basis="provider-free synthetic target binding",
            ),
        ),
        scope="Synthetic controller scope",
        source_refs=("nl:NL1",),
        reason="The synthetic fixture supplies one atomic endpoint obligation.",
        basis="provider-free synthetic contract",
    )
    candidate = _candidate(
        pair,
        predicate_id="S2",
        inputs={
            "source": transition.source,
            "target": transition.target,
            "scope": "closed_fcstm",
        },
        refs=[transition.ref],
    ).model_copy(
        update={
            "contract_id": contract.contract_id,
            "locus_names": contract.locus_names,
        }
    )
    exact = _prepare_candidate(
        pair,
        candidate,
        1,
        0,
        {contract.contract_id: contract},
    )
    assert exact["binding"].precise is True

    reversed_property = candidate.model_copy(
        update={
            "property": "initial_entry",
            "violation_direction": "wrong_target",
        }
    )
    rejected = _prepare_candidate(
        pair,
        reversed_property,
        1,
        1,
        {contract.contract_id: contract},
    )
    assert rejected["binding"].precise is False
    assert "property" in rejected["binding"].basis
    assert "violation_direction" in rejected["binding"].basis


def test_source_owned_ref_does_not_poison_exact_fcstm_binding() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    searching = pair.model.state("Searching")
    assert searching is not None
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL2-ACTION-1",
        locus_kind="action",
        locus_names=("UAV swarm target search",),
        property="state_action",
        violation_direction="other",
        evidence_types=("source_identity", "action_fact"),
        title="Continuous target-search action lacks executable evidence",
        requirement_quote="The swarm continuously performs target search tasks.",
        predicate_id=None,
        predicate_inputs={},
        element_refs=[
            searching.ref,
            "source:body:UAVSwarmStateMachine.SearchRegion.Searching:2",
        ],
        source_refs=["NL2"],
        expected="Searching owns the required target-search action.",
        observed="The exact closed-model state has no lifecycle action.",
        strongest_rebuttal="A source label alone does not establish executable behavior.",
        reason="The candidate binds the semantic action gap to the exact closed-model state.",
        basis="NL2, exact author-source body ref, and FCSTM state action inventory.",
    )

    prepared = _prepare_candidate(pair, candidate, 1, 0)

    assert prepared["binding"].precise is True
    assert prepared["candidate"].element_refs == [searching.ref]
    assert (
        "source:body:UAVSwarmStateMachine.SearchRegion.Searching:2"
        in prepared["candidate"].source_refs
    )


def test_0029_contract_shape_rejects_bundled_transition_alternatives() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    segment = next(item for item in pair.nl_segments if item.segment_id == "NL2")
    common = {
        "contract_id": "NL-CONTRACT-NL2-BUNDLED",
        "segment_id": segment.segment_id,
        "quote": segment.text,
        "normative_statement": "InitialState must select one of two guarded destinations.",
        "locus_kind": "transition",
        "locus_names": ("InitialState", "HighwayMode", "UrbanMode"),
        "property": "guard",
        "expected_direction": "must_exist",
        "violation_direction": "missing",
        "evidence_types": ("source_identity", "transition_fact", "guard_fact"),
        "scope": "AutonomousMode initialization",
        "source_refs": (segment.segment_id,),
        "reason": "The fixture reproduces a structurally bundled contract row.",
        "basis": "0029 numbered NL input without ledger or judge data",
    }
    with pytest.raises(ValidationError, match="split independently violable endpoints"):
        NLContract(
            **common,
            binding_hints=(
                ContractBindingHint(
                    role="source",
                    value="InitialState",
                    source_ref=segment.segment_id,
                    reason="The source state is explicit.",
                    basis=segment.segment_id,
                ),
                ContractBindingHint(
                    role="target",
                    value="HighwayMode",
                    source_ref=segment.segment_id,
                    reason="The first destination is explicit.",
                    basis=segment.segment_id,
                ),
                ContractBindingHint(
                    role="target",
                    value="UrbanMode",
                    source_ref=segment.segment_id,
                    reason="The second destination is independently violable.",
                    basis=segment.segment_id,
                ),
            ),
        )

    split = NLContract(
        **{
            **common,
            "contract_id": "NL-CONTRACT-NL2-HIGHWAY-ENDPOINT",
            "normative_statement": "InitialState must transition to HighwayMode.",
            "locus_names": ("InitialState", "HighwayMode"),
            "property": "transition_endpoints",
        },
        binding_hints=(
            ContractBindingHint(
                role="source",
                value="InitialState",
                source_ref=segment.segment_id,
                reason="The source state is explicit.",
                basis=segment.segment_id,
            ),
            ContractBindingHint(
                role="target",
                value="HighwayMode",
                source_ref=segment.segment_id,
                reason="This contract has one exact destination.",
                basis=segment.segment_id,
            ),
        ),
    )
    assert split.property == "transition_endpoints"
    assert [hint.role for hint in split.binding_hints] == ["source", "target"]

    transition_group = NLTransitionGroup(
        group_id="NL-GROUP-NL2-INITIALSTATE-CHOICE",
        segment_id=segment.segment_id,
        source_name="InitialState",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL2-HIGHWAY",
                target_name="HighwayMode",
                guard="high_way=true",
                source_refs=(segment.segment_id,),
                reason="The first destination has its own normative condition.",
                basis="provider-free NL2 transition-group fixture",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL2-URBAN",
                target_name="UrbanMode",
                guard="urban_way=true",
                source_refs=(segment.segment_id,),
                reason="The second destination has its own normative condition.",
                basis="provider-free NL2 transition-group fixture",
            ),
        ),
        source_refs=(segment.segment_id,),
        reason="Both target alternatives share the same semantically stated source.",
        basis="provider-free NL2 discourse fixture",
    )
    grouped = NLContractResponse(
        contracts=[split],
        transition_groups=[transition_group],
        segment_disposition={segment.segment_id: "covered"},
        reason="The response preserves both an atomic endpoint and its relation group.",
        basis="provider-free transition-group fixture",
    )
    assert len(grouped.transition_groups[0].alternatives) == 2
    compact_prompt = build_grounding_prompt(
        pair,
        lens="contract_structure_contrast",
        round_index=1,
        contracts=grouped,
    )
    assert '"group_id": "NL-GROUP-NL2-INITIALSTATE-CHOICE"' in compact_prompt
    assert '"alternative_id": "ALT-NL2-HIGHWAY"' in compact_prompt
    assert "compare all alternatives as one relation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT


def test_0029_local_exit_target_survives_typed_contract_projection() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    nl4 = next(item for item in pair.nl_segments if item.segment_id == "NL4")
    nl6 = next(item for item in pair.nl_segments if item.segment_id == "NL6")

    def endpoint_contract(
        contract_id: str,
        *,
        segment_id: str,
        quote: str,
        source: str,
        target: str,
        guard: str,
    ) -> NLContract:
        return NLContract(
            contract_id=contract_id,
            segment_id=segment_id,
            quote=quote,
            normative_statement=f"{source} must transition to {target} when {guard}.",
            locus_kind="transition",
            locus_names=(source, target),
            property="transition_endpoints",
            expected_direction="must_exist",
            violation_direction="wrong_target",
            evidence_types=("source_identity", "transition_fact", "semantic_comparison"),
            binding_hints=(
                ContractBindingHint(
                    role="source",
                    value=source,
                    source_ref=segment_id,
                    reason="The numbered segment states the transition source.",
                    basis=segment_id,
                ),
                ContractBindingHint(
                    role="target",
                    value=target,
                    source_ref=segment_id,
                    reason="The numbered segment states this normative target role.",
                    basis=segment_id,
                ),
                ContractBindingHint(
                    role="guard",
                    value=guard,
                    source_ref=segment_id,
                    reason="The numbered segment attaches this condition to the endpoint.",
                    basis=segment_id,
                ),
            ),
            scope="HighwayMode",
            source_refs=(segment_id,),
            reason="The fixture preserves the segment-local target before model grounding.",
            basis="provider-free numbered NL contract fixture",
        )

    local_exit = endpoint_contract(
        "NL-CONTRACT-NL4-LOCAL-EXIT",
        segment_id="NL4",
        quote=nl4.text,
        source="lane_change",
        target="HighwayMode local exit",
        guard="dist_to_exit<2",
    )
    later_termination = endpoint_contract(
        "NL-CONTRACT-NL6-TERMINATION-TARGET",
        segment_id="NL6",
        quote=nl6.text,
        source="HighwayMode",
        target="FinishState",
        guard="auto_finished=true",
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL4-LOCAL-EXIT",
        segment_id="NL4",
        source_name="lane_change",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL4-CRUISE",
                target_name="cruise",
                guard="lane change completed",
                source_refs=("NL4",),
                reason="NL4 states the return-to-cruise alternative.",
                basis="provider-free NL4 transition-group fixture",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL4-LOCAL-EXIT",
                target_name="HighwayMode local exit",
                guard="dist_to_exit<2",
                source_refs=("NL4",),
                reason="NL4 states a local highway-exit role without naming FinishState.",
                basis="provider-free NL4 transition-group fixture",
            ),
        ),
        source_refs=("NL4",),
        reason="NL4 gives two distinct alternatives from lane_change.",
        basis="provider-free NL4 discourse fixture",
    )
    response = NLContractResponse(
        contracts=(local_exit, later_termination),
        transition_groups=(group,),
        segment_disposition={"NL4": "covered", "NL6": "covered"},
        reason="The fixture keeps local exit and later termination as distinct concepts.",
        basis="provider-free target-identity fixture",
    )

    validated = NLContractResponse.model_validate(response.model_dump(mode="json"))
    local_target = next(
        hint.value
        for hint in validated.contracts[0].binding_hints
        if hint.role == "target"
    )
    termination_target = next(
        hint.value
        for hint in validated.contracts[1].binding_hints
        if hint.role == "target"
    )
    assert local_target == "HighwayMode local exit"
    assert termination_target == "FinishState"
    assert local_target != termination_target
    assert validated.transition_groups[0].alternatives[1].target_name == local_target

    schema = NLContractResponse.model_json_schema()
    defs = schema["$defs"]
    assert "current numbered segment" in defs["ContractBindingHint"]["properties"][
        "value"
    ]["description"]
    assert "may not rewrite an explicit local-exit" in defs[
        "NLTransitionAlternative"
    ]["properties"]["target_name"]["description"]
    assert "may not rewrite a local-exit" in defs["NLContract"]["properties"][
        "normative_statement"
    ]["description"]

    grounding_prompt = build_grounding_prompt(
        pair,
        lens="contract_structure_contrast",
        round_index=1,
        contracts=validated,
    )
    assert '"value": "HighwayMode local exit"' in grounding_prompt
    assert '"value": "FinishState"' in grounding_prompt
    assert '"target_name": "HighwayMode local exit"' in grounding_prompt
    assert "current numbered segment's explicit semantic target" in CONTRACT_SYSTEM_PROMPT
    assert "must not become `NamedCompletionState`" in CONTRACT_SYSTEM_PROMPT


def test_containment_and_termination_contracts_survive_covered_segment_accounting() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    segment = next(item for item in pair.nl_segments if item.segment_id == "NL1")

    def contract(
        contract_id: str,
        *,
        property_name: str,
        locus_kind: str,
        locus_names: tuple[str, ...],
        expected_direction: str,
        violation_direction: str,
        state_role: str | None = None,
    ) -> NLContract:
        binding_hints = ()
        if property_name == "transition_endpoints":
            binding_hints = (
                ContractBindingHint(
                    role="source",
                    value=locus_names[0],
                    source_ref=segment.segment_id,
                    reason="The fixture binds the first typed endpoint as source.",
                    basis="provider-free endpoint source fixture",
                ),
                ContractBindingHint(
                    role="target",
                    value=locus_names[1],
                    source_ref=segment.segment_id,
                    reason="The fixture binds the second typed endpoint as target.",
                    basis="provider-free endpoint target fixture",
                ),
            )
        return NLContract(
            contract_id=contract_id,
            segment_id=segment.segment_id,
            quote=segment.text,
            normative_statement=f"The fixture requires {property_name}.",
            locus_kind=locus_kind,
            locus_names=locus_names,
            property=property_name,
            state_role=state_role,
            expected_direction=expected_direction,
            violation_direction=violation_direction,
            evidence_types=("source_identity", "semantic_comparison"),
            binding_hints=binding_hints,
            scope="AutonomousMode",
            source_refs=(segment.segment_id,),
            reason=f"The fixture preserves the independent {property_name} obligation.",
            basis="provider-free typed contract fixture",
        )

    containment = contract(
        "NL-CONTRACT-NL1-CONTAINMENT",
        property_name="containment",
        locus_kind="state",
        locus_names=("AutonomousMode", "InitialState"),
        expected_direction="must_be_contained",
        violation_direction="wrong_scope",
    )
    endpoint = contract(
        "NL-CONTRACT-NL1-ENDPOINT",
        property_name="transition_endpoints",
        locus_kind="transition",
        locus_names=("AutonomousMode", "InitialState"),
        expected_direction="must_exist",
        violation_direction="missing",
    )
    termination = contract(
        "NL-CONTRACT-NL1-TERMINATION",
        property_name="termination",
        locus_kind="state",
        locus_names=("FinishState",),
        expected_direction="must_terminate",
        violation_direction="not_completed",
        state_role="termination_state",
    )
    response = NLContractResponse(
        contracts=[containment, endpoint, termination],
        segment_disposition={segment.segment_id: "covered"},
        reason="Covered retains every independently violable contract.",
        basis="provider-free segment-accounting fixture",
    )
    normalized, _ = normalize_contract_state_roles(response)
    assert {item.property for item in normalized.contracts} == {
        "containment",
        "transition_endpoints",
        "termination",
    }
    assert not any(item.property == "deadlock_freedom" for item in normalized.contracts)


def test_0046_contract_shape_separates_endpoint_and_event_consumer() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    segment = next(item for item in pair.nl_segments if item.segment_id == "NL3")
    common = {
        "contract_id": "NL-CONTRACT-NL3-INTERCEPTION",
        "segment_id": segment.segment_id,
        "quote": segment.text,
        "normative_statement": "The interception event must be consumed in the UAV swarm scope.",
        "locus_kind": "event",
        "locus_names": ("interception event", "UAV swarm scope"),
        "expected_direction": "must_cover",
        "evidence_types": ("source_identity", "event_consumer_fact", "reachability_fact"),
        "binding_hints": (
            ContractBindingHint(
                role="event",
                value="interception event",
                source_ref=segment.segment_id,
                reason="The source clause supplies the event.",
                basis=segment.segment_id,
            ),
            ContractBindingHint(
                role="scope",
                value="UAV swarm scope",
                source_ref=segment.segment_id,
                reason="The source clause supplies the applicable scope.",
                basis=segment.segment_id,
            ),
        ),
        "scope": "UAV swarm operation",
        "source_refs": (segment.segment_id,),
        "reason": "The fixture separates consumer coverage from endpoint identity.",
        "basis": "0046 numbered NL input without ledger or judge data",
    }
    with pytest.raises(ValidationError, match="event-consumer"):
        NLContract(
            **common,
            property="trigger_set",
            violation_direction="wrong_target",
        )

    event_consumer = NLContract(
        **common,
        property="event_consumer_coverage",
        violation_direction="unconsumed",
    )
    assert event_consumer.property == "event_consumer_coverage"
    assert event_consumer.violation_direction == "unconsumed"
    assert "One contract represents one property" in CONTRACT_SYSTEM_PROMPT
    assert "semantic LLM judgment" in CONTRACT_SYSTEM_PROMPT
    assert "bidirectional or dynamic A-to-B/B-to-A requirement" in CONTRACT_SYSTEM_PROMPT
    assert "one normalized guard hint" in CONTRACT_SYSTEM_PROMPT
    assert "`property=state_action` uses `evidence_types=[action_fact]`" in CONTRACT_SYSTEM_PROMPT
    assert "return the complete replacement" in build_contract_prompt(pair, 1)
    assert "Never return only the" in " ".join(build_contract_prompt(pair, 1).split())
    contract_schema = NLContractResponse.model_json_schema()
    contracts_description = contract_schema["properties"]["contracts"]["description"]
    assert "complete replacement list" in contracts_description
    with pytest.raises(ValidationError, match="each contract_id at most once"):
        NLContractResponse(
            contracts=[event_consumer, event_consumer],
            segment_disposition={segment.segment_id: "covered"},
            reason="The response contains a duplicate contract identity.",
            basis="provider-free duplicate-ID fixture",
        )
    invalid_evidence_type = event_consumer.model_dump(mode="json")
    invalid_evidence_type["evidence_types"] = ["state_action"]
    with pytest.raises(ValidationError):
        NLContract.model_validate(invalid_evidence_type)
    evidence_description = NLContract.model_json_schema()["properties"][
        "evidence_types"
    ]["description"]
    assert "trigger_fact" in evidence_description
    assert "action_fact" in evidence_description
    assert "state_action is a property name" in evidence_description
    role_description = NLContract.model_json_schema()["$defs"][
        "ContractBindingHint"
    ]["properties"]["role"]["description"]
    assert "mode or composite itself transitions" in role_description
    assert "never substitutes for an endpoint source" in role_description
    assert "`trigger_fact`" in CONTRACT_SYSTEM_PROMPT
    trigger_evidence_payload = event_consumer.model_dump(mode="json")
    trigger_evidence_payload["evidence_types"] = ["trigger_fact"]
    trigger_evidence = NLContract.model_validate(trigger_evidence_payload)
    assert trigger_evidence.evidence_types == ("trigger_fact",)
    assert "Every candidate object must explicitly include" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "must always be a JSON object" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Never return a candidate-only derived reference" in " ".join(
        DISCOVERY_GROUNDING_SYSTEM_PROMPT.split()
    )
    assert "Complete-inventory absence protocol" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "a nonexistent transition cannot supply its own ref" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Do not leave a normative qualifier only inside" in CONTRACT_SYSTEM_PROMPT
    assert "instead of duplicating every mentioned qualifier" in CONTRACT_SYSTEM_PROMPT
    assert "derive only actual mismatches" in CONTRACT_SYSTEM_PROMPT
    assert 'Words such as "when", "if", or "based on"' in CONTRACT_SYSTEM_PROMPT
    assert "effect and guard are property values" in NLContract.model_json_schema()["properties"]["locus_kind"]["description"]
    group_schema = NLTransitionGroup.model_json_schema()
    owner_description = group_schema["properties"][
        "common_enclosing_owner_name"
    ]["description"]
    assert "does not create containment contracts" in owner_description
    assert "source itself is the owner" in owner_description


def test_state_role_normalization_merges_only_exact_typed_progress_identity() -> None:
    def progress_contract(
        contract_id: str,
        segment_id: str,
        state_name: str,
    ) -> NLContract:
        return NLContract(
            contract_id=contract_id,
            segment_id=segment_id,
            quote=f"{state_name} remains operational.",
            normative_statement=f"{state_name} must retain progress.",
            locus_kind="state",
            locus_names=(state_name,),
            property="deadlock_freedom",
            state_role="operating_state",
            expected_direction="must_progress",
            violation_direction="dead_end",
            evidence_types=("deadlock_frontier_fact",),
            binding_hints=(
                ContractBindingHint(
                    role="state",
                    value=state_name,
                    source_ref=segment_id,
                    reason="The numbered segment establishes this operating state.",
                    basis=segment_id,
                ),
            ),
            scope=f"{state_name} operation",
            source_refs=(segment_id,),
            reason="The state has an active operating role.",
            basis=segment_id,
        )

    first = progress_contract("NL-CONTRACT-NL1-PROGRESS", "NL1", "DoorOpen")
    repeated = progress_contract("NL-CONTRACT-NL2-PROGRESS", "NL2", "DoorOpen")
    distinct = progress_contract(
        "NL-CONTRACT-NL2-OTHER-PROGRESS", "NL2", "DoorOpenWithItem"
    )
    response = NLContractResponse(
        contracts=[first, repeated, distinct],
        segment_disposition={"NL1": "covered", "NL2": "covered"},
        reason="The fixture extracted typed operating-state roles.",
        basis="provider-free numbered NL fixture",
    )

    normalized, diagnostics = normalize_contract_state_roles(response)

    assert [item.contract_id for item in normalized.contracts] == [
        first.contract_id,
        distinct.contract_id,
    ]
    assert normalized.contracts[0].source_refs == ("NL1", "NL2")
    assert diagnostics[0]["merged_contract_ids"] == [repeated.contract_id]
    assert diagnostics[0]["semantic_key"]["locus_names"] == ["DoorOpen"]


def test_exact_outgoing_fact_rejects_false_dead_end_but_preserves_true_frontier() -> None:
    def response_for(pair, state_name: str) -> GroundingResponse:
        state = next(item for item in pair.model.states if item.name == state_name)
        contract_id = "NL-CONTRACT-NL1-PROGRESS"
        candidate = CandidateIssue(
            contract_id=contract_id,
            locus_kind="state",
            locus_names=(state_name,),
            property="deadlock_freedom",
            violation_direction="dead_end",
            evidence_types=("deadlock_frontier_fact", "verify_fact"),
            title=f"{state_name} has no progress",
            requirement_quote=f"{state_name} must continue.",
            predicate_id="V4",
            predicate_inputs={"initial_scope": pair.model.states[0].name},
            element_refs=[state.ref],
            source_refs=["NL1"],
            expected=f"{state_name} retains progress.",
            observed=f"{state_name} was proposed as a dead end.",
            strongest_rebuttal="An exact outgoing transition would satisfy local progress.",
            reason="The grounding fixture proposes one typed dead-end candidate.",
            basis="provider-free exact ModelIR fixture",
        )
        return GroundingResponse(
            lens="behavior_consequence",
            candidates=[candidate],
            reason="The fixture returns one behavior candidate.",
            basis="provider-free grounding fixture",
        )

    with_outgoing = load_pair(REPORT_ROOT / "pairs" / "0035")
    normalized, diagnostics = _normalize_grounding_exact_facts(
        with_outgoing, response_for(with_outgoing, "DoorOpen")
    )
    assert normalized.candidates == []
    assert normalized.unresolved == []
    assert diagnostics[0]["class"] == "exact_local_progress_satisfied"
    assert diagnostics[0]["outgoing_transition_refs"]["DoorOpen"]

    zero_outgoing = load_pair(REPORT_ROOT / "pairs" / "0023")
    preserved, diagnostics = _normalize_grounding_exact_facts(
        zero_outgoing, response_for(zero_outgoing, "PumpState")
    )
    assert len(preserved.candidates) == 1
    assert preserved.unresolved == []
    assert diagnostics == []


def test_cardinality_owner_mapping_normalizes_only_exact_published_ref() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    representation_ref = (
        "state:llms_emp_feedback_final_0046.UAVSwarmStateMachine.SearchRegion"
    )
    owned_ref = pair.model.state("SearchRegion").ref

    def response_for(model_ref: str) -> GroundingResponse:
        return GroundingResponse(
            lens="contract_structure_contrast",
            cardinality_bindings=[
                CardinalityDomainBinding(
                    binding_id="CARD-BIND-NL2-SEARCH-AREAS",
                    contract_id="NL-CONTRACT-NL2-THREE-AREAS",
                    status="exact",
                    member_domain="direct_child_states",
                    owner_source_id="UAVSwarmStateMachine.SearchRegion",
                    owner_model_ref=model_ref,
                    reason="The supplied source identifies the exact search-area owner.",
                    basis="provider-free exact source and working-contract fixture",
                )
            ],
            reason="The fixture supplies one exact cardinality binding.",
            basis="provider-free grounding normalization fixture",
        )

    raw = response_for(representation_ref)
    normalized, diagnostics = _normalize_grounding_exact_facts(pair, raw)

    assert raw.cardinality_bindings[0].owner_model_ref == representation_ref
    assert normalized.cardinality_bindings[0].owner_model_ref == owned_ref
    assert "runner exact join" in normalized.cardinality_bindings[0].basis
    assert diagnostics == []

    wrong_owner_ref = (
        "state:llms_emp_feedback_final_0046.UAVSwarmStateMachine.MissionRegion"
    )
    preserved, diagnostics = _normalize_grounding_exact_facts(
        pair, response_for(wrong_owner_ref)
    )
    assert preserved.cardinality_bindings[0].owner_model_ref == wrong_owner_ref
    assert diagnostics == []


def test_execute_boundary_excludes_only_completed_true_receipts() -> None:
    def prepared(terminal_state: str, verdict: str) -> dict:
        return {
            "receipt": RawReceipt(
                receipt_id=f"receipt:{terminal_state}:{verdict}",
                backend="provider-free-fixture",
                terminal_state=terminal_state,
                verdict=verdict,
                reason="The fixture supplies one deterministic backend result.",
                basis="provider-free execute-boundary fixture",
            )
        }

    assert not _prepared_is_finding_candidate(prepared("completed", "true"))
    assert _prepared_is_finding_candidate(prepared("completed", "false"))
    assert _prepared_is_finding_candidate(prepared("unknown", "unknown"))
    assert _prepared_is_finding_candidate(prepared("error", "unknown"))


def test_exact_s2_scout_materializes_missing_typed_edge_without_text_rules() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0035")
    segment = next(item for item in pair.nl_segments if item.segment_id == "NL2")
    contract = NLContract(
        contract_id="NL-CONTRACT-NL2-ENDPOINT-MISSING",
        segment_id="NL2",
        quote=segment.text,
        normative_statement="DoorOpen must transition to DoorShut.",
        locus_kind="transition",
        locus_names=("DoorOpen", "DoorShut"),
        property="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        evidence_types=("source_identity", "transition_fact"),
        binding_hints=(
            ContractBindingHint(
                role="source",
                value="DoorOpen",
                source_ref="NL2",
                reason="The typed source endpoint is explicit.",
                basis="provider-free NL2 fixture",
            ),
            ContractBindingHint(
                role="target",
                value="DoorShut",
                source_ref="NL2",
                reason="The typed target endpoint is explicit.",
                basis="provider-free NL2 fixture",
            ),
        ),
        scope="microwave operation",
        source_refs=("NL2",),
        reason="The provider-free contract captures one ordered endpoint obligation.",
        basis="provider-free typed NL contract without ledger data",
    )
    contracts = NLContractResponse(
        contracts=[contract],
        segment_disposition={"NL2": "covered"},
        reason="The fixture provides one exact transition contract.",
        basis="provider-free exact contract fixture",
    )

    candidates, receipts = _materialize_exact_s2_inventory_candidates(
        pair, contracts, []
    )

    assert len(candidates) == 1
    assert len(receipts) == 1
    candidate = candidates[0]
    assert candidate.contract_id == contract.contract_id
    assert candidate.predicate_id == "S2"
    assert candidate.violation_direction == "wrong_target"
    assert candidate.predicate_inputs == {
        "source": "DoorOpen",
        "target": "DoorShut",
        "scope": "closed_fcstm",
    }
    assert set(candidate.element_refs) == {
        pair.model.state("DoorOpen").ref,
        pair.model.state("DoorShut").ref,
    }
    prepared = _prepare_candidate(
        pair,
        candidate,
        1,
        0,
        {contract.contract_id: contract},
    )
    assert prepared["binding"].precise is True
    assert prepared["receipt"].terminal_state == "completed"
    assert prepared["receipt"].verdict == "false"

    duplicate_candidates, duplicate_receipts = (
        _materialize_exact_s2_inventory_candidates(pair, contracts, candidates)
    )
    assert duplicate_candidates == []
    assert duplicate_receipts == []

    source_hint, target_hint = contract.binding_hints
    present_contract = contract.model_copy(
        update={
            "contract_id": "NL-CONTRACT-NL2-ENDPOINT-PRESENT",
            "locus_names": ("DoorShut", "DoorOpen"),
            "binding_hints": (
                source_hint.model_copy(update={"value": "DoorShut"}),
                target_hint.model_copy(update={"value": "DoorOpen"}),
            ),
        }
    )
    present_contracts = contracts.model_copy(update={"contracts": [present_contract]})
    present_candidates, present_receipts = (
        _materialize_exact_s2_inventory_candidates(pair, present_contracts, [])
    )
    assert present_candidates == []
    assert present_receipts == []


def _completion_endpoint_contract() -> NLContract:
    return NLContract(
        contract_id="NL-CONTRACT-COMPLETION-ENDPOINT",
        segment_id="NL6",
        quote="The operating mode ends by transitioning to the named completion state.",
        normative_statement="The operating mode must transition to the named completion state.",
        locus_kind="transition",
        locus_names=("HighwayMode", "FinishState"),
        property="transition_endpoints",
        state_role="termination_state",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        evidence_types=("source_identity", "transition_fact"),
        binding_hints=(
            ContractBindingHint(
                role="source",
                value="HighwayMode",
                source_ref="NL6",
                reason="The operating mode is the explicit transition source.",
                basis="provider-free endpoint fixture",
            ),
            ContractBindingHint(
                role="target",
                value="FinishState",
                source_ref="NL6",
                reason="The completion state is the explicit transition target.",
                basis="provider-free endpoint fixture",
            ),
        ),
        scope="Operating-mode completion",
        source_refs=("NL6",),
        reason="The endpoint requirement is independently testable.",
        basis="provider-free typed endpoint fixture",
    )


def test_complete_protected_source_transition_macro_suppresses_endpoint_candidate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    contract = _completion_endpoint_contract()

    receipt = evaluate_source_transition_closure(pair, contract)

    assert isinstance(receipt, SourceTransitionClosureReceipt)
    assert receipt.status == "satisfied"
    assert receipt.candidate_disposition == "suppress_matching_endpoint_candidates"
    assert receipt.source_transition_id == "tr_0027"
    assert receipt.macro_id == "macro:transition:tr_0027"
    assert len(receipt.expected_member_ids) == 9
    assert receipt.expected_member_ids == receipt.observed_member_ids
    assert receipt.published_member_digest == receipt.recomputed_member_digest
    assert receipt.target_entry_fcstm_ref == "fcstm:line:27"
    assert all(member.closed for member in receipt.member_receipts)
    assert receipt.hashes.source_inventory_sha256 is not None
    assert not receipt.diagnostics

    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Completion appears to target the enclosing mode",
        requirement_quote=contract.quote,
        predicate_id="S2",
        predicate_inputs={
            "source": "HighwayMode",
            "target": "FinishState",
            "scope": "closed_fcstm",
        },
        element_refs=[],
        source_refs=["NL6"],
        expected=contract.normative_statement,
        observed="A compiler-generated controller segment is a self-loop.",
        strongest_rebuttal="The complete protected macro may realize the author transition.",
        reason="The candidate reads one compiler-owned segment as an independent endpoint.",
        basis="provider-free candidate fixture",
    )
    assert endpoint_candidate_is_satisfied_by_macro(candidate, receipt)
    retained, dispositions = suppress_satisfied_source_transition_candidates(
        [candidate],
        {contract.contract_id: receipt},
        candidate_origin="grounding",
    )
    assert retained == []
    assert len(dispositions) == 1
    assert dispositions[0].disposition == "suppressed_satisfied_endpoint"

    contracts = NLContractResponse(
        contracts=[contract],
        segment_disposition={"NL6": "covered"},
        reason="The endpoint fixture is complete.",
        basis="provider-free endpoint fixture",
    )
    materialized, scout_receipts = _materialize_exact_s2_inventory_candidates(
        pair,
        contracts,
        [],
        {contract.contract_id: receipt},
    )
    assert materialized == []
    assert scout_receipts == []


def test_cross_scope_target_entry_closes_source_transition_macro() -> None:
    """A cross-scope descendant entry is still the exact macro target carrier."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    base = _completion_endpoint_contract()
    contract = base.model_copy(
        update={
            "contract_id": "NL-CONTRACT-CROSS-SCOPE-ENDPOINT",
            "locus_names": ("UrbanMode", "FinishState"),
            "binding_hints": (
                base.binding_hints[0].model_copy(update={"value": "UrbanMode"}),
                base.binding_hints[1].model_copy(update={"value": "FinishState"}),
            ),
            "source_refs": ("NL10",),
        }
    )

    receipt = evaluate_source_transition_closure(pair, contract)

    assert receipt.status == "satisfied"
    assert receipt.source_transition_id == "tr_0026"
    assert receipt.target_entry_fcstm_ref == "fcstm:line:26"
    assert not receipt.diagnostics


def test_closed_route_controller_macro_suppresses_representation_gap_candidate() -> None:
    """Complete event/effect/guard/target closure is not a missing guard."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0024")
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL2-GUARD-EMERGENCY-1",
        locus_kind="transition",
        locus_names=("InMotion", "EmergencyStopping"),
        property="guard",
        violation_direction="wrong_guard",
        evidence_types=("guard_fact", "transition_fact"),
        title="Emergency alternative lacks the required obstacle guard",
        requirement_quote="The emergency branch requires obstacle detection.",
        predicate_id=None,
        predicate_inputs={},
        element_refs=["transition:line:31"],
        source_refs=["NL2", "source:transition:tr_0009"],
        expected="The emergency branch requires obstacle detection.",
        observed="The parent carrier uses a route-token guard.",
        strongest_rebuttal="The protected macro may encode the source event.",
        reason="Provider-free route-controller representation fixture.",
        basis="Exact source transition and protected macro fixture.",
    )

    retained, dispositions = suppress_closed_route_controller_candidates(
        pair, [candidate]
    )

    assert retained == []
    assert len(dispositions) == 1
    assert dispositions[0]["status"] == (
        "suppressed_closed_route_controller_equivalence"
    )
    assert dispositions[0]["macro_ids"] == ["macro:transition:tr_0009"]


def test_synthetic_root_wrapper_does_not_make_reachable_child_unreachable() -> None:
    """A generated machine container is not an additional runtime root state."""

    pair = load_pair(REPORT_ROOT / "pairs" / "0056")
    facts = pair.inspection_facts
    assert facts is not None
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-ROOT-WRAPPER-REACHABILITY",
        locus_kind="composite",
        locus_names=("SearchState",),
        property="reachability",
        violation_direction="unreachable",
        evidence_types=("reachability_fact",),
        title="SearchState is unreachable from the wrapper",
        requirement_quote="SearchState must be reachable.",
        predicate_id="G1",
        predicate_inputs={
            "source": [facts.machine_root_ref],
            "target": ["state:SearchState:line:9"],
        },
        element_refs=[facts.machine_root_ref, "state:SearchState:line:9"],
        source_refs=["source:transition:tr_0001"],
        expected="SearchState must be reachable.",
        observed="The synthetic wrapper is marked unreachable.",
        strongest_rebuttal="The exact top-level initial source transition enters SearchState.",
        reason="Provider-free synthetic-wrapper fixture.",
        basis="Exact inspection and source-inventory fixture.",
    )

    retained, dispositions = _preflight_synthetic_root_wrapper_reachability(
        pair, [candidate]
    )

    assert retained == []
    assert len(dispositions) == 1
    assert dispositions[0]["status"] == (
        "suppressed_synthetic_root_wrapper_projection"
    )


def test_incomplete_source_transition_macro_remains_unresolved_and_keeps_candidate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    assert pair.working_contract is not None
    contract = _completion_endpoint_contract()
    payload = json.loads(json.dumps(pair.working_contract.payload))
    macro = next(
        item
        for item in payload["macros"]
        if item["macro_id"] == "macro:transition:tr_0027"
    )
    missing_member_id = macro["member_element_ids"][-1]
    payload["elements"] = [
        item
        for item in payload["elements"]
        if item["element_id"] != missing_member_id
    ]
    incomplete_pair = pair.model_copy(
        update={
            "working_contract": pair.working_contract.model_copy(
                update={"payload": payload}
            )
        }
    )

    receipt = evaluate_source_transition_closure(incomplete_pair, contract)

    assert receipt.status == "unresolved"
    assert receipt.candidate_disposition == "retain_candidates"
    assert missing_member_id not in receipt.observed_member_ids
    assert any(not member.closed for member in receipt.member_receipts)
    assert any("protected ownership" in item for item in receipt.diagnostics)


def _ambiguous_source_endpoint_fixture(
    *,
    carrier_ref: str = "transition:line:40",
    target_model_ref: str = "state:FormationAdjustment:line:38",
) -> tuple[CandidateIssue, GroundingResponse]:
    candidate = CandidateIssue(
        contract_id="NL-CONTRACT-NL3-ENDPOINT-1",
        locus_kind="transition",
        locus_names=("unresolved source state", "formation adjustment state"),
        property="transition_endpoints",
        violation_direction="wrong_target",
        evidence_types=(
            "source_identity",
            "transition_fact",
            "closed_model_inventory",
        ),
        title="Interception transition source is not uniquely grounded",
        requirement_quote="When intercepted, transition to formation adjustment.",
        predicate_id=None,
        predicate_inputs={},
        element_refs=[carrier_ref, target_model_ref],
        source_refs=[
            "llms_emp_feedback_final_0056.puml:line:16",
            "source:transition:tr_0009",
        ],
        expected="The intended interception source enters FormationAdjustment.",
        observed="The exact target carrier is present but its source is called ambiguous.",
        strongest_rebuttal="The cited author transition and closed carrier may have identical endpoints.",
        reason="The source is described as ambiguous despite one cited author transition.",
        basis="provider-free exact-carrier contradiction fixture",
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=[
            SemanticBinding(
                binding_id="BIND-NL3-SOURCE",
                contract_id=candidate.contract_id,
                role="source",
                concept_name="interception response source state",
                status="ambiguous",
                reason="The source was left ambiguous by this grounding branch.",
                basis="provider-free ambiguous source fixture",
            ),
            SemanticBinding(
                binding_id="BIND-NL3-TARGET",
                contract_id=candidate.contract_id,
                role="target",
                concept_name="formation adjustment state",
                status="exact",
                source_element_ref="source:state:FormationAdjustment",
                model_element_ref=target_model_ref,
                carrier_transition_ref=carrier_ref,
                reason="The target and its closed carrier are exact.",
                basis="provider-free exact target fixture",
            ),
        ],
        reason="The fixture isolates typed source ambiguity and one exact target carrier.",
        basis="provider-free source-transition binding fixture",
    )
    return candidate, grounding


def test_exact_author_and_closed_endpoints_suppress_only_contradicted_source_ambiguity() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0056")
    candidate, grounding = _ambiguous_source_endpoint_fixture()
    second_grounding = grounding.model_copy(
        update={"lens": "behavior_consequence"}
    )

    retained, dispositions = suppress_contradicted_ambiguous_source_candidates(
        pair,
        [candidate],
        [grounding],
    )
    assert retained == [candidate]
    assert dispositions == []

    retained, dispositions = suppress_contradicted_ambiguous_source_candidates(
        pair,
        [candidate],
        [grounding, second_grounding],
    )

    assert retained == []
    assert len(dispositions) == 1
    assert dispositions[0].disposition == (
        "suppressed_contradicted_ambiguous_source"
    )
    assert dispositions[0].author_transition_id == "tr_0009"
    assert dispositions[0].closed_carrier_ref == "transition:line:40"
    assert dispositions[0].supporting_lenses == (
        "behavior_consequence",
        "contract_structure_contrast",
    )
    assert dispositions[0].ambiguous_source_binding_ids == ("BIND-NL3-SOURCE",)
    assert dispositions[0].exact_target_binding_ids == ("BIND-NL3-TARGET",)

    exact_source = SemanticBinding(
        binding_id="BIND-NL3-SOURCE-EXACT",
        contract_id=candidate.contract_id,
        role="source",
        concept_name="SearchState",
        status="exact",
        source_element_ref="source:state:SearchState",
        model_element_ref="state:SearchState:line:9",
        reason="The fixture supplies an exact source binding.",
        basis="provider-free exact source fixture",
    )
    grounding_with_exact_source = grounding.model_copy(
        update={
            "semantic_bindings": [*grounding.semantic_bindings, exact_source],
        }
    )
    retained, dispositions = suppress_contradicted_ambiguous_source_candidates(
        pair,
        [candidate],
        [grounding_with_exact_source, second_grounding],
    )
    assert retained == [candidate]
    assert dispositions == []

    mismatched_candidate, mismatched_grounding = _ambiguous_source_endpoint_fixture(
        carrier_ref="transition:line:41",
        target_model_ref="state:AttackState:line:39",
    )
    retained, dispositions = suppress_contradicted_ambiguous_source_candidates(
        pair,
        [mismatched_candidate],
        [
            mismatched_grounding,
            mismatched_grounding.model_copy(update={"lens": "behavior_consequence"}),
        ],
    )
    assert retained == [mismatched_candidate]
    assert dispositions == []


def _runtime_fixture_pricing() -> LLMPricing:
    return LLMPricing(
        prices=LLMTokenPrices(
            input_usd_per_million_tokens=1.0,
            output_usd_per_million_tokens=2.0,
            cache_read_usd_per_million_tokens=0.1,
            cache_write_usd_per_million_tokens=0.2,
        ),
        source_url="https://example.invalid/pricing",
        verified_on=date(2026, 8, 21),
        basis="official_list_price",
        scope_note="fixture",
    )


def _provider_free_public_runtime(
    tmp_path: Path,
    *,
    pricing: LLMPricing,
    request: pytest.FixtureRequest,
) -> PublicStructuredRuntime:
    runtime = PublicStructuredRuntime.__new__(PublicStructuredRuntime)
    runtime.profile = "fixture"
    runtime.artifact_root = tmp_path
    runtime.streaming = True
    runtime.transport_retries = 0
    runtime.config = SimpleNamespace(
        pricing=pricing,
        context_window_tokens=272_000,
    )
    runtime._start_event_loop()

    async def initialize() -> None:
        runtime._async_call_lock = asyncio.Lock()
        runtime._transport_model = SimpleNamespace(
            root_async_client=None,
            root_client=None,
        )

    runtime._submit_to_event_loop(initialize())
    request.addfinalizer(runtime.close)
    return runtime


def test_provider_retry_exemption_is_row_local_and_other_usage_is_billable() -> None:
    pricing = _runtime_fixture_pricing()
    rows = [
        {"model_call_id": "failed", "status": "failed", "input_tokens": None, "output_tokens": None},
        {"model_call_id": "successful", "status": "completed", "input_tokens": 100, "output_tokens": 10},
    ]
    audit_records = [
        {
            "record": "transport_retry",
            "record_type": "transport_retry",
            "operation": "scheduled",
            "failed_model_call_id": "failed",
            "error": {"type": "RateLimitError", "message": "rate limit"},
        }
    ]
    _annotate_usage_billing(rows, audit_records=audit_records, final_error=None)
    cost = _cost_for_usage(rows, pricing)

    assert rows[0]["cost_counted"] is False
    assert rows[0]["billing_disposition"] == "provider_error_retry_exempt"
    assert rows[1].get("cost_counted", True) is True
    assert cost["eligible"] is True
    assert cost["total_usd"] is not None and cost["total_usd"] > 0
    assert cost["attempts"][0]["total_usd"] == 0.0
    assert cost["attempts"][1]["total_usd"] > 0


def test_usage_rows_normalize_nested_cache_fields_before_pricing() -> None:
    rows = _usage_rows(
        {
            "usage": [
                {
                    "model_call_id": "nested-cache",
                    "status": "completed",
                    "input_tokens": 1_000,
                    "output_tokens": 100,
                    "input_token_details": {
                        "cache_read": 800,
                        "cache_creation": 50,
                    },
                },
                {
                    "model_call_id": "standard-cache",
                    "status": "completed",
                    "input_tokens": 500,
                    "output_tokens": 20,
                    "cache_read_input_tokens": 300,
                    "cache_creation_input_tokens": 25,
                },
                {
                    "model_call_id": "no-cache",
                    "status": "completed",
                    "input_tokens": 200,
                    "output_tokens": 10,
                },
            ]
        }
    )

    assert rows[0]["cache_read_input_tokens"] == 800
    assert rows[0]["cache_creation_input_tokens"] == 50
    assert rows[1]["cache_read_input_tokens"] == 300
    assert rows[1]["cache_creation_input_tokens"] == 25
    assert rows[2]["cache_read_input_tokens"] is None
    assert rows[2]["cache_creation_input_tokens"] is None

    cost = _cost_for_usage(rows, _runtime_fixture_pricing())
    assert cost["eligible"] is True
    assert cost["attempts"][0]["categories"]["input"]["tokens"] == 150
    assert cost["attempts"][0]["categories"]["cache_read"]["tokens"] == 800
    assert cost["attempts"][0]["categories"]["cache_write"]["tokens"] == 50
    assert cost["attempts"][1]["categories"]["input"]["tokens"] == 175
    assert cost["attempts"][2]["categories"]["input"]["tokens"] == 200


def test_corrected_cost_aggregate_preserves_retry_billing_and_source_hashes(
    tmp_path: Path,
) -> None:
    root = tmp_path / "historical-run"
    method_path = root / "method" / "0004" / "round-1.json"
    billable_result = root / "llm" / "billable" / "result.json"
    provider_result = root / "llm" / "provider-error" / "result.json"
    method_path.parent.mkdir(parents=True)
    billable_result.parent.mkdir(parents=True)
    provider_result.parent.mkdir(parents=True)
    (root / "run_manifest.json").write_text(
        json.dumps(
            {
                "run_id": "historical-cost-fixture",
                "profile": "fixture-profile",
                "source_provenance": {"source_commit": "a" * 40},
            }
        ),
        encoding="utf-8",
    )
    (root / "summary.json").write_text(
        json.dumps(
            {
                "run_id": "historical-cost-fixture",
                "profile": "fixture-profile",
                "source_commit": "a" * 40,
                "method_cost_usd": 99.0,
            }
        ),
        encoding="utf-8",
    )
    billable_result.write_text(
        json.dumps(
            {
                "usage": [
                    {
                        "input_tokens": 1_000,
                        "output_tokens": 100,
                        "input_token_details": {
                            "cache_read": 800,
                            "cache_creation": 50,
                        },
                    },
                    {
                        "input_tokens": 500,
                        "output_tokens": 20,
                        "cache_read_input_tokens": 300,
                        "cache_creation_input_tokens": 25,
                    },
                    {"input_tokens": 200, "output_tokens": 10},
                ]
            }
        ),
        encoding="utf-8",
    )
    provider_result.write_text(
        json.dumps(
            {"usage": [{"input_tokens": 10_000, "output_tokens": 1_000}]}
        ),
        encoding="utf-8",
    )
    method_path.write_text(
        json.dumps(
            {
                "run_id": "historical-cost-fixture",
                "pair_id": "0004",
                "round": 1,
                "llm_calls": [
                    {
                        "kind": "contract_extraction",
                        "schema_validation_failures": [{"turn": 1}],
                        "attempts": [
                            {
                                "outer_attempt": 1,
                                "result_path": str(billable_result.resolve()),
                                "billing_disposition": "billable",
                                "provider_error": False,
                            }
                        ],
                    },
                    {
                        "kind": "grounding",
                        "schema_validation_failures": [],
                        "attempts": [
                            {
                                "outer_attempt": 2,
                                "result_path": str(provider_result.resolve()),
                                "billing_disposition": "provider_error_retry_exempt",
                                "provider_error": True,
                            }
                        ],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    aggregate = build_corrected_method_cost(
        root, pricing=_runtime_fixture_pricing()
    )

    assert aggregate.method_cell_count == 1
    assert aggregate.logical_call_count == 2
    assert aggregate.outer_attempt_count == 2
    assert aggregate.provider_request_count == 4
    assert aggregate.billable_provider_request_count == 3
    assert aggregate.provider_error_exempt_request_count == 1
    assert aggregate.schema_validation_failure_count == 1
    assert aggregate.breakdown.uncached_input.tokens == 525
    assert aggregate.breakdown.cache_read.tokens == 1_100
    assert aggregate.breakdown.cache_creation.tokens == 75
    assert aggregate.breakdown.output.tokens == 130
    assert aggregate.corrected_method_cost_usd == pytest.approx(0.00091)
    assert aggregate.result_receipts[0].corrected_cost_usd > 0
    assert aggregate.result_receipts[1].corrected_cost_usd == 0
    assert len(aggregate.source_artifacts) == 5
    assert aggregate.source_closure_hash.startswith("sha256:")


def test_corrected_cost_preserves_billable_rows_before_provider_failure(
    tmp_path: Path,
) -> None:
    root = tmp_path / "mixed-provider-error-run"
    method_path = root / "method" / "0004" / "round-1.json"
    failed_result = root / "llm" / "failed-attempt" / "result.json"
    retry_result = root / "llm" / "successful-retry" / "result.json"
    method_path.parent.mkdir(parents=True)
    failed_result.parent.mkdir(parents=True)
    retry_result.parent.mkdir(parents=True)
    (root / "run_manifest.json").write_text(
        json.dumps(
            {
                "run_id": "mixed-provider-error-fixture",
                "profile": "fixture-profile",
                "source_provenance": {"source_commit": "a" * 40},
            }
        ),
        encoding="utf-8",
    )
    (root / "summary.json").write_text(
        json.dumps(
            {
                "run_id": "mixed-provider-error-fixture",
                "profile": "fixture-profile",
                "source_commit": "a" * 40,
                "method_cost_usd": 0.0018,
            }
        ),
        encoding="utf-8",
    )
    failed_result.write_text(
        json.dumps(
            {
                "usage": [
                    {"input_tokens": 10_000, "output_tokens": 1_000},
                    {"input_tokens": None, "output_tokens": None},
                ]
            }
        ),
        encoding="utf-8",
    )
    retry_result.write_text(
        json.dumps({"usage": [{"input_tokens": 500, "output_tokens": 50}]}),
        encoding="utf-8",
    )
    method_path.write_text(
        json.dumps(
            {
                "run_id": "mixed-provider-error-fixture",
                "pair_id": "0004",
                "round": 1,
                "llm_calls": [
                    {
                        "kind": "grounding",
                        "schema_validation_failures": [{"turn": 1}],
                        "attempts": [
                            {
                                "outer_attempt": 1,
                                "result_path": str(failed_result.resolve()),
                                "billing_disposition": "provider_error_attempt_requires_row_level_join",
                                "provider_error": True,
                            },
                            {
                                "outer_attempt": 2,
                                "result_path": str(retry_result.resolve()),
                                "billing_disposition": "billable",
                                "provider_error": False,
                            },
                        ],
                        "usage": [
                            {
                                "outer_attempt": 1,
                                "input_tokens": 1_000,
                                "output_tokens": 100,
                                "cost_counted": True,
                                "billing_disposition": "billable",
                            },
                            {
                                "outer_attempt": 1,
                                "input_tokens": None,
                                "output_tokens": None,
                                "status": "failed",
                                "cost_counted": True,
                                "billing_disposition": "billable",
                            },
                            {
                                "outer_attempt": 2,
                                "input_tokens": 500,
                                "output_tokens": 50,
                                "cost_counted": True,
                                "billing_disposition": "billable",
                            },
                        ],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    aggregate = build_corrected_method_cost(
        root, pricing=_runtime_fixture_pricing()
    )

    assert aggregate.provider_request_count == 3
    assert aggregate.billable_provider_request_count == 2
    assert aggregate.provider_error_exempt_request_count == 1
    assert aggregate.breakdown.uncached_input.tokens == 1_500
    assert aggregate.breakdown.output.tokens == 150
    assert aggregate.corrected_method_cost_usd == pytest.approx(0.0018)
    assert aggregate.cost_eligible is True
    assert aggregate.result_receipts[0].provider_error is True
    assert aggregate.result_receipts[0].cost_eligible is True
    assert aggregate.result_receipts[0].corrected_cost_usd == pytest.approx(0.0012)
    assert "earlier completed schema-repair requests" in aggregate.result_receipts[0].reason


def test_identified_provider_retry_does_not_exempt_unrelated_cancellation() -> None:
    rows = [
        {
            "model_call_id": "failed-provider-call",
            "status": "failed",
            "input_tokens": None,
            "output_tokens": None,
        },
        {
            "model_call_id": "later-local-cancellation",
            "status": "cancelled",
            "input_tokens": None,
            "output_tokens": None,
        },
    ]
    audit_records = [
        {
            "record": "transport_retry",
            "record_type": "transport_retry",
            "operation": "scheduled",
            "failed_model_call_id": "failed-provider-call",
        }
    ]

    _annotate_usage_billing(
        rows,
        audit_records=audit_records,
        final_error={"code": "structured_stage_timeout"},
    )

    assert rows[0]["cost_counted"] is False
    assert rows[0]["billing_disposition"] == "provider_error_retry_exempt"
    assert rows[1].get("cost_counted", True) is True
    assert rows[1].get("billing_disposition", "billable") == "billable"


def test_terminal_provider_failure_without_an_actual_retry_remains_billable() -> None:
    rows = [
        {
            "model_call_id": "terminal",
            "status": "failed",
            "input_tokens": 100,
            "output_tokens": 0,
        }
    ]
    _annotate_usage_billing(
        rows,
        audit_records=[],
        final_error={"code": "provider_timeout", "message": "terminal timeout"},
    )
    assert rows[0].get("cost_counted", True) is True
    assert rows[0].get("billing_disposition", "billable") == "billable"

    _annotate_usage_billing(
        rows,
        audit_records=[],
        final_error={"code": "provider_timeout", "message": "retrying timeout"},
        actual_outer_retry=True,
    )
    assert rows[0]["cost_counted"] is False
    assert rows[0]["billing_disposition"] == "provider_error_retry_exempt"


def test_structured_stage_deadline_is_distinct_from_provider_timeout() -> None:
    assert PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS == 30
    assert PROVIDER_CALL_DEADLINE_SECONDS == 300
    assert _structured_model_call_reservation_limit(0) == 6
    assert _structured_model_call_reservation_limit(8) == 12
    assert STRUCTURED_STAGE_FINALIZATION_GRACE_SECONDS == 30
    assert STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS == 30
    assert STRUCTURED_STAGE_DEADLINE_SECONDS == 4795
    assert STRUCTURED_STAGE_WRAPPER_DEADLINE_SECONDS == 4825
    assert _provider_timeout_seconds(True) == 30
    assert _provider_timeout_seconds(False) == 300
    assert PROVIDER_CALL_DEADLINE_SECONDS > PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS


def test_four_call_structured_correction_fits_derived_stage_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    request: pytest.FixtureRequest,
) -> None:
    per_call_seconds = 0.04
    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )
    stage_deadline_seconds = _structured_stage_deadline_seconds(
        0,
        provider_call_deadline_seconds=per_call_seconds,
        finalization_grace_seconds=0.02,
    )
    monkeypatch.setattr(
        runtime_module,
        "_structured_stage_deadline_seconds",
        lambda _transport_retries: stage_deadline_seconds,
    )
    monkeypatch.setattr(
        runtime_module,
        "STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS",
        0.02,
    )

    class FourCallCorrectionApp:
        def __init__(self) -> None:
            self.calls = 0

        async def arun(self, _prompt: str, **_kwargs: object) -> dict[str, int]:
            for _ in range(4):
                await asyncio.sleep(per_call_seconds)
                self.calls += 1
            return {"calls": self.calls}

    app = FourCallCorrectionApp()
    result = runtime._submit_to_event_loop(runtime._arun_app(app, "fixture"))

    assert result == {"calls": 4}
    assert app.calls == 4
    assert stage_deadline_seconds > 4 * per_call_seconds


def test_structured_stage_timeout_recovers_committed_usage_without_outer_retry(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class StageTimeoutApp:
        async def arun(self, _prompt: str, **kwargs: object) -> object:
            result_path = Path(str(kwargs["result_out"]))
            result_path.write_text(
                json.dumps(
                    {
                        "status": "cancelled",
                        "output": None,
                        "error": {
                            "code": "cancelled",
                            "message": "local stage deadline cancelled the run",
                        },
                        "usage": [
                            {
                                "model_call_id": "completed-before-stage-timeout",
                                "status": "completed",
                                "input_tokens": 100,
                                "output_tokens": 10,
                            },
                            {
                                "model_call_id": "cancelled-at-stage-timeout",
                                "status": "cancelled",
                                "input_tokens": None,
                                "output_tokens": None,
                                "source": "unavailable",
                                "unavailable_reason": "adapter_did_not_expose_provider_usage",
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            raise StructuredStageTimeout("fixture structured stage timeout")

    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )
    runtime._app = lambda *_args, **_kwargs: StageTimeoutApp()

    outcome = runtime._call_unlocked(
        kind="fixture_stage",
        schema=FixtureResponse,
        system_prompt="fixture system prompt",
        prompt="fixture prompt",
        artifact_id="fixture-stage-timeout",
        retry_cell_on_provider_error=True,
    )

    assert outcome.status == "failed"
    assert len(outcome.attempts) == 1
    assert outcome.attempts[0]["provider_error"] is False
    assert outcome.attempts[0]["error"]["code"] == "structured_stage_timeout"
    assert outcome.attempts[0]["usage_count"] == 2
    assert outcome.attempts[0]["usage_recovery"]["status"] == "recovered"
    assert outcome.result["status"] == "cancelled"
    assert outcome.result["wrapper_error"]["code"] == "structured_stage_timeout"
    assert len(outcome.usage) == 2
    assert outcome.usage[0]["cost_counted"] is True
    assert outcome.usage[0]["billing_disposition"] == "billable"
    assert outcome.cost["attempts"][0]["total_usd"] > 0
    assert outcome.usage[1]["cost_counted"] is True
    assert outcome.usage[1]["billing_disposition"] == "billable"
    assert outcome.cost["attempts"][1]["eligible"] is False
    assert outcome.cost["attempts"][1]["total_usd"] is None
    assert outcome.cost["total_usd"] > 0
    assert outcome.cost["unpriced_usage_count"] == 1


def test_exception_provider_failure_recovers_usage_and_exempts_only_retried_row(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class ProviderFailureApp:
        async def arun(self, _prompt: str, **kwargs: object) -> object:
            result_path = Path(str(kwargs["result_out"]))
            result_path.write_text(
                json.dumps(
                    {
                        "status": "failed",
                        "output": None,
                        "error": {
                            "code": "provider_timeout",
                            "message": "fixture provider timeout",
                        },
                        "usage": [
                            {
                                "model_call_id": "failed-provider-attempt",
                                "status": "failed",
                                "input_tokens": 100,
                                "output_tokens": 0,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            raise AgentError(
                "provider_timeout",
                "fixture provider timeout",
                details={"source": "provider"},
            )

    success_result = SimpleNamespace(
        status="success",
        output=FixtureResponse(value="ok"),
        error=None,
        usage=[
            {
                "model_call_id": "successful-provider-attempt",
                "status": "completed",
                "input_tokens": 120,
                "output_tokens": 12,
            }
        ],
        to_dict=lambda: {
            "status": "success",
            "output": {"value": "ok"},
            "error": None,
        },
    )
    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )
    app_count = 0

    class SuccessApp:
        async def arun(self, *_args: object, **_kwargs: object) -> object:
            return success_result

    def app_factory(*_args: object, **_kwargs: object) -> object:
        nonlocal app_count
        app_count += 1
        return ProviderFailureApp() if app_count == 1 else SuccessApp()

    runtime._app = app_factory
    outcome = runtime._call_unlocked(
        kind="fixture_provider_retry",
        schema=FixtureResponse,
        system_prompt="fixture system prompt",
        prompt="fixture prompt",
        artifact_id="fixture-provider-retry",
        retry_cell_on_provider_error=True,
    )

    assert outcome.status == "success"
    assert len(outcome.attempts) == 2
    assert outcome.attempts[0]["provider_error"] is True
    assert outcome.attempts[0]["usage_recovery"]["status"] == "recovered"
    assert outcome.usage[0]["cost_counted"] is False
    assert outcome.usage[0]["billing_disposition"] == "provider_error_retry_exempt"
    assert outcome.usage[1]["cost_counted"] is True
    assert outcome.usage[1]["billing_disposition"] == "billable"
    assert outcome.cost["eligible"] is True
    assert outcome.cost["attempts"][0]["total_usd"] == 0.0
    assert outcome.cost["attempts"][1]["total_usd"] > 0


def test_structured_stage_timeout_without_result_records_unknown_billable_usage(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class StageTimeoutWithoutResultApp:
        async def arun(self, _prompt: str, **_kwargs: object) -> object:
            raise StructuredStageTimeout("fixture timeout before result commit")

    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )
    runtime._app = lambda *_args, **_kwargs: StageTimeoutWithoutResultApp()

    outcome = runtime._call_unlocked(
        kind="fixture_stage_without_result",
        schema=FixtureResponse,
        system_prompt="fixture system prompt",
        prompt="fixture prompt",
        artifact_id="fixture-stage-without-result",
        retry_cell_on_provider_error=True,
    )

    assert len(outcome.attempts) == 1
    assert outcome.attempts[0]["provider_error"] is False
    assert outcome.attempts[0]["usage_recovery"]["status"] == "unavailable"
    assert outcome.usage == [
        {
            "model_call_id": None,
            "status": "cancelled",
            "input_tokens": None,
            "output_tokens": None,
            "source": "unavailable",
            "unavailable_reason": "result_artifact_missing",
            "cost_counted": True,
            "billing_disposition": "billable_usage_unavailable",
            "outer_attempt": 1,
        }
    ]
    assert outcome.cost["eligible"] is False
    assert outcome.cost["total_usd"] == 0.0
    assert outcome.cost["unpriced_usage_count"] == 1


def test_local_schema_failure_does_not_duplicate_in_memory_usage(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    invalid_result = SimpleNamespace(
        status="success",
        output={},
        error=None,
        usage=[
            {
                "model_call_id": "schema-failure-call",
                "status": "completed",
                "input_tokens": 100,
                "output_tokens": 10,
            }
        ],
        to_dict=lambda: {
            "status": "success",
            "output": {},
            "error": None,
        },
    )
    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )

    class InvalidResultApp:
        async def arun(self, *_args: object, **_kwargs: object) -> object:
            return invalid_result

    runtime._app = lambda *_args, **_kwargs: InvalidResultApp()

    outcome = runtime._call_unlocked(
        kind="fixture_local_schema_failure",
        schema=FixtureResponse,
        system_prompt="fixture system prompt",
        prompt="fixture prompt",
        artifact_id="fixture-local-schema-failure",
        retry_cell_on_provider_error=True,
    )

    assert outcome.status == "failed"
    assert len(outcome.attempts) == 1
    assert outcome.attempts[0]["provider_error"] is False
    assert outcome.attempts[0]["usage_count"] == 1
    assert outcome.attempts[0]["usage_recovery"]["source"] == (
        "in_memory_public_result"
    )
    assert len(outcome.usage) == 1
    assert outcome.usage[0]["model_call_id"] == "schema-failure-call"
    assert outcome.cost["eligible"] is True
    assert outcome.cost["total_usd"] > 0


def test_schema_validation_failures_are_typed_and_persisted(
    tmp_path: Path,
    request: pytest.FixtureRequest,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    audit_records = [
        {
            "record": "action",
            "record_type": "action",
            "turn": 2,
            "tool_call_id": "fixture-tool-call",
            "arguments": {},
        }
    ]
    failures = _schema_validation_failures(
        audit_records,
        FixtureResponse,
        outer_attempt=1,
    )
    assert len(failures) == 1
    assert failures[0].turn == 2
    assert failures[0].error_count == 1
    assert "value" in failures[0].validation_error

    class SchemaFailureApp:
        async def arun(self, _prompt: str, **kwargs: object) -> object:
            audit_path = Path(str(kwargs["audit_out"]))
            audit_path.write_text(
                json.dumps(audit_records[0]) + "\n",
                encoding="utf-8",
            )
            return SimpleNamespace(
                status="failed",
                output=None,
                error={
                    "code": "limit_exceeded",
                    "message": "fixture schema turns exhausted",
                },
                usage=[],
                to_dict=lambda: {
                    "status": "failed",
                    "output": None,
                    "error": {
                        "code": "limit_exceeded",
                        "message": "fixture schema turns exhausted",
                    },
                },
            )

    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
        request=request,
    )
    runtime._app = lambda *_args, **_kwargs: SchemaFailureApp()
    outcome = runtime._call_unlocked(
        kind="fixture_schema_audit",
        schema=FixtureResponse,
        system_prompt="fixture system prompt",
        prompt="fixture prompt",
        artifact_id="fixture-schema-audit",
        retry_cell_on_provider_error=True,
    )

    assert outcome.status == "failed"
    assert outcome.schema_validation_failures == failures
    failure_path = Path(
        outcome.attempts[0]["schema_validation_failure_path"]
    )
    bundle = StructuredSchemaValidationBundle.model_validate_json(
        failure_path.read_text(encoding="utf-8")
    )
    assert bundle.failures == tuple(failures)
    assert "value" in bundle.failures[0].errors_json


def test_provider_error_classification_uses_typed_ownership_not_message_text() -> None:
    assert _is_provider_error({"code": "provider_error"}) is True
    assert _is_provider_error(
        {"code": "runtime_error", "details": {"source": "provider"}}
    ) is True
    assert _is_provider_error(
        {
            "code": "structured_output_invalid",
            "message": "local schema bug mentions provider timeout",
        }
    ) is False
    assert _is_provider_error(
        {
            "code": "structured_output_invalid",
            "details": {
                "source": "runtime",
                "type": "ProviderCallTimeout",
            },
        }
    ) is True
    assert _is_provider_error(
        {"code": "ValueError", "message": "timeout field is invalid", "phase": "local_runtime"}
    ) is False


def test_pair_failure_receipts_are_written_for_all_cells(tmp_path: Path) -> None:
    error = RuntimeError("fixture pair failure")
    run_identity = {
        "run_id": "0" * 32,
        "run_contract_hash": "sha256:" + "0" * 64,
        "source_provenance": {
            "source_commit": "0" * 40,
            "source_branch": "fixture",
            "source_dirty": False,
            "reason": "Fixture source provenance.",
            "basis": "provider-free test fixture",
        },
        "pair_input_hashes": {},
    }
    for round_index in (1, 2, 3):
        _failure_method_cell(
            pair_id="0000",
            round_index=round_index,
            output_root=tmp_path,
            error=error,
            run_identity=run_identity,
        )
    assert len(list((tmp_path / "method" / "0000").glob("round-*.json"))) == 3
    assert not (tmp_path / "judge").exists()


def test_provider_free_run_manifest_resume_and_concurrent_atomic_writes(tmp_path: Path) -> None:
    run_id = "2" * 32
    summary = run_experiment(
        report_root=REPORT_ROOT,
        output_dir=tmp_path,
        profile="fixture",
        rounds=1,
        pair_ids=["0004", "0023"],
        workers=2,
        run_id=run_id,
    )
    run_root = tmp_path / run_id
    manifest = json.loads(
        (run_root / "run_manifest.json").read_text(encoding="utf-8")
    )

    assert summary["run_id"] == run_id
    assert summary["artifact_root"] == str(run_root.resolve())
    assert manifest["workers"] == 2
    assert manifest["retry_policy"]["stream_first_byte_timeout_seconds"] == 30
    assert manifest["retry_policy"]["provider_call_total_timeout_seconds"] == 300
    assert manifest["retry_policy"]["structured_model_call_reservation_limit"] == 12
    assert manifest["retry_policy"]["structured_stage_retry_delay_budget_seconds"] == 1165
    assert manifest["retry_policy"]["structured_stage_finalization_grace_seconds"] == 30
    assert manifest["retry_policy"]["structured_stage_timeout_seconds"] == 4795
    assert manifest["retry_policy"]["structured_stage_wrapper_timeout_seconds"] == 4825
    assert manifest["retry_policy"]["structured_stage_timeout_owner"] == (
        "local_runtime"
    )
    assert manifest["retry_policy"]["structured_stage_timeout_outer_retry"] is False
    assert manifest["retry_policy"]["non_stream_provider_timeout_seconds"] == 300
    assert manifest["retry_policy"]["unavailable_non_provider_usage"] == (
        "cost_ineligible_not_zero"
    )
    assert manifest["prompt_schema_hash"].startswith("sha256:")
    assert manifest["input_data_hash"].startswith("sha256:")
    assert manifest["pair_input_hashes"].keys() == {"0004", "0023"}
    assert len(list((run_root / "method").glob("*/round-1.json"))) == 2
    assert not (run_root / "judge").exists()
    assert not (run_root / "llm" / "judge").exists()
    assert "judge_cost_usd" not in summary
    assert {"hit", "false_positive", "precision"}.isdisjoint(summary["metrics"])
    assert not list(run_root.rglob("*.tmp"))
    audit_files = list((run_root / "audit_bundles").glob("*.json"))
    assert audit_files == []
    for method_path in (run_root / "method").glob("*/round-1.json"):
        cell = json.loads(method_path.read_text(encoding="utf-8"))
        assert cell["report_issue_clusters"] == []
        assert all(
            record["witness_level"] == "W0"
            for record in cell["evidence_records"]
        )
        assert all(
            "typed semantic key" in record["binding"]["reason"]
            for record in cell["evidence_records"]
        )

    resumed = run_experiment(
        report_root=REPORT_ROOT,
        output_dir=tmp_path,
        profile="fixture",
        rounds=1,
        pair_ids=["0004", "0023"],
        workers=2,
        run_id=run_id,
        resume=True,
    )
    assert resumed["run_id"] == run_id
    assert resumed["resume"] is True

    stale_path = run_root / "method" / "0004" / "round-1.json"
    stale_payload = json.loads(stale_path.read_text(encoding="utf-8"))
    stale_payload["schema"] = "evidence-discovery.method_cell.v1"
    stale_path.write_text(
        json.dumps(stale_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    repaired = run_experiment(
        report_root=REPORT_ROOT,
        output_dir=tmp_path,
        profile="fixture",
        rounds=1,
        pair_ids=["0004", "0023"],
        workers=2,
        run_id=run_id,
        resume=True,
    )
    current = json.loads(stale_path.read_text(encoding="utf-8"))
    stale_receipts = list((run_root / "stale").rglob("round-1.json"))
    assert repaired["run_id"] == run_id
    assert current["schema"] == "evidence-discovery.method_cell.v8"
    assert stale_receipts
    assert any(
        json.loads(path.read_text(encoding="utf-8"))["schema"]
        == "evidence-discovery.method_cell.v1"
        for path in stale_receipts
    )


def test_method_terminal_smoke_exports_w2_release_without_builtin_judge(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fixture_method_cell(
        *,
        pair: object,
        round_index: int,
        runtime: object,
        output_root: Path,
        run_identity: dict[str, object] | None = None,
    ) -> dict[str, object]:
        del runtime
        assert run_identity is not None
        transition = pair.model.transitions[0]
        candidate = _candidate(
            pair,
            predicate_id="S2",
            inputs={
                "source": transition.source,
                "target": transition.target,
                "scope": "closed_fcstm",
            },
            refs=[transition.ref],
            expected="The required executable transition must be present.",
            observed="The deterministic fixture establishes that it is absent.",
        )
        binding = bind_candidate(candidate, pair.model)
        obligation_id = f"{pair.pair_id}:r{round_index}:fixture-w2"
        plan = compile_plan(
            candidate,
            binding,
            load_registry(),
            obligation_id=obligation_id,
            round_index=round_index,
            model=pair.model,
            model_hash=pair.hashes["fcstm"],
        )
        receipt = RawReceipt(
            receipt_id=f"{obligation_id}:receipt",
            backend="fixture",
            terminal_state="completed",
            verdict="false",
            reason="The provider-free backend fixture returns a concrete violation.",
            basis="fixed deterministic terminal-smoke fixture",
            counterexample=[
                {"source": transition.source, "target": transition.target}
            ],
        )
        record = build_evidence_record(
            pair=pair,
            obligation_id=obligation_id,
            candidate=candidate,
            binding=binding,
            plan=plan,
            receipt=receipt,
            source_attribution={
                "requirement": {"path": "fixture:nl"},
                "model": {"hash": pair.hashes["fcstm"]},
            },
            retry_records=[],
            semantic_adjudication=SemanticAdjudication(
                obligation_id=obligation_id,
                grounding="established",
                violated_obligation="The exact executable transition obligation is violated.",
                strongest_defeater=None,
                defeater_kind="none",
                defeater_disposition="defeated",
                reason="The fixture supplies an established obligation and exact typed binding.",
                basis="fixed NL, model, predicate, and backend fixture",
            ),
        )
        record["d_level"] = "D2"
        record["issue_emitted"] = True
        audit_bundle = dict(record["audit_bundle"])
        audit_bundle["issue_emitted"] = True
        audit_bundle = validate_and_hash_w2_audit_bundle(audit_bundle)
        audit_path = output_root / "audit_bundles" / f"{obligation_id}.json"
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        audit_path.write_text(
            json.dumps(audit_bundle, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        record["audit_bundle"] = audit_bundle
        record["audit_bundle_path"] = str(audit_path)
        release = {
            "issue_id": f"{pair.pair_id}:r{round_index}:issue:fixture-w2",
            "title": "Required executable transition is absent",
            "requirement_quote": "The controller shall provide the required transition.",
            "locus_kind": "transition",
            "locus_names": [transition.source, transition.target],
            "property": "transition_endpoints",
            "violation_direction": "missing",
            "predicate_id": "S2",
            "predicate_inputs": plan.inputs.model_dump(mode="json"),
            "element_refs": [transition.ref],
            "source_refs": ["fixture:nl", transition.ref],
            "expected": candidate.expected,
            "observed": candidate.observed,
            "strongest_rebuttal": None,
            "d_level": "D2",
            "witness_level": "W2",
            "candidate_reason": "The exact typed obligation and backend result establish the issue.",
            "candidate_basis": "fixed provider-free W2 terminal fixture",
            "reason": "The D2/W2 issue is eligible for external evaluation.",
            "basis": "method-owned D/W publication receipt",
        }
        cell = MethodCellReceipt(
            schema="evidence-discovery.method_cell.v8",
            run_id=str(run_identity["run_id"]),
            run_contract_hash=str(run_identity["run_contract_hash"]),
            source_provenance=run_identity["source_provenance"],
            pair_id=pair.pair_id,
            pair_input_hash=pair.context_manifest.manifest_hash,
            round=round_index,
            status="completed",
            prompt_hash="sha256:" + "1" * 64,
            context_manifest=pair.context_manifest.model_dump(mode="json"),
            input_hashes=dict(pair.hashes),
            stage_outputs={"fixture": {"release_count": 1}},
            stage_receipts=[],
            model_output={
                "issues": [release],
                "reason": "The fixed fixture emitted one issue.",
                "basis": "provider-free method terminal smoke",
            },
            llm_calls=[],
            llm_call={
                "status": "success",
                "usage": [],
                "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
                "reason": "No provider call was required.",
                "basis": "fixed provider-free method stub",
            },
            eligible=True,
            eligibility_reasons=["fixed_provider_free_terminal_fixture"],
            evidence_records=[record],
            report_issue_clusters=[release],
            errors=[],
            reason="The method fixture completed with one release.",
            basis="fixed provider-free method terminal smoke",
        ).model_dump(mode="json")
        method_path = (
            output_root / "method" / pair.pair_id / f"round-{round_index}.json"
        )
        method_path.parent.mkdir(parents=True, exist_ok=True)
        method_path.write_text(
            json.dumps(cell, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return cell

    monkeypatch.setattr(runner_module, "_method_cell", fixture_method_cell)
    run_id = "3" * 32
    summary = run_experiment(
        report_root=REPORT_ROOT,
        output_dir=tmp_path,
        profile="fixture",
        rounds=1,
        pair_ids=["0004"],
        workers=1,
        run_id=run_id,
    )
    run_root = tmp_path / run_id
    method_path = run_root / "method" / "0004" / "round-1.json"
    status = json.loads(
        (run_root / "pairs" / "0004" / "status.json").read_text(encoding="utf-8")
    )
    method = json.loads(method_path.read_text(encoding="utf-8"))
    audit_files = list((run_root / "audit_bundles").glob("*.json"))

    assert summary["status"] == "completed"
    assert status["status"] == "completed"
    assert len(method["report_issue_clusters"]) == 1
    assert len(audit_files) == 1
    finalized_audit = json.loads(audit_files[0].read_text(encoding="utf-8"))
    assert finalized_audit["judge_receipt"]["status"] == "pending_independent_judge"
    assert finalized_audit["method_receipt"]["status"] == "completed"
    assert not (run_root / "judge").exists()
    assert not (run_root / "llm" / "judge").exists()
    assert "judge_cost_usd" not in summary
    assert {"hit", "false_positive", "precision"}.isdisjoint(summary["metrics"])

    reports, adapter_audit, round_no, pair_id = adapt_evidence_discovery_release(
        method_path,
        (),
    )
    assert (round_no, pair_id) == (1, "0004")
    assert len(reports) == 1
    assert reports[0].claim == "Required executable transition is absent"
    assert adapter_audit.source_format == "evidence_discovery_release"
