# 论文大纲：第二篇研究者引导的智能体式 SLR 支持工作流

## 1. 使用说明

本文件给出后续论文稿的章节级架构。章节标题可以保留必要英文术语，便于后续转英文稿；每节内容说明以中文为主。PR-S0 不写完整论文正文，也不写结果型 claim。

## 2. 引言

目标：解释为什么“LLM / 智能体自动化综述”这个宽泛叙事已经不够，以及为什么 SE SLR/SMS 需要围绕研究发现形成过程来重新设计智能体支持。

建议结构：

1. SE SLR/SMS 的核心价值：不是只整理文献，而是形成可解释、可复核的 research findings。
2. LLM / 智能体机会：检索、筛选、抽取、编码、综合、报告生成都可被部分支持。
3. 已有近邻压力：AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025、survey generation 已经覆盖很多自动化环节。
4. 核心主张：从“生成综述文本 / 证据包”转向“围绕候选研究发现形成可审计（auditable）、可挑战、可修订、可降级、可接受的证据过程”。
5. 贡献预告必须谨慎：PR-S0 只定义候选贡献，后续 A2/A3/A5/A6 用真实 schema、场景、运行记录和评价闭合。

## 3. 背景与相关工作

建议分组：

1. **软件工程 SLR 与系统映射研究**：介绍协议、检索、筛选、抽取、综合、报告的基本规范。
2. **PRISMA 与透明报告**：说明 PRISMA-style、PRISMA-informed、PRISMA-compliant 的区别。
3. **综述自动化工具**：至少覆盖 ASReview、RobotReviewer、AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 和 SE 方法学讨论。
4. **LLM 辅助证据综合与综述生成**：讨论幻觉、来源追溯、无证据支撑主张、报告级过强主张风险。
5. **发现导向的 SLR 支持**：本文定位，明确研究者定义的综述元模型、研究发现模式、以研究发现为中心的证据链与研究者质疑闭环的差异。

## 4. 问题定义

建议定义：

1. 输入：综述主题、RQ、种子论文、候选论文池、全文状态、研究者关注点。
2. 输出：主题特定综述元模型、研究者批准的可执行 schema、证据对象表、候选研究发现台账、质疑 / 修订 / 降级 / 未解决日志、PRISMA-style 透明材料、报告投影。
3. 人工 / 研究者审计门：meta-model approval、schema approval、finding challenge、final finding review；这些英文保留为后续 schema / stage 名称锚点。
4. 不属于任务目标：禁止写完全自动 SLR、PRISMA-compliant、complete coverage、first automated / first agentic SLR。

## 5. 方法 / 工作流

应按 [paper_story.md](./paper_story.md) 的阶段契约展开：

1. **综述元模型实例化**：研究者基于脚手架设定综述对象、关系、证据字段、范围约束与研究发现类型。
2. **可执行 schema 准备**：系统辅助将主题特定综述元模型转成研究者批准的可执行 schema。
3. **证据获取**：检索、去重、筛选、全文状态记录和合法获取状态管理。
4. **证据抽取与编码**：从全文 / metadata 抽取证据对象并按 schema 编码。
5. **候选研究发现提出**：智能体根据研究发现模式脚手架从证据对象中提出候选研究发现。
6. **证据链构建**：组织支持性 / 反向证据、来源锚点、主张强度与不确定性。
7. **研究者质疑 / 细化**：研究者发起质疑，系统补证、找反例、修订、降级或标为未解决。
8. **最终研究发现决策与报告投影**：研究者接受、降级或保留未解决研究发现，并投影到报告草案。

本节必须明确：agent 只提出 candidate finding；final finding 必须由 researcher audit 后确认。

## 6. 评价设计

