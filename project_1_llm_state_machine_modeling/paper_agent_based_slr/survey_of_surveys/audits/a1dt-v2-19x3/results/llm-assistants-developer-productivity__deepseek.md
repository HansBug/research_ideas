Now I have all the material needed. Let me compile the complete A1-DT v2 audit.

---

# A1-DT v2 单篇全文审计报告：`llm-assistants-developer-productivity`

## 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `llm-assistants-developer-productivity` |
| agent | `deepseek` |
| 是否已读 `paper_content.txt` | 是，全文 1842 行，从 §1 到 §References 逐章读过 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是，均完整读取 |
| 是否打开或核对 `paper.pdf` | 否。未对 PDF 版面做逐页视觉核验；所有证据来自 `paper_content.txt` 文本提取。表/图编号、精确排版和页码仍需人工 PDF 核对。 |
| 原文类型 | **SLR + SMS**（systematic literature review + systematic mapping study） |
| 被编码样本单位 | **peer-reviewed primary study**（单篇实证研究论文），经过数据库检索→去重→标题摘要筛选→全文筛选→snowballing→质量评估后纳入 |
| 样本数量 / 分母 | 最终纳入 **39** 篇（全文筛选后 39 篇 + snowballing 获得 5 篇 = 44 篇进入 QA，但只有 39 篇被统计报告；QA 不淘汰论文——原文 §3.3 明确"no study was excluded on the basis of low quality scores"——因此报告基数仍为通过全文筛选的 39 篇） |
| 原生树类型 | **维度森林**（多表多分类框架并存，不是单一 tree） |
| 主统计池资格 | **是**。有系统检索、系统纳排、系统数据抽取、QA 表和 replication package；满足 SLR/SMS 统计池要求 |
| 总体判定 | **pass**（证据充分、schema 完整、原生维度森林可恢复；现有 `review.md` 需返修） |

## 1. 原文证据阅读说明

### 1.1 读取文件清单

| 文件 | 状态 | 说明 |
|---|---|---|
| `paper_content.txt` | ✅ 全文读完（1842 行） | 逐章节阅读 §1 Introduction → §2 Background → §3 Method → §4 RQ0 → §5 RQ1 → §6 RQ2 (benefits + risks) → §7 RQ3 (SPACE) → §8 Discussion → §9 Threats → §10 Conclusion → §References |
| `bibtex.bib` | ✅ 完整读取 | 确认 DOI、作者、年份、期刊（TOSEM） |
| `metadata.json` | ✅ 完整读取 | 确认 eligibility、evidence_role、statistical_pool 等本地分类字段 |
| `review.md` | ✅ 完整读取（492 行） | 确认现有维度树、A.1--A.4、SUMMARY 表内容 |
| `paper.pdf` | ❌ 未核对 | 未打开 PDF 做版面/图表视觉核验 |

### 1.2 是否需要 PDF 核验

需要。以下内容建议 PDF 视觉核验：
- Table 1--11 的精确表头、页码和列名（text 提取可能丢失跨页表头或列对齐）
- Fig. 1--9 的图形类型和轴标（radar plot、UpSet plot、Venn/intersection plot、Tetrad diagram）
- 附录 / supplementary material 条目（Zenodo replication package 的结构）
- 39 篇 primary studies 的 [PS1]--[PS39] 完整文献表

### 1.3 12 个关键原文证据锚点

| # | 锚点标识 | 原文章节 | 段落/表图线索 | 短引或释义 |
|---|---|---|---|---|
| EV-001 | method-protocol | §3.1 | Table 1, Fig. 1 | 数据库检索：ACM/IEEE/ScienceDirect/WoS/Scopus/Springer，初始 n=9756→去重后 8953→标题摘要筛选 228→全文筛选 39→snowballing +5→QA 44→最终纳入 39 |
| EV-002 | control-papers | §3.1.1 | "17 control papers" | Pre-review mapping 识别 17 篇控制论文，用于迭代验证搜索式 |
| EV-003 | ic-ec | §3.1.1 | IC1--IC3, EC1--EC5 | 5 条纳入 + 5 条排除标准；EC3 明确排除 secondary studies |
| EV-004 | qa-criteria | §3.3, Table 2 | QA1--QA11 (adapted from Lenarduzzi et al.) | 11 条质量评价标准，3 分制；"no study was excluded" |
| EV-005 | extraction-form | §3.4 | "study goals, tools, empirical strategy and design, tasks, settings, and key results" | 数据抽取字段列表；分轮 thematic iteration 执行 |
| EV-006 | rq0-landscape | §4, Table 3--4 | venue 5-category classification, tool frequency | 39 篇按研究社区、工具分布编码 |
| EV-007 | rq1-strategy-taxonomy | §5.1, Table 5 | Stol & Fitzgerald [50] taxonomy: 6 strategies | Field Study/Experiment, Experimental Simulation, Lab Experiment, Sample Study, Judgment Study |
| EV-008 | rq1-procedure-taxonomy | §5.2, Table 6 | Glass, Vessey, Ramesh [51] taxonomy: 5 procedures | Survey, User Experiment, Concept Implementation, Interview, Case Study |
| EV-009 | rq1-instruments | §5.3, Table 7 | 3 instrument categories (self-reported / validated / behavioral & performance) | 明细列出 instruments + studies 映射 |
| EV-010 | rq2-benefit-themes | §6.1, Table 8 | 8 benefit themes from thematic analysis | Accelerate development, Minimize code search, Automate trivial tasks, Knowledge acquisition, Code-adjacent tasks, Task initiation, Code quality, Debugging |
| EV-011 | rq2-risk-themes | §6.2, Table 9 | 5 risk themes | Fail to meet requirements, Over-reliance/cognitive offloading, Disrupt flow, Limit code quality, Reduce team collaboration |
| EV-012 | rq3-space-mapping | §7, Table 10, Table 11 | SPACE 5 dimensions + 11 emergent sub-dimensions | Satisfaction 77%, Performance 64%, Efficiency 59%, Activity 31%, Communication 26%；Quality metrics table |

