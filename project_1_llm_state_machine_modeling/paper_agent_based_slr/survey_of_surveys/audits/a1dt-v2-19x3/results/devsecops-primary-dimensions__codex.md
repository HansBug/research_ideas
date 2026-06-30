### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `devsecops-primary-dimensions` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已通读 3158 行全文文本、表 1--21、附录与参考文献尾部 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；核对标题、作者、年份、DOI、样本规模与本地 eligibility 元数据 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo`、`pdftotext -layout` 核对页 1、19--24、26--31，并渲染目视核验 PDF 第 20、24 页的 Fig. 5、Table 20/21 |
| 原文类型 | 多声部文献综述（Multi-vocal Literature Review, MLR） |
| 被编码样本单位 | 主样本为纳入的 white literature / grey literature 文献条目；实际编码观察单位为文献中的 text segment，经 code、theme、category、CPTM item 与 lifecycle stage 聚合 |
| 样本数量 / 分母 | 主 MLR：104 篇 WL + 43 篇 GL = 147；其中 RQ1 为 102 WL + 43 GL，RQ2 另有 2 WL + 0 GL；confirmatory search 13 WL + 7 GL 不进入 TA/CPTM |
| 原生树类型 | 维度森林 + 关系型模型；核心是 aspect -> text segment/code -> theme/category -> C/P/T/M item -> lifecycle stage/edge |
| 主统计池资格 | 局部可统计；可进入 A1-DT schema / 维度树统计池，不可把 DevSecOps 领域结论迁移为 Paper2 final finding |
| 总体判定 | needs repair；原文证据充分，但现有 `review.md` 仍需把通用六叶投影降级，把原生字段树与关系边抬升为事实源 |

### 1. 原文证据阅读说明

实际读取文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。PDF 做了定向版面核验：第 20 页确认 Fig. 5 与 Table 18，第 24 页确认 Table 20/21 与 RQ2 文本；未核验 Zenodo full CPTM package，因此完整图中每一条连线仍需 A2a 精核。

关键证据锚点：

1. 摘要：声明 MLR 覆盖 104 WL、43 GL，并用 TA 生成五大方面和 CPTM 模型。
2. §3.3：RQ1 直接要求 aspects、themes 与 links；RQ2 检查 GSE context。
3. §3.4.1--3.4.3：ACM、IEEE、Scopus、Google 双轨检索；Search String 1/2 与 snowballing。
4. §3.5：纳入/排除标准、QA 表、18 分满分、11 分阈值。
5. Table 3：检索执行链，显示 Search 1/2 的收集、预筛、选择、QA、snowballing 数量。
6. §3.8.1--3.8.2：TA 链路为 text、code、theme、model；WL 先归纳，GL 后演绎。
7. Table 5：五大 aspect 的 text segment、code、theme、category 规模。
8. Tables 6--19：definitions、challenges、practices、metrics、tools 的原生主题表与取值空间。
9. Fig. 5、Table 20、Table 21：CPTM 与 Gartner 十阶段生命周期映射，PDF 已定向核验存在。
10. §4.2 与 §5.3：GSE 缺失结论及 search string 威胁，作者给出竞争解释。
11. §4.3：confirmatory search 不进入 TA/CPTM，只作新近验证。
12. Data availability：开放材料包括 protocol、QA score、raw text/codes、TA tables、full CPTM model；Zenodo 未在本任务核验。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 white / grey literature 文献条目，附录按 `S1-ACM-*`、`S1-IEEE-*`、`S1-SC-*`、`S1-GL-*`、`S2-*` 列出。真正进入编码的单位是这些文献中关于 definition、challenge、practice、tool、metric、GSE adoption 的 text segment。

2. 作者有系统检索、纳排、质量评价、数据抽取与编码方案。检索分 Search String 1 和 2，纳排规则在 §3.5，QA 阈值为 11/18，数据抽取使用 adapted extraction form，综合使用 reflexive TA。

