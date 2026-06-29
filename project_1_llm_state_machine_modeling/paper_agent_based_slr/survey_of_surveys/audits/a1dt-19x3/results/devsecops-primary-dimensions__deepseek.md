# devsecops-primary-dimensions · deepseek 全文审计报告

## 1. 审计身份与输入

- **reviewer 身份**：deepseek
- **是否读取 `$ai-research-writing-skill`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
  - `references/paper-story.md`
  - `references/reviewer-guidelines.md`
  - `references/reviewer-self-review.md`
- **是否读取 `$research-planning`**：是。读取路径：
  - `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
  - `references/planning-prompts.md`
- **是否读取 `$oh-my-codex:autoresearch`**：是。读取路径：
  - `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`
- **是否完整阅读 `paper_content.txt`**：是。全文 3158 行，分三段（1--1000、1001--2000、2001--3158）完整阅读，覆盖摘要、引言、RQ1/RQ2、方法（双轨 MLR / 质量评价 / snowballing / Thematic Analysis）、Table 5 TA 合成结果、定义/挑战/实践/工具/度量五方面的 Table 6--20 编码表、CPTM 模型 Table 21（Gartner 生命周期映射）、GSE 分析（4.2 节及 Table 3--4）、confirmatory search（4.3 节）、implications（4.4）、validity threats（5 节）、conclusion、references。
- **是否核对 `paper.pdf`**：否。未打开 `paper.pdf` 进行图形/表格的版面级视觉核对。审计结论依赖 `paper_content.txt` 文本级证据，涉及 Fig. 5--9、Table 5--21 细节处记为 "图表待人工核对"。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

论文设定两个显式研究问题：

| RQ | 原文内容 |
|---|---|
| RQ1 | What is the current state of DevSecOps in the existing white and grey literature, including which aspects are involved, what are the themes for each aspect, and how these aspects/themes are linked to each other? |
| RQ2 | How is DevSecOps applied in Global Software Engineering (GSE) contexts? |

**贡献声明**（来自 1 Introduction 末尾 + 4.4 Implications + 6 Conclusion）：
1. 提供 DevSecOps 第一个十年（2012--2021）的系统现状全貌，覆盖 white（104 篇）+ grey（43 篇）双轨文献。
2. 识别 DevSecOps 五大方面（Definitions、Challenges、Practices、Tools/Technologies、Metrics/Measurement）及每个方面的 themes。
3. 通过 Thematic Analysis 将挑战、实践、工具、度量整合为 Challenge-Practice-Tool-Metric（CPTM）模型，并映射到 Gartner 十阶段生命周期。
4. 揭示 DevSecOps 在 GSE 场景中的研究空白——现有 white + grey 文献几乎未覆盖 Global DevSecOps。
5. 开放科学材料（Zenodo）通过 JSS Open Science Board 验证。

### 2.2 原文方法流程

论文使用 **Multi-vocal Literature Review (MLR)**，执行双轨策略：

```
Search String 1 (DevSecOps general) ──→ White literature (WL) ──→ Quality Assessment ──→
Search String 2 (GSE + DevSecOps) ──→ Grey literature (GL) ──→ Snowballing       ──→
                                                                                        │
                                           ┌────────────────────────────────────────────┘
                                           ▼
                                    Thematic Analysis (Braun & Clarke)
                                    text → code → theme → category
                                           │
                                           ▼
                                    五大方面 + 四类范畴 (OPC / PC / Technology / Business)
                                           │
                                           ▼
                                    CPTM 模型 + Gartner 生命周期映射
                                           │
                                           ▼
                                    Confirmatory Search (2022+, 不入 TA/CPTM)
