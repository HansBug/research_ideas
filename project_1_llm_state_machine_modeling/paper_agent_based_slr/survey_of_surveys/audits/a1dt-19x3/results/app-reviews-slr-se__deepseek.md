# app-reviews-slr-se · deepseek 全文审计报告

## 1. 审计身份与输入

| 项目 | 内容 |
|---|---|
| reviewer 身份 | deepseek |
| 审计日期 | 2026-06-29 |
| 审计目标 | 判断 `review.md` 中维度树是否完整、准确、可追溯，尤其检查是否过小、是否把通用 6 个 leaf 接口误当成原文 schema、是否遗漏原文关键结构 |
| 是否读取 `$ai-research-writing-skill` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` |
| 是否读取 `paper-story.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md` |
| 是否读取 `reviewer-guidelines.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` |
| 是否读取 `reviewer-self-review.md` | 是；路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` |
| 是否读取 `$research-planning` | 是；路径 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 和 `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` |
| 是否读取 `$oh-my-codex:autoresearch` | 是；路径 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` |
| 是否完整阅读 `paper_content.txt` | 是；已从头至尾阅读全部 2661 行，覆盖 Abstract、Introduction（§1）、Background（§2）、Method（§3: §3.1 搜索与纳排、§3.2 数据抽取、§3.3 分类过程与 reliability）、Results（§3: RQ1--RQ4 各子节）、Discussion & Findings（§4: 十个子节的 RQ5 回答）、Threats to Validity（§5）、Related Work（§6）、Conclusions（§7）、References 和附录级信息 |
| 是否核对 `paper.pdf` | 否；当前 paper.pdf 为 63 页，已通过 `pdfinfo` 确认页数，但未做逐页图/表视觉核对。复杂表格（Table 3 F1--F18、Table 7/10/14/16/17/18/19/20 等）的精确取值空间和页码锚点需 A2a 人工核对 |
| 是否读取文库级规则 | 是；已读 `README.md`、`GUIDE.md`、`SUMMARY.md`、`pattern-field-schema.md`、`paper_story.md` |
| 是否读取 BibTeX / metadata | 是；已读 `bibtex.bib`、`metadata.json` |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文是一篇发表于 Empirical Software Engineering（ESE, CCF-B）的系统文献综述，覆盖 2012--2020 年间 182 篇 primary studies。

**五个显式 RQ**（见 §1 Introduction 末尾和 §3.1）：

| RQ | 内容 | 原文对应节 |
|---|---|---|
| RQ1 | What **types of analysis** are used for mining app reviews? | §3 Results — "Types of app review analysis"（对应 Table 7） |
| RQ2 | What **techniques** are used for mining app reviews? | §3 Results — "Techniques for mining app reviews"（对应 Table 10；分 NLP §3.3.2、ML §3.3.3、Statistical §3.3.4） |
| RQ3 | What **software engineering activities** are supported by app review analysis? | §3 Results — "Software engineering activities"（对应 Table 14） |
| RQ4 | How are app review analysis techniques **evaluated**? | §3 Results — "Evaluation of app review analysis techniques"（对应 Table 16, Table 17, Table 18） |
| RQ5 | How **well** do app review analysis techniques **support** software engineers? | §4 Discussion — 十个子节（§4.1--§4.10） |

**贡献声明**（Abstract + §1）：首篇同时覆盖"mined information 类型 + mining technique + supported SE activity"三维度的 app review analysis 综述；报告评价质量和 replication package 状态；识别未来研究方向。

### 2.2 原文方法流程

1. **检索**：2010-01 至 2020-12；六个数字图书馆（ACM DL, IEEE Xplore, ScienceDirect, Scopus, SpringerLink, Web of Science）；两组 search query（generic + specific）；initial 1656 篇 → 去重 303 篇 → 筛选后 1353 篇 → title/abstract/keyword 筛选排除 1225 篇 → full-text 排除后 128 篇 → 手工逐卷检索 +14 篇 → snowballing +40 篇 → **最终 182 篇**。
2. **纳排标准**：纳入 = 与 SE 相关 + peer-reviewed + 使用 app reviews 支持至少一种 SE activity；排除 = 非英文、非 SE、secondary/tertiary studies、technical reports、manuals。
3. **数据抽取**：Table 3 定义 **F1--F18** 共计 18 个抽取字段（bibliographic 信息 + review analysis 类型 + mining technique + SE activity + evaluation 全套字段 + annotation dataset/annotator/quality + replication package）。
4. **分类 schema 构造**：三套分类体系 — app review analysis 类型、mining technique、SE activity。过程为 content analysis：从 sample studies 中提取概念 → 合并语义相近类别 → 作者讨论形成最终 schema。可靠性检查使用 intra-rater agreement（93% / 100% / 90%）和 inter-rater agreement（87% / 80% / 87%）。
5. **统计**：频次分布、交叉表（analysis type × technique、technique × SE activity）、年度趋势。描述统计为主，部分使用统计检验。
6. **Finding 形成**：RQ5 的回答分布在 §4 Discussion 十个子节中，每个子节基于前文统计观察 + 作者判断形成 gap / recommendation / roadmap。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

| 原文结构 | 在 paper_content.txt 中的定位 | 对 Paper2 的价值 |
|---|---|---|
| **F1--F18 抽取表** | §3.2 "Data extraction strategy"，Table 3 | 18 字段覆盖 bibliographic → analysis type → technique → SE activity → evaluation → annotation → replication；是最完整的字段级证据模板之一 |
| **app review analysis 分类 schema** | §3 Results "Types of app review analysis"，Table 7 | 封闭分类体系：Classification、Information Extraction、Content Analysis、Clustering、Sentiment Analysis、Summarization、Feature Extraction、Recommendation、Search/Retrieval、Visualization、Other；每类含子类和多对多关系 |
| **mining technique 分类 schema** | §3 Results "Techniques for mining app reviews"，§3.3.1--§3.3.4，Table 10 | NLP（pre-processing、text similarity、pattern matching、collocation finding）、ML（supervised + unsupervised 十种算法）、Statistical Analysis、Manual Analysis；每种有子类和具体技术枚举 |
| **SE activity 分类 schema** | §3 Results "Software engineering activities"，Table 14 | Requirements Engineering（elicitation/prioritization/RE other）、Testing、Maintenance & Evolution（change management/M&E other）、Design（design decisions/D other）、General（awareness/G other）、Other/Not Specified |
| **交叉统计表** | Table 19（analysis type × technique）、Table 20（technique × SE activity） | 展示字段间可统计关系，是 A2a/A2b 交叉统计的模板 |
| **评价质量字段** | §3 Results "Evaluation of app review analysis techniques"，Table 16（evaluation objective/procedure/metrics）、Table 17（annotation details: dataset size/annotation task/annotators/quality measure）、Table 18（replication package） | 展示"如何评价"和"能否复现"两个关键维度 |
| **Discussion 十个子节** | §4.1--§4.10 | 每个子节 = 一个领域 gap 或 finding，包括：evaluation limits（§4.2/4.3）、small datasets（§4.4）、replication packages（§4.5）、practical impact（§4.6）、practitioners' needs（§4.7）、industrial needs verification（§4.8）、efficiency/scalability（§4.9）、ML training problem（§4.10） |
| **Threats to Validity** | §5 | 四个维度：completeness（keyword list + publication bias）、quality/reliability（procedure）、construct validity（classification schema）、external validity |
| **Figure 4: manual analysis process** | §3.3.1 | 手动分析流程示意图，说明标注过程和编码员工作流 |

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 RQ4 的结构是：**evaluation objective → procedure → metrics → result → annotation quality → replication package**。RQ5 在此基础上将 182 篇统计观察转化为十个子节的 discussion，每个子节遵循"统计发现 → 问题诊断 → gap/recommendation"模式。例如 §4.4：统计发现 evaluation dataset 平均仅 2800 reviews → 诊断 small dataset 威胁外推 → 推荐 semi-automated labeling / active learning。整个过程不是从统计直接跳到结论，而是经过作者的诊断、比较和 roadmap 建议。

## 3. 当前 `review.md` 维度树审计

### 3.1 总体判断

当前 `review.md` 的维度树存在 **两层结构**：

1. **主树**：6 个 `leaf-*` 节点（scope / corpus / taxonomy / method / evidence / finding），挂在 5 个 `dim-*` 分支（b1--b5）下。这实际上是 **A1-M0--M6 元维度的跨论文通用接口层**，不是对本文 schema 的完整复原。
2. **候选叶子映射**：`leaf-app-reviews-slr-se-orig-*` 系列节点（extraction F1--F18 / analysis type / mining technique / SE activity / evaluation artifact），作为 A2a 精核入口的 `schema_seed`。

`review.md` 在 **"A1-DT 叶子层口径校准"** 段落中已显式声明：六个 `leaf-*` 是"跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原"。这一声明避免了"把通用接口误当成原文 schema"的强误导，但仍存在以下需要关注的问题。

### 3.2 逐项审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-app-reviews-slr-se-root]` 正确指向本文的研究目标和贡献声明，根节点说明充分。 | 通过 |
| 主干分支是否覆盖原文 schema | **部分覆盖；遗漏关键原文结构** | b1--b5 的五分支结构大致对应原文：b1=analysis type、b2=technique、b3=SE activity、b4=evaluation、b5=discussion。但以下原文结构未被主干分支覆盖：① **Threats to Validity**（§5，四个效度维度）无对应分支或叶子；② **Discussion 十个子节**被压缩到 b5 下仅两个通用 leaf，丢失了 §4.1--§4.10 的具体 finding 路径；③ **检索 / 纳排链条**作为独立方法学资产（数量链 1656→182）被归入 b2 的 `leaf-corpus`，但其本身不属于"mining technique"范畴，语义归属有偏差；④ **分类 schema 构造过程与 reliability**（intra/inter-rater agreement 数据）被归入 b3 的 `leaf-taxonomy`，但 reliability 是独立的方法学质量信息，不是 taxonomy 的一部分。 | I |
| 叶子维度是否足够具体 | **不足** | 6 个 `leaf-*` 是元维度通用接口，不是本文特化叶子。例如本文实际有 18 个抽取字段（F1--F18）、3 套分类 schema 共有 30+ 子类、10 个 discussion finding，但主树只将其映射为 6 个抽象叶子。`leaf-finding` 把十个 finding 压缩为一个通用槽位，丢失了每个 finding 的独立可追溯性。候选叶子映射虽然列举了原文结构，但未融入主树，读者需要跳转多个位置才能拼出完整图景。 | I |
| 取值空间是否可执行 | **部分可执行** | 6 个 `leaf-*` 的取值空间定义为"自由文本 + 受控标签"或"完整枚举 / 层级枚举 / 自由文本加理由"，对于 A1-DT 阶段的 schema seed 用途是可接受的。但具体的枚举值（如 analysis type 的 10+ 类别、technique 的 NLP/ML/Statistical 子类、SE activity 的 5 大类）被放在候选叶子映射中，且未在主树中显式可查。A2a 不可仅靠 6 个 leaf 就能执行字段抽取；必须回头读候选叶子映射或原文。 | M |
| 关系边是否缺失 | **缺失关键边** | 当前仅定义两条关系边：`method→evidence`（支撑/度量）和 `taxonomy→finding`（导出候选发现）。原文中至少还存在以下可审计关系：① **technique × analysis type** 的交叉统计（Table 19）—— 原文显式交叉分析了两套分类 schema，这条边是原文核心贡献（"三维度"中的二维交叉）；② **technique × SE activity** 的交叉统计（Table 20）—— 同上；③ **evaluation → finding** —— RQ4 的评价结果直接支撑 RQ5 的 discussion finding；④ **annotation quality → evaluation reliability** —— 标注质量和评价可靠性之间的支撑关系。这些边的缺失意味着 A2a 无法从当前维度树中获知原文的交叉统计设计。 | I |
| 统计用途 / 分母是否正确 | **正确但过于保守** | b5 的 `leaf-finding` 正确标注"候选发现台账，不直接作为 final finding"，且明确分母为"统计结果 + discussion"。所有统计用途在 A1-DT 阶段均设为"不进入主统计池（仅作 schema seed）"，这符合 A1-DT 的降级纪律。但"可统计方式"列中，`leaf-taxonomy` 写为"分类项频次 / 交叉表 / 主题分布"，而原文实际存在 Table 19/20 的显式交叉统计设计，当前未将这一可统计方式与具体原文表格链接。 | M |
| 候选 finding 路径是否完整 | **不完整** | 原文 §4 Discussion 有十个 finding，当前仅通过 `leaf-finding` 一个通用节点承载。例如原文 §4.6 "Impacts on SE practice" 和 §4.7 "Practitioners' requirements" 是两个独立且不同方向的 finding，但当前维度树无法区分它们。A2a 若仅依赖 `leaf-finding`，会丢失 finding 粒度和分类。候选叶子映射中 `leaf-orig-evaluation-artifact` 可部分覆盖，但 discussion finding 本身未被列为独立候选叶子。 | I |
| A.1--A.4 证据链是否足够 | **结构完整，证据强度待升级** | A.1 来源标识完善；A.2 证据账本有 6 条证据（EV-001 至 EV-006），覆盖根、分类、统计、discussion 和关系边；A.3 结论-证据映射有 12 条结论；A.4 复验清单有 2 项。结构上符合 `pattern-field-schema.md` 的合同。但：① EV-002/003/005 的证据强度均为 `not_verified`（"待 A2a 精确页码复核"），这意味着 A.3 的 12 条结论支撑证据实际处于待核验状态；② A.4 中 `needs_manual_check` 的视觉核对项覆盖了 3 条证据，但具体应核对的表格编号未在 A.4 中逐表列出（如 Table 3/7/10/14/16/17/18/19/20）。 | M |
| 是否存在可能误导 A2a 的强主张 | **存在风险但已有缓解** | 校准声明避免了"通用接口 = 原文 schema"的直接误导。但以下构造仍有误导风险：① b2 "mining technique" 下挂 `leaf-corpus`（语料与纳排链条）—— 检索/纳排不属于 mining technique，这会让 A2a 误以为检索策略是 technique 的子维度；② b5 "discussion gap" 下同时挂了 `leaf-evidence` 和 `leaf-finding`，而 evidence 实际上主要来自 §3 Results 的 evaluation section，并非 discussion 的子节点，这种归属偏差可能让 A2a 在阅读原文时找错位置。③ 候选叶子映射中的 `leaf-orig-extraction-f1-f18` 未标明具体 18 字段名（F1--F18 的字段语义），A2a 需要回头查 Table 3 原文。 | M |

