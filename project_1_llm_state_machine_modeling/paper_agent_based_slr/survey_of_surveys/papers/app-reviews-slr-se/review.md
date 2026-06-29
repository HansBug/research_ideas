# Analysing app reviews for software engineering: a systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Analysing app reviews for software engineering: a systematic literature review |
| 作者 | Jacek Dąbrowski; Emmanuel Letier; Anna Perini; Angelo Susi |
| 年份 | 2022 |
| 类型 | SLR；面向 app reviews for software engineering。 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [ESE](https://link.springer.com/journal/10664) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | Empirical Software Engineering；正式 DOI、Springer PDF 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 63 页；未做复杂表格视觉级人工核对。 |
| 证据等级 | 全文文本级；复杂表格、搜索式和部分百分比需 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.1007/s10664-021-10065-7> |
| 综述类型 | SLR |
| SE 子领域 | app reviews / mobile user feedback / mining software repository。 |
| A1 角色 | 从失败路径升级为全文级现代高等级 SLR 样本：提供完整 RQ→抽取字段→分类 schema→统计表→discussion finding 的闭环。 |
| 是否目标证据池 | 是，作为 `survey_of_surveys/` 的 SLR 方法 / 报告结构 / 维度模式统计池样本；不是 Paper2 目标主题的领域证据。 |
| 是否统计池 | 是；可进入 A1 方法学统计池和 SLR/SMS 报告模式统计池。 |
| 一句话结论 | 这篇论文是 A1 中字段体系最完整的现代 SLR 样本之一，尤其适合迁移“多套分类 schema + 评价质量字段 + replication package 字段 + discussion finding”设计。 |

## 2. 论文内容详读

### 2.1 研究目标与 RQ

本文研究 app reviews 如何支持软件工程活动。作者提出五个 RQ：app review analysis 的类型、使用的技术、声称支持的软件工程活动、empirical evaluation 的方式、以及现有方法对软件工程师的支持效果。

该 RQ 设计对 Paper2 很有启发：它不是只问“有什么论文”，而是把目标对象拆成对象 / 信息类型、技术实现、软件工程活动、评价方式、评价结果五层。这种五层结构可迁移到 LLM4STM 或 agent-assisted SLR 主题：对象是什么、方法是什么、支持哪类工程活动、如何评价、结果能支撑什么结论。

### 2.2 搜索、筛选与纳排

论文遵循 Kitchenham 风格 SLR 流程：先定义 RQ 和 protocol，再执行自动检索、手工检索和 snowballing，最后抽取数据并回答 RQ。检索覆盖 2010 年 1 月至 2020 年 12 月；最终纳入 182 篇 primary studies，实际发表时间覆盖 2012--2020。数量链包括初始检索 1656 篇、去重 303 篇、筛选 1353 篇、排除 1225 篇，手工逐卷检索增加 14 篇，snowballing 增加 40 篇，最终形成 182 篇。

纳排标准强调：必须与软件工程相关、peer-reviewed，并使用 app reviews 支持至少一种软件工程活动；排除非英文、非 SE、secondary / tertiary studies、technical reports、manuals 等。

### 2.3 数据抽取字段

Table 3 给出 F1--F18 抽取表，覆盖：bibliographic 信息、review analysis 类型、mining technique、software engineering activity、justification、evaluation objective、evaluation procedure、metrics / criteria、evaluation result、annotated dataset、annotation task、annotators、quality measure、replication package 等。

这是 A1 最值得采纳的字段级证据模板之一。它说明一个高质量 SLR 不只记录“论文用了什么方法”，还要记录“评价用什么数据、谁标注、标注质量如何、是否公开 replication package”。这与 Paper2 的审计优先证据链高度一致。

### 2.4 分类 schema 与 reliability

作者构建三套 classification schema：app review analysis、mining technique、software engineering activity。分类过程使用 content analysis，先从 sample studies 中抽概念，再合并语义相近类别，最后由作者讨论并形成最终 schema。分类可靠性用 intra-rater 和 inter-rater agreement 检查：app review analysis、SE task、mining technique 的 inter-rater 约为 87%、87%、80%，intra-rater 约为 93%、100%、90%。

这说明维度模式不是任意主观命名，而应有构造过程、示例、合并规则和一致性检查。Paper2 后续若让 agent 自动提出 dimension pattern，也必须由研究者批准、记录修改理由和回填影响。

### 2.5 主要维度与统计结果

本文的 app review analysis 类型包括 classification、information extraction、content analysis、clustering、sentiment analysis、recommendation、summarization、search and information retrieval、visualization。mining technique 主要包括 NLP、ML、statistical analysis、manual analysis。SE activity 覆盖 requirements、maintenance、testing、design 等，且有一部分 studies 未明确指定 SE activity。

评价维度特别重要：109 篇研究做 empirical evaluation，105 篇做 effectiveness evaluation，23 篇做 user-perceived quality；RQ5 的结果来自 87 篇研究。作者还记录 public annotated datasets、public tools、annotators、annotation quality measure、replication package 等字段。公开数据和工具并不充分，这构成后续 discussion finding 的重要证据。

### 2.6 证据呈现与统计分析

本文是 A1 中统计呈现最丰富的样本之一：PRISMA 式筛选图、年度趋势、venue 类型图、top venue、highly cited papers、分类维度频次、analysis-technique 交叉表、analysis-SE activity 交叉表、dataset/tool 表、five-number summary、user-study criteria / participants 表、effectiveness range / median 表，以及 user-study qualitative result synthesis。

作者明确指出 primary studies 异质性太强，不适合做 meta-analysis，因此采用 summarizing effect estimates 这类描述性合成。这个判断可直接迁移为 Paper2 的统计纪律：异质字段先做分母清晰的描述统计和交叉表，不能为了显得“强”而硬做不成立的统计合成。

### 2.7 Discussion finding 与未来方向

本文的 discussion 把统计观察转化为多个 research implications，例如：需要更清晰的软件工程 use case、缺少 reference model、评价数据集偏小、replication package 不足、practice impact 不清、scalability / efficiency 评估不足、监督式 ML 训练数据成本和漂移问题等。

这对 Paper2 的启发非常直接：research finding 不是表格频次本身，而是“统计观察 + 解释 + 工程语境 + 不足 / 未来工作”。后续 agent 可以辅助提出 candidate finding，但必须保留支持证据、反证和研究者裁决。

### 2.8 效度威胁

作者列出四类主要威胁：关键词不完整、publication bias、筛选 / 抽取 / 分类主观性、taxonomy reliability。缓解方式包括 iterative keyword construction、specific + generic query、manual venue search、backward / forward snowballing、second coder sample cross-check、inter-coder / intra-coder agreement、content analysis 和作者讨论。

这些 threat pattern 可以迁移到 Paper2 的所有阶段：检索、筛选、抽取、分类、统计、候选 finding 都要对应记录风险与缓解，而不是只在最后写一段泛泛 limitations。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ1--RQ5 覆盖 analysis type、technique、SE activity、evaluation method、evaluation result。 | `paper_content.txt` §2.1。 | 可迁移为多层综述元模型：对象 / 方法 / 活动 / 评价 / 结果。 | app review 领域 RQ 不能直接改名套到 LLM4STM。 |
| dimension pattern | F1--F18 extraction form + 三套 classification schema + evaluation / artifact 字段。 | Table 3、§2.4、Table 4。 | 高度可迁移为 A2a 字段表和 reliability check 模板。 | 部分细分字段与 app review mining 特有。 |
| finding pattern | 从统计表形成 practice impact、evaluation quality、replication package、scalability、training cost 等 gaps。 | §4 Discussion、§6 Conclusion。 | 可迁移为 candidate finding ledger 的构造方式。 | 不能把 app review 领域 gap 写成 LLM4STM gap。 |
| evidence presentation pattern | PRISMA、频次表、交叉表、range/median、dataset/tool 表、qualitative result table。 | Figure 1--3、Table 5--23。 | 可迁移为 A2b 总账和 Paper2 结果呈现模式。 | 复杂表格需 PDF 视觉核对；OCR 中个别百分比错位。 |
| validity / threat pattern | 覆盖 query incompleteness、publication bias、screening/extraction/classification subjectivity、taxonomy reliability。 | §5 Threats to Validity。 | 可迁移为 agent-assisted SLR 分阶段风险表。 | 还需补充 LLM/provider/prompt/schema drift 等新风险。 |
| report structure pattern | Abstract → Introduction → Research Method → Results by RQ → Discussion → Threats → Related Work → Conclusion。 | 章节结构。 | 可迁移为现代高等级 SLR 报告结构。 | Paper2 还需加方法贡献、审计制品链和人机交互评估。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 用 RQ1--RQ5 定义对象、技术、SE activity、evaluation、result 五层元模型。 | 可迁移为目标主题的 researcher-defined meta-model。 | 需要由研究者决定哪些层适合目标主题。 |
| A1-M1 语料收集与纳排 | 给出数据库、时间窗、自动检索、手工检索、snowballing、纳排和数量链。 | 可迁移为 A2b 完整文库分母链条。 | 检索式在文本抽取中不完整，需 PDF 核对。 |
| A1-M2 研究对象与主题语义 | 把 mined information、SE activity 和 app review analysis 分层分类。 | 可迁移为对象 / 工件 / 生命周期活动分类。 | 领域语义必须重建，不能直接套用 app review taxonomy。 |
| A1-M3 方法 / 技术 / 干预 | NLP、ML、statistical、manual analysis 等技术分类，以及 analysis-technique 交叉表。 | 可迁移为 LLM/agent/tool/method/application-role 字段。 | 需扩展现代 LLM、agent 和 human-in-the-loop 取值。 |
| A1-M4 评价、证据与复现资产 | annotated dataset、metrics、quality measure、replication package、public tools 等字段。 | 可直接迁移为 Paper2 的 artifact / evaluation / evidence strength 模块。 | 必须区分“有 replication package”与“可复现质量高”。 |
| A1-M5 统计分析就绪 | 大量频次、百分比、交叉表、range/median、five-number summary。 | 可迁移为分母固定、字段版本化、missing-value 语义和交叉统计。 | 异质结果只做描述性合成，不强行 meta-analysis。 |
| A1-M6 research finding 形成与裁决 | Discussion 将统计观察转化为 research implications 和 future work。 | 可迁移为“统计观察 → 候选 finding → 研究者裁决”的台账流程。 | 需要记录支持 / 反证 / scope / claim strength。 |

## 5. 可迁移字段树 / 维度锚点

```text
modern_slr_field_pattern
├── research_question_layers
│   ├── analysis_or_object_type
│   ├── technique_or_method
│   ├── supported_engineering_activity
│   ├── evaluation_method
│   └── evaluation_result
├── corpus_and_screening
│   ├── automatic_database_search
│   ├── manual_venue_search
│   ├── backward_forward_snowballing
│   ├── inclusion_exclusion_criteria
│   ├── duplicate_count
│   ├── excluded_count
│   └── final_included_count
├── extraction_fields
│   ├── bibliographic_metadata
│   ├── analysis_type
│   ├── technique_type
│   ├── engineering_activity
│   ├── evaluation_objective
│   ├── evaluation_procedure
│   ├── metrics_and_criteria
│   ├── evaluation_result
│   ├── annotated_dataset
│   ├── annotation_quality
│   └── replication_package
├── classification_schema
│   ├── content_analysis_seed
│   ├── category_merge_split
│   ├── intra_rater_agreement
│   ├── inter_rater_agreement
│   └── final_taxonomy_version
├── statistical_presentation
│   ├── frequency_table
│   ├── cross_tabulation
│   ├── trend_plot
│   ├── range_median_summary
│   └── no_meta_analysis_rationale
└── finding_adjudication
    ├── statistical_observation
    ├── practical_gap
    ├── evidence_strength
    ├── future_work
    └── researcher_judgment_needed
```

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **字段表应覆盖 evaluation 和 artifact**：仅抽输入、输出、方法不够；还要抽评价数据、指标、标注者、质量度量和复制包。
2. **classification schema 需要可靠性证据**：即便是人工 SLR，也要报告 inter-rater / intra-rater；Paper2 的 agent-assisted 抽取更需要 disagreement / adjudication 记录。
3. **discussion finding 要有统计来源**：该文的 gap 来自具体统计与表格，而不是作者随意观点。
4. **异质性是正常情况**：不能把所有 primary studies 强行汇入一个统一效果值；更适合用描述统计、交叉表和分层解释。
5. **可复现资产是字段，不是附带说明**：replication package 和公开数据集应成为 Paper2 的一等抽取维度。

### 6.2 风险

1. `paper_content.txt` 对搜索式、部分表格和百分比抽取存在错位；A2a 正式统计前需视觉核对。
2. app review mining 的细分 taxonomy 与 LLM4STM 不同，只能迁移结构和字段设计，不迁移领域结论。
3. 本文虽然记录 replication package，但没有完整评价制品质量；Paper2 需要更强的 audit artifact completeness rubric。
4. 如果后续只学习它的表格而不学习它的 reliability / threat 设计，就会变成“漂亮总账但弱证据”。

## 7. 待复核

1. 视觉核对 Figure 1（p.4）的 PRISMA 数量链。
2. 视觉核对 p.5 搜索式；当前 `paper_content.txt` 对 exact query 抽取不完整。
3. 视觉核对 p.4--5 digital libraries 数量；文本称 six major digital libraries，但抽取文本只清楚显示五个名称。
4. 视觉核对 Figure 2、Figure 3 和 Table 5--7 的年度、venue 和 analysis type 统计。
5. 视觉核对 Table 9--15 的 technique / SE activity 交叉表，尤其多列表格对齐。
6. 视觉核对 Table 16--23 的 dataset、tool、five-number summary、effectiveness range / median 和 related survey comparison。

## 维度树复原

### 一句话结论

本文的维度树主类型为“RQ 驱动分类树”，辅助类型为“评价 / 复现资产审计树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-app-reviews-slr-se-tree-type]

