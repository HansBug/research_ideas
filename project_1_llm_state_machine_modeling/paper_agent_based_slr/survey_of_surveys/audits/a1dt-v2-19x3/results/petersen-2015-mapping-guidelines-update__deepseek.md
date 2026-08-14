I have now read all required files. Let me compose the comprehensive audit report.

---

# A1-DT v2 单篇全文审计报告：`petersen-2015-mapping-guidelines-update`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2015-mapping-guidelines-update` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是；已逐段通读 1973 行全文，覆盖 Introduction (§1)、Background (§2)、Method (§3)、Results (§4)、Guideline Updates (§5)、Conclusion (§6)、References、Appendix A/B |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；bibtex 已读、metadata.json 已读 |
| 是否打开或核对 `paper.pdf` | 否；本次审计基于 `paper_content.txt` 全文文本级阅读。`paper.pdf` 仅通过 `pdfinfo` 元数据确认 18 页，未做图表视觉版面级人工核对（已记录为 `needs_manual_check`） |
| 原文类型 | systematic mapping study of systematic mapping studies（SMS 之 SMS，即 tertiary mapping / meta-mapping）；同时产出 guideline update |
| 被编码样本单位 | 单个已发表的 systematic mapping study（primary study） |
| 样本数量 / 分母 | 57 篇 primary studies（初始检索 5569 → 去重 3708 → title/abstract 筛选 152 → full-text 后 46 → backward snowballing +11 = 57 → quality assessment 后仍 57 全计入） |
| 原生树类型 | **维度森林**（dimension forest）：一棵以"单篇 SMS 研究所执行的 mapping process"为核心的多层级编码森林，覆盖文献元数据树、检索策略子树、分类方案子树、可视化子树、效度子树 |
| 主统计池资格 | 是；属方法学统计池，非领域效果/因果统计池。其编码字段直接作为 A2a 对 SLR/SMS 类文献的 extraction form 种子 |
| 总体判定 | **needs repair**（需返修）：现有 `review.md` 的 A.1 维度树过于抽象，将原文丰富的 process-level 编码字段折叠为六个通用叶子；需按本报告 §3--§4 重写 A.1 原生树并更新 A.2 证据账本 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取范围

| 文件 | 读取状态 | 说明 |
|---|---|---|
| `paper_content.txt` | 全文通读 | 1973 行，覆盖 §1 Introduction、§2 Background and Related Work (§2.1--2.2)、§3 Research Method (§3.1--3.6)、§4 Results of the Mapping (§4.1--4.4)、§5 Guideline Updates (§5.1--5.3)、§6 Conclusion、Appendix A/B、References |
| `bibtex.bib` | 已读 | DOI、journal、authors、year、pages 一致 |
| `metadata.json` | 已读 | CCF 分类、eligibility、evidence_role 均确认 |
| `review.md` | 已读 | 348 行，含 §1 快速结论卡片、§2 详读、A.1--A.4 附录 |
| `paper.pdf` | 未做视觉核验 | 18 页已通过 pdfinfo 确认；Table 3/5/6/7/14、Fig. 1--21、Appendix B 表 B.15--B.27 的精确版面值仍需 PDF 视觉核对 |

### 1.2 关键原文证据锚点（12 个）

| 锚点编号 | 章节 | 线索 | 短引或释义 |
|---|---|---|---|
| EV-001 | §3.3 | 数据抽取表 Table 3 | 9 字段：Study ID、Article Title、Author、Year、Area (SWEBOK)、Venue、Guidelines、Search strategy、Search type、Classification schemes、Visualization type |
| EV-002 | §4.1 / Fig. 2 | RQ1 结果 | 2004--2012 年 57 篇 SMS 的逐年分布；2011--2012 显著增长 |
| EV-003 | §4.2 / Fig. 3 / Table B.15 | RQ2 结果：SWEBOK 主题分类 | 11 类别（Software design/testing/quality/requirements 等 + Education + Research methods）；testing 最多 |
| EV-004 | §4.3 / Fig. 4 / Table 4 | RQ3 结果：venue 分布 | Journal/Conference/Workshop 三分；14 篇期刊（IST、JSS 等） |
| EV-005 | §4.4.1 / Fig. 5 / Table B.17 | 使用的 guideline 枚举 | Kitchenham & Charters (2007) 最多；Petersen et al. (2008) 次之；多种组合 |
| EV-006 | §4.4.2 / Fig. 6--9 / Table B.18--B.21 | 检索策略四层子树 | 选库策略（DB/Snowballing/Manual）、构造检索（PICO/专家/迭代/关键词/标准）、评估检索（test-set/专家/test-retest）、纳排（criteria/多审/rule） |
| EV-007 | §4.4.3 / Fig. 10 / Table B.22 | 质量评价 | 14/57 有 QA；其余无 |
| EV-008 | §4.4.4 / Fig. 11--13 / Table B.23--B.25 | 数据抽取与分类 | 抽取过程（多审/客观标准/test-retest）；topic-independent facets（venue/research type/research method/study focus/contribution type）；topic-specific（emerging vs. standards-based） |
| EV-009 | §4.4.5 / Fig. 14 | 可视化类型 | Bubble plot、Bar plot、Pie diagram、Venn diagram、Heatmap |
| EV-010 | §4.4.6 / Fig. 15 | 效度讨论 | 45/57 讨论 validity threats |
| EV-011 | §5.1--5.3 / Table 5 | 更新后的 guideline 结构 | Planning（need/scoping → study ID → extraction/classification → visualization → validity）→ Conducting → Reporting |
| EV-012 | §5.3 / Table 14 | quality evaluation rubric | 5 活动 × 4 执行度（No/Min.E./Part.E./Full E.） |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象

