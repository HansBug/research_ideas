# On the road to interactive LLM-based systematic mapping studies

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | On the road to interactive LLM-based systematic mapping studies |
| 年份 | 正式期刊卷期 2025；online available 为 2024-10-31，`metadata.json` 记录 `publication_date=2024-11-01` |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 类型 | solution proposal；LLM-supported systematic mapping study 方法设想；非实证 SLR/SMS |
| SE 子领域 | LLM-supported mapping study / evidence-based software engineering 方法学 |
| 阅读状态 | 已读全文文本-paper_content核验；已回 PDF 核对 Fig. 1 映射流程图 |
| 证据等级 | 全文文本级；Fig. 1 为 PDF 图表级核对；无实证数值表可核对；补充材料未打开 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| A1 角色 | 为 survey-of-surveys 脚手架提供“LLM 介入 SMS 流程”的阶段划分、输入/输出、人机交互、agent 角色、traceability 和模型漂移风险先验。 |
| 是否目标证据池 | 是：作为 A1 方法脚手架与人机协同风险证据；否：不作为 Paper2 目标领域 finding 或“LLM 自动完成综述”的实证证据。 |
| 一句话结论 | 该文价值在于把 LLM 辅助 mapping study 拆成可讨论的流程阶段和 agent 角色；局限在于它是概念性 proposal，没有原型评测、语料分母、纳排执行或性能指标。 |

## 2. 论文内容详读

### 2.1 背景 / 问题

1. 论文从 SE 中 mapping study 的常用性出发：mapping study 主要用于分类研究和观察趋势，而 SLR 更偏证据综合。由于 mapping study 往往覆盖更大主题范围，人工分析大量论文和持续更新都很费力。
2. 作者提出使用 LLM 的动机包括：论文数量持续增加、mapping 范围可扩大、研究设计可通过与 LLM 互动获得补充想法、降低更新 mapping study 的工作量。
3. 论文明确采用 human-in-the-loop 视角：研究者仍需要懂 mapping study 方法并具备主题专家能力，才能判断 LLM 输出是否可靠。这一点对 Paper2 很关键：该文不是让系统取代专家的论证，而是“专家在环的 LLM 支持流程”设想。

证据锚点：`paper_content.txt` Page 1 Introduction；Page 1 摘要的 Context / Objective / Method / Results / Conclusion。

### 2.2 目标

论文目标不是完成一个新的 mapping study，而是讨论在 mapping study 各步骤中使用 LLM 的可能性与下一步研究方向。作者希望它作为 SE 社区讨论起点，推动一个经过评估的 holistic solution，但没有宣称已经完成该解决方案。

证据锚点：`paper_content.txt` Page 1 摘要 Objective / Conclusion；Page 1 Introduction 最后一段。

### 2.3 方法：输入 / 输出 / 流程 / 人机或 LLM 角色

论文自述方法是 solution proposal：两位作者基于自身 LLM 与 literature review 经验，迭代设计并讨论出方案。核心流程按 Petersen 等 mapping guideline 的阶段展开，Fig. 1 展示了“研究者输入与交互修订”和“LLM 输出”的对应关系；本轮已回 `paper.pdf` Page 2 核对 Fig. 1。

#### 2.3.1 Establishing a need for the map

- **用户输入**：研究目标、上下文信息，例如已有论文摘要。
- **LLM 输出**：研究问题候选、目标补充项。
- **人类角色**：编辑、筛选和确认问题，将其作为下一阶段输入。
- **可迁移点**：Paper2 scaffold 可以把“研究目标 → RQ 候选 → 人工确认”作为 stage 0，而不是让 LLM 直接固定最终 RQ。

证据锚点：`paper_content.txt` Page 2 §2.1；`paper.pdf` Page 2 Fig. 1。

#### 2.3.2 Study identification：search

作者强调搜索策略需要透明和可复现。虽然语义搜索越来越常见，但为了复现性，布尔检索仍有必要。作者提出一个以 human-in-the-loop 为中心的三 agent 架构：

