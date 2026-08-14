阅读完成。论文为 vision/roadmap 文，无系统检索/纳排/编码 schema；以下为完整审计报告。

---

# A1-DT v2 单篇审计报告：formal-re-llm-roadmap

## 0. 审计结论卡片

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
| 总体判定 | **needs repair**：现有 review.md 在“维度树复原”小节仍把六个跨论文通用接口叶子（scope/corpus/taxonomy/method/evidence/finding）摆成主树骨架，导致原文真实结构（双 roadmap × 3 layer × N action point × concern/mechanism/artifact 子字段）被压低为投影；19×3 返修虽已加“原文 schema 主树”，但 6 个原文主干粒度过粗、未对齐到 12 action points 与 3 layers，需进一步精修 |

## 1. 原文证据阅读说明

- **实读文件**：`bibtex.bib`、`metadata.json`、`paper_content.txt`（全 2517 行三段读完）、`review.md`（全 480 行两段读完）。`paper.pdf` 本轮未打开（属本审计的 transparency 项，需 A2a 复核排版级证据）。
- **技能文件**：均已读取：`ai-research-writing-skill/SKILL.md`、`reviewer-guidelines.md`、`reviewer-self-review.md`、`research-planning/SKILL.md`、`planning-prompts.md`、`output-schemas.md`、`autoresearch/SKILL.md`。所用核心原则：claim-evidence gate、reviewer 5-dim、5-dim 自评、reviewer constructive specificity、autoresearch validator-gated 边界判定。
- **覆盖章节**：Abstract、§1 Introduction、§2 Background (含 §2.1 LMs/LLMs in RE、§2.2 Formal RE)、§3 Example A (PROMELA)、§4 Roadmap A、§5 Example B (ChatGPT)、§6 Roadmap B、§7 Practical considerations、§8 Conclusion、CRediT、Data availability、References（175 条）。

### 关键证据锚点（约 10 条）

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

## 2. 样本单位与字段来源判定

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

## 3. 原生样本编码维度树 / 维度森林

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

## 4. 叶子维度表

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

## 5. 关系边表

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

## 6. 统计观察、候选 finding 与 final finding 边界

### 6.1 由字段 / 统计表支持的统计观察
**无**。本文不含任何统计表、频次表、Q&A 表或 coding distribution。作者明确 "No data was used"（§Data availability）。

### 6.2 作者 discussion / roadmap 提出的候选 finding（每条均为 candidate，evidence_strength ≤ worked_example_only）
- CF-1：LLM 的 code-summarisation 能力可被借用于 code→formal spec 抽象，以缓解 state-space explosion（AP-A1）。
- CF-2：counterexample 的解释难度类似 stack-trace，可借用 LLM 的 trace-explain 思路（AP-A2，引 [132]）。
- CF-3：FM diversity 可通过 LLM 驱动的 model-to-model translation 维持（AP-A3）。
- CF-4：trace-link 由 code-specific LLM + NL-oriented LLM 联合更可靠（AP-A4）。
- CF-5：LLM 的数学推理瓶颈未必能靠规模扩张解决，需要外挂 formal/calc 资源（AP-B2，引 [151]）。
- CF-6：prompt 即“需求”，应引入 ACSL-style pre/post-condition（AP-B3）。
- CF-7：abstract interpretation 在 NN/transformer 上的应用是缓解 LLM 不可重复性的可行路径（AP-B5）。
- CF-8：regulatory compliance 必须从一次性证明转为 runtime monitoring（AP-B6）。
- CF-9：ethical/fairness 必须先 formalise 为 requirement，再用 formal techniques 验证（AP-B7）。

### 6.3 对 Paper2 可迁移的方法学启发
- 双向 roadmap 叙事（LLM 帮 X / X 帮 LLM）作为 Paper2 第二篇的结构 seed。
- “concern → mechanism → artifact → action” 字段串作为 candidate-finding 表的字段约束。
- "analytic vs generative" 二分（E9）可作 LLM4SLR 任务大类基础。
- §7 七项 practical consideration 作为 Paper2 risk register 的字段种子（特别 overreliance、empirical eval 难题、artifact proliferation 与 project_1 / Paper2 高度对应）。

### 6.4 绝不可迁移的领域结论
- 任何“LLM + FM 能自动保证 correctness/fairness/trustworthiness”形式的强主张。
- 任何“UPPAAL/Spin/PROMELA 是 LLM4STM 最佳工具链”这类来自示例选择的工具偏好。
- ChatGPT 3.5 在 RE 任务上的具体能力描述（作者 explicitly "slightly adjusted" 输出）。
- §2 background taxonomy 不可作为 LLM4STM 主综述的工具/模型分类的事实源，只能作为术语启发。

## 7. 对现有 `review.md` 的返修建议

按 C / I / M 分级，**严重性以学术目标 / Paper2 证据链可靠性为锚**：

### C（critical）— 阻塞合并到 Paper2 主线

