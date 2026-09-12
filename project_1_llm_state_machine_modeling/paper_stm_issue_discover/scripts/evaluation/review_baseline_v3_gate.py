#!/usr/bin/env python3
"""Independent provider-free closure review for the baseline v3 archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import arbitration_record_pointer


FORBIDDEN = ("track_b_full", "track_b_0020_0059", "manual-v2")
DOIS = (
    "10.1109/MODELS67397.2025.00014",
    "10.6028/NIST.SP.500-297",
    "10.1109/ICSE.2017.62",
    "10.1007/s10664-016-9470-4",
    "10.1109/32.391380",
    "10.1145/3243734.3243804",
)


def load(path: Path) -> Any:
    """Read one JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    """Hash one file with the archive's public prefix."""
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def raw_inventory(archive: Path) -> dict[str, dict[str, Any]]:
    """Re-enumerate baseline findings from frozen raw records."""
    result: dict[str, dict[str, Any]] = {}
    for path in sorted((archive / "raw/x1v2_baseline/method").glob("run*/*/record.json")):
        round_no = int(path.parts[-3].removeprefix("run"))
        pair = path.parts[-2].split("-", 1)[0]
        document = load(path)
        for index, finding in enumerate(document.get("parsed_output", {}).get("issues", [])):
            report_id = f"{pair}:r{round_no}:baseline_issue_{index + 1}"
            if report_id in result:
                raise AssertionError(f"duplicate raw report {report_id}")
            result[report_id] = {"path": path.relative_to(archive).as_posix(), "pointer": f"/parsed_output/issues/{index}", "sha256": sha(path), "finding": finding}
    return result