3. 原文字段来源是 extraction form + thematic analysis tables + CPTM model + lifecycle mapping table。具体证据在 Table 5--21，Zenodo 复现材料可作为外部增强证据但本任务未核验。

4. RQ 不是树根本身的字段值，而是结果组织方式和字段生成目标：RQ1 产生 aspect/theme/link schema；RQ2 产生 GSE context gap 分支。

5. 本文不是 roadmap / vision / guideline；有系统样本库，不需要降级为无系统样本库。但 DevSecOps 具体领域结论只能作 boundary anchor / methodological seed，不进入 Paper2 目标领域 final finding。

### 3. 原生样本编码维度树 / 维度森林

```text
MLRIncludedEvidenceSet
├── LiteratureRecord
│   ├── paper_id: S1/S2/CS + source prefix
│   ├── source_track: white_literature / grey_literature / confirmatory
│   ├── search_string_id: Search 1 / Search 2 / confirmatory
│   ├── source_database_or_engine: ACM / IEEE / Scopus / Google / snowballing
│   ├── included_role: main_TA / RQ2_gap_probe / confirmatory_only / prior_review_validation
│   └── qa_status: pass_threshold / score_available_in_Zenodo / not_verified_locally
├── ExtractedObservation
│   ├── aspect: Definition / Challenge / Practice / ToolOrTechnology / MetricOrMeasurement / GSEContext
│   ├── text_segment
│   ├── code
│   ├── theme_or_item_id: definition_theme / Cxx / Pxx / Txx / Mxx
│   ├── category: OPC / PC / Technology / Business
│   ├── frequency
│   ├── contributed_paper_ids
│   └── prior_review_match_or_complement
├── DefinitionForest
│   ├── 28 WL + 15 GL definitions
│   ├── 74 codes -> 21 themes -> 4 categories
│   └── common_definition_author_frequency
├── ChallengePracticeToolMetricForest
│   ├── Challenge: 85 codes -> 23 themes -> final 28 challenges
│   ├── Practice: 142 codes -> 56 themes -> final 60 practices
│   ├── Metric: 20 codes -> 16 themes -> final 20 metrics
│   ├── Tool: 56 tool codes -> 16 themes -> final 18 tool groups
│   └── CPTM relation edges: Challenge -> Practice -> Tool / Metric
├── LifecycleProjection
│   ├── stage: Plan / Create / Verify / Preproduction / Release / Prevent / Detect / Respond / Predict / Adapt
│   └── mapped C/P/T/M items
└── GSEGapProbe
    ├── Search String 2 hits: 2 WL, 0 GL after QA
    ├── matched partial global DevOps/security evidence
    ├── absence finding
    └── alternative explanations and search-string limitation
```

