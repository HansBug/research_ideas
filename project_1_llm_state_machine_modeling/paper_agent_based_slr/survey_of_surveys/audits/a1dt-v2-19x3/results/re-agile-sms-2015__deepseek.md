现在我已完整阅读所有必需材料。下面开始撰写完整的审计报告。

---

# A1-DT v2 单篇全文审计报告：`re-agile-sms-2015`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `re-agile-sms-2015` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。全文 954 行，覆盖全部 9 页（Page 1–9），包括 Abstract、Background、Methodology（III）、Results（IV）、Discussion（V）、Conclusion（VI）、References、Primary Sources。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib` 含标准 BibTeX entry（Heikkilä et al., SEAA 2015）；`metadata.json` 含 slug、DOI、authors、year、venue、review_type=SMS 等完整元数据。 |
| 是否打开或核对 `paper.pdf` | 是。通过 `pdf2image` 将 9 页 PDF 转为 PNG，但因当前环境不支持图片内联查看，版面核对（表格精确数值、页码对应）标记为 `needs_manual_check`。已对比 `paper_content.txt` 与 PDF 文本抽取结果，内容一致。 |
| 原文类型 | SMS（systematic mapping study）。作者自述 method 为 "mapping study [18]"（[18] = Kitchenham & Charters, 2007），符合 Petersen et al. 的 SMS 方法论。 |
| 被编码样本单位 | primary study（研究文章）。纳入 28 篇 peer-reviewed 文章，对每篇文章进行元数据提取 + 主题分类 + benefit/problem/solution 编码。 |
| 样本数量 / 分母 | **28** / 初始搜索 241 → 去除非 English/非 article 54 → 标题摘要筛选 187 → 全文筛选 65 → 最终纳入 28。 |
| 原生树类型 | **维度森林（dimension forest）**。论文对同一组 28 个样本沿多个独立分类轴进行编码：出版属性轴、研究方法轴、敏捷方法上下轴、RE 主题分类轴、收益轴（B1–B6）、问题轴（P1–P6）、方案轴（与问题多对多映射）。各轴之间非树形 strict hierarchy，而是平行分类 + 交叉统计。 |
| 主统计池资格 | **是**。SMS 有系统检索策略（Scopus）、显式纳排标准、结构化数据抽取表单、主题编码方案、统计分布报告（N=28 的频次和百分比）。可进入统计池，但需注意样本小（28）、单数据库（Scopus）、无质量评价（no quality appraisal），不宜做效应量合成。 |
| 总体判定 | **pass** — 材料完整，原文维度森林可用 `paper_content.txt` 充分复原；需返修现有 `review.md`（详见 §7）；PDF 版面精核仍为人工待办。 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取范围

- **全文文本**：`paper_content.txt`（954 行，9 页），逐节通读 Abstract、Section I–VI、References [1]–[26]、Primary Sources [S1]–[S28]。
- **BibTeX**：确认 4 位作者、SEAA 2015 会议、DOI `10.1109/SEAA.2015.70`。
- **Metadata JSON**：确认 `review_type: "SMS"`、`se_subfield: "Agile Requirements Engineering"`、`eligible_for_statistical_synthesis: true`。
- **PDF 版面核验**：通过 `pdf2image` 转换 9 页为 PNG，但因环境限制未完成逐表视觉对照。对 Table I–V 的解读基于 `paper_content.txt` 的文本提取，已交叉验证 OCR 质量良好（表格边界清晰，数字可对齐）。**所有表格级精确引用仍需人工 PDF 版面最终核验**。

### 1.2 关键原文证据锚点（10 个）

