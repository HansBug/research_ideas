"""Provider-free recomputation for the X1v2 baseline v3 publication layer."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    """Load one JSON artifact."""
    return json.loads(path.read_text(encoding="utf-8"))


def ratio(numerator: int, denominator: int, unit: str, reason: str) -> dict[str, Any]:
    """Return a metric with an explicit unit and denominator."""
    return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator if denominator else None, "unit": unit, "reason": reason}


def rows_and_relations(rows: list[dict[str, Any]], ledger: dict[str, Any]) -> tuple[set[tuple[str, int]], set[tuple[str, int]], Counter[str]]:
    """Project FULL/PARTIAL relations to same-pair expected-round units."""
    full: set[tuple[str, int]] = set()
    partial: set[tuple[str, int]] = set()
    counts: Counter[str] = Counter()
    for report in rows:
        for relation in report["relations"]:
            value = relation["relation"]
            counts[value] += 1
            if str(ledger["items"].get(relation["expected_id"], {}).get("pair")) != report["pair_id"]:
                continue
            if value == "FULL_MATCH":
                full.add((relation["expected_id"], report["round"]))
            elif value == "PARTIAL_MATCH":
                partial.add((relation["expected_id"], report["round"]))
    return full, partial, counts


def full_w2_units(rows: list[dict[str, Any]], full: set[tuple[str, int]]) -> set[tuple[str, int]]:
    """Return unique expected-round FULL units supported by original W2 evidence."""
    return {
        (relation["expected_id"], report["round"])
        for report in rows
        if report["validity"] == "VALID_KNOWN" and report.get("witness", {}).get("level") == "W2"
        for relation in report["relations"]
        if relation["relation"] == "FULL_MATCH"
        and (relation["expected_id"], report["round"]) in full
    }


def project_metrics(rows: list[dict[str, Any]], ledger: dict[str, Any], n_groups: int, i_groups: int, i_report_count: int, cost: dict[str, Any]) -> dict[str, Any]:
    """Compute all report, expected-round, and grouped metrics."""
    expected = ledger["items"]
    expected_ids = set(expected)
    l2_ids = {key for key, value in expected.items() if value.get("L") == "L2"}
    full, partial, relation_counts = rows_and_relations(rows, ledger)
    supported = full | partial
    full_any = {key for key, _ in full}
    full_all = {key for key in expected_ids if {(key, 1), (key, 2), (key, 3)} <= full}
    l2_full = {(key, round_no) for key, round_no in full if key in l2_ids}
    l2_any = {key for key, _ in l2_full}
    l2_all = {key for key in l2_ids if {(key, 1), (key, 2), (key, 3)} <= l2_full}
    valid = [row for row in rows if row["validity"] != "INVALID"]
    invalid = [row for row in rows if row["validity"] == "INVALID"]
    partial_only_reports = [row for row in rows if row["corrected_kni"] == "K" and not any(x["relation"] == "FULL_MATCH" for x in row["relations"]) and any(x["relation"] == "PARTIAL_MATCH" for x in row["relations"])]
    # This metric is published in unique expected-ID units.  A direct set
    # difference here would count expected-round observations instead.
    partial_only_expected = {
        key
        for key in expected_ids
        if any((key, round_no) in partial for round_no in (1, 2, 3))
        and not any((key, round_no) in full for round_no in (1, 2, 3))
    }
    max_witness: Counter[str] = Counter()
    for expected_id, round_no in full:
        witnesses = [row.get("witness", {}).get("level") for row in rows if row["round"] == round_no and row["validity"] == "VALID_KNOWN" and any(x["expected_id"] == expected_id and x["relation"] == "FULL_MATCH" for x in row["relations"])]
        if witnesses:
            max_witness[max(witnesses, key={"W0": 0, "W1": 1, "W2": 2}.get)] += 1
    w2_units = full_w2_units(rows, full)
    k_hits = len(full_any)
    grouped_denominator = k_hits + n_groups + i_groups
    grouped_valid = k_hits + n_groups
    report_denominator = len(rows)
    return {
        "report_count": report_denominator,
        "decision_counts": dict(Counter(row["d_tier"] for row in rows)),
        "d_a_distribution": {key: ratio(Counter(row["d_tier"] for row in rows)[key], report_denominator, "report", "D/A report denominator") for key in ("D2", "D1", "D0", "A0")},
        "validity_counts": dict(Counter(row["validity"] for row in rows)),
        "kni_counts": dict(Counter(row["corrected_kni"] for row in rows)),
        "witness_counts": dict(Counter(row.get("witness", {}).get("level") for row in rows)),
        "relation_counts": {key: ratio(relation_counts[key], report_denominator * len(expected_ids), "report x expected relation", "Dense relation denominator") for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")},
        "full_partial_none": {key: ratio(relation_counts[key], report_denominator * len(expected_ids), "report x expected relation", "Dense relation denominator") for key in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")},
        "hit_at_1_full": ratio(len(full), len(expected_ids) * 3, "expected-round units across all 3 rounds", "One deduplicated expected-round unit per expected and round; denominator is 145 x 3"),
        "hit_at_3_full": ratio(len(full_any), len(expected_ids), "unique expected IDs hit in any of 3 rounds", "Expected-level deduplication"),
        "hit_at_all_full": ratio(len(full_all), len(expected_ids), "unique expected IDs hit in all 3 rounds", "Expected-level all-round closure"),
        "l2_hit_at_1_full": ratio(len(l2_full), len(l2_ids) * 3, "L2 expected-round units across all 3 rounds", "One deduplicated L2 expected-round unit per expected and round; denominator is 39 x 3"),
        "l2_hit_at_3_full": ratio(len(l2_any), len(l2_ids), "unique L2 expected IDs hit in any round", "L2 expected-level deduplication"),
        "l2_hit_at_all_full": ratio(len(l2_all), len(l2_ids), "unique L2 expected IDs hit in all rounds", "L2 expected-level all-round closure"),
        "supported_coverage_round_units": ratio(len(supported), len(expected_ids) * 3, "expected-round units with FULL or PARTIAL", "FULL/PARTIAL supported coverage"),
        "supported_coverage_unique_expected": ratio(len({key for key, _ in supported}), len(expected_ids), "unique expected IDs with FULL or PARTIAL", "Expected-level supported coverage"),
        "partial_only_known_report": ratio(len(partial_only_reports), report_denominator, "report", "K reports with PARTIAL and no FULL"),
        "partial_only_known_expected": ratio(len(partial_only_expected), len(expected_ids), "unique expected IDs", "PARTIAL-only expected IDs after FULL subtraction"),
        "report_based_precision": ratio(len(valid), report_denominator, "raw report", "Valid K or N reports divided by all reports"),
        "report_based_fp_rate": ratio(len(invalid), report_denominator, "raw report", "Invalid I reports divided by all reports"),
        "ledger_group_based_precision": ratio(grouped_valid, grouped_denominator, "unique K expected hit + substantive N groups + invalid diagnostic clusters", "Valid K expected hits plus substantive N groups divided by the grouped publication composition; I clusters are invalid diagnostics"),
        "ledger_group_based_fp_rate": ratio(i_groups, grouped_denominator, "unique K expected hit + substantive N groups + invalid diagnostic clusters", "Invalid diagnostic-cluster share of grouped composition"),
        "ledger_group_composition": {"K_hit": k_hits, "N_group": n_groups, "I_group": i_groups, "denominator": grouped_denominator},
        "ledger_group_sensitivity_unmerged_I": ratio(grouped_valid, k_hits + n_groups + i_report_count, "unique K expected hit + substantive N groups + raw I reports", "Sensitivity when invalid reports are not diagnostically merged"),
        "hit_max_witness": {key: ratio(max_witness[key], len(full), "FULL expected-round hit units", "Maximum W among supporting reports") for key in ("W0", "W1", "W2")},
        "w2_all_expected": ratio(len(w2_units), len(expected_ids) * 3, "expected-round units", "Only original baseline W2 receipts qualify; duplicate reports for one expected-round unit do not increase the numerator and post-hoc Judging cannot upgrade W"),
        "l2_ledger_based": {"status": "not_applicable", "reason": "N/I groups have no natural L2 expected attribution; the baseline layer does not manufacture an L2 ledger precision or FP denominator."},
        "predicate_usage": {"status": "not_applicable", "reason": "X1v2 baseline has no current-side predicate binding schema; not_applicable is not zero."},
        "cost": cost,
    }


def normalize_v2(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize one frozen v2 K/non-K row for combined calculations."""
    return {"report_id": row["report_id"], "pair_id": row["pair_id"], "round": row["round"], "validity": row["validity"], "corrected_kni": row["corrected_kni"], "d_tier": row["strict_da"], "witness": row["witness"], "relations": row["relations"], "source": "frozen_v2"}


