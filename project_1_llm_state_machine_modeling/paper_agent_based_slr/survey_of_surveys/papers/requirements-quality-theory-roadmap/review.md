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

**一句话结论**：这篇文献最值得迁移的不是 requirements quality 的具体结论，而是“先定义理论对象与关系 → 用对象级 codebook 评价现有研究 → 把缺口组织成 roadmap 与 tool-support 架构”的三段式。它可以启发 Paper2 如何把 researcher-defined meta-model 做成一等制品，而不是把抽取字段表当作临时表格。

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

作者用 RQT 反向评价 requirements quality literature：研究问题是“requirements quality literature 如何报告 RQT 中的概念”。样本来自作者此前关于 requirements quality factors 的系统研究，共 57 篇 原始研究；这是 convenience sampling，但作者认为足以做理论状态初步评价。

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
5. **经济影响（Economic impact）**
   - 质量因子需要连接到 resource 和 cost，才能支持工业决策。
   - economic impact 是复杂但高优先级方向。
6. **工具支持（tool support）**
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
4. **External validity**：样本约束在 empirical contributions；非经验性理论工作可能提供 演绎证据，例如基于语言学理论解释名词化（名义类别ization）的影响，因此关于 impact evidence 类型的结论不能无限外推。

对本地使用而言，最大风险是：这是一篇 research commentary + theory/evaluation/roadmap，而不是标准 tertiary study；它能提供 meta-model 启发，但不能作为 LLM/agent-based SLR 的直接有效性证据。

## 3. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 本文不是普通 SLR 的多 RQ 结构，而是围绕“理论统一 + 现状评价 + roadmap”组织；唯一显式评价 RQ 是 requirements quality literature 如何报告 RQT concepts。 | `paper_content.txt` Page 2 贡献列表；Page 7 研究问题；Page 8--9 结果解释。 | 可作为 Paper2 theory-driven evaluation RQ 候选：先定义 meta-model，再问现有文献/运行制品如何覆盖这些概念。 | roadmap/commentary 不适合改写为 PICO 或效果评价型 RQ；不得把其 57 篇样本当作目标 SLR/SMS 证据池。 |
| dimension pattern | 维度核心是 RQT concepts：Entity、Factor、Entity-fact、Agent、Activity、Attribute、Activity-fact、Impact、Context factor、Cost、Resource；编码还包括 explicitness、factor form、impact evidence、impact modality 等。 | `paper_content.txt` Page 4--6 RQT 与 Table 1；Page 7--8 instrument design；Page 8 Fig. 4 结果说明。 | 高度可迁移到 Paper2 的 researcher-defined meta-model：字段不是平铺标签，而是对象、关系、属性、上下文和经济后果的结构。 | 具体概念属于 requirements quality；Paper2 需重命名为 SLR/SMS 对象，如 Paper、Evidence field、Analysis activity、Finding claim、Review context、Human/LLM agent。 |
| finding pattern | findings 不是单纯频次，而是“理论覆盖缺口 → 实践相关性风险 → roadmap 需求”：artifact-centric 概念覆盖好，activity/context/economic 概念覆盖差。 | `paper_content.txt` Page 8--9 Study results / Interpretation；Page 11--12 Conclusion。 | 可迁移为 gap-to-action finding pattern：统计覆盖率要进一步解释为方法风险和行动方向。 | 本文 finding 是 requirements quality 领域事实，不可转写为 Paper2 领域结论；只能迁移推理结构。 |
| evidence presentation pattern | 证据呈现包括 57 篇样本来源、extraction guideline、categorical codes、双人 reliability、descriptive statistics、Fig. 4 concept coverage、replication package。 | `paper_content.txt` Page 7--8 Study design；Page 8 Study results；Page 7 replication package footnote。 | 可迁移为 Paper2 的审计证据链：字段合同、抽取指南、编码可靠性、分布图和复现实验包应共同支撑结论。 | 本轮未人工核对 Fig. 4 图形数值；正式引用数字前需回 PDF 和 replication package。 |
| validity / threat pattern | 明确区分 internal、construct、external validity；重点是 convenience sampling、隐式概念抽取、样本仅 empirical contributions。 | `paper_content.txt` Page 9--10 Threats to validity。 | 可迁移到 Paper2：若研究者定义 meta-model 后评价文献或 agent output，必须说明样本来源、构念对齐、隐式字段抽取和外推边界。 | 本文 threat 主要面向 survey of literature，不覆盖 LLM 服务提供商漂移（provider drift）、prompt variance、run record 缺失等 Paper2 专属风险。 |
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

