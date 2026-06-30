### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `app-reviews-slr-se` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是。按页码顺序阅读全文 1--63 页对应的 2661 行文本抽取。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。已核对题名、作者、年份、DOI、ESE 期刊、SLR 类型、本地全文状态。 |
| 是否打开或核对 `paper.pdf` | 是。用 `pdfinfo` 核对 63 页 PDF；用 `pdftotext -layout` 局部核对表 3、4、7、8、13、16--22 与 Discussion/Threats。未做截图级人工视觉核验。 |
| 原文类型 | SLR |
| 被编码样本单位 | 182 篇 primary studies，发表时间覆盖 2012--2020；检索时间窗为 2010-01 至 2020-12。 |
| 样本数量 / 分母 | 主样本分母 182；经验评价分母 109；effectiveness evaluation 105；user-perceived quality 23；RQ5 结果分母 87。 |
| 原生树类型 | 维度森林：以 primary study record 为根，包含 F1--F18 数据抽取字段、三套分类 schema、评价/复现资产 schema、交叉关系表。 |
| 主统计池资格 | 局部可统计。原文是系统 SLR 且分母清楚，可统计其原生字段与表格观察；但 app review 领域结论不能迁移为 Paper2 领域 final finding。 |
| 总体判定 | needs repair。现有 `review.md` 已有全文基础，但维度树仍过度受六叶通用接口影响，应重写为原文 F1--F18 + 三套分类 schema 的维度森林。 |

### 1. 原文证据阅读说明

实际读取文件：`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`。实际读取章节：Abstract、Introduction、Research Method、RQ1--RQ5 Results、Discussion、Threats to Validity、Related Work、Conclusion、References。PDF 核验：`pdfinfo` 确认 63 页；`pdftotext -layout` 核对表 3、表 4、表 7、表 8、表 13、表 16--22、Discussion 与 Threats 的版面文本。未读取 supplementary GitHub package；表 14/15 的宽表内容在文本抽取中不完整，需 A2a 视觉核验。

关键证据锚点：

1. Abstract：原文称覆盖 182 篇 2012--2020 论文，并按 mined information、data mining techniques、supported SE activities 分类。
2. §2.1 RQ1--RQ5：RQ 分别对应 analysis type、technique、SE activity、empirical evaluation、evaluation result。
3. §2.2 + Fig. 1：检索选择链条包括 1656 初始命中、303 去重、1353 筛选、1225 排除、14 手工检索、40 snowballing、最终 182。
4. Table 1：纳入 primary studies；排除 secondary / tertiary studies、technical reports、manuals 等。
5. Table 3：F1--F18 数据抽取表，是本审计最核心的原生字段来源。
6. §2.3：F6/F7/F8/F10/F14/F18 有子字段说明，F18 还记录 replication package 内容并联系作者确认。
7. §2.4 + Table 4：三套 classification schema：app review analysis、mining technique、SE activity；并报告 intra/inter-rater agreement。
8. Table 7：app review analysis 九类及频次。
9. Table 9：mining technique 四类及频次；Table 10/11 为 analysis-technique 关系统计。
10. Table 13：SE activity taxonomy，含 14 个活动和 `NOT SPECIFIED`。
11. §3.5 + Tables 16--20：评价字段、公开数据集、工具、数据集五数概括、user study criteria/participants。
12. §3.6 + Tables 21--22：因异质性不做 meta-analysis，采用 summarizing effect estimates 和 user-study synthesis。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？  
原文逐项描述对象是 primary study。每篇 primary study 被抽取 F1--F18 字段，再被编码进 app review analysis、mining technique、SE activity、empirical evaluation、replication package 等维度。公开数据集、工具、参与者、评价指标是 primary study 的派生属性或评价资产，不是主样本单位。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？  
有。作者遵循 Kitchenham SLR 流程，定义 RQ 和 protocol，自动检索 + 手工 venue 检索 + backward/forward snowballing，使用 Table 1 纳排标准，最终 182 篇。数据抽取使用 Table 3 的 F1--F18 form；编码使用三套 classification schema，并报告筛选、抽取和分类可靠性。

