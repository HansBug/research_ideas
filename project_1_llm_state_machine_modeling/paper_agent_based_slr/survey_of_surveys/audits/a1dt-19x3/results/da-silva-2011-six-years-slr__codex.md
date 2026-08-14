# da-silva-2011-six-years-slr · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取路径 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- 是否读取 `$research-planning`：是；读取路径 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`，并读取 `references/planning-prompts.md`
- 是否读取 `$oh-my-codex:autoresearch`：是；读取路径 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- 是否完整阅读 `paper_content.txt`：是；覆盖摘要、引言、previous studies、RQ、DCP、search、selection、quality assessment、data extraction、data extraction results、RQ1--RQ5 discussion、limitations、conclusion、references 和 Appendix A，全文 1--1625 行均已阅读
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认 PDF 为 15 页，并目标性视觉核对 PDF 第 3 页 RQ、第 4 页 Fig. 1、第 5 页 Table 1 / QA rubric / data extraction form、第 6 页 Fig. 2、第 12 页 Table 6--10。未逐页视觉核对所有表格，Table 2--5、11--13 的精确页码和表格内容仍应在 A2a 做完整版面精核

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是对两个前序 tertiary studies 做扩展和更新，覆盖 2008-07-01 到 2009-12-31，并把新发现与 OS / FE 两个前序研究整合。摘要明确说明分析对象包括 SLR 的质量、软件工程主题覆盖，以及对教育和实践的潜在影响。正文第 114--120 行把本文定位为对 2008-07-01 到 2009-12-31 发表的 SE SLR 的 mapping / tertiary study，并说明目标是整合前序结果。

原文显式 RQ 是 5 个，且 RQ1 有两个子问题：

- RQ1：2004-01-01 到 2009-12-31 发表了多少 SLR？
- RQ1.1：2004-01-01 到 2008-06-30 发表了多少 SLR？
- RQ1.2：2008-07-01 到 2009-12-31 发表了多少 SLR？
- RQ2：研究主题是什么？
- RQ3：哪些个人和组织在 SLR-based research 中最活跃？
- RQ4：前两项研究 OS / FE 观察到的 SLR 限制是否仍然存在？
- RQ5：SLR 质量是否在改善？

这些 RQ 在 `paper_content.txt` 第 221--248 行出现，并在 PDF 第 3 页视觉核对确认。它们不是普通“范围 / 语料 / 分类 / 证据 / finding”六叶接口，而是原文结果结构的主轴。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法首先定义 OS、FE 与 SE 的关系。第 200--220 行说明作者沿用 FE protocol、独立执行扩展，并将 OS / FE 的 53 篇与 SE 的 67 篇整合为 OS/FE + SE 的 120 篇 secondary studies。

原文有一个跨 selection、quality assessment、data extraction 的 Decision and Consensus Procedure。第 257--280 行描述 R1 随机分配、两名研究者独立评估、R4/R5 整合 Agreement/Disagreement Table、Rk 处理分歧，以及六人共识。PDF 第 4 页确认 Fig. 1 是 DCP 流程图。这个流程是方法 schema 的显式节点，不应只并入“语料链条”。

检索流程包括自动检索、手工检索和 backward reference search。第 281--331 行给出六个自动检索源、检索范围和检索式，并说明自动检索 1389 篇，title / abstract 初筛后 157 篇；手工检索 Table 1 的期刊和会议源得到 66 篇；合并去重后 154 篇进入 selection。第 333--357 行说明全文阅读 154 篇，按是否为 SE SLR 等标准排除，并通过参考文献搜索补 2 篇。PDF 第 6 页确认 Fig. 2 的完整分母链为 1389 → 157、66 → 154 → 75 → 77 → 67，并含 69 duplicates、79 exclusions、10 final exclusions。

质量评价使用 OS / FE 同一 DARE 口径。第 387--447 行给出 QA1--QA4、Y/P/N 判定、Y=1/P=0.5/N=0 评分，以及 10 篇 blind assessment 的一致性检查。PDF 第 5 页视觉核对确认 QA rubric 是显式质量 schema。

