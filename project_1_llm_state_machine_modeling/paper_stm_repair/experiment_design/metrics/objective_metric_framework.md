# R5.7.3 客观代理指标框架 v0

> **定位**：本文件冻结 R5.7.3 的客观代理指标合同，回答“在 R5.7.2 的 Better STM gate 链下，哪些可量化指标可以作为 supporting evidence，如何计算、如何分层、如何防止刷指标，以及哪些内容必须留给 R7 预注册实验继续冻结”。本文件不运行 repair loop，不生成 `STM_k`，不报告 repair effectiveness，也不把 `.fcstm` / `pyfcstm` / converter 写成论文方法贡献。
>
> **证据引用说明**：正文中的 `[src-*]`、`[dec-*]`、`[clm-*]`、`[cmd-*]` 是文末审计附录中的稳定 ASCII 证据键，不按数字重排。

## 1. 一句话结论

R5.7.3 将客观指标定义为 **Better STM 判定链中的可审计证据层**：指标可以支持 G0--G6 gate、触发语义裁决、暴露风险和帮助 R7/R8 统计，但不能绕过 R5.7.2 的 `NL + raw STM_0 + canonical STM_0 + STM_k + change ledger + evidence bundle` 语义裁决，也不能单独产生 `better` verdict [dec-q1][dec-q13]。

因此，任何指标 entry 至少必须写清：它属于哪个指标族、在哪个 gate 使用、权限是什么、分母是哪一层、偏序方向是什么、适用 T0/T0.5/T1 哪个 scope、证据来自哪里、有哪些刷指标风险、是否需要语义裁决、不能外推出什么 [dec-q1][dec-q4][dec-q12]。

## 2. 指标权限与非目标

### 2.1 五级 `metric_permission`

| `metric_permission` | 含义 | 典型例子 | 是否可直接产生 Better verdict |
|---|---|---|---|
| `hard_gate` | 硬准入或硬阻断条件。 | schema invalid、parse invalid、run record 缺失、关键 source evidence 缺失。 | 否，只决定能否进入评价或是否协议无效。 |
| `supporting_evidence` | 支持 G3/G4/G5 判断的辅助证据。 | guard/action fidelity 提升、traceability coverage 提升、target closure 改善。 | 否。 |
| `trigger_only` | 只触发 semantic adjudication、人工复查或 failure analysis。 | action 数骤降、guard 消失、关键 scenario regression。 | 否。 |
| `report_only` | 只进入报告、效率、稳定性或 related-work 背景分析。 | token cost、runtime、文本相似度、conversion audit cost。 | 否。 |
| `forbidden` | 禁止用于某类 gate 或结论。 | conversion success 证明 repair gain、overall F1 单独证明 Better。 | 否，且必须显式禁止。 |

`trigger_only` 特别容易误用：它只说明“必须进一步裁决”，不改变 `better_adjudication_outcome`；裁决结果仍由 R5.7.2 的 G5 semantic gate 产出 [dec-q1][src-better]。

### 2.2 明确非目标

本文件不冻结以下内容 [dec-q12]：

| 内容 | R5.7.3 状态 | 原因 |
|---|---|---|
| numeric thresholds | `r7_to_freeze` | 需 R7 预注册，不能拍脑袋设阈值。 |
| statistical test plan | `r7_to_freeze` | 需正式样本、主表和假设后确定。 |
| effect size plan | `r7_to_freeze` | 需 R7/R8 结果协议。 |
| final eligibility filter | `r7_to_freeze` | R5.7.3 只定义指标，不冻结最终样本 eligibility。 |
| final success denominator | `forbidden_in_r573` | 当前无真实 `STM_k` / no repair run。 |
| repair effectiveness result | `forbidden_in_r573` | 当前无真实运行证据。 |
| Better STM success rate | `forbidden_in_r573` | 当前无 R7/R8 adjudicated outcomes。 |
| overall quality score / weighted score | `forbidden_in_r573` | 会掩盖 guard/action/traceability 局部退化。 |

## 3. 指标 entry schema v0

每个 R7/R8 可消费的 metric entry 至少包含以下字段 [dec-q12]：

| 字段 | 必填 | 说明 |
|---|---:|---|
| `metric_id` | 是 | 稳定 ASCII id。 |
| `metric_family` | 是 | 见 §4 的 v0 指标族。 |
| `metric_definition` | 是 | 中文定义，说明输入、输出和可解释范围。 |
| `metric_permission` | 是 | `hard_gate / supporting_evidence / trigger_only / report_only / forbidden`。 |
| `gate_position` | 是 | G0--G6 中的默认使用位置；可多值，但必须解释。 |
| `denominator_layer` | 是 | `pre_registered_pool / scope_pool / evaluation_eligible_pool / adjudicated_pool / target_instance_ledger / scenario_ledger / run_ledger / baseline_reference_only`。 |
| `aggregation_level` | 是 | `pair / cluster / llm_family / target_instance / scenario / run / report_only`。 |
| `reference_type` | 是 | `parser_schema / canonical_stm0_preservation / adjudicated_target_set / confirmed_target_ledger / scenario_oracle / nl_source_span / run_record / baseline_reference_only / not_required`。 |
| `fallback_when_no_reference` | 是 | 无合法 reference set 时如何降级。 |
| `ordering_relation` | 是 | 机器可读偏序，见 §7。 |
| `scope_applicability` | 是 | `T0_main / T0_5_caveat / T1_stress_or_excluded / cross_scope_report_only`。 |
| `headline_inclusion` | 是 | `yes_if_eligible / no_caveat_only / no_stress_or_excluded / report_only`。 |
| `evidence_source` | 是 | 指向文件、ledger、run record、PR 决策或 baseline paper。 |
| `evidence_confidence` | 是 | `verified_source / needs_recheck / not_ingested / derived_from_decision / future_run_required`。 |
| `gaming_risk_tag` | 是 | 见 §8 的 risk tag；可多值。 |
| `risk_trigger_condition` | 是 | 什么情况下触发风险检查。 |
| `risk_required_evidence` | 是 | 风险确认所需 evidence bundle。 |
| `risk_gate_impact` | 是 | 风险会影响 G2/G3/G4/G5/G6 哪些 gate。 |
| `semantic_adjudication_required` | 是 | `always / when_triggered / no_but_report / forbidden`。 |
| `forbidden_extrapolation` | 是 | 不能由该指标推出的主张。 |
| `freeze_status` | 是 | `frozen_v0 / provisional_dry_run_to_validate / r7_to_freeze / future_optional / forbidden_in_r573`。 |
| `downstream_owner` | 是 | R5.7.4 / R5.7.5 / R7 / R8 / report-only。 |

