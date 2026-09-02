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
    requirement_quote: str | None = None,
    source_refs: list[str] | tuple[str, ...] | None = None,
    binding_element_refs: list[str] | tuple[str, ...] | None = None,
    binding_precise: bool | None = None,
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
    attribution["instance_authority"] = {
        "requirement_quote": requirement_quote,
        "source_refs": list(source_refs or ()),
        "binding_element_refs": list(binding_element_refs or ()),
        "binding_precise": binding_precise,
        "reason": "The requirement quote and source references authorize the concrete obligation; exact binding only resolves that authority on the closed current artifact.",
    }
    attribution["reason"] = "Attribution keeps author source, closed model, and deterministic facts as separate authorities."
    attribution["basis"] = "source_chain.v1 plus evidence_discovery source-role policy"
    return attribution
