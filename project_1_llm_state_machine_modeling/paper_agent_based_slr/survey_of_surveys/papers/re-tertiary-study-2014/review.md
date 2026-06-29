# Systematic Reviews in Requirements Engineering: A Tertiary Study

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Systematic Reviews in Requirements Engineering: A Tertiary Study |
| 年份 | 2014 |
| 类型 | tertiary study |
| 出版形态 | 工作坊 |
| 期刊/会议/预印本 | [EmpiRE](https://empire2014.wordpress.com/) |
| CCF 官方大类 | -- |
| CCF 官方等级 | -- |
| CCF 复核状态 | 非 CCF venue / workshop |
| 来源等级 | EmpiRE 2014 workshop；非顶级会议；IEEE DOI |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；图表/表格细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | Requirements Engineering 领域 tertiary study |
| SE 子领域 | Requirements Engineering |
| A1 角色 | 领域专门化 tertiary study 样本，用于验证“特定 SE 子领域如何定义 topic / quality / impact / practitioners”。 |
| 是否目标证据池 | 否。 |
| schema 历史观察 | 暴露“领域专门化”字段：目标 SE 子领域、topic taxonomy、教育/实践影响。 |

## 2. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 目标是给出 RE 领域 SLR 的 comprehensive overview，并评估 quality、topics、impact for education/practice。 | `paper_content.txt` Page 2 摘要。 | 可迁移为“特定 SE 子领域的综述元模型”。 | RE 子领域样本，不能直接代表 testing/MDE/LLM4SE 等主题。 |
| dimension pattern | 维度包括 automated/manual search、53 distinct reviews、64 publications、quality、topics、education/practice relevance。 | `paper_content.txt` Page 2 摘要与方法段。 | 可迁移到 A2a 的领域专门字段。 | 教育/实践影响字段可参考，但字段树需由目标主题研究者裁定。 |
| finding pattern | finding 关注 RE SLR 数量、主题与质量；具体结论需进一步深读结果章节。 | `paper_content.txt` Page 2 摘要。 | 候选可迁移。 | 当前只读摘要级结果，具体 finding 需 A2a 深读结果章节。 |
| evidence presentation pattern | 使用 distinct reviews / publications 分母、自动与手工搜索来源、质量评估结果。 | `paper_content.txt` Page 2 摘要。 | 可迁移为候选池和去重字段。 | distinct reviews/publications 分母可迁移，细节需 PDF 表格核对。 |
| validity / threat pattern | 本轮未完整定位 threat section；需 A2a 深读。 | `paper_content.txt` Page 2--9。 | 待核验。 | threat section 未完整定位，不能作为已饱和 threat 模板。 |
| report structure pattern | 短 workshop tertiary study，结构紧凑；适合压测短文档字段缺失情况。 | `paper_content.txt` Page 1--9。 | 可迁移为“短论文也要记录缺失字段”。 | 短 workshop 结构紧凑，不能当成完整期刊综述结构。 |

## 3. 对 PR-A1 schema 的启发

1. `target_se_subfield` 应成为候选字段，避免把所有 SE SLR 混为一个领域。
2. `publication_count` 与 `distinct_study_count` 应分开，避免多篇报告同一 SLR 造成重复。
3. 需要 `education_practice_relevance` 字段，承接导师强调的 research finding / practical impact。

## 4. 待复核

- PDF 表格与质量评价细节待人工核对。
- EmpiRE 是 workshop，不能写成顶级 venue。

## 5. A1-M0--M6 脚手架元维度贡献

| A1-M 脚手架元维度 | 本篇可贡献的模式先验 | 采纳边界 |
|---|---|---|
| A1-M0 研究意图与综述元模型 | 将 Requirements Engineering 二次研究作为 tertiary study 对象。 | 可迁移“SE 子领域 tertiary”元模型。 |
| A1-M1 语料收集与纳排 | 提供 RE 三级研究的搜索与选择流程。 | EmpiRE workshop 来源需标注非顶级 venue。 |
| A1-M2 研究对象与主题语义 | 提供 RE 子领域 topic / evidence 分类样本。 | 可作为 RE 子领域 模式种子。 |
| A1-M3 方法 / 技术 / 干预 | 主要关注 RE review 类型和主题，不是具体技术干预。 | 只作弱候选。 |
| A1-M4 评价、证据与复现资产 | 可迁移 quality / reporting / evidence-presentation 字段。 | 表格需后续核对。 |
| A1-M5 统计分析就绪 | 可形成 RE secondary studies 的分布统计。 | 小样本与 workshop 语境需降级。 |
| A1-M6 research finding 形成与裁决 | 可从 RE review 覆盖缺口形成候选 finding。 | 不支撑 Paper2 目标领域结论。 |

## 维度树复原

### 一句话结论

本文的维度树主类型为“RE tertiary 主题统计树”，辅助类型为“质量 / impact 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-re-tertiary-study-2014-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-re-tertiary-study-2014-source-schema-candidates]

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-re-tertiary-study-2014-root] | Systematic Reviews in Requirements Engineering 的研究目标 / RQ / 贡献声明 | primary study / secondary study | [dim-re-tertiary-study-2014-b1] 综述范围与研究问题；[dim-re-tertiary-study-2014-b2] 语料收集与纳排；[dim-re-tertiary-study-2014-b3] 主题 / 对象分类；[dim-re-tertiary-study-2014-b4] 方法 / 技术 / 干预；[dim-re-tertiary-study-2014-b5] 评价、统计与候选发现 | [ev-re-tertiary-study-2014-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-re-tertiary-study-2014-root] Systematic Reviews in Requirements Engineering
├── [dim-re-tertiary-study-2014-b1] 综述范围与研究问题
│   └── [leaf-re-tertiary-study-2014-scope] 研究范围与单位对象
├── [dim-re-tertiary-study-2014-b2] 语料收集与纳排
│   └── [leaf-re-tertiary-study-2014-corpus] 语料与纳排链条
├── [dim-re-tertiary-study-2014-b3] 主题 / 对象分类
│   └── [leaf-re-tertiary-study-2014-taxonomy] 主题与维度分类
├── [dim-re-tertiary-study-2014-b4] 方法 / 技术 / 干预
│   └── [leaf-re-tertiary-study-2014-method] 方法 / 技术 / 干预分类
└── [dim-re-tertiary-study-2014-b5] 评价、统计与候选发现
    └── [leaf-re-tertiary-study-2014-evidence] 评价、证据与复现资产
    └── [leaf-re-tertiary-study-2014-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-re-tertiary-study-2014-scope] | 研究范围与单位对象 | [dim-re-tertiary-study-2014-b1] | 定义 Requirements Engineering 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-scope] |
