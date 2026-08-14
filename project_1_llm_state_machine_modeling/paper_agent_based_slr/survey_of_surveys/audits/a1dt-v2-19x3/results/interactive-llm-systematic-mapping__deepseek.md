I've now read all materials in full. Below is the complete A1-DT v2 audit report.

---

# A1-DT v2 单篇全文审计报告：`interactive-llm-systematic-mapping`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `interactive-llm-systematic-mapping` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是 — 全文 280 行，分两段逐行通读（lines 1–140、141–280），覆盖全部 4 页 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是 — 均已完整读取 |
| 是否打开或核对 `paper.pdf` | 是 — 已用 PyPDF2 抽取 4 页全文，与 paper_content.txt 逐页核验一致；Fig. 1 出现在 Page 2 顶部，确认为"映射流程 + LLM 支撑"框架图；未对 Fig. 1 做像素级视觉复核（仅文本抽取） |
| 原文类型 | **solution proposal**（非实证 SLR/SMS/tertiary） |
| 被编码样本单位 | **无系统样本库**。原文没有对任何 primary study / secondary study / tool / artifact / dataset 执行系统检索、纳排、数据抽取或逐单位编码。§2 中各步骤引用的 "Relevant literature" 是说明性例证（illustrative examples），不是通过系统检索与纳排产生的样本集。 |
| 样本数量 / 分母 | **N/A**。无检索式、无纳入排除流程、无 PRISMA-style 流程图、无样本数量报告。参考文献列表共 10 条，均为介绍性引用或背景支撑。 |
| 原生树类型 | **降级树 / 无系统样本库**。原文唯一的"结构"是 mapping study 的 5-step 流程（Fig. 1），以及各步骤的 proposed strategy / agent 角色 / 输入输出 / human-in-the-loop 交互模式。这不是对样本单位的编码维度树，而是对方法流程的分解。 |
| 主统计池资格 | **否** — solution proposal；没有已执行的系统检索、纳排与实证合成；`metadata.json` 中 `eligible_for_statistical_synthesis: false` 和 `statistical_pool_exclusion_reason` 的判定与本审计一致。 |
| 总体判定 | **pass（降级通过）** — 本文作为 solution proposal 的作用是方法学脚手架（boundary anchor / methodological seed / candidate heuristic），不应以实证 SLR/SMS 口径要求其具备编码方案、leaf 取值空间或统计池。当前 `review.md` 已正确识别了本文类型并降级处理，但对"原文 schema 主树"的复原仍需按本报告 §4 修正。 |

## 1. 原文证据阅读说明

### 1.1 实际读取的文件与范围

| 文件 | 读取方式 | 覆盖范围 |
|---|---|---|
| `bibtex.bib` | 全文 | 1 条 BibTeX entry |
| `metadata.json` | 全文 | 全部字段（Abstract、type、evidence_role、eligibility 等） |
| `paper_content.txt` | 逐行通读 | Lines 1–280，覆盖全部 4 页 |
| `paper.pdf` | PyPDF2 逐页抽取 | 4 页全部文本抽取，与 `paper_content.txt` 逐页核验 |
| `review.md` | 全文 | 436 行完整 review，含快速结论、内容详读、§3–§8 及 A.1–A.4 |

### 1.2 PDF 视觉核验状态

- Fig. 1 位于 Page 2 顶部，标题"The mapping process with LLM support"，确认存在但未做像素级视觉复核。
- 全文为纯文本结构，无统计表/数值图/附录表可核验（仅 Fig. 1 一张框架图）。
- Supplementary material 链接指向 `https://doi.org/10.1016/j.infsof.2024.107611`，本文档集合中未获取。

### 1.3 关键原文证据锚点（8 个）

| 锚点 ID | 原文章节 | 段落/表图 | 短引或释义 |
|---|---|---|---|
| EV-001 | Abstract | Page 1, lines 17–22 | "Method: The research can be classified as a solution proposal." |
| EV-002 | §1 Introduction | Page 1, lines 50–55 | "follow this human-in-the-loop approach outlined by [1]"；研究者须懂 mapping method + 主题专家 |
| EV-003 | §2 LLM-supported mapping process | Page 1, line 65; Page 2, Fig. 1 | Fig. 1 展示 mapping process 5 步与 user input / LLM output 对应 |
| EV-004 | §2.1 Establishing a need | Page 2 | 输入：研究目标+上下文；LLM 输出：RQ 提案；人类：编辑确认 |
| EV-005 | §2.2.1 Search | Page 2 | 三 agent 架构：Keyword Identification Agent、Semantic Search Agent、Search Strategy Agent；human-in-the-loop 居中 |
| EV-006 | §2.2.2 Inclusion/exclusion | Page 2–3 | 分类问题；需要 CoT 解释；citation 支撑 traceability；DSPy 与持续学习 |
| EV-007 | §2.3 Data extraction & classification | Page 3 | 归纳编码（BERTopic）+ 演绎编码（Few-shot + RAG）；全 PDF 作为输入 |
| EV-008 | §3 Reflections + Data availability | Page 3–4 | "No data was used for the research described in the article"；两个研究方向 |

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**无纳入对象。** 本文不是实证 mapping study，没有对任何 primary study 做系统纳入、逐项描述或编码。原文逐项描述的是 **mapping study 流程各步骤的 LLM 策略设计方案**，对象是"方法步骤/agent 角色/输入输出/交互模式"，而非样本论文。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**没有。** 原文明确声明 "The research can be classified as a solution proposal"（Abstract），且 Data availability 段写明 "No data was used for the research described in the article."（Page 3）。各节 "Relevant literature" 是引证已有研究以说明某步骤的可行性或挑战，不是系统检索的产品。没有检索式、纳排标准、PRISMA 流程图、数据抽取表或编码手册。

