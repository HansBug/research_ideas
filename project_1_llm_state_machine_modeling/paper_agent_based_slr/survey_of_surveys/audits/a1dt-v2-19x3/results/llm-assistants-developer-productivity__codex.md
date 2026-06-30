### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm-assistants-developer-productivity` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已按全文顺序阅读，并定位方法、结果、讨论、威胁与 Primary Studies 列表 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；BibTeX 记录 TOSEM 2026、DOI `10.1145/3809494`；metadata 记录 arXiv PDF 来源、正式发布日期与本地状态 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 确认 43 页，并用 `pdftotext -layout` 核对 Table 1、Fig. 1、Table 2、Table 10、Fig. 7--9、Table 11 的版面文本；未做图片像素级视觉核验 |
| 原文类型 | SLR + SMS |
| 被编码样本单位 | 主要单位是最终纳入的 peer-reviewed primary study；辅助单位是检索记录 / 全文报告 / QA 候选报告 |
| 样本数量 / 分母 | 初检 9,756；去重后 8,953；全文筛选 228；snowballing 后 QA 44；最终纳入 39 primary studies |
| 原生树类型 | 维度森林：检索纳排流 + 质量评价树 + 方法分类树 + 工具/景观树 + benefit/risk 主题树 + SPACE 映射树 |
| 主统计池资格 | 是，但限于“该文原生编码维度 / 统计观察”层面；LLM-assistant productivity 的领域结论不能直接迁移为 Paper2 final finding |
| 总体判定 | needs repair：本次审计完成且未 blocked；现有 `review.md` 需要按 v2 口径重写原生维度树 |

### 1. 原文证据阅读说明

已读取文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。PDF 核验为局部版面文本核验，不是逐页视觉审校；Fig. 6 雷达图精确频次、supplemental appendix / Zenodo package 内部字段仍需后续核验。

关键证据锚点：

| 证据锚点 | 原文位置 | 作用 |
|---|---|---|
| 摘要与引言 | Page 1--2 / §1 | 明确研究对象为 39 篇 peer-reviewed studies，主题是 LLM-assistants 对 developer productivity 的影响 |
| RQ0--RQ3 | §3 | 给出四层结果组织：研究景观、方法实践、影响主题、SPACE 映射 |
| Table 1 | §3.1.1 | 六数据库搜索式与初检分母 9,756 |
| Fig. 1 | §3.2 | PRISMA-style 分母链：8,953、228、44、39 |
| Table 2 | §3.3 | QA1--QA11 质量评价 rubric，0--4 评分，50% 阈值 |
| §3.4 | Data Extraction and Synthesis | 抽取字段包括 goals、tools、strategy/design、tasks、settings、key results；多轮 thematic analysis |
| Table 3--4 | RQ0 | venue research focus 与 LLM tools 分布 |
| Table 5--7 | RQ1 | empirical strategy、procedure、instrument / metric schema |
| Table 8--9 + Fig. 6 | RQ2 | benefit / risk theme taxonomy |
| Table 10--11 + Fig. 7--8 | RQ3 | SPACE 维度、sub-dimensions、quality metrics |
| Fig. 9 + §8 | Discussion | McLuhan Tetrad 是解释框架，不是原始纳排字段 |
| §9 | Threats to Validity | 记录 selection bias、classification rigor、primary evidence limitations、temporal relevance |

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 peer-reviewed primary studies。最终进入综合的是 39 篇；检索 / 筛选流程还涉及 record、full-text report、quality-assessed report 等辅助单位。
2. 作者有系统检索、纳排、QA、数据抽取和编码方案：六数据库检索、control papers 校验搜索式、Rayyan 标注排除理由、full-text screening、snowballing、QA1--QA11、三轮 targeted thematic analysis。
3. 字段来源包括：检索协议、IC/EC、QA rubric、data extraction description、Stol & Fitzgerald strategy taxonomy、Glass/Vessey/Ramesh procedure taxonomy、Hartson formative/summative objective、instrument table、benefit/risk thematic coding、SPACE framework mapping、quality metrics table、McLuhan Tetrad discussion synthesis。
4. RQ 不是字段树根本身，而是结果组织方式；真正被编码的是 primary study。RQ0--RQ3分别调用不同字段簇。
5. 不需要降级为 roadmap / guideline。本文有系统样本库，可进入主统计池；但 Discussion 中的 recommendations / Tetrad 只能作为候选 finding 或解释镜头。

