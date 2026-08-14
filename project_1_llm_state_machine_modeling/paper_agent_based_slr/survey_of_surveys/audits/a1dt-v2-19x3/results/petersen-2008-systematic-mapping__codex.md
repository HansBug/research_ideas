### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2008-systematic-mapping` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已按全文页标阅读 1--10 页文本，并用分段读取补齐中间截断区间。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；BibTeX 确认题名、作者、DOI、年份；metadata 确认当前本地归类为 SMS 方法论文、schema seed、非普通统计池。 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 与 `pdftotext -layout` 核对 PDF 为 10 页，并核对 Figure 1--3、Table 1--5 的版面文本。未做截图式人工视觉核验。 |
| 原文类型 | other：系统映射研究（systematic mapping study, SMS）方法论文；内含对 10 篇系统综述（systematic review, SR）的嵌入式 tertiary-style characterization。 |
| 被编码样本单位 | 双样本单位：1. 示例 SMS 中的 primary articles / relevant articles；2. §3 中纳入并编码的 10 篇 SE systematic reviews。 |
| 样本数量 / 分母 | §3 比较样本：检索得 21 篇，筛入 8 篇，另从 Kitchenham 2007 加 2 篇，共 10 篇 SR。示例 mapping：Figure 3 给出 facet-specific totals，如 research facet 128、contribution facet 118；不能合并成单一分母。 |
| 原生树类型 | 维度森林：SMS 流程-分类方案树 + 示例 map facet 树 + 10 篇 SR 比较特征树。 |
| 主统计池资格 | 局部可统计；10 篇 SR 的 Table 5 和 Figure 3 的方法学频数可作“方法学统计 / schema seed”。不进入普通 SE 领域结论统计池，也不能支撑 Paper2 final domain finding。 |
| 总体判定 | needs repair；论文材料可用，但现有 `review.md` 仍需把原生维度森林提升为主事实源，通用六叶只能保留为投影层。 |

### 1. 原文证据阅读说明

已读取本地文件：

- `bibtex.bib`：题名、DOI、作者、年份、publisher。
- `metadata.json`：当前仓库口径、统计池排除理由、schema seed 状态。
- `paper_content.txt`：全文 10 页文本。
- `review.md`：现有审查、维度树复原、A.1--A.4。
- `paper.pdf`：通过 `pdfinfo` 和 `pdftotext -layout` 做版面文本核对；未做图片截图式人工核验。`file` 报 6 页但 `pdfinfo` 与全文页标均为 10 页，后者更可信。

关键原文证据锚点：

1. 摘要：SMS 用于构建分类方案并按类别频数分析研究覆盖。
2. 摘要 METHOD：作者定义 SMS process，且系统分析 existing systematic reviews。
3. §2 / Figure 1：流程为 RQ 定义、检索、筛选、keywording、数据抽取与 mapping。
4. §2.1 / Table 1：SMS RQ 面向研究区域、文章数量、文章类型、时间趋势与发表论坛。
5. §2.2：search string 可按 population / intervention / comparison / outcome 构造，但示例 mapping 为保 breadth 未限制 outcome / experimental design。
6. §2.3 / Table 2：纳排标准由 RQ 驱动，且两个示例 map 的纳排不同。
7. §2.4 / Figure 2：keywording 由 abstract 触发，必要时读 introduction / conclusion，关键词聚类形成分类方案。
8. §2.4 / Table 3：research type facet 采用 Wieringa 分类：validation、evaluation、solution proposal、philosophical、opinion、experience。
9. §2.5：Excel extraction table 包含每个分类项，且每篇论文归类要写 short rationale。
10. §2.5 / Figure 3：bubble plot 展示 topic / contribution / research type 的交叉频数。
11. §3 / Table 4--5：10 篇 SR 被编码为 research goals、inclusion requirements、article counts、means of analysis。
12. §4：guideline 包括方法互补、自适应阅读深度、按 evidence / novelty 分类、可视化数据。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文有两个层次的对象。第一层是 SMS 方法流程中的 primary articles / relevant articles，主要来自作者已应用的 software product line variability map 和 Bailey 的 OO design map 对照；这些对象在本文中主要作为方法示例出现。第二层是 §3 系统分析的 10 篇 SE systematic reviews；这部分有检索式、数据库、筛选逻辑、Table 4 样本清单和 Table 5 编码表，是本文最明确的样本编码 corpus。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

