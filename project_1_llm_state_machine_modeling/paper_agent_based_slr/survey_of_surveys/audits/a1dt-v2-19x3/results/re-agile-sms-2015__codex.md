### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-agile-sms-2015` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是。已按全文顺序读取 9 页提取文本，覆盖摘要、引言、背景、方法、结果、讨论、限制、结论和 primary sources。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。已读取并用于核对标题、作者、年份、DOI、venue、review type 和本地状态。 |
| 是否打开或核对 `paper.pdf` | 是。使用 `pdfinfo` 核对 PDF 元数据和 9 页页数；使用 `pdftotext -layout -f 3 -l 6` 核对方法段与表 I--V 的 PDF 版面文本。未做截图式人工视觉核验。 |
| 原文类型 | SMS / systematic mapping study。 |
| 被编码样本单位 | 纳入的 28 篇 primary articles / primary studies，即文中 `[S1]`--`[S28]`。 |
| 样本数量 / 分母 | Scopus 初检 241；去除非 journal/conference 46、非英语 8 后标题摘要筛 187；排除 123 后全文候选 65；全文排除 37；最终纳入 28。 |
| 原生树类型 | 维度森林。核心为“纳入论文 metadata/context/methods/results 抽取”加“benefit/problem/solution 主题编码”和若干 article-level 分类表。 |
| 主统计池资格 | 局部可统计。28 篇样本、纳排链、Table I--V 的分类和多对多 article-code 关系可统计；discussion 中领域解释与未来研究建议只能作候选 finding。 |
| 总体判定 | needs repair。论文原文证据充分，但现有 `review.md` 仍以通用六叶投影开头，A.2/A.3 证据锚点过泛，需要按原生维度森林返修。 |

### 1. 原文证据阅读说明

实际读取文件：

- 技能 / 指南：任务指定的 7 个技能文件均已先读。
- 论文材料：[bibtex.bib](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/re-agile-sms-2015/bibtex.bib)、[metadata.json](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/re-agile-sms-2015/metadata.json)、[paper_content.txt](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/re-agile-sms-2015/paper_content.txt)、[review.md](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/re-agile-sms-2015/review.md)。
- PDF 核验：[paper.pdf](/home/zhangshaoang/oo-projects/research_ideas-2/project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/papers/re-agile-sms-2015/paper.pdf)。核验了 PDF 元数据、总页数、方法页和表格页的 layout text；未做图片截图核验。

关键原文证据锚点：

1. 摘要：作者说明纳入 28 篇文章，并概括定义模糊、benefits、problems、solutions。
2. Section I：列出 3 个研究问题，分别问研究了什么、关键 benefit、problem 及 solution。
3. Section III：说明研究类型为 mapping study，检索源为 Scopus，检索时间为 2014 年 9 月。
4. Section III：给出检索式、241 初检、标题摘要筛和全文筛的分母链。
5. Section III：说明对 28 篇提取 article metadata、context、methods、results。
6. Section III：说明 results 被分为四个主题区：定义、benefit、problem、solution。
7. Table I：按 publication venue type / venue 统计 28 篇样本。
8. Table II：按 agile method context 编码样本：unspecified agile、Scrum、FDD。
9. Table III：按 article type 编码样本：case study、experience report、evaluation、proposal、position paper 等。
10. Table IV：用 B1--B6 给出 agile RE benefits 与相关文章列表。
11. Table V：用 P1--P6 给出 problem themes 与相关文章列表。
12. Section V.D：限制说明检索只用 Scopus，且检索词较小；这是统计外推边界。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 28 篇关于 agile requirements engineering 的 primary articles。作者在结果中用 `[S1]`--`[S28]` 引用这些样本，并在表 II、表 III、表 IV、表 V 中把文章映射到 context、article type、benefit code 和 problem code。

2. 作者有系统检索、纳排、数据抽取和编码方案。检索源为 Scopus；有标题摘要阶段和全文阶段排除标准；最终对 28 篇提取 metadata、context、methods、results；再把 results 分类到定义、benefit、problem、solution 四个主题区。

3. 原文字段来源不是独立 appendix 或 replication package，而是 Section III 的 extraction 描述、Section IV 的分类表和 narrative synthesis。可确认字段包括：metadata、context、methods、results；publication venue type / venue；agile method context；article type；benefit code；problem code；problem-to-solution narrative relation。

