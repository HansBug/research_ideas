#!/usr/bin/env python3
"""Audit v3 baseline fairness and leakage metadata without assigning labels."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


FORBIDDEN_PROPOSAL_INPUTS = {
    "v2 decisions or derived/manual_adjudication_v2",
    "v3 decisions and any other proposal JSON",
    "pane5 decision register",
    "Judge labels, Judge outputs, and Judge source-run summaries",
    "Track A/B/C reviewer conclusions",
}
EXCLUDED_PROPOSALS = {
    "proposals/track_b_full_0000_0059.json",
    "proposals/track_b_full_legacy.json",
    "proposals/track_b_0020_0059.json",
    "proposals/raw_scope_probe_0000_0019.json",
}


def load(path: Path) -> Any:
    """Read one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def finding(
    finding_id: str,
    severity: str,
    status: str,
    reason: str,
    evidence: list[str],
    disposition: str,
    targeted_re_review: str,
) -> dict[str, Any]:
    """Build one structured audit finding."""

    return {
        "finding_id": finding_id,
        "severity": severity,
        "status": status,
        "reason": reason,
        "evidence_paths": evidence,
        "disposition": disposition,
        "targeted_re_review": targeted_re_review,
    }


def audit(archive: Path) -> dict[str, Any]:
    """Check only persisted provenance, boundary, and metric-symmetry facts."""

    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    proposal_path = v3 / "proposals/track_b_0040_0059.json"
    proposal = load(proposal_path)
    decisions_path = v3 / "baseline_report_decisions_v3.json"
    decisions = load(decisions_path)["decisions"]
    frozen = load(v3 / "frozen_k_snapshot_v3.json")["rows"]
    old = load(archive / "derived/manual_adjudication_v2/x1v2_report_decisions.json")["decisions"]
    v3_manifest = load(v3 / "publication_manifest_v3_baseline_ni.json")
    report = (archive / "report/v60_current_vs_x1v2_baseline_cn.md").read_text(encoding="utf-8")
    summary = load(v3 / "recomputed_summary_v3.json")
    findings: list[dict[str, Any]] = []

    forbidden = set(proposal.get("forbidden_inputs_read", []))
    records = proposal.get("reports", [])
    blind_ok = bool(records) and all(
        row.get("review_status") == "PROPOSAL"
        and row.get("reference_visible") is False
        and row.get("primary_visible") is False
        for row in records
    )
    if len(records) == 152 and forbidden == FORBIDDEN_PROPOSAL_INPUTS and blind_ok:
        findings.append(finding(
            "FAIR-V3-001", "I", "PASS",
            "Track B 0040-0059 records are explicitly proposal-only and blind to frozen labels, pane5, and other reviewer conclusions.",
            [str(proposal_path.relative_to(archive)), "#/forbidden_inputs_read", "#/reports[*]/reference_visible", "#/reports[*]/primary_visible"],
            "Retain as proposal provenance; never treat it as final human adjudication.",
            "Re-run this audit after any proposal or manifest change.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-001", "C", "FAIL",
            "Track B blind metadata, forbidden-input declaration, or 152-record coverage is incomplete.",
            [str(proposal_path.relative_to(archive))],
            "Repair proposal metadata and re-run the provider-free audit.",
            "Required before finalization.",
        ))

    if frozen == [row for row in old if row["corrected_kni"] == "K"] and len(frozen) == 279:
        findings.append(finding(
            "FAIR-V3-002", "C", "PASS",
            "The frozen K projection is exactly the v2 K sequence and contains 279 rows.",
            ["derived/manual_adjudication_v3_baseline_ni/frozen_k_snapshot_v3.json", "derived/manual_adjudication_v2/x1v2_report_decisions.json#/decisions"],
            "Keep frozen K outside v3 semantic reclassification.",
            "Run the same equality check after final commit.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-002", "C", "FAIL",
            "Frozen K projection differs from the v2 K rows or its count is not 279.",
            ["frozen_k_snapshot_v3.json", "x1v2_report_decisions.json"],
            "Stop publication and restore the exact frozen projection without changing raw.",
            "Required before finalization.",
        ))

    independent_ok = all(
        len(row["review"]["independent_opinions"]) >= 2
        and len(set(row["review"]["independent_reviewer_ids"])) >= 2
        and all(
            opinion["review_status"] == "PROPOSAL"
            and opinion["reference_visible"] is False
            and opinion["primary_visible"] is False
            for opinion in row["review"]["independent_opinions"]
        )
        for row in decisions
    )
    if len(decisions) == 233 and independent_ok:
        findings.append(finding(
            "FAIR-V3-003", "I", "PASS",
            "All 233 canonical rows retain at least two distinct proposal identities, and each retained opinion records blind submission flags.",
            ["baseline_report_decisions_v3.json#/decisions[*]/review"],
            "Canonical labels remain pane5-confirmed; proposal identities are evidence only.",
            "Re-run with the final canonical hash.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-003", "C", "FAIL",
            "Canonical review-chain separation is incomplete.",
            ["baseline_report_decisions_v3.json#/decisions[*]/review"],
            "Repair review-chain closure; do not publish affected rows.",
            "Required before finalization.",
        ))

    boundary = v3_manifest.get("execution_boundary", {})
    if boundary == {
        "provider_calls": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "raw_modified": False,
        "current_modified": False,
    }:
        findings.append(finding(
            "FAIR-V3-004", "C", "PASS",
            "The v3 manifest records zero provider, method, and Judge reruns and no raw/current modification.",
            ["derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json#/execution_boundary", "reviews/arbitration_log_v3.json"],
            "Retain the explicit execution boundary in both v3 and top-level manifests.",
            "Compare final manifest boundary with repository run records.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-004", "C", "FAIL",
            "The persisted v3 execution boundary is missing or records a forbidden call/change.",
            ["publication_manifest_v3_baseline_ni.json#/execution_boundary"],
            "Do not finalize until the boundary is corrected from evidence.",
            "Required before finalization.",
        ))

    excluded = {item["path"] for item in v3_manifest.get("excluded_outputs", [])}
    output_paths = {item["path"] for item in v3_manifest.get("outputs", [])}
    if excluded == EXCLUDED_PROPOSALS and not excluded & output_paths:
        findings.append(finding(
            "FAIR-V3-005", "I", "PASS",
            "Broad, legacy, and probe proposal files are explicitly excluded and cannot enter canonical v3 outputs.",
            ["derived/manual_adjudication_v3_baseline_ni/publication_manifest_v3_baseline_ni.json#/excluded_outputs", "derived/manual_adjudication_v3_baseline_ni/README.md"],
            "Keep excluded files for history; do not delete or silently include them.",
            "Re-run after the final manifest and link check.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-005", "I", "FAIL",
            "Retained proposal files are not completely classified in the v3 manifest.",
            ["publication_manifest_v3_baseline_ni.json#/excluded_outputs"],
            "Classify every retained non-canonical proposal before finalization.",
            "Required before finalization.",
        ))

    metric_ok = (
        "| 指标 | v60/current | X1v2 baseline | delta (n; pp) |" in report
        and summary["metrics"]["l2_ledger_based"]["status"] == "not_applicable"
        and summary["metrics"]["predicate_usage"]["status"] == "not_applicable"
        and summary["metrics"]["hit_at_1_full"]["denominator"] == 435
    )
    if metric_ok:
        findings.append(finding(
            "FAIR-V3-006", "I", "PASS",
            "The publication report uses paired current/baseline columns and the baseline summary preserves shared hit denominators plus explicit not-applicable L2/predicate metrics.",
            ["report/v60_current_vs_x1v2_baseline_cn.md", "derived/manual_adjudication_v3_baseline_ni/recomputed_summary_v3.json#/metrics"],
            "Keep report values generated from canonical summaries; do not hand-edit numeric claims.",
            "Independent numeric review must compare every rendered row to recomputed JSON.",
        ))
    else:
        findings.append(finding(
            "FAIR-V3-006", "I", "FAIL",
            "Paired metric columns, shared denominator, or not-applicable distinctions are incomplete.",
            ["report/v60_current_vs_x1v2_baseline_cn.md", "recomputed_summary_v3.json"],
            "Regenerate the report and re-run numeric review.",
            "Required before finalization.",
        ))

    passed = sum(item["status"] == "PASS" for item in findings)
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.fairness-leakage-review",
        "review_id": "baseline-v3-fairness-leakage-provider-free",
        "reviewer_role": "read-only provenance, blind-input, boundary, and metric-symmetry audit; not a semantic label adjudicator",
        "scope": "X1v2 baseline non-K v3 archive and Track B 0040-0059 proposal metadata.",
        "findings": findings,
        "pass_count": passed,
        "fail_count": len(findings) - passed,
        "status": "PASS" if passed == len(findings) else "FAIL",
    }


def main() -> None:
    """Write JSON and Markdown audit artifacts under the v3 review directory."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    review_dir = archive / "derived/manual_adjudication_v3_baseline_ni/reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    result = audit(archive)
    (review_dir / "fairness_leakage_review_v3.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Baseline v3 fairness/leakage review: {result['status']}",
        "",
        "This is a read-only provenance and boundary audit. It does not assign or replace semantic labels.",
        "",
        "| Finding | Severity | Status | Reason | Disposition | Targeted re-review |",
        "|---|---|---|---|---|---|",
    ]
    for item in result["findings"]:
        lines.append(f"| `{item['finding_id']}` | `{item['severity']}` | `{item['status']}` | {item['reason']} | {item['disposition']} | {item['targeted_re_review']} |")
    lines += ["", f"PASS: `{result['pass_count']}`; FAIL: `{result['fail_count']}`.", ""]
    (review_dir / "fairness_leakage_review_v3.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "pass": result["pass_count"], "fail": result["fail_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
