# reports/ — 阶段性研究报告（按日期命名）

> **现行评测边界（2026-08-24）**：method 只负责发现、D/W、release 和 W2 audit；L 只来自
> 台账；正式 validity/relation/hit/FP/precision 只由独立冻结
> `semantic-judge.two-stage.v3.2` 按 issue #195 产生。下表中早期报告若引用 runner 内置
> Judge、旧 Luna/Sol Judge 或其费用/分数，只能按该报告的历史协议阅读，不与 v3.2 正式结果混用。

> 本目录共 **16** 份 active human-facing report，跨 2026-06 至 2026-08：
>
> | 份数 | 时间 | 是什么 |
> | --: | :-- | :-- |
> | 7 | 2026-06 | 语料准入、转换恢复、负证据、directional analysis、scope handoff、主 seed profile、selected smoke |
> | 2 | 2026-07-08 | issue ledger / source trace 两份 v0 字段合同说明 |
> | 1 | 2026-07-19 | Issue #161 PlantUML Java frontend 技术路线报告——当前 60 例语料的由来 |
> | 1 | 2026-08-11 | 重构后 e2e smoke。⛔ **工程验证，不是研究性运行，数字不得进论文统计** |
> | 5 | 2026-08-19 至 2026-08-25 | v26/v27 历史实验、v51 method-only 最终 54x3、Judge sensitivity、provider 健康探针 |
>
> | 你想找 | 去哪 |
> | :-- | :-- |
> | **当前 v51 method-only 54x3 + 冻结 v3.2 Judge 正式结果** | [2026-08-25-evidence-discovery-v51-final-54x3.md](./2026-08-25-evidence-discovery-v51-final-54x3.md) |
> | v27-stream 旧 Judge 历史结果 | [2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md](./2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md) |
> | v26 全量 x3 历史结果 | [2026-08-19-luna-full-x3-v26.md](./2026-08-19-luna-full-x3-v26.md) |
> | Luna/Sol judge 对照与开发/正式分层 | [2026-08-19-judge-model-comparison.md](./2026-08-19-judge-model-comparison.md) |
> | Luna/Terra 当前 provider 健康证据 | [2026-08-19-luna-terra-provider-health.md](./2026-08-19-luna-terra-provider-health.md) |
> | v46 全量矩阵双侧结论（历史） | [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) |
> | 逐格 / 逐轮结果、代次对比 | [../discover_matrix/](../discover_matrix/) |
> | Issue #161 Java frontend 技术报告 | [2026-07-19-issue-161-plantuml-java-frontend.md](./2026-07-19-issue-161-plantuml-java-frontend.md) |
>
> 本目录只保存稳定的 human-facing 研究报告。逐格机器制品、运行记录和 usage 回到 [../pipeline/](../pipeline/) 或 `runs/`，判据与事前登记回到 [../discover_matrix/](../discover_matrix/)；GitHub PR/issue 继续只负责动态施工状态。
>
> ⚠️ 本目录**机器事实源为零**；统计一律回到 [../pipeline/](../pipeline/)、[../corpora/](../corpora/) 与根目录 `runs/` 下的 JSON / JSONL / registry / immutable receipts。

## 1. 文库定位

本目录保存 `paper_stm_issue_discover/` 下仍处于 active 主路径的人类可读研究报告：主要是 R5/R5.5 seed readiness、conversion readiness、negative evidence、scope handoff、主 seed profile 的历史快照，以及战略转向后形成的 source-level issue lifecycle 合同报告。机器事实源仍以 [../pipeline/](../pipeline/) 和 [../corpora/](../corpora/) 下 JSON / JSONL / registry / archive 为准。

R5.7 / Better STM / constructed `STM_k` / blind adjudication 报告链已经迁入 cold archive：[../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/)。它们不再作为本目录 active report 表的一部分。

## 2. Active report 列表

