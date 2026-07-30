「能不能用现有 19 个封闭谓词把这条问题说出来」是独立复跑出来的，不采信批次自报的值：每条断言都在同一语料上重新求值一次，**只有返回 `False` 才计入可表述**。返回 `True` 说明断言不判别，返回 `None` 或抛异常说明无法判定——两者都不是缺陷证据。

| 复跑结论 | 条数 | 含义 |
| --- | ---: | --- |
| `captured` | **123** | 返回 `False`，缺陷可被现有谓词表述并捕获 |
| 自报不可表述 | 30 | 批次自己判为写不出，逐条给了缺口分析 |
| `not_captured` / `disputed` / `uses_non_closed` | 0 / 0 / 0 | 三项皆为 0：没有断言写错、没有与批次报告不一致、没有偷用 19 谓词之外的旧原语 |
| **合计** | **153** | |

**123 / 153 = 80% 可用现有谓词表述到位。**按承载谓词分布如下（同一条只记首个判别谓词）：

| 谓词 | 族 | 捕获条数 | 只能证存在性 |
| --- | :-: | ---: | :-: |
| `initial_target` | S | 21 |  |
| `state_declared` | S | 14 | ✓ |
| `containment` | S | 13 |  |
| `edge_declared` | S | 13 | ✓ |
| `reaches` | B | 9 |  |
| `terminates` | B | 8 |  |
| `event_consumed` | B | 7 |  |
| `occupancy_after` | B | 7 |  |
| `guard_distinguishable` | S | 6 |  |
| `event_declared` | S | 6 | ✓ |
| `action_declared` | S | 6 | ✓ |
| `cardinality` | S | 5 |  |
| `effect_declared` | S | 3 | ✓ |
| `persists_until` | P | 3 |  |
| `stays_in` | B | 2 |  |
| **合计** | | **123** | |

19 个谓词里有 **4 个一条都没用上**：`invariant`、`response_within`、`variable_declared`、`variable_delta_after`。这不代表它们无用，而是说明本轮 153 条问题的形态集中在结构与可达性上。

### 不可表述的 30 条：按缺口族归类

每条都由复核者先尝试写断言、失败后给出缺口分析，因此「不可表述」是尝试过的结论，不是没试。归类如下：

| 缺口族 | 主缺口 | 另被提及 | 是真缺口 | 说明 |
| --- | ---: | ---: | :-: | --- |
| `deliberate_refusal` | **1** | — | ✗ | 词表刻意设防（非缺口） |
| `minimality_no_provenance` | **12** | — | ✓ | 缺『不应多出』谓词：无法断言某元素没有需求依据、不该存在 |
| `action_content` | **8** | — | ✓ | 缺动作内容 / 动作计数谓词（非数值 effect、输出信号） |
| `guard_content` | **2** | — | ✓ | 缺『边必须携带区分条件 / 守卫非空』谓词 |
| `triggerless_edge` | **2** | — | ✓ | 缺『无触发 / completion 边存在』谓词 |
| `synthetic_nodes` | — | 2 | ✓ | 合成节点污染 cardinality，计数命题不可信 |
| `initial_edge` | **1** | 1 | ✓ | 初始边族被 initial_target 的拒答语义封死 |
| `false_false_source` | **1** | 1 | ✓ | 行为族对不可判定目标返回 False 而非拒答——会伪造缺陷 |
| `existential` | **1** | — | ✓ | S 族无存在量词，『壳缺失』只能照搬参考名 |
| `granularity` | **1** | — | ✓ | 缺『一个 NL 概念对应几个模型状态』的粒度谓词 |
| `exact_occupancy` | **1** | — | ✓ | 缺 exact occupancy 与隔离单个多余元素的计数口径 |
| **合计** | **30** | 4 | | |

其中 **29 条按真词表缺口计**，1 条（`0006`#4）不计入。**这条排除用的是一条窄规则，须写明**：不是因为该形态「良性」——30 条里有 15 条同属 `over_specification_benign`，其中 14 条照样计入缺口，所以良性本身不是判据。真正的理由是**谓词文档把这个形状明写为假阳性**：`edge_declared` 的 caveat 与 `occupancy_after` 的 horizon 自检共同封死了「把多出的一跳记成缺陷」这条路。需要同时承认该自检是**内容无关**的：只要更大的 `within_cycles` 也返回 True 它就拒答，无论那一跳有害还是无害——因此它在这里给出正确答案靠的是构造，不是对缺陷的判别。