## 2. 样本单位与字段来源判定

### 2.1 原文纳入和逐项描述的对象是什么？

**单篇 peer-reviewed primary study**（即直接研究 LLM-assistants 对软件开发者生产力影响的实证论文）。每篇 primary study 获得一个 `[PSn]` 标识符（PS1--PS39），其元数据和发现被编码在多张表中。

### 2.2 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

**有，且层级清晰**：

1. **系统检索**：6 个数据库，统一搜索式（3 段 AND 结构：AI+LLM × developer × productivity），proximity operators（NEAR/5, w/5），17 篇控制论文验证
2. **系统纳排**：5 IC + 5 EC，PRISMA flow chart（Fig. 1），去重→标题摘要筛选（47 天）→全文筛选（10 周）→snowballing（2 周）
3. **系统数据抽取**：初始 thematic analysis 提取 study goals / tools / empirical strategy / tasks / settings / key results
4. **多轮编码**：RQ1 方法论编码（3 个外部 taxonomy）、RQ2 主题分析（benefit/risk themes）、RQ3 SPACE 映射（5 dim + emergent sub-dimensions）
5. **质量评价**：11 条 QA criteria，3 分制，但不用于淘汰
6. **Replication package**：Zenodo DOI 中提供 exclusion decision、classification、supplementary material

### 2.3 原文字段来自哪里？

| 字段来源 | 对应 RQ / 章节 | 形式 |
|---|---|---|
| Data extraction form（初始） | §3.4 | study goals, tools, strategy, tasks, settings, key results |
| Stol & Fitzgerald [50] taxonomy | RQ1 §5.1, Table 5 | 6-category research strategy |
| Glass/Vessey/Ramesh [51] taxonomy | RQ1 §5.2, Table 6 | 5-category research procedure |
| Hartson et al. [52] formative/summative | RQ1 §5.2 | binary classification |
| Instrument classification（自编） | RQ1 §5.3, Table 7 | 3-category: self-reported / validated / behavioral&performance |
| Thematic analysis（自编） | RQ2 §6, Table 8--9 | benefit 8 themes, risk 5 themes |
| SPACE framework [19] | RQ3 §7, Table 10 | 5 dimensions + 11 emergent sub-dimensions |
| Quality metrics（自编） | RQ3 §7, Table 11 | metric-by-study mapping |
| QA criteria (Lenarduzzi et al. [48]) | §3.3, Table 2 | 11 QA criteria |
| Publication venue classification（自编） | RQ0 §4.3, Table 3 | 5 research focus categories |

### 2.4 RQ 与样本单位的关系

RQ 不是树根，而是**编码结果的组织方式**。每个 RQ 就像一个"视图"：同一批 39 篇 primary study 在不同 RQ 下被不同分类框架重新编码。真正的树根是 `[PSn]` primary study 集合本身。

### 2.5 降级判断

无需降级。本文是标准 SLR+SMS，有完整检索/纳排/抽取/编码/QA 链。

## 3. 原生样本编码维度树 / 维度森林

本文采用**多视图维度森林**（不是单树），根节点为 `Primary Studies (n=39)`，下面按 RQ 分成 5 个主要维度簇：

