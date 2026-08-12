# 卡片 · Accurate and Consistent Graph Model Generation from Text with Large Language Models（AbsCon, MODELS 2025）

⭐ **本卡的一句话结论**：⭐⭐ **这是本轨里最强的一条「反循环」证据** —— ⛔ 它**一轮迭代都没有**、⛔ 一次 LLM 自评都没有、⛔ 一次修复调用都没有，⭐ 却把约束一致性做到 **96.6%–100%**。⭐⭐ **它的做法是把「满足约束」这件事从 LLM 手里整个拿走，交给一个 0/1 整数规划求解器（CBC）**：⭐ LLM 只负责**并行采 `n` 个候选**（⛔ 候选之间互不可见），⭐ 然后由求解器在候选并集里选一个既满足全部约束、又最大化元素存在概率的子集。⭐⭐ **一次 LLM 阶段 + 七八个确定性阶段。**

⛔⛔ **但它对我们的直接可比性很有限，⭐ 有三条硬限制必须先读（见 §0）**：⛔ ① **制品不是状态机**；⛔ ② **它只能从候选并集里「减」，永远无法「补」缺失元素**；⛔ ③ **它的 `consistent` 只管结构良构性，⛔ 完全不管语义正确性** —— ⭐ 而我们做的恰恰是语义层的缺陷检测。

