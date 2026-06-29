# re-agile-sms-2015 · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（任务字段：codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`、`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`。本审计采用 claim-evidence-engineering、claim gate、reviewer risk、claims-to-avoid 口径。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`。本审计采用先复原 research question、methodology、evidence、再判断字段结构是否可执行的口径。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本任务只产出单篇审计 artifact，不启动 autoresearch 循环，不使用 sub-subagent。
- 是否完整阅读 `paper_content.txt`：是；完整阅读 `paper_content.txt` 1--954 行，覆盖摘要、引言、背景、methodology、检索与纳排、数据抽取、Results、Tables I--V、Discussion、Limitations、Conclusion、References 和 Primary Sources。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认本地 PDF 为 9 页，并用 `pdftoppm` 临时渲染后视觉核对关键页。已核对 PDF 第 1 页的摘要和 3 个 RQ，第 3 页的 Scopus 检索、纳排、数据抽取和 Table I，第 4 页的 Table II / Table III，第 5 页的 Table IV，第 6 页的 Table V，第 7--8 页的 Discussion、Limitations 和 Conclusion。未做逐字版面转录，未将全部 primary source references 逐条视觉复核。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是对 agile software development 中的 requirements engineering 做 systematic mapping study，理由是已有 agile software development 研究和综述很多，但 RE in ASD 还没有被专门映射，缺少强知识区和知识空白的总体图谱。摘要明确说作者识别并分析了 28 篇相关论文，结果包括 agile RE 定义模糊、收益、问题领域和对应方案。

原文显式给出 3 个 RQ，位于 PDF 第 1 页 / `paper_content.txt` 48--55 行：

| RQ | 原文问题 | 维度含义 |
|---|---|---|
| RQ1 | What has been researched regarding requirements engineering in an agile context? | 研究对象 / 主题语义 / 研究类型 / agile 方法上下文字段。 |
| RQ2 | What are the reported key benefits of agile requirements engineering? | benefit taxonomy，后续 Table IV 的 B1--B6 编码。 |
| RQ3 | What are the reported problems and corresponding solutions related to agile requirements engineering? | problem taxonomy、problem-to-solution relation、absence evidence，后续 Table V 的 P1--P6 与正文 solution paragraphs。 |

原文贡献不是完整效果综合，也不是质量评价型 SLR，而是 mapping：用 28 篇文章复原该主题的研究分布、概念定义、收益、问题、方案和未来研究空白。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文 §III Methodology 明确说明研究是 mapping study。检索使用 Elsevier Scopus abstracts database，2014 年 9 月执行。检索式为 `TITLE-ABS-KEY(("requirements analysis" OR "requirements engineering") AND (agile OR scrum)) AND NOT KEY("agile manufacturing")`。

纳排链条是可统计的分母字段：

| 阶段 | 数量 / 规则 | 证据定位 |
|---|---|---|
| 初始检索 | 241 results | `paper_content.txt` 217--223 行；PDF 第 3 页。 |
| 排除非 journal/conference | 46 篇 | 223--224 行。 |
| 排除非英文 | 8 篇 | 225--226 行。 |
| title/abstract 筛选分母 | 187 篇 | 227--228 行。 |
| title/abstract 排除 | 123 篇，排除标准 5 条 | 229--243 行。 |
| full text 获取 / 筛选分母 | 65 篇 | 243--245 行。 |
| full text 排除 | 37 篇，排除标准 3 条 | 245--255 行。 |
| 最终纳入 | 28 articles | 254--256 行；摘要 13--15 行；Conclusion 727--731 行。 |

数据抽取也有显式 extraction form。原文说从 28 篇文章中抽取 article metadata、context、methods and results；metadata、context 和 methods 被 summarized；results 被归类到 4 个 subject areas：Definition of RE in the agile context、benefits identified in agile RE、problems identified in agile RE、solutions proposed for the aforementioned problems。benefits、problems、solutions further collated, analysed and categorized under thematic areas（`paper_content.txt` 255--264 行，PDF 第 3 页）。

