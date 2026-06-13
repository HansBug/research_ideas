# evidence/ — 上游事实与旧资产边界

## 1. 职责

`evidence/` 记录 R0/R1 需要依赖的上游事实源、PR 状态、旧资产继承边界、baseline / seed 资产审计和使用限制。它可以承载 PR-R1 的候选级资产总账与 strict seed 调研协议，但不替代后续 PR-R2 seed registry、PR-R3 转换器 fixture 或 PR-R6 实验结果。

## 2. 文件说明

| 文件 | 作用 |
|---|---|
| [upstream_fact_ledger.md](./upstream_fact_ledger.md) | 记录 PR #100、#99、talks、#93/#94/#96、#73/#82/#92、sources/baselines 的事实等级与使用方式。 |
| [legacy_asset_inheritance.md](./legacy_asset_inheritance.md) | 记录旧 `paper_v1/`、`path1_foundation/` 和 baseline 资产哪些可参考、哪些不可继承。 |
| [baseline_asset_audit.md](./baseline_asset_audit.md) | PR-R1 对 baseline / seed / converter / comparison 资产的分层审计总账。 |
| [baseline_candidate_matrix.md](./baseline_candidate_matrix.md) | PR-R1 对九个五绿 direct baseline 与强近邻的 R2 / 主实验 / 对照资格矩阵。 |
| [artifact_availability_ledger.md](./artifact_availability_ledger.md) | PR-R1 对论文、代码、数据、结果和 artifact 可获取性的紧凑台账。 |
| [format_conversion_matrix.md](./format_conversion_matrix.md) | PR-R1 对 prior output formats 与 R3 转换压力的矩阵化记录。 |
| [branch_asset_trace.md](./branch_asset_trace.md) | PR-R1 对 #93/#94/#96 分支局部资产的状态、消费决策与使用限制。 |
| [source_coverage_ledger.md](./source_coverage_ledger.md) | PR-R1 对来源覆盖、去重闭合和未逐篇深审边界的记录。 |
| [strict_seed_literature_survey.md](./strict_seed_literature_survey.md) | PR-R1 对大规模 strict seed 文献调研的硬定义、排除码、多维指标、分级标准、初始事实台账和后续执行方案。 |

## 3. R0 / R1 边界

1. R0 只做事实等级和继承边界；R1 可以做候选级 baseline / seed / artifact 审计，但仍不冻结最终 seed。
2. strict seed 调研采用“广搜、严入、分层使用”口径：历史 direct baseline 不是封闭全集，`sources/` 也只是 source pool，不得把宽口径正例直接写成 strict paired seed。
3. 不把 PR #93/#94/#96 的分支局部文件写成 `main` 已有事实。
4. 不复制 `path1_foundation/`，不在其中新增、移动或修改文件。
5. 不决定具体 seed_id、转换格式或实验样本；这些由 PR-R2 / PR-R3 冻结。
6. R1 虽然新增 baseline 资产审计和 strict seed 调研协议，但仍不冻结四例 seed、不实现转换器、不运行真实 LLM、不跑主实验。