缺失部分：Fig. 5 的完整连线在 PDF 图中字体很小，Table 21 已给出阶段映射，但 full CPTM model 在 Zenodo。A2a 应核验 Zenodo full CPTM，逐条确认 C->P、P->T、P->M 边。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 来源轨道 | LiteratureRecord | §3.4、Table 3、附录 | 文献来自正式出版或灰色来源 | WL / GL / confirmatory | 完整枚举 | 未标明则不可分层统计 | WL/GL 对比 | 多声部证据差异 | §3.4、§4.1 | 只迁移分层做法 |
| L2 | 文献 ID | LiteratureRecord | Table 4、附录 | 纳入文献的内部编号 | `S1-ACM-*` 等 | 层级枚举 | 无 ID 则无法回溯 | 来源回链 | 审计追踪 | Appendix A.1/A.2 | 不迁移具体论文池 |
| L3 | 检索角色 | LiteratureRecord | Table 3、§4.3 | 主 TA、RQ2 或确认性检索 | main / RQ2 / confirmatory_only | 完整枚举 | 混用会污染统计 | 分母隔离 | staleness 控制 | §3.7、§4.3 | 必须保留 confirmatory 排除 |
| L4 | aspect | ExtractedObservation | §4.1.1、Fig. 4、Table 5 | DevSecOps 被抽取的一级方面 | Definition / Challenge / Practice / Tool / Metric / GSE | 完整枚举 | 未覆盖不等于不存在 | aspect 分布 | schema 主干 seed | Table 5 | 只迁移结构 |
| L5 | text segment count | ExtractedObservation | Table 5 | 每个 aspect 抽取片段数量 | 28/15、73/53、219/137、7/13、18/45 | 数值/分母 | 仅表示文献关注度 | 频次统计 | 关注强弱 | Table 5 | 不外推真实重要性 |
| L6 | code | ExtractedObservation | §3.8、Tables 6--17 | 从 text segment 标注出的编码 | 自由文本 | 自由文本加理由 | 缺失则 theme 无回链 | 审计链 | 编码证据 | §3.8.2 | A2a 需原始表核验 |
| L7 | theme / item id | CPTMForest | Tables 6--19 | 主题或编号项 | definition theme、C01--C28、P01--P60、T01--T18、M01--M20 | 层级枚举 | 未编号项需待核验 | 分类统计 | schema seed | Tables 8--19 | 不迁移领域值 |
| L8 | category | CPTMForest | Table 5、Tables 6--17 | 高阶主题类别 | OPC / PC / Technology / Business | 完整枚举 | tool 默认 Technology；模型中可跨切 | 交叉统计 | 维度分层 | Table 5 | 类别名可迁移，内容不可照搬 |
| L9 | frequency | CPTMForest | Tables 6--19 | 主题或项被提及次数 | 非负整数 / 未给出 | 数值 | 无频次不代表无效 | 排名/关注度 | 弱 finding | Tables 6--19 | 不等于现实优先级 |
| L10 | contributed papers | CPTMForest | Tables 6--19 | 支撑 code/theme 的文献 ID | 文献 ID 集合 | 关系值 | 缺失则证据弱 | 回溯审计 | 证据强度 | Tables 6--19 | 需保留 source IDs |
| L11 | prior review match | CPTMForest | Tables 8--19、§3.6 | 是否与前序综述匹配或补充 | matched / partly / complemented / none | 布尔/枚举 | 无匹配不等于错误 | 可信度辅助 | confirmatory role | §3.6、Tables 8--19 | 前序综述不进主样本 |
| L12 | measuring / goal | Metric | Tables 16--17 | 指标的测量方法和目标 | 自由文本 + 方向性 | 自由文本加理由 | 无测量方法则不可量化 | metric schema | 评价启发 | Tables 16--17 | 不迁移 DevSecOps 指标值 |
| L13 | tool function group | Tool | Table 19 | 工具按功能归组 | T01--T18 | 层级枚举 | 未链接工具是有效缺失 | 工具类别统计 | 工具缺口 | Table 19 | 不迁移工具清单 |
| L14 | lifecycle stage | LifecycleProjection | Table 20/21、Fig. 5--9 | CPTM 项映射到阶段 | Plan/Create/Verify/Preprod/Release/Prevent/Detect/Respond/Predict/Adapt | 完整枚举 | NA 表示无对应项 | 阶段分布 | shift-left 等候选观察 | Table 20/21 | Gartner 模型非通用真理 |
| L15 | CPTM relation target | CPTMRelation | Fig. 5、Table 21 | C/P/T/M 之间的连接 | C->P、P->T、P->M | 关系值 | no linked tool/metric 是重要缺失 | 关系统计 | 缺口发现 | Fig. 5、Table 21 | full edge 需 Zenodo 核验 |
| L16 | GSE gap status | GSEGapProbe | §4.2 | DevSecOps+GSE 命中与缺失 | 2 WL / 0 GL / absence / alternative explanation | 数值+自由文本 | 没搜到需降级 | gap 统计 | negative finding seed | §4.2、§5.3 | 不迁移为目标领域结论 |
| L17 | open science material | EvidenceQuality | Data availability | 可复核材料类型 | protocol / QA / raw text-codes / TA tables / full CPTM | 外部资料引用 | 未打开则待核验 | 复现资产统计 | 审计链启发 | Data availability | 本任务未核验 Zenodo |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | LiteratureRecord | contributes_to | ExtractedObservation | text segment/code/theme | 无来源 ID 则弱证据 | Tables 6--19 | 证据回链 |
| E2 | text segment | coded_as | code | 自由文本 code | 缺失则 TA 链断裂 | §3.8.2 | 编码审计 |
| E3 | code | translated_to | theme/item | theme、C/P/T/M 编号 | 待核验 | §3.8.2、Table 5 | 维度生成 |
| E4 | theme/item | classified_as | category | OPC/PC/Technology/Business | tool 默认 Technology，模型中可跨切 | Table 5 | 分类统计 |
| E5 | challenge | addressed_by | practice | P01--P60 | 无实践表示 unresolved gap | Fig. 5、Table 21 | CPTM 核心关系 |
| E6 | practice | supported_by | tool group | T01--T18 / NA | NA 是有效缺失，不应删掉 | Fig. 5、Table 21 | 工具支持分析 |
| E7 | practice | measured_by | metric | M01--M20 / NA | NA 是 metrics gap | Fig. 5、Table 21 | 评价缺口分析 |
| E8 | C/P/T/M item | allocated_to | lifecycle stage | 10 个 Gartner stage | NA 表示该 stage 无对应元素 | Table 20/21 | 生命周期投影 |
| E9 | metric | mapped_to | DevOps metric | Amaro et al. DevOps metric | 未匹配表示外部对齐不足 | Table 18 | 外部分类法引用 |
| E10 | Search String 2 result | supports | GSE absence claim | 2 WL、0 GL、四种解释 | absence 需保留 search limitation | §4.2、§5.3 | negative finding 降级 |

