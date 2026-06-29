# Machine Learning for Software Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Machine Learning for Software Engineering: A Tertiary Study |
| 年份 | 2023 |
| 类型 | tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [CSUR](https://dl.acm.org/journal/csur) |
| CCF 官方大类 | 待核验（疑似非软件工程大类；官方页 WAF） |
| CCF 官方等级 | 待核验 |
| CCF 复核状态 | 官方待人工复核（WAF）；本地未建 CSUR 条目 |
| 来源等级 | 高等级综述期刊；ACM Computing Surveys；arXiv 开放 PDF；CCF 官方等级暂不写死 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | tertiary study；汇总 83 篇 reviews 与 6117 篇 primary studies |
| SE 子领域 | ML4SE；覆盖软件生命周期多个活动 |
| A1 角色 | 现代高等级 tertiary study 样本，用于压测大规模二次研究汇总、分类体系、research challenges 与 action recommendations。 |
| 是否目标证据池 | 否；只作为脚手架模式先验。 |
| schema 历史观察 | 暴露“挑战 / 行动建议”类 finding pattern；已在 SUMMARY 中作为 A2a 重点候选。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 原文以 ML for SE 的覆盖、分类、质量评估与研究挑战组织三级研究；摘要直接说明 systematically collected、quality-assessed、summarized、categorized 83 reviews。 | `paper_content.txt` Page 1 摘要。 | 可迁移为“覆盖 + 分类 + 质量 + 挑战 / 行动”组合。 | ML4SE 的覆盖/挑战 RQ 可迁移为样式，不迁移具体领域问题。 |
| dimension pattern | 维度包括 SE 生命周期活动、ML 技术、review 质量、primary study 数量、研究挑战和建议行动。 | `paper_content.txt` Page 1 摘要；全文目录与分类章节待 PDF 表格核对。 | 高度可迁移，但字段树较大，A2a 需细分。 | 字段树较大，A2a 需要拆分并验证取值空间。 |
| finding pattern | 发现不仅是分布统计，还提出 ML4SE research challenges/actions，如更多实证验证、工业研究、数据/管线文档化、增量 ML。 | `paper_content.txt` Page 1 摘要。 | 可迁移为 Paper2 的 candidate finding heuristic：统计观察之后要形成行动建议。 | 挑战/行动建议是启发式，不代表目标主题最终 finding。 |
| evidence presentation pattern | 使用 83 reviews / 6117 primary studies 的分母、质量评估、分类表和挑战列表。 | `paper_content.txt` Page 1 摘要；表格待原文核对。 | 可迁移为大规模总账和 pattern-to-source anchor。 | 83 reviews/6117 primary studies 的数值需 PDF 表格核对后才能引用。 |
| validity / threat pattern | 本轮只读题摘和全文开头，threats 章节待进一步定位；当前不能写成已完整核验。 | `paper_content.txt` 全文待 A2a 深读。 | 作为待核验字段，不能强写。 | 本轮未完整定位 threat 章节，不能强写完整核验。 |
| report structure pattern | CSUR 综述结构，含 introduction、method、classification/results、discussion/challenges；具体章节待 A2a 深读。 | `paper_content.txt` 目录提取不完整；需 PDF 目录核对。 | 候选可迁移。 | CSUR 长综述结构适合参考，但 paper2 仍需突出方法贡献。 |

## 3. 对 PR-A1 schema 的启发

1. 新增 `challenge_action_pattern` 作为 `finding_pattern` 的子类型：从统计分布转为研究挑战和行动建议。
2. 大型 tertiary study 需要 `secondary_count`、`primary_count`、`classification_axis` 等字段。
3. 高等级现代样本会暴露 A1 早期 EBSE 文献过旧的问题，A2a 应优先扩展 2020 年后的 SE tertiary/survey。

## 4. 待复核

- 需进一步定位 RQ、threats、classification 表和 challenge 表的页码。
- DOI/最终出版页已记录；正式写作前应核对 ACM 版与 arXiv 版差异。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 把 ML4SE 三级研究定义为“收集、质量评价、汇总、分类 reviews 并追溯 primary studies”。 | 可迁移三级研究的 scope / unit-of-analysis 设计；不能迁移 ML4SE 具体结论。 |
| A1-M1 语料收集与纳排 | 提供 reviews / primary studies 双层分母、质量评价和纳排边界。 | 可作为二次研究语料台账字段候选。 |
| A1-M2 研究对象与主题语义 | 以 SE 生命周期活动、ML technique、研究挑战组织 taxonomy。 | 可候选为“生命周期 + 技术 + 任务”字段树样式。 |
| A1-M3 方法 / 技术 / 干预 | 抽取 ML 方法族与 SE 活动之间的关系。 | 只迁移“方法与任务交叉分类”模式。 |
| A1-M4 评价、证据与复现资产 | 使用质量评价、review / primary-study 数量和分类表支撑结论。 | 正式引用具体数值前需 原文图表核对。 |
| A1-M5 统计分析就绪 | 大规模 tertiary 能形成跨 review / primary-study 的分布与覆盖统计。 | 可作为 A2a 大样本统计字段候选。 |
| A1-M6 research finding 形成与裁决 | 从分布统计进一步形成 challenges 和 action recommendations。 | 可作为 candidate finding heuristic，不作为 Paper2 目标领域 finding。 |

## 维度树复原

### 一句话结论

本文的维度树主类型为“tertiary 主题 / 挑战树”，辅助类型为“action recommendation 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-ml4se-tertiary-study-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-ml4se-tertiary-study-root] | Machine Learning for Software Engineering 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-ml4se-tertiary-study-b1] 综述范围与研究问题；[dim-ml4se-tertiary-study-b2] 语料收集与纳排；[dim-ml4se-tertiary-study-b3] 主题 / 对象分类；[dim-ml4se-tertiary-study-b4] 方法 / 技术 / 干预；[dim-ml4se-tertiary-study-b5] 评价、统计与候选发现 | [ev-ml4se-tertiary-study-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-ml4se-tertiary-study-root] Machine Learning for Software Engineering
├── [dim-ml4se-tertiary-study-b1] 综述范围与研究问题
│   └── [leaf-ml4se-tertiary-study-scope] 研究范围与单位对象
├── [dim-ml4se-tertiary-study-b2] 语料收集与纳排
│   └── [leaf-ml4se-tertiary-study-corpus] 语料与纳排链条
├── [dim-ml4se-tertiary-study-b3] 主题 / 对象分类
│   └── [leaf-ml4se-tertiary-study-taxonomy] 主题与维度分类
├── [dim-ml4se-tertiary-study-b4] 方法 / 技术 / 干预
│   └── [leaf-ml4se-tertiary-study-method] 方法 / 技术 / 干预分类
└── [dim-ml4se-tertiary-study-b5] 评价、统计与候选发现
    └── [leaf-ml4se-tertiary-study-evidence] 评价、证据与复现资产
    └── [leaf-ml4se-tertiary-study-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-ml4se-tertiary-study-scope] | 研究范围与单位对象 | [dim-ml4se-tertiary-study-b1] | 定义 ML4SE 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-scope] |
