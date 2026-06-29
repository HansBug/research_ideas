# Formal requirements engineering and large language models: A two-way roadmap

## 1. 快速结论卡片

| 字段 | 内容 |
|---|---|
| 标题 | Formal requirements engineering and large language models: A two-way roadmap |
| 作者 | Alessio Ferrari; Paola Spoletini |
| 年份 | 2025；在线发表日期 2025-02-18；卷期页码 Information and Software Technology 181:107697 |
| DOI | <https://doi.org/10.1016/j.infsof.2025.107697> |
| 类型 | vision / roadmap；不是 SLR / SMS / tertiary study |
| 出版形态 | 期刊 |
| 期刊/会议/预印本 | [IST](https://www.sciencedirect.com/journal/information-and-software-technology) |
| CCF 官方大类 | 软件工程 / 系统软件 / 程序设计语言 |
| CCF 官方等级 | B |
| CCF 复核状态 | 本地缓存；官方待人工复核（WAF） |
| 来源等级 | IST 2025；正式期刊 roadmap / vision paper；开放全文 PDF 已入库 |
| 阅读状态 | 已读全文文本-paper_content核验；关键图 Fig. 2 / Fig. 4 已回 PDF 图片核对 |
| 证据等级 | 全文文本级；两张 roadmap 图为 原文图表级人工核对；其余表格/代码清单未逐项复核排版 |
| 核验入口 | [bibtex.bib](./bibtex.bib)、[metadata.json](./metadata.json)、[paper_content.txt](./paper_content.txt)、[paper.pdf](./paper.pdf) |
| 主题 | formal requirements engineering / formal methods 与 LLM 的双向赋能：LLM 提高 FM 可用性，FM 提高 LLM-based RE 的可靠性、正确性、公平性和可信性。 |
| A1 角色 | roadmap 边界锚点：证明本脚手架需要容纳非 SLR/SMS 的高价值 vision / roadmap 文献，但其贡献应作为字段树、concern taxonomy 和 finding heuristic 先验，不可升级为目标领域经验发现。 |
| 是否目标证据池 | 否；只作为 Paper2 综述元模型、维度模式、trustworthiness concern 与候选发现启发式的先验。 |
| schema 历史观察 | 现有六类 SLR/SMS pattern 不足以表达 roadmap 文的双向路线、concern、action point、trustworthiness constraint；建议仅在本条记录为候选字段树，若后续 A2a 采纳再回修 schema。 |

## 2. 阅读范围与证据锚点

本轮按用户指定完成单篇全文阅读：先读 [bibtex.bib](./bibtex.bib) 和 [metadata.json](./metadata.json) 锁定元信息，再通读 [paper_content.txt](./paper_content.txt) 的摘要、引言、背景、两个示例、两个 roadmap、实践考虑、结论和参考文献列表；必要处回到 [paper.pdf](./paper.pdf) 核对 Fig. 2 与 Fig. 4 的层级结构。

关键锚点如下：

- 摘要与贡献边界：`paper_content.txt` Page 1--2，说明目标是用两组示例揭示 FM 与 LLM 的局限，并提出两个 roadmaps；正文明确这是 vision paper，不提供 sound empirical evidence，且 roadmap 不应视为 exhaustive。
- 背景：Page 2--6，覆盖 LLM/RE 应用、formal specification、temporal logic、formal models、model checking、proof assistant、deductive verification、refinement 等。
- FM-based development 示例：Page 6--8，sender-receiver handshaking protocol，PROMELA / Spin / LTL assertion / counterexample / Python 实现。
- Roadmap A：Page 8--11 与 Fig. 2，LLM agents 支持 FM-based development。
- LLM-driven RE/SE 示例：Page 11--14，ChatGPT 3.5 生成/分析/补全需求、生成 PlantUML sequence diagram、分类、追踪和代码相关任务。
- Roadmap B：Page 14--16 与 Fig. 4，FMs 支持 LLM-based development。
- Practical considerations and limitations：Page 16--17，专家协作、经验评估、overreliance、人类创造力、FM 数据不足、制品维护、部署/扩展/技术演化。
- 结论与数据声明：Page 17--18，强调两个 roadmap 用于激发研究；声明 No data was used。

## 3. 全文内容详读

### 3.1 背景 / 问题设定

论文的出发点不是“LLM 已经可以自动完成 RE”，而是更谨慎：LLM 在需求摘要、用户故事、追踪、模型生成等 RE 任务上表现出潜力，但输出存在可靠性、正确性、可解释性和可信性问题。作者提出 formal requirements / formal methods 可以为 LLM-assisted RE 活动提供保证；反过来，formal RE 的门槛高、工具复杂、应用多局限于 critical / complex systems，LLM 可以帮助 formalisation、解释 formal artefacts、解释 formal tools 的结果，从而提高 FM 可用性。

背景章节有两个作用：

1. 为非 NLP 读者建立 LLM 技术背景：传统 BoW/tf-idf、word embeddings、BERT、LLM、prompting、instruction tuning、RAG、LoRA、distillation、LLM agents。
2. 为非 FM 读者建立 formal RE 背景：formal specification language、temporal logic、formal models、model checking、proof assistant、deductive verification、design by refinement。

对本仓库尤其相关的是作者把 formal RE 定义为一组数学化技术，用于 specification、model、verification；其中 formal models 涵盖 LTS/FSM/Büchi Automata、Timed Automata、Probabilistic/Stochastic State Machines、Statecharts、Petri Nets 等，formal analysis 涵盖 abstract interpretation、static analysis、model checking、proof assistants、deductive verification、refinement。该定义与 project_1 的状态机建模、pyfcstm / UPPAAL / 时间约束方向高度贴近。

### 3.2 Roadmap 构造方式

该文不是系统综述，也没有 PRISMA 式检索、纳排、质量评价或统计综合。roadmap 的构造方式更接近“例子驱动的 vision synthesis”：

1. 先给出一个 formal software development 示例，展示 NL requirements → formal model / property → model checking → implementation 的链路，以及 formal process 的复杂性和可用性障碍。
2. 基于该示例抽出 LLM 能帮助 FM 的 action points，并在 Fig. 2 中组织为 Formal Development Layer、Conventional Development Layer 与 LLM Layer 的交互。
3. 再给出一个 LLM-driven software development 示例，展示 ChatGPT 3.5 在需求生成、反馈分析、smell detection、completeness check、requirements completion、model generation、requirements classification、requirements tracing 等 RE/SE 任务中的潜力与风险。
4. 基于第二组示例抽出 FM 能帮助 LLM 的 action points，并在 Fig. 4 中组织为 Formal Layer、SW Artifact Layer 与 LLM Layer 的交互。
5. 最后用 practical considerations and limitations 约束 roadmap 的可实施性，明确这不是经验验证，而是研究议程。

这对 Paper2 有一个重要提示：roadmap 文的价值不在统计“出现了多少技术”，而在把 concern、artefact、mechanism、guarantee、risk 和 action point 串成一个可审计字段树。

### 3.3 示例一：formal software development

作者用 sender-receiver handshaking protocol 展示 formal RE 过程。初始 NL requirements 包括 message integrity、order preservation、flow control。随后作者给出 PROMELA 模型，包含 Sender / Receiver 两个 process，并用 Spin 验证 Flow Control 对应的性质：Receiver 当前收到的 message 应等于 Sender 当前生成的 message。正确模型通过验证；去掉 control channel 后，Spin 生成 counterexample，展示 Sender 可在 Receiver 处理旧消息前继续产生新消息。最后作者给出 Python sender / receiver 实现，并指出代码有 host、port、socket 等模型中没有的细节，因此仍可能需要额外 verification；Python 代码也可借助 Dafny / Nagini 等方向进行验证。

该示例服务于 roadmap A：formal methods 强，但成本来自 formal model / property / code / counterexample / implementation 之间的手工转换、抽象和解释。

### 3.4 Roadmap A：Using LLMs to support FM-based development

Fig. 2 由三个图层组成：Formal Development Layer、Conventional Development Layer、LLM Layer。核心思想是用多个 LLM agents 连接 formal artefacts 与 conventional artefacts。五个 action points 如下。

1. **Generating FM and SE Artifacts**：从 formal specification 生成 code，或从 code / requirements 生成 formal specification / logic formulae。作者强调 specification-to-code 可用 RAG 引入已有库；code-to-model 需要从实现细节中抽象出可验证的 functional backbone，避免 state-space explosion；NL-to-logic 需要处理歧义、专业 requirement-formula 数据集与解释。
2. **Explaining FM Artifacts**：LLM 可解释 formal models、logic formulae、assertions、counterexamples。该点直击 FM 可用性：domain experts 通常不自己写 formal specification，但需要理解 specification 是否正确表达了系统信息；counterexample 也需要自然语言解释。
3. **Translating Formal Languages**：不同 formal languages / tools 服务不同 concern、property、audience；LLM 的 code-to-code translation 能力可用于 model-to-model / logic-to-logic translation，以支持 FM diversity 和不同抽象层级视图。
4. **Supporting Iterations and Evolution**：formal RE-based process 也是增量迭代的，requirements、specifications、tests、code 和其他 artefacts 需要 trace-links 保持一致；作者建议组合 code-specific LLM 与 NL-oriented LLM 支持 trace-link identification。
5. **Automating Knowledge Engineering**：LLM 可从 requirements、models、documentation、tests 等 artefacts 抽取知识，构建 ontologies；ontologies 又可反过来支持一致性检查、artefact 生成、解释与 trace。

对 project_1，Roadmap A 的可迁移点是：LLM 不应只被看作“生成状态机”的黑箱，而应拆成 Req2Logic、Req2Model、Code2Model、Model2Code、Explanation、Trace-link、Knowledge Representation 等角色；每个角色对应不同输入、输出、可验证边界和失败模式。

### 3.5 示例二：LLM-driven software development

第二组示例不追求 benchmark，而是展示 LLM 支持 RE/SE 的典型任务面。作者使用 ChatGPT 3.5 online interface，并说明输出经过少量压缩和有限调整，有些图需要多轮提示才能得到清晰结果。示例包括：

1. **Requirements Generation**：为 guitar tuning app 生成 user stories，既包含常规功能，也包含社交/协作等较有创造性的功能。
2. **User Feedback Analysis**：用 RAG 想象场景把用户反馈归纳为 Accuracy、Performance、Security、Compatibility、Cost 等 concerns，并映射到 non-functional requirement classes。
3. **Smell Detection**：检测 anaphoric ambiguity，区分 nocuous / innocuous ambiguity；也识别 generality。
4. **Completeness Check and Requirements Completion**：以 railway red-crossing function 为例，LLM 识别单条需求与需求集层面的缺口，并补全 architectural / functional requirements。
5. **Model Generation**：用 PlantUML / PlantText 从补全后的 red-crossing requirements 生成 UML sequence diagram。
6. **Requirements Classification**：把一个涉及 ease-of-use 与 underage access 的需求同时归入 usability / security。
7. **Requirements Tracing**：推断 dashboard 与 electronic speedometer 的关系，从而建议两条需求应建立 trace。
8. **Code-related Tasks**：作者只简述 code generation、comments、tests 等，因为本文主要聚焦 RE。

示例的价值在于揭示 LLM 输出“看起来合理但需要控制”：能生成、分类、推断和补全，但可能过度补充、隐式引入架构假设、受提示语影响且不具备可重复保证。

### 3.6 Roadmap B：Using FMs to support LLM-based development

Fig. 4 由 Formal Layer、SW Artifact Layer、LLM Layer 组成。LLM Layer 分析或生成需求、模型、代码、测试等 SW artefacts；Formal Layer 以 formal requirements、formal verification、argumentation、FM knowledge、formal domain knowledge、formal prompts、runtime verification、ethical requirements 等方式提供控制。七个 action points 如下。

1. **Ensuring Correctness through Formal Requirements and Argumentation**：LLM-generated requirements / specifications / artefacts 需要像人工需求一样做 quality assurance；formal notation、formal specification、verification、formal argumentation structure 可提高可解释性、逻辑一致性并缓解 hallucination。
2. **Improving Mathematical Reasoning with Formal LLMs**：cyber-physical requirements 常包含数学公式；LLM 数学推理弱，可通过数学/FM 专用模型、RAG、多个专长 LLM agents、calculator / reasoner 等外部工具支持。
3. **Formal Prompt Engineering**：prompt 在 code/model generation 场景中近似“需求”；自然语言 prompt 也会有歧义。作者建议用 formal notations、controlled NL、pre/post-conditions、UML-like prompt architecture 来约束 prompt 和 agent orchestration。
4. **Formal Domain Knowledge and Explainability**：domain-specific text scarce 时，formal ontologies / knowledge graphs 可约束推理、减少 hallucination、提高效率，并作为解释/justification 的外部依据。
5. **Ensure LLM Output Consistency through Formal Verification**：LLM 系统缺乏传统软件那种 predictability / repeatability；作者提出用 abstract interpretation / abstraction methods 近似分析 neural network 行为，验证 prompt perturbation 下输出一致性，尤其面向 safety-critical LLM components。
6. **Regulatory Compliance at Runtime**：LLM 会随新知识或 fine-tuning 演化，法规也会变化；runtime verification 可用于持续监测 regulatory requirements。
7. **Mitigate Bias and Address Ethical Concerns**：trustworthiness threats 包括 toxicity、stereotype bias、adversarial / out-of-distribution robustness、privacy、machine ethics、fairness 等；作者建议 formalise ethical requirements，并用 formal techniques 验证 LLM-generated artefacts。

对 Paper2 最关键的是 Roadmap B 的组织方式：不是笼统说“formal methods make LLM reliable”，而是把 reliability 分解为 correctness、logical coherence、mathematical reasoning、prompt precision、domain grounding、output consistency、regulatory compliance、bias/ethics/fairness 等 concern，并给出对应 formal mechanism。

### 3.7 主要结论

论文结论保持 vision paper 口径：两个 roadmaps 旨在激发 RE / SE 社区研究。一方面，LLM 可让 formal languages / tools 更易用；另一方面，在 LLM 参与 RE 活动时，formal techniques 可缓解 LLM-generated artefacts 的正确性和可信性问题，并支撑 responsible / trustworthy AI。作者特别指出这些 roadmaps 适合 mission-critical systems 的 rigorous process，如 V-process，但并不限于此，因为 safety、security、privacy、ethical requirements 正变得更普遍。

作者自述将优先推进三个方向：requirements-to-formal-logic translation、LLM 生成/分析软件 artefacts、LLM 解释 formal artefacts。

### 3.8 局限与实践考虑

原文局限不是传统 threats-to-validity 表，而是 practical considerations：

1. LLM 与 FM 专家分属 statistical vs deterministic 思维传统，需要 RE bridge role。
2. 经验评估困难：RE 缺少数据集，FM 经验成熟度有限；很多 generative output 没有唯一 ground truth，需要 qualitative methods。
3. overreliance：LLM 幻觉可能因语言流畅和“自信”解释误导 analyst；formal verification 不是全部，还需要 human-centred quality control、hallucinatory pattern 识别和部署前 robustness testing。
4. 人类创造力风险：图中有意省略 human actors，以强调自动化，但作者反过来认为 requirements engineers 会更核心，因为 requirements 成为控制 LLM/code generation 的主要接口。
5. FM 数据训练不足：formal language 数据有限，需 code-specialised LLM、FM fine-tuning、多模型集成、interactive generation、agent 访问 model checker / compiler 等。
6. 制品增殖与可维护性：更多 code、models、formulae、counterexamples、trace links 会带来维护负担，需要可视化、analytics 和演化监控。
7. 部署、扩展和技术演化：FM 有 state-space explosion，LLM 有计算资源需求；LLM 技术迭代快，组织需可渐进部署和适应变化。

## 4. 六类 pattern 抽取

| 模式类型 | 抽取结论 | 证据锚点 | 可迁移性 | 不可迁移点 / 限制 |
|---|---|---|---|---|
| RQ pattern | 原文没有正式 RQ 列表；隐含问题是两个对称问题：如何用 LLM 提高 formal RE / FM 可用性，如何用 FMs 提高 LLM-based RE 的 correctness / fairness / trustworthiness。 | 摘要 Objective / Methods；Introduction contributions；Sections 4 与 6。 | 可迁移为 Paper2 的“roadmap question pattern”：双向关系 + concern + mechanism + action point。 | 不适合作为 SLR/SMS 的 RQ 模板；没有系统检索问题、纳排问题或统计综合问题。 |
| dimension pattern | 维度不是 review extraction dimensions，而是 roadmap axes：方向、层级、artefact、任务、mechanism、concern、action point、limitation。Roadmap A 有 5 个 action points，Roadmap B 有 7 个 action points。 | Fig. 2、Fig. 4；Sections 4 / 6 summaries。 | 高度可迁移为 Paper2 的字段树，特别适合将“技术路线”拆成 task / artefact / constraint / evidence / risk。 | 不是由系统编码得到的 taxonomy，存在作者经验选择偏差；不能当成饱和分类体系。 |
| finding pattern | 原文的“发现”主要是 vision conclusions 与 action points，而非经验 findings。可抽取为 concern-to-action heuristic：识别技术痛点，再提出 formal / LLM 机制。 | Sections 4 / 6 的每个 Action Point；Section 7 limitations。 | 可迁移为候选发现生成启发式：统计观察之后必须说明 concern、机制、证据强度、限制和所需验证。 | 不可把 action points 写成已验证 research findings；不支持“LLM+FM 必然可行”之类强主张。 |
| evidence presentation pattern | 证据呈现采用两组 worked examples、代码清单、model-checking counterexample、ChatGPT prompt/output 片段、两张 roadmap 图和大量文献锚点。 | Section 3 sender-receiver；Section 5 LLM-driven RE examples；Fig. 2 / 4。 | 可迁移为 Paper2 的 evidence package：示例 + 图层 + action point + 限制，比单纯文字综述更容易审计。 | 示例不是 benchmark；ChatGPT 输出有人工压缩/有限调整；没有样本分母、纳排流程或可重复实验协议。 |
| validity / threat pattern | 没有传统 threats-to-validity 章节；Section 7 以 practical considerations 替代，覆盖专家协作、评价难题、overreliance、human role、training data、artefact maintainability、scalability、technology evolution。 | Section 7。 | 可迁移为 Paper2 risk register 字段，尤其是 overreliance、human-centred QC、model/tool drift、artefact proliferation。 | 不是系统化效度威胁模板；缺少对文献选择、示例选择和作者主观判断的显式方法学威胁分析。 |
| report structure pattern | 结构是：structured abstract → Introduction / Background → formal process example → Roadmap A → LLM-driven RE example → Roadmap B → Practical considerations → Conclusion。 | 全文目录与章节。 | 对 Paper2 的 roadmap / discussion section 有参考价值：先示例揭示痛点，再分层路线图，再列 implementation risks。 | 不适合直接复制为 SLR/SMS report structure；缺少 Method / Search / Selection / Data extraction / Synthesis 章节。 |

## 5. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 | 可用方式 | 限制 |
|---|---|---|---|
| A1-M0 主题与综述元模型设定 | 提供“LLM automation 需要被 correctness / fairness / trustworthiness concerns 约束”的主题边界；也提供“LLM 支持形式化、形式化约束 LLM”的双向元模型。 | 在 Paper2 设定综述元模型时，可把 automation capability 与 audit / assurance capability 并列，而不是只收集工具功能。 | Roadmap 不是系统证据，不能决定最终综述范围；需要研究者批准。 |
| A1-M1 脚手架挖掘与种子探测 | 可作为非 SLR/SMS 的 roadmap seed，用来挖掘 concern/action pattern：accessibility、correctness、explainability、traceability、domain knowledge、regulatory compliance、ethics。 | 用于补充 `survey_of_surveys` 的 pattern library，提醒 A2a 支持 `vision/roadmap` 类型。 | 只做边界锚点；不能进入目标 evidence pool。 |
| A1-M2 维度模式批准 | 启发字段：`roadmap_direction`、`layer`、`task_family`、`artifact_in/out`、`assurance_concern`、`mechanism`、`action_point`、`evaluation_need`、`implementation_risk`。 | 研究者可把这些字段纳入候选维度模式，要求每个候选发现都说明 concern 与 mechanism。 | 若过度扩字段，会让抽取负担过高；需 A2a dry-run 决定是否拆分。 |
| A1-M3 论文收集与概览 | 提醒候选池不要只收 SLR/SMS；高价值 vision/roadmap 需要以 `review_type=vision/roadmap` 降级管理。 | 概览卡中显式写“非 SLR/SMS，但可作 schema/heuristic seed”。 | 不能把 roadmap 文数量统计混入 SLR/SMS 统计口径。 |
| A1-M4 字段级证据抽取与模式演化 | 提供 action-point-level evidence anchors；每个 action point 都可抽为 `concern -> mechanism -> artifact -> limitation`。 | 对 Paper2 字段证据表，可要求非统计类文献也保留来源锚点和不确定说明。 | 作者观点和例子驱动，不应作为强证据；要标注证据等级。 |
| A1-M5 统计分析 | 主要贡献是负面边界：本文不支撑分布统计，不应纳入频次结论。 | 在统计分析协议中增加 `eligible_for_statistical_synthesis` 或 `evidence_role` 字段。 | 若混入统计，会污染目标综述 findings。 |
| A1-M6 候选发现形成 | 启发候选发现从“某技术常见”升级为“某 concern 在某 artefact/task 中出现，现有 mechanism 能部分缓解，但需要某类验证”。 | 适合生成 finding heuristic：concern-first、mechanism-linked、risk-aware、human-gated。 | 只能生成候选发现线索，不能直接接受为最终领域发现。 |

## 历史草稿（已迁移，不作事实真源）：旧第 6 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

### 历史草稿（已迁移，不作事实真源）：旧第 6.1 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

- `roadmap_id`
  - `LLM_for_FM_usability`：LLM 支持 FM-based development。
  - `FM_for_LLM_trustworthiness`：FMs 支持 LLM-based development。
- `direction`
  - `LLM -> FM/RE artefact`
  - `FM/formal artefact -> LLM governance`
  - `bidirectional / feedback`
- `layer`
  - formal layer / formal development layer
  - conventional or SW artefact layer
  - LLM / agent layer
  - knowledge layer / external tool layer
- `task_family`
  - generation：Req2Logic、Req2Model、Model2Code、Code2Model、test/code/comment generation
  - analysis：smell detection、completeness check、classification、trace-linking、counterexample explanation
  - transformation：model-to-model、logic-to-logic、prompt architecture、ontology construction
  - assurance：formal verification、argumentation、runtime monitoring、ethical requirements validation
- `artifact_in`
  - natural language requirements、user stories、feedback、issues、code、formal model、logic formula、counterexample、domain documents、regulations、ethical principles
- `artifact_out`
  - formal specification、formal property、software model、code、trace link、classification、explanation、knowledge graph、verification result、runtime monitor、candidate requirement completion
- `mechanism`
  - prompt engineering / formal prompt
  - RAG / external knowledge
  - specialised LLM / fine-tuning / LoRA / distillation
  - multi-agent orchestration
  - model checking / static analysis / abstract interpretation / proof / runtime verification
  - ontology / knowledge graph / argumentation structure
- `action_point`
  - 以原文 Section 4 的 5 个和 Section 6 的 7 个 action points 为初始取值；后续 A2a 可合并或扩展。
- `maturity`
  - worked example / preliminary work / literature-grounded proposal / open research avenue / implementation barrier
- `evaluation_need`
  - benchmark with ground truth / qualitative expert review / case study / robustness test / formal proof / runtime monitoring / human-centred evaluation

### 历史草稿（已迁移，不作事实真源）：旧第 6.2 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

- `FM_usability_concern`
  - formal language difficulty
  - limited modularity / long specifications
  - counterexample interpretability
  - tool diversity and translation burden
  - state-space explosion
  - artefact traceability and evolution
  - domain expert accessibility
- `LLM_output_concern`
  - correctness / hallucination
  - ambiguity and incompleteness
  - logical coherence
  - mathematical reasoning
  - prompt ambiguity / prompt architecture consistency
  - domain grounding and world model gap
  - output consistency under prompt perturbation
  - predictability / repeatability
  - overreliance by analysts
- `process_concern`
  - LLM-FM expert collaboration
  - empirical evaluation difficulty
  - absence of single ground truth
  - human role and creativity
  - artefact proliferation
  - deployment and organisational adoption
  - scalability and computational cost
  - technological evolution / model drift / tool drift

### 历史草稿（已迁移，不作事实真源）：旧第 6.3 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

- `trustworthiness_target`
  - generated requirements
  - generated formal artefacts
  - generated code / tests / models
  - LLM agent orchestration
  - LLM component in mission-critical system
  - runtime regulatory behaviour
  - ethical/fairness-sensitive artefacts
- `trustworthiness_property`
  - correctness
  - fairness
  - trustworthiness / reliability
  - explainability / justification
  - robustness to prompt perturbation
  - out-of-distribution robustness
  - privacy / security
  - regulatory compliance
  - machine ethics
- `assurance_mechanism`
  - formal requirements and properties
  - formal verification of associated SW artefacts
  - formal argumentation constraints
  - formal prompts and pre/post-conditions
  - formal ontologies / knowledge graphs
  - abstract interpretation / abstraction of neural behaviour
  - runtime verification / monitoring
  - formalised ethical requirements
- `human_gate`
  - ambiguity clarification
  - expert review of non-unique outputs
  - quality-control checklist
  - challenge of hallucination patterns
  - final acceptance / downgrade / rejection
- `evidence_strength`
  - formal proof / verification result
  - executable counterexample
  - expert qualitative evaluation
  - worked example only
  - author opinion / future work

## 7. 对 Paper2 的启发与风险

### 7.1 启发

1. **支持“concern-first finding heuristic”**：候选发现不应只是“某类工具很多”，而应表达为“某类 task / artefact 存在某 concern，某类 mechanism 可部分缓解，但仍需要某类 evidence / human gate”。
2. **支持双向路线图叙事**：Paper2 的 agentic SLR 不仅是“LLM/agent 支持综述”，还应有“审计制品、研究者门控和证据链约束 LLM/agent”的反向控制线。这与本文 two-way roadmap 结构高度一致。
3. **支持把 trustworthiness 拆为字段**：correctness、fairness、explainability、robustness、compliance、ethics 等应成为候选 concern，而不是笼统写“可信”。
4. **支持 action-point 级抽取**：roadmap 文不提供统计分母，但每个 action point 都可成为模式先验；Paper2 可把 action point 抽成可审计字段，而非直接当 finding。
5. **支持“formal / structured artefact 作为审计接口”**：formal prompts、pre/post-conditions、ontology、argumentation、runtime monitor 等提醒 Paper2：智能体工作流的提示词、字段表、证据表、质疑日志都应结构化，不能只保存在自然语言对话里。
6. **支持非唯一答案的评价设计**：作者明确指出 formal specification / code 转换常没有唯一正确答案，需要 qualitative evaluation。这对 Paper2 的人工裁决、质疑日志和降级机制非常重要。
7. **贴近 project_1 / Paper2 交叉点**：状态机、Timed Automata、model checking、UPPAAL、formal artefact explanation、Req2Model / Req2Logic 都可作为后续 LLM4STM / LLM4Modeling mini-case 的维度种子。

### 7.2 风险

1. **roadmap 文不能混入 SLR/SMS 统计池**：它没有系统检索与纳排，不能支撑“领域中多数研究如何”的统计观察。
2. **action point 不是 empirical finding**：只能作为候选启发式或 模式种子，不能作为目标领域最终发现。
3. **示例带有演示性质**：sender-receiver 和 red-crossing 示例有助于讲清思路，但不能代表复杂工业系统；ChatGPT 3.5 输出还经过人工压缩和少量调整。
4. **“formal methods provide guarantees”有前提**：formalisation 必须正确、property 必须覆盖真实需求、抽象必须保守、工具链必须可信；否则 formal verification 只能验证错误模型或不完整 property。
5. **过度形式化风险**：Paper2 若照搬 FM 叙事，可能把 agentic SLR 写成重形式化系统，增加实现负担；应只迁移“结构化审计与 concern field”，不迁移全部 formal verification 承诺。
6. **人类角色不能被弱化**：原文 Fig. 2 / Fig. 4 有意省略 human actors，但 Section 7 反而强调 requirements engineers 的核心性。Paper2 必须坚持 G0--G5 研究者门控，避免被误读为自动化替代专家。
7. **模型/工具漂移**：本文示例基于 2024 年前后的技术状态；Paper2 若引用具体 LLM 能力，应避免写成稳定事实，应记录 model version、调用时间和可复核输出。

## 历史草稿（已迁移，不作事实真源）：旧第 8 节迁移来源

> 本节为 PR-A1-DT 前的历史草稿 / 迁移来源，不再作为事实真源；正式维度树、叶子取值空间、证据强度、统计池资格与候选发现用途，以[维度树复原](#维度树复原)和文末 A.1--A.4 审计附录为准。

- 当前 `survey_of_surveys` 六类 pattern 可容纳本条，但不足以表达 roadmap 文的核心贡献。建议后续 A2a 若继续纳入 vision / roadmap 文，新增或复用以下字段：
  - `review_type = vision/roadmap`
  - `evidence_role = boundary_anchor / schema_seed / concern_taxonomy_seed`
  - `roadmap_direction`
  - `action_point`
  - `concern_taxonomy`
  - `trustworthiness_property`
  - `assurance_mechanism`
  - `eligible_for_statistical_synthesis = false`
- 本轮不回修 [../../patterns/pattern-field-schema.md](../../patterns/pattern-field-schema.md)，因为用户只允许编辑本 `review.md`；以上先作为单篇 schema 历史观察记录。

## 9. 待复核

1. 若后续要在正文引用 Fig. 2 / Fig. 4，建议补页码与图中各元素的正式英文 label，并确认图中 “formal / conventional / LLM layer” 与 “formal / SW artefact / LLM layer” 的命名。
2. 若后续要引用 CCF 字段，建议提交前再次核验当轮 CCF 官方目录；本轮沿用本仓库 ccf_venues 缓存记录 IST 为 B 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
3. Section 5 的 ChatGPT 3.5 输出经过作者“slightly adjusted”；若用于论证 LLM 能力，应只作为 illustrative evidence，不作为可重复实验。
4. 需要决定 A2a 是否正式支持 `vision/roadmap` 类型；若支持，应同步更新 `SUMMARY.md` 和 `pattern-field-schema.md`，并明确不纳入 SLR/SMS 统计池。
5. 若用于 project_1 状态机建模，应进一步深读作者引用的 model generation、nl2spec、Natural2CTL、formal tool usability、formal methods diversity 文献，形成单独相关工作链。

## 维度树复原

### 一句话结论

本文的维度树主类型为“roadmap / concern / action-point 树”，辅助类型为“trustworthiness 边界树”。不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 [clm-formal-re-llm-roadmap-tree-type]

旧有“可迁移字段树 / 字段树 / schema 历史观察”等内容已迁移至维度树复原；后续以本节和审计附录为事实真源。

**A1-DT 叶子层口径校准**：下方“叶子维度表”的六个 `leaf-*` 是跨论文通用接口层，用来统一检查范围、语料、分类、方法、证据和候选发现六类信息；它不是对原文全部抽取字段、分类项或报告叶子的完成复原。本文原文模式的候选叶子已在“原文模式候选叶子映射（A1 种子）”中逐条列出，当前均只作为 `schema_seed` / `not_verified`，A2a 必须回到原文页码、表格、图和附录精核后才能升级为正式统计字段。 [clm-formal-re-llm-roadmap-source-schema-candidates]

### 根问题 / RQ 到主干分支映射

| 节点标识 | 对应问题或贡献声明 | 单位对象 | 主干分支 | 证据引用 | 说明 |
|---|---|---|---|---|---|
| [dim-formal-re-llm-roadmap-root] | Formal requirements engineering and large language models 的研究目标 / RQ / 贡献声明 | roadmap action / guideline item / schema seed | [dim-formal-re-llm-roadmap-b1] roadmap direction；[dim-formal-re-llm-roadmap-b2] layer；[dim-formal-re-llm-roadmap-b3] task family；[dim-formal-re-llm-roadmap-b4] assurance concern；[dim-formal-re-llm-roadmap-b5] human gate / limitation | [ev-formal-re-llm-roadmap-root] | 根节点只复原本文内部 schema，不直接生成 Paper2 目标领域结论。 |

### 维度树结构

```text
[dim-formal-re-llm-roadmap-root] Formal requirements engineering and large language models
├── [dim-formal-re-llm-roadmap-b1] roadmap direction
│   └── [leaf-formal-re-llm-roadmap-scope] 研究范围与单位对象
├── [dim-formal-re-llm-roadmap-b2] layer
│   └── [leaf-formal-re-llm-roadmap-corpus] 语料与纳排链条
├── [dim-formal-re-llm-roadmap-b3] task family
│   └── [leaf-formal-re-llm-roadmap-taxonomy] 主题与维度分类
├── [dim-formal-re-llm-roadmap-b4] assurance concern
│   └── [leaf-formal-re-llm-roadmap-method] 方法 / 技术 / 干预分类
└── [dim-formal-re-llm-roadmap-b5] human gate / limitation
    └── [leaf-formal-re-llm-roadmap-evidence] 评价、证据与复现资产
    └── [leaf-formal-re-llm-roadmap-finding] 统计观察与候选发现
```

### 叶子维度表

| 节点或叶子标识 | 名称 | 父节点 | 定义 | 取值空间 | 证据要求 | 缺失值语义 | 统计用途 | 候选发现用途 | 迁移边界 | 结论引用 |
|---|---|---|---|---|---|---|---|---|---|---|
| [leaf-formal-re-llm-roadmap-scope] | 研究范围与单位对象 | [dim-formal-re-llm-roadmap-b1] | 定义 formal RE + LLM 的综述范围、单位对象和 RQ / 贡献声明。 | 自由文本加 RQ / 贡献声明引用；单位对象可为 paper / study / method / artifact / action point。 | 全文目标、RQ、摘要或贡献声明。 | 无显式 RQ 时使用贡献声明并标注替代依据。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“研究范围与单位对象”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-scope] |
| [leaf-formal-re-llm-roadmap-corpus] | 语料与纳排链条 | [dim-formal-re-llm-roadmap-b2] | 记录数据库、检索式、时间窗、纳排、全文状态、质量门槛或 proposal 降级理由。 | 完整 SLR/SMS 为数值链条；guideline / roadmap 写 not_applicable 并说明。 | 方法章节、protocol、search / selection 描述或降级声明。 | roadmap / guideline 无统计分母时写 not_applicable。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“语料与纳排链条”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-corpus] |
| [leaf-formal-re-llm-roadmap-taxonomy] | 主题与维度分类 | [dim-formal-re-llm-roadmap-b3] | 复原原文中的 taxonomy、classification schema、coding scheme、roadmap branch 或 theory construct。 | 完整枚举 / 层级枚举 / 自由文本加理由。 | 抽取表、分类表、主题表、roadmap 图或结果小节。 | 分类项不完整时写待核验。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“主题与维度分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-taxonomy] |
| [leaf-formal-re-llm-roadmap-method] | 方法 / 技术 / 干预分类 | [dim-formal-re-llm-roadmap-b4] | 记录方法、工具、LLM / agent 角色、人工角色、流程阶段或干预方式。 | 层级枚举、关系值或开放 action point。 | 结果表、方法小节、roadmap action point 或工具 / 技术表。 | 无方法对象时写不适用。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“方法 / 技术 / 干预分类”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-method] |
| [leaf-formal-re-llm-roadmap-evidence] | 评价、证据与复现资产 | [dim-formal-re-llm-roadmap-b5] | 记录评价指标、数据、artifact、replication package、质量评价、threat 或开放材料。 | 布尔、数值、链接状态、质量等级或自由文本。 | 评价章节、质量评价表、artifact / data availability、threats。 | 只作作者愿景时降级为 candidate / risk。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“评价、证据与复现资产”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-evidence] |
| [leaf-formal-re-llm-roadmap-finding] | 统计观察与候选发现 | [dim-formal-re-llm-roadmap-b5] | 说明字段如何支撑统计观察、gap、recommendation、roadmap action 或候选发现。 | 统计用途、候选发现、boundary anchor、risk_only。 | 结果、discussion、conclusion、limitations。 | 不得直接写成 final research finding。 | 不进入主统计池；只作 schema seed / boundary anchor。 | 可生成与“统计观察与候选发现”相关的候选发现，需研究者裁决。 | 迁移结构与证据要求，不迁移领域结论。 | [clm-formal-re-llm-roadmap-leaf-finding] |

