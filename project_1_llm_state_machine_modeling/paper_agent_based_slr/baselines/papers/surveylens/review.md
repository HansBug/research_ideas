# SurveyLens: A Discipline-Aware Benchmark for Automatic Survey Generation

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | SurveyLens: A Discipline-Aware Benchmark for Automatic Survey Generation |
| 年份 | 2026 |
| 分层 | P0-评价协议与 benchmark 强近邻 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)；`paper_content.txt` 含少量 NUL，已容错读取；未人工打开 PDF 图表 |
| 输入 | 1000 篇人写 survey 的结构化表示、100 个生成 topic、11 个 ASG/LLM/Deep Research 系统输出 |
| 输出 | SurveyLens-1k benchmark、discipline-aware rubric、reference-based alignment metrics、跨系统评价结果 |
| 方法/系统形态 | benchmark/evaluation framework，不是新的 ASG 生成器；包含数据构建、structured survey representation、rubric lens 和 human-reference alignment lens |
| 覆盖阶段 | 评价覆盖 outline/content/reference 三类组件；生成侧覆盖 retrieval/organization/synthesis 的评估，不执行 SLR screening 或 evidence extraction |
| 人审/审计机制 | human verification PDF/outline/reference；30 名 PhD-level expert validation；retrieval leakage audit；annotation platform 和 audit logging |
| 实验/指标 | 10 学科、1000 survey、11 系统；discipline-aware rubric 1-5 分、RA-AlignF1、τ-MaxSim、structural ratios、human Spearman/Concordance、leakage audit |
| 主要发现 | Deep Research agents 跨 10 学科最稳；ASG 系统结构强、DR 内容强；reference quality 是所有范式共同瓶颈；naive recall/word count 会奖励文本膨胀 |
| 对 paper2 的作用 | 是 paper2 评价设计的重要证据来源：可借鉴 component-level evaluation、discipline-aware rubric、human alignment、leakage audit 和 reference-quality 风险分析 |
## 2. D1-D7 全文核验评分

emoji 口径：🟢 强，🟡 中，🟠 弱，⚪ 无 / 背景。

| D1 主题 | D2 流程 | D3 自动化 | D4 审计 | D5 评价 | D6 SE | D7 威胁 |
|---|---|---|---|---|---|---|
| 🟢 | 🟡 | 🟡 | 🟢 | 🟢 | 🟠 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---:|---|---|
| D1 主题贴合度 | 🟢 | Abstract；§1 Introduction；§3 SurveyLens | 论文直接研究 Automatic Survey Generation 评价，覆盖 survey/literature review 自动生成的核心近邻问题。 |
| D2 SLR/SMS 流程覆盖度 | 🟡 | §3.2 triplet $S=(O,C,R)$；§3.3；§4 evaluated systems | 评价 outline、content、reference，并面向 retrieval/organization/synthesis 后的 survey 输出；但没有筛选、编码、抽取或 protocol execution。 |
| D3 LLM/agent 自动化深度 | 🟡 | §4.1 11 systems；§3.3 LLM-as-judge rubric | 本文自身是 benchmark，使用 LLM judge 和评估多个 ASG/DR agent，不是提出新的多阶段 agent generation workflow，因此为中等。 |
| D4 人工审计与可追踪性 | 🟢 | §3.1 hybrid LLM-plus-human filtering；Appendix B.3 human verification；§4.3 human evaluation；Appendix D.2 leakage audit | 有数据构建人工核验、专家验证、annotation platform、原始 annotation 发布说明和 leakage audit，审计意识强，虽然不是 claim-level provenance。 |
| D5 评价严谨性 | 🟢 | §4.1 setup；Tables 2-6；Appendix C/D | 大规模 benchmark、11 系统、3 paradigms、专家评估、method ablation、多 judge 鲁棒性和 leakage audit，评价严谨性强。 |
| D6 SE / CCF 相关性 | 🟠 | bibtex: arXiv cs.CL；10 disciplines 含 CS 但非 SE | 泛学科 ASG/NLP benchmark，不是 SE/CCF venue，也不面向软件工程 SLR。 |
| D7 对本文 novelty 的威胁强度 | 🟡 | §3 dual-lens framework；§4 findings；Limitations | 对 paper2 的“评价协议、reference quality、human alignment、leakage audit”构成中强威胁；但不威胁 agent workflow 生成方法或 SE evidence pipeline 主体。 |

## 3. 论文解决的问题与背景

SurveyLens 解决的不是“如何生成 survey”，而是“如何公平评价不同学科中的 automatic survey generation”。作者指出现有 benchmark 多集中在 Computer Science，且使用通用指标或泛化 LLM-as-a-judge 标准，无法捕捉不同学科的写作规范。例如物理综述强调公式和推导，社会学综述更依赖定性叙事综合。

因此本文构建 SurveyLens-1k：10 个学科，每个学科 100 篇人写 survey。评价方法上提出双视角：一是 reference-free 的 discipline-aware rubric，二是 reference-based 的 human-reference alignment。该背景对 paper2 有直接启发：如果 paper2 只用通用 LLM judge 或 ROUGE 类指标评价自动综述，容易被该文指出的 discipline mismatch 和 paragraph bloat 问题击中。

## 4. 方法 / 系统拆解

SurveyLens 的输入是原始 PDF、人写 survey corpus 和被评价系统生成的 survey。数据构建从 Semantic Scholar 检索 2020-2025 年 review 类文献，使用关键词与 LLM 二分类过滤，再按 citationCount 和 influentialCitationCount 排序，每学科保留 100 篇。结构化表示为 $S=(O,C,R)$，分别表示 outline、content 和 reference list。PDF 解析采用 MinerU、规则层级/引用抽取、LLM normalization 和 human verification。