无。本文 review.md 已在最近一轮 PR-A1-DT v2 19×3 返修中正确判定 `eligible_for_statistical_synthesis=false` 与 `evidence_role=boundary_anchor`，不会污染主统计池。

### I（important）— 影响 schema seed 质量、需在 A2a 前修

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
4. **I-4：现有 review.md 把 Section 7 当成“限制”而未结构化为 boundary forest 主干**（在“3.8 局限与实践考虑”中只做散述）；应在维度树复原节内显式列为 7 个 leaf-practical_consideration，与 leaf-concern 区分开（PC 是 process / org / human-side，concern 是 technical-side）。

### M（minor）— 学术影响低，可后续

1. **M-1**：CCF 复核状态字段标注 “WAF”，建议改为 “待核验（HTTP 403/Aliyun WAF）”，措辞更精确。
2. **M-2**：review.md §1 卡片“证据等级”列写“两张 roadmap 图为 原文图表级人工核对”，但本审计与 review.md 各自均**未真的打开 PDF**，应改为“仅文本级（Fig. 2 / Fig. 4 由文本中的 figure caption 与 Summary 段定位）”。
3. **M-3**：A.4 复验清单只有 2 项，建议补充“action point 计数复验”（A=5 个、B=7 个、PC=7 个）等可自动检查项。

### SUMMARY.md 相关行须修正项
- 样本单位 / 样本数量：应保持 `not_applicable`（roadmap），并显式注明 “Roadmap A action points = 5; Roadmap B = 7; PC = 7（皆为作者构造，非编码样本）”。
- 原生树类型：应改为 “**降级森林（双根 roadmap 森林 + 边界森林）**”，而不是单树。
- 统计池资格：保持 `否（boundary_anchor）`，理由列保留现状。

## 8. 审计附录草案：证据账本与结论映射

下两表可直接替换 / 扩充 review.md 现 A.2 / A.3。

### A.2 维度树证据账本草案（扩充至 ≥ 10 条）

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

### A.3 结论-证据映射草案

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

## 9. 技能使用与自我审查记录

### 9.1 所用技能与采纳的原则
| 技能 / 文件 | 已读 | 采用要点 |
|---|---|---|
| `ai-research-writing-skill/SKILL.md` | ✓ | claim-evidence gate（C/I/M 严格按学术目标定级）；Evidence policy（不臆造引用 / 数字） |
| `reviewer-guidelines.md` | ✓ | constructive specificity（每条返修都给出位置与可执行动作）；review 五维 |
| `reviewer-self-review.md` | ✓ | 五维自评（Contribution / Clarity / Experiment / Eval / Method / Responsibility）；adversarial questions；claim audit 格式 |
| `research-planning/SKILL.md` + `planning-prompts.md` + `output-schemas.md` | ✓ | 用 schema-first 思路区分 “原文 schema” vs “Paper2 desired schema”；保留 unclear 标记 |
| `autoresearch/SKILL.md` | ✓ | validator-gated 边界：只有具备显式可验证 artifact 的内容才算 verified；本文除作者声明外不构成 validator 满足 |
| ARS reviewer plugin（系统已加载） | ✓（仅元数据） | 不调用，遵守任务 §0 不启动 subagent 的硬约束 |

### 9.2 reviewer 视角的最高风险 3 点（主线程合并时务必复核）
1. **R-1（高）**：本审计未打开 `paper.pdf`。Fig. 2 / Fig. 4 的“三层”、AP 编号位置、boxed Action Point 文本是否与文本完全一致，**仍需主线程或 A2a 用 PDF 版面核验**。若 PDF 标签与文本叙述差异（例如图层重命名、AP 顺序调整），上表 leaf-layer 与 leaf-action_point 的枚举可能需要微调。
2. **R-2（中）**：每条 action point 的 concern / mechanism / artifact 子字段，是 reviewer 在通读段落后归纳的“准 schema”，不是作者显式列出的字段。主线程在重写 review.md 时应在叶子表里**显式标注** `inferred_by_reviewer=true`，并把这部分提取动作正式委派给 A2a 精核。
3. **R-3（中）**：候选 finding（CF-1..CF-9）只是 candidate；它们在 vision paper 内只有 author-opinion 级强度，但易被下游 LLM agent 误升级为 “研究共识”。主线程应在 Paper2 的 candidate-finding 库中对每条 CF 标注 `evidence_strength=author_opinion`，并要求 Paper2 提供独立证据反复验证后才能升级。

### 9.3 阻塞 / 超时 / 文件缺失
- **No blocked**：7 个技能文件 + 4 个论文文件均成功读取。
- **transparency 说明**：`paper.pdf` 本轮未打开，已在卡片与 A.2 表中显式标注；不算 blocked，但是 transparent gap，A2a 必须完成 PDF 复核。
- **无 timeout**。
- **总判定**：`pass with I-level repair` — 维度树结构与候选发现边界已锁定，review.md 与 A.2/A.3 需按 I-1..I-4 返修后即可合并至 Paper2 主线。

---

**报告结束。**
