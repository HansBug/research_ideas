### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2015-mapping-guidelines-update` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已通读 18 页提取文本，并按方法、结果、guideline update、appendix 复核 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；题录、DOI、全文状态、既有 eligibility 元数据均已读取 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 核对 18 页，并用 `pdftotext -layout` 核对 Fig.1、Table 3、Table 5、Appendix B 等关键版面；未做图像级人工视觉核验 |
| 原文类型 | SMS / tertiary-like methodological mapping / guideline update |
| 被编码样本单位 | 软件工程 systematic mapping study；最终结果统计分母为 52 篇 included mapping studies |
| 样本数量 / 分母 | 检索 7752；去 2004 年前后 5082；title/abstract 后 60；全文后 43；snowball 后 54；quality 后 44；review excluded 后最终 52。另有 57 作为 quality assessment 前候选集合 |
| 原生树类型 | 维度森林：样本抽取字段森林 + 过程策略分类森林 + quality/rubric 森林 + guideline action 综合树 |
| 主统计池资格 | 局部可统计：可进入 A1 方法学 / survey-of-surveys 统计池；不可作为目标领域效果或 Paper2 final finding 统计证据 |
| 总体判定 | needs repair：原文可审计，当前 `review.md` 仍需按 v2 口径重写原生维度森林和证据账本 |

### 1. 原文证据阅读说明

已读取本地四个指定文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。PDF 侧做了 CLI 版面核验：`pdfinfo` 确认 18 页；`pdftotext -layout` 核对了第 4-5 页方法与 Table 3 / Fig.1、第 9-15 页 Table 5 / guideline update / rubric、第 16-17 页 Appendix B 分类映射表。未对 PDF 图像、气泡图、柱状图做人工视觉截图核验，因此图形精确读数仍应留给 A2a。

关键证据锚点：

1. 摘要：作者声明方法是对 systematic maps 做 systematic mapping，并据此更新 guideline。
2. §3.1：RQ1-RQ4 分别覆盖 guideline 使用、SE topic、发表地点与年份、mapping process 执行方式。
3. §3.2：搜索使用 IEEE Xplore、ACM、Scopus、Inspec/Compendex，并给出 Table 1 / Table 2。
4. §3.3 与 Fig.1：纳排链条最终到 52 篇 included mapping studies，但中间有 57、44 等阶段性分母。
5. §3.4 Table 3：原文 extraction form 是样本编码主入口，字段包括 general 与 process 两组。
6. §3.5：抽取项被制表、可视化，策略由第一作者归组并计数。
7. §3.6：效度框架包括 descriptive validity、theoretical validity、generalizability、interpretive validity、repeatability。
8. §4.4 与 Fig.5-Fig.15：结果按 guideline、study identification、quality evaluation、classification、visualization、validity threats 展开。
9. §5 与 Table 5：作者把既有指南和本研究实践映射成 planning / conducting / reporting guideline update。
10. §5.4 Table 8-14：提出 26 个 action 的评价清单与 rubric，并统计既有 studies 的得分分布。
11. Appendix A：列出 included 与 excluded studies。
12. Appendix B Tables B.15-B.27：给出逐类 studies-to-category 映射，是关系边和取值空间的重要来源。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是软件工程领域的 systematic mapping studies。作者称其为 primary studies，但相对于本 A1 任务，它们是二级研究 / mapping studies 样本。

2. 作者有系统检索、纳排、数据抽取和编码方案。检索源、搜索串、纳排标准、snowball、quality assessment、data extraction form、分析归类流程均有正文描述；缺陷是筛选与 quality assessment 主要由单人执行，作者自己也列为效度威胁。

3. 原文字段来源主要是 Table 3 extraction form、§4.4 的分类与统计图、Appendix B 的 mapping tables、§5 的 guideline comparison / action checklist、Table 9-13 rubric。不是单纯 RQ 列表，也不是综述流程说明。

4. RQ 是字段用途和结果组织方式，不是维度树根本身。真正的根对象应是“included mapping study”，RQ1-RQ4 决定抽取哪些字段和如何组织统计：guidelines、topic、venue/year、process execution。

5. 本文不是无系统样本库的 roadmap / vision；不需降级为 boundary anchor。但其 guideline update finding 只能作为方法学候选启发，不能直接迁移为 Paper2 目标领域结论。

### 3. 原生样本编码维度树 / 维度森林

