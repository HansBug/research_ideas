# 第二篇论文：agent-based SLR 工作区

## 1. 定位

本目录是第二篇论文 **agent-based SLR / systematic mapping 方法学论文** 的工作区。它接续伞 PR [#101](https://github.com/HansBug/research_ideas/pull/101) 与 PR-0 / PR-A0 [#103](https://github.com/HansBug/research_ideas/pull/103)，用于把 2026-06-12 导师讨论后的第二篇新主线落成可维护、可审计、可继续迭代的 paper planning / evidence workspace。

本目录不是传统论文集，不收录 PDF，也不是 `sources/` 文库的替代入口。它的目标是服务一篇方法学论文：研究如何将软件工程系统文献综述 / systematic mapping 的检索、筛选、全文获取状态记录、抽取、编码、综合与报告环节组织成带 human audit gates 的 agent-executed workflow，并用可追踪性、事实准确性、幻觉控制、筛选一致性、透明报告、覆盖代理、成本效率和人工审计通过率评价其可靠性。

## 2. 当前 A0 结论

A0 阶段冻结以下口径：

1. 第二篇不再写成 `project_1_llm_state_machine_modeling/sources/` corpus / benchmark-source landscape paper。
2. `sources/`、PR [#97](https://github.com/HansBug/research_ideas/pull/97) 与 issue [#85](https://github.com/HansBug/research_ideas/issues/85) 的资产只作为 case study、benchmark scenario、evidence package 或 stress test 候选。
3. PR #97 当前仍为 OPEN / 未合入，其 438→69→25 与 25 篇全文文库只能作为 **PR #97 snapshot / 分支局部证据** 使用，不能写成 `main` fact。
4. A0 只冻结 story、协议、术语、claim 边界、事实漂移政策、相关工作边界、评价维度种子和 reviewer 风险；不跑真实 LLM，不跑四个真实例子，不实现 pipeline。
5. A0 不冻结评价指标公式、阈值、统计协议或最终评价脚本；这些留给 PR-A5。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文 thesis、协议、术语、claim-evidence map、差异化 novelty 和章节架构 | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、PR #97 事实漂移政策、citation seed、已核验引用种子与证据层级 | [evidence/README.md](./evidence/README.md) |
| [baselines/](./baselines/) | 自动化综述、SLR/SMS 方法学、ASReview、RobotReviewer、LLM-assisted SLR 等相关工作对照入口 | [baselines/README.md](./baselines/README.md) |
| [dataset_selection/](./dataset_selection/) | A0 候选场景与证据资产选择入口；不冻结 benchmark scenarios | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | A0 评价维度种子和 reviewer 风险登记；不冻结 A5 指标公式 | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前 PR task packet、进度、验证命令与 capability-use audit | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

后续 agent / 人类进入本目录时，建议按以下顺序阅读：

1. [story/paper_story.md](./story/paper_story.md)：理解论文主张、任务边界、gap、贡献边界和 reviewer risks。
2. [story/terminology_policy.md](./story/terminology_policy.md)：确认 SLR、systematic mapping、agent、audit gate、PRISMA-style、traceability、hallucination 等术语口径。
3. [story/protocol.md](./story/protocol.md)：理解 agent-based SLR workflow 与 human audit gates。
4. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：写任何 abstract / introduction / contribution 前必须检查。
5. [story/differential_novelty_matrix.md](./story/differential_novelty_matrix.md)：确认与 SLR/SMS、PRISMA、ASReview、RobotReviewer、review automation 和 LLM-assisted evidence synthesis 的边界。
6. [baselines/SUMMARY.md](./baselines/SUMMARY.md)：查看 A0 已核验 related-work 锚点和 A1 待补近邻。
7. [dataset_selection/sample_assets.md](./dataset_selection/sample_assets.md)：查看 A0 候选场景和证据资产，但不要把它们当成已冻结 benchmark。
8. [evidence/fact_drift_policy.md](./evidence/fact_drift_policy.md)：引用 PR #97、`sources/` 或 historical comments 前必须检查。
9. [evidence/project_inventory.md](./evidence/project_inventory.md)：查看当前可用证据、待构造证据和资产角色。
10. [experiment_design/evaluation_dimensions_seed.md](./experiment_design/evaluation_dimensions_seed.md)：理解 A0 只冻结哪些评价维度种子。
11. [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)：查看当前审稿风险和缓解入口。
12. [plan/progress.md](./plan/progress.md)：查看当前 PR 进度、检查和剩余风险。

## 5. 非目标

本目录 A0 阶段不做：

1. 不实现 agent workflow / pipeline / runtime code。
2. 不跑真实 LLM；后续真实运行必须先 `source .env`。
3. 不跑四个真实例子；真实场景设计留给 PR-A3。
4. 不复制 PR #97 的 PDF / fulltext 文库。
5. 禁止声称 PRISMA-compliant、complete coverage、first automated SLR 或 agent 替代专家。
6. 不写完整英文 manuscript，不生成最终 LaTeX，不冻结最终投稿 venue。

## 6. 当前验收标准

- [x] 路径不使用 `foundation/` 子目录层。
- [x] `story/`、`evidence/`、`experiment_design/`、`plan/` 四个入口齐全。
- [x] A0 核心文件可解释论文 story、术语、协议、claim 边界、事实漂移和风险登记。
- [x] PR #97 被标注为 OPEN / 未合入 / snapshot / 分支局部证据。
- [x] A0 不跑真实 LLM、不跑四个真实例子、不冻结 A5 指标公式。