## 4. v0 指标族

| `metric_family` | 中文名 | 默认用途 | 默认权限 | 代表性 metric id |
|---|---|---|---|---|
| `readiness_artifact_validity` | 制品有效性 | 判断 `STM_0^{can}` / `STM_k` 是否可评价。 | `hard_gate` | `schema_validity_status`、`parse_validity_status`、`inspect_validity_status`。 |
| `provenance_reporting_completeness` | 证据链与报告完整性 | 判断 source、hash、ledger、run record、报告证据是否完整。 | `hard_gate` / `report_only` | `evidence_bundle_completeness`、`change_ledger_presence`、`denominator_declared`。 |
| `diagnostics` | 工具诊断 | 观察 parse / semantic / design / scenario diagnostics 的阻塞与改善。 | `supporting_evidence` / `trigger_only` | `blocking_diagnostic_count_delta`、`unknown_diagnostic_flag`。 |
| `structural_element` | 状态机结构元素 | 分槽位观察 state、transition、event、guard、action、hierarchy、trace link。 | `supporting_evidence` | `slot_fidelity_state`、`slot_fidelity_guard`、`event_guard_action_folding_risk`。 |
| `traceability_grounding` | 追踪与需求落地 | 检查元素是否能回到 `NL` / raw `STM_0` / source label。 | `supporting_evidence` / `trigger_only` | `trace_link_coverage`、`untraced_addition_count`。 |
| `scenario_behavior` | 场景与行为义务 | 支持 no-regression、局部行为改善和关键义务检查。 | `supporting_evidence`；关键负例可触发 hard negative | `critical_scenario_regression_flag`、`scenario_obligation_pass_status`。 |
| `semantic_target_closure` | 修复目标闭合 | 统计 must/should/monitor/not-target/out-of-scope 分层闭合。 | `supporting_evidence` | `must_fix_closure_rate`、`should_fix_improvement_rate`。 |
| `cost_stability` | 成本与稳定性 | 记录 token、runtime、retry、rollback、oscillation。 | `report_only` | `token_cost_per_valid_run`、`retry_count`、`rollback_rate`。 |
| `baseline_migration_or_textual_similarity` | baseline 迁移与弱相似度 | 只解释相关工作指标来源或弱辅助信号。 | `report_only` / `forbidden` 于质量 verdict | `source_metric_mapping_entry`、`textual_similarity_auxiliary`。 |

降级规则：`textual_similarity`、conversion success、LLM-as-Judge 分数、overall aggregate score 和 pass@k 不进入核心客观质量指标。它们只能作为 weak auxiliary、semantic adjudication provisional evidence、cost/stability 或 related-work 背景，并且不得推出 Better STM [dec-q2][dec-q5][dec-q6]。

## 5. G0--G6 gate × metric matrix

`objective metrics` 必须放入 R5.7.2 的 Better STM gate 链，而不是另起一套评分系统 [dec-q13]。

| metric family | G0 scope | G1 readiness | G2 attribution | G3 no-regression | G4 improvement | G5 semantic | G6 reporting |
|---|---|---|---|---|---|---|---|
| `readiness_artifact_validity` | `forbidden` | `hard_gate` | `supporting_evidence` | `forbidden` | `forbidden` | `forbidden` | `supporting_evidence` |
| `provenance_reporting_completeness` | `supporting_evidence` | `hard_gate` | `hard_gate` | `trigger_only` | `forbidden` | `supporting_evidence` | `hard_gate` |
| `diagnostics` | `forbidden` | `supporting_evidence` | `trigger_only` | `trigger_only` | `supporting_evidence` | `trigger_only` | `report_only` |
| `structural_element` | `forbidden` | `forbidden` | `trigger_only` | `supporting_evidence` | `supporting_evidence` | `supporting_evidence` / `trigger_only` | `report_only` |
| `traceability_grounding` | `forbidden` | `supporting_evidence` | `supporting_evidence` | `supporting_evidence` / `trigger_only` | `supporting_evidence` | `supporting_evidence` / `trigger_only` | `hard_gate` if evidence missing |
| `scenario_behavior` | `forbidden` | `forbidden` | `trigger_only` | `hard_gate` for critical regression; otherwise `supporting_evidence` | `supporting_evidence` | `supporting_evidence` / `trigger_only` | `report_only` |
| `semantic_target_closure` | `forbidden` | `forbidden` | `trigger_only` | `trigger_only` | `supporting_evidence` | `supporting_evidence` / `trigger_only` | `report_only` |
| `cost_stability` | `forbidden` | `report_only` | `report_only` | `forbidden` | `report_only` | `forbidden` | `report_only` |
| `baseline_migration_or_textual_similarity` | `forbidden` | `report_only` | `report_only` | `forbidden` | `report_only` | `forbidden` | `report_only` |

