# kitchenham-charters-2007-slr-guidelines · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是。读取路径：
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是。已全文通读 3091 行的 `paper_content.txt`，覆盖从 Table of Contents（Page 2--3）到 Appendix 3 末尾（Page 65）的全部正文、表格和附录。阅读覆盖范围：§0--§7 全部章节、Table 1--Table 9、Figure 1--Figure 2、Appendix 1--Appendix 3。
- **是否核对 `paper.pdf`**：否。PDF 已驻留在同目录 `paper.pdf`（1.5 MB），但未使用视觉工具逐页核对图表编号、页码和排版。原因：审计工具链不提供 PDF 渲染能力；`paper_content.txt` 是全文文本提取产物，已作为主证据源。报告中所有图表引用均以 `paper_content.txt` 的页号区段和文本证据为锚点，并标注"待 PDF 视觉核对"。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

Kitchenham & Charters (2007) 不是一篇执行后的系统综述，而是 **软件工程领域系统综述的方法学指南**。其核心贡献声明为：为软件工程研究者提供一份从规划（Planning）、执行（Conducting）到报告（Reporting）三阶段全覆盖的 SLR 操作指南。

原文没有传统意义上的"研究问题（RQ）"，而是定义了指南需要回答的操作性问题：
- 系统综述规划阶段需要什么？（§5：need for review, commissioning, research questions, protocol, protocol evaluation）
- 系统综述执行阶段需要什么？（§6：search, selection, quality assessment, data extraction, data synthesis）
- 系统综述报告阶段需要什么？（§7：dissemination, formatting, evaluation）

原文在 §5.3 中定义了 RQ 的结构化方法 PICOC（Population, Intervention, Comparison, Outcome, Context），并在 §5.3.1 中区分了 question types。这些是元级别的 RQ 构造规范，不是指南自身的研究问题。

### 2.2 原文方法流程

原文自身的方法学来源在 §1.1--§1.2 中声明：基于已有医学 SLR 指南（Cochrane Collaboration, CRD, NHS）、软件工程经验方法学文献、以及作者自身执行 SLR 的实践经验。它不是通过系统检索/纳排/数据抽取形成的指南，而是基于专家经验综合的方法学文献。

原文为读者定义了完整的三阶段 SLR 流程（Figure 1, §4）：

```
Planning → Conducting → Reporting
```

各阶段细化为：

**Planning（§5）**：
1. 确定 review need（§5.1）
2. 委托/授权 review（§5.2）
3. 制定研究问题（§5.3）：question types + PICOC structure
4. 制定 review protocol（§5.4）：包含 RQ、search strategy、study selection criteria/procedures、quality assessment checklists/procedures、data extraction strategy、synthesis strategy、dissemination strategy、project timetable
5. 评估 protocol（§5.5）

**Conducting（§6）**：
1. 文献检索（§6.1）：search strategy、publication bias mitigation、bibliography management、documenting search（Table 2）
2. 研究筛选（§6.2）：selection criteria、selection process、reliability
3. 质量评价（§6.3）：hierarchy of evidence、quality instruments（Tables 3, 4, 5, 6）、limitations
4. 数据抽取（§6.4）：design of extraction forms（Table 5）、contents of collection forms（Table 6）、procedures、duplicate handling、missing data
5. 数据综合（§6.5）：descriptive synthesis、quantitative synthesis/meta-analysis、presentation of quantitative results、qualitative synthesis、mixed synthesis、sensitivity analysis、publication bias

**Reporting（§7）**：
1. 确定传播策略（§7.1）
2. 格式化主报告（§7.2, Table 7）
3. 评估综述报告（§7.3）

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文包含以下显式结构化要素：