原文纳入的 **57 篇 primary studies** 均为已发表的 systematic mapping studies（SMS）。每篇是一个"已完成的 mapping study"，作者对其逐一编码了：谁做的、哪年、什么主题、发在哪里、用了什么 guideline、如何检索/筛选/抽取/分类/可视化/评估效度。

样本单位不是 guideline item、tool、artifact 或 claim。它是 **assessed primary study**——即被 quality assessment 筛过后保留下来的 SMS 实例。

### 2.2 系统检索/纳排/数据抽取/编码方案

**有**，且为三级系统流程：
1. **检索**：IEEE Xplore、ACM、Scopus、Inspec/Compendex 四库；自定义检索式（systematic mapping + software engineering + method/classification/guideline 组合词）；EndNote 去重。
2. **纳排**：title/abstract → full-text → backward snowballing → quality assessment。纳排标准明确（见 §3.3）。
3. **数据抽取**：Table 3 的 9 字段结构化 template。第二作者抽取，第一作者复核。
4. **编码方案**：§4 的 analysis and classification 对抽取结果做了二次分组/主题化（例如将"检索策略"分入 choosing/developing/evaluating/inclusion-exclusion 四主题；将"分类"区分为 topic-independent vs. topic-specific）。

### 2.3 原文字段来源

字段来自四个层面，各自扮演不同角色：

| 层 | 来源 | 角色 |
|---|---|---|
| **数据抽取 schema** | Table 3（extraction form） | 对每个 primary study 的逐篇编码 |
| **结果分类维度** | §4.1--4.6 的统计分组（Figures + Appendix B 映射表） | 将逐篇编码聚合成可计数的维度 |
| **guideline 更新框架** | §5 / Table 5 | 综合 external guideline 对比 + 本文发现的 output schema |
| **quality evaluation rubric** | §5.3 / Table 14 | 评估 mapping study 执行完整度的评价表 |

### 2.4 RQ 与样本单位的关系

RQ 是**编码维度的组织线索**，不是树根：
- RQ1（guidelines used）→ 编码字段 "Guidelines"
- RQ2（topics）→ 编码字段 "Area in SE (SWEBOK)"
- RQ3（venues/time）→ 编码字段 "Venue" + "Year of Publication"
- RQ4（process）→ 所有 process-level 字段：Search strategy、Search type、Classification schemes、Visualization type，以及二次派生的诸多子维度

### 2.5 降级说明

无需降级为无系统样本库。本文有明确、可追溯的 57 篇 primary study 样本池和结构化编码方案。但需注意：
- 57 篇样本来自 2012 年底关闭窗口，不覆盖 2013+ SMS
- 编码由单一研究者（第二作者）主导，虽有第一作者复核，但非独立双人编码

---

## 3. 原生样本编码维度树 / 维度森林

> 以下树型结构复原自：Table 3 数据抽取表（§3.4）、§4 结果分类统计（§4.1--4.6）、Appendix B 映射表（Table B.15--B.27）、Table 5 guideline 对比表（§5）、Table 14 质量评价 rubric（§5.3）。

```
[Root] 单篇 SMS primary study（n=57）
│
├── [Branch-A] 文献元数据 (publication metadata)
│   ├── [Leaf-A1] Study ID                              — 整数编号
│   ├── [Leaf-A2] Article Title                          — 自由文本
│   ├── [Leaf-A3] Author Names                           — 自由文本（多值）
│   ├── [Leaf-A4] Year of Publication                    — 数值区间 [2004, 2012]
│   ├── [Leaf-A5] Area in SE (SWEBOK topic)              — 层级枚举：11 类（Software design / testing / ... / Education / Research methods）
│   └── [Leaf-A6] Venue                                  — 层级枚举：Journal / Conference / Workshop；再按芬兰分类细分为子类
│
├── [Branch-B] 遵循的指南 (guidelines followed)
│   └── [Leaf-B1] Guidelines adopted                     — 多值枚举：Kitchenham & Charters 2007 / Petersen et al. 2008 / Budgen et al. 2008 / Arksey & O'Malley 2005 / Petticrew & Roberts 2006 / Biolchini et al. 2005 / Dyb & Dingsyr 2008 / Bailey et al. 2007 / Jorgensen & Shepperd 2007 / Durham template
│
├── [Branch-C] 研究识别 (study identification)
│   ├── [Sub-C1] 选择检索策略 (choosing search strategy)
│   │   └── [Leaf-C1.1] Search strategy type              — 多值枚举：Database search / Snowballing / Manual search
│   ├── [Sub-C2] 构造检索式 (developing the search)
│   │   ├── [Leaf-C2.1] PICO(C)                          — 布尔
│   │   ├── [Leaf-C2.2] Consult librarians/experts        — 布尔
│   │   ├── [Leaf-C2.3] Iteratively improve search        — 布尔
│   │   ├── [Leaf-C2.4] Keywords from known papers        — 布尔
│   │   └── [Leaf-C2.5] Use standards/encyclopedias       — 布尔
│   ├── [Sub-C3] 评估检索 (evaluating the search)
│   │   ├── [Leaf-C3.1] Test-set of known papers          — 布尔
│   │   ├── [Leaf-C3.2] Expert evaluates result           — 布尔
│   │   ├── [Leaf-C3.3] Search authors' web pages         — 布尔
│   │   └── [Leaf-C3.4] Test-retest                       — 布尔
│   └── [Sub-C4] 纳入/排除 (inclusion and exclusion)
│       ├── [Leaf-C4.1] Identify objective criteria        — 布尔（Table B.21 计数）
│       ├── [Leaf-C4.2] Multiple reviewers + resolve       — 布尔
│       └── [Leaf-C4.3] Decision rules                     — 布尔
│
├── [Branch-D] 质量评价 (quality assessment)
│   └── [Leaf-D1] QA conducted                            — 布尔 (Yes/No)
│
├── [Branch-E] 数据抽取与分类 (data extraction and classification)
│   ├── [Sub-E1] 数据抽取过程 (extraction process)
│   │   ├── [Leaf-E1.1] Identify objective criteria        — 布尔
│   │   ├── [Leaf-E1.2] Multiple reviewers + resolve       — 布尔
│   │   └── [Leaf-E1.3] Test-retest                        — 布尔
│   ├── [Sub-E2] Topic-independent classification facets used
│   │   ├── [Leaf-E2.1] Research method                    — 布尔（使用 Wohlin et al. / Easterbrook 分类法：Survey / Case study / Controlled experiment / Action research / Ethnography / Simulation / Prototyping / Mathematical analysis）
│   │   ├── [Leaf-E2.2] Research type                      — 布尔（使用 Wieringa et al. 2006 六类：Validation / Evaluation / Solution proposal / Philosophical / Opinion / Experience）
│   │   ├── [Leaf-E2.3] Study focus                        — 布尔
│   │   ├── [Leaf-E2.4] Contribution type                  — 布尔
│   │   └── [Leaf-E2.5] Venue                              — 布尔
│   └── [Sub-E3] Topic-specific classification approach
│       ├── [Leaf-E3.1] Emerging scheme (keywording)       — 布尔
│       └── [Leaf-E3.2] Use of standards/classifications    — 布尔
│
├── [Branch-F] 可视化 (visualization)
│   └── [Leaf-F1] Visualization types used                 — 多值枚举：Bubble plot / Bar plot / Pie diagram / Venn diagram / Heatmap / Line diagram
│
└── [Branch-G] 效度评估 (validity evaluation)
    └── [Leaf-G1] Validity threats discussed               — 布尔 (Yes/No)
```

