# petersen-2008-systematic-mapping · deepseek 全文审计报告

## 1. 审计身份与输入

| 字段 | 内容 |
|---|---|
| reviewer 身份 | deepseek |
| 审计日期 | 2026-06-29 |
| 审计范围 | 单篇论文 `petersen-2008-systematic-mapping` 的 `review.md` 维度树完整性、准确性、可追溯性 |
| 是否读取 `$ai-research-writing-skill` | 是。路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`；并读取其 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md` |
| 是否读取 `$research-planning` | 是。路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`；并读取 `references/planning-prompts.md` |
| 是否读取 `$oh-my-codex:autoresearch` | 是。路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` |
| 是否完整阅读 `paper_content.txt` | 是。已逐段阅读全部 536 行（10 页 PDF 全文），覆盖 §1 Introduction、§2 The Systematic Mapping Process（§2.1–§2.6）、§3 Systematic Mapping vs Systematic Review（§3.1–§3.5）、§4 Additional Guidelines（G1–G5）、§5 Conclusion、References。 |
| 是否核对 `paper.pdf` | 是。已通过 `pdfinfo` 确认 PDF 为 10 页 A4、未加密、由 pdfTeX 生成（CreationDate: 2008-05-20）。未进行图表视觉级逐页核对，因为 `paper_content.txt` 文本提取质量良好、关键表格与图题均被正确提取，且当前审计聚焦于维度树结构完整性而非表格数值精准锚定。 |
| 是否读取文库规则 | 是。已读取 `survey_of_surveys/` 的 README、GUIDE、SUMMARY、`patterns/pattern-field-schema.md`，以及 `story/paper_story.md`。 |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

Petersen et al. (2008) 是一篇 **SMS 方法论文**，发表目标如下：

- **核心目标**：将 systematic mapping 方法学引入软件工程，描述如何执行 SMS，并提供指南。
- **次要目标**：通过系统性分析已有 SE systematic reviews，对比 SMS 与 SR 的差异，澄清何时选择何种方法。
- **贡献声明**（来自 Abstract / §1 / §5）：
  1. 提出 SE systematic mapping 五步流程。
  2. 通过完整 SMS 案例（软件产品线可变性）演示该流程。
  3. 通过分析 8 篇已有 SE SR 对比 SMS 与 SR 的目标、广度、深度、效度与启示。
  4. 基于对比给出 SMS 扩展指南（G1–G5）。

原文未声称该论文发现某个 SE 主题领域的统计结论；它声称的是**方法学贡献**。

### 2.2 原文方法流程

**SMS 五步流程（§2.1 §2.2–§2.6，Figure 1）：**

1. **定义研究问题 / 研究范围**（§2.2）：用 PICO 框架界定 scope。
2. **检索 primary studies**（§2.3）：构建搜索串、选择数据库（IEEE Xplore, ACM Digital Library, Inspec, Compendex 等）。
3. **按纳排标准筛选论文**（§2.4）：基于标题和摘要筛选；纳排标准由 RQ 驱动；对于 mapping，搜索不宜被特定实验设计或 outcome 过度限制。
4. **对摘要做 keywording，形成分类方案**（§2.5）：读摘要 → 识别关键词 / 概念 → 聚类成类别 → 迭代精化；若摘要质量不足，继续读引言或结论；允许追加、合并或拆分类别。
5. **数据抽取并映射成 systematic map**（§2.6）：将每篇论文按分类方案归类，记录归类理由（rationale）；用频数表 / 交叉表 / bubble plot 呈现。

**SR 分析流程（§3）：**
- 从 EBSE 技术报告中选取 8 篇已完成 SE SR（§3.1 明确列出：Davis et al. 2006, Grimstad et al. 2006, Jørgensen & Shepperd 2007, Kampenes et al. 2007, Kitchenham et al. 2007, MacDonell & Shepperd 2007, Mendes 2005, Hannay et al. 2007）。
- RQ1: 这些 SR 如何使用 primary studies（分析目的）？
- RQ2: 这些 SR 如何分类论文？
- 按目标、广度、深度、效度、启示维度对比归纳。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

