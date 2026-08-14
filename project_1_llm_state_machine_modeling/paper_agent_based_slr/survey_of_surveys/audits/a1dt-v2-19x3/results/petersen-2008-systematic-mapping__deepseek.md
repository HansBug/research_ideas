## 阶段 2：论文全文审计（A1-DT v2）

---

# A1-DT v2 单篇全文审计报告

**论文**：Petersen et al. 2008, *Systematic Mapping Studies in Software Engineering*
**slug**: `petersen-2008-systematic-mapping`
**审计 agent**: `deepseek`

---

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `petersen-2008-systematic-mapping` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。536 行全文通读，覆盖所有 10 页 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。bibtex.bib 含 DOI、作者、年份；metadata.json 含完整元数据、CCF 评级、阅读状态 |
| 是否打开或核对 `paper.pdf` | 否。未直接打开 PDF 做版面/图表视觉核验。本次审计基于 `paper_content.txt` 全文文本提取结果。`metadata.json` 记录 text 模式正常（无乱码），但 table/figure 编号与内容仍需 A2a 人工核验 |
| 原文类型 | SMS 方法论文（含 guideline 建议）；有对照分析（12 SR），但无系统样本库 |
| 被编码样本单位 | 两层：(1) 方法层：SMS 自身流程 / Facet 体系，无被编码的 primary study 样本；(2) 对照层：12 篇已发表 SE 系统综述作为 **SR-vs-SMS 对照对象**（非 mapping 目标） |
| 样本数量 / 分母 | 方法层：N/A（无系统样本库）；对照层：12 篇 SR |
| 原生树类型 | **降级树**（guideline/methodological seed + 含对照型叶子集合） |
| 主统计池资格 | **否**（局部可统计）。对照型叶子（12 SR 维度对比）可进入 A2a 作为 method comparison seed，但不进入 SLR/SMS 领域统计池。metadata.json 已正确设为 `"eligible_for_statistical_synthesis": false` |
| 总体判定 | **needs repair** — 现有 `review.md` 存在"六叶接口伪装成原生树"的历史残留，维度树复原需从 method facet 和 SR comparison table 两个真实来源重建；但本文作为方法学 seed 的角色在 metadata 中已正确，本轮审计重点是修复 review.md 的维度树和证据账本 |

---

### 1. 原文证据阅读说明

#### 1.1 实际读取文件清单

| 文件 | 读取情况 | 内容范围 |
|---|---|---|
| `bibtex.bib` | 完整读取 | 标题、DOI、作者、年份、abstract、publisher、语言 |
| `metadata.json` | 完整读取 | 全部 3 section 元数据，包括阅读状态、evidence_role、exclusion_reason、eligible 判定 |
| `paper_content.txt` | 完整读取 536 行 | 10 页全文，包括 Abstract、§1 Introduction、§2 The Systematic Mapping Process（2.1～2.5）、§3 Comparison of Systematic Reviews and Maps、§4 Guidelines for Systematic Maps 与表 1、表 2 的文本抽取内容、§5 Conclusions、References |
| `paper.pdf` | **未打开** | 未做 PDF 版面/图表编号视觉级核验 |
| `review.md` | 完整读取 | 331 行现有 review，包含快速结论、内容详读、A.1-A.4 附录草案 |

#### 1.2 关键原文证据锚点（10 个）

| # | 锚点 | 原文章节 | 段落或表图线索 | 短引或释义 |
|---|---|---|---|---|
| 1 | Abstract 定义 SMS | Abstract | 第 1 段 | 「A software engineering systematic map is a defined method to build a classification scheme and structure a software engineering field of interest...」|
| 2 | SMS 五步流程 | §2, §2.1–§2.5 | 全节 | 流程：define RQs → search → screen → keywording → data extraction & mapping |
| 3 | Keywording 迭代机制 | §2.4 | 第 2-3 段 | 「The keywording is done in two steps... When reading the abstract the reviewer should also look for keywords and concepts that reflect the contribution of the paper... the set of keywords will evolve...」|
| 4 | 三维 Facet 分类 | §2.4 | 表线索 + 文本描述 | Topic facet（领域子主题）、Contribution facet（process/method/model/tool/metrics ...）、Research type facet（validation/evaluation/solution proposal/philosophical/opinion/experience/personal experience papers，引用 Wieringa 等 2006） |
| 5 | 频数/气泡图呈现 | §2.5 | 文本描述 | 「The main focus is on frequencies of publications for categories within the scheme... bubble plot can be used to combine two or more facets...」|
| 6 | 研究空白发现 | §2.5 | 末段 | 「By using the method, claims as to where there are research gaps can be made」 |
| 7 | 12 篇 SR 对照 | §3 | 表线索 | 作者 systematic analyze 12 existing SRs，对比 SR vs SMS 在「goal」「breadth」「depth」「analysis method」「implications」的差异 |
| 8 | Table 1: SR 对照维度 | §3 | Table 1（名称从 text 推测） | 对比维度包括：research questions、search string、screening criteria、data extraction form、analysis method 等 |
| 9 | Table 2: Map vs Review 差异 | §3 | Table 2（名称从 text 推测） | 对比 SMS vs SR 的 goal、breadth、depth、validity issues、implications |
| 10 | §4 补充 guideline | §4 | 全节 | 基于 SMS 经验给出额外 guideline，强调 visual summary 的重要性、SMS 与 SR 互补使用 |

