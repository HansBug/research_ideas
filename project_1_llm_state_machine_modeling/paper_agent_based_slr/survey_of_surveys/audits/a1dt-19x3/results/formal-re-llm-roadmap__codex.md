# formal-re-llm-roadmap · codex 全文审计报告

## 1. 审计身份与输入

- reviewer 身份：codex reviewer（codex）
- 是否读取 `$ai-research-writing-skill`：是；读取 `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`，并读取 `references/paper-story.md`、`references/reviewer-guidelines.md`、`references/reviewer-self-review.md`。采用 claim-evidence、roadmap 不得升级为完成型 finding、强主张必须降级的口径。
- 是否读取 `$research-planning`：是；读取 `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md` 与 `references/planning-prompts.md`。采用“严格对齐原文、不可臆造、模糊处显式标注”的复原口径。
- 是否读取 `$oh-my-codex:autoresearch`：是；读取 `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`。采用 artifact-gated、validator-evidence-gated 的完成口径；本次未启动 autoresearch workflow。
- 是否读取文库级规则与 story：是；读取 `survey_of_surveys/README.md`、`GUIDE.md`、`SUMMARY.md`、`patterns/pattern-field-schema.md` 与 `paper_agent_based_slr/story/paper_story.md`。核心约束是：roadmap / vision 只能作 schema seed / boundary anchor，不进入主统计池；维度树必须从原文 RQ / 贡献 / roadmap figure / action point / evidence chain 推导。
- 是否完整阅读 `paper_content.txt`：是；已覆盖 `paper_content.txt` 全部 2516 行 / PDF 1--21 页，包括摘要、引言、背景、两个 worked examples、Fig. 2 / Fig. 4 对应 roadmap、Section 7 limitations、结论、Data availability 与参考文献。
- 是否核对 `paper.pdf`：是，有限核对；通过 `pdfinfo` 确认 21 页，通过 `pdftoppm` 渲染第 9 页与第 14 页，视觉核对 Fig. 2 与 Fig. 4 的层级、节点与关系。未逐项视觉核对所有代码清单、参考文献和版面页码，因此这些细节仍应在 A2a 精核。

## 2. 原文真实结构复原

### 原文 RQ / 目标 / 贡献声明

原文没有显式编号 RQ。真实根问题是双向 roadmap：一方面用形式化方法为 LLM 用于 RE 活动提供 correctness、fairness、trustworthiness 保障；另一方面用 LLM 提高 formal RE / FM 的可用性与可理解性。该目标在摘要 Objective / Methods / Results 中直接说明：用两组示例揭示 FM 与 LLM 在软件开发 / RE 中的局限，并提出两个 roadmaps（`paper_content.txt:31-43`）。

引言贡献声明进一步给出四项贡献：LLM 与 RE / formal RE 背景；LLM 支持 FM-based development 的 roadmap；formal RE 克服 LLM-based RE 限制的 roadmap；roadmap 实践实现的 risks / limitations（`paper_content.txt:90-102`）。原文同时明示这是 vision paper，不提供 sound empirical evidence，roadmaps 不应被视为 exhaustive，反映作者经验与观点（`paper_content.txt:103-115`）。

因此，维度树根节点应是“Formal RE 与 LLM 的双向路线图”，而不是普通 SLR/SMS 的 RQ tree 或 extraction schema。

### 原文方法流程、检索 / 纳排 / 数据抽取 / 编码 / 统计 / finding 形成方式

原文不是 SLR、SMS 或 tertiary study，没有系统检索、纳排、数据抽取表、编码流程、质量评价或统计综合。其形成方式是：

1. 背景综述：概述 LLM / RE 与 formal RE，包括 LLM 技术、RE 任务、formal specification、formal properties、formal models、formal analysis methods（`paper_content.txt:116-623`）。
2. Worked example A：sender-receiver handshaking protocol，从 NL requirements 到 PROMELA model、LTL assertion、Spin verification、counterexample、Python implementation，展示 formal process 的强度与复杂性（`paper_content.txt:624-933`）。
3. Roadmap A：基于示例与相关文献提出 “Using LLMs to support FM-based development”，包含 Fig. 2 的三层结构和 5 个 action points（`paper_content.txt:934-1221`）。
4. Worked example B：用 ChatGPT 3.5 展示 requirements generation、feedback analysis、smell detection、completeness check / completion、model generation、classification、tracing、code-related tasks；原文说明输出经过轻微压缩和有限调整，部分图需多轮提示（`paper_content.txt:1223-1538`）。
5. Roadmap B：提出 “Using FMs to support LLM-based development”，包含 Fig. 4 的三层结构和 7 个 action points（`paper_content.txt:1539-1807`）。
6. Practical considerations and limitations：用 7 类风险约束 vision 的外推（`paper_content.txt:1808-1955`）。
7. 结论：两条路线图用于激发研究；作者后续重点是 req-to-logic translation、LLM 生成/分析 artefacts、LLM 解释 formal artefacts（`paper_content.txt:1956-1982`）。Data availability 明确 No data was used（`paper_content.txt:2009-2010`）。

