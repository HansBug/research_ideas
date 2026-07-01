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

对本仓库尤其相关的是作者把 formal RE 定义为一组数学化技术，用于 specification、model、verification；其中 formal models 涵盖 LTS/FSM/Büchi Automata、时间自动机（Timed Automata）、Probabilistic/Stochastic State Machines、状态图（Statecharts）、Petri 网（Petri Nets） 等，formal analysis 涵盖 abstract interpretation、static analysis、model checking、proof assistants、deductive verification、refinement。该定义与 project_1 的状态机建模、pyfcstm / UPPAAL / 时间约束方向高度贴近。

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
3. **Translating Formal Languages**：不同 formal languages / tools 服务不同 concern、property、audience；LLM 的 代码到代码翻译（code-to-code translation） 能力可用于 model-to-model / logic-to-logic translation，以支持 FM diversity 和不同抽象层级视图。
4. **Supporting Iterations and Evolution**：formal RE-based process 也是增量迭代的，requirements、specifications、tests、code 和其他 artefacts 需要 trace-links 保持一致；作者建议组合 code-specific LLM 与 NL-oriented LLM 支持 trace-link identification。
5. **Automating Knowledge Engineering**：LLM 可从 requirements、models、文档、tests 等 artefacts 抽取知识，构建 ontologies；ontologies 又可反过来支持一致性检查、artefact 生成、解释与 trace。

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

Fig. 4 由 Formal Layer、SW Artifact Layer、LLM Layer 组成。LLM Layer 分析或生成需求、模型、代码、测试等 SW artefacts；Formal Layer 以 formal requirements、formal verification、argumentation、FM knowledge、formal domain knowledge、formal prompts、运行时验证（runtime verification）、ethical requirements 等方式提供控制。七个 action points 如下。

1. **Ensuring Correctness through Formal Requirements and Argumentation**：LLM-generated requirements / specifications / artefacts 需要像人工需求一样做 quality assurance；formal notation、formal specification、verification、formal argumentation structure 可提高可解释性、逻辑一致性并缓解 hallucination。
2. **Improving Mathematical Reasoning with Formal LLMs**：cyber-physical requirements 常包含数学公式；LLM 数学推理弱，可通过数学/FM 专用模型、RAG、多个专长 LLM agents、calculator / reasoner 等外部工具支持。
3. **Formal Prompt Engineering**：prompt 在 code/model generation 场景中近似“需求”；自然语言 prompt 也会有歧义。作者建议用 formal notations、controlled NL、前置 / 后置条件（pre/post-conditions）、UML-like prompt architecture 来约束 prompt 和 agent orchestration。
4. **Formal Domain Knowledge and Explainability**：domain-specific text scarce 时，formal ontologies / knowledge graphs 可约束推理、减少 hallucination、提高效率，并作为解释/justification 的外部依据。
5. **Ensure LLM Output Consistency through Formal Verification**：LLM 系统缺乏传统软件那种 predictability / repeatability；作者提出用 abstract interpretation / abstraction methods 近似分析 neural network 行为，验证 prompt perturbation 下输出一致性，尤其面向 safety-critical LLM components。
6. **Regulatory Compliance at Runtime**：LLM 会随新知识或 fine-tuning 演化，法规也会变化；运行时验证（runtime verification） 可用于持续监测 regulatory requirements。
7. **Mitigate Bias and Address Ethical Concerns**：trustworthiness threats 包括 toxicity、stereotype bias、adversarial / out-of-distribution robustness、privacy、machine ethics、fairness 等；作者建议 formalise ethical requirements，并用 formal techniques 验证 LLM-generated artefacts。

对 Paper2 最关键的是 Roadmap B 的组织方式：不是笼统说“formal methods make LLM reliable”，而是把 reliability 分解为 correctness、logical coherence、mathematical reasoning、prompt precision、domain grounding、output consistency、regulatory compliance、bias/ethics/fairness 等 concern，并给出对应 formal mechanism。

### 3.7 主要结论

论文结论保持 vision paper 口径：两个 roadmaps 旨在激发 RE / SE 社区研究。一方面，LLM 可让 formal languages / tools 更易用；另一方面，在 LLM 参与 RE 活动时，formal techniques 可缓解 LLM-generated artefacts 的正确性和可信性问题，并支撑 responsible / trustworthy AI。作者特别指出这些 roadmaps 适合 mission-critical systems 的 rigorous process，如 V-process，但并不限于此，因为 safety、security、privacy、ethical requirements 正变得更普遍。

作者自述将优先推进三个方向：requirements-to-formal-logic translation、LLM 生成/分析软件 artefacts、LLM 解释 formal artefacts。

### 3.8 局限与实践考虑

原文局限不是传统 threats-to-validity 表，而是 practical considerations：

