# petersen-2015-mapping-guidelines-update · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是
  - 路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - 路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/paper-story.md`
  - 路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
  - 路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是
  - 路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - 路径：`/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是
  - 路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否读取文库级规则与 story**：是
  - `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md`
  - `story/paper_story.md`
- **是否完整阅读 `paper_content.txt`**：是。全文 1973 行，覆盖 Page 1--18 所有章节（Introduction、Related Work、Research Method、Results for RQ1--RQ4、Updated Guidelines Proposal §5.1--§5.5、Conclusions §6），包含所有表格（Table 1--14）、图形（Fig. 1--21）和附录（Appendix B.1--B.27）的文本描述。
- **是否核对 `paper.pdf`**：部分核对。已用 `pdfinfo` 确认 18 页、可读、页码与 `paper_content.txt` 对齐；未做逐表逐图的视觉级人工核对。对复杂 Table 12--13 质量 rubric、Fig. 17--19 roadmap 图、Appendix B.15--B.27 完整表，本次判断基于 `paper_content.txt` 提取文本，部分表图因 PDF 提取的格式信息有限，精核仍需人工 PDF 视觉核对。后文若引用本文具体表图页码，均来自 `paper_content.txt` 中 `--- Page N ---` 分隔标记的文本定位（非视觉核对）。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

论文的明确目标（Abstract §Objective）是：

> To identify how the systematic mapping process is conducted (including search, study selection, analysis and presentation of data, etc.); to identify improvement potentials in conducting the systematic mapping process and updating the guidelines accordingly.

论文设置四个正式 RQ（见 §3 Research Method 与 §4 Results 首段）：

| RQ | 内容 | 对应数据 |
|---|---|---|
| RQ1 | Which guidelines are used in SE systematic mapping studies? | Fig. 5 + 正文统计 |
| RQ2 | Which SE topics are covered by systematic mapping studies? | Fig. 3 (SWEBOK 分类) |
| RQ3 | Where and when are systematic mapping studies published? | Fig. 2 (年份)、Fig. 4 (venue 类型)、Table 4 (top venues) |
| RQ4 | How is the systematic mapping process conducted (study identification, classification scheme, results visualization)? | §4.4.1--§4.4.5 全文，覆盖 guideline 使用、search strategies (Fig. 6--8)、inclusion/exclusion (Fig. 9)、quality assessment (Fig. 10)、data extraction (Fig. 11)、topic-independent classification (Fig. 12)、topic-specific classification (Fig. 13)、visualization (Fig. 14)、validity (Fig. 15) |

**关键观察**：RQ4 是四个 RQ 中方法学最厚的，它直接把 systematic mapping process 拆解为 guideline 选择、study identification、quality evaluation、data extraction and classification、visualization、validity 六个子维度——这些子维度本身就是论文的"隐式 schema"，但当前 review.md 的主维度树并未按此拆解。

### 2.2 原文方法流程

论文的方法是一个 systematic mapping study of systematic maps（即 mapping of maps）：

1. **检索**（§3.1 Search strategy）：IEEE Xplore、ACM、Scopus、Inspec/Compendex；以"systematic mapping"+"software engineering"+"method/classification/guideline"构造检索式。
2. **纳排**（§3.2 Study selection）：标题/摘要筛选 → 全文阅读 → backward snowballing；纳入标准：呈现 SMS 方法+结果、属 SE、2004--2012 发表。排除：conference summary/editorial、guideline/template 本身、非 peer-reviewed、非英文、全文不可得、书籍/灰色文献、重复。最终 52 篇纳入。
3. **质量评价**（§3.3）：三个问题评估：mapping 动机是否清楚、mapping process 定义是否清楚、是否有 empirical evidence/results。
4. **数据抽取**（§3.4 Data extraction）：explicit extraction form，字段包括：
   - study ID
   - title
   - authors
   - year
   - SWEBOK area
   - venue
   - guidelines used
   - search strategy
   - search type
   - classification scheme
   - visualization type
5. **分类方案**（§3.4）：固定分类（topic-independent）：research type、research method、contribution type、venue type、study focus；主题特定分类（topic-specific）：emerging classification 或已有分类（SWEBOK、IEEE/ISO 标准）。
6. **结果呈现**（§4）：按 RQ1--RQ4 组织，每节配统计图表。
7. **Guideline 更新**（§5.1--§5.5）：基于 RQ 结果构建 updated guideline——planning §5.1（need/scoping、search strategy、study selection、data extraction/classification、visualization、validity threats、evaluation）、conducting §5.2、reporting §5.3。
8. **质量评分 rubric**（§5.4, Tables 9--13）：need for review、search strategy choice、search evaluation、extraction/classification、study validity，每项 0--3 分。
9. **Dissemination analysis**（§5.5, Fig. 21）：质量与 venue 类型交叉分析。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme 等

