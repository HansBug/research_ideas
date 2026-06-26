# 第二篇论文：智能体辅助 SLR 工作区

## 1. 定位

本目录是第二篇论文的工作区，主题是：**面向软件工程系统综述 / 系统映射研究（SLR/SMS）的研究者引导、模式演化、证据支撑、发现导向的智能体式支持方法**。

本工作区不收录 PDF，不替代 `sources/` 文库，也不把语料规模作为论文贡献。它的作用是沉淀论文主线、术语、主张边界、证据来源、基线威胁、候选场景、评价义务和后续 PR 计划。后续任何实现、实验、写作或相关工作补充，都应先回到本目录确认当前合同。

## 2. 当前 PR-S0-v2 结论

PR-S0-v2 将第二篇论文主线收紧为以下口径：

1. 第二篇不再写成 `sources/` 语料 / 基准来源全景论文，也不写成“LLM / agent 自动化综述生成”。
2. 当前安全主线是：**researcher-guided、pattern-evolving、evidence-backed、finding-oriented agentic SLR support approach**。研究者定义 topic / RQ / scope / meta-model，agent 只在研究者批准的 dimension schema 下辅助论文收集、字段级证据抽取、统计分析和 candidate finding signal 生成，final target-domain findings 必须由研究者裁决。
3. 真实 SLR 实践被显式拆成三层：论文收集与初步处理、维度 pattern 驱动的论文分析、统计分析与 research finding 形成。
4. `dimension pattern / extraction schema` 是一等制品，必须可版本化、可修订、可记录 impact analysis 与 backfill 状态；不能写成一次性平铺字段表。
5. `statistical analysis` 只产生统计观察；进入 research finding 前必须经过 finding heuristic、content evidence、counter-evidence、claim strength 控制与 researcher challenge / adjudication。
6. `content evidence` 支撑字段值、统计分析和 target-domain findings；`process evidence` 只支撑 method-evaluation findings，如方法可用性、审计性、成本和失败模式。
7. `survey-of-surveys` 只作为 scaffold mining / pattern prior；不得写成目标 evidence pool、complete tertiary review 或 PRISMA-compliant tertiary review。
8. pilot run 只验证 closure / feasibility / artifact completeness；后续硕士生 human-LLM interaction data 只用于 method evaluation，并需 consent、匿名化、脱敏与教学关系隔离。
9. PR-S0-v2 不实现运行时代码，不跑真实 LLM，不跑四个真实例子，不冻结最终指标公式；这些分别留给后续 A2/A3/A4/A5/A6。
10. 后续若新增基线、脚手架、真实运行或评价结果，必须同步更新 [story/paper_story.md](./story/paper_story.md)、[story/paper_outline.md](./story/paper_outline.md)、[story/claim_evidence_map.md](./story/claim_evidence_map.md) 与 [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文主线、术语、主张-证据映射、差异化新颖性和章节架构 | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、事实漂移政策、引用种子与证据层级 | [evidence/README.md](./evidence/README.md) |
| [baselines/](./baselines/) | 自动化综述、LLM 辅助 SLR、综述生成等近邻工作对照入口 | [baselines/README.md](./baselines/README.md) |
| [dataset_selection/](./dataset_selection/) | 候选场景与证据资产选择入口；不冻结最终基准 | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | 评价维度种子和审稿风险登记；不冻结 A5 指标公式 | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前任务包、进度、验证命令与能力使用审计 | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

1. [story/paper_story.md](./story/paper_story.md)：理解论文核心论点、任务边界、方法阶段、候选贡献和禁用主张。
2. [story/terminology_policy.md](./story/terminology_policy.md)：确认 dimension pattern、content/process evidence、statistical analysis、candidate/final finding、G0--G6 等术语边界。
3. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：写摘要、引言、贡献或 PR comment 前必须检查。
4. [story/differential_novelty_matrix.md](./story/differential_novelty_matrix.md)：确认与 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等近邻的边界。
5. [baselines/SUMMARY.md](./baselines/SUMMARY.md)：查看已核验近邻与 B0 基线结论。
6. [evidence/fact_drift_policy.md](./evidence/fact_drift_policy.md)：引用 PR #97、`sources/` 或历史 comment 前必须检查。
7. [experiment_design/evaluation_dimensions_seed.md](./experiment_design/evaluation_dimensions_seed.md)：理解 PR-S0-v2 只冻结哪些评价义务。
8. [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)：查看当前最高优先级审稿风险。
9. [plan/progress.md](./plan/progress.md)：查看本 PR 当前状态、检查和剩余风险。

## 5. 文档卫生要求

本目录当前阶段的 Markdown 应尽量作为可独立阅读的当前合同，而不是历史 PR 流水账：

1. 保留必要事实源链接、PR 编号、commit 或路径，但不要把 review 过程、旧计划分歧和已修复问题堆成正文。
2. 每个入口文件都应能说明“当前结论是什么、该读哪里、禁止误用什么”，避免读者必须翻旧 comment 才能理解主线。
3. 若历史信息会影响当前判断，应压缩为证据来源或风险条目；若只反映已过期过程，应移出当前正文或只留在 PR comment。
4. 中文为主，必要英文只保留为术语锚点、论文 / 工具名、路径、命令或代码标识。

## 6. 非目标与禁止主张

本目录当前阶段不做：

1. 不实现智能体工作流、管线或运行时代码。
2. 不跑真实 LLM；后续真实运行必须先 `source .env` 并保存运行记录。
3. 不跑四个真实例子；真实场景设计留给 PR-A3。
4. 不复制 PR #97 的 PDF / 全文文库。
5. 不写完整英文论文稿，不生成最终 LaTeX，不冻结最终投稿 venue。

禁止写成以下主张：端到端无人自动 SLR、智能体替代专家、PRISMA 合规、完整覆盖、首次自动化 SLR、首次智能体式 SLR、LLM 自动定义可靠元模型、统计分析直接等于 final finding、process evidence 支撑 target-domain finding、survey-of-surveys 是目标 evidence pool、pilot 证明泛化。
