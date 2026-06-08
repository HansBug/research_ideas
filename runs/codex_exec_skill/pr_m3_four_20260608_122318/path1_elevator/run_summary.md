# PR-M3 codex exec run summary

- case_key: `path1_elevator`
- case_id: `automatic-elevator-controller`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1095.577`
- final_model_sha256: `b5029bb2a00886f5da1392ee2506afa4b6aed735eee772bb0ad0ac8f29d4ded7`
- report_sha256: `a1e593ffaa53f6415c86cafae2c648c6f3da4ccd6a3c7fa7bd8ffd2940a10eeb`
- forbidden_runner_used: `False`
- redaction_ok: `True`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_elevator/codex_transcript.redacted.md`

## Checks / NFRR snapshot

```json
{
  "checks": {
    "sd2_parse": {
      "ok": true
    },
    "sd3_semantic": {
      "ok": true
    },
    "sd4_design": {
      "ok": true,
      "blocking_count": 0,
      "advisory_count": 1
    },
    "sd5a_coverage_gap": false,
    "sd6_sim": {
      "ok": true,
      "passed": 8,
      "total": 8,
      "oracle_weak": false
    },
    "forbidden_call_check": {
      "forbidden_runner_used": false
    },
    "redaction": {
      "raw_secret_written": false
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
      "DMR": 2
    },
    "allowed_use": "reviewer_queue",
    "ready_for_reviewer_queue": true
  }
}
```
