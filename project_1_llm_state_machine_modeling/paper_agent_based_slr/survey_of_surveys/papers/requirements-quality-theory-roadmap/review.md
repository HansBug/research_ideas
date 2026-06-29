# Requirements quality research: a harmonized theory, evaluation, and roadmap

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Requirements quality research: a harmonized theory, evaluation, and roadmap |
| 年份 | 2023 |
| 类型 | research commentary / theory + evaluation + roadmap |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [RE](https://link.springer.com/journal/766) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | Requirements Engineering 期刊；Springer 正式 DOI；本地已有 PDF 与全文文本 |
| 阅读状态 | 已读全文文本-paper_content核验 |
| 证据等级 | 全文文本级；Fig. 2 / Fig. 4 / Fig. 5 图形细节待人工 PDF 核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 非典型 SLR；属于 requirements quality 的理论统一、57 篇文献状态评价与研究路线图 |
| SE 子领域 | Requirements Engineering / requirements quality |
| A1 角色 | 为 Paper2 的 researcher-defined meta-model、字段树、gap-to-roadmap 结构提供强脚手架先验。 |
| 是否目标证据池 | 否；只作为综述/路线图写法与元模型设计的脚手架样本。 |
| schema 缺口 | 暴露 `theory / evaluation / roadmap` 类型：不是普通 SLR/SMS，也不是纯 guideline；六类 pattern 需要允许“research commentary 不适用 / 转译后适用”。 |

**一句话结论**：这篇文献最值得迁移的不是 requirements quality 的具体结论，而是“先定义理论对象与关系 → 用对象级 codebook 评价现有研究 → 把缺口组织成 roadmap 与 tool-support 架构”的三段式。它可以直接启发 Paper2 如何把 researcher-defined meta-model 做成一等制品，而不是把抽取字段表当作临时表格。

## 2. 全文内容详读

### 2.1 背景 / 问题设定

原文的问题意识是：高质量需求能降低后续生命周期中缺陷传播和返工风险，但 requirements quality research 长期停留在“写作规则 / smell / metric”层面，缺少清晰理论结构来解释为什么某个质量因子重要。作者指出，现有需求质量研究主要存在三类缺口：

1. **规范性规则多，影响证据少**：大量研究提出 passive voice、句长、模板符合性等质量因子，但很少证明这些因子会如何影响后续活动。
2. **artifact-centric 偏置**：研究常只看需求文本本身，忽略需求会被哪些 agent 用于哪些 activity，以及 activity 的哪些 attribute 受到影响。
3. **实践相关性不足**：如果无法连接 activity impact、context factor 和 economic impact，质量因子很容易变成“为了规则而规则”，也难以被工业实践接受。

作者先回顾 software quality research 的演化：guideline / metric → quality model → quality meta-model → activity-based quality model → tool-supported operationalization。然后把这一演化映射到 requirements quality research，认为 RE 领域也需要从“文本质量因子”转向“需求实体对受影响活动的可测影响”。

### 2.2 Harmonized Requirements Quality Theory（RQT）

RQT 是本文核心贡献。它从 ABRE-QM 和 Quamoco 等 activity-based quality model 出发，形成一个可操作化的 requirements quality 理论。理论类型被作者定位为 explanatory + prescriptive：既解释 requirements quality 是什么，也规范后续研究应如何报告相关贡献。

核心对象可概括为四层：

1. **artifact-related 层**
   - `Entity`：需求制品或其组成部分，可按 specification、section、paragraph、sentence、requirement 等粒度分解。
   - `Factor`：对 entity 的规范性度量或质量因子，可进一步分解为 sub-factor。
   - `Entity-fact`：某个 entity 被某个 factor 评价后的事实，例如某条 user story 的 template conformance = missing role。
2. **activity-related 层**
   - `Agent`：参与活动的人、群体或自动化机制。
   - `Activity`：以 requirements entity 为输入并产生输出的 requirements-affected activity；不等同于传统 RE 活动分类。理解、解释、测试设计、实现等都可以作为活动或子活动。
   - `Attribute`：activity 的可测属性，例如 determinism、duration、agreement level、readability 等。
   - `Activity-fact`：某个 activity 在某个 attribute 上的状态。
3. **impact / context 层**
   - `Impact`：entity-fact 对 activity-fact 的影响关系。作者特别扩展了 impact 概念：它不必只是正 / 负 / 无影响，也不必是线性关系，可以是更复杂的经验关系或统计关系。
   - `Context factor`：影响 impact 关系的上下文因素，例如组织结构、过程模型、人员沟通方式、产品类型、工具环境等。
4. **economic 层**
   - `Cost` 与 `Resource`：activity-fact 的经济后果，例如时间、金钱或其他资源消耗。作者认为没有 economic impact，质量因子的工业接受度仍然不足。

文中 fictitious example 很关键：一条 user story 缺少 role，导致理解活动 determinism 下降，可能带来 ambiguous interpretation；但同一个 entity-fact 对 programming duration 可能没有显著影响。这个例子说明质量因子不能抽象地说“好 / 坏”，而要绑定到 activity、attribute、context 和 cost。

### 2.3 State of research evaluation

作者用 RQT 反向评价 requirements quality literature：研究问题是“requirements quality literature 如何报告 RQT 中的概念”。样本来自作者此前关于 requirements quality factors 的系统研究，共 57 篇 primary studies；这是 convenience sampling，但作者认为足以做理论状态初步评价。

评价流程包括：

1. 基于 RQT concepts 建立 extraction guideline。
2. 为每个 concept 设置一个或多个 categorical variable，用 codes 表示是否以及如何报告该 concept。
3. 第一作者对 57 篇论文编码；第二作者抽取约 10% 样本做 instrument validation。
4. 报告 inter-rater reliability：percentage agreement 83.3%，Cohen’s Kappa 54.2%，S-Score 76.8%。
5. 用 descriptive statistics 解释当前研究状态。

主要结果如下：

1. Entity 与 factor 在 57 篇中都被报告，但 24/57 的 entity 是 implicit，说明“requirement”这一对象粒度常常不清。
2. 17/57 不报告任何 activity impact，导致 quality factor 的实践相关性不足。
3. Agent 只在 14/57 中报告；attribute 只在 8/57 中报告。
4. impact evidence 以 hypothesized 为主，inductive 或 referenced 证据较少。
5. activities 即使被提到，也多数是 ad hoc elicited，而不是系统识别。
6. context factor、cost、resource 几乎被忽略；cost/resource 即使出现，也主要是推测或引用，而非经验测量。

作者的解释是：requirements quality theory 已经隐含存在于文献中，但大多数研究只覆盖 artifact-centric 部分，activity-centric、context 和 economic 部分覆盖不足。这会削弱外部效度、实践相关性和工业采纳。

### 2.4 Roadmap

roadmap 基于 Femmer 等人的旧路线图，并结合本次状态评价扩展为六条研究流：

1. **Artifact and usage model**
   - artifact model 已有 AMDiRE 等基础。
   - activity / agent model 仍需补强，特别是 requirements-affected activities 及其 attributes。
   - 作者强调 interpretation sub-activity 可能嵌入几乎所有 requirements-affected activities，这解释了 ambiguity 研究为何突出。
2. **Taxonomy of quality factors**
   - requirements quality factor ontology 是已有进展。
   - 仍需持续迭代，把 quality factor、dataset、automation approach 等收进中央仓库。
3. **Taxonomy / framework of impacts**
   - 作者认为“taxonomy of impacts”不足，应升级为 impact framework。
   - impact 可建模为 regression problem：一侧是 entity/context 的量化，另一侧是 activity attribute 的量化；可用 Bayesian data analysis 等工具估计复杂关系。
4. **Context factors**
   - 需要建立 RE 专属 context factor 集合，而不是直接照搬 generic software engineering context。
   - context-driven reporting 可以让不同研究的数据在限定上下文中组合。
5. **Economic impact**
   - 质量因子需要连接到 resource 和 cost，才能支持工业决策。
   - economic impact 是复杂但高优先级方向。
6. **Tool support**
   - 工具目标是估计 requirements entities 及其 context 对 requirements-affected activities attributes 的影响。
   - 工具需要 entity 接口、agent/context 信息、organization/context 信息、entity/context characterization、impact prediction model 和 economic impact quantification。
   - 自动化模块包括 automatic entity characterization 与 automatic impact prediction。

这一路线图不是简单 future work 清单，而是从理论对象缺口、评价缺口、数据需求和工具架构逐步推导出来的 roadmap。

### 2.5 Quality factors / impacts / context / economic / tool support 的细化价值

这篇对 Paper2 的字段启发非常强：

- **quality factors**：不要只记录“是否有字段 / 是否遵守规则”，而要把字段视为可度量 factor，并说明它作用于哪个 entity 粒度。
- **impacts**：每个 factor 的价值应通过 impact relationship 连接到后续 activity attribute；Paper2 可类比为“某个抽取字段 / 审计字段如何影响后续统计、候选发现或审稿复核”。
- **context**：impact 不能脱离上下文。Paper2 中的 context 应至少包括 SE 子领域、综述类型、模型/provider、prompt 版本、全文可得性、研究者经验、目标 venue、样本规模、证据类型。
- **economic**：应把人工时间、LLM token/cost、复核成本、回填成本、错误修复成本作为 resource/cost 字段，而不是只报告“流程更透明”。
- **tool support**：最终工具不只是生成 review 文本，而应连接 corpus、字段 schema、context characterization、impact/finding prediction、审计与人类裁决。

### 2.6 Threats to validity

作者按 Wohlin 与 Molléri 的 threat 分类报告：

1. **Internal validity**：样本来自先前 systematic study，属于 convenience sampling；作者认为对初始理论足够，但不是全域饱和结论。
2. **Construct validity**：RQT 概念严格对齐成熟 software quality theories，缓解构念与测量不一致风险。
3. **Extraction difficulty**：由于被调查文献并没有按 RQT 报告，许多概念只能从隐含表达中抽取；作者用独立标注与 reliability metrics 缓解。
4. **External validity**：样本约束在 empirical contributions；非经验性理论工作可能提供 deductive evidence，例如基于语言学理论解释 nominalization 的影响，因此关于 impact evidence 类型的结论不能无限外推。

对本地使用而言，最大风险是：这是一篇 research commentary + theory/evaluation/roadmap，而不是标准 tertiary study；它能提供 meta-model 启发，但不能作为 LLM/agent-based SLR 的直接有效性证据。

## 3. 六类 pattern 抽取

| pattern | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 本文不是普通 SLR 的多 RQ 结构，而是围绕“理论统一 + 现状评价 + roadmap”组织；唯一显式评价 RQ 是 requirements quality literature 如何报告 RQT concepts。 | `paper_content.txt` Page 2 贡献列表；Page 7 研究问题；Page 8--9 结果解释。 | 可迁移为 Paper2 的 theory-driven evaluation RQ：先定义 meta-model，再问现有文献/运行制品如何覆盖这些概念。 | roadmap/commentary 不适合直接迁移为 PICO 或效果评价型 RQ；不能把其 57 篇样本当作目标 SLR/SMS 证据池。 |
| dimension pattern | 维度核心是 RQT concepts：Entity、Factor、Entity-fact、Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource；编码还包括 explicitness、factor form、impact evidence、impact modality 等。 | `paper_content.txt` Page 4--6 RQT 与 Table 1；Page 7--8 instrument design；Page 8 Fig. 4 结果说明。 | 高度可迁移到 Paper2 的 researcher-defined meta-model：字段不是平铺标签，而是对象、关系、属性、上下文和经济后果的结构。 | 具体概念属于 requirements quality；Paper2 需重命名为 SLR/SMS 对象，如 Paper、Evidence field、Analysis activity、Finding claim、Review context、Human/LLM agent。 |
| finding pattern | findings 不是单纯频次，而是“理论覆盖缺口 → 实践相关性风险 → roadmap 需求”：artifact-centric 概念覆盖好，activity/context/economic 概念覆盖差。 | `paper_content.txt` Page 8--9 Study results / Interpretation；Page 11--12 Conclusion。 | 可迁移为 gap-to-action finding pattern：统计覆盖率要进一步解释为方法风险和行动方向。 | 本文 finding 是 requirements quality 领域事实，不可转写为 Paper2 领域结论；只能迁移推理结构。 |
| evidence presentation pattern | 证据呈现包括 57 篇样本来源、extraction guideline、categorical codes、双人 reliability、descriptive statistics、Fig. 4 concept coverage、replication package。 | `paper_content.txt` Page 7--8 Study design；Page 8 Study results；Page 7 replication package footnote。 | 可迁移为 Paper2 的审计证据链：字段合同、抽取指南、编码可靠性、分布图和复现实验包应共同支撑结论。 | 本轮未人工核对 Fig. 4 图形数值；正式引用数字前需回 PDF 和 replication package。 |
| validity / threat pattern | 明确区分 internal、construct、external validity；重点是 convenience sampling、隐式概念抽取、样本仅 empirical contributions。 | `paper_content.txt` Page 9--10 Threats to validity。 | 可迁移到 Paper2：若研究者定义 meta-model 后评价文献或 agent output，必须说明样本来源、构念对齐、隐式字段抽取和外推边界。 | 本文 threat 主要面向 survey of literature，不覆盖 LLM provider drift、prompt variance、run record 缺失等 Paper2 专属风险。 |
| report structure pattern | 结构是 Introduction → Software quality research evolution → RQT theory → State-of-research survey → Roadmap → Conclusion。 | `paper_content.txt` Page 2 manuscript organization；全文各节。 | 非常适合 Paper2 的方法故事：相关领域演化/理论 → 本文元模型 → 现状/运行评价 → roadmap/tooling。 | research commentary 的叙事性较强，不等同标准 SLR/SMS 报告结构；若 Paper2 写实证评价，需要额外方法、实验和威胁章节。 |

## 4. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可迁移贡献 | 具体启发 | 风险边界 |
|---|---|---|---|
| A1-M0 主题 / RQ / 综述元模型设定 | RQT 表明元模型应先定义对象、关系、活动、上下文、经济后果。 | Paper2 的 researcher-defined meta-model 不应只是字段列表；应显式定义 `研究对象 → 字段/因子 → 分析活动 → 候选发现/裁决 → 成本/上下文` 的关系。 | RQT 对象不能原样套用；必须由 Paper2 研究者按 SE SLR/SMS 任务重建。 |
| A1-M1 脚手架挖掘 / 种子探测 | 本文用 software quality 演化史和 ABRE-QM/Quamoco 作为脚手架来源。 | Paper2 可用 survey-of-surveys、baseline、guideline 和 pilot papers 提供候选维度，但需记录采纳/拒绝理由。 | 脚手架不是目标领域证据；不能把 roadmap 文献的判断当最终 finding。 |
| A1-M2 维度模式批准 | RQT Table 1 类似字段合同，定义每个 concept 的含义与来源。 | Paper2 需要为每个抽取字段写操作化定义、取值空间、缺失语义、证据要求、上下游用途。 | 若字段没有后续用途，会退化为规范性清单，重蹈 requirements quality 的“impact unknown”问题。 |
| A1-M3 论文收集与概览 | 本文明确 target population、sample 来源和 convenience sampling 边界。 | Paper2 的 A1-M3 应记录候选池来源、全文状态、样本继承关系、去重和纳排边界，不能只给最终列表。 | convenience sample 只能支撑初步评价；若 Paper2 要写更强结论，必须扩大或明确抽样边界。 |
| A1-M4 字段级证据抽取与模式演化 | 本文把 RQT concepts 变成 categorical variables，并用编码指南抽取。 | Paper2 可把 `schema field` 设计为可编码变量，并要求每个字段绑定 source anchor、implicit/explicit、uncertainty 和修订触发原因。 | 隐式字段抽取会引入主观性，必须设计抽查、一致性或裁决机制。 |
| A1-M5 统计分析 | 本文用 descriptive statistics 展示 concept coverage，并区分统计结果和解释。 | Paper2 的分布、交叉表、覆盖率代理应记录字段版本、样本范围和分析限制；统计观察不能直接升级为最终发现。 | 图表数字需 PDF/数据包核对；统计覆盖不等于理论正确或实践有效。 |
| A1-M6 候选发现形成 | 本文把 coverage gap 转成 roadmap streams：activity model、quality factor ontology、impact framework、context、economic impact、tool support。 | Paper2 可把统计缺口转成候选 finding / action item / roadmap，而不是停留在“某字段出现率低”。 | roadmap 是候选行动，不是已经验证的解决方案；后续仍需研究者质疑和裁决。 |

## 5. 可迁移理论 / 评价 / roadmap 字段树

### 5.1 理论元模型字段树（迁移版）

```text
theory_meta_model
├── object_layer
│   ├── entity_type            # 研究对象粒度；Paper2 可对应 paper / claim / evidence item / field row
│   ├── entity_decomposition   # 对象是否可分解；例如论文→章节→表格→字段锚点
│   ├── factor_or_field        # 评价/抽取因子；例如 evidence availability、claim support、review type
│   └── entity_fact            # 某对象在某字段上的取值与证据
├── activity_layer
│   ├── agent                  # human researcher / LLM agent / tool / reviewer
│   ├── activity               # screening / extraction / coding / analysis / finding adjudication
│   ├── activity_attribute     # accuracy、agreement、duration、traceability、determinism、reviewability
│   └── activity_fact          # 某活动属性的观测结果
├── impact_layer
│   ├── impact_relation        # entity_fact 如何影响 activity_fact
│   ├── impact_evidence        # hypothesized / referenced / inductive / experimental / replay-based
│   ├── impact_modality        # necessary / possible / conditional / no observed impact
│   └── impact_model_form      # categorical / linear / regression / Bayesian / qualitative rationale
├── context_layer
│   ├── domain_context         # SE 子领域、综述类型、目标 venue、数据可得性
│   ├── process_context        # 人审 gate、schema version、抽取流程、回填流程
│   ├── model_tool_context     # provider、model_id、prompt、toolchain、run date
│   └── organization_context   # 团队角色、研究者经验、复核资源
└── economic_layer
    ├── resource               # time / money / token / human attention / review bandwidth
    ├── cost                   # 采集、抽取、复核、回填、修错成本
    └── cost_link              # activity_fact 到 resource cost 的关系
```

### 5.2 状态评价字段树（迁移版）

```text
state_evaluation
├── population_and_sample
│   ├── target_population
│   ├── sample_source
│   ├── sampling_strategy
│   └── inclusion_boundary
├── codebook
│   ├── concept_to_variable_map
│   ├── code_definition
│   ├── missing_value_semantics
│   └── implicit_vs_explicit_rule
├── extraction_process
│   ├── extractor_roles
│   ├── training_set
│   ├── validation_sample
│   ├── disagreement_resolution
│   └── replication_package
├── reliability
│   ├── agreement_metric
│   ├── agreement_value
│   └── metric_limitation
├── descriptive_statistics
│   ├── concept_coverage
│   ├── evidence_type_distribution
│   ├── context_coverage
│   └── economic_coverage
└── interpretation
    ├── artifact_centric_bias
    ├── activity_gap
    ├── context_gap
    ├── economic_gap
    └── practical_relevance_risk
```

### 5.3 Roadmap 字段树（迁移版）

```text
roadmap_stream
├── stream_id
├── stream_name
├── triggering_gap             # 来自 state_evaluation 的哪个缺口
├── theory_concepts_covered    # 补 theory_meta_model 哪些节点
├── required_artifact          # taxonomy / reference model / framework / dataset / tool module
├── required_empirical_data    # 需要什么数据才能验证 impact
├── automation_candidate       # 哪些部分可由工具或 agent 支持
├── human_gate                 # 哪些决策必须由研究者批准
├── economic_or_practice_value # 对成本、实践采纳或审稿可信度的作用
└── residual_risk              # 仍不能证明什么
```

## 6. 对 Paper2 的启发与风险

### 6.1 强启发

1. **researcher-defined meta-model 应成为第一贡献对象**
   - RQT 说明，高质量研究不是先堆字段，而是先定义理论对象、对象之间的关系、影响路径和成本后果。
   - Paper2 可把“研究者定义综述元模型”写成类似 RQT 的对象图：paper / requirement-like evidence entity、field/factor、agent、activity、attribute、candidate finding、context、cost。

2. **字段必须绑定下游 activity impact**
   - requirements quality 研究的问题是 factor impact unknown。
   - Paper2 不能只说某字段“应该抽取”；要说明它服务于哪类后续活动：筛选复核、统计分析、候选发现生成、反向证据检查、审稿人复核、run record 审计等。

3. **从理论到评价再到 roadmap 的三段式可直接复用**
   - 本文结构提供一个稳健写法：先提出理论/元模型，再评价当前研究/制品覆盖，最后将缺口转成 roadmap / tool architecture。
   - Paper2 可采用同构结构：meta-model → agent workflow / corpus dry-run coverage → schema evolution / evidence chain roadmap。

4. **activity attribute 是评价设计关键**
   - RQT 提醒：如果不定义 activity 的 measurable attribute，就无法评价 impact。
   - Paper2 的评价维度应显式包括 traceability、field correctness、source-anchor accuracy、reviewer agreement、revision effort、candidate finding precision、human adjudication cost 等。

5. **context 与 economic impact 是审稿人会追问的边界**
   - Paper2 若只报告准确率或文本质量，会忽略 provider/model drift、领域差异、全文可得性、人工复核成本等 context/resource。
   - 可把 context/cost 做成 run record 与 evaluation table 的必填字段。

6. **tool support 不能只是文本生成器**
   - 本文的 tool architecture 以 entity/context characterization 和 impact prediction 为核心。
   - Paper2 的工具形态应更像 evidence engineering environment：管理 corpus、schema、field evidence、statistics、candidate findings、human challenges、process evidence 和 redaction。

### 6.2 主要风险

1. **不要把本文当作 LLM/agent SLR 的直接 baseline**
   - 它不研究 LLM，不研究自动化系统综述，也不评价 agent workflow。
   - 只能作为理论结构和 roadmap 写法先验。

2. **不要过度形式化而缺少实证闭环**
   - RQT 的强处是理论结构，但作者也承认许多 impact/context/economic 关系难以测量。
   - Paper2 如果只画 meta-model 而没有最小闭环样例、字段证据表和裁决日志，会被审稿人质疑为“强协议 / 弱证据”。

3. **implicit concept extraction 会引入主观性**
   - 本文通过双人编码和 reliability metrics 缓解。
   - Paper2 若让 agent 抽取隐式字段，必须设置人工抽查、冲突裁决和不确定性记录。

4. **roadmap 不是已验证方案**
   - 本文提出 impact framework、economic stream 和 tool support，但不是全部实现或验证。
   - Paper2 使用 roadmap 写法时，应把 future direction 与已完成 evidence 严格区分。

5. **context/economic 字段会增加工作量**
   - 这些字段最有价值，但也最难稳定抽取。
   - Paper2 需要在字段树中区分必填、可选、待人工补证和不适用，避免 schema 过重导致真实运行失败。

## 7. 待复核

1. **PDF 图形核对**：Fig. 2 RQT 概念关系、Fig. 4 concept coverage 分布、Fig. 5 tool-support architecture 需回 [paper.pdf](./paper.pdf) 做图形级核对后再用于正式图表引用。
2. **数值核对**：24/57、17/57、14/57、8/57、83.3%、54.2%、76.8% 等数值来自 `paper_content.txt`；正式写作前建议核对 PDF 与 replication package。
3. **replication package**：原文 Zenodo package 未在本轮打开；后续若要复用 codebook 或 codes，需要下载并检查字段定义。
4. **RQT tool repository**：原文提到 GitHub tool；本轮未核验仓库状态，不能写成当前可用工具事实。
5. **对 Paper2 字段树的落地**：本文提供强先验，但 Paper2 仍需单独冻结 SE SLR/SMS 专属对象、活动、context 和 cost 字段，不能直接复制 requirements quality 概念。
