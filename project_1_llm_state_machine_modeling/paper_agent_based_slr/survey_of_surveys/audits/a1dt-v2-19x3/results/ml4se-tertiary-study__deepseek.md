现在我已拥有足够信息。以下是完整的 A1-DT v2 单篇全文审计报告。

---

# A1-DT v2 单篇全文审计报告：`ml4se-tertiary-study`

---

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `ml4se-tertiary-study` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是。完整阅读 1774 行全文，覆盖 Introduction（pp.1-4）、Background（pp.4-6）、Method（pp.6-12）、Results（pp.12-24）、Discussion（pp.24-27）、Threats（pp.27-29）、Conclusion（pp.29-30）及全部参考文献 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是。`bibtex.bib` 含完整 CSUR 条目；`metadata.json` 含当前元数据快照 |
| 是否打开或核对 `paper.pdf` | 否。仅基于 `paper_content.txt` 文本提取；未做 PDF 版面视觉核验。Table 6 行内数值、Table 7 长列表、Fig.6 热力图颜色等仍需 PDF 视觉核对 |
| 原文类型 | tertiary study |
| 被编码样本单位 | 83 篇质量接受的 secondary studies（reviews/SLRs/systematic mappings/surveys） |
| 样本数量 / 分母 | 83 篇纳入（140 篇检索 → 质量筛选后 83 篇）；覆盖 6,117 篇 non-unique primary studies |
| 原生树类型 | 维度森林 |
| 主统计池资格 | 是。有系统检索、纳排、质量评估、数据抽取编码方案，且样本明确可审计 |
| 总体判定 | **needs repair** — 现有 `review.md` 的六叶通用接口严重偏离原文实际编码 schema，须按本文审计结果重写"维度树复原"。但原文自身是高质量 tertiary study，维度森林清晰，修复可行 |

---

## 1. 原文证据阅读说明

### 1.1 实际读取范围

- **文件**：`paper_content.txt`（全文 1774 行）
- **核心章节**：
  - §1 Introduction（pp.1-4）：ML4SE 背景与论文定位
  - §2 Background（pp.4-6）：EBSE / tertiary study 方法论先例
  - §3 Method（pp.6-12）：§3.1 RQs、§3.2 检索策略、§3.3 纳排标准、§3.4 筛选过程、§3.5 质量评估（DARE-4）、**§3.6 数据抽取与编码方案**
  - §4 Results（pp.12-24）：§4.1 数据抽取元统计、§4.2 RQ1（SE tasks/KA）、§4.3 RQ2（研究缺口与挑战）、§4.4 RQ3（ML 技术四轴分类）
  - §5 Discussion（pp.24-27）：7 条 Implication
  - §6 Threats to Validity（pp.27-29）：Ampatzoglou 分类
  - §7 Conclusion（pp.29-30）
- **关键表图**：Table 1（检索关键词）、Table 2（DARE-4 质量标准）、Tables 3-4（83 篇 study overview）、Table 5（SWEBOK KA × subarea）、**Table 6（ML 四轴分类）**、Table 7（ML 技术按应用任务分组）、Fig.6（ML×KA 分布热力图）

### 1.2 仍需 PDF 视觉核验项

以下证据锚点来自 `paper_content.txt` 的行内文本解析，但：
- Table 6 引用编号列表（如 `[1, 3, 6, 7, 30, ...]`）行内可能因文本提取有截断
- Table 7 的 ML 技术全枚举行内非常长，需 PDF 确认完整性
- Fig.6 的精确百分比值依赖文本提取精度

### 1.3 关键原文证据锚点（12 个）

1. **样本单位定义**：§4.1 — *"The papers in our final set of 83 quality-accepted secondary studies were published between 2009–2022, and cover 6,117 non-unique primary studies"*
2. **RQs 定义**：§3.1 — RQ1（SE tasks）、RQ2（less-covered KAs）、RQ3（ML techniques）
3. **数据抽取字段**：§3.6 开段 — 列出 9 类提取字段（title/source, year, venue, authors, study type, method, QA score, primary count, domain KA/subarea/SE tasks, implications, ML techniques）
4. **SWEBOK 分类**：§3.6 RQ1 段 — *"extracted from each secondary study its application domain in terms of related SWEBOK KA, subarea, and SE task(s)"*，每个 study 最多 3 个 SE tasks，通过 open coding + Qualitative Content Analysis 获得
5. **ML 四轴分类方案**：§3.6 RQ3 段 — 来源：Harman [65] 的 AI in SE 角色 + Kaur and Jindal [77] 的 supervision/incrementality/generalizability
6. **四轴枚举**：Axis 1（3 类）— Computational search, Fuzzy/probabilistic, Classification/learning/prediction；Axis 2（4 类）— Supervised, Unsupervised, Semi-supervised, Reinforcement；Axis 3（2 类）— Batch/offline, Online/incremental；Axis 4（2 类）— Model-based, Instance-based
7. **质量评估方案**：§3.5 — DARE-4 四问（QA1-QA4），每问 0-1 分，总分 0-4
8. **纳排标准**：§3.3 — IC/EC 明确列出（inclusion 含"systematic methods with defined RQs, search process, data extraction"；exclusion 含"non-secondary studies, informal surveys"等）
9. **RQ1 结果**：Table 5 — 11 个 SWEBOK KA，SW Quality 占 30%，SW Testing 占 20%
10. **RQ3 结果**：Table 6 — Classification/learning/prediction 65%，Supervised 78%，Batch/offline 99%，Model-based 87%
11. **Implications**：§5 — 7 条编号 Implication（Implication 1-7）
12. **ML 技术全枚举**：Table 7 — 8 个 ML application tasks（classification/regression, pattern discovery, dimensionality reduction, information retrieval, stochastic search, generation, hybrid, miscellaneous），每个下含数十种子技术