统计呈现是 mapping 风格的描述统计和分类表，不是 effect synthesis。原文至少统计了 publication venue type、agile method context、article type、benefit code、problem theme code，并在 Discussion 中从分布和分类关系形成 finding / gap：

- publication venues：conference proceedings 15、journal articles 8、magazine articles 5；Table I。
- agile method context：Unspecified agile 20、Scrum 7、FDD 1；Table II。
- article type：multiple case study 6、single case study 5、experience report 3、tool evaluation 1、method evaluation 2、method proposal 8、position paper 3；Table III。
- benefits：B1--B6；Table IV。
- problem themes：P1--P6；Table V。
- solution coverage：P1/P2/P5 有方案，P3/P4/P6 明确没有方案或缺乏已报告方案；正文 560--590 行与 682--707 行。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式 schema 不是当前 `review.md` 的六个通用 leaf，而是下列结构：

| 原文结构 | 真实字段 / 取值空间 | 证据定位 |
|---|---|---|
| RQ schema | RQ1 研究了什么；RQ2 key benefits；RQ3 problems and corresponding solutions | PDF 第 1 页；`paper_content.txt` 48--55 行。 |
| Search / screening protocol | Scopus、检索式、时间点、241→187→65→28 数量链、title/abstract 5 条排除标准、full-text 3 条排除标准 | 217--255 行；PDF 第 3 页。 |
| Extraction form | article metadata、context、methods、results；results 四类 subject areas | 255--264 行；PDF 第 3 页。 |
| Publication venue taxonomy | Conference proceedings、Journal、Magazine；具体 venues 与数量 | Table I；289--300 行；PDF 第 3 页。 |
| Agile method context taxonomy | Unspecified agile、Scrum、FDD | Table II；310--318 行；PDF 第 4 页。 |
| Article type taxonomy | Multiple case study、Single case study、Experience report、Tool evaluation、Method evaluation、Method proposal、Position paper | Table III；319--329 行；PDF 第 4 页。 |
| Benefit coding scheme | B1 Lower process overheads、B2 Improved requirements understanding、B3 Reduced overburden、B4 Responsiveness to change、B5 Rapid delivery and validation、B6 Improved customer relationships | Table IV；416--427 行；PDF 第 5 页。 |
| Problem coding scheme | P1 Problems with client/customer representatives、P2 Insufficiency of user story format、P3 Difficulties in prioritization、P4 Growing technical debt、P5 Reliance on tacit requirements knowledge、P6 Imprecise effort estimates | Table V；522--530 行；PDF 第 6 页。 |
| Problem-to-solution relation | P1 / P2 / P5 有对应方案；P3 / P4 / P6 明确 no solutions proposed | 474--507、537--559、571--590、682--707 行。 |
| Agile RE definition synthesis | 作者提出 agile RE 定义，基于 included articles 的综合 | 641--662 行；PDF 第 7 页。 |
| Limitation schema | Scopus 单库限制、关键词限制；无完整 QA rubric | 708--726 行；PDF 第 7--8 页。 |

原文没有 roadmap figure，也没有 formal quality assessment rubric 或 replication package / artifact availability 字段。它有 Limitations，但不等同于 secondary-study quality rubric。对 Paper2 来说，artifact / quality 字段应记录为 `not_reported_by_original_paper` 或 `not_applicable_to_short_sms`，不能臆造。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding path 至少有 5 条：

1. RQ1 / overview 路径：Table I--III 的 venue、context、article type 分布支持 “RE in ASD has not found a comfortable publication home”、“context often unspecified”、“empirical work exists but method proposals remain high” 等 discussion 观察（592--640 行）。
2. Definition 路径：RQ1 背景讨论和 included studies synthesis 支持 “agile RE definition is difficult / no universal definition”，随后作者提出定义（641--662 行）。
3. Benefit 路径：Table IV 的 B1--B6 和 benefit paragraphs 支持 agile RE benefits 与 general agile benefits 相似（404--455、663--671 行）。
4. Problem / solution 路径：Table V 的 P1--P6、正文每个 problem theme 的 solution paragraphs、absence evidence 支持 “solutions concentrate on P1 and P2, additional documentation supports P5, no solutions for P3/P4/P6”（456--590、682--707 行）。
5. Future research 路径：Discussion 和 Conclusion 将未解决 problem themes、弱 evaluation、method proposal 偏多、large/complex contexts 汇总为 research gaps：prioritization、technical debt、tacit requirements knowledge、effort estimation、large organizations、solution empirical evaluation（699--707、727--745 行）。

