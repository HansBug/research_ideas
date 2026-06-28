# reports/SUMMARY.md — 研究报告总账

## 1. 当前总览

| 项 | 数量 / 状态 |
|---|---|
| canonical human-facing reports | 6 |
| 已 superseded reports | 0 |
| 待来源复核 reports | 0 |
| 当前主入口 | [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) |
| 机器事实源位置 | [../pipeline/readiness_audit/](../pipeline/readiness_audit/) |

本目录只做稳定研究报告总账。row-level canonical facts 以 [../pipeline/](../pipeline/) 下 JSON / JSONL / ZIP / committed artifact 为准；本 SUMMARY 不复制完整大表。

## 2. 报告总表

状态口径：🟢 = 已迁移并含来源考据表；🟡 = 需补来源或链接；🔴 = 不应作为 canonical report 使用。时间口径：`freeze` = 结论冻结时间；`migration` = 原冻结时间不可恢复，只能按迁移时间。

| report | 精确时间 | 时间口径 | 阶段 | 类型 | 状态 | 核心结论一句话 | canonical machine source | 来源 commit | superseded_by |
|---|---|---|---|---|---|---|---|---|---|
| [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | 2026-06-29 00:03:56 | `freeze` | R5.5 | main seed profile | 🟢 | `llms-emp` 主 seed 池为 10 NL × 6 LLM；16 converted / 41 partial / 3 blocked，后续按 cluster 报告。 | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[llms_emp_cluster_llm_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl) | `49f34c39b8f8ecf037c60d8ab54d9c33ea1c443a` | — |
| [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | 2026-06-28 23:18:32 | `freeze` | R5.5 | negative evidence | 🟢 | 3 个 blocked 样例当前只能说明 committed evidence 未复现可信 SCXML，不证明不可渲染。 | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl)、[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) | `81995de735586b602284e02cea0f0754f36b37b1` | — |
| [2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md) | 2026-06-28 22:54:39 | `freeze` | R5.5 -> R5.6 | scope handoff | 🟢 | `proceed_with_supplementary`：T0/T0.5 作为主线，Digital Camera/T1 与 blocked 进入 supplementary / negative evidence。 | [llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | `ee35e44407c85835dc4f3ec669477e298d89cb8a` | — |
| [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) | 2026-06-28 19:42:58 | `freeze` | R5 | directional analysis | 🟢 | `llms-emp-stm-subset` 是 R6/R7 优先主 seed 池；60 pair 应解释为 10 NL cluster × 6 LLM。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)、[llms-emp records zip](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` | — |
| [2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) | 2026-06-28 04:03:18 | `freeze` | R5 | seed readiness | 🟢 | R5 seed library denominator、entry/pair 状态、抽样、blocked/partial 阅读入口已经冻结。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)、[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) | `185aa02c26caba9eece9327248379004fd7f6488` | — |
| [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md) | 2026-06-28 03:42:24 | `freeze` | R5 | selected smoke | 🟢 | 四例全部为 `partial` 但 contract checks 通过；这是 pre-repair baseline，不是修正失败。 | [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json) | `5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4` | — |

## 3. 当前阅读路线

1. **主 seed profile**：[2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。用于回答“10 个 NL 分别是什么、状态如何、风险是什么”。
2. **负证据**：[2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md)。用于回答 blocked 是否应 drop、修或后置。
3. **scope handoff**：[2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md)。用于后续 R5.6 story / scope 冻结。
4. **R5 历史方向分析**：[2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)。用于解释为什么主线从全 seed library 收敛到 `llms-emp`。
5. **readiness denominator**：[2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) 与 [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md)。用于复盘 R5 准备度边界。

## 4. 风险与待复查项

1. report 中的完整表是 human snapshot；后续若修改 [../pipeline/readiness_audit/llms_emp_profile/](../pipeline/readiness_audit/llms_emp_profile/) 的 JSONL，必须同步再生成或复核 report 表格。
2. `condition_like_label_lowered_as_event` 只能作为 R5.7 repair-target 候选，不能直接写成已确认语义缺陷。
3. Digital Camera/T1 只能作为 supplementary stress，不支撑 T0 主 claim。
4. blocked 样例目前是 committed evidence 下的负证据；不能外推为“官方工具永远不可渲染”。

## 5. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-29 01:48:34 | 初始化 reports 文库，迁移 6 份秒级 human-facing report，并建立入口三件套。 |
