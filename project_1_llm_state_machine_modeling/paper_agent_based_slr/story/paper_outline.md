# Paper Outline：第二篇 researcher-guided agentic SLR 支持工作流

## 1. 使用说明

本文件给出后续 manuscript 的 section-level 架构。section heading 可保留必要英文术语，便于后续转英文稿；每节内容说明以中文为主。PR-S0 不写完整论文正文，也不写结果型 claim。

## 2. Introduction

目标：解释为什么 researcher-guided agentic SLR support workflow 是一个值得研究的问题，而不是把它写成又一篇自动化综述或 `sources/` 文库综述。

应覆盖：

1. 软件工程 SLR / systematic mapping 不只是文献整理，也是在特定研究主题上形成 research findings。
2. 现有自动化工具和新近 LLM / agent 工作已经覆盖筛选、抽取、evidence synthesis、survey generation、human-in-the-loop 和局部 provenance；因此本文不能写成 firstness。
3. 本文不追求 agent 替代专家，而是研究由 researcher 先定义 / 裁剪 / 实例化 review meta-model scaffold 的 support workflow。
4. 核心主张：从“生成综述文本 / evidence package”转向“围绕 candidate findings 形成可挑战、可修订、可降级、可接受的证据过程”。
5. 贡献草案必须保持 candidate 性质，等待 A2/A3/A5/A6 证据闭合。

## 3. Background and Related Work

建议分成以下小节：

1. **Software Engineering SLR and Systematic Mapping**：软件工程系统综述与系统映射研究，重点介绍 protocol、search、screening、extraction、synthesis、reporting 的基本规范。
2. **PRISMA and Transparent Reporting**：PRISMA 与透明报告，说明它是 flow / checklist / exclusion ledger 参考，不等于本文默认合规。
3. **Review Automation Tools**：综述自动化工具，至少要覆盖 ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 和 SE 方法学讨论。
4. **LLM-assisted Evidence Synthesis and Survey Generation**：LLM 辅助筛选、抽取、综合和 survey generation，重点讨论幻觉、provenance、unsupported claim、report-level overclaim 风险。
5. **Finding-oriented SLR support**：本文定位，明确 researcher-defined review meta-model、finding patterns、finding-centered evidence chain 与 researcher challenge loop 的差异。

## 4. Problem Definition

应定义：

1. 输入：综述主题、初始 RQ、seed papers、研究者关注点、review meta-model scaffold、source scope、候选论文、全文状态、抽取 schema、编码 schema、审计政策。
2. 输出：topic-specific review meta-model、researcher-approved executable schema、evidence object table、candidate finding ledger、challenge / revision / downgrade / unresolved log、PRISMA-style 透明材料、report projection。
3. human / researcher gates：meta-model approval、schema approval、finding challenge、final finding review。
4. 不属于任务目标：禁止写完全自动 SLR、PRISMA-compliant、complete coverage、first automated / first agentic SLR。

## 5. Method / Workflow

应按 [story/paper_story.md](./paper_story.md) 的 stage contract 展开：

1. review meta-model instantiation：researcher 基于 scaffold 设定 review objects、relations、evidence fields、scope constraints 与 finding types。
2. executable schema preparation：系统辅助将 topic-specific review meta-model 转成 researcher-approved executable schema。
3. evidence acquisition：检索、去重、筛选、全文状态记录和合法获取状态管理。
4. evidence extraction and coding：从全文 / metadata 抽取 evidence objects 并按 schema 编码。
5. candidate finding proposal：agent 根据 finding pattern scaffold 从 evidence objects 中提出 candidate findings。
6. evidence-chain construction：组织 supporting / counter evidence、source anchors、claim strength 与 uncertainty。
7. researcher challenge / refinement：researcher 发起质疑，系统补证、找反例、修订或降级。
8. final finding decision and report projection：researcher 接受、降级或保留 unresolved findings，并投影到报告草案。
9. transparency artifacts：PRISMA-style flow、排除理由、协议偏离记录、审计日志。

关键写法：强调接口、证据包、finding lifecycle 和审计门，不把工程日志写成方法贡献。

## 6. Evaluation Design

PR-S0 只列维度，不写最终公式。后续 A5 冻结指标。

维度包括：

1. traceability：claim-to-source chain 是否断链；
2. factuality：metadata、venue、DOI、抽取字段是否正确；
3. unsupported / overclaimed findings：不存在论文、错误来源、无证据 finding、过度综合；
4. finding quality / usefulness：candidate finding 是否有研究意义、非平凡且可审计；
5. screening consistency：include / exclude 决策与理由稳定性；
6. extraction / coding consistency：字段和标签的一致性；
7. challenge effectiveness：challenge 是否产生修订、降级、unresolved 或新证据；
8. coverage proxy：known-item recall、seed recovery、database overlap；
9. transparency：PRISMA-style flow、排除理由、协议偏离日志；
10. cost and efficiency：agent 时间、token / API cost、人工审计时间；
11. audit effectiveness：审计拦截率、误报率、残余 unsupported claim。


### 6.1 PR #101 RQ1--RQ7 到 PR-S0 评价 gate 的显式映射

本表只登记 downstream obligation，不表示 PR-S0 已经完成实验；状态列含义为：`PR-S0冻结口径` = 本 PR 只冻结问题与边界，`A2` = workflow/schema gate，`A3` = 场景/gold set gate，`A5` = 指标/统计 gate，`A6` = 论文写作 gate。

