#!/usr/bin/env python3
"""Export deterministic TSV mirrors and audit logs for baseline v3."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def load(path: Path) -> Any:
    """Load one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Return the archive-prefixed SHA-256 of one file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def json_cell(value: Any) -> str:
    """Serialize nested JSON values as one deterministic TSV cell."""

    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_tsv(path: Path, fieldnames: tuple[str, ...], rows: Iterable[dict[str, Any]]) -> int:
    """Write a fixed-column TSV mirror and return its row count."""

    count = 0
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n", extrasaction="raise")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})
            count += 1
    return count


def group_rows(groups: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """Flatten substantive N groups and separately named I clusters."""

    for group in sorted(groups["n_groups"] + groups["invalid_clusters"], key=lambda value: value["group_id"]):
        yield {
            "schema": "paper1.manual-adjudication.v3-baseline-ni.groups",
            "group_id": group["group_id"],
            "group_kind": group["group_kind"],
            "side": group["side"],
            "pair_id": group["pair_id"],
            "cross_round_merge": group.get("cross_round_merge", ""),
            "member_report_ids": json_cell(group["member_report_ids"]),
            "member_count": len(group["member_report_ids"]),
            "normative_obligation": group.get("normative_obligation", ""),
            "author_source_locus": group.get("author_source_locus", ""),
            "substantive_root_cause": group.get("substantive_root_cause", ""),
            "repair_intent": group.get("repair_intent", ""),
            "d_tiers": json_cell(group.get("d_tiers", [])),
            "reason": group["reason"],
            "basis": group["basis"],
            "source_refs": json_cell(group["source_refs"]),
            "member_source_refs": json_cell(group["member_source_refs"]),
            "non_merge_reasons": json_cell(group.get("non_merge_reasons", [])),
        }


def relation_rows(document: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """Flatten the canonical non-K relation matrix."""

    for row in document["rows"]:
        yield {
            "schema": "paper1.manual-adjudication.v3-baseline-ni.relations",
            "side": row["side"],
            "pair_id": row["pair_id"],
            "round": row["round"],
            "report_id": row["report_id"],
            "expected_id": row["expected_id"],
            "relation": row["relation"],
            "reason": row["reason"],
            "basis": row["basis"],
            "source_refs": json_cell(row["source_refs"]),
            "report_owned_field_refs": json_cell(row["report_owned_field_refs"]),
        }


def full_relation_rows(document: dict[str, Any]) -> Iterable[dict[str, Any]]:
    """Flatten the full 512-report relation projection."""

    for row in document["rows"]:
        yield {
            "schema": "paper1.manual-adjudication.v3-baseline-ni.relation-projection",
            "source": row["source"],
            "side": "x1v2_baseline",
            "pair_id": row["pair_id"],
            "round": row["round"],
            "report_id": row["report_id"],
            "expected_id": row["expected_id"],
            "relation": row["relation"],
            "reason": row["reason"],
            "basis": row["basis"],
            "source_refs": json_cell(row["source_refs"]),
            "report_owned_field_refs": json_cell(row["report_owned_field_refs"]),
        }


def main() -> None:
    """Write TSV mirrors plus provider-free audit/review logs."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    reviews = v3 / "reviews"
    reviews.mkdir(parents=True, exist_ok=True)

    decisions = load(v3 / "baseline_report_decisions_v3.json")["decisions"]
    relations = load(v3 / "baseline_relation_decisions_v3.json")
    projection = load(v3 / "baseline_relation_projection_v3.json")
    groups = load(v3 / "baseline_n_groups_v3.json")["groups"]
    summary = load(v3 / "recomputed_summary_v3.json")
    inventory = load(v3 / "inventory.json")

    group_fields = (
        "schema", "group_id", "group_kind", "side", "pair_id", "cross_round_merge",
        "member_report_ids", "member_count", "normative_obligation", "author_source_locus",
        "substantive_root_cause", "repair_intent", "d_tiers", "reason", "basis",
        "source_refs", "member_source_refs", "non_merge_reasons",
    )
    relation_fields = (
        "schema", "side", "pair_id", "round", "report_id", "expected_id", "relation",
        "reason", "basis", "source_refs", "report_owned_field_refs",
    )
    projection_fields = ("schema", "source", *relation_fields[1:])
    group_count = write_tsv(v3 / "baseline_n_groups_v3.tsv", group_fields, group_rows(groups))
    relation_count = write_tsv(v3 / "baseline_relation_decisions_v3.tsv", relation_fields, relation_rows(relations))
    projection_count = write_tsv(v3 / "baseline_relation_projection_v3.tsv", projection_fields, full_relation_rows(projection))

    decision_ids = {row["original_report_id"] for row in decisions}
    final_n = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "N"}
    final_i = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "I"}
    review_statuses = Counter(row["review"]["review_status"] for row in decisions)
    reviewer_ids = sorted({reviewer for row in decisions for reviewer in row["review"]["independent_reviewer_ids"]})
    disagreement_ids = sorted(row["original_report_id"] for row in decisions if row["review"]["disagreement_flag"])
    arbitration_ids = sorted(row["original_report_id"] for row in decisions if row["review"].get("arbitration_record_pointer"))

    output_paths = (
        "baseline_n_groups_v3.tsv",
        "baseline_relation_decisions_v3.tsv",
        "baseline_relation_projection_v3.tsv",
    )
    audit = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.audit-log",
        "protocol_version": summary["protocol_version"],
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "generator": "scripts/evaluation/export_baseline_v3_audit.py",
        "scope": "Provider-free export and closure audit of the frozen baseline v3 layer.",
        "inputs": {
            "inventory": {"path": "inventory.json", "sha256": sha256(v3 / "inventory.json")},
            "decisions": {"path": "baseline_report_decisions_v3.json", "sha256": sha256(v3 / "baseline_report_decisions_v3.json")},
            "relations": {"path": "baseline_relation_decisions_v3.json", "sha256": sha256(v3 / "baseline_relation_decisions_v3.json")},
            "projection": {"path": "baseline_relation_projection_v3.json", "sha256": sha256(v3 / "baseline_relation_projection_v3.json")},
            "groups": {"path": "baseline_n_groups_v3.json", "sha256": sha256(v3 / "baseline_n_groups_v3.json")},
            "summary": {"path": "recomputed_summary_v3.json", "sha256": sha256(v3 / "recomputed_summary_v3.json")},
        },
        "outputs": [{"path": path, "sha256": sha256(v3 / path)} for path in output_paths],
        "counts": {
            "inventory_items": len(inventory["items"]),
            "decisions": len(decisions),
            "final_n_reports": len(final_n),
            "final_i_reports": len(final_i),
            "n_groups": len(groups["n_groups"]),
            "i_clusters": len(groups["invalid_clusters"]),
            "non_k_relation_rows": relation_count,
            "full_projection_rows": projection_count,
            "group_rows": group_count,
        },
        "review_chain": {
            "review_statuses": dict(review_statuses),
            "independent_reviewer_ids": reviewer_ids,
            "independent_reviewer_count": len(reviewer_ids),
            "disagreement_count": len(disagreement_ids),
            "disagreement_report_ids": disagreement_ids,
            "arbitration_count": len(arbitration_ids),
            "arbitration_report_ids": arbitration_ids,
            "all_human_confirmed": all(row["review"]["human_confirmation"] for row in decisions),
        },
        "execution_boundary": {
            "provider_calls": 0,
            "method_reruns": 0,
            "judge_reruns": 0,
            "raw_modified": False,
            "current_modified": False,
        },
        "canonical_rule": "This file records exports and checks only; it does not assign D/A, validity, relation, K/N/I, or groups.",
    }
    (v3 / "baseline_audit_log_v3.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    review_log = {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.review-log",
        "protocol_version": summary["protocol_version"],
        "scope": "Persisted review-chain and independent provider-free review index; proposals remain proposals.",
        "canonical_decision_path": "baseline_report_decisions_v3.json",
        "canonical_group_path": "baseline_n_groups_v3.json",
        "review_artifacts": [
        "reviews/independent_final_gate_review.json",
        "reviews/grouping_independent_review.json",
        "reviews/academic_citation_review.json",
        "reviews/academic_grouping_review_v3.json",
        "reviews/numeric_recompute_review_v3.json",
        "reviews/evidence_closure_review_v3.json",
        "reviews/fairness_leakage_review_v3.json",
        "reviews/shuorenhua_process_v3.json",
        ],
        "report_count": len(decision_ids),
        "independent_reviewer_ids": reviewer_ids,
        "independent_reviewer_count": len(reviewer_ids),
        "coverage": {"decisions": len(decisions), "expected_per_decision": 145, "non_k_relation_rows": relation_count},
        "disagreement_count": len(disagreement_ids),
        "arbitration_count": len(arbitration_ids),
        "human_confirmation": all(row["review"]["human_confirmation"] for row in decisions),
        "proposal_policy": "Track A/Track B and other subagent artifacts are proposal-only; none is renamed as final human truth.",
        "provider_calls": 0,
        "method_or_judge_reruns": 0,
    }
    (v3 / "review_log_v3.json").write_text(json.dumps(review_log, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "groups_tsv": group_count, "non_k_relations_tsv": relation_count, "projection_tsv": projection_count, "review_log": str(v3 / "review_log_v3.json")}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
