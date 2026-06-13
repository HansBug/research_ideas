# Automated Literature Review Using NLP Techniques and LLM-Based Retrieval-Augmented Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Automated Literature Review Using NLP Techniques and LLM-Based Retrieval-Augmented Generation |
| 年份 | 2024 |
| 作者 / venue / 出版状态 | Nurshat Fateh Ali、Md. Mahdi Mohtasim 等；arXiv:2411.18583; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt) |
| 研究脉络 | LLM 辅助文献综述与证据综合 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM 参与单阶段或少数阶段任务；未形成完整 agent 式 SLR 工作流。 |
| 证据溯源粒度 | decision-log / trace 级 provenance；需核验是否能导出完整证据包。 |
| 输入 | 多篇 research paper PDFs；部分 pipeline 还使用 DOI；SciTLDR dataset 用于训练/测试/知识库。 |
| 输出 | 自动生成的 literature review segment；最终实现为基于 GPT-3.5-TURBO-0125 的 GUI tool。 |
| 方法/系统形态 | 比较 spaCy frequency-based、Simple T5、GPT-3.5-TURBO-0125 RAG/OpenAI Assistant 三种生成管线。 |
| 覆盖阶段 | 主要覆盖从 PDF 文本抽取、单篇 summarization、合并为 literature review 段落；不覆盖系统检索、筛选、质量评价、编码或证据审计。 |
| 不覆盖阶段 | 不覆盖系统检索、筛选、质量评价、编码或证据审计。 |
| 人审/审计机制 | 没有系统性 人工审计、provenance、claim-to-source trace；仅有 4 篇论文的 UI 示例输出。 |
| 人类角色 | 运行中审查者或用户反馈；需区分是否为正式审计 gate |
| 审计时机 | 原文未给出清晰审计时机或本轮未抽取 |
| 主张追踪状态 | 无明确 claim-to-source trace；仅 RAG/UI 示例，不能支撑审计 claim。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 不可导出或仅论文叙述；正式写作不得承诺可审计 artifact。 |
| 实验/指标 | SciTLDR 数据集，ROUGE-1/2/L/Lsum 比较三种方法；UI demo 使用 4 篇 healthcare/IoT 论文。 |
| 模型/API 设置 | Gemini、Llama、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 正文提到 prompt；完整模板待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | GPT-3.5-TURBO-0125 在 ROUGE-1 和 ROUGE-2 上最高；T5 在 ROUGE-L 和 ROUGE-Lsum 上高于 GPT；作者仍把 LLM pipeline 作为最终系统。 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 是 报告生成/RAG 的弱背景 baseline，可用于说明仅靠 PDF summarization 和 ROUGE 不足以支撑可审计 SLR claim。 |
| 受影响主张 ID | C6 |
| 威胁类型 | 背景定位 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 是 报告生成/RAG 的弱背景 baseline，可用于说明仅靠 PDF summarization 和 ROUGE 不足以支撑可审计 SLR claim。 |
| 支持的 paper2 主张 | 支持 paper2 将贡献收窄到可审计 evidence workflow、run record、人工审计 gate 与 claim-to-source trace，而非泛称自动综述生成。 |
| paper2 应避免的主张 | 避免声称“首次 LLM/agent 自动化 SLR”“完整覆盖 SLR 生命周期”“PRISMA 合规”，也不得把 arXiv 预印本当作 CCF/peer-reviewed 事实。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---:|---:|---:|---:|---:|---:|---:|
| 🟡 | 🟡 | 🟡 | ⚪ | 🟡 | 🟠 | 🟠 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟡 | `paper_content.txt:30-52`, `paper_content.txt:73-88` | 论文直接做自动 literature review segment generation，且比较 NLP/LLM/RAG 方法；但它不是严格 SLR/SMS 方法，也没有 systematic evidence synthesis protocol。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt:187-192`, `paper_content.txt:228-238`, `paper_content.txt:306-314` | 实现覆盖 PDF 文本抽取、单篇 summarization、合并生成 review segment，可视作抽取/综合/报告的弱流程；但输入论文已给定，不包含 search、screening、quality assessment、coding。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt:278-314`, `paper_content.txt:315-328` | 有 GPT-3.5-TURBO-0125 RAG/OpenAI Assistant pipeline 和 GUI，输入 PDF 后自动生成 review segment；但没有 agent planning、工具链审计或多阶段修复。 |
| D4 人工审计与可追踪性 | ⚪ | `paper_content.txt:293-302`, `paper_content.txt:395-442` | prompt 要求写 first author 和 title，UI demo 展示生成结果；原文没有人工审核机制、引用核验、证据定位、日志、provenance 或 claim-level trace。 |
| D5 评价严谨性 | 🟡 | `paper_content.txt:193-208`, `paper_content.txt:332-389`, `paper_content.txt:443-469` | 有 SciTLDR 数据集、三种方法对照和 ROUGE 指标；但评价对象更接近 scientific summarization，缺少人工 factuality/citation 评估、错误分类、统计显著性和真实 SLR 任务评价。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt:6-26`, `paper_content.txt:510-526` | 作者来自 CS/CSE 机构，主题是泛自动 literature review/NLP/RAG，不是软件工程 SLR 或 CCF SE venue。 |
| D7 对本文 novelty 的威胁强度 | 🟠 | `paper_content.txt:470-488` | 它只威胁 paper2 的“PDF 输入生成综述段落”弱表述；对 agent 工作流、人工审计、run record、SE setting 和 claim-to-source 支撑不构成强威胁。 |

## 3. 论文解决的问题与背景

这篇论文从“文献数量增长导致人工 literature review 很耗时”出发，目标是开发一个系统，只用相关论文 PDF 作为输入，自动生成 research paper 的 literature review segment。作者比较三类方法：frequency-based spaCy、transformer-based Simple T5、LLM-based RAG/OpenAI Assistant，并用 ROUGE 指标找出表现较好的方案，最后实现一个 GUI 工具。

需要注意，它所说的 literature review 更接近“多篇论文摘要拼接成综述段落”，不是严格意义上的 SLR/SMS。Related Work 中提到自动 composition of systematic literature reviews、searching/screening/mapping/synthesizing 等工作，但本文自己的系统没有执行这些步骤。对 paper2 来说，它是一个早期工具型背景，不能作为可审计 agentic SLR 的直接强 baseline。

## 4. 方法 / 系统拆解

方法共三条 pipeline。第一条是 spaCy frequency-based approach。模型对文本做 tokenization、去停用词和标点，计算词频和句子权重，选择 top 10% sentences 作为摘要。系统 pipeline 接收多个 papers 的 DOI 和 PDF，使用 Requests 获取标题和第一作者，用 PyPDF2 和正则抽取每个 PDF 的 conclusion，再用 spaCy summarizer 生成每篇摘要，最后 post-processing 并合并成 coherent literature review segment。

第二条是 Simple T5 transformer approach。作者使用 SciTLDR 训练 T5，加 task-specific prefix 来做单篇 summarization。系统接收 DOI 和 PDF，获取标题/第一作者，抽取每篇 PDF 的 abstract、introduction 和 conclusion，合并为模型输入，再用训练好的 T5 生成每篇摘要，最后合并成 literature review segment。

第三条是 LLM/RAG approach。作者选择 GPT-3.5-TURBO-0125 创建 OpenAI Assistant，打开 retrieval，把 SciTLDR dataset 加入知识库，并进行 prompt engineering。prompt 要求用户未来给 PDF，assistant 根据知识库中的 data.json input/output 样式，为输入 PDF 生成最多 80 词的 output，写成可作为新 research paper literature review 的风格，并提及第一作者和论文标题。实际系统 pipeline 接收多个 PDFs，用 PyPDF2 抽取全文，将文本作为 thread message/query 提交给 assistant，取回每篇输出后合并为最终 literature review segment。最终 GUI 后端使用 GPT-3.5-TURBO-0125，用户上传多个 PDF 后自动处理并显示完成状态。

人机协作和审计方面，全文没有设计人工确认、证据定位、引用核验或分歧处理。用户只负责上传 PDF，系统输出段落。生成文本是否忠实、是否遗漏关键论文、是否引用正确，需要外部人工另行判断。

## 5. 实验 / 评价设计

论文没有清晰列出 RQ，但实验目的可以概括为：比较 frequency-based、transformer-based 和 LLM/RAG 三种自动 literature review generation pipeline 的 ROUGE 表现，并用最佳方法实现 GUI。

数据集是 Hugging Face 上的 SciTLDR。原文说明它包含 5,400 个 TLDR，来自 3,200 多篇论文，source 是论文的 AIC 或 full text，target 是对应 summaries。spaCy 不训练，只在 test data 上评估；T5 使用 SciTLDR 训练后在 test data 上评估；LLM 方法把 SciTLDR 作为 assistant knowledge base。评价指标是 ROUGE-N、ROUGE-L 和 ROUGE-Lsum，比较机器生成摘要与 reference summaries 的 n-gram overlap 和最长公共子序列。

baseline 是三种方法之间互相对比：spaCy、T5、GPT-3.5-TURBO-0125。没有人工专家评审、factuality 评价、citation grounding 评价，也没有报告 train/test split 细节、随机种子、模型训练参数、prompt 多次运行稳定性或成本。UI evaluation 只是让用户输入 4 篇 healthcare/IoT 论文并展示输出段落，没有量化评分。

## 6. 主要结果与结论

ROUGE 表格给出以下结果。spaCy: ROUGE-1 0.257、ROUGE-2 0.055、ROUGE-L 0.144、ROUGE-Lsum 0.146。T5: ROUGE-1 0.268、ROUGE-2 0.115、ROUGE-L 0.204、ROUGE-Lsum 0.204。GPT-3.5-TURBO-0125: ROUGE-1 0.364、ROUGE-2 0.123、ROUGE-L 0.181、ROUGE-Lsum 0.182。

作者据此认为 LLM-based model 表现最好，并最终用 GPT-3.5-TURBO-0125 实现 GUI。这里需要保守解读：GPT 确实在 ROUGE-1 和 ROUGE-2 上最高，但 T5 在 ROUGE-L 和 ROUGE-Lsum 上高于 GPT。因此不能把表格解读为 GPT 在所有指标上全面胜出。更稳妥的写法是：LLM/RAG 在 unigram/bigram overlap 上最好，T5 在 longest-common-subsequence 类指标上更好；原文最终系统选择 LLM 可能还考虑了生成风格和交互部署便利，但这些没有被额外实验量化。

UI 示例输出显示系统能把 4 篇 healthcare/IoT 论文合并成一段较长 literature review，但原文没有人工检查 factual correctness、coverage、citation accuracy 或 source support。因此该 demo 只能证明工具能生成文本，不能证明它能生成可信的系统综述。

## 7. 局限与可复现性

原文的 future work 主要是增强 GUI 功能，例如加入 model options、output size，并尝试 BERT、Gemini、LLaMA 等更多模型。作者没有系统讨论方法局限，但从全文证据看，至少有几类限制：第一，输入是用户给定 PDF，不解决检索和筛选；第二，PDF 解析依赖 PyPDF2 和正则，抽取 abstract/introduction/conclusion 或全文的鲁棒性未知；第三，ROUGE 对 literature review 的事实性、引用正确性、论证结构和综合质量支持有限；第四，LLM 输出没有 provenance，不能追踪句子来自哪篇论文哪段文本；第五，没有代码/数据/配置公开说明，prompt 只给出一段文本，缺少 assistant 配置、retrieval 设置和调用日期。

本地只核验了 `paper_content.txt`，没有打开 PDF 图 1-7，也没有复跑系统。BibTeX 为 arXiv 元数据，正式发表状态、DOI 和代码可用性仍待复查。

## 8. 对 paper2 story / 实验设计的影响

这篇论文提醒 paper2：仅用 PDF 输入、自动摘要、拼接成 review segment，并用 ROUGE 评价，已经不足以支撑强 novelty。paper2 的差异必须落到 SLR/SMS 的研究流程、筛选/抽取/编码/综合/报告的阶段化证据、以及每条 claim 的 source grounding。

同时，它也提供一个负面评价参照。ROUGE 可以作为低成本文本相似度指标，但不能替代 evidence-level audit。paper2 如果评估报告生成，应加入 unsupported claim rate、citation/source alignment、evidence span correctness、人工审计拦截率和复现性字段，而不是只比较自动生成段落的表面相似度。

## 9. 可用于写作的引用角度

1. 可作为自动 literature review generation 早期工具背景：该工作比较 spaCy、T5 和 GPT-3.5-TURBO-0125 RAG pipeline，并实现 PDF-to-review GUI。
2. 可作为评价不足的例子：ROUGE 能衡量摘要与 reference 的词面重合，但不能证明 SLR 报告的 factuality、coverage 或 citation grounding。
3. 可作为 paper2 差异化参照：paper2 不应定位为“自动生成综述段落”，而应定位为可审计的 multi-stage evidence workflow。
4. 不应把它写成完整 SLR 自动化、PRISMA-style review 或 agentic workflow。

## 10. 待复核清单

1. 当前只读 `paper_content.txt`，未回 PDF 核对 Figure 1-7 和表格版式。
2. 需核验是否有公开代码、GUI、训练脚本、OpenAI Assistant 配置和 SciTLDR split。
3. 需补查正式发表状态和 DOI；本地 BibTeX 只有 arXiv 信息。
4. 若用作 paper2 baseline，需人工检查其 UI demo 输出是否有事实错误、引用缺失或 source mismatch，原文没有提供这类审计。
