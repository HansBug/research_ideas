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

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实真源。它替代旧版 `review.md` 中的“六个通用 leaf / A1-M0--M6 投影”主树写法；A1-M0--M6 只能作为跨论文投影层，不能反向冒充本文原生 schema。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__codex.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__codex.md)、[../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__claude.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__claude.md)、[../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__deepseek.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。下方若出现“旧版 `review.md` 需要返修 / needs repair”等表述，均指 A1-DT v2 返工前的旧版状态；本节已经按该返修意见重写，最终剩余风险统一归入 A2a 的页码、表图和 supplementary 精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `formal-re-llm-roadmap` |
| agent | `claude` |
| 是否已读 `paper_content.txt` | 是；全 2517 行分两批读取（1–939、940–1840、1840–2517 引用列表），结合 paper 末段三遍核验 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；都已读取，确认期刊为 Information and Software Technology 181:107697 (2025)，DOI `10.1016/j.infsof.2025.107697` |
| 是否打开或核对 `paper.pdf` | 否，本轮**未做 PDF 版面核验**；以 `paper_content.txt` 文本为准，Fig. 2、Fig. 4 仅以文本中“Fig. 2/Fig. 4 summarises and connects…”段落定位；版面级（页码、图层标签位置、表格排版）需 A2a 回 PDF 复核 |
| 原文类型 | **vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） |
| 被编码样本单位 | **无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations |
| 样本数量 / 分母 | 不存在系统样本分母；roadmap action 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** |
| 原生树类型 | **降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 |
| 主统计池资格 | **否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 |
| 总体判定 | **v2 已返修完成**：原始审计对旧版 `review.md` 的判定为 needs repair；本节已按该意见重写为原生样本编码树 / 维度森林，剩余页码、表图、supplementary 风险进入 A2a。 |

### 1. 原文证据阅读说明

- **实读文件**：`bibtex.bib`、`metadata.json`、`paper_content.txt`（全 2517 行三段读完）、`review.md`（全 480 行两段读完）。`paper.pdf` 本轮未打开（属本审计的 transparency 项，需 A2a 复核排版级证据）。
- **技能文件**：均已读取：`ai-research-writing-skill/SKILL.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`、`research-planning/SKILL.md`、`planning-prompts.md`、`output-schemas.md`、`autoresearch/SKILL.md`。所用核心原则：claim-evidence gate、reviewer 5-dim、5-dim 自评、reviewer constructive specificity、autoresearch validator-gated 边界判定。
- **覆盖章节**：Abstract、§1 Introduction、§2 Background (含 §2.1 LMs/LLMs in RE、§2.2 Formal RE)、§3 Example A (PROMELA)、§4 Roadmap A、§5 Example B (ChatGPT)、§6 Roadmap B、§7 Practical considerations、§8 Conclusion、CRediT、Data availability、References（175 条）。

#### 关键证据锚点（约 10 条）

| 序号 | 证据位置 | 原文短引 / 释义 | 用途 |
|---|---|---|---|
| E1 | Page 2 §1 contributions 段 | “It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence but rather to indicate possible avenues of research… the discussed roadmaps should not be considered exhaustive.” | 决定论文类型 = vision/roadmap；不进主统计池 |
| E2 | Page 8 §4 引言段 + Fig. 2 描述 | “Each discussion topic is associated with a circled number… Fig. 2 summarises and connects the different discussion topics” + 标注 ①~⑤ | 锁定 Roadmap A 由 5 个 action points 组成 |
| E3 | Page 8–11 §4 各 Action Point | 五个标号 Action Point: Generating FM/SE Artifacts; Explaining FM Artifacts; Translating Formal Languages; Supporting Iterations and Evolution; Automating Knowledge Engineering | Roadmap A action point 名单 |
| E4 | Page 14 §6 引言段 + Fig. 4 描述 | “Each discussion item is associated with a circled number, which appears in the figure” + ①~⑦ | 锁定 Roadmap B 由 7 个 action points 组成 |
| E5 | Page 14–16 §6 各 Action Point | 七个标号 Action Point: Ensuring Correctness… Argumentation; Improving Mathematical Reasoning…; Formal Prompt Engineering; Formal Domain Knowledge…; Ensure LLM Output Consistency…; Regulatory Compliance at Runtime; Mitigate Bias… Ethical Concerns | Roadmap B action point 名单 |
| E6 | §4 Summary（Fig. 2 描述） | "structured into three interconnected layers… a formal development layer, a conventional development layer and an LLM layer” | Roadmap A 三 layer 结构 |
| E7 | §6 Summary（Fig. 4 描述） | "structured into three layers, a formal layer, a software (SW) artefact layer and a LLM layer” | Roadmap B 三 layer 结构 |
| E8 | §7 段落标题序列 | "Collaboration… / Empirical Evaluation / Overreliance on LLM Output / Diminishing Role of Human Creativity / Limited Training on FM datasets / Proliferation and Maintainability of Artefacts / Deployment, Scalability and Technological Evolution" | Section 7 的 7 类 practical consideration 边界森林 |
| E9 | §6 行内说明 §6 type-of-task | LLM Layer 任务被作者显式二分为：“(i) analytic tasks… (ii) generative tasks” | Roadmap B 内部任务分类（analytic vs generative） |
| E10 | §8 Conclusion + Data availability | “No data was used for the research described in the article.” + 作者自述未来工作 3 项 | 锁定无样本数据；roadmap 不是 evidence base |
| E11 | §2.2 formal models 段 | LTS/FSM/Büchi Automata / Timed Automata / Probabilistic & Stochastic SM / Statecharts / Hierarchical SM / Petri Nets 子分类 | Background 内置的描述性 taxonomy（不是抽取 schema，仅供 LLM4STM 主题边界参考） |
| E12 | §5 段落标题序列 | Requirements Generation / User Feedback Analysis / Smell Detection / Completeness Check / Model Generation / Requirements Classification / Requirements Tracing / Code-related Tasks | Example B 演示的 LLM4RE task family（用例驱动，不是 systematic survey） |

### 2. 样本单位与字段来源判定

1. **原文纳入对象**：本文不“纳入”样本。它通过两个 worked example 揭示 FM 与 LLM 各自的局限，再以作者经验 + 引用 seminal works 的方式构造两个 roadmap。
2. **是否有系统检索 / 纳排 / 数据抽取 / 编码方案**：**没有**。无 search protocol、无 PRISMA、无 inclusion / exclusion criteria、无 quality appraisal、无 extraction form、无 coding scheme。
3. **字段来源**：所有结构化内容都来自**作者自身组织**：
   - Roadmap A / B 的“action point”是作者自定义的研究议程项。
   - Fig. 2 / Fig. 4 的“three layers”是作者用 Photoshop-layer 比喻定义的可视化层级（脚注 9：layers 应理解为 graphical layers）。
   - Section 7 的 7 个 practical consideration 是作者枚举的实践约束类别。
4. **RQ 与样本单位关系**：原文无显式 RQ 列表；隐含两个对称 question：(a) 如何用 LLM 提升 formal RE 的可用性？(b) 如何用 FM 提升 LLM-based RE 的 correctness/fairness/trustworthiness？这两个 RQ 直接对应两个 roadmap，**roadmap action point 就是 RQ 的结构化答案，而非用 RQ 编码出的样本**。
5. **降级处理**：作为 vision/roadmap，本文只能作 **boundary anchor + methodological seed + candidate heuristic**：
   - boundary anchor：证明 Paper2 的脚手架需要容纳非 SLR/SMS 文献，并显式 `eligible_for_statistical_synthesis=false`
   - methodological seed：双向 roadmap 结构、layer 分层、concern→mechanism→action 字段串
   - candidate heuristic：每个 action point 是一条 candidate finding，但需 Paper2 跨文献证据再次裁决

### 3. 原生样本编码维度树 / 维度森林

原生结构为**双根 roadmap 森林 + 边界森林**：

```text
[本文 native forest]
│
├── (Tree A) Roadmap A: Using LLMs to support FM-based development        [Fig.2]
│   ├── Layer-A1: Formal Development Layer
│   ├── Layer-A2: Conventional Development Layer
│   ├── Layer-A3: LLM Layer (LLM agents)
│   └── ActionPoints[5]
│       ├── AP-A1 Generating FM and SE Artifacts
│       │   ├── concern: state-space explosion / spec abstraction / NL ambiguity / limited FM training data
│       │   ├── mechanism: RAG / code-summarisation / nl2spec / Natural2CTL / interactive translation
│       │   ├── artifact_in: code / NL requirements
│       │   ├── artifact_out: formal spec / LTL formula / never-claim / assertion
│       │   └── refs: [113][114][115][118][119]
│       ├── AP-A2 Explaining FM Artifacts
│       │   ├── concern: explainability / counterexample interpretability / non-modular long specs
│       │   ├── mechanism: code-comment generation analogue [129] / localised illustration [130] / stack-trace explanation [132]
│       │   ├── target: model / formula / counterexample
│       │   └── refs: [120][121][122][123][124][125][126][127][128][129][130][131][132]
│       ├── AP-A3 Translating Formal Languages
│       │   ├── concern: tool diversity / FM diversity for soundness / different audiences
│       │   ├── mechanism: code-to-code translation [137]
│       │   └── refs: [127][133][134][135][136][137]
│       ├── AP-A4 Supporting Iterations and Evolution
│       │   ├── concern: trace-link maintenance / artefact alignment
│       │   ├── mechanism: code-specific LLM + NL-oriented LLM combo
│       │   └── refs: [6][138][139]
│       └── AP-A5 Automating Knowledge Engineering
│           ├── concern: domain knowledge extraction / ontology maintenance
│           ├── mechanism: ontology engineering with LLMs / knowledge graph
│           └── refs: [140][141][142]
│
├── (Tree B) Roadmap B: Using FMs to support LLM-based development        [Fig.4]
│   ├── Layer-B1: Formal Layer
│   ├── Layer-B2: SW Artifact Layer
│   ├── Layer-B3: LLM Layer
│   │     │   └── llm_task_kind: analytic | generative                      [E9]
│   └── ActionPoints[7]
│       ├── AP-B1 Ensuring Correctness through Formal Requirements & Argumentation
│       │     concern={hallucination, plausibility, novice over-trust, logical coherence}
│       │     mechanism={formal spec verification, formal argumentation [146][147], explanation-of-FM-artifact loopback}
│       ├── AP-B2 Improving Mathematical Reasoning with Formal LLMs
│       │     concern={weak math reasoning [151], CPS math requirements}
│       │     mechanism={math-specialised LLMs (Lemma [150], MathStral), RAG (LeanDojo [152]), multi-LLM agents, external calculator/reasoner}
│       ├── AP-B3 Formal Prompt Engineering
│       │     concern={prompt ambiguity → artifact defects, complex multi-prompt orchestration}
│       │     mechanism={ACSL [105]-style pre/post-conditions in prompts, UML-style prompt architecture, agent paradigm [30]}
│       ├── AP-B4 Formal Domain Knowledge and Explainability
│       │     concern={domain corpus scarcity, world-model gap [148][155]}
│       │     mechanism={formal ontology / knowledge graph injected via RAG, justification through KG}
│       ├── AP-B5 Ensure LLM Output Consistency through Formal Verification
│       │     concern={predictability / repeatability under prompt perturbation, safety-critical embedding}
│       │     mechanism={abstract interpretation of NN [159], abstraction methods for verification [160]}
│       ├── AP-B6 Regulatory Compliance at Runtime
│       │     concern={LLM evolution + law evolution → recurring compliance}
│       │     mechanism={runtime verification [163]}
│       └── AP-B7 Mitigate Bias and Address Ethical Concerns
│             concern={toxicity, stereotype, robustness, OOD, privacy, fairness, machine ethics [164]}
│             mechanism={formalised ethical requirements [166], formal validation of LLM-generated artefacts}
│
└── (Boundary Forest) §7 Practical Considerations & Limitations [E8]
    ├── PC-1 Collaboration Between LLM and FM Experts
    ├── PC-2 Empirical Evaluation (qualitative methods, no ground truth)
    ├── PC-3 Overreliance on LLM Output (human-centred QC, hallucinatory patterns)
    ├── PC-4 Diminishing Role of Human Creativity (RE engineer recentred)
    ├── PC-5 Limited Training on FM datasets (fine-tune / code-analogue / interactive)
    ├── PC-6 Proliferation and Maintainability of Artefacts (visualisation, analytics)
    └── PC-7 Deployment, Scalability and Technological Evolution
            (state-space explosion mitigations [174][175]; distillation [28]; tech evolution pace)
```

辅助：**§2 Background taxonomy**（与抽取无关，仅作描述性领域底图，可作 LLM4STM 边界种子）：

```text
[bg-tax] Background descriptive taxonomy
├── LLM history: BoW/tf-idf → word embeddings → BERT → LLM → prompting/RAG/LoRA/distillation → LLM agents
├── Formal RE
│   ├── Specification languages: Z, VDM, B-Method, CCS, CSP, SDL, CASL, LOTOS, TLA+, Alloy, FizzBee, ACE
│   ├── Property logics: LTL, CTL, CTL*, μ-calculus, HOL, Modal, MTL/RTTL, Probabilistic TL
│   ├── Formal models: LTS, FSM, Büchi, Timed Automata, Probabilistic/Stochastic SM, Statecharts, Hierarchical SM, Modelica SM, Ptolemy II SM, Petri Nets (Colored/Timed/Stochastic/Hierarchical)
│   └── Analysis methods: Abstract Interpretation, Semantic Static Analysis, Model Checking (Spin/NuSMV/UPPAAL), Proof Assistants (Coq/Isabelle/Agda), Deductive Verification (Frama-C/Dafny/KeY), Design by Refinement (Event-B/Rodin)
```

### 4. 叶子维度表

下表是把上述原生森林的每条 action point 拆出 **6 维子字段** 后的叶子表。这些子字段是作者实际在每个 action point 段落中写到的内容（concern / mechanism / artifact / refs / action recommendation），不是 reviewer 主观套模板。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-roadmap_direction | roadmap 方向 | 森林根 | §4/§6 章节自述 | 双向中的具体方向 | {LLM→FM, FM→LLM} | 完整枚举（闭） | 不允许缺失 | 不入统计池；二元 boundary 标签 | 用作 Paper2 双向叙事种子 | E2,E4 | 仅迁移“双向 roadmap”结构 |
| leaf-layer | 可视化层 | Roadmap A/B 内 | §4/§6 Summary 段、Fig.2/4 描述 | 作者定义的 graphical layer | A:{Formal Dev, Conventional Dev, LLM}; B:{Formal, SW Artifact, LLM} | 完整枚举（但 A/B 不同义） | n/a | 不入统计池 | 用作 layer-based 叙事框架 | E6,E7 | A、B 层数同为 3 但语义不同，不能直接合并 |
| leaf-action_point | 行动点 | layer 内 | §4/§6 ①~⑤ / ①~⑦ 段 | 作者标号的研究议程项 | A: 5 项已枚举；B: 7 项已枚举（见 §3 节树） | 完整枚举（封闭，但作者声明非穷尽） | 不允许缺失 | 不入统计池；可作 candidate-finding 计数（n=12） | 每条 = 一条 candidate finding 种子 | E3,E5 | 必须配 concern + mechanism；不可孤立迁移 |
| leaf-concern | 关注 / 痛点 | action_point | 段落内显式 concern 表述 | action point 想解决的问题 | 自由文本 + concern_taxonomy {explainability, hallucination, math reasoning, prompt ambiguity, domain grounding, output consistency, regulatory compliance, bias/ethics, FM data scarcity, state-space explosion, …} | 自由文本加 emergent 分类 | 缺失时标 not_stated | 不入统计池 | 作 Paper2 concern field 种子 | E3,E5,E8 | 部分 concern 在 §7 重述，注意去重 |
| leaf-mechanism | 机制 / 干预 | action_point | 段落内 mechanism 描述 | 应对 concern 的形式化或 LLM 机制 | 自由文本 + mechanism_taxonomy {RAG, fine-tuning, multi-agent, formal verification, abstract interpretation, runtime verification, ontology/KG, formal argumentation, controlled NL, ACSL-style pre/post, code-translation} | 层级枚举（emergent，不封闭） | 缺失时 not_stated | 不入统计池 | 作 mechanism field 种子 | E3,E5 | 机制粒度不一，A2a 需拆细 |
| leaf-artifact_in | 输入制品 | action_point | 段落内提及的输入对象 | LLM/FM 处理的对象 | {NL req, user story, feedback, issue, code, formal model, logic formula, counterexample, domain doc, regulation, ethics principle} | 完整枚举（emergent） | 缺失时 not_stated | 不入统计池 | 作 RE artifact 流图种子 | E3,E5 | 与 leaf-artifact_out 配对，构成 transformation 关系 |
| leaf-artifact_out | 输出制品 | action_point | 段落内提及的输出对象 | LLM/FM 生成的对象 | {formal spec, formal property, software model, code, trace link, classification, NL explanation, knowledge graph, verification result, runtime monitor, candidate req completion} | 完整枚举（emergent） | 缺失时 not_stated | 不入统计池 | 作 RE artifact 流图种子 | E3,E5 | 同上 |
| leaf-action_recommendation | 行动建议 | action_point | "Action Point:" 框 | 作者明文落款的研究建议 | 自由文本 | 自由文本（≈12 条） | 不允许缺失（每个 AP 必有一条） | 不入统计池 | 可作 candidate research action | E3,E5 | 不可直接外推为已验证发现 |
| leaf-supporting_refs | 支持文献 | action_point | 段内行内引用 | 作者所举 seminal / preliminary work | 引用列表（参考 §References） | 关系值（指向 BibTeX 编号） | 缺失允许 | 不入统计池 | 可作扩库候选种子（如 [115][118][119][152][159][160][163]） | E3,E5 | 引用 ≠ 系统综述，不能当 evidence base |
| leaf-evidence_strength | 证据强度 | action_point | reviewer 评估 | 该 AP 的支撑性质 | {formal_proof, executable_counterexample, expert_qualitative, worked_example_only, author_opinion} | 完整枚举 | -- | 不入统计池 | 用于 candidate-finding 降级 | E1,E10 | 全部应默认 ≤ worked_example_only / author_opinion |
| leaf-llm_task_kind | LLM 任务种类 | Roadmap B / Layer-B3 | §6 Fig.4 Summary 段 | 作者把 LLM-layer 任务二分 | {analytic, generative} | 完整枚举（闭） | n/a | 不入统计池 | 作 Paper2 LLM4RE 任务大类种子 | E9 | 仅适用 Roadmap B；不映射到 Roadmap A |
| leaf-practical_consideration | 实践约束类别 | Boundary Forest | §7 子标题 | 作者枚举的实施障碍 | {Collaboration, Empirical Eval, Overreliance, Human Creativity, FM Training Data, Proliferation, Deployment/Scalability/Tech Evol} | 完整枚举（n=7） | -- | 不入统计池 | 作 Paper2 risk-register 种子 | E8 | 与 leaf-concern 部分重叠，注意去重 |

> **重要边界**：现 `review.md` 主表中的 6 个 `leaf-formal-re-llm-roadmap-{scope,corpus,taxonomy,method,evidence,finding}` 是**跨论文通用接口投影**，不是原文叶子；它们正确的位置是后文 “通用接口投影” 小节，不应被当成主原生树。本审计上表 12 个叶子才是原文真实结构的最小复原层。

### 5. 关系边表

本文 schema 不是 entity–relation 型；但仍可识别出 **隐式关系边**，用于支撑 Paper2 的 RE artifact 流图：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel-ap_addresses_concern | action_point | addresses | concern | 多对多 | 缺失→ not_stated | E3,E5 | 反向检索：某 concern 由哪些 AP 覆盖 |
| rel-ap_proposes_mechanism | action_point | proposes | mechanism | 多对多 | 缺失→ not_stated | E3,E5 | 机制族归并 |
| rel-artifact_transformation | artifact_in | transformed_to | artifact_out | 多对多（由 mechanism 实现） | 缺失允许 | E3,E5 | RE artifact 流图 |
| rel-layer_contains_ap | layer | contains | action_point | 一对多 | n/a | E6,E7 | layer-AP 归属 |
| rel-direction_owns_layer | roadmap_direction | owns | layer | 一对多 | n/a | E2,E4 | 双向路线图区分 |
| rel-ap_supported_by_ref | action_point | supported_by | bibref | 多对多 | 缺失允许 | E3,E5 | 扩库 seed |
| rel-pc_constrains_roadmap | practical_consideration | constrains | roadmap (A 或 B) | 多对多 | n/a | E8 | 边界森林对正树的反向约束 |

未发现：原文未给出形式化的 ER schema、UML class model 或 OWL 关系；上述关系边均为 reviewer 从段落中归纳，**非作者显式声明**，A2a 复核时需在每条边上标注 `inferred_by_reviewer=true`。

### 6. 统计观察、候选 finding 与 final finding 边界

#### 6.1 由字段 / 统计表支持的统计观察
**无**。本文不含任何统计表、频次表、Q&A 表或 coding distribution。作者明确 "No data was used"（§Data availability）。

#### 6.2 作者 discussion / roadmap 提出的候选 finding（每条均为 candidate，evidence_strength ≤ worked_example_only）
- CF-1：LLM 的 code-summarisation 能力可被借用于 code→formal spec 抽象，以缓解 state-space explosion（AP-A1）。
- CF-2：counterexample 的解释难度类似 stack-trace，可借用 LLM 的 trace-explain 思路（AP-A2，引 [132]）。
- CF-3：FM diversity 可通过 LLM 驱动的 model-to-model translation 维持（AP-A3）。
- CF-4：trace-link 由 code-specific LLM + NL-oriented LLM 联合更可靠（AP-A4）。
- CF-5：LLM 的数学推理瓶颈未必能靠规模扩张解决，需要外挂 formal/calc 资源（AP-B2，引 [151]）。
- CF-6：prompt 即“需求”，应引入 ACSL-style pre/post-condition（AP-B3）。
- CF-7：abstract interpretation 在 NN/transformer 上的应用是缓解 LLM 不可重复性的可行路径（AP-B5）。
- CF-8：regulatory compliance 必须从一次性证明转为 runtime monitoring（AP-B6）。
- CF-9：ethical/fairness 必须先 formalise 为 requirement，再用 formal techniques 验证（AP-B7）。

#### 6.3 对 Paper2 可迁移的方法学启发
- 双向 roadmap 叙事（LLM 帮 X / X 帮 LLM）作为 Paper2 第二篇的结构 seed。
- “concern → mechanism → artifact → action” 字段串作为 candidate-finding 表的字段约束。
- "analytic vs generative" 二分（E9）可作 LLM4SLR 任务大类基础。
- §7 七项 practical consideration 作为 Paper2 risk register 的字段种子（特别 overreliance、empirical eval 难题、artifact proliferation 与 project_1 / Paper2 高度对应）。

#### 6.4 绝不可迁移的领域结论
- 任何“LLM + FM 能自动保证 correctness/fairness/trustworthiness”形式的强主张。
- 任何“UPPAAL/Spin/PROMELA 是 LLM4STM 最佳工具链”这类来自示例选择的工具偏好。
- ChatGPT 3.5 在 RE 任务上的具体能力描述（作者 explicitly "slightly adjusted" 输出）。
- §2 background taxonomy 不可作为 LLM4STM 主综述的工具/模型分类的事实源，只能作为术语启发。

### 7. 对旧版 `review.md` 的返修来源

按 C / I / M 分级，**严重性以学术目标 / Paper2 证据链可靠性为锚**：

#### C（critical）— 阻塞合并到 Paper2 主线

无。本文 review.md 已在最近一轮 PR-A1-DT v2 19×3 返修中正确判定 `eligible_for_statistical_synthesis=false` 与 `evidence_role=boundary_anchor`，不会污染主统计池。

#### I（important）— 影响 schema seed 质量、需在 A2a 前修

1. **I-1：维度树主表的“六叶通用接口”应明确降级到 `通用接口投影` 小节，主表换成 12 叶原文结构表**。当前 review.md §维度树复原 → 叶子维度表（行 351–360）仍把 scope/corpus/taxonomy/method/evidence/finding 摆成原生树叶子；这与 A1-DT v2 要求“单篇维度树必须像论文自己的 schema”冲突。建议替换为本审计 §4 的 12 叶表。
   - 学术影响：若后续 A2a 用该主表做 schema 抽取，会把所有 roadmap action point 压缩成 generic taxonomy 叶，丢失 12 个 action point + 双 layer 结构 + concern→mechanism 字段串，使 Paper2 的 candidate-finding heuristic 失去原文锚定。
2. **I-2：补齐“原文 schema 主树（19×3 审计后返修）”中 5 个原文主干，使其对齐到本文真实主干结构（2 roadmap × 3 layer × N action point + 1 boundary forest）**。当前那 6 个原文主干（direction-a/direction-b/llm-mechanism/formal-re-task/trustworthiness/evidence-boundary）粒度不一致：direction-a/b 是 roadmap 方向，但与 llm-mechanism / formal-re-task / trustworthiness 是不同层次（前者是 axis，后者是 facet）。建议改为：
   - 主干 1：Roadmap A direction（5 action points 子节点）
   - 主干 2：Roadmap B direction（7 action points 子节点 + analytic/generative 二分）
   - 主干 3：3-layer 视图（A/B 各自）
   - 主干 4：concern×mechanism×artifact 字段三元组
   - 主干 5：Background descriptive taxonomy（仅作领域底图）
   - 主干 6：§7 Practical considerations 边界森林（7 项）
3. **I-3：A.2 证据账本只有 4 行，全部 `not_verified`；至少应将本审计 §1 的 E1/E2/E3/E4/E5/E6/E7/E8/E9/E10 拆为独立证据条目**，并对 E1（vision paper 声明）、E10（No data was used）这两条核心边界证据标注 `evidence_strength=verified`（仅基于 paper_content.txt 文本，无需 PDF 版面）。
4. **I-4：旧版 review.md 把 Section 7 当成“限制”而未结构化为 boundary forest 主干**（在“3.8 局限与实践考虑”中只做散述）；应在维度树复原节内显式列为 7 个 leaf-practical_consideration，与 leaf-concern 区分开（PC 是 process / org / human-side，concern 是 technical-side）。

#### M（minor）— 学术影响低，可后续

1. **M-1**：CCF 复核状态字段标注 “WAF”，建议改为 “待核验（HTTP 403/Aliyun WAF）”，措辞更精确。
2. **M-2**：review.md §1 卡片“证据等级”列写“两张 roadmap 图为 原文图表级人工核对”，但本审计与 review.md 各自均**未真的打开 PDF**，应改为“仅文本级（Fig. 2 / Fig. 4 由文本中的 figure caption 与 Summary 段定位）”。
3. **M-3**：A.4 复验清单只有 2 项，建议补充“action point 计数复验”（A=5 个、B=7 个、PC=7 个）等可自动检查项。

#### SUMMARY.md 相关行须修正项
- 样本单位 / 样本数量：应保持 `not_applicable`（roadmap），并显式注明 “Roadmap A action points = 5; Roadmap B = 7; PC = 7（皆为作者构造，非编码样本）”。
- 原生树类型：应改为 “**降级森林（双根 roadmap 森林 + 边界森林）**”，而不是单树。
- 统计池资格：保持 `否（boundary_anchor）`，理由列保留现状。

### 8. 审计附录草案：证据账本与结论映射

下两表可直接替换 / 扩充 review.md 现 A.2 / A.3。

#### A.2 维度树证据账本草案（扩充至 ≥ 10 条）

| 证据标识 | 来源文件 | 原文章节 | 段落 / 表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要 PDF 版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-frelr-001 | paper_content.txt | §1 contributions | Page 2 / 倒数第 2 段 | "this is a vision paper, which does not aim to offer sound empirical evidence… not exhaustive" | type_declaration | text_verified | 决定论文类型 = vision/roadmap；不入统计池 | 否 | 仅锁定类型 |
| EV-frelr-002 | paper_content.txt | §4 引言 + Fig.2 描述 | "Each discussion topic is associated with a circled number… 5 action points" | "Fig. 2 summarises and connects the different discussion topics" | structure_claim | text_verified | Roadmap A 含 5 AP | 建议（图层标签） | A 与 B 层数同 3 但语义不同 |
| EV-frelr-003 | paper_content.txt | §4 各 AP 段 | AP-A1..A5 标号段 | 5 个 action point 名称完整枚举 | action_point_enum | text_verified | leaf-action_point (A) | 否 | 不可外推 |
| EV-frelr-004 | paper_content.txt | §6 引言 + Fig.4 描述 | "7 action points; analytic vs generative tasks" | "structured into three layers" | structure_claim | text_verified | Roadmap B 含 7 AP + 任务二分 | 建议 | -- |
| EV-frelr-005 | paper_content.txt | §6 各 AP 段 | AP-B1..B7 标号段 | 7 个 action point 名称完整枚举 | action_point_enum | text_verified | leaf-action_point (B) | 否 | -- |
| EV-frelr-006 | paper_content.txt | §4 Summary | "formal development layer / conventional development layer / LLM layer" | A 三层结构 | layer_enum | text_verified | leaf-layer (A) | 建议（图） | A 三层 ≠ B 三层 |
| EV-frelr-007 | paper_content.txt | §6 Summary | "formal layer / SW artefact layer / LLM layer" | B 三层结构 | layer_enum | text_verified | leaf-layer (B) | 建议 | -- |
| EV-frelr-008 | paper_content.txt | §7 章节标题序列 | 7 个 PC 子标题 | Collaboration / Empirical Eval / Overreliance / Human Creativity / FM data / Proliferation / Deployment | pc_enum | text_verified | leaf-practical_consideration | 否 | -- |
| EV-frelr-009 | paper_content.txt | §6 Fig.4 Summary 段 | "(i) analytic tasks… (ii) generative tasks" | LLM-task 二分 | task_taxonomy | text_verified | leaf-llm_task_kind | 否 | 仅 Roadmap B |
| EV-frelr-010 | paper_content.txt | §Data availability | "No data was used for the research described in the article." | declaration | dataset_claim | text_verified | 不入统计池的硬证据 | 否 | -- |
| EV-frelr-011 | paper_content.txt | §2.2 formal models | LTS/FSM/Büchi/TA/Statecharts/PN 等 | descriptive taxonomy | background_taxonomy | text_verified | bg-tax | 否 | 仅做描述底图 |
| EV-frelr-012 | paper_content.txt | §5 题序 | 8 个 LLM4RE task demos | task family hints | example_taxonomy | text_verified | candidate task seeds | 否 | ChatGPT 3.5 output 经作者调整 |
| EV-frelr-013 | bibtex.bib / metadata.json | -- | title/author/year/DOI | publisher metadata | metadata | local_verified | 卡片元信息 | 否 | -- |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| C-frelr-T01 | 本文原生维度结构为“双根 roadmap 森林 + 边界森林”，不是单维度树，也不是基于样本编码的 taxonomy | tree_type | 森林根 | EV-frelr-001/002/004/008 | medium | boundary_anchor + schema_seed | 仅本文；不可外推 |
| C-frelr-T02 | Roadmap A 严格含 5 个 action point；Roadmap B 严格含 7 个 action point；§7 严格含 7 项 practical consideration | leaf_enum | leaf-action_point, leaf-practical_consideration | EV-frelr-003/005/008 | strong（在文本范围内） | candidate finding 计数种子（n=5/7/7） | 作者声明 roadmap “非穷尽” |
| C-frelr-T03 | 三层视图存在但 A 与 B 的层语义不同（A: Formal Dev / Conv Dev / LLM；B: Formal / SW Artifact / LLM），不能直接合并 | semantics_warning | leaf-layer | EV-frelr-006/007 | medium | 避免 schema 误并 | -- |
| C-frelr-T04 | 本文不入主统计池（vision/roadmap；无系统检索 / 纳排 / 质量评价 / 数据综合；"No data was used") | pool_exclusion | 森林根 | EV-frelr-001, EV-frelr-010 | strong | boundary_anchor | -- |
| C-frelr-T05 | 每个 action point 可拆解为 6 子字段（concern / mechanism / artifact_in / artifact_out / action_recommendation / supporting_refs），是 Paper2 candidate-finding 表的字段种子 | schema_seed | 12 leaf 表 §4 | EV-frelr-003/005 | weak（基于段落归纳） | schema seed only | 字段是 reviewer 归纳，非作者显式 schema |
| C-frelr-T06 | LLM 任务可二分为 analytic / generative，可作 Paper2 LLM4RE 任务大类种子 | leaf_definition | leaf-llm_task_kind | EV-frelr-009 | weak | candidate heuristic | 仅 Roadmap B Fig.4 范围 |
| C-frelr-T07 | §2 background taxonomy 可作 LLM4STM 领域底图，但不可作为 LLM4STM 综述的工具 / 模型分类事实源 | migration_boundary | bg-tax | EV-frelr-011 | weak | terminology seed | 非编码 schema |
| C-frelr-T08 | §7 的 7 项 practical consideration 可直接迁入 Paper2 risk register（overreliance、empirical eval 难题、artifact proliferation 与 project_1 高度对齐） | candidate_heuristic | leaf-practical_consideration | EV-frelr-008 | medium | risk register seed | -- |
| C-frelr-T09 | review.md 当前主表把 6 个跨论文通用接口叶冒充原生主树，需要降级到“通用接口投影”子节，由本审计 §4 的 12 叶原生表替代 | review_repair | review.md §维度树复原 | EV-frelr-002/004/008 | strong | I 级返修 | -- |

