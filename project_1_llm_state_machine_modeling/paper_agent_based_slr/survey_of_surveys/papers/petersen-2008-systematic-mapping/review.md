# Systematic Mapping Studies in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Mapping Studies in Software Engineering |
| 作者 | Kai Petersen; Robert Feldt; Shahid Mujtaba; Michael Mattsson |
| 年份 | 2008 |
| 类型 | SMS 方法论文；包含 systematic mapping process、分类维度构造、map/review 对照和 guideline 扩展建议。 |
| 出版形态 | 会议 |
| 期刊/会议/预印本 | [EASE](https://conf.researchr.org/series/ease) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | C |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | EASE 2008 / BCS Electronic Workshops in Computing；DOI 与用户本地 Zotero PDF 已核验。 |
| 阅读状态 | 已读 `bibtex.bib`、`paper_content.txt` 全文；已用 `pdfinfo` 核对 `paper.pdf` 为 10 页；未做图表视觉级人工核对。 |
| 证据等级 | 全文文本级；图表 / 表格布局待 A2a 人工原文核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.14236/ewic/EASE2008.8> |
| 综述类型 | SMS 方法论文 / systematic mapping 方法学 seed。 |
| SE 子领域 | 软件工程 systematic mapping 方法学。 |
| A1 角色 | 从失败路径升级为全文级方法学种子：提供 SMS 流程、keywording、三维分类 facet、频数 / bubble plot 呈现、map 与 review 的互补边界。 |
| 是否目标证据池 | 否；只作为 `survey_of_surveys/` 的方法学 模式种子，不作为某个 SE 主题领域事实。 |
| 是否统计池 | 不进入普通 SLR/SMS 领域统计池；其内部频数和 map/review 对照只可作为方法学描述性统计 seed。 |
| 一句话结论 | 这篇论文最适合支撑 Paper2 的“维度模式会随阅读演化、字段值要有 rationale、统计观察主要来自类别频数和交叉覆盖”的方法故事。 |

## 2. 论文内容详读

### 2.1 论文定位与目标

本文的目标不是回答某个具体技术是否有效，而是把 systematic mapping 引入软件工程，说明其流程、产物和与 systematic review 的区别。作者在摘要和 §2.1 中把 mapping 的主要目标定义为：为研究领域提供概览、识别研究数量与类型、观察时间趋势、识别发表论坛，并用这些信息暴露研究空白。

对 Paper2 来说，这篇论文是“先构造领域地图，再决定是否需要深度证据合成”的方法学母文。它直接支持导师讨论中的判断：SLR / SMS 不是机械整理，真正关键是由研究者设定 scope 与维度，再用论文阅读持续修正维度模式。

### 2.2 systematic mapping 流程

作者给出五步流程：

1. 定义研究问题 / 研究范围。
2. 检索 primary studies。
3. 按纳排标准筛选相关论文。
4. 对摘要做 keywording，形成分类方案。
5. 抽取数据并映射成 systematic map。

其中对 A1 最关键的是 §2.4--§2.5：分类方案不是预先一次性冻结，而是在读摘要、聚类关键词、排序论文时形成；如果摘要质量不足，可继续看引言或结论；在数据抽取过程中还可以新增、合并或拆分类别。作者还要求在抽取表中记录每篇论文为什么被放入某个类别的短理由，这与 Paper2 的字段级证据链高度一致。

### 2.3 搜索与纳排

本文对搜索与纳排的启发主要是“广覆盖优先于过早深挖”。作者指出，如果目标是 mapping，则搜索串不宜被特定实验设计或特定 outcome 过度限制，否则容易导致地图不完整。纳排标准要由 RQ 驱动，例如排除只在摘要开头泛泛提到关键词、但正文贡献并不相关的论文。

这对 A1/A2a 的含义是：构建综述之综述文库时，不能只收高等级、方法最完整的 SLR；还要保留 SMS、guideline、roadmap、失败路径和边界样本，用来校准字段取值空间和降级规则。

### 2.4 分类维度与字段模式

本文最可迁移的是三类 facet：

1. **主题 facet**：按领域对象划分，例如 variability 的不同子主题。
2. **贡献 facet**：按论文贡献形态划分，例如 process、method、model、tool。
3. **研究类型 facet**：采用 Wieringa 等提出的研究类型，如 validation research、evaluation research、solution proposal、philosophical paper、opinion paper、experience paper。

这说明 Paper2 后续的维度模式应是树状 / 分层的，而不是只列一张扁平字段表。一个目标主题可以有 topic axis、artifact axis、method axis、research-type axis、evaluation axis；其中部分轴来自领域，部分轴来自通用 SE research methodology。

### 2.5 证据呈现与统计分析

本文强调 systematic map 的分析重心是类别频数和类别交叉。作者使用 summary statistics、frequency table 和 bubble plot 展示论文在不同 facet 组合下的分布。bubble plot 的价值在于同时展示多个 facet 的交叉覆盖，让研究空白以“某类主题 / 研究类型组合论文很少”的方式显现。

这对 Paper2 的启发是：统计分析不等于最终 research finding。统计分析先产生 coverage / density / gap / imbalance 这类观察；随后才由研究者判断这些观察是否构成可写入论文的发现、是否需要反证、是否只适用于某一 scope。

### 2.6 map 与 review 的互补边界

作者比较 systematic maps 和 systematic reviews 后指出，二者目标不同：mapping 更关注分类、主题覆盖和发表论坛；review 更关注证据状态、方法效果和更深入的叙述解释。两者都可以识别研究空白，但空白类型不同：map 看到的是类别覆盖不足，review 看到的是证据不足或报告不足。

这给 A1/A2a 一个重要边界：`survey_of_surveys/` 中的 SMS / guideline 可以为维度模式、统计观察和可视化方式提供先验，但不能替代针对目标主题的深度证据审查。

### 2.7 效度与限制

本文没有独立的传统 threats 章节，但在比较和 guideline 讨论中反复提到：摘要可能不足以支持分类；术语使用不稳定；过窄纳排会损害 breadth；过细分类会放大判断错误；mapping 通常不做与 systematic review 同等深度的质量评价。作者提出的缓解方式包括自适应阅读深度、使用较高层级分类、保留 rationale、必要时查看引言或结论。

这些都适合转化为 Paper2 的证据等级规则：题摘级只能候选；全文文本级才可采纳字段；图表级数值要回原文核对；每个字段都要有 source anchor 和裁决记录。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 主要面向 overview、topic coverage、publication trend、venue/forum、research type，而非 effect size。 | `paper_content.txt` §2.1、Table 1。 | 可迁移为 A2a 的 mapping 型 RQ 模板。 | 不适合直接回答技术有效性或 causal outcome。 |
| dimension pattern | 三个核心 facet：topic、contribution、research type；分类方案通过 keywording 从论文中演化。 | §2.4、Figure 2、Table 3。 | 高度可迁移到 researcher-defined meta-model 的字段树。 | 具体 topic facet 来自 product-line variability 示例，不能直接迁移到 LLM4STM。 |
| finding pattern | 通过类别频数和交叉覆盖识别研究空白，并提出 map 与 review 互补使用的建议。 | §2.5、§3.2、§4、§5。 | 可迁移为“统计观察 → 缺口解释 → 后续 review 决策”的 finding heuristic。 | finding 属方法学层，不是目标领域事实。 |
| evidence presentation pattern | extraction table + short rationale + category frequency + bubble plot / table。 | §2.5、Figure 3、Table 5。 | 可迁移为字段级证据表和 coverage dashboard。 | 图表布局和气泡位置需 PDF 视觉核对。 |
| validity / threat pattern | 主要威胁是摘要信息不足、术语混乱、搜索/纳排过窄、分类误判、depth/breadth trade-off。 | §3.2、§4。 | 可迁移为 A2a 的分类效度与证据等级说明。 | 本文没有完整独立 threats checklist。 |
| report structure pattern | 结构为背景 / 方法流程 / 比较分析 / guideline / 结论，适合作为方法学综述写作模板。 | 章节 §1--§5。 | 可迁移到 survey-of-surveys 方法章节和 pattern library 文档。 | 后续 Paper2 还需加入人机协同、审计制品链和研究者裁决。 |

## 4. A1-M0--M6 元维度贡献

| A1-M 脚手架元维度 | 本文可贡献的模式先验 | 可迁移锚点 | 风险控制 |
|---|---|---|---|
| A1-M0 研究意图与综述元模型 | 定义 systematic map 的目标、范围、产物和与 systematic review 的差异。 | 先由研究者设定主题范围与 mapping / review 类型。 | 不把 map 的 breadth 误写成 review 的 evidence strength。 |
| A1-M1 语料收集与纳排 | 搜索串、数据库 / 手工论坛、纳排标准都由 RQ 驱动；过窄 outcome 会破坏地图完整性。 | 检索计划应记录 scope、forum、数据库、排除理由和失败路径。 | 搜索范围和纳排宽度需与目标论文贡献一致。 |
| A1-M2 研究对象与主题语义 | topic facet 展示如何把领域对象组织为主题轴。 | 可迁移为 LLM4STM / LLM4modeling 的对象、工件、任务、输出谱系等字段树。 | 示例 topic 不能跨领域照搬。 |
| A1-M3 方法 / 技术 / 干预 | contribution facet 与 research type facet 展示论文方法形态分类。 | 可迁移为方法类型、工具、agent 角色、human-in-the-loop、研究类型字段。 | Wieringa 分类需结合现代 LLM/agent 研究扩展。 |
| A1-M4 评价、证据与复现资产 | extraction table、short rationale、frequency table、bubble plot 都是字段证据资产。 | Paper2 字段值必须带 rationale / source anchor / schema version。 | 本文不要求公开复制包，不能直接支撑 artifact completeness。 |
| A1-M5 统计分析就绪 | 类别频数、交叉覆盖、趋势和 bubble plot 可直接支持描述性统计。 | 可迁移为 coverage matrix、cross-tab、分母固定和 missing-value 语义。 | 不支持 effect-size meta-analysis。 |
| A1-M6 research finding 形成与裁决 | 从覆盖缺口形成 future review / guideline 建议，强调 map 与 review 互补。 | 可迁移为候选 finding ledger 的“覆盖缺口 / 后续深读”启发式。 | 最终领域发现仍需研究者裁决和反证检查。 |

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

```text
mapping_study_pattern
├── research_scope
│   ├── overview_goal
│   ├── time_trend_goal
│   ├── venue_forum_goal
│   └── gap_identification_goal
├── search_and_selection
│   ├── database_search
│   ├── manual_forum_search
│   ├── rq_driven_search_terms
│   ├── inclusion_criteria
│   └── exclusion_criteria
├── classification_scheme
│   ├── topic_facet
│   ├── contribution_facet
│   ├── research_type_facet
│   ├── keywording_source
│   └── evolve_merge_split_record
├── extraction_evidence
│   ├── paper_to_category_table
│   ├── short_rationale
│   ├── category_frequency
│   └── cross_facet_frequency
├── visualization
│   ├── frequency_table
│   ├── summary_statistics
│   └── bubble_plot
└── finding_boundary
    ├── coverage_gap
    ├── publication_forum_gap
    ├── map_vs_review_boundary
    └── next_review_recommendation
```

## 6. 对 Paper2 的启发与风险

### 6.1 启发

1. **维度模式必须允许演化**：keywording 和后续分类更新说明字段不是一次写死的，而是要有版本、合并、拆分和回填。
2. **字段值要有短理由**：作者要求每篇论文归类时给 rationale；Paper2 应把这个升级为 source span + rationale + confidence。
3. **统计分析适合先做 coverage**：map 的核心是频数和交叉覆盖，适合让研究者快速看出哪里值得深读。
4. **map 与 review 应分工**：A1/A2b 的 survey-of-surveys 可以先提供模式地图，A4/A5 目标主题试运行再做深度证据和 finding 裁决。
5. **分类效度是核心风险**：LLM/agent 自动抽字段时，最危险的不是少写摘要，而是把论文放错类别且没有证据链。

### 6.2 风险

1. 该文的图表信息较多，`paper_content.txt` 难以还原 Figure 1--3 的布局；正式引用图形模式前需视觉核对。
2. 该文的统计主要是描述性覆盖，不应被写成效果评估或因果证据。
3. 2008 年的研究类型分类需要用现代 LLM/agent 论文重新扩展，否则可能低估工具 / 系统 / agentic workflow 的类别。
4. 该文没有把开放制品作为强制字段；Paper2 不能因此放松 run record、原文 span、schema revision log 等审计要求。

## 7. 待复核

1. A2a 若要精确引用 mapping process 图，需视觉核对 Figure 1（p.2）。
2. A2a 若要复用 keywording 流程，需视觉核对 Figure 2（p.4）。
3. A2a 若要复用 bubble plot 模式，需视觉核对 Figure 3（p.5）。
4. Table 3 的 Wieringa research type 与 Table 5 的 review characteristics 若用于正式字段定义，需核对跨列表格排版。
5. `file` 与 `pdfinfo` 页数显示不一致；当前以 `pdfinfo` 和 `paper_content.txt` 的 10 页为准。

## 维度树复原

### 一句话结论

本文的维度树主类型为“方法流程树”，辅助类型为“topic-independent taxonomy 示例树”。不进入主统计池：方法论文 / guideline-like seed；其内部频数和 map/review 对照只用于方法学描述性统计，不进入普通领域统计合成池；仅作 schema_seed。 [clm-petersen-2008-systematic-mapping-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-petersen-2008-systematic-mapping-source-schema-candidates]

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-petersen-2008-systematic-mapping-root] | Systematic Mapping Studies in Software Engineering 的研究目标 / RQ / 贡献声明 | roadmap action / guideline item / schema seed | [dim-petersen-2008-systematic-mapping-b1] mapping planning；[dim-petersen-2008-systematic-mapping-b2] keywording；[dim-petersen-2008-systematic-mapping-b3] classification scheme；[dim-petersen-2008-systematic-mapping-b4] map visualization；[dim-petersen-2008-systematic-mapping-b5] research gap identification | [ev-petersen-2008-systematic-mapping-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-petersen-2008-systematic-mapping-root] Systematic Mapping Studies in Software Engineering
├── [dim-petersen-2008-systematic-mapping-b1] mapping planning
│   └── [leaf-petersen-2008-systematic-mapping-scope] 研究范围与单位对象
├── [dim-petersen-2008-systematic-mapping-b2] keywording
│   └── [leaf-petersen-2008-systematic-mapping-corpus] 语料与纳排链条
├── [dim-petersen-2008-systematic-mapping-b3] classification scheme
│   └── [leaf-petersen-2008-systematic-mapping-taxonomy] 主题与维度分类
├── [dim-petersen-2008-systematic-mapping-b4] map visualization
│   └── [leaf-petersen-2008-systematic-mapping-method] 方法 / 技术 / 干预分类
└── [dim-petersen-2008-systematic-mapping-b5] research gap identification
    └── [leaf-petersen-2008-systematic-mapping-evidence] 评价、证据与复现资产
    └── [leaf-petersen-2008-systematic-mapping-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-petersen-2008-systematic-mapping-scope] | 研究范围与单位对象 | [dim-petersen-2008-systematic-mapping-b1] | 定义 SMS 方法学 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-scope] |