数据抽取表是本文最关键的 extraction form。第 448--468 行列出 9 个抽取 bullet，若把 `Cited EBSE papers` 和 `Cited Guidelines` 拆成 Table 2 的两列，则实际结果表包含至少 10 个字段：Year、Quality Score、Review Type、Review Scope、Review Topic、Cited EBSE paper、Cited guidelines、Number primary studies、Practitioners guidelines、Paper type / Source type。PDF 第 5 页视觉核对确认这些字段以加粗字段名出现在 `Data extraction process` 中。

统计和 finding 形成方式是 RQ 驱动的表格链：

- RQ1 使用 Year 与 EBSE / guideline citation 形成 Table 4 的年度增长和 EBSE-positioned SLR 比例。
- RQ2 使用 Review topic、SE Curriculum、SWEBOK 映射形成 Table 2、5、6 的主题覆盖、教育和实践相关性。
- RQ3 使用作者、组织、国家形成 Table 7、8 的活跃研究者和地理分布。
- RQ4 使用 Review type、Review focus、Number primary studies、Practitioner guidelines、QA3、Cited guidelines 等字段形成 Table 9--12 和 discussion。
- RQ5 使用 Quality score、guideline citation、source type、review scope、number of primary studies 形成 Table 3、13、回归分析和相关性分析。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 至少包括以下对象：

- RQ schema：RQ1、RQ1.1、RQ1.2、RQ2、RQ3、RQ4、RQ5。
- DCP 流程模型：Fig. 1，适用于 study selection、quality assessment、data extraction。
- 检索 / 纳排分母模型：Fig. 2，含自动检索、初筛、手工检索、合并、selection、reference search、final exclusion。
- Manual search source list：Table 1。
- Data extraction form / result table：Table 2，字段包括 study ref、year、quality score、review type、review focus、review topic、EBSE citation、guideline citation、primary-study count、practitioner guidelines、paper type。
- Quality rubric：QA1--QA4、Y/P/N 取值、Y=1/P=0.5/N=0 评分，结果见 Table 3。
- External classification schema：SE 2004 Curriculum 与 SWEBOK 映射，见 Table 5、6。
- Active authors / countries taxonomy：Table 7、8。
- Review-type and evidence extent comparison：Table 9。
- Practitioner guideline count：Table 10。
- Primary-study quality-evaluation count：Table 11。
- EBSE / guideline citation count：Table 12。
- Quality trend by year and cited-guideline factor：Table 13。
- Update / extension taxonomy：conclusion 第 1343--1357 行区分 temporal update、search extension、combined temporal update and search extension。这不是 roadmap figure，但它是作者给出的后续更新型 SLR 方法分类。
- Artifact / appendix：Appendix A 是 67 篇 SE systematic reviews 的完整清单。原文没有报告独立 replication package，不能臆造 artifact availability。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文不是从单个字段直接给 final finding，而是先按 RQ 构造统计表，再在 discussion / conclusion 中解释。

第 502--512 行用 Table 4 支撑 SLR 数量增长和 EBSE-positioned SLR 增加。第 514--520 行从 Table 2 归纳 67 篇覆盖 24 个 topic；第 663--678 行用 Table 5 / 6 说明覆盖增加但仍稀疏，且 Software Configuration Management 与 Software Quality 未被 120 篇覆盖。第 689--731 行用作者、组织、国家统计说明 SLR 使用更分散。第 774--820 行围绕 RQ4 解释主题集中、mapping studies 增加、实践导向有所改善但多数仍间接服务实践。第 821--1042 行指出 primary-study quality assessment 有改善但 full explicit evaluation 仍低，并给出三类原因。第 1144--1225 行用质量趋势、回归和相关性说明质量提升、QA3/QA4 是低质量 quartile 的主要弱点、primary-study 数量与质量分数负相关。