3. 原文字段来自哪里？  
主要来自 extraction form（Table 3）、classification schema（§2.4、Table 4、Table 7、Table 9、Table 13）、mapping/cross-tabulation tables（Table 8、10、11、14、15、19、20）、evaluation result tables（Table 16--22）和 supplementary spreadsheet。Replication package 字段来自 F18 及作者主动联系 primary studies 作者的可用性确认。

4. RQ 与样本单位是什么关系？  
RQ 不是树根本身，而是字段用途与结果组织方式。F6 用于 RQ1，F7 用于 RQ2，F8/F9 用于 RQ3，F10--F12/F14--F18 用于 RQ4，F13 用于 RQ5。真正的编码根对象是 primary study record。

5. 若无系统样本库，如何降级？  
本文不需要降级为 roadmap/guideline seed，因为它有系统样本库、纳排链条、抽取字段、分类 schema 和统计分母。但没有读取 supplementary package，因此 supplementary 中更细字段仍应标为待核验。

### 3. 原生样本编码维度树 / 维度森林

```text
Primary study record, n = 182
├── A. 文献书目信息 / Documentation
│   ├── F1 Title
│   ├── F2 Author(s)
│   ├── F3 Year
│   ├── F4 Venue
│   └── F5 Citation
├── B. App review analysis schema, for RQ1
│   ├── F6.1 Review analysis type
│   │   ├── Information Extraction
│   │   ├── Classification
│   │   ├── Clustering
│   │   ├── Search and Information Retrieval
│   │   ├── Sentiment Analysis
│   │   ├── Content Analysis
│   │   ├── Recommendation
│   │   ├── Summarization
│   │   └── Visualization
│   ├── F6.2 Mined information
│   └── F6.3 Supplementary description
├── C. Mining technique schema, for RQ2
│   ├── F7.1 Technique type
│   │   ├── Manual Analysis
│   │   ├── Natural Language Processing
│   │   ├── Machine Learning
│   │   └── Statistical Analysis
│   └── F7.2 Technique name
├── D. Software engineering activity schema, for RQ3
│   ├── F8 SE Activity
│   │   ├── Requirements
│   │   │   ├── Requirements Elicitation
│   │   │   ├── Requirements Classification
│   │   │   ├── Requirements Prioritization
│   │   │   └── Requirements Specification
│   │   ├── Design
│   │   │   ├── Design Rationale Capture
│   │   │   └── User Interface Design
│   │   ├── Testing
│   │   │   ├── Validation by Users
│   │   │   ├── Test Documentation
│   │   │   ├── Test Design
│   │   │   └── Test Prioritization
│   │   ├── Maintenance
│   │   │   ├── Problem and Modification Analysis
│   │   │   ├── Requested Modification Prioritization
│   │   │   ├── Help Desk
│   │   │   └── Impact Analysis
│   │   └── Not specified
│   └── F9 Justification
├── E. Empirical evaluation / evidence schema, for RQ4--RQ5
│   ├── F10 Evaluation Objective
│   │   ├── F10.1 general objective
│   │   └── F10.2 evaluated app review analysis type
│   ├── F11 Evaluation Procedure
│   ├── F12 Evaluation Metrics and Criteria
│   ├── F13 Evaluation Result
│   ├── F14 Annotated Dataset
│   │   ├── F14.1 App Store name
│   │   └── F14.2 number of annotated reviews
│   ├── F15 Annotation Task
│   ├── F16 Number of Annotators
│   ├── F17 Quality Measure
│   └── F18 Replication Package
│       ├── package availability
│       ├── annotated dataset availability
│       ├── implementation availability
│       └── experiment scripts availability
└── F. Derived relation/statistics layer
    ├── analysis type × mining technique
    ├── technique-combination × analysis type
    ├── analysis type × SE activity
    ├── analysis-combination × SE activity
    ├── user-study criterion × analysis type
    ├── participant type × user-study
    ├── effectiveness result × mined information
    └── discussion gap derived from statistical observations
```