## 4. 建议维度树骨架

以下给出更忠实于原文结构的维度树。该树将原文的 5 个 RQ 映射为 5 条主干分支，每条分支下展开原文中实际存在的子维度和叶子。

```text
[dim-root] Analysing app reviews for SE: SLR of 182 primary studies (2012--2020)
│
├── [dim-rq1] RQ1: Types of app review analysis (→ Table 7, Table 19)
│   ├── [leaf-rq1-analysis-type] 分析类型分类
│   │   ├── Classification (bug report / feature request / user experience / rating)
│   │   ├── Information Extraction
│   │   ├── Content Analysis
│   │   ├── Clustering
│   │   ├── Sentiment Analysis
│   │   ├── Summarization
│   │   ├── Recommendation
│   │   ├── Feature Extraction
│   │   ├── Searching & Information Retrieval
│   │   ├── Visualization
│   │   └── Other / Not Specified
│   └── [leaf-rq1-analysis-type-multi] 是否允许多对多分类 → yes (一篇 primary study 可归属多个 analysis type)
│
├── [dim-rq2] RQ2: Techniques for mining app reviews (→ Table 10, Table 19, Table 20)
│   ├── [leaf-rq2-technique-category] 技术大类
│   │   ├── Manual Analysis (§3.3.1)
│   │   ├── Natural Language Processing (§3.3.2)
│   │   │   ├── Text Normalization (lowercase, sentence splitting, tokenization, spelling correction, stemming/lemmatization)
│   │   │   ├── Text Cleaning (punctuation removal, stop word removal, non-English filtering)
│   │   │   ├── Text Augmentation (PoS tagging, dependency parsing)
│   │   │   ├── Text Similarity (Cosine, Dice, Jaccard) [21 studies]
│   │   │   ├── Pattern Matching (regex, PoS sequences, dependency patterns, keyword) [22 studies]
│   │   │   └── Collocation Finding (bigrams, PMI, hypothesis testing)
│   │   ├── Machine Learning (§3.3.3) [108 studies / 59%]
│   │   │   ├── Supervised: Naïve Bayes, SVM, Decision Tree, Logistic Regression, Random Forest, Neural Network, Linear Regression, KNN
│   │   │   └── Unsupervised: LDA, K-Means
│   │   └── Statistical Analysis (§3.3.4)
│   └── [leaf-rq2-technique-features] 特征工程属性 (textual: text length / tense / tf-idf / n-gram / dependency; non-textual: sentiment / rating / app category)
│
├── [dim-rq3] RQ3: Supported SE activities (→ Table 14, Table 20)
│   ├── [leaf-rq3-se-activity] SE 活动分类
│   │   ├── Requirements Engineering (Elicitation / Prioritization / RE Other)
│   │   ├── Testing
│   │   ├── Maintenance & Evolution (Change Management / M&E Other)
│   │   ├── Design (Design Decisions / D Other)
│   │   ├── General (Awareness / G Other)
│   │   └── Other / Not Specified
│   └── [leaf-rq3-activity-multi] 是否允许多对多 → yes
│
├── [dim-rq4] RQ4: Evaluation of techniques (→ Table 16, Table 17, Table 18)
│   ├── [leaf-rq4-eval-objective] 评价目标 (effectiveness / perceived quality / comparison / other / not reported)
│   ├── [leaf-rq4-eval-procedure] 评价方法 (quantitative / qualitative / mixed / case study / user study)
│   ├── [leaf-rq4-eval-metrics] 评价指标 (precision / recall / F1 / accuracy / AUC / manual assessment / other)
│   ├── [leaf-rq4-eval-result] 评价结果 (量化或质性；含 sample size)
│   ├── [leaf-rq4-annotation-dataset] 标注数据规模 (average ~2800 reviews; range [min, max])
│   ├── [leaf-rq4-annotation-task] 标注任务类型
│   ├── [leaf-rq4-annotator] 标注者 (authors / external / mixed / not reported)
│   ├── [leaf-rq4-annotation-quality] 标注质量度量 (agreement / other / not reported)
│   └── [leaf-rq4-replication] 复现包 (tool available / dataset available / both / none / not reported)
│
├── [dim-rq5] RQ5: Discussion findings & research gaps (→ §4.1--§4.10)
│   ├── [leaf-rq5-diversity] §4.1 Diversity & trends in app review analysis research
│   ├── [leaf-rq5-eval-better] §4.2 Need for better evaluations (precision/recall baselines)
│   ├── [leaf-rq5-eval-context] §4.3 Context-specific evaluation (app domain / review language)
│   ├── [leaf-rq5-small-datasets] §4.4 Small evaluation datasets (avg 2800 reviews; threat to external validity)
│   ├── [leaf-rq5-replication-packages] §4.5 Replication packages (most papers do NOT provide)
│   ├── [leaf-rq5-practical-impact] §4.6 Impact on SE practice (unclear if techniques are "good enough")
│   ├── [leaf-rq5-practitioners-needs] §4.7 Practitioners' requirements (current research is data-driven, not goal-driven)
│   ├── [leaf-rq5-industrial-needs] §4.8 Verifying industrial needs (average app = 22 reviews/day; who benefits?)
│   ├── [leaf-rq5-efficiency] §4.9 Efficiency & scalability (no study measured runtime/scalability)
│   └── [leaf-rq5-ml-training] §4.10 Training ML techniques (annotation cost / domain drift / active learning)
│
├── [dim-method] Method: Search, selection, extraction & classification (→ §3.1--§3.3)
│   ├── [leaf-method-search] 检索链条 (1656 → 1353 → 128 → 182; generic + specific query; 6 databases)
│   ├── [leaf-method-inclusion] 纳入标准 (SE-relevant / peer-reviewed / uses app reviews for SE activity)
│   ├── [leaf-method-exclusion] 排除标准 (non-English / non-SE / secondary-tertiary / technical reports / manuals)
│   ├── [leaf-method-extraction-form] F1--F18 抽取字段 (Table 3 完整清单)
│   ├── [leaf-method-classification-process] 分类过程 (content analysis: concept extraction → merge → author discussion)
│   └── [leaf-method-classification-reliability] 分类可靠性 (intra-rater: 93%/100%/90%; inter-rater: 87%/80%/87%)
│
├── [dim-validity] Threats to validity (→ §5)
│   ├── [leaf-validity-completeness] 完整性威胁 (keyword list construction: iterative approach; publication bias: snowballing + issue-by-issue search)
│   ├── [leaf-validity-quality-reliability] 质量与可靠性 (systematic procedure defined)
│   ├── [leaf-validity-construct] 构造效度 (classification schemas from sample studies; potential misclassification)
│   └── [leaf-validity-external] 外部效度 (findings limited to 2010--2020; specific databases)
│
└── [dim-relations] 跨维度关系（交叉统计）
    ├── [edge-analysis-type-x-technique] RQ1 × RQ2: analysis type 与 technique 的交叉分布 (→ Table 19)
    └── [edge-technique-x-se-activity] RQ2 × RQ3: technique 与 SE activity 的交叉分布 (→ Table 20)
```

