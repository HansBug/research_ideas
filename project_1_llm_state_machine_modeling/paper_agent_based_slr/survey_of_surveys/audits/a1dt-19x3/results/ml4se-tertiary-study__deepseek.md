# ml4se-tertiary-study · deepseek 全文审计报告

## 1. 审计身份与输入

| 项 | 内容 |
|---|---|
| reviewer 身份 | deepseek |
| 审计日期 | 2026-06-29 |
| 是否读取 `$ai-research-writing-skill` | 是。读取路径：`/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并加载其 Reviewer mode 所需的两份 reference：`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`，以及 Story mode 的 `references/paper-story.md`。 |
| 是否读取 `$research-planning` | 是。读取路径：`/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 及 `references/planning-prompts.md`。 |
| 是否读取 `$oh-my-codex:autoresearch` | 是。读取路径：`/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。 |
| 是否完整阅读 `paper_content.txt` | 是。完整阅读 1774 行，覆盖：摘要、Introduction（pp.1-2）、Related Work / Background（pp.2-4）、Method（pp.4-11）：RQ 定义、检索策略、纳排标准、筛选流程、质量评价 DARE-4、数据抽取 11 字段、ML 分类方案 5 大类、编码方案；Results（pp.11-26）：RQ1 覆盖分布、RQ2 未覆盖区域与 challenges、RQ3 ML 技术分布、RQ4 质量评估；Implications 8 条（pp.24-27）；Threats to Validity（pp.27-28）；Conclusions（pp.28-29）；References（pp.29-37）。 |
| 是否核对 `paper.pdf` | 否。当前审计环境无法视觉打开 PDF；但 `paper_content.txt` 已提供完整正文文本，包括表格结构说明（Tables 1-6、Figure 1）和脚注中 CSV 制品路径。以下涉及表格 / 图的精确数值核对一律标注"待 PDF 视觉核验"。 |
| 文库规则读取 | 是。已读取 `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md` 及 `story/paper_story.md`。 |
| 论文文件读取 | 是。已读取 `bibtex.bib`、`metadata.json`、`paper_content.txt`（全文）、`review.md`（全文 171 行）。 |

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文定义了 **4 个显式 RQ**（Section 3.1）：

| RQ | 内容 | 回答方式 |
|---|---|---|
| RQ1 | What SE tasks have been tackled with ML techniques? | 从每篇 secondary study 提取 SWEBOK KA / subarea / SE task(s)；通过 open coding → qualitative content analysis 归类。每个 secondary study 关联 1-3 个 SE task。 |
| RQ2 | What SE knowledge areas could be better covered by ML techniques? | 基于 RQ1 的覆盖分布识别未覆盖 / 稀疏覆盖 KA；从 secondary studies 的 abstract / introduction / results / conclusion / future directions 中抽取 implications for further research 和 ML-related obstacles。 |
| RQ3 | What ML techniques have been used in SE? | 使用 5 大类 ML 分类方案（Table 6），对每篇 secondary study 进行归类。 |
| RQ4 | What is the quality of the secondary studies? | 通过 DARE-4 质量评价（4 个 criterion），计算每篇得分，总分≥2 纳入。 |

原文的核心贡献声明（Abstract）为："We systematically collected, quality-assessed, summarized, and categorized 83 reviews in ML for SE published between 2009–2022, covering 6,117 primary studies."

### 2.2 原文方法流程

完整的方法流程（Section 3）包含以下阶段：

1. **检索策略**（Section 3.2）：
   - Automated search：7 个 digital libraries（ACM DL、IEEE Xplore、ScienceDirect、Scopus、SpringerLink、Web of Science、Wiley），时间范围 2015–2020，搜索字符串见 Table 1（3 组关键词组合：ML terms + SE terms + review type terms）。
   - Manual search：检索 9 个 SE 会议论文集和 5 个 SE 期刊。
   - Backward snowballing + Forward snowballing。

2. **纳排标准**（Section 3.3）：6 条 Inclusion Criteria + 6 条 Exclusion Criteria。

3. **筛选流程**（Section 3.4）：两步筛选（先 15 篇 pilot 达 Cohen's Kappa≥0.8，再分半独立筛选 1552 篇），通过 Figure 1（Review Protocol Overview）可视化。最终筛选出 140 篇 distinct secondary studies。

4. **质量评价**（Section 3.5）：DARE-4 4 个 criterion（QA1: IC/EC 定义；QA2: 搜索空间；QA3: 原始研究质量评价；QA4: 原始研究信息呈现），每 criterion 评分 Y(1)/P(0.5)/N(0)，总分≥2 纳入。57/140 排除，83 篇纳入，inter-rater agreement 82%。

5. **数据抽取**（Section 3.6）：**11 个显式抽取字段**（见下文 2.3）。

6. **ML 技术分类方案**（Section 3.6）：5 大类 + 子类（Table 6），类别包括：(1) Classification, Clustering, Regression; (2) Computational search and optimization techniques; (3) Deep and transfer, active, semi-supervised, reinforcement learning; (4) Fuzzy and probabilistic methods; (5) Search-based software engineering。

7. **编码方案**（Section 3.6）：open coding → qualitative content analysis：两位作者分别对半数据独立编码，从 title / author keywords / abstract / introduction 提取 code（SE tasks），然后讨论、泛化/特化、归组。

8. **统计分析**：频次分布（各 KA 的 secondary study 数量、各 ML 类别的 secondary study 数量）、覆盖度分析（哪些 KA 未被覆盖/稀疏覆盖）。

9. **发现形成**（Section 5 Discussion / Implications）：从统计观察到分布结论 → 8 条 Implications（Implication 1-8），每条附带来自 secondary studies 的 $n$ 计数支撑。

### 2.3 原文显式 extraction form / classification schema / taxonomy / coding scheme

#### 2.3.1 数据抽取字段（Section 3.6，11 个显式字段）

| # | 字段 | 类型 | 用途 |
|---|---|---|---|
| 1 | Title and source | 字符串 / 枚举（journal, workshop proceedings, conference proceedings, book chapter） | 元数据 |
| 2 | Publication year | 数值 | 时间趋势 |
| 3 | Publication venue | 枚举 | 出版者分布 |
| 4 | Author names, institutions, and countries | 字符串 | 研究团队分布 |
| 5 | Study type | 枚举（SLR, systematic mapping study, taxonomy...） | 综述类型分布 |
| 6 | Research method | 枚举 | 采用的 guideline |
| 7 | Quality assessment score | 数值（0-4） | 质量分层 |
| 8 | Number of primary studies | 数值 | secondary 规模 |
| 9 | Application domain (SWEBOK KA, subarea, SE tasks) | 分类 + 编码 | RQ1, RQ2 |
| 10 | Implications for further research / comments on ML in SE | 自由文本 | RQ2 |
| 11 | Employed ML techniques | 分类（5 大类 + 子类） | RQ3 |

#### 2.3.2 ML 技术分类方案（Table 6，5 大类 + 子类）

1. **Classification, Clustering, Regression**：包括 SVM、Naïve Bayes、Decision Trees、Random Forest、k-NN、Logistic Regression、Neural Networks、k-means 等子类。
2. **Computational search and optimization techniques**：包括 Genetic Algorithms、Particle Swarm Optimization、Ant Colony Optimization 等。
3. **Deep and transfer, active, semi-supervised, reinforcement learning**：包括 CNN、RNN、LSTM、Transfer Learning、Active Learning、Semi-supervised Learning、Reinforcement Learning 等。
4. **Fuzzy and probabilistic methods for reasoning in the presence of uncertainty**：包括 Fuzzy Logic、Bayesian Networks、Hidden Markov Models 等。
5. **Search-based software engineering**：包括 search-based methods 应用于 SE 问题。

#### 2.3.3 质量评价 rubric（DARE-4，Table 2）

| QA Criterion | 评价维度 | 评分 |
|---|---|---|
| QA1 | IC/EC 定义 | Y(1): 显式定义; P(0.5): 隐式定义; N(0): 未定义 |
| QA2 | 搜索空间 | Y(1): 4+ digital libraries + 额外策略; P(0.5): 3-4 libraries; N(0): 1-2 libraries |
| QA3 | 原始研究质量评价 | Y(1): 显式描述并应用; P(0.5): 隐式; N(0): 无 |
| QA4 | 原始研究信息 | Y(1): 完整信息; P(0.5): 摘要信息; N(0): 未说明 |

#### 2.3.4 SWEBOK KA 分类层次

原文以 SWEBOK 15 个 Knowledge Areas 作为顶层分类框架（Table 5），包含：Software Requirements、Software Design、Software Construction、Software Testing、Software Maintenance、Software Configuration Management、SE Management、SE Process、SE Models and Methods、Software Quality、SE Professional Practice、Engineering Foundations、Computing Foundations、Mathematical Foundations、SE Economics。

#### 2.3.5 编码方案

Open coding（从 title / author keywords / abstract / introduction 提取 SE task codes）→ Qualitative Content Analysis（两位作者讨论、泛化/特化、归组为概念相关的 task 类别）。每个 secondary study 最终关联至少 1 个、最多 3 个 SE task。

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的发现路径是严格分层推进的：

1. **字段抽取** → **频次统计**：从 83 篇纳入的 secondary study 中按 11 个字段抽取数据，形成 Tables 3-6。
2. **分布观察** → **RQ 回答**：
   - RQ1：统计各 SWEBOK KA 下 secondary study 的分布（Table 5），识别最常被 ML 覆盖的 SE 任务（Software Quality、Testing 等）。
   - RQ2：从 RQ1 覆盖分布识别未覆盖/稀疏覆盖的 KA（Software Construction、SE Economics 未被覆盖；SE Configuration Management、SE Models and Methods、SE Professional Practice 各仅 1 篇），并从 secondary studies 中抽取 implications 和 obstacles。
   - RQ3：统计各 ML 类别下 secondary study 的数量分布。
   - RQ4：通过 DARE-4 评分分布识别质量分层。
3. **统计观察 + 作者抽取** → **8 条 Implications**（Section 5）：每条 Implication 明确标注来自 $n$ 篇 secondary studies 的支撑。
4. **Threats to Validity**（Section 6）：按 Ampatzoglou et al. 分类方案，覆盖 Study Selection Validity、Data Validity、Research Rigor、Review Conclusion Validity 四个维度。
5. **Replication package**：CSV 文件记录了 cohen_kappa_agreement、study_selection、dare_assessment、knowledge_areas、backward_snowballing 等过程数据。

### 2.5 原文 artifact / replication package

原文在脚注中记录了以下 CSV 制品（Section 3）：
- `cohen_kappa_agreement.csv`
- `study_selection_reviewer_{1,2}.csv`
- `dare_assessment.csv`
- `knowledge_areas.csv`
- `backward_snowballing_references.csv`
- `backward_snowballing.csv`
- `forward_snowballing_reviewer_{1,2}.csv`

### 2.6 原文图表清单

| 表/图 | 内容 | 位置 |
|---|---|---|
| Table 1 | Search Keywords for Automated Search（3 组关键词） | Section 3.2 |
| Table 2 | DARE-4 Criteria for Quality Assessment（4 QA 维度 + 评分标准） | Section 3.5 |
| Table 3 | Studies passed QA per SLR guidelines（含 quality score、primary study 数量） | Section 4.1 |
| Table 4 | Studies passed QA in other SE secondary review types | Section 4.1 |
| Table 5 | Classification of Studies per SWEBOK KA（含 15 个 KA 的 secondary study 计数） | Section 4.2 |
| Table 6 | ML Classification per High-Level Category and Sub-Category（5 大类 + 子类 + 计数） | Section 4.4 |
| Figure 1 | Review Protocol Overview（PRISMA 式流程图） | Section 3 |

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树结构还原

从 `review.md` 的 A.2（证据账本）和 A.3（结论-证据映射）中可还原出以下维度树结构：

```
[dim-ml4se-tertiary-study-root]  "ml4se-tertiary-study 维度树根"
│
├── [leaf-ml4se-tertiary-study-scope]        "研究范围与单位对象"     ← A1-M0 通用叶子
├── [leaf-ml4se-tertiary-study-corpus]       "语料与纳排链条"        ← A1-M1 通用叶子
├── [leaf-ml4se-tertiary-study-taxonomy]     "主题与维度分类"        ← A1-M2 通用叶子
├── [leaf-ml4se-tertiary-study-method]       "方法/技术/干预分类"    ← A1-M3 通用叶子
├── [leaf-ml4se-tertiary-study-evidence]     "评价、证据与复现资产"   ← A1-M4 通用叶子
├── [leaf-ml4se-tertiary-study-finding]      "统计观察与候选发现"    ← A1-M7 通用叶子
│
└── [clm-ml4se-tertiary-study-source-schema-candidates] 下挂 5 个原文候选叶子:
    ├── [leaf-ml4se-tertiary-study-orig-se-problem]           "SE任务/领域"
    ├── [leaf-ml4se-tertiary-study-orig-ml-technique]         "ML技术/方法"
    ├── [leaf-ml4se-tertiary-study-orig-data-source]          "数据来源与质量"
    ├── [leaf-ml4se-tertiary-study-orig-evaluation-quality]   "评价证据与质量"
    └── [leaf-ml4se-tertiary-study-orig-challenge-recommendation] "挑战与建议"
