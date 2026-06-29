# pattern-field-schema.md：脚手架字段模式合同

## 1. 目的

本文件定义 A1 `survey_of_surveys/` 的最小字段合同。它的目标是让后续 A2a / A2b 能把单篇 SLR/SMS/survey/guideline review 汇总为可演化维度模式，而不是只堆自然语言摘要。

## 2. 字段使用边界

- 本 schema 只服务脚手架模式先验，不支撑目标领域发现。
- 字段定义必须可执行：读者应能判断一篇论文是否能填该字段。
- `metadata-only` 条目不能把字段升级为已采纳，只能进入候选或待核验。
- 缺失值必须区分 `原文未报告`、`文本提取缺失`、`尚未阅读`、`不适用`，不得统一写成 `无`。

## 3. 证据等级枚举

| 枚举 | 含义 | 是否可采纳 pattern |
|---|---|---|
| `题摘级` | 只读题名、摘要、元数据 | 否；只能候选。 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文 | 可以作为 A1 dry-run 采纳，但正式数值待 PDF 核对。 |
| `PDF图表级` | 已人工核对关键表格/图形/公式 | 可以支撑图表/数值级 pattern。 |
| `全文不可得` | PDF 未获取或无法合法访问 | 否；只能进入人工下载清单。 |

## 4. 六类 pattern 字段总表

