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

## PR-R1.5 seed corpus agent 摘要

| 时间 | agent / 来源 | 任务 | 输出 | 状态 |
|---|---|---|---|---|
| 2026-06-14 | literature scout A | 只读盘点 baseline / reproduction strict seed 候选 | 5 个最可能候选 + 4 个强但不适合主 seed + 排除列表 | completed |
| 2026-06-14 | literature scout B | 只读盘点 sources 宽池抽样策略 | 10 个 sources 优先目录与字段建议 | completed |
| 2026-06-14 | external search planner | 设计外部检索 query plan | Semantic Scholar / arXiv / OpenAlex / Google 替代 query 与 20 个候选线索 | completed |
| 2026-06-14 | paper-reader agents | 高优先单篇全文核验 | 10 个候选目录的 `seed_desc.md` / `artifacts.md` | completed |
| 2026-06-14 | implementation reviewers #106 | 三路实现强审与修复迭代 | 统计闭合、TTool timing、`designing-fsm-gpt4` initial-only、`req-mermaid-statechart` 目录补齐 | completed / C-I fixed / awaiting final ready check |

## PR-R1.6 / #107 agent provenance

| 时间 | agent / 来源 | 任务 | 输出 / 状态 |
|---|---|---|---|
| 2026-06-14 03:10:00 | main session | 创建 PR-R1.6 empty PR、更新 body、完成 body review C/I 修复 | PR [#107](https://github.com/HansBug/research_ideas/pull/107)；body review C/I 闭合后进入实现。 |
| 2026-06-14 03:12:00 | paper-reader agents A-F | 分别核验 completion/GWT、use-case/UML SM、behavior-tree/state-machine、scenario/statechart、LLM recent、classic requirements/statechart 候选 | completed；结果已由主 session 复核后回填 `seed_corpus`。 |

| 2026-06-14 03:55:00 | main session + R1.6 subagents | 整合 Crossref / Zenodo / GitHub / HF / PDF 证据，新增 5 个单篇目录与 `seed_selection_candidates.md` | 36 candidates / 36 screening / 15 dirs / 4 handoff；待 implementation review。 |

## PR-R1.7 / #108 agent provenance

| 时间 | agent / 来源 | 任务 | 输出 / 状态 |
|---|---|---|---|
| 2026-06-14 04:45:00 | main session | 创建 PR-R1.7 empty PR、完成 body review C/I 修复与复审 | PR [#108](https://github.com/HansBug/research_ideas/pull/108)；contract ready 后进入实现。 |
| 2026-06-14 12:00:00 | seed-scout-agent-A | 只读广域文献 scout | 18 个候选、query/source、5 个优先全文对象、噪声模式；无 edits。 |
| 2026-06-14 12:00:00 | seed-scout-agent-B | 只读 artifact/manual queue scout | R1.6 11 条 manual queue 资源状态、6 个新增目录 SS/SA 建议、manual/排除建议；无 edits。 |
| 2026-06-14 12:00:00 | seed-structure-reviewer | 只读结构审查 | 指出 9 个 C 级 gap：round 缺失、central ledger 未同步、manual queue 未收口、SUMMARY/selection 未更新等；已由主 session 修复。 |
| 2026-06-14 12:10:00 | main session | R1.7 实现整合 | 46 candidates / 46 screening / 23 dirs / 8 R1.7 rounds / manual queue 状态分布；negative evidence 表明新增主候选仍不足 6。 |
| 2026-06-14 13:20:00 | main session + sidecar reviewer | R1.7 seed 方法集合口径纠偏 | 补齐旧九个 direct baseline crosswalk，新增 `pushing-generative-envelope-mbse`，更新为 47 candidates / 47 screening / 24 dirs；R2 四例可计候选仍为 4。 |