| 要素类型 | 原文位置 | 内容 |
|---|---|---|
| **问题分类体系** | §5.3.1, Table 1 | PICOC 五要素分解（Population, Intervention, Comparison, Outcome, Context）；question types 分类 |
| **检索文档模板** | §6.1.4, Table 2 | Search process documentation：含 Digital Library / Journal Hand Searches / Conference proceedings / Efforts to identify unpublished studies / Other sources 五列 + 字段模板 |
| **质量概念定义** | §6.3.1, Table 3 | Quality concept definitions：含 bias、internal validity、external validity 等概念定义 |
| **偏倚类型表** | §6.3.2, Table 4 | Types of Bias：列举 selection bias、performance bias、measurement bias、attrition bias 等 |
| **量化研究质量清单** | §6.3.2, Table 5 | Summary Quality Checklist for Quantitative Studies：含研究设计、conduct、analysis、conclusion 等多条评分问题 |
| **质性研究质量清单** | §6.3.2, Table 6 | Checklist for qualitative studies：含研究设计、数据收集、分析、credibility、transferability 等条目 |
| **数据抽取表单设计原则** | §6.4.1, Tables 5（前） | Design of Data Extraction Forms：单 researcher vs 多 researcher 的 form 设计指导 |
| **数据收集表单内容类别** | §6.4.2, Table 6（前） | Contents of Data Collection Forms：含 study identifier、study context、study design、data、results 等类别 |
| **数据抽取表单完整示例** | §6.4.2, Pages 30--40 | 以跨公司/单公司工作量估计 SLR 为例，展示完整已填 extraction form（含 20+ 字段） |
| **证据层级** | §6.3.1 | Hierarchy of Evidence：从 systematic reviews 到 expert opinion 的五层结构 |
| **流程图** | §4, Figure 1 | 三阶段 SLR 流程图 |
| **漏斗图** | §6.5.7, Figure 2 | Funnel plot 示例（publication bias 检测） |
| **报告结构模板** | §7.2, Table 7/8 | Structure and Contents of Reports of Systematic Reviews：Title, Authorship, Executive Summary, Background, Review questions, Search, Selection, Quality, Data extraction, Data synthesis, Discussion, Conclusions, Conflicts of interest, Acknowledgements, References, Appendices |
| **流程对比表** | §4, Table 9 | Systematic review process proposed in different sources：对比多个来源的流程定义 |
| **附录 1** | Appendix 1 | Steps in a systematic review：完整步骤清单 |
| **附录 2** | Appendix 2 | Software Engineering Systematic Literature Reviews：以具体 SLR 为例展示抽取字段和数据整理方法；含 extraction form 字段列表（source, year, classification (type, scope), topic area, authors/affiliation, RQ, EBSE reference, practitioner guidelines, #primary studies, summary, quality score） |
| **附录 3** | Appendix 3 | Protocol for a Tertiary study of Systematic Literature Reviews and Meta-analyses in Software Engineering from 2004：完整 tertiary review protocol；含 search strategy（7 个数字图书馆 + 手工检索）、inclusion/exclusion criteria、quality scoring scheme（Y=1, P=0.5, N=0 + 4 个评分问题 + 总分 0--4）、data extraction fields（含 source, year, classification, topic, authors, RQ, EBSE ref, guidelines, #primary, summary, quality score）、data analysis plan（按年份 count、按 topic count、按组织 count、quality trend over time、quality vs guideline reference） |

### 2.4 原文如何从字段/统计观察形成 conclusion/finding/gap/recommendation

作为 guideline，原文本身不产生领域 finding。但它提供了从数据综合到结论形成的规范：

- **§6.5.1**：描述性综合通过表格组织 extract 数据，识别一致/不一致模式。
- **§6.5.2--§6.5.3**：定量综合（meta-analysis）通过统计技术（effect size、funnel plot、forest plot）汇总结果；介绍了固定效应和随机效应模型。
- **§6.5.4**：质性综合通过 thematic analysis、meta-ethnography 等方法整合质性证据。
- **§6.5.6**：敏感性分析用于检测结论是否对包含/排除特定研究、质量阈值、数据操作敏感。
- **§6.5.7**：发表偏倚检测用 funnel plot 和统计检验（Egger's test, Begg's test）。
- **§7.2**：报告中的讨论/结论应回答 RQ、讨论局限性、提出对未来研究和实践的建议（Table 7/8）。
- **Appendix 2 和 3**：提供了从提取字段到统计计数再到趋势判断的完整 working example。

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树快照