单项指标可以在不超过该 family 权限上限的前提下细化 override；override 必须记录 evidence 与理由。G0 只做 scope routing，G1 只做可评价性，G2 只做归因，G3/G4/G5 才消费质量相关 evidence，G6 只做审计完整性 [dec-q13]。

## 6. structural slot 与 folding risk

`structural_element` 必须拆成 7 个槽位 [dec-q3]：

```text
state / transition / event / guard / action / hierarchy_or_pseudostate / trace_link
```

| slot | 默认用途 | 默认权限 | 典型风险 |
|---|---|---|---|
| `state` | 状态覆盖、冗余、命名、边界。 | `supporting_evidence` | 删除需求相关状态换取简单模型。 |
| `transition` | 迁移源/目标/连通性/义务。 | `supporting_evidence` | 删除复杂迁移以减少 diagnostics。 |
| `event` | trigger / event 抽象。 | `supporting_evidence` | 把 guard/action 全塞进 event label。 |
| `guard` | 条件、布尔表达式、变量比较。 | `supporting_evidence` / `trigger_only` | 无 NL 证据新增 guard；或把 guard folding 洗白。 |
| `action` | 输出、赋值、显示、计数器更新。 | `supporting_evidence` / `trigger_only` | 把 UI 文本强行 action 化，或删除 action。 |
| `hierarchy_or_pseudostate` | HSM 层级、choice/junction/initial/final、pseudo-state relay。 | `supporting_evidence` / `trigger_only` | 用可驻停 state 代替应瞬时通过的 pseudo-state。 |
| `trace_link` | 元素到 `NL` / raw label 的证据连接。 | cross-cutting + `traceability_grounding` | untraced additions 或 trace loss。 |

示例：若 raw label 为 `buttonPressed [battery_ok] / motor_on`，候选只保留 `event="buttonPressed [battery_ok] / motor_on"`，则至少记录：

```text
event_present = true
guard_structured = false
action_structured = false
folding_risk = true
```

该风险默认是 `trigger_only` 或 negative supporting evidence，必须进入 G3/G5 evidence bundle，不能因 event present 或 overall F1 改善而被覆盖 [dec-q3][dec-q8]。

## 7. reference、分母与偏序

### 7.1 metric-specific reference

R5.7.3 不设统一 gold STM；不同指标使用不同合法 reference [dec-q4]。

| 指标类型 | 合法 reference |
|---|---|
| readiness / artifact validity | parser、schema、inspector、required artifact checklist。 |
| provenance / report completeness | source link、conversion ledger、run record、metric record checklist。 |
| no-regression | canonical `STM_0`、critical scenarios、trace preservation evidence。 |
| structural slot improvement | adjudicated target set、repair target evidence、slot-level expected elements。 |
| repair target closure | confirmed target ledger / target-instance ledger。 |
| scenario / behavior | scenario oracle、expected trace、pre-registered critical obligation。 |
| traceability / grounding | NL span、raw STM source evidence、source element link。 |
| cost / stability | attempted run / valid run record。 |
| external baseline comparison | baseline paper 自身 reference 逻辑，只作评价方法借鉴，不迁移为本论文主 reference。 |

禁止把 canonical `STM_0` 当作统一 gold；canonical `STM_0` 是 repair 起点和 no-regression reference，不是“越像越好”的目标 [dec-q4]。

### 7.2 P/R/F1 使用条件与降级

P/R/F1 只在存在明确 reference set 时使用，例如 adjudicated target set、confirmed repair target set、scenario oracle 或可复核 baseline reference set。若 reference set 不明确，必须降级 [dec-q4]。

| 无 reference 的情形 | 合法降级 |
|---|---|
| 无 gold guard set | `guard_count_delta`、`guard_structured_presence`、`folding_risk`、semantic adjudication。 |
| 无 gold action set | `action_structured_presence`、target closure、semantic adjudication。 |
| 无 gold hierarchy set | `hierarchy_preservation_status`、`pseudostate_loss_flag`。 |
| 无 gold trace set | `trace_link_coverage`、`untraced_addition_count`。 |
| 无 scenario oracle | `scenario_not_available` / `unknown`；不得计算 pass rate。 |
| 只存在 canonical `STM_0` | 用于 no-regression / preservation / diff attribution，不得作为“越像越好”的 gold。 |

### 7.3 `denominator_layer`

| 指标 / 统计 | 默认分母层 |
|---|---|
| seed/source coverage | `pre_registered_pool` |
| scope counts / T0-T0.5-T1 routing | `scope_pool` |
| parse/readiness / artifact validity | `evaluation_eligible_pool` 或 readiness ledger；必须说明 failed artifacts 去向。 |
| Better outcome / semantic adjudication | `adjudicated_pool` |
| repair target closure | `target_instance_ledger`；不得偷用 pair denominator。 |
| scenario pass rate | `scenario_ledger` / evaluation-eligible scenario set。 |
| cost / stability | `run_ledger`，区分 attempted run 与 valid run。 |
| baseline metric migration | `baseline_reference_only`，不得混入本论文实验 denominator。 |

禁止跨层直接相除；尤其禁止用 `T0 = 48 pairs` 直接作为 final eligible 或 success denominator [dec-q4][src-eval-logic]。

### 7.4 `ordering_relation`

`ordering_relation` 只描述单个指标自身方向，不提升指标权限 [dec-q7]。