```text
Root: included SE systematic mapping study, n = 52 final included studies
├── A. General extraction fields, Table 3
│   ├── study_id: integer
│   ├── article_title: article name
│   ├── author_name: author set
│   ├── publication_year: calendar year, RQ3
│   ├── area_in_SE: SWEBOK knowledge area plus added categories, RQ2
│   └── venue: publication venue, RQ3
├── B. Process extraction fields, Table 3
│   ├── guidelines_adopted: guideline set, RQ1
│   ├── search_strategy: strategy and selection process, RQ4
│   ├── search_type: manual / automated / both, RQ4
│   ├── classification_schemes: how articles were classified, RQ4
│   └── visualization_type: pictorial presentation type, RQ4
├── C. Derived process strategy categories, §4.4 + Appendix B
│   ├── guidelines followed: 10 guideline/template sources
│   ├── choosing search strategy: database search / snowballing / manual
│   ├── developing search: PICO, experts, iteration, known papers, standards/thesaurus
│   ├── evaluating search: known-paper test set, expert result evaluation, author webpages, test-retest
│   ├── inclusion/exclusion reliability: objective criteria, extra reviewer/consensus, decision rules
│   ├── quality assessment: yes / no
│   ├── data extraction reliability: objective criteria, extra reviewer/consensus, test-retest
│   ├── topic-independent classification: research method, research type, study focus, contribution type, venue
│   ├── topic-related classification: emerging classification / existing scheme
│   ├── visualization: line, pie, bar, bubble, Venn, heatmap
│   └── validity threats discussion: yes / no
├── D. Quality / rubric forest, §5.4
│   ├── need_for_review score: no / partial / full
│   ├── search_strategy score: no / minimal / full
│   ├── search_evaluation score: no / minimal / partial / full
│   ├── extraction_classification score: no / minimal / partial / full
│   └── validity score: no / full
└── E. Guideline update synthesis, §5
    ├── planning the mapping
    ├── conducting the mapping
    ├── reporting the mapping
    ├── evaluating the mapping process
    └── dissemination
```

