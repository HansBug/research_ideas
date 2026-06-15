# Paper Story：研究者引导、发现导向、可审计的 agentic SLR 支持工作流

## 1. Working title

候选中文标题：**面向软件工程 SLR/SMS 的研究者引导、发现导向、可审计 agentic 支持工作流**。

候选英文标题只作为后续写作入口：**Toward Researcher-Guided and Finding-Oriented Agentic Support for Auditable Software Engineering Reviews**。

标题边界：不得暗示端到端无人、完全自动、完整覆盖、PRISMA-compliant；`agent-based SLR` 只能作为 umbrella term，正式 story 优先使用 **researcher-guided agentic SLR support workflow**。

## 2. Thesis

本文研究一种 **researcher-guided, finding-oriented, auditable agentic SLR support workflow**：researcher 基于 review meta-model scaffold 裁剪并实例化 topic-specific review meta-model，确认 researcher-approved executable schema；agent 在该 schema 与 finding pattern scaffold 约束下抽取 evidence objects、提出 candidate findings 并构建 evidence chains；researcher 通过 audit / challenge loop 对 finding 的证据、反例、scope 与 claim strength 进行质疑、修订、降级或接受。本文评价的核心不是自动生成综述文本，而是 candidate finding 的 evidence-groundedness、traceability、unsupported / overclaimed finding 控制、challenge revision、审计成本与可复查性。

## 2.1 Story 成熟度与更新策略

PR-B0 的 35 篇全文文本级 baseline 调研与全 CCF A/B/C 扩展 discovery 已经表明，宽泛的“LLM / agent 自动化综述”“多 agent SLR workflow”“自动生成 survey / review”叙事会被已有近邻工作打穿。因此 PR-S0 不再把 story 写成“自动生成综述文本”或“多阶段 evidence package workflow”本身，而是把 novelty 候选收紧到：**researcher-defined meta-model scaffold + finding pattern scaffold + finding-level evidence chain + researcher challenge loop**。

本文档是 PR-S0 后续 story 真源之一；术语必须优先遵守 [terminology_policy.md](./terminology_policy.md)。若本文档与 2026-06-15 正式导师讨论记录或 [terminology_policy.md](./terminology_policy.md) 冲突，应以后者为准并回写本文件。

更新原则：宁可把 story 写成可审计、可降级、可迭代的研究假设，也不要把尚未实验验证的 candidate contribution 写成最终结论。后续 PR 若新增 baseline、survey-of-surveys、scaffold、真实运行或评价结果，必须同步更新本文档、[paper_outline.md](./paper_outline.md)、[claim_evidence_map.md](./claim_evidence_map.md)、[differential_novelty_matrix.md](./differential_novelty_matrix.md) 与 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。

## 3. Task Boundary

| 项 | PR-S0 冻结口径 |
|---|---|
| 输入 | 综述主题、初始 RQ、seed papers、领域知识、researcher 关注点、source scope、候选论文池、全文可获取性记录。 |
| researcher-owned 输入 | review meta-model scaffold 的裁剪 / 实例化决定、topic-specific review meta-model、finding pattern 选择、audit / challenge 政策。 |
| agent 处理对象 | metadata、全文、evidence objects、抽取字段、coding decisions、candidate findings、supporting / counter evidence、challenge logs。 |
| 输出 | finding-centered evidence package：researcher-approved executable schema、evidence object table、candidate finding ledger、claim-evidence map、challenge / revision / downgrade / unresolved log、PRISMA-style 透明报告材料、downstream report projection。 |
| final finding 条件 | 只有 source-anchored supporting evidence、counter-evidence / uncertainty 检查或缺口标记、scope 与 claim strength 经 researcher 确认后，candidate finding 才能升级为 final finding。 |
| 人的角色 | 设定 / 确认 meta-model、批准 executable schema、审计证据链、发起 challenge、裁决分歧、确认 final finding。 |
| agent 的角色 | 辅助检索、筛选、抽取、编码、candidate finding proposal、evidence-chain construction、counter-evidence search、revision / downgrade proposal 和报告投影。 |
| 不属于 PR-S0 | 真实 pipeline 实现、真实 LLM 运行、四个真实例子、完整 survey-of-surveys、完整 scaffold schema、最终评价指标公式、完整论文正文。 |
| 不属于本文强 claim | 禁止写完全替代 SLR 专家、端到端无人自动产出合格 SLR、PRISMA-compliant、complete coverage、first automated / first agentic SLR、LLM 自动定义可靠 meta-model。 |

