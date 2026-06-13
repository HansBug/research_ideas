# AutoSurvey2: Empowering Researchers with Next Level Automated Literature Surveys

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | AutoSurvey2: Empowering Researchers with Next Level Automated Literature Surveys |
| 年份 | 2025，arXiv:2510.26012 v3 |
| 分层 | 全文建议 P1-/P2+：结构化 survey generation pipeline 近邻，非严格 SLR/SMS |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工 PDF 核对 |
| 核验入口 | `bibtex.bib`；`paper_content.txt` Page 1--15，文件含 NUL，阅读时临时去除 NUL |
| 输入 | 用户 topic；arXiv 元数据/摘要库；配置中的 LLM provider、embedding model、检索参数 |
| 输出 | IEEE 风格 `survey.tex`、`survey.bib`、`state.json`、research log/状态文件 |
| 方法/系统形态 | PostgreSQL + pgvector 检索库；DAG/state-machine 式四阶段 pipeline；OutlineGeneration、PaperSearch、ContentAnalysis、ContentSynthesis、PaperGeneration、post-processing 节点 |
| 覆盖阶段 | 数据库构建、outline planning、section-level retrieval/analysis/synthesis、LaTeX 生成、citation extraction、BibTeX/DBLP enhancement、Judge Agent 评价 |
| 人审/审计机制 | 有状态快照和引用后处理，鼓励 human review；没有生成中人工 gate、双人审计或逐 claim 证据包 |
| 实验/指标 | 10 个代表性主题；top-k 100、threshold 0.7、最多 1500 reference papers、8 sections、20 papers/section；Judge Agent 评价 Coverage/Structure/Relevance |
| 主要发现 | AutoSurvey2 平均 4.76，高于 AutoSurvey 4.60 和 Naive RAG 4.23；移除 planner 时 Structure 明显下降；局限承认仍需 verification modules 和 human-in-the-loop review |
| 对 paper2 的作用 | 可作为“stateful automated survey writing pipeline”近邻；paper2 需在 SLR/SMS 语境、人工审计、claim evidence 和可复现实验记录上差异化 |
## 2. D1-D7 全文核验评分

| 维度 | 评分 |
|---|---|
| D1 主题贴合度 | 🟢 |
| D2 SLR/SMS 流程覆盖度 | 🟡 |
| D3 LLM/agent 自动化深度 | 🟡 |
| D4 人工审计与可追踪性 | 🟡 |
| D5 评价严谨性 | 🟡 |
| D6 SE / CCF 相关性 | 🟠 |
| D7 对本文 novelty 的威胁强度 | 🟡 |

| 维度 | 评分 | 全文证据锚点 | 判定理由 |
|---|---|---|---|
| D1 | 🟢 | `paper_content.txt` Page 1--2 摘要和 Introduction | 论文直接研究 LLM 自动生成 long-form academic surveys，属于 paper2 baseline 库的核心邻域。 |
| D2 | 🟡 | Page 2--9 四阶段 workflow | 覆盖检索、分析、生成、引用后处理和评价，但没有 SLR/SMS 的筛选协议、抽取字段、编码、质量评价表或证据综合流程。 |
| D3 | 🟡 | Page 4 Figure 1；Page 5--8 stage descriptions | 有多节点 LLM pipeline 和 Judge Agent，但不像 SurveyG/Agentic AutoSurvey 那样明确多 agent 分工；自动化深度较高但 agentic 性质中等。 |
| D4 | 🟡 | Page 8 state JSON；Page 8--9 citation extraction/DBLP；Page 11 limitation | 保存 `state.json`、related papers 和 section papers，具备工程 trace；但人类审计、claim-to-source 和决策日志仍缺失，作者也把 human-in-the-loop review 放到未来工作。 |
| D5 | 🟡 | Page 9--11 Experiments/Results；Tables 1--2 | 有 baseline、ablation 和参数设置，但评价主要来自 Judge Agent 三维 Likert 分，缺少人工专家、统计显著性和 raw generation 复验细节。 |
| D6 | 🟠 | `bibtex.bib` primaryClass cs.AI；Page 9 topics | arXiv 预印本，泛 AI/academic writing；没有软件工程 SLR 或 CCF venue 事实。 |
| D7 | 🟡 | Page 2 contributions；Page 4 shared state；Page 8 post-processing | 对 paper2 的 stateful workflow 和引用后处理 claim 有局部威胁，但没有 SLR 人审闭环与报告级 evidence provenance。 |

## 3. 论文解决的问题与背景

AutoSurvey2 关注的是快速增长的 LLM/AI 文献使人工 survey 写作变难。作者把已有问题概括为三类：LLM context window 难以容纳大型文献语料；模型内部知识无法保证最新性和引用真实性；LLM-generated academic content 缺乏标准化评价协议。基于此，论文提出 end-to-end automated framework，把检索、结构规划、section writing、LaTeX assembly 和自动评价组合到一个可复现 pipeline 中。

这篇论文与 paper2 的关系是“自动 survey 写作流水线”而非“系统综述方法学”。它没有构造 SLR/SMS 的研究问题、纳排标准、质量评价与编码流程，也没有正式报告规范约束。其重要性在于 state management 和 citation post-processing，这些会影响 paper2 对 run record 与 evidence trace 的表述方式。

## 4. 方法 / 系统拆解

系统先构建 arXiv 语义检索库：通过 Kaggle 官方 Cornell-University/arxiv dataset 获取元数据，保留 cs.AI、cs.CL、cs.CV、cs.LG、stat.ML 等类别，用 nomic-embed-text-v2-moe 生成 768 维摘要向量，并存入 PostgreSQL + pgvector。后续所有检索都依赖该向量库。

