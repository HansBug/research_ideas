# LR-Robot: An Human-in-the-Loop LLM Framework for Systematic Literature Reviews with Applications in Financial Research

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | LR-Robot: An Human-in-the-Loop LLM Framework for Systematic Literature Reviews with Applications in Financial Research |
| 年份 | 2026 |
| 作者 / venue / 出版状态 | Wei Wei、Jin Zheng 等；arXiv:2604.14793; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P0 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)；未人工逐页打开 PDF 图表 |
| 研究脉络 | agent式 SLR 工作流与评价基准 |
| 引用角色 | 直接新颖性门槛 / 强 baseline |
| LLM/agent 角色 | LLM 参与单阶段或少数阶段任务；未形成完整 agent 式 SLR 工作流。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | Scopus option pricing records、标题/摘要/元数据/引用列表、专家四维 taxonomy、prompt constraints、人工标注样本 |
| 输出 | 多维分类标签、RAG knowledge base、temporal co-occurrence 分析、label-enhanced citation networks、PageRank/子网络分析 |
| 方法/系统形态 | Human-in-the-loop LLM classification framework；专家定义 taxonomy，LLM 批量分类，RAG/网络分析做下游综述 |
| 覆盖阶段 | 检索、分类/编码、样本评估、知识库构建、主题演化和引用网络分析；不做全文报告生成或 claim-level writing |
| 不覆盖阶段 | 不覆盖阶段需按全文方法章节复核；当前不得据此写“完整覆盖 SLR 生命周期”。 |
| 人审/审计机制 | 专家设计分类维度和 prompt constraints，人工标注 1000 篇样本，417 篇继续标注 Dims 2--4；持久化分类输出支持 re-evaluation |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | 分类标签/人工标注 gold 级；无报告级 claim trace。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | 12,666 篇 option pricing 文献；BERTopic baseline；11/5 个 LLM；Accuracy、F1、Jaccard、self-consistency、error heatmap、PageRank overlap |
| 模型/API 设置 | GPT-5、Opus、Gemini、DeepSeek、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | 专家约束显著提升 Dim 1；Dims 2--3 表现较强，Dim 4 中等；错误多来自摘要内在模糊；RAG 标签支持发现传统 bibliometrics 看不到的结构 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 强约束 human-in-the-loop + taxonomy/prompt/evaluation story；但领域是金融文献分类，不是 SE SLR 报告生成 |
| 受影响主张 ID | C1,C2,C4,C5,C7 |
| 威胁类型 | 直接覆盖 + 局部覆盖 |
| 威胁的 paper2 主张 | 强约束 human-in-the-loop + taxonomy/prompt/evaluation story；但领域是金融文献分类，不是 SE SLR 报告生成 |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免写“首次 agentic SLR / 首次自动化 evidence synthesis”；必须承认跨域强近邻并收窄到 SE 场景和可审计证据包。 |
| baseline 可用性 | 定性强baseline；若代码/数据可得，后续再判定是否可运行复现。 |
| 对比方式 | 定性强baseline |
| 代码状态 | 需申请；原文写 data and code will be available upon request，非公开可运行入口 |
| 数据状态 | 需申请；原文写 data and code will be available upon request，非公开下载入口 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 定性强baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | 🟢 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Page 2 lines 15--39；Page 24 lines 1014--1042 | 标题和正文均以 systematic literature reviews 为任务背景，提出 human-in-the-loop LLM framework，直接相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟢 | `paper_content.txt` Page 7--9 lines 296--377；Page 10--24 | 覆盖数据检索、人工 taxonomy/prompt 设计、LLM 分类/编码、人工样本评估、RAG 知识库、主题演化和引用网络分析，超过四个综述相关环节。 |
| D3 LLM/agent 自动化深度 | 🟢 | `paper_content.txt` Page 8 lines 329--353；Page 9 lines 354--377；Page 16 lines 656--661 | LLM 在专家约束下批量执行多维分类，并将结果用于动态知识库和网络分析；虽非多 agent 编排，但有清晰的多阶段自动化输入输出链。 |
| D4 人工审计与可追踪性 | 🟢 | `paper_content.txt` Page 8 lines 329--353；Page 9 lines 360--367；Page 10 lines 424--429 | 专家标注代表性样本、迭代 refinement、比较模型和 prompt，并持久存储输出以便 audit/re-evaluation；缺点是没有 claim-to-source span，但按本维度可评强。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` Page 10--15 lines 424--652；Page 24 lines 1028--1042 | 有 12,666 篇大规模语料、人工标注样本、BERTopic/text mapping baseline、多模型比较、多指标和 error distribution analysis，评价扎实。 |
| D6 SE/CCF 相关性 | 🟠 | `bibtex.bib` arXiv q-fin.CP；正文为 financial research / option pricing | 与软件工程和 CCF venue 无直接关系；作为方法学和评价协议 baseline 有价值，但不能写成 SE 近邻。 |
| D7 对本文 novelty 的威胁 | 🟢 | `paper_content.txt` Page 4 lines 98--116；Page 24 lines 1014--1053 | 覆盖 human-in-the-loop、专家 taxonomy、prompt constraints、LLM 批处理、评价和知识库分析，对 paper2 的“人审 + LLM 综述自动化 + 评价协议”组合构成强威胁；差异化应放在 SE、agent run record 与 claim provenance。 |

## 3. 论文解决的问题与背景

LR-Robot 针对的是金融研究文献数量膨胀导致传统 SLR 不可持续的问题。作者认为 manual screening 和 narrative synthesis 在 option pricing 这种高重叠、强概念边界的领域中成本过高；传统 bibliometrics 依赖 metadata，不能理解论文真实贡献；LDA/BERTopic 等无监督主题模型又会把概念上不同的方法按词汇相似性混在一起。

论文的核心主张是分工：领域专家定义要分类什么，LLM 执行大规模分类，人工评估决定分类质量是否可信。这个设定对 paper2 很重要，因为它展示了“LLM 自动化”与“专家约束/人审”可以被组合成一个可评价的 SLR pipeline。

## 4. 方法 / 系统拆解

LR-Robot 有 framework development 和 application 两个阶段。Development phase 包含三层：Data Retrieval、Human-in-the-Loop Processing、RAG Knowledge Base Construction。Data Retrieval 由专家和 LLM 协作构建查询，在 Scopus/Web of Science 等数据库检索记录，并保存标题、摘要、作者、年份和引用等结构化元数据。

Human-in-the-Loop Processing 是方法核心。专家基于领域文献设计四个分类维度：是否开发/比较 pricing model、underlying asset type、option type、model type。专家还设计 prompt constraints 处理边界案例。LLM 在这些约束下分类，人工标注样本用于评估模型、调整 taxonomy、改进 prompt 和选择模型。

RAG Knowledge Base Construction 将最佳模型/提示产生的分类标签、原始元数据、摘要和引用列表存入结构化知识库。Application phase 支持新增文献定期进入知识库，自动分类，并用于 retrieval、temporal evolution、co-occurrence 和 label-enhanced citation network。审计机制主要是持久化输出、人工样本标注和可重评估，不是逐句 claim provenance。

## 5. 实验 / 评价设计

数据集来自 Scopus，检索到 16,174 条记录，去掉缺失/不完整 metadata 后保留 12,666 篇英文 option pricing 文章、会议论文和综述，时间跨度到 2026 年 3 月 5 日。BERTopic 被作为无监督 baseline，作者报告它在 12,666 个摘要中识别 54 个 topic，但将 5,298 篇归为 outlier，并出现 fragmentation/conflation。

LLM 评价部分随机选择 1,000 篇人工标注 Dim 1；其中 417 篇被判定为 pricing/volatility model development 后继续标注 Dims 2--4。Dim 1 评价 11 个 LLM，并比较有/无 expert constraints，指标包括 accuracy、F1、self-consistency。Dims 2--4 使用 5 个模型，指标包括 mean Jaccard、lenient accuracy、micro F1、sample F1、full agreement、pairwise Jaccard，并包含 text-mapping baseline。

评价还包括 error distribution analysis，观察错误是否集中在同一批困难样本；下游应用则用 Gemini Flash 3.0 在全量数据上分类，产生主题演化、co-occurrence、global/modeling citation network、sub-network divergence 和 cross-category citation preference 分析。

## 6. 主要结果与结论

Dim 1 中，expert constraints 使所有 11 个模型提升。正文给出例子：Gemini Flash 2.0 F1 从 0.7419 到 0.8152，DeepSeek V3 从 0.3418 到 0.7010；最佳模型 F1 超过 0.81，自一致性超过 0.94。Dims 2--3 因类别边界较清楚，sample F1 普遍较高；Dim 3 上 text mapping 达到 sample F1 0.9251，说明有些任务关键词规则仍有竞争力。

Dim 4 最难，subclass-to-class 策略优于直接大类分类，sample F1 提升约 0.08--0.12，full agreement 提升约 0.05--0.17。错误热图显示很多错误在所有模型上集中，作者解释为摘要信息不足或论文跨多个类别，而不是单个模型问题。

应用结果包括：全量 12,666 篇中 6,766 篇被识别为 pricing/volatility model papers；引用网络 12,560 篇有 reference 信息；global 与 modeling PageRank Top 10 重合 8 篇；sub-network analysis 发现 ML、market imperfections、emerging approaches 等子领域有不同于 global ranking 的 citation priorities。

## 7. 局限与可复现性

作者承认当前主要依赖摘要，摘要可能缺少区分复杂方法类别的关键细节；未来可扩展到 introduction 或 full text。另一个局限是只在 option pricing 领域验证，跨学科泛化仍需验证。

可复现性方面有不足。正文详细给出查询、样本规模、指标和大量表格，但 `Data Availability` 写的是 data and code will be available upon request，未看到公开仓库或可直接下载数据。若 paper2 以它为 baseline，需要将其视作方法/评价设计强证据，而不是可直接复现实验包。

## 8. 对 paper2 story / 实验设计的影响

LR-Robot 强烈提醒 paper2：只说“LLM 能辅助 SLR”不够，必须说明专家 taxonomy、prompt constraints、人工标注样本、模型选择和 error analysis 如何形成闭环。paper2 如果面向 SE 文献或状态机建模文献，应把 domain taxonomy 与 人工审计 设计成正式实验对象，而不是写成附带步骤。

paper2 的差异化可以是：从金融摘要分类转向 SE/AI4SE 文献中的 multi-stage evidence synthesis；从 abstract-level labels 转向 claim-to-source/page/table provenance；从 upon-request 可用性转向完整 run record 和可复现审计包；从 RAG knowledge base 分析转向自动生成 Related Work/SLR report 的可靠性评价。

## 9. 可用于写作的引用角度

- LR-Robot 可作为 human-in-the-loop LLM literature classification 的强 baseline，说明专家定义 taxonomy 与 prompt constraints 对可靠性很关键。
- 可引用其人工标注 1,000 篇样本、多模型、多指标、自一致性和 error heatmap 设计，支撑 paper2 的评价协议。
- 可用它对比“摘要级分类/知识库构建”和 paper2 的“证据可追踪综述生成/审计记录”差异。
- 不应复用原文任何过强 novelty 口号；在 paper2 中只写其已验证金融文献分类和下游网络分析。

## 10. 待复核清单

- 人工打开 PDF 图表核对 Figure 1--7、Table 1--5 中关键数字，尤其 OCR/文本提取中的表格换行。
- 检查 arXiv 是否更新版本，以及是否补充公开代码/数据链接。
- 若作为 baseline 复现实验，需要联系作者或确认 upon-request 数据获取可能性。
- 核实文中 GPT-5/Gemini Flash 3.0 等模型命名与实际可用模型是否存在版本漂移；写 paper2 时需要用“原文实验报告的模型名”而不是当前 provider 状态。
