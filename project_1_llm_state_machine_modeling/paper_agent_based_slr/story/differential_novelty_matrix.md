# 差异化新颖性矩阵：PR-S0 相关工作边界

## 1. 目的

关键词覆盖：系统综述自动化（systematic review automation）、智能体式 SLR（agentic SLR）、LLM 辅助筛选 / 抽取 / 综合、综述生成、人在回路证据综合、来源追溯（provenance）与可审计性（auditability）。

本文件冻结 PR-S0 阶段的差异化新颖性门槛。它不是完整 Related Work，也不声称已经排除所有直接竞争工作；它用于防止第二篇论文误写成首次自动化 SLR、首次智能体式 SLR、PRISMA 合规工具、自动综述生成论文或 `sources/` 语料论文。

PR-B0 已完成 35 篇本地全文文本级基线 review 与全 CCF A/B/C 扩展检索。后续 story 不能继续写“待 A1 才知道是否有强近邻”；当前已知事实是：多智能体 SLR、临床证据综合、人在回路来源追溯、筛选 / 抽取、综述生成和 SE LLM-SLR 方法学风险都已有强近邻。本文差异化不能再用“无人自动综述”来表述，而必须显式体现研究者引导与研究发现生命周期。

## 2. 矩阵口径

状态口径：🟢 = PR-S0 可作为已核验证据锚点使用；🟡 = B0 已登记但仍需后续 PDF / 制品 / 引用深化；🟣 = PR #97 OPEN / 未合入 / 快照 / 分支局部证据。

| 方向 / 工具 | B0 证据等级 | 覆盖环节 / 能力 | 对本文的新颖性威胁 | 本文安全差异 | 禁止主张 | 状态 |
|---|---|---|---|---|---|---:|
| 软件工程 SLR / SMS 方法学 | 引用种子 / 方法学基础 | 协议、检索、筛选、抽取、综合、报告和效度威胁。 | 本文不能替代 SLR 方法学，也不能忽略人工规范。 | 本文研究如何把研究者综述框架、研究发现模式、证据链和质疑闭环智能体化。 | 不能声称替代 SLR/SMS 方法学。 | 🟢 |
| PRISMA 2020 / 透明报告 | 官方 / 种子证据 | 流程、检查清单、排除理由、透明报告。 | PRISMA 合规是高风险合规主张。 | 只生成类 PRISMA / 受 PRISMA 启发的材料，合规需检查清单和专家核验。 | 不能写 PRISMA 合规。 | 🟢 |
| ASReview | 官方 / Nature / GitHub 种子证据 | 主动学习 / ML 辅助题摘筛选。 | 证明综述自动化和筛选辅助早已有成熟工具。 | 本文不是只优化筛选排序，而是研究发现级证据链与质疑闭环。 | 不能写首次辅助筛选；不能说 ASReview 与自动化综述无关。 | 🟢 |
| RobotReviewer | PubMed / PMC / DOI / 官方种子证据 | 临床试验、偏倚风险评估、证据自动化。 | 证明特定证据自动化不是空白。 | 本文不是偏倚风险分类器，聚焦 SE SLR/SMS 的研究发现审计。 | 不能写已有工作没有证据自动化。 | 🟢 |
| AgentSLR / AI-based scientific knowledge synthesis evaluation harness | B0 全文文本级 review；图表待 PDF 核对 | 检索、题摘筛选、PDF-to-Markdown、全文筛选、参数 / 模型 / 暴发抽取、专家标注、分阶段评价、成本。 | 直接威胁“AI / 智能体执行 SLR 多阶段流程”和“评估智能体式 SLR 工作流”的主张。 | 不主张首次多阶段智能体式 SLR；本文差异落在 SE SLR/SMS、研究者定义的综述元模型、研究发现生命周期和质疑日志。 | 不能写智能体式 SLR 工作流 / 分阶段隔离评价是空白。 | 🟡 |
| LatteReview | B0 全文文本级 review；图表待 PDF 核对 | 多智能体筛选、相关性评分、结构化抽取、资深 reviewer 裁决、Pydantic 输出、成本 / 速度示例。 | 直接威胁“多智能体系统综述自动化”主张。 | 不以多智能体工作流为新颖性；强调候选研究发现的证据、反证、范围、主张强度和最终决策。 | 不能写首次多智能体 SLR 自动化。 | 🟡 |
| EviSearch | B0 全文文本级 review；图表待 PDF 核对 | 临床证据抽取、单元格级 value / reasoning / page / modality / quote provenance、reviewer edits。 | 直接威胁人在回路来源追溯、证据定位和审计主张。 | 从单元格级抽取来源追溯转向 SE review 的研究发现级主张到来源、反向证据与质疑修订。 | 不能声称人在回路来源追溯 / 证据归因是空白。 | 🟡 |
| LR-Robot | B0 全文文本级 review；图表待 PDF 核对 | 专家 taxonomy、LLM 分类、RAG 知识库、网络分析、人在回路评价。 | 威胁专家定义 taxonomy + LLM 批量分类 + 下游结构发现方向。 | 元模型不只服务分类，还约束研究发现模式、候选研究发现和质疑闭环。 | 不能写专家 taxonomy + LLM SLR 分类未被研究。 | 🟡 |
| TrialMind | B0 全文文本级 review；图表待 PDF 核对 | 临床检索、筛选 / 排序、数据抽取、标准化 meta-analysis 输入、森林图、人机协作。 | 威胁完整证据综合管线和人机协作主张。 | 避免 clinical PICO / 统计综合主线，强调 SE SLR/SMS 的开放证据对象与研究发现审计。 | 不能写完整证据综合管线为空白。 | 🟡 |
| WSESE@ICSE 2025 LLM-SLR difficulties | B0 全文文本级 review；workshop / PDF 已本地保存 | SE 中使用 LLM 进行 SLR 执行 / 复现的困难：prompt 敏感、随机性、模型漂移、成本、透明性、仓库缺口。 | 约束“SE 社区尚未讨论 LLM-SLR 风险”的主张。 | 把这些困难转成 PR-S0 的审计、运行记录、质疑和透明性义务。 | 不能写 SE 社区尚未研究 LLM-assisted SLR difficulties。 | 🟢 |
| Beyond Accuracy / SE SLR screening variability | B0 全文文本级 review；图表待 PDF 核对 | 真实 SE SLR 筛选、12 个 LLM、重复运行、一致性、人工复核路由。 | 威胁筛选阶段准确率 / 稳定性主张。 | 将筛选风险纳入研究发现证据链与质疑协议，不把 F1 当完整贡献。 | 不能写 LLM screening 变异性不是问题。 | 🟡 |
| Closed-loop scientific literature summarization | B0 全文文本级 review；图表待 PDF 核对 | 多智能体人机协作、数据抽取、置信度、人审、模型拟合、报告闭环。 | 威胁通用人在回路科学综述 / 报告闭环主张。 | 聚焦 SE SLR/SMS 的研究者实例化综述元模型与发现导向审计。 | 不能写 human-in-the-loop literature summarization loop 是空白。 | 🟡 |
| Automated survey / literature review generation | B0 多篇全文文本级 review | 自动综述生成、引用图、rubric refinement、参考文献生成、LLM-as-Judge 评价。 | 威胁“自动生成综述文本 / survey”方向。 | 报告生成只是已接受 / 已降级 / 未解决研究发现的下游投影；本文关注 SLR/SMS 证据工作流。 | 不能把文本流畅度或引用质量当 SLR 方法学可靠性。 | 🟡 |
| General LLM-assisted screening / extraction / synthesis | B0 已建多个 P0/P1；仍需 A6 深化 | 筛选、抽取、摘要、结构化综合、prompt reproducibility。 | 证明局部环节已有大量近邻。 | 本文必须在研究发现级审计、研究者质疑和 SE 场景上差异化。 | 不能写 LLM screening / extraction / synthesis 从未用于综述。 | 🟡 |
| 本仓库 `sources/` 文库 | `main` 已有资产 | 控制系统 STM 领域资产。 | 若写成语料论文，会偏离第二篇主线。 | 仅作为真实案例、压力测试或证据来源。 | 不能写 `sources` 语料论文是主线。 | 🟢 |
| PR #97 baseline 文库 | OPEN / 快照证据 | related-work screening / fulltext extraction 线索。 | 若误写成 `main` 事实，会造成事实漂移。 | 必须按快照证据使用，不能升级为 `main` 事实。 | 不能写 PR #97 资产已合入。 | 🟣 |

