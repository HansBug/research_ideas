"""Deterministic post-run stage-loss and receipt-closure reports.

The builder consumes completed method and external Judge artifacts only.  It is
an evaluator-side audit tool: no result from the Judge or ledger is imported by
the method runner, and no value produced here is suitable for a method prompt.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from ..registry import load_registry
from .applicability import GLOBAL_PLANNED_PREDICATES
from .export import write_json

ALL_FROZEN_PREDICATES = (
    "S1", "S2", "S3", "S4", "S5", "S6",
    "G1", "G2", "G3", "G4",
    "R1", "R2", "R3", "R4",
    "V1", "V2", "V3", "V4", "V5",
)
STAGES = (
    "contract_extraction",
    "grounding",
    "frontier",
    "candidate",
    "execute_batch",
    "evidence_record",
    "publish",
    "judge_mapping",
)
STAGE_OWNERS = {
    "contract_extraction": "contract_extraction",
    "grounding": "grounding",
    "frontier": "typed_frontier",
    "candidate": "candidate_projection",
    "execute_batch": "predicate_compiler_or_backend",
    "evidence_record": "evidence_assembly",
    "publish": "publish_adapter",
    "judge_mapping": "external_judge",
}
WITNESS_RANK = {"W0": 0, "W1": 1, "W2": 2}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _items(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, dict)]
    return []


def _refs(value: Any) -> set[str]:
    if not isinstance(value, list | tuple):
        return set()
    return {str(item) for item in value if isinstance(item, str) and item}


def _hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _max_witness_level(rows: Iterable[dict[str, Any]]) -> str | None:
    """Return the strongest observed three-level witness without inventing one."""

    levels = [
        str(row.get("witness_level"))
        for row in rows
        if row.get("witness_level") in WITNESS_RANK
    ]
    return max(levels, key=WITNESS_RANK.__getitem__) if levels else None


def _method_path(method_root: Path, pair_id: str) -> Path:
    return method_root / "method" / pair_id / "round-1.json"


def _index_method(payload: dict[str, Any]) -> dict[str, Any]:
    stages = payload.get("stage_outputs", {})
    extraction = stages.get("contract_extraction", {})
    grounding = stages.get("discovery_grounding", {})
    execute = stages.get("execute_batch", {})
    contracts = _items(extraction.get("contracts"))
    grounding_rows: list[dict[str, Any]] = []
    branches = grounding.get("branches", {})
    for branch in _items(branches):
        grounding_rows.extend(_items(branch.get("candidates")))
        grounding_rows.extend(_items(branch.get("additional_contracts")))
        grounding_rows.extend(_items(branch.get("unresolved")))
        grounding_rows.extend(_items(branch.get("semantic_bindings")))
        grounding_rows.extend(_items(branch.get("cardinality_bindings")))
    frontier = execute.get("frontier_batch", {})
    checks = _items(frontier.get("checks"))
    checks.extend(_items(execute.get("frontier_unresolved_admission")))
    candidates = []
    for raw_candidate in _items(execute.get("candidates")):
        candidate = raw_candidate.get("candidate")
        normalized = dict(candidate) if isinstance(candidate, dict) else dict(raw_candidate)
        for key in ("obligation_id", "plan", "receipt", "binding", "source_attribution"):
            if key not in normalized and key in raw_candidate:
                normalized[key] = raw_candidate[key]
        candidates.append(normalized)
    receipts = _items(execute.get("predicate_execution_receipts"))
    evidence = _items(payload.get("evidence_records"))
    issue_ids = {str(item) for item in execute.get("publish", {}).get("report_issue_ids", ()) if item}
    issue_ids.update(str(item) for item in stages.get("publish", {}).get("report_issue_ids", ()) if item)
    by_contract: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in contracts + grounding_rows + checks + candidates:
        contract_id = item.get("contract_id") or item.get("canonical_contract_id")
        if isinstance(contract_id, str) and contract_id:
            by_contract[contract_id].append(item)
    by_obligation: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in candidates:
        obligation_id = item.get("obligation_id")
        if isinstance(obligation_id, str) and obligation_id:
            by_obligation[obligation_id].append(item)
    by_issue = {
        str(item.get("issue_id")): item
        for item in evidence
        if isinstance(item.get("issue_id"), str)
    }
    by_predicate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for receipt in receipts:
        predicate_id = receipt.get("predicate_id")
        if isinstance(predicate_id, str) and predicate_id in ALL_FROZEN_PREDICATES:
            by_predicate[predicate_id].append(receipt)
    return {
        "contracts": contracts,
        "grounding_rows": grounding_rows,
        "checks": checks,
        "candidates": candidates,
        "receipts": receipts,
        "evidence": evidence,
        "by_contract": by_contract,
        "by_obligation": by_obligation,
        "by_issue": by_issue,
        "by_predicate": by_predicate,
        "publish_issue_ids": sorted(issue_ids),
    }


def _compact_candidate(item: dict[str, Any], *, evidence: dict[str, Any] | None = None) -> dict[str, Any]:
    plan = item.get("plan") if isinstance(item.get("plan"), dict) else {}
    receipt = item.get("execution_receipt")
    if not isinstance(receipt, dict):
        receipt = item.get("receipt") if isinstance(item.get("receipt"), dict) else {}
    return {
        "issue_id": (evidence or {}).get("issue_id"),
        "obligation_id": item.get("obligation_id"),
        "contract_id": item.get("contract_id"),
        "predicate_id": item.get("predicate_id"),
        "predicate_inputs": item.get("predicate_inputs", {}),
        "element_refs": item.get("element_refs", []),
        "source_refs": item.get("source_refs", []),
        "witness_level": item.get("witness_level") or (evidence or {}).get("witness_level"),
        "d_level": item.get("d_level") or (evidence or {}).get("d_level"),
        "published": bool(item.get("issue_emitted")) or bool(item.get("issue_id")) or evidence is not None,
        "plan_id": plan.get("plan_id"),
        "receipt_hash": receipt.get("receipt_hash"),
    }


def _matching_contracts(index: dict[str, Any], expected: dict[str, Any]) -> list[dict[str, Any]]:
    expected_refs = _refs(expected.get("source_refs"))
    matches: list[dict[str, Any]] = []
    for contract in index["contracts"]:
        contract_refs = _refs(contract.get("source_refs"))
        segment_id = contract.get("segment_id")
        if expected_refs & contract_refs or (isinstance(segment_id, str) and segment_id in expected_refs):
            matches.append(contract)
    return matches


def _grounding_for_contract(index: dict[str, Any], contract_ids: Iterable[str]) -> list[dict[str, Any]]:
    rows = []
    for contract_id in contract_ids:
        for item in index["by_contract"].get(contract_id, ()):
            if item in index["grounding_rows"]:
                rows.append(item)
    return rows


def _frontier_for_contract(index: dict[str, Any], contract_ids: Iterable[str]) -> list[dict[str, Any]]:
    wanted = set(contract_ids)
    return [
        item for item in index["checks"]
        if item.get("canonical_contract_id") in wanted
        or wanted.intersection(_refs(item.get("source_contract_ids")))
        or item.get("contract_id") in wanted
    ]


def _method_stage(contract_rows: list[dict[str, Any]], grounding: list[dict[str, Any]], frontier: list[dict[str, Any]], candidates: list[dict[str, Any]], receipts: list[dict[str, Any]], evidence: list[dict[str, Any]], published: list[str]) -> str:
    if published:
        return "publish"
    if evidence:
        return "evidence_record"
    if receipts:
        return "execute_batch"
    if candidates:
        return "candidate"
    if frontier:
        return "frontier"
    if grounding:
        return "grounding"
    if contract_rows:
        return "contract_extraction"
    return "no_observation"


def _expected_row(
    *,
    pair_id: str,
    method_path: Path,
    index: dict[str, Any],
    expected: dict[str, Any],
    judge_pair_path: Path,
    report_validity: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    full_reports = [str(item) for item in expected.get("full_report_ids", ()) if item]
    partial_reports = [str(item) for item in expected.get("partial_report_ids", ()) if item]
    mapped_reports = full_reports + partial_reports
    evidence = [index["by_issue"][report_id] for report_id in mapped_reports if report_id in index["by_issue"]]
    candidates: list[dict[str, Any]] = []
    for item in evidence:
        obligation_id = item.get("obligation_id")
        candidates.extend(index["by_obligation"].get(obligation_id, ()))
    contract_rows = _matching_contracts(index, expected)
    contract_ids = sorted({str(item.get("contract_id")) for item in candidates + evidence if item.get("contract_id")})
    contract_ids.extend(
        item.get("contract_id") for item in contract_rows
        if isinstance(item.get("contract_id"), str) and item.get("contract_id") not in contract_ids
    )
    grounding = _grounding_for_contract(index, contract_ids)
    frontier = _frontier_for_contract(index, contract_ids)
    evidence_by_obligation = {
        item.get("obligation_id"): item
        for item in evidence
        if item.get("obligation_id")
    }
    candidate_rows = [
        _compact_candidate(item, evidence=evidence_by_obligation.get(item.get("obligation_id")))
        for item in candidates
        if item.get("predicate_id") is not None or item.get("obligation_id")
    ]
    obligation_ids = {item.get("obligation_id") for item in candidates if item.get("obligation_id")}
    receipts = [item for item in index["receipts"] if item.get("obligation_id") in obligation_ids]
    published = [report_id for report_id in mapped_reports if report_id in index["publish_issue_ids"]]
    receipt_by_obligation = {
        str(item.get("obligation_id")): item
        for item in receipts
        if item.get("obligation_id")
    }
    report_match = {
        **{report_id: "FULL" for report_id in full_reports},
        **{report_id: "PARTIAL" for report_id in partial_reports},
    }
    matching_reports: list[dict[str, Any]] = []
    for report_id in mapped_reports:
        evidence_row = index["by_issue"].get(report_id)
        obligation_id = evidence_row.get("obligation_id") if evidence_row else None
        receipt = receipt_by_obligation.get(str(obligation_id), {}) if obligation_id else {}
        plan = evidence_row.get("plan") if isinstance((evidence_row or {}).get("plan"), dict) else {}
        audit_bundle = evidence_row.get("audit_bundle") if isinstance((evidence_row or {}).get("audit_bundle"), dict) else {}
        matching_reports.append({
            "report_id": report_id,
            "match_status": report_match[report_id],
            "predicate_id": (evidence_row or {}).get("predicate_id"),
            "witness_level": (evidence_row or {}).get("witness_level"),
            "d_level": (evidence_row or {}).get("d_level"),
            "published": report_id in published,
            "receipt_chain": {
                "obligation_id": obligation_id,
                "predicate_logic": plan.get("semantics") or plan.get("formal_program"),
                "typed_inputs": receipt.get("typed_inputs") or plan.get("inputs"),
                "typed_inputs_hash": receipt.get("typed_inputs_hash"),
                "compiled_program": receipt.get("compiled_program") or plan.get("formal_program"),
                "compiled_program_hash": receipt.get("compiled_program_hash") or plan.get("formal_program_hash"),
                "backend": receipt.get("backend"),
                "algorithm_version": receipt.get("algorithm_version"),
                "execution_state": receipt.get("execution_state"),
                "terminal_state": receipt.get("terminal_state"),
                "predicate_verdict": receipt.get("predicate_verdict"),
                "verdict": receipt.get("verdict"),
                "failure_kind": receipt.get("failure_kind"),
                "artifact_attribution_complete": receipt.get("artifact_attribution_complete"),
                "receipt_hash": receipt.get("receipt_hash"),
                "audit_bundle_hash": audit_bundle.get("audit_hash"),
                "reason": receipt.get("reason") or (evidence_row or {}).get("reason"),
                "basis": receipt.get("basis") or (evidence_row or {}).get("basis"),
            },
        })
    max_witness_level = _max_witness_level(matching_reports)
    last_stage = _method_stage(contract_rows, grounding, frontier, candidates, receipts, evidence, published)
    if full_reports:
        judge_disposition = "FULL"
    elif partial_reports:
        judge_disposition = "PARTIAL"
    else:
        judge_disposition = "NO_MATCH"
    if evidence:
        method_disposition = "evidence_recorded"
    elif candidates:
        method_disposition = "candidate_not_published"
    elif frontier:
        method_disposition = "frontier_without_candidate"
    elif grounding:
        method_disposition = "grounding_without_downstream_candidate"
    elif contract_rows:
        method_disposition = "contract_without_downstream_row"
    else:
        method_disposition = "identity_or_contract_unresolved"
    if judge_disposition == "NO_MATCH" and method_disposition == "identity_or_contract_unresolved":
        root_cause_owner = "contract_extraction_or_identity_binding"
    else:
        root_cause_owner = STAGE_OWNERS.get(last_stage, last_stage)
    return {
        "pair_id": pair_id,
        "expected_id": expected.get("ledger_id"),
        "summary": expected.get("reason"),
        "method_artifact": str(method_path.resolve()),
        "contract_ids": contract_ids,
        "contract_extraction": {
            "status": "present" if contract_rows else "no_matching_contract",
            "contracts": [
                {
                    "contract_id": item.get("contract_id"),
                    "segment_id": item.get("segment_id"),
                    "property": item.get("property"),
                    "source_refs": item.get("source_refs", []),
                    "reason": item.get("reason"),
                    "basis": item.get("basis"),
                }
                for item in contract_rows
            ],
        },
        "grounding": {
            "status": "present" if grounding else "no_row",
            "bindings": [
                {
                    "contract_id": item.get("contract_id"),
                    "binding_id": item.get("binding_id"),
                    "model_element_ref": item.get("model_element_ref"),
                    "carrier_transition_ref": item.get("carrier_transition_ref"),
                    "status": item.get("status"),
                    "reason": item.get("reason"),
                    "basis": item.get("basis"),
                }
                for item in grounding
                if item.get("binding_id") or item.get("model_element_ref")
            ],
            "unresolved": [
                {"contract_id": item.get("contract_id"), "reason": item.get("reason"), "basis": item.get("basis")}
                for item in grounding
                if item.get("status") in {"unresolved", "identity_unresolved"}
            ],
        },
        "frontier": {
            "status": "present" if frontier else "no_row",
            "checks": [
                {
                    "check_id": item.get("check_id"),
                    "kind": item.get("kind"),
                    "status": item.get("status"),
                    "model_refs": item.get("model_refs", []),
                    "root_refs": item.get("root_refs", []),
                    "marked_refs": item.get("marked_refs", []),
                    "reason": item.get("reason"),
                    "basis": item.get("basis"),
                }
                for item in frontier
            ],
        },
        "candidate": {
            "status": "exact_candidate" if candidate_rows else "no_prepared_candidate",
            "exact_candidate": bool(candidate_rows),
            "rows": candidate_rows,
        },
        "execute_batch": {
            "status": "receipt_present" if receipts else "no_execution_row",
            "receipts": [
                {
                    "obligation_id": item.get("obligation_id"),
                    "predicate_id": item.get("predicate_id"),
                    "execution_status": item.get("execution_status"),
                    "terminal_state": item.get("terminal_state"),
                    "verdict": item.get("verdict"),
                    "typed_inputs_hash": item.get("typed_inputs_hash"),
                    "compiled_program_hash": item.get("compiled_program_hash"),
                    "receipt_hash": item.get("receipt_hash"),
                    "reason": item.get("reason"),
                    "basis": item.get("basis"),
                }
                for item in receipts
            ],
        },
        "evidence_record": {
            "status": "present" if evidence else "not_published_to_evidence",
            "rows": [
                {
                    "issue_id": item.get("issue_id"),
                    "obligation_id": item.get("obligation_id"),
                    "predicate_id": item.get("predicate_id"),
                    "witness_level": item.get("witness_level"),
                    "d_level": item.get("d_level"),
                    "reason": item.get("reason"),
                    "basis": item.get("basis"),
                }
                for item in evidence
            ],
        },
        "publish": {
            "status": "published" if published else "not_published",
            "issue_ids": published,
        },
        "judge_mapping": {
            "status": "mapped",
            "artifact": str(judge_pair_path.resolve()),
            "full_report_ids": full_reports,
            "partial_report_ids": partial_reports,
            "source_refs": expected.get("source_refs", []),
            "report_validity": {key: report_validity[key] for key in mapped_reports if key in report_validity},
            "reason": expected.get("reason"),
            "basis": expected.get("basis"),
        },
        "match_status": (
            "FULL" if full_reports else "PARTIAL" if partial_reports else "NONE"
        ),
        "matching_report_ids": mapped_reports,
        "matching_reports": matching_reports,
        "max_witness_level": max_witness_level,
        "max_witness_basis": (
            "max(W) is computed over matching reports with the fixed ordering W2 > W1 > W0; "
            "a missing evidence record never manufactures a witness level."
        ),
        "last_method_stage": last_stage,
        "last_observed_stage": "judge_mapping",
        "method_disposition": method_disposition,
        "judge_disposition": judge_disposition,
        "witness_level": next((item.get("witness_level") for item in evidence if item.get("witness_level")), None),
        "d_level": next((item.get("d_level") for item in evidence if item.get("d_level")), None),
        "root_cause_owner": root_cause_owner,
        "reason": "Every expected row is assigned a terminal method and Judge disposition from immutable artifact joins; no missing downstream stage is silently omitted.",
        "basis": "method JSON stage_outputs, evidence records, external Judge expected_outcomes, and evaluator-side report IDs",
    }


def _predicate_feasibility(
    *,
    method_indexes: dict[str, dict[str, Any]],
    applicability: dict[str, Any] | None,
) -> dict[str, Any]:
    rows = _items(applicability.get("rows")) if applicability else []
    app_by_predicate: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        predicate_id = row.get("predicate_id")
        if isinstance(predicate_id, str):
            app_by_predicate[predicate_id].append(row)
    output: dict[str, Any] = {}
    for predicate_id in ALL_FROZEN_PREDICATES:
        receipts = [receipt for index in method_indexes.values() for receipt in index["receipts"] if receipt.get("predicate_id") == predicate_id]
        terminal = [receipt for receipt in receipts if receipt.get("execution_status") == "executed" and receipt.get("terminal_state") == "completed" and receipt.get("verdict") in {"pass", "violation"}]
        pass_count = sum(receipt.get("verdict") == "pass" for receipt in terminal)
        violation_count = sum(receipt.get("verdict") == "violation" for receipt in terminal)
        evidence = [item for index in method_indexes.values() for item in index["evidence"] if item.get("predicate_id") == predicate_id]
        w_counts = Counter(item.get("witness_level") for item in evidence if item.get("witness_level") in {"W0", "W1", "W2"})
        applicable_rows = app_by_predicate.get(predicate_id, [])
        not_applicable = sum(row.get("feasibility") == "not_applicable" for row in applicable_rows)
        unsupported = [receipt for receipt in receipts if receipt.get("execution_status") == "unsupported"]
        input_missing = sum("missing" in str(receipt.get("reason", "")).lower() for receipt in unsupported)
        backend_missing = sum(receipt.get("backend") in {None, "none"} for receipt in unsupported)
        if terminal:
            zero_use_reason = None
        elif unsupported and input_missing:
            zero_use_reason = "input_contract_missing"
        elif backend_missing and not terminal:
            zero_use_reason = "backend_missing"
        elif predicate_id not in GLOBAL_PLANNED_PREDICATES:
            zero_use_reason = "not_planned_in_selected_protocol"
        elif applicable_rows and not_applicable == len(applicable_rows):
            zero_use_reason = "not_applicable_in_selected_pairs"
        else:
            zero_use_reason = "no_method_route_or_contract"
        output[predicate_id] = {
            "predicate_id": predicate_id,
            "planned_global": predicate_id in GLOBAL_PLANNED_PREDICATES,
            "applicable_pair_count": sum(row.get("status") == "applicable" for row in applicable_rows),
            "applicability_feasibility": dict(Counter(row.get("feasibility") for row in applicable_rows)),
            "receipt_count": len(receipts),
            "terminal_execution_count": len(terminal),
            "executed_pass": pass_count,
            "executed_violation": violation_count,
            "input_contract_missing": input_missing,
            "backend_missing": backend_missing,
            "outside_selected_planned_denominator": predicate_id not in GLOBAL_PLANNED_PREDICATES,
            "finding_count": len(evidence),
            "pass_count": pass_count,
            "witness_counts": dict(w_counts),
            "zero_use_reason": zero_use_reason,
            "reason": "Terminal execution counts only validated PredicateExecutionReceipt records with pass or violation; plans, prompt IDs, and nonterminal receipts do not count.",
            "basis": "method-owned receipt and evidence joins plus external preflight metadata",
        }
    return output


def _w2_closure(method_indexes: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair_id, index in sorted(method_indexes.items()):
        receipt_by_obligation = {
            item.get("obligation_id"): item for item in index["receipts"] if item.get("obligation_id")
        }
        for evidence in index["evidence"]:
            if evidence.get("witness_level") != "W2":
                continue
            receipt = receipt_by_obligation.get(evidence.get("obligation_id"), {})
            plan = evidence.get("plan") if isinstance(evidence.get("plan"), dict) else {}
            attribution = evidence.get("source_attribution") if isinstance(evidence.get("source_attribution"), dict) else {}
            rows.append({
                "pair_id": pair_id,
                "obligation_id": evidence.get("obligation_id"),
                "issue_id": evidence.get("issue_id"),
                "contract_id": evidence.get("contract_id"),
                "predicate_id": evidence.get("predicate_id"),
                "predicate_logic": plan.get("semantics") or plan.get("formal_program"),
                "compiled_program": plan.get("formal_program"),
                "compiled_program_hash": plan.get("formal_program_hash"),
                "typed_inputs": plan.get("inputs"),
                "typed_inputs_hash": receipt.get("typed_inputs_hash"),
                "backend": receipt.get("backend"),
                "algorithm_version": receipt.get("algorithm_version"),
                "terminal_state": receipt.get("terminal_state"),
                "verdict": receipt.get("verdict"),
                "receipt_hash": receipt.get("receipt_hash"),
                "source_attribution": attribution,
                "reason": evidence.get("reason"),
                "basis": evidence.get("basis"),
            })
    return rows


def build_stage_loss_audit(
    *,
    method_root: str | Path,
    judge_root: str | Path,
    applicability_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build stage-loss, feasibility, and W2 closure artifacts from completed runs."""

    method_root_path = Path(method_root).expanduser().resolve()
    judge_root_path = Path(judge_root).expanduser().resolve()
    manifest = _load(method_root_path / "run_manifest.json")
    pair_ids = tuple(str(item) for item in manifest.get("selected_pair_ids", ()))
    if not pair_ids:
        raise ValueError("method manifest has no selected_pair_ids")
    method_indexes: dict[str, dict[str, Any]] = {}
    method_paths: dict[str, str] = {}
    for pair_id in pair_ids:
        path = _method_path(method_root_path, pair_id)
        payload = _load(path)
        method_indexes[pair_id] = _index_method(payload)
        method_paths[pair_id] = str(path)
    rows: list[dict[str, Any]] = []
    judge_pair_paths: dict[str, str] = {}
    for pair_id in pair_ids:
        judge_pair_path = judge_root_path / "pairs" / f"{pair_id}.json"
        judge_pair_paths[pair_id] = str(judge_pair_path)
        judge_payload = _load(judge_pair_path)
        validity = {
            str(item.get("original_report_id")): {
                "validity": item.get("validity"),
                "full_ledger_ids": item.get("full_ledger_ids", []),
                "partial_ledger_ids": item.get("partial_ledger_ids", []),
            }
            for item in _items(judge_payload.get("report_outcomes"))
            if isinstance(item.get("original_report_id"), str)
        }
        for expected in _items(judge_payload.get("expected_outcomes")):
            rows.append(
                _expected_row(
                    pair_id=pair_id,
                    method_path=_method_path(method_root_path, pair_id),
                    index=method_indexes[pair_id],
                    expected=expected,
                    judge_pair_path=judge_pair_path,
                    report_validity=validity,
                )
            )
    applicability = _load(Path(applicability_path).expanduser().resolve()) if applicability_path else None
    feasibility = _predicate_feasibility(method_indexes=method_indexes, applicability=applicability)
    receipt_rows = [receipt for index in method_indexes.values() for receipt in index["receipts"]]
    evidence_rows = [evidence for index in method_indexes.values() for evidence in index["evidence"]]
    w2_rows = _w2_closure(method_indexes)
    summary = _load(method_root_path / "summary.json")
    payload: dict[str, Any] = {
        "schema": "evidence-discovery.stage-loss-audit.v1",
        "run_id": manifest.get("run_id"),
        "method_root": str(method_root_path),
        "judge_root": str(judge_root_path),
        "source_commit": manifest.get("source_provenance", {}).get("source_commit"),
        "registry_hash": manifest.get("registry_hash"),
        "selected_pair_ids": list(pair_ids),
        "pair_count": len(pair_ids),
        "method_summary_path": str((method_root_path / "summary.json").resolve()),
        "judge_pair_paths": judge_pair_paths,
        "method_boundary": "This report is evaluator-side only and is never imported into method prompts or backend routing.",
        "judge_boundary": "Judge rows are used only to attach final FULL/PARTIAL/NO_MATCH mapping after method artifacts are immutable.",
        "rows": rows,
        "row_count": len(rows),
        "method_pair_artifacts": method_paths,
        "predicate_feasibility": feasibility,
        "w2_receipt_closure": w2_rows,
        "receipt_closure": {
            "receipt_count": len(receipt_rows),
            "terminal_receipt_count": sum(item.get("execution_status") == "executed" and item.get("verdict") in {"pass", "violation"} for item in receipt_rows),
            "predicate_counts": {
                str(predicate_id): count
                for predicate_id, count in Counter(item.get("predicate_id") for item in receipt_rows).items()
            },
            "missing_obligation_ids": sorted(
                str(item.get("obligation_id")) for item in evidence_rows
                if item.get("obligation_id") and not any(receipt.get("obligation_id") == item.get("obligation_id") for receipt in receipt_rows)
            ),
        },
        "method_metrics_snapshot": summary.get("metrics", {}).get("method", {}),
        "audit_basis": "immutable method round JSON, external Judge pair JSON, and optional evaluator-only applicability JSON",
        "reason": "The matrix retains each external expected row, including rows with no method candidate, and records the final observed method stage and loss condition.",
    }
    unsigned = dict(payload)
    payload["artifact_hash"] = _hash(unsigned)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build an evaluator-side evidence-discovery stage-loss audit.")
    parser.add_argument("--method-root", required=True)
    parser.add_argument("--judge-root", required=True)
    parser.add_argument("--applicability", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_stage_loss_audit(
        method_root=args.method_root,
        judge_root=args.judge_root,
        applicability_path=args.applicability,
    )
    write_json(Path(args.output), payload)
    print(json.dumps({"output": str(Path(args.output).resolve()), "artifact_hash": payload["artifact_hash"], "rows": payload["row_count"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
