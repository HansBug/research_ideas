# kitchenham-2009-slr-tertiary · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`、`references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。本次按 claim-evidence gate、reviewer-risk gate 和“不要把 roadmap / 过程说明升级为完成型证据”的口径审计。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。本次使用其“先完整理解研究问题、方法、实验/评估和风险，再给可执行计划”的口径审计维度树是否足以支撑后续 A2a。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。本次只借用 artifact-gated / validator-gated 完成观，不启动任何 autoresearch loop 或 subagent。
- 是否完整阅读 `paper_content.txt`：是；逐段阅读 962 行，覆盖 title/abstract、Introduction、Method、RQ、Search process、Inclusion/exclusion、Quality assessment、Data collection、Data analysis、Deviations、Results、Discussion、Limitations、Conclusion、Appendix A1--A3 和 References。
- 是否核对 `paper.pdf`：是；用 `pdfinfo` 确认 9 页 PDF，用 `pdftotext -layout` 和 `/tmp/kitchenham-2009-audit/page-2.png` 至 `page-8.png` 目视核对正文页 8--14，重点核对 RQ、Table 1、Table 2、Table 3--5、Table A1--A3 的版面存在和表头结构。未逐格复录所有表值，因此表格数值仍建议 A2a 做精确页码/表号/字段锚定。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文目标是评估 2004 年 EBSE 提出后，系统文献综述作为 EBSE 推荐证据聚合方法在软件工程中的影响。作者明确说本研究是一个 review of SLRs，并因研究对象是 secondary studies 而归类为 tertiary literature review。

显式 RQ 为四个主问题和四个 RQ4 子问题：

- RQ1：2004 年以来有多少 SLR 活动。
- RQ2：这些 SLR 覆盖哪些研究主题。
- RQ3：谁在引领 SLR 研究。
- RQ4：当前研究有什么限制。
- RQ4.1：研究主题是否有限。
- RQ4.2：是否有证据表明 SLR 使用受 primary studies 缺乏限制。
- RQ4.3：SLR 质量是否合适、是否在改进。
- RQ4.4：SLR 是否通过定义实践指南贡献于实践。

这些 RQ 不是装饰性问题；原文后续数据抽取、数据分析和 Discussion 小节逐项映射到 RQ1--RQ4.4。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文方法流程包括：

1. **检索语料构建**：人工检索 10 个期刊和 4 个会议 proceedings，自 2004 年到 2007 年 6 月 30 日；Table 1 给出来源清单，Table A1 给出每个来源按年份的 total / relevant / selected 分母。
2. **补充发现路径**：除检索指定 venue，还直接联系 Travassos，并通过 Jorgensen 网页引用补充 Simula 相关研究。
3. **纳排标准**：纳入 peer-reviewed SLR 与 meta-analysis；排除 informal literature survey、只讨论 EBSE/SLR 程序的论文、重复报告，并保留最完整版本。
4. **质量评价**：使用 DARE 四个 QA 问题 QA1--QA4，并给出 Y/P/N/Unknown 到 1/0.5/0/Unknown 的评分规则；Kitchenham 评估全部论文，其他作者独立评估子集，分歧讨论解决，Unknown 通过邮件询问作者。
5. **数据抽取**：原文 2.5 明确列出 extraction form，包括 source/reference、study type、scope、topic area、authors/institution/country、summary/RQ answers、research question/issue、quality evaluation、是否引用 EBSE/SLR guideline、是否提出 practitioner guidelines、primary-study 数。
6. **数据分析**：原文 2.6 把抽取字段映射到 RQ：年份/source 与 guideline 引用支撑 RQ1；scope/topic 支撑 RQ2 与 RQ4.1；affiliation 支撑 RQ3；primary-study count 支撑 RQ4.2；quality score 支撑 RQ4.3；practitioner-oriented guideline 支撑 RQ4.4。
7. **finding 形成**：原文先用 Table 2、Table 3、Table 4、Table 5、Table A1--A3 给统计观察，再在 4.1--4.5 和 Conclusion 中形成解释性 finding，例如 SLR 数量稳定、topic 覆盖有限、欧洲/Simula 主导、质量改善但不能归因于 guideline、实践指南贡献不足、检索范围限制导致外推边界。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文没有 roadmap figure，也没有复杂理论模型；其 schema 主要由 RQ、extraction form、quality rubric 和 evidence tables 组成。

显式结构包括：

