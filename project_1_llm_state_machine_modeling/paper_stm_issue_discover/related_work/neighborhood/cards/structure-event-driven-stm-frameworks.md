# 卡片 · Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models

⭐ **本卡的一句话结论**：⭐⭐ **这是本轨里与我们同题程度最高的一篇**（非结构化 NL → UML 状态机，逐分量 P/R/F1），⛔ **但它对本轨的核心问题给出的是一个「零」答案** —— 四条流水线里**一个反馈循环都没有、一个裁决者都没有**，唯一的确定性底座是一个 rule-based post-processor，而它的作用是**丢弃不合规输出**而不是把不合规打回重做。⭐ 它真正贵重的地方在**另外一件事**：它是我们能找到的唯一一篇**在同一套任务上把「单提示」与「分阶段多步」做了 2 模型 × 4 策略完整对照**的工作，⭐ 而结论是 **分阶段的价值完全取决于模型强度：弱模型 +8～+11pp，强模型 −7～−40pp，且全实验最好的数字来自「基线」而不是来自任何一个被提出的框架。**

⚠️ **本卡包含一批「原文没有、本轮从公开 artifact 自算」的数字。** ⭐ 凡属自算一律显式标注 `⚙️ 自算`，⛔ 不与 M 级原文数字混排。⭐ 自算的可信度由一件事背书：⭐⭐ **我用同一套聚合方法复算全 7 分量，在 8 个「策略 × 模型」格里精确复现了论文 6 格到小数点后 4 位**（见 C 节 §C.9），⛔ 剩下 2 格的偏差本身就是发现。

---

## A. 元信息