⚠️ **一条与本轨另一张卡的联系**：⭐ **Boqi Chen 与 Gunter Mussbacher 同时是 [`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md) 的作者** —— ⭐⭐ **同一个 McGill 组，⭐ 同一年，两条完全相反的技术路线**（⭐ 那篇：多步 prompting，零求解器；⭐ 这篇：单步采样，全靠求解器）。⭐ 这个对照本身有信息量，⭐ 见 §E.4。

---

## 0. ⛔⛔ 三条硬限制（⭐ 放最前，⛔ 引用前必读）

| # | 限制 | 后果 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **制品不是状态机** —— ⭐ 统一制品是**通用带标签图** `G = (𝒩, ℰ, L)`；⭐ 三个案例分别是**流程图/活动图**（行为）、**分类树**（结构）、**Clevr 程序图**（可执行） | ⛔ **不得把它当作状态机工作引用。** ⭐ 全文零状态、零事件、零守卫、零层次态、零迁移系统语义。⭐ **硬门 2 只在 1/3 个案例上过**（⭐ 见 §A.2） |
| **2** | ⛔⛔ **concretization 只能从候选并集里「选子集」，⭐ 永远无法「补」一个候选都没产出的元素** | ⭐⭐ **recall 的上界被候选并集钉死。** ⭐ 论文自己承认与「best candidate」仍有差距。⛔ **所以它不是「修复」方法，⛔ 是「筛选」方法** |
| **3** | ⛔⛔ **`consistent` 只管结构良构性（well-formedness），⛔ 不管语义正确性** | ⭐ 它的 `Con` 是「有多少个模型满足全部约束」的**整模型二值率**；⭐ `accurate` 那一轴则是**对着参考图**比，⛔ **不是对着自然语言比**（⭐ 论文明说自动比 NL 不可靠）。⛔⛔ **所以它与我们「模型 vs NL 需求」的缺陷检测不是同一个问题** |

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `accurate-consistent-graph-model-generation` |
| `title` | **Accurate and Consistent Graph Model Generation from Text with Large Language Models** —— ⚠️ **完整标题比任务里给的长**：⛔ 缺的是 `from Text with Large Language Models` |
| 方法名 | ⭐ **AbsCon**（abstraction–concretization） |
| 作者 | **Boqi Chen**（McGill + Huawei Research Canada 实习）· **Ou Wei**（Huawei Research Canada）· **Bingzhou Zheng**（Huawei Research Canada）· **Gunter Mussbacher**（McGill） |
| ⭐ 脚注 | ⭐ 逐字：`"Work partially done during an internship at Huawei Research Canada."`；⭐ 致谢 `"We thank Dániel Varró, Zohreh Aghababaeyan, Khaled Ahmed, Ru Ji, and anonymous reviewers"` |
| `year` | **2025** —— ⭐ Crossref `issued = [[2025, 10, 5]]` |
| `venue` | ⭐⭐ **MODELS 2025** · `2025 ACM/IEEE 28th International Conference on Model Driven Engineering Languages and Systems (MODELS)` —— ⭐ Crossref `container-title` 实取确认。⭐ **Research Papers 主会track**，⛔ **不是 workshop**；⭐ 页码 **130–141 = 12 页**（⭐ Crossref `page = 130-141` 实取确认） |
| `ccf` | ⭐⭐ **B** —— ⭐ 本仓库 [ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 实取命中该行，其字段依次为 `conf-b-models` / `MoDELS` / `会议` / `🥈`，备注逐字「建模与模型驱动核心 venue，P1 核心。」 |
| `doi` | ⭐⭐ [10.1109/MODELS67397.2025.00018](https://doi.org/10.1109/MODELS67397.2025.00018) —— ⭐ **本轮我方独立在 Crossref API 实取核对**：标题、container、页码、四位作者、`type = proceedings-article` 全部一致 |
| `arxiv` | ⭐⭐ [2508.00255](https://arxiv.org/abs/2508.00255)（v1, `cs.SE`, **2025-08-01**, ⭐ CC BY 4.0）—— ⭐ **本轮实测 `abs` HTTP 200、`html/2508.00255v1` HTTP 200**，⭐ 并已下载全文（244,302 bytes HTML → 76,849 字符正文）**逐节通读** |
| `url` | ⭐ **本卡全文来源**：[arXiv HTML v1](https://arxiv.org/html/2508.00255v1)（⭐ 完整，含全部章节 + 参考文献 + Table I，⛔ 非仅摘要） |
| `artifact_type` | ⚠️ **通用带标签图** `G = (𝒩, ℰ, L)`，⭐ 序列化为 **Mermaid** 文本。⭐ 三个案例：⭐ ① **流程图 / UML 活动图**（行为）· ⭐ ② **WordNet 分类树**（结构）· ⭐ ③ **Clevr 程序图**（可执行） |
| `task` | ⭐ **生成 + 一致性保障**（⭐ 一步出，⛔ 无修复循环）—— ⛔ **不是**缺陷检测、⛔ 不是修复、⛔ 不是追溯 |
| `boundary` | ⚠️ **邻域（1/3）+ 界外或不适用（2/3）** —— 见 §A.2 |

### A.1 ⛔⛔ 硬门核对（⭐ 本卡这一格必须如实写）

| 硬门 | 判定 | 理由 |
| :-- | :-: | :-- |
| **1 · 基于 LLM** | ⭐ **过** | ⭐ LLM 是候选来源，⭐ 整个方法围绕「如何用好 LLM 的多次采样」设计。⚠️ **但只占 1 个阶段**（⭐ 见 §B1） |
| **2 · 行为类模型制品** | ⚠️⚠️ **部分过 —— ⭐ 1/3 个案例过，⛔ 2/3 不过** | ⭐ **过的那一个有作者自己的逐字背书**：`"Flowcharts serve as example behavioral models targeted by model generation."`（§IV 开头）⭐ 且 artifact 的 prompt 逐字自称 `"You are an expert software modeler who can create an UML activity diagram from a text description"` —— ⭐⭐ **UML 活动图在 [README.md](../README.md) §2 硬门 2 的白名单里**。⛔ **不过的两个**：⭐ WordNet 分类树是**结构**模型（⭐ 论文自己归为 `structural`），⭐ Clevr 程序图是**可执行**程序图（⭐ 论文自己归为 `executable`）—— ⛔ **两者都不是行为模型** |

#### ⭐⭐ 为什么它仍然成档（⛔ 必须给理由）

⭐ **三条理由，⛔ 都不依赖它是不是状态机工作**：

1. ⭐⭐ **它对本轨 B4 那一格给出的答案是「零」，⭐ 而零本身就是本轨最需要的一类数据点。** ⭐ 本轨的核心问题是「LLM 该被放在哪一环、循环的裁决者是谁」；⭐⭐ **AbsCon 的答案是「不要循环，把满足性交给求解器」** —— ⭐ 这是一个**明确的、带实测数字的、可比的架构立场**，⛔ 而不是一句意见。
2. ⭐ **它的行为模型案例（活动图）真实存在且是三个案例里排第一个的那个**，⛔ 不是附带提一句。⭐ PAGED 数据集 326 个评测样本全是流程图。
3. ⭐⭐ **它正面挑战我们的架构假设。** ⭐ 若「零迭代 + 求解器」能拿到 96.6%–100% 的一致性，⭐ 那么**任何带循环的方法都必须回答「迭代买到了什么」** —— ⭐ 而这正是 M1 要回答的问题。

### A.2 ⚠️ 边界拆分

| 案例 | 制品 | 边界 | 理由 |
| :-- | :-- | :-: | :-- |
| **① 流程图 / 活动图** | ⭐ 活动 + 决策 + 关系（决策出边带 condition） | ⭐ **邻域** | ⭐ 活动图在「邻域」档。⚠️⚠️ **但有一处落到界外**：⭐ artifact 的 prompt 逐字含 **fork/join** 例子（`"activity A and B happens at the same time after activity F"`），⭐ 论文正文也写 `"Parallel flows are represented by activities with multiple outgoing connections."` —— ⛔⛔ **这是并发语义，⛔ 在我们 $M$ 的边界外** |
| **② WordNet 分类树** | ⭐ 概念 + 父子关系 | ⛔ **不适用**（⭐ 结构模型，⛔ 非行为） | ⭐ 论文自归 `structural` |
| **③ Clevr 程序图** | ⭐ 操作序列 + 类型化输入输出 | ⛔ **不适用**（⭐ 可执行程序图，⛔ 非行为模型） | ⭐ 论文自归 `executable` |

⭐ **零时钟、零不变式** —— ⭐ 与我们边界的冲突只在 fork/join 一处，⛔ 且那是 prompt 里的一个示例而非方法主张。

---

## B. LLM 应用形态

### B1 · ⭐⭐ 流水线阶段（⛔ **约 9–10 个阶段，⭐ 其中 LLM 只有 1 个**）

```
[人/数据集] 规约 S = (元模型 M, 约束集 Φ, 描述 D)
  → [确定性] 1. prompt 组装（模板 + few-shot CoT 例子 + M + Φ + D）
  → ⭐⭐ [LLM ×n] 2. 并行采 n 个候选（n = 10，temp 0.7）  ← 全流水线唯一的 LLM 阶段
        ⛔ 候选之间互不可见、⛔ 无反馈、⛔ 无修订
        → n 份 Mermaid 文本
  ── 以下全是确定性 ──
  → [parser] 3. Mermaid 解析 + 语法错误过滤（⛔ 丢弃，不打回）
  → [神经编码器（非 LLM）] 4. 元素相似度：all-MiniLM-L6-v2 编码节点标签
        ⭐ 关系用「标签 + 源 + 靶」三者精确匹配（⛔ 不用嵌入）
  → [图算法] 5. 图匹配 = 图编辑距离（NP-hard，近优解，5 s 超时）
  → [计数] 6. 增量合并 → 概率偏序模型 𝔾 = (𝒩, ℰ, L, P)
  → [⛔ 人工，离线，每域一次] 7. 约束翻译：Φ + M → 一阶逻辑
  → [确定性] 8. 建模成 0/1 整数规划（二元交叉熵目标）
  → ⭐ [求解器] 9. CBC 求解  ← ⭐⭐ 这一步是一致性的唯一保证
  → 具体图 G*
  →（⭐ 仅 Clevr）[解释器] 10. 在 scene 上执行程序图 → 答案
```

⭐⭐ **阶段计数**：⭐ **9–10 个阶段；⭐ LLM 1 个；⭐ 人工离线 1 个（约束→FOL，每域一次，⛔ 不是每样本）；⭐ 其余 7–8 个全确定性。**

⭐⭐ **形状要点（⛔ 三条）**：

1. ⛔⛔ **LLM 在入口被并行调用 `n` 次就退场，⛔ 此后一次都不再被调用。** ⭐ 与 [`llm-guided-predicate-discovery`](./llm-guided-predicate-discovery.md)（RunVS）的形状**几乎相同**（⭐ 那篇也是 LLM 只在入口调一次，循环内零 LLM），⛔ 差别是 RunVS 有循环、AbsCon 连循环都没有。
2. ⭐⭐ **候选之间严格独立** —— ⭐ 逐字（§V-F Discussion）：`"each candidate is independent and can be generated in parallel"`。⛔ **所以这不是「多轮迭代」，是「一次性并行采样」。**
3. ⭐ **语法问题的处理是「丢弃」而不是「打回」** —— ⭐ 逐字（§III-B）：`"we use Mermaid as the output language and filter out any generated models with syntax errors. Alternatively, one may use constraint decoding [15] to ensure syntactical correctness."` ⭐ 论文还给了理由：`"In early experiments, we observe that LLMs rarely produce syntax errors when using the Mermaid diagramming language"`。

### B2 · 每次 LLM 调用的角色（⭐ **只有一种角色**）

| 调用 | 角色 |
| :-- | :-- |
| 候选生成 ×n | ⭐ **生成器** |

⛔⛔ **全篇没有**：⛔ **抽取器 · 分类器 · 翻译器**（⭐ NL→FOL 是**人工**做的）· ⛔ **评审者 · 修复者 · 规划者 · 裁决者 · 解释者 · 检索改写器 · LLM-as-judge**。

⭐ **机械核证（⭐ 本轮全文 grep 计数）**：`repair` **0** · `revision` **0** · `revise` **0** · `re-generat` **0** · `regenerat` **0** · `self-reflect` **0** · `critique` **0** · `LLM-as-a-judge` **0** · `human annotat` **0** · `annotator` **0** · `kappa` **0** · `inter-rater` **0** · `agreement` **0**；⭐ `feedback` **2**（⭐ 均在致谢与相关工作里）· `iterativ` **2** · `refine` **8**（⭐ 见 §B4）。

⭐ **论文自己的立场逐字（§V-F）**：`"Since it treats LLMs as a black box and requires no additional training or modification to their structure, AbsCon can be easily applied to various model generation tasks."`

### B3 · prompt 策略

| 项 | 值 |
| :-- | :-- |
| **few-shot + CoT** | ⭐ 逐字（§V-B）：`"For model generation, we adopt few-shot CoT [18]. We include few-shot examples with manually crafted chain-of-thought reasoning steps embedded in each prompt."` ⭐ **推理步骤是人手写的** |
| ⭐ **self-consistency 式采样** | ⭐ 逐字：`"we adapt the original self-consistency setup, which produces multiple outputs from the same input prompt using a non-zero temperature"`。⭐ 候选 temp **0.7**；⭐ `Direct` 基线 temp **0.01**（⭐ 理由逐字：`"since determinism cannot be guaranteed for OpenAI models"`） |
| ⭐ **元模型 + 约束写进 prompt** | ⭐ 逐字（§III-A）：`"the input prompt includes the metamodel of the flowchart, its constraints, and the problem description"` |
| ⭐ **角色扮演** | ⭐ **有** —— ⭐ artifact 逐字（`activity/prompts.py`，⭐ 本轮实取）：`"You are an expert software modeler who can create an UML activity diagram from a text description."` |
| ⭐ **CoT 指令内联** | ⭐ artifact 逐字：`"First identifying all activities and decisions, then describe how they can be connected, finally output the activity diagram as a mermaid graph"` |
| 输出格式约束 | ⚠️ **弱** —— ⭐ 靠 Mermaid 围栏块 + **事后过滤**，⛔ **不是**受限解码、⛔ 不是 JSON schema、⛔ 无解析失败回灌 |
| few-shot 样例隔离 | ⭐ **有** —— ⭐ PAGED 5 个 / WordNet 3 个 / Clevr 4 个作为样例，⭐ 且**从评测集里排除** |
| ⛔ 无 | RAG · 工具调用 · 多智能体辩论 · LLM 投票（⚠️ **注意**：⭐ `MV` 基线是**元素级多数投票**，⛔ 但那是**确定性统计**，⛔ 不是 LLM 在投票） |
| prompt 是否公开 | ⭐⭐ **完全公开** —— ⭐ 见 D 节，⭐ 三个域各一个 `prompts.py`，⭐ 本轮实取读过 `activity/prompts.py` 全文 |

#### ⛔⛔ 一处论文与 artifact 的约束集不一致（⭐ 我方核出）

⭐ **论文说流程图有 5 条约束（§III-A 逐字）**：

> `"a valid instance flowchart must: (1) have a single starting node; (2) allow reaching every other node from the starting node; (3) require decision nodes to have at least two targets; (4) ensure that each outgoing relation from a decision node has a non-empty condition; and (5) contain no self-cycles."`

⭐ **但 artifact 的 prompt 里列的 5 条是（⭐ 本轮逐字实取）**：

> `"1. All outgoing edges of a decision node must have a condition / 2. There can only be one initial node / 3. The activity diagram should be connected / 4. The initial node should be able to reach all nodes in the activity diagram / 5. Use numbers (1..N) to represent node IDs as shown in the example"`

⭐ **逐条对照**：

| 论文的 Φ | prompt 里有吗 |
| :-- | :-- |
| (1) 单一起始节点 | ⭐ **有**（prompt #2） |
| (2) 起始节点可达全部节点 | ⭐ **有**（prompt #4） |
| ⛔ **(3) 决策节点至少两个出靶** | ⛔⛔ **没有** |
| (4) 决策节点出边条件非空 | ⭐ **有**（prompt #1） |
| ⛔ **(5) 无自环** | ⛔⛔ **没有** |
| — | ⚠️ prompt #3「图应连通」在论文的 5 条里**没有对应项** |
| — | ⛔ prompt #5「用数字当节点 ID」是**格式要求，⛔ 不是良构约束** |

⚠️ ⭐ **怎么读这个不一致**：⭐ **它不一定是错** —— ⭐ 因为 AbsCon 的一致性由 **ILP 保证**，⛔ 不由 prompt 保证，⭐ 所以 prompt 里少写两条不影响最终 `Con`。⛔ **但论文说 `"The input prompt provided to the LLM comprises a specification, including a metamodel, well-formedness constraints, and description of the model"`，⭐ 字面上暗示 Φ 全在 prompt 里** —— ⛔ **实际不是。** ⭐ 这一条对复现者重要：⛔ **照论文的 5 条写 prompt，与照 artifact 写，不是同一件事。**

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| **有无循环** | ⛔⛔ **无。⭐ 一轮迭代都没有。** |
| ⭐ **裁决者是谁** | ⭐⭐ **`sound oracle`（约束优化求解器 **CBC**）** —— ⛔ **但它不在「循环里」，⭐ 它是流水线末端一次性施加的门。⭐⭐ 更准确的说法是：⛔ 它不是「裁决要不要再来一轮」，⭐ 而是「一次性把满足约束的解构造出来」** |
| 终止条件 | ⛔ **不适用**（无轮次） |
| 最大轮数 | ⛔ **不适用** |
| ⭐ 有无报告循环的边际收益 | ⛔ **无逐轮收益（无轮次）**；⭐⭐ **但有「第 k 个候选的边际收益」，⭐ 且方向与我们一致** —— 见下 |

#### ⭐⭐ 它的立场：⛔ **明确反对迭代式精化**

⭐ 逐字（§I Introduction）：

> `"However, current approaches rely exclusively on the LLM to generate or iteratively refine outputs, limiting their effectiveness."`

⭐⭐ **这句话把「iteratively refine」列为**被批评的对象**，⛔ 不是被采纳的手段。** ⭐ AbsCon 的替代方案是**测试时并行计算**（`n` 个独立候选）+ **构造性满足**（求解器）。

#### ⭐⭐ 「构造性满足」是本卡最该带走的机制

⭐ 目标函数逐字（§III-E）：

$$
\max_{\mathcal{X}} \sum_{a \in \mathcal{N} \cup \mathcal{E}} x_a \log P(a) + (1 - x_a)\log(1 - P(a)), \quad s.t.\ \mathcal{X} \models \mathcal{C}
$$

⭐ 逐字：`"The solution to this problem represents the optimal concretization of the partial model while satisfying all constraints."`

⭐⭐ **关键在于 `s.t.` 那一半**：⛔ **约束不是「检查完了打回去重做」，⭐ 而是「作为硬约束写进求解器，使不满足的解在搜索空间里根本不存在」。** ⭐⭐ **这就是为什么它不需要循环。**

⭐ **失败模式论文也写了**（⭐ 逐字）：

> `"Failure to obtain a feasible solution implies that no combination of candidates can produce a consistent graph, which may indicate that the LLM is not capable of this task or that more candidates are needed."`

⚠️ ⭐ **注意这句话的诚实之处**：⭐ 它承认**存在无解的情况**，⭐ 并给出了两种归因。⛔ 但论文**没有报「无解发生了多少次」** —— ⭐ 见 F.4。

#### ⭐⭐ 「第 k 个候选的边际收益」—— ⭐ 与我们「第 3–5 轮零收益」的同构对照

⭐ 这是 RQ3 的内容。⭐ **逐字抄下来**：

> `"This improvement plateaus as the number of candidates increases, stabilizing at around 5 candidates for Llama3.1-8B and between 5 and 8 candidates for Llama3.1-70B. This result suggests that only a small number of candidates is needed to achieve significant improvements over the Direct approach."`

> `"For Llama3.1-8B on WordNet and Clevr, performance slightly declines as the number of candidates increases. We suspect this is due to smaller LLMs tending to repeat common mistakes, making these errors more dominant among the candidates."`

> `"Model quality improves as the number of candidates increases. The gains plateau quickly at around 5 to 8 candidates, suggesting that AbsCon requires only a few candidates to be effective. However, there is still room for improvement compared to the best possible model."`

⭐⭐⭐ **对照我们的实测（⛔ 这一段是本卡对 M1 最直接的价值）**：

| | ⭐ AbsCon | ⭐ 我们 v46 | ⭐ RunVS（[另一张卡](./llm-guided-predicate-discovery.md)） |
| :-- | :-- | :-- | :-- |
| 「多来一次」是什么 | ⭐ **多采一个独立候选** | ⛔ **多跑一轮 LLM 自评修订** | ⭐ 多跑一轮确定性反例检查 |
| 收益什么时候见底 | ⭐⭐ **第 5–8 个候选** | ⛔⛔ **第 3 轮** | ⭐ 500 轮里只有 1–9 次真修订 |
| 见底之后继续跑的成本 | ⭐ **LLM token（贵），⛔ 但可并行** | ⛔⛔ **LLM token（贵），⛔ 且串行** | ⭐ **0.004–0.672 s 确定性计算（几乎免费）** |
| ⛔ 见底之后会不会变差 | ⚠️ **会** —— ⭐ 小模型上「performance slightly declines」 | ⛔ **净变化 ≈ 0** | ⭐ 不会 |

⭐⭐ **三条连起来的结论**：⭐⭐ **「收益在很早的轮次/样本数就见底」是一个跨方法、跨制品、跨裁决者类型都成立的现象。** ⭐ 差别只在**见底之后继续跑要付多少钱**，⭐ 以及**多来一次的形式是「独立采样」还是「串行修订」**。⭐⭐ **而 AbsCon 提供了一个我们没有的选项：⭐ 把「多来一次」做成可并行的独立采样，⛔ 而不是串行的修订链** —— ⭐ 前者的墙钟成本可以被并行度摊掉，⛔ 后者不能。

#### ⚠️ 一个小例外：artifact 里有一处盲重试

⭐ **论文正文没有任何重试**，⛔ 但 artifact 的 `run_generation.py` 里有一个 `while result is None:` 包住 Mermaid 块抽取 —— ⭐ **即「采到能解析的为止」的盲重采**，⛔ **不带任何反馈进下一次**。⭐ 这是全套代码里唯一的重复结构，⛔ **它是解析重试，不是被裁决的循环。**

### B5 · ⭐⭐ 中间表示（⛔ 本卡第二重要的一格）

| 子字段 | 值 |
| :-- | :-- |
| **有无** | ⭐⭐ **有，⭐ 而且它就是论文的中心构造** |
| **形态** | ⭐⭐ **概率偏序模型（probabilistic partial model）** —— ⭐ 逐字（§III-D）：`"a probabilistic partial model is defined as a tuple 𝔾 = (𝒩, ℰ, L, P), where L: 𝒩 ∪ ℰ → T is the probabilistic label mapping that assigns to each node and edge a probability distribution over labels 𝒯 … P: 𝒩 ∪ ℰ → [0,1] is a mapping that assigns the likelihood of existence for each element."` |
| | ⭐ 它是**经典三值偏序模型（1 / 0 / ½）的概率化推广** —— ⭐ 逐字：`"Traditional partial models represent uncertainty using three-valued logic … However, this formulation does not capture the likelihood of each element, which is a crucial aspect for determining the frequency of model elements."` |
| ⭐ **是否闭合** | ⚠️⚠️ **两层，⭐ 两层都闭合，⛔ 但闭合的意思不同** —— 见下 |
| ⭐ **谁定的 / 谁选类** | ⛔⛔ **没有任何「选类」动作** —— 见下 |

#### ⚠️ 「是否闭合」的两层拆解

| 层 | 闭合性 | 说明 |
| :-- | :-: | :-- |
| ⭐⭐ **元素空间** | ⭐⭐ **闭合于候选并集** | ⭐ ILP 的决策变量恰是偏序模型里已有的元素（`x_n`、`x_e`），`x = 1` 表示入选最终模型。⛔⛔ **concretization 只能选子集 —— ⭐ 永远不能新造一个节点/边，⭐ 也永远不能补一个所有候选都漏掉的元素。** ⭐⭐ **这就是 §0 限制 2** |
| ⭐ **约束 / 元模型目录** | ⭐⭐ **闭合、预编、人工撰写** | ⭐ 逐域固定：⭐ **流程图 5 条**、⭐ **分类树 3 条**、⭐ **Clevr 程序 8 条**（⭐ 三个数字本轮均从原文逐字核过）。⭐ 翻译成 FOL 也是人工：⭐ 逐字 `"In this paper, we manually translate the metamodel and well-formedness constraints into first-order logic (FOL) formulae"`。⭐ 论文说实践中可自动化：`"Typically, such FOL formulae can be automatically derived from high-level graph constraint languages like Object Constraint Language"` |

#### ⛔⛔ 「谁选类」：**没人选，全部无条件同时施加**

⭐ **这一格是与我们最关键的错位。** ⛔ **没有分类器、⛔ 没有缺陷类型学、⛔ 没有谓词族选择、⛔ 没有规则匹配、⛔ 没有 LLM 自动选类。** ⭐ 全部约束作为**硬约束同时**写进一个 ILP。⭐ 决策只有两处，⭐ 且都是确定性的：

| 决策 | 判据 |
| :-- | :-- |
| ⭐ 合并节点后用哪个标签 | ⭐ **频次** —— 逐字：`"Update the representative label of m to the most frequent label in the list."` |
| ⭐ 哪些元素入选最终模型 | ⭐ **ILP 目标函数的 argmax**（⭐ 二元交叉熵 s.t. 约束） |

⭐ 另有一条论文明写的链接约束：`"for each relation e = (s,t) ∈ ℰ, we require that if either the source node s or the target node t is not selected, then e must be excluded."`

⭐⭐ **与我们的对照（⛔ 必须说清，⛔ 否则会被误读成先例）**：

- ⭐ 我们是「**闭合 19 条谓词词表 + LLM 每条需求自动选**」。
- ⛔ 它是「**闭合约束集 + 全部无条件穷举施加**」。
- ⛔⛔ **所以它不是「闭合词表 + LLM 自动选」的先例。** ⭐ **本轨这个组合的先例计数在本篇这里 +0。**
- ⭐⭐ **但它给了我们一个值得认真考虑的替代设计**：⛔ **如果所有检查都能被无条件施加（因为它们是确定性的、成本低的），那「让 LLM 选类」这个环节本身就是可以删掉的。** ⚠️ ⭐ 我们之所以需要选类，⭐ 是因为我们的谓词求值成本不为零、且要绑到具体需求上；⛔ **但 v46 实测只用到 15/19 —— ⭐ 值得问一句：如果把 19 条全部无条件跑一遍，会不会比让 LLM 选更好？** ⭐ 这是 I 级建议，⛔ 不是本篇的结论。

#### ⭐ 一处反泄漏纪律，⭐ 值得抄

⭐ 逐字（§V-B Metrics）：

> `"We do not use embedding similarity since it is used during the abstraction step to avoid potential bias."`

⭐⭐ **即：因为方法内部用嵌入相似度做元素匹配，⛔ 所以评测时刻意不用嵌入相似度当指标，⭐ 以免自证。** ⭐ **这正是仓库 §3.5 第 5 条「自证式验证」的正面处理范例** —— ⭐ 值得直接抄进我们的评测口径说明。

### B6 · 模型

⭐⭐ **四个模型，⭐ 全部在全部数据集 × 全部基线上做了对照** —— ⭐ 逐字：`"Two of these models, GPT-4o-mini [46] and GPT-4o [47], are the latest in OpenAI's GPT family… we also evaluate our approach using two variants of the open-source LLM Llama3.1 (8B and 70B) [2]."`

| 模型 | 精确度 |
| :-- | :-- |
| **GPT-4o-mini** | ⛔ **仅别名，⛔ 无 snapshot 日期** |
| **GPT-4o** | ⛔ **仅别名，⛔ 无 snapshot 日期** |
| **Llama 3.1-8B Instruct** | ⭐ repo 目录名 `Meta-Llama-3.1-8B-Instruct`（⭐ 本轮实取确认） |
| **Llama 3.1-70B Instruct** | ⭐ repo 目录名 `Meta-Llama-3.1-70B-Instruct` |

⭐ **非 LLM 神经组件**：⭐ **all-MiniLM-L6-v2**（Sentence Transformers）编码节点标签；⭐ GPT-4o tokenizer 仅用于算 token overlap 指标。

⚠️ **代差与 pin 缺口**：⛔ **两个 GPT 都没有 dated snapshot ID**（⛔ 如 `gpt-4o-2024-08-06`），⛔ 论文与代码里都没有。⭐ Llama 通过自建 endpoint 服务（`HOSTED_LLM_URL`）—— ⛔ **私有端点，⛔ 外人无法复现那两列。**

⭐⭐ **一条对我们有用的跨能力观察**：⭐ 逐字（§V-C）：`"In 3 out of 6 cases, smaller LLMs combined with AbsCon outperform their larger counterparts using Direct."` ⭐⭐ **即「弱模型 + 好架构」有一半机会打赢「强模型 + 朴素做法」。** ⚠️ ⭐ **注意方向**：⭐ 这与 [`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md)「分阶段帮弱模型、伤强模型」**不矛盾** —— ⭐ 那篇讲的是架构收益随模型变强而衰减，⭐ 这篇讲的是架构收益在弱模型上足以跨越一个模型档位。⭐ **两者都指向「架构收益与模型能力负相关」。**