### 3.1 与更新后 guideline 输出 schema 的关系

原文还产出了一个 **输出型 guideline schema**（§5 / Table 5），它是对上述编码维度的**重组和补全**，不完全等同于编码树：

```
planning
├── need identification and scoping
├── study identification
│   ├── choosing search strategy
│   ├── developing the search
│   ├── evaluating the search
│   └── inclusion and exclusion
├── data extraction and classification
│   ├── topic-independent facets (venue, research type, research method → 推荐)
│   └── topic-specific (emerging / standards-based)
├── visualization
└── validity threats
conducting (执行 planning 定义的过程)
reporting (标准化结构)
```

这个输出 schema 的叶子值与编码树大部分重复，但增加了 **need identification** 和 **reporting** 两个 planning 树中未编码的维度（因为 57 篇 primary study 的 need/reporting 没有被系统编码），以及 **decision rules table (Table 6)** 和 **venue classification (Fig. 18 / Finnish system)** 等操作性工具。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [Leaf-A5] | SE 主题领域 | Branch-A 文献元数据 | Table 3 "Area in SE" + §4.2 / Fig. 3 / Table B.15 | 按 SWEBOK 知识域对本篇 SMS 的主题归属进行分类 | {Software design, Software testing, Software quality, Software requirements, Software construction, Software tools and methods, Software engineering process, Software engineering management, Software configuration management, Education, Research methods} | 层级枚举（加 Education / Research methods 非 SWEBOK 补充类） | 每篇 SMS 必定归入至少一个主题 | 计数每个主题覆盖的 SMS 数量（Fig. 3） | 识别 SE 各子领域 SMS 的密集/稀疏状态（testing 最高，configuration management 最低） | EV-003 / Table B.15 | 仅限 2012 年末前窗口；主题间不可比（每篇可跨多主题） |
| [Leaf-A6] | 发表渠道 | Branch-A 文献元数据 | Table 3 "Venue" + §4.3 / Fig. 4 / Table 4 | 本篇 SMS 发表在 journal、conference 还是 workshop | {Journal, Conference, Workshop} + 芬兰分类子级（Fig. 18） | 层级枚举 | 每篇 SMS 有且仅有一个主要发表渠道 | 计数 venue 分布（Fig. 4）；与 year 交叉得趋势 | 期刊/会议二分各半，2011--2012 显著增长 | EV-004 / Table 4 / Fig. 18 | venue 分类法（芬兰体系）仅在 SE 语境下有较好复用性 |
| [Leaf-B1] | 遵循的指南 | Branch-B | Table 3 "Guidelines" + §4.4.1 / Fig. 5 / Table B.17 | 本篇 SMS 使用了哪些 guideline | ~10 种 guideline 的多值组合 | 完整枚举（来自 known guideline corpus） | 空值罕见（每篇必须声明 guideline）；组合常见 | 计数各 guideline 使用频率（Fig. 5） | Kitchenham 系列最常用；多 guideline 组合是常态（单一 guideline 不足） | EV-005 / Table B.17 | guideline corpus 随时间更新需扩展 |
| [Leaf-C1.1] | 检索策略类型 | Sub-C1 选择检索策略 | §4.4.2 / Fig. 6 / Table B.18 | 本研究使用了哪种检索策略 | {Database search, Snowballing, Manual search} | 多值枚举 | 至少一种；常为三种组合 | 计数各策略使用频率（Fig. 6） | DB search 几乎全用；snowballing 和 manual 约 1/4 | EV-006 / Table B.18 | 策略间非互斥 |
| [Leaf-C2.1] | 是否使用 PICO(C) | Sub-C2 构造检索 | §4.4.2 / Fig. 7 / Table B.19 | 检索式构造是否使用 PICO(C) 框架 | {Yes, No} | 布尔 | No 为常见默认 | 计数（Fig. 7） | PICO 约 11/57 使用 | EV-006 / Table B.19 | PICO 在 SE 中的适用性本身有争议 |
| [Leaf-C2.2] | 是否咨询专家/馆员 | Sub-C2 | Table B.19 | 检索式构造是否咨询 librarian 或领域专家 | {Yes, No} | 布尔 | No 为多数 | 计数 | 少数（6/57） | EV-006 | — |
| [Leaf-C2.3] | 是否迭代改进检索 | Sub-C2 | Table B.19 | 检索式是否经过多轮迭代改进 | {Yes, No} | 布尔 | No 常见 | 计数 | — | EV-006 | — |
| [Leaf-C2.4] | 是否从已知论文取关键词 | Sub-C2 | Table B.19 | 是否从已知相关论文中提取关键词构造检索式 | {Yes, No} | 布尔 | No 常见 | 计数 | 约 10/57 | EV-006 | — |
| [Leaf-C2.5] | 是否使用标准/百科全书 | Sub-C2 | Table B.19 | 是否使用 standards, encyclopedias, thesaurus 辅助构造检索 | {Yes, No} | 布尔 | No 常见 | 计数 | — | EV-006 | — |
| [Leaf-C3.1] | test-set 评估 | Sub-C3 评估检索 | §4.4.2 / Fig. 8 / Table B.20 | 是否用已知论文集测试检索召回 | {Yes, No} | 布尔 | No 常见 | 计数（Fig. 8） | 约 8/57 | EV-006 / Table B.20 | — |
| [Leaf-C3.2] | 专家评估 | Sub-C3 | Table B.20 | 是否请专家评审检索结果 | {Yes, No} | 布尔 | No 为绝大多数 | 计数 | 仅 1 篇 | EV-006 | — |
| [Leaf-C3.3] | 作者主页检索 | Sub-C3 | Table B.20 | 是否搜索关键作者主页 | {Yes, No} | 布尔 | No 为绝大多数 | 计数 | 仅 1 篇 | EV-006 | — |
| [Leaf-C3.4] | test-retest | Sub-C3 | Table B.20 | 是否做 test-retest 评估 | {Yes, No} | 布尔 | No 为绝大多数 | 计数 | 仅 1 篇 | EV-006 | — |
| [Leaf-C4.1] | 有客观纳排标准 | Sub-C4 纳入/排除 | §4.4.2 / Fig. 9 / Table B.21 | 是否定义了客观的 inclusion/exclusion criteria | {Yes, No} | 布尔 | No 常见 | 计数（Fig. 9） | 约 8/57 | EV-006 / Table B.21 | — |
| [Leaf-C4.2] | 多审+分歧解决 | Sub-C4 | Table B.21 | 是否使用多位 reviewer 并解决分歧 | {Yes, No} | 布尔 | No 常见 | 计数 | 约 22/57（最高频单一策略） | EV-006 / Table B.21 | — |
| [Leaf-C4.3] | 决策规则 | Sub-C4 | Table B.21 | 是否使用 formal decision rules（如 Table 6 的 3×3 矩阵） | {Yes, No} | 布尔 | No 为多数 | 计数 | 约 4/57 | EV-006 / Table B.21 | Table 6 是本文提出的工具，非 primary study 原生 |
| [Leaf-D1] | 质量评价 | Branch-D | §4.4.3 / Fig. 10 / Table B.22 | 是否对纳入论文做了 quality assessment | {Yes, No} | 布尔 | No 为多数（43/57） | 计数（Fig. 10） | 仅 14/57 做 QA | EV-007 / Table B.22 | — |
| [Leaf-E1.1] | 抽取-客观标准 | Sub-E1 数据抽取 | §4.4.4 / Fig. 11 / Table B.23 | 抽取过程是否有客观标准 | {Yes, No} | 布尔 | No 常见 | 计数 | 约 4/57 | EV-008 / Table B.23 | — |
| [Leaf-E1.2] | 抽取-多审 | Sub-E1 | Table B.23 | 抽取过程是否多 reviewer + 分歧解决 | {Yes, No} | 布尔 | No 常见 | 计数 | 约 17/57（最高频） | EV-008 / Table B.23 | — |
| [Leaf-E1.3] | 抽取-test-retest | Sub-E1 | Table B.23 | 抽取过程是否 test-retest | {Yes, No} | 布尔 | No 为绝大多数 | 计数 | 仅 1/57 | EV-008 | — |
| [Leaf-E2.1] | 使用 Research method facet | Sub-E2 topic-independent facets | §4.4.4 / Fig. 12 / Table B.24 | 该 SMS 的分类方案是否包含 research method 维度 | {Yes, No} | 布尔 | No 常见 | 计数（Fig. 12） | 约 17/57 | EV-008 / Table B.24 | 外部分类法引用（Wohlin/Easterbrook） |
| [Leaf-E2.2] | 使用 Research type facet | Sub-E2 | Table B.24 | 是否含 research type 维度（Wieringa et al. 分类） | {Yes, No} | 布尔 | No 常见 | 计数 | 约 21/57（最高频 topic-independent facet） | EV-008 / Table B.24 | 外部分类法引用；原文 §5.1.3 提供了 Table 7 消除歧义的决策表 |
| [Leaf-E2.3] | 使用 Study focus facet | Sub-E2 | Table B.24 | 是否含 study focus 维度 | {Yes, No} | 布尔 | No 常见 | 计数 | — | EV-008 | 定义尚不统一 |
| [Leaf-E2.4] | 使用 Contribution type facet | Sub-E2 | Table B.24 | 是否含 contribution type 维度 | {Yes, No} | 布尔 | No 常见 | 计数 | 仅约 5/57（使用率最低） | EV-008 / Table B.24 | 原文指出此 facet 不推荐为通用维度 |
| [Leaf-E2.5] | 使用 Venue facet | Sub-E2 | Table B.24 | 是否对纳入文献做 venue 分类 | {Yes, No} | 布尔 | No 常见 | 计数 | 约 27/57（最高频） | EV-008 | — |
| [Leaf-E3.1] | 话题分类-涌现式 | Sub-E3 topic-specific | §4.4.4 / Fig. 13 / Table B.25 | 话题分类是否从文献中自底向上涌现 | {Yes, No} | 布尔 | No 常见 | 计数（Fig. 13） | 大多数（Fig. 13 shows emerging as majority） | EV-008 | keywording 方法与 open coding/Grounded Theory 的关系在原文 §5.1.3 中有讨论 |
| [Leaf-E3.2] | 话题分类-基于标准 | Sub-E3 | Table B.25 | 话题分类是否基于已有标准/分类法（如 SWEBOK、IEEE、ISO/IEC） | {Yes, No} | 布尔 | No 常见 | 计数 | 少数 | EV-008 | — |
| [Leaf-F1] | 可视化类型 | Branch-F | §4.4.5 / Fig. 14 / Table B.26 | 使用了哪些可视化方式呈现结果 | {Bubble plot, Bar plot, Pie diagram, Venn diagram, Heatmap, Line diagram} | 多值枚举 | 至少一种；常为多种组合 | 计数（Fig. 14） | Bar plot 和 Pie diagram 最常用；Bubble plot 和 Heatmap 适合交叉分类 | EV-009 | — |
| [Leaf-G1] | 效度讨论 | Branch-G | §4.4.6 / Fig. 15 | 是否讨论了研究效度威胁 | {Yes, No} | 布尔 | No 为少数（12/57） | 计数（Fig. 15） | 45/57 讨论 validity（高比例） | EV-010 | — |

