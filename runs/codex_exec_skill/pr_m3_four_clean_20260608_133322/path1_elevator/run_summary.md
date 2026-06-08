# PR-M3 codex exec run summary

- case_key: `path1_elevator`
- case_id: `automatic-elevator-controller`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `945.642`
- final_model_sha256: `3029f80ff8b3a0b00fdacfbdc2817daae4c0e63c53d996a7ccf3225dd925f54c`
- report_sha256: `ea747ee29df719b232431c9511106dfa562a81b5b4f265606aa8ec589bc4fc26`
- forbidden_runner_used: `False`
- redaction_ok: `True`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/codex_transcript.redacted.md`

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
      "status": "ok",
      "blocking_count": 0,
      "advisory_count": 1
    },
    "SD-5A": {
      "ok": true,
      "status": "ok",
      "coverage_gap": false
    },
    "SC-5F": {
      "ok": true,
      "scenario_set_id": "scenario-set-elevator-pr-m3-final",
      "scenario_count": 8
    },
    "SD-6": {
      "ok": true,
      "status": "ok",
      "passed": 8,
      "total": 8,
      "oracle_weak": false
    },
    "SD-8": {
      "ok": true,
      "status": "ok"
    },
    "SD-10-local": {
      "ok": true,
      "status": "ok"
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
      "GAS": 3,
      "SCB": 3,
      "AAT": 3,
      "BVS": 3,
      "DMR": 3
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