---

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**对象：83 篇 quality-accepted secondary studies**（SLR、systematic mapping study、survey、taxonomy）。每篇都是一个已发表的文献综述，被当作编码的基本单元。这是 tertiary study 的标准设计——"review of reviews"。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有，且极系统。** 检索策略包括：
- 自动检索（IEEE Xplore、ACM DL、Scopus，2015-2020，用三组关键词的 3-tuple 组合）
- 手动检索（随机一个 3-tuple 补检各库）
- 后向雪球（一轮，3,195 篇参考文献 → 纳入 16 篇 → 7 篇通过质量 → 二轮无新增）
- 前向雪球（一轮，Scopus 2,461 篇引用 → 纳入 84 篇 → 43 篇通过质量）

纳排标准（IC/EC）在 §3.3 有完整定义。质量评估使用 DARE-4 四问框架（Table 2），满分 4 分，≥2.0 纳入（§3.5）。数据抽取方案在 §3.6 有完整定义。

### 2.3 原文字段来自哪里？

字段来源是**多层次组合**：

| 层次 | 来源 | 用途 |
|---|---|---|
| **元数据抽取表** | §3.6 开头 9 字段 | 描述每个 secondary study 的基本特征 |
| **SWEBOK V3 KA/subarea** | 外部标准分类法 | RQ1 的预定义分类框架 |
| **SE tasks（open coding）** | 从 secondary study 标题/关键词/摘要/引言中手动编码 | RQ1 的自由文本→归类编码 |
| **ML 四轴分类方案** | 融合 Harman [65] + Kaur and Jindal [77] | RQ3 的预定义分类框架 |
| **ML 技术全枚举** | 从 secondary study 中手动提取 | RQ3 的细粒度计数 |
| **Implications for further research** | 从 secondary study 摘要/引言/结果/结论/未来方向中手动搜索提取 | RQ2 的自由文本提取 |
| **DARE-4 质量评分** | 外部质量评估框架 | 纳排门控 + 分布统计 |

### 2.4 RQ 与样本单位是什么关系？

**RQ 是字段用途说明，不是树根本身。** 树根是"83 篇 secondary study"。三个 RQ 分别驱动不同字段子树的编码：

- RQ1 → SWEBOK KA/subarea + SE task（open coding）
- RQ2 → implications for further research + issues/obstacles（文本提取）
- RQ3 → ML 四轴 + ML techniques 全枚举

RQ 是"为什么要编这些字段"，字段是"编了什么"。RQ 列表不直接等于维度树。

### 2.5 降级风险

**无需降级。** 本文有明确的系统样本库（83 篇）、系统检索策略、纳排标准、质量评估方案和编码 protocol。所有 replication package 文件均有命名（如 `knowledge_areas.csv`、`ml_techniques.csv`、`further_research.csv` 等），理论上可审计。

---

## 3. 原生样本编码维度树 / 维度森林

以下是该论文**自身**的维度森林（原文 schema）：

```
83 Secondary Studies (根)
│
├── [A] 元数据层 (§3.6 前 9 字段)
│   ├── title/source (自由文本)
│   ├── publication_year (数值, 2009–2022)
│   ├── publication_venue (层级枚举: journal/proceedings/book_chapter)
│   ├── author_names (自由文本, 274 unique authors)
│   ├── institutions (自由文本, 140 institutions)
│   ├── countries (自由文本)
│   ├── study_type (层级枚举: SLR | systematic_mapping | survey | taxonomy; 允许多值, e.g. SLR+meta-analysis)
│   ├── research_method (关系值: 引用 Kitchenham/Petersen/Hall/Wohlin 等标准指南)
│   ├── quality_score (数值区间, DARE-4: 0.0–4.0, step 0.5)
│   └── primary_study_count (数值, range 10–445, non-unique across studies)
│
├── [B] SWEBOK 分类层 (§3.6 RQ1)
│   ├── swebok_ka (层级枚举: SW Quality | SW Testing | SE Process | SE Management | SW Requirements | SW Maintenance | SW Design | SW Config Mgmt | SE Models & Methods | SE Professional Practice | Engineering Foundations)
│   │   └── swebok_subarea (层级枚举, 每 KA 2–4 个 subarea, 见 Table 5)
│   │       └── se_tasks (自由文本, via open coding, 1–3 tasks/study; 可跨 KA, e.g. "test automation", "defect prediction")
│
├── [C] ML 技术分类层 (§3.6 RQ3)
│   ├── role_of_ai_in_se (层级枚举 3: computational_search | fuzzy_probabilistic | classification_learning_prediction)
│   ├── supervision (层级枚举 4: supervised | unsupervised | semi_supervised | reinforcement)
│   ├── incrementality (层级枚举 2: batch_offline | online_incremental)
│   ├── generalizability (层级枚举 2: model_based | instance_based)
│   └── ml_techniques (层级枚举 8 大类 + 外部分类法引用: classification_clustering_regression | pattern_discovery | dimensionality_reduction | information_retrieval | stochastic_search | generation | hybrid | miscellaneous; 每大类下含子技术, e.g. Random Forest, SVM, LSTM, BERT, 见 Table 7)
│
├── [D] 研究缺口与挑战层 (§3.6 RQ2)
│   ├── further_research_implications (自由文本+理由, 按 KA 分组, §4.3 分 7 个子领域)
│   ├── general_recommendations (§4.3.1: 跨 KA 通用建议)
│   └── issues_obstacles (自由文本+理由, 从各 secondary study 中提取)
│
└── [E] 综合发现层 (Discussion §5)
    ├── implication (7 条编号 Implication, 显式合成)
    └── recommendation (按受众: for researchers | for practitioners)
```