当前 review.md 维度树由两部分组成：
1. **4 个原文模式候选叶子**：`orig-protocol`、`orig-search-selection`、`orig-quality-validity`、`orig-synthesis-reporting`
2. **6 个 Paper2 投影叶子**：`rq`、`theme`、`taxonomy`、`method`、`evidence`、`finding`

根节点：`[dim-kitchenham-charters-2007-slr-guidelines-root]` = "SLR guideline"

### 3.2 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | "SLR guideline" 准确描述了本文性质。原文是 EBSE Technical Report EBSE-2007-01，定位为软件工程 SLR 方法学指南。 | 通过 |
| 主干分支是否覆盖原文 schema | **不通过** | 原文具有三阶段主干（Planning → Conducting → Reporting），但当前树未将其作为维度树的第一层分支。4 个"原文模式候选叶子"跨越合并了 Planning/Conducting/Reporting 的阶段划分。例如 `orig-synthesis-reporting` 将 Conducting 阶段的 Data Synthesis 与 Reporting 阶段的 Dissemination/Formatting/Evaluation 混为一叶。 | **I** |
| 叶子维度是否足够具体 | **不通过** | 原文包含 10+ 个显式结构化表格和分类体系（PICOC、Table 2 检索文档、Tables 3--6 质量清单、Tables 5--6 数据抽取表单、Table 7/8 报告结构、Appendix 2--3 工作示例），当前 4 个原文叶子将所有这些压缩为 4 个粗粒度 buckets。尤其遗漏：PICOC 五要素分解、evidence hierarchy、quality instrument item 级字段、data extraction form 设计原则与内容类别、search documentation 模板字段、sensitivity analysis 与 publication bias 检测方法。 | **I** |
| 取值空间是否可执行 | **不通过** | 原文中 Tables 2--8 和 Appendices 1--3 提供了大量可执行模板和枚举值，但当前 review 的 `pattern-field-schema.md` compliant 叶子并未把这些枚举值映射为候选取值空间。例如 quality checklist items 可形成结构化打分空间，但当前树中 quality-validity 叶子无子字段。 | **I** |
| 关系边是否缺失 | **不通过** | 原文明确定义了流程阶段之间的顺序依赖：RQ → Search Strategy → Study Selection → Quality Assessment → Data Extraction → Data Synthesis → Reporting。当前维度树没有任何关系边表示这些依赖。此外，原文还定义了 Protocol 作为统领所有阶段的元结构，以及 sensitivity analysis 与 synthesis 之间的回环关系。 | **M** |
| 统计用途 / 分母是否正确 | 通过 | 本文已正确标记为 `eligible_for_statistical_synthesis=false`，排除理由为"方法学 guideline；不是执行后的 SLR/SMS/tertiary 统计样本"。方法论正确。 | 通过 |
| 候选 finding 路径是否完整 | **不通过** | review.md 的 [clm-kitchenham-charters-2007-slr-guidelines-finding-boundary] (C09) 正确声明了"本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决"。但 A.3 的 C04--C07 将 "rq / theme / taxonomy / method / evidence / finding" 六个 Paper2 投影叶子直接声明为 dimension leaf definition，而未说明它们只是 Paper2 自己的维度接口、并非原文自身 schema 的直接复原。这会误导下游 A2a 将 Paper2 的通用接口当成原文 schema。 | **I** |
| A.1--A.4 证据链是否足够 | **不通过** | A.2 只有 5 条证据（EV-001 到 EV-005），其中 EV-002 的原文定位是"Page 2--3 目录 + §5--§7 正文"，EV-003 是"Page 29--40 data extraction forms area"，均为宽泛范围引用且均标记为 `not_verified` 强度。5 条证据中 4 条为 `not_verified`，1 条（EV-001）为 `weak`。这些证据不足以支撑 A.3 中任何 concrete claim。按照 `pattern-field-schema.md` §8.6 的降级规则，`not_verified` 和 `weak` 证据不得支撑 `statistical_synthesis`，且 A.3 只能允许 `schema_seed`、`boundary_anchor`、`candidate_finding`、`risk_only` 或 `do_not_use`。当前 C04--C07 的 `allowed_paper_position` 已正确设为 `schema_seed`，但 claims 本身的 `leaf_definition` 声明显得比证据强度更确定。 | **M** |
| 是否存在可能误导 A2a 的强主张 | **是** | 当前树将原文 57 页的方法学内容压缩为 4 个粗粒度叶子 + 6 个 Paper2 投影叶子，且 6 个投影叶子使用了通用维度命名（rq/theme/taxonomy/method/evidence/finding），这会让下游 A2a 误以为：(a) 这篇 guideline 的 schema 就是这 10 个维度；(b) 6 个 Paper2 投影叶子直接对应原文结构。实际上原文没有 "taxonomy" 或 "finding" 作为自身维度——原文有的是 PICOC classification、question types、quality checklists、extraction form categories、synthesis methods、sensitivity analysis 和 reporting template。把 Paper2 的接口维度当成原文 schema 会系统性地导致维度树过小和维度语义失真。 | **I** |