```

关键方法步骤的原文定位：

| 步骤 | 原文位置 | 关键参数 |
|---|---|---|
| 主检索 | §3.1--3.2 | 双轨搜索字符串：Search String 1 侧重 DevSecOps 全局，Search String 2 加入 GSE/global/distributed 词簇；时间范围 2012--2021 |
| 纳排 | §3.3 | 纳入/排除标准表格化，含 peer-reviewed、灰色文献来源、语言限制 |
| 质量评价 | §3.4 | 对 WL 做 narrative quality evaluation（非 scoring 除名），GL 按权威性/出版者分类 |
| Snowballing | §3.5 | 前向/后向 snowballing，Wohlin et al. 2022 指导 |
| Thematic Analysis | §3.6 | Braun & Clarke reflexive TA：familiarization → generating codes → searching themes → reviewing themes → defining/naming themes → producing report |
| 数据抽取与合成 | §3.7 + §4.1 | 对每篇文献抽取 text segments → code → theme → category（四级抽象） |
| Table 5 | §4.1 p.11 | TA 合成总表：5 个 aspect × (extracted data + coded data + themes + categories) 的完整四级抽象统计 |
| CPTM 建模 | §4.1.6 + §4.1.7 | 将 Challenges/Practices/Tools/Metrics 的 themes 建立交叉链接（谁解决谁、谁度量谁），映射到 Gartner 10-stage lifecycle |
| Table 21 | §4.2.3 p.25 | CPTM 模型全生命周期映射表：每个 stage 列出 C/P/T/M 编号 |
| Confirmatory Search | §4.3 | 2022 年前后补充 13 WL + 7 GL，不进入 TA/CPTM 以保持原 MLR 结果不变 |

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme

该论文有**非常丰富的显式分类和编码体系**，绝不仅是 6 个通用维度可以覆盖：

#### A. 五大方面（Aspects）
- **Definitions**：28 WL + 15 GL 定义 → 74 codes → 21 themes → 4 categories
- **Challenges**：73 WL + 53 GL 挑战 → 85 codes → 23 themes → 4 categories
- **Practices**：219 WL + 137 GL 实践 → 142 codes → 56 themes → 4 categories
- **Tools/Technologies**：18 WL + 45 GL 工具 → 56 codes → 16 themes → 1 category (Technology)
- **Metrics/Measurement**：7 WL + 13 GL 度量 → 20 codes → 16 themes → 3 categories

#### B. 四级抽象管道（提取 → 编码 → 主题 → 范畴）
```
text segment → code → theme → category
```
每一层都有原文 Table 5 的完整统计映射，且 Table 6--20 给出每个 aspects 的 code、theme、category、频次、来源文献编号。

#### C. 四类高层范畴（Categories）
- **OPC**（Organization, People and Culture）：组织、人员、文化相关
- **Process Capabilities**（PC）：流程能力相关
- **Technology**（Technology）：技术方案、软硬件工具
- **Business**：商业利益、客户、产品服务质量

此四类范畴是原文分类体系的核心轴，贯穿定义、挑战、实践、度量各 aspects（工具方面仅 Technology 一类，度量方面仅 OPC/PC/Technology 三类）。原文明确解释了 Business 类别是为容纳灰色文献中显现的商业视角而增设的归纳结果。

#### D. CPTM 模型：编码化命名 + 交叉链接 + 生命周期映射
- **C01--C28**：28 个挑战编码（23 自研 + 5 来自 Myrbakken and Colomo-Palacios 2017）
- **P01--P60**：60 个实践编码
- **T01--T18**：18 个工具/技术编码
- **M01--M20**：20 个度量编码
- 交叉链接：哪些实践解决哪些挑战，哪些工具支撑哪些实践，哪些度量衡量哪些实践/挑战
- **Gartner 十阶段生命周期**：Plan → Create → Verify → Preprod → Release → Prevent → Detect → Respond → Predict → Adapt

#### E. 质量评价体系
- WL 使用 narrative quality evaluation，从研究设计、数据收集、数据分析等维度逐篇评价
- GL 按 source type 和 authority level 分类（organisation reports、vendor white papers、practitioner blogs 等）

#### F. GSE 维度
- 两条确认搜索（Confirmatory Search 中 4 WL papers 含 GSE/global 维度）
- 表 3--4 列出仅有的 4 篇与 GSE 部分相关的 WL papers
- 明确结论：现有 WL+GL 未真正覆盖 Global DevSecOps

#### G. Validity Threats 体系
原文在 §5 按 Wohlin et al. 2012 框架讨论：
- Construct validity（搜索词完整性、GSE 术语覆盖）
- Internal validity（TA 主观性、双人独立编码缺失）
- External validity（GL 时变风险、语言限制）
- Conclusion validity（确认搜索未整合入 TA 导致可能的滞后）

#### H. Open Science / Replication Artifacts
- Zenodo DOI: 10.5281/zenodo.7959584
- 包含 protocol、included papers + QA score、raw text/codes、thematic synthesis、TA tables、full CPTM model

### 2.4 原文如何从字段/统计观察形成结论

原文的 finding 形成路径非常清晰：

```
RQ1 路径：
  提取 text segments → 编码 → 主题 → 范畴 → 频次统计（WL/GL 分别计数）
  → 频次/覆盖率作为 "关注度" 信号
  → 跨方面链接形成 CPTM 模型 → 生命周期映射 → 识别 coverage gap

RQ2 路径：
  Search String 2 → 极少量命中 → 逐篇分析 → 无文献同时覆盖 DevSecOps+GSE
  → 四种可能解释 → 声明研究空白
