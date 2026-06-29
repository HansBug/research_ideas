# requirements-quality-theory-roadmap · deepseek 全文审计报告

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
- **是否完整阅读 `paper_content.txt`**：是。已全文阅读全部 1187 行，覆盖摘要（Page 1）、引言与方法背景（Sections 1-2）、RQT 理论与 Table 1 概念全集（Section 3）、实验对象与设计（Section 4.1-4.2）、57 篇编码结果与 Figure 4 统计（Section 4.3）、interpretation 与 finding（Section 4.4）、效度威胁（Section 4.5）、六条 roadmap action point（Sections 5.1-5.6）、结论与 references。所有关键段落均已定位并用于交叉验证。
- **是否核对 `paper.pdf`**：是（有限度）。通过 PyPDF2 按页提取 PDF 文本，确认以下关键信息：(a) Table 1 包含全部 11 个 RQT concept 及其定义与来源；(b) Figure 2 / Figure 4 / Figure 5 在图注中确认存在；(c) 图、表的具体视觉内容无法通过文本提取精确复原，因此图表级细节仍标注为待人工版面核对。PDF 共计 14 页，与 paper_content.txt 的 14 页标记一致。

## 2. 原文真实结构复原

### 2.1 原文 RQ / 目标 / 贡献声明

原文为一篇 **Research Commentary**（期刊 VIEW POINT 栏目），标题为 "Requirements quality research: a harmonized theory, evaluation, and roadmap"。作者在 Introduction 中声明三项贡献：

1. **A harmonized requirements quality theory（RQT）**：作为 requirements quality 领域的理论基石。
2. **A survey of requirements quality research**：揭示现有文献如何（或未能）报告 RQT 的概念。
3. **A consequent research roadmap**：针对发现的缺口提出研究路线图。

原文显式 **RQ**：*"How are the concepts of the requirements quality theory reported in requirements quality literature?"*（Section 4 开头）。

### 2.2 原文方法流程

原文的方法流程不是经典 SLR/SMS，而是 **survey research on secondary study objects**：

1. **对象选择（Section 4.1）**：使用 Frattini et al. [7] 前期系统研究中的 57 篇 primary study 作为 convenience sample。不是从头检索，而是从已有系统研究中继承语料。
2. **工具设计（Section 4.2）**：
   - 创建基于 RQT 概念的 **extraction guideline**。
   - 每个 RQT concept 关联一个或多个 categorical variable，每个 variable 有一组 codes（如 Entity 的 codes：explicit / implicit；Factor 的 codes：explicit / referenced × textual / formula；Impact 的 codes：N/A / hypothesized / inductive / referenced × necessary / possible）。
   - codes 经过两轮迭代（ad hoc → 讨论与理论背景精炼）。
3. **数据抽取**：第一作者对所有 57 篇执行编码，第二作者对 6 篇（≈10%）独立抽取以计算 inter-rater reliability。
4. **统计**：生成描述性统计（频次、百分比）并按 concept × code 维度展示（Figure 4）。
5. **Interpretation（Section 4.4）**：从统计数据回答 RQ，形成关于 artifact-centric bias、activity-neglect、context-neglect、economic-neglect 等 finding。
6. **效度威胁（Section 4.5）**：按 Wohlin et al. [72] 框架讨论 internal / construct / external validity。
7. **Roadmap（Section 5）**：六条具体 action point（5.1--5.6）。

### 2.3 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

1. **RQT 理论模型（Table 1 + Figure 2）**：
   - 11 个核心 concept：`Entity`、`Factor`、`Entity-fact`、`Agent`、`Activity`、`Attribute`、`Activity-fact`、`Impact`、`Context factor`、`Cost`、`Resource`。
   - 概念关系：Entity × Factor → Entity-fact；Entity-fact × Context factor → Impact → Activity-fact (Activity × Attribute)；Activity-fact → Cost × Resource。
   - 理论类型：同时是 explanatory（解释 requirements quality 是什么）和 prescriptive（规定如何报告相关贡献）。