缺失部分：Appendix B 的逐篇 study ID 映射未在本报告逐篇展开；A2a 若要做精确统计，应逐表核对 B.15-B.27 的 study 列表、重复引用、分母和图表读数。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `study_id` | 研究编号 | General | Table 3 | 样本 study 的整数 ID | Integer | 数值 | 不适用 | join key | 无 | §3.4 Table 3 | 仅用于样本追踪 |
| `publication_year` | 出版年 | General | Table 3 / Fig.2 | 论文发表年份 | 2007-2012 结果区间 | 数值或区间 | 未报告则不可入年趋势 | 年度趋势 | mapping study 增长趋势 | §4.1 | 不能外推 2013 后 |
| `area_in_SE` | SE 主题领域 | General | Table 3 / B.15 | SWEBOK area，另加 education / research methods | quality, tools/methods, process, management, configuration, testing, construction, design, requirements, research methods, education | 层级枚举 / 外部分类法引用 | 未归类表示表中未映射或待核验 | 主题覆盖统计 | 研究空白候选 | §4.2, Table B.15 | SWEBOK 时代和粒度限制 |
| `venue` | 发表 venue | General | Table 3 / B.16 | 发表地点和类型 | journal / conference / workshop；具体 venue 名 | 层级枚举 | 未列入表示未映射 | venue 分布 | SMS 是否被高质量论坛接受 | §4.3, Table 4, B.16 | venue 质量判断不可过度 |
| `guidelines_adopted` | 采用指南 | Process | Table 3 / B.17 | 每篇 mapping study 采用的 guideline/template | Kitchenham/Charters, Petersen et al., Budgen et al., Arksey/O'Malley, Durham template, Biolchini et al., Petticrew/Roberts 等 | 完整枚举（本样本内） | 未列不等于未受影响，只是未报告/未映射 | guideline 频次与组合 | 单一 guideline 不足的候选发现 | §4.4.1, Fig.5, B.17 | 不迁移为目标领域结论 |
| `search_strategy_action` | 搜索策略动作 | Process strategy | §4.4.2 / B.18 | study identification 使用的主策略 | database search / snowballing / manual | 完整枚举 | 未列为未报告该动作 | 搜索策略分布 | 多策略权衡启发 | Fig.6, B.18 | 不证明某策略最优 |
| `search_type` | 搜索类型 | Process | Table 3 | 搜索是 manual、automated 或 both | manual / automated / both | 完整枚举 | text 未单独给 Appendix 统计，需 A2a 对齐 | 可与 strategy 交叉 | 搜索自动化程度 | Table 3 | 与 B.18 策略口径需区分 |
| `search_development_action` | 搜索式开发动作 | Process strategy | §4.4.2 / B.19 | 如何形成关键词和检索式 | PICO, experts/librarians, iterative, known papers, standards/thesaurus | 完整枚举 | 未列为未报告该动作 | 搜索质量动作频次 | early QA 启发 | Fig.7, B.19 | 不构成强因果 |
| `search_evaluation_action` | 搜索评价动作 | Process strategy | §4.4.2 / B.20 | 如何检查检索覆盖 | known-paper test set, expert evaluates result, key-author webpages, test-retest | 完整枚举 | 未列为未报告该动作 | search validation 频次 | reference set / test set 启发 | Fig.8, B.20 | 不保证召回完整 |
| `include_exclude_action` | 纳排可靠性动作 | Process strategy | §4.4.2 / B.21 | 如何提高纳排可靠性 | objective criteria, extra reviewer/consensus, decision rules | 完整枚举 | 未列为未报告该动作 | screening QA 统计 | 人机协作裁决设计 | Fig.9, B.21 | 单人筛选风险仍在 |
| `quality_assessment` | 是否质量评价 | Process strategy | §4.4.3 / B.22 | mapping study 是否评估 primary study quality | yes / no | 布尔 | no 通常表示未做或未报告 | 14/52 等比例统计 | SMS 是否需要 QA 的候选讨论 | Fig.10, B.22 | mapping 与 SLR 目标不同 |
| `data_extraction_action` | 抽取可靠性动作 | Process strategy | §4.4.4 / B.23 | 如何保障数据抽取/分类可靠性 | objective criteria, extra reviewer/consensus, test-retest | 完整枚举 | 未列为未报告该动作 | extraction QA 频次 | 双人复核启发 | Fig.11, B.23 | 只基于报告文本 |
| `topic_independent_facet` | 跨主题分类 facet | Classification | §4.4.4 / B.24 | 不强依赖具体 topic 的分类维度 | research method, research type, study focus, contribution type, venue | 完整枚举 | 未列为 study 未使用/未报告该 facet | facet 频次统计 | 通用维度种子 | Fig.12, B.24 | 不能机械套到 LLM4STM |
| `topic_specific_classification` | 主题特化分类 | Classification | §4.4.4 / B.25 | topic 分类来自新建或既有方案 | emerging classification / existing scheme | 完整枚举 | 未列需核验 | 分类来源分布 | emergent coding 方法启发 | Fig.13, B.25 | 具体主题类不可迁移 |
| `visualization_type` | 可视化类型 | Process | Table 3 / B.26 | 用于呈现 mapping 数据的图形 | line, pie, bar, bubble, Venn, heatmap | 完整枚举 | 未列为未报告该类型 | 图形使用频次 | evidence dashboard 启发 | Fig.14, B.26 | 不代表图形优劣 |
| `validity_threats_reported` | 是否报告效度威胁 | Process strategy | §4.4.6 / B.27 | study 是否讨论 validity threats | yes / no | 布尔 | no 为未报告/未映射 | threat reporting 比例 | 审计必填项启发 | Fig.15, B.27 | 不能说明实际无威胁 |
| `rubric_need` | review need 评分 | Rubric | Table 9 / 14 | 是否说明动机、目标、受众协商 | 0/1/2；no/partial/full | 有序枚举 / 数值 | 未报告按 no description | 质量分布 | 报告质量候选 finding | §5.4 | 基于 reported information |
| `rubric_search_strategy` | 搜索策略评分 | Rubric | Table 10 / 14 | 使用搜索策略数量 | 0/1/2；no/minimal/full | 有序枚举 / 数值 | 未报告按 no description | 质量分布 | 搜索可靠性启发 | §5.4 | 多策略不一定高 ROI |
| `rubric_search_eval` | 搜索评价评分 | Rubric | Table 11 / 14 | 是否提高 search 与纳排可靠性 | 0/1/2/3 | 有序枚举 / 数值 | 未报告按 no description | 质量分布 | validation gate 启发 | §5.4 | 需要反证与成本权衡 |
| `rubric_extract_class` | 抽取/分类评分 | Rubric | Table 12 / 14 | 抽取可靠性与 research type/method 分类 | 0/1/2/3 | 有序枚举 / 数值 | 未报告按 no description | 质量分布 | schema QA 启发 | §5.4 | 不等同于研究有效性 |
| `rubric_validity` | validity 评分 | Rubric | Table 13 / 14 | 是否描述 threats / limitations | 0/1 | 有序枚举 / 布尔 | 未报告按 no description | 质量分布 | limitations gate 启发 | §5.4 | 报告有无不等于威胁大小 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `edge_study_topic` | included study | classified_as | `area_in_SE` | Table B.15 topic categories | 未列为未映射或待核验 | Appendix B.15 | 主题分布 |
| `edge_study_venue` | included study | published_in | `venue` | journal / conference / workshop | 未列为待核验 | Appendix B.16 | venue 分布 |
| `edge_study_guideline` | included study | follows | `guidelines_adopted` | 10 guideline/template sources | 未列不等于未读，只是不报告 | Appendix B.17 | guideline adoption |
| `edge_study_search_strategy` | included study | uses_action | `search_strategy_action` | database / snowballing / manual | 未列为未报告 | Appendix B.18 | study identification 分析 |
| `edge_study_search_development` | included study | uses_action | `search_development_action` | PICO 等 5 类 | 未列为未报告 | Appendix B.19 | search QA 分析 |
| `edge_study_search_eval` | included study | uses_action | `search_evaluation_action` | test set 等 4 类 | 未列为未报告 | Appendix B.20 | search validation |
| `edge_study_ie_reliability` | included study | uses_action | `include_exclude_action` | objective criteria / consensus / decision rules | 未列为未报告 | Appendix B.21 | screening reliability |
| `edge_study_classification_facet` | included study | uses_facet | `topic_independent_facet` | 5 facets | 未列为未使用或未报告 | Appendix B.24 | 通用分类 facet 统计 |
| `edge_study_topic_specific_schema` | included study | uses_schema_source | `topic_specific_classification` | emerging / existing | 未列为待核验 | Appendix B.25 | coding schema 来源 |
| `edge_study_visualization` | included study | presents_with | `visualization_type` | 6 visualization types | 未列为未报告 | Appendix B.26 | evidence presentation |
| `edge_action_guideline` | research process action | recommended_by_or_used_in | guideline source | Table 5 columns | 空格/符号抽取需 PDF 版面核验 | Table 5 | guideline update synthesis |
| `edge_method_research_type` | research method | maps_to | research type | validation / evaluation research | 多归属允许 | Fig.19 | disambiguate research type |
| `edge_rubric_activity_score` | included study | receives_score | rubric category | no/minimal/partial/full | 基于 reported information | Table 9-14 | quality distribution |

