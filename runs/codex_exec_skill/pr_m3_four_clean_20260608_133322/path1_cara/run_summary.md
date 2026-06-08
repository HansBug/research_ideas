# PR-M3 codex exec run summary

- case_key: `path1_cara`
- case_id: `cara-infusion-pump-formal-spec__01`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1373.319`
- final_model_sha256: `b48aa16eee2c0616f82f9706756377a508952aabd8447ad5652bd765448aa332`
- report_sha256: `f8cfc7e5c9083a6bb3051038ccfbc7aae19d22c2182a5f84373ca92c6536a2f5`
- forbidden_runner_used: `False`
- redaction_ok: `True`
- producer_run_commit: `187b2474c4a2af2213bc4abb79593ceb671ade79`
- audit_tool_commit: `eb6da53924d81c2d2fb34f96f6bf41c3b66f044e`
- audit_provenance_mode: `deterministic_refresh_existing_run`
- recovered_provider_error_count: `0`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/codex_transcript.redacted.md`
- normalized_summary: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/checks/normalized_summary.json`

## Runner audit provenance

```json
{
  "schema_version": "pr-m3-runner-audit-provenance-v1",
  "mode": "deterministic_refresh_existing_run",
  "producer_run_git": {
    "branch": "feature/project1-pr-m3-codex-exec-experiment-entry",
    "commit": "187b2474c4a2af2213bc4abb79593ceb671ade79",
    "dirty": false,
    "status_short": ""
  },
  "producer_run_git_after": {
    "branch": "feature/project1-pr-m3-codex-exec-experiment-entry",
    "commit": "187b2474c4a2af2213bc4abb79593ceb671ade79",
    "dirty": false,
    "status_short": ""
  },
  "audit_tool_git": {
    "branch": "feature/project1-pr-m3-codex-exec-experiment-entry",
    "commit": "eb6da53924d81c2d2fb34f96f6bf41c3b66f044e",
    "dirty": false,
    "status_short": ""
  },
  "postprocess_git": {
    "branch": "feature/project1-pr-m3-codex-exec-experiment-entry",
    "commit": "eb6da53924d81c2d2fb34f96f6bf41c3b66f044e",
    "dirty": false,
    "status_short": ""
  },
  "audit_tool_feature_floor": {
    "structured_event_marker_audit_minimum_commit": "e0da6d8c6c6e5f9984934fd63983bf4fb4f8e219",
    "reason": "codex_json_stream_audit only rejects explicit event type/marker fields, not marker-like text inside tool output."
  },
  "audit_generated_at": "2026-06-08T07:02:18+00:00",
  "audit_artifacts": [
    "checks/codex_json_stream_audit.json",
    "forbidden_call_check.json",
    "redaction_report.json",
    "checks/normalized_summary.json",
    "run_summary.md"
  ],
  "note": "Existing codex exec event/model artifacts were not regenerated; runner-owned audit/provenance/normalized summary were refreshed deterministically."
}
```

## Normalized summary snapshot

```json
{
  "event_audit_ok": true,
  "event_type_counts": {
    "thread.started": 1,
    "item.completed": 105,
    "turn.started": 1,
    "item.started": 70,
    "item.updated": 3,
    "turn.completed": 1
  },
  "recovered_provider_error_count": 0,
  "recovered_provider_errors": [],
  "redaction_ok": true,
  "forbidden_runner_used": false
}
```

## Checks / NFRR snapshot

```json
{
  "checks": {
    "SD-2": {
      "ok": true,
      "status": "pass"
    },
    "SD-3": {
      "ok": true,
      "status": "pass"
    },
    "SD-4": {
      "ok": true,
      "status": "pass_with_advisories",
      "blocking_count": 0,
      "advisory_count": 18,
      "info_count": 2,
      "waiver_ref": "repair_ledger.json#waiver_ledger"
    },
    "SD-5A": {
      "ok": false,
      "status": "advisory_gap",
      "coverage_gap": true,
      "impact": "lowers DMR and prevents T3 claim"
    },
    "SC-5F": {
      "ok": true,
      "status": "pass"
    },
    "SD-6": {
      "ok": true,
      "status": "pass",
      "n_scenarios": 5,
      "n_scenarios_passed": 5,
      "counted_main_bvs_count": 5
    }
  },
  "nfrr": {
    "nfrr_version": "3.0",
    "evidence_mode": "NL+paper",
    "scope_type": "full_NL_fragment",
    "obligation_independence": "single_self_assessment",
    "scores": {
      "FE": 3,
      "NGF": 3,
      "REC": 3,
      "GAS": 2,
      "SCB": 3,
      "AAT": 2,
      "BVS": 3,
      "DMR": 1
    },
    "tier_before_cap": "T2",
    "cap_reasons": [
      "IND_SINGLE_SELF_ASSESSMENT",
      "NO_HUMAN_SIGNOFF"
    ],
    "final_tier": "T2",
    "allowed_use_rule_id": "AU-3",
    "allowed_use": "reviewer_queue",
    "signed_reference": false,
    "calibration_status": "uncalibrated_candidate_gate"
  }
}
```