2. **Coding scheme**：
   - 每个 RQT concept 的 codes 即是 extraction form。例如：
     - Entity：`explicit` / `implicit`
     - Factor：`explicitly reported` / `referenced` × `textual description` / `formal definition`
     - Impact：`N/A` / `hypothesized` / `inductive` / `referenced` × `necessary` / `possible`
     - Activity：`not reported` / `ad hoc` / `systematic`
     - Agent / Attribute / Context / Cost / Resource：各自对应的 classification codes
   - `N/A` 表示某篇 publication 未报告该 concept。

3. **Figure 4**：以柱状图 + 子行（dimension codes）展示每个 RQT concept 在 57 篇上的 code 分布。这是原文的核心 evidence table。

4. **Roadmap（Sections 5.1--5.6）**：六条可引用的 action point：
   - 5.1 Artifact and usage model（需求实体的 reference activity model + activity attribute）
   - 5.2 Taxonomy of quality factors
   - 5.3 Taxonomy of impacts → 升级为 impact framework / regression problem
   - 5.4 Context factors
   - 5.5 Economic impact
   - 5.6 Tool support（包括 Figure 5 的架构图：entity characterization → context characterization → impact prediction model → economic impact quantification）

5. **Replication package**：Zenodo DOI `10.5281/zenodo.8167598`，包含 extraction guideline、raw coding spreadsheet 等。

6. **Quality / validity rubric**：无独立 quality assessment rubric（如 AMSTAR、DARE、EBSE quality checklist），但 inter-rater reliability（percentage agreement 83.3%, S-Score 76.8%）承担了 extraction quality 的角色。

### 2.4 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文的 conclusion formation 路径如下：

```
Field extraction (RQT codes on 57 papers)
  ↓
Descriptive statistics (频次 / 百分比 per concept × code)
  ↓
Interpretation (Section 4.4):
  - "all publications mention entity + factor" → artifact-centric coverage
  - "42.1% entities implicit" → terminological ambiguity
  - "29.8% no impact (N/A)" → normative bias, missing practical relevance
  - "24.6% report agents, 14% report attributes" → activity-side neglect
  - "47.5% impact hypothesized vs 27.5% inductive" → anecdotal evidence dominance
  - "context factors almost completely neglected" → external validity threat
  - "cost/resources reported rarely (15.8% / 8.8%)" → economic disconnect
  ↓
Gap identification:
  - Artifact-centric bias
  - Missing activity perspective → critical for practical relevance
  - Non-systematic activity selection
  - Missing measurable activity attributes
  - Missing context factors & economic perspective
  ↓
Roadmap (Sections 5.1--5.6): six concrete action points to close gaps
```

## 3. 当前 `review.md` 维度树审计

### 3.1 当前维度树结构（引自 review.md）

```
[dim-requirements-quality-theory-roadmap-root] Requirements quality research
├── [dim-requirements-quality-theory-roadmap-b1] 综述范围与研究问题
│   └── [leaf-requirements-quality-theory-roadmap-scope] 研究范围与单位对象
├── [dim-requirements-quality-theory-roadmap-b2] 语料收集与纳排
│   └── [leaf-requirements-quality-theory-roadmap-corpus] 语料与纳排链条
├── [dim-requirements-quality-theory-roadmap-b3] 主题 / 对象分类
│   └── [leaf-requirements-quality-theory-roadmap-taxonomy] 主题与维度分类
├── [dim-requirements-quality-theory-roadmap-b4] 方法 / 技术 / 干预
│   └── [leaf-requirements-quality-theory-roadmap-method] 方法 / 技术 / 干预分类
└── [dim-requirements-quality-theory-roadmap-b5] 评价、统计与候选发现
    ├── [leaf-requirements-quality-theory-roadmap-evidence] 评价、证据与复现资产
    └── [leaf-requirements-quality-theory-roadmap-finding] 统计观察与候选发现
```

另有独立 "原文模式候选叶子映射" 表，包含 5 个候选叶子：
- `[leaf-requirements-quality-theory-roadmap-orig-quality-construct]`
- `[leaf-requirements-quality-theory-roadmap-orig-theory-model]`
- `[leaf-requirements-quality-theory-roadmap-orig-evaluation-method]`
- `[leaf-requirements-quality-theory-roadmap-orig-roadmap-question]`
- `[leaf-requirements-quality-theory-roadmap-orig-boundary]`