有，但分层不同。§2 是 SMS 方法流程与示例说明，未完整复现 Mujtaba 2008 的全套样本清单；§3 对 existing systematic reviews 则明确给出检索式、数据库、21 个结果、排除标准、8+2 纳入逻辑、10 个样本 ID 和 Table 5 编码维度。

3. 原文字段来自哪里？

字段来源包括：Figure 1 的 process schema、Table 1 的 RQ examples、Table 2 的 inclusion/exclusion criteria、Figure 2 的 keywording / classification process、Table 3 的 Wieringa research type taxonomy、§2.5 的 Excel extraction table + rationale 描述、Figure 3 的 map visualization、§3.1 的 review characterization fields 和 Table 5。

4. RQ 与样本单位是什么关系？

RQ 不是维度树本身的唯一树根，而是字段用途和纳排 / 分类设计的驱动因素。SMS 的 RQ 决定 search、screening、topic facet、frequency / trend / forum 统计；§3 的比较问题则驱动对 SR 样本进行 research goal、inclusion requirement、article count、analysis method 编码。

5. 若无系统样本库，如何降级？

本文不是纯 guideline 无样本库。§3 的 10 篇 SR corpus 可局部统计；§2 的示例 mapping 因完整样本库不在本文中复现，应降级为 methodological schema seed，不可把 Figure 3 的领域分布迁移为 Paper2 领域结论。

### 3. 原生样本编码维度树 / 维度森林

```text
petersen-2008-native-dimension-forest
├── Tree A: SMS 方法流程与示例 map 编码树
│   ├── research_scope
│   │   ├── overview_goal
│   │   ├── quantity_and_type_goal
│   │   ├── publication_trend_goal
│   │   └── publication_forum_goal
│   ├── search_and_screening
│   │   ├── search_mode: database_search / manual_forum_browse / journal_browse
│   │   ├── search_string_components: population / intervention / comparison / outcome
│   │   ├── search_string_text
│   │   ├── inclusion_criteria
│   │   └── exclusion_criteria
│   ├── keywording_and_classification
│   │   ├── keyword_source: abstract; intro/conclusion fallback
│   │   ├── topic_facet: requirements / architecture / implementation / verification_and_validation / variability_management / orthogonal_variability
│   │   ├── contribution_facet: metric / tool / model / method / process
│   │   ├── research_type_facet: validation / evaluation / solution_proposal / philosophical / opinion / experience
│   │   ├── category_update: add / merge / split
│   │   └── classification_rationale
│   └── map_analysis
│       ├── category_frequency
│       ├── cross_facet_frequency
│       ├── frequency_table
│       ├── bubble_plot
│       └── coverage_gap_candidate
└── Tree B: 10 篇 SE systematic reviews 比较特征树
    ├── review_search_selection
    │   ├── search_string
    │   ├── searched_databases
    │   ├── initial_hits: 21
    │   ├── exclusion_basis
    │   ├── included_from_search: 8
    │   └── included_from_kitchenham_2007: 2
    ├── review_identity
    │   ├── reference_id: 1..10
    │   └── bibliographic_reference
    ├── research_goals
    │   ├── identify_best_and_typical_practices
    │   ├── classification_and_taxonomy
    │   ├── emphasis_on_topic_categories
    │   └── identify_publication_fora
    ├── inclusion_requirements
    │   ├── research_within_focus_area
    │   └── empirical_methods_used
    ├── article_counts
    │   ├── potentially_relevant_studies
    │   └── relevant_studies_included
    └── means_of_analysis
        ├── meta_study
        ├── comparative_analysis
        ├── thematic_analysis
        └── narrative_summary
```