4. RQ 不是维度树树根本身，而是字段用途和结果组织方式。RQ1 驱动 overview/context/type/definition 叙述；RQ2 驱动 B1--B6 benefit 编码；RQ3 驱动 P1--P6 problem 编码与 solution mapping。

5. 本文不是 roadmap / vision / proposal，也不是无系统样本库。无需降级为 boundary anchor；但由于作者没有公开完整 extraction form，除表 I--V 与明确 narrative relation 外，更细的 per-article metadata/context/method/results 字段应标为 `schema_seed` 或 `not_verified`。

### 3. 原生样本编码维度树 / 维度森林

```text
Root: 28 included primary articles [S1]--[S28]
├── Corpus / Selection Meta-Flow
│   ├── database: Scopus
│   ├── search date: 2014-09
│   ├── candidate count chain: 241 -> 187 -> 65 -> 28
│   └── exclusion criteria: title/abstract stage + full-text stage
├── Extracted Per-Article Record
│   ├── article metadata
│   ├── context
│   ├── methods
│   └── results
├── Publication / Context Classification
│   ├── publication venue type and venue name
│   ├── agile method context
│   └── article type
├── Result Theme Classification
│   ├── definition of RE in agile context
│   ├── benefits identified in agile RE
│   │   └── B1--B6 benefit codes, each linked to source articles
│   ├── problems identified in agile RE
│   │   └── P1--P6 problem codes, each linked to source articles
│   └── solutions proposed for problems
│       ├── problem-linked solution descriptions
│       └── explicit no-solution observations for P3, P4, P6
└── Discussion / Synthesis Layer
    ├── proposed agile RE definition
    ├── venue/context/type interpretation
    ├── benefit-problem-solution interpretation
    ├── research gaps
    └── limitations of search and generalization
```

取值空间说明：

- `publication venue type`、`agile method context`、`article type`、`benefit code`、`problem code` 是本文内封闭枚举。
- `venue name` 是表内枚举，但不是理论 taxonomy。
- `solution descriptions` 是 problem-linked 自由文本 / 关系值，不是完整封闭 taxonomy。
- `metadata/context/methods/results` 是 extraction top-level 字段；原文没有公开完整表单，不能向下脑补。
- `definition` 和 `research gaps` 是综合性 narrative synthesis，不应当按 per-article closed code 处理。