1. LLM 与 FM 专家分属 statistical vs deterministic 思维传统，需要 RE bridge role。
2. 经验评估困难：RE 缺少数据集，FM 经验成熟度有限；很多 generative output 没有唯一 真值（ground truth），需要 定性方法（qualitative methods）。
3. overreliance：LLM 幻觉可能因语言流畅和“自信”解释误导 analyst；formal verification 不是全部，还需要 以人为中心的质量控制（human-centred quality control）、hallucinatory pattern 识别和部署前 robustness testing。
4. 人类创造力风险：图中有意省略 human actors，以强调自动化，但作者反过来认为 requirements engineers 会更核心，因为 requirements 成为控制 LLM/code generation 的主要接口。
5. FM 数据训练不足：formal language 数据有限，需 code-specialised LLM、FM fine-tuning、多模型集成、交互式（interactive） generation、agent 访问 model checker / compiler 等。
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
| report structure pattern | 结构是：structured abstract → Introduction / Background → formal process example → Roadmap A → LLM-driven RE example → Roadmap B → Practical considerations → Conclusion。 | 全文目录与章节。 | 对 Paper2 的 roadmap / discussion section 有参考价值：先示例揭示痛点，再分层路线图，再列 implementation risks。 | 不适合作为 SLR/SMS report structure 的复制对象；缺少 Method / Search / Selection / Data extraction / Synthesis 章节。 |

## 5. A1-M0--M6 脚手架元维度贡献

| 脚手架元维度 | 本文可贡献的模式先验 | 可用方式 | 限制 |
|---|---|---|---|
| A1-M0 主题与综述元模型设定 | 提供“LLM automation 需要被 correctness / fairness / trustworthiness concerns 约束”的主题边界；也提供“LLM 支持形式化、形式化约束 LLM”的双向元模型。 | 在 Paper2 设定综述元模型时，可把 automation capability 与 audit / assurance capability 并列，而不是只收集工具功能。 | Roadmap 不是系统证据，不能决定最终综述范围；需要研究者批准。 |
| A1-M1 脚手架挖掘与种子探测 | 可作为非 SLR/SMS 的 roadmap seed，用来挖掘 concern/action pattern：accessibility、correctness、explainability、traceability、domain knowledge、regulatory compliance、ethics。 | 用于补充 `survey_of_surveys` 的 pattern library，提醒 A2a 支持 `vision/roadmap` 类型。 | 只做边界锚点；不能进入目标 evidence pool。 |
| A1-M2 维度模式批准 | 启发字段：`roadmap_direction`、`layer`、`task_family`、`artifact_in/out`、`assurance_concern`、`mechanism`、`action_point`、`evaluation_need`、`implementation_risk`。 | 研究者可把这些字段纳入候选维度模式，要求每个候选发现都说明 concern 与 mechanism。 | 若过度扩字段，会让抽取负担过高；需 A2a dry-run 决定是否拆分。 |
| A1-M3 论文收集与概览 | 提醒候选池不要只收 SLR/SMS；高价值 vision/roadmap 需要以 `review_type=vision/roadmap` 降级管理。 | 概览卡中显式写“非 SLR/SMS，但可作 schema/heuristic seed”。 | 不能把 roadmap 文数量统计混入 SLR/SMS 统计口径。 |
| A1-M4 字段级证据抽取与模式演化 | 提供 action-point-level evidence anchors；每个 action point 都可抽为 `concern -> mechanism -> artifact -> limitation`。 | 对 Paper2 字段证据表，可要求非统计类文献也保留来源锚点和不确定说明。 | 作者观点和例子驱动，不应作为已最终核验的依据；要标注证据等级。 |
| A1-M5 统计分析 | 主要贡献是负面边界：本文不支撑分布统计，不应纳入频次结论。 | 在统计分析协议中增加 `eligible_for_statistical_synthesis` 或 `evidence_role` 字段。 | 若混入统计，会污染目标综述 findings。 |
| A1-M6 候选发现形成 | 启发候选发现从“某技术常见”升级为“某 concern 在某 artefact/task 中出现，现有 mechanism 能部分缓解，但需要某类验证”。 | 适合生成 finding heuristic：concern-first、mechanism-linked、risk-aware、human-gated。 | 只能生成候选发现线索，不能直接接受为最终领域发现。 |

## 7. 对 Paper2 的启发与风险

### 7.1 启发

1. **支持“concern-first finding heuristic”**：候选发现不应只是“某类工具很多”，而应表达为“某类 task / artefact 存在某 concern，某类 mechanism 可部分缓解，但仍需要某类 evidence / human gate”。
2. **支持双向路线图叙事**：Paper2 的 agentic SLR 不仅是“LLM/agent 支持综述”，还应有“审计制品、研究者门控和证据链约束 LLM/agent”的反向控制线。这与本文 two-way roadmap 结构高度一致。
3. **支持把 trustworthiness 拆为字段**：correctness、fairness、explainability、robustness、compliance、ethics 等应成为候选 concern，而不是笼统写“可信”。
4. **支持 action-point 级抽取**：roadmap 文不提供统计分母，但每个 action point 都可成为模式先验；Paper2 可把 action point 抽成可审计字段，而非直接当 finding。
5. **支持“formal / structured artefact 作为审计接口”**：formal prompts、前置 / 后置条件（pre/post-conditions）、ontology、argumentation、runtime monitor 等提醒 Paper2：智能体工作流的提示词、字段表、证据表、质疑日志都应结构化，不能只保存在自然语言对话里。
6. **支持非唯一答案的评价设计**：作者明确指出 formal specification / code 转换常没有唯一正确答案，需要 qualitative evaluation。这对 Paper2 的人工裁决、质疑日志和降级机制非常重要。
7. **贴近 project_1 / Paper2 交叉点**：状态机、时间自动机（Timed Automata）、model checking、UPPAAL、formal artefact explanation、Req2Model / Req2Logic 都可作为后续 LLM4STM / LLM4Modeling mini-case 的维度种子。