### B7 · ⭐⭐ 确定性成分（⭐ 本轨最厚的一格）

| 环节 | 是什么 | ⭐ 逐字/证据 |
| :-- | :-- | :-- |
| **Mermaid parser + 语法过滤** | ⭐ 解析并**丢弃**语法错的候选 | ⭐ `"filter out any generated models with syntax errors"`；⭐ repo `activity/parser.py`(2,728B) · `taxonomy/output_parsers.py`(966B) · `programs/parser.py`(1,784B) |
| **元素相似度** | ⭐ 节点用 all-MiniLM-L6-v2 嵌入；⭐ **关系用精确匹配** | ⭐ `"since relations may have empty labels, we use an exact match approach for assessing relation similarity: two relations are considered a match if their labels and both their source and target nodes match exactly"` |
| **图匹配** | ⭐ **图编辑距离**，⭐ NP-hard，⭐ 近优解，⭐ 5 s 超时 | ⭐ `"Although the problem is NP-hard for arbitrary graphs, in practice, near-optimal matches are typically identified in a short amount of time."` |
| **增量合并** | ⭐ 纯计数 → 存在概率 = 元素计数 / 候选数；⭐ 标签概率 = 该标签出现次数 / 元素计数 | ⭐ 合并规则逐字见 §B5 |
| ⛔ **约束 → FOL** | ⛔ **人工，离线，每域一次** | ⭐ `"we manually translate the metamodel and well-formedness constraints into first-order logic (FOL) formulae"` |
| ⭐⭐ **CBC 求解器** | ⭐⭐ **0/1 整数规划求解 —— ⭐ 一致性的唯一保证** | ⭐ `"During concretization, the constraint optimization problem is solved using the CBC solver [31]."` ⭐ 约束类型选择逐字：`"we focus on linear constraints since they cover a wide range of practical scenarios and are efficient to solve. Nonetheless, our framework can be adapted with any type of constraints and corresponding solvers."` |
| ⭐ **Clevr 程序解释器** | ⭐ 在 scene 上执行程序图求答案 | ⭐ repo `programs/program_executor.py`(17,817B) |