原文 finding 不是经验 finding，而是“示例揭示问题 → action point → roadmap → limitation”的 vision synthesis。任何 Paper2 复用都必须降级为 schema seed / candidate heuristic / boundary anchor。

### 原文显式 extraction form、classification schema、taxonomy、coding scheme、模型、图表、roadmap 或 quality rubric

原文没有 extraction form、coding scheme、quality rubric、PRISMA flow、统计表或 evidence table。

原文有多类可复原结构：

- 背景 taxonomy：formal specification languages、property logics、formal models、formal analysis methods；其中 formal models 包含 LTS、FSM、Büchi automata、Timed Automata、Probabilistic / Stochastic State Machines、Statecharts、Petri Nets 等，贴近本仓库状态机方向。
- Worked-example artefact chain：NL requirements、PROMELA listings、LTL assertion、Spin counterexample Fig. 1、Python sender / receiver code listings。
- Fig. 2 Roadmap A：三层为 Formal Development Layer、Conventional Development Layer、LLM Layer；显式节点包括 Model / Formal Specification、Logic Formulae / Formal Properties、Formal Verification、Counterexample、Code、SW Process Artifacts、Natural Language Requirements，以及 Model2Code、Code2Model、Req2Logic、Logic2Req、Explanation LLM、Model2Model LLM、Knowledge Representation LLM、Trace-link LLM。
- Section 4 的 5 个 action points：Generating FM and SE Artifacts；Explaining FM Artifacts；Translating Formal Languages；Supporting Iterations and Evolution；Automating Knowledge Engineering。
- Fig. 4 Roadmap B：三层为 Formal Layer、SW Artefact Layer、LLM Layer；显式节点包括 Formalised System Requirements、External Tools、FM Knowledge、Formal Domain Knowledge、Formal Prompts、Formalised Requirements including Ethical Requirements、Runtime Verification、Analytic Task LLMs、Generative Task LLMs、Input Requirement Artefacts、Generated SW Artefacts、Formal SW Artefact。
- Section 6 的 7 个 action points：formal requirements and argumentation；formal LLMs / RAG / tools for mathematical reasoning；formal prompt engineering；formal domain knowledge / knowledge graphs；formal verification of output consistency；runtime regulatory compliance；ethical requirements / bias / fairness.
- Section 7 limitations：LLM-FM expert collaboration、empirical evaluation、overreliance、human creativity / human role、limited FM datasets、artefact proliferation / maintainability、deployment / scalability / technological evolution。

### 原文如何从字段 / 统计观察形成 conclusion / finding / gap / recommendation

原文没有字段表和统计观察。它通过两个示例暴露限制，再把限制映射到 action points，并用文献锚点论证 plausibility。结论强度应是 vision / roadmap / research agenda，不是 empirical finding。对 Paper2 可迁移的是“concern → artefact/task → mechanism → validation need / limitation → action point”的候选发现路径。

## 3. 当前 `review.md` 维度树审计

