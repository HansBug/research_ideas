from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

import pytest
from pydantic import ValidationError
from utils.llm.config import LLMPricing, LLMTokenPrices

from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.backends.bounded_verification import _terminal_states, run_bounded_verification
from pipeline.evidence_discovery.backends.topology import _graph
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.evidence.receipts import RawReceipt
from pipeline.evidence_discovery.evidence.audit_bundle import W2AuditBundle
from pipeline.evidence_discovery.evidence.witness_levels import (
    build_evidence_record,
    calculate_witness_level,
)
from pipeline.evidence_discovery.inputs import load_pair, parse_fcstm
from pipeline.evidence_discovery.orchestration.runner import (
    AtomicMatchDecision,
    LedgerAssessment,
    JudgeResponse,
    ReleaseAssessment,
    _failure_judge_payload,
    _failure_method_cell,
    _judge_shape_errors,
    _normalize_judge_shape,
    _judge_pair,
    _metrics,
    run_experiment,
)
from pipeline.evidence_discovery.orchestration.contracts import (
    IndependentJudgeReceipt,
    MethodCellReceipt,
    PairRunStatus,
    RunManifest,
    RunSummaryReceipt,
    SourceProvenance,
)
from pipeline.evidence_discovery.orchestration.runtime import (
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    ProviderCallTimeout,
    StructuredCallOutcome,
    _annotate_usage_billing,
    _cost_for_usage,
    _provider_timeout_seconds,
    _provider_deadline,
)
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import (
    CandidateIssue,
    ContextBudgetReceipt,
    D_SYSTEM_PROMPT,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    MethodResponse,
    SemanticAdjudication,
    adjudicate_disposition,
    assemble_method_response,
    bind_candidate,
    build_method_prompt,
    fallback_grounding,
    build_d_adjudication_prompt,
    resolve_transition_ref,
)
from pipeline.evidence_discovery.semantics.binding import BindingResult


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

def test_w2_audit_contains_logic_hashes_backend_and_retry_records() -> None:
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
    audit_hash = bundle.pop("audit_hash")
    expected_hash = "sha256:" + hashlib.sha256(
        json.dumps(bundle, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    assert audit_hash == expected_hash


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


def test_source_grounding_rows_are_attribution_only() -> None:
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
        GroundingResponse(
            branch="source",
            candidates=[source_candidate],
            rejected_contract_ids=[],
            reason="source fixture",
            basis="source fixture",
        ),
        GroundingResponse(
            branch="model",
            candidates=[model_candidate],
            rejected_contract_ids=[],
            reason="model fixture",
            basis="model fixture",
        ),
        reason="join fixture",
        basis="exact source refs",
    )
    assert len(joined.issues) == 1
    assert joined.issues[0].element_refs == [transition.ref]
    assert joined.issues[0].source_refs == ["nl:NL1"]


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


def test_frontier_fallback_preserves_exact_leaf_facts_and_v4_dossier_guidance() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    contract = NLContract(
        contract_id="NL-CONTRACT-NL1",
        segment_id="NL1",
        quote=pair.nl_segments[0].text,
        normative_statement=pair.nl_segments[0].text,
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
        branch="model",
        contracts=contracts,
        reason="provider-free fallback fixture",
    )
    frontier = next(item for item in fallback.candidates if item.predicate_id == "V4")
    expected_leaf_refs = {
        diagnostic.refs[0]
        for diagnostic in pair.inspection_facts.diagnostics
        if diagnostic.code == "LEAF_WITHOUT_OUTGOING" and diagnostic.refs
    }
    assert set(frontier.element_refs) == expected_leaf_refs
    assert frontier.predicate_inputs == {"initial_scope": "closed_fcstm_initial_scope"}
    assert frontier.reason and frontier.basis
    assert "reachable non-final leaf" in D_SYSTEM_PROMPT
    assert "intentional terminal or synthetic" in D_SYSTEM_PROMPT

    dossier = {
        "obligation_id": "0023:test:frontier",
        "candidate": frontier.model_dump(mode="json"),
        "binding": {"precise": True, "element_refs": frontier.element_refs, "source_refs": frontier.source_refs, "reason": "exact", "basis": "fixture"},
        "plan": {"predicate_id": "V4", "predicate_name": "deadlock_free", "family": "Bounded Verification", "semantics": "finite progress", "inputs": frontier.predicate_inputs, "supported": False, "binding_complete": True, "missing_inputs": [], "reason": "W1", "basis": "fixture"},
        "receipt": {"receipt_id": "fixture", "backend": "bounded_verification:V4", "terminal_state": "unsupported", "verdict": "false", "counterexample": [{"state": "PumpState"}], "trace": [], "run_metadata": {"terminal_states": [], "nonterminal_deadlock_states": ["PumpState"]}, "reason": "fixture frontier", "basis": "fixture facts"},
        "source_attribution": {},
    }
    prompt = build_d_adjudication_prompt(pair, [dossier])
    assert "nonterminal_deadlock_states" in prompt
    assert "Do not infer" in prompt
    assert "terminality from a state name" in prompt


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
        "title", "requirement_quote", "predicate_id", "predicate_inputs", "element_refs",
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
        W2AuditBundle,
        AtomicMatchDecision,
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
    assert PROVIDER_CALL_DEADLINE_SECONDS == 120
    assert _provider_timeout_seconds(True) == 30
    assert _provider_timeout_seconds(False) == 120
    assert PROVIDER_CALL_DEADLINE_SECONDS > PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS
    with pytest.raises(ProviderCallTimeout):
        with _provider_deadline(0.01):
            import time

            time.sleep(0.05)


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


class _AtomicJudgeFixtureRuntime:
    """Real-provider-shaped fixture that forces pair-wide shape fallback."""

    real_llm = True

    def __init__(self) -> None:
        self.kinds: list[str] = []

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        self.kinds.append(kind)
        if schema is JudgeResponse:
            response = JudgeResponse(
                ledger_assessments=[],
                release_assessments=[],
                reason="The fixture intentionally returns an incomplete pair-wide shape.",
                basis="provider-free atomic fallback test",
            )
        elif schema is AtomicMatchDecision:
            response = AtomicMatchDecision(
                matches=False,
                confidence="high",
                reason="The supplied fixture units do not describe the same locus and property.",
                basis="one supplied ledger entry and one supplied release issue",
            )
        else:
            raise AssertionError(f"unexpected schema: {schema}")
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
            context_budget={
                "mode": "provider_free_real_shape_fixture",
                "projection_version": "stage-context-projection.v1",
                "prompt_characters": len(prompt),
                "estimated_prompt_tokens": (len(prompt) + 3) // 4,
                "provider_input_tokens": 0,
                "context_window_tokens": 1_000_000,
                "max_output_tokens": 8000,
                "truncation_applied": False,
                "projection_decision": "The complete fixture prompt was retained.",
                "reason": "The fixture records the judge prompt size.",
                "basis": "provider-free atomic fallback test",
            },
            real_llm=True,
            reason="The provider-shaped fixture returned a validated response.",
            basis="provider-free atomic fallback test",
        )