### 7.2 风险

1. **roadmap 文不能混入 SLR/SMS 统计池**：它没有系统检索与纳排，不能支撑“领域中多数研究如何”的统计观察。
2. **action point 不是 empirical finding**：只能作为候选启发式或 模式种子，不能作为目标领域最终发现。
3. **示例带有演示性质**：sender-receiver 和 red-crossing 示例有助于讲清思路，但不能代表复杂工业系统；ChatGPT 3.5 输出还经过人工压缩和少量调整。
4. **“formal methods provide guarantees”有前提**：formalisation 必须正确、property 必须覆盖真实需求、抽象必须保守、工具链必须可信；否则 formal verification 只能验证错误模型或不完整 property。
5. **过度形式化风险**：Paper2 若照搬 FM 叙事，可能把 agentic SLR 写成重形式化系统，增加实现负担；应只迁移“结构化审计与 concern field”，不迁移全部 formal verification 承诺。
6. **人类角色不能被弱化**：原文 Fig. 2 / Fig. 4 有意省略 human actors，但 Section 7 反而强调 requirements engineers 的核心性。Paper2 必须坚持 G0--G5 研究者门控，避免被误读为自动化替代专家。
7. **模型/工具漂移**：本文示例基于 2024 年前后的技术状态；Paper2 若引用具体 LLM 能力，应避免写成稳定事实，应记录 model version、调用时间和可复核输出。

## 9. 待复核

1. 若后续要在正文引用 Fig. 2 / Fig. 4，建议补页码与图中各元素的正式英文 label，并确认图中 “formal / conventional / LLM layer” 与 “formal / SW artefact / LLM layer” 的命名。
2. 若后续要引用 CCF 字段，建议提交前再次核验当轮 CCF 官方目录；本轮沿用本仓库 ccf_venues 缓存记录 IST 为 B 类；2026-06-29 官方目录 HTTP/CLI 访问返回 Aliyun WAF 壳，正式写作前需人工打开官方目录复核。
3. Section 5 的 ChatGPT 3.5 输出经过作者“slightly adjusted”；若用于论证 LLM 能力，应只作为 illustrative evidence，不作为可重复实验。
4. 需要决定 A2a 是否正式支持 `vision/roadmap` 类型；若支持，应同步更新 `SUMMARY.md` 和 `pattern-field-schema.md`，并明确不纳入 SLR/SMS 统计池。
5. 若用于 project_1 状态机建模，应进一步深读作者引用的 model generation、nl2spec、Natural2CTL、formal tool usability、formal methods diversity 文献，形成单独相关工作链。

## 维度树复原

> [!IMPORTANT]
> 本节是 A1-DT v2 主线程裁决后的当前事实入口。A1-M0--M6 只作为跨论文投影层，不能反向冒充本文原生模式。
> 三路原始审计结果见 [../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__codex.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__codex.md)、[../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__claude.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__claude.md)、[../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__deepseek.md](../../audits/a1dt-v2-19x3/results/formal-re-llm-roadmap__deepseek.md)；主线程裁决见 [../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md](../../audits/a1dt-v2-19x3/adjudications/formal-re-llm-roadmap.md)。

### v2 主线程采用说明

本节采用 `claude` 审计结果作为正文主干，并用另外两路结果校正分母、统计池资格和降级边界。当前剩余风险统一归入 A2a 的页码、表图和补充材料精核。

### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| 论文目录标识 | `formal-re-llm-roadmap` |
| 审计代理 | `claude` |
| 是否已读 `paper_content.txt` | 是；全 2517 行分两批读取（1–939、940–1840、1840–2517 引用列表），结合 paper 末段三遍核验 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；都已读取，确认期刊为 Information and Software 技术 181:107697 (2025)，DOI `10.1016/j.infsof.2025.107697` |
| 是否打开或核对 `paper.pdf` | 否，本轮**未做 PDF 版面核验**；以 `paper_content.txt` 文本为准，Fig. 2、Fig. 4 仅以文本中“Fig. 2/Fig. 4 summarises and connects…”段落定位；版面级（页码、图层标签位置、表格排版）需 A2a 回 PDF 复核 |
| 原文类型 | **愿景 / 路线图**（作者原文 Page 2 明确：“It is worth remarking that this is a 愿景 paper, which does not aim to offer sound 经验研究（empirical） 证据”） |
| 被编码样本单位 | **无系统样本单位**；最接近的可结构化单位是“**行动点**”（Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个）；以及 Sec 7 的 7 项 practical considerations |
| 样本数量 / 分母 | 不存在系统样本分母；路线图行动项 数固定为 5 + 7 = 12；如把 Section 7 视为辅助森林则 +7 = 19。**不可作为统计分母使用** |
| 原生树类型 | **降级森林**：双根 路线图 森林（Roadmap A、Roadmap B）+ 边界森林（Practical considerations）；不是单树，也不是基于样本编码的维度森林 |
| 主统计池资格 | 否；不进入后续主统计池。A1-DT v2 仅允许其作为方法学种子、模式种子或边界锚点；若原文内部存在 convenience sample / guideline 示例统计，也不得混入 Paper2 主统计池。 |
| 总体判定 | **v2 已返修完成**：本节已按 A1-DT v2 口径重写为原生样本编码树 / 维度森林，剩余页码、表图、补充材料风险进入 A2a。 |

### 1. 原文证据阅读说明

- **实读文件**：`bibtex.bib`、`metadata.json`、`paper_content.txt`（全 2517 行三段读完）、`review.md`（全 480 行两段读完）。`paper.pdf` 本轮未打开（属本审计的 transparency 项，需 A2a 复核排版级证据）。
- **技能文件**：均已读取：`ai-research-writing-skill/SKILL.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`、`research-planning/SKILL.md`、`planning-prompts.md`、`output-schemas.md`、`autoresearch/SKILL.md`。所用核心原则：claim-证据 gate、reviewer 5-dim、5-dim 自评、reviewer constructive specificity、autoresearch validator-gated 边界判定。
- **覆盖章节**：Abstract、§1 Introduction、§2 Background (含 §2.1 LMs/LLMs in RE、§2.2 Formal RE)、§3 Example A (PROMELA)、§4 Roadmap A、§5 Example B (ChatGPT)、§6 Roadmap B、§7 Practical considerations、§8 Conclusion、CRediT、数据可获得性（Data 可获得性）、References（175 条）。

#### 关键证据锚点（约 10 条）

| 序号 | 证据位置 | 原文短引 / 释义 | 用途 |
|---|---|---|---|
| E1 | Page 2 §1 contributions 段 | “It is worth remarking that this is a 愿景 paper, which does not aim to offer sound 经验研究（empirical） 证据 but rather to indicate possible avenues of research… the discussed 路线图 should not be considered exhaustive.” | 决定论文类型 = 愿景/路线图；不进主统计池 |
| E2 | Page 8 §4 引言段 + Fig. 2 描述 | “Each discussion topic is associated with a circled number… Fig. 2 summarises and connects the different discussion topics” + 标注 ①~⑤ | 锁定 Roadmap A 由 5 个 行动点 组成 |
| E3 | Page 8–11 §4 各 Action Point | 五个标号 Action Point: Generating FM/SE Artifacts; Explaining FM Artifacts; Translating Formal Languages; Supporting Iterations and Evolution; Automating Knowledge Engineering | Roadmap A 行动点 名单 |
| E4 | Page 14 §6 引言段 + Fig. 4 描述 | “Each discussion item is associated with a circled number, which appears in the figure” + ①~⑦ | 锁定 Roadmap B 由 7 个 行动点 组成 |
| E5 | Page 14–16 §6 各 Action Point | 七个标号 Action Point: Ensuring Correctness… Argumentation; Improving Mathematical Reasoning…; Formal Prompt Engineering; Formal Domain Knowledge…; Ensure LLM Output Consistency…; Regulatory Compliance at Runtime; Mitigate Bias… Ethical Concerns | Roadmap B 行动点 名单 |
| E6 | §4 Summary（Fig. 2 描述） | "structured into three interconnected layers… a formal development layer, a conventional development layer and an LLM layer” | Roadmap A 三 layer 结构 |
| E7 | §6 Summary（Fig. 4 描述） | "structured into three layers, a formal layer, a software (SW) artefact layer and a LLM layer” | Roadmap B 三 layer 结构 |
| E8 | §7 段落标题序列 | "Collaboration… / Empirical Evaluation / Overreliance on LLM Output / Diminishing Role of Human Creativity / Limited Training on FM 数据集 / Proliferation and Maintainability of Artefacts / 部署, Scalability and Technological Evolution" | Section 7 的 7 类 practical consideration 边界森林 |
| E9 | §6 行内说明 §6 type-of-task | LLM Layer 任务被作者显式二分为：“(i) analytic tasks… (ii) generative tasks” | Roadmap B 内部任务分类（analytic vs generative） |
| E10 | §8 Conclusion + 数据可获得性（Data 可获得性） | “No data was used for the research described in the article.”（即未使用数据） + 作者自述未来工作 3 项 | 锁定无样本数据；路线图 不是 证据 base |
| E11 | §2.2 formal 模型 段 | LTS/FSM/Büchi Automata / 时间自动机（Timed Automata） / Probabilistic & Stochastic SM / 状态图（Statecharts） / 层次状态机（Hierarchical SM） / Petri 网（Petri Nets） 子分类 | Background 内置的描述性 分类法（不是抽取 模式，仅供 LLM4STM 主题边界参考） |
| E12 | §5 段落标题序列 | 需求 生成（Generation） / User Feedback Analysis / Smell Detection / Completeness Check / Model 生成（Generation） / 需求 分类 / 需求 Tracing / Code-related Tasks | Example B 演示的 LLM4RE task family（用例驱动，不是 systematic survey） |