| 检查项 | 结论 | 证据 / 理由 | 严重度 |
|---|---|---|---|
| 根节点是否准确 | 基本准确但过泛 | 当前根写成 `Formal requirements engineering and large language models`，能覆盖题名与主题；但应显式写成“双向 roadmap：LLM 支持 FM-based development / FM 支持 LLM-based RE”。否则后续主干容易退化成普通六类 review interface。 | M |
| 主干分支是否覆盖原文 schema | 未通过 | 当前主干为 `roadmap direction / layer / task family / assurance concern / human gate limitation`，方向上接近，但没有把原文两个 roadmap 作为一级结构，也没有保留 Fig. 2 / Fig. 4 的三层、artefact 节点、LLM role、formal mechanism、action point 编号和 limitation 分类。 | C |
| 叶子维度是否足够具体 | 未通过 | 当前“叶子维度表”的 6 个 leaf 是跨论文通用接口；虽然 `review.md` 已声明它们不是原文叶子全集，但 A.3 又把这些 leaf 写成“来自本文”的候选节点。原文模式候选叶子只有 4 行，明显小于原文 5+7 action points、两张 roadmap 图和 Section 7 limitation。 | C |
| 取值空间是否可执行 | 不足 | 多数取值空间写成“自由文本”“层级枚举”“待核验”，没有给出原文可执行枚举：2 个 roadmap direction、Fig. 2/4 layer、5+7 action point、artefact input/output、LLM role、formal mechanism、concern、evaluation need、limitation type。A2a 不能据此稳定抽取。 | I |
| 关系边是否缺失 | 缺失 | 原文两张图本质是关系型 roadmap：LLM role 与 artefact、formal layer 与 SW artefact、formal mechanism 与 concern 之间有方向关系。当前没有关系边表，无法表达 Model2Code、Code2Model、Req2Logic、Formal prompts → generated code constraints、Runtime verification → regulatory compliance 等边。 | I |
| 统计用途 / 分母是否正确 | 大方向正确但需收紧 | 当前正确排除主统计池，符合 `metadata.json` 和 GUIDE；但 `leaf-taxonomy` 仍写“分类项频次 / 交叉表 / 主题分布”，分母却是 `not_applicable`，容易被 A2a 误读。应统一写“不作单篇统计；仅记录 schema seed；跨文库只可统计树型/证据角色”。 | M |
| 候选 finding 路径是否完整 | 不完整 | 当前只写“候选发现需研究者裁决”，没有结构化原文的 concern-to-action path。原文可提供更强路径：concern / limitation → task or artefact → mechanism → action point → evaluation need / human gate → limitation。 | I |
| A.1--A.4 证据链是否足够 | 结构存在，证据不足 | A.1--A.4 表头齐全；但 A.2 只有 4 条大粒度证据，页码、章节、行号和图号大量写“待复核”“见释义”。Fig. 2 / Fig. 4 已可局部核对，却没有拆成独立证据行。A.3 中 C02--C07 使用同一泛证据支撑通用 leaf，证据粒度不足。 | I |
| 是否存在可能误导 A2a 的强主张 | 存在中等风险 | 正文多处正确降级为 `weak` / `not_verified` / `boundary_anchor`，但“六个通用 leaf 来自本文”的 A.3 写法、快速卡片“Fig.2/Fig.4 已回 PDF 图片核对”与 A.4 `needs_manual_check` 的不一致，可能让 A2a 误以为原文 schema 已经复原。 | I |

## 4. 建议维度树骨架

当前 `review.md` 不足以作为完整原文 schema 复原。建议把“通用 6 leaf interface”移到兼容层或审计 checklist，把原文真实结构作为主树。

