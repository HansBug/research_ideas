# kitchenham-charters-2007-slr-guidelines · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；已读 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。本审计按 claim-evidence-engineering、Reviewer gate、强主张降级和可复现证据链口径执行。
- 是否读取 `$research-planning`：是；已读 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`。本审计按“先理解研究问题、方法、数据/字段、评价和风险，再给可执行计划”的口径检查维度树。
- 是否读取 `$oh-my-codex:autoresearch`：是；已读 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本审计借用 artifact-gated completion 口径：`review.md` 不能只声明完成，必须有可核验 artifact 和证据回链。
- 是否完整阅读 `paper_content.txt`：是；覆盖 `paper_content.txt` Page 1--65 / line 1--3091，包含正文、Table 1--9、Figure 1--2、Appendix 1--3。
- 是否核对 `paper.pdf`：是，做了关键页视觉抽查而非 65 页逐页人工核验。用 `pdfinfo` 确认 PDF 为 65 页；用 `pdftoppm` 渲染并查看了 Table 2 所在页、Table 5、Table 7、Table 8、Table 9、Appendix 3 质量评价页。结论：关键表格真实存在，文本提取方向可信；但本审计仍不把逐格字段升级为强证据。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文不是完成型 SLR/SMS，而是 EBSE 技术报告 / guideline。其主目标是为软件工程研究者和 PhD 学生提出“comprehensive guidelines for systematic literature reviews”，强调 SLR 应以 trustworthy、rigorous、auditable methodology 公平评价研究主题；同时说明只给 high-level description，不覆盖不同 RQ 对 procedure 的细节影响，也不详细给 meta-analysis 机制（`paper_content.txt:240-258`）。引言进一步说明目标是把严格综述方法引入软件工程，并适配 SE 与医学的差异：SE 经验研究较少、方法严谨性不同、数据常为 proprietary（`paper_content.txt:298-315`）。

原文没有普通研究论文式 RQ 表，但它显式给出 RQ 设计 schema：RQ 驱动 search、data extraction、data analysis（`paper_content.txt:707-715`）；RQ 类型包含技术效果、项目因素频率、成本/风险因素、技术对可靠性/性能/成本模型影响、成本收益分析（`paper_content.txt:716-739`）；RQ 结构采用 PICOC，包含 population、intervention、comparison、outcomes、context，并可用 study design 约束 selection（`paper_content.txt:785-884`）。Appendix 3 另给一个 tertiary study protocol 的具体 RQ：EBSE 活动量、研究主题、领先研究者、当前研究限制（`paper_content.txt:2901-2910`）。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法有两层：一层是 guideline 自身的构建过程，一层是它要求 SLR 执行者遵循的 review process。guideline 自身来自医疗指南、社会科学书籍、跨学科专家讨论和 EBSE 项目经验（`paper_content.txt:316-342`），并经历内部 EBSE 项目成员 review 和外部专家 independent review（`paper_content.txt:347-355`）。

SLR 执行流程被组织为三大阶段：planning、conducting、reporting。Planning 包括 review need、commissioning、RQ、protocol、protocol evaluation；Conducting 包括 identification of research、study selection、quality assessment、data extraction/monitoring、data synthesis；Reporting 包括 dissemination、main report formatting、report evaluation（`paper_content.txt:539-565`）。原文强调该流程不是纯顺序，selection criteria、data extraction forms、synthesis methods 都会在 protocol 与 review proper 之间迭代修订（`paper_content.txt:574-591`）。

检索字段包括从 RQ facets 生成同义词、缩写、拼写变体和 Boolean string，结合 digital libraries、reference lists、journals、grey literature、conference proceedings、research registers、Internet 和专家联系（`paper_content.txt:967-1008`）。Table 2 给出 search process documentation 的字段：digital library 名称、search strategy、date、years covered；journal hand search 的 journal 名称、years searched、missing issues；conference proceedings 的 title/conference/journal 信息；unpublished study 的 research group、contact detail、website、URL/date；其他来源的 date/URL/conditions（`paper_content.txt:1059-1087`）。

纳排字段包括 study selection criteria、liberal title/abstract/conclusion screening、practical criteria、excluded study list with reason、Cohen Kappa / disagreement resolution / advisor or test-retest reliability（`paper_content.txt:1240-1304`）。Appendix 3 的 tertiary protocol 则给出具体 inclusion/exclusion：纳入 2004-01-01 到 2007-06-30 的 SLR/MA，排除 informal survey、只讨论 EBSE process、非 peer-reviewed 论文；重复发表取最完整版本（`paper_content.txt:2950-2970`）。

质量评价是原文的核心 schema，不只是一个普通 evidence 字段。它定义 quality 用于更细纳排、解释结果差异、加权/解释 synthesis、决定 inference strength、指导未来研究（`paper_content.txt:1305-1317`）。Table 3 定义 bias、internal validity、external validity（`paper_content.txt:1319-1336`）；Table 4 定义 selection/performance/measurement/attrition bias 及保护机制（`paper_content.txt:1379-1427`）；Table 5 是 quantitative study checklist，按 Design / Conduct / Analysis / Conclusions 和 study type 组织；Table 6 是 qualitative study checklist；原文还要求按具体 RQ 选择 checklist 项并 pilot reliability/usability（`paper_content.txt:1454-1462`）。

数据抽取也有显式 form schema。原文要求 extraction form 覆盖 RQ 和 quality criteria，质量若用于纳排应单独表单，若用于分析可与主抽取表合并；表单要 pilot，最好电子化（`paper_content.txt:1710-1737`）。标准字段包括 reviewer name、date、title/authors/journal/publication details、additional notes（`paper_content.txt:1738-1745`）。Table 7 展示完整 data collection form，包括 extractor/checker、study identifier、application domain、database、project counts、FP/LOC/other metrics、company/country counts、quality controls、accuracy measures、cross-company model、within-company model、comparison、statistical test、data summary 等（`paper_content.txt:1751-1967`）。Jørgensen 示例又列出 study design、estimation method selection、models、calibration、expert process、motivational bias、input、context、complexity、fairness limitations、accuracy、variance 等字段（`paper_content.txt:1969-1991`）。

数据抽取过程要求 double extraction / checker / consensus / arbitration / sensitivity analysis / correction form；单研究者可用 supervisor sample 或 test-retest（`paper_content.txt:1992-2023`）。还要求处理 duplicate publications、unpublished / missing / manipulated data，并把 manipulated data 先按原文报告，再做 sensitivity analysis（`paper_content.txt:2024-2045`）。

统计与 finding 形成不是“频次即结论”。Data synthesis 要先按 protocol 计划，但 heterogeneity 等问题可在数据分析后决定（`paper_content.txt:2052-2064`）。Narrative synthesis 需把 intervention、population、context、sample sizes、outcomes、study quality 表格化，并用表格凸显相似/差异和 heterogeneity 来源（`paper_content.txt:2065-2074`）。Quantitative synthesis 记录 sample size、effect size、standard errors、mean differences、confidence intervals、units，并根据 binary/continuous outcome 选择 odds、risk、OR、RR、ARR、mean difference、WMD、SMD 等（`paper_content.txt:2133-2172`）。结果呈现包括 forest plot、heterogeneity investigation、protocol-defined subgroup source（`paper_content.txt:2173-2198`），qualitative synthesis 包含 reciprocal translation、refutational synthesis、line-of-argument synthesis（`paper_content.txt:2207-2225`），混合研究要先分开综合再整合解释（`paper_content.txt:2226-2245`），sensitivity/publication bias 分别用 subset analysis、forest plot annotation、funnel plot 支撑（`paper_content.txt:2246-2312`）。

Appendix 3 给出最接近“finding path”的实例：先按 year/source 统计 papers/candidate/selected（`paper_content.txt:2972-2981`），再用 DARE 四问评分（`paper_content.txt:2983-3015`），抽取 source、year、type、scope、topic、authors/affiliation、RQ、是否引用 EBSE/guidelines、是否产生 practitioner guideline、primary-study 数、summary、quality score（`paper_content.txt:3016-3037`），最后用 counts and reviewed tables 回答 EBSE activity、topic、leading organization、limitations，并检查 quality over time / guideline influence（`paper_content.txt:3039-3065`）。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 至少包括：

- Definition / glossary schema：meta-analysis、primary study、secondary study、sensitivity analysis、SLR、protocol、systematic mapping、tertiary study（`paper_content.txt:259-293`）。
- Review process roadmap：planning / conducting / reporting 三阶段及 mandatory / optional / iterative stage（`paper_content.txt:539-591`）。
- RQ schema：RQ 类型、PICOC、study design 选择（`paper_content.txt:707-884`）。
- Protocol component schema：background、RQ、search strategy、selection criteria/procedure、quality checklist/procedure、data extraction、synthesis、dissemination、timetable（`paper_content.txt:886-928`）。
- Search documentation schema：Table 2（`paper_content.txt:1059-1087`）。
- Study selection / reliability schema：criteria、process、excluded list、Kappa、disagreement resolution、test-retest（`paper_content.txt:1240-1304`）。
- Quality rubric：Table 3 quality definitions、Table 4 bias types、Table 5 quantitative checklist、Table 6 qualitative checklist、DARE four-question scoring in Appendix 3（`paper_content.txt:1319-1462`, `paper_content.txt:1625-1684`, `paper_content.txt:2983-3015`）。
- Extraction form schema：Table 7 + Jørgensen design/result fields（`paper_content.txt:1738-1991`）。
- Synthesis / finding schema：narrative table, quantitative effect measures, forest plot, qualitative synthesis, mixed synthesis, sensitivity, funnel plot/publication bias（`paper_content.txt:2052-2312`）。
- Reporting schema：dissemination channels and Table 8 report structure, including title/authorship/structured abstract/background/RQ/methods/included-excluded/findings/discussion/conclusions/conflict/reference/appendix（`paper_content.txt:2315-2464`）。
- Mapping-study schema：broad RQ、less focused search、classification/categorisation rather than deep extraction、totals/summaries/graphical distributions（`paper_content.txt:2468-2518`）。
- Appendix 1/Table 9 cross-source process comparison roadmap（`paper_content.txt:2624-2719`）。
- Appendix 2 evidence table：author/date/title/reference details/topic type/topic area/quality score（`paper_content.txt:2725-2852`）。
- Appendix 3 tertiary protocol schema：具体 RQ、source/responsible、inclusion/exclusion、selection-count chain、DARE scoring、data collection、data analysis、dissemination（`paper_content.txt:2860-3065`）。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的 conclusion path 有三种：

1. 普通 SLR path：RQ 定义决定 search / extraction / synthesis；extracted study descriptors 与 quality 字段先表格化，再观察 consistency / heterogeneity / subgroup differences，最后解释 principal findings、strengths/weaknesses、applicability、practical implications、unanswered questions（`paper_content.txt:707-715`, `paper_content.txt:2065-2074`, `paper_content.txt:2427-2455`）。
2. 质量/效度 path：quality criteria 不只是 metadata，而可用于纳排、解释结果差异、分析子集、判断 inference strength 和未来研究建议（`paper_content.txt:1305-1317`, `paper_content.txt:1685-1709`）。
3. Appendix 3 tertiary path：从 selected SLR/MA 表抽取 source/year/type/scope/topic/author/RQ/guideline/primary-study count/summary/quality score，再用 counts/trends/quality comparisons 回答 EBSE 活动、主题、leading actors、limitations 和 guideline influence（`paper_content.txt:3016-3065`）。

这些 path 对 Paper2 很关键：finding 不是一个 generic leaf，也不是 guideline 作者观点；它是 RQ -> 字段 -> 分母/质量 -> synthesis/统计 -> limitation/recommendation 的有向链。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 大体准确但表达混入不适用术语。 | 当前根节点指向 guideline 目标是对的（`review.md:72-74`），但单位对象写成 `roadmap action / guideline item / schema seed`，其中 roadmap action 不适合本文。原文根目标是“为 SE SLR 提供 guideline”，并非 roadmap。 | M |
| 主干分支是否覆盖原文 schema | 未覆盖。 | 当前只有 protocol、search/selection、data extraction、quality assessment、reporting/threats 五支（`review.md:78-90`），漏掉 review need、commissioning、RQ type/PICOC、protocol evaluation、data synthesis、mapping study、Appendix process comparison、Appendix 2 evidence table、Appendix 3 tertiary protocol。并且把 quality assessment 下面挂“方法 / 技术 / 干预分类”是错位。 | I |
| 叶子维度是否足够具体 | 不足。 | 当前六个 `leaf-*` 是通用接口，文件也承认不是原文全集（`review.md:68`）。但“原文模式候选叶子映射”只有 4 行（`review.md:108-113`），远小于原文 Table 2/5/6/7/8/9/Appendix 3 的字段规模。 | I |
| 取值空间是否可执行 | 不足。 | 当前取值空间多为“自由文本 / 完整枚举 / 层级枚举 / 布尔”等抽象类型（`review.md:97-102`），而不是原文的 PICOC、search documentation、DARE Y/P/N scoring、Table 7 data item、Table 8 report sections 等可执行取值。A2a 不能据此直接编码。 | I |
| 关系边是否缺失 | 缺失。 | 原文存在 RQ -> search/extraction/analysis，quality -> selection/synthesis/inference，protocol -> conduct -> reporting，Appendix 3 RQ -> data collection -> analysis 的关系；当前没有关系边表，只用树层级表达，无法审计字段如何形成 finding。 | I |
| 统计用途 / 分母是否正确 | 降级方向正确，但字段层用途不完整。 | 当前正确标记本文不进入主统计池（`review.md:64`, `review.md:119`）。但这不等于所有原文字段 `not_applicable`：Appendix 2/3 明确有 method-seed 级统计字段、分母和质量分数；当前把 taxonomy/finding 的分母写成 `not_applicable` 或 `discussion / conclusion / roadmap action`（`review.md:120-121`），遗漏 protocol 内的计数与分析链。 | I |
| 候选 finding 路径是否完整 | 不完整。 | 当前只写 generic candidate finding / researcher adjudication（`review.md:120-128`）。原文 Appendix 3 明确把 source/year/topic/author/quality/guideline reference 等字段映射到 EBSE activity、topics、leading actors、limitations、quality trend/guideline influence（`paper_content.txt:3039-3065`），这应成为 finding path seed。 | I |
| A.1--A.4 证据链是否足够 | 不足。 | A.1 有本地文件来源（`review.md:132-138`），但 A.2 只有 4 条泛定位证据，页码写“待 A2a 精确页码复核”，段落写“邻近段落”，短引写“见释义”（`review.md:144-147`）。这符合降级为 `not_verified`，但不满足“完整、准确、可追溯”的全文级审计目标。A.4 的 structure-check 写 `passed`，但没有给出真实命令输出或脚本路径（`review.md:170`）。 | I |
| 是否存在可能误导 A2a 的强主张 | 局部存在。 | 文件已显式说明六叶不是原文全集，降低了误导风险（`review.md:68`）。但 A.3 C12 写“本文已把原文抽取字段、分类项、模型节点或报告叶子列为原文模式候选叶子映射”（`review.md:164`），实际只列 4 个粗类，容易让 A2a 误以为候选入口已经足够。 | I |

## 4. 建议维度树骨架

当前 `review.md` 未足够。建议保留“方法流程树 + 质量/效度 guideline 树”的根判断，但把树扩展为“原文指南流程主干 + 表格/附录字段主干 + finding path 关系边”。所有叶子在当前阶段仍可为 `schema_seed`，但必须给出可执行取值和证据定位。

| 根 / 主干 | 叶子维度 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| 根：SE SLR guideline schema | guideline objective / scope | SE researchers / PhD students；high-level guideline；不含 meta-analysis details；不含 question-type-specific procedures | 否；schema seed | not_reported / out_of_scope | `paper_content.txt:240-258`, `paper_content.txt:298-315` |
| 根：SE SLR guideline schema | guideline construction evidence | medical guidelines / social science books / domain experts / EBSE experience / internal review / external review | 可用于 provenance 统计，不进主统计池 | not_reported | `paper_content.txt:316-355` |
| Planning | review need | existing review check；CRD checklist；DARE four criteria；practice/research motivation | 可作为 checklist seed | not_applicable for non-review | `paper_content.txt:600-672` |
| Planning | commissioning document | project title、background、review questions、advisory group、methods、timetable、dissemination、support、budget、references | 可作为 document-field seed | not_applicable when not commissioned | `paper_content.txt:673-706` |
| Planning | RQ type | effect、frequency/rate、cost/risk factor、technology impact、cost-benefit；diagnostic-test equivalent unclear | 可统计 RQ type in future corpus | not_reported / not_classifiable | `paper_content.txt:716-742` |
| Planning | RQ quality criteria | meaningful to practitioners/researchers；changes practice/confidence；identifies belief-reality discrepancy；research-scoping | 可编码 as criterion booleans | not_reported | `paper_content.txt:744-762` |
| Planning | PICOC schema | population、intervention、comparison、outcome、context、study design | 可统计 field coverage | not_reported / not_applicable | `paper_content.txt:785-884` |
| Planning | protocol components | background、RQ、search strategy、selection criteria/procedure、quality checklist/procedure、data extraction、synthesis、dissemination、timetable | 可统计 protocol completeness | not_reported | `paper_content.txt:886-928` |
| Planning | protocol evaluation | independent expert review；supervisor review；search string from RQ；data extracted answers RQ；analysis answers RQ | 可作 quality gate seed | not_reported | `paper_content.txt:929-947` |
| Planning | protocol lessons | pre-review mapping、question revision、team involvement、pilot protocol、clear/narrow RQ | 可作 recommendation seed | not_reported | `paper_content.txt:948-966` |
| Conducting / Search | search strategy generation | preliminary search、trial search、known-study check、expert consultation、facet/synonym/Boolean strategy | 可统计 search rigor | not_reported | `paper_content.txt:967-989` |
| Conducting / Search | search sources | digital libraries、reference lists、journals、grey literature、conference proceedings、research registers、Internet、experts、related disciplines | 可统计 source type | not_reported | `paper_content.txt:993-1013` |
| Conducting / Search | publication bias controls | grey literature、conference proceedings、expert contact、funnel plot later | 可作 threat mitigation seed | not_reported | `paper_content.txt:1020-1049` |
| Conducting / Search | search documentation Table 2 | database/search strategy/date/years；journal/year/issues；conference/proceeding/title；unpublished contact/site/date/URL；other source/date/URL/conditions | 可统计 documentation completeness | not_reported | `paper_content.txt:1059-1087`; PDF Table 2 checked |
| Conducting / Selection | selection criteria | inclusion/exclusion based on RQ; pilot; practical criteria; complementary non-RQs; detailed quality criteria | 可统计 selection rigor | not_reported | `paper_content.txt:1230-1291` |
| Conducting / Selection | selection reliability | two reviewers、Cohen Kappa、initial Kappa reported、disagreement resolution、author contact、sensitivity analysis、advisor/test-retest | 可统计 reliability controls | not_reported / single_reviewer | `paper_content.txt:1292-1304` |
| Conducting / Quality | quality purpose | detailed inclusion/exclusion、heterogeneity explanation、weighting/interpretation、inference strength、future research | 可统计 quality use type | not_reported | `paper_content.txt:1305-1317` |
| Conducting / Quality | quality concepts | bias、internal validity、external validity | 可作 controlled concept enum | not_reported | `paper_content.txt:1319-1336` |
| Conducting / Quality | evidence hierarchy / study-design fit | RCT/observational/quasi/expert opinion hierarchy；question-suitable design；confounders/sensitivity | 可作 quality rationale seed | not_reported | `paper_content.txt:1337-1372` |
| Conducting / Quality | bias taxonomy Table 4 | selection/allocation；performance；measurement/detection；attrition/exclusion；protection mechanisms | 可统计 threat category | not_reported | `paper_content.txt:1379-1427` |
| Conducting / Quality | quantitative quality checklist Table 5 | Design / Conduct / Analysis / Conclusions x quantitative/correlation/survey/experiment questions | 可统计 checklist item coverage after page-table extraction | not_verified until table parsed | `paper_content.txt:1454-1624`; PDF Table 5 checked |
| Conducting / Quality | qualitative quality checklist Table 6 | credibility、importance、knowledge extension、aims、wider inference、appraisal basis、design、sample、data collection、analysis、context/data source、diversity、richness、data-to-conclusion route、reporting、assumptions、ethics、process documentation | 可统计 checklist item coverage | not_verified until table parsed | `paper_content.txt:1625-1684` |
| Conducting / Quality | quality instrument use | selection gate vs synthesis/analysis; separate vs joint form; subset analysis; no quality-weighted meta-analysis recommendation | 可统计 quality-use mode | not_reported | `paper_content.txt:1685-1709` |
| Conducting / Extraction | extraction form design | form covers RQ and quality; separate/joint quality forms; numerical data; pilot; electronic form | 可统计 extraction readiness | not_reported | `paper_content.txt:1710-1737` |
| Conducting / Extraction | standard metadata fields | reviewer name、date、title/authors/journal/publication details、additional notes | 可统计 standard field coverage | not_reported | `paper_content.txt:1738-1745` |
| Conducting / Extraction | Table 7 detailed fields | extractor/checker、study ID、domain、database、project counts、metrics、companies/countries、quality controls、accuracy、model construction、variables、cross-validation、baseline、benchmark、comparison、tests、data summary | 可统计 only after exact table parsing | not_verified until table parsed | `paper_content.txt:1751-1967`; PDF Table 7 checked |
| Conducting / Extraction | Jørgensen design/result fields | design、method selection、models、calibration、model-use expertise、expert process、motivational bias、input、context、complexity、fairness、accuracy、variance、other results | 可作 alternative extraction schema seed | not_reported | `paper_content.txt:1969-1991` |
| Conducting / Extraction | extraction procedure | double extraction、checker、consensus/arbitration、sensitivity for uncertainty、correction form、single-researcher validation | 可统计 extraction QA | not_reported | `paper_content.txt:1992-2023` |
| Conducting / Extraction | duplicate/missing/manipulated data | most complete duplicate report、author contact、include unpublished with permission/quality info、report manipulated data both raw and derived、sensitivity analysis | 可作 missing-data semantics | not_reported | `paper_content.txt:2024-2045` |
| Conducting / Synthesis | narrative synthesis | table intervention/population/context/sample/outcomes/quality; highlight similarity/difference; heterogeneity sources | 可统计 synthesis type | not_reported | `paper_content.txt:2052-2074` |
| Conducting / Synthesis | quantitative synthesis | sample size、effect size、SE、mean difference、CI、unit、binary and continuous effect measures | 可统计 synthesis field availability | not_reported / not_applicable | `paper_content.txt:2133-2172` |
| Conducting / Synthesis | quantitative presentation | forest plot、summary estimate、heterogeneity investigation、protocol-defined subgroups | 可统计 presentation type | not_reported | `paper_content.txt:2173-2198`; Figure 1 present |
| Conducting / Synthesis | qualitative / mixed synthesis | reciprocal translation、refutational synthesis、line-of-argument；separate quantitative/qualitative synthesis then cross-study integration | 可 statistic synthesis method type | not_reported | `paper_content.txt:2207-2245` |
| Conducting / Synthesis | sensitivity / publication bias | high-quality-only、study type、data difficulty、method subsets；forest plot annotation；funnel plot | 可统计 threat analysis | not_reported | `paper_content.txt:2246-2312`; Figure 2 present |
| Reporting | dissemination strategy | academic journals/conferences、practitioner outlets、press release、leaflets、posters、web pages、direct communication | 可统计 dissemination channel | not_reported | `paper_content.txt:2315-2329` |
| Reporting | report format | technical report/thesis plus journal/conference paper; journal should reference full report/thesis | 可作 artifact requirement | not_reported | `paper_content.txt:2330-2338` |
| Reporting | Table 8 report structure | title、authorship、structured abstract/context/objectives/methods/results/conclusions、background、review questions、methods、included/excluded、findings、discussion、conclusions、acknowledgements、conflict、references/appendices | 可统计 report-section coverage after table parse | not_verified until table parsed | `paper_content.txt:2379-2464`; PDF Table 8 checked |
| Reporting | report evaluation / deviations | peer review, expert panel, quality checklist, decision record, protocol deviations | 可 statistic QA/reporting control | not_reported | `paper_content.txt:2343-2370` |
| Other review types | systematic mapping differences | broad/multiple RQ、less focused search、classification/categorisation、totals/summaries/graphs、limited dissemination | 可 statistic review-type difference | not_applicable for SLR-only | `paper_content.txt:2468-2518` |
| Appendix roadmap | Table 9 cross-source process | source-specific process steps from SRG/Australian/Cochrane/CRD/Petticrew/Fink | 可作 process-roadmap source comparison | not_verified until table parsed | `paper_content.txt:2624-2719`; PDF Table 9 checked |
| Appendix evidence table | Appendix 2 SE SLR table | author、date、title、reference details、topic type、topic area、quality score | 可 statistic historical SLR evidence table | not_verified until table parsed | `paper_content.txt:2725-2852` |
| Appendix tertiary protocol | Appendix 3 RQ / corpus / extraction / analysis | EBSE RQs、sources/responsible、inclusion/exclusion、selected/candidate counts、DARE score、data collection fields、RQ-to-analysis mapping | 可作 worked example finding path seed; not main pool for this guideline | not_reported / not_applicable | `paper_content.txt:2860-3065`; PDF Appendix 3 pages checked |

建议关系边最少补 8 类：

| 关系边 | 源 | 关系 | 目标 | 证据来源 |
|---|---|---|---|---|
| RQ drives search | RQ / PICOC | determines | search terms / sources / selection | `paper_content.txt:707-715`, `paper_content.txt:983-989` |
| RQ drives extraction | RQ / quality criteria | determines | data extraction form | `paper_content.txt:707-715`, `paper_content.txt:1710-1721` |
| RQ drives synthesis | RQ | determines | analysis/synthesis method | `paper_content.txt:707-715`, `paper_content.txt:2052-2064` |
| Quality gates selection | quality checklist | can be used as | detailed inclusion/exclusion | `paper_content.txt:1685-1693` |
| Quality supports synthesis | quality data | explains | outcome difference / inference strength | `paper_content.txt:1305-1317`, `paper_content.txt:1694-1709` |
| Extraction QA controls bias | extractor/checker | validates | extracted field values | `paper_content.txt:1992-2023` |
| Statistics become findings | extracted field table | supports | findings / limitations / recommendations | `paper_content.txt:2065-2074`, `paper_content.txt:2427-2455` |
| Appendix 3 RQ-to-analysis | protocol RQs | answered by | counts/topic/org/quality trend/guideline influence | `paper_content.txt:3039-3065` |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 扩展主干树，不再用 5 个粗分支代表全文 schema。 | `review.md` 的“维度树结构” | 改为 Planning / Conducting / Reporting / Mapping-study note / Appendix evidence-protocol 五大主干；Planning 下补 review need、commissioning、RQ/PICOC、protocol、protocol evaluation；Conducting 下补 search、selection、quality、extraction、synthesis；Reporting 下补 dissemination、report table、evaluation/deviation。 | `paper_content.txt:539-591`, `paper_content.txt:886-928`, `paper_content.txt:2315-2464` | I |
| 把“六个通用接口叶子”降为接口摘要，不计为原文叶子。 | “叶子维度表” | 保留通用接口表可以，但标题应改为“跨论文接口投影”；新增“原文叶子维度表”列出可执行字段，不少于本报告第 4 节骨架中的关键叶子。 | `review.md:68`, `paper_content.txt:707-884`, `paper_content.txt:1059-1087`, `paper_content.txt:1738-1991` | I |
| 细化原文候选叶子映射。 | “原文模式候选叶子映射（A1 种子）” | 从 4 个粗类扩展为 protocol component、RQ type、PICOC、search documentation、selection reliability、quality concepts/bias/checklists、Table 7 extraction form、synthesis method、Table 8 report structure、Appendix 3 protocol/extraction/analysis 等叶子。 | `review.md:108-113`, `paper_content.txt:893-922`, `paper_content.txt:1059-1087`, `paper_content.txt:1319-1462`, `paper_content.txt:1738-1991`, `paper_content.txt:2379-2464`, `paper_content.txt:2860-3065` | I |
| 补关系边表。 | “统计与候选发现链路”之后 | 新增关系边表，至少记录 RQ -> search/extraction/analysis、quality -> selection/synthesis/inference、extraction QA -> field reliability、field table -> findings/recommendations、Appendix 3 RQ -> analysis。 | `paper_content.txt:707-715`, `paper_content.txt:1305-1317`, `paper_content.txt:1992-2023`, `paper_content.txt:3039-3065` | I |
| 修正 quality branch 下挂错叶子。 | “维度树结构”与叶子表 | 当前 quality assessment 下挂“方法 / 技术 / 干预分类”不忠实。应挂 quality purpose、quality concepts、evidence hierarchy、bias taxonomy、quantitative checklist、qualitative checklist、quality use/limitations。 | `review.md:86-87`, `paper_content.txt:1305-1709` | I |
| 区分“不进主统计池”和“原文有统计/分母字段”。 | “统计与候选发现链路” | 保持本文作为 guideline 不进入 survey-of-surveys 主统计池；但 Appendix 2/3 的 method-seed 统计字段、counts、quality score、trend analysis 应作为 finding-path seed，不应写成全部 `not_applicable`。 | `review.md:119-121`, `paper_content.txt:2725-2852`, `paper_content.txt:2972-3065` | I |
| 提升 A.2 证据账本粒度。 | A.2 | 把 4 条泛证据拆成 15--25 条，至少覆盖目标/来源、process phases、RQ/PICOC、protocol, Table 2, selection/reliability, Table 3/4/5/6, Table 7, synthesis/Figure 1/2, Table 8, Table 9, Appendix 2, Appendix 3。每条给 page、section、line range、table/figure number。 | 当前 A.2：`review.md:144-147`；原文锚点见本报告第 4 节 | I |
| 修正 A.4 中未给真实命令的 `passed`。 | A.4 | 若结构检查脚本真实运行，应写脚本路径与命令；若只是人工检查，应改成 `manual_reviewed` 或 `not_run`。不要把无命令证据写成 passed。 | `review.md:170` | M |
| 补 PDF 核对状态。 | 快速卡片 / A.4 | 可写“关键页已视觉抽查；未完成逐页表格字段精核”。把需要逐格解析的 Table 5/6/7/8/9 标为 `needs_table_parse`，而不是笼统“图表待人工核对”。 | 本审计已抽查关键页；原 review 仅写 `needs_manual_check`：`review.md:171` | M |
| 降低 C12 的完成语气。 | A.3 C12 | 将“本文已把原文抽取字段、分类项、模型节点或报告叶子列为……”改成“当前仅列出 4 个粗粒度入口，尚未完成原文 schema 展开”。否则容易误导 A2a。 | `review.md:164` | I |

## 6. C/I/M 结论

- C：0。当前 `review.md` 已明确本文是 guideline、不可进入主统计池，并承认六个 `leaf-*` 不是原文叶子全集；因此未发现会立即把 guideline 当作完成型统计 finding 的阻断级错误。
- I：8。核心问题是原文 schema 复原过小、主干分支不完整、叶子取值不可执行、关系边缺失、Appendix 2/3 的 evidence table / tertiary protocol / finding path 未入树、A.2/A.3 证据链泛定位。这会实质影响 Paper2 的 A2a/A2b 维度模式演化和证据链可审计性。
- M：2。根节点 wording 中有 roadmap action 等不贴切术语；A.4 `passed` 需要改成有命令证据或人工状态。
- 最终建议：NEEDS FIX。
