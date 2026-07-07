# ledgers/ — 历史事实账本入口

> **硬边界**：本子路径保存 R0/R1 阶段形成的历史事实账本，以及 2026-07-07 战略转向后的 paper1 资产清账地图。它不是当前 seed / baseline / NL dataset 的事实真源；当前事实必须回到 [../../corpora/](../../corpora/) 与对应 SUMMARY。

## 1. 什么时候读这里

| 场景 | 是否建议读 | 理由 |
|---|---:|---|
| 想理解 R1 当时如何判断上游事实等级、来源覆盖和 artifact 可获取性 | 是 | 这里保存历史 ledger。 |
| 想确认当前 `llms-emp-stm-subset` 是否进入主 seed 池 | 否 | 应读 [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md) 和 [../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。 |
| 想写论文 claim 或主实验数字 | 否 | ledger 只能作为 provenance；claim 必须回到当前 report / machine source。 |
| 想排查旧分支资产为什么被继承或排除 | 是 | 这里有 legacy asset inheritance。 |
| 想判断某个 Better STM / `STM_k` / adjudication / repair target 资产后续应保留、改写、归档还是只作历史证据 | 是 | [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) 是 PR-asset-map 的主资产地图。 |

## 2. 本子路径文件清单

| 文件 | 内容 | 推荐阅读场景 | 禁止误用 |
|---|---|---|---|
| [paper1_strategy_asset_map.md](./paper1_strategy_asset_map.md) | 2026-07-07 战略转向后的资产清账地图。 | 后续 `PR-story-reset`、`PR-better-archive`、`PR-issue-ledger`、`PR-source-trace`、`PR-loop-io` 施工前。 | 不能把 `archive` 资产继续当 active 方法协议；不能把 `active` conversion / representation 资产写成 method gain。 |
| [upstream_fact_ledger.md](./upstream_fact_ledger.md) | 上游 PR、导师讨论、旧分支、仓库事实等级。 | 解释某个事实为何被采信或降级。 | 不能替代当前 PR body / report / registry。 |
| [source_coverage_ledger.md](./source_coverage_ledger.md) | R1 检索来源覆盖、去重闭合和未深审边界。 | 解释 search coverage 与未覆盖风险。 | 不能直接推出当前 seed eligibility。 |
| [artifact_availability_ledger.md](./artifact_availability_ledger.md) | 代码、数据、结果、artifact 可获取性历史台账。 | 追溯某论文资源当时是否可得。 | 不能当作当前可下载状态，正式实验前必须重新核验。 |
| [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) | `paper_v1/`、旧 baseline、旧 source 继承边界。 | 判断旧资产能否作为 provenance 或线索。 | 不能把旧二手 parquet / derived asset 当一手资源。 |

## 3. 与其他 evidence 子路径的关系

| 子路径 | 何时跳转 |
|---|---|
| [../audits/README.md](../audits/README.md) | 需要读某轮审计执行方案或审计结论时。 |
| [../matrices/README.md](../matrices/README.md) | 需要看候选集、格式转换压力等二维对照时。 |
| [../traces/README.md](../traces/README.md) | 需要追踪某个分支局部资产如何被消费 / 排除时。 |

## 4. 当前事实源回跳

- 当前 seed library：[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)
- 当前 repair baseline：[../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md)
- 当前纯 NL 数据源：[../../corpora/nl_datasets/SUMMARY.md](../../corpora/nl_datasets/SUMMARY.md)
- R5.5 主画像：[../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)
