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

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path2_lng_ems/codex_transcript.redacted.md`

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