---

## 5. 关系边表

### 5.1 显式关系边（原文统计交叉）

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| [Rel-01] | [Leaf-A4] Year | 时间趋势 | [Leaf-A5] Topic | 按年统计各主题 SMS 数 | 无缺失（全样本） | §4.2 / Fig. 3 隐含时间维度（图未做交叉，但文本指出 testing 持续增长） | 识别主题热度变化 |
| [Rel-02] | [Leaf-A6] Venue | 分组对比 | [Leaf-D1] QA | Journal vs. Conference 下 QA 比率 | 无缺失 | §5.3 / Fig. 21 | 期刊 QA 率高于会议（Fig. 21） |
| [Rel-03] | [Leaf-A6] Venue | 分组对比 | [Leaf-B1] Guidelines | 不同 venue 类型使用的 guideline 组合 | 待核验 | §4.4.1 文字未做此交叉 | 为 A2a 精核入口 |
| [Rel-04] | [Leaf-C4.2] Multiple reviewers | 互补关系 | [Leaf-E1.2] Multiple reviewers + resolve | 同一布尔×2 | 可均为 No | Table B.21 / Table B.23 分别计数 | 研究识别和抽取阶段的多审模式可比较 |
| [Rel-05] | [Sub-E2] Topic-independent facets | 互斥/组合 | [Sub-E3] Topic-specific approach | topic-independent 和 topic-specific 是否在同一 SMS 中同时使用 | 常见并存 | §4.4.4 文字 | 多数 SMS 同时使用两类分类 |

