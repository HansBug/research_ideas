### 0. 审计结论卡片

| 项 | 结论 |
|---|---|
| paper slug | `formal-re-llm-roadmap` |
| agent | `codex` |
| 是否已读 `paper_content.txt` | 是；已通读全文提取文本，重点复核摘要、引言、背景、两个示例、两个 roadmap、实践限制、结论和数据声明。 |
| 是否读取 `bibtex.bib` / `metadata.json` | 是；已核对题名、作者、年份、DOI、期刊、文献类型、本地 eligibility 字段。 |
| 是否打开或核对 `paper.pdf` | 是；用 PDF 转图并视觉核验 Fig. 2 与 Fig. 4 的路线图层级和节点。未逐项视觉核对全部 listing / prompt box。 |
| 原文类型 | roadmap / vision / proposal；不是 SLR、SMS、tertiary 或 MLR。 |
| 被编码样本单位 | 无系统样本库。可抽取的原生单位是两条 roadmap 下的 action point、layer、artefact、mechanism、concern、practical limitation。 |
| 样本数量 / 分母 | 系统样本数量：不适用。路线图 action point 可作局部结构单位：Roadmap A 为 5 个，Roadmap B 为 7 个；这不是系统综述分母。 |
| 原生树类型 | 降级树 / 维度森林：双向 roadmap-action 森林 + concern / limitation 边界树。 |
| 主统计池资格 | 否；作者明示 vision paper，不提供 sound empirical evidence，且无系统检索、纳排、质量评价、数据抽取或统计综合。 |
| 总体判定 | needs repair；论文可作为 boundary anchor / schema seed，但现有 `review.md` 仍需把六叶通用接口降级，并细化原文 action-point 维度树。 |

### 1. 原文证据阅读说明

本轮实际读取了以下本地文件：

- `bibtex.bib`：确认 2025 年 IST 期刊论文、DOI `10.1016/j.infsof.2025.107697`。
- `metadata.json`：确认本地已标注 `review_type = vision / roadmap`、`eligible_for_statistical_synthesis = false`、`evidence_role = roadmap_boundary_anchor`。
- `paper_content.txt`：全文读取，覆盖 Page 1--21。
- `review.md`：全文读取，重点检查快速卡片、六类 pattern、历史草稿、维度树复原、A.1--A.4。
- `paper.pdf`：已视觉核验第 9 页 Fig. 2 与第 14 页 Fig. 4；未对所有代码清单和框图排版做逐项核验。

关键证据锚点：

1. 摘要 Context / Objective / Methods：作者目标是提出 formal methods 与 LLM 的双向 roadmap，而非报告系统综述结果。
2. Introduction 贡献列表：Section 4 是 LLM 支持 formal RE，Section 6 是 formal RE 支持 LLM-based development。
3. Introduction 明示本文是 vision paper，不以提供可靠实证证据为目标，roadmap 不声称穷尽。
4. Section 2.2：formal RE 被界定为 specification、model、verification 相关数学化技术。
5. Section 3：sender-receiver 示例展示需求、PROMELA 模型、LTL/Spin 验证、反例、Python 实现之间的链路。
6. Fig. 2 / Section 4：路线图 A 由 formal development、conventional development、LLM 三层构成，围绕 5 个 action point。
7. Section 5：ChatGPT 3.5 示例展示需求生成、反馈分析、歧义检测、完整性检查、模型生成、分类、追踪等任务；作者说明输出经过有限调整和多轮提示。
8. Fig. 4 / Section 6：路线图 B 由 formal layer、SW artefact layer、LLM layer 构成，围绕 7 个 action point。
9. Section 7：实践限制覆盖专家协作、评价难、过度依赖、人的角色、FM 数据不足、制品维护、部署扩展和技术演化。
10. Conclusion / Data availability：路线图主要用于激发研究；数据声明为未使用数据。

### 2. 样本单位与字段来源判定

1. 原文纳入和逐项描述的对象是什么？

原文没有纳入 primary study、secondary study、tool 或 dataset 样本库。它逐项描述的是两个例子驱动的研究路线图：第一条是 LLM 如何支持 formal methods / formal RE 的可用性，第二条是 formal methods 如何约束 LLM-based RE / SE 的可靠性与可信性。可编码单位只能降级为 roadmap action point、图层、输入输出工件、技术机制、关注点和实践限制。

