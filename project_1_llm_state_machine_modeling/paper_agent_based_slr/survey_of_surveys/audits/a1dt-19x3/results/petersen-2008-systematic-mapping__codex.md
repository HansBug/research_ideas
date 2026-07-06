# petersen-2008-systematic-mapping · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（对应本轮目标 reviewer 字段：codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取指定 reference：`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。审计口径采用 claim-evidence-engineering、claim gate、reviewer risk 和 claims-to-avoid。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。审计口径采用“先理解 research question / methodology / evidence，再判断实现计划是否可执行”的规划纪律。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本任务是单篇审计交付，不启动 autoresearch 循环，也没有使用 sub-subagent。
- 是否完整阅读 `paper_content.txt`：是；按行完整阅读 `paper_content.txt` 1--536 行，覆盖摘要、引言、§2 mapping process、§3 comparative analysis、§4 guidelines、§5 conclusion 和 references。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认 PDF 为 10 页，并将 p.2--p.9 临时渲染到 `/tmp` 后视觉核对关键页面。已核对 Figure 1 / Table 1（p.2）、Figure 2 / Table 3（p.4）、Figure 3（p.5）、Table 5（p.7）、§4 guidelines 与 conclusion（p.9）。未做逐页逐字版面转录。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文的核心目标不是完成某个 SE 子领域的事实综述，而是定义并说明 software engineering systematic mapping study 的方法、产物和适用边界。摘要明确给出四层声明：background 是 mapping 用来构建 classification scheme 并结构化领域；objective 是描述如何在 SE 中做 systematic mapping 并提供 guidelines，同时比较 systematic maps 与 systematic reviews；method 是定义 mapping process、应用到一个 mapping study，并系统分析已有 systematic reviews；results / conclusion 是给出 process、比较差异，并说明 maps 与 reviews 在 goals、breadth、validity issues、implications 上不同且互补。

Table 1 给出 mapping 型 RQ 的真实 schema 示例，不只是泛化的“研究范围”。OO design map 的 RQ 包含：哪些 journals 包含 software design papers；最常研究的 OO design topics 及其时间变化；最常应用的 research methods 及 study context。Software product line variability map 的 RQ 包含：哪些 variability areas 被覆盖及覆盖文章数；论文类型，特别是 evaluation 与 novelty 类型。这些 RQ 是后续 topic facet、research type facet、forum / trend / coverage 统计的来源。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

Figure 1 给出五步 mapping process：Definition of Research Question / Review Scope、Conduct Search / All Papers、Screening of Papers / Relevant Papers、Keywording using Abstracts / Classification Scheme、Data Extraction and Mapping Process / Systematic Map。

搜索部分区分数据库检索与人工浏览 relevant conference proceedings / journal publications。作者建议搜索串可按 population、intervention、comparison、outcome 结构设计，但 mapping 为保持 breadth，不应过早用特定 outcome 或 experimental design 限制。原文给出两个 search string 示例，并说明 product line variability map 重点使用 SPLC、PFE 和 journal articles。

筛选部分由 RQ 驱动，Table 2 给出 inclusion / exclusion schema。OO design map 包含 books、papers、technical reports、grey literature 中的 empirical OO design studies，并处理同一研究多篇报告 / 一篇报告多个研究的单位问题；SPL variability map 要求 abstract 明确提到 variability / variation 且能推断论文贡献属于 product line variability，排除 SE 域外或只在 abstract 引言句泛提 variability 的论文。

编码与分类部分由 Figure 2 和 §2.4 定义：先读 abstracts 寻找反映 contribution 与 context 的 keywords / concepts；若 abstract 质量不足，可读 introduction 或 conclusion；再聚类关键词形成 categories；文章排序入 classification scheme 时可 update scheme。§2.5 进一步说明 data extraction 用 Excel table 记录分类方案的每个 category，并要求 reviewer 为每篇论文进入某 category 提供 short rationale；抽取过程中可新增、合并或拆分类别。