```

### 3.2 逐项审计表

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-ml4se-tertiary-study-root]` 作为论文维度树根节点是合适的；该论文确实是一个完整 tertiary study，需要一棵维度树。 | 通过 |
| 主干分支是否覆盖原文 schema | **不通过** | 当前树的主干是 6 个 **A1-M0--M6 通用元维度叶子**（scope / corpus / taxonomy / method / evidence / finding），而非原文自身的 schema。原文真实的 11 个 extraction fields（2.3.1）、5 大类 ML 分类方案（2.3.2）、DARE-4 质量评价 schema（2.3.3）、SWEBOK 15 KA 分类层次（2.3.4）、open coding→qualitative content analysis 编码方案（2.3.5）均未被独立建模为叶子节点。5 个原文候选叶子虽部分覆盖，但严重不完整：例如"se-problem"无法区分原文的 SWEBOK KA 层次 vs SE task 编码两种不同粒度的分类；"ml-technique"只有一级分类，缺少原文的 5 大类→子类层次；"evaluation-quality"无法表达 DARE-4 的 4 个独立 criteria 评分。 | **C** |
| 叶子维度是否足够具体 | **不通过** | 6 个通用叶子是 A1-M 元维度——它们是"对所有 SLR/SMS paper 都适用的通用接口"，不是本文特有的维度。例如"corpus"对本文而言应展开为：双层分母（83 reviews ← 140 筛选 ← 6117 primary studies）、纳排 6+6 标准、自动+手动+雪球三种检索渠道；但当前只是一个短语标签。5 个原文候选叶子虽有 paper-specific 方向，但命名和粒度远不足以表达原文真实的 extraction form 字段结构。 | **C** |
| 取值空间是否可执行 | **不通过** | 6 个通用叶子在 `review.md` 中均未定义候选取值空间，只给出了节点标识和简短中文标签。5 个原文候选叶子的取值空间同样未定义（例如 `se-problem` 下应有哪些 SWEBOK KA 枚举值、`ml-technique` 下应有 5 大类 + 子类的完整枚举）。依据 `pattern-field-schema.md` §8.2 的取值空间规则，不定义取值空间的叶子无法进入统计。 | **I** |
| 关系边是否缺失 | **不通过** | 原文存在大量跨维度的固有关系：每个 secondary study 同时有 SWEBOK KA 归属 AND ML 技术归类 AND DARE-4 质量评分 AND 发表年份，这些形成交叉表（例如"哪些 KA 倾向于使用哪些 ML technique"）。当前树完全没有关系边（`[edge-*]`）记录，例如 `se-problem` ↔ `ml-technique` 的交叉、`quality_score` ↔ `publication_year` 的趋势。依据 `pattern-field-schema.md` §8.3 的关系边规则，这属于缺失链接。 | **I** |
| 统计用途 / 分母是否正确 | **不通过** | 当前树的所有叶子均未标注统计用途（是否用于频次、交叉表、趋势）、分母定义和统计池资格。原文有非常明确的分母：83 篇纳入 secondary studies（总分母）；Tables 3-6 各自的统计口径（per-KA 分布、per-ML-category 分布、per-quality-score 分布）。当前 `review.md` 的 A.3 中所有结论强度均为 `weak`，允许位置为 `schema_seed` 或 `candidate_finding`，这虽然符合 A1-DT 降级纪律，但也意味着当前的维度树完全不是一棵"可统计的树"，而只是一棵"概念占位树"。 | **I** |
| 候选 finding 路径是否完整 | **不通过** | 原文的 finding 路径是：抽取字段 → 统计分布 → RQ 回答 → 8 条 Implications（每条有 $n$ 计数支撑）→ 4 类 validity threats。当前树的 finding 叶子只有一个 `[leaf-ml4se-tertiary-study-finding]` 通用节点，没有区分：(1) RQ 层级的分布发现，(2) Implication 层级的 normative recommendation，(3) threat 层级的 validity limitation。原文 8 条 Implications 的具体内容（如"Implication 4: document and automate data pipeline"）未映射到树的任何分支。 | **C** |
| A.1--A.4 证据链是否足够 | 部分通过 | A.1 来源账本：记录了 bibtex、metadata.json、paper_content.txt、paper.pdf 四个入口，结构完整。A.2 证据账本：4 条证据（EV-001 ~ EV-004）均为全文泛定位（"本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"），未做具体章节/段落/表格锚定。A.3 结论-证据映射：结构符合合同，但所有结论强度均为 `weak`，所有允许位置均为 `schema_seed`，这意味着 A1-DT 当前不是一棵可用的维度树，而是一组等待 A2a 补充的概念标签。A.4 复验清单：结构检查 passed，视觉核验 needs_manual_check。A.2 证据锚定粒度过粗（缺乏精确页码和段落定位）是一个 **I 级问题**。 | **I** |
| 是否存在可能误导 A2a 的强主张 | 通过 | `review.md` 中所有结论均标注 `weak` + `schema_seed`，且 A.3 中 `[clm-ml4se-tertiary-study-source-schema-candidates]` 明确说明"这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结"。Section 2（六类 pattern 抽取）中对 validity_threat_pattern 标注"本轮未完整定位 threat 章节，不能强写完整核验"，不存在强主张风险。 | 通过 |