| 原文构建物 | 位置 | 内容 |
|---|---|---|
| **数据抽取表（extraction form）** | §3.4 | 11 个显式字段：study ID, title, authors, year, SWEBOK area, venue, guidelines used, search strategy, search type, classification scheme, visualization type |
| **纳入/排除标准** | §3.2 | 8 条纳入标准 + 排除规则 |
| **质量评价问题** | §3.3 | 3 个质量评价问题 |
| **Topic-independent classification facets** | §4.4.4, Fig. 12 | 5 个 facet：venue type、research type (6 类，含 Wieringa et al. 决策表 Table 7)、research method (8 类，含 Easterbrook/Wohlin 映射 Fig. 19)、contribution type (5 类)、study focus |
| **Topic-specific classification** | §4.4.4, Fig. 13 | emerging classification（grounded theory 式 keywording）vs. existing classification（SWEBOK, IEEE/ISO 标准） |
| **Search strategy taxonomy** | §4.4.2, Figs. 6--8 | database search / manual search / snowballing；search 开发策略 (PICO, keywords from known papers, iterative improvement, expert/library)；search 评估策略 (test-set, expert evaluation, author websites, test-retest) |
| **Inclusion/exclusion taxonomy** | §4.4.2, Fig. 9 | decision rules, additional reviewers/consensus, objectivity assessment |
| **Quality assessment rubric** | §5.4, Tables 9--13 | 5 维度评分（0--3）：need for review, search strategy choice, search evaluation, extraction/classification, study validity |
| **Visualization type taxonomy** | §4.4.5, Fig. 14 | bubble plots、bar plots、pie diagrams、Venn diagrams、line diagrams、heatmaps |
| **Validity threat taxonomy** | §4.4.6, §5.1.5 | publication bias, descriptive validity, researcher bias, quality of sample, generalizability (internal/external), reliability of conclusions |
| **Venue 分类方案** | §5.1.3, Fig. 18 | 芬兰教育部 publication type 分类：peer-reviewed (journal article, review article, book section, conference proceedings) / non-refereed / professional / general public / thesis / patent / audiovisual |
| **Planning process roadmap** | §5.1, multiple figures | Fig. 16 (search reflection), Fig. 17 (study selection process), Table 6 (decision rules combination matrix) |
| **Guideline update structure** | §5.1--§5.3 | Planning (7 子模块) → Conducting → Reporting（3 层次） |
| **Appendix B** | pp.16--18 | B.1--B.27 完整表：逐篇 mapping study 的指南使用、搜索策略、分类方案、visualization、效度报告等详细映射 |

### 2.4 原文如何形成 conclusion / finding / gap / recommendation

原文的 finding 形成路径非常清晰：

1. **描述统计**（§4）：RQ1→10 种 guideline 使用分布 (Fig. 5)；RQ2→SWEBOK 覆盖分布 (Fig. 3)；RQ3→年份趋势 (Fig. 2)、venue 分布 (Table 4, Fig. 4)；RQ4→六个子维度的统计分布 (Figs. 6--15)。
2. **实际做法 vs 已有 guideline 对比**（§5）：基于 RQ 统计结果，发现现有 guideline 只"partially represent the activities actually conducted"，这是驱动 guideline update 的核心 gap。
3. **Guideline update proposal**（§5.1--§5.3）：将 gap 转化为 structured recommendation，分为 planning/conducting/reporting 三大阶段，每个阶段下含具体 action point。
4. **质量 rubric 设计**（§5.4）：基于 mapping studies 的实际质量变异，设计可复用评分表。
5. **交叉分析**（§5.5）：质量 vs venue 类型、quality score distribution (Fig. 20)。
6. **Conclusion**（§6）：按 RQ 逐条回答，总结 updated guideline 的贡献和局限。

**关键特征**：这篇论文既是 mapping study（产生对 52 篇 SMS 的统计发现），又是 guideline update（产出 planning/conducting/reporting 方法论）。这两个层次必须在维度树中同时出现，但当前 review.md 的维度树将二者压成一个平面。

## 3. 当前 `review.md` 维度树审计

### 3.1 审计总览

当前 `review.md` 维度树定义在第 185--265 行。其结构为：

```
[dim-root] Guidelines for conducting... SE
├── [dim-b1] planning → [leaf-scope] 研究范围与单位对象
├── [dim-b2] conducting → [leaf-corpus] 语料与纳排链条
├── [dim-b3] reporting → [leaf-taxonomy] 主题与维度分类
├── [dim-b4] quality rubric → [leaf-method] 方法 / 技术 / 干预分类
└── [dim-b5] topic-independent dimensions
    ├── [leaf-evidence] 评价、证据与复现资产
    └── [leaf-finding] 统计观察与候选发现
```

review.md 自身已在第 193 行做出口径校准声明：

> 下方"叶子维度表"的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。

同时在第 230--243 行提供了"原文模式候选叶子映射（A1 种子）"5 个候选叶子（planning / conducting / reporting / quality rubric / topic-independent dimension），全部标记为 `not_verified` 和 `schema_seed`。