这些都应进入候选 finding 链路，但只能作为 `schema_seed` / `candidate_finding`。单篇 mapping 的统计观察不能直接升级为 Paper2 目标领域 final research finding。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 大方向正确，但 RQ 复原不足 | `review.md` 将主类型定为 “SMS problem-benefit-solution 树”，辅助类型为 “Agile RE 主题分类树”，这与原文摘要和 RQ2/RQ3 相符。但根节点只写“研究目标 / RQ / 贡献声明”，没有逐条列出 RQ1--RQ3，也没有把 RQ1 的 overview / context / article-type 维度作为主干。原文 RQ 是维度树根部事实源，缺失会影响 A2a 回填。 | I |
| 主干分支是否覆盖原文 schema | 不完整 | 当前主干是范围、语料、主题、方法、证据/候选发现五类通用分支。它覆盖了 SMS 的外壳，但未覆盖原文显式 extraction form：article metadata、context、methods、results；也未覆盖 Table I venue、Table II agile method context、Table III article type、Table IV B1--B6、Table V P1--P6。主干缺少 `RQ1 overview / article landscape` 和 `problem-to-solution relation`。 | I |
| 叶子维度是否足够具体 | 不足 | `review.md` 67 行已正确声明六个 `leaf-*` 是跨论文通用接口，不是原文 schema 全集，因此没有把通用 leaf 直接冒充原文全集。但 “原文模式候选叶子映射” 只有 5 行，并且 `orig-problem`、`orig-benefit`、`orig-solution` 写成概括性自由文本，没有列出 B1--B6 / P1--P6、venue/context/article-type、definition、solution absence 等可执行叶子。 | I |
| 取值空间是否可执行 | 目前不可执行到字段级抽取 | 原文有多个封闭枚举和数值分母：Unspecified agile/Scrum/FDD；7 类 article type；B1--B6；P1--P6；241→187→65→28。当前候选取值空间写“需求变更、沟通、文档、质量、客户参与、规模化等 problem”“效率、反馈、协作、适应性等 benefit”，既不完整也未绑定原文 code，A2a 难以直接判断字段值。 | I |
| 关系边是否缺失 | 缺失关键关系边 | 原文 RQ3 是 “problems and corresponding solutions”，必须有 problem theme → proposed solution / no solution 的关系边。当前 `review.md` 没有关系边表，只在统计链路里泛写 taxonomy/finding。P3/P4/P6 的 “no solutions proposed” 是重要 absence evidence，若缺失会破坏 candidate finding path。 | I |
| 统计用途 / 分母是否正确 | A1-DT 降级正确，但原文内部分母不够 | 当前正确写明 A1-DT 只作 schema seed，不进入 SUMMARY 定量统计，这符合 GUIDE。但是原文内部可统计分母没有复原：241 初始检索、187 title/abstract 筛选、65 full text、28 included、Table I--V 的 N 与百分比都缺少字段级记录。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前写 “definition ambiguity / solution gap”，但没有复原完整链路：Table I--III → publication/context/type finding；Table IV → benefit finding；Table V + solution paragraphs → P1/P2/P5 有方案、P3/P4/P6 无方案；Discussion → large/complex systems、weak evaluation、future research。Paper2 需要 candidate finding ledger，这里证据链过粗。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，证据过泛 | A.1--A.4 表头齐全，A.3 回链 A.2，且 A.2 证据均降为 `not_verified`，没有违规升级为 strong/medium。这是合规的。但 A.2 只有 4 条泛证据，使用“见释义”“邻近段落”“表 / 图待核验”，没有表 I--V、RQ、纳排、extraction form 的独立证据行，不能支撑“完整准确”的维度树复原。 | I |
| 是否存在可能误导 A2a 的强主张 | 没有 C 级误导，但有 I/M 风险 | 优点是 `review.md` 明确说明通用 6 leaf 不是原文叶子全集，并把原文候选叶子降为 `schema_seed` / `not_verified`。风险是快速结论和六类 pattern 小节仍显得比 A.2 证据更肯定，例如 validity 写“未定位完整 threat section”但原文有明确 Limitations；候选叶子写 problem/benefit/solution 却没有 code 枚举，会让 A2a 误以为当前叶子已足够。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足够。建议保留现有“通用接口层”，但必须在其下补一个忠实原文的 “source schema layer”。下面是最小修复骨架。

