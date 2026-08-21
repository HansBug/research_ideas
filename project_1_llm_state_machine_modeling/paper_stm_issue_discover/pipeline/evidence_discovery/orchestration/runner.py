from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from collections.abc import Sequence
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..backends import run_backend
from ..compiler import compile_plan
from ..compiler.plans import validate_plan
from ..evidence import build_evidence_record
from ..evidence.receipts import RawReceipt
from ..evidence.source_attribution import build_source_attribution
from ..inputs import FROZEN_PAIR_IDS, load_pair
from ..inputs.models import PairInput
from ..registry import load_registry
from ..reporting.export import write_json, write_markdown_summary
from ..semantics import (
    CandidateIssue,
    CONTRACT_SYSTEM_PROMPT,
    DAdjudicationResponse,
    D_SYSTEM_PROMPT,
    GroundingResponse,
    MODEL_GROUNDING_SYSTEM_PROMPT,
    NLContractResponse,
    SemanticAdjudication,
    SOURCE_GROUNDING_SYSTEM_PROMPT,
    StageReceipt,
    MethodResponse,
    assemble_method_response,
    bind_candidate,
    build_contract_prompt,
    build_d_adjudication_prompt,
    build_d_correction_prompt,
    build_grounding_prompt,
    fallback_contracts,
    fallback_d_adjudication,
    fallback_grounding,
    resolve_transition_ref,
)
from ..semantics.obligations import fallback_candidates
from .runtime import FixtureStructuredRuntime, PublicStructuredRuntime, StructuredCallOutcome


REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS = ("0004", "0023", "0029", "0035", "0046", "0053")


class LedgerAssessment(BaseModel):
    """Independent judge assessment for one frozen ledger entry."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_id: str = Field(min_length=1, description="Frozen ledger entry ID being assessed; copy it exactly from judge input.")
    hit_r1: bool = Field(default=False, description="Whether method round 1 contains a semantically identical release issue.")
    hit_r2: bool = Field(default=False, description="Whether method round 2 contains a semantically identical release issue.")
    hit_r3: bool = Field(default=False, description="Whether method round 3 contains a semantically identical release issue.")
    matched_issue_ids: list[str] = Field(default_factory=list, description="Method issue IDs that support the claimed round hits.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this ledger item is or is not semantically matched.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis for this ledger assessment, tied to the supplied ledger and method release data.")


class ReleaseAssessment(BaseModel):
    """Independent judge assessment for one released method issue."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    issue_id: str = Field(min_length=1, description="Released method issue ID being assessed; copy it exactly from method input.")
    accounted_ledger_ids: list[str] = Field(default_factory=list, description="Frozen ledger IDs that semantically account for this release issue.")
    is_false_positive: bool = Field(description="True only when no supplied frozen ledger entry can semantically carry this issue.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this release issue is or is not a false positive.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis for the release decision, tied to supplied ledger and method release data.")


class JudgeResponse(BaseModel):
    """Complete independent judge response with rationale for all decisions."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    ledger_assessments: list[LedgerAssessment] = Field(default_factory=list, description="One assessment for every frozen ledger item supplied to the judge.")
    release_assessments: list[ReleaseAssessment] = Field(default_factory=list, description="One assessment for every method issue in the supplied release surface.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the judge's overall assessment decision.")
    basis: str = Field(min_length=1, description="Non-empty basis identifying the supplied ledger and method release facts used by the judge.")


METHOD_SYSTEM_PROMPT = """The method is staged. The public method-generation surface is the NL contract extraction stage followed by two complementary grounding branches. Use only the complete context manifest supplied to each stage. Never read ledger answers, baseline results, judge examples, or historical release outputs. Do not emit W, D, or L levels. Every structured object must contain non-empty reason and basis."""

JUDGE_SYSTEM_PROMPT = """You are an independent judge separated from method generation. You may use the supplied frozen ledger entries to assess method D1/D2 release issues. Judge semantic identity of locus and property, not string similarity. Do not read baseline results, other pairs, other judge outputs, or historical examples. Every assessment and the top-level response must contain non-empty reason and basis fields that explain the judgment and its supplied-input support. Preserve the model's original wording."""


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump(mode="json"))
    return str(value)


