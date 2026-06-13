# Evaluating Prompting Strategies and Large Language Models in Systematic Literature Review Screening: Relevance and Task-Stage Classification

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Evaluating Prompting Strategies and Large Language Models in Systematic Literature Review Screening: Relevance and Task-Stage Classification |
| 年份 | 2025 |
| 作者 / venue / 出版状态 | Binglan Han、Anuradha Mathrani 等；arXiv:2510.16091; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P1 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；未人工打开 PDF 核对图表 |
| 研究脉络 | SLR/SMS 筛选、语料过滤与规划 |
| 引用角色 | 模块级 baseline / 重要相关工作定位 |
| LLM/agent 角色 | LLM 主要作为生成器、评价器或被综述对象；非多 agent 执行 workflow。 |
| 证据溯源粒度 | 未见可执行 provenance；只能作为背景或弱审计证据。 |
| 输入 | 2014--2024 年 SLR automation 相关候选文献；去重筛选后 1,376 条，人工标注出 491 条 relevant 记录 |
| 输出 | relevance yes/no、五类 SLR stage 自动化标签、是否使用 LLM 标签、prompt/model 指标和每 1,000 abstracts 成本 |
| 方法/系统形态 | 6 个 LLM × 5 类 prompt 的系统评价；两层分类任务；非 agent 系统 |
| 覆盖阶段 | 实质执行 relevance screening 与 task-stage coding；其他 SLR 阶段只是被分类为标签对象 |
| 不覆盖阶段 | 不覆盖检索策略冻结、全文抽取、编码、综合、报告生成和报告级 claim-to-source。 |
| 人审/审计机制 | 两名研究者独立标注并 consensus；prompt 模板和 CI 报告较完整；无 per-record provenance 或审计日志 |
| 人类角色 | 无正式人审 gate；若有评价者仅作实验评价 |
| 审计时机 | 运行前 + 运行后复核 |
| 主张追踪状态 | 无明确 claim-to-source trace 或本轮未核验 |
| 决策日志状态 | per-record / reasoning 级线索；导出格式待核验 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | accuracy、precision、recall、F1、Wilson CI、bootstrap F1 CI、Friedman / Nemenyi、成本分析 |
| 模型/API 设置 | GPT-4、GPT-4o、Claude、Opus、Gemini、Llama、DeepSeek、GPT；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | CoT-few-shot 在 relevance classification 中整体均衡；zero-shot 适合高召回初筛；self-reflection 过度纳入且不稳定；GPT-4o / DeepSeek 强，GPT-4o-mini 成本低 |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 支撑 paper2 的 prompt/model/cost baseline 和分层筛选策略；不应被写成端到端 SLR 自动化竞品 |
| 受影响主张 ID | C5,C7 |
| 威胁类型 | 评价协议约束 |
| 威胁的 paper2 主张 | 支撑 paper2 的 prompt/model/cost baseline 和分层筛选策略；不应被写成端到端 SLR 自动化竞品 |
| 支持的 paper2 主张 | 支持 paper2 把筛选阶段评价扩展到 false negative、模型变异、人工复核路由、成本和决策日志，而不是只报告 accuracy/F1。 |
| paper2 应避免的主张 | 避免把筛选 accuracy/F1 当作完整 SLR 自动化贡献；避免忽视 false negative、模型变异和人工复核成本。 |
| baseline 可用性 | 协议/指标baseline或局部强baseline；主要用于模块级对照与写作定位。 |
| 对比方式 | 协议/指标baseline |
| 代码状态 | 声称有/正文出现 GitHub 或 code 线索；本轮未打开核验 |
| 数据状态 | 声称有/正文出现 dataset 或 data availability 线索；license 未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅从 paper_content/review 识别线索；URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 协议/指标baseline |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

