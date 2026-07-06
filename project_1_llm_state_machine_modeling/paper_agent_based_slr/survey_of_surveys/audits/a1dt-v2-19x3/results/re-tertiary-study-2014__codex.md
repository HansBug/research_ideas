### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-tertiary-study-2014` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是。已全文读取 966 行，覆盖摘要、方法、RQ、表 I--VI、limitations、conclusion、Appendix A。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。BibTeX 与 metadata 均已读取并用于核对题名、作者、年份、DOI、类型。 |
| 是否打开或核对 `paper.pdf` | 是。用 `pdfinfo` 核对 9 页 PDF 元信息，并用 `pdftotext -layout` 核对表 I--VI 与正文版面；未做截图式人工逐像素核验。 |
| 原文类型 | tertiary study；作者称为 systematic mapping tertiary study。 |
| 被编码样本单位 | 主单位：53 个 Requirements Engineering 领域的 distinct secondary studies，即 SLR / SMS / meta-analysis；辅单位：64 篇 publications，同一 study 可有 A/B/C 多个 publication。 |
| 样本数量 / 分母 | 53 unique SLR / SMS / meta-analysis；64 publications；质量评价实际可评 51 studies，因为 S3、S8 全文不可得；检索链含 primary search 267 hits、91 included before dedup、58 after duplicates、secondary searches 补入。 |
| 原生树类型 | 维度森林：study-level 主森林 + publication-level 辅助字段 + RQ3 gap-diagnosis 派生层。 |
| 主统计池资格 | 局部可统计。检索、纳排、样本分母、主题分组、scope 分类、QA rubric、citation 字段明确；但 topic naming、gap analysis 作者承认非穷尽，图 1--4 的精确数值仍需 PDF 视觉或表源复核。 |
| 总体判定 | needs repair。论文原生 schema 可复原；现有 `review.md` 仍需从六叶通用模板返修为本文自己的维度森林。 |

### 1. 原文证据阅读说明

已读取文件：

- `bibtex.bib`：核对 IEEE EmpiRE 2014、DOI、作者、页码。
- `metadata.json`：核对本地状态、review type、eligibility 字段。
- `paper_content.txt`：全文读取，主证据来源。
- `review.md`：读取既有审查内容，用于返修建议。
- `paper.pdf`：用 `pdfinfo` 与 `pdftotext -layout` 核对版面；表 I--VI 已做 layout-level 核验，图 1--4 的柱形/折线精确读数未做视觉精核。

关键证据锚点：

1. 摘要：说明本文是 RE 领域 SLR 的 tertiary study，采用自动检索和手工检索，识别 53 个 distinct reviews / 64 publications。
2. Introduction：定义 SLR、SMS、tertiary study，并说明本文目标是识别 RE 相关 SLR、覆盖主题和 primary study 数量。
3. Section II.A Planning：列出三个 RQ：覆盖的 RE 研究区域、SLR 质量、RE 主题覆盖缺口。
4. Table I：给出 QA1--QA4 质量评价 rubric，每项 Yes / Partial / No 分别计 1 / 0.5 / 0。
5. Search strategy：给出两个主检索概念、完整布尔检索式、数据库和手工补充来源。
6. Selection criteria：纳入条件为英文、SLR/SMS/meta-analysis、聚焦 RE；排除普通 literature review、survey、bibliographic study。
7. Data extraction：抽取 title、authors、year、publication type、venue/reference、citation、primary studies count、focus of SLR。
8. Table II：搜索执行与选择链，最终 53 studies / 64 publications。
9. Table III--V：publication type、scope classification、topic grouping、focus、primary study count、year。
10. RQ2 + Figures 2--4 + Table VI：51 个 study 可做 QA，42 个得分 >=2；记录 citation impact 与 top cited SLR。
11. RQ3：gap 分为 anomalies、low primary-study counts、ignored RE areas，并与 RE roadmap 对照。
12. Limitations：作者承认 topic grouping 主观、gap analysis preliminary / non-exhaustive、部分 publication details 或 full sources 缺失。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是 RE 领域已发表的二级研究：systematic literature review、systematic mapping study、meta-analysis。作者将同一研究的多个 publication 归并到同一 study ID，例如 A/B/C 后缀。因此必须区分 `study` 与 `publication` 两层单位。

