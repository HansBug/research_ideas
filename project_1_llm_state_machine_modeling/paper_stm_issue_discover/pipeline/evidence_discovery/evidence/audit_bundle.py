from __future__ import annotations

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..compiler.lowering import PredicatePlan
from ..inputs.models import PairInput
from ..semantics.adjudication import SemanticAdjudication
from ..semantics.binding import BindingResult
from .receipts import RawReceipt


class W2AuditBundle(BaseModel):
    """Complete independently reproducible evidence package for one W2 record."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    schema: Literal["paper1.evidence_discovery.w2_audit_bundle.v2"] = Field(description="Versioned W2 audit schema identifier.")
    generated_at: datetime = Field(description="Timezone-aware backend evidence generation timestamp.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen pair owning this W2 evidence record.")
    obligation_id: str = Field(min_length=1, description="Stable pair-round-candidate obligation identity.")
    input_context: dict[str, Any] = Field(description="Complete context manifest, artifact hashes, roles, and deterministic facts.")
    predicate_id: str = Field(min_length=1, description="Frozen predicate ID compiled and executed for this W2 result.")
    registry_version: str = Field(min_length=1, description="Exact frozen predicate registry version.")
    predicate_logic: dict[str, Any] = Field(description="Complete predicate semantics, bound inputs, assumptions, sources, and support state.")
    binding: dict[str, Any] = Field(description="Exact model/source references and deterministic binding rationale.")
    compiled_program: dict[str, Any] = Field(description="Full assertion or formal program source and its SHA-256 hash.")
    model_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the exact executed FCSTM model.")
    program_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the exact compiled assertion or formal program.")
    backend_result: dict[str, Any] = Field(description="Complete real deterministic backend receipt.")
    structured_run_summary: dict[str, Any] = Field(description="Backend terminal summary plus available stdout/stderr or explicit unavailability.")
    execution_environment: dict[str, Any] = Field(description="Non-secret Python and platform execution environment identity.")
    terminal_state: str = Field(min_length=1, description="Actual backend terminal state used by deterministic W publication.")
    counterexample: list[dict[str, Any]] = Field(default_factory=list, description="Structured backend counterexample, when present.")
    trace: list[dict[str, Any]] = Field(default_factory=list, description="Structured backend graph or execution trace.")
    semantic_adjudication: dict[str, Any] | None = Field(default=None, description="Typed method-owned semantic D facts, when available.")
    retry_records: list[dict[str, Any]] = Field(default_factory=list, description="All model/provider retry and billing records associated with the cell.")
    source_attribution: dict[str, Any] = Field(description="Requirement, source/model, plan, and backend receipt attribution chain.")
    method_receipt: dict[str, Any] = Field(description="Terminal method receipt link or explicit pre-finalization state.")
    judge_receipt: dict[str, Any] = Field(description="Terminal independent judge link or explicit pre-finalization state.")
    audit_finalization: dict[str, Any] | None = Field(default=None, description="Judge-time finalization timestamp, receipt hash, reason, and basis.")
    issue_emitted: bool | None = Field(default=None, description="Whether deterministic D/W publication emitted this W2 record as a release issue.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the deterministic evidence and D publication state.")
    basis: str = Field(min_length=1, description="Non-empty predicate, binding, program, backend, and source basis.")
    audit_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the complete bundle excluding this hash field at calculation time.")


def validate_and_hash_w2_audit_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize a W2 bundle through Pydantic before calculating its hash."""

    candidate = dict(payload)
    candidate["audit_hash"] = "sha256:" + "0" * 64
    normalized = W2AuditBundle.model_validate(candidate).model_dump(mode="json")
    normalized.pop("audit_hash", None)
    normalized["audit_hash"] = "sha256:" + hashlib.sha256(
        json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return W2AuditBundle.model_validate(normalized).model_dump(mode="json")


def build_audit_bundle(
    *,
    pair: PairInput,
    obligation_id: str,
    binding: BindingResult,
    plan: PredicatePlan,
    receipt: RawReceipt,
    source_attribution: dict[str, Any],
    reason: str,
    basis: str,
    retry_records: list[dict[str, Any]],
    semantic_adjudication: SemanticAdjudication | None = None,
) -> dict[str, Any]:
    program = plan.formal_program or "UNCOMPILED_W1_PLAN"
    program_hash = plan.formal_program_hash or (
        "sha256:" + hashlib.sha256(program.encode("utf-8")).hexdigest()
    )
    payload = {
        "schema": "paper1.evidence_discovery.w2_audit_bundle.v2",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "pair_id": pair.pair_id,
        "obligation_id": obligation_id,
        "input_context": {
            "manifest": pair.context_manifest.model_dump(mode="json") if pair.context_manifest else None,
            "artifact_hashes": dict(pair.hashes),
            "canonical_source_ir_hash": pair.hashes.get("canonical"),
            "source_roles": {
                "plantuml": "author_source_localization_only",
                "canonical_source_ir": "author_source_localization_only",
                "exact_source_inventory": "author_source_inventory",
                "fcstm": "closed_model_execution",
                "inspection_facts": "deterministic_inventory_and_diagnostics",
                "verify_facts": "deterministic_finite_verification_summary",
                "smt_facts": "normalized_formal_inputs_not_solver_result",
            },
            "inspection_equivalent_facts": pair.inspection_facts.model_dump(mode="json") if pair.inspection_facts else None,
            "verify_facts": pair.verify_facts.model_dump(mode="json") if pair.verify_facts else None,
            "smt_facts": pair.smt_facts.model_dump(mode="json") if pair.smt_facts else None,
        },
        "predicate_id": plan.predicate_id,
        "registry_version": plan.registry_version,
        "predicate_logic": {
            "predicate_id": plan.predicate_id,
            "name": plan.predicate_name,
            "family": plan.family,
            "semantics": plan.semantics,
            "inputs": plan.inputs,
            "soundness_fragment": plan.soundness_fragment,
            "assumptions": list(plan.assumptions),
            "source_ids": list(plan.source_ids),
            "source_audit_status": plan.source_audit_status,
            "source_gate_passed": plan.source_gate_passed,
            "binding_complete": plan.binding_complete,
            "missing_inputs": list(plan.missing_inputs),
        },
        "binding": {
            "element_refs": list(binding.element_refs),
            "source_refs": list(binding.source_refs),
            "reason": binding.reason,
            "basis": binding.basis,
        },
        "compiled_program": {
            "source": program,
            "sha256": program_hash,
        },
        "model_hash": pair.hashes["fcstm"],
        "program_hash": program_hash,
        "backend_result": receipt.to_dict(),
        "structured_run_summary": {
            "backend": receipt.backend,
            "terminal_state": receipt.terminal_state,
            "verdict": receipt.verdict,
            "run_metadata": receipt.run_metadata,
            "stdout": receipt.run_metadata.get("stdout", "unavailable: backend returned a structured receipt"),
            "stderr": receipt.run_metadata.get("stderr", "unavailable: backend returned a structured receipt"),
            "reason": "The deterministic backend is audited through its structured result; raw streams are retained when the backend exposes them.",
            "basis": "RawReceipt and backend run_metadata",
        },
        "execution_environment": {
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "platform": platform.platform(),
            "python_executable_path_hash": "sha256:" + hashlib.sha256(sys.executable.encode("utf-8")).hexdigest(),
            "reason": "The audit records the deterministic backend process environment without exposing secrets.",
            "basis": "Python platform metadata and executable path hash",
        },
        "terminal_state": receipt.terminal_state,
        "counterexample": receipt.counterexample,
        "trace": receipt.trace,
        "semantic_adjudication": (
            semantic_adjudication.model_dump(mode="json")
            if semantic_adjudication is not None
            else None
        ),
        "retry_records": retry_records,
        "source_attribution": source_attribution,
        "method_receipt": {
            "status": "pending_cell_finalization",
            "reason": "The W2 bundle is created before the enclosing method-cell receipt is atomically written.",
            "basis": "method cell construction order",
        },
        "judge_receipt": {
            "status": "pending_independent_judge",
            "reason": "The independent judge runs only after every method round is terminal.",
            "basis": "method/judge isolation boundary",
        },
        "audit_finalization": None,
        "issue_emitted": None,
        "reason": reason,
        "basis": basis,
    }
    return validate_and_hash_w2_audit_bundle(payload)