### 原文模式候选叶子映射（A1 种子）

本表把原文中已经出现的抽取字段、分类项、模型节点或报告叶子先作为 A1 候选种子列出，用来避免把上表六个通用接口误读为原文叶子全集。由于本 PR 仍未完成逐页表图精核，本表所有候选叶子默认 `not_verified`，只能作为 A2a 精核任务入口。

| 候选叶子标识 | 所属主干节点 | 原文模式来源 | 候选取值空间 | 当前用途 | 证据引用 | A2a 精核任务 |
|---|---|---|---|---|---|---|
| [leaf-formal-re-llm-roadmap-orig-roadmap-direction] | [dim-formal-re-llm-roadmap-root] | 路线图方向 | formal RE 与 LLM 双向结合的方向、层次和目标。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-formal-re-llm-roadmap-002, EV-formal-re-llm-roadmap-003 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-formal-re-llm-roadmap-orig-task-family] | [dim-formal-re-llm-roadmap-b3] | 任务族 | 需求抽取、形式化、分析、验证、追踪、修复等 formal RE 任务族。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-formal-re-llm-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-formal-re-llm-roadmap-orig-assurance-concern] | [dim-formal-re-llm-roadmap-b4] | 可信性 / 保证关注点 | 正确性、可解释性、验证、审计、人类确认和安全边界。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-formal-re-llm-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |
| [leaf-formal-re-llm-roadmap-orig-human-gate] | [dim-formal-re-llm-roadmap-b5] | 人类裁决点 | 研究者 / 工程师需要批准、质疑或复核的 gate。 | `schema_seed`；不得进入当前 SUMMARY 定量统计 | EV-formal-re-llm-roadmap-002 | 核对原文页码、表号 / 图号、附录或复现实验包；确认取值空间是否封闭、是否可统计以及缺失值语义。 |