| [leaf-petersen-2008-systematic-mapping-corpus] | 语料与纳排链条 | [dim-petersen-2008-systematic-mapping-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-corpus] |
| [leaf-petersen-2008-systematic-mapping-taxonomy] | 主题与维度分类 | [dim-petersen-2008-systematic-mapping-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-taxonomy] |
| [leaf-petersen-2008-systematic-mapping-method] | 方法 / 技术 / 干预分类 | [dim-petersen-2008-systematic-mapping-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-method] |
| [leaf-petersen-2008-systematic-mapping-evidence] | 评价、证据与复现资产 | [dim-petersen-2008-systematic-mapping-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-evidence] |
| [leaf-petersen-2008-systematic-mapping-finding] | 统计观察与候选发现 | [dim-petersen-2008-systematic-mapping-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-petersen-2008-systematic-mapping-leaf-finding] |

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-petersen-2008-systematic-mapping-orig-mapping-planning] | [dim-petersen-2008-systematic-mapping-b1] | 映射规划字段 | 目标、RQ、范围、检索策略、纳排和分类准备。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-petersen-2008-systematic-mapping-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-petersen-2008-systematic-mapping-orig-keywording] | [dim-petersen-2008-systematic-mapping-b2] | 关键词化字段 | abstract keywording、主题提取、类别合并和分类 scheme 构造。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-petersen-2008-systematic-mapping-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-petersen-2008-systematic-mapping-orig-classification-scheme] | [dim-petersen-2008-systematic-mapping-b3] | 分类方案字段 | research type、contribution type、topic facet、application facet 等分类维度。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-petersen-2008-systematic-mapping-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-petersen-2008-systematic-mapping-orig-map-visualization] | [dim-petersen-2008-systematic-mapping-b4] | 映射可视化字段 | bubble plot、频次表、二维 map 和空白区域识别。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-petersen-2008-systematic-mapping-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-petersen-2008-systematic-mapping-orig-gap-identification] | [dim-petersen-2008-systematic-mapping-b5] | 研究空白字段 | 未覆盖 topic、薄弱组合、后续研究方向和 threat。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-petersen-2008-systematic-mapping-002, EV-petersen-2008-systematic-mapping-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/petersen-2008-systematic-mapping__codex.md)、[claude](../../audits/a1dt-19x3/results/petersen-2008-systematic-mapping__claude.md)、[deepseek](../../audits/a1dt-19x3/results/petersen-2008-systematic-mapping__deepseek.md)。 [clm-petersen-2008-systematic-mapping-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-petersen-2008-systematic-mapping-orig-planning] | SMS 计划 | objective、RQ、scope、search、inclusion/exclusion | SMS 方法 seed | 方法论文不进主统计池 | 核对 process 描述 |
| [dim-petersen-2008-systematic-mapping-orig-keywording] | abstract keywording | keyword extraction、merge/split categories、classification scheme generation | dimension construction seed | keywording 人工性需记录 | 核对 §keywording |
| [dim-petersen-2008-systematic-mapping-orig-research-type] | Wieringa 研究类型 | validation、evaluation、solution proposal、philosophical、opinion、experience | 封闭枚举 seed | 类别定义需引用原文 | 核对 research type 表 |
| [dim-petersen-2008-systematic-mapping-orig-contribution-type] | 贡献类型 | method、tool、model、metric、process 等贡献类别 | contribution taxonomy seed | 与 research type 区分 | 核对 contribution type 表 |
| [dim-petersen-2008-systematic-mapping-orig-visualization] | 地图可视化 | bubble plot、frequency table、2D map、topic facet × research type | statistics-ready schema seed | 空格子也是 gap | 核对 map visualization |
| [dim-petersen-2008-systematic-mapping-orig-map-vs-review] | mapping 与 review 比较 | Table 5 比较维度、breadth/depth、aggregation、outcome | 方法边界 seed | 不把 SMS 当 SLR | 核对 Table 5 |
| [dim-petersen-2008-systematic-mapping-orig-gap] | gap identification | 空白/低密度 cell、future research、classification imbalance | candidate finding heuristic | 需要研究者裁决 | 核对 discussion |