## 4. 建议维度树骨架

以下维度树更忠实地反映原文结构，按原文的三阶段主干（Planning → Conducting → Reporting）展开，并在叶子上映射到原文具体表格/附录：

```
[dim-root] SLR guideline (Kitchenham & Charters, 2007)

  ├── [dim-planning] Planning (§5)
  │   ├── [leaf-review-need] Review need determination (§5.1)
  │   │   └── 取值空间: new topic / confirm existing finding / resolve controversy
  │   ├── [leaf-rq-picoc] Research question PICOC structure (§5.3, Table 1)
  │   │   ├── [sub-leaf-population] Population
  │   │   ├── [sub-leaf-intervention] Intervention
  │   │   ├── [sub-leaf-comparison] Comparison
  │   │   ├── [sub-leaf-outcome] Outcome
  │   │   └── [sub-leaf-context] Context
  │   ├── [leaf-question-types] Question types (§5.3.1)
  │   │   └── 取值空间: feasibility / characterisation / evaluation / causal / comparative
  │   ├── [leaf-protocol-elements] Protocol elements (§5.4)
  │   │   └── 取值空间: RQ / search strategy / selection criteria+procedures /
  │   │              quality checklist+procedures / data extraction strategy /
  │   │              synthesis strategy / dissemination strategy / timetable
  │   └── [leaf-protocol-evaluation] Protocol evaluation criteria (§5.5)
  │       └── 取值空间: expert review / supervisor review / internal consistency check /
  │                     search↔RQ alignment / extraction↔RQ alignment / analysis↔RQ alignment

  ├── [dim-conducting] Conducting (§6)
  │   ├── [leaf-search-documentation] Search documentation template (§6.1.4, Table 2)
  │   │   └── 取值空间: digital library (name, strategy, date, years) /
  │   │              journal hand search (name, years, issues not searched) /
  │   │              conference proceedings (title, name, translation, journal) /
  │   │              unpublished (groups, researchers, websites) /
  │   │              other sources (date, URL, conditions)
  │   ├── [leaf-publication-bias] Publication bias (§6.1.2, §6.5.7)
  │   │   └── 取值空间: grey literature scan / conference proceedings /
  │   │              expert contact / funnel plot / Egger test / Begg test
  │   ├── [leaf-study-selection] Study selection (§6.2)
  │   │   └── 取值空间: inclusion criteria / exclusion criteria /
  │   │              selection process (initial→title/abstract→full text→final) /
  │   │              reliability (Kappa / inter-rater agreement)
  │   ├── [leaf-evidence-hierarchy] Evidence hierarchy (§6.3.1)
  │   │   └── 取值空间: systematic reviews / RCTs / controlled observational /
  │   │              uncontrolled observational / expert opinion
  │   ├── [leaf-quality-checklist-quant] Quality checklist — quantitative (§6.3.2, Table 5)
  │   │   └── 取值空间: study design (design description, controls, randomization...) /
  │   │              conduct (population, data collection, analysis...) /
  │   │              analysis (data quality, statistical methods, sensitivity...) /
  │   │              conclusion (credibility, limitations, link evidence→conclusion...)
  │   ├── [leaf-quality-checklist-qual] Quality checklist — qualitative (§6.3.2, Table 6)
  │   │   └── 取值空间: design (appropriateness, rigor, research question link...) /
  │   │              data collection (description, contextualization...) /
  │   │              analysis (richness, iterative questioning, negative case...) /
  │   │              findings (credibility, roles, transferability, reflexivity...)
  │   ├── [leaf-extraction-form-design] Data extraction form design (§6.4.1, Table 5)
  │   │   └── 取值空间: single researcher form / team form / mapping study form /
  │   │              piloting requirement / inter-rater check procedure
  │   ├── [leaf-extraction-form-content] Data extraction form content categories (§6.4.2, Table 6)
  │   │   └── 取值空间: study identifier (title, authors, source, year...) /
  │   │              study context (population, intervention, setting...) /
  │   │              study design (design type, sample size, controls...) /
  │   │              data (variables, measurement...) /
  │   │              results (effect size, uncertainty, direction...)
  │   ├── [leaf-synthesis-descriptive] Descriptive synthesis (§6.5.1)
  │   │   └── 取值空间: tabulation by outcome / homogeneity assessment /
  │   │              heterogeneity source identification / vote counting
  │   ├── [leaf-synthesis-quantitative] Quantitative synthesis (§6.5.2--§6.5.3)
  │   │   └── 取值空间: meta-analysis / fixed-effect / random-effect /
  │   │              effect size (SMD, OR, RR) / forest plot / heterogeneity (I², Q)
  │   ├── [leaf-synthesis-qualitative] Qualitative synthesis (§6.5.4--§6.5.5)
  │   │   └── 取值空间: thematic analysis / meta-ethnography /
  │   │              grounded theory / narrative synthesis
  │   └── [leaf-sensitivity-analysis] Sensitivity analysis (§6.5.6)
  │       └── 取值空间: excluding low-quality studies / changing inclusion criteria /
  │                     varying synthesis method / testing missing data assumptions

  ├── [dim-reporting] Reporting (§7)
  │   ├── [leaf-dissemination-strategy] Dissemination strategy (§7.1)
  │   │   └── 取值空间: academic journal / conference / technical report / web page /
  │   │              practitioner magazine
  │   ├── [leaf-report-structure] Report structure template (§7.2, Table 7/8)
  │   │   └── 取值空间: Title / Authorship / Executive Summary / Background /
  │   │              Review Questions / Search Strategy / Study Selection /
  │   │              Quality Assessment / Data Extraction / Data Synthesis /
  │   │              Discussion / Conclusions / Conflicts of Interest /
  │   │              Acknowledgements / References / Appendices
  │   └── [leaf-report-evaluation] Review report evaluation (§7.3)
  │       └── 取值空间: RQ answer completeness / search thoroughness /
  │                 selection appropriateness / quality assessment rigor /
  │                 synthesis adequacy / conclusion validity

  └── [dim-appendix-examples] Appendices: working examples
      ├── [leaf-appendix1] Steps checklist (Appendix 1)
      ├── [leaf-appendix2-extraction-fields] SLR extraction field examples (Appendix 2)
      │   └── 取值空间: source / year / classification (type, scope) / topic area /
      │              authors+affiliation+country / RQ / EBSE reference /
      │              practitioner guidelines / #primary studies / summary / quality score
      └── [leaf-appendix3-protocol] Tertiary review protocol (Appendix 3)
          └── 取值空间: search (7 digital libraries + manual) / inclusion/exclusion /
                        quality scoring (Y=1, P=0.5, N=0, 4 items, total 0--4) /
                        data extraction fields (10 items) /
                        data analysis (count per year, per topic, per org, quality trend,
                        quality vs guideline reference)

  [edge-planning-to-conducting] Planning → Conducting (protocol-driven execution)
  [edge-conducting-to-reporting] Conducting → Reporting (synthesis-driven reporting)
  [edge-protocol-to-all] Protocol → {Search, Selection, Quality, Extraction, Synthesis, Reporting}
  [edge-sensitivity-to-synthesis] Sensitivity Analysis → Synthesis (iterative refinement)
```