⛔ **没有**：⛔ **模型检查器 · SMT solver · 类型检查器 · EMF/Ecore 一致性检查器**。⭐ 元模型一致性靠两件事保证：⭐ ① 语法层由 Mermaid 过滤，⭐ ② 语义层由人手写的 FOL 塞进 ILP。

⭐⭐ **这一格与我们的关系（⛔ 最该带走的一条）**：⭐⭐ **我们有 pyfcstm（真 sound oracle），⛔ 放在求值端；⭐ 它有 CBC（真求解器），⭐ 放在「构造端」。** ⭐⭐ **「构造端」是第三个位置，⛔ 比「裁决端」更强**：⛔ 裁决端是「检查完了打回」，⭐ 构造端是「让不合规的解不存在」。⭐ **M1 第二条设计原则若只写到「把裁决者换成 sound oracle」，⛔ 就漏掉了这个更强的选项。**

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐⭐ **4 个 + 2 个 oracle 上界** —— 见 §C.2 |
| `dataset` | ⭐ **3 个**：PAGED（流程图，**326** 评测）· WordNet（分类树，**100**）· Clevr（程序图，**300**）—— 见 §C.3 |
| `metrics` | ⭐ soft P / soft R / soft F1（soft cardinality）· `Con`（%）· `SR`（%）· `ACC`（%）。⛔⛔ **无任何 `@k` 口径** —— 见 §C.4 |
| ⭐ `judged_by` | ⭐⭐ **全自动脚本对着数据集 ground truth；⭐ Clevr 用执行结果** —— ⛔⛔ **零人类标注、⛔ 零 LLM-as-judge、⛔ 因此也零标注者间一致性** |
| `human_baseline` | ⛔⛔ **无** |
| `runs` | ⚠️ **RQ1 每格 1 次（n=10 候选）、⛔ 无标准差/置信区间/误差棒**；⭐ **但有统计检验**（Wilcoxon + Cliff's Delta）—— 见 §C.6 |
| ⭐ `adverse_results` | ⭐⭐ **报得相当坦白（6 类）**，⛔ 但有 1 处表里有、正文不提 —— 见 §C.7 |

### C.1 ⭐ 三个 RQ（逐字）

```text
1. How do the consistency and quality of AbsCon's outputs compare to those of alternative approaches?
2. How does the consistency of LLM-generated models impact model quality?
3. How does the number of candidates affect AbsCon's performance?
```

### C.2 ⭐⭐ 必答 ① 之一 · `accurate` 与 `consistent` 的操作化定义

#### ⭐ 它们是**两条明确分开的轴**，⭐ 而且论文的整个立论就建立在「前人把其中一条漏掉了」上

⭐ 三个问题逐字（Abstract）：

> `"(1) syntax violations: the generated model may not adhere to the syntax defined by its metamodel, (2) constraint inconsistencies: the structure of the model might not conform to some domain-specific constraints, and (3) inaccuracy: due to the inherent uncertainty in LLMs, the models can include inaccurate, hallucinated elements."`

⭐ 并明写前人只解决了第一个：`"While the first issue is often addressed through techniques such as constraint decoding or filtering, the latter two remain largely unaddressed."`

#### ⭐ 两轴的操作化（**M**，§V-B Metrics 逐字）

> `"The generated graph models are evaluated based on two criteria: (1) consistency, which measures the percentage of models that are fully compliant with all constraints, and (2) quality, which assesses how accurately the generated graphs match the given description. Since automated comparison of a graph model with the natural language description may be unreliable, we evaluate model quality using either downstream task performance or ground truth comparison, depending on the use case."`

| 轴 | 操作化 | ⛔ 注意 |
| :-- | :-- | :-- |
| ⭐⭐ **`consistent`** | ⭐ **整模型二值谓词，⭐ 全有或全无** —— ⭐ `Con` = 满足**全部**约束的模型百分比；⭐ Clevr 上改用 `SR`（success rate）= `"the percentage of graphs that can be successfully executed without error"` | ⛔⛔ **只管结构良构性。⛔ 一个结构完美但内容全错的图，`Con` 也是 100%** |
| ⭐ **`accurate`**（⚠️ **论文多数时候叫 `quality`**） | ⭐ **对着 ground-truth 参考模型比**，⛔ **不是对着 NL 比**。⭐ 关系集比对，每条关系 = (源标签, 靶标签, 关系标签)；⭐ 用 **soft precision / soft recall / soft F1**（soft cardinality）。⭐ 分域：⭐ 分类树用**精确匹配**（标签固定）；⭐ 流程图用 **token overlap**（token 集合 Jaccard）；⭐ Clevr 用**执行准确率 ACC** | ⚠️⚠️ **`accurate` 与 `quality` 在原文里近乎互换使用** —— ⛔ 引用时应统一说「quality（论文亦称 accuracy）」，⛔ 不要把它们当两个量 |

⭐ **形式化目标逐字**：`G^gt ⊧ (M, Φ) ∧ G* ∼ D` —— ⭐ 即 ground truth 既满足元模型+约束、又符合描述；⭐⭐ **两条轴正对应这两个合取项。**

⚠️⚠️ ⭐ **对我们最重要的一句限定**：⭐ 论文**自己承认**「自动把图与 NL 描述比对不可靠」，⭐ 所以它**绕开了**这件事，⛔ 改用参考图。⭐⭐ **而我们的 discover 任务做的正是它绕开的那件事** —— ⛔ **所以它的 quality 指标与我们的 `hit@k` 不可并列。**

### C.3 ⭐ 基线与数据集

#### ⭐ 4 个基线 + 2 个 oracle 上界

| # | 基线 | 说明 |
| :-: | :-- | :-- |
| 1 | **Direct** | ⭐ 单次 CoT 生成，temp 0.01，`"approximates greedy decoding"` |
| 2 | ⭐⭐ **MV** | ⭐ self-consistency 元素级多数投票 —— ⭐ `"performing majority voting on the relations (including the source and target nodes)"`，`"similar to atomic self-consistency [30]"`。⭐⭐ **这是最重要的对照臂**（见 §C.5） |
| 3 | **ESC** | ⭐ 执行式 self-consistency（**仅 Clevr**） |
| 4 | **ESC-F** | ⭐ ESC + 过滤，⭐ 论文自称 `"a stronger baseline"`：`"graphs that result in execution errors are excluded from the majority voting. If all candidates are inconsistent, the method will output an error."` |
| ⭐ oracle | **median candidate** / **best candidate** | ⭐ 仅 RQ3 用作上界。⭐ 论文明写不可实用：`"Note that these best candidates are difficult to identify in practice due to lack of oracle evaluator."` |

⛔ **无外部方法作为基线**（⭐ 全部是自建的 self-consistency 变体）。

#### ⭐ 数据集与分母

| 数据集 | 来源 | ⭐ 分母 | few-shot 隔离 |
| :-- | :-- | :-- | :-- |
| ⭐ **PAGED**（流程图，行为） | PAGED benchmark, ACL 2024（ref [44]） | ⭐ 逐字：`"A portion of the dataset consists of trivial graphs without branches or forks, which are removed during evaluation. After filtering, we obtain 331 non-trivial description-graph pairs."` → ⭐ 减 5 个样例 → ⭐ **326 评测** | ⭐ 5 个 |
| ⭐ **WordNet**（分类树，结构） | WordNet（ref [45]）—— ⭐ `"761 taxonomies, each containing between 11 and 50 terms"` | ⭐ 逐字：`"We randomly sample 100 taxonomies for evaluation and select three as few-shot examples."` | ⭐ 3 个 |
| ⭐ **Clevr**（程序图，可执行） | Clevr（ref [43]） | ⭐ 逐字：`"We randomly select 100 questions for each category, resulting in 300 questions for evaluation, and designate four as few-shot examples."`（⭐ 三类：count / judge / query） | ⭐ 4 个 |

⭐⭐ **分母口径值得肯定的两点**：⭐ ① **trivial 样本的剔除被明写出来并给了理由**（⛔ 不是悄悄剔）；⭐ ② **few-shot 样例从评测集里排除**。⛔ **但没有独立的 dev/hold-out split**，⛔ 也没有描述任何超参调优集。

### C.4 ⛔ `metrics`：⛔ 无 `@k` 口径

⛔⛔ **全篇无 `hit@k` / `pass@k` / `best@k` 之类的多轮口径。** ⭐ 唯一的多样本构造是两处，⛔ 但都不是 `@k`：

1. ⭐ **`n` 个候选被聚合成一个输出**（⭐ RQ1 用 n = 10；⭐ RQ3 从 1 扫到 20）—— ⛔ **这是「多样本合成一个答案」，⛔ 不是「多次尝试取最好」。**
2. ⭐ **RQ3 的 median-candidate / best-candidate 上界曲线** —— ⚠️ ⭐ **功能上像 `best@k`，⛔ 但论文从未这样命名或定义。**

⭐⭐ **所以 §0 限制之外还有一条**：⛔ **它的 `Con` 是整模型二值率，⛔ 不是逐缺陷命中率** —— ⛔ **本篇的任何数字都不能与我们的逐条 `hit@1/@3/@all` 直接比。**

### C.5 ⭐⭐ 主要结果（**M**，⭐ Table I 逐字抄，单位 %）

#### PAGED（流程图 · 行为模型 · n=326）

