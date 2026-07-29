# expected issue 分母的已知缺口

本文件记录 evaluator-side ground truth（Issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的 47 条 E1）**系统性不覆盖**哪些问题类，以及每处缺口是"问题定义边界"还是"待补欠账"。它是论文 threats to validity 一节的直接材料。

判定命中的原则见 [HIT_CRITERION.md](./HIT_CRITERION.md)。原论文逐 case 的问题记录见
[paper_reported_problems.json](./paper_reported_problems.json)（由 [extract_paper_problems.py](./extract_paper_problems.py) 从论文公开 workbook 提取，60/60 对齐）。

---

## 1. 外部锚点：原论文自己记录了什么

原论文（Wang et al. 2025, Internetware，DOI 10.1145/3755881.3755926）的公开 workbook
`Experiment Results.xlsx` / sheet `STM Results` 对 60 个生成结果逐 case 记录三类问题，
各带 `Resolved` 标记。它是唯一可用的外部对照，因为它的判定方式与我们不同：
**它对着作者重建的参考模型算 grammar-point F1**，而我们**仅凭 NL 建立正向命题、禁止使用参考模型**。

语义 / 需求一致性类共 50 条，散布 41 个 case：

| 论文语义类目 | 条数 | 涉及 case | 台帐有 E1 的 case | 覆盖率 |
| --- | ---: | ---: | ---: | ---: |
| **missing region（缺正交区）** | **18** | 18 | 7 | **39%** |
| composite state 误用 | 8 | 8 | 3 | 38% |
| **missing state / transition** | **7** | 7 | **1** | **14%** |
| interaction error | 7 | 7 | 5 | 71% |
| missing final state | 5 | 5 | 2 | 40% |
| pseudostate（junction / fork / join） | 5 | 4 | 4 | 100% |

四象限交叉：

| | 论文有语义错 | 论文无语义错 |
| --- | ---: | ---: |
| 台帐有 E1 | 17 | 12 |
| 台帐无 E1 | 24 | 7 |

---

## 2. 缺口一：正交并发（问题定义边界，不补）

**裁决：不补进 expected issue，作为 limitation 如实陈述。**

原论文的最大语义问题类是 `missing regions`（18 条 / 18 个 case，论文 Table 9 记 20 条）。
台帐对其覆盖率仅 39%，其余 11 个 case 被排除，排除类型为
`E2a/pump_hierarchy_or_concurrency_ambiguity`、`E3/uav_concurrency_or_textual_effect_boundary`、
`E2c/orthogonal_region_assertion_missing`。

**这不是方法未能检出，是本轮评测的边界**：本轮 Discover 实验的断言对象是
FSM / HSM / EFSM 类状态机模型，其形式定义中**不含正交区与并发语义**；同理，时间约束类
（台帐 taxonomy 的 `TO`，实际 0 条）也不在本轮的断言对象内。语料侧有对应边界：R4.5 表示层的
`r4_5_boundary` 明写 `do not infer guard/effect/timing/concurrency`，
`PlantUML concurrent region 29/29` 只保留结构与顺序、不声称已实现正交并发执行。

**论文中应如实写明**：分母系统性排除了基线论文最大的一类语义问题（18/50 = 36% 的语义条目），
原因是该类不在本轮评测的断言对象内，而非方法未能检出。不得把该类的缺席呈现为
"这些模型没有此类问题"。§2.1 给出它与总纲创新点的关系。

### 2.1 与总纲创新点的关系（已裁定）

[TARGET.md](../../../TARGET.md) 第 238 行的创新点 1 写「系统性解决层次化状态、**并发行为**和
时间属性的建模难题」。这与本节的 limitation **不冲突**，因为两者说的是不同的东西：

| | 对象 | 陈述 |
| --- | --- | --- |
| 总纲创新点 | **建模方法的能力** | 方法面向含层次、并发、时间的控制系统状态机 |
| 本节 limitation | **本轮 effectiveness 实验 oracle 的覆盖范围** | 这批 60 例的 expected issue 分母不含并发与时间类可判定命题 |

分母不含它们有两条独立于方法能力的原因：

1. **语料的表示层不推断并发与时间**。R4.5 的 `r4_5_boundary` 明写
   `do not infer guard/effect/timing/concurrency`；`PlantUML concurrent region 29/29`
   只保留结构与顺序，不声称已实现正交并发执行。所以即使方法能建模并发，**这批 FCSTM 制品里
   没有可供断言的并发语义**。
2. **oracle 无法在归因安全的前提下形成并发/时间命题**。台帐门槛要求逐 issue 绑定
   attribution-safe source trace entry；并发相关的候选一律落在 `E2a/E2c/E3`
   （`pump_hierarchy_or_concurrency_ambiguity`、`orthogonal_region_assertion_missing`、
   `uav_concurrency_or_textual_effect_boundary`），时间类落在
   `E2c/camera_timing_adapter_missing`。