## 4. Problem Gap

传统 SE SLR / SMS 的价值不只是把文献整理成列表，而是围绕 researcher 关心的问题形成 research findings：哪些主题被充分研究，哪些方法存在系统性不足，哪些证据相互冲突，哪些结论只在特定 scope 下成立。已有自动化工具和新近 LLM / agent 工作已经覆盖了筛选、抽取、分类、evidence synthesis、survey generation、human-in-the-loop 与局部 provenance；当前缺口不再是“没有自动化”，而是：**当 agent 参与多阶段 review 时，如何让 researcher 的概念框架、candidate finding、证据链、反证、降级和最终接受过程成为可审计对象**。

因此本文不主张发明 SLR，也不主张首次自动化 SLR；本文聚焦 agent 化之后的 **finding formation reliability**：candidate findings 如何在 researcher-defined meta-model 与 finding patterns 约束下生成，如何被 evidence chain 支撑或反驳，如何经 researcher challenge loop 修订、降级、保留 unresolved 或接受为 final findings。

## 5. Technical Challenge

1. **review frame 隐性化**：不同 researcher 对同一 SLR 主题的对象、关系、证据字段和 finding 类型理解不同；若 meta-model 不显式化，agent 很容易把通用摘要框架误当成领域发现框架。
2. **candidate finding 与 final finding 混淆**：LLM / agent 很容易生成看似合理的 gap、trend 或 conclusion；若没有 finding lifecycle，就会把未审计 candidate finding 误写成最终研究发现。
3. **证据链必须支持质疑而非只支持展示**：报告级 traceability 只是最低要求；researcher 还需要看到 supporting evidence、counter-evidence、uncertainty、scope 与 revision history，才能质疑或降级 finding。
4. **多环节漂移会累积到 finding**：检索、筛选、全文可用性、抽取、编码和综合任一阶段的错误都会改变 candidate finding 的强度和范围。
5. **人工审计不是免费 oracle**：challenge loop 可能提高可复查性，也可能增加成本、暴露 unresolved finding；必须记录审计时间、分歧、降级、残余 unsupported claim，而不是只报告“人工通过”。

## 6. Method Insight

核心设计原则：**把 agentic SLR 从“生成综述文本 / 证据包”进一步改写成“围绕 candidate findings 构建可质疑、可修订、可降级、可接受的证据形成过程”**。

这意味着：

1. meta-model 是 researcher 的问题意识入口，不是 LLM 自动生成的 universal SE ontology；
2. finding patterns 约束 agent 提出何种 candidate finding，而不是让模型自由综合；
3. evidence package 以 finding 为中心组织，既保存 supporting evidence，也保存 counter-evidence、uncertainty 与 challenge history；
4. final finding 是 researcher 审计后的状态，不是 agent 输出后的默认标签。

## 7. System / Method Stages

