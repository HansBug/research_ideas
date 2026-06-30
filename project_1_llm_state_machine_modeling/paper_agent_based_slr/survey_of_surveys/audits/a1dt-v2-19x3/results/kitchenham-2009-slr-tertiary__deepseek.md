现在我已经读取了所有必需的技能/指南文件和论文文件。让我仔细分析这篇论文并构建完整的审计报告。

---

# A1-DT v2 单篇全文审计报告：`kitchenham-2009-slr-tertiary`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-2009-slr-tertiary` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是；已完整读取全文 962 行，覆盖 Abstract 到 References 全部内容 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；已读取 BibTeX 元数据和 metadata.json 全部字段 |
| 是否打开或核对 `paper.pdf` | 否；本次审计基于 `paper_content.txt` 文本提取结果。PDF 版面核验（Table 1--Table 5 的具体数值、quality score 的精确分项分布、Figure 1 的视觉布局）标记为待核验 |
| 原文类型 | tertiary-like SLR（三级研究：对 SE 领域已发表 SLR 进行系统文献综述） |
| 被编码样本单位 | 2004--2007 年间发表的 SE 领域 SLR（systematic literature review），每篇 SLR 是一个样本单位（primary study of this tertiary review） |
| 样本数量 / 分母 | N = 20（manual search 10 journals + 4 conference proceedings，初始命中 53 篇，经纳排后得到 20 篇 relevant SLR） |
| 原生树类型 | **维度森林**（dual-layer schema）：Layer 1 为 data extraction form 的 9 个编码字段组成的主维度树；Layer 2 为 quality assessment rubric 的 4 个评分项组成的质量评价子树 |
| 主统计池资格 | 是；原文有系统检索、纳排、数据抽取和编码方案，样本单位明确可追溯 |
| 总体判定 | **needs repair** — 现有 `review.md` 将六叶通用接口直接当作原文维度树，需重写为原文 9 字段原生 Schema + 4 项 QA rubric 的双层维度森林 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件

| 文件 | 读取状态 | 说明 |
|---|---|---|
| `bibtex.bib` | 完整读取 | 确认 DOI `10.1016/j.infsof.2008.09.009`，期刊 IST Vol. 51(1)，pp. 7--15 |
| `metadata.json` | 完整读取 | 确认 CCF-B、review_type 为 tertiary-like SLR、eligible_for_schema_seed=true |
| `paper_content.txt` | 完整读取 | 962 行 PDF 文本提取，覆盖 Abstract--References；来源为 PyPDF2 text mode |
| `review.md` | 完整读取 | 221 行，含快速结论卡片、六类 pattern 抽取、A.1--A.4 附录草案 |
| `paper.pdf` | **未核对** | 本次审计未打开 PDF 进行版面级视觉核验；Table 1--5 数值和 quality score 分项分布需人工对照 PDF |

### 1.2 关键证据锚点（12 个）

| # | 原文位置 | 证据角色 | 短引或释义 |
|---|---|---|---|
| EV-001 | Abstract, Page 1 | 样本数量与总体结论 | "Of 20 relevant studies, eight addressed research trends... Seven SLRs addressed cost estimation." |
| EV-002 | §2.1 Research questions, Page 2 | RQ 定义 | RQ1--RQ4：activity scale, research topics, researchers/organizations, limitations |
| EV-003 | §2.2 Search process, Page 2 | 检索策略 | Manual search of 10 journals + 4 conference proceedings (2004--June 2007) |
| EV-004 | §2.3 Inclusion/exclusion, Page 2 | 纳排标准 | "include any paper... claiming to be a systematic literature review" + exclusion of informal surveys, mapping studies, meta-analyses |
| EV-005 | §2.4 Quality assessment, Page 2 | QA rubric | 4-question instrument：inclusion criteria, search coverage, quality assessment of primary studies, adequate data description；每项 0/0.5/1，总分 0--4 |
| EV-006 | §2.5 Data collection, Page 2--3 | **核心维度树来源** | 9 字段 data extraction form：topic area, RQs, search strategy, inclusion/exclusion criteria, quality criteria, data extraction, synthesis methods, limitations, implications |
| EV-007 | §3.1 Search results, Page 3 | 检索结果与纳排流 | 初始命中 53 → screening → 20 relevant；按年份分布 Table 1 |
| EV-008 | §3.2 Quality evaluation, Page 3--4 | 质量评分分布 | Mean score ~2.75/4；仅 3 篇 < 2；分项分数 Table 2 |
| EV-009 | §3.3 Quality factors, Page 4 | 质量因素分析 | Reporting、rigour、credibility、contribution 四因素分类；Table 3 |
| EV-010 | §4.1--4.4 Discussion, Page 5--7 | RQ1--RQ4 讨论 | 年度活动趋势、topic 分布（cost estimation 7 篇为最大集群）、Simula 实验室突出、limitations 讨论 |
| EV-011 | §5 Conclusions, Page 7 | 最终结论 | "topic areas covered by SLRs are limited"；cost estimation 系列证明 EBSE 聚合证据潜力 |
| EV-012 | §2.7 Deviations from protocol, Page 3 | 协议偏离 | 额外纳入 2008 年 online-first 论文 1 篇（超出原检索窗口 2004--June 2007） |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