| # | 锚点 | 原文章节 / 表 | 短引 / 释义 |
|---|---|---|---|
| E1 | 样本定义：28 articles | Abstract、III Methodology | "28 articles on the topic were identified and analyzed" |
| E2 | 检索策略 | III Methodology, Page 3 | Scopus, TITLE-ABS-KEY("requirements analysis" OR "requirements engineering") AND (agile OR scrum)), Sep 2014, 241→28 |
| E3 | RQ 结构 | I Introduction, Page 1 | RQ1: What has been researched; RQ2: Key benefits; RQ3: Problems and solutions |
| E4 | 提取表单字段 | III Methodology, Page 3 | "article metadata, context, methods and results were extracted" → 4 主题区: definition, benefits, problems, solutions |
| E5 | Table I: 出版 venue 分布 | IV.A, Page 3–4 | Conference 15 (≈53%), Journal 8 (≈29%), Magazine 5 (≈18%) |
| E6 | Table II: Agile method 上下文 | IV.A, Page 4 | Unspecified agile 20 (≈71%), Scrum 7 (25%), FDD 1 (≈4%) |
| E7 | Table III: 文章类型分类 | IV.A, Page 4 | Method proposal 8 (≈28%), Multiple case study 6 (≈21%), Single case study 5 (≈18%)... |
| E8 | Table IV: Benefits 编码 | IV.C, Page 5 | B1–B6: Lower process overheads, Improved requirements understanding, Reduced overallocation, Responsiveness to change, Rapid delivery & validation, Improved customer relationships |
| E9 | Table V: Problem themes 编码 | IV.D, Page 5–6 | P1–P6: Client/customer reps, User story insufficiency, Prioritization difficulties, Growing technical debt, Tacit knowledge reliance, Imprecise effort estimates |
| E10 | Discussion 中的 gap 识别 | V Discussion, Page 6–8 | P3–P6 have no proposed solutions in the articles; P1/P2 solutions lack empirical evaluation |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**每篇 primary study（研究文章）** 是基础编码单元。作者对每篇纳入文章提取：bibliographic metadata、研究上下文（agile method）、方法类型、RE 主题、以及定性提取的 benefits / problems / solutions 陈述。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有，完整且可审计**：

- **检索**：Scopus 数据库，显式 search string，执行日期 Sep 2014。
- **纳排**：两级筛选——标题摘要级（5 条 exclusion criteria，排除 123/187）→ 全文级（3 条 exclusion criteria，排除 37/65）→ 最终 28。
- **数据抽取**：从每篇文章提取 "article metadata, context, methods and results"，按 4 个 subject area 分类：definition、benefits、problems、solutions。
- **编码方案**：benefits 归纳为 6 个主题（B1–B6），problems 归纳为 6 个主题（P1–P6），solutions 按 problem 分别编码并交叉引用文章。RE 主题分类基于传统 RE process（elicitation、analysis、specification、validation、prioritization、management）。

### 2.3 原文字段来自哪里？

| 字段来源 | 原文对应 | 说明 |
|---|---|---|
| 数据抽取表单（extraction form） | III Methodology: "article metadata, context, methods and results were extracted" | 隐式表单，未以附录形式提供 |
| 分类方案（classification schema） | III Methodology + IV Results: RE topics 基于 Section II 的传统 RE process 定义 | RE 主题为预设分类轴 |
| 主题归纳（thematic analysis） | IV.C–IV.D: "benefits...were collated, analysed and categorized under thematic areas identified in the analysis" | Benefits/Problems/Solutions 为归纳编码 |
| 统计表（Table I–V） | IV Results: 频次分布，以 N 和百分比呈现 | 交叉统计表 |

### 2.4 RQ 与样本单位是什么关系？

- RQ1（"What has been researched"）驱动**描述性分类**：RE topics、研究类型、出版属性 → 这些是树的**分类轴**。
- RQ2（"Key benefits"）驱动**benefit taxonomy**：B1–B6 → 一个独立维度轴。
- RQ3（"Problems and solutions"）驱动**problem-solution mapping**：P1–P6 + 对应 solutions → 两个关联维度轴。
- RQ 是树的**根意图 / 组织原则**，而非树的根节点；根节点始终是 primary study。

### 2.5 降级判断

**不需要降级**。本文具备 SMS 的全部要素：系统检索、显式纳排、结构化抽取、主题编码、频次统计。但以下需标注：
- 质量评价缺失（SMS 可接受，但不适合进入 effect synthesis）
- 单数据库（Scopus only）
- 样本小（28），统计仅能支撑描述性观察，不能支撑推断性结论

---

## 3. 原生样本编码维度树 / 维度森林

### 3.1 判定：维度森林（Dimension Forest）

本文对同一组 28 个样本沿 **7 个平行分类轴** 进行编码，各轴之间非严格层级关系，而是平行交叉：