结论第 1261--1388 行进一步合成三类正向变化、三类主要限制和后续建议。正向变化是主题覆盖增加、研究者 / 组织更分散、mapping studies 比例更高。主要限制是许多 SLR 仍不评价 primary-study quality、primary-study result integration 很弱、practitioner guidelines 仍少，因而 EBSE 尚未 fully realised in practice。后续建议包括更多 proper updates / extensions、改进报告组织以便 extraction / comparison、调查 120 篇 SLR 作者的问题来源和结果应用，并研究 qualitative synthesis 方法。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但单位对象需要修正 | `review.md` 第 64 行把树型判为 tertiary 更新统计树，方向正确；但第 74 行写单位对象为 `primary study / secondary study`，容易混淆。原文 tertiary 的分析单位是 secondary studies / SLRs；primary-study count 只是被抽取字段。 | M |
| 主干分支是否覆盖原文 schema | 不足 | 当前主干是范围、语料、主题、方法、评价/统计/候选发现五类通用层。原文主轴还包括 RQ1--RQ5、OS/FE/SE predecessor integration、DCP、Fig. 2 分母链、QA rubric、data extraction form、external curriculum/SWEBOK mapping、Table 2--13 finding path。 | I |
| 叶子维度是否足够具体 | 不足 | `review.md` 第 68 行正确声明六个 `leaf-*` 是通用接口，不是原文全集；但第 108--113 行的原文候选叶子只有 4 个，漏掉原文第 448--468 行明确 extraction form 中的大量字段。 | I |
| 取值空间是否可执行 | 不足 | 原文有可执行封闭取值：Review Type = SLR / MA / MS，Review Scope = RQ / SERT / RT，EBSE / guideline citation = Y/N + cited reference group，Source Type = J / C / WS / BS，QA = Y/P/N，Practitioner guidelines = Y/N，Year / Quality Score / Number primary studies 为数值。当前树多写“自由文本 / 数值 / 布尔”，没有保留这些原文取值空间。 | I |
| 关系边是否缺失 | 缺失 | 原文需要至少保留 predecessor relation、RQ→extraction fields→tables→findings、DCP→selection/quality/extraction、topic→curriculum/SWEBOK、quality score→quality trend、practitioner guidelines→practice impact 等关系。当前 `review.md` 没有关系边表。 | I |
| 统计用途 / 分母是否正确 | 有降级声明，但原文分母不足 | 当前第 117--121 行正确声明 A1-DT 不进入 SUMMARY 定量统计；但没有把原文分母链 1389/157/66/154/75/77/67、OS/FE 53、SE 67、OS/FE+SE 120、Table-specific N=67/120 等写入树或候选叶子。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前第 115--128 行只给 generic candidate finding 链。原文的 finding path 是 RQ1--RQ5 分别回到 Table 4、2/5/6、7/8、9--12、3/13，再进入 conclusion 的增长、覆盖、扩散、质量、实践影响和综合方法缺口。 | I |
| A.1--A.4 证据链是否足够 | 结构存在但证据粒度不足 | A.1 有本地来源；A.2 第 144--147 行均为泛定位，原文短引写“见释义”，表 / 图多为“待核验”；A.3 能回链但全部 weak / schema_seed；A.4 标出 visual check needs_manual_check。由于使用 `not_verified`，没有把弱证据升级成统计结论，但目前仍不可审计到字段级。 | I |
| 是否存在可能误导 A2a 的强主张 | 风险较低，但有维护性风险 | `review.md` 第 68、106、119 行明确声明通用叶子不是原文全集、候选叶子为 `schema_seed` / `not_verified`，避免了最严重误导。风险在于 C02--C07 仍把通用接口写成“来自本文 RQ / 方法 / 分类 / 评价 / 讨论结构”，A2a 若只读这些 C 条目会低估原文 extraction form。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足以忠实复原原文 schema。建议最小修复为以下骨架。所有叶子在未完成完整 PDF 表图精核前只应为 `schema_seed`，不得进入 `statistical_synthesis`。

