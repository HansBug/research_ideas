# 差异化新颖性矩阵：PR-S0 相关工作边界

## 1. 目的

关键词覆盖：系统综述自动化（systematic review automation）、智能体式 SLR（agentic SLR）、LLM 辅助筛选 / 抽取 / 综合、综述生成、人在回路证据综合、provenance / auditability。

本文件冻结 PR-S0 阶段的差异化新颖性门槛。它不是完整 Related Work，也不声称已经排除所有 direct competitor；它用于防止第二篇论文误写成 first automated SLR、first agentic SLR、PRISMA-compliant 工具、自动 survey generation paper 或 `sources/` corpus paper。

PR-B0 已完成 35 篇本地全文文本级 baseline review 与全 CCF A/B/C 扩展 discovery。后续 story 不能继续写“待 A1 才知道是否有强近邻”；当前已知事实是：多智能体 SLR、clinical evidence synthesis、HITL provenance、screening / extraction、survey generation 和 SE LLM-SLR 方法学风险都已有强近邻。本文差异化不能再用“无人自动综述”来表述，而必须显式体现 researcher-guided 与 finding lifecycle。

## 2. 矩阵口径

状态口径：🟢 = PR-S0 可作为已核验证据锚点使用；🟡 = B0 已登记但仍需后续 PDF / artifact / citation 深化；🟣 = PR #97 OPEN / 未合入 / snapshot / branch-local evidence。

