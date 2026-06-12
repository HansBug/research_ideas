# Project Inventory：agent-based SLR 证据资产盘点

## 1. Repository Map

| 路径 / 入口 | 证据层级 | 当前角色 | 使用规则 |
|---|---|---|---|
| [../README.md](../README.md) | A0 工作区入口 | 第二篇 paper workspace 总入口。 | 后续 agent 先读。 |
| [../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md](../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | T0 `main` fact | 正式导师讨论记录，冻结第二篇转向 agent-based SLR。 | 高优先级事实源。 |
| PR [#101](https://github.com/HansBug/research_ideas/pull/101) | 上游伞 PR | 第二篇新主线 umbrella contract。 | 子 PR 需与之对齐。 |
| PR [#103](https://github.com/HansBug/research_ideas/pull/103) | 当前 A0 PR | 主线与协议冻结。 | 当前工作入口。 |
| [../../sources/](../../sources/) | T0 `main` fact / 待复核 | 控制系统 STM domain scenario 候选。 | A1 需复核当前 `SUMMARY.md` 和资产状态。 |
| PR [#97](https://github.com/HansBug/research_ideas/pull/97) | T1 PR #97 snapshot fact | related-work screening / fulltext extraction case 候选。 | 必须按 [fact_drift_policy.md](./fact_drift_policy.md) 引用。 |
| issue [#85](https://github.com/HansBug/research_ideas/issues/85) | T2 historical comment / planning | 旧 corpus / benchmark-source landscape 规划与后续转向背景。 | 不能作为完成事实。 |

## 2. Method Evidence

A0 阶段尚未实现 agent-based SLR pipeline。后续方法证据预计来自：

| 未来证据 | 当前状态 | 后续 PR |
|---|---|---|
| workflow schema | 待构造 | A2 |
| stage input/output contract | 待构造 | A2 |
| agent execution skeleton | 待构造 | A4 |
| evidence package writer | 待构造 | A4 |
| run record / redaction report | 待构造 | A4/A5 |

## 3. Experiment Evidence

A0 不跑真实例子，也不运行真实 LLM。

| 未来证据 | 当前状态 | 后续 PR |
|---|---|---|
| 回顾型 replay 场景 | 待设计 | A3 |
| 前瞻型 execution 场景 | 待设计 | A3 |
| gold / silver facts | 待构造 | A3 |
| trap papers / 易混淆论文集 | 待构造 | A3 |
| pilot run evidence package | 待运行 | A4/A5 |
| traceability / hallucination / cost 指标 | 待冻结 | A5 |

## 4. Writing Assets

| 文件 | 当前状态 | 用途 |
|---|---|---|
| [../story/paper_story.md](../story/paper_story.md) | 已创建 | story 真源。 |
| [../story/protocol.md](../story/protocol.md) | 已创建 | workflow protocol 真源。 |
| [../story/claim_evidence_map.md](../story/claim_evidence_map.md) | 已创建 | claim gate。 |
| [../story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md) | 已创建 | related-work boundary。 |
| [../story/paper_outline.md](../story/paper_outline.md) | 已创建 | manuscript section 入口。 |

## 5. Citation Assets

当前 citation seed 入口见 [citation_seed_inventory.md](./citation_seed_inventory.md)。A0 不生成最终 `references.bib`；后续写 Related Work 前必须从 DOI、出版页、DBLP、arXiv、官方工具文档等 authoritative source 获取 BibTeX。

## 6. Missing Inputs

| 缺口 | 影响 | 后续处理 |
|---|---|---|
| 完整 related-work corpus | novelty 不可最终确认 | A1 / related-work PR。 |
| PR #97 merge 或 snapshot 冻结 | 资产当前性不稳 | A1 按 fact drift policy 处理。 |
| benchmark scenarios | 无法支撑实证 claim | A3。 |
| gold / silver facts | 无法评价 factuality / hallucination | A3。 |
| 真实 run records | 无法报告 cost / error / audit rate | A4/A5。 |
| A5 指标公式 | 无法写结果 | A5。 |
