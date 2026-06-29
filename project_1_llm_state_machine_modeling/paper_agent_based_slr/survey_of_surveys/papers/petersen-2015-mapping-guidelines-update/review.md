# Guidelines for conducting systematic mapping studies in software engineering: An update

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Guidelines for conducting systematic mapping studies in software engineering: An update |
| 作者 | Kai Petersen; Sairam Vakkalanka; Ludwik Kuzniarz |
| 年份 | 2015 |
| 类型 | systematic mapping guideline update；对 SE systematic mapping studies 的 systematic map。 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology；DOI 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 18 页；未做图表视觉级人工核对。 |
| 证据等级 | 全文文本级；复杂图表 / 附录矩阵待 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.1016/j.infsof.2015.03.007> |
| 综述类型 | mapping guideline update / systematic mapping of systematic maps。 |
| SE 子领域 | 软件工程 systematic mapping 方法学。 |
| A1 角色 | 从失败路径升级为全文级核心方法锚点：用于抽取 planning-conducting-reporting 流程、topic-independent dimensions、validity taxonomy、reporting structure、quality rubric。 |
| 是否目标证据池 | 否；它支撑综述方法学与 模式种子，不支撑某一目标 SE 主题的领域结论。 |
| 是否统计池 | 是，但仅限 A1 `survey_of_surveys/` 的方法学统计池；不能作为目标领域效果 / 因果统计证据。 |
| 一句话结论 | 这篇论文是 A1 中最关键的 SMS guideline update：它证明“维度模式”和“报告 / 效度 / 评价 rubric”本身可以从综述之综述中抽取、统计、回修。 |

## 2. 论文内容详读

### 2.1 研究目标与定位

本文的出发点是：2008 年的 systematic mapping guideline 已经不足以覆盖后来软件工程 mapping studies 的真实做法，许多研究会组合多个 guideline，导致实践差异较大。因此作者通过对既有 mapping studies 做 systematic mapping，识别这些研究如何执行搜索、选择、分类、可视化、效度和报告，并据此更新 guideline。

这篇论文对 Paper2 的价值在于，它不仅说明“如何做 mapping”，还说明“如何从一批已有 mapping studies 中抽出方法 pattern，再反过来更新 guideline”。这与 A1/A2a 的定位完全一致：先从综述论文中抽模式，而不是直接写目标领域发现。

### 2.2 RQ 与方法流程

作者设置四个 RQ：

1. 哪些 guidelines 被用于 SE systematic mapping studies。
2. 这些 studies 覆盖哪些 SE topics。
3. 它们在哪里、何时发表。
4. 它们如何执行 systematic mapping process，包括 study identification、分类方案和结果可视化。

方法上，作者使用 IEEE Xplore、ACM、Scopus、Inspec/Compendex；以 systematic mapping 相关词、software engineering、method / classification / guideline 等词构造检索式；用 EndNote 去重；先 title/abstract，再 full-text，再 backward snowballing；最终对纳入研究做 quality assessment 和数据抽取。

### 2.3 纳排、质量评价与抽取表

纳入标准包括：论文呈现 systematic mapping study 的研究方法与结果、属于软件工程、发表在 2004--2012。排除标准包括 conference summary / editorial、guideline/template 本身、非 peer-reviewed、非英文、全文不可得、书籍 / 灰色文献、重复研究。

质量评价问题包括：mapping 动机是否清楚；mapping process 是否清楚定义；是否有该 mapping process 的 empirical evidence / 结果。数据抽取表覆盖 study ID、title、authors、year、SWEBOK area、venue、使用的 guidelines、search strategy、search type、classification scheme、visualization type。

这些字段几乎可以直接迁移为 A2a 对 SLR/SMS 文献的 extraction form。

### 2.4 guideline update 与维度模式

本文把 mapping guideline 组织为三大阶段：planning、conducting、reporting。Planning 中包括 need identification / scoping、study identification、data extraction and classification、visualization、validity threats、evaluate the mapping。Conducting 强调执行搜索、筛选、抽取、分类和可视化；Reporting 强调标准化结构、可复用性和可比较性。

