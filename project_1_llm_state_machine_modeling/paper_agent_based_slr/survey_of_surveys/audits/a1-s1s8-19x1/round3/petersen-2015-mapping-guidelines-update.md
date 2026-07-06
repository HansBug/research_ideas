# petersen-2015-mapping-guidelines-update：A1 survey-of-surveys S1--S8 单篇维度抽取审计（round3）

## 0. 审计边界与阅读状态

- 角色：A1 `survey_of_surveys` 单篇维度抽取 subagent；本轮只处理 `papers/petersen-2015-mapping-guidelines-update`，未开启 sub-subagent。
- 已先读并遵循：`ai-research-writing-skill` 的 claim-evidence-engineering 要求、`research-planning` 的风险显式化要求、以及本目录 [GUIDE.md](../../../GUIDE.md) §6.3/§6.4。
- 已读取本地材料：
  - `bibtex.bib`：确认题名、作者、IST 64:1--18、2015、DOI `10.1016/j.infsof.2015.03.007`。
  - `paper_content.txt`：已按页序通读 1--1973 行，覆盖摘要、§1--§6、Appendix A、Appendix B 与 references。
  - `review.md`：已通读快速卡片、全文详读、六类 pattern、A1-M0--M6、维度树复原、叶子表、关系边表、S1--S8 与四分栏。
  - `evidence_chain.md`：已通读 A.1--A.4；当前证据链多为树级 claim map，关键证据仍多标 `not_verified` / A2a 待页码表图精核。
- 已局部核对 `paper.pdf`：用 `pdfinfo` 确认为 18 页；用 `pdftotext -layout` 辅助检查版面；人工查看 PDF 第 4 页 Table 3 与第 5 页 Fig. 1，确认 Fig. 1 分母链为 `7752 -> 5082 -> 60 -> 43 -> 54 -> 44 -> 52`，对应边为 `-2666, -5022, -17, +11, -10, +8`。
- 以下判断均为 **A1 文本级 + 局部 PDF 核对审计**，只服务 A2a/A2b schema 与方法学模式建设，**不得写成 Paper2 final quantitative finding**。

## 1. 总体裁决

本文不是纯 guideline，也不是目标领域效果综述，而是“系统映射研究之系统映射（systematic mapping study of systematic maps）+ mapping guideline update”的混合型方法学样本。主样本单位是 52 篇 2004--2012 年软件工程 systematic mapping / scoping studies；作者用 Table 3 抽取表、§4 统计结果、Appendix B 逐研究映射表和 §5 guideline update，把既有 SMS 实践转化为 planning-conducting-reporting guideline、topic-independent facets、validity taxonomy 与 evaluation rubric。

统计池资格：**可作为 `survey_of_surveys` 方法学 / schema 主统计池候选，但 A2a 精核前不得进入最终定量发现**。理由是原文有系统检索、纳排、QA、抽取表、字段统计、逐研究附录和方法学 finding；但本地 `evidence_chain.md` 仍未把所有叶子 / 表图 / 页码细化到 A.2，Appendix B 跨页表和 Figures 3--21 的数值仍需视觉核验。

## 2. S1--S8 审计表

