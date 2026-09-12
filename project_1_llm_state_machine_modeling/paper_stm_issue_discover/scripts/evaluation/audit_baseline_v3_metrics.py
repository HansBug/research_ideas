#!/usr/bin/env python3
"""Independently check provider-free baseline v3 metric serialization."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def load(path: Path) -> Any:
    """Load one UTF-8 JSON artifact."""

    return json.loads(path.read_text(encoding="utf-8"))


def fail(check: str, reason: str, evidence: list[str]) -> dict[str, Any]:
    """Build one failed check record."""

    return {"check": check, "status": "FAIL", "reason": reason, "evidence": evidence}


def passed(check: str, reason: str, evidence: list[str]) -> dict[str, Any]:
    """Build one passed check record."""

    return {"check": check, "status": "PASS", "reason": reason, "evidence": evidence}


def expected_tsv_cell(value: Any) -> str:
    """Mirror the canonical writer's fixed-column serialization."""

    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "" if value is None else str(value)


def audit(archive: Path) -> dict[str, Any]:
    """Check summaries, report rendering, dense units, and TSV serialization."""

    v3 = archive / "derived/manual_adjudication_v3_baseline_ni"
    summary_path = v3 / "summary_v3.json"
    recomputed_path = v3 / "recomputed_summary_v3.json"
    decisions_path = v3 / "baseline_report_decisions_v3.json"
    tsv_path = v3 / "baseline_report_decisions_v3.tsv"
    dense_path = v3 / "baseline_relation_decisions_v3.json"
    combined_path = v3 / "baseline_combined_512_v3.json"
    report_path = archive / "report/v60_current_vs_x1v2_baseline_cn.md"
    summary = load(summary_path)
    recomputed = load(recomputed_path)
    decisions_doc = load(decisions_path)
    decisions = decisions_doc["decisions"]
    dense = load(dense_path)["rows"]
    combined = load(combined_path)["rows"]
    checks: list[dict[str, Any]] = []

    if summary == recomputed:
        checks.append(passed("SUMMARY-EQUALITY", "summary_v3 and recomputed_summary_v3 are structurally equal.", [str(summary_path), str(recomputed_path)]))
    else:
        checks.append(fail("SUMMARY-EQUALITY", "The recorded and recomputed summaries differ.", [str(summary_path), str(recomputed_path)]))

    migration_counts = summary["non_k_migrations"]["counts"]
    if sum(migration_counts.values()) == 233:
        checks.append(passed("MIGRATION-CLOSURE", "All original non-K rows occur in exactly one migration bucket.", [str(summary_path) + "#/non_k_migrations/counts"]))
    else:
        checks.append(fail("MIGRATION-CLOSURE", "Migration buckets do not sum to 233.", [str(summary_path) + "#/non_k_migrations/counts"]))

    if len(decisions) == 233 and len(dense) == 233 * 145 and len(combined) == 512:
        checks.append(passed("UNIT-CLOSURE", "Canonical non-K, dense relation, and combined report units close at 233, 33785, and 512.", [str(decisions_path), str(dense_path), str(combined_path)]))
    else:
        checks.append(fail("UNIT-CLOSURE", "Canonical report or relation unit counts are incomplete.", [str(decisions_path), str(dense_path), str(combined_path)]))

    csv.field_size_limit(sys.maxsize)
    with tsv_path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        tsv_rows = list(reader)
    fields = list(decisions[0])
    tsv_matches = len(tsv_rows) == len(decisions) and all(
        all(tsv_row.get(field) == expected_tsv_cell(row.get(field)) for field in fields)
        for row, tsv_row in zip(decisions, tsv_rows)
    )
    if tsv_matches:
        checks.append(passed("TSV-MIRROR", "Every fixed-column TSV cell matches its canonical JSON value.", [str(decisions_path), str(tsv_path)]))
    else:
        checks.append(fail("TSV-MIRROR", "The fixed-column TSV is not an exact serialization of canonical decisions.", [str(decisions_path), str(tsv_path)]))

    with tempfile.TemporaryDirectory(prefix="baseline-v3-render-") as temp_dir:
        rendered = Path(temp_dir) / "report.md"
        command = [
            sys.executable,
            str(archive.parents[1] / "scripts/evaluation/render_baseline_v3_report.py"),
            "--archive-root",
            str(archive),
            "--output",
            str(rendered),
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        render_matches = result.returncode == 0 and rendered.read_bytes() == report_path.read_bytes()
    if render_matches:
        checks.append(passed("REPORT-RENDER", "The checked-in paired report equals a fresh provider-free render.", [str(report_path), "scripts/evaluation/render_baseline_v3_report.py"]))
    else:
        checks.append(fail("REPORT-RENDER", "The checked-in report differs from a fresh provider-free render.", [str(report_path), "scripts/evaluation/render_baseline_v3_report.py", result.stderr.strip()]))

    metrics = summary["metrics"]
    denominator_ok = (
        metrics["hit_at_1_full"]["denominator"] == 435
        and metrics["l2_hit_at_1_full"]["denominator"] == 117
        and metrics["hit_at_3_full"]["denominator"] == 145
        and metrics["l2_hit_at_3_full"]["denominator"] == 39
        and metrics["l2_ledger_based"]["status"] == "not_applicable"
        and metrics["predicate_usage"]["status"] == "not_applicable"
    )
    if denominator_ok:
        checks.append(passed("DENOMINATOR-SYMMETRY", "Expected, L2, and not-applicable denominators are explicit and protocol-consistent.", [str(summary_path) + "#/metrics", str(report_path)]))
    else:
        checks.append(fail("DENOMINATOR-SYMMETRY", "One or more shared denominators or not-applicable metrics are inconsistent.", [str(summary_path) + "#/metrics", str(report_path)]))

    if summary.get("provider_calls_in_this_recompute") == 0 and summary.get("method_or_judge_reruns_in_this_goal") == 0:
        checks.append(passed("EXECUTION-BOUNDARY", "The recomputed summary records zero provider and method/Judge reruns.", [str(summary_path)]))
    else:
        checks.append(fail("EXECUTION-BOUNDARY", "The recompute metadata records a forbidden execution.", [str(summary_path)]))

    failures = [check for check in checks if check["status"] == "FAIL"]
    return {
        "schema": "paper1.manual-adjudication.v3-baseline-ni.numeric-recompute-review",
        "review_id": "baseline-v3-numeric-serialization-provider-free",
        "reviewer_role": "independent deterministic metric and serialization audit; not a semantic label adjudicator",
        "checks": checks,
        "status": "FAIL" if failures else "PASS",
        "fail_count": len(failures),
    }


def main() -> None:
    """Write the numeric review JSON and Markdown artifacts."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--archive-root", type=Path, required=True)
    args = parser.parse_args()
    archive = args.archive_root.resolve()
    review_dir = archive / "derived/manual_adjudication_v3_baseline_ni/reviews"
    review_dir.mkdir(parents=True, exist_ok=True)
    result = audit(archive)
    json_path = review_dir / "numeric_recompute_review_v3.json"
    md_path = review_dir / "numeric_recompute_review_v3.md"
    json_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Baseline v3 numeric recomputation review: {result['status']}",
        "",
        "This is an independent deterministic audit of serialization, unit closure, report rendering, and denominator symmetry. It does not assign semantic labels.",
        "",
        "| Check | Status | Reason | Evidence |",
        "|---|---|---|---|",
    ]
    for check in result["checks"]:
        lines.append(f"| `{check['check']}` | `{check['status']}` | {check['reason']} | {'; '.join(check['evidence'])} |")
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"status": result["status"], "checks": len(result["checks"]), "fail_count": result["fail_count"]}, sort_keys=True))


if __name__ == "__main__":
    main()