生成流程分为四阶段。Stage 1 Research Planning 根据用户 topic 检索默认 1500 篇参考论文，由 LLM 生成默认 8 个 section 的 outline。Stage 2 Research Phase 针对每个 section 用 `topic + section` 检索默认 20 篇，ContentAnalysis 只分析 top 5 篇，提取 findings、themes、methods，再交给 ContentSynthesis 写 section。Stage 3 PaperGeneration 生成摘要、结论和 IEEE LaTeX，并把 metadata、topic、outline、related papers、section papers、generated sections 和 final paper 序列化到 JSON。Stage 4 post-processing 用正则提取 `\cite{}`，从 arXiv metadata 生成 BibTeX，再查询 DBLP 替换正式发表版本，并整理 LaTeX 包和 bibliography。

人机协作方面，正文没有人工参与生成或审计环节。审计更接近工程 trace：shared state、stage_results、citation keys 和 BibTeX 后处理。伦理声明中作者明确建议发布前人工 review。

## 5. 实验 / 评价设计

原文未以 RQ 形式列出问题。实验评估 pipeline 生成 long-form survey 的效果和模块贡献。设置为 PostgreSQL 本地库、nomic embedding、GPT-4.1 作为 outline、section writing 和 refinement backbone；vector search top-k 为 100，相似度阈值 0.7；每篇 survey 最多考虑 1500 篇 reference papers，生成 8 个 sections，每 section 检索 20 篇。

评价使用 Judge Agent，将 expert review criteria 转成 Coverage、Structure、Relevance 三个 1--5 Likert 维度，并零温度推理以增强可复现性。实验覆盖 10 个代表性主题，横跨 computer science、mathematics、physics。对比 baseline 包括 AutoSurvey 和 Naive RAG。另有 ablation：w/o planner 和 w/o refactor。

## 6. 主要结果与结论

Table 1 显示 AutoSurvey2 在 Coverage 4.72、Structure 4.68、Relevance 4.88、Avg 4.76 上均高于 AutoSurvey 的 4.60 和 Naive RAG 的 4.23。作者认为 graph-based planning 和 semantic retrieval 提高了结构连贯性和主题覆盖。Table 2 显示去掉 planner 后 Avg 下降到 4.35，Structure 从 4.68 降到 3.78；去掉 refactor 后 Avg 为 4.57，说明规划模块对结构最关键。

结论强调 structured planning、retrieval augmentation 和 iterative refinement 可以缓解 context length 与知识滞后问题，提升 scalable academic writing。但这些结论必须限定在 Judge Agent 评价和所选主题范围内，不能扩展成对真实学术可发表性或 SLR 合规性的证明。

## 7. 局限与可复现性

论文给出了 GitHub 链接、公式化 stage 描述、参数和输出文件类型，可复现性基础强于只给 prompt 的系统。`state.json` 设计对 paper2 有启发：中间状态应保存 topic、outline、related papers、section papers 和 generated sections。

局限也很明确。系统依赖底层 literature database 的完整性；并行 section generation 可能导致风格不一致；生成和评价都依赖 LLM，继承 factual inaccuracies、citation errors 和 bias；verification modules 与 human-in-the-loop review 仍是未来工作。另一个重要边界是 ContentAnalysis 默认只分析每 section top 5 papers，因此即使检索到 20 篇，也不代表每篇都被深度综合。

## 8. 对 paper2 story / 实验设计的影响

AutoSurvey2 迫使 paper2 不要把“保存中间状态”写成完全新颖点。更稳妥的差异化是：AutoSurvey2 保存的是生成流水线状态，而 paper2 应保存 SLR/SMS 决策证据，包括 query、screening decision、extraction cell、coding decision、claim support、human audit action 和 failed/partial run eligibility。

实验上，paper2 可以借鉴其 ablation 设计，但评价不能只用 LLM judge 的 Coverage/Structure/Relevance。应加入人工审计一致性、claim support precision/recall、unsupported claim 分类、citation grounding、run record completeness 和 reviewer workload。对于引用后处理，paper2 可以借鉴 arXiv/DBLP normalization，但必须保留“引用支持了哪个 claim”的证据，而不仅是 BibTeX 能生成。

## 9. 可用于写作的引用角度

1. AutoSurvey2 展示了自动 survey 写作可以被组织成 state-machine/DAG 式 pipeline，并输出 LaTeX、BibTeX 与 serialized state。
2. 其 citation extraction 和 DBLP enhancement 说明引用格式标准化是 survey generation 系统的重要后处理，但不等价于 claim-level evidence verification。
3. 其限制段落可用于支撑 paper2 的论点：仅靠 LLM 生成和 LLM 评价仍会留下事实错误、引用错误和 bias，需要 verification 和 human-in-the-loop。
4. paper2 可将其定位为 long-form academic survey generation baseline，而非 SLR/SMS evidence synthesis baseline。

## 10. 待复核清单

- 未人工打开 PDF 图表；Figure 1 的 state-machine 细节如需截图引用，应回 PDF 核对。
- GitHub 仓库链接需后续访问核验代码是否完整、是否含数据和 prompt。
- Table 1/2 为 Judge Agent 结果，若写入论文 related work，应明确不是人工专家评审。
- 原文提到 DBLP 替换正式版本，但未给出错误率；paper2 不应把它当成已验证 citation accuracy 的证据。
