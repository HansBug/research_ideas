# dataset_selection/：场景与证据资产选择入口

## 1. 定位

本目录复刻旧 Path-1 工作区中的 `dataset_selection/` 层级，但在第二篇 agent-based SLR 论文中，它不表示已经冻结实验数据集。A0 阶段只登记后续 A3 可能使用的 scenario / evidence asset 类型，避免把 `sources/`、PR #97 或历史 comment 直接升级成正式 benchmark。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [sample_assets.md](./sample_assets.md) | A0 阶段的候选场景和证据资产总账，区分 `main` fact、PR #97 snapshot、historical comment 和 planned evidence。 |

## 3. 使用规则

1. 引用 PR #97 前必须先读 [../evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。
2. A0 不冻结场景数量；“四个真实例子”不是 PR #101 对 A0 的硬要求。
3. 后续 A3 若选择真实场景，必须补齐数据来源、纳排理由、gold / silver fact 构造方式、人工审计计划和版权 / fulltext 可发布性。