### 3.2 逐项检查

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 部分准确但过于泛化 | 根节点标签 "Requirements quality research 的研究目标 / RQ / 贡献声明" 泛化为 "Requirements quality research"，未体现原文 **theory + evaluation + roadmap** 三段式核心贡献结构。原文是 research commentary，不是传统 SLR 的范围定义。根节点应体现三段式，否则 A2a 无法判断这篇论文在 Paper2 元模型中的独特位置。 | **I** |
| 主干分支是否覆盖原文 schema | **未覆盖**——主干分支 b1--b5 是 [pattern-field-schema.md](./../../patterns/pattern-field-schema.md) 六类通用接口的降维投影，不是原文自身 schema | 原文的结构是：(1) RQT 理论（11 个 concept + 关系），(2) 基于 coding scheme 的 57 篇评价，(3) 六条 roadmap action point。当前主干完全缺失：(a) RQT 理论 concept 树（Entity, Factor, Entity-fact, Agent, Activity, Attribute, Activity-fact, Impact, Context factor, Cost, Resource）；(b) 概念间关系边（impact chain: Entity×Factor → Entity-fact → Impact ← Context factor → Activity-fact ← Activity×Attribute → Cost → Resource）；(c) Section 5 的六条 roadmap action point 分支；(d) extraction guideline / coding scheme 分支。b1--b5 本质上是把通用 "综述六问" 接口套用到这篇 paper 上，不是复原 paper 自身的信息结构。 | **C** |
| 叶子维度是否足够具体 | **不足**——6 个叶子是 6 类通用接口，不是原文的 actual leaf | 原文有非常具体的 leaf：(a) 11 个 RQT concept 各自是独立 leaf，每个有具体 codes（Entity: explicit/implicit; Impact: N/A/hypothesized/inductive/referenced × necessary/possible; 等等）；(b) 6 条 roadmap action point 各自是独立 leaf；(c) inter-rater reliability（百分比一致性 83.3%, Kappa 54.2%, S-Score 76.8%）是独立的 quality indicator leaf；(d) 57 是分母 leaf。当前 6 个叶子把这些全部压缩成泛化标签。 | **C** |
| 取值空间是否可执行 | **不可执行**——当前叶子取值空间是泛化描述，不是原文的实际 codebook | 原文每个 RQT concept 有显式 categorical codes（如 Impact 的 "N/A / hypothesized / inductive / referenced × necessary / possible"）。当前叶子取值空间写 "自由文本加 RQ / 贡献声明引用"、"完整枚举 / 层级枚举 / 自由文本加理由"，这些无法指导 A2a 从原文精确抽取事实。review.md 的 candidate leaves (orig-*) 表承认了这一点但未将实际 codebook 映射到主树。 | **I** |
| 关系边是否缺失 | **严重缺失**——原文的 impact chain 关系完全不在维度树中 | 原文 RQT 有显式的关系链：`Entity × Factor → Entity-fact → [Impact] → Activity-fact (Activity × Attribute)`；`Context factor → Impact`；`Activity-fact → Cost → Resource`。这些关系边是原文最核心的学术贡献（the theory itself），当前维度树中完全没有关系边。这在 paper-field-schema 8.3 节中已定义了关系边合同（`[edge-*]`），但此篇 review 未使用。 | **C** |
| 统计用途 / 分母是否正确 | 部分正确 | review.md 正确标注 "不进入主统计池；只作 schema seed / boundary anchor" 并在 metadata.json 中填写了 exclusion reason。这符合 GUIDE 和 SUMMARY 的三池规则（theory/evaluation/roadmap → schema seed / boundary pool）。但当前树未记录原文的实际统计结构：分母 = 57，每个 concept 的频次与百分比（如 17/57 = 29.8% 无 impact，14/57 = 24.6% 报告 agent，8/57 = 14% 报告 attribute 等），这些是可被 A2a 使用的 scoping evidence。 | **M** |
| 候选 finding 路径是否完整 | **不完整**——原文的 gap identification 路径被压缩成单个泛化叶子 | 原文从统计到 finding 的路径是明确的：每个统计（如 29.8% 无 impact）→ interpretation（"neglect practical relevance"）→ gap claim（"artifact-centric bias"）→ roadmap action。当前树只有一个 "统计观察与候选发现" 叶子，无法追踪 57 个统计值 → 5+ 个 gap → 6 个 roadmap action 的映射。 | **I** |
| A.1--A.4 证据链是否足够 | 结构完整但内容待升级 | A.1（来源）、A.2（证据账本）、A.3（结论映射）、A.4（复验清单）的结构完整，符合 contract。但 A.2 的实际证据条目全部标为 `not_verified`，且 EV-requirements-quality-theory-roadmap-002 同时支撑 12 个维度节点（b1--b5 + 多个 leaves + 全部 5 个 orig 候选叶子），一条证据覆盖过多节点的模式表明维度树颗粒度不足以区分子概念。 | **M** |
| 是否存在可能误导 A2a 的强主张 | **存在中等风险** | review.md 的 "原文模式候选叶子映射" 表声明了 5 个 orig- 候选叶子，但它们 (a) 不在主树中；(b) 无取值空间；(c) 全部 not_verified。如果一个 A2a 读者只看主树结构，会误以为 6 个泛化叶子就是对原文 schema 的完整复原。review.md 在结论中写 "本文已把原文抽取字段、分类项、模型节点或报告叶子列为'原文模式候选叶子映射'" 是准确的自我认知，但主树与候选叶子的分离可能造成误读。 | **I** |

