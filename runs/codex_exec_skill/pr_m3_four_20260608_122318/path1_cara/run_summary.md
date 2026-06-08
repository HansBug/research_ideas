# PR-M3 codex exec run summary

- case_key: `path1_cara`
- case_id: `cara-infusion-pump-formal-spec__01`
- path: `path1`
- status: `completed`
- invalid_run_reason: `None`
- duration_seconds: `1469.527`
- final_model_sha256: `d473c81f4c5684da0ecbfcf01b4790eadc93e16f33ca808b0d87803bb035d9db`
- report_sha256: `a6424e7c7ddca6b59683fdc001dd9fb2248393e6c0e662446531151ca86dcae1`
- forbidden_runner_used: `False`
- redaction_ok: `True`

## Artifact paths

- manifest: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/run_manifest.json`
- report: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/report.md`
- final_model: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/final_model.fcstm`
- metadata: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/metadata.json`
- codex_events: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/codex_events.jsonl`
- transcript_redacted: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_cara/codex_transcript.redacted.md`

## Checks / NFRR snapshot

```json
{
  "checks": {
    "SD-2": "pass",
    "SD-3": "pass",
    "SD-4": "pass_no_blocking",
    "SD-5A": "advisory_gap",
    "SC-5F": "pass",
    "SD-6": "pass 8/8"
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
      "AAT": 2,
      "BVS": 3,
      "DMR": 2
    },
    "cap_reasons": [
      "IND_SINGLE_SELF_ASSESSMENT",
      "NO_HUMAN_SIGNOFF"
    ],
    "reviewer_queue_ready": true
  }
}
```