**论文中的正确写法**：把它写成**评测边界**而非方法边界——"本次 effectiveness 实验的
expected issue 集合不含正交并发与时间约束类命题，因为该批语料的表示层按设计不推断这两类语义，
oracle 亦无法在归因安全前提下形成对应命题；方法本身对这两类的支持不在本实验的度量范围内。"

不要写成"方法不支持并发"，也不要写成"这些模型没有并发问题"——后者与基线论文的记录直接矛盾
（`missing regions` 是其最大语义类）。

---

## 3. 缺口二：over-specification（整类无槽位）

台帐的 8 类 taxonomy（`SH` / `IT` / `TR` / `GC` / `UA` / `EA` / `TO` / `DA`）**没有任何一类承担
"凭空多出的状态或迁移"**，而 `UA` 明确拒绝该角色（"单纯 NL 未提及不得归入 UA"）。

原论文**有**这一类：Table 10 的一级分类含 `Over-specification`，在 ACT 图上占 33%（9 例
`Extra ActivityNode`）。实例：`0001` 的作者 PlantUML 第 14 行
`OperationalState --> ClampingLoseState : Transition to Clamping Lose State`，
而 `ClampingLoseState` 在该 case 的 NL 里从未出现。

**这是真缺口，不是问题定义边界**——多出的状态属于 FSM/HSM/EFSM 完全能表达的范围。
处理方式待裁决：新增一个 `OS` 类做敏感性分析，或在 threats 中明确列为整类漏判。

---

## 4. 缺口三：7 个 case 连候选都未记录

以下 7 个 case 论文记录了具体语义问题，台帐既无 E1、`observations` 亦为空，
且全部标 `no_supported_finding`：

| case | LLM | 论文记录的语义问题 |
| --- | --- | --- |
| `0003` | GPT-4o | missing final state |
| `0012` | GPT-4 | missing final state |
| `0052` | Claude | missing final state |
| `0013` | GPT-4 | use region |
| `0022` | Llama | missing composite state |
| `0032` | Kimi | missing composite state |
| `0027` | Llama | missing regions |

`0003` / `0012` / `0052` 是同一 NL（HSUV）的三个不同 LLM，论文对三者都记 `missing final state`。

**`no_supported_finding` 这个 status 的措辞有风险**：它会被读成"该模型无问题"，而实际含义是
"仅凭 NL 在严格蕴含门槛下形成不了可执行命题"。这 7 个至少应改为 `candidate_only` 并补记候选与排除理由。

其中 `0013` / `0027` 属 §2 的正交并发缺口；`0003` / `0012` / `0052` 的 `missing final state`
与 `0022` / `0032` 的 `missing composite state` **不属于任何已声明的问题定义边界**，是待补欠账。

**一个可能的机会点**：台帐建立于当前 19 谓词体系之前，其"正向断言可执行"门槛是对
`transition_exists` / `transitions` / `states` / `initial_child` / `effect_deltas` / `path`
六个底层原语判定的。当前谓词表中的 `terminates`（直接判定某配置能否终止）与
`cardinality` / `containment` 可能使部分当年判不了的命题变得可判——**"终态存在"与"能终止"
不是一回事**，一个模型可以声明 `FinalState` 却到不了它。是否据此补充，见对应的裁决记录。

---

## 5. 分母的构成偏差（不是缺口，但必须披露）

E1 条数与 **NL 的具体程度**强相关，与 NL 长度无关：

| E1 条数 | 领域 | NL 词数 |
| ---: | --- | ---: |
| 11 | Digital camera | 282 |
| 10 | high-level driving module | **71** |
| 7 | autonomous mode | 434 |
| 0 | **base brake subsystem** | 80 |
| 0 | **HSUV** | 65 |

两个 NL 最含糊的领域在**全部 6 个 LLM 上都是 0 条**。原论文的模板规则第三条明写
"Requirements must avoid explicitly stating the number of elements or inter-element relations"，
这直接压低了可形成的命题数。

同源的一个偏差是**可绑定性**：命题需要一个可绑定的状态名才能实例化。`0020` 有
`AutoFinalState` 这个名字故计 E1，`0050` 是同一缺陷但没有该状态名故计 E0。后果是
"模型越含糊、可判定缺陷越少"。

**因此 per-LLM 的 E1 矩阵（Claude 1 条 vs Kimi 13 条，13 倍）不得作为缺陷率比较呈现**，
只能作为"可判定缺陷数"呈现，并与原论文 F1 的跨度（Claude 80.27 vs Kimi 66.68，1.2 倍）并列对照。

---

## 6. 建议的分母表述

不要写"60 个模型中共有 47 个缺陷"。如实写：

> 我们在 evaluator 侧构建了 N 条 expected issue，其定义是：**能仅凭 NL 文本形成正向命题、
> 被作者源 PlantUML 直接矛盾、且在当前谓词面上可执行判定的作者源缺陷**。它不是 60 个模型
> 缺陷的完备集，也不是缺陷率的无偏估计。已知系统性排除：正交并发与时间约束（问题定义
> 边界）、over-specification（整类无槽位）；已知构成偏差：NL 具体程度与状态名可绑定性。