```
Primary Studies (n=39) ─ [SLR+SMS 系统纳入与编码]
│
├── RQ0: Landscape（景观维度簇）
│   ├── Publication Year ─ 数值/区间 (2014--2024 peak 2024=77%) [Table not numbered, §4.1, Fig.2]
│   ├── Author Distribution ─ 关系值：per-author paper count (max=3) [§4.2]
│   ├── Publication Venue ─ 层级枚举：5-category research focus [Table 3, §4.3]
│   │   ├── SE & CS (46%)
│   │   ├── HCI (18%)
│   │   ├── Information Systems & Decision Science (13%)
│   │   ├── Human-Aspects & Socio-Economic (10%)
│   │   └── AI for SE / AI Engineering (8%) + SE Education (5%)
│   └── LLM Tool ─ 完整枚举：tool frequency (ChatGPT=15, Copilot=14, ...) [Table 4, §4.4]
│
├── RQ1: Methodology（方法维度簇）
│   ├── Research Strategy ─ 层级枚举：Stol & Fitzgerald taxonomy (6 values) [Table 5, §5.1]
│   │   ├── Laboratory Experiment (38%)
│   │   ├── Field Study (23%)
│   │   ├── Sample Study (15%)
│   │   ├── Experimental Simulation (13%)
│   │   ├── Field Experiment (5%)
│   │   └── Judgment Study (5%)
│   ├── Research Procedure ─ 多值枚举：Glass/Vessey/Ramesh taxonomy (5 values, mixed-method) [Table 6, §5.2]
│   │   ├── Survey (82%)
│   │   ├── User Experiment (41%)
│   │   ├── Case Study (31%)
│   │   ├── Interview (26%)
│   │   └── Concept Implementation (10%)
│   ├── Study Objective ─ 布尔/二值：Formative (59%) / Summative (41%) [§5.2, Hartson et al. taxonomy]
│   ├── Data Analysis Method ─ 层级枚举：Quantitative / Qualitative / Both [§5.2]
│   ├── Instrument Category ─ 层级枚举 3 大类 [Table 7, §5.3]
│   │   ├── Self-Reported (designed by authors)
│   │   │   ├── Surveys
│   │   │   ├── Interviews
│   │   │   └── Users' open-ended feedback
│   │   ├── Validated Instruments & Frameworks
│   │   │   ├── NASA-TLX
│   │   │   ├── SPACE Framework-Based Surveys
│   │   │   ├── TAM
│   │   │   ├── Self-Efficacy Questionnaires
│   │   │   ├── AAR/AI
│   │   │   └── Emotion Affect Questionnaire
│   │   └── Behavioral & Performance Metrics
│   │       ├── Task Completion & Correctness
│   │       ├── Suggestions Acceptance Rate
│   │       ├── Interaction Patterns
│   │       ├── Time to Completion
│   │       ├── Code Quality Metrics
│   │       ├── Productivity Gain
│   │       └── Validated Frameworks (TCQ, RBV)
│   └── Data Source Type ─ 布尔/二值：Self-reported vs Observed/Performance
│
├── RQ2: Effects（效果维度簇）
│   ├── Benefit Theme ─ 层级枚举：8 themes from thematic analysis [Table 8, §6.1]
│   │   ├── Accelerate development (§6.1.1)
│   │   ├── Minimize code search (§6.1.2)
│   │   ├── Automate trivial/repetitive tasks (§6.1.3)
│   │   ├── Support knowledge acquisition (§6.1.4)
│   │   ├── Support code-adjacent tasks (§6.1.5)
│   │   ├── Reduce task initiation overhead (§6.1.6)
│   │   ├── Improve code quality (§6.1.7)
│   │   └── Support troubleshooting/debugging (§6.1.8)
│   └── Risk Theme ─ 层级枚举：5 themes from thematic analysis [Table 9, §6.2]
│       ├── Fail to meet requirements (§6.2.1)
│       ├── Promote over-reliance and cognitive offloading (§6.2.2)
│       ├── Disrupt the flow (§6.2.3)
│       ├── Limit code quality (§6.2.4)
│       └── Reduce team collaboration (§6.2.5)
│
├── RQ3: Productivity Dimensions（维度映射簇）[Table 10, §7]
│   ├── Satisfaction (77% of studies) ─ SPACE dimension + emergent sub-dimensions
│   │   ├── Developer Experience ─ 关系值 (mapped from [46])
│   │   ├── Self-Efficacy ─ 关系值 (mapped from [19, 65])
│   │   ├── Trust ─ 关系值 (emergent from [65])
│   │   └── Cognitive Load ─ 关系值 (emergent)
│   ├── Performance (64%)
│   │   ├── Quality ─ 关系值 (mapped from [19, 65])
│   │   └── Impact ─ 关系值 (mapped from [19])
│   ├── Efficiency (59%)
│   │   ├── Temporal Efficiency ─ 关系值 (mapped from [19])
│   │   ├── Interruptions and Flow ─ 关系值 (mapped from [19, 65])
│   │   └── Automation ─ 关系值 (emergent)
│   ├── Activity (31%)
│   │   └── Activity ─ 关系值 (mapped)
│   └── Communication (26%)
│       ├── Human-LLM Collaboration ─ 关系值 (emergent)
│       └── Human-Human Collaboration ─ 关系值 (emergent)
│
├── Quality Assessment（质量维度簇）
│   ├── QA1: Is the paper based on research? ─ 3 级评分 [Table 2, §3.3]
│   ├── QA2: Clear statement of aims? ─ 3 级评分
│   ├── QA3: Adequate description of context? ─ 3 级评分
│   ├── QA4: Appropriate research design? ─ 3 级评分
│   ├── QA5: Appropriate recruitment strategy? ─ 3 级评分
│   ├── QA6: Control group? ─ 3 级评分
│   ├── QA7: Data collected to address research issue? ─ 3 级评分
│   ├── QA8: Sufficiently rigorous data analysis? ─ 3 级评分
│   ├── QA9: Researcher-participant relationship considered? ─ 3 级评分
│   ├── QA10: Clear statement of findings? ─ 3 级评分
│   └── QA11: Value for research or practice? ─ 3 级评分
│
└── Discussion Lens（讨论维度簇）[§8]
    ├── McLuhan's Tetrad Mapping ─ 外部分类法引用：Enhance / Reverse / Obsolesce / Retrieve [§8.1]
    ├── Lessons Learned ─ 自由文本加理由 [§8.1]
    ├── Recommendations for Developers ─ 自由文本加理由 [§8.2]
    ├── Recommendations for Researchers ─ 自由文本加理由 [§8.3]
    └── Threats to Validity ─ 自由文本加理由 [§9]
```

**说明**：
- RQ0/RQ1/RQ2/RQ3 的叶子字段均在原文的表格（Table 3--11）或章节（§4--§7）中有明确来源。
- 部分 sub-dimension 映射（如 SPACE 的 emergent sub-dimensions）的详细编码表在 Zenodo supplementary material 中，`paper_content.txt` 只给出了概要。
- RQ2 的 benefit/risk theme 下还有两级子主题（原文 §6.1.1--§6.1.8 和 §6.2.1--§6.2.5 的详细描述），但原文没有进一步的分类编码表，这些是定性主题分析的结果。
- Quality Metrics table（Table 11）按 study 列出 quality metrics，但未提供统一的 metrics 分类 taxonomy。
- **A2a 精核任务**：核对 Zenodo supplementary material 中的完整编码表；核对 Table 10 的 sub-dimension mapping 细节；获取 quality metrics 的分类 schema（若有）。

## 4. 叶子维度表