```
Primary Study (Article) — N=28
│
├── [Axis 1] 出版属性轴 (Bibliographic)
│   ├── Publication year (2004–2014)                   [数值区间]
│   ├── Venue type (Conference | Journal | Magazine)   [完整枚举: 3]
│   └── Specific venue name                            [自由文本 + 外部分类法引用]
│
├── [Axis 2] 研究方法轴 (Research Approach)
│   └── Article type                                    [完整枚举: 7]
│       ├── Method proposal (N=8)
│       ├── Multiple case study (N=6)
│       ├── Single case study (N=5)
│       ├── Experience report (N=3)
│       ├── Position paper (N=3)
│       ├── Method evaluation (N=2)
│       └── Tool evaluation (N=1)
│
├── [Axis 3] 敏捷方法上下文轴 (Agile Method Context)
│   └── Agile method                                    [完整枚举: 3]
│       ├── Unspecified agile (N=20)
│       ├── Scrum (N=7)
│       └── FDD (N=1)
│
├── [Axis 4] RE 主题分类轴 (RE Topic Classification)
│   └── RE topic                                        [层级枚举: 预设 + 涌现]
│       ├── Requirements Elicitation
│       ├── Requirements Analysis
│       ├── Requirements Specification
│       ├── Requirements Validation
│       ├── Requirements Prioritization
│       └── Requirements Management
│       └── (其他涌现主题, from data)
│
├── [Axis 5] 收益分类轴 (Benefits Taxonomy)
│   └── Benefit category                                [完整枚举: 6]
│       ├── B1: Lower process overheads
│       ├── B2: Improved requirements understanding
│       ├── B3: Reduced overallocation
│       ├── B4: Responsiveness to change
│       ├── B5: Rapid delivery and validation
│       └── B6: Improved customer relationships
│
├── [Axis 6] 问题分类轴 (Problems Taxonomy)
│   └── Problem theme                                   [完整枚举: 6]
│       ├── P1: Problems with client or customer representatives
│       ├── P2: Insufficiency of the user story format
│       ├── P3: Difficulties in the prioritization of requirements
│       ├── P4: Growing technical debt
│       ├── P5: Reliance on tacit requirements knowledge
│       └── P6: Imprecise effort estimates
│
└── [Axis 7] 方案分类轴 (Solutions Taxonomy)
    └── Solution (per problem)                          [自由文本 + 关系值]
        ├── For P1: requirements engineer role, domain owner, ethnography, ...
        ├── For P2: delivery stories, hierarchical req model, aspect-oriented, ...
        ├── For P3: NO solutions reported
        ├── For P4: NO solutions reported
        ├── For P5: additional requirements documentation
        └── For P6: NO solutions reported
```

### 3.2 缺失部分说明