### 3. 原生样本编码维度树 / 维度森林

```text
root: primary_study_set
├── selection_flow
│   ├── source_database
│   ├── search_string_segment: technology / actor / productivity
│   ├── screening_stage: identified / deduplicated / title_abstract / full_text / snowball / QA / included
│   ├── exclusion_code: EC1 / EC2 / EC3 / EC4 / EC5 / ~IC1
│   └── final_inclusion_status
├── quality_assessment
│   ├── QA1--QA11 criterion
│   ├── score_scale: 0--4
│   ├── threshold: 50%
│   └── QA_exclusion_status
├── RQ0_landscape
│   ├── publication_year
│   ├── author_distribution
│   ├── venue_research_focus
│   └── LLM_tool
├── RQ1_methodology
│   ├── empirical_strategy
│   ├── methodological_procedure
│   ├── study_objective: formative / summative
│   ├── analysis_type: qualitative / quantitative / mixed
│   ├── data_source
│   ├── instrument_origin
│   ├── instrument_or_framework
│   └── productivity_metric
├── RQ2_effect_theme
│   ├── benefit_theme: 8 enumerated themes
│   └── risk_theme: 5 enumerated themes
├── RQ3_SPACE_mapping
│   ├── SPACE_dimension
│   ├── SPACE_sub_dimension
│   ├── dimension_count_per_study
│   ├── dimension_overlap
│   └── quality_metric_type
└── discussion_synthesis
    ├── McLuhan_Tetrad: enhance / reverse / obsolesce / retrieve
    ├── practitioner_recommendation
    ├── researcher_recommendation
    └── threat_or_limitation
```

