# 卡片 · Stateful Multi-Agent LLMs for Cross-View Interface Alignment in Automotive Model-Based Systems Engineering

⭐ **本卡的一句话结论**：⭐⭐ **它把「编造了不存在的元素」化约成一个纯集合公式** `T = |L ∩ C| / |L|`（时序图里的 lifeline 是否都在类图里声明过）—— ⭐ **这正是我们该抄的形态**。⛔ **但它只把这个公式当评测指标，流水线里真正拦截的仍然是一个 LLM Validator Agent。** ⚠️ 而它自己撞上了我们最担心的那个坑并给它起了名字：**"Critic-Hallucination Paradox"**。

⚠️⚠️ **数据可信度警示（⛔ 必须先读）**：本篇是**未经同行评审的 arXiv 预印本**，⛔ **n = 1 个场景**、⛔ 未报重复次数 / 方差 / 温度 / seed、⛔ Precision/Recall/F1 三个指标**没有定义**、⛔ 判定执行者未声明、⛔ 零资产公开、⛔ 参考文献 [27] 里留着未替换的占位符 `arXiv:2401.xxxxx`，⛔ 且**摘要与正文表格自相矛盾两处**（见 C 节 `adverse_results`）。⭐ **可搬的只有两个设计思路，⛔ 它的任何数字都不得引用为对照基线。**

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `stateful-multiagent-crossview-drift` |
| `title` | Stateful Multi-Agent LLMs for Cross-View Interface Alignment in Automotive Model-Based Systems Engineering |
| 作者 | Aleksei Velsh, Nenad Petrovic, Alois Knoll（Chair of Robotics, AI and Real-Time Systems, Technical University of Munich） |
| `year` | **2026**（v1 提交 2026-08-08 09:49:10 UTC，900 KB） |
| `venue` | ⛔ **arXiv 预印本**（`cs.SE`）—— ⛔ 未见任何会议 / 期刊投稿或录用声明 |
| `ccf` | ⛔ **无**（预印本，无 venue） |
| `arxiv` | [arXiv:2608.08038](https://arxiv.org/abs/2608.08038) · DOI [10.48550/arXiv.2608.08038](https://doi.org/10.48550/arXiv.2608.08038) · License **CC BY 4.0** |
| `url` | ⭐ 全文来源：[https://arxiv.org/html/2608.08038v1](https://arxiv.org/html/2608.08038v1)（本轮已下载 151,553 bytes 并全文转文本） |
| `artifact_type` | ⭐ **PlantUML 三视图** —— Class（结构）· Activity（行为）· Sequence（交互）；⭐ 信号取自 **VSS**（Vehicle Signal Specification, COVESA） |
| `task` | ⭐ **生成** + **跨视图一致性检查** + **修复**（打回重生成 / 回退上游） |
| `boundary` | ⭐ **邻域**（活动图 / 时序图；⛔ 无时钟、无正交并发语义） |

### ⭐ 硬门核对

| 硬门 | 判定 | 理由 |
| :-- | :-: | :-- |
| 1 · 基于 LLM | ⭐ **过** | LLM 是生成器**与**语义裁决者，是方法核心 |
| 2 · 行为类模型制品 | ⭐ **过** | Activity 图 + Sequence 图，PlantUML 文本模型 |

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐ **6 个阶段 · 其中 LLM 2 个**，另有 1 个 embedding 模型）

```
[人] NL 需求（序列化成 8 条 chronological Ground Truths）
  ↓  ── 顺序矩阵：Class → Activity → Sequence，上游锁定后注入下游 prompt ──
  → [LLM · Generator Agent，"tool-first"] 调 Pinecone 检索 VSS → 产出 PlantUML 草稿
  → [确定性] JavaScript 语法门（括号 / 组合箭头 / markdown 残留）→ 保证 100% 编译率
  → [LLM · Validator Agent] 语义审计：六桶分类学 → 输出 strict JSON payload
  → [确定性] n8n 路由：按 bucket 构造 dense diagnostic prompt 回灌 Generator；
             ⭐ 若根因在上游 Class，则**改写全局 loop index** 做 dynamic backtrack
  ⇄ 循环（上限 40）
  → [确定性] Kroki.io 渲染 SVG
```

⭐ **M** 逐字（§IV-A）：`"Once validated, this structural baseline is preserved in the orchestrator's global memory and injected directly into the prompt for the Activity diagram generation."`

⭐ **M** 逐字（§V-B，dynamic backtrack 的机制）：`"The programmable routing node overwrites the global loop index, forcing the orchestrator to revert to the Class generation phase. It injects the missing requirement, updates the structural diagram, and cascades the corrected interface down through the subsequent views."`

⚠️ **注意 `Activity → Sequence` 的顺序被声明为「越往后约束越多」**：**M**（§IV-A）：`"Finally, the Sequence diagram serves as the ultimate integration test. Its generation is constrained by both the structural interfaces of the Class diagram and the chronological flow dictates of the Activity diagram."`

### B2 · 每次 LLM 调用的角色

| 调用 | 角色 |
| :-- | :-- |
| Generator Agent | ⭐ **生成器** + **检索改写器 / 工具调用**（"tool-first" reasoning prompt，自己发起向量相似度检索） |
| Validator Agent | ⛔⛔ **评审者 + 裁决者 + 分类器**（判过 / 不过 · 归到六桶之一）—— ⛔ **本质是 LLM 自评的一种**（独立实例，但仍是 LLM 判 LLM） |
| n8n 路由 | ⭐ **不是** LLM —— 确定性 `switch` / index 改写 |

⭐ **M**（§IV-B）：`"Diagrams that pass syntax validation are audited by an independent AI Validator Agent. This agent is explicitly isolated from the generation process and acts as a semantic critic."`

### B3 · prompt 策略

| 项 | 值 |
| :-- | :-- |
| 策略 | ⭐ `RAG`（Pinecone 向量库）· `工具调用`（"tool-first" 强制先检索后生成）· `结构化输出约束`（Validator 输出 strict JSON）· `多智能体`（generator vs adversarial critic）· **上下文注入**（上游已验证制品进下游 prompt）· **诊断反馈回灌**（按 bucket 构造 dense diagnostic prompt） |
| ⛔ 无 | `few-shot` 示例（未提及）· `CoT`（只在参考文献里引 [28]）· `self-consistency` 投票 |
| ⭐ prompt 是否公开 | ⛔⛔ **未公开** —— 全文无 prompt 原文、无附录、无仓库 |

### B4 · ⭐⭐ 循环与裁决者（⛔ 本卡最关键的一格）

⭐⭐ **双层裁决者，且两层的性质截然不同。**

| 层 | 裁决者 | 类型 | 它能拦什么 |
| :-- | :-- | :-- | :-- |
| **第一层** | JavaScript 语法解析脚本 | ⭐ **确定性规则 / parser** | ⭐ 括号不平衡、箭头畸形、markdown 残留 → **保证 100% PlantUML 编译率** |
| **第二层** | **AI Validator Agent** | ⛔⛔ **LLM 自评**（独立实例，⛔ 非 sound oracle） | ⛔ 一切语义问题：接口不兼容、类型不匹配、幻觉组件、需求遗漏、擅自删基线 |

⭐ **M**（§IV-B 第一层）：`"The first layer utilizes a programmatic parsing script (JavaScript) to execute deterministic syntax validation on the raw PlantUML output. It instantly rejects unbalanced brackets, malformed composition arrows, and formatting drift, guaranteeing 100% compilation success without wasting LLM inference cycles on basic syntax."`

⛔ **作者自己承认第二层不是 sound oracle** —— **M**（§VIII 限制 4）：`"The AI Validator successfully proves semantic interface compatibility, but lacks formal verification capabilities (e.g., TLA+ checking). The AI can verify that a braking command is logically routed, but cannot calculate if the braking torque will physically stop the vehicle."`

| 子字段 | 值 |
| :-- | :-- |
| 有无循环 | ⭐ **有**，且带 **dynamic backtrack**（下游失败可回退改上游） |
| 终止条件 | ⭐ 收敛（"until absolute cross-view interface compatibility is achieved"）**或** 最大轮数 |
| **最大轮数** | ⛔⛔ **40**（硬上限）—— **M**：`"This cyclical, multi-agent deliberation iterates (capped at 40 loops to prevent critic-hallucination gridlock) until absolute cross-view interface compatibility is achieved"` |
| ⭐ 有无报循环边际收益 | ⚠️ **有，但只有轮数分布，⛔ 没有逐轮指标曲线** |

⭐ **逐字抄下所有轮数数字**（§VII-D）：

- **M**：`"The multi-agent system did not achieve a zero-error state on the first generation pass. On average, achieving structural compliance required between 3 to 6 cyclical validation loops per diagram type."`
- **M**：`"Bucket 6 (Interface Incompatibilities) and Bucket 3 (Hallucinated Components) accounted for over 70% of the triggered backtracking loops."`
- **M**：`"The generation of static Class diagrams typically converged within 1 to 2 iterations … Conversely, Sequence diagrams, which demand simultaneous tracking of temporal control flows and strict structural typing, required the maximum average iterations (5.4 loops) before satisfying the Validator Agent's interface compatibility matrix."`
- **M**（§VIII 限制 2）：`"Achieving absolute traceability requires significant cyclical reasoning, averaging 282.6 seconds per scenario."`

⛔⛔ **但它没有报我们最想要的那个东西**：⛔ **第 k 轮之后 Traceability 涨了多少**。⭐ 表 II 只有四档配置的**终值**，⛔ 没有任何「第 1/2/3/4/5 轮的指标」。⚠️ **所以本篇无法用来验证或否证我们「第 3–5 轮零收益」那条实测** —— ⭐ 只能说明「他们的循环平均要跑 3–6 轮才停」，⛔ 而「跑到第 6 轮时新增收益是否为零」这个问题原文未提供。

⭐⭐ **生产者能否推翻裁决？** ⛔ **原文未明说**（未提供），⭐ 但据 §VIII 限制 3 可直接推出（**S**）：**不能** —— 生产者唯一的出路是重生成；validator 误拒时生产者被逼死，唯一逃生口是 40 轮硬上限后转人工。

⛔⛔ **M** 逐字（§VIII 限制 3，⭐ **本卡对我们最有价值的一段**）：`"The 'Critic-Hallucination' Paradox: A fundamental theoretical limitation of employing an LLM as a semantic critic is the risk of second-order hallucinations, where the Validator Agent unjustly rejects a valid interface [14]. This forces the Generator into a state of confusion. To prevent infinite adversarial gridlock, the orchestrator relies on a hard 40-iteration cap, after which manual intervention is required."`

⭐⭐ **这与我们 §13「多道门交集为空」是同一类事故的两种形态**：⛔ 他们是**单个 LLM 门的假阳性**（门的判据本身不稳定），⛔ 我们是**多个确定性门的合法解空间为空**（每道门都稳定但交集空）。⭐ **共同点是：被卡住的一方没有任何合法写法能通过。** ⛔ **而他们的处理方式正是我们 §10 明令禁止的形态**：耗尽上限之后**没有产物**（`"manual intervention is required"`），⛔ 不是降级落盘 + 结构化诊断。

### B5 · ⭐ 中间表示（⭐ **两个，别只看第一个**）

**中间表示 ①：六桶错误分类学（Six-Bucket Error Taxonomy）**

| 子字段 | 值 |
| :-- | :-- |
| 有无 | ⭐ **有** |
| 形态 | ⭐ **缺陷类型学**（⛔ 不是谓词族、不是 DSL） |
| ⭐ **是否闭合** | ⭐⭐ **闭合** —— 固定 6 个桶 |
| ⭐ **谁选类** | ⭐⭐ **LLM 自动选**（Validator Agent 把失败归桶） |

⭐ **M** 逐字（§IV-B，六桶全文）：`"the Validator Agent is governed by a novel Six-Bucket Error Taxonomy: (1) Target Diagram Misalignment, (2) Syntax/Logic Breaks, (3) Hallucinated Components, (4) Missing Requirements, (5) Unwarranted Baseline Deletions, and crucially, (6) Interface Incompatibilities."`

⭐ **M**（§V-B）：`"it outputs a strict JSON payload categorizing the failure based on the six-bucket taxonomy."`

⚠️⚠️ **这是「闭合集 + LLM 自动选」的一个实例，⛔ 但它与我们的 19 条谓词词表不是同一件事，⛔ 不得当成先例登记。** ⭐ 三条硬差别：

1. ⛔ **分类的对象不同** —— 他们的桶给**已经被发现的失败**贴标签（事后归因）；⭐ 我们的谓词决定**该问什么**（事前选题）。⛔ **前者是分类问题，后者是规划问题。**
2. ⛔ **规模差一个量级** —— 6 vs 19，⛔ 且六桶里有 2 桶（Syntax/Logic Breaks、Target Diagram Misalignment）根本不是语义判定。
3. ⛔ **选错的代价不同** —— 他们归错桶只影响回灌 prompt 的措辞（仍会重生成）；⛔ 我们选错谓词那一位就直接不可能命中。

**中间表示 ②：⭐⭐ VSS 信号目录（⛔ 这个对 M1 更有意思）**

| 子字段 | 值 |
| :-- | :-- |
| 形态 | ⭐ 外部标准本体，flattened **JSON Lines**，字段 `signal_id` / 层级 `name` / `datatype`（M，§V-A） |
| ⭐ **是否闭合** | ⭐⭐ **闭合，且是硬闭合** —— 不在 VSS 里的信号一律不许生成 |
| ⭐ **谁选类** | ⭐ **向量相似度检索（确定性）**，⛔ 由 LLM 发起（"tool-first" 强制先检索） |

⭐⭐ **这一格才是可搬的形状**：**闭合词表 + LLM 发起检索 + 确定性相似度返回候选**。⭐ 对照我们：19 条词表**整表塞进 prompt 让 LLM 直接选**。⚠️ **他们那种「检索式选类」在我们 19 条的规模上未必必要**（19 条塞得进上下文），⛔ 但它提供了一个「选类不必由 LLM 独自完成」的存在性证明。

⭐ 作者自己指出这个硬闭合的代价 —— **M**（§VIII 限制 5）：`"Because it is intrinsically tied to the VSS JSONL dataset, it suffers from ontology gaps. If an engineer requests a proprietary sensor dynamic not formalized in the vector database, the pipeline's anti-hallucination guardrails actively prevent its design."` ⚠️ **这正是我们「15/19 使用率」问题的另一面**：⛔ 闭合词表的完备性缺口会表现为**方法主动拒绝正确的东西**。

### B6 · 模型

| 角色 | 型号 |
| :-- | :-- |
| Validator Agent | ⚠️ **GPT-4**，⛔ 但措辞是 `"e.g."` 且引的是 GPT-4 技术报告（[22] OpenAI 2023）—— **M**：`"When the AI Validator Agent detects an interface mismatch (e.g., via the GPT-4 architecture [22])"`。⛔ **精确型号 / 快照 / 版本未提供** |
| Generator Agent | ⛔⛔ **原文未提供** —— 全文未指名生成器用什么模型 |
| Embedding | ⭐ `models/gemini-embedding-2`，3072 维（M，§V-A）—— ⚠️ 但引的来源是 [8] **Gemini 2023 技术报告**，⛔ 时间上对不上，型号真实性未核 |
| 推理载体 | ⭐ TUM LRZ 超算集群（"To ensure data privacy and mitigate commercial API rate limiting"，M），⚠️ 与「用 GPT-4」在部署上互相矛盾（⛔ GPT-4 不能自托管） |
| 多模型对照 | ⛔ **无** |

⚠️⚠️ **这一格是本篇最不可靠的一格。** ⛔ **两个 LLM 里有一个完全没指名、另一个只给了 `e.g.` 级别的措辞**，⛔ 而 §VIII 限制 7 恰恰自己写着「模型版本漂移会破坏可复现性」（`"A prompt template that yields a 100% compilation rate today may trigger novel hallucination patterns following a model update."`）—— ⛔ **它论证了记录精确型号的必要性，自己却没记。**

### B7 · ⭐ 确定性成分

| 环节 | 是什么 | 承重程度 |
| :-- | :-- | :-- |
| JavaScript 语法门 | PlantUML 语法解析 | ⭐ 硬承重（100% 编译率），⛔ 但只管语法 |
| n8n 编排 / 全局状态 | 状态锁定、loop index 改写、bucket 路由 | ⭐ 硬承重（整个 statefulness 靠它） |
| Pinecone 向量检索 | 相似度搜索 | ⭐ 承重（VSS 闭合靠它） |
| Kroki.io | SVG 渲染 | 非承重 |
| 指标计算 `T` / `S` | ⭐ **纯集合公式**（$T = \vert L \cap C\vert / \vert L\vert$、$S = \vert A \cap GT\vert / \vert GT\vert$） | ⚠️ **只用在评测端，⛔ 不是流水线组件** |
| ⛔ sound oracle | ⛔⛔ **完全没有** | ⛔ 作者自己承认缺 TLA+ |

⭐⭐ **对 M1 最关键的一条观察**：⭐ 他们**已经有了**一个可以当门用的确定性引用检查（`T = |L∩C|/|L|`，⛔ 且论文明写 `"A score below 100% definitively indicates a cross-phase structural hallucination"`），⛔ **却只把它拿来算分，没有把它接进循环当门。** ⭐ 流水线里拦截「幻觉组件」的仍然是 LLM Validator 的 Bucket 3。⚠️ **这是一个被浪费掉的确定性底座。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **有 · 四档自身 ablation**：① Zero-Shot ② Grounded RAG Only ③ RAG + Static Val. ④ Proposed Workflow。⛔ **无任何外部方法 baseline** —— MetaGPT / SWE-agent / Stephan et al. / Misini et al. / Req2Road 只在 Table I 做**定性**对照（"Cross-View Interface Validation: No/No/No/Partial"），⛔ 一个都没实跑 |
| `dataset` | ⛔⛔ **n = 1 个场景** —— Child Presence Detection (CPD)，序列化成 **8 条 chronological "Ground Truths"**（M：`"the CPD requirements were serialized into eight distinct chronological 'Ground Truths' (GTs)"`）。⭐ 分母：`S` 的分母是这 8 条 GT；`T` 的分母是时序图 lifeline 集合 $L$（⛔ **$\vert L\vert$ 的具体数值原文未提供**）。⛔ 场景不公开 |
| `metrics` | ⭐ PlantUML 编译率 · Entity Recall · State Reachability · ⭐⭐ **Entity Traceability** $T = \vert L \cap C\vert / \vert L\vert \times 100$ · ⭐ **Signal Conservation** $S = \vert A \cap GT\vert / \vert GT\vert \times 100$ · Precision / Recall / F1。⛔⛔ **P / R / F1 三个指标全文没有定义** —— 表 II 有数字但从未说明「对什么算」「分母是什么」。⛔ **无 `@k` 口径** |
| ⭐ `judged_by` | ⛔⛔ **原文未提供** —— 全文未声明判定由谁执行。⭐ `T` 与 `S` 是集合公式，**可**脚本化（**S** 级推断，⛔ 但原文未说是脚本算的）；⛔ 而 Entity Recall / State Reachability / P / R / F1 的判定主体、判定材料、判定次数**全部未给**。⛔ **无标注者一致性 · 无 $\kappa$ · 无第三方 · 无 LLM-as-judge 声明** |
| `human_baseline` | ⛔ **无** |
| `runs` | ⛔⛔ **未提供** —— 跑几次、温度、seed、是否重复全无。⭐ 表 II 是**单组数字**，⛔ 无方差 / 无区间。⚠️ `"On average … 3 to 6 loops"` 与 `"averaging 282.6 seconds per scenario"` 暗示多次运行，⛔ **但样本量从未给出** |
| ⭐ `adverse_results` | ⛔⛔ **处理方式与我们相反，且存在两处内部矛盾** |

### ⛔⛔ `adverse_results` 详析（⭐ 本节是本卡的反面教材价值所在）

**做法**：主结果全部对自己有利（97% / 87% / 85%），⛔ 不利内容**全部搬进 §VIII 的 8 条定性 Limitations**，⛔ 且那 8 条**一个数字都不带**（唯一带数字的是 282.6 s 与 40 轮上限）。⭐ 对照我们 v46 把 `Δ = −15.82pp` 直接写进主结果 —— ⛔ **两种态度。**

**⚠️ 矛盾 ①（⭐ 摘要 vs 表 II，⛔ 双方逐字）**

- 摘要 **M**：`"Evaluated on an Advanced Driver Assistance System (ADAS) scenario, standard RAG yielded 0% Entity Traceability."`
- 表 II **M**：`2: Grounded RAG Only` 一行的 Traceability = **34%**；`1: Zero-Shot Baseline` = **18%**。
- ⛔ **没有任何一档配置是 0%。** ⚠️ 摘要把最不利于 baseline 的数字**夸大到了表格之外**。

**⚠️ 矛盾 ②（⭐ 正文 vs 正文，⛔ 更硬，因为判据是他们自己定的）**

- §VI-B **M**：`"A score below 100% definitively indicates a cross-phase structural hallucination, meaning the AI fabricated an interface in the dynamic view that lacks a structural foundation."`
- 表 II **M**：Proposed Workflow 的 Traceability = **97%**。
- 摘要 **M**：`"our multi-agent workflow eradicated cross-phase hallucinations"` · `"This proves adversarial auditing enables LLMs to reliably synthesize zero-error MBSE architectures."`
- ⛔⛔ **按他们自己写的判据，97% < 100% 就「definitively」意味着仍有跨视图结构幻觉** —— ⛔ 因此 `"eradicated"` 与 `"zero-error"` 与自己的判据直接冲突。⚠️ `zero-error` 一词在全文出现 **4 次**（摘要 / §VI / §VII-D / §IX），`This proves` 出现 **2 次**。

⭐⭐ **这两处矛盾对我们的价值**：⭐ 它们是「⛔ **导语与标题必须与正文同步**」这条纪律（[talks/GUIDE.md](../../../../../talks/GUIDE.md) §9 / 仓库 CLAUDE.md §7.5）的一个现成反例 —— ⛔ **正文的判据已经否掉了摘要的卖点，而摘要仍在用它当卖点。** ⭐ 可在 M1 的报告纪律里当负面案例引。

---

## D. 资产

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（⭐ `tools.verify_assets` 输出逐字） |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arxiv.org/abs/2608.08038](https://arxiv.org/abs/2608.08038) | `🟢 HTTP 200 · text/html; charset=utf-8` ⭐ HTML 全文 [arxiv.org/html/2608.08038v1](https://arxiv.org/html/2608.08038v1) 已下载 **151,553 bytes**，转文本 1,252 行，含全部 9 节 + 35 条参考文献。⭐ CC BY 4.0 |
| ⭐ **实验代码 / n8n workflow** | ⛔ ⚪ | —— | ⛔ **原文未提供** —— 全文 grep `github` / `available` / `zenodo` / `artifact` / `repositor` 后，⛔ **命中全部是 arXiv 页面自带的「Report GitHub Issue」控件、参考文献标题、或正文里 `artifact` 一词的普通用法**。⛔ **无仓库、无 workflow JSON 导出、无 n8n 节点定义** |
| ⭐ **数据集 / Benchmark** | ⛔ ⚪ | —— | ⛔ **原文未提供** —— CPD 场景的 8 条 GT **未公开**（正文只举了 GT3 一例：`vehicle.cabin.seat.row2.passenger_side.isOccupied`）。⛔ 无 ground-truth 文件、无需求原文、无 Deterministic Logic Rubric 全文 |
| VSS 目录（**非本文产物**） | ⚠️ 🟢（第三方） | COVESA VSS | ⚠️ 论文只引 [6]「COVESA Alliance (2022) Vehicle Signal Specification (VSS) release documentation」，⛔ **未给他们实际使用的 VSS 版本号**，⛔ 也未给 flattened JSONL 的生成脚本。⭐ VSS 本体是公开标准（⛔ 本轮未独立核验其入口，因为不是本文资产） |
| 实验结果细则 | ⛔ ⚪ | 论文 Table II | ⭐ Table II（4 档 × 5 指标 = 20 个数）已逐字抄入本卡 C 节；⛔ **无逐条结果、无 execution log、无 Validator JSON payload 样本** —— ⚠️ 而正文多处以 "execution logs reveal" 作为论据（§VII-A、§VIII），⛔ **那些日志一份都没放出来** |
| Artifact / 复现包 | ⛔ ⚪ | —— | ⛔ **原文未提供** |
| ⭐ **prompt 是否公开** | ⛔ ⚪ | —— | ⛔⛔ **未公开** —— 六桶分类学的**名字**给了，⛔ 但 Generator 的 "tool-first" prompt、Validator 的审计 prompt、dense diagnostic prompt 模板**一个字都没给**。⚠️ 而 §VIII 限制 6 自称 `"The generative agents remain highly sensitive to input perturbations"` —— ⛔ **prompt 敏感却不公开 prompt，本篇不可复现** |

⛔⛔ **资产结论：除论文本身外，全部 ⚪。** ⭐ 本篇对 M1 只能贡献**设计思路**，⛔ 贡献不了任何可运行的东西。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

1. ⭐⭐⭐ **`T = |L ∩ C| / |L|` 这个集合公式，可以直接搬成我们的「运行期主张锚在不存在元素上」的检测器。** ⭐ 它把一个看起来需要语义判断的问题（「模型编造了元素吗」）化约成**纯集合交运算**：动态视图里出现的每个标识符，是否都在结构视图里声明过。⛔ **不需要任何 LLM，不需要任何门，不需要 `depends_on` 闭包，不需要 `blocked_by`。** ⚠️ 对照我们现状：为同一件事我们加了引用门 + `depends_on` 闭包 + `blocked_by` + 满足性只数 `primary`/`precondition` + 证据族门 —— ⭐ **五条互相牵制的约束，且它们的交集曾经为空（v44：22/35 格降级、97 次降级事件）。** ⭐⭐ **这条是本卡对 M1 最直接的一条可搬项。**
2. ⭐⭐ **「跨视图冗余当确定性过滤器」这个思路本身。** ⭐ **M** 逐字（§II-D）：`"hallucinating a non-existent VSS signal in a Sequence diagram inherently triggers an interface incompatibility when cross-referenced against the preceding Class diagram"` · `"Enforcing cross-view consistency thus acts as a deterministic filter: isolated hallucinations surface as interface contradictions caught by the critic agent, forcing the LLM to synthesize holistically integrated architectures"`。⭐ **要点是：让制品在两个地方各表达一次同一件事，矛盾自己就浮出来，于是语义问题变成机械比对问题。** ⭐ 这个思路对我们的 `named_elements` ⇄ 模型声明、断言引用 ⇄ 元素表都成立。
3. ⭐ **把语法门放在语义门之前，且明确理由是省 LLM 调用。** ⭐ **M**：`"guaranteeing 100% compilation success without wasting LLM inference cycles on basic syntax."` ⭐ 我们的 `precheck_and_seal` 已经是这个形状（0 token、性价比最高），⭐ **本篇提供了一条外部佐证。**
4. ⭐ **`dynamic backtrack`：下游发现的问题允许回退去改上游。** ⭐ 我们的流水线是单向的（split → convert → release），⛔ `convert_assertions` 发现需求切分有问题时**没有回头路**。⚠️ 值得考虑，⛔ 但注意成本（他们平均 3–6 轮、282.6 s/场景，且这个机制正是「critic 误拒」放大器）。
5. ⭐ **"Critic-Hallucination Paradox" 这个命名可以直接借用。** ⭐ 我们需要一个词来指「裁决者假阳性把生产者逼死」，⛔ 而这篇给了一个已在文献里出现过的名字（虽然出处只是预印本）。

### 2. ⛔ 不可取 / 陷阱（⛔ 它踩了我们踩过的坑，⛔ 而且踩得更深）

1. ⛔⛔ **语义裁决者是 LLM，且没有任何 sound oracle 兜底。** ⭐ 这正是我们 X1 已经证否的形态（两个 LLM 自评 reviewer 零收益、吃 79% token）。⛔ **本篇的 Validator 更危险**，因为它是**唯一的**语义门（我们至少还有 pyfcstm 在求值端）。⚠️ 且作者自己把风险写在限制里 —— ⛔ **即「LLM 当语义裁决者」这条路在文献里已被其倡导者本人标注为有理论缺陷。** ⭐ M1 可以引这句。
2. ⛔⛔ **耗尽即无产物。** ⭐ 40 轮上限之后 `"manual intervention is required"` —— ⛔ **没有降级落盘、没有结构化诊断、没有残缺产物。** ⚠️ 这正是仓库 §10 明令禁止的形态：⛔ 最容易撞上限的恰恰是缺陷最硬的样本，⛔ 于是**信息量最大的那些格从被测集里消失**。⭐ **我们不要退回这个形态。**
3. ⛔ **确定性检查被降级成评测指标。** ⭐ 他们手里有 `T` 这个可以当门的公式，⛔ 却让 LLM 的 Bucket 3 去干同一件事。⚠️ **这是我们的镜像错误**：我们把 sound oracle（pyfcstm）放在求值端而非裁决端，⛔ 他们把确定性引用检查放在评测端而非门上。⭐ **两边都在同一件事上做错了同一个方向的选择** —— ⭐ 这条对照本身就是 M1 第二条设计原则的论据。
4. ⛔ **闭合本体的完备性缺口会伪装成「方法主动拒绝正确答案」**（§VIII 限制 5，逐字见 B5）。⚠️ 我们的 `15/19` 使用率问题必须按这个方向也查一遍：⛔ 有没有正确的东西被词表挡在外面。
5. ⛔ **报告纪律的反面教材**：⛔ 摘要夸大 baseline 的失败（0% vs 表里 34%）、⛔ 结论与自己的判据冲突（97% vs "zero-error"）、⛔ 反复用 `This proves` / `mathematically guarantee` / `definitively` 这类过强措辞、⛔ 引用里留占位符 `arXiv:2401.xxxxx`。⭐ **这一组问题合起来正好是我们 §3.7「报告自包含」与 §7.5「导语与正文同步」要防的东西。**

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

1. ⛔⛔ **它的 `T` 之所以能纯机械算，是因为「结构视图」这个 ground truth 是流水线自己先产出并锁定的。** ⭐ 我们的对应物是**模型的元素声明**（也在制品里，所以这条**可以搬**）；⚠️ **但我们真正难的那部分不是这个** —— 我们要判的是「制品有没有违背 NL 需求」，⛔ 而 NL 需求侧**没有一个可枚举的元素集合**能拿来做交运算。⭐ **所以 `T` 能解决我们「主张锚在不存在元素上」这一类，⛔ 解决不了「该问什么」那一类。**
2. ⛔ **数字完全不可比。** ⛔ n=1 场景、无重复、无方差、P/R/F1 无定义、判定主体未声明、零资产 —— ⛔ **不得进 L1 的外部可比数字表**，⛔ 也不得写成「文献报告 97% 而我们 60.4%」。⭐ 按 [README.md](../README.md) §3 的防火墙，本卡内容是方法素材，⛔ 不是论文证据。
3. ⚠️ **"stateful" 的含义比字面弱得多。** ⭐ 它指的是 **n8n 编排器的全局内存里锁定上游已验证制品并注入下游 prompt**，加上**可编程改写 loop index** 实现回退 —— ⛔ **这是工作流状态（workflow state），不是 agent 的长期记忆、不是跨会话状态、不是学习。** ⭐ 我们的 LangGraph state 已经是同一层级的东西，⛔ 所以这个词在本篇不构成新机制。⛔ 论文里不可把它引成「有状态多智能体」这类更强的说法。
4. ⚠️ **制品类型不同**：他们是 UML 三视图（Class/Activity/Sequence，PlantUML），⭐ 我们是 pyfcstm DSL 单一制品（FSM/HSM/EFSM）。⛔ **「跨视图冗余」在我们这里没有现成的第二视图** —— ⭐ 要用这条思路，得先想清楚我们的「第二视图」是什么（候选：`named_elements` 表 vs 模型声明；断言引用 vs 元素表）。⛔ 这是 M1 要设计的东西，不是照搬。

---

## F. 存疑与未核项

1. ⛔⛔ **Generator Agent 用什么模型 —— 原文未提供。** 已在全文 grep `GPT` / `gpt` / `gemini` / `llama` / `claude` / `model used`，⭐ 唯一的型号线索是 Validator 的 `"e.g., via the GPT-4 architecture [22]"` 与 embedding 的 `models/gemini-embedding-2`。⛔ 生成器零线索。
2. ⚠️ **`models/gemini-embedding-2` 型号真实性未核** —— 论文引的支撑来源是 [8] Gemini 2023 技术报告，⛔ 时间对不上。⭐ 本轮**未**去 Google 官方文档核这个型号是否存在（⚠️ 若要核，按 CLAUDE.md 应走 [llm_model_landscape/04-gemini-models.md](../../../../../llm_model_landscape/04-gemini-models.md)）。
3. ⛔ **跑了几次 / 温度 / seed / 是否单次 —— 原文未提供。** ⭐ grep `repeat` / `trial` / `runs` / `seed` / `temperature` 后仅命中「ambient temperature」这类无关用法。
4. ⛔ **Precision / Recall / F1 的定义 —— 原文未提供。** ⭐ 表 II 有 12 个 P/R/F1 数字，⛔ 全文从未说明对什么算、分母是什么、正例是什么。⛔ **表 II 的 F1 列不可解读。**
5. ⛔ **判定执行者 —— 原文未声明。** ⭐ `T` / `S` 是集合公式（**S**：可脚本化），⛔ 但 Entity Recall / State Reachability 的判定主体、材料、次数全无；⛔ 是否有人类复核未提。
6. ⛔ **`|L|`（时序图 lifeline 数）具体是多少 —— 原文未提供。** ⚠️ 这直接决定 97% 的含义（**I** 级：看起来 `|L|` 需在 30 上下才能出现 97% 这个数，⛔ 但这只是我方推测，⛔ 原文没给，也可能是多次运行的平均）。
7. ⛔ **40 轮上限实际触发过几次 —— 原文未提供。** ⚠️ 这是本篇最该报而没报的数字：⛔ 它等于「有多少格因为 critic 误拒而无产物」。
8. ⛔ **`"3 to 6 loops per diagram type"` 与 `"5.4 loops"` 的分母未给** —— ⛔ 平均是在几次运行、几个 diagram 上取的未说明。
9. ⛔ **逐轮指标曲线不存在** —— ⚠️ 因此**本篇无法用于验证或否证我们「第 3–5 轮零收益」那条实测**（详见 B4）。⛔ 不要在 M1 里把它当那条发现的外部佐证。
10. ⚠️ **参考文献 [27] 逐字为 `"X. Wang et al. (2024) A survey on multi-agent large language models. arXiv preprint arXiv:2401.xxxxx"`** —— ⛔ **占位符未替换**。⭐ 这是一条 rigor 红旗，⛔ 也说明本篇未经同行评审。⚠️ 我**没有**逐条核验其余 34 条参考文献的真实性（⛔ 按 [EXTRACTION_SCHEMA.md](../EXTRACTION_SCHEMA.md) 通用纪律 3，只有我自己写进卡片的 DOI / arXiv id 才是我核过的：⭐ 本卡只写了 `arXiv:2608.08038` 与 `10.48550/arXiv.2608.08038`，⭐ 两者均已实际访问）。
11. ⚠️ **是否已投稿 / 录用未知** —— ⛔ arXiv 页面无 journal-ref、无 comments 说明 venue。⭐ 有 EU Chips JU 项目致谢（HAL4SDV, FPA No. 101139789）。
12. ⚠️ **一处内部不一致我未能解释**：⛔ 声称推理走 TUM LRZ 集群「以规避商业 API 限流」，⛔ 却又说 Validator 用 GPT-4（不可自托管）、embedding 用 Gemini（同样是商业 API）。⭐ 可能指只有部分组件走集群，⛔ 但原文未澄清。
