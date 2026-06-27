# 证据资产盘点：智能体辅助系统综述论文

## 1. 作用

本文件盘点第二篇论文当前可用、待复核和计划构造的证据入口。它不是历史 PR 流水账；只保留会影响 PR-S0-v2 论文主线、后续 A2/A3/A5/A6 设计或事实当前性的证据资产。

当前最高优先级口径：第二篇论文主线已由 PR-S0-v2 收紧为**研究者引导、模式演化、证据支撑、发现导向的智能体式系统综述 / 系统映射研究支持方法**。引用任何旧 A0 / B0 / PR #97 / issue #85 信息时，都必须先判断其证据层级和当前状态。

## 2. 当前核心入口

| 路径 / 入口 | 证据层级 | 当前角色 | 使用规则 |
|---|---|---|---|
| [../README.md](../README.md) | 当前工作区入口 | 第二篇论文工作区总入口。 | 后续智能体先读。 |
| [../story/paper_story.md](../story/paper_story.md) | PR-S0-v2 论文主线真源 | 当前论文主线、方法图、候选贡献与禁止主张。 | 写摘要、引言、方法或 PR 评论 前必须检查。 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | PR-S0-v2 主张审查门 | 区分可写、待补证、禁止和快照依赖主张。 | 强主张必须回到本表。 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | PR-S0-v2 新颖性边界 | 对齐 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等强近邻。 | 相关工作和贡献写作必须引用。 |
| [../story/terminology_policy.md](../story/terminology_policy.md) | PR-S0-v2 术语政策 | 固定维度模式、内容证据 / 过程证据、统计分析、候选发现 / 最终发现、G0--G6、类 PRISMA 等术语。 | 防止术语漂移。 |
| [../plan/progress.md](../plan/progress.md) | 当前 PR 进度 | 记录本 PR 最新状态、验证和剩余风险。 | 只作为进度入口，不替代 论文主线真源。 |

## 3. 上游事实源