class _PartitionJudgeFixtureRuntime:
    """Provider-shaped fixture for bounded release partitioning."""

    real_llm = True

    def __init__(
        self,
        ledger_ids: list[str],
        *,
        malformed_first: bool = False,
        malformed_always: bool = False,
    ) -> None:
        self.ledger_ids = ledger_ids
        self.kinds: list[str] = []
        self.malformed_first = malformed_first
        self.malformed_always = malformed_always
        self.partition_calls = 0

    def call(self, *, kind, schema, system_prompt, prompt, artifact_id, **kwargs):
        del system_prompt, artifact_id, kwargs
        self.kinds.append(kind)
        if schema is not JudgeResponse or kind not in {"judge_partition", "judge_partition_correction"}:
            raise AssertionError(f"unexpected partition call: {kind}, {schema}")
        if kind == "judge_partition":
            self.partition_calls += 1
        issue_ids = list(dict.fromkeys(re.findall(r"0000:r[1-3]:issue:\d+", prompt)))
        if self.malformed_always or (kind == "judge_partition" and self.malformed_first):
            issue_ids = issue_ids[:-1]
        response = JudgeResponse(
            ledger_assessments=[
                LedgerAssessment(
                    ledger_id=ledger_id,
                    matched_issue_ids=[],
                    reason="The partition fixture found no semantic match.",
                    basis="bounded partition fixture with the supplied ledger and release IDs",
                )
                for ledger_id in self.ledger_ids
            ],
            release_assessments=[
                ReleaseAssessment(
                    issue_id=issue_id,
                    accounted_ledger_ids=[],
                    is_false_positive=True,
                    reason="The partition fixture found no frozen ledger item with the same locus and property.",
                    basis="bounded partition fixture with the supplied ledger and release IDs",
                )
                for issue_id in issue_ids
            ],
            reason="The fixture closed one exact release partition.",
            basis="bounded partition fixture",
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
                "mode": "provider_free_partition_fixture",
                "projection_version": "stage-context-projection.v1",
                "prompt_characters": len(prompt),
                "estimated_prompt_tokens": (len(prompt) + 3) // 4,
                "provider_input_tokens": 0,
                "context_window_tokens": 1_000_000,
                "max_output_tokens": 8000,
                "truncation_applied": False,
                "projection_decision": "The bounded partition prompt was retained.",
                "reason": "The fixture records the partition prompt size.",
                "basis": "provider-free bounded partition fixture",
            },
            real_llm=True,
            reason="The provider-shaped fixture returned a validated partition response.",
            basis="provider-free bounded partition fixture",
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