| Method | GPT-4o-mini P/R/F1/**Con** | GPT-4o P/R/F1/**Con** | Llama3.1-8b P/R/F1/**Con** | Llama3.1-70b P/R/F1/**Con** |
| :-- | :-- | :-- | :-- | :-- |
| Direct | 77.88 / 74.17 / 75.19 / **95.40** | 81.01 / 78.68 / 79.13 / **96.63** | 76.87 / 78.42 / 76.98 / **94.48** | 79.28 / 81.15 / 79.54 / **93.25** |
| ⛔ **MV** | 80.10 / 70.32 / 73.93 / ⛔ **66.26** | 82.90 / 75.62 / 78.17 / ⛔ **71.47** | 79.87 / 70.02 / 73.43 / ⛔⛔ **51.23** | 80.01 / 78.67 / 78.66 / ⛔ **69.33** |
| ⭐ **AbsCon** | 77.81 / 76.88 / 76.59 / ⭐ **99.08** | 80.87 / 79.93 / 79.73 / ⭐ **99.08** | 77.47 / 79.31 / 77.79 / ⭐ **98.47** | 79.13 / 81.69 / 79.85 / ⭐ **96.63** |

#### WordNet（分类树 · 结构 · n=100）

| Method | GPT-4o-mini | GPT-4o | Llama3.1-8b | Llama3.1-70b |
| :-- | :-- | :-- | :-- | :-- |
| Direct | 72.53 / 52.80 / 59.20 / **78.00** | 75.84 / 66.58 / 69.69 / **83.00** | 67.24 / 55.55 / 59.84 / **65.00** | 78.56 / 66.97 / 71.14 / **95.00** |
| MV | 83.06 / 43.42 / 54.28 / ⛔ **64.00** | 84.13 / 54.48 / 63.97 / ⛔ **75.00** | 82.23 / 33.16 / 44.55 / ⛔ **65.00** | 86.24 / 52.65 / 63.13 / ⛔ **80.00** |
| ⭐ **AbsCon** | 82.91 / 69.22 / 73.83 / ⭐ **100** | 80.01 / 73.52 / 75.93 / ⭐ **99.00** | 74.99 / 64.75 / 68.81 / ⭐ **100** | 80.24 / 73.42 / 75.94 / ⭐ **100** |

#### Clevr（程序图 · 可执行 · n=300，⭐ 报 ACC / SR）

| Method | GPT-4o-mini | GPT-4o | Llama3.1-8b | Llama3.1-70b |
| :-- | :-- | :-- | :-- | :-- |
| Direct | 39.00 / 45.67 | 65.33 / 71.33 | 38.00 / 48.33 | 65.00 / 72.00 |
| ⛔ MV | ⛔ **21.00** / 65.67 | ⛔ 51.67 / 77.33 | ⛔⛔ **19.00** / 86.33 | ⛔ 57.67 / 90.33 |
| ESC | 33.67 / 39.00 | 66.00 / 71.00 | 28.67 / 31.67 | 70.00 / 76.00 |
| ESC-F | 65.33 / 80.33 | 80.33 / 86.67 | 73.00 / 94.67 | 88.33 / 96.00 |
| ⭐ **AbsCon** | ⭐ **69.67 / 98.33** | ⭐ **81.33 / 100** | ⭐ **74.67 / 100** | ⭐ **89.67 / 100** |

⭐ 汇总数字逐字：`"The F1-score improves by an average of 0.78% for the PAGED dataset and 8.61% for WordNet… answer accuracy increases by approximately 27% on average with AbsCon."`；⭐ `"AbsCon produces consistent models for all samples in 6 out of 12 cases. In the remaining cases, AbsCon remains consistently above 96.6%."`

#### ⭐⭐⭐ 本表里对我们最有价值的一行：⛔ **朴素 self-consistency 投票（MV）把一致性打崩了**

| 数据集 | Direct 的 `Con` | ⛔ MV 的 `Con` | 落差 |
| :-- | --: | --: | --: |
| PAGED / GPT-4o-mini | 95.40 | ⛔ **66.26** | ⛔ **−29.1** |
| PAGED / GPT-4o | 96.63 | ⛔ **71.47** | ⛔ **−25.2** |
| PAGED / Llama-8b | 94.48 | ⛔⛔ **51.23** | ⛔⛔ **−43.3** |
| PAGED / Llama-70b | 93.25 | ⛔ **69.33** | ⛔ **−23.9** |
| Clevr / GPT-4o-mini（ACC） | 39.00 | ⛔ **21.00** | ⛔ **−18.0** |
| Clevr / Llama-8b（ACC） | 38.00 | ⛔⛔ **19.00** | ⛔⛔ **−19.0** |

⭐⭐ **读法**：⛔⛔ **在模型元素上做多数投票，会把一个原本良构的图拆成一个不良构的图** —— ⭐ 因为投票是**逐元素独立**的，⛔ 而良构性是**整图性质**。⭐ 论文自己的解释（§V-F）：`"While MV achieves slightly higher precision, AbsCon consistently yields much better recall and F1-"`。

⭐⭐⭐ **这条对 M1 是一个直接的、可操作的警示**：⭐ 若我们考虑给流水线加 self-consistency 投票（⭐ 我们 v46 明确**没有**这个），⛔ **本篇给出实测证据：逐元素投票会破坏整体性质，⛔ 除非有一个东西负责把整体性质重新缝回来（他们那个东西是 ILP）。**

### C.6 ⭐ `runs` 与统计检验

| 项 | 状况 |
| :-- | :-- |
| RQ1 | ⭐⭐ **每（模型 × 数据集 × 方法）格 1 次，⭐ n=10 候选；⛔ 无标准差、⛔ 无置信区间、⛔ 无误差棒** —— ⭐⭐ **本轮已从 artifact 侧证实**（⭐ `results_N.csv` 的 `N` 是候选编号而非重复次数，⭐ 见 §D.2 与 F.3），⛔ 故这不再是推断 |
| RQ2 | ⭐ 逐字：`"The average model quality score in each group is computed over 10 runs."` ⚠️ **「10 runs」指的是 10 个候选**，⛔ 不是 10 次独立完整实验 |
| ⭐⭐ **统计检验** | ⭐⭐ **有，⭐ 而且做得对** —— ⭐ 逐字：`"Since the performance distribution of LLM-generated models is unknown, we use the non-parametric Wilcoxon rank-sum test to assess statistical significance. Additionally, we use Cliff's Delta, a non-parametric effect size measure, to quantify the impact of consistency on model quality."` |
| ⭐ 检验结果 | ⭐ 逐字：`"The results reject the null hypothesis in all cases except for GPT-4o on the PAGED dataset, with p ≤ 0.02. For WordNet, the null hypothesis is rejected across all cases, with p ≤ 0.001… all effect sizes exceed 0.6."` |

⭐⭐ **值得抄的一点**：⭐ **非参数检验 + 效应量，⭐ 且给了选择理由（分布未知）。** ⭐ 本轨里做统计检验的很少 —— ⭐ [`iet-software-2025-consistency-traceability`](./iet-software-2025-consistency-traceability.md) 一个检验都没做，⭐ [`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md) 也没有。⭐ **我们报 −15.82pp 时应当配一个检验 + 效应量**，⛔ 而不是只报点估计。

### C.7 ⭐ `adverse_results`

#### ⭐ 坦白报出的（⭐ 6 类）

| # | 不利结果 | 逐字 |
| :-: | :-- | :-- |
| 1 | ⭐ **precision 低于 MV 基线** | `"Compared to the baselines, for non-executable models, recall improves by 0.55%−2.69% on the PAGED dataset and 6.45%−16.42% on WordNet. Compared to the MV baseline, AbsCon generally achieves slightly lower precision. However, the higher precision of MV comes at the cost of a significant reduction in recall"` |
| 2 | ⭐⭐ **RQ2 的结论有一个反例，⭐ 且明写** | `"Consistent models also demonstrate better F1-score in the PAGED and WordNet datasets, except for GPT-4o on the PAGED dataset, where this trend does not hold."` ⭐ **且对应的统计检验也恰好只在那一格不显著** —— ⭐ 两处口径一致，⛔ 没有藏 |
| 3 | ⚠️ **加候选会变差的情况** | `"For Llama3.1-8B on WordNet and Clevr, performance slightly declines as the number of candidates increases. We suspect this is due to smaller LLMs tending to repeat common mistakes, making these errors more dominant among the candidates."` |
| 4 | ⭐ **与 best candidate 仍有差距** | `"However, there is still room for improvement compared to the best possible model."` |
| 5 | ⭐ **残留不一致给了假说而非掩盖** | `"We suspect that the small fraction of inconsistent models may result from the inherent limitations of LLMs in generating consistent models for certain descriptions."` |
| 6 | ⭐⭐ **外部效度的诚实承认（⭐ 对我们直接相关）** | `"due to the limited availability of datasets for behavioral and executable models, we adapt similar datasets from other domains, transforming them into behavioral and executable models."` |
| 7 | ⭐ **成本未测，⭐ 明写留给未来** | `"Most test samples are processed within seconds. We leave the detailed study on the runtime cost of AbsCon to the future."` |

⭐⭐ **第 6 条对我们特别有用**：⭐ **它承认「行为模型的数据集本来就少，所以我们是把别的领域的数据集改造成行为模型的」** —— ⭐ 这与我们 L1 实测「外部可比数字 0 条」是同一个困境的另一面表述。⭐ **可作为我们「为什么没有外部 baseline」的一条领域佐证。**

#### ⛔ 表里有、正文不提的（⭐ 我方核出）

⛔ **AbsCon 的 precision 在 PAGED 上不仅低于 MV，⛔ 也低于 Direct** —— ⭐ 4 格里 3 格如此（⭐ 本轮从 Table I 逐格核算）：

| PAGED | Direct P | AbsCon P | 差 |
| :-- | --: | --: | --: |
| GPT-4o-mini | 77.88 | ⛔ **77.81** | ⛔ −0.07 |
| GPT-4o | 81.01 | ⛔ **80.87** | ⛔ −0.14 |
| Llama-8b | 76.87 | ⭐ 77.47 | ⭐ +0.60 |
| Llama-70b | 79.28 | ⛔ **79.13** | ⛔ −0.15 |

⚠️ ⭐ **幅度极小（≤0.15pp），⛔ 不改变任何结论**（⭐ F1 仍全面胜出）。⛔ **但论文只提了「低于 MV」，⛔ 没提「也略低于 Direct」。** ⭐ 登记它是为了完整，⛔ 不是为了指控 —— ⭐ 这个量级在单次运行、无方差的实验里本来就在噪声内（⭐ 而这也正是 §C.6 那个「无方差」缺口的后果：⛔ **没有误差棒，就无法说这 0.15pp 是不是噪声。**）

### C.8 ⛔ 未做的消融

⛔ **无消融隔离「嵌入相似度匹配 vs 精确匹配」的贡献**；⛔ **无消融目标函数**（⭐ 二元交叉熵 vs 其它）；⛔ **无「不加约束只做概率选择」的对照**（⚠️ ⭐ 严格说 MV 部分扮演了这个角色，⛔ 但 MV 的投票是逐元素独立的，⛔ 不是同一个目标函数去掉约束）；⛔ **无「无解发生率」的报告**。

---

## D. 资产（⭐ 本轮 2026-08-13 全部实取核验）

⭐ 论文逐字（ref [52]）：`"The paper artifacts, including the prompt used in the experiments, are available at [52]."`

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（2026-08-13） |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐⭐ 🟢 | [arXiv:2508.00255](https://arxiv.org/abs/2508.00255) · [HTML v1](https://arxiv.org/html/2508.00255v1) · [DOI](https://doi.org/10.1109/MODELS67397.2025.00018) | ⭐ `abs` **HTTP 200**、`html/2508.00255v1` **HTTP 200**；⭐ **本轮已下载 244,302 bytes HTML → 76,849 字符正文并逐节通读**，⭐ 含全部章节 + Table I + 参考文献。⭐ 预印本 **CC BY 4.0**。⭐ DOI 已在 Crossref 独立核对（⭐ 标题/container/页码/作者全一致） |
| ⭐⭐ **实验代码** | ⭐⭐ 🟢 | [github.com/20001LastOrder/LLM-AbsCon](https://github.com/20001LastOrder/LLM-AbsCon) | ⭐⭐ **本轮我方独立通过 GitHub API 实取核验，⛔ 绝非空壳**。⭐ 公开、⛔ 未归档、⭐ 默认分支 `main`、⭐ 1 star、⭐ 创建 `2025-04-01T20:09:45Z`、⭐ 最后 push `2025-04-02T04:47:16Z`（⭐ **此后未动**）。⭐⭐ **HEAD commit `908e49f2ae59`**（`"Add code"`, `2025-04-02T04:47:04Z`）；⭐ **共 3 个 commit**（`908e49f2ae59` / `401064198099` "Update README.md" / `668d10e1b890` "Initial commit"）。⭐⭐ **tree 未截断：1,461 个 blob + 130 个目录。** ⭐ 核心方法码：`abscon/abstraction.py`(15,089B) · `abscon/concretization.py`(**27,661B**) · `abscon/base.py`(1,484B) · `abscon/llms.py`(2,644B) · `abscon/utils.py`(2,355B)。⛔ **license = None** |
| ⭐⭐ **prompt 是否公开** | ⭐⭐ 🟢 | `activity/prompts.py` · `taxonomy/prompts.py` · `programs/prompts.py` | ⭐⭐ **完全公开，⭐ 且本轮我方已实取并逐字读过 `activity/prompts.py`**（15,240B）：⭐ 含 `PROMPT_SIMPLE` 与 `PROMPT_SIMPLE_WITH_EXAMPLES` 完整模板、⭐ 三类节点的 Mermaid worked example（含 fork/join）、⭐ 5 条约束清单、⭐ 角色扮演句、⭐ CoT 指令。⭐ 另两个：`taxonomy/prompts.py`(13,909B) · `programs/prompts.py`(8,764B)。⭐⭐ **本卡 §B3 引的 prompt 逐字片段出自实取原文** |
| ⭐⭐ **数据集** | ⭐ 🟢 | `activity/data/` · `taxonomy/data/` · `programs/data/` | ⭐ 逐文件实取确认：⭐ `paged.json`(1,337,776B) · `paged_raw.json`(1,439,827B) · `paged_small.json`(81,139B)；⭐ `wordnet.csv`(70,955B) · `wordnet_full.csv`(461,713B)；⭐ `clevr.json`(298,431B) · `questions.json`(1,137,942B) · `scenes.json`(**33,916,162B**)。⭐⭐ **另有论文未报告的第四个数据集**：⭐ `ccs.csv`(77,752B) · `ccs_full.csv`(132,349B)（⭐ ACM-CCS 分类树）—— ⛔ **论文正文一次都没提它，⛔ 但它有完整跑完的结果**（见下一行） |
| ⭐⭐ **实验结果细则** | ⭐⭐ 🟢 | `*/results/` | ⭐⭐ **可下载的逐候选原始产出，⛔ 不只是论文内表格**：⭐ `activity/results` **421** 个条目、⭐ `taxonomy/results` **692** 个、⭐ `programs/results` **396** 个。⭐⭐ **本轮已实取一份确认格式**：`activity/results/gpt-4o/paged/results_1.csv` = **326 行 × 1 列 Mermaid 文本** —— ⭐⭐ **326 恰好等于论文的 PAGED 评测分母（331 − 5 few-shot），⭐ 即分母从 artifact 侧独立复核通过。** ⭐ 目录结构与文件语义见 §D.2 |
| ⭐ 分析脚本 | ⭐ 🟢 | notebooks | ⭐ `activity/evaluation.ipynb`(13,343B) · `activity/influence_of_consistency.ipynb`(8,742B) · `taxonomy/evaluation.ipynb`(18,281B) · `programs/influence_of_consistency.ipynb`(**105,095B**) · `measurements/rq2.ipynb`(5,407B)；⭐ `impact_of_candidates.py`(3,608B) **三份，⭐ 分别在 `activity/measurements/` · `taxonomy/measurements/` · `programs/measurements/`**；⭐ 另有与论文 Fig. 4–5 对应的 PNG（⭐ `measurements/paged_Meta-Llama-3.1-70B-Instruct.png` 等 3 张） |
| ⭐ 运行说明 | ⭐ 🟢 | `activity/README.md`(1,534B) · `taxonomy/README.md`(1,501B) · `programs/README.md`(2,241B) | ⭐ 含真实 CLI 参数（⭐ `--temperature 0.7` 用于候选、`0.01` 用于 direct；⭐ `--num_generations 10`） |
| ⭐ Clevr 执行器 | ⭐ 🟢 | `programs/program_executor.py`(17,817B) + `programs/test_program_parser.py`(4,672B) | ⭐ 实取确认 |
| ⛔ **归档 DOI** | ⛔ ⚪ | — | ⛔⛔ **无 Zenodo / OSF / figshare。** ⭐ 唯一 DOI 是论文的（IEEE + arXiv） |
| ⛔ **license** | ⛔ ⚪ | — | ⛔ GitHub API `license: None`。⚠️ **注意错配**：⭐ **arXiv 预印本是 CC BY 4.0，⛔ 而代码无 license** |
| ⛔ **4open 匿名仓库** | ⛔ **不适用** | — | ⭐⭐ **没有遇到 4open —— ⭐ artifact 是实名 GitHub 仓库，⛔ 因此不存在过期风险** |
| ⛔ MODELS artifact badge | ⛔ ⚪ | — | ⛔ 未见 artifact evaluation badge |

### D.1 ⭐⭐ 判 🟢 的理由，⭐ 与四条剩余缺口

⭐⭐ **这是本轨到目前为止 artifact 质量最好的一篇** —— ⭐ prompt、数据集、**逐候选原始产出**、方法码、分析 notebook 全都在，⭐ 而且**只有 3 个 commit、自 2025-04-02 起未动** —— ⭐⭐ **即它是一份冻结的、可 pin 的、可复算的 artifact。**

⛔ **四条缺口**：

1. ⛔ **无 license** —— ⭐ 论文是 CC BY，⛔ 代码不是任何东西。⛔ 复用授权不明。
2. ⛔ **无归档 DOI** —— ⛔ 长期可获取性依赖 GitHub 账号存续。
3. ⛔ **模型无 dated snapshot** —— ⛔ `gpt-4o` / `gpt-4o-mini` 只有别名，⛔ 两个 GPT 列不可精确复现。
4. ⛔⛔ **Llama 两列依赖私有自建端点**（`HOSTED_LLM_URL` / `HOSTED_LLM_TOKEN`，⚠️ 且代码里 `verify=False`）—— ⛔ **外人无法复现那两列。** ⭐ 另 OpenAI 调用走 `OPENAI_BASE_URL` / `OPENAI_PROXY`。

⭐⭐ **行动建议（⭐ 给 M1 / N1b）**：⭐ **这个 artifact 值得冻结并实际读一遍 `abscon/concretization.py`（27,661B）** —— ⭐ 那是「把约束写成 ILP」的具体做法，⭐⭐ **如果我们要把 pyfcstm 从求值端搬到构造端，这份代码是最接近的参考实现。** ⛔ **本轮未读该文件**（⭐ 见 F.5）。

### D.2 ⭐⭐ artifact 里有三批论文完全没报告的实验（⭐ 本轮实取核出）

⭐ **先把文件命名语义定下来**（⭐ 本轮已实取 `results_1.csv` 确认）：

| 文件名 | 含义 |
| :-- | :-- |
| ⭐ `results_N.csv` | ⭐⭐ **第 `N` 个独立候选**（⛔ **不是**第 N 次重复实验）。⭐ 每份是「326 行 × 1 列 Mermaid」，⭐ 即该候选在全部评测样本上的产出 |
| ⭐ `results_greedy.csv` | ⭐ `Direct` 基线（temp 0.01 ≈ greedy） |
| ⭐ `results_mv_N.csv` | ⭐ `MV` 基线在 `N` 个候选下的输出 |
| ⭐ `results_abscon_N.csv` | ⭐ AbsCon 在 `N` 个候选下的输出（⭐ 即 RQ3 扫描曲线的每一点） |

⭐⭐ **这一条直接解决了「有没有重复运行」这个问题**：⛔ **`N` 是候选编号，⛔ 所以「RQ1 每格只做了一次 n=10 聚合、无重复」这个判断成立。** ⚠️ ⭐ **但要注意一个细节**：⭐ 由于 10–20 个独立候选**都存着**，⭐ **候选间的离散度是可以事后算出来的**（⭐ RQ2 正是这么做的）；⛔ **缺的是 AbsCon 最终输出本身的重复。**

#### ⛔⛔ 未报告实验一 · ⭐ **四点温度消融，全域全模型跑满**

⭐ `*/results/temperature/{0.2, 0.5, 0.7, 1}/` —— ⭐ 逐目录实取确认，⭐ 每个温度点下有 `gpt-4o-mini` / `Meta-Llama-3.1-8B-Instruct` / `Meta-Llama-3.1-70B-Instruct`，⭐ 覆盖 `paged` / `wordnet` / `ccs` / `clevr` 四个数据集，⭐ 每格 10 个候选 + `results_mv_10.csv` + `results_abscon_*.csv`。

⛔⛔ **论文正文对温度只说了两句**：⭐ 候选用 **0.7**、⭐ `Direct` 用 **0.01** —— ⛔ **从未报告任何温度消融，⛔ 也从未说明 0.7 是怎么选出来的。** ⭐⭐ **而 artifact 里有一份跑满的四点扫描。**

⚠️ ⭐ **怎么读这件事（⛔ 不要过度解读）**：⛔ **这不是不端** —— ⭐ 12 页会议论文放不下所有消融是常态。⛔ **但它意味着两件事**：⭐ ① 论文里 temp = 0.7 这个选择**有实测支撑，只是没写**；⭐⭐ ② **我们可以自己把那份数据算出来** —— ⭐⭐ **即「温度对 self-consistency 式采样的影响」这个我们自己也会遇到的问题，⭐ 这里有一份现成的、四点的、跨三模型跨四数据集的公开原始数据。**

#### ⛔ 未报告实验二 · ⭐ **第四个数据集 `ccs`（ACM CCS 分类树）跑满了**

⭐ `taxonomy/results/*/ccs/` —— ⭐ 四个模型全有，⭐ 且 `gpt-4o-mini/ccs` 与两个 Llama 都有**完整的 20 候选 + 20 个 abscon 点 + 20 个 mv 点**（⭐ 即 RQ3 级别的完整扫描）。⛔ **论文正文只报 WordNet 一个分类树数据集，⛔ `ccs` 一次都没出现。**

#### ⛔ 未报告实验三 · ⭐ **有 DeepSeek 的结果文件，⛔ 而论文把 DeepSeek 列为 future work**

⭐ `taxonomy/results/gpt-4o-mini/wordnet/results_deepseek.csv` 与 `results_deepseek_1.csv` —— ⭐ 本轮实取目录清单确认存在。⚠️ ⭐ **而论文把 DeepSeek-R1 / o1 只写成未来工作。** ⛔ **本轮未打开这两个文件**，⛔ 所以无法判断它是完整跑还是一次试水（⭐ 从只有 2 个文件、且挂在 `gpt-4o-mini` 目录下看，⚠️ **更像是探索性试跑，⛔ 甚至可能是目录放错** —— ⛔ 这是 I 级推测）。

⭐⭐ **三条合起来对我们的价值**：⭐ **这个 artifact 的信息量明显大于论文本身。** ⭐ 若 M1 要拿它做参照，⭐⭐ **值得把 `temperature/` 那批算一遍** —— ⛔ 那是本轨目前唯一一份「温度 × 候选数 × 模型 × 数据集」的公开四维原始数据。

### D.3 ⭐ 与另两篇的 artifact 对照

| 项 | ⭐ **AbsCon（本篇）** | ⭐ [structure-event-driven](./structure-event-driven-stm-frameworks.md) | ⭐ [iet-software-2025](./iet-software-2025-consistency-traceability.md) |
| :-- | :-- | :-- | :-- |
| 入口 | ⭐⭐ 实名 GitHub | ⛔ 匿名 4open | ⭐ 实名 GitHub |
| commit 可 pin | ⭐⭐ **可**（`908e49f2ae59`） | ⛔⛔ **不可** | ⭐ 可（`079953dd26b1`） |
| 会不会过期 | ⭐ 不会 | ⛔⛔ **会** | ⭐ 不会 |
| 实测是否漂移 | ⭐⭐ **未漂**（⭐ 3 commit，2025-04 后未动） | ⛔ **已漂**（⭐ README/app.py 自 2026-06 变了） | ⭐ 未漂 |
| 代码 | ⭐⭐ **有，真实可跑** | ⭐ 有 | ⛔⛔ **零代码** |
| prompt | ⭐⭐ 全公开 | ⭐⭐ 全公开 | ⚠️ 只在正文里 |
| ⭐ 逐样本原始结果 | ⭐⭐ **有，CSV，1,500+ 份** | ⛔ **只有渲染后的 PNG** | ⛔ **只有 PDF** |
| license | ⛔ 无 | ⛔ 无 | ⛔ 无 |
| 归档 DOI | ⛔ 无 | ⛔ 无 | ⛔ 无 |

⭐⭐ **三篇没有一篇有 license 或归档 DOI。** ⭐ 这是一条可以写进 SUMMARY 的领域观察。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处

| # | 可搬的东西 | 为什么 |
| :-: | :-- | :-- |
| **1** | ⭐⭐⭐ **把「满足约束」从检查式改成构造式** | ⭐⭐ **本卡最重要的一条。** ⭐ 它不检查「这个模型满足约束吗」再打回，⭐ 而是把约束当硬约束写进求解器，⭐ **让不满足的解在搜索空间里不存在**。⭐⭐ **这是「裁决端」之外的第三个位置：构造端。** ⭐ M1 第二条设计原则若只写「把裁决者换成 sound oracle」，⛔ 就漏掉了这个更强的形态 |
| **2** | ⭐⭐ **把「多来一次」做成可并行的独立采样，⛔ 而不是串行修订链** | ⭐ 逐字 `"each candidate is independent and can be generated in parallel"`。⭐⭐ **我们那 79% 的修订 token 是串行花掉的，墙钟无法摊薄；⭐ 独立采样可以。** ⭐ 且它的收益在第 5–8 个候选就见底 —— ⭐ 与我们第 3 轮见底同构，⛔ 但成本结构完全不同 |
| **3** | ⭐⭐ **反泄漏纪律：方法内部用了的相似度，评测时刻意不用** | ⭐ 逐字 `"We do not use embedding similarity since it is used during the abstraction step to avoid potential bias."` ⭐⭐ **这是仓库 §3.5 第 5 条「自证式验证」的正面范例** —— ⭐ 值得直接抄进我们评测口径说明 |
| **4** | ⭐⭐ **非参数检验 + 效应量，并给出选择理由** | ⭐ Wilcoxon rank-sum + Cliff's Delta，⭐ 理由是 `"the performance distribution of LLM-generated models is unknown"`。⭐ 本轨另两篇一个检验都没做。⭐⭐ **我们报 −15.82pp 应当配检验与效应量，⛔ 而不是只报点估计** |
| **5** | ⭐ **trivial 样本剔除明写 + few-shot 样例从评测集排除** | ⭐ 分母口径干净。⭐ 与我们 `00x8` 系列永久排除的处理方式同类（⭐ 我们也是先验判据 + 明写） |
| **6** | ⭐ **把「无解」当成一种有信息量的输出，⭐ 并给了归因** | ⭐ 逐字 `"Failure to obtain a feasible solution implies that no combination of candidates can produce a consistent graph, which may indicate that the LLM is not capable of this task or that more candidates are needed."` ⭐⭐ **与仓库 §12「结构性死路 vs 采样波动」的判别思路一致** —— ⭐ 无解不是 bug，⛔ 是一个可分析的结论 |

### 2. ⛔ 不可取 / 陷阱

| # | 坑 | 与我们的对应 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **只能减、不能补** | ⭐ concretization 的决策变量只覆盖候选并集里已有的元素。⛔ **缺失元素永远无法被恢复，⛔ recall 上界被候选并集钉死。** ⚠️ ⭐ **对我们的含义**：⛔ 我们的赤字有两处，⛔ 其中「根本没问」（选题）69 位就是**缺失**类型 —— ⛔⛔ **AbsCon 这套机制对那 69 位完全无效。** ⭐ 它只能治「问了但答错」那一半 |
| **2** | ⛔⛔ **`consistent` 只管结构良构，⛔ 不管语义正确** | ⛔ 一个结构完美、内容全错的图 `Con` 也是 100%。⛔ **所以它的 96.6–100% 不能被读成「模型是对的」** —— ⭐ 它的 quality 轴（F1 只有 68–80）才是那个量，⛔ 而那一轴的提升只有 0.78%（PAGED）到 8.61%（WordNet） |
| **3** | ⛔⛔ **朴素逐元素多数投票会破坏整图性质** | ⭐ MV 基线把 `Con` 从 93–96 打到 51–71（§C.5）。⭐⭐ **若我们考虑加 self-consistency 投票，⛔ 这是必读的反面证据**：⛔ 逐元素投票 + 无整体性质缝合 = 结构崩坏 |
| **4** | ⛔ **约束 → FOL 是人工的，⭐ 每域一次** | ⛔ `"we manually translate"`。⛔ **迁移到新域要人重写一遍 FOL** —— ⭐ 这是它的隐性成本，⭐ 论文只说「实践中可从 OCL 自动导出」（⛔ 但没做） |
| **5** | ⛔ **论文的 Φ 与 artifact prompt 里的约束清单不一致** | ⭐ §B3 末段：⛔ 论文 5 条里有 2 条（决策≥2 出靶、无自环）**不在 prompt 里**，⛔ 而 prompt 多了 1 条论文没有的（连通）+ 1 条格式要求。⭐ **对我们的教训：⛔ 论文里声明的约束集必须与实际进 prompt 的那一份逐条对齐**，⛔ 否则复现者会做出不同的东西 |
| **6** | ⛔ **无成本数字、⛔ 无方差、⛔ 无消融、⛔ 无「无解率」** | ⭐ 论文明写把成本留给未来。⛔ 但它的方法**必然比 Direct 贵 10 倍**（n=10 候选）+ 图匹配（NP-hard）+ ILP —— ⛔ **而它没报这个代价。** ⚠️ ⭐ **对照我们：我们报了 212.6× 的成本**，⭐ 这一点上我们做得比它好 |
| **7** | ⛔ **无 license、⛔ 无归档 DOI、⛔ 无 dated snapshot、⛔ Llama 依赖私有端点** | ⭐ 见 §D.1 |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | 后果 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **任务不同：它做「生成」，我们做「缺陷检测」** | ⛔ 它的产出是模型，我们的产出是**关于模型的发现**。⛔ **它的 `Con` / F1 与我们的 `hit@k` 不可并列。** |
| **2** | ⛔⛔ **它比对参考图，我们比对自然语言** | ⭐ 论文**自己承认**自动比 NL 不可靠（`"may be unreliable"`）并绕开了它。⛔⛔ **我们做的正是它绕开的那件事** —— ⛔ 所以它的评测方法学对我们不可用 |
| **3** | ⛔ **它的约束是结构良构性，我们的谓词是语义检查算子** | ⛔ 良构约束可以线性化写进 ILP；⛔ **我们的 19 条谓词大部分不能**（⭐ 仿真族 6 条、BMC 族 3 条本质上不是线性约束）。⛔ **所以「把约束塞进求解器」这个招数不能整体照搬** —— ⭐ 但可以在**结构族 S 那 10 条**上考虑 |
| **4** | ⛔ **制品不是状态机，⭐ 且 1/3 案例才是行为模型** | ⭐ 见 §A.2。⭐ 活动图 + fork/join；⛔ 分类树与程序图都不适用 |
| **5** | ⛔ **无「选类」环节** | ⛔ **不是「闭合词表 + LLM 自动选」的先例。** ⭐ 本轨这个组合的先例计数 **+0** |
| **6** | ⛔ **模型代差：GPT-4o / GPT-4o-mini / Llama 3.1（2024）** | ⭐ vs 我们 `gpt-5.5` / `claude-opus-4-7`。⚠️ ⭐ **且它的核心结论对代差敏感**：⛔ 若新一代模型本身的 `Con` 已经很高（⭐ Direct 在 PAGED 上已有 93–97%），⛔ 那 ILP 能挤出的空间只剩几个百分点 —— ⭐⭐ **注意 PAGED 上 quality 提升只有 0.78%，⛔ 这个数字很可能就是「Direct 已经够好了」的表现** |
| **7** | ⛔ **它的 recall 上界是候选并集，⭐ 我们的赤字有一半是「根本没问」** | ⭐ 见 §E.2 第 1 条。⛔ **这是它对我们最不适用的一处** |

### 4. ⭐⭐ 一条跨卡观察：⭐ **同一个组、同一年、两条相反的路线**

⭐ **Boqi Chen + Gunter Mussbacher 同时署名本篇与 [`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md)。** ⭐ 两篇的技术选择几乎是镜像：

| | ⭐ **AbsCon**（MODELS 2025 主会，CCF B） | ⭐ **Structure/Event-Driven SMF**（arXiv 预印本） |
| :-- | :-- | :-- |
| LLM 阶段数 | ⭐ **1**（并行 ×10） | ⛔ **8 / 12 / 9**（串行） |
| 确定性底座 | ⭐⭐ **重**（parser + 图匹配 + ILP + CBC） | ⛔⛔ **极轻**（⭐ 只有一个格式后处理器） |
| 有无 LLM 自评 | ⛔ **零** | ⛔ **两处，⭐ 且都在自己的职责上失效** |
| 有无求解器 | ⭐⭐ **有（核心）** | ⛔ **无**（⚠️ 手里有 `umple.jar` 却没接进去） |
| 结果 | ⭐⭐ **一致性 96.6–100%** | ⛔ **最好的 F1 来自基线（0.7029），⛔ 被提出的框架在强模型上全输** |
| 制品 | ⚠️ 图（1/3 是活动图） | ⭐⭐ **UML 状态机（正题）** |

⭐⭐ **这个对照本身对 M1 有信息量**：⛔ **多步 prompting 那条路线在同题任务上没打赢基线；⭐ 而「一次采样 + 求解器」那条路线上了 CCF B 主会并拿到 96.6–100%。** ⚠️ ⭐ **必须谨慎**（⛔ 两篇的任务、制品、指标都不同，⛔ 不构成受控对照），⭐ **但方向性提示很强：把工程量投到确定性底座上，比投到更多轮 LLM 调用上更划算。** ⭐⭐ **这与我们 v46 的实测（⛔ 确定性裁决者付钱、⛔ LLM 自评不付钱）完全同向。**

### 5. ⭐⭐ 三卡合并后的一条结论（⭐ 给 m1_recommendations 直接取用）

⭐ 把本卡与 [`llm-guided-predicate-discovery`](./llm-guided-predicate-discovery.md)、[`structure-event-driven-stm-frameworks`](./structure-event-driven-stm-frameworks.md) 并起来看，⭐ 「裁决者位置」有一条清晰的阶梯：

| 位置 | 代表 | 效果 |
| :-- | :-- | :-- |
| ⭐⭐ **构造端**（让不合规的解不存在） | ⭐ **AbsCon**（CBC ILP） | ⭐⭐ **一致性 96.6–100%，⭐ 零迭代** |
| ⭐ **裁决端 · 确定性**（检查后打回，判据可复算） | ⭐ **RunVS**（反例判定）· ⭐ 我们的 `precheck_and_seal` | ⭐ **有效，⭐ 且白跑的轮次几乎免费** |
| ⚠️ **裁决端 · 词法规则**（判据可复算，⛔ 但把语义做成词法） | ⭐ [`iet-software-2025`](./iet-software-2025-consistency-traceability.md)（业务对象名等号匹配） | ⚠️ **能用，⛔ 但误判来自措辞差异** |
| ⛔⛔ **裁决端 · LLM 自评** | ⛔ 我们的两个 reviewer · ⛔ SMF 的 `FinalSanityCheck` / `FilterTransitions` | ⛔⛔ **零收益（我们）到负收益（SMF 的 precision 0.20）** |
| ⛔ **无裁决者** | ⛔ SMF 的单提示与多步主干 | ⛔ 基线赢过被提出的方法 |

⭐⭐⭐ **M1 的落点很清楚：把 pyfcstm 从「求值端」往上搬，⭐ 且首选目标不是「裁决端」而是「构造端」** —— ⛔ 至少对结构族 S 那 10 条谓词而言。

---

## F. ⛔ 存疑与未核项

1. ⚠️ **Figure 1 / 2 / 3 / 4 / 5 的图内内容未核。** —— ⭐ 已试过：⭐ arXiv HTML 全文（⭐ 图题可读，⛔ 图内元模型与约束的图形表示不可读）。⭐ **代偿**：⭐ 流程图的 5 条约束、分类树的 3 条、Clevr 的 8 条**均有正文散文版本，⭐ 本轮已逐字核过**。⛔ **但 Fig. 1 / Fig. 3 里的元模型图形细节未核**（⭐ 论文自陈 Clevr 的第 8 条 `"not shown in the figure for brevity"`）。
2. ⚠️ **Fig. 4 / Fig. 5 的具体曲线数值未核。** —— ⭐ RQ2 的箱线图与 RQ3 的候选数扫描曲线只有图，⛔ 无数值表。⭐ **代偿路径已确认可行但本轮未走**：⭐ artifact 里逐候选 CSV 与 `results_abscon_N.csv`（⭐ 即扫描曲线的每一点）齐全，⭐ 加上 `measurements/rq2.ipynb` 与三份 `impact_of_candidates.py`，⭐ **可复算出那两张图的全部数字**。⭐⭐ **若 M1 需要精确的「第 k 个候选的边际收益」逐点数字，⭐ 这条路是通的** —— ⛔ 本轮没走。
3. ⭐⭐ **【本轮已解决】「RQ1 每格只跑一次、无重复」原为 S 级推断，⭐ 现已从 artifact 侧证实。** —— ⭐ 我实取了 `activity/results/gpt-4o/paged/results_1.csv`：⭐ **326 行 × 1 列 Mermaid 文本**，⭐ 即它是**第 1 个候选在全部 326 个评测样本上的产出**，⛔ **不是第 1 次重复实验**。⭐ 同目录另有 `results_greedy.csv`（Direct 基线）与 `results_mv_10.csv`（MV 基线）。⭐⭐ **所以 `N` 是候选编号，⛔ 「无重复」的判断成立。** ⚠️ **但要加一条限定**：⭐ 由于 10–20 个独立候选都存着，⭐ **候选间离散度事后可算**（⭐ RQ2 就是这么做的）；⛔ **缺的只是 AbsCon 最终输出本身的重复。** ⭐ 详见 §D.2。
4. ⛔⛔ **「无解」（infeasible）发生了多少次，原文未提供。** —— ⭐ 已试过 grep `infeasible` / `Failure to obtain`（⭐ 只在 §III-E 那句方法学说明里出现一次）。⛔ **论文没有报无解率。** ⚠️ ⭐ 这对我们重要：⛔ **如果无解率不低，那「零迭代」的代价就是「有一部分样本没有输出」** —— ⛔ 而那正是仓库 §10 讲的「崩掉的格等于样本消失」。⛔ **本篇无法回答。**
5. ⛔ **`abscon/concretization.py`(27,661B) 本轮未读。** —— ⭐ 它是「把约束写成 ILP」的具体实现，⭐⭐ **也是 M1 若要把 pyfcstm 搬到构造端时最直接的参考。** ⛔ 本卡关于 ILP 建模的描述全部来自论文正文，⛔ 未与实现对拍。
6. ⭐⭐ **【本轮已部分解决】artifact 里有三批论文未报告的实验 —— ⭐ 目录结构已核实，⛔ 但内容未逐份打开。** ⭐ 详见 §D.2：⭐ ① **四点温度消融**（`temperature/{0.2,0.5,0.7,1}/` × 3 模型 × 4 数据集，⭐ 每格 10 候选 + MV + AbsCon）—— ⭐ 目录与文件数已逐格核过，⛔ **未打开任一 CSV 算结果**；⭐ ② **第四个数据集 `ccs`（ACM CCS 分类树）**，⭐ 四模型全跑，⭐ 三个模型有完整 20 点扫描 —— ⛔ 未算；⭐ ③ **`results_deepseek.csv` / `results_deepseek_1.csv`**（⭐ 挂在 `taxonomy/results/gpt-4o-mini/wordnet/` 下），⚠️ **而论文把 DeepSeek 列为 future work** —— ⛔ **本轮未打开这两个文件**，⛔ 无法判断是完整跑还是试水，⚠️ 也无法排除目录放错（**I**）。
7. ⚠️ **soft precision / soft recall / soft F1 的确切公式未核。** —— ⭐ 论文引 Fränti & Mariescu-Istodor（soft cardinality），⛔ **本轮未去原文核该定义**。⭐ 所以本卡对 Table I 里 P/R/F1 的解读停留在「soft cardinality 意义下的关系集比对」，⛔ 未能说明 soft 具体软在哪。
8. ⚠️ **两个 GPT 模型的 dated snapshot 无法确定。** —— ⛔ 论文与 artifact 均只有别名。⛔ 复现时这是硬缺口。⭐ Llama 两列另有私有端点问题（⭐ `HOSTED_LLM_URL`，⛔ 外人无法访问）。
9. ⚠️ **MODELS 2025 的 artifact evaluation 情况未核。** —— ⛔ 本轮未查该会是否设 artifact track、⛔ 也未查本文是否申请过 badge。⛔ 不得据「未见 badge」断言它没通过评审 —— ⭐ **可能是没申请。**
10. ⚠️ **`ccf = B` 的判定来自本仓库 [ccf_venues/01-venue-scope.md](../../../../../ccf_venues/01-venue-scope.md) 的 `conf-b-models | MoDELS | 🥈` 一行。** —— ⛔ **本轮未独立核对官方 CCF 目录**，⭐ 但这是仓库内已核过的事实源，⭐ 可信度足够。
11. ⚠️ **同会另有一篇同名近亲，⛔ 不要混。** —— ⭐ MODELS 2025 的 **SRC（ACM Student Research Competition）** track 里有一篇「Consistent Graph Model Generation with Large Language Models」（⭐ 标题少了 `Accurate and`），⛔ **是另一个更短的条目**。⚠️ ⭐ **引用时务必用 DOI `10.1109/MODELS67397.2025.00018` 与页码 130–141 锁定本篇**（⭐ 12 页主会 Research Papers），⛔ 不要引到 SRC 那篇。⛔ **本轮未取 SRC 那篇的元信息。**
12. ⚠️ **`accurate` 与 `quality` 在原文里近乎互换使用，⛔ 本卡按「quality（论文亦称 accuracy）」统一处理。** —— ⭐ 严格说论文的 Abstract 用 `inaccuracy` 命名第三个问题，⭐ 而 §V-B 的指标名叫 `quality`。⛔ **两者是否严格同义，原文未明确定义。**