1. **Keyword Identification Agent**：识别相关术语、近义词、历史术语和研究焦点层级。例如同一主题可按概念、子类型或上位类型检索。
2. **Semantic Search Agent**：用 RAG 依据语义相似度提出相关文献；可结合图数据库保存引用关系。它不直接选文献，而是辅助调整检索策略。
3. **Search Strategy Agent**：生成最终可执行的检索式或搜索策略。

作者把前两个 agent 与 citation pearl growing 关联起来：先由种子文献和语义相似文献扩展术语，再回到可复现检索式。

证据锚点：`paper_content.txt` Page 2 §2.2.1；`paper.pdf` Page 2 Fig. 1。

#### 2.3.3 Study identification：inclusion / exclusion

作者认为纳排标准捕捉研究者意图很关键，而研究者搜索意图常常不是一开始就完全显性化，因此持续学习系统可能比硬编码 prompt 更好。技术上，纳排是分类问题，但只输出 include/exclude 不够；LLM 需要给出理由、文本证据和引用，便于研究者核验。

需要注意：原文提到 chain-of-thought prompting 可帮助理解 LLM 决策。迁移到 Paper2 时，不应把它理解为必须暴露模型隐藏推理链；更稳妥的落点是要求可审计的 rationale、证据片段、引用位置和人工 override 记录。

证据锚点：`paper_content.txt` Page 2--3 §2.2.2。

#### 2.3.4 Data extraction and classification

作者区分 inductive coding 与 deductive coding：

- **归纳编码**：以标题和摘要为输入，使用 topic modeling；典型流程为生成 embedding、降维、聚类和生成 topic representation。作者举 BERTopic 作为模块化工具例子。
- **演绎编码**：已有 data extraction scheme，例如 SWE-BOK 类别；可用 one-shot / few-shot prompting，并在处理完整 PDF 时结合 RAG 先定位相关片段再调用 LLM。
- **阅读深度变化**：由于自动化能力提高，作者认为 mapping 不必只停留在 manual screening 的 adaptive reading depth，可把完整论文作为 deductive coding 输入。

证据锚点：`paper_content.txt` Page 3 §2.3。

#### 2.3.5 Visualization

作者指出 ChatGPT 已能生成可视化代码与图表，同时也出现 LIDA 等专门工具；BERTopic 可用于探索文献 landscape。Fig. 1 中用户负责提供数据表并核验图形表示的正确性和质量，LLM 输出图表、bar chart、气泡图等可视化建议或结果。

证据锚点：`paper_content.txt` Page 3 §2.4；`paper.pdf` Page 2 Fig. 1。

#### 2.3.6 Reporting

作者建议把数据表和可视化结果提供给 GPT，请其突出有趣模式、观察和研究空白；研究者再调整和补充报告。这里 LLM 角色更像 pattern spotting / drafting assistant，而不是最终结论裁决者。

证据锚点：`paper_content.txt` Page 3 §2.5；`paper.pdf` Page 2 Fig. 1。

### 2.4 研究问题或等价问题

原文没有列出正式 RQ 表。等价问题是：如何在 mapping study 流程各步骤中引入 LLM，以及每个步骤需要什么 agent、prompting、RAG、topic modeling、人类反馈和追踪机制。结尾提出两条研究方向：改进并评估单个步骤；构建覆盖整体 mapping process 的 prototype 来收集进一步想法。

证据锚点：`paper_content.txt` Page 1 Objective；Page 3 Reflections 末尾两条 research directions。

### 2.5 语料 / 纳排 / 抽取

1. **本文自身没有执行系统检索**：没有搜索库、搜索式、筛选分母、纳排清单或 primary study corpus。
2. **没有数据抽取表**：作者只引用若干相关研究来支撑每个阶段的可行性或风险，例如检索式生成、screening、topic modeling、case study 判断等。
3. **Data availability**：原文明确说明该研究没有使用数据。
4. **补充材料**：原文 DOI 下有 supplementary material，主要用于被下划线术语的定义；本轮未打开补充材料，不能把其中定义写成已核验事实。