## 4. 建议维度树骨架

以下给出忠实于原文结构的建议维度树。该树基于对 `paper_content.txt` 全文（1774 行）的逐段阅读，所有节点均有原文 section 定位。

```
[dim-ml4se-tertiary-study-root] "Machine Learning for Software Engineering: A Tertiary Study 维度树 (Kotti et al., 2023)"

├── [dim-meta] "元数据层"
│   ├── [leaf-title] "标题"                         ← 原文 extraction field #1
│   ├── [leaf-year] "发表年份"                       ← 原文 extraction field #2（用于时间趋势）
│   ├── [leaf-venue] "发表 venue"                    ← 原文 extraction field #3
│   ├── [leaf-authors] "作者/机构/国家"              ← 原文 extraction field #4
│   ├── [leaf-study-type] "综述类型"                 ← 原文 extraction field #5
│   │   候选取值：{SLR, SMS, taxonomy, survey, mapping study, ...}
│   └── [leaf-research-method] "研究方法/guideline"  ← 原文 extraction field #6

├── [dim-search-n-selection] "检索与纳排层"
│   ├── [leaf-search-strategy] "检索策略"
│   │   候选取值：{automated, manual, backward_snowballing, forward_snowballing}
│   │   (原文 Section 3.2: 7 digital libraries + 14 venues + snowballing)
│   ├── [leaf-inclusion-criteria] "纳入标准"
│   │   候选取值：6 条 IC 枚举（原文 Section 3.3）
│   ├── [leaf-exclusion-criteria] "排除标准"
│   │   候选取值：6 条 EC 枚举（原文 Section 3.3）
│   ├── [leaf-selection-process] "筛选流程"
│   │   候选取值：{pilot_inter_rater, split_independent, full_text_consultation}
│   │   (原文 Section 3.4: Cohen's Kappa≥0.8 → 分半独立筛选)
│   └── [leaf-review-count] "纳入综述数量"
│       候选取值：整数（原文：83/140 passed QA；6117 primary studies）

├── [dim-quality-assessment] "质量评价层"
│   ├── [leaf-qa-framework] "评价框架"
│   │   候选取值：{DARE-4, DARE-5, ...}（原文：DARE-4）
│   ├── [leaf-qa1-ic-ec] "QA1: IC/EC 定义"
│   │   候选取值：{Y(1), P(0.5), N(0)}（原文 Table 2）
│   ├── [leaf-qa2-search] "QA2: 搜索空间"
│   │   候选取值：{Y(1), P(0.5), N(0)}
│   ├── [leaf-qa3-primary-qa] "QA3: 原始研究质量评价"
│   │   候选取值：{Y(1), P(0.5), N(0)}
│   ├── [leaf-qa4-primary-info] "QA4: 原始研究信息呈现"
│   │   候选取值：{Y(1), P(0.5), N(0)}
│   ├── [leaf-qa-total-score] "DARE-4 总分"
│   │   候选取值：数值 [0, 4]（步长 0.5；原文 inclusion threshold ≥2）
│   └── [leaf-inter-rater] "评分者一致性"
│       候选取值：数值 [0, 1]（原文：82%）

├── [dim-domain-classification] "领域分类层"
│   ├── [leaf-swebok-ka] "SWEBOK KA（知识领域）"
│   │   候选取值：{Software Requirements, Software Design, Software Construction, Software Testing,
│   │             Software Maintenance, Software Configuration Management, SE Management, SE Process,
│   │             SE Models and Methods, Software Quality, SE Professional Practice, Engineering Foundations,
│   │             Computing Foundations, Mathematical Foundations, SE Economics}
│   │   (原文 Table 5: 15 个 KA)
│   ├── [leaf-se-task] "SE 任务（open coding 编码结果）"
│   │   候选取值：开放枚举（原文 Section 3.6: open coding → qualitative content analysis；
│   │   每篇 secondary study 关联 1-3 个 task code）
│   │   示例：test automation, software defect prediction, bug prioritization,
│   │         traceability link recovery, concept location, effort estimation, ...
│   ├── [leaf-se-subarea] "SE 子领域"
│   │   候选取值：SWEBOK subarea 枚举（原文 Section 4.2 按 KA 展开）
│   └── [edge-swebok-se-task] "KA ↔ SE task 映射"
│       关系类型：属于（原文 Section 3.6: "a SE task may be associated with multiple KAs"）

├── [dim-ml-classification] "ML 技术分类层"
│   ├── [leaf-ml-category] "ML 大类"
│   │   候选取值：{Classification/Clustering/Regression, Computational search/optimization,
│   │             Deep/transfer/active/semi-supervised/RL, Fuzzy/probabilistic,
│   │             Search-based SE}
│   │   (原文 Table 6: 5 大类)
│   ├── [leaf-ml-subcategory] "ML 子类"
│   │   候选取值：{SVM, Naïve Bayes, Decision Trees, Random Forest, k-NN, Logistic Regression,
│   │             Neural Networks, k-means, Genetic Algorithms, PSO, ACO, CNN, RNN, LSTM,
│   │             Transfer Learning, Active Learning, Semi-supervised, RL, Fuzzy Logic,
│   │             Bayesian Networks, HMM, ...}
│   │   (原文 Table 6 完整枚举)
│   └── [edge-ka-ml] "KA ↔ ML technique 交叉"
│       关系类型：交叉引用（原文 Section 4.2 按 KA 展开时描述各 KA 下使用的主要 ML 技术）

├── [dim-findings] "发现层"
│   ├── [leaf-rq-answer] "RQ 答案"
│   │   候选取值：分布描述文本（原文 Section 4: RQ1-RQ4 回答）
│   │   可统计：是（基于 Table 3-6 的频次统计）
│   ├── [leaf-implication] "Implication / 研究挑战"
│   │   候选取值：{Implication 1: empirical validation & industrial studies,
│   │             Implication 2: reconsider deficient SE methods,
│   │             Implication 3: human-centered SE areas,
│   │             Implication 4: document & automate data pipeline,
│   │             Implication 5: industrial data sharing,
│   │             Implication 6: online & incremental ML,
│   │             Implication 7: hybrid ML techniques,
│   │             Implication 8: reproducibility}
│   │   (原文 Section 5: 每条有 n 计数支撑)
│   │   可统计：否（规范性建议，但每条有 n 计数可作为影响力信号）
│   ├── [leaf-implication-n-support] "Implication 支撑计数"
│   │   候选取值：整数（原文每条 Implication 标注来自多少篇 secondary studies）
│   └── [edge-rq-implication] "RQ 答案 → Implication 推导"
│       关系类型：支撑（原文从分布观察到 normative recommendation 的推导逻辑）

├── [dim-validity] "效度威胁层"
│   ├── [leaf-threat-search-selection] "检索与筛选效度"
│   │   候选取值：文本描述（原文 Section 6: Study Selection Validity）
│   ├── [leaf-threat-data] "数据效度"
│   │   候选取值：文本描述（原文 Section 6: Data Validity）
│   ├── [leaf-threat-rigor] "研究严谨性"
│   │   候选取值：文本描述（原文 Section 6: Research Rigor）
│   └── [leaf-threat-conclusion] "结论效度"
│       候选取值：文本描述（原文 Section 6: Review Conclusion Validity）

└── [dim-artifacts] "制品层"
    ├── [leaf-csv-artifacts] "CSV 过程制品"
    │   候选取值：{cohen_kappa_agreement.csv, study_selection_reviewer_{1,2}.csv,
    │             dare_assessment.csv, knowledge_areas.csv, backward_snowballing_*.csv,
    │             forward_snowballing_reviewer_{1,2}.csv}
    │   (原文 Section 3 脚注)
    ├── [leaf-figure1] "Figure 1: Review Protocol Overview"
    │   候选取值：流程图（PRISMA-style）
    └── [leaf-tables] "统计表"
        候选取值：{Table 1: search keywords, Table 2: DARE-4 criteria, Table 3: QA-passed SLRs,
                  Table 4: QA-passed other types, Table 5: per-KA classification,
                  Table 6: per-ML-category classification}
```