| [leaf-ml4se-tertiary-study-corpus] | 语料与纳排链条 | [dim-ml4se-tertiary-study-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-corpus] |
| [leaf-ml4se-tertiary-study-taxonomy] | 主题与维度分类 | [dim-ml4se-tertiary-study-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-taxonomy] |
| [leaf-ml4se-tertiary-study-method] | 方法 / 技术 / 干预分类 | [dim-ml4se-tertiary-study-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-method] |
| [leaf-ml4se-tertiary-study-evidence] | 评价、证据与复现资产 | [dim-ml4se-tertiary-study-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-evidence] |
| [leaf-ml4se-tertiary-study-finding] | 统计观察与候选发现 | [dim-ml4se-tertiary-study-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-ml4se-tertiary-study-leaf-finding] |

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-ml4se-tertiary-study-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-ml4se-tertiary-study-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-ml4se-tertiary-study-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-ml4se-tertiary-study-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | ML4SE 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-ml4se-tertiary-study-transfer] |
| [leaf-ml4se-tertiary-study-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-ml4se-tertiary-study-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-ml4se-tertiary-study-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-ml4se-tertiary-study-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-ml4se-tertiary-study-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-ml4se-tertiary-study-001 | [ev-ml4se-tertiary-study-root] | [src-ml4se-tertiary-study-text], [src-ml4se-tertiary-study-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-ml4se-tertiary-study-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-ml4se-tertiary-study-002 | [ev-ml4se-tertiary-study-taxonomy] | [src-ml4se-tertiary-study-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-ml4se-tertiary-study-b1], [dim-ml4se-tertiary-study-b2], [dim-ml4se-tertiary-study-b3], [dim-ml4se-tertiary-study-b4], [dim-ml4se-tertiary-study-b5], [leaf-ml4se-tertiary-study-taxonomy], [leaf-ml4se-tertiary-study-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-ml4se-tertiary-study-003 | [ev-ml4se-tertiary-study-stat] | [src-ml4se-tertiary-study-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-ml4se-tertiary-study-evidence], [leaf-ml4se-tertiary-study-finding] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-ml4se-tertiary-study-004 | [ev-ml4se-tertiary-study-risk] | [src-ml4se-tertiary-study-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-ml4se-tertiary-study-root], [leaf-ml4se-tertiary-study-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-ml4se-tertiary-study-tree-type] | A1DT-ml4se-tertiary-study-C01 | 本文的维度树主类型为“tertiary 主题 / 挑战树”，辅助类型为“action recommendation 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-ml4se-tertiary-study-tree-type] | tree_type | [dim-ml4se-tertiary-study-root] | EV-ml4se-tertiary-study-001, EV-ml4se-tertiary-study-004 | 树型判断仅限本文，不代表所有 ML4SE 综述。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-scope] | A1DT-ml4se-tertiary-study-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-scope] | EV-ml4se-tertiary-study-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-corpus] | A1DT-ml4se-tertiary-study-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-corpus] | EV-ml4se-tertiary-study-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-taxonomy] | A1DT-ml4se-tertiary-study-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-taxonomy] | EV-ml4se-tertiary-study-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-method] | A1DT-ml4se-tertiary-study-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-method] | EV-ml4se-tertiary-study-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-evidence] | A1DT-ml4se-tertiary-study-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-evidence] | EV-ml4se-tertiary-study-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-leaf-finding] | A1DT-ml4se-tertiary-study-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-ml4se-tertiary-study-finding] | EV-ml4se-tertiary-study-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-transfer] | A1DT-ml4se-tertiary-study-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-ml4se-tertiary-study-root] | EV-ml4se-tertiary-study-002, EV-ml4se-tertiary-study-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-ml4se-tertiary-study-finding-boundary] | A1DT-ml4se-tertiary-study-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-ml4se-tertiary-study-finding] | EV-ml4se-tertiary-study-003, EV-ml4se-tertiary-study-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |


### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-ml4se-tertiary-study-structure-check] | [dim-ml4se-tertiary-study-root], A1DT-ml4se-tertiary-study-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-ml4se-tertiary-study-visual-check] | EV-ml4se-tertiary-study-002, EV-ml4se-tertiary-study-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