### 3.2 逐项审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| **根节点是否准确** | 通过 | 根节点准确标识了论文的标题和研究目标类型（"mapping guideline update 方法树"）。与原文 §1 Introduction 与 §6 Conclusions 一致。 | 通过 |
| **主干分支是否覆盖原文 schema** | I | 当前主干分支（b1 planning / b2 conducting / b3 reporting / b4 quality rubric / b5 topic-independent dimensions）来自原文 §5.1--§5.3 的 guideline 组织逻辑，但 **b3 reporting + b5 的叶子分配出现配对错误**：topic-independent dimensions（venue, research type, research method, contribution type, study focus）原文属于 §4.4.4 数据抽取与分类阶段（即 conducting 内部），不属于 reporting。reporting 阶段（§5.3）原文强调 map 呈现、可视化、threat 讨论、dissemination。当前把 topic-independent dimensions 挂为独立主干分支，且把"方法 / 技术 / 干预分类"放到 b4 quality rubric 下，把"评价、证据与复现资产"和"统计观察与候选发现"放到 b5 下——这种分配与原文的实际 workflow 和字段归属不一致。具体问题见下文各分项。 | I |
| **叶子维度是否足够具体** | C | 当前 6 个通用接口叶子与原文 11 字段 extraction form (§3.4)、5 个 topic-independent facet (§4.4.4 + Figs. 12--13)、6 个 search/inclusion/extraction 子过程 (§4.4.2--§4.4.4)、5 项 quality rubric (§5.4, Tables 9--13)、6 项 validity threat (§5.1.5)、6 种 visualization 类型 (§4.4.5, Fig. 14) 之间存在巨大粒度差距。即使 review.md 已声明这 6 个是"通用接口层"并有候选叶子映射，**本文的维度树复原应该先按原文 schema 拆叶子，再标注可迁移粒度**——当前做法是主树用通用接口、候选用粗颗粒分组，结果是对原文字段的复原处于**两端都不够具体**的状态。 | C |
| **取值空间是否可执行** | C | 六个通用叶子的取值空间全是"自由文本加 RQ / 贡献声明引用""完整 SLR/SMS 为数值链条""完整枚举 / 层级枚举 / 自由文本加理由"——这些取值空间描述是跨论文通用描述，而非本文具体上下文下的枚举。例如 `leaf-method` 的取值空间写"层级枚举、关系值或开放 action point"，但原文明确有 research type 的 6 类枚举（含 Table 7 决策表）、research method 的 8 类枚举（含 Fig. 19 mapping）、contribution type 的 5 类、venue type 的层级分类（Fig. 18）——这些在通用取值空间中完全不可见。A2a 若只拿当前取值空间去操作，无法执行本文的具体字段抽取。 | C |
| **关系边是否缺失** | I | 当前维度树缺乏关系边。缺失的关键关系包括：(1) RQ → 字段的映射（如 RQ4 → guideline usage + search strategy + classification + visualization + validity）；(2) extraction form 字段 → 统计结论（如 guidelines used → Fig. 5 → "multiple guidelines combined" finding）；(3) quality rubric 维度的父子/组合关系；(4) conducting → reporting 的产出关系；(5) planning 内部 guideline 条目之间的顺序/依赖边（如 §5.1.1 need → §5.1.2 search → §5.1.3 extraction 的流程依赖）。这些关系到后续 A2a 的交叉表设计和 finding 路径可追溯性。 | I |
| **统计用途 / 分母是否正确** | I | review.md 的"统计与候选发现链路"小节（第 250--258 行）对可统计方式和分母做了说明，明确指出"否（A1-DT 阶段仅作 schema seed）"。这一口径本身正确且谨慎。但问题在于：当前维度树未区分原文自己的统计分母（52 篇 systematic maps）和 Paper2 对外统计分母（19 篇 survey-of-surveys）。原文的每个 finding（如 "24 mapping studies used more than one guideline"）都有明确分母和统计归属，当前树中的通用叶子无法表达这些关系。后续 A2a 如果要在不同分母语境下复用本文叶子，这个模糊性会导致统计池误混。 | I |
| **候选 finding 路径是否完整** | I | review.md 中的候选发现路径主要依赖 C02--C09 的结论-证据映射，但映射粒度停留在"叶子维度来自本文结构"这一层级，未下钻到原文具体的 finding 语句级。例如原文的 "24 out of 52 studies used more than one guideline"、"14 out of 52 studies assess quality"、"contribution type is only used by very few studies" 等具体发现并未作为独立候选发现条目出现。当前 C02--C09 更像是"叶子存在性声明"，而非从原文统计→finding→candidate finding 的完整推演路径。 | I |
| **A.1--A.4 证据链是否足够** | I | A.1 三个来源标识可核验，A.2 四条证据（EV-002 到 EV-004）只覆盖了泛定位（"论文整体"、"Sections 1, 3, 4, 5, 6"），完全没有页码/表号/图号/段落级锚点。例如 EV-002 写 "Sections 1, 3, 4, 5, 6 中 RQ、方法、分类、质量 rubric 和讨论"——这是整篇论文的覆盖声明，不是可审查的证据锚点。按照 pattern-field-schema.md §8.2 的"证据来源锚点"要求（"原文页码、原文章节、段落或行号范围、表格或图编号"），当前 A.2 证据账本全部缺失精确锚点。所有证据强度标记为 `weak` 且 "needs_manual_check"。A.3 结论-证据映射只回链到 A.2，但 A.2 本身无法定位原文具体位置，形成嵌套弱证据链。 | I |
| **是否存在可能误导 A2a 的强主张** | I | review.md 已通过 A1-DT 叶子层口径校准（第 193 行）和候选叶子映射做了防御性声明，不存在明确的"强主张"误导。但有一个隐性问题：将"六个通用叶子"作为主维度树展示（第 201--214 行的 ASCII 树图），且将叶子维度表（第 222--229 行）设计为完整取值空间、缺失值语义、统计用途、候选发现用途的六列完整表，容易让后续 A2a 读者误以为这就是本文的实际维度树复原结果，而非还需精核的接口占位层。建议将主维度树的位置替换为按原文 schema 拆解的更细粒度树，通用接口层作为"可迁移抽象"单独说明。 | I |