def _hash_json(value: Any) -> str:
    """Hash a canonical JSON value for stage and prompt receipts."""

    text = json.dumps(
        _jsonable(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _source_provenance() -> dict[str, str]:
    """Capture the repository revision that produced a run receipt."""

    repo_root = Path(__file__).resolve().parents[5]
    try:
        commit = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        branch = subprocess.run(
            ["git", "-C", str(repo_root), "branch", "--show-current"],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.strip()
        if not commit or not branch:
            raise RuntimeError("git returned an empty commit or branch")
        return {
            "source_commit": commit,
            "source_branch": branch,
            "reason": "The run records the repository revision used to construct method and judge artifacts.",
            "basis": "git rev-parse HEAD and git branch --show-current",
        }
    except (OSError, subprocess.SubprocessError, RuntimeError) as exc:
        return {
            "source_commit": "unknown",
            "source_branch": "unknown",
            "reason": "Repository provenance could not be resolved; the run remains explicitly diagnostic.",
            "basis": f"git provenance error: {type(exc).__name__}",
        }


def _stage_receipt(
    *,
    pair: PairInput,
    stage_id: str,
    stage_name: str,
    status: str,
    artifact_roles: tuple[str, ...],
    output: Any,
    reason: str,
    basis: str,
    outcome: StructuredCallOutcome[Any] | None = None,
    diagnostics: tuple[dict[str, Any], ...] = (),
) -> dict[str, Any]:
    """Build one validated stage receipt with the input manifest hash."""

    if pair.context_manifest is None:
        raise ValueError("stage receipt requires a complete context manifest")
    return StageReceipt(
        stage_id=stage_id,
        stage_name=stage_name,  # type: ignore[arg-type]
        status=status,  # type: ignore[arg-type]
        input_manifest_hash=pair.context_manifest.manifest_hash,
        input_artifact_roles=artifact_roles,
        output_hash=_hash_json(output),
        llm_call_id=(
            str(outcome.result.get("call_id"))
            if outcome is not None and outcome.result.get("call_id")
            else None
        ),
        diagnostics=diagnostics,
        reason=reason,
        basis=basis,
    ).model_dump(mode="json")


def _aggregate_outcomes(outcomes: list[StructuredCallOutcome[Any]]) -> dict[str, Any]:
    """Retain every public runtime call while keeping the legacy llm_call key."""

    usage = [row for outcome in outcomes for row in outcome.usage]
    attempts = [
        {"stage": outcome.kind, **attempt}
        for outcome in outcomes
        for attempt in outcome.attempts
    ]
    costs = [outcome.cost for outcome in outcomes]
    eligible = all(bool(cost.get("eligible")) for cost in costs) if costs else True
    total = sum(
        float(cost.get("total_usd") or 0.0)
        for cost in costs
        if isinstance(cost.get("total_usd"), (int, float))
    )
    return {
        "kind": "method",
        "status": "success" if outcomes and all(item.succeeded for item in outcomes) else "completed_with_diagnostics",
        "response": None,
        "result": {"stage_count": len(outcomes), "stage_kinds": [item.kind for item in outcomes]},
        "attempts": attempts,
        "usage": usage,
        "cost": {"eligible": eligible, "total_usd": total if eligible else None, "attempts": [cost for cost in costs]},
    }


def _enrich_candidate(candidate: CandidateIssue, binding: Any, pair: PairInput) -> CandidateIssue:
    inputs = dict(candidate.predicate_inputs)
    inputs.setdefault("element_refs", list(binding.element_refs))
    bound_transitions = [item for item in pair.model.transitions if item.ref in binding.element_refs]
    transition_hint = inputs.get("transition") or inputs.get("transition_ref")
    transition_ref = resolve_transition_ref(
        transition_hint if isinstance(transition_hint, str) else None,
        pair.model,
        source=inputs.get("source") if isinstance(inputs.get("source"), str) else None,
        target=inputs.get("target") if isinstance(inputs.get("target"), str) else None,
    )
    if transition_ref is None and not transition_hint and len(bound_transitions) == 1:
        transition_ref = bound_transitions[0].ref
    # A predicate requiring one transition must receive one unambiguous
    # transition binding. Composite candidates remain W0 until the method names
    # the exact edge instead of silently selecting the first one.
    if transition_ref is not None:
        transition = pair.model.transition(transition_ref)
        if transition is not None:
            inputs["transition"] = transition.ref
            inputs.setdefault("transition_ref", transition.ref)
            inputs.setdefault("source", transition.source)
            inputs.setdefault("target", transition.target)
    if candidate.predicate_id == "S1" and "element" not in inputs and binding.element_refs:
        ref = binding.element_refs[0]
        state = next((item for item in pair.model.states if item.ref == ref), None)
        event = next((item for item in pair.model.events if item.ref == ref), None)
        inputs["element"] = state.name if state else event.name if event else ref
        inputs.setdefault("kind", "state" if state else "event")
    return candidate.model_copy(update={"predicate_inputs": inputs})


def _prepare_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
 ) -> dict[str, Any]:
    """Bind, compile, and execute once before the separate semantic D call."""

    obligation_id = f"{pair.pair_id}:r{round_index}:i{index}"
    binding = bind_candidate(candidate, pair.model)
    candidate = _enrich_candidate(candidate, binding, pair)
    plan = compile_plan(
        candidate,
        binding,
        load_registry(),
        obligation_id=obligation_id,
        round_index=round_index,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    validate_plan(plan)
    try:
        receipt = run_backend(plan, pair.model, f"{obligation_id}:receipt")
    except Exception as exc:
        # Backend failures are execution uncertainty, not violations. Preserve
        # a structured receipt so the candidate remains auditable and W cannot
        # be promoted by an exception path.
        receipt = RawReceipt(
            receipt_id=f"{obligation_id}:receipt",
            backend=f"error:{plan.predicate_id or 'none'}",
            terminal_state="error",
            verdict="unknown",
            reason=f"The backend raised {type(exc).__name__}; the exception was downgraded to execution uncertainty, not a violation.",
            basis="backend exception downgraded to explicit execution uncertainty",
            run_metadata={"error_type": type(exc).__name__, "error_message": str(exc)},
        )
    attribution = build_source_attribution(
        pair_id=pair.pair_id,
        obligation_id=obligation_id,
        nl_path=pair.pair_dir / "nl.txt",
        model_path=pair.pair_dir / "fcstm.fcstm",
        model_hash=pair.hashes["fcstm"],
        plan_id=plan.plan_id,
        receipt_id=receipt.receipt_id,
    )
    attribution["input_context"] = {
        "manifest_hash": pair.context_manifest.manifest_hash if pair.context_manifest else None,
        "artifact_hashes": dict(pair.hashes),
        "versions": {
            "model_parser": pair.model.algorithm_version,
            "inspection_equivalent": pair.inspection_facts.algorithm_version if pair.inspection_facts else None,
            "verify": pair.verify_facts.algorithm_version if pair.verify_facts else None,
            "smt": pair.smt_facts.algorithm_version if pair.smt_facts else None,
        },
        "reason": "The candidate receipt carries the same input closure identity used by method and grounding.",
        "basis": "pair context manifest and deterministic fact model versions",
    }
    return {
        "obligation_id": obligation_id,
        "candidate": candidate,
        "binding": binding,
        "plan": plan,
        "receipt": receipt,
        "source_attribution": attribution,
    }


def _deterministic_candidate(
    pair: PairInput,
    candidate: CandidateIssue,
    round_index: int,
    index: int,
    retry_records: list[dict[str, Any]],
    *,
    semantic_adjudication: SemanticAdjudication | None = None,
    prepared: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    prepared = prepared or _prepare_candidate(pair, candidate, round_index, index)
    candidate = prepared["candidate"]
    binding = prepared["binding"]
    plan = prepared["plan"]
    receipt = prepared["receipt"]
    attribution = prepared["source_attribution"]
    obligation_id = prepared["obligation_id"]
    record = build_evidence_record(
        pair=pair,
        obligation_id=obligation_id,
        candidate=candidate,
        binding=binding,
        plan=plan,
        receipt=receipt,
        source_attribution=attribution,
        retry_records=retry_records,
        semantic_adjudication=semantic_adjudication,
    )
    record.update(
        {
            "issue_id": f"{pair.pair_id}:r{round_index}:issue:{index}",
            "title": candidate.title,
            "requirement_quote": candidate.requirement_quote,
            "predicate_inputs": candidate.predicate_inputs,
            "element_refs": list(candidate.element_refs),
            "source_refs": list(candidate.source_refs),
            "expected": candidate.expected,
            "observed": candidate.observed,
            "strongest_rebuttal": candidate.strongest_rebuttal,
            "candidate_reason": candidate.reason,
            "candidate_basis": candidate.basis,
        }
    )
    # A completed positive predicate result is evidence against the candidate's
    # alleged defect. W1 has no executable result, so a precise D1/D2 candidate
    # remains a legal semantic issue.
    record["issue_emitted"] = bool(
        record["d_level"] in {"D1", "D2"}
        and (
            record["witness_level"] == "W1"
            or (record["witness_level"] == "W2" and receipt.verdict == "false")
        )
    )
    if record["witness_level"] == "W2":
        record["audit_bundle"]["issue_emitted"] = record["issue_emitted"]
    return record, record if record["issue_emitted"] else None


def _fallback_method(pair: PairInput, round_index: int, reason: str) -> MethodResponse:
    fallback = fallback_candidates(pair, round_index)
    return fallback.model_copy(
        update={
            "reason": "The provider or schema response was unavailable; deterministic input facts were preserved.",
            "basis": "The provider/runtime diagnostic is stored in llm_call and cell errors; no ledger or judge data was read.",
        }
    )


def _method_cell(
    *,
    pair: PairInput,
    round_index: int,
    runtime: PublicStructuredRuntime,
    previous: list[dict[str, Any]],
    output_root: Path,
) -> dict[str, Any]:
    if pair.context_manifest is None or pair.exact_source_inventory is None:
        raise ValueError("method cell requires the complete v27-equivalent input closure")
    stage_receipts: list[dict[str, Any]] = []
    stage_outputs: dict[str, Any] = {}
    all_outcomes: list[StructuredCallOutcome[Any]] = []
    all_errors: list[dict[str, Any]] = []
    prepare_output = {
        "pair_id": pair.pair_id,
        "manifest": pair.context_manifest.model_dump(mode="json"),
        "artifact_hashes": dict(pair.hashes),
        "source_roles": {
            "plantuml": "author_source_localization",
            "canonical_source_ir": "author_source_localization",
            "fcstm": "closed_model_execution",
            "inspection_facts": "deterministic_inventory_and_validation_facts",
            "working_contract": "mapping_and_eligibility_contract",
            "source_trace": "source_attribution",
            "verify_facts": "deterministic_finite_verification_context",
            "smt_facts": "normalized_formal_input_context_not_solver_result",
        },
        "reason": "The complete method input closure was prepared before contract extraction.",
        "basis": "context manifest, artifact hashes, and explicit source-role separation",
    }
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:prepare",
            stage_name="prepare",
            status="completed",
            artifact_roles=tuple(item.role for item in pair.context_manifest.artifacts),
            output=prepare_output,
            reason=prepare_output["reason"],
            basis=prepare_output["basis"],
        )
    )

    contract_prompt = build_contract_prompt(pair, round_index, previous)
    contract_outcome: StructuredCallOutcome[NLContractResponse] = runtime.call(
        kind="nl_contract_extraction",
        schema=NLContractResponse,
        system_prompt=CONTRACT_SYSTEM_PROMPT,
        prompt=contract_prompt,
        artifact_id=f"method/{pair.pair_id}/round-{round_index}/contract",
    )
    all_outcomes.append(contract_outcome)
    contract_response = contract_outcome.response if contract_outcome.succeeded else fallback_contracts(
        pair,
        str(contract_outcome.result.get("error", "structured contract output unavailable")),
    )
    stage_outputs["nl_contract_extraction"] = contract_response.model_dump(mode="json")
    if not contract_outcome.succeeded:
        all_errors.append(
            {
                "stage": "nl_contract_extraction",
                "error": contract_outcome.result.get("error", "structured contract output unavailable"),
                "reason": "Contract provider/schema failure was downgraded to a deterministic receipt.",
                "basis": "public structured runtime outcome and numbered NL fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:nl-contract",
            stage_name="nl_contract_extraction",
            status="completed" if contract_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "working_contract", "source_trace"),
            output=contract_response,
            outcome=contract_outcome,
            reason=contract_response.reason,
            basis=contract_response.basis,
        )
    )

    source_prompt = build_grounding_prompt(
        pair,
        branch="source",
        round_index=round_index,
        contracts=contract_response,
        previous=previous,
    )
    source_outcome: StructuredCallOutcome[GroundingResponse] = runtime.call(
        kind="source_grounding",
        schema=GroundingResponse,
        system_prompt=SOURCE_GROUNDING_SYSTEM_PROMPT,
        prompt=source_prompt,
        artifact_id=f"method/{pair.pair_id}/round-{round_index}/source-grounding",
    )
    all_outcomes.append(source_outcome)
    source_response = source_outcome.response if source_outcome.succeeded else fallback_grounding(
        pair,
        branch="source",
        contracts=contract_response,
        reason=str(source_outcome.result.get("error", "source grounding output unavailable")),
    )
    stage_outputs["source_grounding"] = source_response.model_dump(mode="json")
    if not source_outcome.succeeded:
        all_errors.append(
            {
                "stage": "source_grounding",
                "error": source_outcome.result.get("error", "source grounding output unavailable"),
                "reason": "Source grounding provider/schema failure was downgraded to a deterministic candidate receipt.",
                "basis": "public structured runtime outcome and source-role fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:source-grounding",
            stage_name="source_grounding",
            status="completed" if source_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "working_contract", "source_trace"),
            output=source_response,
            outcome=source_outcome,
            reason=source_response.reason,
            basis=source_response.basis,
        )
    )

    model_prompt = build_grounding_prompt(
        pair,
        branch="model",
        round_index=round_index,
        contracts=contract_response,
        previous=previous,
    )
    model_outcome: StructuredCallOutcome[GroundingResponse] = runtime.call(
        kind="model_grounding",
        schema=GroundingResponse,
        system_prompt=MODEL_GROUNDING_SYSTEM_PROMPT,
        prompt=model_prompt,
        artifact_id=f"method/{pair.pair_id}/round-{round_index}/model-grounding",
    )
    all_outcomes.append(model_outcome)
    model_response = model_outcome.response if model_outcome.succeeded else fallback_grounding(
        pair,
        branch="model",
        contracts=contract_response,
        reason=str(model_outcome.result.get("error", "model grounding output unavailable")),
    )
    stage_outputs["model_grounding"] = model_response.model_dump(mode="json")
    if not model_outcome.succeeded:
        all_errors.append(
            {
                "stage": "model_grounding",
                "error": model_outcome.result.get("error", "model grounding output unavailable"),
                "reason": "Model grounding provider/schema failure was downgraded to a deterministic candidate receipt.",
                "basis": "public structured runtime outcome and closed-model fallback",
            }
        )
    stage_receipts.append(
        _stage_receipt(
            pair=pair,
            stage_id=f"{pair.pair_id}:r{round_index}:model-grounding",
            stage_name="model_grounding",
            status="completed" if model_outcome.succeeded else "completed_with_diagnostics",
            artifact_roles=("natural_language", "fcstm_model", "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts", "working_contract"),
            output=model_response,
            outcome=model_outcome,
            reason=model_response.reason,
            basis=model_response.basis,
        )
    )

    response = assemble_method_response(
        source_response,
        model_response,
        reason="The method merged two complementary grounding branches after NL contract extraction; typed semantic D is adjudicated separately and W remains deterministic downstream output.",
        basis="source-grounding and closed-model-grounding responses over the same context manifest",
    )
    candidates = response.issues
    records: list[dict[str, Any]] = []
    release: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = list(all_errors)
    prepared_candidates: list[dict[str, Any]] = []
    for index, candidate in enumerate(candidates):
        try:
            prepared = _prepare_candidate(pair, candidate, round_index, index)
            prepared_candidates.append(prepared)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:binding",
                        stage_name="exact_binding",
                        status="completed",
                        artifact_roles=("natural_language", "fcstm_model", "source_inventory", "working_contract"),
                        output=prepared["binding"],
                        reason=prepared["binding"].reason,
                        basis=prepared["binding"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:compile",
                        stage_name="predicate_compilation",
                        status="completed",
                        artifact_roles=("fcstm_model", "inspection_equivalent_facts", "verify_facts", "smt_facts", "predicate_registry"),
                        output=prepared["plan"],
                        reason=prepared["plan"].reason,
                        basis=prepared["plan"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:execute",
                        stage_name="backend_execution",
                        status="completed" if prepared["receipt"].terminal_state in {"completed", "unsupported", "unknown"} else "completed_with_diagnostics",
                        artifact_roles=("fcstm_model", "verify_facts", "smt_facts"),
                        output=prepared["receipt"],
                        reason=prepared["receipt"].reason,
                        basis=prepared["receipt"].basis,
                    )
                ]
            )
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate processing failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    if not prepared_candidates:
        # A valid method cell always has a deterministic auditable output, even
        # when the provider returns an empty list or the candidate schema fails.
        candidate = fallback_candidates(pair, round_index).issues[0]
        try:
            prepared = _prepare_candidate(pair, candidate, round_index, 0)
            prepared_candidates.append(prepared)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:binding",
                        stage_name="exact_binding",
                        status="completed",
                        artifact_roles=("natural_language", "fcstm_model", "source_inventory", "working_contract"),
                        output=prepared["binding"],
                        reason=prepared["binding"].reason,
                        basis=prepared["binding"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:compile",
                        stage_name="predicate_compilation",
                        status="completed",
                        artifact_roles=("fcstm_model", "inspection_equivalent_facts", "verify_facts", "smt_facts", "predicate_registry"),
                        output=prepared["plan"],
                        reason=prepared["plan"].reason,
                        basis=prepared["plan"].basis,
                    ),
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:fallback:execute",
                        stage_name="backend_execution",
                        status="completed" if prepared["receipt"].terminal_state in {"completed", "unsupported", "unknown"} else "completed_with_diagnostics",
                        artifact_roles=("fcstm_model", "verify_facts", "smt_facts"),
                        output=prepared["receipt"],
                        reason=prepared["receipt"].reason,
                        basis=prepared["receipt"].basis,
                    ),
                ]
            )
        except Exception as exc:
            errors.append({"candidate_index": 0, "error_type": type(exc).__name__, "message": str(exc), "reason": "Deterministic fallback processing failed.", "basis": "Fallback diagnostic preservation."})

    d_prompt = ""
    d_correction_prompt = ""
    d_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_stage_outcome: StructuredCallOutcome[DAdjudicationResponse] | None = None
    d_response = fallback_d_adjudication(
        [item["obligation_id"] for item in prepared_candidates],
        "no prepared candidate dossier",
    )
    decisions: dict[str, SemanticAdjudication] = {}
    if prepared_candidates:
        dossiers = [
            {
                "obligation_id": item["obligation_id"],
                "candidate": item["candidate"].model_dump(mode="json"),
                "binding": item["binding"].model_dump(mode="json"),
                "plan": item["plan"].to_dict(),
                "receipt": item["receipt"].to_dict(),
                "source_attribution": item["source_attribution"],
                "reason": "The dossier contains exact method outputs and formal execution facts for semantic adjudication.",
                "basis": "prepared candidate, exact binding, frozen predicate plan, and backend receipt",
            }
            for item in prepared_candidates
        ]
        d_prompt = build_d_adjudication_prompt(pair, dossiers)
        d_outcome = runtime.call(
            kind="d_adjudication",
            schema=DAdjudicationResponse,
            system_prompt=D_SYSTEM_PROMPT,
            prompt=d_prompt,
            artifact_id=f"method/{pair.pair_id}/round-{round_index}/d-adjudication",
        )
        all_outcomes.append(d_outcome)
        d_stage_outcome = d_outcome
        d_response = d_outcome.response if d_outcome.succeeded else fallback_d_adjudication(
            [item["obligation_id"] for item in prepared_candidates],
            str(d_outcome.result.get("error", "D adjudication output unavailable")),
        )
        if not d_outcome.succeeded:
            errors.append(
                {
                    "stage": "d_adjudication",
                    "error": d_outcome.result.get("error", "D adjudication output unavailable"),
                    "reason": "Typed semantic D failure was downgraded to explicit unresolved decisions.",
                    "basis": "public structured runtime outcome and no-silent-drop D fallback",
                }
            )
        expected_ids = [item["obligation_id"] for item in prepared_candidates]
        expected_id_set = set(expected_ids)
        def coverage(
            response: DAdjudicationResponse,
        ) -> tuple[list[SemanticAdjudication], list[str], list[str], list[str]]:
            supplied_decisions = [
                decision
                for decision in response.decisions
                if decision.obligation_id in expected_id_set
            ]
            unique: list[SemanticAdjudication] = []
            duplicate: list[str] = []
            for decision in supplied_decisions:
                if any(item.obligation_id == decision.obligation_id for item in unique):
                    duplicate.append(decision.obligation_id)
                    continue
                unique.append(decision)
            supplied_by_id = {decision.obligation_id: decision for decision in unique}
            missing = [
                obligation_id
                for obligation_id in expected_ids
                if obligation_id not in supplied_by_id
            ]
            extra = [
                decision.obligation_id
                for decision in response.decisions
                if decision.obligation_id not in expected_id_set
            ]
            return unique, missing, extra, duplicate

        unique_supplied, missing_ids, extra_ids, duplicate_ids = coverage(d_response)
        if missing_ids and d_outcome.succeeded:
            d_correction_prompt = build_d_correction_prompt(
                pair,
                dossiers,
                missing_ids=missing_ids,
                duplicate_ids=duplicate_ids,
                extra_ids=extra_ids,
            )
            correction_outcome: StructuredCallOutcome[DAdjudicationResponse] = runtime.call(
                kind="d_adjudication_correction",
                schema=DAdjudicationResponse,
                system_prompt=D_SYSTEM_PROMPT,
                prompt=d_correction_prompt,
                artifact_id=f"method/{pair.pair_id}/round-{round_index}/d-adjudication-correction",
            )
            all_outcomes.append(correction_outcome)
            d_stage_outcome = correction_outcome
            if correction_outcome.succeeded:
                d_response = d_response.model_copy(
                    update={
                        "decisions": [
                            *unique_supplied,
                            *correction_outcome.response.decisions,
                        ]
                    }
                )
                unique_supplied, missing_ids, extra_ids, duplicate_ids = coverage(d_response)
            else:
                errors.append(
                    {
                        "stage": "d_adjudication_correction",
                        "error": correction_outcome.result.get(
                            "error",
                            "D correction output unavailable",
                        ),
                        "reason": "The D coverage correction failed; missing obligations remain unresolved.",
                        "basis": "in-node structured contract correction and public runtime outcome",
                    }
                )
        if missing_ids or extra_ids or duplicate_ids:
            diagnostics: list[str] = []
            if missing_ids:
                diagnostics.append(f"missing={missing_ids}")
            if extra_ids:
                diagnostics.append(f"extra={extra_ids}")
            if duplicate_ids:
                diagnostics.append(f"duplicate={duplicate_ids}")
            errors.append(
                {
                    "stage": "d_adjudication",
                    "error": "; ".join(diagnostics),
                    "reason": "D structured output did not cover the exact obligation set; missing units were retained as unresolved.",
                    "basis": "deterministic obligation-ID coverage and uniqueness check",
                }
            )
            missing_response = fallback_d_adjudication(
                missing_ids,
                "D structured output coverage check",
            )
            d_response = d_response.model_copy(
                update={"decisions": unique_supplied + missing_response.decisions}
            )
            unique_supplied, _, _, _ = coverage(d_response)
        decisions = {decision.obligation_id: decision for decision in unique_supplied}
        stage_outputs["d_adjudication"] = d_response.model_dump(mode="json")
        stage_receipts.append(
            _stage_receipt(
                pair=pair,
                stage_id=f"{pair.pair_id}:r{round_index}:d-adjudication",
                stage_name="d_adjudication",
                status="completed" if d_stage_outcome is not None and d_stage_outcome.succeeded and not any(
                    item.get("stage") in {"d_adjudication", "d_adjudication_correction"}
                    for item in errors
                ) else "completed_with_diagnostics",
                artifact_roles=("natural_language", "plantuml_source", "canonical_source_ir", "source_inventory", "fcstm_model", "working_contract", "source_trace", "predicate_registry"),
                output=d_response,
                outcome=d_stage_outcome,
                reason=d_response.reason,
                basis=d_response.basis,
            )
        )
    retry_records = [
        {"stage": outcome.kind, **attempt}
        for outcome in all_outcomes
        for attempt in outcome.attempts
    ]
    for index, prepared in enumerate(prepared_candidates):
        try:
            record, emitted = _deterministic_candidate(
                pair,
                prepared["candidate"],
                round_index,
                index,
                retry_records,
                semantic_adjudication=decisions.get(prepared["obligation_id"]),
                prepared=prepared,
            )
            records.append(record)
            if emitted is not None:
                release.append(emitted)
            stage_receipts.extend(
                [
                    _stage_receipt(
                        pair=pair,
                        stage_id=f"{pair.pair_id}:r{round_index}:i{index}:w",
                        stage_name="w_publication",
                        status="completed",
                        artifact_roles=("fcstm_model", "predicate_registry", "verify_facts"),
                        output={"witness_level": record["witness_level"], "issue_emitted": record["issue_emitted"]},
                        reason="W level and issue publication were computed by the deterministic evidence state machine.",
                        basis="binding, plan support, backend terminal state, receipt verdict, and D adjudication",
                    ),
                ]
            )
            if record.get("audit_bundle") is not None:
                audit_path = output_root / "audit_bundles" / f"{record['issue_id']}.json"
                write_json(audit_path, record["audit_bundle"])
                record["audit_bundle_path"] = str(audit_path)
        except Exception as exc:  # preserve a cell-level diagnostic instead of losing a candidate
            errors.append({"candidate_index": index, "error_type": type(exc).__name__, "message": str(exc), "reason": "Candidate publication failed; the cell remains readable.", "basis": "Candidate-level diagnostic preservation."})
    prompt_hash = _hash_json(
        {
            "contract": contract_prompt,
            "source_grounding": source_prompt,
            "model_grounding": model_prompt,
            "d_adjudication": d_prompt,
            "d_adjudication_correction": d_correction_prompt,
        }
    )
    llm_call = _aggregate_outcomes(all_outcomes)
    cell = {
        "schema": "paper1.evidence_discovery.method_cell.v1",
        "pair_id": pair.pair_id,
        "round": round_index,
        "status": (
            "completed"
            if records and all_outcomes and all(item.succeeded for item in all_outcomes) and not errors
            else "completed_with_diagnostics"
            if records
            else "failed_with_receipt"
        ),
        "prompt_hash": prompt_hash,
        "context_manifest": pair.context_manifest.model_dump(mode="json"),
        "input_hashes": dict(pair.hashes),
        "stage_outputs": stage_outputs,
        "stage_receipts": stage_receipts,
        "model_output": response.model_dump(mode="json"),
        "llm_calls": [outcome.to_dict() for outcome in all_outcomes],
        "llm_call": llm_call,
        "evidence_records": records,
        "report_issue_clusters": release,
        "errors": errors,
        "reason": response.reason,
        "basis": response.basis,
    }
    write_json(output_root / "method" / pair.pair_id / f"round-{round_index}.json", cell)
    return cell


