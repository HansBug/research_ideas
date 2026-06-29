# survey_of_surveys/GUIDE.md：综述之综述脚手架维护规则

## 1. 目标与边界

本目录的目标是建立可维护的综述之综述脚手架，帮助后续 A2a / A2b 从软件工程 SLR/SMS/survey 文献中抽取模式先验。它不追求 A1 阶段数量完备，也不把脚手架样本写成目标领域证据。

所有结论必须回到原文或可靠元数据。若只读题名、摘要或元数据，只能写候选线索，不能写成已核验模式。

## 2. 检索策略

A1 只做种子检索和 dry-run；A2a/A2b 才做大规模闭合。A1 检索记录必须写入 [search/search-log.md](./search/search-log.md)，候选条目写入 [search/candidate-pool.md](./search/candidate-pool.md)。

推荐关键词簇：

1. `software engineering systematic literature review tertiary study`。
2. `software engineering systematic mapping study guidelines`。
3. `software engineering survey systematic review quality assessment`。
4. `evidence based software engineering systematic review guideline`。
5. `SLR SMS software engineering reporting threats validity`。

来源优先级：

1. DOI / 出版商页面 / 官方 PDF。
2. 作者主页或大学技术报告页面。
3. DBLP / ACM / IEEE / ScienceDirect / BCS 等索引。
4. 聚合页只作为发现线索，不能作为已核验事实。

## 3. 筛选标准

纳入必须至少满足一项：

1. 论文自身是 SE SLR / SMS / tertiary study / systematic survey。
2. 论文是 SE SLR/SMS 方法学指南或 guideline。
3. 论文能提供可抽取的 RQ、维度字段、finding、证据呈现、validity threat 或 report structure pattern。

排除或降级：

1. 无法核验题名 / 作者 / 年份 / 来源的条目。
2. 仅普通 narrative survey 且无系统检索或纳排信息。
3. 与 SLR/SMS 方法学无关的自动综述生成工具；这类条目应进入 [../baselines/](../baselines/)。
4. PDF 不可获取但元数据可靠的条目可保留为 `metadata-only`，不得进入已采纳 pattern。

## 4. 证据等级与阅读状态

阅读状态说明“读到哪里”，证据等级说明“能支撑多强的脚手架结论”。二者必须分开记录。

| 阅读状态 | 含义 | 可写边界 |
|---|---|---|
| `未读原文-仅题摘粗筛` | 只读题名、摘要、元数据 | 只能写候选相关性。 |
| `已读全文文本-paper_content核验` | 已读 `paper_content.txt` 的摘要、方法、结果、结论等关键部分 | 可写全文级 pattern，但图表/表格数值需标注待 PDF 核对。 |
| `已回PDF核对图表` | 已人工打开 PDF 核对关键图表、表格、公式或版式 | 可支撑图表级细节。 |
| `全文不可得-待人工下载` | 合法 PDF 未获取 | 只能保留元数据、下载尝试和候选理由。 |

| 证据等级 | 适用条件 | 写作边界 |
|---|---|---|
| `题摘级` | title / abstract / metadata | 不支撑 pattern 采纳。 |
| `全文文本级；图表待人工核对` | 已读 `paper_content.txt` 关键正文 | 支撑 A1 dry-run pattern；正式数字需 PDF 核对。 |
| `PDF图表级` | 已打开 PDF 核对关键图表/表格 | 可支撑图表/数值级 pattern。 |
| `全文不可得` | PDF 未获取或无法合法访问 | 只进入 manual-download / metadata-only。 |

## 4.1 出版形态、Venue 与 CCF 官方字段

后续 [SUMMARY.md](./SUMMARY.md)、[search/candidate-pool.md](./search/candidate-pool.md) 和每篇 `papers/<slug>/review.md` 的快速结论卡片必须显式维护以下来源字段，不能只写泛化的“来源等级”：

