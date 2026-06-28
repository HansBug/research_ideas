# 第二篇论文：智能体辅助系统综述工作区

## 1. 定位

本目录是第二篇论文的工作区，主题是：**面向软件工程系统综述（Systematic Literature Review, SLR）/ 系统映射研究（Systematic Mapping Study, SMS）的审计优先证据工程方法：研究者引导的维度模式演化与发现裁决**。

本工作区不收录 PDF，不替代 `sources/` 文库，也不把语料规模作为论文贡献。它的作用是沉淀论文主线、术语、主张边界、证据来源、基线威胁、候选场景、评价义务和后续 PR 计划。后续任何实现、实验、写作或相关工作补充，都应先回到本目录确认当前合同。

## 2. 当前 PR-S0-v2 结论

PR-S0-v2 将第二篇论文主线收紧为以下口径：

1. 第二篇不再写成 `sources/` 语料 / 基准来源全景论文，也不写成“大语言模型（Large Language Model, LLM）/ 智能体（agent）自动化综述生成”。
2. 当前安全主线是：**面向软件工程系统综述 / 系统映射研究的审计优先证据工程方法**。首次出现的中英文术语以 [story/paper_story.md](./story/paper_story.md) §2 和 [story/terminology_policy.md](./story/terminology_policy.md) 为准；后续正文一律优先使用中文术语。研究者定义主题、研究问题、范围和综述元模型；方法把综述元模型投影为可版本化、可修订、可回填的维度模式；智能体只在研究者批准的维度模式下辅助论文收集、字段级证据抽取、统计分析和候选发现生成；最终领域发现必须由研究者裁决；全过程导出可审计制品链和过程证据。
3. 真实系统综述实践被显式拆成三层：论文收集与初步处理、维度模式驱动的论文分析、统计分析与研究发现形成。
4. 维度模式是一等制品，必须可版本化、可修订、可记录影响分析与回填状态；不能写成一次性平铺字段表。
5. 统计分析只产生统计观察；进入研究发现前必须经过发现启发式、内容证据、反向证据、主张强度控制与研究者质疑 / 裁决。
6. 内容证据支撑字段值、统计分析和领域发现；过程证据只支撑方法发现，如方法可用性、审计性、成本和失败模式。
7. 综述之综述脚手架只作为模式先验；不得写成目标证据池、完整三级综述或 PRISMA 透明报告框架（Preferred Reporting Items for Systematic Reviews and Meta-Analyses, PRISMA）合规三级综述。
8. 试运行只验证闭环可行性与制品完整性；后续硕士生人机交互数据只用于方法评估，并需同意、匿名化、脱敏与教学关系隔离。
9. PR-S0-v2 不实现运行时代码，不跑真实大语言模型，不跑四个真实例子，不冻结最终指标公式；这些分别留给后续设计、试运行、真实运行、评价和相关工作。
10. 后续若新增基线、脚手架、真实运行或评价结果，必须同步更新 [story/paper_story.md](./story/paper_story.md)、[story/paper_outline.md](./story/paper_outline.md)、[story/claim_evidence_map.md](./story/claim_evidence_map.md) 与 [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)。

11. 为避免主线停留在“强协议 / 弱证据”，当前 PR 进一步要求后续 A2/A3/A5 至少实例化一组审计制品链：维度模式与修订 / 回填日志、字段级内容证据表、候选发现台账、质疑 / 裁决 / 未解决日志和过程证据包；并用 LLM4STM / LLM4Modeling 的 3--5 篇种子论文完成最小闭环样例。

## 3. 目录分层

| 子路径 | 作用 | 入口 |
|---|---|---|
| [story/](./story/) | 论文主线、术语、主张-证据映射、差异化新颖性和章节架构 | [story/README.md](./story/README.md) |
| [evidence/](./evidence/) | 仓库证据资产、事实漂移政策、引用种子与证据层级 | [evidence/README.md](./evidence/README.md) |
| [baselines/](./baselines/) | 自动化综述、大语言模型辅助系统综述、综述生成等近邻工作对照入口 | [baselines/README.md](./baselines/README.md) |
| [dataset_selection/](./dataset_selection/) | 候选场景与证据资产选择入口；不冻结最终基准 | [dataset_selection/README.md](./dataset_selection/README.md) |
| [experiment_design/](./experiment_design/) | 评价维度种子和审稿风险登记；不冻结 A5 指标公式 | [experiment_design/README.md](./experiment_design/README.md) |
| [plan/](./plan/) | 当前任务包、进度、验证命令与能力使用审计 | [plan/README.md](./plan/README.md) |

## 4. 推荐阅读顺序

1. [story/paper_story.md](./story/paper_story.md)：理解论文核心论点、任务边界、方法阶段、候选贡献和禁用主张。
2. [story/terminology_policy.md](./story/terminology_policy.md)：确认维度模式、内容证据 / 过程证据、统计分析、候选发现 / 最终发现、G0--G6 等术语边界。
3. [story/claim_evidence_map.md](./story/claim_evidence_map.md)：写摘要、引言、贡献或 PR 评论 前必须检查。
4. [story/differential_novelty_matrix.md](./story/differential_novelty_matrix.md)：确认与 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等近邻的边界。
5. [baselines/SUMMARY.md](./baselines/SUMMARY.md)：查看已核验近邻与 B0 基线结论。
6. [evidence/fact_drift_policy.md](./evidence/fact_drift_policy.md)：引用 PR #97、`sources/` 或历史评论 前必须检查。
7. [experiment_design/evaluation_dimensions_seed.md](./experiment_design/evaluation_dimensions_seed.md)：理解 PR-S0-v2 只冻结哪些评价义务。
8. [experiment_design/reviewer_risk_register.md](./experiment_design/reviewer_risk_register.md)：查看当前最高优先级审稿风险。
9. [plan/progress.md](./plan/progress.md)：查看本 PR 当前状态、检查和剩余风险。

## 5. 文档卫生要求

本目录当前阶段的 Markdown 应尽量作为可独立阅读的当前合同，而不是历史 PR 流水账：

1. 保留必要事实源链接、PR 编号、commit 或路径，但不要把审查过程、旧计划分歧和已修复问题堆成正文。
2. 每个入口文件都应能说明“当前结论是什么、该读哪里、禁止误用什么”，避免读者必须翻旧评论才能理解主线。
3. 若历史信息会影响当前判断，应压缩为证据来源或风险条目；若只反映已过期过程，应移出当前正文或只留在 PR 评论。
4. 中文为主，必要英文只保留为术语锚点、论文 / 工具名、路径、命令或代码标识。

## 6. 非目标与禁止主张

本目录当前阶段不做：

1. 不实现智能体工作流、管线或运行时代码。
2. 不跑真实大语言模型；后续真实运行必须先 `source .env` 并保存运行记录。
3. 不跑四个真实例子；真实场景设计留给 PR-A3。
4. 不复制 PR #97 的 PDF / 全文文库。
5. 不写完整英文论文稿，不生成最终 LaTeX，不冻结最终投稿目标。

禁止写成以下主张：端到端无人自动系统综述、智能体替代专家、PRISMA 透明报告框架合规、完整覆盖、首次自动化系统综述、首次智能体式系统综述、大语言模型自动定义可靠综述元模型、统计分析直接等于最终发现、过程证据支撑领域发现、脚手架是目标证据池、试运行证明泛化。
