# SurveyGen: Quality-Aware Scientific Survey Generation with Large Language Models

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | SurveyGen: Quality-Aware Scientific Survey Generation with Large Language Models |
| 年份 | 2025，arXiv:2508.17647 |
| 作者 / venue / 出版状态 | Tong Bao、Mir Tafseer Nayeem 等；arXiv:2508.17647; 本轮未核验正式 peer-reviewed / CCF 状态 |
| 分层 | P2 |
| 近邻强度备注 | 强 survey 生成 benchmark/evaluation 近邻；因非 agent 工作流 且不覆盖 SLR/SMS 执行协议，SUMMARY 保持 P2。 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | `bibtex.bib`；`paper_content.txt` Page 1--25；已清理 PDF 提取残留 NUL 后阅读 |
| 研究脉络 | 自动 survey / literature review 生成与评价 |
| 引用角色 | 背景近邻 / 局部 claim 风险或禁用 claim 证据 |
| LLM/agent 角色 | LLM/agent 执行部分检索、筛选、抽取、组织、生成或评价环节；具体阶段见方法/覆盖阶段字段。 |
| 证据溯源粒度 | 人工核验或 benchmark/gold 级；未必有 claim-level provenance。 |
| 输入 | S2ORC survey corpus；survey topic；title/abstract/full-text sections；direct citations、second-level references、OpenAlex quality metadata |
| 输出 | SurveyGen 数据集；QUAL-SG quality-aware retrieval framework；三类 task 的生成结果和 citation/content/structure/human evaluation |
| 方法/系统形态 | 大规模 human-written survey benchmark + quality-aware RAG ranking；非 multi-agent 系统，LLM 被称为 generation/evaluation agents |
| 覆盖阶段 | survey-type detection、dataset construction、citation/metadata enrichment、candidate retrieval、co-citation expansion、quality reranking、outline/content generation、自动与人工评价 |
| 不覆盖阶段 | 不覆盖 SLR/SMS 的双人筛选、纳入/排除审计、抽取表、编码协议、质量评价和系统综述级报告审计。 |
| 人审/审计机制 | 有 human-written surveys 作为 gold standard；3 名 CS PhD 做匿名人工比较；但生成流程没有人类 audit gate |
| 人类角色 | 领域专家gold / 标注者 / 事后评价者（具体角色见人审机制字段） |
| 审计时机 | 仅评价阶段 / 运行后审计 |
| 主张追踪状态 | gold survey 和人工比较级；无生成期 claim trace。 |
| 决策日志状态 | 无或仅论文叙述 |
| 冲突处理机制 | 原文未给出明确冲突处理或不适用 |
| 审计导出性 | 有表格/JSON/schema 输出线索；是否形成可审计证据包待 artifact audit。 |
| 实验/指标 | 4205 篇 human surveys、242143 direct references、5062596 second-level references；120 surveys across Bio/Med/Psy/CS；6 个 LLM；Task 1/2/3；citation P/R/F1、accuracy、semantic similarity、ROUGE-L、KPR、structural overlap、human eval |
| 模型/API 设置 | GPT-4、GPT-4.1、Claude、Sonnet、Gemini、Llama、DeepSeek、GLM；具体版本/调用日期按原文与 artifact 待复核 |
| 提示词状态 | 附录/正文给出 prompt 或片段；完整可复用性待核验 |
| 温度/重复/随机种子 | 原文未给出或本轮未抽取 temperature / seed / repeats |
| 主要发现 | fully automatic survey 生成 citation accuracy 最高仅 35.84%；QUAL-SG Task 2 citation F1 16.73 高于 Fully-LLMGen 7.76 和 Naive-RAG 5.93；human-guided Task 3 提升内容质量，但仍未达 human standard |
| 关键结果锚点 | review.md §2 D1-D7 证据锚点 + §5/§6 实验与结果；SUMMARY 数字不得脱离单篇锚点引用 |
| 数值使用许可 | 仅文本级引用；正式写作前需 PDF 图表/表格核对 |
| 对 paper2 的作用 | 为 paper2 提供强负证据：全自动/普通 RAG 仍低 引用质量 和弱 critical analysis；paper2 应把 人工审计、claim grounding 和 evidence selection 作为核心实验指标 |
| 受影响主张 ID | C5,C6,C7 |
| 威胁类型 | 负面证据 + 禁用 claim 证据 |
| 威胁的 paper2 主张 | 为 paper2 提供强负证据：全自动/普通 RAG 仍低 引用质量 和弱 critical analysis；paper2 应把 人工审计、claim grounding 和 evidence selection 作为核心实验指标 |
| 支持的 paper2 主张 | 支持 paper2 把报告生成 claim 收窄为“生成必须可审计”，并把 citation validity、unsupported claim 和 有证据支撑的断言 纳入评价。 |
| paper2 应避免的主张 | 避免声称自动 survey / review generation 尚无人研究；避免把文本流畅度、引用准确率或 LLM-as-Judge 总分等同于 SLR/SMS 方法学可靠性。 |
| baseline 可用性 | 仅related-work背景或局部强近邻；不作为主流程可运行 baseline。 |
| 对比方式 | 仅related-work背景 / survey生成局部近邻 |
| 代码状态 | 给出 GitHub code/data 入口；本轮未打开 URL、commit 或 license 核验 |
| 数据状态 | 给出 code and data GitHub；含 SurveyGen 数据集，license 本轮未核验 |
| 许可状态 | 未核验；不得据此承诺可复现或可再分发 |
| 制品入口 | 本轮仅做 paper_content 文本级线索识别，未打开外部 URL；具体 URL、commit、license 和 smoke 运行留待下一轮 artifact audit |
| 运行可行性 | 仅related-work背景 / survey生成局部近邻 |
| 可复现资产 / 阻塞项 | 代码、数据、prompt、license、正式 venue/DOI 与 PDF 图表级数值均按 §7 / §10 待复核清单处理；未核验项不得支撑强实验比较。 |