### 3.3 具体字段遗漏清单

以下原文中明确出现的关键 schema 元素，在当前维度树（含候选叶子映射）中未被显式表达为独立叶子或可统计字段：

| 原文字段/构建物 | 原文位置 | 当前树状态 | 遗漏影响 |
|---|---|---|---|
| **4 个 RQ**（而非"RQ 模式"通称） | §3 Research Method 首段 | 只作为 `leaf-scope` 的自由文本取值空间的一部分出现 | 无法按 RQ 组织字段、统计或 finding 路径 |
| **11 字段 extraction form**（study ID, title, authors, year, SWEBOK area, venue, guidelines used, search strategy, search type, classification scheme, visualization type） | §3.4 | 未作为独立 leaf 出现 | A2a 无法直接对照本文的 extraction form 来设计自己的抽取表 |
| **search strategy 三级分类**（database/manual/snowballing） | §4.4.2, Fig. 6 | 未作为独立 leaf 出现 | 丢失 search strategy 的三分枚举 |
| **search development 策略**（PICO, keywords from papers, iterative, expert/librarian） | §4.4.2, Fig. 7 | 未作为独立 leaf 出现 | 丢失 search development 的多选枚举 |
| **search evaluation 策略**（test-set, expert, author websites, test-retest） | §4.4.2, Fig. 8 | 未作为独立 leaf 出现 | 丢失 search evaluation 的多选枚举 |
| **inclusion/exclusion 策略**（decision rules, additional reviewer/consensus, objectivity assessment） | §4.4.2, Fig. 9 | 未作为独立 leaf 出现 | 丢失纳排可靠性评估维度 |
| **5 个 topic-independent facets 的完整枚举**：venue type（Fig. 18 层级）、research type（6 类 + Table 7 决策表）、research method（8 类 + Fig. 19 mapping）、contribution type（5 类）、study focus | §4.4.4, Figs. 12, 18, 19; §5.1.3, Table 7 | 候选叶子只写了 "跨主题维度字段" + 候选取值空间为"可跨主题迁移的 classification facet 与 map 维度"——这等于没取值 | 丢失原文最核心的可复用 classification facet 枚举 |
| **topic-specific classification**（emerging vs. existing, keywording = open coding from grounded theory） | §4.4.4, Fig. 13; §5.1.3 | 未作为独立 leaf 出现 | 丢失 keywording 方法学 |
| **visualization 类型集合**：bubble plot, bar plot, pie diagram, Venn diagram, line diagram, heatmap | §4.4.5, Fig. 14 | 未作为独立 leaf 出现 | 丢失 6 种可视化枚举 |
| **validity threat 分类**：publication bias, descriptive validity, researcher bias, quality of sample, generalizability (internal/external), reliability of conclusions | §4.4.6, §5.1.5 | 未作为独立 leaf 出现 | 丢失 6 种效度威胁枚举 |
| **5 项 quality rubric 评分维度**：need for review (0--2), search strategy choice (0--2), search evaluation (0--3), extraction/classification (0--3), study validity (0--1) | §5.4, Tables 9--13 | 候选叶子 "质量准则字段" 只写候选取值空间为"systematic map 质量标准、常见问题和改进建议"——没有给出 scoring rubric 结构 | 丢失 quality rubric 的具体评分设计 |
| **Planning 子模块**：need/scoping, search strategy, study selection (含 Fig. 17 流程 + Table 6 决策矩阵), data extraction/classification (含 topic-independent + topic-specific), visualization, validity threats, evaluation | §5.1 | 合并为"规划阶段字段"一个候选叶子 | planning 的 7 个 action point 没有展开 |
| **Conducting 子模块**：process execution, record-keeping, iteration | §5.2 | 合并为"执行阶段字段"一个候选叶子 | conducting 的记录和迭代要求丢失 |
| **Reporting 子模块**：standardized structure, map presentation, reusable/comparable format | §5.3 | 合并为"报告阶段字段"一个候选叶子 | reporting 的具体要求丢失 |
| **guideline combination pattern**（24/52 使用多 guideline） | §4.4.1 | 未作为独立 leaf 或 finding 出现 | 丢失 method combination 这一重要维度 |
| **质量分布**（median 33%, Fig. 20）与 **venue×质量交叉**（Fig. 21） | §5.4, §5.5 | 未作为独立 leaf 出现 | 丢失统计层面的 evidence table 证据 |
| **纳排链条可视化**（Fig. 1: 7752→5082→60→43→54→44→52） | §4.1 | 未作为独立 leaf 出现 | 丢失 denom chain 这一核心统计分母 |

