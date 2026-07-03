# 当前状态总账

本文件回答“现在 paper1 到底做到哪一步”。它只汇总稳定研究结论；完整事实仍以对应 JSON、registry 和 report 为准。

## 1. 总体结论

当前完成的是 **修正前准备度审计**，不是正式修正实验。

| 项 | 状态 | 说明 |
|---|---|---|
| 一手 seed registry | 已建立 | 入口：[corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md) |
| 四例静态冒烟样例 | 已建立 | 入口：[selected_seed_examples/README.md](./selected_seed_examples/README.md) |
| 原始模型到规范化 JSON | 已跑通四例，并完成 PlantUML 全量恢复摸排 | 入口：[pipeline/conversion/README.md](./pipeline/conversion/README.md) |
| 规范化 JSON 到 `.fcstm` | 四例均可导出并通过 parse / inspect | 入口：[pipeline/representation/README.md](./pipeline/representation/README.md) |
| 评价门 v0 | 已定义并 dry-run 四例 | 入口：[pipeline/evaluation/README.md](./pipeline/evaluation/README.md) |
| R5 全量摸排 | 已完成 | 入口：[pipeline/readiness_audit/README.md](./pipeline/readiness_audit/README.md) |
| R5.5 `llms-emp` 主 seed 池深度画像 | 已完成 | 入口：[reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)、[reports/2026-06-28-22-54-39-model-scope-handoff.md](./reports/2026-06-28-22-54-39-model-scope-handoff.md)、[experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./experiment_design/scope/2026-06-29-17-33-35-r5-5-scope-handoff.md) |
| R5.6 paper story / model scope / claim boundary | 已冻结 | 入口：[story/model_scope.md](./story/model_scope.md)、[experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](./experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md)、[story/claim_evidence_map.md](./story/claim_evidence_map.md) |
| R5.7.1 评价逻辑链 / claim boundary | 已冻结 | 入口：[experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md)、[reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md](./reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md)；仅为协议与主张边界，不代表 repair loop 已运行 |
| R5.7.2 Better STM / repair target 合同 | 已冻结 v0 | 入口：[experiment_design/quality_model/better_stm_definition.md](./experiment_design/quality_model/better_stm_definition.md)、[experiment_design/quality_model/repair_target_taxonomy.md](./experiment_design/quality_model/repair_target_taxonomy.md)；冻结 gate 链、三层输出模型、candidate-only 纪律和修复目标分类，不代表 repair loop 已运行 |
| R5.7.3 客观代理指标框架 | 已冻结 v0 | 入口：[experiment_design/metrics/objective_metric_framework.md](./experiment_design/metrics/objective_metric_framework.md)、[reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md](./reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md)；冻结指标权限、entry schema、G0--G6 gate matrix、分母 / reference / anti-gaming 和 baseline 迁移边界，不代表 repair loop 已运行 |
| R5.7.4 静态裁决 / metric dry-run | 已完成四例 static finding | 入口：[experiment_design/repair_target_adjudication/README.md](./experiment_design/repair_target_adjudication/README.md)、[reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](./reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md)；验证 0000 / 0001 / 0045 / 0018 四例如何消费 R5.7.2 taxonomy 与 R5.7.3 metric permission；不生成 `STM_k`，不产生正式 `valid_run` 或 Better STM 成功率 |
| 真实修正循环 | 未完成 | 后续阶段实现；当前没有 `STM_k` 主实验结果 |
| Better STM 主结果 | 未完成 | 需要真实修正、回归、人工/结构化裁决后才能判定 |

## 2. Seed 资源现状

R5 全量摸排后的方向性结论：后续主实验在 R5.5/R5.6 阶段设计选定并优先围绕 `llms-emp-stm-subset` 深度推进。它满足 `<NL, LLM-generated STM_0>` 硬边界，且具备 10 个唯一 NL × 6 个 LLM 输出的可比较结构；这是一项阶段性主 seed 池选择，不是对所有候选资源的客观排名。完整 60 case 状态表与问题谱系见 [reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)，本文件 §4.3 也给出当前深度画像摘要；R5.5 深度画像与边界交接见 [reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)、[reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) 与 [reports/2026-06-28-22-54-39-model-scope-handoff.md](./reports/2026-06-28-22-54-39-model-scope-handoff.md)。R5.5.2 全局重跑还把 `unified_uml_state_train_0265` 从 `blocked` 带到 `partial`，但这只是 synthetic collateral conversion audit fact，不改变 `llms-emp` 主 seed 定位。