#### 1.3 仍需 PDF 视觉核验的项

- Table 1（SR 对照表）的确切列名、行数、与 A.2 证据账本的对应关系
- Table 2（Map vs Review 差异表）的确切字段
- 三维 Facet 是否有原文图表或 numbered figure
- bubble plot 是否有原文插图，图编号是什么

---

### 2. 样本单位与字段来源判定

#### 2.1 原文纳入和逐项描述的对象是什么？

两层结构：

1. **方法层（核心）**：本文定义一个 systematic mapping process，描述其五步流程和三维分类 Facet。这些 Facet **不是通过对一批论文的编码结果**，而是作者基于方法学经验和引用 Wieringa 等（2006）的已有分类方案提出的方法论建议。

2. **对照层（辅助）**：作者在 §3 中系统性分析 12 篇已发表 SR，对比 SR 和 SMS 在 goal、breadth、depth、analysis method、implications 等维度的差异。这 12 篇 SR 构成一个小型对照样本集。

#### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

- **对 SMS 方法本身**：作者自述应用过一次 SMS 于 software product line variability（Mujtaba et al. 2008, "submission"）。本文描述的就是那次实践的流程。未给出 systematic inclusion/exclusion 结果数据。
- **对 12 篇 SR**：作者说 systematically analyzed existing systematic reviews，但原文未给出这 12 篇的来源标准、检索策略、纳排流程的详细信息。因此其系统性和可复现性有限。

#### 2.3 原文字段来自哪里？

| 来源 | 位置 | 内容 |
|---|---|---|
| classification scheme（三维 Facet） | §2.4 keywording | Topic facet / Contribution facet / Research type facet — 由作者在 keywording 过程中迭代形成的分类方案，是本文的核心 method 产物 |
| Wieringa et al. 2006 分类法 | §2.4 引用 | Research type 维度引用外部 taxonomy |
| SR 对照维度 | §3 + Table 1 | goal / breadth / depth / analysis method / implications — 是作者为对比 SR vs SMS 而构造的分析维度 |
| SMS vs SR 差异表 | §3 + Table 2 | goal / breadth / depth / validity issues / implications — 是作者的综合结论 |

#### 2.4 RQ 与样本单位是什么关系？

本文没有传统的"研究问题→样本单位→编码"线性结构。其两套 RQ 分别为：

- 方法 RQ：「How to conduct a systematic mapping study in SE?」（§1-2）
- 对比 RQ：「How do systematic maps differ from systematic reviews?」（§1, §3）

第一套 RQ 产出流程和分类方案（方法产物），第二套 RQ 通过对 12 篇 SR 的对照分析产出差异维度（对比产物）。两者都**不是**基于对 primary study 大样本的编码统计。

#### 2.5 若无系统样本库，如何降级？

本文降级为 **guideline / methodological seed**，其两套维度来源分别处理：

1. 三维 Facet（Topic / Contribution / Research type）→ **schema_seed**，作为 Paper2 维度树构建的候选模式参考
2. 12 SR 对照维度 → **method_comparison_seed**，仅用于描述性方法对比，不进入领域统计池

降级后不参与 `survey_of_surveys/` 的跨论文频数统计，但在 A2a 精核时仍可贡献候选叶子定义和取值空间类型。

**现有 metadata.json 的降级记录已正确**：`"eligible_for_statistical_synthesis": false`，reason 为方法论文 / guideline-like seed。

---

### 3. 原生样本编码维度树 / 维度森林

由于本文是 guideline / methodological seed 而非基于样本的 empirical mapping，其"原生树"有两条主干：

#### 主干 A：SMS 三维分类 Facet（方法定义层）

