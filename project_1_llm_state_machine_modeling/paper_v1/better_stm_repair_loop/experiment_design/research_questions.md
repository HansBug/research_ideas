# Research Questions（R0 草案）

> R0 只提出 RQ 草案和证据需求。R4/R6 需要在真实修正预演前冻结评价门、指标骨架和统计表结构。

| RQ | 问题 | 初步证据需求 | 依赖 | 降级写法 |
|---|---|---|---|---|
| RQ1 | 初始 `STM_0` 的主要缺陷类型是什么？ | seed-level diagnostics、错误分类、来源分层。 | R1/R2/R4 | 若样本小，写成试点刻画。 |
| RQ2a | 不同反馈来源能发现哪些结构、语义或行为缺陷？ | diagnostics type、feedback source、未闭合缺陷。 | R4 | 若覆盖有限，写成反馈覆盖分析。 |
| RQ2b | 结构化反馈进入修正循环后，哪些缺陷能关闭，哪些会引入回归或振荡？ | closed defect、rejected repair、rollback、oscillation、non-convergence。 | R5/R6 | 若不稳定，报告失败模式。 |
| RQ3 | 场景 / 仿真反馈是否发现静态诊断难以发现的行为缺陷？ | simulation-only defect、trace mismatch、scenario regression。 | R4/R6 | 若证据弱，写成补充证据。 |
| RQ4 | 自动修正是否产生相对更优 `STM_k`？ | 五条件逐项台账、`STM_0` vs `STM_k`、NL-grounded adjudication。 | R6 | 任一条件失败则不计更优，只报告局限 / 失败。 |
| RQ5 | seed 来源如何影响修正效果？ | prior artifact、弱 prompt、旧模型、学生 / 人工种子分层结果。 | R1/R2/R6 | 若来源不足，写成探索性分析。 |
| RQ6 | 转换规范化风险是什么？ | 转换成功率、不可映射字段、转换前 / 后 / 修正后诊断差异。 | R3/R6 | 若转换器很薄，写成制品局限。 |

## R0 约束

1. 不得在 RQ 中写“提升质量”作为既成事实。
2. RQ4 的成功判定必须继承 [better_stm_definition.md](./better_stm_definition.md) 的五条件。
3. RQ2/RQ3/RQ4 必须报告拒绝、回滚、振荡和不收敛，而不是只报告最终成功样例。
4. RQ6 必须区分 converter normalization 与 repair-loop improvement。