作者还抽出了可跨主题使用的 topic-independent dimensions，包括 research type、research method、study focus、venue；传统 contribution type 并不总是最通用。topic-specific classification 则可来自 emergent scheme 或既有知识体系，例如 SWEBOK / IEEE / ISO 标准。

对 Paper2 来说，这直接支持“维度 pattern 类似树结构”的判断：有横向通用维度，也有主题特化维度；两者需要由研究者裁决后组合，而不是由 LLM 自动一次性定死。

### 2.5 证据呈现、统计与评价 rubric

本文大量使用频数、比例、分布图、bubble plot、bar chart、pie diagram、Venn diagram、heatmap 和附录矩阵来呈现 mapping studies 的方法差异。作者还构建了用于评价 systematic map 质量的 action / rubric，并报告不同 studies 在 rubric 上的表现。

这说明 survey-of-surveys 不只是收摘要：它可以抽取“哪些维度被使用、哪些可视化被使用、哪些 validity 被报告、哪些 reporting 结构被采用”，并对这些方法维度做统计。这是 A1/A2b 后续大文库的直接统计目标。

### 2.6 效度威胁

作者在 §3.6 使用 descriptive validity、theoretical validity、generalizability、interpretive validity 等框架，讨论搜索漏检、单人筛选 / 抽取偏差、术语混淆、样本代表性和结论解释风险。其缓解方式包括 backward snowballing、reference set validation、抽取表、抽取回溯、纳排后的复查和明确 reporting。

这对 Paper2 有两个强启发：第一，agent 辅助抽取必须把单点自动判断升级为可回溯证据；第二，研究者裁决不是装饰，而是对 selection / extraction / interpretation bias 的核心缓解机制。

### 2.7 报告结构

本文建议 systematic map 报告结构尽量标准化，包括 Introduction、Related Work、Research Method、Results、Discussion / Conclusions 和 Appendix。Research Method 应包含 research question、search、study selection、data extraction、quality assessment、analysis and classification、validity evaluation。附录可保留纳入 / 排除边界论文与矩阵表。