2. 作者有没有系统检索 / 纳排 / 数据抽取 / 编码方案？

没有。原文有背景文献引用和例子，但没有检索数据库、检索式、时间窗、纳排标准、质量评价、数据抽取表、编码员一致性或统计综合。作者还主动声明本文是 vision paper。

3. 原文字段来自哪里？

字段主要来自 roadmap / guideline item，而不是 extraction form。具体来源包括：

- Abstract / Introduction 的双向目标与贡献声明。
- Section 4 的 5 个 action point。
- Fig. 2 的三层结构与 LLM 节点。
- Section 6 的 7 个 action point。
- Fig. 4 的三层结构、formal mechanisms、SW artefacts、LLM task 类型。
- Section 7 的 practical considerations / limitations。
- Section 5 的 LLM-driven RE 示例任务列表，可作为任务面 seed，但不是实验样本编码。

4. RQ 与样本单位是什么关系？

原文没有正式 RQ。隐含问题是“双向路线图”问题：如何用 LLM 降低 formal RE 使用门槛，以及如何用 formal methods 提升 LLM-based RE 的正确性、公平性和可信性。RQ 不是树根下的样本分组字段，而是路线图根对象的目标声明；实际叶子应来自 action point、layer、artifact、mechanism、concern、limitation。

5. 若无系统样本库，如何降级？

本文应降级为 `boundary_anchor` / `schema_seed` / `candidate_heuristic`。可以用于补充 Paper2 的字段树设计、候选 concern taxonomy 和方法学启发；不能进入主统计池，不能支撑“领域中多数研究如何”的频次结论，不能把 action point 写成 final finding。

### 3. 原生样本编码维度树 / 维度森林

```text
formal-re-llm-roadmap 原生降级维度森林
├── 元信息与资格边界
│   ├── 文献类型：vision / roadmap
│   ├── 系统样本库：无
│   ├── 证据角色：boundary anchor / schema seed
│   └── 统计资格：不进入主统计池
├── Roadmap A：LLM 支持 FM-based development
│   ├── 图层
│   │   ├── formal development layer
│   │   ├── conventional development layer
│   │   └── LLM / agent layer
│   ├── 工件流
│   │   ├── 需求 ↔ 逻辑公式
│   │   ├── 模型 ↔ 代码
│   │   ├── formal artefact → explanation
│   │   ├── formal language / model ↔ formal language / model
│   │   ├── artefact ↔ trace link
│   │   └── artefact → ontology / knowledge representation
│   ├── action point
│   │   ├── 从 formal specification 生成 code，或从 code / requirements 生成 formal artefact
│   │   ├── 解释 formal model、formula、assertion、counterexample
│   │   ├── 在 formal languages / tools 之间转换
│   │   ├── 支持迭代、演化和 trace-link consistency
│   │   └── 自动化 knowledge / ontology engineering
│   └── 主要风险
│       ├── FM 数据不足
│       ├── 抽象不当导致验证不可行或不忠实
│       ├── state-space explosion
│       └── 多工件维护负担
├── Roadmap B：FMs 支持 LLM-based development
│   ├── 图层
│   │   ├── formal layer
│   │   ├── SW artefact layer
│   │   └── LLM layer
│   ├── LLM task 类型
│   │   ├── analytic task：smell、completeness、trace 等注释/分析
│   │   └── generative task：requirements、model、code、test 等生成
│   ├── formal mechanism / assurance mechanism
│   │   ├── formal requirements / formal SW artefact verification
│   │   ├── formal argumentation
│   │   ├── FM knowledge / formal domain knowledge
│   │   ├── formal prompt / prompt architecture
│   │   ├── neural behaviour abstraction / formal verification
│   │   ├── runtime verification
│   │   └── formalised ethical requirements
│   ├── assurance concern
│   │   ├── correctness / hallucination
│   │   ├── logical coherence
│   │   ├── mathematical reasoning
│   │   ├── prompt ambiguity
│   │   ├── domain grounding / explainability
│   │   ├── output consistency / repeatability
│   │   ├── regulatory compliance
│   │   └── bias / ethics / fairness / privacy / robustness
│   └── action point：Section 6 中 7 个路线点
└── 实践限制 / 迁移边界
    ├── LLM-FM 专家协作
    ├── empirical evaluation 困难
    ├── overreliance
    ├── human creativity / requirements engineer role
    ├── limited FM datasets
    ├── artefact proliferation and maintainability
    └── deployment / scalability / technological evolution
```

