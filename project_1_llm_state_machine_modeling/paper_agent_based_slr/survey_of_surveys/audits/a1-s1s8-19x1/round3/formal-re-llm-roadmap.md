# A1 survey-of-surveys 单篇维度抽取审计：formal-re-llm-roadmap

> 本文件是 A1 survey-of-surveys 的独立单篇审计输出，仅服务 `formal-re-llm-roadmap` 的 S1--S8 与原生维度树 / 森林复核。**不得把本文 A1 文本级抽取结果写成 final quantitative finding**；roadmap / vision 类结构数只可作为边界锚点、模式种子或 A2a 待核验入口。

## 0. 执行边界与全文阅读依据

- 已按要求读取并遵循：`ai-research-writing-skill/SKILL.md`、`research-planning/SKILL.md`、`survey_of_surveys/GUIDE.md` §6.3/§6.4。
- 未开启 sub-subagent；本审计只处理 `papers/formal-re-llm-roadmap/`。
- 已读本地材料：
  - `bibtex.bib`：确认题名、作者、IST 2025、DOI `10.1016/j.infsof.2025.107697`。
  - `metadata.json`：确认本地已标记为 `vision / roadmap`、`eligible_for_statistical_synthesis=false`、`roadmap_boundary_anchor`。
  - `paper_content.txt`：按全文顺序覆盖 Page 1--21，包括摘要、引言、背景、§3 formal software development example、§4 Roadmap A、§5 LLM-driven development example、§6 Roadmap B、§7 practical considerations、§8 conclusion、Data availability 与 References。
  - `review.md`：重点复核快速结论、全文详读、维度树复原、S1--S8 表与四分栏。
  - `evidence_chain.md`：复核 A.1--A.4 中原文类型、样本单位、分母、树型和统计池资格结论。
- PDF 核对：本轮用 `paper.pdf` 对 Fig. 2（PDF 第 9 页）与 Fig. 4（PDF 第 14 页）做了视觉核对，确认两张 roadmap 图的三层结构、圈号与 LLM / FM / SW artefact 节点；未逐页精核所有页码、图注和参考文献，仍需 A2a。

### 0.1 关键原文依据

| 依据 | 本轮读到的事实 | 对审计的作用 |
|---|---|---|
| 摘要 / Objective / Methods | 作者目标是提出两个 roadmaps：用 FMs 保障 LLM-assisted RE 的 correctness、fairness、trustworthiness；反向用 LLMs 提高 FMs 可用性。方法是两个示例 + grounded in current literature and technologies 的路线图。 | S1、S3、S7 的任务设定与候选启发来源。 |
| Introduction Page 2 | 原文明示这是 vision paper，不提供 sound empirical evidence，roadmaps 不 exhaustive，反映作者观点与经验。 | S2、S6、统计池排除的核心依据。 |
| §3 | sender-receiver / PROMELA / Spin / LTL assertion / counterexample / Python 示例。 | Roadmap A 的动机示例，不是样本库。 |
| §4 + Fig. 2 | Roadmap A：Using LLMs to support FM-based development；Fig. 2 三层为 Formal Development Layer、Conventional Development Layer、LLM Layer。 | 原生森林 Roadmap A 的主干。 |
| §4 Action Point 文本 | Roadmap A 有 5 个圈号 discussion topics，但显式 `Action Point:` 文本块为 7 条：A1 topic 下有 3 条，A2--A5 各 1 条。 | 必须区分 topic / item / action statement，避免把结构数误作样本分母。 |
| §5 | ChatGPT 3.5 示例覆盖 requirements generation、feedback analysis、smell detection、completeness / completion、model generation、classification、tracing、code-related tasks；作者说明输出经过 slightly adjusted 和 iterative prompting。 | Roadmap B 的动机示例；不能当可重复 benchmark。 |
| §6 + Fig. 4 | Roadmap B：Using FMs to support LLM-based development；三层为 Formal Layer、SW Artefact Layer、LLM Layer；LLM 任务二分 analytic / generative。 | 原生森林 Roadmap B 的主干。 |
| §6 Action Point 文本 | Roadmap B 有 7 个圈号 discussion items，且 7 条显式 `Action Point:` 文本与圈号一一对应。 | Roadmap B item / action statement 的结构复原。 |
| §7 | 七项 practical considerations：专家协作、经验评价、overreliance、人类创造力、FM 数据不足、制品增殖、部署 / 可扩展性 / 技术演进。 | 边界森林与 S8 弱证据。 |
| Data availability | “No data was used for the research described in the article.” | S2 / S6 不适用、统计池排除。 |

