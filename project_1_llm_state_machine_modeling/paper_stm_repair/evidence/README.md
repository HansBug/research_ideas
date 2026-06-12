# evidence/ — 上游事实与旧资产边界

## 1. 职责

`evidence/` 只记录 R0 需要依赖的上游事实源、PR 状态、旧资产继承边界和使用限制。它不是 PR-R1 的逐篇 baseline 资产盘点，也不替代后续 experiment evidence。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [upstream_fact_ledger.md](./upstream_fact_ledger.md) | 记录 PR #100、#99、talks、#93/#94/#96、#73/#82/#92、sources/baselines 的事实等级与使用方式。 |
| [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) | 记录旧 `paper_v1/`、`path1_foundation/` 和 baseline 资产哪些可参考、哪些不可继承。 |

## 3. R0 边界

1. 只做事实等级和继承边界，不逐篇盘点论文 / 代码 / artifact。
2. 不把 PR #93/#94/#96 的分支局部文件写成 `main` 已有事实。
3. 不复制 `path1_foundation/`，不在其中新增、移动或修改文件。
4. 不决定具体 seed_id、转换格式或实验样本。