### 9. 技能使用与自我审查记录

#### 9.1 所用技能与采纳的原则
| 技能 / 文件 | 已读 | 采用要点 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | ✓ | claim-evidence gate（C/I/M 严格按学术目标定级）；Evidence policy（不臆造引用 / 数字） |
| `reviewer-guidelines.md` | ✓ | constructive specificity（每条返修都给出位置与可执行动作）；review 五维 |
| `reviewer-self-review.md` | ✓ | 五维自评（Contribution / Clarity / Experiment / Eval / Method / Responsibility）；adversarial questions；claim audit 格式 |
| `research-planning/SKILL.md` + `planning-prompts.md` + `output-schemas.md` | ✓ | 用 schema-first 思路区分 “原文 schema” vs “Paper2 desired schema”；保留 unclear 标记 |
| `autoresearch/SKILL.md` | ✓ | validator-gated 边界：只有具备显式可验证 artifact 的内容才算 verified；本文除作者声明外不构成 validator 满足 |
| ARS reviewer plugin（系统已加载） | ✓（仅元数据） | 不调用，遵守任务 §0 不启动 subagent 的硬约束 |

#### 9.2 reviewer 视角的最高风险 3 点（主线程合并时务必复核）
1. **R-1（高）**：本审计未打开 `paper.pdf`。Fig. 2 / Fig. 4 的“三层”、AP 编号位置、boxed Action Point 文本是否与文本完全一致，**仍需主线程或 A2a 用 PDF 版面核验**。若 PDF 标签与文本叙述差异（例如图层重命名、AP 顺序调整），上表 leaf-layer 与 leaf-action_point 的枚举可能需要微调。
2. **R-2（中）**：每条 action point 的 concern / mechanism / artifact 子字段，是 reviewer 在通读段落后归纳的“准 schema”，不是作者显式列出的字段。主线程在重写 review.md 时应在叶子表里**显式标注** `inferred_by_reviewer=true`，并把这部分提取动作正式委派给 A2a 精核。
3. **R-3（中）**：候选 finding（CF-1..CF-9）只是 candidate；它们在 vision paper 内只有 author-opinion 级强度，但易被下游 LLM agent 误升级为 “研究共识”。主线程应在 Paper2 的 candidate-finding 库中对每条 CF 标注 `evidence_strength=author_opinion`，并要求 Paper2 提供独立证据反复验证后才能升级。