| 节点 / 叶子 | 父节点 | 原文定义 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| root：2004--2009 SE SLR tertiary update | -- | 更新并整合 OS / FE 与 SE 的 tertiary study | OS、FE、SE、OS/FE、OS/FE+SE；unit = secondary study / SLR | 是，后续精核后可统计 | not_applicable / not_verified | abstract；3 Method；3.1 RQ；Conclusion |
| b0 前序研究与更新关系 | root | 本文如何继承、更新、扩展前序 tertiary studies | predecessor = OS / FE；relation = temporal_update / search_extension / combined_update_extension / external_update | 是 | predecessor_not_reported / not_applicable | Previous studies；Method 第 200--220 行；Conclusion 第 1343--1357 行 |
| leaf-b0-update-mode | b0 | update / extension 类型 | temporal update；search extension；temporal + search extension；none observed in 120 SLRs | 是 | not_reported | Conclusion 第 1343--1357 行 |
| b1 RQ 与范围 | root | RQ 如何定义统计问题和结果章节 | RQ1、RQ1.1、RQ1.2、RQ2、RQ3、RQ4、RQ5 | 是，作为 finding path 索引 | rq_not_reported | paper_content 第 221--248 行；PDF 第 3 页 |
| leaf-b1-time-window | b1 | 统计时间窗 | 2004-01-01--2008-06-30；2008-07-01--2009-12-31；2004-01-01--2009-12-31 | 是 | not_reported | RQ1.1/RQ1.2；Method |
| b2 语料收集与纳排 | root | 自动、手工、参考文献搜索及纳排 | search source；search string；manual source；dedup；selection；reference search；final exclusion | 是 | not_reported / not_verified | 3.4--3.5；Table 1；Fig. 2 |
| leaf-b2-search-source | b2 | 检索源 | ACM DL、IEEE Xplore、ScienceDirect、CiteSeerX、ISI Web of Science、Scopus；Table 1 manual sources | 是 | source_not_reported | 第 281--331 行；PDF 第 4--5 页 |
| leaf-b2-flow-count | b2 | 纳排分母链 | 1389、157、66、154、75、77、67；duplicates=69；excluded=79；final_exclusion=10 | 是 | not_verified | Fig. 2；第 315--357、469--476 行 |
| leaf-b2-exclusion-reason | b2 | final exclusion 10 篇原因 | not SE；duplicate reports from FE; out-of-period 2010; shorter version; zero quality / missing info | 是 | not_reported | 第 469--475 行；Fig. 2 |
| b3 决策与编码流程 | root | selection、quality、data extraction 的共识流程 | Ri/Rj independent evaluation；ADT；Rk third evaluation；six-researcher consensus | 局部统计，可做方法 schema seed | not_reported | Fig. 1；第 257--280 行 |
| leaf-b3-dcp-stage | b3 | DCP 应用阶段 | study selection；quality assessment；data extraction | 是 | not_applicable | 第 257--280、438、474 行 |
| b4 质量评价 rubric | root | DARE QA1--QA4 与评分 | QA1 inclusion/exclusion；QA2 search coverage；QA3 quality/validity；QA4 basic data/studies described | 是 | qa_not_reported / not_applicable | 3.6；Table 3 |
| leaf-b4-qa-score | b4 | 每篇 SLR 质量分数 | QA answer Y/P/N；score Y=1, P=0.5, N=0；final 0--4；quartile | 是 | not_verified | 第 387--447 行；Table 3 |
| b5 Data extraction form | root | 原文明确抽取字段 | 见下列叶子 | 是 | field_not_reported / not_applicable / not_verified | 3.7；Table 2 |
| leaf-b5-year | b5 | SLR 年份 | 2008 / 2009 for SE；2004--2009 for integrated tables | 是 | not_reported | 第 448--468 行；Table 2/4 |
| leaf-b5-review-type | b5 | Review Type | SLR；MA；MS | 是 | not_reported | 第 453--455 行；Table 2 |
| leaf-b5-review-scope | b5 | Review Scope | RQ；SERT；RT | 是 | not_reported | 第 456--459 行；Table 2 |
| leaf-b5-topic-area | b5 | SE Topic Area | Requirements Engineering、Distributed Software Development、Software Product Line、Software Testing、Empirical Research Methods 等开放但可回填分类 | 是 | not_reported / topic_other | 第 460、514--520 行；Table 2 |
| leaf-b5-citation-ebse-guideline | b5 | 是否引用 EBSE papers / SLR guidelines | EBSE Y/N；Guidelines Y/N；reference codes [14,8,20]、[15,16] 等 | 是 | not_reported | 第 461--462 行；Table 2/12 |
| leaf-b5-primary-study-count | b5 | SLR 分析的 primary studies 数量 | 非负整数；可能来自明示或表格 | 是 | not_reported / inferred_from_table | 第 463--464 行；Table 2/9 |
| leaf-b5-practitioner-guidelines | b5 | 是否包含实践指南 | Y/N；显式 identifiable part；discussion 中也比较 implicit / explicit | 是 | not_reported | 第 465--466、807--820 行；Table 10 |
| leaf-b5-source-type | b5 | 首次报告来源类型 | J；C；WS；BS | 是 | not_reported | 第 467--468 行；Table 2 |
| b6 外部主题 / 教育 / 实践映射 | root | 用 SE Curriculum / SWEBOK 判断教育和实践相关性 | education = Yes / Possibly / No；practitioner = Yes / Possibly / No；Curriculum section；SWEBOK chapter | 是 | not_mapped / academic_only | 第 521--523、663--678 行；Table 5/6 |
| b7 RQ-to-finding path | root | 每个 RQ 的统计表和 conclusion 映射 | RQ1→Table4；RQ2→Table2/5/6；RQ3→Table7/8；RQ4→Table9--12；RQ5→Table3/13 + regression/correlation | 是，A2a 精核后 | missing_table_anchor / not_verified | Section 5；Conclusion |
| leaf-b7-positive-change | b7 | 正向变化 finding | growth；topic coverage increase；researcher/org/country spread；more mapping studies | 是，限原文语料 | not_supported | 第 1269--1279 行 |
| leaf-b7-limitation-gap | b7 | 限制 / gap finding | no primary-study QA；poor synthesis; few practitioner guidelines; EBSE not fully realised | 是，限原文语料 | not_supported | 第 1280--1342 行 |
| b8 Validity / reporting limitation / artifact | root | 作者对检索、质量、抽取和报告的效度限制 | search coverage limitation；QA4 subjectivity；QA2 inconsistency；poor reporting; Appendix A study list; replication package not reported | 局部可统计或风险字段 | not_reported / no_replication_package_reported | Section 6；Appendix A |

