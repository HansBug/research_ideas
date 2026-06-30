### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `research-artifacts-secondary-studies` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已全文读取 358 行，并按章节、表 1、结论与限制逐项审计。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；已读取 BibTeX 与 metadata，确认题名、作者、DOI、IST 期刊信息、PDF 来源和本地 eligibility 元数据。 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 与 `pdftotext -layout` 对 PDF 页数、Table 1、方法页和结果页做了本地版面文本核验；未做截图级视觉核验。 |
| 原文类型 | SMS（systematic mapping study）；对象是 SE secondary studies，带 tertiary-like 元研究性质。 |
| 被编码样本单位 | 软件工程领域 secondary study 论文 / 文章。 |
| 样本数量 / 分母 | Scopus 初检 643 篇；最终纳入 537 篇；artifact 可得 169 / 537；permanent repository 65 / 169 或 65 / 537；2023 年分母 79。 |
| 原生树类型 | 维度森林：语料筛选维度 + artifact availability / storage / reporting / trend 统计维度。 |
| 主统计池资格 | 局部可统计：可进入“系统样本库 + 原生编码字段”统计池；但 artifact 内容质量、artifact 类型清单和 Paper2 领域结论只能作 seed / 启发，不能直接统计迁移。 |
| 总体判定 | needs repair；原文可用，但现有 `review.md` 仍需按 A1-DT v2 重写维度树、证据账本和关系边。 |

### 1. 原文证据阅读说明

已读取本地 `bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md` 全文。PDF 核验覆盖 `paper.pdf` 的 6 页元信息、Methods 页、Table 1 所在页和 Results / Limitations 页的 layout 文本；没有打开 Zenodo artifact，也没有对出版商最终排版做外部核验。

关键证据锚点如下：

| 证据锚点 | 原文章节 / 表图 | 证据内容 |
|---|---|---|
| E1 | Abstract | 目标是评估 SRs 如何报告 research artifacts，并分析 537 篇 secondary studies。 |
| E2 | Introduction | 作者给出 artifact 必要性的四个理由：replicability、trust、updates、automation。 |
| E3 | Methods §2 | 原文自称 systematic mapping study，遵循 Petersen 指南与 SIGSOFT Empirical Standards checklist。 |
| E4 | §2.1 Search process | Scopus 检索、15 个期刊 ISSN、2013--2023、标题关键词，初始 643 篇。 |
| E5 | §2.2 Study selection | IC1--IC3：年份、secondary study、SE 相关；最终 537 篇。 |
| E6 | §2.3 Data extraction | 两轮抽取：人工全文筛查 dedicated sections；关键词脚本输出命中前后 100 字符后人工检查。 |
| E7 | §2.3 Data extraction | 抽取判断包括是否有 external resource，以及是否位于 Figshare / Zenodo / Mendeley 等 permanent repository。 |
| E8 | Table 1a / 1b | 原生字段包括 venue、year、Yes、Permanent repo、No、By Request、Dead Link、Dedicated section。 |
| E9 | Results RQ1--RQ3 | 169 / 537 有 artifact；65 / 169 使用 permanent repository；50 / 169 有 dedicated section。 |
| E10 | Results RQ4 / Table 1c | logistic regression 以 artifact availability 为响应变量，解释变量为 year 与 journal。 |
| E11 | Limitations | 排除会议、只用 Scopus、只纳入 2013--2023 是外推边界。 |
| E12 | Conclusion / Future work | 建议强制发布 artifacts、使用 DOI permanent repositories，并指出 artifact quality 是未来工作。 |

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 537 篇软件工程 secondary studies。它们不是工具、数据集或 artifact 本身；artifact 是每篇 secondary study 的被抽取属性。

2. 作者有系统检索、纳排和数据抽取流程。检索使用 Scopus、15 个期刊 ISSN、标题关键词和 2013--2023 时间窗；纳入标准是年份、secondary study、SE 相关；数据抽取分人工全文筛查和关键词脚本辅助检查。

3. 字段来源主要是 data extraction protocol、Table 1、logistic regression model。正文没有给出完整 artifact type taxonomy，也没有给出 artifact quality rubric。Zenodo artifact 可能包含逐篇清单或更细字段，但本轮未打开核验，因此只能标为待核验。