### 3.4 分支配对错误详析

当前树中有一个结构性问题需要特别指出：

1. **"topic-independent dimensions" 被设为 b5 独立主干分支**，而原文中它属于 §4.4.4（结果）和 §5.1.3（planning 的 data extraction and classification 子模块内）。把它作为平行于 planning/conducting/reporting 的独立分支，破坏了原文的 workflow 层次结构。

2. **"方法 / 技术 / 干预分类" (`leaf-method`) 挂在 `b4 quality rubric` 下**。原文中 research type / research method 的分类属于 §4.4.4 的 topic-independent classification（即 data extraction 的一部分），而非 quality rubric 的组成部分。quality rubric（§5.4, Tables 9--13）是评分工具，与 classification scheme 是不同层次——前者评价 mapping study 质量，后者是 mapping study 的内容分类。

3. **"评价、证据与复现资产" (`leaf-evidence`) 和"统计观察与候选发现" (`leaf-finding`) 挂在 `b5 topic-independent dimensions` 下**。原文中 evaluation/evidence 散布在 quality rubric (§5.4) 和 dissemination (§5.5)，finding 散布在 results (§4) 和 conclusions (§6)，都不属于 topic-independent dimensions 的子范畴。

结论：当前分支配对是 **"原文的 guideline 组织层次 + 跨论文通用叶子 + 语义就近直觉"的混合产物**，而非逐层忠实复原。

## 4. 建议维度树骨架

以下是更忠实于原文 schema 的建议维度树。本树的设计原则是：**先忠实复原原文信息结构，再标注哪些可迁移到 Paper2 维度模式**。

