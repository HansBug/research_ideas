# Systematic literature reviews in software engineering – A systematic literature review

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic literature reviews in software engineering – A systematic literature review |
| 年份 | 2009 |
| 类型 | tertiary-like SLR / SE SLR 状态综述 |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | 高等级 SE 期刊；Information and Software Technology |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 对 SE SLR 的三级/二级综述；文中自称 review of SLRs / tertiary study |
| SE 子领域 | EBSE / SE 二级研究方法学 |
| A1 角色 | 提供 RQ、搜索范围、纳排、质量评价、数据抽取、数据分析、limitations 都较清晰的 tertiary-study 样例。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 缺口 | 无硬缺口；但 quality score 数值需 原文图表级核对后才能进入正式统计。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | RQ 覆盖活动规模、主题分布、研究者 / 机构、当前研究限制；属于“领域现状 + 局限”组合。 | `paper_content.txt` Page 2 lines around RQ1--RQ4。 | 可迁移到 Paper2 的 research finding：不仅统计数量，还问主题覆盖与限制。 | 早期 EBSE 样本，不能代表近年 SE/LLM4SE 综述 RQ 全貌。 |
| dimension pattern | 抽取范围包括 search venues、纳排标准、quality assessment、data collection、data analysis、deviation from protocol。 | `paper_content.txt` Page 1 contents；Page 2--3 Method。 | 可迁移为 survey-of-surveys review 表字段。 | 字段反映早期 SLR 生态，现代开放科学字段需 A2a 补充。 |
| finding pattern | 从数量、主题、组织、限制和实践影响形成 findings；结论指出主题覆盖有限、部分 SLR 可为实践提供指南。 | `paper_content.txt` Page 1 abstract；Page 7--8 discussion/conclusion。 | 可迁移为“统计观察 → 研究发现”的桥接模板。 | 只作为“统计到发现”的模板，不能迁移具体领域结论。 |
| evidence presentation pattern | 用 manual search 分母、search results、quality evaluation、quality factors 支撑结论。 | `paper_content.txt` Page 1 abstract；Page 3--5 results。 | 可迁移为字段证据与统计表结构。 | 质量评价和搜索分母可迁移，具体指标需现代样本校准。 |
| validity / threat pattern | 单列 limitations of study，包含搜索范围、术语历史和 protocol deviation。 | `paper_content.txt` Page 1 contents；Page 7 limitations。 | 可迁移到 Paper2 的效度威胁章节。 | 早期 threat 口径可能不足以覆盖 LLM 辅助综述风险。 |
| report structure pattern | 标准结构：Introduction → Method → Results → Discussion → Conclusions，并将每个 RQ 映射到 discussion 小节。 | `paper_content.txt` Page 1 contents。 | 高度可迁移。 | 结构可参考，但后续必须加入人机协同与审计制品链部分。 |

## 3. 对 PR-A1 schema 的启发

1. `RQ pattern` 应允许“规模 / 主题 / 主体 / 局限”四类组合，不只允许 PICO 式技术效果问题。
2. `finding pattern` 需要区分统计观察和可行动结论，例如“SLR 数量增加”与“需要更好实践指导”。
3. `evidence presentation pattern` 应要求每个 finding 对应搜索范围、筛选分母、质量评价或 data extraction 字段。
4. `validity pattern` 需要记录 protocol deviation，而不是只列外部效度。

## 4. 待复核

- Table / quality score 数值正式使用前需回原文核对。
- 该文是早期 SE tertiary study；A2a/A2b 需要补近年样本，避免 pattern 过拟合早期 EBSE。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 把 SE SLR 自身作为研究对象，适合作为 tertiary-like scope 样本。 | 可迁移“二次研究的二次研究”元模型。 |
| A1-M1 语料收集与纳排 | 提供早期 SE SLR 的检索、纳排和质量评价过程。 | 可作为历史 baseline；不代表现代检索生态。 |
| A1-M2 研究对象与主题语义 | 提供早期 SE SLR topic / quality / reporting 分类。 | 可迁移分类方式，不迁移领域覆盖结论。 |
| A1-M3 方法 / 技术 / 干预 | 主要是综述方法和主题分类，不是技术干预 taxonomy。 | 对 A1-M3 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 强调 reporting quality、search bias、质量评价等证据呈现。 | 可迁移到 validity / audit 字段。 |
| A1-M5 统计分析就绪 | 可形成 review 数量、主题、质量等统计观察。 | 分母年代久远；需标注历史边界。 |
| A1-M6 research finding 形成与裁决 | 从早期 SE SLR 质量问题形成方法学改进建议。 | 可迁移 finding 写法，不迁移 2009 年状态结论。 |

