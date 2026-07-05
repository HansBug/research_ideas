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


def rel_if_exists(path: Path) -> str | None:
    """Return a manifest path only when the artifact is actually archived."""
    return rel(path) if path.exists() else None


def parse_cli_identity(stderr_path: Path) -> dict[str, Any]:
    identity: dict[str, Any] = {
        "requested_model_alias": None,
        "observed_cli_model": None,
        "observed_cli_provider": None,
        "resolved_provider_model_id": None,
        "resolution_status": "not_recorded",
    }
    if not stderr_path.exists():
        return identity
    try:
        for line in stderr_path.read_text(encoding="utf-8", errors="replace").splitlines():
            s = line.strip()
            if s.startswith("model:") and identity["observed_cli_model"] is None:
                identity["observed_cli_model"] = s.split(":", 1)[1].strip()
            if s.startswith("provider:") and identity["observed_cli_provider"] is None:
                identity["observed_cli_provider"] = s.split(":", 1)[1].strip()
            if identity["observed_cli_model"] and identity["observed_cli_provider"]:
                break
    except Exception as exc:  # pragma: no cover - audit best effort
        identity["resolution_status"] = f"stderr_parse_failed:{exc}"
        return identity
    if identity["observed_cli_model"] or identity["observed_cli_provider"]:
        identity["requested_model_alias"] = identity["observed_cli_model"]
        identity["resolution_status"] = "cli_transcript_model_and_provider_only_exact_backend_model_id_not_exposed"
    return identity


