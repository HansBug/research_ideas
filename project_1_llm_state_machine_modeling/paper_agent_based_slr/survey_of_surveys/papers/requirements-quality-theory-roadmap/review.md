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

### 一句话结论

本文的维度树主类型为“理论 / 元模型概念树”，辅助类型为“requirements quality roadmap 树”。不进入主统计池：theory/evaluation/roadmap；非标准 SLR/SMS，样本/编码可启发字段但不进入 SLR/SMS 统计池；仅作 boundary_anchor。 [clm-requirements-quality-theory-roadmap-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-requirements-quality-theory-roadmap-source-schema-candidates]

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-requirements-quality-theory-roadmap-root] | Requirements quality research 的研究目标 / RQ / 贡献声明 | roadmap action / guideline item / schema seed | [dim-requirements-quality-theory-roadmap-b1] 综述范围与研究问题；[dim-requirements-quality-theory-roadmap-b2] 语料收集与纳排；[dim-requirements-quality-theory-roadmap-b3] 主题 / 对象分类；[dim-requirements-quality-theory-roadmap-b4] 方法 / 技术 / 干预；[dim-requirements-quality-theory-roadmap-b5] 评价、统计与候选发现 | [ev-requirements-quality-theory-roadmap-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
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
    └── [leaf-requirements-quality-theory-roadmap-evidence] 评价、证据与复现资产
    └── [leaf-requirements-quality-theory-roadmap-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-requirements-quality-theory-roadmap-scope] | 研究范围与单位对象 | [dim-requirements-quality-theory-roadmap-b1] | 定义 requirements quality 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-scope] |
| [leaf-requirements-quality-theory-roadmap-corpus] | 语料与纳排链条 | [dim-requirements-quality-theory-roadmap-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-corpus] |
| [leaf-requirements-quality-theory-roadmap-taxonomy] | 主题与维度分类 | [dim-requirements-quality-theory-roadmap-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-taxonomy] |
| [leaf-requirements-quality-theory-roadmap-method] | 方法 / 技术 / 干预分类 | [dim-requirements-quality-theory-roadmap-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-method] |
| [leaf-requirements-quality-theory-roadmap-evidence] | 评价、证据与复现资产 | [dim-requirements-quality-theory-roadmap-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-evidence] |
| [leaf-requirements-quality-theory-roadmap-finding] | 统计观察与候选发现 | [dim-requirements-quality-theory-roadmap-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-requirements-quality-theory-roadmap-leaf-finding] |

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-requirements-quality-theory-roadmap-orig-quality-construct] | [dim-requirements-quality-theory-roadmap-b1] | 需求质量构念 | 质量属性、缺陷类型、语义维度、可测量质量构念。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-requirements-quality-theory-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-requirements-quality-theory-roadmap-orig-theory-model] | [dim-requirements-quality-theory-roadmap-b2] | 理论 / 元模型元素 | 概念关系、质量定义、测量对象和理论边界。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-requirements-quality-theory-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-requirements-quality-theory-roadmap-orig-evaluation-method] | [dim-requirements-quality-theory-roadmap-b3] | 评价方法 | 人工评价、自动检测、NLP / ML、实验或案例证据。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-requirements-quality-theory-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-requirements-quality-theory-roadmap-orig-roadmap-question] | [dim-requirements-quality-theory-roadmap-b4] | 路线图问题 | 开放问题、未来方向、方法缺口和实践挑战。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-requirements-quality-theory-roadmap-orig-boundary] | [dim-requirements-quality-theory-roadmap-b5] | 外推边界 | 非标准 SLR、理论整合、样本限制和统计池排除理由。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/requirements-quality-theory-roadmap__codex.md)、[claude](../../audits/a1dt-19x3/results/requirements-quality-theory-roadmap__claude.md)、[deepseek](../../audits/a1dt-19x3/results/requirements-quality-theory-roadmap__deepseek.md)。 [clm-requirements-quality-theory-roadmap-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-requirements-quality-theory-roadmap-orig-construct] | 需求质量 construct | quality attribute、defect、semantic dimension、measurement object | theory construct seed | 理论对象与统计字段分开 | 核对概念定义 |
| [dim-requirements-quality-theory-roadmap-orig-rqt] | RQT 概念模型 | 11 concepts、relations、theory boundary、causal/semantic links | 关系型理论树 seed | 概念关系需保留边表 | 核对 RQT 模型图/表 |
| [dim-requirements-quality-theory-roadmap-orig-evidence-base] | 57 篇状态评价 | manual assessment、automatic detection、NLP/ML、case evidence、coverage status | 评价语料 seed | 该文非标准 SLR 时降级 | 核对 evaluation 章节 |
| [dim-requirements-quality-theory-roadmap-orig-coding] | 抽取 guideline / coding scheme | concept coding、evidence type、theory synthesis、harmonization rule | dimension pattern seed | coding 主观性记录 | 核对 coding 描述 |
| [dim-requirements-quality-theory-roadmap-orig-roadmap] | roadmap questions | open issue、future direction、method gap、research agenda | candidate finding heuristic | roadmap 不进入统计池 | 核对 roadmap 小节 |
| [dim-requirements-quality-theory-roadmap-orig-boundary] | 理论整合边界 | non-standard SLR、theory integration、author synthesis、statistical exclusion | 边界锚点 | 不得与完成型 SLR 混算 | 核对 limitations/conclusion |

