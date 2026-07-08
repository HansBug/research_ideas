# experiment_design/ — source-level issue lifecycle 实验设计入口

本目录现在只维护 paper1 后续实验协议的 **active scaffold**。2026-07-07 战略校准后，paper1 不再以 Better STM / which STM is better 作为 headline evaluation framework；R5.7 的 Better STM definition、repair target taxonomy、objective metric framework、constructed `STM_k` / blind adjudication prompt 与 dry-run 资产已经整体迁入 cold archive：[../archive/r5_7_better_stm_snapshot/](../archive/r5_7_better_stm_snapshot/)。

当前 active 实验问题是：给定 `NL + raw/source STM_0`，如何发现、确认、修复 source-level behavioral issues，并回到 raw/source 层审计 issue closure 与 regression。

## 1. 当前 active 职责

| 未来协议块 | 当前状态 | 后续 owner |
|---|---|---|
| candidate issue discovery | v0 ledger / schema 已定义；真实 discovery runner 未实现 | [issue_lifecycle/](./issue_lifecycle/), `PR-discover-confirm` |
| strict source-level confirmation | v0 两条 confirmed path 已定义；source trace 仍未定义 | [issue_lifecycle/source_level_issue_definition.md](./issue_lifecycle/source_level_issue_definition.md), `PR-source-trace` |
| confirmed issue ledger | v0 JSON schema / fixture / pytest gate 已定义；尚未接真实 case | [../pipeline/evaluation/schemas/source_issue_ledger.schema.json](../pipeline/evaluation/schemas/source_issue_ledger.schema.json) |
| issue-grounded repair / change ledger | 尚未定义 | `PR-repair-runner`, `PR-loop-io` |
| raw/source patch bundle or final raw/source `STM_k` | 尚未定义导出 / 投影协议 | `PR-source-trace`, `PR-raw-export` |
| closure / regression audit | 尚未定义 | `PR-closure-audit`, later `PR-eval-rubric` |
| final metrics / baseline / judge prompt | pilot 前不得冻结 | `PR-loop-pilot` 之后再进入 `PR-eval-rubric` / `PR-baseline-contract` |

## 2. 当前保留文件

| 路径 | 当前作用 | 禁止误读 |
|---|---|---|
| [SUMMARY.md](./SUMMARY.md) | active 实验设计轻量总账。 | 不复制历史 R5.7 评价表，不替代 future ledger/schema。 |
| [GUIDE.md](./GUIDE.md) | 后续协议设计纪律。 | 不把 archived Better STM gate 迁回 active guardrail。 |
| [metrics/README.md](./metrics/README.md) | future metrics placeholder。 | pilot 前不冻结 final metric / baseline / judge prompt。 |
| [issue_lifecycle/README.md](./issue_lifecycle/README.md) | source issue ledger v0 合同入口。 | 只定义 issue status / evidence gate，不运行 repair、不生成实验结果。 |

## 3. 历史 R5.7 快照

R5.7 资产已经从本目录移出。若需要追溯旧讨论，请只从 archive 入口进入：

- [../archive/r5_7_better_stm_snapshot/README.md](../archive/r5_7_better_stm_snapshot/README.md)
- [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md)
- [../archive/r5_7_better_stm_snapshot/experiment_design/](../archive/r5_7_better_stm_snapshot/experiment_design/)

这些材料只能作为 historical / superseded / calibration-only 资产；不得作为 active method result、正式 evaluation endpoint 或 paper1 contribution evidence。

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 10:15:00 | `PR-issue-ledger` 后新增 [issue_lifecycle/](./issue_lifecycle/) 合同入口，并将前三个协议块从“未定义”更新为 v0 contract 已定义 / runner 未实现。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重写为 source-level issue lifecycle scaffold；R5.7 Better STM 资产改由 cold archive 入口追溯。 |
