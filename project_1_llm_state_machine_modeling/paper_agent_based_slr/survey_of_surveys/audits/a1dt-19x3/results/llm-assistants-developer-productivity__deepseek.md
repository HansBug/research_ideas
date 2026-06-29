# llm-assistants-developer-productivity · deepseek 全文审计报告

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
- **是否完整阅读 `paper_content.txt`**：是。覆盖范围：全文 1842 行，从 Page 1 标题/摘要/Introduction 到 Page 43 参考文献末尾；涵盖 §1 Introduction、§2 Background & Related Work、§3 Method（含检索式、纳排标准、控制论文、质量评价、数据抽取表单）、§4 RQ0 Results、§5 RQ1 Results、§6 RQ2 Results（含 8 类 benefit + 5 类 risk 主题）、§7 RQ3 Results（含 SPACE 五维 + sub-dimensions）、§8 Discussion（含 Tetrad 框架与 practitioner/researcher recommendations）、§9 Threats to Validity、§10 Conclusion、参考文献和全部 PS 标识主研究列表。
- **是否核对 `paper.pdf`**：否。当前为纯文本级审计，未打开 PDF 逐页核对 Table 1--11、Fig. 1--9 的精确页码、版式和数值。「图表待人工核对」这一限制适用于本报告全部表图级判断；若后续发现 PDF/ACM 正式版与文本提取版存在差异，相关结论需相应降级。

---

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

**目标**：系统综合 LLM-assistants 对软件开发者生产力的影响，提供该方向的第一个系统综述与映射研究（SLR + SMS）。

**研究问题**（原文 §3 显式列出，§4--§7 逐 RQ 回答）：

| RQ | 原文措辞（摘录） | 承载层级 |
|---|---|---|
| RQ0 | What are the characteristics of peer-reviewed studies that investigate the impact of LLM-assistants on software developer productivity? | 研究景观：年份、作者、venue、工具分布 |
| RQ1 | What are the methodological strategies, procedures, and instruments used by peer-reviewed studies that investigate the impact of LLM-assistants on software developer productivity? | 方法实践：策略（Stol & Fitzgerald taxonomy）、程序、研究目标、分析类型、评价工具/指标 |
| RQ2 | What is the impact of LLM-assistants on software developer productivity reported in the reviewed studies? | 效果综合：主题分析得出 8 类 benefit + 5 类 risk，含 contested finding（code quality 同时为 benefit 和 risk） |
| RQ3 | To what extent do the reviewed studies examine the different dimensions of developer productivity? | 维度覆盖：以 SPACE 框架为 lens 统计各维度覆盖，识别 underexplored 维度 |

**贡献声明**（摘要 + §1 Introduction）：
1. 首个综合 LLM-assistants 对 developer productivity 影响的 SLR + SMS。
2. 揭示 productive benefits 与 critical risks 并存。
3. 发现 code quality 是否为 benefit 存在矛盾证据。
4. 用 SPACE 框架映射维度覆盖与缺口。
5. 提出面向实践者和研究者的建议。
6. 公开全部 artifact（Zenodo replication package）。

### 2.2 原文方法流程

**检索与纳排**（§3.1）：
- 数据库：ACM DL、IEEE Xplore、Scopus、Web of Science、arXiv。
- 时间窗：2014-01 至 2024-12。
- 检索式：经多轮迭代，以 control papers 验证召回。
- 筛选：47 天 title/abstract screening；10 周 full-text screening。
- 最终纳入：39 篇 primary studies。
- 前向/后向 snowballing。
- PRISMA-style flow diagram（Fig. 1）。

**质量评价**（§3.5）：
- 质量评价标准（quality assessment criteria），从 Kitchenham & Charters 改编。
- 评分（QA scores），用于评估纳入研究的 rigor。

**数据抽取**（§3.2）：
- 显式 data extraction form，覆盖字段包括：study metadata、research strategy（Stol & Fitzgerald taxonomy）、research procedure、research objective（formative/summative）、analysis type（quantitative/qualitative/mixed）、data collection instruments、evaluation metrics、LLM tools evaluated、developer tasks、reported impacts（benefits/risks）、SPACE dimensions。

