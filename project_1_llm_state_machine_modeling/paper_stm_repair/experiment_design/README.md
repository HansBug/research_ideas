# experiment_design/ — source-level issue lifecycle 实验设计入口

本目录现在只维护 paper1 后续实验协议的 **active scaffold**。2026-07-07 战略校准后，paper1 不再以 Better STM / which STM is better 作为 headline evaluation framework；R5.7 的 Better STM definition、repair target taxonomy、objective metric framework、constructed `STM_k` / blind adjudication prompt 与 dry-run 资产已经整体迁入 cold archive：[../archive/r5_7_better_stm_snapshot/](../archive/r5_7_better_stm_snapshot/)。

当前 active 实验问题是：给定 `NL + raw/source STM_0`，一次 Discover 能发现哪些 source-level behavioral issues，多轮 Repair-Confirm 能否处理全部 issue chains，并最终在 raw/source 层审计 closure 与 regression。

## 1. 当前 active 职责

| 未来协议块 | 当前状态 | 稳定 owner / 入口 |
|---|---|---|
| Discover roots / checks | v0 ledger / schema 是迁移输入；真实 Discover Agent、runtime roots 与 immutable checks 未实现 | [issue_lifecycle/](./issue_lifecycle/), [Issue #152](https://github.com/HansBug/research_ideas/issues/152) |
| Repair dispositions / change ledger | 尚未实现；每轮必须覆盖全部 pending nodes，并对每项 `fix/reject` 给出理由 | [Issue #152](https://github.com/HansBug/research_ideas/issues/152) |
| Confirm decisions / successor chains | 尚未实现；每轮必须覆盖全部 dispositions，reject 只追加 successor 并回 Repair | [Issue #152](https://github.com/HansBug/research_ideas/issues/152) |
| deterministic B loop / B-final | 尚未实现；顶层不新增 Agent/prompt，只按 typed results 控制循环 | [Issue #152](https://github.com/HansBug/research_ideas/issues/152) |
| post-Confirm semantic-root export bundle + fresh canonical raw/source `STM_k` | source trace v0 已定义；独立 export bundle / canonical exporter 尚未实现，不采用 textual minimal patch | [source_trace/](./source_trace/), [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) |
| closure / regression audit | 尚未定义；只在 B-final 后进入一次性 C 阶段 | [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) |
| final metrics / baseline / judge prompt | pilot 前不得冻结 | pilot 后路线见 [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) |

## 2. 当前保留文件

| 路径 | 当前作用 | 禁止误读 |
|---|---|---|
| [SUMMARY.md](./SUMMARY.md) | active 实验设计轻量总账。 | 不复制历史 R5.7 评价表，不替代 future ledger/schema。 |
| [GUIDE.md](./GUIDE.md) | 后续协议设计纪律。 | 不把 archived Better STM gate 迁回 active guardrail。 |
| [metrics/README.md](./metrics/README.md) | future metrics placeholder。 | pilot 前不冻结 final metric / baseline / judge prompt。 |
| [issue_lifecycle/README.md](./issue_lifecycle/README.md) | source issue ledger v0 合同入口。 | 只定义 issue status / evidence gate，不运行 repair、不生成实验结果。 |
| [source_trace/README.md](./source_trace/README.md) | source trace v0 合同入口。 | 只定义 legacy trace / projection / attribution gate，不授权当前 working bundle 生成 canonical source output 或 closure 结果。 |

## 3. 历史 R5.7 快照

R5.7 资产已经从本目录移出。若需要追溯旧讨论，请只从 archive 入口进入：

- [../archive/r5_7_better_stm_snapshot/README.md](../archive/r5_7_better_stm_snapshot/README.md)
- [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md)
- [../archive/r5_7_better_stm_snapshot/experiment_design/](../archive/r5_7_better_stm_snapshot/experiment_design/)

这些材料只能作为 historical / superseded / calibration-only 资产；不得作为 active method result、正式 evaluation endpoint 或 paper1 contribution evidence。

## 4. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 对齐 Issue #152：active 协议块改为 Discover roots/checks、Repair dispositions、Confirm decisions/successors、deterministic B loop 与一次性 C audit。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 后新增 [source_trace/](./source_trace/) 合同入口，并将 source trace / projection 从未定义更新为 v0 trace contract 已定义 / raw export 未实现。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 后新增 [issue_lifecycle/](./issue_lifecycle/) 合同入口，并将前三个协议块从“未定义”更新为 v0 contract 已定义 / runner 未实现。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后重写为 source-level issue lifecycle scaffold；R5.7 Better STM 资产改由 cold archive 入口追溯。 |