**关于 6 个 Paper2 投影叶子的说明**：上述建议树不将 Paper2 的通用维度（rq/theme/taxonomy/method/evidence/finding）混入原文 schema 复原。Paper2 应在 A2a 阶段通过一份独立的"原文 schema → Paper2 维度模型"映射表完成维度投影，而不是把 Paper2 的维度名直接当成原文叶子。这样做的好处：(1) 原文维度树忠实于原文，(2) 跨 19 篇论文的维度可比较性由 Paper2 映射层保证，(3) 避免下游混淆"原文有什么"和"Paper2 需要什么"。

## 5. 必须补充 / 修正清单

| # | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|---|
| 1 | 将维度树从 4+6 扁平结构改为三阶段主干展开 | review.md §A 维度树 | 按 §4 建议树重建维度树，以 Planning → Conducting → Reporting 为第一层分支，展开到 25+ 叶子。 | `paper_content.txt` Page 2--3 目录结构 + §4 Figure 1 流程 | **I** |
| 2 | 从维度树中分离 Paper2 投影维度 | review.md §A 维度树 | 将 6 个 Paper2 投影叶子（rq/theme/taxonomy/method/evidence/finding）从维度树中移除，单独记录为 "Paper2 维度映射表" | `pattern-field-schema.md` §8.6 降级规则；`paper_story.md` §7 维度模式定义 | **I** |
| 3 | 补充 PICOC 五要素作为叶子及子字段 | review.md §A 维度树 `dim-planning` 下 | 新增 `leaf-rq-picoc` 及其 5 个子叶子，映射 Population/Intervention/Comparison/Outcome/Context，并引用 Table 1 | `paper_content.txt` Page 10--11 (§5.3.2, Table 1) | **I** |
| 4 | 补充数据抽取表单设计/内容类别 | review.md §A 维度树 `dim-conducting` 下 | 新增 `leaf-extraction-form-design` 与 `leaf-extraction-form-content`，分别引用 §6.4.1 Table 5 和 §6.4.2 Table 6 | `paper_content.txt` Page 29--40 (§6.4.1, §6.4.2, Tables 5, 6) | **I** |
| 5 | 补充质量清单 item 级叶子和子字段 | review.md §A 维度树 `dim-conducting` 下 | 拆分当前 `orig-quality-validity` 为：`leaf-evidence-hierarchy`、`leaf-quality-checklist-quant`、`leaf-quality-checklist-qual`，并映射 Tables 3--6 的具体条目 | `paper_content.txt` Page 20--29 (§6.3, Tables 3, 4, 5, 6) | **I** |
| 6 | 补充检索文档模板字段、发表偏倚检测方法、敏感性分析方法 | review.md §A 维度树 `dim-conducting` 下 | 新增 `leaf-search-documentation`（Table 2）、`leaf-publication-bias`（§6.1.2, §6.5.7）、`leaf-sensitivity-analysis`（§6.5.6） | `paper_content.txt` Page 16 (Table 2), Page 38--39 (§6.5.6, §6.5.7) | **M** |
| 7 | 补充附录 2 和附录 3 的工作 extraction form 字段 | review.md §A 维度树 `dim-appendix-examples` 下 | 新增 `leaf-appendix2-extraction-fields` 和 `leaf-appendix3-protocol`，将附录中的实际抽取字段作为候选取值空间 | `paper_content.txt` Page 50--65 (Appendix 2, 3) | **M** |
| 8 | 细化 A.2 证据定位 | review.md §A.2 | 将 EV-002（"Page 2--3 目录 + §5--§7 正文"）拆分为 10+ 条表格/章节级精确证据，每条明确指定 section/table 编号、原文定位，并将 `not_verified` 更新为 `weak` 或保持 `not_verified` 但说明 specific anchor point | 当前 EV-002 / EV-003 / EV-004 均为泛定位 | **M** |
| 9 | 在维度树中补充关系边 | review.md §A 维度树 | 至少添加 `Planning → Conducting`、`Conducting → Reporting`、`Protocol → {Search, Selection, Quality, Extraction, Synthesis, Reporting}` 三条关系边 | `paper_content.txt` Figure 1, §4, §5.4 | **M** |
| 10 | 明确 A.3 claims 的 Paper2 角色标识 | review.md §A.3 | 在 C01--C12 已正确使用 `schema_seed` 的基础上，显式声明"本文只提供 guideline 结构先验，不产生统计 evidence；所有 claims 进入 A2a 前需由后续执行型 SLR/SMS/tertiary 样本补充统计证据" | `pattern-field-schema.md` §8.6 | **M** |