### 5.2 原文未显式编码但可从 Table B 映射表反推的关系

| 关系边标识 | 说明 | 证据 |
|---|---|---|
| [Rel-06] | 每篇 primary study 与其使用的 all guidelines 的多对多映射 | Table B.17 完全展开 |
| [Rel-07] | 每篇 primary study 与其覆盖 topic 的多对多映射 | Table B.15 |
| [Rel-08] | 每篇 primary study 与其使用的 all search strategies / development methods / evaluation methods 的多对多映射 | Table B.18--B.21 |
| [Rel-09] | 每篇 primary study 与其使用的 all topic-independent facets 的多对多映射 | Table B.24 |

### 5.3 不适用说明

原文没有编码 primary study 与其**结果发现/效果量/因果推断**之间的关系边。这是因为 mapping study 的目标是结构化领域而非合成证据，所以这种关系边不出现在本文的 encoding schema 中是**设计上合理的**。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段/统计表支持的统计观察（statistical observations）

这些是直接从编码维度计数的结果，证据来自 §4 各 Fig 和 Appendix B 映射表：

| 统计观察 | 证据来源 | 可靠度 |
|---|---|---|
| 多 guideline 组合使用是常态；单一 guideline 不足 | Fig. 5 / Table B.17 | high |
| DB search 几乎全覆盖；snowballing 和 manual search 各约 1/4 | Fig. 6 / Table B.18 | high |
| PICO 使用率不高（~11/57）；Keywords from known papers 为最高频 search development 策略 | Fig. 7 / Table B.19 | high |
| Test-set 是最高频 search evaluation 策略（~8/57） | Fig. 8 / Table B.20 | high |
| Multiple reviewers 是最高频 inclusion/exclusion 策略（~22/57） | Fig. 9 / Table B.21 | high |
| 仅 14/57 做 QA | Fig. 10 / Table B.22 | high |
| 数据抽取中 Multiple reviewers 最高频（~17/57） | Fig. 11 / Table B.23 | high |
| Venue 和 Research type 是最高频 topic-independent facets | Fig. 12 / Table B.24 | high |
| Contribution type 使用率最低，原文建议不推荐为通用 facet | Fig. 12 + §5.1.3 discussion | medium（单点统计，需更多证据） |
| 多话题分类采用 emerging scheme（keywording） | Fig. 13 | high |
| Bar plot 和 Pie diagram 最常用可视化 | Fig. 14 | high |
| 45/57 讨论 validity threats | Fig. 15 | high |
| 2011--2012 年 SMS 数量显著增长 | Fig. 2 | high |
| Software testing 是 SMS 最多的主题 | Fig. 3 / Table B.15 | high |
| Journal 和 Conference/Workshop 各占约一半 | Fig. 4 / Table 4 | high |