| 字段 ID | 中文字段名 | 英文字段名 | 操作化定义 | 取值空间 | 最低证据要求 | 缺失值语义 | 来源锚点 |
|---|---|---|---|---|---|---|---|
| `rq_pattern` | 研究问题模式 | RQ pattern | 论文如何组织研究问题，例如规模、主题、主体、限制、效果、趋势、实践影响。 | 自由文本 + 受控标签 | 全文文本级 | `原文未报告` / `guideline不适用` / `尚未阅读` | 必须 |
| `dimension_pattern` | 维度模式 | dimension pattern | 论文为抽取、分类或统计设置了哪些字段和类别。 | 字段树 / 表格 / 分类轴 | 全文文本级 | `原文未报告` / `metadata-only` / `不适用` | 必须 |
| `finding_pattern` | 研究发现模式 | finding pattern | 论文如何从统计或抽取结果形成 finding、gap、建议或实践影响。 | 增长、覆盖、质量、缺口、实践影响、方法限制等 | 全文文本级 | `guideline不适用` / `原文未报告` | 必须，guideline 可说明不适用 |
| `evidence_presentation_pattern` | 证据呈现模式 | evidence presentation pattern | 论文用哪些表格、分母、搜索日志、质量表、抽取表或图形支撑结论。 | 搜索分母、筛选流程、质量表、主题表、引用表、报告结构 | 全文文本级 | `文本提取缺失` / `尚未阅读` | 必须 |
| `validity_threat_pattern` | 效度威胁模式 | validity / threat pattern | 论文如何报告搜索偏倚、纳排可靠性、质量评价、protocol 偏离、外推限制等。 | bias、selection、quality、protocol deviation、external validity、publication bias | 全文文本级 | `原文未报告` / `尚未阅读` | 必须 |
| `report_structure_pattern` | 报告结构模式 | report structure pattern | 论文整体章节如何组织，以及 RQ 与结果/讨论如何映射。 | IMRaD、Previous studies + Method + Results、Guideline sections 等 | 全文文本级或目录级 | `文本提取缺失` / `尚未阅读` | 建议必须 |
| `publication_type` | 出版形态 | publication type | 条目正式发表或发布形态；正式出版优先于预印本。 | `期刊` / `会议` / `预印本` / `技术报告` / `工作坊` / `其他` | 题摘级 | `无法判定` | 必须 |
| `venue_short_link` | 期刊/会议/预印本短名链接 | venue short link | 用短名 Markdown 链接记录具体 venue 或预印本平台，例如 `[IST](...)`、`[EASE](...)`、`[arXiv](...)`。 | Markdown 链接或 `--` | 题摘级 | `无稳定入口` | 必须 |
| `ccf_official_category` | CCF 官方大类 | CCF official category | 按 CCF 官方最新国际推荐目录记录 venue 所属大类，不受本地 `ccf_venues/` 建档范围限制。 | CCF 官方大类名或 `--` / `待核验` | 官方目录核验；异常时记录待核验 | `--` / `待核验` | 必须 |
| `ccf_official_rank` | CCF 官方等级 | CCF official rank | 按 CCF 官方最新国际推荐目录记录 A/B/C；非 CCF venue 写 `--`。 | `A` / `B` / `C` / `--` / `待核验` | 官方目录核验；异常时记录待核验 | `--` / `待核验` | 必须 |
| `ccf_verification_status` | CCF 复核状态 | CCF verification status | 说明 CCF 大类/等级是官方人工核验、本地 `ccf_venues` 缓存、官方页面访问异常待复核，还是非 CCF venue。 | `官方已核验` / `本地缓存；官方待复核` / `非CCF` / `待核验` + 自由文本 | 与 CCF 字段同等级 | `--` / `待核验` | 必须 |
| `online_first_date` | 在线优先日期 | online-first date | 当 online-first 日期与正式卷期或 BibTeX 年份不一致时记录在线优先日期。 | ISO 日期或 `--` | 元数据 / PDF 首页 / 出版商页面 | `不适用` / `待核验` | 条件必填 |
| `publication_year_basis` | 年份统计口径 | publication year basis | 说明年度统计采用正式卷期、BibTeX 年份、online-first 还是预印本年份。 | 自由文本 | 元数据 / BibTeX / PDF 首页 | `未说明` | 条件必填 |
| `review_type` | 综述 / 指南类型 | review type | 条目属于 SLR、SMS、tertiary study、guideline、mapping guideline update、MLR、solution proposal、vision/roadmap 等哪类。 | `SLR` / `SMS` / `SLR+SMS` / `systematic mapping` / `tertiary study` / `guideline` / `mapping guideline update` / `multivocal literature review` / `solution proposal` / `vision/roadmap` / `theory/evaluation/roadmap` / `other` | 题摘级 | `尚未阅读` | 必须 |
| `predecessor_relation` | 前序综述关系 | predecessor relation | 是否扩展、复现、更新、整合已有综述或 guideline。 | `none` / `extends` / `updates` / `replicates` / `integrates` / `unknown` | 全文文本级；metadata 可候选 | `原文未报告` / `尚未阅读` | 建议必须 |
| `target_se_subfield` | 目标软件工程子领域 | target SE subfield | 论文面向哪个 SE 子领域或横向方法学主题。 | RE、Testing、MDE、ML4SE / AI4SE、LLM4SE、Empirical SE、EBSE guideline 等 | 题摘级可候选；全文文本级可采纳 | `尚未阅读` / `横向方法学` / `无法判定` | 必须 |
| `challenge_action_pattern` | 挑战与行动建议模式 | challenge / action pattern | 论文是否把统计观察进一步组织成 research challenge、open issue、future direction 或 action recommendation。 | challenge、open issue、future work、practice recommendation、education recommendation、无 | 全文文本级 | `原文未报告` / `guideline不适用` / `尚未阅读` | 建议必须 |
| `taxonomy_axis` | 分类轴模式 | taxonomy axis pattern | SMS / tertiary 是否建立分类轴或分类树，以及分类轴如何支撑后续统计分析。 | topic、method、artifact、context、benefit、problem、solution、evidence type 等 | 全文文本级 | `原文未报告` / `非SMS不适用` / `尚未阅读` | 建议必须 |
| `problem_solution_pattern` | 问题-方案模式 | problem / solution pattern | 论文是否把领域现状组织为 problem、benefit、solution、practice implication 等可复用 finding pattern。 | problem、benefit、solution、implication、limitation、无 | 全文文本级 | `原文未报告` / `不适用` / `尚未阅读` | 候选 |
| `adoption_status` | 采纳状态 | adoption status | 该字段或 pattern 是否进入后续候选模式库。 | `🟢 已采纳` / `🟡 候选` / `⚪ 未采纳` / `⏳ 待核验` | 取决于字段 | `待核验` | 必须 |
| `eligible_for_schema_seed` | 可作 schema seed | eligible for schema seed | 该文是否允许作为后续维度、字段、报告结构或 finding heuristic 的候选来源。 | `true` / `false` | 题摘级可候选；全文文本级可采纳 | `尚未判定` | 必须，尤其 #95 现代锚点 |
| `eligible_for_statistical_synthesis` | 可进统计合成池 | eligible for statistical synthesis | 该文是否允许进入 SLR/SMS/MLR/systematic mapping 等统计合成池。 | `true` / `false` | 全文文本级；必须有系统检索/纳排/数据综合或等价 MLR 证据 | `尚未判定` | 必须，roadmap/proposal/commentary 必须显式 `false` |
| `evidence_role` | 证据角色 | evidence role | 该文在 A1/A2a 中扮演的证据角色。 | `slr_field_schema_pattern` / `systematic_mapping_pattern` / `multivocal_review_dimension_pattern` / `roadmap_boundary_anchor` / `solution_proposal_boundary_anchor` / `theory_roadmap_schema_seed` / `metadata_only_candidate` / 其他受控值 | 题摘级可候选；全文文本级可采纳 | `尚未判定` | 必须 |
| `systematic_evidence_status` | 系统性证据状态 | systematic evidence status | 记录该文是否有系统检索、纳排、质量评价、数据抽取与统计综合。 | `systematic_review` / `systematic_mapping` / `systematic_review_or_mapping` / `multivocal_literature_review` / `non_systematic_or_boundary_anchor` / `metadata_only` | 全文文本级；metadata-only 只能候选 | `尚未阅读` | 必须 |
| `statistical_pool_exclusion_reason` | 统计池排除理由 | statistical pool exclusion reason | 当 `eligible_for_statistical_synthesis=false` 时，说明不可进入统计池的可审计原因。 | 自由文本；建议写 `vision/roadmap`、`solution proposal`、`metadata-only`、`非系统综述`、`全文不可得` 等 | 与排除原因同等级 | `不适用` / `尚未判定` | 条件必填 |


