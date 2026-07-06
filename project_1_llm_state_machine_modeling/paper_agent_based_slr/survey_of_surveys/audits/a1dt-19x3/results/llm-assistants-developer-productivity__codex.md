# llm-assistants-developer-productivity · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer
- 是否读取 `$ai-research-writing-skill`：是；已读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。本审计按 claim-evidence、reviewer risk、claim strength 与 claims-to-avoid 口径执行。
- 是否读取 `$research-planning`：是；已读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`。本审计按“严格跟随原文方法、字段、评价、风险，不臆造缺失配置”的口径检查维度树可执行性。
- 是否读取 `$oh-my-codex:autoresearch`：是；已读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本审计采用 artifact-gated 思路，要求输出报告本身成为可复验完成 artifact。
- 是否完整阅读 `paper_content.txt`：是；已按行号覆盖 `paper_content.txt` 第 1--1842 行，包括摘要/引言、RQ0--RQ3、pre-review mapping、search/selection、quality assessment、data extraction/synthesis、RQ0 landscape、RQ1 method/instrument、RQ2 benefit/risk、RQ3 SPACE mapping、Discussion/Tetrad/recommendations、Threats、Conclusion、References 与 Primary Studies。
- 是否核对 `paper.pdf`：是，局部视觉核对；用 `pdftoppm` 导出并人工查看关键页：第 5 页 Table 1 检索式与数据库分母、第 8 页 Table 2 QA1--QA11、第 25 页 Table 10 与 Fig. 7 SPACE 子维度、第 28 页 Fig. 9 Tetrad。未逐页核对全部 Table 1--11 / Fig. 1--9，也未核验 Zenodo 包内部文件。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是综合 2014--2024 年 39 篇 peer-reviewed primary studies，回答 LLM-assistants 如何影响 软件开发者 productivity。其贡献声明包含四块：首次围绕该主题做 systematic review and mapping；结构化刻画 methodological strategies / evaluation practices / reported effects；用 SPACE 作为 productivity mapping lens、用 McLuhan Tetrad 做 discussion synthesis；发布 Zenodo replication package，包含 study data、selection decisions、exclusion rationales。

原文 RQ 是明确的四层结构：

- RQ0：研究 LLM-assistants 对 developer productivity 影响的 peer-reviewed studies 有哪些 characteristics。其结果字段包括 publication year、authorship、venue focus、LLM tools。
- RQ1：这些研究使用哪些 methodological strategies、procedures、instruments。其结果字段包括 empirical strategy、procedure、formative/summative objective、analysis type、data source、instrument origin、specific instrument/metric。
- RQ2：LLM-assistants 对 developer productivity 的影响是什么。其结果字段是 benefits 与 risks 的 thematic schema，并包含 contested theme。
- RQ3：哪些 productivity dimensions 被研究，以及如何映射到 SPACE。其 schema 是 SPACE 五维 + derived sub-dimensions + study-to-dimension matrix + overlap / coverage statistics。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文遵循 Kitchenham & Charters。方法流程不是单步摘要，而是：pre-review mapping → control papers → query iteration → database search → duplicate removal → title/abstract screening → full-text screening → snowballing → quality assessment → final synthesis。

关键分母链条如下：数据库初检 9,756；去重 803 后剩 8,953；标题摘要排除 8,725，剩 228；全文排除 189；snowballing 加 5；44 篇进入 QA；QA 排除 5；最终 39 篇。原文还记录 47 天标题摘要筛选、10 周全文筛选、2 周 snowballing、3 个月 synthesis、9 个月 weekly meetings，这些是过程证据与人工成本字段。

数据抽取与编码流程包括：初始 thematic analysis 抽取 study goals、tools、empirical strategy and design、tasks、settings、key results；每篇写 descriptive summary；随后三轮 targeted thematic analysis 分别服务 RQ1、RQ2、RQ3；主题合并后由第一作者与最后一位作者 cross-check citations against original text，以保证 traceability。

原文 statistical / finding 形成方式不是“频次 = finding”。RQ0--RQ3 先形成字段统计、分布、overlap 或主题频次；discussion 再用 McLuhan Tetrad 与 practitioner/researcher recommendations 把统计观察升级为 lessons learned、research gaps 和 recommendations。Code quality 同时出现在 benefit 与 risk，是明确的 contested finding path，需要保留 support/counter-evidence 与 boundary conditions。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 至少包含以下对象：

- Search / selection schema：Table 1 数据库与检索式；Fig. 1 PRISMA flow；IC1--IC3 / EC1--EC5；Rayyan exclusion tagging；control papers 与 query iterations。
- Quality rubric：Table 2 的 QA1--QA11，0--4 Likert scale，50% average threshold，5 篇因 QA 排除。
- Extraction / coding scheme：study goals、tools、empirical strategy/design、tasks、settings、key results；descriptive summary；RQ-specific thematic iterations；citation cross-check。
- RQ0 taxonomy：year distribution；author distribution；Table 3 venue focus；Table 4 LLM tools。
- RQ1 taxonomy：Table 5 Stol & Fitzgerald empirical strategies；Table 6 Glass/Vessey/Ramesh procedures；formative / summative objective；quantitative / qualitative / mixed analysis；Table 7 data source、instrument origin、instrument/metric。
- RQ2 thematic taxonomy：Fig. 6 + Table 8 八类 benefit；Table 9 五类 risk；code quality 的 benefit/risk 双重归属。
- RQ3 framework schema：SPACE 五维；Table 10 derived sub-dimensions 与 primary studies / percentages；Fig. 7 sub-dimension distribution；Fig. 8 dimension overlap；Table 11 quality metrics。
- Discussion / roadmap-like model：Fig. 9 McLuhan Tetrad，Enhance / Reverse / Obsolesce / Retrieve；developer recommendations 1--5；researcher recommendations 1--3；open issues / gaps。
- Threat schema：review methodology threats 与 primary evidence base limitations 两层，包括 selection/search bias、human-centered study identification、bias/repeatability、classification rigor、formative/controlled studies、methodological diversity、temporal relevance。
- Artifact fields：Zenodo supplemental material / replication package，声明包含 study data、selection decisions、exclusion rationales、control papers、query refinement、QA scores 等，但本次未下载核验包内部完整性。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的路径是：字段表和 thematic codes → RQ-specific distribution / summary → contested interpretation → discussion synthesis → recommendation / gap。典型例子：RQ1 从 strategy/procedure/instrument 字段得到 lab experiment 38%、mixed methods 69%、time to completion 31%、NASA-TLX mixed，然后在 threats 和 researcher recommendations 中转化为“当前证据多为 formative/controlled、缺少 longitudinal/team-based/shared metrics”。RQ2 从八类 benefit 与五类 risk 形成 mixed impact 结论，尤其将 code quality 标为 contested。RQ3 从 SPACE coverage 得到 90% 至少两维、15% 四维以上、Communication/Activity underexplored，再转化为研究者应补 well-being、team dynamics、human-human collaboration、validated instruments 的建议。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确，但单位对象写成 `primary study / secondary study` 有轻微不准。 | 原文是 SLR+SMS，真正分析单位是 39 篇 peer-reviewed primary studies，不是 secondary study；`review.md` 第 335 行把单位对象写成 `primary study / secondary study`。原文第 57--62、141--169 行支持 primary-study scope。 | M |
| 主干分支是否覆盖原文 schema | 不足。 | `review.md` 第 339--351 行只给 5 个泛化主干：范围/RQ、语料纳排、主题分类、方法干预、评价统计发现。这能覆盖 A1-M0--M6 接口，但不能忠实表达原文的 RQ0 landscape、RQ1 method/instrument、RQ2 benefit/risk、RQ3 SPACE mapping、Discussion/Tetrad、threats/artifacts 等主干。 | I |
| 叶子维度是否足够具体 | 不足，树过小。 | 正式事实源叶子只有 6 个通用接口 leaf（第 358--363 行）+ 5 个很粗的候选原文 leaf（第 371--375 行）。原文实际有 Table 1--11、Fig. 1--9、QA1--QA11、SPACE 12 个左右子维度、8 benefit、5 risk、5 practitioner recommendations、3 researcher recommendations、6 类 threats 等。 | I |
| 取值空间是否可执行 | 部分不可执行。 | 通用 leaf 的取值空间多为“自由文本”“完整枚举/层级枚举/自由文本加理由”“统计用途/候选发现”等，无法直接指导 A2a 回填。候选原文 leaf 的取值空间也把多个 schema 压成粗类别，如“效率、质量、满意度、认知负担、风险和负面效应”，没有保留 SPACE 五维/子维度、benefit/risk 主题、strategy/procedure 枚举。 | I |
| 关系边是否缺失 | 明显缺失。 | 当前关系边只有 method→evidence 与 taxonomy→finding（第 381--382 行）。原文需要保留至少 RQ→结果表、strategy↔instrument、procedure overlap、benefit/risk↔evidence、SPACE dimension↔sub-dimension↔primary study、quality metric↔Performance/Quality、Tetrad↔recommendation、threat↔mitigation 的关系。 | I |
| 统计用途 / 分母是否正确 | 降级纪律正确，但分母粒度不足。 | `review.md` 第 388--390 行正确禁止 A1-DT 进入主统计池，但没有为原文字段分别记录分母：39 primary studies、44 QA candidates、9,756 initial records、8,953 screened records、228 full texts、17 control papers、SPACE dimension counts 等。 | I |
| 候选 finding 路径是否完整 | 部分完整但过粗。 | 前文第 89--137、160--169 行对 RQ summaries、contested code quality、Tetrad/recommendations 描述充分；但维度树事实源第 390、431、433 行只抽象为“候选发现台账 / 研究者裁决”，没有将 RQ2 benefit/risk、RQ3 underexplored dimensions、RQ1 methodological limitations、Threats 中的 primary evidence limitations 分别作为可追溯 finding path。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据过泛。 | A.1--A.4 表头齐全；A.2 全部证据为 `not_verified`，这符合 A1-DT 降级纪律。但证据账本只有 5 行，行号范围均为“邻近段落”，原文短引均为“见释义”，没有绑定 `paper_content.txt` 行号、页码、表号和图号，无法审计具体叶子的来源。 | I |
| 是否存在可能误导 A2a 的强主张 | 有轻度风险但已被降级声明缓解。 | `review.md` 第 329、367、388--390、423--434 行明确说明通用 leaf 不是原文全集、候选 leaf 仅 schema_seed/not_verified，不进入定量统计。因此不是 C。但 SUMMARY 已把该文列为“RQ 驱动分类树 / 生产力 benefit-risk 评价树”，如果 A2a 只读事实源树而不读历史字段树，会误以为原文 schema 已被足够复原。 | I |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为原文 schema 的事实真源；建议把“历史草稿字段树”中的完整结构迁移、收敛到 `## 维度树复原`，并将通用 6 leaf 保留为跨论文接口层，而不是主事实树。建议最小骨架如下。