**「30」是一个带政策条件的数，不是纯测量值——这一点必须写在表旁边。**[predcov_BRIEF.md](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_brief-md) 定的判据是纯机械的：在这个有缺陷的模型上实测返回 `False` 即算可表述。按该判据，`minimality_no_provenance` 里的 NL02 钳夹类**本不该留在「不可表述」里**——本轮复跑发现 P 族的 `invariant(scope=S, condition=active(S))` 在那几个 case 上**确实返回 `False`**（此前的有害性判定没试过 P 族），且有效负控：`0026` 的真吸收态返回 `True`、同模型有出边的状态返回 `False`，该形态并非恒假。它们仍被留在「不可表述」里，依据的是一条**未写进 BRIEF 的政策**：闭世界禁令（「该状态必须保持吸收」「不得声明该事件」）不算合法断言。这条政策若翻转，**至少 8 条会移出「不可表述」**（除 NL02 钳夹类，还有 `0002`#3、`0010`#7、`0043`#2 这类「沉默封闭」）。所以 30 应读作「在不采纳闭世界禁令的前提下不可表述的条数」。**这是分层政策问题，不是谓词能力问题，必须由人裁定。**

还有一处粒度限制：NL02 钳夹类的 5 条对应的其实是 **4 条 case 级断言**——`0041`#0 与 `0041`#1 是同一模型同一个 `ClampingState` 上的两条多余出边，写出来的表达式逐字相同，那一个 `False` 由两条 extra 共同造成、**无法互相隔离**。

**最大的缺口是「无法断言某元素不该存在」：`minimality_no_provenance` 族 12 条，占 30 条的 40%。**19 个谓词全是正面的存在性或正面的可达性命题，所以能问「模型有没有声明 X」「跑起来会不会到 Y」，问不了「X 有没有需求依据、是不是根本不该出现」——把 `extra` 写成正面断言必然退化成闭世界禁令。这 12 条**全部**是 `verdict = extra` 且 `stratum = over_specification_benign`，同一种形状、同一种拒绝理由。

**第二大缺口落在动作 $A$ 上：`action_content` 族 8 条（27%）。**形态是「非数值的动作或输出信号义务」——`Start Timer`、`Stop Timer`、`Display / Update Cooking Time` 这类。它在 19 谓词里无处落脚：effect 通道（`effect_declared` / `variable_declared` / `variable_delta_after`）要求「变量 + 符号」，而该通道在本语料恒为空（全库唯一被声明过的变量是 converter 的 `R45RouteToken`，非 route 变量声明为 0）；action 通道 `action_declared(state=..., phase=...)` **没有动作名参数**，只能证明「这个状态挂了某个动作」，证明不了「挂的是 `Start Timer`」。$A$ 是 $M = (S, E, V, Tr, A)$ 的一个分量，却只有一个只看相位的谓词覆盖它。

另需注明一处推断与观测的边界：NL 通常不规定动作该挂状态还是挂迁移，而 `action_declared` 只读状态侧字段、迁移承载的具名动作在 19 谓词里不可见，**因此原则上两种渲染会让同一条断言给出相反答案**。但这是从谓词签名与 NL 欠定推出的机制推断，不是观测结果：`0014`#1 确实出现过同一个 `Entry/Accelerate` 挪到初始边标签后断言翻面，但该 pair 的 NL 逐字点名了相位、迁移写法被判 `problem`；`0004`#5 是 NL 未指定相位的真实例，可作者的 entry + during 写法被判 `similar`。**「两种都正确的渲染同时出现并使断言翻面」目前尚无观测实例。**

复跑逐条结果（153 行，含断言原文、复跑值、与批次自报值的比对）：[predcov_verified_assertions.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_verified_assertions-json) ｜ 五批原始判定 [批1](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result1-json)、[批2](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result2-json)、[批3](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result3-json)、[批4](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result4-json)、[批5](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result5-json) ｜ 方法与已知坑 [predcov_BRIEF.md](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_brief-md) ｜ 复跑脚本 `project_1_llm_state_machine_modeling/eval/discover_matrix/verify_assertions.py`
