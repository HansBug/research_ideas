# Patience is all you need! An agentic system for performing scientific literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Patience is all you need! An agentic system for performing scientific literature review |
| 年份 | 2025，arXiv:2504.08752 |
| 作者 / venue / 出版状态 | David Brett、Anniek Myatt；arXiv:2504.08752; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 近邻强度备注 | agentic retrieval / 来源归因 强近邻；因不覆盖 SLR/SMS 报告生成、抽取编码和人审协议，SUMMARY 保持 P2。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | `bibtex.bib`；`paper_content.txt` Page 1--10；已清理 PDF 提取残留 NUL 后阅读 |
| 研究脉络 | 文献综述的检索、组织与来源归因 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 生物医学开放文献库 PubMed/PubMed Central；用户科学问题；NER 识别的 genes/diseases；LLM 生成的搜索词、同义词和候选答案 |
| 输出 | 带来源归因的问答/长文回答；用于 review generation 的扩展问题和更广文献覆盖；benchmark recall/accuracy/coverage/precision |
| 方法/系统形态 | Claude 3.5 Sonnet + Elasticsearch + HunFlair/TrendyGenes + BM25L + reciprocal rank fusion + CoVe 的 agentic retrieval/distillation 系统 |
| 覆盖阶段 | 文献检索、chunk re-ranking、信息抽取/摘要、去重、答案生成、Chain-of-Verification 扩展；未覆盖正式 SLR 的筛选、编码、报告写作 |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 有 来源归因、CoVe fact-checking 和 benchmark source recall；无人工审计 gate 或 claim-level 审计包 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 来源归因/source recall 级；无人工审计 gate 或 claim ledger。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | LitQA2、PubMedQA 子集、10 篇 Nature review reference recall；报告 source article recall、key passage recall、accuracy/coverage/precision、CoVe reference coverage |
| 模型/API 设置 | Claude、Sonnet；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 重复；正式复现前需回原文核对 |
| 主要发现 | sparse retrieval + LLM query expansion 可接近 PaperQA2 水平；LitQA2 中最终 available subset workflow accuracy 60.4%、precision 90.3%；CoVe 将 Nature review primary+secondary reference mean coverage 从 6% 提升到 25% |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强烈提醒 paper2：检索覆盖和 来源归因 是核心 evidence 风险；但该文不是 SLR/SMS 报告生成或编码综合系统 |
| 受影响主张 ID | C3,C5,C6 |
| 威胁类型 | 负面证据 + 背景定位 |
| 威胁的 paper2 主张 | 强烈提醒 paper2：检索覆盖和 来源归因 是核心 evidence 风险；但该文不是 SLR/SMS 报告生成或编码综合系统 |
| 支持的 paper2 主张 | 支持 paper2 把 retrieval coverage、来源归因 和长尾文献遗漏作为 evidence workflow 的关键风险。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 |
| 代码状态 | 未提及源码入口；本轮不得写成 code 可用 |
| 数据状态 | 未提及公开数据包；依赖 PubMed/PubMed Central OA 与 Nature reviews 样例，license 待核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| 维度 | 评分 |
|---|---|
| D1 主题贴合度 | 🟢 |
| D2 SLR/SMS 流程覆盖度 | 🟡 |
| D3 LLM/agent 自动化深度 | 🟢 |
| D4 人工审计与可追踪性 | 🟡 |
| D5 评价严谨性 | 🟢 |
| D6 SE / CCF 相关性 | 🟠 |
| D7 对本文 novelty 的威胁强度 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---|---|---|
| D1 | 🟢 | `paper_content.txt` Page 1 摘要；Page 2 “literature review generation” | 直接处理 scientific literature review 中的检索、信息蒸馏、来源归因和覆盖扩展，主题贴合度高。 |
| D2 | 🟡 | Page 3 Methodology；Page 4--5 Results | 覆盖检索、re-ranking、抽取摘要、verification/diversification，但没有 SLR/SMS 的筛选标准、数据抽取表、编码、综合报告结构。 |
| D3 | 🟢 | Page 2 agentic system definition；Page 3 retrieval steps | 多个 LLM-augmented agents 串联，含 NER agent、search terms agent、document retrieval agent、re-ranking 和 CoVe，自动化深度强。 |
| D4 | 🟡 | Page 1 来源归因s；Page 4 CoVe；Tables 1--3 | 有来源归因、source article recall 和 CoVe 验证扩展，可追踪到论文/段落；但没有人类 audit、claim-to-source table 或可复查运行包。 |
| D5 | 🟢 | Page 4--5 Tables 1--3；Appendix analysis | 有公开 benchmark、baseline、置信区间、重复运行和 Nature review reference recall，实证严谨性在本批中较强。 |
| D6 | 🟠 | `bibtex.bib` primaryClass cs.IR；Page 1 biomedical domain | arXiv 预印本，主要在 biomedical literature QA/review；对 SE/CCF 只提供方法背景。 |
| D7 | 🟡 | Page 2--3 method；Page 5 discussion | 威胁 paper2 的检索覆盖、来源归因 和 verification/diversification claim，但不覆盖 agent-based SLR 端到端报告、人工审计 gate 或 run record。 |