**说明**：
- 该论文有 **5 个子树**，不是单树。这是 tertiary study 的标准特征——它同时对样本做元数据描述（A）、领域分类（B）、技术分类（C）、缺口提取（D）和跨样本综合发现（E）。
- 叶子大多来自原文，不是通用接口。
- **A2a 精核任务**：Table 6 的具体引用编号需要 PDF 核对完整性；Table 7 的长列表中技术名称（如 `hW-Inference`、`SArF`、`SysMar` 等特殊缩写）需要视觉确认；Fig.6 的精确百分比需要 PDF 核对。

---

## 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-study-type | 研究类型 | [A] 元数据层 | §3.6 "Study type (e.g., SLR, systematic mapping study, taxonomy)" | 每篇 secondary study 的方法类型 | SLR \| systematic_mapping \| survey \| taxonomy；允许多值（如 SLR+meta-analysis） | 层级枚举 | 原文明确分类；无缺失 | §4.1 分布统计：SLR 64%, mapping 19%, survey 16%, taxonomy 1 | 用于 Paper2 审查纳入研究的方法学基线 | §4.1 "53 (64%) are primarily SLRs...16 (19%) are systematic mapping studies" | 可迁移"研究类型"字段；不可迁移具体分布 |
| leaf-qa-score | 质量评分 | [A] 元数据层 | §3.5 DARE-4 framework; §3.6 "Quality assessment score" | DARE-4 四问评分，每问 0/0.5/1，总分 0–4 | [0.0, 4.0]，step 0.5 | 数值区间 | 未通过质量筛选（<2.0）的 57 篇被排除 | §4.1 Fig.4 年度平均分趋势 | 作为方法学可信度的 proxy 字段 | §3.5 "quality thresholds...0 (Very Poor), 0.5 (Poor), 1 (Fair)" | 质量评估框架可迁移为 gate 条件；不可迁移 DARE-4 具体四问 |
| leaf-primary-count | 覆盖初探数 | [A] 元数据层 | §3.6 "Number of primary studies" | 每篇 secondary 覆盖的 distinct primary studies 数量 | 数值区间 [10, 445] | 数值区间 | 部分 study 未列汇总表；从参考文献列表推断（§6 Data Validity） | §4.1 总分母 6,117 non-unique | 评估每篇综述的覆盖广度 | Tables 3-4 "Primary" 列 | 可迁移"覆盖初探数"为规模指标；不可迁移具体数值 |
| leaf-swebok-ka | SWEBOK 知识域 | [B] SWEBOK 分类层 | §3.6 "Application domain in terms of SWEBOK KAs and subareas"；Table 5 | 基于 SWEBOK V3 的 11 个知识域 | SW Quality (30%) \| SW Testing (20%) \| SE Process (18%) \| SE Management (14%) \| SW Requirements (6%) \| 其余 5 个 KA (1–2% each) | 层级枚举 | 每个 study 分配一个 most prominent KA；跨 KA 的次要关联不记录 | RQ1 覆盖率柱状图；Table 5 计数 | 识别 ML4SE 的 domain 热点和冷区 | §3.6 "the most prominent one was kept" | 可迁移"外部分类法引用"模式；SWEBOK 只适用于 SE 领域 |
| leaf-swebok-subarea | SWEBOK 子域 | [B] SWEBOK 分类层 | Table 5 中 "Subarea" 列 | 每个 KA 下的细分领域 | 例如 SW Quality 下：Practical Considerations (22 studies) / Quality Fundamentals (2) / Quality Management Processes (1) | 层级枚举 | 同 KA 级分配规则 | Table 5 子域计数 | 更细粒度的 sub-domain 热点识别 | Table 5 | 可迁移层级分类模式；不可迁移 SWEBOK 具体子域 |
| leaf-se-task | SE 任务 | [B] SWEBOK 分类层 | §3.6 "the SE tasks, we followed the open coding practice" | 通过 open coding + Qualitative Content Analysis 从每篇 study 提取的 SE 任务描述 | 自由文本；每 study 1–3 个 tasks；可跨 KA | 自由文本加理由 | 每个 study 必有 1 个最突出的 SE task | RQ1 定性描述（§4.2 按 KA 分述） | 跨 KA 的 SE task 模式发现 | §3.6 "Each secondary study was associated with at least one and up to three SE tasks" | 可迁移 open coding 方法论；不可迁移具体 SE task 词表 |
| leaf-role-of-ai | AI 在 SE 中的角色 | [C] ML 技术分类层 | §3.6 "The role of AI in SE [65]" | Harman 的三类 AI 角色分类 | computational_search (14%) \| fuzzy_probabilistic (20%) \| classification_learning_prediction (65%) | 层级枚举 | 每 study 分配一个 most prominent 类别 | Table 6 统计；Fig.6 分布 | KA×AI-role 交叉分布分析 | §4.4 "the majority of studies (n=54; 65%) were classified in Classification, learning and prediction" | 可迁移"外部分类法引用 + 多轴交叉"模式 |
| leaf-supervision | 监督类型 | [C] ML 技术分类层 | §3.6 "the supervision type [77]" | Kaur and Jindal 的监督类型分类 | supervised (78%) \| unsupervised (13%) \| semi_supervised (6%) \| reinforcement (2%) | 层级枚举 | 同"most prominent"规则 | Table 6 | ML 方法学偏好分析 | §4.4 "most studies (n=65; 78%) adopt supervised learning" | 可迁移为 ML 论文的方法学编码轴 |
| leaf-incrementality | 增量性 | [C] ML 技术分类层 | §3.6 "the incrementality type [77]" | 在线/离线学习分类 | batch_offline (99%) \| online_incremental (1%) | 层级枚举 | 同 | Table 6；驱动 Implication 6 | 识别方法学断层 | §4.4 "almost all studies perform batch/offline learning" | 可迁移为方法学成熟度指标 |
| leaf-generalizability | 泛化类型 | [C] ML 技术分类层 | §3.6 "the generalizability type [77]" | 基于实例 vs 基于模型的学习 | model_based (87%) \| instance_based (13%) | 层级枚举 | 同 | Table 6 | 方法学模式分析 | §4.4 "majority of studies (n=72; 87%) perform model-based learning" | 可迁移 |
| leaf-ml-technique | ML 技术 | [C] ML 技术分类层 | §3.6 "we extracted by hand the ML techniques employed in the primary studies"；Table 7 | 从 secondary study 中手动提取的具体 ML 算法/工具名 | 8 大类（classification/clustering/regression, pattern discovery, dimensionality reduction, information retrieval, stochastic search, generation, hybrid, miscellaneous）下 100+ 种子技术 | 层级枚举 + 外部分类法引用 | 仅当 secondary study 报告了 primary study 所用技术时才记录 | RQ3 §4.4 结尾 — "Classifying...results in no insight—the same algorithms appear to be used in all SE tasks" | 技术流行度统计；与 SE tasks 交叉分析 | Table 7 全枚举 | 可迁移"技术全枚举"模式；不可迁移具体技术名 |
| leaf-implication | 研究启示 | [D] 研究缺口层 | §3.6 "Implications for further research"；§5 的 7 条 Implication | 从各 secondary study 中提取，并在 Discussion 中合成为跨 KA 启示 | 自由文本；§5 中显式编号为 Implication 1–7 | 自由文本加理由 | 并非每篇 study 都包含明确 implication | §5 的 7 条跨 KA 综合 | 作为 Paper2 candidate finding 的启发来源 | §5 "Implication 1. Further empirical validation studies..." | 可迁移"统计→启示"的 evidence chain 模式；不可迁移具体启示内容 |
| leaf-issue-obstacle | 障碍与问题 | [D] 研究缺口层 | §3.6 "any identified issues or obstacles associated with the use of ML techniques in SE" | ML4SE 面临的数据/方法/实践障碍 | 自由文本；按 KA 分组 | 自由文本加理由 | 同 implication 的提取规则 | §4.3 各 KA 段内的 issues/obstacles | 识别系统性瓶颈 | §5 "lack of empirical work...comparative analyses...industrial trials" | 可迁移为 Paper2 的"障碍清单"模式 |