## 4.1 A1-M0--M6 元维度字段合同

A1-M0--M6 是对六类 pattern 的上层组织，用于把 researcher-defined meta-model、维度模式演化、字段证据、统计分析和 finding 裁决串成可审计链条。它不是最终 A3 schema，但 A1 单篇 review 必须按该表报告贡献。

| 层级 | 字段 ID | 中文名 | 操作化定义 | 可采纳条件 | 不可采纳 / 降级条件 |
|---|---|---|---|---|---|
| A1-M0 | `meta_model_intent` | 研究意图与综述元模型 | 主题、RQ、scope、review type、unit of analysis、研究者 gate 如何被定义。 | 全文说明研究目标 / RQ / scope，或 roadmap 明确研究对象。 | 只有标题关键词时仅候选。 |
| A1-M1 | `corpus_screening_protocol` | 语料收集与纳排 | 数据库、检索式、时间范围、venue、去重、筛选、全文状态、排除理由。 | 有方法 / protocol / search / inclusion-exclusion 正文证据。 | roadmap / vision 无系统检索时写不适用。 |
| A1-M2 | `domain_semantic_taxonomy` | 研究对象与主题语义 | SE 子领域、生命周期阶段、研究对象、工件、任务、场景分类。 | 有 taxonomy / classification / mapping table 或 RQ answer。 | 仅叙述背景无分类时仅候选。 |
| A1-M3 | `method_intervention_taxonomy` | 方法 / 技术 / 干预 | 方法类别、工具链、LLM / agent 角色、自动化程度、human-in-the-loop 点。 | 有方法分类、工具/LLM/agent 角色或干预定义。 | 没有方法对象时不适用。 |
| A1-M4 | `evaluation_evidence_artifact` | 评价、证据与复现资产 | metrics、dataset、baseline、artifact、source anchor、replication package、evidence strength。 | 有评价指标、数据、工件链接或 evidence presentation。 | 只写“数据可得”标题但无链接时不得采纳 artifact 字段。 |
| A1-M5 | `analysis_ready_field_model` | 统计分析就绪 | 字段版本、取值空间、缺失值语义、可交叉统计字段、回填状态。 | 有明确统计表、编码方案或可复用字段取值空间。 | 无分母 / 无取值空间时只能候选。 |
| A1-M6 | `finding_adjudication_model` | 研究发现形成与裁决 | candidate finding、支持 / 反证、claim strength、scope、研究者裁决。 | 有 gap / roadmap / recommendation / implication 且可追溯至数据或论证。 | 只有作者观点但无证据链时标为启发式，不进已采纳 finding pattern。 |

