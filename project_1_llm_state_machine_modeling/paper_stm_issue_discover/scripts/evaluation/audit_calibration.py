"""Recompute the frozen v60 calibration comparison without provider calls.

The preserved v60 N/I audits are reference evidence only.  This command does
not copy their labels into the canonical decisions; it reports exact
agreement, distribution deltas, sentinel checks, and every mismatch.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


RELATIONS = ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")


def load(path: Path) -> Any:
    """Load one JSON document."""

    return json.loads(path.read_text(encoding="utf-8"))


def normalize(value: Any) -> Any:
    """Map legacy empty markers to the canonical null value."""

    return None if value in (None, "", "-", "NA", "null") else value


def parse_ids(value: Any, relation: str) -> tuple[set[str], set[str]]:
    """Parse the legacy relation/ledger representation into exact ID sets."""

    if isinstance(value, list):
        ids = {str(item) for item in value}
        return (ids, set()) if relation == "FULL_MATCH" else (set(), ids) if relation == "PARTIAL_MATCH" else (set(), set())
    full: set[str] = set()
    partial: set[str] = set()
    for token in str(value or "").split("|"):
        kind, separator, expected_id = token.partition(":")
        if not separator:
            continue
        if kind == "FULL":
            full.add(expected_id)
        elif kind == "PARTIAL":
            partial.add(expected_id)
    if relation == "FULL_MATCH":
        return full, set()
    if relation == "PARTIAL_MATCH":
        return set(), full | partial
    return set(), set()


def reference_rows(archive: Path) -> dict[str, dict[str, Any]]:
    """Read the 444 N and 106 I reference rows."""

    rows: dict[str, dict[str, Any]] = {}
    novel = load(archive / "reviews" / "12_v60_valid_novel_posthoc_reaudit.json")
    for source in novel["decisions"]:
        relation = str(source.get("relation") or "NO_MATCH")
        full, partial = parse_ids(source.get("ledger_ids"), relation)
        rows[str(source["report_id"])] = {
            "strict_da": source.get("strict_da"),
            "a0_type": normalize(source.get("a0_type")),
            "corrected_kni": source.get("corrected_kni"),
            "relation": relation,
            "full": full,
            "partial": partial,
            "group_key": source.get("group_key"),
            "source": "reviews/12_v60_valid_novel_posthoc_reaudit.json",
        }
    with (archive / "reviews" / "11_v60_invalid_manual_reaudit.tsv").open(encoding="utf-8", newline="") as handle:
        for source in csv.DictReader(handle, delimiter="\t"):
            # The frozen I audit stores the report-level relation in
            # ``strict_ledger_ids`` even though its legacy default relation
            # column is NO_MATCH.  Parse that field before expanding to the
            # dense expected universe; otherwise valid historical K rows are
            # silently turned into all-NO_MATCH during calibration.
            full, _ = parse_ids(source.get("strict_ledger_ids"), "FULL_MATCH")
            _, partial = parse_ids(source.get("strict_ledger_ids"), "PARTIAL_MATCH")
            partial -= full
            relation = "FULL_MATCH" if full else "PARTIAL_MATCH" if partial else "NO_MATCH"
            rows[str(source["report_id"])] = {
                "strict_da": source.get("manual_d_strict"),
                "a0_type": normalize(source.get("strict_a0_type")),
                "corrected_kni": source.get("strict_correction"),
                "relation": relation,
                "full": full,
                "partial": partial,
                "group_key": source.get("group_key"),
                "source": "reviews/11_v60_invalid_manual_reaudit.tsv",
            }
    if len(rows) != 550:
        raise ValueError(f"reference closure expected 550 rows, got {len(rows)}")
    return rows


def canonical_relation_map(decision: dict[str, Any]) -> dict[str, str]:
    """Return a report's dense relation map."""

    return {str(row["expected_id"]): str(row["relation"]) for row in decision["relations"]}


def reference_relation_map(row: dict[str, Any], expected_ids: set[str]) -> dict[str, str]:
    """Expand a legacy report relation into the dense comparison universe."""

    return {
        expected_id: "FULL_MATCH" if expected_id in row["full"] else "PARTIAL_MATCH" if expected_id in row["partial"] else "NO_MATCH"
        for expected_id in expected_ids
    }


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    """Return count, denominator, and proportion."""

    return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator if denominator else None}