- **数据抽取表单原文未附录化**：作者提到 "The metadata, context and methods were summarized. The extracted results were categorized under the following four subject areas"，但精确的 extraction form 字段名、是否每个字段对每篇文章都有值、缺失值处理策略，均未以附录或 replication package 形式提供。此为 **A2a 精核任务**——需联系作者或从 Table I–V 反推。
- **RE 主题轴（Axis 4）在 Table I 中有映射但未单独列表**：Table I 的 "Topic in RE" 列对 28 篇文章逐一标注，但 `paper_content.txt` 中该列的精确内容被表格格式打断，需 PDF 版面核验才能完整复原每一行的 RE 主题赋值。此为 **A2a 精核任务**。
- **Solutions 轴未做独立频次统计**：仅按 problem 分组列出文章引用，未像 Table IV/Table V 那样对 solution 做独立 N-count。可能因 solution 粒度细、难以做互斥分类。此为该轴的局限。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `pub-year` | 出版年份 | Axis 1 出版属性 | III Methodology: article metadata | 文章发表年份 | 2004–2014（整数） | 数值区间 | 未报告（隐含全部已知） | 描述时间分布（Fig 1） | 判断研究热度趋势 | E1, Table I | 年份区间因主题而异 |
| `venue-type` | 出版 venue 类型 | Axis 1 出版属性 | IV.A Results: "Conference proceedings were the most prominent venue" | 出版 venue 的大类 | {Conference proceedings, Journal, Magazine} | 完整枚举: 3 | 未报告 | 描述 venue 分布 | gap: "no primary venue for RE in ASD" | E5, Table I | venue 分类体系需按目标领域重建 |
| `article-type` | 文章研究类型 | Axis 2 研究方法 | IV.A Results: Table III | 文章采用的研究方法 | {Method proposal, Multiple case study, Single case study, Experience report, Tool evaluation, Method evaluation, Position paper} | 完整枚举: 7 | 未报告 | 描述方法分布 | gap: method proposals lack empirical evaluation | E7, Table III | 分类体系是 SE-specific |
| `agile-method` | 敏捷方法上下文 | Axis 3 敏捷方法 | IV.A Results: Table II | 文章讨论的敏捷方法 | {Unspecified agile, Scrum, FDD} | 完整枚举: 3 | 未报告（Unspecified 占 71%，可能含隐式 Scrum/XP） | 描述方法上下文分布 | gap: 71% 不指定具体方法，影响可推广性 | E6, Table II | 敏捷方法名因生态系统而异 |
| `re-topic` | RE 主题分类 | Axis 4 RE 主题 | III Methodology: 基于 Section II 的传统 RE process | 文章涉及的 RE 子活动 | {Elicitation, Analysis, Specification, Validation, Prioritization, Management} + emergent | 层级枚举：预设 + 涌现 | 未报告；需 PDF 核对 Table I 的 "Topic in RE" 列 | 交叉统计 RE 主题与研究类型/方法 | mapping 知识覆盖与空白 | E4, Table I | RE 主题分类体系可迁移至其他 RE-related SLR |
| `benefit-code` | 收益类别 | Axis 5 收益分类 | IV.C Results: Table IV | 文章声称的 agile RE 收益 | {B1, B2, B3, B4, B5, B6}（见上文定义） | 完整枚举: 6 | 未报告；文章可关联 0 个或多个 benefit | 频次统计：每 benefit 的文章支持数 | gap: benefits 缺乏实证验证，多为声称 | E8, Table IV | benefit 内容不可迁移，分类方法可迁移 |
| `problem-code` | 问题主题 | Axis 6 问题分类 | IV.D Results: Table V | 文章报告的 agile RE 问题 | {P1, P2, P3, P4, P5, P6}（见上文定义） | 完整枚举: 6 | 未报告；文章可关联 0 个或多个 problem | 频次统计：每 problem 的文章支持数 | gap: P3–P6 无解决方案 | E9, Table V | problem 内容不可迁移，分类方法可迁移 |
| `solution-text` | 方案描述 | Axis 7 方案分类 | IV.D Results: 按 P1–P6 分组的文本 | 针对特定 problem 提出的解决方案 | 自由文本，按 problem 组织 | 自由文本 + 关系值 | 显式记录：P3/P4/P6 "No solutions were proposed" | 描述 solution 覆盖与 gap | gap: 多数方案缺乏实证评估 | IV.D, Page 5–6 | solution 内容不可迁移，gap 识别模式可迁移 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `article-has-benefit` | primary study | many-to-many | benefit-code (B1–B6) | {B1, B2, B3, B4, B5, B6} | 文章可无 benefit 报告；Table IV 只列有关联的文章 | Table IV: "Benefits from Agile RE and Related Articles" | 描述哪些文章支持哪些 benefit |
| `article-has-problem` | primary study | many-to-many | problem-code (P1–P6) | {P1, P2, P3, P4, P5, P6} | 文章可无 problem 报告；Table V 只列有关联的文章 | Table V: "Problem Themes and Related Articles" | 描述哪些文章报告哪些 problem |
| `article-proposes-solution` | primary study | many-to-many | solution-text (per problem) | 自由文本 + 按 problem 分组 | 显式：P3/P4/P6 无文章提出 solution | IV.D: "The following solutions were proposed..." vs "No solutions to P3 were proposed" | 描述 solution 的覆盖与 gap |
| `problem-addressed-by-solution` | problem-code | many-to-many（通过 article 间接） | solution-text | 自由文本 | P3/P4/P6 无 solution 边 | IV.D 按 problem 分组组织 solution | 映射 problem–solution 空间 |
| `article-has-context` | primary study | one-to-one（或 one-to-many，若涉及多方法） | agile-method | {Unspecified agile, Scrum, FDD} | 71% 为 Unspecified；作者推测隐含 Scrum/XP | Table II: "Summary of Agile Methods Discussed in Articles" | 按敏捷方法上下文切片结果 |
| `article-has-type` | primary study | one-to-one | article-type | {Method proposal, Multiple case study, ...} | 未报告缺失 | Table III: "Summary of Types of Articles" | 按研究类型切片结果 |
| `article-has-topic` | primary study | one-to-many | re-topic | {Elicitation, Analysis, ...} + emergent | 需 PDF 核对 Table I "Topic in RE" 列 | Table I: Mapping of papers | 按 RE 主题交叉统计 |

**补充说明**：
- 本文未发现显式的**层级关系边**（如 "benefit B2 subsumes B1"）或**因果边**（如 "problem P1 causes problem P5"）。所有关系边均为 article 与分类轴之间的编码关联。
- 方案与问题的映射是**非形式化**的——作者按 problem 分组叙述 solution，但未以结构化 schema（如 CSV mapping table）发布。此为关系边粒度不够精确的风险，A2a 精核时需确认是否可从 Table V 映射反推。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的统计观察