#### 三路审计综合返修结论

| 审计共同问题 | 本轮返修动作 | 剩余风险 |
|---|---|---|
| 原先主树过度依赖六个通用接口叶子，容易把跨论文投影误读成原文 schema。 | 将原文 RQ、抽取字段、分类项、质量 rubric、关系边、统计表或 roadmap action 抬升为上表主干，并把通用接口降级为后文投影。 | 上表仍是 `schema_seed`，需 A2a 精确核对页码、表号、图号和附录。 |
| 原文显式取值空间未完全进入叶子层。 | 在“叶子 / 取值空间种子”中列出封闭枚举、层级枚举、数值分母、关系值或自由文本边界。 | 取值空间是否封闭、是否饱和、是否可统计，需要 A2a 逐项判定。 |
| 统计观察、候选发现和最终 finding 容易混层。 | 统计用途列显式保留 `schema_seed`、候选 finding 和不得进入当前 SUMMARY 定量统计的边界。 | final research finding 仍必须等跨论文证据、反证和研究者裁决。 |

#### 审计返修口径

- 本节吸收 `codex`、`claude`、`deepseek` 三路全文审计的共同结论：原文 schema 主树必须优先于跨论文通用接口层；通用接口只做投影，不再冒充原文叶子全集。
- 本节只完成 A1-DT 结构化返修；凡未补齐精确页码、表号、图号或 supplementary 定位的节点均保持 `schema_seed` / `not_verified`，并作为 A2a 精核入口。
- 若三路审计之间存在细节差异，后续 A2a 以原文 PDF、`paper_content.txt`、附录和复现实验包为准，并在 A.3 中新增替代结论或废弃旧结论。
#### 通用接口投影

下表只用于把原文 schema 主树投影到跨论文统一接口，不能替代上表成为原文事实源。

| 通用接口 | 在本文中的投影对象 | 使用边界 |
|---|---|---|
| 研究范围与单位对象 | `requirements quality constructs` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
| 语料与纳排链条 | 与检索、纳排、样本分母、方法流程相关的原文主干。 | 无系统检索的 roadmap / vision 需写不适用。 |
| 主题与维度分类 | 原文 taxonomy、classification schema、concept model 或 roadmap action 分类。 | 必须保留原文取值空间，不得压成泛词。 |
| 方法 / 技术 / 干预分类 | 原文 method / tool / intervention / agent role / guideline stage。 | 方法学 guideline 不得误写成目标领域方法效果。 |
| 评价、证据与复现资产 | 原文 quality、metric、artifact、replication、validity、evidence table。 | 弱证据或未核验链接不得进入统计。 |
| 统计观察与候选发现 | 原文 result / discussion / gap / recommendation / action point。 | 只能作 candidate finding，需研究者裁决。 |

#### 返修后仍需 A2a 精核

1. 将上表每个原文主干拆成更细叶子，并为每个叶子补具体页码、表号 / 图号、段落或附录定位。
2. 核对取值空间是否是原文封闭枚举、层级枚举、数值 / 分母、关系值，还是只能自由文本。
3. 若三路审计意见冲突，以原文证据为准，并在 A.3 新增替代结论或废弃旧结论。

### 统计与候选发现链路

