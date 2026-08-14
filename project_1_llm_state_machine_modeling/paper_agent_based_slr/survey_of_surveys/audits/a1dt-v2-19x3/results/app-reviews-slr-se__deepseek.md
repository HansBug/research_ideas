所有材料已阅读完毕。现在撰写完整审计报告。

---

# A1-DT v2 单篇全文审计报告：`app-reviews-slr-se`

**agent**: deepseek (本 codex 进程)
**审计日期**: 2026-06-30
**审计类型**: A1-DT v2 原生维度森林审计（独立进程，无 subagent）

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `app-reviews-slr-se` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是；已逐段阅读全部 2661 行（63 页文本提取），覆盖 Abstract 至 References 及 biographic notes |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；均已完整读取 |
| 是否打开或核对 `paper.pdf` | 是；通过 `pdfinfo` 核验元数据（63 页、作者 Dąbrowski、DOI 匹配）；未做逐页视觉级表图核对，当前证据等级为全文文本级 + PDF 元数据级 |
| 原文类型 | SLR（Systematic Literature Review） |
| 被编码样本单位 | primary studies（单篇研究论文），最终纳入 182 篇（2012--2020） |
| 样本数量 / 分母 | 182 篇 primary studies；初始检索 1656 篇→去重 303 篇→筛选 1353 篇→排除 1225 篇→手工增补 54 篇→最终 182 篇 |
| 原生树类型 | **维度森林**（dimension forest）：三套独立分类 schema（analysis type / mining technique / SE activity）+ 一套数据抽取字段表（F1--F18）+ 一套评价字段体系 + 一套讨论发现体系；schema 之间存在交叉表关系 |
| 主统计池资格 | **是**；具备完整系统检索 / 纳排 / 抽取 / 分类 / 统计 / discussion 闭环，可作为 survey_of_surveys 的 SLR 方法学统计池样本。但当前 A1-DT 阶段仅作 schema_seed，A2a 精核后方可进入定量统计 |
| 总体判定 | **pass**（具备可审计的维度森林结构，证据链完整，返修后可直接作为 A2a 精核入口） |

---

## 1. 原文证据阅读说明

### 1.1 实际读取文件清单

| 文件 | 读取方式 | 内容范围 |
|---|---|---|
| `bibtex.bib` | 全文读取 | 标题、作者、期刊、DOI、年份、摘要 |
| `metadata.json` | 全文读取 | 所有元数据字段，含 CCF 等级、publication_type、evidence_role 等 |
| `paper_content.txt` | 全文逐段读取（2661 行） | Abstract、§1 Introduction (p.2--3)、§2 Research Method (p.4--7)、§3 Results (p.8--43)：含 §3.1 RQ1 review analysis 类型 + Table 7、§3.2 各类型详解、§3.3 RQ2 mining techniques + Table 9、§3.4 RQ3 SE activities + Table 10--15、§3.5 RQ4 evaluation + Table 16--20、§3.6 RQ5 empirical results + Table 21--23、§4 Discussion (p.44--?)（文本中 discussion 片段存在但不完整）、§5 Related Work (含 comparison table)、§6 Threats to Validity、§7 Conclusion、References、Biographic notes |
| `paper.pdf` | `pdfinfo` 元数据核验 | 63 页、作者、DOI、标题均与 bibtex/metadata 一致 |
| `review.md` | 全文读取（349 行） | 完整现有 review，含快速卡片、维度树、A.1--A.4 附录 |

### 1.2 PDF 视觉核验说明

当前未做 PDF 逐页视觉级表图核对。以下位置仍需 PDF 视觉核验，但本审计基于 `paper_content.txt` 已可形成有效判断：

1. Table 3（F1--F18 抽取字段表）——文本提取中字段编号和名称可辨识，但完整表结构需视觉确认
2. Table 7（analysis type 频次表）——文本中已出现完整 9 行数据，可采信
3. Table 9（mining technique 统计）——文本中出现但抽取可能不完整
4. Table 10--13（SE activity 多级分类统计）——文本中出现大量子行数据，但部分行可能跨页错位
5. Table 14--15（交叉表）——文本中可辨识表头但数据可能不完整
6. Table 21（effectiveness result 汇总）——文本中出现完整保留，可采信
7. Figure 1（PRISMA 流程图）——文本中仅片段提及，需视觉核验
8. §3.2 各子节的论文引用列表——文本中提取为连续引用串，原文为表行

### 1.3 关键原文证据锚点（12 个）

| # | 锚点 | 原文章节/页 | 内容 |
|---|---|---|---|
| EV1 | 五 RQ 列表 | §2.1 / p.4--5 | RQ1--RQ5 完整列出：analysis type, technique, SE activity, evaluation, results |
| EV2 | PRISMA 数量链 | §2.2 / p.5--6 | 1656→1353→182 的筛选链路 |
| EV3 | Table 3 F1--F18 | §2.3 / p.7 | 完整 18 字段数据抽取表 |
| EV4 | 三套 classification schema | §2.4 / p.8 | content analysis 构建过程，inter-rater ~80--87%，intra-rater ~90--100% |
| EV5 | Table 7 analysis type | §3.1 / p.12 | 9 类分析类型及论文数/百分比 |
| EV6 | Table 9 mining technique | §3.3 / p.20--21 | NLP/ML/Statistical/Manual 四类及子类 |
| EV7 | Table 10--13 SE activities | §3.4 / p.22--27 | 四层活动分类 + "Not Specified"，每层有子类、论文数和百分比 |
| EV8 | Table 14--15 交叉表 | §3.4 / p.28 | analysis type × SE activity 和 multi-technique 组合统计 |
| EV9 | Table 16--20 evaluation | §3.5 / p.29--38 | dataset、tool、user study、evaluation criteria、participants |
| EV10 | Table 21 effectiveness | §3.6 / p.39--40 | 按 analysis type 分组的 precision/recall/accuracy range 和 median |
| EV11 | §4 Discussion 实践启示 | §4 / p.44--? | practical implications、research gaps、future work 列表 |
| EV12 | Table 23 related surveys | §5 / p.? | 与 5 篇相关 survey 的比较表 |

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象