## 1. 总体裁决

| 项 | 审计结论 |
|---|---|
| 原文类型 | `vision / roadmap`，不是 SLR / SMS / tertiary / MLR。 |
| 是否存在系统样本库 | 否；无数据库检索、检索式、纳排、质量评价、数据抽取表、样本 ID 或编码分布。 |
| 原生结构单位 | 最稳妥写法是“roadmap topic / discussion item / Action Point statement”三层：Roadmap A 为 5 个圈号 topic、7 条显式 Action Point statement；Roadmap B 为 7 个圈号 item、7 条显式 Action Point statement；§7 为 7 项 practical consideration。 |
| 主统计池资格 | 否。5、7、14、7 等只能描述本文内部结构，不能作为系统样本分母、领域频次或 final empirical finding。 |
| A1 允许用途 | `boundary_anchor`、`schema_seed`、`candidate_finding`、`risk_only`。 |
| A2a 重点 | 精确页码 / 图注核验；逐 Action Point 建表；明确 `topic_count=12` 与 `action_statement_count=14` 的非统计语义；关系边标注 inferred。 |

## 2. S1--S8 五分栏审计

> 表中“统计池资格”只说明该维度是否可进入后续主统计池；它不同于该维度对 schema 设计是否有启发。本文所有 S 维度均不得直接写成 final quantitative finding。

| 维度 | 原文证据 | 维度树复原 | 统计池资格 | A2a 待核验 |
|---|---|---|---|---|
| S1 综述任务设定 | 摘要和 §1 明确两个目标：FM→LLM-based RE assurance 与 LLM→FM usability；§1 又明示 vision paper、非 empirical evidence、roadmaps non-exhaustive。 | 判定为**中**：任务设定清楚，但不是正式 RQ-driven review；样本单位需降级为 roadmap topics / action statements / practical considerations。 | 不进入主统计池；可作为 roadmap / vision 类型边界样本。 | 核对 §1 原文页码、贡献 bullet、vision paper 声明与 “non-exhaustive” 句子。 |
| S2 语料收集与筛选 | 原文无 search protocol、database、search string、time window、inclusion/exclusion、quality appraisal、screening flow；Data availability 声明 no data。 | 判定为**不适用**：参考文献仅是作者论证线索，不构成系统语料或 review corpus。 | 不适用；这是排除主统计池的核心维度。 | A2a 只需确认全文无 appendix / supplementary protocol；不要把参考文献列表误作语料库。 |
| S3 原生维度树 / 样本编码对象 | §4/Fig.2 给出 Roadmap A；§6/Fig.4 给出 Roadmap B；§7 给出 practical considerations。PDF 视觉核对确认 Fig.2/Fig.4 三层结构。 | 判定为**中（降级）**：原生结构是“Roadmap A + Roadmap B + §7 边界森林”。Roadmap A=5 个圈号 topic / 7 条 Action Point statement；Roadmap B=7 个圈号 item / 7 条 Action Point statement；不是 primary-study coding tree。 | 不进入主统计池；可作为原生树 / 字段树 seed。 | 必须精核 Fig.2 / Fig.4 中圈号、LLM role label、layer label；尤其修正或解释 A 侧 5 topic 与 7 Action Point statement 的双计数。 |
| S4 字段级证据 | Action Point 段落可逐条抽取 concern、mechanism、artifact in/out、recommendation、supporting refs；但无样本 ID、抽取表或样本级 evidence object。 | 判定为**中（仅 roadmap item 级）**：可以建立 action-point-level 字段表；不能冒充 study-level data extraction form。 | 不进入主统计池；可进入 pattern library seed 或 A2a 字段 schema dry-run。 | A2a 应逐 AP 建表并标注页码、段落、图中节点、是否 reviewer inferred；当前 review/evidence 仍多为树级泛定位。 |
| S5 维度模式演化 | 原文从两个 worked examples 推出 roadmaps，并引用 seminal / recent works；未报告 open coding、thematic analysis、codebook revision、冲突裁决或 saturation。 | 判定为**弱**：只有 “example → concern → mechanism → action” 的愿景构造链条，不能视为经验性 schema evolution。 | 不进入主统计池；只能作为 researcher-defined meta-model 的启发。 | 核查 §4/§6 是否有额外 roadmap construction 说明；若没有，应保持弱等级。 |
| S6 统计分析 | 原文没有频次表、比例、趋势、交叉表、模型或系统观察；Data availability 为 no data。 | 判定为**不适用**：5 / 7 / 14 / 7 只是本文内部结构数，不是领域统计结果。 | 不适用；不得把 topic/action/practical consideration 数量写入 SUMMARY 定量统计或 final finding。 | A2a 确认没有隐藏数据包；若记录结构数，字段名必须写 `roadmap_internal_structure_count` 而非 sample denominator。 |
| S7 候选 finding | §4/§6 的 Action Points 提出 RAG、NL2logic、formal prompts、formal verification、runtime monitoring、ethical requirements 等研究建议；§7 给出 overreliance、evaluation difficulty 等风险。 | 判定为**中（候选启发）**：可形成 concern→mechanism→artifact→action 的 candidate finding heuristic；全部按 roadmap/author-opinion 降级。 | 不进入主统计池；可作为候选 finding 生成规则或边界锚点。 | 逐 AP 标注 evidence strength（worked example / author opinion / cited precedent），防止写成已验证领域结论。 |
| S8 研究者 / 作者质疑与裁决 | §7 讨论专家协作、经验评价、overreliance、人类质量控制、技术演进；无多研究者筛选、编码一致性、QA 表、disagreement log。 | 判定为**弱**：仅有作者限制讨论与风险提醒，可提示 Paper2 需要 human gate / QC / override，但不是裁决机制证据。 | 不进入主统计池；可作为 risk register seed。 | 核对 §7 各小标题页码；不要把 limitation discussion 升级为 formal adjudication。 |