证据锚点：`paper_content.txt` Page 3 Data availability；Page 4 References；Page 1--3 各 Relevant literature 段。

### 2.6 统计 / 分析

本文没有自己的统计分析。它通过 narrative discussion 汇总已有相关研究结论，例如：

- LLM 生成布尔检索式有潜力，但可能牺牲 recall；要求 refinement 可能提高 precision 但进一步降低 recall。
- screening 中 GPT-4 和优化 prompt 可能比 GPT-3.5 或 zero-shot 更好，但高 recall 仍是问题。
- topic modeling 和 BERTopic 可提供层次 topic、关键词和时间分析。
- GPT-4 被用于判断研究是否为 case study 的任务，并被作者作为 data extraction / classification 可能性的旁证。

这些都是“引用文献中的结果”，不是本文的独立实验结果。

证据锚点：`paper_content.txt` Page 2 §2.2.1 Relevant literature；Page 3 §2.2.2、§2.3 Relevant literature。

### 2.7 主要结果

1. 提出 LLM-supported mapping process 的阶段化设想，覆盖 need / RQ、search、inclusion/exclusion、data extraction/classification、visualization、reporting。
2. 提出 search 阶段的三 agent 角色：Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent。
3. 明确 human-in-the-loop 是核心控制点，研究者需要检查、修订、确认 LLM 输出。
4. 强调 traceability：纳排和分类需要理由、引用、证据片段，而不是只给最终标签。
5. 提出未来研究方向：分别评估单步骤策略，以及构建端到端 prototype。

证据锚点：`paper_content.txt` Page 1 Results / Conclusion；Page 2--3 §2；Page 3 Reflections。

### 2.8 效度威胁 / 限制

原文在 Reflections 中集中讨论 validity：

1. 现有研究可能存在 publication bias，且关于 LLM 在 literature review 中可靠性的研究还有限。
2. LLM 快速演化，例如不同模型和未来模型会让当前评估结果过时；这对应 Paper2 中需要处理的 provider drift / model drift 风险。
3. 很多现有研究来自 SE 之外，因此需要 SE-specific solution 和 SE-specific evaluation。
4. 原文是概念框架，不包含原型、benchmark、真实 mapping run、成本统计、错误分布或人工一致性分析。

证据锚点：`paper_content.txt` Page 3 §3 Reflections。

### 2.9 开放工件

- 论文 PDF 为开放获取，文本提取完整，共 4 页正文与参考文献。
- DOI 页面提供 supplementary material；本轮未打开，不能使用其内容作为已核验证据。
- 原文没有代码仓库、prompt set、benchmark corpus、run record 或评测数据；Data availability 声明没有使用数据。

证据锚点：`paper_content.txt` Page 1 开放获取声明；Page 3 Appendix A / Data availability。