| 原文要素 | 位置 | 内容 |
|---|---|---|
| **SMS 流程图** | §2.1 Figure 1 | 五步流程（Process Steps: Definition of Research Questions → Conduct Search → Screening of Papers → Keywording using Abstracts → Data Extraction and Mapping Process） |
| **分类方案（三维 facet）** | §2.5–§2.6 | 1. **Topic facet**：领域子主题，如 SPL variability 的子类。2. **Contribution facet**：process、method、model、tool、metric、other。3. **Research type facet**：采用 Wieringa et al. (2006) 分类——validation research、evaluation research、solution proposal、philosophical paper、opinion paper、experience paper。 |
| **Keywording 方法** | §2.5 | 从摘要中识别关键词 / 概念 → 聚类成类别集合 → 迭代精化；摘要不足时读引言或结论；抽取过程中可新增 / 合并 / 拆分类别的演进规则。 |
| **数据抽取表结构** | §2.6 | 至少包含：论文元数据（标题、作者、年份、venue）、分类类别归属、归类理由（rationale for classification）。 |
| **Bubble plot 呈现** | §2.6、§4（G1） | X 轴 = topic facet，Y 轴 = contribution facet，bubble 大小 = 该交叉类别的论文数；建议参考 Trendalyzer / GapMinder 风格。 |
| **Map vs Review 对比表** | §3.4 Table 1 | 按 Goals、Breadth、Depth、Validity issues、Implications 五行对比 SMS 与 SR。 |
| **扩展指南 G1–G5** | §4 | G1: 呈现可视化结果地图；G2: 可视化 mapping 流程；G3: 提供分类工具支持；G4: 每个类别提供详细报告；G5: 结合系统映射与系统综述。 |
| **Quality rubric** | 无 | 原文明确说明 SMS 不做 formal quality assessment（§3.4 指出 mapping 以 publication bias 为主要效度威胁，而 SR 关注 internal validity 与 quality）。这是一个 **absence evidence**，应在维度树中记录。 |
| **Roadmap figure** | §2.1 Figure 1 | 五步流程图是 roadmap 性质，描述了 SMS 的执行路径，不是统计 finding。 |

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的发现形成路径如下：

1. **频数统计**：每个 facet 类别中的论文数量 → 识别高频 / 低频 / 空白区域。
2. **交叉统计**：topic × contribution × research-type 的交叉频数 → bubble plot → 暴露研究空白（gaps）。
3. **Map vs Review 对比**：按 Goals / Breadth / Depth / Validity / Implications 五维归纳 SR 分析结果 → 得出结论：SMS 与 SR 互补。
4. **Guideline 推导**：从 SMS 案例执行经验和对比中，抽象出 G1–G5。

原文的结论分为两类：
- **方法学结论**（SMS 流程、指南）：基于作者的案例执行经验和对 SR 的比较归纳，属 author claim。
- **案例领域统计观察**（SPL variability 的论文分布）：来自一次完整 SMS 执行，有频数数据支撑。

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树结构回顾

当前 `review.md` A.2 的维度树主干为：

```
[dim-petersen-2008-systematic-mapping-root]
├── [dim-petersen-2008-systematic-mapping-planning]  ← A1-M0 equivalent
├── [dim-petersen-2008-systematic-mapping-corpus]    ← A1-M1 equivalent
├── [dim-petersen-2008-systematic-mapping-taxonomy]  ← A1-M2 equivalent
├── [dim-petersen-2008-systematic-mapping-method]    ← A1-M3 equivalent
├── [dim-petersen-2008-systematic-mapping-evidence]  ← A1-M4 equivalent
└── [dim-petersen-2008-systematic-mapping-finding]   ← A1-M5/M6 equivalent
```

并有一个 C12 结论行 "原文模式候选叶子映射"，列出 5 个原文叶子：
- `leaf-petersen-2008-systematic-mapping-orig-mapping-planning`
- `leaf-petersen-2008-systematic-mapping-orig-keywording`
- `leaf-petersen-2008-systematic-mapping-orig-classification-scheme`
- `leaf-petersen-2008-systematic-mapping-orig-map-visualization`
- `leaf-petersen-2008-systematic-mapping-orig-gap-identification`

