from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from typing import Any


SCHEMA_VERSION = "paper1.working_fcstm_contract.v2"


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _source_id(kind: str, value: str) -> str:
    return f"source:{kind}:{value}"


def _compiler_id(kind: str, value: str) -> str:
    return f"compiler:{kind}:{value}"


def _macro_id(kind: str, value: str) -> str:
    return f"macro:{kind}:{value}"


def _element(
    *,
    element_id: str,
    kind: str,
    origin: str,
    source_refs: list[str],
    model_refs: list[str],
    edit_policy: str,
    macro_ids: list[str] | None = None,
    field_ownership: dict[str, str] | None = None,
    semantic_fields: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "element_id": element_id,
        "kind": kind,
        "origin": origin,
        "source_refs": source_refs,
        "model_refs": model_refs,
        "edit_policy": edit_policy,
        "macro_ids": macro_ids or [],
        "field_ownership": field_ownership or {},
        "semantic_fields": semantic_fields or {},
        "metadata": metadata or {},
    }


def _source_trace_entry(
    *,
    trace_id: str,
    source_element_id: str,
    intermediate_ref: str,
    relation: str = "exact",
    evidence: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    normalized = relation == "normalized"
    return {
        "trace_id": trace_id,
        "trace_class": "source_semantic_identity",
        "trace_dimension": "identity_only",
        "source_elements": [source_element_id],
        "intermediate_elements": [intermediate_ref],
        "trace_relation": relation,
        "projection_status": "projectable",
        "required_for_issue_ids": [],
        "issue_binding_policy": "discover_must_confirm_source_issue",
        "behavioral_fidelity": "not_assessed",
        "attribution_boundary": {
            "source_level_claim_allowed": True,
            "conversion_or_lowering_related": False,
            "representation_related": False,
            "closure_claim_allowed": False,
            "rationale": (
                "This entry proves stable source identity only. Discover still needs NL/source/"
                "typed evidence, and closure remains disabled until the issue-bound C audit."
            ),
        },
        "trace_relation_rationale": (
            "Source-input normalization is hash-bound and explicitly recorded."
            if normalized
            else "Stable one-to-one source semantic identity; compiler members are internal."
        ),
        "trace_evidence": evidence or [],
        "reviewer_notes": (
            "Issue-agnostic identity trace; it is not behavior equivalence or closure evidence."
        ),
    }


def _boundary_trace_entry(
    *,
    trace_id: str,
    source_element_id: str,
    intermediate_ref: str,
    evidence: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "trace_class": "conversion_boundary",
        "trace_dimension": "identity_only",
        "source_elements": [source_element_id],
        "intermediate_elements": [intermediate_ref],
        "trace_relation": "conversion_artifact",
        "projection_status": "not_applicable",
        "required_for_issue_ids": [],
        "issue_binding_policy": "candidate_or_rejected_only",
        "behavioral_fidelity": "not_assessed",
        "attribution_boundary": {
            "source_level_claim_allowed": False,
            "conversion_or_lowering_related": True,
            "representation_related": True,
            "closure_claim_allowed": False,
            "rationale": (
                "Source-input normalization is an ingestion boundary, not a source behavioral "
                "issue and not repair-gain evidence."
            ),
        },
        "trace_relation_rationale": (
            "The raw and normalized text are hash-bound, but the normalization cannot support "
            "a source-level issue or closure claim."
        ),
        "trace_evidence": evidence,
        "reviewer_notes": "Discover must reject or exclude normalization-only propositions.",
    }


def _capability(
    *,
    status: str,
    eligible: list[str],
    excluded: list[str],
    reasons: list[str],
    claim_boundary: str,
) -> dict[str, Any]:
    return {
        "status": status,
        "eligible_element_ids": sorted(set(eligible)),
        "excluded_element_ids": sorted(set(excluded)),
        "eligible_field_refs": [],
        "excluded_field_refs": [],
        "reason_codes": sorted(set(reasons)),
        "evidence_refs": [],
        "claim_boundary": claim_boundary,
    }


def _field_ref(element_id: str, field_name: str) -> str:
    return f"{element_id}#field:{field_name}"


def _bind_capability_fields(
    *, capabilities: dict[str, dict[str, Any]], elements: list[dict[str, Any]]
) -> None:
    for capability in capabilities.values():
        eligible_elements = set(capability["eligible_element_ids"])
        eligible_fields: list[str] = []
        excluded_fields: list[str] = []
        for element in elements:
            for field_name, ownership in element["field_ownership"].items():
                ref = _field_ref(element["element_id"], field_name)
                if (
                    element["element_id"] in eligible_elements
                    and ownership == "source_owned"
                ):
                    eligible_fields.append(ref)
                else:
                    excluded_fields.append(ref)
        capability["eligible_field_refs"] = sorted(eligible_fields)
        capability["excluded_field_refs"] = sorted(excluded_fields)


def build_review_obligations(
    *,
    comparison: dict[str, Any],
    official_identity: dict[str, Any],
    contract: dict[str, Any],
) -> list[dict[str, Any]]:
    elements = {item["element_id"]: item for item in contract["elements"]}
    macros = {item["macro_id"]: item for item in contract["macros"]}
    source_state_by_fcstm_path = {
        item.get("metadata", {}).get("fcstm_path"): item["element_id"]
        for item in contract["elements"]
        if item.get("origin") == "source_owned" and item.get("kind") == "state"
    }
    root_source_state_ids = sorted(
        item["element_id"]
        for item in contract["elements"]
        if item.get("origin") == "source_owned"
        and item.get("kind") == "state"
        and item.get("metadata", {}).get("source_parent") is None
    )
    root_fcstm_paths = {
        item["metadata"]["fcstm_path"].rsplit(".", 1)[0]
        for item in contract["elements"]
        if item.get("origin") == "source_owned"
        and item.get("kind") == "state"
        and item.get("metadata", {}).get("source_parent") is None
    }
    obligations: list[dict[str, Any]] = []

    def add(
        risk_tag: str,
        occurrence_key: str,
        element_ids: list[str],
        source_refs: list[str | None],
        rationale: str,
    ) -> None:
        normalized = sorted(set(item for item in element_ids if item in elements))
        if not normalized:
            raise ValueError(
                f"review obligation lacks owned elements: {risk_tag}:{occurrence_key}"
            )
        bound_source_refs = {
            item for item in source_refs if item
        }
        for element_id in normalized:
            bound_source_refs.update(elements[element_id].get("source_refs", []))
        obligations.append(
            {
                "obligation_id": (
                    f"review:{risk_tag}:{len(obligations) + 1:04d}:{occurrence_key}"
                ),
                "risk_tag": risk_tag,
                "element_ids": normalized,
                "expected_origins": {
                    item: elements[item]["origin"] for item in normalized
                },
                "source_refs": sorted(bound_source_refs),
                "rationale": rationale,
            }
        )

    for index, item in enumerate(official_identity["state_identity_remaps"], start=1):
        add(
            "official_identity_remap",
            f"state-{index:03d}",
            [f"source:state:{item['after']}"],
            [item.get("raw_ref")],
            "Pinned PlantUML changed the provisional source state identity.",
        )
    for index, item in enumerate(
        official_identity["transition_endpoint_remaps"], start=1
    ):
        add(
            "official_identity_remap",
            f"transition-{index:03d}-{item['transition_id']}",
            [f"source:transition:{item['transition_id']}"],
            [item.get("raw_ref")],
            "Pinned PlantUML changed a provisional transition endpoint identity.",
        )
    for mapping in comparison["transition_mappings"]:
        transition_id = mapping["transition_id"]
        macro = macros[f"macro:transition:{transition_id}"]
        element_ids = [
            f"source:transition:{transition_id}",
            *macro["member_element_ids"],
        ]
        if len(mapping["emitted"]) > 1:
            add(
                "multi_segment_macro",
                transition_id,
                element_ids,
                [mapping.get("raw_ref")],
                "One source transition is lowered into multiple protected FCSTM members.",
            )
        if mapping["source_transition"].get("kind") == "final":
            add(
                "final_boundary",
                transition_id,
                element_ids,
                [mapping.get("raw_ref")],
                "A PlantUML final boundary is represented by an FCSTM termination macro.",
            )
    for index, item in enumerate(comparison["synthetic_state_mappings"], start=1):
        element_ids = [f"compiler:state:{item['fcstm_path']}"]
        transition_id = item.get("source_transition_id")
        if transition_id:
            element_ids.append(f"source:transition:{transition_id}")
        else:
            owner = source_state_by_fcstm_path.get(item.get("fcstm_parent_path"))
            if owner:
                element_ids.append(owner)
            elif item.get("fcstm_parent_path") in root_fcstm_paths:
                # A root-level missing initial is an absence fact. Bind its review
                # obligation to the complete set of declared top-level source states
                # so the reviewer inspects the actual PlantUML root scope.
                element_ids.extend(root_source_state_ids)
        add(
            "synthetic_state",
            f"{index:03d}-{item['fcstm_id']}",
            element_ids,
            [item.get("raw_ref")],
            "A protected FCSTM state was introduced only to preserve or fail-close source structure.",
        )
    for index, item in enumerate(comparison["lifecycle_mappings"], start=1):
        source_id = f"source:lifecycle:{item['state_id']}:{index}"
        element_ids = [source_id]
        element_ids.extend(
            member
            for macro_id in elements[source_id]["macro_ids"]
            for member in macros[macro_id]["member_element_ids"]
        )
        add(
            "lifecycle",
            f"{index:03d}-{item['state_id']}",
            element_ids,
            [item.get("raw_ref")],
            "A source lifecycle declaration is preserved by an abstract, non-execution FCSTM projection.",
        )
    for item in comparison["concurrent_region_mappings"]:
        add(
            "concurrent_region",
            item["id"],
            [f"source:region:{item['id']}"],
            [item.get("raw_ref")],
            "A PlantUML orthogonal region is preserved as source metadata without runtime equivalence.",
        )
    for index, item in enumerate(comparison["source_normalization_mappings"], start=1):
        add(
            "source_normalization",
            f"{index:03d}",
            [f"source:normalization:{index}"],
            [item.get("raw_ref")],
            "A transport-only source normalization is isolated in the conversion boundary.",
        )
    concurrency_codes = {
        "R45.DEBT.explicit_concurrency_pseudostate",
        "R45.DEBT.ambiguous_unlabeled_fanout",
        "R45.DEBT.multiple_initial_fanout",
    }
    concurrency_debts = [
        item
        for item in comparison["operational_debts"]
        if item["reason_code"] in concurrency_codes
    ]
    for index, item in enumerate(concurrency_debts, start=1):
        element_ids = [
            f"source:transition:{transition_id}"
            for transition_id in item.get("transition_ids", [])
        ]
        if item.get("transition_id"):
            element_ids.append(f"source:transition:{item['transition_id']}")
        state_id = item.get("state_id") or item.get("source")
        if state_id and f"source:state:{state_id}" in elements:
            element_ids.append(f"source:state:{state_id}")
        add(
            "explicit_concurrency",
            f"{index:03d}-{item['reason_code'].rsplit('.', 1)[-1]}",
            element_ids,
            [item.get("raw_ref"), *item.get("raw_refs", [])],
            "A source concurrency or fan-out occurrence is structurally visible but runtime-excluded.",
        )
    return obligations


def _unbound_diagnostic_attribution() -> dict[str, Any]:
    return {
        "schema_version": "paper1.inspect_diagnostic_attribution.v1",
        "binding_status": "unbound",
        "inspect_report_sha256": None,
        "records": [],
        "outcome_counts": {},
        "record_set_sha256": _sha256_json([]),
        "promotion_policy": "no_diagnostic_is_a_source_issue_without_typed_attribution",
    }


def _diagnostic_record(
    *,
    index: int,
    diagnostic: dict[str, Any],
    outcome: str,
    compiler_element_ids: list[str],
    source_element_ids: list[str],
    rationale: str,
) -> dict[str, Any]:
    return {
        "diagnostic_index": index,
        "diagnostic_sha256": _sha256_json(diagnostic),
        "severity": str(diagnostic.get("severity", "unknown")),
        "code": str(diagnostic.get("code", "UNKNOWN")),
        "message": str(diagnostic.get("message", "")),
        "fcstm_span": diagnostic.get("span"),
        "outcome": outcome,
        "compiler_element_ids": sorted(set(compiler_element_ids)),
        "source_element_ids": sorted(set(source_element_ids)),
        "promotion_ceiling": (
            "candidate_only"
            if outcome == "candidate_only_until_source_evidence"
            else "rejected_or_insufficient"
        ),
        "rationale": rationale,
    }


def _unique_compiler_line_owners(
    *,
    fcstm: str,
    contract: dict[str, Any],
) -> dict[int, list[str]]:
    """Map only unambiguous generated FCSTM lines to compiler-owned elements."""

    line_numbers_by_text: dict[str, list[int]] = {}
    for line_number, line in enumerate(fcstm.splitlines(), start=1):
        line_numbers_by_text.setdefault(line.strip(), []).append(line_number)

    element_ids_by_text: dict[str, list[str]] = {}
    for element in contract.get("elements", []):
        if element.get("origin") != "compiler_owned":
            continue
        emitted_line = element.get("metadata", {}).get("line")
        if isinstance(emitted_line, str) and emitted_line.strip():
            element_ids_by_text.setdefault(emitted_line.strip(), []).append(
                element["element_id"]
            )

    result: dict[int, list[str]] = {}
    for text, line_numbers in line_numbers_by_text.items():
        element_ids = element_ids_by_text.get(text, [])
        if len(line_numbers) == 1 and len(element_ids) == 1:
            result[line_numbers[0]] = element_ids
    return result


def bind_inspect_diagnostics(
    *,
    fcstm: str,
    inspect_report: dict[str, Any],
    contract: dict[str, Any],
) -> dict[str, Any]:
    """Bind inspect output without parsing diagnostic message strings.

    Only an unambiguous FCSTM span on a generated compiler line is attributed.
    Macro-member diagnostics remain candidate-only; all other diagnostics stay
    insufficient rather than being promoted to source issues.
    """

    bound = copy.deepcopy(contract)
    elements_by_id = {item["element_id"]: item for item in bound.get("elements", [])}
    macros_by_id = {item["macro_id"]: item for item in bound.get("macros", [])}
    line_owners = _unique_compiler_line_owners(fcstm=fcstm, contract=bound)
    records: list[dict[str, Any]] = []
    for index, diagnostic in enumerate(inspect_report.get("diagnostics", [])):
        span = diagnostic.get("span") or {}
        line_number = span.get("line")
        compiler_ids = line_owners.get(line_number, [])
        macro_ids = sorted(
            {
                macro_id
                for element_id in compiler_ids
                for macro_id in elements_by_id[element_id].get("macro_ids", [])
            }
        )
        source_ids = sorted(
            {
                source_id
                for macro_id in macro_ids
                for source_id in macros_by_id[macro_id]["source_element_ids"]
            }
        )
        if compiler_ids and source_ids:
            outcome = "candidate_only_until_source_evidence"
            rationale = (
                "The structured FCSTM span resolves to a compiler-owned macro member. "
                "The source macro root may be investigated, but the diagnostic cannot "
                "confirm a source issue."
            )
        elif compiler_ids:
            outcome = "rejected_conversion_artifact"
            rationale = (
                "The structured FCSTM span resolves only to a protected compiler-owned "
                "element and cannot support a source-level proposition."
            )
        else:
            outcome = "insufficient_evidence"
            rationale = (
                "No unique structured ownership binding exists for this FCSTM span; "
                "diagnostic message text is deliberately not parsed for attribution."
            )
        records.append(
            _diagnostic_record(
                index=index,
                diagnostic=diagnostic,
                outcome=outcome,
                compiler_element_ids=compiler_ids,
                source_element_ids=source_ids,
                rationale=rationale,
            )
        )

    outcome_counts = Counter(item["outcome"] for item in records)
    bound["diagnostic_attribution"] = {
        "schema_version": "paper1.inspect_diagnostic_attribution.v1",
        "binding_status": "bound",
        "inspect_report_sha256": _sha256_json(inspect_report),
        "records": records,
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "record_set_sha256": _sha256_json(records),
        "promotion_policy": "no_diagnostic_is_a_source_issue_without_typed_attribution",
    }
    all_ids = sorted(elements_by_id)
    bound["capability_eligibility"]["inspect_diagnostics"] = _capability(
        status="ineligible",
        eligible=[],
        excluded=all_ids,
        reasons=(
            sorted(outcome_counts)
            if records
            else ["inspect_report_contains_no_diagnostics"]
        ),
        claim_boundary=(
            "Inspect diagnostics are bound as rejected, candidate-only, or insufficient. "
            "None is typed source-issue evidence in the baseline contract."
        ),
    )
    _bind_capability_fields(
        capabilities=bound["capability_eligibility"],
        elements=bound["elements"],
    )
    bound["summary"]["diagnostic_binding_status"] = "bound"
    bound["summary"]["diagnostic_record_count"] = len(records)
    if (
        bound.get("usage_gate") == "audit_only"
        and bound["capability_eligibility"]["contract_integrity"]["status"]
        == "eligible"
        and bound["capability_eligibility"]["source_static_discovery"]["status"]
        in {"eligible", "eligible_with_exclusions"}
    ):
        bound["usage_gate"] = "discover_input_with_capability_mask"
        bound["artifact_role"] = "attribution_scoped_working_model"
    return bound


def build_working_contract(
    *,
    canonical: dict[str, Any],
    fcstm: str,
    comparison: dict[str, Any],
) -> dict[str, Any]:
    elements: list[dict[str, Any]] = []
    macros: list[dict[str, Any]] = []
    trace_entries: list[dict[str, Any]] = []
    boundary_trace_entries: list[dict[str, Any]] = []

    elements.append(
        _element(
            element_id=_compiler_id("root", comparison["example_id"]),
            kind="root_wrapper",
            origin="compiler_owned",
            source_refs=[],
            model_refs=[
                f"state:{comparison['state_mappings'][0]['fcstm_path'].split('.')[0]}"
                if comparison["state_mappings"]
                else "state:__root__"
            ],
            edit_policy="protected",
            metadata={"generated_reason": "fcstm_root_wrapper"},
        )
    )

    for mapping in comparison["state_mappings"]:
        element_id = _source_id("state", mapping["state_id"])
        model_ref = f"state:{mapping['fcstm_path']}"
        elements.append(
            _element(
                element_id=element_id,
                kind="state",
                origin="source_owned",
                source_refs=[mapping["raw_ref"]] if mapping.get("raw_ref") else [],
                model_refs=[model_ref],
                edit_policy="direct_issue_bound",
                field_ownership={
                    "identity": "source_owned",
                    "parent": "source_owned",
                    "kind": "source_owned",
                    "source_label": "source_owned",
                    "display_label": "compiler_owned",
                    "fcstm_identifier": "compiler_owned",
                },
                semantic_fields={
                    "identity": mapping["state_id"],
                    "parent": mapping.get("source_parent"),
                    "kind": mapping.get("source_kind"),
                    "source_label": mapping.get("source_label"),
                    "display_label": mapping.get("fcstm_display_name"),
                    "fcstm_identifier": mapping["fcstm_path"],
                },
                metadata={
                    "source_state_id": mapping["state_id"],
                    "source_parent": mapping.get("source_parent"),
                    "fcstm_path": mapping["fcstm_path"],
                },
            )
        )
        trace_entries.append(
            _source_trace_entry(
                trace_id=f"trace:state:{mapping['state_id']}",
                source_element_id=element_id,
                intermediate_ref=model_ref,
            )
        )

    transition_macro_ids: dict[str, str] = {}
    for mapping in comparison["transition_mappings"]:
        transition_id = mapping["transition_id"]
        source_element_id = _source_id("transition", transition_id)
        macro_id = _macro_id("transition", transition_id)
        transition_macro_ids[transition_id] = macro_id
        macro_ref = macro_id
        elements.append(
            _element(
                element_id=source_element_id,
                kind="transition_macro_root",
                origin="source_owned",
                source_refs=[mapping["raw_ref"]] if mapping.get("raw_ref") else [],
                model_refs=[macro_ref],
                edit_policy="macro_issue_bound",
                macro_ids=[macro_id],
                field_ownership={
                    "source_endpoint": "source_owned",
                    "target_endpoint": "source_owned",
                    "raw_label": "source_owned",
                    "event_interpretation": "compiler_owned",
                    "macro_expansion": "compiler_owned",
                },
                semantic_fields={
                    "source_endpoint": mapping["source"],
                    "target_endpoint": mapping["target"],
                    "raw_label": mapping["source_transition"].get("raw_label"),
                    "event_interpretation": mapping["source_transition"].get(
                        "raw_event"
                    ),
                    "macro_expansion": [
                        item["emitted_object_id"] for item in mapping["emitted"]
                    ],
                },
                metadata={
                    "transition_id": transition_id,
                    "mapping_reason": mapping["reason_code"],
                    "source": mapping["source"],
                    "target": mapping["target"],
                },
            )
        )
        member_ids: list[str] = []
        for emitted in mapping["emitted"]:
            member_id = _compiler_id("transition_segment", emitted["emitted_object_id"])
            member_ids.append(member_id)
            elements.append(
                _element(
                    element_id=member_id,
                    kind="transition_segment",
                    origin="compiler_owned",
                    source_refs=[mapping["raw_ref"]] if mapping.get("raw_ref") else [],
                    model_refs=[f"fcstm-transition:{emitted['emitted_object_id']}"],
                    edit_policy="protected",
                    macro_ids=[macro_id],
                    metadata={
                        "scope": emitted["scope"],
                        "line": emitted["line"],
                        "scope_line_occurrence": emitted["scope_line_occurrence"],
                        "generated_role": emitted["generated_role"],
                        "source_transition_id": transition_id,
                    },
                )
            )
        linked_synthetics = [
            item
            for item in comparison["synthetic_state_mappings"]
            if item.get("source_transition_id") == transition_id
        ]
        for item in linked_synthetics:
            member_ids.append(_compiler_id("state", item["fcstm_path"]))
        macros.append(
            {
                "macro_id": macro_id,
                "macro_kind": mapping["reason_code"],
                "source_element_ids": [source_element_id],
                "member_element_ids": sorted(member_ids),
                "rewrite_policy": "controller_regenerate_only",
                "member_digest": _sha256_json(sorted(member_ids)),
                "capability_effects": [],
            }
        )
        trace_entries.append(
            _source_trace_entry(
                trace_id=f"trace:transition:{transition_id}",
                source_element_id=source_element_id,
                intermediate_ref=macro_ref,
            )
        )

    for item in comparison["synthetic_state_mappings"]:
        element_id = _compiler_id("state", item["fcstm_path"])
        macro_ids = []
        if item.get("source_transition_id") in transition_macro_ids:
            macro_ids.append(transition_macro_ids[item["source_transition_id"]])
        elements.append(
            _element(
                element_id=element_id,
                kind="synthetic_state",
                origin="compiler_owned",
                source_refs=[item["raw_ref"]] if item.get("raw_ref") else [],
                model_refs=[f"state:{item['fcstm_path']}"],
                edit_policy="protected",
                macro_ids=macro_ids,
                metadata={
                    "generated_reason": item["generated_reason"],
                    "source_transition_id": item.get("source_transition_id"),
                },
            )
        )

    for item in comparison["synthetic_transition_mappings"]:
        element_id = _compiler_id("synthetic_transition", item["emitted_object_id"])
        elements.append(
            _element(
                element_id=element_id,
                kind="synthetic_transition",
                origin="compiler_owned",
                source_refs=[],
                model_refs=[f"fcstm-transition:{item['emitted_object_id']}"],
                edit_policy="protected",
                metadata={
                    "scope": item["scope"],
                    "line": item["line"],
                    "scope_line_occurrence": item["scope_line_occurrence"],
                    "generated_reason": item["generated_reason"],
                    "owner_state_id": item.get("owner_state_id"),
                },
            )
        )

    transitions_by_event: dict[str, list[dict[str, Any]]] = {}
    for transition in canonical["model"]["transitions"]:
        if transition.get("event"):
            transitions_by_event.setdefault(transition["event"], []).append(transition)
    for item in comparison["event_mappings"]:
        source_transitions = transitions_by_event.get(item["raw_label"], [])
        elements.append(
            _element(
                element_id=_compiler_id("event_projection", item["fcstm_path"]),
                kind="opaque_event_projection",
                origin="compiler_owned",
                source_refs=sorted(
                    {
                        entry["raw_ref"]
                        for entry in source_transitions
                        if entry.get("raw_ref")
                    }
                ),
                model_refs=[f"event:{item['fcstm_path']}"],
                edit_policy="protected",
                macro_ids=sorted(
                    {
                        transition_macro_ids[entry["id"]]
                        for entry in source_transitions
                        if entry["id"] in transition_macro_ids
                    }
                ),
                field_ownership={
                    "raw_label": "compiler_owned",
                    "event_semantics": "compiler_owned",
                    "fcstm_identifier": "compiler_owned",
                },
                semantic_fields={
                    "raw_label": item["raw_label"],
                    "event_semantics": "opaque_named_event_projection",
                    "fcstm_identifier": item["fcstm_path"],
                },
                metadata={"raw_label": item["raw_label"]},
            )
        )

    for index, item in enumerate(comparison["body_mappings"], start=1):
        element_id = _source_id("body", f"{item['state_id']}:{index}")
        macro_id = _macro_id("body_projection", f"{item['state_id']}:{index}")
        elements.append(
            _element(
                element_id=element_id,
                kind="state_body_text",
                origin="source_owned",
                source_refs=[item["raw_ref"]] if item.get("raw_ref") else [],
                model_refs=[macro_id],
                edit_policy="macro_issue_bound",
                macro_ids=[macro_id],
                field_ownership={
                    "text": "source_owned",
                    "display_encoding": "compiler_owned",
                },
                semantic_fields={
                    "text": item["text"],
                    "display_encoding": "state_display_metadata",
                },
                metadata={"state_id": item["state_id"], "text": item["text"]},
            )
        )
        macros.append(
            {
                "macro_id": macro_id,
                "macro_kind": "state_display_metadata",
                "source_element_ids": [element_id],
                "member_element_ids": [],
                "rewrite_policy": "controller_regenerate_only",
                "member_digest": _sha256_json([]),
                "capability_effects": ["non_executable_metadata"],
            }
        )
        trace_entries.append(
            _source_trace_entry(
                trace_id=f"trace:body:{item['state_id']}:{index}",
                source_element_id=element_id,
                intermediate_ref=macro_id,
            )
        )

    for index, item in enumerate(comparison["lifecycle_mappings"], start=1):
        element_id = _source_id("lifecycle", f"{item['state_id']}:{index}")
        macro_id = _macro_id("lifecycle_projection", f"{item['state_id']}:{index}")
        projection_id = _compiler_id(
            "lifecycle_action",
            f"{item['state_id']}:{index}:{item['fcstm_action_id']}",
        )
        elements.append(
            _element(
                element_id=element_id,
                kind="lifecycle_action",
                origin="source_owned",
                source_refs=[item["raw_ref"]] if item.get("raw_ref") else [],
                model_refs=[macro_id],
                edit_policy="macro_issue_bound",
                macro_ids=[macro_id],
                field_ownership={
                    "kind": "source_owned",
                    "text": "source_owned",
                    "execution": "compiler_owned",
                },
                semantic_fields={
                    "kind": item["kind"],
                    "text": item["text"],
                    "execution": "abstract_lifecycle_projection",
                },
                metadata={
                    "state_id": item["state_id"],
                    "text": item["text"],
                    "lifecycle_kind": item["kind"],
                },
            )
        )
        elements.append(
            _element(
                element_id=projection_id,
                kind="abstract_lifecycle_projection",
                origin="compiler_owned",
                source_refs=[item["raw_ref"]] if item.get("raw_ref") else [],
                model_refs=[f"action:{item['fcstm_action_id']}"],
                edit_policy="protected",
                macro_ids=[macro_id],
                metadata={"representation": item["representation"]},
            )
        )
        macros.append(
            {
                "macro_id": macro_id,
                "macro_kind": "abstract_lifecycle_projection",
                "source_element_ids": [element_id],
                "member_element_ids": [projection_id],
                "rewrite_policy": "controller_regenerate_only",
                "member_digest": _sha256_json([projection_id]),
                "capability_effects": ["abstract_action_not_execution_evidence"],
            }
        )
        trace_entries.append(
            _source_trace_entry(
                trace_id=f"trace:lifecycle:{item['state_id']}:{index}",
                source_element_id=element_id,
                intermediate_ref=macro_id,
            )
        )

    for item in comparison["concurrent_region_mappings"]:
        element_id = _source_id("region", item["id"])
        macro_id = _macro_id("region_projection", item["id"])
        region_source_refs = sorted(
            {
                *item.get("separator_before_raw_refs", []),
                *item.get("separator_after_raw_refs", []),
            }
        )
        elements.append(
            _element(
                element_id=element_id,
                kind="concurrent_region",
                origin="source_owned",
                source_refs=region_source_refs,
                model_refs=[macro_id],
                edit_policy="macro_issue_bound",
                macro_ids=[macro_id],
                field_ownership={
                    "owner_scope": "source_owned",
                    "region_index": "source_owned",
                    "execution": "compiler_owned",
                },
                semantic_fields={
                    "owner_scope": item.get("owner_scope"),
                    "region_index": item["region_index"],
                    "execution": "orthogonal_runtime_unsupported",
                },
                metadata={
                    "owner_scope": item.get("owner_scope"),
                    "region_index": item["region_index"],
                },
            )
        )
        macros.append(
            {
                "macro_id": macro_id,
                "macro_kind": "concurrent_region_metadata",
                "source_element_ids": [element_id],
                "member_element_ids": [],
                "rewrite_policy": "controller_regenerate_only",
                "member_digest": _sha256_json([]),
                "capability_effects": ["orthogonal_runtime_unsupported"],
            }
        )
        trace_entries.append(
            _source_trace_entry(
                trace_id=f"trace:region:{item['id']}",
                source_element_id=element_id,
                intermediate_ref=macro_id,
            )
        )

    for index, item in enumerate(comparison["source_normalization_mappings"], start=1):
        element_id = _source_id("normalization", str(index))
        macro_id = _macro_id("normalization", str(index))
        elements.append(
            _element(
                element_id=element_id,
                kind="source_normalization",
                origin="source_owned",
                source_refs=[item["raw_ref"]] if item.get("raw_ref") else [],
                model_refs=[macro_id],
                edit_policy="protected",
                macro_ids=[macro_id],
                field_ownership={
                    "before": "source_owned",
                    "after": "compiler_owned",
                    "rule_id": "compiler_owned",
                },
                semantic_fields={
                    "before": item["before"],
                    "after": item["after"],
                    "rule_id": item["rule_id"],
                },
                metadata={
                    "rule_id": item["rule_id"],
                    "before": item["before"],
                    "after": item["after"],
                },
            )
        )
        macros.append(
            {
                "macro_id": macro_id,
                "macro_kind": "source_input_normalization",
                "source_element_ids": [element_id],
                "member_element_ids": [],
                "rewrite_policy": "protected_input_normalization",
                "member_digest": _sha256_json([]),
                "capability_effects": ["normalization_requires_source_audit"],
            }
        )
        boundary_trace_entries.append(
            _boundary_trace_entry(
                trace_id=f"trace:normalization:{index}",
                source_element_id=element_id,
                intermediate_ref=macro_id,
                evidence=[
                    {
                        "evidence_type": "normalization_report",
                        "reference": item.get("raw_ref") or f"normalization:{index}",
                        "summary": f"{item['before']} -> {item['after']}",
                    }
                ],
            )
        )

    element_ids = {item["element_id"] for item in elements}
    source_ids = sorted(
        item["element_id"] for item in elements if item["origin"] == "source_owned"
    )
    compiler_ids = sorted(
        item["element_id"] for item in elements if item["origin"] == "compiler_owned"
    )
    source_semantic_ids = sorted(
        item["element_id"]
        for item in elements
        if item["origin"] == "source_owned" and item["kind"] != "source_normalization"
    )
    source_repairable_ids = sorted(
        item["element_id"]
        for item in elements
        if item["origin"] == "source_owned"
        and item["edit_policy"] in {"direct_issue_bound", "macro_issue_bound"}
        and item["source_refs"]
    )
    attribution_exclusions = sorted(
        item["element_id"]
        for item in elements
        if item["origin"] == "compiler_owned" or item["kind"] == "source_normalization"
    )
    debts = comparison["operational_debts"]
    debt_codes = sorted({item["reason_code"] for item in debts})
    blockers = comparison["blockers"]
    structure_ok = (
        comparison["structural_verdict"] == "structure_preserved" and not blockers
    )
    source_static_status = "eligible_with_exclusions" if structure_ok else "ineligible"
    simulation_status = "ineligible"
    capabilities = {
        "contract_integrity": _capability(
            status="eligible" if structure_ok else "ineligible",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=[item["reason_code"] for item in blockers],
            claim_boundary=(
                "Artifact-level contract validity proves trace/accounting integrity only; it "
                "authorizes no source semantic element."
            ),
        ),
        "parse": _capability(
            status="eligible" if structure_ok else "ineligible",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=[item["reason_code"] for item in blockers],
            claim_boundary=(
                "Artifact-level FCSTM parseability only; parse success authorizes no source "
                "semantic element or behavioral claim."
            ),
        ),
        "inspect_structure": _capability(
            status="eligible" if structure_ok else "ineligible",
            eligible=source_semantic_ids if structure_ok else [],
            excluded=attribution_exclusions,
            reasons=["compiler_owned_elements_excluded"],
            claim_boundary="Source structure may be inspected; compiler-owned diagnostics are not source issues.",
        ),
        "inspect_diagnostics": _capability(
            status="not_run",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=["inspect_diagnostic_attribution_not_bound"],
            claim_boundary=(
                "Diagnostics are unavailable until the inspect report is bound through "
                "structured FCSTM spans; message strings are never attribution evidence."
            ),
        ),
        "source_static_discovery": _capability(
            status=source_static_status,
            eligible=source_semantic_ids if structure_ok else [],
            excluded=attribution_exclusions,
            reasons=debt_codes + ["runtime_debts_do_not_block_source_static_analysis"],
            claim_boundary=(
                "Static Discover may inspect every positively traced source semantic root. "
                "Operational debt limits behavioral evidence, not source-text analysis."
            ),
        ),
        "simulation": _capability(
            status=simulation_status,
            eligible=[],
            excluded=sorted(element_ids),
            reasons=debt_codes
            + [
                "runtime_has_no_stable_fired_transition_id",
                "runtime_path_taint_not_computable",
            ],
            claim_boundary=(
                "Baseline simulation is not attribution evidence: runtime history lacks "
                "stable fired-transition IDs, so a state observation cannot prove that its "
                "path avoided compiler macros or unsupported source semantics."
            ),
        ),
        "transition_trace": _capability(
            status="ineligible",
            eligible=[],
            excluded=source_ids + compiler_ids,
            reasons=["runtime_has_no_stable_fired_transition_id"],
            claim_boundary="State observations cannot be promoted to transition-level attribution.",
        ),
        "repair": _capability(
            status="not_run",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=["confirmed_source_issue_binding_required"],
            claim_boundary=(
                "This baseline lists potential source targets but authorizes no edit. Repair "
                "eligibility is created only by a separately validated confirmed issue binding."
            ),
        ),
        "confirm": _capability(
            status="not_run",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=["repair_disposition_and_confirm_adapter_not_implemented"],
            claim_boundary=(
                "No Repair disposition may be accepted or promoted to closure until the "
                "future Confirm adapter validates issue, patch, source evidence, and regression "
                "bindings."
            ),
        ),
        "final_export": _capability(
            status="not_run",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=["final_export_not_implemented"],
            claim_boundary=(
                "The future canonical PlantUML exporter will consume semantic roots and "
                "collapse compiler members, but this baseline implements and authorizes no "
                "final export."
            ),
        ),
        "main_result": _capability(
            status="not_run",
            eligible=[],
            excluded=sorted(element_ids),
            reasons=["discover_repair_confirm_not_run"],
            claim_boundary="Main-result eligibility is owned by the post-loop experiment gate.",
        ),
    }
    _bind_capability_fields(capabilities=capabilities, elements=elements)

    source_sha256 = canonical.get("metadata", {}).get("source_sha256")
    source_trace = {
        "schema_version": "source_trace_base.v1",
        "trace_scope": "formal_experiment_candidate",
        "relation_policy": "attribution_safe_macro_roots.v1",
        "entries": trace_entries,
        "boundary_entries": boundary_trace_entries,
        "attribution_exclusions": attribution_exclusions,
        "source_traceability": {
            "source_stm0_sha256": source_sha256,
            "fcstm_sha256": _sha256_text(fcstm),
            "closure_claim_allowed": False,
            "attribution": "source_macro_roots_only_compiler_members_excluded",
        },
        "notes": (
            "Issue-agnostic identity trace. Compiler-owned members and source-input "
            "normalizations are explicit attribution exclusions; no entry proves behavior "
            "equivalence or closure."
        ),
    }
    origin_counts = Counter(item["origin"] for item in elements)
    contract = {
        "schema_version": SCHEMA_VERSION,
        "example_id": canonical["example_id"],
        "artifact_role": "structural_projection",
        "usage_gate": "audit_only",
        "input_identity": {
            "source_sha256": source_sha256,
            "canonical_semantic_sha256": _sha256_json(canonical),
            "fcstm_sha256": _sha256_text(fcstm),
        },
        "ownership_policy": {
            "policy_id": "paper1.forward_attribution.v1",
            "origins": ["source_owned", "compiler_owned", "agent_created"],
            "agent_edit_policy": "source_semantic_patch_only.v1",
            "compiler_member_policy": "protected_controller_regeneration_only",
        },
        "attribution_policy": {
            "policy_id": "paper1.discover_attribution.v1",
            "compiler_only_diagnostic": "rejected_conversion_artifact",
            "macro_member_diagnostic": "candidate_only_until_source_evidence",
            "unresolved_diagnostic": "insufficient_evidence",
            "candidate_conversion_artifact_policy": (
                "allowed_only_as_explicitly_classified_non_repairable_noise"
            ),
            "source_internal_consistency_check_policy": (
                "manifest_bound_executed_checker_artifact_required"
            ),
            "confirmed_issue_requirements": [
                "nl_or_raw_internal_evidence",
                "raw_source_fragment",
                "positive_source_identity_trace",
                "capability_eligible_typed_evidence",
                "conversion_or_lowering_related_false",
            ],
            "repair_target_policy": "source_or_issue_bound_agent_root_only",
            "confirmed_issue_conversion_artifact_limit": 0,
            "repair_target_conversion_artifact_limit": 0,
            "confirm_accepted_conversion_artifact_limit": 0,
            "main_result_conversion_artifact_limit": 0,
        },
        "diagnostic_attribution": _unbound_diagnostic_attribution(),
        "repair_gate": {
            "status": "awaiting_confirmed_issue",
            "potential_source_target_ids": source_repairable_ids,
            "confirmed_issue_bindings": [],
            "required_issue_fields": [
                "issue_id",
                "source_element_ids",
                "raw_source_evidence",
                "positive_identity_trace_ids",
                "typed_evidence_refs",
                "conversion_or_lowering_related_false",
            ],
            "field_patch_validator": "required_not_implemented_in_baseline",
        },
        "confirm_gate": {
            "status": "not_run",
            "accepted_disposition_bindings": [],
            "required_disposition_fields": [
                "issue_id",
                "disposition_id",
                "source_element_ids",
                "pre_model_sha256",
                "post_model_sha256",
                "typed_confirmation_evidence_refs",
                "regression_audit_ref",
                "conversion_or_lowering_related_false",
            ],
            "accepted_conversion_artifact_limit": 0,
            "disposition_validator": "required_not_implemented_in_baseline",
        },
        "elements": elements,
        "macros": macros,
        "capability_eligibility": capabilities,
        "source_trace_base": source_trace,
        "summary": {
            "element_count": len(elements),
            "origin_counts": dict(sorted(origin_counts.items())),
            "macro_count": len(macros),
            "positive_trace_count": len(trace_entries),
            "boundary_trace_count": len(boundary_trace_entries),
            "compiler_owned_count": len(compiler_ids),
            "agent_created_count": origin_counts.get("agent_created", 0),
            "protected_element_count": sum(
                item["edit_policy"] == "protected" for item in elements
            ),
            "source_static_discovery_status": source_static_status,
            "simulation_status": simulation_status,
            "diagnostic_binding_status": "unbound",
            "diagnostic_record_count": 0,
        },
        "inventory_digests": {
            "element_set_sha256": _sha256_json(elements),
            "macro_set_sha256": _sha256_json(macros),
            "source_trace_set_sha256": _sha256_json(trace_entries),
            "boundary_trace_set_sha256": _sha256_json(boundary_trace_entries),
            "compiler_owned_set_sha256": _sha256_json(compiler_ids),
        },
    }
    validate_working_contract(
        canonical=canonical,
        fcstm=fcstm,
        comparison=comparison,
        contract=contract,
    )
    return contract


def validate_working_contract(
    *,
    canonical: dict[str, Any],
    fcstm: str,
    comparison: dict[str, Any],
    contract: dict[str, Any],
    inspect_report: dict[str, Any] | None = None,
) -> None:
    if contract.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("working contract schema version mismatch")
    if contract.get("example_id") != canonical.get("example_id"):
        raise ValueError("working contract example identity mismatch")
    identity = contract.get("input_identity", {})
    if identity.get("canonical_semantic_sha256") != _sha256_json(canonical):
        raise ValueError("working contract canonical hash mismatch")
    if identity.get("fcstm_sha256") != _sha256_text(fcstm):
        raise ValueError("working contract FCSTM hash mismatch")

    elements = contract.get("elements", [])
    element_ids = [item.get("element_id") for item in elements]
    if len(element_ids) != len(set(element_ids)) or None in element_ids:
        raise ValueError("working contract element IDs are not unique")
    elements_by_id = {item["element_id"]: item for item in elements}
    if any(
        item.get("origin") == "compiler_owned"
        and item.get("edit_policy") != "protected"
        for item in elements
    ):
        raise ValueError("compiler-owned element is not protected")
    if any(item.get("origin") == "agent_created" for item in elements):
        raise ValueError(
            "baseline working contract cannot contain agent-created elements"
        )
    expected_field_contracts: dict[str, tuple[dict[str, str], dict[str, Any]]] = {
        element_id: ({}, {}) for element_id in elements_by_id
    }
    for mapping in comparison["state_mappings"]:
        expected_field_contracts[_source_id("state", mapping["state_id"])] = (
            {
                "identity": "source_owned",
                "parent": "source_owned",
                "kind": "source_owned",
                "source_label": "source_owned",
                "display_label": "compiler_owned",
                "fcstm_identifier": "compiler_owned",
            },
            {
                "identity": mapping["state_id"],
                "parent": mapping.get("source_parent"),
                "kind": mapping.get("source_kind"),
                "source_label": mapping.get("source_label"),
                "display_label": mapping.get("fcstm_display_name"),
                "fcstm_identifier": mapping["fcstm_path"],
            },
        )
    for mapping in comparison["transition_mappings"]:
        expected_field_contracts[_source_id("transition", mapping["transition_id"])] = (
            {
                "source_endpoint": "source_owned",
                "target_endpoint": "source_owned",
                "raw_label": "source_owned",
                "event_interpretation": "compiler_owned",
                "macro_expansion": "compiler_owned",
            },
            {
                "source_endpoint": mapping["source"],
                "target_endpoint": mapping["target"],
                "raw_label": mapping["source_transition"].get("raw_label"),
                "event_interpretation": mapping["source_transition"].get("raw_event"),
                "macro_expansion": [
                    item["emitted_object_id"] for item in mapping["emitted"]
                ],
            },
        )
    for item in comparison["event_mappings"]:
        expected_field_contracts[
            _compiler_id("event_projection", item["fcstm_path"])
        ] = (
            {
                "raw_label": "compiler_owned",
                "event_semantics": "compiler_owned",
                "fcstm_identifier": "compiler_owned",
            },
            {
                "raw_label": item["raw_label"],
                "event_semantics": "opaque_named_event_projection",
                "fcstm_identifier": item["fcstm_path"],
            },
        )
    for index, item in enumerate(comparison["body_mappings"], start=1):
        expected_field_contracts[_source_id("body", f"{item['state_id']}:{index}")] = (
            {"text": "source_owned", "display_encoding": "compiler_owned"},
            {
                "text": item["text"],
                "display_encoding": "state_display_metadata",
            },
        )
    for index, item in enumerate(comparison["lifecycle_mappings"], start=1):
        expected_field_contracts[
            _source_id("lifecycle", f"{item['state_id']}:{index}")
        ] = (
            {
                "kind": "source_owned",
                "text": "source_owned",
                "execution": "compiler_owned",
            },
            {
                "kind": item["kind"],
                "text": item["text"],
                "execution": "abstract_lifecycle_projection",
            },
        )
    for item in comparison["concurrent_region_mappings"]:
        expected_field_contracts[_source_id("region", item["id"])] = (
            {
                "owner_scope": "source_owned",
                "region_index": "source_owned",
                "execution": "compiler_owned",
            },
            {
                "owner_scope": item.get("owner_scope"),
                "region_index": item["region_index"],
                "execution": "orthogonal_runtime_unsupported",
            },
        )
    for index, item in enumerate(comparison["source_normalization_mappings"], start=1):
        expected_field_contracts[_source_id("normalization", str(index))] = (
            {
                "before": "source_owned",
                "after": "compiler_owned",
                "rule_id": "compiler_owned",
            },
            {
                "before": item["before"],
                "after": item["after"],
                "rule_id": item["rule_id"],
            },
        )
    for element_id, (
        expected_ownership,
        expected_fields,
    ) in expected_field_contracts.items():
        element = elements_by_id[element_id]
        if element.get("field_ownership") != expected_ownership:
            raise ValueError(f"field ownership drift: {element_id}")
        if element.get("semantic_fields") != expected_fields:
            raise ValueError(f"semantic field value drift: {element_id}")

    source_state_ids = {
        _source_id("state", item["state_id"]) for item in comparison["state_mappings"]
    }
    actual_source_states = {
        item["element_id"]
        for item in elements
        if item.get("origin") == "source_owned" and item.get("kind") == "state"
    }
    if actual_source_states != source_state_ids:
        raise ValueError("source state ownership inventory drift")
    expected_synthetic_states = {
        _compiler_id("state", item["fcstm_path"])
        for item in comparison["synthetic_state_mappings"]
    }
    if not expected_synthetic_states.issubset(elements_by_id):
        raise ValueError("synthetic state ownership inventory is incomplete")

    macros = contract.get("macros", [])
    macro_ids = [item.get("macro_id") for item in macros]
    if len(macro_ids) != len(set(macro_ids)) or None in macro_ids:
        raise ValueError("working contract macro IDs are not unique")
    macros_by_id = {item["macro_id"]: item for item in macros}
    expected_macro_ids = {
        macro_id for item in elements for macro_id in item.get("macro_ids", [])
    }
    if set(macros_by_id) != expected_macro_ids:
        raise ValueError("working contract macro inventory drift")
    expected_transition_macros = {
        _macro_id("transition", item["transition_id"])
        for item in comparison["transition_mappings"]
    }
    if not expected_transition_macros.issubset(macros_by_id):
        raise ValueError("transition macro inventory is incomplete")
    for mapping in comparison["transition_mappings"]:
        macro_id = _macro_id("transition", mapping["transition_id"])
        macro = macros_by_id[macro_id]
        source_element_id = _source_id("transition", mapping["transition_id"])
        if macro.get("source_element_ids") != [source_element_id]:
            raise ValueError(
                f"transition macro source binding drift: {mapping['transition_id']}"
            )
        if elements_by_id[source_element_id].get("macro_ids") != [macro_id]:
            raise ValueError(
                f"transition source macro binding drift: {mapping['transition_id']}"
            )
        expected_members = {
            _compiler_id("transition_segment", item["emitted_object_id"])
            for item in mapping["emitted"]
        }
        expected_members.update(
            _compiler_id("state", item["fcstm_path"])
            for item in comparison["synthetic_state_mappings"]
            if item.get("source_transition_id") == mapping["transition_id"]
        )
        if set(macro["member_element_ids"]) != expected_members:
            raise ValueError(
                f"transition macro member drift: {mapping['transition_id']}"
            )
        if macro["member_digest"] != _sha256_json(sorted(expected_members)):
            raise ValueError(
                f"transition macro digest drift: {mapping['transition_id']}"
            )
        if any(
            elements_by_id[item]["origin"] != "compiler_owned"
            for item in expected_members
        ):
            raise ValueError(
                f"transition macro contains non-compiler member: {mapping['transition_id']}"
            )
        for emitted in mapping["emitted"]:
            member_id = _compiler_id(
                "transition_segment", emitted["emitted_object_id"]
            )
            if elements_by_id[member_id].get("metadata", {}).get(
                "scope_line_occurrence"
            ) != emitted.get("scope_line_occurrence"):
                raise ValueError(
                    f"transition occurrence binding drift: {emitted['emitted_object_id']}"
                )
    for item in comparison["synthetic_transition_mappings"]:
        element_id = _compiler_id("synthetic_transition", item["emitted_object_id"])
        if elements_by_id[element_id].get("metadata", {}).get(
            "scope_line_occurrence"
        ) != item.get("scope_line_occurrence"):
            raise ValueError(
                f"synthetic transition occurrence binding drift: {item['emitted_object_id']}"
            )
    for macro_id, macro in macros_by_id.items():
        expected_sources = sorted(
            item["element_id"]
            for item in elements
            if item.get("origin") == "source_owned"
            and macro_id in item.get("macro_ids", [])
        )
        if macro.get("source_element_ids") != expected_sources:
            raise ValueError(f"macro source binding drift: {macro_id}")
        members = macro.get("member_element_ids", [])
        if len(members) != len(set(members)) or any(
            item not in elements_by_id
            or elements_by_id[item].get("origin") != "compiler_owned"
            for item in members
        ):
            raise ValueError(f"macro compiler member inventory drift: {macro_id}")
        if macro.get("member_digest") != _sha256_json(sorted(members)):
            raise ValueError(f"macro member digest drift: {macro_id}")

    trace = contract.get("source_trace_base", {})
    if trace.get("source_traceability", {}).get("fcstm_sha256") != _sha256_text(fcstm):
        raise ValueError("source trace FCSTM binding mismatch")
    trace_entries = trace.get("entries", [])
    trace_ids = [entry.get("trace_id") for entry in trace_entries]
    if len(trace_ids) != len(set(trace_ids)) or None in trace_ids:
        raise ValueError("positive source trace IDs are not unique")
    traced_source_ids: list[str] = []
    for entry in trace_entries:
        source_elements = entry.get("source_elements", [])
        intermediate_elements = entry.get("intermediate_elements", [])
        if len(source_elements) != 1 or len(intermediate_elements) != 1:
            raise ValueError(
                "positive source trace must be one-to-one at semantic root level"
            )
        source_element = elements_by_id.get(source_elements[0])
        if source_element is None or source_element.get("origin") != "source_owned":
            raise ValueError("positive source trace binds a non-source-owned element")
        traced_source_ids.extend(source_elements)
        if intermediate_elements != source_element.get("model_refs"):
            raise ValueError("positive source trace target drift")
        if intermediate_elements[0].startswith("compiler:"):
            raise ValueError("positive source trace exposes compiler-owned member")
        if entry.get("trace_class") != "source_semantic_identity":
            raise ValueError("positive source trace has the wrong trace class")
        if entry.get("trace_dimension") != "identity_only":
            raise ValueError("positive source trace overclaims beyond identity")
        if entry.get("behavioral_fidelity") != "not_assessed":
            raise ValueError("baseline source trace cannot claim behavioral fidelity")
        boundary = entry.get("attribution_boundary", {})
        if not boundary.get("source_level_claim_allowed") or boundary.get(
            "conversion_or_lowering_related"
        ):
            raise ValueError("positive source trace attribution boundary is unsafe")
        if boundary.get("closure_claim_allowed"):
            raise ValueError("baseline identity trace cannot allow closure claims")
    expected_positive_source_ids = sorted(
        item["element_id"]
        for item in elements
        if item.get("origin") == "source_owned"
        and item.get("kind") != "source_normalization"
    )
    if sorted(traced_source_ids) != expected_positive_source_ids:
        raise ValueError("positive source trace coverage drift")
    boundary_entries = trace.get("boundary_entries", [])
    expected_boundary_sources = {
        item["element_id"]
        for item in elements
        if item.get("kind") == "source_normalization"
    }
    actual_boundary_sources: set[str] = set()
    for entry in boundary_entries:
        if entry.get("trace_class") != "conversion_boundary":
            raise ValueError("conversion boundary trace has the wrong trace class")
        source_elements = entry.get("source_elements", [])
        if len(source_elements) != 1:
            raise ValueError(
                "conversion boundary trace must bind one normalization element"
            )
        actual_boundary_sources.add(source_elements[0])
        boundary = entry.get("attribution_boundary", {})
        if boundary.get("source_level_claim_allowed"):
            raise ValueError("conversion boundary trace allows a source-level claim")
        if not boundary.get("conversion_or_lowering_related"):
            raise ValueError(
                "conversion boundary trace is not marked conversion-related"
            )
        if boundary.get("closure_claim_allowed"):
            raise ValueError("conversion boundary trace allows a closure claim")
    if actual_boundary_sources != expected_boundary_sources:
        raise ValueError("source normalization boundary trace inventory drift")
    exclusions = set(trace.get("attribution_exclusions", []))
    expected_exclusions = {
        item["element_id"]
        for item in elements
        if item.get("origin") == "compiler_owned"
        or item.get("kind") == "source_normalization"
    }
    if exclusions != expected_exclusions:
        raise ValueError("attribution exclusion inventory drift")

    all_element_ids = set(elements_by_id)
    diagnostic_attribution = contract.get("diagnostic_attribution", {})
    binding_status = diagnostic_attribution.get("binding_status")
    records = diagnostic_attribution.get("records", [])
    if binding_status not in {"unbound", "bound"}:
        raise ValueError("inspect diagnostic attribution binding status is invalid")
    if diagnostic_attribution.get("promotion_policy") != (
        "no_diagnostic_is_a_source_issue_without_typed_attribution"
    ):
        raise ValueError("inspect diagnostic promotion policy drift")
    if diagnostic_attribution.get("record_set_sha256") != _sha256_json(records):
        raise ValueError("inspect diagnostic attribution digest drift")
    outcome_counts = Counter(item.get("outcome") for item in records)
    if diagnostic_attribution.get("outcome_counts") != dict(
        sorted(outcome_counts.items())
    ):
        raise ValueError("inspect diagnostic attribution outcome count drift")
    allowed_outcomes = {
        "rejected_conversion_artifact",
        "candidate_only_until_source_evidence",
        "insufficient_evidence",
    }
    if not set(outcome_counts).issubset(allowed_outcomes):
        raise ValueError(
            "inspect diagnostic attribution promotes an unsupported outcome"
        )
    for index, record in enumerate(records):
        if record.get("diagnostic_index") != index:
            raise ValueError("inspect diagnostic attribution index drift")
        compiler_elements = set(record.get("compiler_element_ids", []))
        source_elements = set(record.get("source_element_ids", []))
        if not compiler_elements.issubset(all_element_ids) or any(
            elements_by_id[item].get("origin") != "compiler_owned"
            for item in compiler_elements
        ):
            raise ValueError("inspect diagnostic attribution has non-compiler members")
        if not source_elements.issubset(all_element_ids) or any(
            elements_by_id[item].get("origin") != "source_owned"
            for item in source_elements
        ):
            raise ValueError("inspect diagnostic attribution has non-source roots")
        if record.get("outcome") == "candidate_only_until_source_evidence":
            if not compiler_elements or not source_elements:
                raise ValueError(
                    "macro diagnostic candidate lacks both ownership sides"
                )
            if record.get("promotion_ceiling") != "candidate_only":
                raise ValueError(
                    "macro diagnostic candidate exceeds its promotion ceiling"
                )
        elif record.get("promotion_ceiling") != "rejected_or_insufficient":
            raise ValueError("non-candidate diagnostic has an unsafe promotion ceiling")
    if binding_status == "unbound":
        if records or diagnostic_attribution.get("inspect_report_sha256") is not None:
            raise ValueError("unbound inspect diagnostics contain bound evidence")
    else:
        if inspect_report is None:
            raise ValueError("bound inspect diagnostics require the inspect report")
        if diagnostic_attribution.get("inspect_report_sha256") != _sha256_json(
            inspect_report
        ):
            raise ValueError("inspect diagnostic report hash mismatch")
        diagnostics = inspect_report.get("diagnostics", [])
        if len(records) != len(diagnostics):
            raise ValueError("inspect diagnostic attribution coverage drift")
        for record, diagnostic in zip(records, diagnostics):
            if record.get("diagnostic_sha256") != _sha256_json(diagnostic):
                raise ValueError("inspect diagnostic attribution record hash drift")

    expected_repair_targets = {
        item["element_id"]
        for item in elements
        if item.get("origin") == "source_owned"
        and item.get("edit_policy") in {"direct_issue_bound", "macro_issue_bound"}
    }
    repair_gate = contract.get("repair_gate", {})
    if repair_gate.get("status") != "awaiting_confirmed_issue":
        raise ValueError("baseline repair gate is not awaiting a confirmed issue")
    if set(repair_gate.get("potential_source_target_ids", [])) != (
        expected_repair_targets
    ):
        raise ValueError("potential repair target inventory drift")
    if repair_gate.get("confirmed_issue_bindings"):
        raise ValueError("baseline repair gate contains confirmed issue bindings")
    if repair_gate.get("field_patch_validator") != (
        "required_not_implemented_in_baseline"
    ):
        raise ValueError("baseline repair field-patch gate drift")
    confirm_gate = contract.get("confirm_gate", {})
    if confirm_gate != {
        "status": "not_run",
        "accepted_disposition_bindings": [],
        "required_disposition_fields": [
            "issue_id",
            "disposition_id",
            "source_element_ids",
            "pre_model_sha256",
            "post_model_sha256",
            "typed_confirmation_evidence_refs",
            "regression_audit_ref",
            "conversion_or_lowering_related_false",
        ],
        "accepted_conversion_artifact_limit": 0,
        "disposition_validator": "required_not_implemented_in_baseline",
    }:
        raise ValueError("baseline confirm gate drift")

    origin_counts = Counter(item["origin"] for item in elements)
    summary = contract.get("summary", {})
    if summary.get("element_count") != len(elements):
        raise ValueError("working contract element count drift")
    if summary.get("origin_counts") != dict(sorted(origin_counts.items())):
        raise ValueError("working contract origin count drift")
    if summary.get("agent_created_count") != 0:
        raise ValueError("baseline agent-created count must be zero")
    if summary.get("positive_trace_count") != len(trace.get("entries", [])):
        raise ValueError("positive source trace count drift")
    if summary.get("boundary_trace_count") != len(boundary_entries):
        raise ValueError("conversion boundary trace count drift")
    if summary.get("diagnostic_binding_status") != binding_status:
        raise ValueError("inspect diagnostic binding summary drift")
    if summary.get("diagnostic_record_count") != len(records):
        raise ValueError("inspect diagnostic count summary drift")
    digests = contract.get("inventory_digests", {})
    if digests.get("element_set_sha256") != _sha256_json(elements):
        raise ValueError("working contract element digest drift")
    if digests.get("macro_set_sha256") != _sha256_json(macros):
        raise ValueError("working contract macro digest drift")
    compiler_ids = sorted(
        item["element_id"] for item in elements if item["origin"] == "compiler_owned"
    )
    if digests.get("compiler_owned_set_sha256") != _sha256_json(compiler_ids):
        raise ValueError("working contract compiler-owned digest drift")
    if digests.get("source_trace_set_sha256") != _sha256_json(trace.get("entries", [])):
        raise ValueError("positive source trace digest drift")
    if digests.get("boundary_trace_set_sha256") != _sha256_json(boundary_entries):
        raise ValueError("conversion boundary trace digest drift")
    capabilities = contract.get("capability_eligibility", {})
    allowed_status = {"eligible", "eligible_with_exclusions", "ineligible", "not_run"}
    if set(capabilities) != {
        "contract_integrity",
        "parse",
        "inspect_structure",
        "inspect_diagnostics",
        "source_static_discovery",
        "simulation",
        "transition_trace",
        "repair",
        "confirm",
        "final_export",
        "main_result",
    }:
        raise ValueError("working contract capability inventory drift")
    if any(item.get("status") not in allowed_status for item in capabilities.values()):
        raise ValueError("working contract capability status is invalid")
    for capability_name, capability in capabilities.items():
        eligible = set(capability.get("eligible_element_ids", []))
        excluded = set(capability.get("excluded_element_ids", []))
        if not eligible.issubset(all_element_ids) or not excluded.issubset(
            all_element_ids
        ):
            raise ValueError(
                f"working contract capability references unknown elements: {capability_name}"
            )
        if eligible.intersection(excluded):
            raise ValueError(
                f"working contract capability both includes and excludes elements: {capability_name}"
            )
        expected_eligible_fields = sorted(
            _field_ref(element["element_id"], field_name)
            for element in elements
            for field_name, ownership in element["field_ownership"].items()
            if element["element_id"] in eligible and ownership == "source_owned"
        )
        expected_excluded_fields = sorted(
            _field_ref(element["element_id"], field_name)
            for element in elements
            for field_name, ownership in element["field_ownership"].items()
            if not (element["element_id"] in eligible and ownership == "source_owned")
        )
        if capability.get("eligible_field_refs") != expected_eligible_fields:
            raise ValueError(
                f"working contract eligible field projection drift: {capability_name}"
            )
        if capability.get("excluded_field_refs") != expected_excluded_fields:
            raise ValueError(
                f"working contract excluded field projection drift: {capability_name}"
            )
    for capability_name, expected_status in {
        "simulation": "ineligible",
        "transition_trace": "ineligible",
        "repair": "not_run",
        "confirm": "not_run",
        "final_export": "not_run",
        "main_result": "not_run",
    }.items():
        capability = capabilities[capability_name]
        if capability.get("status") != expected_status:
            raise ValueError(f"baseline {capability_name} status is not fail-closed")
        if capability.get("eligible_element_ids"):
            raise ValueError(
                f"baseline {capability_name} unexpectedly authorizes elements"
            )
        if set(capability.get("excluded_element_ids", [])) != all_element_ids:
            raise ValueError(f"baseline {capability_name} exclusion inventory drift")
    diagnostic_capability = capabilities["inspect_diagnostics"]
    expected_diagnostic_status = (
        "not_run" if binding_status == "unbound" else "ineligible"
    )
    if diagnostic_capability.get("status") != expected_diagnostic_status:
        raise ValueError("inspect diagnostic capability status does not match binding")
    if diagnostic_capability.get("eligible_element_ids"):
        raise ValueError("baseline inspect diagnostics authorize source issue evidence")
    if set(diagnostic_capability.get("excluded_element_ids", [])) != all_element_ids:
        raise ValueError("inspect diagnostic capability exclusion inventory drift")
    for capability_name in ("contract_integrity", "parse"):
        capability = capabilities[capability_name]
        if capability.get("eligible_element_ids") or capability.get(
            "eligible_field_refs"
        ):
            raise ValueError(
                f"artifact-scoped {capability_name} authorizes semantic elements"
            )
        if set(capability.get("excluded_element_ids", [])) != all_element_ids:
            raise ValueError(
                f"artifact-scoped {capability_name} exclusion inventory drift"
            )
    attribution_policy = contract.get("attribution_policy", {})
    expected_attribution_limits = {
        "confirmed_issue_conversion_artifact_limit": 0,
        "repair_target_conversion_artifact_limit": 0,
        "confirm_accepted_conversion_artifact_limit": 0,
        "main_result_conversion_artifact_limit": 0,
    }
    for field, expected in expected_attribution_limits.items():
        if attribution_policy.get(field) != expected:
            raise ValueError(f"{field} drift")
    if attribution_policy.get("candidate_conversion_artifact_policy") != (
        "allowed_only_as_explicitly_classified_non_repairable_noise"
    ):
        raise ValueError("candidate conversion artifact policy drift")
    if attribution_policy.get("source_internal_consistency_check_policy") != (
        "manifest_bound_executed_checker_artifact_required"
    ):
        raise ValueError("source internal consistency checker policy drift")
    if contract.get("usage_gate") == "discover_input_with_capability_mask":
        if binding_status != "bound":
            raise ValueError(
                "Discover input requires bound inspect diagnostic attribution"
            )
        if capabilities["contract_integrity"]["status"] != "eligible":
            raise ValueError("Discover input requires an eligible contract")
        if capabilities["source_static_discovery"]["status"] not in {
            "eligible",
            "eligible_with_exclusions",
        }:
            raise ValueError("Discover input requires source-static capability")
        compiler_ids = {
            item["element_id"]
            for item in elements
            if item.get("origin") == "compiler_owned"
        }
        if not compiler_ids.issubset(
            capabilities["inspect_diagnostics"]["excluded_element_ids"]
        ):
            raise ValueError("Discover diagnostics expose compiler-owned elements")
        if not compiler_ids.issubset(capabilities["repair"]["excluded_element_ids"]):
            raise ValueError("Repair capability exposes compiler-owned elements")
        if trace.get("source_traceability", {}).get("closure_claim_allowed"):
            raise ValueError("Discover input cannot pre-authorize closure claims")
    review_subject = contract.get("review_subject")
    if review_subject is not None:
        expected_obligations = build_review_obligations(
            comparison=comparison,
            official_identity=canonical["metadata"]["official_identity_reconciliation"],
            contract=contract,
        )
        if review_subject.get("review_obligations") != expected_obligations:
            raise ValueError("review obligation inventory drift")
        expected_risk_tags = sorted({item["risk_tag"] for item in expected_obligations})
        if review_subject.get("risk_tags") != expected_risk_tags:
            raise ValueError("review risk-tag inventory drift")
        if review_subject.get("second_pass_required") != bool(expected_obligations):
            raise ValueError("review second-pass requirement drift")