**编码与分类**（§3.3--§3.4 + §5--§7）：
- 研究策略分类：Stol & Fitzgerald 的 6 类 taxonomy（Field Study、Field Experiment、Experimental Simulation、Laboratory Experiment、Sample Study、Judgment Study）。
- 研究程序分类：5 类 taxonomy（Survey、User Experiment、Concept Implementation、Interview、Case Study）。
- 研究目标：Formative / Summative。
- 分析类型：Quantitative / Qualitative / Mixed。
- 工具与指标枚举（原文 Table 7）：self-reported instruments（自设 + validated instruments 如 NASA-TLX、SPACE-based、TAM、self-efficacy、AAR/AI、emotion affect）、behavioral/performance metrics（task completion/correctness、acceptance rate、interaction logs、time to completion、code quality metrics、productivity gain）、econometric frameworks（TCQ、RBV）。
- 效益/风险主题分析：8 类 benefit + 5 类 risk，编码过程见 §3.3。
- SPACE 维度映射（§7）：Satisfaction（experience、self-efficacy、trust、cognitive load；well-being 未覆盖）、Performance（quality、impact）、Activity（action/task counts）、Communication（human-LLM、human-human）、Efficiency（temporal、automation、interruptions/flow）。

**发现形成方式**：
- 每个 RQ 内有独立结果表/图 → 分类/频次统计 → 解释 → RQ summary（含数字 + 主导模式 + gap）。
- Discussion（§8）超越单 RQ，用 McLuhan's Tetrad 框架做 socio-technical synthesis，然后给出 practitioner recommendations（5 类）和 researcher recommendations（3 大方向）。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

| 原文结构 | 原文位置 | 具体内容 |
|---|---|---|
| **Explicit extraction form** | §3.2 | 11 个以上字段：study metadata、strategy、procedure、objective、analysis type、instruments、metrics、LLM tools、developer tasks、impacts、SPACE dimensions |
| **Stol & Fitzgerald taxonomy (strategy)** | §5.1 Table 5 | 6 类：Field Study、Field Experiment、Experimental Simulation、Laboratory Experiment、Sample Study、Judgment Study |
| **Procedure taxonomy** | §5.2 Table 6 | 5 类：Survey、User Experiment、Concept Implementation、Interview、Case Study |
| **Instruments & metrics** | §5.3 Table 7 | 3 大类 + validated instrument 枚举（NASA-TLX、SPACE-based、TAM、self-efficacy、AAR/AI、emotion affect）+ behavioral metrics 枚举 |
| **Benefit categories** | §6.1 Table 8 | 8 类：Accelerate development、Minimize code search、Automate trivial tasks、Support knowledge acquisition、Support code-adjacent tasks、Reduce task initiation overhead、Improve code quality、Support debugging/troubleshooting |
| **Risk categories** | §6.2 Table 9 | 5 类：Fail to meet requirements、Promote over-reliance and cognitive offloading、Disrupt the flow、Limit code quality、Reduce team collaboration |
| **SPACE framework** | §7 | 5 dimensions + sub-dimensions；Satisfaction（4 sub）、Performance（2 sub）、Activity（1）、Communication（2 sub）、Efficiency（3 sub） |
| **Quality assessment** | §3.5 | QA criteria + QA scores |
| **Contradictory finding: code quality** | §6.1 Table 8 + §6.2 Table 9 + §6.2.4 | 明示 code quality 同时出现在 benefit 和 risk，并讨论 context/metric/task 差异解释 |
| **PRISMA-style flow diagram** | Fig. 1 | 检索、筛选、纳入流程及分母 |
| **Tetrad discussion framework** | §8 | 4 维 socio-technical interpretation：Enhance、Reverse、Obsolesce、Retrieve |
| **Practitioner recommendations** | §8 | 5 类：校准信任、从 coder 到 reviewer、调整 workflow、组织 adoption strategy、专业伦理 |
| **Researcher recommendations** | §8 | 3 大方向：shared frameworks + validated instruments + longitudinal/field studies；multidimensional evaluation；confounding variables + replication |
| **Replication package** | §1 + §10 | Zenodo：https://zenodo.org/records/18489222（含 study data、selection decisions、exclusion rationales、supplemental appendix） |

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

路径如下：

1. 每个 RQ 内：**表格/图 → 频次/分布统计 → 文字解释 → RQ summary**。例如 RQ1：Table 5（strategy 分布）→ "Laboratory experiment 38%, field study 23%" → 解释为 "strong internal validity but limited ecological validity" → RQ1 summary。
2. RQ2 特别：**主题分析 → benefit/risk 分类表 → 每个主题的 sub-analysis（含引用特定 PS 编号的证据句）→ 识别 contested themes（code quality）**。
3. RQ3：**外部框架（SPACE）映射 → 维度覆盖频次统计 → 维度组合分析 → 覆盖缺口**。
4. Discussion：**跨 RQ 综合（Tetrad） → 面向实践者的行动建议 → 面向研究者的方向建议**。
5. 每个 recommendation 编号并绑定到具体 RQ 发现。

---

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树全貌

review.md §"维度树复原" 给出的维度树结构如下：