| 类型 | 写法 | 示例 | 注意 |
|---|---|---|---|
| `boolean_true_better` | true 优于 false。 | `schema_valid=true`。 | 仅 hard gate / readiness。 |
| `lower_is_better` | 越小越好。 | `blocking_diagnostic_count`、`untraced_addition_count`。 | 需防止语义删除刷低。 |
| `higher_is_better_with_reference` | 有 reference set 时越高越好。 | slot-level F1。 | 无 reference 必须降级。 |
| `set_inclusion_or_closure` | 集合闭合 / 包含关系。 | must-fix targets closed。 | 按 target-instance 分层。 |
| `ordinal_status` | 枚举状态有局部偏序。 | `closed > improved > unchanged`，但 `unknown` 不可比。 | 不得强行总分。 |
| `non_comparable_report_only` | 只报告不可排序。 | token cost vs quality、text similarity。 | 不进入 Better verdict。 |
| `trigger_only_no_order` | 无“更好”方向，只触发裁决。 | `folding_risk=true`。 | 不得直接判结果。 |

R5.7.3 禁止 overall score、weighted score 和跨 family 总分；如后续 R7 需要 primary/secondary endpoints，必须另行预注册 [dec-q7][dec-q12]。

## 8. anti-gaming 风险模型

### 8.1 v0 风险标签

| `gaming_risk_tag` | 典型触发 | 必须检查什么 | 影响 gate |
|---|---|---|---|
| `semantic_deletion` | diagnostics / scenario 表面改善但 state/transition/action 大幅减少。 | 是否删除 NL 明示行为。 | G3/G5。 |
| `guard_action_event_folding` | 条件 / 效果全部落入 event label。 | raw label、NL span、guard/action evidence。 | G4/G5。 |
| `over_repair` | 新增无 trace 行为、改写非目标元素。 | change ledger 与 trace。 | G3/G5。 |
| `under_repair` | must/should target 未闭合或只修表示层症状。 | target-instance closure。 | G4/G5。 |
| `trace_loss` | trace link 减少或新增元素无 source。 | trace map 与 source evidence。 | G2/G5/G6。 |
| `conversion_laundering` | raw -> canonical 改善被写成 repair gain。 | conversion ledger 与 change ledger 分离。 | G2/G6。 |
| `hierarchy_pseudostate_loss` | HSM / pseudo-state 被 flatten 或变成可驻停 state。 | hierarchy / pseudostate evidence。 | G3/G5。 |
| `scenario_overfitting` | 只优化少数场景，未测需求退化。 | critical scenario + NL coverage。 | G3/G5。 |
| `textual_similarity_misuse` | 文本相似度被用作行为正确性。 | 禁止外推。 | G5/G6。 |

### 8.2 风险状态与证据包

风险标签本身不直接判定 Better / not_better。风险状态采用：`flag_raised / cleared / confirmed / unknown` [dec-q8]。

| 风险状态 | 允许动作 | 禁止动作 |
|---|---|---|
| `flag_raised` | 触发 G3/G4/G5/G6 检查并要求补 evidence bundle。 | 直接判 `not_better` 或直接忽略。 |
| `cleared` | 允许该指标按原 `metric_permission` 使用。 | 把 cleared 写成额外改善收益。 |
| `confirmed` | 作为对应 gate 的负证据，由 gate 输出 `not_better / partial / unknown`。 | 绕过 gate 直接生成最终 verdict。 |
| `unknown` | 进入 unknown / limitation / failure ledger。 | 静默按 pass、静默删除或计入 success。 |

风险确认最低证据包为：

```text
NL + raw STM_0 + canonical STM_0 + STM_k + change ledger + trace / scenario / diagnostics
```

## 9. scope、汇总层级与 target closure

### 9.1 T0 / T0.5 / T1 指标权限

| `scope_applicability` | 含义 | `headline_inclusion` | 指标权限 |
|---|---|---|---|
| `T0_main` | 离散 FSM / HSM / 离散 statechart 子集。 | `yes_if_eligible` | 可进入 T0 主表，但仍需 R7 eligibility 与 adjudication。 |
| `T0_5_caveat` | timer-like cue / timeout event / tick-counter abstraction caveat。 | `no_caveat_only` | 可单列表，允许 caveat-tier analysis；不得写 timed automata。 |
| `T1_stress_or_excluded` | timed / hybrid / T1-ish stress 或 out-of-scope。 | `no_stress_or_excluded` | 只进 stress / limitation / exclusion ledger；不进入 Better quality comparison。 |
| `cross_scope_report_only` | 仅做资源画像或 related-work 背景。 | `report_only` | 不进入 headline。 |

T0.5 可增加辅助字段 `temporal_cue_type = timeout_event / tick_counter / ambiguous_timer_text / clock_like_out_of_scope`，但不得用该辅助字段把 T0.5 升级为 T0 headline [dec-q10]。

### 9.2 pair / cluster / LLM-family 汇总

| `aggregation_level` | 用途 | 禁止写法 |
|---|---|---|
| `pair` | 最小 repair attempt：`<nl_cluster_id, llm_family, raw_pair_id, canonical_stm0_id, stmk_id, run_id>`。 | 不得从 pair 单项指标直接推出 Better。 |
| `cluster` | 同一 NL 下 6 个 source STM 输出的 outcome distribution。 | 不得只报 `any_better` 掩盖失败 pair。 |
| `llm_family` | source STM bias / repair difficulty 辅助分析。 | 不得写成 LLM 排行榜或本论文核心贡献。 |
| `target_instance` | target closure 最小统计单元。 | 不得用 pair denominator 替代。 |
| `scenario` | scenario oracle / trace 统计单元。 | 无 oracle 时不得计算 pass rate。 |
| `run` | cost / stability / rollback / retry。 | 不得用 valid run denominator 掩盖 attempted failures。 |