def _judge_prompt(pair: PairInput, ledger_items: list[dict[str, Any]], method_rounds: list[dict[str, Any]]) -> str:
    compact_rounds: list[dict[str, Any]] = []
    for cell in method_rounds:
        compact_rounds.append(
            {
                "round": cell["round"],
                "release_issue_clusters": [
                    {
                        key: issue.get(key)
                        for key in (
                            "issue_id", "title", "requirement_quote", "predicate_id", "binding",
                            "expected", "observed", "d_level", "witness_level", "reason", "basis",
                        )
                    }
                    for issue in cell.get("report_issue_clusters", [])
                ],
            }
        )
    return f"""Assess the three method rounds for frozen pair {pair.pair_id} as an independent judge.

Frozen ledger entries (the judge's only ground-truth answer source; method generation did not read them):
{json.dumps(ledger_items, ensure_ascii=False, sort_keys=True)}

Method release surface for all supplied method rounds (assess only D1/D2 release issues; D0 is excluded):
{json.dumps(compact_rounds, ensure_ascii=False, sort_keys=True)}

A hit requires the same locus and the same property. Wording and evidence depth may differ. A broad
category, an opposite-direction claim, a passing mention, a complaint about a reference artifact, or
a bundle of unrelated issues is not a hit for the ledger item. Emit one ledger assessment for every
ledger_id with separate r1/r2/r3 decisions. Emit one release assessment for every release issue; set
is_false_positive=true only when no frozen ledger item can semantically account for it. Do not omit
units. Every assessment and the top-level response must have non-empty reason and basis fields. Do
not read baseline results, other pairs, historical judge examples, or files outside this input.
"""