| 字段 | 填写规则 |
|---|---|
| `出版形态` | 写 `期刊`、`会议`、`预印本`、`技术报告`、`工作坊` 或其他可审计形态。若同一论文有 arXiv 预印本和正式出版版本，优先按正式出版版本填写，并在备注中说明 arXiv 只作为开放全文来源。 |
| `期刊/会议/预印本` | 写可点击的短名链接，例如 `[IST](https://www.sciencedirect.com/journal/information-and-software-technology)`、`[ESE](https://link.springer.com/journal/10664)`、`[EASE](https://conf.researchr.org/series/ease)`；预印本写 `[arXiv](https://arxiv.org/)`。若不是期刊 / 会议 / 预印本，应写最接近的可审计入口；实在没有稳定入口时写 `--` 并说明原因。 |
| `CCF 官方大类` | 必须从 CCF 官方最新国际推荐目录核验，默认先查 [CCF 推荐国际学术刊物目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/2024-06-28/825349.shtml) 及其各大类页面，例如 [软件工程 / 系统软件 / 程序设计语言](https://www.ccf.org.cn/Academic_Evaluation/TCSE_SS_PDL/)。不得只因为本仓库 [../../../ccf_venues/](../../../ccf_venues/) 未建档就写未知；`ccf_venues/` 只能作为本地缓存和二次跳转入口。非 CCF venue 写 `--`。 |
| `CCF 官方等级` | 写 `A` / `B` / `C` / `--`。只有官方目录明确收录时才写等级；预印本、技术报告、非 CCF workshop / conference / journal 写 `--`。若 CCF 官方页面访问异常或需人工核验，临时写 `待核验` 并在失败记录中说明，不能用第三方镜像升级为官方事实。 |
| `CCF 复核状态` / `ccf_verification_status` | 记录该 CCF 字段是“官方页面已人工核验”“本地缓存；官方待人工复核（WAF）”“非 CCF venue”还是“待核验”。若使用本地缓存，必须说明缓存来源与访问异常类型，不能把缓存口径写成实时官方在线核验。 |
| `online_first_date` / `publication_year_basis` | 当 online-first 日期与正式卷期 / BibTeX 年份不一致时必须写入 `metadata.json`，并在 `review.md` 快速卡片说明统计年份采用哪一个口径。默认正式引用和年度统计采用正式卷期 / BibTeX 年份，online-first 只作为时间背景。 |

执行纪律：

1. CCF 大类和等级的范围必须来自 CCF 官方完整目录视角，不局限于当前 [../../../ccf_venues/](../../../ccf_venues/) 已收录的 42 个 venue。
2. 若一个 venue 属于 CCF 官方目录但本库尚未建档，仍应填写官方大类和等级，并把“本库未建档”作为后续情报库补链线索。
3. 第三方 CCF 镜像、博客、个人主页、学校主页或搜索摘要只能作为发现线索；正式字段必须回到 CCF 官方目录或显式标为 `待核验`。
4. [SUMMARY.md](./SUMMARY.md) 的总表、[search/candidate-pool.md](./search/candidate-pool.md) 的候选表和单篇 `review.md` 的快速结论卡片必须使用同一组字段，避免总账与单篇事实脱节。
5. 从 issue #95 或其他外部候选总表批量引入条目时，必须建立来源审计文件；本轮使用 [search/issue95-selection-audit.md](./search/issue95-selection-audit.md) 记录 Gist 来源、选择理由、PDF 状态、统计池资格和年份/CCF 口径。

## 5. 单篇目录规则

单篇目录最低结构：

```text
papers/<slug>/
├── bibtex.bib
├── metadata.json          # 机器可读事实、证据角色、统计池资格与年份/CCF口径
├── review.md
├── paper.pdf              # 全文可得时必须有
└── paper_content.txt      # 全文可得时必须由 tools/pdf_extractor.py 生成
```

全文可得时，必须使用仓库工具生成文本：

```bash
source venv/bin/activate
python -m tools.pdf_extractor -i papers/<slug>/paper.pdf -o papers/<slug>/paper_content.txt -m text
```

若文字模式提取异常，再记录 OCR 或人工核验需求。不可获取 PDF 不得假装已读全文，必须进入 [search/manual-download-needed.bib](./search/manual-download-needed.bib)。若一轮新增条目全部成功获取 PDF，也必须在 [search/search-log.md](./search/search-log.md) 中记录“无新增人工下载”。

`metadata.json` 是 A1 之后的机器可读事实入口，必须至少包含：`slug`、`title`、`authors`、`year`、`publication_year_basis`、`online_first_date`、`publication_type`、`venue_short_link`、`ccf_official_category`、`ccf_official_rank`、`ccf_verification_status`、`review_type`、`se_subfield`、`current_fulltext_status`、`eligible_for_schema_seed`、`eligible_for_statistical_synthesis`、`evidence_role`、`systematic_evidence_status`、`statistical_pool_exclusion_reason`。若字段不适用，必须显式写 `null`、`--` 或 `待核验`，不能缺键。

## 6. 模式字段抽取规则

每篇 `review.md` 至少抽取六类 pattern：

1. RQ pattern。
2. dimension pattern。
3. finding pattern。
4. evidence presentation pattern。
5. validity / threat pattern。
6. report structure pattern。

每类 pattern 必须有：抽取结论、证据锚点、可迁移性、不可迁移点。若某类不适用，写“不适用”并说明是 `guideline`、`metadata-only`、`目标不符` 还是 `原文未报告`。


## 6.1 A1-M0--M6 元维度抽取规则

A1 之后，单篇 `review.md` 不得只填六类 pattern，还必须说明该论文对 A1-M0--M6 元维度的贡献。A1-M0--M6 是“如何构建 researcher-defined meta-model 与可审计字段证据链”的脚手架层，不是固定 SE 综述字段表。

| 层级 | 中文名 | 操作化问题 | 最低证据要求 | 典型输出 |
|---|---|---|---|---|
| A1-M0 | 研究意图与综述元模型层 | 论文如何定义 topic、RQ、scope、review type、unit of analysis、researcher gate？ | 题摘级可候选，全文文本级可采纳 | 综述元模型对象、RQ 类型、研究者裁决点 |
| A1-M1 | 语料收集与纳排层 | 论文如何定义数据库、检索式、时间范围、venue、去重、筛选、全文状态、排除理由？ | 全文文本级 | 检索 / 纳排字段、PRISMA 或等价分母、失败路径 |
| A1-M2 | 研究对象与主题语义层 | 论文如何划分 SE 子领域、生命周期阶段、研究对象、工件、任务、场景？ | 全文文本级 | 主题 / 对象 taxonomy、scope tree |
| A1-M3 | 方法 / 技术 / 干预层 | 论文如何分类方法、工具链、LLM / agent 角色、自动化程度、human-in-the-loop 点？ | 全文文本级 | method taxonomy、agent role、intervention field |
| A1-M4 | 评价、证据与复现资产层 | 论文如何记录 metrics、dataset、baseline、artifact、source anchor、replication package、evidence strength？ | 全文文本级；artifact 字段需链接核验 | 评价字段、制品资产字段、证据锚点字段 |
| A1-M5 | 统计分析就绪层 | 字段是否有版本、取值空间、缺失值语义、可交叉统计字段、回填状态？ | 全文文本级 | 可统计字段表、分母定义、missing-value semantics |
| A1-M6 | research finding 形成与裁决层 | 论文如何从统计观察形成 candidate finding、support / counter-evidence、claim strength、scope、researcher adjudication？ | 全文文本级 | finding heuristic、claim strength、裁决日志候选 |

执行规则：

1. 每篇 `review.md` 必须有 “A1-M0--M6 元维度贡献”小节；若某层不适用，写明 `不适用` 和理由。
2. A1-M0--M6 只能记录“模式先验 / 候选字段 / 启发式”，不能直接生成目标领域 finding。
3. Roadmap、vision、research commentary 可以贡献 A1-M0、A1-M3、A1-M6 或 report/finding heuristic，但如果没有系统检索和纳排，不得贡献 A1-M1 的已采纳 SLR/SMS pattern。
4. 若某个字段来自题摘级或自动结构统计，只能标为 `候选` 或 `待全文核验`；不得进入已采纳 pattern。
5. 每个可采纳字段必须同时有来源论文、证据锚点、适用条件、不适用条件和缺失值语义。

## 6.2 #95 现代维度锚点全文阅读规则

issue #95 的 10 篇现代锚点必须遵守“一篇一 subagent”原则：每个 subagent 只能读自己负责的 `bibtex.bib`、`metadata.json`、`paper_content.txt` 和必要 PDF，不得混读多篇，也不得开启 sub-subagent。`review.md` 必须显式写明是否已读全文、是否回 PDF 核对图表、是否只做 metadata-only。

新增锚点的 `review.md` 最低结构：快速结论卡片、论文内容详读、六类 pattern、A1-M0--M6 元维度贡献、可迁移字段树 / 维度锚点、对 Paper2 的启发与风险、待复核。快速卡片必须明确“是否已读全文”“是否回 PDF 核对图表”“是否只做 metadata-only”，避免把粗筛结论误写成全文审查结论。



## 6.3 维度树复原规则

本节是 PR-A1-DT 后长期维护 `review.md` 的强制规则。每篇论文不仅要给出六类 pattern 和 A1-M0--M6 贡献，还必须复原其“研究问题 / 贡献声明如何转化为维度树、维度树如何转化为可抽取字段、字段如何支撑统计观察与候选发现”的结构。

### 6.3.1 唯一事实源与旧节迁移

1. 每篇 `papers/<slug>/review.md` 必须包含 `## 维度树复原` 小节，并以该小节作为单篇维度树事实真源。
2. 旧有 `可迁移字段树`、`字段树草案`、`字段树`、`可迁移 roadmap`、`schema 缺口` 等章节必须升级、合并或标注“已迁移至维度树复原”，不得与新小节长期并列为第二事实源。
3. 若旧节与新判断冲突，以原文证据和本 GUIDE 为准，同时在审计附录中记录降级或替代原因。

### 6.3.2 从原文推导维度树的优先级

1. 根节点优先来自显式 RQ、总目标、scope、unit of analysis；roadmap / vision 无 RQ 时来自贡献声明、problem framing 或 roadmap action point。
2. 主干分支优先来自 extraction form、classification schema、coding scheme、taxonomy、roadmap figure、CPTM model、质量评价表或报告结构，而不是 reviewer 主观造词。
3. 叶子维度必须对应可抽取字段、稳定分类项、action point 或可复验的缺失事实；仅凭 reviewer 感觉概括的词只能写作候选节点。
4. RQ / 贡献声明与字段必须显式连接：每个主干分支至少说明服务哪个 RQ、子 RQ、贡献声明或候选发现方向。
5. 统计用途必须说明分母、样本单位、统计池资格和缺失值处理；无分母或证据不足时必须写“不进入主统计池”。
6. 候选发现用途必须与最终 research finding 分开；roadmap / proposal / vision 的 action point 默认只能作为候选启发、边界锚点或风险提示。
7. 节点、叶子与关系边必须有稳定标识：`[dim-{slug}-*]`、`[leaf-{slug}-*]`、`[edge-{slug}-*]`；这些标识必须能从叶子表、关系边表、证据账本和结论映射互相回链。

### 6.3.3 叶子维度必填字段与取值空间

每个叶子维度至少包含：节点或叶子标识、名称、父节点、定义、取值空间、证据要求、缺失值语义、统计用途、候选发现用途、迁移边界和结论引用。

| 取值空间类型 | 使用条件 | 写法要求 |
|---|---|---|
| 完整枚举 | 原文给出封闭类别集合 | 写出所有类别或指向原文表 / 图；缺失值单列说明。 |
| 层级枚举 | 原文给出 taxonomy / 分类树 | 保留父子层级，不压成逗号清单。 |
| 布尔 | 是否存在某制品、字段或特征 | 明确 `true` / `false` / `not_reported` 的判定证据。 |
| 数值或区间 | 计数、年份、比例、评分 | 写分母、范围和单位；图表待核验时不得进入强统计结论。 |
| 关系值 | 字段表示节点间关系 | 使用关系边表，保留关系类型、目标取值空间和缺失关系。 |
| 外部分类法引用 | 原文使用 SWEBOK、CCS、ISO 等外部体系 | 写清外部体系版本或待核验状态。 |
| 自由文本加理由 | 原文本身是开放问题、愿景或叙述性结果 | 说明为什么不能枚举，并默认降级为候选启发。 |
| 待核验或待补全 | 图表 / 附录 / supplementary 尚未核对 | 标为 `not_verified`，不得进入主统计池或 SUMMARY 定量统计。 |

### 6.3.4 关系型维度：主干树加关系边表

DevSecOps CPTM、生命周期投影、工具-实践-指标链接等关系型 schema 不得强行压平成普通树。应使用主干树表达实体层级，再用关系边表表达横向关系。

关系边表至少包含：关系边标识、源节点、关系类型、目标节点、目标取值空间、缺失值语义、证据引用和结论引用。`no linked metric`、`not reported`、`no linked tool` 等缺失关系也要入账，可在 A.2 中使用 `absence_evidence` 或 `not_reported` 证据角色。

### 6.3.5 roadmap / vision / proposal / guideline 降级

1. roadmap、vision、proposal 默认不进入主统计池；只能作为 `boundary_anchor`、`candidate_finding` 或 `risk_only`。
2. guideline 若无统计样本，只作为方法学 seed，不得当作目标领域统计 finding。
3. 这类条目仍必须有维度树和审计附录，但证据强度通常不高于 `medium`；若只靠作者观点或示例，应降级为 `weak`。
4. 降级声明必须写清：非系统检索 / 非统计 finding / 需要研究者裁决 / 不可外推范围。

### 6.3.6 审计附录与结论-证据映射

每篇 `review.md` 文末必须包含以下固定结构，正式表头必须使用纯中文，不得出现 `ID`、`PDF`、snake_case 或中英文对照表头：

```markdown
## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
```

执行纪律：

1. 正文核心判断、维度树一句话结论、树类型、统计池资格、可迁移 / 不可迁移判断、roadmap 降级判断均必须有 `[clm-*]` 引用键。
2. A.3 的“支撑证据标识列表”必须回链 A.2；A.2 的“来源标识”必须回链 A.1。
3. `weak` / `not_verified` 证据不得进入主统计池、SUMMARY 定量归纳或 final research finding。
4. A.2 中“需要原文版面核验”为 `true` 的证据，必须在 A.4 的“复验对象”中列出。
5. 旧结论或旧证据被替代时不得删除键，应标记“已废弃”和“替代证据 / 替代结论”。

### 6.3.7 SUMMARY 回链规则

SUMMARY 的跨论文归纳必须维护 `SUMMARY 结论-证据映射` 表，使用 `[sum-A1DT-*]` 归纳标识，列出分母、纳入 / 排除的单篇结论标识、证据强度过滤、外推限制和允许用途。凡进入 SUMMARY 定量统计的单篇结论，其 A.3 结论强度不得为 `weak` / `unknown`，允许用途必须与统计用途一致。

## 7. schema 回修闭环

`patterns/pattern-field-schema.md` 是 A1 的脚手架字段合同，但不是不可改的先验。dry-run 暴露缺口时必须执行：

1. 在单篇 `review.md` 的“schema 缺口 / 不可迁移点”中记录触发原因。
2. 回修 [patterns/pattern-field-schema.md](./patterns/pattern-field-schema.md) 的字段定义、取值空间、证据要求或缺失值语义。
3. 在 [SUMMARY.md](./SUMMARY.md) 的“schema 修订 / 回填日志”记录时间、触发条目、受影响字段、修订内容、回填状态和冻结理由。
4. 若不回修，必须说明为什么该缺口留给 A2a/A2b。

## 8. SUMMARY.md 回填规则

[SUMMARY.md](./SUMMARY.md) 是长期文库总账，不是 PR 施工记录。后续更新必须优先呈现“当前文库事实、当前规则、当前结论和后续接力入口”，把批次来源、下载失败细节和检索过程主要下沉到 [search/search-log.md](./search/search-log.md)、[search/candidate-pool.md](./search/candidate-pool.md) 或专项审计文件。

[SUMMARY.md](./SUMMARY.md) 必须至少维护：

1. 当前文库状态和总判断：明确当前收录数量、全文状态、manual-download 状态、A1 能支撑什么、不能支撑什么。
2. 核心口径：阅读状态、证据等级、schema seed、主统计池、方法学参考池、schema seed / boundary pool、CCF / venue 字段。
3. 统一论文总表：所有入账论文必须在一个主表中维护，不得按 PR 批次拆成多个主表；本目录显式 override 根级默认排序，主表按年份从高到低排列。
4. 证据池 / 统计池分布：至少区分主统计池、方法学参考池、schema seed / boundary pool、待下载 / metadata-only。
5. A1-M0--M6 元维度定义：解释每层的操作化问题、最低证据和当前主要启发。
6. A1-M0--M6 逐篇覆盖矩阵：每篇论文至少给出 7 个元维度的短语级贡献，并链接到单篇 `review.md`。
7. 当前 pattern 总结与 A2a 接力建议：说明 RQ、dimension、finding、evidence、validity、report structure 的当前观察和下一步处理方式。
8. schema 修订 / 回填日志：只记录会影响后续 A2a/A2b schema、统计池或字段回填的变更；必须包含时间、触发条目、受影响字段、修订内容、回填状态和冻结理由。
9. 当前风险与待复核：只保留影响后续工作的风险，例如图表视觉核对、CCF 官方 WAF、publisher final 差异、统计池误混风险。
10. 更新时间降序日志，时间格式为 `yyyy-mm-dd hh:mm:ss`。

主表建议字段：`状态`、`年份`、`标题`、`出版形态`、`期刊/会议/预印本`、`CCF 大类`、`CCF 等级`、`CCF 复核状态`、`综述类型`、`schema seed`、`主统计池`、`证据角色`、`关键价值`、`详情`。其中 `CCF 复核状态` 是事实口径的一部分，主表复制到 issue / PR / paper 草稿时必须同时保留该列，不能只复制 `A/B/C` 字面等级。

emoji 列只写 emoji；中文释义放在表格外。

### 8.1 三类证据池规则

`eligible_for_statistical_synthesis` 只表示“是否进入主统计池”，不表示论文是否有学术价值。后续维护必须区分以下三类池：

| 池 | 可进入条件 | 当前用途 | 计数规则 |
|---|---|---|---|
| 主统计池 | 论文自身已经执行完成 SLR / SMS / tertiary / MLR / systematic mapping；有系统检索或等价语料构造、纳排 / 编码 / 数据抽取、可统计字段或结果；本地至少全文文本级 | A2a/A2b 统计字段频次、覆盖度、维度饱和度和 finding 支撑 | 以 `eligible_for_statistical_synthesis=true` 为准 |
| 方法学参考池 | guideline、mapping guideline、方法论文；能定义流程、抽取、报告、效度或质量评价规则，但不是普通领域统计样本 | 指导方法设计、schema 设计、证据链设计；不与普通领域统计池混算 | 只计主归属为方法学参考且 `eligible_for_statistical_synthesis=false` 的条目 |
| schema seed / boundary pool | roadmap、vision、solution proposal、theory roadmap、非标准系统综述但有高价值维度或 finding heuristic | 启发维度、方法边界、人机协同和 finding heuristic；不得污染统计池 | 只计主归属为边界 / 启发 seed 且 `eligible_for_statistical_synthesis=false` 的条目 |

三类池在 SUMMARY 的当前数量必须按“主归属”计数，合计应等于入账论文数，避免 Petersen 2015 这类同时有方法学价值和统计样本资格的论文被重复计数。若某论文有次级用途，应在说明文字中标注，不改变主归属计数。

当 `eligible_for_statistical_synthesis=false` 时，`metadata.json` 必须填写 `statistical_pool_exclusion_reason`；若条目仍可作 schema seed，应保留 `eligible_for_schema_seed=true` 并说明其证据角色。

### 8.2 禁止按 PR 批次维护主表

`SUMMARY.md` 的主论文表不得按“初始 dry-run”“#95 十篇”“本轮新增”等来源批次拆分。批次信息可记录在检索日志、候选池、审计文件或更新日志中；长期总账只按文库对象组织。若后续确需展示批次来源，应作为主表中的辅助字段或附录，不得替代统一主表。

## 9. dry-run 验收规则

A1 的 3--5 篇 dry-run 必须满足：

1. 至少覆盖 SLR / SMS / tertiary review / guideline 中的 2 类。
2. 至少 1 篇高等级来源、1 篇非 A 或非顶级来源。
3. 至少 1 篇非 LLM4SE 的 SE 子领域或泛 SE 方法学样本。
4. 六类 pattern 中至少 4 类被全文样本实际填充。
5. 至少 1 个字段展示“不可填 / 不适用 / 证据不足”的降级记录。
6. 若 schema 暴露缺口，必须完成回修或登记留给 A2a/A2b。

## 10. 禁止写法与拒收检查

禁止写法：

- “首次自动化系统综述”。
- “完整覆盖”。
- “替代专家”。
- “PRISMA-compliant”。
- “100+ 篇完整文库完成”。
- “脚手架样本证明目标领域 finding”。

A1 完成前至少运行：

```bash
git diff --check
rg -n "首次自动化|PRISMA-compliant|完整覆盖|替代专家|100\+ 篇完整文库完成" project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys || true
```