R7/R8 主结果必须同时保留 pair-level 和 cluster-level；LLM-family-level 只作辅助分析 [dec-q9]。

### 9.3 semantic target closure

禁止单一 `target_closure_rate`；必须按实例级 `repair_action_allowed` 分层 [dec-q11]。

| 分层指标 | 分母 | 分子 | 用途 |
|---|---|---|---|
| `must_fix_closure_rate` | adjudicated `must_fix` target instances | `closure_status=closed` | 判断关键 target 是否闭合，直接影响 G5。 |
| `should_fix_improvement_rate` | adjudicated `should_fix` target instances | `closed` 或 `improved` | 支撑局部 improvement / partial 分析。 |
| `monitor_stability_rate` | `monitor` target instances | `unchanged` 或 cleared 后无 over-repair | 证明未把 candidate-only 现象乱修。 |
| `not_repair_target_respect_rate` | `not_repair_target` instances | `not_applicable` 或 unchanged | 证明没有 over-repair。 |
| `out_of_scope_exclusion_count` | `out_of_scope` instances | `not_applicable` / excluded | scope / limitation / stress ledger，不进 Better rate。 |

`closure_status` 主枚举为 `closed / improved / unchanged / worsened / not_applicable / unknown`。closure 统计必须消费实例级 override 后的 `repair_action_allowed`；若实例值不同于类级默认值，必须记录 `repair_action_override_reason` [dec-q11][src-taxonomy]。

## 10. baseline 指标迁移表

R5.7.3 使用奥卡姆剃刀：如无必要，不增指标实体；只保留迁移价值高、迁移成本可控、能落到当前可审计结构的来源 [dec-q6]。

| source_work | source_metric_id / 评价逻辑 | migration_role | target_metric_family | target_metric_id / 迁移内容 | evidence_status | 禁止外推 |
|---|---|---|---|---|---|---|
| `llms_emp` | `llms_emp.T_G` | `core_metric_source` | `cost_stability` | `generation_or_repair_time_cost`；R7 后用于 cost/stability，不代表质量。 | `verified_source` for metric definitions | 不把生成时间低写成模型更好。 |
| `llms_emp` | `llms_emp.Acc_P` | `core_metric_source` | `readiness_artifact_validity` | 不沿用 `Acc_P` 名称；迁移为 `Acc(format)` / `artifact_validity_rate`。 | `verified_source` for metric definitions | 不把 PlantUML 格式准确率写成本论文语义质量。 |
| `llms_emp` | `llms_emp.Acc_S` | `core_metric_source` | `readiness_artifact_validity` | 不沿用 `Acc_S` 名称；迁移为 `Acc(schema)` / `representation_validity_rate`。 | `verified_source` for metric definitions | 不把 SysML grammar accuracy 写成 Better STM。 |
| `llms_emp` | `llms_emp.F1` | `core_metric_source` | `structural_element` / `semantic_target_closure` | 只迁移“有 reference set 时可计算 slot-level P/R/F1”的思想。 | `verified_source` for metric definitions | 不迁移原文数值为本论文结果；无 reference 不强算 F1。 |
| `llms_emp` | Phase-II feedback resolution | `core_metric_source` | `semantic_target_closure` | 迁移为 issue / target closure：must-fix closed、should-fix improved、unresolved target。 | `verified_source` for metric definitions | 不照搬原文 hallucination taxonomy 为本论文 taxonomy。 |
| Structure/Event | states / transitions / guards / actions / hierarchy P/R/F1 | `core_metric_source` | `structural_element` | 迁移 slot-level structural metrics 思想，特别是 guard/action/hierarchy 分槽位。 | `needs_recheck` before final R7 use | 不用 overall F1 掩盖局部退化。 |
| Designing FSM | oracle / checking sequence / trace comparison | `supporting_design_note` | `scenario_behavior` | 有 oracle 时可做 scenario / behavior 评估；无 oracle 不强算。 | `needs_recheck` | 随机 DFSM oracle success 不代表真实控制系统 repair。 |
| TTool-AI | expert feedback / scoring | `supporting_design_note` | semantic adjudication design | 启发 G5 human / structured adjudication。 | `needs_recheck` | expert score 不进入 objective metrics。 |
| Nimbus | strict matching / count discipline | `supporting_design_note` | anti-gaming | 提醒 count/F1 虚高风险。 | `needs_recheck` | strict matching 不能否定语义等价表达。 |
| Umple | compile / pass@k / textual similarity | `supporting_design_note` | readiness / cost warning | 只提示 artifact validity 与 usability。 | `needs_recheck` | compile / pass@k / Levenshtein / CodeBLEU 不证明语义正确。 |
| Agentic Flow FSM | protocol FSM extraction P/R/F1 | `background_only` | related work | 只作背景。 | `needs_recheck` | 不外推到控制系统 STM repair。 |
| Pushing Envelope MBSE | METEOR / SME feedback | `background_only` | related work | 只作背景或人工评价启发。 | `needs_recheck` | 文本相似度不进入核心指标。 |
| req | token accuracy / valid loss / human comparison | `background_only` | related work | 只作训练/评价背景。 | `needs_recheck` | token accuracy 不是 STM repair quality。 |
| SpecGPT 线索 | 未定位独立单论文路径 | `background_only` | none | 不进入强证据区。 | `not_ingested` | 不得写成已核验 baseline。 |