统计部分以 category frequency 和 facet cross-tab 为核心。原文使用 summary statistics、frequency table 和 bubble plot。Figure 3 是关系型 map：contribution facet、variability context facet 与 research facet 被交叉显示，bubble size 代表对应类别交叉中的 article count。统计观察用于识别哪些 category 被强调，哪些 category / facet combination 薄弱，从而形成 gap 和 future research possibility。

§3 另有一套 comparative analysis schema。作者用 `"systematic review" AND "software engineering"` 在 Inspec & Compendex、IEEExplore、ACM Digital Library 中检索，得到 21 篇；按 SE 域、Kitchenham & Charters 2007 依据、title / abstract 显式 systematic review 等条件筛选为 8 篇，再加入 Kitchenham 2007 中的 2 篇，共 10 篇。Table 5 对这 10 篇 systematic reviews 的 characterization schema 包含 research goals、inclusion requirements、number of included articles、means of analysis。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文显式结构至少包括：

1. Figure 1：systematic mapping process model，五个 process steps 与 outcomes。
2. Table 1：mapping RQ schema 示例，覆盖 publication forum、topic / trend、research method / context、area coverage、paper type、evaluation / novelty。
3. Table 2：inclusion / exclusion criteria schema，并包含单位对象差异，如 paper / study、同一研究多篇报告、同一论文多个研究。
4. Figure 2：classification scheme construction / coding workflow，包含 abstract、keywording、classification scheme、sort article into scheme、update scheme、systematic map。
5. Table 3：Wieringa research type facet，封闭枚举为 Validation Research、Evaluation Research、Solution Proposal、Philosophical Papers、Opinion Papers、Experience Papers，并给出判定描述。
6. Figure 3：bubble plot visualization，至少显式包含 contribution facet（Metric、Tool、Model、Method、Process）、variability context facet（Requirements Variability、Architecture Variability、Implementation Variability、Verification and Validation、Variability Management、Orthogonal Variability）和 research facet（Evaluation Research、Validation Research、Solution Proposal、Philosophical Paper、Experience Report、Opinion Paper）。
7. Table 4：10 篇 systematic reviews 的 reference IDs。
8. Table 5：existing systematic review characterization schema：Research Goals、Inclusion Requirements、Number of Included Articles、Means of Analysis。
9. §4 guideline action points：Use Methods Complementarity、Adaptive Reading Depth For Classification、Classify Papers Based on Evidence and Novelty、Visualize Your Data。

原文没有完整 quality rubric，也没有 replication package / open artifact 字段。相反，§3.2 明确说 maps 不像 systematic reviews 那样评价文章质量，因为目标不是 establishing the state of evidence；validity concern 主要来自 abstract 误导、术语不一致和高层分类带来的 judgmental errors。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding 形成链路有两条。

第一条是 mapping process 内部链路：RQ / scope 决定搜索和纳排；keywording 形成 classification scheme；data extraction 把每篇文章放入 facet/category 并记录 rationale；频数与 bubble plot 展示 category coverage；覆盖薄弱或空白的 facet combination 形成 research gap / future research possibility。这里的 gap 是 coverage gap，不是 effect-size 或 causal finding。

