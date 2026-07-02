# claim-evidence map：主张与证据门

## 1. 使用原则

每条论文主张必须有可追溯证据。R5.6 已冻结 paper story / model scope / claim boundary，但这仍然**不证明 repair-loop claim 已成立**。若后续 R6/R8 无法提供真实修正证据，R7 写作必须降级或删除对应 claim。

本文件只做 story-level claim gate；完整 scope 真源见 [model_scope.md](./model_scope.md)，R5.7.1 评价逻辑链和 claim boundary 见 [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)，实验协议和 eligibility 后续仍归 [../experiment_design/](../experiment_design/) 管理。

## 2. 主张台账

| Claim ID | 可写主张草案 | in-scope model family | 当前支持状态 | claim strength | 必需证据 | 后续 PR | 安全降级写法 | forbidden extrapolation |
|---|---|---|---|---|---|---|---|---|
| C1 | 本文定义并研究 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集；EFSM-lite 不进入 headline，只作为当前无独立样例的 future taxonomy candidate / 语义维度标签。 | R0/R5.5/R5.6 可支撑任务定义、主 seed 池画像和模型范围边界。 | task framing / main scope supported | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md)、[model_scope.md](./model_scope.md)、[../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。 | R0 / R5.5 / R5.6 / R7 | “We frame / study” 而非 “we solve”。headline scope 默认写 FSM/HSM/statechart；EFSM-lite 只能在 R7 有独立 eligible 证据后进入分层/非 headline 表述。 | 不写成一轮式 `NL -> STM` 生成论文；不外推到 timed automata、hybrid automata、arbitrary UML 或 protocol FSM；不把 EFSM-lite 写成当前已有独立数据覆盖。 |
| C2 | 结构化 diagnostics 与 scenario feedback 被设计为可集成进无人化修正循环。 | 同 C1；T0.5 只可作为 caveat / annotation。 | 仅有规划、评价门和表示链路；未实证 repair 效果；R5.7.1 已冻结它只能支撑 protocol / evaluation claim。 | protocol / evaluation claim only | pipeline diagnostics / scenario gate、[../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)、R6/R8 repair ledger、回归检查。 | R4 / R5.7.1 / R6 / R8 | “can be integrated into a repair loop” 或 “is designed to support” 而非 “guarantee improvement”。 | 不写成完整形式化验证、不写 sound model checking guarantee；不写成 repair effectiveness。 |
| C3 | `STM_k` 可在预注册条件下相对同一个 canonical `STM_0` 更优。 | 只能对 R7 eligible repair runs 生效；selected smoke examples 不自动进入主结果。 | 尚未验证；R5.7.1 冻结当前无 `STM_k` / 无真实 repair run；R5.7.2 冻结 Better STM 必须通过 G0–G6 gate、三层输出模型和 semantic adjudication，conversion readiness、A-pass、taxonomy candidate 或客观指标改善都不能替代语义裁决。 | future repair effectiveness claim only | [../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md)、[../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md)、同一 `STM_0` 对比、change ledger、人工/结构化裁决、回归检查、failure / unknown ledger。 | R5.7.1 / R5.7.2 / R5.7.4 / R6 / R7 / R8 | 在 eligible runs 中逐 gate 报告；未满足 gate 者不得计为 Better STM，只能作局部改善、partial、unknown、protocol invalid 或失败模式。 | 不把 normalization、canonical conversion、`.fcstm` lowering、parse/inspect success、metric-only improvement、pyfcstm combo 表达成功或 taxonomy 候选写成 repair-loop gain。 |
| C4 | prior artifacts 可重排为 seed source、repair-baseline / near-neighbor landscape 和 converter pressure。 | `llms-emp-stm-subset` 是 R5.5/R5.6 阶段设计选定并深度画像的主 seed 池；SEFM/Unified/TTool 分别作为 readable smoke、synthetic stress、conversion pressure / conditional supplementary。 | R1--R5.6 已有 seed registry、repair baseline 总账、conversion profile、scope report 和 model scope contract，但 eligibility 仍未最终冻结。 | preliminary evidence / resource characterization | seed 看 [../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)；baseline 看 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)；human-facing handoff 看 [../reports/SUMMARY.md](../reports/SUMMARY.md)；scope 看 [model_scope.md](./model_scope.md)。 | R1 / R2 / R3 / R5.6 / R5.7 | 若资源不足，写“可获取 artifact 子集”，并区分 seed、baseline、converter pressure、supplementary stress；不得把该设计选择写成跨所有 seed 的客观排名。 | 不把 Unified synthetic stress 包装成真实控制系统需求主池；不把 SEFM 9 个 NL 写成 9 个 generated pair。 |
| C5 | 转换规范化收益与 repair-loop 收益可以分开归因。 | 适用于所有进入 pipeline 的 seed；主结果只允许在 frozen `<NL, STM_0>` 上计 repair gain。 | R0/R5/R5.5/R5.6 已定义归因边界并有 partial attribution ledger；R5.7.1 已冻结 raw -> canonical 不计 repair gain；还没有 repair 后对照。 | methodological accounting supported, result claim pending | 转换前 / 后 / 修正后诊断计数、conversion attribution ledger、repair ledger；R5.6 禁止项见 [model_scope.md](./model_scope.md)；R5.7.1 见 [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)。 | R3 / R5 / R5.6 / R5.7.1 / R6 / R8 | 若台账不完整，只作 case analysis。 | 不把 PlantUML recovery、SCXML conversion、canonical lowering、`.fcstm` parse success 或 inspect success 计入修正收益。 |
| C6 | 修正协议能报告拒绝修复、回滚、振荡和不收敛。 | 只针对 R6/R8 真实 repair runs；不适用于 R5 readiness audit。 | 仅有 protocol requirement，尚无真实 run evidence；R5.7.1 已冻结 failure / partial / unknown / out-of-scope 必须入 ledger。 | protocol / evaluation claim only | R6/R8 repair ledger、accept / reject / rollback ledger、oscillation / non-convergence ledger 与结果统计；R5.7.1 failure reporting 纪律见 [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)。 | R5.7.1 / R6 / R8 | 若实现不完整，改写为“we log and analyze observed failure modes”。 | 不隐藏失败、回滚或 provider failure；不把 schema-invalid / replay-invalid run 纳入主成功统计；不把 partial / unknown 静默删除。 |
| C7 | 本文主实验模型范围的 R5.6 上限是 T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集，EFSM-lite 只作为 future taxonomy candidate / 语义维度标签留给 R5.7/R7 裁决。 | T0 main；T0.5 caveat；Digital Camera / T1-ish supplementary stress；timed/hybrid/arbitrary UML/protocol FSM excluded；当前 `llms-emp` 没有独立 EFSM-lite cluster。 | R5.6 已冻结 headline scope 为 FSM/HSM/离散 statechart；R7 eligibility 可进一步收窄，但不得扩大 headline claim。 | headline scope supported; final eligibility pending | [model_scope.md](./model_scope.md)、[../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md)、[../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)。 | R5.6 / R5.7 / R7 | 若 R7 只能纳入更窄子集，就写更窄 scope；EFSM-lite 默认不进入 headline，除非 R7 有独立 eligible 证据。 | 不把 T0.5/T1 变成 timed automata 支持；不把 discrete statechart subset 写成 arbitrary UML coverage；不把 EFSM-lite 写成已有独立样本族或 headline family。 |
| C8 | 本文的评价逻辑链将 task/scope、readiness、protocol/evaluation、repair effectiveness 和 limitation/negative evidence 分开，并用 R5.7.2 gate / taxonomy 防止把准备度、指标代理或 candidate target 误写成方法效果。 | 适用于 R5.7.2--R5.7.5、R6/R7/R8 所有后续协议与结果写法。 | R5.7.1 已冻结评价逻辑链；R5.7.2 已冻结 Better STM gate 与 repair target taxonomy；尚未产生任何 repair effectiveness evidence。 | protocol / claim-boundary supported | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)、[../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md)、[../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md)、[../STATUS.md](../STATUS.md)、[model_scope.md](./model_scope.md)。 | R5.7.1 / R5.7.2 / R5.7.3 / R5.7.5 / R7 | 当前只能写“评价逻辑链与 Better STM 判定合同已冻结 / will be evaluated”，不能写“方法有效”。 | 不用 A-pass、parse ok、inspect ok、客观指标总分、T0 scope 上限、conversion readiness 或 repair target candidate 支撑 Better STM 成功率。 |