| 字段 | 值 |
| :-- | :-- |
| `id` | `structure-event-driven-stm-frameworks` |
| `title` | Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models |
| 作者 | Samer Abdulkarim, Evan Boyd, Karl Bridi, Alec Tufenkjian（⭐ 四人等贡献）, Boqi Chen, Gunter Mussbacher —— McGill University, Electrical and Computer Engineering |
| `year` | **2026**（arXiv v1，逐字 `arXiv:2604.00275v1 [cs.SE] 31 Mar 2026`） |
| `venue` | ⛔ **arXiv 预印本**（`cs.SE`）—— ⛔ 原文无任何 venue / 投稿状态标记 |
| `ccf` | ⚪ **不适用**（预印本） |
| `doi` | [10.48550/arXiv.2604.00275](https://doi.org/10.48550/arXiv.2604.00275) |
| `arxiv` | [2604.00275](https://arxiv.org/abs/2604.00275) —— ⭐ 本轮实测 `abs` 页 **HTTP 200**、`html/2604.00275v1` **HTTP 200** |
| `url` | ⭐ 本卡全文来源：**本仓库本地副本** [`baselines/structure-and-event-driven-frameworks-.../paper_content.txt`](../../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper_content.txt)（10 页，已全文通读） |
| 工具名 | ⭐ 论文正文**未给方法起名**；⚠️ **artifact 的 README 自称 `AutoState`**（逐字：`# AutoState: State Machine-Driven LLM Framework for UML Modeling Automation`）—— ⛔ 这个名字在论文里一次都没出现 |
| `artifact_type` | ⭐ **UML 状态机**（单提示输出 `Umple` 代码；多步框架输出 3 张 HTML table，再经后处理） |
| `task` | ⭐ **生成**（NL → 状态机）—— ⛔ **不是**缺陷检测、⛔ 不是一致性检查、⛔ 不是修复 |
| `boundary` | ⚠️ **界内 5 / 界外 2 混合** —— 见下方 §A.2，⛔ 这一格是本卡最容易被错用的地方 |

### A.1 ⭐ 硬门核对

| 硬门 | 判定 | 理由 |
| :-- | :-: | :-- |
| 1 · 基于 LLM | ⭐⭐ **过（最强的一种过）** | LLM 是方法的**全部**：四条策略的每一个阶段都是一次 LLM 调用，⛔ 除 post-processor 外没有非 LLM 环节 |
| 2 · 行为类模型制品 | ⭐⭐ **过（最强的一种过）** | 制品就是 UML 状态机本身 |

### A.2 ⚠️⚠️ 边界拆分（⛔ 本卡必须先读这一格）

⭐ 论文评的是 **7 个分量**，⛔ 其中 **2 个落在我们 $M = (S,E,V,Tr,A)$ 之外**：

| 分量 | 边界 | 理由 |
| :-- | :-: | :-- |
| States | ⭐ **界内** | $S$ |
| Transitions | ⭐ **界内** | $Tr$ |
| Guards | ⭐ **界内** | 迁移守卫，$Tr$ 的一部分 |
| Actions | ⭐ **界内** | ⭐ $A$；⚠️ 论文**只算迁移上的动作**，逐字：`"we are only considering actions on transitions and not entry/exit/do actions in states"` |
| Hierarchical states | ⭐ **界内** | ⭐ HSM 层次结构，正是 project_1 三个核心关注点之一 |
| **Parallel regions** | ⛔⛔ **界外** | ⛔ **正交并发语义** —— 仓库根 CLAUDE.md 明确把「正交区并发语义」排除在 project_1 建模对象之外 |
| **History states** | ⛔ **界外** | ⛔ history 是 UML 伪状态，$M = (S,E,V,Tr,A)$ 里没有它 |

⚠️ **这意味着论文报的 overall F1（0.5431 / 0.7029 / …）不能直接当作「我们边界内的数字」引用。** ⭐ 本卡在 §C.10 给出**只含界内 5 分量**的自算版本，⛔ 并说明它改变了什么、没改变什么。

⭐ **一件对我们有利的事实**：⭐⭐ **论文全篇零时钟、零时间约束、零不变式。** ⭐ grep 全文，`clock` / `timed automaton` / `invariant` 均零命中；⭐ 唯一与时间沾边的是 `Chess Clock` 这个案例名（那是被建模的系统，不是时钟变量）。⛔ 所以它与我们的边界冲突**只在并发 + history 两处**，⛔ 没有更深的语义鸿沟。

---

## B. LLM 应用形态

### B1 · 流水线阶段（⭐⭐ **四条并列策略，不是一条流水线**）

⚠️ **本篇的形状与本轨其它卡不同**：⛔ 它不是「一条流水线」，而是**四条互相竞争的生成策略**，用同一个评测端量。⭐ 逐条画出来（阶段数以 artifact 源码里的 FSM 定义为准，见 §B1.5）：

```
── 策略 1 · Single-Prompt Baseline ── 阶段数 1，LLM 1 ──
[人] 非结构化 NL 系统描述
  → [LLM ×1] 3-shot 一次性直出完整 Umple 状态机
  → 完（⛔ 无 post-processor 参与，输出已是 Umple 代码）

── 策略 2 · Structure-Driven SMF ── ⭐ 阶段数 8，LLM 8 ──
[人] NL 描述
  → [LLM] 1. states + events（⭐ temp 0.5）
  → [LLM] 2. parallel regions
  → [LLM] 3. transitions + guards
  → [LLM] 4. actions
  → [LLM] 5. hierarchical states（分组相似状态）
  → [LLM] 6. history states
  → [LLM] 7. initial state
  → [LLM] 8. ⛔⛔ FinalSanityCheck（⭐ LLM 自评：逐句回扫描述、原地补表）
  → [确定性] rule-based post-processor → 3 张 HTML table

── 策略 3 · Event-Driven SMF ── ⭐ 阶段数 12，LLM 12 ──
[人] NL 描述
  → [LLM] 1. system name → [LLM] 2. states（⭐ temp 0.5）→ [LLM] 3. initial state
  → [LLM] 4. events
  → [LLM] 5. 逐事件问「该事件能在哪些状态发生」
  → [LLM] 6. 由「状态 × 事件」组建 transitions
  → [LLM] 7. ⛔⛔ filter transitions（⭐ LLM 自评：**专为压 false positive 而设**）
  → [LLM] 8. parallel regions → [LLM] 9. hierarchical states → [LLM] 10. 各层次态的 initial state
  → [LLM] 11. 把子状态共有迁移上提到父状态
  → [LLM] 12. history states
  → [确定性] post-processor → 3 张 HTML table

── 策略 4 · Hybrid Approach ── ⭐ 阶段数 1 + 8 = 9，LLM 9 ──
[人] NL 描述
  → [LLM ×1] Single-Prompt 出一份完整 Umple 草稿
  → ⭐ 把该草稿**原文附在 Structure-Driven SMF 每一个 prompt 的末尾**
     （逐字提示语：`"this solution was provided by your helpful colleague as a baseline"`）
  → [LLM ×8] 走完 Structure-Driven 的 8 步
  → [确定性] post-processor → 3 张 HTML table
```

⭐⭐ **形状要点（⛔ 三条，都与本轨的问题正面相关）**：

1. ⛔⛔ **四条策略里一条循环都没有。** ⭐ 全部是**单向流水**（strictly feed-forward）：第 `k` 步的输出喂给第 `k+1` 步，⛔ **没有任何一步能把控制权交回前面的步**。
2. ⛔ **唯一的确定性环节（post-processor）在流水线末端，而且它的失败处理是「退回上一版」而不是「打回重做」。** ⭐ 逐字（§III-A）：`"In case post-processing fails for a state machine component in a step, then the output of the last step where the component was successfully post-processed is considered."` ⭐ 这是**降级**，不是**反馈**。
3. ⚠️ **阶段总数在论文正文里查不到。** ⭐ 论文只写「Step 1 … Step 2 … Step 3 … Step 4 … and so on」（§III-A），⛔ 剩下几步靠图 2 / 图 4，⛔ 而图无法从 `paper_content.txt` 读出。⭐ **上面的 8 / 12 是我去 artifact 源码里数出来的**（见 §B1.5），⛔ 不是论文给的。

### B1.5 ⭐⭐ 阶段数的出处：artifact 源码里的 FSM 定义（**M**，⛔ 但出自代码不是论文）

⭐⭐ **一个很有意思的自指结构**：⛔ 这套「用 LLM 建状态机」的流水线，⭐ 它自己就是用一台状态机编排的（这也是 README 自称 `AutoState` 的原因）。

⭐ Structure-Driven SMF 的真源是 [`backend/simple_linear_smf/simple_linear_smf_transitions.py`](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/backend/simple_linear_smf/simple_linear_smf_transitions.py)（2,351 bytes，本轮实取），⛔ 里面是 8 条 `trigger / source / dest / before` 的迁移记录。⭐ **逐字抄下它的 8 条步骤注释**：

```
# step 1: identify the states and events of the UML State Machine in a "From State" to "To State" manner using StateEventSearchAction
# step 2: identify the parallel states of the UML State Machine using ParallelRegionSearchAction
# step 3: identify the transitions along with their guards of the UML State Machine using TransitionsGuardsSearchAction
# step 4: add actions to identified transitions using ActionSearchAction
# step 5: group similar states using HierarchicalStateSearchAction
# step 6: identify history states using HistoryStateSearchAction
# step 7: identify state machine initial state
# step 8: ask LLM to revise its created tables using FinalSanityCheckAction
```

⭐ 状态链逐字为 `SearchStatesEvents → ParallelRegions → TransitionsGuards → FiguringActions → HierarchicalStates → HistoryStates → InitialStateSearch → SanityCheck → Done`。⛔⛔ **`dest` 全是下一个状态，没有一条指回前面** —— ⭐ 这就是「无循环」的机械证据，⛔ 不是我从论文措辞推的。

⭐ Event-Driven SMF 同理（[`backend/event_driven_smf/event_driven_smf_transitions.py`](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/backend/event_driven_smf/event_driven_smf_transitions.py)，4,704 bytes）。⚠️ **注意它的注释编号有笔误**：⛔ 有两个 `# step 10`，⛔ 且直接从 10 跳到 13、14，⛔ 所以「14 步」是错的，⭐ **实际迁移条目 12 条**。

### B2 · 每次 LLM 调用的角色

| 阶段 | 角色 |
| :-- | :-- |
| Single-Prompt 单步 | ⭐ **生成器**（一次产出终态制品） |
| Structure-Driven step 1–7 · Event-Driven step 1–6/8–12 | ⭐ **抽取器**（从 NL 里找某一类分量）+ **生成器** |
| Event-Driven step 5（逐事件问处理方式） | ⭐ **抽取器**，⚠️ 但形态特殊：⭐ **对每个事件单独发一次调用**，⛔ 调用次数随事件数线性增长 |
| ⛔ **Structure-Driven step 8 · FinalSanityCheck** | ⛔⛔ **评审者（LLM 自评）** —— ⭐ 见 §B4，这是全篇唯一的自评环节 |
| ⛔ **Event-Driven step 7 · FilterTransitions** | ⛔⛔ **评审者 / 过滤器（LLM 自评）** —— ⭐ 见 §B4，⭐ **它的实测结果是本卡对 M1 最有价值的一条** |
| Hybrid 的草稿注入 | ⭐ **修复者 / 精化者**（⛔ 但没有裁决者告诉它哪里要修） |

⛔ **全篇没有**：裁决者（判定「这是不是一条发现」）· 规划者（决定下一步做什么，⭐ 步序是**硬编码**的）· 分类器 · 解释者 · 检索改写器。

### B3 · prompt 策略

| 项 | 值 |
| :-- | :-- |
| few-shot | ⭐ **有，且两档不同** —— 逐字（§V-B）：`"We use a 2-shot prompting strategy … for our multi-step generation strategies. For our single-prompt strategy we employ 3-shot prompting, adding another ground truth state machine, ChessClock, to our pool, aiming to improve upon the baseline accuracy."` |
| ⚠️ **2-shot vs 3-shot 是一处不对称** | ⛔⛔ **被提出的框架用 2-shot，基线用 3-shot** —— ⭐ 论文自陈动机是 `"aiming to improve upon the baseline accuracy"`，⭐ 即**刻意把基线做强**。⭐ **方向对作者自己不利，是加分项而非减分项**，⛔ 但引用时必须一起说，⛔ 否则「基线赢了」这个结论会被误读 |
| ⭐ **样例泄漏防护** | ⭐ **有，且明写** —— 逐字：`"If a particular state machine is used as test input, it is excluded from the examples shown to the LLM, ensuring that the LLM is never tested on a state machine it has already seen in the prompt."` ⭐ **这条纪律值得抄** |
| CoT | ⭐ **有**（与 few-shot 组合）—— 逐字（§II）：`"We use a combination of both techniques to enhance performance."` |
| ⭐ 结构化输出约束 | ⚠️ **有，但是「弱」的一种** —— ⭐ 靠 **HTML table 格式 + 严格列约束**（prompt 逐字：`"Your output tables must have the same exact format as specified below. You are NOT allowed to add extra columns."`），⛔ **不是** JSON schema、⛔ 不是 Pydantic、⛔ 不是受限解码，⛔ 也**没有**解析失败原地回灌重试 |
| 输出长度上限 | ⭐ **1500 tokens / prompt**（逐字：`"We also limited the LLMs to generate up to 1500 tokens for each prompt."`）—— ⚠️ 对 W-UMPLE（17 states / 41 transitions）这种规模，⭐ 这个上限**很可能就是那次全崩的机制原因**，⛔ 见 §C.7 |
| ⛔ 无 | RAG · 工具调用 / function calling · self-consistency 投票 · 多智能体辩论 · 角色扮演（⚠️ 严格说 prompt 里有 `"You are an AI assistant specialized in creating UML state machines"`，⭐ 算轻度角色设定，⛔ 但没有多角色对抗） |
| prompt 是否公开 | ⭐⭐ **完全公开**（⭐ 本轮逐文件实取，见 D 节）—— ⭐ Structure-Driven 7 个 `.txt` + Event-Driven 9 个 `.txt` + 3 份 n-shot 例子 `.py` |

⭐⭐ **一条 prompt 工程层面的观察（对我们直接有用）**：⭐ 我实取了 `FinalSanityCheckAction.txt` 全文（1,043 bytes），⛔ 它的最后一段是**纯激励性话术**，⚠️ 与任务毫无关系：

> ⭐ 逐字：`"Your methodical approach to state machine verification protects against subtle behavioral flaws. Each scenario you analyze helps validate our state machine's correctness. Your commitment to thorough testing ensures reliable system behavior in all conditions."`

⚠️ ⛔ **这三句话不含任何可执行指令、不含判据、不含形状要求。** ⭐ 它是「夸模型让它更努力」那一类 prompt 迷信的残留。⛔ 对照我们的做法（每条谓词带 `nl_cue`、带形状约束、带 worked example），⭐ **这里的自评步骤在 prompt 层面几乎是空的** —— ⛔ 而它实测零效果（§B4），⚠️ **两件事很可能是同一件事**。

### B4 · ⭐⭐ 循环与裁决者（⛔ 本轨最关键的一格）

| 子字段 | 值 |
| :-- | :-- |
| **有无循环** | ⛔⛔ **无。四条策略全部是单向流水。** ⭐ 机械证据见 §B1.5（`dest` 无一条回指） |
| ⭐ **裁决者是谁** | ⛔⛔ **没有裁决者。** ⭐ 没有任何环节决定「要不要再来一轮」，⛔ 因为根本没有「再来一轮」这个动作 |
| 终止条件 | ⭐ **走完固定步数**（8 / 12 / 9），⛔ 不是收敛、不是预算、不是人叫停 |
| 最大轮数 | ⛔ **不适用**（无轮次概念） |
| ⭐ 有无报告循环的边际收益 | ⛔ **无**（无循环则无此数） |

⭐⭐ **但有两个「一次性自评环节」，⛔ 它们不是循环，⭐ 却恰好构成对我们那条「LLM 自评零收益」发现的两次独立旁证。** ⭐ 逐个说，⛔ 因为这是本卡最值钱的部分。

#### ⛔ 旁证一 · Structure-Driven step 8 `FinalSanityCheck` —— LLM 逐句回扫补漏

⭐ 我实取了 prompt 全文。⭐ **它做的事逐字是**：

> `"Your task is to ensure to examine each sentence in the description. If the sentence is relevant to {table_name}, then add an entry in the {table_name} table. If the sentence is not relevant to {table_name}, then do not add an entry to the table for the sentence."`

⭐⭐ **这在形态上就是「需求侧覆盖回扫」** —— ⭐ 拿原始 NL 的**每一句**去问「模型里有没有对应的东西」，⛔ 没有就补。⚠️ **这正是我们 C-③ 那一维想要的方向**（「需求说了而模型没有」）。⛔ **但它的三个特征让它不能直接借鉴**：

1. ⛔ **裁决者是 LLM 自己**，⛔ 没有任何机械核验。
2. ⛔ **只跑一遍**，⛔ 跑完直接 `→ Done`。
3. ⛔⛔ **它只被允许「加」，不被允许「删」** —— ⭐ prompt 里只有 `add an entry`，⛔ 没有任何一句授权它删除错项。⚠️ **这是一个单向偏置的自评器。**

⭐⭐ **实测结果（⚙️ 自算，见 §C.10 与 §C.6）**：⭐ Structure-Driven 是**四条策略里 precision 最不稳的一条之一**，⛔ 且 GPT-4o 上 precision 相对基线**下降** 0.7130 → 0.6562（−0.0568，⭐ 这是 M 级原文数字）。⭐ **一个只准加不准删的自评器带来 precision 下降，方向完全自洽。**

#### ⛔⛔ 旁证二 · Event-Driven step 7 `FilterTransitions` —— ⭐⭐ **本卡最值得 M1 看的一格**

⭐ 源码注释逐字：`"# step 7: filter the transitions created in step 6 to reduce number of false positives using EventDrivenFilterTransitionsAction"`。

⭐⭐ **也就是说：Event-Driven SMF 里专门有一个 LLM 自评步骤，唯一职责就是压 false positive。** ⛔ **然后 Event-Driven 成了全实验 precision 最差的一条策略，差得不是一点：**

| 策略 | GPT-4o precision | Claude precision |
| :-- | --: | --: |
| Single-Prompt（⛔ **无任何过滤**） | **0.7130** | **0.7931** |
| Structure-Driven | 0.6562 | 0.5041 |
| Hybrid | 0.7110 | 0.6368 |
| ⛔⛔ **Event-Driven（⭐ 带专用 FP 过滤器）** | ⛔ **0.2667** | ⛔⛔ **0.2038** |

⭐ 全是 M 级（Table IV / VI）。⭐ 论文自己的解释逐字（§V-F）：

> `"One possible explanation is that while this strategy achieves the highest recall, it suffers from extremely low precision, indicating that it tends to overgenerate elements that are not present in the ground truth."`

⚠️ ⛔ **论文没有把这件事和它自己那个 filter 步骤联系起来** —— ⭐ 因为 filter 步骤在论文正文里根本没被提到（⭐ 我是从源码里挖出来的）。⭐⭐ **于是这里有一条论文没说、但由「论文数字 + 公开源码」共同支撑的结论**：

> ⭐⭐ **一个专为压 FP 而设的 LLM 自评步骤，在最需要它的那条流水线上，把 precision 压到了 0.20** —— ⛔ 比完全不过滤的基线低 **0.59**（Claude：0.7931 → 0.2038）。

⭐ 严格说，这不是「filter 让 precision 变差」的因果证明（⛔ 没有 filter 的消融对照），⚠️ **但它足以否证「加一个 LLM 自评过滤器就能控住多报」这个假设**。⭐⭐ **这与我们 v46 的实测同向且更极端**：⛔ 我们的两个 LLM 自评 reviewer 是**零收益**，⛔ 这里的 LLM 自评 filter 是**在它唯一的职责上彻底失效**。

#### ⭐ 那么 Hybrid 算不算「带反馈的第二遍」？

⚠️ **不算，⛔ 但它是本卡里最接近「反馈」的东西，值得单独讲清楚。** ⭐ Hybrid 的机制逐字（§III-A）：

> `"the LLM is first prompted to generate a complete state machine in Umple syntax using the Single-Prompt Baseline. Then, this fully generated solution is appended at the end of all prompts within the Structure-Driven SMF (e.g., "this solution was provided by your helpful colleague as a baseline") to guide the LLM in refining and expanding upon the initial draft"`

⭐ **它是「把一版完整草稿当上下文注入」，⛔ 不是「把某个检查器的判定当反馈回灌」。** ⛔ 三点差别：

1. ⛔ 注入的是**草稿本身**，⛔ 不是**关于草稿的诊断**。
2. ⛔ 没有任何东西告诉后续步骤「草稿哪里错了」。
3. ⛔ 只发生一次，⛔ 不迭代。

⭐⭐ **但它是全实验对 GPT-4o 最有效的策略（0.6559，7 个分量里 6 个最优）。** ⚠️ ⭐ **这一条对 M1 有直接含义**：⭐ 在没有任何裁决者的前提下，**仅靠「保住一份全局草稿再逐分量细化」就拿到了最大增益** —— ⛔ 说明这批增益的来源是**上下文完整性**，⛔ 而不是**反馈**。⭐ 我们那 79% 花在修订机器上的 token，⚠️ **可能有相当一部分买的是这个「上下文完整性」而不是「修订」本身**，⛔ 但本篇不能证明这一点。

### B5 · ⭐ 中间表示

| 子字段 | 值 |
| :-- | :-- |
| **有无** | ⭐ **有（多步策略）/ 无（单提示）** —— ⭐ 这两者的差别本身就是论文的一个 threat（见下） |
| **形态** | ⭐ **3 张固定列结构的 HTML table**（§III-A + 图 3）。⛔ 不是 DSL、⛔ 不是缺陷类型学、⛔ 不是谓词族、⛔ 不是 JSON schema |
| ⭐ **是否闭合** | ⚠️⚠️ **两层要分开答，⛔ 混起来会得出错误对照** —— 见下方拆解 |
| ⭐ **谁定的** | ⭐ **作者预定义** —— 逐字（§IV-B）：`"we considered the seven components of the state machine that we deemed to be the most characteristic or representative of the state machine modeling decisions"`。⛔ 不是从语料归纳、⛔ 不是 LLM 生成、⛔ 不是从标准条文导出 |

#### ⚠️ 「是否闭合」的两层拆解（⛔ 本格最容易被错位对照）

| 层 | 闭合性 | 说明 |
| :-- | :-: | :-- |
| **分量类型集合**（7 类：states / transitions / guards / actions / hierarchical / parallel / history） | ⭐ **闭合** | ⭐ 固定 7 类，⛔ 既是**步序的骨架**（Structure-Driven 一步一类），⛔ 也是**评测的分母**。⭐ 由作者预编 |
| **每类里的具体内容**（哪些 state、哪个 guard 表达式） | ⛔ **完全开放** | ⛔ LLM 自由生成，⛔ 无候选集、⛔ 无词表、⛔ 无枚举约束 |

⭐⭐ **与我们的关键错位（⛔ 必须说清，否则会被误读成先例）**：

- ⭐ 我们的 **19 条闭合谓词词表** 是「**问什么问题**」的闭合集合 —— ⭐ 模型从固定 19 个**检查算子**里选。
- ⛔ 它的 **7 类分量** 是「**产出什么零件**」的闭合集合 —— ⭐ 模型按固定顺序填 7 种**制品成分**。
- ⛔⛔ **两者都叫「闭合」，但闭合的对象一个是提问、一个是产物，不是同一件事。** ⛔ **不得把它当作「闭合词表 + LLM 自动选」的先例。**
- ⛔ **更关键的是「谁选」这一格**：⭐ 我们是 **LLM 在每条需求上自动选谓词**；⛔ 它是 **步序硬编码，没有任何选择动作** —— ⛔ 第 3 步一定做 transitions+guards，⛔ 模型无权决定这条需求该问什么。⭐ **所以它在 B5 的「谁选类」这一格上，答案是「没人选，写死的」。**

#### ⚠️ 中间表示带来的一个 threat，论文自己承认了

⭐ 逐字（§V-G Internal validity）：

> `"The Single-Prompt Baseline and the multi-step generation strategies use different output syntaxes to represent state machines. … This fundamental difference means that the Single-Prompt Baseline focuses on direct code generation, whereas the multi-step generation strategies are structured reasoning tasks. As such, performance results should be considered in the context of these fundamental differences in task structure and output representation. Furthermore, the strict post-processor module for HTML tables may suppress valid LLM outputs that are not fully compliant, hence influencing the final result."`

⚠️⚠️ **这一段极重要，⛔ 它意味着「单提示 vs 多步」这个对照并非同构**：⛔ 单提示走 Umple 代码通道（⭐ 模型的强项），⛔ 多步走 HTML table 通道（⛔ 且要过一个会「suppress valid outputs」的严格后处理）。⭐⭐ **所以 §C.8 那些 Δ 值里，有多少来自「分阶段」、有多少来自「换了输出语言 + 多了一道会丢东西的后处理」，本篇无法分离。** ⛔ 引用这些 Δ 时必须带上这句限定。

### B6 · 模型

| 模型 | 定位 | 精确度 |
| :-- | :-- | :-- |
| **GPT-4o** | ⭐ 论文归为 **non-reasoning LLM** | ⛔ **无 snapshot 日期**（`"accessed via OpenAI's API"`）—— ⛔ 不可 pin |
| **Claude 3.5 Sonnet** | ⚠️ 论文归为 **reasoning LLM** | ⛔ **无 snapshot 日期**（`"via Anthropic API"`）—— ⛔ 不可 pin，⚠️ 而 Claude 3.5 Sonnet 有两个版本（2024-06 / 2024-10），⛔ 无法判断用的是哪个 |

⭐ 多模型对照：⭐⭐ **有，而且是全因子** —— 2 模型 × 4 策略 × 8 系统 = 64 格，⭐ 全部报出。⭐ **这一点比本轨大多数工作做得好。**

#### ⚠️⚠️ 一条必须标 **I** 的重要质疑：「reasoning vs non-reasoning」这个轴很可能名不副实

⭐ 论文的分类逐字（§II）：`"Some LLMs (e.g., DeepSeek-R1, Claude 3.5 Sonnet) are designed or fine-tuned to generate intermediate reasoning steps (a chain-of-thoughts) as part of their output. We refer to these as reasoning LLMs."`

⚠️ ⭐ **我方判断（I，⛔ 不写成事实句）**：⛔ 把 **Claude 3.5 Sonnet** 与 **DeepSeek-R1** 归为同一类，看起来站不住 —— ⭐ Claude 3.5 Sonnet 没有 o1/R1 那种独立的推理阶段或 thinking budget，⭐ 它在业界通常不被算作 reasoning model。⛔ **若这个归类不成立，则论文 RQ3 的因果解释也随之松动。** ⭐ 论文的解释逐字是：

> `"multi-step strategies may interfere with the step-by-step reasoning process embodied within reasoning LLMs such as Claude 3.5 Sonnet."`

⚠️ ⭐ **一个同样能解释全部数据、且不需要「reasoning 架构」这个前提的替代假设（I）**：⛔ 观察到的现象只是「**分阶段帮弱模型、伤强模型**」—— ⭐ 即**能力效应**而非**推理架构效应**。⭐⭐ **论文自己的证据其实更支持这个简单版本**，⭐ 因为它紧接着就给了一个纯能力/通道层面的解释（§V-E）：

> `"The lower overall F1-scores of the Hybrid Approach (0.6336), Structure-Driven SMF (0.5026), and Event-Driven SMF (0.3052) suggest that the multi-step strategies do not leverage a key strength of Claude 3.5 Sonnet: its single-step code generation capabilities."`

⭐ **这条对 M1 的实际含义**：⛔ **不要把本篇当成「reasoning 模型不需要分阶段」的证据**，⭐ 而应当当成「**在更强的模型上，分阶段的收益会转负**」的证据。⚠️ ⭐ 而我们用的是 `gpt-5.5` / `claude-opus-4-7` —— ⛔ **两个都远强于本篇的两个模型**，⛔ 所以按本篇的趋势外推，⚠️ **分阶段对我们的净收益预期应当是负的或接近零**。⛔ 这是 I 级外推，⛔ 不是本篇的结论。

### B7 · ⭐ 确定性成分（⛔ 本卡这一格几乎是空的）

| 环节 | 是什么 | 评价 |
| :-- | :-- | :-- |
| **rule-based post-processor** | ⭐ 合并 / 精化 LLM 输出，输出 3 张 HTML table。逐字（§III-A）：`"the framework includes a strict rule-based post-processor module that merges and refines the LLM outputs"` | ⚠️ **唯一的确定性环节**。⛔ 但它是**格式合规过滤器 + 合并器**，⛔ 不是语义检查器，⛔ 更不是裁决者 |
| 温度设置 | 0.01（多数步）/ 0.5（state / event 发现步） | ⭐ 确定性配置，⛔ 不是流水线环节 |
| 1500 token 上限 | 每次调用的输出上限 | ⚠️ 见 §C.7 —— ⛔ 这个上限很可能是一次整格全崩的机制原因 |
| ⛔ **Umple 编译器** | ⚠️⚠️ **artifact 里有 `umple.jar`（3,134,073 bytes，本轮实取确认），⛔ 但论文正文从未说它被用来校验生成结果** | ⛔ **这是一个「有 sound oracle 却没接进流水线」的实例**，⛔ 见下 |

⭐⭐ **本格最重要的一条观察**：

> ⛔⛔ **他们手里有一个真正的 parser / 编译器（`umple.jar`，3.1 MB，就躺在 `backend/resources/` 里），⛔ 而单提示策略的输出恰好就是 Umple 代码 —— ⛔ 也就是说「把生成结果丢给 Umple 编译一下」这件事在工程上唾手可得。⛔ 但论文里没有任何一处把编译结果用作反馈、门或裁决。**

⭐ 严格说，`umple.jar` 的实际用途原文未提供（⚠️ 从 artifact 结构看**最可能是渲染状态机图片**，⭐ 因为 `Paper Experiment Resources/Final */` 下确实存着大量 `.png`；⛔ 这是 I 级推测）。⭐⭐ **但无论用途如何，「一个可用的 sound-ish oracle 存在于仓库里、却不在裁决路径上」这个拓扑，与我们「pyfcstm 在求值端而不在裁决端」是同一个毛病** —— ⛔ 区别在于我们至少把它接进了求值，⛔ 他们连求值都没接。

---

## C. 实验

| 字段 | 值 |
| :-- | :-- |
| `baseline` | ⭐ **Single-Prompt Baseline**（⭐ 自建、内生）—— ⛔ **无任何外部方法作为 baseline**。⚠️ 论文自陈无先例可比，逐字（§IV-A）：`"to the best of our knowledge, this is the first exploration into automated state machine generation from non-structured NL system descriptions with LLMs, and as such, no existing evaluators are available for performing automated state machine evaluation"` |
| `dataset` | ⭐ **8 个** 非结构化英文 reactive-system 描述 + 专家参考状态机。⭐ 来源逐字：`"from an undergraduate university course, designed to assess students' proficiency in state machine design"`。⭐ 8 个系统：`Printer` `Spa Manager` `Dishwasher` `Chess Clock` `Bread Maker` `Thermomix TM6` `W-UMPLE` `SSC7` |
| ⭐ **分母怎么定的** | ⭐ **逐分量按 ground-truth 计数**（Table I 全表见 §C.2）。⚠️⚠️ **但 overall 的分母不稳定，⛔ 见 §C.6 与 §C.7 —— ⭐ 这是本卡最硬的两条发现** |
| `metrics` | ⭐ `precision` / `recall` / `F1`，⭐ 逐 7 分量 + overall。⛔⛔ **无任何 `@k` 口径** —— ⛔ 无 `hit@k`、⛔ 无 `pass@k`、⛔ 无多轮聚合 |
| ⭐ `judged_by` | ⛔⛔ **作者手工，且「一个策略一个人」** —— 见 §C.3。⛔ **无标注者间一致性、⛔ 无 $\kappa$、⛔ 无第二评分者、⛔ 无 LLM-as-judge** |
| `human_baseline` | ⚠️ **无**（⭐ 专家参考解是 **ground truth**，⛔ 不是「人在同条件下的表现」对照臂） |
| `runs` | ⛔⛔ **每格 1 次，⛔ 无方差、⛔ 无重复** —— 见 §C.4 |
| ⭐ `adverse_results` | ⭐⭐ **处理得相当坦白**（⭐ 4 类不利结果全部正面报出）—— 见 §C.5 |

### C.1 三个 RQ（逐字）

> `1: How well do reasoning and non-reasoning LLMs generate state machines using a single-prompt technique?` `2: How much do the multi-step generation strategies improve state machine generation for non-reasoning LLMs compared to the single-prompt technique from RQ1?` `3: How well do the multi-step generation strategies from RQ2 generalize to reasoning LLMs for state machine generation?`

### C.2 ⭐ ground-truth 规模（**M**，Table I 逐字抄）

| 分量 | Printer | Spa Mgr | Dishwasher | Chess Clock | Bread Maker | Thermomix | W-UMPLE | SSC7 |
| :-- | --: | --: | --: | --: | --: | --: | --: | --: |
| States | 6 | 11 | 9 | 9 | 9 | 9 | **17** | 7 |
| Transitions | 17 | 17 | 17 | 16 | 17 | 17 | **41** | 24 |
| Guards | 6 | 4 | 4 | 4 | 4 | 7 | 5 | 10 |
| Actions | 3 | **0** | 7 | 6 | 5 | 6 | **24** | 16 |
| Hierarchical states | 2 | 3 | 2 | 3 | 3 | 1 | 5 | 1 |
| Parallel regions | **0** | 5 | 2 | 2 | **0** | **0** | 2 | **0** |
| History states | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

⭐ **两个直接后果**：

1. ⭐ **W-UMPLE 是压倒性最大的一个**（17 states / 41 transitions / 24 actions），⛔ 且它正是出事的那一个（§C.7）。
2. ⭐ **好几格 ground truth 为 0**（Spa Manager 的 actions；4 个系统的 parallel regions）。⭐ 这些格在 workbook 里记为 `N/A`，⛔ **即分母逐系统变化**。⭐ 这本身是正确处理，⛔ 但它与 §C.7 那个 bug 叠加后就产生了口径问题。

### C.3 ⛔⛔ `judged_by`：本卡这一格必须完整读

⭐ 逐字（§IV-A）：

> `"Therefore, we manually evaluate the outputs from the generation strategies."` `"To streamline the evaluation process, we adopt an approach focused on efficiency and consistency. A single author conducts the evaluation for a given designed approach."`

⭐ 逐字（§V-G Internal validity）：

> `"The manual evaluation of the experiments is done by a subset of the authors, which may introduce bias. We compensate for this bias by agreeing on evaluation guidelines."`

⭐ **拆开看，这套判定机制有四个特征**：

| 特征 | 内容 | 评价 |
| :-- | :-- | :-- |
| 判定主体 | ⛔ **作者本人** | ⛔ 非第三方 |
| ⛔ **判定粒度** | ⛔⛔ **一个策略 = 一个人**（`A single author conducts the evaluation for a given designed approach`） | ⛔⛔ **这是最严重的一条**：⛔ 四条策略由**不同的人**评，⛔ 而论文的核心结论正是**跨策略比较**。⚠️ **策略间的差异与评分者间的差异在这个设计下无法分离。** |
| 一致性度量 | ⛔⛔ **完全没有** | ⛔ 无 $\kappa$、⛔ 无双评、⛔ 无一致率、⛔ 无仲裁流程 |
| 偏差缓解 | ⭐ 「事先商定评分指南」+「严格判据」 | ⚠️ 逐字：`"We compensate for this bias by agreeing on evaluation guidelines."` ⛔ **商定指南不产生一致性数据**，⛔ 无法验证指南被一致执行 |

⭐⭐ **F1 到底是怎么算的（⛔ 本任务的必答 ③，分三层答）**：

**第一层 · 匹配是什么？** ⭐⭐ **人的语义等价判断，⛔ 不是状态名字符串匹配，⛔ 也不是结构同构。** 逐字（§IV-A / §IV-B）：

> `"To minimize bias, the evaluation protocol focuses on identifying exact or near-exact matches between the generated outputs and the ground-truth state machine. In essence, if two components are intended to represent the same concept (e.g., the same state or action), they are graded as equivalent, even if their names differ."` `"The first category includes the generated components that have an exact match or semantic match with the ground-truth model (true positives). This also includes the components which are named differently than in the ground-truth model but serve the same purpose (superstates or parallel regions that contain the same set of matching substates for instance)."`

⭐ **并且他们明确说了为什么不能自动化**，逐字（§IV-A）：

> `"Due to the subjective nature of model-driven software design, two or more state machine designs may correctly model the same behavior for a given problem description. For instance, while state names, hierarchical state names, or parallel region names might differ between two state machines, the underlying transitions and overall behavior of the components could remain the same. Consequently, automating the evaluation of a state machine output is complex."`

**第二层 · 有一条级联惩罚规则（⭐ 很重要，⛔ 容易漏）。** 逐字（§IV-B）：

> `"By default, transitions that are connected to states that do not match any state in the ground-truth model are considered false positives. A similar strategy is applied to guards and actions that belong to false positive transitions. This underlines a strict evaluation schema for transitions, guards, and actions that recognizes the fact that they are of little value if the component(s) on which they depend are incorrect."`

⭐⭐ **即：state 错 → 挂在它上面的 transition 自动 FP → 挂在该 transition 上的 guard/action 也自动 FP。** ⭐ 这是**依赖闭包式惩罚**，⭐ 会放大 state 层错误的影响。⭐ **这条设计本身是对的**（⚠️ 与我们「引用门要求缺失名出现在 primary 的依赖闭包内」是同类思路），⭐ 论文也承认它压低了绝对值（§V-G：`"The strictness of the evaluation regarding transitions, guards, and conditions may lead to lower evaluation results but ensures greater consistency across different graders."`）。

**第三层 · overall 怎么聚合？** ⭐ 论文逐字（§IV-C）：

> `"in addition to the overall result (computed by aggregating the true positives (TP), false positives (FP), and false negatives (FN) of all components)"`

⭐⭐ **⚙️ 我实测反推出的完整口径是**：⭐ **先在每个系统内把 7 个分量的 TP/FP/FN 求和 → 算该系统的 P/R/F1（micro）→ 再对 8 个系统取算术平均（macro）**。⭐ **这个口径在 8 格里精确复现论文 6 格到 4 位小数**（§C.9），⛔ 所以它是对的。⚠️ **一个副作用值得记**：⛔ 由于 P、R、F1 **各自独立取平均**，⛔ 报出的三元组**不满足** $F_1 = 2PR/(P+R)$。⭐ 例：GPT-4o 单提示报 `P=0.7130, R=0.4501, F1=0.5431`，⛔ 但 $2 \times 0.7130 \times 0.4501 / (0.7130+0.4501) = 0.5519 \ne 0.5431$。⭐ **这不是错，是 macro 平均的正常性质**，⛔ 但读者若按公式反算会对不上。

### C.4 `runs`：⛔ 单次，⛔ 且论文自己指出了这个缺口却用错了缓解手段

⭐ 逐字（§V-G Internal validity）：

> `"Due to the temperature of 0.5 used in the creative setting for state generation steps (Section V-B), the generated state machines can be different for each run of the Structure-Driven SMF, Event-Driven SMF, and Hybrid Approach. Based on informal observations, we believe the higher temperature is of value as it leads to more states being proposed by the LLM, thus improving recall rates. We mitigate this risk by averaging the results of eight state machine examples."`

⚠️⚠️ **「用 8 个样例取平均」并不缓解「同一样例跑多次会不同」。** ⛔ 前者降的是**样例间**方差，⛔ 后者是**运行间**方差 —— ⛔ **两个不同的量，前者不是后者的替代。** ⭐ 而且 `"Based on informal observations"` 逐字承认了温度选择的依据是非正式观察。

⭐⭐ **这一条对我们的直接意义**：⭐ 我们做的正是这件他们没做的事 —— ⭐ **3 轮 + `hit@1` / `hit@3` / `hit@all` 三口径**。⛔ **本篇 8 个格子的每一个数字都只有一次采样，⛔ 因此它的「策略 A 优于策略 B」结论没有稳定性证据。** ⭐ 这是我们相对它的一个真实方法学优势，⛔ 但也要注意：⚠️ 我们能这么做是因为我们的样本量（54 pair）撑得起，⛔ 他们只有 8 个。

### C.5 ⭐⭐ `adverse_results`：⭐ 处理方式值得直接借鉴

⭐ **四类对作者自己不利的结果，全部正面写出，⛔ 没有一条被埋在附录或省略**：

| # | 不利结果 | 论文怎么处理 |
| :-- | :-- | :-- |
| 1 | ⛔ **被提出的两个 SMF 里有一个（Event-Driven）大幅劣于基线** | ⭐ **写进摘要外的每一个相关章节**，⭐ 并给出机制解释（overgeneration → precision 崩）。⭐ 逐字（§V-F）：`"The poor performance of the Event-Driven SMF compared to other strategies is unexpected, given that state machines are inherently event-driven."` ⭐ **「unexpected」这个词用得很诚实** |
| 2 | ⛔⛔ **对更强的那个模型，所有被提出的策略都输给基线** | ⭐ **直接写成 RQ3 的答案**，⛔ 不加修饰。⭐ 逐字：`"For the Claude 3.5 Sonnet reasoning LLM, the Single-Prompt Baseline achieves a higher overall state machine F1-score than the Structure-Driven SMF, Event-Driven SMF, and Hybrid Approach."` ⭐ 并在结论里再说一次：`"the multi-step generation strategies do not consistently outperform the Single-Prompt Baseline"` |
| 3 | ⛔ **GPT-4o 的 actions F1 = 0.0000（完全失败）** | ⭐ **摘要里就写出来**：`"e.g., F1-scores of 0.23 for guards and 0.00 for actions for GPT-4o"`。⭐⭐ **把自己最差的数字放进摘要，⭐ 这个做法值得抄** |
| 4 | ⛔ **总体结论是「还不够用」** | ⭐ 摘要 + 每个 RQ 的答案 + 结论都说：`"their performance is not yet fully sufficient for a fully automated solution"` |

⭐⭐ **对我们「−15.82pp」那条的直接借鉴（⛔ 这是本节的落点）**：

1. ⭐ **把不利数字写进摘要**，⛔ 不要藏在结果节深处。⭐ 他们把 `0.00` 放进了 abstract。
2. ⭐ **给不利结果配机制解释，而不是配辩解。** ⭐ Event-Driven 崩了，他们说的是「它 overgenerate，recall 最高但 precision 崩」—— ⛔ 这是**机制**；⛔ 他们没有说「但它在某个子分量上最好所以其实不错」（⚠️ 尽管它在 parallel regions / history states 上确实最好，⭐ 他们把这一点单独作为一个观察写，⛔ 而不是拿它去救 overall）。
3. ⭐ **让不利结果直接进 RQ 的答案框。** ⭐ RQ3 的 answer box 逐字就是「多步不如单提示」，⛔ 没有软化。
4. ⚠️ **他们没做、我们应该做的一件事**：⛔ 他们**没有把不利结果转成「所以下一步该改什么」的具体设计动作**，⭐ 只写了「future work includes investigating further generation strategies」。⭐⭐ **我们的 −15.82pp 报告应当比这走得更远一步：给出可落地的下一步。**

### C.6 ⛔⛔ 发现一：`Event-Driven / GPT-4o / W-UMPLE` 的 `All` 行与它自己的分量行对不上

⭐ **这是我复算全 64 格（8 系统 × 4 策略 × 2 模型）后唯一的一处内部不一致，⛔ 但它落在论文报出的数字上。**

⭐ 公开 workbook `Final Detailed F1-Scores.xlsx`（⭐ SHA-256 `fe3cb7e4…4bbf`，本轮实取核对）里，`EventDriven` sheet 的 `WUMPLE (event-driven)` / GPT-4o 块：

| 来源 | TP | FN | FP |
| :-- | --: | --: | --: |
| ⭐ 该系统 7 个分量行**求和** | **26** | **58** | **187** |
| ⛔ 该系统的 `All` 行 | ⛔ **46** | ⛔ **75** | ⛔ **232** |
| **差** | ⛔ **+20** | ⛔ **+17** | ⛔ **+45** |

⭐ 逐分量原始值（⚙️ 自算，⭐ 直接抄自 workbook）：States `6/11/12`、Transitions `8/24/78`、Guards `2/2/24`、Actions `5/18/69`、Hierarchical `3/2/2`、Parallel Regions `1/1/1`、History States `1/0/1` → 和 = `26/58/187`。⛔ `All` 行却是 `46/75/232`。

⭐ **后果**：⭐ 论文 Table IV 报 Event-Driven / GPT-4o overall `F1 = 0.3735`（⭐ 取自 `All` 行的跨系统平均）；⛔ **若改用分量行求和重算，得 `F1 = 0.3665`**（⚙️ 自算，Δ = −0.0070）。

⚠️ **影响评估**：⛔ 幅度很小（0.7pp），⛔ **不改变任何结论**（Event-Driven 无论 0.3735 还是 0.3665 都是垫底）。⭐ **登记它的理由不是它重要，而是它证明了 workbook 的 `All` 列不是从分量列算出来的**，⛔ 因此 §C.7 那个更严重的问题不能假定「`All` 列可信」。

### C.7 ⛔⛔⛔ 发现二：⭐ 论文的 GPT-4o 单提示基线，分母是 **7** 而不是 **8**

⭐⭐ **这是本卡最硬的一条发现，⛔ 且它直接影响本任务的必答 ①。**

⭐ workbook `SinglePrompt` sheet，GPT-4o 块，`WUMPLE (single prompt)` 这一格：

| 分量 | TP | FN | FP | P | R | F |
| :-- | --: | --: | --: | :-- | :-- | :-- |
| States | 0 | 17 | 0 | 0 | 0 | 0 |
| Transitions | 0 | 41 | 0 | 0 | 0 | 0 |
| Guards | 0 | 5 | 0 | 0 | 0 | 0 |
| Actions | 0 | 24 | 0 | 0 | 0 | 0 |
| Hierarchical states | 0 | 5 | 0 | 0 | 0 | 0 |
| Parallel Regions | 0 | 2 | 0 | 0 | 0 | 0 |
| History States | 0 | 1 | 0 | 0 | 0 | 0 |
| ⛔ **All** | ⛔ **0** | ⛔ **95** | ⛔ **0** | ⛔ **空** | ⛔ **空** | ⛔ **空** |

⭐⭐ **读法**：⛔ **GPT-4o 在 W-UMPLE 上的单提示运行产出了「零 TP 且零 FP」** —— ⛔ 即**什么都没有被评上，连一个错的元素都没有**。⭐ 这不是「答错了」，⛔ 是**整格没有可评产物**（⭐ 全部 95 个 ground-truth 元素记为 FN）。

⭐ **于是 $P = 0/(0+0)$ 未定义**，⭐ workbook 的 P/R/F 三格是**空的**，⛔ 而空格在跨系统求平均时**被跳过**。

⭐⭐ **⚙️ 自算验证（⛔ 精确到 4 位）**：

| 口径 | 分母 | P | R | F1 | 与论文 |
| :-- | :-: | --: | --: | --: | :-- |
| ⛔ **丢掉 W-UMPLE**（⭐ 空格跳过） | **7** | **0.7130** | **0.4501** | **0.5431** | ⭐⭐ **精确等于论文 Table IV** |
| ⭐ **W-UMPLE 记 F1 = 0**（⭐ 零 TP 就是零 F1） | **8** | 0.6238 | 0.3938 | ⛔ **0.4752** | ⛔ **低 6.79 pp** |

⭐ **所以论文那个 `0.5431` 是 7 个系统的平均，⛔ 而它被拿去和 8 个系统平均的 `0.6260 / 0.3735 / 0.6559` 直接比较。**

#### ⚠️ 偏差方向：⛔ **对作者自己不利，⛔ 不是有利**

⭐⭐ **必须把方向说清楚，⛔ 否则会变成一条错误指控。** ⭐ 剔除的是一次**基线的彻底失败**，⛔ 所以剔除**抬高了基线** —— ⛔ 而基线是他们要打败的对象。⭐ **修正后，他们自己的核心主张变得更强而不是更弱**：

| 对照（GPT-4o，全 7 分量） | ⭐ 论文口径（基线 n=7） | ⚙️ 统一 n=8 口径 |
| :-- | --: | --: |
| Single-Prompt | 0.5431 | **0.4752** |
| Structure-Driven | 0.6260（**Δ = +0.0829**） | 0.6260（⭐ **Δ = +0.1508**） |
| Hybrid | 0.6559（**Δ = +0.1128**） | 0.6559（⭐ **Δ = +0.1807**） |

⭐⭐ **即：论文把自己的增益低报了约 7 pp。** ⭐ 这与「剔除不利样本抬高自己」是**反向**的，⛔ 所以本卡把它登记为**口径不一致 + 一次未被讨论的整格失败**，⛔ **不登记为选择性剔除**。

#### ⛔ 但仍有两条实质问题

1. ⛔⛔ **论文正文完全没有提到这次整格失败。** ⭐ grep 全文，`W-UMPLE` 只在 Table I 的图例（`W..W-UMPLE`）和数据集描述里出现，⛔ **没有任何一句说「GPT-4o 单提示在 W-UMPLE 上没有产出」**。⭐ 而这是全实验里**唯一**的整格零产出，⛔ 且发生在**最大的那个系统**上（17 states / 41 transitions / 95 元素）。
2. ⚠️ **机制原因很可能是 1500 token 输出上限（I，⛔ 我方推测，⛔ 原文未提供）**：⭐ W-UMPLE 的参考解有 41 条迁移 + 24 个动作，⛔ 一份完整 Umple 状态机码在 1500 token 内几乎不可能写完；⭐ 而 `Actions` 在 GPT-4o 单提示上**全 8 个系统合计 F1 = 0.0000**，⚠️ 与「输出被截断在动作还没写到之前」这个解释相容。⛔ **这是推测，不是事实**：⛔ 也可能是 API 报错、格式不合规被判全 FN、或人工评分时判定无可评内容。⛔ **artifact 里没有该格的 raw output 可查**（⭐ `Final Single Prompt/` 下只有图片）。

⭐⭐ **对我们的直接映射（⛔ 这是本节最该带走的东西）**：⛔ **这正是仓库 CLAUDE.md §10 讲的那件事** —— 「⛔ **崩掉的格没有产物，等于该样本从被测集里消失**，⛔ 而最容易崩的恰恰是缺陷最硬的样本」。⭐ 本篇给了一个**外部实例**：⛔ 最大最难的那个系统在基线上整格无产出，⛔ 于是它**静默地退出了那一格的分母**，⛔ 论文正文一个字都没提。⭐ **我们的 eligibility filter + 降级落盘纪律，正是为了避免这个。**

### C.8 ⭐⭐ 必答 ① · single-step vs multi-step 的完整对照

#### 全 7 分量（**M**，⭐ Table IV / VI 逐字）

| 策略 | GPT-4o（non-reasoning） | | | Claude 3.5 Sonnet（论文称 reasoning） | | |
| :-- | --: | --: | --: | --: | --: | --: |
| | **P** | **R** | **F1** | **P** | **R** | **F1** |
| **Single-Prompt Baseline** | 0.7130 | 0.4501 | **0.5431** | **0.7931** | 0.6384 | ⭐⭐ **0.7029** |
| **Structure-Driven SMF** | 0.6562 | 0.6268 | **0.6260** | 0.5041 | 0.5116 | 0.5026 |
| **Event-Driven SMF** | ⛔ 0.2667 | **0.6870** | ⛔ **0.3735** | ⛔⛔ 0.2038 | **0.6542** | ⛔ **0.3052** |
| **Hybrid Approach** | 0.7110 | 0.6142 | ⭐ **0.6559** | 0.6368 | 0.6473 | 0.6336 |

#### ⭐⭐ 「分阶段到底值多少」—— Δ F1 相对同模型的单提示基线

| 策略 | GPT-4o（论文口径） | ⚙️ GPT-4o（统一 n=8） | Claude |
| :-- | --: | --: | --: |
| Structure-Driven | ⭐ **+0.0829** | ⭐ **+0.1508** | ⛔ **−0.2003** |
| Event-Driven | ⛔ **−0.1696** | ⛔ **−0.1087** | ⛔⛔ **−0.3977** |
| Hybrid | ⭐ **+0.1128** | ⭐ **+0.1807** | ⛔ **−0.0693** |

⭐⭐⭐ **答案，四句话**：

1. ⭐ **在弱模型（GPT-4o）上，分阶段值 +8.3 pp（Structure）到 +11.3 pp（Hybrid）** —— ⚙️ 若把基线的分母修正统一到 8，则是 **+15.1 pp 到 +18.1 pp**。
2. ⛔⛔ **在强模型（Claude 3.5 Sonnet）上，分阶段值负数，全部三条都是** —— **−6.9 pp（Hybrid）、−20.0 pp（Structure）、−39.8 pp（Event）**。⛔ **没有一条策略打赢基线。**
3. ⛔⛔ **全实验最好的单个数字 `0.7029` 来自基线，不来自任何一个被提出的框架。** ⭐ 摘要里那两个被拿来当门面的数字（`F1 = 0.90 for states and 0.75 for transitions`）**也是基线的数字**（⭐ Claude 单提示的 States 0.8991 / Transitions 0.7502）—— ⛔ **不是被提出方法的数字。** ⚠️ 引用本篇时若说「他们的方法 state F1 0.90」，那是**错的**。
4. ⚠️ **「分阶段」与「换输出通道」这两个因素本篇分不开**（§B5 末段的 threat）：⛔ 单提示走 Umple 代码，多步走 HTML table + 严格后处理。⛔ **所以上面所有 Δ 都是「分阶段 + 换通道 + 加后处理」的联合效应**，⛔ 不是「分阶段」的净效应。

#### ⭐ 逐分量 F1（**M**，⭐ Table III / V 逐字，⭐ 界外分量已标记）

**GPT-4o**

| 策略 | States | Transitions | Guards | Actions | Hierarchical | ⛔ Parallel | ⛔ History |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| Single-Prompt | 0.8038 | 0.5741 | 0.2348 | ⛔ **0.0000** | 0.5810 | 0.1905 | **0.4286** |
| Structure-Driven | 0.7377 | 0.6277 | 0.2611 | 0.3250 | 0.6962 | 0.1429 | 0.1250 |
| Event-Driven | 0.6584 | 0.3432 | 0.2295 | 0.2391 | 0.6208 | **0.3173** | 0.2083 |
| Hybrid | ⭐ **0.8582** | ⭐ **0.7107** | ⭐ **0.4240** | ⭐ **0.3436** | ⭐ **0.7928** | ⭐ **0.3429** | 0.1250 |

**Claude 3.5 Sonnet**

| 策略 | States | Transitions | Guards | Actions | Hierarchical | ⛔ Parallel | ⛔ History |
| :-- | --: | --: | --: | --: | --: | --: | --: |
| Single-Prompt | ⭐ **0.8991** | ⭐ **0.7502** | ⭐ **0.5645** | 0.1633 | 0.6509 | 0.5333 | 0.2500 |
| Structure-Driven | 0.8203 | 0.5145 | 0.2744 | 0.2380 | 0.5592 | 0.5333 | 0.1250 |
| Event-Driven | 0.7314 | 0.2988 | 0.1525 | 0.1862 | 0.4750 | ⭐ **0.5500** | ⭐ **0.4583** |
| Hybrid | 0.8737 | 0.7209 | 0.4152 | ⭐ **0.3375** | ⭐ **0.7132** | 0.3939 | 0.3333 |

⭐ **难度阶梯很清楚，⭐ 且两个模型一致**：`states`（0.66–0.90）> `hierarchical`（0.48–0.79）> `transitions`（0.30–0.75）> `guards`（0.15–0.56）> `actions`（0.00–0.34）。⭐ **actions 是最难的分量，⛔ 而它恰在我们边界内（$A$）。**

⭐ 论文自己对 actions 的诊断（**M**，§V-F）：

> `"The poor performance on actions highlights a significant limitation in current LLMs' ability to extract non-explicit behaviors from textual descriptions."`

### C.9 ⚙️ 复算校准（⛔ 本卡所有自算数字的可信度背书）

⭐ 我从公开 workbook 逐系统逐分量取 TP/FN/FP，⭐ 按 §C.3 第三层反推出的口径重算全 7 分量 overall F1，⭐ 与论文 Table IV / VI 对拍：

| 策略 | 模型 | ⚙️ 复算 F1 | ⭐ 论文 F1 | Δ | 判定 |
| :-- | :-- | --: | --: | --: | :-- |
| Single-Prompt | Claude | 0.7029 | 0.7029 | **0.0000** | ⭐ **精确复现** |
| Structure-Driven | GPT-4o | 0.6260 | 0.6260 | **0.0000** | ⭐ **精确复现** |
| Structure-Driven | Claude | 0.5026 | 0.5026 | **0.0000** | ⭐ **精确复现** |
| Event-Driven | Claude | 0.3052 | 0.3052 | **0.0000** | ⭐ **精确复现** |
| Hybrid | GPT-4o | 0.6559 | 0.6559 | **0.0000** | ⭐ **精确复现** |
| Hybrid | Claude | 0.6336 | 0.6336 | **0.0000** | ⭐ **精确复现** |
| ⛔ Single-Prompt | GPT-4o | 0.4752 | 0.5431 | ⛔ −0.0679 | ⛔ **§C.7 的 n=7 问题** |
| ⛔ Event-Driven | GPT-4o | 0.3665 | 0.3735 | ⛔ −0.0070 | ⛔ **§C.6 的 `All` 行不一致** |

⭐⭐ **6/8 精确到小数点后 4 位** —— ⭐ 说明口径反推正确；⛔ 剩下 2 格的偏差**各自都有已定位的、可复现的原因**，⛔ 不是我算错。⭐ **所以 §C.10 的界内自算数字可以用。**

### C.10 ⚙️⚙️ 必答 ④ · 只算界内 5 分量会怎样

⭐ 剔除 `Parallel Regions` 与 `History States`（⛔ 两个界外分量），⭐ 用同一口径重算：

| 策略 | ⚙️ GPT-4o 界内 F1 | ⚙️ Claude 界内 F1 | ⭐ 对照：全 7 分量（论文） |
| :-- | --: | --: | :-- |
| Single-Prompt | **0.4780**（n=8）/ **0.5463**（n=7，⭐ 论文口径） | **0.7077** | 0.5431 / 0.7029 |
| Structure-Driven | **0.6318** | **0.5114** | 0.6260 / 0.5026 |
| Event-Driven | **0.3621** | **0.2999** | 0.3735 / 0.3052 |
| Hybrid | ⭐ **0.6663** | **0.6391** | 0.6559 / 0.6336 |

⭐ **界外 2 分量单独算（⚙️ 自算，n=8）** —— ⭐ 用来看它们到底拖了多少：

| 策略 | ⚙️ GPT-4o 界外 F1 | ⚙️ Claude 界外 F1 |
| :-- | --: | --: |
| Single-Prompt | 0.2708 | 0.4213 |
| Structure-Driven | ⛔ **0.0833** | 0.2521 |
| Event-Driven | 0.2857 | ⭐ **0.4821** |
| Hybrid | 0.1667 | 0.3438 |

⭐⭐ **界内 Δ（single vs multi-step）**：

| 策略 | ⚙️ GPT-4o（n=7 基线，论文口径） | ⚙️ GPT-4o（统一 n=8） | ⚙️ Claude |
| :-- | --: | --: | --: |
| Structure-Driven | **+0.0856** | **+0.1539** | ⛔ **−0.1963** |
| Event-Driven | ⛔ **−0.1842** | ⛔ **−0.1159** | ⛔ **−0.4078** |
| Hybrid | ⭐ **+0.1201** | ⭐ **+0.1884** | ⛔ **−0.0686** |

⭐⭐⭐ **答案（⛔ 三句）**：

1. ⭐⭐ **限定到界内，什么结论都没变。** ⭐ 所有 Δ 的**符号完全一致**，⭐ 量级变化在 ±3.5 pp 内，⭐ 策略排序**一格未动**（GPT-4o：Hybrid > Structure > Single > Event；Claude：Single > Hybrid > Structure > Event）。
2. ⭐ **界外两个分量确实是最弱的**（界外 F1 0.08–0.48 vs 界内 0.30–0.71），⭐ 所以剔除它们**普遍略微抬高**数字，⛔ 但抬得很少（⭐ 因为它们的元素**计数**也少：ground truth 里 parallel regions 共 11 个、history states 共 8 个，⛔ 相对 states 77 / transitions 166 是小量）。
3. ⭐ **一个例外方向值得记**：⛔ **Event-Driven 在界外分量上反而是最强的**（Claude 界外 0.4821 为四策略最高，⭐ parallel regions 0.5500 / history states 0.4583 都是它最好）。⭐ 论文也注意到了这点。⚠️ ⭐ **对我们的含义是「反向」的**：⛔ Event-Driven 唯一的相对优势恰好落在**我们不要的那两个分量上**，⛔ 所以**从我们的边界看，Event-Driven 比论文显示的还要更没有价值。**

---

## D. 资产（⭐ 本轮 2026-08-13 全部实取核验）

⭐ artifact 入口（论文 `[18]`，逐字 `Anonymous, "Paper artifacts." [Online]. Available: https://anonymous.4open.science/r/llm state machine modeling/`）。

⚠️⚠️ **踩坑先说**：⛔ 论文给的普通 `/r/...` 路由**不是**可用的人类入口（⭐ 会 302 到 API 并可能回 `401 {"error":"not_connected"}`）。⭐ **可用入口有两个**：⭐ 浏览器 hashbang `https://anonymous.4open.science/#!/r/llm_state_machine_modeling/`，⭐ 与 API `https://anonymous.4open.science/api/repo/llm_state_machine_modeling/...`。

| 资源类型 | 状态 | URL / 路径 | ⭐ 核验证据（2026-08-13 实取） |
| :-- | :-: | :-- | :-- |
| 论文全文 | ⭐ 🟢 | [arXiv:2604.00275](https://arxiv.org/abs/2604.00275) · [本地 PDF](../../../../baselines/structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/paper.pdf) | ⭐ `abs` **HTTP 200**；⭐ `html/2604.00275v1` **HTTP 200**；⭐ 本地 538,695 bytes PDF + 已提取 `paper_content.txt`（10 页，本卡据其全文通读） |
| ⭐ **实验代码** | ⭐ 🟢 | [4open hashbang](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/) | ⭐ 根目录文件清单实取：`.chainlit/` `.env.example`(117B) `.gitignore`(79B) `Paper Experiment Resources/` `README.md`(5,230B) `app.py`(7,501B) `backend/` `chainlit.md`(761B) `chainlit_en-US.md`(761B) `output_example.py`(21,527B) `public/` `requirements.txt`(161B)。⭐ `backend/` 下 5 项：`single_prompt.py`(5,044B) · `simple_linear_smf/` · `event_driven_smf/` · `merged_simple_linear_smf/` · `merged_event_driven_smf/` · `resources/`。⭐ 核心方法码实取：`simple_linear_smf.py`(8,677B) `simple_linear_smf_transitions.py`(2,351B) `event_driven_smf.py`(12,795B) `event_driven_smf_transitions.py`(4,704B) `merged_simple_linear_smf.py`(9,723B)。⛔ **无 LICENSE（实测 HTTP 404）**、⛔ 无 git commit、⛔ 无 release、⛔ 无 DOI |
| ⭐ **数据集 / Benchmark** | ⭐ 🟢 | [Reference Solutions](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/Paper%20Experiment%20Resources/Reference%20Solutions) | ⭐⭐ **8 个系统 × (`.txt` 描述 + `.png` 参考状态机) = 16 文件，逐个实取确认**：`bread-maker`(2,424B/95,975B) `chess-clock`(2,231B/83,744B) `dishwasher`(1,785B/55,870B) `printer`(2,045B/63,536B) `spa-manager`(1,958B/86,991B) `ssc7`(4,952B/220,549B) `thermomix`(2,684B/90,211B) `wumple`(3,407B/292,224B)。⭐ 另有 `backend/resources/state_machine_descriptions.py`(20,997B)。⚠️ **ground truth 是 `.png` 图片，⛔ 不是机器可读的状态机** —— ⛔ 见下方评级说明 |
| ⭐ **实验结果细则** | ⭐ 🟢 | [F1 workbook](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/Paper%20Experiment%20Resources/Final%20Detailed%20F1-Scores.xlsx) | ⭐⭐ **本轮已实际下载并解析**：58,116 bytes，⭐ SHA-256 `fe3cb7e44820a1e73dcdc71f8d5218d19c0f75203544aea47d646afacf2a4bbf`。⭐ 5 个 sheet：`SinglePrompt` `StructureDriven` `EventDriven` `Hybrid` `Averages`。⭐ 逐系统逐分量 TP/FN/FP/P/R/F + image reference。⭐⭐ **本卡 §C.6 / §C.7 / §C.9 / §C.10 的全部自算数字出自它** |
| ⭐ **prompt 是否公开** | ⭐⭐ 🟢 | [`backend/resources/prompts/`](https://anonymous.4open.science/#!/r/llm_state_machine_modeling/backend/resources/prompts) | ⭐⭐ **完全公开，逐文件实取**。⭐ `simple_linear_smf/` **7 个**：`StateEventSearchAction.txt`(7,498B) `ParallelRegionSearchAction.txt`(10,048B) `TransitionsGuardsSearchAction.txt`(11,873B) `ActionSearchAction.txt`(11,943B) `HierarchicalStateSearchAction.txt`(12,808B) `HistoryStateSearchAction.txt`(13,976B) `FinalSanityCheckAction.txt`(1,043B)。⭐ `event_driven_smf/` **9 个 + `legacy_prompts/`**：`SystemNameSearch.txt`(3,976B) `StateSearch.txt`(3,981B) `InitialStateSearch.txt`(4,342B) `EventSearch.txt`(4,766B) `AssociateEventsWithStates.txt`(5,045B) `CreateTransitions.txt`(5,577B) `CreateHierarchicalState.txt`(7,134B) `HierarchicalInitialStateSearch.txt`(3,266B) `HistoryState.txt`(7,659B)。⭐ 另有 `Prompts for event driven SMF.txt`(7,611B) 与 3 份 n-shot 例子：`n_shot_examples_single_prompt.py`(12,669B) `n_shot_examples_simple_linear.py`(24,251B) `n_shot_examples_event_driven.py`(19,927B)。⭐⭐ **本卡 §B3 / §B4 引的 prompt 逐字片段全部出自实取全文** |
| Artifact / 复现包 | ⚠️ 🟡 | [ZIP](https://anonymous.4open.science/api/repo/llm_state_machine_modeling/zip) | ⭐ 实测 **HTTP 200**，`application/zip`，**3,357,298 bytes**。⛔ **降为 🟡 的理由见下** |
| ⭐ 生成产物（逐样本输出） | ⚠️ 🟠 | `Paper Experiment Resources/Final {Single Prompt, Structure-Driven, Event-Driven, Hybrid}/` | ⭐ 4 个目录确认存在，⭐ 按 GPT-4o / Claude 分存生成状态机**图片**。⛔⛔ **只有渲染后的 `.png`，⛔ 没有 LLM 的 raw output、⛔ 没有 token usage、⛔ 没有 API 元数据。** ⚠️ ⭐ **后果：§C.7 那次整格全崩无法从 artifact 复盘** |
| 依赖清单 | ⭐ 🟢 | `requirements.txt`(161B) | ⭐ 关键项：`chainlit==1.2.0` `openai==1.35.7` `sherpa-ai==0.4.0` `pydantic==2.9.2` `mermaid-py` `aisuite` `anthropic` `groq` `vertexai` `ecologits` `graphviz`。⭐ `.env.example` 只列变量名，⛔ 未泄漏 key |
| ⭐ Umple 工具链 | ⭐ 🟢 | `backend/resources/umple.jar` | ⭐ 3,134,073 bytes 实取确认。⚠️ **用途原文未提供**（⛔ 见 §B7） |
| ⛔ **归档 DOI** | ⛔ ⚪ | — | ⛔⛔ **无 Zenodo / OSF / figshare / 任何归档 DOI。** ⭐ 唯一 DOI 是 arXiv 自己的 `10.48550/arXiv.2604.00275` |
| ⛔ **license** | ⛔ ⚪ | — | ⛔ 实测 `/file/LICENSE` **HTTP 404** |

### D.1 ⚠️⚠️ 为什么复现包判 🟡 而不是 🟢 —— ⭐ 三条，⛔ 第 3 条是本轮新发现

1. ⛔ **匿名 artifact 没有 commit / release / DOI**，⛔ 无法 pin 版本。
2. ⛔ **无 license**（实测 404），⛔ 复用授权不明。
3. ⭐⭐ **⛔ 本轮实测到它在变 —— ⛔ 而且是静默变的。** ⭐ 与本仓库 2026-06-10 的记录对拍：

| 文件 | 2026-06-10 记录 | ⭐ 2026-08-13 实测 | 判定 |
| :-- | --: | --: | :-- |
| `README.md` | 5,079 bytes | ⛔ **5,230 bytes** | ⛔ **已改（+151B）** |
| `app.py` | 7,417 bytes | ⛔ **7,501 bytes** | ⛔ **已改（+84B）** |
| `Final Detailed F1-Scores.xlsx` | 58,116 bytes · SHA-256 `fe3cb7e4…4bbf` | ⭐ 58,116 bytes · SHA-256 `fe3cb7e4…4bbf` | ⭐ **未变（逐字节相同）** |
| ZIP 整包 | 3,357,298 bytes | ⭐ 3,357,298 bytes | ⚠️ 同尺寸（⛔ 但 ZIP 尺寸不是可靠锚点） |

⭐⭐ **结论**：⛔ **代码侧在动，结果侧没动。** ⭐ 这对我们是**好消息中的坏消息**：⭐ 好在**本卡引用的全部数字来自那份未变的 workbook**（⭐ SHA-256 双次一致），⛔ 坏在**代码与论文的对应关系已经不可靠** —— ⛔ 我从源码里数出的「8 步 / 12 步」是**今天这一版**的，⛔ 无法证明它等于跑实验那一版。⛔ **§B1.5 的阶段数必须带这条限定引用。**

⭐⭐ **行动建议（⛔ 给 M1 / N1b）**：⭐ **现在就冻结**，⭐ 并按逐文件 hash 存清单（⛔ 不要只存 ZIP 整包 hash，⛔ 因为归档元数据会让整包 hash 漂）。⚠️ ⭐ 本轮已见到该平台的匿名仓库**会过期**（⭐ 本批另一个入口返回 `410 repository_expired`），⛔ 本仓库这一个今天还活着，⛔ 但没有任何保证。

### D.2 ⚠️ 数据集判 🟢 但有一条重要限定

⛔ **ground truth 是 `.png` 图片，⛔ 不是机器可读的状态机。** ⭐ 后果有两层：

1. ⛔ **想复用这 8 个 pair 做我们的对照，必须先人工把 8 张图转成机器可读形式** —— ⭐ 这是真实的人工成本，⛔ 不是「下载即用」。
2. ⛔⛔ **它也解释了为什么本篇的判定只能靠人**：⛔ ground truth 本身不可机械求值，⛔ 所以**自动评测在这个数据集上物理上做不到**。⭐ 论文那句 `"no existing evaluators are available"` 有一半原因在这里。

⭐ **对比我们的处境**：⭐ 我们的 54 pair 是 **pyfcstm DSL**，⭐ 机器可读、可求值、可求解 —— ⭐⭐ **这是我们相对本篇一个结构性的、而非程度性的优势**，⛔ 且它是我们能做 `hit@k` 的前提。

---

## E. 对 M1 的意义

### 1. ⭐ 可取之处（⛔ 具体到可搬的设计决定）

| # | 可搬的东西 | 为什么 |
| :-: | :-- | :-- |
| **1** | ⭐⭐ **「保住一份完整草稿，再逐分量细化」这个形状（Hybrid）** | ⭐ 它是全实验对弱模型最有效的策略（+11.3 pp，⚙️ 修正口径 +18.1 pp），⭐ 7 个分量里 6 个最优，⭐ 而且**它不需要任何裁决者**。⭐⭐ **这条对我们的价值是「省」而不是「增」**：⛔ 我们那 79% 的修订 token 里，若有一部分买的其实是「上下文完整性」，⭐ 那么用「注入一份完整草稿」这种**零裁决成本**的方式可能拿到同样的东西 |
| **2** | ⭐ **样例泄漏防护写成硬纪律** | ⭐ 逐字 `"If a particular state machine is used as test input, it is excluded from the examples shown to the LLM"`。⭐ 我们的 few-shot worked example 应当有一条同等明确、同等可被检查的纪律陈述 |
| **3** | ⭐⭐ **把最差的数字写进摘要** | ⭐ 他们把 `actions F1 = 0.00` 放进 abstract。⭐⭐ **我们的 −15.82pp 应当照这个规格处理** |
| **4** | ⭐ **依赖闭包式的严格判据 + 明写它压低了绝对值** | ⭐ state 错 → 挂它的 transition 自动 FP → 挂该 transition 的 guard/action 自动 FP，⭐ 并在 threats 里说明这压低了数字但提高了评分者间一致性。⭐ 这个「先说清判据严格性，再说清它的代价」的写法可以直接抄 |
| **5** | ⭐ **刻意把基线做强并说出来** | ⭐ 基线用 3-shot、被提出的框架用 2-shot，⭐ 动机逐字 `"aiming to improve upon the baseline accuracy"`。⭐ 这让「基线赢了」这个结论更可信而不是更可疑 |

### 2. ⛔ 不可取 / 陷阱（⭐ 尤其：它踩了我们踩过的哪些坑）

| # | 坑 | 与我们的对应 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **两个 LLM 自评步骤，各自都在自己唯一的职责上失效** | ⭐⭐ **这是本卡对我们最直接的一条旁证。** ⛔ Event-Driven 的 `FilterTransitions` 专为压 FP 而设，⛔ 结果 precision 0.2038（⛔ 比无过滤基线低 **0.59**）；⛔ Structure-Driven 的 `FinalSanityCheck` 只准加不准删，⛔ 结果 precision 相对基线 −0.0568。⭐ **我们 v46 的两个 LLM 自评 reviewer 是零收益 —— ⭐ 本篇给出两个「负收益」的外部实例。** ⛔ **合起来支持同一条设计原则：LLM 自评不该被放在裁决位。** |
| **2** | ⛔⛔ **有 sound-ish oracle 却不接进裁决路径** | ⛔ `umple.jar` 3.1 MB 就在仓库里，⛔ 单提示输出恰好是 Umple 代码，⛔ 而论文没有任何一处把编译结果当反馈/门。⭐⭐ **这与我们「pyfcstm 在求值端而非裁决端」是同一个拓扑毛病** —— ⛔ 差别是他们连求值都没接。⭐ **M1 第二条设计原则（把裁决者换成 sound oracle）在本篇这里得到的是反面教材式的支持** |
| **3** | ⛔ **整格失败被静默吞掉、且不在正文出现** | ⛔ §C.7：最大的系统在基线上整格零产出（0 TP / 0 FP / 95 FN），⛔ P 未定义 → 空格 → 跨系统平均时被跳过 → **该格的分母从 8 变成 7**，⛔ 而论文一个字没提。⭐⭐ **这正是仓库 §10「崩掉的格等于该样本消失，⛔ 而最容易崩的是最难的样本」的外部实例。** ⭐ 我们的降级落盘 + eligibility filter 纪律是对的，⛔ 本篇是不这么做的代价 |
| **4** | ⛔ **单次运行 + 用「样例间平均」冒充「运行间稳定性」** | ⛔ 论文承认 temp 0.5 会让结果每次不同，⛔ 缓解手段却是 `"averaging the results of eight state machine examples"` —— ⛔ **降的是样例间方差，不是运行间方差。** ⭐ 我们的 3 轮 + `hit@1/@3/@all` 正是这件事的正解，⭐ **这条差别可以直接作为我们方法学上的一个优势陈述** |
| **5** | ⛔⛔ **一个策略一个评分者，而结论是跨策略比较** | ⛔ `A single author conducts the evaluation for a given designed approach` + ⛔ 零一致性数据。⛔ **策略间差异与评分者间差异不可分离。** ⭐ 我们的 574 位逐位判据虽然也是自评，⛔ 但至少是**同一套判据跨全部格**，⛔ 不是每条臂换个人 |
| **6** | ⛔ **prompt 里有纯激励性话术** | ⛔ `FinalSanityCheckAction.txt` 结尾三句夸模型的话，⛔ 零可执行内容。⭐ 检查我们自己的 prompt 有没有同类残留 |
| **7** | ⛔ **无 snapshot pin、无 license、无归档 DOI、artifact 静默漂移** | ⛔ 两个模型都只有别名；⛔ 代码侧文件已改（README +151B / app.py +84B）而结果未改。⭐ 我们要求 run record 记精确 `model_id` 的纪律，⛔ 在这里得到又一次背书 |

### 3. ⚠️ 与我们的关键差别（⛔ 为什么不能直接照搬）

| # | 差别 | 后果 |
| :-: | :-- | :-- |
| **1** | ⛔⛔ **任务不同：它做「生成」，我们做「缺陷检测」** | ⛔ 它的产物是状态机，我们的产物是**关于状态机的发现**。⛔ **它的所有指标（P/R/F1 对参考解）在我们这里没有对应物** —— ⛔ 我们没有「参考状态机」，我们有「期望缺陷台账」。⛔ **不得把它的 F1 与我们的 `hit@k` 并列。** |
| **2** | ⛔⛔ **模型代差：它用 GPT-4o / Claude 3.5 Sonnet（2024 年），我们用 `gpt-5.5` / `claude-opus-4-7`** | ⭐ 而本篇最强的结论恰恰是**分阶段的收益随模型变强而转负**。⚠️ ⭐ **按它的趋势外推，分阶段对我们这一代模型的净收益预期是负的或接近零**（⛔ I 级外推，⛔ 不是本篇结论）。⛔ **这条要慎用**：⛔ 它可以支持「简化流水线」的方向，⛔ 但不足以单独支撑该决定 |
| **3** | ⛔ **它的「闭合」闭的是产物成分，我们的闭合闭的是提问算子** | ⛔ 见 §B5。⛔⛔ **它不是「闭合词表 + LLM 自动选」的先例** —— ⛔ 它的步序是**硬编码**的，⛔ 模型没有任何选择动作。⛔ 我们那个组合的先例数在本篇这里 **+0** |
| **4** | ⛔ **ground truth 不可机械求值（`.png` 图）** | ⛔ 所以它**只能**人工判定，⛔ 也只能报单次数字。⭐ 我们的 pyfcstm DSL 语料是**结构性优势**，⭐ 它是 `hit@k` 与自动求值的前提。⛔ **反过来说：我们不能把它的 8 个 pair 直接拿来当对照数据，⛔ 得先人工转录 8 张图** |
| **5** | ⛔ **边界：它含 parallel regions 与 history states，我们不含** | ⭐ 但 §C.10 已实测：⭐ **限定到界内后所有结论符号不变、排序不变**。⭐ **所以这条差别不妨碍我们引用它的趋势结论**，⛔ 只妨碍我们引用它的**绝对数字** |
| **6** | ⛔ **样本量 8 vs 我们 54 pair × 2 模型 × 3 轮** | ⭐ 论文自陈 `"our dataset of eight examples is a limitation"` 且来自本科课程。⛔ **它的任何「策略 A 优于 B」都建立在 8 个单次样本上。** ⭐ 引用它时应当把它当作**方向性证据**，⛔ 不当作**效应量证据** |

### 4. ⭐⭐ 一条给 M1 的直接可执行建议

⭐ 本卡与 [`llm-guided-predicate-discovery`](./llm-guided-predicate-discovery.md) 那张卡合起来，⭐ 指向同一件事的两面：

- ⭐ 那篇（RunVS）：⭐ **裁决者是确定性的 → 白跑的轮次几乎免费**（每轮 0.004–0.672 s）。
- ⭐ 本篇：⭐⭐ **裁决者不存在 → 于是「专门用来压 FP 的 LLM 自评步骤」把 precision 压到了 0.20**，⛔ 而**完全不过滤的单提示基线 precision 是 0.79**。
- ⭐ 我们（v46）：⛔ **裁决者是 LLM 自评 → 零收益却吃 79% 的 token。**

⭐⭐ **三点连起来是一条单调的关系：裁决者的可靠性决定循环值不值得存在，⛔ 而 LLM 自评在这条曲线上处于「不但不值得、还可能有害」的一端。**

---

## F. ⛔ 存疑与未核项

1. ⚠️ **图 1 / 图 2 / 图 4 / 图 3 / 图 5 的内容无法从 `paper_content.txt` 读出** —— 已试过本地 `paper_content.txt` 全文与 `paper.pdf` 存在性确认，⛔ 结果：图是位图，文本提取只拿到图题。⭐ **代偿手段**：⭐ 阶段数改从 artifact 源码的 FSM 定义反推（§B1.5），⛔ **但那是今天这一版代码，⛔ 不能证明等于跑实验那一版**（⭐ 因为 artifact 已被实测到在漂移，见 §D.1）。⭐ 若阶段数要进对照表，建议标「据 artifact 源码，2026-08-13 版」。
2. ⛔⛔ **`FinalSanityCheck` 与 `FilterTransitions` 两个自评步骤在论文正文中完全没有出现** —— 已试过 grep `paper_content.txt` 全文，⛔ `sanity` / `filter` 零命中。⭐ 所以 §B4 的两条旁证是「**论文数字 + 公开源码**」拼出来的，⛔ **不是论文自己的论证**。⚠️ **引用时必须这样说明**，⛔ 不得写成「论文报告了 LLM 自评过滤器降低 precision」——⛔ 论文没报，⛔ 论文甚至没提这个步骤存在。
3. ⛔⛔ **没有 filter / sanity-check 的消融对照** —— ⛔ 因此「LLM 自评过滤器导致 precision 崩」**无法被证成因果**。⭐ 能证成的只有更弱的一条：**加了专用 FP 过滤器的策略，precision 是四条里最差的，⛔ 差到 0.20**。⛔ **不要越过这条线。**
4. ⚠️ **§C.7 那次整格全崩的机制原因不明** —— 已试过：⛔ 查 artifact 的 `Final Single Prompt/` 目录（⭐ 只有 `.png`，⛔ 无 raw output）；⛔ grep 论文全文 `W-UMPLE`（⭐ 只在图例与数据集列表出现）。⭐ 1500 token 上限是**我方推测（I）**，⛔ 未证实。⛔ 其它可能：API 报错、格式不合规被判全 FN、人工评分时判定无可评内容。
5. ⚠️ **`umple.jar` 的实际用途原文未提供** —— 已试过 grep 论文全文 `Umple`（⭐ 只作为输出语言与引用 [15] 出现，⛔ 从未作为校验器）。⭐ 「用于渲染 `.png`」是**我方推测（I）**。⛔ 若要断言「他们有编译器但没用它做校验」，⭐ 应当再读 `backend/resources/util.py`(37,085B) 确认 —— ⛔ **本轮未读该文件。**
6. ⚠️ **`Claude 3.5 Sonnet` 属于 reasoning LLM 这个归类，我方判为可疑（I）** —— ⛔ 本轮未做独立核证（⛔ 未查 Anthropic 官方文档是否声明其具备独立推理阶段）。⭐ 若要在报告里使用「本篇的 reasoning/non-reasoning 轴实为强弱轴」这个改写，⛔ **应先去 [`llm_model_landscape/03-claude-models.md`](../../../../../llm_model_landscape/03-claude-models.md) 核 Claude 3.5 Sonnet 的定位与两个版本日期。**
7. ⚠️ **两个模型都无 snapshot 日期，Claude 3.5 Sonnet 有 2024-06 / 2024-10 两版，无法判断用哪个** —— ⛔ 原文未提供，⛔ artifact 的 `.env.example` 只有变量名。⛔ 复现时这是硬缺口。
8. ⚠️ **Structure-Driven 的第 8 步（sanity check）是否真的在跑实验时启用，未独立确认** —— ⭐ 已从 `simple_linear_smf_transitions.py` 的 `transitions` 列表确认它被列入（⭐ 列表末项就是 `sanity_check`），⛔ 但未读 `simple_linear_smf.py`(8,677B) 确认该列表被无条件加载。
9. ⚠️ **`merged_event_driven_smf/` 这一支的用途未确认** —— ⭐ 目录存在（实取确认），⛔ 但论文只报了 `Hybrid = Single-Prompt + Structure-Driven`（⭐ 逐字：`"we combine the Single-Prompt Baseline and the Structure-Driven SMF, because the Structure-Driven SMF clearly outperforms the Event-Driven SMF"`）。⛔ 所以 `merged_event_driven_smf` 很可能是**未报告的第五条策略**，⛔ 本轮未核其内容。
10. ⚠️ **`ccf` 判 ⚪ 是按「预印本不适用」处理** —— ⛔ 本轮未检索该文是否已被某 venue 接收（⛔ 未查 DBLP / Crossref 该标题）。⭐ 若后续正式发表，`year` 与 `venue` 需回填。
11. ⭐ **界外 2 分量的自算 F1 有一个口径脆弱点** —— ⛔ 4 个系统的 parallel regions ground truth 为 0，⛔ 这些格在 workbook 里是 `N/A` 或 `-`；⛔ 我按「跳过缺格、缺格记 0」两种口径都算过（§C.10 只报 n=8 记 0 的那版）。⚠️ **界外那张表的数字比界内那张脆弱得多**，⛔ 因为它的有效分母小（⭐ 只有 11 + 8 = 19 个元素）。⛔ **不要用界外那张表做任何强断言。**
12. ⚠️ **本卡对 `paper_content.txt` 的依赖** —— ⭐ 该文件由 `tools/pdf_extractor.py` text 模式提取，⭐ 质量总体良好（⭐ 全部表格数字与 workbook 独立交叉一致，⭐ 这本身是一次强校验），⛔ 但**排版处有粘连**（例：`tofully automateUML`、`F 1-scores`）。⛔ 本卡引用的逐字片段已逐条人工顺过，⛔ 但不排除个别空格错位。