## 4. 建议维度树骨架

以下给出更忠实于原文的维度树。由于原文是 theory + evaluation + roadmap 三段式 research commentary（不是标准 SLR/SMS），维度树应反映这三段结构。

### 4.1 建议主树

```
[dim-rqtr-root] requirements-quality-theory-roadmap: 三段式 theory → evaluation → roadmap
│   根定义：Frattini et al. (2023) 在 Requirements Engineering 期刊发表的 research commentary，
│   贡献 (1) RQT 理论、(2) 57 篇文献评价、(3) 六条 roadmap action point。
│   统计池资格：eligible_for_statistical_synthesis=false（非标准 SLR/SMS）；
│   证据角色：theory_roadmap_schema_seed（仅作 boundary anchor / schema seed）。
│
├── [dim-rqtr-t1] 第一部分：RQT 理论（Harmonized Requirements Quality Theory）
│   │   来源：Section 3 + Table 1 + Figure 2 + Figure 3（example instantiation）
│   │   证据强度：strong（原文显式文本 + 表 + 图）
│   │
│   ├── [dim-rqtr-t1-artifact] artifact-related concepts（左侧）
│   │   ├── [leaf-rqtr-concept-entity] Entity：需求制品或其组成部分
│   │   │   取值空间：specification / section / paragraph / sentence / requirement（可分解）
│   │   │   缺失语义：implicit（42.1% publications 中 entity scope 不明确）
│   │   ├── [leaf-rqtr-concept-factor] Factor：对 entity 的规范性度量
│   │   │   取值空间：explicitly reported / referenced × textual description / formal definition（可分解为 sub-factor）
│   │   │   缺失语义：not_reported（0/57，全样本均有 factor）
│   │   └── [leaf-rqtr-concept-entity-fact] Entity-fact：entity × factor 的评估结果
│   │       取值空间：conform / missing role / missing all elements 等（由 factor 决定）
│   │
│   ├── [dim-rqtr-t1-activity] activity-related concepts（中间）
│   │   ├── [leaf-rqtr-concept-agent] Agent：参与 activity 的人/群体/自动化
│   │   │   取值空间：human / group / automatism / not_reported（24.6% 报告）
│   │   ├── [leaf-rqtr-concept-activity] Activity：以 entity 为输入的 requirements-affected activity
│   │   │   取值空间：ad hoc / systematic / not_reported；子活动可聚合
│   │   │   缺失语义：92% 报告 activity 的 publications 使用 ad hoc 方式
│   │   ├── [leaf-rqtr-concept-attribute] Attribute：activity 的可测属性
│   │   │   取值空间：determinism / duration / agreement level / readability 等
│   │   │   缺失语义：仅 14% publications 报告
│   │   └── [leaf-rqtr-concept-activity-fact] Activity-fact：activity × attribute 的组合状态
│   │       取值空间：由具体 activity + attribute 决定
│   │
│   ├── [dim-rqtr-t1-impact] impact & context concepts（连接层）
│   │   ├── [leaf-rqtr-concept-impact] Impact：entity-fact 对 activity-fact 的影响
│   │   │   取值空间：N/A（29.8%） / hypothesized（47.5%） / inductive（27.5%） / referenced（25%）
│   │   │          × necessary / possible；可建模为 regression problem
│   │   │   缺失语义：N/A = 未报告任何 impact
│   │   ├── [leaf-rqtr-concept-context] Context factor：影响 impact 的外部上下文
│   │   │   取值空间：organization / people / tools / product / process / not_reported
│   │   │   缺失语义：近全部 publications 未报告或极少报告
│   │   └── [edge-rqtr-impact-chain] impact 关系链
│   │       关系：Entity-fact --[Impact]--> Activity-fact；Context factor --[moderates]--> Impact
│   │
│   └── [dim-rqtr-t1-economic] economic concepts（右侧，novel addition）
│       ├── [leaf-rqtr-concept-cost] Cost：与 activity-fact 相关的成本量级
│       │   取值空间：expected change / general magnitude / not_reported（15.8% 报告）
│       └── [leaf-rqtr-concept-resource] Resource：经济影响所涉及的资源
│           取值空间：money / time / not_reported（8.8% 报告）
│
├── [dim-rqtr-t2] 第二部分：57 篇文献评价（State of Research Evaluation）
│   │   来源：Section 4 + Figure 4 + replication package (Zenodo)
│   │   证据强度：medium（编码统计有 inter-rater reliability 支撑，但图表细节待版面核对）
│   │
│   ├── [leaf-rqtr-eval-rq] 研究问题
│   │   RQ："How are the concepts of the requirements quality theory reported in
│   │        requirements quality literature?"
│   │   取值空间：单条 RQ（原文仅一条显式 RQ）
│   │
│   ├── [leaf-rqtr-eval-objects] 评价对象
│   │   57 篇 primary studies from Frattini et al. [7]；convenience sample（非概率抽样）
│   │   来源锚点：Section 4.1；分母 = 57
│   │
│   ├── [leaf-rqtr-eval-extraction] extraction guideline / coding scheme
│   │   每个 RQT concept → categorical variables → ad-hoc codes（两轮迭代精炼）
│   │   extraction guideline 未在正文完整展示，但 replication package (Zenodo) 中可得
│   │
│   ├── [leaf-rqtr-eval-irr] inter-rater reliability
│   │   percentage agreement: 83.3%；Cohen's Kappa: 54.2%；S-Score: 76.8%（good）
│   │   第二作者对 6/57 (≈10%) 独立编码
│   │
│   ├── [leaf-rqtr-eval-figure4] Figure 4：各 concept 的 code 分布柱状图
│   │   每个 concept 一行柱状图 + 子行 dimension codes
│   │   当前状态：图表细节待 PDF 版面人工核对
│   │
│   └── [leaf-rqtr-eval-stats] 关键统计结果（每项含 n/57 分母）
│       - Entity implicit: 24/57 = 42.1%
│       - Impact N/A: 17/57 = 29.8%
│       - Agent reported: 14/57 = 24.6%
│       - Activity ad hoc (of 40 reporting): 37/40 = 92%
│       - Attribute reported: 8/57 = 14%
│       - Impact hypothesized (of 40 reporting): 19/40 = 47.5%
│       - Impact inductive: 11/40 = 27.5%
│       - Impact referenced: 10/40 = 25%
│       - Cost reported: 9/57 = 15.8%
│       - Resource reported: 5/57 = 8.8%
│       - Context factors: 0 (tools) to 14/57 = 24.6% (product-related)
│
├── [dim-rqtr-t3] 第三部分：Gap → Roadmap
│   │   来源：Section 4.4 (Interpretation) + Section 5 (Research Roadmap)
│   │   证据强度：medium（gap 有统计支撑，但 roadmap 是 vision/proposal）
│   │
│   ├── [leaf-rqtr-gap] Gap identification（5 个核心 gap）
│   │   G1: artifact-centric bias / normative rules without impact evidence
│   │   G2: activity perspective neglected（29.8% no impact; 14% no attributes）
│   │   G3: non-systematic activity selection（92% ad hoc）
│   │   G4: context factors almost completely neglected
│   │   G5: economic perspective disconnected from quality factors
│   │   取值空间：5 个 gap，每个有统计值支撑；G2--G5 有具体百分比锚点
│   │
│   └── [dim-rqtr-roadmap] Roadmap action points（Section 5.1--5.6）
│       │   取值空间：6 条 action point，每条含具体研究流 + 方法指引
│       │   注意：roadmap 属于 vision/proposal，不是完成型 finding
│       │
│       ├── [leaf-rqtr-roadmap-5.1] AP1: Artifact and usage model
│       │   建立 requirements-affected activity 的 reference model + activity attributes
│       ├── [leaf-rqtr-roadmap-5.2] AP2: Taxonomy of quality factors
│       │   扩充 requirements quality factor ontology
│       ├── [leaf-rqtr-roadmap-5.3] AP3: Impact framework（升级 taxonomy → regression framework）
│       │   用 Bayesian data analysis 建模 entity-fact → activity-fact 的 impact relationship
│       ├── [leaf-rqtr-roadmap-5.4] AP4: Context factors
│       │   从 SE context factor sets 出发，建立 RE 视角的 context factor collection
│       ├── [leaf-rqtr-roadmap-5.5] AP5: Economic impact
│       │   量化 activity-fact 的经济后果（cost × resource）
│       └── [leaf-rqtr-roadmap-5.6] AP6: Tool support（Figure 5 架构）
│           输入: entity + context info → entity characterization → context characterization
│           → impact prediction model → economic impact quantification
│
├── [dim-rqtr-t4] 效度威胁
│   │   来源：Section 4.5
│   │
│   ├── [leaf-rqtr-validity-internal] Internal validity
│   │   sampling: convenience sample from [7]；deemed "sufficiently rigorous for initial theory"
│   └── [leaf-rqtr-validity-construct] Construct validity
│       constructs aligned with mature software quality theories
│       implicit embedding of concepts in surveyed publications → extraction difficulty
│       mitigated by independent labeling + inter-rater reliability
│
└── [leaf-rqtr-artifact] Replication package
    Zenodo DOI: 10.5281/zenodo.8167598（extraction guideline + coding spreadsheet）
    Tool repo: github.com/JulianFrattini/rqt-tool（DOI: 10.5281/zenodo.8167541）
```