```
[dim-llm-assistants-developer-productivity-root]
├── [dim-llm-assistants-developer-productivity-b1] 综述范围与研究问题
│   └── [leaf-llm-assistants-developer-productivity-scope] 研究范围与单位对象
├── [dim-llm-assistants-developer-productivity-b2] 语料收集与纳排
│   └── [leaf-llm-assistants-developer-productivity-corpus] 语料与纳排链条
├── [dim-llm-assistants-developer-productivity-b3] 主题 / 对象分类
│   └── [leaf-llm-assistants-developer-productivity-taxonomy] 主题与维度分类
├── [dim-llm-assistants-developer-productivity-b4] 方法 / 技术 / 干预
│   └── [leaf-llm-assistants-developer-productivity-method] 方法 / 技术 / 干预分类
└── [dim-llm-assistants-developer-productivity-b5] 评价、统计与候选发现
    ├── [leaf-llm-assistants-developer-productivity-evidence] 评价、证据与复现资产
    └── [leaf-llm-assistants-developer-productivity-finding] 统计观察与候选发现
```

另在 CLM C12 中列出「原文模式候选叶子映射（A1 种子）」5 个候选叶：
- `[leaf-llm-assistants-developer-productivity-orig-assistant-type]`
- `[leaf-llm-assistants-developer-productivity-orig-developer-task]`
- `[leaf-llm-assistants-developer-productivity-orig-productivity-outcome]`
- `[leaf-llm-assistants-developer-productivity-orig-evaluation-design]`
- `[leaf-llm-assistants-developer-productivity-orig-human-factor]`

review.md 自身在 CLM C12 中坦诚声明："当前候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。"

review.md §"A1-DT 叶子层口径校准" 也声明："下方'叶子维度表'的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。"