A2a 精核任务：若要升级为正式统计字段，应逐项补表 I--V 的 PDF 页码、表号、article-code membership、是否作者显式报告 N、以及 solution relation 是否只来自 narrative 段落。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 数据库 | Corpus / Selection Meta-Flow | Section III 方法 | 检索使用的文献数据库 | Scopus | 完整枚举 / 单值 | 不适用；仅使用一个库 | 支撑分母来源 | 检索覆盖风险 | Section III；Limitations | 不迁移“Scopus 足够”判断 |
| L2 | 检索日期 | Corpus / Selection Meta-Flow | Section III 方法 | 实际执行检索的时间 | 2014-09 | 时间值 | 缺失会影响复现；本文已给出 | 复现窗口 | 版本漂移风险 | Section III | 不外推到当前文献状态 |
| L3 | 纳排分母链 | Corpus / Selection Meta-Flow | Section III 方法 | 从初检到最终纳入的数量链 | 241、187、65、28 等 | 数值链 / 区间阶段 | 阶段不明会阻断统计；本文阶段较清楚 | 样本池资格 | 检索严格性评估 | Section III | 只说明本文筛选过程 |
| L4 | 排除标准 | Corpus / Selection Meta-Flow | Section III 方法 | 标题摘要和全文阶段排除原因 | 无 abstract、非研究文章、非 SE、非 agile RE、predatory/vanity、无全文、冗余、主题不符 | 层级枚举 | 未命中标准不等于质量高，只是通过筛选 | 复核纳排 | 方法学 seed | Section III | 不替代质量评价 rubric |
| L5 | 抽取顶层字段 | Extracted Per-Article Record | Section III 数据抽取描述 | 作者对 28 篇提取的字段族 | metadata、context、methods、results | 完整枚举 / 顶层字段 | 子字段未公开；不能补全 | schema seed | 设计 Paper2 extraction form | Section III | 只能迁移顶层结构 |
| L6 | publication venue type | Publication / Context Classification | Table I | 样本发表形态分类 | conference proceedings、journal、magazine | 完整枚举 | 未发现缺失；聚合表不列每篇完整元数据 | 描述统计 | 判断研究分散性 | Table I；Discussion V.A | 不迁移 venue 重要性结论 |
| L7 | venue name | Publication / Context Classification | Table I | 具体发表 venue | AREW、RE、IEEE Software 等表内名称 | 完整枚举 / 表内列表 | 不适用；按表聚合 | venue 分布 | “无主要 venue”候选观察 | Table I；Discussion V.A | 不用于 CCF/质量推断 |
| L8 | agile method context | Publication / Context Classification | Table II | 每篇文章讨论的 agile 方法语境 | unspecified agile、Scrum、FDD | 完整枚举 | `unspecified agile` 是显式类别，不是普通空值 | context 分布 | 语境报告不足 | Table II；Discussion V.A | 不说明方法实际使用比例 |
| L9 | article type | Publication / Context Classification | Table III | 每篇样本研究类型 / 文章类型 | multiple case study、single case study、experience report、tool evaluation、method evaluation、method proposal、position paper | 完整枚举 | 无缺失；但分类标准细节未展开 | evidence-type 分布 | 证据强度候选判断 | Table III；Discussion V.A | 不等于正式 quality score |
| L10 | result subject area | Result Theme Classification | Section III 结果分类 | results 被归入的主题区 | agile RE definition、benefits、problems、solutions | 完整枚举 / 主干分类 | 未覆盖的结果可能未进入本文分析 | 结果组织 | Paper2 主题编码 seed | Section III | 主题名需按目标领域重建 |
| L11 | benefit code | Benefits | Table IV + Section IV.C | agile RE benefit 主题代码 | B1--B6 | 完整枚举 | 某文章不在某 benefit 下表示未被作者归为该 benefit | benefit-code 频次 / membership | 候选 positive finding | Table IV | 不迁移具体 agile RE benefit |
| L12 | benefit-to-article membership | Benefits | Table IV | benefit code 与支持文章的多对多关系 | B code -> `[Sx]` 列表 | 关系值 | 无文章则无支持；本文所有 B1--B6 均有文章 | 支持数可复算 | 证据覆盖 | Table IV | 不能当作效果量 |
| L13 | problem code | Problems | Table V + Section IV.D | agile RE problem theme 代码 | P1--P6 | 完整枚举 | 某文章不在某 problem 下表示未被作者归类 | problem-code 频次 / membership | gap seed | Table V | 不迁移具体问题结论 |
| L14 | problem-to-article membership | Problems | Table V | problem code 与相关文章的多对多关系 | P code -> `[Sx]` 列表 | 关系值 | 无文章则无支持；本文 P1--P6 均有文章 | 支持数可复算 | evidence coverage | Table V | 不能当作严重性排序 |
| L15 | problem-linked solution | Solutions | Section IV.D narrative | 针对 P1--P6 的方案叙述 | 角色补充、文档、mind-mapping、storytests、ATDD、delivery stories、hierarchical model、traceability 等 | 自由文本加关系值 | 无 solution 是有意义缺失；P3/P4/P6 明确无方案 | problem-solution coverage | “方案空白”候选 finding | Section IV.D；Discussion V.C | solution taxonomy 未封闭 |
| L16 | no-solution marker | Solutions | Section IV.D narrative | 作者明确指出某些 problem 未有 solution | P3、P4、P6 no solution；P5 one solution | 布尔 / 关系值 | `true` 表示原文明确缺口，不是抽取失败 | gap 统计 | research gap seed | Section IV.D；Discussion V.C | 不等于该领域今天仍无方案 |
| L17 | proposed agile RE definition | Discussion / Synthesis | Section V.B | 作者基于样本综合提出的定义 | 自由文本定义 | 自由文本加理由 | 无通用定义是作者 finding，不是字段空值 | 不宜主统计 | boundary / definition seed | Section V.B | 不迁移到其他领域定义 |
| L18 | limitation marker | Discussion / Synthesis | Section V.D | 作者说明检索和外推限制 | Scopus-only、小关键词集等 | 自由文本 / 风险项 | 未报告质量评价不应补写 | 风险标注 | 降级依据 | Section V.D | 不支撑强泛化 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| E1 | candidate record | filtered_by | exclusion criterion / screening stage | 标题摘要阶段、全文阶段及对应排除标准 | 不适用；这是纳排流程边 | Section III | 复原分母链 |
| E2 | included article `[Sx]` | has_context | agile method context | unspecified agile、Scrum、FDD | `unspecified agile` 是显式类别 | Table II | context 统计 |
| E3 | included article `[Sx]` | has_article_type | article type | 7 类 article type | 未发现缺失 | Table III | evidence-type 统计 |
| E4 | venue type | contains_venue | venue name + count | conference/journal/magazine 下的 venue 列表 | 不适用 | Table I | publication 分布 |
| E5 | included article `[Sx]` | supports_benefit | benefit code | B1--B6 | 未列入表示未被归为该 benefit | Table IV | benefit membership / coverage |
| E6 | included article `[Sx]` | supports_problem | problem code | P1--P6 | 未列入表示未被归为该 problem | Table V | problem membership / coverage |
| E7 | problem code | has_solution | solution description | 针对 P1、P2、P5 的 narrative solution 项 | solution 未封闭，不能补全为 taxonomy | Section IV.D | problem-solution relation |
| E8 | problem code | has_no_reported_solution | no-solution marker | P3、P4、P6 | 这是作者明确缺口，不是 missing data | Section IV.D；Discussion V.C | gap candidate |
| E9 | article type distribution | informs | evidence strength discussion | empirical part、method proposal、position paper 等解释 | 不是质量评分 | Section V.A | 候选 evidence-risk |
| E10 | limitation marker | constrains | statistical generalization | Scopus-only、keyword scope | 不是反证，但限制外推 | Section V.D | 迁移边界 |