| 方向 / 工具 | B0 证据等级 | 覆盖环节 / 能力 | 对本文的新颖性威胁 | 本文安全差异 | 禁止主张 | 状态 |
|---|---|---|---|---|---|---:|
| 软件工程 SLR / SMS 方法学 | citation seed / 方法学基础 | 协议、search、screening、extraction、synthesis、reporting、threats。 | 本文不能替代 SLR 方法学，也不能忽略人工规范。 | 本文研究如何把 researcher frame、finding pattern、evidence chain 和 challenge loop 智能体化。 | 不能声称替代 SLR/SMS 方法学。 | 🟢 |
| PRISMA 2020 / 透明报告 | official / seed | flow、checklist、排除理由、透明报告。 | PRISMA-compliant 是高风险合规主张。 | 只生成 PRISMA-style / PRISMA-informed 材料，合规需 checklist 和专家核验。 | 不能写 PRISMA-compliant。 | 🟢 |
| ASReview | official / Nature / GitHub seed | 主动学习 / ML 辅助 title-abstract screening。 | 证明 review automation 和筛选辅助早已有成熟工具。 | 本文不是只优化 screening 排序，而是 finding-centered evidence chain 与 challenge loop。 | 不能写首次辅助筛选；不能说 ASReview 与自动化综述无关。 | 🟢 |
| RobotReviewer | PubMed / PMC / DOI / official seed | clinical trials / risk-of-bias / evidence automation。 | 证明特定证据自动化不是空白。 | 本文不是 risk-of-bias 分类器，聚焦 SE SLR/SMS finding audit。 | 不能写 prior work 没有证据自动化。 | 🟢 |
| AgentSLR / AI-based scientific knowledge synthesis evaluation harness | B0 全文文本级 review；图表待 PDF 核对 | 检索、题摘筛选、PDF-to-Markdown、全文筛选、参数 / 模型 / 暴发抽取、专家标注、分阶段评价、成本。 | 直接威胁“AI / agent 执行 SLR 多阶段流程”和“评估 agentic SLR workflow”的主张。 | 不主张首次多阶段 agentic SLR；本文差异落在 SE SLR/SMS、researcher-defined review meta-model、finding lifecycle 和 challenge log。 | 不能写 agentic SLR workflow / stage-isolated evaluation 是空白。 | 🟡 |
| LatteReview | B0 全文文本级 review；图表待 PDF 核对 | 多智能体 screening、relevance scoring、structured extraction、senior reviewer 裁决、Pydantic 输出、成本 / 速度示例。 | 直接威胁“multi-agent systematic review automation”claim。 | 不以多智能体 workflow 为 novelty；强调 candidate finding 的证据、反证、scope、claim strength 和 final decision。 | 不能写 first multi-agent SLR automation。 | 🟡 |
| EviSearch | B0 全文文本级 review；图表待 PDF 核对 | clinical evidence extraction、per-cell value / reasoning / page / modality / quote provenance、reviewer edits。 | 直接威胁 HITL provenance / evidence locator / audit claim。 | 从 cell-level extraction provenance 转向 SE review finding-level claim-to-source、counter-evidence 与 challenge revision。 | 不能声称 HITL provenance / evidence attribution 是空白。 | 🟡 |
| LR-Robot | B0 全文文本级 review；图表待 PDF 核对 | expert taxonomy、LLM classification、RAG knowledge base、network analysis、human-in-the-loop evaluation。 | 威胁 expert-defined taxonomy + LLM 批量分类 + finding / structure discovery 方向。 | meta-model 不只服务分类，还约束 finding patterns、candidate findings 和 challenge loop。 | 不能写 expert taxonomy + LLM SLR classification 未被研究。 | 🟡 |
| TrialMind | B0 全文文本级 review；图表待 PDF 核对 | clinical search、screening / ranking、data extraction、standardized meta-analysis inputs、forest plots、human-AI collaboration。 | 威胁 complete evidence synthesis pipeline 和 human-AI collaboration claim。 | 避免 clinical PICO / 统计综合主线，强调 SE SLR/SMS 开放证据对象与 finding audit。 | 不能写完整 evidence synthesis pipeline 为空白。 | 🟡 |
| WSESE@ICSE 2025 LLM-SLR difficulties | B0 全文文本级 review；workshop / PDF 已本地保存 | SE 中使用 LLM 进行 SLR conducting / replication 的困难：prompt 敏感、随机性、模型漂移、成本、透明性、仓库缺口。 | 约束“SE 社区尚未讨论 LLM-SLR 风险”的 claim。 | 把这些困难转成 PR-S0 的 audit / run record / challenge / transparency obligations。 | 不能写 SE 社区尚未研究 LLM-assisted SLR difficulties。 | 🟢 |
| Beyond Accuracy / SE SLR screening variability | B0 全文文本级 review；图表待 PDF 核对 | 真实 SE SLR screening、12 个 LLM、重复运行、一致性、人工复核路由。 | 威胁 screening 阶段准确率 / 稳定性 claim。 | 将 screening 风险纳入 finding evidence chain 与 challenge protocol，不把 F1 当完整贡献。 | 不能写 LLM screening 变异性不是问题。 | 🟡 |
| Closed-loop scientific literature summarization | B0 全文文本级 review；图表待 PDF 核对 | multi-agent human-LLM collaboration、数据抽取、置信度、人审、模型拟合、报告闭环。 | 威胁 generic human-in-the-loop scientific review / report loop。 | 聚焦 SE SLR/SMS 的 researcher-instantiated review meta-model 与 finding-oriented audit。 | 不能写 human-in-the-loop literature summarization loop 是空白。 | 🟡 |
| Automated survey / literature review generation | B0 多篇全文文本级 review | 自动 survey generation、citation graph、rubric refinement、reference generation、LLM-as-Judge 评价。 | 威胁“自动生成综述文本 / survey”方向。 | 报告生成只是 accepted / downgraded / unresolved findings 的下游投影；本文关注 SLR/SMS evidence workflow。 | 不能把文本流畅度或引用质量当 SLR 方法学可靠性。 | 🟡 |
| General LLM-assisted screening / extraction / synthesis | B0 已建多个 P0/P1；仍需 A6 深化 | 筛选、抽取、摘要、结构化综合、prompt reproducibility。 | 证明局部环节已有大量近邻。 | 本文必须在 finding-centered audit、researcher challenge 和 SE 场景上差异化。 | 不能写 LLM screening / extraction / synthesis 从未用于综述。 | 🟡 |
| 本仓库 `sources/` 文库 | main 已有资产 | 控制系统 STM domain asset。 | 若写成 corpus paper，会偏离第二篇主线。 | 仅作为真实 case / stress test / evidence source。 | 不能写 `sources` corpus paper 是主线。 | 🟢 |
| PR #97 baseline 文库 | OPEN / snapshot evidence | related-work screening / fulltext extraction 线索。 | 若误写成 main fact，会造成事实漂移。 | 必须按 snapshot evidence 使用，不能升级为 `main` fact。 | 不能写 PR #97 资产已合入。 | 🟣 |