### 3.2 审计矩阵

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| **根节点是否准确** | 通过 | 根节点正确指向论文全文，子节点 b1--b5 覆盖综述的五大关注面。根节点定义、取值空间、证据源和用途声明在 review.md 行 335--339 中完整。 | 通过 |
| **主干分支是否覆盖原文 schema** | **不完整** | 当前 5 个主干分支 b1--b5 是跨论文通用接口而非本文专有 schema。原文实际具有以下未在主干中分解的结构：(1) RQ0--RQ3 四级 RQ 骨架（当前 b1 只一个 leaf-scope）；(2) SPACE 五维框架及其 sub-dimensions（当前被压入 leaf-taxonomy）；(3) benefit/risk 的 8+5 主题枚举（当前被压入 leaf-taxonomy）；(4) quality assessment 体系（当前不在任何显式分支）；(5) Tetrad discussion 框架；(6) practitioner/researcher recommendations。原文有 6 类显式 classification scheme + 1 个 extraction form，均未在主干中展开。 | **I** |
| **叶子维度是否足够具体** | **不足** | 当前 7 个叶子（6 个通用接口叶 + 1 个原文 finding 叶被合并计数）对应原文真实 schema 的粒度严重不足。例如：(a) 原文 extraction form 有 11+ 字段，当前只有 5 个候选 orig-* 叶，且均为 `not_verified`、无取值空间、无证据锚点；(b) SPACE 5 维 + 12 sub-dimensions 完全被单一 leaf-taxonomy 吞没；(c) benefit 8 类 + risk 5 类的完整枚举被单一 leaf-taxonomy 吞没；(d) Stol & Fitzgerald 6 类 taxonomy 和 procedure 5 类 taxonomy 被单一 leaf-method 吞没；(e) validated instruments 枚举（NASA-TLX、TAM 等）在树中不可见。通用接口叶不能满足原文 schema 复原的目标。 | **I** |
| **取值空间是否可执行** | **否（对原文候选叶）** | 6 个通用接口叶的取值空间为"自由文本 + 受控标签"——这是跨论文层合理的，但对单篇审计而言不够。5 个 orig-* 候选叶在 CLM C12 中标记为 `schema_seed / not_verified`，没有给出候选取值空间、证据锚点或原文页码。例如 `orig-productivity-outcome` 应有取值为 benefit 8 类 + risk 5 类 + contested（code quality 双面）的枚举，但当前为空。由于 A.3 中 CLM C12 明确声称为 `not_verified`，review.md 自身已承认这一不足。 | **I** |
| **关系边是否缺失** | **是，实质性缺失** | 当前只有两条关系边：`[edge-llm-assistants-developer-productivity-method-evidence]` 和 `[edge-llm-assistants-developer-productivity-taxonomy-finding]`。缺失的关键关系包括：(1) RQ → result table → summary 的映射边（原文每个 RQ 内部有明确的 table-RQ-summary 三元组）；(2) extraction form field → table/evidence 的映射边；(3) benefit/risk theme → primary study evidence（原文每条 theme 都引用具体 PS 编号，但在树中不可见）；(4) SPACE dimension → coverage count（原文 RQ3 的核心统计关系）；(5) quality assessment score → evidence strength（影响 finding 可靠性）；(6) recommendation → supporting RQ finding（原文每条 rec 绑定特定 RQ 发现）。 | **I** |
| **统计用途 / 分母是否正确** | **未定义** | 当前所有叶子在 review.md 中标注"可进入描述统计 / 交叉统计，前提是分母和样本单位明确"，但没有任何叶子给出了实际分母（例如：39 篇 primary studies、SPACE 各维度覆盖的 N=39、benefit/risk 各主题涉及的 PS 计数、quality scores 分布等）。review.md A.2 证据表中引用原文统计数字（如 EV-002 引用"38% lab experiments"），但这些数字未锚定到维度树叶子的统计用途字段。当前状态是：统计数字在 A.2 证据表中以自由文本形式存在，维度树叶子声称"可统计"但未给出实际统计赋值。这对后续 A2a/A2b 跨论文统计造成障碍。 | **I** |
| **候选 finding 路径是否完整** | **不完备** | review.md A.3 包含 12 条 CLM，主要类型为 `leaf_definition`、`migration_boundary`、`candidate_finding`、`relation_edge`、`source_schema_candidate`。其中：(1) CLM C09 声明本文可为候选发现提供启发但不可直接升级为最终发现——这是正确的声明；(2) 但 A.3 中没有一条 CLM 将原文的 8 个 benefit themes、5 个 risk themes、SPACE 覆盖缺口或 contested findings 逐条映射为可审计的候选发现路径。例如原文关键发现"code quality 同时为 benefit 和 risk"在 CLM 中无对应条目。原文 Discussion 中的 5 条 practitioner recommendations 和 3 大 researcher directions 也未在 A.3 中形成可审计映射。 | **C** |
| **A.1--A.4 证据链是否足够** | **部分足够** | A.1 来源清单完整，4 个本地文件（bibtex.bib、metadata.json、paper_content.txt、paper.pdf）+ 1 个外部（Zenodo）。A.2 证据表共 5 条 EV，覆盖 root/b3/b4/b5 和 method-evidence 边，但覆盖范围不均匀：EV-001 为 root 定义，EV-002 为全文结构，EV-003 为通用判例（全文文本提取），EV-004 为人工核验边界，EV-005 为分类结果表/讨论章节。关键遗漏：(1) 没有专门 EV 锚定 benefit 主题枚举（原文 Table 8）；(2) 没有专门 EV 锚定 risk 主题枚举（原文 Table 9）；(3) 没有专门 EV 锚定 SPACE dim-by-dim 覆盖统计（原文 Table 10/11）；(4) 没有专门 EV 锚定 quality assessment criteria/scores；(5) EV 均为 `weak` 强度，因为均未标注精确页码/表号。A.4 本地复验清单只有 2 条（structure check passed + visual check needs_manual_check），不足以覆盖原文 11 张表和 9 张图的核验范围。 | **I** |
| **是否存在可能误导 A2a 的强主张** | **否（C12 已明确降级）** | review.md CLM C12 显式声明 5 个 orig-* 候选叶仅为 `schema_seed / not_verified`，且当前"不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结"。CLM C08 声明"本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论"。CLM C09 声明"单篇 discussion、roadmap 或统计观察不能直接升级为最终发现"。这些降级声明正确且充分。但 "A1-DT 叶子层口径校准" 段落的自我批评虽坦诚，并未解决底层不足——它承认了问题，但没有给出修复路径。 | M |

---

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树，同时保留与跨论文通用接口的映射关系。**原则**：不臆造原文没有的字段；所有叶子均能从原文 §3--§9 中定位证据。

