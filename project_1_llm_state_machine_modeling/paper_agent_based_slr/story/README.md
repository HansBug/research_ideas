# story/：论文主线、协议、术语与主张控制

本目录维护第二篇 researcher-guided agentic SLR support workflow 论文的 story 真源。PR-S0 后，它回答：这篇论文如何从宽泛“自动化 SLR / evidence package workflow”收紧为 研究者定义的 meta-model、finding patterns（研究发现模式）、candidate / final finding（候选 / 最终研究发现） lifecycle、evidence challenge loop（证据质疑闭环） 与 finding-centered evaluation（以研究发现为中心的评价）；哪些术语如何使用，哪些 claim 可以写，哪些 claim 必须避免，与已有工具和方法学如何区分。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | PR-S0 后的核心论点、任务边界、问题缺口、技术挑战、方法洞察、以研究发现为中心的候选贡献、证据计划和审稿风险。 |
| [protocol.md](./protocol.md) | 智能体辅助 SLR / systematic mapping 的最小工作流协议与人工审计门。 |
| [terminology_policy.md](./terminology_policy.md) | SLR、systematic mapping、agent、audit gate、PRISMA-style、traceability、hallucination 等术语口径。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每类潜在主张的证据状态、禁止写法、安全写法和后续所需证据。 |
| [differential_novelty_matrix.md](./differential_novelty_matrix.md) | 与 SLR/SMS、PRISMA、ASReview、RobotReviewer、review automation、LLM-assisted evidence synthesis 的差异化新颖性矩阵。 |
| [paper_outline.md](./paper_outline.md) | 面向后续 论文稿 的 章节级架构，正文说明以中文为主。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认主线是带人工审计门的智能体辅助 SLR 方法学，而不是 `sources/` corpus paper。
2. 再读 [terminology_policy.md](./terminology_policy.md)，避免 PRISMA、audit、traceability、hallucination 等术语漂移；这些英文保留为术语锚点。
3. 写任何 protocol 或方法 描述前读 [protocol.md](./protocol.md)。
4. 写任何 摘要 / 贡献 / 结论 句子前必须查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 写 相关工作 前读 [differential_novelty_matrix.md](./differential_novelty_matrix.md)。
6. 组织论文大纲时读 [paper_outline.md](./paper_outline.md)。

## A0 硬约束

- 不把第二篇写成 `sources/` corpus / mapping / dataset paper。
- 禁止写 智能体完全替代 SLR 专家。
- 不写端到端无人自动产出合格 SLR。
- 禁止在 checklist 未闭合前写 PRISMA-compliant。
- 禁止写 complete coverage 或 first automated SLR。
- 不把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 不把 PR-S0 的 finding-centered 评价义务写成 A5 已冻结指标协议。
- 不把 candidate finding 直接写成 final finding。
- 不把 研究者定义的 meta-model 写成 LLM 自动生成或作者预设 universal SE ontology。
