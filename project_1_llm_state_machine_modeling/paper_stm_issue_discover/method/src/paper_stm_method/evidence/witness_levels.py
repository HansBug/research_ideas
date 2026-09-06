from __future__ import annotations

from typing import Any

from ..compiler.lowering import PredicatePlan
from ..semantics.adjudication import SemanticAdjudication, adjudicate_disposition
from ..semantics.binding import BindingResult
from ..semantics.obligations import CandidateIssue
from .audit_bundle import build_audit_bundle
from .receipts import RawReceipt, build_predicate_execution_receipt


def calculate_witness_level(binding: BindingResult, plan: PredicatePlan, receipt: RawReceipt) -> str:
    """Return the local preflight W ceiling when no receipt identity is available.

    This legacy helper cannot inspect the exact pair/obligation/model/program/
    receipt identity, normative quotation, source references, or polarity
    publication rule.  It therefore never upgrades a record to W2.  Callers
    that own the complete evidence chain must use
    :func:`build_predicate_execution_receipt` instead.
    """

    if not binding.precise:
        return "W0"
    return "W1"


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
    run_id: str = "00000000000000000000000000000000",
) -> dict[str, Any]:
    disposition = adjudicate_disposition(
        candidate,
        binding,
        semantic_adjudication,
        receipt=receipt,
    )
    independent_semantic_basis = bool(
        semantic_adjudication is not None
        and semantic_adjudication.grounding == "established"
    )
    execution_receipt = build_predicate_execution_receipt(
        pair_id=pair.pair_id,
        run_id=run_id,
        contract_id=candidate.contract_id,
        obligation_id=obligation_id,
        plan=plan,
        receipt=receipt,
        source_attribution=source_attribution,
        model_hash=pair.hashes["fcstm"],
        retry_records=retry_records,
        independent_semantic_basis=independent_semantic_basis,
        binding_precise=binding.precise,
    )
    witness_level = execution_receipt["witness_level"]
    # A failed or unavailable backend cannot manufacture a D1/D2 finding. A
    # separately established semantic adjudication may still support a W1
    # issue, but the failure itself remains only an execution-audit fact.
    if (
        binding.precise
        and
        execution_receipt["execution_state"] != "completed"
        and not independent_semantic_basis
    ):
        disposition = {
            **disposition,
            "d_level": "D0",
            "reason": disposition["reason"] + " The backend failure/absence is not independent violation evidence, so deterministic publication is D0.",
            "basis": disposition["basis"] + "; execution audit requires an independently established semantic basis before D1/D2 publication",
        }
    issue_emitted = disposition["d_level"] in {"D1", "D2"}
    if witness_level == "W0":
        coverage_class = "coverage_gap"
    elif witness_level == "W1":
        coverage_class = (
            "execution_degraded"
            if execution_receipt["execution_state"] != "not_attempted"
            else "semantic_hit"
        )
    else:
        coverage_class = "executable_evidence"
    record: dict[str, Any] = {
        "schema": "evidence-discovery.evidence_record.v1",
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
        "execution_receipt": execution_receipt,
        "witness_level": witness_level,
        "d_level": disposition["d_level"],
        "semantic_adjudication": disposition["semantic_adjudication"],
        "issue_emitted": bool(
            issue_emitted
            and (witness_level == "W1" or (witness_level == "W2" and receipt.verdict == "false"))
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
            execution_receipt=execution_receipt,
        )
    else:
        record["audit_bundle"] = None
    return record