| 节点 | 叶子维度 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| 根节点：LLM-assistants 对 developer productivity 的 SLR+SMS schema | 研究对象、影响对象、证据对象、解释框架 | LLM-assistants；developer productivity；peer-reviewed primary studies；SPACE / Tetrad | 是，描述性 | `not_reported` / `not_applicable` | 摘要；引言贡献；RQ 列表；`paper_content.txt` 行 7--21、57--73、132--169 |
| RQ0 landscape | publication year | 年份 2014--2024；ChatGPT 前后；2024 peak | 是，分母 39 | `not_reported` | Fig. 2；行 414--418 |
| RQ0 landscape | authorship distribution | author count；single-publication author；multi-publication author | 是，分母 154 authors | `not_reported` | §4.2；行 419--428 |
| RQ0 landscape | venue focus | SE/CS、HCI、information systems、human-aspects、AI for software、SE education | 是，分母 39 | `not_reported` | Table 3；行 429--480 |
| RQ0 landscape | LLM tool | ChatGPT、GitHub Copilot、Tabnine、GPT-4、CodeWhisperer、GPT-3.5、Claude、Codex、Gemini 等 | 是，分母 39，可多值 | `not_reported` | Table 4；行 485--513 |
| Protocol / corpus | database search | ACM、IEEE、ScienceDirect、Web of Science、Scopus、Springer；每库 search string 与 count | 是，分母 9,756 records | `not_searched` / `not_supported_by_database_syntax` | Table 1；行 182--209；PDF p.5 已核对 |
| Protocol / corpus | inclusion / exclusion criteria | IC1--IC3；EC1--EC5 | 是，可用于 exclusion code | `not_applicable` | 行 210--232 |
| Protocol / corpus | screening flow | initial 9,756；dedup 803；screened 8,953；excluded 8,725；full text 228；snowball +5；QA 44；QA excluded 5；included 39 | 是，PRISMA-style 分母链 | `not_reported` | Fig. 1；行 294--334、337--363 |
| Protocol / corpus | human validation / cost | first author screening；second/last validation；meetings；47 days；10 weeks；2 weeks；9 months | 可统计为过程字段，不用于领域统计 | `not_reported` | 行 342--363、1516--1523 |
| Quality rubric | QA criterion | QA1--QA11 | 是，分母 44 QA candidates | `not_applicable` | Table 2；行 364--390；PDF p.8 已核对 |
| Quality rubric | QA score / threshold / exclusion | 0--4 Likert；50% threshold；excluded_by_QA=5 | 是，分母 44/39 | `not_reported` | 行 387--400 |
| Extraction / coding | extracted field | study goals、tools、strategy/design、tasks、settings、key results、descriptive summary | 是，字段级 | `not_extracted` / `not_reported` | 行 402--411 |
| Extraction / coding | thematic iteration | initial thematic analysis；RQ1 method；RQ2 benefit/risk；RQ3 SPACE mapping | 可统计为 coding process | `not_reported` | 行 405--411 |
| Extraction / coding | traceability check | citation cross-check by first and last authors | 布尔 / 过程字段 | `not_reported` | 行 410--411 |
| RQ1 method schema | empirical strategy | Field Study、Field Experiment、Experimental Simulation、Laboratory Experiment、Sample Study、Judgment Study | 是，分母 39 | `not_classified` | Table 5；行 521--574 |
| RQ1 method schema | procedure | Survey、User Experiment、Concept Implementation、Interview、Case Study；允许多值与 overlap | 是，分母 39，多值 | `not_classified` | Table 6 / Fig. 4；行 579--609 |
| RQ1 method schema | objective | formative、summative | 是，分母 39 | `not_classified` | 行 610--621 |
| RQ1 method schema | analysis type | quantitative、qualitative、mixed | 是，分母 39 | `not_classified` | 行 622--625 |
| RQ1 instrument schema | data source / instrument origin | Self-Reported / Behavioral & Performance Metrics；Designed by Authors / Validated Instruments and Frameworks / Validated Frameworks | 是，分母 39，多值 | `not_reported` | Table 7；行 626--660 |
| RQ1 instrument schema | instrument / metric | surveys, interviews, NASA-TLX, SPACE surveys, TAM, self-efficacy, AAR/AI, affect questionnaire, task completion/correctness, acceptance rate, interaction logs, time, code quality metrics, productivity gain, TCQ, RBV | 是，多值 | `not_reported` | Table 7；行 626--660 |
| RQ1 finding path | metric caveat | acceptance rate should not be used alone；cognitive load mixed；throughput-quality trade-off | 候选 finding，不作 final | `not_applicable` | 行 688--719、721--742 |
| RQ2 benefit taxonomy | benefit theme | accelerate development；minimize online code search；automate trivial/repetitive tasks；support knowledge acquisition；support code-adjacent tasks；reduce task initiation overhead；improve code quality；support debugging/troubleshooting | 是，分母 39 / theme frequency | `not_observed` | Fig. 6、Table 8、§6.1；行 743--933 |
| RQ2 risk taxonomy | risk theme | fail to meet requirements；promote over-reliance/cognitive offloading；limit code quality；disrupt flow；reduce team collaboration | 是，分母 39 / theme frequency | `not_observed` | Fig. 6、Table 9、§6.2；行 934--1043 |
| RQ2 contested theme | code quality direction | benefit、risk、mixed、context-dependent；support evidence；counter-evidence；boundary condition | 候选 finding，必须保留反证 | `not_contested` | 行 905--927、1006--1032、1048--1055 |
| RQ3 SPACE mapping | SPACE dimension | Satisfaction、Performance、Activity、Communication、Efficiency | 是，分母 39，多值 | `not_mapped` | Table 10 / Fig. 7--8；行 1056--1210；PDF p.25 已核对 |
| RQ3 SPACE sub-dimension | sub-dimensions | Developer experience、Self-efficacy、Trust、Cognitive load、Quality、Impact、Activity、Human-LLM collaboration、Human-human collaboration、Temporal efficiency、Interruptions and flow、Automation；well-being as absent/underexplored | 是，多值 | `not_reported` / `absence_evidence` | Table 10；行 1091--1110、1132--1189 |
| RQ3 quality metric | quality metric type | Passing unit tests、Functional correctness/accuracy、Code smells、BLEU、Halstead、Cyclomatic complexity、Translation error rate、Maintainability index、Cognitive complexity、Defect density/rate、Technical debt、Code coverage | 是 | `not_reported` | Table 11；行 1190--1204 |
| Discussion synthesis | Tetrad category | Enhance、Reverse、Obsolesce、Retrieve | 候选 explanation/finding path，不作 primary statistical field | `not_applicable` | Fig. 9 / §8.1；行 1227--1309；PDF p.28 已核对 |
| Recommendation path | practitioner recommendation | calibrated trust；coder-to-reviewer role; workflow adaptation; organizational adoption; professional/ethical accountability | 候选 recommendation | `not_reported` | §8.2；行 1310--1422 |
| Recommendation path | researcher recommendation | shared frameworks/validated instruments/longitudinal field team studies；multidimensional evaluation; confounder reporting/replication | 候选 recommendation | `not_reported` | §8.3；行 1423--1498 |
| Threat schema | review-methodology threat | study selection bias；human-centered study identification；bias/repeatability；classification rigor | 风险字段 | `not_reported` | §9.1；行 1499--1532 |
| Threat schema | primary evidence limitation | formative/controlled studies；methodological diversity；temporal relevance | 风险字段 | `not_reported` | §9.2；行 1533--1549 |
| Artifact / reproducibility | artifact availability | Zenodo package URL；study data；selection decisions；exclusion rationales；control papers；query refinement；QA scores | 布尔 / 链接状态；需外部核验 | `not_verified` / `dead_link` / `available` | 摘要行 20--21；贡献行 71--73；references 行 1618--1620；未核验包内部 |