### 原文 schema 主树（19×3 审计后返修）

本节根据 19×3 全文审计结果补充，是当前单篇 `review.md` 中更接近原文的 schema 主事实源。上方六个通用 leaf 仅保留为跨论文接口投影；本节才描述原文 RQ、抽取表、分类 schema、编码方案、统计表、roadmap / guideline stage 与 finding path 的具体结构。所有节点在本 PR 仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计或 final research finding。

审计入口：[codex](../../audits/a1dt-19x3/results/formal-re-llm-roadmap__codex.md)、[claude](../../audits/a1dt-19x3/results/formal-re-llm-roadmap__claude.md)、[deepseek](../../audits/a1dt-19x3/results/formal-re-llm-roadmap__deepseek.md)。 [clm-formal-re-llm-roadmap-a1dt-19x3-repair]

| 原文主干标识 | 原文主干名称 | 叶子 / 取值空间种子 | 统计用途与分母 | 缺失值语义 | 证据与 A2a 精核任务 |
|---|---|---|---|---|---|
| [dim-formal-re-llm-roadmap-orig-direction-a] | Roadmap A：LLM 支持形式化需求工程 | 需求形式化、建模、分析、验证、traceability、repair 等任务族和 action point | roadmap action seed；不进入统计池 | 作者愿景与已有证据分开 | 核对 Roadmap A 小节和图 |
| [dim-formal-re-llm-roadmap-orig-direction-b] | Roadmap B：形式化方法增强 LLM | 正确性保障、验证、解释、约束、运行时监控、可信评估等 action point | assurance schema seed | 非实证效果不得统计 | 核对 Roadmap B 小节和图 |
| [dim-formal-re-llm-roadmap-orig-llm-mechanism] | LLM 机制族 | 词袋/tf-idf、embedding、BERT 家族、GPT/Llama/Mixtral/Gemini、prompt、RAG、LoRA、distillation、agent | 技术背景分类 seed | 仅作为 roadmap 上下文 | 核对 LLM 技术背景章节 |
| [dim-formal-re-llm-roadmap-orig-formal-re-task] | 形式化 RE 任务与工件 | 需求文本、形式规约、模型检查、trace、repair、verification artifact | 与 Paper1/Paper2 主题相关的领域边界 seed | 不能外推为实验证据 | 核对 formal RE 章节 |
| [dim-formal-re-llm-roadmap-orig-trustworthiness] | 可信与实践关注 | 正确性、可解释性、human gate、tool integration、data quality、safety-critical boundary | candidate heuristic | 需研究者裁决 | 核对 trustworthiness / practical consideration |
| [dim-formal-re-llm-roadmap-orig-evidence-boundary] | 双向路线图边界 | 非系统检索、愿景/roadmap、引用案例、未来行动 | 统计池排除理由 | 无分母写 not_applicable | 核对 conclusion 和 limitations |

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
| 研究范围与单位对象 | `Roadmap A: LLM for formal RE` 及根问题 / RQ。 | 只记录 scope，不代表完整原文 schema。 |
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
| [dim-formal-re-llm-roadmap-root] | 树型分布与 schema seed 分布 | 当前 19 篇 survey-of-surveys 样本 | 否 | 识别可迁移的维度模式类型 | 不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 |
| [leaf-formal-re-llm-roadmap-taxonomy] | 分类项频次 / 交叉表 / 主题分布 | not_applicable | 否 | 形成主题覆盖、缺口或 roadmap action 的候选发现 | 需要 A2a 扩库验证取值空间是否饱和。 |
| [leaf-formal-re-llm-roadmap-finding] | 候选发现台账，不直接作为 final finding | discussion / conclusion / roadmap action | 否 | 支撑 candidate finding、risk 或 boundary anchor | final research finding 必须由研究者裁决。 |