```

关键方法学特征：
1. **频次统计始终做 WL/GL 区分**，不混算单一总量（GL 的 grey nature 可能 inflate/deflate 特定信号）。
2. **讨论始终在频次、覆盖、缺口中进行**，不声称因果。
3. **Confirmatory search 不与主 TA 混合**，保证双轨统计口径不随时间漂移。
4. 挑战方面主动与 Akbar et al. 2022 和 Rajapakse et al. 2022 两个相近时间发表的新综述交叉验证，使用 "all can match or partly match" 表述，不做 superiority claim。
5. 对 GSE gap 提出四种可能解释（不相关、安全职能集中化、研究空白、术语遗漏），不做单一断言。

## 3. 当前 `review.md` 维度树审计

### 3.1 审计总判断

当前 `review.md` 的维度树存在**结构性不对称**：树明确声明了 6 个通用叶子（scope、data_source、method、evidence、finding、taxonomy），这 6 个叶子本质上是 survey-of-surveys 脚手架本身的六类 pattern 字段元模型（即 A1 用于"研究综述"的元维度框架），而不是本文 `devsecops-primary-dimensions` 的实际 extraction form / coding scheme / taxonomy 的忠实复原。

当前树另设 5 个 `[leaf-*-orig-*]` 候选叶子（aspect、theme-category、cptm-item、lifecycle-stage、gse-gap），作为"原文模式候选叶子映射"，但标注为 "A1 种子" 且未经 A2a 精核。这 5 个候选叶子确实指向了原文的真实 schema 元素，但：

1. 它们被放在与 6 个通用叶子平行但标注为"候选"的位置，缺乏明确的父子嵌套关系（例如，原文的 aspect 应下辖 definition/challenge/practice/tool/metric，再下辖各 theme，再下辖各 code）。
2. 原文的核心四级抽象管道（text→code→theme→category）并未作为独立维度节点被建模。
3. CPTM 模型的跨 aspect 链接（Challenge↔Practice↔Tool↔Metric 的交叉索引）、生命周期映射、WL/GL 分流计数、质量评价体系、confirmatory search 与主 TA 的分离规则均未进入维度树结构。

按 `pattern-field-schema.md` §8 的合同规定，完整的维度树应包含 "节点标识、操作化定义、取值空间、证据要求、缺失值语义、统计用途、候选发现用途、父节点 ID、子节点列表"，并支持关系边。当前的 6+5 结构在这些维度上缺少原文级填充。

### 3.2 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 通过 | `[dim-devsecops-primary-dimensions-root]` 已正确声明，回链到论文来源与 A.1。 | 通过 |
| 主干分支是否覆盖原文 schema | **I** | 6 个通用叶子（scope/data_source/method/evidence/finding/taxonomy）是 A1 元维度框架而非本文提取表。原文的五大 aspects（Definitions/Challenges/Practices/Tools/Metrics）、四类范畴（OPC/PC/Technology/Business）、CPTM 交叉链接、四级抽象管道（text→code→theme→category）、Gartner 生命周期、WL/GL 分流均未在树枝中直接出现，仅作为 "候选叶子" 旁置。 | I |
| 叶子维度是否足够具体 | **C** | scope/data_source/method 等叶子没有原文的 aspect 级子节点（如 "Challenges 包含 23 themes"、"Practices 包含 56 themes"），取值空间仍然是 "A2a 精核入口" 级别的 placeholder，无法执行字段级编码。对 Paper2 而言，缺少足够具体的维度意味着后续 A2a/A2b 无法直接复用这些叶子作为抽取模板。 | C |
| 取值空间是否可执行 | **C** | 每个叶子维度标注 "取值空间在 A2a 扩库前不得视为饱和"，这正确地避免了过度收敛，但也意味着当前叶子没有从原文 Table 5--21 中提取任何可操作的候选取值枚举（例如 scope 应能从原文的 "WL 104 篇，GL 43 篇，2012--2021" 中得出候选约束）。叶子空有节点标识，没有可填充的取值。 | C |
| 关系边是否缺失 | **I** | 当前仅建模了 method↔evidence 和 taxonomy↔finding 两条边。原文有更丰富的关系需要建模：aspect→category（定义/挑战/实践/工具/度量各属于哪些 category）；challenge→practice（哪些实践解决哪些挑战）；practice→tool（哪些工具支撑哪些实践）；practice→metric（哪些度量衡量哪些实践/挑战）；aspect→lifecycle_stage（CPTM 映射到 Gartner 10 stage）；WL↔GL（双轨分流关系）。这些关系才是原文 "linking aspects/themes" 的核心贡献，当前树遗漏了。 | I |
| 统计用途 / 分母是否正确 | **M** | 原文在所有频次统计中都区分 WL/GL（例如 "挑战方面 OPC 类别 9 项排第一" 需知分母是 28 个挑战编码），且 confirmatory search 与非 confirmatory 有明显统计边界。当前树未将 WL/GL 分流和 confirmatory search 排除规则建模为统计约束。 | M |
| 候选 finding 路径是否完整 | **I** | A.3 的 12 条结论中，C09 正确地指出 "final research finding 必须经过跨论文证据、反证与研究者裁决"，但原文的完整 finding 路径（频次统计→覆盖缺口→CPTM 链接→GSE 空白→四种可能解释→implications）在维度树和 A.3 中未得到完整复现。原文四个方面的 GSE gap 解释（不相关/集中化/空白/术语遗漏）是一种重要的 "不确定 finding" 模式，对 Paper2 的 finding 裁决有启发价值，却被完全遗漏。 | I |
| A.1--A.4 证据链是否足够 | **M** | A.1 来源文件记录完整；A.2 有 5 条证据（EV-001--005），覆盖了论文结构、RQ/方法、分类结论、限制和跨字段关系，但证据强度均为 `weak` 且缺乏原文页码/表号/段落号锚定；A.3 有 12 条结论，均标记 `weak` 和 `schema_seed`，口径审慎；A.4 的 visual-check 仍为 `needs_manual_check`。整体证据链框架正确但深度不足。 | M |
| 是否存在可能误导 A2a 的强主张 | **通过** | 所有结论均标记为 `weak`/`schema_seed`/`candidate_finding`，没有将本文的领域统计结论写成可迁移 Paper2 的 final finding。审查通过。 | 通过 |

### 3.3 核心问题详析

#### 问题一：6 个通用叶子是 "通用接口" 而非 "原文 schema"

`review.md` 当前的结构是：

```
[dim-devsecops-primary-dimensions-root]
  ├── [leaf-devsecops-primary-dimensions-scope]       ← 通用元维度（A1 六类 pattern）
  ├── [leaf-devsecops-primary-dimensions-data_source]  ← 通用元维度
  ├── [leaf-devsecops-primary-dimensions-method]       ← 通用元维度
  ├── [leaf-devsecops-primary-dimensions-evidence]     ← 通用元维度
  ├── [leaf-devsecops-primary-dimensions-finding]      ← 通用元维度
  ├── [leaf-devsecops-primary-dimensions-taxonomy]     ← 通用元维度
  └── [leaf-*-orig-*] × 5                              ← 候选原文叶子
