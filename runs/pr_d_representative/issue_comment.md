## PR-D representative full staged run evidence

本 comment 汇总 PR-D 对 #14 两条 representative NL 的真实默认入口复跑结果。

### 总体结论

| Case | verdict | record status | main result eligible | oracle weak | stage graph | wiring断链 | run record |
|---|---|---|---:|---:|---|---|---|
| Path1 CARA representative NL | `not_converged` | `rejected` | ❌ | ❌ | ✅ | ✅ 未出现 | `runs/pr_d_representative/pr-d-path1_cara.agent_loop.json.gz` |
| Path2 LNG-ship EMS representative NL | `not_converged` | `rejected` | ❌ | ❌ | ✅ | ✅ 未出现 | `runs/pr_d_representative/pr-d-path2_lng_ems.agent_loop.json.gz` |

### Path1 CARA representative NL

- 上游 #14 诊断：https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890685
- case_id：`cara-infusion-pump-formal-spec__01`
- 输入 NL 长度：`1602`
- run_id：`pr-d-path1_cara`
- run record：`runs/pr_d_representative/pr-d-path1_cara.agent_loop.json.gz`
- git commit：`56ad2865b204560f2d9b65cecd6c27e50fa9e872`
- resolved config：condition_id=`full_staged_v1`，policy_profile=`experiment_default`，config_hash=`sha256:dab33bb796a6f69f9e6bc2b7f956966a96e4f3ef72724d8ea25f835f32d437de`
- provider/model：mode=`real_env`，real_api=`True`，config_read=`True`，model=`gpt-5.5`
- verdict：`not_converged`，record_status=`rejected`，source_stage=`SC-11`
- verdict reason：candidate semantic failed
- stage 摘要：iterations=`1`，repairs=`1`，scenario_history=`0`，LLM stages=`SL-1, SL-9`
- scenario：scenario_set_id=`None`，epoch=`None`，oracle_weak=`False`
- eligibility：main_result_eligible=`False`，inclusion_reason=`None`，exclusion_reason=`verdict_not_success`
- redaction/schema：schema_valid=`True`，secret_redacted=`True`，redaction_report_count=`0`
- 旧 wiring 断链检查：`scenario generation unavailable because initial DSL parse failed` 出现？`False`
- final DSL length：`1741`

### Path2 LNG-ship EMS representative NL

- 上游 #14 诊断：https://github.com/HansBug/research_ideas/issues/14#issuecomment-4598890799
- case_id：`state-transitions-logical-design-for-hybrid-energy-generation-with-renewable-energy-sources-in-lng-ship`
- 输入 NL 长度：`1558`
- run_id：`pr-d-path2_lng_ems`
- run record：`runs/pr_d_representative/pr-d-path2_lng_ems.agent_loop.json.gz`
- git commit：`56ad2865b204560f2d9b65cecd6c27e50fa9e872`
- resolved config：condition_id=`full_staged_v1`，policy_profile=`experiment_default`，config_hash=`sha256:eed0ab47b50ea1a85505136061b8dea0e024d6ea73b7b07bf7f7b5f6c03057de`
- provider/model：mode=`real_env`，real_api=`True`，config_read=`True`，model=`gpt-5.5`
- verdict：`not_converged`，record_status=`rejected`，source_stage=`SC-11`
- verdict reason：design_target_unresolved
- stage 摘要：iterations=`1`，repairs=`1`，scenario_history=`0`，LLM stages=`SL-1, SL-9`
- scenario：scenario_set_id=`None`，epoch=`None`，oracle_weak=`False`
- eligibility：main_result_eligible=`False`，inclusion_reason=`None`，exclusion_reason=`verdict_not_success`
- redaction/schema：schema_valid=`True`，secret_redacted=`True`，redaction_report_count=`0`
- 旧 wiring 断链检查：`scenario generation unavailable because initial DSL parse failed` 出现？`False`
- final DSL length：`3933`

### PR-D 解释边界

- 若 verdict 为 `not_converged`，本 evidence 只能说明默认入口与 run-record 基础设施可审计执行，不能解释为模型质量已经达到高可信主结果。
- 只有 verdict 为 `success` 且 `main_result_eligible=true` 时，才可作为 Path1/Path2 后续高可信主结果候选。
- 本 comment 不包含 provider secret；provider/model 仅以 run record 中的脱敏标识呈现。
