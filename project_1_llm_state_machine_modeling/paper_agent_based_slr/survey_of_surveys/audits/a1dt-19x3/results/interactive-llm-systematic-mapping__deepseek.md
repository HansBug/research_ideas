# interactive-llm-systematic-mapping · deepseek 全文审计报告

## 1. 审计身份与输入

| 项 | 值 |
|---|---|
| reviewer 身份 | deepseek |
| 审计日期 | 2026-06-29 |
| 是否读取 `$ai-research-writing-skill` | 是。读取路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，以及 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` |
| 是否读取 `$research-planning` | 是。读取路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`，以及 `references/planning-prompts.md` |
| 是否读取 `$oh-my-codex:autoresearch` | 是。读取路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` |
| 是否完整阅读 `paper_content.txt` | 是。280 行全部阅读，覆盖 Page 1（摘要、Introduction）、Page 2（§2.1--§2.2.2 Fig. 1、Search、Inclusion/Exclusion）、Page 3（§2.3 Data extraction/classification、§2.4 Visualization、§2.5 Reporting、§3 Reflections、Data availability）、Page 4（References）。每节正文均逐段核验，未只读摘要或 grep。 |
| 是否核对 `paper.pdf` | 否。因本审计环境无法以可视方式打开 PDF；但已确认 `paper.pdf` 文件存在（953KB）。review.md 声称已回 PDF 核对 Fig. 1，本审计接受该声称但标注为"原文图表级核对依赖 review.md 自我声明，deepseek 未独立视觉复核"。所有需要 PDF 图表核对才能定论的结论，在本文中标注为 `需要原文版面复核`。 |
| 是否读取文库规则与 story | 是。已读取：`survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md`、`../story/paper_story.md`。 |
| 是否读取单篇文件 | 是。已读取 `bibtex.bib`、`metadata.json`、`paper_content.txt`（全文）、`review.md`（全文）。 |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

本文没有列出正式 RQ 表。等价目标是「讨论在系统映射研究（Systematic Mapping Study, SMS）各步骤中使用大语言模型（如 GPT-4）的可能性与下一步研究方向」。[1] 原文定位为 **solution proposal**，而非已执行的 SMS。

贡献声明分布在两处：
- 正文（§2）：按 SMS 流程 6 个阶段，逐一提出 agent / prompting / RAG / topic modeling / 可视化 / 人类反馈策略。
- 结尾（§3 Reflections）：提出两条研究路线——(a) 改进单个步骤并评估不同策略（如 prompting），(b) 构建覆盖整体 mapping process 的 prototype。

证据锚点：`paper_content.txt` Page 1 摘要 Objective / Results / Conclusion；Page 1 Introduction 最后两段；Page 3 §3 末尾。

### 2.2 原文方法流程

论文自述方法为 solution proposal，两位作者基于 LLM 与 literature review 经验迭代设计并讨论。**未执行实际系统检索、纳排、数据抽取或统计**。核心流程按 Petersen 等 [4] mapping guideline 的阶段展开，Fig. 1 展示了每阶段的用户输入 / 用户动作 / LLM 输出的循环。

完整 6 阶段流程（来自 Fig. 1 + §2 正文）：

| 阶段 | 用户输入 | 用户动作 | LLM 输出 | 关键方法/工具锚点 |
|---|---|---|---|---|
| **§2.1 Establishing need** | 研究目标、上下文信息（如论文摘要） | 编辑、筛选、确认 RQ | 研究问题候选、目标补充项 | -- |
| **§2.2.1 Search** | 搜索意图 | 审核术语、反馈、迭代 refinement | 三 agent 协作：①Keyword Identification Agent（识别术语/近义词/历史术语/层级）；②Semantic Search Agent（RAG 语义文献+图数据库引用）；③Search Strategy Agent（最终检索式） | citation pearl growing；Wang et al. [5] |
| **§2.2.2 Inclusion/Exclusion** | 包含/排除决策（通过学习系统积累） | 分类论文并检查 LLM 理由 | 分类决策+CoT 理由+引用；DSPy 优化 prompt | Huotala et al. [6]；Guo et al. [7] |
| **§2.3 Data extraction/classification** | 数据抽取方案（如 SWE-BOK 类别） | 定义方案、审核编码结果 | ①**Inductive coding**：BERTopic（embedding→降维→聚类→主题表示）；②**Deductive coding**：One-shot/Few-shot prompting + RAG（先定位文档片段再调用 API） | Wang et al. [8]；Petersen [9] |
| **§2.4 Visualization** | 数据表 | 核验图形的正确性和质量 | 图表/bar chart/气泡图生成或可视化建议；LIDA 工具 | LIDA；BERTopic |
| **§2.5 Reporting** | 表格结果、可视化 | 审核并裁决 | 高亮数据中令人兴奋的模式和观察（如研究缺口） | -- |

证据锚点：`paper_content.txt` Page 2 §2.1--§2.2.2；Page 3 §2.3--§2.5；`paper.pdf` Page 2 Fig. 1（review.md 声称已核对；deepseek 未独立视觉复核）。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme

**这篇文章没有已执行的 extraction form**——它是 proposal，不是完成的 SMS。但它**显式定义了以下分类 / 编码 / taxonomy 模式**：

| 原文模式 | 类型 | 具体内容 | 原文位置 |
|---|---|---|---|
| SMS 流程阶段 taxonomy（6 阶段） | 流程分类 | ①确立需求 → ②检索（含三 agent 子分类）→ ③纳排 → ④数据抽取与分类 → ⑤可视化 → ⑥报告 | §2 + Fig. 1 |
| 搜索 agent taxonomy（3 agent） | 架构分类 | ①Keyword Identification Agent / ②Semantic Search Agent / ③Search Strategy Agent | §2.2.1 |
| 编码模式 taxonomy（2 类） | 方法分类 | ①Inductive coding（topic modeling / BERTopic）/ ②Deductive coding（extraction scheme + Few-shot + RAG） | §2.3 |
| 每阶段的人机交互模式 | 角色分类 | user input → user action → LLM output 三元组，含 verify / refine / approve / classify / review | Fig. 1 |
| 可追溯性风险 taxonomy | 风险分类 | 纳排缺乏理由和引用、模型漂移、域外证据迁移、recall 下降、概念方案未评估 | §2.2.2 + §3 |
| 后续研究路线（2 条） | roadmap | ①改进并评估单步骤策略 / ②构建端到端 prototype | §3 末尾 |

**原文没有的内容**（避免脑补）：
- 没有正式的 extraction form 字段表
- 没有正式的证据质量评价 rubric
- 没有 formal coding scheme 的完整枚举
- 没有 PRISMA 流程图或筛选分母
- 没有统计结果表或效应量比较

证据锚点：上述各点均已在上表标注原文位置；Fig. 1 来自 `paper.pdf` Page 2（review.md 自我声明核对；deepseek 未独立视觉复核）。

### 2.4 原文如何形成 conclusion / finding / gap / recommendation

原文的形成路径是**论证型**而非**统计型**：

1. 按 SMS 流程阶段逐一提出 LLM 介入策略（Fig. 1 + §2）。
2. 每阶段引用 relevant literature 作为可行性旁证（而非系统验证）——例如 Wang et al. [5] 对 GPT 生成检索式的评估、Huotala et al. [6] 对 GPT 筛选的性能比较。
3. 在 §3 Reflections 中汇总效度风险（publication bias + limited studies + model evolution）、推荐互补工具（LangSmith / WebVoyager）、提出两条研究路线。
4. **结论是方向性呼吁**："we should work on a holistic solution"、"inspire further research"。没有声称已证明任何策略优于人工或不需人工。

这意味着该文的 "finding" 不能以跨论文统计频次或效应量的方式出现——它是 **boundary anchor**，只能贡献流程结构、人机角色和风险先验。

## 3. 当前 `review.md` 维度树审计

### 3.1 树结构全景审视

当前 review.md 的维度树呈现为**双层结构**：

- **上层**：5 个主干分支（b1 SMS流程阶段、b2 LLM/agent介入点、b3 researcher interaction、b4 traceability risk、b5 proposal boundary），每个分支挂 1 个（b5 挂 2 个）**通用叶子接口**（scope / corpus / taxonomy / method / evidence / finding）。
- **下层**：4 个"原文模式候选叶子"（orig-sms-stage / orig-llm-intervention / orig-researcher-interaction / orig-traceability-risk），被标注为 `not_verified` 和 `schema_seed`。

review.md 已经通过"A1-DT 叶子层口径校准"声明「下方"叶子维度表"的六个 `leaf-*` 是跨论文通用接口层」且「原文模式候选叶子已在『原文模式候选叶子映射（A1 种子）』中逐条列出」。**但问题不在是否有这句声明，而在树结构的实际呈现是否造成系统性的误导。**

### 3.2 逐项审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | **通过** | `[dim-interactive-llm-systematic-mapping-root]` 用论文标题作为根节点标识，说明"roadmap action / guideline item / schema seed"，与论文 solution proposal 性质一致。单位对象识别准确。 | 通过 |
| 主干分支是否覆盖原文 schema | **I — 覆盖不全且语义映射偏差** | 5 个主干分支（b1--b5）是按跨论文 A1-M0--M6 框架设计的**方法学分析维度**，而非对本文内部 schema 的忠实复原。具体问题：(1) b1「SMS 流程阶段」→ leaf「scope」：原文的 6 阶段 taxonomy 是论文核心贡献，不应只降解为 scope 子节点。(2) b2「LLM/agent 介入点」→ leaf「corpus」：原文的 3-agent 搜索架构 + inductive/deductive coding 元分类应在 b2 下有专门子维度，而非被合并进 corpus。(3) b3「researcher interaction」→ leaf「taxonomy」：原文 Fig. 1 的 user input / user action / LLM output 三元组是论文最具原创性的 pattern，当前只作为候选叶子的候选取值空间，未作为正式叶子编码。(4) b4「traceability risk」→ leaf「method」：原文 §2.2.2 纳排透明性 + §3 效度威胁是独立内容轴，不应被"方法/技术/干预分类"吸收。 | I |
| 叶子维度是否足够具体 | **I — 6 个通用叶子接口不足以代表原文全部维度** | 6 个通用叶子（scope / corpus / taxonomy / method / evidence / finding）是对任何 SLR/SMS 综述都通用的抽象层，它们**不是本文特有的维度**。本文的独特维度（6 阶段流程 taxonomy、3-agent 搜索架构、inductive/deductive coding 元分类、Fig. 1 三元组模式、两条研究路线）在树结构中只以"候选叶子"形式出现且全部 `not_verified`。虽然 review.md 澄清了这是跨论文接口而非原文叶子全集，但**树的视觉呈现让 reader 第一眼看到的是 6 个通用接口，而非原文真实的 10+ 个候选维度**。这违反了 `pattern-field-schema.md` §8.2 的要求：「叶子必须回到原文具体字段，不得停留在跨论文抽象」。 | I |
| 取值空间是否可执行 | **I — 候选叶子的取值空间过于泛化** | 4 个候选叶子的取值空间均为开放自由文本（「研究问题、检索、筛选、分类、统计、报告等 SMS 阶段」「LLM 可辅助的检索、分类、抽取、聚类、总结和交互步骤」「确认、修改、追问、证据质疑、迭代 refinement 等 human-in-the-loop 行为」）。这些取值空间是**描述性短语列表**，不是可统计的枚举值。例如 `orig-sms-stage` 的取值空间应精确为 {establish_need, search_keyword, search_semantic, search_strategy, inclusion_exclusion, data_extraction_inductive, data_extraction_deductive, visualization, reporting} 这 9 个子阶段，但当前写成「研究问题、检索、筛选、分类、统计、报告等 SMS 阶段」丢失了原文的精细结构。 | I |
| 关系边是否缺失 | **I — 阶段-GPT 策略映射边缺失** | 原文 §2 中每个流程阶段都映射到具体的 GPT/LLM 策略（如 search 映射到 keyword agent / semantic search agent / search strategy agent），且每个策略映射到具体的 prompting 方法（如 inclusion/exclusion 映射到 CoT + DSPy）、具体工具（BERTopic / LIDA / LangSmith）和具体引用文献。当前维度树的 4 个候选叶子是**平行列表**，没有建立「阶段 → GPT 策略 → 工具/文献」的横向关系边。`pattern-field-schema.md` §8.3 要求关系边至少包含源节点、关系类型、目标节点和目标取值空间。 | I |
| 统计用途 / 分母是否正确 | **通过** | 正确判定为 `eligible_for_statistical_synthesis=false`，理由充分：「solution proposal；没有已执行的系统检索、纳排与实证合成」。所有叶子正确标记为「不进入主统计池；只作 schema seed / boundary anchor」。 | 通过 |
| 候选 finding 路径是否完整 | **M — 路径框架存在但内容空泛** | A.3 结论-证据映射中，每个 leaf 的候选发现用途写为「可生成与"XXX"相关的候选发现，需研究者裁决」——这是一个**模板化的占位句**，没有给出针对本文的具体候选发现线索。例如本文确实提供了可操作线索：如「GPT 生成检索式 recall 可能下降 → Paper2 需保留 recall-oriented sanity check」「纳排分类缺乏 traceability → Paper2 需记录 evidence span + rationale + source location」。这些在 §6.3 对 Paper2 方法的风险提示中已有，但未回链到 A.3 候选发现台账。 | M |
| A.1--A.4 证据链是否足够 | **M — 证据引用均为泛定位** | A.2 证据账本中关键证据 EV-002（支撑 taxonomy + 所有 candidate leaf）的原文定位写为「方法 / 结果页；待 A2a 精确页码复核」「extraction / taxonomy / action point 邻近段落」。这违反了 `pattern-field-schema.md` §8.4 对证据账本的要求：「原文页码、原文章节、段落或行号范围、表格或图编号」。当前所有 `not_verified` 证据均无精确页码锚点（虽然 paper_content.txt 是纯文本提取，但可用行号或 § 编号代替页码）。此外，证据强度全部为 `not_verified`，与 A.3 的结论强度 `weak` 之间的降级逻辑未被显式文档化。 | M |
| 是否存在可能误导 A2a 的强主张 | **C — 树结构以通用接口为主体会误导 A2a 对原文的理解** | 这是本审计最严重的问题。当前树结构在视觉上呈现为「5 分支 + 6 通用叶子」，而原文真实的 10+ 个维度被埋在"候选叶子"表中且全部 `not_verified`。如果 A2a 的 agent 或研究者只看树结构（不细读"候选叶子"表），会误以为这篇论文的维度就是 scope/corpus/taxonomy/method/evidence/finding 这 6 个通用概念——这不仅是疏漏，而是**系统性偏差**。具体风险：(a) A2a 会把 6 个通用叶子误当成该论文对 A1-M0--M6 的具体贡献；(b) 原文独有的 6 阶段 taxonomy + 3-agent 架构 + inductive/deductive 分类 + Fig. 1 三元组 + 2 条研究路线等富含领域知识的维度会被忽略；(c) 当与其他 18 篇论文的维度树合并时，本论文会被错误地代表为"满足了 6 个通用维度"，而非"贡献了 SMS+LLM 交互流程这一独特维度类型"。 | C |

## 4. 建议维度树骨架

以下是更忠实于原文的维度树。该树的设计原则是：**原文有什么就复原什么，不为了和跨论文接口对齐而强行归类**。

```
[dim-root] On the road to interactive LLM-based systematic mapping studies
│   类型：solution proposal / boundary anchor
│   证据等级：全文文本级；Fig. 1 待独立视觉复核
│   统计池：不进入
│
├── [dim-b1] 系统映射流程阶段 taxonomy（6 阶段）          ← 原文 §2 + Fig. 1
│   ├── [leaf-sms-stage] 流程阶段
│   │   取值空间：{establish_need, search, inclusion_exclusion,
│   │            data_extraction_classification, visualization, reporting}
│   │   可统计：否（单篇 proposal，无跨论文频次）
│   │   证据：§2.1–§2.5; Fig. 1
│   │
│   └── [leaf-sms-substage] 子阶段（search + extraction 下层）
│       取值空间（search）：{keyword_identification, semantic_search, search_strategy}
│       取值空间（extraction）：{inductive_coding, deductive_coding}
│       可统计：否
│       证据：§2.2.1 (search 3-agent); §2.3 (inductive/deductive)
│
├── [dim-b2] 每阶段的 LLM 介入策略                     ← 原文 §2.2–§2.5
│   ├── [leaf-llm-technique] LLM 技术/方法
│   │   取值空间：{RAG, one_shot_prompting, few_shot_prompting,
│   │            chain_of_thought, DSPy_prompt_optimization,
│   │            BERTopic_topic_modeling, embedding_clustering}
│   │   关系边：[leaf-llm-technique] -- deployed_at --> [leaf-sms-stage]
│   │   证据：§2.2.1 RAG; §2.2.2 CoT + DSPy; §2.3 BERTopic + Few-shot
│   │
│   ├── [leaf-llm-agent-role] LLM agent 角色
│   │   取值空间：{keyword_identifier, semantic_searcher,
│   │            search_strategist, document_classifier,
│   │            data_extractor, topic_modeler, visualizer, pattern_spotter}
│   │   证据：§2.2.1 (3 agent); §2.3–§2.5
│   │
│   └── [leaf-llm-tool] 引用工具/库
│       取值空间：{BERTopic, LIDA, LangSmith, WebVoyager, DSPy, GPT}
│       关系边：[leaf-llm-tool] -- used_for --> [leaf-sms-stage]
│       证据：§2.2.2 DSPy; §2.3 BERTopic; §2.4 LIDA; §3 LangSmith, WebVoyager
│
├── [dim-b3] 人机交互模式（per stage）                   ← 原文 Fig. 1 三元组
│   ├── [leaf-human-input] 研究者输入类型
│   │   取值空间：{objectives_context, search_intent,
│   │            inclusion_exclusion_decisions, extraction_scheme,
│   │            data_tables, tabular_results}
│   │   关系边：[leaf-human-input] -- feeds_into --> [leaf-sms-stage]
│   │
│   ├── [leaf-human-action] 研究者动作类型
│   │   取值空间：{edit_approve_rq, review_refine_terms,
│   │            classify_papers_check_rationale,
│   │            define_scheme_review_coding,
│   │            verify_visualization_correctness,
│   │            review_adjudicate}
│   │   关系边：[leaf-human-action] -- after_receiving --> [leaf-llm-output]
│   │
│   └── [leaf-llm-output] LLM 输出类型
│       取值空间：{rq_candidates, search_terms, semantic_document_suggestions,
│                search_strategy, classification_with_rationale,
│                extracted_data_coded, topic_clusters, visualization_code,
│                pattern_observation}
│       关系边：[leaf-llm-output] -- presented_to --> [leaf-human-action]
│
├── [dim-b4] 可追溯性与效度风险                          ← 原文 §2.2.2 + §3
│   ├── [leaf-traceability-mechanism] 可追溯性机制
│   │   取值空间：{chain_of_thought_rationale, citation_verification,
│   │            data_provenance_log, prompt_version_tracking}
│   │   证据：§2.2.2 "language models have to explain the reasons";
│   │         "citations are indispensable"
│   │
│   └── [leaf-validity-threat] 效度威胁
│       取值空间：{publication_bias, limited_evaluation_studies,
│                model_rapid_evolution, domain_generalization_gap,
│                search_recall_risk, untested_proposal}
│       证据：§3 "Study validity"; §2.2.1 recall risk
│
├── [dim-b5] 后续研究路线（roadmap）                      ← 原文 §3 末尾
│   └── [leaf-research-direction] 研究路线
│       取值空间：{improve_evaluate_individual_steps,
│                build_end_to_end_prototype}
│       证据：§3 末尾
│
└── [dim-b6] 出版与制品元数据                              ← 原文 Data availability
    ├── [leaf-artifact-status] 制品状态
    │   取值空间：{no_data_used, no_code_repository,
    │           supplementary_terms_defined,
    │           supplementary_not_opened}
    │   证据：§Data availability "No data was used";
    │         §2.2.1 "Underlined words are defined in the supplementary material"
    │
    └── [leaf-publication-meta] 出版元数据
        取值空间：{journal_IST, year_2025, ccf_B, oa_hybrid,
                online_first_2024_10_31}
        证据：bibtex.bib + metadata.json