2. 作者有系统检索、纳排、数据抽取和编码方案。检索覆盖 IEEE Xplore、ACM DL、ScienceDirect、Google Scholar、EI Compendex，并补充 snowballing、既有 tertiary studies、RE/SLR 相关会议和期刊手工检索。纳入条件、去重、secondary search、无法获得全文的例外均有记录。

3. 原文字段来源如下：
   - extraction form / data extraction：publication details、citation、primary studies count、focus of SLR。
   - classification schema：Table IV 的 scope 分类；Table V 的 RE topic grouping。
   - quality rubric：Table I 的 DARE-like QA1--QA4。
   - mapping table：Table II、III、IV、V、VI。
   - appendix：Appendix A 的 included studies reference + citation。
   - roadmap comparison：RQ3 中将 Table V topic 与 RE roadmap 的建议方向对照。
   - 不是 replication package；原文未提供机器可读抽取表。

4. RQ 不是维度树根本身，而是字段用途组织方式。RQ1 驱动 topic / scope / primary-study-count 字段；RQ2 驱动 QA rubric 与 citation impact；RQ3 驱动 gap-diagnosis 派生层。

5. 本文不是无系统样本库，不需要降级为 roadmap / guideline。需要降级的是 RQ3 的领域结论：gap list 和 ignored areas 只能作为候选 finding，因为作者自己说明 gap analysis 非穷尽。

### 3. 原生样本编码维度树 / 维度森林

```text
Root: RE secondary-study evidence base
单位: distinct SLR / SMS / meta-analysis study；辅单位: publication

├── A. Corpus Construction / Selection Pipeline
│   ├── search_concepts: Requirements Engineering × systematic-review family terms
│   ├── search_sources: IEEE, ACM, ScienceDirect, Google Scholar, EI Compendex
│   ├── supplementary_sources: snowballing, prior tertiary studies, RE/SLR venues/journals
│   ├── selection_criteria: English; SLR/SMS/meta-analysis; RE-focused
│   ├── exclusion: ordinary review/survey/bibliographic study
│   ├── search_counts: found, included, deduplicated, secondary additions
│   └── retrieval_exceptions: S3/S8 no full source; S40 channel unknown
├── B. Study / Publication Identity
│   ├── study_id: S1--S53, with A/B/C publication suffix where needed
│   ├── publication_reference: title, authors, year, venue/channel, complete reference
│   ├── publication_type: conference, journal, workshop, technical report, thesis, unknown
│   ├── study_type: SMS, meta-analysis, SLR
│   └── citation_count: Google Scholar count checked 2014-05-19
├── C. RQ1 Coverage Schema
│   ├── scope_class: state of the art, methods, techniques, tools, frameworks, technology
│   ├── main_topic_group: Table V RE topic groups
│   ├── focus_of_slr: free-text study focus within topic
│   ├── primary_study_count: numeric, plus NM/NF exceptions
│   ├── publication_year
│   └── overlap_note: e.g. S26/S39 overlap with Knowledge Management and RE
├── D. RQ2 Quality / Impact Schema
│   ├── QA1 inclusion/exclusion criteria: Yes/Partial/No -> 1/0.5/0
│   ├── QA2 search-space adequacy: Yes/Partial/No -> 1/0.5/0
│   ├── QA3 primary-study quality assessment: Yes/Partial/No -> 1/0.5/0
│   ├── QA4 information about primary studies: Yes/Partial/No -> 1/0.5/0
│   ├── total_quality_score: 0--4; 51 studies applicable
│   ├── quality_distribution / average_by_year: figures
│   └── top_cited_publications: S-ID, GS citations, pub channel, QA score
├── E. RQ3 Gap Diagnosis
│   ├── anomaly_type: inconsistent primary-study counts on same/broad topics
│   ├── low_coverage_type: low primary-study count in topic
│   ├── ignored_area_type: roadmap / known RE area not covered by selected SLR
│   ├── comparison_baseline: Nuseibeh & Easterbrook 2000; Cheng & Atlee 2007 roadmap
│   └── replication_need: candidate recommendation, not final transferable fact
└── F. Limitations / Future-use Filter
    ├── completeness_risk
    ├── topic_grouping_subjectivity
    ├── QA_rubric_dependency
    ├── gap_analysis_non_exhaustive
    └── future_filter: exclude non-peer-reviewed or low-quality SLR for roadmap work
```