### 2. 样本单位与字段来源判定

1. **原文纳入对象**：本文不“纳入”样本。它通过两个 worked example 揭示 FM 与 LLM 各自的局限，再以作者经验 + 引用 seminal works 的方式构造两个 路线图。
2. **是否有系统检索 / 纳排 / 数据抽取 / 编码方案**：**没有**。无 search protocol、无 PRISMA、无 inclusion / 排除标准、无 质量 appraisal、无 抽取 form、无 编码方案。
3. **字段来源**：所有结构化内容都来自**作者自身组织**：
   - Roadmap A / B 的“行动点”是作者自定义的研究议程项。
   - Fig. 2 / Fig. 4 的“three layers”是作者用 Photoshop-layer 比喻定义的可视化层级（脚注 9：layers 应理解为 graphical layers）。
   - Section 7 的 7 个 practical consideration 是作者枚举的实践约束类别。
4. **RQ 与样本单位关系**：原文无显式 RQ 列表；隐含两个对称 question：(a) 如何用 LLM 提升 formal RE 的可用性？(b) 如何用 FM 提升 LLM-based RE 的 correctness/fairness/trustworthiness？这两个 RQ 直接对应两个 路线图，**路线图行动项 point 就是 RQ 的结构化答案，而非用 RQ 编码出的样本**。
5. **降级处理**：作为 愿景/路线图，本文只能作 **边界锚点 + 方法学种子 + candidate heuristic**：
   - 边界锚点：证明 Paper2 的脚手架需要容纳非 SLR/SMS 文献，并显式 `eligible_for_statistical_synthesis=false`
   - 方法学种子：双向 路线图 结构、layer 分层、concern→mechanism→action 字段串
   - candidate heuristic：每个 行动点 是一条 候选发现，但需 Paper2 跨文献证据再次裁决

### 3. 原生样本编码维度树 / 维度森林

> 中文化导读：本维度树复原的是形式化需求工程与大语言模型路线图如何组织研究机会、技术路径、风险和边界。树中保留 LLM、RAG、CTL、ontology、knowledge graph 等英文，是因为它们是原文领域术语或形式化方法缩写；中文层级负责说明它们属于哪一类问题、技术或风险。该文更适合作为边界锚点和模式种子，而不是统计池样本。可迁移到 Paper2 的是“路线图论文也需要区分问题空间、技术空间、证据边界和过度信任风险”。