### 4.1 建议树与当前树的关键差异

| 差异维度 | 当前树 | 建议树 | 原因 |
|---|---|---|---|
| 叶子数量 | 6 通用 + 5 候选 = 11 | ~40（含分类枚举） | 当前树是 A1-M 元维度投影，不是原文 schema 还原 |
| 分层结构 | 扁平（1 层根 + 1 层叶） | 7 个 dim 分组 + 多级 leaf | 原文有自然的分层：元数据→检索→质量→领域→技术→发现→效度→制品 |
| 取值空间 | 全部未定义 | 每个 leaf 有枚举或类型定义 | 不定义取值空间就无法统计；字段合同要求可执行 |
| 关系边 | 无 | 3 条（KA↔task, KA↔ML, RQ→implication） | 原文的交叉分析与推导逻辑本就是研究价值所在 |
| 统计用途 | 未标注 | 每个 leaf 标注可否统计 + 分母 | 这是 pattern-field-schema.md §8.2 的必填合同 |
| 原文特有字段 | 5 个粗粒度候选 | 11 个 extraction fields + DARE-4 4 criteria + SWEBOK 15 KA + ML 5 大类 + 8 implications + 4 threats + CSV artifacts | 当前树丢失约 75% 的原文结构化信息 |
| 质量评价 | 混在 "evidence" 叶子 | 独立 dim 分组 + 4 criteria + 总分 + inter-rater | DARE-4 是原文方法的核心组件，不应混入通用 "evidence" |
| Coding scheme | 完全缺失 | 在 domain-classification 下独立建模 | Open coding → qualitative content analysis 是原文的关键方法贡献 |
| Validity threats | 完全缺失 | 独立 dim 分组 + 4 个 threat 类型 | 原文 Section 6 是整个讨论的关键组成部分 |
| Artifacts / replication | 完全缺失 | 独立 dim 分组 + CSV + 图表 | 原文有 7+ 个 CSV 制品文件和 6 个表 + 1 个图 |