### 2.3 原文字段来自哪里？

**不存在传统意义上的 extraction form / classification schema / taxonomy / quality rubric。** 原文的"字段"（如果可以这样称呼）来自：

1. **Petersen et al. [4] 的 mapping study 流程指南** — 提供了 5 步流程的骨架：Establishing need → Study identification (Search, Inclusion/Exclusion) → Data extraction & classification → Visualization → Reporting。
2. **作者对 LLM 能力的经验判断** — 为每个步骤设计了 proposed strategy，定义了 agent 角色（Keyword Identification Agent / Semantic Search Agent / Search Strategy Agent）、技术路径（RAG / BERTopic / DSPy / CoT prompting / Few-shot）、输入输出（user input → LLM output）和 human-in-the-loop 交互模式。
3. **Fig. 1** — 将 5 步流程可视化为"研究者输入与交互修订 → LLM 输出"的对位框架。

### 2.4 RQ 与样本单位是什么关系？

本文没有传统意义上的 RQ-样本单位关系。论文目标（Objective in Abstract）是 "To discuss possibilities and next steps for using LLMs in the mapping study process"，这是一个方法学讨论目标，不是实证研究问题。因此不存在"RQ→样本单位→字段→统计"的链条。

### 2.5 如何降级？

按任务规范 §2 降级规则处理：

1. 本文为 **solution proposal**，无系统样本库。
2. 降级角色：**boundary anchor / methodological seed / candidate heuristic**。
3. 可提取的结构是 **mapping process 5-step flow** 及其 **agent 角色与交互模式**，作为跨论文方法学脚手架。
4. 不进入主统计池（与 `metadata.json` 现有判定一致）。
5. 可为 Paper2 方法学设计提供"LLM 介入 mapping study 的阶段划分与 agent 角色参考"，**不能**为 Paper2 提供领域 finding、定量统计或效应量。

## 3. 原生样本编码维度树 / 维度森林

由于本文无系统样本库，不存在对样本单位编码的维度树。本节的"维度树"是对原文 **方法流程结构** 的忠实复原——即 Fig. 1 中 mapping process 的 5 步骨架及其子结构。这**不是**样本编码树，而是 **process decomposition tree（流程分解树）**，用于理解本文的方法学贡献结构。

### 3.1 流程分解树（process decomposition tree）

