# LLAssist: Simple Tools for Automating Literature Review Using Large Language Models

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | LLAssist: Simple Tools for Automating Literature Review Using Large Language Models |
| 年份 | 2024 |
| 分层 | P1-开源 screening/relevance 工具近邻 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 图表 |
| 输入 | CSV 格式论文元数据/标题/摘要、用户给定 research questions 文本 |
| 输出 | 每篇文章的 key semantics、RQ relevance/contribution TRUE/FALSE、0-1 分数、reasoning、must-read 标记；JSON 与 CSV |
| 方法/系统形态 | C# console tool；单 LLM 后端进行语义抽取和相关性/贡献评估；支持本地 Ollama 与 OpenAI API |
| 覆盖阶段 | 初筛/优先阅读列表；不做检索策略生成、全文抽取、编码、综合或报告写作 |
| 人审/审计机制 | 输出 reasoning 和 CSV/JSON 供人审；作者强调 human-in-the-loop 和 PRISMA；无正式审计日志或金标裁决机制 |
| 实验/指标 | IEEE Xplore/Scopus cybersecurity 数据；17、37、115、2576 篇；Gemma 2、GPT-3.5、GPT-4o、Llama 3；分类分布、must-read ratio、时间/成本；人工定性检查 reasoning |
| 主要发现 | Gemma 2 较有区分度，GPT-3.5 过度包容，GPT-4o 较平衡，Llama 3 binary/score 不一致；大数据集 Gemma 2 标出 324 must-read、100 contributing |
| 对 paper2 的作用 | 可作为 lightweight screening / transparent open-source tool 对照；对完整 agentic SLR workflow novelty 威胁中等偏低 |
## 2. D1-D7 全文核验评分

emoji 口径：🟢 强，🟡 中，🟠 弱，⚪ 无 / 背景。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟠 | 🟡 | 🟠 | 🟠 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Abstract；§1 Introduction；§2 Methodology | 论文直接讨论 LLM 辅助 literature review automation，具体任务是 systematic literature review 初筛和 relevance estimation。 |
| D2 SLR/SMS 流程覆盖度 | 🟠 | §2.1 Article Processing；§2.2 Evaluation | 只覆盖标题/摘要语义抽取、RQ relevance/contribution 判断和 must-read 标记，属于单一 screening 阶段。 |
| D3 LLM/agent 自动化深度 | 🟡 | §2.1；§3 Technical Implementation | 使用 LLM 执行 key semantics extraction 和 relevance assessment，流程清楚；但不是 multi-agent，也没有迭代综合或工具编排。 |
| D4 人工审计与可追踪性 | 🟠 | §2.1 Output Generation；§2.2.5 Preliminary Nature；§4.1.4 Reasoning Quality | 输出 reasoning 方便人工判断，并强调 human-in-the-loop；但无 audit log、provenance、双人筛选 adjudication 或可复验人审协议。 |
| D5 评价严谨性 | 🟠 | §2.2；§4 Experiment Results；§5 Analysis | 有多数据规模、多 LLM 后端、时间/成本和分布分析，但准确性/meaningful reasoning 评估是 uncontrolled，缺少 gold labels、F1/precision/recall 和正式人工标注。 |
| D6 SE / CCF 相关性 | 🟠 | bibtex: arXiv cs.DL；case domain 为 cybersecurity | 研究对象是 cybersecurity 文献初筛，和 SE/安全综述有间接关系，但不是 CCF/SE SLR venue。 |
| D7 对本文 novelty 的威胁强度 | 🟡 | §2.1 tool design；§8 Availability | 威胁 paper2 的“LLM screening/relevance scoring/open-source transparency”局部点；不覆盖 agentic multi-stage workflow、evidence synthesis 或审计证据链。 |

## 3. 论文解决的问题与背景

LLAssist 的出发点是 systematic literature review 中初筛工作量随文献增长而变大，闭源 LLM 工具又带来透明性、可复现性和偏差风险。作者希望提供一个简单、开源、可修改的工具，帮助研究者基于标题、摘要和 research questions 估计文献相关性，从而减少初始筛选压力。

它的研究目标比 LiRA、ARISE 和 SurveyLens 更窄：不是自动生成 survey，不处理 full-text synthesis，也不是 benchmark。它强调“lightweight filtering enhancement”，并明确要求研究者仍应遵循 PRISMA 等既有方法。这一点对 paper2 有利，因为它说明早期 LLM literature review 工具往往只覆盖 screening 子任务。

## 4. 方法 / 系统拆解

输入是 CSV 文件和 research questions 文本。CSV 包含文章 metadata 和 abstracts；RQ 文件列出用户关心的问题。对每篇文章，LLAssist 首先调用 LLM 从 title/abstract 提取 topics、entities、keywords。随后对每个 RQ 输出二元 relevance decision、0-1 relevance score、二元 contribution decision、0-1 contribution score，以及 relevance/contribution reasoning。默认阈值为 0.7，超过阈值则认为相关或有贡献。Must-read 通过所有 RQ 的 relevance/contribution 阈值做逻辑 OR 得到。

