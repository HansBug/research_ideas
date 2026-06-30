### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `interactive-llm-systematic-mapping` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；完整读取 280 行全文抽取文本，并用行号复核关键段落 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；`bibtex.bib` 记录 IST 178, 2025, DOI；`metadata.json` 记录 online-first/本地资格判断 |
| 是否打开或核对 `paper.pdf` | 是；用 `pdfinfo` 确认 4 页，并渲染 PDF 第 2 页视觉核验 Fig. 1 |
| 原文类型 | proposal；原文自称 solution proposal，不是已执行的 SLR/SMS/tertiary/MLR |
| 被编码样本单位 | 无系统样本库；降级对象是“LLM-supported mapping process”的流程阶段、agent 角色、交互动作和 proposal guideline item |
| 样本数量 / 分母 | 无 primary/secondary study 分母；可记录的设计元素包括 Fig. 1 的 5 个流程阶段、§2.2.1 的 3 个 search agents、§2.3 的 2 类 coding modes，但这些不是实证样本数 |
| 原生树类型 | 降级树 / 方法流程维度森林 |
| 主统计池资格 | 否；只能作 `boundary_anchor` / `schema_seed` / 方法学启发，不进入主统计池 |
| 总体判定 | needs repair；现有 `review.md` 有可用材料，但仍混入六叶通用投影和旧 v1 审计口径，需按原文流程树重写核心维度树 |

### 1. 原文证据阅读说明

本次实际读取并使用了：

- `bibtex.bib`：核对题名、作者、IST 卷期、年份、DOI。
- `metadata.json`：核对本地记录的 proposal 类型、统计池排除理由、fulltext 状态。
- `paper_content.txt`：完整阅读全文抽取文本。
- `review.md`：完整阅读作为返修对象，不作为原生树事实源。
- `paper.pdf`：打开元数据并渲染第 2 页核对 Fig. 1。未打开 supplementary material，因此下划线术语定义不进入已核验证据。

关键证据锚点：

1. 摘要：Objective 是讨论 LLM 在 mapping process 中的可能性，Method 明确为 solution proposal。
2. 引言：mapping study 用于分类研究和观察趋势，SLR 更偏证据综合。
3. 引言：作者提出 LLM 动机，包括研究量增加、扩大范围、辅助研究设计、降低更新成本。
4. 引言：作者明确采用 human-in-the-loop，研究者需懂 mapping 方法并是主题专家。
5. §2 开头：Fig. 1 展示 review process 各步、用户输入/动作、LLM 输出。
6. Fig. 1：五个阶段为 need/review、study identification、data extraction、visualization、reporting。
7. §2.1：LLM 生成 research questions 和补充目标，人类编辑后进入下一步。
8. §2.2.1：搜索策略需透明、可复现；提出 Keyword Identification、Semantic Search、Search Strategy 三类 agent。
9. §2.2.2：纳排是分类问题，但需要理由、引用和可追踪性。
10. §2.3：数据抽取分 inductive coding 与 deductive coding；deductive 可用完整 PDF 与 RAG。
11. §2.4--2.5：LLM 可辅助可视化和报告中的 pattern/gap spotting。
12. §3 与 Data availability：现有证据有限、模型快速演化、需 SE-specific evaluation；原文声明未使用数据。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象不是 primary study、secondary study 或工具样本库，而是一个拟议的 LLM-supported systematic mapping process。逐项描述对象是流程阶段、每阶段用户输入、交互修订、LLM 输出，以及若干技术角色。
2. 作者没有执行系统检索、纳排、质量评价、数据抽取或编码统计。参考文献 [5]--[9] 是 narrative support，不构成本论文的样本分母。
3. 原文字段来源主要是 Fig. 1、§2 的流程小节、§2.2.1 的 agent 枚举、§2.3 的 coding mode 枚举、§3 的 reflection/risk。没有 extraction form、quality rubric、mapping table、replication package。
4. RQ 不是树根。RQ 在本文中既是 stage 1 的 LLM 输出，也是后续 stage 的输入；真正的根对象是“LLM 如何支持 mapping study 流程”。
5. 因无系统样本库，必须降级为 boundary anchor / methodological seed / candidate heuristic；不能进入主统计池，不能产生领域统计结论。