| 维度 | 等级 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|---|
| S1 综述任务设定 | 强 | 摘要说明目标是识别 systematic mapping process 如何执行并据此更新 guideline；§3.1 给出 RQ1--RQ4：guidelines、SE topics、where/when、mapping process execution。证据：`paper_content.txt` L11--25、L217--230。 | 根任务是“对 SE systematic mapping studies 做 systematic map，并将实践统计转化为 updated guideline”；RQ 同时是 Table 3 字段 owner。 | 支持方法学统计池候选；不支撑任何目标 SE 技术效果结论。 | 核正式页码与 DOI final；现有 PDF p.1/p.3 足以支撑文本级判断。 |
| S2 语料收集与筛选 | 强 | §3.2 给出 PICO、IEEE/ACM/Scopus/Inspec-Compendex、检索式、EndNote 去重与 2012 截止；§3.3 给出题摘、全文、snowball、QA、validation set 和 excluded review 回补。证据：L231--366；PDF p.5 Fig.1。 | 检索漏斗树：数据库检索 7752 → 2004 前剔除 5082 → 题摘纳排 60 → 全文 43 → snowball 54 → QA 44 → 回查排除项 52。57 是 QA 前候选，不是 final included studies。 | 强；可作为“语料收集 / 分母链”候选字段。A2a 前只可写文本级候选统计。 | 已局部核对 Fig.1；仍需核 Table 1/2 与 Appendix A included/excluded 清单是否完全一致。 |
| S3 原生维度树 / 样本编码对象 | 强 | §3.4 Table 3 给抽取表；§4 按 RQ 展开结果；Appendix B Tables B.15--B.27 给逐研究映射；§5 形成 guideline update。证据：L367--408、L492--1473、L1548--1805。 | 原生结构是维度森林：T1 抽取表单树、T2 topic/classification facet 树、T3 guideline action/rubric 树、T4 validity / threat taxonomy 树；共享样本单位 52 篇 mapping studies。 | 强；可作为“同一分母上多根方法学维度森林”样本。 | 核 Table 3 字段数与 RQ 绑定；核 Appendix B 每张表的行数 / 缺失值语义 / 跨页残缺。 |
| S4 字段级证据 | 中到强（文本级） | Table 3 明示 Study ID、Title、Author、Year、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type 等数据项；Appendix B 提供 topic、venue、guidelines、search、QA、facet、visualization、validity 的样本级映射。证据：L392--408、L1559--1805。 | 字段层包括 bibliographic fields、SE topic fields、process/search fields、classification facets、visualization fields、validity fields、rubric fields。 | 字段存在性强；逐样本取值、频次和比例在 A2a 前只能作候选。 | Table 3 原文其实是 **11 个 data items**（若把 Year of Publication 视作一个 data item），当前 `review.md` E2 写“12 字段”需修正或说明 counting 口径；Appendix B 全表需视觉精核。 |
| S5 维度模式演化 | 强 | §4.4.4 指出 Petersen 2008 未强调的新维度为 venue、study focus、research method；§5 与 Table 5 比较既有 guidelines；§5.1.3 最终鼓励 topic-independent facets 使用 venue、research type、research method。证据：L661--674、L1109--1114。 | 演化链是“既有 guideline 覆盖差异 + 52 篇实际 SMS practice 统计 + Table 5 comparison → updated guideline / facets / rubric”，不是完整 codebook 版本日志。 | 强；可入“实践统计驱动 schema/guideline 修订”的方法学模式池。 | 核 Table 5 9 列 guideline comparison；明确区分“新识别五元 facet”与“最终鼓励三元 facet”。 |
| S6 统计分析 | 强 | §3.5 明确 tabulate、visualize、theme grouping and counting；§4 统计 guideline adoption、topics、venue、search、QA、classification、visualization、validity；§5.4 Table 14 / Fig.20--21 给 rubric 统计。证据：L376--385、L492--691、L1364--1473。 | 字段 → 统计路径清楚：52 分母上的 guideline、topic、venue、search、QA、classification facet、visualization、validity、rubric score。 | 强；只限方法学统计池候选，A2a 前不得并入最终跨论文定量 finding。 | 核 Figures 2--15、20--21 与 Table 14；尤其 median quality ratio=33%、25% ≥40%、journal vs conference 差异。 |
| S7 候选 finding | 强（方法学 finding） | §6 总结单一 guideline 不足、需要 updated guideline；§5.1.3 推荐通用 facets；§5.4 提出 evaluation rubric；§2/§6 多次强调 good sample / representation。证据：L1483--1535、L1109--1114、L1364--1384。 | Finding 链条是“字段统计观察 → 方法学解释 → guideline action/rubric/reporting 建议”；不是目标 SE 领域因果 / 效果结论。 | 强但严格限界；可入 finding-formation 模式池，不可迁移为 LLM4STM / LLM4SE 领域发现。 | 把每条候选 finding 回连到 RQ、Fig/Table 或 §5 recommendation；区分作者结论与本地 Paper2 启发。 |
| S8 研究者 / 作者质疑与裁决 | 中 | §3.3 承认 title/abstract 单人筛选是 reliability threat，并用 first-author validation sets、引用集、回查排除研究缓解；§3.4 第二作者抽取、第一作者 trace-back review；§3.6 系统讨论 validity；§5.1.2/§5.1.3 提供 additional reviewer、consensus、decision rules 等 guideline action。证据：L301--374、L421--489、L1134--1149。 | 可复原为 threat-aware validation / checker 机制与 guideline-level reviewer consensus 建议；不是完整双人独立筛选、完整 coding adjudication 或 inter-rater 日志。 | 中；可统计为“有复核和效度缓解”，不能统计为“完整裁决日志”。 | 核 Fig.17、Table 6、§3.3--§3.6；避免把 guideline 推荐的 ideal process 误写成本研究自身 process。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 森林总览