**对象是 primary studies**——即针对 app review analysis 发表的研究论文。每篇 primary study 被编码到三套分类 schema 中，并按 F1--F18 字段逐项抽取数据。

原文明确限定：必须与软件工程相关、peer-reviewed、并使用 app reviews 支持至少一种软件工程活动。排除非英文、非 SE、secondary/tertiary studies、technical reports、manuals 等。

### 2.2 系统检索/纳排/数据抽取/编码方案

**有**。完整 Kitchenham 风格 SLR 流程：

1. **检索**（§2.2）：六大数据源（ACM DL, IEEE Xplore, Scopus, Web of Science, ScienceDirect, DBLP）+ 手工逐卷检索 + backward/forward snowballing
2. **纳排**（§2.2）：基于标题/摘要/全文三阶段筛选，有 inclusion/exclusion criteria
3. **数据抽取**（§2.3）：F1--F18 结构化字段表（Table 3）
4. **编码方案**（§2.4）：三套 classification schema 通过 content analysis 构建，先 open coding 再合并相似类别，最后作者讨论定稿

### 2.3 原文字段来源

| 来源类型 | 具体路径 |
|---|---|
| 数据抽取表 | Table 3：F1--F18（书目、分析类型、技术、SE 活动、评价目标/过程/指标/结果、标注数据/任务/者/质量、复现包） |
| 分类 schema | §2.4：三套独立 taxonomy（app review analysis type / mining technique / SE activity），每套有构建过程、示例、inter-rater reliability |
| 评价 rubric | §3.5：evaluation objective/procedure/metrics/criteria/result + 标注质量 + replication package 状态 |
| 统计表 | Table 7, 9, 10--13（频次/百分比）、Table 14--15（交叉表）、Table 21（effectiveness range/median） |
| Discussion finding | §4：practical implications / research gaps / future work 列表 |

### 2.4 RQ 与样本单位的关系

RQ 是**分类组织框架**，而不是独立的维度树。五 RQ 分别对应：
- RQ1/RQ2/RQ3：对每篇 primary study 赋予 analysis type / mining technique / SE activity 分类值
- RQ4：对每篇 primary study 抽取评价方法字段
- RQ5：汇总评价结果

**关系类型**：RQ → 分类 schema → 字段赋值 → 统计汇总 → 讨论发现。RQ 层是树根之上的第一个分叉，决定字段的选择和统计口径。

### 2.5 降级说明

不适用降级。本文有完整系统样本库和编码方案，不需要降级处理。

---

## 3. 原生样本编码维度树 / 维度森林

### 3.1 总览

本文是典型的**维度森林**（dimension forest）结构——不是单一树，而是多棵相互关联的树：

- **Tree A**：样本单位树（检索→筛选→纳入→编码）
- **Tree B**：分类维度森林（三套独立 schema：analysis type / mining technique / SE activity）
- **Tree C**：评价与复现资产维（evaluation fields + replication package）
- **Tree D**：统计结果与发现维（effectiveness summary + discussion finding）

A2a 精核任务：将下表中标 `[A2a]` 的叶子补全精确页码、表号/图号、封闭取值空间和缺失值策略。

### 3.2 Tree A：样本单位树（检索与纳排链）

```
[dim-app-reviews-slr-se-root] 182 primary studies (2012--2020)
├── [dim-a-retrieval] 检索层
│   ├── [leaf-a-acm] ACM Digital Library
│   ├── [leaf-a-ieee] IEEE Xplore
│   ├── [leaf-a-scopus] Scopus
│   ├── [leaf-a-wos] Web of Science
│   ├── [leaf-a-sciencedirect] ScienceDirect
│   ├── [leaf-a-dblp] DBLP
│   ├── [leaf-a-manual] 手工逐卷检索 (14 篇增补)
│   └── [leaf-a-snowball] backward/forward snowballing (40 篇增补)
├── [dim-a-screening] 筛选层
│   ├── [leaf-a-initial] 初始检索: 1656 篇
│   ├── [leaf-a-dedup] 去重后: 1353 篇
│   ├── [leaf-a-excluded] 排除: 1225 篇
│   └── [leaf-a-final] 最终纳入: 182 篇
└── [dim-a-time] 时间范围: 2012--2020
```

- 叶子 `leaf-a-initial` 取值空间：数值（分母级）。
- 叶子 `leaf-a-excluded` 取值空间：需原文筛除理由枚举 [A2a]。

### 3.3 Tree B：分类维度森林（三棵独立分类树）

#### B1：App Review Analysis Type 分类树 [dim-b1-analysis-type]

```
[dim-b1-analysis-type] App Review Analysis Type (非互斥，一篇可属多类)
├── [leaf-b1-ie] Information Extraction
├── [leaf-b1-clf] Classification
│   ├── [leaf-b1-clf-request] User Request Type Classification
│   ├── [leaf-b1-clf-nfr] NFR Type Classification
│   ├── [leaf-b1-clf-issue] Issue Type Classification
│   └── [leaf-b1-clf-req] Requirements Classification
├── [leaf-b1-clu] Clustering
├── [leaf-b1-sir] Search and Information Retrieval
├── [leaf-b1-sa] Sentiment Analysis
├── [leaf-b1-ca] Content Analysis
├── [leaf-b1-rec] Recommendation
├── [leaf-b1-sum] Summarization
└── [leaf-b1-vis] Visualization
```

- 取值空间类型：**层级枚举**（9 个顶层类 + Classification 下的 4 个子类）。
- 取值方式：多值（非互斥），每篇 primary study 可属多类。
- 统计分母：182 篇（每类统计为该类论文数 / 182 × 100%）。
- 原文证据：Table 7（§3.1，p.12）给出 9 类的论文数和百分比；子类在 §3.2.2 及各子节中详细定义。