### 3. 原生样本编码维度树 / 维度森林

```text
root: LLM-supported mapping process proposal
├── stage: Establish a need for the review/map
│   ├── activity: formulate gap, research goals, research questions
│   ├── user_input: research objective + request refinements/additions
│   ├── interactive_refinement: edit suggested questions until acceptable
│   └── llm_output: candidate research questions supporting the goal
├── stage: Study identification
│   ├── activity: search and study selection
│   ├── user_input: objective/questions, search terms, inclusion/exclusion criteria, paper metadata
│   ├── search_agents
│   │   ├── Keyword Identification Agent
│   │   ├── Semantic Search Agent
│   │   └── Search Strategy Agent
│   ├── selection_schema: include / exclude / final verdict with rationale and confidence
│   ├── interactive_refinement: pilot, iterate, update searches and criteria
│   └── llm_output: search strings, criteria suggestions, structured assessment output
├── stage: Data extraction and classification
│   ├── activity: classify articles and store retrieved information
│   ├── coding_mode
│   │   ├── inductive coding: topic model, topics, article associations, topic words
│   │   └── deductive coding: extraction scheme/items tied to RQs
│   ├── input_scope: title/abstract for topic modeling; complete PDF for deductive coding
│   ├── interactive_refinement: adjust topic model; pilot extraction forms
│   └── llm_output: topic model outputs, extraction item suggestions, structured extracted values
├── stage: Visualization
│   ├── user_input: data tables/frequencies and chosen representations
│   ├── interactive_refinement: check correctness and quality
│   └── llm_output: graphical/tabular representations
├── stage: Reporting
│   ├── user_input: tables and request for patterns/insights
│   ├── interactive_refinement: adjust and add to suggestions
│   └── llm_output: suggested patterns and insights
└── reflection_boundary
    ├── validity_risk: publication bias, limited studies, model drift
    ├── domain_risk: many studies outside SE; need SE-specific evaluation
    └── future_work: evaluate individual steps; build end-to-end prototype
```