### 4.1 建议树与当前树的差异总结

| 差异维度 | 当前 `review.md` 树 | 建议树 |
|---|---|---|
| 主干分支数 | 5 条（b1--b5） | 8 条（rq1--rq5 + method + validity + relations） |
| 叶子层级 | 6 个通用 leaf | 30+ 个原文特化 leaf，下钻到原文子类 |
| RQ 映射 | 未显式引用原文 RQ 编号 | 每条分支显式标注原文 RQ 编号和对应原文节 |
| 分类 schema 展开 | 仅 `leaf-taxonomy` 一个通用槽 | 三套 schema 分别展开到子类，并标注原文 Table 引用 |
| Discussion finding | `leaf-finding` 一个通用槽 | 十个独立 leaf，每个对应原文 §4 的一个子节 |
| Validity threats | 无 | 独立分支，四个 leaf 对应原文 §5 的四个效度维度 |
| Method 与 corpus 分离 | `leaf-corpus` 挂在 b2 "mining technique" 下 | method 独立分支，检索/纳排/抽取/分类/可靠性独立成 leaf，不再与 technique 混淆 |
| 交叉统计关系 | 缺失 | `dim-relations` 捕获 Table 19 和 Table 20 的交叉边 |
| 取值空间 | 自由文本为主 | 基于原文表格枚举（需 A2a 核对封闭性） |