| # | 统计观察 | 支撑字段 / 表 | 证据强度 |
|---|---|---|---|
| SO1 | Conference proceedings 是最主要的出版 venue（53%），没有单一 venue 占主导 | Table I | 强（N=28，计数明确） |
| SO2 | 71% 的文章未指定具体敏捷方法上下文 | Table II | 强（N=28，计数明确） |
| SO3 | Method proposal 是最常见的文章类型（≈29%），但缺乏实证评估 | Table III | 强 |
| SO4 | 约 60% 的文章有实证成分（case study + experience report + evaluation） | Table III 汇总 | 中（"empirical" 定义宽泛） |
| SO5 | B2（Improved requirements understanding）获得最多文章支持（6 篇），B6（Improved customer relationships）最少（2 篇） | Table IV | 强 |
| SO6 | P1（Client/customer representatives）获得最多文章关注（6 篇） | Table V | 强 |
| SO7 | P3、P4、P6 三个问题领域没有任何文章提出解决方案 | Table V + IV.D 叙述 | 强（显式报告 "No solutions were proposed"） |
| SO8 | P1 和 P2 的多数解决方案借鉴了传统 RE 方法 | IV.D + V.C Discussion | 中（作者归纳，非量化） |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

| # | 候选 finding | 来源 | 与本仓库 Paper2 的关系 |
|---|---|---|---|
| CF1 | "There is no primary venue for articles on RE in ASD" —— RE in ASD 尚未在学术出版中找到稳定归属 | V.A Discussion | 可迁移为 SLR/SMS 对 venue 分散度的观察模式 |
| CF2 | "There is still considerable uncertainty of what requirements engineering in agile software development is" —— 概念仍模糊 | VI Conclusion | 可迁移为 "概念定义不统一" 的 mapping study 典型发现 |
| CF3 | Agile RE 的 benefits 与 agile methods 的通用声称基本一致 | V.C Discussion | 可迁移为 "benefit 分类法未发现与通用声称的区分性差异" |
| CF4 | Many problems mirror the proposed benefits —— 问题与收益存在镜像关系 | V.C Discussion | 可迁移为 problem–benefit 结构对称性的观察模式 |
| CF5 | Solutions for P1/P2 largely draw from traditional RE, but lack empirical evaluation | V.C Discussion + VI | 可迁移为 "方案大量借鉴旧范式但缺乏新证据" 的 gap 模式 |
| CF6 | Large/complex systems and large organizations need more research | VI Conclusion | 可迁移为 scope-condition gap 识别模式 |

### 6.3 对 Paper2 可迁移的方法学启发

1. **Benefit-Problem-Solution 三轴编码法**：对非效果导向的 mapping study，这是一种可复用的分类框架，适用于 Paper2 对 SMS 样本的跨论文维度投影。
2. **问题与方案的非对称映射**：P3/P4/P6 无方案 ↔ P1/P2 有多方案——这种**非对称 gap 识别法**可迁移为 Paper2 发现 "研究投入不均" 的通用启发式。
3. **"Unspecified context" 作为统计风险**：71% 文章未指定敏捷方法，这一观察方法可迁移为 Paper2 对任何 "上下文缺失" 风险的检测模式。
4. **概念模糊作为 mapping 发现**：CF2 揭示了 "没有统一定义" 本身就是一个有效发现——Paper2 可以类似地报告跨 SMS 样本的概念定义收敛/发散状态。

### 6.4 绝不能迁移的领域结论

- 所有具体的 benefit/problem/solution 内容（B1–B6、P1–P6）是 **Agile RE 领域特定**的，不可迁移到状态机建模、形式化验证等本仓库的目标领域。
- "Scrum 是最常见的显式上下文（25%）" 是 ASD 领域特定统计。
- "User story 不足" 是 ASD 实践特定问题。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 风险分级

#### 🔴 C 级（Critical — 必须修）

