# 差异化新颖性矩阵：PR-S0-v2 相关工作边界

## 1. 目的

关键词覆盖：系统综述自动化（systematic review automation）、智能体式 SLR（agentic SLR）、LLM 辅助筛选 / 抽取 / 综合、综述生成、人在回路证据综合、来源追溯（provenance）与可审计性（auditability）。

本文件冻结 PR-S0-v2 阶段的差异化新颖性门槛。它不是完整 Related Work，也不声称已经排除所有直接竞争工作；它用于防止第二篇论文误写成首次自动化 SLR、首次智能体式 SLR、PRISMA 合规工具、自动综述生成论文或 `sources/` 语料论文。

PR-B0 已完成 35 篇本地全文文本级基线 review 与全 CCF A/B/C 扩展检索。后续 story 不能继续写“待 A1 才知道是否有强近邻”；当前已知事实是：多智能体 SLR、临床证据综合、人在回路来源追溯、筛选 / 抽取、综述生成和 SE LLM-SLR 方法学风险都已有强近邻。本文差异化不能再用“无人自动综述”来表述，而必须显式体现 **研究者定义的 review meta-model、可演化 dimension schema、字段级 content evidence、statistical analysis / research finding 分层、researcher challenge / adjudication、process evidence 支撑方法评价** 这一组合。

## 2. 矩阵口径

状态口径：🟢 = PR-S0-v2 可作为已核验证据锚点使用；🟡 = B0 已登记但仍需后续 PDF / 制品 / 引用深化；🟣 = PR #97 OPEN / 未合入 / 快照 / 分支局部证据。