第二条是 map-review comparison 链路：作者用 Table 5 characterization schema 总结 10 篇 SE systematic reviews，再比较 maps 与 reviews 在 goals、process、breadth/depth、topic classification、research approach classification、validity 和 industrial accessibility 上的差异；随后在 §4 给出 guideline extensions。该链路说明 recommendation 不是来自单个频次，而是来自 Table 5 观察、mapping study experience 和方法学讨论的组合。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确，但单位对象写法过泛 | `review.md` 将根节点定为 `Systematic Mapping Studies in Software Engineering`，主类型为“方法流程树”，这与原文匹配。但根节点表把单位对象写成 `roadmap action / guideline item / schema seed`，不够忠实；本文真实单位对象至少包括 SMS process / guideline item、mapping example 中的 primary paper / category assignment、comparative analysis 中的 systematic review row。 | M |
| 主干分支是否覆盖原文 schema | 不完整 | 当前主干为 planning、keywording、classification scheme、map visualization、research gap identification，覆盖 Figure 1 / Figure 2 的一部分。但遗漏或弱化 Table 1 RQ schema、Table 2 inclusion/exclusion schema、Table 5 systematic review characterization schema，以及 §4 guideline action points。对 Paper2 来说，这会让 A2a 低估“方法论文也有多个可抽取 schema”，影响维度模式库的完整性。 | I |
| 叶子维度是否足够具体 | 不足 | 当前“叶子维度表”是 scope/corpus/taxonomy/method/evidence/finding 六个通用接口；`review.md` 第 176 行已说明它不是原文全集，这是正确降级。但“原文模式候选叶子映射”只有 5 行粗粒度候选，未列 Table 3 六类 research type、Figure 3 三个 facet 的实际枚举、Table 5 的 characterization fields、§4 guideline items。 | I |
| 取值空间是否可执行 | 不可执行到 A2a 字段级抽取 | 当前候选叶子多写“目标、RQ、范围、检索策略、纳排和分类准备”“bubble plot、频次表、二维 map”等自由文本集合，没有封闭枚举、层级枚举、数值分母或缺失值规则。A2a 若按此执行，会无法判断一篇后续论文应填 `Validation Research`、`Evaluation Research` 等原文类别，还是只填泛化的“research type”。 | I |
| 关系边是否缺失 | 缺失关键关系边 | 原文 Figure 2 有 `Update Scheme` 反馈到 classification scheme / sorting 的模式演化边；Figure 3 有 contribution facet × variability context facet × research facet 的交叉统计边；§4 有 map first → review focus 的方法互补边。当前 `review.md` 没有关系边表，无法表达“字段值如何交叉形成 gap”。这直接影响 Paper2 对“树 + 关系边”的方法主张。 | I |
| 统计用途 / 分母是否正确 | 主统计池降级正确，但内部统计分母缺失 | 当前明确 Petersen 2008 不进入普通主统计池，仅作 schema_seed，这是正确的；也避免把 not_verified 升级为 statistical_synthesis。但原文内部有 21→8+2=10 的 review comparison 分母、Table 5 的 potentially relevant / included counts、Figure 3 的 facet counts / percentages。当前没有把这些作为“方法学描述性统计 seed”的可复验字段。 | I |
| 候选 finding 路径是否完整 | 不完整 | 当前写出“coverage gap / publication forum gap / map_vs_review_boundary / next_review_recommendation”，但没有复原两条 finding path：一是 category frequency / bubble plot → coverage gap；二是 Table 5 characterization → map-review differences → §4 guideline extensions。缺少 support / counterevidence / claim strength，会削弱 Paper2 的 candidate finding ledger 设计。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，但证据过泛 | A.1--A.4 表头齐全，且 A.3 回链 A.2；这满足结构合同。但 A.2 多处写“见释义”“邻近段落”“表 / 图 / 清单待核验”，证据强度均为 `not_verified`。这符合 A1-DT 降级纪律，却不足以支撑“维度树复原完整准确”。A2a 前必须补页码、表号、图号、行号和短引。 | I |
| 是否存在可能误导 A2a 的强主张 | 未发现 C 级误导，但有轻微表述风险 | 当前 `review.md` 明确说明六个 leaf 是通用接口，不是原文 leaf 全集，并把候选叶子降为 `schema_seed` / `not_verified`，没有把 roadmap / proposal 或 weak evidence 升级为 final finding。风险在于前文快速结论和六类 pattern 小节比 A.2 证据更肯定，后续应让强判断回链到更具体证据。 | M |

## 4. 建议维度树骨架

当前 `review.md` 不足够。建议最小修复不是删除六个通用接口，而是在其下方补一个“原文 schema 复原表 + 关系边表”，将 Petersen 2008 的真实 schema 显式化。