### 4.2 建议树与当前树的关键差异

| 差异项 | 当前树 | 建议树 |
|---|---|---|
| 根节点 | 泛化 "Requirements quality research" | 具体 "三段式 theory → evaluation → roadmap" |
| 主干数 | 5（b1--b5） | 4+（theory / evaluation / gap→roadmap / validity / artifact） |
| RQT theory 叶子 | 0（仅在候选表中） | 11 个 concept leaf + 关系边 |
| coding scheme | 未体现 | `[leaf-rqtr-eval-extraction]` leaf |
| inter-rater reliability | 未体现 | `[leaf-rqtr-eval-irr]` leaf |
| 统计值 | 未记录 | `[leaf-rqtr-eval-stats]` leaf（10+ 个带分母的统计） |
| Gap→Roadmap 映射 | 压缩为 1 个 "统计观察与候选发现" 叶子 | 完整映射：5 gap → 6 roadmap AP |
| Roadmap action points | 未体现 | 6 个独立 leaf（5.1--5.6） |
| Figure 5 工具架构 | 未体现 | 六组件流水线 leaf |
| 效度威胁 | 部分合并入 A.2 证据 | 独立 validity branch |

### 4.3 统计可执行性说明

建议树中 `[leaf-rqtr-eval-stats]` 的每个统计值都有分母 57（或子集分母 40），可被 A2a 直接引用为 scoping evidence（虽不进入 Paper2 主统计池）。但所有统计值 **当前仅从 paper_content.txt 文本段提取**，其精确页码、Figure 4 的视觉 bar 宽度、sub-dimension 的完整 codes 仍需 A2a 配合 PDF 版面核对后升级为 `strong`。

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 主树根节点过于泛化 | review.md "维度树结构" 节 `[dim-requirements-quality-theory-roadmap-root]` | 根节点名称从 "Requirements quality research 的研究目标 / RQ / 贡献声明" 改为体现三段式："requirements-quality-theory-roadmap: theory → evaluation → roadmap 三段式 research commentary" | 原文 Abstract / Introduction / 三个 contribution bullet | **I** |
| 主干分支是通用接口投影，非原文 schema | review.md 整个 b1--b5 分支结构 | 将 b1--b5 替换为至少 theory-part / evaluation-part / gap→roadmap-part / validity / artifact 五个主干分支。当前 b1--b5 可降级为辅助注释（说明此 paper 映射到通用六类 interface 的方式），但不得作为主事实源。 | 原文 Sections 3/4/5 结构 + Table 1 + Figure 2/4/5 | **C** |
| 缺失全部 11 个 RQT concept leaf | 新增 theory-part 分支 | 新增 `[leaf-rqtr-concept-entity]` 至 `[leaf-rqtr-concept-resource]` 共 11 个 leaf，每个来自 Table 1 + Section 3.1。取值空间使用原文 codes（explicit/implicit/N/A/hypothesized/inductive/referenced/...）。 | Table 1 (Page 5) + Section 4.2 coding scheme description + Figure 4 code dimensions | **C** |
| 缺失 RQT 关系边 | 新增关系边表 | 新增至少一条 `[edge-rqtr-impact-chain]` 关系边，记录 Entity-fact → Impact → Activity-fact → Cost → Resource 的 causal chain。遵循 pattern-field-schema 8.3 节合同。 | Figure 2 (Page 5) + Section 3.1 正文描述 | **C** |
| 缺失 coding scheme leaf | evaluation-part 分支 | 新增 `[leaf-rqtr-eval-extraction]` leaf，记录 extraction guideline / categorical variables / ad hoc codes / 两轮迭代过程。 | Section 4.2 (Page 7-8) | **I** |
| 缺失 inter-rater reliability leaf | evaluation-part 分支 | 新增 `[leaf-rqtr-eval-irr]` leaf，取值空间：percentage agreement 83.3% / Kappa 54.2% / S-Score 76.8% / n=6 (≈10%)。 | Section 4.2 (Page 8) | **I** |
| 缺失 6 条 roadmap action point leaf | roadmap-part 分支 | 新增 `[leaf-rqtr-roadmap-5.1]` 至 `[leaf-rqtr-roadmap-5.6]` 共 6 个 leaf，每条包含原文具体 research stream 描述。 | Sections 5.1--5.6 (Page 10-12) | **I** |
| 缺失 10+ 个统计值 leaf | evaluation-part 分支 | 新增 `[leaf-rqtr-eval-stats]` leaf，列出 10+ 个关键统计（均带 n/57 分母）。标注为 boundary anchor（不进入主统计池）。 | Section 4.3 (Page 8) | **M** |
| 缺失 gap identification leaf | roadmap-part 分支 | 新增 `[leaf-rqtr-gap]` leaf，列出 5 个核心 gap 及其统计锚点。 | Section 4.4 (Page 9) | **I** |
| "原文模式候选叶子映射" 表应合并到主树 | review.md 独立候选叶子表 | 将 5 个 orig-* 候选叶子的内容（quality construct / theory model / evaluation method / roadmap question / boundary）吸收到建议树对应分支（theory-part / evaluation-part / roadmap-part / validity），不再维持分离的 "候选" 状态。这消除了主树与候选表的歧义。 | 建议树 Section 4 中已分配对应位置 | **I** |
| A.2 证据条目 EV-002 支撑 12 个节点 | review.md A.2 表 | 在维度树修复后，将 EV-requirements-quality-theory-roadmap-002 拆分为多个更精准的证据条目，每个只支撑 1--3 个维度节点，并标注原文页码 / 段落位置。 | 当前 EV-002 同时支撑 b1--b5 + 6 leaves + 5 orig leaves | **M** |