| PR #101 RQ | PR-S0 改写后的问题 | 评价维度 | 后续 gate / 验收口径 | PR-S0 状态 |
|---|---|---|---|---|
| RQ1 证据包可追踪性 | researcher-guided workflow 能否让 candidate / final finding 回溯到 search、screening、extraction、coding、evidence locator 与 audit status？ | traceability、finding-centered evidence chain、transparency | A2 定义 claim-to-source / finding-to-source schema；A5 统计断链率、定位错误率和未闭合 finding。 | PR-S0冻结口径 |
| RQ2 筛选 / 抽取事实准确性 | meta-model 与 executable schema 是否帮助提高 evidence extraction / coding 的事实准确性和一致性？ | factuality、extraction / coding consistency、screening consistency | A3 构造 gold / silver facts；A5 冻结字段级准确率、标签一致性、错误分类。 | PR-S0冻结口径 |
| RQ3a 幻觉 / unsupported 主张 | agent 提出的 candidate findings 中会出现哪些 unsupported、overclaimed、错误引用或 scope drift？ | unsupported / overclaimed findings、factuality、hallucination taxonomy | A3 设计 trap papers / known irrelevant set；A5 报告 unsupported finding rate、overclaim 类型和残余错误。 | PR-S0冻结口径 |
| RQ3b 人工审计拦截 | researcher challenge / audit loop 能拦截、修订、降级或标 unresolved 多少 candidate findings？ | challenge effectiveness、audit effectiveness、residual unsupported finding | A2 定义 challenge log；A5 统计 interception、revision、downgrade、unresolved、false positive / false negative。 | PR-S0冻结口径 |
| RQ4 成本收益 | meta-model、finding pattern 与 challenge loop 带来的人工成本、agent cost 与可靠性权衡是什么？ | cost / efficiency、audit time、revision cost | A4 run record 写 usage / time；A5 统计 token/API、人审时间、修订成本；禁止预设正收益。 | PR-S0冻结口径 |
| RQ5 场景差异 | 不同 SE / LLM4Modeling / MDE / `sources` 场景下 finding 类型、错误模式和 challenge 结果有何差异？ | scenario-level differences、finding type coverage、coverage proxy | A3 冻结 replay / prospective scenarios、known-item sets、scope limitation；A5 分场景报告。 | PR-S0冻结口径 |
| RQ6 与手工 SLR / 已有自动化工具关系 | 相比 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 和传统手工流程，本文的定位是什么？ | differential novelty、baseline capability matrix、human-in-the-loop boundary | A6 Related Work 必须引用 B0 P0/P1；A5 若做对比只能比明确阶段子任务，不硬比“优于人类”。 | PR-S0冻结口径 |
| RQ7 透明报告与覆盖代理 | workflow 能否生成 PRISMA-style 透明材料和 coverage proxy，同时避免 PRISMA-compliant / complete coverage 过强 claim？ | transparency、coverage proxy、protocol deviation log | A2 定义 report artifact；A3 定义 seed / known set；A5 冻结 proxy 公式与 checklist。 | PR-S0冻结口径 |

## 7. Benchmark / Case Study Scenarios

PR-S0 不冻结场景。候选资产总账见 [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，后续 A3 应考虑：

1. 小型已知领域场景，便于 gold / silver fact 构造。
2. 中型 systematic mapping 场景，检验 taxonomy / coding 和 challenge loop。
3. LLM4SE / LLM4Modeling 场景，贴近博士主题。
4. 控制系统 STM / `sources/` 场景，作为 stress test。

注意：场景数量不是 PR-S0 的硬要求；不要把“四个真实例子”写成当前已冻结要求。

## 8. Results Plan

PR-S0 不写结果。后续结果应围绕：

1. evidence package completeness：证据包字段是否齐全，哪些环节最容易缺证据。
2. traceability failure modes：claim-to-source 链条在哪些阶段断裂。
3. factuality / unsupported finding errors：metadata、引用、抽取和综合中的事实错误或无证据 finding。
4. challenge loop effects：人工 challenge 产生了哪些 revision / downgrade / unresolved / new evidence。
5. coverage proxy：known-item、seed recovery 和 database overlap 等覆盖代理。
6. cost / efficiency trade-off：agent 时间、token / API 成本、人工审计成本之间的权衡。
7. scenario-level differences：不同场景下错误模式和审计收益是否不同。

## 9. Threats to Validity / Limitations

必须提前承认：

1. coverage proxy 不等于 complete coverage；禁止把覆盖代理写成完整覆盖；
2. PRISMA-style 不等于 PRISMA-compliant；禁止写合规 claim；
3. human / researcher audit gates 不保证完全正确；
4. scenario 数量和领域会限制泛化；
5. LLM provider drift 和模型版本会影响复现；
6. PR #97 若未合入，只能作为 snapshot evidence；
7. copyright / fulltext availability 会限制 artifact release；
8. challenge loop 可能增加成本并产生 unresolved findings，不能预设正收益。

## 10. Artifact and Reproducibility

应说明后续 artifact 包括：

1. workflow schema：每个阶段的输入、输出、状态和失败字段。
2. query logs：检索式、数据库、时间、结果数和异常记录。
3. screening ledger：纳排决策、理由、分歧和裁决。
4. extraction / coding tables：字段抽取、证据定位、编码标签和不确定标记。
5. candidate finding ledger：candidate finding、supporting evidence、counter evidence、uncertainty、revision / downgrade / unresolved / accepted 状态。
6. challenge logs：researcher 的质疑、系统补证、反例、修订、降级和 stop condition。
7. claim-evidence map：报告级 claim 与来源、抽取、编码、审计状态的映射。
8. audit logs：人工审计样本、发现的问题、裁决和修正。
9. run records：模型、prompt、usage、错误、重试和 redaction 记录。
10. redaction / copyright-safe policy：版权安全发布、全文不可发布时的替代证据策略。

## 11. Conclusion

结论应回到谨慎主张：本文研究 researcher-guided agentic SLR support workflow 与 finding-centered evidence package；不声称 agent 替代 SLR 专家。