### 6. 统计观察、候选 finding 与 final finding 边界

原文字段/统计表支持的统计观察：

- 最终 included mapping studies 为 52；选择链条可追溯到 Fig.1，但 57、44、52 是不同阶段分母，不能混写。
- 24 篇 mapping studies 使用多个 guideline，支持“单一 guideline 不足”的方法学观察。
- 质量评价并不普遍：正文给出 14/52。
- venue、research type、research method 是最常见的 topic-independent facets；contribution type 使用较少。
- topic-specific classification 多数为 emerging classification，也有 existing scheme。
- bar plot 与 bubble plot 是常见可视化；validity threats 多数被报告。
- Table 14 支持 rubric 分布：例如 validity 为 45 full / 7 no；search evaluation 没有 full evaluation。

原文 discussion / recommendation / guideline 的候选 finding：

- SMS 不应追求“找到全部论文”作为唯一目标，good sample / representation 更关键。
- mapping study 的通用字段应包含 venue、research type、research method；contribution type 的通用性较弱。
- 检索应考虑 P/I、专家/标准/已知论文、test set 等早期 QA。
- selection、extraction、classification 都需要可靠性动作，单人流程是威胁。
- 报告结构应标准化，appendix 应保留 included / excluded 或 borderline 信息。
- 可以用 action checklist / rubric 评价 mapping study 报告质量。

对 Paper2 可迁移的方法学启发：

- 先定义样本单位，再从 extraction form / appendix mapping table 复原 schema。
- 把通用维度与主题特化维度分层，不要一棵树压扁。
- 建立 evidence ledger、relationship edges、missing semantics，而不只写摘要。
- 对 agent-assisted SLR，必须记录 selection/extraction/classification 的人机裁决和 drift 风险。
- 统计观察、candidate finding、final finding 必须分层。