## 6. C/I/M 结论

### C（Critical）：直接破坏 Paper2 学术目标、证据链或后续 A2a/A2b 可靠性

1. **主干分支是通用接口而非原文 schema（C）**：b1--b5 六类通用接口投影到 paper 上，完全遗漏了原文三元结构（theory / evaluation / roadmap）。若 A2a 基于当前树进行跨论文维度抽取，会将 A1-M0--M6 元维度误当成 paper-specific schema，丢失本文最独特的贡献——RQT 概念树 + impact chain 关系。这对 Paper2 "研究者定义综述元模型 → 维度模式演化" 主线有直接破坏作用，因为这正是脚手架中最靠近 "formal theory → operational schema" 的先验样本。

2. **缺失全部 11 个 RQT concept leaf 与 impact 关系边（C）**：原文 RQT 是 paper-level 的最核心贡献。当前维度树零覆盖理论 concept 和关系边，意味着 Paper2 脚手架无法从这篇论文提取 "如何把理论对象转化为 codebook" 的模式。这直接削弱 A1-DT 对该论文的核心价值定位（见 review.md "一句话结论" 中 "先定义理论对象与关系 → 用对象级 codebook 评价现有研究" 的迁移目标）。

### I（Important）：会实质影响维度树可用性、原文 schema 复原、证据可审计性

