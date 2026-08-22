from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from importlib import import_module
from pathlib import Path

import pytest
from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.backends.bounded_verification import (
    _terminal_states,
    run_bounded_verification,
)
from pipeline.evidence_discovery.backends.topology import _graph
from pipeline.evidence_discovery.compiler import compile_plan
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
    JudgeResponse,
    LedgerAssessment,
    ReleaseAssessment,
    _d_decision_consistency_errors,
    _deduplicate_release_issues,
    _enrich_candidate,
    _failure_judge_payload,
    _failure_method_cell,
    _finalize_w2_audit_links,
    _judge_pair,
    _judge_prompt,
    _judge_shape_errors,
    _materialize_exact_s2_inventory_candidates,
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
    ProviderCallTimeout,
    StructuredCallOutcome,
    _annotate_usage_billing,
    _cost_for_usage,
    _is_provider_error,
    _provider_deadline,
    _provider_timeout_seconds,
)
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import (
    CONTRACT_SYSTEM_PROMPT,
    D_SYSTEM_PROMPT,
    DISCOVERY_GROUNDING_SYSTEM_PROMPT,
    CandidateIssue,
    ContextBudgetReceipt,
    ContractBindingHint,
    GroundingDisposition,
    GroundingResponse,
    MethodResponse,
    NLContract,
    NLContractResponse,
    SemanticAdjudication,
    adjudicate_disposition,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_grounding_prompt,
    build_method_prompt,
    fallback_grounding,
    normalize_contract_state_roles,
    resolve_transition_ref,
)
from pipeline.evidence_discovery.semantics.binding import BindingResult
from pydantic import BaseModel, ValidationError

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
        "schema": "paper1.evidence_discovery.method_cell.v6",
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
        "schema": "paper1.evidence_discovery.independent_judge.v3",
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
                contract_dispositions=[
                    GroundingDisposition(
                        contract_id=source_candidate.contract_id,
                        status="candidate_emitted",
                        candidate_count=1,
                        reason="The source fixture emitted one exact candidate.",
                        basis="provider-free source candidate fixture",
                    )
                ],
                reason="structure fixture",
                basis="structure fixture",
            ),
            GroundingResponse(
                lens="behavior_consequence",
                candidates=[model_candidate],
                contract_dispositions=[
                    GroundingDisposition(
                        contract_id=model_candidate.contract_id,
                        status="candidate_emitted",
                        candidate_count=1,
                        reason="The model fixture emitted one exact candidate.",
                        basis="provider-free model candidate fixture",
                    )
                ],
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


def test_judge_shape_normalization_is_exact_id_only() -> None:
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
        reason="Fixture response.",
        basis="Fixture response basis.",
    )
    normalized = _normalize_judge_shape(response, ledger, release, 1)
    assert not _judge_shape_errors(normalized, ledger, release, 1)
    assert normalized.ledger_assessments[0].hit_r1 is True
    assert normalized.release_assessments[0].is_false_positive is False


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

    errors = _judge_shape_errors(response, ledger, release, 1)
    assert any("same exact relation pairs" in error for error in errors)
    assert any(
        'release-side-only=[["L-1", "0000:r1:issue:0"]]' in error
        for error in errors
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
    assert fallback.contract_dispositions[0].contract_id == contract.contract_id
    assert fallback.contract_dispositions[0].status == "unresolved"
    assert fallback.contract_dispositions[0].reason
    assert fallback.contract_dispositions[0].basis
    assert "reachable non-final leaf" in D_SYSTEM_PROMPT
    assert "intentional-terminal alternative is competent only" in D_SYSTEM_PROMPT
    assert "`rebutting+survives`" in D_SYSTEM_PROMPT
    assert "Predicate/backend availability is a W question" in D_SYSTEM_PROMPT
    assert "different root-level initial edge" in D_SYSTEM_PROMPT
    assert "For each semantically active operating state" in CONTRACT_SYSTEM_PROMPT
    assert "semantic state-role coverage pass" in CONTRACT_SYSTEM_PROMPT
    assert "required target of an operating transition" in CONTRACT_SYSTEM_PROMPT
    assert "need not repeat words such as continue" in CONTRACT_SYSTEM_PROMPT
    assert "first enter ModeA" in CONTRACT_SYSTEM_PROMPT
    assert '"the system begins in Controller" yields owner=root/system' in CONTRACT_SYSTEM_PROMPT
    assert "an intermediate region or nested composite still satisfies" in CONTRACT_SYSTEM_PROMPT
    hint_schema = ContractBindingHint.model_json_schema()
    assert "owns the required initial pseudostate edge" in hint_schema["properties"]["role"]["description"]
    assert "Emit a candidate only for a possible violated obligation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "treat its typed `owner` binding hint" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "does not satisfy a `Controller -> ModeA`" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "satisfied `root/system -> Controller`" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "already-satisfied owner-local contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Interpret containment at the depth stated by the contract" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "synthetic placeholders are not author-specified operating-state" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "an unreachable state that" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "not a deadlock/dead-end violation" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "declared consumer with no consumer reachable" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "complete exact inventory" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "element_refs` contains" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Negative-property carrier example" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
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
    assert "The required disposition table contains 1 row(s)" in grounding_prompt
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
    assert "needs its own separate progress contract" in contract_schema["state_role"]["description"]
    response_schema = NLContractResponse.model_json_schema()["properties"]
    assert "every semantically active operating state" in response_schema["contracts"]["description"]


def test_grounding_response_rejects_empty_or_inconsistent_local_accounting() -> None:
    with pytest.raises(ValidationError):
        GroundingResponse(
            lens="contract_structure_contrast",
            candidates=[],
            contract_dispositions=[],
            reason="The fixture returned no candidates.",
            basis="provider-free empty-accounting fixture",
        )

    with pytest.raises(ValidationError, match="must equal 0"):
        GroundingResponse(
            lens="behavior_consequence",
            candidates=[],
            contract_dispositions=[
                GroundingDisposition(
                    contract_id="NL-CONTRACT-NL1",
                    status="candidate_emitted",
                    candidate_count=1,
                    reason="The malformed fixture claims one candidate.",
                    basis="provider-free inconsistent-count fixture",
                )
            ],
            reason="The fixture carries inconsistent local accounting.",
            basis="provider-free local-accounting fixture",
        )


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
        GroundingDisposition,
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
        binding_hints=(),
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
    assert "Never return only the" in build_contract_prompt(pair, 1)
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
    assert "action_fact" in evidence_description
    assert "state_action is a property name" in evidence_description
    assert "Every candidate object must explicitly include" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "must always be a JSON object" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Complete-inventory absence protocol" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "a nonexistent transition cannot supply its own ref" in DISCOVERY_GROUNDING_SYSTEM_PROMPT
    assert "Do not leave a normative qualifier only inside" in CONTRACT_SYSTEM_PROMPT
    assert "effect and guard are property values" in NLContract.model_json_schema()["properties"]["locus_kind"]["description"]


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
            contract_dispositions=[
                GroundingDisposition(
                    contract_id=contract_id,
                    status="candidate_emitted",
                    candidate_count=1,
                    reason="The branch emitted the candidate.",
                    basis="provider-free grounding fixture",
                )
            ],
            reason="The fixture returns one behavior candidate.",
            basis="provider-free grounding fixture",
        )

    with_outgoing = load_pair(REPORT_ROOT / "pairs" / "0035")
    normalized, diagnostics = _normalize_grounding_exact_facts(
        with_outgoing, response_for(with_outgoing, "DoorOpen")
    )
    assert normalized.candidates == []
    assert normalized.contract_dispositions[0].status == "satisfied"
    assert diagnostics[0]["class"] == "exact_local_progress_satisfied"
    assert diagnostics[0]["outgoing_transition_refs"]["DoorOpen"]

    zero_outgoing = load_pair(REPORT_ROOT / "pairs" / "0023")
    preserved, diagnostics = _normalize_grounding_exact_facts(
        zero_outgoing, response_for(zero_outgoing, "PumpState")
    )
    assert len(preserved.candidates) == 1
    assert preserved.contract_dispositions[0].status == "candidate_emitted"
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


def test_provider_retry_exemption_is_row_local_and_other_usage_is_billable() -> None:
    pricing = LLMPricing(
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


def test_provider_deadline_is_finite_and_provider_timeout_is_bounded() -> None:
    assert PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS == 30
    assert PROVIDER_CALL_DEADLINE_SECONDS == 300
    assert STRUCTURED_STAGE_DEADLINE_SECONDS == 900
    assert _provider_timeout_seconds(True) == 30
    assert _provider_timeout_seconds(False) == 300
    assert PROVIDER_CALL_DEADLINE_SECONDS > PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS
    with pytest.raises(ProviderCallTimeout):
        with _provider_deadline(0.01):
            import time

            time.sleep(0.05)


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
        if schema is not JudgeResponse or kind not in {"judge", "judge_correction"}:
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
        if schema is not JudgeResponse or kind not in {"judge", "judge_correction"}:
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
                "schema": "paper1.evidence_discovery.method_cell.v6",
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
                "schema": "paper1.evidence_discovery.method_cell.v6",
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
            "schema": "paper1.evidence_discovery.method_cell.v6",
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
    assert "Previous pair-wide JudgeResponse to repair" in runtime.prompts[1]
    assert "Merge duplicate rows for one ledger ID" in runtime.prompts[1]
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
    assert "if it is a match, include the pair on both sides" in runtime.prompts[1]
    assert "if it is not a match, remove it from both sides" in runtime.prompts[1]


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
                "schema": "paper1.evidence_discovery.method_cell.v6",
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
    assert manifest["retry_policy"]["non_stream_provider_timeout_seconds"] == 300
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
    assert current["schema"] == "paper1.evidence_discovery.method_cell.v6"
    assert stale_receipts
    assert any(
        json.loads(path.read_text(encoding="utf-8"))["schema"]
        == "paper1.evidence_discovery.method_cell.v1"
        for path in stale_receipts
    )