```
Root: LLM-supported mapping study process (Fig. 1)
│
├── Step 1: Establishing a need for the map (§2.1)
│   ├── Input: Research objectives + contextual info (e.g., paper abstracts)
│   ├── LLM output: RQ proposals + complementary info (e.g., additional objectives)
│   ├── Human action: Edit questions, confirm for next stage
│   ├── Agent role: (未分配独立 agent；GPT prompt 直接完成)
│   └── Relevant literature: (无显式引用)
│
├── Step 2: Study identification (§2.2)
│   ├── 2a. Search (§2.2.1)
│   │   ├── Agent 1: Keyword Identification Agent
│   │   │   ├── Function: 识别相关术语、近义词、历史术语、概念层级
│   │   │   ├── Technique: 语义相似度
│   │   │   └── Example: 3D printing → concept/subtype/supertype level
│   │   ├── Agent 2: Semantic Search Agent
│   │   │   ├── Function: RAG-based 语义相似文献推荐
│   │   │   ├── Storage: graph database (citation links)
│   │   │   └── Note: 不直接选文献，辅助调整检索策略
│   │   ├── Agent 3: Search Strategy Agent
│   │   │   ├── Function: 生成最终可执行的 Boolean 检索式
│   │   │   └── Output: reproducible search strategy
│   │   ├── Interaction pattern: citation pearl growing
│   │   └── Relevant literature: Wang et al. [5] (ChatGPT for Boolean queries)
│   │
│   └── 2b. Inclusion and exclusion (§2.2.2)
│       ├── Approach: classification problem + CoT explanation
│       ├── Technical: continual learning (DSPy), users' preferences from doc in/ex
│       ├── Human role: oversight, verification via citations
│       ├── Traceability: citations as verification anchors
│       └── Relevant literature: Huotala et al. [6], Guo et al. [7]
│
├── Step 3: Data extraction and classification (§2.3)
│   ├── Premise: full PDF as input (beyond adaptive reading depth)
│   ├── 3a. Inductive coding
│   │   ├── Technique: topic modeling (embeddings → dimension reduction → clustering → topic representation)
│   │   ├── Tool: BERTopic (modular framework)
│   │   └── Relevant literature: Wang et al. [8] (BERTopic for interdisciplinary topics)
│   ├── 3b. Deductive coding
│   │   ├── Input: predefined extraction scheme (e.g., SWEBOK categories)
│   │   ├── Prompting: One-shot / Few-shot
│   │   ├── Architecture: RAG (document splitting → relevant parts → OpenAI API)
│   │   └── Relevant literature: Petersen [9] (GPT-4 for case study identification)
│   └── (inductive/deductive 不是叶子互斥，而是两种 coding 策略)
│
├── Step 4: Visualization (§2.4)
│   ├── Tool: ChatGPT code generation + data visualization
│   ├── Specialized: LIDA (Microsoft)
│   └── Exploratory: BERTopic for document landscape visualization
│
└── Step 5: Reporting (§2.5)
    ├── Input: tabular results + visualizations
    ├── LLM task: highlight patterns, observations, research gaps
    └── Human role: interpretation and writing
```

### 3.2 取值空间类型说明（对流程节点的叶子属性）

流程分解树的"叶子"是各个 strategy element，其取值空间类型与采样编码的叶子不同：

| 叶子节点 | 取值空间类型 | 取值空间 |
|---|---|---|
| Agent role（每个 step 中） | 层级枚举 | {Keyword Identification Agent, Semantic Search Agent, Search Strategy Agent} 三 agent（仅 Search step）；其他 step 无明显 agent 分配 |
| Technique（每个 step 中） | 自由文本加理由 | RAG / BERTopic / DSPy / CoT / One-shot / Few-shot / continual learning — 作者按 step 需求推荐技术路径，非穷举 |
| Human-in-the-loop pattern | 布尔 + 描述 | 所有 step 都要求 human-in-the-loop；具体交互形式因 step 而异（编辑确认 / oversight / interpretation） |
| Input type | 自由文本加理由 | 研究目标 / 上下文信息 / 预设 extraction scheme / 表格结果 — 随 step 变化 |
| Output type | 自由文本加理由 | RQ 提案 / 检索式 / 分类结果（含 rationale）/ topic clusters / 模式高亮 — 随 step 变化 |
| Relevant literature | 关系值（引证关系） | 每个 step 引用 0–2 篇已有研究作为 feasibility evidence，非系统检索产物 |

### 3.3 缺失部分与 A2a 精核任务

由于本文无系统样本库，不存在"缺失的叶子字段"的传统意义。但以下需 A2a 精核：

1. **Fig. 1 像素级视觉复核**：当前仅通过 PDF 文本抽取确认存在，未逐框核验图中每个 step 的 input/output/action 标签与正文一致。
2. **Supplementary material 获取**：文中提到 "Underlined words are defined in the supplementary material"，该材料未在本地文件集中。
3. **流程步与 Petersen et al. [4] 的原 guideline 步的精确对应关系**：需核验是否完整覆盖还是有选择性裁剪。

## 4. 叶子维度表

