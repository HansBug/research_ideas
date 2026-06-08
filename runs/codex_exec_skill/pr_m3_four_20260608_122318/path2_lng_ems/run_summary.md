# PR-M3 codex exec run summary

- case_key: `path2_lng_ems`
- case_id: `state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`
- path: `path2`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1056.785`
- final_model_sha256: `c91fcc5861ba5c8f9a08aa4dbc5630acd045e23ff4f1c376cff07b26ea9bade8`
- report_sha256: `d681b1ee32210a1902aad4aba76f7a41081dab5b3233c4539c3cf13420369037`
- forbidden_runner_used: `False`
- redaction_ok: `True`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path2_lng_ems/codex_transcript.redacted.md`

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
      "blocking_count": 0,
      "advisory_count": 28
    },
    "SD-5A": {
      "ok": true,
      "coverage_gap": false
    },
    "SD-6": {
      "ok": true,
      "passed": 12,
      "total": 12
    },
    "mutations": {
      "caught": 5,
      "total": 5
    },
    "redaction": {
      "ok": true
    },
    "forbidden_call_check": {
      "ok": true
    }
  },
  "nfrr": {
    "final_tier": "T2",
    "allowed_use": "reviewer_queue",
    "scores": {
      "FE": 3,
      "NGF": 3,
      "REC": 3,
      "GAS": 2,
      "SCB": 3,
      "AAT": 3,
      "BVS": 2,
      "DMR": 2
    },
    "cap_reasons": [
      "IND_SINGLE_SELF_ASSESSMENT",
      "NO_HUMAN_SIGNOFF",
      "DYNAMIC_RESAMPLING_NOT_FULLY_SIMULATED"
    ]
  }
}
```