def merge_cli_identities(judge: str, identities: list[dict[str, Any]]) -> dict[str, Any]:
    observed = [
        {
            "requested_model_alias": item.get("requested_model_alias"),
            "observed_cli_model": item.get("observed_cli_model"),
            "observed_cli_provider": item.get("observed_cli_provider"),
            "resolved_provider_model_id": item.get("resolved_provider_model_id"),
            "resolution_status": item.get("resolution_status"),
        }
        for item in identities
        if item.get("resolution_status") != "not_recorded"
    ]
    if not observed:
        return {
            "judge": judge,
            "requested_model_alias": None,
            "observed_cli_model": None,
            "observed_cli_provider": None,
            "resolved_provider_model_id": None,
            "resolution_status": "not_recorded",
            "observed_attempts": [],
        }

    unique_pairs = sorted(
        {
            (item.get("observed_cli_model"), item.get("observed_cli_provider"))
            for item in observed
        }
    )
    compact_attempts = [
        {
            "observed_cli_model": model,
            "observed_cli_provider": provider,
            "resolved_provider_model_id": None,
        }
        for model, provider in unique_pairs
    ]
    if len(unique_pairs) == 1:
        model, provider = unique_pairs[0]
        return {
            "judge": judge,
            "requested_model_alias": model,
            "observed_cli_model": model,
            "observed_cli_provider": provider,
            "resolved_provider_model_id": None,
            "resolution_status": "cli_transcript_model_and_provider_only_exact_backend_model_id_not_exposed",
            "observed_attempts": compact_attempts,
        }
    providers = {provider for _, provider in unique_pairs}
    return {
        "judge": judge,
        "requested_model_alias": "mixed_attempts",
        "observed_cli_model": "mixed_attempts",
        "observed_cli_provider": next(iter(providers)) if len(providers) == 1 else "mixed_attempts",
        "resolved_provider_model_id": None,
        "resolution_status": "mixed_cli_transcript_model_or_provider_observations_exact_backend_model_id_not_exposed",
        "observed_attempts": compact_attempts,
    }


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
    provider_notes = list(args.provider_note)
    if args.judge == "claude-blind-judge" and not provider_notes:
        provider_notes.append(
            "Claude CLI archived command records requested model alias `sonnet`; "
            "the CLI output/run meta available to this PR did not expose the resolved provider-side exact model_id. "
            "This R5.7.5 artifact is therefore eligible only as a constructed protocol blind dry-run, "
            "not as model-comparison evidence; R6/R7 real LLM runs must capture provider/model exact IDs when available."
        )
    if args.judge == "codex-blind-judge" and not provider_notes:
        provider_notes.append(
            "Codex blind judge could not be completed in this PR because the archived B01--B03 Codex CLI attempts "
            "returned 502 Bad Gateway / upstream failures or no model output under provider=pro; B04 has "
            "prompt/start preflight artifacts only; B05--B20 were intentionally not run after the provider failure "
            "pattern. This manifest is a provider-failure audit, not an eligible multi-judge score and not a Codex "
            "model-capability conclusion."
        )
    model_identity = {
        "judge": args.judge,
        "requested_model_alias": "sonnet" if args.judge == "claude-blind-judge" else None,
        "observed_cli_model": None,
        "observed_cli_provider": None,
        "resolved_provider_model_id": None,
        "resolution_status": (
            "alias_only_exact_model_id_not_exposed_by_archived_claude_cli_run"
            if args.judge == "claude-blind-judge"
            else "not_recorded"
        ),
    }

    cases: list[dict[str, Any]] = []
    case_identities: list[dict[str, Any]] = []
    for row in score["rows"]:
        bid = row["blind_case_id"]
        cdir = outroot / bid
        start_path = cdir / "run_meta_start.json"
        end_path = cdir / "run_meta_end.json"
        start = load_json(start_path) if start_path.exists() else {}
        end = load_json(end_path) if end_path.exists() else {}
        observed_identity = parse_cli_identity(cdir / "stderr.txt")
        case_identities.append(observed_identity)
        cases.append(
            {
                "blind_case_id": bid,
                "source_case_id": row.get("source_case_id"),
                "status": row.get("status"),
                "eligible_for_final_score": row.get("eligible_output") is True,
                "prompt_path": rel_if_exists(cdir / "prompt.txt"),
                "raw_output_path": rel_if_exists(cdir / "raw_output.txt"),
                "combined_output_for_parse_path": rel_if_exists(cdir / "combined_output_for_parse.txt"),
                "parsed_output_path": rel_if_exists(cdir / "parsed_output.json"),
                "stdout_path": rel_if_exists(cdir / "stdout.txt"),
                "stderr_path": rel_if_exists(cdir / "stderr.txt"),
                "run_meta_start_path": rel_if_exists(start_path),
                "run_meta_end_path": rel_if_exists(end_path),
                "artifact_path_exists": {
                    "prompt": (cdir / "prompt.txt").exists(),
                    "raw_output": (cdir / "raw_output.txt").exists(),
                    "combined_output_for_parse": (cdir / "combined_output_for_parse.txt").exists(),
                    "parsed_output": (cdir / "parsed_output.json").exists(),
                    "stdout": (cdir / "stdout.txt").exists(),
                    "stderr": (cdir / "stderr.txt").exists(),
                    "run_meta_start": start_path.exists(),
                    "run_meta_end": end_path.exists(),
                },
                "model_identity_observation": observed_identity,
                "started_at": start.get("started_at"),
                "completed_at": end.get("completed_at"),
                "exit_code": end.get("exit_code"),
                "parse_error": end.get("parse_error"),
                "parse_source": end.get("parse_source"),
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

    if args.judge != "claude-blind-judge":
        model_identity = merge_cli_identities(args.judge, case_identities)

    manifest = {
        "schema_version": "r5_7_5.final_blind_run_manifest.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "judge": args.judge,
        "score_summary_path": rel(score_path),
        "case_count": score["case_count"],
        "eligible_score_applicable": score.get("eligible_score_applicable"),
        "attempted_case_count": score.get("attempted_case_count"),
        "completed_case_count": score.get("completed_case_count"),
        "provider_or_cli_failure_count": score.get("provider_or_cli_failure_count"),
        "incomplete_or_preflight_only_count": score.get("incomplete_or_preflight_only_count"),
        "not_run_count": score.get("not_run_count"),
        "valid_output_count": score["valid_output_count"],
        "verdict_match_count": score["verdict_match_count"],
        "scope_match_count": score["scope_match_count"],
        "run_validity_match_count": score["run_validity_match_count"],
        "gate_all_match_count": score.get("gate_all_match_count"),
        "gate_status_match_counts": score.get("gate_status_match_counts"),
        "gate_disagreement_count": score.get("gate_disagreement_count"),
        "leakage_detected_count": score["leakage_detected_count"],
        "run_validity_match_policy": score.get("run_validity_match_policy"),
        "model_identity": model_identity,
        "provider_notes": provider_notes,
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