缺失部分：未精核 supplementary spreadsheet，因此 F6.2、F6.3、F7.2、F9、F11、F13、F18 的每篇论文级原始取值未展开；表 14/15 宽表需要 A2a PDF 视觉级核验。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| F1 | 标题 | 文献书目信息 | Table 3 | primary study 题名 | 文本 | 自由文本 | 不应缺失 | 去重、索引 | 无直接 finding | Table 3 | 仅作元数据 |
| F2 | 作者 | 文献书目信息 | Table 3 | primary study 作者 | 文本/列表 | 自由文本 | 不应缺失 | 元数据统计 | 无直接 finding | Table 3 | 仅作元数据 |
| F3 | 年份 | 文献书目信息 | Table 3 | 发表年份 | 2012--2020 | 数值/区间 | 不应缺失 | 年度趋势 | 研究增长观察 | Fig. 2, §3.1 | 不迁移领域趋势 |
| F4 | Venue | 文献书目信息 | Table 3 | 发表 venue | venue 名称/类型 | 自由文本 + 分类 | 未报告则待核验 | venue 分布 | 社区关注度 | Fig. 3, Table 5 | 不迁移 venue 质量结论 |
| F5 | 引用数 | 文献书目信息 | Table 3 | Google Scholar citation，日期为 2021-08-04 | 非负整数 | 数值 | 未取到则缺失 | 影响力表 | 识别 influential papers | Table 6 | 引用数会漂移 |
| F6.1 | app review analysis 类型 | Review Analysis | Table 3, §2.4, Table 7 | 对 reviews 做的分析任务类型 | 9 类：IE, classification, clustering, SIR, sentiment, content, recommendation, summarization, visualization | 完整枚举 | 不适用少见；多值允许 | 频次、交叉表 | 识别任务覆盖与空白 | Table 7 | 类别为 app review 领域特化 |
| F6.2 | mined information | Review Analysis | §2.3 | 被挖掘信息，如 feature、bug report、request、opinion | 文本/领域标签 | 自由文本 + 待核验枚举 | 未说明则 not_reported | 分层统计 seed | 识别信息需求 | §2.3, RQ1 sections | 需 supplementary 精核 |
| F6.3 | supplementary description | Review Analysis | §2.3 | 分析任务补充说明 | 文本 | 自由文本 | 可缺失 | 解释性字段 | 支撑分类裁决 | §2.3 | 不宜定量化 |
| F7.1 | mining technique 类型 | Mining Technique | Table 3, §2.4, Table 9 | 实现 review analysis 的技术大类 | Manual Analysis, NLP, ML, Statistical Analysis | 完整枚举 | 未说明则 not_reported；多值允许 | 技术频次、组合统计 | 识别技术偏向 | Table 9--11 | 需重建 LLM/agent 时代 taxonomy |
| F7.2 | technique name | Mining Technique | §2.3, Table 12 | 具体技术名，如 Naive Bayes、SVM、LDA | 文本/技术名 | 自由文本 + 层级枚举 seed | 未说明则 not_reported | 技术细分统计 | baseline/方法启发 | Table 12 | 不是通用方法优劣证据 |
| F8 | SE activity | SE Activity | Table 3, §2.4, Table 13 | primary study 声称支持的软件工程活动 | 14 活动 + Not specified | 层级枚举 | 原文显式 `NOT SPECIFIED` 是有意义缺失 | 活动覆盖、交叉表 | 用例清晰度 gap | Table 13 | 活动 taxonomy 需按目标领域重建 |
| F9 | justification | SE Activity | Table 3, §2.3 | 论文解释 app review analysis 如何支持 SE activity | 文本 | 自由文本加理由 | 原文称部分论文无 justification | 用例强度审计 | 模糊 use case finding | §2.3, §4.2 | 不可把声称当效果 |
| F10.1 | evaluation objective general | Evaluation | §2.3, §3.5 | 评价目标，如 quantitative effectiveness 或 user-perceived usefulness | effectiveness / user-perceived quality 等 | 层级枚举 seed | 未评价则 not_applicable | 评价覆盖统计 | 评价偏向 gap | §3.5 | 需区分 objective 与 result |
| F10.2 | evaluated analysis type | Evaluation | §2.3, §3.5 | 被评价的 app review analysis 类型 | 与 F6.1 对齐的分析类型 | 外部分类法引用 | 未评价则 not_applicable | evaluation × analysis | 哪类任务缺评价 | §3.5 | 不代表任务本身有效 |
| F11 | evaluation procedure | Evaluation | Table 3, §3.5 | 评价方法和步骤 | annotated dataset / output assessment / artifact baseline / user study 等 | 自由文本 + 枚举 seed | 未评价则 not_applicable | 方法学比较 | 评价设计启发 | §3.5.1--3.5.2 | 需逐篇核验 |
| F12 | metrics and criteria | Evaluation | Table 3, §3.5 | 量化指标或用户评价标准 | precision, recall, F1, accuracy, usefulness, usability, efficiency, informativeness 等 | 层级枚举 | 未报告则 not_reported | 指标统计 | 指标-claim 对齐审计 | §3.5, Table 19, Table 21 | 指标值不可跨异质任务硬合并 |
| F13 | evaluation result | Evaluation | Table 3, §3.6 | 经验评价结果 | 数值范围/median/qualitative synthesis | 数值或自由文本 | 未报告则 not_reported | RQ5 描述合成 | 结果强弱边界 | Table 21--22 | 原文明确不做 meta-analysis |
| F14.1 | app store name | Annotated Dataset | §2.3, §3.5.1 | 数据集 reviews 来源商店 | Google Play, Apple Store 等 | 枚举 seed | 无 annotated dataset 则 not_applicable | 数据来源统计 | 外部有效性风险 | §3.5.1 | 需 supplementary 精核 |
| F14.2 | annotated review count | Annotated Dataset | §2.3, Table 18 | 标注 reviews 数量 | 80--41793；median 2800 | 数值/区间 | 无 annotated dataset 则 not_applicable | 数据规模统计 | 小数据集 gap | Table 18, §4.4 | 不能代表真实工业数据规模 |
| F15 | annotation task | Annotation | Table 3, §3.5 | 人类标注任务 | classify issue types, feature/sentiment, user story 等 | 自由文本 + 枚举 seed | 无标注则 not_applicable | 标注任务分布 | 标注成本/质量风险 | Table 16, §3.5 | 需逐 dataset 核验 |
| F16 | number of annotators | Annotation | Table 3, §3.5 | 标注者数量 | 1--5；median 2 | 数值/区间 | 未报告则 not_reported | 评价质量统计 | 标注可靠性 gap | §3.5.1 | 数量不等于质量 |
| F17 | quality measure | Annotation | Table 3, §3.5 | 标注可靠性度量 | Cohen’s Kappa, Percentage Agreement, Jaccard, Fleiss’ Kappa | 枚举 | 未报告是重要缺失；仅 26 studies 报告 | 质量报告覆盖 | 复现/可信度 gap | §3.5.1 | 需保留任务差异 |
| F18 | replication package | Replication | Table 3, §3.5, §4.5 | 是否有复现包及其内容 | availability 布尔 + dataset/implementation/scripts 内容 | 布尔 + 关系值 | 未发布或不可获得需区分 | 可复现性统计 | replication gap | Table 16--17, §4.5 | 不能等同于复现质量高 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | primary study | has_analysis | F6.1 analysis type | 9 类，可多值 | 未编码需待核验 | Table 7, §3.2 | 任务覆盖统计 |
| R2 | F6.1 analysis type | realized_by | F7.1 technique type | MA/NLP/ML/SA，可组合 | 未说明技术为 not_reported | Table 10--11 | analysis-technique 交叉统计 |
| R3 | F7.1 technique type | has_concrete_method | F7.2 technique name | 技术名列表 | 未说明则 not_reported | Table 12 | baseline/方法趋势 |
| R4 | primary study | claims_support_for | F8 SE activity | 14 活动 + Not specified，可多值 | `NOT SPECIFIED` 是显式类别 | Table 13 | SE 用例覆盖统计 |
| R5 | F8 SE activity | justified_by | F9 justification | 自由文本理由 | 无 justification 是重要弱证据 | §2.3, §4.2 | 区分声称与可解释用途 |
| R6 | F6.1 analysis type | used_for | F8 SE activity | analysis × activity | 表 14/15 需视觉核验 | Table 14--15 | 分析任务如何支持活动 |
| R7 | Search/IR analysis | links_review_to | external artifact | App description, Git commit, Goal model, Issue report, Lint warning, Source code, Stack trace, Tweet | 不适用其他 analysis | Table 8 | 关系型 schema seed |
| R8 | evaluated approach | evaluated_by | F10--F13 evaluation record | objective/procedure/metric/result | 未评价则 not_applicable | §3.5--3.6 | 评价证据链 |
| R9 | evaluation record | uses_dataset | F14--F17 annotation record | store/count/task/annotators/quality measure | 无标注数据则 not_applicable | Tables 16, 18 | 数据与标注质量审计 |
| R10 | evaluation record | has_replication_asset | F18 replication package | package/dataset/tool/scripts | 未发布需记录 | Table 16--17, §4.5 | 可复现性审计 |
| R11 | user study | assesses_by | evaluation criterion | accuracy, efficiency, informativeness, usability, usefulness | 非 user study 不适用 | Table 19 | 用户感知质量 schema |
| R12 | statistical observation | motivates | discussion gap | use case, reference model, dataset size, replication, practice impact, practitioner needs, scalability, ML training | discussion 不等于 final finding | §4.1--4.10 | 候选 finding 生成 |

