# experiment_design/：RQ、执行计划与 reviewer risk

| 文件 | 职责 |
|---|---|
| [experiment_inventory.md](./experiment_inventory.md) | RQ/DQ、数据、指标、后续协议清单 |
| [execution_plan.md](./execution_plan.md) | G0--G10 gate 与后续 PR 拆分 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | 学术审稿风险、C/I/M 口径、当前缓解动作 |

本 PR 不跑四个真实 LLM 例子，也不调用 `.env`。原因：#85 当前阶段是 related-work / baseline screening 与 paper workspace 初始化，不是 agent-loop method PR；上游 issue #85 没要求四例真实运行。