## 3. 论文解决的问题与背景

论文认为 raw LLM 在专家级科学问题上容易失败，尤其当答案依赖全文上下文和具体来源归因时。作者强调，领域专家只有在答案带文献引用时才会信任系统；而当前 benchmark 如 PubMedQA、LitQA2 多为单篇或多选问答，无法衡量长文 review generation 所需的广泛文献覆盖。

因此论文问题不是“自动写一篇 survey”，而是“如何为科学 literature review 生成更可靠的检索、信息抽取、来源归因和 coverage expansion”。这个定位非常接近 paper2 的 evidence-chain 问题，但仍停留在生物医学 QA 和 review-support，而不是完整 SLR/SMS 方法学。

## 4. 方法 / 系统拆解

系统使用 PubMed titles/abstracts 与 PubMed Central open access full text。索引阶段对 PubMed citation 做 gene/disease NER，并用 TrendyGenes 处理 gene 命名歧义；对 PubMed Central full text 用 HunFlair 做 NER，每篇文章按 section/sub-document 索引到 Elasticsearch。

检索阶段包括四步。第一，NER agent 识别问题中的 gene/disease。第二，Search terms agent 让 LLM 生成 must/should keyword terms、boost 等级和同义词。第三，Document retrieval agent 用搜索模板查询 Elasticsearch，并 boost 新近文章。第四，Re-ranking agent 先把 section 切成约 10000 词 chunk、250 词 overlap；再让 LLM 生成三个多样化候选答案及 rationale 和 synonyms，用这些文本与原问题通过 BM25L 排序，并用 reciprocal rank fusion 合并 rank，从而选出进入抽取的 chunk。

信息抽取阶段先对每个 article chunk 生成与问题相关的 facts summary，若无相关 facts 则拒绝；可选第二阶段对每 3 篇摘要去重；最终把剩余摘要放入 LLM context 生成答案。Verification/diversification 使用 Chain-of-Verification：从 draft response 中规划约 10 个关键 statement，转成验证问题，再用新增检索与回答生成 final response。作者观察这些验证问题会扩大文献覆盖。

## 5. 实验 / 评价设计

实验分为三类。第一类检索实验：在 LitQA2 可机器读取的 PubMed Central OA 子集上，只找到 103/199 个 source articles；在 PubMedQA 上取前 200 个 labeled questions。评价 source documents 在 top 200 search results 中的位置，并与 More Like This TF-IDF baseline 对比。

第二类 re-ranking 和 QA 实验：LitQA2 有 key passage，作者看 key passage 在 chunk ranking 中的位置；同时按 LitQA2 的 Accuracy、Coverage、Precision 评价 QA。Table 1 分析 source article recall 在 LLM keyword retrieval、top 30 chunks、summarisation/retention、final attribution 之间的损失。Table 2 比较不同上下文粒度和 PaperQA2。

第三类 CoVe 文献覆盖实验：选取 10 篇 Nature review articles，由摘要生成起始问题，并以 review references 为 benchmark，比较 initial recall 与 CoVe recall，包含 primary references 和 secondary references。

