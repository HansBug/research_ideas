# PR-R0 progress

## 1. 当前阶段

| 字段 | 状态 |
|---|---|
| PR | [#102](https://github.com/HansBug/research_ideas/pull/102) |
| 上游 PR | [#100](https://github.com/HansBug/research_ideas/pull/100) |
| 当前阶段 | Impl-1：R0 文档落地 |
| 四例真实运行 | 不需要；R0 是文档 / story gate。 |
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

## 5. 本地检查记录

| 检查 | 命令 / 口径 | 结果 |
|---|---|---|
| Markdown 相对链接 | 自定义 Python 链接检查脚本 | 通过；missing links = 0。 |
| Markdown diff whitespace | `git diff --check` | 通过。 |
| forbidden wording grep | `grep -RIn "首个\|最强\|new DSL\|完整形式化验证\|model checking\|NL -> STM.*主贡献" project_1_llm_state_machine_modeling/paper_stm_repair` | 命中均位于 forbidden / 降级 / 自检语境；未发现旧 story 回流。 |
| `path1_foundation` 修改 | `git diff --name-only origin/paper1/better-stm-repair-loop-umbrella...HEAD | grep path1_foundation` | 通过；无命中。 |
| 四例真实运行 | 按 PR #100 / #102 R0 合同 | 不执行。 |
| 真实 LLM 调用 | 按 R0 范围 | 不执行。 |

## 6. 剩余风险

| 风险 | 状态 | 后续处理 |
|---|---|---|
| baseline / prior artifact 可用性尚未盘点。 | 已知未闭合 | PR-R1 |
| 四例样本尚未冻结。 | 已知未闭合 | PR-R2 |
| 转换器范围尚未冻结。 | 已知未闭合 | PR-R3 |
| 评价量表和主结果 eligibility 尚未冻结。 | 已知未闭合 | PR-R4 / PR-R6 |
| 修正循环效果尚未实证。 | 已知未闭合 | PR-R5 / PR-R6 |

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
| 2026-06-12 23:43:33 | 完成本地链接、diff、forbidden wording 与 `path1_foundation` 修改检查；补充旧 `paper_v1/README.md` 入口提示。 |
| 2026-06-12 23:42:20 | 初始化 R0 文档路径与 progress 记录。 |