```text
森林根：52 篇软件工程 systematic mapping / scoping studies（final included N=52）
├─ T1 数据抽取表单树（Table 3；字段绑定 RQ1--RQ4）
│  ├─ 一般书目信息：Study ID / Article Title / Author Name
│  ├─ RQ3 时间与发表源：Year of Publication / Venue
│  ├─ RQ2 主题：Area in SE（SWEBOK + research methods + education）
│  └─ RQ1/RQ4 过程：Guidelines / Search strategy / Search type / Classification schemes / Visualization type
├─ T2 映射实践分类树（§4.4 + Appendix B）
│  ├─ guideline adoption（10 类 guideline，多选）
│  ├─ study identification（search strategy / search development / search evaluation / inclusion-exclusion）
│  ├─ QA 与 data extraction reliability（是否 QA；客观准则 / additional reviewer / test-retest）
│  ├─ topic-independent facets（research method / research type / study focus / contribution type / venue）
│  ├─ topic-specific classification（emerging scheme / existing scheme）
│  └─ visualization（line / pie / bar / bubble / Venn / heatmap）
├─ T3 guideline action 与 evaluation rubric 树（§5 + Table 5 + Tables 8--14）
│  ├─ planning：need/scoping、study identification、data extraction/classification、visualization、validity
│  ├─ conducting：record information、iteration/revision、reference manager/spreadsheet 等工具性活动
│  ├─ reporting：Introduction / Related Work / Research Method / Results / Discussion-Conclusions / Appendix
│  └─ rubric：need、search strategy、search evaluation、extraction/classification、validity 的有序评分
└─ T4 validity taxonomy 与 threat-mitigation 树（§3.6 + §5.1.5）
   ├─ descriptive validity
   ├─ theoretical validity（含 study identification / sampling 与 researcher bias）
   ├─ generalizability（internal / external）
   ├─ interpretive validity
   └─ repeatability
```

### 3.2 叶子维度与取值空间（精选）