1. **叶子维度泛化（I）**：6 个泛化叶子无法指导 A2a 精确抽取原文事实。取值空间写成 "自由文本" 而非原文显式 codes。

2. **缺失 coding scheme / inter-rater reliability leaf（I）**：extraction guideline 和 IAA 是本文区别于纯 theory paper 的关键方法学制品。缺失意味着 A2a 无法判断本文的 extraction 方法学质量。

3. **缺失 6 条 roadmap action point leaf（I）**：roadmap 是本文三大贡献之一，完全遗漏在维度树外。

4. **主树与候选叶子分离造成歧义（I）**：读者可能误将主树 6 个泛化 leaf 当作完整复原。建议合并候选叶子到主树对应位置。

5. **根节点过于泛化（I）**：无法体现论文的独特三元结构，降低脚手架对 similar theory/evaluation/roadmap paper 的识别能力。

### M（Minor）：不阻塞的清晰度或维护性建议

1. **统计值缺失（M）**：10+ 个带分母的统计值是 scoping evidence 的良好来源（虽不进主统计池），建议记录在 evaluation-part leaf 中。

2. **证据条目 EV-002 颗粒度过粗（M）**：一条证据支撑 12 个节点，降低了证据审计的精确度。修复后应拆分为多条。

3. **Figure 4 / Figure 5 视觉核对未完成（M）**：A.4 已标注 `needs_manual_check`，建议 A2a 优先完成。