def _fallback_judge(ledger_items: list[dict[str, Any]], release: list[dict[str, Any]], reason: str) -> JudgeResponse:
    return JudgeResponse(
        ledger_assessments=[
            LedgerAssessment(
                ledger_id=item["id"],
                reason=f"Provider/schema output was unavailable; ledger item {item['id']} is conservatively marked unhit.",
                basis=f"Provider/schema output was unavailable; conservatively mark ledger item {item['id']} unhit. Runtime diagnostics are stored in llm_call.",
            )
            for item in ledger_items
        ],
        release_assessments=[
            ReleaseAssessment(
                issue_id=item["issue_id"],
                is_false_positive=True,
                reason="Provider/schema output was unavailable; this release issue is conservatively classified as a false positive.",
                basis="Provider/schema output was unavailable; conservatively classify this release issue as false positive.",
            )
            for item in release
        ],
        reason="The independent judge provider or schema result was unavailable; conservative assessments were generated for every supplied unit.",
        basis="deterministic no-silent-drop judge fallback",
    )


def _read_ledger_for_pair(ledger_path: Path, pair_id: str) -> list[dict[str, Any]]:
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    items = data.get("items")
    if not isinstance(items, dict):
        raise ValueError("ledger.json items must be a mapping")
    return [dict(item) for item in items.values() if item.get("pair") == pair_id]