```
SMS Classification Scheme (root)
├── Topic Facet (主题维度)
│   └── 取值：由具体领域决定，原文以 software product line variability 为例
│       ├── Variability modeling
│       ├── Variability management
│       ├── ...
│       └── 取值空间类型：开放枚举（领域相关，keywording 过程中迭代生成）
│
├── Contribution Facet (贡献维度)
│   ├── Process
│   ├── Method
│   ├── Model
│   ├── Tool
│   ├── Metrics
│   ├── ...
│   └── 取值空间类型：层级枚举（作者在 §2.4 给出但未列出完整闭合集；原文称「such as」）
│
└── Research Type Facet (研究类型维度)
    ├── Validation research
    ├── Evaluation research
    ├── Solution proposal
    ├── Philosophical paper
    ├── Opinion paper
    ├── Experience paper
    └── 取值空间类型：完整枚举（引用 Wieringa et al. 2006 的外部分类法）
```

**说明**：
- 这是作者在 §2.4 中描述的分类方案。原文未以表格形式列出所有类别的完整闭合集，而是通过文本和引用给出框架。
- Contribution Facet 的叶子列表是**非封闭的**（「such as process, method, model, tool, metrics」），完整集仍需回到原文检查或确认。A2a 精核任务之一：逐字确认 §2.4 原文中 Contribution Facet 的完整列举。
- 这三个 Facet 之间通过 bubble plot 形成**交叉关系**（如 Topic × Contribution、Topic × Research Type），即 facet 间不是简单树而是可组合的 graph/dimension matrix。

#### 主干 B：SR vs SMS 对照维度（对照分析层）

```
SR-vs-SMS Comparison (root)
├── 研究目标 (Goal)
│   ├── SR: 回答具体研究问题 / 聚合证据
│   ├── SMS: 分类和结构研究领域
│   └── 取值空间类型：二元对比
├── 广度 (Breadth)
│   ├── SR: 窄 / 聚焦
│   ├── SMS: 宽 / 概览型
│   └── 取值空间类型：二元对比
├── 深度 (Depth)
│   ├── SR: 深入分析方法和结果
│   ├── SMS: 粗粒度分类
│   └── 取值空间类型：二元对比
├── 分析方法 (Analysis Method)
│   ├── SR: meta-analysis / narrative synthesis
│   ├── SMS: frequency statistics / bubble plots / cross-tabulation
│   └── 取值空间类型：二元对比
├── 效度问题 (Validity Issues)
│   ├── SR: 高内部效度要求
│   ├── SMS: 侧重外部效度 / 覆盖度
│   └── 取值空间类型：二元对比
├── 意义/产出 (Implications)
│   ├── SR: 实践证据推荐
│   ├── SMS: 研究空白识别 / 为后续 SR 指路
│   └── 取值空间类型：二元对比
└── 取值空间类型：层级枚举（来自 §3 和 Table 2 的对比维度）
```

**说明**：
- 主干 B 来自 §3 的 SR 分析和 Table 2 的 SMS vs SR 差异表。
- 这六个维度是从 text 提取的，但原文是否使用完全相同的一组名称、Table 2 的确切列数，仍需 PDF 视觉核验。
- 主干 B 不是"编码 primary study"的树，而是"方法学对比"的维度表。对 Paper2 的价值在于：它提供了区分 SMS 和 SR 的维度框架，可用于判断被纳入的 SLR/SMS 的类型。

#### 补充说明：A2a 精核任务

| 任务 | 内容 |
|---|---|
| 1 | 核查 §2.4 原文 Contribution Facet 的完整列表（是否只列举了 process/method/model/tool/metrics 五项，还是有更多） |
| 2 | 确认 Wieringa et al. 2006 中 Research Type Facet 的完整枚举（原文§2.4 列出 6 类，是否完整） |
| 3 | 从 PDF 确认 Table 1（12 SR 对照表）的确切列名和行数 |
| 4 | 从 PDF 确认 Table 2（Map vs Review 差异表）的确切字段名 |
| 5 | 检查 §2.5 是否有 bubble plot 插图及其编号 |

---

### 4. 叶子维度表