| 节点 / 叶子 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|
| `[dim-petersen-2008-root]` SMS 方法与 map-review 互补方法学 | -- | SMS process、mapping examples、existing SE systematic reviews、guideline extensions | 不进入普通领域主统计池；仅方法学 schema seed | `not_applicable_to_target_domain_stats` | Abstract；§1；§5 |
| `[dim-petersen-2008-process]` mapping process | root | Definition of Research Question / Review Scope；Conduct Search / All Papers；Screening / Relevant Papers；Keywording / Classification Scheme；Data Extraction and Mapping / Systematic Map | 可作流程字段，不作领域统计 | `not_reported` 表示原文未报告某步骤细节 | Figure 1；§2 |
| `[leaf-petersen-2008-rq-goal]` RQ / goal 类型 | process | publication forum；topic coverage；topic trend；research method / study context；area coverage count；paper type；evaluation type；novelty type | 可作 RQ pattern seed | `not_reported`；`not_applicable` | Table 1；§2.1 |
| `[leaf-petersen-2008-search-mode]` 搜索方式 | process | database search；manual proceedings / journal browsing；forum-focused search | 可作方法字段 | `not_reported` | §2.2 |
| `[leaf-petersen-2008-search-source]` 搜索源 | process | scientific databases；Inspec & Compendex；IEEExplore；ACM Digital Library；SPLC；PFE；journal articles | 局部可统计，需区分 mapping example 与 review comparison | `not_reported`；`source_scope_not_applicable` | §2.2；§3 |
| `[leaf-petersen-2008-screening-rule]` 纳排规则 | process | focus area match；empirical study requirement；same-study duplicate handling；same-paper multi-study handling；abstract explicitly contributes；domain outside SE；term only mentioned in intro sentence | 可作 screening schema seed | `not_reported`；`not_applicable` | Table 2；§2.3 |
| `[dim-petersen-2008-keywording]` keywording / coding workflow | process | abstract reading；keyword / concept extraction；context identification；keyword clustering；introduction / conclusion fallback；sort article；update scheme | 可作模式演化字段 | `not_reported`；`not_verified` | Figure 2；§2.4 |
| `[leaf-petersen-2008-category-operation]` 分类方案演化操作 | keywording | add category；merge category；split category；cluster keywords；sort article into scheme；update scheme | 可统计修订类型 | `no_change_reported`；`not_reported` | §2.4--§2.5；Figure 2 |
| `[leaf-petersen-2008-assignment-rationale]` 分类理由 | keywording | free text rationale per paper-category assignment | 不直接统计，作 evidence anchor | `not_reported` | §2.5 |
| `[dim-petersen-2008-map-facets]` mapping classification facets | root | topic / variability context facet；contribution facet；research type facet | 可作为 facet schema seed | `not_applicable` | §2.4；Table 3；Figure 3 |
| `[leaf-petersen-2008-topic-facet]` topic / variability context | map-facets | Requirements Variability；Architecture Variability；Implementation Variability；Verification and Validation；Variability Management；Orthogonal Variability | 可统计，但仅限原文 example | `not_in_example_scope`；`not_reported` | Figure 3；§2.4 |
| `[leaf-petersen-2008-contribution-facet]` contribution type | map-facets | Metric；Tool；Model；Method；Process | 可统计，但仅限原文 example | `not_reported` | Figure 3；§2.4 |
| `[leaf-petersen-2008-research-type-facet]` research type | map-facets | Validation Research；Evaluation Research；Solution Proposal；Philosophical Papers；Opinion Papers；Experience Papers | 可作通用 SE research type seed；A2a 可扩展现代 LLM/agent 类别 | `not_classifiable_from_available_evidence`；`not_reported` | Table 3；Figure 3 |
| `[dim-petersen-2008-map-visualization]` map visualization / statistics | root | summary statistics；frequency table；bubble plot；bar plot；time-varying bubble plot candidate | 可作 evidence presentation seed | `not_reported`；`not_verified` | §2.5；Figure 3；§4 |
| `[leaf-petersen-2008-frequency-count]` category / cross-facet count | map-visualization | integer count + denominator + facet combination | 可统计，必须记录分母与 facet pair / triple | `zero_count` 与 `not_reported` 分开 | §2.5；Figure 3 |
| `[dim-petersen-2008-review-characterization]` existing SE systematic review characterization | root | research goals；inclusion requirements；number of included articles；means of analysis | 可作方法学 evidence table seed；不进入目标领域统计 | `n.a.`；`not_reported` | §3；Table 4；Table 5 |
| `[leaf-petersen-2008-review-goal]` systematic review goal | review-characterization | Identify Best and Typical Practices；Classification and Taxonomy；Emphasis on Topic Categories；Identify Publication Fora | 可统计于 10-review comparison | `not_reported` | Table 5；§3.1 |
| `[leaf-petersen-2008-review-inclusion-requirement]` inclusion requirement | review-characterization | Research is Within Focus Area；Empirical Methods Used | 可统计于 10-review comparison | `not_reported` | Table 5 |
| `[leaf-petersen-2008-review-counts]` included article counts | review-characterization | Potentially Relevant Studies；Relevant Studies Included | 数值字段；分母为 Table 5 的 10 reviews | `n.a.`；`not_reported` | Table 5 |
| `[leaf-petersen-2008-analysis-method]` means of analysis | review-characterization | Meta Study；Comparative Analysis；Thematic Analysis；Narrative Summary | 可统计于 10-review comparison | `not_reported` | Table 5；§3.1 |
| `[dim-petersen-2008-map-review-boundary]` map vs review differences | root | goals；process；breadth/depth；topic classification；research approach classification；validity consideration；industrial accessibility | 候选 finding / boundary anchor | `not_applicable` | §3.2 |
| `[leaf-petersen-2008-quality-boundary]` quality / validity boundary | map-review-boundary | maps do not evaluate quality in detail；reviews evaluate methodology in more detail；classification errors from misleading terms / abstracts；adaptive reading depth mitigation | 不进入统计；作 risk / validity pattern | `not_reported`；`not_applicable` | §3.2；§4 |
| `[dim-petersen-2008-guidelines]` guideline extensions | root | Use Methods Complementarity；Adaptive Reading Depth For Classification；Classify Papers Based on Evidence and Novelty；Visualize Your Data | candidate recommendation seed | `not_reported` | §4 |
| `[leaf-petersen-2008-artifact-field]` artifact / replication package | evidence boundary | 原文未提供 replication package / open artifact 字段；仅提 extraction Excel table | 不统计，记录 absence evidence | `not_reported_by_original_paper` | §2.5；全文未见 artifact availability |