`llms_emp.Acc_P` 与 `llms_emp.Acc_S` 只可在描述源论文时使用；本论文自有指标名必须写成 `Acc(scope)` 或 descriptive id，例如 `artifact_validity_rate` / `schema_validity_rate` [dec-q5]。

## 11. 代表性 metric entries v0

| `metric_id` | family | permission | gate | denominator | aggregation | ordering | scope | headline | semantic adjudication | freeze |
|---|---|---|---|---|---|---|---|---|---|---|
| `schema_validity_status` | readiness | `hard_gate` | G1 | readiness ledger | pair/run | `boolean_true_better` | T0/T0.5/T1 routed | `yes_if_eligible` for T0 | no | `frozen_v0` |
| `parse_validity_status` | readiness | `hard_gate` | G1 | readiness ledger | pair/run | `boolean_true_better` | T0/T0.5/T1 routed | `yes_if_eligible` for T0 | no | `frozen_v0` |
| `evidence_bundle_completeness` | provenance | `hard_gate` | G2/G6 | run ledger | run | `boolean_true_better` | cross-scope | report-only gate | no | `frozen_v0` |
| `blocking_diagnostic_count_delta` | diagnostics | `supporting_evidence` / `trigger_only` | G4/G5 | evaluation_eligible_pool | pair | `lower_is_better` with deletion risk | T0_main | yes if eligible | when_triggered | `provisional_dry_run_to_validate` |
| `slot_fidelity_guard` | structural | `supporting_evidence` / `trigger_only` | G4/G5 | adjudicated target set | pair/target_instance | `higher_is_better_with_reference` or fallback | T0_main / T0_5_caveat | T0 yes; T0.5 no | when_triggered | `provisional_dry_run_to_validate` |
| `slot_fidelity_action` | structural | `supporting_evidence` / `trigger_only` | G4/G5 | adjudicated target set | pair/target_instance | `higher_is_better_with_reference` or fallback | T0_main / T0_5_caveat | T0 yes; T0.5 no | when_triggered | `provisional_dry_run_to_validate` |
| `event_guard_action_folding_risk` | structural | `trigger_only` | G4/G5 | target / risk ledger | pair/target_instance | `trigger_only_no_order` | T0_main / T0_5_caveat | no direct headline | always if raised | `frozen_v0` |
| `trace_link_coverage` | traceability | `supporting_evidence` | G5/G6 | adjudicated_pool or trace ledger | pair/target_instance | `higher_is_better_with_reference` | T0_main | yes if eligible | when changed | `provisional_dry_run_to_validate` |
| `untraced_addition_count` | traceability | `trigger_only` | G2/G5/G6 | change ledger | pair/run | `lower_is_better` | T0_main | no direct headline | always if nonzero critical | `frozen_v0` |
| `critical_scenario_regression_flag` | scenario | `hard_gate` negative / `trigger_only` | G3/G5 | scenario ledger | pair/scenario | `boolean_false_better` | T0_main / T0_5_caveat | T0 yes if eligible | always if true | `frozen_v0` |
| `must_fix_closure_rate` | semantic_target_closure | `supporting_evidence` | G4/G5 | target_instance_ledger | target_instance/pair/cluster | `set_inclusion_or_closure` | T0_main | yes if eligible | always | `frozen_v0` |
| `should_fix_improvement_rate` | semantic_target_closure | `supporting_evidence` | G4/G5 | target_instance_ledger | target_instance/pair/cluster | `ordinal_status` | T0_main / T0_5_caveat | T0 yes; T0.5 no | when unresolved | `frozen_v0` |
| `token_cost_per_valid_run` | cost | `report_only` | G6/report | run_ledger | run/llm_family | `non_comparable_report_only` | cross-scope | report_only | no | `r7_to_freeze` |
| `textual_similarity_auxiliary` | baseline/textual | `report_only` / `forbidden` for quality | report-only | baseline_reference_only | report_only | `non_comparable_report_only` | cross-scope | report_only | no | `future_optional` |

这些 entries 是 v0 合同样例，不是 R7 最终主表列。R7 可以基于 dry-run findings 和正式协议保留、拆分或降级，但不能删除本文件冻结的禁止外推与分母纪律 [dec-q12]。

## 12. R5.7.4 / R5.7.5 / R7 handoff

| 下游阶段 | 必须消费 | 必须输出 / 冻结 | 禁止事项 |
|---|---|---|---|
| R5.7.4 | 本文件 schema、指标族、gate matrix、risk tag、baseline migration 表。 | static dry-run findings ledger、schema missing fields、ambiguous metric cases、rule revision requests、v0-to-v1 proposals。 | 不报告 repair effectiveness；规则修订必须由 finding 驱动。 |
| R5.7.5 | R5.7.1 evaluation logic、R5.7.2 Better/taxonomy、本文件、R5.7.4 findings。 | R6/R7 handoff。 | 不在无 findings 情况下重写指标。 |
| R7 | 本文件的 field schema、禁止项、分母、scope、aggregation、risk。 | final eligibility、metric table columns、thresholds、statistical tests、primary/secondary endpoints。 | 不把指标替代 Better verdict，不把 T0.5/T1 混入 headline。 |
| R8 | R7 正式结果、failure / partial / unknown / stress ledger。 | 论文结果表与失败分析。 | 不隐藏失败、partial、unknown 或 protocol invalid。 |

## 13. 禁止外推清单