emoji 口径见 [../../GUIDE.md](../../GUIDE.md)；本表单元格只放 emoji。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟡 | 🟠 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | `paper_content.txt` Abstract / Page 1；§1 / Page 2 | 论文直接研究 LLM 与 prompt strategy 在 SLR screening / stage classification 中的表现，和 paper2 的筛选与分类模块高度相关。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | `paper_content.txt` §3.1 / Page 4--5；§4.2 / Page 11--18 | LLM 实际执行 relevance screening 和 Level-2 task-stage coding；虽然标签覆盖 searching、screening、retrieval、synthesis、writing，但模型并未执行这些阶段，因此按两个核心环节计。 |
| D3 LLM/agent 自动化深度 | 🟡 | `paper_content.txt` §3.2--3.4 / Page 5--7；Appendix B / Page 31--35 | 有清楚的 prompt、模型、JSON 输出和批量分类流程，但没有 agent、工具链、迭代审计或跨阶段状态传递。 |
| D4 人工审计与可追踪性 | 🟠 | `paper_content.txt` §3.1 / Page 4--5；§5.4 / Page 20 | 数据集由两名研究者独立标注并 consensus，prompt 附录可复核；但自动化流程没有 人工审计 gate、决策日志、claim-to-source 或 per-cell provenance。 |
| D5 评价严谨性 | 🟢 | `paper_content.txt` §4 / Page 7--18；Table 2--9；Appendix A / Page 25--30 | 评价覆盖 6 个 LLM、5 类 prompt、两层分类任务、置信区间、显著性检验、成本表和附录细表，实验设计扎实。 |
| D6 SE / CCF 相关性 | 🟠 | `paper_content.txt` BibTeX / arXiv cs.CL；§2 / Page 2--4 | 论文属于泛 SLR automation / NLP 评价，不是 SE venue，也不是直接面向 SE SLR；可作为方法学和评价设计背景。 |
| D7 novelty 威胁强度 | 🟡 | `paper_content.txt` §5.1--5.5 / Page 18--21 | 对 paper2 的 prompt selection、model-cost tradeoff、分层筛选 workflow 构成局部威胁；但没有多 agent SLR workflow、证据链、报告生成或 SE 场景。 |

## 3. 论文解决的问题与背景

论文关注的问题是：LLM 能用于 literature screening，但不同 prompt 和模型之间的交互效应没有被系统量化。作者指出，现实 screening 常有成千上万 abstracts，prompt token 会影响成本和延迟，模型选择也会造成数量级级别的费用差异。因此只比较一个模型或一种 prompt 不足以指导大规模使用。

这篇论文的“screening”需要谨慎理解。它并不是针对一个具体医学或 SE SLR 的 inclusion/exclusion protocol 来筛选候选文献，而是作者构建了一个 SLR automation 文献库，先判断论文是否与 SLR automation 相关，再判断它涉及哪些 SLR stage 以及是否使用 LLM。也就是说，它更接近“文献库构建中的 relevance screening + coding”，而不是端到端 SLR 执行。

## 4. 方法 / 系统拆解

输入来自 Scopus、ScienceDirect、ACM Digital Library、IEEE Xplore、Web of Science、Semantic Scholar 等数据库，检索 2014--2024 年与 literature review automation / systematic review automation 相关的论文。初始返回超过 5,000 条，去重和剔除非研究项后剩 1,376 条。两名有 LLM 和 systematic-review 经验的研究者独立标注并协商，得到 491 条 relevant 记录。Level 1 是 relevance yes/no；Level 2 是 searching、screening、retrieval、synthesis、writing 五类 stage 自动化标签，以及 Using LLMs 标签。

prompt 设计覆盖 zero-shot、few-shot、CoT、CoT-few-shot、self-reflection。Level 1 relevance classification 使用五类 prompt；Level 2 task classification 只使用四类 prompt，self-reflection 因预实验较弱未纳入。所有 prompt 都要求严格 JSON 输出，附录 B 给出了模板。模型包括 GPT-4o、GPT-4o-mini、DeepSeek-Chat-V3、Gemini-2.5-Flash、Claude-3.5-Haiku、Llama-4-Maverick，统一经 OpenRouter API 调用。

系统形态是批量分类评测，不是 agent。LLM 不执行检索、不读全文抽取、不综合证据、不写报告；它只根据 title 和 abstract 生成分类标签。人机协作主要在数据集标注阶段和作者建议阶段，并未形成模型输出后的人工复核闭环。

## 5. 实验 / 评价设计

RQ1 询问 prompt strategy 和 LLM choice 如何单独及共同影响 accuracy、precision、recall、F1 和 criteria/task 表现。RQ2 询问大规模 screening 下 model-prompt 组合的成本-性能权衡，以及哪些配置能兼顾效果和操作效率。

评价分两层。Level 1 对 1,376 条记录做 SLR automation relevance classification。Level 2 对 491 条 relevant 记录做六类标签预测：五个 SLR stage 和 LLM use。指标包括 accuracy、precision、recall、F1；Accuracy / Precision / Recall 使用 Wilson score interval，F1 使用 5,000 次 abstract-level bootstrap。显著性分析使用 Friedman 检验和 Nemenyi ranks。成本分析按每 1,000 abstracts 汇总 input/output tokens、美元成本和 F1。

人工标注和专家评审方面，原文只说明两名研究者独立标注并通过 consensus 解决分歧；未报告 Cohen's kappa、具体分歧率或标注手册版本。baseline 是不同 LLM / prompt 组合之间的横向比较，没有传统 ML、active learning 工具或 human-only speed baseline。