| 来源 | 当前状态 | 对本文的作用 | 注意事项 |
|---|---|---|---|
| PR [#101](https://github.com/HansBug/research_ideas/pull/101) | 上游伞 PR | 第二篇论文上游合同、子 PR 依赖与进度同步目标。 | 当前 PR 必须与其 body 进度保持一致。 |
| PR-A0 / PR [#103](https://github.com/HansBug/research_ideas/pull/103) | 已合入上游的历史输入 | 提供早期目录结构、初始 story 与协议雏形。 | 不能再写成“当前 A0 PR”；当前 story 以 PR-S0-v2 为准。 |
| PR-B0 / PR [#105](https://github.com/HansBug/research_ideas/pull/105) | 已合入上游的基线调研 | 提供 35 篇全文文本级近邻 review 与“宽泛自动化叙事被击穿”的证据。 | 作为新颖性降级和强近邻清单的核心证据。 |
| PR-S0-pre / PR [#112](https://github.com/HansBug/research_ideas/pull/112) | 已合入上游的导师讨论 PR | 提供“元模型由使用者定义、SLR 要形成研究发现、研究者可质疑证据”的定调。 | PR-S0-pre 的最高优先级导师约束之一。 |
| PR-S0B / PR [#123](https://github.com/HansBug/research_ideas/pull/123) | 已合入上游的导师讨论 PR | 提供三阶段 SLR、维度模式、统计分析 / 研究发现分层、人在回路方法、试运行与过程数据约束。 | PR-S0-v2 的最高优先级导师约束之一。 |
| [2026-06-26 导师讨论记录](../../talks/2026-06-26-导师-三阶段SLR与human-in-the-loop-finding.md) | 已合入上游分支的正式导师记录 | 固定 研究者引导、模式演化、证据支撑、发现导向主线。 | 与旧 A0/S0 文档冲突时，以该记录和 PR-S0-v2 文档为准。 |
| [2026-06-15 导师讨论记录](../../talks/2026-06-15-导师-PR112-发现导向SLR与meta-model边界.md) | 已合入上游分支的正式导师记录 | 固定 研究者定义综述元模型、发现导向系统综述与研究者质疑闭环方向。 | 与旧 A0 文档冲突时，以该记录和 PR-S0-v2 文档为准。 |
| [2026-06-12 导师讨论记录](../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | `main` / 上游可复查导师记录 | 提供从旧第二篇方向转向 智能体式系统综述背景。 | 只作历史背景，不替代 2026-06-15 定调。 |

## 4. 数据与场景资产

| 资产 | 证据层级 | 当前角色 | 使用规则 |
|---|---|---|---|
| [../../sources/](../../sources/) | `main` 已有资产 / 待按最新总账复核 | 控制系统 STM 领域场景、压力测试或证据来源候选。 | 可作为 A3 场景线索；不能把语料规模写成第二篇主贡献。 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | OPEN / 未合入 / 快照 / 分支局部证据 | 相关工作筛选、全文抽取和候选案例线索。 | 必须按 [fact_drift_policy.md](./fact_drift_policy.md) 引用；不能写成 `main` 事实。 |
| issue [#85](https://github.com/HansBug/research_ideas/issues/85) | 历史讨论 / 规划线索 | 旧 corpus / benchmark-source landscape 规划与转向背景。 | 不能替代仓库文件、PR body 或可复验数据。 |
| [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md) | PR-S0-v2 候选资产总账 | 汇总后续 A3 可用场景和前置要求。 | 不冻结最终 benchmark。 |

## 5. 方法证据状态

PR-S0-v2 阶段尚未实现 智能体式系统综述运行时；当前只冻结 story、术语、维度模式生命周期、证据边界和后续评价义务。

| 未来证据 | 当前状态 | 后续 PR |
|---|---|---|
| 综述元模型 / 维度模式阶段契约 | 待构造 | A2 |
| 模式修订 / 影响分析 / 回填日志 | 待构造 | A2/A5 |
| 候选发现台账与最终裁决状态机 | 待构造 | A2/A5 |
| 智能体执行骨架 | 待构造 | A4 |
| 字段证据表 / 模式修订日志 / 候选发现台账 / 透明材料写出器 | 待构造 | A4 |
| 运行记录 / 脱敏报告 | 待构造 | A4/A5 |

## 6. 实验证据状态

PR-S0-v2 不跑真实例子，也不运行真实大语言模型。

| 未来证据 | 当前状态 | 后续 PR |
|---|---|---|
| 回放型场景 | 待设计 | A3 |
| 前瞻型场景 | 待设计 | A3 |
| 金事实 / 银事实 | 待构造 | A3 |
| 陷阱论文 / 易混淆论文集 | 待构造 | A3 |
| 试运行制品与运行记录 | 待运行 | A4/A5 |
| 内容证据 / 统计正确性 / 质疑结果 / 过程数据指标 | 待冻结 | A5 |

## 7. 写作资产

| 文件 | 当前状态 | 用途 |
|---|---|---|
| [../story/paper_story.md](../story/paper_story.md) | PR-S0-v2 已重写 | 论文主线真源、方法图、贡献边界。 |
| [../story/protocol.md](../story/protocol.md) | PR-S0-v2 已重写 | 模式演化、字段证据、统计观察、finding challenge 与 G0--G6 gate 的最小协议。 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | PR-S0-v2 已重写 | 主张审查门。 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | PR-S0-v2 已重写 | 相关工作边界。 |
| [../story/paper_outline.md](../story/paper_outline.md) | PR-S0-v2 已重写 | 后续论文结构和 RQ 映射。 |

## 8. 引用资产

当前引用种子入口见 [citation_seed_inventory.md](./citation_seed_inventory.md)。PR-S0-v2 不生成最终 `references.bib`；后续写 相关工作 前必须从 DOI、出版页、DBLP、arXiv、官方工具文档等 权威来源 获取 BibTeX。

## 9. 缺口

| 缺口 | 影响 | 后续处理 |
|---|---|---|
| 完整相关工作语料 | 新颖性不可最终确认 | A1 / A6 / 相关工作 PR。 |
| PR #97 合并或快照复核 | 资产当前性不稳 | 按 [fact_drift_policy.md](./fact_drift_policy.md) 处理。 |
| 基准场景 | 无法支撑实证主张 | A3。 |
| 金事实 / 银事实 | 无法评价事实准确性 / 幻觉 | A3。 |
| 真实运行记录 | 无法报告成本、错误和审计率 | A4/A5。 |
| A5 指标公式 | 无法写结果 | A5。 |