def _normalize_judge(
    response: JudgeResponse,
    ledger_items: list[dict[str, Any]],
    release: list[dict[str, Any]],
) -> JudgeResponse:
    by_id = {item.ledger_id: item for item in response.ledger_assessments}
    assessments = [
        by_id.get(
            item["id"],
            LedgerAssessment(
                ledger_id=item["id"],
                reason="Judge omitted this ledger unit; deterministic completion marks it unhit.",
                basis="judge omitted this ledger unit; deterministic completion marks it unhit",
            ),
        )
        for item in ledger_items
    ]
    release_by_id = {item.issue_id: item for item in response.release_assessments}
    releases = [
        release_by_id.get(
            item["issue_id"],
            ReleaseAssessment(
                issue_id=item["issue_id"],
                is_false_positive=True,
                reason="Judge omitted this release issue; deterministic completion marks it as a false positive.",
                basis="judge omitted this release issue; deterministic completion marks it false positive",
            ),
        )
        for item in release
    ]
    return response.model_copy(update={"ledger_assessments": assessments, "release_assessments": releases})


def _judge_pair(
    *,
    pair: PairInput,
    method_rounds: list[dict[str, Any]],
    ledger_path: Path,
    runtime: PublicStructuredRuntime,
    output_root: Path,
) -> dict[str, Any]:
    ledger_items = _read_ledger_for_pair(ledger_path, pair.pair_id)
    release = [issue for cell in method_rounds for issue in cell.get("report_issue_clusters", [])]
    prompt = _judge_prompt(pair, ledger_items, method_rounds)
    outcome: StructuredCallOutcome[JudgeResponse] = runtime.call(
        kind="judge",
        schema=JudgeResponse,
        system_prompt=JUDGE_SYSTEM_PROMPT,
        prompt=prompt,
        artifact_id=f"judge/{pair.pair_id}",
    )
    response = outcome.response if outcome.succeeded else _fallback_judge(
        ledger_items, release, str(outcome.result.get("error", "judge output unavailable"))
    )
    response = _normalize_judge(response, ledger_items, release)
    payload = {
        "schema": "paper1.evidence_discovery.independent_judge.v1",
        "pair_id": pair.pair_id,
        "status": "completed" if outcome.succeeded else "completed_with_diagnostics",
        "ledger_count": len(ledger_items),
        "release_count": len(release),
        "ledger_source": str(ledger_path),
        "prompt_hash": "sha256:" + __import__("hashlib").sha256(prompt.encode("utf-8")).hexdigest(),
        "llm_call": outcome.to_dict(),
        "judgement": response.model_dump(mode="json"),
        "reason": response.reason,
        "basis": response.basis,
    }
    write_json(output_root / "judge" / f"{pair.pair_id}.json", payload)
    return payload