以下只列出代表性叶子（核心主干 + 最高信息密度叶子），完整叶子恢复是 A2a 任务。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-pub-year | 发表年份 | RQ0-Landscape | §4.1, Fig.2 | Primary study 的发表年份 | 2014--2024 integer | 数值区间 | N/A（全部有年份） | 年度频次分布、时间趋势 | 评估研究领域成熟度/爆发阶段 | EV-006 | 年份编码可迁移；具体分布不可迁移 |
| leaf-venue-category | 发表 venue 研究领域 | RQ0-Landscape | §4.3, Table 3 | 按研究焦点分 5 类的 venue 归类 | SE&CS / HCI / IS&DS / Human-Aspects / AI-SE-Edu | 层级枚举（5 类，自编） | 未知：若某 venue 无法归类 | 跨领域分布、社区参与度 | 评估跨学科关注度 | EV-006, Table 3 | 分类方法可迁移；类别系统不可迁移 |
| leaf-llm-tool | 使用的 LLM 工具 | RQ0-Landscape | §4.4, Table 4 | Primary study 中评估的 LLM-assistant | ChatGPT, Copilot, Tabnine, GPT-4, ... (完整枚举) | 完整枚举 | 未知：部分 study 工具未明确定名 | 工具使用热图 | 分析工具生态与偏移 | EV-006, Table 4 | 不可迁移（不同领域工具不同） |
| leaf-strategy | 研究策略 | RQ1-Methodology | §5.1, Table 5 | Stol & Fitzgerald [50] taxonomy | Lab Experiment / Field Study / Sample Study / Experimental Simulation / Field Experiment / Judgment Study | 层级枚举（6 类） | 未知：若研究设计无法归类 | 方法类型分布、研究严谨度 | 证据强度分层（lab vs field） | EV-007, Table 5 | taxonomy 可迁移为方法学编码种子 |
| leaf-procedure | 研究过程 | RQ1-Methodology | §5.2, Table 6 | Glass/Vessey/Ramesh [51] taxonomy | Survey / User Experiment / Concept Implementation / Interview / Case Study | 层级枚举（5 类），允许多选 | 未知：若过程描述不清 | 方法频次、方法组合分析 | 证据三角验证程度评估 | EV-008, Table 6 | taxonomy 可迁移 |
| leaf-objective | 研究目标类型 | RQ1-Methodology | §5.2, Hartson et al. [52] | Formative vs Summative | Formative (59%) / Summative (41%) | 布尔/二值 | 未知：若目标不明确 | 研究阶段分布 | 评估领域成熟度 | EV-008 | 二值分类可迁移 |
| leaf-data-analysis | 数据分析方法 | RQ1-Methodology | §5.2 | 定量/定性/混合 | Quantitative / Qualitative / Both | 层级枚举（3 类） | 未知 | 分析方法分布 | 证据类型多样性 | EV-008 | 可迁移 |
| leaf-instrument-category | 评价工具类别 | RQ1-Methodology | §5.3, Table 7 | 3 大类评价工具 | Self-Reported / Validated Instruments / Behavioral & Performance Metrics | 层级枚举（3 类） | 未知：若使用非标工具 | 工具类别频次 | 证据可靠性（validated vs ad-hoc） | EV-009, Table 7 | 分类逻辑可迁移 |
| leaf-instrument-nasa-tlx | 是否使用 NASA-TLX | RQ1-Methodology | §5.3, Table 7 | 使用 NASA-TLX 测量认知负荷 | Yes / No | 布尔 | No = 未使用或未报告 | 验证工具使用率 | 认知负荷证据强度 | EV-009 | 不可迁移（领域特定） |
| leaf-instrument-accept-rate | 是否使用接受率指标 | RQ1-Methodology | §5.3, Table 7 | 是否使用 suggestion acceptance rate | Yes / No | 布尔 | No = 未使用或未报告 | 行为指标使用率 | — | EV-009 | 可迁移为行为指标种子 |
| leaf-benefit-theme | 收益主题 | RQ2-Effects | §6.1, Table 8, Fig.6 | Thematic analysis 所得收益主题 | 8 个枚举主题 | 层级枚举（8 类），允许多值 | 未知：某 study 可能报告额外收益但未被主题覆盖 | 收益频次分布、主题热度 | 候选发现：LLM-assistant 主要收益集中在哪些方面 | EV-010, Table 8 | 主题分析方法可迁移；具体主题不可迁移 |
| leaf-risk-theme | 风险主题 | RQ2-Effects | §6.2, Table 9, Fig.6 | Thematic analysis 所得风险主题 | 5 个枚举主题 | 层级枚举（5 类），允许多值 | 未知：同上 | 风险频次分布、主题热度 | 候选发现：LLM-assistant 主要风险集中在哪些方面 | EV-011, Table 9 | 同上 |
| leaf-space-satisfaction | SPACE: 满意度 | RQ3-SPACE | §7, Table 10 | 是否纳入 Satisfaction dimension | Yes / No + sub-dimensions | 布尔 + 关系值 (sub-dim) | No = 未考察满意度 | 维度覆盖率 (77%) | 候选发现：满意度是最常研究的维度 | EV-012, Table 10 | SPACE 框架可迁移；覆盖率数字不可迁移 |
| leaf-space-performance | SPACE: 绩效 | RQ3-SPACE | §7, Table 10 | 是否纳入 Performance dimension | Yes / No + sub-dimensions | 布尔 + 关系值 | No = 未考察绩效 | 维度覆盖率 (64%) | — | EV-012 | 同上 |
| leaf-space-efficiency | SPACE: 效率 | RQ3-SPACE | §7, Table 10 | 是否纳入 Efficiency dimension | Yes / No + sub-dimensions | 布尔 + 关系值 | No = 未考察效率 | 维度覆盖率 (59%) | — | EV-012 | 同上 |
| leaf-space-activity | SPACE: 活动 | RQ3-SPACE | §7, Table 10 | 是否纳入 Activity dimension | Yes / No | 布尔 | No = 未考察活动 | 维度覆盖率 (31%) | gap: Activity underexplored | EV-012 | 同上 |
| leaf-space-communication | SPACE: 沟通 | RQ3-SPACE | §7, Table 10 | 是否纳入 Communication dimension | Yes / No + sub-dimensions | 布尔 + 关系值 | No = 未考察沟通 | 维度覆盖率 (26%) | gap: Communication underexplored | EV-012 | 同上 |
| leaf-qa-score | QA 评分 | QA | §3.3, Table 2 | 11 条 QA criteria，每条 0/0.5/1 | 0--1 连续值（实际为 3 级） | 数值区间（3 级评分） | 缺失需记录原因 | 证据质量加权 | 证据强度分层 | EV-004, Table 2 | QA 方法可迁移；具体 criteria 需适配领域 |
| leaf-dim-count | 研究覆盖维度数 | RQ3-SPACE | §7 | 单篇 study 覆盖的 SPACE 维度数 | 1--5 integer | 数值区间 | N/A | 多维覆盖分布 | 候选发现：90%≥2 dim, 仅 15%≥4 dim | EV-012 | 可迁移为维度覆盖分析模式 |