每篇被纳入的 **已发表 SLR**（secondary study）是本三级综述的样本单位。原文 §2.3 明确定义：纳入标准为 "any paper published between 1st January 2004 and 30th June 2007 that claimed to be a systematic literature review"。20 篇 SLR 中每个都被逐项编码。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**全部有。**

- **系统检索**：§2.2 明确手动检索 10 种期刊（IST、TSE、JSS、ESE、IEEE Software、TOSEM、ACM Computing Surveys、Software Practice and Experience、IEE Proceedings Software、Journal of Software Maintenance and Evolution）和 4 个会议论文集（ICSE、ISESE/EASE、Metrics Symposium、ESEM）。
- **纳排标准**：§2.3 明确纳入 claimed SLR；排除 informal survey、mapping study、meta-analysis。筛选分两阶段：先看 title/abstract，再看全文。
- **数据抽取**：§2.5 使用 standard data extraction form（基于 EBSE Technical Report [24]，经 pilot 后定稿），明确列出 9 个抽取字段。
- **编码方案**：quality assessment 使用 4 项 rubric（§2.4），data extraction 使用 9 字段 form（§2.5），topic 分类和 quality factors 分类在 Results 中进一步展开。

### 2.3 原文字段来自哪里？

字段来源明确：

| 来源 | 位置 | 字段数 |
|---|---|---|
| Data extraction form | §2.5 | 9 个字段 |
| Quality assessment rubric | §2.4 | 4 个评分项（各有评分标准） |
| 作者信息列（researcher/organization） | §3.1, Table 1 | 2 个附字段（author、institution） |
| 年份分布 | §3.1, Table 1 | 1 个时间字段 |
| Quality factor classification | §3.3, Table 3 | 4 个因素类别（reporting/rigour/credibility/contribution） |

注意：原文并未在 data extraction form 中显式列出 "author" 和 "institution" 作为抽取字段，但 RQ3 独立询问 "Which researchers and organizations are most active in conducting SLRs?"，且 Table 1 包含作者和机构信息。这属于 "RQ 驱动的辅助编码"，不应与主 extraction form 混淆。

### 2.4 RQ 与样本单位是什么关系？

- RQ **不是维度树根**，而是**结果组织方式**（即 findings 如何分组报告）。
- 样本单位是 20 篇 SLR，每篇 SLR 通过 data extraction form 编码 9 个字段。
- RQ1（activity scale）对应"年份"时间分布统计；RQ2（topics）对应 extraction form 中 "topic area" 字段的汇总分类；RQ3（researchers/organizations）对应作者/机构的描述性统计；RQ4（limitations）对应 extraction form 中 "limitations" 字段的归纳。
- 综上：编码 schema 是 **extraction-form-first**，RQ 驱动的是跨样本单位的结果组织方式。

### 2.5 若无系统样本库，如何降级？

不适用。本文有明确系统样本库（N=20），有检索策略、纳排标准和编码方案。

---

## 3. 原生样本编码维度树 / 维度森林

本文的原生编码体系是 **双层维度森林**：

### Layer 1：数据抽取主维度树（Data Extraction Schema，每 SLR 逐一编码）

```
SLR (sample unit, n=20)
├── topic_area
│   └── 取值空间类型：自由文本 + 后验分类
│       （原文 §3.1 / §4.2 将其归并为：cost estimation, testing techniques,
│        software process, defect detection, etc.）
│
├── research_questions
│   └── 取值空间类型：自由文本加理由
│       （每篇 SLR 的原始 RQ 被逐字抽取；在分析时归纳为 trends/technique evaluation）
│
├── search_strategy
│   ├── search_venues: 自由文本（列举检索来源）
│   ├── search_type: 层级枚举（manual only / automated / both）
│   └── 取值空间类型：关系值（每个 SLR → 其使用的具体来源列表）
│
├── inclusion_exclusion_criteria
│   ├── defined: 布尔（是/否定义纳排标准）
│   ├── selection_process_described: 布尔（是/否描述筛选过程）
│   └── 取值空间类型：布尔
│
├── quality_criteria_used
│   └── 取值空间类型：自由文本加理由
│       （每篇 SLR 是否使用了质量评价、使用了什么标准）
│
├── data_extraction_process
│   └── 取值空间类型：自由文本加理由
│       （每篇 SLR 的数据抽取方法，如 standard form / bespoke form / not described）
│
├── data_synthesis_methods
│   └── 取值空间类型：自由文本加理由
│       （narrative synthesis / meta-analysis / thematic analysis / not reported）
│
├── limitations_considered
│   └── 取值空间类型：布尔 + 自由文本
│       （每篇 SLR 是否讨论自身 limitation，若有则记录具体内容）
│
└── implications_for_SE_community
    └── 取值空间类型：布尔 + 自由文本
        （是否讨论对 SE 社区的实践/研究启示）
```

### Layer 2：质量评价子树（Quality Assessment Rubric，每 SLR 评分）

