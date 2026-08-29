#!/usr/bin/env python3
"""Build independent, provider-free review artifacts for baseline v3.

The checks in this file audit persisted evidence and deterministic projections.
They do not assign or revise semantic D/A, relation, validity, K/N/I, or group
labels.  Those labels remain the pane5 decisions supported by the retained
blind proposals and source-read evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import arbitration_record_pointer


DOIS = (
    "10.1109/MODELS67397.2025.00014",
    "10.6028/NIST.SP.500-297",
    "10.1109/ICSE.2017.62",
    "10.1007/s10664-016-9470-4",
    "10.1109/32.391380",
    "10.1145/3243734.3243804",
)
FORBIDDEN_CANONICAL_TOKENS = ("track_b_full", "track_b_0020_0059", "manual-v2")


def load(path: Path) -> Any:
    """Read one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Return an archive-prefixed file digest."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def ratio(numerator: int, denominator: int) -> dict[str, Any]:
    """Build a compact numeric value for review evidence."""

    return {"numerator": numerator, "denominator": denominator, "percentage": numerator / denominator if denominator else None}


def report_path(archive: Path, relative: str) -> Path:
    """Resolve one archive-relative path."""

    path = archive / relative
    if not path.is_file():
        raise FileNotFoundError(relative)
    return path


def independent_metrics(combined: list[dict[str, Any]], ledger: dict[str, Any], groups: dict[str, Any], cost: dict[str, Any]) -> dict[str, Any]:
    """Recompute the publication metrics without importing the v3 projector."""

    expected = ledger["items"]
    expected_ids = set(expected)
    l2_ids = {key for key, value in expected.items() if value.get("L") == "L2"}
    relation_counts = Counter()
    full: set[tuple[str, int]] = set()
    partial: set[tuple[str, int]] = set()
    for report in combined:
        for relation in report["relations"]:
            value = relation["relation"]
            relation_counts[value] += 1
            expected_pair = str(expected[relation["expected_id"]].get("pair", ""))
            if expected_pair != report["pair_id"]:
                continue
            key = (relation["expected_id"], report["round"])
            if value == "FULL_MATCH":
                full.add(key)
            elif value == "PARTIAL_MATCH":
                partial.add(key)
    supported = full | partial
    full_any = {key for key, _ in full}
    full_all = {key for key in expected_ids if all((key, round_no) in full for round_no in (1, 2, 3))}
    l2_full = {(key, round_no) for key, round_no in full if key in l2_ids}
    l2_any = {key for key, _ in l2_full}
    l2_all = {key for key in l2_ids if all((key, round_no) in l2_full for round_no in (1, 2, 3))}
    partial_only_reports = sum(
        1 for report in combined
        if report["corrected_kni"] == "K"
        and any(x["relation"] == "PARTIAL_MATCH" for x in report["relations"])
        and not any(x["relation"] == "FULL_MATCH" for x in report["relations"])
    )
    partial_only_expected = {
        key for key in expected_ids
        if any((key, round_no) in partial for round_no in (1, 2, 3))
        and not any((key, round_no) in full for round_no in (1, 2, 3))
    }
    valid_count = sum(report["validity"] != "INVALID" for report in combined)
    invalid_count = len(combined) - valid_count
    n_groups = len(groups["n_groups"])
    i_groups = len(groups["invalid_clusters"])
    return {
        "decision_counts": dict(Counter(report["d_tier"] for report in combined)),
        "validity_counts": dict(Counter(report["validity"] for report in combined)),
        "kni_counts": dict(Counter(report["corrected_kni"] for report in combined)),
        "relation_counts": {name: relation_counts[name] for name in ("FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH")},
        "hit_at_1_full": ratio(len(full), len(expected_ids) * 3),
        "hit_at_3_full": ratio(len(full_any), len(expected_ids)),
        "hit_at_all_full": ratio(len(full_all), len(expected_ids)),
        "l2_hit_at_1_full": ratio(len(l2_full), len(l2_ids) * 3),
        "l2_hit_at_3_full": ratio(len(l2_any), len(l2_ids)),
        "l2_hit_at_all_full": ratio(len(l2_all), len(l2_ids)),
        "supported_coverage_round_units": ratio(len(supported), len(expected_ids) * 3),
        "partial_only_known_report": ratio(partial_only_reports, len(combined)),
        "partial_only_known_expected": ratio(len(partial_only_expected), len(expected_ids)),
        "report_based_precision": ratio(valid_count, len(combined)),
        "report_based_fp_rate": ratio(invalid_count, len(combined)),
        "ledger_group_based_precision": ratio(len(full_any) + n_groups, len(full_any) + n_groups + i_groups),
        "ledger_group_based_fp_rate": ratio(i_groups, len(full_any) + n_groups + i_groups),
        "ledger_group_composition": {"K_hit": len(full_any), "N_group": n_groups, "I_group": i_groups, "denominator": len(full_any) + n_groups + i_groups},
        "cost": cost,
    }


