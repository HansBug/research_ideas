from __future__ import annotations

import hashlib
import json
import re
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
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.compiler.lowering import PredicatePlan
from pipeline.evidence_discovery.evidence.audit_bundle import W2AuditBundle
from pipeline.evidence_discovery.evidence.receipts import RawReceipt
from pipeline.evidence_discovery.evidence.witness_levels import (
    build_evidence_record,
    calculate_witness_level,
)
from pipeline.evidence_discovery.inputs import load_pair, parse_fcstm
from pipeline.evidence_discovery.orchestration.contracts import (
    IndependentJudgeReceipt,
    MethodCellReceipt,
    PairRunStatus,
    RunManifest,
    RunSummaryReceipt,
    SourceProvenance,
)
from pipeline.evidence_discovery.orchestration.runner import (
    ExactJudgeResponse,
    JudgeRelationAssessment,
    JudgeResponse,
    LedgerAssessment,
    ReleaseAssessment,
    _d_decision_consistency_errors,
    _deduplicate_release_issues,
    _enrich_candidate,
    _failure_judge_payload,
    _failure_method_cell,
    _finalize_w2_audit_links,
    _grounding_response_contract,
    _judge_issue_projection,
    _judge_pair,
    _judge_prompt,
    _judge_response_contract,
    _judge_shape_errors,
    _materialize_exact_s2_inventory_candidates,
    _merge_grounding_contracts,
    _metrics,
    _normalize_grounding_exact_facts,
    _normalize_judge_shape,
    _prepare_candidate,
    _prepared_is_finding_candidate,
    run_experiment,
)
from pipeline.evidence_discovery.orchestration.runtime import (
    JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
    MAX_STRUCTURED_OUTPUT_TOKENS,
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    STRUCTURED_STAGE_DEADLINE_SECONDS,
    FixtureStructuredRuntime,
    PublicStructuredRuntime,
    StructuredCallOutcome,
    StructuredStageTimeout,
    _annotate_usage_billing,
    _cost_for_usage,
    _is_provider_error,
    _provider_timeout_seconds,
    _structured_stage_deadline,
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
    GroundingUnresolved,
    MethodResponse,
    NLContract,
    NLContractResponse,
    NLTransitionAlternative,
    NLTransitionGroup,
    SemanticAdjudication,
    adjudicate_disposition,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_grounding_prompt,
    build_method_prompt,
    canonicalize_grounding_response,
    fallback_grounding,
    normalize_contract_state_roles,
    resolve_transition_ref,
)
from pipeline.evidence_discovery.semantics.binding import BindingResult
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


def test_predicate_plan_uses_discriminated_inputs_and_invalid_shape_downgrades() -> None:
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

    assert plan.supported is False
    assert plan.inputs.predicate_id == "unsupported"
    assert plan.inputs.claimed_predicate_id == "S5"
    assert plan.inputs.validation_errors
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
        "schema": "paper1.evidence_discovery.method_cell.v8",
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
    judge = {
        "schema": "paper1.evidence_discovery.independent_judge.v5",
        "run_id": "1" * 32,
        "run_contract_hash": "sha256:" + "1" * 64,
        "status": "completed",
        "eligible": True,
        "adjudication_mode": "pair_wide",
        "reason": "Fixture judge completed.",
        "basis": "Fixture terminal receipt.",
    }
    _finalize_w2_audit_links(
        output_root=tmp_path,
        pair_id="0000",
        rounds_data=[cell],
        judge=judge,
    )
    finalized = json.loads(audit_path.read_text(encoding="utf-8"))
    assert finalized["pre_finalization_audit_hash"] == audit_hash
    assert finalized["audit_finalization"]["pre_finalization_audit_hash"] == audit_hash
    assert finalized["audit_hash"] != audit_hash
    W2AuditBundle.model_validate(finalized)


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


def test_issue_189_distinguishes_undercutting_d1_from_rebutting_d0() -> None:
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
        basis="issue #189 typed defeater fixture",
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


def test_both_v27_grounding_lenses_contribute_exact_candidates() -> None:
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


def test_judge_shape_normalization_does_not_rewrite_decision_fields() -> None:
    ledger = [{"id": "L-1", "pair": "0000"}]
    release = [{"issue_id": "0000:r1:issue:0"}]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="L-1",
                hit_r1=False,
                matched_issue_ids=["0000:r1:issue:0"],
                reason="The fixture matched the exact issue ID.",
                basis="exact relation fixture",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0000:r1:issue:0",
                accounted_ledger_ids=["L-1"],
                is_false_positive=True,
                reason="The fixture accounted for the exact ledger ID.",
                basis="exact relation fixture",
            )
        ],
        relation_assessments=[
            JudgeRelationAssessment(
                ledger_id="L-1",
                issue_id="0000:r1:issue:0",
                relation="exact",
                reason="The exact locus, property, scope, and direction match.",
                basis="provider-free typed judge relation fixture",
            )
        ],
        reason="Fixture response.",
        basis="Fixture response basis.",
    )
    normalized = _normalize_judge_shape(response, ledger, release, 1)
    errors = _judge_shape_errors(normalized, ledger, release, 1)
    assert normalized.ledger_assessments[0].hit_r1 is False
    assert normalized.release_assessments[0].is_false_positive is True
    assert any("hit_r1 must agree" in error for error in errors)
    assert any("is_false_positive must equal" in error for error in errors)


def test_judge_shape_rejects_asymmetric_exact_relations() -> None:
    ledger = [{"id": "L-1", "pair": "0000"}]
    release = [{"issue_id": "0000:r1:issue:0"}]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="L-1",
                matched_issue_ids=[],
                reason="The ledger side reports no match.",
                basis="fixture ledger relation surface",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0000:r1:issue:0",
                accounted_ledger_ids=["L-1"],
                is_false_positive=False,
                reason="The release side reports a match.",
                basis="fixture release relation surface",
            )
        ],
        reason="The fixture intentionally disagrees across relation directions.",
        basis="provider-free asymmetric relation fixture",
    )

    normalized = _normalize_judge_shape(response, ledger, release, 1)
    errors = _judge_shape_errors(normalized, ledger, release, 1)
    assert any("same exact relation pairs" in error for error in errors)
    assert any(
        'release-side-only=[["L-1", "0000:r1:issue:0"]]' in error
        for error in errors
    )