缺失部分：supplemental appendix / Zenodo replication package 中的 per-study extraction form、QA scores、selection decisions 未在本次下载核验；A2a 应精核这些矩阵后再冻结完整叶子取值空间。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 数据库 | selection_flow | Table 1 | 检索来源 | ACM / IEEE / ScienceDirect / Web of Science / Scopus / Springer | 完整枚举 | 未检索则不在范围 | 检索分母 | 检索覆盖风险 | Table 1 | 仅迁移检索设计 |
| L2 | 筛选阶段 | selection_flow | Fig. 1 | record/report 所处流程 | identified / dedup / title-abstract / full-text / QA / included | 流程枚举 | 不适用需说明 | PRISMA 分母 | 透明性证据 | Fig. 1 | 非领域 finding |
| L3 | 排除理由 | selection_flow | IC/EC + Fig. 1 | 排除代码 | EC1--EC5 / ~IC1 | 完整枚举 | 未排除则空 | 排除统计 | scope gate | §3.1.1, Fig. 1 | 可迁移为 protocol 字段 |
| L4 | QA criterion | quality_assessment | Table 2 | 经验研究质量标准 | QA1--QA11 | 完整枚举 | 未评估则 blocked | 质量门控 | 证据强度 | Table 2 | 需补 per-study score |
| L5 | QA score | quality_assessment | §3.3 | 每项质量分 | 0--4 | 数值区间 | supplement 未核验 | eligibility | 证据加权 | §3.3 | 本地无逐项分数 |
| L6 | publication year | RQ0_landscape | Fig. 2 | 发表年份 | 2014--2025-Jan 图示；主要 2014--2024 | 数值/年份 | 未报告则待核验 | 时间趋势 | temporal drift | Fig. 2 | 年份需正式元数据复核 |
| L7 | venue focus | RQ0_landscape | Table 3 | venue 研究社区分类 | SE/CS、HCI、IS/Decision、Human-aspects、AI for Software、SE Education | 层级枚举 | venue 未分类则待核验 | 社区分布 | 研究社区缺口 | Table 3 | 不迁移具体比例 |
| L8 | LLM tool | RQ0_landscape | Table 4 | study 使用/评价的 LLM assistant | ChatGPT、Copilot、Tabnine、GPT-4 等 | 枚举，可扩展 | 未说明则 not_reported | 工具频次 | 工具覆盖缺口 | Table 4 | 工具生态漂移快 |
| L9 | empirical strategy | RQ1_methodology | Table 5 | Stol & Fitzgerald taxonomy | field study / field experiment / experimental simulation / laboratory experiment / sample study / judgment study | 完整枚举 | 无法判定则待核验 | 方法分布 | 证据生态风险 | Table 5 | 可迁移 taxonomy 口径 |
| L10 | procedure | RQ1_methodology | Table 6 | 具体研究方法 | survey / user experiment / concept implementation / interview / case study | 多值枚举 | 未用则空 | 方法组合 | mixed-method 启发 | Table 6, Fig. 4 | 不当作质量高低 |
| L11 | objective | RQ1_methodology | §5.2 | 研究目标类型 | formative / summative | 二值枚举 | supplement 待核验 | 研究成熟度 | 证据阶段判断 | §5.2 | 需 per-study 表 |
| L12 | analysis type | RQ1_methodology | §5.2 | 数据分析类型 | qualitative / quantitative / both | 枚举 | 待核验 | 方法统计 | 可比性风险 | §5.2 | 需 per-study 表 |
| L13 | instrument origin | RQ1_methodology | Table 7 | 工具来源 | author-designed / validated instrument / validated framework | 层级枚举 | 未说明则 not_reported | 评价可信度 | 标准化缺口 | Table 7 | 不等价于质量分 |
| L14 | productivity metric | RQ1_methodology | Table 7, §5.3 | 生产力测量指标 | time、acceptance rate、logs、code quality、productivity gain 等 | 层级枚举 | 未量化则空 | 指标分布 | 指标标准化缺口 | Table 7 | 指标不可混算 |
| L15 | benefit theme | RQ2_effect_theme | Table 8 | 正向影响主题 | accelerate、minimize search、automate、knowledge、code-adjacent、initiation、quality、debugging | 完整枚举 | 未报告则空 | 主题频次 | 候选 benefit | Table 8, Fig. 6 | 领域结论不可迁移 |
| L16 | risk theme | RQ2_effect_theme | Table 9 | 负向影响主题 | requirements failure、over-reliance、quality limit、flow disruption、reduced collaboration | 完整枚举 | 未报告则空 | 风险频次 | 候选 risk | Table 9, Fig. 6 | 领域结论不可迁移 |
| L17 | SPACE dimension | RQ3_SPACE_mapping | Table 10 | 生产力主维度 | Satisfaction / Performance / Activity / Communication / Efficiency | 完整枚举 | 未映射则空 | 维度覆盖 | underexplored dimensions | Table 10 | SPACE 不可泛化替代 Paper2 元模型 |
| L18 | SPACE sub-dimension | RQ3_SPACE_mapping | Table 10 | 细分生产力概念 | developer experience、trust、quality、impact、human-LLM collaboration 等 | 层级枚举 | 无细分则按父维 | 细粒度覆盖 | gap 发现 | Table 10 | emergent 项需核验 |
| L19 | quality metric type | RQ3_SPACE_mapping | Table 11 | code quality 指标类型 | unit tests、correctness、smells、BLEU、complexity、defects、coverage 等 | 完整枚举 | 未测质量则空 | 指标分布 | code quality contested | Table 11 | 不可跨指标直接比较 |
| L20 | Tetrad category | discussion_synthesis | Fig. 9, §8 | 解释性 socio-technical 分类 | enhance / reverse / obsolesce / retrieve | 完整枚举 | 非 discussion 则不适用 | 不进主统计 | 解释框架 seed | Fig. 9 | 不是原始抽取字段 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | record | comes_from | database | 六数据库 | 非数据库来源标 snowball | Table 1, Fig. 1 | 检索分母 |
| E2 | record/report | excluded_by | exclusion_code | EC1--EC5 / ~IC1 / QA fail | included 则空 | Fig. 1, §3.1.1 | 排除透明性 |
| E3 | report | assessed_by | QA criterion / score | QA1--QA11, 0--4 | 未进 QA 则不适用 | Table 2 | eligibility gate |
| E4 | primary study | uses_tool | LLM_tool | Table 4 工具枚举 | 未说明则 not_reported | Table 4 | 工具分布 |
| E5 | primary study | classified_as | empirical_strategy | Table 5 枚举 | 无法判定则待核验 | Table 5 | 方法策略统计 |
| E6 | primary study | uses_procedure | procedure | Table 6 多值 | 无该方法则空 | Table 6, Fig. 4 | 方法组合 |
| E7 | primary study | measured_by | instrument / metric | Table 7 层级 | 未报告则 not_reported | Table 7 | 评价设计 |
| E8 | primary study | reports_theme | benefit/risk theme | Table 8--9 枚举 | 未报告则空 | Table 8--9 | effect synthesis |
| E9 | primary study | maps_to | SPACE dimension/subdimension | Table 10 层级 | 未映射则空 | Table 10, Fig. 8 | 维度覆盖 |
| E10 | quality metric | instantiates | Performance/quality | Table 11 指标 | 未测质量则空 | Table 11 | code quality 争议边界 |
| E11 | result theme | interpreted_by | McLuhan Tetrad | enhance/reverse/obsolesce/retrieve | discussion 外不适用 | Fig. 9, §8 | 候选解释，不作因果边 |

