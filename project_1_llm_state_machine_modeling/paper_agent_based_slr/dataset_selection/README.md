# dataset_selection/：场景与证据资产选择入口

## 1. 定位

本目录复刻旧 Path-1 工作区中的 `dataset_selection/` 层级，但在第二篇智能体辅助 SLR 论文中，它不表示已经冻结实验数据集。PR-S0 阶段只登记后续 A3 可能使用的场景 / 证据资产类型，避免把 `sources/`、PR #97 或历史评论直接升级成正式 基准。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [sample_assets.md](./sample_assets.md) | PR-S0 阶段的候选场景和证据资产总账，区分 `main` 事实、PR #97 快照、历史评论和计划证据。 |
| [a1_seed_papers.md](./a1_seed_papers.md) | PR-A1 的 5 篇 LLM4STM / LLM4Modeling 最小闭环种子、备选 / 排除候选、覆盖矩阵与 A2/A3/A5a 交接。 |

## 3. 使用规则

1. 引用 PR #97 前必须先读 [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。
2. PR-S0 不冻结场景数量；“四个真实例子”不是 PR #101 对 PR-S0 的硬要求。
3. 后续 A3 若选择真实场景，必须补齐数据来源、纳排理由、金事实 / 银事实构造方式、人工审计计划和版权 / 全文可发布性。