本文发现显式关系型 schema：尤其是 analysis-technique、analysis-SE activity、evaluation-analysis、dataset-evaluation、review-external artifact traceability。关系边不是因果边，主要是编码、支持、评价或映射关系。

### 6. 统计观察、候选 finding 与 final finding 边界

原文字段/统计表支持的统计观察：

- 最终纳入 182 篇 primary studies；发表时间覆盖 2012--2020。
- App review analysis 九类中，classification 105 篇、information extraction 56、content analysis 54、clustering 44、sentiment 40、recommendation 30、summarization 25、search/IR 24、visualization 20。
- Mining technique 四类：NLP 113、ML 108、statistical analysis 53、manual analysis 45。
- SE activity 覆盖 requirements、maintenance、testing、design；14 个细活动；62 篇未指定 SE activity。
- 109 篇做 empirical evaluation；105 篇 effectiveness，23 篇 user-perceived quality。
- 公开 annotated datasets 23 个、公开 tools 16 个；annotator 数 1--5，median 2；仅 26 篇报告 annotation quality measure。
- Annotated dataset 的 review 数五数概括为 min 80、Q1 1000、median 2800、Q3 4400、max 41793。
- RQ5 基于 87 篇 evaluation result；作者因异质性不做 meta-analysis，而采用 summarizing effect estimates。