### 可迁移与不可迁移边界

| 对象标识 | 可迁移内容 | 不可迁移内容 | 外推限制 | 结论引用 |
|---|---|---|---|---|
| [dim-formal-re-llm-roadmap-root] | 树型、叶子字段、证据要求、缺失值语义和降级规则。 | formal RE + LLM 的具体领域结论、统计结论或作者立场。 | 当前仅基于本文全文文本级审计；复杂图表和 supplementary 仍需 A2a 精核。 | [clm-formal-re-llm-roadmap-transfer] |
| [leaf-formal-re-llm-roadmap-finding] | “统计观察 / discussion → 候选发现 → 研究者裁决”的链路。 | 未经反证检查的 final research finding。 | 不得从单篇论文直接外推到 Paper2 目标主题。 | [clm-formal-re-llm-roadmap-finding-boundary] |

## 审计附录：证据链与结论-证据映射

### A.1 论文与本地文件来源

| 来源标识 | 文件或链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| [src-formal-re-llm-roadmap-pdf] | [paper.pdf](./paper.pdf) | paper_pdf | 原文版面、图表、页码和表格人工核验 | local_verified | 本轮以文本审计为主，复杂图表留待 A2a 复核。 |
| [src-formal-re-llm-roadmap-text] | [paper_content.txt](./paper_content.txt) | paper_text | 维度树、证据账本和结论映射的主要正文来源 | local_verified | 由仓库 PDF 提取工具生成。 |
| [src-formal-re-llm-roadmap-bib] | [bibtex.bib](./bibtex.bib) | publisher_page | 标题、作者、年份、DOI / venue 元信息 | local_verified | 与 [metadata.json](./metadata.json) 交叉核对。 |