- **RQ schema**：RQ1--RQ4.4。
- **Search source schema**：Table 1 的 source/acronym，Table A1 的 source × year × total/relevant/selected。
- **Inclusion/exclusion coding scheme**：SLR、MA、informal survey、procedure paper、duplicate report；Table A2 给 rejected candidate 的 source、authors、reference、year、title、reason for rejection。
- **Quality rubric**：DARE QA1--QA4，Y/P/N/Unknown 评分规则，Table 3 给每个 study 的 QA1--QA4、total score、initial rater agreement。
- **Study evidence table**：Table 2 给 ID、author、date、topic type、topic area、article type、refs、include practitioner guidelines、num primary studies。
- **Quality trend/statistical tables**：Table 4 按 year 给 number of studies、mean quality score、standard deviation；Table 5 按是否 referenced SLR guidelines 给 number and mean quality score。
- **Affiliation evidence table**：Table A3 给 ID、authors、institution、country。
- **Validity / limitations fields**：manual search restriction、single selector checked by another、single extractor checked by another、possible missing national/topic-specific venues、possible inclusion of weakly systematic studies、data extraction errors、DARE subjectivity。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文 finding 路径是清晰的：

- `search source + selected counts + Table 2 type/scope` → RQ1 activity finding：20 relevant studies，19 SLR + 1 MA，12 technology evaluation + 8 research trends，数量稳定。
- `topic type + topic area + practitioner guideline` → RQ2/RQ4.1 topic/practice finding：cost estimation 占主导，mainstream lifecycle topics 覆盖不足，research trends 多于直接实践技术问题。
- `author/institution/country` → RQ3 leadership finding：European researchers and Simula dominate early SE SLR output。
- `num primary studies` → RQ4.2 primary-study support finding：research trends studies 通常 primary studies 更多，部分 topic 足够支撑详细 RQ，但 topic 数仍有限。
- `QA1--QA4 + total quality score + Table 4/5` → RQ4.3 quality finding：质量整体 fair，随年份上升，和引用 guideline 的差异不显著；primary-study quality assessment 较少是问题。
- `include practitioner guidelines + Discussion` → RQ4.4 practice finding：12 个 technology-question SLR 中只有 4 个提供 practitioner advice，EBSE 对实践影响仍不足。
- `limitations` → scope qualification：结论只适用于 major international SE journals 和 general/empirical SE conferences，且抽取/质量评价存在人工流程和主观性限制。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但单位对象写法混乱 | `review.md` 将根节点归为 tertiary 生态统计树 / 质量评价树，符合原文 tertiary review 目标；但根节点表把单位对象写成 `primary study / secondary study`，没有明确本研究的 primary unit 是被纳入的 SLR/MA secondary studies，primary studies 只是被抽取字段。 | I |
| 主干分支是否覆盖原文 schema | 不完整 | 当前主干是通用 A1-M 接口：scope、corpus、taxonomy、method、evidence/finding。虽然第 68 行声明六个 leaf 不是原文全集，但原文真实 schema 中 RQ1--RQ4.4、Table 1/A1 搜索分母、纳排代码、2.5 extraction form、2.6 RQ-analysis mapping、DARE QA rubric、Table 2/3/4/5/A2/A3 没有成为主干或子分支。 | C |
| 叶子维度是否足够具体 | 不足 | `review.md` 只列出 6 个通用 leaf 和 4 个原文候选叶子。4 个候选叶子把 `tertiary corpus`、`quality criteria`、`topic distribution`、`impact-limit` 粗略覆盖原文，但漏掉 source/reference、type/scope、authors/institution/country、EBSE/guideline reference、practitioner-guideline flag、num primary studies、excluded candidate/reason、year/source search denominator、quality trend、guideline-use comparison 等可执行叶子。 | C |
| 取值空间是否可执行 | 多数不可执行 | 通用 leaf 的取值空间多为“自由文本加 RQ / 贡献声明引用”“完整 SLR/SMS 为数值链条”等泛化描述，原文候选叶子也只是短语级候选，没有列出 QA1--QA4 的 Y/P/N/Unknown、topic type = research trends / technology evaluation、article type = SLR / MA、practitioner guidelines = yes/no、refs = EBSE paper / guideline TR / no 等封闭或半封闭取值。 | C |
| 关系边是否缺失 | 缺失 | 原文最关键关系不是横向复杂图，而是 RQ → extraction field → analysis table → Discussion finding 的映射。当前 `review.md` 没有关系边表，无法审计 Table 2 字段如何服务 RQ1/RQ2/RQ4.1/RQ4.2/RQ4.4，Table 3--5 如何服务 RQ4.3，Table A3 如何服务 RQ3。 | I |
| 统计用途 / 分母是否正确 | 降级纪律正确，但原文分母未复原 | 当前明确 A1-DT 不进入 SUMMARY 定量统计，这是正确的；但维度树本身没有复原原文分母链：2506 total venue articles、33 relevant、19 search-selected、18 unique search studies、+2 peer-reviewed 补充、20 relevant studies、12 technology evaluation、8 research trends、8 guideline references、2 EBSE references、4 practitioner-guideline SLR 等。 | I |
| 候选 finding 路径是否完整 | 不完整 | `review.md` 有“统计观察与候选发现”通用 leaf，但没有把 RQ1--RQ4.4 对应的统计观察、support、scope limit 和 recommendation 拆成 finding path。对 Paper2 来说，这会削弱“统计观察不是 final finding”的教学样本价值。 | I |
| A.1--A.4 证据链是否足够 | 结构存在但证据过泛 | A.1 完整；A.2/A.3 有回链且均降级为 `not_verified` / `weak`，没有弱证据误入统计，这是优点。但 A.2 只有 4 条泛证据，原文页码写“待 A2a 精确页码复核”、原文短引写“见释义”，不足以支撑“已复原原文 schema”；A.4 仍显示 PDF visual check `needs_manual_check`，而本次审计已局部核对但源 review 未记录。 | I |
| 是否存在可能误导 A2a 的强主张 | 有中等风险 | 第 68 行已避免把 6 个 leaf 误称为原文全集；A.2/A.3 也正确降级。但第 64 行和 SUMMARY 仍把本篇概括为“tertiary 生态统计树 / 质量评价树”，若不补细粒度候选叶子，A2a 可能误以为只需精核四个候选叶子，而遗漏 extraction form 和 evidence tables。 | I |