#### B2：Mining Technique 分类树 [dim-b2-mining-technique]

```
[dim-b2-mining-technique] Mining Technique (层级枚举)
├── [leaf-b2-nlp] Natural Language Processing
│   ├── Tokenization, POS tagging, Parsing, Stemming/Lemmatization
│   └── N-gram analysis, Keyword matching
├── [leaf-b2-ml] Machine Learning
│   ├── Supervised: SVM, Naive Bayes, Decision Trees, Random Forest, Maximum Entropy
│   ├── Unsupervised: LDA, K-means, Apriori algorithm, DBSCAN
│   └── Deep Learning: CNN, LSTM, Word2Vec, BERT
├── [leaf-b2-stat] Statistical Analysis
│   └── Correlation analysis, Regression, Descriptive statistics, Hypothesis testing
└── [leaf-b2-manual] Manual Analysis
    └── Open coding, Thematic analysis, Grounded theory
```

- 取值空间类型：**层级枚举**（4 大类 + 每类下有具体技术子类）。
- 取值方式：多值（一篇可用多种技术）。
- 原文证据：Table 9（§3.3，p.20--21）+ §3.3 文字描述。
- [A2a] 需要核对 Table 9 的完整子类枚举和每类论文数/百分比。

#### B3：Software Engineering Activity 分类树 [dim-b3-se-activity]

```
[dim-b3-se-activity] Software Engineering Activity (层级枚举，含 "Not Specified")
├── [leaf-b3-req] Requirements (74 studies, 41%)
│   ├── [leaf-b3-req-elicitation] Requirements Elicitation (44 studies, 24%)
│   ├── [leaf-b3-req-classification] Requirements Classification (10 studies, 5%)
│   ├── [leaf-b3-req-prioritization] Requirements Prioritization (19 studies, 10%)
│   └── [leaf-b3-req-specification] Requirements Specification (6 studies, 3%)
├── [leaf-b3-design] Design (8 studies, 4%)
│   ├── [leaf-b3-design-rationale] Design Rationale Capture (5 studies, 3%)
│   └── [leaf-b3-design-ui] User Interface Design (3 studies, 2%)
├── [leaf-b3-testing] Testing (28 studies, 15%)
│   ├── [leaf-b3-testing-validation] Validation by Users (20 studies, 11%)
│   ├── [leaf-b3-testing-doc] Test Documentation (3 studies, 2%)
│   ├── [leaf-b3-testing-design] Test Design (4 studies, 2%)
│   └── [leaf-b3-testing-prioritization] Test Prioritization (3 studies, 2%)
├── [leaf-b3-maintenance] Maintenance (66 studies, 36%)
│   ├── [leaf-b3-maint-analysis] Problem and Modification Analysis (46 studies, 25%)
│   ├── [leaf-b3-maint-prioritization] Requested Modification Prioritization (18 studies, 10%)
│   ├── [leaf-b3-maint-helpdesk] Help Desk (7 studies, 4%)
│   └── [leaf-b3-maint-impact] Impact Analysis (5 studies, 3%)
└── [leaf-b3-not-specified] Not Specified (62 studies, 34%)
```

- 取值空间类型：**层级枚举**（4 个顶层 SE 活动类 + "Not Specified"）。
- 取值方式：多值（一篇可映射到多个活动）。
- 注意：百分比之和 > 100%，因为一篇 primary study 可同时支持多个 SE 活动。
- 原文证据：Table 10--13（§3.4，p.22--27）。

### 3.4 Tree C：评价与复现资产维 [dim-c-evaluation-artifact]

```
[dim-c-evaluation-artifact] 评价与复现资产维
├── [dim-c-extraction] 数据抽取字段 (F1--F18)
│   ├── [leaf-c-f1-f3] Bibliographic: title, authors, year, venue
│   ├── [leaf-c-f4] Analysis type(s)
│   ├── [leaf-c-f5] Mining technique(s)
│   ├── [leaf-c-f6] SE activity/activities
│   ├── [leaf-c-f7] Justification for app reviews
│   ├── [leaf-c-f8] Evaluation objective [A2a]
│   ├── [leaf-c-f9] Evaluation procedure [A2a]
│   ├── [leaf-c-f10] Metrics/criteria [A2a]
│   ├── [leaf-c-f11] Evaluation result [A2a]
│   ├── [leaf-c-f12] Annotated dataset [A2a]
│   ├── [leaf-c-f13] Annotation task [A2a]
│   ├── [leaf-c-f14] Annotators (number and type) [A2a]
│   ├── [leaf-c-f15] Quality measure [A2a]
│   ├── [leaf-c-f16] Replication package [A2a]
│   ├── [leaf-c-f17] Key findings [A2a]
│   └── [leaf-c-f18] Limitations [A2a]
├── [dim-c-dataset] Dataset 信息 (Table 16)
│   ├── [leaf-c-ds-apps] Number of apps covered
│   ├── [leaf-c-ds-reviews] Number of reviews
│   ├── [leaf-c-ds-source] App store source (Google Play, Apple Store, etc.)
│   └── [leaf-c-ds-period] Collection period
├── [dim-c-tool] Tool 信息 (Table 17)
│   ├── [leaf-c-tool-name] Tool name
│   ├── [leaf-c-tool-public] Public availability (yes/no)
│   └── [leaf-c-tool-ref] Reference
├── [dim-c-user-study] User Study 信息 (Table 18--20)
│   ├── [leaf-c-us-n] Number of participants (range: 1--85, median: 9)
│   ├── [leaf-c-us-sector] Participant sector (Academia/Industry)
│   ├── [leaf-c-us-role] Participant role (Student, Researcher, Developer, etc.)
│   ├── [leaf-c-us-criteria] Evaluation criteria (Usefulness, Accuracy, Usability, Efficiency, Informativeness)
│   └── [leaf-c-us-procedure] Evaluation procedure type
└── [dim-c-replication] Replication Package 状态
    ├── Replication package available (yes/no/partial)
    └── Public dataset (yes/no/partial)
```