## 5. 必须补充 / 修正清单

| # | 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|---|
| 1 | 维度树主干从通用 6 叶替换为原文 schema 树 | `review.md` A.2/A.3 维度节点清单 | 用 §4 建议树的 7 个 `[dim-*]` 分组 + ~40 个 `[leaf-*]` 替换当前 6+5 结构。当前 6 个通用叶子（scope/corpus/taxonomy/method/evidence/finding）应在 Paper2 的 A1-M 元维度总表中统一维护，不应在单篇 review 中冒充原文 schema。 | `paper_content.txt` Section 3.6（11 extraction fields）、Table 2（DARE-4）、Table 5（SWEBOK KA）、Table 6（ML categories）、Section 5（8 Implications）、Section 6（4 threats）、Section 3 脚注（CSV artifacts） | **C** |
| 2 | 为每个叶子定义候选取值空间 | A.2 证据账本 → 每个 `[leaf-*]` 条目 | 按 §4 建议树中的候选取值，为每个叶子定义可执行取值空间。SWEBOK KA、ML 5 大类、DARE-4 评分维度等应有完整枚举。open coding 产生的 SE task 可取开放枚举，但标注"开放枚举；A2a 需收敛"。 | `paper_content.txt` Table 2/5/6；Section 3.6 编码说明 | **I** |
| 3 | 补充关系边 | A.2 新增 `[edge-*]` 条目 | 至少添加 3 条：`SWEBOK KA ↔ SE task`（属于映射）、`SWEBOK KA ↔ ML technique`（交叉引用）、`RQ 答案 → Implication`（支撑关系）。 | `paper_content.txt` Section 3.6（"a SE task may be associated with multiple KAs"）、Section 4.2（按 KA 展开时描述使用的 ML 技术）、Section 5（Implications 附 n 计数） | **I** |
| 4 | 标注每个叶子的统计用途和分母 | A.2 每个 `[leaf-*]` 条目 | 区分"可统计"（频次/分布/趋势）与"不可统计"（规范性建议/自由文本）。总分母为 83 篇纳入 review；per-table 分母为 Tables 3-6 各自的 sum。 | `paper_content.txt` Section 3.5-3.6（83/140 纳入、Tables 3-6 统计口径） | **I** |
| 5 | 补充质量评价维度 | A.2 新增 `[dim-quality-assessment]` 及子节点 | 原文 DARE-4 的 4 个 criterion + 总分 + inter-rater agreement 应作为独立维度分组，不能混入 generic "evidence" 叶子。 | `paper_content.txt` Table 2、Section 3.5 | **I** |
| 6 | 补充效度威胁维度 | A.2 新增 `[dim-validity]` 及子节点 | 原文 Section 6 的 4 类 validity threats 应作为独立维度。当前 `review.md` Section 2 的 validity_threat_pattern 标注为"本轮未完整定位"，但实际全文已在 `paper_content.txt` Pages 27-28 定位。 | `paper_content.txt` Pages 27-28（Section 6） | **I** |
| 7 | 补充 artifact / replication 维度 | A.2 新增 `[dim-artifacts]` 及子节点 | 原文有 7+ CSV 过程制品 + 6 个 table + 1 个 figure，这些是 tertiary study 方法透明性的核心，也是 Paper2 中"内容证据"的重要建模对象。 | `paper_content.txt` Section 3 脚注、Tables 1-6、Figure 1 | **I** |
| 8 | 补充编码方案维度 | A.2 `[dim-domain-classification]` 下 | 原文的 open coding → qualitative content analysis 流程是区别于简单分类的关键方法学特征。当前树完全没有建模。 | `paper_content.txt` Section 3.6（"we followed the open coding practice...Qualitative Content Analysis approach"） | **I** |
| 9 | A.2 证据锚定精确化 | A.2 每条 EV-* 条目 | 当前 4 条证据（EV-001 ~ EV-004）均为泛定位（"本文的 RQ / 方法 / 分类 / 评价 / 讨论结构"），应精确到：(1) Section 编号（如 Section 3.6, Section 4.2）；(2) 段落范围；(3) 表格/图编号（如 Table 2, Table 5, Table 6, Figure 1）。精确锚定后才能将证据强度从 `weak` 升级为 `medium` 或 `strong`。 | `paper_content.txt` 各 Section 标题与段落 | **I** |
| 10 | 区分 RQ 层 vs Implication 层 vs Threat 层 finding | A.3 结论-证据映射 | 当前只有一个通用 `[leaf-finding]`。应拆分为：(1) RQ-level distribution findings（可统计）；(2) Implication-level normative recommendations（不可统计但可计数支撑）；(3) Threat-level validity limitations（定性）。 | `paper_content.txt` Sections 4/5/6 | **C** |

