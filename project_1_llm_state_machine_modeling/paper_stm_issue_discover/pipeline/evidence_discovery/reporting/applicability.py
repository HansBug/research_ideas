"""Deterministic pair/predicate applicability preflight.

This module is a selection and audit artifact producer only.  Its route table
is never imported by the method runner and it never supplies candidates or
predicate IDs to a method prompt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from ..compiler.inputs import predicate_input_schema
from ..inputs import load_pair
from ..registry import load_registry
from .export import write_json

GLOBAL_PLANNED_PREDICATES = (
    "S1", "S2", "S3", "S4", "S5", "S6",
    "G1", "G4",
    "R1", "R4",
    "V1", "V4",
)

DEFAULT_DIAGNOSTIC_PAIRS = (
    "0001", "0002", "0004", "0010", "0012", "0013", "0023", "0024",
    "0029", "0035", "0046", "0049", "0053", "0054", "0056",
)

# This is a pre-registered diagnostic route baseline, not a method rule.  It
# records which semantic shapes the fixed diagnostic set is intended to test;
# exact execution still requires a method-produced typed contract and closed
# inputs.  The ledger itself currently has no reliable predicate column.
REGISTERED_ROUTE_BASELINE: dict[str, tuple[str, ...]] = {
    "0001": ("G4",),
    "0002": ("G1", "S1", "S2", "S3"),
    "0004": ("G1",),
    "0010": ("R1", "S1", "S2", "S3"),
    "0012": ("R4", "S1"),
    "0023": ("G1",),
    "0024": ("R4", "S2", "S4", "V4"),
    "0029": ("G1", "S2", "V1"),
    "0035": ("S1", "S2", "S5"),
    "0046": ("G1", "S2", "S3"),
    "0053": ("G1", "S2"),
    "0056": ("G4", "R1", "R4", "S6"),
    "0013": ("S1",),
    "0049": ("G1", "S2"),
    "0054": ("S3", "V4"),
}

BACKENDS = {
    **{predicate_id: "source_static" for predicate_id in ("S1", "S2", "S3", "S4", "S5", "S6")},
    **{predicate_id: "topology" for predicate_id in ("G1", "G2", "G3", "G4")},
    **{predicate_id: "trajectory" for predicate_id in ("R1", "R2", "R3", "R4")},
    **{predicate_id: "bounded_verification" for predicate_id in ("V1", "V2", "V3", "V4", "V5")},
}

PREDICATE_ROUTE_BASIS = {
    "S1": "closed declaration membership of an explicitly named element",
    "S2": "exact source/target/scope transition endpoint inventory",
    "S3": "exact transition trigger-set comparison with a closed event inventory",
    "S4": "typed state lifecycle phase and action attachment",
    "S5": "exact typed equality between a requirement guard and transition guard",
    "S6": "exact effect attachment to a specified transition",
    "G1": "finite may-reach graph path from typed source to typed target",
    "G2": "finite universal reachability from a closed source set to a target set",
    "G3": "finite route avoidance with an explicit forbidden node/edge set",
    "G4": "finite coaccessibility from typed roots to typed marked nodes",
    "R1": "closed scenario event-consumption trace over a selected macrostep",
    "R2": "closed finite trace window after an exact stimulus",
    "R3": "closed finite trace window for an exact owner, slot, and behavior occurrence",
    "R4": "closed finite trace interval for an exact retained state",
    "V1": "finite guard domain and independently justified guard disjointness",
    "V2": "finite guard domain and exact choice-group coverage check",
    "V3": "finite closed trace response check with an explicit bound and unit",
    "V4": "finite closed-model progress check from an exact initial scope",
    "V5": "finite reachable-state occupancy invariant check from an exact initial scope",
}


def _hash_payload(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _model_anchors(pair: Any) -> dict[str, Any]:
    return {
        "nl": [segment.segment_id for segment in pair.nl_segments],
        "states": [state.ref for state in pair.model.states],
        "transitions": [transition.ref for transition in pair.model.transitions],
        "events": [event.ref for event in pair.model.events],
    }


def _typed_input_contract(predicate_id: str, predicate: Any) -> dict[str, Any]:
    """Describe a predicate's typed input boundary without supplying values."""

    schema = predicate_input_schema(predicate_id)
    properties = schema.get("properties", {})
    required = set(schema.get("required", []))
    fields = []
    for field_name in predicate.inputs:
        field = properties.get(field_name, {})
        fields.append(
            {
                "name": field_name,
                "required": field_name in required,
                "json_schema": field,
                "description": field.get("description", ""),
            }
        )
    return {
        "predicate_id": predicate_id,
        "registry_inputs": list(predicate.inputs),
        "pydantic_schema": schema,
        "fields": fields,
        "value_status": "method_owned_at_execution; no values supplied by preflight",
    }