```
[dim-llm-assistants-developer-productivity-root] The Impact of LLM-Assistants on Software Developer Productivity
│
├── [dim-llm-assistants-developer-productivity-rq] ← 论文 RQ 结构（替代当前仅 b1+leaf-scope）
│   ├── [leaf-llm-assistants-developer-productivity-rq0-landscape] RQ0: 研究景观
│   │   ├── 取值空间：year_distribution, author_distribution, venue_distribution, tool_distribution
│   │   ├── 证据：§4 + Table 3, Table 4
│   │   └── 可统计：是（N=39；venue 分布 %；tool 频次）
│   ├── [leaf-llm-assistants-developer-productivity-rq1-method] RQ1: 方法实践
│   │   ├── 取值空间：strategy_taxonomy(6类), procedure_taxonomy(5类), objective(formative|summative),
│   │   │   analysis_type(quant|qual|mixed), instrument_category(self-reported|behavioral|econometric),
│   │   │   metric_name(free), metric_type(performance|cognitive|quality|productivity|acceptance)
│   │   ├── 证据：§5 + Table 5, Table 6, Table 7, Fig. 3, Fig. 4
│   │   └── 可统计：是（N=39；strategy %；procedure %；mixed-methods %；instrument/method frequency）
│   ├── [leaf-llm-assistants-developer-productivity-rq2-impact] RQ2: 效果综合
│   │   ├── 取值空间：benefit_category(8类), risk_category(5类), contested_theme(code_quality)
│   │   ├── 证据：§6 + Table 8, Table 9, Fig. 6
│   │   └── 可统计：是（N=39；各 benefit/risk 类别涉及的 PS 数）
│   └── [leaf-llm-assistants-developer-productivity-rq3-coverage] RQ3: 维度覆盖
│       ├── 取值空间：SPACE-dim_Satisfaction(sub: experience|self_efficacy|trust|cognitive_load),
│       │   SPACE-dim_Performance(sub: quality|impact),
│       │   SPACE-dim_Activity(sub: action_counts),
│       │   SPACE-dim_Communication(sub: human_LLM|human_human),
│       │   SPACE-dim_Efficiency(sub: temporal|automation|interruptions)
│       ├── 证据：§7 + Table 10, Table 11
│       └── 可统计：是（N=39；各 dim 覆盖频次；最小/最大/最常见 dim 组合）
│
├── [dim-llm-assistants-developer-productivity-extraction-form] ← 原文 extraction form（全新）
│   ├── [leaf-llm-assistants-developer-productivity-ef-strategy] 研究策略（Stol & Fitzgerald 6 类）
│   ├── [leaf-llm-assistants-developer-productivity-ef-procedure] 研究程序（5 类 procedure）
│   ├── [leaf-llm-assistants-developer-productivity-ef-objective] 研究目标（formative/summative）
│   ├── [leaf-llm-assistants-developer-productivity-ef-analysis-type] 分析类型（quant/qual/mixed）
│   ├── [leaf-llm-assistants-developer-productivity-ef-instrument] 评价工具（自设/已验证枚举）
│   ├── [leaf-llm-assistants-developer-productivity-ef-metric] 评价指标（枚举：time/correctness/acceptance/quality/cognitive/NPS）
│   ├── [leaf-llm-assistants-developer-productivity-ef-llm-tool] LLM 工具（ChatGPT/Copilot/Tabnine/...）
│   ├── [leaf-llm-assistants-developer-productivity-ef-task] 开发者任务（coding/testing/debugging/...）
│   ├── [leaf-llm-assistants-developer-productivity-ef-impact] 影响方向（benefit/risk/contested）
│   └── [leaf-llm-assistants-developer-productivity-ef-space-dim] SPACE 维度（5 维 + sub-dimensions）
│
├── [dim-llm-assistants-developer-productivity-corpus] ← 语料与纳排（保留当前 b2）
│   ├── [leaf-llm-assistants-developer-productivity-search-databases] 检索数据库（ACM/IEEE/Scopus/WoS/arXiv）
│   ├── [leaf-llm-assistants-developer-productivity-time-window] 时间窗（2014-01--2024-12）
│   ├── [leaf-llm-assistants-developer-productivity-inclusion-count] 纳入数（39）
│   ├── [leaf-llm-assistants-developer-productivity-control-papers] 控制论文（用于 query validation）
│   └── [leaf-llm-assistants-developer-productivity-snowballing] 前向/后向 snowballing
│
├── [dim-llm-assistants-developer-productivity-quality] ← 质量评价（全新，原文 §3.5）
│   ├── [leaf-llm-assistants-developer-productivity-qa-criteria] QA 标准
│   ├── [leaf-llm-assistants-developer-productivity-qa-scores] QA 评分
│   └── 缺失值语义：not_reported（若原文未给出）
│
├── [dim-llm-assistants-developer-productivity-benefit-risk] ← benefit/risk 主题（全新，分解当前 leaf-taxonomy）
│   ├── [leaf-llm-assistants-developer-productivity-benefit] 效益主题（枚举 8 类）
│   │   └── 取值：accelerate_development, minimize_search, automate_trivial,
│   │          knowledge_acquisition, code_adjacent_tasks, reduce_init_overhead,
│   │          improve_code_quality, support_debugging
│   ├── [leaf-llm-assistants-developer-productivity-risk] 风险主题（枚举 5 类）
│   │   └── 取值：fail_requirements, over_reliance, disrupt_flow,
│   │          limit_code_quality, reduce_collaboration
│   └── [leaf-llm-assistants-developer-productivity-contested] 竞争性发现
│       └── 取值：code_quality（同时出现在 benefit 和 risk）
│
├── [dim-llm-assistants-developer-productivity-discussion] ← Discussion（全新，原文 §8）
│   ├── [leaf-llm-assistants-developer-productivity-tetrad] Tetrad 解释框架
│   │   └── 取值：enhance, reverse, obsolesce, retrieve
│   ├── [leaf-llm-assistants-developer-productivity-practitioner-rec] 实践建议（5 类）
│   └── [leaf-llm-assistants-developer-productivity-researcher-rec] 研究方向（3 大方向）
│
├── [dim-llm-assistants-developer-productivity-threats] ← 效度威胁（分解当前，原文 §9）
│   ├── [leaf-llm-assistants-developer-productivity-threat-review] 综述方法威胁
│   │   └── 取值：selection_bias, query_challenge, subjectivity, classification_rigor
│   └── [leaf-llm-assistants-developer-productivity-threat-evidence] 证据基础限制
│       └── 取值：formative_studies, methodological_diversity, temporal_relevance
│
└── [dim-llm-assistants-developer-productivity-artifacts] ← 复现资产（原文 §1+§10）
    ├── [leaf-llm-assistants-developer-productivity-replication-url] Zenodo URL
    └── [leaf-llm-assistants-developer-productivity-artifact-contents] 声明内容（data/decisions/rationales/appendix）
```