Discussion / recommendation 提出的候选 finding：

- 研究快速增长，但 SE goals/use cases 经常不够清楚。
- 需要 review mining tools 的 reference model。
- 评价数据集偏小，影响泛化。
- replication package、公开数据集和工具不足，阻碍复制与比较。
- 仍不清楚技术是否足够支持真实实践。
- 当前工具更 data-driven than goal-driven，缺少 practitioner needs study。
- 需要验证工业需求和目标用户。
- 缺少 efficiency/scalability 评价。
- 监督式 ML 训练数据成本高，且存在 domain/time drift 风险。

对 Paper2 可迁移的方法学启发：

- 抽取表必须覆盖 evaluation、annotation quality、replication package，而不是只抽方法类别。
- RQ 可以作为字段用途和结果组织，但样本单位与 extraction form 才是维度树根。
- 分类 schema 应说明来源、迭代构造、合并规则和 inter/intra-rater agreement。
- 异质结果应做描述统计/范围/median/qualitative synthesis，不强行 meta-analysis。
- Discussion finding 应由统计观察触发，再记录解释、限制与 future work。

绝不能迁移的领域结论：

- 不能把 app review analysis 九类或频次当作 LLM4STM 的任务 taxonomy。
- 不能把 app review 中 NLP/ML 占比推断为状态机建模研究的方法占比。
- 不能把 “classification 最常见” 或 “requirements/maintenance 36%” 外推到 Paper2。
- 不能把 user-perceived usefulness 结果迁移为 LLM 状态机工具有效性证据。
- 单篇 discussion gap 不能直接成为 Paper2 final finding；只能作为 candidate finding seed。