### A.2 维度树证据账本

| 证据标识 | 引用键 | 来源标识 | 来源文件 | 原文页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要原文版面核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EV-formal-re-llm-roadmap-001 | [ev-formal-re-llm-roadmap-root] | [src-formal-re-llm-roadmap-text], [src-formal-re-llm-roadmap-bib] | paper_content.txt, bibtex.bib | 摘要 / 引言页；待 A2a 精确页码复核 | 摘要、引言或研究目标 | 目标 / RQ / contribution 邻近段落 | -- | 见释义 | 原文题名、摘要和研究目标支撑根问题、综述类型和单位对象。 | rq | not_verified | [dim-formal-re-llm-roadmap-root] | false | false | -- | 只支撑本文内部维度树根节点。 |
| EV-formal-re-llm-roadmap-002 | [ev-formal-re-llm-roadmap-taxonomy] | [src-formal-re-llm-roadmap-text] | paper_content.txt | 方法 / 结果页；待 A2a 精确页码复核 | 方法、数据抽取、分类或 roadmap 章节 | extraction / taxonomy / action point 邻近段落 | 表 / 图 / 清单待核验 | 见释义 | 原文中的抽取字段、分类 schema、coding scheme、roadmap branch 或 guideline item 支撑主干分支和叶子维度；本行在 A1-DT 仅作维度树 seed，待 A2a 精确页码 / 表图核验后才能升级为可统计证据。 | taxonomy | not_verified | [dim-formal-re-llm-roadmap-b1], [dim-formal-re-llm-roadmap-b2], [dim-formal-re-llm-roadmap-b3], [dim-formal-re-llm-roadmap-b4], [dim-formal-re-llm-roadmap-b5], [leaf-formal-re-llm-roadmap-taxonomy], [leaf-formal-re-llm-roadmap-method] | true | false | -- | 当前取值空间是 A1 seed，A2a 扩库前不得视为饱和。 |
| EV-formal-re-llm-roadmap-003 | [ev-formal-re-llm-roadmap-stat] | [src-formal-re-llm-roadmap-text] | paper_content.txt | 结果 / 讨论页；待 A2a 精确页码复核 | Results、Discussion、Conclusion 或 Limitations | 统计结果 / discussion / roadmap action 邻近段落 | 表 / 图待核验 | 见释义 | 原文结果、讨论、限制或路线图说明字段如何支撑统计观察、缺口、建议或边界判断；本行在 A1-DT 仅作 boundary / candidate seed，待 A2a 精确页码 / 表图核验后才能升级。 | author_claim | not_verified | [leaf-formal-re-llm-roadmap-evidence], [leaf-formal-re-llm-roadmap-finding], [leaf-formal-re-llm-roadmap-orig-roadmap-direction], [leaf-formal-re-llm-roadmap-orig-task-family], [leaf-formal-re-llm-roadmap-orig-assurance-concern], [leaf-formal-re-llm-roadmap-orig-human-gate] | true | false | -- | 仅当系统性证据和分母明确时才可进入统计；roadmap / proposal 仅作启发。 |
| EV-formal-re-llm-roadmap-004 | [ev-formal-re-llm-roadmap-risk] | [src-formal-re-llm-roadmap-text] | paper_content.txt | threats / limitations 页；待 A2a 精确页码复核 | Threats、Limitations、Practical considerations 或 Conclusion | 风险 / 限制邻近段落 | -- | 见释义 | 原文威胁、局限、实践考虑或非系统性边界支撑迁移边界和降级判断。 | limitation | not_verified | [dim-formal-re-llm-roadmap-root], [leaf-formal-re-llm-roadmap-finding] | false | false | -- | 只支撑可迁移边界，不支撑强领域结论。 |