## 3. 原生维度树 / 维度森林复原

### 3.1 样本单位降级声明

本文没有系统样本库。按 GUIDE §6.3.4，应降级为 roadmap / vision：优先根对象为 roadmap action / vision item / challenge item。对本文更精确的单位层次是：

1. **路线图方向**：A = LLMs support FM-based development；B = FMs support LLM-based development。
2. **圈号 topic / discussion item**：Fig.2 A 侧为 5 个圈号 topic；Fig.4 B 侧为 7 个圈号 discussion items。
3. **显式 Action Point statement**：§4 A 侧为 7 条 `Action Point:` 文本块；§6 B 侧为 7 条 `Action Point:` 文本块。
4. **边界项**：§7 为 7 项 practical considerations / limitations。

这些都是**原文内部结构单位**，不是 primary study、system、tool、dataset 或实验样本。

### 3.2 原生森林

```text
[formal-re-llm-roadmap 原生降级森林]
│
├── Roadmap A：用 LLM 支持基于形式化方法的开发（Using LLMs to support FM-based development；Fig. 2）
│   ├── 图层 A-L1：Formal Development Layer
│   │   ├── Model / Formal Specification
│   │   ├── Logic Formulae / Formal Properties
│   │   ├── Counterexample
│   │   └── Formal Verification
│   ├── 图层 A-L2：Conventional Development Layer
│   │   ├── Code
│   │   ├── SW Process Artefacts（tests、docs 等）
│   │   └── Natural Language Requirements
│   ├── 图层 A-L3：LLM Layer（由多个 LLM role / agent 连接 A-L1 与 A-L2）
│   └── 圈号 topic 与 Action Point statement
│       ├── A-T1 Generating FM and SE Artifacts（圈号 1；含 3 条 AP）
│       │   ├── A-AP1a：formal specification → code；RAG 引入 existing libraries / function blocks
│       │   ├── A-AP1b：code 或 requirements → formal specification；用 summarisation / abstraction 提取 functional backbone，并利用 programming language 与 formal language 相似性
│       │   └── A-AP1c：NL requirements → logic；需要 user interaction 消歧、requirement-formula datasets、translation explanations
│       ├── A-T2 Explaining FM Artifacts（圈号 2；1 条 AP）
│       │   └── A-AP2：用 code comment generation、localized textual illustration、stack-trace analysis 等技术解释 models、formulae、counterexamples
│       ├── A-T3 Translating Formal Languages（圈号 3；1 条 AP）
│       │   └── A-AP3：利用 code-to-code translation 能力进行 model-to-model / logic-to-logic translation，适配不同 verification environments 与 audiences
│       ├── A-T4 Supporting Iterations and Evolution（圈号 4；1 条 AP）
│       │   └── A-AP4：结合 code-specific LLM 与 NL-oriented LLM 做 trace-link identification，维护 requirements / specifications / tests / code 一致性
│       └── A-T5 Automating Knowledge Engineering（圈号 5；1 条 AP）
│           └── A-AP5：从 SE artefacts 自动创建 ontologies，并反向支持 consistency checking、generation、explanation、tracing
│
├── Roadmap B：用形式化方法支持基于 LLM 的开发（Using FMs to support LLM-based development；Fig. 4）
│   ├── 图层 B-L1：Formal Layer
│   │   ├── Formal System Requirements（including Ethical）
│   │   ├── Regulatory Requirements
│   │   ├── FM Knowledge / Formal Domain Knowledge
│   │   ├── Formal Prompt(s)
│   │   ├── External Tools
│   │   ├── Formal Verification & Argumentation
│   │   └── Runtime Verification
│   ├── 图层 B-L2：SW Artefact Layer
│   │   ├── Input Requirement Artefact（system requirements、feedback、issues）
│   │   ├── Analysis of Requirement Artefact（smells、completeness、trace-links 等）
│   │   ├── Generated SW Artefact（code、tests、models、requirements 等）
│   │   └── Formal SW Artefact
│   ├── 图层 B-L3：LLM Layer
│   │   ├── Analytic Task LLMs：分析输入并产生 annotations，例如 smells、trace-links、completeness issues
│   │   └── Generative Task LLMs：生成 code、models、requirements 等新 artefacts
│   └── 7 个 discussion item / 7 条 Action Point statement
│       ├── B-AP1：通过 formal requirements、formal development process、LLM-generated explanations 与 formal argumentation structure 提升 correctness / logical coherence 并缓解 hallucinations
│       ├── B-AP2：用 specialised training、RAG、multi-LLM agents、external calculator / reasoner 支持数学约束与 formal reasoning
│       ├── B-AP3：Formal Prompt Engineering；用 formal notation / controlled NL、pre/post-conditions 与 semi-formal prompt architectures 约束 prompts 和 agent orchestration
│       ├── B-AP4：用 formal ontologies / knowledge graphs / RAG 注入 domain-specific knowledge，约束 reasoning、减少 hallucination、提高 explainability / justification
│       ├── B-AP5：用 abstraction / formal verification 近似分析 neural network / transformer 行为，验证 prompt perturbations 下 output consistency
│       ├── B-AP6：用 runtime monitoring / runtime verification 持续保证 regulatory compliance，应对 LLM knowledge 与法规演化
│       └── B-AP7：形式化 ethical requirements，桥接 values 与 formal operationalisation，用 formal techniques 验证 LLM-generated artefacts
│
├── Worked-example 动机森林（不是样本库）
│   ├── Example A：sender-receiver handshaking protocol → PROMELA model → Spin / LTL assertion → counterexample → Python code
│   └── Example B：ChatGPT 3.5 RE tasks showcase
│       ├── requirements generation
│       ├── user feedback analysis
│       ├── smell / ambiguity detection
│       ├── completeness check and requirements completion
│       ├── PlantUML sequence diagram generation
│       ├── requirements classification
│       ├── requirements tracing
│       └── code / comments / tests related tasks（简述，未展开）
│
└── §7 边界森林：Practical considerations and limitations
    ├── PC1 Collaboration Between LLM and FM Experts
    ├── PC2 Empirical Evaluation：RE / FM 数据集不足，generative outputs 无唯一 ground truth，需 qualitative methods
    ├── PC3 Overreliance on LLM Output：hallucination、machine self-confidence、human-centred quality control
    ├── PC4 Diminishing Role of Human Creativity：requirements engineers 转为 orchestrator / central role
    ├── PC5 Limited Training on FM datasets：FM data scarcity、fine-tuning、multi-model、interactive generation、agent access to model checkers / compilers
    ├── PC6 Proliferation and Maintainability of Artefacts：models、formulae、counterexamples、trace links 增殖与可视化 / analytics 需求
    └── PC7 Deployment, Scalability and Technological Evolution：state-space explosion、LLM resource demand、distillation、rapid model evolution
```