由于本文无系统样本库，传统叶子维度表不适用。以下表列出 **流程分解树的末端节点（process leaves）**，这些是本文方法学贡献的最小可讨论单元，而非对样本单位的编码字段。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `proc-establish-need-input` | 需求建立-输入 | Step 1 Establishing need | §2.1 正文 | 研究者向 LLM 提供的研究目标与上下文信息 | 研究目标描述 + 论文摘要等上下文 | 自由文本加理由 | 未指定输入形式规范 | 无统计用途 | Paper2 可将"研究目标→RQ 候选→人工确认"作为 stage 0 设计参考 | EV-004 | 方法学脚手架；非统计池 |
| `proc-establish-need-output` | 需求建立-LLM输出 | Step 1 Establishing need | §2.1 正文 | LLM 生成的研究问题提案与补充信息 | RQ 候选列表 + 补充目标项 | 自由文本加理由 | 未指定输出格式 | 无统计用途 | 作为 agent-loop 中 RQ generation 步骤的参考 | EV-004 | 同上 |
| `proc-establish-need-human` | 需求建立-人类角色 | Step 1 Establishing need | §2.1 正文 | 人类编辑、筛选、确认问题的动作 | 编辑/筛选/确认 | 层级枚举（3 值） | N/A | 无统计用途 | human-in-the-loop 模式参考 | EV-004 | 同上 |
| `proc-search-kw-agent` | 检索-关键词 Agent | Step 2a Search | §2.2.1 Agent 1 | 识别相关术语、近义词、历史术语和研究焦点层级的 agent | {存在, 不存在} + 功能描述 | 布尔 + 自由描述 | 未指定实现细节 | 无统计用途 | 多 agent 架构参考 | EV-005 | 同上 |
| `proc-search-sem-agent` | 检索-语义搜索 Agent | Step 2a Search | §2.2.1 Agent 2 | 基于 RAG + 图数据库的语义相似文献推荐 agent | {存在, 不存在} + 功能描述 | 布尔 + 自由描述 | 未指定实现细节 | 无统计用途 | RAG 在文献检索中的应用参考 | EV-005 | 同上 |
| `proc-search-strategy-agent` | 检索-策略生成 Agent | Step 2a Search | §2.2.1 Agent 3 | 生成最终可执行 Boolean 检索式的 agent | {存在, 不存在} + 功能描述 | 布尔 + 自由描述 | 未指定实现细节 | 无统计用途 | 可复现检索式生成参考 | EV-005 | 同上 |
| `proc-search-interaction` | 检索-交互模式 | Step 2a Search | §2.2.1 | citation pearl growing 策略：keyword + semantic agent 联动 | {citation pearl growing, 未指定其他} | 自由文本加理由 | N/A | 无统计用途 | 人机协同检索迭代模式参考 | EV-005 | 同上 |
| `proc-inclusion-approach` | 纳排-方法路径 | Step 2b Inclusion/exclusion | §2.2.2 | 将 inclusion/exclusion 作为分类问题，要求 LLM 提供 CoT 解释与 citation 支撑 | 分类 + CoT 解释 + citation | 自由文本加理由 | 未指定分类阈值/评估标准 | 无统计用途 | traceability 与可解释性的设计参考 | EV-006 | 同上 |
| `proc-inclusion-learning` | 纳排-持续学习 | Step 2b Inclusion/exclusion | §2.2.2 | 通过 DSPy 等框架从用户的 inclusion/exclusion 偏好中持续学习 | {DSPy 优化, 未指定其他学习框架} | 自由文本加理由 | 未指定学习数据量要求 | 无统计用途 | 持续学习/自适应 prompt 设计参考 | EV-006 | 同上 |
| `proc-extraction-inductive` | 抽取-归纳编码 | Step 3 Data extraction | §2.3 1.Inductive coding | 用 BERTopic 做 topic modeling：embeddings → 降维 → 聚类 → topic representation | BERTopic pipeline（模块化可替换组件） | 外部分类法引用（BERTopic 框架） | 未指定具体 embedding model / clustering 算法 | 无统计用途 | 归纳编码自动化路径参考 | EV-007 | 同上 |
| `proc-extraction-deductive` | 抽取-演绎编码 | Step 3 Data extraction | §2.3 2.Deductive coding | 用 One-shot/Few-shot + RAG 按预定义 extraction scheme 做逐文档编码 | One-shot / Few-shot prompting + RAG architecture | 层级枚举（prompt 策略）+ 自由描述 | 未指定 extraction scheme 模板 | 无统计用途 | 演绎编码自动化路径参考 | EV-007 | 同上 |
| `proc-visualization` | 可视化 | Step 4 Visualization | §2.4 | LLM 生成可视化代码（ChatGPT / LIDA）+ BERTopic 探索性可视化 | ChatGPT code gen / LIDA / BERTopic vis | 自由文本加理由 | 未指定可视化质量标准 | 无统计用途 | 综述可视化 pipeline 参考 | — | 同上 |
| `proc-reporting` | 报告生成 | Step 5 Reporting | §2.5 | 将表格结果与可视化输入 GPT，请求高亮模式/观察/研究空白 | GPT 分析表格+可视化 → 文本高亮 | 自由文本加理由 | 未指定表格/可视化格式要求 | 无统计用途 | 综述报告半自动化参考 | — | 同上 |

## 5. 关系边表