- 取值空间类型：混合。F1--F3 为自由文本，F4--F6 为分类枚举（关联 B1/B2/B3），F8--F18 为混合（含枚举 + 自由文本 + 布尔）。
- Evaluation criteria 为封闭枚举：Usefulness、Accuracy、Usability、Efficiency、Informativeness（5 类）。
- Participant sector 为二值枚举：Academia / Industry。
- [A2a] 标记表示需核对原文 Table 3 及 §3.5 完整字段定义。

### 3.5 Tree D：统计结果与发现维 [dim-d-finding]

```
[dim-d-finding] 统计结果与发现维
├── [dim-d-effectiveness] Effectiveness 汇总 (Table 21)
│   ├── [leaf-d-eff-ie-features] IE Features: median precision 58%, recall 62%
│   ├── [leaf-d-eff-ie-requests] IE User Requests: median precision 91%, recall 89%
│   ├── [leaf-d-eff-clf-request] Classification Request Type: median precision 80%, recall 82%
│   ├── [leaf-d-eff-clf-nfr] Classification NFR: median precision 74%, recall 79%
│   ├── [leaf-d-eff-clf-issue] Classification Issue: median precision 76%, recall 79%
│   ├── [leaf-d-eff-clu] Clustering: median accuracy 83%, MojoFM 80%
│   ├── [leaf-d-eff-sir-feature] SIR Feature-Specific: median precision 70%, recall 56%
│   ├── [leaf-d-eff-sir-links] SIR Review-Artifact Links: precision 77--85%, recall 71--75%
│   ├── [leaf-d-eff-sa] Sentiment Analysis: median precision 71%, recall 67%
│   ├── [leaf-d-eff-rec] Recommendation: median accuracy 78%
│   └── [leaf-d-eff-sum] Summarization: recall 71%
├── [dim-d-discussion] Discussion 发现 (candidate findings)
│   ├── [leaf-d-disc-practice] Practical implications (4 条)
│   ├── [leaf-d-disc-gap] Research gaps
│   └── [leaf-d-disc-future] Future work directions
└── [dim-d-threats] Threats to validity
    ├── Internal validity
    ├── External validity
    └── Construct validity
```

- 取值空间类型：`leaf-d-eff-*` 为数值区间 + median；其他为自由文本加理由。
- 注意：作者明确声明因 heterogeneity 过大未做 meta-analysis，采用 "summarising effect estimates" 替代（Table 21 前说明）。
- Discussion 的 practical implications 基于具体统计表推导，不是无根基观点。

---

## 4. 叶子维度表

由于本文维度森林包含 50+ 叶子，下表列出核心代表性叶子（完整叶子及 A2a 精核入口见 §3 各树和 §8 A.2 草案）。每行只列一个叶子。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-b1-ie] | 信息抽取 | [dim-b1-analysis-type] | Table 7 row "Information Extraction"; §3.2.1 | 从 app reviews 中抽取 features、user requests、NFR 等结构化信息 | 56 studies (31%) | 层级枚举（顶层 9 类之一） | 未做 IE 的论文不归入此类；多值允许 | 频次/百分比统计 | 识别 SLR 分类 schema 的粒度设计模式 | EV5 | 分类结构可迁移；具体类别名不可迁移 |
| [leaf-b1-clf] | 分类 | [dim-b1-analysis-type] | Table 7 row "Classification"; §3.2.2 | 将 app reviews 归入预定义类别（user request type、NFR type、issue type 等） | 105 studies (58%)；子类：User Request Type / NFR Type / Issue Type / Requirements | 层级枚举（含 4 子类） | 未做分类的论文不归入 | 频次 + 子类分布 | 层级枚举 + 子类细分是 SLR schema 的高价值模式 | EV5 | schema 的层级设计模式可迁移 |
| [leaf-b2-ml] | 机器学习技术 | [dim-b2-mining-technique] | Table 9; §3.3 | 使用 ML 方法分析 app reviews，含 Supervised/Unsupervised/Deep Learning | Supervised (SVM, NB, DT, RF, ME), Unsupervised (LDA, K-means, Apriori, DBSCAN), Deep Learning (CNN, LSTM, Word2Vec, BERT) | 层级枚举（3 子类 + 每子类下技术名枚举） | 未使用 ML 论文不归入 | 技术分布统计 + 与 analysis type 交叉表 | 技术分类 + 交叉表模式可直接迁移到 LLM4STM 的分类 schema 设计 | EV6 | 技术名不可迁移；层级结构 + 交叉表设计可迁移 |
| [leaf-b3-req] | 需求工程活动 | [dim-b3-se-activity] | Table 10; §3.4.1 | SE 活动中的需求工程类，含 Elicitation/Classification/Prioritization/Specification | Elicitation (44, 24%), Classification (10, 5%), Prioritization (19, 10%), Specification (6, 3%) | 层级枚举（4 子类） | 不涉及 SE 活动的论文写 "Not Specified"（另有 62 篇） | 活动分布统计 | SE 活动分类的层级粒度可作为 Paper2 维度设计参考 | EV7 | 活动名不可迁移；层级设计可迁移 |
| [leaf-c-f16] | 复现实验包 | [dim-c-extraction] | Table 3 F16; §3.5 | 论文是否提供 replication package（代码/数据/工具） | 有/无/部分 | 布尔（允许 partial） | 未提及即视为无 | artifact 可用率统计 | Paper2 应把 replication package 作为一等抽取字段 | EV3 | 字段设计直接可迁移 |
| [leaf-c-us-criteria] | 用户评价准则 | [dim-c-user-study] | Table 19; §3.5 | 评价 app review analysis 工具/方法的准则 | Usefulness, Accuracy, Usability, Efficiency, Informativeness | 完整枚举（5 个值） | 未做 user study 时 N/A | 评价准则分布 | 封闭枚举的评价准则可作为 Paper2 agent evaluation 维度的分类参考 | EV9 | 准则名不可迁移；封闭枚举设计 + 映射表模式可迁移 |
| [leaf-d-eff-clf-request] | 分类-请求类型效果 | [dim-d-effectiveness] | Table 21 row "Classification / User Request Type" | Classification 方法在 User Request Type 分类上的 precision/recall | Precision: range 35%--94%, median 80%; Recall: range 51%--99%, median 82% | 数值区间 + median | 未报告 evaluation 的论文不出现在此统计 | 效果区间 + median summary | "summarising effect estimates" 方法是 heterogeneity 大时的替代统计方法 | EV10 | 方法学可迁移；具体数值不可迁移 |
| [leaf-d-disc-practice] | 实践启示 | [dim-d-discussion] | §4 Discussion | 从统计结果提炼的对实践者的建议 | 4 条实践启示（自由文本） | 自由文本加理由 | N/A（discussion 层） | 不能进入统计 | 候选 finding，需研究者裁决 | EV11 | discussion → finding 推导链可迁移；具体结论不可迁移 |

