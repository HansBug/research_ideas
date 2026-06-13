# A Multi-Agent LLM Framework with Hierarchical Citation Graph for Automated Survey Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | A Multi-Agent LLM Framework with Hierarchical Citation Graph for Automated Survey Generation |
| 年份 | 2025 arXiv version；PDF 内 ACM 模板写 2026，但 DOI 为占位 |
| 作者 / venue / 出版状态 | Minh-Anh Nguye、Minh-Duc Nguyen 等；arXiv:2510.07733; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 近邻强度备注 | 自动 survey 生成 强近邻；因不执行 SLR/SMS 筛选/抽取/编码协议，SUMMARY 保持 P2，但 D7 保留 🟢 并要求 paper2 正面差异化。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | `bibtex.bib`；`paper_content.txt` Page 1--14；已清理 PDF 提取残留 NUL 后阅读 |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | 用户 query；crawled paper database；paper metadata、全文/摘要 summary、citation links、semantic similarity |
| 输出 | 层次 citation graph、horizontal/vertical summaries、structured outline、full survey、评价分数和改进查询 |
| 方法/系统形态 | hierarchical citation graph + horizontal Leiden clustering + vertical weighted BFS + Writing Agent/Evaluation Agent iterative refinement |
| 覆盖阶段 | 查询扩展、检索过滤、图构建、paper summarization、outline generation、subsection writing、evaluation-agent feedback、RAG refinement、LLM/human/引用质量 evaluation |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 有 20 位 domain experts 的 ground truth selection 与 human evaluation；有 proof_ids prompt、引用质量 NLI；但生成流程中没有 人工审计 gate |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | 引用级 / proof-id 线索；不等同 SLR 抽取表、编码决策或报告级 claim ledger。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 10 个 SurGE CS topics；205 human surveys/one million papers 背景；每 topic 10 runs；AutoSurvey/SurveyX/SurveyForge baseline；LLM-as-judge、人类 win rate、citation recall/precision/F1、ablation |
| 模型/API 设置 | GPT-4、GPT-4o、Claude、Sonnet、Gemini、DeepSeek、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 10 runs、seed；正式复现前需回原文核对 |
| 主要发现 | SurveyG 在多数 LLM-as-judge 指标、human win rate、citation F1 和 ablation 上优于 SurveyForge 等 baseline；vertical traversal、horizontal clustering、multi-agent refinement 都有贡献 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强 novelty 威胁来自“multi-agent + graph memory + 引用质量 evaluation”；paper2 必须明确自己不是普通 survey 生成，而是 SLR/SMS evidence workflow with audit |
| 受影响主张 ID | C1,C3,C5,C6,C7 |
| 威胁类型 | 局部覆盖 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 强 novelty 威胁来自“multi-agent + graph memory + 引用质量 evaluation”；paper2 必须明确自己不是普通 survey 生成，而是 SLR/SMS evidence workflow with audit |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 / survey生成局部近邻 |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 / survey生成局部近邻 |
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
| D7 对本文 novelty 的威胁强度 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---|---|---|
| D1 | 🟢 | `paper_content.txt` Page 1 Abstract；Page 2 contributions | 直接研究 multi-agent automated survey 生成，并显式与 AutoSurvey、SurveyForge、SurveyX 比较。 |
| D2 | 🟡 | Page 2 Methodology；Page 4 Algorithm 2 | 覆盖检索、summarization、outline、writing、evaluation refinement，但不是 SLR/SMS 的筛选、抽取、编码和系统综述报告协议。 |
| D3 | 🟢 | Page 4 Generation Phase；Algorithm 2 | Writing Agent 和 Evaluation Agent 迭代协作，Evaluation Agent 生成 feedback 和 retrieval queries，自动化深度强。 |
| D4 | 🟡 | Page 5 expert ground truth；Page 11 proof_ids prompt；Page 6 引用质量 | 有专家 ground truth、人类评价、proof_ids 和 citation NLI 指标；但生成过程不含人工 gate，proof_ids 是 prompt 结构而非可审计 claim ledger。 |
| D5 | 🟢 | Page 5--8 Tables 1--5；Page 10--12 Appendix C/E | 有多 baseline、100 survey runs、四个 LLM judge、人类评价、一致性 κ、引用质量、ablation 和成本分析，是本批评价较严谨者。 |
| D6 | 🟠 | `bibtex.bib` primaryClass cs.AI；Page 5 CS topics | 预印本/模板稿，面向 CS survey 生成；不是 SE/CCF 正式 venue，虽然 topics 属 CS。 |
| D7 | 🟢 | Page 2--4 graph + multi-agent；Page 6 human eval/引用质量 | 覆盖 paper2 的多个潜在 claim：agent 工作流、structured evidence memory、引用质量、人类评价和 ablation。paper2 需正面差异化。 |