```
SLR (sample unit)
└── quality_score (0--4, 连续值/区间)
    ├── Q1: inclusion_exclusion_appropriate — 层级枚举 {0, 0.5, 1}
    │   └── 原文 scoring criteria: "1 = criteria defined and appropriate,
    │       0.5 = defined but not clearly appropriate, 0 = not defined"
    ├── Q2: search_coverage — 层级枚举 {0, 0.5, 1}
    │   └── scoring criteria: 1 = covers 4+ digital libraries + extra manual,
    │       0.5 = limited, 0 = minimal
    ├── Q3: quality_assessment_of_primary_studies — 层级枚举 {0, 0.5, 1}
    │   └── scoring criteria: 1 = explicit quality criteria used,
    │       0.5 = mentioned, 0 = not considered
    └── Q4: adequate_data_description — 层级枚举 {0, 0.5, 1}
        └── scoring criteria: 1 = adequate description, 0.5 = partial, 0 = not described
```

### 辅助统计维度（RQ 驱动的跨 SLR 汇总字段，不在 per-SLR 编码中）

```
Cross-SLR aggregation
├── publication_year (2004--2008)
├── author / first_author
├── institution / country
├── topic_classification (RQ2 分析中后验归类)
├── quality_factor_category (reporting / rigour / credibility / contribution)
└── primary_study_type (trend study vs. technique evaluation study)
```

**缺失说明**：原文 §3.3 的 quality factor 分类（Table 3）只有归纳后的四个大类，而不是对每篇 SLR 的细粒度编码。A2a 精核任务需要：① 从 Table 1 补齐每篇 SLR 的实际 author/institution；② 从 Table 2 / Table 3 补齐每篇 SLR 的 per-question QA 分项得分和 factor 分类；③ 判断 §4.3 中 7 篇 cost estimation SLR 的完整列表。

---

## 4. 叶子维度表

对 Layer 1 主维度树的每个叶子字段：

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-topic | 研究主题 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 的研究主题领域 | 自由文本 → 后验分类：cost estimation (7), testing techniques, defect detection, software process, effort estimation, web engineering, COTS, component-based quality, laboratory comparison, cross-company vs within-company | 自由文本加理由 | not_reported → 无法归类 → 排除或列为 unknown | RQ2 主题分布统计 | 识别 SE SLR 主题覆盖缺口，为 Paper2 设定纳入主题范围提供历史基线 | EV-001, EV-006, EV-010（§4.2） | 可迁移分类方法论；不可迁移具体主题分布（2004--2007 样本） |
| leaf-rq | 研究问题 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 的原始 research questions | 自由文本（每篇 1--N 个）→ 后验二分类：trends RQ / technique evaluation RQ | 自由文本加理由 | not_reported → RQ 可能隐含于目标声明中 | RQ 类型分析（§3.1："eight addressed research trends"） | 为 Paper2 的 RQ taxonomy 提供两分类种子 | EV-006, EV-007（§3.1） | 可迁移 RQ 类型分类逻辑；不可迁移具体 RQ 内容 |
| leaf-search-strategy | 检索策略 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 的检索方式与来源范围 | search_venues: 自由文本列表；search_type: {manual, automated, both} | 关系值 + 层级枚举 | not_described → 视为方法学缺陷，在 quality score Q2 中反映 | quality factor analysis（§3.3 reporting/rigour） | 为 Paper2 的 search strategy 审计模式提供字段模板 | EV-006, EV-009（§3.3） | 高度可迁移（为 survey-of-surveys 提供检索策略审计字段） |
| leaf-ie-criteria | 纳排标准定义与描述 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 是否定义 inclusion/exclusion criteria 并描述筛选流程 | {defined: 是/否, selection_described: 是/否} | 布尔 | 否 = 未定义（quality score Q1 受影响） | quality evaluation（§3.2, Table 2 Q1 分项） | 为 Paper2 的纳入/排除标准编码方案提供种子 | EV-005, EV-006, EV-008（§3.2） | 高度可迁移 |
| leaf-quality-criteria | 质量评价标准 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 是否使用了 primary study 质量评价，使用何种标准 | 自由文本（如 DARE criteria, bespoke checklist, none） | 自由文本加理由 | none → quality score Q3 = 0 | quality evaluation（§3.2, Table 2 Q3 分项） | 为 Paper2 的 quality appraisal 字段提供历史模式 | EV-005, EV-006, EV-008（§3.2） | 可迁移分类逻辑；具体 checklist 名称需现代更新 |
| leaf-data-extraction | 数据抽取过程 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 的数据抽取方法和工具 | 自由文本（form-based, multiple reviewers, bespoke tool, not described） | 自由文本加理由 | not_described → quality score Q4 受影响 | quality factor analysis（§3.3 credibility） | 为 Paper2 提供 data extraction 审计字段种子 | EV-006, EV-009（§3.3） | 可迁移 |
| leaf-synthesis | 数据综合方法 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 的数据综合/分析方法 | {narrative, thematic, meta-analysis, vote counting, not reported} | 层级枚举 + 自由文本 | not_reported → 影响 rigour 评分 | quality factor analysis（§3.3 rigour） | 为 Paper2 的 synthesis method taxonomy 提供种子 | EV-006, EV-009（§3.3） | 可迁移；entry 需现代 SE SLR 方法论补充 |
| leaf-limitations | SLR 局限性讨论 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 是否讨论了自身局限性 | 布尔 + 自由文本（具体 limitation 内容） | 布尔 + 自由文本加理由 | 否 → 方法学缺陷 | quality factor analysis（§3.3 credibility）；RQ4 | 为 Paper2 的 validity threats 提取模板 | EV-006, EV-009, EV-011（§3.3, §5）| 可迁移 |
| leaf-implications | 对 SE 社区的启示讨论 | topic_area (root→SLR) | §2.5 Data collection form | 每篇 SLR 是否讨论了 research/practice implications | 布尔 + 自由文本（具体 implication） | 布尔 + 自由文本加理由 | 否 → 缺乏实践连接 | RQ4（§4.4）研究限制与影响 | 为 Paper2 提供 implication coding 种子 | EV-006, EV-011（§4.4） | 可迁移 |