建议另外增加关系边表：

| 关系边 | 源节点 | 关系类型 | 目标节点 | 缺失值语义 | 证据定位 |
|---|---|---|---|---|---|
| edge-rq1-growth | RQ1 / time-window | supports | Table 4 / growth finding | no_count_table | Section 5.1 |
| edge-rq2-topic | RQ2 / topic-area | supports | Table 2 / Table 5 / Table 6 / coverage finding | no_topic_mapping | Section 5.2 |
| edge-rq3-actors | RQ3 / authors-organisations-countries | supports | Table 7 / Table 8 / diffusion finding | no_affiliation_data | Section 5.3 |
| edge-rq4-limitations | RQ4 / review type / QA / practitioner guideline | supports | Table 9--12 / limitation finding | no_limitation_metric | Section 5.4 |
| edge-rq5-quality | RQ5 / QA score | supports | Table 3 / Table 13 / regression / correlation | no_quality_score | Section 5.5 |
| edge-dcp-process | DCP | governs | selection / quality assessment / data extraction | no_consensus_process | Fig. 1 |
| edge-topic-external-map | topic area | mapped_to | SE Curriculum / SWEBOK | not_mapped | Table 5 / 6 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补完整 RQ 主轴 | `review.md` 的“根问题 / RQ 到主干分支映射”和“维度树结构” | 显式列出 RQ1、RQ1.1、RQ1.2、RQ2、RQ3、RQ4、RQ5，并把每个 RQ 连接到对应字段和结果表。影响：否则 Paper2 的 finding path 无法从 RQ 追溯到字段和统计观察。 | `paper_content.txt` 第 221--248 行；PDF 第 3 页 | I |
| 修正单位对象 | `review.md` 第 74 行附近 | 把根节点单位对象改为 secondary study / SLR；把 primary study 作为 `number_primary_studies` 抽取字段，而不是根层 unit。影响：避免 A2a 混淆 tertiary 的样本单位和被二级研究纳入的一次研究数量。 | `paper_content.txt` 第 217--220、448--468 行 | M |
| 展开原文 extraction form | “原文模式候选叶子映射（A1 种子）” | 从 4 个候选叶子扩展到至少 Year、Quality Score、Review Type、Review Scope、Review Topic、Cited EBSE、Cited Guidelines、Number Primary Studies、Practitioner Guidelines、Source Type，并给出取值空间和缺失语义。影响：当前过小树会让 Paper2 错失最可迁移的字段合同。 | `paper_content.txt` 第 448--468 行；PDF 第 5 页；Table 2 | I |
| 展开 QA rubric | “维度树结构”“叶子维度表”“原文模式候选叶子映射” | 新增 QA1--QA4、Y/P/N、Y=1/P=0.5/N=0、final score、quartile 等叶子。影响：质量评价是原文 RQ5 和 Paper2 证据审计最强的模式之一，目前被压缩为“质量评价字段”。 | `paper_content.txt` 第 387--447 行；Table 3 | I |
| 补 DCP 和 Fig. 2 流程节点 | “维度树结构”与关系边表 | 把 DCP 作为决策 / 编码流程分支，把 Fig. 2 的 1389→157/66→154→75→77→67 分母链作为 corpus flow 叶子。影响：否则 run record / evidence chain 不能学习原文如何保留过程分母和共识机制。 | `paper_content.txt` 第 257--357、469--476 行；PDF 第 4、6 页 | I |
| 补外部分类和映射 schema | “原文模式候选叶子映射” | 增加 SE Curriculum section、SWEBOK chapter、education relevance、practitioner relevance、why 字段，并记录取值空间 Yes / Possibly / No / academic-only。影响：当前“实践影响字段”过粗，无法复现 RQ2 到 education / practice impact 的字段链。 | `paper_content.txt` 第 521--523、663--678、903--1138 行；Table 5 / 6 | I |
| 增加 RQ→表→finding 关系边 | 新增“关系边表” | 为 RQ1--RQ5 分别建立到 Table 4、2/5/6、7/8、9--12、3/13 的边，并说明 conclusion 中正向变化和限制如何由这些表支持。影响：没有关系边，A2a 只能看到字段，不能学习原文 finding 形成路径。 | Section 5；Conclusion 第 1261--1388 行 | I |
| 拆分 A.2 证据账本 | A.2 | 把 EV-002 / EV-003 这类 catch-all 证据拆成 RQ、DCP、search flow、QA rubric、data extraction form、Table 2、Table 4、Table 5/6、Table 7/8、Table 9--13、limitations、conclusion 等细粒度证据；每行填原文页码、表号、行号和短引。影响：目前 A.3 虽有回链，但无法审计具体字段来源。 | `review.md` 第 144--147 行；全文对应段落和 PDF 表图 | I |
| 保持 not_verified 降级但补精核任务 | A.4 | 继续保留 `not_verified`，但把 visual check 从一个总任务拆成 Table 2--13、Fig. 1、Fig. 2、RQ 页、QA 页的精核项。影响：防止 A2a 误以为“needs_manual_check”只是一项泛任务。 | `review.md` 第 168--171 行；PDF 第 3--13 页 | M |
| 记录 artifact 缺失语义 | 维度树与 A.2/A.3 | 不要臆造 replication package。可把 Appendix A 作为 study-list artifact，replication package 写 `not_reported`。影响：Paper2 的 artifact 字段需要区分“有附录清单”和“有开放复现包”。 | Appendix A；Conclusion / Limitations | I |

## 6. C/I/M 结论

- C：0 项。当前 `review.md` 明确把主要证据降级为 `not_verified` / `schema_seed`，没有把 roadmap、泛定位证据或弱证据升级成 `statistical_synthesis` 或 final research finding，因此暂未直接破坏 Paper2 的最终证据链。
- I：8 项。核心问题是原文 schema 复原过小：RQ 主轴、data extraction form、QA rubric、DCP、Fig. 2 分母链、Table 2--13 finding path、外部 curriculum / SWEBOK mapping 和 artifact 缺失语义均未充分展开。这会实质影响 Paper2 的维度模式可用性、A2a 回填任务和 candidate finding ledger 的可审计性。
- M：3 项。主要是根节点单位对象表述、A.4 精核任务粒度、以及 C02--C07 通用接口对 A2a 的潜在阅读歧义。
- 最终建议：NEEDS FIX。

最小修复方案：保留当前“六个通用接口不是原文全集”的声明，但必须把“原文模式候选叶子映射”升级为真正的原文 schema seed 表，并新增关系边表和细粒度 A.2/A.3 证据链。修复完成前，该篇只能作为粗粒度 schema seed，不能作为 Paper2 的完整维度树复原样本。