建议补充关系边：

| 关系边 | 源节点 | 关系类型 | 目标节点 | 证据来源 | 缺失值语义 |
|---|---|---|---|---|---|
| `[edge-petersen-2008-rq-to-search]` | RQ / scope | drives | search string / source / screening criteria | §2.1--§2.3；Table 1--2 | `not_reported` |
| `[edge-petersen-2008-keyword-to-category]` | abstracts / keywords | forms | classification categories | §2.4；Figure 2 | `abstract_insufficient` triggers intro/conclusion fallback |
| `[edge-petersen-2008-update-scheme]` | sort article into scheme | updates | classification scheme | Figure 2；§2.5 | `no_update_needed` / `not_reported` |
| `[edge-petersen-2008-category-to-frequency]` | category assignment + rationale | aggregates_to | frequency count | §2.5 | `not_counted` |
| `[edge-petersen-2008-facet-cross]` | contribution facet / topic facet / research facet | crossed_with | bubble plot cell | Figure 3 | `zero_count` distinct from `not_reported` |
| `[edge-petersen-2008-frequency-to-gap]` | frequency / bubble plot | supports_candidate | coverage gap / future research possibility | §2.5；§3.2；§4 | `candidate_only` |
| `[edge-petersen-2008-review-table-to-guideline]` | Table 5 characterization | supports | map-review differences and §4 guidelines | §3.1--§4 | `author_interpretation` |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补原文 schema 复原，不只列五个粗粒度候选叶子 | `review.md` “原文模式候选叶子映射（A1 种子）” | 将 Table 1、Table 2、Table 3、Figure 3、Table 5、§4 guidelines 拆成具体叶子；每个叶子给出取值空间、统计资格、缺失值语义和 evidence source。 | `paper_content.txt` 81--100、129--158、179--218、219--261、283--345、423--467；PDF p.2 / p.4 / p.5 / p.7 / p.9 | I |
| 补 Table 5 comparative analysis schema | `review.md` “维度树结构”与“叶子维度表” | 新增 `existing systematic review characterization` 主干，叶子包括 research goals、inclusion requirements、potentially relevant / included counts、means of analysis。 | `paper_content.txt` 266--345；PDF p.6--p.7 Table 4--5 | I |
| 补关系边表 | `review.md` “维度树复原”中叶子表之后 | 新增 RQ→search/screening、keywording→classification、sort article→update scheme、facet cross→bubble plot、frequency→gap、Table 5→guidelines 等关系边。 | Figure 1--3；§2.1--§2.5；§3.1--§4 | I |
| 细化取值空间与分母 | `review.md` “叶子维度表”“统计与候选发现链路” | 对 Table 3 六类 research type、Figure 3 contribution / context / research facets、Table 5 的 10-review comparison 分母、21→8+2 纳排链条给出可执行取值。 | `paper_content.txt` 187--205、246--261、269--275、327--344 | I |
| 修正根节点单位对象 | `review.md` “根问题 / RQ 到主干分支映射” | 将 `roadmap action / guideline item / schema seed` 改为更忠实的单位对象组合：SMS process step、mapping example 中的 paper/category assignment、comparative analysis 中的 systematic review row、guideline extension。 | Abstract；Figure 1；§2.5；Table 5；§4 | M |
| 显式记录 quality / validity / artifact absence | `review.md` “叶子维度表”与 A.2 / A.3 | 写清本文没有完整 quality rubric、没有 replication package / open artifact 字段；maps 不做与 SR 同等深度的质量评价，这应作为 absence evidence 和迁移边界，而不是空缺。 | `paper_content.txt` 361--414；全文未见 artifact availability 字段 | I |
| 将 A.2 泛定位证据拆为精确证据行 | `review.md` A.2 | 以 Table/Figure/section 为单位新增证据行，至少覆盖 Figure 1、Table 1、Table 2、Figure 2、Table 3、Figure 3、Table 5、§4 guideline paragraphs；减少“见释义”“邻近段落”。 | 本次已视觉核对关键 PDF 页面；维护时仍应由主 reviewer 复验并写入页码 / 表号 / 图号 | I |
| 更新 PDF 核对状态 | `review.md` 快速卡片与 A.4 | 当前写“未做图表视觉级人工核对 / needs_manual_check”。若采纳本审计，可把 Figure 1/2/3、Table 1/3/5 标为已关键图表核对，同时保留 Table 2 和全部数值的 A2a 精核任务。 | `pdfinfo` 10 页；临时渲染核对 p.2 / p.4 / p.5 / p.7 / p.9 | M |
| 弱化前文比 A.2 更强的自然语言结论 | `review.md` §2--§4 快速总结和六类 pattern | 在每个强启发后补证据锚点或降级语句，避免前文“高度一致”“直接支持”等措辞被误读成已完成图表级证据。 | `review.md` 31--79、83--90、94--102；A.2 目前均为 `not_verified` | M |

## 6. C/I/M 结论

- C：未发现 C 级问题。当前 `review.md` 已明确六个 `leaf-*` 是跨论文通用接口，不是原文 schema 全集；A.2 / A.3 也把证据降为 `not_verified` / `weak`，没有把 Petersen 2008 写成普通领域统计池证据或 final research finding。
- I：存在多项 I 级问题。最主要的是原文 schema 复原过粗：Table 1 RQ schema、Table 2 纳排 schema、Table 3 research type facet、Figure 3 三 facet 交叉、Table 5 comparative evidence table、§4 guideline action points 没有被转成可执行叶子和关系边。这会实质影响 Paper2 的维度模式库、A2a 字段抽取、统计分母控制和 candidate finding ledger 可靠性。
- M：根节点单位对象和前文自然语言强度需要清理；PDF 关键图表核对状态可根据本审计复验后更新；局部措辞应避免比 A.2 `not_verified` 证据更强。
- 最终建议：NEEDS FIX。