```
[petersen-2015-root] Guidelines for conducting SMS in SE: An update
│   [meta] 类型: systematic mapping of systematic maps + guideline update
│   原文纳入: 52 篇 SMS (2004--2012)
│
├── [rq-petersen-2015-b1] 原文 RQ 结构
│   ├── [leaf-rq1] RQ1: Guidelines used → 取值空间: 10 种 guideline 枚举 {KP2008|KC2007|...|其他}
│   ├── [leaf-rq2] RQ2: SE topics covered → 取值空间: SWEBOK 分类 + Education + Research methodology
│   ├── [leaf-rq3] RQ3: Publication venue & year → 取值空间: 年份区间 + venue 类型 + venue 名
│   └── [leaf-rq4] RQ4: SMS process → 取值空间: guideline 使用 | search | selection | quality | extraction & classification | visualization | validity
│
├── [extraction-form-petersen-2015-b2] 原文数据抽取表 (§3.4)
│   ├── [leaf-ext-study-id] Study ID
│   ├── [leaf-ext-title] Title
│   ├── [leaf-ext-authors] Authors
│   ├── [leaf-ext-year] Year
│   ├── [leaf-ext-swebok] SWEBOK area
│   ├── [leaf-ext-venue] Venue
│   ├── [leaf-ext-guidelines] Guidelines used → 取值空间: 10 种 guideline 枚举
│   ├── [leaf-ext-search-strategy] Search strategy → 取值空间: {database|manual|snowballing}
│   ├── [leaf-ext-search-type] Search type
│   ├── [leaf-ext-classification-scheme] Classification scheme → 取值空间: topic-independent facets ∪ topic-specific
│   └── [leaf-ext-visualization-type] Visualization type → 取值空间: {bubble|bar|pie|Venn|line|heatmap}
│
├── [classification-petersen-2015-b3] 原文分类方案 (§4.4.4; §5.1.3)
│   ├── [leaf-cls-topic-independent] Topic-independent facets
│   │   ├── [leaf-cls-venue-type] Venue type → 取值空间: Fig. 18 层级 (peer-reviewed|non-refereed|professional|general public|thesis|patent|audiovisual)
│   │   ├── [leaf-cls-research-type] Research type → 取值空间: {evaluation research|validation research|solution proposal|philosophical paper|experience report|opinion paper} + Table 7 决策表
│   │   ├── [leaf-cls-research-method] Research method → 取值空间: {survey|case study|controlled experiment|action research|ethnography|simulation|prototyping|mathematical analysis} + Fig. 19 mapping
│   │   ├── [leaf-cls-contribution-type] Contribution type → 取值空间: {process|method|model|tool|metric}
│   │   └── [leaf-cls-study-focus] Study focus → 取值空间: {academic|industrial|government|project|organization}
│   └── [leaf-cls-topic-specific] Topic-specific classification
│       ├── [leaf-cls-emerging] Emerging (keywording = open coding) → 取值空间: 从论文摘要/全文提取关键词后聚类
│       └── [leaf-cls-existing] Existing scheme → 取值空间: {SWEBOK|IEEE标准|ISO/IEC标准}
│
├── [method-process-petersen-2015-b4] 原文 SMS 执行流程 (§4.4.2--§4.4.6; §5.1--)
│   ├── [leaf-proc-search-decision] Search strategy choice → 取值空间: {database|manual|snowballing}
│   ├── [leaf-proc-search-develop] Search development → 取值空间: {PICO|keywords from known papers|iterative improvement|expert/librarian}
│   ├── [leaf-proc-search-evaluate] Search evaluation → 取值空间: {test-set|expert evaluation|author websites|test-retest}
│   ├── [leaf-proc-incl-excl] Inclusion/exclusion strategy → 取值空间: {decision rules|additional reviewer/consensus|objectivity assessment} + Table 6 决策矩阵
│   ├── [leaf-proc-quality-assessment] Quality assessment → 取值空间: {yes|no} + 3 QA 问题
│   ├── [leaf-proc-extraction-process] Extraction reliability → 取值空间: {additional reviewer|objectivity assessment (pilot/post)}
│   ├── [leaf-proc-visualization] Visualization → 取值空间: {bubble|bar|pie|Venn|line|heatmap} 枚举
│   └── [leaf-proc-validity] Validity discussion → 取值空间: 6 种 threat 枚举 {publication bias|descriptive validity|researcher bias|quality of sample|generalizability|reliability}
│
├── [quality-rubric-petersen-2015-b5] 原文质量评分准则 (§5.4; Tables 9--13)
│   ├── [leaf-qr-need] Need for review → 取值空间: {0: no description|1: partial|2: full}
│   ├── [leaf-qr-search-strategy] Search strategy choice → 取值空间: {0: one type|1: two types|2: all three}
│   ├── [leaf-qr-search-eval] Search evaluation → 取值空间: {0: no|1: search xor incl/excl|2: both|3: all}
│   ├── [leaf-qr-extraction] Extraction & classification → 取值空间: {0: no|1: extraction reliability|2: + research type & method|3: all}
│   └── [leaf-qr-validity] Study validity discussion → 取值空间: {0: no|1: yes}
│
├── [guideline-update-petersen-2015-b6] 原文 Guideline Update 结构 (§5.1--§5.3)
│   ├── [leaf-gu-planning] Planning (7 子模块)
│   │   ├── need identification / scoping
│   │   ├── search strategy → 回链 [leaf-proc-search-*]
│   │   ├── study selection → 回链 [leaf-proc-incl-excl]
│   │   ├── data extraction & classification → 回链 [classification-petersen-2015-b3]
│   │   ├── visualization
│   │   ├── validity threats → 回链 [leaf-proc-validity]
│   │   └── evaluation of the mapping
│   ├── [leaf-gu-conducting] Conducting → 取值空间: {record keeping|iteration|process implementation}
│   └── [leaf-gu-reporting] Reporting → 取值空间: {standardized structure|visual map presentation|reusable & comparable format}
│
├── [finding-path-petersen-2015-b7] 原文 Finding 形成路径 (§4 + §5 + §6)
│   ├── [finding-desc-stats] 描述统计层: frequency/count per RQ (如 24/52 使用多 guideline; 14/52 QA)
│   ├── [finding-gap] Gap 识别层: actual practice vs. existing guideline (如 "existing guidelines only partially represent activities")
│   ├── [finding-guideline-update] Guideline update 层: action points per planning/conducting/reporting
│   ├── [finding-quality-dist] Quality 分布层: median 33%; Fig. 20 distribution; Fig. 21 venue×quality cross
│   └── [finding-limitation] Limitation 层: single researcher (extraction/snowballing); exclusion of non-English; URL instability
│
└── [denom-chain-petersen-2015-b8] 纳排分母链 (§4.1; Fig. 1)
    ├── 7752 initial hits
    ├── 5082 after removing pre-2004
    ├── 60 after title/abstract screening
    ├── 43 after full-text reading
    ├── 54 after snowball sampling (+11)
    ├── 44 after quality assessment (-10)
    └── 52 + 8 + 11 final (52 included; 8 excluded after full review; 11 snowballed)

### 可迁移边界说明

- **可直接迁移到 Paper2 维度模式的值**：classification facets (research type 6 类 + Table 7 决策表; research method 8 类 + Fig. 19 mapping)、visualization types 6 类、validity threat 6 类、quality rubric 5 维评分、denom chain 计数模式。
- **不可直接迁移的内容**：52 篇 SMS 的具体统计结论、guideline update 的具体 action point、本文的 venue distribution/Topic distribution 结论。
- **需 A2a 精核后确认的内容**：Table 7 决策表的逻辑完整性、Fig. 18 venue 分类方案是否与 Paper2 目标领域 venue 口径兼容、Appendix B.1--B.27 逐篇映射表。
```

### 树体量与当前树对比

