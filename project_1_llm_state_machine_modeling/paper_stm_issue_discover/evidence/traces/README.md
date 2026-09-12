# traces/ — 分支资产追踪入口

> **硬边界**：本子路径只保存分支局部资产如何被消费、迁移、排除或降级的追踪记录。它不是 execution trace、repair trace 或 verification trace；不要把这里的 trace 与后续实验 run record 混淆。

## 1. 什么时候读这里

| 场景 | 是否建议读 | 理由 |
|---|---:|---|
| 想知道 PR #93/#94/#96 等分支局部资产后来如何处理 | 是 | [branch_asset_trace.md](./branch_asset_trace.md) 是分支资产追踪。 |
| 想解释某个旧资产为何没有进入当前 registry | 是 | trace 可作为 provenance。 |
| 想读取真实实验运行 trace / repair loop trace | 否 | 后续应放在 pipeline / run record / reports，不在本目录。 |
| 想写当前主实验统计 | 否 | trace 不是事实总账。 |

## 2. 本子路径文件清单

| 文件 | 内容 | 推荐阅读场景 | 禁止误用 |
|---|---|---|---|
| [branch_asset_trace.md](./branch_asset_trace.md) | PR #93/#94/#96 分支局部资产消费决策。 | 查某个旧分支资产是否已迁移、排除或只作线索。 | 不能当作当前 seed / baseline / result。 |

## 3. 与其他 evidence 子路径的关系

| 子路径 | 何时跳转 |
|---|---|
| [../ledgers/README.md](../ledgers/README.md) | 需要资产继承边界、可获取性和来源等级背景时。 |
| [../audits/README.md](../audits/README.md) | 需要知道被追踪资产最初如何被审计时。 |
| [../matrices/README.md](../matrices/README.md) | 需要看被追踪资产是否进入过候选矩阵时。 |

## 4. 当前事实源回跳

- 当前 seed library：[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)
- 当前 repair baselines：[../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md)
- 当前 NL datasets：[../../corpora/nl_datasets/SUMMARY.md](../../corpora/nl_datasets/SUMMARY.md)
- pipeline reports：[../../reports/SUMMARY.md](../../reports/SUMMARY.md)