## 6. C/I/M 结论

### 6.1 分类说明

| 等级 | 含义 |
|---|---|
| **C** | 直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性的问题。 |
| **I** | 会实质影响维度树可用性、原文 schema 复原、证据可审计性的问题。 |
| **M** | 不阻塞的清晰度或维护性建议。 |

### 6.2 逐项判定

| 严重度 | 数量 | 涉及修复项 |
|---|---|---|
| C | 3 | #1（主干用通用 6 叶替代原文 schema）、#2（叶子粒度不足，丢失原文关键维度）、#10（finding 路径混淆 RQ/Implication/Threat 三层） |
| I | 7 | #3（取值空间未定义）、#4（关系边缺失）、#5（统计用途/分母未标注）、#6（质量评价维度缺失）、#7（效度威胁维度缺失）、#8（artifact 维度缺失）、#9（编码方案维度缺失）、#11（A.2 证据锚定粒度过粗） |
| M | 0 | — |

### 6.3 C 级问题的学术影响分析

**C-1：主干用通用 6 叶替代原文 schema**。当前 `review.md` 的维度树主干（scope / corpus / taxonomy / method / evidence / finding）是 A1-M0--M6 元维度——它是对"所有 SLR/SMS paper 都应抽取什么"的通用接口定义，不是本文独有的 schema。如果把通用接口当作单篇论文的维度树，则 A2a 在汇总时：(a) 无法区分不同论文的不同 schema 结构；(b) 会丢失 cross-paper 维度比较的机会（例如 Kittchenham 2007 的 guideline 字段 vs Kotti 2023 的 extraction form 字段 vs 另一篇 SMS 的 classification scheme 之间的结构性差异）；(c) 会误导后续 A2b / A3 以为所有 tertiary study 共享同一套维度树，掩盖真实的维度多样性和 schema 演化需求。这直接违反 `paper_story.md` 中"模式演化"和"维度模式投影"的核心假设。

