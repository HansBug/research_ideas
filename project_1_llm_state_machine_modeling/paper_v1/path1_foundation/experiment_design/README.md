# experiment_design/：实验合同、执行计划与审稿风险

本目录维护 Path-1 第一篇论文从 foundation 到实验与写作的执行合同。它回答“接下来怎么做、每一步什么情况下可以进入下一步、哪些 reviewer 风险必须提前处理”。

## 文件说明

| 文件 | 作用 |
|---|---|
| [experiment_inventory.md](./experiment_inventory.md) | RQ、样本层级、baseline / condition matrix、metrics、human adjudication 与 run record 计划。 |
| [execution_plan.md](./execution_plan.md) | G0-G8 gate-driven 后续执行方案。 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | baseline fairness、sample/reference bias、oracle weakness、claim-evidence mismatch 等 C/I/M 风险台账。 |

## 使用顺序

1. 先读 [experiment_inventory.md](./experiment_inventory.md)，确认实验对象、条件和指标。
2. 再读 [execution_plan.md](./execution_plan.md)，按 gate 推进后续 PR。
3. 每轮设计或实验结果进入 paper 前，更新 [reviewer_risk_register.md](./reviewer_risk_register.md)。

## 当前硬约束

- 不允许在 G2/G3/G5 完成前写 result-level claim。
- 正式 oracle 必须以透明 human adjudication 为主，LLM 只能作为辅助且需要披露。
- 如果使用 PR #9 样本资产，必须明确其 historical / stress-test 性质，并在正式 sample registry 中重新冻结。