旧有“可迁移字段树 / 字段树 / schema 缺口”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-app-reviews-slr-se-root] | Analysing app reviews for software engineering 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-app-reviews-slr-se-b1] app review analysis 类型；[dim-app-reviews-slr-se-b2] mining technique；[dim-app-reviews-slr-se-b3] 支持的软件工程活动；[dim-app-reviews-slr-se-b4] 评价与复现资产；[dim-app-reviews-slr-se-b5] discussion gap | [ev-app-reviews-slr-se-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-app-reviews-slr-se-root] Analysing app reviews for software engineering
├── [dim-app-reviews-slr-se-b1] app review analysis 类型
│   └── [leaf-app-reviews-slr-se-scope] 研究范围与单位对象
├── [dim-app-reviews-slr-se-b2] mining technique
│   └── [leaf-app-reviews-slr-se-corpus] 语料与纳排链条
├── [dim-app-reviews-slr-se-b3] 支持的软件工程活动
│   └── [leaf-app-reviews-slr-se-taxonomy] 主题与维度分类
├── [dim-app-reviews-slr-se-b4] 评价与复现资产
│   └── [leaf-app-reviews-slr-se-method] 方法 / 技术 / 干预分类
└── [dim-app-reviews-slr-se-b5] discussion gap
    └── [leaf-app-reviews-slr-se-evidence] 评价、证据与复现资产
    └── [leaf-app-reviews-slr-se-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-app-reviews-slr-se-scope] | 研究范围与单位对象 | [dim-app-reviews-slr-se-b1] | 定义 App reviews / mobile user feedback 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-scope] |