### 3.3 关系边复原

| 关系边 | 源 | 关系 | 目标 | 证据性质 | 审计边界 |
|---|---|---|---|---|---|
| edge-A-layer-mediation | Conventional artefacts / Formal artefacts | mediated_by | LLM roles / agents | Fig.2 + §4 summary | 图中显式，但具体边含义需 A2a 逐箭头核对。 |
| edge-A-transform | NL requirements / code / formal specs / logic formulae | transformed_to | formal specs / code / logic / requirements | §4 A-T1 + Fig.2 | 文本显式支持 req→logic、spec→code、code→spec；Fig.2 还出现 Logic2Req，需 A2a 精核。 |
| edge-A-explain | formal model / logic formula / counterexample | explained_as | NL explanation / comments / localized illustration | §4 A-T2 | 文本显式。 |
| edge-A-model-translation | formal language / model | translated_to | another formal language / model / abstraction view | §4 A-T3 | 文本显式；具体 tool pair 非系统枚举。 |
| edge-A-trace | requirements / specifications / tests / code / artefacts | linked_by | trace-links | §4 A-T4 | 文本显式；无 trace dataset。 |
| edge-A-knowledge | requirements / models / docs / tests | extracted_to | ontology / knowledge base | §4 A-T5 | 文本显式；ontology 再支持 consistency / generation / explanation / trace 属作者愿景。 |
| edge-B-task | input requirement artefact | processed_by | analytic / generative task LLMs | Fig.4 + §6 summary | 图与 summary 显式。 |
| edge-B-formal-control | formal layer elements | constrain_or_verify | LLM task / generated SW artefact / formal SW artefact | Fig.4 + §6 B-AP1--B-AP7 | 宏观显式，逐 AP 边需 A2a 建表。 |
| edge-B-math-support | FM knowledge / external tools / multi-agent | supports | mathematical reasoning in code generation | §6 B-AP2 | 文本显式，仍是 action recommendation。 |
| edge-B-prompt | formal prompts / pre-post conditions / UML-like architecture | constrains | generative LLM / prompt orchestration | §6 B-AP3 | 文本显式。 |
| edge-B-domain | formal ontology / knowledge graph | grounds_and_explains | domain-specific LLM reasoning/output | §6 B-AP4 | 文本显式。 |
| edge-B-consistency | abstraction / formal verification | verifies | output consistency under prompt perturbation | §6 B-AP5 | 研究建议；非已验证结果。 |
| edge-B-runtime | runtime verification | monitors | regulatory compliance during evolution | §6 B-AP6 | 研究建议；非部署证据。 |
| edge-B-ethics | formalised ethical requirements | checked_against | LLM-generated artefacts | §6 B-AP7 | 研究建议；需避免过度主张。 |
| edge-PC-constrains | practical considerations | constrain | Roadmap A/B implementation | §7 | 作者限制讨论；非 formal adjudication。 |

