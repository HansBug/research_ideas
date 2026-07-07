# evidence/SUMMARY.md — 历史审计总账

## 1. 当前结论

`evidence/` 已按 R5.5.1 路径重构为四类历史证据索引：[ledgers/README.md](./ledgers/README.md)、[audits/README.md](./audits/README.md)、[matrices/README.md](./matrices/README.md)、[traces/README.md](./traces/README.md)。本目录保留 R0/R1 证据链，但不再作为当前 corpus 事实真源。

2026-07-07 战略转向后，本目录新增 [ledgers/paper1_strategy_asset_map.md](./ledgers/paper1_strategy_asset_map.md) 与 [audits/2026-07-07-post-strategy-asset-scan.md](./audits/2026-07-07-post-strategy-asset-scan.md)，作为 `PR-story-reset`、`PR-better-archive`、`PR-issue-ledger`、`PR-source-trace` 和 `PR-loop-io` 的清账入口。它们只做资产地图与静态扫描审计，不移动文件、不重写 story、不报告方法效果。

当前事实源：seed 看 [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) 与 [../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)，repair baseline 看 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)，纯 NL 数据源看 [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md)，转换 / 表示 / readiness 看 [../pipeline/conversion/README.md](../pipeline/conversion/README.md)、[../pipeline/representation/README.md](../pipeline/representation/README.md)、[../pipeline/readiness_audit/README.md](../pipeline/readiness_audit/README.md)，人类结论看 [../reports/SUMMARY.md](../reports/SUMMARY.md)。

## 2. 子路径入口

| 子路径 README | 先读场景 |
|---|---|
| [ledgers/README.md](./ledgers/README.md) | 需要理解历史事实等级、来源覆盖、artifact 可获取性和旧资产继承时。 |
| [audits/README.md](./audits/README.md) | 需要理解 R1 审计设计、strict seed 调研口径和排除标准时。 |
| [matrices/README.md](./matrices/README.md) | 需要理解历史候选矩阵、baseline 横向比较和格式转换压力时。 |
| [traces/README.md](./traces/README.md) | 需要追踪分支局部资产如何迁移、消费、排除或降级时。 |

## 3. 文件总账

| 类别 | 文件 | 作用 | 当前性 |
|---|---|---|---|
| ledger | [ledgers/paper1_strategy_asset_map.md](./ledgers/paper1_strategy_asset_map.md) | 2026-07-07 战略转向后的资产清账地图，把 paper1 相关文件 / PR / issue / comment 分为 `active`、`update`、`archive`、`historical`，并指定 downstream PR。 | 当前清账入口 |
| ledger | [ledgers/upstream_fact_ledger.md](./ledgers/upstream_fact_ledger.md) | 上游 PR、导师讨论、旧分支和仓库事实等级。 | 历史审计 |
| ledger | [ledgers/source_coverage_ledger.md](./ledgers/source_coverage_ledger.md) | R1 来源覆盖、去重闭合和未深审边界。 | 历史审计 |
| ledger | [ledgers/artifact_availability_ledger.md](./ledgers/artifact_availability_ledger.md) | 代码、数据、结果、artifact 可获取性台账。 | 历史审计 |
| ledger | [ledgers/legacy_asset_inheritance.md](./ledgers/legacy_asset_inheritance.md) | `paper_v1/`、旧 baseline、旧 source 继承边界。 | 历史审计 |
| audit | [audits/2026-07-07-post-strategy-asset-scan.md](./audits/2026-07-07-post-strategy-asset-scan.md) | PR-asset-map 静态扫描审计报告，记录 Better STM / `STM_k` / adjudication / repair target / conversion gain 关键词命中、`paper_v1/` 命中与 `CLAUDE.md` / `AGENTS.md` 去重事实。 | 当前清账证据 |
| audit | [audits/baseline_asset_audit.md](./audits/baseline_asset_audit.md) | R1 baseline / seed / converter / comparison 资产审计总账。 | 历史审计 |
| audit | [audits/strict_seed_literature_survey.md](./audits/strict_seed_literature_survey.md) | strict seed 调研定义、排除码、分级标准和初始事实台账。 | 历史审计 |
| matrix | [matrices/baseline_candidate_matrix.md](./matrices/baseline_candidate_matrix.md) | 五绿 direct generation baseline 与近邻候选矩阵。 | 历史审计 |
| matrix | [matrices/format_conversion_matrix.md](./matrices/format_conversion_matrix.md) | prior output format 与 R3 转换压力矩阵。 | 历史审计 |
| trace | [traces/branch_asset_trace.md](./traces/branch_asset_trace.md) | PR #93/#94/#96 分支局部资产消费决策。 | 历史审计 |

## 4. 风险与使用限制

1. 旧矩阵中的候选、数量和可获取性判断只代表 R1 审计阶段，不等于当前 seed / baseline eligibility。
2. 活链接、GitHub artifact、Drive、4open、dynareport 等外部资源在正式实验前必须重新冻结 commit / hash / 日期。
3. 分支局部资产只能作为 provenance 或交叉核验线索，不能写成当前 `main` 已有事实。
4. `sources/` 的真实控制系统 NL 池不是 paired seed 总账；是否进入实验必须由 `corpora/seed_library` 和后续 eligibility 冻结。
5. 历史格式转换矩阵和 converter pressure 只能作为 R3/R4.5 设计线索；当前转换状态必须回到 `pipeline/` 机器事实源和 `reports/` 人读报告复核。

## 5. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-07-07 19:57:36 | 新增 PR-asset-map 资产清账地图与静态扫描审计入口，记录 R5.7 / Better STM-facing 资产后续归档、story reset、issue lifecycle、conversion attribution boundary 与 `paper_v1` historical 口径。 |
| 2026-06-29 11:46:00 | 同步 evidence 根三件套与子 README 的当前事实源回跳，补齐 conversion / representation / readiness / reports 入口。 |
| 2026-06-29 03:08:00 | 补齐 evidence 四个子路径 README，并在总账中增加子路径阅读入口。 |
| 2026-06-29 01:54:30 | 按 R5.5.1 路径重构将 evidence 重构为 `ledgers/`、`audits/`、`matrices/`、`traces/`，新增三件套并声明历史审计边界。 |