### 6. 统计观察、候选 finding 与 final finding 边界

原文字段/统计表支持的统计观察：

- practices 是覆盖最多的 aspect，metrics/measurement 覆盖最少；来自 Fig. 4 与 Table 5。
- WL 更偏 definitions、challenges、practices；GL 更偏 tools、metrics 与 business/pragmatic implications。
- challenge 最终 28 项，practice 最终 60 项，metric 最终 20 项，tool group 最终 18 组。
- Table 21 显示许多 tool/metric 对应项为 NA，这不是普通缺失，而是模型中的关系缺口。
- RQ2 的系统检索仅留下 2 篇 WL、0 篇 GL 支撑 GSE 相关讨论，形成 absence observation。
- confirmatory search 的 20 篇新材料只用于验证和趋势观察，不进入主 TA/CPTM。

discussion / recommendation / roadmap 候选 finding：

- DevSecOps metrics 研究薄弱，尤其 academic WL 中更薄。
- DevSecOps 落地高度依赖技术工具，但组织/流程挑战多在早期阶段出现。
- GSE/global DevSecOps 是潜在研究空白，但受术语和检索式限制。
- 2021--2022 新文献显示 DevSecOps 研究可能转向 framework/model design。
- 开放材料链可作为 high-trust secondary study 的方法学样板。

对 Paper2 可迁移的方法学启发：

- 维度树必须支持层级字段、来源分层、频次、证据回链、关系边、缺失值语义。
- negative finding 必须绑定检索式、失败路径、竞争解释和 claim strength。
- confirmatory-only 样本必须与主统计分母隔离。
- reflexive TA 可以作为人机协作编码的审计参照，但要记录主观性与裁决过程。

绝不能迁移的领域结论：

