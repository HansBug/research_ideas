# reports/SUMMARY.md — 研究报告总账

## 1. 当前总览

| 项 | 数量 / 状态 |
|---|---|
| canonical human-facing reports | 7 |
| 已部分 superseded / current-status-overridden reports | 4（R5.5.2 覆盖 R5 directional analysis、main seed profile、scope handoff、negative evidence report 中的 blocked/current-status 部分；这些 report 仍保留历史画像和方向性价值） |
| 待来源复核 reports | 0 |
| 当前主入口 | 当前状态数字优先读 [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)；10 cluster / 60 pair 历史画像再读 [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) |
| 机器 / 一手事实源位置 | [../pipeline/readiness_audit/](../pipeline/readiness_audit/)；[../corpora/](../corpora/) |

本目录只做稳定研究报告总账。row-level canonical facts 以 [../pipeline/](../pipeline/) 下 JSON / JSONL / ZIP / committed artifact，以及 [../corpora/](../corpora/) 下的一手 raw / extracted assets 为准；本 SUMMARY 不复制完整大表。报告总表中的 `canonical machine source` 列只列**导航入口**，不等于该 report 的完整证据源清单；完整事实源、claim-evidence map 与复验命令必须回到对应 report 文末 `A.2`–`A.4`。

## 2. 报告总表

状态口径：🟢 = 已迁移，且含来源考据表、上游事实源清单、Claim-evidence map 与复验命令；🟡 = 缺少来源、证据锚点、复验命令或 claim caveat；🔴 = 不应作为 canonical report 使用。时间口径：`freeze` = 结论冻结时间；`migration` = 原冻结时间不可恢复，只能按迁移时间。

| report | 精确时间 | 时间口径 | 阶段 | 类型 | 状态 | 核心结论一句话 | canonical machine source | 来源 commit | superseded_by |
|---|---|---|---|---|---|---|---|---|---|
| [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md) | 2026-06-29 19:55:45 | `freeze` | R5.5.2 | PlantUML blocked recovery | 🟢 | `llms-emp` 三个原 blocked 已恢复为 partial；当前 16 converted / 44 partial / 0 blocked，conversion recovery 不计 repair gain。 | [case matrix](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[PlantUML recovery report](../pipeline/conversion/reports/plantuml_recovery_report.json)、[sweep report](../pipeline/readiness_audit/seed_sweep/sweep_report.json) | 当前 PR 提交 | — |
| [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | 2026-06-29 00:03:56 | `freeze` | R5.5 | main seed profile | 🟢 | `llms-emp` 主 seed 池为 10 NL × 6 LLM；原 R5.5 快照为 16 converted / 41 partial / 3 blocked；当前状态数字必须改读 R5.5.2 recovery report。 | [case matrix](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl)、[cluster profiles](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl)、[LLM matrix](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_llm_matrix.jsonl)、[partial ledger](../pipeline/readiness_audit/llms_emp_profile/llms_emp_partial_attribution_ledger.jsonl)、[blocked probe](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl)；完整清单见 report A.2 | `49f34c39b8f8ecf037c60d8ab54d9c33ea1c443a` | [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)（仅 current-status / blocked 部分） |
| [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | 2026-06-28 23:18:32 | `freeze` | R5.5 | negative evidence | 🟢 | 原 3 个 blocked 样例的历史负证据；当前已由 R5.5.2 恢复为 partial，只能作历史快照。 | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl)、[plantuml_recovery_report.json](../pipeline/conversion/reports/plantuml_recovery_report.json) | `81995de735586b602284e02cea0f0754f36b37b1` | [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)（current-status supersede） |
| [2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md) | 2026-06-28 22:54:39 | `freeze` | R5.5 -> R5.6 | scope handoff | 🟢 | `proceed_with_supplementary`：T0 作为主线；T0.5 仅作 timer-like caveat；Digital Camera/T1 仍为 supplementary stress；旧 blocked 数字已由 R5.5.2 覆盖。 | [llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) | `ee35e44407c85835dc4f3ec669477e298d89cb8a` | [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)（current-status supersede） |
| [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) | 2026-06-28 19:42:58 | `freeze` | R5 | directional analysis | 🟢 | `llms-emp-stm-subset` 是 R6/R7 优先主 seed 池；60 pair 应解释为 10 NL cluster × 6 LLM；旧 16/41/3 状态数字已由 R5.5.2 覆盖。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)、[llms-emp records zip](../pipeline/readiness_audit/artifact_archives/archives/llms-emp-stm-subset_records.zip) | `bbd974c17da1c113eca847c1ae7ba2969c7f0644` | [2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)（current-status supersede） |
| [2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) | 2026-06-28 04:03:18 | `freeze` | R5 | seed readiness | 🟢 | R5 seed library denominator、entry/pair 状态、抽样、blocked/partial 阅读入口已经冻结。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)、[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) | `185aa02c26caba9eece9327248379004fd7f6488` | — |
| [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md) | 2026-06-28 03:42:24 | `freeze` | R5 | selected smoke | 🟢 | 四例全部为 `partial` 但 contract checks 通过；这是 pre-repair baseline，不是修正失败。 | [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json) | `5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4` | — |

## 3. 当前阅读路线

1. **当前 blocked recovery / 状态更新**：[2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md](./2026-06-29-19-55-45-r5-5-2-plantuml-blocked-recovery.md)。用于回答“3 个原 blocked 是否已恢复、当前 60 pair 状态是什么”。
2. **主 seed profile 历史画像**：[2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。用于回答“10 个 NL 分别是什么、状态如何、风险是什么”；其中 blocked/current-status 数字以 R5.5.2 report 为准。
3. **负证据历史快照**：[2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md)。用于回答 blocked 是否应 drop、修或后置。
4. **scope handoff**：[2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md)。用于后续 R5.6 story / scope 冻结。
5. **R5 历史方向分析**：[2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)。用于解释为什么主线从全 seed library 收敛到 `llms-emp`。
6. **readiness denominator**：[2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) 与 [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md)。用于复盘 R5 准备度边界。

## 4. 风险与待复查项

1. report 中的完整表是 human snapshot；后续若修改 [../pipeline/readiness_audit/llms_emp_profile/](../pipeline/readiness_audit/llms_emp_profile/) 的 JSONL，必须同步再生成或复核 report 表格。
2. `condition_like_label_lowered_as_event` 只能作为 R5.7 repair-target 候选，不能直接写成已确认语义缺陷。
3. Digital Camera/T1 只能作为 supplementary stress，不支撑 T0 主 claim。
4. `llms-emp` 当前已无 blocked pair；旧 blocked 只作为 R5.5.1 历史负证据和 R5.5.2 conversion-recovery 线索。其他 seed 源的 blocked 仍需按各自 report / JSON 审计，不能套用 `llms-emp` 当前状态。

## 5. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-30 15:32:00 | 按 R5.6 academic review 修正 reports 总账 currentness：明确 4 份旧 report 仅被 R5.5.2 部分覆盖，当前 `llms-emp` 状态数字以 R5.5.2 recovery report 为准。 |
| 2026-06-29 15:43:00 | 明确本 SUMMARY 的 machine source 列只作导航入口，并补强主 seed profile 的关键事实源入口，完整证据链仍回到各 report 文末 A.2–A.4。 |
| 2026-06-29 14:39:35 | 补齐 6 份 canonical report 的上游事实源清单、Claim-evidence map 与复验命令，并加固 [GUIDE.md](./GUIDE.md) 的证据链纪律。 |
| 2026-06-29 01:48:34 | 初始化 reports 文库，迁移 6 份秒级 human-facing report，并建立入口三件套。 |
