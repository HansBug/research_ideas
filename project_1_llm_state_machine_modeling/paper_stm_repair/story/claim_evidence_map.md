# claim-evidence map：主张与证据门

## 1. 使用原则

每条论文主张必须有可追溯证据。R5.6 已冻结 paper story / model scope / claim boundary，但这仍然**不证明 repair-loop claim 已成立**。若后续 R6/R8 无法提供真实修正证据，R7 写作必须降级或删除对应 claim。

本文件只做 story-level claim gate；完整 scope 真源见 [model_scope.md](./model_scope.md)，实验协议和 eligibility 后续仍归 [../experiment_design/](../experiment_design/) 管理。

## 2. 主张台账

| Claim ID | 可写主张草案 | in-scope model family | 当前支持状态 | claim strength | 必需证据 | 后续 PR | 安全降级写法 | forbidden extrapolation |
|---|---|---|---|---|---|---|---|---|
| C1 | 本文定义并研究 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集；EFSM-lite 仅作为当前无独立样例的候选范围上限。 | R0/R5.5/R5.6 可支撑任务定义、主 seed 池画像和模型范围边界。 | task framing / main scope supported | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md)、[model_scope.md](./model_scope.md)、[../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。 | R0 / R5.5 / R5.6 / R7 | “We frame / study” 而非 “we solve”。若 R7 无 EFSM-lite eligible 样例，headline scope 写 FSM/HSM/statechart。 | 不写成一轮式 `NL -> STM` 生成论文；不外推到 timed automata、hybrid automata、arbitrary UML 或 protocol FSM；不把 EFSM-lite 写成当前已有独立数据覆盖。 |
| C2 | 结构化 diagnostics 与 scenario feedback 被设计为可集成进无人化修正循环。 | 同 C1；T0.5 只可作为 caveat / annotation。 | 仅有规划、评价门和表示链路；未实证 repair 效果。 | design claim only | pipeline diagnostics / scenario gate、R6/R8 repair ledger、回归检查。 | R4 / R6 / R8 | “can be integrated into a repair loop” 或 “is designed to support” 而非 “guarantee improvement”。 | 不写成完整形式化验证、不写 sound model checking guarantee。 |
| C3 | `STM_k` 可在预注册条件下相对同一个 `STM_0` 更优。 | 只能对 R7 eligible repair runs 生效；selected smoke examples 不自动进入主结果。 | 尚未验证；R5.6 只冻结不能把 conversion gain 算 repair gain。 | future empirical claim | 五条件台账、同一 `STM_0` 对比、人工裁决、回归检查、三阶段归因。 | R4 / R6 / R8 | 在 eligible runs 中逐条件报告；未满足五条件者不得计为 Better STM，只能作局部改善或失败模式。 | 不把 normalization、canonical conversion、`.fcstm` lowering、parse/inspect success 写成 repair-loop gain。 |
| C4 | prior artifacts 可重排为 seed source、repair-baseline / near-neighbor landscape 和 converter pressure。 | `llms-emp-stm-subset` 是 R5.5/R5.6 阶段设计选定并深度画像的主 seed 池；SEFM/Unified/TTool 分别作为 readable smoke、synthetic stress、conversion pressure / conditional supplementary。 | R1--R5.6 已有 seed registry、repair baseline 总账、conversion profile、scope report 和 model scope contract，但 eligibility 仍未最终冻结。 | preliminary evidence / resource characterization | seed 看 [../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)；baseline 看 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)；human-facing handoff 看 [../reports/SUMMARY.md](../reports/SUMMARY.md)；scope 看 [model_scope.md](./model_scope.md)。 | R1 / R2 / R3 / R5.6 / R5.7 | 若资源不足，写“可获取 artifact 子集”，并区分 seed、baseline、converter pressure、supplementary stress；不得把该设计选择写成跨所有 seed 的客观排名。 | 不把 Unified synthetic stress 包装成真实控制系统需求主池；不把 SEFM 9 个 NL 写成 9 个 generated pair。 |
| C5 | 转换规范化收益与 repair-loop 收益可以分开归因。 | 适用于所有进入 pipeline 的 seed；主结果只允许在 frozen `<NL, STM_0>` 上计 repair gain。 | R0/R5/R5.5/R5.6 已定义归因边界并有 partial attribution ledger；还没有 repair 后对照。 | methodological accounting supported, result claim pending | 转换前 / 后 / 修正后诊断计数、conversion attribution ledger、repair ledger；R5.6 禁止项见 [model_scope.md](./model_scope.md)。 | R3 / R5 / R5.6 / R6 / R8 | 若台账不完整，只作 case analysis。 | 不把 PlantUML recovery、SCXML conversion、canonical lowering 或 `.fcstm` parse success 计入修正收益。 |
| C6 | 修正协议能报告拒绝修复、回滚、振荡和不收敛。 | 只针对 R6/R8 真实 repair runs；不适用于 R5 readiness audit。 | 仅有 protocol requirement，尚无真实 run evidence。 | design claim only | R6/R8 repair ledger、accept / reject / rollback ledger、oscillation / non-convergence ledger 与结果统计。 | R6 / R8 | 若实现不完整，改写为“we log and analyze observed failure modes”。 | 不隐藏失败、回滚或 provider failure；不把 schema-invalid / replay-invalid run 纳入主成功统计。 |
| C7 | 本文主实验模型范围的 R5.6 上限是 T0 离散 FSM / HSM / 离散 UML-SysML statechart 子集，并把 EFSM-lite 作为候选 in-scope envelope 留给 R5.7/R7 裁决。 | T0 main；T0.5 caveat；Digital Camera / T1-ish supplementary stress；timed/hybrid/arbitrary UML/protocol FSM excluded；当前 `llms-emp` 没有独立 EFSM-lite cluster。 | R5.6 已冻结 scope upper envelope；R7 eligibility 可进一步收窄到 FSM/HSM/statechart only，但不得扩大 headline claim。 | scope envelope supported; final eligible scope pending | [model_scope.md](./model_scope.md)、[../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md](../experiment_design/scope/r5_6_to_r5_7_handoff_constraints.md)、[../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)。 | R5.6 / R5.7 / R7 | 若 R7 只能纳入更窄子集，就写更窄 scope；若无 EFSM-lite eligible 样例，删除或降级 EFSM-lite headline wording。 | 不把 T0.5/T1 变成 timed automata 支持；不把 discrete statechart subset 写成 arbitrary UML coverage；不把 EFSM-lite 写成已有独立样本族。 |

