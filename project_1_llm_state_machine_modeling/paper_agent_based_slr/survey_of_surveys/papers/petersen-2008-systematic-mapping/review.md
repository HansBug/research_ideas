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
| 证据等级 | 全文文本级；图表 / 表格布局待 A2a 人工 PDF 核对。 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf)、DOI: <https://doi.org/10.14236/ewic/EASE2008.8> |
| 综述类型 | SMS 方法论文 / systematic mapping 方法学 seed。 |
| SE 子领域 | 软件工程 systematic mapping 方法学。 |
| A1 角色 | 从失败路径升级为全文级方法学种子：提供 SMS 流程、keywording、三维分类 facet、频数 / bubble plot 呈现、map 与 review 的互补边界。 |
| 是否目标证据池 | 否；只作为 `survey_of_surveys/` 的方法学 schema seed，不作为某个 SE 主题领域事实。 |
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

这些都适合转化为 Paper2 的证据等级规则：题摘级只能候选；全文文本级才可采纳字段；图表级数值要回 PDF 核对；每个字段都要有 source anchor 和裁决记录。

## 3. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
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

## 5. 可迁移字段树 / 维度锚点

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