---

## 5. 关系边表

本文存在明确的**关系边**——三类 schema 之间的交叉表和统计关联。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| [edge-b1-b2] | [dim-b1-analysis-type] | 交叉统计 | [dim-b2-mining-technique] | 每对 (analysis type, technique) 的论文数 | 无法交叉的论文不出现在该 cell | Table 14 (§3.4) | 分析类型与技术选择的关联模式 |
| [edge-b1-b3] | [dim-b1-analysis-type] | 交叉统计 | [dim-b3-se-activity] | 每对 (analysis type, SE activity) 的论文数 | 同上 | Table 14 (§3.4) | 分析类型与工程活动的关联 |
| [edge-b1-b1] | [dim-b1-analysis-type] | multi-technique 组合 | [dim-b1-analysis-type] | 多种 analysis type 的组合频次 | 单类型论文不进入组合统计 | Table 15 (§3.4) | 揭示 common technique pipelines |
| [edge-c-d] | [dim-c-evaluation-artifact] | 汇总到 effectiveness | [dim-d-effectiveness] | 评价字段（F8--F11）→ Table 21 的效果值 | 未做 evaluation 的论文不参与汇总 | EV3→EV10 | 字段→统计→finding 的三层链路 |
| [edge-d-stat-finding] | [dim-d-effectiveness] | 支撑 candidate finding | [dim-d-discussion] | 实践启示和研究缺口（自由文本） | 无统计支撑的 discussion 应降级 | EV10→EV11 | 从统计表到 discussion finding 的可审计推导 |
| [edge-b3-not-specified] | [dim-b3-se-activity] | 缺失值指示 | [leaf-b3-not-specified] | 62 studies (34%) 未明确 SE activity | 未报告 activity 时归入此值 | EV7 (Table 13) | 警示 SE activity 分类覆盖不足 |

**不存在显式关系边的节点**：
- `[dim-a-retrieval]` 与各分类 schema 之间无关系边（检索层是前置筛选，不与编码字段交叉）。
- `[dim-d-threats]` 与 effectiveness 值之间无定量关系（效度威胁是定性讨论，不改变统计值）。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文中由字段/统计表支持的统计观察

| # | 统计观察 | 来源表/节 | 支撑字段 |
|---|---|---|---|
| SO1 | Classification 是最常见的 analysis type（58%），其次是 IE（31%）和 Content Analysis（30%） | Table 7 | F4 |
| SO2 | ML-based 技术使用最广（NLP 和 ML 合计占主导） | Table 9 | F5 |
| SO3 | Requirements (41%) 和 Maintenance (36%) 是最受关注的 SE 活动 | Table 10, 13 | F6 |
| SO4 | 34% 的 primary studies 未明确 SE activity | Table 13 | F6 |
| SO5 | Feature extraction 效果最低（median precision 58%）；User Request extraction 效果最高（median precision 91%） | Table 21 | F10, F11 |
| SO6 | Classification 技术的中位 precision/recall 约 75--83% | Table 21 | F10, F11 |
| SO7 | User study 参与者中位数仅 9 人，且以学生和研究者为主 | Table 18, 20 | F9, F14 |
| SO8 | 已有公开 replication package 和 dataset 的论文有限 | §3.5 | F16 |

### 6.2 原文 discussion / recommendation 提出的候选 finding

| # | 候选 finding | 原文 § | 是否可迁移到 Paper2 |
|---|---|---|---|
| CF1 | App review analysis 的 industrial adoption 有限，多数评价停留在学术环境 | §4 | 启发 Paper2 讨论 LLM4STM 的 industrial readiness 和 evaluation ecological validity |
| CF2 | Feature extraction 仍是难题（precision 中位仅 58%），需要更好的 NLP 方法 | §4 | 与 LLM4STM 的 state machine element extraction 精度问题平行 |
| CF3 | 评价指标和数据集缺乏标准化，阻碍方法可比性 | §4 | 直接对应 Paper2 的 standardized benchmark / evaluation protocol 需求 |
| CF4 | 缺少对 analysis result 如何被 SE practitioners 实际使用的 empirical study | §4 | 对应 Paper2 的 "formally-verified model usefulness" 的 downstream validation |

### 6.3 对 Paper2 可迁移的方法学启发

| # | 启发 | 迁移方式 |
|---|---|---|
| M1 | 多套独立 schema + 交叉表的 SLR 组织方式 | Paper2 的维度树设计应允许多棵独立分类树，然后用交叉表揭示 schema 间关系 |
| M2 | 抽取字段应包含 evaluation 和 artifact 列 | Paper2 的 primary study 编码表至少应有：method、task、evaluation、dataset、replication |
| M3 | classification schema 需报告 reliability | Paper2 的 agent-assisted 编码应有 inter-agent agreement 和 human adjudication 记录 |
| M4 | heterogeneity 大时用 "summarising effect estimates" 替代 meta-analysis | Paper2 的跨论文统计不强行追求统一 effect size |
| M5 | discussion finding 要有具体表/统计支撑 | Paper2 的每个 final finding 必须标注统计来源表和字段 |