**C-2：叶子粒度不足**。当前树的 6 个通用叶子无法承载原文的真实结构化信息。例如原文的 DARE-4 四个独立 criteria 被压缩到一个 "evaluation-quality" 候选叶子中，丢失了每个 criterion 的评分空间和 inter-rater reliability；原文的 SWEBOK 15 KA + open coding SE task 双层分类被压缩到一个 "se-problem" 叶子中，无法区分体系分类（top-down）vs 涌现编码（bottom-up）。如果这种粒度进入 A2a，后续统计分析将无法执行有意义的交叉表（例如"高 DARE-4 QA3 得分的 review 是否倾向于覆盖更广泛的 SWEBOK KA"）。

**C-10：finding 路径混淆**。原文的 finding 是三层结构：RQ-level distribution → Implication-level recommendation → Threat-level limitation。当前 review.md 用一个 `[leaf-finding]` 覆盖全部三层，且所有结论均为 `weak` + `schema_seed`。这虽然在 A1-DT 降级纪律下合规，但意味着 A2a 将无法从当前树中区分"原文的哪些结论是统计驱动的、哪些是作者 normative 判断、哪些是方法学自我批评"。这对 Paper2 的核心主张——"区分统计分析、候选发现、最终领域发现"——构成方法论层面的自相矛盾风险。