## 6. C/I/M 结论

### C（阻塞 Paper2 学术目标或证据链）

**无**。当前 review.md 正确识别了本文的 guideline 性质，将其排除出主统计池，并限制了 finding 使用范围。这些关键判断没有破坏 Paper2 的证据链。

### I（实质影响维度树可用性或原文 schema 复原准确性）

**5 项 I 级问题**（对应 §5 修复清单 #1--#5）：

1. **#1 — 主干缺失**：维度树未反映原文的三阶段主干（Planning → Conducting → Reporting），这是原文最核心的组织结构。缺失后，下游 A2a 将无法正确理解本文的任何维度组织逻辑。
2. **#2 — Paper2 投影污染**：6 个 Paper2 投影叶子混入原文 schema 复原，可能导致 A2a 将 Paper2 接口当成原文结构，系统性低估原文的信息丰富度。
3. **#3 — PICOC 缺失**：PICOC 是原文对 RQ 结构化最核心的贡献，在 SE SLR 领域被广泛引用。缺失此项会使 Paper2 的综述元模型初始化错失关键的结构化规范。
4. **#4 — 数据抽取表单缺失**：原文 §6.4 的 Tables 5--6 提供了完整的数据抽取表单设计/内容规范，是 SLR protocol 中最可操作的字段来源。缺失后，Paper2 的维度模式抽取表单设计将失去最直接的先验。
5. **#5 — 质量清单缺失**：原文 Tables 3--6 提供了研究偏倚分类、证据层级和量化/质化研究质量清单的直接 item 级参考，是 Paper2 中 A5（效度威胁与风险评估）的核心先验。当前 `orig-quality-validity` 粒度太粗，无法支撑 item 级风险建模。