缺失部分和 A2a 精核任务：本轮已核验 Fig. 2 / Fig. 4 的图层和主要节点，但未把图中每个箭头逐一编码为完整 source-target relation，也未视觉核对全部 listing、prompt box 和引用项。A2a 若要冻结正式字段，应逐页确认每个 action point 的原文位置、图中节点 label、箭头方向、是否封闭枚举、是否可跨论文复用。

### 4. 叶子维度表

| 叶子标识 | 中文名称 | 父节点 | 原文字段来源 | 定义 | 取值空间 | 取值空间类型 | 缺失值语义 | 统计用途 | 候选发现用途 | 证据锚点 | 迁移边界 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L0-doc-type | 文献类型与资格 | 元信息与资格边界 | Abstract、Introduction、metadata | 判定本文是否为系统综述及能否进入主统计池 | vision / roadmap；非 SLR/SMS；no systematic sample | 完整枚举 | 若无声明需从方法结构推断；本文有明确声明 | 排除主统计池 | 支持非系统文献降级规则 | Page 1--2；metadata eligibility | 只迁移资格判断，不迁移领域结论 |
| L0-evidence-role | 证据角色 | 元信息与资格边界 | Introduction、Conclusion、Data availability | 说明本文在 Paper2 中的证据角色 | boundary anchor、schema seed、candidate heuristic、not statistical evidence | 层级枚举 | 无数据声明时需降级为 not_verified | 统计池外标签 | 形成 roadmap 文处理规则 | Introduction vision 声明；Data availability | 不能作为经验发现 |
| A-layer | Roadmap A 图层 | Roadmap A | Fig. 2、Section 4 summary | LLM 支持 formal development 的层级结构 | formal development、conventional development、LLM/agent layer | 完整枚举，已 PDF 核验 | 图未核验时写待核验 | 不做频次统计；可统计为 tree-shape seed | 指导字段树层级设计 | PDF Fig. 2；Page 8--11 | 只迁移结构 |
| A-artifact-flow | Roadmap A 工件流 | Roadmap A | Fig. 2、Section 4 | conventional artefact 与 formal artefact 的转换/解释/追踪关系 | requirements、logic formulae、models、code、process artefacts、trace links、knowledge representations | 关系值 / 层级枚举 | 未见箭头或节点时写 not_verified | 不进入主统计池 | 生成 artifact-in/out 字段 | Fig. 2；Section 4 action points | 不代表完整 FM 工件全集 |
| A-action | Roadmap A action point | Roadmap A | Section 4 每个 action point | LLM 介入 FM-based development 的研究行动点 | 生成工件、解释工件、语言转换、迭代演化、知识工程 | 完整枚举，限本文 | 若缺段落证据则待核验 | 可作 action seed，不作领域频次 | 生成 LLM-for-FM 候选机制 | Page 8--11 | 不是经验证实的效果 |
| A-mechanism | Roadmap A LLM 机制 | Roadmap A | Section 4、Fig. 2 | 支撑 action 的 LLM 技术或 agent 角色 | RAG、summarisation、translation、explanation、code-specialised LLM、NL-oriented LLM、ontology extraction | 自由文本加理由 / 层级枚举 | 未给机制时记 unknown | 不统计效果 | 帮助 Paper2 区分 agent role | Section 4 段落 | 机制可迁移，性能不可迁移 |
| B-layer | Roadmap B 图层 | Roadmap B | Fig. 4、Section 6 summary | formal methods 控制 LLM-based development 的层级结构 | formal layer、SW artefact layer、LLM layer | 完整枚举，已 PDF 核验 | 图未核验时写待核验 | 不做主统计 | 支持 assurance-control 架构 | PDF Fig. 4；Page 14--16 | 只迁移控制结构 |
| B-task-type | LLM task 类型 | Roadmap B | Section 6 summary | LLM 对 SW artefact 的任务类型 | analytic task、generative task | 完整枚举 | 未说明任务类型时 unknown | 可作 schema seed | 区分分析型与生成型 agent | Section 6 summary | 不代表所有 RE 任务 |
| B-artifact | SW artefact 类型 | Roadmap B | Fig. 4、Section 5--6 | LLM 输入/输出或 formal verification 关联工件 | input requirements、feedback、issues、generated code/test/model/requirements、formal SW artefact | 层级枚举 | 未在图或段落出现则待核验 | 不进主统计 | 建立 artifact target 字段 | Fig. 4；Section 5 examples | 示例性，不等于系统分类 |
| B-assurance-mechanism | formal assurance 机制 | Roadmap B | Section 6 action points、Fig. 4 | 用于约束、验证或解释 LLM 输出的 formal mechanism | formal requirements、argumentation、FM knowledge、formal domain knowledge、formal prompts、formal verification、runtime verification、ethical requirements | 层级枚举 | 无机制则 not_applicable | 不统计效果 | 形成 concern→mechanism 模式 | Page 14--16 | 不声称机制已有效 |
| B-concern | 可信性关注点 | Roadmap B | Abstract、Section 6、Section 7 | LLM-based RE/SE 中需要 formal control 的风险或质量目标 | correctness、fairness、trustworthiness、hallucination、logical coherence、math reasoning、prompt ambiguity、domain grounding、consistency、compliance、bias、ethics、privacy、robustness | 层级枚举 / 自由文本加理由 | 若只由外部文献背景出现，标 background_only | 不统计领域分布 | 候选 concern taxonomy | Abstract；Section 6；Section 7 | 单篇不构成饱和 taxonomy |
| B-action | Roadmap B action point | Roadmap B | Section 6 每个 action point | FMs 支持 LLM-based development 的研究行动点 | 正确性与论证、数学推理、formal prompt、domain knowledge、output consistency、runtime compliance、ethical requirements | 完整枚举，限本文 | 缺段落证据则待核验 | 可作 action seed | 生成 FM-for-LLM 候选机制 | Page 14--16 | 不作为 final finding |
| E-example-type | 例子类型 | 示例证据 | Section 3、Section 5 | 原文用来支撑 roadmap 的 worked example 类型 | sender-receiver formal development；ChatGPT 3.5 RE task showcase | 完整枚举，限本文 | 无示例则 not_applicable | 不作 benchmark | 说明证据强度 | Page 6--14 | 示例不能代表总体 |
| E-llm-adjustment | LLM 输出处理 | 示例证据 | Section 5 | 作者是否说明 LLM 输出经过人工处理 | slightly adjusted、iterative prompting、compressed output | 自由文本加理由 | 未说明时 unknown | 证据降级 | 标注 reproducibility risk | Section 5 opening | 不可当可重复实验 |
| R-limitation | 实践限制 | 实践边界 | Section 7 | 实施 roadmap 的风险、限制和配套条件 | 专家协作、评价难、overreliance、人类角色、FM 数据不足、制品维护、部署扩展、技术演化 | 层级枚举 | 未提及时不补造 | 不做领域统计 | 候选 risk register | Page 16--17 | 只作风险启发 |
| R-data | 数据 / 复现状态 | 元信息与资格边界 | Data availability | 是否存在实验数据或复现资产 | no data used | 布尔 / 自由文本 | 未声明则 not_verified | 支持统计排除 | 支持证据等级判定 | Page 18 data statement | 不代表无引用文献 |