**缺失部分说明**：上表未穷尽原文所有叶子，以下叶子需 A2a 精核补充：
- Table 10 中每个 SPACE sub-dimension 与 primary study 的精确映射（当前只知百分比，不知每个 study 的 [PSn] 编码）
- Table 11 中 quality metrics 按 study 的详细列表（text 提取可能不完整）
- Zenodo supplementary material 中的完整 exclusion decision 表和详细 classification 表

## 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| edge-study-strategy | Primary Study [PSn] | has_strategy | Research Strategy leaf | 6 类枚举 | N/A | Table 5 | 每篇 study 的方法论策略归类 |
| edge-study-procedure | Primary Study [PSn] | uses_procedure (1:N) | Research Procedure leaf | 5 类枚举，多值 | N/A | Table 6, Fig.4 | 每篇 study 的方法论过程归类，支持 overlap 分析 |
| edge-study-instrument | Primary Study [PSn] | uses_instrument (1:N) | Instrument leaf | 自报/验证/行为 | N/A | Table 7 | 每篇 study 使用的评价工具 |
| edge-study-benefit | Primary Study [PSn] | reports_benefit (1:N) | Benefit Theme leaf | 8 类枚举，多值 | N/A | Table 8, Fig.6 | 每篇 study 报告的收益主题 |
| edge-study-risk | Primary Study [PSn] | reports_risk (1:N) | Risk Theme leaf | 5 类枚举，多值 | N/A | Table 9 | 每篇 study 报告的风险主题 |
| edge-study-space | Primary Study [PSn] | mapped_to_space (1:N) | SPACE Dimension leaf | 5 维 + sub-dim，多值 | N/A | Table 10 | 每篇 study 覆盖的 productivity dimension |
| edge-study-qa | Primary Study [PSn] | scored_on_qa | QA Score leaf | 0--1 连续 | N/A | Table 2 | 每篇 study 的质量评分 |
| edge-strategy-instrument | Research Strategy leaf | correlates_with | Instrument Category leaf | 关联关系 | N/A | §5.3 Fig.5 | 研究策略与评价工具的关联模式 |
| edge-procedure-objective | Research Procedure leaf | associated_with | Study Objective leaf | 关联关系 | N/A | §5.2 | 方法过程与研究目标的关联 |
| edge-benefit-risk-contradiction | Benefit Theme "Improve code quality" | contradicted_by | Risk Theme "Limit code quality" | 矛盾关系 | N/A | §6.1.7, §6.2.4, RQ2 summary | code quality 的双重证据：既是收益也是风险 |
| edge-finding-dimension-gap | SPACE Communication leaf | identified_as_gap | Discussion: Research Gaps | gap & recommendation | N/A | §8.3 | 维度覆盖缺口→研究建议 |
| edge-mcluhan-tetrad | Benefit/Risk Theme leaves | synthesized_through | McLuhan's Tetrad lens | Enhance/Reverse/Obsolesce/Retrieve | N/A | §8.1, Fig.9 | 用外部理论框架综合 benefit/risk 发现 |

**说明**：原文有明确的关系型 schema（多对多映射表如 Table 5/6/7/8/9/10），但没有显式的"关系边"概念。上表的 `edge-*` 是从原文表格结构中推导出的关系语义。

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 原文的统计观察（Statistics from coded tables）

| # | 统计观察 | 来源 | 统计类型 |
|---|---|---|---|
| S-01 | 77% studies published in 2024; only 4 studies pre-2022 | §4.1, Fig.2 | 年度频次分布 |
| S-02 | 46% venues in SE & CS; 18% in HCI | §4.3, Table 3 | 分类频次 |
| S-03 | ChatGPT (15) and Copilot (14) most evaluated | §4.4, Table 4 | 工具频次 |
| S-04 | Lab experiment most common strategy (38%) | §5.1, Table 5 | 分类频次 |
| S-05 | Survey most used procedure (82%); 69% mixed-method | §5.2, Table 6 | 分类频次 + 组合 |
| S-06 | 59% formative / 41% summative | §5.2 | 二值比例 |
| S-07 | 67% mixed quantitative+qualitative analysis | §5.2 | 分类频次 |
| S-08 | Benefit themes: "Accelerate development" most reported (24 studies) | §6.1, Table 8, Fig.6 | 主题频次 |
| S-09 | Risk themes: "Fail to meet requirements" most reported (20 studies) | §6.2, Table 9 | 主题频次 |
| S-10 | Code quality reported as both benefit (7 studies) and risk (multiple studies) | §6.1.7, §6.2.4 | 矛盾证据 |
| S-11 | Satisfaction most studied SPACE dim (77%), Communication least (26%) | §7, Table 10 | 维度覆盖率 |
| S-12 | 90% studies cover ≥2 SPACE dim; 15% cover ≥4 dim | §7 | 多维覆盖分布 |
| S-13 | Only 44% examine ≥3 SPACE dimensions | §7 | 阈值比例 |
| S-14 | Most co-occurring combination: Satisfaction-Performance-Efficiency (5 studies) | §7, Fig.8 | 组合频次 |

### 6.2 原文 discussion / recommendation 提出的候选 finding