### 3.2 维度树逐项审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| **根节点是否准确** | 通过 | `[dim-petersen-2008-systematic-mapping-root]` 正确指向论文全文。无问题。 | 通过 |
| **主干分支是否覆盖原文 schema** | **I** | 当前 6 个分支全部使用 A1-M0--M6 元维度标签（planning = M0, corpus = M1, taxonomy = M2, method = M3, evidence = M4, finding = M5/M6），而非从原文自身结构中派生。原文有三个显式分类轴（topic、contribution、research-type）、一个五步流程、一个对比分析（map vs review）、一组扩展指南（G1–G5），这些**全部被压缩进 A1-M2 "主题与维度分类" 和 A1-M3 "方法 / 技术 / 干预分类" 两个桶**。原文的 §3 Map vs Review 整章、§4 Guidelines G1–G5 在主干分支中无对应节点。 | I |
| **叶子维度是否足够具体** | **C** | 当前 A.2 维度树中 6 个 dim-* 节点的叶子均来自 A1-M0--M6 元维度框架，取值空间使用通用描述（如"研究者定义研究问题 / 范围 / PICO"、"数据库选择 / 搜索串构造 / 筛选策略"），而非原文的具体分类方案。例如 `[dim-petersen-2008-systematic-mapping-taxonomy]` 下应有原文的三维 facet（topic、contribution、research-type）作为独立叶子，且 contribution facet 应展开为 process/method/model/tool/metric/other 六值枚举，research-type facet 应展开为 Wieringa et al. 六值枚举。当前这些全部缺失。C12 列出的 5 个"原文候选叶子"虽然方向正确，但被放在一个**独立的结论节点**而非维度树主干中，且没有取值空间、没有统计用途、没有缺失值语义。这等于承认原文模式尚未被真正嵌入维度树。 | C |
| **取值空间是否可执行** | **C** | 当前 A.2 证据表对叶子取值空间的描述全是泛化的："类别区间 / 标签 / 关系 / 来源 / 频数"、"纳入 / 排除 / 未知 / 暂存"等。原文有明确可执行的取值空间：(1) contribution facet 的 6 值枚举；(2) research-type facet 的 6 值枚举（validation research / evaluation research / solution proposal / philosophical paper / opinion paper / experience paper）；(3) keywording 方法中从 abstract → keyword → cluster → category 的语义类型链；(4) G1–G5 的五条具体指南文本。这些可执行取值在维度树中不可见。 | C |
| **关系边是否缺失** | **I** | 原文有明确的横向关系：(a) 三个 facet 之间的交叉关系（topic × contribution 构成 bubble plot X/Y 轴）；(b) 流程步骤之间的 sequential 关系（Figure 1）；(c) guidelines G1–G5 与流程步骤之间的支撑关系（G1 支撑 §2.6 的可视化，G5 支撑 §3 的互补结论）；(d) keywording 与 classification scheme 之间的生成关系。当前 A.2 无任何 `[edge-*]` 关系边记录。 | I |
| **统计用途 / 分母是否正确** | **I** | 原文的统计分母是：经纳排标准筛选后的 primary studies 集合（SMS 案例中为具体篇数，SR 对比中为 8 篇）。统计用途是频数分布、交叉频数和空白检出。当前 A.2 对分母无任何显式记录，A.3 结论中 `[clm-petersen-2008-systematic-mapping-transfer]` 写"不可迁移具体领域统计结论"是正确的边界声明，但因为维度树本身没有记录原文的统计分母，该声明缺乏可审计的结构锚点。 | I |
| **候选 finding 路径是否完整** | **I** | 原文有两条清晰的 finding 路径：路径 A（频数 → 交叉 → gap → 推荐后续 SR）；路径 B（SR 对比 → 目标/广度/深度/效度/启示对比表 → 互补结论 → G5 指南）。当前 A.3 只有一个通用的 `[clm-petersen-2008-systematic-mapping-finding-boundary]` 说明"可为候选发现提供启发，但 final research finding 必须经过跨论文证据……"，没有分别映射到两条路径。A.3 的 C04–C07 只是将 M0–M6 层级标签回写为 leaf_definition，不是原文 finding 路径。 | I |
| **A.1–A.4 证据链是否足够** | **I** | A.2 仅有 4 条证据（EV-001 到 EV-004），对应以下内容：(001) bibtex/metadata/pdf；(002) paper_content.txt 全文→§2 流程、§2.4–§2.6 分类、§3 map/review 对比；(003) paper_content.txt→§2.5–§2.6 category/examples、§4 guidelines；(004) §3.4 对比总结。但原文 §2.3 检索细节（数据库列表、搜索串示例）、§2.5 keywording 的具体规则（摘要不足→读引言/结论、迭代允许新增/合并/拆分）、§3.1 SR 清单的 8 篇逐一引用、§4 G1–G5 的全部五条指南文本等**在 A.2 中没有独立的证据条目**。4 条证据支撑一棵 6 分支树和 12 条 A.3 结论，证据-结论比过大，存在"弱证据承载多结论"的风险。 | I |
| **是否存在可能误导 A2a 的强主张** | **M** | `[clm-petersen-2008-systematic-mapping-transfer]` 写"本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论"，方向正确。但 A.3-C04–C07 使用"可为 Paper2 维度树候选节点"的表述，在叶子本身没有从原文取值空间重建的情况下，可能让 A2a 误以为这 6 个叶子已经完整表达了 Petersen 2008 的 schema。建议在所有 leaf_definition 结论中显式标注"当前叶子仅来自 A1-M0--M6 元框架投影，非原文 schema 完整复原；A2a 需从原文三维 facet / 五步流程 / 指南重建"。 | M |
| **原文 RQ pattern 是否被复原** | **I** | 原文有两个独立 RQ 集：(a) 隐含在 SMS 案例中——"SPL variability 领域有哪些研究？按 topic/contribution/research-type 分类后呈现怎样的分布和空白？"(b) 显式在 §3.1——RQ1 "Clarify the objective for using the reviewed papers"，RQ2 "Determine how the papers have been classified in the reviewed papers"。当前 A.2/A.3 没有将这两组 RQ 作为独立维度树分支。 | I |
| **原文 extraction form 是否被复原** | **I** | 原文 §2.6 描述了数据抽取表至少包含三个字段：论文元数据、分类类别归属、归类理由（rationale）。这是与 Paper2 "字段级内容证据"和"rationale 记录"高度相关的原文要素，当前维度树中没有显式节点。 | I |
| **原文 quality rubric 缺失是否被记录** | **M** | 原文明确不做 formal quality assessment，是一个重要的 absence evidence——说明 SMS 与 SR 在证据等级上的根本差异。当前 `review.md` §2.4 提到了"本文强调 systematic map 的分析重心是类别频数和类别交叉"，但 A.2/A.3 中没有 `absence_evidence` 类型的条目记录"本文无 quality rubric"。 | M |
| **原文 artifact / replication 状态是否被记录** | **M** | 原文提到 SPL variability SMS 案例已提交（"in submission"——Mujtaba et al. 2008），Map vs Review 对比的 8 篇 SR 均有可追溯引用。G4 建议"每个类别提供详细报告"暗示了制品产出。当前 A.2 未将引用清单可追溯性、配套 SMS 案例提交状态作为独立证据。 | M |