## 6. 对 Paper2 的启发与风险

### 6.1 强启发

1. **researcher-defined meta-model 应成为第一贡献对象**
   - RQT 说明，高质量研究不是先堆字段，而是先定义理论对象、对象之间的关系、影响路径和成本后果。
   - Paper2 可把“研究者定义综述元模型”写成类似 RQT 的对象图：paper / requirement-like evidence entity、field/factor、agent、activity、attribute、候选发现、context、cost。

2. **字段必须绑定下游 activity impact**
   - requirements quality 研究的问题是 factor impact unknown。
   - Paper2 不能只说某字段“应该抽取”；要说明它服务于哪类后续活动：筛选复核、统计分析、候选发现生成、反向证据检查、审稿人复核、run record 审计等。

3. **从理论到评价再到 roadmap 的三段式可作为候选复用**
   - 本文结构提供一个稳健写法：先提出理论/元模型，再评价当前研究/制品覆盖，最后将缺口转成 roadmap / tool architecture。
   - Paper2 可采用同构结构：meta-model → agent workflow / corpus dry-run coverage → schema evolution / evidence chain roadmap。

4. **activity attribute 是评价设计关键**
   - RQT 提醒：如果不定义 activity 的 measurable attribute，就无法评价 impact。
   - Paper2 的评价维度应显式包括 traceability、field correctness、source-anchor accuracy、reviewer agreement、revision effort、候选发现 precision、human adjudication cost 等。

5. **context 与 economic impact 是审稿人会追问的边界**
   - Paper2 若只报告准确率或文本质量，会忽略 provider/model drift、领域差异、全文可得性、人工复核成本等 context/resource。
   - 可把 context/cost 做成 run record 与 evaluation table 的必填字段。