下表的"叶子"来自上文两条主干的末端节点。所有叶子均为 `schema_seed` 级别，不进入定量统计。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `leaf-p08-topic` | 主题分类 | Topic Facet | §2.4 keywording 描述 | 按领域子主题划分研究领域。由 keywording 过程中从摘要/关键词聚类产生 | {由具体领域决定} 例如 variability modeling / variability management 等 | 开放枚举 | 某论文若未在任何子主题中出现，可能属于新主题或分类不完整 | 计算各主题的论文数量，生成频率分布；与 contribution facet 交叉生成气泡图 | 识别研究空白、主题热度变化 | 锚点 4 | 取值空间完全取决于目标领域；Paper2 在 SLR/SMS 领域需自行设计主题维度 |
| `leaf-p08-contribution` | 贡献形态 | Contribution Facet | §2.4 keywording 描述；原文列出 "process, method, model, tool, metrics" | 按论文贡献形态划分：方法论、模型、工具、度量等 | {process, method, model, tool, metrics} + 其他未列出的形态 | 层级枚举（非封闭） | 未归类的论文可能属于未预见的贡献形态，应记录 rationale | 频率分布；与其他 facet 交叉 | 判断某领域以哪种贡献形态为主（如工具多→工程化成熟，方法多→早期） | 锚点 4 | 类别集合非封闭，Paper2 需补完并冻结；迁移时需改造成 SLR/SMS 专属 contribution 分类（如 method paper / empirical survey / meta-analysis / guideline 等） |
| `leaf-p08-research-type` | 研究类型 | Research Type Facet | §2.4 引用 Wieringa et al. 2006 | 按研究范式分类 | {validation research, evaluation research, solution proposal, philosophical paper, opinion paper, experience paper}（6 类等） | 外部分类法引用（完整枚举引用） | 无归类的论文可能不属于 Wieringa 六类中的任一项，需记录 | 频率分布；交叉分析 | 判断领域的研究成熟度（validation/evaluation 多→实证成熟，opinion 多→初期） | 锚点 4 | 引用 Wieringa 分类法可能不完全适用 SLR/SMS 领域；Paper2 需评估是否需要自定义研究类型维度 |
| `leaf-p08-sr-goal` | SR 研究目标 | SR-vs-SMS → Goal | §3 + Table 2 | 现有 SE 系统综述的研究目标特征：回答具体 RQ、聚合证据 | "回答具体 RQ" vs "分类概览" | 二元对比 | 若 SR 未明确区分 goal 类型，可能需要人工判断 | 不直接用于统计；用于区分 SR vs SMS 类型定义 | 帮助判定一篇被纳入论文是 SR 还是 SMS，影响后续字段选用 | 锚点 9 | 对 SLR/SMS survey of surveys 而言，此维度是类型判定依据而非编码字段 |
| `leaf-p08-sr-breadth` | 研究广度 | SR-vs-SMS → Breadth | §3 + Table 2 | 窄/聚焦 vs 宽/概览 | "窄/聚焦" vs "宽/概览" | 二元对比 | 未明确描述广度的 SR 可能为中间状态 | 判定 survey 类型 | 用于维度森林中 type-classification 子树的判定节点 | 锚点 9 | 同上 |
| `leaf-p08-sr-depth` | 分析深度 | SR-vs-SMS → Depth | §3 + Table 2 | 深入分析 vs 粗粒度分类 | "深入分析方法和结果" vs "粗粒度分类" | 二元对比 | — | 判定 survey 类型 | 同上 | 锚点 9 | 同上 |
| `leaf-p08-analysis-method` | 分析方法 | SR-vs-SMS → Analysis Method | §3 + Table 2 | meta-analysis / narrative synthesis vs frequency / bubble plot | {meta-analysis, narrative synthesis, frequency statistics, bubble plots, cross-tabulation} | 层级枚举 | — | 可用于编码 SLR/SMS 的分析方法选择 | 观察领域内分析方法的使用偏好和演化趋势 | 锚点 9 | 取值集合需从原文扩展，当前仅描述了 SR 与 SMS 两端，未枚举全部可能方法 |
| `leaf-p08-implications` | 产出类型 | SR-vs-SMS → Implications | §3 + Table 2 | 实践证据推荐 vs 研究空白识别 | {实践证据推荐, 研究空白识别, 对后续 SR 的指引} | 层级枚举 | 某些 survey 的 implication 可能同时具有多种类型 | 编码 survey 的产出意图 | 区分不同类型 survey 的价值产出 | 锚点 9 | 对 Paper2 的 survey-of-surveys 而言，可用于但需细化取值层次 |

---

### 5. 关系边表