Table V 的 topic group 可视为原文层级枚举，核心取值包括：Non Functional Requirements、Complete RE Process、Model Driven Development、Knowledge Management and RE、RE in GSD、RE in Software Product Lines、Requirements Management、Multi Agent Systems、Requirements Reuse、Value based RE、Virtual Reality Systems、Web Engineering、Creativity in RE、Requirements Elicitation、Stakeholders and users、Requirements Prioritization、Meta Modelling、Software Requirements Specifications、Requirements Verification / Validation / Evaluation、Requirements Traceability、Requirements Change Management、RE Education、Mobile Learning、Checklist for RE。该枚举是本篇样本内分类，不是 RE 全域 taxonomy。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L1 | 检索概念 | Corpus | 方法段 search string | RE 术语组与 SLR 术语组的布尔组合 | RE 同义词组 × review/mapping/meta-analysis 组 | 外部构造式 / 自由文本 | 未给则检索不可复现；本文已给 | 支撑检索可复验 | 可启发 Paper2 检索式结构 | E3 | 只迁移“术语组化”做法 |
| L2 | 检索源 | Corpus | 方法段 | 自动检索数据库 | IEEE、ACM、ScienceDirect、Google Scholar、EI | 完整枚举 | 未列来源则 coverage 风险 | 数据源覆盖统计 | 评估检索偏倚 | E3 | 不能迁移具体数据库到所有领域 |
| L3 | 补充检索源 | Corpus | 方法段 | snowballing、既有 tertiary、venue/journal 手工查找 | prior tertiary studies、RE/EASE/ESEM/REFSQ/REJ/ESE/IST 等 | 完整枚举 | 无补充检索则漏检风险 | search strategy completeness | 方法学启发 | E3 | 具体 venue 只适用于 RE |
| L4 | 纳入条件 | Corpus | selection criteria | 样本必须满足的三项条件 | English；SLR/SMS/meta-analysis；RE-focused | 完整枚举 / 布尔组合 | 不满足则排除 | eligibility filter | 定义主统计池边界 | E4 | 迁移结构，不迁移 RE 条件 |
| L5 | 排除类别 | Corpus | selection paragraph | 排除普通综述、survey、bibliographic studies | ordinary literature review / survey / bibliographic study | 完整枚举 | 未区分会污染样本 | 排除非系统样本 | boundary anchor | E4 | 适合 Paper2 区分系统/非系统综述 |
| L6 | 搜索数量链 | Corpus | Table II | 每个 source 的 found/included 与去重后总数 | numeric counts; secondary additions | 数值 | 缺失则无法重建分母 | PRISMA-like 分母统计 | 检索充分性候选证据 | E6 | 不迁移具体数字 |
| L7 | Study ID | Identity | Appendix A / execution | 聚合同一二级研究的 ID | S1--S53；A/B/C 后缀为 publication | 关系值 | 缺失则 study/publication 混淆 | 去重、归并、多报告识别 | 多版本报告方法学启发 | E6/E12 | 强迁移：必须区分 study vs publication |
| L8 | Publication type | Identity | Table III | publication 渠道类型 | conference, journal, workshop, technical report, thesis, unknown | 完整枚举 | S40 unknown | 渠道分布 | 质量/影响解释辅助 | E7 | 取值可迁移，分布不可迁移 |
| L9 | Study type | Identity | Results paragraph | 二级研究类型 | SMS、meta-analysis、SLR | 完整枚举 | 未标明则待核验 | 样本构成统计 | 不同综述类型边界 | E7 | 适合 Paper2 的 review_type 字段 |
| L10 | Scope class | RQ1 Coverage | Table IV | SLR 评估对象/产物范围 | state of the art, methods, techniques, tools, frameworks, technology | 完整枚举 | 无法分类则待核验 | scope 频次统计 | 方法/工具覆盖缺口 | E8 | 原文枚举可做 seed，非通用最终分类 |
| L11 | Main topic group | RQ1 Coverage | Table V | 作者按 title/abstract thematic analysis 得到的 RE 主题组 | 24 个左右 Table V topic groups | 层级枚举 | 作者承认命名可能不同 | topic coverage map | 领域缺口 seed | E8/E11 | 只能迁移“topic grouping 方法” |
| L12 | Focus of SLR | RQ1 Coverage | Table V | 单个 study 在 topic 内的具体焦点 | 自由文本标题/焦点 | 自由文本加理由 | 缺失则无法细分 topic | 细粒度描述 | 支撑相近 topic 聚合 | E8 | 不可直接统计为封闭枚举 |
| L13 | Primary-study count | RQ1 Coverage | Table V | 被该 SLR 纳入的 primary study 数量 | numeric；NM；NF；复合如 26+13 | 数值或特殊值 | NM=not mentioned；NF=not found | coverage proxy | anomaly / low coverage | E8/E10 | 可迁移字段，不能迁移阈值 |
| L14 | Publication year | RQ1 Coverage | Table V / Appendix A | study/publication 年份 | 2006--2014；NF exception | 数值 / 年份 | NF 表示未找到年份 | 时间分布 | trend seed | E7/E8 | 日期口径需按 publication vs study 区分 |
| L15 | QA1 | RQ2 Quality | Table I | 是否显式定义 inclusion/exclusion criteria | Yes=1, Partial=0.5, No=0 | 完整枚举 | S3/S8 不适用，因全文不可得 | QA 分数 | 综述严谨性 | E4/E9 | 可迁移为 quality rubric seed |
| L16 | QA2 | RQ2 Quality | Table I | search-space adequacy | Yes/Partial/No with scores | 完整枚举 | 同上 | QA 分数 | 搜索充分性风险 | E4/E9 | 阈值需按领域调整 |
| L17 | QA3 | RQ2 Quality | Table I | 是否评价 primary-study quality | Yes/Partial/No with scores | 完整枚举 | 同上 | QA 分数 | 质量缺陷 finding seed | E4/E9 | 可迁移为 evidence-quality 字段 |
| L18 | QA4 | RQ2 Quality | Table I | 是否呈现 primary-study 信息 | Yes/Partial/No with scores | 完整枚举 | 同上 | QA 分数 | 可复查性风险 | E4/E9 | 可迁移为 reporting completeness 字段 |
| L19 | Citation count | RQ2 Impact | Appendix A / Table VI | Google Scholar citation count，检查日 2014-05-19 | non-negative integer | 数值 | 缺失则影响字段不可用 | impact proxy | 质量与影响不一致观察 | E5/E9/E12 | citation 不等于质量 |
| L20 | Gap type | RQ3 Gap | RQ3 subsections | gap diagnosis 类型 | anomalies；low primary-study count；ignored RE areas | 完整枚举 | 作者承认 preliminary | 候选 finding 分类 | replication / neglected area | E10/E11 | 领域结论不可迁移 |
| L21 | Roadmap coverage status | RQ3 Gap | RQ3 roadmap comparison | roadmap topic 是否被 SLR 覆盖 | addressed / not covered / unclear | 外部分类法引用 | 未映射则 not_verified | topic-roadmap 对照 | future-work seed | E10 | 只迁移“against roadmap”方法 |
| L22 | Limitation type | Limitations | Section IV | 原文自承认限制 | completeness risk；topic naming subjectivity；QA guideline dependency；gap non-exhaustive | 完整枚举 / 自由文本 | 无限制说明则审计风险 | 降级依据 | 约束候选 finding | E11 | 应直接进入 review.md 降级规则 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R1 | publication | grouped_under | study_id | S1--S53 with suffix A/B/C | 无 study ID 会导致重复统计 | E6/E12 | 去重与分母修正 |
| R2 | study | has_publication_type_via | publication | conference/journal/workshop/report/thesis/unknown | S40 unknown | E7 | 区分 study-level 与 publication-level 字段 |
| R3 | study | classified_as | study_type | SLR/SMS/meta-analysis | 未标明则待核验 | E7 | review_type 统计 |
| R4 | study | assigned_scope | scope_class | 6 类 Table IV 枚举 | 无法归类则待核验 | E8 | RQ1 scope 分布 |
| R5 | study | assigned_topic | main_topic_group | Table V topic groups | 作者承认 topic naming 主观 | E8/E11 | topic map 与 gap seed |
| R6 | study | has_coverage_count | primary_study_count | numeric/NM/NF | NM/NF 为显式特殊值 | E8 | coverage proxy、anomaly 检测 |
| R7 | study | assessed_by | QA1--QA4 | 0/0.5/1 per item；total 0--4 | S3/S8 因全文不可得未评 | E4/E9 | 质量评价 |
| R8 | publication | has_impact_proxy | citation_count | Google Scholar citation integer | 未找到则 not_verified | E5/E9/E12 | impact proxy，不等于质量 |
| R9 | topic_group | compared_against | RE roadmap topic | addressed / not covered | roadmap mapping 不穷尽 | E10/E11 | RQ3 ignored-area 候选 finding |
| R10 | primary-study-count comparison | indicates_candidate | anomaly | inconsistent / suspicious / needs replication | 作者解释为 concern，不是证明错误 | E10 | 复制研究建议 |