## 4. 建议维度树骨架

当前 review 不足够。建议最小修复不是重写全文摘要，而是在“原文模式候选叶子映射（A1 种子）”中扩展为如下忠实于原文的树，并为每个叶子补 A.2 证据锚点。所有条目在 A1-DT 阶段仍可保持 `schema_seed` / `not_verified`，但必须具体到可执行取值空间。

| 节点 / 叶子 | 父节点 | 定义 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| `[dim-kitchenham-2009-root]` EBSE SLR tertiary review 元模型 | -- | 以 SE SLR/MA secondary studies 为分析单位，评估 EBSE 后 SLR 活动、主题、领导者与限制。 | review of SLRs / tertiary literature review | 是，A2a 精核后 | not_applicable | Abstract；Section 1；Section 2 |
| `[leaf-kitchenham-2009-rq]` RQ 与子 RQ | root | 原文研究问题树。 | RQ1, RQ2, RQ3, RQ4, RQ4.1, RQ4.2, RQ4.3, RQ4.4 | 是，可统计 RQ 类型模式 | not_reported | Section 2.1；PDF p.8 |
| `[leaf-kitchenham-2009-source-frame]` 检索来源框架 | corpus | 被人工检索的期刊/会议来源。 | Table 1 source/acronym；10 journals + 4 conference proceedings | 是 | not_verified | Section 2.2；Table 1；PDF p.8 |
| `[leaf-kitchenham-2009-search-counts]` 搜索分母链 | corpus | 每个 source/year 的 total/relevant/selected。 | 数值表：source × 2004/2005/2006/2007 × total/relevant/selected；总计 2506/33/19 | 是 | not_available / not_verified | Table A1；PDF p.12 |
| `[leaf-kitchenham-2009-supplemental-search]` 补充识别路径 | corpus | 联系 Travassos、查 Jorgensen web page / Simula website 等补充来源。 | direct contact / researcher webpage / Simula website | 局部可统计 | not_reported | Section 2.2, 3.1 |
| `[leaf-kitchenham-2009-inclusion]` 纳入标准 | screening | 被纳入文章条件。 | peer-reviewed SLR; meta-analysis; literature review main/partial element | 可作为筛选字段 | not_reported | Section 2.3 |
| `[leaf-kitchenham-2009-exclusion]` 排除标准与原因 | screening | 排除 informal survey、procedure paper、duplicate report 等。 | informal literature survey; EBSE/SLR procedure paper; duplicate report; not SE topic; literature survey not described | 是 | not_reported | Section 2.3；Table A2；PDF p.13 |
| `[leaf-kitchenham-2009-study-id]` study identity | extraction | 纳入 study 的 ID、author、date、reference/source。 | S1--S20；author/date/source/reference | 是 | not_reported | Table 2；Tables A2/A3 |
| `[leaf-kitchenham-2009-study-type]` article type | extraction | study 类型。 | SLR; MA | 是 | unknown | Section 2.5；Table 2 |
| `[leaf-kitchenham-2009-scope]` topic type / scope | extraction | 研究是 research trends 还是 technology evaluation。 | research trends; technology evaluation | 是 | unknown | Section 2.5；Table 2 |
| `[leaf-kitchenham-2009-topic-area]` topic area | extraction | 被综述的 SE 主题。 | cost estimation; SE experiments; testing methods; CMM; COTS; web research; architecture evaluation; etc. | 是 | unknown | Section 2.5；Table 2；Discussion 4.2 |
| `[leaf-kitchenham-2009-authorship]` author / institution / country | extraction | 谁在做 SLR 研究。 | author name; institution; country | 是 | not_reported | Section 2.5；Table A3；Discussion 4.3 |
| `[leaf-kitchenham-2009-rq-answer-summary]` study summary / RQ answer | extraction | 每篇 SLR 的主问题与答案摘要。 | 自由文本，链接 Appendix 3 / technical report；当前论文正文只部分展示 | 局部可统计，更多为证据锚 | not_available_in_article | Section 2.5；Section 4.2 |
| `[leaf-kitchenham-2009-reference-to-ebse-guideline]` refs field | extraction | study 是否引用 EBSE papers 或 SLR guidelines。 | Guideline TR; EBSE paper; No; combinations | 是 | unknown | Section 2.5；Table 2；Discussion 4.1 |
| `[leaf-kitchenham-2009-practitioner-guideline]` practitioner guideline flag | extraction | study 是否提出 practitioner-oriented guideline。 | Yes; No; note/qualified no | 是 | unknown | Section 2.5；Table 2；Discussion 4.4 |
| `[leaf-kitchenham-2009-primary-study-count]` primary studies count | extraction | 每篇 SLR 使用的 primary study 数。 | integer; ranges for analysis | 是 | not_reported | Section 2.5；Table 2；Discussion 4.4/RQ4.2 |
| `[leaf-kitchenham-2009-quality-rubric]` DARE QA rubric | quality | QA1--QA4 与评分规则。 | QA1--QA4; Y=1; P=0.5; N=0; Unknown; author email re-score | 是 | unknown | Section 2.4；PDF p.9 |
| `[leaf-kitchenham-2009-quality-score-table]` per-study quality score | quality | 每个 study 的 QA1--QA4、total score、initial rater agreement。 | Y/P/N/P*/Y*; numeric total; integer rater agreement | 是 | unknown | Table 3；PDF p.11 |
| `[leaf-kitchenham-2009-quality-trend]` quality trend by year | analysis | 按 publication year 的数量、均值、标准差和 Spearman 相关。 | year; number; mean; SD; Spearman r/p | 是 | not_verified | Table 4；Section 3.3 |
| `[leaf-kitchenham-2009-guideline-comparison]` guideline-use comparison | analysis | 引用 guideline 与未引用 guideline 的平均质量比较。 | referenced vs not referenced; number; mean; ANOVA F/p | 是 | not_verified | Table 5；Section 3.3 |
| `[leaf-kitchenham-2009-protocol-deviation]` protocol deviation | validity | 对原始 protocol 的变更。 | concentration on SLRs; expanded RQ; author queries for unknown QA; clarified RQ-data link | 可作为 threat/process 字段 | not_reported | Section 2.7 |
| `[leaf-kitchenham-2009-study-limitations]` limitations/threats | validity | 本文自身限制。 | manual restricted search; single selector checked; single extractor checked; missed national/topic venues; possible inclusion of weak studies; extraction errors; DARE subjectivity | 可作为 threat taxonomy | not_reported | Section 4.5 |
| `[edge-kitchenham-2009-rq-field]` RQ 到抽取/分析字段映射 | relation | 每个 RQ 如何由字段和表支持。 | RQ1→year/source/refs；RQ2→scope/topic；RQ3→affiliation；RQ4.2→primary-study count；RQ4.3→quality score；RQ4.4→practitioner guideline | 是，关系边 | no_linked_field | Section 2.6 |
| `[edge-kitchenham-2009-stat-finding]` 统计观察到 finding 映射 | relation | 统计表如何支持 discussion / conclusion。 | activity stability; topic limitation; European/Simula leadership; quality improving; guideline no significant effect; practice guideline gap; scope limitation | 候选 finding，不是 final finding | not_verified | Sections 3--5 |