## 3. 差异化主线压缩

PR-S0 后，本文可尝试成立的差异化不再是“agent 也能做 SLR”，而是以下组合是否能被后续 A2/A3/A5/A6 证据支撑：

1. **Researcher-guided / researcher-instantiated review meta-model scaffold**：让使用该 work 的 researcher 先显式化 review frame，而不是作者预设一套 universal SE ontology，也不是 LLM 自动决定 schema；researcher 还要亲自裁剪、实例化和批准。
2. **研究发现模式脚手架（Finding pattern scaffold）**：把 SLR 的 research finding 功能结构化为 topic gap、method gap、evidence gap、contradiction、trend、consensus、taxonomy、maturity、transferability 等候选 pattern。
3. **以研究发现为中心的证据链（Finding-centered evidence chain）**：每个 candidate finding 必须回到 evidence objects、source anchors、supporting / counter evidence、uncertainty、scope 和 claim strength。
4. **Researcher challenge loop**：researcher 可以质疑 finding，系统补证、找反例、修订、降级或标 unresolved，并留下 challenge log；最终接受仍由 researcher 作出 final finding 决策。
5. **SE SLR/SMS 场景约束**：把上述机制落到 SE / LLM4Modeling / MDE 等软件工程综述场景，而不是泛医学 / 金融 / 材料科学 evidence synthesis。

## 4. 最低相关工作门槛

后续任何 story / outline / manuscript 若要写 novelty，必须至少回答：

1. 为什么本文不是 first automated SLR / first agentic SLR，而是研究者引导 / 发现导向 / 可审计的支持工作流？
2. 与 AgentSLR 的 stage-isolated evaluation 和 expert reference 有什么差别？
3. 与 LatteReview 的 multi-agent screening / extraction workflow 有什么差别？
4. 与 EviSearch 的 per-cell provenance / HITL audit 有什么差别？
5. 与 LR-Robot 的 expert taxonomy + LLM classification + downstream structure discovery 有什么差别？（这里保留英文术语作为论文名词锚点。）
6. 与 TrialMind 的 clinical evidence synthesis pipeline 有什么差别？
7. 与 WSESE@ICSE 2025 的 SE LLM-SLR difficulties 讨论如何衔接？
8. 与 survey generation / automated literature review generation 的差别是什么？
9. 本文为什么只写 PRISMA-style，并禁止写 PRISMA-compliant？
10. `sources/` 和 PR #97 是 evidence source 还是论文主贡献？

## 5. 禁止的新颖性写法

- 禁止写 first automated SLR / first agentic SLR / first LLM-based systematic review（首次类强主张）。
- 禁止写 prior work 只做人工综述、没有自动化。
- 禁止写已有工作没有 multi-agent SLR workflow、HITL、provenance、screening / extraction 或 evidence synthesis。
- 禁止写 ASReview / RobotReviewer / AgentSLR / LatteReview / EviSearch / LR-Robot / TrialMind 与本文无关。
- 禁止写 PRISMA-compliant。
- 禁止把 PR #97 OPEN / 未合入 snapshot 当成已合入 dataset。
- 禁止把 automated survey generation 或 review writing 作为本文核心 contribution。

## 6. 后续待补

A6 或相关 related-work PR 应继续补：

1. 对 B0 P0/P1 的 PDF 图表核对和 artifact audit。
2. 对全 CCF A/B/C discovery 中 IST / TOSEM / CHI / TKDD / ACL / EMNLP / JAMIA 等正式 venue 线索的全文复核。
3. Human-in-the-loop / provenance / auditability for evidence synthesis 的更系统定位。
4. survey-of-surveys 对 SE / AI4SE / MDE / LLM4SE survey 的 RQ、taxonomy、finding pattern 和 evidence schema 抽取；这些英文保留为后续英文稿术语锚点。