def main() -> None:
    """Write the calibration comparison artifact."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=Path, required=True)
    args = parser.parse_args()
    directory = args.directory.resolve()
    archive = directory.parent.parent
    reference = reference_rows(archive)
    all_final = {
        row["report_id"]: row
        for row in load(directory / "v60_report_decisions.json")["decisions"]
    }
    decisions = {
        row["report_id"]: row
        for row in all_final.values()
        if row["report_id"] in reference
    }
    expected_ids = set(load(archive / "reference" / "ledger.json")["items"])
    if set(decisions) != set(reference):
        raise ValueError("calibration IDs do not exactly close over the 444+106 reference rows")
    mismatches: list[dict[str, Any]] = []
    comparisons: dict[str, dict[str, Any]] = {}
    exact_da = exact_a0 = exact_kni = exact_relation = 0
    final_da = Counter()
    reference_da = Counter()
    for report_id, old in sorted(reference.items()):
        new = decisions[report_id]
        old_da = str(old["strict_da"])
        old_a0 = normalize(old["a0_type"])
        old_kni = str(old["corrected_kni"])
        new_da = str(new["strict_da"])
        new_a0 = normalize(new.get("a0_type"))
        new_kni = str(new["corrected_kni"])
        old_relations = reference_relation_map(old, expected_ids)
        new_relations = canonical_relation_map(new)
        da_match = new_da == old_da and new_a0 == old_a0
        kni_match = new_kni == old_kni
        relation_match = new_relations == old_relations
        comparisons[report_id] = {
            "reference_source": old["source"],
            "da_match": da_match,
            "a0_match": new_a0 == old_a0,
            "kni_match": kni_match,
            "relation_match": relation_match,
            "reference_da": old_da,
            "final_da": new_da,
        }
        exact_da += da_match
        exact_a0 += new_a0 == old_a0
        exact_kni += kni_match
        exact_relation += relation_match
        final_da[new_da] += 1
        reference_da[old_da] += 1
        if not (da_match and kni_match and relation_match):
            mismatches.append({
                "report_id": report_id,
                "reference_source": old["source"],
                "strict_da": {"reference": old_da, "final": new_da, "match": new_da == old_da},
                "a0_type": {"reference": old_a0, "final": new_a0, "match": new_a0 == old_a0},
                "corrected_kni": {"reference": old_kni, "final": new_kni, "match": kni_match},
                "relation": {"reference": old_relations, "final": new_relations, "match": relation_match},
                "disposition": "targeted reread recorded; final label remains the pane5 source-backed decision",
            })
    distribution_delta = {
        level: {
            "reference": ratio(reference_da[level], len(reference)),
            "final": ratio(final_da[level], len(reference)),
            "percentage_point_difference": (final_da[level] - reference_da[level]) / len(reference) * 100,
        }
        for level in ("D2", "D1", "D0", "A0")
    }
    final_by_id = all_final
    evidence_reads = {
        row["report_id"]: row
        for row in load(directory / "pane5_evidence_reads.json")["rows"]
    }

    def raw_target(report_id: str) -> dict[str, Any]:
        """Read one frozen report target for a sentinel check."""

        decision = final_by_id[report_id]
        raw_path = archive / decision["raw_method_path"]
        target = load(raw_path)
        for token in decision["raw_json_pointer"].strip("/").split("/"):
            target = target[int(token)] if isinstance(target, list) else target[token]
        if not isinstance(target, dict):
            raise ValueError(f"sentinel target is not an object: {report_id}")
        return target

    cruise_ids = ("0009:r1:issue:4", "0009:r2:issue:10", "0009:r3:issue:8")
    cruise_source = archive / "reference/x1v2_input_closure/pairs/llms_emp_feedback_final_0009/plantuml.puml"
    cruise_source_text = cruise_source.read_text(encoding="utf-8")
    cruise_sentinel = all(
        "dist_to_front>=25" in cruise_source_text
        and "dist_to_front>=25" in final_by_id[report_id]["reason"]
        and "dist_to_front>=25" in final_by_id[report_id]["basis"]
        and "transition:line:27" in raw_target(report_id).get("element_refs", [])
        and raw_target(report_id).get("predicate_id") == "S5"
        and raw_target(report_id).get("property") == "guard"
        for report_id in cruise_ids
    )
    reviewed_category_ids = (
        "0023:r1:issue:5", "0029:r1:issue:5", "0029:r2:issue:5", "0029:r3:issue:5",
        "0039:r1:issue:5", "0049:r1:issue:5", "0043:r3:issue:8", "0053:r2:issue:0",
    )
    category_sentinel = all(
        report_id in final_by_id
        and final_by_id[report_id]["review"].get("review_status") == "FINAL"
        and final_by_id[report_id]["review"].get("human_confirmation") is True
        and evidence_reads[report_id].get("raw_read") is True
        and evidence_reads[report_id].get("author_source_read") is True
        and bool(raw_target(report_id).get("property"))
        for report_id in reviewed_category_ids
    )
    sentinels = {
        "0003:r2:issue:2_separate_transition_endpoints": final_by_id["0003:r2:issue:2"].get("canonical_group_key", "").startswith("0003:transition_endpoints:"),
        "0014_four_reference_K_FULL_EIS_0014_01": all(
            final_by_id[report_id]["strict_da"] == "D2"
            and final_by_id[report_id]["corrected_kni"] == "K"
            and any(row["expected_id"] == "EIS-0014-01" and row["relation"] == "FULL_MATCH" for row in final_by_id[report_id]["relations"])
            for report_id in ("0014:r1:issue:14", "0014:r3:issue:4", "0014:r3:issue:5", "0014:r3:issue:15")
        ),
        "0006:r3:issue:0_no_uav_count_crosswire": not any(token in json.dumps(final_by_id["0006:r3:issue:0"], ensure_ascii=False).lower() for token in ("uav-count", "semantic_adjudication")),
        "0009_cruise_exact_guard_text": cruise_sentinel,
        "special_categories_remain_reviewed": category_sentinel,
    }
    targeted_document = load(directory / "pane5_targeted_re_review.json")
    targeted_ids = {
        str(row.get("report_id"))
        for row in targeted_document.get("rows", [])
        if isinstance(row, dict) and row.get("report_id")
    }

    def cohort_metrics(source_name: str, expected_size: int) -> dict[str, Any]:
        """Compute agreement and D/A distribution for one frozen reference cohort."""

        cohort_ids = [report_id for report_id, comparison in comparisons.items() if comparison["reference_source"] == source_name]
        final_counts = Counter(comparisons[report_id]["final_da"] for report_id in cohort_ids)
        reference_counts = Counter(comparisons[report_id]["reference_da"] for report_id in cohort_ids)
        return {
            "reference_source": source_name,
            "report_count": len(cohort_ids),
            "expected_report_count": expected_size,
            "agreement": {
                "strict_da_and_a0_type": ratio(sum(comparisons[report_id]["da_match"] for report_id in cohort_ids), len(cohort_ids)),
                "a0_type": ratio(sum(comparisons[report_id]["a0_match"] for report_id in cohort_ids), len(cohort_ids)),
                "corrected_kni": ratio(sum(comparisons[report_id]["kni_match"] for report_id in cohort_ids), len(cohort_ids)),
                "dense_relation": ratio(sum(comparisons[report_id]["relation_match"] for report_id in cohort_ids), len(cohort_ids)),
            },
            "distribution": {
                level: {
                    "reference": ratio(reference_counts[level], len(cohort_ids)),
                    "final": ratio(final_counts[level], len(cohort_ids)),
                    "percentage_point_difference": (final_counts[level] - reference_counts[level]) / len(cohort_ids) * 100,
                }
                for level in ("D2", "D1", "D0", "A0")
            },
        }

    cohort_names = {
        "frozen_n": ("reviews/12_v60_valid_novel_posthoc_reaudit.json", 444),
        "frozen_i": ("reviews/11_v60_invalid_manual_reaudit.tsv", 106),
    }
    cohorts = {name: cohort_metrics(source, size) for name, (source, size) in cohort_names.items()}
    targeted_closure = {
        "mismatch_ids": sorted(item["report_id"] for item in mismatches),
        "targeted_ids": sorted(targeted_ids),
        "mismatch_count": len(mismatches),
        "matched_mismatch_count": len({item["report_id"] for item in mismatches} & targeted_ids),
        "total_targeted_re_review_count": len(targeted_ids),
        "all_mismatches_targeted": all(item["report_id"] in targeted_ids for item in mismatches),
    }
    result = {
        "schema": "paper1.manual-adjudication.calibration.v2",
        "protocol_version": "issue-189-195-manual-evidence-v2",
        "status": "PASS" if exact_da / 550 >= 0.90 and exact_relation / 550 >= 0.90 and all(sentinels.values()) and targeted_closure["all_mismatches_targeted"] else "FAIL",
        "reference_rows": {"frozen_n": 444, "frozen_i": 106, "total": 550},
        "agreement": {
            "strict_da_and_a0_type": ratio(exact_da, 550),
            "a0_type": ratio(exact_a0, 550),
            "corrected_kni": ratio(exact_kni, 550),
            "dense_relation": ratio(exact_relation, 550),
        },
        "distribution": distribution_delta,
        "sentinels": sentinels,
        "mismatches": mismatches,
        "cohorts": cohorts,
        "targeted_re_review_closure": targeted_closure,
        "blind_review_policy": "The pane5 primary and independent subagent proposal were submitted with reference_visible=false and primary_visible=false; legacy rows were unblinded only for this comparison.",
        "basis": "reviews/12_v60_valid_novel_posthoc_reaudit.json, reviews/11_v60_invalid_manual_reaudit.tsv, canonical v60_report_decisions.json, and reference/ledger.json",
    }
    (directory / "calibration_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": result["status"], "strict_da": result["agreement"]["strict_da_and_a0_type"], "relation": result["agreement"]["dense_relation"], "mismatches": len(mismatches)}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