def test_runtime_judge_contract_rejects_identity_deduplication() -> None:
    schema = _judge_response_contract(
        ledger_ids=("INS-0029-01", "INS-0029-05"),
        release_ids=("0029:r1:issue:7", "0029:r1:issue:12"),
        rounds=1,
    )
    json_schema = schema.model_json_schema()
    ledger_property = json_schema["properties"]["ledger_assessments"]
    release_property = json_schema["properties"]["release_assessments"]
    assert ledger_property["minItems"] == ledger_property["maxItems"] == 2
    assert release_property["minItems"] == release_property["maxItems"] == 2
    release_definition = release_property["items"]["$ref"].rsplit("/", 1)[-1]
    assert set(
        json_schema["$defs"][release_definition]["properties"]["issue_id"]["enum"]
    ) == {"0029:r1:issue:7", "0029:r1:issue:12"}

    payload = {
        "ledger_assessments": [
            {
                "ledger_id": ledger_id,
                "matched_issue_ids": [],
                "reason": "No exact release establishes this ledger item.",
                "basis": "Provider-free exact identity fixture.",
            }
            for ledger_id in ("INS-0029-01", "INS-0029-05")
        ],
        "release_assessments": [
            {
                "issue_id": issue_id,
                "accounted_ledger_ids": [],
                "is_false_positive": True,
                "reason": "This exact release identity has no hit-eligible relation.",
                "basis": "Provider-free exact identity fixture.",
            }
            for issue_id in ("0029:r1:issue:7", "0029:r1:issue:12")
        ],
        "relation_assessments": [],
        "reason": "Every exact ledger and release identity was retained.",
        "basis": "Provider-free exact identity fixture.",
    }
    validated = schema.model_validate(payload)
    assert isinstance(validated, ExactJudgeResponse)

    identity_deduplicated = dict(payload)
    identity_deduplicated["release_assessments"] = [
        payload["release_assessments"][1],
        payload["release_assessments"][1],
    ]
    with pytest.raises(
        ValidationError,
        match=r"missing=.*0029:r1:issue:7.*duplicates=.*0029:r1:issue:12",
    ):
        schema.model_validate(identity_deduplicated)


def test_runtime_judge_contract_rejects_asymmetric_accounting() -> None:
    schema = _judge_response_contract(
        ledger_ids=("L-1",),
        release_ids=("0000:r1:issue:0",),
        rounds=1,
    )
    with pytest.raises(ValidationError, match="same exact relation pairs"):
        schema.model_validate(
            {
                "ledger_assessments": [
                    {
                        "ledger_id": "L-1",
                        "matched_issue_ids": [],
                        "reason": "The ledger side reports no match.",
                        "basis": "Provider-free asymmetric fixture.",
                    }
                ],
                "release_assessments": [
                    {
                        "issue_id": "0000:r1:issue:0",
                        "accounted_ledger_ids": ["L-1"],
                        "is_false_positive": False,
                        "reason": "The release side reports a match.",
                        "basis": "Provider-free asymmetric fixture.",
                    }
                ],
                "relation_assessments": [],
                "reason": "The fixture intentionally disagrees across directions.",
                "basis": "Provider-free asymmetric fixture.",
            }
        )


def test_0053_typed_judge_relation_rejects_wrong_source_narrow_manifestation() -> None:
    ledger = [{"id": "DIFF-0053-01", "pair": "0053"}]
    release = [
        {"issue_id": "0053:r1:issue:correct-sequence"},
        {"issue_id": "0053:r1:issue:wrong-owner-source"},
    ]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="DIFF-0053-01",
                hit_r1=True,
                matched_issue_ids=[
                    "0053:r1:issue:correct-sequence",
                ],
                reason="Only the exact cross-wrapper sequence has the ledger property.",
                basis="provider-free v27 positive/negative relation fixture",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0053:r1:issue:correct-sequence",
                accounted_ledger_ids=["DIFF-0053-01"],
                is_false_positive=False,
                reason="The exact sequence establishes the ledger defect.",
                basis="PumpState to WaterState to MethaneState relation",
            ),
            ReleaseAssessment(
                issue_id="0053:r1:issue:wrong-owner-source",
                accounted_ledger_ids=[],
                is_false_positive=True,
                reason="This nearby issue shares a global causal context only.",
                basis="PumpControl to WaterState wrong-source relation",
            ),
        ],
        relation_assessments=[
            JudgeRelationAssessment(
                ledger_id="DIFF-0053-01",
                issue_id="0053:r1:issue:correct-sequence",
                relation="semantic_equivalent",
                reason="The source sequence, cross-wrapper scope, and missing connectivity property are equivalent.",
                basis="typed v27 correct-sequence positive fixture",
            ),
            JudgeRelationAssessment(
                ledger_id="DIFF-0053-01",
                issue_id="0053:r1:issue:wrong-owner-source",
                relation="partial_overlap",
                reason="The owner-source endpoint has the wrong locus and does not establish wrapper mutual unreachability.",
                basis="typed v27 PumpControl-source negative fixture",
            ),
        ],
        reason="The fixture distinguishes exact semantics from a shared-cause narrow manifestation.",
        basis="v27 0053 positive and negative examples",
    )

    normalized = _normalize_judge_shape(response, ledger, release, 1)

    assert not _judge_shape_errors(normalized, ledger, release, 1)
    assert normalized.ledger_assessments[0].matched_issue_ids == [
        "0053:r1:issue:correct-sequence"
    ]
    release_by_id = {
        item.issue_id: item for item in normalized.release_assessments
    }
    assert release_by_id["0053:r1:issue:correct-sequence"].is_false_positive is False
    assert release_by_id["0053:r1:issue:wrong-owner-source"].is_false_positive is True


