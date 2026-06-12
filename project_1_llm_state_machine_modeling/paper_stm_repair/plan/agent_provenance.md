# agent provenance：PR-R0 reviewer 与实现记录

## 1. 目的

本文件记录 PR-R0 中主 session、reviewer、实现侧 subagent 的输入输出和结论，便于后续审计。它不是论文方法贡献。

## 2. Plan-stage reviewers

| 轮次 | reviewer | 入口 | 结论 | 备注 |
|---|---|---|---|---|
| 初始 plan review | codex reviewer | PR #102 comments | C=0 / I=0 | 确认初始 contract 可执行。 |
| 初始 plan review | claude reviewer | PR #102 comments | C=0 / I=0 或仅 M | 确认导师定调一致。 |
| 初始 plan review | deepseek reviewer | PR #102 comments | 曾提出 I；后续修复 | 促成 R0 核心 / 辅助边界和 `paper_v1/` 共存策略。 |
| 路径修正后复审 | codex reviewer | <https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692686352> | C=0 / I=0 | 确认 `paper_stm_repair/` 路径 ready。 |
| 路径修正后复审 | claude reviewer | <https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692678198> | C=0 / I=0 | 提供措辞 M 建议。 |
| 路径修正后复审 | deepseek reviewer | <https://github.com/HansBug/research_ideas/pull/102#issuecomment-4692683224> | C=0 / I=0 | 确认路径、旧 `paper_v1/`、foundation 边界。 |

## 3. 实现侧 subagent

| subagent | 任务 | 使用方式 | 状态 |
|---|---|---|---|
| story 草案 subagent | 只读分析 PR #102 / #100 / talks，提供 `story/` 文档建议。 | 作为实现参考；主 session 最终整合落盘。 | 已完成。 |
| evidence / experiment / plan 草案 subagent | 只读分析 PR #102 / #100 / talks，提供 `evidence/`、`experiment_design/`、`plan/` 文档建议。 | 作为实现参考；主 session 最终整合落盘。 | 已完成。 |

## 4. 主 session 决策

1. 采用 `project_1_llm_state_machine_modeling/paper_stm_repair/` 作为新主线根路径。
2. 不在旧 `paper_v1/` 下追加新子目录。
3. 不拥有、不修改、不继承 `path1_foundation/`。
4. R0 只冻结 story/scope/claim gate；R1--R7 承担资产、样本、转换器、评价门、runtime、评价协议和论文正文。

## 5. 后续实现 review 要求

实现完成后，codex / claude / deepseek 三路 reviewer 应重点检查：

1. 文档是否与 PR body 一致。
2. 是否有旧 `NL -> STM` story 回流。
3. 是否把 `fcstm` / DSL 写成贡献。
4. 是否误动旧 `paper_v1/path1_foundation/`。
5. 是否把 R1--R7 内容提前冻结。
6. Markdown 链接和路径是否可用。