### 6.4 绝不能迁移的领域结论

- app review mining 的细分 taxonomy（如 "User Request Type Classification"、"NFR" 等）不可迁移到 LLM4STM。
- "App Store / Google Play / Apple Store" 相关 discussion 不可迁移。
- 具体 precision/recall 数值（如 "Classification median precision 80%"）不可迁移。

---

## 7. 对现有 `review.md` 的返修建议

### 7.1 C 级（Critical：必须修复，否则阻塞进入主统计池）

| # | 问题 | 当前状态 | 建议修复 |
|---|---|---|---|
| C1 | **维度树复原节已有 "原文 schema 主树" 但缺少完整的原生森林层级** | 现有 "原文 schema 主树" 表只列出了主干标识（如 `[dim-app-reviews-slr-se-orig-analysis-type]`），但没有把每个主干的叶子展开到原生取值空间级别。例如 `[dim-app-reviews-slr-se-orig-se-activity]` 只写了 "需求、维护、测试、设计、发布规划、用户反馈管理等活动" 而未列出其完整的三级层级。 | 从本审计 §3.3 的三棵分类树中提取完整叶子枚举，补入 review.md。尤其是 SE activity 的四层结构（Requirements→Elicitation/Classification/Prioritization/Specification）必须在 review 中显式列出。 |
| C2 | **样本单位 "182" 与 "分母是否闭合" 未在维度树中显式处理** | review.md 中提到 182 篇但未在维度树中作为根节点的分母注释。 | 将 `[dim-app-reviews-slr-se-root]` 的叶子层补上 `样本数量：182；分母类型：闭合（已完成检索引纳排全流程）`。 |
| C3 | **"Not Specified (62 studies, 34%)" 的缺失值语义未进入维度树** | review.md 提到了 SE activity 分类但未单独列出 "Not Specified" 叶子及其含义。 | 在 B3 树下新增 `[leaf-b3-not-specified]` 叶子，标注其取值为 62 studies (34%)，语义为 "论文未明确声明其支持的软件工程活动"，这本身是一个有意义的统计发现。 |

### 7.2 I 级（Important：影响统计精度或可审计性）

| # | 问题 | 当前状态 | 建议修复 |
|---|---|---|---|
| I1 | **A.2 证据账本中缺少 Table 3 (F1--F18) 的逐字段证据锚点** | A.2 现有证据行大多指向 RQ-level 或整节，缺少逐字段级别的精细锚定。 | 按本审计 §4 的叶子维度表，为每个叶子补一条 A.2 行，标注来源节、表号、页码和取值空间。 |
| I2 | **关系边表只列了 2 条边，缺少关键的交叉表关系** | 现有 `edge-app-reviews-slr-se-method-evidence` 和 `edge-app-reviews-slr-se-taxonomy-finding` 是正确的但覆盖面窄。 | 补充至少 4 条新边：`[edge-b1-b2]`（analysis type × technique）、`[edge-b1-b3]`（analysis type × SE activity）、`[edge-b1-b1]`（multi-technique combination）、`[edge-c-d]`（evaluation → effectiveness）。见本审计 §5。 |
| I3 | **原文 "summarising effect estimates" 方法未进入 review 的方法学注释** | review 提到了 heterogeneity 但未记录作者选择的 alternative synthesis method。 | 在统计观察区域增加一条注释："因 heterogeneity 过大未做 meta-analysis，采用 Cochrane 的 'summarising effect estimates' 方法（Table 21 前说明）"。 |
| I4 | **三棵分类树的 reliability 值已有原文数据但未记入 review 维度树** | review 提到 "87%/87%/80% inter-rater" 但在维度树叶子层未显式标注。 | 为每棵分类树添加 `[leaf-*-reliability]` 叶子，记录 inter-rater 和 intra-rater agreement。 |

### 7.3 M 级（Minor：改进但非阻塞）

| # | 问题 | 建议修复 |
|---|---|---|
| M1 | "通用接口投影" 表仍保留了六个通用 leaf 标识 | 可以考虑将此表移到附录或折叠为一行注释，突出 "原文 schema 主树" 为事实源。当前写法中两表并列可能让下游 reader 混淆。 |
| M2 | "历史草稿" 节中的旧 text tree 与 "原文 schema 主树" 存在信息冗余 | 旧 tree 中的 `corpus_and_screening`、`extraction_fields` 等节点可以在 "原文 schema 主树" 中保留对应行，但旧 text tree 可以标记为 `<!-- collapsed: migrated to §维度树复原 -->`。 |
| M3 | SUMMARY 表中的 "样本单位/样本数量/原生树类型/统计池资格" | 当前 review.md 未看到 SUMMARY 总表（可能在 survey_of_surveys/SUMMARY.md 中）。如果存在，应确保该表记录 `样本单位=primary study, 样本数量=182, 原生树类型=维度森林, 统计池资格=是（A2a 精核后）`。 |

---

## 8. 审计附录草案：证据账本与结论映射

### 8.1 注意事项