| 方向 / 工具 | B0 证据等级 | 覆盖环节 / 能力 | 对本文的新颖性威胁 | 本文安全差异 | 禁止主张 | 状态 |
|---|---|---|---|---|---|---:|
| 软件工程 SLR / SMS 方法学 | 引用种子 / 方法学基础 | 协议、检索、筛选、抽取、综合、报告和效度威胁。 | 本文不能替代 SLR 方法学，也不能忽略人工规范。 | 本文研究如何把研究者定义的 topic / RQ / scope / meta-model 投影为可演化 dimension schema，并把字段级证据、统计观察、候选发现和最终裁决显式化。 | 不能声称替代 SLR/SMS 方法学。 | 🟢 |
| PRISMA 2020 / 透明报告 | 官方 / 种子证据 | 流程、检查清单、排除理由、透明报告。 | PRISMA 合规是高风险合规主张。 | 只生成类 PRISMA / 受 PRISMA 启发的透明材料；合规需完整检查清单和专家核验。 | 不能写 PRISMA 合规。 | 🟢 |
| ASReview | 官方 / Nature / GitHub 种子证据 | 主动学习 / ML 辅助题摘筛选。 | 证明综述自动化和筛选辅助早已有成熟工具。 | 本文不是只优化筛选排序，而是把筛选后的论文分析层落实为 approved dimension schema、field-level content evidence 和 finding adjudication。 | 不能写首次辅助筛选；不能说 ASReview 与自动化综述无关。 | 🟢 |
| RobotReviewer | PubMed / PMC / DOI / 官方种子证据 | 临床试验、偏倚风险评估、证据自动化。 | 证明特定证据自动化不是空白。 | 本文不是偏倚风险分类器，聚焦 SE SLR/SMS 中开放研究对象的字段级证据、统计观察和研究者裁决。 | 不能写已有工作没有证据自动化。 | 🟢 |
| AgentSLR / AI-based scientific knowledge synthesis evaluation harness | B0 全文文本级 review；图表待 PDF 核对 | 检索、题摘筛选、PDF-to-Markdown、全文筛选、参数 / 模型 / 暴发抽取、专家标注、分阶段评价、成本。 | 直接威胁“AI / 智能体执行 SLR 多阶段流程”和“评估智能体式 SLR 工作流”的主张。 | 不主张首次多阶段智能体式 SLR；本文差异落在 SE SLR/SMS 的 researcher-approved dimension schema、schema revision / backfill、字段级 content evidence、统计观察到 candidate finding signal 的转移和 final adjudication。 | 不能写智能体式 SLR 工作流 / 分阶段隔离评价是空白。 | 🟡 |
| LatteReview | B0 全文文本级 review；图表待 PDF 核对 | 多智能体筛选、相关性评分、结构化抽取、资深 reviewer 裁决、Pydantic 输出、成本 / 速度示例。 | 直接威胁“多智能体系统综述自动化”主张。 | 不以多智能体工作流为新颖性；强调 schema 版本、field evidence anchor、statistical-analysis-vs-finding 分层，以及 candidate finding 被研究者 challenge / downgrade / reject / accept 的状态机。 | 不能写首次多智能体 SLR 自动化。 | 🟡 |
| EviSearch | B0 全文文本级 review；图表待 PDF 核对 | 临床证据抽取、单元格级 value / reasoning / page / modality / quote provenance、reviewer edits。 | 直接威胁人在回路来源追溯、证据定位和审计主张。 | 承认单元格级 provenance 已有强近邻；本文把 provenance 放入 SE SLR/SMS 的 dimension schema、统计观察、candidate finding、反向证据与 final adjudication 链条。 | 不能声称人在回路来源追溯 / 证据归因是空白。 | 🟡 |
| LR-Robot | B0 全文文本级 review；图表待 PDF 核对 | 专家 taxonomy、LLM 分类、RAG 知识库、网络分析、人在回路评价。 | 威胁专家定义 taxonomy + LLM 批量分类 + 下游结构发现方向。 | 本文不只做 taxonomy 分类；dimension pattern 是可演化 schema，包含字段定义、证据要求、缺失值语义、schema revision、impact analysis 和 backfill。 | 不能写专家 taxonomy + LLM SLR 分类未被研究。 | 🟡 |
| TrialMind | B0 全文文本级 review；图表待 PDF 核对 | 临床检索、筛选 / 排序、数据抽取、标准化 meta-analysis 输入、森林图、人机协作。 | 威胁完整证据综合管线和人机协作主张。 | 避免 clinical PICO / 统计综合主线；聚焦 SE SLR/SMS 的开放证据对象、非标准字段、schema 演化、researcher challenge 与方法过程证据。 | 不能写完整证据综合管线为空白。 | 🟡 |
| WSESE@ICSE 2025 LLM-SLR difficulties | B0 全文文本级 review；workshop / PDF 已本地保存 | SE 中使用 LLM 进行 SLR 执行 / 复现的困难：prompt 敏感、随机性、模型漂移、成本、透明性、仓库缺口。 | 约束“SE 社区尚未讨论 LLM-SLR 风险”的主张。 | 把这些困难转成 S0-v2 的 process evidence、run record、redaction、challenge、schema revision 和透明性评价义务。 | 不能写 SE 社区尚未研究 LLM-assisted SLR difficulties。 | 🟢 |
| Beyond Accuracy / SE SLR screening variability | B0 全文文本级 review；图表待 PDF 核对 | 真实 SE SLR 筛选、12 个 LLM、重复运行、一致性、人工复核路由。 | 威胁筛选阶段准确率 / 稳定性主张。 | 将筛选风险纳入 L3 screening audit 和后续 process metrics，不把筛选 F1 当完整贡献。 | 不能写 LLM screening 变异性不是问题。 | 🟡 |
| Closed-loop scientific literature summarization | B0 全文文本级 review；图表待 PDF 核对 | 多智能体人机协作、数据抽取、置信度、人审、模型拟合、报告闭环。 | 威胁通用人在回路科学综述 / 报告闭环主张。 | 聚焦 SE SLR/SMS 的 researcher-defined meta-model、dimension pattern lifecycle、field evidence 和 final adjudication；报告只是透明投影。 | 不能写 human-in-the-loop literature summarization loop 是空白。 | 🟡 |
| Automated survey / literature review generation | B0 多篇全文文本级 review | 自动综述生成、引用图、rubric refinement、参考文献生成、LLM-as-Judge 评价。 | 威胁“自动生成综述文本 / survey”方向。 | 报告生成只是 accepted / downgraded / unresolved findings 的下游透明材料；本文关注 SLR/SMS 的字段证据、统计观察和研究者裁决。 | 不能把文本流畅度或引用质量当 SLR 方法学可靠性。 | 🟡 |
| General LLM-assisted screening / extraction / synthesis | B0 已建多个 P0/P1；仍需 A6 深化 | 筛选、抽取、摘要、结构化综合、prompt reproducibility。 | 证明局部环节已有大量近邻。 | 本文必须在 SE 场景中的 pattern evolution、field evidence、statistical/finding separation、human gate 和 process-evidence-based method evaluation 上差异化。 | 不能写 LLM screening / extraction / synthesis 从未用于综述。 | 🟡 |
| 本仓库 `sources/` 文库 | `main` 已有资产 | 控制系统 STM 领域资产。 | 若写成语料论文，会偏离第二篇主线。 | 仅作为真实案例、压力测试或证据来源。 | 不能写 `sources` 语料论文是主线。 | 🟢 |
| PR #97 baseline 文库 | OPEN / 快照证据 | related-work screening / fulltext extraction 线索。 | 若误写成 `main` 事实，会造成事实漂移。 | 必须按快照证据使用，不能升级为 `main` 事实。 | 不能写 PR #97 资产已合入。 | 🟣 |

