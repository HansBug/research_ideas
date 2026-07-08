# reports 研究报告文库

## 1. 文库定位

本目录保存 `paper_stm_repair/` 下仍处于 active 主路径的人类可读研究报告：主要是 R5/R5.5 seed readiness、conversion readiness、negative evidence、scope handoff、主 seed profile 的历史快照，以及战略转向后形成的 source-level issue lifecycle 合同报告。机器事实源仍以 [../pipeline/](../pipeline/) 和 [../corpora/](../corpora/) 下 JSON / JSONL / registry / archive 为准。

R5.7 / Better STM / constructed `STM_k` / blind adjudication 报告链已经迁入 cold archive：[../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/)。它们不再作为本目录 active report 表的一部分。

## 2. Active report 列表

| 时间 | report | 类型 | 当前使用方式 |
|---|---|---|---|
| 2026-07-08 10:15:00 | [2026-07-08-10-15-00-pr-issue-ledger-contract.md](./2026-07-08-10-15-00-pr-issue-ledger-contract.md) | issue ledger contract | source issue ledger v0 合同报告；定义 candidate / confirmed / rejected / out-of-scope / insufficient-evidence gate，不是实验结果。 |
| 2026-06-29 19:55:45 | [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | PlantUML blocked recovery | `llms-emp` 三个原 blocked 已恢复为 partial；conversion recovery 不计 repair gain。 |
| 2026-06-29 00:03:56 | [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | main seed profile | 10 NL cluster × 6 LLM 输出的历史画像；当前状态数字以 R5.5.2 recovery report 为准。 |
| 2026-06-28 23:18:32 | [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | negative evidence | 旧 blocked 的历史负证据；当前 `llms-emp` blocked 状态已被 R5.5.2 覆盖。 |
| 2026-06-28 22:54:39 | [2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md) | scope handoff | T0/T0.5/T1 历史 scope handoff；当前 active scope 以 story/model_scope.md 为准。 |
| 2026-06-28 19:42:58 | [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) | directional analysis | 解释为什么 `llms-emp-stm-subset` 成为优先主 seed 池。 |
| 2026-06-28 04:03:18 | [2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) | seed readiness | R5 seed readiness 历史快照；`llms-emp` 当前状态以 R5.5.2 为准。 |
| 2026-06-28 03:42:24 | [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md) | selected smoke | 四例 pre-repair baseline smoke；不是修正失败或修正成功。 |

## 3. Archived R5.7 报告链

| archive 入口 | 内容 | 使用限制 |
|---|---|---|
| [../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/) | R5.7.1 evaluation logic、R5.7.2 Better STM / repair target contract、R5.7.3 objective metric framework、R5.7.4 static adjudication、R5.7.5 constructed / blind adjudication reports。 | historical / superseded / calibration-only；不得写成真实 repair-loop effectiveness、active evaluation endpoint 或 current baseline contract。 |

## 4. 推荐阅读顺序

1. 想理解当前 issue lifecycle 合同：先读 [2026-07-08-10-15-00-pr-issue-ledger-contract.md](./2026-07-08-10-15-00-pr-issue-ledger-contract.md)，再读 [../experiment_design/issue_lifecycle/README.md](../experiment_design/issue_lifecycle/README.md)。
2. 想理解当前 seed / conversion readiness：先读 [SUMMARY.md](./SUMMARY.md)，再读 R5.5.2 recovery report 和 main seed profile。
3. 想理解当前 paper1 story / contribution：不要从 archived R5.7 报告开始；应读 [../README.md](../README.md) 与 [../story/README.md](../story/README.md)。
4. 想追溯 R5.7 为什么被归档：读 [../archive/r5_7_better_stm_snapshot/README.md](../archive/r5_7_better_stm_snapshot/README.md) 与 [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md)。

## 5. 维护纪律

1. 本目录不记录 PR review 状态、CI 状态或 merge 进度；这些动态信息留在 GitHub PR body/comment。
2. 新增 report 必须是稳定研究结论、human-facing handoff 或证据链说明；高基数机器制品留在 pipeline / corpora / runs。
3. 若 report 被新事实覆盖，应在 [SUMMARY.md](./SUMMARY.md) 中标明 superseded / current-status-overridden，而不是删除历史报告。
4. archived R5.7 报告只能通过 archive 入口引用，不能恢复为 active report row。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 10:15:00 | `PR-issue-ledger` 新增 source issue ledger v0 合同报告，并更新 active report 表。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后将 R5.7 报告链移出 active reports 表，改为 cold archive pointer。 |