def _metrics(
    *,
    ledger_path: Path,
    pair_method: dict[str, list[dict[str, Any]]],
    pair_judge: dict[str, dict[str, Any]],
    selected_pair_ids: Sequence[str],
    rounds: int,
) -> dict[str, Any]:
    data = json.loads(ledger_path.read_text(encoding="utf-8"))
    selected = set(selected_pair_ids)
    all_items = [item for item in data["items"].values() if item.get("pair") in selected]
    dimensions = {
        "overall": lambda item: True,
        "L2": lambda item: item.get("L") == "L2",
        "D2xL2": lambda item: item.get("D") == "D2" and item.get("L") == "L2",
    }
    metrics: dict[str, Any] = {}
    assessment_map: dict[str, dict[str, LedgerAssessment]] = {}
    for pair_id, payload in pair_judge.items():
        judgement = payload["judgement"]
        assessment_map[pair_id] = {item["ledger_id"]: LedgerAssessment.model_validate(item) for item in judgement["ledger_assessments"]}
    for name, selector in dimensions.items():
        selected = [item for item in all_items if selector(item)]
        positions = len(selected) * rounds
        hit1 = hit3 = hitall = 0
        for item in selected:
            assessment = assessment_map.get(item["pair"], {}).get(
                item["id"],
                LedgerAssessment(
                    ledger_id=item["id"],
                    reason="No judge assessment was available; deterministic metrics count this ledger unit as unhit.",
                    basis="missing deterministic assessment",
                ),
            )
            round_hits = [
                bool(getattr(assessment, f"hit_r{round_index}"))
                for round_index in range(1, rounds + 1)
            ]
            hit1 += sum(round_hits)
            hit3 += int(any(round_hits))
            hitall += int(all(round_hits))
        metrics[name] = {
            "entries": len(selected),
            "positions": positions,
            "hit_at_1": hit1,
            "hit_at_1_rate": hit1 / positions if positions else 0.0,
            "hit_at_3": hit3,
            "hit_at_3_rate": hit3 / len(selected) if selected else 0.0,
            "hit_at_all": hitall,
            "hit_at_all_rate": hitall / len(selected) if selected else 0.0,
        }
    emissions = [issue for cells in pair_method.values() for cell in cells for issue in cell.get("report_issue_clusters", [])]
    release_by_pair = {
        pair_id: {item["issue_id"]: item for item in payload["judgement"]["release_assessments"]}
        for pair_id, payload in pair_judge.items()
    }
    fp = sum(int(release_by_pair.get(issue["issue_id"].split(":", 1)[0], {}).get(issue["issue_id"], {}).get("is_false_positive", True)) for issue in emissions)
    release_count = len(emissions)
    return {
        "overall": metrics,
        "emissions": {"release_issue_count": release_count, "false_positive": fp, "precision": (release_count - fp) / release_count if release_count else 0.0},
        "method_quality": {
            "witness_levels": dict(Counter(record.get("witness_level") for cells in pair_method.values() for cell in cells for record in cell.get("evidence_records", []))),
            "d_levels": dict(Counter(record.get("d_level") for cells in pair_method.values() for cell in cells for record in cell.get("evidence_records", []))),
        },
    }


