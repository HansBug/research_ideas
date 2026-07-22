# paper_stm_repair/SUMMARY.md — 顶层轻量总账

本文件是 `paper_stm_repair/` 的轻量总账入口，用于从 `README.md -> SUMMARY.md -> STATUS.md -> GUIDE.md` 快速理解当前积累和下一步。机器事实、运行结果和完整制品仍以具体 JSON / registry / report / ledger 为准；本文件不做第二事实源。

## 1. 当前一句话状态

paper1 当前已经完成战略转向后的资产清账，并将 active 主线重置为 **source-level behavioral issue discovery and closure**：给定 `NL + raw/source STM_0`，通过中间语义执行表示执行一次 Discover，再以多轮 Repair-Confirm 处理全部 issue chains，最后回到 raw/source 层做 closure / regression audit。

当前 contribution 口径已进一步收敛为：**feedback-driven LLM refinement loop + diagnostics / simulation / formal-verification feedback integration + source-level repair/evaluation setup**。ledger、audit、trace、run record 和 attribution boundary 只是方法 / 评价 / 可复现纪律，不能作为 headline contribution。

最小 source issue ledger v0 与 source trace v0 已定义；真实 repair loop、pilot、final evaluation rubric、baseline contract 和正式实验协议均尚未完成。

## 2. 当前事实源

