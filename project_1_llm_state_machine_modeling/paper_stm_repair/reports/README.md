# reports 研究报告文库

## 1. 文库定位

本目录是 `paper_stm_repair/` 下 **面向人类阅读的稳定研究报告文库**。它负责保存 seed readiness、main seed profile、negative evidence、handoff、story-facing analysis 等已经形成稳定结论的 Markdown report，供论文写作、审查和后续阶段决策引用。

它不是 pipeline 输出目录，也不是 PR 施工进度台账。机器事实源仍保存在 [../pipeline/](../pipeline/) 的 JSON / JSONL / ZIP / schema / CLI / tests 中；本目录只保存人类可读快照、解释和学术风险分析。

## 2. 收录范围与排除范围

| 类型 | 是否进入本目录 | 说明 |
|---|---:|---|
| seed readiness 报告 | 是 | 例如 R5 全量 seed 摸排的人类阅读入口。 |
| main seed profile | 是 | 例如 `llms-emp` 10 NL cluster × 6 LLM 输出的画像表。 |
| negative evidence / blocked 分析 | 是 | 用于解释不能进入主实验或需要 converter follow-up 的稳定证据。 |
| story / scope handoff | 是 | 只记录稳定研究结论和后续入口，不记录 PR 动态状态。 |
| JSON / JSONL / ZIP / schema | 否 | 放在 [../pipeline/](../pipeline/)；reports 只链接它们。 |
| raw seed assets / extracted pairs | 否 | 放在 [../corpora/](../corpora/)；reports 只引用。 |
| PR review 状态 / merge 进度 / CI 状态 | 否 | 维护在 GitHub PR body / comment。 |

## 3. 与其他路径的边界

| 路径 | 职责 | 与 reports 的关系 |
|---|---|---|
| [../pipeline/](../pipeline/) | 可复算机器事实源、schema、CLI、测试与高基数运行制品。 | reports 必须声明 canonical machine source；row-level facts 以 pipeline 为准。 |
| [../corpora/](../corpora/) | 一手 seed、repair baseline、纯 NL 数据源。 | reports 可解释 corpus 结论，但不能替代 corpus 当前总账。 |
| [../experiment_design/](../experiment_design/) | scope、quality model、eligibility、protocol、metrics。 | reports 可作为 handoff；正式实验定义应沉淀到 experiment_design。 |
| [../story/](../story/) | 论文叙事、claim gate 与写作定位。 | story 引用 reports 的稳定结论，不从 reports 复制成第二事实源。 |
| [../evidence/](../evidence/) | 历史审计与证据索引。 | reports 面向当前 paper 决策；evidence 保存历史来龙去脉。 |

## 4. 报告列表

| 时间 | report | 类型 | 机器事实源入口 |
|---|---|---|---|
| 2026-06-29 00:03:56 | [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) | main seed profile | [llms_emp_case_matrix.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_case_matrix.jsonl) |
| 2026-06-28 23:18:32 | [2026-06-28-23-18-32-negative-evidence-report.md](./2026-06-28-23-18-32-negative-evidence-report.md) | negative evidence | [llms_emp_blocked_probe.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_blocked_probe.jsonl) |
| 2026-06-28 22:54:39 | [2026-06-28-22-54-39-model-scope-handoff.md](./2026-06-28-22-54-39-model-scope-handoff.md) | scope handoff | [llms_emp_cluster_profiles.jsonl](../pipeline/readiness_audit/llms_emp_profile/llms_emp_cluster_profiles.jsonl) |
| 2026-06-28 19:42:58 | [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md) | directional analysis | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) |
| 2026-06-28 04:03:18 | [2026-06-28-04-03-18-seed-readiness-report.md](./2026-06-28-04-03-18-seed-readiness-report.md) | seed readiness | [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) |
| 2026-06-28 03:42:24 | [2026-06-28-03-42-24-selected-smoke-summary.md](./2026-06-28-03-42-24-selected-smoke-summary.md) | selected smoke | [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json) |

## 5. 推荐阅读顺序

1. 先读本文件，确认 reports 文库边界。
2. 再读 [GUIDE.md](./GUIDE.md)，理解秒级命名、来源考据和 machine-source 同步纪律。
3. 再读 [SUMMARY.md](./SUMMARY.md)，从总表选择当前要看的 report。
4. 想看 R5.5 主结论：读 [2026-06-29-00-03-56-llms-emp-main-seed-profile.md](./2026-06-29-00-03-56-llms-emp-main-seed-profile.md) 的 10 cluster 表、10×6 LLM 矩阵与行为特征矩阵。
5. 想解释后续 R6/R7 为什么优先 `llms-emp-stm-subset`：读 [2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)。
6. 需要复算或审计时，回到每个 report 文末“审计附录：证据链与事实源”中的上游事实源清单、Claim-evidence map 与复验命令。

## 6. 命名纪律

除本目录三件套 [README.md](./README.md)、[SUMMARY.md](./SUMMARY.md)、[GUIDE.md](./GUIDE.md) 外，所有长期 report 必须使用秒级时间前缀：

```text
yyyy-mm-dd-hh-mm-ss-short-slug.md
```

时间前缀表示报告核心学术结论冻结时间；迁移、路径重命名和链接修正不得改变该时间，但必须进入 report 文末审计附录的 A.1 来源考据表。