本文作为 methodology paper，其"维度森林"的核心结构特征是 **Facet 之间的可交叉组合关系**，而非树状父子关系。此外 SR-vs-SMS 对照表构成一组平行对比关系。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `rel-p08-facet-cross` | Topic Facet | cross-tabulation | Contribution Facet | Contribution 的取值空间 | 若某交叉格子为空，表示该子主题中暂无该类贡献形态的论文→候选研究空白 | 锚点 5（bubble plot） | 生成二维气泡图；对 Paper2 而言，Survey 类型 × 方法特征的交叉是核心分析模式 |
| `rel-p08-facet-cross-rt` | Topic Facet | cross-tabulation | Research Type Facet | Research Type 的取值空间 | 同上逻辑 | 锚点 5 | 同上 |
| `rel-p08-sr-vs-sms-goal` | SR | contrastive | SMS | {具体 RQ 型, 概览型} | — | 锚点 9,10 | 定义 SR 与 SMS 的核心方法论差异 |
| `rel-p08-sr-vs-sms-breadth` | SR | contrastive | SMS | {窄/聚焦, 宽/概览} | — | 锚点 9,10 | 同上 |
| `rel-p08-sr-vs-sms-depth` | SR | contrastive | SMS | {深, 浅} | — | 锚点 9,10 | 同上 |
| `rel-p08-sr-vs-sms-method` | SR | contrastive | SMS | 两类分析方法的取值空间 | — | 锚点 9,10 | 同上 |
| `rel-p08-sr-vs-sms-validity` | SR | contrastive | SMS | {高内部效度, 侧重外部效度} | — | 锚点 9,10 | 同上 |
| `rel-p08-sr-vs-sms-implications` | SR | contrastive | SMS | {实践推荐, 空白识别} | — | 锚点 9,10 | 同上 |

**说明**：本文未发现其他类型的显式关系边（如因果关系、依赖关系、层级包含关系）。核心关系模式是 Facet 交叉制表（cross-tabulation）和方法对比（contrastive comparison），这与 SMS 的"通过类别频数和交叉覆盖发现模式"的方法目标一致。

---

### 6. 统计观察、候选 finding 与 final finding 边界

#### 6.1 原文统计观察（原文中由字段/统计表支持的）

由于本文无系统样本库（见 §2），"统计观察"是指：

1. **Facet 间交叉频数**（§2.5）：作者在自身 SMS 实践（Mujtaba et al. 2008, submission）中按 Facet 交叉生成频率表和 bubble plot。**原文未给出这些频率表的具体数值**，仅描述了方法。
2. **12 篇 SR 的 method 特征**（§3）：作者分析 12 篇 SR 在 search strategy、screening、data extraction 等方面的一致性/差异模式。原文是否给出 12 篇 SR 的完整 table 信息需 PDF 核验。

**对 Paper2 的含义**：无直接可引用的统计数值，只有可借鉴的分析模式。

#### 6.2 候选 finding（原文 discussion / recommendation / roadmap 提出）

| 候选 finding | 原文来源 | 类型 | 对 Paper2 的启发 |
|---|---|---|---|
| SMS 和 SR 是互补性方法，应先后使用 | §4, §5 | methodological recommendation | Paper2 的 survey-of-surveys 应根据纳入论文的类型（SR/SMS/guideline）选用不同的编码维度和统计口径 |
| Keywording 过程中分类维度会演化，不是一次性冻结 | §2.4 | 过程 insight | Paper2 维度森林应在 A1→A2a→A2b 阶段迭代演化，保留 schema_evolve 记录 |
| 摘要质量不足时可看引言/结论 | §2.4 | 操作 heuristic | Paper2 的阅读深度分级应支持多级 reading depth |
| 可视化（bubble plot）对呈现 SMS 结果至关重要 | §4 | presentation guideline | Paper2 应设计 survey-of-surveys 的可视化呈现方案 |
| 每篇论文的归类应有短 rationale | §2.5 | data quality guideline | 对照现有的 `field_level_rationale` 机制：Paper2 应保留每篇纳入论文在各维度的归类理由 |

#### 6.3 对 Paper2 可迁移的方法学启发

| 启发 | 迁移方式 |
|---|---|
| 三维分类 Facet 框架 | Paper2 的维度森林可按 method/domain/contribution-type 等轴组织 |
| Facet 交叉制表 | 用 cross-tabulation 发现"SLR/SMS 方法特征 × SE 子领域"的模式 |
| Keywording 迭代机制 | 维度树从 seed 开始，随论文阅读持续新增/合并/拆分叶子 |
| 广覆盖优先于过早深挖 | survey-of-surveys 不应只收高等级 SLR，保留 SMS/guideline/roadmap 边界样本 |
| Bubble plot 呈现 | Paper2 可使用二维气泡图呈现调查方法的交叉分布 |

#### 6.4 绝不能迁移的领域结论

本文结论关于 **software product line variability**（Mujtaba et al. 2008）的具体频数、空白断言、"12 篇早期 SR 的具体方法特征"——这些都是 SE 领域特定发现，与 SLR/SMS survey-of-surveys 目标领域不重合，不可迁移。

---

### 7. 对现有 `review.md` 的返修建议

#### 总体评价

现有 `review.md`（331 行）整体**结构完整、证据记录充分**，在 A1-DT v2 要求下存在以下问题：