| 节点 / 叶子 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| `[dim-re-agile-sms-2015-root]` Agile RE mapping study schema | -- | RQ1 research landscape；RQ2 benefits；RQ3 problems and corresponding solutions | 后续主统计池候选；A1-DT 当前只作 `schema_seed` | `not_applicable_to_current_summary_stats` | PDF 第 1 页；`paper_content.txt` 48--55 行。 |
| `[dim-re-agile-sms-2015-rq]` 原文 RQ 层 | root | RQ1 / RQ2 / RQ3 | 可作 RQ pattern seed | `not_reported` 不适用，原文明确报告 | 48--55 行。 |
| `[leaf-re-agile-sms-2015-rq1-landscape]` 研究了什么 | RQ 层 | article metadata、context、methods、results；venue、agile method context、article type、definition discussion | 可统计，分母 28 articles | `not_classified`、`not_reported_by_primary_study` | 255--264 行；Table I--III。 |
| `[leaf-re-agile-sms-2015-rq2-benefit]` key benefits | RQ 层 | B1 Lower process overheads；B2 Improved requirements understanding；B3 Reduced overburden；B4 Responsiveness to change；B5 Rapid delivery and validation；B6 Improved customer relationships | 可统计，分母 28 articles，multi-label | `no_benefit_reported`、`not_reported` | Table IV；416--427 行；404--455 行。 |
| `[leaf-re-agile-sms-2015-rq3-problem]` problem themes | RQ 层 | P1 Customer representatives；P2 User story insufficiency；P3 Prioritization difficulties；P4 Technical debt；P5 Tacit knowledge；P6 Effort estimates | 可统计，分母 28 articles，multi-label | `no_problem_reported`、`not_reported` | Table V；522--530 行；456--590 行。 |
| `[leaf-re-agile-sms-2015-rq3-solution]` corresponding solutions | RQ 层 | requirements engineer role、domain owner/business analyst、ethnography、goal-oriented RE / IT governance、additional documentation、mind-mapping、storytests / ATDD、delivery stories、hierarchical requirements model、aspect-oriented RE、feature-driven security RE、traditional RE transformation、preserve traceability | 可统计，但应绑定 source problem code | `no_solution_proposed`、`solution_not_empirically_evaluated`、`not_reported` | 474--507 行；537--559 行；571--590 行；682--707 行。 |
| `[dim-re-agile-sms-2015-protocol]` 检索与纳排协议 | root | Scopus、September 2014、search string、language / document type / full text / redundancy / topic criteria | 可统计，分母链 241→187→65→28 | `not_accessible_abstract`、`not_accessible_full_text`、`non_research_article`、`out_of_scope`、`predatory_or_no_peer_review`、`redundant_extension` | 217--255 行；PDF 第 3 页。 |
| `[leaf-re-agile-sms-2015-search-source]` 检索源与检索式 | protocol | Elsevier Scopus abstracts database；给定 TITLE-ABS-KEY search string；NOT agile manufacturing | 可作方法字段 | `not_reported` | 217--223 行。 |
| `[leaf-re-agile-sms-2015-screening-counts]` 纳排数量链 | protocol | 241 initial；46 non-journal/conference excluded；8 non-English excluded；187 title/abstract screened；123 excluded；65 full text; 37 excluded；28 included | 可统计，数值字段 | `not_verified` 若未 PDF 页码核对；`not_applicable` 不用 | 223--256 行。 |
| `[leaf-re-agile-sms-2015-exclusion-title-abstract]` title/abstract 排除标准 | protocol | no abstract access；not research article；not SE；not RE/analysis in ASD；predatory / no peer review | 可统计，若原文有排除 reason counts 则补；当前只有 criteria | `criterion_not_applicable` | 229--241 行。 |
| `[leaf-re-agile-sms-2015-exclusion-fulltext]` full-text 排除标准 | protocol | no full text access；extended by later included article；not RE/analysis in ASD | 可统计，若有 counts 则补；当前总数 37 | `criterion_not_applicable` | 245--255 行。 |
| `[dim-re-agile-sms-2015-extraction]` extraction form / coding layer | root | article metadata；context；methods；results；results 四 subject areas | 可作 extraction-form pattern seed | `field_not_reported_in_primary_study`、`text_extraction_missing` | 255--264 行。 |
| `[leaf-re-agile-sms-2015-metadata]` article metadata | extraction | publication venue type、venue name、year、source article IDs | 可统计 | `metadata_missing` | Table I；Conclusion 731--732 行。 |
| `[leaf-re-agile-sms-2015-context]` agile method context | extraction | Unspecified agile、Scrum、FDD | 可统计，分母 28 | `unspecified_agile` 是原文显式类别，不等同抽取失败 | Table II；310--318 行；612--626 行。 |
| `[leaf-re-agile-sms-2015-methods]` article type / method | extraction | multiple case study、single case study、experience report、tool evaluation、method evaluation、method proposal、position paper | 可统计，分母 28 | `method_not_reported` | Table III；319--329 行；627--640 行。 |
| `[leaf-re-agile-sms-2015-definition]` agile RE definition | extraction | free text synthesis；proposed definition paragraph | 不宜频次统计，作 concept / definition seed | `no_universal_definition`、`definition_not_reported` | 641--662 行。 |
| `[dim-re-agile-sms-2015-evidence]` 证据呈现与表格层 | root | Table I--V、正文主题段落、Discussion、Conclusion | 可作 evidence presentation seed | `needs_pdf_check`、`not_verified` | PDF 第 3--8 页；`paper_content.txt` 表格 markers。 |
| `[leaf-re-agile-sms-2015-table-i-venue]` publication venue evidence | evidence | Conference proceedings 15；Journal 8；Magazine 5；venues list | 可统计，分母 28 | `not_verified` 若未 PDF 表格核对 | Table I；289--300 行。 |
| `[leaf-re-agile-sms-2015-table-ii-context]` agile method context evidence | evidence | Unspecified agile 20；Scrum 7；FDD 1 | 可统计，分母 28 | `unspecified_agile` | Table II；310--318 行。 |
| `[leaf-re-agile-sms-2015-table-iii-type]` article type evidence | evidence | 7 类 article type + article IDs + N | 可统计，分母 28 | `not_reported` | Table III；319--329 行。 |
| `[leaf-re-agile-sms-2015-table-iv-benefits]` benefits evidence | evidence | B1--B6 + related articles | 可统计，分母 28，multi-label | `no_benefit_reported` | Table IV；416--427 行。 |
| `[leaf-re-agile-sms-2015-table-v-problems]` problems evidence | evidence | P1--P6 + related articles | 可统计，分母 28，multi-label | `no_problem_reported` | Table V；522--530 行。 |
| `[dim-re-agile-sms-2015-finding-path]` finding / gap 形成层 | root | venue home gap、context underspecification、method proposal/evaluation weakness、definition ambiguity、benefit mirrors agile claims、solution gap、future research topics | 只作 `candidate_finding`，不进入 Paper2 final finding | `candidate_only`、`needs_counterevidence` | Discussion 592--707 行；Conclusion 727--745 行。 |
| `[leaf-re-agile-sms-2015-solution-gap]` problem-to-solution gap | finding-path | P1/P2/P5 have solutions；P3/P4/P6 no solutions proposed；many P1/P2 solutions not empirically evaluated | 可作 candidate finding seed | `no_solution_proposed` 是 absence evidence | 560--590 行；682--707 行。 |
| `[leaf-re-agile-sms-2015-evaluation-gap]` empirical evaluation gap | finding-path | method proposals without empirical evaluation；weak evaluation of proposed methods | 可统计 / candidate finding | `not_empirically_evaluated` | 627--637 行；743--745 行。 |
| `[dim-re-agile-sms-2015-validity]` limitations / validity | root | Scopus-only search；small keyword set；additional DBs / keywords could add peripheral studies | 可作 validity pattern seed | `no_formal_quality_rubric`、`artifact_not_reported` | 708--726 行。 |
| `[leaf-re-agile-sms-2015-quality-rubric]` quality assessment rubric | validity | 原文未报告 formal quality rubric | 不统计，记录 absence evidence | `not_reported_by_original_paper` | 全文未见 QA rubric；Limitations 708--726 行。 |
| `[leaf-re-agile-sms-2015-artifact]` artifact / replication package | validity | 原文未报告 replication package、dataset、script、open artifact | 不统计，记录 absence evidence | `not_reported_by_original_paper` | 全文未见 artifact availability 字段。 |