def _failure_method_cell(
    *,
    pair_id: str,
    round_index: int,
    output_root: Path,
    error: BaseException,
) -> dict[str, Any]:
    payload = {
        "schema": "paper1.evidence_discovery.method_cell.v1",
        "pair_id": pair_id,
        "round": round_index,
        "status": "failed_with_receipt",
        "model_output": {},
        "llm_call": {
            "kind": "method",
            "status": "not_started",
            "response": None,
            "result": {},
            "attempts": [],
            "usage": [],
            "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
        },
        "evidence_records": [],
        "report_issue_clusters": [],
        "errors": [{
            "error_type": type(error).__name__,
            "message": str(error),
            "reason": "The pair-level failure was converted to an explicit method-cell receipt.",
            "basis": "no-silent-drop frozen cell contract",
        }],
        "reason": "Pair setup or orchestration failed; no method evidence was silently discarded.",
        "basis": "deterministic pair-level failure receipt",
    }
    write_json(output_root / "method" / pair_id / f"round-{round_index}.json", payload)
    return payload


def _failure_judge_payload(
    *,
    pair_id: str,
    ledger_path: Path,
    release: list[dict[str, Any]],
    output_root: Path,
    error: BaseException,
) -> dict[str, Any]:
    try:
        ledger_items = _read_ledger_for_pair(ledger_path, pair_id)
        ledger_error = None
    except Exception as ledger_exc:
        ledger_items = []
        ledger_error = {
            "error_type": type(ledger_exc).__name__,
            "message": str(ledger_exc),
            "reason": "The frozen ledger could not be loaded for conservative judge completion.",
            "basis": "ledger read failure receipt",
        }
    reason = f"judge setup failed: {type(error).__name__}: {error}"
    judgement = _fallback_judge(ledger_items, release, reason).model_dump(mode="json")
    payload = {
        "schema": "paper1.evidence_discovery.independent_judge.v1",
        "pair_id": pair_id,
        "status": "completed_with_diagnostics",
        "ledger_count": len(ledger_items),
        "release_count": len(release),
        "ledger_source": str(ledger_path),
        "prompt_hash": None,
        "llm_call": {
            "kind": "judge",
            "status": "not_started",
            "response": None,
            "result": {},
            "attempts": [],
            "usage": [],
            "cost": {"eligible": True, "total_usd": 0.0, "attempts": []},
        },
        "judgement": judgement,
        "reason": "The independent judge did not start; conservative completion was generated for the frozen ledger and release surface.",
        "basis": "deterministic no-silent-drop judge fallback",
        "errors": [
            {
                "error_type": type(error).__name__,
                "message": str(error),
                "reason": "judge setup failure receipt",
                "basis": "pair-level orchestration diagnostic",
            },
            *([ledger_error] if ledger_error else []),
        ],
    }
    write_json(output_root / "judge" / f"{pair_id}.json", payload)
    return payload


def _write_pair_status(output_root: Path, pair_id: str, status: dict[str, Any]) -> None:
    write_json(
        output_root / "pairs" / pair_id / "status.json",
        {
            "schema": "paper1.evidence_discovery.pair_status.v1",
            "pair_id": pair_id,
            **status,
            "reason": status.get("reason", "pair status is a deterministic run receipt"),
            "basis": status.get("basis", "frozen 54-pair three-round protocol"),
        },
    )