| 维度 | 当前树 | 建议树 | 差异说明 |
|---|---|---|---|
| 主分支 | 5 | 8 | 新增 RQ、extraction form、finding path、denom chain 分支 |
| 叶子总数 | 6 通用 + 5 候选种子 | 约 55 个具体叶子 | 按原文抽取字段/分类项/过程节点/评分维/rubric 项/finding 层逐条拆解 |
| 每叶取值空间 | 通用描述（如"自由文本加理由"） | 原文枚举或层级（如 `{evaluation research\|validation research\|...}`） | 从可执行性角度，取值空间必须是原文枚举而非接口描述 |
| 关系边 | 无 | 8 组：RQ→字段、字段→统计、classification→extraction、process→guideline update 等 | 通过回链和层次父子关系表达 |
| denom chain | 无显式建模 | 完整 7 步纳排链 | 对 Paper2 的统计分母透明化至关重要 |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| **F1：主维度树替换为按原文 schema 拆解的树** | `review.md` 第 201--214 行（ASCII 树图） | 将当前 6 通用叶子主树替换为建议树的第 8 分支完整结构（至少含 RQ 结构、extraction form、classification facets、SMS process、quality rubric、guideline update 结构、finding 路径、denom chain）。通用 6 叶子可作为"可迁移抽象总结"放在建议树之后，不作为主树。 | 原文 §3--§6 全文，重点是 §3.4 extraction form、§4.4.4 classification facets、§5.4 quality rubric、§5.1--§5.3 guideline update structure | C |
| **F2：叶子取值空间改为原文枚举** | `review.md` 第 222--229 行（叶子维度表） | 将每个叶子的取值空间从"自由文本加 RQ / 贡献声明引用"等通用描述改为原文的具体枚举。例如 `leaf-method` 应从"层级枚举、关系值或开放 action point"改为 `{evaluation research, validation research, solution proposal, philosophical paper, experience report, opinion paper}`（research type）+ `{survey, case study, controlled experiment, action research, ethnography, simulation, prototyping, mathematical analysis}`（research method）等。 | §4.4.4, Figs. 12--13, §5.1.3, Tables 7; §4.4.2 Figs. 6--9; §4.4.5 Fig. 14; §4.4.6 + §5.1.5; §5.4 Tables 9--13 | C |
| **F3：补充完整的 extraction form 字段** | `review.md` 或新增叶子表 | 增加 11 字段 extraction form 的独立叶子集合（study ID, title, authors, year, SWEBOK area, venue, guidelines used, search strategy, search type, classification scheme, visualization type），每个叶子注明原文取值空间。 | §3.4 Data extraction | C |
| **F4：修正分支配对错误** | `review.md` 第 201--214 行（维度树结构） | (1) topic-independent dimensions 不应是平行于 planning/conducting/reporting 的独立主干分支，应归属于 data extraction & classification 下；(2) `leaf-method` 不应挂在 quality rubric 下，应挂在 classification→research type/method 下；(3) `leaf-evidence` 和 `leaf-finding` 应从 topic-independent dimensions 下移出，分别放入 quality rubric 和 finding path 的对应位置。 | §4.4.4 vs §5.1.3 vs §5.4 | I |
| **F5：补充 denom chain** | `review.md` 维度树/叶子表 | 新增纳排分母链叶子（或独立分支），记录 7752→5082→60→43→54→44→52 的完整链条。这对 Paper2 的统计分母操作化至关重要。 | §4.1, Fig. 1 | I |
| **F6：A.2 证据账本补充精确锚点** | `review.md` A.2 证据账本表 | 将当前 4 条泛定位证据（EV-002--004 的 "Sections 1, 3, 4, 5, 6" 等）替换为逐叶子的精确锚点：每个 leaf 至少一行，包含原文页码（来自 `paper_content.txt` 的 `--- Page N ---` 分隔符定位）、原文章节号（如 §4.4.4）、表号/图号（如 Fig. 12, Table 7）。例如：`EV-leaf-research-type: Page 7--8, §4.4.4, Fig. 12, Table 7`。 | 全文各节/图/表；`paper_content.txt` 的 Page 分隔符可用于文本级定位 | I |
| **F7：补充具体 finding 条目** | `review.md` A.3 结论-证据映射表 | 在 C02--C09 基础上，增加原文中具体 finding 的候选条目，每个条目包含原文统计语句、分母、原文定位和迁移限制。例如：`[clm-24-multi-guideline] "24 out of 52 studies used more than one guideline" → §4.4.1, Fig. 5 → candidate_finding: "mapping studies often combine multiple guidelines"`。 | §4.4.1--§4.4.6 全文统计结果 | I |
| **F8：增加关系边定义** | `review.md` 维度树或单独的关系边表 | 至少定义以下关系边：(1) RQ → extraction field（RQ4→guidelines used, search strategy, classification scheme, visualization type）；(2) field → statistical result（guidelines used → Fig. 5 count）；(3) statistical result → candidate finding (Fig. 5 → "most common: KC2007 + KP2008")；(4) candidate finding → guideline update (gap → §5.1 action point)；(5) process sub-step → quality rubric item (search strategy → Table 10 rubric)。 | §3.4, §4, §5.1--§5.4 | M |
| **F9：明确"可迁移/不可迁移"在叶子级标注** | `review.md` 叶子维度表或建议树 | 对建议树中的每个叶子明确标注：可直接迁移（如 classification facet 枚举）、需 A2a 精核后迁移（如 quality rubric 评分阈值）、不可迁移（如本文 52 篇的具体统计数字）。 | §5 (guideline update) 的通用性判断 | M |