- 以下草案可直接迁入 `review.md` 的 A.2/A.3 节。
- 表头使用中文，字段名沿用 review.md 的原生标识体系。
- 所有行当前强度为 `文本级（text-level）`，PDF 视觉核验后可按实际结果升级为 `交叉核验级（cross-verified）` 或降级。

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-app-reviews-slr-se-001 | paper_content.txt | §2.1, p.4--5 | "RQ1: What types of app review analysis...", "RQ2: What mining techniques...", "RQ3: What SE activities...", "RQ4: How are approaches empirically evaluated...", "RQ5: How well..." | 五 RQ 是维度森林的第一层分叉——定义了 analysis type / technique / SE activity / evaluation / results 五维度 | schema_root_definition | text-level | [dim-b1-analysis-type], [dim-b2-mining-technique], [dim-b3-se-activity], [dim-c-evaluation-artifact], [dim-d-effectiveness] | 否（文本清晰） | RQ 结构可迁移；具体问题内容不可迁移 |
| EV-app-reviews-slr-se-002 | paper_content.txt | §2.2, p.5--6 | "1,656 studies", "303 duplicates", "1,353 unique studies", "1,225 excluded", "14 additional papers from manual search", "40 additional papers from snowballing", "182 papers" | PRISMA 数量链完整可审计 | sample_size_definition | text-level | [dim-a-screening] | 是（Figure 1 PRISMA 图） | 分母来源可迁移；具体数值不可迁移 |
| EV-app-reviews-slr-se-003 | paper_content.txt | §2.3, p.7 | Table 3 提及 "F1 bibliographic info", "F4 review analysis type", "F5 mining technique", "F6 SE activity"... "F16 replication package" | F1--F18 是本文对每篇 primary study 的编码字段（叶子），取自 data extraction form | extraction_field_schema | text-level（Table 3 全文在文本中不完整） | [dim-c-extraction] 下所有 F1--F18 叶子 | 是（Table 3 完整布局） | 字段表结构可迁移；字段内容不可迁移 |
| EV-app-reviews-slr-se-004 | paper_content.txt | §2.4, p.8 | "three classification schemas", "content analysis", "open coding", "inter-rater agreement: 87% (app review analysis), 87% (SE task), 80% (mining technique)", "intra-rater: 93%, 100%, 90%" | 三套 schema 通过 content analysis 构建，有 reliability 检查 | classification_schema_construction | text-level | [dim-b1-analysis-type], [dim-b2-mining-technique], [dim-b3-se-activity] | 否（文本清晰） | schema 构建方法可迁移 |
| EV-app-reviews-slr-se-005 | paper_content.txt | §3.1, p.12 | Table 7 行 "Information Extraction 56 31%", "Classification 105 58%", "Clustering 44 24%"..."Visualization 20 11%" | 9 类 app review analysis 的频次和百分比（n=182） | leaf_value_space | text-level（Table 7 在文本中可辨识） | [leaf-b1-ie], [leaf-b1-clf], [leaf-b1-clu], [leaf-b1-sir], [leaf-b1-sa], [leaf-b1-ca], [leaf-b1-rec], [leaf-b1-sum], [leaf-b1-vis] | 是（Table 7 原表核对） | 只限本文 |
| EV-app-reviews-slr-se-006 | paper_content.txt | §3.4, p.22--27 | Table 10 row "Requirements Elicitation 44 24%", Table 11 row "Requirements Classification 10 5%"...Table 12 row "Validation by Users 20 11%"...Table 13 row "Not Specified 62 34%" | SE 活动四层分类 + Not Specified 的频次和百分比 | leaf_value_space | text-level（嵌套表格抽取可能有错位） | [dim-b3-se-activity] 下全部叶子 | 是（Table 10--13 多级表格核验） | 只限本文 |
| EV-app-reviews-slr-se-007 | paper_content.txt | §3.6, p.39--40 | Table 21 row "Information Extraction / Features: precision 21% to 84%, median 58%; recall 42% to 77%, median 62%" | 按 analysis type × mined information 分组的 effectiveness range/median | statistical_result | text-level（Table 21 在文本中保留较完整） | [dim-d-effectiveness] 下全部叶子 | 是（Table 21 完整行核验） | 只限本文 |
| EV-app-reviews-slr-se-008 | paper_content.txt | §3.5, p.38 | Table 19 "Assessment Criteria: Usefulness, Accuracy, Usability, Efficiency, Informativeness" | 5 类 evaluation criteria 为封闭枚举 | leaf_value_space | text-level | [leaf-c-us-criteria] | 是（Table 19 完整布局） | 准则名不可迁移；枚举设计可迁移 |
| EV-app-reviews-slr-se-009 | paper_content.txt | §3.5, p.38--39 | "number of participants ranges from 1 to 85 with the median of 9" | user study 规模偏小 | statistical_observation | text-level | [leaf-c-us-n] | 否（文本清晰） | 只限本文 |
| EV-app-reviews-slr-se-010 | paper_content.txt | §3.4, p.28 | Table 14 "How often a type of app review analysis are used to realise a SE activity", Table 15 "How often certain combination of app review analyses are used" | classification schema 之间存在交叉表关系 | relation_edge_definition | text-level（交叉表在文本中可能不完整） | [edge-b1-b2], [edge-b1-b3], [edge-b1-b1] | 是（Table 14, 15 原表核验） | 交叉表设计可迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| A1DT-app-reviews-slr-se-C01 | 本文的维度树主类型为"RQ 驱动维度森林"（三套独立分类 schema + 一套抽取字段表 + 一套评价字段体系），非单树 | tree_type_classification | [dim-app-reviews-slr-se-root] | EV-app-reviews-slr-se-001, EV-app-reviews-slr-se-003, EV-app-reviews-slr-se-004 | text-level（强） | schema_seed 分类；维度森林类型标注 | 需 A2a 确认三套 schema 独立性（原文§2.4 已说明独立构建） |
| A1DT-app-reviews-slr-se-C02 | 样本单位为 primary studies，样本量 182（2012--2020），分母闭合 | sample_unit_and_size | [dim-a-screening] | EV-app-reviews-slr-se-002 | text-level（强） | 主统计池资格判定；分母归一化 | PDF 视觉核验 Figure 1 PRISMA 后升级证据强度 |
| A1DT-app-reviews-slr-se-C03 | 本文是 A1 中字段体系最完整的现代 SLR 样本之一，适合迁移"多套分类 schema + evaluation 字段 + replication package 字段 + discussion finding"设计 | migration_value | [dim-app-reviews-slr-se-root] | EV-app-reviews-slr-se-003, EV-app-reviews-slr-se-004, EV-app-reviews-slr-se-007, EV-app-reviews-slr-se-008 | text-level（中） | Paper2 维度树设计参考；SLR 方法学模式迁移 | 领域 taxonomy 不可迁移；只迁移字段结构和 schema 设计模式 |
| A1DT-app-reviews-slr-se-C04 | Classification schema 需要 reliability 证据（inter-rater ~80--87%），Paper2 的 agent-assisted 编码同样需要 | methodology_requirement | [dim-b1-analysis-type], [dim-b2-mining-technique], [dim-b3-se-activity] | EV-app-reviews-slr-se-004 | text-level（强） | Paper2 编码协议设计参考 | 本文的 reliability 值不能替代 Paper2 自己的 agreement 测量 |
| A1DT-app-reviews-slr-se-C05 | 34% primary studies 未明确 SE activity（"Not Specified"），说明分类 schema 覆盖存在系统性缺失 | classification_gap | [leaf-b3-not-specified] | EV-app-reviews-slr-se-006 | text-level（强） | candidate finding；Paper2 的 schema 设计应预留给 "Unknown/Not Reported" 类别 | 单篇统计观察；跨论文后才能升级为 final finding |
| A1DT-app-reviews-slr-se-C06 | Feature extraction 是 app review analysis 中效果最低的子任务（median precision 58%），Sentiment Analysis 次低（median precision 71%） | statistical_observation | [leaf-d-eff-ie-features], [leaf-d-eff-sa] | EV-app-reviews-slr-se-007 | text-level（强） | candidate finding；不可迁移到 Paper2 的具体领域结论 | 数值不可迁移；"效果分层"的组织方式可迁移 |
| A1DT-app-reviews-slr-se-C07 | 文章的评价维度包含五类 evaluation criteria（Usefulness/Accuracy/Usability/Efficiency/Informativeness）的封闭枚举 | leaf_value_space_definition | [leaf-c-us-criteria] | EV-app-reviews-slr-se-008 | text-level（强） | Paper2 evaluation criteria 分类的 schema seed | 准则内容不可迁移；封闭枚举设计可迁移 |
| A1DT-app-reviews-slr-se-C08 | 本文可迁移的是维度树结构、关系边设计、证据要求和降级纪律，不可迁移具体领域统计结论 | migration_boundary | [dim-app-reviews-slr-se-root] | 全部证据 | text-level（强） | 迁移边界标注 | complex tables 仍需 A2a 精核 |
| A1DT-app-reviews-slr-se-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决 | finding_boundary | [dim-d-discussion] | EV-app-reviews-slr-se-007, EV-app-reviews-slr-se-009 | text-level（中） | candidate finding 边界标注 | 单篇 discussion 不能升级为 final finding |