| 阶段 | 目标 | PR-S0 证据 / 后续 gate |
|---|---|---|
| M0 Review meta-model instantiation | researcher 基于 scaffold 声明 review objects、relations、evidence fields、scope constraints 与 finding types。 | 后续 scaffold PR 必须给出字段、示例和 approval log；PR-S0 只冻结术语和 story 角色。 |
| M1 Executable schema preparation | 系统辅助把 topic-specific review meta-model 转成 researcher-approved executable schema。 | A2 需冻结 schema contract；未经 researcher approval 的 schema 不进入正式 run。 |
| M2 Evidence acquisition | 执行检索、去重、筛选、全文状态记录和合法获取状态管理。 | query log、screening ledger、fulltext status、版权/失败记录；coverage 只能用 proxy。 |
| M3 Evidence extraction and coding | 从全文 / metadata 抽取 evidence objects 并按 schema 编码。 | extraction table、source locator、negative evidence、uncertain、coding disagreement。 |
| M4 Candidate finding proposal | agent 根据 finding pattern scaffold 从 evidence objects 中提出 candidate findings。 | candidate finding ledger；必须标明 finding type、scope、supporting evidence 和 uncertainty。 |
| M5 Evidence-chain construction | 为每个 candidate finding 组织 supporting / counter evidence、claim strength 与 source anchors。 | claim-to-source chain、counter-evidence list、unsupported / overclaim 检查。 |
| M6 Researcher challenge / refinement | researcher 对 candidate finding 提出质疑，系统补证、找反例、修订或降级。 | challenge input、operation、output、stop condition、revision / downgrade / unresolved log。 |
| M7 Final finding decision and report projection | researcher 接受、降级或保留 unresolved findings，并投影到报告草案。 | final finding status、scope / claim strength、PRISMA-style 透明材料；禁止写 PRISMA-compliant。 |

传统 query / screening / fulltext / extraction 流程仍然重要，但在 PR-S0 story 中它们服务于 finding-centered evidence workflow，而不是论文主贡献本身。

## 8. Candidate Contributions

PR-S0 只冻结候选贡献。后续 A2/A3/A5/A6 必须用 scaffold、运行记录和评价结果支持后，才可进入摘要或引言。

| 候选贡献 | 当前状态 | 所需证据 |
|---|---|---|
| Researcher-instantiated review meta-model scaffold | 方法设计候选 | scaffold 字段、实例化协议、researcher approval 记录、survey-of-surveys 设计依据。 |
| Finding pattern scaffold for SLR findings | 方法设计候选 | finding pattern 来源、示例、适用/不适用条件、人工可理解性与审计记录。 |
| Meta-model-guided agent support workflow | workflow / artifact 候选 | schema-driven extraction / coding / finding proposal 的 stage contract、run record 和失败分类。 |
| Evidence-backed researcher challenge loop | 方法与评价候选 | challenge log、supporting / counter evidence、revision / downgrade / unresolved rate、审计成本。 |
| Finding-centered evaluation protocol | 评价候选 | candidate finding relevance、evidence-groundedness、claim-to-source accuracy、unsupported finding rate、cost / audit effectiveness。 |

“多场景 benchmark / case study”是后续证据计划，不是 PR-S0 的核心贡献；它必须服务于上述贡献的验证。

## 9. Evidence Plan

| 证据类型 | 当前 PR-S0 状态 | 后续落点 |
|---|---|---|
| 导师定调 | 2026-06-15 正式记录已明确 meta-model 由使用该 work 的 researcher 基于 scaffold 设定，SLR 要形成 findings，并允许 researcher challenge。 | 本文档、[paper_outline.md](./paper_outline.md)、[claim_evidence_map.md](./claim_evidence_map.md)。 |
| B0 baseline | 35 篇全文文本级 baseline + 全 CCF A/B/C discovery 已说明宽泛自动化 story 被击穿。 | [differential_novelty_matrix.md](./differential_novelty_matrix.md)、Related Work、A1/A6。 |
| `sources/` 文库 | `main` 已有，可作为 domain scenario / stress test 线索。 | A3 场景设计；不能作为 paper novelty 本身。 |
| PR #97 438→69→25 与 25 篇全文 | PR #97 OPEN / 未合入 / snapshot evidence。 | 若 PR #97 merge 或冻结 SHA 后再复核；不得写成 main fact。 |
| survey-of-surveys | PR-S0 只登记为 design basis need，不执行。 | 后续新增子 PR：抽取 SE / AI4SE / MDE / LLM4SE survey 的 RQ、taxonomy、finding pattern 与 evidence schema。 |
| scaffold / runtime | PR-S0 不实现。 | A2 / scaffold PR / A4。 |
| 真实运行 | PR-S0 不运行。 | A3/A4/A5；真实 LLM 必须 `source .env` 并保存 run record。 |
| 评价指标 | PR-S0 只登记 finding-centered obligations。 | A5 冻结公式、阈值、统计协议和 artifact checklist。 |

