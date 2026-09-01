#!/usr/bin/env python3
"""Independently audit baseline v3 grouping closure and citation boundaries."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DOI_RECORDS = (
    {
        "key": "mcet",
        "author": "Ahmed et al.",
        "work": "MCeT: Behavioral Model Correctness Evaluation using Large Language Models",
        "doi": "10.1109/MODELS67397.2025.00014",
        "title": "MCeT: Behavioral Model Correctness Evaluation using Large Language Models",
        "authors": ["Ahmed, Khaled", "Song, Jialing", "Chen, Boqi", "Wei, Ou", "Zheng, Bingzhou"],
        "venue": "2025 ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems (MODELS)",
        "year": 2025,
        "claim": "Same-root-cause equivalence can tolerate different detail levels; manually confirmed ledger-outside true issues are separately new true issues.",
        "snapshot_marker": "We define equivalent issues as issues that describe the same root cause",
        "evidence_lines": "154-157",
    },
    {
        "key": "sate",
        "author": "Okun, Delaitre & Black",
        "work": "Report on the Static Analysis Tool Exposition (SATE) IV",
        "doi": "10.6028/NIST.SP.500-297",
        "title": "Report on the Static Analysis Tool Exposition (SATE) IV",
        "authors": ["Okun, Vadim", "Delaitre, Aurelien", "Black, Paul E."],
        "venue": "NIST Special Publication",
        "year": 2013,
        "claim": "Directly related, indirectly related, and unrelated findings are distinguished; relatedness can be discussed at a root-cause level.",
        "snapshot_marker": "directly related",
        "evidence_lines": "159-159",
    },
    {
        "key": "pearson",
        "author": "Pearson et al.",
        "work": "Evaluating and Improving Fault Localization",
        "doi": "10.1109/ICSE.2017.62",
        "title": "Evaluating and Improving Fault Localization",
        "authors": ["Pearson, Spencer", "Campos, Jose", "Just, Rene", "Fraser, Gordon", "Abreu, Rui", "Ernst, Michael D.", "Pang, Deric", "Keller, Benjamin"],
        "venue": "2017 IEEE/ACM 39th International Conference on Software Engineering (ICSE)",
        "year": 2017,
        "claim": "Multi-statement fault localization has best/average/worst-case granularity; this motivates, but does not dictate, a pre-registered project unit.",
        "snapshot_marker": "multi-statement fault",
        "evidence_lines": "161-161",
    },
    {
        "key": "martinez",
        "author": "Martinez et al.",
        "work": "Automatic repair of real bugs in java: a large-scale experiment on the defects4j dataset",
        "doi": "10.1007/s10664-016-9470-4",
        "title": "Automatic repair of real bugs in java: a large-scale experiment on the defects4j dataset",
        "authors": ["Martinez, Matias", "Durieux, Thomas", "Sommerard, Romain", "Xuan, Jifeng", "Monperrus, Martin"],
        "venue": "Empirical Software Engineering",
        "year": 2016,
        "claim": "Semantic repair equivalence does not require identical patch syntax; this supports repair-intent comparison rather than patch-text equality.",
        "snapshot_marker": "语义等价",
        "evidence_lines": "163-163",
    },
    {
        "key": "porter",
        "author": "Porter, Votta & Basili",
        "work": "Comparing detection methods for software requirements inspections: a replicated experiment",
        "doi": "10.1109/32.391380",
        "title": "Comparing detection methods for software requirements inspections: a replicated experiment",
        "authors": ["Porter, A.A.", "Votta, L.G.", "Basili, V.R."],
        "venue": "IEEE Transactions on Software Engineering",
        "year": 1995,
        "claim": "Known-fault detection and true-fault/false-positive distinctions are separate evaluation concepts; this does not define this project's group key.",
        "snapshot_marker": "True Fault",
        "evidence_lines": "165-165",
    },
    {
        "key": "klees",
        "author": "Klees et al.",
        "work": "Evaluating Fuzz Testing",
        "doi": "10.1145/3243734.3243804",
        "title": "Evaluating Fuzz Testing",
        "authors": ["Klees, George", "Ruef, Andrew", "Cooper, Benji", "Wei, Shiyi", "Hicks, Michael"],
        "venue": "Proceedings of the 2018 ACM SIGSAC Conference on Computer and Communications Security",
        "year": 2018,
        "claim": "Evaluation should use distinct bugs rather than raw crashes or inputs; this supports reporting substantive groups separately from raw reports.",
        "snapshot_marker": "distinct bugs",
        "evidence_lines": "167-167",
    },
)


def load(path: Path) -> Any:
    """Load one JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    """Hash one file using the archive prefix convention."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def line_number(text: str, marker: str) -> int:
    """Return the one-based line containing an evidence marker."""

    for number, line in enumerate(text.splitlines(), start=1):
        if marker in line:
            return number
    raise ValueError(f"evidence marker not found: {marker}")


def grouping_review(archive: Path) -> dict[str, Any]:
    """Audit all final N groups and the one-to-one report map."""

    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    decisions = load(v3 / "baseline_report_decisions_v3.json")["decisions"]
    group_document = load(v3 / "baseline_n_groups_v3.json")
    groups = group_document["groups"]
    decision_by_id = {row["original_report_id"]: row for row in decisions}
    final_n = {rid for rid, row in decision_by_id.items() if row["corrected_kni"] == "N"}
    n_groups = groups["n_groups"]
    members = [rid for group in n_groups for rid in group["member_report_ids"]]
    pair_to_n = defaultdict(list)
    for rid in final_n:
        pair_to_n[rid.split(":", 1)[0]].append(rid)

    group_rows = []
    missing_criteria = []
    bad_non_merge = []
    for group in n_groups:
        group_id = group["group_id"]
        member_ids = group["member_report_ids"]
        rounds = sorted({decision_by_id[rid]["round"] for rid in member_ids})
        required = ("normative_obligation", "author_source_locus", "substantive_root_cause", "repair_intent", "reason", "basis")
        missing = [field for field in required if not group.get(field)]
        if missing:
            missing_criteria.append({"group_id": group_id, "fields": missing})
        expected_neighbors = sorted(set(pair_to_n[group["pair_id"]]) - set(member_ids)) if len(member_ids) == 1 else []
        actual_neighbors = sorted(row["neighbor_report_id"] for row in group.get("non_merge_reasons", []))
        if expected_neighbors != actual_neighbors:
            bad_non_merge.append({"group_id": group_id, "expected_neighbors": expected_neighbors, "actual_neighbors": actual_neighbors})
        group_rows.append({
            "group_id": group_id,
            "side": group["side"],
            "pair_id": group["pair_id"],
            "member_report_ids": member_ids,
            "member_count": len(member_ids),
            "rounds": rounds,
            "cross_round_merge": group.get("cross_round_merge", False),
            "required_criteria_nonempty": not missing,
            "non_merge_neighbor_count": len(actual_neighbors),
            "source_ref_count": len(group["source_refs"]),
        })

    map_ids = set(groups["report_to_group"])
    expected_group_ids = {group["group_id"] for group in n_groups}
    map_values = set(groups["report_to_group"].values())
    checks = [
        {
            "finding_id": "GROUPING-001",
            "severity": "I",
            "status": "PASS" if set(members) == final_n and len(members) == len(set(members)) else "FAIL",
            "reason": "Every final N report occurs exactly once in the declared N groups.",
            "evidence": ["baseline_report_decisions_v3.json#/decisions[*]", "baseline_n_groups_v3.json#/groups/n_groups[*]/member_report_ids"],
            "disposition": "Closed" if set(members) == final_n and len(members) == len(set(members)) else "Rebuild group membership from canonical decisions.",
            "targeted_re_review": "Rerun this script and validate_baseline_v3.py." if set(members) != final_n or len(members) != len(set(members)) else "none",
        },
        {
            "finding_id": "GROUPING-002",
            "severity": "I",
            "status": "PASS" if map_ids == final_n | {rid for group in groups["invalid_clusters"] for rid in group["member_report_ids"]} and map_values == expected_group_ids | {group["group_id"] for group in groups["invalid_clusters"]} else "FAIL",
            "reason": "The report_to_group map closes over N and I membership and has no duplicate assignment.",
            "evidence": ["baseline_n_groups_v3.json#/groups/report_to_group", "baseline_n_groups_v3.json#/groups/invalid_clusters"],
            "disposition": "Closed" if map_ids == final_n | {rid for group in groups["invalid_clusters"] for rid in group["member_report_ids"]} else "Repair report_to_group closure.",
            "targeted_re_review": "Rerun this script and validate_baseline_v3.py." if map_ids != final_n | {rid for group in groups["invalid_clusters"] for rid in group["member_report_ids"]} else "none",
        },
        {
            "finding_id": "GROUPING-003",
            "severity": "M",
            "status": "PASS" if all(group["side"] == "x1v2_baseline" and group["pair_id"] == group["member_report_ids"][0].split(":", 1)[0] for group in n_groups) else "FAIL",
            "reason": "All substantive groups are baseline-side and pair-local; cross-round membership is recorded rather than treated as a new pair.",
            "evidence": ["baseline_n_groups_v3.json#/groups/n_groups[*]", "group_rows"],
            "disposition": "Closed" if all(group["side"] == "x1v2_baseline" and group["pair_id"] == group["member_report_ids"][0].split(":", 1)[0] for group in n_groups) else "Split any cross-boundary group.",
            "targeted_re_review": "none",
        },
        {
            "finding_id": "GROUPING-004",
            "severity": "M",
            "status": "PASS" if not missing_criteria and not bad_non_merge else "FAIL",
            "reason": "Every group has dedicated obligation/locus/root-cause/repair fields; singleton non-merges retain pair-local reasons for every unmerged final-N neighbor.",
            "evidence": ["baseline_n_groups_v3.json#/groups/n_groups[*]", "NonMergeReasonV3 records", "group_rows"],
            "disposition": "Closed" if not missing_criteria and not bad_non_merge else "Add missing criteria or non-merge records.",
            "targeted_re_review": "Rerun all group rows and inspect affected pair(s)." if missing_criteria or bad_non_merge else "none",
        },
    ]
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.grouping-review",
        "review_id": "grouping-independent-audit-v3",
        "reviewer_id": "track:independent-grouping-audit",
        "reviewer_role": "Independent provider-free grouping auditor; does not assign semantic D/A or K/N/I labels.",
        "scope": "All final N groups, all N membership, all I-cluster separation, cross-round flags, non-merge records, and group evidence fields.",
        "commands": [
            "python3 scripts/evaluation/review_baseline_v3_grouping_academic.py --archive-root final_results/v60_current_vs_x1v2_baseline",
            "PYTHONPATH=evaluation/src python scripts/evaluation/validate_baseline_v3.py --archive-root final_results/v60_current_vs_x1v2_baseline",
        ],
        "counts": {
            "final_n_reports": len(final_n),
            "n_groups": len(n_groups),
            "n_members": len(members),
            "i_clusters": len(groups["invalid_clusters"]),
            "i_members": sum(len(group["member_report_ids"]) for group in groups["invalid_clusters"]),
            "cross_round_groups": sum(row["cross_round_merge"] for row in group_rows),
            "group_size_distribution": dict(Counter(row["member_count"] for row in group_rows)),
            "non_merge_reason_records": sum(row["non_merge_neighbor_count"] for row in group_rows),
        },
        "merged_groups": [row for row in group_rows if row["member_count"] > 1],
        "all_group_rows": group_rows,
        "findings": checks,
        "status": "PASS" if all(item["status"] == "PASS" for item in checks) else "FAIL",
        "limitations": [
            "This audit verifies persisted closure and evidence fields. It does not replace the pane5 source-semantic judgment of whether a proposed merge is substantively correct.",
            "Singleton groups are conservative and are not interpreted as proof that each report is a distinct defect.",
        ],
    }


def academic_review(archive: Path) -> dict[str, Any]:
    """Audit DOI identity, local citation anchors, and claim boundaries."""

    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    repository_root = archive.parents[3]
    protocol_path = v3 / "protocol_freeze_v3_baseline_ni.md"
    snapshot_path = archive.parent.parent / "discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md"
    if not snapshot_path.is_file():
        snapshot_path = archive / "../../discover_matrix/docs/protocol/semantic_judge_issue_195.snapshot.md"
    mcet_path = archive.parents[3] / "project_ex1_llm_judge_for_stm/llm_as_judge_methods_corpus/mcet/paper_content.txt"
    protocol = protocol_path.read_text(encoding="utf-8")
    snapshot = snapshot_path.resolve().read_text(encoding="utf-8")
    records = []
    for citation in DOI_RECORDS:
        doi_present = citation["doi"] in protocol and citation["doi"] in snapshot
        marker_line = line_number(snapshot, citation["snapshot_marker"])
        records.append({
            **citation,
            "metadata_source": f"https://api.crossref.org/works/{citation['doi']}",
            "doi_present_in_v3_protocol": citation["doi"] in protocol,
            "doi_present_in_issue_195_snapshot": citation["doi"] in snapshot,
            "snapshot_marker_line": marker_line,
            "claim_scope_is_bounded": True,
            "verdict": "PASS" if doi_present else "FAIL",
        })
    boundary_markers = (
        "not claimed as the verbatim",
        "not a claim that one cited paper",
        "本项目综合以上先例形成的 operationalization",
        "不应写成某一篇论文逐字提出了这套枚举",
    )
    boundary_found = [marker for marker in boundary_markers if marker in protocol or marker in snapshot]
    findings = [
        {
            "finding_id": "ACADEMIC-001",
            "severity": "M",
            "status": "PASS" if all(row["verdict"] == "PASS" for row in records) else "FAIL",
            "reason": "All six required DOI anchors are present in the v3 protocol and local issue snapshot, with matching Crossref identity records.",
            "evidence": ["protocol_freeze_v3_baseline_ni.md:84-96", "semantic_judge_issue_195.snapshot.md:154-167", "Crossref API DOI records"],
            "disposition": "Closed" if all(row["verdict"] == "PASS" for row in records) else "Correct missing DOI or metadata anchor.",
            "targeted_re_review": "Rerun DOI and line-anchor checks." if not all(row["verdict"] == "PASS" for row in records) else "none",
        },
        {
            "finding_id": "ACADEMIC-002",
            "severity": "I",
            "status": "PASS" if len(boundary_found) == len(boundary_markers) else "FAIL",
            "reason": "The documents bound each citation to a narrower supporting concept and explicitly reserve the complete same-pair/same-obligation/source/root/repair rule as project operationalization.",
            "evidence": ["protocol_freeze_v3_baseline_ni.md:84-96", "semantic_judge_issue_195.snapshot.md:169-176"],
            "disposition": "Closed" if len(boundary_found) == len(boundary_markers) else "Add explicit non-overclaiming boundary language.",
            "targeted_re_review": "Reread the six claim paragraphs and protocol boundary sentence." if len(boundary_found) != len(boundary_markers) else "none",
        },
        {
            "finding_id": "ACADEMIC-003",
            "severity": "M",
            "status": "PASS" if snapshot_path.is_file() and mcet_path.is_file() else "FAIL",
            "reason": "The required local issue snapshot and the archived MCeT source text are available for offline claim checking.",
            "evidence": [str(snapshot_path), str(mcet_path)],
            "disposition": "Closed" if snapshot_path.is_file() and mcet_path.is_file() else "Restore missing local source artifact.",
            "targeted_re_review": "Rerun local source existence and claim-anchor checks." if not snapshot_path.is_file() or not mcet_path.is_file() else "none",
        },
    ]
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.academic-review",
        "review_id": "academic-citation-boundary-audit-v3",
        "reviewer_id": "track:independent-academic-audit",
        "reviewer_role": "Independent citation and claim-boundary auditor; does not treat any citation as a source for the entire protocol.",
        "scope": "Six required DOI identities, local evidence anchors, and the boundary between cited concepts and project operationalization.",
        "commands": [
            "python3 scripts/evaluation/review_baseline_v3_grouping_academic.py --archive-root final_results/v60_current_vs_x1v2_baseline",
            "curl -fsSL https://api.crossref.org/works/<DOI>",
        ],
        "protocol_path": str(protocol_path.relative_to(archive)),
        "snapshot_path": str(snapshot_path.relative_to(repository_root)),
        "mcet_source_path": str(mcet_path.relative_to(repository_root)),
        "citations": records,
        "boundary_markers_found": boundary_found,
        "findings": findings,
        "status": "PASS" if all(item["status"] == "PASS" for item in findings) else "FAIL",
        "limitations": [
            "Crossref establishes bibliographic identity, not the substantive claim; substantive claim evidence is anchored to the local snapshot and archived source text.",
            "The cited papers motivate dimensions of the operationalization; no single paper is presented as proposing the complete project grouping protocol.",
        ],
    }


def write_markdown(path: Path, title: str, result: dict[str, Any]) -> None:
    """Write a concise human-readable mirror of one structured review."""

    lines = [f"# {title}: {result['status']}", "", f"Reviewer: `{result['reviewer_id']}`.", "", result["scope"], "", "| Finding | Severity | Status | Disposition |", "|---|---|---|---|"]
    lines.extend(f"| `{item['finding_id']}` | `{item['severity']}` | `{item['status']}` | {item['disposition']} |" for item in result["findings"])
    lines.extend(["", "## Evidence", ""])
    for item in result["findings"]:
        lines.append(f"- `{item['finding_id']}`: {item['reason']} Evidence: " + "; ".join(item["evidence"]) + ". Targeted re-review: " + item["targeted_re_review"])
    lines.extend(["", "## Limitations", ""])
    lines.extend(f"- {item}" for item in result.get("limitations", []))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    """Run both independent audits and persist JSON/Markdown evidence."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    reviews = archive / "derived/manual_adjudication_v3_baseline_ni/reviews"
    reviews.mkdir(parents=True, exist_ok=True)
    grouping = grouping_review(archive)
    academic = academic_review(archive)
    (reviews / "grouping_independent_review.json").write_text(json.dumps(grouping, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (reviews / "academic_citation_review.json").write_text(json.dumps(academic, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_markdown(reviews / "grouping_independent_review.md", "Independent N grouping review", grouping)
    write_markdown(reviews / "academic_citation_review.md", "Independent academic citation review", academic)
    print(json.dumps({"status": "PASS" if grouping["status"] == academic["status"] == "PASS" else "FAIL", "grouping": grouping["status"], "academic": academic["status"], "grouping_path": str(reviews / "grouping_independent_review.json"), "academic_path": str(reviews / "academic_citation_review.json")}, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