| # | 候选 finding | 来源 | 类型 |
|---|---|---|---|
| CF-01 | Productivity gains are task-contingent, strongest for well-scoped and repetitive activities | §8.1 Lessons Learned | synthesis claim |
| CF-02 | Uncritical reliance introduces diminishing returns through validation overhead and erosion of reflective practice | §8.1 Lessons Learned | synthesis claim |
| CF-03 | LLM-assistants reshape, not replace, developer expertise—shifting effort toward evaluation, judgment, and coordination | §8.1 Lessons Learned | synthesis claim |
| CF-04 | Trust is fragile: excessive trust → automation complacency; insufficient trust → underutilization | §8.2 | recommendation-derived |
| CF-05 | Developer role is shifting from coder to reviewer (>50% time in evaluation) | §8.2 | observation → claim |
| CF-06 | Code quality outcome is unresolved: studies report contradictory results contingent on context and evaluation criteria | §6, §10 Conclusion | contested finding |
| CF-07 | Communication and human-human collaboration are underexplored | §7, §8.3 | research gap |
| CF-08 | Lack of longitudinal and team-based evaluations in existing studies | §6.2, §10 | research gap |
| CF-09 | Well-being is not examined by any empirical study | §7 (under Satisfaction) | research gap |
| CF-10 | LLM-assistants are reshaping traditional information-seeking—developers shifting from Stack Overflow to ChatGPT | §6.1.2, §8.1.3 | observation → claim |

### 6.3 对 Paper2 的方法学启发（可迁移）

| # | 可迁移启发 | 迁移方式 |
|---|---|---|
| M-01 | RQ0→RQ3 的分层组织模式：先 landscape → 再 method → 再 effects → 再 dimension mapping | 直接用作 Paper2 的 RQ 结构模板 |
| M-02 | 外部 taxonomy + emergent sub-dimensions 的混合编码策略 | 用于设计 A1-M2 字段审批机制 |
| M-03 | benefit/risk 双主题台帐模式 | 用于 Paper2 candidate finding ledger |
| M-04 | SPACE 维度映射作为跨 study 综合镜头 | 用于 A1-M4/M5 字段抽取与统计分析 |
| M-05 | PRISMA flow + exclusion code log | 用于 Paper2 审计制品链 |
| M-06 | Quality assessment 不淘汰论文但用于证据分层 | 用于 Paper2 证据强度分层 |

### 6.4 绝不能迁移的领域结论

| 不可迁移项 | 原因 |
|---|---|
| "LLM-assistants accelerate development" | 领域特定结论 |
| benefit/risk 主题的具体内容和频次 | 来自 developer productivity 领域的 primary studies |
| SPACE 维度覆盖率的百分比数据 | 来自不同的 primary study 语料 |
| ChatGPT/Copilot 等工具使用分布 | 领域特定、时间敏感 |
| "Satisfaction is most studied dimension (77%)" | 领域特定统计 |

## 7. 对现有 `review.md` 的返修建议

### 7.1 总体评估

现有 `review.md` 质量较高，捕捉了论文的核心结构和 RQ 组织逻辑。但存在以下需要修正的问题：

### 7.2 C 级（Critical：阻塞统计池资格或维度树正确性）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| C-01 | **样本单位描述不够精确**。现有 review 只在"综述类型"行写"SLR + SMS；39 篇"，但没有在维度树或 SUMMARY 中显式命名"样本单位 = peer-reviewed primary study"。 | §1 快速结论卡片；维度树复原 | 在 SUMMARY 表中补：`样本单位 = peer-reviewed primary study`，并注明 39 vs 44 的区分。 |
| C-02 | **维度树不是"复原"**。现有 review 的"维度树复原"和 A.1--A.4 包含大量 A1 scaffold projection（如 `clm-*` claims），与原文自己的编码表混淆。维度树应该是 paper's own schema，而不是我们套上去的 observation tree。 | 维度树复原 + A.1--A.4 | 用本审计 §3 的多视图维度森林替换现有维度树；将现有的 `clm-*` 和 scaffold 内容降级为 "A1 seed projection"（独立于原生树）。 |
| C-03 | **统计池资格元数据需补字段**。现有 SUMMARY 表缺少"样本单位"和"原生树类型"两个关键字段。 | SUMMARY 表 | 补：`样本单位 = peer-reviewed primary study`、`原生树类型 = 维度森林（多表多分类框架）`、`统计池资格 = 是`。 |

### 7.3 I 级（Important：影响 cross-paper synthesis 或 leaf 语义清晰度）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| I-01 | **"通用六叶"残影**。A.1 的叶子维度表中虽有 19 个 leaf，但其中 `leaf-orig-*` 的 5 个叶子（assistant-type, developer-task, productivity-outcome, evaluation-design, human-factor）是 A1 scaffold projection 而不是原文 schema。原文没有按这些维度编码 primary studies。 | A.1--A.3 | 区分两套叶子系统：(a) paper-native leaves（来自 Table 3--11 和 §4--§7），(b) A1-cross-paper projection leaves（用于跨论文比较）；后者标注 `schema_seed` 且不进入原生树统计。 |
| I-02 | **SPACE 维度被当作"原生维度"**。SPACE 是外部 productivity framework，作者用它作为综合镜头（§7），而不是 primary study 的编码对象。现有 review 把 `leaf-space-*` 当成 paper-native leaf，但没有说明它是"外部框架映射"而非"原文自产分类"。 | §4 叶子维度表；A.2 | 在叶子维度表中明确标注 SPACE 维度的来源是 [19] Forsgren et al. 的外部框架，取值空间是"外部分类法引用"。 |
| I-03 | **RQ 与维度的关系未澄清**。现有 review §2.2 正确描述了 RQ0--RQ3 的组织逻辑，但维度树中没有体现"每个 RQ 是一个视图/维度簇，不是一个 node"。 | 维度树复原 | 采用本审计 §3 的分簇结构，根为 Primary Studies，下面分 RQ0/RQ1/RQ2/RQ3/QA/Discussion 子簇。 |
| I-04 | **缺失 benefit/risk 叶子行**。叶子维度表中没有 benefit theme 和 risk theme 叶子（Table 8, 9 的 8+5 主题）。 | §4 叶子维度表 | 补充 `leaf-benefit-theme` 和 `leaf-risk-theme` 行。 |
| I-05 | **缺失关系边表**。现有 review 没有关系边表（§5），但原文有明确的多对多映射结构（Table 5/6/7/8/9/10 的 study-to-category 映射）。 | — | 补充关系边表（参考本审计 §5），标注 evidence_type = `mapping_table`。 |