| 类型 | 入口 | 作用 |
|---|---|---|
| 战略讨论 | [../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | 当前最高优先级导师路线：paper1 淡化 fcstm，主打 loop + simulation / verification feedback + issue closure。 |
| 资产地图 | [evidence/ledgers/paper1_strategy_asset_map.md](./evidence/ledgers/paper1_strategy_asset_map.md) | 标定哪些资产 active / update / archive / historical。 |
| 扫描审计 | [evidence/audits/2026-07-07-post-strategy-asset-scan.md](./evidence/audits/2026-07-07-post-strategy-asset-scan.md) | 记录 Better STM / `STM_k` / contribution drift 等风险命中分布。 |
| 当前状态 | [STATUS.md](./STATUS.md) | 记录已完成、未完成和下一步依赖。 |
| 后续纪律 | [GUIDE.md](./GUIDE.md) | 约束后续 agent 如何读资产、写 story、避免 claim 漂移。 |
| story 入口 | [story/README.md](./story/README.md) | 进入 paper story / task boundary / terminology / claim-evidence。 |
| issue lifecycle | [experiment_design/issue_lifecycle/README.md](./experiment_design/issue_lifecycle/README.md) | 当前 v0 candidate / confirmed / rejected / out-of-scope / insufficient evidence 合同。 |
| source trace | [experiment_design/source_trace/README.md](./experiment_design/source_trace/README.md) | raw/source ↔ intermediate trace、projection status 与 negative attribution gate 合同。 |
| machine contract | [pipeline/evaluation/schemas/source_issue_ledger.schema.json](./pipeline/evaluation/schemas/source_issue_ledger.schema.json), [pipeline/evaluation/tests/test_source_issue_ledger_schema.py](./pipeline/evaluation/tests/test_source_issue_ledger_schema.py) | issue ledger schema、fixture 与 pytest gate。 |
| trace machine contract | [pipeline/evaluation/schemas/source_trace.schema.json](./pipeline/evaluation/schemas/source_trace.schema.json), [pipeline/evaluation/tests/test_source_trace_schema.py](./pipeline/evaluation/tests/test_source_trace_schema.py) | source trace schema、fixture 与 pytest gate。 |

## 3. 资产状态概览

| 类别 | 当前处理 | 后续入口 |
|---|---|---|
| Root docs 和 story | 已转向 source-level issue lifecycle 口径；仍需后续 review 持续防止旧 wording 回流。 | [README.md](./README.md), [story/](./story/) |
| R5.7 / Better STM-facing 资产 | 已迁入 [archive/r5_7_better_stm_snapshot/](./archive/r5_7_better_stm_snapshot/)；只作 historical / superseded / calibration-only。 | archive snapshot |
| conversion / representation / pyfcstm 相关基础设施 | 可继续作为中间语义执行表示和工具反馈 infrastructure；当前 pyfcstm gitlink 已在伞分支直接更新，paper1 adapter 仍待阶段实现。 | [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100) 当前路线 |
| seed / corpus / baseline 候选 | 可作为未来 protocol 输入来源，但本阶段不冻结样本分母或 baseline contract。 | pilot 后实验设计阶段；动态顺序见 [#100](https://github.com/HansBug/research_ideas/pull/100) |
| reports / paper_v1 / discussions | 只作历史动机、negative evidence 或旧路线 provenance。 | 后续 archive / story 引用时必须降级 |
| issue ledger v0 | 已定义最小 schema / fixture / pytest gate；只覆盖合同分支，不是实验结果。 | [experiment_design/issue_lifecycle/](./experiment_design/issue_lifecycle/), [pipeline/evaluation/](./pipeline/evaluation/) |
| source trace v0 | 已定义最小 schema / fixture / pytest gate；覆盖 raw/source ↔ intermediate trace、projection status 与 negative attribution gate，不是实验结果。 | [experiment_design/source_trace/](./experiment_design/source_trace/), [pipeline/evaluation/](./pipeline/evaluation/) |

## 4. 下一步依赖

1. 已完成的 issue ledger v0 与 source trace v0 是 runtime v1 的迁移输入，后续实现不得绕过其 attribution / negative gate，但也不得把 v0 直接冒充真实 loop 输出。
2. 先交付完整 Discover Agent，同时落下最小 shared kernel、schema-safe pyfcstm adapter、records/context/renderer、工具、prompt、runner、CLI 与 stage smoke。
3. 再依次交付完整 Repair Agent 与 Confirm Agent；Repair 处理当前全部 pending nodes，Confirm 审查全部 dispositions，reject 只追加 successor 并回 Repair。
4. 三个阶段完成后，由无顶层 Agent/prompt、只按 typed stage result 转移的确定性 controller 组织闭环，再由独立 post-Confirm semantic-root export bundle 一次性生成 fresh canonical raw/source `STM_k` 并执行 closure audit。
5. 动态 subPR slug、状态和前置依赖只维护在 [伞 PR #100](https://github.com/HansBug/research_ideas/pull/100)；pilot 产出真实 canonical raw/source `STM_k`、semantic change/correspondence ledger 与 closure audit 后，才能冻结 final rubric 与 baseline contract。

## 5. 禁止误读

- 不再把 Better STM / which STM is better 作为 paper1 active headline question。
- 不把 constructed `STM_k` dry-run 或 blind adjudication 写成真实 repair-loop result。
- 不把 `fcstm` / `pyfcstm` 写成 paper1 contribution。
- 不把 ledger / audit / evidence bookkeeping 写成 paper1 contribution。
- 不把 conversion / normalization / lowering 算成 method gain。
- 不在 pilot 前冻结 final metrics、baseline contract 或 judge prompt。
- 不把 folded event / ugly expression 自动升级为 confirmed source-level behavioral issue。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-17 00:32:36 | 对齐 Issue #152 与伞 PR #100：删除旧 active subPR 路由，固定一次 Discover、多轮 Repair-Confirm、确定性顶层 controller 与 pilot 后冻结评价/baseline 的稳定能力顺序。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 后同步总账：最小 source trace v0 已落到 source_trace 文档、schema、六个 fixture 与 pytest gate；真实 loop / patch export / closure audit 仍未运行。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 后同步总账：最小 issue ledger v0 已落到 issue lifecycle 文档、schema、六个 fixture 与 pytest gate；真实 loop / pilot 仍未运行。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后同步总账：R5.7 / Better STM-facing 资产已迁入 cold archive，下一步依赖从 `PR-issue-ledger` 开始。 |
| 2026-07-07 22:10:00 | SUMMARY 补充 contribution 口径修正：主贡献是 loop + executable feedback integration；ledger / audit 只作评价和证据链纪律。 |
| 2026-07-07 21:20:00 | SUMMARY 改为 source-level issue discovery and closure 总账；R5.7 Better STM-facing 资产降级为 historical，并在 `PR-better-archive` 后迁入 cold archive。 |
| 2026-07-07 20:44:08 | 资产清账完成，新增 asset map 与 scan audit 作为后续 story reset / archive / issue lifecycle PR 的事实入口。 |