### A.3 结论-证据映射

| 引用键 | 结论标识 | 结论内容 | 结论类型 | 支撑对象标识 | 支撑证据标识列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| [clm-formal-re-llm-roadmap-tree-type] | A1DT-formal-re-llm-roadmap-C01 | 本文的维度树主类型为“roadmap / concern / action-point 树”，辅助类型为“trustworthiness 边界树”。不进入主统计池：vision/roadmap；没有系统检索、纳排、质量评价或数据综合；仅作 boundary_anchor。 [clm-formal-re-llm-roadmap-tree-type] | tree_type | [dim-formal-re-llm-roadmap-root] | EV-formal-re-llm-roadmap-001, EV-formal-re-llm-roadmap-004 | 树型判断仅限本文，不代表所有 formal RE + LLM 综述。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-scope] | A1DT-formal-re-llm-roadmap-C02 | 叶子维度“研究范围与单位对象”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-scope] | EV-formal-re-llm-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-corpus] | A1DT-formal-re-llm-roadmap-C03 | 叶子维度“语料与纳排链条”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-corpus] | EV-formal-re-llm-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-taxonomy] | A1DT-formal-re-llm-roadmap-C04 | 叶子维度“主题与维度分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-taxonomy] | EV-formal-re-llm-roadmap-002 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-method] | A1DT-formal-re-llm-roadmap-C05 | 叶子维度“方法 / 技术 / 干预分类”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-method] | EV-formal-re-llm-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-evidence] | A1DT-formal-re-llm-roadmap-C06 | 叶子维度“评价、证据与复现资产”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-evidence] | EV-formal-re-llm-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-leaf-finding] | A1DT-formal-re-llm-roadmap-C07 | 叶子维度“统计观察与候选发现”来自本文的 RQ / 方法 / 分类 / 评价 / 讨论结构，可作为 Paper2 维度树候选节点。 | leaf_definition | [leaf-formal-re-llm-roadmap-finding] | EV-formal-re-llm-roadmap-003 | 只限本文证据范围；取值空间在 A2a 扩库前不得视为饱和。 | weak | boundary_anchor | false | -- |
| [clm-formal-re-llm-roadmap-transfer] | A1DT-formal-re-llm-roadmap-C08 | 本文可迁移的是维度树结构、证据要求和降级纪律，不可迁移具体领域统计结论。 | migration_boundary | [dim-formal-re-llm-roadmap-root] | EV-formal-re-llm-roadmap-002, EV-formal-re-llm-roadmap-004 | 复杂表图和 supplementary 仍需 A2a 精核。 | weak | schema_seed | false | -- |
| [clm-formal-re-llm-roadmap-finding-boundary] | A1DT-formal-re-llm-roadmap-C09 | 本文可为候选发现提供启发，但 final research finding 必须经过跨论文证据、反证与研究者裁决。 | candidate_finding | [leaf-formal-re-llm-roadmap-finding] | EV-formal-re-llm-roadmap-003, EV-formal-re-llm-roadmap-004 | 单篇 discussion、roadmap 或统计观察不能直接升级为最终发现。 | weak | candidate_finding | false | -- |