#### 9.3 阻塞 / 超时 / 文件缺失
- **No blocked**：7 个技能文件 + 4 个论文文件均成功读取。
- **transparency 说明**：`paper.pdf` 本轮未打开，已在卡片与 A.2 表中显式标注；不算 blocked，但是 transparent gap，A2a 必须完成 PDF 复核。
- **无 timeout**。
- **总判定**：`pass with I-level repair` — 维度树结构与候选发现边界已锁定，review.md 与 A.2/A.3 需按 I-1..I-4 返修后即可合并至 Paper2 主线。

---

**报告结束。**

## 审计附录：证据链与结论-证据映射

> 本附录是 A1-DT v2 的最小可复验 claim map。更细粒度的证据账本、叶子表和关系边见上文“维度树复原”内的审计报告正文，以及主线程裁决 [../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md)。A1-DT v2 只冻结原生树与迁移边界；页码、表图、supplementary 的最终精核进入 A2a。

### A.1 论文与本地文件来源

| 来源 ID | 文件 / 链接 | 类型 | 用途 | 可核验性 | 备注 |
|---|---|---|---|---|---|
| src-formal-re-llm-roadmap-bib | [bibtex.bib](./bibtex.bib) | 本地元数据 | 标题、作者、年份、DOI / venue | 本地可复验 | 写作引用前仍需按正式出版页复核 |
| src-formal-re-llm-roadmap-text | [paper_content.txt](./paper_content.txt) | PDF 提取全文 | 原生树、字段、统计观察、限制与 finding 边界 | 文本级可复验 | 图表版面与页码进入 A2a |
| src-formal-re-llm-roadmap-pdf | [paper.pdf](./paper.pdf) | PDF 原文 | 表图、页码、版式和补充视觉核验 | 本地可复验 | 未逐项视觉核验的内容不得升级为最终定量证据 |
| src-formal-re-llm-roadmap-codex | [codex 审计结果](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__codex.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-formal-re-llm-roadmap-claude | [claude 审计结果](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__claude.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-formal-re-llm-roadmap-deepseek | [deepseek 审计结果](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__deepseek.md) | 三路审计 | 独立复核输入 | 可复验 | 仅作审计输入，不替代原文 |
| src-formal-re-llm-roadmap-adjudication | [主线程裁决](../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md) | 裁决记录 | 三路冲突处理与最终采用口径 | 可复验 | SUMMARY 回填依据 |

### A.2 维度树证据账本

| 证据 ID | 引用键 | 来源文件 | PDF 页码 | 原文章节 | 段落或行号范围 | 表格或图编号 | 原文短引 | 释义支撑 | 证据角色 | 证据强度 | 支撑的维度节点 | 需要 PDF 视觉核验 | 已废弃 | 替代证据 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ev-formal-re-llm-roadmap-type | clm-formal-re-llm-roadmap-type | paper_content.txt | 待 A2a | 摘要 / 方法 / 研究问题 | 待 A2a | -- | 短引见上文证据锚点 | 支撑原文类型：**vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） | paper_type | text_verified | 原文类型 | 是 | 否 | -- | 不迁移领域结论 |
| ev-formal-re-llm-roadmap-unit | clm-formal-re-llm-roadmap-unit | paper_content.txt | 待 A2a | 方法 / 数据抽取 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本单位：**无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations | sample_unit | text_verified | 样本单位 | 是 | 否 | -- | 只记录本文自己的样本单位 |
| ev-formal-re-llm-roadmap-denom | clm-formal-re-llm-roadmap-denom | paper_content.txt | 待 A2a | 检索 / 纳排 / 结果表 | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑样本数量 / 分母：不存在系统样本分母；roadmap action 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** | denominator | text_verified | 分母链 | 是 | 否 | -- | 中间候选数不得冒充最终分母 |
| ev-formal-re-llm-roadmap-tree | clm-formal-re-llm-roadmap-tree | paper_content.txt + 三路 result | 待 A2a | 抽取表 / taxonomy / roadmap / guideline | 待 A2a | 待 A2a | 短引见上文证据锚点 | 支撑原生树类型：**降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 | schema | text_verified | 原生树 / 维度森林 | 是 | 否 | -- | A1-M0--M6 只作投影 |
| ev-formal-re-llm-roadmap-pool | clm-formal-re-llm-roadmap-pool | 主线程裁决 | -- | adjudication | -- | -- | 见裁决表 | 支撑统计池资格：**否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 | eligibility | adjudicated | 统计池资格 | 否 | 否 | -- | A2a 前不得作为 final finding |

### A.3 结论-证据映射

| 引用键 | 结论 ID | 结论内容 | 结论类型 | 支撑的节点或叶子 ID | 支撑证据 ID 列表 | 反证或限制 | 结论强度 | 允许用于论文的位置 | 已废弃 | 替代结论 |
|---|---|---|---|---|---|---|---|---|---|---|
| clm-formal-re-llm-roadmap-type | A1DT-formal-re-llm-roadmap-C01 | 本文原文类型为：**vision / roadmap**（作者原文 Page 2 明确：“It is worth remarking that this is a vision paper, which does not aim to offer sound empirical evidence”） | paper_type | type | ev-formal-re-llm-roadmap-type | 正式写作前需核对出版页和 PDF 版式 | text_verified | schema_seed / 背景方法样本描述 | 否 | -- |
| clm-formal-re-llm-roadmap-unit | A1DT-formal-re-llm-roadmap-C02 | 本文被编码样本单位为：**无系统样本单位**；最接近的可结构化单位是“**action point**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations | sample_unit | sample_unit | ev-formal-re-llm-roadmap-unit | 若原文同时含辅助单位，主统计只使用裁决后的主单位 | text_verified | schema_seed / A2a 抽取表设计 | 否 | -- |
| clm-formal-re-llm-roadmap-tree | A1DT-formal-re-llm-roadmap-C03 | 本文原生维度树 / 维度森林为：**降级森林**：双根 roadmap 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 | tree_type | native_tree | ev-formal-re-llm-roadmap-tree | 不代表跨论文通用模板 | text_verified | Paper2 方法设计与 pattern library seed | 否 | -- |
| clm-formal-re-llm-roadmap-pool | A1DT-formal-re-llm-roadmap-C04 | 本文统计池资格为：**否**；roadmap / vision；缺系统检索、纳排、质量评价、数据综合 | eligibility | statistical_pool | ev-formal-re-llm-roadmap-pool | A1-DT v2 不生成 final research finding | adjudicated | SUMMARY 总账 / A2a 入口 | 否 | -- |

### A.4 本地复验命令与人工核验清单

| 检查 ID | 复验对象 | 命令 / 人工核验动作 | 通过条件 | 当前状态 |
|---|---|---|---|---|
| chk-formal-re-llm-roadmap-structure | A1-DT v2 结构门禁 | `python project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys/audits/a1dt-v2-19x3/check_structure.py --strict --ready-to-run` | 57 个 result、57 个 log、19 个 adjudication 与 19 篇 review 链接均存在 | 已通过 / 待最终 PR 前复验 |
| chk-formal-re-llm-roadmap-pdf | PDF 表图页码核验 | 人工打开 `paper.pdf`，核对上文涉及的表格、图、页码和附录 | 关键证据锚点可精确到页码 / 表图 / 行号 | A2a 待办 |
| chk-formal-re-llm-roadmap-summary | SUMMARY 回填 | 核对 [../../SUMMARY.md](../../SUMMARY.md) 对应行 | v2 审计状态、样本单位、树型、统计池资格与裁决一致 | 本 PR 已回填 |