## 10. Related Work Positioning

本文必须主动承认：已有工作已经覆盖多 agent SLR workflow、clinical evidence synthesis、HITL provenance、screening / extraction、survey generation 与 SE LLM-SLR 方法学风险。差异化不能写成“首次 agentic SLR”，只能写成特定组合：**researcher-instantiated meta-model + finding pattern scaffold + finding-level evidence chain + researcher challenge protocol**。

| baseline / 方向 | 已有能力 | 对本文的约束 | 本文候选差异 |
|---|---|---|---|
| AgentSLR / epidemiological systematic review evaluation harness | 检索、筛选、PDF-to-Markdown、结构化抽取、专家标注与分阶段评价。 | 不能写“首次评估 AI-based SLR workflow”；必须有阶段级评价和成本意识。 | 聚焦 SE SLR/SMS 的 researcher-defined review frame、finding lifecycle 与 challenge log。 |
| LatteReview | 多 agent screening / relevance scoring / structured extraction workflow，含 senior reviewer 裁决和结构化输出。 | 不能把“多 agent SLR workflow”当核心 novelty。 | 不以筛选/抽取工作流为终点，而以 candidate findings 的证据、反证、降级和 final decision 为中心。 |
| EviSearch | clinical evidence extraction 的 per-cell provenance、page / modality / quote attribution 与 reviewer edits。 | 不能声称 evidence provenance / HITL audit 是空白。 | 从 cell-level extraction provenance 扩展到 SE review finding-level claim-to-source、counter-evidence 与 challenge revision。 |
| LR-Robot | expert taxonomy + LLM classification + RAG knowledge base / network analysis，human-in-the-loop。 | 不能声称 expert-defined taxonomy + LLM 分类未被研究。 | meta-model 不只服务分类，还约束 finding patterns、candidate finding proposal 和 challenge loop。 |
| TrialMind | clinical search、screening、extraction、meta-analysis inputs 与 human-AI collaboration。 | 不能写完整 evidence synthesis pipeline 空白。 | 避免 clinical PICO/统计综合语境，强调 SE SLR/SMS 的开放证据对象、finding audit 与报告级 claim control。 |
| WSESE@ICSE 2025 LLM-SLR difficulties | SE 社区已讨论 LLM 支持 SLR conducting / replication 的困难。 | 不能写 SE 社区尚未意识到 LLM-SLR 风险。 | 把 prompt 敏感性、随机性、透明性、数据仓库缺口转成可审计 workflow 与 evaluation obligations。 |
| Beyond Accuracy / SE SLR screening variability | SE SLR screening 中 LLM 变异性、人工复核路由和治理问题。 | 不能把 screening accuracy/F1 当完整贡献。 | 将 screening 风险纳入 finding evidence chain 与 challenge protocol。 |
| Automated survey / literature review generation | 自动生成综述文本、引用、survey 结构和 LLM-as-Judge 评价。 | 不能把报告生成或文本质量当核心 novelty。 | 报告只是 accepted / downgraded / unresolved findings 的下游投影。 |
| ASReview / RobotReviewer / review automation | 主动学习筛选、risk-of-bias / evidence automation、机器学习辅助综述。 | 不能写 first automated SLR 或 prior work 只有人工综述。 | 正面定位在 agentic / LLM 时代的 finding-centered audit 与 researcher challenge。 |

## 11. Claims to Make

以下 claim 只有在后续证据闭合后才能进入摘要 / 引言；PR-S0 仅登记安全方向。

