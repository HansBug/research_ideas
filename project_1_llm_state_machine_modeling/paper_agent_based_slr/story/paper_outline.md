# 论文大纲：研究者引导、模式演化、证据支撑的智能体式 SLR 支持方法

## 1. 使用说明

本文件给出后续论文稿的章节级架构。PR-S0-v2 不写完整论文正文，也不写结果型主张；它只冻结章节功能、论证顺序、证据义务和禁止误读。章节标题可保留必要英文术语锚点，说明文字以中文为主。

## 2. Introduction / 引言

目标：解释为什么宽泛的“LLM / agent 自动化综述”叙事已经被近邻工作压缩，为什么 SE SLR/SMS 更需要围绕 **dimension pattern lifecycle、field-level content evidence、statistical-analysis-to-finding transition、human-in-the-loop adjudication** 来设计智能体支持。

建议叙事顺序：

1. SE SLR/SMS 的核心价值不是只整理文献，而是形成可解释、可复核、能指导后续研究的 research findings。
2. LLM/agent 已经能辅助检索、筛选、抽取、总结、证据综合和报告生成；因此“自动化某个环节”不是足够强的新颖性。
3. B0 baseline 表明 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 等近邻已经覆盖多阶段 workflow、HITL、provenance、screening/extraction 和 SE LLM-SLR 风险。
4. 真实 SLR 可拆为三层：论文收集与初步处理、维度模式驱动的论文分析、统计分析与 research finding 形成。
5. 本文的核心主张：让研究者定义 meta-model 与 schema，让 agent 在批准 schema 下工作，让统计观察经过 finding heuristics 与研究者 challenge 才进入 final findings，并保留 content/process evidence 的分层审计链。
6. 贡献预告必须谨慎：所有贡献在 PR-S0-v2 只是候选，后续 A2/A3/A5/A6 用真实 schema、pilot、process data、related work 和评价闭合。

## 3. Background and Related Work / 背景与相关工作

建议分组：

1. **SE SLR / SMS 方法学**：protocol、search、screening、data extraction、synthesis、reporting、threats to validity。
2. **PRISMA 与透明报告**：解释 PRISMA-style、PRISMA-informed、PRISMA-compliant 的边界。
3. **传统 review automation**：ASReview、RobotReviewer 等，说明筛选与特定证据自动化早已有基础。
4. **LLM / agentic SLR 近邻**：AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、Closed-loop summarization、survey generation 等。
5. **SE LLM-SLR 方法学风险**：WSESE@ICSE 2025、screening variability、prompt reproducibility、model drift、transparency gap。
6. **本文定位**：不主张首次自动化；本文关注 SE SLR/SMS 中研究者定义 meta-model、可演化 dimension schema、字段级 content evidence、统计观察到 research finding 的转移，以及 researcher challenge/adjudication。

## 4. Problem Definition / 问题定义

建议明确定义：

| 要素 | 内容 |
|---|---|
| 输入 | topic、RQ、scope、seed papers、候选论文池、全文状态、研究者关注点、可用 survey-of-surveys scaffold。 |
| 研究者拥有的决策 | meta-model、dimension schema approval、schema revision/backfill、statistical analysis protocol、candidate finding challenge、final adjudication、process evidence boundary。 |
| agent 辅助对象 | 元数据、全文、overview card、field-level content evidence、统计视图、candidate finding signals、support/counter evidence draft。 |
| 输出 | approved dimension schema、overview cards、evidence table、schema revision/backfill log、statistical analysis table、candidate finding ledger、challenge/adjudication log、transparency package、process evidence。 |
| 非目标 | 端到端无人 SLR、PRISMA 合规、完整覆盖、首次 agentic SLR、LLM final findings。 |

## 5. Method / 方法

本节应以 [paper_story.md](./paper_story.md) 的 Mermaid 方法图和 [protocol.md](./protocol.md) 的阶段契约为准。建议小节如下：

### 5.1 Researcher-defined review meta-model

研究者根据 topic / RQ / scope 定义综述对象、关系、证据类型、纳排范围和潜在 finding 类型。agent 可以建议，但不能决定 operative meta-model。