## 4. C/I/M 修改清单（仅作为回填建议，本文件不直接修改）

### C 级

- **暂无已进入 final quantitative finding 的 C 级问题。**当前 `review.md`、`evidence_chain.md` 与 `SUMMARY.md` 多处明确写了 “不进入主统计池 / roadmap 降级”，因此暂未发现已经把该文冒充系统样本分母的最终结论。但下列 I 级问题若被下游统计脚本或论文正文当作分母使用，会升级为 C。

### I 级

1. **I-1：`action point` 分母口径混淆，需要修正 `review.md` 与 `evidence_chain.md`。**
   - 现状：`evidence_chain.md` A.2/A.3 与 `review.md` 某些卡片把“Roadmap A 共 5 个 + Roadmap B 共 7 个 = 12 个”写成 action point 样本单位。
   - 审计结论：Roadmap A 是 **5 个圈号 topic / 7 条显式 Action Point statement**；Roadmap B 是 **7 个圈号 item / 7 条显式 Action Point statement**。因此 `12` 只可称为 `circled roadmap topic/item count`，`14` 才是 `explicit Action Point statement count`。二者都不是系统样本分母。
   - 建议：把样本单位字段改成“roadmap topic/item 与 Action Point statement 双层单位”，并在 A.3 中标注 `do_not_use_for_statistical_synthesis`。