输出包括 JSON 和 CSV。作者有意识地要求输出详细信息，便于导入其他工具和保持 process visibility。技术实现中，所谓 CoT 是通过“抽取 key semantics”和“filtering/self-consistency”两步模拟推理。后端支持本地 Ollama Llama 3、Gemma 2，以及 OpenAI GPT-3.5/GPT-4。实现语言是 C#，目标是后续能接入更大的 enterprise system。

该方法没有专门的 agent role 分工。所谓 reasoning 是给人看的解释，而不是可验证的证据链。

## 5. 实验 / 评价设计

实验场景是 LLM applications in cybersecurity。数据来自 IEEE Xplore 和 Scopus：IEEE 查询 `"llm AND cyber AND security"` 得到 17 篇；Scopus 三组查询得到 37、115 和 2576 篇。作者制定 4 个 RQ，分别关于 LLM 在威胁检测/分析中的使用、集成 LLM 的风险漏洞、对抗样本/恶意软件生成检测、伦理与隐私问题。

小数据集实验使用 Gemma 2:9B、GPT-3.5-turbo-0125、GPT-4o-2024-05-13 和 Llama 3:8B；大数据集只用本地 Gemma 2 和 Llama 3。评价指标写作上包括 consistency、accuracy in matching papers to RQs、meaningful insights/reasoning，但 §2.2.5 承认准确性和 reasoning 质量是在 uncontrolled environment 下评估。正文实际报告主要是二元相关/贡献数量分布、must-read/discard ratio、定性 reasoning 检查、处理时间和 API 成本。

## 6. 主要结果与结论

小数据集结果显示，不同模型行为差异大。Gemma 2 给出较强 binary decision 和 score 区分；GPT-3.5 几乎把所有内容都判为相关，可能导致高 false positive；GPT-4o 更平衡但常给中间分；Llama 3 的 relevance score 和 binary classification 不一致，因此作者决定不使用其 binary relevance decisions 作为 screening performance 分析基础。

大数据集使用 Scopus 2576 篇。Table 1 中 SL-Gemma2 总计标出 324 篇 relevant/must-read，100 篇 contributing；按年份看 2023 年 relevant 数 117、contributing 数 42，作者解释 2024 年下降主要来自年中截断。SL-Llama3 则给出 536 篇 relevant 和 791 篇 contributing，显示模型口径差异很大。

时间和成本方面，17-37 篇少于 10 分钟，115 篇约 20-50 分钟，2576 篇约 10-11 小时。GPT-4o 最慢且约每 100 篇 3.16 美元，GPT-3.5 每 100 篇约 0.22 美元，本地 Gemma 2/Llama 3 无云 API 成本。作者结论是 LLAssist 可显著减少初筛时间，但不能替代人类判断。

## 7. 局限与可复现性

作者明确承认 evaluation preliminary、uncontrolled。系统只看 title/abstract，没有利用全部 metadata，如年份、引用数等，也可能错过全文中的相关信息。模型行为差异大，提示词需要更精确调优。未来工作包括 full-text analysis、feedback mechanism 和 domain-specific models。

可复现性方面，论文提供 GitHub 地址，工具开源，这是强项。缺口是没有 gold standard inclusion/exclusion labels，没有双人筛选一致性，没有 precision/recall/F1，也没有报告 prompt 版本、完整运行日志和错误样例分类。因此不能把它当作严谨的 screening benchmark，只能当作工具原型和初步实证。

## 8. 对 paper2 story / 实验设计的影响

LLAssist 支持 paper2 的一个背景论点：现有开源 LLM literature review 工具已经能做标题/摘要层面的相关性评分和可解释筛选，但通常停留在 lightweight assistant，不具备完整 evidence workflow。paper2 如果包含 screening stage，可以把 LLAssist 作为简单 baseline：输入同样的 metadata/RQs，比较 inclusion ranking、human workload reduction 和 false exclusion 风险。

paper2 应比 LLAssist 更强地处理 audit：保留每篇文献的 inclusion/exclusion rationale、人工复核结果、冲突裁决、证据定位和 schema-valid run record。实验也不能只报告数量分布，应使用人工标注 gold labels、precision/recall、work saved over sampling、错误类型和 reviewer trust。

## 9. 可用于写作的引用角度

可引用为“早期开源 LLM 工具已尝试用标题/摘要和 RQ 自动估计文献相关性，输出分数、二元判断和 reasoning 以支持 human-in-the-loop 初筛”。也可引用为“不同 LLM 后端在 relevance screening 上口径差异很大，GPT-3.5 可能过度包容，Llama 3 的分数与二元判断可能不一致”。

不应引用为“LLM 可可靠自动筛选 SLR 文献”。原文没有受控金标评估，也明确说 LLAssist 不是人类判断替代品。

## 10. 待复核清单

- GitHub 仓库当前是否仍活跃，是否包含论文实验 CSV/JSON 和 prompt。
- 是否有后续版本加入 full-text analysis 或 feedback mechanism。
- 2576 篇大数据集的人工抽检结果是否存在但未写入正文。
- 若作为 paper2 baseline，需固定阈值 0.7 是否公平，或改成可调 ranking baseline。
- 需要确认 cybersecurity 数据是否适合作为 SE/SMS 场景，或仅作为方法背景。
