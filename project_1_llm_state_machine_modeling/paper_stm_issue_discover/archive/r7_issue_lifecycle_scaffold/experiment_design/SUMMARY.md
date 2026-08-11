# experiment_design/SUMMARY.md — source-level issue lifecycle 实验设计总账

## 1. 当前一句话状态

本目录已清理为后续 **source-level behavioral issue discovery / repair / closure** 的 active scaffold。旧 R5.7 / Better STM-facing 实验设计、constructed `STM_k` dry-run、blind adjudication、objective metric framework 与 repair target taxonomy 已整体迁入 [../archive/r5_7_better_stm_snapshot/](../../r5_7_better_stm_snapshot/)。

## 2. 当前尚未冻结的核心合同

| 合同 | 当前状态 | 为什么不能现在冻结 |
|---|---|---|
| candidate issue ledger | v0 已定义 | 字段、证据和 confirmation status 见 [issue_lifecycle/issue_ledger_contract.md](./issue_lifecycle/issue_ledger_contract.md) 与 schema。 |
| confirmed issue ledger | v0 已定义 | 只允许 `nl_grounded_behavioral_issue` 与 `raw_internal_inconsistency` 两条 confirmed path；folded event 默认仍 candidate。 |
| source trace / canonical export | source trace v0 已定义；post-Confirm semantic-root export bundle 与 canonical exporter 未实现 | [source_trace/](./source_trace/) 已定义 legacy raw/source ↔ intermediate trace、projection status 与 attribution gate；当前 PlantUML working bundle 只授权 input attribution，未来独立 export PR 负责 fresh canonical source output。 |
| stage runtime / run record | Issue #152 已定义稳定语义，尚未实现 | 必须由完整 Discover/Repair/Confirm 阶段纵向落地 input/output、失败态、append-only records、context 与 redaction，不能再拆空 IO PR。 |
| closure / regression audit | 未定义 | 需要基于真实 Repair-Confirm issue chains、fresh canonical source output、semantic change/correspondence ledger 与隐藏审计资产设计，不能用 post-repair rediscovery 代替。 |
| final metrics / baseline / judge prompt | 未冻结 | 必须等 pilot 产出真实 fresh canonical raw/source repaired STM（暂称 `STM_final`，不是 archived constructed `STM_k`）与 export audit 后再冻结。 |

## 3. R5.7 archive 状态

| 历史资产 | archive 入口 | 当前角色 |
|---|---|---|
| R5.7 evaluation logic / quality model / eligibility / protocols / dry-run | [../archive/r5_7_better_stm_snapshot/experiment_design/](../../r5_7_better_stm_snapshot/experiment_design/) | historical / calibration only |
| R4/R5.7 evaluation gate / schemas / dry-run examples / blind judge outputs | [../archive/r5_7_better_stm_snapshot/pipeline/evaluation/](../../r5_7_better_stm_snapshot/pipeline/evaluation/) | historical / calibration only |
| R5.7.1--R5.7.5 reports | [../archive/r5_7_better_stm_snapshot/reports/](../../r5_7_better_stm_snapshot/reports/) | historical report chain |

## 4. 下一步阅读路径

1. 当前 story 与贡献口径：先读 [../README.md](../../../README.md) 和 [../story/README.md](../../r8_story_pre_rebuild/story/README.md)。
2. 资产归档依据：读 [../evidence/ledgers/paper1_strategy_asset_map.md](../evidence_ledgers/paper1_strategy_asset_map.md) 与 [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../../r5_7_better_stm_snapshot/PATH_MAPPING.md)。
3. 后续实验设计：先读 [Issue #152](https://github.com/HansBug/research_ideas/issues/152)、[issue_lifecycle/README.md](./issue_lifecycle/README.md) 与 [source_trace/README.md](./source_trace/README.md)，再到 [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) 查询动态施工顺序；不要从 archive 直接恢复旧 Better STM gate。

## 5. 禁止误读

- 不把 Better STM / which STM is better 作为 active headline。
- 不把 constructed `STM_k` 或 blind adjudication 写成真实 repair-loop evidence。
- 不把 archived objective metrics 或 repair target taxonomy 直接迁成 active metric / rubric。
- 不把 conversion / representation / `.fcstm` lowering 改善计为 repair gain。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 对齐一次 Discover + 多轮 Repair-Confirm 合同；runtime 由完整阶段 Agent 纵向落地，C closure/regression 不再依赖 post-repair rediscovery。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 后把 source trace / patch projection 行更新为 trace v0 已定义 / patch export 未实现，并链接 source_trace docs / schema / fixture / tests。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 后把 candidate / confirmed issue ledger 标为 v0 已定义，并链接 issue lifecycle docs / schema / fixture / tests。 |
| 2026-07-08 00:20:00 | `PR-better-archive` review 后将 pilot 后产物记号从易混淆的 active `STM_k` 改为 `STM_final`，避免与 archived constructed `STM_k` 混淆。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重写总账：R5.7 资产 cold archived，active 实验设计回到 source-level issue lifecycle。 |