| 角色 | 条目 | 可用数量 / 特征 | 当前处理 |
|---|---|---|---|
| 可直接复验的一手 `NL + STM_0` | `llms-emp-stm-subset` | 60 个 LLM-generated PlantUML pair；10 个唯一 NL × 6 个 LLM 输出；R5.5.2：16 converted / 44 partial / 0 blocked；cluster 时间等级为 8 个 T0、1 个 T0.5、1 个 T1 | 作为 R6/R7 主实验优先 seed 池；必须隔离 reference / checking 后结果，并按 10 个 NL cluster 报告；Digital Camera 仍作为 supplementary stress，不支撑 T0 主 claim；R5.5.2 的 blocked 恢复只算 conversion readiness，不算 repair gain |
| 可直接复验的一手 `NL + STM_0` | `sefm-llm-state-machine` | 9 个 NL description，但只有 1 个 SSC7 generated Umple 输出 | 可作可读冒烟 / 小样例；不能按 8 或 9 个 generated pair 计算 |
| 可直接复验的一手 `NL + STM_0` | `unified-uml-multimodal-validation` | 999 行 raw；989 个有效 generated PlantUML pair；10 个 generation failure | 可作 synthetic stress；不能包装成真实控制系统需求 |
| 条件候选 | `ttool-ai-smd-subset` | 6 个 `NL + generated TTool XML` 条件 pair，4 个唯一 NL | 可作转换压力源；进入主实验前需冻结 T0/SMD 切片和泄漏边界 |
| 需本项目复跑 | `fsm-bench-20` | 20 个系统、252 条 NL requirements；作者未公开 generated `STM_0` | 后续若使用，必须另建 generation run record |
| 需本项目复跑 | `designing-fsm-gpt4` | 作者源码可用，但未公开冻结 `<NL, generated STM_0>` pair | 后续若使用，必须另建 generation run record |
| 相关工作 / 论文可重建 | 其余条目 | 当前没有一手机读 generated pair | 不进入现成 seed 池 |

完整主表见 [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md)。

## 3. 转换与表示现状

### 3.1 四例转换

| 样例 | 来源 | 原始格式 | R3 conversion | R4.5 `.fcstm` | 备注 |
|---|---|---|---|---|---|
| `llms-emp-gpt4o-hldcs` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 官方 SCXML 可用 |
| `llms-emp-deepseek-microwave` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 依赖 R3.1 转换前规范化 replay；raw 不覆盖 |
| `llms-emp-kimi-autonomous-collision` | LLMS-EMP | PlantUML | `converted` | parse / inspect `ok` | 较复杂 HSM / 条件标签 caveat |
| `sefm-ssc7-umple` | SEFM | Umple | `partial` | parse / inspect `ok` | `after(60)` timing loss 保留 |

### 3.2 PlantUML 全量恢复

| 指标 | 数量 |
|---|---:|
| 一手 PlantUML pair 总数 | 1049 |
| 原始官方 SCXML 已可转换 | 550 |
| 原始失败 | 499 |
| all-rules 技术通过 | 480 |
| low-risk / main eligibility 通过 | 470 |
| normalization 后仍失败 | 19 |
| source-level semantic audit 总数 | 490 |
| semantic audit pass | 481 |
| semantic audit fail | 9 |
| low-risk semantic fail | 0 |

解释：这些数字只说明 conversion eligibility，不说明 修正循环改善。

## 4. R5 全量摸排结果

事实源：[pipeline/readiness_audit/seed_sweep/sweep_report.json](./pipeline/readiness_audit/seed_sweep/sweep_report.json)。

| 指标 | 数量 |
|---|---:|
| seed entry directories | 36 |
| registry entries | 16 |
| unregistered entries | 20 |
| pair records total | 1078 |
| asset records total | 16 |
| archives | 2 |

### 4.1 entry 状态

| 状态 | entries |
|---|---:|
| `partial` | 4 |
| `needs_generation` | 2 |
| `not_applicable` | 30 |

### 4.2 pair 状态

| 状态 | pairs | 解释 |
|---|---:|---|
| `converted` | 529 | 可进入修正前 `.fcstm` 表示，但仍需保留归因 |
| `partial` | 508 | 可进入 R7 eligibility review，不能无条件进入主实验 |
| `blocked` | 19 | 剩余非 `llms-emp` 当前转换负证据，进入 R8 negative evidence 或转换器 follow-up；`llms-emp` 三个原 blocked 已在 R5.5.2 恢复为 partial，不再计入当前 blocked |
| `needs_generation` | 2 | 有 NL+code / pipeline，但作者未公开 generated `STM_0` |
| `not_applicable` | 20 | 不是作者一手 generated seed，或不属于目标形式 |


### 4.3 R5.5 `llms-emp` 深度画像

事实源：[reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./reports/2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) 给出当前 blocked recovery / 状态更新；[reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) 的 §1.1 是 10 个唯一 NL cluster 的完整历史指标结论表，§1.2 是 10 NL × 6 LLM 输出状态矩阵，§1.3 是行为特征矩阵；机器事实源仍是 pipeline 下对应 JSONL。