### 5. 关系边表

| 关系边标识 | 源节点 | 关系类型 | 目标节点 | 目标取值空间 | 缺失值语义 | 证据锚点 | 用途 |
|---|---|---|---|---|---|---|---|
| R-A-req-logic | natural language requirements | translates_to / from | logic formulae | LTL、CTL 等 formal logic；本文示例含 LTL | 未出现具体 logic 时待核验 | Section 3；Section 4 Req2Logic / Logic2Req 节点 | 支持 Req2Logic 字段 |
| R-A-model-code | formal model | translates_to / from | code | PROMELA model、Python code、code abstraction | 箭头方向未核验时待核验 | Section 3；Fig. 2 Model2Code / Code2Model | 支持 Model2Code / Code2Model 字段 |
| R-A-formal-explain | formal artefact | explained_by | LLM explanation | model、formula、assertion、counterexample | 若无 explanation target 则 unknown | Section 4 explaining FM artefacts | 支持 explainability action |
| R-A-model-model | formal model/language | translated_to | another formal model/language | tool/language/audience-specific views | 若只背景提到则 background_only | Section 4 translating formal languages | 支持 FM diversity / model transformation |
| R-A-artefact-trace | development artefact | linked_by | trace link LLM | requirements、specifications、tests、code、other artefacts | 未指定 artefact 对时 open | Section 4 iterations/evolution | 支持 artefact evolution 字段 |
| R-A-artefact-ontology | software/formal artefacts | abstracted_to | ontology / knowledge representation | requirements、models、docs、tests → ontology | 未说明来源时 open | Section 4 knowledge engineering | 支持 knowledge engineering seed |
| R-B-input-task | input requirement artefact | consumed_by | LLM analytic/generative task | system requirements、user feedback、issues | 输入不明时 unknown | Section 6 summary；Fig. 4 | 区分输入工件 |
| R-B-task-output | generative LLM task | produces | generated SW artefact | code、test、model、requirements | 输出不明时 unknown | Section 5 examples；Fig. 4 | 支持 generated artefact target |
| R-B-formal-verify | formal requirements | verify_against | formal SW artefact | generated artefact associated formal artefact | 未 formalised 时 not_applicable | Section 6 correctness / Fig. 4 | 支持 formal assurance |
| R-B-argumentation | LLM response | constrained_by | formal argumentation | argumentation structure | 未有论证结构时 not_applicable | Section 6 correctness | 支持 hallucination mitigation seed |
| R-B-knowledge | FM/domain knowledge | injected_into | LLM process | FM knowledge、formal domain knowledge、knowledge graph、RAG | 未说明注入机制时 open | Section 6 math/domain knowledge | 支持 grounding / reasoning 字段 |
| R-B-prompt | prompt / prompt architecture | constrained_by | formal notation / controlled NL | pre/post-conditions、semi-formal prompt relations | 未 formalised 时 not_applicable | Section 6 formal prompt engineering | 支持 prompt-as-requirement |
| R-B-consistency | LLM behaviour | checked_by | formal verification / abstraction | prompt perturbation consistency、NN abstraction | 未有 formal target 时 not_verified | Section 6 output consistency | 支持 robustness/consistency concern |
| R-B-runtime | regulatory requirements | monitored_by | runtime verification | evolving regulation / evolving LLM knowledge | 非运行时场景不适用 | Section 6 regulatory compliance | 支持 runtime compliance |
| R-B-ethics | ethical requirements | validated_on | LLM-generated artefacts | fairness、privacy、ethics、bias-related targets | 未 operationalise 时 schema_seed | Section 6 ethics | 支持 ethics assurance |

