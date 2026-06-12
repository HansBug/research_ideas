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

1. Software Engineering SLR and Systematic Mapping：软件工程系统综述与系统映射研究，重点介绍 protocol、search、screening、extraction、synthesis、reporting 的基本规范。
2. PRISMA and Transparent Reporting：PRISMA 与透明报告，说明它是 flow / checklist / exclusion ledger 参考，不等于本文默认合规。
3. Review Automation Tools：综述自动化工具，覆盖 ASReview、RobotReviewer 和 systematic review automation practical guide。
4. LLM-assisted Evidence Synthesis：LLM 辅助筛选、抽取与综合，重点讨论幻觉、provenance 和 unsupported claim 风险。
5. Positioning：本文定位，明确多阶段 agent workflow、claim-to-source evidence package 与 human audit gates 的差异。

## 4. Problem Definition

应定义：

1. 输入：研究主题、RQ seed、检索协议、候选论文、全文状态、抽取 schema、编码 schema、审计政策。
2. 输出：query log、screening ledger、fulltext status、extraction table、coding decisions、claim-evidence map、PRISMA-style materials、report draft。
3. human audit gates：protocol approval、screening audit、gold / silver fact audit、disagreement adjudication、final claim review。
4. 不属于任务目标：禁止写完全自动 SLR、PRISMA-compliant、complete coverage。

## 5. Agent-Based SLR Workflow

应按 [protocol.md](./protocol.md) 的 stage contract 展开：

1. protocol setup：定义 RQ、范围、纳排标准、数据库和人工审计门。
2. query planning and search logging：生成检索式并记录数据库、时间、结果数和失败。
3. deduplication and screening：去重、标题摘要筛选、保留 include / exclude 理由。
4. fulltext availability logging：记录全文获取状态、版权边界和人工下载需求。
5. extraction with evidence locator：抽取字段时保留页码、段落或原文定位。
6. coding and taxonomy：把抽取结果映射到 taxonomy，并标注 uncertain / disagreement。
7. synthesis and claim-evidence map：综合结论必须回连证据链和审计状态。
8. PRISMA-style reporting：生成 flow、排除理由和协议偏离记录，但不声称合规。
9. audit / rollback / claim downgrade：人工审计发现问题后回滚、降级或删除 claim。

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

A0 不冻结场景。候选资产总账见 [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，后续 A3 应考虑：

1. 小型已知领域场景，便于 gold / silver fact 构造。
2. 中型 systematic mapping 场景，检验 taxonomy / coding。
3. LLM4SE / LLM4Modeling 场景，贴近博士主题。
4. 控制系统 STM / `sources/` 场景，作为 stress test。

注意：场景数量不是 A0 的硬要求；不要把“四个真实例子”写成 PR #101 的已冻结要求。

## 8. Results Plan

A0 不写结果。后续结果应围绕：

1. evidence package completeness：证据包字段是否齐全，哪些环节最容易缺证据。
2. traceability failure modes：claim-to-source 链条在哪些阶段断裂。
3. factuality / hallucination errors：metadata、引用、抽取和综合中的事实错误或无证据 claim。
4. audit gate interception：人工审计门拦截了哪些错误，仍残留哪些风险。
5. coverage proxy：known-item、seed recovery 和 database overlap 等覆盖代理。
6. cost / efficiency trade-off：agent 时间、token / API 成本、人工审计成本之间的权衡。
7. scenario-level differences：不同场景下错误模式和审计收益是否不同。

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

1. workflow schema：每个阶段的输入、输出、状态和失败字段。
2. query logs：检索式、数据库、时间、结果数和异常记录。
3. screening ledger：纳排决策、理由、分歧和裁决。
4. extraction / coding tables：字段抽取、证据定位、编码标签和不确定标记。
5. claim-evidence map：报告级 claim 与来源、抽取、编码、审计状态的映射。
6. audit logs：人工审计样本、发现的问题、裁决和修正。
7. run records：模型、prompt、usage、错误、重试和 redaction 记录。
8. redaction / copyright-safe policy：版权安全发布、全文不可发布时的替代证据策略。

## 11. Conclusion

结论应回到谨慎主张：本文研究可审计 agent-based SLR workflow 与 evidence package；不声称 agent 替代 SLR 专家。