未发现严格的因果型 schema；原文的“impact”多为跨研究主题综合和 reported effects，不应把关系边解释为统一因果估计。

### 6. 统计观察、候选 finding 与 final finding 边界

字段 / 统计表支持的统计观察：

| 观察 | 支撑 | 强度 |
|---|---|---|
| 最终样本为 39 篇 primary studies | Fig. 1, §3.2, §3.3 | strong |
| Laboratory experiment 是最多的 strategy，15/39 | Table 5 | strong |
| Survey 是最常见 procedure，32/39 | Table 6 | strong |
| mixed-method designs 占 27/39 | §5.2 | medium，需 supplement per-study 表核验 |
| time to completion 是最常用 performance metric，12/39 | §5.3.1 | strong |
| Satisfaction、Performance、Efficiency 是最常覆盖 SPACE 维度 | Table 10, RQ3 summary | strong |
| Communication、Activity 覆盖较少 | Table 10, RQ3 summary | strong |
| code quality 同时作为 benefit 与 risk 出现 | Table 8--9, §6.2.4 | strong |

Discussion / recommendation 提出的候选 finding：

| 候选 finding | 使用边界 |
|---|---|
| LLM-assistants 适合 well-scoped / repetitive activities | 只能作为本文领域候选结论 |
| 过度依赖可能削弱 reflective practice 与团队协作 | 只能迁移为“需要记录反向证据”的方法启发 |
| 研究需要 longitudinal / field / team-based designs | 可迁移为 Paper2 文献综述方法学启发 |
| 需要 standardized metrics / validated instruments | 可迁移为 schema 设计启发 |

对 Paper2 可迁移的方法学启发：多分母筛选链、QA 门控、per-study extraction form、多轮 thematic analysis、外部 framework + emergent sub-dimensions、contested theme 记录、summary 绑定统计证据。