本文未定义显式的关系型 schema（如样本之间的引用关系、层级关系、演化关系等）。但流程步之间存在**顺序依赖**和**信息流转**关系。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `flow-1-to-2` | Step 1 Establishing need | 顺序依赖 + 信息传递 | Step 2 Study identification | Step 1 的人类确认后的 RQ 作为 Step 2 输入 | 未显式建模，仅 Fig. 1 暗示顺序 | EV-004, Fig. 1 | 理解流程整体性 |
| `flow-2a-to-2b` | Step 2a Search | 顺序依赖 | Step 2b Inclusion/exclusion | 检索结果作为纳排输入 | 未显式建模 | Fig. 1 | 理解 sub-step 顺序 |
| `flow-2-to-3` | Step 2 Study identification | 顺序依赖 + 信息传递 | Step 3 Data extraction | 纳入文献集作为抽取输入 | 未显式建模 | Fig. 1 | 理解流程整体性 |
| `flow-3-to-4` | Step 3 Data extraction | 顺序依赖 | Step 4 Visualization | 抽取结果作为可视化输入 | 未显式建模 | Fig. 1 | 同上 |
| `flow-4-to-5` | Step 4 Visualization | 顺序依赖 | Step 5 Reporting | 可视化产物作为报告输入 | 未显式建模 | Fig. 1 | 同上 |
| `human-in-loop-all` | Human (common) | 跨步交互 | All steps | 编辑/确认/监督/解释 | 所有 step 均声明 human-in-the-loop，但交互粒度未统一 | EV-004, EV-005, EV-006, EV-007 | human-in-the-loop 全流程约束 |

**未发现显式关系边**：原文没有定义 agent-agent 通信协议、样本间引用图、或编码字段间推导关系。流程步间的信息传递是隐含的（通过 Fig. 1 的视觉顺序暗示），没有正式建模为数据流或 schema 关系。各 step 的 "Relevant literature" 与被引用文献之间是引证关系，但不是本论文内部的 schema 关系。

## 6. 统计观察、候选 finding 与 final finding 边界

### 6A. 原文中由字段/统计表支持的统计观察

**无。** 本文不含任何统计表、数值结果、效应量或量化比较。文中引用的外部研究结果（如 Wang et al. [5] 的 F-Measure、Huotala et al. [6] 的 human-LLM 一致性）来自被引用文献，不是本文的实证产物。

### 6B. 原文 discussion / recommendation / roadmap 提出的候选 finding

以下来自 §3 Reflections，属于 **作者意见/建议（candidate heuristic）**，不具备实证 finding 的证据等级：

| 候选 finding ID | 内容 | 证据基础 | 等级 |
|---|---|---|---|
| CF-01 | GPT 在文献筛选中的表现与人类相当或更好 | 引用已有研究（非本文实证） | candidate heuristic |
| CF-02 | LLM 快速迭代使当前评估迅速过时 → 需要概念框架 | 作者观察 + 推理 | candidate heuristic |
| CF-03 | 很多现有 LLM-for-review 研究来自 SE 外部 → 需 SE-specific 方案 | 作者观察 | candidate heuristic |
| CF-04 | 两个研究方向：(1) 优化单步策略；(2) 构建端到端 prototype | 作者建议 | roadmap item |
| CF-05 | LangSmith 用于 LLM 系统 tracing，WebVoyager 用于 grey literature | 工具推介 | methodological seed |

### 6C. 对 Paper2 可迁移的方法学启发

1. **LLM 介入 mapping study 的 5-step 阶段框架** — 可作为 Paper2 自身 agent-based SLR 方法设计的参考骨架。
2. **Human-in-the-loop 的全程约束** — 明确研究者必须在每个步骤判断 LLM 输出可靠性，对 Paper2 的自动化程度边界有警示意义。
3. **Multi-agent 架构分解**（Keyword ID / Semantic Search / Search Strategy）— 可启发 Paper2 的 agent 角色设计。
4. **Traceability 与 citation 支撑** — 要求 LLM 提供可检验的论证与引用，可作为 Paper2 的 auditability 设计要求。
5. **归纳 + 演绎双轨编码** — BERTopic + Few-shot RAG 的组合，可为 Paper2 的分类方案设计提供技术选型参考。

### 6D. 绝不能迁移的领域结论

- 本文关于 SE mapping study 的任何具体领域 finding、趋势声明或论文分类。
- 本文引用的外部实证结果（如 Wang et al. [5] 的 recall/precision 数据），除非 Paper2 独立核验该被引文献。
- 本文声称的"GPT 性能与人类相当"等论断 — 这是对已有研究的综述性陈述，不是本文的实证结论，也不一定适用于 Paper2 的目标领域（控制系统状态机建模）。

## 7. 对现有 `review.md` 的返修建议

### 分级说明
- **C（Critical）**：影响事实正确性或统计池资格判定，必须修复。
- **I（Important）**：影响维度树复原准确性或下游可用性，应修复。
- **M（Minor）**：措辞、格式或可读性改进。

### 7.1 C 级