def test_0046_d1_ambiguity_is_semantically_equivalent_not_partial_overlap() -> None:
    ledger = [
        {
            "id": "EIS-0046-02",
            "pair": "0046",
            "D": "D1",
            "D_basis": (
                "The primary reading requires three search-period state areas and finds "
                "the authored area structure short; a second competent reading counts "
                "three named operating states and remains satisfied."
            ),
            "summary": "The search-period operating scope does not realize three state areas.",
        }
    ]
    release = [
        {
            "issue_id": "0046:r1:issue:cardinality",
            "d_level": "D1",
            "locus_kind": "composite",
            "locus_names": ["UAVSwarmStateMachine"],
            "property": "cardinality",
            "violation_direction": "missing",
            "requirement_quote": "it operates within three different state areas",
            "expected": (
                "Within the target-search operating scope, UAVSwarmStateMachine must "
                "realize three state areas under the primary direct-child reading."
            ),
            "observed": "The complete author-source inventory realizes two such direct areas.",
            "strongest_rebuttal": (
                "The phrase may instead count three named operating states; that "
                "competent reading remains satisfied."
            ),
        }
    ]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="EIS-0046-02",
                hit_r1=True,
                matched_issue_ids=["0046:r1:issue:cardinality"],
                reason="Both sides represent the same search-scope D1 cardinality ambiguity.",
                basis="The primary three-area shortfall and compatible alternative reading align.",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0046:r1:issue:cardinality",
                accounted_ledger_ids=["EIS-0046-02"],
                is_false_positive=False,
                reason="The D1 release is semantically equivalent to the frozen D1 defect.",
                basis="Same owner, search scope, state-area cardinality, count, and direction.",
            )
        ],
        relation_assessments=[
            JudgeRelationAssessment(
                ledger_id="EIS-0046-02",
                issue_id="0046:r1:issue:cardinality",
                relation="semantic_equivalent",
                reason=(
                    "The surviving satisfying reading is part of the same D1 ambiguity, "
                    "not a locus or property mismatch."
                ),
                basis="Typed D1 ledger/release fields preserve compatible primary and alternative readings.",
            )
        ],
        reason="The provider-free fixture preserves D1 ambiguity without weakening semantic identity.",
        basis="0046 v27 positive cardinality relation fixture",
    )

    normalized = _normalize_judge_shape(response, ledger, release, 1)

    assert not _judge_shape_errors(normalized, ledger, release, 1)
    assert normalized.relation_assessments[0].relation == "semantic_equivalent"
    prompt = _judge_prompt(
        load_pair(REPORT_ROOT / "pairs" / "0046"),
        ledger,
        [{"round": 1, "report_issue_clusters": release}],
    )
    normalized_prompt = " ".join(prompt.split())
    assert "a surviving satisfying alternative is part of the same D1 defect" in normalized_prompt
    assert "must never repair a wrong source" in normalized_prompt
    assert "the ledger subsumes that candidate" in normalized_prompt
    assert "typed property and violation_direction are authoritative" in normalized_prompt
    assert "absence of a required construct is possible negative" in (
        DISCOVERY_GROUNDING_SYSTEM_PROMPT
    )


def test_aggregate_ledger_rejects_subset_candidate_subsumption() -> None:
    ledger = [{"id": "L-AGGREGATE", "pair": "0000"}]
    release = [
        {"issue_id": "0000:r1:issue:whole-scope"},
        {"issue_id": "0000:r1:issue:one-sibling"},
    ]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="L-AGGREGATE",
                hit_r1=True,
                matched_issue_ids=["0000:r1:issue:whole-scope"],
                reason="Only the whole-scope claim establishes every enumerated component.",
                basis="The ledger enumerates sibling scopes A and B.",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0000:r1:issue:whole-scope",
                accounted_ledger_ids=["L-AGGREGATE"],
                is_false_positive=False,
                reason="Unreachability of the common owner entails both sibling failures.",
                basis="The candidate claims that the owner containing A and B is unreachable.",
            ),
            ReleaseAssessment(
                issue_id="0000:r1:issue:one-sibling",
                accounted_ledger_ids=[],
                is_false_positive=True,
                reason="The candidate establishes A only and cannot account for sibling B.",
                basis="Its supplied locus and observed facts mention only A.",
            ),
        ],
        relation_assessments=[
            JudgeRelationAssessment(
                ledger_id="L-AGGREGATE",
                issue_id="0000:r1:issue:whole-scope",
                relation="candidate_subsumes_ledger",
                entailment_basis=(
                    "The candidate's own whole-owner unreachability claim entails that "
                    "both contained sibling scopes A and B are unreachable."
                ),
                reason="The whole-owner claim covers every ledger component.",
                basis="Typed owner scope contains both enumerated sibling scopes.",
            ),
            JudgeRelationAssessment(
                ledger_id="L-AGGREGATE",
                issue_id="0000:r1:issue:one-sibling",
                relation="ledger_subsumes_candidate",
                reason="The ledger includes sibling B, which the candidate does not establish.",
                basis="The candidate's supplied claim is limited to sibling A.",
            ),
        ],
        reason="The fixture separates complete logical entailment from a shared-cause subset.",
        basis="Provider-free aggregate-ledger positive and negative relation fixture.",
    )

    normalized = _normalize_judge_shape(response, ledger, release, 1)

    assert not _judge_shape_errors(normalized, ledger, release, 1)
    by_issue = {
        item.issue_id: item.relation for item in normalized.relation_assessments
    }
    assert by_issue["0000:r1:issue:whole-scope"] == "candidate_subsumes_ledger"
    assert by_issue["0000:r1:issue:one-sibling"] == "ledger_subsumes_candidate"
    prompt = _judge_prompt(
        load_pair(REPORT_ROOT / "pairs" / "0000"),
        ledger,
        [{"round": 1, "report_issue_clusters": release}],
    )
    normalized_prompt = " ".join(prompt.split())
    assert "a candidate that covers only a subset cannot subsume it" in normalized_prompt
    assert "Do not use ledger detail to add an absent sibling" in normalized_prompt
    assert "never semantic_equivalent" in normalized_prompt
    assert "recount hits and misses" in normalized_prompt


def test_aggregate_ledger_rejects_collective_subset_accounting() -> None:
    ledger = [{"id": "L-AGGREGATE", "pair": "0000"}]
    release = [
        {"issue_id": "0000:r1:issue:sibling-a"},
        {"issue_id": "0000:r1:issue:sibling-b"},
    ]
    response = JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id="L-AGGREGATE",
                hit_r1=True,
                matched_issue_ids=[
                    "0000:r1:issue:sibling-a",
                    "0000:r1:issue:sibling-b",
                ],
                reason="The invalid fixture unions two subset candidates.",
                basis="The ledger enumerates sibling scopes A and B.",
            )
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id="0000:r1:issue:sibling-a",
                accounted_ledger_ids=["L-AGGREGATE"],
                is_false_positive=False,
                reason="The invalid fixture accounts subset A.",
                basis="The candidate establishes sibling A only.",
            ),
            ReleaseAssessment(
                issue_id="0000:r1:issue:sibling-b",
                accounted_ledger_ids=["L-AGGREGATE"],
                is_false_positive=False,
                reason="The invalid fixture accounts subset B.",
                basis="The candidate establishes sibling B only.",
            ),
        ],
        relation_assessments=[
            JudgeRelationAssessment(
                ledger_id="L-AGGREGATE",
                issue_id="0000:r1:issue:sibling-a",
                relation="ledger_subsumes_candidate",
                reason="The ledger also requires sibling B.",
                basis="The candidate scope contains sibling A only.",
            ),
            JudgeRelationAssessment(
                ledger_id="L-AGGREGATE",
                issue_id="0000:r1:issue:sibling-b",
                relation="ledger_subsumes_candidate",
                reason="The ledger also requires sibling A.",
                basis="The candidate scope contains sibling B only.",
            ),
        ],
        reason="The fixture reproduces invalid collective subset accounting.",
        basis="Provider-free aggregate-ledger shape regression.",
    )

    normalized = _normalize_judge_shape(response, ledger, release, 1)
    errors = _judge_shape_errors(normalized, ledger, release, 1)

    relation_error = next(
        error for error in errors if "typed hit relations" in error
    )
    assert "0000:r1:issue:sibling-a" in relation_error
    assert "0000:r1:issue:sibling-b" in relation_error
    assert "accounting-only" in relation_error