| 节点 / 叶子标识 | 建议名称 | 父节点 | 候选取值空间 | 是否可统计 | 缺失值语义 | 证据来源定位 |
|---|---|---|---|---|---|---|
| `dim-formal-re-llm-roadmap-root` | Formal RE 与 LLM 的双向 roadmap | -- | two-way roadmap | 否；boundary anchor | `not_applicable_to_slr_stats` | 摘要 Objective / Methods / Results；Intro contributions；`paper_content.txt:31-43`, `90-115` |
| `dim-formal-re-llm-roadmap-direction-a` | Roadmap A：LLM 支持 FM-based development | root | `LLM_for_FM_usability` | 否 | `vision_roadmap` | Section 4；Fig. 2；`paper_content.txt:934-1221` |
| `dim-formal-re-llm-roadmap-direction-b` | Roadmap B：FM 支持 LLM-based development | root | `FM_for_LLM_trustworthiness` | 否 | `vision_roadmap` | Section 6；Fig. 4；`paper_content.txt:1539-1807` |
| `leaf-formal-re-llm-roadmap-a-layer` | Roadmap A layer | direction-a | Formal Development Layer；Conventional Development Layer；LLM Layer | 可作 schema seed 枚举，不作领域统计 | `not_in_figure` / `not_verified` | Fig. 2；Section 4 summary；`paper_content.txt:1203-1221` |
| `leaf-formal-re-llm-roadmap-a-artefact` | Roadmap A artefact node | direction-a | model / formal specification；logic formulae / formal properties；counterexample；code；SW process artefacts；NL requirements | 可作节点枚举；不作主统计 | `not_in_figure` / `not_verified` | Fig. 2 PDF 核对；Section 4 summary |
| `leaf-formal-re-llm-roadmap-a-llm-role` | Roadmap A LLM role | direction-a | Model2Code；Code2Model；Req2Logic；Logic2Req；Explanation LLM；Model2Model LLM；Knowledge Representation LLM；Trace-link LLM | 可作 schema seed | `not_in_figure` / `not_verified` | Fig. 2 PDF 核对 |
| `leaf-formal-re-llm-roadmap-a-action-point` | Roadmap A action point | direction-a | generating FM/SE artefacts；explaining FM artefacts；translating formal languages；supporting iterations/evolution；automating knowledge engineering | 可作 action-point 枚举；不作 empirical finding | `not_reported` / `not_verified` | Section 4 headings/action points；`paper_content.txt:955`, `1111`, `1143`, `1167`, `1191` |
| `leaf-formal-re-llm-roadmap-a-mechanism` | Roadmap A mechanism | direction-a | RAG；code summarisation / abstraction；NL-to-logic with human disambiguation；explanation generation；code-to-code / model-to-model translation；trace-link identification；ontology engineering | schema seed | `not_reported` | Section 4 paragraphs |
| `leaf-formal-re-llm-roadmap-a-risk` | Roadmap A limitation / validation need | direction-a | limited FM data；state-space explosion；trace maintainability；need explanation quality checks；need human iteration | candidate risk only | `not_reported` | Section 4 + Section 7 |
| `leaf-formal-re-llm-roadmap-b-layer` | Roadmap B layer | direction-b | Formal Layer；SW Artefact Layer；LLM Layer | schema seed | `not_in_figure` / `not_verified` | Fig. 4；Section 6 summary；`paper_content.txt:1780-1807` |
| `leaf-formal-re-llm-roadmap-b-task-type` | LLM task type | direction-b | analytic task LLMs；generative task LLMs | schema seed | `not_in_figure` | Fig. 4；Section 6 summary |
| `leaf-formal-re-llm-roadmap-b-artefact` | Roadmap B artefact node | direction-b | input requirement artefacts；generated SW artefacts；formal SW artefact；formalised system requirements；formal prompts；formal domain knowledge；FM knowledge；external tools；runtime verification；ethical requirements | schema seed | `not_in_figure` / `not_verified` | Fig. 4 PDF 核对 |
| `leaf-formal-re-llm-roadmap-b-concern` | Trustworthiness / assurance concern | direction-b | correctness；hallucination；logical coherence；mathematical reasoning；prompt ambiguity；domain grounding；output consistency；regulatory compliance；bias；ethics；privacy；fairness；robustness | candidate concern taxonomy | `not_reported` / `not_verified` | Section 6 action points；Section 7 risks |
| `leaf-formal-re-llm-roadmap-b-mechanism` | Formal assurance mechanism | direction-b | formal requirements；formal verification；formal argumentation；formal LLM / RAG / external reasoner；formal prompt / pre-post condition；ontology / knowledge graph；abstract interpretation / abstraction；runtime monitoring；ethical requirement formalisation | schema seed | `not_reported` | Section 6 |
| `leaf-formal-re-llm-roadmap-b-action-point` | Roadmap B action point | direction-b | 7 个 Section 6 action points | action-point seed；不作 empirical finding | `not_reported` / `not_verified` | `paper_content.txt:1599`, `1633`, `1668`, `1710`, `1744`, `1765`, `1777` |
| `leaf-formal-re-llm-roadmap-example-type` | Worked-example evidence type | root | FM development example；LLM-driven RE example；prompt/output excerpt；code listing；counterexample；roadmap figure；literature anchor | 只作 evidence type，不作统计 | `not_applicable` | Sections 3 and 5 |
| `leaf-formal-re-llm-roadmap-evaluation-status` | Evaluation / data status | root | no empirical evidence；no systematic review；no data used；illustrative examples；literature-grounded proposal；qualitative evaluation need | 否 | `not_applicable_to_stats` | Intro caveat；Data availability；Section 7 empirical evaluation |
| `leaf-formal-re-llm-roadmap-limitation` | Practical consideration / limitation | root | collaboration；empirical evaluation；overreliance；human role；limited FM datasets；artefact maintainability；deployment/scalability/technology evolution | candidate risk taxonomy | `not_reported` | Section 7；`paper_content.txt:1808-1955` |

关系边建议至少补以下类型：

| 关系边类型 | 源 | 目标 | 缺失值语义 | 证据来源 |
|---|---|---|---|---|
| `translates_between` | LLM role | artefact in/out | `no_linked_artefact` | Fig. 2 / Fig. 4 |
| `supports_action_point` | mechanism | action point | `not_reported` | Section 4 / 6 action point paragraphs |
| `mitigates_concern` | formal mechanism | assurance concern | `not_claimed` | Section 6 |
| `requires_validation` | action point | evaluation need / limitation | `not_reported` | Section 7 |
| `evidence_from_example` | example artefact | roadmap action point | `illustrative_only` | Sections 3 / 5 |
| `human_gate_needed` | action point / concern | human role / quality control | `not_applicable` | Section 7 overreliance and human role |