| # | 问题 | 修复建议 |
|---|---|---|
| **C1** | **六叶通用接口被用作原文维度树**：当前 `review.md` 的维度树复原（A1DT-re-agile-sms-2015-C01–C07）使用 `scope`/`corpus`/`taxonomy`/`method`/`evidence`/`finding` 六个通用叶子，这些是 A1-M0–M6 跨论文投影，**不是**本文自己的编码方案。本文的真实维度森林是 7 轴（出版属性、研究方法、敏捷方法上下文、RE 主题、Benefits B1–B6、Problems P1–P6、Solutions）。 | 重写 §维度树复原 为 §3 本文提供的原生维度森林结构。将六叶接口降级为 "跨论文投影辅助"（移至 A1-M0–M6 节或独立附录）。 |
| **C2** | **样本单位未明确声明**：`review.md` 未在任何位置明确指出 "primary study（n=28）是本文的编码单元"。 | 在 §1 快速结论卡片中新增 "被编码样本单位: primary study（n=28）"。 |
| **C3** | **原生树类型错误**：当前 `review.md` 未标注 "维度森林" 类型，叶子表把 7 个独立轴压缩为单树的 7 个叶子，丢失了轴之间的平行关系。 | 将 §3 重写为维度森林结构，明确标注 "类型: 维度森林（7 个平行分类轴）"。 |

#### 🟡 I 级（Important — 建议修）

| # | 问题 | 修复建议 |
|---|---|---|
| **I1** | **叶子表中缺少原文的具体字段值**：当前叶子表只给出抽象标签（如 "主题与维度分类"），没有列出 B1–B6、P1–P6、article-type 的 7 取值等具体内容。 | 按 §4 本文的叶子维度表，补全每个叶子的取值空间和具体枚举值。 |
| **I2** | **缺少关系边表**：`review.md` 无 §5 关系边表，未记录 article–benefit、article–problem、article–solution、problem–solution 等关系。 | 新增 §5 关系边表。 |
| **I3** | **SUMMARY 表中统计池相关字段需修正**：当前 A.3 的结论卡片中 "样本单位" 和 "原生树类型" 应修正为 "primary study（n=28）" 和 "维度森林（7 轴）"。 | 修正 A.3 对应行。 |
| **I4** | **Threat/validity section 误标**：§2 中 "validity/threat pattern" 写 "本轮未定位完整 threat section"，但本文 Section V.D 有明确的 Limitations paragraph（Scopus only + search string 受限）。 | 引用 V.D Limitations 作为 threat 证据锚点。 |

#### 🟢 M 级（Mild — 可选优化）

| # | 问题 | 修复建议 |
|---|---|---|
| **M1** | A.2 证据账本中的叶子标识仍用六叶通用名（`leaf-re-agile-sms-2015-scope` 等），需替换为原生字段名。 | 重命名叶子标识以匹配 §4 的原生字段。 |
| **M2** | A.4 人工核验清单中 `cmd-re-agile-sms-2015-visual-check` 标记为 `needs_manual_check`，可补充具体待核验的表/图编号。 | 明确列出 Table I–V 的待核验项。 |
| **M3** | §2 六类 pattern 中的 "dimension pattern" 应使用原生 benefit/problem/solution 轴，而非模糊的 "taxonomy/issue/solution"。 | 重写 dimension pattern 为原生 7 轴结构。 |

### 7.2 返修优先级