| [leaf-re-tertiary-study-2014-corpus] | 语料与纳排链条 | [dim-re-tertiary-study-2014-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-corpus] |
| [leaf-re-tertiary-study-2014-taxonomy] | 主题与维度分类 | [dim-re-tertiary-study-2014-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-taxonomy] |
| [leaf-re-tertiary-study-2014-method] | 方法 / 技术 / 干预分类 | [dim-re-tertiary-study-2014-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-method] |
| [leaf-re-tertiary-study-2014-evidence] | 评价、证据与复现资产 | [dim-re-tertiary-study-2014-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-evidence] |
| [leaf-re-tertiary-study-2014-finding] | 统计观察与候选发现 | [dim-re-tertiary-study-2014-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 可进入描述统计 / 交叉统计，前提是分母和样本单位明确。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-re-tertiary-study-2014-leaf-finding] |

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-re-tertiary-study-2014-orig-re-topic] | [dim-re-tertiary-study-2014-b1] | RE 主题字段 | 需求获取、建模、验证、管理、追踪、质量等子主题。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-re-tertiary-study-2014-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-re-tertiary-study-2014-orig-secondary-study-quality] | [dim-re-tertiary-study-2014-b2] | 二级研究质量字段 | 检索、纳排、QA、数据抽取、综合和报告质量。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-re-tertiary-study-2014-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-re-tertiary-study-2014-orig-impact] | [dim-re-tertiary-study-2014-b3] | 影响字段 | 学术影响、实践影响、工业采用和引用 / follow-up。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-re-tertiary-study-2014-orig-method-gap] | [dim-re-tertiary-study-2014-b4] | 方法缺口字段 | 方法报告不足、主题覆盖不足、数据缺失和 validity threat。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/re-tertiary-study-2014__codex.md)、[claude](../../audits/a1dt-19x3/results/re-tertiary-study-2014__claude.md)、[deepseek](../../audits/a1dt-19x3/results/re-tertiary-study-2014__deepseek.md)。 [clm-re-tertiary-study-2014-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-re-tertiary-study-2014-orig-rq] | RE tertiary RQ | secondary study count、topic、quality、impact、method gap | tertiary seed | SLR/SMS 单位对象分开 | 核对 RQ |
| [dim-re-tertiary-study-2014-orig-corpus] | RE 二级研究语料 | search、selection、included SLR/SMS、year/venue | 分母链 seed | workshop/venue 边界记录 | 核对 selection |
| [dim-re-tertiary-study-2014-orig-topic] | RE topic taxonomy | elicitation、modeling、validation、management、traceability、quality、testing | topic seed | topic 多值需记录 | 核对 topic 表 |
| [dim-re-tertiary-study-2014-orig-quality] | QA1--QA4 与总分 | quality checklist、score、threshold、DARE-like criteria | quality rubric seed | 评分和阈值精核 | 核对 QA table |
| [dim-re-tertiary-study-2014-orig-impact] | 学术/实践影响 | top cited、education、practice relevance、follow-up research | impact seed | citation 与 impact 不等同 | 核对 impact/result |
| [dim-re-tertiary-study-2014-orig-gap] | 方法与主题缺口 | coverage gap、reporting deficiency、validity threat、missing replication | candidate finding seed | 需跨论文验证 | 核对 discussion |

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
| 研究范围与单位对象 | `RE tertiary RQ` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
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
| [dim-re-tertiary-study-2014-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否（A1-DT 阶段仅作 schema seed） | 识别可迁移的维度模式类型 | 原文具备系统性证据，可作为后续主统计池候选；但当前 A.2/A.3 多数证据仍待 A2a 精确锚定，不直接进入 SUMMARY 定量统计。 |
| [leaf-re-tertiary-study-2014-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | 本文纳入样本或分类表 | 否（A1-DT 阶段仅作 schema seed） | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 精确页码 / 表图核验并扩库验证取值空间是否饱和。 |
| [leaf-re-tertiary-study-2014-finding] | 候选发现台账，不直接作为 final finding | 统计结果 + discussion | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-re-tertiary-study-2014-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | Requirements Engineering 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-re-tertiary-study-2014-transfer] |
| [leaf-re-tertiary-study-2014-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-re-tertiary-study-2014-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-re-tertiary-study-2014-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-re-tertiary-study-2014-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-re-tertiary-study-2014-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-re-tertiary-study-2014-001 | [ev-re-tertiary-study-2014-root] | [src-re-tertiary-study-2014-text], [src-re-tertiary-study-2014-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-re-tertiary-study-2014-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-re-tertiary-study-2014-002 | [ev-re-tertiary-study-2014-taxonomy] | [src-re-tertiary-study-2014-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-re-tertiary-study-2014-b1], [dim-re-tertiary-study-2014-b2], [dim-re-tertiary-study-2014-b3], [dim-re-tertiary-study-2014-b4], [dim-re-tertiary-study-2014-b5], [leaf-re-tertiary-study-2014-taxonomy], [leaf-re-tertiary-study-2014-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-re-tertiary-study-2014-003 | [ev-re-tertiary-study-2014-stat] | [src-re-tertiary-study-2014-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作候选发现 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | statistical_result | not_verified | [leaf-re-tertiary-study-2014-evidence], [leaf-re-tertiary-study-2014-finding], [leaf-re-tertiary-study-2014-orig-re-topic], [leaf-re-tertiary-study-2014-orig-secondary-study-quality], [leaf-re-tertiary-study-2014-orig-impact], [leaf-re-tertiary-study-2014-orig-method-gap] | true | false | -- | 统计观察仍需保留分母和外推限制。 |
| EV-re-tertiary-study-2014-004 | [ev-re-tertiary-study-2014-risk] | [src-re-tertiary-study-2014-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-re-tertiary-study-2014-root], [leaf-re-tertiary-study-2014-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-re-tertiary-study-2014-tree-type] | A1DT-re-tertiary-study-2014-C01 | 本文的维度树主类型为“RE tertiary 主题统计树”，辅助类型为“质量 / impact 树”。候选主统计池资格：有系统检索 / 映射 / tertiary / MLR 证据，但本 A1-DT 维度树仍是 schema seed；正式统计用途须等 A2a 完成精确页码、表图和字段锚定后再升级。 [clm-re-tertiary-study-2014-tree-type] | tree_type | [dim-re-tertiary-study-2014-root] | EV-re-tertiary-study-2014-001, EV-re-tertiary-study-2014-004 | 树型判断仅限本文，不代表所有 Requirements Engineering 综述。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-scope] | A1DT-re-tertiary-study-2014-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-scope] | EV-re-tertiary-study-2014-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-corpus] | A1DT-re-tertiary-study-2014-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-corpus] | EV-re-tertiary-study-2014-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-taxonomy] | A1DT-re-tertiary-study-2014-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-taxonomy] | EV-re-tertiary-study-2014-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-method] | A1DT-re-tertiary-study-2014-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-method] | EV-re-tertiary-study-2014-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-evidence] | A1DT-re-tertiary-study-2014-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-evidence] | EV-re-tertiary-study-2014-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-leaf-finding] | A1DT-re-tertiary-study-2014-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-re-tertiary-study-2014-finding] | EV-re-tertiary-study-2014-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-transfer] | A1DT-re-tertiary-study-2014-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-re-tertiary-study-2014-root] | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-finding-boundary] | A1DT-re-tertiary-study-2014-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-re-tertiary-study-2014-finding] | EV-re-tertiary-study-2014-003, EV-re-tertiary-study-2014-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |

| [clm-re-tertiary-study-2014-source-schema-candidates] | A1DT-re-tertiary-study-2014-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-re-tertiary-study-2014-orig-re-topic], [leaf-re-tertiary-study-2014-orig-secondary-study-quality], [leaf-re-tertiary-study-2014-orig-impact], [leaf-re-tertiary-study-2014-orig-method-gap] | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-re-tertiary-study-2014-a1dt-19x3-repair] | A1DT-re-tertiary-study-2014-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-re-tertiary-study-2014-root] | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-re-tertiary-study-2014-structure-check] | [dim-re-tertiary-study-2014-root], A1DT-re-tertiary-study-2014-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-re-tertiary-study-2014-visual-check] | EV-re-tertiary-study-2014-002, EV-re-tertiary-study-2014-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