### 6.2 原文 discussion / recommendation / roadmap 提出的候选 finding（candidate findings）

| 候选 finding | 来源 | 类型 | 对 Paper2 的迁移价值 |
|---|---|---|---|
| "a good sample and representation of studies is more important than having a higher number of studies" | §6 Conclusion | methodological guideline | 直接指导 A2a 纳排策略：质>量 |
| "quality assessment should not pose high requirements on the primary studies as the goal of mapping is to give a broad overview" | §5.1.2 (near QA) | methodological guideline | 指导 A2a QA rubric 设计 |
| "topic-independent classifications should be used by the majority of mapping studies...to enable comparisons" | §5.1.3 | methodological guideline | 指导 A2a 编码方案的通用维度选择 |
| Venue/Research type/Research method 是推荐的通用 facet 三件套；Contribution type 不推荐 | §5.1.3 | methodological guideline | 直接用于 A2a extraction form 设计 |
| keywording（open coding 式）是 topic-specific classification 的主要建类方法 | §5.1.3 | methodological pattern | 直接指导 A2a 对 SLR/SMS 文献的话题分类流程 |
| guideline comparison matrix (Table 5) 可作为选择 guideline 组合的决策工具 | §5.1 | methodological tool | 指导 Paper2 方法学部分的 guideline 选取理由 |

### 6.3 对 Paper2 可迁移的方法学启发

1. **extraction form 设计**：Table 3 的 9 字段结构可直接作为 A2a 对 SLR/SMS 综述文献的最小 extraction form 种子。
2. **topic-independent + topic-specific 双轨分类**：A2a 也应区分"跨主题通用维度"和"领域专属分类"，前者保证可比性，后者捕获领域特性。
3. **quality evaluation rubric**：Table 14 的五活动四等级评价框架可适配为 A2a 对纳入综述文献的方法学质量评价表。
4. **guideline comparison matrix**：Table 5 的 guideline × activity 对比矩阵模式可迁移为 Paper2 方法学 self-assessment 工具。
5. **validity taxonomy**：§3.6 使用的 descriptive/theoretical/generalizability/interpretive validity 四分类可直接引入 Paper2 的效度威胁讨论。

### 6.4 绝不能迁移的领域结论

- 本文所有关于 "software testing SMS 最多""software configuration management SMS 最少" 等主题分布统计，**完全不可迁移**到任何非 SMS-method 的目标领域。
- SWEBOK 主题分类本身不应迁移为非 SE 领域的分类方案。
- 所有基于 2004--2012 时间窗口的逐年趋势不可迁移到当前时间窗口。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 分级

| 级别 | 内容 | 理由 |
|---|---|---|
| **C** | A.1 维度树仍过度抽象，将原文的 Branch-A--G 七支 + 30+ 叶子折叠为 planning/conducting/reporting 三阶段 + 六个通用 leaf（scope/literature-corpus/classification/method/evidence/finding） | 这六个 leaf 是跨论文的通用投影接口（来自 A1-M0--M6），不是本文的原生编码 schema。当前 A.1 虽然加了 orig-planning/orig-conducting/orig-reporting/orig-quality-rubric/orig-topic-independent-dimension 作为中间节点，但叶子仍然是六个通用标签，丢失了原文 30+ 个编码字段的细节 |
| **C** | A.2 证据账本草案未映射到原文的具体 leaf 维度 | 当前 A.2 的证据锚点只链接到 §3/§4/§5 整节和 Table B，缺少对 [Leaf-C1.1]--[Leaf-G1] 等具体叶子的逐个证据锚定 |
| **C** | SUMMARY 表中"样本单位"字段需更新 | 现有 review.md 未在 A.1 维度树中明确样本单位是 "primary SMS study"；当前维度树根节点描述为"方法学与维度模式"，未区分样本单位根和编码 schema 根 |
| **I** | A.3 结论-证据映射草案方向正确，但结论粒度与原生 leaf 不匹配 | A.3 的结论（C01--C13）中 C05--C07 三个 "叶子维度...可作为 Paper2 维度树候选节点" 实际上是跨论文投影而非本文原生 leaf 映射 |
| **I** | 缺少对关系边（§5 of 本审计）的显式建模 | 原文有丰富的多对多映射关系（Table B.15--B.27），当前 review.md 的关系边表为空或缺失 |
| **M** | A.4 人工核验清单已到位，但需补充 PDF 图表视觉核验的具体页码/表号清单 | 当前只有 needs_manual_check 标记，未列出 Fig. 1--21 + Table 3/5/6/7/14 + Appendix B.15--B.27 的具体核验条目 |

### 7.2 具体返修动作

1. **重写 A.1 维度树**：将 current 的 planning/conducting/reporting 三阶段 + 六通用 leaf 替换为本报告 §3 的七支 (Branch-A--G) + 30+ leaf 结构。保留 orig-planning/orig-conducting/orig-reporting 作为输出 guideline schema 的并行展示（标注为"输出型 schema"，非样本编码 schema）。
2. **补充 A.1 样本单位根节点**：明确根节点为"单篇 SMS primary study (n=57)"，与编码维度树根区分。
3. **重写叶子维度表**：用本报告 §4 的完整叶子维度表替换当前或新增为 A.1 子表。
4. **新增关系边表**：基于本报告 §5，补充关系边表（至少包含 [Rel-01]--[Rel-05]）。
5. **更新 A.2 证据账本**：将每个 [Leaf-XX] 映射到具体的 Table/Fig/Appendix 页码（待 PDF 核验后补页码）。
6. **更新 SUMMARY 口径**：样本单位统一为"single SMS primary study"，样本数量 57，原生树类型从"降级树"改为"维度森林"。
7. **C06/C07 结论重定向**：将 A.3 中 C05--C07 的"叶子维度...可作为 Paper2 候选节点"改为直接引用具体 [Leaf-XX] 标识，并标注为 schema_seed。
8. **补充 A.4 PDF 核验条目清单**：列出所有待核验图表编号。