4. RQ 不是树根本身，而是字段用途 / 结果组织方式。真正根对象是 included secondary study；RQ1 使用 availability 字段，RQ2 使用 storage / permanent repository 字段，RQ3 使用 reporting / dedicated section 字段，RQ4 使用 year / journal covariates 与 logistic regression。

5. 本文不是 roadmap / guideline，也不是无系统样本库。无需降级为 boundary-only；但因正文只统计 availability / storage / reporting，不评估 artifact 质量，所以 artifact quality 和细粒度 artifact content 只能降级为 `schema_seed` / `not_verified`。

### 3. 原生样本编码维度树 / 维度森林

```text
included_secondary_study  (n = 537)
├── corpus_identity
│   ├── publication_channel / venue
│   ├── publication_year
│   ├── source_database = Scopus
│   ├── title_keyword_match
│   └── inclusion_basis
│       ├── IC1: 2013--2023
│       ├── IC2: secondary study
│       └── IC3: SE-related
├── artifact_availability
│   ├── availability_status
│   │   ├── Yes
│   │   ├── No
│   │   ├── By Request
│   │   └── Dead Link
│   └── external_resource_reference
├── artifact_storage_persistence
│   ├── permanent_repository_flag
│   ├── permanent_repository_examples
│   │   ├── Zenodo
│   │   ├── Figshare
│   │   └── Mendeley Data
│   └── DOI / persistent-storage expectation
├── reporting_anchor
│   ├── dedicated_section_flag
│   ├── data_availability_statement
│   └── statement_problem_type
│       ├── no data was used
│       └── available upon request
└── statistical_context
    ├── yearly_statistics
    ├── publication_channel_statistics
    └── logistic_regression
        ├── response: artifact available
        ├── predictor: ordered scaled year
        ├── predictor: journal
        └── reference category: IEEE TSE
```