## 3. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 不是正式 RQ 表，而是“按 mapping study 阶段提出 LLM 支持策略”的等价问题；末尾把后续研究拆为单步骤评估与端到端 prototype 两类。 | `paper_content.txt` Page 1 Objective；Page 2 §2.1；Page 3 Reflections 末尾。 | 可迁移为 Paper2 的问题分层：先问流程各阶段如何被支持，再问每阶段如何被评估。 | 不能迁移为“已验证的 RQ 生成方法”；原文没有实证 RQ 质量评价。 |
| dimension pattern | 核心维度是流程树：need/RQ、search、inclusion/exclusion、data extraction/classification、visualization、reporting；search 进一步拆出 keyword、semantic search、search strategy 三 agent；extraction 拆为 inductive / deductive coding。 | `paper_content.txt` Page 2--3 §2；`paper.pdf` Page 2 Fig. 1 已核对。 | 高度可迁移为 survey-of-surveys scaffold 的阶段维度和字段树，尤其适合把“人类输入、交互修订、LLM 输出”作为每阶段通用字段。 | 这是作者提出的 conceptual dimension，不是通过 corpus saturation 得出的分类体系；不能写成通用标准。 |
| finding pattern | finding 形态是 solution proposal 的 design claim：LLM 可在 mapping 流程各阶段提供支持，但需要专家在环、可复现检索、可追溯证据和后续评估。 | `paper_content.txt` Page 1 Results / Conclusion；Page 3 Reflections。 | 可迁移为 Paper2 的“方法启发式 finding”：将 LLM 贡献写成辅助、建议、候选生成和审计支持。 | 不能迁移为效果结论；没有证明 LLM 提升 recall、降低成本或提高综述质量。 |
| evidence presentation pattern | 证据呈现以 Fig. 1 流程图 + 各阶段 relevant literature 叙述为主；没有 PRISMA 流程图、筛选表、质量评价表或数据抽取表。 | `paper.pdf` Page 2 Fig. 1；`paper_content.txt` Page 2--3 Relevant literature；Page 3 Data availability。 | 可迁移“流程图 + stage input/output + related evidence”的报告方式，用于展示 Paper2 scaffold。 | 不可作为 empirical evidence presentation 模板；没有分母、样本、统计图或效应比较。 |
| validity / threat pattern | 原文直接指出 publication bias、研究数量有限、模型快速演化、非 SE 证据外推不足，并呼吁 SE-specific evaluation。 | `paper_content.txt` Page 3 §3 Reflections。 | 高度可迁移到 Paper2 风险章节：model drift、证据域偏移、社区评估需求、LLM reliability。 | 原文没有系统 threat checklist；没有定量分析 prompt sensitivity、人工一致性或 API 版本漂移。 |
| report structure pattern | 短期刊 proposal 结构：Introduction → LLM-supported mapping process（按阶段分小节）→ Reflections → references；没有 Method/Results/Discussion 的实证研究结构。 | `paper_content.txt` Page 1--4。 | 可迁移为方法/vision 类 paper 的结构样式：先界定痛点，再给阶段化流程，最后讨论风险与研究议程。 | 不适合作为完整 SLR/SMS 报告结构；不能替代 protocol、search、selection、quality assessment、data synthesis 等章节。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 层级 | 对 survey-of-surveys scaffold 的启发 | 证据锚点 | 采纳边界 |
|---|---|---|---|
| A1-M0：元信息与来源层 | 同一条目可能存在 online year 与正式卷期 year 差异；review 卡片应同时记录正式卷期和 online 日期，避免总账年份混乱。 | `bibtex.bib` year=2025；`metadata.json` publication_date=2024-11-01；`paper_content.txt` Page 1 available online 2024-10-31。 | 只影响元数据记录，不影响方法结论。 |
| A1-M1：综述类型层 | 该文是 solution proposal，不是 SLR/SMS/tertiary study；schema 需要允许“方法设想型文献”进入脚手架，但与实证综述样本分开。 | `paper_content.txt` Page 1 Method。 | 不能把它计为 completed mapping study。 |
| A1-M2：流程阶段层 | Fig. 1 和 §2 提供了 mapping process 的阶段维度：need、study identification、extraction、visualization、reporting。 | `paper.pdf` Page 2 Fig. 1；`paper_content.txt` Page 2--3 §2。 | 可作为候选 stage taxonomy，不是最终标准。 |
| A1-M3：人机角色层 | 每个阶段都应记录 user input、interactive refinement、LLM output；这比只记录“使用了 LLM”更可审计。 | `paper.pdf` Page 2 Fig. 1。 | Paper2 应进一步加入人工 override、时间成本、错误类型和证据锚点。 |
| A1-M4：agent / 技术机制层 | Search 阶段三 agent、RAG、graph database、BERTopic、one/few-shot、完整 PDF deductive coding 等机制可成为字段候选。 | `paper_content.txt` Page 2--3 §2.2--§2.3。 | 这些是方案组件，不能默认都有效；每个组件需要独立评估。 |
| A1-M5：证据与效度层 | 该文把 traceability、citations、publication bias、model evolution、SE-specific evaluation 放在核心位置。 | `paper_content.txt` Page 2--3 §2.2.2 与 §3。 | Paper2 需要把这些落实为 run record、source anchor、eligibility filter，而不仅是口号。 |
| A1-M6：story / method 贡献层 | 对 Paper2 的启发是“交互式、可审计、阶段化 scaffold”，不是让系统自动接管系统综述专家工作。 | 全文综合；尤其 Page 1 Introduction 与 Page 3 Reflections。 | 任何首创性口号、端到端全自动口号、取代专家口号或已验证端到端的强主张都不受该文支持。 |

