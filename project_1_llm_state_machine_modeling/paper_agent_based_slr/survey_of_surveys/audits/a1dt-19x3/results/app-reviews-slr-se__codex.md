# app-reviews-slr-se · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（按任务结构字段记为 codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`、`references/planning-prompts.md`
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- 是否完整阅读 `paper_content.txt`：是；按行号全文阅读 1--2661 行，覆盖摘要、引言、研究方法、RQ、检索/纳排、F1--F18 抽取表、classification/coding scheme、全部 RQ 结果、Discussion、Threats、Related Work、Conclusion 和 References。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` / `mutool info` 确认 PDF 逻辑页数为 63 页，并抽样视觉核对关键页：Table 3（p.7）、Table 4（p.9）、Table 7（p.12）、Table 13（p.26--27）、Table 16--17（p.35--36）、Table 21（p.40）、Table 22（p.43）。未完成所有表格、图、supplementary 的逐页视觉核对。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是系统综述 app review analysis 如何支持软件工程。摘要明确覆盖 182 篇 2012--2020 年论文，并按 mined information、data mining techniques、supported software engineering activities、empirical evaluation quality/results 和 future research avenues 组织结论（`paper_content.txt` 行 8--20）。引言列出四项目标：识别 app review analysis 类型、识别 NLP/data mining 技术、识别支持的软件工程活动、报告 empirical evaluation 方法和结果（行 79--87）。贡献声明包括 mining approaches/techniques synthesis、SE scenario knowledge、empirical evaluation summary、literature growth/gaps/future directions（行 93--97）。

原文显式 RQ 为五个：

| RQ | 原文问题 | 主要证据 |
|---|---|---|
| RQ1 | app review analysis 有哪些类型 | 行 105--119；结果 §3.2 / Table 7 |
| RQ2 | 使用哪些技术实现 app review analysis | 行 119--121；结果 §3.3 / Table 9--12 |
| RQ3 | 声称支持哪些 SE activities | 行 121--124；结果 §3.4 / Table 13--15 |
| RQ4 | 如何做 empirical evaluation | 行 124--126；结果 §3.5 / Table 16--20 |
| RQ5 | 现有方法支持软件工程师的效果如何 | 行 126--127；结果 §3.6 / Table 21--22 |

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

方法流程是 Kitchenham-style SLR：定义 RQ 和 protocol、执行 literature search/selection、按 agreed criteria 筛选、阅读入选研究、用 Table 3 数据抽取表收集数据，最后 synthesis for reporting（行 98--104）。

检索与纳排链条包括：2010-01 至 2020-12 时间窗、digital-library keyword search、manual issue-by-issue search、backward/forward snowballing、Table 1 inclusion/exclusion criteria、Table 2 manual search venues，以及 PRISMA 数量链。文本中可确认初始 1656 篇、303 duplicates、筛选 1353 篇、排除 1225 篇、manual search 增加 14 篇、snowballing 增加 40 篇，最终 182 篇（行 131--171）。Table 1 明确排除非英文、非 SE、secondary/tertiary studies、technical reports/manuals 等（行 182--193）。

数据抽取使用显式 Table 3 F1--F18。F1--F5 是 bibliographic/documentation；F6--F9 对应 RQ1--RQ3；F10--F18 对应 RQ4/RQ5 的 evaluation、annotation、quality、replication package 字段（行 172--176、227--269；PDF p.7 已视觉核对）。

编码和分类 schema 是原文维度树的关键，不只是结果摘要。原文构建三套 classification schemas：app review analysis（F6）、mining techniques（F7）、SE activities（F8）。构造方法是 content analysis 和 iterative coding：从既有类别/文献 taxonomy 出发，合并语义相关类别、删除不相关类别、加入未标注数据中抽象出的新类别，然后 final coding（行 283--313）。SE activity schema 基于 SWEBOK terminology，从 258 terms 到 58 candidate terms，再到 14 final activities（行 314--328）。Reliability 用 intra-/inter-rater agreement 检查，Table 4 给出 app review analysis 93%/87%、SE task 100%/87%、mining technique 90%/80%（行 321--338；PDF p.9 已视觉核对）。

统计与综合方式是描述统计、交叉表、range/median、five-number summary、qualitative synthesis；原文明确 RQ5 的 effectiveness evaluation 太异质，不适合 meta-analysis，因此采用 summarizing effect estimates（行 1485--1497）。这一点是 finding path 的方法约束。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式结构如下：

| 原文结构 | 内容 | 审计说明 |
|---|---|---|
| Extraction form | Table 3 F1--F18：Title、Authors、Year、Venue、Citation、Review Analysis、Mining Technique、SE Activity、Justification、Evaluation Objective/Procedure/Metrics/Result、Annotated Dataset、Annotation Task、Number of Annotators、Quality Measure、Replication Package | 这是最核心的原文 schema，不能只压缩为一个候选 leaf。 |
| Classification schema 1 | App review analysis 9 类：Information Extraction、Classification、Clustering、Search and Information Retrieval、Sentiment Analysis、Content Analysis、Recommendation、Summarization、Visualization | Table 7 有封闭枚举、数量和百分比。 |
| Classification schema 2 | Mining techniques 4 大类：Manual Analysis、NLP、ML、Statistical Analysis；另有 ML technique 分布和 technique × analysis 交叉表 | Table 9--12，Table 11 文本抽取有错位，需 PDF 精核。 |
| Classification schema 3 | SE activities 14 个 final terms，按 Requirements / Design / Testing / Maintenance 组织，并含 `NOT SPECIFIED` 缺失类别 | Table 13--15；PDF p.26--27 横排表已抽样核对。 |
| Coding scheme / reliability | content analysis、iterative coding、sample re-coding/cross-check、Table 4 intra/inter-rater agreement | 这是 taxonomy quality 字段，不应遗漏。 |
| Evaluation / artifact fields | effectiveness evaluation、user study、annotated datasets、annotation task、annotators、quality measure、public dataset、public tools、replication package | Table 16--22 与 F10--F18 对应。 |
| Quality / validity | search incompleteness、publication bias、screening/extraction/classification subjectivity、taxonomy reliability；protocol/pilot/cross-check mitigation | §5 Threats to Validity。 |
| Related-work comparison | Table 23 对比 previous surveys 的 study type、time period、paper count、RQ coverage | 是 scope/novelty 证据，不是 dimension tree 主干但应入证据账本。 |
| Roadmap figure | 原文没有显式 roadmap figure；Discussion 中有 future research directions / gaps | `review.md` 中泛写 roadmap/action point 应降级为模板残留，不能当作原文结构。 |

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文不是把频次表直接当 finding，而是通过 RQ-specific tables 形成讨论结论：

- Demographics / Table 5--6 支撑 “growing research area” 和高质量 SE venues 观察（行 1693--1715）。
- RQ3 / Table 13--15 支撑 “SE goals/use cases 描述不够清晰”“需要 reference model for review mining tools”（行 1716--1739）。
- RQ4 / Table 16--18 支撑 “evaluation datasets small”“public datasets/tools/replication packages insufficient”（行 1740--1767）。
- RQ5 / Table 21--22 支撑 “practice impact not yet clear，需要用 SE-specific concerns 评价”（行 1768--1782）。
- Tool / user-study evidence 支撑 practitioners' requirements、industrial needs、efficiency/scalability、training data/drift 等 future work（行 1783--1848）。
- Threats §5 把 search, publication bias, subjectivity, taxonomy reliability 作为结论外推边界（行 1849--1884）。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但单位对象有偏差 | `review.md` 把根节点定义为 app reviews SLR 目标/RQ/贡献声明，并标出 5 个主干（行 188--192），方向正确；但单位对象写成 `primary study / secondary study`，原文 Table 1 明确排除 secondary/tertiary studies（`paper_content.txt` 行 190--193），原文单位应是 primary study / paper / approach / evaluation artifact。 | I |
| 主干分支是否覆盖原文 schema | 不足且父子挂接错位 | 主干大致对应 RQ1--RQ5，但树结构把 `app review analysis 类型` 下挂 `研究范围与单位对象`、把 `mining technique` 下挂 `语料与纳排链条`、把 `评价与复现资产` 下挂 `方法 / 技术 / 干预分类`（`review.md` 行 196--208），语义错位。原文 RQ 与 F 字段的映射应是 RQ1/F6、RQ2/F7、RQ3/F8/F9、RQ4/F10--F12/F14--F18、RQ5/F13。 | I |
| 叶子维度是否足够具体 | 不足；已有防误读声明但原文叶子仍过小 | `review.md` 明确说明六个 `leaf-*` 是跨论文通用接口，不是原文全集（行 186、224），避免了最危险的误读；但“原文模式候选叶子映射”只有 5 行（行 228--232），把 F1--F18、三套 classification schema、coding/reliability、evaluation results、artifact fields、finding path 大量压缩，无法作为完整原文维度树。 | I |
| 取值空间是否可执行 | 部分可执行，整体仍太泛 | analysis type 9 类、mining technique 4 类、SE activity top categories 被列出（行 229--231），但缺少 Table 13 的 14 个 activities + `NOT SPECIFIED`、F10--F18 的 evaluation/objective/procedure/metric/result/dataset/annotation/quality/replication 细分、Table 19--22 的 user-study criteria/result 取值。许多通用 leaf 的取值空间仍是“完整枚举 / 层级枚举 / 自由文本”等元类型（行 215--220），不能直接执行 A2a 抽取。 | I |
| 关系边是否缺失 | 明显缺失 | 现有只有 method→evidence、taxonomy→finding 两条边（行 234--239）。原文至少需要 RQ→F 字段、F6→Table 7、F7→Table 9/10/11/12、F8/F9→Table 13/14/15、F10--F18→Table 16--22、results→Discussion gaps、artifact availability→replicability gap 等关系边。 | I |
| 统计用途 / 分母是否正确 | 降级纪律正确，但分母不够具体 | `review.md` 正确写明 A1-DT 不进入当前 SUMMARY 定量统计（行 182、245--247），没有把 `not_verified` 升级为 statistical synthesis；但分母写成“本文纳入样本或分类表”“统计结果 + discussion”等（行 246--247），没有逐字段记录 182、109、105、23、87、23 datasets、16 tools、14 SE activities 等分母。 | I |
| 候选 finding 路径是否完整 | 不完整 | `review.md` 提到 discussion gap（行 206--208、241--247），但没有把 Discussion 4.1--4.10 的 finding path 映射到具体 evidence tables：growing area、unclear use cases、reference model、small datasets、replication packages、practice impact unclear、practitioner requirements、industrial need、efficiency/scalability、training data/drift。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，证据强度纪律正确，但锚点过泛 | A.1--A.4 表头齐全（行 256--298），A.2 全部 `not_verified` 且 A.4 标 `needs_manual_check`，符合 A1-DT 不强行升级的纪律；但 A.2 只有 5 条泛定位证据（行 270--274），无精确页码/表号/行号，且 EV-002 泛写 “roadmap branch or guideline item” 与本文不符。 | I |
| 是否存在可能误导 A2a 的强主张 | 有局部风险，但不是不可控强主张 | 优点是行 186/224 已明确六个 leaf 不是原文全集，行 182/245--247 已冻结统计用途；风险是快速卡片写“是否统计池：是；可进入 A1 方法学统计池”（行 24）容易与 A1-DT `schema_seed` 降级口径混淆，且 A.4 `structure-check passed`（行 297）没有在本 review 中给出可复验命令输出或日志链接。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为忠实原文 schema，但可保留其“通用接口层 + 原文候选叶子层”的双层设计。最小修复应把“原文候选叶子映射”升级为以下骨架，并把原来的六个通用 leaf 明确标为 `interface_layer`。

| 根 / 主干 / 叶子 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|
| [dim-app-root] app reviews for SE SLR | 研究对象：182 primary studies；主题：app review analysis for SE | 是，后续主统计池候选；A1-DT 当前只 schema_seed | 不适用 | 摘要行 8--20；目标/贡献行 79--97；RQ 行 105--127 |
| [dim-protocol] 检索与纳排协议 | time window、digital libraries、specific/generic query、manual venues、snowballing、IC/EC、PRISMA counts | 是；分母为 identification/screening/inclusion counts | `not_reported`、`text_extraction_missing`、`not_verified` | Fig.1 / §2.2；行 131--171；Table 1 行 182--193；Table 2 行 210--224 |
| [leaf-search-counts] 搜索数量链 | 1656、303 duplicates、1353 screened、1225 excluded、14 manual、40 snowballing、182 final | 是 | `not_verified` for PRISMA visual count until PDF checked | 行 152--171；PDF p.4--5 |
| [dim-rq-field-map] RQ 到抽取字段映射 | RQ1--RQ5 ↔ F6--F18 | 是，作为 schema relation | `not_applicable` only if no RQ | RQ 行 105--127；Table 3 行 227--246；PDF p.7 |
| [leaf-f1-f5] 书目信息 | Title、Authors、Year、Venue、Citation | 是，metadata/demographics | `missing_metadata` | Table 3 F1--F5 |
| [leaf-f6-analysis] Review Analysis | F6.1 type、F6.2 mined information、F6.3 description；9 analysis types | 是；分母 182 studies，multi-label 需记录 | `not_reported` / `not_classifiable` | 行 197--199；Table 7 行 440--450；PDF p.12 |
| [leaf-f7-technique] Mining Technique | Manual Analysis、NLP、ML、Statistical Analysis；ML subtypes | 是；可与 F6 交叉统计 | `not_reported` / `multiple_techniques` | 行 200--201、639--657；Table 9--12；PDF p.17/40 等 |
| [leaf-f8-se-activity] SE Activity | 14 final activities under Requirements/Design/Testing/Maintenance + `NOT SPECIFIED` | 是；multi-label，Table 13 分母 182 | `not_specified` 是原文显式类别，不等同缺失抽取 | 行 202--206、885--910；Table 13 行 945--1016；PDF p.26--27 |
| [leaf-f9-justification] Support justification | 自由文本理由；可关联 SE goal/use case | 可做 qualitative coding，不宜频次化除非 A2a 定义类别 | `no_justification` | 行 207--209；Discussion 4.2 行 1716--1730 |
| [dim-coding-reliability] 分类构造与可靠性 | content analysis、iterative coding、schema source、merge/remove/add category、inter/intra agreement | 是；作为质量/validity 字段 | `not_reported` / `not_verified` | §2.4 行 283--341；Table 4 行 321--338；PDF p.9 |
| [leaf-analysis-schema-construction] analysis schema 构造 | previous survey 5 categories + 14 additions + merge/remove + recommendation category + final 9 | 可统计为 schema construction pattern | `not_reported` | 行 295--304 |
| [leaf-technique-schema-construction] technique schema 构造 | prior surveys/text analytics → 5 categories → remove feature extraction → final 4 | 可统计 | `not_reported` | 行 305--313 |
| [leaf-se-activity-schema-construction] SE activity schema 构造 | SWEBOK 258 terms → 58 candidate activities → 14 final activities | 可统计 | `not_reported` | 行 314--328 |
| [dim-evaluation] Empirical evaluation schema | effectiveness evaluation、user-perceived quality、evaluation subject/objective/procedure/metrics/result | 是；分母 109 evaluated, 105 effectiveness, 23 user studies, 87 RQ5 result studies | `not_evaluated` / `not_reported` / `not_comparable` | §3.5--3.6；行 1245--1251、1485--1497 |
| [leaf-f10-f13] Evaluation objective/procedure/metrics/result | effectiveness/user-perceived quality；precision/recall/F1/accuracy/usability/usefulness等；range/median | 是，但异质性下不做 meta-analysis | `not_reported` / `not_comparable` | Table 21--22；PDF p.40/p.43 |
| [leaf-f14-f17] Annotation dataset / task / annotators / quality | app store、review count、annotation task、annotator count 1--5 median 2、quality metrics Cohen's Kappa/percentage/Jaccard/Fleiss | 是 | `no_public_dataset`、`quality_measure_not_reported` | 行 1253--1281；Table 16、18；PDF p.35 |
| [leaf-f18-artifact] Replication package / public assets | replication package available? annotated dataset/tool/script available? author contacted? public datasets/tools | 是；artifact availability field | `no_replication_package`、`no_public_tool`、`link_unverified` | 行 265--269、1263--1267、1758--1767；Table 16--17；PDF p.35--36 |
| [dim-result-presentation] Evidence presentation tables | Fig.1--4, Table 5--23, cross-tabs, five-number summary, range/median, related survey comparison | 是，作为 report structure pattern | `table_text_misaligned` / `needs_pdf_check` | `paper_content.txt` table markers；PDF 抽样核对页 |
| [dim-finding-path] 统计观察到 discussion gaps | growth、use case vagueness、reference model、small datasets、replication gap、practice impact unclear、practitioner needs、industrial need、efficiency/scalability、training data/drift | 只作为 candidate_finding / schema_seed，不是 Paper2 final finding | `candidate_only`、`needs_counterevidence` | Discussion 行 1693--1848；Conclusion 行 1939--1971 |
| [dim-validity] Validity threats / mitigation | incomplete keywords、publication bias、screening/extraction/classification subjectivity、taxonomy reliability、protocol/pilot/cross-check | 是，作为 threat pattern | `not_reported` | §5 行 1849--1884 |
| [dim-related-work-scope] Previous survey comparison | study type、time period、No. papers、RQ1--RQ5 coverage | 可做 scope/novelty support，不作领域统计 | `not_applicable` | §6 行 1885--1938；Table 23 行 1923--1933 |

最小关系边表应包含：

| 关系边 | 源 | 关系 | 目标 | 缺失语义 / 用途 |
|---|---|---|---|---|
| [edge-rq-f6] | RQ1 | answered_by | F6 / Table 7 | 若无 F6 则 RQ1 无法统计 |
| [edge-rq-f7] | RQ2 | answered_by | F7 / Table 9--12 | 多技术组合需 multi-label |
| [edge-rq-f8-f9] | RQ3 | answered_by | F8/F9 / Table 13--15 | `NOT SPECIFIED` 是显式类别 |
| [edge-rq4-eval] | RQ4 | answered_by | F10--F12/F14--F18 / Table 16--20 | `not_evaluated`、`quality_measure_not_reported` 要单列 |
| [edge-rq5-result] | RQ5 | answered_by | F13 / Table 21--22 | 异质结果只 summarizing effect estimates |
| [edge-artifact-gap] | F18 + Table 16/17 | supports | replication package discussion gap | 不得从 `no package` 直接推 final reproducibility claim |
| [edge-stats-discussion] | Table 5--22 | supports | Discussion 4.1--4.10 | 每个 finding 需支撑表/段落和反证限制 |
| [edge-validity-limit] | Threats §5 | limits | all statistical / candidate findings | 外推限制必须回链 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 修正主干和叶子父子挂接 | `review.md` 维度树结构，行 196--208 | 把 protocol/corpus 从 mining technique 分支移出，单独设 `检索与纳排协议`；把 method/technique 挂到 RQ2/F7；把 evidence/artifact 挂到 RQ4/F10--F18；把 finding 挂到 RQ5 + Discussion。 | RQ 与 F 字段映射：`paper_content.txt` 行 105--127、227--246。 | I |
| 扩展原文 schema 叶子，不只保留 5 个候选 leaf | `原文模式候选叶子映射` 行 222--232 | 至少拆出 F1--F5、F6、F7、F8、F9、F10--F13、F14--F17、F18、classification construction、reliability、result table/finding path、validity threats。 | Table 3 行 227--269；§2.4 行 283--341；Table 4 行 321--338。 | I |
| 补全三套 classification schema 的取值空间 | 维度树叶子表和候选叶子映射 | F6 写 9 类；F7 写 4 大类及 Table 12 ML subtype；F8 写 14 SE activities + `NOT SPECIFIED`，不要只写 requirements/maintenance/testing/design。 | Table 7 行 440--450；Table 9 行 660--665；Table 13 行 945--1016；PDF p.12/p.26--27。 | I |
| 把 coding/reliability 作为质量节点 | 维度树主干或叶子 | 增加 content analysis、iterative coding、schema source、merge/remove/add category、inter/intra-rater agreement 字段。 | §2.4 行 289--341；Table 4 PDF p.9。 | I |
| 补 evaluation / artifact 字段结构 | `评价与复现资产` 分支 | 拆出 effectiveness evaluation、user study、metrics/criteria、annotated dataset、annotation task、annotators、quality measure、public dataset/tool、replication package、author contact。 | F10--F18 行 247--269；§3.5 行 1245--1284；Table 16--22。 | I |
| 补关系边 | `关系边表` 行 234--239 | 新增 RQ→F、F6/F7/F8→结果表、F10--F18→评价表、artifact→replication gap、result tables→Discussion finding、Threats→外推限制。 | Table 10--11、14--15、21--22；Discussion 行 1693--1848；Threats 行 1849--1884。 | I |
| 补 finding path 明细 | `统计与候选发现链路` 和 A.3 | 把 Discussion 4.1--4.10 拆成候选 finding，并为每条绑定支撑统计表、反证/限制和 claim strength。 | Discussion 行 1693--1848；Conclusion 行 1939--1971。 | I |
| 精确化 A.2 证据账本 | A.2 行 270--274 | 至少新增 Table 3、Table 4、Table 7、Table 9、Table 13、Table 16/17、Table 21/22、§5 Threats、Table 23 的独立证据行；填页码、表号、行号范围、是否视觉核对。 | 本次已抽样视觉核对 PDF p.7/p.9/p.12/p.26--27/p.35--36/p.40/p.43。 | I |
| 删除或改写模板残留的 roadmap/action point/guideline 表述 | A.2 EV-002/EV-003、叶子定义 | 本文没有 roadmap figure；只保留 future research directions / discussion gaps。不要把 roadmap/action point 当原文 schema。 | 原文 §4 Discussion，未发现 roadmap figure；`paper_content.txt` 图表 markers 仅 Fig.1--4。 | I |
| 修正 root 单位对象 | 根问题/RQ 映射表行 192 | 把 `primary study / secondary study` 改为 `primary study / paper / approach / evaluation artifact`；说明 secondary/tertiary 被排除。 | Table 1 行 190--193。 | I |
| 统一统计池表述 | 快速卡片行 24、维度树行 182/245--247 | 快速卡片改为“后续主统计池候选；A1-DT 当前只作 schema_seed，不进入 SUMMARY 定量统计”，避免与 A1-DT 降级纪律冲突。 | SUMMARY 三池规则；`review.md` 行 182、245--247。 | M |
| 给 A.4 `passed` 提供可复验命令或日志 | A.4 行 297 | 若保留 `passed`，补脚本路径、命令和输出摘要；若无本地记录，改为 `not_rerun_in_this_review` 或 `needs_log_link`。 | A.4 当前只有自然语言，未见命令输出。 | M |

## 6. C/I/M 结论

- C：0。没有发现当前 `review.md` 把六个通用 leaf 直接冒充原文完整 schema，也没有把 `not_verified` 证据升级为可统计结论；这避免了最直接破坏 Paper2 证据链的错误。
- I：9。核心问题是维度树过小、主干/叶子挂接错位、原文 F1--F18 / 三套 classification schema / coding reliability / evaluation-artifact / result-to-finding path 没有完整结构化复原。这会实质影响后续 A2a/A2b 的字段精核、统计池准备和候选 finding 审计。
- M：2。主要是快速卡片统计池措辞和 A.4 `passed` 复验证据的清晰度问题。
- 最终建议：NEEDS FIX。当前版本可作为 A1-DT 的粗粒度 seed，但不能作为 `app-reviews-slr-se` 原文维度树复原的完成版；最小修复是保留 6 个通用接口层，同时把原文 schema 层扩展到 RQ→F1--F18→classification/reliability→evaluation/artifact→result/finding/validity 的结构化树和关系边。
