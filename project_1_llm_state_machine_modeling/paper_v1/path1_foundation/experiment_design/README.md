# experiment_design/：实验合同、执行计划与审稿风险

本目录维护 Path-1 第一篇论文从 S0a story gate 到实验与写作的执行合同。它回答“接下来怎么做、每一步什么情况下可以进入下一步、哪些 reviewer 风险必须提前处理”。

## 文件说明

| 文件 | 作用 |
|---|---|
| [experiment_inventory.md](./experiment_inventory.md) | S0a 后的 RQ、样本层级、B0-B5 condition matrix、EXT baseline 分层、metrics、human adjudication 与 run record 计划。 |
| [execution_plan.md](./execution_plan.md) | S0a/S0b 拆分后的 G0a-G8 gate-driven 后续执行方案、Mermaid 依赖图和 stop condition。 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | novelty、baseline fairness、oracle、sample bias、formal overclaim、run-record contribution 回潮、`fcstm` naming burden、soft novelty 回潮等 C/I/M 风险台账。 |

## 使用顺序

1. 先读 [experiment_inventory.md](./experiment_inventory.md)，确认 RQ 已围绕 deterministic diagnostics、scenario-level simulation feedback、structured repair decision 与 baseline-aware evaluation。
2. 再读 [execution_plan.md](./execution_plan.md)，确认 S0a pass 后才能进入 S0b / S1b / S2 / S3 / S5，不得沿用旧 venue-first 路线。
3. 每轮设计、实验结果或 paper claim 进入正文前，更新 [reviewer_risk_register.md](./reviewer_risk_register.md)。
4. 如果要运行真实 LLM / agent-loop，必须等 S3/S4 相关样本、oracle、baseline budget、runtime eligibility 冻结，并按仓库 `.env` / run record 规则执行；S0a 不跑四例真实 agent-loop。

## 当前硬约束

- 不允许在 G2/G3/G5 完成前写 result-level claim。
- 正式 oracle 必须以透明 human adjudication 为主，LLM 只能作为辅助且需要披露。
- 如果使用 PR #9 样本资产，必须明确其 historical / stress-test 性质，并在正式 sample registry 中重新冻结。
- E1/E2 只是 orchestration condition / RQ dimension，不作为独立 contribution。
- Run record 只支撑 reproducibility、debugging、eligibility 与 artifact audit，不作为 contribution。
- 后续实验与写作默认按 [../story/venue_readiness_gate.md](../story/venue_readiness_gate.md) 的 CCF-A 标准门禁执行；目标可为 fit-first CCF-B rolling journal，但 baseline、oracle、artifact 和 threats 要按 A 类审稿强度准备。