## 5. 必须补充 / 修正清单

| 修复项 | 建议修改位置 | 具体修改建议 | 证据来源 | 严重度 |
|---|---|---|---|---|
| 重建主树为“双向 roadmap” | `review.md` 的 `## 维度树复原` / `维度树结构` | 把一级分支改为 Roadmap A 与 Roadmap B；当前 `roadmap direction/layer/task/concern/human gate` 可作为二级 field axis，而不是主树唯一结构。 | 摘要 Objective/Methods/Results；Intro contributions；Sections 4/6；Fig. 2/4 | C |
| 将通用 6 leaf 从“原文叶子”降级为兼容接口 | `叶子维度表` 与 A.3 C02--C07 | 明确这些 leaf 是 review 兼容层，不作为原文 leaf_definition 结论；A.3 中不要写“来自本文”，改成 `compatibility_interface` 或移出主结论表。 | GUIDE 6.3；当前 `review.md` 已自称 6 leaf 不是原文全集，但 A.3 又反向升级 | C |
| 补全原文候选叶子 | `原文模式候选叶子映射（A1 种子）` | 至少补入 2 个 roadmap direction、5 个 Roadmap A action points、7 个 Roadmap B action points、Fig. 2/4 layer、artefact、LLM role、mechanism、concern、evaluation status、limitations。每项给取值空间、缺失语义、统计用途。 | Fig. 2 / Fig. 4；Section 4/6 action point headings；Section 7 | C |
| 增加关系边表 | `维度树复原` 中新增 `关系边表` | 记录 LLM role ↔ artefact、mechanism → action point、formal mechanism → concern、action point → validation need、example → roadmap 的关系。缺失关系也要有 `not_reported` / `illustrative_only` 语义。 | Fig. 2/4 是关系图，不是单纯 taxonomy | I |
| 修正 corpus / extraction / quality / artifact 字段语义 | `leaf-corpus`、`leaf-evidence`、统计链路、A.3 | 对本文应写：无系统检索、无纳排、无 extraction form、无 quality rubric、无数据、无统计；证据资产是 illustrative examples、listings、figures、references、Data availability=no data。 | `paper_content.txt:103-115`, `2009-2010` | I |
| 拆分 A.2 证据账本 | A.2 | 至少拆为：objective/contribution；vision caveat；Fig. 2；Roadmap A action points；Section 5 ChatGPT adjustment caveat；Fig. 4；Roadmap B action points；Section 7 limitations；Data availability。每行给页码 / 行号 / 图号。 | 当前 A.2 仅 4 条泛证据，不能支撑具体 leaf | I |
| 修正 PDF 核对状态不一致 | 快速结论卡片与 A.4 | 若 Fig. 2 / Fig. 4 已核对，则 A.4 对相应证据应拆成 `passed`；若还需逐项图内 label 精核，则快速卡片不要写成已完成图表级证据。 | 本次审计已渲染核对 Fig. 2 / Fig. 4；其他表/代码未全核 | M |
| 保留 roadmap 降级并防止 final finding 升级 | 统计与候选发现链路 / A.3 | 保持 `eligible_for_statistical_synthesis=false`；所有 action point 允许用途只写 `schema_seed` / `boundary_anchor` / `candidate_finding` / `risk_only`，不得写 `statistical_synthesis`。 | 文库 GUIDE 6.3.5；原文 vision caveat | 通过 |

## 6. C/I/M 结论

- C：2 项。当前维度树主干和叶子层没有忠实复原原文双向 roadmap、Fig. 2/Fig. 4 和 5+7 action points；通用 6 个 leaf interface 仍在事实真源中占据主树位置，会直接削弱 Paper2 后续 A2a/A2b 的 schema seed 可靠性。
- I：5 项。取值空间不可执行、关系边缺失、candidate finding 路径不完整、A.1--A.4 证据粒度不足、roadmap 的 corpus / quality / artifact / no-data 语义未完全落到维度树。
- M：2 项。根节点需更精确表达 two-way roadmap；PDF 核对状态需要与 A.4 一致。
- 最终建议：NEEDS FIX。

当前 `review.md` 的全文摘要部分质量较好，且已正确识别本文不是 SLR/SMS、不能进入主统计池；问题集中在 `## 维度树复原` 事实真源。最小修复不是重写整篇 review，而是把已有历史草稿中的细字段正式迁移进维度树主表、补 Fig. 2/Fig. 4 关系边和 A.2 证据拆分，并把通用 6 leaf 明确降级为兼容检查接口。