1. **先修 C1/C2/C3**（重写维度树）— 阻塞所有下游使用。
2. **再修 I1/I2/I3**（补叶子内容和关系边）— 影响统计池和 Paper2 维度设计。
3. **最后修 M1–M3**（细节优化）。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-2015-001 | paper_content.txt | III Methodology, Page 3 | "28 articles on the topic were identified and analyzed" | 样本总量 28 | 样本定义 | strong | 根节点 Primary Study (n=28) | 是（需核对全文筛选是否确为 28） | N=28 为本文特定 |
| EV-2015-002 | paper_content.txt | III Methodology, Page 3 | Search string: TITLE-ABS-KEY(...), Sep 2014, Scopus | 系统检索策略 | 方法论证据 | strong | 检索与纳排流程 | 否 | 检索策略因主题而异 |
| EV-2015-003 | paper_content.txt | III Methodology, Page 3 | 5 title/abstract exclusion criteria + 3 full-text exclusion criteria | 两级纳排标准 | 方法论证据 | strong | 样本纳入标准 | 否 | 纳排标准因研究问题而异 |
| EV-2015-004 | paper_content.txt | III Methodology, Page 3 | "The extracted results were categorized under the following four subject areas: Definition of RE... benefits... problems... solutions" | 四主题区分类框架 | 分类方案定义 | strong | Axis 5 Benefits, Axis 6 Problems, Axis 7 Solutions | 是（需核对 extraction form 字段是否与叙述一致） | 四主题区框架是本文特定归纳 |
| EV-2015-005 | paper_content.txt | IV.A, Page 3–4 | Table I: SUMMARY OF THE PUBLICATION VENUES | Venue type 分布: Conference 15, Journal 8, Magazine 5 | 频次统计 | strong | Axis 1 出版属性轴, leaf `venue-type` | 是（需核对 Table I 中每个 venue 的计数） | 分布为 2014 年时间截面 |
| EV-2015-006 | paper_content.txt | IV.A, Page 4 | Table II: SUMMARY OF AGILE METHODS | Unspecified 20 (≈71%), Scrum 7 (25%), FDD 1 (≈4%) | 频次统计 | strong | Axis 3 agile-method, leaf `agile-method` | 是（需核对 article [S1]–[S28] 的逐一赋值） | "Unspecified" 类目可能含隐式上下文 |
| EV-2015-007 | paper_content.txt | IV.A, Page 4 | Table III: SUMMARY OF TYPES OF ARTICLES | 7 种 article type 的频次 | 频次统计 | strong | Axis 2 研究方法轴, leaf `article-type` | 是（需核对逐一赋值） | 分类体系是 SE 特定 |
| EV-2015-008 | paper_content.txt | IV.C, Page 5 | Table IV: BENEFITS FROM AGILE RE AND RELATED ARTICLES | B1–B6 六类 benefit 及各自关联文章 | 分类 + 频次 | strong | Axis 5 Benefits, leaf `benefit-code` | 是（需核对 Table IV 的完整文章列表） | benefit 内容不可迁移 |
| EV-2015-009 | paper_content.txt | IV.D, Page 5–6 | Table V: PROBLEM THEMES AND RELATED ARTICLES | P1–P6 六类 problem 及各自关联文章 | 分类 + 频次 | strong | Axis 6 Problems, leaf `problem-code` | 是（需核对 Table V 的完整文章列表） | problem 内容不可迁移 |
| EV-2015-010 | paper_content.txt | IV.D, Page 5–6 | "No solutions to P3 were proposed in the articles"; "No solutions to P4 were proposed"; "No solutions to P6 were proposed" | 三个 problem 无 solution | 缺失值显式声明 | strong | Axis 7 Solutions, P3/P4/P6 的 solution-text | 否 | 缺失声明为本文特定发现 |
| EV-2015-011 | paper_content.txt | V.D, Page 7 | "The literature search was constrained to the Elsevier Scopus abstracts database... Additional keywords might have produced more articles" | 局限性声明 | 局限性证据 | strong | 整体证据强度评估 | 否 | 作为威胁声明样例可迁移 |
| EV-2015-012 | paper_content.txt | V.B, Page 7 | Proposed definition: "In agile RE, the requirements are elicited, analysed and specified in an ongoing and close collaboration..." | 概念定义提案 | 候选 finding | medium | CF2（概念仍模糊） | 是（需核对 exact wording） | 定义为 Agile RE 特定 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-2015-01 | Agile RE 的概念定义仍模糊，尚未统一 | 候选 finding | CF2 | EV-2015-001, EV-2015-012, V.B Discussion | medium | 用于说明 "概念模糊是 SMS 常见发现类型" | 仅限 2014 年前的 28 篇文章；可能有后续定义工作 |
| CONC-2015-02 | Benefit-Problem-Solution 三轴构成 agile RE 的完整证据空间 | 方法学贡献 | Axis 5/6/7 | EV-2015-004, EV-2015-008, EV-2015-009 | strong | 可迁移为三轴编码框架到其他领域的 mapping study | 框架是归纳性的，不一定穷尽所有维度 |
| CONC-2015-03 | 问题与方案的覆盖存在严重不对称：P1/P2 多方案，P3/P4/P6 无方案 | 统计 gap | CF5, SO7 | EV-2015-009, EV-2015-010 | strong | 可用于 "gap 识别方法学" 的模式样例 | 28 篇样本量小，可能遗漏已发表的 P3/P4/P6 方案 |
| CONC-2015-04 | 71% 的文章未指定具体敏捷方法，影响结果可推广性 | 方法论风险 | SO2 | EV-2015-006 | strong | 可用于 "上下文缺失作为方法论风险" 的样例 | "Unspecified" 不等于 "无上下文"；可能隐含 Scrum/XP |
| CONC-2015-05 | Method proposals 缺乏实证评估，研究社区需更多评估研究 | 未来工作方向 | CF5 | EV-2015-007, VI Conclusion | medium | 可用于 "方法提案与实证评估失衡" 的模式 | 28 篇中 8 篇是 method proposal，样本偏小 |
| CONC-2015-06 | 多数方案借鉴传统 RE 方法而非创新 agile-native 方案 | 候选 finding | CF4 | IV.D + V.C Discussion | medium | 可用于 "解决方案来源分布" 的观察模式 | 基于作者归纳而非量化分类 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件及采用的原则