def normalize_v3(row: dict[str, Any]) -> dict[str, Any]:
    """Normalize one v3 non-K row for combined calculations."""
    return {"report_id": row["original_report_id"], "pair_id": row["pair_id"], "round": row["round"], "validity": row["validity"], "corrected_kni": row["corrected_kni"], "d_tier": row["d_tier"], "a0_type": row.get("a0_type"), "witness": row["witness"], "relations": row["relations"], "source": "v3_non_k"}


def main() -> None:
    """Recompute combined baseline v3 JSON and a relation mirror."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    v2_dir = args.archive_root / "derived/manual_adjudication_v2"
    v3_dir = args.archive_root / "derived/manual_adjudication_v3_baseline_ni"
    old = load(v2_dir / "x1v2_report_decisions.json")["decisions"]
    new = load(v3_dir / "baseline_report_decisions_v3.json")["decisions"]
    groups = load(v3_dir / "baseline_n_groups_v3.json")["groups"]
    ledger = load(args.archive_root / "reference/ledger.json")
    cost = load(v2_dir / "summary.json")["sides"]["x1v2_baseline"]["cost"]
    frozen_k = [normalize_v2(row) for row in old if row["corrected_kni"] == "K"]
    v3_rows = [normalize_v3(row) for row in new]
    combined = frozen_k + v3_rows
    if len(frozen_k) != 279 or len(v3_rows) != 233 or len(combined) != 512:
        raise ValueError("combined baseline closure failed")
    n_groups = len(groups["n_groups"])
    i_groups = len(groups["invalid_clusters"])
    metrics = project_metrics(combined, ledger, n_groups, i_groups, sum(row["corrected_kni"] == "I" for row in v3_rows), cost)
    original_non_k = {row["report_id"]: row for row in old if row["corrected_kni"] != "K"}
    migrations = Counter(f"{original_non_k[row['report_id']]['corrected_kni']}->{row['corrected_kni']}" for row in v3_rows)
    migration_rows = [{"report_id": row["original_report_id"], "from": original_non_k[row["original_report_id"]]["corrected_kni"], "to": row["corrected_kni"], "d_tier": row["d_tier"], "full_ledger_ids": row["full_ledger_ids"], "partial_ledger_ids": row["partial_ledger_ids"], "reason": row["reclassification_reason"]} for row in sorted(new, key=lambda x: x["original_report_id"])]
    by_round = defaultdict(list)
    by_pair = defaultdict(list)
    for row in combined:
        by_round[row["round"]].append(row)
        by_pair[row["pair_id"]].append(row)
    summary = {
        "schema": "paper1.manual-adjudication.baseline-v3-summary",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "scope": "Frozen baseline K rows plus the complete re-review of the frozen baseline non-K rows; no current/v60 rows are included.",
        "report_count": len(combined),
        "frozen_k_count": len(frozen_k),
        "reviewed_non_k_count": len(v3_rows),
        "metrics": metrics,
        "by_round": {str(key): {"report_count": len(value), "kni": dict(Counter(x["corrected_kni"] for x in value)), "d_a": dict(Counter(x["d_tier"] for x in value))} for key, value in sorted(by_round.items())},
        "by_pair": {key: {"report_count": len(value), "kni": dict(Counter(x["corrected_kni"] for x in value)), "d_a": dict(Counter(x["d_tier"] for x in value))} for key, value in sorted(by_pair.items())},
        "non_k_migrations": {"counts": dict(sorted(migrations.items())), "rows": migration_rows, "new_k_report_ids": [row["report_id"] for row in migration_rows if row["to"] == "K"]},
        "n_grouping": {"original_non_k_n_reports": sum(row["corrected_kni"] == "N" for row in original_non_k.values()), "corrected_n_reports": sum(row["corrected_kni"] == "N" for row in v3_rows), "substantive_n_groups": n_groups, "root_cause_group_count": n_groups, "group_size_distribution": dict(Counter(len(group["member_report_ids"]) for group in groups["n_groups"])), "invalid_diagnostic_cluster_count": i_groups, "invalid_clusters_are_not_defects": True},
        "a0_subtypes": dict(Counter(row["a0_type"] for row in v3_rows + frozen_k if row.get("a0_type"))),
        "reference_ledger_aggregate": {"status": "recomputed", "unit": "expected-round and expected-level", "expected_count": len(ledger["items"]), "full_round_units": len(rows_and_relations(combined, ledger)[0]), "partial_round_units": len(rows_and_relations(combined, ledger)[1]), "reason": "Recomputed from the frozen ledger and combined canonical relation rows."},
        "old_v2_comparison": {"status": "historical_only", "old_v2_counts": dict(Counter(row["corrected_kni"] for row in old)), "new_counts": dict(Counter(row["corrected_kni"] for row in combined)), "delta_reason": "Only non-K rows are re-reviewed in v3; frozen K rows are copied without semantic edits."},
        "provider_calls_in_this_recompute": 0,
        "method_or_judge_reruns_in_this_goal": 0,
    }
    summary_bytes = json.dumps(summary, ensure_ascii=False, indent=2) + "\n"
    args.output.write_text(summary_bytes, encoding="utf-8")
    # Keep the publication summary and the explicitly named recompute copy
    # byte-identical.  Both are generated from the same canonical rows; the
    # validator compares their metrics to prevent stale report snapshots.
    (v3_dir / "summary_v3.json").write_text(summary_bytes, encoding="utf-8")
    full, partial, _ = rows_and_relations(combined, ledger)
    reference_aggregate = {
        "schema": "paper1.manual-adjudication.baseline-v3-reference-ledger-aggregate",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "source_ledger": "reference/ledger.json",
        "source_ledger_sha256": "sha256:" + hashlib.sha256((args.archive_root / "reference/ledger.json").read_bytes()).hexdigest(),
        "unit_definitions": {
            "expected_level": "one unique expected ledger ID",
            "expected_round": "one expected ledger ID in one of three rounds",
            "full_and_partial": "combined frozen-K plus v3 non-K canonical relation projection, same-pair only",
        },
        "expected_count": len(ledger["items"]),
        "expected_round_count": len(ledger["items"]) * 3,
        "l2_expected_count": sum(item.get("L") == "L2" for item in ledger["items"].values()),
        "l2_expected_round_count": sum(item.get("L") == "L2" for item in ledger["items"].values()) * 3,
        "combined_relation_units": {
            "FULL_MATCH": {"numerator": len(full), "denominator": len(ledger["items"]) * 3},
            "PARTIAL_MATCH": {"numerator": len(partial), "denominator": len(ledger["items"]) * 3},
        },
        "provider_calls": 0,
        "reason": "Recomputed offline from the frozen reference ledger and canonical v3 relation projection; no legacy relation label is used to assign a v3 decision.",
    }
    (v3_dir / "reference_ledger_aggregate_v3.json").write_text(json.dumps(reference_aggregate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    relation_rows = []
    for report in combined:
        for relation in report["relations"]:
            relation_rows.append({
                **relation,
                "report_id": report["report_id"],
                "pair_id": report["pair_id"],
                "round": report["round"],
                "source": report["source"],
            })
    (v3_dir / "baseline_relation_projection_v3.json").write_text(json.dumps({"schema": "paper1.manual-adjudication.baseline-v3-relation-projection", "rows": relation_rows}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (v3_dir / "baseline_combined_512_v3.json").write_text(json.dumps({"schema": "paper1.manual-adjudication.baseline-v3-combined", "rows": combined}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"reports": len(combined), "kni": dict(Counter(x["corrected_kni"] for x in combined)), "migrations": dict(migrations), "n_groups": n_groups, "i_clusters": i_groups}, sort_keys=True))


if __name__ == "__main__":
    main()