- DevSecOps 的具体 C/P/T/M 项不能成为 Paper2 目标领域结论。
- Gartner 十阶段不能作为所有软件工程综述的通用生命周期。
- GSE 缺失不能外推到其他 topic。
- WL/GL 关注差异不能外推为所有 MLR 的稳定规律。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | 现有 `review.md` 仍把六个通用 leaf 放在显著位置，容易被误读为原文树 | 将“原文 schema 主树”移到维度树复原开头；六个通用接口只保留为投影层 |
| C | “是否目标证据池：否”与 metadata 的 `eligible_for_statistical_synthesis: true`、本文系统样本证据冲突 | 拆成两列：A1-DT 主统计池 = 局部可统计/是；Paper2 目标领域 final finding pool = 否 |
| C | 样本数量需精确拆分 | SUMMARY 应写：主 MLR 104 WL + 43 GL；RQ1 102 WL +43 GL；RQ2 2 WL +0 GL；confirmatory 13 WL +7 GL excluded |
| I | 关系边太泛，只有 method-evidence / taxonomy-finding | 新增原生 CPTM 边：C->P、P->T、P->M、item->stage、metric->DevOps metric |
| I | A.2 证据账本当前大量 `not_verified` 和泛化释义 | 用本审计的 A.2 草案替换/补充，至少锚定 §3.3、§3.4、§3.5、§3.8、Table 5、Tables 6--19、Fig. 5、Table 20/21、§4.2、§5 |
| I | 原文叶子缺少 source_track、paper_id、frequency、prior_review_match、measuring/goal、tool function | 按第 4 节叶子表补齐 |
| M | 旧 v1/19x3 历史提示仍很长 | 压缩为历史说明，避免成为事实真源 |
| M | PDF 核验状态不够具体 | 写明本轮已核验 PDF 第 20、24 页，但 full CPTM / Zenodo 未核验 |
| M | A1-M0--M6 脚手架内容过多 | 保留为跨论文投影提示，不参与单篇原生树定义 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV1 | `bibtex.bib`, `metadata.json`, `paper_content.txt` | 摘要 | 标题、DOI、abstract | 2024 JSS MLR，104 WL +43 GL | 元数据 | strong | paper type, sample denominator | 否 | 不支撑字段树细节 |
| EV2 | `paper_content.txt` | §3.3 | RQ1/RQ2 | RQ1 关心 aspects/themes/links；RQ2 关心 GSE | RQ/schema source | strong | root, aspect/link/gap branches | 否 | RQ 不是叶子全集 |
| EV3 | `paper_content.txt` | §3.4, Table 3 | Search String 1/2、search execution | WL/GL 双轨检索与 RQ2 加词检索 | corpus denominator | strong | source_track, search_role | 否 | Google relevance 截断有局限 |
| EV4 | `paper_content.txt` | §3.5, Fig. 2 | inclusion/exclusion, QA | QA 18 分、阈值 11，QA score 在 Zenodo | quality gate | medium | qa_status | 是，若需 Fig.2 细项 | Zenodo QA 分数未读 |
| EV5 | `paper_content.txt` | §3.8.1--3.8.2 | TA 方法 | text -> code -> theme -> model | coding chain | strong | text/code/theme/model tree | 否 | 不等于 coding reliability |
| EV6 | `paper_content.txt` | Table 5 | TA summary | 五大 aspect 的 segments/codes/themes/categories | dimension counts | strong | aspect, frequency, category | 否 | 表示关注度，不表示现实重要性 |
| EV7 | `paper_content.txt` | Tables 6--19 | thematic analysis tables | C/P/T/M、definition themes、tools、metrics | leaf value space | medium | native leaves L6--L13 | 是，A2a 逐表核验 | 具体取值不可跨域迁移 |
| EV8 | `paper.pdf`, `paper_content.txt` | Fig. 5, Table 20/21 | PDF 第20、24页已看 | CPTM 图、Gartner stage、stage mapping | relation schema | medium | relation edges, lifecycle stage | 是，full CPTM/Zenodo | PDF 图连线需精核 |
| EV9 | `paper_content.txt` | §4.2 | RQ2 results | 2 WL、0 GL，GSE/global 维度缺失 | gap evidence | strong | GSEGapProbe | 否 | absence 受检索词影响 |
| EV10 | `paper_content.txt` | §4.3 | Confirmatory search | 13 WL +7 GL 不进入 TA/CPTM | denominator boundary | strong | included_role | 否 | 只能作验证/趋势 |
| EV11 | `paper_content.txt` | §5.1--5.3 | threats | selection、extraction、synthesis、search string 风险 | limitation | strong | migration boundary | 否 | 限制不否定 schema seed |
| EV12 | `paper_content.txt` | Data availability | Zenodo material list | protocol、QA、raw text/codes、TA tables、full CPTM | reproducibility asset | medium | open science leaf | 是，需打开 Zenodo | 本任务未核验外部包 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CL1 | 本文是有系统样本库的 MLR，不应降级为 roadmap/guideline | type | paper | EV1, EV3, EV4 | strong | A1-DT 统计资格判断 | QA 明细需 Zenodo 核验 |
| CL2 | 样本单位是纳入文献条目，编码观察单位是 text segment/code/theme | sample_unit | LiteratureRecord, ExtractedObservation | EV5, EV6, EV7 | strong | 重写 review.md 样本单位 | 不应把 RQ 当样本单位 |
| CL3 | 原生树是维度森林 + CPTM 关系模型 | tree_type | native schema | EV6, EV7, EV8 | strong | 维度树复原 | full CPTM 连线仍需 A2a |
| CL4 | 本文可进入 A1-DT schema 主统计池，但不可进入 Paper2 目标领域 final finding pool | eligibility | statistical pool | EV1, EV3, EV10, EV11 | medium | SUMMARY 修正 | 需区分统计池类型 |
| CL5 | 原文叶子至少包括 source_track、aspect、code/theme、category、frequency、source IDs、stage、relation target | leaf_set | L1--L17 | EV6, EV7, EV8 | medium | review.md 返修 | 叶子全集需 Zenodo/A2a 核验 |
| CL6 | CPTM 边是本文最重要的关系型 schema，不可用通用 method-evidence 边替代 | relation | E5--E8 | EV8 | medium | 关系边表 | Fig.5 图内细线需精核 |
| CL7 | GSE absence 是候选 gap，不是强 final finding | candidate_finding | GSEGapProbe | EV9, EV11 | medium | finding boundary | 作者承认术语遗漏可能 |
| CL8 | confirmatory search 必须排除在主 TA/CPTM 分母之外 | denominator | included_role | EV10 | strong | 统计口径 | 可用于趋势，不可混入主统计 |
| CL9 | 现有 `review.md` 需要返修，而不是 blocked | repair | existing review | EV1--EV12 | strong | C/I/M 修复清单 | 不需改原文材料 |

### 9. 技能使用与自我审查记录

已读取并采用的技能/指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence discipline、evidence gate、reviewer mode。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 要具体、可操作、证据支撑。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 claim audit、risk audit、weak/needs evidence 降级。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先读资源、明确假设、风险与依赖的结构化输出。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用严格贴合原文、不编造缺失实验/配置的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用 schema 化字段、任务风险、证据状态表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：只采用 artifact-gated / validator-gated 思路；未启动任何 autoresearch、subagent 或后台 agent。

最高风险 3 点及主线程复核方式：

1. Fig. 5 的完整 CPTM 连线未逐条核验。主线程应打开 Zenodo full CPTM model 和 PDF 高分辨率图，逐条补 C->P、P->T、P->M。
2. QA score 明细只知道存在于开放材料，未读取 Zenodo。主线程若要统计质量分，应先下载/核验 included papers + QA score。
3. 现有 `review.md` 的历史 A1-M0--M6 与 v1 审计内容很长，容易污染 v2 口径。主线程合并时应以本报告的 native schema 为事实源，旧内容仅作投影提示。

blocked / timeout / 文件缺失：未出现。所有指定本地技能文件与论文四个本地文件均可读；PDF 可读并完成定向核验。