本文存在显式关系型 schema 的图示与叙述，但不是系统抽取 schema；关系边只能作为 roadmap relation seed，不可直接升级为统计字段。

### 6. 统计观察、候选 finding 与 final finding 边界

**字段 / 统计表支持的统计观察**

- 没有系统统计观察。本文没有样本分母、数据抽取表、质量评价表或频次结果。
- 可局部记录的只是文本结构事实：两条 roadmap、5 个 Roadmap A action point、7 个 Roadmap B action point、三层图结构、Section 7 的若干实践限制。
- 这些局部计数只能用于复原本文结构，不能进入跨论文主统计池。

**discussion / recommendation / roadmap 的候选 finding**

- LLM 可作为 formal RE 的翻译、解释、追踪、知识工程辅助机制，但这只是研究路线，不是已验证效果。
- Formal methods 可作为 LLM-based RE 的 correctness、argumentation、prompt constraint、domain grounding、consistency、runtime compliance、ethics/fairness 控制机制，但也是研究议程。
- LLM 与 FM 的结合会增加新型维护与评估问题，如非唯一 ground truth、overreliance、工具/模型漂移、多制品一致性等。

**对 Paper2 可迁移的方法学启发**

- 将非系统 roadmap 文献显式标为 `boundary_anchor` / `schema_seed`。
- 候选发现应采用 concern-first 结构：任务/工件 → concern → mechanism → evidence strength → human gate / limitation。
- 对 agentic SLR，LLM 自动化能力应与结构化证据链、人工门控和审计制品并列，而不是只记录“能生成什么”。
- Formal prompt、argumentation、ontology、runtime monitor 等可迁移为“结构化审计接口”的灵感，但不要承诺形式化验证。