取值空间说明：`stage`、`search_agents`、`coding_mode` 在本文内可视作封闭/层级枚举；`user_input`、`interactive_refinement`、`llm_output` 多数是自由文本动作项或例示列表；prompt strategy、tool examples、relevant literature 不是本论文抽取 schema 的封闭字段。缺失部分：supplementary terminology 未核验；A2a 若要精核，应裁剪 Fig. 1 并逐框录入字段文本。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `stage.id` | 流程阶段 | root | Fig. 1 / §2 | LLM-supported mapping process 的主阶段 | need, identification, extraction, visualization, reporting | 层级枚举；本文内完整 | 无阶段则不适用 | 仅可统计 proposal 结构数 | 方法 scaffold | Fig. 1 | 不代表实证 SMS 标准 |
| `stage.activity` | 阶段任务 | stage | Fig. 1 标题下说明 | 每阶段人工/LLM要完成的任务 | gap/RQ、search/selection、classification、visualization、reporting | 自由文本加理由 | 未写则 not_reported | 不进主统计 | stage contract seed | Fig. 1 | 需保留原文阶段语义 |
| `user_input` | 用户输入 | stage | Fig. 1 | 研究者交给 LLM 的目标、数据、表格、元数据等 | 每阶段不同 | 自由文本/例示列表 | 不适用不等于缺失 | 不进主统计 | human-in-loop 字段 | Fig. 1 | 不能推断真实输入日志 |
| `interactive_refinement` | 交互修订 | stage | Fig. 1 | 研究者编辑、pilot、检查、调整 LLM 输出 | edit / pilot / check / adjust | 自由文本/动作列表 | 未报告具体次数 | 不进主统计 | 人工 gate 字段 | Fig. 1 | 不能推断人工一致性 |
| `llm_output` | LLM 输出 | stage | Fig. 1 | LLM 产生的问题、检索式、结构化判断、图表、pattern 建议 | questions, strings, criteria, structured output, charts, insights | 自由文本/例示列表 | 未报告质量指标 | 不进主统计 | 输出 schema seed | Fig. 1 | 不能推断效果 |
| `search_agent` | 搜索 agent 角色 | Study identification | §2.2.1 | 支持检索策略构造的三类 agent | Keyword Identification / Semantic Search / Search Strategy | 完整枚举（本文内） | 仅适用于 search | 可作 schema seed 计数 | agent 分工启发 | §2.2.1 | 未经原型验证 |
| `search_reproducibility` | 检索可复现约束 | Study identification | §2.2.1 | 搜索策略应透明、可复现，并保留 Boolean search 价值 | Boolean, semantic, citation pearl growing, query strategy | 外部分类法引用 + 自由文本 | 无真实检索式 | 不进主统计 | 搜索日志要求 | §2.2.1 | 不能说明 recall 足够 |
| `selection_decision_trace` | 纳排决策追踪 | Inclusion/exclusion | §2.2.2 / Fig. 1 | include/exclude 分类需理由、引用、文本证据、置信度 | verdict, rationale, citation, confidence | 关系值 + 自由文本 | 无真实样本则 not_applicable | 不进主统计 | 审计字段 | §2.2.2 | 不等于已实现工具 |
| `coding_mode` | 编码模式 | Data extraction | §2.3 | 数据抽取/分类分归纳与演绎 | inductive / deductive | 完整枚举（本文内） | 只适用 extraction | schema seed | coding scaffold | §2.3 | 非实证分类结果 |
| `inductive_pipeline` | 归纳编码流程 | Data extraction | §2.3 | 用标题/摘要做 topic modeling | embeddings, reduction, clustering, topic representation | 过程枚举/例示 | 无真实 corpus | 不进主统计 | topic pipeline seed | §2.3 | 不证明 BERTopic 最优 |
| `deductive_pipeline` | 演绎抽取流程 | Data extraction | §2.3 | 既定 extraction scheme + examples + full PDF/RAG | SWE-BOK example, one/few-shot, RAG chunks | 外部分类法引用 + 例示 | 无真实抽取表 | 不进主统计 | full-text extraction seed | §2.3 | 不可推断准确率 |
| `visualization_output` | 可视化输出 | Visualization | Fig. 1 / §2.4 | LLM/工具生成图表或表格呈现 | bar chart, bubble plot, tabular summary 等 | 例示枚举 | 无数据表则 not_applicable | 不进主统计 | report UI seed | Fig. 1, §2.4 | 不保证图表正确 |
| `reporting_pattern` | 报告 pattern 建议 | Reporting | Fig. 1 / §2.5 | 基于表格/图形让 GPT 提示 patterns/gaps | patterns, insights, research gaps | 自由文本 | 无数据则 not_applicable | 不进主统计 | candidate finding seed | §2.5 | 必须人工裁决 |
| `validity_boundary` | 效度边界 | Reflection | §3 | LLM literature review 可靠性受 publication bias、模型演化、SE 域外证据限制 | risk statements | 自由文本加理由 | 无量化不是缺失 | 不进主统计 | risk finding | §3 | 只能作限制，不作效果结论 |
| `data_availability` | 数据可用性 | Data availability | Data availability | 原文是否使用数据 | no data used | 布尔/声明 | 无数据是明确边界 | 排除主统计池 | eligibility filter | Data availability | 不能据此否定所有内部讨论材料 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| `edge.root.external_process` | root | follows | Petersen mapping guideline process | external guideline | 不适用 | §2 开头 | 说明阶段来源 |
| `edge.stage.role_fields` | stage | has_role_field | user_input / interactive_refinement / llm_output | 三元角色字段 | 若图中未列则 not_reported | Fig. 1 | 复原原生流程树 |
| `edge.need.to_identification` | need stage | feeds_next_stage | study identification | edited questions | 无真实 run | §2.1 | 表示 RQ 是阶段输出 |
| `edge.search.has_agents` | study identification/search | decomposes_into | three search agents | 3 agent enum | 仅 search 适用 | §2.2.1 | agent 分工 schema |
| `edge.keyword_semantic.support` | keyword + semantic agents | support | citation pearl growing | strategy relation | 无真实执行 | §2.2.1 | 搜索策略启发 |
| `edge.selection.classifies` | inclusion/exclusion | classifies | documents | relevant / not relevant | 无样本则 not_applicable | §2.2.2 | 决策字段 |
| `edge.selection.requires_trace` | selection decision | requires | rationale / citations / fragments | evidence anchors | 无真实判例 | §2.2.2 | 审计证据链 |
| `edge.extraction.has_modes` | data extraction | decomposes_into | inductive / deductive coding | 2 mode enum | 仅 extraction 适用 | §2.3 | coding schema |
| `edge.deductive.uses_scheme` | deductive coding | uses | extraction scheme | e.g. SWE-BOK | example only | §2.3 | 外部 taxonomy 接口 |
| `edge.reporting.generates_candidate` | reporting | suggests | patterns / insights / gaps | free text | 无数据则 not_applicable | §2.5 | 候选 finding，不是 final finding |
| `edge.reflection.limits_transfer` | reflection_boundary | limits | all method claims | publication bias/model drift/non-SE | 无量化不是缺失 | §3 | 降级与迁移边界 |