## 3. 差异化主线压缩

PR-S0 后，本文可尝试成立的差异化不再是“agent 也能做 SLR”，而是以下组合是否能被后续 A2/A3/A5/A6 证据支撑：

1. **研究者引导 / 研究者实例化的综述元模型脚手架（researcher-guided / researcher-instantiated review meta-model scaffold）**：让使用本文方法的研究者先显式化综述框架，而不是作者预设一套通用软件工程本体，也不是 LLM 自动决定 schema；研究者还要亲自裁剪、实例化和批准。
2. **研究发现模式脚手架（finding pattern scaffold）**：把 SLR 的研究发现功能结构化为主题缺口、方法缺口、证据缺口、矛盾、趋势、共识、taxonomy、成熟度、可迁移性等候选模式。
3. **以研究发现为中心的证据链（finding-centered evidence chain）**：每个候选研究发现必须回到证据对象、来源锚点、支持性 / 反向证据、不确定性、适用范围和主张强度。
4. **研究者质疑闭环（researcher challenge loop）**：研究者可以质疑研究发现，系统补证、找反例、修订、降级或标为未解决，并留下质疑日志；最终接受仍由研究者作出最终研究发现决策。
5. **SE SLR/SMS 场景约束**：把上述机制落到 SE / LLM4Modeling / MDE 等软件工程综述场景，而不是泛医学、金融或材料科学证据综合。

## 4. 最低相关工作门槛

后续任何 story / outline / manuscript 若要写新颖性，必须至少回答：

1. 为什么本文不是首次自动化 SLR / 首次智能体式 SLR，而是研究者引导、发现导向、可审计的支持工作流？
2. 与 AgentSLR 的分阶段隔离评价和专家参考答案有什么差别？
3. 与 LatteReview 的多智能体筛选 / 抽取工作流有什么差别？
4. 与 EviSearch 的单元格级来源追溯 / 人在回路审计有什么差别？
5. 与 LR-Robot 的专家 taxonomy + LLM 分类 + 下游结构发现有什么差别？（这里保留 `taxonomy` 作为论文名词锚点。）
6. 与 TrialMind 的临床证据综合管线有什么差别？
7. 与 WSESE@ICSE 2025 的 SE LLM-SLR difficulties 讨论如何衔接？
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