### 4.1 与当前 review.md 树的映射关系

| 当前 review.md 节点 | 建议新增/拆分 | 理由 |
|---|---|---|
| b1 + leaf-scope | 拆为 dim-rq + 4 个 leaf-rq0/1/2/3 | 原文 RQ 是全文骨架，不是一个单一 scope 字段能承载 |
| b2 + leaf-corpus | 保留 dim-corpus + 拆为 5 个具体叶 | 原文搜索细节（数据库、时间窗、控制论文、snowballing）在文本中可独立定位 |
| b3 + leaf-taxonomy | 拆为 dim-benefit-risk（3 叶）+ dim-extraction-form（10 叶）+ RQ 叶上的分类赋值 | 原文有 2 套 independent taxonomy + 1 个 extraction form + 1 个 SPACE mapping，不应被一个 leaf-taxonomy 吞没 |
| b4 + leaf-method | 保留 dim-method 但放入 extraction form 域或 RQ1 域 | 原文方法是综述对象（primary studies 的方法），不是综述自身方法 |
| b5 + leaf-evidence + leaf-finding | 拆为 dim-quality + dim-artifacts + dim-threats + dim-discussion | 原文 quality/artifact/threat/discussion 各自有独立章节和可定位证据 |
| 缺失 | dim-quality、dim-discussion、dim-threats、dim-artifacts | 均为原文独立章节（§3.5、§8、§9、§1+§10），当前树不包含 |

### 4.2 建议树与通用接口的关系

建议树中每个叶子都可以在取值空间字段中标注它对应哪个 A1-M0--M6 元维度。例如：
- dim-corpus 叶 → A1-M1 语料收集与纳排
- dim-benefit-risk 叶 → A1-M2 研究对象与主题语义
- dim-extraction-form 叶 → A1-M3 方法/技术
- dim-quality + dim-artifacts 叶 → A1-M4 评价证据
- dim-rq 叶中可统计子叶 → A1-M5 统计分析
- dim-discussion + dim-threats 叶 → A1-M6 finding 形成与裁决

这样可以同时满足“单篇原文 schema 完整复原”和“跨论文可比较”的两层需求。