缺失部分：正文没有逐篇 artifact 清单、关键词列表、repository URL 列、link check 时间戳、artifact 内容质量评分或 artifact type taxonomy。A2a 精核应打开 Zenodo DOI `10.5281/zenodo.15488074`，确认 supplementary 是否包含这些字段。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 样本单位 | root | Abstract / Methods | 被纳入分析的 SE secondary study 论文 | 537 included studies | 数值 / 分母 | 不适用 | 定义所有比例分母 | 限定外推对象 | E1, E5 | 不可外推到 primary studies 或会议论文 |
| L2 | publication venue | corpus_identity | Table 1a | 样本发表渠道 | 15 个期刊 | 完整枚举 | 不在 15 期刊即不入样本 | venue 交叉统计、回归变量 | 期刊差异候选观察 | E4, E8, E10 | 不代表 SE 全部 venue |
| L3 | publication year | corpus_identity | §2.1 / Table 1b | 样本发表年份 | 2013--2023 | 完整枚举 / 数值 | 年份外论文被排除 | 年度趋势、回归变量 | open data adoption trend | E4, E8, E10 | 不可外推到 2012 前或 2024 后 |
| L4 | inclusion criteria | corpus_identity | §2.2 | 样本进入最终集合的条件 | IC1 / IC2 / IC3 | 布尔过滤条件 | 不满足则排除 | 分母链审计 | scope boundary | E5 | 不是样本内容分类 |
| L5 | artifact availability status | artifact_availability | §2.3 / Table 1 | 是否提供 research artifact 及访问状态 | Yes / No / By Request / Dead Link | 完整枚举 | 未发现链接通常归 No；失效归 Dead Link | 核心统计字段 | artifact availability gap | E6, E8, E9 | 不等于 artifact 质量 |
| L6 | external resource reference | artifact_availability | §2.3 | 论文是否包含指向外部资源的引用 | 有 / 无 / 待核验 | 布尔 | 未报告或未发现为无 | 支撑 availability 判定 | 报告透明度候选观察 | E6, E7 | 正文未列逐篇 URL |
| L7 | permanent repository flag | artifact_storage_persistence | §2.3 / RQ2 / Table 1 | artifact 是否位于 permanent repository | 是 / 否 / 不适用 | 布尔 | 无 artifact 时不适用 | 65 / 169 与 65 / 537 统计 | persistence gap | E7, E8, E9 | 不等于可复现性充分 |
| L8 | repository provider | artifact_storage_persistence | §2.3 | permanent repository 示例 / 类型 | Zenodo / Figshare / Mendeley Data / 其他待核验 | 外部分类法引用 / 自由文本 | 正文未给逐篇 provider 时待核验 | A2a 后可统计 | repository preference seed | E7 | 正文示例不是完整枚举 |
| L9 | DOI / persistent identifier expectation | artifact_storage_persistence | RQ2 / Conclusion | permanent storage 应带 DOI | DOI / 无 DOI / 待核验 | 布尔 / 自由文本 | 正文未单列 DOI 字段时待核验 | persistence quality seed | DOI adoption gap | E9, E12 | 不要把 “permanent repo” 拆成已核验 DOI，除非 supplementary 支持 |
| L10 | dedicated section flag | reporting_anchor | §2.3 / RQ3 / Table 1b | 是否有数据 / artifact 可用性专门章节 | 是 / 否 | 布尔 | 无专门章节为否 | 72 / 537；50 / 169 | reporting anchor gap | E6, E8, E9 | 有章节不代表有 artifact |
| L11 | statement problem type | reporting_anchor | Conclusion | dedicated section 中的问题声明 | “no data was used” / “available upon request” / 其他 | 自由文本加理由 | 未给数量则弱证据 | 不宜主统计 | false transparency candidate | E12 | 正文只说 some，不能编数量 |
| L12 | dead link status | artifact_availability | Table 1 / Conclusion | artifact 链接失效状态 | Dead Link / 非 Dead Link | 布尔 / 枚举 | 未检查时间不明 | 22 / 537；2023 非永久链接 2 / 19 | link rot risk | E8, E12 | dead link 是时间敏感事实 |
| L13 | by request status | artifact_availability | Table 1 / Conclusion | artifact 仅可请求获取 | By Request / 非 By Request | 布尔 / 枚举 | 不可视为开放可用 | 16 / 537 | open access gap | E8, E12 | 不等同于 open artifact |
| L14 | logistic response | statistical_context | Table 1c / RQ4 | 回归模型响应变量 | artifact available | 布尔 | By Request / Dead Link 如何二值化正文未细述 | 回归建模 | trend finding | E10 | 不可推出因果 |
| L15 | year ordered factor | statistical_context | RQ4 / Table 1c | 年份作为 scaled ordered factor | 2013--2023 scaled | 数值 / 有序变量 | 不适用 | odds ratio 2.31 | adoption trend | E10 | 仅限样本窗口 |
| L16 | journal factor | statistical_context | RQ4 / Table 1c | 期刊作为回归解释变量 | 期刊；TSE reference；少于 10 篇排除 | 层级枚举 / 模型变量 | 样本 <10 期刊不入模型 | venue effect | venue gap candidate | E10 | 不迁移具体期刊结论到 Paper2 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | search result | filtered_by | included_secondary_study | IC1 / IC2 / IC3 | 不满足则排除 | E4, E5 | 复原分母链：643 → 537 |
| R2 | included_secondary_study | has_status | artifact_availability_status | Yes / No / By Request / Dead Link | 未发现外部资源通常归 No | E6, E8 | 核心样本编码 |
| R3 | availability_status = Yes | may_have | permanent_repository_flag | true / false | 无 artifact 时不适用 | E7, E8, E9 | 区分 availability 与 persistence |
| R4 | included_secondary_study | has_reporting_anchor | dedicated_section_flag | true / false | 无专门章节为 false | E6, E8, E9 | 区分报告位置与真实开放 artifact |
| R5 | dedicated_section_flag | does_not_imply | artifact_available | true / false | 需读取章节内容 | E9, E12 | 防止把 Data Availability section 误算为 artifact |
| R6 | artifact_availability | modeled_by | year + journal | ordered year / journal factor | 样本不足期刊被排除 | E10 | 支撑 RQ4 回归观察 |
| R7 | storage type | affects_risk_of | dead link | dead / alive / not checked | 检查日期正文未报告 | E9, E12 | 支撑 permanent repository recommendation |

未发现更复杂的关系型 schema，例如 artifact 类型与质量评分之间的关系、artifact 内容项之间的依赖、或逐篇 repository URL 与 link-check 时间戳的结构化边。这些若存在，只能在 Zenodo artifact 精核后补入。