```

这 6 个叶子与 `pattern-field-schema.md` 中定义的六类 pattern 字段（dimension_pattern、finding_pattern、evidence_presentation_pattern、report_structure_pattern 等）高度同构。它们回答的问题是 "这篇综述的维度/发现/证据模式是什么"，而非 "这篇综述自身使用了哪些字段来抽取和分析文献"。

**对 Paper2 的影响**：A2a 如果使用当前树作为种子，得到的将是一套 "元综述字段"，而非可用于索引目标领域论文的 "领域抽取字段"。这会导致 Paper2 的维度模式在 A2a 阶段发生严重概念漂移。

#### 问题二：原文富结构未被复原

原文实际上提供了一个五级层次结构（以 Challenges 为例）：

```
五大方面(Aspect)
  ├── Challenges (aspect)
  │   ├── 73 WL segments → 85 codes → 23 themes → 4 categories
  │   │   ├── OPC category (9 challenges: C01--C09)
  │   │   ├── PC category (8 challenges: C10--C17)
  │   │   ├── Technology category (7 challenges: C18--C24)
  │   │   └── Business category (4 challenges: C25--C28)
  │   └── CPTM links: C01→P01, C02→{P02, P08, P10}, ...
  ├── Practices (aspect)
  │   └── 219 WL + 137 GL → 142 codes → 56 themes → 4 categories
  │       └── CPTM links: P01→{T??}, P01→{M01}...
  ├── ...
  └── CPTM 生命周期映射 (Gartner 10 stages)