### 3.3 核心问题总结

当前 `review.md` 的维度树的**根问题**是：它将 A1-M0--M6 元维度框架当作 Peterse2008 自身的 schema 来呈现，而 Petersen 2008 自身的结构（五步流程、三维 facet、Map vs Review 双 RQ 分析、G1–G5 扩展指南）只是被松散地提及在 C12 "原文候选叶子"和 A.3 的几个 leaf_definition 结论中。这导致：

1. **维度树过小**：用 6 个通用桶覆盖了一篇结构丰富的方法论文。
2. **通用 A1-M0--M6 接口被误当成原文 schema**：A.2 中的 dim-* 使用了 A1-M* equivalent 标注，使得 A2a 阅读者可能认为已复原原文 schema，实际上并未。
3. **原文最可迁移的三维分类方案（topic / contribution / research-type）** 没有被展开为可执行维度和取值空间。
4. **原文的 Map vs Review 对比整章**没有独立维度节点。
5. **原文的 G1–G5 扩展指南**没有独立维度节点。
6. **证据条目过少**（4 条），不足以支撑对 10 页方法论文的完整维度覆盖。

## 4. 建议维度树骨架

以下是从 Petersen 2008 原文结构中直接派生的维度树骨架。每个维度和叶子都有原文节号锚点。

