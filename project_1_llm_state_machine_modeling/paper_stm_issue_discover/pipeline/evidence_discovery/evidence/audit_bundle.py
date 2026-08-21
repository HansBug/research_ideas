from __future__ import annotations

import hashlib
import json
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..inputs.models import PairInput
from ..semantics.adjudication import SemanticAdjudication
from ..semantics.binding import BindingResult
from .receipts import RawReceipt


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
        "schema": "paper1.evidence_discovery.w2_audit_bundle.v1",
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
        "reason": reason,
        "basis": basis,
    }
    payload["audit_hash"] = "sha256:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()
    return payload