发现显式关系型 schema：尤其是 publication grouped under study、study assigned topic/scope、study assessed by QA、topic compared to roadmap。没有发现可复用的 formal ontology 或机器可读 relation schema。

### 6. 统计观察、候选 finding 与 final finding 边界

**字段 / 统计表支持的统计观察**

- 原文明确支持：53 个 unique secondary studies、64 publications。
- 原文明确支持：64 publications 的渠道分布为 conference 31、journal 16、workshop 4、technical report 4、thesis 8、unknown 1。
- 原文明确支持：53 studies 中 12 个 SMS、1 个 meta-analysis，其余为 SLR。
- Table IV 支持 scope 分布：state of the art 33、methods 7、techniques 7、tools 4、frameworks 1、technology 1。
- Table V 支持 topic group、focus、primary-study count、year；其中 primary-study count 有 NM / NF 特殊值。
- RQ2 支持：51 个 study 可评价 QA；42 个得分 >=2；S3/S8 因全文不可得无法评价。
- Table VI 支持 top-cited publication 的 citation、publication channel、QA score。
- 作者基于图 3/4 观察：QA3/QA4 被大量忽略，2009 年后平均质量下降；若要写精确图中 count，需 PDF 视觉精核。

**discussion / recommendation / roadmap 候选 finding**