原生结构为**双根 路线图 森林 + 边界森林**：

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[本文原生维度森林]
│
├── [路线图 A] 用 LLM 支持基于形式化方法的开发（Using LLMs to support FM-based development；Fig. 2）
│   ├── 形式化开发层
│   ├── 传统开发层
│   ├── LLM 层：LLM 智能体（LLM 智能体）
│   └── 五个行动点
│       ├── AP-A1 生成形式化方法与软件工程制品：关注状态空间爆炸、规约抽象、自然语言歧义、FM 训练数据不足；机制包括 RAG、代码摘要、nl2spec、Natural2CTL、交互式翻译
│       ├── AP-A2 解释形式化制品：关注可解释性、反例可理解性、长规约非模块化；目标对象包括模型、公式、反例
│       ├── AP-A3 翻译形式化语言：关注工具多样性、形式化方法多样性和不同受众；机制借鉴 代码到代码翻译（code-to-code translation）
│       ├── AP-A4 支持迭代与演化：关注 追踪链接维护（trace-link maintenance） 与制品对齐；机制为 面向代码的 LLM（code-specific LLM）+ 面向自然语言的 LLM（NL-oriented LLM） 组合
│       └── AP-A5 自动化知识工程：关注领域知识抽取与本体维护；机制包括 基于 LLM 的本体工程（ontology engineering）/ 知识图谱（knowledge graph）
│
├── [路线图 B] 用形式化方法支持基于 LLM 的开发（LLM-based development）（Using FMs to support LLM-based development；Fig. 4）
│   ├── 形式化层
│   ├── 软件制品层
│   ├── LLM 层：任务类型为分析型（analytic）或生成型（generative）
│   └── 七个行动点
│       ├── AP-B1 通过形式化需求与论证确保正确性：关注 幻觉（hallucination）、貌似合理性（plausibility）、新手过度信任（novice over-trust）、逻辑一致性（logical coherence）
│       ├── AP-B2 用 Formal LLMs 改善数学推理：关注 弱数学推理（weak math reasoning） 与 CPS 数学需求；机制包括 LeanDojo、multi-LLM 智能体、外部计算器 / 推理器（external calculator / reasoner）
│       ├── AP-B3 形式化提示工程：关注 提示词歧义（prompt ambiguity）、制品缺陷（制品 defects）、多提示词编排（multi-prompt orchestration）；机制包括 ACSL-style 前置 / 后置条件（pre/post-conditions） 与 UML-style prompt architecture
│       ├── AP-B4 形式化领域知识与可解释性：关注 领域语料稀缺（domain 语料 scarcity） 与 世界模型缺口（world-模型 gap）；机制为通过 检索增强生成（RAG）注入形式化本体（formal ontology）/ 知识图谱（knowledge graph）
│       ├── AP-B5 通过形式化验证确保 LLM 输出一致性：关注 提示词扰动下的可预测性（predictability）/ 可重复性（repeatability） 与 安全关键嵌入（safety-critical embedding）
│       ├── AP-B6 运行时监管合规：关注 LLM 演化与法规演化导致的 反复合规（recurring compliance）；机制为 运行时验证（runtime verification）
│       └── AP-B7 缓解偏见与伦理问题：关注 毒性（toxicity）、刻板印象（stereotype）、鲁棒性（robustness）、分布外（OOD）、隐私（privacy）、公平性（fairness）、机器伦理（machine ethics）；机制为 形式化伦理需求（formalised ethical requirements）
│
└── [边界森林] §7 实践考虑与限制（Practical Considerations & Limitations；下文简称“实践限制”）
    ├── PC-1 LLM 与 FM 专家协作
    ├── PC-2 经验评价：定性方法（定性 方法）、缺少 真值（ground truth）
    ├── PC-3 过度依赖 LLM 输出：以人为中心的质量控制（human-centred 质量 control）、幻觉模式（hallucinatory patterns）
    ├── PC-4 人类创造力角色变化：重新定位 RE engineer
    ├── PC-5 FM 数据集训练不足：微调（fine-tune）、代码类比（code-analogue）、交互式（interactive）
    ├── PC-6 制品数量膨胀与可维护性：可视化（visualisation）、分析（analytics）
    └── PC-7 部署、可扩展性与技术演进：状态空间爆炸（state-space explosion）、蒸馏（distillation）、技术演进速度（tech evolution pace）
```

辅助：**§2 Background 分类法**（与抽取无关，仅作描述性领域底图，可作 LLM4STM 边界种子）：

```text
说明：本树已中文化；括号内保留的英文 / 缩写为原文术语、作者枚举或稳定标识。
[背景描述分类法]
├── LLM 历史：词袋（BoW）/ tf-idf → 词向量（word embeddings）→ BERT → LLM → 提示（prompting）/ RAG / LoRA / 蒸馏（distillation）→ LLM 智能体（LLM 智能体）
└── 形式化需求工程（Formal RE）背景
    ├── 规约语言：Z、VDM、B-Method、CCS、CSP、SDL、CASL、LOTOS、TLA+、Alloy、FizzBee、ACE
    ├── 性质逻辑：LTL、CTL、CTL*、μ-calculus、HOL、Modal、MTL / RTTL、概率时序逻辑（Probabilistic TL）
    ├── 形式模型：LTS、FSM、Büchi、时间自动机（Timed Automata）、概率 / 随机状态机（Probabilistic / Stochastic SM）、状态图（Statecharts）、层次状态机（Hierarchical SM）、Modelica SM、Ptolemy II SM、Petri 网（Petri Nets）
    └── 分析方法：抽象解释（Abstract Interpretation）、语义静态分析（Semantic Static Analysis）、模型检查（Model Checking）、证明助手（Proof Assistants）、演绎验证（Deductive Verification）、精化式设计（设计 by Refinement）