对 Layer 2 质量评价子树的叶子：

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-qa-q1 | 纳排适当性评分 | quality_score (root→SLR) | §2.4 QA rubric Q1 | 纳排标准是否定义且适当 | {0, 0.5, 1} | 层级枚举 | 缺失即 0 | 质量总分计算；QA 分项分布 | 为 Paper2 的 quality instrument design 提供 4 项模板 | EV-005, EV-008（Table 2） | 可迁移 rubric 结构；评分细则需兼容现代 SE SLR |
| leaf-qa-q2 | 检索覆盖度评分 | quality_score (root→SLR) | §2.4 QA rubric Q2 | 检索是否可能覆盖所有相关文献 | {0, 0.5, 1} | 层级枚举 | 缺失即 0 | 同上 | 同上 | EV-005, EV-008 | 同上 |
| leaf-qa-q3 | 初级研究质量评价评分 | quality_score (root→SLR) | §2.4 QA rubric Q3 | SLR 是否评价了纳入初级研究的质量 | {0, 0.5, 1} | 层级枚举 | 缺失即 0 | 同上 | 同上 | EV-005, EV-008 | 同上 |
| leaf-qa-q4 | 数据描述充分性评分 | quality_score (root→SLR) | §2.4 QA rubric Q4 | 基础数据/研究是否被充分描述 | {0, 0.5, 1} | 层级枚举 | 缺失即 0 | 同上 | 同上 | EV-005, EV-008 | 同上 |
| leaf-qa-total | 质量总分 | quality_score (root→SLR) | §2.4 QA rubric (computed) | Q1+Q2+Q3+Q4 合计 | [0, 4] 连续区间（实际整数+0.5） | 数值或区间 | 不适用（计算值） | 质量排名；quality factor analysis | 识别低质量 SLR 的 common weakness | EV-005, EV-008 | 可迁移总分类比逻辑 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-q1-to-ie | leaf-qa-q1 | 评分映射 | leaf-ie-criteria | 布尔 → {0, 0.5, 1} | 若 extraction form 中 ie-criteria 未定义，QA Q1 必为 0 | EV-005, EV-006, EV-008 | 证明 "defined" 不保证 "appropriate"：两级信息差是 QA 的设计意图 |
| edge-q2-to-search | leaf-qa-q2 | 评分映射 | leaf-search-strategy | search_venues 丰富度 → {0, 0.5, 1} | 未描述检索 → Q2 为 0 | EV-005, EV-008 | 连接 extraction form 与 QA 评分 |
| edge-q3-to-qcrit | leaf-qa-q3 | 评分映射 | leaf-quality-criteria | 使用与否 → {0, 0.5, 1} | 未提及质量评价 → Q3 为 0 | EV-005, EV-008 | 同上 |
| edge-q4-to-extraction | leaf-qa-q4 | 评分映射 | leaf-data-extraction | 描述充分性 → {0, 0.5, 1} | 未描述 → Q4 为 0 | EV-005, EV-008 | 同上 |
| edge-qa-factor-classification | leaf-qa-total | 后验分类 | quality_factor_category | {reporting, rigour, credibility, contribution} | 无法归类 → 排除 | EV-009（§3.3, Table 3） | 跨 SLR 的 QA weakness 模式识别 |
| edge-year-trend | publication_year | 时序统计 | SLR 计数 | 年度频数（2004: 1, 2005: 5, 2006: 6, 2007: 7, 2008: 1） | 无 | EV-007（§3.1, Table 1） | RQ1 年度活动趋势 |
| edge-author-institution | SLR | 归属关系 | author + institution | 姓名 + 机构名（自由文本） | 无 | EV-007（§3.1, Table 1） | RQ3 研究者/机构活跃度 |

**说明**：本文的维度森林主要存在于 **per-SLR parallel encoding**（每篇 SLR 独立编码同样的 9+X 个字段），跨 SLR 的关系边稀少。上表中 edge-qa-* 四条边是同一 SLR 内部 extraction form ↔ QA score 的映射关系，这构成了该双层 schema 的核心结构性特征。论文的 Topic 分类和 Quality factor 分类是**后验归纳**（基于 data extraction 结果做二次归类），不是 per-SLR 编码时记录的字段。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的统计观察

这些是从 extraction form 字段汇总而来的**描述性统计事实**：

