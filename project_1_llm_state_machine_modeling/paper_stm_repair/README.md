# 第一篇论文：反馈驱动状态机修正工作区

## 0. 定位

`paper_stm_repair/` 是 project_1 第一篇论文在 2026-06-12 导师讨论后重新冻结的新主线工作区。它承载 **`<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动状态机修正** 论文规划，不再沿用旧 `NL -> STM` 生成论文主线。

本工作区源自 PR [#100](https://github.com/HansBug/research_ideas/pull/100) 下的第一篇论文新主线落地。GitHub PR / issue body 与 comment 是执行计划、review 状态、ready gate 和 merge 进度的流程真源；本仓库路径只沉淀长期研究定位、文库结构纪律、事实总账与论文材料，不维护 PR 施工流水账。

需要注意的是，这里冻结的是**可执行的论文工作基线**，不是最终论文论证链。由于 baseline artifact 可用性、四例 seed、转换器范围、评价门和真实修正效果尚未经过后续实证闭合，当前 story 和 RQ 只要求先把方向、边界和禁止 claim 讲清楚；后续若产生新的事实证据，应回填本工作区，并允许在不突破导师定调的前提下局部调整论证链、术语侧重和实验问题。

历史 baseline / prior artifact 会逐步改写为 seed、转换压力和有限对照资产，并进一步补充 strict seed 文献调研口径：seed 搜索不能局限于旧九个 direct baseline，但进入主 strict seed 的样本必须满足 `NL -> T0（无关键时间语义）FSM/HSM/EFSM/statechart` 且有生成 / 派生关系证据。这些台账仍只是**阶段性候选证据**：后续实证可能继续回填甚至局部修正当前链路。因此当前文档要优先保证边界清楚、事实可追踪、禁止 claim 不回流，而不是提前把最终论文论证写满。

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
7. [corpora/README.md](./corpora/README.md)：确认三类文库入口、README/GUIDE/SUMMARY 纪律、project-level 边界和 R2 读取链路。
8. [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md)：确认当前 seed library 的 `47/47`、`36 dirs`、旧九 `9/9` crosswalk、R2=4、manual queue 和 negative evidence；这是后续 R2 seed 冻结的当前入口。
9. [selected_seed_examples/README.md](./selected_seed_examples/README.md)：查看静态 smoke 用代表性 `<NL, STM_0>` 样例及其 R4.5 `model.fcstm` 派生快照；它只服务转换器 / 诊断器 / 修正循环的最小连通性自检，不是最终实验集合或主结果样本上限。
10. [conversion/README.md](./conversion/README.md)：查看 R3 开发 / 审计级 converter v0、schema、四例裁决报告和 loss ledger；若关注 R3.1 PlantUML 转换前规范化 / 恢复，还应继续读 [conversion/normalization/README.md](./conversion/normalization/README.md)、[conversion/normalization/GUIDE.md](./conversion/normalization/GUIDE.md)、[conversion/reports/plantuml_recovery_summary.md](./conversion/reports/plantuml_recovery_summary.md) 与 [conversion/artifacts/plantuml_recovery/r3_1_committed/README.md](./conversion/artifacts/plantuml_recovery/r3_1_committed/README.md)。conversion 层不是正式实验级转换器，R3.1 的恢复收益只属于 conversion eligibility，不属于 Better STM repair 收益。
11. [evaluation/README.md](./evaluation/README.md)：查看 R4 诊断 / 场景 / Better STM 评价门 v0、四例 dry-run fixture、schema 与 pytest contract。evaluation 层只冻结评价门草案，不调用真实 LLM、不执行 repair loop、不产生主实验结果。
12. [representation/README.md](./representation/README.md)：查看 R4.5 canonical STM JSON 到 `.fcstm` / pyfcstm inspect report 的表示桥；representation 层只服务 R5 deterministic smoke 的可机检输入，不把转换收益计入 repair gain。
13. [smoke/README.md](./smoke/README.md)：查看 R5 selected 四例 deterministic smoke 与 seed library 全量转换摸排；该层只做 pre-repair readiness audit、seed eligibility census 与 handoff，不执行 repair loop、不调用 LLM、不产生主实验结果。
14. [corpora/repair_baselines/SUMMARY.md](./corpora/repair_baselines/SUMMARY.md)：确认当前 STM repair baseline / 近邻结论；它不提供 R2 seed，只服务 related work、对照与消融边界。
15. [corpora/nl_datasets/SUMMARY.md](./corpora/nl_datasets/SUMMARY.md)：确认纯 NL 数据源入口；只有生成并记录 `STM_0` 后，生成后的 `<NL, STM_0>` 才能 crosslink 到 seed。
16. 需要追溯 PR-R1 generation-era 资产审计时，再读 [evidence/README.md](./evidence/README.md) 及其子文件；这些文件是历史审计入口，不替代当前三类 corpora 总账。
17. 需要追溯 R1.5--R1.7 旧 seed ledger / raw search 时，读 [archive/r1_5_to_r1_7_seed_corpus_snapshot/](./archive/r1_5_to_r1_7_seed_corpus_snapshot/)；archive 不作为当前事实真源。

## 3. 目录结构

```text
paper_stm_repair/
├── README.md
├── GUIDE.md
├── story/
├── experiment_design/
├── corpora/        # 当前三类论文级文库入口与事实总账读取链路
│   ├── seed_library/
│   ├── repair_baselines/
│   └── nl_datasets/
├── selected_seed_examples/  # smoke 用代表性 <NL, STM_0> + R4.5 .fcstm 快照；不是最终实验集合
├── conversion/     # R3 converter v0 + R3.1 PlantUML recovery eligibility audit；不是正式实验级转换器
├── evaluation/     # R4 诊断 / 场景 / Better STM 评价门 v0；只做 dry-run 与 schema contract
├── representation/ # R4.5 canonical JSON -> .fcstm / pyfcstm inspect 表示桥；不计 repair gain
├── smoke/         # R5 selected smoke + seed library sweep；pre-repair readiness audit，不跑 repair loop
├── seed_corpus/    # 旧入口 redirect；不再承载当前事实
├── evidence/       # PR-R1 generation-era 历史审计入口；不替代当前 corpora 总账
└── archive/        # R1.5--R1.7 旧 ledger / raw search 审计快照
```

## 4. 与旧目录 / 旧 PR 的关系

- 旧 [paper_v1/](../paper_v1/) 保留为 2026-05 Direction-Decision Sprint / Path-1 / Path-2 历史工作区；其旧 `NL -> STM` / hard comparison 叙事不再作为当前第一篇事实真源。
- 本工作区不拥有、不修改、不继承 PR [#93](https://github.com/HansBug/research_ideas/pull/93) 分支中的 `path1_foundation/` 路径；只参考其“入口 + story + evidence + experiment_design”等长期研究材料分层经验，不继承仓库内 PR 流程记录。
- PR [#94](https://github.com/HansBug/research_ideas/pull/94) / [#96](https://github.com/HansBug/research_ideas/pull/96) 已合入 #93 分支但未进入 `main`；其内容只能作为分支局部线索。
- 已合入 `main` 的 PR [#73](https://github.com/HansBug/research_ideas/pull/73)、[#82](https://github.com/HansBug/research_ideas/pull/82)、[#92](https://github.com/HansBug/research_ideas/pull/92) 是后续 PR-R1 baseline / seed 资产盘点线索。

## 5. R0 非目标

| 非目标 | 后续落点 |
|---|---|
| 逐篇 baseline 资产盘点、代码 / artifact 可获取性台账 | 后续资产整理 |
| seed registry 与最终实验样本冻结 | 后续样本整理；当前 [selected_seed_examples/](./selected_seed_examples/) 只保存 smoke 用代表性静态样例及 R4.5 `.fcstm` 派生快照 |
| 多格式转换器 schema / fixture / 归因实现 | [conversion/](./conversion/) 已提供 R3 开发 / 审计级 converter v0，并在 R3.1 下补充 PlantUML 转换前规范化 / 恢复 eligibility audit；[representation/](./representation/) 提供 R4.5 `.fcstm` 表示桥；[smoke/](./smoke/) 提供 R5 readiness audit 与 seed sweep；正式实验级转换仍待 R7/R8 冻结 |
| 诊断、场景、评价量表 v0 与统计表骨架冻结 | [evaluation/](./evaluation/) 已提供 R4 v0；正式 protocol 仍待 R7 冻结 |
| 无人化修正循环 runtime / prompt / LLM 调用 | 后续 runtime 整理 |
| 主实验协议、对照矩阵、端到端四例预演 | [smoke/](./smoke/) 已完成 pre-repair selected 四例 smoke 与 seed sweep；正式 repair loop / 主实验仍待后续 R6-R8 |
| 完整论文正文 / submission package | 后续正文整理 |

## 6. 上游正式记录

- PR #100 第一篇新伞 PR：<https://github.com/HansBug/research_ideas/pull/100>
- PR #99 会后定调 comment：<https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818>
- 正式导师讨论记录：[2026-06-12-导师-两篇论文转向与模型修正定调.md](../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md)
- project_1 导师讨论总账：[talks/SUMMARY.md](../talks/SUMMARY.md)

## 7. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-28 14:20:00 | 新增 [smoke/](./smoke/) R5 pre-repair readiness audit 入口，落地 selected 四例 smoke、seed library sweep、archive/index/manifest、handoff 三件套与 CLI contract；R5 不执行 repair loop、不调用 LLM、不计主实验结果。 |
| 2026-06-28 00:26:00 | [selected_seed_examples/](./selected_seed_examples/) 补齐四例 R4.5 `model.fcstm` 派生快照与 `fcstm_meta.json`，并明确该目录是 smoke 迷你文库，不是 seed registry 或最终实验集合；`.fcstm` 只同步自 [representation/](./representation/) reports，不计 repair gain。 |
| 2026-06-27 01:20:00 | PR-R4.5 新增 [representation/](./representation/) 表示桥工作区，落地 canonical STM JSON 到 `.fcstm` / pyfcstm inspect report 的 exporter、schema、loss ledger 与 pytest contract；R4.5 只服务 R5 deterministic smoke，不计 repair gain。 |
| 2026-06-26 12:35:00 | PR-R4 新增 [evaluation/](./evaluation/) 评价门工作区，落地 diagnostic / scenario / Better STM checklist / eligibility / human rubric schema、四例 dry-run fixture 与 pytest contract；R4 只做 gate dry-run，不产生 repair 或主实验结果。 |
| 2026-06-25 23:55:00 | PR-R3.1 在 [conversion/](./conversion/) 下新增 PlantUML 转换前规范化 / 恢复入口、source-level semantic preservation gate 与高基数制品归档；全量 raw / normalized `.puml` 与官方 `.scxml` 只以 [workdir.zip](./conversion/artifacts/plantuml_recovery/r3_1_committed/workdir.zip) 保存，论文主 claim 只能引用 low-risk / main eligibility 口径。 |
| 2026-06-24 17:45:00 | PR-R3 新增 [conversion/](./conversion/) 开发 / 审计级 converter v0，落地四例 smoke 转换裁决、schema、toolchain survey、canonical report 与 loss ledger；正式实验级转换仍待 R7/R8 冻结。 |
| 2026-06-24 10:25:00 | 将 smoke 用代表性样例迁至 [selected_seed_examples/](./selected_seed_examples/) 根路径，明确其不是最终实验集合，并在顶层入口中加入读取指引。 |
| 2026-06-16 23:08:00 | PR-R1.8-E 收敛三类文库总账一致性：R2 当前 seed 入口统一为 [corpora/seed_library/SUMMARY.md](./corpora/seed_library/SUMMARY.md)，旧 [seed_corpus/](./seed_corpus/) 与 [evidence/](./evidence/) 降级为 redirect / 历史审计入口，并将 seed 哨兵统一为 `36 dirs`。 |
| 2026-06-14 17:55:00 | PR-R1.8-B 将旧 `seed_corpus/` 迁移为 [corpora/seed_library/](./corpora/seed_library/) SUMMARY-first 三件套，并归档 R1.5--R1.7 旧 ledger / raw search。 |
| 2026-06-14 00:16:15 | PR-R1 补充 strict seed 大规模文献调研口径、排除码、多维指标、分级标准与执行方案，明确不局限旧 direct baseline 且不把宽口径 `<NL, STM>` 共现误作 strict seed。 |
| 2026-06-13 00:45:00 | PR-R1 新增 baseline 资产审计、候选矩阵、artifact 可获取性、格式转换压力、分支局部资产追踪与 source coverage ledger。 |
| 2026-06-12 23:42:20 | 初始化 PR-R0 新工作区，冻结 `<NL, STM_0> -> STM_k / Better STM` 主线、路径结构与后续子 PR 接口。 |