#### C 级（必须修复）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| C1 | "通用六叶接口"历史残留 | `review.md` 的 A.1 节（截断部分可见 `leaf-petersen-2008-systematic-mapping-scope` 等标识）仍把「范围 / 语料 / 分类 / 方法 / 证据 / finding」六叶作为节点插入维度森林 | **删除**所有六叶节点标识，完整替换为本审计报告 §3 的双主干结构。保留现有 A1DT 修复记录（C13）作为施工日志，但正文维度树必须以原文 Facet 和 SR-vs-SMS 对照维度为准 |
| C2 | 维度树复原不完整 | 现有 review 在"分类维度与字段模式"（§2.4）中描述了三个 Facet，但未以树形或表形完整展开叶子取值空间 | 将 §2.4 的内容升级为本审计报告 §3 主干 A 的完整 text tree，补充每个叶子的取值空间类型和封闭性判定 |
| C3 | 缺失 SR-vs-SMS 对照维度树 | 现有 review 在 §2.3 和 §3 部分提到了 SR 对比，但未将 §3/Table 2 的对照维度单独作为一条维度主干提取 | 补充本审计报告 §3 主干 B 的对照维度树 |

#### I 级（应该修复）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| I1 | A.2 证据账本中"通用叶子"证据行需重写 | A.2（截断末尾可见 `[leaf-petersen-2008-systematic-mapping-scope]` 等标识） | 将 A.2 中与六叶接口相关的证据行替换为基于原文真实 Facet 的证据锚点（参照本审计报告 §4 叶子维度表） |
| I2 | A.3 结论-证据映射中结论标识不精确 | A.3（可见 `[clm-petersen-2008-systematic-mapping-leaf-scope]` 等） | 将结论标识从六叶命名改为双主干叶子标识（如 `[clm-p08-topic-facet-as-method-seed]`） |
| I3 | SUMMARY 表需确认一致性 | survey_of_surveys/SUMMARY.md | 确认"样本单位 / 样本数量 / 原生树类型 / 统计池资格"与本审计报告 §0 卡片一致。当前 `metadata.json` 中的 `eligible_for_statistical_synthesis: false` 正确。SUMMARY 表中如有六叶误入需同步清理 |

#### M 级（建议修复）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| M1 | A.4 本地复验命令缺少 A2a 精核任务清单 | A.4 | 补充本审计报告 §3 末尾的 A2a 精核任务 1-5 |
| M2 | review.md 快速结论卡片应增补"原生树类型"和"降级理由"字段 | §1 | 在快速结论卡片中显式增加"原生树类型：降级树（guideline seed + method comparison seed）"和"降级理由：无系统 sample 库，Facet 为方法论建议，SR 对照为辅助分析" |
| M3 | 参考文献格式建议 | §References（review.md 无此节） | 若 review.md 后续需独立作为报告发布，建议增加参考文献节，引用 Wieringa et al. 2006 和 Kitchenham & Charters 2007 等被本文依赖的外部 taxonomy |

---

### 8. 审计附录草案：证据账本与结论映射

