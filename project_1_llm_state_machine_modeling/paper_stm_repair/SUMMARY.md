# paper_stm_repair/SUMMARY.md — 顶层轻量总账

本文件是 `paper_stm_repair/` 的轻量总账入口，用于从 `README.md -> SUMMARY.md -> STATUS.md -> GUIDE.md` 快速理解当前积累和下一步。机器事实、运行结果和完整制品仍以具体 JSON / registry / report / ledger 为准；本文件不做第二事实源。

## 1. 当前一句话状态

paper1 当前已经完成战略转向后的资产清账，并将 active 主线重置为 **source-level behavioral issue discovery and closure**：给定 `NL + raw/source STM_0`，通过中间语义执行表示和工具 / agent 反馈发现、确认、修复 source-level behavioral issues，并回到 raw/source 层做 closure / regression audit。

真实 repair loop、pilot、final evaluation rubric、baseline contract 和正式实验协议均尚未完成。

## 2. 当前事实源

| 类型 | 入口 | 作用 |
|---|---|---|
| 战略讨论 | [../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | 当前最高优先级导师路线：paper1 淡化 fcstm，主打 loop + simulation / verification feedback + issue closure。 |
| 资产地图 | [evidence/ledgers/paper1_strategy_asset_map.md](./evidence/ledgers/paper1_strategy_asset_map.md) | 标定哪些资产 active / update / archive / historical。 |
| 扫描审计 | [evidence/audits/2026-07-07-post-strategy-asset-scan.md](./evidence/audits/2026-07-07-post-strategy-asset-scan.md) | 记录 Better STM / `STM_k` / contribution drift 等风险命中分布。 |
| 当前状态 | [STATUS.md](./STATUS.md) | 记录已完成、未完成和下一步依赖。 |
| 后续纪律 | [GUIDE.md](./GUIDE.md) | 约束后续 agent 如何读资产、写 story、避免 claim 漂移。 |
| story 入口 | [story/README.md](./story/README.md) | 进入 paper story / task boundary / terminology / claim-evidence。 |

## 3. 资产状态概览

| 类别 | 当前处理 | 后续入口 |
|---|---|---|
| Root docs 和 story | 已转向 source-level issue lifecycle 口径；仍需后续 review 持续防止旧 wording 回流。 | [README.md](./README.md), [story/](./story/) |
| R5.7 / Better STM-facing 资产 | 只作 historical / superseded / archive-pending；不得作为 active evaluation framework。 | 后续 `PR-better-archive` |
| conversion / representation / pyfcstm 相关基础设施 | 可继续作为中间语义执行表示和工具反馈 infrastructure。 | 后续 `PR-source-trace`, `PR-loop-io`, `PR-raw-export` |
| seed / corpus / baseline 候选 | 可作为未来 protocol 输入来源，但本阶段不冻结样本分母或 baseline contract。 | 后续 `PR-loop-pilot`, `PR-baseline-contract`, `PR-exp-protocol` |
| reports / paper_v1 / discussions | 只作历史动机、negative evidence 或旧路线 provenance。 | 后续 archive / story 引用时必须降级 |

## 4. 下一步依赖

1. `PR-better-archive`：把 R5.7 / Better STM-facing 资产整体迁入 archive snapshot。
2. `PR-issue-ledger`：定义最小 candidate / confirmed issue ledger。
3. `PR-source-trace`：定义 raw/source element 与中间表示、patch/projection 的追踪关系。
4. `PR-loop-io`：冻结最小 stage IO、artifact naming、run record 和失败状态。
5. `PR-discover-confirm` 之后才进入真实 issue discovery / confirmation 实现。
6. `PR-loop-pilot` 产出真实 raw/source `STM_k` 或 source-level patch bundle 后，才能冻结 `PR-eval-rubric` 与 `PR-baseline-contract`。

## 5. 禁止误读

- 不再把 Better STM / which STM is better 作为 paper1 active headline question。
- 不把 constructed `STM_k` dry-run 或 blind adjudication 写成真实 repair-loop result。
- 不把 `fcstm` / `pyfcstm` 写成 paper1 contribution。
- 不把 conversion / normalization / lowering 算成 method gain。
- 不在 pilot 前冻结 final metrics、baseline contract 或 judge prompt。
- 不把 folded event / ugly expression 自动升级为 confirmed source-level behavioral issue。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 21:20:00 | SUMMARY 改为 source-level issue discovery and closure 总账；R5.7 Better STM-facing 资产降级为 historical / archive-pending。 |
| 2026-07-07 20:44:08 | 资产清账完成，新增 asset map 与 scan audit 作为后续 story reset / archive / issue lifecycle PR 的事实入口。 |