**绝不能迁移的领域结论**

- 不能说 LLM+FM 已被证明能提高 RE 正确性、可靠性或公平性。
- 不能把 ChatGPT 3.5 示例当作 benchmark 或可重复实验。
- 不能把本文 action point 当作 formal RE + LLM 领域的饱和 taxonomy。
- 不能把本文引用的背景文献数量或示例任务当作系统综述统计。

### 7. 对现有 `review.md` 的返修建议

| 等级 | 返修建议 | 理由 |
|---|---|---|
| C | 重写“维度树结构”主表，把六个通用接口从主树中移出，只保留为 cross-paper projection。 | 当前 `review.md` 后半段已意识到六叶接口问题，但第 318--360 行仍把 scope/corpus/taxonomy/method/evidence/finding 画成主树，容易违反 A1-DT v2。 |
| C | 将原生树改为“无系统样本库 + 双向 roadmap action 森林”，根对象是 roadmap action / layer / artefact / concern，而不是 paper/study extraction schema。 | 本文无系统样本库；原生字段来自 Section 4、Fig. 2、Section 6、Fig. 4、Section 7。 |
| C | SUMMARY 中 `样本单位 / 样本数量 / 原生树类型 / 统计池资格` 应写：无系统样本库；局部 action point 5+7；降级树/维度森林；不进入主统计池。 | 避免把 5+7 action point 误写为综述样本数量。 |
| I | 叶子表应补充 action-level 字段：roadmap_direction、layer、artifact_in/out、task_type、action_point、mechanism、assurance_concern、evidence_boundary、limitation。 | 现有原文主树只有粗主干，尚不足以直接指导 A2a 精核或 review.md 重写。 |
| I | A.2 证据账本需要替换泛化证据行，补入具体章节 / 图 / 段落锚点。 | 当前 A.2 多处写“待 A2a 精确页码复核”，证据强度被不必要地降到 `not_verified`；本轮可至少升级 Fig. 2、Fig. 4、vision 声明、Data availability 为已读文本/PDF核验。 |
| I | A.3 结论映射应删除“叶子维度来自 RQ / 方法 / 分类 / 评价 / 讨论结构”这类模板句，改成具体结论：无系统样本、Roadmap A 五类 action、Roadmap B 七类 action、Section 7 限制。 | 当前映射仍像通用模板，不像这篇论文自己的 schema。 |
| M | 保留现有 review 对 Paper2 的启发，但改名为“候选启发”，并为每条标注 `schema_seed` 或 `risk_only`。 | 防止把 vision recommendation 写成 final research finding。 |
| M | PDF 核验状态可更新为：Fig. 2 / Fig. 4 已核验；listing / prompt boxes 未逐项核验。 | 比当前“needs_manual_check”更精确。 |

### 8. 审计附录草案：证据账本与结论映射

#### A.2 维度树证据账本草案