#### 三路审计综合返修结论

| 审计共同问题 | 本轮返修动作 | 剩余风险 |
|---|---|---|
| 原先主树过度依赖六个通用接口叶子，容易把跨论文投影误读成原文 schema。 | 将原文 RQ、抽取字段、分类项、质量 rubric、关系边、统计表或 roadmap action 抬升为上表主干，并把通用接口降级为后文投影。 | 上表仍是 `schema_seed`，需 A2a 精确核对页码、表号、图号和附录。 |
| 原文显式取值空间未完全进入叶子层。 | 在“叶子 / 取值空间种子”中列出封闭枚举、层级枚举、数值分母、关系值或自由文本边界。 | 取值空间是否封闭、是否饱和、是否可统计，需要 A2a 逐项判定。 |
| 统计观察、候选发现和最终 finding 容易混层。 | 统计用途列显式保留 `schema_seed`、候选 finding 和不得进入当前 SUMMARY 定量统计的边界。 | final research finding 仍必须等跨论文证据、反证和研究者裁决。 |

#### 审计返修口径

- 本节吸收 `codex`、`claude`、`deepseek` 三路全文审计的共同结论：原文 schema 主树必须优先于跨论文通用接口层；通用接口只做投影，不再冒充原文叶子全集。
- 本节只完成 A1-DT 结构化返修；凡未补齐精确页码、表号、图号或 supplementary 定位的节点均保持 `schema_seed` / `not_verified`，并作为 A2a 精核入口。
- 若三路审计之间存在细节差异，后续 A2a 以原文 PDF、`paper_content.txt`、附录和复现实验包为准，并在 A.3 中新增替代结论或废弃旧结论。
#### 通用接口投影