## 5. 可迁移字段树 / 维度锚点

下面字段树是从原文 §2 与 Fig. 1 抽出的候选维度，用于后续 A2a/A2b scaffold 讨论；它是“可迁移字段候选”，不是最终 schema。

```text
llm_supported_mapping_study
├── metadata
│   ├── review_type: solution proposal / SMS / SLR / tertiary / guideline
│   ├── venue_and_year: formal_year + online_date
│   └── evidence_level: metadata / fulltext / pdf-figure / artifact
├── establish_need
│   ├── human_input: research_objective, context_material, seed_abstracts
│   ├── llm_output: candidate_RQs, additional_objectives
│   └── human_refinement: edited_RQs, accepted_rejected_suggestions
├── study_identification
│   ├── search
│   │   ├── search_intent: concept_level, subtype_level, supertype_level
│   │   ├── keyword_identification_agent: terms, synonyms, historical_terms
│   │   ├── semantic_search_agent: RAG, candidate_documents, citation_links
│   │   ├── search_strategy_agent: boolean_query, database_specific_query
│   │   └── reproducibility_log: query_versions, source_databases, refinement_history
│   └── inclusion_exclusion
│       ├── criteria: inclusion, exclusion, borderline_cases
│       ├── input_document: title, abstract, full_text_optional, metadata
│       ├── llm_decision: include, exclude, uncertain
│       ├── audit_evidence: rationale, cited_fragments, source_location
│       └── human_feedback: override, label_examples, continual_learning_signal
├── data_extraction_and_classification
│   ├── inductive_coding
│   │   ├── corpus_view: titles, abstracts
│   │   ├── topic_modeling_pipeline: embeddings, dimension_reduction, clustering
│   │   └── topic_outputs: labels, topic_hierarchy, temporal_patterns
│   └── deductive_coding
│       ├── extraction_scheme: taxonomy_or_standard, RQ_linked_items
│       ├── prompt_examples: one_shot, few_shot
│       ├── fulltext_processing: pdf_input, document_splitting, RAG_chunks
│       └── extracted_form: item_value, evidence_span, confidence_or_uncertainty
├── visualization
│   ├── input: data_tables, frequencies, categories
│   ├── llm_or_tool_output: plots, bar_charts, bubble_plots, topic_landscape
│   └── human_check: representation_quality, correctness, misleading_chart_risk
├── reporting
│   ├── input: tables, figures, RQs
│   ├── llm_output: pattern_suggestions, gap_suggestions, narrative_draft
│   └── human_revision: accepted_patterns, rejected_patterns, added_interpretation
└── validity_and_audit
    ├── search_risk: recall_loss, precision_recall_tradeoff, database_bias
    ├── selection_risk: low_recall_exclusion, rationale_quality, citation_support
    ├── model_risk: model_drift, provider_drift, prompt_sensitivity
    ├── domain_risk: non_SE_evidence_transfer, SE_specific_validation_needed
    └── artifact_risk: no_data, no_prompt_repo, no_run_record, no_prototype
```

### 5.1 维度 pattern 的组织原则

1. **先按流程阶段分层**：比按单个工具名分层更稳，因为工具会变，mapping study 阶段较稳定。
2. **每个阶段保留三元组**：`human_input / llm_output / human_refinement`，这是 Fig. 1 对 Paper2 最有迁移价值的结构。
3. **技术组件放在阶段内部**：例如 RAG、BERTopic、graph database、LIDA、prompt examples 都应挂在具体阶段下，避免把工具名误当成研究贡献。
4. **每个 LLM 输出必须挂 audit evidence**：纳排、抽取和报告建议都需要 source fragment、citation、query version 或人工 override；否则不进入正式证据池。
5. **validity 不是末尾附录**：检索 recall、selection recall、model drift 和 SE-specificity 应贯穿字段树，而不是最后才补一句 limitation。

