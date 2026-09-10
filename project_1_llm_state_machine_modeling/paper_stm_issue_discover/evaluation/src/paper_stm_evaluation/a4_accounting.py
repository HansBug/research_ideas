"""Deterministic A4 report-content reuse and oracle precedence, without LLM calls."""

from __future__ import annotations

from copy import deepcopy
import json
from typing import Any


CLAIM_FIELDS = (
    "locus_kind", "locus_names", "property", "violation_direction",
    "requirement_quote", "expected", "observed", "element_refs", "source_refs",
)
SET_FIELDS = {"locus_names", "element_refs", "source_refs", "author_source_anchor", "contract_ids"}


def normalize(value: Any, field: str = "") -> Any:
    if isinstance(value, str):
        return " ".join(value.split())
    if isinstance(value, dict):
        return {key: normalize(item, key) for key, item in sorted(value.items())}
    if isinstance(value, (list, tuple)):
        items = [normalize(item) for item in value]
        return sorted(set(json.dumps(item, sort_keys=True) for item in items)) if field in SET_FIELDS else items
    return value


def claim(item: dict) -> dict:
    return {field: normalize(item.get(field), field) for field in CLAIM_FIELDS}


def publication_members(cell: dict, report: dict) -> list[dict]:
    """Follow only published facet/folding identities, never attached audit receipts."""
    evidence = {item["issue_id"]: item for item in cell["evidence_records"]}
    if len(evidence) != len(cell["evidence_records"]):
        raise ValueError("Duplicate evidence identity")
    ids = {report["issue_id"], *report.get("facet_issue_ids", [])}
    ids.update(item["issue_id"] for item in report.get("folded_sub_claims", []))
    ids.update(report.get("guard_modality_aggregation", {}).get("member_issue_ids", []))
    # A folded representative may itself summarize duplicate facets. Those facets
    # are in its pre-publication typed semantic group, not arbitrary audit probes.
    for issue_id in list(ids):
        if issue_id not in evidence or not evidence[issue_id]["issue_emitted"]:
            raise ValueError(f"Published facet lacks emitted evidence: {issue_id}")
        item = evidence[issue_id]
        key = tuple(json.dumps(item.get(field), sort_keys=True) for field in (
            "locus_kind", "locus_names", "property", "violation_direction"
        ))
        for facet in evidence.values():
            other = tuple(json.dumps(facet.get(field), sort_keys=True) for field in (
                "locus_kind", "locus_names", "property", "violation_direction"
            ))
            if facet["issue_emitted"] and key == other:
                ids.add(facet["issue_id"])
    return [evidence[issue_id] for issue_id in sorted(ids)]


def report_projection(cell: dict, report: dict) -> dict:
    facets = [
        {"obligation_id": item["obligation_id"], "contract_id": item["contract_id"],
         "claim": claim(item)}
        for item in publication_members(cell, report)
    ]
    return {
        "claim": claim(report),
        "author_source_anchor": normalize(report.get("author_source_anchor", []), "author_source_anchor"),
        "contract_ids": normalize(report.get("contract_ids", [report.get("contract_id")]), "contract_ids"),
        "facets": sorted(facets, key=lambda item: item["obligation_id"]),
    }


def account_cell(source: dict, full_judge: dict, replay: dict) -> dict:
    if (source["pair_id"], source["round"]) != (replay["pair_id"], replay["round"]):
        raise ValueError("Cross-cell label reuse is forbidden")
    candidates = {
        item["obligation_id"]: item
        for item in source["stage_outputs"]["execute_batch"]["candidates"]
    }
    labels = {item["original_report_id"]: item for item in full_judge["report_outcomes"]}
    full_reports = {item["issue_id"]: item for item in source["report_issue_clusters"]}
    if set(labels) != set(full_reports):
        raise ValueError("Full labels do not cover final reports exactly")
    by_content = {}
    for report in full_reports.values():
        key = json.dumps(report_projection(source, report), sort_keys=True)
        if key in by_content:
            raise ValueError("Ambiguous Full content identity")
        by_content[key] = report["issue_id"]
    rows, matched = [], set()
    final_ids = [report["issue_id"] for report in replay["report_issue_clusters"]]
    if len(final_ids) != len(set(final_ids)):
        raise ValueError("Duplicate final report identity")
    for report in replay["report_issue_clusters"]:
        projection = report_projection(replay, report)
        true_claims = []
        for item in publication_members(replay, report):
            original = candidates[item["obligation_id"]]
            if original["receipt"]["verdict"] == "true" and claim(item) == claim(original["candidate"]):
                true_claims.append(item["obligation_id"])
        equivalent = by_content.get(json.dumps(projection, sort_keys=True))
        row = {"report_id": report["issue_id"], "projection": projection,
               "oracle_true_obligation_ids": sorted(set(true_claims)),
               "full_equivalent_report_id": equivalent}
        if equivalent is not None:
            matched.add(equivalent)
            row["wording_audit"] = {
                field: {"full": full_reports[equivalent].get(field), "a4": report.get(field)}
                for field in ("reason", "basis", "semantic_adjudication", "witness_level")
                if full_reports[equivalent].get(field) != report.get(field)
            }
        if true_claims:
            row.update(route="oracle_true_I", outcome={
                "original_report_id": report["issue_id"], "validity": "INVALID",
                "full_ledger_ids": [], "partial_ledger_ids": [],
                "reason": "User-specified oracle: a published constituent defect claim had an original true verdict.",
            })
        elif equivalent is not None:
            outcome = deepcopy(labels[equivalent])
            outcome["original_report_id"] = report["issue_id"]
            row.update(route="reused_full", outcome=outcome)
        else:
            row.update(route="residual", outcome=None)
        rows.append(row)
    return {
        "schema": "paper1.a4.report-accounting.v1", "pair_id": replay["pair_id"],
        "round": replay["round"], "reports": rows,
        "disappeared_or_changed_full_report_ids": sorted(set(full_reports) - matched),
        "pending": sum(row["route"] == "residual" for row in rows),
        "completed_zero_report_cell": not rows,
    }
