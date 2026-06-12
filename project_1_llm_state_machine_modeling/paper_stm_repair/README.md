# 第一篇论文：反馈驱动状态机修正工作区

## 0. 定位

`paper_stm_repair/` 是 project_1 第一篇论文在 2026-06-12 导师讨论后重新冻结的新主线工作区。它承载 **`<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正** 论文规划，不再沿用旧 `NL -> STM` 生成论文主线。

本工作区是 PR [#100](https://github.com/HansBug/research_ideas/pull/100) 下 PR-R0 的落地产物；本 PR 只冻结 story、范围、claim gate、研究问题草案和后续子 PR 接口，不实现 runtime，不跑四例真实样例，不调用真实 LLM。

需要注意的是，R0 当前冻结的是**可执行的论文工作基线**，不是最终论文论证链。由于 baseline artifact 可用性、四例 seed、转换器范围、评价门和真实修正效果尚未经过后续 PR 实证闭合，当前 story 和 RQ 只要求先把方向、边界和禁止 claim 讲清楚；后续 PR-R1--R6 若产生新的事实证据，应回填本工作区，并允许在不突破导师定调的前提下局部调整论证链、术语侧重和实验问题。

## 1. 核心口径

| 维度 | R0 冻结口径 |
|---|---|
| 论文主任务 | 给定自然语言需求 `NL` 与初始状态机 `STM_0`，通过无人化反馈驱动循环得到候选 `STM_k`。 |
| `NL -> STM_0` 定位 | seed construction / baseline source / related work，不作为主贡献。 |
| 修正循环 | 单次 repair run 内 no human-in-the-loop；人类只参与 seed 构造、reference / adjudication、最终审计。 |
| 状态机表示 | 语义增强、可机检、可执行表示是 feedback 的必要载体；`fcstm` / `pyfcstm` / DSL 不进标题、摘要或贡献位。 |
| Better STM | 必须按预注册诊断、场景、人工裁决与转换归因台账操作化，不是宣传词。 |
| baseline 角色 | seed artifact、转换压力、错误类型来源、有限对照、related work evidence。 |

## 2. 阅读顺序

1. [story/paper_story.md](./story/paper_story.md)：先读主线、gap、contribution 和禁止 claim。
2. [story/task_boundary.md](./story/task_boundary.md)：确认输入输出、人类角色、seed 与 repair loop 边界。
3. [story/terminology_policy.md](./story/terminology_policy.md)：确认术语写法和 `fcstm` 弱化策略。
4. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：确认每条 claim 的证据门与降级写法。
5. [experiment_design/better_stm_definition.md](./experiment_design/better_stm_definition.md)：确认 `Better STM` 的最小操作化定义。
6. [experiment_design/research_questions.md](./experiment_design/research_questions.md)：确认 RQ 草案和后续 PR 依赖。
7. [evidence/upstream_fact_ledger.md](./evidence/upstream_fact_ledger.md)：确认上游事实源等级。
8. [plan/progress.md](./plan/progress.md)：确认当前 PR 执行状态。

## 3. 目录结构

```text
paper_stm_repair/
├── README.md
├── story/
├── evidence/
├── experiment_design/
└── plan/
```

## 4. 与旧目录 / 旧 PR 的关系

- 旧 [paper_v1/](../paper_v1/) 保留为 2026-05 Direction-Decision Sprint / Path-1 / Path-2 历史工作区；其旧 `NL -> STM` / hard comparison 叙事不再作为当前第一篇事实真源。
- 本工作区不拥有、不修改、不继承 PR [#93](https://github.com/HansBug/research_ideas/pull/93) 分支中的 `path1_foundation/` 路径；只参考其“入口 + story + evidence + experiment_design + plan”分层经验。
- PR [#94](https://github.com/HansBug/research_ideas/pull/94) / [#96](https://github.com/HansBug/research_ideas/pull/96) 已合入 #93 分支但未进入 `main`；其内容只能作为分支局部线索。
- 已合入 `main` 的 PR [#73](https://github.com/HansBug/research_ideas/pull/73)、[#82](https://github.com/HansBug/research_ideas/pull/82)、[#92](https://github.com/HansBug/research_ideas/pull/92) 是后续 PR-R1 baseline / seed 资产盘点线索。

## 5. R0 非目标

| 非目标 | 后续落点 |
|---|---|
| 逐篇 baseline 资产盘点、代码 / artifact 可获取性台账 | PR-R1 |
| seed registry 与四例样本冻结 | PR-R2 |
| 多格式转换器 schema / fixture / 归因实现 | PR-R3 |
| 诊断、场景、评价量表 v0 与统计表骨架冻结 | PR-R4 |
| 无人化修正循环 runtime / prompt / LLM 调用 | PR-R5 |
| 主实验协议、对照矩阵、端到端四例预演 | PR-R6 |
| 完整论文正文 / submission package | PR-R7 |

## 6. 上游正式记录

- PR #100 第一篇新伞 PR：<https://github.com/HansBug/research_ideas/pull/100>
- PR #99 会后定调 comment：<https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818>
- 正式导师讨论记录：[2026-06-12-导师-两篇论文转向与模型修正定调.md](../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)
- project_1 导师讨论总账：[talks/SUMMARY.md](../talks/SUMMARY.md)

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-12 23:42:20 | 初始化 PR-R0 新工作区，冻结 `<NL, STM_0> -> STM_k / Better STM` 主线、路径结构与后续子 PR 接口。 |