## 6. 对 Paper2 story / method 的启发与风险

### 6.1 可正向迁移的启发

1. **定位为 interactive scaffold 更稳**：Paper2 可以强调“帮助研究者构建、审计和迭代综述脚手架”，而不是宣称自动完成系统综述。
2. **阶段化 agent 更容易评估**：按 need、search、selection、extraction、visualization、reporting 拆分，可以分别设计 deterministic checks、LLM judge、人工审计和 run record。
3. **可复现搜索仍要保留 Boolean/log**：原文虽认可 semantic search，但把可复现性与 Boolean search 放在关键位置；Paper2 不应只依赖语义检索或 LLM 生成候选。
4. **纳排和抽取必须 source-grounded**：LLM 输出应带理由、证据片段和引用位置；这可直接转化为 Paper2 的 evidence anchor / review trace 字段。
5. **完整 PDF 输入是机会也是风险**：原文认为 deductive coding 可从完整 PDF 获益；Paper2 可探索 full-text extraction，但必须处理 PDF 提取质量、图表缺失和上下文截断。
6. **从单步骤到端到端 prototype 的路线合理**：原文建议先优化 individual steps，再构建整体 prototype；Paper2 方法章可采用类似 staged evaluation 叙事。

### 6.2 必须避免的强主张

1. 不应写首创性或首个全自动 mapping study 系统这类口号：本文已经在 2024/2025 提出 interactive LLM-based SMS 的整体方向，且还有相关 screening/search 文献。
2. 不应写系统可以取代专家：原文明确要求研究者懂 mapping methodology 且是主题专家。
3. 不应写端到端全自动或 holistic solution 已实现：原文只是呼吁社区共同构建和评估 holistic solution。
4. 不能写“LLM 搜索已可靠覆盖文献”：原文引用的检索式生成研究反而提示 recall 下降风险。
5. 不应写符合 PRISMA：本文不是 PRISMA 报告，也没有执行系统筛选流程。

### 6.3 对 Paper2 方法的风险提示

| 风险 | 原文触发点 | Paper2 应对 |
|---|---|---|
| Search recall 风险 | GPT-generated query 可能漏掉相关论文；refinement 可能降低 recall。 | 保留人工种子、数据库搜索日志、query version、citation chasing 和 recall-oriented sanity check。 |
| 纳排透明性风险 | include/exclude 分类如果没有理由和引用，缺乏 traceability。 | 要求 evidence span、rationale、source location、人工 override；不要只存最终标签。 |
| 模型漂移风险 | 原文指出 LLM 快速演化会让当前评估过时。 | 记录 provider、model_id、调用日期、prompt、raw output、usage；不要把一次模型结果写成稳定事实。 |
| 域外证据迁移风险 | 很多 LLM literature review 研究来自 SE 之外。 | Paper2 的 claims 限定在 SE 语境，必要时设置 SE-specific pilot。 |
| 概念方案未评估风险 | 本文没有 prototype 或实验。 | Paper2 若要超越该文，需要提供可审计原型、case run、错误分析或至少真实 dry-run 证据。 |
| 工具名过拟合风险 | 文中举 BERTopic、LIDA、LangSmith、WebVoyager 等工具。 | 方法贡献应抽象为功能角色与审计接口，不绑定单一工具名。 |

## 7. 待复核

1. Supplementary material 未打开；其中被下划线术语定义未进入本 review 的已核验证据。
2. Fig. 1 已回 PDF 核对；除 Fig. 1 外，本文没有需要数值级核验的表格。
3. CCF 字段本轮沿用本仓库 ccf_venues 缓存记录 IST 为 B 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
4. 原文没有开放代码、prompt、数据或原型；如果后续要引用“artifact availability”，只能写“无数据使用 / 无代码仓库”，不要推断作者未提供所有内部材料。
5. 年份引用需统一：正式引用按 IST volume 178 (2025)；讨论 online-first 背景时可注明 2024-10-31 available online。