以下草案可直接迁移到 `review.md` 的 A.2 / A.3 节（替换现有六叶相关条目）。

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| `EV-p08-001` | paper_content.txt | Abstract | 第 1 段 | 「build a classification scheme and structure a software engineering field」 | 定义 SMS 核心目标：通过 classification scheme 结构化研究领域 | strong | `dim-p08-root` | 否 | — |
| `EV-p08-002` | paper_content.txt | §2.1 | §2.1 全文 | 「The five steps of the mapping process are...」 | 定义 SMS 五步流程 | strong | `dim-p08-root` | 否 | — |
| `EV-p08-003` | paper_content.txt | §2.4 | 第 2-3 段 | 「keywording is done in two steps... the set of keywords will evolve」 | 证明 keywording 是一个迭代演化过程，分类方案在读摘要过程中动态形成 | strong | `leaf-p08-topic`, `leaf-p08-contribution` | 否 | — |
| `EV-p08-004` | paper_content.txt | §2.4 | 中段 | 「Three facets: topic facet, contribution facet, research type facet...」 | 作者明确给出三维分类 Facet | strong | `leaf-p08-topic`, `leaf-p08-contribution`, `leaf-p08-research-type` | 需核验原文是否给出每个 Facet 的完整类别列表 | — |
| `EV-p08-005` | paper_content.txt | §2.4 | Contribution Facet 描述 | 「such as process, method, model, tool, metrics」 | Contribution Facet 的示例叶子，但不一定是完整枚举 | moderate | `leaf-p08-contribution` | 需核验原文是否在别处给出了完整列表 | "such as"暗示非封闭枚举 |
| `EV-p08-006` | paper_content.txt | §2.4 | Research Type 引用 | 引用 Wieringa et al. 2006 的六类 | Research Type Facet 引用外部 taxonomy | moderate | `leaf-p08-research-type` | 需交叉核验 Wieringa 原文确认六类的完整性和适用性 | 外部引用，分类法本身可能有后续修订 |
| `EV-p08-007` | paper_content.txt | §2.5 | 频数/气泡图描述 | 「frequency of publications... bubble plot combining facets...」 | 定义 SMS 的分析方法和呈现手段 | strong | `rel-p08-facet-cross` | 需核验是否有 bubble plot 插图及其编号 | — |
| `EV-p08-008` | paper_content.txt | §3 | 全文 | 「we analyze the differences between systematic review and systematic mapping studies」 | 定义 SR vs SMS 对比的目标 | strong | `dim-p08-sr-compare` | 需核验 Table 1 和 Table 2 的确切列名 | — |
| `EV-p08-009` | paper_content.txt | §3 | Table 2 线索 | 对比 goal、breadth、depth、validity、implications | 定义 SR vs SMS 的差异维度 | moderate | `leaf-p08-sr-goal`, `leaf-p08-sr-breadth`, `leaf-p08-sr-depth`, `leaf-p08-analysis-method`, `leaf-p08-implications` | 需 PDF 视觉核验 Table 2 | text 中列名可能与 Table 2 实际列名有措辞差异 |
| `EV-p08-010` | paper_content.txt | §4 | guideline 段落 | 「visualizing results... should be more widely used」 | 补充 guideline：强调可视化在 SMS 中的重要性 | moderate | `clm-p08-visual-importance` | 否 | guideline 强度视后续 empirical evidence 而定 |
| `EV-p08-011` | paper_content.txt | §5 | Conclusions | 「systematic maps and reviews... should and can be used complementary」 | 核心方法学结论：SMS 与 SR 互补 | strong | `clm-p08-complementary` | 否 | — |
| `EV-p08-012` | paper_content.txt | §2.5 | 末段 | 「claims as to where there are research gaps can be made」 | SMS 可产出研究空白识别 | moderate | `clm-p08-gap-claim` | 否 | 空白识别的可靠性仍需更多实证 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| `clm-p08-sms-process-defined` | SMS 五步流程可用于 SE mapping | method_claim | `dim-p08-root` | EV-p08-001, EV-p08-002 | strong | Paper2 可参考其流程设计 survey-of-surveys 的阅读-编码 pipeline | 流程是基于一次实践提炼，通用性需更多 SMS 验证（作者也承认此点） |
| `clm-p08-three-facets` | SMS 分类方案应由三维 Facet 组成：Topic / Contribution / Research Type | schema_seed | `leaf-p08-topic`, `leaf-p08-contribution`, `leaf-p08-research-type` | EV-p08-004, EV-p08-005, EV-p08-006 | moderate | Paper2 维度树可参考 Facet 思路设计多维交叉轴 | Contribution Facet 类别非封闭；Research Type 引用 Wieringa 可能不完全适用 SLR/SMS 领域 |
| `clm-p08-keywording-evolution` | 分类方案在 keywording 过程中迭代演化 | process_insight | `leaf-p08-topic`, `leaf-p08-contribution` | EV-p08-003 | strong | Paper2 维度森林应设计为迭代演化而非一次性冻结 | — |
| `clm-p08-cross-tab-analysis` | Facet 交叉制表是 SMS 的核心分析模式 | method_claim | `rel-p08-facet-cross`, `rel-p08-facet-cross-rt` | EV-p08-007 | moderate | Paper2 应以交叉制表作为主分析模式（如 Survey 类型 × 方法特征） | bubble plot 只适合二维交叉；三维以上需要其他 visualization |
| `clm-p08-sr-vs-sms` | SR 和 SMS 在 goal/breadth/depth/validity/implications 方面有根本差异 | method_comparison | `leaf-p08-sr-goal`, `leaf-p08-sr-breadth`, `leaf-p08-sr-depth`, `leaf-p08-analysis-method`, `leaf-p08-implications` | EV-p08-008, EV-p08-009 | moderate | Paper2 的 survey-of-surveys 可根据这些维度区分纳入论文的类型，选用不同编码口径 | 对比维度来自 2008 年的 12 SR，可能不覆盖后续 SLR 方法学进展 |
| `clm-p08-complementary` | SMS 和 SR 应互补使用，先 mapping 后 review | methodological_recommendation | `dim-p08-root` | EV-p08-011 | strong | 支持 Paper2 survey-of-surveys 同时收录 SMS 和 SR 的设计决策 | — |
| `clm-p08-visual-importance` | 可视化（bubble plot）对 SMS 结果呈现至关重要 | presentation_guideline | `rel-p08-facet-cross` | EV-p08-010 | weak | Paper2 最终应产出可视化产物 | 结论来自方法论建议而非实证比较 |
| `clm-p08-gap-claim` | SMS 可产出研究空白声明 | candidate_finding | `clm-p08-gap-claim` | EV-p08-012 | weak | 可作为 Paper2 的候选 finding 类型模板，但需跨论文验证 | 单篇 SMS 的空白声明可靠性有限；需反证 |
| `clm-p08-rationale-per-item` | 每篇论文的归类应有短 rationale | data_quality_guideline | `leaf-p08-contribution`, `leaf-p08-topic` | EV-p08-003（隐含） | moderate | Paper2 的 field-level-rationale 机制与此一致 | — |