## 6. 主要结果与结论

检索结果显示，LitQA2 中 LLM generated keyword approach 在 top 200 内找到 63.6±1.2 个 source articles（可用总数 103），简单 TF-IDF 为 52。PubMedQA 200 个问题中找到 154 个 source articles。re-ranking 方面，前 30 个 chunks 可覆盖约 83% key passages，而 baseline 需要约 900 chunks。

Table 1 显示 LitQA2 source article recall 从 top 200 retrieval 的 61.7±1.2%，经过 top 30 chunks 57.3±1.9%、summarisation 57.0±2.4%，到 final attribution 50.5±0.8%。Table 2 显示 full agentic workflow 在 available subset 上 Accuracy 0.604±0.006、Coverage 0.668±0.007、Precision 0.903±0.019；PaperQA2 all 为 0.66/0.78/0.852。作者解释 Claude 3.5 Sonnet 更保守，可能降低 coverage 但提升 precision。

Table 3 和 discussion 报告 CoVe 在 10 篇 Nature review 上将 primary+secondary reference mean coverage 从 6% 提升到 25%。结论是 sparse retrieval 配合 LLM query expansion 可在不使用 dense retrieval 和 citation network 的情况下达到接近 SOTA 的检索/归因能力，并能通过 CoVe 扩展 review generation 的相关文献覆盖。

## 7. 局限与可复现性

论文的证据链比一般 survey 生成 论文更实：有 benchmark、baseline、置信区间、重复次数和附录例子。但可复现仍受限制：没有在正文给出代码/数据链接；PubMed Central OA 只覆盖 LitQA2 的一部分；商业或受版权限制文献不能机器读取；系统依赖 Claude 3.5 Sonnet 和特定 biomedical NER/Elasticsearch pipeline。

方法局限包括：多选 QA benchmark 不能充分代表真实长文 literature review；source specificity 假设在实验中被发现不总成立；文献 coverage benchmark 依赖 Nature review 作者引用集合，而这些集合本身有作者知识和 affiliation bias；系统没有正式人工审核流程，也没有把最终长文 claim 逐条绑定到 source evidence。

## 8. 对 paper2 story / 实验设计的影响

这篇文献对 paper2 的最大影响是强调“检索召回是 evidence workflow 的第一瓶颈”。如果检索阶段漏掉 source paper，后续 LLM 抽取、编码和综合再强也无法恢复证据。因此 paper2 的实验应显式报告 retrieval candidate coverage、screening false negative、来源归因 precision/coverage，以及 verification/secondary-query 是否能扩展文献覆盖。

同时，它也提示 paper2 不应把 citation network 或 dense retrieval 当成唯一方案。Patience 证明 sparse retrieval + LLM query expansion + long-context chunk reranking 可以是强 baseline。paper2 若面向 SE/LLM4SE/SMS，需要说明自己的 retrieval stack、query expansion、人工审计 gate 和 eligibility filter 如何处理 coverage 风险。

## 9. 可用于写作的引用角度

1. Patience 可用于说明 scientific literature review automation 的关键瓶颈不只是生成，而是全文检索、来源归因 和 coverage expansion。
2. 该文通过 LitQA2 和 PubMedQA 表明，初始检索阶段造成最大 recall 损失，这支持 paper2 把检索证据链纳入 run record。
3. CoVe 扩展 review references 的结果可作为“verification questions can broaden evidence coverage”的相关工作，但不能写成已经解决 SLR 综合。
4. 与 paper2 的差异是：Patience 支持 question answering/review support，paper2 应覆盖 SLR/SMS 的筛选、抽取、编码、综合、报告与人工审计闭环。

## 10. 待复核清单

- 未人工打开 PDF 图表；Figure 2--5 曲线如需精确引用，应回 PDF 核对。
- 需核验作者是否发布代码或实验配置；正文未明确给出。
- LitQA2/LAB-Bench 名称在正文中有 LitAQ2/LitQA2 混写，正式写作时应回原基准核对名称。
- 若后续 SUMMARY 更新，建议标为 P1，因为它直接威胁 retrieval/evidence coverage，而不是普通 survey 生成 背景。