```

当前树未保留这个层次。`leaf-*-orig-*` 只列举了 aspect/theme-category/cptm-item/lifecycle-stage/gse-gap 作为平面节点，没有嵌套关系，没有编码值列表，没有跨 aspect 链接。

#### 问题三：原文的方法学特征被转换为内容特征

原文的核心方法学贡献——四级抽象管道、双轨 WL/GL 分流、confirmatory search 排除规则、质量评价——在 A.2 中被归类为 "evidence role: method"，但这些**方法学特征本身应该成为维度树中关于 "综述方法" 的分支**（例如，对于 Paper2 来说，"一篇论文使用了什么证据等级体系" 是一个需要从综述中抽取的维度）。当前树将它们归入 review.md 的证据账本（A.2），而不是维度树的结构节点。

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树。该树包括两个层面：(a) 原文自己的 extraction/coding schema（这是 Paper2 需要从中学习的）；(b) A1 元维度注释（说明这对 Paper2 的 schema seed 价值）。

```
[dim-devsecops-primary-dimensions-root]
├── [dim-devsecops-primary-dimensions-review-meta]        # 综述元信息（论文自身属性）
│   ├── [leaf-devsecops-primary-dimensions-review-type]    # 单篇综述类型
│   │   取值空间: {MLR, SLR, SMS, tertiary_study, guideline, roadmap}
│   │   证据: §3, §2 与既有综述比较表 → EV-002
│   │   取值: "multivocal literature review (MLR)"
│   ├── [leaf-devsecops-primary-dimensions-review-domain] # SE 子领域
│   │   取值: "DevSecOps; GSE"
│   ├── [leaf-devsecops-primary-dimensions-year-range]     # 年份范围
│   │   取值: "2012--2021"（主 MLR）；"2022+"（confirmatory search，不入统计）
│   └── [leaf-devsecops-primary-dimensions-review-aim]     # 综述目标类型
│       取值空间: {status_quo, gap_identification, taxonomy, model_construction, methodology_guidance}
│       取值: "status_quo + gap_identification + model_construction"
│
├── [dim-devsecops-primary-dimensions-search-strategy]     # 检索策略
│   ├── [leaf-devsecops-primary-dimensions-search-track]   # 检索轨数
│   │   取值: "dual-track (white + grey)"
│   │   原文: §3.1--3.2
│   ├── [leaf-devsecops-primary-dimensions-search-scope]   # 数据库/来源
│   │   取值: WL={ACM DL, IEEE Xplore, ScienceDirect, Scopus, ...}; GL={Google, practitioner sources}
│   │   原文: §3.1 Table 1, §3.2
│   ├── [leaf-devsecops-primary-dimensions-search-string-count] # 搜索字符串数
│   │   取值: 2 (SS1: DevSecOps general; SS2: +GSE terms)
│   └── [leaf-devsecops-primary-dimensions-snowballing]    # 是否 snowballing
│       取值: "yes (forward + backward, per Wohlin et al. 2022)"
│       原文: §3.5
│
├── [dim-devsecops-primary-dimensions-inclusion-exclusion] # 纳排体系
│   ├── [leaf-devsecops-primary-dimensions-incl-criteria-count]
│   │   取值: 原文 §3.3 表；具体条目数
│   ├── [leaf-devsecops-primary-dimensions-excl-criteria-count]
│   │   取值: 原文 §3.3 表
│   ├── [leaf-devsecops-primary-dimensions-corpus-size]    # 最终语料
│   │   取值结构: {WL: 104, GL: 43, total: 147}
│   │   confirmatory: {WL: 13, GL: 7} (不计入 TA)
│   ├── [leaf-devsecops-primary-dimensions-quality-assessment] # 质量评价
│   │   取值空间: {narrative, scoring_exclusion, checklist, authority_classification, none}
│   │   取值: "narrative quality evaluation (WL) + source authority classification (GL)"
│   │   原文: §3.4
│   └── [leaf-devsecops-primary-dimensions-confirmatory-search] # 确认搜索
│       取值: "yes; 13 WL + 7 GL post-2021; excluded from TA/CPTM"
│       原文: §4.3
│
├── [dim-devsecops-primary-dimensions-extraction-schema]   # 数据抽取 / 编码方案（核心）
│   ├── [dim-devsecops-primary-dimensions-extraction-pipeline] # 抽取管道
│   │   ├── [leaf-devsecops-primary-dimensions-extraction-levels] # 抽象层级
│   │   │   取值: 4 ("text segments → codes → themes → categories")
│   │   │   原文: §3.6, Table 5
│   │   └── [leaf-devsecops-primary-dimensions-analysis-method] # 分析方法
│   │       取值: "Braun & Clarke reflexive Thematic Analysis (6 phases)"
│   │
│   ├── [dim-devsecops-primary-dimensions-aspects]         # 五大方面
│   │   ├── [leaf-devsecops-primary-dimensions-aspect-list]
│   │   │   取值: {Definitions, Challenges, Practices, Tools/Technologies, Metrics/Measurement}
│   │   ├── [leaf-devsecops-primary-dimensions-aspect-n-extracted] # 每 aspect 的抽取量
│   │   │   取值结构: per-aspect {WL count, GL count, codes count, themes count}
│   │   │   原文: Table 5
│   │   └── [leaf-devsecops-primary-dimensions-aspect-dominant] # 主导 aspect
│   │       取值: "Practices (219 WL + 137 GL = most extracted); Metrics (7 WL + 13 GL = least)"
│   │
│   ├── [dim-devsecops-primary-dimensions-category-system] # 范畴体系
│   │   ├── [leaf-devsecops-primary-dimensions-category-list]
│   │   │   取值: {OPC, Process Capabilities, Technology, Business}
│   │   │   定义: 原文 §4.1 (OPC=Organization/People/Culture; PC=Process Capabilities; Tech=technological approaches; Business=business benefits/customers/quality)
│   │   ├── [leaf-devsecops-primary-dimensions-category-per-aspect]
│   │   │   取值结构: Definitions→4 cats; Challenges→4 cats; Practices→4 cats; Metrics→3 cats (no Business); Tools→1 cat (Technology)
│   │   │   原文: Table 5
│   │   └── [leaf-devsecops-primary-dimensions-category-inductive]
│   │       取值: "yes; Business category added inductively from GL data"
│   │       原文: §4.1 Business definition paragraph
│   │
│   ├── [dim-devsecops-primary-dimensions-theme-coding]    # 主题编码体系
│   │   ├── [leaf-devsecops-primary-dimensions-theme-count-by-aspect]
│   │   │   取值: {Def 21, Ch 23, Pr 56, To 16, Me 16}
│   │   │   原文: Table 5
│   │   ├── [leaf-devsecops-primary-dimensions-code-count-by-aspect]
│   │   │   取值: {Def 74, Ch 85, Pr 142, To 56, Me 20}
│   │   │   原文: Table 5
│   │   └── [leaf-devsecops-primary-dimensions-source-tracking]
│   │       取值: "per-code source paper IDs (e.g., S1-ACM-01, S1-GL-01 etc.)"
│   │       原文: Table 6--20
│   │
│   └── [dim-devsecops-primary-dimensions-cptm-model]      # CPTM 模型
│       ├── [leaf-devsecops-primary-dimensions-cptm-item-count]
│       │   取值: {C: 28, P: 60, T: 18, M: 20}
│       │   原文: §4.1.6, Table 21
│       ├── [leaf-devsecops-primary-dimensions-cptm-cross-links]
│       │   取值: "yes; C→P→T, P→M (cross-aspect links)"
│       │   原文: §4.1.6 (p.15--22), Table 21
│       ├── [leaf-devsecops-primary-dimensions-cptm-lifecycle-model]
│       │   取值: "Gartner 10-stage: Plan, Create, Verify, Preprod, Release, Prevent, Detect, Respond, Predict, Adapt"
│       │   原文: §4.1.7, Table 21 (p.25)
│       ├── [leaf-devsecops-primary-dimensions-cptm-lifecycle-coverage]
│       │   取值: "per-stage {challenges, practices, tools, metrics} mapping"
│       │   原文: Table 21
│       └── [leaf-devsecops-primary-dimensions-cptm-coverage-gap]
│           取值: "某些 stage 缺少特定 C/P/T/M 映射 → 识别研究/实践空白"
│           原文: §4.1.7 discussion
│
├── [dim-devsecops-primary-dimensions-gse-analysis]        # GSE 维度
│   ├── [leaf-devsecops-primary-dimensions-gse-search-result]
│   │   取值: "negative finding; no paper covers all three terms (DevOps + security + GSE)"
│   │   原文: §4.2
│   ├── [leaf-devsecops-primary-dimensions-gse-partial-hits]
│   │   取值: "4 WL papers partially relevant (Table 3--4)；0 GL hits (top 100 Google results)"
│   ├── [leaf-devsecops-primary-dimensions-gse-explanations]
│   │   取值空间: {no_correlation, centralized_security_function, research_gap, terminology_missed}
│   │   取值: "all four possibilities discussed, none concluded"
│   │   原文: §4.2.3
│   └── [leaf-devsecops-primary-dimensions-gse-finding-strength]
│       取值: "absence_evidence (not a positive finding)"
│
├── [dim-devsecops-primary-dimensions-evidence-presentation] # 证据呈现方式
│   ├── [leaf-devsecops-primary-dimensions-evidence-table-count]
│   │   取值: "Tables 1--21 (includes search strategy, QA, TA synthesis, theme-code tables × 15 aspects, CPTM lifecycle)"
│   ├── [leaf-devsecops-primary-dimensions-evidence-figure-count]
│   │   取值: "Figs 1--9 (including PRISMA-style flowchart, TA process, CPTM model diagrams)"
│   ├── [leaf-devsecops-primary-dimensions-evidence-source-disaggregation]
│   │   取值: "yes; WL and GL counts always reported separately"
│   │   原文: throughout §4.1
│   ├── [leaf-devsecops-primary-dimensions-evidence-confirmatory-separation]
│   │   取值: "confirmatory search results NOT integrated into TA/CPTM; reported separately in §4.3"
│   └── [leaf-devsecops-primary-dimensions-evidence-zenodo]
│       取值: "Zenodo DOI: 10.5281/zenodo.7959584; validated by JSS Open Science Board"
│
├── [dim-devsecops-primary-dimensions-finding-path]        # 发现形成路径
│   ├── [leaf-devsecops-primary-dimensions-finding-frequency-based]
│   │   取值: "yes; theme frequency within each aspect/category used as 'attention' signal"
│   │   约束: "explicitly not claimed as real-world priority (needs Delphi validation)"
│   ├── [leaf-devsecops-primary-dimensions-finding-cross-validation]
│   │   取值: "yes; challenges cross-validated with Myrbakken 2017, Akbar 2022, Rajapakse 2022"
│   ├── [leaf-devsecops-primary-dimensions-finding-gap]
│   │   取值: "GSE absence as research gap; lifecycle stage coverage gaps"
│   └── [leaf-devsecops-primary-dimensions-finding-implications]
│       取值: "researcher implications (4 points) + practitioner implications (roadmap use)"
│
└── [dim-devsecops-primary-dimensions-validity-threats]    # 效度威胁
    ├── [leaf-devsecops-primary-dimensions-validity-framework]
    │   取值: "Wohlin et al. 2012: construct, internal, external, conclusion"
    │   原文: §5
    ├── [leaf-devsecops-primary-dimensions-validity-construct]
    │   取值: "search string completeness; GSE terminology coverage"
    ├── [leaf-devsecops-primary-dimensions-validity-internal]
    │   取值: "TA subjectivity acknowledged; no dual independent coding"
    ├── [leaf-devsecops-primary-dimensions-validity-external]
    │   取值: "GL temporal volatility; English-only; small WL sample per sub-aspect"
    ├── [leaf-devsecops-primary-dimensions-validity-conclusion]
    │   取值: "confirmatory search not integrated into TA (possible lag)"
    └── [leaf-devsecops-primary-dimensions-validity-addressed]
        取值: "partially; acknowledged but not mitigated (e.g., no inter-rater reliability)"