6. **tool support 不能只是文本生成器**
   - 本文的 tool architecture 以 entity/context characterization 和 impact prediction 为核心。
   - Paper2 的工具形态应更像 evidence engineering environment：管理 corpus、schema、field evidence、statistics、候选发现、human challenges、process evidence 和 redaction。

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
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__codex.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__codex.md)、[../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__claude.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__claude.md)、[../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__deepseek.md](../../audits/a1dt-v2-19x3/results/requirements-quality-theory-roadmap__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/requirements-quality-theory-roadmap.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `requirements-quality-theory-roadmap` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；通读 14 页全文（Page 1–Page 14 含 References） |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；两份均已读，且交叉核对元信息 |
| 是否打开或核对 `paper.pdf` | 否；本轮仅基于 text 审计，未做 PDF 版面核验（图 Fig. 2/4/5、Table 1 字段对齐留待 A2a） |
| 原文类型 | research commentary / theory + 评价 + 路线图（非标准 SLR/SMS，作者自述为 viewpoint + survey） |
| 被编码样本单位 | 原始研究（来自 Frattini et al. 2022 质量因素本体（质量-factor ontology） 的 requirements 质量 一手研究文献） |
| 样本数量 / 分母 | n = 57 publications（§4.1）；分子分母 17/57、24/57、14/57、8/57、9/57、5/57 以及 19/40、11/40、10/40、37/40、32/40（impact-已报告 子集为 40） |
| 原生树类型 | **维度森林（森林）**：树 A = RQT 概念元模型（11 concepts, Fig.2/Table 1）；树 B = §4 抽取 编码本（把 11 concepts 转为 categorical variables + 代码）；树 C = §5 路线图 streams（6 streams）。**真正的样本编码树是 B**。 |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

---

### 1. 原文证据阅读说明

实际读取的本地文件与覆盖范围：

1. `bibtex.bib` 完整 — 锁定 Frattini et al. 2023, *Requirements Engineering* 28(4):507–520, DOI 10.1007/s00766-023-00405-y。
2. `metadata.json` 完整 — 已知 `eligible_for_statistical_synthesis: false`、`evidence_role: theory_roadmap_schema_seed`（理论路线图模式种子）、`systematic_evidence_status: non_systematic_or_boundary_anchor`，与本审计判定一致。
3. `paper_content.txt` 通读 Page 1–14 全文，含摘要、§1–§6、References。
4. `paper.pdf` 未在本轮打开（Fig. 2 RQT 概念图、Fig. 3 example 实例化、Fig. 4 代码 分布柱状、Fig. 5 工具 architecture、Table 1 concept origins 留待 A2a 版面核验）。
5. `review.md` 完整阅读（含 §1–§7 与“维度树复原”；证据链已迁至 evidence_chain.md）。

关键证据锚点（5–12 条）：

1. **Page 2，§1 contributions**："(1) A harmonized requirements 质量 theory… (2) A survey of requirements 质量 research… (3) A consequent research 路线图"。三段式贡献声明，决定森林型结构。
2. **Page 4，§3.1 + Fig. 2 + Table 1**：RQT 概念 = `Entity / Factor / 实体事实 / Agent / Activity / Attribute / 活动事实 / Impact / Context factor / Cost / Resource`，共 11 concepts，每个有 origin 引用。这是**树 A**。
3. **Page 7，§4.1**："a sample of 57 原始研究… non-probabilistic, more specifically convenience sampling"。锁定样本单位、分母与抽样性质。
4. **Page 7，§4.2 instrument design**："Each concept of the RQT was associated with one or more categorical variables, each containing a set of 代码 that represented if and how the concept was 已报告. The 代码 were created ad hoc in the first iteration of 抽取 and refined based on discussions and theoretical background in the second iteration."。**这是树 B 的存在证据**。
5. **Page 7，§4.2 entity 代码 示例**："代码 that represent how the concept entity is 已报告 are, for example, explicit and implicit"。
6. **Page 7，§4.2 factor 代码 示例**："the 代码 of the concept Factor were split into two groups, representing both the explicitness… and the form"。
7. **Page 7–8，§4.2 reliability**：percentage agreement 83.3%、Cohen's Kappa 54.2%、S-Score 76.8%；两人编码、6 篇约 10% 验证子样（其中 2 篇训练、4 篇正式计算）。
8. **Page 8，§4.3 results**：分子分母枚举 — Entity implicit 24/57（42.1%）；Impact N/A 17/57（29.8%）；Agent 14/57（24.6%）；Activity ad hoc 37/40（92%）；Attribute 8/57（14%）；Impact 证据 假设性19/40、归纳式11/40、引用式10/40；Context factor 范围 0%–24.6%；Cost 9/57（15.8%）；Resource 5/57（8.8%）。
9. **Page 8，§4.3 impact dimensions**："We grouped the 代码 classifying how impact is 已报告 into four distinct dimensions, two of which are 已报告 here…"。Impact 有 **4 个子维度**：证据、modality、generality、frame of reference；其中后两个原文未报告但作者声明编码存在。
10. **Page 9–10，§5 路线图**：6 streams = 制品/usage 模型、质量因素分类法（taxonomy of quality factors）、影响框架（impact framework）（升级自 影响分类法（分类法 of impacts））、context factors、economic impact、工具 support。
11. **Page 11，§5.6 + Fig. 5**：工具 architecture 含 entity characterization + 影响预测（impact prediction） 模型；并提到 GitHub `JulianFrattini/rqt-tool`（本轮未核验）。
12. **Page 8，§4.5 威胁**：external 效度 = 样本仅 经验研究（empirical） contributions；construct = 隐式 concept 抽取困难。

未做 PDF 版面核验的部分：Fig. 4 柱状图实际数值与文本数字是否一致；Table 1 origin 引用列；Fig. 2 关系箭头方向；复现包（Zenodo 8167598）字段定义。

---

### 2. 样本单位与字段来源判定

**Q1 — 原文逐项编码的对象是什么？**
是 requirements 质量 文献中的 原始研究（一篇一项）。Page 7 明确："a sample of 57 原始研究"，每篇被 需求质量理论编码本（需求质量理论编码本；首次术语） 编码一次。

**Q2 — 作者是否做了系统检索 / 纳排 / 抽取 / 编码方案？**
- 系统检索：**否，未新做**。样本直接借用作者团队前作 Frattini et al. 2022 质量因素本体（质量-factor ontology） 研究（arXiv 2206.05959）的 57 篇 sample，作者明确标注为 convenience sampling。
- 抽取方案：**有**。基于 RQT concepts 构建 抽取 指南，每个 concept 关联 ≥1 个 categorical variable，每个 variable 含若干 代码（代码 在第一轮 ad hoc 生成，第二轮基于讨论与理论背景精炼）。
- 编码方案：第一作者全样本编码，第二作者在 6 篇随机子样（2 篇训练 + 4 篇正式）独立编码，计算 percentage agreement / Cohen's Kappa / S-Score。

**Q3 — 字段来源**：来自 §4.2 抽取 指南 与 §4.3 results 中显式提到的 代码、复现包（Zenodo），与 §3 RQT 11 concepts 的对应映射。

**Q4 — RQ 与样本单位的关系**：唯一显式 RQ = "How are the concepts of the requirements 质量 theory 已报告 in requirements 质量 literature?"（Page 7）。RQ 把 RQT 概念当作**编码字段集合**，把 57 篇当作**被编码样本**，结果是**字段在样本中的报告频次与方式分布**。RQ 本身不构成树根，而是把树 A（RQT 概念）作为字段、应用到样本上、产出统计观察。

**Q5 — 是否要降级？**
**部分降级**：
- 该文不是新做的 SLR/SMS，而是 viewpoint + 内部 survey + 路线图。
- 但它有真实样本（n=57）、有 编码本、有 reliability、有 descriptive statistics。
- 对本文自身而言：可作内部统计；对 Paper2 而言：仅作 `模式种子（schema_seed） / methodological_seed / 边界锚点（boundary_anchor）`，不进入跨论文 SLR/SMS 主统计池。这与 metadata.json `eligible_for_statistical_synthesis: false` 一致。

---

### 3. 原生样本编码维度树 / 维度森林

本文是**维度森林**（A + B + C 三树），其中 **树 B = 样本编码维度树**，是 A1-DT v2 关注的真正主树。

#### 树 A：RQT 概念元模型（§3, Fig. 2, Table 1）

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
需求质量理论概念元模型（RQT；理论层）
├── 制品相关层
│   ├── 实体            — 需求制品或其组成（规格说明、小节、段落、句子、需求）
│   ├── 因素            — 对实体的规范性度量；可分解为 sub-factor
│   └── 实体事实       — 实体 × 因素 的具体取值（如用户故事的符合性 = 缺少角色）
├── 活动相关层
│   ├── 主体             — 人、群体或自动化机制
│   ├── 活动          — 以实体为输入并产生输出的受需求影响活动（requirements-affected activity；首次术语）
│   ├── 属性         — 活动的可测属性（确定性、持续时间、可读性等）
│   └── 活动事实     — 活动 × 属性 的具体取值
├── 影响 / 上下文层
│   ├── 影响            — 实体事实对活动事实的关系（可分类、线性、非线性、回归）
│   └── 上下文因素    — 影响的外部因素（组织、过程模型、产品、工具、人员）
└── 经济层
    ├── 成本              — 活动事实的经济量级
    └── 资源          — 受影响的资源类型（时间、金钱等）
```

#### 树 B：§4 抽取编码本（抽取 编码本；**真正的样本编码维度树**）

> 这是 §4.2 抽取 指南 中"每个 RQT concept 关联 ≥1 个 categorical variable + 代码"的真实复原。Page 8 §4.3 提到的所有 代码 与分母都来自此树。文本明确列出的 代码 完整列出；文本未展开但暗示存在的 代码 标 待核验（Zenodo 复现包）。

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[B] 样本编码树（样本编码树；首次术语）— 需求质量理论编码本（需求质量理论编码本；首次术语）应用于 57 篇原始研究
│
├── 实体报告情况
│   └── 实体显式性（stable id: B.entity.explicitness）取值 ∈ {明确（explicit）, 隐式（implicit）}
│       — Page 7 显式定义；Page 8 隐式（implicit）= 24/57 = 42.1%
│
├── 因素报告情况
│   ├── 因素显式性（stable id: B.factor.explicitness）取值 ∈ {明确报告、引用自另一出版物（原枚举标识保留于审计附录）}
│   │   — Page 7 §4.2 显式
│   └── 因素表达形式（stable id: B.factor.form）取值 ∈ {文本描述、逻辑或数学公式（原枚举标识保留于审计附录）}
│       — Page 7 §4.2 显式
│
├── 实体事实报告情况     ⟵ 文本未展开代码（待 Zenodo 核验）
│
├── 主体报告情况
│   └── 主体是否出现（stable id: B.agent.presence）取值 ∈ {已报告、未报告}
│       — Page 8 已报告= 14/57 = 24.6%
│
├── 活动报告情况
│   ├── 活动是否出现（活动出现情况（stable id: B.activity.presence））取值 ∈ {已报告、未报告}
│   │   — 当“已报告”时分母 = 40
│   └── 活动获取方式（stable id: B.activity.elicitation_mode）取值 ∈ {临时识别、系统识别（原枚举标识保留于审计附录）}
│       — Page 8 临时识别 = 37/40 = 92%
│
├── 属性报告情况
│   └── 属性是否出现（stable id: B.attribute.presence）取值 ∈ {已报告、未报告}
│       — Page 8 已报告= 8/57 = 14%
│
├── 活动事实报告情况   ⟵ 文本未展开代码（待 Zenodo 核验）
│
├── 影响报告情况          ⟵ 4 个维度（论文正文仅报告其中 2 个）
│   ├── 影响是否出现（影响出现情况（stable id: B.impact.presence））取值 ∈ {已报告, 不适用（N/A）}
│   │   — Page 8 N/A = 17/57 = 29.8%；已报告分母 = 40
│   ├── 影响证据类型（stable id: B.impact.evidence）取值 ∈ {假设性、归纳式、引用式}
│   │   — Page 8 假设性19/40、归纳式11/40、引用式10/40
│   ├── 影响模态（stable id: B.impact.modality）取值 ∈ {必要、可能}
│   │   — Page 8 原文说明“必要”和“可能”大体均衡
│   ├── 影响普遍性（stable id: B.impact.generality）⟵ 编码存在但 Page 8 原文说明未产生额外洞察
│   └── 影响参照框架（stable id: B.impact.frame_of_reference）⟵ 编码存在但 Page 8 原文说明未产生额外洞察
│
├── 上下文因素报告情况
│   └── 上下文因素子类（stable id: B.context_factor.sub_category） 取值 ∈ {工具、产品、组织、过程、人员, …}
│       — Page 8 工具= 0/57；产品= 14/57 = 24.6%；其他子类待 Zenodo 核验
│
├── 成本报告情况
│   ├── 成本是否出现（成本出现情况（stable id: B.cost.presence））取值 ∈ {已报告、未报告}
│   │   — Page 8 已报告= 9/57 = 15.8%
│   └── 成本证据（stable id: B.cost.evidence）取值 ∈ {假设性、引用式、经验式}
│       — Page 8 "仅为假设性或引用式，未被经验确定"
│
└── 资源报告情况
    ├── 资源是否出现（资源出现情况（stable id: B.resource.presence））取值 ∈ {已报告、未报告}
    │   — Page 8 已报告= 5/57 = 8.8%
    └── 资源类型（stable id: B.resource.type）取值 ∈ {金钱, 时间, …}
        — Page 8 "提到金钱和时间"；其他类型待 Zenodo 核验
```

#### 树 C：§5 路线图 streams（候选发现树（候选发现 树））

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[C] 路线图主线
├── 5.1 制品与使用模型（Artifact and usage model）— 含参考活动模型与属性（参考活动模型与属性（reference activity model and attributes））
├── 5.2 质量因素分类法（taxonomy of quality factors）— 基于质量因素本体（质量-factor ontology）
├── 5.3 影响框架（impact framework）               — 升级自原影响分类法（分类法 of impacts）；引入回归 / 贝叶斯方法（Bayesian）
├── 5.4 上下文因素                — 需求工程（RE）专属上下文因素（context factor）集合
├── 5.5 经济影响（Economic impact）— 把活动事实（activity-fact）关联到成本 / 资源（cost/resource）
└── 5.6 工具支持（tool support）— 实体与上下文刻画（entity & context characterization）+ 影响预测（impact prediction）
```

#### 当前 review.md 缺失的部分

- 把 §4 编码本（树 B）当作"原文模式主树"完整列出。
- 把 影响的 4 个子维度（证据 / 模态 / 普遍性 / 参照框架）显式列叶。
- 把 因素的显式性 × 表达形式 两组 代码 显式列叶。
- 把 成本与资源的子代码（证据、type）显式列叶。

---

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `B.entity.explicitness` | 实体显式性 | 实体报告情况 | §4.2 显式给出 | 一篇文献是否清晰报告 entity 的 scope 与 form | {显式（explicit）, 隐式（implicit）} | 完整枚举 | 不报告时默认 implicit | 分子/57；隐式（implicit）= 24/57 | "术语模糊"型 缺口发现 | 可迁移为 Paper2 中字段 explicit/implicit 二分；不迁移 RE 领域结论 |
| `B.factor.explicitness` | 因子显式性 | 因素报告情况 | §4.2 显式 | 因子是本文显式定义还是引用其他文献 | {明确报告、引用自另一出版物（原枚举标识保留于审计附录）} | 完整枚举 | 所有 57 篇都报告 factor，无缺失 | 分子/57 | 引用链型 候选发现 | 可迁移结构；不迁移 RE factor 具体集合 |
| `B.factor.form` | 因子形式 | 因素报告情况 | §4.2 显式 | 因子是文字描述还是数学/逻辑公式 | {文本描述、逻辑或数学公式（原枚举标识保留于审计附录）} | 完整枚举 | 默认文本描述 | 分子/57 | 形式化程度型 发现 | 可迁移；Paper2 字段可同构分"文本/形式化" |
| `B.agent.presence` | 主体报告与否 | 主体报告情况 | §4.3 | 是否报告活动中的 智能体 | {已报告、未报告} | 布尔 | 未报告 | 14/57 = 24.6% | 活动侧缺口发现 | 可迁移 |
| `B.activity.presence` | 活动报告与否 | 活动报告情况 | §4.3 | 是否报告 受影响活动 | {已报告、未报告} | 布尔 | 未报告；进入 17/57 N/A | 40/57 已报告 | 缺口发现 | 可迁移 |
| `B.activity.elicitation_mode` | 活动识别方式 | 活动报告情况 | §4.3 | 活动是临时识别还是系统识别 | {临时识别、系统识别（原枚举标识保留于审计附录）} | 完整枚举 | 仅当活动已报告时生效，分母 40 | 37/40 = 92% 为临时识别 | "非系统性 activity"型 发现 | 可迁移 |
| `B.attribute.presence` | 属性报告与否 | 属性报告情况 | §4.3 | 是否报告 活动的可测属性 | {已报告、未报告} | 布尔 | 未报告 | 8/57 = 14% | 测量缺口发现 | 可迁移 |
| `B.impact.presence` | 影响报告与否 | 影响报告情况 | §4.3 | 是否报告 factor → 活动的 impact | {已报告, 不适用（N/A）} | 布尔 | N/A 计 17/57 | 已报告分母 = 40 | core 缺口发现 | 可迁移 |
| `B.impact.evidence` | 影响证据类型 | 影响报告情况 | §4.3 | impact 关系的证据基础 | {假设性、归纳式、引用式} | 完整枚举 | 仅当 impact 已报告；分母 40 | 19 / 11 / 10 of 40 | "证据等级"型 发现 | 可迁移为 Paper2 evidence_type 字段 |
| `B.impact.modality` | 影响模态 | 影响报告情况 | §4.3 | impact 是必然还是可能 | {必要、可能} | 完整枚举 | impact 已报告 子集 | "balanced" 文本表述 | "确定性 vs 可能性"分布 发现 | 可迁移 |
| `B.impact.generality` | 影响普遍性 | 影响报告情况 | §4.3 提到但未展开 | impact 是普遍还是上下文特异 | 待核验（Zenodo） | 待核验 | 文本声明"no additional insight"故未报告 | 不进入本文统计 | A2a 补叶后可作 候选发现 | 取值空间未核验前不得统计 |
| `B.impact.frame_of_reference` | 影响参照框架 | 影响报告情况 | §4.3 提到但未展开 | impact 的参照对象 | 待核验（Zenodo） | 待核验 | 同上 | 不进入本文统计 | A2a 补叶后可作 候选发现 | 同上 |
| `B.context_factor.sub_category` | 上下文子类 | 上下文因素报告情况 | §4.3 | 报告了哪类 context（工具 / product / organization / 流程 / people …） | 工具, 产品（product，已命名）, 其他（待 Zenodo 补全） | 层级枚举 | 多数为 0 报告 | 工具=0；product=14/57；其他待核 | "context 忽视"型 缺口发现 | 可迁移为 Paper2 context 多类字段 |
| `B.cost.presence` | 成本报告与否 | 成本报告情况 | §4.3 | 是否报告经济成本 | {已报告、未报告} | 布尔 | 未报告 | 9/57 = 15.8% | 经济侧缺口发现 | 可迁移 |
| `B.cost.evidence` | 成本证据类型 | 成本报告情况 | §4.3 | cost 的证据基础 | {假设性, 引用式, 经验式（empirical；本样本为 0）} | 完整枚举 | cost 已报告 子集；分母 9 | "never 通过经验方式确定（empirically determined）" | 经验研究（empirical）-证据 缺口（gap） | 可迁移 |
| `B.resource.presence` | 资源报告与否 | 资源报告情况 | §4.3 | 是否报告 resource 类型 | {已报告、未报告} | 布尔 | 未报告 | 5/57 = 8.8% | 资源侧缺口发现 | 可迁移 |
| `B.resource.type` | 资源类型 | 资源报告情况 | §4.3 | 受影响资源的具体类型 | {金钱, 时间, …待 Zenodo} | 部分枚举 | 资源已报告子集；分母 5 | 金钱 / 时间文本提及 | 资源类型分布候选发现 | 可迁移；类型空间需 A2a 扩展 |
| `B.entity_fact.codes` | 实体事实代码 | 实体事实 | §3 概念存在；§4 文本未展开 | 实体 × 因素（entity-factor） 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 entity + factor 联合 | 不进入本文统计 | 复合事实型 发现 入口 | 取值空间未核验前不得统计 |
| `B.activity_fact.codes` | 活动事实代码 | 活动事实 | §3 概念存在；§4 文本未展开 | 活动（activity） × 属性（attribute） 的取值表达方式 | 待核验（Zenodo） | 待核验 | 视为 activity + attribute 联合 | 不进入本文统计 | 同上 | 同上 |

---

### 5. 关系边表

本文 RQT 是**显式关系型模型**（Fig. 2 即关系图）。关系边来自树 A（概念模型），而非树 B（编码本）。树 B 是字段-代码 平面表，本身没有关系边。

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `R1.entity_compose` | 实体 | 分解为 | 子实体 | 递归实体类型 | 单层实体不报告子实体 | §3.1 Page 4 | 表达需求粒度层级 |
| `R2.factor_compose` | 因素 | 分解为 | 子因素 | 递归因素类型 | 单层因素不报告子因素 | §3.1 Page 4（Antinyan 例） | 表达复合因子 |
| `R3.entity_fact` | 实体 × 因素 | 组合为 | 实体事实 | 由实体与因素联合定义 | 未取值时不存在实体事实 | Table 1 Page 5 | 编码具体观测 |
| `R4.activity_compose` | 活动 | 分解为 | 子活动 | 递归活动类型 | 单层活动不分解 | §3.1 Page 4–5 | 表达 理解 等子活动 |
| `R5.activity_fact` | 活动 × 属性 | 组合为 | 活动事实 | 由活动与属性联合定义 | 未取值时不存在活动事实 | Table 1 Page 5 | 编码活动观测 |
| `R6.impact` | 实体事实 | 影响 | 活动事实 | 关系模型：分类 / 线性 / 回归 / 贝叶斯 | 影响不报告 = 不适用 | §3.1 generalised impact, Page 5 | 核心因果/关系边 |
| `R7.context_modulates` | 上下文因素 | 调节 | 影响（实体事实→活动事实关系） | 同影响取值空间 | 上下文不报告 = 假设统一上下文 | §3.1 Page 5 + 例 Page 6 | 解释外部效度 |
| `R8.activity_fact_cost` | 活动事实 | 产生 | 成本 | 成本数值或量级 | 不报告 = 无经济维度 | §3.1 Page 5 | 经济关系边 |
| `R9.cost_resource` | 成本 | 消耗 | 资源 | 金钱 / 时间 / … | 不报告资源时成本保持抽象 | §3.1 Page 5 | 资源映射边 |
| `R10.agent_activity` | 主体 | 执行 | 活动 | 主体类型 | 活动不报告主体时假设隐式主体 | §3.1 Page 5 | 人/工具归属 |

当前版本已在上表按 R1–R10 补入关系边；后续只需在 A2a 精核页码与 Zenodo 证据。

---

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表支持的统计观察（仅限本文样本 n=57，convenience）

1. Entity-explicitness：隐式（implicit）= 24/57 (42.1%)。
2. Factor：所有 57 篇都报告 factor；explicitness 与 form 子分布作者文本未展开数字。
3. Agent：已报告= 14/57 (24.6%)。
4. 活动：已报告 = 40/57；其中临时识别 = 37/40（92%）。
5. Attribute：已报告= 8/57 (14%)。
6. Impact：N/A = 17/57 (29.8%)；已报告 40/57 中 证据 = hypothesized 19 / inductive 11 / referenced 10；modality "balanced"。
7. Context factor：工具= 0%；product-related = 14/57 (24.6%)。
8. Cost：已报告= 9/57 (15.8%)；从未 通过经验方式确定（empirically determined）。
9. Resource：已报告= 5/57 (8.8%)；types 提及 money、time。
10. Reliability：percentage agreement 83.3%；Cohen's κ = 54.2%（作者标 moderate，并自陈受 uneven marginal 影响）；S-Score = 76.8%。

#### 6.2 原文 discussion / 推荐 / 路线图 候选发现

1. requirements 质量 literature 实现 制品-centric 偏置，activity / context / economic 覆盖严重不足（§4.4 + §6）。
2. 32/40 已报告 activities 涉及 理解/interpretation 子活动 → 暗示 interpretation 是关键 sub-activity（§5.1）。
3. 路线图 6 streams 是 缺口（gap） → action 的直接映射（§5.1–§5.6）。
4. impact 应升级为 框架 而非 分类法（§5.3）。

#### 6.3 对 Paper2 可迁移的方法学启发

1. 把 研究者-defined meta-模型 当作"第一贡献"，再用 编码本 把 meta-模型 转成可统计变量。
2. 用 inter-rater reliability + 双人编码 + 复现包 验证 编码本。
3. 把 缺口（gap） 分布转成 路线图行动项 而不是停留在频次。
4. 显式区分 impact 的 4 个子维度（证据 / modality / generality / frame_of_reference）作为字段冗余/正交检验。

#### 6.4 绝不可迁移的领域结论

1. RE 领域中 entity-implicit / impact-N/A 等具体比例。
2. RQT 11 个具体 concept 名（Entity、Factor 等不能直接套用到 SLR/SMS 的 Paper、Field 等对象）。
3. 路线图 6 streams 的具体名称与内容（属 RE 领域 future work，不是 Paper2 的）。
4. 质量因素本体（质量-factor ontology）、AMDiRE、Quamoco、ABRE-QM 等被引工具的具体可用性。

---

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