### 6. 统计观察、候选 finding 与 final finding 边界

**字段 / 统计表支持的统计观察**

| 观察 | 证据 | 强度 |
|---|---|---|
| 537 篇中 169 篇提供 research artifact，占 31.5%。 | RQ1 / Table 1 | high |
| 65 / 169 有 artifact 的论文使用 permanent repository；以全体为分母是 65 / 537。 | RQ2 / Table 1 | high |
| 2023 年 49 / 79 有 artifact，24 / 79 使用 permanent repository。 | Abstract / Table 1b | high |
| 50 / 169 有 artifact 的论文有 dedicated section；Table 1b 另给 dedicated section 总计 72 / 537。 | RQ3 / Table 1b | medium；分母必须分开 |
| 年份是 availability 的显著预测因子，odds ratio 为 2.31。 | RQ4 / Table 1c | high for association |
| 部分期刊相对 TSE 的 artifact availability odds 更低。 | Table 1c | medium；样本与模型限制明显 |

**discussion / recommendation 提出的候选 finding**

| 候选 finding | 可用性 |
|---|---|
| SE secondary studies 的 artifact availability 正在改善。 | 可作候选 finding；不能解释为因果。 |
| permanent repository / DOI 采用仍不足。 | 可作强候选 finding，分母清楚。 |
| Data Availability section 可能造成“形式透明”，如 no data / upon request。 | 可作候选风险；正文未给精确数量。 |
| journals should enforce artifact reporting practices。 | 作者建议，可作 policy recommendation seed。 |
| artifact quality 需要未来研究。 | 明确 future work，不是本文已完成结论。 |

**对 Paper2 可迁移的方法学启发**

可迁移的是字段设计和证据纪律：availability、persistence、DOI、dead link、by request、dedicated section、分母区分、人工筛查 + 关键词上下文检查、year / venue 等上下文变量。也可迁移“有 artifact 不等于 artifact quality”的边界。

**绝不能迁移的领域结论**

不能把 31.5%、62.0%、30.4%、2.31 odds ratio、IST / TSE 等期刊差异迁移为 Paper2 目标领域事实。不能把正文未核验的 Zenodo 内部清单当作 artifact type taxonomy。不能把 dedicated section 直接当作 artifact 可用性。

### 7. 对现有 `review.md` 的返修建议