```

### 4.1 与当前树的关系说明

当前树的 scope/data_source 可映射到上述 search-strategy 分支；method 可映射到 extraction-schema 分支；evidence 可映射到 evidence-presentation 分支；finding 可映射到 finding-path 分支；taxonomy 可映射到 category-system + cptm-model 分支。新增的 GSE、validity-threats、inclusion-exclusion、confirmatory search 分支是当前树完全缺失的。

上述骨架的每个叶子均可根据原文 Table 5--21 填充具体取值（如 C01--C28 的挑战编号列表），而非仅留 "A2a 精核入口"。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 将 6 个通用叶子降级为 A1 元注释，不作为维度树主体 | `review.md` A.1 下方的维度树定义 | 在维度树根节点注释中声明 "以下 6 个叶是 A1 元维度注释层，非原文 schema"，并在树中增加明确的原文维度分支。或者将 6 个通用叶子移至 A.2 证据账本作为 "A1 meta-dimensions"，不在维度树中与原文结构并列。 | `pattern-field-schema.md` §8.2--8.3；本文 Table 5 | C |
| 补充五大 aspect 的层级节点及子叶 | 维度树 `[dim-*]` 节点列表 | 新增 `[dim-devsecops-primary-dimensions-aspects]` 并下设 `[leaf-*-aspect-list]`、`[leaf-*-aspect-n-extracted]`、`[leaf-*-aspect-dominant]` | 原文 §4.1, Table 5, p.11 | C |
| 补充四级抽象管道节点 | 维度树 | 新增 `[dim-devsecops-primary-dimensions-extraction-pipeline]`，包含 `[leaf-*-extraction-levels]`（text→code→theme→category）和 `[leaf-*-analysis-method]`（Braun & Clarke reflexive TA） | 原文 §3.6, Table 5 | I |
| 补充范畴体系（OPC/PC/Technology/Business）及 aspect 归属 | 维度树 | 新增 `[dim-devsecops-primary-dimensions-category-system]`，含四类范畴的完整列表、各 aspect 归属关系、Business 的归纳来源 | 原文 §4.1 各类别定义段 | I |
| 补充 CPTM 交叉链接和生命周期映射 | 维度树 + A.2 | 新增 `[dim-devsecops-primary-dimensions-cptm-model]`，含 C/P/T/M 计数、交叉链接存在性、Gartner 10-stage 生命周期、coverage gap | 原文 §4.1.6--4.1.7, Table 21 | I |
| 补充 GSE 分析的完整 finding 路径 | 维度树 + A.3 | 新增 `[dim-devsecops-primary-dimensions-gse-analysis]`，含空结果、部分命中、四种解释枚举 | 原文 §4.2, Table 3--4 | I |
| 补充纳排/语料/质量评价节点 | 维度树 | 新增 `[dim-devsecops-primary-dimensions-inclusion-exclusion]` 分支，含纳入排除标准、语料规模（WL/GL 分开）、质量评价类型、confirmatory search 规则 | 原文 §3.3--3.4, §4.3 | M |
| 补充效度威胁节点 | 维度树 | 新增 `[dim-devsecops-primary-dimensions-validity-threats]`，按 construct/internal/external/conclusion 四维展开 | 原文 §5 | M |
| 补充 WL/GL 分流统计约束 | 维度树中统计用途注释 | 在所有涉及频次的叶子中明确写 "WL 和 GL 必须分开计数；confirmatory search 不计入主统计池" | 原文 Table 5 及各处 WL/GL 分列 | M |
| 将 `leaf-*-orig-*` 从平级候选升级为维度树的正式子节点 | 维度树 | 当前 `[leaf-*-orig-aspect]` 等 5 个候选叶子应重新归类到上述新增分支下（如 orig-aspect → aspects 分支；orig-theme-category → category 分支；orig-cptm-item → cptm 分支；orig-lifecycle-stage → cptm 分支；orig-gse-gap → gse 分支） | 原文对应章节 | I |
| 列出原文 Table 5--21 的精确页码、表号锚定 | A.2 证据账本 | 每条 EV 增加 "页码/表号/段落号" 字段，将当前所有 `not_verified` 证据的 source anchors 至少定位到 `paper_content.txt` 的行级或 § 级 | 原文 §4.1, Table 5 (p.11), Table 21 (p.25) 等 | M |

## 6. C/I/M 结论

### C（阻塞级）—— 直接破坏 Paper2 学术目标或证据链

| 编号 | 问题 | 对 Paper2 的影响 |
|---|---|---|
| C1 | 6 个通用叶子（scope/data_source/method/evidence/finding/taxonomy）是 A1 元维度框架，不是本文 extraction form / coding scheme / taxonomy 的忠实复原。当前树以此为主体，其取值空间均为空或 "待 A2a 精核"，无法指导 A2a 构建可操作的领域字段抽取模板。 | 如果 A2a 直接继承此树，将得到一套 "元综述字段" 而非 "领域抽取字段"，导致 Paper2 维度模式在 A2a→A3 阶段发生根本性概念漂移——相当于用审稿人的 checklist 去对论文做内容抽取。 |
| C2 | CPTM 模型的 Challenge↔Practice↔Tool↔Metric 交叉链接体系（原文核心贡献之一）完全未进入维度树。这是本文为 Paper2 提供的最有价值先验之一：如何将多个平铺 aspect 通过关系边整合为一个可审计的交叉模型。 | Paper2 缺失 "跨字段关系建模" 的关键模式先验，可能在 A3 发现形成阶段缺乏 "如何从字段统计走到跨字段发现" 的路线图。 |

### I（重要级）—— 实质影响维度树可用性、原文 schema 复原、证据可审计性

| 编号 | 问题 | 对 Paper2 的影响 |
|---|---|---|
| I1 | 原文的四级抽象管道（text→code→theme→category）未在维度树中建模。这是原文 Thematic Analysis 的核心方法学特征——对 Paper2 来说，它可以启发 "不同综述使用几层抽象" 的元维度比较。 | 后续 A2a 可能忽略不同综述在抽象层级上的差异（有的 3 级、有的 4 级），导致跨综述比较时字段粒度不可比。 |
| I2 | 原文的 GSE 分析（双搜索字符串、极少量部分命中、四种可能解释的讨论模式）被简化为单个 `[leaf-*-orig-gse-gap]`，完整的负面发现路径（搜索→评估→解释枚举→未下结论）被丢失。 | Paper2 对 "absence evidence / negative finding" 的处理模式缺少一个重要范本——如何把 "没找到" 写成一个可审计的结构化发现，而非单行标注。 |
| I3 | 原文的 WL/GL 双轨统计口径、confirmatory search 排除规则未被建模为统计约束。 | Paper2 在汇总跨综述统计时可能误混不同来源性质（如将 GL practitioner claims 与 WL peer-reviewed 等权相加），违反原文本身的证据纪律。 |
| I4 | 四类范畴（OPC/PC/Technology/Business）的归纳性质（特别是 Business 的灰色文献诱导）未在维度树中记录。这是 "分类体系可随数据诱导演化" 的活证据，对 Paper2 的 "维度模式演化" 主题有直接启发。 | Paper2 的 "模式演化" 主线可能缺少一个来自强样本的实证案例：分类体系如何因为新数据类型（GL business perspective）而修订。 |

### M（维护级）—— 不阻塞的清晰度或维护性建议

| 编号 | 问题 | 建议 |
|---|---|---|
| M1 | A.2 证据账本的 5 条 EV 均为泛定位（"§1, §2, §3--5"），未锚定到 `paper_content.txt` 的行号或原著页码。 | 增加来源锚点精度（至少到 `paper_content.txt` 的 `--- Page N ---` 标记级）。 |
| M2 | A.4 的 visual-check 仍为 `needs_manual_check`。涉及 Fig. 5--9 的 CPTM 模型截图和 Table 5--21 的版面核对应尽快完成，否则证据强度始终为 `not_verified`。 | 在后续轮次执行 PDF 视觉核对。 |
| M3 | `[leaf-*-orig-*]` 的 5 个候选叶子当前与 6 个通用叶子平级，但缺少明确的父子归属（如 `orig-aspect` 应归属到 `dim-aspects` 下）。 | 按 §4 建议骨架重新组织。 |
| M4 | A.3 结论 C05--C07（对 scope/data_source/method 三个叶子的 "来自原文 RQ/方法/分类/评价/讨论结构" 描述过于泛化，不足以区分这三个叶子承载的具体内容差异。 | 每个叶子至少写一句与本文具体关联的差异化说明。 |

### 最终建议

**NEEDS FIX**。核心原因是：
1. 当前树的骨架是 A1 元维度框架，而非原文 schema 的忠实复原。C1 级别。
2. 原文最独特的 CPTM 交叉链接模型和 GSE negative finding 路径完全缺失。C2 + I2 级别。
3. 这些缺失会直接导致 Paper2 在 A2a/A3 阶段无法从本文获取其本应提供的最强模式先验（跨 aspect 关系建模、absence finding 结构化、WL/GL 统计分流）。

上述建议修复在 §5 中给出了 11 项具体操作。修复后应使维度树至少达到 §4 骨架的信息密度，并在 A.2/A.3 中补全对应的证据锚点和结论项。

---

*审计完成时间：2026-06-29*
*reviewer: deepseek*
*未使用 sub-subagent；未修改仓库文件；未 push；未 gh comment*