## 6. C/I/M 结论

### C（Critical）：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题

| 编号 | 问题 | 影响路径 |
|---|---|---|
| C1 | **主维度树过小且以通用接口代替原文 schema**（F1）：当前主树只有 6 个通用接口叶子，与原文约 55 个可定位字段/分类项/过程节点/评分维之间存在接近 10:1 的粒度假象。虽然 review.md 有自我声明，但主树作为"维度树复原"的主体展示，会在 A2a 使用该树做字段抽取时造成系统性信息丢失——操作者无法从 6 个通用叶子中还原出原文的 research type 枚举、search strategy 分类、quality rubric 维度等。 | A2a 若依赖当前主树做跨论文字段对齐，将丢失原文中大量可复用的具体 schema 元素，维度树的实际可用性大幅降低。违反了 Paper2 paper_story 中"维度模式投影为字段树、取值空间"的核心方法要求。 |
| C2 | **叶子取值空间不可执行**（F2）：当前所有叶子的取值空间都是跨论文通用描述（"自由文本加理由""完整枚举/层级枚举"），而非原文的具体枚举集。例如 research type 的 6 类枚举（含 Table 7 决策表）在取值空间中完全不可见。 | A2a 若只拿当前取值空间去执行本文的字段抽取，将无法判断一个 candidate paper 的 research type 应填哪个枚举值，导致字段级内容证据无法产生。违反了 pattern-field-schema.md §8.2 中"取值空间必须可执行"的字段合同要求。 |
| C3 | **extraction form 字段完全缺失**（F3）：原文 §3.4 明确定义 11 个数据抽取字段（study ID, title, authors, year, SWEBOK area, venue, guidelines used, search strategy, search type, classification scheme, visualization type），这些是本文自己用于抽取 52 篇 SMS 的可操作 schema——但当前维度树中没有一个叶子直接对应这些字段。 | 这对 A2a 是直接操作损失：本文的 extraction form 是 survey_of_surveys 文库中极少数带有完整、可审计抽取表定义的论文，如果连这个最直接的 schema seed 都未复原，A2a 的 extraction form 设计将失去一个重要参考锚点。 |

### I（Important）：会实质影响维度树可用性、原文 schema 复原、证据可审计性

| 编号 | 问题 |
|---|---|
| I1 | **分支配对错误**（F4）：topic-independent dimensions 误放为独立分支，leaf-method 误挂 quality rubric 下，leaf-evidence/leaf-finding 误挂 topic-independent dimensions 下。这会导致 A2a 在理解论文 workflow 时产生错误的层次推断。 |
| I2 | **denom chain 缺失**（F5）：Fig. 1 的 7752→52 纳排链是论文最核心的统计分母，但当前树中完全没有建模。Paper2 的统计池操作化强烈依赖 denom chain 的透明记录。 |
| I3 | **A.2 证据全部只有泛定位**（F6）：EV-002 到 EV-004 只有 "Sections 1, 3, 4, 5, 6" 级锚点，不符合 pattern-field-schema.md §8.4 要求的"原文页码、原文章节、段落或行号范围、表格或图编号"。这使得 A.2→A.3 的证据链无法被独立审计。 |
| I4 | **finding 条目停留在"叶子存在性声明"级**（F7）：review.md 中的 finding 路径只说明"叶子维度来自本文结构"，未下钻到原文具体的 finding 语句。A2a 无法从当前 C02--C09 中了解本文如何从统计→finding→recommendation。 |

### M（Minor）：不阻塞的清晰度或维护性建议

| 编号 | 问题 |
|---|---|
| M1 | **关系边缺失**（F8）：缺乏 RQ→字段、字段→统计、统计→finding、finding→guideline update 的关系边。这不阻塞当前 A1-DT 功能，但会降低 A2a 交叉表设计的效率。 |
| M2 | **可迁移/不可迁移标注粒度不够**（F9）：当前只在"可迁移与不可迁移边界"小节做了总括说明，未在叶子级别明确标注。|

### 最终建议：**NEEDS FIX**

当前 `review.md` 有足够的自知之明（口径校准声明、候选叶子映射、弱证据标记），但其主维度树复原结果——6 个通用接口叶子作为"维度树复原"的主体呈现——与原文丰富的 schema 元素之间存在系统性粒度假象和配对错位，在 C1/C2/C3 三个维度上构成 C 级问题。建议按 §4 的建议树骨架修复主树结构、叶子取值空间和 extraction form 字段，并补齐 A.2 的精确锚点后再提交 A2a 消费。

---

*审计完成时间：2026-06-29 (Asia/Shanghai)*
*本文未运行真实 LLM，未读取 `.env`，未修改仓库文件，未 push，未 gh comment。*