## 维度树复原

### 一句话结论

本文的维度树主类型为“tertiary 生态统计树”，辅助类型为“质量评价树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-kitchenham-2009-slr-tertiary-tree-type]

旧有“可迁移字段树 / 字段树 / schema 缺口”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-kitchenham-2009-slr-tertiary-root] | Systematic literature reviews in software engineering – A systematic literature  的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-kitchenham-2009-slr-tertiary-b1] 综述范围与研究问题；[dim-kitchenham-2009-slr-tertiary-b2] 语料收集与纳排；[dim-kitchenham-2009-slr-tertiary-b3] 主题 / 对象分类；[dim-kitchenham-2009-slr-tertiary-b4] 方法 / 技术 / 干预；[dim-kitchenham-2009-slr-tertiary-b5] 评价、统计与候选发现 | [ev-kitchenham-2009-slr-tertiary-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-kitchenham-2009-slr-tertiary-root] Systematic literature reviews in software engineering – A systematic literature
├── [dim-kitchenham-2009-slr-tertiary-b1] 综述范围与研究问题
│   └── [leaf-kitchenham-2009-slr-tertiary-scope] 研究范围与单位对象
├── [dim-kitchenham-2009-slr-tertiary-b2] 语料收集与纳排
│   └── [leaf-kitchenham-2009-slr-tertiary-corpus] 语料与纳排链条
├── [dim-kitchenham-2009-slr-tertiary-b3] 主题 / 对象分类
│   └── [leaf-kitchenham-2009-slr-tertiary-taxonomy] 主题与维度分类
├── [dim-kitchenham-2009-slr-tertiary-b4] 方法 / 技术 / 干预
│   └── [leaf-kitchenham-2009-slr-tertiary-method] 方法 / 技术 / 干预分类
└── [dim-kitchenham-2009-slr-tertiary-b5] 评价、统计与候选发现
    └── [leaf-kitchenham-2009-slr-tertiary-evidence] 评价、证据与复现资产
    └── [leaf-kitchenham-2009-slr-tertiary-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-kitchenham-2009-slr-tertiary-scope] | 研究范围与单位对象 | [dim-kitchenham-2009-slr-tertiary-b1] | 定义 EBSE / SE SLR 状态 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-scope] |