新增或回填 A1-M0--M6 字段时，必须在单篇 `review.md` 同时记录：来源锚点、可迁移性、不可迁移点、对 Paper2 的启发和风险。

## 5. 字段变更规则

字段变更必须记录：触发论文、触发原因、变更类型、受影响字段、是否需要回填、回填状态和冻结理由。A1 dry-run 已触发多类核心回修，并把部分 SMS / MLR / roadmap 候选字段留给 A2a 扩展：

1. `review_type`：Kitchenham & Charters 2007 是 guideline，不适合按普通 tertiary study 处理。
2. `predecessor_relation`：da Silva 2011 是 updated tertiary study，需要记录与前序研究的扩展/整合关系。
3. `target_se_subfield`：Bano 2014、Heikkilä 2015、Kotti 2023 表明不同 SE 子领域会产生不同维度模式，必须显式记录。
4. `challenge_action_pattern`：Kotti 2023 显示现代 tertiary study 常把统计观察升级为挑战和行动建议，需要与 Paper2 后续 finding ledger 衔接。
5. `taxonomy_axis` / `problem_solution_pattern`：Heikkilä 2015 暴露 SMS 常见的 taxonomy、problem、solution 结构；A1 先列为候选字段，A2a 用更多 SMS 样本确认取值空间。
6. `publication_type` / `venue_short_link` / `ccf_official_category` / `ccf_official_rank` / `ccf_verification_status`：用户新增要求需要把“来源等级”拆成可审计的出版形态、可点击 venue、CCF 大类、CCF 等级和复核状态；这些字段必须同步到 SUMMARY、候选池和单篇 review。

7. `review_type` 取值空间扩展：#95 十篇现代锚点引入 `SLR+SMS`、`systematic mapping`、`multivocal literature review`、`solution proposal`、`vision/roadmap`、`theory/evaluation/roadmap`。
8. `eligible_for_schema_seed` / `eligible_for_statistical_synthesis` / `evidence_role` / `statistical_pool_exclusion_reason`：#95 显示 roadmap、vision、solution proposal 可以启发 schema，但必须从统计合成池机器可读排除。
9. `online_first_date` / `publication_year_basis`：#95 中 `interactive-llm-systematic-mapping` 暴露 online-first 年份与正式卷期年份不同，必须把年度统计口径显式化。

## 6. 回填规则

1. 新字段加入后，必须检查所有 A1 dry-run 条目是否需要回填。
2. metadata-only 条目只能回填题摘级字段，例如标题、年份、来源、review type 候选。
3. 已读全文文本条目至少回填六类 pattern 中 4 类。
4. 若回填失败，必须在 [../SUMMARY.md](../SUMMARY.md) 的 schema 修订 / 回填日志中记录。

## 7. dry-run 检查清单

- [x] 至少 3 篇全文文本级 dry-run。
- [x] 至少 1 个 metadata-only / manual-download-needed 失败路径。
- [x] 六类 pattern 中至少 4 类被实际填充。
- [x] 至少 1 个“不适用 / 证据不足”降级记录。
- [x] dry-run 暴露 schema 缺口并已回修字段合同。