### 5.2 Survey-of-surveys scaffold and seed-paper probing

从既有 SE / AI4SE / MDE / LLM4SE survey、SLR、SMS 中低成本提取 dimension patterns、finding patterns 和 evidence-presentation patterns，并用 seed papers 做可执行性压力测试。必须强调：survey-of-surveys 是 scaffold，不是目标 evidence pool，也不是 PRISMA tertiary review。

### 5.3 Pattern-evolving dimension schema

将 meta-model 投影为树状/类型化 extraction schema，定义字段、取值、证据要求、缺失值语义和版本。新类型或抽取失败触发 schema revision proposal、impact analysis 和 backfill gate。

### 5.4 Field-level content evidence extraction

agent 在 approved schema 下抽取 source anchors、quotes、tables、figures、artifact links、missing/uncertainty，并生成 evidence table。字段级证据是统计分析和 target-domain finding 的基础。

### 5.5 Statistical analysis as intermediate observation

在稳定字段表上做频次、分布、交叉表、趋势、coverage proxy 和 contradiction signal。统计分析只产生 statistical observations，不直接产生 final research findings。

### 5.6 Candidate finding signals and finding heuristics

agent 基于统计观察、finding heuristics 与 content evidence 提出 candidate finding signals。finding heuristics 可以包括 gap、trend、consensus、contradiction、maturity、method weakness、evidence weakness 等。

### 5.7 Researcher challenge and final adjudication

研究者检查证据、反例、范围、主张强度和 schema 适配性；系统补证、找反例、修订、降级、拒绝或标记 unresolved。只有经过 final adjudication 的 finding 才能进入 target-domain findings。

### 5.8 Process evidence for method evaluation

记录 schema revision、approval、challenge、adjudication、interaction turns、time cost、人工修改、拒绝建议、prompt/raw log redaction。process evidence 只支撑 method-evaluation findings。

## 6. Artifact Schema and Implementation Plan / 制品与实现计划

后续 A2/A4 应把方法落为可审计制品，而不是只写 prompt：

1. review meta-model brief；
2. dimension schema registry；
3. search/screening ledger；
4. overview cards；
5. field-level evidence table；
6. schema revision/backfill log；
7. statistical analysis table；
8. candidate finding ledger；
9. challenge/adjudication log；
10. transparency package；
11. process evidence / redaction report；
12. run record（真实 LLM 运行前必须 `source .env`，并记录 model_id、provider、usage、raw output、错误与脱敏报告）。

## 7. Pilot Study / 单主题 pilot

PR-S0-v2 不冻结 pilot 主题，但建议优先考虑 LLM4STM / LLM4Modeling，因为它贴近博士主线且已有 baseline / sources 资产可作为压力测试线索。pilot 目标不是证明泛化，而是验证：

1. L0--L7 是否能闭环；
2. dimension pattern 是否能从 scaffold / seed papers 进入 approved schema；
3. 字段级 content evidence 是否能支撑统计观察；
4. candidate finding signals 是否能被 challenge、降级、拒绝或接受；
5. schema revision 是否能触发 impact analysis 与 backfill；
6. transparency package 是否能让第三方复核。

## 8. Multi-user Process Evaluation / 多使用者过程评价

后续让硕士生使用方法时，应明确数据用途：评价方法自身，而不是证明目标领域结论。建议记录：

1. 每个 gate 的交互轮次、时间、修改和拒绝建议；
2. schema revision / backfill 次数和原因；
3. 研究者 challenge 的类型、补证量和裁决结果；
4. 学生对 schema、证据链和 finding 边界的理解难点；
5. prompt/raw log 的脱敏、匿名化和访问控制；
6. 教学关系隔离、同意书和数据使用范围。

## 9. Evaluation Design / 评价设计

评价维度种子见 [../experiment_design/evaluation_dimensions_seed.md](../experiment_design/evaluation_dimensions_seed.md)。后续 A5 至少覆盖：