| [leaf-kitchenham-2009-slr-tertiary-corpus] | 语料与纳排链条 | [dim-kitchenham-2009-slr-tertiary-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-corpus] |
| [leaf-kitchenham-2009-slr-tertiary-taxonomy] | 主题与维度分类 | [dim-kitchenham-2009-slr-tertiary-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-taxonomy] |
| [leaf-kitchenham-2009-slr-tertiary-method] | 方法 / 技术 / 干预分类 | [dim-kitchenham-2009-slr-tertiary-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-method] |
| [leaf-kitchenham-2009-slr-tertiary-evidence] | 评价、证据与复现资产 | [dim-kitchenham-2009-slr-tertiary-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-evidence] |
| [leaf-kitchenham-2009-slr-tertiary-finding] | 统计观察与候选发现 | [dim-kitchenham-2009-slr-tertiary-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-2009-slr-tertiary-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-kitchenham-2009-slr-tertiary-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 是 | 识别可迁移的维度模式类型 | 可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 |
| [leaf-kitchenham-2009-slr-tertiary-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 是 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-kitchenham-2009-slr-tertiary-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-kitchenham-2009-slr-tertiary-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | EBSE / SE SLR 状态 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-kitchenham-2009-slr-tertiary-transfer] |
| [leaf-kitchenham-2009-slr-tertiary-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-kitchenham-2009-slr-tertiary-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-kitchenham-2009-slr-tertiary-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-kitchenham-2009-slr-tertiary-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-kitchenham-2009-slr-tertiary-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-kitchenham-2009-slr-tertiary-001 | [ev-kitchenham-2009-slr-tertiary-root] | [src-kitchenham-2009-slr-tertiary-text], [src-kitchenham-2009-slr-tertiary-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | strong | [dim-kitchenham-2009-slr-tertiary-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-kitchenham-2009-slr-tertiary-002 | [ev-kitchenham-2009-slr-tertiary-taxonomy] | [src-kitchenham-2009-slr-tertiary-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度。 | taxonomy | medium | [dim-kitchenham-2009-slr-tertiary-b1], [dim-kitchenham-2009-slr-tertiary-b2], [dim-kitchenham-2009-slr-tertiary-b3], [dim-kitchenham-2009-slr-tertiary-b4], [dim-kitchenham-2009-slr-tertiary-b5], [leaf-kitchenham-2009-slr-tertiary-taxonomy], [leaf-kitchenham-2009-slr-tertiary-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-kitchenham-2009-slr-tertiary-003 | [ev-kitchenham-2009-slr-tertiary-stat] | [src-kitchenham-2009-slr-tertiary-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | statistical_result | medium | [leaf-kitchenham-2009-slr-tertiary-evidence], [leaf-kitchenham-2009-slr-tertiary-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-kitchenham-2009-slr-tertiary-004 | [ev-kitchenham-2009-slr-tertiary-risk] | [src-kitchenham-2009-slr-tertiary-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | medium | [dim-kitchenham-2009-slr-tertiary-root], [leaf-kitchenham-2009-slr-tertiary-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-kitchenham-2009-slr-tertiary-tree-type] | A1DT-kitchenham-2009-slr-tertiary-C01 | 本文的维度树主类型为“tertiary 生态统计树”，辅助类型为“质量评价树”。可进入主统计池：有系统检索 / 映射 / tertiary / MLR 证据，可用于 survey-of-surveys 的字段和树型统计。 [clm-kitchenham-2009-slr-tertiary-tree-type] | tree_type | [dim-kitchenham-2009-slr-tertiary-root] | EV-kitchenham-2009-slr-tertiary-001, EV-kitchenham-2009-slr-tertiary-004 | 树型判断仅限本文，不代表所有 EBSE / SE SLR 状态 综述。 | strong | statistical_synthesis | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-scope] | A1DT-kitchenham-2009-slr-tertiary-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-scope] | EV-kitchenham-2009-slr-tertiary-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-corpus] | A1DT-kitchenham-2009-slr-tertiary-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-corpus] | EV-kitchenham-2009-slr-tertiary-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-taxonomy] | A1DT-kitchenham-2009-slr-tertiary-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-taxonomy] | EV-kitchenham-2009-slr-tertiary-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-method] | A1DT-kitchenham-2009-slr-tertiary-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-method] | EV-kitchenham-2009-slr-tertiary-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-evidence] | A1DT-kitchenham-2009-slr-tertiary-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-evidence] | EV-kitchenham-2009-slr-tertiary-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | strong | statistical_synthesis | false | -- |
| [clm-kitchenham-2009-slr-tertiary-leaf-finding] | A1DT-kitchenham-2009-slr-tertiary-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-2009-slr-tertiary-finding] | EV-kitchenham-2009-slr-tertiary-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | medium | schema_seed | false | -- |
| [clm-kitchenham-2009-slr-tertiary-transfer] | A1DT-kitchenham-2009-slr-tertiary-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-kitchenham-2009-slr-tertiary-root] | EV-kitchenham-2009-slr-tertiary-002, EV-kitchenham-2009-slr-tertiary-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | medium | schema_seed | false | -- |
| [clm-kitchenham-2009-slr-tertiary-finding-boundary] | A1DT-kitchenham-2009-slr-tertiary-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-kitchenham-2009-slr-tertiary-finding] | EV-kitchenham-2009-slr-tertiary-003, EV-kitchenham-2009-slr-tertiary-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | medium | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-kitchenham-2009-slr-tertiary-structure-check] | [dim-kitchenham-2009-slr-tertiary-root], A1DT-kitchenham-2009-slr-tertiary-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-kitchenham-2009-slr-tertiary-visual-check] | EV-kitchenham-2009-slr-tertiary-002, EV-kitchenham-2009-slr-tertiary-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
