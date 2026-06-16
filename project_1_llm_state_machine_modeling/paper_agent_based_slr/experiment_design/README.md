# experiment_design/：评价维度种子与审稿风险

本目录在 PR-S0 阶段只冻结评价维度种子与审稿风险登记，不实现实验，不跑真实 LLM，不冻结最终指标公式、阈值或统计协议。

## 文件说明

| 文件 | 作用 |
|---|---|
| [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md) | 从 PR #101 中抽取可追踪性、事实准确性、幻觉 / 无证据支撑主张、筛选一致性、覆盖代理、透明报告、成本效率等维度种子，并说明留给 A5 的接口。 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | 登记 PR-S0 阶段可预见的 C/I/M 审稿风险、触发条件、影响和缓解入口。 |

## 边界

- PR-S0 不跑四个真实例子；真实场景设计留给 A3。
- PR-S0 不冻结指标公式、阈值或统计协议；这些留给 A5。
- PR-S0 不启动真实 LLM。后续若真实调用，必须先 `source .env` 并保留 run record。
