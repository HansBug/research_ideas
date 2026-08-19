# reports/SUMMARY.md — 研究报告总账

## 1. 当前总览

| 项 | 数量 / 状态 |
|---|---|
| active human-facing reports | **14** |
| archived R5.7 Better STM reports | 6，见 [../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/) |
| 已部分 superseded / current-status-overridden reports | 5（R5.5.2 覆盖 R5 seed readiness、R5 directional analysis、main seed profile、scope handoff、negative evidence report 中的 blocked/current-status 部分） |
| 当前主入口 | 当前正式实验读 [2026-08-19-luna-full-x3-v26.md](./2026-08-19-luna-full-x3-v26.md)，judge 模型敏感性读 [2026-08-19-judge-model-comparison.md](./2026-08-19-judge-model-comparison.md)，运行前 provider 健康证据读 [2026-08-19-luna-terra-provider-health.md](./2026-08-19-luna-terra-provider-health.md)。 |
| 实验与代次边界 | 本目录保存当前自包含 human-facing 报告；逐格 / 逐轮机器事实、代次协议与事前登记分别回 [../pipeline/](../pipeline/) 和 [../discover_matrix/](../discover_matrix/) 核对。旧 v46 自包含报告在 [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md)，仅作历史。 |
| 机器 / 一手事实源位置 | [../pipeline/readiness_audit/](../pipeline/readiness_audit/)；[../corpora/](../corpora/) |

本 SUMMARY 不复制完整大表。row-level canonical facts 以 [../pipeline/](../pipeline/) 下 JSON / JSONL / ZIP / committed artifact，以及 [../corpora/](../corpora/) 下的一手 raw / extracted assets 为准。

> **历史口径提醒**：下方 active report 总表中的 R5 / R5.5 报告是 **pre-R5.7 / pre-strategy-reset historical reports**。它们可能保留 “Better STM”、`STM_k` 或早期 scope wording，但这些 wording 只反映当时的方向性探索；不得作为当前 paper1 的 active evaluation framework、method result、baseline contract 或 `fcstm` contribution 证据。当前 story / contribution / evaluation 口径以 [../README.md](../README.md)、[../story/README.md](../archive/r8_story_pre_rebuild/story/README.md) 与 [../experiment_design/README.md](../experiment_design/README.md) 为准。

## 2. Active report 总表

状态口径：🟢 = 已迁移且有来源 / 证据 / 复验入口；🟡 = 缺少来源、证据锚点、复验命令或 caveat；🔴 = 不应作为 canonical report 使用。