| 证据标识 | 来源文件 | 原文章节 | 段落或表图线索 | 原文短引或释义 | 证据角色 | 证据强度 | 支撑对象 | 需要原文版面核验 | 外推限制 |
|---|---|---|---|---|---|---|---|---|---|
| EV-FRLLM-01 | `paper_content.txt`、`bibtex.bib`、`metadata.json` | 题名、摘要、元数据 | Page 1；BibTeX / metadata | 2025 IST roadmap 文；目标是 formal RE 与 LLM 双向路线 | 元信息 / 类型判定 | strong | L0-doc-type、L0-evidence-role | 否 | 只支撑本文类型 |
| EV-FRLLM-02 | `paper_content.txt` | Introduction | Page 2 贡献列表与 vision 声明 | 作者明示本文不是提供实证证据，而是提出研究方向 | 统计池排除 | strong | L0-evidence-role、R-data | 否 | 不代表该领域没有证据 |
| EV-FRLLM-03 | `paper_content.txt` | Background 2.2 | Page 4--6 formal RE 背景 | formal RE 包括 specification、model、verification 等技术 | 背景分类 seed | medium | A-artifact-flow、B-assurance-mechanism | 否 | 背景综述不是系统 taxonomy |
| EV-FRLLM-04 | `paper_content.txt` | Section 3 | sender-receiver 示例、PROMELA、Spin、counterexample、Python | 用 worked example 展示 formal development 链路与可用性成本 | 示例证据 | medium | E-example-type、A-artifact-flow | 部分；listing 未逐项视觉核验 | 不是 benchmark |
| EV-FRLLM-05 | `paper.pdf`、`paper_content.txt` | Section 4 / Fig. 2 | PDF 第 9 页 Fig. 2；Page 8--11 | Fig. 2 三层结构及多类 LLM agent 节点已视觉核验 | 原生结构 | strong | A-layer、A-artifact-flow、A-action | 已核验 Fig. 2 | 图结构不等于系统分类 |
| EV-FRLLM-06 | `paper_content.txt` | Section 4 | 5 个 action point 段落 | Roadmap A 包含生成、解释、转换、演化追踪、知识工程五类 action | action 枚举 | strong | A-action、A-mechanism | 否 | action 未经效果验证 |
| EV-FRLLM-07 | `paper_content.txt` | Section 5 | Page 11--14；ChatGPT 3.5 示例 | 示例输出经有限调整和多轮提示；覆盖 RE 任务面 | 示例边界 | strong | E-llm-adjustment、B-task-type | prompt box 未逐项视觉核验 | 不可当可重复实验 |
| EV-FRLLM-08 | `paper.pdf`、`paper_content.txt` | Section 6 / Fig. 4 | PDF 第 14 页 Fig. 4；Page 14--16 | Fig. 4 三层结构、formal mechanism、SW artefact、LLM task 节点已视觉核验 | 原生结构 | strong | B-layer、B-artifact、B-assurance-mechanism | 已核验 Fig. 4 | 图结构不等于实证架构 |
| EV-FRLLM-09 | `paper_content.txt` | Section 6 | 7 个 action point 段落 | Roadmap B 覆盖 correctness、math reasoning、formal prompt、domain knowledge、consistency、runtime compliance、ethics | action / concern 枚举 | strong | B-action、B-concern | 否 | 不代表 concern taxonomy 饱和 |
| EV-FRLLM-10 | `paper_content.txt` | Section 7 | Practical considerations and limitations | 实施风险包括协作、评价、overreliance、human role、FM data、maintainability、scalability 等 | 迁移边界 / 风险 | strong | R-limitation | 否 | 只支撑风险启发 |
| EV-FRLLM-11 | `paper_content.txt` | Conclusion / Data availability | Page 18 | 路线图旨在激发研究；未使用数据 | 证据等级 / 统计排除 | strong | R-data、L0-evidence-role | 否 | 不代表无材料引用 |

#### A.3 结论-证据映射草案