评价框架包括两条 lens。Discipline-aware rubric lens 先从已有评估方法抽取 universal aspects，再对每个学科和组件 expand/merge 成 rubric items，并用 Bradley-Terry 模型将 pairwise preferences 转成权重。Human-reference alignment lens 用 RA-AlignF1 和 τ-MaxSim 比较生成条目与人写条目：前者采用 Hungarian one-to-one matching 和 redundancy penalty，后者用 thresholded MaxSim 反映局部相似程度。

LLM/agent 角色主要是 judge、rubric synthesis 和被评价对象，不是本文生成流程。人机协作较扎实：数据构建有人核 PDF 可得性和结构表示，评价有人类专家偏好，appendix 还描述了 annotation platform、随机展示、盲标签和 audit logging。

## 5. 实验 / 评价设计

实验评估 11 个系统，分为 ASG systems、vanilla LLMs 和 Deep Research agents。ASG 系统包括 AutoSurvey、SurveyForge、AutoSurvey2、InteractiveSurvey、LLM×MapReduce-V2、SurveyX 和 SciSage；vanilla LLM 包括 Qwen3-Max 和 Gemini-3-Pro；DR 包括 Qwen DR 和 Gemini DR。每个系统接收 100 个 topic，覆盖 10 学科，每个 system-topic cell 三次试验；开放 ASG 系统统一使用 Qwen3-30B-A3B backbone。

指标包括 rubric score、RA-AlignF1、τ-MaxSim、outline/content/reference component score、structural ratios。人类验证部分包括 CS subset 的 7 名 PhD-level CS researcher method ablation，以及 9 个非 CS 学科的 22 名专家跨学科验证。Appendix 还补充 multi-judge robustness、retrieval leakage audit 和 generation failure breakdown。

## 6. 主要结果与结论

Table 2 表明 Deep Research Agents 是唯一在 10 个学科都超过学科均值的范式；ASG 系统在部分学科强，但跨学科波动更大。Table 3 和 Figure 4 显示结构与内容存在分工：ASG systems 在 outline 上强，Deep Research agents 在 content 上强，而 reference 质量普遍弱。Table 4 的 human-reference alignment 显示 τ-MaxSim 普遍高于 RA-AlignF1，说明系统能在局部段落接近人写内容，但全局组织和覆盖仍弱。

Table 5 指出 pipeline ASG 系统有明显文本膨胀：AutoSurvey 的段落数和词数可达到人写 survey 的多倍，却没有带来同等质量提升。Table 6 的 human evaluation 显示 discipline-aware rubric 与人类 outline judgment 高度相关，明显优于 holistic LLM scoring。Limitations 和 Appendix D.2 特别指出 DR outputs 存在引用或复用 paired human-written survey 的 leakage 风险，作者进行排除后分析但也承认 audit 不能捕捉全部 paraphrased reuse。

## 7. 局限与可复现性

作者列出四类局限：DR agents 对 paired human-written survey 的 citation/reuse 可能影响 reference-based metrics；rubric score 主要依赖 Qwen3-30B-A3B judge，Gemini-3-Pro 只是 secondary check；每学科只有 10 个 topic 且受 API 成本约束；10 学科仍只是代表性覆盖，不包括 humanities/law 等领域。

可复现性方面，论文声称公开 dataset、code、results 和 annotation platform，并在 ethics 中说明不发布原始 PDF，只发布 metadata、structured representations 和 URL/DOI。这比多数 ASG 论文更强。但由于它评估的是 2025 能力边界，系统排名会随模型产品变化快速失效，paper2 引用时应强调“评价方法与发现”，而不是把具体系统排名当作长期稳定事实。

## 8. 对 paper2 story / 实验设计的影响

SurveyLens 最直接影响 paper2 的实验设计。它支持 paper2 避免单一 ROUGE、BERTScore 或通用 LLM judge，改用组件级评价：outline、evidence/content、reference/citation 分开打分。同时它提醒 paper2 需要检测文本膨胀、reference hallucination、paired-source leakage 和 global organization failure。

paper2 若面向 SE SLR/SMS，可以借鉴 SurveyLens 的 dual-lens 结构，但要替换为 SE-specific rubric：protocol adherence、screening rationale、data extraction completeness、claim-to-source traceability、human adjudication quality、reproducible run record 等。相比 SurveyLens，paper2 的 novelty 应落在生成/执行和审计流程，而不是泛 ASG benchmark。

## 9. 可用于写作的引用角度

可引用为“最新 ASG 评价工作表明，跨学科 survey generation 的评价不能只依赖 CS benchmark 或通用写作指标，outline/content/reference 组件应分开评估”。也可引用为“reference quality 是 ASG、vanilla LLM 和 DR agents 的共同瓶颈，且 DR outputs 可能受 paired survey leakage 影响，需要显式审计”。

不应引用为“提出新的 agentic SLR generation method”。它的核心贡献是 benchmark 和评价，不是一个可作为生成 baseline 直接运行的 agent。

## 10. 待复核清单

- GitHub 仓库是否已公开 SurveyLens-1k structured representation、annotation platform 和 full results。
- 11 个系统的 generation prompt、topic list 和每次运行 output 是否可下载。
- Qwen3/Gemini 模型版本和官方部署配置是否随时间漂移。
- Leakage audit 是否有可复验脚本和人工核验标注。
- 若 paper2 采用其指标，需判断 RA-AlignF1 的 `τ=0.95` 和 Qwen3-Embedding-8B 是否适合 SE 文献证据。
