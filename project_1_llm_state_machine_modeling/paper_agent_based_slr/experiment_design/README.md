# experiment_design/：评价维度种子与审稿风险

本目录在 A0 阶段只冻结评价维度种子与 reviewer 风险登记，不实现实验，不跑真实 LLM，不冻结最终指标公式、阈值或统计协议。

## 文件说明

| 文件 | 作用 |
|---|---|
| [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md) | 从 PR #101 中抽取 traceability、factuality、hallucination、screening consistency、coverage proxy、透明报告、成本效率等维度种子，并说明留给 A5 的接口。 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | 登记 A0 阶段可预见的 C/I/M 审稿风险、触发条件、影响和缓解入口。 |

## 边界

- A0 不跑四个真实例子；真实场景设计留给 A3。
- A0 不冻结指标公式 / 阈值 / 统计协议；这些留给 A5。
- A0 不启动真实 LLM。后续若真实调用，必须先 `source .env` 并保留 run record。