### 7. 对现有 `review.md` 的返修建议

| 级别 | 问题 | 最小返修建议 |
|---|---|---|
| C | 维度树仍以“RQ 驱动分类树 + 六个通用接口叶子”为主要表达，容易把跨论文投影误读成原文原生树。 | 重写“维度树复原”：根对象改为 `primary study record, n=182`；主干改为 F1--F18、三套 classification schema、evaluation/replication schema、关系统计层。六叶接口只能放到“通用投影”小节。 |
| C | A.2/A.3 证据账本大量 `not_verified` 泛化行，不能直接支撑强结论。 | 用 Table 3、Table 4、Table 7、Table 9、Table 13、Table 16--22 的具体证据替换泛化行；区分 text-level strong、PDF-layout checked、needs visual check。 |
| C | “候选主统计池资格”表述过保守且混淆 A1-DT 阶段限制与原文本身系统性。 | SUMMARY 中应写：`局部可统计` 或 `是，限方法学/schema/原文统计观察；领域结论不可迁移`。 |
| I | F1--F18 没有逐项成为叶子维度，F6/F7/F10/F14/F18 子字段缺失。 | 新增叶子维度表，至少列 F1--F18；F6.1/F6.2/F6.3、F7.1/F7.2、F10.1/F10.2、F14.1/F14.2、F18 contents 可拆为子叶。 |
| I | 关系边不足，未充分表达 Table 8、10、11、14、15、19、20。 | 新增关系边：analysis→technique、analysis→SE activity、SIR→external artifact、evaluation→dataset、user study→criterion/participant。 |
| I | 统计观察、discussion recommendation、Paper2 可迁移启发仍可能混层。 | 单独维护三段：统计观察、candidate finding、不可迁移领域结论；final finding 一律需跨论文裁决。 |
| I | 表 14/15 宽表在 text/PDF-layout 抽取中没有完整内容。 | 标记 A2a 视觉核验；返修时避免使用未核出的具体表格数值。 |
| M | PDF 核验记录不够细。 | 在 review.md 增加“PDF layout 核验范围”：pages 7--9、12--20、24--29、34--44、45--51；说明 supplementary 未读。 |
| M | `review.md` 历史草稿较长，事实真源不够集中。 | 将历史草稿下沉，保留一份“当前事实真源”表，避免后续 agent 误读旧 v1 树。 |

SUMMARY 当前表建议修正：

