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

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_cara/codex_transcript.redacted.md`

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