```
[dim-petersen-2008-root]  ← 论文全文：Systematic Mapping Studies in Software Engineering
│                          （Petersen, Feldt, Mujtaba, Mattsson 2008）
│
├── [dim-petersen-2008-sms-process]  ← §2 The SMS Process
│   ├── [leaf-step1-rq-scope]           ← §2.2 | 取值: 自由文本 (PICO 框架)
│   ├── [leaf-step2-search]             ← §2.3 | 取值: 数据库列表、搜索串示例
│   ├── [leaf-step3-screening]         ← §2.4 | 取值: inclusion/exclusion criteria
│   ├── [leaf-step4-keywording]         ← §2.5 | 取值: abstract→keyword→cluster→iterate
│   └── [leaf-step5-extraction]        ← §2.6 | 取值: metadata + category + rationale
│
├── [dim-petersen-2008-classification-facets]  ← §2.5–§2.6 三维分类方案
│   ├── [leaf-facet-topic]              ← §2.5 | 取值: 领域子主题标签（free text / 聚类生成）
│   │   │                               │ 统计用途: 频数 / 横轴（bubble plot X）
│   │   │                               │ 缺失语义: not_classified（分类方案演进中未覆盖）
│   │   │
│   ├── [leaf-facet-contribution]      ← §2.6 | 取值: {process, method, model, tool, metric, other}
│   │   │                               │ 统计用途: 频数 / 纵轴（bubble plot Y）
│   │   │                               │ 缺失语义: not_reported / not_applicable
│   │   │
│   └── [leaf-facet-research-type]     ← §2.6 (Wieringa et al. 2006)
│       │                               │ 取值: {validation research, evaluation research,
│       │                               │        solution proposal, philosophical paper,
│       │                               │        opinion paper, experience paper}
│       │                               │ 统计用途: 频数 / 交叉分类
│       │                               │ 缺失语义: not_classified / not_applicable
│       │
│       [edge-facets-cross]  ← 关系边: topic × contribution → bubble plot
│
├── [dim-petersen-2008-keywording-methodology]  ← §2.5
│   ├── [leaf-keywording-source]        ← 取值: {abstract, introduction, conclusion}
│   ├── [leaf-keywording-action]        ← 取值: {identify_keywords, cluster, name_category}
│   └── [leaf-keywording-evolution]     ← 取值: {add_category, merge_categories, split_category}
│       │                               │ 缺失语义: no_evolution_needed
│
├── [dim-petersen-2008-extraction-form]  ← §2.6
│   ├── [leaf-extract-paper-meta]       ← 取值: {title, authors, year, venue}
│   ├── [leaf-extract-category]         ← 取值: 回链 [dim-petersen-2008-classification-facets]
│   └── [leaf-extract-rationale]        ← 取值: 自由文本（why this paper in this category）
│       │
│       [edge-rationale-to-evidence-chain]  ← 与 Paper2 "字段级内容证据"的直接对应
│
├── [dim-petersen-2008-map-vs-review-comparison]  ← §3
│   ├── [leaf-compare-rq1]              ← §3.1 RQ1: "Clarify the objective for using
│   │   │                                   the reviewed papers"
│   │   │                               ← 取值: {meta_analysis, narrative_summary,
│   │   │                                       thematic_analysis, ...}（从原文 §3.2 归纳）
│   │   │
│   ├── [leaf-compare-rq2]              ← §3.1 RQ2: "Determine how the papers have been
│   │   │                                   classified"
│   │   │                               ← 取值: {by_study_design, by_topic, by_outcome,
│   │   │                                       no_formal_classification, ...}
│   │   │
│   ├── [leaf-compare-sr-corpus]        ← 纳入对比的 8 篇 SR 清单（§3.1 逐一列出）
│   │   │                               ← 取值: 8 篇可追溯引用（有作者/年份/venue）
│   │   │
│   └── [leaf-compare-contrast-table]   ← §3.4 Table 1: Goals / Breadth / Depth /
│       │                                   Validity issues / Implications 五行对比
│       │                               ← 取值: 每行 SMS 侧文本 + SR 侧文本
│       │
│       [edge-compare-to-guide]  ← 关系边: §3 对比结论 → §4 G5 "Combine maps and reviews"
│
├── [dim-petersen-2008-extended-guidelines]  ← §4
│   ├── [leaf-guide-g1]                 ← G1: Present a visual map of results
│   │   │                               ← 对应 bubble plot / GapMinder 建议
│   ├── [leaf-guide-g2]                 ← G2: Visualize the mapping process
│   │   │                               ← 对应 Figure 1 流程可视化
│   ├── [leaf-guide-g3]                 ← G3: Provide tool support for classification
│   ├── [leaf-guide-g4]                 ← G4: Detailed reports per category
│   │   │                               ← 对应 "对每个类别撰写详细报告，提供更深洞见"
│   └── [leaf-guide-g5]                 ← G5: Combine systematic maps and reviews
│       │                               ← 对应 maps→reviews 互补使用
│       │
│       [edge-guide-to-process]  ← 关系边: G1→§2.6, G2→§2.1 Figure 1, G5→§3 对比结论
│
├── [dim-petersen-2008-absence-fields]  ← 原文明确不做的事项（absence evidence）
│   ├── [leaf-absence-quality-assessment]  ← §3.4: SMS 不做 formal quality assessment
│   └── [leaf-absence-meta-analysis]        ← §3: SMS 不做 statistical meta-analysis
│
└── [dim-petersen-2008-artifacts]       ← 制品、引用与可复现性
    ├── [leaf-artifact-sms-case]         ← SPL variability SMS 案例（Mujtaba et al. 2008,
    │   │                                    "in submission"）
    ├── [leaf-artifact-sr-corpus]        ← 8 篇已有 SE SR 的可追溯引用（§3.1 + References）
    └── [leaf-artifact-tool-mention]    ← G3: 建议开发分类工具，未提供具体工具
```