PR-S0 只冻结评价义务，不写结果。评价维度种子见 [../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。后续 A5 至少要考虑：

1. 研究发现相关性与非平凡性；
2. 证据支撑度与主张到来源可追踪性；
3. 元数据、venue、DOI、抽取字段事实准确性；
4. 无证据支撑 / 过强主张研究发现率；
5. 质疑闭环的拦截、修订、降级、未解决和接受比例；
6. 人工审计时间、token / API cost 与失败重试成本；
7. 筛选、抽取、编码一致性；
8. 覆盖代理：known-item recall、seed recovery、database overlap；
9. PRISMA-style 透明材料、排除理由、协议偏离日志；
10. 不同 SE / LLM4Modeling / MDE 场景间的差异。

### 6.1 PR #101 RQ1--RQ7 到 PR-S0 评价门槛的显式映射

| PR #101 RQ | PR-S0 后的解释 | 对应评价维度 | 后续门槛 | PR-S0 状态 |
|---|---|---|---|---|
| RQ1 证据包可追踪性 | 研究者引导的工作流能否让候选 / 最终研究发现回溯到检索、筛选、抽取、编码、证据定位与审计状态？ | 可追踪性、以研究发现为中心的证据链、透明性 | A2 定义 claim-to-source / finding-to-source schema；A5 统计断链率、定位错误率和未闭合 finding。 | PR-S0 冻结口径 |
| RQ2 事实准确性 / 抽取一致性 | 论文元数据、全文字段、编码与证据定位是否与来源一致？ | 事实准确性、抽取 / 编码一致性 | A3/A5 构造 gold / silver facts 与人工核验样本。 | PR-S0 冻结口径 |
| RQ3a 幻觉 / 无证据支撑主张 | 智能体提出的候选研究发现中会出现哪些 unsupported、overclaimed、错误引用或范围漂移？ | 无证据支撑 / 过强主张研究发现、事实准确性、幻觉 taxonomy | A3 设计 trap papers / known irrelevant set；A5 报告 unsupported finding rate、overclaim 类型和残余错误。 | PR-S0 冻结口径 |
| RQ3b 人工审计拦截 | 研究者质疑 / 审计闭环能拦截、修订、降级或标未解决多少候选研究发现？ | 质疑闭环有效性、审计有效性、残余 unsupported finding | A2 定义质疑日志；A5 统计拦截、修订、降级、未解决、误报 / 漏报。 | PR-S0 冻结口径 |
| RQ4 成本收益 | meta-model、研究发现模式与质疑闭环带来的人工成本、agent cost 与可靠性权衡是什么？ | 成本 / 效率、审计时间、修订成本 | A4 运行记录写 usage / time；A5 统计 token/API、人审时间、修订成本；禁止预设正收益。 | PR-S0 冻结口径 |
| RQ5 场景差异 | 不同 SE / LLM4Modeling / MDE / `sources` 场景下 finding 类型、错误模式和 challenge 结果有何差异？ | 场景级差异、研究发现类型覆盖、覆盖代理 | A3 冻结 replay / prospective scenarios、known-item sets、scope limitation；A5 分场景报告。 | PR-S0 冻结口径 |
| RQ6 与手工 SLR / 已有自动化工具关系 | 相比 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 和传统手工流程，本文的定位是什么？ | 差异化新颖性、baseline capability matrix、human-in-the-loop boundary | A6 相关工作必须引用 B0 P0/P1；A5 若做对比只能比明确阶段子任务，不硬比“优于人类”。 | PR-S0 冻结口径 |
| RQ7 透明报告与覆盖代理 | 工作流能否生成 PRISMA-style 透明材料和 coverage proxy，同时避免 PRISMA-compliant / complete coverage 过强 claim？ | 透明性、覆盖代理、协议偏离日志 | A2 定义 report artifact；A3 定义 seed / known set；A5 冻结 proxy 公式与 checklist。 | PR-S0 冻结口径 |

## 7. 基准 / 案例研究场景

PR-S0 不冻结场景。候选资产总账见 [../dataset_selection/sample_assets.md](../dataset_selection/sample_assets.md)，后续 A3 应考虑：

1. 小型已知领域场景，便于 gold / silver facts 构造。
2. 中型 systematic mapping 场景，检验 taxonomy / coding 和质疑闭环。
3. LLM4SE / LLM4Modeling 场景，贴近博士主题。
4. 控制系统 STM / `sources/` 场景，作为 stress test。

注意：场景数量不是 PR-S0 的硬要求；不要把“四个真实例子”写成当前已冻结要求。

## 8. 结果计划

PR-S0 不写结果。后续结果应围绕：

1. 证据包完整性：证据包字段是否齐全，哪些环节最容易缺证据。
2. 可追踪性失败模式：主张到来源链条在哪些阶段断裂。
3. 事实准确性 / 无证据支撑研究发现错误：元数据、引用、抽取和综合中的事实错误或无证据 finding。
4. 质疑闭环效果：人工 challenge 产生了哪些修订、降级、未解决或新证据。
5. 覆盖代理：known-item、seed recovery 和 database overlap 等覆盖代理。
6. 成本 / 效率权衡：智能体时间、token / API 成本、人工审计成本之间的权衡。
7. 场景级差异：不同场景下错误模式和审计收益是否不同。

## 9. 效度威胁 / 局限性

必须提前承认：

1. 覆盖代理不等于 complete coverage；禁止把覆盖代理写成完整覆盖；
2. PRISMA-style 不等于 PRISMA-compliant；禁止写合规 claim；
3. 人工 / 研究者审计门不保证完全正确；
4. 场景数量和领域会限制泛化；
5. LLM provider drift 和模型版本会影响复现；
6. PR #97 若未合入，只能作为 snapshot evidence；
7. copyright / fulltext availability 会限制 artifact release；
8. 质疑闭环可能增加成本并产生 unresolved findings，不能预设正收益。

## 10. 制品与可复现性

应说明后续 artifact 包括：

1. 工作流 schema：每个阶段的输入、输出、状态和失败字段。
2. 检索日志：检索式、数据库、时间、结果数和异常记录。
3. 筛选台账：纳排决策、理由、分歧和裁决。
4. 抽取 / 编码表：字段抽取、证据定位、编码标签和不确定标记。
5. 候选研究发现台账：candidate finding、支持性证据、反向证据、不确定性、修订 / 降级 / 未解决 / 接受状态。
6. 质疑日志：研究者的质疑、系统补证、反例、修订、降级和停止条件。
7. 主张-证据映射：报告级 claim 与来源、抽取、编码、审计状态的映射。
8. 审计日志：人工审计样本、发现的问题、裁决和修正。
9. 运行记录：模型、prompt、usage、错误、重试和 redaction 记录；若后续触发真实 LLM 运行，必须先 `source .env`，并把精确模型 ID、调用日期、用量和脱敏报告写入 run record。
10. redaction / copyright-safe policy：版权安全发布、全文不可发布时的替代证据策略。

## 11. 结论

结论应回到谨慎主张：本文研究研究者引导的智能体式 SLR 支持工作流与以研究发现为中心的证据包；不声称智能体替代 SLR 专家。