### 4.2 为什么当前树需要升级

当前 6-leaf 通用接口在 A1 奠基阶段提供了跨论文对比的统一框架，有其工程合理性。但当单篇论文的原文 schema 非常丰富时（如本文有 18 个抽取字段、3 套分类体系、10 个 finding、4 个效度威胁、2 张交叉表），仅用 6 个通用 leaf 无法为 A2a 提供足够精确的 schema 锚点。A2a 执行字段抽取时需要知道"这篇论文的 taxonomy 具体有哪些类别"，而不是只知道"有 taxonomy 这个维度"。当前"候选叶子映射"虽然部分弥补了这一缺口，但候选叶子不在主树中，且被统一标注为 `not_verified` / `schema_seed`，A2a 无法从主树直接导航到原文特化结构。

## 5. 必须补充 / 修正清单

| 编号 | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|---|
| FIX-01 | b5 "discussion gap" 下 `leaf-evidence` 归属不当 | 维度树结构段 | 将 `leaf-evidence` 从 b5 移到 b4（或新建 b4 子节点），因为 evaluation 信息（Table 16/17/18）是 §3 Results 的内容，不属于 §4 Discussion。b5 应只保留 finding 相关节点。 | paper_content.txt §3 "Evaluation of app review analysis techniques" vs §4 "Discussion" | I |
| FIX-02 | b2 "mining technique" 下 `leaf-corpus` 归属不当 | 维度树结构段 | 将检索/纳排信息从 b2 分离，建立独立 `dim-method` 分支或归入 b1（与 scope 并列）。检索策略和纳排标准是 method 级信息，不是 "mining technique" 在综述元模型中的子类。 | paper_content.txt §3.1 "Search strategy & study selection" 发生在 technique 分类之前 | I |
| FIX-03 | 缺失 Threats to Validity 分支 | 维度树结构段 | 新增 `dim-validity` 分支或至少一个 `leaf-validity`，因为原文 §5 显式讨论了 completeness / quality-reliability / construct / external 四个 validity threat，且这是 pattern-field-schema 的 `validity_threat_pattern` 必填维度。 | paper_content.txt §5 "Threats to validity"; pattern-field-schema.md §4 六类 pattern 中包含 `validity_threat_pattern` | I |
| FIX-04 | Discussion finding 被压缩为单个 leaf | 维度树结构段和叶子维度表 | 在 b5 下将 `leaf-finding` 拆为至少对应原文 §4.1--§4.10 的多个子 leaf，或在 `leaf-finding` 取值空间中枚举十个子节的 finding 标签。当前 "统计观察与候选发现" 的取值空间过于抽象，A2a 无法区分 "practitioners' needs"（§4.7）和 "industrial needs"（§4.8）这两个方向不同的 finding。 | paper_content.txt §4.1--§4.10 | I |
| FIX-05 | 缺失原文交叉统计关系边 | 关系边表 | 新增 `edge-analysis-type-x-technique`（对应 Table 19）和 `edge-technique-x-se-activity`（对应 Table 20），这是原文的核心贡献声明（"三维度综合分析"）的方法学支柱。 | paper_content.txt Table 19, Table 20; §1 Contribution | I |
| FIX-06 | 候选叶子 F1--F18 缺少字段级枚举 | 原文模式候选叶子映射表 | 在 `leaf-app-reviews-slr-se-orig-extraction-f1-f18` 的取值空间列中或紧随其后的说明中枚举 F1--F18 的字段名和简短定义，使 A2a 无需回头查 Table 3 原文即可了解抽取字段的覆盖范围。当前只写了 "F1--F18" 作为标识，未展开字段语义。 | paper_content.txt Table 3; review.md §2.3 已有人类可读描述，但未以机器可读形式融入候选叶子映射 | M |
| FIX-07 | A.4 视觉核对清单缺少待核表格编号 | A.4 本地复验清单 | 在 `cmd-app-reviews-slr-se-visual-check` 的"复验对象"列中增加具体表格编号清单：Table 3（F1--F18）、Table 7（analysis types）、Table 10（techniques）、Table 14（SE activities）、Table 16（evaluation）、Table 17（annotation）、Table 18（replication）、Table 19（analysis type × technique）、Table 20（technique × SE activity）。当前仅笼统写"相关表格、图、统计页"。 | paper_content.txt 中明确列出上述所有表格 | M |
| FIX-08 | 分类 schema 构造过程与 reliability 信息未进入叶子 | 维度树结构段 | 将原文 §3.3 的 classification construction process（content analysis: concept extraction → merge → author discussion）和 reliability check（intra-rater 93%/100%/90%, inter-rater 87%/80%/87%）作为 `leaf-taxonomy` 的附加取值空间或新建 `leaf-classification-reliability`。这对 Paper2 的方法学设计至关重要：它证明了分类 schema 的构造是可审计的，不是任意命名的。 | paper_content.txt §3.3 "Classification process"; review.md §2.4 已在自然语言中记录但未进入维度树 | M |
| FIX-09 | 主树 6-leaf 与候选叶子映射的衔接说明不够突出 | 维度树复原节标题附近 | 在"维度树结构"代码块之前增加一个显式的"读者导航"段落，明确说明：(a) 6-leaf 是跨论文通用接口；(b) 本文原文特化结构（18 字段 + 3 schema + 10 finding + 4 threat + 2 cross-table）的全部位置在"原文模式候选叶子映射"表中；(c) A2a 使用时应先读 6-leaf 接口定位大类，再跳转到候选叶子映射获取精确字段。当前校准声明在"维度树结构"之前但不够突出。 | 当前 `review.md` 已有校准声明，但位于 6-leaf 表之后和候选映射表之前，读者可能漏读 | M |