---

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel-ka-task | swebok_ka | one-to-many（一个 KA 下多个 SE tasks） | se_tasks | 自由文本 | open coding 保证全覆盖，无缺失 | §3.6 "a SE task may be associated with multiple KAs" | 将 KA 结构映射到具体 SE 活动 |
| rel-study-ml-axes | study | one-to-one（每 study 在四轴上各有一个值） | role_of_ai_in_se, supervision, incrementality, generalizability | 层级枚举各轴 | 每 study 在每轴上分配一个 most prominent 类别 | §3.6 "studies were classified to the most prominent category" | 构建四轴交叉分类表（Table 6） |
| rel-ka-ml-cross | swebok_ka × ml_axes | many-to-many（每个 KA 与 ML 技术有分布关系） | 四轴交叉百分比 | 百分比（每 KA 内各轴值和为 100%） | Fig.6 覆盖全部 11 个 KA | Fig.6 热力图 | KA×ML 交叉可视化，支持 Implication 7 |
| rel-implication-source | implication | derived-from（跨样本综合） | secondary study implications（原始） | 自由文本 | N/A — 是上层合成产物 | §5 每 Implication 附带引用编号 | 从 83 篇原始发现到 7 条综合启示的证据链 |

**说明**：该论文没有使用关系型数据库 schema（如主键/外键/join），但如上所示，存在明确的逻辑关系边。DWAR-SWEBOK KA 与 SE task（open coding）是多对多关系，ML 四轴与 KA 之间通过 Fig.6 热力图表达分布关系，Implication 与原始 secondary study 之间通过引用编号回链。