| 结论标识 | 结论内容 | 结论类型 | 支撑对象 | 支撑证据 | 结论强度 | 允许用途 | 反证或限制 |
|---|---|---|---|---|---|---|---|
| CLM-FRLLM-01 | 本文是 vision / roadmap，不是 SLR/SMS/tertiary；没有系统样本库。 | 类型判定 | L0-doc-type | EV-FRLLM-01、EV-FRLLM-02 | strong | boundary_anchor | 作者引用大量文献，但未形成系统检索 |
| CLM-FRLLM-02 | 本文不具备主统计池资格，只能作为 schema seed / candidate heuristic。 | 统计资格 | L0-evidence-role、R-data | EV-FRLLM-02、EV-FRLLM-11 | strong | SUMMARY eligibility、A1-DT 降级 | 不影响其作为高价值 vision 文的启发作用 |
| CLM-FRLLM-03 | 原生结构应复原为双向 roadmap-action 维度森林，而不是六叶通用 SLR 模板。 | tree_type | A-layer、B-layer、A-action、B-action | EV-FRLLM-05、EV-FRLLM-06、EV-FRLLM-08、EV-FRLLM-09 | strong | 重写 review.md 维度树 | 不是跨论文统一模板 |
| CLM-FRLLM-04 | Roadmap A 的局部结构单位是 5 类 LLM-for-FM action point。 | schema_seed | A-action | EV-FRLLM-05、EV-FRLLM-06 | strong | A2a 字段精核 | 不能转成效果统计 |
| CLM-FRLLM-05 | Roadmap B 的局部结构单位是 7 类 FM-for-LLM action point。 | schema_seed | B-action | EV-FRLLM-08、EV-FRLLM-09 | strong | A2a 字段精核 | 不能转成效果统计 |
| CLM-FRLLM-06 | Section 5 的 ChatGPT 示例只能作为 illustrative evidence。 | evidence_boundary | E-example-type、E-llm-adjustment | EV-FRLLM-07 | strong | 证据强度降级 | 输出经作者调整且无实验协议 |
| CLM-FRLLM-07 | 本文可迁移的核心方法学是 concern→mechanism→artefact→limitation 的候选发现结构。 | candidate_heuristic | B-concern、B-assurance-mechanism、R-limitation | EV-FRLLM-09、EV-FRLLM-10 | medium | Paper2 候选 finding 生成 | 单篇 vision，需跨论文反证 |
| CLM-FRLLM-08 | 现有 `review.md` 需要返修：六叶接口不能作为原生树事实源。 | audit_repair | `review.md` 维度树复原 | EV-FRLLM-05--10 + `review.md` 行 318--360 | strong | review.md 最小返修 | 后续可保留六叶作为投影层 |
| CLM-FRLLM-09 | Fig. 2 / Fig. 4 已完成本轮 PDF 版面核验，但 listing / prompt box 未逐项核验。 | verification_status | PDF 核验状态 | EV-FRLLM-05、EV-FRLLM-08 | strong | A.4 核验清单 | 不覆盖全部图表/代码清单 |

### 9. 技能使用与自我审查记录

本轮已读取并采用以下技能 / 指南文件：

- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/SKILL.md`：采用 claim-evidence-engineering 原则，强结论必须有本地证据，证据不足则降级。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-guidelines.md`：采用 reviewer-quality objection 标准，返修意见需可操作、可定位。
- `/home/zhangshaoang/.codex/skills/ai-research-writing-skill/references/reviewer-self-review.md`：采用高风险先行、自我审查和 claim/evidence gap 思路。
- `/home/zhangshaoang/.codex/skills/research-planning/SKILL.md`：采用先理解研究上下文、再分解方法/任务/风险的规划方式。
- `/home/zhangshaoang/.codex/skills/research-planning/references/planning-prompts.md`：采用“严格跟随原文，不清楚就显式说明”的原则。
- `/home/zhangshaoang/.codex/skills/research-planning/references/output-schemas.md`：借鉴结构化输出、风险字段和任务依赖表达，但未伪造超出原文的信息。
- `/home/zhangshaoang/.codex/plugins/cache/oh-my-codex-local/oh-my-codex/0.18.7/skills/autoresearch/SKILL.md`：采用 artifact-gated / validator-gated 思路，最终报告以可审计证据表和结论映射闭合。

最高风险 3 点及主线程复核建议：

1. **风险：Fig. 2 / Fig. 4 的箭头关系未逐箭头编码。**
   复核：A2a 打开 PDF，逐个节点和箭头建立 source-target 表，确认是否存在我未列出的关系边。

2. **风险：取值空间“完整枚举”只对本文内部 action point 成立。**
   复核：合并时所有 `完整枚举` 后面应注明“限本文”，不得扩展为领域全集。

3. **风险：Section 7 limitation 的枚举是段落级归纳，非作者给出的正式 taxonomy。**
   复核：若写入 `review.md`，应标 `risk register seed` 或 `free text + rationale`，不要写成系统化 validity rubric。

本任务未出现 blocked、timeout 或文件缺失。未启动 subagent，未修改仓库文件，未 commit、push 或发布评论。