| 指标 | 数量 / 结论 |
|---|---|
| raw pair | 60 = 10 个唯一 NL cluster × 6 个 LLM 输出 |
| pair 状态 | 16 converted / 44 partial / 0 blocked |
| canonical / parse / inspect | 60/60 canonical converted、parse ok、inspect ok |
| cluster 时间等级 | 8 个 T0、1 个 T0.5、1 个 T1 |
| pair 时间等级 | 48 T0 / 6 T0.5 / 6 T1 |
| cluster story role | 9 个 main_candidate、1 个 supplementary_stress |
| boundary_decision | `proceed_with_supplementary`；当前无 blocked，但 Digital Camera/T1 仍为 supplementary stress |

R5.5/R5.6 的结论是：主线应围绕 T0 离散 FSM/HSM/statechart artifacts 推进；`main_candidate` 包含 T0.5，因此 headline denominator 必须过滤 `time_level=T0`（8 clusters / 48 pairs）；T0.5 仅作为 timer-like caveat under event abstraction 单独标注，不支撑 timed automata 主 claim。`condition_like_label_lowered_as_event` 只能作为 R5.7 候选 repair target，必须逐例回到 NL 与 raw `STM_0` 判定，不能把 representation symptom 直接写成已确认语义缺陷。

## 5. 四例冒烟结果

事实源：[pipeline/readiness_audit/selected_examples/smoke_report.json](./pipeline/readiness_audit/selected_examples/smoke_report.json)。

| 指标 | 数量 |
|---|---:|
| examples | 4 |
| pass | 0 |
| partial | 4 |
| blocked | 0 |

四例全部通过 R5 contract checks，但都保留为 `partial`，因为上游 R3/R4/R4.5 已记录 conversion 或 representation caveat。`partial` 不表示 smoke 未跑通；它表示后续使用时不能把这些损失当作修正收益清零。

## 6. 当前不能写的结论

1. 不能写修正循环已经有效。
2. 不能写已经生成 `STM_k` 或得到 Better STM 主结果。
3. 不能把 PlantUML normalization、canonical conversion 或 `.fcstm` lowering 的收益计入 修正循环收益。
4. 不能把 选定四例写成最终实验集合或样本上限。
5. 不能把 Unified synthetic 数据包装成真实控制系统需求。
6. 不能把 TTool XML 当成已经切好的纯 T0 状态机。

## 7. 下一步决策入口

| 后续方向 | 需要做什么 | 依赖当前产物 |
|---|---|---|
| R6 修正循环骨架 | 优先围绕 `llms-emp-stm-subset` 选 12–18 条分层样本，真正跑 `<NL, STM_i> -> feedback -> candidate -> regression` 的最小闭环 | [pipeline/readiness_audit/handoff/r5_to_r6_repair_inputs.json](./pipeline/readiness_audit/handoff/r5_to_r6_repair_inputs.json)、[reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) |
| R5.7.2 Better STM / repair target taxonomy | 已冻结 v0：Better STM gate 链、三层输出模型、11 类 taxonomy、11 字段合同、五级 `repair_action_allowed` 和 candidate-only 纪律；后续需 R5.7.4 dry-run 校准 | [experiment_design/quality_model/better_stm_definition.md](./experiment_design/quality_model/better_stm_definition.md)、[experiment_design/quality_model/repair_target_taxonomy.md](./experiment_design/quality_model/repair_target_taxonomy.md)、[story/model_scope.md](./story/model_scope.md)、[experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](./experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md) |
| R5.7.4 / R5.7.5 | R5.7.4 已完成四例静态 dry-run；R5.7.5 继续合成 R6/R7 handoff。必须继承 claim boundary、Better gate、taxonomy v0、objective metric framework v0 与 R5.7.4 evidence gap，且规则修订需由 dry-run findings 驱动 | [experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md)、[experiment_design/quality_model/better_stm_definition.md](./experiment_design/quality_model/better_stm_definition.md)、[experiment_design/quality_model/repair_target_taxonomy.md](./experiment_design/quality_model/repair_target_taxonomy.md)、[experiment_design/metrics/objective_metric_framework.md](./experiment_design/metrics/objective_metric_framework.md) |
| R7 协议 / eligibility freeze | 冻结 `llms-emp-stm-subset` A/B/C/D 分层、10-NL clustered reporting 与 conversion-aware attribution；再决定 supplementary seed 角色 | [pipeline/readiness_audit/handoff/r5_to_r7_seed_eligibility.json](./pipeline/readiness_audit/handoff/r5_to_r7_seed_eligibility.json)、[reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./reports/2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)、[reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md) |
| R8 负证据 / 主实验前清理 | 处理剩余非 `llms-emp` blocked、missing、not_applicable、needs_generation；`llms-emp` 原 3 个 blocked 已转为 partial | [pipeline/readiness_audit/handoff/r5_to_r8_negative_evidence.json](./pipeline/readiness_audit/handoff/r5_to_r8_negative_evidence.json) |
| generation follow-up | 对 `fsm-bench-20` / `designing-fsm-gpt4` 这类 NL+code 来源复跑并建立 run record | seed registry 中的 仅流水线 条目 |