### 4.1 建议树与当前树的关键差异

| 维度 | 当前树 | 建议树 |
|---|---|---|
| **组织原则** | A1-M0--M6 元维度框架（自上而下投影） | 原文自身结构驱动（自下而上复原） |
| **分支数** | 6 个 dim-* | 8 个 dim-* + 3 个 edge-* |
| **叶子数** | 6 个（A1-M0--M6 leaf）+ 5 个（C12 候选）| 约 28 个叶子 |
| **分类方案** | 折叠在 A1-M2 taxonomy | 独立展开为 3 个 facet leaf + 取值空间 |
| **Map vs Review** | 无独立维度 | 独立 `dim-petersen-2008-map-vs-review-comparison` |
| **G1–G5 指南** | 无独立维度 | 独立 `dim-petersen-2008-extended-guidelines` |
| **关系边** | 无 | 3 条 edge-* |
| **Absence evidence** | 无 | 2 个 absence leaf |
| **Evidence 条目建议** | 4 条（EV-001–004） | 建议扩展到 10+ 条，每条对应独立节号 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| **FIX-1**: 维度树从 A1-M0--M6 投影改为原文结构驱动 | `review.md` A.2 维度树段 | 用 §4 建议树替换当前 6 分支 A1-M0--M6 投影。保留当前 A1-M0--M6 关系作为旁注（如 `← maps to A1-M0`），但主树应如实反映原文结构。 | 原文 §2–§4 | C |
| **FIX-2**: 展开三维分类 facet 为独立 dim-* 节点 | A.2 新增 `[dim-petersen-2008-classification-facets]` | 创建 topic / contribution / research-type 三个叶子，每个叶子配备完整取值空间、统计用途和缺失值语义。contribution 取值 = {process, method, model, tool, metric, other}，research-type 取值 = Wieringa et al. 6 值枚举。 | §2.5–§2.6 | C |
| **FIX-3**: 新增 Map vs Review 对比维度 | A.2 新增 `[dim-petersen-2008-map-vs-review-comparison]` | 包含 RQ1、RQ2、SR 语料清单、Table 1 对比表四个叶子。 | §3 全文 | I |
| **FIX-4**: 新增 G1–G5 扩展指南维度 | A.2 新增 `[dim-petersen-2008-extended-guidelines]` | 5 个 leaf-guide 各对应一条指南文本。增加 `[edge-guide-to-process]` 关系边。 | §4 | I |
| **FIX-5**: 补齐关系边 | A.2 新增 `[edge-*]` 记录 | 至少补 3 条：topic×contribution（bubble plot 交叉）、§3→G5（互补结论→指南）、指南→流程（G1→§2.6, G2→Figure 1）。 | §2.6, §3, §4 | I |
| **FIX-6**: 为每个叶子补全取值空间、统计用途和缺失值语义 | A.2 各 leaf-* | 当前 leaf 取值空间全是泛化描述。应按 §4 建议树为每个叶子写可执行取值空间枚举。 | 原文对应章节 | C |
| **FIX-7**: 记录 absence evidence（无 quality rubric、无 meta-analysis） | A.2 新增 `[dim-petersen-2008-absence-fields]` | 添加 `[leaf-absence-quality-assessment]` 和 `[leaf-absence-meta-analysis]`，并写为 `absence_evidence` 证据角色。 | §3.4 | M |
| **FIX-8**: 扩展 A.2 证据条目 | A.2 证据表 | 从当前 4 条扩展到 10+ 条。至少追加：(a) §2.3 检索细节；(b) §2.5 keywording 规则；(c) §3.1 8 篇 SR 清单；(d) §3.4 Table 1 对比表；(e) §4 G1–G5 指南文本。 | 原文对应节号 | I |
| **FIX-9**: A.3 结论重新映射到原文 finding 路径 | A.3 结论表 | 新增：(a) finding 路径 A（频数→交叉→gap）；(b) finding 路径 B（SR 对比→Table 1→互补结论→G5）；(c) 对当前 C04–C07 的 leaf_definition 结论标注"当前仅 A1-M0--M6 投影，待 FIX-1–FIX-2 修正"。 | §2.6, §3, §4 | I |
| **FIX-10**: 记录原文 extraction form 字段 | A.2 新增 `[dim-petersen-2008-extraction-form]` | 至少列出：论文元数据、分类类别归属、归类理由（rationale）三个叶子。这直接支撑 Paper2 的 "字段级内容证据" 概念。 | §2.6 | M |
| **FIX-11**: 标注 C12 的临时性 | A.3-C12 行 | 在 C12 备注中说明：这 5 个原文候选叶子应在 FIX-1 完成后成为主维度树的一部分，C12 自身降级为迁移记录或删除。 | -- | M |