---

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| **补全 RQ0--RQ3 四级 RQ 叶** | review.md §"维度树复原" 树结构 + A.2 证据表 | 在维度树中将当前 leaf-scope 拆为 4 个 RQ 叶（见 §4 建议树）。每叶给出取值空间、证据锚点（原文 §4/§5/§6/§7 + Table 3--11）。RQ0 应能统计 year/author/venue/tool distribution；RQ1 应能统计 strategy/procedure/objective/instrument 分布；RQ2 应能列举 8 类 benefit + 5 类 risk；RQ3 应能按 SPACE 5 维统计覆盖频次。 | paper_content.txt §4 RQ0 summary、"35 out of 39 were published after ChatGPT"、Table 3/4；§5 表 5/6/7 及 Fig. 3/4；§6 表 8/9 及 Fig. 6；§7 表 10/11 | **C** |
| **补全 extraction form 字段叶** | review.md §"维度树复原" + CLM C12 | 将当前 5 个 orig-* 候选叶从 `not_verified` 升级为 at least `weak`，并逐叶给出原文 evidence anchor（§3.2 extraction form 描述 + 对应结果表）。补齐缺失叶：ef-objective（formative/summative）、ef-analysis-type（quant/qual/mixed）、ef-instrument-category（self-reported/behavioral/econometric）、ef-metric-name（枚举 time/correctness/acceptance/quality/cognitive/NPS）。 | paper_content.txt §3.2 description of extraction form; §5 各表对 extraction fields 的使用 | **C** |
| **显式列出 benefit 8 类 + risk 5 类枚举** | review.md A.2 证据表 | 新增 EV 条目专门锚定 Table 8 和 Table 9，将 8 个 benefit 和 5 个 risk 作为受控枚举值写入维度树叶子的取值空间。若当前只做 `schema_seed`，也应至少完整列出原文使用的类别名，并标注为 `待 A2a 原文表页核对`。 | paper_content.txt §6.1 八类 benefit（accelerate development 到 support debugging）、§6.2 五类 risk（fail to meet requirements 到 reduce team collaboration）、Table 8、Table 9 | **I** |
| **补全 SPACE 5 维 + sub-dimensions** | review.md §"维度树复原" 或新 dim-benefit-risk 域 | 将 SPACE dimensions 作为受控枚举：Satisfaction (4 sub)、Performance (2 sub)、Activity (1)、Communication (2 sub)、Efficiency (3 sub)。在维度树中作为 RQ3 叶子或独立分类叶的取值空间。当前 leaf-taxonomy 太粗。 | paper_content.txt §7 SPACE mapping with sub-dimensions、"Satisfaction 77%, Performance 64%, Efficiency 59%, Activity 31%, Communication 26%" | **I** |
| **补充 finding 路径映射** | review.md A.3 CLM 表 | 为以下原文发现逐条建立 CLM：(1) "90% examine at least 2 SPACE dimensions" → CLM（可统计候选发现）；(2) "code quality reported as both benefit and risk" → CLM（contested finding 候选）；(3) "only 15% extend beyond 3 dimensions" → CLM（gap 候选）；(4) "Communication and Activity remain underexplored" → CLM（gap 候选）；(5) 8 条 benefit themes 和 5 条 risk themes 应至少各有一条 CLM 作为 candidate_finding，标记证据强度为 `weak`（来自单篇文献综述，需跨论文验证）。 | paper_content.txt §6--§8 各 RQ summary + Discussion | **C** |
| **补全 quality assessment 维度** | review.md §"维度树复原" 新增 dim-quality | 原文 §3.5 有显式 quality assessment criteria 和 scoring。当前维度树完全缺失。新增 dim-quality → leaf-qa-criteria + leaf-qa-scores，证据锚点为 §3.5 + 可能存在的 supplementary Appendix QA scores。 | paper_content.txt §3.5 中提及 QA criteria 改编自 Kitchenham & Charters；原文可能有 supplemental QA 表 | **I** |
| **补充 relation edge 矩阵** | review.md A.2 证据表 + A.3 CLM | 新增以下关系边：(1) RQ → result table 的映射边（已隐式存在于原文结构但需在维度树中显式）；(2) benefit/risk theme → cited PS evidence 的引用边（原文每个 theme 内都引用具体 PS 编号）；(3) SPACE dimension → coverage count 的统计边；(4) recommendation → supporting RQ 的依赖边。 | paper_content.txt §6.1 各 benefit 段内的 [PSxx] 引用、§6.2 各 risk 段内的 [PSxx] 引用、§7 各 SPACE dim 覆盖 %、§8 各 rec 与 RQ 的绑定 | **I** |
| **补全 A.4 人工核验清单** | review.md A.4 | 当前 A.4 只有 2 条（structure check + visual check）。应扩展为：(1) PDF 逐页核对 Table 3--11 的版式、数值与文本提取一致性；(2) PDF 核对 Fig. 1--9；(3) 核验 Zenodo replication package 内容完整性；(4) 核验 extraction form 确切实体是否在原文或 supplemental appendix 中完整呈现；(5) 核对 RQ2 radar plot 的精确数值。 | paper.pdf 待核验；Zenodo https://zenodo.org/records/18489222 待下载核验 | M |
| **补充 summary style 与 RQ→finding 映射** | review.md §3（当前已有一个 RQ summary 写作分析表） | §3 的 RQ summary 写作分析表质量很好，但它不在维度树和 A.2/A.3 表内。建议将 summary style 作为 leaf-report-structure 的一个取值，或通过 relation edge 把 summary 文本锚定到对应 RQ 叶。 | paper_content.txt 各 RQ summary 段落 | M |

---

## 6. C/I/M 结论

### C（阻塞性）: 3 项