这对 `survey_of_surveys/` 后续文库有直接价值：A2a/A2b 的单篇 review 和总账应显式记录 report structure pattern，而不能只写“这篇讲了什么”。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖 guideline 使用、SE topic、venue/year、mapping process execution。 | `paper_content.txt` §3.1。 | 可迁移为“方法实践如何被执行”的 survey-of-surveys RQ 模板。 | 不回答具体 SE 技术效果。 |
| dimension pattern | 抽出 topic-independent dimensions：research type、research method、study focus、venue；topic-specific classification 可来自 emergent / existing scheme。 | §5.1、Table 5、Appendix B。 | 高度可迁移为 A2a 初版维度模式库。 | 具体维度需与目标主题和研究者 meta-model 对齐。 |
| finding pattern | 从 mapping studies 的实践差异形成 guideline update、rubric 和改进建议。 | §5、§6。 | 可迁移为“统计方法实践 → guideline 修订”的 finding heuristic。 | finding 属方法学裁决，不是领域效果结论。 |
| evidence presentation pattern | 以流程图、频数表、分布图、可视化类型统计、quality rubric、附录矩阵呈现证据。 | Figure 1、Table 3、Table 8、Table 14、Appendix A/B。 | 可迁移到 A2b 的 pattern evidence dashboard。 | 图表和附录表格复杂，需 PDF 视觉核对。 |
| validity / threat pattern | 使用 descriptive/theoretical/generalizability/interpretive validity，记录单人筛选、漏检、分类误差和代表性风险。 | §3.6、§5.1.5、Table 13。 | 可迁移为 agent-assisted SLR 的 threat taxonomy。 | 需要补充 LLM/provider drift、prompt drift、schema revision bias 等现代风险。 |
| report structure pattern | 标准化 systematic map 报告结构，并建议纳入附录清单与排除边界。 | §5.3。 | 可迁移为 A2a/A2b 单篇 review 和最终论文 method/reporting 结构。 | Paper2 还要加入 human-in-the-loop、候选发现裁决和审计制品链。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 将研究目标定义为更新 mapping guideline，并明确为何单一 guideline 不足。 | A2a 可用“方法实践差异 → guideline update”作为综述之综述元模型。 | 不能把 guideline update 误写成领域事实。 |
| A1-M1 语料收集与纳排 | 数据库、检索式、时间窗、title/abstract/full-text、snowball、quality assessment 都有清楚记录。 | 可迁移为 A2b 完整文库检索和纳排总账模板。 | 单人筛选风险需要额外裁决 / double-check 记录。 |
| A1-M2 研究对象与主题语义 | 使用 SWEBOK area、topic categories、study focus 等定义研究对象语义。 | 可迁移为主题语义树和横向方法维度并存的字段设计。 | SWEBOK 与现代 LLM/agent 主题存在时代差异。 |
| A1-M3 方法 / 技术 / 干预 | 记录 search strategy、search type、classification scheme、visualization type、guideline adoption。 | 可迁移为“agent 做了哪些环节、人做了哪些环节、分类与可视化如何执行”的方法字段。 | 需扩展 LLM/agent role、prompting、工具链和交互日志字段。 |
| A1-M4 评价、证据与复现资产 | 有 data extraction form、validity schema、quality rubric、included studies appendix。 | 可迁移为字段证据、schema version、reviewer check、artifact completeness 的审计资产。 | 本文的开放制品要求不如 Paper2 高，不能降低审计标准。 |
| A1-M5 统计分析就绪 | 对 guideline、topic、venue、search、classification、visualization、rubric score 做计数与分布。 | 可迁移为 A2b 的方法学统计池。 | 只能做方法学频次 / 分布统计，不支持目标领域效果合成。 |
| A1-M6 research finding 形成与裁决 | 从方法实践统计形成更新 guideline 和质量评价建议。 | 可迁移为“统计观察 → 方法学 finding → researcher 裁决”的模板。 | 最终领域 finding 必须另由目标主题证据支持。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
mapping_guideline_update_pattern
├── guideline_usage
│   ├── followed_guideline
│   ├── combined_guidelines
│   ├── missing_guideline_coverage
│   └── update_rationale
├── mapping_process
│   ├── planning
│   │   ├── need_identification
│   │   ├── scoping
│   │   ├── study_identification_plan
│   │   ├── extraction_classification_plan
│   │   ├── visualization_plan
│   │   └── validity_plan
│   ├── conducting
│   │   ├── search_database
│   │   ├── search_type
│   │   ├── screening_stage
│   │   ├── quality_assessment
│   │   ├── data_extraction_form
│   │   └── classification_scheme
│   └── reporting
│       ├── method_section_structure
│       ├── results_structure
│       ├── included_excluded_appendix
│       └── repeatability_detail
├── dimensions
│   ├── topic_independent
│   │   ├── research_type
│   │   ├── research_method
│   │   ├── study_focus
│   │   └── venue
│   └── topic_specific
│       ├── emergent_scheme
│       └── existing_scheme
├── visualization_and_statistics
│   ├── frequency_table
│   ├── distribution_plot
│   ├── bubble_plot
│   ├── venn_diagram
│   ├── heatmap
│   └── quality_rubric_score
└── validity_and_quality
    ├── descriptive_validity
    ├── theoretical_validity
    ├── generalizability
    ├── interpretive_validity
    ├── repeatability
    └── researcher_bias_mitigation
