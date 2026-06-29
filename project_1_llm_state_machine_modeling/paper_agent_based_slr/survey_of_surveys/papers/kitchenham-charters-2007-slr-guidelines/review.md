# Guidelines for performing Systematic Literature Reviews in Software Engineering

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Guidelines for performing Systematic Literature Reviews in Software Engineering |
| 年份 | 2007 |
| 类型 | 方法学 guideline / SLR 指南 |
| 出版形态 | 技术报告 |
| 期刊/会议/预印本 | [EBSE-2007-01](https://legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | 非 CCF venue；技术报告 |
| 来源等级 | 方法学基准；非 CCF 论文；技术报告 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | SLR guideline；同时定义 mapping study 与 tertiary review |
| SE 子领域 | 软件工程证据综合方法学 |
| A1 角色 | 提供 PR-A1 的基础术语、流程阶段、研究问题、protocol、搜索、选择、质量评价、数据抽取、数据综合与报告结构先验。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 暴露“guideline 类文献没有普通研究结果 RQ 表”的差异；已在 schema 中使用 `综述 / 指南类型` 与 `不适用` 缺失值语义处理。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 研究问题是 SLR 最重要的 protocol 元素；可按 population/intervention/comparison/outcome/context 等结构化。 | `paper_content.txt` Page 2--3 目录列出 §5.3 Research Questions；Page 12 附近说明 protocol 应包含 research questions。 | 可迁移到 Paper2 的“研究者定义综述元模型”和维度模式初始化。 | 这是 guideline，不代表任一 SE 子领域的真实 RQ 分布。 |
| dimension pattern | SLR protocol 至少需要 review need、research questions、search strategy、study selection、quality assessment、data extraction、data synthesis、reporting。 | `paper_content.txt` Page 2--3 目录列出 §5--§7；Page 30 附近讨论 data extraction forms。 | 可作为 `pattern-field-schema.md` 的阶段字段候选。 | 只能作为流程字段先验，不能直接冻结目标主题字段树。 |
| finding pattern | guideline 本身不生成领域 finding；它提供流程规范与质量判据。 | `paper_content.txt` Page 2--3 目录；Page 40 附近 reporting/evaluating review reports。 | 对 Paper2 的 finding 启发式不可直接迁移，只能迁移报告与评价结构。 | guideline 不产生领域 finding，只迁移 finding 报告约束。 |
| evidence presentation pattern | 强调 documenting search、selection criteria、quality checklists、data extraction forms、synthesis 和 reporting。 | `paper_content.txt` Page 2--3 目录；Page 16 附近 documenting search；Page 29--34 data extraction。 | 高度可迁移到审计制品链。 | 规范建议需由后续真实论文样本验证。 |
| validity / threat pattern | 明确讨论 inclusion decision reliability、publication bias、quality assessment、sensitivity analysis。 | `paper_content.txt` Page 2--3 目录；Page 20 reliability；Page 38--39 sensitivity/publication bias。 | 可迁移为后续 A5 风险指标。 | 可迁移为风险清单，但具体权重需按 pilot 数据校准。 |
| report structure pattern | reporting review 部分要求 dissemination strategy、main report formatting、review report evaluation。 | `paper_content.txt` Page 3 目录 §7。 | 可迁移为 Paper2 输出材料结构。 | 报告建议偏 guideline，不等同于 paper2 最终论文结构。 |

## 3. 对 PR-A1 schema 的启发

1. `综述 / 指南类型` 必须允许 `guideline`，否则该文无法自然归类。
2. `finding pattern` 对 guideline 可能为“不适用”，不能误记为缺失或低质量。
3. `evidence presentation pattern` 应覆盖 protocol、表单、checklist 和报告结构，而不仅是论文结果表。
4. 后续 A2a 若纳入更多 guideline，需要单独区分“规范性文献”和“经验性 tertiary study”。

## 4. 待复核

- PDF 表格和 checklists 尚未逐页人工核对。
- 技术报告不是 peer-reviewed venue，正式引用时需说明来源性质。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 用 review need、research question、population/intervention/outcome/context 等要素定义系统综述协议。 | 可作为元模型初始化规范；不能直接代表任一 SE 子领域的主题结构。 |
| A1-M1 语料收集与纳排 | 提供 search strategy、study selection、quality assessment 和 data extraction 的流程字段。 | 可作为检索/纳排台账字段模板；具体数据库和检索式需由目标主题重建。 |
| A1-M2 研究对象与主题语义 | 仅提供通用 PICO / scope 组织方式，不提供具体 SE 子领域 taxonomy。 | 可候选，不作为已采纳领域语义字段。 |
| A1-M3 方法 / 技术 / 干预 | 指南强调 intervention / comparison 等变量，但不是技术综述样本。 | 对方法分类只提供形式约束，不提供具体取值空间。 |
| A1-M4 评价、证据与复现资产 | 强调质量评价、数据抽取表、搜索记录、报告结构和 sensitivity analysis。 | 可迁移到 Paper2 的 evidence anchor / run record / extraction-form 要求。 |
| A1-M5 统计分析就绪 | 说明 data synthesis 可叙述、定量或混合，并要求记录分母与合成方式。 | 可作为统计分析协议的最低规则，不提供现代字段树。 |
| A1-M6 research finding 形成与裁决 | guideline 本身不生成领域 finding，只提供报告和评价约束。 | 只作为 finding 报告规范；不进入目标领域 finding。 |

## 维度树复原

### 一句话结论

本文的维度树主类型为“方法流程树”，辅助类型为“质量 / 效度 guideline 树”。不进入主统计池：方法学 guideline；不是执行后的 SLR/SMS/tertiary 统计样本；仅作 schema_seed。 [clm-kitchenham-charters-2007-slr-guidelines-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-kitchenham-charters-2007-slr-guidelines-root] | Guidelines for performing Systematic Literature Reviews in Software Engineering 的研究目标 / RQ / 贡献声明 | roadmap action / guideline item / schema seed | [dim-kitchenham-charters-2007-slr-guidelines-b1] review protocol；[dim-kitchenham-charters-2007-slr-guidelines-b2] search and selection；[dim-kitchenham-charters-2007-slr-guidelines-b3] data extraction；[dim-kitchenham-charters-2007-slr-guidelines-b4] quality assessment；[dim-kitchenham-charters-2007-slr-guidelines-b5] reporting / threats | [ev-kitchenham-charters-2007-slr-guidelines-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-kitchenham-charters-2007-slr-guidelines-root] Guidelines for performing Systematic Literature Reviews in Software Engineering
├── [dim-kitchenham-charters-2007-slr-guidelines-b1] review protocol
│   └── [leaf-kitchenham-charters-2007-slr-guidelines-scope] 研究范围与单位对象
├── [dim-kitchenham-charters-2007-slr-guidelines-b2] search and selection
│   └── [leaf-kitchenham-charters-2007-slr-guidelines-corpus] 语料与纳排链条
├── [dim-kitchenham-charters-2007-slr-guidelines-b3] data extraction
│   └── [leaf-kitchenham-charters-2007-slr-guidelines-taxonomy] 主题与维度分类
├── [dim-kitchenham-charters-2007-slr-guidelines-b4] quality assessment
│   └── [leaf-kitchenham-charters-2007-slr-guidelines-method] 方法 / 技术 / 干预分类
└── [dim-kitchenham-charters-2007-slr-guidelines-b5] reporting / threats
    └── [leaf-kitchenham-charters-2007-slr-guidelines-evidence] 评价、证据与复现资产
    └── [leaf-kitchenham-charters-2007-slr-guidelines-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-kitchenham-charters-2007-slr-guidelines-scope] | 研究范围与单位对象 | [dim-kitchenham-charters-2007-slr-guidelines-b1] | 定义 EBSE 方法学 / SLR guideline 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-scope] |