| 技能文件 | 路径 | 采用的核心原则 |
|---|---|---|
| ai-research-writing-skill SKILL.md | `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | **Evidence gate**: 每个 major claim 必须有代码/结果/笔记/已验证引文支持。**Claim gate**: Abstract/Introduction 中的强声称不能无支撑。这两条用于本审计中区分 "原文支持的统计观察" vs "作者 discussion 中的候选 finding"。 |
| reviewer-guidelines.md | `.../references/reviewer-guidelines.md` | **Universal Review Dimensions**: Originality, Quality/Soundness, Clarity, Significance, Reproducibility, Ethics。用于评估本文的 method 透明度、limitation 报告、可复现性。**Common Reviewer Concerns**: 特别关注 "claims in Abstract/Introduction exceed the experiments"——本文 Abstract 声称 "28 articles were identified and analyzed" 与正文一致，未超售。 |
| reviewer-self-review.md | `.../references/reviewer-self-review.md` | **Claim Audit**: "Strong claims need direct evidence... First, general, unified, end-to-end, robust, and state-of-the-art require extra scrutiny"——本文未使用这些过度声称词，合标。**Experiment Audit**: 检查每个 experiment 是否对应一个 RQ——本文 Table I–V 与 RQ1–3 对应良好。 |
| research-planning SKILL.md | `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | 未直接用于本文审计。其 **task dependency graph** 和 **risk flagging** 原则用于本审计的返修优先级编排。 |
| planning-prompts.md | `.../references/planning-prompts.md` | 未直接使用。 |
| output-schemas.md | `.../references/output-schemas.md` | 未直接使用。 |
| autoresearch SKILL.md | `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | **Completion artifact contract**: "The loop does not stop because the model says done"——此原则指导本审计拒绝以 "review.md 已存在" 为理由跳过全文阅读，坚持基于 `paper_content.txt` 全文独立审计。 |

### 9.2 本输出最高风险的 3 点及主线程合并复核建议

| # | 风险 | 风险等级 | 复核建议 |
|---|---|---|---|
| R1 | **PDF 版面未完成视觉核验**：Table I–V 的精确数值、Table I 的 "Topic in RE" 列内容、Table IV/Table V 的完整 article 列表，均基于 `paper_content.txt` 的文本提取，未与 PDF 版面逐行核对。文本提取可能遗漏表格中的合并单元格、脚注或排版异常。 | 中 | 主线程合并时，由人工或具备 PDF 渲染能力的 agent 打开 `paper.pdf`，逐表核对 Table I–V 的每个 cell，并将差异记录到 §1 证据锚点或降级相关证据强度。 |
| R2 | **RE 主题轴（Axis 4）的取值空间不完整**：`paper_content.txt` 中 Table I 的 "Topic in RE" 列被文本提取打断，无法确定对 28 篇文章逐一赋值的精确内容。当前 §3 维度森林中 Axis 4 的取值空间仍基于 III Methodology 的预设分类（elicitation 等 6 项），实际赋值的涌现主题未知。 | 高 | A2a 精核时需从 PDF 逐行提取 Table I 的 "Topic in RE" 列，补充涌现主题并核实预设分类的赋值得分率。若 PDF 无法获取，将此轴标记为 `not_verified`。 |
| R3 | **现有 `review.md` 的六叶接口与原生森林结构差异大**：返修建议 C1 要求大范围重写 §维度树复原，可能与其他 A1 论文的 tree 风格不一致。 | 中 | 主线程需决定是统一所有 A1 论文的树表示（全部用原生树）还是保留两套表示（原生树 + 六叶投影）。若采用后者，需在 `review.md` 中清晰分层并标注互引关系。 |

### 9.3 任务状态

- **blocked**: 否。所有必需文件均可读取。
- **timeout**: 否。本任务在单次 turn 内完成。
- **文件缺失**: 无。`bibtex.bib`、`metadata.json`、`paper_content.txt`、`review.md`、`paper.pdf` 均存在。
- **PDF 版面精核**: 标记为 `needs_manual_check`（R1 和 R2），建议在人工核对完成后将证据强度从 strong 降级或维持。

---

*审计完成时间: 2026-06-30。本报告自包含，所有章节均包含实质内容，可直接用于重写 `review.md`。*