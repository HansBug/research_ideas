# LG-F1 durable checkpoint / resume evidence

- mode: `mock`
- case_key: `path1_abs`
- condition_id: `default`
- verdict: `consistent`
- checkpoint_backend: `sqlite` / `SqliteSaver`
- interrupt requested/actual: `repair_sl10_review` / `repair_path`
- run_record_path: `runs/pr_lg_f1_resume_mock/records/lg-f1-mock-abs.agent_loop.json.gz`
- resume_diff_report_path: `runs/pr_lg_f1_resume_mock/resume_diff_report.json`
- resume_run_main_result_eligible: `False`
- uninterrupted_baseline_available: `True`
- support_level: `controlled_parent_node_boundary_only`
- scope: `controlled_parent_node_boundary_resume`；mid_node_crash_supported=`False`；nested_subgraph_resume_supported=`False`

## Append-only audit

- `duplicate_fix_log_entry_detected`: `False`
- `fix_log_prefix_preserved`: `True`
- `llm_interactions_prefix_preserved`: `True`
- `repair_history_prefix_preserved`: `True`
- `scenario_history_prefix_preserved`: `True`
- `stage_records_prefix_preserved`: `True`

## Comparison checks

- `stage_ids`: `consistent`
- `fix_log`: `consistent`
- `llm_interactions`: `consistent`
- `scenario_history`: `consistent`
- `repair_history`: `consistent`
- `final_dsl_hash`: `consistent`
- `verdict`: `consistent`
- `result_status`: `consistent`

## Stage replay audit

- unexpected_stage_replay_detected: `False`
- post_repair_full_revalidation_expected: `True`
- explanation: Expected: interrupt_after mapped to parent node repair_path; after resume the pending repair_decision routes into a full post-repair validation pass, so SD-2/SD-3/... appear after the preserved repair prefix.

## PR comment snippet

LG-F1 resume run 是 evidence-only hardening 证据，不进入主四例统计；真实运行如使用 provider，命令前必须 `set -a; source .env; set +a`，且不得回显密钥。