| [leaf-kitchenham-charters-2007-slr-guidelines-corpus] | 语料与纳排链条 | [dim-kitchenham-charters-2007-slr-guidelines-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-corpus] |
| [leaf-kitchenham-charters-2007-slr-guidelines-taxonomy] | 主题与维度分类 | [dim-kitchenham-charters-2007-slr-guidelines-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-taxonomy] |
| [leaf-kitchenham-charters-2007-slr-guidelines-method] | 方法 / 技术 / 干预分类 | [dim-kitchenham-charters-2007-slr-guidelines-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-method] |
| [leaf-kitchenham-charters-2007-slr-guidelines-evidence] | 评价、证据与复现资产 | [dim-kitchenham-charters-2007-slr-guidelines-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-evidence] |
| [leaf-kitchenham-charters-2007-slr-guidelines-finding] | 统计观察与候选发现 | [dim-kitchenham-charters-2007-slr-guidelines-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-kitchenham-charters-2007-slr-guidelines-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-kitchenham-charters-2007-slr-guidelines-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否 | 识别可迁移的维度模式类型 | 不进入主统计池：方法学 guideline；不是执行后的 SLR/SMS/tertiary 统计样本；仅作 schema_seed。 |
| [leaf-kitchenham-charters-2007-slr-guidelines-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | not_applicable | 否 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-kitchenham-charters-2007-slr-guidelines-finding] | 候选发现台账，不直接作为 final finding | discussion / conclusion / roadmap action | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-kitchenham-charters-2007-slr-guidelines-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | EBSE 方法学 / SLR guideline 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-kitchenham-charters-2007-slr-guidelines-transfer] |
| [leaf-kitchenham-charters-2007-slr-guidelines-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-kitchenham-charters-2007-slr-guidelines-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-kitchenham-charters-2007-slr-guidelines-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-kitchenham-charters-2007-slr-guidelines-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-kitchenham-charters-2007-slr-guidelines-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-kitchenham-charters-2007-slr-guidelines-001 | [ev-kitchenham-charters-2007-slr-guidelines-root] | [src-kitchenham-charters-2007-slr-guidelines-text], [src-kitchenham-charters-2007-slr-guidelines-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-kitchenham-charters-2007-slr-guidelines-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-kitchenham-charters-2007-slr-guidelines-002 | [ev-kitchenham-charters-2007-slr-guidelines-taxonomy] | [src-kitchenham-charters-2007-slr-guidelines-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-kitchenham-charters-2007-slr-guidelines-b1], [dim-kitchenham-charters-2007-slr-guidelines-b2], [dim-kitchenham-charters-2007-slr-guidelines-b3], [dim-kitchenham-charters-2007-slr-guidelines-b4], [dim-kitchenham-charters-2007-slr-guidelines-b5], [leaf-kitchenham-charters-2007-slr-guidelines-taxonomy], [leaf-kitchenham-charters-2007-slr-guidelines-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-kitchenham-charters-2007-slr-guidelines-003 | [ev-kitchenham-charters-2007-slr-guidelines-stat] | [src-kitchenham-charters-2007-slr-guidelines-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | author_claim | not_verified | [leaf-kitchenham-charters-2007-slr-guidelines-evidence], [leaf-kitchenham-charters-2007-slr-guidelines-finding] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
| EV-kitchenham-charters-2007-slr-guidelines-004 | [ev-kitchenham-charters-2007-slr-guidelines-risk] | [src-kitchenham-charters-2007-slr-guidelines-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-kitchenham-charters-2007-slr-guidelines-root], [leaf-kitchenham-charters-2007-slr-guidelines-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-kitchenham-charters-2007-slr-guidelines-tree-type] | A1DT-kitchenham-charters-2007-slr-guidelines-C01 | 本文的维度树主类型为“方法流程树”，辅助类型为“质量 / 效度 guideline 树”。不进入主统计池：方法学 guideline；不是执行后的 SLR/SMS/tertiary 统计样本；仅作 schema_seed。 [clm-kitchenham-charters-2007-slr-guidelines-tree-type] | tree_type | [dim-kitchenham-charters-2007-slr-guidelines-root] | EV-kitchenham-charters-2007-slr-guidelines-001, EV-kitchenham-charters-2007-slr-guidelines-004 | 树型判断仅限本文，不代表所有 EBSE 方法学 / SLR guideline 综述。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-scope] | A1DT-kitchenham-charters-2007-slr-guidelines-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-scope] | EV-kitchenham-charters-2007-slr-guidelines-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-corpus] | A1DT-kitchenham-charters-2007-slr-guidelines-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-corpus] | EV-kitchenham-charters-2007-slr-guidelines-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-taxonomy] | A1DT-kitchenham-charters-2007-slr-guidelines-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-taxonomy] | EV-kitchenham-charters-2007-slr-guidelines-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-method] | A1DT-kitchenham-charters-2007-slr-guidelines-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-method] | EV-kitchenham-charters-2007-slr-guidelines-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-evidence] | A1DT-kitchenham-charters-2007-slr-guidelines-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-evidence] | EV-kitchenham-charters-2007-slr-guidelines-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-leaf-finding] | A1DT-kitchenham-charters-2007-slr-guidelines-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-kitchenham-charters-2007-slr-guidelines-finding] | EV-kitchenham-charters-2007-slr-guidelines-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-transfer] | A1DT-kitchenham-charters-2007-slr-guidelines-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-kitchenham-charters-2007-slr-guidelines-root] | EV-kitchenham-charters-2007-slr-guidelines-002, EV-kitchenham-charters-2007-slr-guidelines-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-finding-boundary] | A1DT-kitchenham-charters-2007-slr-guidelines-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-kitchenham-charters-2007-slr-guidelines-finding] | EV-kitchenham-charters-2007-slr-guidelines-003, EV-kitchenham-charters-2007-slr-guidelines-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-kitchenham-charters-2007-slr-guidelines-structure-check] | [dim-kitchenham-charters-2007-slr-guidelines-root], A1DT-kitchenham-charters-2007-slr-guidelines-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-kitchenham-charters-2007-slr-guidelines-visual-check] | EV-kitchenham-charters-2007-slr-guidelines-002, EV-kitchenham-charters-2007-slr-guidelines-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
