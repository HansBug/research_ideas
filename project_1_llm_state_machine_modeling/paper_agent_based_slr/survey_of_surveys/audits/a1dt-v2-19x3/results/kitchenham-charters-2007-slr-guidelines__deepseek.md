现在我已全面阅读所有材料。以下为完整审计报告。

---

# A1-DT v2 单篇全文审计报告

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `kitchenham-charters-2007-slr-guidelines` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。已读全部 3091 行、覆盖 §0--§8 及 Appendix 1--3 全文。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。已完整读取。 |
| 是否打开或核对 `paper.pdf` | 否。本次审计基于 `paper_content.txt` 全文文本级。PDF 版面核验（表格完整度、页码精确对应、版权页、图表版式）未做，标注为 `needs_manual_check`。 |
| 原文类型 | **guideline** — 方法学准则 / 技术报告，非执行后的 SLR/SMS/tertiary study |
| 被编码样本单位 | **无系统样本库**。本文以 SLR 流程阶段、程序组件、结构化框架（PICOC、Quality Checklist、Report Template、Protocol Template）为描述对象，不以 primary study 为编码单元。文中 Kitchenham et al. [21]、Jørgensen [17] 等例子是教学性插图（pedagogical illustration），不是系统采样后的编码样本。 |
| 样本数量 / 分母 | **不适用**。无系统检索、纳排或数据抽取；附录 A 中 Appendix 2 列出 20 篇 SE SLR 的 DARE 评分，但这不是本文的系统样本库，而是附录性质的 existing review summary。 |
| 原生树类型 | **降级树** — 本文没有"对 N 个 primary study 逐项编码"的维度树。原生结构是 **SLR 过程阶段树** + **结构化框架清单**（PICOC 五元组、定量/定性质量核对清单、报告结构模板、protocol 模板字段）。属于 guideline 降级：可作 boundary anchor / methodological seed / candidate heuristic，不进入主统计池。 |
| 主统计池资格 | **否**。理由：本文是方法学 guideline，不是执行后的 SLR/SMS/tertiary 统计样本；`metadata.json` 已正确标记 `eligible_for_statistical_synthesis: false`，`statistical_pool_exclusion_reason` 为"方法学 guideline；不是执行后的 SLR/SMS/tertiary 统计样本"。 |
| 总体判定 | **needs repair** — 现有 `review.md` 维度树复原存在三个 I 级问题：(1) 仍在用六叶通用投影接口作为原文树根；(2) 缺 RQ 结构框架（PICOC）作为独立叶子节点；(3) A.2 / A.3 证据链缺少页码精确锚定。M 级问题包括摘要写法使 guideline 听起来像 tertiary study。详见 §7。 |

---

## 1. 原文证据阅读说明

### 目标文件与读取方式

| 文件 | 读取方式 | 读取范围 |
|---|---|---|
| `paper_content.txt` | `cat` 全文，分段读取 | §0（目录 / 版本控制）-- §8（Mapping Studies）全文，含 Appendix 1（Steps）、Appendix 2（20 篇 SLR 的 DARE 摘要）、Appendix 3（Tertiary Review Protocol 完整文本） |
| `bibtex.bib` | `cat` 全文 | 技术报告元数据 |
| `metadata.json` | `cat` 全文 | 15 字段完整 meta |
| `review.md` | `cat` 全文 | 约 220 行，含六类 pattern、A.1--A.4 附录草案 |
| `paper.pdf` | 未读取 | — |

### 未做 PDF 版面核验的部分

- Table 5 的完整 33 行在 `paper_content.txt` 中已全部提取，但 PDF 中跨页断裂、列对齐和脚注需要在原文中核验。
- Table 6 的完整 18 行同样已提取，但 PDF 版面的表格编号（Table 5/6 的页码在原文中是 25--28 页范围）需 PDF 确认。
- Table 8（Report Structure）已完整提取，但 "asterisk" 标记（PhD thesis 不适用项）和子节标题层级需 PDF 核对。
- Appendix 2 中的 20 篇 DARE-scored SLR 列表，`paper_content.txt` 提取了所有条目，但 DARE 四项评分细节和论文来源需要 PDF 版面确认。
- Appendix 3 的完整 Tertiary Review Protocol 文本已提取。

### 12 个关键原文证据锚点

| # | 原文章节 | 段落 / 表图线索 | 短引 / 释义 |
|---|---|---|---|
| 1 | §2.4 Features of SLRs | Page 4, §2.4 | SLR 三阶段：planning → conducting → reporting |
| 2 | §2.5.1 Mapping Studies | Page 4 | Mapping studies = broad overview, classification/categorisation stage, less focused search |
| 3 | §2.5.2 Tertiary Reviews | Page 5 | Tertiary review = review of secondary studies, uses same methodology as SLR |
| 4 | §5.3.1 Question Types | Page 9--10 | 五类 SE 问题改编自医学六类；例：assessing effect of SE technology, frequency/rate of project factor, cost/risk factors, impact on reliability, cost-benefit |
| 5 | §5.3.2 Question Structure (PICOC) | Page 10--13 | PICOC = Population, Intervention, Comparison, Outcome, Context；各有 SE 实例定义 |
| 6 | §5.4 Developing a Review Protocol | Page 12--13 | Protocol 必须包含：background, RQs, search strategy, selection criteria, quality checklists, data extraction, synthesis, timetable |
| 7 | §6.2 Study Selection | Page 18--20 | Inclusion/exclusion criteria, selection process, reliability of inclusion decisions |
| 8 | §6.3 Quality Assessment + Table 5 + Table 6 | Page 20--28 | Table 5: 33 个量化研究质量检查项（Design / Conduct / Analysis / Conclusions 四阶段）；Table 6: 18 个质性研究质量检查项 |
| 9 | §6.4 Data Extraction | Page 28--34 | Extraction form 设计原则：需覆盖 general info、specific data items 以回答 RQ、需 pilot |
| 10 | §6.5 Data Synthesis | Page 34--39 | 五种综合方式：narrative、tabular、quantitative (meta-analysis)、qualitative aggregation、mixed；强调 tabulation 是 SE 中最实用的 |
| 11 | §7.2 + Table 8 | Page 40--43 | Table 8: SLR 报告结构模板（Title, Authorship, Structured Abstract, Background, Review Questions, Methods, Results, Discussion, Conclusions, References & Appendices） |
| 12 | Appendix 3 | Page 55--57 | 完整 Tertiary Review Protocol 实例：Background, Research Questions (4 RQs about EBSE activity since 2004), Search Strategy, Study Selection, Quality Assessment (4-item scoring), Data Extraction (10 fields), Data Analysis, Dissemination |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

原文的纳入和描述对象不是 primary studies，而是 **SLR 方法论本身的构成要素**：流程阶段、程序组件、结构化框架和 protocol 模板。具体而言：

- **流程阶段**：Planning（§5）、Conducting（§6）、Reporting（§7）。
- **程序组件**：每个阶段下的子步骤（如 Planning 下的 need identification、commissioning、RQ formulation、protocol development、protocol evaluation）。
- **结构化框架**：PICOC 五元组（§5.3.2）、定量研究质量核对清单 Table 5（§6.3.2）、质性研究质量核对清单 Table 6（§6.3.2）、报告结构模板 Table 8（§7.2）、数据抽取表设计原则（§6.4.1）。
- **Protocol 模板实例**：Appendix 3 给出一个完整的 Tertiary Review Protocol，其字段列表为：Background → Research Questions → Search Strategy → Study Selection Criteria → Quality Assessment Procedures → Data Extraction Variables → Data Analysis Plan → Dissemination Strategy。