| # | 问题 | 对 Paper2 的影响 |
|---|---|---|
| C1 | **候选 finding 路径不完整**（§3.2 审计矩阵第 7 行）。review.md A.3 没有将原文 8 类 benefit、5 类 risk、SPACE 覆盖缺口、code quality contested finding、5 条 practitioner recommendations 或 3 大 researcher directions 映射为可审计的 CLM。这直接破坏 Paper2 的 "维度模式 → 统计观察 → 候选发现 → 研究者裁决" 证据链——后续 A2a/A2b 无法从此 review 中提取可引用的候选发现信号。 | **Paper2 A2a/A2b 无法从本文获取候选发现信号。若其他 18 篇也有类似缺失，Paper2 统计综合将缺乏 finding 级数据源。** |
| C2 | **extraction form 字段叶未赋值**（§3.2 审计矩阵第 3--4 行 + §5 清单第 2 项）。原文显式 extraction form 的 11+ 字段在维度树中仅以 5 个 `not_verified` 候选叶存在，无取值空间、无证据锚点。这使得 Paper2 无法从本文学习"如何把 extraction form 投影为维度树"，而这是论文 scaffold 的核心目标之一。 | **Paper2 丢失一个最优的 extraction form → dimension tree 映射范例。C12 的自知声明诚实但未修复问题。** |
| C3 | **RQ 结构在维度树中被扁平化**（§5 清单第 1 项）。原文 RQ0--RQ3 四级架构是全文骨架，当前被压缩为单一 leaf-scope。这使得后续 Paper2 无法从本文学习 "RQ 驱动综述如何按 RQ 分叶组织维度树"。 | **Paper2 丢失 SLR+SMS 标准 RQ→dimension→evidence 组织模式的结构性参考。** |

### I（重要）: 5 项

| # | 问题 | 对 Paper2 的影响 |
|---|---|---|
| I1 | **benefit/risk 枚举未在维度树中显式列出**（§5 清单第 3 项）。8 类 benefit + 5 类 risk 的完整枚举被单一 leaf-taxonomy 吞没。 | 后续跨论文统计无法区分"有主题分析的 SLR" 和"没有主题分析"的样本，也无法按 benefit/risk 类别进行交叉统计。 |
| I2 | **SPACE framework 未分解**（§5 清单第 4 项）。5 维 + 12 sub-dimensions 在树中不可见。 | Paper2 无法学习"外部框架 + emergent coding" 的双层分类模式，也无法在使用 SPACE 的综述之间交叉比较。 |
| I3 | **quality assessment 维度缺失**（§5 清单第 6 项）。原文 §3.5 的 QA 体系完全未进入维度树。 | Paper2 无法从本文获取 quality assessment → evidence strength 的关系模式，这是一个关键的方法学 pattern。 |
| I4 | **关系边严重不完整**（§3.2 审计矩阵第 5 行）。当前仅 2 条边，缺失 RQ→table→summary、benefit/risk→cited PS、SPACE dim→coverage count、recommendation→RQ 等多条关键关系边。 | Paper2 维度树的 relation edge 模式将无法从本文获得充分启发，影响后续字段间关系定义。 |
| I5 | **A.2 证据表覆盖不均**（§3.2 审计矩阵第 8 行）。5 条 EV 中无一专门锚定 benefit table/risk table/SPACE mapping/quality assessment，且均为 `weak` 强度。 | 后续 A2a 精核时，本文的 benefit/risk/SPACE/quality 证据需要从零开始锚定，A1-DT 的 EV 表未提供起点。 |

### M（建议）: 2 项

| # | 问题 |
|---|---|
| M1 | A.4 人工核验清单过于简短（仅 2 条），建议扩展到覆盖所有 11 张表和 9 张图的逐项核对。 |
| M2 | §3 的 RQ summary 写作分析表质量很好，建议将其与 A.2 证据表和 A.3 CLM 表建立交叉引用，使 summary style pattern 可被统计工具消费。 |

### 最终建议：**NEEDS FIX**

当前 review.md 在以下方面是正确的：
- 根节点、跨论文通用接口层（6 叶）、迁移边界声明、降级纪律、A.1 来源清单；
- CLM C08/C09/C12 的自我认知诚实且降级充分——它承认了通用叶不是原文 schema 还原。

但 review.md 未能满足以下 A1-DT 验收关键要求：
- **原文 schema 的完整叶子层复原**（这是 GUIDE.md §7 "A1-DT 维度树复原规则" 的核心要求，即"维度树必须可追溯到原文具体段落、表、图或附录锚点"）；
- **候选发现路径的完整映射**（这是 pattern-field-schema.md §8.4 "结论-证据映射合同" 的要求，即每个结论必须有 `[clm-*]`，支持证据必须回链 A.2）；
- **extraction form 字段 → 维度树叶子的显式投影**（这是本论文作为 SLR + SMS 模式样本的核心价值所在）。

建议优先修复 C1--C3 和 I1--I4，I5 和 M1--M2 可在后续 A2a 中一并处理。修复后建议由另一位 reviewer（如 qwen 或 sonnet）做二次审计确认。

---

*审计人：deepseek*
*审计日期：2026-06-29*
*审计范围：单篇 llm-assistants-developer-productivity 全文文本级*
*审计原则：不修改仓库文件，不 push，不 gh comment*
