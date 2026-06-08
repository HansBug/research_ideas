# PR-M3 codex exec run summary

- case_key: `path2_lng_ems`
- case_id: `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`
- path: `path2`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1468.212`
- final_model_sha256: `d936802cd18ae021cc80c6c66bda16c00d3a8149630584708cf34cf8ed0e8fe1`
- report_sha256: `768a78311437e4991f36d30871274be1b5d98f57403e98ad3bcabbada241b052`
- forbidden_runner_used: `False`
- redaction_ok: `True`
- producer_run_commit: `187b2474c4a2af2213bc4abb79593ceb671ade79`
- audit_tool_commit: `eb6da53924d81c2d2fb34f96f6bf41c3b66f044e`
- audit_provenance_mode: `deterministic_refresh_existing_run`
- recovered_provider_error_count: `2`

## Artifact paths

- manifest: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/run_manifest.json`
- report: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/report.md`
- final_model: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/final_model.fcstm`
- metadata: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/metadata.json`
- codex_events: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/codex_transcript.redacted.md`
- normalized_summary: `runs/codex_exec_skill/2026-06-08-133322-pr39-pr-m3-codex-exec-skill-final-four-case-evidence/path2-lng-ems-codex-exec-skill-completed/checks/normalized_summary.json`

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
  "audit_generated_at": "2026-06-08T07:02:19+00:00",
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
    "item.completed": 73,
    "turn.started": 1,
    "item.started": 49,
    "item.updated": 2,
    "error": 2,
    "turn.completed": 1
  },
  "recovered_provider_error_count": 2,
  "recovered_provider_errors": [
    {
      "line": 87,
      "message": "Reconnecting... 1/5 (stream disconnected before completion: Upstream request failed)"
    },
    {
      "line": 101,
      "message": "Reconnecting... 1/5 (stream disconnected before completion: Upstream request failed)"
    }
  ],
  "redaction_ok": true,
  "forbidden_runner_used": false
}
```

## Checks / NFRR snapshot

```json
{
  "checks": {
    "SD-2": {
      "ok": true
    },
    "SD-3": {
      "ok": true
    },
    "SD-4": {
      "ok": true,
      "unwaived_blocking_count": 0
    },
    "SD-5A": {
      "ok": false,
      "coverage_gap": true,
      "waived_as_advisory": true
    },
    "SC-5F": {
      "ok": true
    },
    "SD-6": {
      "ok": true,
      "passed": 13,
      "total": 13
    },
    "DMR-local": {
      "ok": true,
      "caught": 6,
      "total": 6
    }
  },
  "nfrr": {
    "final_tier": "T2",
    "tier_before_cap": "T3",
    "scores": {
      "FE": 3,
      "NGF": 3,
      "REC": 3,
      "GAS": 3,
      "SCB": 3,
      "AAT": 3,
      "BVS": 3,
      "DMR": 1
    },
    "allowed_use": "reviewer_queue",
    "cap_reasons": [
      "IND_SINGLE_SELF_ASSESSMENT",
      "NO_HUMAN_SIGNOFF"
    ]
  }
}
```