---

## 8. 审计附录草案：证据账本与结论映射

### 8.1 A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §3.4 | Table 3 Data extraction form | "To extract data from the identified primary studies, we developed the following template shown in Table 3." | 直接定义 sample encoding schema | high | [Branch-A]--[Branch-F] 全部 | 是（Table 3 列对齐、完整的 Data item / Value / RQ 三栏确认） | 仅限 SMS 元研究方法学 |
| EV-002 | paper_content.txt | §4.1 | Fig. 2 / RQ1 | "Fig. 2 shows the number of mapping studies identified within the time frame." | 时间分布统计 | high | [Leaf-A4] | 是（Fig. 2 精确 y 轴值） | 时间窗口不可外推 |
| EV-003 | paper_content.txt | §4.2 | Fig. 3 / Table B.15 | "Fig. 3 shows the number of mapping articles per topic category. ... SWEBOK structure." | 主题分布统计 | high | [Leaf-A5] | 是（Fig. 3 柱值 + Table B.15 逐篇映射） | 主题分类不可迁移至非 SE 领域 |
| EV-004 | paper_content.txt | §4.3 | Fig. 4 / Table 4 | "Fig. 4 provides an overview of the distribution of mapping articles ... Table 4." | venue 分布统计 | high | [Leaf-A6] | 是（Table 4 逐 venue 统计） | — |
| EV-005 | paper_content.txt | §4.4.1 | Fig. 5 / Table B.17 | "The guidelines used are...Kitchenham...followed by most mapping studies." | guideline 使用频率 | high | [Leaf-B1] | 是（Fig. 5 柱值 + Table B.17 逐篇映射） | guideline corpus 随时间扩展 |
| EV-006 | paper_content.txt | §4.4.2 | Fig. 6--9 / Table B.18--B.21 | "Three search strategies have been identified... The strategies for developing the search are shown in Fig. 7... The most common strategy for evaluating the search... strategies have been identified..." | study identification 四层子树计数 | high | [Leaf-C1.1]--[Leaf-C4.3] | 是（Fig. 6--9 柱值 + Table B.18--B.21 逐篇映射） | — |
| EV-007 | paper_content.txt | §4.4.3 | Fig. 10 / Table B.22 | "quality assessment is conducted in..." | QA 计数 | high | [Leaf-D1] | 是（Table B.22 逐篇标记） | — |
| EV-008 | paper_content.txt | §4.4.4 | Fig. 11--13 / Table B.23--B.25 | "the most frequently applied facets for classification are venue, research type, and research method..." | 分类维度计数 | high | [Leaf-E1.1]--[Leaf-E3.2] | 是（Fig. 11--13 柱值 + Table B.23--B.25 逐篇映射） | — |
| EV-009 | paper_content.txt | §4.4.5 | Fig. 14 / Table B.26 | "The most common approaches are bar plots and pie diagrams." | 可视化类型计数 | high | [Leaf-F1] | 是（Fig. 14 柱值 + Table B.26） | — |
| EV-010 | paper_content.txt | §4.4.6 | Fig. 15 | "45 of the mapping studies...reported validity threats." | 效度讨论计数 | high | [Leaf-G1] | 是（Fig. 15） | — |
| EV-011 | paper_content.txt | §5.1--5.3 | Table 5 Guideline comparison | "The main activities of the systematic mapping process as identified in Section 4 are mapped to the guidelines in Table 5." | 输出 schema 定义 | high | guideline update 的三阶段框架 | 是（Table 5 的完整 p/— 矩阵） | Table 5 是综合产物，非单篇 primary study 映射 |
| EV-012 | paper_content.txt | §5.3 | Table 14 Rubric evaluation | "We provided an evaluation rubric and exemplified it by application to this systematic map." | quality rubric 定义 | high | quality evaluation schema | 是（Table 14 五活动 × 四等级值） | rubric 按本文 self-application 校准 |
| EV-013 | paper_content.txt | §6 | Conclusion | "a good sample...is more important than having a higher number...trade-off between effort and reliability." | 候选 finding | medium（单篇 discussion） | 纳排策略、effort-reliability trade-off | 否（text-level） | 需跨论文验证 |
| EV-014 | paper_content.txt | §5.1.3 | Table 7 Decision table for research types | "Table 7 presents a decision table to disambiguate the classification of studies." | 分类歧义消除工具 | medium | [Leaf-E2.2] 的取值空间 | 是（Table 7 的 4 条件 × 6 类型） | 工具本身是 guideline output，非 primary study 编码 |