```

### 4. 叶子维度表

下表是把上述原生森林的每条 行动点 拆出 **6 维子字段** 后的叶子表。这些子字段是作者实际在每个 行动点 段落中写到的内容（concern / mechanism / 制品 / refs / action 推荐），不是 reviewer 主观套模板。

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| leaf-路线图_direction | 路线图 方向 | 森林根 | §4/§6 章节自述 | 双向中的具体方向 | {LLM→FM, FM→LLM} | 完整枚举（闭） | 不允许缺失 | 不入统计池；二元 boundary 标签 | 用作 Paper2 双向叙事种子 | E2,E4 | 仅迁移“双向 路线图”结构 |
| leaf-layer | 可视化层 | Roadmap A/B 内 | §4/§6 Summary 段、Fig.2/4 描述 | 作者定义的 graphical layer | A:{Formal Dev, Conventional Dev, LLM}; B:{Formal, SW Artifact, LLM} | 完整枚举（但 A/B 不同义） | n/a | 不入统计池 | 用作 layer-based 叙事框架 | E6,E7 | A、B 层数同为 3 但语义不同，不能直接合并 |
| leaf-action_point | 行动点 | layer 内 | §4/§6 ①~⑤ / ①~⑦ 段 | 作者标号的研究议程项 | A: 5 项已枚举；B: 7 项已枚举（见 §3 节树） | 完整枚举（封闭，但作者声明非穷尽） | 不允许缺失 | 不入统计池；可作 candidate-发现 计数（n=12） | 每条 = 一条 候选发现 种子 | E3,E5 | 必须配 concern + mechanism；不可孤立迁移 |
| leaf-concern | 关注 / 痛点 | action_point | 段落内显式 concern 表述 | 行动点 想解决的问题 | 自由文本 + concern_分类法 {可解释性（explainability）, 幻觉（hallucination）, 数学推理（math reasoning）, 提示词歧义（prompt ambiguity）, 领域落地（domain grounding）, 输出一致性（output consistency）, 监管合规（regulatory compliance）, 偏见 / 伦理（bias/ethics）, FM 数据稀缺（FM data scarcity）, 状态空间爆炸（state-space explosion）, …} | 自由文本加 emergent 分类 | 缺失时标 未说明（not stated） | 不入统计池 | 作 Paper2 concern field 种子 | E3,E5,E8 | 部分 concern 在 §7 重述，注意去重 |
| leaf-mechanism | 机制 / 干预 | action_point | 段落内 mechanism 描述 | 应对 concern 的形式化或 LLM 机制 | 自由文本 + mechanism_分类法 {RAG, 微调（fine-tuning）, 多智能体（multi-智能体）, 形式化验证（formal verification）, 抽象解释（abstract interpretation）, 运行时验证（runtime verification）, 本体 / 知识图谱（ontology/KG）, 形式化论证（formal argumentation）, 受控自然语言（controlled NL）, ACSL 风格前 / 后置条件（ACSL-style pre/post）, 代码翻译（code-translation）} | 层级枚举（emergent，不封闭） | 缺失时 未说明（not stated） | 不入统计池 | 作 mechanism field 种子 | E3,E5 | 机制粒度不一，A2a 需拆细 |
| leaf-artifact_in | 输入制品 | action_point | 段落内提及的输入对象 | LLM/FM 处理的对象 | {自然语言需求（NL req）, 用户故事（user story）, 反馈（feedback）, issue, 代码（code）, 形式化模型（formal 模型）, 逻辑公式（logic formula）, 反例（counterexample）, 领域文档（domain doc）, 法规（regulation）, 伦理原则（ethics principle）} | 完整枚举（emergent） | 缺失时 未说明（not stated） | 不入统计池 | 作 RE 制品 流图种子 | E3,E5 | 与 leaf-artifact_out 配对，构成 transformation 关系 |
| leaf-artifact_out | 输出制品 | action_point | 段落内提及的输出对象 | LLM/FM 生成的对象 | {形式化规约（formal spec）, 形式化性质（formal property）, 软件模型（software 模型）, 代码（code）, 追踪链接（trace link）, 分类结果（分类）, 自然语言解释（NL explanation）, 知识图谱（knowledge graph）, 验证结果（verification result）, 运行时监视器（runtime monitor）, 候选需求补全（candidate req completion）} | 完整枚举（emergent） | 缺失时 未说明（not stated） | 不入统计池 | 作 RE 制品 流图种子 | E3,E5 | 同上 |
| leaf-action_推荐 | 行动建议 | action_point | "Action Point:" 框 | 作者明文落款的研究建议 | 自由文本 | 自由文本（≈12 条） | 不允许缺失（每个 AP 必有一条） | 不入统计池 | 可作 candidate research action | E3,E5 | 不可直接外推为已验证发现 |
| leaf-supporting_refs | 支持文献 | action_point | 段内行内引用 | 作者所举 seminal / preliminary work | 引用列表（参考 §References） | 关系值（指向 BibTeX 编号） | 缺失允许 | 不入统计池 | 可作扩库候选种子（如 [115][118][119][152][159][160][163]） | E3,E5 | 引用 ≠ 系统综述，不能当 证据 base |
| leaf-evidence_strength | 证据强度 | action_point | reviewer 评估 | 该 AP 的支撑性质 | {formal_proof, executable_counterexample, expert_定性, worked_example_only, author_opinion} | 完整枚举 | -- | 不入统计池 | 用于 candidate-发现 降级 | E1,E10 | 全部应默认 ≤ worked_example_only / author_opinion |
| leaf-llm_task_kind | LLM 任务种类 | Roadmap B / Layer-B3 | §6 Fig.4 Summary 段 | 作者把 LLM-layer 任务二分 | {analytic, generative} | 完整枚举（闭） | n/a | 不入统计池 | 作 Paper2 LLM4RE 任务大类种子 | E9 | 仅适用 Roadmap B；不映射到 Roadmap A |
| leaf-practical_consideration | 实践约束类别 | Boundary Forest | §7 子标题 | 作者枚举的实施障碍 | {协作（Collaboration）, 实证评价（Empirical Eval）, 过度依赖（Overreliance）, 人类创造力（Human Creativity）, 基础模型训练数据（FM Training Data）, 制品扩散（Proliferation）, 部署 / 可扩展性 / 技术演进（部署/Scalability/Tech Evol）} | 完整枚举（n=7） | -- | 不入统计池 | 作 Paper2 risk-register 种子 | E8 | 与 leaf-concern 部分重叠，注意去重 |

> **重要边界**：现 `review.md` 主表中的 6 个 `leaf-formal-re-llm-roadmap-{scope,corpus,分类法,method,evidence,发现}` 是**跨论文通用接口投影**，不是原文叶子；它们正确的位置是后文 “通用接口投影” 小节，不应被当成主原生树。本审计上表 12 个叶子才是原文真实结构的最小复原层。

### 5. 关系边表

本文 模式 不是 entity–关系 型；但仍可识别出 **隐式关系边**，用于支撑 Paper2 的 RE 制品 流图：

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| rel-ap_addresses_concern | action_point | addresses | concern | 多对多 | 缺失→ 未说明（not stated） | E3,E5 | 反向检索：某 concern 由哪些 AP 覆盖 |
| rel-ap_proposes_mechanism | action_point | proposes | mechanism | 多对多 | 缺失→ 未说明（not stated） | E3,E5 | 机制族归并 |
| rel-artifact_transformation | artifact_in | transformed_to | artifact_out | 多对多（由 mechanism 实现） | 缺失允许 | E3,E5 | RE 制品 流图 |
| rel-layer_contains_ap | layer | contains | action_point | 一对多 | n/a | E6,E7 | layer-AP 归属 |
| rel-direction_owns_layer | 路线图_direction | owns | layer | 一对多 | n/a | E2,E4 | 双向路线图区分 |
| rel-ap_supported_by_ref | action_point | supported_by | bibref | 多对多 | 缺失允许 | E3,E5 | 扩库 seed |
| rel-pc_constrains_路线图 | practical_consideration | constrains | 路线图 (A 或 B) | 多对多 | n/a | E8 | 边界森林对正树的反向约束 |

未发现：原文未给出形式化的 ER 模式、UML class 模型 或 OWL 关系；上述关系边均为 reviewer 从段落中归纳，**非作者显式声明**，A2a 复核时需在每条边上标注 `inferred_by_reviewer=true`。

### 6. 统计观察、候选发现 与 最终发现边界

#### 6.1 由字段 / 统计表支持的统计观察
**无**。本文不含任何统计表、频次表、Q&A 表或 coding distribution。作者在数据可获得性（Data 可获得性）声明中明确写作 "No data was used"（即未使用数据）。

#### 6.2 作者 discussion / 路线图 提出的候选发现（每条均为 candidate，evidence_strength ≤ worked_example_only）
- CF-1：LLM 的 code-summarisation 能力可被借用于 code→formal spec 抽象，以缓解 state-space explosion（AP-A1）。
- CF-2：counterexample 的解释难度类似 stack-trace，可借用 LLM 的 trace-explain 思路（AP-A2，引 [132]）。
- CF-3：FM diversity 可通过 LLM 驱动的 模型-to-模型 translation 维持（AP-A3）。
- CF-4：trace-link 由 面向代码的 LLM（code-specific LLM）+ 面向自然语言的 LLM（NL-oriented LLM） 联合更可靠（AP-A4）。
- CF-5：LLM 的数学推理瓶颈未必能靠规模扩张解决，需要外挂 formal/calc 资源（AP-B2，引 [151]）。
- CF-6：prompt 即“需求”，应引入 ACSL-style pre/post-condition（AP-B3）。
- CF-7：abstract interpretation 在 NN/transformer 上的应用是缓解 LLM 不可重复性的可行路径（AP-B5）。
- CF-8：regulatory compliance 必须从一次性证明转为 runtime monitoring（AP-B6）。
- CF-9：ethical/fairness 必须先 formalise 为 requirement，再用 formal techniques 验证（AP-B7）。

#### 6.3 对 Paper2 可迁移的方法学启发
- 双向 路线图 叙事（LLM 帮 X / X 帮 LLM）作为 Paper2 第二篇的结构 seed。
- “concern → mechanism → 制品 → action” 字段串作为 candidate-发现 表的字段约束。
- "analytic vs generative" 二分（E9）可作 LLM4SLR 任务大类基础。
- §7 七项 practical consideration 作为 Paper2 risk register 的字段种子（特别 overreliance、经验研究（empirical） eval 难题、制品 proliferation 与 project_1 / Paper2 高度对应）。

#### 6.4 绝不可迁移的领域结论
- 任何“LLM + FM 能自动保证 correctness/fairness/trustworthiness”形式的强主张。
- 任何“UPPAAL/Spin/PROMELA 是 LLM4STM 最佳工具链”这类来自示例选择的工具偏好。
- ChatGPT 3.5 在 RE 任务上的具体能力描述（作者 explicitly "slightly adjusted" 输出）。
- §2 background 分类法 不可作为 LLM4STM 主综述的工具/模型分类的事实源，只能作为术语启发。

## 证据链入口

证据链与结论-证据映射已迁移至 [evidence_chain.md](./evidence_chain.md)。