## 3. 禁止 claim

| 禁止 claim | 为什么禁止 | 证据 / 规则入口 |
|---|---|---|
| 本文是首个 `NL -> STM` 生成方法。 | 与导师定调冲突，也缺乏 novelty gate。 | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md) |
| 本文提出了新的状态机 DSL。 | 会把贡献带偏；DSL 只是内部载体。 | [terminology_policy.md](./terminology_policy.md) |
| 本文完成形式化验证并保证正确性。 | 当前只计划轻量诊断 / 场景反馈，没有 soundness 证明。 | [paper_story.md](./paper_story.md) |
| 修正循环总能提升状态机质量。 | 必须报告失败、回滚、振荡和不收敛；当前尚无真实 repair 结果。 | [task_boundary.md](./task_boundary.md) |
| 转换器带来的改善属于 repair-loop 能力。 | 必须用三阶段台账分开归因。 | [model_scope.md](./model_scope.md)、[task_boundary.md](./task_boundary.md) |
| 客观指标总分、parse ok、inspect ok 或 diagnostics fewer 可以单独证明 Better STM。 | R5.7.1/R5.7.2 已冻结客观指标只能作 supporting evidence，必须回到 `NL`、canonical `STM_0`、`STM_k` 与 change ledger 做语义裁决。 | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)、[../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) |
| `T0 headline main = 8 clusters / 48 pairs` 是最终 eligible 或 success denominator。 | R5.7.1 已冻结它只是 scope / pre-eligibility 上限。 | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)、[model_scope.md](./model_scope.md) |
| partial 样例可以静默丢弃或直接等于失败。 | partial 是带 caveat 的可评价候选；failure / partial / unknown / out-of-scope / protocol invalid 都必须进入台账。 | [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)、[../experiment_design/quality_model/better_stm_definition.md](../experiment_design/quality_model/better_stm_definition.md) |
| `condition_like_label_lowered_as_event` 等 representation symptom 可以直接写成 confirmed guard/action defect。 | R5.7.2 已冻结 candidate-only 纪律：必须回到 `NL + raw STM_0 + canonical STM_0 + evidence bundle` 裁决后才能确认 repair target。 | [../experiment_design/quality_model/repair_target_taxonomy.md](../experiment_design/quality_model/repair_target_taxonomy.md) |
| 本文覆盖 timed automata / hybrid automata / arbitrary UML / protocol FSM repair。 | R5.6 已把这些排除在 headline scope 外。 | [model_scope.md](./model_scope.md) |
| T0.5 timer-like cue 证明 timed automata 支持。 | T0.5 只是 caveat / annotation，不是 clocks / timed semantics。 | [model_scope.md](./model_scope.md) |
| Digital Camera / T1-ish cluster 支撑 T0 主结果。 | R5.6 只允许其作 supplementary stress / limitation。 | [model_scope.md](./model_scope.md) |

## 4. R7 写作前检查

1. 每个 abstract / introduction claim 必须映射到上表某个 claim ID。
2. 每个 claim ID 必须在 R1--R8 中有明确证据文件或降级理由。
3. 没有实验证据的 claim 只能写成 task framing、method design 或 pilot observation。
4. 工程审计制品可以支撑 reproducibility，但不能替代方法贡献或实验结论。
5. 任何涉及模型族、时间语义、resource role 或 forbidden extrapolation 的写法，必须先对照 [model_scope.md](./model_scope.md)。
6. 任何涉及方法有效性、指标、分母或失败报告的写法，必须先对照 [../experiment_design/evaluation_logic.md](../experiment_design/evaluation_logic.md)。
7. R5.7 若新增 repair target taxonomy，必须同时更新本表的 `in-scope model family`、`claim strength`、`downgrade wording` 和 `forbidden extrapolation`。

## 5. story 文件入口

- 主线与贡献草案：[paper_story.md](./paper_story.md)
- 方法内外边界：[task_boundary.md](./task_boundary.md)
- 模型范围与 claim boundary：[model_scope.md](./model_scope.md)
- 术语与禁用表达：[terminology_policy.md](./terminology_policy.md)
