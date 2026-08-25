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

    This receipt is emitted for both finding and passing checks.  A source gate
    can keep a real execution at W1; it must not erase the backend result, and
    a passing result is never published as an issue.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema: Literal["evidence-discovery.predicate_execution_receipt.v1"] = Field(
        default="evidence-discovery.predicate_execution_receipt.v1",
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
    terminal_state: str = Field(min_length=1, description="Actual backend terminal state.")
    verdict: Literal["pass", "violation", "unsupported", "blocked"] = Field(description="Normalized execution verdict; it is not W, D, or L.")
    raw_verdict: str = Field(min_length=1, description="Backend-native verdict retained without normalization.")
    execution_status: Literal["executed", "unsupported", "blocked"] = Field(description="Whether a backend reached a terminal result.")
    source_audit_status: str | None = Field(default=None, description="Predicate source-catalog status at compilation.")
    source_gate_passed: bool = Field(description="Whether the source gate admitted W2 publication.")
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
) -> dict[str, Any]:
    """Normalize one compiled plan and RawReceipt into an immutable execution record."""

    typed_inputs = plan.inputs.model_dump(mode="json")
    typed_inputs_hash = _canonical_hash(typed_inputs)
    program = plan.formal_program
    program_hash = plan.formal_program_hash
    if receipt.terminal_state == "completed" and receipt.verdict == "true":
        verdict = "pass"
    elif receipt.terminal_state == "completed" and receipt.verdict == "false":
        verdict = "violation"
    elif receipt.terminal_state in {"unsupported", "error"} or receipt.backend == "none":
        verdict = "unsupported"
    else:
        verdict = "blocked"
    execution_status = (
        "executed" if verdict in {"pass", "violation"} else verdict
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
        "source_audit_status": plan.source_audit_status,
        "source_gate_passed": bool(plan.source_gate_passed),
        "backend_result": receipt.to_dict(),
        "reason": receipt.reason,
        "basis": (
            f"plan={plan.plan_id}; executable={bool(getattr(plan, 'executable', plan.supported))}; "
            f"source_gate_passed={bool(plan.source_gate_passed)}; {receipt.basis}"
        ),
        "receipt_hash": "sha256:" + "0" * 64,
    }
    normalized = PredicateExecutionReceipt.model_validate(payload).model_dump(mode="json")
    normalized.pop("receipt_hash", None)
    normalized["receipt_hash"] = _canonical_hash(normalized)
    return PredicateExecutionReceipt.model_validate(normalized).model_dump(mode="json")