### 8.2 A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| [CLM-01] | 本文样本单位为单篇 SMS primary study（n=57）；样本来自 2004--2012 窗口的四库系统检索 + backward snowballing | scope_definition | [Root] | EV-001, EV-002 | high | 定义统计池边界 | 2013+ SMS 未覆盖 |
| [CLM-02] | Table 3 的 9 字段 extraction form 是本文的 sample encoding schema，可直接迁移为 A2a 对 SLR/SMS 文献的最小 extraction form 种子 | schema_seed | [Branch-A]--[Branch-F] | EV-001 | high | A2a extraction form 设计 | 9 字段需按 A2a 目标扩展 |
| [CLM-03] | 原文对每个 primary study 在 30+ 个叶子维度上做了编码，覆盖文献元数据、guideline、study identification（四子树）、QA、extraction/classification（三子树）、visualization、validity | schema_definition | [Leaf-A5]--[Leaf-G1] | EV-003--EV-010 | high | A2a 编码方案建模 | 部分叶子（如 Leaf-E2.3 study focus）原文定义模糊 |
| [CLM-04] | guideline 多组合使用是常态；Kitchenham (2007) 与 Petersen et al. (2008) 是最常用组合 | statistical_observation | [Leaf-B1] | EV-005 | high | 指导 A2a 的 guideline 选取理由 | — |
| [CLM-05] | Venue + Research type + Research method 是推荐的三件套 topic-independent facets；Contribution type 不推荐 | methodological_guideline | [Leaf-E2.1]--[Leaf-E2.5] | EV-008 | medium（单点统计 + 作者推荐） | 指导 A2a 通用维度选择 | 需要在更多 SMS 样本上验证 |
| [CLM-06] | keywording / open coding 式方法是 topic-specific classification 的主流建类方式 | methodological_pattern | [Leaf-E3.1] | EV-008 | high | 指导 A2a 话题分类流程 | keywording 过程在原文 §5.1.3 中有更详细的操作化说明 |
| [CLM-07] | Quality evaluation rubric（Table 14 五活动 × 四等级）可直接适配为 A2a 方法学质量评价表 | methodological_tool | [quality rubric schema] | EV-012 | medium（rubric 为本研究提出，非外部验证） | A2a quality rubric 模板 | rubric 等级描述（Min.E./Part.E./Full E.）需 A2a 重定义 |
| [CLM-08] | Table 5 的 guideline comparison matrix 展示了不同 guideline 的 activity 覆盖差异 | methodological_tool | [output guideline schema] | EV-011 | high | 用在 Paper2 方法学 self-assessment | matrix 不完整（部分 cell 为空） |
| [CLM-09] | "good sample > high number" 和 "trade-off between effort and reliability" 是本文的核心方法学洞察，可用于指导 A2a 的纳排与质量策略 | candidate_finding | [统计池策略] | EV-013 | medium（需跨论文验证） | 指导 A2a 纳排策略 | 单篇 discussion，非多文交叉验证 |
| [CLM-10] | 本文所有主题分布统计（testing 最多、configuration management 最少等）不可迁移 | migration_boundary | [Leaf-A5] | EV-003 | high | 仅限审计边界声明 | — |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件与采用的原则

| 技能/指南文件 | 读取状态 | 采用的原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 已读 | evidence gate（证据优先于记忆）、citation gate（不编造引用）、claim gate（不强于证据的声称） |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 已读 | originality/quality/clarity/significance/reproducibility/ethics 六维 review 框架；避免"main contribution unclear"或"reads like implementation report" |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 已读 | claim audit（每个 Abstract/Introduction 声称需有直接证据）、rejection-risk audit、adversarial questions |
| `research-planning/SKILL.md` | 已读 | 四阶段计划（Overall Plan → Architecture → Logic → Configuration）与 paper-structure-schema 模板 |
| `research-planning/references/planning-prompts.md` | 已读 | Paper2Code 四轮规划方法；Plan Agent 的 dataset/model/training/testing 四层 plan schema |
| `research-planning/references/output-schemas.md` | 已读 | JSON schema 模板（paper_structure / task_list / experiment_design / risks） |
| `autoresearch/SKILL.md`（oh-my-codex） | 已读 | completion artifact-gated loop；mission-validator-script vs. prompt-architect-artifact 两种验证模式 |

### 9.2 本输出最高风险 3 点（reviewer 视角）

| 风险 | 说明 | 主线程合并时的复核建议 |
|---|---|---|
| **Risk-1：PDF 图表未做视觉版面核验** | 本审计基于 `paper_content.txt` 文本提取结果。Table 3/5/6/7/14 和 Fig. 1--21 的精确列值、柱高、映射关系，以及 Appendix B 表 B.15--B.27 的逐篇标记，均依赖 text-mode PDF 提取的保真度。若 text 提取有误（例如表格列对齐丢失），则 30+ leaf 的取值空间枚举可能不完整或偏误 | 逐项打开 PDF 核对每个 Fig 和 Table 的原始版面；优先核对 Table 3（extraction form）、Table 5（guideline comparison）、Table B.15--B.27（per-study mappings） |
| **Risk-2：30+ leaf 取值空间的"饱和性"未验证** | 本文编码了 57 篇 SMS 在 2004--2012 窗口内的所有已知 mapping process 变异。但 2013 年至今的 SMS 实践可能引入了新检索策略、新可视化或新分类 facet。本报告所有枚举声明为"完整枚举"的 leaf 仅限该 window 内 | A2a 扩库时按需扩展取值空间；对每个枚举 leaf 标注窗口范围 |
| **Risk-3：review.md 的六通用 leaf 残留** | 现有 review.md 虽然在 A.1 加入了 orig-planning/orig-conducting 等中间节点，但叶子仍是六个通用接口标签。本审计报告用 Branch-A--G + 30+ leaf 替换后，需确保 review.md 的 A.2/A.3/A.4 与新的 leaf 命名体系完全对齐，不留旧 ref | 先更新 A.1 维度树为 Branch-A--G 七支，再将 A.2 证据锚点和 A.3 结论-证据映射的支撑对象全部替换为 [Leaf-XX] 标识 |

### 9.3 blocked / timeout / 文件缺失

| 项目 | 状态 |
|---|---|
| `paper_content.txt` 读取 | 完整，1973 行全通读 |
| `bibtex.bib` | 完整 |
| `metadata.json` | 完整 |
| `review.md` | 完整 |
| 所有 7 个技能/指南文件 | 全部成功读取 |
| `paper.pdf` 视觉核验 | **未做**（文本级审计完成，但 PDF 版面核验标记为 needs_manual_check） |
| 本任务是否 blocked | **否**：所有文件均可读，审计可完成；PDF 视觉核验作为独立 follow-up 清单移交给主线程 |

---

*审计完成时间：2026-06-30 | agent: deepseek | 基于 paper_content.txt 全文文本级阅读 | 总 leaf 复原：7 支 30+ leaf，全部标定证据锚点*