## 6. C/I/M 结论

### 6.1 C 级（阻塞）

**无。** 当前 `review.md` 在 A1-DT 阶段的 schema seed 定位下，不存在直接破坏 Paper2 学术目标或证据链的问题。所有统计结论均标注为 `schema_seed` / `weak` / `not_verified`，不会误入 SUMMARY 定量统计。校准声明避免了"通用接口 = 原文 schema"的强误导。

### 6.2 I 级（影响维度树可用性与证据可审计性）

| 编号 | 问题 | 对 Paper2 的影响 |
|---|---|---|
| I-01 | b2 "mining technique" 下挂 `leaf-corpus`（归属偏差） | A2a 检索 Paper2 方法论时，若按当前树将"检索/纳排"定位为 technique 子维度，会导致 schema 继承偏差：检索策略是综述的 method 级信息，不是 technique 分类的子类。这影响 A2a 的检索字段设计。 |
| I-02 | b5 缺失 Discussion 十个 finding 的特化叶子 | A2a/A2b 若仅依赖 `leaf-finding` 一个通用槽位，无法进行 finding 粒度的跨论文统计（例如"多少篇 SLR 讨论了 replicability gap"）。本文是 A1 中 finding 组织最清晰的样本之一，丢失这一粒度是信息损失。 |
| I-03 | 缺失 Validity threats 分支 | `pattern-field-schema.md` 要求的 `validity_threat_pattern` 是六类必须 pattern 之一。对本文，§5 的四个 validity threat 是显式存在的原文结构，缺失会导致 A2a 的效度 threat 字段缺乏此样本的种子。 |
| I-04 | 缺失 Table 19/20 交叉统计关系边 | 原文的核心方法学贡献之一是"交叉分析三套分类 schema"，这是 Paper2 后续做字段间交叉统计的直接先例。缺失此边意味着 A2a 无法从维度树获知"不同字段间可以且应该做交叉统计"。 |
| I-05 | b5 下 `leaf-evidence` 和 `leaf-finding` 并列，且 evidence 归属 discussion | evaluation 是 §3 Results 的内容（对应 RQ4），不是 discussion（对应 RQ5）。这种归属错位会让 A2a 在原文中定位 evidence 信息时找到错误章节。 |