## 3. 差异化主线压缩

PR-S0-v2 后，本文可尝试成立的差异化不再是“agent 也能做 SLR”，也不只是旧口径的“meta-model + evidence chain”。更安全的差异化组合是：

1. **研究者定义的 review meta-model**：使用本文方法的 researcher 明确 topic / RQ / scope / 核心对象 / 关系 / 证据类型；LLM/agent 只能建议，不能决定 operative meta-model。
2. **可演化 dimension schema**：把 meta-model 投影为树状/类型化、可版本化、可修订的 extraction schema；每次 revision 记录 change trigger、impact analysis、impacted papers 与 backfill 状态。
3. **字段级 content evidence**：每个字段值、统计输入和 target-domain finding 都必须回到目标论文中的 source anchor、quote、table、artifact URL、missing/uncertainty。
4. **statistical analysis / research finding 分层**：统计分析只产生 frequency、distribution、cross-tab、trend、coverage proxy、contradiction signal 等统计观察；agent 输出只是 candidate finding signal。
5. **researcher challenge / final adjudication**：candidate signal 必须经过证据、反例、范围、主张强度和 schema 适配性的研究者质疑，才能被接受、降级、拒绝或标为 unresolved。
6. **process evidence 支撑 method evaluation**：pilot 和硕士生 human-LLM interaction logs 用于评价方法可用性、审计性、成本和失败模式，不支撑目标领域 findings。
7. **SE SLR/SMS 场景约束**：上述机制落在 SE / LLM4Modeling / MDE 等软件工程综述场景中，而不是泛医学、金融或通用 survey generation。

这组差异化必须正面对齐 B0 中的强近邻：AgentSLR 与 LatteReview 已经覆盖多阶段 workflow；EviSearch 已经覆盖单元格级 provenance；LR-Robot 已经覆盖专家 taxonomy + LLM 分类；TrialMind 已经覆盖临床 evidence synthesis；WSESE@ICSE 2025 已经讨论 SE LLM-SLR 风险。因此本文的 safe novelty 应落在“研究者定义 schema 如何演化、字段证据如何进入统计观察、统计观察如何通过人类质疑变成 finding、过程证据如何评价方法”这一组合上。

## 4. 最低相关工作门槛

后续任何 story / outline / manuscript 若要写新颖性，必须至少回答：

1. 为什么本文不是首次自动化 SLR / 首次智能体式 SLR，而是研究者引导、模式演化、证据支撑、发现导向的支持方法？
2. 与 AgentSLR 的分阶段隔离评价和专家参考答案有什么差别？
3. 与 LatteReview 的多智能体筛选 / 抽取工作流有什么差别？
4. 与 EviSearch 的单元格级来源追溯 / 人在回路审计有什么差别？
5. 与 LR-Robot 的专家 taxonomy + LLM 分类 + 下游结构发现有什么差别？（这里保留 `taxonomy` 作为论文名词锚点。）
6. 与 TrialMind 的临床证据综合管线有什么差别？
7. 与 WSESE@ICSE 2025 的 SE LLM-SLR difficulties 讨论如何衔接，并把 prompt 敏感性、随机性、透明性转成 process evidence 与评价义务？
8. 与综述生成 / 自动化文献综述生成的差别是什么？
9. 本文为什么只写类 PRISMA，并禁止写 PRISMA 合规？
10. `sources/` 和 PR #97 是证据来源还是论文主贡献？

## 5. 禁止的新颖性写法

- 禁止写 first automated SLR / first agentic SLR / first LLM-based systematic review（首次类强主张）。
- 禁止写已有工作只做人工综述、没有自动化。
- 禁止写已有工作没有 multi-agent SLR workflow、HITL、provenance、screening / extraction 或 evidence synthesis。
- 禁止写 ASReview / RobotReviewer / AgentSLR / LatteReview / EviSearch / LR-Robot / TrialMind 与本文无关。
- 禁止写 PRISMA 合规。
- 禁止把 PR #97 OPEN / 未合入快照当成已合入数据集。
- 禁止把自动综述生成或综述写作作为本文核心贡献。

## 6. 后续待补

A6 或相关 related-work PR 应继续补：

1. 对 B0 P0/P1 的 PDF 图表核对和制品审计。
2. 对全 CCF A/B/C 检索中 IST / TOSEM / CHI / TKDD / ACL / EMNLP / JAMIA 等正式 venue 线索的全文复核。
3. 对证据综合中的人在回路、来源追溯和可审计性做更系统定位。
4. survey-of-surveys 对 SE / AI4SE / MDE / LLM4SE survey 的 RQ、taxonomy、研究发现模式和证据 schema 抽取；这些英文保留为后续英文稿术语锚点。