### 6.4 最终建议

**NEEDS FIX**。当前 `review.md` 的维度树是一个以 A1-M0--M6 元维度为骨架的通用接口，而非原文 schema 的忠实复原。虽然 A.3 中通过 `weak` + `schema_seed` 降级纪律避免了强主张，但这种降级不应替代"把树建对"这个基本前提。

最小修复路径：
1. **立即**：用 §4 建议树中的 7 个 dim 分组 + 对应叶子替换当前 6+5 结构（修复项 #1）。
2. **同时**：为每个叶子定义候选取值空间（修复项 #2）、标注统计用途/分母（修复项 #4）、添加缺失的关系边（修复项 #3）。
3. **本轮或 A2a 前**：补充 DARE-4 质量评价、4 类 validity threats、CSV artifacts 等原文独立维度（修复项 #5-#8）。
4. **A2a 时**：将 A.2 证据从泛定位升级到精确 Section + Table/Figure 锚定，从而将证据强度从 `weak` 升级为 `medium` 或 `strong`（修复项 #9）。

修复后，6 个 A1-M 通用元维度应回归其本源位置——它们在 A1-M0--M6 总表（`SUMMARY.md` 覆盖矩阵）中定义，不应在单篇 review 中伪装成原文 schema。

---

*审计报告完成。撰写依据：`paper_content.txt` 全文 1774 行逐段阅读；`review.md` 全文 171 行；`pattern-field-schema.md` §8 字段合同；`paper_story.md` 维度模式演化要求；`ai-research-writing-skill` Reviewer mode 指南。*
