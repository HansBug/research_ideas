# experiment_design/：评价维度种子与审稿风险

本目录在 PR-S0-v2 阶段只冻结评价维度种子与审稿风险登记，不实现实验，不跑真实 LLM，不冻结最终指标公式、阈值或统计协议。

## 文件说明

| 文件 | 作用 |
|---|---|
| [evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md) | 冻结 S0-v2 评价维度种子：dimension pattern stability、backfill cost、field-level evidence accuracy、statistical correctness、candidate-to-final transition、content/process evidence separation、process-data metrics 等，并说明留给 A5 的接口。 |
| [reviewer_risk_register.md](./reviewer_risk_register.md) | 登记 PR-S0-v2 阶段可预见的 C/I/M 审稿风险、触发条件、影响和缓解入口。 |

## 边界

- PR-S0-v2 不跑四个真实例子；真实场景设计和 pilot 主题留给 A3。
- PR-S0-v2 不冻结指标公式、阈值或统计协议；这些留给 A5。
- PR-S0-v2 不启动真实 LLM。后续若真实调用，必须先 `source .env` 并保留 run record。

## S0-v2 特别注意

评价设计必须区分 target-domain research findings 与 method-evaluation findings：前者只能由目标论文 content evidence、统计观察、反向证据和研究者裁决支撑；后者才使用 process evidence、pilot 制品和 human-LLM interaction logs。