| 禁止外推 | 安全写法 |
|---|---|
| conversion success -> repair gain | conversion / normalization / representation bridge readiness。 |
| parse / inspect ok -> Better STM | artifact validity / A gate pass。 |
| diagnostics fewer -> semantic improvement | diagnostics improvement as supporting evidence under anti-gaming checks。 |
| overall F1 -> Better STM | slot-level P/R/F1 when reference exists; semantic adjudication required。 |
| scenario pass rate -> full semantic correctness | scenario evidence for registered obligations only。 |
| textual similarity -> behavior correctness | weak auxiliary or related-work background only。 |
| lower token / runtime -> model quality | cost / stability report-only evidence。 |
| T0.5 tick -> timed automata support | discrete timeout / tick-counter abstraction caveat。 |
| T1 stress result -> T0 headline claim | supplementary stress / limitation。 |
| LLM-family difference -> LLM ranking | source STM bias / repair difficulty auxiliary analysis。 |

## 审计附录：证据链与事实源

### A.1 上游事实源清单

| 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-eval-logic] | `r571_evaluation_logic` | [../evaluation_logic.md](../evaluation_logic.md) | md | R5.7.1 claim boundary、四层分母、A 层、归因边界、指标位置。 | §2–§10。 |
| [src-better] | `r572_better_stm_definition` | [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) | md | R5.7.2 G0--G6、三层输出、semantic gate、T0.5 caveat。 | §1–§13。 |
| [src-taxonomy] | `r572_repair_target_taxonomy` | [../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md) | md | 11 类 target、字段合同、五级 `repair_action_allowed`、target ledger。 | §1–§7。 |
| [src-model-scope] | `r56_model_scope` | [../../story/model_scope.md](../../story/model_scope.md) | md | T0/T0.5/T1、模型族、状态机抽象、禁止外推。 | §2–§6。 |
| [src-r56-handoff] | `r56_to_r57_handoff` | [../scope/r5_6_to_r5_7_handoff_constraints.md](../scope/r5_6_to_r5_7_handoff_constraints.md) | md | R5.7 必须继承的 scope 与 candidate-only 纪律。 | §1–§6。 |
| [src-case] | `llms_emp_case_matrix` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) | jsonl | 10×6 denominator、time level、readiness 当前事实。 | fields: `nl_cluster_id`、`llm_family`、`time_level`、`conversion_status`。 |
| [src-cluster] | `llms_emp_cluster_profiles` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | jsonl | cluster-level time / structure / story role。 | fields: `nl_cluster_id`、`time_level`、`structure_family`。 |
| [src-partial] | `llms_emp_partial_attribution` | [../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl](../../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl) | jsonl | representation symptom、candidate-only 与 pipeline artifact。 | fields: `r5_loss_code`、`primary_attribution`、`r5_7_candidate_only`。 |
| [src-llms-emp-desc] | `llms_emp_desc` | [../../../baselines/llms_emp/DESC.md](../../../baselines/llms_emp/DESC.md) | md | `llms_emp` 指标定义与 Phase-II feedback 摘要。 | lines around Evaluation Metrics / Phase-II。 |
| [src-llms-emp-paper] | `llms_emp_paper_content` | [../../../baselines/llms_emp/paper_content.txt](../../../baselines/llms_emp/paper_content.txt) | txt | `T_G`、`Acc_P`、`Acc_S`、F1、feedback resolution 的原文抽取入口。 | search `Evaluation Metrics`、`Acc_P`、`Acc_S`、`F1`。 |
| [src-structure-event] | `structure_event_desc` | [../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md](../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/DESC.md) | md | slot-level P/R/F1 评价思想。 | `states / transitions / guards / actions / hierarchical states`。 |

### A.2 决策键清单