本文有显式关系型 schema，尤其是 article-to-code membership 与 problem-to-solution / no-solution 边。最应保留的是 E5--E8，因为它们体现 SMS 的原生统计和 gap 形成路径。

### 6. 统计观察、候选 finding 与 final finding 边界

原文中由字段 / 统计表支持的统计观察：

- 最终样本为 28 篇，分母链清楚，支持 SMS 样本池资格。
- Table I 支持 publication venue 分布；作者据此讨论 RE in ASD 没有明显主 venue。
- Table II 支持 agile method context 分布；`unspecified agile` 是最大类。
- Table III 支持 article type 分布；method proposal、case study、experience report、evaluation、position paper 等构成证据类型图谱。
- Table IV 支持 B1--B6 benefit 主题和 source article membership。
- Table V 支持 P1--P6 problem theme 和 source article membership。
- Section IV.D / V.C 支持 problem-to-solution 关系，其中 P3、P4、P6 被作者明确指出无 proposed solutions。

原文 discussion / recommendation / roadmap 提出的候选 finding：

- agile RE 定义模糊，作者提出一个综合性定义。
- 复杂、大型软件和大型组织语境下，customer representative、user story、prioritization、technical debt、tacit knowledge、estimation 等问题较突出。
- solutions 更集中在 P1 和 P2；P3/P4/P6 的 solution gap 更明显。
- 许多 proposed methods 的 empirical evaluation 较弱，需要更多评价研究。

对 Paper2 可迁移的方法学启发：

- 可迁移“样本文章 -> context/type -> thematic code -> source article membership”的 SMS 编码模式。
- 可迁移“problem theme -> proposed solution -> no-solution marker -> research gap”的关系边。
- 可迁移对 extraction top-level fields 的设计：metadata、context、methods、results。
- 可迁移分母链和限制字段的显式记录方式。

绝不能迁移的领域结论：