## 6. 主要结果与结论

Level 1 relevance classification 中，CoT-few-shot 的宏平均 F1 最高，为 0.913；few-shot 为 0.912，CoT 为 0.905。zero-shot 的 recall 最高，为 0.971，但 precision 只有 0.834，适合高敏感度初筛。self-reflection 表现最弱，F1 为 0.835，precision 为 0.753，作者认为它容易过度纳入且模型间方差大。

模型层面，GPT-4o 宏平均 F1 为 0.918，DeepSeek-Chat-V3 为 0.914；Gemini、Claude、Llama、GPT-4o-mini 形成第二梯队。作者强调没有单一 prompt 适合所有模型：GPT-4o 的 zero-shot 很强，DeepSeek 适合 CoT，Llama 和 Claude 更依赖 CoT-few-shot。

Level 2 task classification 显示任务复杂度差异明显。LLM-use detection 最容易，F1 为 0.925；screening F1 为 0.868，retrieval 为 0.810；synthesis 最难，F1 为 0.642，writing 为 0.702。作者据此认为 LLM 对具体、词汇线索明显的任务更可靠，而对 synthesis / writing 这类抽象概念分类仍弱。

成本分析显示 GPT-4o-mini 在多种 prompt 下成本很低。Table 9 中 GPT-4o-mini 的 zero-shot 每 1,000 abstracts 成本为 0.09 美元、F1 为 0.896；CoT / CoT-few-shot 成本约 0.12 / 0.18 美元，F1 均为 0.910。作者推荐用低成本模型和结构化 prompt 做第一轮，再把 borderline / contentious cases 升级给更强模型。

## 7. 局限与可复现性

原文明确承认 domain scope 是主要局限。数据集集中在 SLR automation 论文，这类标题和摘要常有显式词汇线索，如 systematic review、screening、automation，可能导致 shortcut learning，性能不一定迁移到 PICO-guided clinical meta-analysis、social policy 或 ecology 这类信号更隐性的领域。

第二类局限是方法范围：论文没有测试 RAG、迭代/meta prompting、declarative prompt optimization，也没有 qualitative error analysis、user study 或 human-in-the-loop audit。第三类局限是数据不平衡，writing 和 synthesis 样本少，导致 F1 和置信区间不稳定。可复现性方面，论文提供模型名、prompt 模板、指标和统计方法，但 `paper_content.txt` 中没有发现当前代码、数据、标注 rubrics 的公开链接；作者在 future work 中建议开放这些材料，说明当前还不能视为制品级完全可复现。

## 8. 对 paper2 story / 实验设计的影响

paper2 需要把这篇作为 prompt/model/cost evaluation 的局部强 baseline。它提示我们在实验中不能只报告一个默认 prompt 的结果，而应至少固定 zero-shot、few-shot/CoT-few-shot 等代表性 prompt，并说明为什么选择某个 operating point。若 paper2 有大规模 screening，成本表也应成为设计的一部分。

但 paper2 不能把这篇当作完整 SLR 自动化系统来对比。它没有 agent、没有检索到报告的闭环、没有 run record、没有人工 audit gate，也没有 claim-to-source trace。paper2 的差异化应写成：在已知 prompt/model 选择会显著影响筛选结果的前提下，本文进一步把阶段输入输出、人工裁决、证据来源和报告 claim 组织成可审计 workflow。

## 9. 可用于写作的引用角度

- Han 等人的系统评价表明，LLM screening 中 prompt 与模型存在显著交互，CoT-few-shot 往往提供较好的 precision-recall 平衡，而 zero-shot 更适合高召回初筛。
- 该工作还显示 self-reflection 并非自然带来更好 screening，反而可能产生过度纳入和跨模型不稳定；本文不应把“反思”类步骤写成无条件收益。
- 其成本分析支持 staged workflow：低成本模型先筛，争议样本再交给强模型；本文可把该思想扩展为带人工 audit 和 run record 的阶段化决策。
- 由于该数据集集中于 SLR automation 主题，作者自己提醒外部迁移风险；本文在 SE / LLM4SE / MDE 场景中需要独立验证。

## 10. 待复核清单

- 人工打开 PDF 核对 Table 9 的成本列和附录表格，`paper_content.txt` 中表格换行较密。
- 核验是否有 GitHub / OSF / data release；全文文本中未见公开代码数据链接。
- 若用于 paper2 实验设计，需复核 OpenRouter 调用时间、模型版本和价格是否仍适用。
- 补查是否已有 peer-reviewed 版本；当前 BibTeX 仅为 arXiv preprint。