文中 Kitchenham et al. [21] 和 Jørgensen [17] 以 "Examples" 小节形式嵌入（Page 10, 12, 28, 32），作用是教学性插图，不是系统采样后的 data point。同样，Appendix 2 列出的 20 篇 SE SLR 是作为 DARE 评分标准的演示案例，不是本文进行系统纳排和编码的样本。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**没有。** 原文声明其构建方法是"基于现有医学 SLR 指南、社会学研究文本和软件工程经验改编"（§1.1 Source Material, §1.2 Construction Process）。这不是 systematic review，而是 **guideline construction**。

原文本身就是一个**规范性文档**（normative document），不是**经验性研究**（empirical study）。它没有对任何样本库执行检索、纳排、编码或统计。Appendix 3 给出的是 protocol 模板（即"将来应这样做"），不是已执行结果。

### 2.3 原文"字段"来自哪里？

原文的结构化内容来源于以下 **guideline 定义型来源**，不是来自于对 primary studies 的 empirical extraction：

| 结构化内容 | 来源性质 | 证据锚点 |
|---|---|---|
| PICOC 五元组 | 改编自 Petticrew & Roberts 的医学 guideline 框架 | §5.3.2, Page 10--13 |
| 流程阶段三步法 | 综合自 Cochrane、NHS CRD、Aus NHMRC 等医学 SLR 指南 | §1.1, Page 1 |
| Table 5 质量核对清单 | 聚合自 [10][11][12][19][25] 等已有的 empirical study quality 评估文献 | §6.3.2, Page 25--27 |
| Table 6 质性研究质量清单 | 聚合自 [12][25][11] | §6.3.2, Page 28 |
| Table 8 报告结构模板 | 基于 [19] 的建议 | §7.2, Page 42--43 |
| Appendix 3 Protocol 模板 | 作者自己设计的 Tertiary Review 示例 | Appendix 3, Page 55--57 |
| Appendix 2 DARE 评分列表 | 对 20 篇已有 SE SLR 的摘要性评分（不是本文的系统样本） | Appendix 2, Page 50--54 |

### 2.4 RQ 与"样本单位"的关系

原文没有自己的 empirical RQ（它不回答"SLR 在 SE 中如何如何"这类问题）。但是：

- 原文 §5.3 定义了一个 RQ **分类框架**（五类 SE 问题类型）和 RQ **结构化模板**（PICOC）。这是 guideline 的元级别定义，不是该 guideline 自身的研究问题。
- Appendix 3 的 Tertiary Review Protocol 给出了一个具体 RQ 例子（4 个 RQ about EBSE activity），但这个 protocol 本身是示例模板，不是已执行结果。
- 因此：**原文的维度结构以"应如何定义 RQ"为根**，而不是"我们通过 RQ 发现了什么"。

### 2.5 降级策略

本文属于 **guideline 降级**：无系统样本库、无 empirical 统计结果。按 `GUIDE.md` §8.1，本文入 **方法学参考池**（不是主统计池），证据角色为 `guideline_methodology_seed`。可迁移内容限于：

1. **流程阶段 / 程序组件**作为 Paper2 方法流程的 boundary anchor。
2. **PICOC 框架**作为 RQ 维度初始化的 methodological seed。
3. **质量核对清单（Table 5 / Table 6）**作为 Paper2 质量评价维度的候选 heuristic。
4. **报告结构模板（Table 8）**作为 Paper2 输出物结构约束的 candidate schema。
5. **Appendix 3 Protocol 字段列表**作为 Paper2 agent-protocol schema 的初始化参考。

---

## 3. 原生样本编码维度树 / 维度森林

如前判定，本文没有以 primary study 为样本单位的编码树。以下复原的是该 guideline 自身的 **流程 / 结构化框架维度树**。这棵树以"SLR Guideline 的规范体系"为根。