def test_candidate_subsumes_ledger_requires_entailment_basis() -> None:
    with pytest.raises(ValidationError, match="entailment_basis"):
        JudgeRelationAssessment(
            ledger_id="ledger-1",
            issue_id="issue-1",
            relation="candidate_subsumes_ledger",
            reason="The fixture deliberately omits logical entailment.",
            basis="provider-free invalid judge relation",
        )


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
    assert "judge examples" in prompt
    assert "S2={source, target, scope}" in prompt
    assert "set predicate_id to null" in prompt


def test_judge_prompt_keeps_one_assessment_per_ledger_object() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0004")
    ledger = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(
            encoding="utf-8"
        )
    )
    ledger_items = [
        item for item in ledger["items"].values() if item.get("pair") == "0004"
    ]
    prompt = _judge_prompt(
        pair,
        ledger_items,
        [
            {
                "round": 1,
                "stage_receipts": [{"stage_name": "execute_batch"}],
                "report_issue_clusters": [
                    {
                        "issue_id": "0004:r1:issue:0",
                        "contract_id": "NL-CONTRACT-NL1",
                        "locus_kind": "state",
                        "locus_names": ["Stopping"],
                        "property": "deadlock_freedom",
                        "violation_direction": "dead_end",
                        "title": "Stopping has no progress",
                        "requirement_quote": "The train can stop safely.",
                        "element_refs": ["state:Stopping"],
                        "source_refs": ["nl:NL1"],
                        "expected": "Stopping can make progress.",
                        "observed": "Stopping is a reachable non-final leaf.",
                        "strongest_rebuttal": "Stopping may be intended as terminal.",
                        "d_level": "D1",
                        "witness_level": "W1",
                        "reason": "The supplied facts support two competent readings.",
                        "basis": "final method publication",
                        "candidate_reason": (
                            "The complete aggregate covers display/update and "
                            "cancel/update for one typed data subject."
                        ),
                        "candidate_basis": (
                            "source_contract_ids=['NL-CONTRACT-NL5', "
                            "'NL-CONTRACT-NL6']; variable='cooking time'"
                        ),
                        "facet_count": 2,
                        "facet_issue_ids": [
                            "0004:r1:issue:0",
                            "0004:r1:issue:1",
                        ],
                        "contract_ids": [
                            "NL-CONTRACT-NL5",
                            "NL-CONTRACT-NL6",
                        ],
                        "plan": {"formal_program": "must not enter judge"},
                        "receipt": {"trace": ["must not enter judge"]},
                        "audit_bundle": {"audit_hash": "sha256:" + "1" * 64},
                        "audit_bundle_path": "/tmp/audit.json",
                    }
                ],
            }
        ],
    )

    assert len(ledger_items) == 3
    assert prompt.count('"id": "EIS-0004-01"') == 1
    normalized_prompt = " ".join(prompt.split())
    assert "exactly one ledger assessment for each supplied object" in normalized_prompt
    assert "Do not split one object into multiple assessments" in normalized_prompt
    assert '"stage_receipts"' not in prompt
    assert '"predicate_plan"' not in prompt
    assert '"backend_receipt"' not in prompt
    assert '"formal_program"' not in prompt
    assert '"trace"' not in prompt
    assert '"pre_finalization_audit_hash": "sha256:' in prompt
    assert "The complete aggregate covers display/update" in prompt
    assert "source_contract_ids=['NL-CONTRACT-NL5'" in prompt
    assert '"facet_count"' not in prompt
    assert '"facet_issue_ids"' not in prompt
    assert '"contract_ids"' not in prompt