| # | 统计观察 | 支撑字段 | 原文位置 |
|---|---|---|---|
| SO-1 | 20 篇 SLR 纳入，年份分布 2004(1) → 2005(5) → 2006(6) → 2007(7) + 2008(1) | publication_year | Table 1 (Page 3 附近), §3.1 |
| SO-2 | 8 篇 addressing research trends，其余为 technique evaluation | leaf-rq（后验二分类） | Abstract, §3.1 |
| SO-3 | 7 篇 SLR 聚焦 cost estimation（最大主题集群） | leaf-topic（后验归类） | Abstract, §4.2 |
| SO-4 | Mean quality score ≈ 2.75/4，仅 3 篇 < 2 | leaf-qa-total | Abstract, §3.2 |
| SO-5 | Q2 (search coverage) 是 QA 最低分项；Q3 (quality assessment of primary studies) 变动最大 | leaf-qa-q1--q4 | §3.2, Table 2 |
| SO-6 | 大多数 SLR 在 limitations 和 implications 方面不足 | leaf-limitations, leaf-implications | §3.3 (quality factors credibility/contribution) |
| SO-7 | Simula Laboratory (Norway) 的研究者在 SLR 产出中最为突出 | author + institution | §3.1, §4.3 |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

这些是作者对统计观察的**解释与推荐**，具有"候选发现"性质：

| # | 候选 finding | 原文位置 | 支撑统计 |
|---|---|---|---|
| CF-1 | "The topic areas covered by SLRs are limited" — SE SLR 主题覆盖不均衡，集中在少数领域 | §5 Conclusions | SO-2, SO-3 |
| CF-2 | "European researchers, particularly those at the Simula Laboratory appear to be the leading exponents" | Abstract, §4.3 | SO-7 |
| CF-3 | Cost estimation SLR 系列证明了 EBSE 聚合证据、向实践者传递知识的潜力 | §5 Conclusions | SO-3 |
| CF-4 | SE SLR 方法学质量 fair 但仍有提升空间；search coverage 薄弱；primary study QA 差异大 | §3.2, §3.3 | SO-4, SO-5 |
| CF-5 | SE SLR 需要在 limitations 和 implications 方面更多讨论（credibility 和 contribution 因素薄弱） | §3.3 | SO-6 |

### 6.3 对 Paper2 可迁移的方法学启发

| # | 可迁移启发 | 迁移用途 |
|---|---|---|
| M-1 | 9 字段 data extraction form 结构可直接作为 Paper2 survey-of-surveys 编码表的**种子模板** | 维度树种子 |
| M-2 | 4 项 quality rubric（Q1--Q4）+ per-SLR quality factor 分类为 Paper2 的**综述质量评价方案**提供设计先验 | 质量评价子树种子 |
| M-3 | "protocol deviation 显式记录"模式（§2.7）应被 Paper2 采纳为 agents-augmented review 的透明度要求 | 方法学规范种子 |
| M-4 | RQ 作为结果组织方式（而非编码根）这一区分对 Paper2 的 survey-of-surveys 结构设计至关重要 | 维度树 vs. RQ 的关系定义种子 |
| M-5 | 统计观察 → 候选 finding → final finding 的三级区分方法论 | finding 模式种子 |

### 6.4 绝不能迁移的领域结论

- CF-1 "SE SLR 主题覆盖有限" 是基于 2004--2007 样本的**历史观察**，不能延伸为 2024+ SE LLM4SE SLR 的现状判断。
- CF-2 "Simula 实验室是领导性代表" 是**机构级历史事实**，Paper2 不应将其作为现代 LLM4SE 综述的作者分布假设。
- SO-3 "cost estimation 是最大主题集群" 是 **2004--2007 特定时段**的分布，Paper2 不应预设其 dominant 地位。

---

## 7. 对现有 `review.md` 的返修建议

### C 级（Critical — 阻塞性，修复前不得进入正式统计）

| # | 问题 | 严重性 | 修复建议 |
|---|---|---|---|
| C-1 | **§2 "六类 pattern 抽取" 把六个通用接口当作原文维度树**。这是 `review.md` 最根本的问题：dimension pattern 中 "RQ pattern / dimension pattern / finding pattern / evidence presentation pattern / validity pattern / report structure pattern" 是跨论文通用六叶投影，而非本文的原生 9 字段 extraction form + 4 项 QA rubric 维度森林 | C | 重写 §2 为原文原生维度森林复原（见本报告 §3）。六叶接口可保留作为跨论文参考，但必须标为外部投影而非原文 schema |
| C-2 | **SUMMARY 当前表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"缺少或错误**。当前 review.md 没有独立的 SUMMARY 行，A.1--A.4 附录中的 claims 未区分统计池资格 | C | 在 review.md 中新增一行 SUMMARY 等价字段：样本单位 = "20 SLR"，原生树类型 = "维度森林（9 字段 extraction form + 4 项 QA rubric）"，统计池资格 = "是" |

### I 级（Important — 影响后续 A2a 精核和 Paper2 设计）