绝不能迁移的领域结论：

- 不能把“software testing 是 SMS 中最多 topic”等结论迁移到 LLM4STM。
- 不能把 2015 年 SE mapping guideline 直接当成现代 LLM agent SLR 的完整规范。
- 不能把 rubric score 当成 study scientific quality 的绝对度量；作者明确说这是基于 reported information。
- 不能用单篇 guideline update 的 discussion 直接形成 Paper2 final research finding。

### 7. 对现有 `review.md` 的返修建议

| 级别 | 建议 | 理由 |
|---|---|---|
| C | 重写“维度树复原”，以 Table 3 + §4.4 + Appendix B 为原生样本编码森林；planning/conducting/reporting 只能作为 guideline update synthesis，不应当替代 sample coding tree | 当前仍残留六个通用 leaf 和 v1 历史投影，容易违背 A1-DT v2 |
| C | 将样本单位修正为 `SE systematic mapping study`，样本数量写成“最终 52；57/44 为阶段性分母” | 现有表述容易把 selection chain 混成一个不清楚分母 |
| C | SUMMARY 行若写“统计池资格=是”，应改为“局部可统计：A1 方法学统计池 yes，目标领域统计池 no” | 避免把方法学证据误用为领域效果证据 |
| I | A.2 / A.3 应替换 placeholder 式 `not_verified` 行，补入 Table 3、Fig.1、B.15-B.27、Table 8-14 的具体证据 | 当前证据账本太泛，不能支撑 leaf 级返修 |
| I | 新增关系边表，尤其是 study-to-category、action-to-guideline、method-to-research-type、rubric-to-study-score | 本文原生 schema 关系性强，不能只用树描述 |
| I | 删除或下沉 A1-M0--M6、patterns、v1 audit link 的事实源地位 | 用户明确禁止把旧 v1 或跨论文投影当单篇模板 |
| M | 保留六个通用接口为“跨论文投影”，但不得放在原文主树首位 | 可用于总账对齐，但不是原文字段 |
| M | A2a 做 PDF 图表视觉核验：Fig.1、Fig.5-Fig.15、Table 5、Table 8-14、B.15-B.27 | 当前仅 CLI layout 核对，复杂图形读数仍有风险 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-P2015-01 | `bibtex.bib`, `metadata.json` | 题录 | title / DOI / journal | 2015 IST 期刊论文，主题为 SMS guideline update | metadata | high | 论文身份、类型 | 否 | 不支撑 schema |
| EV-P2015-02 | `paper_content.txt` | Abstract | Context / Method / Results | 作者对 systematic maps 做 systematic mapping，并提出 updated guideline | root_type | high | 原文类型、样本库存在性 | 否 | 只支撑方法学定位 |
| EV-P2015-03 | `paper_content.txt` | §3.1 | RQ1-RQ4 | RQ 覆盖 guideline、topic、venue/year、process | rq_to_fields | high | 字段用途 | 否 | RQ 不是树根 |
| EV-P2015-04 | `paper_content.txt`, `paper.pdf` | §3.2 | Table 1 / Table 2 | 数据库、搜索串、搜索结果数 | search_protocol | high | 语料收集链条 | 表格已 CLI 核对 | 不保证召回完整 |
| EV-P2015-05 | `paper_content.txt`, `paper.pdf` | §3.3 | Fig.1 | 选择链条最终到 52 篇 included studies | denominator | medium | 样本数量 / 分母 | 是 | 中间 57/44 不可混用 |
| EV-P2015-06 | `paper_content.txt`, `paper.pdf` | §3.4 | Table 3 | extraction form 含 General 与 Process 字段 | extraction_schema | high | 原生主树 | 否 | 字段定义仍较粗 |
| EV-P2015-07 | `paper_content.txt` | §3.5 | analysis paragraph | 抽取项被制表、可视化、归主题并计数 | coding_process | high | 分类与统计流程 | 否 | 主题归组有作者判断 |
| EV-P2015-08 | `paper_content.txt` | §3.6 | validity subsections | 描述性、理论、泛化、解释、可重复性威胁 | validity_schema | high | threat leaf | 否 | 未覆盖 LLM drift |
| EV-P2015-09 | `paper_content.txt` | §4.4 | Fig.5-Fig.15 | guideline、search、classification、visualization、validity 结果 | result_categories | medium | derived process forest | 是 | 图形精确读数待核 |
| EV-P2015-10 | `paper_content.txt`, `paper.pdf` | §5 | Table 5 | research process actions 映射到各 guideline | guideline_synthesis | medium | guideline update tree | 是 | 是 synthesis，不是逐篇原始字段 |
| EV-P2015-11 | `paper_content.txt`, `paper.pdf` | §5.4 | Table 8-14 | action checklist、rubric、score distribution | rubric_schema | high | quality/rubric forest | 表格已 CLI 核对 | 基于 reported information |
| EV-P2015-12 | `paper_content.txt`, `paper.pdf` | Appendix B | B.15-B.27 | study-to-category mapping tables | relation_edges | high | 关系边、取值空间 | 表格已 CLI 核对，逐项仍需 A2a | 逐篇分母需复算 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-P2015-01 | 本文有系统样本库，样本单位是 SE systematic mapping study | sample_unit | root | EV-P2015-02, 03, 05 | strong | A1-DT 卡片 / review 重写 | 作者称 primary studies，但相对 A1 是 secondary studies |
| CLM-P2015-02 | 最终统计分母应写 52 included mapping studies | denominator | sample set | EV-P2015-05, 12 | strong | SUMMARY / review | 57、44 是阶段分母 |
| CLM-P2015-03 | 原生样本编码主入口是 Table 3 extraction form | schema_root | dimension tree | EV-P2015-06 | strong | 维度树复原 | Table 3 字段较粗，需要 Appendix B 展开 |
| CLM-P2015-04 | 原生 schema 是维度森林，不是单一 planning/conducting/reporting 树 | tree_type | full schema | EV-P2015-06, 09, 10, 11, 12 | strong | A1-DT v2 判定 | guideline stage 是 synthesis 层 |
| CLM-P2015-05 | Appendix B 提供显式 study-to-category 关系边 | relation_schema | edges | EV-P2015-12 | strong | 关系边表 | 逐篇列表需 A2a 复算 |
| CLM-P2015-06 | topic-independent facets 包括 venue、research type、research method、study focus、contribution type | leaf_values | classification | EV-P2015-09, 12 | strong | schema seed | 不可直接套为 LLM4STM 字段全集 |
| CLM-P2015-07 | 多 guideline 组合支持“单一指南不足”的方法学候选 finding | candidate_finding | guideline usage | EV-P2015-09, 10 | medium | discussion / method motivation | 只对 SMS guideline update 有效 |
| CLM-P2015-08 | quality/rubric 可作为 Paper2 审计 rubric 设计启发 | method_seed | rubric | EV-P2015-11 | medium | Paper2 方法设计 | 原 rubric 未覆盖 LLM/provider/prompt drift |
| CLM-P2015-09 | 本文可进入方法学统计池，但不可进入目标领域效果统计池 | eligibility | statistical boundary | EV-P2015-02, 06, 09 | strong | SUMMARY 修正 | 不是 LLM4STM 领域研究 |
| CLM-P2015-10 | 当前 `review.md` 需要返修以降级六叶接口和 v1 历史内容 | repair | local review | EV-P2015-06, 12 + `review.md` | strong | 返修任务 | 可保留六叶为投影接口 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence discipline、unsupported claim 降级、review task 以风险和证据为先。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 soundness、clarity、reproducibility、constructive specificity 标准。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用 evidence gaps、severity、claim audit、自我审查风险记录。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先读材料、显式标注歧义、输出结构化 schema / risk 的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“不编造缺失细节”“严格贴合原文方法”的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化字段、任务依赖、风险项表达。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 完成纪律；未启动 autoresearch、tmux、subagent 或后台 agent。

本输出最高风险 3 点：

1. Appendix B 逐篇映射没有逐项复算，只按原文表结构审计。主线程合并时应对 B.15-B.27 做逐表计数。
2. PDF 核验是 CLI layout，不是视觉级图像核验。Fig.5-Fig.15 的柱状/气泡读数应在 A2a 用 PDF 视觉复查。
3. Table 5 符号在 text extraction 中有编码噪声，本文只把它作为 action-to-guideline 综合证据；若要精确标注每个 guideline 覆盖哪些 action，需人工核对原 PDF 表格。

blocked / timeout / 文件缺失：未出现。所有指定技能文件和四个论文材料均可读取；未修改仓库文件，未 commit，未 push，未发 gh comment，未启动任何 subagent。