---

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 统计观察（由字段 / 统计表直接支持）

| 统计观察 | 证据 | 领域相关性 |
|---|---|---|
| SW Quality 和 SW Testing 是最常被 ML 覆盖的 SE 域（30% + 20%） | Table 5 | 不可直接迁移到形式化验证/状态机（本仓库的关注点不同） |
| 65% 的 study 使用 classification/learning/prediction，99% 使用 batch/offline | Table 6 | 方法学偏好信息——对理解 ML-based 方法的主流范式有参考价值 |
| 87% 使用 model-based learning | Table 6 | 同上 |
| 所有 SE 任务中使用的 ML 算法高度重叠 | §4.4 "Classifying...results in no insight" | 这一"no insight"发现对 Paper2 有方法论启示：按 ML 技术分类可能无区分度，应优先按 SE 任务或验证目标分类 |
| 人类中心 KAs（SE Professional Practice, SW Requirements）覆盖不足 | §5, 以及 Table 5 中 1 study each | 提示"人类主观性"在自动化方法中的挑战——对 LLM-based 方法有类比意义 |

### 6.2 候选 finding（从 Discussion 提取的方法学启示）

以下从 §5 的 7 条 Implication 中筛选与 Paper2（状态机建模与验证）相关的方法学候选：

| 候选 finding | 来源 Implication | 对 Paper2 的潜在启发 |
|---|---|---|
| 工业数据/真实案例对 ML 方法的可信度至关重要 | Implication 1, 5 | Paper2 的状态机建模方法应考虑工业控制系统真实案例的可用性 |
| 基础 SE 概念如有缺陷（如 smell definition 不一致），下游 ML 模型不可靠 | Implication 2 | 类比：如果状态机建模的基础语义（如时序约束、状态转移规则）定义不清，LLM 生成/验证也受影响 |
| 数据管线的文档化和自动化有助于模型可信度 | Implication 4 | Paper2 的 pipeline 应包括数据/指令/反馈的文档化记录 |
| 在线/增量学习是 underrepresented 但有前景的方向 | Implication 6 | 类比：状态机的增量修复/迭代式验证可能是类似机会 |
| 跨域方法融合（hybrid ML + search-based + probabilistic）有正面信号 | Implication 7 | Paper2 的 LLM + 形式化方法融合正是这种跨域范式 |

### 6.3 对 Paper2 可迁移的方法学启发

1. **"no insight" 发现的方法论意义**：本文发现按 ML 技术分类无法区分 SE 任务——同样的算法用在不同任务上。这暗示 Paper2 在构建分类体系时，不应简单按 LLM 型号或 prompt 技术分类，而应按 **验证目标/状态机结构特征**分类。
2. **SWEBOK 充当外部分类法**的模式：Paper2 可以借鉴——将生成-验证-修复三阶段映射到已有的控制系统软件工程标准（如 IEC 61131-3, IEC 61499）。
3. **Implication 合成方法**：从 83 篇 review 的独立 finding 合成为 7 条 Implication 的方法，对 Paper2 的跨论文 synthesis 有直接参考。
4. **DARE-4 质量评估范式**：可以用类似思路评估 SLR/survey 的方法学质量，作为 Paper2 文献纳入的质量 gate。

### 6.4 绝不能迁移的领域结论

- 所有关于 SWEBOK KA 分布的具体百分比
- 所有关于 ML technique popularity 的具体排名
- ML4SE 领域的研究缺口内容（如 smell detection、effort estimation 等）
- 工业数据共享的具体建议

---

## 7. 对现有 `review.md` 的返修建议

### C 级（Critical — 阻塞性）