绝不能迁移的领域结论：ChatGPT / Copilot 的具体频次、LLM-assistants 是否提升开发速度、是否减少搜索、是否降低团队协作、code quality 的方向性结论。这些都属于该综述的目标领域，不是 Paper2 的目标领域证据。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 建议 |
|---|---|
| C | 重写“维度树复原”：当前仍把六个通用 leaf 放在显著位置，虽然有校准说明，但 v2 应直接以 primary study 为根对象，展开原文维度森林；六叶只能放到“跨论文投影”附录。 |
| C | 修正“主统计池资格”：本文有系统检索、纳排、QA 和 39 篇 primary study 编码，应标为可进入主统计池；但应限定为原生 schema / 统计观察，不迁移领域结论。 |
| I | 删除或隔离 v1 / 19×3 历史审计引用。现有 `review.md` 仍大量提到 v1-deprecated、19×3、A2a seed，容易让主线程误把旧审计当事实源。 |
| I | 叶子表需改为原文字段：selection flow、QA、publication year、venue focus、LLM tool、strategy、procedure、objective、analysis type、instrument origin、metric、benefit theme、risk theme、SPACE dimension/subdimension、quality metric、Tetrad category。 |
| I | A.2 证据账本应从泛化 EV-001--005 改成具体证据行，绑定 Table/Fig/section；证据强度不应全部 `not_verified`，Table 1、Fig. 1、Table 2、Table 5--11 可升为 text+PDF-layout verified。 |
| I | A.3 结论映射要区分统计观察、schema seed、candidate finding、migration boundary；不要把 discussion recommendations 写成 final finding。 |
| M | metadata 与 paper text 存在年份/版本痕迹差异：BibTeX / metadata 为 TOSEM 2026，paper text ACM reference 仍带 manuscript / placeholder 痕迹；引用时按 DOI/metadata，正文注明 arXiv PDF 来源。 |
| M | Zenodo replication package 仅记录为作者声明，未本地核验；`review.md` 不应写成 package 内容已验证。 |
| M | SUMMARY 当前字段建议：样本单位改为“39 primary studies”；样本数量改为“39 final included; 44 QA assessed; 9,756 initial records”；原生树类型改为“维度森林”；统计池资格改为“是，领域结论不可迁移”。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV01 | paper_content.txt / paper.pdf | Abstract, §1 | 摘要、贡献列表 | 研究综合 39 篇 peer-reviewed studies | root/sample | strong | 样本单位、综述类型 | 否 | 不迁移领域结论 |
| EV02 | paper_content.txt / paper.pdf | §3 | RQ0--RQ3 | 四个 RQ 对应 landscape、method、impact、SPACE mapping | rq_structure | strong | 维度森林主干 | 否 | RQ 不是样本单位 |
| EV03 | paper_content.txt / paper.pdf | §3.1.1 | Table 1 | 六数据库、搜索式、初检 9,756 | selection_schema | strong | 检索字段 | 否 | 搜索式不可直接复用 |
| EV04 | paper_content.txt / paper.pdf | §3.2 | Fig. 1 | 去重、筛选、全文、snowballing、QA、最终 39 | selection_flow | strong | 分母链 | 部分：图像版式 | 仅流程统计 |
| EV05 | paper_content.txt / paper.pdf | §3.3 | Table 2 | QA1--QA11、0--4、50% threshold | quality_schema | strong | QA 叶子 | 否 | per-study 分数在 supplement |
| EV06 | paper_content.txt | §3.4 | Data Extraction and Synthesis | 抽取 goals/tools/strategy/tasks/settings/key results，多轮 thematic analysis | extraction_schema | medium | 抽取字段来源 | 否 | extraction form 未核验 |
| EV07 | paper_content.txt | §4 | Table 3--4 | venue focus 与 LLM tools 分布 | landscape_schema | strong | RQ0 叶子 | 否 | 工具生态时间敏感 |
| EV08 | paper_content.txt | §5 | Table 5--7 | strategy、procedure、instrument / metric 分类 | methodology_schema | strong | RQ1 叶子 | 否 | taxonomy 适配需说明 |
| EV09 | paper_content.txt | §6 | Table 8--9, Fig. 6 | 八类 benefit、五类 risk；code quality 为 contested theme | effect_schema | strong | RQ2 叶子 | 是：Fig. 6 频次 | 不迁移领域 finding |
| EV10 | paper_content.txt / paper.pdf | §7 | Table 10--11, Fig. 7--8 | SPACE 主维与 sub-dimensions、quality metrics | framework_mapping | strong | RQ3 叶子 | 部分：Fig. 8 overlap | SPACE 不替代 Paper2 元模型 |
| EV11 | paper_content.txt / paper.pdf | §8 | Fig. 9 | Tetrad 用于 enhance/reverse/obsolesce/retrieve 解释 | discussion_lens | medium | candidate finding | 部分 | 非原始编码字段 |
| EV12 | paper_content.txt | §9 | Threats to Validity | selection bias、classification rigor、formative/lab evidence、temporal relevance | limitation | strong | 迁移边界 | 否 | 只支持风险降级 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C01 | 本文是 SLR + SMS，不是 roadmap / guideline / tertiary review | paper_type | 审计结论卡片 | EV01, EV02, EV03, EV04 | strong | SUMMARY 类型字段 | metadata 与 arXiv 版本需区分 |
| C02 | 主要被编码样本单位是 final included primary study | sample_unit | 维度树 root | EV01, EV04, EV06 | strong | A1-DT 样本单位字段 | selection flow 有辅助 record/report 单位 |
| C03 | 本文可进入主统计池，但只限原生 schema / 统计观察 | eligibility | 主统计池资格 | EV03--EV10 | strong | SUMMARY 统计池字段 | 领域结论不可迁移 |
| C04 | 原生树应复原为维度森林，而非六叶通用模板 | tree_type | 维度树复原 | EV02, EV06--EV10 | strong | 重写 `review.md` | 六叶可作投影附录 |
| C05 | RQ1 的方法分类树是本文最强 schema seed 之一 | schema_seed | RQ1_methodology | EV08 | strong | Paper2 方法字段设计 | taxonomy 需说明来源 |
| C06 | RQ2 benefit/risk 是主题树，不能升级为 Paper2 final finding | migration_boundary | RQ2_effect_theme | EV09, EV12 | strong | 候选 finding 边界 | 只可迁移 contested-theme 写法 |
| C07 | SPACE mapping 是外部框架 + emergent subdimension 的实例 | schema_pattern | RQ3_SPACE_mapping | EV10 | strong | 元模型设计启发 | SPACE 领域绑定 productivity |
| C08 | McLuhan Tetrad 是 discussion 解释框架，不是 primary-study extraction schema | boundary | discussion_synthesis | EV11 | medium | 候选解释框架 | 不应用于主统计频次 |
| C09 | 现有 `review.md` 需要返修，核心问题是原生树与通用投影混层 | repair | review.md | EV02, EV06--EV10 + review.md 现状 | strong | 返修计划 | 不代表原文质量问题 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南：

| 文件 | 采用原则 |
|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | claim-evidence workflow；无证据则降级；review 任务优先指出风险 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | 关注 soundness、clarity、reproducibility、claim support |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | 用 reviewer 视角区分 major risks、claim/evidence gaps、revision priorities |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 先理解研究上下文，再输出结构化、可执行 schema |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | 不补造缺失配置；不清楚处显式标注 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | 用结构化字段、任务、风险组织输出 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 完成必须 artifact-gated；不能因“看起来完成”而省略验证记录 |

最高风险 3 点：

1. Fig. 6 和 Fig. 8 的图形频次未做像素级核验；合并时应用 PDF 视觉核对或 replication package 数据表复查。
2. supplement / Zenodo replication package 未下载，因此 per-study extraction form、QA scores、selection decisions 只能标为作者声明或待核验。
3. 本输出给出了较完整原生 schema，但仍基于 paper text + 局部 PDF layout；主线程若要写入 `review.md`，应将每个叶子补成精确 page/table/figure 证据。

blocked / timeout / 文件缺失：未出现。没有修改文件、没有 commit、没有 push、没有启动 subagent。