本文没有 formal database-style 关系型 schema；上表是 proposal 流程中的概念关系边，不能作为已执行样本编码关系表。

### 6. 统计观察、候选 finding 与 final finding 边界

原文自身字段/统计表支持的统计观察：

- 无。原文没有系统检索分母、样本库、质量评价、数据抽取表、统计表或实验结果。
- 可记录的“5 阶段 / 3 agents / 2 coding modes”只是 proposal 结构，不是研究对象统计结果。

原文 discussion / recommendation / roadmap 提出的候选 finding：

- LLM 可被嵌入 mapping study 的多个阶段，但应保持专家在环。
- search 阶段应兼顾语义能力与可复现 Boolean/search log。
- 纳排和抽取不应只给标签，需提供理由、引用、文本片段和可审计 trace。
- data extraction 可区分 inductive topic modeling 与 deductive scheme-based extraction。
- 当前 LLM literature review 证据会受 publication bias、研究数量少、模型快速演化和非 SE 证据外推影响。
- 后续研究应先评估 individual steps，再构建整体 prototype。

对 Paper2 可迁移的方法学启发：

- 把 LLM 辅助综述写成 interactive scaffold，而非全自动替代专家。
- 每个 stage 都保留 `human input -> LLM output -> human refinement -> audit evidence`。
- run record 应记录模型、prompt、source anchor、人工 override 和版本漂移风险。
- 候选 finding 必须经过人工裁决和跨论文反证，不能由 LLM reporting suggestion 直接升级。

绝不能迁移的领域结论：

