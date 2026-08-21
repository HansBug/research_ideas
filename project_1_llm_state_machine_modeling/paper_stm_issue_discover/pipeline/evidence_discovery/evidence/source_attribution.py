from __future__ import annotations

from pathlib import Path
from typing import Any

from ..inputs.provenance import source_chain


def build_source_attribution(
    *,
    pair_id: str,
    obligation_id: str,
    nl_path: Path,
    model_path: Path,
    model_hash: str,
    plan_id: str | None,
    receipt_id: str | None,
) -> dict[str, Any]:
    attribution = source_chain(
        pair_id=pair_id,
        nl_path=nl_path,
        model_path=model_path,
        model_hash=model_hash,
        obligation_id=obligation_id,
        plan_id=plan_id,
        receipt_id=receipt_id,
    )
    attribution["roles"] = {
        "natural_language": "normative_source_contract",
        "plantuml": "author_source_localization",
        "canonical_source_ir": "author_source_identity_and_inventory",
        "fcstm": "closed_model_binding_and_execution",
        "inspection_facts": "deterministic_inventory_and_diagnostics_only",
        "verify_facts": "deterministic_verification_summary_only",
        "smt_facts": "normalized_formal_inputs_only",
    }
    attribution["reason"] = "Attribution keeps author source, closed model, and deterministic facts as separate authorities."
    attribution["basis"] = "source_chain.v1 plus evidence_discovery source-role policy"
    return attribution