```

### 4.1 新旧树对比

| 维度 | 旧树（当前 review.md） | 新树（本审计建议） | 差异 |
|---|---|---|---|
| 主干分支数 | 5（b1--b5） | 6（b1--b6） | 新增 b6 制品元数据维度 |
| 正式叶子数 | 6 个通用接口 leaf | 12 个原文特定 leaf | 从跨论文抽象 → 原文具体维度 |
| 取值空间 | 自由文本 + 短语列表 | 封闭/半封闭枚举值 | 可统计性提升（虽然本论文不进入统计池） |
| 关系边 | 无 | 4 组有向关系边 | `deployed_at` / `used_for` / `feeds_into` / `presented_to` |
| 原文 SMS 阶段 | 只在候选叶子 `orig-sms-stage` 中以短语列表出现 | 正式 leaf `sms-stage` + `sms-substage`，取值精确到 9 个子阶段 | 从"候选种子" → 正式维度 |
| 原文 Fig. 1 三元组 | 模糊分布在 b1/b2/b3 通用接口中 | 独立 dim-b3 映射 input → action → output 三元组 | 论文核心 pattern 得到独立编码 |
| 原文效度讨论 | 被合并进 traceability risk | 独立 leaf `validity-threat` | 区分了机制与威胁 |
| 原文研究路线 | 未出现 | 独立 dim-b5 | 补漏 |
| 原文制品状态 | 只在 §6.3 risk 表中以「未评估风险」出现 | 独立 leaf `artifact-status` | 补漏 |

### 4.2 为什么当前树不够

当前树采用的跨论文 6 通用 leaf 结构虽然在"统一 19 篇论文的汇总视角"上有一致性优势，但对于**单篇审计**而言存在根本性缺陷：

1. **信息损失**：原文 10+ 个维度被压缩为 6 个通用接口，丢失了原文具体的 taxonomy 内容（如 9 个 SMS 子阶段、7 种 LLM 技术、8 种 agent 角色、6 种效度威胁、2 条研究路线）。
2. **语义漂移**：b1→leaf-scope 意味着将"SMS 流程阶段"解释为"研究范围与单位对象"——这是两个不同的概念。
3. **不可审计**：A2a 无法从当前树中判断哪些维度来自原文、哪些来自跨论文框架，也无法追踪具体取值空间的原文来源。
4. **累积风险**：如果 19 篇论文都这样处理，A2a/A2b 的 cross-paper synthesis 将建立在被通用接口过滤过的信息上，导致维度多样性被系统性低估。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| **修改维度树主干结构** | review.md "维度树结构" 代码块 | 将 5 个 b1--b5 分支替换为 §4 建议的 6 分支（b1--b6）结构，每分支挂原文特定叶子而非通用接口。保留当前的 6 个通用 leaf 作为"跨论文元维度标签"（即标注原文叶子对应 A1-M0--M6 哪个元维度），但不再作为树的主干叶子。 | 原文 §2--§3；Fig. 1 | **C** |
| **补充 Fig. 1 三元组正式叶子** | review.md 叶子维度表 | 新增 dim-b3 下的 3 个 leaf（human-input / human-action / llm-output），取值空间按 §4 建议的封闭枚举填写。 | 原文 Fig. 1（`paper.pdf` Page 2） | **C** |
| **细化取值空间到可枚举水平** | review.md "原文模式候选叶子映射" 表 | 4 个候选叶子的取值空间从自由文本短语改为 §4 建议的封闭/半封闭枚举值。例如 `orig-sms-stage` 改为 {establish_need, search_keyword, search_semantic, search_strategy, inclusion_exclusion, data_extraction_inductive, data_extraction_deductive, visualization, reporting}。 | 原文 §2.1--§2.5 正文 | **I** |
| **增加维度间关系边** | review.md 新增"关系边表" | 补 4 组关系边：LLM technique → SMS stage (deployed_at)；tool → stage (used_for)；human input → stage (feeds_into)；LLM output → human action (presented_to)。 | 原文 Fig. 1 + §2 正文 | **I** |
| **补充效度威胁独立叶子** | review.md 叶子维度表 | 新增 `leaf-validity-threat`，枚举原文 §3 明确的 6 项效度风险。 | 原文 §3 "Study validity" | **I** |
| **补充研究路线独立叶子** | review.md 叶子维度表 | 新增 `leaf-research-direction`，枚举原文 §3 末尾的 2 条路线。 | 原文 §3 末尾 | **M** |
| **补充制品状态独立叶子** | review.md 叶子维度表 | 新增 `leaf-artifact-status`，记录 "No data was used" + supplementary 未打开 + 无代码仓库。 | 原文 Data availability 声明 | **M** |
| **为 A.2 证据添加精确定位** | review.md A.2 证据账本 | 所有 `not_verified` 证据（EV-001, EV-002, EV-003, EV-004）从当前「摘要 / 引言页；待 A2a 精确页码复核」升级为使用 paper_content.txt 行号 + § 编号 + 段落定位（如「`paper_content.txt` §2.2.1, lines ~89--119, "Keyword Identification Agent" 段」）。虽然不如原版 PDF 页码精确，但至少可被 audit trail 追踪。 | paper_content.txt 行号 + § 编号 | **M** |
| **A.3 候选发现填充具体线索** | review.md A.3 结论-证据映射 | 当前模板化占位句「可生成与"XXX"相关的候选发现」替换为 review.md §6.3 中已有的 6 条具体风险线索（search recall、纳排透明性、模型漂移、域外迁移、未评估、工具过拟合），并回链到对应证据。 | review.md §6.3 风险表 | **M** |
| **新增 A.5 缺失维度登记** | review.md 新增 A.5 节 | 登记当前维度树未覆盖的原文内容：supplementary 未定义术语、两条研究路线、"No data was used"声明、引用文献 per stage 映射模式。说明为何当前未进树（是 A2a 待补还是非维度化信息），避免后续误判为遗漏。 | 原文 supplementary 引用 + Data availability | **M** |

## 6. C/I/M 结论

### 6.1 C（Critical）—— 直接破坏 Paper2 学术目标或证据链

| C 编号 | 问题 | 影响 |
|---|---|---|
| **C1** | 维度树以 6 个跨论文通用 leaf 接口为主体呈现，将原文 10+ 个真实维度降级为候选种子。视觉上让 reader 误以为该论文的维度就是 scope/corpus/taxonomy/method/evidence/finding。 | 若 A2a 基于此树做 cross-paper synthesis，会系统性地：(a) 把 19 篇论文都压入 6 个通用维度，掩蔽不同论文的独特维度类型差异；(b) 使"SMS+LLM 交互流程"这一独特维度类型无法被统计。这直接破坏 Paper2 「综述之综述必须抽取多样性维度模式」这一学术目标。 |
| **C2** | 原文 Fig. 1 的三元组模式（user input → user action ↔ LLM output）是论文最具原创性的 schema 贡献，但在当前树中没有正式叶子编码。 | Fig. 1 三元组是本文对 "human-in-the-loop systematic mapping" 的核心形式化，丢失它将使 A2a 无法识别"人机交互模式"作为一个独立维度类型存在。这直接影响 Paper2 对脚手架维度多样性的判断。 |

### 6.2 I（Important）—— 实质影响维度树可用性或证据可审计性

| I 编号 | 问题 | 影响 |
|---|---|---|
| **I1** | 主干分支 b1--b5 的语义映射偏差（b1→scope, b2→corpus, b3→taxonomy, b4→method, b5→evidence/finding）。 | A2a 按此树执行 cross-paper field mapping 时，会将原文「SMS 流程阶段」误标记为「scope 维度」，将「LLM agent 角色」误标记为「corpus 维度」。字段级错误映射会污染 A2b 的统计池。 |
| **I2** | 4 个候选叶子的取值空间为自由文本短语，不可统计。 | 虽然本论文不进入主统计池，但取值空间的设计直接影响 A2a 对维度类型的判断（是可统计分类轴还是自由文本描述）。过于泛化的取值空间会使得本论文在与其他 boundary anchor 比较时无法对齐。 |
| **I3** | 维度间关系边缺失（阶段-GPT策略、策略-工具、输入-阶段）。 | Paper2 的核心贡献之一是「维度模式演化 + 证据链」，关系边是实现该贡献的基础设施。缺失关系边意味着后续 cross-paper synthesis 只能做扁平统计，无法做结构化交叉分析。 |
| **I4** | 原文显式的效度威胁讨论 + 两条研究路线未被编码为维度叶子。 | 效度威胁和 roadmap 是综述之综述方法论的核心关注点（A1-M4/M6）。遗漏这些内容会削弱本论文对 Paper2 方法评估和 finding 裁决的启发价值。 |

### 6.3 M（Minor）—— 不阻塞的清晰度或维护性建议

| M 编号 | 问题 | 建议 |
|---|---|---|
| **M1** | A.3 候选发现采用模板化占位句，未填充本文的具体风险线索。 | 从 §6.3 复制 6 条具体风险线索到 A.3，并回链证据。 |
| **M2** | A.2 证据全部 `not_verified` 且无精确行号/§ 定位。 | 用 paper_content.txt 行号 + § 编号作为过渡性定位（A2a 再升级为 PDF 页码）。 |
| **M3** | 缺少 A.5 缺失维度登记。 | 新增 A.5 登记：supplementary 未打开术语、两条研究路线、"No data was used"。 |
| **M4** | 叶子维度表中"证据要求"列写的是全文级描述（"方法章节、protocol、search/selection 描述"），但这些在该论文中不适用（没有 protocol / search execution）。 | 标注为 "not_applicable: 本文为 solution proposal，该证据类型不适用"。 |
| **M5** | 没有记录原文 supplementary 中下划线术语未核验这一已知空白。 | 在 A.4 人工核验清单中新增一项：`supplementary_terms_check` — 打开 supplementary PDF 核对被定义术语列表。 |

### 6.4 最终建议

**NEEDS FIX**。

当前 review.md 的维度树存在 2 个 C 级问题和 4 个 I 级问题。虽然 review.md 通过"A1-DT 叶子层口径校准"和"原文模式候选叶子映射"展示了自知之明，但这不能弥补树结构本身的**系统性偏差**。核心矛盾在于：**跨论文通用接口（6 leaf）被放在了"维度树"的位置，而原文真实维度（10+ 候选叶子）被放在了"待精核种子"的位置**。这在逻辑上是颠倒的——维度树应该首先忠实复原原文 schema，然后才标注每个原文维度可以映射到哪个 A1-M0--M6 元维度。

**最小修复路径**（按优先级）：

1. **替换维度树结构**（修 C1/C2）：将树从「5 分支挂 6 通用 leaf」改为 §4 建议的「6 分支挂 12 原文特定 leaf」。
2. **细化取值空间**（修 I2）：将 4 个候选叶子（及新增叶子）的取值空间从自由文本改为封闭/半封闭枚举。
3. **增加关系边**（修 I3）：补 4 组阶段-策略-工具-人机交互关系边。
4. **补充缺失维度**（修 I4）：新增 validity-threat、research-direction、artifact-status 三个叶子。
5. **填充证据与候选发现**（修 M1/M2）：为 A.2 证据添加行号定位，为 A.3 填充具体线索。
6. **保留原 6 通用 leaf 作为标签层**（保留跨论文对齐价值）：将 scope/corpus/taxonomy/method/evidence/finding 作为每个原文叶子的「元维度标签」属性，标注「该 leaf 属于 A1-M0--M6 的哪个元维度」，实现单篇忠实 + 跨论文对齐的双重目标。

---

*审计报告结束。本报告未修改仓库任何文件，未 push，未 gh comment。*