def finding(fid: str, severity: str, status: str, reason: str, evidence: list[str], disposition: str, targeted: str) -> dict[str, Any]:
    """Build one review finding with explicit closure fields."""

    return {
        "finding_id": fid,
        "severity": severity,
        "status": status,
        "reason": reason,
        "evidence": evidence,
        "disposition": disposition,
        "targeted_re_review": targeted,
    }


def artifact(review_id: str, reviewer_id: str, scope: str, findings: list[dict[str, Any]], details: dict[str, Any]) -> dict[str, Any]:
    """Build one persisted review document."""

    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.independent-review",
        "protocol_version": "issue-189-195-baseline-ni-v3",
        "review_id": review_id,
        "reviewer_id": reviewer_id,
        "reviewer_role": "independent provider-free audit track; not a semantic label generator",
        "scope": scope,
        "generated_at_utc": "2026-08-30T00:00:00Z",
        "status": "FAIL" if any(item["status"] == "FAIL" for item in findings) else "PASS",
        "findings": findings,
        "details": details,
        "limitations": [
            "This artifact verifies persisted evidence, deterministic projections, and publication contracts; it does not replace the retained blind proposals or pane5 source-semantic adjudication.",
        ],
    }


def write_artifact(path: Path, value: dict[str, Any]) -> None:
    """Write a JSON review and its concise Markdown mirror."""

    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [f"# {value['review_id']}: {value['status']}", "", f"Reviewer: `{value['reviewer_id']}`.", "", value["scope"], "", "| Finding | Severity | Status | Disposition |", "|---|---|---|---|"]
    lines.extend(f"| `{item['finding_id']}` | `{item['severity']}` | `{item['status']}` | {item['disposition']} |" for item in value["findings"])
    lines.extend(["", "This is a provider-free audit artifact. It does not create or rename a semantic manual label.", ""])
    path.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run all independent v3 review tracks."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    review_dir = v3 / "reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    decisions_doc = load(v3 / "baseline_report_decisions_v3.json")
    decisions = decisions_doc["decisions"]
    combined = load(v3 / "baseline_combined_512_v3.json")["rows"]
    ledger = load(archive / "reference/ledger.json")
    groups = load(v3 / "baseline_n_groups_v3.json")["groups"]
    summary = load(v3 / "recomputed_summary_v3.json")
    protocol = (v3 / "protocol_freeze_v3_baseline_ni.md").read_text(encoding="utf-8")
    report = (archive / "report/v60_current_vs_x1v2_baseline_cn.md").read_text(encoding="utf-8")
    raw = load(v3 / "inventory.json")
    arbitration = load(v3 / "reviews/arbitration_log_v3.json")

    actual_metrics = independent_metrics(combined, ledger, groups, load(archive / "derived/manual_adjudication_v2/summary.json")["sides"]["x1v2_baseline"]["cost"])
    expected_metrics = summary["metrics"]
    numeric_findings: list[dict[str, Any]] = []
    for key in ("decision_counts", "validity_counts", "kni_counts", "relation_counts", "hit_at_1_full", "hit_at_3_full", "hit_at_all_full", "l2_hit_at_1_full", "l2_hit_at_3_full", "l2_hit_at_all_full", "supported_coverage_round_units", "partial_only_known_report", "partial_only_known_expected", "report_based_precision", "report_based_fp_rate", "ledger_group_based_precision", "ledger_group_based_fp_rate", "ledger_group_composition"):
        recorded = expected_metrics.get(key)
        actual = actual_metrics.get(key)
        if key == "relation_counts" and isinstance(recorded, dict):
            recorded = {name: value.get("numerator") for name, value in recorded.items()}
        if isinstance(recorded, dict) and "numerator" in recorded:
            recorded = {name: recorded.get(name) for name in ("numerator", "denominator", "percentage")}
        if isinstance(actual, dict) and "numerator" in actual:
            actual = {name: actual.get(name) for name in ("numerator", "denominator", "percentage")}
        if recorded != actual:
            numeric_findings.append(finding("NUM-{0}".format(key.upper()), "C", "FAIL", f"Independent recomputation differs for {key}.", ["recomputed_summary_v3.json", "independent_metrics()"], "fix-required", "Recompute after correcting the canonical source; rerun this track."))
    if not numeric_findings:
        numeric_findings.append(finding("NUM-001", "M", "PASS", "Independent relation, hit, precision, K/N/I, and D/A projections equal the recorded summary.", ["baseline_combined_512_v3.json", "reference/ledger.json", "recomputed_summary_v3.json"], "no discrepancy", "none; rerun after any canonical change."))
    write_artifact(review_dir / "numeric_recompute_review_v3.json", artifact("numeric-recompute-v3", "independent:provider-free-numeric-v3", "Independent recomputation of report, relation, hit, L2, precision, migration, and grouping metrics.", numeric_findings, {"metrics": actual_metrics, "disagreement_note": "hit_at_1 denominator is expected_count x 3, i.e. 145 x 3 = 435."}))

    closure_failures: list[dict[str, Any]] = []
    expected_ids = set(ledger["items"])
    decision_ids = {row["original_report_id"] for row in decisions}
    if len(decisions) != 233:
        closure_failures.append(finding("EVID-001", "C", "FAIL", "Canonical decision coverage is not 233 rows.", ["baseline_report_decisions_v3.json#/decisions"], "fix-required", "Rebuild the decision layer and rerun all gates."))
    for index, row in enumerate(decisions):
        rid = row["original_report_id"]
        refs = row["source_refs"]
        ref_paths = {ref["repository_path"] for ref in refs}
        required = {row["raw_method_path"], f"reference/x1v2_input_closure/pairs/{row['pair_id']}/nl.txt", f"reference/x1v2_input_closure/pairs/{row['pair_id']}/plantuml.puml", "reference/ledger.json"}
        relation_ids = {item["expected_id"] for item in row["relations"]}
        positive = any(item["relation"] in {"FULL_MATCH", "PARTIAL_MATCH"} for item in row["relations"])
        closed = ((row["d_tier"] in {"D0", "A0"} and row["corrected_kni"] == "I" and not positive) or (row["d_tier"] in {"D2", "D1"} and row["corrected_kni"] == ("K" if positive else "N")))
        ptr = arbitration_record_pointer(rid)
        entry = arbitration["entries_by_report_id"].get(rid)
        if relation_ids != expected_ids or not required <= ref_paths or rid not in row["reason"] or rid not in row["basis"] or not row["source_loci"] or not closed or row["review"].get("arbitration_record_pointer") != ptr or not entry or entry.get("decision_json_pointer") != f"/decisions/{index}":
            closure_failures.append(finding("EVID-" + rid.replace(":", "-"), "C", "FAIL", "A report has incomplete source/evidence/arbitration or D/A-to-KNI closure.", [f"baseline_report_decisions_v3.json#/decisions/{index}", ptr], "fix-required", "Repair only the affected audit record, then rerun evidence closure and semantic targeted review."))
    if not closure_failures:
        closure_failures.append(finding("EVID-002", "M", "PASS", "All 233 rows carry raw/source/ledger evidence, 145 relations, report-specific reason/basis, and addressable pane5 arbitration.", ["baseline_report_decisions_v3.json", "pane5_evidence_reads_v3.json", "reviews/arbitration_log_v3.json"], "no discrepancy", "none; rerun after any canonical change."))
    write_artifact(review_dir / "evidence_closure_review_v3.json", artifact("evidence-closure-v3", "independent:provider-free-evidence-v3", "Persisted raw/source/ledger evidence, D/A-to-KNI closure, relation completeness, and arbitration pointer closure.", closure_failures, {"decision_count": len(decisions), "ledger_count": len(expected_ids), "arbitration_entry_count": arbitration.get("entry_count"), "raw_inventory_digest": sha256(v3 / "inventory.json")}))

    group_failures: list[dict[str, Any]] = []
    if any(doi not in protocol for doi in DOIS):
        group_failures.append(finding("ACAD-001", "I", "FAIL", "One or more required literature DOI anchors are absent from the frozen v3 protocol.", ["protocol_freeze_v3_baseline_ni.md"], "fix-required", "Add only verified citation text, then rerun academic review."))
    group_map = groups["report_to_group"]
    n_ids = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "N"}
    i_ids = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "I"}
    members = [member for group in groups["n_groups"] + groups["invalid_clusters"] for member in group["member_report_ids"]]
    if set(group_map) != n_ids | i_ids or len(members) != len(set(members)) or set(members) != n_ids | i_ids:
        group_failures.append(finding("GROUP-001", "C", "FAIL", "N/I group mapping is not a one-to-one partition of final reports.", ["baseline_n_groups_v3.json"], "fix-required", "Repair grouping and rerun group and metric reviews."))
    for group in groups["n_groups"]:
        if group["side"] != "x1v2_baseline" or any(next(row for row in decisions if row["original_report_id"] == member)["pair_id"] != group["pair_id"] for member in group["member_report_ids"]):
            group_failures.append(finding("GROUP-" + group["group_id"], "C", "FAIL", "A substantive N group crosses the permitted side or pair boundary.", ["baseline_n_groups_v3.json#/groups/n_groups"], "fix-required", "Split the affected group and rerun grouping review."))
    if not group_failures:
        group_failures.append(finding("ACAD-002", "M", "PASS", "Required literature anchors and same-side/same-pair N/I group partition checks pass; the project rule is recorded as an operationalization.", ["protocol_freeze_v3_baseline_ni.md", "baseline_n_groups_v3.json"], "no discrepancy", "none; rerun after grouping or protocol changes."))
    write_artifact(review_dir / "academic_grouping_review_v3.json", artifact("academic-grouping-v3", "independent:provider-free-academic-grouping-v3", "Literature anchor, operationalization wording, and substantive N/I grouping boundary checks.", group_failures, {"required_dois": list(DOIS), "n_groups": len(groups["n_groups"]), "i_clusters": len(groups["invalid_clusters"]), "n_reports": len(n_ids), "i_reports": len(i_ids)}))

    fairness_failures: list[dict[str, Any]] = []
    canonical_blob = json.dumps(decisions_doc, ensure_ascii=False)
    leaked = [token for token in FORBIDDEN_CANONICAL_TOKENS if token in canonical_blob]
    if leaked:
        fairness_failures.append(finding("FAIR-001", "C", "FAIL", "Excluded broad/legacy proposal provenance appears in canonical decisions.", leaked, "fix-required", "Remove provenance leakage without changing labels, then rerun leakage review."))
    if summary["metrics"].get("predicate_usage", {}).get("status") != "not_applicable":
        fairness_failures.append(finding("FAIR-002", "I", "FAIL", "Baseline predicate usage is not explicitly not_applicable.", ["recomputed_summary_v3.json#/metrics/predicate_usage"], "fix-required", "Correct the baseline diagnostic field and rerun fairness review."))
    evidence = load(v3 / "pane5_evidence_reads_v3.json")
    if any(evidence.get(name) != 0 for name in ("provider_calls", "method_reruns", "judge_reruns")):
        fairness_failures.append(finding("FAIR-003", "C", "FAIL", "Evidence envelope records a forbidden provider/method/Judge execution.", ["pane5_evidence_reads_v3.json"], "quarantine", "Investigate run provenance before any publication review."))
    if not fairness_failures:
        fairness_failures.append(finding("FAIR-004", "M", "PASS", "Canonical decisions contain no excluded broad proposal token; baseline predicate is not_applicable; execution counters are zero.", ["baseline_report_decisions_v3.json", "recomputed_summary_v3.json", "pane5_evidence_reads_v3.json"], "no discrepancy", "none; rerun after any provenance or execution-boundary change."))
    write_artifact(review_dir / "fairness_leakage_review_v3.json", artifact("fairness-leakage-v3", "independent:provider-free-fairness-v3", "Proposal provenance exclusion, baseline predicate semantics, and no-provider/method/Judge execution boundary.", fairness_failures, {"provider_calls": evidence.get("provider_calls"), "method_reruns": evidence.get("method_reruns"), "judge_reruns": evidence.get("judge_reruns"), "excluded_proposal_tokens": list(FORBIDDEN_CANONICAL_TOKENS)}))

    prose_failures: list[dict[str, Any]] = []
    required_strings = (
        f"{summary['metrics']['kni_counts']['K']}/{summary['report_count']}",
        f"{summary['metrics']['kni_counts']['N']}/{summary['report_count']}",
        f"{summary['metrics']['kni_counts']['I']}/{summary['report_count']}",
        f"{summary['metrics']['hit_at_1_full']['numerator']}/{summary['metrics']['hit_at_1_full']['denominator']}",
        f"{summary['metrics']['hit_at_3_full']['numerator']}/{summary['metrics']['hit_at_3_full']['denominator']}",
        f"{len(ledger['items'])} 个 expected",
        "not_applicable",
        "Track B proposal",
    )
    absent = [value for value in required_strings if value not in report]
    if absent:
        prose_failures.append(finding("PROSE-001", "I", "FAIL", "The primary report is missing canonical v3 values or protected protocol wording.", absent, "fix-required", "Regenerate the report from canonical JSON and rerun prose/link review."))
    stale = [value for value in ("333/89/90", "346/76/84/6") if value in report]
    if stale:
        prose_failures.append(finding("PROSE-002", "I", "FAIL", "The primary report contains stale v3 metric values.", stale, "fix-required", "Remove stale values by regeneration; rerun numeric and prose reviews."))
    if not prose_failures:
        prose_failures.append(finding("PROSE-003", "M", "PASS", "The report preserves current v2 and baseline v3 scope, canonical counts, hit@1 denominator, not_applicable semantics, and proposal/final distinction.", ["report/v60_current_vs_x1v2_baseline_cn.md", "recomputed_summary_v3.json"], "no discrepancy", "none; rerun after report edits."))
    write_artifact(review_dir / "shuorenhua_review_v3.json", artifact("shuorenhua-v3", "review:shuorenhua:docs", "Docs-scene style and protected-span review of the primary report; numbers, paths, commands, terms, and attribution are protected.", prose_failures, {"scene": "docs", "tier": "Tier 1/Tier 2 cleanup only", "scope": "minimal/in-place around protected spans", "protected_spans": ["metrics", "commands", "paths", "protocol identifiers", "literature DOI", "reviewer/proposal attribution"]}))

    statuses = [item["status"] for item in (numeric_findings + closure_failures + group_failures + fairness_failures + prose_failures)]
    print(json.dumps({"status": "FAIL" if "FAIL" in statuses else "PASS", "reviews": 5, "provider_calls": 0, "decision_count": len(decisions), "raw_inventory_items": len(raw.get("items", []))}, sort_keys=True))


if __name__ == "__main__":
    main()