### 最终建议：**NEEDS FIX**

当前维度树将 6 类通用 pattern-field-schema 接口投影为 paper 的事实源，而非从原文三段式结构中忠实复原 paper 自身的 schema。核心缺失包括：11 个 RQT theory concept + impact chain 关系边、coding scheme + inter-rater reliability、6 条 roadmap action point、gap→roadmap 映射、和原文显式统计值。

当前 `review.md` 的 "原文模式候选叶子映射" 表已诚实标注所有候选叶子为 `not_verified`，这是正确的降级做法，但不应以此替代主树修复。建议按 Section 4 的骨架完成主树修复后再进入 A2a 精核阶段。

**修复优先级**：
1. P0（阻塞 A2a）：将主干从 b1--b5 通用接口改为 three-part (theory / evaluation / roadmap) 原文结构 → 加入 11 个 RQT concept leaf + impact 关系边。
2. P1（影响 A2a 精确性）：加入 evaluation-part 的 coding scheme + inter-rater reliability leaf。
3. P1（影响 A2a 完整性）：加入 6 条 roadmap action point leaf + gap identification leaf。
4. P2（提升可维护性）：细化 A.2 证据条目颗粒度、补记录统计值。

---

*审计完成时间：2026-06-29 | reviewer：deepseek | 基于所有上述读取文件的全文级交叉验证*
