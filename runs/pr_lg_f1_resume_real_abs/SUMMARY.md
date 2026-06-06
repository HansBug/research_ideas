# LG-F1 durable checkpoint / resume evidence

- mode: `real`
- case_key: `path1_abs`
- condition_id: `default`
- verdict: `consistent`
- checkpoint_backend: `sqlite` / `SqliteSaver`
- interrupt requested/actual: `sl1_initial_modeling` / `sl1_initial_modeling`
- run_record_path: `runs/pr_lg_f1_resume_real_abs/records/lg-f1-real-abs.agent_loop.json.gz`
- resume_diff_report_path: `runs/pr_lg_f1_resume_real_abs/resume_diff_report.json`
- resume_run_main_result_eligible: `False`
- uninterrupted_baseline_available: `False`
- baseline_comparison_method: `not_available`
- baseline_comparison_verdict: `not_applicable`
- verdict_scope: `append_only_stage_replay_only_no_independent_baseline`
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

> No independent uninterrupted baseline is available for this run.
> The following checks are `not_applicable` for baseline equivalence and only keep resumed/prefix hashes for audit.

- `stage_ids`: `not_applicable` (basis=`no_independent_baseline`)
- `fix_log`: `not_applicable` (basis=`no_independent_baseline`)
- `llm_interactions`: `not_applicable` (basis=`no_independent_baseline`)
- `scenario_history`: `not_applicable` (basis=`no_independent_baseline`)
- `repair_history`: `not_applicable` (basis=`no_independent_baseline`)
- `final_dsl_hash`: `not_applicable` (basis=`no_independent_baseline`)
- `verdict`: `not_applicable` (basis=`no_independent_baseline`)
- `result_status`: `not_applicable` (basis=`no_independent_baseline`)

## Stage replay audit

- unexpected_stage_replay_detected: `False`
- post_repair_full_revalidation_expected: `False`
- explanation: No repeated stage ids after the preserved prefix.

## PR comment snippet

LG-F1 resume run 是 evidence-only hardening 证据，不进入主四例统计；真实运行如使用 provider，命令前必须 `set -a; source .env; set +a`，且不得回显密钥。