## 3. 论文解决的问题与背景

SurveyG 的背景判断是：已有自动 survey 生成 多把论文当成独立记录，直接检索后汇总，容易忽略 citation links、方法关系和研究演化，导致 taxonomy 不清、上下文理解浅、outline 或 full survey 变成单篇摘要拼接。论文因此提出用 hierarchical citation graph 表示文献之间的 citation dependencies 与 semantic relatedness，再用横向/纵向遍历生成多层 summaries，供 multi-agent 写作。

这对 paper2 很关键，因为它已经把“证据结构化为可写作 memory”推进了一步。不同的是，SurveyG 的结构是 citation graph 和 summary memory，目标是提高 survey 文本质量；paper2 若要成立，应强调 SLR/SMS 中更细的 screening/extraction/coding/claim evidence 记录，而不是只做 citation graph。

## 4. 方法 / 系统拆解

Preparation phase 先由 LLM 将用户 query 扩成关键词，检索候选论文并抓取 metadata。系统建立 hierarchical citation graph $G=(V,E,L)$：节点是论文，边包括 citation 和 semantic similarity，层为 Foundation、Development、Frontier。每个节点带 metadata 和 summary。semantic edge 权重由 text encoder embedding 的 cosine similarity 定义；若全文可得，默认用 LLM summary embedding，否则 fallback 到 abstract embedding。

知识表示阶段用 citation count 与 elapsed years 计算 trend score，选 top-K foundation papers；time landmark 之前的非 foundation 论文进入 Development，之后进入 Frontier。Horizontal summarization 对每层用 Leiden algorithm 分 community，再让 LLM 生成方法、主题和比较性总结。Vertical summarization 从每个 foundation seed 出发，用 weighted BFS 先到 Development，再到 Frontier，生成 path summary，捕捉研究演化。

Generation phase 使用 Writing Agent 与 Evaluation Agent。Writing Agent 以 $K+N$ graph summaries 初始化 memory，先生成 outline；Evaluation Agent 评估逻辑、覆盖与结构，并反馈改进。正文写作时，Writing Agent 对每个 subsection 生成 draft；Evaluation Agent 给出 critique 和 suggested queries，系统再 RAG 检索补充，最多迭代 $T_{max}$ 次。Prompt 要求 proof_ids、避免简单列表、强调后续工作如何解决前人限制。

## 5. 实验 / 评价设计

实验比较 AutoSurvey、SurveyX、SurveyForge 与 SurveyG。数据为 SurGE benchmark 的 10 个 CS topics，背景包含 205 篇 human-authored surveys 和 over one million papers。作者招募 20 位 domain experts，包括 CS PhD 和 senior AI research engineers。Ground truth construction 分为 topic selection、survey selection 和 reference curation：每 topic 2--3 位专家按 coverage、structure、recency、citation impact 选择 human survey，并整理 30--50 篇 essential papers。

实现上，每个方法检索 1500 candidate papers 构建 outline，每 chapter 选 60 篇，每 final survey 包含 300 篇；主 backbone 为 GPT-4o-mini-2024-07-18，另测 Gemini-2.5-Flash。每 topic 生成 10 次，共 100 surveys。评价包括 outline quality、content quality 五维（Coverage、Structure、Relevance、Synthesis、Critical Analysis）、引用质量 三维（Recall、Precision、F1）。LLM judges 包括 GPT-4o、Claude-3.5-Sonnet、DeepSeek-V3.2-Exp、Gemini-2.5-Pro；human evaluation 采用匿名 pairwise/score win rate。