| 对象标识 | 可统计方式 | 分母 | 是否进入主统计池 | 候选发现用途 | 降级说明 |
|---|---|---|---|---|---|
| [dim-requirements-quality-theory-roadmap-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否 | 识别可迁移的维度模式类型 | 不进入主统计池：theory/evaluation/roadmap；非标准 SLR/SMS，样本/编码可启发字段但不进入 SLR/SMS 统计池；仅作 boundary_anchor。 |
| [leaf-requirements-quality-theory-roadmap-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | not_applicable | 否 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-requirements-quality-theory-roadmap-finding] | 候选发现台账，不直接作为 final finding | discussion / conclusion / roadmap action | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-requirements-quality-theory-roadmap-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | requirements quality 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-requirements-quality-theory-roadmap-transfer] |
| [leaf-requirements-quality-theory-roadmap-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-requirements-quality-theory-roadmap-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-requirements-quality-theory-roadmap-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-requirements-quality-theory-roadmap-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-requirements-quality-theory-roadmap-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-requirements-quality-theory-roadmap-001 | [ev-requirements-quality-theory-roadmap-root] | [src-requirements-quality-theory-roadmap-text], [src-requirements-quality-theory-roadmap-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-requirements-quality-theory-roadmap-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-requirements-quality-theory-roadmap-002 | [ev-requirements-quality-theory-roadmap-taxonomy] | [src-requirements-quality-theory-roadmap-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-requirements-quality-theory-roadmap-b1], [dim-requirements-quality-theory-roadmap-b2], [dim-requirements-quality-theory-roadmap-b3], [dim-requirements-quality-theory-roadmap-b4], [dim-requirements-quality-theory-roadmap-b5], [leaf-requirements-quality-theory-roadmap-taxonomy], [leaf-requirements-quality-theory-roadmap-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-requirements-quality-theory-roadmap-003 | [ev-requirements-quality-theory-roadmap-stat] | [src-requirements-quality-theory-roadmap-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作 boundary / candidate seed，待 A2a 精确页码 / 表图核验后才能升级。 | author_claim | not_verified | [leaf-requirements-quality-theory-roadmap-evidence], [leaf-requirements-quality-theory-roadmap-finding], [leaf-requirements-quality-theory-roadmap-orig-quality-construct], [leaf-requirements-quality-theory-roadmap-orig-theory-model], [leaf-requirements-quality-theory-roadmap-orig-evaluation-method], [leaf-requirements-quality-theory-roadmap-orig-roadmap-question], [leaf-requirements-quality-theory-roadmap-orig-boundary] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
| EV-requirements-quality-theory-roadmap-004 | [ev-requirements-quality-theory-roadmap-risk] | [src-requirements-quality-theory-roadmap-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-requirements-quality-theory-roadmap-root], [leaf-requirements-quality-theory-roadmap-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-requirements-quality-theory-roadmap-tree-type] | A1DT-requirements-quality-theory-roadmap-C01 | 本文的维度树主类型为“理论 / 元模型概念树”，辅助类型为“requirements quality roadmap 树”。不进入主统计池：theory/evaluation/roadmap；非标准 SLR/SMS，样本/编码可启发字段但不进入 SLR/SMS 统计池；仅作 boundary_anchor。 [clm-requirements-quality-theory-roadmap-tree-type] | tree_type | [dim-requirements-quality-theory-roadmap-root] | EV-requirements-quality-theory-roadmap-001, EV-requirements-quality-theory-roadmap-004 | 树型判断仅限本文，不代表所有 requirements quality 综述。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-scope] | A1DT-requirements-quality-theory-roadmap-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-scope] | EV-requirements-quality-theory-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-corpus] | A1DT-requirements-quality-theory-roadmap-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-corpus] | EV-requirements-quality-theory-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-taxonomy] | A1DT-requirements-quality-theory-roadmap-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-taxonomy] | EV-requirements-quality-theory-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-method] | A1DT-requirements-quality-theory-roadmap-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-method] | EV-requirements-quality-theory-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-evidence] | A1DT-requirements-quality-theory-roadmap-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-evidence] | EV-requirements-quality-theory-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-leaf-finding] | A1DT-requirements-quality-theory-roadmap-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-requirements-quality-theory-roadmap-finding] | EV-requirements-quality-theory-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-requirements-quality-theory-roadmap-transfer] | A1DT-requirements-quality-theory-roadmap-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-requirements-quality-theory-roadmap-root] | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-requirements-quality-theory-roadmap-finding-boundary] | A1DT-requirements-quality-theory-roadmap-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-requirements-quality-theory-roadmap-finding] | EV-requirements-quality-theory-roadmap-003, EV-requirements-quality-theory-roadmap-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |

| [clm-requirements-quality-theory-roadmap-source-schema-candidates] | A1DT-requirements-quality-theory-roadmap-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-requirements-quality-theory-roadmap-orig-quality-construct], [leaf-requirements-quality-theory-roadmap-orig-theory-model], [leaf-requirements-quality-theory-roadmap-orig-evaluation-method], [leaf-requirements-quality-theory-roadmap-orig-roadmap-question], [leaf-requirements-quality-theory-roadmap-orig-boundary] | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-requirements-quality-theory-roadmap-a1dt-19x3-repair] | A1DT-requirements-quality-theory-roadmap-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-requirements-quality-theory-roadmap-root] | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-requirements-quality-theory-roadmap-structure-check] | [dim-requirements-quality-theory-roadmap-root], A1DT-requirements-quality-theory-roadmap-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-requirements-quality-theory-roadmap-visual-check] | EV-requirements-quality-theory-roadmap-002, EV-requirements-quality-theory-roadmap-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
