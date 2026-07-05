#!/usr/bin/env python3
"""Build an auditable final-run manifest for an R5.7.5 blind judge output set."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", required=True)
    ap.add_argument(
        "--provider-note",
        action="append",
        default=[],
        help="Provider/configuration caveat to persist in the manifest.",
    )
    args = ap.parse_args()

    outroot = ROOT / "judge_outputs" / args.judge
    score_path = outroot / "score_summary.json"
    if not score_path.exists():
        raise SystemExit(f"score_summary.json not found: {score_path}")
    score = load_json(score_path)

    cases: list[dict[str, Any]] = []
    for row in score["rows"]:
        bid = row["blind_case_id"]
        cdir = outroot / bid
        start_path = cdir / "run_meta_start.json"
        end_path = cdir / "run_meta_end.json"
        start = load_json(start_path) if start_path.exists() else {}
        end = load_json(end_path) if end_path.exists() else {}
        cases.append(
            {
                "blind_case_id": bid,
                "source_case_id": row.get("source_case_id"),
                "status": row.get("status"),
                "eligible_for_final_score": row.get("eligible_output") is True,
                "prompt_path": rel(cdir / "prompt.txt"),
                "raw_output_path": rel(cdir / "raw_output.txt"),
                "combined_output_for_parse_path": rel(cdir / "combined_output_for_parse.txt"),
                "parsed_output_path": rel(cdir / "parsed_output.json"),
                "stdout_path": rel(cdir / "stdout.txt"),
                "stderr_path": rel(cdir / "stderr.txt"),
                "run_meta_start_path": rel(start_path),
                "run_meta_end_path": rel(end_path),
                "started_at": start.get("started_at"),
                "completed_at": end.get("completed_at"),
                "exit_code": end.get("exit_code"),
                "parse_error": end.get("parse_error"),
                "provider_or_cli_nonzero_with_parsed_output": end.get("provider_or_cli_nonzero_with_parsed_output"),
                "expected_verdict": row.get("expected_verdict"),
                "observed_verdict": row.get("observed_verdict"),
                "verdict_match": row.get("verdict_match"),
                "expected_scope": row.get("expected_scope"),
                "observed_scope": row.get("observed_scope"),
                "scope_match": row.get("scope_match"),
                "expected_run_validity": row.get("expected_run_validity"),
                "observed_run_validity": row.get("observed_run_validity"),
                "run_validity_match": row.get("run_validity_match"),
                "gate_all_match": row.get("gate_all_match"),
                "gate_disagreements": row.get("gate_disagreements", []),
                "leakage_detected": row.get("leakage_detected"),
            }
        )

    manifest = {
        "schema_version": "r5_7_5.final_blind_run_manifest.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "judge": args.judge,
        "score_summary_path": rel(score_path),
        "case_count": score["case_count"],
        "valid_output_count": score["valid_output_count"],
        "verdict_match_count": score["verdict_match_count"],
        "scope_match_count": score["scope_match_count"],
        "run_validity_match_count": score["run_validity_match_count"],
        "gate_all_match_count": score.get("gate_all_match_count"),
        "gate_status_match_counts": score.get("gate_status_match_counts"),
        "gate_disagreement_count": score.get("gate_disagreement_count"),
        "leakage_detected_count": score["leakage_detected_count"],
        "provider_notes": args.provider_note,
        "eligibility_policy": {
            "valid_json_required": True,
            "provider_or_cli_failures_excluded_from_main_score": True,
            "schema_invalid_excluded_from_main_score": True,
            "constructed_cases_are_not_repair_effectiveness_evidence": True,
        },
        "cases": cases,
    }
    out = outroot / "final_run_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