| [leaf-app-reviews-slr-se-corpus] | 语料与纳排链条 | [dim-app-reviews-slr-se-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-corpus] |
| [leaf-app-reviews-slr-se-taxonomy] | 主题与维度分类 | [dim-app-reviews-slr-se-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-taxonomy] |
| [leaf-app-reviews-slr-se-method] | 方法 / 技术 / 干预分类 | [dim-app-reviews-slr-se-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-method] |
| [leaf-app-reviews-slr-se-evidence] | 评价、证据与复现资产 | [dim-app-reviews-slr-se-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-evidence] |
| [leaf-app-reviews-slr-se-finding] | 统计观察与候选发现 | [dim-app-reviews-slr-se-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-app-reviews-slr-se-leaf-finding] |

### 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据引用 | 结论引用 |
|---|---|---|---|---|---|---|---|
| [edge-app-reviews-slr-se-method-evidence] | [leaf-app-reviews-slr-se-method] | 支撑 / 度量 | [leaf-app-reviews-slr-se-evidence] | 工具 / 指标 / 数据集 / artifact / not_reported | 未报告评价或复现资产时写 `not_reported` | [ev-app-reviews-slr-se-taxonomy] | [clm-app-reviews-slr-se-edge-method-evidence] |
| [edge-app-reviews-slr-se-taxonomy-finding] | [leaf-app-reviews-slr-se-taxonomy] | 导出候选发现 | [leaf-app-reviews-slr-se-finding] | gap / recommendation / trend / limitation | 无 discussion 支撑时写 `not_reported` | [ev-app-reviews-slr-se-stat] | [clm-app-reviews-slr-se-edge-taxonomy-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-app-reviews-slr-se-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 是 | 识别可迁移的维度模式类型 | 可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 |
| [leaf-app-reviews-slr-se-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 是 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-app-reviews-slr-se-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-app-reviews-slr-se-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | App reviews / mobile user feedback 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-app-reviews-slr-se-transfer] |
| [leaf-app-reviews-slr-se-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-app-reviews-slr-se-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-app-reviews-slr-se-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-app-reviews-slr-se-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-app-reviews-slr-se-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-app-reviews-slr-se-001 | [ev-app-reviews-slr-se-root] | [src-app-reviews-slr-se-text], [src-app-reviews-slr-se-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | strong | [dim-app-reviews-slr-se-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-app-reviews-slr-se-002 | [ev-app-reviews-slr-se-taxonomy] | [src-app-reviews-slr-se-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度。 | taxonomy | medium | [dim-app-reviews-slr-se-b1], [dim-app-reviews-slr-se-b2], [dim-app-reviews-slr-se-b3], [dim-app-reviews-slr-se-b4], [dim-app-reviews-slr-se-b5], [leaf-app-reviews-slr-se-taxonomy], [leaf-app-reviews-slr-se-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-app-reviews-slr-se-003 | [ev-app-reviews-slr-se-stat] | [src-app-reviews-slr-se-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | statistical_result | medium | [leaf-app-reviews-slr-se-evidence], [leaf-app-reviews-slr-se-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-app-reviews-slr-se-004 | [ev-app-reviews-slr-se-risk] | [src-app-reviews-slr-se-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | medium | [dim-app-reviews-slr-se-root], [leaf-app-reviews-slr-se-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |
| EV-app-reviews-slr-se-005 | [ev-app-reviews-slr-se-relation] | [src-app-reviews-slr-se-text] | paper_content.txt | 结果 / 讨论相关页；待 A2a 精确页码复核 | 关系 / 交叉表 / discussion 邻近段落 | 关系型表或交叉统计 | -- | 见释义 | 原文将分类字段与评价、工具、指标、artifact 或 discussion finding 连接，本记录用于支撑关系边。 | taxonomy | medium | [edge-app-reviews-slr-se-method-evidence], [edge-app-reviews-slr-se-taxonomy-finding] | true | false | -- | 关系边只表示本文中的字段联系，不能外推为目标领域因果关系。 |

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-app-reviews-slr-se-tree-type] | A1DT-app-reviews-slr-se-C01 | 本文的维度树主类型为“RQ 驱动分类树”，辅助类型为“评价 / 复现资产审计树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-app-reviews-slr-se-tree-type] | tree_type | [dim-app-reviews-slr-se-root] | EV-app-reviews-slr-se-001, EV-app-reviews-slr-se-004 | 树型判断仅限本文，不代表所有 App reviews / mobile user feedback 综述。 | strong | statistical_synthesis | false | -- |
| [clm-app-reviews-slr-se-leaf-scope] | A1DT-app-reviews-slr-se-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-scope] | EV-app-reviews-slr-se-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-app-reviews-slr-se-leaf-corpus] | A1DT-app-reviews-slr-se-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-corpus] | EV-app-reviews-slr-se-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-app-reviews-slr-se-leaf-taxonomy] | A1DT-app-reviews-slr-se-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-taxonomy] | EV-app-reviews-slr-se-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-app-reviews-slr-se-leaf-method] | A1DT-app-reviews-slr-se-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-method] | EV-app-reviews-slr-se-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-app-reviews-slr-se-leaf-evidence] | A1DT-app-reviews-slr-se-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-evidence] | EV-app-reviews-slr-se-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-app-reviews-slr-se-leaf-finding] | A1DT-app-reviews-slr-se-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-app-reviews-slr-se-finding] | EV-app-reviews-slr-se-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-app-reviews-slr-se-transfer] | A1DT-app-reviews-slr-se-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-app-reviews-slr-se-root] | EV-app-reviews-slr-se-002, EV-app-reviews-slr-se-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | medium | schema_seed | false | -- |
| [clm-app-reviews-slr-se-finding-boundary] | A1DT-app-reviews-slr-se-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-app-reviews-slr-se-finding] | EV-app-reviews-slr-se-003, EV-app-reviews-slr-se-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | medium | candidate_finding | false | -- |
| [clm-app-reviews-slr-se-edge-method-evidence] | A1DT-app-reviews-slr-se-C10 | 方法 / 技术节点与评价 / 证据节点之间存在可审计关系，适合作为 Paper2 字段间关系的 schema seed。 | relation_edge | [edge-app-reviews-slr-se-method-evidence] | EV-app-reviews-slr-se-005 | 关系含义限于本文分类和统计表，不代表因果关系。 | medium | schema_seed | false | -- |
| [clm-app-reviews-slr-se-edge-taxonomy-finding] | A1DT-app-reviews-slr-se-C11 | 主题 / 分类节点可通过统计观察或 discussion 支撑候选发现，但不能绕过研究者裁决。 | relation_edge | [edge-app-reviews-slr-se-taxonomy-finding] | EV-app-reviews-slr-se-005 | 候选发现仍需反证、scope 与 claim strength 审核。 | medium | candidate_finding | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-app-reviews-slr-se-structure-check] | [dim-app-reviews-slr-se-root], A1DT-app-reviews-slr-se-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-app-reviews-slr-se-visual-check] | EV-app-reviews-slr-se-002, EV-app-reviews-slr-se-003, EV-app-reviews-slr-se-005 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
