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

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_abs/codex_transcript.redacted.md`

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
