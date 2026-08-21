from __future__ import annotations

from typing import Any

from ..compiler.lowering import PredicatePlan
from ..semantics.adjudication import SemanticAdjudication, adjudicate_disposition
from ..semantics.binding import BindingResult
from ..semantics.obligations import CandidateIssue
from .audit_bundle import build_audit_bundle
from .receipts import RawReceipt


def calculate_witness_level(binding: BindingResult, plan: PredicatePlan, receipt: RawReceipt) -> str:
    if not binding.precise or not plan.binding_complete:
        return "W0"
    if not plan.supported:
        return "W1"
    if receipt.terminal_state == "completed" and receipt.verdict in {"true", "false"}:
        return "W2"
    # UNKNOWN, timeout, unsupported execution and errors are a third state:
    # they are not semantic W1 and can never become a violation or W2.
    return "UNKNOWN"


def build_evidence_record(
    *,
    pair: Any,
    obligation_id: str,
    candidate: CandidateIssue,
    binding: BindingResult,
    plan: PredicatePlan,
    receipt: RawReceipt,
    source_attribution: dict[str, Any],
    retry_records: list[dict[str, Any]],
    semantic_adjudication: SemanticAdjudication | None = None,
) -> dict[str, Any]:
    disposition = adjudicate_disposition(
        candidate,
        binding,
        semantic_adjudication,
        receipt=receipt,
    )
    witness_level = calculate_witness_level(binding, plan, receipt)
    issue_emitted = disposition["d_level"] in {"D1", "D2"}
    if witness_level == "W0":
        coverage_class = "coverage_gap"
    elif witness_level == "W1":
        coverage_class = "semantic_hit"
    elif witness_level == "UNKNOWN":
        coverage_class = "execution_unknown"
    else:
        coverage_class = "executable_evidence"
    record: dict[str, Any] = {
        "schema": "paper1.evidence_discovery.evidence_record.v1",
        "obligation_id": obligation_id,
        "predicate_id": plan.predicate_id,
        "binding": {
            "precise": binding.precise,
            "element_refs": list(binding.element_refs),
            "source_refs": list(binding.source_refs),
            "reason": binding.reason,
            "basis": binding.basis,
        },
        "plan": plan.to_dict(),
        "receipt": receipt.to_dict(),
        "witness_level": witness_level,
        "d_level": disposition["d_level"],
        "semantic_adjudication": disposition["semantic_adjudication"],
        "issue_emitted": bool(
            issue_emitted
            and (
                witness_level == "W1"
                or (witness_level == "W2" and receipt.verdict == "false")
            )
        ),
        "coverage_class": coverage_class,
        "reason": disposition["reason"],
        "basis": disposition["basis"],
        "retry_records": retry_records,
        "source_attribution": source_attribution,
    }
    if witness_level == "W2":
        record["audit_bundle"] = build_audit_bundle(
            pair=pair,
            obligation_id=obligation_id,
            binding=binding,
            plan=plan,
            receipt=receipt,
            source_attribution=source_attribution,
            reason=record["reason"],
            basis=record["basis"],
            retry_records=retry_records,
            semantic_adjudication=semantic_adjudication,
        )
    else:
        record["audit_bundle"] = None
    return record