## 6. C/I/M 结论

### 6.1 C 级（Critical）：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

| 编号 | 问题 | 对 Paper2 的影响 |
|---|---|---|
| **C1** | 维度树使用 A1-M0--M6 元框架作为 Petersen 2008 的 schema 呈现，而非从原文结构派生（FIX-1） | Paper2 的核心故事是"从原文中抽取维度模式并演化"（paper_story.md §5 "维度模式"）。如果 A1-DT 阶段连 Peterse2008 的三维分类方案、Map vs Review 对比、G1–G5 指南都没有正确复原，A2a 抽取的"维度模式"将在错误的基线上出发，整个证据链的源头失真。Petersen 2008 又是 SMS 方法学母文，其分类方案直接影响 Paper2 的维度模式设计，此错误会 cascade 到后续所有依赖此法论文的维度节点。 |
| **C2** | 原文三维 facet 的取值空间缺失（FIX-2、FIX-6） | contribution facet 的 6 值枚举和 research-type 的 6 值枚举是 Petersen 2008 最核心的、可被 Paper2 直接引用或对比的分类方案。缺失这些取值空间意味着 A2a 无法判断 Peterse2008 的分类粒度，也无法与自己的维度模式做覆盖度比较。 |
| **C3** | A.2 证据仅 4 条，无法支撑对 10 页方法论文的完整维度覆盖（FIX-8） | pattern-field-schema.md §8.4 要求 A.2 证据必须与 A.3 结论回链。当前 4 条证据支撑 12 条 A.3 结论和一棵 6 分支树，证据-结论比严重不足。A2a 在做精确页码/表图锚定时会发现大量 A.3 结论没有明确证据来源。 |

### 6.2 I 级（Important）：会实质影响维度树可用性、原文 schema 复原、证据可审计性