| 叶子 | 所属树 | 原文依据 | 取值空间 | 缺失值语义 / 统计用途 |
|---|---|---|---|---|
| `area_in_se` | T1/T2 | Table 3；Table B.15；§4.2 | SWEBOK 知识域 + Research methods + Education | 52 分母主题分布；A2a 前不作最终比例。 |
| `guidelines_adopted` | T1/T2 | Table 3；Fig.5；Table B.17；§4.4.1 | Kitchenham2004、Kitchenham&Charters2007、Petersen2008、Budgen2008、Arksey&O'Malley2005、Dybå&Dingsøyr2008、Bailey2007、Petticrew&Roberts2006、Biolchini2005、Jorgensen&Shepperd2007、Durham template 等多选集合 | 未声明 guideline 需与“无 guideline”区分；24/52 多指南是候选统计。 |
| `search_strategy` | T1/T2 | Table 3；Fig.6；Table B.18 | Database search / Snowballing / Manual 的多选集合 | 至少一个；用于比较过度依赖 database search。 |
| `search_development` | T2/T3 | Fig.7；Table B.19 | PICO、consult experts/librarians、iterative improvement、keywords from known papers、standards/encyclopedias/thesaurus | 未报告 ≠ false；需 A2a 确认缺失值。 |
| `search_evaluation` | T2/T3 | Fig.8；Table B.20 | test-set of known papers、expert evaluation、authors' web pages、test-retest | 可空；支撑“search evaluation 报告不足”候选 finding。 |
| `inc_excl_reliability` | T2/T3 | Fig.9；Table B.21；Table 6 | objective criteria、additional reviewer + consensus、decision rules；Table 6 还有 A--F 决策状态 | 本文自身未完整采用双人筛选；不要把 guideline action 当成自身裁决日志。 |
| `quality_assessment` | T2 | §4.4.3；Fig.10；Table B.22 | Yes / No | 14/52 yes 是方法学候选统计，非目标领域质量结论。 |
| `topic_independent_facets` | T2/T3 | §4.4.4；Fig.12；Table B.24 | research method / research type / study focus / contribution type / venue | 新识别五元 facet；最终推荐三元 facet 为 venue / research type / research method。 |
| `research_type` | T2/T3 | Table 7；§5.1.3 | evaluation research / solution proposal / validation research / philosophical paper / opinion paper / experience paper | 由六条件真值表判定；适合迁移为 rule-check 启发，但需研究者裁决。 |
| `research_method` | T2/T3 | Fig.19；§5.1.3 | survey、case study、controlled experiment、action research、ethnography、simulation、prototyping、mathematical analysis | 与 research_type 有关系边：方法可落在 validation/evaluation/both。 |
| `topic_specific_classification` | T2 | Fig.13；Table B.25；§5.1.3 | emerging classification / existing scheme | emerging scheme 类似 open coding；existing scheme 可来自 SWEBOK、IEEE、ISO/IEC。 |
| `visualization_type` | T1/T2 | Table 3；Fig.14；Table B.26 | line、pie、bar、bubble、Venn、heatmap | 多选；heatmap 低使用仅作候选观察。 |
| `validity_discussed` | T2/T4 | Fig.15；Table B.27 | Yes / No | 45/52 yes；不能替代 validity taxonomy 的细分类。 |
| `validity_taxonomy` | T4 | §3.6；§5.1.5 | descriptive、theoretical、generalizability、interpretive、repeatability | 本文未覆盖 LLM/provider/prompt/schema drift，Paper2 需扩展。 |
| `rubric_scores` | T3 | Tables 8--14；§5.4 | need ∈ 0/1/2；search strategy ∈ 0/1/2；search evaluation ∈ 0/1/2/3；extraction/classification ∈ 0/1/2/3；validity ∈ 0/1 | 是方法学 quality rubric；ratio=33% 等数字 A2a 前只作文本级候选。 |

### 3.3 关系边

| 边 | 源节点 | 关系 | 目标节点 | 证据 | 审计说明 |
|---|---|---|---|---|---|
| E1 | study | has_extraction_field | Table 3 数据项 | §3.4 / Table 3 | 每个字段绑定 RQ；Paper2 可迁移“字段 owner RQ”设计。 |
| E2 | study | adopts | guideline set | Table B.17 | 支撑多指南并用与单指南不足的 finding。 |
| E3 | study | uses | search / selection action | Tables B.18--B.21 | search development、evaluation、inc/excl 是分开的子树，不应混成一个字段。 |
| E4 | study | classified_by | topic-independent facet | Table B.24 | facet 是多选关系，不是互斥类别。 |
| E5 | research method | constrains | research type | Fig.19 / Table 7 | 本文重要结构化约束，可用于 A2a rule-check 启发。 |
| E6 | guideline | covers | activity/action | Table 5 | 指南比较矩阵是 guideline update 的核心证据，不是普通结果表。 |
| E7 | mapping study | scored_by | rubric dimension | Tables 8--14 | action/rubric 与 guideline action 同源，但 scoring 是 evaluation layer。 |
| E8 | threat | mitigated_by | search/data-extraction/reporting action | §3.6 / §5.1.5 | validity taxonomy 与 rubric/guideline action 有关系：threat 说明为什么需要这些 action。 |

## 4. 对既有 `review.md` / `evidence_chain.md` / `SUMMARY.md` 的 C/I/M 清单

### C（critical）

- 暂未发现必须立即阻断的 C 级问题。现有正文总体已声明 A2a 前不得作为最终定量发现；但下列 I 级问题若被后续 SUMMARY 或 paper 草稿直接数值化，可能升级为 C。

### I（important）