- 本文研究 researcher-guided agentic support for SE SLR/SMS，而不是端到端无人自动 SLR。
- 本文把 researcher-owned meta-model 作为 review frame 起点，让 agent 在 researcher-approved schema 下执行抽取、编码和 candidate finding proposal。
- 本文把 SLR 的 research finding 功能显式化，用 finding patterns 约束 candidate finding 类型和证据要求。
- 本文要求 candidate finding 通过 evidence chain、counter-evidence / uncertainty 标记和 researcher challenge 后，才能升级为 final finding。
- 本文计划以 finding relevance、evidence-groundedness、claim-to-source traceability、unsupported / overclaimed finding rate、challenge revision、coverage proxy、transparency 与 human cost 评价方法可靠性。

## 12. Claims to Be Careful About

| 谨慎 claim | 风险 | 安全写法 |
|---|---|---|
| meta-model scaffold 有用 | 需要 survey-of-surveys、实例化案例和用户/专家审计支持。 | 在若干 SE review 场景中观察 scaffold 是否改善抽取 / 编码结构化程度。 |
| finding patterns 提高 finding quality | quality 需定义，且可能只改变 finding 类型覆盖或可审计性。 | 评估 candidate finding 的 relevance、non-triviality、evidence-groundedness 与可审计性。 |
| challenge loop 有收益 | challenge 可能增加成本，也可能产生 unresolved finding。 | 报告 revision / downgrade / unresolved / new evidence 与 audit time，不预设正收益。 |
| evidence chain 降低 unsupported findings | 需要 gold / silver fact、人工核验和残余错误统计。 | 报告 unsupported / overclaimed finding rate 与 audit interception。 |
| 适用于 SE SLR/SMS | 场景数量和主题会限制泛化。 | 明确 scope：只在选定 SE / LLM4Modeling / MDE 场景中观察。 |
| PRISMA-style report 可生成 | 不等于 checklist 合规。 | 写“生成 PRISMA-style 透明材料”，不写合规。 |

## 13. Claims to Avoid

- 禁止写 agent 完全替代 SLR 专家。
- 禁止写端到端无人自动产出合格 SLR。
- 禁止写首次 LLM / agent 自动化 SLR、first agentic SLR 或 complete coverage。
- 禁止写 PRISMA-compliant，除非后续 checklist 与 reporting 要求全部闭合。
- 禁止写 LLM 自动定义可靠 meta-model；必须写 researcher 基于 scaffold 裁剪并确认。
- 禁止写本文提供 universal SE review ontology；当前只提供 configurable scaffold / protocol 候选。
- 禁止把 candidate finding 直接写成 final finding。
- 禁止把 final findings produced by agents 写成贡献。
- 禁止把 automated report generation 或 survey writing quality 写成核心贡献。
- 禁止把 PR #97 OPEN / 未合入资产写成 `main` 已有事实。
- 禁止把 `sources/` 文库规模写成论文 novelty 本身。
- 禁止把 PR-S0 的评价维度种子写成 A5 已经验证的指标协议。

## 14. Reviewer Risks

核心风险已结构化记录在 [../experiment_design/reviewer_risk_register.md](../experiment_design/reviewer_risk_register.md)。PR-S0 阶段最高优先级风险包括：

1. story 回滑为“又一个 agentic SLR / 自动化综述生成 workflow”；
2. novelty 被 AgentSLR、LatteReview、EviSearch、LR-Robot、TrialMind、WSESE@ICSE 2025 或 survey-generation 工作打穿；
3. meta-model 被误写成作者定义的 universal SE ontology，或误写成 LLM 自动生成；
4. candidate finding / final finding 边界不清，导致 agent 输出被当成最终研究发现；
5. challenge loop 只停留在口号，没有 input / operation / output / stop condition、revision / downgrade / unresolved 记录；
6. 评价仍停留在报告生成质量、筛选 F1 或省时，不能支撑 finding-centered claim；
7. audit gates 只报告“人工通过”，没有成本、分歧、降级和残余 unsupported finding 统计；
8. PR #97 事实漂移或资产版权边界不清。