- 不能声称 LLM 已经提高 mapping study recall、precision、速度或质量。
- 不能声称 end-to-end holistic solution 已实现或已验证。
- 不能声称 GPT/Claude/任一模型在 SE mapping study 中稳定可靠。
- 不能把引用文献中的结果当成本论文实证结果。
- 不能把本文当作 SLR/SMS 样本纳入统计池。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 问题 | 最小返修建议 |
|---|---|---|
| C | 现有结论卡片中“是否目标证据池”写成“是/否”混合，容易误入主统计池 | 改为：主统计池资格=否；仅 `schema_seed` / `boundary_anchor`；若保留 A1 方法脚手架用途，必须单独列为非统计用途 |
| C | “维度树复原”仍先出现六个通用 leaf，虽然后文做了校准，但读者仍可能把它当原文树 | 将原文流程树置于主事实源：5 个 Fig. 1 阶段 + 3 search agents + 2 coding modes + reflection boundary；六叶接口仅放到“跨论文投影” |
| C | 旧 v1 / 19×3 / 三路审计内容仍以较强语气存在 | 按本任务硬约束降级为历史参考，不得作为原生树模板；最终树只从本文 `paper_content.txt` 和 PDF Fig. 1 出发 |
| I | `orig-validity-risk` 中 hallucination、human overtrust 等项未在本次全文证据中直接出现 | 删除或标为 `not_verified`，保留原文直接支持的 publication bias、limited studies、model evolution、non-SE evidence |
| I | A.2/A.3 证据账本太泛，很多行是“待 A2a 精确页码复核” | 替换为本报告第 8 节的具体证据锚点，至少包含摘要、Fig. 1、§2.2.1、§2.2.2、§2.3、§3、Data availability |
| I | SUMMARY 中“样本单位 / 样本数量 / 原生树类型 / 统计池资格”需修正 | 样本单位=无系统样本库；样本数量=无分母；原生树类型=降级流程树/维度森林；统计池资格=否 |
| M | 年份字段需保持清晰 | 正式引用按 2025；online available 2024-10-31，metadata publication_date 2024-11-01 仅作在线日期线索 |
| M | Supplementary material 未核验 | 若 `review.md` 使用下划线术语定义，需打开 supplementary；否则明确“不使用 supplementary 事实” |
| M | 需要补 A.1--A.4 | A.1 已有但可精简；A.2/A.3 应按本报告替换；A.4 加入 Fig. 1 视觉复核命令/清单 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| `EV01` | `paper_content.txt` | Abstract | Context/Objective/Method/Results/Conclusion | 方法被定义为 solution proposal，目标是讨论 LLM 用于 mapping process | 类型判定 | strong | 原文类型、统计池排除 | 否 | 不支撑实证效果 |
| `EV02` | `paper_content.txt` | Introduction | mapping vs SLR | mapping study 用于分类和趋势观察，SLR 用于证据综合 | 背景边界 | strong | root scope | 否 | 不能当作本文执行了 SMS |
| `EV03` | `paper_content.txt` | Introduction | LLM motivations | LLM 动机包括研究量、范围、设计想法、更新成本 | proposal 动机 | medium | candidate finding | 否 | 不是效果评估 |
| `EV04` | `paper_content.txt` | Introduction | human-in-loop paragraph | 研究者需要 mapping 方法能力和主题专家能力 | 人机边界 | strong | human gate | 否 | 不能迁移为全自动 |
| `EV05` | `paper.pdf` + `paper_content.txt` | Fig. 1 / §2 | PDF 第 2 页图 | 五阶段流程及每阶段 user input/refinement/LLM output | 原生树核心 | strong | stage tree | 否；本轮已视觉核验 | 图中文字需二次人工录入时再核 |
| `EV06` | `paper_content.txt` | §2.1 | need for map | LLM 产生 RQ/补充目标，人类编辑后进入下一阶段 | 阶段字段 | strong | need stage | 否 | RQ 不是样本树根 |
| `EV07` | `paper_content.txt` | §2.2.1 | Search | 搜索策略需透明可复现，并提出三类 agent | agent schema | strong | search_agent | 否 | 未验证 agent 效果 |
| `EV08` | `paper_content.txt` | §2.2.1 Relevant literature | Wang et al. discussion | GPT 查询有潜力但 recall 风险存在 | cited evidence caveat | medium | search risk | 否 | 属引用文献结果 |
| `EV09` | `paper_content.txt` | §2.2.2 | Inclusion/exclusion | 纳排是分类问题，但需理由、引用和 traceability | 决策追踪 | strong | selection trace | 否 | 未给真实判例表 |
| `EV10` | `paper_content.txt` | §2.3 | Data extraction/classification | 归纳编码与演绎编码两分；deductive 可用 full PDF/RAG | coding schema | strong | coding_mode | 否 | 不说明准确率 |
| `EV11` | `paper_content.txt` | §2.4--2.5 | Visualization/Reporting | 可视化与报告用于图表生成、pattern/insight 建议 | reporting seed | medium | visualization/reporting | 否 | 建议需人工裁决 |
| `EV12` | `paper_content.txt` | §3 / Data availability | Reflections / Data availability | 证据受 bias、模型演化、非 SE 外推限制；无数据使用 | 降级依据 | strong | main pool exclusion | 否 | 不否定方法启发价值 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| `CL01` | 本文是 solution proposal，不是已执行的 SLR/SMS/tertiary study | type | 原文类型 | `EV01`, `EV12` | strong | metadata / eligibility | 标题含 mapping studies，但方法未执行 mapping |
| `CL02` | 本文无系统样本库、无样本分母，不能进入主统计池 | eligibility | 统计池资格 | `EV01`, `EV12` | strong | SUMMARY 修正 | 参考文献不是系统样本 |
| `CL03` | 原生树应复原为方法流程树：五阶段 + 每阶段人机角色字段 | tree_type | 维度树 | `EV05`, `EV06` | strong | `review.md` 重写 | Fig. 1 框中文字需保留原文边界 |
| `CL04` | Study identification 的 search 子树包含三类 agent | leaf_definition | search_agent | `EV07` | strong | schema seed | 未评估 agent 实现 |
| `CL05` | 纳排节点的核心迁移字段是 rationale/citation/trace，而非只存 include/exclude | methodological_seed | selection trace | `EV09` | medium | Paper2 run record 设计 | chain-of-thought 不宜迁移为隐藏推理链暴露要求 |
| `CL06` | Data extraction 节点分 inductive 与 deductive coding，可作 Paper2 抽取流程 seed | leaf_definition | coding_mode | `EV10` | medium | schema seed | 无真实数据抽取表 |
| `CL07` | Reporting 中 pattern/insight/gap 只能作为候选 finding，不是 final finding | finding_boundary | reporting | `EV11`, `EV12` | strong | 候选发现管理 | 缺少数据和人工裁决 |
| `CL08` | 本文可迁移的是 interactive scaffold、audit trace 和风险意识，不可迁移 LLM 效果结论 | migration_boundary | Paper2 启发 | `EV03`, `EV04`, `EV08`, `EV12` | strong | 方法学启发 | 单篇 proposal 不能外推 |

### 9. 技能使用与自我审查记录

已读取的技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`

采用的原则：

- 证据优先；没有本地原文证据时降级为 `not_verified` / `schema_seed`。
- 区分 claim、evidence、limitation、candidate finding，避免把 proposal 写成实验结论。
- reviewer 输出要具体、可执行，直接指出 `review.md` 返修位置和 C/I/M 风险。
- research planning 的“严格贴合原文、不编造配置/取值空间”原则用于维度树复原。
- autoresearch 的 artifact-gated 思路用于自检：不能因口头完成而结束，必须有证据账本和结论映射。

最高风险 3 点与合并复核建议：

1. Fig. 1 字体较小，本次已视觉核验但仍建议主线程裁剪放大后二次人工录入，尤其是每个框内的完整字段文本。
2. Supplementary material 未打开；若后续 `review.md` 使用下划线术语定义，必须补充核验，否则不得引用。
3. 现有 `review.md` 中 v1/19×3/六叶通用接口内容较多，合并时最容易“保留旧事实源”。建议先改 SUMMARY 资格字段，再整体替换维度树与 A.2/A.3。

本任务未出现 blocked、timeout 或指定文件缺失；未修改仓库文件，未启动 subagent，未 commit/push/gh comment。