## 2. D1-D7 全文核验评分

| 维度 | 评分 |
|---|---|
| D1 主题贴合度 | 🟢 |
| D2 SLR/SMS 流程覆盖度 | 🟡 |
| D3 LLM/agent 自动化深度 | 🟡 |
| D4 人工审计与可追踪性 | 🟡 |
| D5 评价严谨性 | 🟢 |
| D6 SE / CCF 相关性 | 🟠 |
| D7 对本文 novelty 的威胁强度 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---|---|---|
| D1 | 🟢 | `paper_content.txt` Page 1--2 Abstract/Introduction | 直接研究 scientific survey 生成 和 LLM 评价，且对自动 survey 的 引用质量 和 critical analysis 给出系统证据。 |
| D2 | 🟡 | Page 2 Task Design；Page 3 dataset construction | 覆盖 retrieval、reference selection、outline/content generation 和 evaluation；但不是 SLR/SMS 的筛选、抽取、编码和综合协议。 |
| D3 | 🟡 | Page 5 baselines；Page 20--25 prompts | 有 LLM 生成、LLM-as-judge 和 RAG framework，但没有多 agent 协作或复杂 agent 工作流，自动化深度中等。 |
| D4 | 🟡 | Page 3 full-text sections/citation locations；Page 16 human eval protocol；Page 19 data format | 数据集中保留 section、citations_in_section 和 references，评价有人类 gold standard；但没有生成阶段人工审计或 claim-to-source ledger。 |
| D5 | 🟢 | Page 5--8 metrics/results；Page 15--17 appendix metrics/human eval/ablation | 大规模数据集、多任务、多模型、自动+人工评价、ablation 和显著性标注，评价严谨性强。 |
| D6 | 🟠 | `bibtex.bib` primaryClass cs.CL；Page 5 domains | arXiv 预印本，跨 Biology/Medicine/Psychology/CS；对 SE/CCF 只是方法参照。 |
| D7 | 🟡 | Page 1 findings；Page 8--9 discussion；Page 16 human eval | 威胁 paper2 的 evaluation design 和 引用质量 claim，但不覆盖 agent 式 SLR 工作流 或 人工审计 gate。 |