```

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **A1/A2a 本质上也是 guideline update 的前置工作**：我们不是为了堆论文，而是为了从 SE 综述实践中抽出适合 agentic SLR 的维度与证据规范。
2. **维度模式必须分通用层和主题层**：research type / venue / method 这类通用字段，与 LLM4STM / LLM4SE / MDE 等主题字段应分层组合。
3. **评价 rubric 可以成为方法贡献**：Paper2 可以为 agent-assisted SLR 提出审计制品完整性、字段证据完整性、finding 裁决完整性的 rubric。
4. **报告结构本身是可抽取对象**：后续写论文时，应把综述方法、字段表、统计观察、候选发现和裁决日志作为标准报告部件。
5. **效度威胁必须流程化**：每个阶段都要有风险与缓解，例如搜索、筛选、抽取、分类、统计、finding 形成、研究者裁决。

### 6.2 风险

1. 本文的数字链条和 Appendix B 很复杂，A2a 若要精确统计必须视觉核对，不能只依赖 `paper_content.txt`。
2. 2015 的 guideline update 仍未覆盖 LLM/agent/provider drift、prompt drift、schema drift 等新风险，Paper2 需要补充。
3. 该文以 mapping studies 为对象，不能直接告诉我们 LLM-assisted SLR 是否有效，只能告诉我们如何设计字段和审计方法。
4. 如果把本文纳入统计池，必须标注“方法学统计池”，避免与目标领域统计池混淆。

## 7. 待复核

1. 视觉核对 Figure 1（p.5）的 selection flow，特别是 7752、5082、60、43、54、44、52+8+11 等链条。
2. 视觉核对 Table 5（p.8--9）的 guideline comparison matrix。
3. 视觉核对 Figure 5--15（p.6--8）的分布 / 分类 / validity 图。
4. 视觉核对 Figure 16--19（p.9--13）中 search reflection、study selection、venue classification 和 research method classification。
5. 视觉核对 Table 8、Table 14、Figure 20--21（p.14--15）中的 rubric 与质量分布。
6. 若 A2a 要精确复用 Appendix B 的逐篇映射，需要人工检查 p.16--17 的 B.15--B.27 表格。

## 维度树复原

### 一句话结论

本文的维度树主类型为“mapping guideline update 方法树”，辅助类型为“topic-independent dimensions 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-petersen-2015-mapping-guidelines-update-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-petersen-2015-mapping-guidelines-update-root] | Guidelines for conducting systematic mapping studies in software engineering 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-petersen-2015-mapping-guidelines-update-b1] planning；[dim-petersen-2015-mapping-guidelines-update-b2] conducting；[dim-petersen-2015-mapping-guidelines-update-b3] reporting；[dim-petersen-2015-mapping-guidelines-update-b4] quality rubric；[dim-petersen-2015-mapping-guidelines-update-b5] topic-independent dimensions | [ev-petersen-2015-mapping-guidelines-update-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-petersen-2015-mapping-guidelines-update-root] Guidelines for conducting systematic mapping studies in software engineering
├── [dim-petersen-2015-mapping-guidelines-update-b1] planning
│   └── [leaf-petersen-2015-mapping-guidelines-update-scope] 研究范围与单位对象
├── [dim-petersen-2015-mapping-guidelines-update-b2] conducting
│   └── [leaf-petersen-2015-mapping-guidelines-update-corpus] 语料与纳排链条
├── [dim-petersen-2015-mapping-guidelines-update-b3] reporting
│   └── [leaf-petersen-2015-mapping-guidelines-update-taxonomy] 主题与维度分类
├── [dim-petersen-2015-mapping-guidelines-update-b4] quality rubric
│   └── [leaf-petersen-2015-mapping-guidelines-update-method] 方法 / 技术 / 干预分类
└── [dim-petersen-2015-mapping-guidelines-update-b5] topic-independent dimensions
    └── [leaf-petersen-2015-mapping-guidelines-update-evidence] 评价、证据与复现资产
    └── [leaf-petersen-2015-mapping-guidelines-update-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-petersen-2015-mapping-guidelines-update-scope] | 研究范围与单位对象 | [dim-petersen-2015-mapping-guidelines-update-b1] | 定义 SMS 方法学 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-scope] |
| [leaf-petersen-2015-mapping-guidelines-update-corpus] | 语料与纳排链条 | [dim-petersen-2015-mapping-guidelines-update-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-corpus] |
| [leaf-petersen-2015-mapping-guidelines-update-taxonomy] | 主题与维度分类 | [dim-petersen-2015-mapping-guidelines-update-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-taxonomy] |
| [leaf-petersen-2015-mapping-guidelines-update-method] | 方法 / 技术 / 干预分类 | [dim-petersen-2015-mapping-guidelines-update-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-method] |
| [leaf-petersen-2015-mapping-guidelines-update-evidence] | 评价、证据与复现资产 | [dim-petersen-2015-mapping-guidelines-update-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-evidence] |
| [leaf-petersen-2015-mapping-guidelines-update-finding] | 统计观察与候选发现 | [dim-petersen-2015-mapping-guidelines-update-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2015-mapping-guidelines-update-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-petersen-2015-mapping-guidelines-update-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-petersen-2015-mapping-guidelines-update-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-petersen-2015-mapping-guidelines-update-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-petersen-2015-mapping-guidelines-update-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | SMS 方法学 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-petersen-2015-mapping-guidelines-update-transfer] |
| [leaf-petersen-2015-mapping-guidelines-update-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-petersen-2015-mapping-guidelines-update-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-petersen-2015-mapping-guidelines-update-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-petersen-2015-mapping-guidelines-update-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-petersen-2015-mapping-guidelines-update-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-petersen-2015-mapping-guidelines-update-001 | [ev-petersen-2015-mapping-guidelines-update-root] | [src-petersen-2015-mapping-guidelines-update-text], [src-petersen-2015-mapping-guidelines-update-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-petersen-2015-mapping-guidelines-update-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-petersen-2015-mapping-guidelines-update-002 | [ev-petersen-2015-mapping-guidelines-update-taxonomy] | [src-petersen-2015-mapping-guidelines-update-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-petersen-2015-mapping-guidelines-update-b1], [dim-petersen-2015-mapping-guidelines-update-b2], [dim-petersen-2015-mapping-guidelines-update-b3], [dim-petersen-2015-mapping-guidelines-update-b4], [dim-petersen-2015-mapping-guidelines-update-b5], [leaf-petersen-2015-mapping-guidelines-update-taxonomy], [leaf-petersen-2015-mapping-guidelines-update-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-petersen-2015-mapping-guidelines-update-003 | [ev-petersen-2015-mapping-guidelines-update-stat] | [src-petersen-2015-mapping-guidelines-update-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-petersen-2015-mapping-guidelines-update-evidence], [leaf-petersen-2015-mapping-guidelines-update-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-petersen-2015-mapping-guidelines-update-004 | [ev-petersen-2015-mapping-guidelines-update-risk] | [src-petersen-2015-mapping-guidelines-update-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-petersen-2015-mapping-guidelines-update-root], [leaf-petersen-2015-mapping-guidelines-update-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-petersen-2015-mapping-guidelines-update-tree-type] | A1DT-petersen-2015-mapping-guidelines-update-C01 | 本文的维度树主类型为“mapping guideline update 方法树”，辅助类型为“topic-independent dimensions 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-petersen-2015-mapping-guidelines-update-tree-type] | tree_type | [dim-petersen-2015-mapping-guidelines-update-root] | EV-petersen-2015-mapping-guidelines-update-001, EV-petersen-2015-mapping-guidelines-update-004 | 树型判断仅限本文，不代表所有 SMS 方法学 综述。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-scope] | A1DT-petersen-2015-mapping-guidelines-update-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-scope] | EV-petersen-2015-mapping-guidelines-update-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-corpus] | A1DT-petersen-2015-mapping-guidelines-update-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-corpus] | EV-petersen-2015-mapping-guidelines-update-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-taxonomy] | A1DT-petersen-2015-mapping-guidelines-update-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-taxonomy] | EV-petersen-2015-mapping-guidelines-update-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-method] | A1DT-petersen-2015-mapping-guidelines-update-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-method] | EV-petersen-2015-mapping-guidelines-update-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-evidence] | A1DT-petersen-2015-mapping-guidelines-update-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-evidence] | EV-petersen-2015-mapping-guidelines-update-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-leaf-finding] | A1DT-petersen-2015-mapping-guidelines-update-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2015-mapping-guidelines-update-finding] | EV-petersen-2015-mapping-guidelines-update-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-transfer] | A1DT-petersen-2015-mapping-guidelines-update-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-petersen-2015-mapping-guidelines-update-root] | EV-petersen-2015-mapping-guidelines-update-002, EV-petersen-2015-mapping-guidelines-update-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-petersen-2015-mapping-guidelines-update-finding-boundary] | A1DT-petersen-2015-mapping-guidelines-update-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-petersen-2015-mapping-guidelines-update-finding] | EV-petersen-2015-mapping-guidelines-update-003, EV-petersen-2015-mapping-guidelines-update-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-petersen-2015-mapping-guidelines-update-structure-check] | [dim-petersen-2015-mapping-guidelines-update-root], A1DT-petersen-2015-mapping-guidelines-update-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-petersen-2015-mapping-guidelines-update-visual-check] | EV-petersen-2015-mapping-guidelines-update-002, EV-petersen-2015-mapping-guidelines-update-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