1. **Table 3 字段数口径需要修正：现有 `review.md` 证据锚点 E2 写“Table 3 数据抽取表（12 字段）”，但原文 Table 3 可审计 data items 是 11 个。**
   - 证据：PDF p.4 / `paper_content.txt` L392--408 列出 Study ID、Article Title、Author Name、Year of Publication、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type。
   - 影响：字段数是 S3/S4 原生树入口，若不统一会影响后续 A2a 表单字段闭合和 SUMMARY schema 口径。
   - 建议：将 “12 字段” 改为 “11 个 data items”；若主线程想把 `Year` 拆成年/月或把 `Search strategy` 拆成 strategy+selection，则必须显式声明这是本地拆分，不是 Table 3 原文项数。
2. **`evidence_chain.md` A.2 对 S1--S8 仍过粗，不能支撑当前 `review.md` 中大量“强”级 S 维度的逐项回链。**
   - 证据：A.2 只有 type/unit/denom/tree/pool 等树级证据，且多为 `not_verified`；但 `review.md` S1--S8 引用 Table 3、Table 5、Table 8--14、Appendix B、Fig.1 等大量细粒度事实。
   - 影响：违反 §6.4 “若支撑结论已经进入 evidence_chain，还应指向 A.2/A.3”的可审计精神；A2a 前主线程难以判断哪些 S 维度是文本级强、哪些只是待核候选。
   - 建议：A2a 至少拆出 RQ、Fig.1、Table 3、topic-independent facets、Table 5、Tables 8--14、validity taxonomy、Appendix B 八组 A.2 证据，并在 A.3 增加 S1--S8 或 tree/facet/rubric 结论映射。
3. **topic-independent facets 需要在 `review.md` / SUMMARY 中保持“两层口径”：新识别五元 facet ≠ 最终鼓励三元 facet。**
   - 证据：§4.4.4 / L661--674 新识别 `venue, study focus, research method`，并与旧有 `contribution type, research type` 共同构成 Fig.12 五元 facet；§5.1.3 / L1109--1114 最终鼓励 `venue, research type, research method`，并明确 contribution type 相关性较低。
   - 影响：若 SUMMARY 只写“topic-independent dimensions 树”或“新识别 venue、study focus、research method”，容易在 A2a 中把 study focus 误当成最终推荐 core facet，或把 contribution type 漏出五元统计空间。
   - 建议：所有总结写成：“原文统计五元 facets：research method / research type / study focus / contribution type / venue；最终推荐三元 facets：venue / research type / research method。”
4. **S8 不能升级为“强”或“完整裁决日志”。**
   - 证据：§3.3 明示 title/abstract 单人筛选且 quality assessment 也由第二作者单人执行；虽有 first-author validation、trace-back review、§3.6 validity 和 §5 guideline action，但缺少完整双人独立编码 / inter-rater / adjudication log。
   - 影响：如果后续把本文统计为“完整 human adjudication”，会夸大 A1 对 researcher override / 裁决日志的证据基础。
   - 建议：保持 S8 = 中；统计取值写“有复核与效度缓解 / 有 guideline-level consensus action”，而非“完整裁决日志”。

### M（minor）

1. **`review.md` 待复核第 1 条仍写“52+8+11”等文本提取残留。**已局部 PDF 核对后可改为清晰链条：7752、5082、60、43、54、44、52；边为 -2666、-5022、-17、+11、-10、+8。
2. **快速卡片“是否目标证据池：否”与 `eligible_for_statistical_synthesis=true` 容易混淆。**建议改成“不是目标领域证据池；是 `survey_of_surveys` 方法学统计池候选”。
3. **`review.md` 叶子表若继续保留具体频次（如 venue=27、bar=22、bubble=23），应统一标注“文本级 / Appendix B 待视觉核验”。**这不影响当前 S1--S8，但能降低后续误用为 final quantitative finding 的风险。
4. **SUMMARY 中 Petersen 2015 的关键价值可以补充“Table 3 11 data items + Table 5 guideline comparison + Tables 8--14 rubric”。**这会让后续 agent 更容易定位为什么该文是方法学核心样本。

## 5. 明确禁止事项

本审计只给出 A1 文本级和局部 PDF 核验的 S1--S8 与原生维度森林复原。任何数字（如 52、57、24/52、14/52、45/52、median 33%、25% ≥40%、Table 14 各格频数、Appendix B 各表频次）在 A2a 完成 PDF 表图、Appendix B 和 `evidence_chain.md` 细粒度回链前，都只能作为“文本级候选统计观察”或“schema/finding 形成模式”，**不得写成 final quantitative finding**。