- 不能把 agile RE 的 B1--B6、P1--P6 直接作为 LLM 状态机建模领域 taxonomy。
- 不能把 2014 年前 Scopus 样本的比例外推到当前研究格局。
- 不能把 article type 分布当作质量评价或效果证据。
- 不能把 proposed solutions 当作已验证有效的方法。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 返修建议 | 理由 |
|---|---|---|
| C | 重写“维度树复原”的主入口，把原文维度森林放在最前；通用六叶只能作为跨论文投影附录。 | 当前 `review.md` 仍先展示 scope/corpus/taxonomy/method/evidence/finding 六叶，容易违反 A1-DT v2“不要用通用模板替代原文树”。 |
| C | 统一“主统计池资格 / 是否目标证据池”口径。建议写“局部可统计：Table I--V 与 28 篇分母可统计；领域 finding 仅 candidate”。 | `metadata.json` 标为 eligible for statistical synthesis，但 `review.md` 快速卡片写“是否目标证据池：否”，容易让 SUMMARY 误判。 |
| C | A.2 证据账本必须从泛化占位改为具体证据：RQ、Scopus 检索、分母链、extraction fields、Table I--V、solution/no-solution、limitations。 | 当前 EV-002/003 等仍是“方法/结果页待核验”泛称，不足以支撑可审计返修。 |
| I | 新增关系边表，至少覆盖 article->context、article->article type、article->benefit、article->problem、problem->solution、problem->no_solution。 | 本文最有价值的原生 schema 是多对多 membership 与 problem-solution relation，不应只列主题叶子。 |
| I | 把 `validity / threat pattern` 从“未定位完整 threat section”改为“有 Limitations section，但没有质量评价 rubric”。 | 原文 Section V.D 明确存在 limitations；旧说法会误导。 |
| I | 对 benefit/problem 的取值空间标为“本文内封闭枚举”，对 solution 标为“problem-linked 自由文本 / 关系值，非封闭 taxonomy”。 | 这能防止 A2a 把 solution narrative 错当完整分类表。 |
| M | 在 A.4 中把 PDF 核验状态细分：已做 PDF text-layout 核验页 3--6；若需要精确截图/页内位置，再做人工视觉核验。 | 当前只写 `needs_manual_check`，不能反映已有核验程度。 |
| M | SUMMARY 若有字段“样本单位 / 样本数量 / 原生树类型 / 统计池资格”，建议修为：样本单位 `primary articles [S1]--[S28]`；数量 `28`；原生树类型 `维度森林`；统计池资格 `局部可统计`。 | 与 A1-DT v2 口径更一致。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV1 | `bibtex.bib`, `metadata.json` | 元数据 | BibTeX 与 JSON 记录 | 题名、作者、年份、DOI、SEAA 2015、review_type=SMS | 元信息核验 | strong | paper slug、类型、venue | 否 | 不支撑原文 schema |
| EV2 | `paper_content.txt`, `paper.pdf` | Abstract | 摘要开头和结果概述 | 作者说明纳入 28 篇，并概括 definition、benefits、problems、solutions | SMS 样本与主题总览 | strong | 样本单位、结果主题 | 否；PDF 页数已核 | 摘要不能替代表格字段 |
| EV3 | `paper_content.txt` | Section I | 三个编号 RQ | RQ 分别指向研究概况、benefits、problems/solutions | RQ 到字段用途 | strong | RQ-field mapping | 否 | RQ 不是树根模板 |
| EV4 | `paper_content.txt`, PDF layout | Section III | methodology 首段 | 研究被定义为 mapping study，适合广域概览 | 原文类型 | strong | SMS 类型、统计池资格 | 否 | 不等于效果型 SLR |
| EV5 | `paper_content.txt`, PDF layout | Section III | Scopus、检索式、筛选数量 | 241 初检，经标题摘要和全文筛后纳入 28 | 分母链 | strong | Corpus / Selection Meta-Flow | 否 | Scopus-only 限制仍存在 |
| EV6 | `paper_content.txt`, PDF layout | Section III | data extraction 段 | 提取 metadata、context、methods、results；results 分为四个主题区 | extraction schema | strong | L5、L10 | 否 | 子字段未公开 |
| EV7 | `paper_content.txt`, PDF layout | Section IV.A / Table I | publication venues | 按 conference、journal、magazine 和 venue 名统计 | publication 分类 | strong | L6、L7、E4 | 表 I 已用 layout text 核对；最终页码可补 | 不代表 venue 质量 |
| EV8 | `paper_content.txt`, PDF layout | Section IV.A / Table II | agile method contexts | 28 篇映射到 unspecified agile、Scrum、FDD | context 分类 | strong | L8、E2 | 表 II 已 layout 核对 | `unspecified` 不等于真实无方法 |
| EV9 | `paper_content.txt`, PDF layout | Section IV.A / Table III | article types | 7 类 article type 与文章列表 | evidence-type 分类 | strong | L9、E3 | 表 III 已 layout 核对 | 不等于 quality score |
| EV10 | `paper_content.txt`, PDF layout | Section IV.C / Table IV | benefit codes | B1--B6 与相关文章列表 | benefit taxonomy | strong | L11、L12、E5 | 表 IV 已 layout 核对 | 不代表因果效果 |
| EV11 | `paper_content.txt`, PDF layout | Section IV.D / Table V | problem codes | P1--P6 与相关文章列表 | problem taxonomy | strong | L13、L14、E6 | 表 V 已 layout 核对 | 不代表严重性排序 |
| EV12 | `paper_content.txt`, PDF layout | Section IV.D / V.C | solution narrative | P1/P2/P5 有方案叙述；P3/P4/P6 明确无方案 | problem-solution relation | medium-high | L15、L16、E7、E8 | 已核对 layout text；solution 仍需逐句页码 | solution 不是封闭枚举 |
| EV13 | `paper_content.txt` | Section V.B | definition discussion | 作者认为 agile RE 无通用定义，并提出综合定义 | synthesis / definition | medium | L17 | 否 | 不能当 per-article field |
| EV14 | `paper_content.txt` | Section V.D | limitations | 检索限于 Scopus，关键词集合较小 | 外推边界 | strong | L18、E10 | 否 | 不证明遗漏文献无影响 |
| EV15 | `review.md` | 维度树复原 | 通用六叶与后补原文主树并存 | 现有 review 仍有 v1 投影残留，且证据多为待核验 | 返修依据 | strong | Section 7 返修建议 | 否 | 审计对象不是原文事实 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C1 | 本文是 SMS / systematic mapping study，不是 tertiary、roadmap 或 proposal。 | 原文类型 | 审计结论卡片 | EV2、EV4 | strong | 元数据、SUMMARY 类型字段 | 不等于效果综合 |
| C2 | 被编码样本单位是 28 篇 primary articles `[S1]`--`[S28]`。 | 样本单位 | Root object | EV2、EV5 | strong | 样本单位字段 | 未公开完整 extraction dataset |
| C3 | 本文有系统检索与纳排链，最终样本分母可复核。 | 统计池资格 | Corpus flow | EV5 | strong | 局部统计池 | Scopus-only 和小关键词限制 |
| C4 | 原生树不是通用六叶单树，而是围绕 per-article extraction、publication/context/type、benefit/problem/solution 的维度森林。 | tree_type | 原生维度树 | EV6--EV12 | strong | 重写 `review.md` 维度树 | solution 子树不是封闭 taxonomy |
| C5 | `metadata/context/methods/results` 是作者显式提到的 extraction 顶层字段。 | leaf_definition | L5 | EV6 | strong | schema seed | 不能补写未公开子字段 |
| C6 | publication venue type、agile method context、article type 是表格化 article-level 分类字段。 | leaf_definition | L6--L9 | EV7--EV9 | strong | 描述统计 | 不等于质量评价 |
| C7 | B1--B6 和 P1--P6 是本文内封闭主题代码，并与 source articles 建立多对多 membership。 | leaf_definition / relation | L11--L14、E5--E6 | EV10、EV11 | strong | 频次 / coverage seed | 不迁移具体领域代码 |
| C8 | solutions 是 problem-linked narrative relation；P3、P4、P6 的 no-solution 是有意义缺失值。 | relation / missingness | L15--L16、E7--E8 | EV12 | medium-high | gap seed | solution 空间未封闭；今日状态未核 |
| C9 | discussion 中“定义模糊”“评价较弱”“需要更多研究”等只能作为 candidate finding。 | candidate finding | Discussion layer | EV13、EV14 | medium | Paper2 方法学启发 | 不能升级为 final research finding |
| C10 | 现有 `review.md` 需要返修：通用接口应降级，A.2/A.3 应替换为具体证据账本。 | audit repair | review.md | EV15、EV6--EV12 | strong | 返修任务 | 不直接修改文件 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence workflow、证据不足则降级、review 任务优先列风险的原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 必须具体、可执行、证据支撑的标准。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用风险分级、自审、claim/evidence gap 和 revision priority 的输出方式。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解研究上下文、明确资源和风险、输出结构化计划/字段的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“不清楚就显式标注，不编造细节”的规划纪律。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用 schema 化拆分、风险字段和可执行任务分解的结构。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 的完成观，即不能因文字上“完成”就停止证据检查；本任务未启动 autoresearch loop 或任何 agent。

本输出最高风险 3 点：

1. PDF 核验是 `pdfinfo` + `pdftotext -layout`，不是截图式人工视觉核验。主线程合并时若要写精确页码、表格位置或版面说明，应打开 PDF 做人工视觉复核。
2. solution schema 来自 narrative 段落，不是表格化封闭 taxonomy。合并时应保留“problem-linked 自由文本 / 关系值”，不要把方案列表扩写成完整分类法。
3. `metadata/context/methods/results` 是作者公开的顶层抽取字段，但完整 extraction form 未公开。合并时不能脑补每个字段的全部子字段和缺失值规则。

blocked / timeout / 文件缺失状态：未出现 blocked、timeout 或文件缺失。未启动 subagent，未修改仓库文件，未 commit、push 或发布评论。