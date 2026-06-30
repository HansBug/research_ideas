# petersen-2015-mapping-guidelines-update · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；已读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。本审计按 claim-evidence、story、reviewer risk 和 unsupported-claim 降级口径执行。
- 是否读取 `$research-planning`：是；已读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。本审计按“先理解原文研究问题、方法、实验/评价和可执行计划，不补造细节”的口径执行。
- 是否读取 `$oh-my-codex:autoresearch`：是；已读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本审计按 artifact-gated、validator-gated、不能以“看起来完成”替代可检查制品的口径执行。
- 是否完整阅读 `paper_content.txt`：是；已从标题、摘要、引言、背景、§3 Method、§4 Results、§5 Guideline updates、§6 Conclusions、Appendix A/B 和 references 连续阅读到文件末尾，覆盖全文 18 页文本提取内容。
- 是否核对 `paper.pdf`：是，但只做命令行版面核对；使用 `pdfinfo` 确认 PDF 为 18 页，并用 `pdftotext -layout` 核对第 4--5 页 Table 3 / Fig.1、第 8--10 页 Table 5 / Fig.13--16、第 14--16 页 Table 8--14 / Fig.20--21 和 Appendix B 表格版面。未做截图式人工视觉核对，因此不应把所有图形数值升级为完全视觉核验。

同时已读取文库级规则与 story：

- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/README.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/GUIDE.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/SUMMARY.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/patterns/pattern-field-schema.md`
- `project_1_llm_state_machine_modeling/paper_agent_based_slr/story/paper_story.md`

已读取单篇文件：

- `bibtex.bib`
- `metadata.json`
- `paper_content.txt`
- `review.md`
- `paper.pdf` 关键页命令行版面核对

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标不是普通领域综述，而是“对 systematic mapping studies 的 systematic mapping”，用于更新 2008 年 systematic mapping guideline。摘要明确三层目标：识别 systematic mapping process 如何被执行，包括 search、study selection、analysis、presentation of data；识别 improvement potentials；据此更新 guideline。对应 `paper_content.txt` 第 11--26 行。

引言贡献声明有三项：评估 SE systematic mapping studies 的当前实践；把识别出的 mapping guideline 与 Kitchenham and Brereton 的 best practices 对比；整合 findings 以提出 guideline updates。对应第 82--89 行。

原文显式 RQ 在 §3.1：

- RQ1：哪些 guideline 被 SE systematic mapping studies 采用。
- RQ2：覆盖哪些 SE topic。
- RQ3：在哪里、何时发表。
- RQ4：systematic mapping process 如何执行，包含 study identification、categorization / classification schemes and processes、visualization of results。

对应第 216--232 行。RQ 本身已经构成维度树根下的四条问题主干，而不仅是 planning / conducting / reporting 三阶段。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法流程如下：

1. Search：基于 PICO 提取 population / intervention / comparison / outcome，但 outcome 明确不是可测效果；形成三组关键词：software engineering、systematic mapping / maps、method / tool / classification / framework / guideline 等。检索 IEEE Xplore、ACM、Scopus、Inspec/Compendex；2013 年执行检索，覆盖 2012 年及以前文献。对应第 236--294 行。
2. Study selection：title/abstract、full-text reading、quality assessment，并通过 backward snowballing 补充；纳入条件是研究方法和 mapping 结果、SE 领域、2004--2012；排除 conference summary/editorial/guideline/template、非 peer-reviewed、非英文、全文不可得、book/gray literature、重复研究。对应第 297--332 行。
3. Quality assessment：三个质量问题分别是 mapping 动机是否清楚、mapping process 是否清楚定义、是否有 empirical evidence / results；57 篇做质量评价。对应第 333--346 行。
4. 可靠性补救：第一作者构造 validation sets、检查漏检、复查 quality/full-text 阶段排除项，导致若干研究被补回。对应第 347--366 行。
5. Data extraction：Table 3 是显式 extraction form。字段包括 Study ID、Article Title、Author Name、Year of Publication、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type，并映射 RQ1/RQ2/RQ3/RQ4。对应第 367--409 行。
6. Analysis and classification：抽取项被 tabulated 和 visually illustrated；strategies 被 grouped and given a theme；每个 theme 下的论文计数。study identification phase 有 choosing search strategy、developing the search、evaluating the search、inclusion/exclusion 四个主主题。对应第 376--385 行。
7. Validity evaluation：使用 descriptive validity、theoretical validity、generalizability、interpretive validity，并单独说明 repeatability。对应第 386--391 行、第 412--490 行。
8. Finding 形成：§4 的频数和分类观察进入 §5 guideline updates；Table 5 把 systematic mapping process 的活动映射到多个 guideline，进而得出“现有 guideline 不完整，所以需要更新 guideline”的方法学 finding。对应第 691--715 行和第 1482--1533 行。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 远大于当前 `review.md` 的六个通用接口：

- Extraction form：Table 3，字段为 Study ID、Article Title、Author Name、Year of Publication、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type；并给出值类型和 RQ 映射。对应第 392--409 行，PDF 第 4 页。
- Study selection / quality schema：纳入 / 排除条件、Fig.1 selection flow、三个 quality assessment questions、validation set / excluded-paper review 补救流程。对应第 297--366 行，PDF 第 4--5 页。
- Topic taxonomy：RQ2 使用 SWEBOK，另增 Education 和 mapping studies on research methodologies。对应第 522--533 行和 Appendix B Table B.15 第 1585--1597 行。
- Venue taxonomy：journal / conference / workshop，另有 specific venues top list。对应第 534--546 行和 Appendix B Table B.16 第 1598--1605 行。
- Guideline-adoption classification：十类 guideline / template / book / prior studies，附录 B.17 给出 study lists。对应第 551--580 行和第 1559--1575 行。
- Search strategy schema：choosing search strategy 包含 database search、snowballing、manual；develop search 包含 PICO、consult librarians/experts、iteratively improve、keywords from known papers、standards/encyclopedias/thesaurus；evaluate search 包含 test-set、expert evaluation、authors' web pages、test-retest。对应第 593--611 行、第 1606--1651 行。
- Inclusion/exclusion coding scheme：objective criteria / objectivity evaluation、additional reviewer / disagreement resolution、decision rules；Table 6 给出 two-reviewer decision combinations A--F。对应第 612--623 行、第 1038--1067 行和 PDF 第 12 页。
- Data extraction process coding：objective criteria、additional reviewer / disagreement resolution、test-retest。对应第 630--637 行、第 1629--1636 行。
- Topic-independent classification facets：contribution type、research type、venue、study focus、research method；其中 research type 下有 evaluation research、validation research、solution proposal、philosophical paper、experience report、opinion paper；Table 7 是条件-决策表，Fig.19 把 research methods 映射到 validation/evaluation。对应第 638--683 行、第 1081--1136 行、第 1270--1342 行、第 1576--1584 行。
- Topic-specific classification schema：emerging classification vs existing scheme，既有 scheme 可来自 SWEBOK、IEEE、ISO/IEC standards；keywording 类似 grounded theory open coding。对应第 676--683 行、第 1234--1267 行和 Appendix B Table B.25。
- Visualization schema：line diagram、pie diagram、bar plot、bubble plot、Venn diagram、heatmap；Appendix B.26 给出逐项映射。对应第 684--690 行和 PDF 第 17 页。
- Validity taxonomy：descriptive validity、theoretical validity、generalizability、interpretive validity、repeatability；§5.1.5 还列出 publication bias、poorly designed extraction forms、researcher bias、sample quality、generalizability、interpretive reliability 等 mapping-specific threat examples。对应第 386--490 行、第 1272--1294 行。
- Guideline comparison / action model：Table 5 是核心 evidence table，把 Need for map、Study identification、Extraction/Classification、Study validity、visualization 等 process activities 映射到多个 guideline 与 This study / Kitchenham & Brereton。对应第 775--833 行，PDF 第 9 页。
- Quality rubric：Table 8 有 26 个 actions；Tables 9--13 给出 need for review、choosing search strategy、evaluation of search、extraction/classification、study validity 的 scoring rubric；Table 14 给出 existing studies 在各 rubric 档位上的计数。对应第 1359--1541 行，PDF 第 14--15 页。
- Roadmap figure：原文没有独立 roadmap figure；它有 guideline update process、Fig.17 study selection process、Fig.18 venue classification、Fig.19 research method classification。当前 `review.md` 中泛称 “roadmap branch/action point” 对本文不够精确，应改成 guideline activity / decision / rubric / process model。
- Artifact 字段：原文有 EndNote X6、Appendix A included/excluded studies、Appendix B category mappings，但没有现代 replication package / artifact link schema。不能把它升级成开放制品可用性字段。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的 finding path 不是“字段即发现”，而是：

1. Table 3 定义 extraction form，并抽取 guideline、topic、venue/year、process facets。
2. §4 和 Appendix B 对字段做分布、频次和逐 study 映射，例如 guidelines followed、topic-independent facets、quality assessment、visualization、validity threat discussion。
3. §5 将 §4 的实践观察与 existing guideline / best practices 做对比；Table 5 显示 existing guidelines 只覆盖部分 activities。
4. 据此形成 guideline update：mapping process 被组织为 planning、conducting、reporting，并补充 need/scoping、study identification、data extraction/classification、visualization、validity threats、reporting structure、quality rubric。
5. §6 回答 RQ1--RQ4：常用 guideline 是 Kitchenham/Charters 和 Petersen 2008；topic 覆盖多数 SWEBOK 领域但 education/configuration management 少；venue/year 显示 conference/workshop 与 journal 约各半、2011/2012 增长；process finding 支持 updated guideline 和 pocket rubric。对应第 1482--1533 行。

这条链路对 Paper2 关键：A2a/A2b 应记录“字段值 / 频次 / guideline comparison / rubric → candidate method finding → researcher adjudication”，不能把统计观察直接写成 final finding。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 大体准确，但单位对象写得不够精确。 | `review.md` 将根节点设为 “Guidelines for conducting systematic mapping studies in software engineering”，主类型为 mapping guideline update 方法树；这贴近原文目标。但根节点表写“primary study / secondary study”，而原文单位对象更准确是“SE systematic mapping / scoping studies, i.e., included mapping-study papers”，并由 Table 3 的 Study ID / article metadata 表示。 | M |
| 主干分支是否覆盖原文 schema | 未覆盖。 | 当前主干只有 planning、conducting、reporting、quality rubric、topic-independent dimensions。它覆盖 §5 的 guideline update 顶层，但漏掉 RQ1--RQ4 主干、Table 3 extraction form、Table 5 guideline comparison、Appendix B category mapping、validity taxonomy、visualization taxonomy、study selection / search 子 schema。 | C |
| 叶子维度是否足够具体 | 不足。 | `review.md` 已声明六个 `leaf-*` 是通用接口，不是原文 schema，这一点避免了误把通用接口当原文 schema。但“原文模式候选叶子映射”只列 planning / conducting / reporting / quality rubric / topic-independent dimension 五个粗粒度候选，仍没有把原文字段拆成可执行 leaf，如 Search strategy = database/snowballing/manual、Visualization = line/pie/bar/bubble/Venn/heatmap、Quality rubric = Table 9--13 档位。 | C |
| 取值空间是否可执行 | 多数不可执行。 | 通用叶子取值空间多写“自由文本”“完整枚举 / 层级枚举 / 自由文本加理由”；候选叶子只写笼统短语。原文很多取值空间已经可枚举：Table 3 抽取项、Appendix B.17--B.27、Table 8--14。当前 review 没有把这些枚举列出来，也没有说明哪些枚举封闭、哪些是开放编码。 | I |
| 关系边是否缺失 | 缺失。 | 原文存在多类关系：RQ ↔ Table 3 data item；process activity ↔ guideline source / This study / Kitchenham-Brereton in Table 5；rubric criterion ↔ score level；study ↔ category in Appendix B；statistical observation ↔ guideline update recommendation。当前没有关系边表，只用树表达，无法审计横向映射。 | I |
| 统计用途 / 分母是否正确 | 降级口径正确，但细分分母不足。 | `review.md` 正确写明 A1-DT 只作 schema_seed，不进入 SUMMARY 定量统计；也写明后续主统计池候选。但对原文内部统计分母没有细分：search result 7752/5082/60/43/54/44/52、included 52 mapping studies、quality 57/52 的阶段差异、Appendix B 各表分母不完全相同。 | I |
| 候选 finding 路径是否完整 | 不完整。 | `review.md` 写出“统计观察与候选发现”边界，但没有把原文具体 finding path 分解为：Table 3 抽取 → §4/Appendix B 频次 → Table 5 guideline coverage gap → §5 update → §6 RQ answers / rubric recommendation。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据粒度不足。 | A.1 存在本地来源；A.2/A.3/A.4 表头符合文库规则，并把泛定位证据降为 `not_verified` / `weak`，这是正确的。但 A.2 只有 4 行泛证据，原文核心表图和字段没有独立 evidence id；A.3 的 C02--C07 多为通用叶子结论，支撑对象不是原文 schema 叶子；A.4 只有结构检查和视觉检查，缺少 Table 3 / Table 5 / Table 8--14 / Appendix B 的逐项复验任务。 | I |
| 是否存在可能误导 A2a 的强主张 | 有中等风险。 | `review.md` 反复声明 not_verified / schema_seed，避免了最严重的统计升级。但快速卡片和 §2.3 写“这些字段几乎可以直接迁移为 A2a extraction form”、§2.5 写“直接统计目标”，若不接上完整字段表和缺失语义，A2a 可能误以为当前 review 已经完成原文 schema 复原。另有 “roadmap branch/action point” 泛称，与本文真实 guideline update 不完全匹配。 | I |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为忠实原文 schema 复原；应保留其降级声明，但把“原文模式候选叶子映射”扩展为下面这种最小可执行骨架。

| 根 / 分支 / 叶子 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---:|---|---|
| 根节点：SE systematic mapping studies 如何执行，以及如何据此更新 guideline | 单位对象：纳入的 mapping/scoping study paper；研究目标：evaluate current practice / compare guidelines / consolidate updates | 是，后续 A2a 精核后作为方法学统计样本 | `not_verified` 表示页码 / 图表未精核；`not_applicable` 只用于非 SMS 样本 | 摘要；引言贡献；§3.1 RQ；`paper_content.txt` 第 11--26、82--89、216--232 行 |
| RQ1 guideline adoption | Kitchenham 2004 / Kitchenham & Charters 2007；Petersen 2008；Budgen 2008；Dyba & Dingsyr 2008；Bailey 2007；Arksey & O'Malley 2005；Jorgensen & Shepperd 2007；Durham template；Biolchini 2005；Petticrew & Roberts 2006 | 是，分母为 included mapping studies，需以 Appendix B.17 精核 | `not_reported`、`not_codable_from_text`、`multiple_guidelines` | §4.4.1；Fig.5；Appendix B.17；第 551--580、1559--1575 行 |
| RQ2 topic taxonomy | SWEBOK areas + Education + Research methods；具体类含 software quality、tools/methods、process、management、configuration management、testing、construction、design、requirements、research methods、education | 是，分母为 included mapping studies；可多标签需核验 | `not_reported`、`outside_SWEBOK_added_category`、`ambiguous_topic` | §4.2；Fig.3；Appendix B.15；第 522--533、1585--1597 行 |
| RQ3 publication venue/year | Year 2007--2012；venue type = journal / conference / workshop；specific venue top list = IST / EASE / ESEM 等 | 是，分母为 included mapping studies | `not_reported`、`venue_type_unclear`、`year_out_of_scope` | §4.1--4.3；Fig.2--4；Table 4；Appendix B.16；第 493--546、1598--1605 行 |
| RQ4 study identification / search strategy | choosing search strategy = database / snowballing / manual；develop search = PICO / experts / iterative / known papers / standards; evaluate search = test-set / expert / author webpages / test-retest；inclusion/exclusion = objective criteria / additional reviewer / decision rules | 是，分母为 included mapping studies；每 action 独立布尔或多标签 | `not_reported`、`not_applicable`、`not_verified_from_appendix` | §4.4.2；Fig.6--9；Appendix B.18--B.21；第 593--623、1606--1651 行 |
| RQ4 quality assessment | quality assessment conducted = yes/no；quality questions = motivation clear / process defined / empirical evidence/results | 是；yes/no 分母为 included mapping studies，三个问题为本研究筛选 / quality gate | `not_reported`、`excluded_by_quality`、`not_applicable` | §3.3；§4.4.3；Fig.10；Appendix B.22；第 333--346、624--629、1622--1628 行 |
| RQ4 data extraction process | identify objective criteria；additional reviewer / disagreement resolution；test-retest | 是，分母为 included mapping studies | `not_reported`、`single_reviewer_only`、`unclear_process` | §3.4；§4.4.4；Fig.11；Appendix B.23；第 367--375、630--637、1629--1636 行 |
| Table 3 extraction form | Study ID、Article Title、Author Name、Year、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type；每项绑定 RQ | 是，是本文自身抽取字段，不是被综述论文的统计结果 | `not_reported_in_primary`、`not_applicable`、`needs_pdf_table_check` | Table 3；第 392--409 行；PDF 第 4 页 |
| Topic-independent classification | contribution type；research type；venue；study focus；research method；其中 research type = evaluation / validation / solution proposal / philosophical / experience / opinion | 是，需按 Fig.12 / Appendix B.24；research type 可由 Table 7 决策表判定 | `not_reported`、`ambiguous_between_validation_and_evaluation`、`multi_label` | §4.4.4；§5.1.3；Fig.12；Table 7；Fig.19；Appendix B.24；第 638--683、1081--1136、1270--1342、1576--1584 行 |
| Topic-specific classification | emerging classification；existing scheme；existing scheme 可为 SWEBOK / IEEE / ISO/IEC standards 等 | 是，分母为 included mapping studies；同时保留开放编码理由 | `not_reported`、`emergent_scheme_unclear`、`external_taxonomy_version_unknown` | §4.4.4；§5.1.3；Fig.13；Appendix B.25；第 676--683、1234--1267、PDF 第 17 页 |
| Visualization taxonomy | line diagram；pie diagram；bar plot；bubble plot；Venn diagram；heatmap | 是，分母为 included mapping studies；可多标签 | `not_reported`、`not_visualized`、`figure_type_unclear` | §4.4.5；Fig.14；Appendix B.26；第 684--690、PDF 第 17 页 |
| Validity taxonomy | descriptive validity；theoretical validity；generalizability；interpretive validity；repeatability；§5.1.5 threat examples；Appendix B.27 yes/no validity discussion | 部分可统计：validity discussion yes/no；threat taxonomy 为方法学 seed | `not_reported`、`reported_without_taxonomy`、`not_verified` | §3.6；§5.1.5；Fig.15；Appendix B.27；第 386--490、1272--1294、PDF 第 17 页 |
| Guideline comparison action matrix | Table 5 process rows：need for map、study identification、develop/evaluate search、inclusion/exclusion、extraction process、topic-independent/topic-specific classification、validity discussion、visualization；columns 为多个 guideline / This study / Kitchenham-Brereton | 是，但应作为 guideline coverage matrix，不和 primary-study frequency 混算 | `not_covered_by_guideline`、`covered`、`needs_pdf_matrix_check` | Table 5；第 691--715、775--833 行；PDF 第 9 页 |
| Quality rubric / evaluation rubric | Table 8 26 actions；Table 9 score 0--2；Table 10 score 0--2；Table 11 score 0--3；Table 12 score 0--3；Table 13 score 0--1；Table 14 counts | 是；分母为 included existing studies，且区分 score table 与 count table | `not_reported`、`not_applicable`、`no_description`、`minimal`、`partial`、`full` | §5.4；Table 8--14；Fig.20--21；第 1359--1541 行；PDF 第 14--15 页 |
| Reporting structure | Introduction；Related work；Research method with RQ/search/study selection/data extraction/quality assessment/analysis/classification/validity evaluation；Results by mapping questions；Discussion/Conclusions；Appendix with included/excluded borderline papers | 否，主要是 report structure pattern seed；可统计为“是否提供 reporting structure guideline” | `not_reported`、`not_applicable` | §5.3；第 1303--1355 行 |
| Artifact / appendix evidence | Appendix A included/excluded studies；Appendix B mappings B.15--B.27；EndNote X6 used internally | 局部可统计；不能升级为 replication package availability | `appendix_present`、`not_public_replication_package`、`tool_used_but_data_not_released` | §3.2 EndNote；Appendix A/B；第 270--271、1550--1651 行 |
| Finding path | extraction fields → §4 frequency/category observations → Table 5 coverage gaps → §5 updated guideline → §6 RQ answers / quality discussion | 不直接统计为 field；应进入 candidate finding ledger | `unsupported_candidate`、`statistical_observation_only`、`researcher_adjudication_needed` | §4--§6；尤其第 691--715、1482--1533 行 |

必须增加关系边表，至少包括：

| 关系边 | 源 | 关系类型 | 目标 | 缺失值语义 | 证据来源 |
|---|---|---|---|---|---|
| RQ-to-extraction | RQ1--RQ4 | drives / answers | Table 3 data items | `no_direct_rq_mapping` | §3.1、Table 3 |
| extraction-to-results | Table 3 data items | aggregated_as | §4 / Appendix B category tables | `not_tabulated` | §4、Appendix B |
| process-activity-to-guideline | Table 5 rows | covered_by / not_covered_by | guideline columns | `not_covered` | Table 5 |
| rubric-action-to-score | Table 8 actions | evaluated_by | Tables 9--13 scoring levels | `not_applicable` | §5.4 |
| observation-to-guideline-update | §4 observations / Table 5 gaps | motivates | planning / conducting / reporting guideline update | `discussion_only` | §5--§6 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 把原文 RQ1--RQ4 作为维度树主干或至少作为主干映射层 | `review.md` 的“根问题 / RQ 到主干分支映射”和“维度树结构” | 当前只用 planning / conducting / reporting / quality / topic-independent，会遮蔽原文 RQ 结构。建议新增 RQ1 guideline adoption、RQ2 topic、RQ3 venue/year、RQ4 process execution，并说明 §5 guideline update 三阶段是由 RQ4/process observations 与 Table 5 推导出的更新层。 | `paper_content.txt` 第 216--232 行 | C |
| 展开 Table 3 extraction form 为叶子字段 | “叶子维度表”或新增“原文 extraction form 叶子表” | 列出 Study ID、Article Title、Author Name、Year、Area in SE、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type；为每个字段写值类型、RQ 映射、缺失值语义。 | Table 3；第 392--409 行；PDF 第 4 页 | C |
| 将“原文模式候选叶子映射”从 5 个粗项拆成可执行 schema | “原文模式候选叶子映射（A1 种子）” | 至少拆为 guideline adoption、topic taxonomy、venue/year、search strategy、search development、search evaluation、inclusion/exclusion、quality assessment、data extraction process、topic-independent classification、topic-specific classification、visualization、validity discussion、rubric scoring、reporting structure、appendix evidence、finding path。 | §4.4、§5、Appendix B；第 593--715、1081--1541、1550--1651 行 | C |
| 增加关系边表 | “维度树复原”内新增“关系边表” | 记录 RQ→extraction item、extraction item→Appendix B category table、Table 5 process activity→guideline coverage、Table 8 action→Tables 9--13 rubric score、§4 observation→§5 update recommendation。 | Table 3、Table 5、Table 8--14、Appendix B | I |
| 细化统计分母和统计池语义 | “统计与候选发现链路” | 区分检索流水线分母 7752/5082/60/43/54/44/52、included mapping studies 52、quality assessment 57、Appendix B category tables、Table 14 rubric counts；避免统一写“本文纳入样本或分类表”。 | Fig.1；§3.3；Appendix B；Table 14 | I |
| 补充 quality / validity / rubric 字段 | “叶子维度表”和 A.2/A.3 | 原文 quality 不只是泛泛“评价、证据与复现资产”。应加入三个 QA questions、validity taxonomy、Table 8 26 actions、Tables 9--13 scoring levels、Table 14 counts。 | 第 333--346、386--490、1272--1294、1359--1541 行 | I |
| 修正 artifact 表述边界 | §2.5、A1-M4、建议树 | 不要暗示有现代 replication package / open artifact 字段。本文有 EndNote、Appendix A/B 和 paper-level mappings，但未报告可下载数据包或 replication package。建议写为“appendix / mapping table evidence”，不是“复现资产完整字段”。 | 第 270--271、1550--1651 行 | I |
| 移除或改写 roadmap 泛称 | A.2 EV-002、叶子定义、候选发现用途 | 本文是 guideline update，不是 roadmap paper；没有 roadmap figure。将 “roadmap branch/action point” 改为 “guideline activity / recommendation / process model / rubric item”。 | §5 guideline updates；Table 5；Table 8--13 | M |
| 提升 A.2 证据账本粒度 | A.2 维度树证据账本 | 当前 4 条泛证据不足以审计原文 schema。建议新增 EV-Table3-extraction-form、EV-RQ、EV-search-selection、EV-guideline-comparison-Table5、EV-topic-independent-classification、EV-visualization、EV-validity-taxonomy、EV-quality-rubric、EV-appendix-B-mappings 等。仍可保持 `not_verified`，但必须有具体来源节 / 表 / 图。 | 全文关键表图 | I |
| 扩展 A.4 复验清单 | A.4 本地复验命令与人工核验清单 | 增加人工核验项：Table 3、Fig.1、Table 5、Fig.6--15、Fig.17--19、Table 8--14、Appendix B.15--B.27。通过条件要包含页码、表号、字段名、取值空间、分母一致。 | PDF 第 4--17 页 | I |
| 调整可能过强的“直接迁移”措辞 | §2.3、§2.5、§4 A1-M5 | 将“几乎可以直接迁移”“直接统计目标”改为“可作为 A2a 候选 schema seed；需经页码/表图核验、取值空间确认、缺失值语义定义、研究者采纳后迁移”。 | 文库 GUIDE §6.3.7；原文 Table 3 / Appendix B | I |

## 6. C/I/M 结论

- C：当前 `review.md` 虽然没有把通用 6 个 leaf 接口误当成原文 schema，并且显式写了降级声明，但“原文 schema 复原”仍过小。它没有把 RQ1--RQ4、Table 3 extraction form、Table 5 guideline comparison、Appendix B classification tables、Table 8--14 quality rubric 和 finding path 转成可执行叶子 / 关系边 / 取值空间。这会直接破坏 Paper2 A2a 的维度模式种子质量，使后续 agent 只能消费一个粗骨架，而不是原文真实的 evidence-engineering schema。
- I：A.1--A.4 结构存在，证据强度降级正确；但证据账本只有 4 条泛定位证据，无法追溯到具体表图和字段。统计分母、缺失值语义、关系边和 artifact 边界也不够精确，会实质影响证据链可审计性和后续 SUMMARY / A2a 回填可靠性。
- M：根节点单位对象可更精确；roadmap/action point 泛称应改为 guideline activity / recommendation；PDF 核对状态应区分命令行版面核对与人工视觉核对。
- 最终建议：NEEDS FIX。
