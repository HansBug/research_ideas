# story/：论文主线、协议、术语与 claim 控制

本目录维护第二篇 agent-based SLR 论文的 story 真源。A0 阶段，它回答：这篇论文到底讲什么、采用什么流程协议、哪些术语如何使用、哪些 claim 可以写、哪些 claim 必须避免、与已有工具和方法学如何区分。

## 文件说明

| 文件 | 作用 |
|---|---|
| [paper_story.md](./paper_story.md) | A0 后的 thesis、task boundary、gap、technical challenge、method insight、contributions、evidence plan 和 reviewer risks。 |
| [protocol.md](./protocol.md) | agent-based SLR / systematic mapping 的最小 workflow 协议与 human audit gates。 |
| [terminology_policy.md](./terminology_policy.md) | SLR、systematic mapping、agent、audit gate、PRISMA-style、traceability、hallucination 等术语口径。 |
| [claim_evidence_map.md](./claim_evidence_map.md) | 每类潜在 claim 的证据状态、禁止写法、安全写法和后续所需证据。 |
| [differential_novelty_matrix.md](./differential_novelty_matrix.md) | 与 SLR/SMS、PRISMA、ASReview、RobotReviewer、review automation、LLM-assisted evidence synthesis 的差异化 novelty 矩阵。 |
| [paper_outline.md](./paper_outline.md) | 面向后续 manuscript 的 section-level 架构，正文说明以中文为主。 |

## 使用顺序

1. 先读 [paper_story.md](./paper_story.md)，确认主线是带 human audit gates 的 agent-based SLR 方法学，而不是 `sources/` corpus paper。
2. 再读 [terminology_policy.md](./terminology_policy.md)，避免 PRISMA、audit、traceability、hallucination 等术语漂移。
3. 写任何 protocol 或 Method 描述前读 [protocol.md](./protocol.md)。
4. 写任何 abstract / contribution / conclusion 句子前必须查 [claim_evidence_map.md](./claim_evidence_map.md)。
5. 写 Related Work 前读 [differential_novelty_matrix.md](./differential_novelty_matrix.md)。
6. 组织论文大纲时读 [paper_outline.md](./paper_outline.md)。

## A0 硬约束

- 不把第二篇写成 `sources/` corpus / mapping / dataset paper。
- 禁止写 agent 完全替代 SLR 专家。
- 不写端到端无人自动产出合格 SLR。
- 禁止在 checklist 未闭合前写 PRISMA-compliant。
- 禁止写 complete coverage 或 first automated SLR。
- 不把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 不把 A0 的评价维度种子写成 A5 已冻结指标协议。