| 级别 | 问题 | 最小返修建议 |
|---|---|---|
| C | 当前维度树仍残留六个通用接口叶子作为主体结构，虽然写了“不是原文全集”，但表格主体仍会误导后续统计。 | 删除或下沉 `leaf-scope / corpus / taxonomy / method / evidence / finding` 六叶主表，把本报告第 3--5 节的原生维度森林作为事实源。 |
| C | `review.md` 引入 v1 / 19×3 / codex-claude-deepseek 历史审计作为返修来源；本任务明确禁止把旧 v1 审计当模板。 | 将历史审计引用移到“历史背景 / 不作事实源”，A.2/A.3 只保留本地原文证据。 |
| C | A.2 证据账本多为泛化行，如 taxonomy / roadmap / action point；与本文实际 schema 不匹配。 | 用具体证据替换：Search process、IC1--IC3、Data extraction、Table 1a/1b/1c、Limitations、Conclusion。 |
| C | 关系边 `method-evidence`、`taxonomy-finding` 不是本文显式关系边。 | 替换为 availability→permanent repo、dedicated section≠artifact、availability modeled by year/journal 等原文关系。 |
| I | `是否目标证据池` 写成“否”过强；本文有系统样本库和统计表。 | 改为“局部可统计”：availability / storage / reporting / trend 可统计；artifact quality / artifact type taxonomy 不可统计。 |
| I | `artifact type` 主干不稳。正文没有 artifact 类型本体，只说 research artifact 是否存在及存放方式。 | 将 `artifact type` 改为 `artifact availability / storage / reporting`；artifact content/type 标为 Zenodo 待核验。 |
| I | Table 1 的分母需要更清楚。 | 明确 Yes/No/By Request/Dead Link 以 537 为分母；Permanent repo 可用 65/169 或 65/537；Dedicated section 有 50/169 与 72/537 两种口径。 |
| I | A.1--A.4 需要补充真实证据。 | 新增本报告 A.2/A.3 草案；每条证据给章节、表号、证据强度和外推限制。 |
| M | 历史草稿字段如 GitHub / OSF、license、README、raw outputs 等超出正文证据。 | 可保留在 Paper2 设计启发中，但必须标为外推字段，不进入“原生树”。 |
| M | PDF 核验状态表述可更精确。 | 写明已做 `pdftotext -layout` 核验，未做视觉截图级核验，未核验 IST 出版商版。 |
| M | SUMMARY 当前表建议修正。 | 样本单位：`secondary study paper`；样本数量：`537 included / 643 initial`；原生树类型：`维度森林`；统计池资格：`局部可统计`。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-RA-01 | `paper_content.txt` | Abstract | 目标 / 方法 / 结果摘要 | 研究分析 537 篇 secondary studies 的 artifact availability 与 reporting。 | root / sample unit | high | root, L1 | 否 | 只支撑本文样本单位。 |
| EV-RA-02 | `paper_content.txt` | Introduction | four reasons | artifact 支撑 replicability、trust、updates、automation。 | motivation | medium | candidate finding | 否 | 是作者论证，不是编码字段。 |
| EV-RA-03 | `paper_content.txt`; `paper.pdf` | §2 Methods | systematic mapping statement | 作者称按 Petersen 指南与 SIGSOFT checklist 做 systematic mapping。 | method type | high | 原文类型 | 否 | 不代表有质量评分表。 |
| EV-RA-04 | `paper_content.txt`; `paper.pdf` | §2.1 Search process | Scopus query | Scopus、15 期刊 ISSN、title keywords、2013--2023，初检 643。 | corpus protocol | high | L2, L3, R1 | 已做 layout 文本核验 | 不覆盖会议论文。 |
| EV-RA-05 | `paper_content.txt`; `paper.pdf` | §2.2 Study selection | IC1--IC3 | 纳入标准为年份、secondary study、SE 相关；最终 537。 | selection / denominator | high | L1, L4, R1 | 已做 layout 文本核验 | ACM CSUR / CSR 有人工 SE 判断。 |
| EV-RA-06 | `paper_content.txt`; `paper.pdf` | §2.3 Data extraction | manual + automatic extraction | 人工全文筛查 dedicated sections；关键词脚本输出上下文后人工检查。 | extraction method | high | L5, L6, L10 | 已做 layout 文本核验 | 关键词列表正文未给。 |
| EV-RA-07 | `paper_content.txt`; `paper.pdf` | §2.3 Data extraction | permanent repository check | 检查 external resource 以及是否位于 Figshare / Zenodo / Mendeley 等 permanent repository。 | storage field | high | L7, L8, R3 | 已做 layout 文本核验 | provider 示例不是完整枚举。 |
| EV-RA-08 | `paper_content.txt`; `paper.pdf` | Table 1a / 1b | publication channel and yearly statistics | 字段包括 Venue、Total、Yes、Permanent repo、No、By Request、Dead Link、Dedicated section。 | native schema / stats | high | L2, L3, L5, L7, L10, L12, L13 | 已做 layout 文本核验；建议视觉核验 | 表 1 很紧凑，分母需单独说明。 |
| EV-RA-09 | `paper_content.txt`; `paper.pdf` | RQ1--RQ3 Results | 169/537, 65/169, 50/169 | availability、permanent repository、dedicated section 的核心比例。 | statistical result | high | 统计观察 | 已做 layout 文本核验 | dedicated section 的 50/169 与 72/537 不能混用。 |
| EV-RA-10 | `paper_content.txt`; `paper.pdf` | RQ4 / Table 1c | logistic regression | artifact availability 由 publication year 和 journal 建模；year odds ratio 2.31。 | model relation | high | L14, L15, L16, R6 | 已做 layout 文本核验 | 关联不是因果。 |
| EV-RA-11 | `paper_content.txt` | Limitations | conference / Scopus / year scope | 排除会议、只用 Scopus、只含 2013--2023。 | boundary | high | 迁移边界 | 否 | 限制所有外推。 |
| EV-RA-12 | `paper_content.txt` | Conclusion / Future work | recommendations | 建议 permanent repositories with DOIs；artifact quality 是未来工作。 | candidate finding / limitation | high | 候选 finding | 否 | 质量字段不是已完成结果。 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CL-RA-01 | 本文原生样本单位是 SE secondary study 论文，最终分母为 537。 | sample_unit | root, L1 | EV-RA-01, EV-RA-05 | high | SUMMARY 样本单位 / 数量 | 初检 643 不是最终分母。 |
| CL-RA-02 | 本文是 systematic mapping study，不是 roadmap / guideline。 | paper_type | 原文类型 | EV-RA-03 | high | 审计结论卡片 | 对象为 secondary studies，带元研究性质。 |
| CL-RA-03 | 原生维度森林核心为 corpus、artifact availability、storage persistence、reporting anchor、statistical context。 | tree_type | 第 3 节维度树 | EV-RA-04 至 EV-RA-10 | high | 维度树复原 | 不包含 artifact quality taxonomy。 |
| CL-RA-04 | availability status 的原文统计取值至少包括 Yes / No / By Request / Dead Link。 | leaf_definition | L5 | EV-RA-08, EV-RA-09 | high | 叶子维度表 | 是否还有 supplementary 细分待核验。 |
| CL-RA-05 | permanent repository 是 availability 的 persistence 子维度，不能与 artifact availability 混同。 | relation_edge | R3 | EV-RA-07, EV-RA-08, EV-RA-09 | high | 关系边 / Paper2 字段设计 | DOI 独立字段需 supplementary 核验。 |
| CL-RA-06 | dedicated section 是 reporting anchor，不保证 artifact 真实可用。 | relation_edge | R4, R5 | EV-RA-06, EV-RA-08, EV-RA-12 | high | 关系边 / 风险提示 | 正文只给部分 problematic statements，未给完整分类数量。 |
| CL-RA-07 | 年份与期刊可作为 availability 的统计上下文变量。 | statistical_relation | L14-L16, R6 | EV-RA-10 | high | 统计观察 | 关联不能解释为因果；少样本期刊被排除。 |
| CL-RA-08 | 本文可进入局部统计池，但只限 availability / storage / reporting / trend 字段。 | pool_eligibility | 主统计池资格 | EV-RA-04 至 EV-RA-12 | medium-high | SUMMARY 统计池字段 | artifact quality、artifact type、Paper2 领域结论不进入统计。 |
| CL-RA-09 | 对 Paper2 可迁移的是 evidence-asset audit schema，不是本文比例和期刊结论。 | migration_boundary | Paper2 启发 | EV-RA-09, EV-RA-10, EV-RA-11 | high | 可迁移边界 | 单篇统计不可外推。 |
| CL-RA-10 | 现有 `review.md` 需要重写原生树与 A.2/A.3，避免通用六叶模板和历史 v1 审计污染事实源。 | repair_action | review.md | 本轮全文审计 + EV-RA-04 至 EV-RA-10 | high | 返修任务 | 本报告未直接修改文件。 |