## 3. 论文解决的问题与背景

SurveyGen 认为 automatic survey 生成 已成为 scientific document processing 的关键任务，但目前缺少可与 human-written surveys 对照的大规模标准数据集，导致很难严谨评估 LLM 生成 survey 的 引用质量、structural consistency 和 critical analysis。作者同时指出，已有 RAG 方法通常只看 topic/abstract semantic similarity，忽略论文质量、影响力和人类引用偏好，因此可能检索到边缘或低影响论文。

论文的目标有两个：第一，构建一个带有 human-written survey、section structure、direct citations、second-level references 和 quality metadata 的 benchmark；第二，提出 QUAL-SG，在 RAG 检索基础上加入 co-citation expansion 和 quality-aware reranking，提高 reference selection 和 survey 生成 的质量。

## 4. 方法 / 系统拆解

SurveyGen 数据集来自 S2ORC。作者先用 title filter 搜索 “a survey”“survey of”“a review”“literature review”“overview”等关键词，并要求 full-text data available、publication year after 2010，得到 8676 篇候选。之后用三个 LLM 基于 title/abstract 多数投票判断是否为 survey-type article，标准包括显式 survey intent、聚焦综述而非新方法/实验、讨论趋势/挑战/未来方向。6851 篇通过该步。再从 S2ORC bulk 取 full body、section divisions 和 citation locations，并过滤 reference 少于 30 或 top-level section 少于 3 的短文，最终得到 4205 篇 survey、115376 sections、242143 direct references 和 5062596 second-level references。

quality metadata 来自 S2ORC 与 OpenAlex，包括 citation count、influential citation count、作者 h-index/发文数/总引用、venue h-index/i10-index/CORE status 等。QUAL-SG 对 Task 2 使用 topic embedding 先检索候选，再加入至少被候选集中两篇论文共同引用的 co-cited papers。随后按三类分数重排：LLM judge topic relevance、academic impact、content diversity。最终 top-K references 数量与对应 human-written survey 的 reference count 匹配，保证公平比较。

生成任务分三类。Task 1 只给 topic，让 LLM 生成 outline、content 和 references。Task 2 给 topic 和 retrieved references 的 title/abstract/metadata，让 LLM 先生成 outline，再按 subsection 生成内容。Task 3 给 human-written survey 的 outline 和 human-selected references，模拟人类已完成选题/选文/结构后的 guided writing。

## 5. 实验 / 评价设计

实验使用 120 篇 highly cited surveys，四个领域各 30 篇：Biology、Medicine、Psychology、Computer Science。生成模型包括 GLM-4-Flash、LLaMA-3.1-70B、DeepSeek-V3、GPT-4.1-2025-04-14、Gemini-2.0-Flash、Claude-3.7-Sonnet-20250219。Task 2 对比 Fully-LLMGen、Naive-RAG 和 QUAL-SG，并以 Claude-3.7-Sonnet 作为 backbone。

自动评价分三类。Citation quality 用 generated/retrieved references 与 human-selected references 的 overlap 计算 precision、recall、F1；Task 1 还检查 generated references 是否在 S2ORC 中有 exact title match，作为 citation accuracy。Content quality 用 semantic similarity、ROUGE-L、Key Point Recall。Structural consistency 用 section semantic overlap 和 LLM-as-judge relevance 5 分制。人工评价随机选 CS 域每个 task 5 篇，共 15 篇，让 3 名二年级 CS PhD 匿名比较 LLM-generated 与 human-written surveys，在 topic relevance、information coverage、critical analysis、overall rating 上判断。

## 6. 主要结果与结论

Task 1 结果显示，全 LLM 生成的 citation reliability 仍很差。Table 2 中 Claude-3.7-Sonnet citation accuracy 最高，为 35.84%；KPR 最高 46.59%，structural overlap 最高 14.89%。作者明确写到，仅靠 LLM 生成 survey 不足以保证 reliable reference generation。