**影响**：如果不修复 #1--#5，Paper2 在使用这篇 guideline 时，只能获得一个粗粒度的"有 protocol、有 quality、有 synthesis"的模糊印象，而无法获得原文真正贡献的 20+ 结构化字段和模板。考虑到 Kitchenham & Charters (2007) 是 SE SLR 领域被引最多的方法学基准之一，这种维度损失会直接削弱 Paper2 的 "研究者定义综述元模型" 与 "维度模式初始化" 的精度和可信度。

### M（不阻塞的清晰度或维护性建议）

**5 项 M 级问题**（对应 §5 修复清单 #6--#10）：包括检索文档模板细化、附录字段补充、证据定位精度提升、关系边补充和 Paper2 角色声明完善。这些不影响 Paper2 的结构正确性，但会提升下游 A2a 的工作效率、降低误解释风险。

### 最终建议

**NEEDS FIX**。原因：5 项 I 级问题涉及维度树结构的根本性不足——主干缺失 + Paper2 投影污染 + PICOC/质量清单/数据抽取表单三大关键原文要素遗漏。当前树更接近"用 Paper2 通用接口粗略概括了一篇 guideline"，而非"从原文结构中忠实复原其可操作维度"。在进入 A2a 之前，必须按 §4 建议树重建维度树，并将 Paper2 投影维度分离为独立的映射表。