下表只用于把原文 schema 主树投影到跨论文统一接口，不能替代上表成为原文事实源。

| 通用接口 | 在本文中的投影对象 | 使用边界 |
|---|---|---|
| 研究范围与单位对象 | `mapping planning` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
| 语料与纳排链条 | 与检索、纳排、样本分母、方法流程相关的原文主干。 | 无系统检索的 roadmap / vision 需写不适用。 |
| 主题与维度分类 | 原文 taxonomy、classification schema、concept model 或 roadmap action 分类。 | 必须保留原文取值空间，不得压成泛词。 |
| 方法 / 技术 / 干预分类 | 原文 method / tool / intervention / agent role / guideline stage。 | 方法学 guideline 不得误写成目标领域方法效果。 |
| 评价、证据与复现资产 | 原文 quality、metric、artifact、replication、validity、evidence table。 | 弱证据或未核验链接不得进入统计。 |
| 统计观察与候选发现 | 原文 result / discussion / gap / recommendation / action point。 | 只能作 candidate finding，需研究者裁决。 |

#### 返修后仍需 A2a 精核

1. 将上表每个原文主干拆成更细叶子，并为每个叶子补具体页码、表号 / 图号、段落或附录定位。
2. 核对取值空间是否是原文封闭枚举、层级枚举、数值 / 分母、关系值，还是只能自由文本。
3. 若三路审计意见冲突，以原文证据为准，并在 A.3 新增替代结论或废弃旧结论。

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-petersen-2008-systematic-mapping-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否 | 识别可迁移的维度模式类型 | 不进入主统计池：方法论文 / guideline-like seed；其内部频数和 map/review 对照只用于方法学描述性统计，不进入普通领域统计合成池；仅作 schema_seed。 |
| [leaf-petersen-2008-systematic-mapping-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | not_applicable | 否 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-petersen-2008-systematic-mapping-finding] | 候选发现台账，不直接作为 final finding | discussion / conclusion / roadmap action | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-petersen-2008-systematic-mapping-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | SMS 方法学 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-petersen-2008-systematic-mapping-transfer] |
| [leaf-petersen-2008-systematic-mapping-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-petersen-2008-systematic-mapping-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-petersen-2008-systematic-mapping-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-petersen-2008-systematic-mapping-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-petersen-2008-systematic-mapping-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-petersen-2008-systematic-mapping-001 | [ev-petersen-2008-systematic-mapping-root] | [src-petersen-2008-systematic-mapping-text], [src-petersen-2008-systematic-mapping-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-petersen-2008-systematic-mapping-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-petersen-2008-systematic-mapping-002 | [ev-petersen-2008-systematic-mapping-taxonomy] | [src-petersen-2008-systematic-mapping-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-petersen-2008-systematic-mapping-b1], [dim-petersen-2008-systematic-mapping-b2], [dim-petersen-2008-systematic-mapping-b3], [dim-petersen-2008-systematic-mapping-b4], [dim-petersen-2008-systematic-mapping-b5], [leaf-petersen-2008-systematic-mapping-taxonomy], [leaf-petersen-2008-systematic-mapping-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-petersen-2008-systematic-mapping-003 | [ev-petersen-2008-systematic-mapping-stat] | [src-petersen-2008-systematic-mapping-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | author_claim | not_verified | [leaf-petersen-2008-systematic-mapping-evidence], [leaf-petersen-2008-systematic-mapping-finding], [leaf-petersen-2008-systematic-mapping-orig-mapping-planning], [leaf-petersen-2008-systematic-mapping-orig-keywording], [leaf-petersen-2008-systematic-mapping-orig-classification-scheme], [leaf-petersen-2008-systematic-mapping-orig-map-visualization], [leaf-petersen-2008-systematic-mapping-orig-gap-identification] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
| EV-petersen-2008-systematic-mapping-004 | [ev-petersen-2008-systematic-mapping-risk] | [src-petersen-2008-systematic-mapping-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-petersen-2008-systematic-mapping-root], [leaf-petersen-2008-systematic-mapping-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-petersen-2008-systematic-mapping-tree-type] | A1DT-petersen-2008-systematic-mapping-C01 | 本文的维度树主类型为“方法流程树”，辅助类型为“topic-independent taxonomy 示例树”。不进入主统计池：方法论文 / guideline-like seed；其内部频数和 map/review 对照只用于方法学描述性统计，不进入普通领域统计合成池；仅作 schema_seed。 [clm-petersen-2008-systematic-mapping-tree-type] | tree_type | [dim-petersen-2008-systematic-mapping-root] | EV-petersen-2008-systematic-mapping-001, EV-petersen-2008-systematic-mapping-004 | 树型判断仅限本文，不代表所有 SMS 方法学 综述。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-scope] | A1DT-petersen-2008-systematic-mapping-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-scope] | EV-petersen-2008-systematic-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-corpus] | A1DT-petersen-2008-systematic-mapping-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-corpus] | EV-petersen-2008-systematic-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-taxonomy] | A1DT-petersen-2008-systematic-mapping-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-taxonomy] | EV-petersen-2008-systematic-mapping-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-method] | A1DT-petersen-2008-systematic-mapping-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-method] | EV-petersen-2008-systematic-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-evidence] | A1DT-petersen-2008-systematic-mapping-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-evidence] | EV-petersen-2008-systematic-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-leaf-finding] | A1DT-petersen-2008-systematic-mapping-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-petersen-2008-systematic-mapping-finding] | EV-petersen-2008-systematic-mapping-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-transfer] | A1DT-petersen-2008-systematic-mapping-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-petersen-2008-systematic-mapping-root] | EV-petersen-2008-systematic-mapping-002, EV-petersen-2008-systematic-mapping-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-finding-boundary] | A1DT-petersen-2008-systematic-mapping-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-petersen-2008-systematic-mapping-finding] | EV-petersen-2008-systematic-mapping-003, EV-petersen-2008-systematic-mapping-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |

| [clm-petersen-2008-systematic-mapping-source-schema-candidates] | A1DT-petersen-2008-systematic-mapping-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-petersen-2008-systematic-mapping-orig-mapping-planning], [leaf-petersen-2008-systematic-mapping-orig-keywording], [leaf-petersen-2008-systematic-mapping-orig-classification-scheme], [leaf-petersen-2008-systematic-mapping-orig-map-visualization], [leaf-petersen-2008-systematic-mapping-orig-gap-identification] | EV-petersen-2008-systematic-mapping-002, EV-petersen-2008-systematic-mapping-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-petersen-2008-systematic-mapping-a1dt-19x3-repair] | A1DT-petersen-2008-systematic-mapping-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-petersen-2008-systematic-mapping-root] | EV-petersen-2008-systematic-mapping-002, EV-petersen-2008-systematic-mapping-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-petersen-2008-systematic-mapping-structure-check] | [dim-petersen-2008-systematic-mapping-root], A1DT-petersen-2008-systematic-mapping-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-petersen-2008-systematic-mapping-visual-check] | EV-petersen-2008-systematic-mapping-002, EV-petersen-2008-systematic-mapping-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