### 6.3 M 级（清晰度与维护性建议）

| 编号 | 问题 |
|---|---|
| M-01 | 候选叶子 F1--F18 缺少字段级枚举（见 FIX-06） |
| M-02 | A.4 视觉核对清单缺少待核表格编号（见 FIX-07） |
| M-03 | 分类 schema 构造过程与 reliability 未进入叶子（见 FIX-08） |
| M-04 | 6-leaf 接口与候选叶子映射的衔接导航不够突出（见 FIX-09） |

### 6.4 最终建议

**NEEDS FIX（I 级）** — 当前 `review.md` 的维度树存在 5 个 I 级问题（归属偏差 2 项 + finding 粒度丢失 + validity 缺失 + 交叉边缺失），建议在进入 A2a 前完成 FIX-01 至 FIX-05 的修复。这些修复不影响已完成的 19 篇 cross-paper 通用接口层的一致性（因为 6-leaf 接口仍保留为跨论文对比层），而是在主树中补充本文特化的子分支、叶子和关系边。

具体修复路径建议：
1. **先修复归属偏差**（FIX-01、FIX-02）：调整 b2 和 b5 的子节点归属，使 method（检索/纳排/分类）和 evidence（评价字段）各自归入正确的维度分支。
2. **再补充缺失结构**（FIX-03、FIX-04、FIX-05）：新增 validity 分支，展开 discussion finding，添加交叉统计关系边。
3. **最后完善细节**（FIX-06--FIX-09）：枚举候选叶子字段、细化 A.4 清单、补充 reliability、强化导航说明。

当前 A1-DT 阶段的统一口径（所有统计标注为 `schema_seed` / `not_verified`）保持不变；这些修复仅改变维度树的**结构完备性**，不改变证据强度标注。

### 6.5 总体评价

Dąbrowski et al. 2022 是 A1 文库中字段体系最为完整的现代 SLR 样本之一。其 5 个 RQ、18 个抽取字段、3 套分类 schema、双交叉表设计和 10 个 discussion finding 构成了一个可复用的"RQ→抽取→分类→交叉统计→分层 finding"模板。当前 `review.md` 的自然语言详读（§2.1--§2.8）对此有较好的捕捉，但维度树的正式结构未充分反映这一丰富性——6 个通用 leaf 是对跨论文对比层的忠诚，但对本文特化层的捕捉不足。上述 FIX-01 至 FIX-05 的目标是在保留通用接口层的前提下，让维度树更忠实地反映原文实际结构，从而让 A2a 能从一个位置获取足够精确的 schema 锚点。