| 字段 | 建议值 |
|---|---|
| 样本单位 | primary study |
| 样本数量 | 182 |
| 原生树类型 | 维度森林：F1--F18 extraction form + 三套 classification schema + evaluation/replication schema + relation/cross-tab layer |
| 统计池资格 | 局部可统计：可统计原文 schema 与统计观察；不可迁移 app review 领域结论为 Paper2 final finding |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | `paper_content.txt`, `paper.pdf` | Abstract | Page 1 | 覆盖 182 篇 2012--2020 论文；分类 mined information、techniques、SE activities、evaluation。 | 样本分母/综述类型 | strong | 根对象、SLR 类型 | 否 | 不支撑目标领域结论 |
| EV-002 | `paper_content.txt`, `paper.pdf` | §2.1 | RQ1--RQ5 | RQ 对应 analysis、technique、SE activity、evaluation method、evaluation result。 | 字段用途 | strong | F6--F13/F18 的 RQ 映射 | 否 | RQ 不是树根 |
| EV-003 | `paper_content.txt` | §2.2 | Fig. 1 周边段落 | 检索链：1656、303 duplicate、1353 screened、1225 excluded、14 manual、40 snowballing、182 final。 | 纳排链条 | medium | systematic corpus | 是，Fig. 1 视觉核验 | 不复原检索式全文 |
| EV-004 | `paper_content.txt`, `paper.pdf` | §2.2 | Table 1 | 纳入 primary studies；排除 secondary/tertiary、technical reports、manuals 等。 | 样本单位边界 | strong | primary study 单位 | 否 | 不说明每篇排除细节 |
| EV-005 | `paper_content.txt`, `paper.pdf` | §2.3 | Table 3 | F1--F18 data extraction form。 | 原生字段表 | strong | 叶子维度全集骨架 | 否 | F6/F7/F10/F14/F18 子值需逐篇核验 |
| EV-006 | `paper_content.txt`, `paper.pdf` | §2.3 | F18 说明 | F18 记录 replication package availability 与内容，并联系作者确认。 | 复现资产字段 | strong | F18 | 否 | availability 不等于复现成功 |
| EV-007 | `paper_content.txt`, `paper.pdf` | §2.4 | Data synthesis | 三套 schema 用 content analysis 构造，来源含已有 survey、text analytics、SWEBOK。 | schema 构造过程 | strong | F6/F7/F8 分类 schema | 否 | 领域 taxonomy 不可直接迁移 |
| EV-008 | `paper_content.txt`, `paper.pdf` | §2.4 | Table 4 | App Review Analysis 93/87；SE Task 100/87；Mining Technique 90/80。 | reliability evidence | strong | 分类可靠性 | 否 | percentage agreement 不是全部质量证明 |
| EV-009 | `paper_content.txt`, `paper.pdf` | §3.2 | Table 7 | 九类 app review analysis 及频次。 | 分类枚举/统计 | strong | F6.1 | 否 | app review 领域特化 |
| EV-010 | `paper_content.txt`, `paper.pdf` | §3.3 | Table 9--11 | 四类 technique 及 analysis-technique 组合。 | 技术 schema/关系边 | medium | F7.1, R2 | 表 10/11 宽表需复核 | 不代表现代 LLM taxonomy |
| EV-011 | `paper_content.txt`, `paper.pdf` | §3.4 | Table 13 | 14 个 SE activities + Not specified。 | SE activity taxonomy | strong | F8 | 否 | 仅声称支持，不等于实际有效 |
| EV-012 | `paper_content.txt`, `paper.pdf` | §3.5 | Tables 16--20 | 109 empirical evaluation；23 datasets；16 tools；criteria/participants。 | evaluation schema | strong | F10--F18 | 否 | supplementary 未读 |
| EV-013 | `paper_content.txt`, `paper.pdf` | §3.6 | Tables 21--22 | 异质性太高，不做 meta-analysis；报告 ranges/medians 与 user-study synthesis。 | 结果合成纪律 | strong | F13/statistical synthesis | 否 | 不能跨任务合并效果 |
| EV-014 | `paper_content.txt`, `paper.pdf` | §4 | Discussion 4.2--4.10 | use case、reference model、small datasets、replication、practice impact、scalability、ML training 等 gaps。 | candidate finding | medium | 候选 finding | 否 | discussion 不能直接升级 final finding |
| EV-015 | `paper_content.txt`, `paper.pdf` | §5 | Threats to Validity | incompleteness、publication bias、screening/extraction/classification subjectivity、taxonomy reliability。 | 风险/边界 | strong | 迁移边界 | 否 | 不覆盖 LLM/provider drift |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-001 | 本文原生样本单位是 182 篇 primary studies，不是 tool、dataset、claim 或 roadmap action。 | sample_unit | 根对象 | EV-001, EV-003, EV-004 | strong | SUMMARY 样本单位 | 公开 dataset/tool 只是派生资产 |
| CLM-002 | 本文具备系统检索、纳排、抽取和编码方案，应按 SLR 主样本处理。 | review_type | corpus | EV-003, EV-004, EV-005 | strong | 主统计池资格判断 | 检索式全文需 PDF/原文精核 |
| CLM-003 | 原生维度树应复原为 F1--F18 extraction form，而非六叶通用接口。 | tree_repair | dimension_tree | EV-005, EV-006 | strong | 重写 review.md | 六叶只能作为跨论文投影 |
| CLM-004 | 本文是维度森林：F6/F7/F8 三套分类 schema 与 F10--F18 评价/复现 schema 并列作用于 primary study。 | tree_type | dimension_forest | EV-005, EV-007, EV-012 | strong | A1-DT 树型统计 | 细取值需 supplementary 精核 |
| CLM-005 | F6.1 的 app review analysis 类型有九类，可作为原文字段的完整枚举。 | leaf_value_space | F6.1 | EV-009 | strong | 叶子维度表 | 不可迁移为 Paper2 taxonomy |
| CLM-006 | F7.1 的 mining technique 有四类，可统计并与 analysis type 交叉。 | leaf_value_space | F7.1, R2 | EV-010 | medium | 技术维度 seed | 表 10/11 宽表需视觉核验 |
| CLM-007 | F8 的 SE activity 是层级枚举，含 Not specified，且多值允许。 | leaf_value_space | F8 | EV-011 | strong | SE activity 维度 | 声称支持不等于实践效果 |
| CLM-008 | 本文评价 schema 的强项是同时记录 objective、procedure、metrics、result、dataset、annotation、quality measure、replication package。 | method_seed | F10--F18 | EV-005, EV-012 | strong | Paper2 抽取表设计 | 未读 supplementary，不能逐篇填值 |
| CLM-009 | 原文统计观察可局部进入 A1 方法学统计池；app review 领域结论不可迁移为 Paper2 final finding。 | migration_boundary | statistical_pool | EV-009, EV-011, EV-013, EV-014 | strong | SUMMARY 资格说明 | final finding 需跨论文证据 |
| CLM-010 | 原文 discussion gaps 只能作为 candidate finding seed。 | candidate_finding | discussion | EV-014, EV-015 | medium | 候选 finding 台账 | 单篇 discussion 有作者解释成分 |
| CLM-011 | 表 14/15 的 analysis-SE activity 关系存在，但当前文本抽取不完整，需 A2a 视觉核验。 | proof_gap | R6 | EV-011 | weak | A2a 任务清单 | 不应用未核数值 |
| CLM-012 | 现有 `review.md` 需要返修，而非 blocked。 | audit_verdict | review.md | EV-005--EV-014 | strong | 返修计划 | 文件本身可读且材料完整 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering、证据门、reviewer gate，不做无证据强结论。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer 关注的 originality、soundness、clarity、reproducibility，对每个返修意见给出可执行证据。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用风险分级、claim-evidence gap、highest reviewer risk 的自检方式。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解研究上下文、再构造可执行结构和风险清单的流程。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用 “DO NOT FABRICATE DETAILS” 原则，未知处标注 unclear/not_verified。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化输出、任务/风险/证据对象分离的 schema 思路。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated completion 思路；本任务不启动 autoresearch loop，也不启动任何 subagent。

本输出最高风险 3 点：

1. 表 14/15 是宽表，`pdftotext -layout` 未完整抽出表格单元格。主线程合并时应打开 PDF 视觉核验 analysis-SE activity 的具体数值。
2. 未读取 supplementary material，因此逐篇 F6.2/F7.2/F9/F11/F18 原始值不能升级为完整统计字段，只能作为原文 schema seed。
3. 搜索式在 `paper_content.txt` 中缺失具体 query 内容，Fig. 1 只做文本段落级数量链核验；若 review.md 要记录完整检索式，必须回 PDF 版面或 publisher/supplementary 精核。

blocked / timeout / 文件缺失状态：未出现 blocked；未出现 timeout；指定的 `bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`、`paper.pdf` 均可读。未修改仓库文件，未 commit，未 push，未调用 subagent。