| 编号 | 问题 |
|---|---|
| **I1** | Map vs Review 对比整章无独立维度节点（FIX-3）。原文 §3 包含 2 个 RQ、8 篇 SR 清单和 Table 1，是方法论文的重要贡献，缺少此维度会使得 Paper2 无法区分"方法论文自身的发现"与"方法论文的对比框架"。 |
| **I2** | G1–G5 扩展指南无独立维度节点（FIX-4）。5 条指南是原文的核心输出之一，且 G1/G2/G5 直接对应 Paper2 关注的"可视化"和"方法组合"，缺少会丢失重要启发。 |
| **I3** | 无关系边记录（FIX-5）。原文的 topic × contribution 交叉、指南与流程的支撑关系是维度树"语义网络"的核心。缺少关系边意味着维度树退化为扁平字段表。 |
| **I4** | 原文 RQ pattern 未被复原（FIX-3）。原文有显式 RQ1/RQ2（§3.1），是 A1-M0 的原文级实例，但当前 A.2 中没有将这些 RQ 作为独立维度叶子。 |
| **I5** | A.3 结论未映射到原文 finding 路径（FIX-9）。原文有两条清晰路径（频数→gap、对比→互补→指南），当前 A.3 只有通用 leaf_definition 和 migration_boundary，缺少 finding 路径级映射。这会让 A2a 在做 candidate_finding 抽取时缺少原文级参照。 |
| **I6** | 证据条目覆盖不足（FIX-8）：§2.3 检索细节、§2.5 keywording 规则、§3.1 SR 清单、§3.4 Table 1、§4 G1–G5 指南文本均无独立证据条目。 |

### 6.3 M 级（Minor）：不阻塞的清晰度或维护性建议

| 编号 | 问题 |
|---|---|
| **M1** | 未记录 absence evidence（无 quality rubric / 无 meta-analysis）（FIX-7）。SMS 不做 quality assessment 是区分 SMS 与 SR 的关键特征，记录为 absence_evidence 有助于 Paper2 方法设计。 |
| **M2** | 原文 extraction form 字段未展开（FIX-10）。§2.6 的描述抽取表（metadata + category + rationale）与 Paper2 "字段级内容证据"直接对应，值得显式记录。 |
| **M3** | C12 "原文候选叶子"的临时性未标注（FIX-11）。当前 5 个原文候选叶子在 C12 中方向正确但缺少取值空间、统计用途和证据链，应标注为"待 FIX-1 完成后合并入主维度树"。 |
| **M4** | A.3-C04–C07 标注"可为 Paper2 维度树候选节点"可能误导 A2a（见 §3.2 最后一条检查项）。建议显式标注"当前叶子仅来自 A1-M0--M6 投影"。 |
| **M5** | 原文 artifact / replication 状态未记录（§3.2 末条）。SMS 案例提交状态和 8 篇 SR 的可追溯性可作独立证据。 |

### 6.4 最终建议

**NEEDS FIX**。

当前 `review.md` 的 §2（论文内容详读）质量较高，正确识别了原文的五步流程、三维分类方案、keywording 方法和 Map vs Review 对比。但 A.2 维度树使用了 A1-M0--M6 元框架投影，而非从原文自身结构重建。这导致维度树**过小**（6 个通用分支承载 8 个原文独立维度区）、**原文 schema 未复原**（三维 facet 取值空间缺失、§3/§4 整章缺失）、**证据链不足**（4 条证据支撑 12 条结论）。

修复的核心动作是：**将 A.2 维度树从"A1-M0--M6 投影"改为"原文结构驱动"**，采纳本报告 §4 的建议树作为基线，补齐取值空间、统计用途、缺失值语义和关系边，并扩展 A.2 证据条目到 10+ 条。修复后，当前 §2 的高质量详读文本和 C12 的 5 个原文候选叶子可以自然融入新树，不需要重写全文。

按 Paper2 paper_story.md §13.3 的禁止主张中"脚手架是目标系统综述证据池或三级综述"，本审计不存在将 Peterse2008 写成领域证据池的风险——当前 review.md 的 A1 角色判定（"只作为方法学模式种子"）和 SUMMARY 的三池归属（"方法学参考池，不进主统计池"）是正确的。风险完全集中在**维度树复原完整性**上，修复范围可控。

---

*审计工具：deepseek | 目标论文：Petersen et al. 2008 | 审计路径：`audits/a1dt-19x3/results/petersen-2008-systematic-mapping__deepseek.md`*