该骨架保留当前 review 的正确降级纪律，但把“原文模式候选叶子”从 4 个粗粒度入口扩展到可执行的 A2a 精核任务清单。它也避免把通用 6 个 leaf 当作原文 schema。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 补全原文 extraction form 叶子 | `review.md` 的“原文模式候选叶子映射（A1 种子）” | 至少补 source/reference、study type、scope、topic area、authors/institution/country、summary/RQ answers、research question/issue、quality evaluation、EBSE/guideline reference、practitioner guideline、primary-study count。 | Section 2.5；`paper_content.txt` 行 243--258；PDF p.9 | C |
| 补全 DARE quality rubric 与质量结果叶子 | 同上，并补 A.2 证据 | 拆出 QA1--QA4、Y/P/N/Unknown scoring、per-study QA table、total score、initial rater agreement、author-email re-score、year trend、guideline-use comparison。 | Section 2.4；Table 3--5；`paper_content.txt` 行 204--242、317--329、393--403、465--503；PDF p.9--11 | C |
| 补 RQ → 字段 → 表 → finding 的关系边 | `维度树复原` 后新增“关系边表” | 建立 RQ1/RQ2/RQ3/RQ4.1--4.4 到 data analysis bullets、Table 2/3/4/5/A1/A3、Discussion 4.1--4.4 的关系边；缺失时用 `no_linked_field`。 | Section 2.6；`paper_content.txt` 行 268--283；Discussion 4.1--4.4 | I |
| 补搜索分母与排除理由字段 | 候选叶子映射、统计链路、A.2 | 把 Table 1、Table A1、Table A2 独立入账，不要只写“语料字段”。需记录 total/relevant/selected 和 rejected candidate reason。 | Table 1；Table A1；Table A2；`paper_content.txt` 行 142--155、589--633、639--667；PDF p.8、p.12--13 | I |
| 修正单位对象表述 | 根问题 / RQ 到主干分支映射 | 将单位对象明确为“纳入的 SE SLR/MA secondary studies；primary studies count 是被抽取属性”，避免把 primary studies 与本 tertiary review 的主样本单位混写。 | Section 2；Table 2 | I |
| 将 A.2 泛定位升级为可复验锚点 | A.2 维度树证据账本 | 当前 4 条证据都写“见释义 / 邻近段落”。最小修复是为 RQ、extraction form、quality rubric、Table 2、Table 3--5、Table A1--A3、limitations 各建证据行，写页码、章节、表号和短引。 | PDF p.8--14；本次已目视核对关键表格存在 | I |
| 保留降级但更新 PDF 核对状态 | A.4 | 源 review 当前写 `needs_manual_check`。若本轮结果被采纳，可记录“已有 reviewer 局部核对；仍需 A2a 逐格精核”。不要把局部视觉核对升级为所有表值已验证。 | 本审计 `pdfinfo`、`pdftotext -layout`、`pdftoppm` 目视核对 | M |
| 避免 “schema 历史观察：无硬缺口” 误导 | 快速结论卡片 | 建议改为“原始六类 pattern 无硬缺口；维度树原文候选叶子仍需细化”，否则与本次审计发现冲突。 | `review.md` 行 23 与维度树候选叶子过粗 | I |

## 6. C/I/M 结论

- C：2 个。第一，原文 extraction form 和 DARE quality rubric 没有被细粒度复原，导致维度树无法作为 A2a 的可执行精核入口。第二，叶子取值空间缺少原文封闭/半封闭枚举和数值字段，后续字段抽取、统计分母和质量分析会失真。
- I：6 个。包括主干覆盖不足、单位对象混写、RQ-to-field-to-finding 关系边缺失、搜索分母/排除理由未独立入账、A.2/A.3 证据泛定位、候选 finding 路径偏粗。这些会实质影响 Paper2 的“维度模式 → 字段证据 → 统计观察 → 候选发现 → 研究者裁决”证据链。
- M：1 个。PDF 核对状态可以补充为“已有 reviewer 局部核对，但仍需 A2a 逐格精核”。
- 最终建议：NEEDS FIX。

当前 `review.md` 的重要优点是已经明确说明六个 leaf 是通用接口层，不是原文 schema 全集，并且把弱证据降级为 `schema_seed` / `not_verified`。但作为全文级学术审计，当前原文候选叶子仍过小，不足以支撑 Paper2 后续 A2a/A2b 的字段证据链和可复现统计审计。