| ID | 问题 | 位置 | 建议 |
|---|---|---|---|
| C-01 | review.md §3 维度树复原章节中，叶子维度表（`leaf-interactive-llm-systematic-mapping-orig-sms-stage` 等 4 个 "orig" 叶子）将 mapping process step、LLM intervention type、researcher interaction pattern、traceability risk 列为"原文 schema 候选叶子"。但这些不是对样本编码的叶子，而是对方法流程的分解。review.md §3 未明确区分"流程分解"与"样本编码树"。 | review.md §3 + A.1 叶子表 | 在 §3 开头显式声明：本文无系统样本库，以下为"方法流程分解"而非"样本编码维度树"。将叶子类型标注从 `leaf_definition` 改为 `process_leaf` 或等效区分标记。 |
| C-02 | review.md SUMMARY 表中（A.1 部分）未在第 1 页快速结论卡片中明确标注"降级树 / 无系统样本库"，当前 `原生树类型` 字段在快速结论卡片中缺失。 | review.md §1 快速结论卡片 | 在 §1 表中增加字段 "原生树类型 | 降级树（无系统样本库；solution proposal）" 并增设 "样本单位 | 无（solution proposal，非实证 SMS）" 和 "样本数量/分母 | N/A"。 |

### 7.2 I 级

| ID | 问题 | 位置 | 建议 |
|---|---|---|---|
| I-01 | review.md §3 的维度树复原混合了"原文流程分解"和"通用六叶接口投影"。当前 A.1 叶子表中的 `leaf-interactive-llm-systematic-mapping-scope` 等 7 个"通用六叶叶子"是用 reviewer 视角套上的跨论文投影，不是原文自己的分类结构。 | review.md §3 + A.1 叶子表 | 将通用六叶叶子标记为 "cross_projection"（跨论文投影），与原文流程分解的 process leaf 分表呈现。在 §3 正文说明哪些是原文自有的结构、哪些是 reviewer 构造的投影。 |
| I-02 | review.md §6 中 "对 Paper2 可迁移的方法学启发" 与原文 §2.1–§2.5 的对应关系未逐条锚定证据锚点。 | review.md §6 | 为每条迁移启发追加原文证据锚点 ID（如 EV-004, EV-005 等）。 |
| I-03 | review.md A.2 证据账本中的 `EV-interactive-llm-systematic-mapping-003` 将 "Fig. 1 的 5-step 映射流程作为维度树根" 列为证据。但 Fig. 1 是流程框架图，不是维度树定义。证据角色应更精确。 | review.md A.2 | 将 EV-003 的证据角色从 `dimension_tree_root` 改为 `process_framework_diagram`。 |
| I-04 | review.md A.3 结论-证据映射表中，`A1DT-interactive-llm-systematic-mapping-C02` 声称"原文为 solution proposal，维度树降级为流程分解"的结论强度为 `weak`。考虑到原文 Abstract 明确声明 solution proposal + Data availability 段声明 "No data"，该结论强度应调整为 `strong`。 | review.md A.3 | 将 C02 的 `结论强度` 从 `weak` 改为 `strong`，并补充 Data availability 段的证据引用。 |

### 7.3 M 级