2. **I-2：`review.md` 叶子维度表中 `leaf-action_point` 的取值空间应拆成 topic 与 statement。**
   - 现状：叶子表容易让读者理解为 A 侧只有 5 条 action point。
   - 建议新增 / 拆分为 `leaf-roadmap_topic`（A=5, B=7）与 `leaf-action_statement`（A=7, B=7），并保留 A-T1 下 3 条 statement 的父子关系。

3. **I-3：`evidence_chain.md` 仍是树级 claim map，未覆盖 S1--S8 与逐 AP 字段证据。**
   - 影响：S4/S7 的 action-point 字段目前只能靠 `review.md` 叙述支撑，不足以让 A2a 逐字段核验。
   - 建议：A2a 增补逐 AP 证据行：AP 标识、页码、段落、短引、concern、mechanism、artifact in/out、recommendation、supporting refs、evidence_strength、是否 inferred。

4. **I-4：关系边需要显式标注 `inferred_by_reviewer`。**
   - 现状：`review.md` 关系边表已说明不少边是 reviewer 从段落归纳，但 A.2/A.3 未建字段承接。
   - 建议：A2a 对每条 edge 增加“原文显式 / 图中显式 / reviewer inferred”字段；图中箭头才可标 `figure_explicit`，concern→mechanism 这类抽象边多半应标 `reviewer_inferred`。

5. **I-5：`SUMMARY.md` 中 formal-re-llm-roadmap 的 S3 行已接近正确，但应避免“5 个 discussion topics / 7 条 Action Point statements”读成 B 侧也双计数。**
   - 建议写成：“Roadmap A：5 个圈号 topic、7 条显式 AP；Roadmap B：7 个圈号 item、7 条显式 AP；§7：7 项 practical considerations；均为内部结构数，不作统计分母。”

### M 级

1. **M-1：S4 等级建议归一。** 当前 `review.md` 写“弱 / 中”，不利于 S1--S8 覆盖矩阵机器读取。建议统一为“中（仅 roadmap item 级）”或“弱（若按 sample-level 字段证据严格口径）”，并把解释写进五分栏。
2. **M-2：Fig.2 / Fig.4 的页码和图中 label 可补全。** 本轮已视觉核对 PDF 第 9 页和第 14 页，但正式 A2a 仍应记录精确图号、页码、圈号和 label。
3. **M-3：§5 ChatGPT 3.5 示例应持续标注 illustrative。** `review.md` 已提示 slightly adjusted；若后续 SUMMARY 或正文引用 LLM 能力，应再次标注它不是 benchmark / reproducible evaluation。

## 5. 本轮可交付结论

- 本文应继续作为 `roadmap_boundary_anchor`，不得进入主统计池。
- 最关键返修点不是“是否排除统计池”（当前已基本正确），而是**Roadmap A/B 的单位层次**：topic/item 与显式 Action Point statement 必须分开。
- 可迁移到 Paper2 的是 `concern → mechanism → artifact → action → risk` 的候选字段串，以及 formal / LLM 双向控制叙事；不可迁移的是任何“FM+LLM 已被证明有效 / 可保证可信”的经验结论。