| 编号 | 问题 | 证据 | 建议 |
|---|---|---|---|
| C-1 | **六叶通用接口冒充原文维度树**。现有 review.md 的 §5 中，维度树被写作 `[leaf-ml4se-tertiary-study-orig-se-problem]`、`[leaf-ml4se-tertiary-study-orig-ml-technique]` 等 5 个叶子 + `scope/corpus/taxonomy/method/evidence/finding` 六个通用接口。这是 A1-M0--M6 跨论文投影，不是该论文自身的编码 schema。 | 原文 §3.6 有明确的 5 层维度森林（见本报告 §3） | **必须重写**。将 §5 的维度树替换为本文 §3 的原生维度森林。保留六叶接口仅作为跨论文投影的元注释（标注为 "meta-projection"，不入统计池）。 |
| C-2 | **SUMMARY 表中 `样本单位 / 样本数量 / 原生树类型 / 统计池资格` 字段与原文不一致**。现有 review.md 未明确声明样本单位为"83 篇 secondary studies"、样本数量为 "83/6,117"。 | 本报告 §0 和 §2 | 修正为：样本单位 = "83 篇质量接受的 secondary studies"，样本数量 = "83（覆盖 6,117 non-unique primary studies）"，原生树类型 = "维度森林（5 子树：元数据/SWEBOK/ML四轴/研究缺口/综合发现）"，统计池资格 = "是" |

### I 级（Important — 影响准确性和完整性）

| 编号 | 问题 | 证据 | 建议 |
|---|---|---|---|
| I-1 | **缺少 Table 6 和 Table 7 的提取**。现有 review.md 未记录 ML 四轴分类方案和 ML 技术全枚举。 | §3.6 RQ3 段，Table 6，Table 7 | 在 A.2 证据账本中新增 ML 四轴和 ML 技术全枚举的证据条目 |
| I-2 | **Implication 体系未被纳入维度树**。现有 review.md 把 challenge/action 作为 finding pattern 的子类型处理，但没有把它当作独立的"研究缺口与综合发现"子树。 | §5 的 7 条 Implication + §4.3 的 7 个子领域 + §4.3.1 的 general recommendations | 在维度树中新增 [D] 研究缺口与挑战层和 [E] 综合发现层 |
| I-3 | **A.2 证据账本中证据标识偏弱**。目前 A.2 的证据均为 `EV-ml4se-tertiary-study-002` 之类笼统编号，没有映射到原文章节/段落/表图编号。 | 本报告 §1.3 的 12 个锚点 | 将 A.2 中的证据标识替换为原文章节锚点（如 `§3.6 ¶RQ3`、`Table 6` 等），提高可审计性 |
| I-4 | **A.3 结论-证据映射缺少原文具体结论**。目前 A.3 的结论均为抽象 schema_seed 结论（如"可作为 Paper2 维度树候选节点"），未记录原文自身的 finding。 | §4.2-4.4 的 RQ 结果，§5 的 7 条 Implication | 新增原文 finding 作为 A.3 的结论条目（标注为 `原文统计/讨论结论`，在 `允许用途` 列限为 `仅作方法学启发`） |

### M 级（Minor — 改进性建议）

| 编号 | 问题 | 证据 | 建议 |
|---|---|---|---|
| M-1 | **"字段树较大，A2a 需细分"**表述不够精确。应明确哪些叶子需要 A2a 精核，哪些已可从文本提取中确认。 | 本报告 §4 叶子表中 `取值空间类型` 列 | 将"字段树较大"替换为"维度森林含 5 子树、~16 叶子节点，其中 Table 6 引用编号、Table 7 技术名和 Fig.6 百分比需 PDF 视觉核验" |
| M-2 | **缺少对"no insight"发现的记录**。本文最有趣的方法学发现之一——ML 技术分类对 SE 任务无区分度——未被记录。 | §4.4 "Classifying the manually extracted ML techniques...results in no insight" | 在 A.3 中新增结论条目："ML 技术分类对 SE 任务无区分度（原文 negative result——方法论启示：Paper2 应按验证目标而非技术栈分类）" |
| M-3 | **CSUR 期刊的综述结构 pattern 可更精确**。现有 review.md 说"具体章节待 A2a 深读"，但本文已完成全文阅读。 | 本报告 §1.1 的章节清单 | 更新为真实的章节结构和表图编号 |

### 附加检查：PR body / GUIDE 规则问题

本审计任务要求的维树口径（不套六叶通用接口、恢复原文 schema）本身是正确的。现有 `review.md` 的问题不来自 GUIDE 规则缺陷，而来自**执行偏差**——reviewer 未按 GUIDE 要求"像这篇论文自己的编码表/分类框架"来恢复。无 GUIDE 层面的 C/I 建议。