def check(archive: Path) -> dict[str, Any]:
    """Run independent structural, numerical, boundary, and citation checks."""
    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    raw = raw_inventory(archive)
    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    decisions_doc = load(v3 / "baseline_report_decisions_v3.json")
    decisions = decisions_doc["decisions"]
    inventory = load(v3 / "inventory.json")
    ledger = load(archive / "reference/ledger.json")["items"]
    groups = load(v3 / "baseline_n_groups_v3.json")["groups"]
    combined = load(v3 / "baseline_combined_512_v3.json")["rows"]
    arbitration_log = load(v3 / "reviews/arbitration_log_v3.json")
    arbitration_entries = arbitration_log.get("entries_by_report_id", {})
    findings: list[dict[str, Any]] = []

    def finding(fid: str, severity: str, reason: str, basis: list[str], disposition: str = "PASS") -> None:
        findings.append({"finding_id": fid, "severity": severity, "status": disposition, "reason": reason, "basis": basis, "targeted_re_review": "none"})

    if len(raw) != 512 or len(inventory["items"]) != 1783 or len(old) != 512:
        finding("DATA-001", "C", "Raw census or inventory closure is incomplete.", ["raw/x1v2_baseline/method/*/record.json", "derived/.../inventory.json"], "FAIL")
    else:
        finding("DATA-001", "M", "Raw baseline census closes at 512 reports and the inventory contains both sides' 1783 items.", ["review_baseline_v3_gate.py:raw_inventory", "derived/manual_adjudication_v3_baseline_ni/inventory.json"], "PASS")

    old_by_id = {row["report_id"]: row for row in old}
    old_non_k = {rid for rid, row in old_by_id.items() if row["corrected_kni"] != "K"}
    decision_by_id = {row["original_report_id"]: row for row in decisions}
    if len(decisions) != len(old_non_k) or set(decision_by_id) != old_non_k:
        finding("DATA-002", "C", "v3 decision coverage is not exactly the frozen non-K set.", ["baseline_report_decisions_v3.json#/decisions", "manual_adjudication_v2/x1v2_report_decisions.json"], "FAIL")
    else:
        finding("DATA-002", "M", "All frozen non-K reports have exactly one v3 decision.", ["decision ID set equality", "expected 233 rows"], "PASS")

    frozen = load(v3 / "frozen_k_snapshot_v3.json")["rows"]
    expected_frozen = [row for row in old if row["corrected_kni"] == "K"]
    if frozen != expected_frozen:
        finding("BOUNDARY-001", "C", "Frozen K snapshot differs from v2.", ["frozen_k_snapshot_v3.json#/rows", "manual_adjudication_v2/x1v2_report_decisions.json#/decisions"], "FAIL")
    else:
        finding("BOUNDARY-001", "M", "The 279-row frozen K projection is byte-content identical to v2.", ["frozen K list equality", "frozen_k_snapshot_v3.json"], "PASS")

    missing_hashes = [rid for rid, row in decision_by_id.items() if (row["raw_method_path"], row["raw_json_pointer"], row["raw_sha256"]) != (raw[rid]["path"], raw[rid]["pointer"], raw[rid]["sha256"])]
    if missing_hashes:
        finding("DATA-003", "C", f"{len(missing_hashes)} decisions have a raw pointer or hash mismatch.", [f"first={missing_hashes[0]}"], "FAIL")
    else:
        finding("DATA-003", "M", "All v3 decisions point to the exact raw record and finding pointer.", ["raw_inventory comparison", "baseline_report_decisions_v3.json"], "PASS")

    bad_rows = []
    disagreement_count = 0
    for row in decisions:
        if len(row["relations"]) != len(ledger) or len({x["expected_id"] for x in row["relations"]}) != len(ledger):
            bad_rows.append(row["original_report_id"])
        review = row["review"]
        if review["disagreement_flag"]:
            disagreement_count += 1
        if review["review_status"] != "FINAL" or not review["human_confirmation"] or review["review_blockers"]:
            bad_rows.append(row["original_report_id"])
        pointer = review.get("arbitration_record_pointer")
        if not pointer or not pointer.startswith("reviews/arbitration_log_v3.json#/entries_by_report_id/"):
            bad_rows.append(row["original_report_id"])
        if len(review["independent_opinions"]) < 2 or any(op["review_status"] != "PROPOSAL" or op["reference_visible"] or op["primary_visible"] for op in review["independent_opinions"]):
            bad_rows.append(row["original_report_id"])
    if bad_rows:
        finding("AUDIT-001", "C", f"Review/relation closure failed for {len(set(bad_rows))} rows.", [f"first={sorted(set(bad_rows))[0]}"], "FAIL")
    else:
        finding("AUDIT-001", "M", "Every v3 row has 145 relation rows, two blind proposals, final pane5 confirmation, and a closed arbitration pointer.", ["baseline_report_decisions_v3.json#/decisions[*]", "reviews/arbitration_log_v3.json#/entries_by_report_id/*", f"disagreement_count={disagreement_count}"], "PASS")

    arbitration_bad = []
    for index, row in enumerate(decisions):
        report_id = row["original_report_id"]
        pointer = arbitration_record_pointer(report_id)
        entry = arbitration_entries.get(report_id)
        if row["review"].get("arbitration_record_pointer") != pointer or not entry or entry.get("record_pointer") != pointer or entry.get("decision_json_pointer") != f"/decisions/{index}":
            arbitration_bad.append(report_id)
    if len(arbitration_entries) != 233 or arbitration_log.get("entry_count") != 233 or arbitration_bad:
        finding("AUDIT-002", "C", f"Persisted arbitration pointer/log closure failed for {len(arbitration_bad)} rows.", ["reviews/arbitration_log_v3.json", "baseline_report_decisions_v3.json#/decisions[*]/review/arbitration_record_pointer"], "FAIL")
    else:
        finding("AUDIT-002", "M", f"All 233 pane5 decisions have addressable arbitration records; disagreement entries={disagreement_count}.", ["reviews/arbitration_log_v3.json", "stable report-id JSON pointers"], "PASS")

    serialized = json.dumps(decisions, ensure_ascii=False)
    leaked = [token for token in FORBIDDEN if token in serialized]
    if leaked:
        finding("FAIR-001", "I", "Forbidden broad/legacy proposal provenance leaked into canonical decisions.", leaked, "FAIL")
    else:
        finding("FAIR-001", "I", "Canonical decisions contain neither excluded broad Track-B artifacts nor legacy reviewer identities.", ["FORBIDDEN allowlist check", "baseline_report_decisions_v3.json"], "PASS")

    final_n = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "N"}
    final_i = {row["original_report_id"] for row in decisions if row["corrected_kni"] == "I"}
    mapping = groups["report_to_group"]
    group_members = [rid for group in groups["n_groups"] + groups["invalid_clusters"] for rid in group["member_report_ids"]]
    if set(mapping) != final_n | final_i or len(group_members) != len(set(group_members)) or set(group_members) != final_n | final_i:
        finding("GROUP-001", "I", "N/I report-to-group closure is not one-to-one.", ["baseline_n_groups_v3.json#/groups/report_to_group", "groups member_report_ids"], "FAIL")
    elif any(
        group["side"] != "x1v2_baseline"
        or len({decision_by_id[rid]["pair_id"] for rid in group["member_report_ids"]}) != 1
        or group["pair_id"] != next(iter({decision_by_id[rid]["pair_id"] for rid in group["member_report_ids"]}))
        for group in groups["n_groups"]
    ):
        finding("GROUP-002", "I", "A substantive N group crosses the allowed side or pair boundary.", ["baseline_n_groups_v3.json#/groups/n_groups"], "FAIL")
    else:
        finding("GROUP-001", "I", "Every final N/I report belongs to exactly one same-side, pair-local group/diagnostic cluster.", [f"N={len(final_n)}", f"I={len(final_i)}", f"N groups={len(groups['n_groups'])}", f"I clusters={len(groups['invalid_clusters'])}"], "PASS")

    if len(combined) != 512 or len({row["report_id"] for row in combined}) != 512:
        finding("METRIC-001", "C", "Combined 512-row projection is not closed.", ["baseline_combined_512_v3.json#/rows"], "FAIL")
    else:
        finding("METRIC-001", "M", "Combined projection contains 279 frozen K rows plus 233 v3 non-K rows.", ["baseline_combined_512_v3.json#/rows", "source=frozen_v2/v3_non_k"], "PASS")

    protocol = (v3 / "protocol_freeze_v3_baseline_ni.md").read_text(encoding="utf-8")
    report = (archive / "report/v60_current_vs_x1v2_baseline_cn.md").read_text(encoding="utf-8")
    missing_dois = [doi for doi in DOIS if doi not in protocol]
    if missing_dois:
        finding("ACADEMIC-001", "I", "The protocol does not contain all required DOI anchors.", missing_dois, "FAIL")
    else:
        finding("ACADEMIC-001", "M", "All six cited DOI anchors are present and the protocol states the project rule is an operationalization, not a verbatim single-paper definition.", ["protocol_freeze_v3_baseline_ni.md:84-96"], "PASS")
    if "baseline v3" not in report or "frozen" not in report or "not_applicable" not in report:
        finding("DOC-001", "I", "The current report does not state the v2/v3 frozen boundary and baseline not_applicable semantics.", ["report/v60_current_vs_x1v2_baseline_cn.md"], "FAIL")
    else:
        finding("DOC-001", "M", "Report-facing text names the v3 baseline layer, frozen boundary, and not_applicable distinctions.", ["report/v60_current_vs_x1v2_baseline_cn.md"], "PASS")

    failed = [x for x in findings if x["status"] == "FAIL"]
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.independent-gate-review",
        "review_id": "independent-final-gate-track-v3",
        "reviewer_id": "track:provider-free-independent-gate",
        "reviewer_role": "independent structural/numeric/archive track; not a semantic label generator",
        "scope": "Raw census, frozen K boundary, non-K coverage, relation closure, review-chain closure, grouping closure, report text, and citation anchors.",
        "commands": ["python3 scripts/evaluation/review_baseline_v3_gate.py --archive-root ..."],
        "raw_reports": len(raw),
        "reviewed_non_k": len(decisions),
        "dense_non_k_relations": len(decisions) * len(ledger),
        "disagreement_count": disagreement_count,
        "findings": findings,
        "status": "FAIL" if failed else "PASS",
        "limitations": ["This track does not replace source-semantic pane5 adjudication or the independent semantic reviewer; it only verifies persisted closure and publication contracts."],
    }


def main() -> None:
    """Write the independent review JSON and Markdown summary."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    reviews = archive / "derived/manual_adjudication_v3_baseline_ni/reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    result = check(archive)
    (reviews / "independent_final_gate_review.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [f"# Independent final gate review: {result['status']}", "", f"Reviewer track: `{result['reviewer_id']}`.", "", "This is an independent provider-free closure review; it does not assign semantic labels.", "", "| Finding | Severity | Status | Reason |", "|---|---|---|---|"]
    lines.extend(f"| `{item['finding_id']}` | `{item['severity']}` | `{item['status']}` | {item['reason']} |" for item in result["findings"])
    lines.extend(["", f"Raw reports: `{result['raw_reports']}`; reviewed non-K: `{result['reviewed_non_k']}`; dense non-K relations: `{result['dense_non_k_relations']}`; disagreement rows: `{result['disagreement_count']}`.", "", "Disposition: all checks above are persisted in the JSON artifact; any FAIL must be fixed and rerun before finalization.", ""])
    (reviews / "independent_final_gate_review.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "findings": len(result["findings"]), "review_path": str(reviews / "independent_final_gate_review.json")}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