| [clm-formal-re-llm-roadmap-source-schema-candidates] | A1DT-formal-re-llm-roadmap-C12 | 本文已把原文抽取字段、分类项、模型节点或报告叶子列为“原文模式候选叶子映射（A1 种子）”；这些候选叶子只表示 A2a 精核入口，不代表 A1-DT 已完成原文叶子全集复原或可统计字段冻结。 | source_schema_candidate | [leaf-formal-re-llm-roadmap-orig-roadmap-direction], [leaf-formal-re-llm-roadmap-orig-task-family], [leaf-formal-re-llm-roadmap-orig-assurance-concern], [leaf-formal-re-llm-roadmap-orig-human-gate] | EV-formal-re-llm-roadmap-002, EV-formal-re-llm-roadmap-003 | 当前候选叶子仍需原文页码、表图、附录和取值空间复核。 | weak | schema_seed | false | -- |
| [clm-formal-re-llm-roadmap-a1dt-19x3-repair] | A1DT-formal-re-llm-roadmap-C13 | 19×3 全文审计表明本文必须以“原文 schema 主树”作为维度树事实源；通用六叶接口只能作为跨论文投影。本轮已补原文主干和 A2a 精核入口，但全部仍为 `schema_seed`，不得进入当前 SUMMARY 定量统计。 | audit_repair | [dim-formal-re-llm-roadmap-root] | EV-formal-re-llm-roadmap-002, EV-formal-re-llm-roadmap-003 | 原文主树仍需 A2a 页码 / 表图 / 附录精核；若审计意见与原文冲突，以原文为准。 | weak | schema_seed | false | -- |

### A.4 本地复验命令与人工核验清单

| 检查标识 | 复验对象 | 命令或人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| [cmd-formal-re-llm-roadmap-structure-check] | [dim-formal-re-llm-roadmap-root], A1DT-formal-re-llm-roadmap-C01 | 运行 PR-A1-DT 结构检查脚本，确认维度树、A.1--A.4、A.2→A.1、A.3→A.2 回链存在。 | 脚本通过且无缺失表头 / 断链 / 弱证据误入统计。 | passed |
| [cmd-formal-re-llm-roadmap-visual-check] | EV-formal-re-llm-roadmap-002, EV-formal-re-llm-roadmap-003 | 人工打开 `paper.pdf` 核对相关表格、图、统计页和 action point 与 A.2 释义一致。 | 表 / 图编号、页码、字段名和结论一致；若不一致则降级证据强度。 | needs_manual_check |
