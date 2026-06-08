# PR-M3 codex exec run summary

- case_key: `path1_abs`
- case_id: `abs-fsm-brake-control`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1399.157`
- final_model_sha256: `2656aa5d8d2966fc924fc9b123603684d67ace3f139adbf90fe443ca0c8604ac`
- report_sha256: `e60417fa2dcaec581a1520900880cd6e94e8d70326d09bbf4e267437bb87218b`
- forbidden_runner_used: `False`
- redaction_ok: `True`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/codex_transcript.redacted.md`

## Checks / NFRR snapshot

```json
{
  "checks": {
    "SD-2": {
      "ok": true,
      "status": "ok"
    },
    "SD-3": {
      "ok": true,
      "status": "ok"
    },
    "SD-4": {
      "ok": true,
      "status": "ok"
    },
    "SD-5A": {
      "ok": true,
      "status": "ok"
    },
    "SC-5F": {
      "ok": true,
      "status": "ok"
    },
    "SD-6": {
      "ok": true,
      "status": "ok"
    }
  },
  "nfrr": {
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
    "allowed_use_rule_id": "AU-3",
    "allowed_use": "reviewer_queue",
    "signed_reference": false,
    "calibration_status": "uncalibrated_candidate_gate"
  }
}
```