| 引用键 | 来源 | 冻结结论 |
|---|---|---|
| [dec-q1] | [PR #141 Q1 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4874342749) | 五级 `metric_permission` 与 G0--G6 定位纪律。 |
| [dec-q2] | [PR #141 Q2 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4874416737) | v0 纳入 8 类核心指标族，并降级 textual similarity / conversion / judge score / pass@k。 |
| [dec-q3] | [PR #141 Q3 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4875625664) | structural metrics 拆 7 槽位，记录 folding risk，hierarchy/pseudostate 是 core slot。 |
| [dec-q4] | [PR #141 Q4 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4875649554) | 无统一 gold STM；P/R/F1 只在有 reference set 时使用；必须声明分母。 |
| [dec-q5] | [PR #141 Q5 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4875897856) | `llms_emp` source metric 迁移、`Acc_P/Acc_S` 命名降级、feedback resolution -> target closure。 |
| [dec-q6] | [PR #141 Q6 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876053568) | baseline 迁移采用奥卡姆三类 role，core source 只保留 `llms_emp` 与 Structure/Event。 |
| [dec-q7] | [PR #141 Q7 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876132176) | 偏序方向、不可合成、禁止 overall weighted score。 |
| [dec-q8] | [PR #141 Q8 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876219969) | anti-gaming 风险标签、状态与证据包。 |
| [dec-q9] | [PR #141 Q9 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876266135) | pair / cluster / LLM-family 三层汇总纪律。 |
| [dec-q10] | [PR #141 Q10 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876298225) | T0 / T0.5 / T1 的指标呈现与 headline 权限。 |
| [dec-q11] | [PR #141 Q11 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876385992) | target closure 分层与 target-instance 分母纪律。 |
| [dec-q12] | [PR #141 Q12 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876508529) | 交付字段、`freeze_status` 与 R5.7.4 / R5.7.5 / R7 接口。 |
| [dec-q13] | [PR #141 Q13 comment](https://github.com/HansBug/research_ideas/pull/141#issuecomment-4876564209) | family-level G0--G6 gate × metric matrix。 |

### A.3 Claim-evidence map

| 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-r573-no-effect] | `R573-C1` | R5.7.3 不运行 repair loop、不生成 `STM_k`、不报告 Better STM 成功率或 repair effectiveness。 | prohibition | [src-eval-logic] §1/§9；[src-better] §1/§9；本文件 §2.2。 | 人工复验 + [cmd-r573-doc-links] | high | R7/R8 才能产生效果证据。 |
| [clm-r573-permission] | `R573-C2` | 客观指标必须声明五级 `metric_permission`，且不能单独产生 Better verdict。 | contract | [dec-q1]；本文件 §2.1。 | [cmd-r573-required-terms] | high | 预注册关键负例可作 hard negative trigger，但不能推出 Better。 |
| [clm-r573-schema] | `R573-C3` | 每个 metric entry 至少需要 schema v0 中列出的字段，包含分母、偏序、scope、风险和 freeze status。 | contract | [dec-q12]；本文件 §3。 | [cmd-r573-required-terms] | high | R7 可扩展字段，但不能删除最低审计字段。 |
| [clm-r573-families] | `R573-C4` | v0 指标族覆盖 readiness、provenance、diagnostics、structural、traceability、scenario、target closure、cost、baseline/textual background。 | contract | [dec-q2][dec-q13]；本文件 §4。 | [cmd-r573-required-terms] | high | textual similarity / conversion success 是降级项。 |
| [clm-r573-gate-matrix] | `R573-C5` | 指标必须落到 G0--G6 gate × metric matrix，不另起评分系统。 | contract | [dec-q13]；本文件 §5。 | [cmd-r573-required-terms] | high | 单项 override 不能超过 family 权限上限。 |
| [clm-r573-no-gold] | `R573-C6` | 本任务不设统一 gold STM；P/R/F1 只在有明确 reference set 时使用。 | decision | [dec-q4]；本文件 §7。 | 人工复验 | high | canonical `STM_0` 是 no-regression reference，不是统一 gold。 |
| [clm-r573-risk] | `R573-C7` | anti-gaming 风险至少覆盖 semantic deletion、folding、over/under repair、trace loss、conversion laundering、hierarchy loss、scenario overfitting。 | protocol | [dec-q8]；本文件 §8。 | [cmd-r573-required-terms] | high | 风险 flag 需 evidence bundle 才能 confirmed。 |
| [clm-r573-scope-agg] | `R573-C8` | 每个统计必须声明 `scope_applicability`、`headline_inclusion`、`aggregation_level × denominator_layer`。 | protocol | [dec-q9][dec-q10]；本文件 §9。 | [cmd-r573-counts] | high | T0 scope 上限不是 success denominator。 |
| [clm-r573-closure] | `R573-C9` | target closure 禁止单一总 rate，必须按实例级 `repair_action_allowed` 分层。 | protocol | [dec-q11][src-taxonomy]；本文件 §9.3。 | [cmd-r573-required-terms] | high | 当前没有真实 target closure 结果。 |
| [clm-r573-baseline] | `R573-C10` | baseline migration 采用三类 role；core metric source 只保留 `llms_emp` 与 Structure/Event。 | decision | [dec-q5][dec-q6]；本文件 §10。 | [cmd-r573-required-terms] | medium | Structure/Event 与其他条目在 R7 前仍需原文复核；`llms_emp` 数值只作 related work。 |

### A.4 复验命令

```bash
# [cmd-r573-doc-links]
python - <<'PY'
from pathlib import Path
base = Path('project_1_llm_state_machine_modeling/paper_stm_repair')
for rel in [
    'experiment_design/metrics/objective_metric_framework.md',
    'experiment_design/metrics/README.md',
    'experiment_design/evaluation_logic.md',
    'experiment_design/quality_model/better_stm_definition.md',
    'experiment_design/quality_model/repair_target_taxonomy.md',
]:
    p = base / rel
    print(rel, p.exists(), p.stat().st_size if p.exists() else 'missing')
PY
```

```bash
# [cmd-r573-counts]
python - <<'PY'
import json, collections, pathlib
base = pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_repair')
case = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl').read_text().splitlines() if l.strip()]
clusters = [json.loads(l) for l in (base/'pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl').read_text().splitlines() if l.strip()]
print('pairs', len(case), 'clusters', len({r['nl_cluster_id'] for r in case}))
print('conversion_status', collections.Counter(r['conversion_status'] for r in case))
print('parse_status', collections.Counter(r['parse_status'] for r in case))
print('inspect_status', collections.Counter(r['inspect_status'] for r in case))
print('pair_time', collections.Counter(r['time_level'] for r in case))
print('cluster_time', collections.Counter(r['time_level'] for r in clusters))
PY
```

```bash
# [cmd-r573-required-terms]
python - <<'PY'
from pathlib import Path
p = Path('project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/metrics/objective_metric_framework.md')
text = p.read_text()
required = [
    'metric_permission', 'hard_gate', 'supporting_evidence', 'trigger_only', 'report_only', 'forbidden',
    'denominator_layer', 'aggregation_level', 'ordering_relation', 'scope_applicability', 'headline_inclusion',
    'gaming_risk_tag', 'semantic_adjudication_required', 'freeze_status',
    'readiness_artifact_validity', 'structural_element', 'traceability_grounding', 'scenario_behavior', 'semantic_target_closure',
    'event_guard_action_folding_risk', 'must_fix_closure_rate', 'should_fix_improvement_rate',
    'G0 scope', 'G1 readiness', 'G2 attribution', 'G3 no-regression', 'G4 improvement', 'G5 semantic', 'G6 reporting',
]
missing = [x for x in required if x not in text]
print('missing', missing)
raise SystemExit(1 if missing else 0)
PY
```
