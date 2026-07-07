# experiment_design/SUMMARY.md — source-level issue lifecycle 实验设计总账

## 1. 当前一句话状态

本目录已清理为后续 **source-level behavioral issue discovery / repair / closure** 的 active scaffold。旧 R5.7 / Better STM-facing 实验设计、constructed `STM_k` dry-run、blind adjudication、objective metric framework 与 repair target taxonomy 已整体迁入 [../archive/r5_7_better_stm_snapshot/](../archive/r5_7_better_stm_snapshot/)。

## 2. 当前尚未冻结的核心合同

| 合同 | 当前状态 | 为什么不能现在冻结 |
|---|---|---|
| candidate issue ledger | 未定义 | 需要先明确 source-level behavioral issue 的字段、证据和 confirmation 规则。 |
| confirmed issue ledger | 未定义 | 不能把 expression debt / folded event 自动升级为 confirmed issue。 |
| source trace / patch projection | 未定义 | 必须先记录 raw/source element 与 intermediate representation 的映射，否则无法回到 source 层评价。 |
| loop IO / run record | 未冻结 | 真实 repair loop 尚未重跑；必须先冻结 stage input/output、失败态和 redaction。 |
| closure / regression audit | 未定义 | 需要基于真实 repair/change ledger 与 post-repair rediscovery 设计。 |
| final metrics / baseline / judge prompt | 未冻结 | 必须等 pilot 产出真实 raw/source patch bundle 或 final raw/source `STM_k` 后再冻结。 |

## 3. R5.7 archive 状态

| 历史资产 | archive 入口 | 当前角色 |
|---|---|---|
| R5.7 evaluation logic / quality model / eligibility / protocols / dry-run | [../archive/r5_7_better_stm_snapshot/experiment_design/](../archive/r5_7_better_stm_snapshot/experiment_design/) | historical / calibration only |
| R4/R5.7 evaluation gate / schemas / dry-run examples / blind judge outputs | [../archive/r5_7_better_stm_snapshot/pipeline/evaluation/](../archive/r5_7_better_stm_snapshot/pipeline/evaluation/) | historical / calibration only |
| R5.7.1--R5.7.5 reports | [../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/) | historical report chain |

## 4. 下一步阅读路径

1. 当前 story 与贡献口径：先读 [../README.md](../README.md) 和 [../story/README.md](../story/README.md)。
2. 资产归档依据：读 [../evidence/ledgers/paper1_strategy_asset_map.md](../evidence/ledgers/paper1_strategy_asset_map.md) 与 [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md)。
3. 后续实验设计：从 `PR-issue-ledger` 开始，不从 archive 直接恢复旧 Better STM gate。

## 5. 禁止误读

- 不把 Better STM / which STM is better 作为 active headline。
- 不把 constructed `STM_k` 或 blind adjudication 写成真实 repair-loop evidence。
- 不把 archived objective metrics 或 repair target taxonomy 直接迁成 active metric / rubric。
- 不把 conversion / representation / `.fcstm` lowering 改善计为 repair gain。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 23:40:00 | `PR-better-archive` 后重写总账：R5.7 资产 cold archived，active 实验设计回到 source-level issue lifecycle。 |