```
[dim-kitchenham-charters-2007-slr-guidelines-root] SLR 方法学 Guideline 规范体系
│
├── [dim-kitchenham-charters-2007-slr-guidelines-process] SLR 过程阶段
│   ├── [dim-kitchenham-charters-2007-slr-guidelines-process-planning] 阶段1：Planning（§5）
│   │   ├── [leaf-kc2007-planning-need] 是否需要系统综述（review need justification）
│   │   ├── [leaf-kc2007-planning-commissioning] 委托与授权（commissioning a review, §5.2）
│   │   ├── [leaf-kc2007-planning-rq-type] 研究问题类型（§5.3.1：5 类 SE 问题类型）
│   │   │   ├── [leaf-kc2007-rq-type-effect] 评估 SE 技术/方法/工具的效应
│   │   │   ├── [leaf-kc2007-rq-type-frequency] 评估项目开发因素的频率或比率
│   │   │   ├── [leaf-kc2007-rq-type-cost-risk] 识别与技术关联的成本和风险因素
│   │   │   ├── [leaf-kc2007-rq-type-impact] 识别技术对可靠性/性能/成本模型的影响
│   │   │   └── [leaf-kc2007-rq-type-cost-benefit] 采用特定 SE 技术的成本效益分析
│   │   ├── [dim-kc2007-rq-structure-picoc] PICOC 研究问题结构框架（§5.3.2）
│   │   │   ├── [leaf-kc2007-picoc-population] Population：受干预影响的群体（SE 角色 / 经验级别 / 应用领域 / 行业组）
│   │   │   ├── [leaf-kc2007-picoc-intervention] Intervention：被评估的 SE 方法/工具/技术/程序
│   │   │   ├── [leaf-kc2007-picoc-comparison] Comparison：对照技术/方法（需充分描述，仅写"not using the intervention"不够）
│   │   │   ├── [leaf-kc2007-picoc-outcome] Outcome：对实践者重要的因子（可靠性、成本、上市时间等，慎用替代度量 surrogate measures）
│   │   │   └── [leaf-kc2007-picoc-context] Context：比较发生的场景（学界 vs 业界、参与者类型、任务规模）
│   │   ├── [leaf-kc2007-planning-protocol] Review Protocol 开发（§5.4）
│   │   └── [leaf-kc2007-planning-protocol-eval] Protocol 评价（§5.5）
│   │
│   ├── [dim-kitchenham-charters-2007-slr-guidelines-process-conducting] 阶段2：Conducting（§6）
│   │   ├── [dim-kc2007-conducting-search] 研究识别 / 检索（§6.1）
│   │   │   ├── [leaf-kc2007-search-strategy] 检索策略生成（search string, digital libraries, manual search）
│   │   │   ├── [leaf-kc2007-search-bias] 发表偏倚处理（§6.1.2）
│   │   │   ├── [leaf-kc2007-search-bib-mgmt] 文献管理与文档检索（§6.1.3）
│   │   │   └── [leaf-kc2007-search-documentation] 检索文档化（§6.1.4）
│   │   ├── [dim-kc2007-conducting-selection] 研究筛选（§6.2）
│   │   │   ├── [leaf-kc2007-selection-criteria] 纳入/排除标准（§6.2.1）
│   │   │   ├── [leaf-kc2007-selection-process] 筛选流程（§6.2.2）
│   │   │   └── [leaf-kc2007-selection-reliability] 纳入决策的信度（§6.2.3）
│   │   ├── [dim-kc2007-conducting-quality] 研究质量评价（§6.3）
│   │   │   ├── [dim-kc2007-quality-quant-checklist] Table 5 定量研究质量核对清单（33 项，分 Design/Conduct/Analysis/Conclusions 四阶段）
│   │   │   ├── [dim-kc2007-quality-qual-checklist] Table 6 质性研究质量核对清单（18 项）
│   │   │   ├── [leaf-kc2007-quality-usage] 质量数据用途（辅助筛选 vs 辅助分析与综合，§6.3.3）
│   │   │   └── [leaf-kc2007-quality-limitations] 质量评价局限性（§6.3.4：报告不完整、不假设未报告即未做）
│   │   ├── [dim-kc2007-conducting-extraction] 数据抽取（§6.4）
│   │   │   ├── [leaf-kc2007-extraction-form-design] 抽取表设计（§6.4.1：需覆盖 general info + specific data items）
│   │   │   ├── [leaf-kc2007-extraction-procedure] 抽取流程（§6.4.2--§6.4.5）
│   │   │   └── [leaf-kc2007-extraction-lessons] 抽取经验教训（§6.4.6）
│   │   └── [dim-kc2007-conducting-synthesis] 数据综合（§6.5）
│   │       ├── [leaf-kc2007-synthesis-narrative] 叙述性综合（§6.5.1）
│   │       ├── [leaf-kc2007-synthesis-descriptive] 描述性综合 / 制表（§6.5.1--§6.5.4：SE 中最实用）
│   │       ├── [leaf-kc2007-synthesis-quantitative] 定量综合 / meta-analysis（§6.5.5）
│   │       ├── [leaf-kc2007-synthesis-qualitative] 质性综合（§6.5.6）
│   │       ├── [leaf-kc2007-synthesis-mixed] 混合方法综合（§6.5.7）
│   │       └── [leaf-kc2007-synthesis-lessons] 综合经验教训（§6.5.8）
│   │
│   └── [dim-kitchenham-charters-2007-slr-guidelines-process-reporting] 阶段3：Reporting（§7）
│       ├── [leaf-kc2007-reporting-dissemination] 传播策略（§7.1：学术期刊 + 实践者渠道）
│       ├── [dim-kc2007-reporting-structure] Table 8 SLR 报告结构模板（§7.2）
│       │   ├── [leaf-kc2007-report-title] Title（应指示为系统综述）
│       │   ├── [leaf-kc2007-report-authorship] Authorship（合作者署名标准）
│       │   ├── [leaf-kc2007-report-structured-abstract] Structured Abstract（Context, Objectives, Methods, Results, Conclusions）
│       │   ├── [leaf-kc2007-report-background] Background（综述必要性论证）
│       │   ├── [leaf-kc2007-report-review-questions] Review Questions（主 / 次 RQ）
│       │   ├── [leaf-kc2007-report-methods] Review Methods（Data sources, Study selection, Quality assessment, Data extraction, Data synthesis）
│       │   ├── [leaf-kc2007-report-included-excluded] Included and Excluded Studies（含排除理由）
│       │   ├── [leaf-kc2007-report-findings] Findings（primary studies 描述、定量总结、meta-analysis 细节）
│       │   ├── [leaf-kc2007-report-discussion] Discussion（主要发现、证据强度与弱点、与其他综述的关系、意义与适用范围）
│       │   └── [leaf-kc2007-report-conclusions] Conclusions（实践建议、未回答问题、未来研究方向）
│       ├── [leaf-kc2007-reporting-evaluation] 综述报告评价（§7.3：同行评议 / 专家 panel）
│       └── [leaf-kc2007-reporting-lessons] 报告经验教训（§7.4）
│
├── [dim-kitchenham-charters-2007-slr-guidelines-review-types] 综述类型定义
│   ├── [leaf-kc2007-type-slr] Systematic Literature Review（§2：完整 SLR，聚焦具体 RQ）
│   ├── [leaf-kc2007-type-sms] Systematic Mapping Study / Scoping Study（§8：宽泛覆盖、分类阶段、不需深度数据抽取）
│   └── [leaf-kc2007-type-tertiary] Tertiary Review（§2.5.2：二级研究的系统综述，方法论同 SLR）
│
├── [dim-kitchenham-charters-2007-slr-guidelines-protocol-template] Appendix 3 Protocol 模板字段（Tertiary Review 实例）
│   ├── [leaf-kc2007-protocol-background] Background / justification
│   ├── [leaf-kc2007-protocol-rqs] Research Questions（4 RQs）
│   ├── [leaf-kc2007-protocol-search] Search Strategy（digital libraries, journals, conferences, individual researchers）
│   ├── [leaf-kc2007-protocol-selection] Study Selection Criteria（含 inclusion / exclusion）
│   ├── [leaf-kc2007-protocol-quality] Quality Assessment（4-item Y=1 / P=0.5 / N=0 scoring）
│   ├── [leaf-kc2007-protocol-extraction] Data Extraction Variables（10 fields: source, year, type, scope, topic, authors/affiliation, RQ/issue, EBSE reference, practitioner guidelines, #primary studies, summary, quality score）
│   ├── [leaf-kc2007-protocol-analysis] Data Analysis Plan（tabulation + counting + trend identification）
│   └── [leaf-kc2007-protocol-dissemination] Dissemination Plan
│
└── [leaf-kc2007-appendix2-dare] Appendix 2：20 篇 SE SLR 的 DARE 评分（不是本文的系统样本库，是现有综述的质量摘要）
```

**说明**：以上树不是论文的 empirical 维度树——本文没有 empirical 样本。它复原的是该 guideline 自身的"规范体系树"：流程阶段为干、程序组件为枝、结构化框架（PICOC / Quality Checklist / Report Template / Protocol Template）为叶子。这种树只能进入 A2a 的 methodological seed pool，不能作为 main statistical pool 的维度来源。