## 6. 主要结果与结论

Table 1 中 SurveyG 在大多数 LLM-as-a-judge 指标上领先。以 GPT judge 为例，SurveyG Coverage 95.7、Structure 88.5、Relevance 95.1、Synthesis 92.2、Critical Analysis 91.2；SurveyForge 对应为 94.2、87.3、94.8、88.6、88.5。Table 2 报告 full paper human eval win rate 为 SurveyG 64.00% vs SurveyForge 36.00%，comparative win rate 为 72.25% vs 27.75%。

Table 3 中 引用质量 显示 SurveyG Recall 91.40±1.8、Precision 77.83±2.7、F1 83.49±2.0；Ground Truth 为 92.53/86.42/89.34。Table 4 报告 LLM-human agreement：outline κ=0.6972，content κ=0.6062；human-human 为 0.7542 和 0.7127。Table 5 ablation 显示去掉 vertical traversal、horizontal clustering 或 multi-agent refinement 都降分，尤其 Synthesis 和 Critical Analysis 下降明显。作者结论是，hierarchical citation graph 和 multi-agent refinement 能改进结构化、综合性和 citation coverage。

## 7. 局限与可复现性

正文给出 GitHub 链接、算法、prompt、baseline、topic、模型、成本和人类评价协议，可复现材料较多。但 PDF 模板中 ACM reference format 仍含占位 conference/DOI，说明不是正式出版版本；BibTeX 为 arXiv metadata。还需实际检查代码仓库是否完整可运行。

局限包括：构图和 multi-agent refinement 需要较多计算资源；coverage 依赖 crawled papers 的质量，paywalled content 会造成缺口；评价限于英文 computer science；citation graph 继承学术出版 bias；生成结果仍需要用户 critical review 以避免 attribution 和 plagiarism 风险。最重要的是，它评估 引用质量，但不是人工逐 claim 审计系统。

## 8. 对 paper2 story / 实验设计的影响

SurveyG 是 paper2 必须正面承认的强近邻。paper2 不能声称此前没有 multi-agent literature survey 生成、没有 graph-based memory、没有 human expert evaluation，也不能把 引用质量 evaluation 写成空白。差异化应落到 SLR/SMS 生命周期：检索式和数据库选择、screening inclusion/exclusion 决策、抽取 schema、coding memo、evidence synthesis、report claim provenance、人工审计 gate 和 run record eligibility。

实验设计上，paper2 可借鉴 SurveyG 的多层评价：LLM judge + human experts + citation precision/recall + ablation。但 paper2 应把评价单位从“整篇 survey 好不好”进一步下钻到“每个 claim 是否由正确来源支持”“每个筛选/抽取/编码决策是否可复核”“人审如何改变错误率”。如果 paper2 也使用 graph/memory，应与 SurveyG 的 hierarchical citation graph 明确区分。

## 9. 可用于写作的引用角度

1. SurveyG 是 multi-agent automated survey 生成 的强 baseline，它将 citation graph、horizontal/vertical summarization 和 writing/evaluation agents 结合。
2. 其 human expert 和 引用质量 评价表明，survey 生成 领域已经开始关注结构、综合、critical analysis 和 citation reliability。
3. SurveyG 的限制可用于引出 paper2：自动 survey 生成 仍主要面向文本质量，缺少 SLR/SMS 过程级证据审计和人工 gate。
4. paper2 应避免把 multi-agent survey 生成 写成无人覆盖的空白，而应写“面向 SLR/SMS evidence workflow 的 agent-based audit framework”。

## 10. 待复核清单

- 未人工打开 PDF 图表；Figure 2、Figure 5--7 如需用于论文，应回 PDF 核对。
- GitHub 仓库需后续核验实际代码、数据和 license。
- `bibtex.bib` 年份为 2025，PDF ACM template 写 2026 且 DOI 占位；正式引用前需核验 arXiv 最新版本和出版状态。
- Citation quality 使用 NLI model 抽样 100 claim-citation pairs；需要核验实现细节是否公开。