| report | 精确时间 | 类型 | 状态 | 核心结论一句话 |
|---|---|---|---|---|
| [2026-08-19-luna-terra-provider-health.md](./2026-08-19-luna-terra-provider-health.md) | 2026-08-19 | provider 健康探针 | 🟢 | 四个时间窗显示 Terra 可间歇恢复，而 Luna 仅短暂成功后再次 0/6；正式运行默认 transport retry 为 8，且只对精确识别的 provider/relay failure 原地重试。 |
| [2026-08-19-judge-model-comparison.md](./2026-08-19-judge-model-comparison.md) | 2026-08-19 | judge sensitivity 与分层协议 | 🟢 | Luna 可作开发期版本筛选，Sol 负责冻结候选的正式 54/54 headline；两套标签不得混用。 |
| [2026-08-19-luna-full-x3-v26.md](./2026-08-19-luna-full-x3-v26.md) | 2026-08-19 | 当前全量 x3 正式实验 | 🟢 | Sol 54/54 release-only 对账下，v26 的 L2、D2×L2 和 precision 高于 X1v2，但 overall hit 仍低于 baseline。 |
| [2026-08-11-post-refactor-e2e-smoke.md](./2026-08-11-post-refactor-e2e-smoke.md) | 2026-08-11 | 重构后 e2e smoke | 🟢 | 大规模目录重构后的端到端验证：`0000` × claude / gpt 各 1 轮，两格均 completed / coverage=full / 零降级零重试，输入哈希与搬迁前逐字节相同，发现的 4 条与 v46 逐条对应。⛔ **工程验证，数字不得进论文统计**。 |
| [2026-07-19-issue-161-plantuml-java-frontend.md](./2026-07-19-issue-161-plantuml-java-frontend.md) | 2026-07-19 | PlantUML Java frontend | 🟢 | **本表中与当前语料关系最直接的一份**：Issue #161 放弃 `PlantUML -> SCXML -> canonical` 路线，改用 Java source frontend，60 例 active 语料由此产生。技术路线报告，不是实验结果。 |
| [2026-07-08-14-03-59-pr-source-trace-contract.md](./2026-07-08-14-03-59-pr-source-trace-contract.md) | 2026-07-08 14:03:59 | source trace contract | 🟢 | source trace v0 合同报告；定义 raw/source ↔ intermediate trace、projection status 与 negative attribution gate，不是实验结果。 |
| [2026-07-08-10-15-00-pr-issue-ledger-contract.md](./2026-07-08-10-15-00-pr-issue-ledger-contract.md) | 2026-07-08 10:15:00 | issue ledger contract | 🟢 | source issue ledger v0 合同报告；定义 candidate / confirmed / rejected / out-of-scope / insufficient-evidence gate，不是实验结果。 |
| [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | 2026-06-29 19:55:45 | PlantUML blocked recovery | 🟢 | `llms-emp` 三个原 blocked 已恢复为 partial；conversion recovery 不计 repair gain。 |
| [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | 2026-06-29 00:03:56 | main seed profile | 🟢 | 10 NL cluster × 6 LLM 输出的历史画像；当前状态数字以 R5.5.2 recovery report 为准。 |
| [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | 2026-06-28 23:18:32 | negative evidence | 🟢 | 旧 blocked 的历史负证据；当前 `llms-emp` blocked 状态已被 R5.5.2 覆盖。 |
| [2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md) | 2026-06-28 22:54:39 | scope handoff | 🟢 | T0/T0.5/T1 历史 scope handoff；当前 active scope 以 story/model_scope.md 为准。 |
| [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) | 2026-06-28 19:42:58 | directional analysis | 🟢 | 解释为什么 `llms-emp-stm-subset` 成为优先主 seed 池。 |
| [2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) | 2026-06-28 04:03:18 | seed readiness | 🟢 | R5 seed readiness 历史快照；`llms-emp` 当前状态以 R5.5.2 为准。 |
| [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md) | 2026-06-28 03:42:24 | selected smoke | 🟢 | 四例 pre-repair baseline smoke；不是修正失败或修正成功。 |

## 3. Archived R5.7 report chain

以下六份 R5.7 报告已经迁入 [../archive/r5_7_better_stm_snapshot/reports/](../archive/r5_7_better_stm_snapshot/reports/)，只作 historical / calibration-only：

| archived report | 历史内容 | 禁止误读 |
|---|---|---|
| [R5.7.1 evaluation logic](../archive/r5_7_better_stm_snapshot/reports/2026-07-02-17-02-42-r5-7-1-evaluation-logic.md) | 旧 evaluation logic handoff。 | 不作为 active closure metric。 |
| [R5.7.2 Better STM target contract](../archive/r5_7_better_stm_snapshot/reports/2026-07-03-02-16-16-r5-7-2-better-stm-target-contract.md) | 旧 Better STM / repair target contract。 | 不作为 active issue taxonomy。 |
| [R5.7.3 objective metric framework](../archive/r5_7_better_stm_snapshot/reports/2026-07-03-21-18-25-r5-7-3-objective-metric-framework.md) | 旧 objective metric framework。 | 不作为 active metric / threshold。 |
| [R5.7.4 static adjudication](../archive/r5_7_better_stm_snapshot/reports/2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) | 四例 static dry-run。 | 不作为真实 repair result。 |
| [R5.7.5 constructed coverage](../archive/r5_7_better_stm_snapshot/reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md) | constructed `STM_k` suite。 | 不作为 agent-loop output。 |
| [R5.7.5 full blind adjudication](../archive/r5_7_better_stm_snapshot/reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md) | blind judge calibration。 | 不作为 method effectiveness / judge reliability claim。 |

## 4. 风险与待复查项

1. R5/R5.5 report 中的完整表是 human-facing snapshot；若修改 [../pipeline/readiness_audit/](../pipeline/readiness_audit/) 的 JSONL，必须同步复核 report。
2. `condition_like_label_lowered_as_event` 等现象只能作为 candidate symptom，不得自动升级为 confirmed source-level issue。
3. Digital Camera/T1 只能作为 supplementary stress，不支撑 T0 主 claim。
4. `llms-emp` 当前已无 blocked pair；旧 blocked 只作历史负证据和 conversion-recovery 线索。
5. R5.7 archived 报告不得回流为 active evaluation protocol；后续 final rubric 必须等 pilot 后重新冻结。
6. issue ledger contract report 只证明 v0 schema / fixture / gate 存在，不证明真实 discovery / repair / closure 效果。
7. source trace contract report 只证明 trace / projection / attribution gate 存在，不证明真实 source-level patch export 或 closure 效果。

## 5. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-08-19 | 补录 v26 全量正式报告、Luna/Sol judge 对照和 Luna/Terra provider 健康探针；active report 计数由 11 更新为 14，并撤销“当前实验结果不在本目录”的过时声明。 |
| 2026-08-11 | 补录两份**此前在本总账中完全缺席**的 report：`2026-07-19-issue-161-plantuml-java-frontend.md` 与 `2026-08-11-post-refactor-e2e-smoke.md`；active report 计数由 9 更正为 11。⚠️ 两份都早已在 [README.md](./README.md) §2 的 active 表里，只有本 SUMMARY 漏登——**两张表必须同增同减**，新增 report 时不要只改一处。同时补上「每代次实验报告不落在本目录」这条口径的入口行。 |
| 2026-07-08 14:03:59 | `PR-source-trace` 新增 source trace contract report，并把 active report 计数从 8 更新为 9。 |
| 2026-07-08 10:15:00 | `PR-issue-ledger` 新增 issue ledger contract report，并把 active report 计数从 7 更新为 8。 |
| 2026-07-08 00:20:00 | `PR-better-archive` review 后补充 R5 / R5.5 active report 的 historical wording 提醒，避免早期 Better STM / `STM_k` wording 被误读为当前 active 口径。 |
| 2026-07-07 23:40:00 | `PR-better-archive` 后将 R5.7.1--R5.7.5 六份报告从 active reports 总账移到 archive pointer。 |
| 2026-06-30 15:32:00 | 按 R5.6 academic review 修正 reports 总账 currentness：明确 4 份旧 report 仅被 R5.5.2 部分覆盖，当前 `llms-emp` 状态数字以 R5.5.2 recovery report 为准。 |
| 2026-06-29 01:48:34 | 初始化 reports 文库，迁移秒级 human-facing report，并建立入口三件套。 |
