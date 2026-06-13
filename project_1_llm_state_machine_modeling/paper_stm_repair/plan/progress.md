# paper_stm_repair progress

## 1. 当前阶段

| 字段 | 状态 |
|---|---|
| 2026-06-14 00:16:15 | 按最新讨论补充 strict seed 大规模文献调研协议：定义 `NL -> T0（无关键时间语义）FSM/HSM/EFSM/statechart` 四谓词、硬排除码、多维指标、分级标准、337 条 `sources/` strict-source 子池统计，以及 direct baseline / reproduction / reviewer corpus 的 strict 使用边界。 |
| 2026-06-13 01:18:00 | 按人工审阅意见补充 R1 是阶段性资产候选证据而非最终论文论证；扩充九个 direct baseline 的候选级证据闭合表，并明确 R2--R6 可按真实实验结果回填 / 局部校准链路。 |
| 2026-06-13 00:57:00 | 修复 deepseek reviewer 指出的 R1 evidence forbidden wording；补充 `sources/` 715 篇 `🟢 直接可用` 的统计口径说明和 R1 本地检查记录。 |
| PR | [#104](https://github.com/HansBug/research_ideas/pull/104) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | R1 implementation / strict seed 调研协议补充后 review iteration |
| 四例真实运行 | 不需要；R1 是文档 / 资产审计 / seed 调研协议。 |
| 真实 LLM 调用 | 不需要。 |
| method runtime 修改 | 不涉及。 |
| `path1_foundation/` 修改 | 不允许。 |

## 2. 已消费输入

| 输入 | 用途 |
|---|---|
| PR #100 body | R0 范围、子 PR 依赖、四例运行要求、评价门顺序。 |
| PR #99 会后定调 comment | 第一篇转向与第二篇背景。 |
| [../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md](../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | 正式导师定调事实源。 |
| [../../talks/SUMMARY.md](../../talks/SUMMARY.md) | 当前高优先级约束。 |
| 旧 [../../paper_v1/](../../paper_v1/) | 历史目录与旧 story 共存风险。 |

## 3. 已产出文件

| 文件 | 状态 |
|---|---|
| [../README.md](../README.md) | 已创建 |
| [../story/README.md](../story/README.md) | 已创建 |
| [../story/paper_story.md](../story/paper_story.md) | 已创建 |
| [../story/task_boundary.md](../story/task_boundary.md) | 已创建 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | 已创建 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 已创建 |
| [../story/paper_outline.md](../story/paper_outline.md) | 已创建 |
| [../evidence/README.md](../evidence/README.md) | 已创建 |
| [../evidence/upstream_fact_ledger.md](../evidence/upstream_fact_ledger.md) | 已创建 |
| [../evidence/legacy_asset_inheritance.md](../evidence/legacy_asset_inheritance.md) | 已创建 |
| [../experiment_design/README.md](../experiment_design/README.md) | 已创建 |
| [../experiment_design/research_questions.md](../experiment_design/research_questions.md) | 已创建 |
| [../experiment_design/better_stm_definition.md](../experiment_design/better_stm_definition.md) | 已创建 |
| [../experiment_design/evaluation_gate.md](../experiment_design/evaluation_gate.md) | 已创建 |
| [./README.md](./README.md) | 已创建 |
| [./agent_provenance.md](./agent_provenance.md) | 已创建 |

## 4. Plan review 状态

| reviewer | comment | 结论 |
|---|---|---|
| codex reviewer | [路径修正后复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692686352) | C=0 / I=0 |
| claude reviewer | [路径修正后复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692678198) | C=0 / I=0 |
| deepseek reviewer | [路径修正后复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692683224) | C=0 / I=0 |
| 主 session | [plan review 收口](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692696625) | 已进入实现 |


## 4.1 Implementation review 状态

| reviewer | comment | 结论 |
|---|---|---|
| deepseek reviewer | [最终复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692946713) | C=0 / I=0 / M=0，implementation ready |
| claude reviewer | [最终复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692952218) | C=0 / I=0 / M=3，implementation ready |
| codex reviewer | [最终复审](https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692966223) | C=0 / I=0 / M=2，implementation ready |

上一轮 implementation review 发现的旧 `paper_v1/better_stm_repair_loop/` 双事实源问题已通过提交 `f8bc3408` 修复：旧目录已从 diff 消失，PR body 目录树已收敛到 `paper_stm_repair/`。

## 5. 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| Markdown 相对链接 | 自定义 Python 链接检查脚本 | 通过；missing links = 0。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| forbidden wording grep | `grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|NL -> STM.*主贡献" project_1_llm_state_machine_modeling/paper_stm_repair` | 命中均位于 forbidden / 降级 / 自检语境；未发现旧 story 回流。 |
| `path1_foundation` 修改 | `git diff --name-only origin/paper1/better-stm-repair-loop-umbrella...HEAD | grep path1_foundation` | 通过；无命中。 |
| 四例真实运行 | 按 PR #100 / #102 R0 合同 | 不执行。 |
| 真实 LLM 调用 | 按 R0 范围 | 不执行。 |
| CI / feedback-smoke | `gh pr checks 102` | 通过；`feedback-smoke` success。 |
| Codecov / coverage | PR comments / checks | 未发现 Codecov 覆盖率评论；本 PR 为 docs-only，无单测覆盖率变化，未虚构 coverage。 |

## 6. 剩余风险

| 风险 | 状态 | 后续处理 |
|---|---|---|
| R0 当前 story 仍是可迭代基线，部分论证链需等待真实实验回填。 | 已显式说明 | R1--R6 根据事实证据校准 claim、RQ 与大纲 |
| baseline / prior artifact 可用性尚未盘点。 | 已知未闭合 | PR-R1 |
| 四例样本尚未冻结。 | 已知未闭合 | PR-R2 |
| 转换器范围尚未冻结。 | 已知未闭合 | PR-R3 |
| 评价量表和主结果 eligibility 尚未冻结。 | 已知未闭合 | PR-R4 / PR-R6 |
| 修正循环效果尚未实证。 | 已知未闭合 | PR-R5 / PR-R6 |
| R1 当前资产审计仍是候选级证据，部分链路需等待 R2--R6 真实实验回填。 | 已显式说明 | R2 样本冻结、R3 转换器、R4--R6 实验结果出来后校准候选角色和论文 story。 |

## 7. Capability-use audit

| 项 | 记录 |
|---|---|
| 使用技能 | sub-agents；ai-research-writing-skill 的 claim-evidence discipline。 |
| 真实 LLM / API | 未调用。 |
| 外部网络 | 通过 `gh` 读取 / 更新 PR。 |
| 产物类型 | Markdown planning docs。 |
| 覆盖率 | docs-only，预计无 Codecov 覆盖率变化。 |

## 8. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-14 00:16:15 | PR-R1 补充 strict seed 大规模文献调研协议、初始统计和 review gate；等待补充后多智能体复审。 |
| 2026-06-13 00:45:00 | PR-R1 创建 baseline 资产审计文档：source coverage、branch-local trace、候选矩阵、artifact 可获取性与格式转换压力；本轮不改写 R0 completion 结论。 |
| 2026-06-13 00:19:18 | 按人工审阅意见补充 R0 是可执行论文工作基线而非最终论证链；后续 R1--R6 可按真实实验结果回填并局部校准 story / RQ / claim。 |
| 2026-06-13 00:08:00 | 三路 implementation re-review 均 C=0/I=0；feedback-smoke 通过；记录 docs-only 无 Codecov 覆盖率变化。 |
| 2026-06-12 23:43:33 | 完成本地链接、diff、forbidden wording 与 `path1_foundation` 修改检查；补充旧 `paper_v1/README.md` 入口提示。 |
| 2026-06-12 23:42:20 | 初始化 R0 文档路径与 progress 记录。 |

## 9. PR-R1 进度

| 字段 | 状态 |
|---|---|
| PR | [#104](https://github.com/HansBug/research_ideas/pull/104) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | R1 implementation / strict seed 调研协议补充后 review iteration |
| 四例真实运行 | 不需要；R1 是资产审计。 |
| 真实 LLM 调用 | 不需要。 |
| method runtime 修改 | 不涉及。 |
| `path1_foundation/` 修改 | 不允许；仅在 [../evidence/branch_asset_trace.md](../evidence/branch_asset_trace.md) 记录分支局部状态。 |

### 9.1 R1 已消费输入

| 输入 | 用途 |
|---|---|
| PR #100 body | R1 合同、字段、四例运行边界、后续依赖。 |
| PR-R0 / #102 文档 | 本地事实锚点，尤其是旧资产继承边界与 Better STM 定义。 |
| [../../baselines/SUMMARY.md](../../baselines/SUMMARY.md) | 91 篇 baseline 总账、九个五绿 direct baseline 与数据集清单。 |
| 九个 direct baseline `ASSETS.md` | 代码 / 数据 / artifact / 结果可获取性深审输入。 |
| [../../sources/SUMMARY.md](../../sources/SUMMARY.md) | 787 篇真实控制系统 seed 池规模与状态分布。 |
| PR #93/#94/#96 gh / git 状态 | 分支局部资产状态与消费决策。 |

### 9.2 R1 已产出文件

| 文件 | 状态 |
|---|---|
| [../evidence/baseline_asset_audit.md](../evidence/baseline_asset_audit.md) | 已创建 |
| [../evidence/baseline_candidate_matrix.md](../evidence/baseline_candidate_matrix.md) | 已创建 |
| [../evidence/artifact_availability_ledger.md](../evidence/artifact_availability_ledger.md) | 已创建 |
| [../evidence/format_conversion_matrix.md](../evidence/format_conversion_matrix.md) | 已创建 |
| [../evidence/branch_asset_trace.md](../evidence/branch_asset_trace.md) | 已创建 |
| [../evidence/source_coverage_ledger.md](../evidence/source_coverage_ledger.md) | 已创建 |
| [../evidence/strict_seed_literature_survey.md](../evidence/strict_seed_literature_survey.md) | 已创建 |

### 9.2.1 R1 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| Markdown 相对链接 | 自定义 Python 链接检查脚本，范围 `project_1_llm_state_machine_modeling/paper_stm_repair` | 通过；missing links = 0。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| forbidden wording grep | `grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|NL -> STM.*主贡献" project_1_llm_state_machine_modeling/paper_stm_repair` | 修复 R1 evidence 中的 `最强` 后，命中仅位于 forbidden / 降级 / 自检语境。 |
| `path1_foundation` 修改 | `git diff --name-only origin/paper1/better-stm-repair-loop-umbrella...HEAD | grep path1_foundation` | 通过；无命中。 |
| 四例真实运行 | 按 PR #100 / #104 R1 合同 | 不执行。 |
| 真实 LLM 调用 | 按 R1 范围 | 不执行。 |

### 9.3 R1 已知边界

| 边界 | 说明 |
|---|---|
| 未逐篇深审全部 91 篇 baseline | R1 对 91 篇做 summary-level closure，对 9 个 direct baseline 和部分强近邻做深审；未完成全部 91 篇 strict seed eligibility 闭合。 |
| 未冻结四例 seed | R2 才能基于本审计选择样本；`sources/` 的 337 条 strict-source 子池仍需构造 / 冻结 `STM_0`。 |
| 未验证转换器 | R3 才能把“可转换性评估”变成 schema / fixture / adapter。 |
| 未复跑外部 artifact | 活链接、仓库 HEAD、Drive / 4open / 3GPP dynareport 等正式实验前仍需冻结。 |

## PR-R1.5：strict seed 文献调研与 seed 文库（进行中）

- 时间：2026-06-14 01:40:00
- PR：[#106](https://github.com/HansBug/research_ideas/pull/106)
- 当前状态：PR body 三路初审发现 C=0/I>0 后已修复；codex / deepseek 快速复审无 C/I；claude 复审指出 `SA-3` 不应计入主 seed 可交接下限，已修复 PR body 与本地 GUIDE/SUMMARY。
- 已产出：`seed_corpus/README.md`、`GUIDE.md`、`SUMMARY.md`、`candidate_matrix.md`、`search_log.md`、`screening_ledger.md`、`exclusion_ledger.md`、`manual_download_queue.md`、`agent_provenance.md` 与 9 个初始单篇候选目录。
- 初始 bounded snapshot：candidate_matrix 已超过 20 条候选；本地 baseline/reproduction 初筛超过 8 条 fulltext/artifact 候选；主 seed 可交接候选仍需单篇 agent 复核到 `SS-A/SS-B + SA-1/SA-2`。
- 检索风险：OpenAlex 两条宽 query 噪声很高，已记录为失败/早停经验；后续需 exact phrase、排除词、IEEE/ACM/DBLP/publisher 与 snowballing 补强。
- 四例运行：本 PR 不跑四例、不调用真实 LLM、不读取 `.env`。

### Capability-use audit

- Required references/scripts: `ai-research-writing-skill` task-state gate、`literature-search` OpenAlex 脚本、`sub-agents` 外部 reviewer/reader。
- Inputs consumed: PR #100 body、PR #104 strict seed 协议、baseline/reproduction/sources scout 结果、外部 search planner 结果。
- Inputs not used and why: IEEE/ACM/DBLP 正式检索尚未执行，需要后续联网或人工检索补齐。
- Artifacts produced: `paper_stm_repair/seed_corpus/` 初始文库结构与候选矩阵。
- Verification run: body 三路 review 与快速复审；本地文件尚待 markdown/link 检查。
- Remaining risk: 单篇全文 reader 仍在运行，9 个高优先本地候选已由 paper-reader agent 完成单篇编码；外部下载 / IEEE / ACM / DBLP / snowballing 仍待补。
