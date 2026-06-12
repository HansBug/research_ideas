# Reviewer Risk Register：agent-based SLR

## 1. 口径

本文件登记 A0 阶段可预见的审稿风险。C/I/M 在这里表示对论文成立性的潜在影响，不等同于当前 PR bug 等级。

| ID | 类别 | 风险 | 等级 | 触发条件 | 缓解入口 | 当前状态 |
|---|---|---|---:|---|---|---|
| R1 | Story 回滑 | 第二篇被写回 `sources/` corpus / benchmark-source landscape paper。 | C | title / abstract / contribution 以文库规模为主贡献。 | [paper_story.md](../story/paper_story.md)、[claim_evidence_map.md](../story/claim_evidence_map.md)。 | A0 已禁止。 |
| R2 | Claim 过强 | 正向声称 PRISMA-compliant。 | C | checklist 未闭合却写合规。 | [terminology_policy.md](../story/terminology_policy.md)、[claim_evidence_map.md](../story/claim_evidence_map.md)。 | A0 已禁止。 |
| R3 | Claim 过强 | 正向声称 complete coverage 或 first automated SLR。 | C | 摘要 / 引言出现无证据首创或覆盖声明。 | [differential_novelty_matrix.md](../story/differential_novelty_matrix.md)。 | A0 已禁止。 |
| R4 | Expert replacement | 写成 agent 完全替代专家。 | C | 方法叙事去掉 human audit gates 或写 end-to-end no human。 | [protocol.md](../story/protocol.md)。 | A0 已禁止。 |
| R5 | Fact drift | 把 PR #97 OPEN / snapshot 资产写成 `main` fact。 | C | 引用 438→69→25 或 25 篇全文但不标 OPEN / snapshot。 | [fact_drift_policy.md](../evidence/fact_drift_policy.md)。 | A0 已建政策。 |
| R6 | Novelty 不足 | 忽略 ASReview、RobotReviewer、review automation 或 LLM-assisted review。 | I | Related Work 只讲传统 SLR，不讲自动化近邻。 | [differential_novelty_matrix.md](../story/differential_novelty_matrix.md)、[citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。 | A0 seed 已覆盖。 |
| R7 | Evaluation 弱 | 只有回顾型 replay，没有前瞻型 execution。 | I | A3 场景只有已知结果复盘。 | A3 场景设计、[evaluation_dimensions_seed.md](./evaluation_dimensions_seed.md)。 | 待 A3。 |
| R8 | Audit 黑箱 | human audit gates 没有成本、分歧、裁决、残余错误。 | I | A5 只说人工复核通过。 | [protocol.md](../story/protocol.md)、A5 指标协议。 | 待 A5。 |
| R9 | Hallucination 未测 | 没有 trap papers、gold / silver facts 或 unsupported claim 检查。 | I | A3/A5 没有幻觉测试集。 | A3 gold / silver / trap design。 | 待 A3。 |
| R10 | Citation creep | 用搜索摘要或未核验 metadata 写 Related Work。 | I | citation seed 未分层或 BibTeX 伪造。 | [citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。 | A0 已分层。 |
| R11 | 术语漂移 | PRISMA-style / compliant、audit / oracle、SLR / mapping 混用。 | I | 不同文档使用不同术语。 | [terminology_policy.md](../story/terminology_policy.md)。 | A0 已建政策。 |
| R12 | 工程日志冒充贡献 | 把 run logs / agent prompts 写成 paper novelty。 | M | Method 过度描述工具实现。 | [paper_story.md](../story/paper_story.md)、A4/A5。 | 后续关注。 |

## 2. Review 使用方式

后续 reviewer 应先检查 C / I 风险是否被新 PR 触发。若触发 C/I，需要给出具体文档路径、复现 grep 或 PR body 段落，并要求修复后再推进。
