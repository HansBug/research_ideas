# SD deterministic tools

PR-0 约定：`SD-*` 是确定性工具层，不调用 LLM、不读取 `.env`。后续 PR-1A 实现 façade 时必须复用 canonical feedback wrappers，不能形成第二套 parse/semantic/sim/design 实现。

最小工具名预留：

- `run_sd2_parse(current_dsl, ...)`
- `run_sd3_semantic(parse_ok_dsl, stage_context, ...)`
- `run_sd4_design(stage_context.model, policy_profile, warning_budget_state, ...)`
- `run_sd5a_scenario_coverage(current_dsl, scenario_candidates, ...)`
- `freeze_scenario_set(scenario_candidates, source_dsl_hash, coverage_report, ...)`
- `run_sd6_sim(current_dsl, frozen_scenario_set, ...)`
- `run_sd8_fix_plan(selected_feedback, grounding_map, policy_profile, ...)`
- `run_sd10_repair_review(nl, grounding_map, old_dsl, candidate_dsl, fix_plan, scenario_set, ...)`
- `accept_repair_candidate(candidate_dsl, repair_review_feedback, ...)`
- `write_agent_loop_run_record(stage_records, iteration_records, llm_interactions, ...)`

## 契约要点

- enabled deterministic stage 必须产出 `StageResultMeta`。
- `skipped` 必须带 `skipped_reason`；`error` 必须带 `stage_error` 或 `output_validation_error`。
- `advisory` 不阻塞，但必须进入 trace / run record。
- inspect_model 的 suggested_fix 只能作为 `FixPlan.suggested_fix_hints`，不是强制执行脚本。