建议补充关系边表：

| 关系边 | 源节点 | 关系类型 | 目标节点 | 证据来源 | 缺失值语义 |
|---|---|---|---|---|---|
| `[edge-re-agile-sms-2015-rq1-extraction]` | RQ1 | answered_by | metadata / context / methods / definition / overview tables | 48--55、255--264、289--329、592--662 行 | `not_classified` |
| `[edge-re-agile-sms-2015-rq2-benefit]` | RQ2 | answered_by | B1--B6 / Table IV | 404--455、416--427 行 | `no_benefit_reported` |
| `[edge-re-agile-sms-2015-rq3-problem-solution]` | RQ3 | answered_by | P1--P6 + corresponding solutions | 456--590、522--530 行 | `no_solution_proposed` |
| `[edge-re-agile-sms-2015-problem-to-solution]` | P1--P6 | has_solution / lacks_solution | solution categories or absence evidence | 474--507、537--559、571--590、682--707 行 | `no_solution_proposed` |
| `[edge-re-agile-sms-2015-type-to-evaluation-gap]` | article type distribution | supports_candidate | weak evaluation / method proposal gap | Table III；627--637、743--745 行 | `candidate_only` |
| `[edge-re-agile-sms-2015-table-to-discussion]` | Table I--V | supports_candidate | discussion findings and future research recommendations | 592--707、727--745 行 | `needs_researcher_adjudication` |
| `[edge-re-agile-sms-2015-limitation-scope]` | limitations | limits | all candidate findings | 708--726 行 | `limited_search_scope` |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补 3 个显式 RQ | `review.md` “根问题 / RQ 到主干分支映射” | 不要只写“研究目标 / RQ / 贡献声明”；逐条写 RQ1--RQ3，并说明 RQ1 对应 overview/context/type/definition，RQ2 对应 B1--B6，RQ3 对应 P1--P6 与 solution relation。 | `paper_content.txt` 48--55 行；PDF 第 1 页。 | I |
| 补原文 extraction form | `review.md` “原文模式候选叶子映射” | 新增 article metadata、context、methods、results 四个抽取字段；results 再拆 Definition、Benefits、Problems、Solutions 四个 subject areas。 | 255--264 行；PDF 第 3 页。 | I |
| 补检索 / 纳排分母链 | `review.md` “语料与纳排链条” 与 A.2 | 写入 Scopus、检索式、September 2014、241→187→65→28，以及 title/abstract 5 条排除标准和 full-text 3 条排除标准。 | 217--255 行；PDF 第 3 页。 | I |
| 补 Table I--III 的 overview taxonomy | `review.md` “原文模式候选叶子映射” | 新增 venue type、agile method context、article type 三个叶子，列完整枚举、N、分母 28 和 `unspecified_agile` 缺失语义。 | Table I 289--300 行；Table II 310--318 行；Table III 319--329 行；PDF 第 3--4 页。 | I |
| 补 Table IV 的 benefit code 枚举 | `review.md` “原文模式候选叶子映射” | 将 benefit 从自由文本改为 B1--B6 封闭枚举，并保留 related articles 字段、multi-label 统计语义。 | 416--427 行；PDF 第 5 页。 | I |
| 补 Table V 的 problem code 枚举 | `review.md` “原文模式候选叶子映射” | 将 problem 从概括清单改为 P1--P6 封闭枚举，并保留 related articles 字段、multi-label 统计语义。 | 522--530 行；PDF 第 6 页。 | I |
| 补 problem-to-solution 关系边和 absence evidence | `review.md` 新增 “关系边表” | 增加 P1/P2/P5 有方案、P3/P4/P6 无方案的关系边；`no_solution_proposed` 必须作为缺失值语义和 candidate gap 证据。 | 474--507、537--590、682--707 行。 | I |
| 修正 validity / threat pattern | `review.md` §2 六类 pattern 与 A.2 | 当前写“未定位完整 threat section”过粗。应写原文有 §V.D Limitations，覆盖 Scopus-only 和 keyword limitation，但没有完整 QA rubric。 | 708--726 行；PDF 第 7--8 页。 | M |
| 显式记录 quality rubric / artifact absence | `review.md` “评价、证据与复现资产” | 原文没有 formal quality assessment、replication package、dataset/tool artifact 字段；应作为 `not_reported_by_original_paper` 记录，不要空缺，也不要臆造。 | 全文未见相关字段；Limitations 708--726 行。 | I |
| 补 finding path 明细 | `review.md` “统计与候选发现链路” 与 A.3 | 把 venue/context/type/definition/benefit/problem-solution/evaluation gap/future research 分成候选 finding，并为每条绑定 Table I--V 或 Discussion 段落。 | Discussion 592--707 行；Conclusion 727--745 行。 | I |
| 精确化 A.2 证据账本 | `review.md` A.2 | 将当前 4 条泛证据拆成至少 RQ、method protocol、extraction form、Table I、Table II、Table III、Table IV、Table V、Discussion、Limitations、Conclusion 的独立证据行；填页码、表号、行号范围和是否 PDF 视觉核对。 | 本次已视觉核对 PDF 第 1、3、4、5、6、7、8 页；维护时仍应由主 reviewer 写入可复验锚点。 | I |
| 统一统计用途措辞 | `review.md` “统计与候选发现链路” | 保留“后续主统计池候选；A1-DT 当前只 schema_seed”，同时补“原文内部字段可统计但不得进入当前 SUMMARY 定量统计”。 | SUMMARY 三池规则；`review.md` 63、117--121 行。 | M |

## 6. C/I/M 结论

- C：0。当前 `review.md` 已明确通用 6 个 `leaf-*` 是跨论文通用接口，不是原文 schema 全集，并将候选叶子降为 `schema_seed` / `not_verified`。没有发现把 `not_verified` 证据升级为可统计结论或 final research finding 的 C 级错误。
- I：10。核心问题是维度树过小且原文 schema 复原不足：3 个 RQ、Scopus 纳排链、article metadata/context/method/results extraction form、Table I--III overview taxonomy、Table IV B1--B6、Table V P1--P6、problem-to-solution 关系边、absence evidence、finding path、quality/artifact absence 都没有被充分结构化。这会实质影响 Paper2 的维度模式库、A2a 字段精核、统计分母控制和 candidate finding ledger 可靠性。
- M：2。主要是 validity 表述和统计用途措辞需要更精确：原文有 Limitations 但无完整 QA rubric；当前 A1-DT 只作 schema seed，同时原文内部仍有可统计字段。
- 最终建议：NEEDS FIX。