def test_pair_wide_judge_shape_failure_uses_atomic_llm_relations(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")
    runtime = _AtomicJudgeFixtureRuntime()
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
                "schema": "paper1.evidence_discovery.method_cell.v2",
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

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "atomic_llm_fallback"
    assert judge["judgement"] is not None
    assert "judge_atomic_relation" in runtime.kinds
    assert len(judge["atomic_relations"]) == judge["ledger_count"]
    assert judge["judgement"]["release_assessments"][0]["is_false_positive"] is True


def test_large_release_surface_is_partitioned_before_atomic_fallback(tmp_path: Path) -> None:
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
    runtime = _PartitionJudgeFixtureRuntime(ledger_ids)
    method_rounds = []
    issue_index = 0
    for round_index in range(1, 4):
        issues = []
        for _ in range(2):
            issues.append(
                {
                    "issue_id": f"0000:r{round_index}:issue:{issue_index}",
                    "title": "Partition fixture issue",
                    "requirement_quote": "Partition fixture requirement",
                    "predicate_id": None,
                    "predicate_inputs": {},
                    "binding": {"precise": True, "element_refs": [pair.model.states[0].ref]},
                    "expected": "Partition fixture expected behavior",
                    "observed": "Partition fixture observed behavior",
                    "d_level": "D1",
                    "witness_level": "W1",
                    "reason": "Partition fixture issue reason.",
                    "basis": "Partition fixture issue basis.",
                }
            )
            issue_index += 1
        method_rounds.append(
            {
                "schema": "paper1.evidence_discovery.method_cell.v2",
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
    assert judge["adjudication_mode"] == "partitioned_pair_wide"
    assert runtime.kinds == ["judge_partition"]
    assert judge["atomic_relations"] == []
    assert len(judge["judgement"]["release_assessments"]) == 6


def test_partition_shape_failure_gets_one_targeted_correction(tmp_path: Path) -> None:
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
    runtime = _PartitionJudgeFixtureRuntime(ledger_ids, malformed_first=True)
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
            "schema": "paper1.evidence_discovery.method_cell.v2",
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
    assert judge["adjudication_mode"] == "partitioned_pair_wide"
    assert runtime.kinds == ["judge_partition", "judge_partition_correction"]
    assert judge["atomic_relations"] == []
    assert len(judge["judgement"]["release_assessments"]) == 6


def test_large_partition_failure_does_not_expand_to_atomic_relation_matrix(
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
    runtime = _PartitionJudgeFixtureRuntime(ledger_ids, malformed_always=True)
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
                "schema": "paper1.evidence_discovery.method_cell.v2",
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
    assert judge["atomic_relations"] == []
    assert "judge_atomic_relation" not in runtime.kinds
    assert any(
        error.get("error") == "atomic_relation_budget_exceeded"
        for error in judge["errors"]
    )


def test_exact_empty_release_closes_without_an_llm_semantic_call(tmp_path: Path) -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0000")

    class NoCallRuntime:
        real_llm = True

        def call(self, **kwargs):
            raise AssertionError("an exact empty release must not call the semantic judge")

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
        runtime=NoCallRuntime(),
        output_root=tmp_path,
        run_identity=_fixture_run_identity(
            "0000", pair.context_manifest.manifest_hash
        ),
    )

    assert judge["eligible"] is True
    assert judge["adjudication_mode"] == "exact_empty_release"
    assert judge["llm_calls"] == []
    assert all(not item["matched_issue_ids"] for item in judge["judgement"]["ledger_assessments"])


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
    assert manifest["prompt_schema_hash"].startswith("sha256:")
    assert manifest["input_data_hash"].startswith("sha256:")
    assert manifest["pair_input_hashes"].keys() == {"0004", "0023"}
    assert len(list((run_root / "method").glob("*/round-1.json"))) == 2
    assert len(list((run_root / "judge").glob("*.json"))) == 2
    assert not list(run_root.rglob("*.tmp"))
    audit_files = list((run_root / "audit_bundles").glob("*.json"))
    assert audit_files
    for audit_file in audit_files:
        bundle = json.loads(audit_file.read_text(encoding="utf-8"))
        assert bundle["method_receipt"]["sha256"].startswith("sha256:")
        assert bundle["judge_receipt"]["sha256"].startswith("sha256:")
        assert bundle["audit_finalization"]["judge_receipt_hash"] == bundle["judge_receipt"]["sha256"]

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
    assert current["schema"] == "paper1.evidence_discovery.method_cell.v2"
    assert stale_receipts
    assert any(
        json.loads(path.read_text(encoding="utf-8"))["schema"]
        == "paper1.evidence_discovery.method_cell.v1"
        for path in stale_receipts
    )