- 同主题或包含关系主题之间 primary-study count 差异很大，作者将其视为 SLR process validity / coverage concern。
- primary-study count 很低的 topic 可能是 neglected empirical RE area，也可能是对应 SLR 检索不足；必须保留双重解释。
- 与 RE roadmap 对照后，作者认为若干 hotspot 未被 selected SLR 覆盖。
- 作者建议 replication，并强调未来研究应关注 primary-study quality assessment。

**对 Paper2 可迁移的方法学启发**

- 必须区分“研究单位”和“发表单位”，避免多篇 publication 重复计算一个 study。
- `# primary studies` 可作为 coverage proxy，但只能和检索协议、topic 边界一起解释。
- QA rubric 可迁移为综述质量字段种子，尤其 QA3/QA4 对结果可靠性影响大。
- Topic grouping 若来自 title/abstract thematic analysis，应记录命名主观性和 reviewer agreement。
- Gap finding 应分层：统计异常、低覆盖、roadmap mismatch、作者解释、最终研究者裁决。

**绝不能迁移的领域结论**

- 不能把 RE 领域的具体 neglected topics 迁移为 Paper2 领域缺口。
- 不能把“RE SLR 质量下降”外推到其他 SE 子领域。
- 不能把 Google Scholar citation 当作质量本身。
- 不能把单篇 tertiary study 的 RQ3 preliminary gap analysis 升级为 final research finding。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | 现有“维度树复原”仍以六个通用 leaf 开场，虽然后文补了“原文 schema 主树”，但读者仍会把通用接口误读为原文树。 | 将主树替换为本审计第 3 节的原生维度森林；六叶接口只保留为“跨论文投影”，不得放在事实源位置。 |
| C | “是否目标证据池：否”和后文 `eligible_for_statistical_synthesis=true` / 局部可统计之间口径冲突。 | SUMMARY / 卡片建议改为：主统计池资格 = 局部可统计；理由 = 53/64 分母、Table IV/V、QA rubric 可统计，但 RQ3 gap 和 figure exact count 需降级。 |
| C | A.2 现有证据账本多为 `not_verified` 占位，没有精确到本文真实表 I--VI、Appendix A 和 limitations。 | 用本报告 A.2 草案重写，至少为 RQ、Table I、search/selection、data extraction、Table II--VI、RQ3、limitations 建锚。 |
| I | 样本单位未充分区分 study 与 publication。 | 在卡片、维度树、叶子表中固定：53 studies 是主单位；64 publications 是辅单位；QA applied to study，citation applied to publication。 |
| I | 原文 topic taxonomy 与 scope classification 未完整进入叶子层。 | 新增 Table IV 的 6 类完整枚举、Table V 的 topic group 枚举、focus free-text、primary-study count/NM/NF。 |
| I | QA rubric 应作为原生叶子，不只是“quality”概括项。 | 拆成 QA1--QA4，每项写 Yes/Partial/No 与 1/0.5/0 取值。 |
| I | RQ3 结论容易被写成领域 final finding。 | 明确 anomalies / low count / ignored areas 只作为 candidate finding；保留作者的双重解释和 non-exhaustive limitation。 |
| M | PDF 核验状态过旧。 | 更新为“已做 layout-level PDF 核验；图 1--4 精确数值仍需视觉核验”。 |
| M | 旧 v1 / 19x3 审计链接容易干扰 v2。 | 保留为历史参考即可；明确 v2 事实源以当前原文证据账本为准。 |

