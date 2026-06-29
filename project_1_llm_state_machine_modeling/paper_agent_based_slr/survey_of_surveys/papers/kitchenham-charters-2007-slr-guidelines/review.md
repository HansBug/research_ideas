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

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-kitchenham-charters-2007-slr-guidelines-source-schema-candidates]

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

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-kitchenham-charters-2007-slr-guidelines-orig-protocol] | [dim-kitchenham-charters-2007-slr-guidelines-b1] | 综述协议字段 | 背景、RQ、检索策略、纳排、质量评价、数据抽取和综合计划。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-kitchenham-charters-2007-slr-guidelines-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-kitchenham-charters-2007-slr-guidelines-orig-search-selection] | [dim-kitchenham-charters-2007-slr-guidelines-b2] | 检索与筛选字段 | 数据库、检索式、时间范围、去重、初筛、全文筛选和排除理由。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-kitchenham-charters-2007-slr-guidelines-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-kitchenham-charters-2007-slr-guidelines-orig-quality-validity] | [dim-kitchenham-charters-2007-slr-guidelines-root] | 质量与效度字段 | 质量 checklist、bias、可靠性、外部效度和报告透明度。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-kitchenham-charters-2007-slr-guidelines-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-kitchenham-charters-2007-slr-guidelines-orig-synthesis-reporting] | [dim-kitchenham-charters-2007-slr-guidelines-b3] | 综合与报告字段 | 定量 / 定性综合、结果呈现、威胁、结论和更新维护建议。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-kitchenham-charters-2007-slr-guidelines-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/kitchenham-charters-2007-slr-guidelines__codex.md)、[claude](../../audits/a1dt-19x3/results/kitchenham-charters-2007-slr-guidelines__claude.md)、[deepseek](../../audits/a1dt-19x3/results/kitchenham-charters-2007-slr-guidelines__deepseek.md)。 [clm-kitchenham-charters-2007-slr-guidelines-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-kitchenham-charters-2007-slr-guidelines-orig-planning] | 计划与协议 | review need、PICOC、RQ type、protocol、scope、stakeholder | 方法学参考 seed | 不是目标领域统计样本 | 核对 planning 章节 |
| [dim-kitchenham-charters-2007-slr-guidelines-orig-search-selection] | 检索与纳排 | source、search string、trial search、inclusion/exclusion、screening、snowballing | 流程字段 seed | 无执行分母写 guideline_not_applicable | 核对 search strategy |
| [dim-kitchenham-charters-2007-slr-guidelines-orig-quality] | 质量评价 | quality checklist、bias、validity、weighting、sensitivity analysis | quality rubric seed | 指南清单不等于实证质量分布 | 核对 QA 章节 |
| [dim-kitchenham-charters-2007-slr-guidelines-orig-extraction] | 数据抽取 | extraction form、pilot extraction、multiple extractor、disagreement resolution | 字段抽取流程 seed | 无具体样本写 not_applicable | 核对 data extraction 章节 |
| [dim-kitchenham-charters-2007-slr-guidelines-orig-synthesis] | 数据综合 | 定量 synthesis、定性 synthesis、meta-analysis、heterogeneity、narrative synthesis | 分析方法 seed | 指南建议与结果统计分开 | 核对 synthesis 章节 |
| [dim-kitchenham-charters-2007-slr-guidelines-orig-reporting] | 报告、威胁与更新 | report structure、limitations、replication、protocol deviation、update planning | 写作/审计规范 seed | 不进入主统计池 | 核对 reporting 章节 |

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
| 研究范围与单位对象 | `planning / protocol` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
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
| EV-kitchenham-charters-2007-slr-guidelines-003 | [ev-kitchenham-charters-2007-slr-guidelines-stat] | [src-kitchenham-charters-2007-slr-guidelines-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断。 | author_claim | not_verified | [leaf-kitchenham-charters-2007-slr-guidelines-evidence], [leaf-kitchenham-charters-2007-slr-guidelines-finding], [leaf-kitchenham-charters-2007-slr-guidelines-orig-protocol], [leaf-kitchenham-charters-2007-slr-guidelines-orig-search-selection], [leaf-kitchenham-charters-2007-slr-guidelines-orig-quality-validity], [leaf-kitchenham-charters-2007-slr-guidelines-orig-synthesis-reporting] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
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

| [clm-kitchenham-charters-2007-slr-guidelines-source-schema-candidates] | A1DT-kitchenham-charters-2007-slr-guidelines-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-kitchenham-charters-2007-slr-guidelines-orig-protocol], [leaf-kitchenham-charters-2007-slr-guidelines-orig-search-selection], [leaf-kitchenham-charters-2007-slr-guidelines-orig-quality-validity], [leaf-kitchenham-charters-2007-slr-guidelines-orig-synthesis-reporting] | EV-kitchenham-charters-2007-slr-guidelines-002, EV-kitchenham-charters-2007-slr-guidelines-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-kitchenham-charters-2007-slr-guidelines-a1dt-19x3-repair] | A1DT-kitchenham-charters-2007-slr-guidelines-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-kitchenham-charters-2007-slr-guidelines-root] | EV-kitchenham-charters-2007-slr-guidelines-002, EV-kitchenham-charters-2007-slr-guidelines-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-kitchenham-charters-2007-slr-guidelines-structure-check] | [dim-kitchenham-charters-2007-slr-guidelines-root], A1DT-kitchenham-charters-2007-slr-guidelines-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-kitchenham-charters-2007-slr-guidelines-visual-check] | EV-kitchenham-charters-2007-slr-guidelines-002, EV-kitchenham-charters-2007-slr-guidelines-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