---

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-001 | paper_content.txt | §3.6 ¶1-4 | 9 类数据抽取字段列表 | "The information extracted from each quality-accepted secondary study was the following. •Title and source...•Publication year...•Publication venue...•Author names...•Study type...•Research method...•Quality assessment score...•Number of primary studies...•Application domain in terms of SWEBOK KAs and subareas...•Implications for further research...•Employed ML techniques" | 元数据层字段来源 | strong | [A] 元数据层全部叶子 | 否 | 字段枚举仅适用于 tertiary study；对 primary study SLR 需调整 |
| EV-002 | paper_content.txt | §3.3 | IC/EC 完整列表 | "Inclusion Criteria. •Only secondary studies...conducted with documented systematic methods... •Taxonomies with the following planning characteristics... •Publications reporting results on the use of ML techniques in SE activities..." | 纳排标准与样本边界 | strong | 样本单位定义 | 否 | IC/EC 仅适用 ML4SE tertiary；Paper2 需定制 |
| EV-003 | paper_content.txt | §3.5 | DARE-4 四问 Table 2 | "QA1: Are the review's inclusion/exclusion criteria described and appropriate?...QA3: Is the included literature assessed for quality?" + "quality thresholds...0 (Very Poor), 0.5 (Poor), 1 (Fair)" | 质量评估方案 | strong | leaf-qa-score | 否 | DARE-4 只适用于 SLR 质量评估 |
| EV-004 | paper_content.txt | §3.6 ¶RQ1 | open coding 方法描述 | "we followed the open coding practice [39] by manually applying codes (i.e., SE tasks—e.g., test automation, software maintainability prediction)...Next, the authors discussed and grouped together conceptually-related codes...employing the Qualitative Content Analysis approach [97]" | SE task 字段的编码方法 | strong | leaf-se-task | 否 | open coding 方法可迁移；编码结果不可迁移 |
| EV-005 | paper_content.txt | §3.6 ¶RQ3 | ML 四轴方案来源 | "The classification scheme was constructed from two sources and consists of four axes: the role of AI in SE [65], the supervision type [77], the incrementality type [77], and the generalizability type [77]" | ML 分类框架来源 | strong | leaf-role-of-ai, leaf-supervision, leaf-incrementality, leaf-generalizability | 否 | 四轴框架是 ML4SE 领域的；Paper2 可借鉴"外部标准融合"模式 |
| EV-006 | paper_content.txt | Table 6 | ML 四轴统计表（行内文本） | "Computational search and optimisation techniques 12 14 [1,3,6,7,...]...Classification, learning and prediction 54 65 [4,5,8,...]" | RQ3 量… | medium | leaf-role-of-ai, leaf-supervision, leaf-incrementality, leaf-generalizability | 是 — 引用编号列表可能因行内截断不完整 | 统计分布不可迁移 |
| EV-007 | paper_content.txt | Table 7 | ML 技术全枚举 | "Classification, Clustering, Regression: Artificial Neural Network (Back Propagation, Multi-Layer Perceptron,...)...Stochastic Search: Ant Colony Optimization..." | ML 技术细粒度枚举 | medium | leaf-ml-technique | 是 — 技术名长列表需 PDF 确认完整性 | 技术名仅作词汇参考 |
| EV-008 | paper_content.txt | Table 5 | SWEBOK KA × Subarea 统计表 | "Software (SW) Quality Practical Considerations 22 27% [refs] 1309...SW Testing Test Techniques 15 18% [refs] 1255" | RQ1 定量结果 | strong | leaf-swebok-ka, leaf-swebok-subarea | 否 | KA 分布不可迁移 |
| EV-009 | paper_content.txt | §4.3.1 | General Recommendations | "Various recommendations apply to all KAs. These include: conducting more comparative analyses...reexamining the industrial relevance...documenting data collection...experimenting with different validation techniques..." | 跨 KA 通用建议 | strong | leaf-implication | 否 | 建议内容不可迁移；"建议提取→合成"的方法可迁移 |
| EV-010 | paper_content.txt | §5 | 7 条 Implication | "Implication 1. Further empirical validation studies...Implication 2. The academic research community could consider taking a step back to address its fundamental SE literature shortcomings...Implication 7. Hybrid ML techniques..." | 综合发现 | strong | leaf-implication | 否 | Implication 内容不可迁移；"统计→Implication"的 evidence chain 结构可迁移 |
| EV-011 | paper_content.txt | §4.4 ¶末尾 | "no insight" negative result | "Classifying the manually extracted ML techniques (Section 3.6) according to the SE tasks outlined in Section 4.2 results in no insight—the same algorithms appear to be used in all SE tasks." | 负结果发现 | strong | leaf-ml-technique | 否 | 方法论启示可迁移：技术分类可能无区分度 |
| EV-012 | paper_content.txt | §6 | Threats to Validity | "We use the classification scheme proposed by Ampatzoglou et al. [12]...Another data validity threat arises from one of the composing axes of the ML classification scheme (Table 6)." | 局限性声明 | strong | 整体 schema 可信度 | 否 | 威胁分类框架可迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-001 | 该论文使用 5 层维度森林对 83 篇 secondary studies 进行编码：元数据层、SWEBOK 分类层、ML 四轴分类层、研究缺口层、综合发现层 | 维度树复原 | [dim-ml4se-tertiary-study-root] 及全部子节点 | EV-001, EV-004, EV-005, EV-006, EV-007, EV-008, EV-009, EV-010 | strong | 作为 A1-DT 单篇维度树基准；驱动 Paper2 维度树设计的方法论参考 | 该维度森林是 tertiary study 的专用结构，Paper2 不能照搬 SWEBOK/ML 四轴 |
| CONC-002 | 样本单位为 83 篇 quality-accepted secondary studies，覆盖 6,117 non-unique primary studies（2009-2022） | 样本范围 | 样本单位定义 | EV-001, EV-002, EV-003 | strong | 主统计池资格确认；分母参考 | 样本是 ML4SE 综述，不包含形式化方法/状态机内容 |
| CONC-003 | SW Quality（30%）和 SW Testing（20%）是最常被 ML 覆盖的 SE 知识域；人类中心 KA 覆盖不足 | 原文统计结论 | leaf-swebok-ka, leaf-swebok-subarea | EV-008 | strong | 仅作方法学模式观察 | 不可迁移到非 SE 领域；Paper2 的关注领域完全不同 |
| CONC-004 | 99% 的 study 使用 batch/offline learning；online/incremental learning 极度 underrepresented | 原文统计结论 | leaf-incrementality | EV-006 | strong | 引出 Implication 6；对 Paper2 有"增量式"方法的方法论启发 | 统计本身不可迁移 |
| CONC-005 | ML 技术按 SE tasks 分类 "results in no insight" — 同样算法用在不同 SE 任务上 | 原文负结果发现 | leaf-ml-technique | EV-011 | strong | 对 Paper2 有重要方法论启示：分类体系应按"任务目标"而非"技术栈"组织 | 该发现限于 ML4SE 域 |
| CONC-006 | 7 条 Implication 是从 83 篇原始 finding 中跨样本合成的综合发现 | 原文综合发现 | leaf-implication | EV-009, EV-010 | strong | 作为 Paper2 "统计观察→综合发现"合成方法论的模式参考 | Implication 具体内容不可迁移 |
| CONC-007 | 现有 review.md 的六叶通用接口严重偏离原文 schema | 审计发现（返修依据） | review.md §5, A.1-A.4 | EV-001 至 EV-012 全部 | strong | 驱动 review.md 重写 | N/A — 这是对现有工作的诊断 |