SUMMARY 当前表建议修正：

| 字段 | 建议值 |
|---|---|
| 样本单位 | distinct RE secondary studies；辅单位 publications |
| 样本数量 | 53 studies / 64 publications / 51 QA-applicable studies |
| 原生树类型 | 维度森林 |
| 统计池资格 | 局部可统计 |
| 主要降级原因 | RQ3 gap 非穷尽；topic naming 主观；图 1--4 精确数值需视觉核验 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| E1 | `paper_content.txt`; `paper.pdf` | Abstract / Introduction | Page 2; lines 23--40, 88--99 | 作者说明本文是 RE SLR 的 tertiary study，并报告 53 reviews / 64 publications。 | root / denominator | strong | 原文类型、主样本单位、样本分母 | 否 | 不支撑其他领域统计 |
| E2 | `paper_content.txt`; `paper.pdf` | Section II.A Planning | lines 112--123 | 三个 RQ 分别对应 coverage、quality、gap。 | RQ-to-field mapping | strong | RQ 与字段用途关系 | 否 | RQ 不是原生树本身 |
| E3 | `paper_content.txt`; `paper.pdf` | Section II.A Planning | lines 125--146; Table I 前 | RQ1 用 title/abstract 分组；RQ2 用 DARE-like checklist；QA applied to whole study。 | coding-method | strong | topic grouping、quality unit | 否 | grouping 主观性需结合 limitations |
| E4 | `paper_content.txt`; `paper.pdf` | Table I | lines 147--178 | QA1--QA4，每项 Yes/Partial/No 对应 1/0.5/0。 | quality rubric | strong | QA1--QA4 叶子 | 是，已 layout 核验 | rubric 是 seed，不等于最终质量理论 |
| E5 | `paper_content.txt`; `paper.pdf` | Search strategy | lines 184--220 | 给出检索词、数据库、snowballing、手工 venue/journal 检索。 | search schema | strong | 检索源、检索式、补充检索 | 否 | RE venue 不可直接迁移 |
| E6 | `paper_content.txt`; `paper.pdf` | Selection / extraction | lines 221--247 | 三项纳入条件；抽取 publication details、citation、# primary studies、focus。 | inclusion / extraction form | strong | 纳排、数据抽取叶子 | 否 | 只说明本文字段，不说明全部隐藏表 |
| E7 | `paper_content.txt`; `paper.pdf` | Execution / Table II | lines 249--288 | 搜索执行链给出 source counts、dedup、secondary additions、53/64。 | denominator chain | strong | 搜索数量链、样本数量 | 是，已 layout 核验 | 不可将 hits 当最终样本 |
| E8 | `paper_content.txt`; `paper.pdf` | Execution exceptions | lines 290--298 | S3/S8 无全文；S40 channel unknown；多个 publication grouped under same study。 | missingness / relation | strong | 缺失值语义、study-publication 关系 | 否 | 不代表样本应排除 |
| E9 | `paper_content.txt`; `paper.pdf` | Results / Table III | lines 300--331 | 64 publications 的年份范围、渠道类型；12 SMS、1 meta-analysis，其余 SLR。 | sample description | strong | publication type、study type | 是，已 layout 核验 | publication type 是辅单位字段 |
| E10 | `paper_content.txt`; `paper.pdf` | RQ1 / Table IV--V | lines 332--430 | Table IV scope 六类；Table V topic group、focus、#PS、year。 | coverage schema | strong | scope、topic、focus、primary-study count | 是，已 layout 核验 | topic group 非 RE 全域 taxonomy |
| E11 | `paper_content.txt`; `paper.pdf` | RQ2 / Figures 2--4 / Table VI | lines 433--493 | 51 studies 可评 QA；42 scored >=2；top cited table。 | quality / impact schema | medium-strong | QA score、citation impact、trend | 是，图精确数值需视觉核验 | citation 不等于质量 |
| E12 | `paper_content.txt`; `paper.pdf` | RQ3 | lines 494--576 | gap 分 anomalies、low counts、ignored areas，并与 RE roadmap 对照。 | candidate finding schema | medium | gap type、roadmap coverage | 否 | 作者承认 preliminary，不能作 final finding |
| E13 | `paper_content.txt`; `paper.pdf` | Limitations | lines 577--615 | 样本完整性、topic naming、QA guideline、gap analysis 均有局限。 | downgrade rule | strong | 缺失值语义、迁移边界 | 否 | 支撑降级，不支撑反向强结论 |
| E14 | `paper_content.txt`; `paper.pdf` | Conclusion / Appendix A | lines 617--645, 697--966 | 总结 53/64、replication、QA 注意事项；Appendix A 列 study references 与 citations。 | conclusion / appendix support | medium-strong | candidate finding、citation field | Appendix layout 需逐页精核 | appendix citation 是 2014 时间点 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C1 | 本文是 RE 领域 tertiary study，主样本单位为 distinct secondary studies。 | tree_root | Root | E1,E2 | strong | review.md 卡片、SUMMARY 样本单位 | 不代表 primary studies |
| C2 | 本文分母应写为 53 studies / 64 publications，并保留 51 QA-applicable studies。 | denominator | Corpus / QA | E1,E7,E8,E11 | strong | 统计池资格、叶子表 | S3/S8 未全文可得 |
| C3 | 原生结构是维度森林，而非六叶通用树。 | tree_type | 全部字段 | E2--E13 | strong | 维度树复原 | 六叶接口只能作投影 |
| C4 | Table IV 的 scope classification 是完整枚举字段。 | leaf_definition | Scope class | E10 | strong | 叶子维度表 | 只覆盖 selected RE SLR |
| C5 | Table V 的 topic grouping 是样本内主题分类，不是 RE 全域 taxonomy。 | boundary | Main topic group | E10,E13 | medium-strong | topic leaf、迁移边界 | 作者承认非穷尽且命名主观 |
| C6 | `# of PS` 可作为 coverage proxy，并支持 anomaly / low coverage 候选发现。 | statistical_observation | Primary-study count | E10,E12 | medium | candidate finding | 数字差异不自动证明某 SLR 错误 |
| C7 | QA1--QA4 是本文最清晰的质量 schema。 | leaf_definition | QA rubric | E4,E11 | strong | quality leaf | DARE-like rubric 有自身局限 |
| C8 | Google Scholar citation count 是 publication-level impact proxy，不是 study quality。 | boundary | Citation count | E5,E11,E14 | strong | impact field | citation date 固定为 2014-05-19 |
| C9 | RQ3 的 anomalies、low-count topics、ignored areas 只能作为候选 finding。 | finding_boundary | Gap diagnosis | E12,E13 | strong | Paper2 候选启发 | 作者称 gap analysis preliminary / non-exhaustive |
| C10 | 本文可迁移的方法学是 study/publication 分层、QA rubric、coverage proxy、roadmap comparison。 | migration | Method seed | E6--E13 | medium-strong | Paper2 schema seed | 不迁移 RE 具体领域结论 |
| C11 | 现有 `review.md` 需要返修，因为仍把通用接口放在原生树事实源位置。 | repair | review.md | 已读 review.md + E2--E13 | strong | 返修任务 | 不要求删除历史审计，只需降级其事实地位 |

### 9. 技能使用与自我审查记录

已读取并采用的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence workflow、evidence gate、unsupported claim 降级原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 必须具体、证据与复现可查的原则。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用五维自审、claim audit、风险优先返修口径。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解上下文、显式标注 ambiguity、输出结构化 plan/schema 的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用严格贴合原文、不编造缺失细节的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：采用结构化字段、风险、任务依赖和输出 schema 思维组织审计。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 的完成观；本任务未启动 autoresearch loop，也未启动任何 subagent。

本输出最高风险 3 点：

1. Table V topic group 从 PDF layout 与 text 抽取复原，虽然已核对版面，但若要作为正式枚举进入主统计，需要人工逐项对照 PDF 表格。
2. 图 1--4 的精确数值没有视觉读图，只采用正文已明说的统计结论；主线程合并时不要从图像推新数字。
3. RQ3 roadmap coverage 是作者的 preliminary analysis；合并时必须保持 candidate finding，不要写成 Paper2 的 final finding。

Blocked / timeout / 文件缺失：

- 未出现 blocked。
- 未出现 timeout。
- 指定四个本地文件均已读取。
- 已核对 PDF，但不是截图式视觉审校。
- 未修改文件、未 commit、未 push、未发 gh comment、未启动 subagent。