缺失部分与 A2a 精核任务：Figure 3 的气泡坐标和百分比应做 PDF 视觉核验；Mujtaba 2008 的完整 Excel extraction table 不在本文中，不能假装本文给出了完整 primary-study database；Table 5 的 `x` 布局应以 PDF 版面核对后再做逐格机器统计。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A.scope.goal | SMS 研究目标 | research_scope | §2.1 / Table 1 | mapping 要回答的概览型目标 | overview、quantity/type、trend、forum | 完整枚举 seed | 未出现则不能推断该 map 追踪该目标 | 组织 RQ 类型频次 | 识别 mapping 型 RQ | §2.1 | 只迁移 RQ 类型，不迁移领域结论 |
| A.search.mode | 检索方式 | search_and_screening | §2.2 | primary studies 的识别渠道 | scientific databases、manual proceedings、journal browse | 完整枚举 seed | 未报告为 not_reported | 比较检索覆盖 | 检索策略启发 | §2.2 | 不能代表现代数据库最佳实践 |
| A.search.components | 检索式结构 | search_and_screening | §2.2 | 用 PICO 类结构组织关键词 | population / intervention / comparison / outcome | 外部分类法引用 | 不使用 outcome 可为主动策略 | 分析 breadth/depth trade-off | 宽检索 vs 窄检索边界 | §2.2 | 仅方法学启发 |
| A.screen.criteria | 纳排标准 | search_and_screening | Table 2 | 判断 relevant papers 的规则 | inclusion / exclusion 自由文本 | 自由文本加理由 | 未给出则不可统计 | 支撑样本分母可信度 | 排除泛提关键词论文 | Table 2 | 示例标准不能跨主题照搬 |
| A.keyword.source | keywording 信息源 | keywording_and_classification | §2.4 / Figure 2 | 提取关键词与概念的阅读来源 | abstract；intro/conclusion fallback | 层级枚举 | abstract 不足时需升级阅读深度 | 记录证据等级 | 自适应阅读深度 | §2.4 | 可迁移为 A2a 证据等级 |
| A.topic.facet | topic facet | keywording_and_classification | §2.4 / Figure 3 | 领域主题分类轴 | requirements、architecture、implementation、verification/validation、variability management、orthogonal variability | 层级枚举 / 示例枚举 | 空白 cell 待核验，可能为 0 或未显示 | topic 覆盖频次 | 主题空白候选 | §2.4 / Figure 3 | SPL variability 类别不可迁移到 LLM4STM |
| A.contribution.facet | contribution facet | keywording_and_classification | §2.4 / Figure 3 | 论文贡献形态 | metric、tool、model、method、process | 完整枚举 seed | 未归类需 rationale | contribution 分布 | 方法/工具缺口 | Figure 3 | 可迁移字段类型，需现代扩展 |
| A.research_type | research type facet | keywording_and_classification | Table 3 | Wieringa 研究类型 | validation、evaluation、solution proposal、philosophical、opinion、experience | 完整枚举 / 外部分类法引用 | 未出现不等于无研究，只是该样本未归类 | research type 频次 | evidence/novelty 分类 | Table 3 | LLM/agent 论文需扩展 |
| A.rationale | 分类短理由 | keywording_and_classification | §2.5 | 每篇论文为何属于某类别的说明 | 自由文本 rationale | 自由文本加理由 | 缺失则分类证据弱 | 审计归类可信度 | 字段级证据链 | §2.5 | 可强迁移为 Paper2 source anchor |
| A.schema_update | 分类方案演化 | keywording_and_classification | §2.5 / Figure 2 | 抽取中新增、合并、拆分类别 | add / merge / split | 完整枚举 seed | 未记录则 schema revision 不可审计 | schema versioning | 维度演化机制 | §2.5 | 可迁移为 schema revision log |
| A.frequency | 类别频数 | map_analysis | §2.5 / Figure 3 | 每类或交叉类文章数量 | 数值、百分比、bubble size | 数值或区间 | 空格需 PDF 核验后判零/缺失 | coverage / density | coverage gap | §2.5 / Figure 3 | 不支持 effect-size meta-analysis |
| B.search_hits | SR 检索与纳入数 | review_search_selection | §3 | existing SR corpus 的形成过程 | 21 hits；8 included；+2 added | 数值 | 未纳入原因需按排除标准解释 | corpus 分母 | 方法学样本可信度 | §3 | 只支撑 2008 前 SE SR 方法比较 |
| B.review_id | SR 样本 ID | review_identity | Table 4 | 10 篇纳入 SR 的编号 | 1--10 | 完整枚举 | 无 ID 不可进入 Table 5 | 行级索引 | 可追踪样本 | Table 4 | 不外推为 primary studies |
| B.research_goals | SR 研究目标 | research_goals | §3.1 / Table 5 | 对每篇 SR 的目标编码 | best practices、classification/taxonomy、topic categories、publication fora | 完整枚举 + 布尔 | 空白表示作者未标记该目标 | 目标类型频次 | SR vs SMS 目标边界 | §3.1 / Table 5 | 只比较 SR 方法目标 |
| B.inclusion_req | SR 纳入要求 | inclusion_requirements | §3.1 / Table 5 | 每篇 SR 的纳入门槛类型 | within focus area、empirical methods used | 完整枚举 + 布尔 | 空白表示未标记 | inclusion policy 频次 | empirical-bias 风险 | §3.1 / Table 5 | 不等于质量评价 |
| B.article_counts | SR 文章数量字段 | article_counts | §3.1 / Table 5 | 每篇 SR 的检索候选数与最终纳入数 | potentially relevant；included；`n.a.` | 数值 / n.a. | `n.a.` 表示原文不可得或未报告 | attrition 观察 | breadth/depth 对比 | Table 5 | 不可混为本文 primary-study 总数 |
| B.analysis_means | SR 分析方法 | means_of_analysis | §3.1 / Table 5 | 每篇 SR 的 synthesis / analysis 类型 | meta、comparative、thematic、narrative | 完整枚举 + 布尔 | 空白表示未标记 | analysis method 频次 | SMS 与 SR 方法互补 | §3.1 / Table 5 | 2008 年分类，需更新 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | research questions | drives | search string / screening criteria | RQ-specific search and inclusion design | 无 RQ 则 search rationale 弱 | §2.1--§2.3 | 解释为什么字段不是孤立模板 |
| R2 | abstracts / intro / conclusion | derives | keywords / concepts | contribution keyword、context keyword | abstract 不足则升级阅读深度 | §2.4 | 建立 keywording 证据链 |
| R3 | keywords | clusters_into | classification categories | topic、contribution、research type | 聚类未记录则 schema seed | §2.4 / Figure 2 | 维度生成机制 |
| R4 | classification scheme | classifies | articles | category assignment + rationale | 无 rationale 则弱证据 | §2.5 | 字段值审计 |
| R5 | article-category assignments | counts | category frequencies | 数值 / 百分比 | 空 cell 待 PDF 核验 | §2.5 / Figure 3 | 统计观察 |
| R6 | topic facet | cross_tabulates_with | contribution facet | bubble plot cell counts | 空格可能为 0，需视觉核验 | Figure 3 | 交叉覆盖 |
| R7 | topic facet | cross_tabulates_with | research type facet | bubble plot cell counts | 同上 | Figure 3 | 发现低覆盖组合 |
| R8 | review ID | has_property | research goals | 4 个目标布尔字段 | blank = not marked | Table 5 | SR 方法目标统计 |
| R9 | review ID | has_property | inclusion requirements | 2 个布尔字段 | blank = not marked | Table 5 | 纳入门槛统计 |
| R10 | review ID | has_numeric_field | article counts | potentially relevant / included / n.a. | `n.a.` 不得补数 | Table 5 | 分母与筛选强度 |
| R11 | review ID | has_property | means of analysis | 4 个 analysis 类型 | blank = not marked | Table 5 | synthesis 方法统计 |
| R12 | low / empty frequency cell | supports_candidate | research gap | coverage shortage | 只可候选，不是 final finding | §2.5 / §3.2 / §4 | finding 边界 |

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段 / 统计表支持的统计观察：