---

## 9. 技能使用与自我审查记录

### 9.1 技能文件读取记录

| 技能文件 | 读取状态 | 采用原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 完整读取 | §Core Mandate（claim-evidence-engineering）— 本次审计以此为最高原则：所有结论必须映射到原文证据锚点 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 完整读取 | §Universal Review Dimensions（Originality/Quality/Clarity/Significance/Reproducibility/Ethics）— 用于校准审计的 rigorousness 标准；§Constructive Specificity Standard — 每个 C/I 建议必须附带具体章节/字段/行引用 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 完整读取 | §Claim Audit — 每个结论必须有证据+风险+修订状态；§Five-Dimension Review — 用于评估现有 review.md 的维度完整度 |
| `research-planning/SKILL.md` | 完整读取 | §Step 2 的 4 阶段规划方法 — 提示维度树设计应先有整体 schema 再有叶子枚举；本次审计按此顺序组织 §3-§4 |
| `research-planning/references/planning-prompts.md` | 完整读取 | §Paper2Code 四轮对话方法 — 提示实现前应先做全面规划；对审计无直接约束但确认了 plan-first 原则 |
| `research-planning/references/output-schemas.md` | 完整读取 | §Complete Research Plan Schema JSON — 确认研究规划输出的结构标准；审计报告的 JSON 类比映射到此 schema |
| `autoresearch/SKILL.md` | 完整读取 | §Core contract 的 "completion is artifact-gated" — 本次审计产出自包含 Markdown 报告，符合 artifact-gate 原则 |

### 9.2 最高风险自审（reviewer 视角）

| 风险 | 描述 | 复核方法 |
|---|---|---|
| **Risk 1: PDF 未核验** | Table 6 的引用编号列表（每行 50+ 个 `[n]`）可能因 `paper_content.txt` 行内文本提取而截断或缺失；Table 7 的 100+ 技术名可能有 OCR/提取错误；Fig.6 的精确百分比需 PDF 确认。 | 主线程合并前必须人工打开 `paper.pdf`，逐项核对 Table 6/7 和 Fig.6 的行数与 `paper_content.txt` 行内版本的一致性 |
| **Risk 2: 维度森林粒度过细** | 本文恢复了 ~16 叶子节点和 5 子树，远超现有 review.md 的 5 叶子接口。如果 Paper2 只需要高层方法论模式，此粒度可能 overfit。 | 主线程合并时明确：本次审计产出的完整维度森林是**该论文的事实真源**；Paper2 仅从中提取可迁移的方法论片段，不要求全量迁移 |
| **Risk 3: 现有 review.md 状态不清** | 现有 review.md 的 §5 中 `19×3 全文审计表明...本轮已补原文主干和 A2a 精核入口` 声称已存在一轮修复，但其维度树仍是六叶接口 + 5 个 `orig-*` 候选叶子。这暗示可能已有另一份 A1-DT 产物与本审计竞争。 | 主线程合并时检查是否有冲突的 A1-DT 产物（如 `dimension_tree_v2.md`），优先以本文的全量阅读结果为准；若冲突，按原文证据裁决 |

### 9.3 任务执行状态

- **blocked**: 无。所有必需文件均可读取。
- **timeout**: 无。
- **文件缺失**: 无。所有 7 个技能/指南文件和 5 个论文文件均已成功读取。
- **PDF 版面核验**: 未执行。标记为 `needs_manual_check`。

---

*审计完成时间：2026-06-30。本报告为自包含完整审计，不依赖任何外部消息或中间输出。*