## 3. 禁止 claim

| 禁止 claim | 为什么禁止 | 证据 / 规则入口 |
|---|---|---|
| 本文是首个 `NL -> STM` 生成方法。 | 与导师定调冲突，也缺乏 novelty gate。 | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md) |
| 本文提出了新的状态机 DSL。 | 会把贡献带偏；DSL 只是内部载体。 | [terminology_policy.md](./terminology_policy.md) |
| 本文完成形式化验证并保证正确性。 | 当前只计划轻量诊断 / 场景反馈，没有 soundness 证明。 | [paper_story.md](./paper_story.md) |
| 修正循环总能提升状态机质量。 | 必须报告失败、回滚、振荡和不收敛；当前尚无真实 repair 结果。 | [task_boundary.md](./task_boundary.md) |
| 转换器带来的改善属于 repair-loop 能力。 | 必须用三阶段台账分开归因。 | [model_scope.md](./model_scope.md)、[task_boundary.md](./task_boundary.md) |
| 本文覆盖 timed automata / hybrid automata / arbitrary UML / protocol FSM repair。 | R5.6 已把这些排除在 headline scope 外。 | [model_scope.md](./model_scope.md) |
| T0.5 timer-like cue 证明 timed automata 支持。 | T0.5 只是 caveat / annotation，不是 clocks / timed semantics。 | [model_scope.md](./model_scope.md) |
| Digital Camera / T1-ish cluster 支撑 T0 主结果。 | R5.6 只允许其作 supplementary stress / limitation。 | [model_scope.md](./model_scope.md) |

## 4. R7 写作前检查

1. 每个 abstract / introduction claim 必须映射到上表某个 claim ID。
2. 每个 claim ID 必须在 R1--R8 中有明确证据文件或降级理由。
3. 没有实验证据的 claim 只能写成 task framing、method design 或 pilot observation。
4. 工程审计制品可以支撑 reproducibility，但不能替代方法贡献或实验结论。
5. 任何涉及模型族、时间语义、resource role 或 forbidden extrapolation 的写法，必须先对照 [model_scope.md](./model_scope.md)。
6. R5.7 若新增 repair target taxonomy，必须同时更新本表的 `in-scope model family`、`claim strength`、`downgrade wording` 和 `forbidden extrapolation`。

## 5. story 文件入口

- 主线与贡献草案：[paper_story.md](./paper_story.md)
- 方法内外边界：[task_boundary.md](./task_boundary.md)
- 模型范围与 claim boundary：[model_scope.md](./model_scope.md)
- 术语与禁用表达：[terminology_policy.md](./terminology_policy.md)