### 7.4 M 级（Minor：措辞、精度或可维护性）

| # | 问题 | 位置 | 建议 |
|---|---|---|---|
| M-01 | "39 篇 peer-reviewed studies" vs "44 篇进入 QA" 的区分未说明。 | §1 快速结论卡片 | 加注：snowballing 后 44 篇进入 QA，但 QA 不淘汰，最终报告基数仍为 39。 |
| M-02 | A.2 evidence anchor 中多处引用 "§2.1 §2.2" 等过于泛泛。 | A.2 | 改为精确锚点如 §5.1 Table 5, §6.1.1 等。 |
| M-03 | A.4 的 `needs_manual_check` 状态应注明具体待核验项。 | A.4 | 细化：Table 10 sub-dimension mapping, Zenodo supplementary details, PDF 版面 Table 1--11 核对。 |
| M-04 | review.md 的"历史草稿（已迁移）" section 与正文重叠，可以删除或压缩。 | 文末 | 删除或压缩为 1 行引用。 |

## 8. 审计附录草案：证据账本与结论映射

### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-llmprod-001 | paper_content.txt | §3.1 | Table 1 "Database search strings and results. Total n=9,756" | 六库检索、3段 AND 搜索式、proximity operators | method_protocol | strong | 纳入流程完整性 | 是（文本提取的 Table 1 可能丢失跨页列结构） | 特定于 developer productivity 检索词 |
| EV-llmprod-002 | paper_content.txt | §3.1.2 | "17 control papers" | Pre-review mapping 识别控制论文用于验证搜索式 | method_protocol | strong | 搜索式验证 | 否 | SLR best practice，可跨领域复用 |
| EV-llmprod-003 | paper_content.txt | §3.1.1 | IC1--IC3, EC1--EC5 | 5 纳入 + 5 排除标准 | method_protocol | strong | 纳排标准完整性 | 否 | EC3 "排除 secondary studies" 是本 survey-of-surveys 的关键边界 |
| EV-llmprod-004 | paper_content.txt | §3.2, Fig.1 | PRISMA flow: n=9756→8953→228→39→44→39 | 完整筛选链与分母 | method_protocol | strong | 样本分母 | 是（Fig.1 PRISMA 图需 PDF 核对） | denominators 不可迁移 |
| EV-llmprod-005 | paper_content.txt | §3.3, Table 2 | QA1--QA11 (Lenarduzzi et al. [48]) | 11 条质量评价标准及评分规则 | quality_instrument | strong | QA schema | 是（Table 2 文本提取核对） | QA criteria 可迁移适配 |
| EV-llmprod-006 | paper_content.txt | §3.4 | "study goals, tools, empirical strategy and design, tasks, settings, and key results" | 原文数据抽取字段列表 | extraction_form | medium | 字段层级 | 否 | 字段列表可参考，需适配目标领域 |
| EV-llmprod-007 | paper_content.txt | §4, Table 3 | venue 5-category research focus classification | 自编 venue 分类系统 | classification | medium | leaf-venue-category | 是（Table 3 版式核对） | 分类体系特定于本文 |
| EV-llmprod-008 | paper_content.txt | §4, Table 4 | LLM tool frequency table | 39 篇 study 使用的 LLM 工具频次 | classification | strong | leaf-llm-tool | 是 | 不可迁移（领域特定） |
| EV-llmprod-009 | paper_content.txt | §5.1, Table 5 | Stol & Fitzgerald [50] taxonomy | 6-category research strategy 分类 | external_taxonomy | strong | leaf-strategy | 是 | taxonomy 可迁移，分布不可迁移 |
| EV-llmprod-010 | paper_content.txt | §5.2, Table 6 | Glass/Vessey/Ramesh [51] taxonomy | 5-category procedure, mixed-method allowed | external_taxonomy | strong | leaf-procedure | 是 | 同上 |
| EV-llmprod-011 | paper_content.txt | §5.3, Table 7 | 3 instrument categories with detail rows | Self-reported / Validated / Behavioral&Performance | classification | strong | leaf-instrument-* | 是 | 分类逻辑可迁移 |
| EV-llmprod-012 | paper_content.txt | §6.1, Table 8 | 8 benefit themes with study mapping | Thematic analysis results | thematic_analysis | medium | leaf-benefit-theme | 是 | 主题内容不可迁移 |
| EV-llmprod-013 | paper_content.txt | §6.2, Table 9 | 5 risk themes with study mapping | Thematic analysis results | thematic_analysis | medium | leaf-risk-theme | 是 | 同上 |
| EV-llmprod-014 | paper_content.txt | §7, Table 10 | SPACE 5 dim + 11 sub-dim with % | SPACE framework mapping | external_framework_mapping | strong | leaf-space-* | 是（sub-dim 细节需 PDF/Zenodo 核对） | SPACE 框架可迁移 |
| EV-llmprod-015 | paper_content.txt | §7, Table 11 | Quality metrics by study | 每篇 study 的质量指标映射 | classification | medium | — | 是（text 提取版可能不完整） | 指标分类可参考 |
| EV-llmprod-016 | paper_content.txt | §9 | Threats to validity: selection/search/repeatability/classification/temporal | 5 类威胁及 mitigation | validity_threats | medium | — | 否 | 威胁分类框架可迁移 |

### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CONC-llmprod-001 | 本文是标准 SLR+SMS，有完整检索/纳排/QA/编码链 | method_classification | method_protocol | EV-llmprod-001 to EV-llmprod-005 | strong | 标记为 statistical_pool eligible | — |
| CONC-llmprod-002 | 样本单位 = peer-reviewed primary study，最终 n=39 | sample_definition | sample_unit | EV-llmprod-004 | strong | 统计池分母 | 需区分 39（最终）vs 44（QA 前） |
| CONC-llmprod-003 | 原生维度树是"维度森林"：多表多分类框架并存 | schema_type | native_dimension_tree | EV-llmprod-007 to EV-llmprod-015 | strong | 维度树复原 | 不是单树；需分簇表达 |
| CONC-llmprod-004 | RQ0--RQ3 构成分层视图：landscape → method → effects → dimension mapping | rq_organization | RQ structure | EV-llmprod-006 | strong | Paper2 RQ 结构模板 | 不能把 RQ 数量固定为 4 |
| CONC-llmprod-005 | SPACE 是外部生产力框架，作者用它作为综合镜头 | framework_usage | leaf-space-* | EV-llmprod-014 | strong | 跨论文维度映射模式参考 | SPACE 只适用于 productivity 主题 |
| CONC-llmprod-006 | Code quality 是 contested finding：同时报告为 benefit 和 risk | contested_finding | leaf-benefit-theme, leaf-risk-theme | EV-llmprod-012, EV-llmprod-013 §6.1.7 §6.2.4 | strong | candidate finding 台账模式 | 不能直接迁移为"LLM 改善/损害代码质量" |
| CONC-llmprod-007 | 现有研究多为 formative/lab/short-term，缺乏 longitudinal/team-based 评价 | research_gap | method leaves | EV-llmprod-009, EV-llmprod-010 | medium | gap identification 模式 | gap 内容领域特定 |
| CONC-llmprod-008 | 本文的 benefit/risk 双主题台账 + external framework mapping 模式可迁移为 Paper2 方法学 | method_transfer | full_schema | all EV items | medium | Paper2 method design seed | 具体主题/框架不可迁移 |
| CONC-llmprod-009 | 现有 review.md 将 A1 scaffold projection 混入原生维度树 | review_diagnosis | existing_review | 本审计 §7 | strong | 返修建议 | 需本审计主线程确认后执行 |

## 9. 技能使用与自我审查记录

### 9.1 读取的技能文件

| 技能文件 | 状态 | 采用的原则 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | ✅ 已读 | Evidence gate：没有证据就降级；Citation gate：不编造引用 |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | ✅ 已读 | Universal review dimensions (Originality/Quality/Clarity/Significance/Reproducibility)；Constructive Specificity Standard |
| `ai-research-writing-skill/references/reviewer-self-review.md` | ✅ 已读 | Five-Dimension Review scoring；Claim Audit；Adversarial Questions |
| `research-planning/SKILL.md` | ✅ 已读 | 基本规划流程参考 |
| `research-planning/references/planning-prompts.md` | ✅ 已读 | Paper2Code 4-turn structure 参考 |
| `research-planning/references/output-schemas.md` | ✅ 已读 | Plan schema 格式参考 |
| `autoresearch/SKILL.md` | ✅ 已读 | Validator-gated 完成判断、completion artifact contract |

### 9.2 最高风险 3 点（reviewer 视角）

| # | 风险 | 说明 | 主线程合并时如何复核 |
|---|---|---|---|
| **R1** | **现有 review.md 维度树与原文字段之间存在混淆风险**。review.md 中 `leaf-orig-*` 系列叶子（assistant-type, developer-task, productivity-outcome, evaluation-design, human-factor）是 A1 cross-paper projection，不是原文编码。合并时必须将两者分层：paper-native leaves vs cross-paper projection。 | 对比本审计 §3 的维度森林与 review.md 现有的维度树复原；凡是 paper_content.txt 中找不到明确字段表的叶子降级为 `schema_seed`。 |
| **R2** | **Zenodo supplementary material 未读取**。原文大量细节（exclusion decisions, detailed classification, SPACE sub-dimension mapping detail）在 supplementary 中。当前审计基于 `paper_content.txt`，Table 10/11 等细节可能不完整。 | 如果 A2a 计划精核此论文，应从 Zenodo DOI 下载 supplementary 并交叉验证 Table 10 的 sub-dimension mapping。如无法获取，标注 `not_verified`。 |
| **R3** | **"无系统样本库"的边界论文可能影响统计池聚合规则**。本文 clearly pass，但如果 survey_of_surveys 中混入 roadmap/proposal/guideline 论文，其统计池聚合逻辑需要与本文的 SLR/SMS 统计池区分。 | 在 Paper2 SUMMARY 中增加"统计池资格"字段分表（eligible / partial / excluded），确保只有 eligible papers 进入主统计。 |

### 9.3 Blocked / Timeout / 文件缺失

| 项 | 状态 |
|---|---|
| PDF 版面核验 | 未完成（未打开 `paper.pdf`）；记录为 `needs_manual_check` |
| Zenodo supplementary material | 未读取；记录为 `A2a 精核入口` |
| 所有 6 个技能文件 | 均成功读取，无 blocked |
| 所有 paper 文件 | 均成功读取（bibtex, metadata, content, review） |
| 本审计输出完整性 | 所有 9 节均已完成 |

---

**审计完成时间**：2026-06-30
**审计 agent**：deepseek (via codex-deepseek exec)
**审计范围**：单篇 `llm-assistants-developer-productivity`
**下一动作**：等待主线程合并本审计报告，执行 C-01/C-02/C-03 和 I-01--I-05 返修