def test_judge_projection_prefers_candidate_semantics_over_publication_status() -> None:
    projected = _judge_issue_projection(
        {
            "issue_id": "0035:r1:issue:aggregate",
            "contract_id": "NL-CONTRACT-NL5-DERIVED-DATA",
            "locus_kind": "variable",
            "locus_names": ["cooking time"],
            "property": "effect",
            "violation_direction": "wrong_effect",
            "expected": "Display/update and cancel/update must both be represented.",
            "observed": "The complete action/effect inventories are empty.",
            "reason": "A grounded violated obligation has no surviving defeater.",
            "basis": "D publication status",
            "candidate_reason": (
                "One aggregate release covers both supplied cooking-time clauses."
            ),
            "candidate_basis": (
                "source_contract_ids=['NL-CONTRACT-NL5', 'NL-CONTRACT-NL6']"
            ),
            "facet_count": 1,
            "facet_issue_ids": ["0035:r1:issue:aggregate"],
            "contract_ids": ["NL-CONTRACT-NL5-DERIVED-DATA"],
        }
    )

    assert projected["reason"] == (
        "One aggregate release covers both supplied cooking-time clauses."
    )
    assert projected["basis"] == (
        "source_contract_ids=['NL-CONTRACT-NL5', 'NL-CONTRACT-NL6']"
    )
    assert "facet_count" not in projected
    assert "facet_issue_ids" not in projected
    assert "contract_ids" not in projected


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
    assert "variable=`setpoint`" in CONTRACT_SYSTEM_PROMPT
    assert "owner-initial-to-ModeA, ModeA-to-ModeB, and ModeB-to-ModeC" in CONTRACT_SYSTEM_PROMPT
    assert "activity to be performed continuously or repeatedly" in CONTRACT_SYSTEM_PROMPT
    assert "segment already has a cardinality or structure contract" in CONTRACT_SYSTEM_PROMPT
    assert "structural-area primary reading" in CONTRACT_SYSTEM_PROMPT
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
    assert "Audit discourse-scoped transition groups" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "synthetic placeholders are not author-specified operating-state" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "an unreachable state that" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "not a deadlock/dead-end violation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "declared consumer with no consumer reachable" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "three independent frontier properties" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "For every supplied `termination` contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "For every transition group with multiple target alternatives" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "canonical author-source inventory" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "complete exact inventory" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "element_refs` contains" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Negative-property carrier example" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "must not emit a cardinality CandidateIssue" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "operates within three different state areas" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
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
    assert "Return sparse v27-style output" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
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
        basis="provider-free sparse v27 grounding fixture",
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
        reason="The fixture exercises the exact list-valued inputs observed in the Luna run.",
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

    chinese_reason = MethodResponse(issues=[], reason="中文理由", basis="中文依据")
    assert chinese_reason.reason == "中文理由"
    assert chinese_reason.basis == "中文依据"

    candidate_schema = CandidateIssue.model_json_schema()
    method_schema = MethodResponse.model_json_schema()
    judge_schema = JudgeResponse.model_json_schema()
    candidate_properties = candidate_schema["properties"]
    for field_name in (
        "contract_id", "locus_kind", "locus_names", "property",
        "violation_direction", "evidence_types", "title", "requirement_quote",
        "predicate_id", "predicate_inputs", "element_refs",
        "source_refs", "expected", "observed", "strongest_rebuttal", "reason", "basis",
    ):
        assert candidate_properties[field_name].get("description"), field_name
    for schema in (method_schema, judge_schema):
        for field_name, field in schema["properties"].items():
            assert field.get("description"), field_name
    for schema_name in ("LedgerAssessment", "ReleaseAssessment"):
        nested = judge_schema["$defs"][schema_name]
        assert nested["properties"]["reason"].get("description")
        assert nested["properties"]["basis"].get("description")
    release_schema = judge_schema["$defs"]["ReleaseAssessment"]["properties"]
    ledger_schema = judge_schema["$defs"]["LedgerAssessment"]["properties"]
    relation_schema = judge_schema["$defs"]["JudgeRelationAssessment"][
        "properties"
    ]
    assert "不得合并、去重或省略" in release_schema["issue_id"]["description"]
    assert "多个 subset release 的并集" in release_schema[
        "accounted_ledger_ids"
    ]["description"]
    assert "多个" in ledger_schema["matched_issue_ids"]["description"]
    assert "不能" in relation_schema["relation"]["description"]
    assert "must not describe the release as matching" in release_schema[
        "is_false_positive"
    ]["description"]
    assert "must not claim a semantic match" in release_schema["basis"][
        "description"
    ]
    assert "不按语义相似性 deduplicate" in judge_schema["properties"][
        "release_assessments"
    ]["description"]
    cardinality_schema = CardinalityDomainBinding.model_json_schema()
    assert "不能仅因某项活动发生在更深的子 composite" in cardinality_schema[
        "properties"
    ]["owner_source_id"]["description"]
    assert "contract's normative `scope_concept`" in (
        DISCOVERY_GROUNDING_SYSTEM_PROMPT
    )
    for model in (
        SourceProvenance,
        RunManifest,
        MethodCellReceipt,
        IndependentJudgeReceipt,
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

    assessment = LedgerAssessment(
        ledger_id="ledger-1",
        reason="This item matches the same locus and property.",
        basis="frozen ledger entry and method release surface",
    )
    release = ReleaseAssessment(
        issue_id="issue-1",
        is_false_positive=False,
        reason="A frozen ledger item accounts for this release issue.",
        basis="semantic identity review",
    )
    judged = JudgeResponse(
        ledger_assessments=[assessment],
        release_assessments=[release],
        reason="The supplied units were assessed.",
        basis="independent judge input",
    )
    assert judged.ledger_assessments[0].reason
    assert judged.release_assessments[0].basis


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
        basis="provider-free v27 transition-group fixture",
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
        basis="provider-free v27 target-identity fixture",
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
    assert "当前编号 segment" in defs["ContractBindingHint"]["properties"]["value"]["description"]
    assert "不能用稍后具名" in defs["NLTransitionAlternative"]["properties"]["target_name"]["description"]
    assert "不能把本段的 local-exit" in defs["NLContract"]["properties"]["normative_statement"]["description"]

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
    assert "deterministic containment expansion" in owner_description
    assert "若 source 本身是 owner" in owner_description


def test_v27_state_role_normalization_merges_only_exact_typed_progress_identity() -> None:
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


def test_v27_execute_boundary_excludes_only_completed_true_receipts() -> None:
    def prepared(terminal_state: str, verdict: str) -> dict:
        return {
            "receipt": RawReceipt(
                receipt_id=f"receipt:{terminal_state}:{verdict}",
                backend="provider-free-fixture",
                terminal_state=terminal_state,
                verdict=verdict,
                reason="The fixture supplies one deterministic backend result.",
                basis="provider-free v27 execute-boundary fixture",
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
) -> PublicStructuredRuntime:
    runtime = PublicStructuredRuntime.__new__(PublicStructuredRuntime)
    runtime.artifact_root = tmp_path
    runtime.streaming = True
    runtime.transport_retries = 0
    runtime.config = SimpleNamespace(
        pricing=pricing,
        context_window_tokens=272_000,
    )
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
    assert STRUCTURED_STAGE_DEADLINE_SECONDS == 900
    assert _provider_timeout_seconds(True) == 30
    assert _provider_timeout_seconds(False) == 300
    assert PROVIDER_CALL_DEADLINE_SECONDS > PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS
    with pytest.raises(StructuredStageTimeout), _structured_stage_deadline(0.01):
        import time

        time.sleep(0.05)


def test_structured_stage_timeout_recovers_committed_usage_without_outer_retry(
    tmp_path: Path,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class StageTimeoutApp:
        def run(self, _prompt: str, **kwargs: object) -> object:
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
    assert outcome.cost["total_usd"] is None


def test_exception_provider_failure_recovers_usage_and_exempts_only_retried_row(
    tmp_path: Path,
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class ProviderFailureApp:
        def run(self, _prompt: str, **kwargs: object) -> object:
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
    )
    app_count = 0

    def app_factory(*_args: object, **_kwargs: object) -> object:
        nonlocal app_count
        app_count += 1
        return ProviderFailureApp() if app_count == 1 else SimpleNamespace(
            run=lambda *_run_args, **_run_kwargs: success_result
        )

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
) -> None:
    class FixtureResponse(BaseModel):
        value: str

    class StageTimeoutWithoutResultApp:
        def run(self, _prompt: str, **_kwargs: object) -> object:
            raise StructuredStageTimeout("fixture timeout before result commit")

    runtime = _provider_free_public_runtime(
        tmp_path,
        pricing=_runtime_fixture_pricing(),
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
    assert outcome.cost["total_usd"] is None


def test_local_schema_failure_does_not_duplicate_in_memory_usage(
    tmp_path: Path,
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
    )
    runtime._app = lambda *_args, **_kwargs: SimpleNamespace(
        run=lambda *_run_args, **_run_kwargs: invalid_result
    )

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
    _failure_judge_payload(
        pair_id="0000",
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        release=[],
        output_root=tmp_path,
        error=error,
        run_identity=run_identity,
    )

    assert len(list((tmp_path / "method" / "0000").glob("round-*.json"))) == 3
    assert (tmp_path / "judge" / "0000.json").is_file()
    judge = json.loads((tmp_path / "judge" / "0000.json").read_text(encoding="utf-8"))
    assert judge["eligible"] is False
    assert judge["judgement"] is None


class _UnavailableJudgeFixtureRuntime:
    """Provider-shaped fixture whose pair-wide shape never closes."""

    real_llm = True

    def __init__(self) -> None:
        self.kinds: list[str] = []
        self.max_output_tokens: list[int | None] = []

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        self.kinds.append(kind)
        self.max_output_tokens.append(kwargs.get("max_output_tokens"))
        if not issubclass(schema, ExactJudgeResponse) or kind not in {"judge", "judge_correction"}:
            raise AssertionError(f"unexpected schema: {schema}")
        response = JudgeResponse(
            ledger_assessments=[],
            release_assessments=[],
            reason="The fixture intentionally returns an incomplete pair-wide shape.",
            basis="provider-free pair-wide failure test",
        )
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
            context_budget={
                "mode": "provider_free_fixture",
                "projection_version": "stage-context-projection.v1",
                "prompt_characters": len(prompt),
                "estimated_prompt_tokens": (len(prompt) + 3) // 4,
                "provider_input_tokens": 0,
                "context_window_tokens": 1_000_000,
                "max_output_tokens": kwargs.get("max_output_tokens", MAX_STRUCTURED_OUTPUT_TOKENS),
                "truncation_applied": False,
                "projection_decision": "The complete fixture prompt was retained.",
                "reason": "The fixture records the judge prompt size.",
                "basis": "provider-free pair-wide failure test",
            },
            real_llm=True,
            reason="The provider-shaped fixture returned a validated response.",
            basis="provider-free pair-wide failure test",
        )


class _PairWideJudgeFixtureRuntime:
    """Provider-shaped fixture for one pair-wide call and one correction."""

    real_llm = True

    def __init__(
        self,
        ledger_ids: list[str],
        *,
        malformed_first: bool = False,
        malformed_always: bool = False,
        asymmetric_first: bool = False,
    ) -> None:
        self.ledger_ids = ledger_ids
        self.kinds: list[str] = []
        self.malformed_first = malformed_first
        self.malformed_always = malformed_always
        self.asymmetric_first = asymmetric_first
        self.pair_wide_calls = 0
        self.max_output_tokens: list[int | None] = []
        self.prompts: list[str] = []

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        del system_prompt, artifact_id
        self.kinds.append(kind)
        self.prompts.append(prompt)
        self.max_output_tokens.append(kwargs.get("max_output_tokens"))
        if not issubclass(schema, ExactJudgeResponse) or kind not in {"judge", "judge_correction"}:
            raise AssertionError(f"unexpected pair-wide call: {kind}, {schema}")
        if kind == "judge":
            self.pair_wide_calls += 1
        issue_ids = list(dict.fromkeys(re.findall(r"0000:r[1-3]:issue:\d+", prompt)))
        if self.malformed_always or (kind == "judge" and self.malformed_first):
            issue_ids = issue_ids[:-1]
        asymmetric = bool(
            kind == "judge"
            and self.asymmetric_first
            and self.ledger_ids
            and issue_ids
        )
        response = JudgeResponse(
            ledger_assessments=[
                LedgerAssessment(
                    ledger_id=ledger_id,
                    matched_issue_ids=[],
                    reason="The pair-wide fixture found no semantic match.",
                    basis="one pair-wide fixture with the supplied ledger and release IDs",
                )
                for ledger_id in self.ledger_ids
            ],
            release_assessments=[
                ReleaseAssessment(
                    issue_id=issue_id,
                    accounted_ledger_ids=(
                        [self.ledger_ids[0]]
                        if asymmetric and issue_id == issue_ids[0]
                        else []
                    ),
                    is_false_positive=not (
                        asymmetric and issue_id == issue_ids[0]
                    ),
                    reason="The pair-wide fixture found no frozen ledger item with the same locus and property.",
                    basis="one pair-wide fixture with the supplied ledger and release IDs",
                )
                for issue_id in issue_ids
            ],
            reason="The fixture closed one exact pair-wide release surface.",
            basis="pair-wide fixture",
        )
        if not (
            self.malformed_always
            or (kind == "judge" and self.malformed_first)
            or asymmetric
        ):
            response = schema.model_validate(response.model_dump(mode="json"))
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
            context_budget={
                "mode": "provider_free_fixture",
                "projection_version": "stage-context-projection.v1",
                "prompt_characters": len(prompt),
                "estimated_prompt_tokens": (len(prompt) + 3) // 4,
                "provider_input_tokens": 0,
                "context_window_tokens": 1_000_000,
                "max_output_tokens": kwargs.get("max_output_tokens", MAX_STRUCTURED_OUTPUT_TOKENS),
                "truncation_applied": False,
                "projection_decision": "The pair-wide prompt was retained.",
                "reason": "The fixture records the pair-wide prompt size.",
                "basis": "provider-free pair-wide fixture",
            },
            real_llm=True,
            reason="The provider-shaped fixture returned a validated pair-wide response.",
            basis="provider-free pair-wide fixture",
        )


def _fixture_run_identity(pair_id: str, pair_manifest_hash: str) -> dict:
    return {
        "run_id": "1" * 32,
        "run_contract_hash": "sha256:" + "1" * 64,
        "source_provenance": {
            "source_commit": "1" * 40,
            "source_branch": "fixture",
            "source_dirty": False,
            "reason": "Fixture source provenance.",
            "basis": "provider-free test fixture",
        },
        "pair_input_hashes": {pair_id: pair_manifest_hash},
    }


def test_pair_wide_judge_shape_failure_becomes_unavailable_after_one_correction(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = _UnavailableJudgeFixtureRuntime()
    issue = {
        "issue_id": "0000:r1:issue:0",
        "title": "Fixture unmatched release",
        "requirement_quote": "Fixture requirement",
        "predicate_id": None,
        "predicate_inputs": {},
        "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
        "expected": "Fixture expected behavior",
        "observed": "Fixture observed behavior",
        "d_level": "D1",
        "witness_level": "W1",
        "reason": "Fixture release reason.",
        "basis": "Fixture release basis.",
    }
    judge = _judge_pair(
        pair=pair,
        method_rounds=[
            {
                "schema": "paper1.evidence_discovery.method_cell.v8",
                "run_id": "1" * 32,
                "run_contract_hash": "sha256:" + "1" * 64,
                "pair_id": "0000",
                "round": 1,
                "status": "completed",
                "eligible": True,
                "eligibility_reasons": ["fixture"],
                "prompt_hash": "sha256:" + "2" * 64,
                "context_manifest": pair.context_manifest.model_dump(mode="json"),
                "input_hashes": pair.hashes,
                "stage_receipts": [],
                "report_issue_clusters": [issue],
                "reason": "Fixture method receipt.",
                "basis": "Fixture method receipt basis.",
            }
        ],
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity(
            "0000", pair.context_manifest.manifest_hash
        ),
    )

    assert judge["eligible"] is False
    assert judge["adjudication_mode"] == "judge_unavailable"
    assert judge["judgement"] is None
    assert runtime.kinds == ["judge", "judge_correction"]
    assert runtime.max_output_tokens == [
        JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
        JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS,
    ]
    assert len(judge["llm_calls"]) == 2


def test_large_release_surface_stays_one_pair_wide_call(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(
            encoding="utf-8"
        )
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids)
    method_rounds = []
    issue_index = 0
    for round_index in range(1, 4):
        issues = []
        for _ in range(2):
            issues.append(
                {
                    "issue_id": f"0000:r{round_index}:issue:{issue_index}",
                    "title": "Pair-wide fixture issue",
                    "requirement_quote": "Pair-wide fixture requirement",
                    "predicate_id": None,
                    "predicate_inputs": {},
                    "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
                    "expected": "Pair-wide fixture expected behavior",
                    "observed": "Pair-wide fixture observed behavior",
                    "d_level": "D1",
                    "witness_level": "W1",
                    "reason": "Pair-wide fixture issue reason.",
                    "basis": "Pair-wide fixture issue basis.",
                }
            )
            issue_index += 1
        method_rounds.append(
            {
                "schema": "paper1.evidence_discovery.method_cell.v8",
                "run_id": "1" * 32,
                "run_contract_hash": "sha256:" + "1" * 64,
                "pair_id": "0000",
                "round": round_index,
                "status": "completed",
                "eligible": True,
                "eligibility_reasons": ["fixture"],
                "prompt_hash": "sha256:" + "2" * 64,
                "context_manifest": pair.context_manifest.model_dump(mode="json"),
                "input_hashes": pair.hashes,
                "stage_receipts": [],
                "report_issue_clusters": issues,
                "reason": "Fixture method receipt.",
                "basis": "Fixture method receipt basis.",
            }
        )

    judge = _judge_pair(
        pair=pair,
        method_rounds=method_rounds,
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity("0000", pair.context_manifest.manifest_hash),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "pair_wide"
    assert judge["response_schema_hash"].startswith("sha256:")
    assert runtime.kinds == ["judge"]
    assert runtime.max_output_tokens == [JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS]
    assert len(judge["judgement"]["release_assessments"]) == 6


def test_pair_wide_shape_failure_gets_one_targeted_correction(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(
            encoding="utf-8"
        )
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids, malformed_first=True)
    issues = [
        {
            "issue_id": f"0000:r1:issue:{index}",
            "title": "Correction fixture issue",
            "requirement_quote": "Correction fixture requirement",
            "predicate_id": None,
            "predicate_inputs": {},
            "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
            "expected": "Correction fixture expected behavior",
            "observed": "Correction fixture observed behavior",
            "d_level": "D1",
            "witness_level": "W1",
            "reason": "Correction fixture issue reason.",
            "basis": "Correction fixture issue basis.",
        }
        for index in range(6)
    ]
    method_rounds = [
        {
            "schema": "paper1.evidence_discovery.method_cell.v8",
            "run_id": "1" * 32,
            "run_contract_hash": "sha256:" + "1" * 64,
            "pair_id": "0000",
            "round": 1,
            "status": "completed",
            "eligible": True,
            "eligibility_reasons": ["fixture"],
            "prompt_hash": "sha256:" + "2" * 64,
            "context_manifest": pair.context_manifest.model_dump(mode="json"),
            "input_hashes": pair.hashes,
            "stage_receipts": [],
            "report_issue_clusters": issues,
            "reason": "Correction fixture method receipt.",
            "basis": "Correction fixture method receipt basis.",
        }
    ]
    judge = _judge_pair(
        pair=pair,
        method_rounds=method_rounds,
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity("0000", pair.context_manifest.manifest_hash),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "pair_wide_corrected"
    assert runtime.kinds == ["judge", "judge_correction"]
    assert '"ledger_assessment_count"' in runtime.prompts[0]
    assert '"release_assessment_count": 6' in runtime.prompts[0]
    assert '"identity_contract_version"' in runtime.prompts[0]
    assert judge["response_schema_hash"] in runtime.prompts[0]
    assert "Previous pair-wide JudgeResponse to repair" in runtime.prompts[1]
    assert "Merge duplicate rows for one ledger ID" in runtime.prompts[1]
    assert '"missing_release_issue_ids": ["0000:r1:issue:5"]' in runtime.prompts[1]
    assert "Never deduplicate release assessment rows" in runtime.prompts[1]
    assert "mechanically compare both assessment ID sets" in runtime.prompts[1]
    assert len(judge["judgement"]["release_assessments"]) == 6


def test_pair_wide_relation_asymmetry_gets_exact_targeted_correction(
    tmp_path: Path,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(
            encoding="utf-8"
        )
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids, asymmetric_first=True)
    issue = {
        "issue_id": "0000:r1:issue:0",
        "title": "Asymmetric relation fixture issue",
        "requirement_quote": "Asymmetric relation fixture requirement",
        "predicate_id": None,
        "predicate_inputs": {},
        "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
        "expected": "Asymmetric relation fixture expected behavior",
        "observed": "Asymmetric relation fixture observed behavior",
        "d_level": "D1",
        "witness_level": "W1",
        "reason": "Asymmetric relation fixture issue reason.",
        "basis": "Asymmetric relation fixture issue basis.",
    }
    judge = _judge_pair(
        pair=pair,
        method_rounds=[
            {
                "round": 1,
                "status": "completed",
                "eligible": True,
                "eligibility_reasons": ["fixture"],
                "report_issue_clusters": [issue],
                "reason": "Asymmetric relation fixture method receipt.",
                "basis": "Asymmetric relation fixture method receipt basis.",
            }
        ],
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity("0000", pair.context_manifest.manifest_hash),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "pair_wide_corrected"
    assert runtime.kinds == ["judge", "judge_correction"]
    assert (
        f'release-side-only=[["{ledger_ids[0]}", "0000:r1:issue:0"]]'
        in runtime.prompts[1]
    )
    assert (
        "if one candidate independently establishes the complete ledger defect"
        in runtime.prompts[1]
    )
    assert "otherwise remove the accounting pair" in runtime.prompts[1]
    assert '"relation_accounting_rows"' in runtime.prompts[1]
    assert "cannot be unioned into one hit" in runtime.prompts[1]


def test_pair_wide_failure_does_not_expand_to_atomic_relation_matrix(
    tmp_path: Path,
) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(
            encoding="utf-8"
        )
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids, malformed_always=True)
    issues = [
        {
            "issue_id": f"0000:r1:issue:{index}",
            "title": "Budget fixture issue",
            "requirement_quote": "Budget fixture requirement",
            "predicate_id": None,
            "predicate_inputs": {},
            "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
            "expected": "Budget fixture expected behavior",
            "observed": "Budget fixture observed behavior",
            "d_level": "D1",
            "witness_level": "W1",
            "reason": "Budget fixture issue reason.",
            "basis": "Budget fixture issue basis.",
        }
        for index in range(6)
    ]
    judge = _judge_pair(
        pair=pair,
        method_rounds=[
            {
                "schema": "paper1.evidence_discovery.method_cell.v8",
                "run_id": "1" * 32,
                "run_contract_hash": "sha256:" + "1" * 64,
                "pair_id": "0000",
                "round": 1,
                "status": "completed",
                "eligible": True,
                "eligibility_reasons": ["fixture"],
                "prompt_hash": "sha256:" + "2" * 64,
                "context_manifest": pair.context_manifest.model_dump(mode="json"),
                "input_hashes": pair.hashes,
                "stage_receipts": [],
                "report_issue_clusters": issues,
                "reason": "Budget fixture method receipt.",
                "basis": "Budget fixture method receipt basis.",
            }
        ],
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity("0000", pair.context_manifest.manifest_hash),
    )

    assert judge["eligible"] is False
    assert judge["adjudication_mode"] == "judge_unavailable"
    assert judge["judgement"] is None
    assert runtime.kinds == ["judge", "judge_correction"]
    assert len(judge["llm_calls"]) == 2
    assert all("atomic" not in json.dumps(error).lower() for error in judge["errors"])


def test_exact_empty_release_still_uses_one_pair_wide_judge_call(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(encoding="utf-8")
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids)

    judge = _judge_pair(
        pair=pair,
        method_rounds=[
            {
                "round": 1,
                "status": "completed",
                "eligible": True,
                "eligibility_reasons": ["fixture"],
                "report_issue_clusters": [],
                "reason": "No release issue was produced.",
                "basis": "Exact empty release fixture.",
            }
        ],
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity(
            "0000", pair.context_manifest.manifest_hash
        ),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "pair_wide"
    assert runtime.kinds == ["judge"]
    assert len(judge["llm_calls"]) == 1
    assert all(not item["matched_issue_ids"] for item in judge["judgement"]["ledger_assessments"])


def test_ineligible_diagnostic_release_never_enters_judge_surface(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    ledger_payload = json.loads(
        (PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json").read_text(encoding="utf-8")
    )
    ledger_ids = [
        str(item["id"])
        for item in ledger_payload["items"].values()
        if item.get("pair") == "0000"
    ]
    runtime = _PairWideJudgeFixtureRuntime(ledger_ids)

    judge = _judge_pair(
        pair=pair,
        method_rounds=[
            {
                "round": 1,
                "status": "completed_with_diagnostics",
                "eligible": False,
                "eligibility_reasons": ["provider_error"],
                "report_issue_clusters": [
                    {
                        "issue_id": "0000:r1:diagnostic:0",
                        "title": "Retained diagnostic issue",
                        "d_level": "D1",
                        "witness_level": "W1",
                        "reason": "The partial method cell retained this diagnostic issue.",
                        "basis": "Ineligible method receipt fixture.",
                    }
                ],
                "reason": "The method cell retained diagnostics but is not eligible.",
                "basis": "Provider-free ineligible-cell fixture.",
            }
        ],
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        runtime=runtime,
        output_root=tmp_path,
        run_identity=_fixture_run_identity(
            "0000", pair.context_manifest.manifest_hash
        ),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "pair_wide"
    assert judge["release_count"] == 0
    assert runtime.kinds == ["judge"]
    assert len(judge["llm_calls"]) == 1
    assert judge["judgement"]["release_assessments"] == []
    assert all(
        not item["matched_issue_ids"]
        for item in judge["judgement"]["ledger_assessments"]
    )


def test_failed_judge_is_unadjudicated_not_a_miss_or_false_positive(tmp_path: Path) -> None:
    run_identity = _fixture_run_identity("0000", "sha256:" + "3" * 64)
    failed = _failure_judge_payload(
        pair_id="0000",
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        release=[{"issue_id": "0000:r1:issue:0"}],
        output_root=tmp_path,
        error=RuntimeError("fixture judge unavailable"),
        run_identity=run_identity,
    )
    metrics = _metrics(
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
        pair_method={
            "0000": [
                {
                    "round": 1,
                    "eligible": True,
                    "report_issue_clusters": [{"issue_id": "0000:r1:issue:0"}],
                    "evidence_records": [],
                    "errors": [],
                }
            ]
        },
        pair_judge={"0000": failed},
        selected_pair_ids=["0000"],
        rounds=1,
    )

    assert metrics["eligibility"]["eligible_judge_pairs"] == 0
    assert metrics["emissions"]["false_positive"] == 0
    assert metrics["emissions"]["unjudged_or_ineligible_release_issue_count"] == 1


def test_provider_free_run_manifest_resume_and_concurrent_atomic_writes(tmp_path: Path) -> None:
    run_id = "2" * 32
    summary = run_experiment(
        report_root=REPORT_ROOT,
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
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
    assert manifest["retry_policy"]["structured_stage_timeout_seconds"] == 900
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
    assert len(list((run_root / "judge").glob("*.json"))) == 2
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
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
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
    stale_payload["schema"] = "paper1.evidence_discovery.method_cell.v1"
    stale_path.write_text(
        json.dumps(stale_payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    repaired = run_experiment(
        report_root=REPORT_ROOT,
        ledger_path=PAPER_ROOT / "discover_matrix/ledger_v2/ledger.json",
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
    assert current["schema"] == "paper1.evidence_discovery.method_cell.v8"
    assert stale_receipts
    assert any(
        json.loads(path.read_text(encoding="utf-8"))["schema"]
        == "paper1.evidence_discovery.method_cell.v1"
        for path in stale_receipts
    )