| ID | 问题 | 位置 | 建议 |
|---|---|---|---|
| M-01 | review.md A.1 叶子表中，多个叶子的 `取值空间类型` 列为 `free_text_with_rationale`，但未给出具体的 rational 说明。 | review.md A.1 | 为每个自由文本叶子简要说明 why-rationale（例如："原文未指定输出格式，属概念性描述"）。 |
| M-02 | review.md A.4 本地复验命令表中，`needs_manual_check` 状态的 `cmd-interactive-llm-systematic-mapping-visual-check` 指向 Fig. 1 视觉复核 + supplementary material 核验。建议补充具体的核验 checklist（如"逐框核对 Fig. 1 中每个 step label 与正文一致"）。 | review.md A.4 | 增加核验 checklist 条目（3–5 条），例如：(a) Fig. 1 5 步标签是否完整覆盖 §2.1–§2.5；(b) supplementary material 中 "underlined words" 定义是否影响流程理解。 |
| M-03 | review.md 中文措辞偶有冗长，如 A.3 表中部分 `结论内容` 字段过长（"19×3 全文审计表明本文必须以'原文 schema 主树'作为维度树事实源..."）。 | review.md A.3 | 精简为 1–2 句核心判定，细节留在 A.2 证据账本。 |

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-INT-001 | paper_content.txt | Abstract | Page 1, lines 17–18 | "The research can be classified as a solution proposal." | 原文类型判定 | strong | 降级树判定、统计池排除 | 否（文本明确） | 无 |
| EV-INT-002 | paper_content.txt | §3 / Data availability | Page 3, line 247 | "No data was used for the research described in the article." | 无样本库确认 | strong | 样本单位=N/A 判定 | 否（文本明确） | 无 |
| EV-INT-003 | paper_content.txt + paper.pdf | §2, Fig. 1 | Page 2, Fig. 1 caption | "Fig. 1. The mapping process with LLM support." | 流程框架图 | medium（需要像素级复核各框标签） | process decomposition tree 根 | 是（像素级复核各框内容与正文一致） | 图含 layout 信息，文本抽取可能丢失部分标签 |
| EV-INT-004 | paper_content.txt | §2.1 | Page 2, §2.1 整段 | "we provide the LLM with our research objectives and contextual information...We edit the questions as input for the next stage." | Step 1 输入/输出/人类角色定义 | medium | proc-establish-need-* 三个叶子 | 否（文本一致） | 仅限本文的 mapping process 语境 |
| EV-INT-005 | paper_content.txt | §2.2.1 | Page 2, §2.2.1 3-agent 描述 | "Keyword Identification Agent...Semantic Search Agent...Search Strategy Agent" | Step 2a 三 agent 架构与功能定义 | medium | proc-search-* 四个叶子 | 否（文本明确） | agent 实现细节未指定 |
| EV-INT-006 | paper_content.txt | §2.2.2 | Page 2–3, §2.2.2 | "classification problem...Chain-of-thoughts prompting...citations are indispensable" | Step 2b 纳排策略定义 | medium | proc-inclusion-* 两个叶子 | 否（文本一致） | 技术路径未具体实现 |
| EV-INT-007 | paper_content.txt | §2.3 | Page 3, §2.3 Inductive/Deductive coding | "BERTopic...One-shot or Few-shot prompting...RAG architecture" | Step 3 归纳/演绎编码策略定义 | medium | proc-extraction-* 两个叶子 | 否（文本一致） | BERTopic 参数、RAG 实现细节未指定 |
| EV-INT-008 | paper_content.txt | §1 | Page 1, lines 50–55 | "human-in-the-loop approach...reviewers (a) are well educated in using the mapping study method, and (b) be experts in the topic" | Human-in-the-loop 全流程约束 | medium | 所有 process leaf 的 human role 子节点 + relation `human-in-loop-all` | 否（文本明确） | 交互粒度未定义 |
| EV-INT-009 | paper_content.txt | §2.4–§2.5 | Page 3, §2.4–§2.5 | "ChatGPT...LIDA...BERTopic...tabular results and result visualizations" | Step 4 可视化 + Step 5 报告策略 | medium | proc-visualization + proc-reporting | 否（文本一致） | 工具链细节未指定 |
| EV-INT-010 | paper_content.txt | §3 | Page 3, §3 整段 | "two research directions: Improving individual steps...Build a prototype" | roadmap items | medium | 候选 finding CF-04 | 否（文本明确） | 方向性建议，非实证结论 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-INT-001 | 本文是 solution proposal，非实证 SMS/SLR | 原文类型判定 | 降级树根 | EV-INT-001, EV-INT-002 | strong | 统计池排除；降级为 boundary anchor / methodological seed | 无有效反证 |
| C-INT-002 | 本文无系统样本库，不存在样本编码维度树 | 结构判定 | 维度树根 | EV-INT-001, EV-INT-002 | strong | A1-DT v2 降级处理：输出 process decomposition tree 而非 sample coding tree | 无有效反证 |
| C-INT-003 | 本文的方法学贡献可分解为 5-step mapping process + 各步骤的 strategy elements（agent 角色/输入输出/技术路径） | 结构复原 | process decomposition tree（§3.1） | EV-INT-003, EV-INT-004, EV-INT-005, EV-INT-006, EV-INT-007, EV-INT-009 | medium | 方法学脚手架；跨论文流程参考 | Fig. 1 像素级复核未完成；supplementary material 未获取 |
| C-INT-004 | 本文的 5-step 流程步之间存在隐含顺序依赖与信息传递关系 | 关系复原 | relation edges（§5） | EV-INT-003 (Fig. 1 视觉顺序) | weak | 理解流程整体性；不可作为形式化 workflow 规范 | Fig. 1 是概念框架图，非形式化数据流模型；隐含关系未在正文显式建模 |
| C-INT-005 | 本文提出的 3-agent 检索架构（Keyword ID / Semantic Search / Search Strategy）可为 Paper2 的 agent 设计提供参考 | 候选发现/迁移 | proc-search-* 叶子 | EV-INT-005 | weak | 方法学启发；不可直接作为 Paper2 的 agent 实现方案 | agent 实现细节未指定；未经验证 |
| C-INT-006 | 本文明确要求 human-in-the-loop 覆盖全流程，研究者必须是 mapping method 专家 + topic 专家 | 设计约束/迁移 | human-in-loop-all 关系边 + 所有 process leaf 的 human role 子节点 | EV-INT-008 | medium | Paper2 方法学设计的 automaton 边界约束 | 交互粒度未定义；原文未给出违反此约束的后果 |
| C-INT-007 | 本文的两个研究方向（单步优化 + 端到端 prototype）是 roadmap item，非实证结论 | 候选 finding | CF-04 | EV-INT-010 | weak | 研究方向参考；不可作为"已被文献支持的下一步工作" | 方向性建议，无实施评估 |
| C-INT-008 | 现有 review.md 的通用六叶接口投影不应与原文流程分解混淆 | 审计返修 | review.md 返修建议 I-01, I-02 | EV-INT-001, EV-INT-003 | medium | review.md 重写指导 | 需主线程确认后执行修改 |

