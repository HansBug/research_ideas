# Paper Outline：第二篇 agent-based SLR

## 1. 使用说明

本文件给出后续 manuscript 的 section-level 架构。section heading 可保留必要英文术语，便于后续转英文稿；每节内容说明以中文为主。A0 不写完整论文正文，也不写结果型 claim。

## 2. Introduction

目标：解释为什么 agent-based SLR 是一个值得研究的问题，而不是把它写成又一篇 `sources/` 文库综述。

应覆盖：

1. 软件工程 SLR / systematic mapping 成本高、过程长、需要透明报告和可审计证据链。
2. LLM / agent 带来自动化机会，但同时引入事实错误、无证据 claim、scope drift 和不可复核风险。
3. 本文不追求 agent 替代专家，而是研究带 human audit gates 的 agent-executed workflow。
4. 核心主张：从生成综述文本转向生成可审计 evidence package。
5. 贡献草案必须保持候选性质，等待 A3/A5 证据闭合。

## 3. Background and Related Work

建议分成以下小节：

1. Software Engineering SLR and Systematic Mapping
   - 介绍 protocol、search、screening、extraction、synthesis、reporting 的基本规范。
2. PRISMA and Transparent Reporting
   - 说明 PRISMA 是透明报告参考，不等于本文默认合规。
3. Review Automation Tools
   - 覆盖 ASReview、RobotReviewer、systematic review automation practical guide。
4. LLM-assisted Evidence Synthesis
   - 覆盖 LLM 用于筛选、抽取、综合的近邻工作，重点讨论幻觉和 provenance 风险。
5. Positioning
   - 明确本文差异：多阶段 agent workflow、claim-to-source evidence package、human audit gates。

## 4. Problem Definition

应定义：

1. 输入：研究主题、RQ seed、检索协议、候选论文、全文状态、抽取 schema、编码 schema、审计政策。
2. 输出：query log、screening ledger、fulltext status、extraction table、coding decisions、claim-evidence map、PRISMA-style materials、report draft。
3. human audit gates：protocol approval、screening audit、gold / silver fact audit、disagreement adjudication、final claim review。
4. 不属于任务目标：禁止写完全自动 SLR、PRISMA-compliant、complete coverage。

## 5. Agent-Based SLR Workflow

应按 [protocol.md](./protocol.md) 的 stage contract 展开：

1. protocol setup；
2. query planning and search logging；
3. deduplication and screening；
4. fulltext availability logging；
5. extraction with evidence locator；
6. coding and taxonomy；
7. synthesis and claim-evidence map；
8. PRISMA-style reporting；
9. audit / rollback / claim downgrade。

关键写法：强调接口、证据包和审计门，不把工程日志写成方法贡献。

## 6. Evaluation Design

A0 只列维度，不写最终公式。后续 A5 冻结指标。

维度包括：

1. traceability：claim-to-source chain 是否断链；
2. factuality：metadata、venue、DOI、抽取字段是否正确；
3. hallucination / unsupported claim：不存在论文、错误来源、无证据 claim；
4. screening consistency：include / exclude 决策与理由稳定性；
5. extraction / coding consistency：字段和标签的一致性；
6. coverage proxy：known-item recall、seed recovery、database overlap；
7. transparency：PRISMA-style flow、排除理由、协议偏离日志；
8. cost and efficiency：agent 时间、token / API cost、人工审计时间；
9. audit effectiveness：审计拦截率、误报率、剩余 unsupported claim。

## 7. Benchmark / Case Study Scenarios

A0 不冻结场景。后续 A3 应考虑：

1. 小型已知领域场景，便于 gold / silver fact 构造。
2. 中型 systematic mapping 场景，检验 taxonomy / coding。
3. LLM4SE / LLM4Modeling 场景，贴近博士主题。
4. 控制系统 STM / `sources/` 场景，作为 stress test。

注意：场景数量不是 A0 的硬要求；不要把“四个真实例子”写成 PR #101 的已冻结要求。

## 8. Results Plan

A0 不写结果。后续结果应围绕：

1. evidence package completeness；
2. traceability failure modes；
3. factuality / hallucination errors；
4. audit gate interception；
5. coverage proxy；
6. cost / efficiency trade-off；
7. scenario-level differences。

## 9. Threats to Validity / Limitations

必须提前承认：

1. coverage proxy 不等于 complete coverage；禁止把覆盖代理写成完整覆盖；
2. PRISMA-style 不等于 PRISMA-compliant；禁止写合规 claim；
3. human audit gates 不保证完全正确；
4. scenario 数量和领域会限制泛化；
5. LLM provider drift 和模型版本会影响复现；
6. PR #97 若未合入，只能作为 snapshot evidence；
7. copyright / fulltext availability 会限制 artifact release。

## 10. Artifact and Reproducibility

应说明后续 artifact 包括：

1. workflow schema；
2. query logs；
3. screening ledger；
4. extraction / coding tables；
5. claim-evidence map；
6. audit logs；
7. run records；
8. redaction / copyright-safe policy。

## 11. Conclusion

结论应回到谨慎主张：本文研究可审计 agent-based SLR workflow 与 evidence package；不声称 agent 替代 SLR 专家。
