# evidence/ — 事实源与旧资产继承边界

## 1. 职责

`evidence/` 记录 R0 使用的事实源等级、上游 PR 状态和旧 Path-1 资产继承边界。它不是 baseline 逐篇资产盘点；后者属于 PR-R1。

## 2. 文件职责

| 文件 | 职责 |
|---|---|
| [upstream_fact_ledger.md](./upstream_fact_ledger.md) | 记录 PR #100、PR #99、导师讨论、#73/#82/#92、#93/#94/#96 和 `sources/` 的事实等级与使用边界。 |
| [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) | 说明旧 `paper_v1/README.md`、Path-1/Path-2 guide 和 PR #93 分支 `path1_foundation/` 哪些结构可复用、哪些 story 不可继承。 |

## 3. 使用原则

1. 已合入 `main` 的文件可以作为仓库事实，但仍需按任务重新解释。
2. PR #93/#94/#96 是历史分支局部资产，不能写成 `main` 已有事实。
3. 旧 comment、Gist 和 PR body 只能作线索；进入实验或论文前必须转成可复验文件、链接或台账。
4. R0 只记录资产类别与继承边界；R1 才逐篇盘点论文、代码、demo、artifact、许可证、输出格式和转换可行性。