- §3 搜索 `"systematic review" AND "software engineering"` 得到 21 篇，筛入 8 篇，并额外纳入 2 篇，共 10 篇 SR。
- Table 5 支持对 10 篇 SR 的研究目标、纳入要求、文章数量和分析方法作描述性统计。
- 作者总结：所有 SR 都有 narrative summary；两篇使用 thematic analysis，两篇使用 meta analysis，一篇使用 comparative analysis。
- 作者总结：只有两篇 SR 主要关注 classification / taxonomy、类别频数和 publication fora，并且仍有更深的 narrative summary。
- Figure 3 支持 SMS 示例中 topic / contribution / research type 的交叉频数观察；但气泡位置和百分比需 A2a 视觉核验后才能逐格入库。

原文 discussion / recommendation / guideline 的候选 finding：

- SMS 与 SR 目标不同，应互补使用；SMS 可先结构化领域，再选择局部主题做 SR。
- SMS 不以建立 state of evidence 为主，因此通常不做与 SR 同等深度的质量评价。
- 摘要可能误导分类，应允许 adaptive reading depth。
- 高层 research type 分类适合 mapping；过细研究方法分类需要更深阅读。
- bubble plot 比单纯 frequency table 更适合展示多 facet 覆盖。

对 Paper2 可迁移的方法学启发：

