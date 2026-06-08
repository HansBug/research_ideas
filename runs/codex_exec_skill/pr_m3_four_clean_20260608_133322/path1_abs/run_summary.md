# PR-M3 codex exec run summary

- case_key: `path1_abs`
- case_id: `abs-fsm-brake-control`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1216.201`
- final_model_sha256: `2c0a3a5d240e75ed458fac0039a7b722979034909cf283d0306c6332e2681397`
- report_sha256: `a12a9c94f02f792c392c12eaa8555d535e8fab802d75b1163602c050e910ff87`
- forbidden_runner_used: `False`
- redaction_ok: `True`
- producer_run_commit: `187b2474c4a2af2213bc4abb79593ceb671ade79`
- audit_tool_commit: `eb6da53924d81c2d2fb34f96f6bf41c3b66f044e`
- audit_provenance_mode: `deterministic_refresh_existing_run`
- recovered_provider_error_count: `0`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/codex_transcript.redacted.md`
- normalized_summary: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/checks/normalized_summary.json`

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
    "item.completed": 116,
    "turn.started": 1,
    "item.started": 84,
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
      "status": "OK",
      "diagnostics": []
    },
    "SD-3": {
      "ok": true,
      "status": "OK",
      "diagnostics": []
    },
    "SD-4": {
      "ok": true,
      "status": "OK",
      "blocking_items": 0,
      "advisory_waivers": [
        "W_UNREFERENCED_VAR:k1/k2/n output-only",
        "W_UNWRITTEN_READ_VAR:slp external input",
        "W_GUARD_VARS_NEVER_CHANGE:slp external input"
      ]
    },
    "SD-5A": {
      "ok": true,
      "status": "OK",
      "coverage_gap": false
    },
    "SC-5F": {
      "ok": true,
      "status": "OK",
      "scenario_set_id": "scenario-set-1bfac7d12d1d"
    },
    "SD-6": {
      "ok": true,
      "status": "OK",
      "n_scenarios": 4,
      "n_scenarios_passed": 4,
      "oracle_weak": false
    }
  },
  "nfrr": {
    "nfrr_report_ref": "nfrr_report.json",
    "claim": {
      "evidence_mode": "NL+paper",
      "scope_type": "full_NL_fragment",
      "obligation_independence": "single_self_assessment",
      "allowed_use_rule_id": "AU-3",
      "allowed_use": "reviewer_queue",
      "signed_reference": false,
      "calibration_status": "uncalibrated_candidate_gate"
    },
    "scores": {
      "FE": 3,
      "NGF": 3,
      "REC": 3,
      "GAS": 3,
      "SCB": 3,
      "AAT": 3,
      "BVS": 3,
      "DMR": 2
    },
    "tier_before_cap": "T3",
    "cap_reasons": [
      "IND_SINGLE_SELF_ASSESSMENT",
      "NO_HUMAN_SIGNOFF"
    ],
    "final_tier": "T2",
    "ready_for_reviewer_queue": true
  }
}
```