## 9. 技能使用与自我审查记录

### 9.1 技能文件使用记录

| 技能文件 | 路径 | 采用的原则 |
|---|---|---|
| ai-research-writing-skill SKILL.md | `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | 证据优先原则（evidence gate：repository files outrank memory）；claim gate（no unsupported strong claim）；"证据不足就降级"策略 |
| reviewer-guidelines.md | `.../ai-research-writing-skill/references/reviewer-guidelines.md` | 通用审查维度（Originality / Quality / Clarity / Significance / Reproducibility / Ethics）；Constructive Specificity Standard（reviewer-quality objection 必须具体到作者可行动）；section-level check（Abstract/Introduction/Method/Experiments 的审查要点） |
| reviewer-self-review.md | `.../ai-research-writing-skill/references/reviewer-self-review.md` | 五维评分（Contribution/Writing/Experimental/Method/Responsibility）；Claim Audit 模板（claim → evidence → risk → revision → status）；Adversarial Questions（作为 skeptical reviewer 的质问清单） |
| research-planning SKILL.md | `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 研究计划结构化方法（Overall Plan → Architecture → Logic → Configuration）；依赖图分析 |
| planning-prompts.md | `.../research-planning/references/planning-prompts.md` | Paper2Code 四轮规划对话模式；AI-Researcher Plan Agent 的 workflow（Code Review → Dataset → Model → Training → Testing） |
| output-schemas.md | `.../research-planning/references/output-schemas.md` | 输出 schema 模板（research_question → methodology → paper_structure → task_list → experiment_design → risks） |
| autoresearch SKILL.md | `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | Validator-gated loop 原则（completion 是 artifact-gated，不是模型声称"done"）；completion artifact contract（对实证产出的刚性验证要求）— 此原则映射到本审计：不能因为 review.md 已声称"完成维度树复原"就不再核验原文，必须有原文证据支持 |

### 9.2 本输出最高风险 3 点

| 风险等级 | 风险描述 | 主线程合并时复核建议 |
|---|---|---|
| **高** | Fig. 1 未做像素级视觉复核。当前仅通过 PDF 文本抽取确认 Fig. 1 存在于 Page 2 顶部，但未逐框核验每个 step 的 input/output/action label 与正文 §2.1–§2.5 的文字描述是否完全一致。如果图中包含正文未提及的细节（如额外子步骤、不同命名），process decomposition tree 的准确性会受影响。 | 主线程合并前，人工打开 `paper.pdf` 逐框核验 Fig. 1，将图像 label 与 §2.1–§2.5 正文做逐 step 比对。若发现不一致，更新 process decomposition tree 的对应节点。 |
| **中** | Supplementary material 未获取。文中声明 "Underlined words are defined in the supplementary material"（Page 2 footnote 2），此材料可能包含术语定义、技术细节或流程约束，若缺失可能导致对某些 strategy element 的理解偏差。 | 尝试从 DOI 链接获取 supplementary material；若无法获取，在 review.md 中显式声明该缺失并标注为待补。 |
| **中** | Process decomposition tree 的取值空间（§3.2）均为自由文本加理由或层级枚举，没有任何一个叶子有"完整枚举"。这意味着 Paper2 不能直接将这些叶子作为定量编码字段使用，只能作为方法设计参考。当前 review.md 中部分叶子的 `取值空间类型` 标注可能暗示比实际更确定的语义。 | 主线程逐 leaf 复核取值空间类型标注，确保 "free_text_with_rationale" 的叶子都有明确的 rationale 说明。 |

### 9.3 Blocked / Timeout / 文件缺失状态

| 状态 | 说明 |
|---|---|
| **未 blocked** | 所有必读文件均可读，无任务级阻塞 |
| **未 timeout** | 本任务在单次 exec 进程中完成 |
| **文件缺失** | Supplementary material 未在本地文件集中；`paper.pdf` 内 Fig. 1 未做像素级视觉复核（仅文本抽取）— 此为 `needs_manual_check` 而非 blocked |

---

**审计完成。** 本报告为自包含完整报告，所有必填章节均已给出实质内容。不可作为"通用 SLR checklist"或"论文总结"使用；核心产出是：(1) 确认本文为 solution proposal / 无系统样本库，(2) 将原文结构正确归类为 process decomposition tree 而非 sample coding tree，(3) 提供可直接迁移到 review.md 返修的 C/I/M 建议和 A.2/A.3 草案。