| # | 问题 | 严重性 | 修复建议 |
|---|---|---|---|
| I-1 | **叶子维度表 A.1 的通用六叶仍被当作原文叶子**。当前 A.1 中列为 "语料与纳排 / 主题与维度分类 / 方法技术干预分类 / 评价证据与复现资产 / 统计观察与候选发现 / 迁移边界" 的叶子是跨论文通用接口，不是原文 9 字段的原生叶子 | I | 用本报告 §4 的叶子维度表替换 A.1。每个叶子必须来自 §2.5 的 9 字段或 §2.4 的 4 项 QA rubric，保留通用六叶作为 appendix "跨论文参考表" 并标注来源 |
| I-2 | **RQ 与样本单位的关系未明确**。review.md 将 RQ 作为 pattern 抽取内容（§2 "RQ pattern"），但没有回答 RQ 是树根还是结果组织方式 | I | 新增 §2.x 明确：RQ 是结果组织方式，不是维度树根。与 sample unit (20 SLR) 的关系是 "RQ 驱动跨 SLR 的统计汇总" |
| I-3 | **双层的 QA rubric 子树完全缺失**。review.md 完全没有复原 §2.4 的质量评价维度（Q1--Q4 四项评分）及其与 extraction form 字段的映射关系 | I | 新增 QA 子树节点和关系边（edge-q1-to-ie 等），补全本报告 §3 Layer 2 和 §5 的内容 |
| I-4 | **§2.7 protocol deviation 作为效度关键证据缺失**。review.md 的 validity pattern 只提 "protocol deviation 记录"，但没有将具体的 2008 年额外纳入 1 篇的 deviation 作为证据锚点列出 | I | 在 §2 validity pattern 中补入具体 protocol deviation 证据（本报告 EV-012），并在 A.2 账本中新增对应行 |

### M 级（Minor — 改善性建议，不阻塞统计池资格）