---

### 9. 技能使用与自我审查记录

#### 9.1 已读取的技能文件与采用原则

| 技能文件 | 读取状态 | 采用原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | ✅ 完整读取 | 采用「claim-evidence-engineering」原则：每个结论必须有原文证据锚点，否则降级为 `schema_seed`、`weak` 或 `candidate_finding`；不编造 citation |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | ✅ 完整读取 | 采用「constructive specificity standard」：每个返修建议指向原文具体位置；采用「common reviewer concerns」框架（贡献不清、实验不支撑 claim、局限未声明）评审现有 review.md |
| `ai-research-writing-skill/references/reviewer-self-review.md` | ✅ 完整读取 | 采用「adversarial questions」框架自审本报告：核心贡献是否明确、每一 leaf 是否有原文证据、取值空间类型判定是否有原文根据 |
| `research-planning/SKILL.md` | ✅ 完整读取 | 采用「task dependency graph」思路组织 A2a 精核任务列表 |
| `research-planning/references/planning-prompts.md` | ✅ 完整读取 | 未直接使用 plan submission 模板，但借鉴了 structured planning 的分层思路（总体→架构→逻辑→配置）组织本报告的 §3 双主干 |
| `research-planning/references/output-schemas.md` | ✅ 完整读取 | 未直接使用 JSON schema，但借鉴了 risks 三要素（risk / mitigation / severity）组织 §7 C/I/M 分级 |
| `autoresearch/SKILL.md` | ✅ 完整读取 | 借鉴「completion artifact-gated」原则：本报告必须包含完整自包含的 §0-§9，不能只给摘要或引用前文 |

#### 9.2 本输出最高风险 3 点

| # | 风险 | 严重程度 | 主线程合并时复核建议 |
|---|---|---|---|
| 1 | **Contribution Facet 取值空间非封闭** | M | `paper_content.txt` 中描述为 "such as process, method, model, tool, metrics"——原文可能仅在 §2.4 文本中列举了这些作为示例，完整闭合集需返回 PDF 原文确认。若原文确实未给出闭合集，本报告 §4 中 `leaf-p08-contribution` 应明确标记为 "开放枚举 + 已列举示例"，而不是 "层级枚举" |
| 2 | **SR-vs-SMS 对照维度的确切列名依赖 text 推断** | M | Table 2 的确切列名在 `paper_content.txt` 的 text 提取中可能被压缩或变形。主线程合并时建议打开 PDF 人工核对 Table 2，确认 §3 主干 B 的 6 个维度是否与原文措辞一致 |
| 3 | **现有 review.md 的 A.1-A.4 附录结构可能与本审计报告§8 草案不一致** | L | 现有 review.md 已有 A.1-A.4，本报告 §8 提供了 A.2/A.3 的完整重写草案。合并时应注意：(a) 保留现有 review 中 A.4 的复验命令和 A.1 的施工日志价值；(b) 删除六叶接口相关的证据行和结论；(c) 新旧证据标识的命名空间不要冲突 |

#### 9.3 本任务执行状态

| 状态 | 说明 |
|---|---|
| blocked | 否 |
| timeout | 否 |
| 文件缺失 | 否 — 所有必需文件均已成功读取 |
| PDF 版面核验 | **未完成**（已明确记录） |
| 能否直接用于重写 review.md | 是 — §0, §3, §4, §5, §7, §8 可直接迁移 |

---

*以上为 `deepseek` agent 对 `petersen-2008-systematic-mapping` 的完整 A1-DT v2 审计报告。所有结论均基于对 `paper_content.txt` 全文的通读，未引用外部 LLM 或子 agent。*