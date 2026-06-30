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
| 证据等级 | 全文文本级；Fig. 2 / Fig. 4 / Fig. 5 图形细节待人工原文核对 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 综述类型 | 非典型 SLR；属于 requirements quality 的理论统一、57 篇文献状态评价与研究路线图 |
| SE 子领域 | Requirements Engineering / requirements quality |
| A1 角色 | 为 Paper2 的 researcher-defined meta-model、字段树、gap-to-roadmap 结构提供强脚手架先验。 |
| 是否目标证据池 | 否；只作为综述/路线图写法与元模型设计的脚手架样本。 |
| schema 历史观察 | 暴露 `theory / evaluation / roadmap` 类型：不是普通 SLR/SMS，也不是纯 guideline；六类 pattern 需要允许“research commentary 不适用 / 转译后适用”。 |

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

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
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

## 历史草稿（已迁移，不作事实真源）：旧第 5 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

### 历史草稿（已迁移，不作事实真源）：旧第 5.1 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

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

### 历史草稿（已迁移，不作事实真源）：旧第 5.2 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

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

### 历史草稿（已迁移，不作事实真源）：旧第 5.3 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

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

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 leaf / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生 schema。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__codex.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__codex.md)、[../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__claude.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__claude.md)、[../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__deepseek.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修 / needs repair”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 supplementary 精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `requirements-quality-theory-roadmap` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；通读 14 页全文（Page 1–Page 14 含 References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两份均已读，且交叉核对元信息 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅基于 text 审计，未做 PDF 版面核验（图 Fig. 2/4/5、Table 1 字段对齐留待 A2a） |
| 原文类型 | research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） |
| 被编码样本单位 | primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） |
| 样本数量 / 分母 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） |
| 原生树类型 | **维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 |
| 主统计池资格 | **局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 needs repair；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、supplementary 风险进入 A2a。 |

---

### 1. 原文证据阅读说明

实际读取的本地文件与覆盖范围：

1. `bibtex.bib` 完整 — 锁定 Frattini et al. 2023, *Requirements Engineering* 28(4):507–520, DOI 10.1007/s00766-023-00405-y。
2. `metadata.json` 完整 — 已知 `eligible_for_statistical_synthesis: false`、`evidence_role: theory_roadmap_schema_seed`、`systematic_evidence_status: non_systematic_or_boundary_anchor`，与本审计判定一致。
3. `paper_content.txt` 通读 Page 1–14 全文，含摘要、§1–§6、References。
4. `paper.pdf` 未在本轮打开（Fig. 2 RQT 概念图、Fig. 3 example 实例化、Fig. 4 codes 分布柱状、Fig. 5 tool architecture、Table 1 concept origins 留待 A2a 版面核验）。
5. `review.md` 完整阅读（含 §1–§7 与"维度树复原"与 A.1–A.4 附录）。

关键证据锚点（5–12 条）：

1. **Page 2，§1 contributions**："(1) A harmonized requirements quality theory… (2) A survey of requirements quality research… (3) A consequent research roadmap"。三段式贡献声明，决定森林型结构。
2. **Page 4，§3.1 + Fig. 2 + Table 1**：RQT 概念 = `Entity / Factor / Entity-fact / Agent / Activity / Attribute / Activity-fact / Impact / Context factor / Cost / Resource`，共 11 concepts，每个有 origin 引用。这是**树 A**。
3. **Page 7，§4.1**："a sample of 57 primary studies… non-probabilistic, more specifically convenience sampling"。锁定样本单位、分母与抽样性质。
4. **Page 7，§4.2 instrument design**："Each concept of the RQT was associated with one or more categorical variables, each containing a set of codes that represented if and how the concept was reported. The codes were created ad hoc in the first iteration of extraction and refined based on discussions and theoretical background in the second iteration."。**这是树 B 的存在证据**。
5. **Page 7，§4.2 entity codes 示例**："codes that represent how the concept entity is reported are, for example, explicit and implicit"。
6. **Page 7，§4.2 factor codes 示例**："the codes of the concept Factor were split into two groups, representing both the explicitness… and the form"。
7. **Page 7–8，§4.2 reliability**：percentage agreement 83.3%、Cohen's Kappa 54.2%、S-Score 76.8%；两人编码、6 篇约 10% 验证子样（其中 2 篇训练、4 篇正式计算）。
8. **Page 8，§4.3 results**：分子分母枚举 — Entity implicit 24/57（42.1%）；Impact N/A 17/57（29.8%）；Agent 14/57（24.6%）；Activity ad hoc 37/40（92%）；Attribute 8/57（14%）；Impact evidence hypothesized 19/40、inductive 11/40、referenced 10/40；Context factor 范围 0%–24.6%；Cost 9/57（15.8%）；Resource 5/57（8.8%）。
9. **Page 8，§4.3 impact dimensions**："We grouped the codes classifying how impact is reported into four distinct dimensions, two of which are reported here…"。Impact 有 **4 个子维度**：evidence、modality、generality、frame of reference；其中后两个原文未报告但作者声明编码存在。
10. **Page 9–10，§5 roadmap**：6 streams = artifact/usage model、taxonomy of quality factors、impact framework（升级自 taxonomy of impacts）、context factors、economic impact、tool support。
11. **Page 11，§5.6 + Fig. 5**：tool architecture 含 entity characterization + impact prediction model；并提到 GitHub `JulianFrattini/rqt-tool`（本轮未核验）。
12. **Page 8，§4.5 threats**：external validity = 样本仅 empirical contributions；construct = 隐式 concept 抽取困难。

未做 PDF 版面核验的部分：Fig. 4 柱状图实际数值与文本数字是否一致；Table 1 origin 引用列；Fig. 2 关系箭头方向；replication package（Zenodo 8167598）字段定义。

---

### 2. 样本单位与字段来源判定

**Q1 — 原文逐项编码的对象是什么？**
是 requirements quality 文献中的 primary study（一篇一项）。Page 7 明确："a sample of 57 primary studies"，每篇被 RQT codebook 编码一次。

**Q2 — 作者是否做了系统检索 / 纳排 / 抽取 / 编码方案？**
- 系统检索：**否，未新做**。样本直接借用作者团队前作 Frattini et al. 2022 quality-factor ontology study（arXiv 2206.05959）的 57 篇 sample，作者明确标注为 convenience sampling。
- 抽取方案：**有**。基于 RQT concepts 构建 extraction guideline，每个 concept 关联 ≥1 个 categorical variable，每个 variable 含若干 codes（codes 在第一轮 ad hoc 生成，第二轮基于讨论与理论背景精炼）。
- 编码方案：第一作者全样本编码，第二作者在 6 篇随机子样（2 篇训练 + 4 篇正式）独立编码，计算 percentage agreement / Cohen's Kappa / S-Score。

**Q3 — 字段来源**：来自 §4.2 extraction guideline 与 §4.3 results 中显式提到的 codes、replication package（Zenodo），与 §3 RQT 11 concepts 的对应映射。

**Q4 — RQ 与样本单位的关系**：唯一显式 RQ = "How are the concepts of the requirements quality theory reported in requirements quality literature?"（Page 7）。RQ 把 RQT 概念当作**编码字段集合**，把 57 篇当作**被编码样本**，结果是**字段在样本中的报告频次与方式分布**。RQ 本身不构成树根，而是把树 A（RQT 概念）作为字段、应用到样本上、产出统计观察。

**Q5 — 是否要降级？**
**部分降级**：
- 该文不是新做的 SLR/SMS，而是 viewpoint + 内部 survey + roadmap。
- 但它有真实样本（n=57）、有 codebook、有 reliability、有 descriptive statistics。
- 对本文自身而言：可作内部统计；对 Paper2 而言：仅作 `schema_seed / methodological_seed / boundary_anchor`，不进入跨论文 SLR/SMS 主统计池。这与 metadata.json `eligible_for_statistical_synthesis: false` 一致。

---

### 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**（A + B + C 三树），其中 **树 B = 样本编码维度树**，是 A1-DT v2 关注的真正主树。

#### 树 A：RQT 概念元模型（§3, Fig. 2, Table 1）

```text
RQT 概念元模型 (theory layer)
├── artifact-related layer
│   ├── Entity            — 需求制品或其组成（specification/section/paragraph/sentence/requirement）
│   ├── Factor            — 对 entity 的规范性度量；可分解为 sub-factor
│   └── Entity-fact       — entity × factor 的具体取值（如 user story 的 conformance = missing role）
├── activity-related layer
│   ├── Agent             — 人、群体或自动化机制
│   ├── Activity          — 以 entity 为输入并产生输出的 requirements-affected activity
│   ├── Attribute         — activity 的可测属性（determinism、duration、readability …）
│   └── Activity-fact     — activity × attribute 的具体取值
├── impact / context layer
│   ├── Impact            — entity-fact 对 activity-fact 的关系（可分类 / 线性 / 非线性 / 回归）
│   └── Context factor    — 影响 impact 的外部因素（组织、过程模型、产品、工具、人员）
└── economic layer
    ├── Cost              — activity-fact 的经济量级
    └── Resource          — 受影响的资源类型（time / money / …）
```

#### 树 B：§4 extraction codebook（**真正的样本编码维度树**）

> 这是 §4.2 extraction guideline 中"每个 RQT concept 关联 ≥1 个 categorical variable + codes"的真实复原。Page 8 §4.3 提到的所有 codes 与分母都来自此树。文本明确列出的 codes 完整列出；文本未展开但暗示存在的 codes 标 `待核验 (Zenodo replication package)`。

```text
[B] Sample coding tree — RQT codebook applied to 57 primary studies
│
├── Entity reporting
│   └── entity.explicitness ∈ {explicit, implicit}
│       — Page 7 显式定义；Page 8 implicit = 24/57 = 42.1%
│
├── Factor reporting
│   ├── factor.explicitness ∈ {explicitly_reported, referenced_from_another_publication}
│   │   — Page 7 §4.2 显式
│   └── factor.form ∈ {textual_description, logical_or_mathematical_formula}
│       — Page 7 §4.2 显式
│
├── Entity-fact reporting     ⟵ 文本未展开 codes（待 Zenodo 核验）
│
├── Agent reporting
│   └── agent.presence ∈ {reported, not_reported}
│       — Page 8 reported = 14/57 = 24.6%
│
├── Activity reporting
│   ├── activity.presence ∈ {reported, not_reported}
│   │   — 当 reported 时分母 = 40
│   └── activity.elicitation_mode ∈ {ad_hoc, systematic}
│       — Page 8 ad_hoc = 37/40 = 92%
│
├── Attribute reporting
│   └── attribute.presence ∈ {reported, not_reported}
│       — Page 8 reported = 8/57 = 14%
│
├── Activity-fact reporting   ⟵ 文本未展开 codes（待 Zenodo 核验）
│
├── Impact reporting          ⟵ 4 dimensions（only 2 reported in paper）
│   ├── impact.presence ∈ {reported, N_A}
│   │   — Page 8 N/A = 17/57 = 29.8%；reported 分母 = 40
│   ├── impact.evidence ∈ {hypothesized, inductive, referenced}
│   │   — Page 8 hypothesized 19/40、inductive 11/40、referenced 10/40
│   ├── impact.modality ∈ {necessary, possible}
│   │   — Page 8 "balanced between necessary and possible"
│   ├── impact.generality          ⟵ 编码存在但 Page 8 "yielded no additional insight"
│   └── impact.frame_of_reference  ⟵ 编码存在但 Page 8 "yielded no additional insight"
│
├── Context factor reporting
│   └── context_factor.sub_category ∈ {tool, product, organization, process, people, …}
│       — Page 8 tool = 0/57；product = 14/57 = 24.6%；其他子类待 Zenodo 核验
│
├── Cost reporting
│   ├── cost.presence ∈ {reported, not_reported}
│   │   — Page 8 reported = 9/57 = 15.8%
│   └── cost.evidence ∈ {hypothesized, referenced, empirical}
│       — Page 8 "only hypothesized or referenced, never determined empirically"
│
└── Resource reporting
    ├── resource.presence ∈ {reported, not_reported}
    │   — Page 8 reported = 5/57 = 8.8%
    └── resource.type ∈ {money, time, …}
        — Page 8 "money and time are mentioned"；其他类型待 Zenodo 核验
```

#### 树 C：§5 roadmap streams（候选 finding 树）

```text
[C] Roadmap streams
├── 5.1 Artifact and usage model       — 含 reference activity model & attributes
├── 5.2 Taxonomy of quality factors    — 基于 quality-factor ontology
├── 5.3 Impact framework               — 升级自原 taxonomy of impacts；引入回归 / Bayesian
├── 5.4 Context factors                — RE 专属 context factor 集合
├── 5.5 Economic impact                — 把 activity-fact 关联到 cost/resource
└── 5.6 Tool support                   — entity & context characterization + impact prediction
```

#### 当前 review.md 缺失的部分

- 把 §4 codebook（树 B）当作"原文 schema 主树"完整列出。
- 把 Impact 的 4 个子维度（evidence / modality / generality / frame_of_reference）显式列叶。
- 把 Factor 的 explicitness × form 两组 codes 显式列叶。
- 把 Cost 与 Resource 的 sub-codes（evidence、type）显式列叶。

---

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `B.entity.explicitness` | 实体显式性 | Entity reporting | §4.2 显式给出 | 一篇文献是否清晰报告 entity 的 scope 与 form | {explicit, implicit} | 完整枚举 | 不报告时默认 implicit | 分子/57；implicit = 24/57 | "术语模糊"型 gap finding | 可迁移为 Paper2 中字段 explicit/implicit 二分；不迁移 RE 领域结论 |
| `B.factor.explicitness` | 因子显式性 | Factor reporting | §4.2 显式 | 因子是本文显式定义还是引用其他文献 | {explicitly_reported, referenced_from_another_publication} | 完整枚举 | 所有 57 篇都报告 factor，无缺失 | 分子/57 | 引用链型 finding 候选 | 可迁移结构；不迁移 RE factor 具体集合 |
| `B.factor.form` | 因子形式 | Factor reporting | §4.2 显式 | 因子是文字描述还是数学/逻辑公式 | {textual_description, logical_or_mathematical_formula} | 完整枚举 | 默认 textual | 分子/57 | 形式化程度型 finding | 可迁移；Paper2 字段可同构分"文本/形式化" |
| `B.agent.presence` | Agent 报告与否 | Agent reporting | §4.3 | 是否报告活动中的 agent | {reported, not_reported} | 布尔 | not_reported | 14/57 = 24.6% | activity-side gap finding | 可迁移 |
| `B.activity.presence` | Activity 报告与否 | Activity reporting | §4.3 | 是否报告 impacted activity | {reported, not_reported} | 布尔 | not_reported；进入 17/57 N/A | 40/57 reported | gap finding | 可迁移 |
| `B.activity.elicitation_mode` | Activity 识别方式 | Activity reporting | §4.3 | activity 是 ad hoc 引出还是系统性识别 | {ad_hoc, systematic} | 完整枚举 | 仅当 activity reported 时生效，分母 40 | 37/40 = 92% ad_hoc | "非系统性 activity"型 finding | 可迁移 |
| `B.attribute.presence` | Attribute 报告与否 | Attribute reporting | §4.3 | 是否报告 activity 的可测属性 | {reported, not_reported} | 布尔 | not_reported | 8/57 = 14% | measurement gap finding | 可迁移 |
| `B.impact.presence` | Impact 报告与否 | Impact reporting | §4.3 | 是否报告 factor → activity 的 impact | {reported, N_A} | 布尔 | N/A 计 17/57 | reported 分母 = 40 | core gap finding | 可迁移 |
| `B.impact.evidence` | Impact 证据类型 | Impact reporting | §4.3 | impact 关系的证据基础 | {hypothesized, inductive, referenced} | 完整枚举 | 仅当 impact reported；分母 40 | 19 / 11 / 10 of 40 | "证据等级"型 finding | 可迁移为 Paper2 evidence_type 字段 |
| `B.impact.modality` | Impact 模态 | Impact reporting | §4.3 | impact 是必然还是可能 | {necessary, possible} | 完整枚举 | impact reported 子集 | "balanced" 文本表述 | "确定性 vs 可能性"分布 finding | 可迁移 |
| `B.impact.generality` | Impact 普适性 | Impact reporting | §4.3 提到但未展开 | impact 是普遍还是上下文特异 | 待核验（Zenodo） | 待核验 | 文本声明"no additional insight"故未报告 | 不进入本文统计 | A2a 补叶后可作 finding 候选 | 取值空间未核验前不得统计 |
| `B.impact.frame_of_reference` | Impact 参照系 | Impact reporting | §4.3 提到但未展开 | impact 的参照对象 | 待核验（Zenodo） | 待核验 | 同上 | 不进入本文统计 | A2a 补叶后可作 finding 候选 | 同上 |
| `B.context_factor.sub_category` | Context 子类 | Context factor reporting | §4.3 | 报告了哪类 context（tool / product / organization / process / people …） | tool, product (named), other（待 Zenodo 补全） | 层级枚举 | 多数为 0 报告 | tool=0；product=14/57；其他待核 | "context 忽视"型 gap finding | 可迁移为 Paper2 context 多类字段 |
| `B.cost.presence` | Cost 报告与否 | Cost reporting | §4.3 | 是否报告经济成本 | {reported, not_reported} | 布尔 | not_reported | 9/57 = 15.8% | economic gap finding | 可迁移 |
| `B.cost.evidence` | Cost 证据类型 | Cost reporting | §4.3 | cost 的证据基础 | {hypothesized, referenced, empirical(=0 在本样本)} | 完整枚举 | cost reported 子集；分母 9 | "never empirically determined" | empirical-evidence gap | 可迁移 |
| `B.resource.presence` | Resource 报告与否 | Resource reporting | §4.3 | 是否报告 resource 类型 | {reported, not_reported} | 布尔 | not_reported | 5/57 = 8.8% | resource gap finding | 可迁移 |
| `B.resource.type` | Resource 类型 | Resource reporting | §4.3 | 受影响 resource 的具体类型 | {money, time, …待 Zenodo} | 部分枚举 | resource reported 子集；分母 5 | money / time 文本提及 | 资源类型分布 finding | 可迁移；类型空间需 A2a 扩展 |
| `B.entity_fact.codes` | Entity-fact codes | Entity-fact | §3 概念存在；§4 文本未展开 | entity × factor 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 entity + factor 联合 | 不进入本文统计 | 复合事实型 finding 入口 | 取值空间未核验前不得统计 |
| `B.activity_fact.codes` | Activity-fact codes | Activity-fact | §3 概念存在；§4 文本未展开 | activity × attribute 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 activity + attribute 联合 | 不进入本文统计 | 同上 | 同上 |

---

### 5. 关系边表

本文 RQT 是**显式关系型模型**（Fig. 2 即关系图）。关系边来自树 A（概念模型），而非树 B（codebook）。树 B 是字段-codes 平面表，本身没有关系边。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `R1.entity_compose` | Entity | decomposes_into | Entity (sub-entity) | 递归 entity 类型 | 单层 entity 不报告 sub-entity | §3.1 Page 4 | 表达需求粒度层级 |
| `R2.factor_compose` | Factor | decomposes_into | Factor (sub-factor) | 递归 factor 类型 | 单层 factor 不报告 sub-factor | §3.1 Page 4（Antinyan 例） | 表达复合因子 |
| `R3.entity_fact` | Entity × Factor | composes | Entity-fact | 由 entity 与 factor 联合定义 | 未取值时不存在 entity-fact | Table 1 Page 5 | 编码具体观测 |
| `R4.activity_compose` | Activity | decomposes_into | Activity (sub-activity) | 递归 | 单层 activity 不分解 | §3.1 Page 4–5 | 表达 understanding 等子活动 |
| `R5.activity_fact` | Activity × Attribute | composes | Activity-fact | 由 activity 与 attribute 联合定义 | 未取值时不存在 activity-fact | Table 1 Page 5 | 编码活动观测 |
| `R6.impact` | Entity-fact | impacts | Activity-fact | 关系模型：categorical / linear / regression / Bayesian | impact 不报告 = N/A | §3.1 generalised impact, Page 5 | 核心因果/关系边 |
| `R7.context_modulates` | Context factor | modulates | Impact (Entity-fact→Activity-fact 关系) | 同 impact 取值空间 | context 不报告 = 假设统一上下文 | §3.1 Page 5 + 例 Page 6 | 解释外部效度 |
| `R8.activity_fact_cost` | Activity-fact | incurs | Cost | cost 数值或量级 | 不报告 = 无 economic 维度 | §3.1 Page 5 | 经济关系边 |
| `R9.cost_resource` | Cost | consumes | Resource | money / time / … | 不报告 resource 时 cost 抽象 | §3.1 Page 5 | 资源映射边 |
| `R10.agent_activity` | Agent | performs | Activity | agent 类型 | activity 不报告 agent 时假设隐式 agent | §3.1 Page 5 | 人/工具归属 |

当前 `review.md` 完全没有关系边表（A1-DT v2 schema 要求显式列出）。这是一个 I 级返修项。

---

### 6. 统计观察、候选 finding 与 final finding 边界

#### 6.1 由字段 / 统计表支持的统计观察（仅限本文样本 n=57，convenience）

1. Entity-explicitness：implicit = 24/57 (42.1%)。
2. Factor：所有 57 篇都报告 factor；explicitness 与 form 子分布作者文本未展开数字。
3. Agent：reported = 14/57 (24.6%)。
4. Activity：reported = 40/57；其中 ad_hoc elicited = 37/40 (92%)。
5. Attribute：reported = 8/57 (14%)。
6. Impact：N/A = 17/57 (29.8%)；reported 40/57 中 evidence = hypothesized 19 / inductive 11 / referenced 10；modality "balanced"。
7. Context factor：tool = 0%；product-related = 14/57 (24.6%)。
8. Cost：reported = 9/57 (15.8%)；从未 empirically determined。
9. Resource：reported = 5/57 (8.8%)；types 提及 money、time。
10. Reliability：percentage agreement 83.3%；Cohen's κ = 54.2%（作者标 moderate，并自陈受 uneven marginal 影响）；S-Score = 76.8%。

#### 6.2 原文 discussion / recommendation / roadmap 候选 finding

1. requirements quality literature 实现 artifact-centric 偏置，activity / context / economic 覆盖严重不足（§4.4 + §6）。
2. 32/40 reported activities 涉及 understanding/interpretation 子活动 → 暗示 interpretation 是关键 sub-activity（§5.1）。
3. roadmap 6 streams 是 gap → action 的直接映射（§5.1–§5.6）。
4. impact 应升级为 framework 而非 taxonomy（§5.3）。

#### 6.3 对 Paper2 可迁移的方法学启发

1. 把 researcher-defined meta-model 当作"第一贡献"，再用 codebook 把 meta-model 转成可统计变量。
2. 用 inter-rater reliability + 双人编码 + replication package 验证 codebook。
3. 把 gap 分布转成 roadmap action 而不是停留在频次。
4. 显式区分 impact 的 4 个子维度（evidence / modality / generality / frame_of_reference）作为字段冗余/正交检验。

#### 6.4 绝不可迁移的领域结论

1. RE 领域中 entity-implicit / impact-N/A 等具体比例。
2. RQT 11 个具体 concept 名（Entity、Factor 等不能直接套用到 SLR/SMS 的 Paper、Field 等对象）。
3. roadmap 6 streams 的具体名称与内容（属 RE 领域 future work，不是 Paper2 的）。
4. quality-factor ontology、AMDiRE、Quamoco、ABRE-QM 等被引工具的具体可用性。

---

### 7. 对旧版 `review.md` 的返修来源

| 等级 | 位置 | 问题 | 返修建议 |
|---|---|---|---|
| **C** | "维度树复原" → "原文 schema 主树（19×3 审计后返修）" | 仅 6 行抽象主干（construct / rqt / evidence-base / coding / roadmap / boundary），没把 §4 codebook 的 11 concept × 各自 codes 列为叶子；与 metadata.json 已记录的 57 篇分母、§4.3 多条数字脱节。 | 把当前第 3 节的**叶子维度表 17 行**直接落入 review.md，作为"原文 schema 主树（B 树：sample coding codebook）"事实源；保留树 A（RQT 概念）与树 C（roadmap streams）为独立子树；保留通用六叶接口为投影 |
| **C** | "维度树复原" 缺关系边表 | A1-DT v2 schema 要求显式列出关系边，本文 RQT 是关系型理论，必须列。 | 落入本审计第 5 节的 10 条关系边 R1–R10 |
| **I** | §1 快速结论卡片 / "维度树复原" → 一句话结论 | 当前写"不进入主统计池"过早一刀切；实际上 57 篇内部统计对 Paper2 是 schema_seed 可参考。 | 改为"内部 n=57 可作 schema_seed / 局部可统计观察；不进入 Paper2 跨论文 SLR/SMS 主统计池" |
| **I** | "原文模式候选叶子映射（A1 种子）" | 5 行候选叶（quality-construct / theory-model / evaluation-method / roadmap-question / boundary）名称泛、与本文实际 codes 不对应，掩盖了 §4 真实 codebook 的存在。 | 用 17 个 `B.*` 叶替换；保留 5 行旧候选叶作为"已迁移历史草稿，不作事实真源"形式归档 |
| **I** | A.2 证据账本 | 只列 4 行宏观证据（root/taxonomy/stat/risk），全部 `not_verified`；漏掉 Page 7 §4.2 codebook 锚点（最关键的一条）与 Page 8 数字锚点（11 条）。 | 至少新增：EV-…-005 `§4.2 codebook 设计`、EV-…-006 `§4.3 17 个分子分母数字`、EV-…-007 `reliability metrics 83.3/54.2/76.8`、EV-…-008 `§5 roadmap 6 streams`、EV-…-009 `Fig. 2 关系图（待 PDF 核验）` |
| **I** | A.3 结论-证据映射 | C04 `taxonomy` 等结论目前仅指向 EV-002 单一证据；与新增 codebook / numerical / reliability 证据无映射。 | 在 C04–C07 上补 EV-005/006/007 引用；新增 C10 = "57 篇 codebook + reliability 构成本文内部可统计基线但 convenience sampling 限制外推" |
| **M** | "六类 pattern 抽取" 表 | 已整体合格；只是 dimension pattern 行写"RQT concepts"作为维度，可补一句"对应 codebook 实际是 §4.2 categorical variables + codes" | 补一句说明，不必重写 |
| **M** | "待复核" 第 3、4 项 | replication package（Zenodo 8167598）与 rqt-tool GitHub 仓库均未访问 | 标注为 A2a 必访资产；优先核 Zenodo 以补 impact.generality / frame_of_reference、entity_fact codes、activity_fact codes、context sub_categories 完整取值空间 |
| **M** | 元信息 | metadata.json 中 `current_fulltext_status` 已注明"图表级细节按单篇待复核说明处理"；A.4 已记 `cmd-...-visual-check = needs_manual_check` | 保持不变 |

SUMMARY 当前表中字段是否需修正：
- "样本单位 / 样本数量 / 原生树类型 / 统计池资格" 应改为 "样本单位 = primary study（借用 Frattini 2022 样本）；n=57；原生树 = 维度森林（A 概念 / B codebook / C roadmap）；主统计池资格 = 本文内部可统计，跨 Paper2 SLR/SMS 不入主池"。

---

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-rqtr-005 | paper_content.txt | §4.2 Study design | Page 7 段 "we maintained two artifacts… extraction guideline based on the RQT concepts" | "Each concept of the RQT was associated with one or more categorical variables… containing a set of codes that represented if and how the concept was reported" | codebook_design | confirmed_text | 树 B 全部 17 个 `B.*` 叶 + 父节点 | 否（文本明确） | 仅本文 codebook；具体 codes 完整集合需 Zenodo 8167598 核验 |
| EV-rqtr-006 | paper_content.txt | §4.3 Study results | Page 8 整段含 24/57、17/57、14/57、40/57、37/40、8/57、19/40、11/40、10/40、24.6%、9/57、5/57 | "24/57 = 42.1% implicit"、"17/57 N/A"、"14/57 agents"、"37/40 ad hoc"、"8/57 attributes"、"hypothesized 19/40, inductive 11/40, referenced 10/40"、"product-related 14/57 = 24.6%"、"cost 9/57"、"resource 5/57" | numerical_distribution | confirmed_text | `B.entity.explicitness` / `B.agent.presence` / `B.activity.*` / `B.attribute.presence` / `B.impact.*` / `B.context_factor.sub_category` / `B.cost.presence` / `B.resource.presence` | 是（Fig. 4 柱状对照） | 仅 57 篇 convenience sample；不可跨域外推 |
| EV-rqtr-007 | paper_content.txt | §4.2 Reliability | Page 7–8 "task overlap achieved… 83.3%… Cohen's Kappa 54.2%… S-Score 76.8%" | 同左 | reliability_metric | confirmed_text | 整个 codebook 与 §4.3 结果的可信度边界 | 否 | Cohen's κ 在 uneven marginal 下不可靠，故作者引入 S-Score |
| EV-rqtr-008 | paper_content.txt | §5 Roadmap | Page 9–11 §5.1–§5.6 标题与正文 | "1. Artifact and usage model … 2. Taxonomy of quality factors … 3. impact framework … 4. Context factors … 5. Economic impact … 6. Tool support" | roadmap_action | confirmed_text | 树 C 6 streams | 否 | candidate finding，不可作 final finding |
| EV-rqtr-009 | paper.pdf | §3 Fig. 2 + Table 1 | Page 4–5 概念关系图与 Table 1 origin 列 | RQT 11 concepts 与 origin 引用 | concept_model | needs_visual_check | 树 A 11 concepts + R1–R10 关系边 | 是 | 仅本文 RQT；不可套用至 SLR/SMS |
| EV-rqtr-010 | paper_content.txt | §4.5 Threats | Page 9–10 internal / construct / external validity 段落 | "non-empirical work could contribute theoretical evidence"、"convenience sampling"、"limited to empirical contributions" | validity_boundary | confirmed_text | 整个森林的外推限制 | 否 | 不可在本文样本外推普适规律 |
| EV-rqtr-011 | metadata.json + paper_content.txt | §4.1 + replication package footnote | Page 7 + footnote 1 | Zenodo DOI 10.5281/zenodo.8167598 | replication_asset | not_verified | `B.impact.generality` / `B.impact.frame_of_reference` / Entity-fact / Activity-fact / context sub-categories 完整取值空间 | 是（Zenodo 访问） | 未核验前 A2a 不得宣称 codes 集合饱和 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C10 | 本文样本编码维度树（树 B）由 11 个 RQT 概念关联的 categorical variables + codes 组成，并已通过 inter-rater reliability 验证；构成 Paper2 可借鉴的 codebook 设计先例 | codebook_seed | 树 B（17 叶） | EV-rqtr-005, EV-rqtr-006, EV-rqtr-007 | medium（文本级 confirmed，PDF/Zenodo 仍需核） | Paper2 §Method codebook design 设计参考；不作 final finding | 取值空间在 Zenodo 核验前不饱和 |
| C11 | 本文报告的 17 个分子/分母均在 n=57 convenience sample 内有效；跨 RE 领域、跨综述类型不可外推 | local_statistic | `B.*.presence` 与频次叶 | EV-rqtr-006, EV-rqtr-010 | medium | Paper2 中作为 "RE 领域 evidence 不足" 的脚手架引用 | 不可作 Paper2 跨论文统计 |
| C12 | RQT 11 concepts + 10 关系边（R1–R10）共同构成一个关系型理论树；本文 codebook 实际只编码节点存在与几类属性，未编码关系边的具体取值 | model_vs_codebook_gap | 树 A 与树 B 的对应 | EV-rqtr-005, EV-rqtr-009 | medium | 提示 Paper2：meta-model 关系边也需 codebook 化才能统计 | codebook 未覆盖关系层 |
| C13 | 树 C 6 streams 仅为 candidate finding；roadmap 行动尚未被本文实证 | candidate_finding | 树 C | EV-rqtr-008, EV-rqtr-010 | weak | 仅作 future work 启发 | 不可作已验证方案引用 |
| C14 | replication package（Zenodo 8167598）与 rqt-tool（GitHub Julian Frattini/rqt-tool）是 A2a 必访资产；未访问前 `B.impact.generality / frame_of_reference / entity_fact / activity_fact / context.sub_category` 取值空间为 schema_seed | a2a_blocker | 上述 5 叶 | EV-rqtr-011 | weak | A2a 入口 | 资产可能已更新或下线 |

---

### 9. 技能使用与自我审查记录

#### 9.1 已读技能 / 指南文件与采用原则

| 文件 | 是否读取 | 本审计采用要点 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | 是 | claim-evidence-engineering 原则：每条统计或叶子必绑定原文证据；证据不足显式标 `not_verified` |
| `ai-research-writing-skill/references/reviewer-guidelines.md` | 是 | 五维 reviewer 视角（Originality / Soundness / Clarity / Significance / Reproducibility）用于第 7 节 C/I/M 分级 |
| `ai-research-writing-skill/references/reviewer-self-review.md` | 是 | 采用 Five-Dimension Review 与"author-facing analysis"思路，把返修建议落到具体节点 |
| `research-planning/SKILL.md` | 是 | 用 4-stage planning 框架理解本文"Theory / Evaluation / Roadmap"三段式 |
| `research-planning/references/planning-prompts.md` | 是（节选） | 借用 Paper2Code Turn 2 "Architecture Design" 视角识别树 A / B / C 的森林结构 |
| `research-planning/references/output-schemas.md` | 是（首 100 行） | 用 task_list / methodology 结构辅助判定原文 RQ 与 sample unit 关系 |
| `oh-my-codex/0.18.7/skills/autoresearch/SKILL.md` | 是 | 采用 "Completion is artifact-gated" 思路：本审计完成等于一份自包含报告而非"工作中" |

未出现 `blocked` 风险；全部技能文件成功读取。

#### 9.2 Reviewer 视角下本输出的 3 大风险

1. **Zenodo replication package 与 rqt-tool 仓库未核验**：树 B 中 `impact.generality`、`impact.frame_of_reference`、`entity_fact.codes`、`activity_fact.codes`、`context_factor.sub_category` 完整取值空间均依赖 Zenodo 8167598 才能饱和。主线程合并时应在 A.4 增加 `cmd-…-zenodo-fetch` 与 `cmd-…-rqt-tool-fetch` 两条人工核验。
2. **未做 PDF 视觉核对**：Fig. 4（codes 分布柱状）与 Page 8 文本数字是否一致、Fig. 2 关系箭头方向、Table 1 origin 列均只来自 `paper_content.txt` 提取结果。主线程合并时应至少打开 PDF 核对一次（A.4 已有 `cmd-…-visual-check = needs_manual_check`，但范围应扩展到 Fig. 4 数字交叉）。
3. **convenience sampling 边界**：本文 57 篇借用前作样本，作者承认是 convenience；本审计的"局部可统计 / 不入主池"判定如果被下游误读为"本文是 SLR/SMS"，会造成 Paper2 跨论文统计误入。主线程合并 SUMMARY 时应再次显式写"样本来源 = Frattini et al. 2022 quality-factor ontology 的 57 篇 convenience sample，不是新做检索"。

#### 9.3 本任务状态

无 blocked、无 timeout、无文件缺失。所有要求的技能文件、论文材料均已读取并在报告中显式引用。本报告为自包含完整审计，未引用"上一条消息"或外部隐藏内容。

---

**报告完结。**

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-requirements-quality-theory-roadmap-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-requirements-quality-theory-roadmap-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-requirements-quality-theory-roadmap-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-requirements-quality-theory-roadmap-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-requirements-quality-theory-roadmap-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-requirements-quality-theory-roadmap-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-requirements-quality-theory-roadmap-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-requirements-quality-theory-roadmap-type | clm-requirements-quality-theory-roadmap-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） | paper_type | text_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-requirements-quality-theory-roadmap-unit | clm-requirements-quality-theory-roadmap-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） | sample_unit | text_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-requirements-quality-theory-roadmap-denom | clm-requirements-quality-theory-roadmap-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-reported 子集为 40） | denominator | text_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-requirements-quality-theory-roadmap-tree | clm-requirements-quality-theory-roadmap-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 | schema | text_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-requirements-quality-theory-roadmap-pool | clm-requirements-quality-theory-roadmap-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 final finding |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-requirements-quality-theory-roadmap-type | A1DT-requirements-quality-theory-roadmap-C01 | 本文原文类型为：research commentary / theory + evaluation + roadmap（非标准 SLR/SMS，作者自述为 viewpoint + survey） | paper_type | type | ev-requirements-quality-theory-roadmap-type | 正式写作前需核对出版页和 PDF 版式 | text_verified | schema_seed / 背景方法样本描述 | 否 | -- |
| clm-requirements-quality-theory-roadmap-unit | A1DT-requirements-quality-theory-roadmap-C02 | 本文被编码样本单位为：primary study（来自 Frattini et al. 2022 quality-factor ontology 的 requirements quality 一手研究文献） | sample_unit | sample_unit | ev-requirements-quality-theory-roadmap-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | text_verified | schema_seed / A2a 抽取表设计 | 否 | -- |
| clm-requirements-quality-theory-roadmap-tree | A1DT-requirements-quality-theory-roadmap-C03 | 本文原生维度树 / 维度森林为：**维度森林（forest）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 extraction codebook（把 11 concepts 转为 categorical variables + codes）；树 C = §5 roadmap streams（6 streams）。**真正的样本编码树是 B**。 | tree_type | native_tree | ev-requirements-quality-theory-roadmap-tree | 不代表跨论文通用模板 | text_verified | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-requirements-quality-theory-roadmap-pool | A1DT-requirements-quality-theory-roadmap-C04 | 本文统计池资格为：**局部可统计 / 不进入 SLR/SMS 主统计池**：内部 57 篇编码有可统计分母与 codes；但样本来自先前研究的 convenience sample，作者自陈非饱和，且整体是 viewpoint/commentary，对 Paper2 而言仅作 `schema_seed / boundary_anchor` | eligibility | statistical_pool | ev-requirements-quality-theory-roadmap-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-requirements-quality-theory-roadmap-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-requirements-quality-theory-roadmap-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-requirements-quality-theory-roadmap-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