| 时间 | report | 类型 | 当前使用方式 |
|---|---|---|---|
| 2026-08-25 | [2026-08-25-evidence-discovery-v51-final-54x3.md](./2026-08-25-evidence-discovery-v51-final-54x3.md) | 当前 method-only 54x3 正式实验 | 162/162 method 与外置 v3.2 Judge 闭包；给出 X1v2 公平对照、v27 六 pair 局部参照、D/W、W2 审计、corrected cost、retry 和逐 pair 结果。 |
| 2026-08-19 | [2026-08-19-luna-terra-provider-health.md](./2026-08-19-luna-terra-provider-health.md) | provider 健康探针 | 四个时间窗的结构化请求证据；用于运行前健康判断、relay failure 分类和 retry 上限依据，不用于模型能力比较。 |
| 2026-08-19 | [2026-08-19-judge-model-comparison.md](./2026-08-19-judge-model-comparison.md) | judge sensitivity 与分层协议 | Luna 用于开发期筛选，Sol 用于冻结候选正式评测；保存相关性、分歧和成本证据。 |
| 2026-08-19 | [2026-08-19-luna-full-x3-v26.md](./2026-08-19-luna-full-x3-v26.md) | 历史全量 x3 实验 | 旧 release-only 54-pair 双臂结果；Judge 与成本口径均不得和 v3.2 正式结果混用。 |
| 2026-08-20 | [2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md](./2026-08-20-luna-full-x3-v27-stream/REPORT-luna.md) | 历史全量 x3 实验 | v27-stream 旧 Judge 快照；冻结 v3.2 下只有六 pair x3 局部参照，正式当前结果读 2026-08-25 报告。 |
| 2026-08-11 | [2026-08-11-post-refactor-e2e-smoke.md](./2026-08-11-post-refactor-e2e-smoke.md) | 重构后 e2e smoke | 大规模目录重构后的端到端验证：`0000` × claude / gpt 各 1 轮，两格均 completed / coverage=full / 零降级零重试，输入哈希与搬迁前逐字节相同，发现的 4 条与 v46 逐条对应。⛔ **工程验证，数字不得进论文统计**。 |
| 2026-07-19 | [2026-07-19-issue-161-plantuml-java-frontend.md](./2026-07-19-issue-161-plantuml-java-frontend.md) | PlantUML Java frontend | **本表中与当前语料关系最直接的一份**：Issue #161 把 PlantUML canonical 从 SCXML 路线换成 Java source frontend，60 例 active 语料由此产生。技术路线报告，不是实验结果。 |
| 2026-07-08 14:03:59 | [2026-07-08-14-03-59-pr-source-trace-contract.md](./2026-07-08-14-03-59-pr-source-trace-contract.md) | source trace contract | source trace v0 合同报告；定义 raw/source ↔ intermediate trace、projection status 与 negative attribution gate，不是实验结果。 |
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

1. 想理解当前 issue lifecycle 合同：先读 [2026-07-08-10-15-00-pr-issue-ledger-contract.md](./2026-07-08-10-15-00-pr-issue-ledger-contract.md)，再读 [../experiment_design/issue_lifecycle/README.md](../archive/r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/README.md)。
2. 想理解当前 source trace 合同：先读 [2026-07-08-14-03-59-pr-source-trace-contract.md](./2026-07-08-14-03-59-pr-source-trace-contract.md)，再读 [../experiment_design/source_trace/README.md](../archive/r7_issue_lifecycle_scaffold/experiment_design/source_trace/README.md)。
3. 想理解当前 seed / conversion readiness：先读 [SUMMARY.md](./SUMMARY.md)，再读 R5.5.2 recovery report 和 main seed profile。
4. 想理解当前 paper1 story / contribution：不要从 archived R5.7 报告开始；应读 [../README.md](../README.md) 与 [../story/README.md](../archive/r8_story_pre_rebuild/story/README.md)。
5. 想追溯 R5.7 为什么被归档：读 [../archive/r5_7_better_stm_snapshot/README.md](../archive/r5_7_better_stm_snapshot/README.md) 与 [../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md](../archive/r5_7_better_stm_snapshot/PATH_MAPPING.md)。

## 5. 维护纪律

1. 本目录不记录 PR review 状态、CI 状态或 merge 进度；这些动态信息留在 GitHub PR body/comment。
2. 新增 report 必须是稳定研究结论、human-facing handoff 或证据链说明；高基数机器制品留在 pipeline / corpora / runs。
3. 若 report 被新事实覆盖，应在 [SUMMARY.md](./SUMMARY.md) 中标明 superseded / current-status-overridden，而不是删除历史报告。
4. archived R5.7 报告只能通过 archive 入口引用，不能恢复为 active report row。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-08-25 | 新增 v51 method-only 54x3 与冻结 v3.2 Judge 最终报告，active report 数由 15 更新为 16，并将 v26/v27 旧 Judge 数字明确降为历史协议。 |
| 2026-08-20 | 新增 v27-stream Luna 全量 x3 结果，更新当前入口、逐条台账、judge 证据和 active report 数。 |
| 2026-08-19 | 补录 v26 正式实验、judge 模型对照和 provider 健康探针，active report 数由 11 更新为 14，并修正“本目录无当前实验结果”的旧入口。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 新增 source trace v0 合同报告，并更新 active report 表。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 新增 source issue ledger v0 合同报告，并更新 active report 表。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后将 R5.7 报告链移出 active reports 表，改为 cold archive pointer。 |
