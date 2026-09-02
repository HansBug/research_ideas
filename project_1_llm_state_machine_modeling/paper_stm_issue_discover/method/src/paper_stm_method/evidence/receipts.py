from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class RawReceipt(BaseModel):
    """Structured terminal receipt emitted by one deterministic evidence backend."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    receipt_id: str = Field(min_length=1, description="Stable identifier for this backend execution receipt.")
    backend: str = Field(min_length=1, description="Backend implementation and predicate dispatch label.")
    terminal_state: str = Field(min_length=1, description="Backend terminal state, including completed, unknown, timeout, or unsupported.")
    verdict: str = Field(min_length=1, description="Backend result such as true, false, or unknown; never a W or D level.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the backend result and its boundary.")
    basis: str = Field(min_length=1, description="Non-empty algorithm, input, or diagnostic basis for the backend result.")
    counterexample: list[dict[str, Any]] = Field(default_factory=list, description="Structured counterexample facts when the backend finds a violating result.")
    trace: list[dict[str, Any]] = Field(default_factory=list, description="Structured execution or graph trace supporting the backend result.")
    run_metadata: dict[str, Any] = Field(default_factory=dict, description="Version, input hash, boundary, and diagnostic metadata for this execution.")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


class PredicateExecutionReceipt(BaseModel):
    """Auditable execution boundary for one frozen predicate plan.

    This receipt is emitted for both finding and passing checks. Bibliography
    provenance remains attached as registry metadata, but never controls the
    runtime W state. A completed true/false result is W2 when the typed plan
    and artifact attribution are complete; failure information is orthogonal.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema: Literal[
        "evidence-discovery.predicate_execution_receipt.v1",
        "evidence-discovery.predicate_execution_receipt.v2",
    ] = Field(
        default="evidence-discovery.predicate_execution_receipt.v2",
        description="Versioned predicate execution receipt schema identifier.",
    )
    predicate_id: str | None = Field(
        default=None,
        description="Frozen predicate ID executed, or null for an explicitly unexpressed candidate.",
    )
    contract_id: str = Field(min_length=1, description="Atomic NL contract owning this execution attempt.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen pair owning the execution.")
    run_id: str = Field(pattern=r"^[0-9a-f]{32}$", description="Method run identity owning the execution.")
    obligation_id: str = Field(min_length=1, description="Stable candidate obligation identity.")
    typed_inputs: dict[str, Any] = Field(description="Complete normalized typed predicate inputs used by the plan.")
    typed_inputs_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of canonical typed_inputs.")
    compiled_program: str | None = Field(default=None, description="Compiled program source, when the executable boundary was reached.")
    compiled_program_hash: str | None = Field(default=None, pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of compiled_program, when present.")
    backend: str = Field(min_length=1, description="Deterministic backend dispatch label.")
    algorithm_version: str = Field(min_length=1, description="Backend algorithm version copied from the raw receipt.")
    terminal_state: str = Field(min_length=1, description="Actual raw backend terminal state retained without collapsing timeout, unsupported, and error outcomes.")
    verdict: Literal["pass", "violation", "unsupported", "blocked"] = Field(description="Normalized execution verdict; it is not W, D, or L.")
    raw_verdict: str = Field(min_length=1, description="Backend-native verdict retained without normalization.")
    execution_status: Literal["executed", "unsupported", "blocked"] = Field(description="Legacy-compatible coarse projection of execution_state: completed maps to executed, not_attempted to unsupported, and failed to blocked.")
    witness_level: Literal["W0", "W1", "W2"] = Field(description="Deterministic three-level witness result derived from exact binding, legal inputs, attribution, and execution state; it never encodes a failure state.")
    execution_state: Literal["not_attempted", "completed", "failed"] = Field(description="Orthogonal execution audit state. completed is reserved for a real terminating true/false backend result.")
    predicate_verdict: Literal["true", "false"] | None = Field(default=None, description="Terminal Boolean predicate result when execution_state is completed; null for not_attempted or failed execution.")
    failure_kind: Literal["provider_error", "timeout", "backend_error", "invalid_input", "unsupported_backend", "attribution_failure"] | None = Field(default=None, description="Structured non-W failure classification. Failure cannot be interpreted as a violation.")
    degraded_from: Literal["W2"] | None = Field(default=None, description="W2 when a previously executable candidate was deterministically downgraded because evaluation did not complete legally; otherwise null.")
    degradation_reason: str | None = Field(default=None, description="Non-empty reason for a W2-to-W1/W0 degradation, or null when no degradation occurred.")
    attempt_count: int = Field(ge=0, description="Number of deterministic backend attempts represented by this receipt, including one controlled retry when recorded.")
    retry_records: tuple[dict[str, Any], ...] = Field(default=(), description="Immutable retry and billing records for all attempts; provider retries remain separately marked as non-billable.")
    billable: bool = Field(description="Whether any represented attempt is billable under the global method pricing policy.")
    independent_semantic_basis: bool = Field(description="Whether a closed semantic basis independent of a failed backend exists for D/publication review; failure alone is always false evidence.")
    artifact_attribution: dict[str, Any] = Field(default_factory=dict, description="Current-artifact NL, PlantUML, canonical source IR, FCSTM, inspect-equivalent fact, model/program, and receipt attribution chain.")
    artifact_attribution_complete: bool = Field(description="Whether the executed-artifact attribution chain is complete enough for W2.")
    backend_result: dict[str, Any] = Field(description="Complete immutable RawReceipt payload.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the execution result and its boundary.")
    basis: str = Field(min_length=1, description="Non-empty typed-input, compiler, source, and backend basis.")
    receipt_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of this receipt excluding receipt_hash.")


def _canonical_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_predicate_execution_receipt(
    *,
    pair_id: str,
    run_id: str,
    contract_id: str,
    obligation_id: str,
    plan: Any,
    receipt: RawReceipt,
    source_attribution: dict[str, Any] | None = None,
    retry_records: list[dict[str, Any]] | None = None,
    independent_semantic_basis: bool = False,
    binding_precise: bool | None = None,
) -> dict[str, Any]:
    """Normalize one compiled plan and RawReceipt into an immutable execution record.

    ``binding_precise`` is supplied by production callers from the current
    :class:`BindingResult`.  ``PredicatePlan.binding_precise`` remains in the
    serialized plan for replay compatibility, but cannot overrule a live
    imprecise binding when a W state is created.
    """

    typed_inputs = plan.inputs.model_dump(mode="json")
    typed_inputs_hash = _canonical_hash(typed_inputs)
    program = plan.formal_program
    program_hash = plan.formal_program_hash
    retry_rows = tuple(retry_records or ())
    attribution = dict(source_attribution or {})
    attribution_complete = _artifact_attribution_complete(attribution, plan)
    input_shape_valid = bool(getattr(plan, "input_shape_valid", False))
    binding_complete = bool(getattr(plan, "binding_complete", False))
    backend_available = bool(getattr(plan, "backend_available", getattr(plan, "executable", False)))
    fragment_ok = bool(getattr(plan, "soundness_fragment_satisfied", getattr(plan, "executable", False)))
    plan_binding_precise = bool(getattr(plan, "binding_precise", True))
    effective_binding_precise = (
        plan_binding_precise
        if binding_precise is None
        else bool(binding_precise)
    )
    registered = bool(getattr(plan, "predicate_registered", plan.predicate_id is not None))
    legal_execution_plan = all(
        (registered, effective_binding_precise, input_shape_valid, binding_complete, backend_available, fragment_ok)
    )
    raw_failure_kind = receipt.run_metadata.get("failure_kind")
    if raw_failure_kind not in {
        None,
        "provider_error",
        "timeout",
        "backend_error",
        "invalid_input",
        "unsupported_backend",
        "attribution_failure",
    }:
        raw_failure_kind = "backend_error"
    # Validate the typed plan before admitting a historical or current Boolean
    # receipt. A backend that happened to return false for an illegal input did
    # not perform the frozen predicate proposition and cannot become a W2
    # violation during replay.
    if raw_failure_kind == "invalid_input" or not input_shape_valid or not binding_complete:
        verdict = "unsupported"
        execution_state = "not_attempted"
        predicate_verdict = None
        failure_kind = "invalid_input"
    elif raw_failure_kind == "unsupported_backend" or not backend_available or receipt.terminal_state == "unsupported" or receipt.backend == "none":
        verdict = "unsupported"
        execution_state = "not_attempted"
        predicate_verdict = None
        failure_kind = "unsupported_backend"
    elif receipt.terminal_state == "completed" and receipt.verdict == "true":
        verdict = "pass"
        execution_state = "completed"
        predicate_verdict = "true"
        failure_kind = None
    elif receipt.terminal_state == "completed" and receipt.verdict == "false":
        verdict = "violation"
        execution_state = "completed"
        predicate_verdict = "false"
        failure_kind = None
    elif raw_failure_kind == "provider_error":
        verdict = "blocked"
        execution_state = "failed"
        predicate_verdict = None
        failure_kind = "provider_error"
    elif raw_failure_kind == "timeout" or receipt.terminal_state == "timeout":
        verdict = "blocked"
        execution_state = "failed"
        predicate_verdict = None
        failure_kind = "timeout"
    elif raw_failure_kind == "attribution_failure" or receipt.terminal_state == "error" or receipt.backend.startswith("error:"):
        verdict = "blocked"
        execution_state = "failed"
        predicate_verdict = None
        failure_kind = "attribution_failure" if raw_failure_kind == "attribution_failure" else "backend_error"
    else:
        verdict = "blocked"
        execution_state = "failed"
        predicate_verdict = None
        failure_kind = "unsupported_backend"
    if not attribution_complete and execution_state == "completed":
        execution_state = "failed"
        predicate_verdict = None
        verdict = "blocked"
        failure_kind = "attribution_failure"
    witness_level: Literal["W0", "W1", "W2"]
    if not effective_binding_precise:
        witness_level = "W0"
    elif legal_execution_plan and attribution_complete and execution_state == "completed":
        witness_level = "W2"
    else:
        witness_level = "W1"
    degraded_from = "W2" if effective_binding_precise and legal_execution_plan and execution_state != "completed" else None
    degradation_reason = (
        f"Execution did not reach a legal completed true/false result: {failure_kind}."
        if degraded_from is not None
        else None
    )
    execution_status: Literal["executed", "unsupported", "blocked"] = (
        "executed" if execution_state == "completed"
        else "unsupported" if execution_state == "not_attempted"
        else "blocked"
    )
    payload: dict[str, Any] = {
        "predicate_id": plan.predicate_id,
        "contract_id": contract_id,
        "pair_id": pair_id,
        "run_id": run_id,
        "obligation_id": obligation_id,
        "typed_inputs": typed_inputs,
        "typed_inputs_hash": typed_inputs_hash,
        "compiled_program": program,
        "compiled_program_hash": program_hash,
        "backend": receipt.backend,
        "algorithm_version": str(receipt.run_metadata.get("algorithm_version", "unknown")),
        "terminal_state": receipt.terminal_state,
        "verdict": verdict,
        "raw_verdict": receipt.verdict,
        "execution_status": execution_status,
        "witness_level": witness_level,
        "execution_state": execution_state,
        "predicate_verdict": predicate_verdict,
        "failure_kind": failure_kind,
        "degraded_from": degraded_from,
        "degradation_reason": degradation_reason,
        "attempt_count": 1 + len(retry_rows),
        "retry_records": retry_rows,
        "billable": any(bool(item.get("billable")) for item in retry_rows),
        "independent_semantic_basis": independent_semantic_basis,
        "artifact_attribution": attribution,
        "artifact_attribution_complete": attribution_complete,
        "backend_result": receipt.to_dict(),
        "reason": receipt.reason,
        "basis": (
            f"plan={plan.plan_id}; registered={registered}; plan_precise={plan_binding_precise}; precise={effective_binding_precise}; "
            f"input_shape_valid={input_shape_valid}; binding_complete={binding_complete}; "
            f"backend_available={backend_available}; fragment={fragment_ok}; "
            f"artifact_attribution_complete={attribution_complete}; {receipt.basis}"
        ),
        "receipt_hash": "sha256:" + "0" * 64,
    }
    normalized = PredicateExecutionReceipt.model_validate(payload).model_dump(mode="json")
    normalized.pop("receipt_hash", None)
    normalized["receipt_hash"] = _canonical_hash(normalized)
    return PredicateExecutionReceipt.model_validate(normalized).model_dump(mode="json")


def _artifact_attribution_complete(attribution: dict[str, Any], plan: Any) -> bool:
    """Require the current-artifact chain that a W2 result must expose.

    A completed backend result is not source-bound merely because it has a
    model hash.  W2 additionally requires the exact normative quote/source
    references and the precise carrier binding that connect this concrete
    execution to the current input pair.
    """

    if not getattr(plan, "artifact_attribution_complete", False):
        return False
    required = {"requirement", "model", "plan", "receipt"}
    if not required.issubset(attribution):
        return False
    instance = attribution.get("instance_authority")
    if not isinstance(instance, dict):
        return False
    quote = instance.get("requirement_quote")
    source_refs = instance.get("source_refs")
    element_refs = instance.get("binding_element_refs")
    return (
        isinstance(quote, str)
        and bool(quote.strip())
        and isinstance(source_refs, list)
        and all(isinstance(ref, str) and ref.strip() for ref in source_refs)
        and bool(source_refs)
        and isinstance(element_refs, list)
        and all(isinstance(ref, str) and ref.strip() for ref in element_refs)
        and bool(element_refs)
        and instance.get("binding_precise") is True
    )