def run_experiment(
    *,
    report_root: str | Path,
    ledger_path: str | Path,
    output_dir: str | Path,
    profile: str = "gpt-5.6-luna",
    rounds: int = 3,
    resume: bool = False,
    allow_live: bool = False,
    pair_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    if rounds not in {1, 3}:
        raise ValueError("rounds must be 1 for a diagnostic run or 3 for the frozen protocol")
    if profile != "fixture" and not allow_live:
        raise RuntimeError(
            "live Luna/full experiment is disabled until input-closure and staged-flow review completes; "
            "use explicit allow_live=True only after review"
        )
    selected_pair_ids = tuple(
        dict.fromkeys(FROZEN_PAIR_IDS if pair_ids is None else pair_ids)
    )
    unknown_pair_ids = sorted(set(selected_pair_ids) - set(FROZEN_PAIR_IDS))
    if not selected_pair_ids:
        raise ValueError("at least one frozen pair ID is required")
    if unknown_pair_ids:
        raise ValueError(f"pair IDs are outside the frozen 54-pair protocol: {unknown_pair_ids}")
    if profile != "fixture":
        if pair_ids is None:
            raise RuntimeError(
                "live diagnostic runs require an explicit pair_ids subset; the 54-pair full run is blocked"
            )
        if len(selected_pair_ids) > len(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS):
            raise RuntimeError(
                "live diagnostic runs are capped at six explicit pair IDs; full 54-pair execution remains blocked"
            )
        if rounds == 3 and pair_ids is None:
            raise RuntimeError("three-round live runs also require an explicit pair_ids subset")
    output_root = Path(output_dir).expanduser().resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    ledger = Path(ledger_path).expanduser().resolve()
    registry = load_registry()
    source_provenance = _source_provenance()
    runtime = (
        FixtureStructuredRuntime()
        if profile == "fixture"
        else PublicStructuredRuntime(profile, output_root / "llm")
    )
    pair_method: dict[str, list[dict[str, Any]]] = {}
    pair_judge: dict[str, dict[str, Any]] = {}
    per_pair: dict[str, dict[str, Any]] = {}
    for pair_id in selected_pair_ids:
        pair_start = datetime.now(timezone.utc).isoformat()
        pair_dir = Path(report_root).expanduser().resolve() / "pairs" / pair_id
        rounds_data: list[dict[str, Any]] = []
        if resume:
            for round_index in range(1, rounds + 1):
                cell_path = output_root / "method" / pair_id / f"round-{round_index}.json"
                if not cell_path.is_file():
                    break
                try:
                    cell = json.loads(cell_path.read_text(encoding="utf-8"))
                    if (
                        not isinstance(cell, dict)
                        or cell.get("pair_id") != pair_id
                        or cell.get("round") != round_index
                    ):
                        break
                except (OSError, json.JSONDecodeError):
                    break
                rounds_data.append(cell)
            judge_path = output_root / "judge" / f"{pair_id}.json"
            if len(rounds_data) == rounds and judge_path.is_file():
                try:
                    judge = json.loads(judge_path.read_text(encoding="utf-8"))
                    if not isinstance(judge, dict) or judge.get("pair_id") != pair_id:
                        raise ValueError("existing judge pair ID mismatch")
                    pair_method[pair_id] = rounds_data
                    pair_judge[pair_id] = judge
                    status_path = output_root / "pairs" / pair_id / "status.json"
                    if status_path.is_file():
                        stored_status = json.loads(status_path.read_text(encoding="utf-8"))
                    else:
                        stored_status = {}
                    if isinstance(stored_status, dict) and stored_status.get("status"):
                        per_pair[pair_id] = {
                            key: stored_status[key]
                            for key in (
                                "status", "started_at", "method_cells", "judge_status", "errors", "cost_usd",
                            )
                            if key in stored_status
                        }
                    else:
                        errors = sum(
                            len(cell.get("errors", []))
                            + int(cell.get("llm_call", {}).get("status") != "success")
                            for cell in rounds_data
                        )
                        per_pair[pair_id] = {
                            "status": "completed" if errors == 0 and judge.get("llm_call", {}).get("status") == "success" else "completed_with_diagnostics",
                            "started_at": pair_start,
                            "method_cells": rounds,
                            "judge_status": judge.get("status", "completed_with_diagnostics"),
                            "errors": errors + int(judge.get("llm_call", {}).get("status") != "success"),
                            "cost_usd": sum(
                                float(cell.get("llm_call", {}).get("cost", {}).get("total_usd") or 0.0)
                                for cell in rounds_data
                            ) + float(judge.get("llm_call", {}).get("cost", {}).get("total_usd") or 0.0),
                        }
                    continue
                except (OSError, json.JSONDecodeError, ValueError, TypeError):
                    # A partial or malformed existing pair is resumed from its
                    # last valid method cell and receives a fresh judge receipt.
                    pass
        try:
            pair = load_pair(pair_dir)
            previous: list[dict[str, Any]] = (
                rounds_data[-1].get("report_issue_clusters", []) if rounds_data else []
            )
            for round_index in range(len(rounds_data) + 1, rounds + 1):
                cell = _method_cell(
                    pair=pair,
                    round_index=round_index,
                    runtime=runtime,
                    previous=previous,
                    output_root=output_root,
                )
                rounds_data.append(cell)
                previous = cell.get("report_issue_clusters", [])
            pair_method[pair_id] = rounds_data
            judge = _judge_pair(
                pair=pair,
                method_rounds=rounds_data,
                ledger_path=ledger,
                runtime=runtime,
                output_root=output_root,
            )
            pair_judge[pair_id] = judge
            errors = sum(len(cell.get("errors", [])) + int(cell.get("llm_call", {}).get("status") != "success") for cell in rounds_data)
            pair_status = "completed" if errors == 0 and judge["llm_call"]["status"] == "success" else "completed_with_diagnostics"
            per_pair[pair_id] = {
                "status": pair_status,
                "started_at": pair_start,
                "method_cells": len(rounds_data),
                "judge_status": judge["status"],
                "errors": errors + int(judge["llm_call"]["status"] != "success"),
                "cost_usd": sum(float(cell["llm_call"].get("cost", {}).get("total_usd") or 0.0) for cell in rounds_data) + float(judge["llm_call"].get("cost", {}).get("total_usd") or 0.0),
            }
            _write_pair_status(output_root, pair_id, per_pair[pair_id])
        except Exception as exc:
            # Existing input/runtime defects become explicit records for every
            # requested method cell
            # and a judge fallback; the outer experiment never silently loses a pair.
            while len(rounds_data) < rounds:
                rounds_data.append(
                    _failure_method_cell(
                        pair_id=pair_id,
                        round_index=len(rounds_data) + 1,
                        output_root=output_root,
                        error=exc,
                    )
                )
            pair_method[pair_id] = rounds_data
            release = [issue for cell in rounds_data for issue in cell.get("report_issue_clusters", [])]
            pair_judge[pair_id] = _failure_judge_payload(
                pair_id=pair_id,
                ledger_path=ledger,
                release=release,
                output_root=output_root,
                error=exc,
            )
            per_pair[pair_id] = {
                "status": "failed_with_receipt",
                "started_at": pair_start,
                "method_cells": rounds,
                "judge_status": "completed_with_diagnostics",
                "errors": 4,
                "cost_usd": 0.0,
            }
            _write_pair_status(output_root, pair_id, per_pair[pair_id])
    metrics = _metrics(
        ledger_path=ledger,
        pair_method=pair_method,
        pair_judge=pair_judge,
        selected_pair_ids=selected_pair_ids,
        rounds=rounds,
    )
    method_cost = sum(float(cell["llm_call"].get("cost", {}).get("total_usd") or 0.0) for cells in pair_method.values() for cell in cells)
    judge_cost = sum(float(payload.get("llm_call", {}).get("cost", {}).get("total_usd") or 0.0) for payload in pair_judge.values())
    summary = {
        "schema": "paper1.evidence_discovery.run_summary.v1",
        "run_started_at": datetime.now(timezone.utc).isoformat(),
        "profile": profile,
        "source_commit": source_provenance["source_commit"],
        "source_branch": source_provenance["source_branch"],
        "source_provenance": source_provenance,
        "resume": resume,
        "rounds": rounds,
        "registry_version": registry.version,
        "registry_hash": registry.registry_hash,
        "pair_count": len(selected_pair_ids),
        "protocol_pair_count": len(FROZEN_PAIR_IDS),
        "selected_pair_ids": list(selected_pair_ids),
        "scope": "full_protocol" if len(selected_pair_ids) == len(FROZEN_PAIR_IDS) else "diagnostic_subset",
        "selection": {
            "pair_ids": list(selected_pair_ids),
            "reason": "The selected subset is recorded separately from the frozen protocol denominator.",
            "basis": (
                "v27-predecessor representative set cross-checked against "
                "runs/paper1/luna-five-v25-20260819 for 0004/0023/0029/0046/0053, "
                "and runs/paper1/witness-search/v39-dprompt-replay-20260820 plus "
                "v40-dprompt-checklist-20260820 for 0035"
                if set(selected_pair_ids) == set(REPRESENTATIVE_DIAGNOSTIC_PAIR_IDS)
                else "explicit pair_ids supplied by the run caller"
            ),
        },
        "method_cell_count": sum(len(value) for value in pair_method.values()),
        "judge_pair_count": len(pair_judge),
        "method_cost_usd": method_cost,
        "judge_cost_usd": judge_cost,
        "metrics": metrics,
        "per_pair": per_pair,
        "failed_pairs": [pair_id for pair_id, row in per_pair.items() if row["status"] == "failed_with_receipt"],
        "method_cells_with_diagnostics": [
            f"{pair_id}:r{cell['round']}"
            for pair_id, cells in pair_method.items()
            for cell in cells
            if cell.get("errors") or cell.get("llm_call", {}).get("status") != "success"
        ],
        "reason": "The selected method cells and independent judge receipts are represented without expanding beyond the requested pair scope.",
        "basis": "four-family-19-core.v1, frozen 54-pair protocol, and explicit selected_pair_ids",
    }
    write_json(output_root / "summary.json", summary)
    write_markdown_summary(output_root / "SUMMARY.md", summary)
    write_json(output_root / "audit_index.json", {"pairs": per_pair, "method_cell_count": summary["method_cell_count"], "judge_pair_count": summary["judge_pair_count"]})
    return summary