### 9. 技能使用与自我审查记录

已读取并采用以下技能 / 指南文件：

| 文件 | 采用原则 |
|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | claim-evidence workflow；没有证据则削弱或标 gap。 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | 审稿式检查 novelty、soundness、clarity、reproducibility；返修建议需具体可执行。 |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | 用高风险问题、claim-evidence gap、revision priority 组织返修。 |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 先理解研究上下文，再给结构化计划；不清楚处显式标注。 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | 严格贴合原文方法、数据、实验设置，不补造细节。 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | 用结构化对象、任务、风险和边界表达审计结果。 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 采用 artifact-gated / validator-gated 思路：结论必须由可审计证据支撑，不能因“看似完成”而结束。 |

最高风险 3 点：

1. Zenodo artifact 未打开，可能包含逐篇 artifact 清单、关键词、repository URL 或更细字段。主线程合并时应核验 DOI `10.5281/zenodo.15488074`。
2. PDF 核验是 layout 文本级，不是截图级视觉核验；Table 1 正式入库前建议人工打开 PDF 视觉确认列对齐和分母。
3. DOI / permanent repository 在正文中高度绑定，但正文没有单独列出 DOI 字段的逐篇取值；主线程不要把 DOI adoption 写成已独立统计字段，除非 supplementary 支持。

本任务未出现 blocked、timeout 或文件缺失。未启动 subagent，未修改文件，未 commit / push / gh comment。