1. dimension pattern stability / evolution；
2. backfill completeness / cost；
3. field-level evidence accuracy；
4. statistical analysis correctness；
5. candidate finding usefulness；
6. challenge outcome：accepted / downgraded / rejected / unresolved；
7. content/process evidence separation；
8. method-evaluation process metrics；
9. transparency package completeness；
10. cost / burden / failure modes。

## 10. PR #101 RQ 到 S0-v2 评价门槛的映射

| PR #101 RQ | S0-v2 解释 | 对应评价维度 | 后续门槛 |
|---|---|---|---|
| RQ1 可追踪性 | final / downgraded / unresolved findings 能否回到 field-level content evidence、统计观察、challenge 和 adjudication？ | content evidence accuracy、claim-evidence traceability、transparency package | A2 定义 trace schema；A5 统计断链和定位错误。 |
| RQ2 事实准确性 | 元数据、字段值、source anchor、统计输入和输出是否与来源一致？ | field-level factuality、statistical correctness | A3/A5 构造 gold/silver facts 与人工核验样本。 |
| RQ3a 无证据 / 过强主张 | candidate signals 中有多少缺证据、范围过宽、统计外推或引用错误？ | unsupported / over-strong finding classification | A3 设计 traps；A5 报告残余错误与降级。 |
| RQ3b 研究者 challenge | challenge 能否发现证据不足、反例、schema 问题和主张强度问题？ | accepted/downgraded/rejected/unresolved rate、challenge cost | A2 定义 log；A5 统计修订、降级、未解决和成本。 |
| RQ4 成本收益 | pattern evolution、evidence anchoring 与 challenge 带来的成本/收益是什么？ | audit time、token/API、backfill burden、process friction | A4 run record；A5 成本分析，不预设正收益。 |
| RQ5 场景差异 | 不同 SE / LLM4Modeling / MDE 主题下 schema 演化、证据缺失和 finding 类型有何差异？ | scenario-level difference、pattern stability、finding type coverage | A3 冻结场景与限制；A5 分场景报告。 |
| RQ6 与已有工具关系 | 相比 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind 等，本文的真正差异是什么？ | novelty matrix、baseline capability mapping | A6 相关工作必须正面对齐 B0 P0/P1。 |
| RQ7 透明报告与覆盖代理 | 方法能否产生类 PRISMA 透明材料和覆盖代理，同时避免合规/完整覆盖过强主张？ | transparency completeness、coverage proxy、protocol deviation log | A2/A5 定义制品与检查清单。 |

## 11. Results Plan / 结果计划

PR-S0-v2 不写结果。未来结果应围绕：

1. schema 演化次数、原因、backfill 范围和完成率；
2. 字段级证据定位正确性、缺失类型和不确定性；
3. 统计观察与字段版本的一致性；
4. candidate finding signals 的接受、降级、拒绝、未解决比例；
5. challenge 带来的补证、反例、修订和主张强度变化；
6. process evidence 中的人机交互成本、失败模式和隐私/脱敏负担；
7. 与强近邻相比，本方法在哪些主张上更安全，哪些仍然只是候选。

## 12. Limitations / 效度威胁

必须提前承认：

1. survey-of-surveys scaffold 不等于 complete survey-of-surveys，也不进入目标 findings evidence pool；
2. coverage proxy 不等于完整覆盖；
3. 类 PRISMA 不等于 PRISMA 合规；
4. final finding 仍依赖研究者判断，不能保证绝对正确；
5. pilot 只验证闭环与可执行性，不能证明泛化；
6. 学生 process data 只能支撑方法评估，且有 consent / anonymization / teaching relationship 风险；
7. LLM provider drift、模型版本和 prompt drift 会影响复现；
8. 版权 / 全文可获取性会限制制品发布。

## 13. Conclusion / 结论

结论应回到谨慎口径：本文研究 researcher-guided、pattern-evolving、evidence-backed、finding-oriented 的智能体式 SLR/SMS 支持方法；它的目标是让 dimension schema、content evidence、statistical analysis、candidate finding signals、researcher challenge 和 final adjudication 可审计，而不是让 agent 替代 SLR 专家或自动生成最终综述。
