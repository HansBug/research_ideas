"""Method-local A1 projection; original artifacts remain audit-only."""

from copy import deepcopy
from typing import Any

from pydantic import BaseModel, Field

from ..inputs.context import prompt_context_payload as full_prompt_context_payload
from ..inputs.context import (
    CanonicalSourceIR, ContextManifest, ExactSourceInventory, NumberedNLSegment, StructuredArtifact,
)
from ..inputs.models import PairInput


NO_INSPECT_VERSION = "no-inspect-projection.v1"
INSPECTION_ROLES = frozenset({
    "reference_inspection_facts", "inspection_equivalent_facts", "verify_facts", "smt_facts",
})
DISABLED_INSPECTION_STEPS = (
    "frontier._materialize_root_reachability",
    "frontier._materialize_dead_ends",
    "frontier._materialize_cross_wrapper",
    "frontier._materialize_event_consumers",
    "frontier._materialize_inspection_diagnostics",
    "domain_invariants.materialize_domain_invariant_contracts",
    "runner._preflight_synthetic_root_wrapper_reachability",
    "runner._d_decision_consistency_errors.closed_model_dead_end",
    "runner._d_decision_consistency_errors.inspection_event_consumers",
)


class NoInspectInput(PairInput):
    """A1 consumers cannot obtain the four removed fact payloads from this view."""

    reference_inspection: None = Field(default=None, description="Reference checks disabled by the no-inspect condition.")
    inspection_facts: None = Field(default=None, description="Precomputed structural checks disabled by the no-inspect condition.")
    verify_facts: None = Field(default=None, description="Precomputed verification facts disabled by the no-inspect condition.")
    smt_facts: None = Field(default=None, description="Precomputed SMT context disabled by the no-inspect condition.")


NoInspectInput.model_rebuild()


def without_inspection(pair: PairInput) -> NoInspectInput:
    fields = {name: getattr(pair, name) for name in PairInput.model_fields}
    for name in ("reference_inspection", "inspection_facts", "verify_facts", "smt_facts"):
        fields[name] = None
    if pair.working_contract is not None:
        payload = deepcopy(pair.working_contract.payload)
        payload.pop("diagnostic_attribution", None)
        for key in ("diagnostic_binding_status", "diagnostic_record_count"):
            payload.get("summary", {}).pop(key, None)
        for key in ("inspect_diagnostics", "inspect_structure", "verification"):
            payload.get("capability_eligibility", {}).pop(key, None)
        for key in ("parse_inspect_file_sha256", "parse_inspect_path"):
            payload.get("artifact_bindings", {}).pop(key, None)
        fields["working_contract"] = pair.working_contract.model_copy(update={"payload": payload})
    if pair.case_report is not None:
        fields["case_report"] = pair.case_report.model_copy(update={"payload": {
            key: value for key, value in pair.case_report.payload.items()
            if key in {"case_id", "pair_index", "canonical_sha256", "fcstm_sha256",
                       "source_trace_sha256", "working_contract_sha256", "source_sha256"}
        }})
    return NoInspectInput(**fields)


def prompt_context_payload(pair: PairInput, *, stage: str) -> dict[str, Any]:
    payload = full_prompt_context_payload(pair, stage=stage)
    if getattr(pair, "ablation_mode", "none") == "no-predicates":
        from .no_predicates import project_context

        return project_context(payload)
    if not isinstance(pair, NoInspectInput):
        return payload
    for role in INSPECTION_ROLES:
        payload.pop(role, None)
        payload["source_roles"].pop(role, None)
    payload["input_hashes"].pop("parse_inspect", None)
    for ref in payload["artifact_refs"]:
        if ref["role"] in INSPECTION_ROLES:
            ref["prompt_included"] = False
    for section in payload["context_manifest"]["sections"]:
        section["artifact_roles"] = [role for role in section["artifact_roles"] if role not in INSPECTION_ROLES]
    case = payload.get("case_report")
    if case is not None:
        case["payload"].pop("artifact_status", None)
        case["reason"] = "Only source identity remains visible; validation results are disabled by ablation."
    if "fcstm_model" in payload:
        payload["fcstm_model"]["model_ir"]["inventory_projection"] = (
            "Stable model refs locate the raw syntax in fcstm_model.text; precomputed inspection rows are not supplied."
        )
    payload["ablation"] = {
        "mode": "no-inspect", "projection_version": NO_INSPECT_VERSION,
        "status": "disabled_by_ablation", "disabled_roles": sorted(INSPECTION_ROLES),
        "reason": "Precomputed checks are unavailable, not passed or refuted. Artifact hashes identify audit originals, not permission to consume them.",
    }
    return payload


# Exact edits to fixed method instructions, never replacements in source text,
# candidate prose, schema feedback, or other provider-generated content.
_INSPECTION_GUIDANCE = (
    ("; inspection-equivalent and verify/SMT summaries are deterministic facts only", ""),
    ("exact source/inspection facts", "exact source facts"),
    ("FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries", "FCSTM and owned ModelIR"),
    (", and inspection/verify/SMT rows are deterministic facts", ""),
    ("supplied structured source/inspection facts", "supplied structured source facts"),
    ("""Inspection-equivalent routing: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one V1(initial_scope) candidate,
for the exact `deadlock_freedom` operating-state contract and exact state locus,
with the exact leaf refs kept in element_refs/supporting facts; it is not an S1
existence claim. A failed finite reachability fact routes to G1 with its exact
source/target sets. A refuted initial-entry fact routes to an exact S2 initial
edge claim. A refuted event-consumer coverage fact may support a precise
predicate-null W1 candidate for the exact event/consumer scope; do not replace
consumer reachability with an event or transition existence claim. An unresolved
inspection fact remains unresolved. """, ""),
)


def system_prompt_for(prompt: str, *, ablation: str = "none") -> str:
    if ablation == "none":
        return prompt
    if ablation == "no-predicates":
        from .no_predicates import project_instruction

        return project_instruction(prompt)
    if ablation != "no-inspect":
        raise ValueError(f"No prompt implementation for ablation: {ablation}")
    for source, replacement in _INSPECTION_GUIDANCE:
        prompt = prompt.replace(source, replacement)
    return prompt


def pair_system_prompt(pair: PairInput, prompt: str) -> str:
    return system_prompt_for(prompt, ablation="no-inspect" if isinstance(pair, NoInspectInput) else getattr(pair, "ablation_mode", "none"))


def response_schema_for(schema: type[BaseModel], *, ablation: str = "none") -> type[BaseModel]:
    if ablation == "no-predicates":
        from .no_predicates import response_schema

        return response_schema(schema)
    if ablation not in {"none", "no-inspect"}:
        raise ValueError(f"No response schema implementation for ablation: {ablation}")
    return schema