| # | 问题 | 严重性 | 修复建议 |
|---|---|---|---|
| M-1 | **A.1 claim 表全部标注 `evidence_strength = weak` 和 `type = schema_seed`** — 这是正确的保守策略，但需要在文本中明确声明"`schema_seed` 意味着本报告尚未完成 A2a 精核，所有取值空间和统计值都待 PDF 版面核对" | M | 在 SUMMARY 中新增声明行 |
| M-2 | **A.2 证据账本缺少 §2.5 的完整 9 字段**。现有证据锚点 EV-kitchenham-2009-slr-tertiary-002/003/004 过于笼统 | M | 拆分为 per-field 证据锚点（本报告 §1.2 EV-001 至 EV-012） |
| M-3 | **A.3 结论-证据映射 `clm_type` 仅使用了 `source_schema_candidate`** — 应区分 `statistical_observation` / `candidate_finding` / `methodological_seed` / `migration_boundary` | M | 重写 A.3，按本报告 §6 的分类体系重新标注 |
| M-4 | **表 `A.4` 中的 `needs_manual_check` 应改为指向具体 PDF 页/表/图的清单** | M | 新增人工核验清单行：Table 1（年份/作者/机构）、Table 2（Q1--Q4 分项分布）、Table 3（quality factor 分类 ± 细粒度 coding）、Table 4（impact/limitation 摘要）、Table 5（search venue list）、Figure 1（检索引擎与 SLR 数量的可视化） |

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001-abstract | paper_content.txt | Abstract | Page 1, Abstract 段落 | "Of 20 relevant studies, eight addressed research trends... Seven SLRs addressed cost estimation. The quality of SLRs was fair with only three scoring less than 2 out of 4." | 样本量 + 关键统计 | high（原文明述） | dim-kitchenham-root, leaf-topic, leaf-qa-total | 否（数值与后续表格一致则无需） | 统计值仅适用于 2004--2007 样本 |
| EV-002-rq | paper_content.txt | §2.1 | Page 2, §2.1 段落 | RQ1 "How much EBSE Activity?"; RQ2 "What research topics?"; RQ3 "Which researchers and organizations?"; RQ4 "What are the limitations?" | RQ 定义 | high | RQ 与维度树的关系定义 | 否 | RQ 结构可迁移，具体 RQ 答案不可迁移 |
| EV-003-search | paper_content.txt | §2.2 | Page 2, §2.2 段落 | "manual search of 10 journals and 4 conference proceedings"；Table 5 列出完整 venue 清单 | 检索策略 | high | leaf-search-strategy, edge-q2-to-search | 是（Table 5 需核验 venue 列表完整性） | 历史检索范围不代表现代检索生态 |
| EV-004-ie | paper_content.txt | §2.3 | Page 2, §2.3 段落 | "include any paper... claiming to be a systematic literature review"; exclusion of informal surveys, mapping studies, meta-analyses | 纳排标准 | high | leaf-ie-criteria, edge-q1-to-ie | 否 | 纳排逻辑可迁移，具体标准不可迁移 |
| EV-005-qa-rubric | paper_content.txt | §2.4 | Page 2, §2.4 段落 | 4-question instrument: Q1 inclusion/exclusion, Q2 search coverage, Q3 primary study QA, Q4 adequate data description; 每项 0/0.5/1 | QA rubric 完整定义 | high | leaf-qa-q1--q4, leaf-qa-total | 是（评分细则的精确措辞需对照 PDF） | rubric 结构可迁移，具体阈值不可迁移 |
| EV-006-extraction-form | paper_content.txt | §2.5 | Page 2--3, §2.5 段落 | "The final data extraction form recorded information about: the topic area, the research questions, the search strategy, whether the authors... had defined inclusion/exclusion criteria..., the quality criteria used, the data extraction process, the methods for synthesising data, whether the authors considered SLR limitations, whether the authors had considered the implications" | 核心维度树：9 字段完整清单 | high | leaf-topic, leaf-rq, leaf-search-strategy, leaf-ie-criteria, leaf-quality-criteria, leaf-data-extraction, leaf-synthesis, leaf-limitations, leaf-implications | 否（9 字段清单为明述） | 字段结构可迁移，但 Paper2 需扩展（如 reproducibility/LLM usage 字段） |
| EV-007-results-table1 | paper_content.txt | §3.1 | Page 3, §3.1 + Table 1 | "We identified 20 SLRs..."; Table 1: SLR 编号、年份、作者、机构、title 的完整列表 | 样本单位完整枚举 | high | dim-kitchenham-root, edge-year-trend, edge-author-institution | 是（Table 1 的 20 行条目需逐一核对） | 具体作者/机构不可迁移 |
| EV-008-qa-results | paper_content.txt | §3.2 | Page 3--4, §3.2 + Table 2 | "Mean score approx 2.75"; "only three papers scoring less than 2"; Table 2: Q1--Q4 分项分布 | QA 评分汇总 | high | leaf-qa-q1--q4, edge-qa-factor-classification | 是（Table 2 精确分数需对照 PDF） | 具体分数不可迁移 |
| EV-009-quality-factors | paper_content.txt | §3.3 | Page 4, §3.3 + Table 3 | "Quality criteria mapped to four factors: reporting, rigour, credibility, contribution" | quality factor 分类 | medium（原文归纳逻辑未完整披露） | edge-qa-factor-classification | 是（Table 3 完整映射需对照 PDF） | 四因素分类可迁移作为 seed；具体 SLR 归属不可迁移 |
| EV-010-discussion-topic | paper_content.txt | §4.2 | Page 5--6, §4.2 段落 | "the 7 cost estimation SLRs [16, 6, 8, 9, 10, 20, 21]"; "Testing techniques [18, 19]"; topic 分布讨论 | topic 分布 | high | leaf-topic, CF-1, CF-3 | 是（7 篇引用编号需核对） | 主题分布不可迁移 |
| EV-011-conclusions | paper_content.txt | §5 | Page 7, §5 段落 | "Currently, the topic areas covered by SLRs are limited"; "The series of cost estimation SLRs demonstrate the potential value of EBSE" | 候选 finding | high | CF-1, CF-3 | 否 | 领域结论不可迁移 |
| EV-012-protocol-deviation | paper_content.txt | §2.7 | Page 3, §2.7 段落 | "We deviated from our protocol in one respect. We found a SLR published in 2008 which was available online in 2007 so we included it." | protocol deviation 记录 | high | validity pattern | 否 | 透明性做法可迁移；具体 deviation 不可迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CON-001 | 本文维度树根为 "单个 SLR (n=20)"，双层维度森林由 9 字段 extraction form（Layer 1）+ 4 项 QA rubric（Layer 2）组成 | dimension_tree_reconstruction | dim-kitchenham-root, leaf-topic, leaf-rq, leaf-search-strategy, leaf-ie-criteria, leaf-quality-criteria, leaf-data-extraction, leaf-synthesis, leaf-limitations, leaf-implications, leaf-qa-q1--q4 | EV-005, EV-006, EV-007 | high | 作为 Paper2 维度树种子 + 现有 review.md 返修的事实基础 | extraction form 中某些字段（如 search_strategy）是复合字段，其亚字段细粒度需 A2a 精核 |
| CON-002 | RQ 是结果组织方式，不是维度树根 | schema_design_principle | RQ vs. dimension tree 关系定义 | EV-002, EV-006 | high | 指导 Paper2 区分编码 schema 与报告结构 | 此结论来自本文的 RQ 角色分析，不隐含所有 tertiary study 的 RQ 都非维度树根 |
| CON-003 | 4 项 QA rubric 评分与 9 字段 extraction form 之间存在系统映射关系 | relation_edge_discovery | edge-q1-to-ie, edge-q2-to-search, edge-q3-to-qcrit, edge-q4-to-extraction | EV-005, EV-006, EV-008 | high | 为 Paper2 的 quality appraisal sub-schema 设计双层映射模式 | 仅当 Paper2 也采用 extraction form + quality rubric 双层设计时适用 |
| CON-004 | 20 篇 SLR 的 quality score 分布：mean ≈ 2.75，仅 3 篇 < 2 | statistical_observation | leaf-qa-total | EV-001, EV-008 | medium（需 PDF 核验 Table 2 精确值） | 作为 Paper2 quality assessment 设计的参考基线 | 样本量小（n=20），不能代表 2024+ SE SLR 质量水平 |
| CON-005 | 7 篇 cost estimation SLR 构成最大主题集群 | statistical_observation | leaf-topic, edge-year-trend | EV-001, EV-010 | high | 作为 tertiary study "主题分布统计"的方法学模板 | 2004--2007 历史分布，不可迁移为 Paper2 的预期分布 |
| CON-006 | 9 字段 extraction form 可作为 Paper2 的 survey-of-surveys 编码表种子 | methodological_seed | leaf-topic, leaf-rq, leaf-search-strategy, leaf-ie-criteria, leaf-quality-criteria, leaf-data-extraction, leaf-synthesis, leaf-limitations, leaf-implications | EV-006 | medium（种子需 A2a 跨论文精核 + 现代字段扩展） | 用于 Paper2 初始 coding form 设计 | 需补充 reproducibility、LLM involvement、code/data availability、preregistration 等现代字段 |
| CON-007 | SE SLR 的 quality factor 可归纳为 reporting / rigour / credibility / contribution 四个维度 | methodological_seed | edge-qa-factor-classification | EV-009 | weak（归纳逻辑未完整披露，待原文 Table 3 核验） | 用于 Paper2 QA sub-schema 的分类维度 | 四因素适合作为种子，但 Paper2 可能需要更细粒度或不同维度 |
| CON-008 | 当前 review.md 的六叶 pattern 非原文原生树，需重写 | audit_finding | review.md §2, §A.1 | EV-006, EV-005（对照 review.md 现有内容） | high | 驱动 review.md 重写 | 此结论基于审计审查，不否定六叶接口作为跨论文投影的价值 |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件