def build_applicability_matrix(
    *,
    report_root: str | Path,
    pair_ids: tuple[str, ...] = DEFAULT_DIAGNOSTIC_PAIRS,
) -> dict[str, Any]:
    """Build a machine-readable preflight without reading method/Judge outputs."""

    report_root_path = Path(report_root).expanduser().resolve()
    registry = load_registry()
    pairs: dict[str, Any] = {}
    rows: list[dict[str, Any]] = []
    for pair_id in pair_ids:
        pair = load_pair(report_root_path / "pairs" / pair_id)
        routes = set(REGISTERED_ROUTE_BASELINE.get(pair_id, ()))
        anchors = _model_anchors(pair)
        pairs[pair_id] = {
            "pair_id": pair_id,
            "input_manifest_hash": pair.context_manifest.manifest_hash if pair.context_manifest else None,
            "input_hashes": dict(pair.hashes),
            "route_baseline": sorted(routes),
            "model_anchors": anchors,
        }
        for predicate_id in GLOBAL_PLANNED_PREDICATES:
            predicate = registry.require(predicate_id)
            applicable = predicate_id in routes
            if not applicable:
                status = "not_applicable"
                feasibility = "not_applicable"
                basis = "The deterministic pre-registered semantic-shape route does not assign this predicate to this pair; this is selection provenance, not a method rule."
            elif predicate_id not in BACKENDS:
                status = "unresolved"
                feasibility = "backend_missing"
                basis = "The pre-registered semantic shape is applicable, but the frozen registry has no deterministic backend for this route."
            else:
                status = "applicable"
                feasibility = "routable_now"
                basis = f"{PREDICATE_ROUTE_BASIS[predicate_id]}; the frozen predicate and backend are available; exact contract inputs remain method-owned."
            rows.append({
                "pair_id": pair_id,
                "predicate_id": predicate_id,
                "status": status,
                "feasibility": feasibility,
                "nl_row_anchors": anchors["nl"],
                "stm_row_anchors": anchors["states"] + anchors["transitions"] + anchors["events"],
                "typed_input_contract": _typed_input_contract(predicate_id, predicate),
                "planned_backend": BACKENDS.get(predicate_id),
                "source_ids": list(predicate.sources),
                "route_basis": PREDICATE_ROUTE_BASIS[predicate_id],
                "value_status": "not_materialized; method-owned typed values are required before execution",
                "basis": basis,
                "reason": "Applicability is preflight metadata only; it does not create a method candidate, supply typed values, or execute a predicate.",
            })
    applicable_predicates = sorted({row["predicate_id"] for row in rows if row["status"] == "applicable"})
    payload: dict[str, Any] = {
        "schema": "evidence-discovery.pair_predicate_applicability.v1",
        "registry_version": registry.version,
        "registry_hash": registry.registry_hash,
        "selected_pair_ids": list(pair_ids),
        "pair_count": len(pair_ids),
        "global_planned_predicates": list(GLOBAL_PLANNED_PREDICATES),
        "candidate_predicates_e15": applicable_predicates,
        "candidate_predicate_count_e15": len(applicable_predicates),
        "registered_route_baseline": {key: list(value) for key, value in REGISTERED_ROUTE_BASELINE.items() if key in pair_ids},
        "selection_policy": "The route table is fixed preflight provenance for semantic-shape set cover only. It is never imported by the method worker and cannot create a candidate or predicate input.",
        "method_boundary": "This artifact contains no ledger, expected-issue, Judge, answer, D, L, hit, precision, or evaluation field. It is recorded only as immutable run provenance and is not supplied to contract extraction, grounding, D adjudication, routing, or backend execution.",
        "pairs": pairs,
        "rows": rows,
    }
    payload["artifact_hash"] = _hash_payload(payload)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build evidence-discovery pair/predicate applicability preflight.")
    parser.add_argument("--report-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_applicability_matrix(report_root=args.report_root)
    write_json(Path(args.output), payload)
    print(json.dumps({"output": str(Path(args.output).resolve()), "artifact_hash": payload["artifact_hash"], "e15": payload["candidate_predicates_e15"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