关系边建议至少补：RQ→结果表；database→record count；screening stage→exclusion reason；QA score→eligibility；strategy→instrument；procedure→overlap；metric→SPACE sub-dimension；benefit/risk→supporting PS list；code_quality benefit↔risk contested edge；SPACE dimension→underexplored gap；Tetrad category→recommendation；threat→mitigation；artifact→reported reproducibility field。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将完整原文 schema 从历史草稿迁移进事实源维度树 | `review.md` `## 维度树复原`，尤其第 337--375 行 | 不要让 6 个通用接口 leaf 成为事实树主体；新增 RQ0/RQ1/RQ2/RQ3/Discussion/Threats/Artifacts 主干和叶子，至少覆盖上节建议骨架。 | 原文 Table 1--11 / Fig. 1--9；`review.md` 第 200--288 行历史树更接近完整结构但被废弃。 | I |
| 修正候选原文叶子过粗问题 | `review.md` 第 365--375 行 | 将 5 个粗候选 leaf 拆为可执行叶子：strategy、procedure、objective、analysis type、instrument origin、metric、benefit theme、risk theme、SPACE dimension/sub-dimension、quality metric、QA criterion、artifact status 等。 | 原文行 521--742、743--1210、364--411。 | I |
| 补充 QA / eligibility 分支 | `review.md` 维度树结构、叶子表、A.2/A.3 | 单独建立 `quality_assessment` 节点：QA1--QA11、0--4 score、50% threshold、excluded_by_quality=5、final_included=39；明确它决定哪些 primary studies 进入 synthesis。 | 原文 Table 2，行 364--400；PDF p.8 已核对。 | I |
| 补充 extraction form / coding process 分支 | `review.md` 维度树结构、叶子表、A.2/A.3 | 建立 `extraction_and_synthesis` 节点，记录 extracted fields、descriptive summary、initial thematic analysis、targeted iterations、citation cross-check。 | 原文行 402--411。 | I |
| 补充 RQ0 landscape 具体叶子 | `review.md` 维度树结构、候选叶子映射 | 增加 publication year、author distribution、venue focus、tool distribution，并为每个字段写分母 39/154、取值空间、缺失语义。 | 原文 Fig. 2、Table 3、Table 4；行 414--518。 | I |
| 补充 RQ1 method/instrument taxonomy | `review.md` 维度树结构、候选叶子映射 | 增加 empirical strategy 六类、procedure 五类及 overlap、formative/summative、analysis type、data source、instrument origin、instrument/metric 列表；保留 external taxonomy 来源 Stol/Fitzgerald、Glass/Vessey/Ramesh、Hartson。 | 原文 Table 5--7；行 521--742。 | I |
| 补充 RQ2 benefit/risk taxonomy 与 contested theme | `review.md` 维度树结构、关系边表、候选 finding 链路 | 将 8 benefit、5 risk 独立成叶子枚举；给 code quality 建立 contested edge：benefit evidence、risk evidence、context/task/metric boundary。 | 原文 Fig. 6、Table 8、Table 9；行 743--1055。 | I |
| 补充 RQ3 SPACE 层级枚举和质量指标表 | `review.md` 维度树结构、候选叶子映射、关系边 | 保留 SPACE 五维、12 个实际 sub-dimensions、well-being absence evidence、study-to-dimension matrix、dimension overlap、Table 11 quality metrics；不要只写“生产力结果/人因字段”。 | 原文 Table 10、Fig. 7--8、Table 11；行 1056--1210；PDF p.25 已核对。 | I |
| 补充 Tetrad / recommendation / roadmap-style finding path | `review.md` 候选 finding 链路、关系边表 | 建立 Tetrad category → lessons learned → practitioner/researcher recommendations 的关系边；标注这是 discussion synthesis / candidate recommendation，不是完成型统计 finding。 | 原文 Fig. 9、§8.1--8.3；行 1227--1498；PDF p.28 已核对。 | I |
| 补充 threats 和 primary evidence limitations 字段 | `review.md` 叶子表、迁移边界、A.2/A.3 | 将 review methodology threats 与 primary evidence base limitations 分开，作为风险字段和 claim-strength 降级依据。 | 原文 §9.1--9.2；行 1499--1549。 | I |
| 补强 A.2 证据账本定位 | `review.md` A.2 | 将 5 行泛证据拆为至少按主干/表图/关键 claim 的证据行，写 `paper_content.txt` 行号、PDF 页码、表/图编号、短引或释义，并将已视觉核对的 Table 1、Table 2、Table 10、Fig. 7、Fig. 9 标为已核对；未核对的仍保留 `not_verified`。 | 当前 A.2 第 413--417 行全为泛定位。 | I |
| 修正单位对象措辞 | `review.md` 第 335 行 | 将单位对象从 `primary study / secondary study` 改为 `primary study`；若保留 secondary study，应说明本论文自身是 secondary study，但被抽取的研究单位是 primary studies。 | 原文行 57--65、390--411。 | M |
| 保留但明确降级声明 | `review.md` 第 329、367、388--390 行 | 当前降级声明是正确的，应继续保留；在新增完整 schema 后仍标注 A1-DT 只作 `schema_seed`，不进入 SUMMARY 定量统计。 | GUIDE §6.3.7；pattern schema §8.6。 | 通过 |

## 6. C/I/M 结论

- C：无。当前 `review.md` 已显式声明 6 个通用 leaf 不是原文 leaf 全集，并把证据强度降为 `not_verified` / `weak`，没有把 roadmap、vision 或 not_verified 证据升级成 final finding，也没有把本论文的 LLM productivity 领域结论直接当成 Paper2 目标领域发现。
- I：有。主要问题是“事实源维度树过小”：当前 `## 维度树复原` 没有把原文 RQ0--RQ3、search/selection flow、QA rubric、extraction/coding process、RQ1 taxonomy、RQ2 benefit/risk taxonomy、RQ3 SPACE schema、Tetrad roadmap/recommendation、Threats、Artifacts 等可执行字段迁入事实源。它会实质影响 A2a/A2b 的 schema seed 质量、字段回填、分母管理和证据审计。
- M：有。单位对象措辞、PDF/Zenodo 核验状态、A.2 行号/页码精细度可以进一步改进。
- 最终建议：NEEDS FIX。