| 技能文件 | 读取状态 | 采用的核心原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 完整读取 | **Evidence gate**（证据优先，没有证据就降级）；**Claim gate**（不在没有支撑处做强烈断言）；**Citation gate**（不做虚假引用） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 完整读取 | 核心 reviewer 问题（what problem? well motivated? experiments support claims? significance?）；"Constructive Specificity Standard"（意见必须足够具体以便作者可执行） |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 完整读取 | C/I/M 分级（Critical/Important/Minor）；**Rejection-Risk Audit** 五要素：thesis → top objections → evidence → remaining gaps → fix plan；"Claim Audit" 模板（claim → evidence → risk → revision → status）；adversarial questions 列表 |
| `research-planning/SKILL.md` | 完整读取 | 结构化 analysis 方法（RQ → methodology → paper structure → task dependency）；"Flag ambiguities explicitly rather than making assumptions" |
| `research-planning/references/planning-prompts.md` | 完整读取 | 多轮对话 planning 模式；系统指令中的 "DO NOT FABRICATE DETAILS" 强制约束 |
| `research-planning/references/output-schemas.md` | 完整读取 | JSON schema 和 Mermaid diagram 模板 —— 本次审计报告不适用这些格式模板，但其中的风险记录（risks list with severity/mitigation）被采纳 |
| `oh-my-codex/autoresearch/SKILL.md` | 完整读取 | "Completion is artifact-gated" —— 审计报告自身即为 artifact；"The loop does not stop because the model says done" —— 本报告需通过主线程合并时的审查 |

### 9.2 本输出最高风险的 3 点

| # | 风险 | 说明 | 主线程合并时的复核建议 |
|---|---|---|---|
| R-1 | **PDF 版面未核验** | Table 1--5 和 Figure 1 的内容依赖 `paper_content.txt` 的文本提取。PyPDF2 text mode 可能丢失表格格式化信息（行列错位、合并单元格、特殊符号），导致 quality score Q1--Q4 的分项分布、Table 3 的 quality factor 细粒度分类、Table 1 的完整 20 行作者/机构列表有偏差 | 主线程合并时必须打开 `paper.pdf` 对照 Table 1--5 逐行核验。若发现文本提取版本与 PDF 版面不一致，以 PDF 为准并更新证据强度 |
| R-2 | **quality factor 分类的原文归纳逻辑不透明** | §3.3 中 "reporting / rigour / credibility / contribution" 四因素分类是将 Q1--Q4 分项得分 + extraction form 字段映射到四个 quality factor 的后验归纳，但原文未给出完整的映射表。当前 CON-007（四因素分类方法论）的证据强度为 weak | 主线程合并时应在 A2a 精核中尝试复原 Table 3 的完整映射，如果原文确实缺少逐 SLR 细粒度编码，应将 CON-007 降级为 "partial_evidence" 并标注 A2a 需补做 gap |
| R-3 | **extraction form 字段的亚结构不完整** | §2.5 的 9 字段清单是高级描述。某些字段（如 search_strategy）实际包含多个亚字段（venues、type、coverage level），但原文未逐一列出。当前维度树采用"复合字段 + 取值空间描述"的保守做法 | 主线程合并时应判断：是否需要进一步拆分 search_strategy 为 {search_venues, search_type, search_coverage} 等亚字段。若原文没有更细粒度信息，在当前 A1-DT 阶段接受复合字段，标注为 A2a 拆分候选 |

### 9.3 任务完成状态

| 项目 | 状态 |
|---|---|
| 所有必需技能文件读取 | ✅ 全部 7 个文件已读取 |
| `paper_content.txt` 全文读取 | ✅ 962 行完整读取 |
| `bibtex.bib` 读取 | ✅ |
| `metadata.json` 读取 | ✅ |
| `review.md` 读取 | ✅ 221 行完整读取 |
| `paper.pdf` 版面核验 | ⚠️ **未做**（文本级审计；PDF 待人工核验） |
| 被 blocking / timeout / 文件缺失 | **无** — 所有文件均可读取，无超时 |

### 9.4 本审计的最高优先级行动项（供主线程合并时使用）

1. **重写 `review.md` §2 和 A.1**：将六叶通用接口替换为 9 字段 extraction form + 4 项 QA rubric 的原生双层维度森林（本报告 §3--§5）。
2. **新增 SUMMARY 行**：标注样本单位 = "20 SLR"、原生树类型 = "维度森林（双层）"、统计池资格 = "是"。
3. **安排 PDF 版面核验**：对照 Table 1--5、Figure 1 逐项核实本报告 A.2 中的 8 个标记为需要原文版面核验的证据行。
4. **A2a 精核预备**：将本报告的叶子维度表和关系边表作为 A2a 入口，标注哪些字段需跨论文比较、哪些需要现代补充。

---

*审计完成时间：2026-06-30 | agent: deepseek | 审计类型：A1-DT v2 单篇全文审计*