由于本文是 guideline，以下叶子维度表只覆盖**有明确取值空间的叶子**（PICOC、Protocol Template），以及**有明确划分的流程组件**。Quality Checklist 等大型核对清单的各子项不逐一展开（那是 A2a 精核任务）。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-kc2007-planning-need` | 是否需要系统综述 | `dim-*-planning` | §5.1 | 判断是否启动 SLR 的论证条件 | 自由文本加理由（没有固定枚举） | 自由文本加理由 | 不适用（guideline 不填值） | 不适用 | Paper2 可用于定义 agent SLR 的"启动门条件" | §5.1, Page 7 | 门条件语义需按 agent 上下文重定义 |
| `leaf-kc2007-rq-type-effect` | SE 技术效应评估 | `dim-*-planning` | §5.3.1 问题类型 1 | 评估 SE 技术/方法/工具的效应（effect） | 自包含类型：是/否该 RQ 属于此类型 | 布尔 | 不适用 | 不适用 | Paper2 的 RQ type classification schema | §5.3.1, Page 9 | 五类不完全覆盖 LLM 时代的 RQ 类型 |
| `leaf-kc2007-rq-type-frequency` | 项目因素频率/比率评估 | `dim-*-planning` | §5.3.1 问题类型 2 | 评估技术采纳率或项目成败率 | 同上 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | 同上 |
| `leaf-kc2007-rq-type-cost-risk` | 成本/风险因素识别 | `dim-*-planning` | §5.3.1 问题类型 3 | 识别与技术关联的成本和风险因素 | 同上 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | 同上 |
| `leaf-kc2007-rq-type-impact` | 技术对非功能属性的影响 | `dim-*-planning` | §5.3.1 问题类型 4 | 识别技术对可靠性/性能/成本模型的影响 | 同上 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | 同上 |
| `leaf-kc2007-rq-type-cost-benefit` | 成本效益分析 | `dim-*-planning` | §5.3.1 问题类型 5 | 特定 SE 技术的成本效益分析 | 同上 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | 同上 |
| `leaf-kc2007-picoc-population` | Population | `dim-kc2007-rq-structure-picoc` | §5.3.2, Page 11 | 受干预影响的群体定义 | SE 角色 / 经验级别 / 应用领域 / 行业组（非穷举） | 层级枚举（非穷举） | 不需限制 population 直到考虑实践影响（SE 特殊性：primary study 少） | 不适用 | Paper2 RQ 模板初始化 | §5.3.2, Page 11 | 类别是 ILUSTRATIVE，不是 complete taxonomy |
| `leaf-kc2007-picoc-intervention` | Intervention | `dim-kc2007-rq-structure-picoc` | §5.3.2, Page 11 | 被评估的 SE 方法/工具/技术/程序 | 自由文本（SE methodology/tool/technology/procedure） | 自由文本加理由 | 不适用 | 不适用 | Paper2 RQ 模板初始化 | 同上 | 同上 |
| `leaf-kc2007-picoc-comparison` | Comparison | `dim-kc2007-rq-structure-picoc` | §5.3.2, Page 11 | 对照技术；"not using the intervention"不够；需区分 training effect confound | 自由文本 | 自由文本加理由 | 不适用 | 不适用 | Paper2 RQ 模板初始化 | 同上 | 同上 |
| `leaf-kc2007-picoc-outcome` | Outcome | `dim-kc2007-rq-structure-picoc` | §5.3.2, Page 11--12 | 对实践者重要的结果因子（可靠性、成本、上市时间）；警告 surrogate measures | 自由文本 | 自由文本加理由 | 不适用 | 不适用 | Paper2 RQ 模板初始化；surrogate measure 警告可迁移为效度指标 | 同上 | 同上 |
| `leaf-kc2007-picoc-context` | Context | `dim-kc2007-rq-structure-picoc` | §5.3.2, Page 12 | 比较发生的场景：学界/业界、参与者类型、任务规模 | 学界 / 业界；practitioners / academics / consultants / students；small/large scale | 层级枚举（非穷举） | 不适用 | 不适用 | Paper2 RQ 模板初始化；可为 Paper2 中 SE 实验的生态效度（ecological validity）提供维度 | 同上 | 同上 |
| `leaf-kc2007-quality-usage` | 质量数据用途 | `dim-kc2007-conducting-quality` | §6.3.3, Page 28 | 质量数据的两类用途：辅助筛选 vs 辅助分析 | "辅助筛选" / "辅助分析" / 两者皆有 | 完整枚举（3 值） | 不适用 | 不适用 | Paper2 质量评价策略维度 | §6.3.3, Page 28 | 对 agent SLR 的 quality gate 设计有启发但非直接模板 |
| `leaf-kc2007-synthesis-narrative` | 叙述性综合 | `dim-kc2007-conducting-synthesis` | §6.5.1, Page 34 | 以文字叙述组织 findings 的综合方式 | 自包含类型（是/否采用） | 布尔 | 不适用 | 不适用 | Paper2 synthesis method classification | §6.5.1, Page 34 | — |
| `leaf-kc2007-synthesis-descriptive` | 描述性/制表综合 | 同上 | §6.5.1--§6.5.4 | 以表格汇总 primary study 信息的综合方式（SE 中最实用） | 自包含类型 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | — |
| `leaf-kc2007-synthesis-quantitative` | 定量综合 / meta-analysis | 同上 | §6.5.5, Page 36 | 用统计方法聚合 quantitative 结果的综合方式 | 自包含类型 | 布尔 | 不适用 | 不适用 | 同上 | 同上 | — |
| `leaf-kc2007-type-slr` | SLR | `dim-*-review-types` | §2.4, Page 4 | 聚焦具体 RQ 的完整系统综述 | 自包含类型 | 布尔 | 不适用 | 不适用 | Paper2 综述类型分类 schema | §2.4, Page 4 | — |
| `leaf-kc2007-type-sms` | Systematic Mapping Study | 同上 | §8, Page 44 | 宽泛覆盖、分类阶段、不需深度数据抽取 | 自包含类型 | 布尔 | 不适用 | 不适用 | 同上 | §8, Page 44 | — |
| `leaf-kc2007-type-tertiary` | Tertiary Review | 同上 | §2.5.2, Page 5 | 二级研究的系统综述 | 自包含类型 | 布尔 | 不适用 | 不适用 | 同上 | §2.5.2, Page 5 | — |
| `leaf-kc2007-protocol-extraction` | Protocol 数据抽取变量 | `dim-*-protocol-template` | Appendix 3, Page 56 | 10 字段的 data extraction form | 1. source; 2. year; 3. classification (type, scope); 4. main SE topic; 5. authors/affiliation; 6. RQ/issue; 7. EBSE paper reference; 8. practitioner guidelines; 9. #primary studies; 10. quality score | 完整枚举（10 字段列表） | 不做次级数据抽取 | 不适用 | Paper2 的 agent extraction schema 初始化参考 | Appendix 3, Page 56 | 这是针对 EBSE tertiary review 设计的专属字段，非通用 |
| `leaf-kc2007-protocol-quality` | Protocol 质量评分方案 | `dim-*-protocol-template` | Appendix 3, Page 55 | 4 项 Y/P/N 评分（Y=1, P=0.5, N=0） | Q1 inclusion criteria, Q2 search coverage, Q3 quality assessment, Q4 per-paper detail | 数值（0--4 范围） | 不适用 | 不适用 | Paper2 质量评分维度种子 | Appendix 3, Page 55 | 仅 4 项粗粒度评分 |
| `leaf-kc2007-selection-reliability` | 纳入决策信度 | `dim-kc2007-conducting-selection` | §6.2.3, Page 20 | 多评审员一致性的必要性和 Kappa 统计 | Kappa statistic / 一致性讨论 | 数值或自由文本 | 不适用 | 不适用 | Paper2 agent 评审一致性指标 | §6.2.3, Page 20 | — |

---

## 5. 关系边表

本文是 guideline，它的"关系"是**规范依赖关系**（normative dependency），不是 empirical 统计关系（如"样本 A 的字段 X 与字段 Y 之间存在相关性"）。以下列出的关系边是从 guideline 的流程逻辑和规范层级中提取的。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `edge-kc2007-rq-drives-protocol` | `dim-kc2007-rq-structure-picoc` | 驱动 / 决定 | `leaf-kc2007-planning-protocol` | Protocol 的要素由 RQ 决定 | 不适用 | §5.3→§5.4, Page 12: "The most important activity during planning is to formulate the research question(s). A review protocol specifies the methods..." | Paper2 的 RQ→Protocol 因果链建模 |
| `edge-kc2007-protocol-drives-search` | `leaf-kc2007-planning-protocol` | 驱动 / 约束 | `dim-kc2007-conducting-search` | 检索策略由 Protocol 中的 RQ 和 search plan 定义 | 不适用 | §6.1, Page 14: "The aim of a systematic review is to find as many primary studies... using an unbiased search strategy. The rigour of the search process is one factor that distinguishes systematic reviews from traditional reviews." | Paper2 的 protocol→search 过程建模 |
| `edge-kc2007-search-feeds-selection` | `dim-kc2007-conducting-search` | 输入 / 供给 | `dim-kc2007-conducting-selection` | 检索结果集是筛选的输入 | 不适用 | §6.1→§6.2, 结构顺序 | Paper2 pipeline 建模 |
| `edge-kc2007-selection-feeds-quality` | `dim-kc2007-conducting-selection` | 输入 / 供给 | `dim-kc2007-conducting-quality` | 通过筛选的 study 进入质量评价 | 不适用 | §6.2→§6.3, 结构顺序 | 同上 |
| `edge-kc2007-quality-feeds-extraction` | `dim-kc2007-conducting-quality` | 输入 / 分层 | `dim-kc2007-conducting-extraction` | 质量数据可用于分层分析 | 不适用 | §6.3.3, Page 28: "quality data are used to identify subsets of the primary study to investigate whether quality differences are associated with different primary study outcomes" | Paper2 quality-stratified analysis 建模 |
| `edge-kc2007-extraction-feeds-synthesis` | `dim-kc2007-conducting-extraction` | 输入 / 供给 | `dim-kc2007-conducting-synthesis` | 抽取的数据是综合的输入 | 不适用 | §6.4→§6.5, 结构顺序；§6.5 "The data synthesis activities should be specified in the review protocol" | Paper2 pipeline 建模 |
| `edge-kc2007-synthesis-feeds-reporting` | `dim-kc2007-conducting-synthesis` | 输入 / 供给 | `dim-kitchenham-charters-2007-slr-guidelines-process-reporting` | 综合结果是报告的输入 | 不适用 | §7, Page 39: "The final phase of a systematic review involves writing up the results" | Paper2 pipeline 建模 |
| `edge-kc2007-report-structure-maps-to-process` | `dim-kc2007-reporting-structure` (Table 8) | 映射 / 对应 | `dim-kitchenham-charters-2007-slr-guidelines-process` | Table 8 各节对应 SLR 流程各阶段 | 不适用 | Table 8 (§7.2) 的 structure vs §5--§6 的 process；两者在 Background→RQ→Methods→Findings→Discussion 线上平行 | Paper2 报告模板的流程耦合 |
| `edge-kc2007-picoc-maps-to-extraction` | `dim-kc2007-rq-structure-picoc` | 映射 / 驱动 | `dim-kc2007-conducting-extraction` | PICOC 的五个维度应映射到 data extraction form 中 | 不适用 | §6.4.1, Page 29--30: extraction form 设计原则建议覆盖 general info + 能回答 RQ 的 specific data items | Paper2 extraction schema 的字段来源 |
| `edge-kc2007-protocol-template-is-instance` | `dim-kitchenham-charters-2007-slr-guidelines-protocol-template` | 实例化 / 属于 | `leaf-kc2007-planning-protocol` | Appendix 3 是 Protocol 概念的一个具体实例 | 不适用 | Appendix 3 标题: "Protocol for a Tertiary study", §5.4 Page 13: "An example of protocol for a tertiary review is given in Appendix 3" | Paper2 protocol instantiation 建模 |

当无法确认关系时（如 PICOC 到 study selection criteria 之间有逻辑联系但未在原文中显式声明），不列为关系边。以上关系边全部可从原文的流程顺序和显式说明中直接推断（多数来自 § 编号的线性顺序）。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段 / 统计表支持的统计观察

**本文没有统计观察。** 原因：本文是 guideline，不是 empirical study。它没有自己的样本库、没有数值数据、没有定量分析结果。

Appendix 2 中的 20 篇 DARE 评分只是摘要演示，不是本文的系统统计结果。Appendix 3 是 protocol 模板（将来时），不是已执行结果（过去时）。

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding

以下是从 guideline 中提取的 **规范主张**（normative claims / methodological recommendations），它们可以视为 Paper2 的候选启发式（candidate heuristic），但绝不能写成"paper X found that..."——因为原文没有"find"：

| # | 候选启发式 | 来源章节 | Paper2 可迁移用途 | 绝不能迁移为 |
|---|---|---|---|---|
| CH1 | SLR 必须从明确的 RQ 出发，RQ 是 protocol 中最重要的元素 | §5.3, Page 9 | Paper2 agent-SLR 的 RQ-first 约束 | 不迁移为"SE SLR 普遍以 RQ 驱动"这一实证发现 |
| CH2 | RQ 可按 PICOC 结构化，但 SE 领域 primary study 少，不宜过早限制 population | §5.3.2, Page 11 | Paper2 RQ schema 设计 | 同上 |
| CH3 | Protocol 必须预先定义并在 review 中记录所有偏离 | §5.4--§5.6, Page 12--13 | Paper2 protocol fidelity 审计维度 | 同上 |
| CH4 | 质量评价可用于辅助筛选（pre-extraction）或辅助分析（post-extraction），两种方式不互斥 | §6.3.3, Page 28 | Paper2 quality gate 设计 | 同上 |
| CH5 | 不应因为"未报告"就假设"未做"——应联系作者核实，或将"未报告"记为限制 | §6.3.4, Page 29 | Paper2 的"缺失值语义"纪律 | 同上 |
| CH6 | 数据综合方式应依据纳入文献的异质性选择：narrative / tabular / quantitative / qualitative / mixed；SE 中最实用的是 tabulation | §6.5, Page 34--39 | Paper2 synthesis method 分类 schema | 同上 |
| CH7 | Mapping study 与 SLR 的主要区别在于：更宽的 RQ、更不聚焦的检索、分类而非深度抽取、摘要性分析 | §8, Page 44 | Paper2 review type classification | 同上 |
| CH8 | 系统综述报告应区分技术报告（完整细节）和期刊/会议论文（缩减版），后者必须引用完整技术报告 | §7.2, Page 40 | Paper2 输出制品链设计 | 同上 |

### 6.3 对 Paper2 可迁移的方法学启发

| # | 启发 | 对 Paper2 的具体用途 |
|---|---|---|
| M1 | PICOC 框架 | 可用于定义 Paper2 中 agent-SLR 的 RQ 模板：每个纳入的 SLR/SMS 可按 PICOC 五元组编码其 RQ，作为维度树的 five mandatory leaves |
| M2 | Table 5 + Table 6 的质量核对清单 | 可作为 Paper2 中评估 agent-SLR 自身 quality 的 checklist 种子；33+18=51 项需在 A2a 精核后选用于 agent 上下文 |
| M3 | Appendix 3 Protocol 模板的 10 字段 extraction form | 可作为 Paper2 data extraction schema 的初始字段集合，再通过 A2a 扩库补充 SLR-specific fields |
| M4 | 流程三步法（Planning → Conducting → Reporting） | 可直接映射为 Paper2 agent pipeline 的三阶段结构 |
| M5 | "Piloting the research protocol is essential"（§5.6） | 支持 Paper2 中 pilot study 设计的必要性论证 |
| M6 | "Review teams need to keep a detailed record of decisions"（§7.4） | 支持 Paper2 agent trace/audit 设计的必要性论证 |

### 6.4 绝不能迁移的领域结论

- 本文关于 SE effort estimation、cross-company vs within-company models、expert judgment vs model-based estimation 的具体案例（来自 Kitchenham et al. [21] 和 Jørgensen [17] 的例子）不能迁移为 Paper2 的领域发现。
- Appendix 2 中 20 篇 SE SLR 的 DARE 评分和主题分布不是本文的系统发现，不能作为"SE SLR 质量分布"的证据。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 C 级（必须修复）

#### C1 — 维度树复原需以"原文流程树 + 结构化框架树"替代"六叶通用投影"
**问题**：当前 `review.md` 的 §5 "A1-M0--M6 脚手架元维度贡献" 表及 A.3 叶子映射仍以 A1-M0（研究意图）→ A1-M1（语料收集）→ ... → A1-M6（报告结构）的六叶通用投影作为本文的"维度树"。但本文是 guideline，不是 empirical SLR/SMS/tertiary。其原生结构应以上述 §3 的"流程阶段树 + 结构化框架树"为准。

**修复建议**：
1. 将 `review.md` 的维度树章节重建为"SLR 过程阶段维度树"（根 = SLR Guideline 规范体系，干 = Planning / Conducting / Reporting 三阶段，叶 = §3 和 §4 中的叶子节点）。
2. 保留 A1-M0--M6 投影表作为 §5 "跨论文投影贡献"，但标题改为"对 A1-M0--M6 脚手架元维度的贡献（投影层）"，并在表头显式声明"以下为跨论文投影，非本文原生树"。
3. 在维度树节开头加一句："本文是 guideline，无 empirical 样本编码树。以下复原的是该 guideline 自身的流程 / 结构化框架维度树，属于降级树。"

#### C2 — A.2 证据账本缺少页码精确锚定
**问题**：当前 A.2 账本中 `EV-kitchenham-charters-2007-slr-guidelines-002`（"原文结构证据"）和 `EV-kitchenham-charters-2007-slr-guidelines-003`（"原文叶子 / 字段 / 取值证据"）均为泛定位。所有结论映射均回链这两个泛证据，违反了 `pattern-field-schema.md` §8.4 的"支撑证据必须回链 A.2"和"A.2 证据标识必须精确可定位"规则。

**修复建议**：
1. 将 A.2 的 2 条泛证据拆分为至少 12 条精确证据（对应上文 §1 的 12 个锚点），每条包含原文页码（Page number）、章节编号、表图编号和短引。
2. 对 Table 5（33 项）、Table 6（18 项）、Table 8、Appendix 2、Appendix 3 各分配独立证据标识。
3. 更新 `EV-kitchenham-charters-2007-slr-guidelines-004`（"降级与规范证据"）为基于以上精确锚点的降级声明，并逐条标注"不是样本库"的原文反证。

#### C3 — 叶子维度表需弃用通用六叶接口叶子，替换为原文原生叶
**问题**：当前 A.3 叶子映射（C05--C07）使用"方法 / 技术 / 干预分类""评价、证据与复现资产""统计观察与候选发现"等泛化叶子，这些是从 A1-M0--M6 投影过来的人造接口，不是原文自有叶子。

**修复建议**：
1. 用上文 §4 的叶子维度表替换当前 A.3 的叶子映射。
2. 已有叶子映射（C05--C07）降级为 `do_not_use` 或归档为"投影层候选"。
3. 新增叶子 `leaf-kc2007-picoc-*`、`leaf-kc2007-quality-*`、`leaf-kc2007-synthesis-*`、`leaf-kc2007-type-*`、`leaf-kc2007-protocol-*` 等系列。

### 7.2 I 级（重要，建议修复）

#### I1 — SUMMARY 当前表中"样本单位 / 样本数量 / 原生树类型 / 统计池资格"列需要修正
**问题**：需确认 `SUMMARY.md` 中该论文所在行的"原生树类型"被标记为"降级树（guideline，无系统样本库）"而非"单树"或"维度森林"；"样本单位"写为"不适用"或"SLR 流程阶段与结构化框架组件"；"样本数量"写为"N/A"。

#### I2 — "快速结论卡片"的综述类型措辞有误导风险
**问题**：当前卡片中写 `综述类型 | SLR guideline；同时定义 mapping study 与 tertiary review`，但更精确的写法应为 `方法学 guideline（EBSE Technical Report）；定义 SLR、SMS 和 tertiary review 的概念与流程`。当前写法可能让后续 agent 误以为本文有综述结果。

**修复建议**：改为 `guideline（方法学技术报告，非执行后的 SLR/SMS/tertiary）`。`schema 历史观察` 可以保留。

#### I3 — 缺少对 PICOC 五个维度的专门抽取和 A.2 锚定
**问题**：当前 `review.md` 完全没有提及 PICOC。但 PICOC 是本文对 SLR community 影响力最大的结构化框架之一，且对 Paper2 的 RQ schema 设计有直接启发。缺失 PICOC 意味着 `review.md` 严重不完整。

**修复建议**：在 §3（对 PR-A1 schema 的启发）中新增一条"PICOC 可作为 RQ 维度初始化框架，五个维度（Population, Intervention, Comparison, Outcome, Context）可分别映射为 Paper2 的五个候选叶子"。

### 7.3 M 级（建议，可稍后修复）

#### M1 — §2 "六类 pattern 抽取"可重构为"guideline 规范结构抽取"
当前 §2 仍套用 empirical SLR 的六类 pattern 框架（RQ pattern / dimension pattern / finding pattern / evidence presentation pattern / validity threat pattern / report structure pattern），这对 guideline 并不自然。建议改为三部分："SLR 流程阶段与组件抽取"（对应 process 树）、"结构化框架抽取"（PICOC / Quality / Report / Protocol 模板）、"规范主张与候选启发式抽取"（对应 §6.2 中的 8 条 CH）。

#### M2 — A.1 文件来源表需补充 paper.pdf 的核验状态
当前 A.1 未列出 `paper.pdf`。建议新增一行：`paper.pdf | PDF 原文 | 全文 | needs_manual_check | 表格编号、页码、版权页、Appendix 2 评分细节待人工核对`。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| `EV-kc2007-001` | `paper_content.txt` | §2.4 (Page 4) | Paragraph starting "A systematic literature review..." | SLR 三阶段：planning → conducting → reporting | definition | medium | `[dim-*-root]`, `[dim-*-process]` | 否 | 这是 guideline 的定义，不是 empirical finding |
| `EV-kc2007-002` | `paper_content.txt` | §5.3.1 (Page 9--10) | Six health care question types → 5 SE adaptations | 五类 SE 问题类型：effect / frequency / cost-risk / impact / cost-benefit | taxonomy | medium | `[leaf-kc2007-rq-type-*]` (5 叶) | 否 | 五类来自医学框架的改编，可能不完全覆盖 agent-based SLR 的 RQ 类型 |
| `EV-kc2007-003` | `paper_content.txt` | §5.3.2 (Page 10--13) | "More recently Petticrew and Roberts suggest using the PICOC..."; 5 paragraphs per dimension | PICOC = Population, Intervention, Comparison, Outcome, Context；每维 SE 实例定义 | definition + taxonomy | medium | `[dim-kc2007-rq-structure-picoc]`, `[leaf-kc2007-picoc-*]` (5 叶) | 否 | 文中类别是 illustrative 不是 exhaustive |
| `EV-kc2007-004` | `paper_content.txt` | §5.4 (Page 12--13) | "A review protocol specifies the methods..." 及其组件列表 | Protocol 必须包含：background, RQs, search strategy, selection criteria, quality checklists, data extraction, synthesis, timetable, dissemination | definition | medium | `[leaf-kc2007-planning-protocol]` | 否 | — |
| `EV-kc2007-005` | `paper_content.txt` | §5.6 (Page 14) | Three lessons: revise questions, train team, pilot protocol | "Piloting the research protocol is essential" | author_claim | medium | `[leaf-kc2007-planning-protocol]` | 否 | 这是经验教训，不是实证证据 |
| `EV-kc2007-006` | `paper_content.txt` | §6.3.2 (Page 25--27) | Table 5: Summary Quality Checklist for Quantitative Studies (33 items) | 33 项质量检查项，按 Design / Conduct / Analysis / Conclusions 四阶段组织 | extraction_field | medium | `[dim-kc2007-quality-quant-checklist]` | 是（需核验表格编号、列对齐、33 项完整性和来源脚注在 PDF 版面的呈现） | 来源聚合自 [10][11][12][19][25]；不能确认此聚合的权威性 |
| `EV-kc2007-007` | `paper_content.txt` | §6.3.2 (Page 28) | Table 6: Checklist for qualitative studies (18 items) | 18 项质性研究质量检查项 | extraction_field | medium | `[dim-kc2007-quality-qual-checklist]` | 是（需核验表格编号和完整 18 项） | 同上 |
| `EV-kc2007-008` | `paper_content.txt` | §6.3.3 (Page 28) | "quality data can be used in two rather different ways" | 质量数据用途：辅助筛选 / 辅助分析与综合 | definition | medium | `[leaf-kc2007-quality-usage]` | 否 | — |
| `EV-kc2007-009` | `paper_content.txt` | §6.3.4 (Page 28--29) | "it is tempting to assume that because something wasn't reported, it wasn't done. This assumption may be incorrect." | 缺失值语义纪律（不应该假设未报告 = 未做） | limitation + author_claim | medium | `[leaf-kc2007-quality-limitations]` | 否 | — |
| `EV-kc2007-010` | `paper_content.txt` | §6.4.1 (Page 29--30) | Extraction form 设计原则 | 需覆盖 general info + 能回答 RQ 的 specific data items；需 pilot | definition | medium | `[leaf-kc2007-extraction-form-design]` | 否 | — |
| `EV-kc2007-011` | `paper_content.txt` | §6.5 (Page 34--39) | Five synthesis approaches | Narrative / descriptive (tabular) / quantitative (meta-analysis) / qualitative / mixed | taxonomy | medium | `[leaf-kc2007-synthesis-*]` (5 叶) | 否 | — |
| `EV-kc2007-012` | `paper_content.txt` | §7.2 (Page 40--43) | Table 8: Structure and Contents of Reports of Systematic Reviews | 报告模板：Title → Authorship → Structured Abstract → Background → Review Questions → Methods → Results → Discussion → Conclusions | extraction_field | medium | `[dim-kc2007-reporting-structure]`, `[leaf-kc2007-report-*]` (10 叶) | 是（需核验 asterisk 标记和子节层级） | 基于 [19] 的建议改编 |
| `EV-kc2007-013` | `paper_content.txt` | §8 (Page 44--46) | "Systematic Mapping Studies... are designed to provide a wide overview..." | Mapping study 定义及其与 SLR 的四个区别 | definition | medium | `[leaf-kc2007-type-sms]` | 否 | — |
| `EV-kc2007-014` | `paper_content.txt` | §2.5.2 (Page 5) | "A tertiary review... uses exactly the same methodology as a systematic literature review" | Tertiary review 定义 | definition | medium | `[leaf-kc2007-type-tertiary]` | 否 | — |
| `EV-kc2007-015` | `paper_content.txt` | Appendix 3 (Page 55--57) | Full protocol text: Background, Research Questions, Search Strategy, Study Selection, Quality Assessment, Data Collection, Data Analysis, Dissemination | Protocol 模板实例；10 字段 extraction form；4 项 Y/P/N 评分 | artifact | medium | `[dim-*-protocol-template]`, `[leaf-kc2007-protocol-*]` (8 叶) | 是（需核验 Appendix 编号和 protocol 文本完整性） | 这是针对 EBSE tertiary review 的专属示例 |
| `EV-kc2007-016` | `paper_content.txt` | Appendix 2 (Page 50--54) | 20 SE SLR 的 DARE 评分列表 | 展示了如何使用 DARE 标准评价已有 SLR | artifact | weak（不是本文的系统统计结果，是附录示例） | `[leaf-kc2007-appendix2-dare]` | 是（需核验 20 篇条目是否在 PDF 中完整且与 content.txt 一致） | 不能作为 empirical evidence of SLR quality distribution |
| `EV-kc2007-017` | `bibtex.bib` + `metadata.json` | — | 技术报告元数据 | 出版形态：技术报告 EBSE-2007-01；非 peer-reviewed venue | metadata | strong | 根节点、统计池资格判定 | 否 | — |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| `clm-kc2007-guideline-not-empirical` | 本文是方法学 guideline / 技术报告，不是执行后的 SLR/SMS/tertiary empirical study；无系统样本库。 | boundary_anchor | `[dim-*-root]` | `EV-kc2007-017`, `EV-kc2007-001` | strong | `boundary_anchor` | 本文定义了 SLR/SMS/tertiary 概念框架，其定义本身是边界锚。 |
| `clm-kc2007-process-tree` | 本文的 SLR 流程分为 Planning → Conducting → Reporting 三阶段，每阶段包含确定子步骤。 | schema_seed | `[dim-*-process]` 及其子树 | `EV-kc2007-001`, `EV-kc2007-004`, `EV-kc2007-012` | medium | `schema_seed` | 流程是三阶段理想化抽象，真实 SLR 执行可能迭代。 |
| `clm-kc2007-picoc-framework` | PICOC（Population, Intervention, Comparison, Outcome, Context）是本文推荐的 RQ 结构化框架，改编自 Petticrew & Roberts 的医学 guideline。 | schema_seed | `[dim-kc2007-rq-structure-picoc]`, `[leaf-kc2007-picoc-*]` (5 叶) | `EV-kc2007-003` | medium | `schema_seed` | 五元组的 SE 实例是 illustrative 不是 exhaustive；Paper2 需根据目标领域补充分类。 |
| `clm-kc2007-quality-checklists` | 本文提供 Table 5（33 项定量）和 Table 6（18 项质性）的质量核对清单，来自 [10][11][12][19][25] 的聚合。 | schema_seed | `[dim-kc2007-quality-quant-checklist]`, `[dim-kc2007-quality-qual-checklist]` | `EV-kc2007-006`, `EV-kc2007-007` | medium | `schema_seed` | 清单全文未在 PDF 版面核验；聚合来源的权威性待评估。 |
| `clm-kc2007-quality-usage-dual` | 质量数据可辅助筛选或辅助分析，两种方式可共存。 | schema_seed | `[leaf-kc2007-quality-usage]` | `EV-kc2007-008` | medium | `schema_seed` | — |
| `clm-kc2007-missing-reporting-not-missing-doing` | "未报告 ≠ 未做"是质量评价的核心纪律。 | schema_seed | `[leaf-kc2007-quality-limitations]` | `EV-kc2007-009` | medium | `schema_seed` | 这条是规范建议，不是实证证据。 |
| `clm-kc2007-synthesis-taxonomy` | 本文定义了五种综合方式：narrative / descriptive-tabular / quantitative-meta-analysis / qualitative / mixed；SE 中最实用的是 tabulation。 | schema_seed | `[leaf-kc2007-synthesis-*]` (5 叶) | `EV-kc2007-011` | medium | `schema_seed` | — |
| `clm-kc2007-report-template` | Table 8 提供 SLR 报告的完整结构模板，从 Title 到 References & Appendices 共 10 个子节。 | schema_seed | `[dim-kc2007-reporting-structure]`, `[leaf-kc2007-report-*]` (10 叶) | `EV-kc2007-012` | medium | `schema_seed` | 需 PDF 版面核验 asterisk 标记和子节层级。 |
| `clm-kc2007-review-type-trilogy` | 本文区分 SLR、Systematic Mapping Study 和 Tertiary Review 三种综述类型。 | schema_seed | `[leaf-kc2007-type-slr]`, `[leaf-kc2007-type-sms]`, `[leaf-kc2007-type-tertiary]` | `EV-kc2007-013`, `EV-kc2007-014` | medium | `schema_seed` | 三种类型的定义来自 guideline 构造，不是来自 empirical taxonomy derivation。 |
| `clm-kc2007-protocol-template` | Appendix 3 提供 Tertiary Review Protocol 的完整实例（Background → 4 RQs → Search → Selection → Quality → 10-field Extraction → Analysis → Dissemination）。 | schema_seed | `[dim-*-protocol-template]`, `[leaf-kc2007-protocol-*]` (8 叶) | `EV-kc2007-015` | medium | `schema_seed` | 这是针对 EBSE tertiary review 的专属示例，非通用 protocol schema。 |
| `clm-kc2007-mapping-vs-slr` | Mapping study 与 SLR 的主要区别：更宽 RQ、更不聚焦检索、分类阶段而非深度抽取、摘要性分析。 | schema_seed | `[leaf-kc2007-type-sms]` | `EV-kc2007-013` | medium | `schema_seed` | — |
| `clm-kc2007-pilot-essential` | "Piloting the research protocol is essential" | candidate_heuristic | `[leaf-kc2007-planning-protocol]` | `EV-kc2007-005` | medium | `candidate_finding` | 不可作为"SLR pilot 频率"的实证发现，只能作为方法学建议。 |
| `clm-kc2007-decision-audit-trail` | "Review teams need to keep a detailed record of decisions made throughout the review process" (§7.4) | candidate_heuristic | `[dim-*-process]` | `EV-kc2007-014` (间接) | weak | `candidate_finding` | 同上。 |
| `clm-kc2007-appendix2-is-demo` | Appendix 2 的 20 篇 DARE 列表是评分标准的演示案例，不是本文的系统样本库。 | boundary_anchor | `[leaf-kc2007-appendix2-dare]` | `EV-kc2007-016` | strong | `boundary_anchor` | — |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件与采用的原则

| 技能文件 | 采用的关键原则 |
|---|---|
| `ai-research-writing-skill/SKILL.md` | **Evidence gate**（"every major claim must be backed by... verified citations"）、**Claim gate**（"no unsupported strong claim"）、**Citation gate**（"no unverified BibTeX"）— 本审计严格遵守"证据不足则降级"，没有编造任何表格、页码或作者结论。 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 通用 reviewer 维度（Originality / Quality / Clarity / Significance / Reproducibility / Ethics）中的 **Quality/soundness**（"tie every strong claim to evidence"）和 **Constructive Specificity Standard**（"A reviewer-quality objection should be specific enough that an author can act on it"）— 本审计的所有返修建议都给出了文件、行号或章节级的精确定位。 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | **Claim Audit** 模板和 **Experiment Audit** 的"what research question does it answer? which main paper claim does it support?"— 本审计的 A.3 结论-证据映射按此原则构建。 |
| `research-planning/SKILL.md` | 研究计划四阶段方法（Overall Plan → Architecture Design → Logic Design → Configuration）中的 **"flag ambiguities explicitly rather than making assumptions"** — 本审计在 PICOC 类别 completeness、Table 5/6 聚合权威性等不确定之处均显式标注。 |
| `research-planning/references/planning-prompts.md` | 输出 schema 要求的结构化字段定义和依赖声明 — 影响本审计叶子维度表和关系边表的结构设计。 |
| `research-planning/references/output-schemas.md` | 任务依赖图（task dependency graph）的结构化思路 — 影响本审计关系边表中的流程依赖关系建模。 |
| `autoresearch/SKILL.md` | **Completion is artifact-gated** — 影响本审计的 evidence gate 严格性：要求每条结论必须可回链到 A.2 证据账本中的精确锚定。 |

### 9.2 最高风险 3 点

| # | 风险 | 主线程合并复核建议 |
|---|---|---|
| R1 | **PICOC 五个维度的 SE 实例化类别不是 exhaustive taxonomy**。本审计已标注"层级枚举（非穷举）"和"ILUSTRATIVE 不是 exhaustive"在外推限制中。但后续 A2a 若据此直接构建 RQ schema 叶子而不经过扩库验证，可能将非穷举类别误当成 complete typology。 | 合并时确认 PAPER2 RQ schema 已将 PICOC 标注为 `methodological_seed`，并关联至少 3 篇真实 SLR 的 RQ 编码实例做饱和度检查。 |
| R2 | **Table 5/6 的 51 项质量核对清单未在 PDF 中逐项核验**。`paper_content.txt` 的 OCR 提取可能存在遗漏、对齐错位或编号错误。A2a 若直接使用这些清单而未做 PDF 版面核验，可能将 OCR artifact 写入 schema。 | 合并时确认 A.4 中已将 Table 5、Table 6 的 PDF 版面核验标记为 `needs_manual_check`，并在 A2a 启动前完成 PDF 对照。 |
| R3 | **本审计的"SLR 流程维度树"和"结构化框架维度树"可能被后续 agent 误当成 empirical dimension tree** 而非 guideline-derived process tree。如果后续 A2a 用这棵树去编码 empirical SLR 的 primary study attributes，会发生 category error。 | 合并时确认每个维度节点的元数据中明确标注 `source_type: guideline_derived`，与 empirical `source_type: extracted_from_primary_study` 区分。 |

### 9.3 文件缺失与 blocked 状态

| 文件 | 状态 |
|---|---|
| 所有 7 个要求技能 / 指南文件 | 均已成功读取，无 blocked。 |
| `paper_content.txt` | 已读全部 3091 行。 |
| `bibtex.bib` | 已读。 |
| `metadata.json` | 已读。 |
| `review.md` | 已读全部约 220 行。 |
| `paper.pdf` | 未读取（非 blocked；本次审计定位为"全文文本级"，PDF 版面核验标记为 A2a 任务）。 |
| `patterns/pattern-field-schema.md` | 已读；用于校准返修建议中的 schema 合同要求。 |
| `GUIDE.md` | 已读；用于判定统计池资格、证据等级和降级规则。 |

**本次审计未出现 blocked / timeout / 文件缺失。**