Task 2 中 QUAL-SG 明显优于 Fully-LLMGen 和 Naive-RAG。Table 3 显示 QUAL-SG citation Precision 15.87、Recall 17.71、F1 16.73；Fully-LLMGen F1 7.76，Naive-RAG F1 5.93。QUAL-SG 也在 Similarity 83.10、ROUGE-L 15.17、KPR 50.25、structural overlap 24.76 上更好。作者将提升归因于 topical relevance、academic impact 和 content diversity 的 reranking。

Task 3 表明，当提供 human-selected references 和 human-written outline 时，内容质量进一步提升。例如 Claude-3.7-Sonnet KPR 54.67，LLaMA-3.1-70B similarity 84.39、ROUGE-L 17.16。人工评价中 Task 3 在 comparable 比例上通常高于 Task 1/2，但 overall rating 中 LLM-generated > human-written 仍只有 20.0%。discussion 明确指出，LLM-generated surveys 即使 topical relevance 可比，也仍缺信息覆盖和深度分析，当前阶段不能独立达到学术标准。

## 7. 局限与可复现性

论文声明 code and data available，并在 appendix 给出 data format 和 prompts。数据结构包含 corpusId、metadata、sections、paragraph citations、citations_in_section、references 和 matched_paper_id，对 paper2 的 evidence schema 很有参考价值。评价指标公式、human eval protocol 和 ablation 也较完整。

局限包括：出于版权，生成阶段只使用 retrieved papers 的 abstracts 和 bibliographic metadata，不能读全文；没有 post-generation refinement 以节省 API 成本；不生成 figures/tables/diagrams；存在 data contamination 风险；主实验只抽取 120 篇相对短的 surveys；human evaluation 只在 CS 域 15 篇上进行。伦理声明强调 LLM-generated survey 只能作为 reference，不能替代 peer-reviewed articles 或 expert judgment。

## 8. 对 paper2 story / 实验设计的影响

SurveyGen 是 paper2 evaluation design 的重要基线。它说明只评估生成文本相似度不够，必须同时看 citation precision、citation recall、key point recall、structural consistency 和 human judgment。更重要的是，它给出强负证据：全自动生成和普通 RAG 即使能写出看似相关的内容，引用质量 和 critical analysis 仍不足。

paper2 可借鉴其 human-written survey gold standard 思路，但应将粒度推进到 SLR/SMS evidence workflow：每个纳入排除决策、抽取字段、编码类别和报告 claim 都应能绑定来源和审计状态。SurveyGen 的 Task 3 也提示，human-guided outline/reference selection 是合理上界或半自动 baseline；paper2 实验可以比较 full-auto、human-audited 和 human-guided 三种设置。

## 9. 可用于写作的引用角度

1. SurveyGen 提供了大规模 human-written survey benchmark，并证明自动 survey 生成 的 evaluation 应包含 引用质量、content quality 和 structural consistency。
2. 其结果显示 fully automatic LLM survey 生成 的 citation accuracy 仍低，支持 paper2 避免无审计自动生成的强 claim。
3. QUAL-SG 表明 reference selection 不应只依赖 topic similarity，还应考虑 co-citation、academic impact 和 diversity。
4. SurveyGen 可作为 paper2 的 evaluation inspiration，而不是 agent 工作流 baseline；paper2 的差异在于 process-level audit 和 claim evidence chain。

## 10. 待复核清单

- 未人工打开 PDF 图表；Figure 1--4 与 Table 6--8 如需精确引用，应回 PDF 核对。
- GitHub 链接需后续核验是否已 发布代码 / 数据，以及 license 是否符合本仓库使用。
- 论文 `bibtex.bib` 为 arXiv 预印本；正式引用前需核验是否有 ACL/EMNLP 等正式版本。
- QUAL-SG 权重来自作者直觉和 preliminary analysis；paper2 若采用类似 quality ranking，需避免把该权重当作普适最优。