- 先定样本单位，再定字段树；RQ 是字段用途和筛选策略的驱动，不应直接替代维度树。
- 字段值必须带 rationale / source anchor。
- 分类方案应记录 add / merge / split 的 schema evolution。
- 统计观察应先停留在 coverage / density / gap candidate，再由研究者裁决是否成为 final finding。
- 可以把 topic facet、contribution facet、research type facet 作为 LLM4STM 综述 schema 的抽象模式，但具体枚举必须重建。

绝不能迁移的领域结论：

- 不能把 software product line variability 的 topic distribution 当成 LLM 状态机建模领域事实。
- 不能把 2008 年 SE SR 的分析方法分布当成现代 SLR/SMS 当前状态。
- 不能把 Wieringa 研究类型完整照搬为现代 LLM/agent 论文分类终版。
- 不能把 Figure 3 的 `0%` 或空白 cell 写成任何目标领域“没有研究”的强结论。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | 当前“维度树复原”仍先给出六个通用 leaf，原文 schema 主树被放在后面且标为候选。 | 重写该节：以本文原生维度森林为主事实源，先写 Tree A / Tree B；六个通用接口移动到“跨论文投影”小节。 |
| C | 样本单位写成 `roadmap action / guideline item / schema seed` 不准确。 | 改为“双样本单位：示例 SMS primary articles + 10 篇 SE systematic reviews”；说明前者局部示例、后者有系统编码表。 |
| C | SUMMARY 当前样本数量为 `--`，会掩盖 §3 的 10 篇 SR corpus。 | SUMMARY 行建议改为：样本单位 `SE systematic reviews（n=10）+ illustrative mapping articles（Figure 3 facet totals 118/128，非统一分母）`。 |
| C | 原生树类型写成“方法流程树 + taxonomy 示例树”不够。 | 改为“维度森林：SMS process/classification tree + map visualization facet tree + 10-review characterization tree”。 |
| I | A.2 证据账本大量写“待 A2a 精确页码复核”，但本文已可给 page / section / table / figure 锚点。 | 补 Page 2 Figure 1 / Table 1，Page 3 Table 2，Page 4 Figure 2 / Table 3，Page 5 Figure 3，Page 6--7 Table 4--5，Page 8--9 guideline。 |
| I | `EV-002/003` 过度泛化为 taxonomy / author_claim，未拆分 Figure 3 与 Table 5。 | 拆成 SMS process、keywording、research type taxonomy、map frequency、review characterization、guideline recommendation 等证据。 |
| I | Figure 3 的分母不一致。 | 显式保留 `research facet n=128`、`contribution facet n=118`，不要合并成一个样本数。 |
| I | `原文 schema 主树` 中出现 quality rubric、roadmap action、supplementary 等泛词，本文并无这些完整对象。 | 删除泛词，只保留本文真实字段：process、keywording、facets、rationale、frequencies、review characterization。 |
| M | 阅读状态可更新。 | 写明已做 PDF layout 文本核对，但仍未做图像视觉核验。 |
| M | metadata 的 `eligible_for_statistical_synthesis=false` 与“局部可统计”容易冲突。 | 不必改为 true；建议增加说明：false 指普通领域主统计池，Table 5 可作为方法学统计 seed。 |
| M | A.3 结论强度全为 weak，过度保守。 | 对直接由 Table 3 / Table 5 / §3 检索流程支持的 schema 结论可升为 `medium/text_verified`；final finding 仍保持不可用。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-P08-001 | `paper_content.txt`; `paper.pdf` | Abstract | BACKGROUND / METHOD | SMS 构建 classification scheme，并按类别频数分析；作者还系统分析 existing SRs。 | root_type | strong | 原文类型、双样本单位 | 否 | 只支撑本文定位 |
| EV-P08-002 | `paper_content.txt`; `paper.pdf` | §2 / Figure 1 | The Systematic Mapping Process | SMS 流程：RQ、search、screening、keywording、data extraction/mapping。 | process_schema | strong | Tree A process root | 是，图形布局 | 流程不是字段取值全集 |
| EV-P08-003 | `paper_content.txt`; `paper.pdf` | §2.1 / Table 1 | Research Questions for Systematic Maps | RQ 面向 areas、article counts、types、evaluation/novelty、journals/methods/context。 | rq_schema | medium | A.scope.goal | 是，表格布局 | 示例 RQ 不等于通用模板全集 |
| EV-P08-004 | `paper_content.txt`; `paper.pdf` | §2.2--§2.3 / Table 2 | search strings; inclusion/exclusion | search / screening 由 RQ 驱动；两个 map 的纳排不同。 | corpus_method | medium | A.search.*, A.screen.criteria | 是，表格布局 | 示例纳排不可跨主题照搬 |
| EV-P08-005 | `paper_content.txt`; `paper.pdf` | §2.4 / Figure 2 | Building the Classification Scheme | keywording 从 abstracts 提取概念，必要时读 intro/conclusion，聚类成 map categories。 | classification_generation | strong | A.keyword.source, A.schema_update | 是，图形布局 | 未给完整 keyword list |
| EV-P08-006 | `paper_content.txt`; `paper.pdf` | §2.4 / Table 3 | Research Type Facet | Wieringa 六类 research type 定义。 | taxonomy | strong | A.research_type | 是，表格布局 | 2008 分类需现代扩展 |
| EV-P08-007 | `paper_content.txt`; `paper.pdf` | §2.5 | Excel table / short rationale | extraction table 记录分类项，归类时提供 short rationale。 | extraction_evidence | strong | A.rationale | 否 | 未提供实际 Excel 附件 |
| EV-P08-008 | `paper_content.txt`; `paper.pdf` | §2.5 / Figure 3 | Bubble plot | topic × contribution / research type 的交叉频数和 bubble plot。 | statistical_visualization | medium | A.frequency, R5--R7 | 是，必须视觉核验 | 不迁移 SPL 领域分布 |
| EV-P08-009 | `paper_content.txt`; `paper.pdf` | §3 / Table 4 | Systematic Reviews Included | 检索 21 篇，筛入 8 篇，加 2 篇，共 10 篇 SR。 | sample_corpus | strong | Tree B review corpus | 是，表格布局 | 只代表 2008 前 SE SR |
| EV-P08-010 | `paper_content.txt`; `paper.pdf` | §3.1 / Table 5 | Systematic Review Characteristics | 对 10 篇 SR 编码 goals、inclusion requirements、article counts、analysis means。 | coding_schema | strong | B.* leaves | 是，表格布局 | `x` 逐格统计需 PDF 视觉复核 |
| EV-P08-011 | `paper_content.txt`; `paper.pdf` | §3.2 | Comparison | SMS 不建立 state of evidence，SR 更深；二者 gap 类型不同。 | boundary_claim | medium | finding boundary | 否 | 属方法边界，不是领域事实 |
| EV-P08-012 | `paper_content.txt`; `paper.pdf` | §4 | Guidelines | 方法互补、自适应阅读、按 evidence/novelty 分类、可视化数据。 | methodological_guideline | medium | candidate finding / migration | 否 | guideline 需后续研究裁决 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-P08-001 | 本文不是纯 guideline；它是 SMS 方法论文，并含 10 篇 SR 的嵌入式比较编码。 | type_and_unit | root | EV-P08-001, EV-P08-009, EV-P08-010 | strong | schema_seed / methodological_seed | 不代表普通领域统计池 |
| CLM-P08-002 | 原生结构应写成维度森林，而非单一六叶通用树。 | tree_type | native forest | EV-P08-002, EV-P08-006, EV-P08-008, EV-P08-010 | strong | review.md 维度树重写 | Tree A 示例 map 不含完整外部数据表 |
| CLM-P08-003 | §3 的样本单位是 10 篇 SE systematic reviews，且有明确检索与纳入链条。 | sample_unit | Tree B | EV-P08-009 | strong | SUMMARY 样本单位修正 | 额外 2 篇来自 Kitchenham 2007，不是原始检索 21 的直接筛选结果 |
| CLM-P08-004 | Table 5 的字段为 research goals、inclusion requirements、article counts、means of analysis。 | leaf_schema | Tree B leaves | EV-P08-010 | strong | 叶子维度表 | 逐格 `x` 值需视觉核验后统计 |
| CLM-P08-005 | SMS 示例 map 的核心字段包括 topic facet、contribution facet、research type facet、classification rationale 与 category frequency。 | leaf_schema | Tree A leaves | EV-P08-005, EV-P08-006, EV-P08-007, EV-P08-008 | medium | schema_seed | Figure 3 分母不统一 |
| CLM-P08-006 | 本文可局部统计方法学字段，但不进入普通 SE 领域主统计池。 | eligibility | statistical boundary | EV-P08-008, EV-P08-010, EV-P08-011 | medium | methodological_statistics / schema_seed | 不支持 Paper2 final domain finding |
| CLM-P08-007 | Paper2 可迁移的是 keywording、rationale、schema evolution、cross-facet frequency 与 candidate-gap 链路。 | migration | methodology | EV-P08-005, EV-P08-007, EV-P08-008, EV-P08-012 | medium | methodology design | 不迁移 SPL variability 枚举和 2008 年分布 |
| CLM-P08-008 | 统计观察、candidate finding、final finding 必须分层；低覆盖 cell 只能先作候选 gap。 | finding_boundary | R12 | EV-P08-008, EV-P08-011, EV-P08-012 | medium | candidate_finding | final finding 需跨论文反证和研究者裁决 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence discipline；强结论必须有证据，缺口降级。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 标准，返修建议必须具体可执行。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 rejection-risk audit 思路，区分 must-fix / should-fix / residual risk。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用“先读资源、显式标注不确定性、计划需可执行”的规则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“不编造细节，只提 unclear”的配置抽取原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化输出、risk 字段和依赖关系显式化。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 思路；不以“已总结”代替证据账本。

最高风险 3 点：

1. Figure 3 的气泡图虽然已用 `pdftotext -layout` 核对，但未做截图式视觉审查；A2a 应打开 PDF 人工核对每个气泡和百分比。
2. Tree A 的 SPL variability map 来源于 Mujtaba 2008，本文只摘述流程和 Figure 3；不能把它当成本文完整 primary-study extraction package。
3. Table 5 的 `x` 逐格值在文本抽取中可能错位；正式统计前应以 PDF 视觉版面逐格复核。

blocked / timeout / 文件缺失：

- 未出现 blocked。
- 未出现 timeout。
- 指定的技能文件、`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md` 均可读取。
- 本任务未修改仓库文件、未 commit、未 push、未发 gh comment、未启动 subagent。