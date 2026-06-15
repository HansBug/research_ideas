# Reviewer Risk Register：researcher-guided agentic SLR support workflow

## 1. 口径

本文件登记 PR-S0 阶段可预见的审稿风险。C/I/M 在这里表示对论文成立性的潜在影响，不等同于当前 PR bug 等级。

| ID | 类别 | 风险 | 等级 | 触发条件 | 缓解入口 | 当前状态 |
|---|---|---|---:|---|---|---|
| R1 | Story 回滑 | 第二篇被写回 `sources/` corpus / benchmark-source landscape paper。 | C | title / abstract / contribution 以文库规模为主贡献。 | [story/paper_story.md](../story/paper_story.md)、[story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | PR-S0 已禁止。 |
| R2 | Claim 过强 | 正向声称 PRISMA-compliant。 | C | checklist 未闭合却写合规。 | [story/terminology_policy.md](../story/terminology_policy.md)、[story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | PR-S0 已禁止。 |
| R3 | Claim 过强 | 正向声称 complete coverage 或 first automated / first agentic SLR。 | C | 摘要 / 引言出现无证据首创或覆盖声明。 | [story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)。 | PR-S0 已禁止。 |
| R4 | Expert replacement | 写成 agent 完全替代专家。 | C | 方法叙事去掉 researcher ownership 或 human audit gates。 | [story/paper_story.md](../story/paper_story.md)、[story/terminology_policy.md](../story/terminology_policy.md)。 | PR-S0 已禁止。 |
| R5 | Fact drift | 把 PR #97 OPEN / snapshot 资产写成 `main` fact。 | C | 引用 438→69→25 或 25 篇全文但不标 OPEN / snapshot。 | [evidence/fact_drift_policy.md](../evidence/fact_drift_policy.md)。 | PR-S0 已建政策。 |
| R6 | Story 回滑到 workflow-only | 把本文又写成“多阶段 agent workflow / evidence package”而没有 finding lifecycle。 | C | thesis、contribution 或 method stages 没有 candidate / final finding、challenge loop。 | [story/paper_story.md](../story/paper_story.md)、[story/claim_evidence_map.md](../story/claim_evidence_map.md)。 | PR-S0 已修正方向，但需后续 review。 |
| R7 | Novelty 不足 | 忽略 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 或 survey generation。 | I | Related Work 只讲传统 SLR，不讲 B0 强近邻。 | [story/differential_novelty_matrix.md](../story/differential_novelty_matrix.md)、[baselines/SUMMARY.md](../baselines/SUMMARY.md)。 | PR-S0 已补，但需继续核验。 |
| R8 | Evaluation 弱 | 只有回顾型 replay，没有 candidate finding / challenge loop 的评价。 | I | A3 场景只有已知结果复盘。 | [dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)、[experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。 | 待 A3。 |
| R9 | Audit 黑箱 | human / researcher audit gates 没有成本、分歧、裁决、残余错误。 | I | A5 只说人工复核通过。 | [story/paper_outline.md](../story/paper_outline.md)、[experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。 | 待 A5。 |
| R10 | Hallucination / unsupported finding 未测 | 没有 trap papers、gold / silver facts 或 unsupported finding 检查。 | I | A3/A5 没有针对 finding 的幻觉测试集。 | [dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)、[experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。 | 待 A3。 |
| R11 | Citation creep | 用搜索摘要或未核验 metadata 写 Related Work。 | I | citation seed 未分层或 BibTeX 伪造。 | [evidence/citation_seed_inventory.md](../evidence/citation_seed_inventory.md)。 | PR-S0 已分层。 |
| R12 | 术语漂移 | PRISMA-style / compliant、audit / oracle、candidate / final finding 混用。 | I | 不同文档使用不同术语。 | [story/terminology_policy.md](../story/terminology_policy.md)。 | PR-S0 已建政策。 |
| R13 | 工程日志冒充贡献 | 把 run logs / agent prompts 写成 paper novelty。 | M | Method 过度描述工具实现。 | [story/paper_story.md](../story/paper_story.md)、A4/A5。 | 后续关注。 |
| R14 | 场景越界 | 把后续场景或“四个真实例子”误写成当前已冻结 benchmark。 | M | A3/A4 直接继承四个候选场景且无审计计划。 | [story/paper_outline.md](../story/paper_outline.md)、[dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)。 | PR-S0 已声明不冻结场景数量。 |