---

## 9. 技能使用与自我审查记录

### 9.1 已读取的技能文件

| 文件 | 读取结果 | 采用的原则 |
|---|---|---|
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md` | ✅ 完整读取 | Evidence gate（证据优先于叙事）；Claim gate（无证据不强宣称）；Reviewer gate（最终稿前解决高严重性 objection） |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md` | ✅ 完整读取 | 六维审稿框架（Originality/Quality/Clarity/Significance/Reproducibility/Ethics）；Constructive specificity standard；Review-ready section checks |
| `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md` | ✅ 完整读取 | Five-dimension review（Contribution/Writing/Experimental/Evaluation/Method soundness/Responsibility）；Claim audit；Rejection-risk audit |
| `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` | ✅ 完整读取 | Research plan 的结构化输出范式（论文结构 → section plans → figures/tables → task list → risks）可作为维度树设计的参考 |
| `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md` | ✅ 完整读取 | Paper2Code 四阶段 planning 可作为 paper generation pipeline 设计参考（但对本审计任务直接帮助有限） |
| `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md` | ✅ 完整读取 | Structured output schema 的设计模式（实验设计→baselines/datasets/metrics/hyperparameters/ablation/seeds）可迁移到 Paper2 的 primary study 抽取字段设计 |
| `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | ✅ 完整读取 | Completion artifact contract（artifact-gated completion）可类比到本审计的 evidence-gated delivery；但与本审计直接操作关系有限 |

### 9.2 本输出最高风险 3 点（reviewer 视角自我审查）

| # | 风险 | 严重性 | 主线程复核建议 |
|---|---|---|---|
| R1 | **Table 3 (F1--F18)、Table 10--13（SE activity 多级表）、Table 14--15（交叉表）的文本抽取可能不完整或错位** | 高 | 主线程 merge 前应做一次 PDF 视觉抽样核验（至少在 Table 7、Table 10、Table 21 中随机抽 3 行对比原表），确认 `paper_content.txt` 的各表行数与原文一致 |
| R2 | **本文 §4 Discussion 的完整内容在 `paper_content.txt` 中抽取不完整**（Discussion 在 p.44 之后但文本中片段很少） | 中 | 主线程应检查 `paper_content.txt` 的 Discussion 节是否有大幅缺失；若有缺失，考虑用 OCR 模式（`-m ocr`）重新抽取 §4 附近的页面，或直接检查 PDF 视觉页 |
| R3 | **本审计对取值空间的 "封闭/非封闭" 判定主要基于文本推断，未经过原文枚举项的 1:1 核对** | 中 | 主线程在 A2a 精核时应逐项验证：每棵分类树的叶子是否有原文明确定义的 complete set，还是作者暗示 "包括但不限于" |

### 9.3 任务状态

| 项 | 状态 |
|---|---|
| blocked | 否 |
| timeout | 否 |
| 文件缺失 | 无；所有必需文件均可读取 |
| 未使用 subagent | 是（严格遵守硬约束） |
| 未修改仓库文件 | 是 |
| 输出为自包含完整报告 | 是 |

---

**审计完成**。本报告可直接传递给主线程用于更新 `review.md` 的 §维度树复原、§A.2、§A.3 和 SUMMARY 表。建议主线程优先处理 3 个 C 级返修项（§7.1），然后按 A2a 精核清单（§3 各树中标记 `[A2a]` 的叶子）逐项进行 PDF 视觉核对。