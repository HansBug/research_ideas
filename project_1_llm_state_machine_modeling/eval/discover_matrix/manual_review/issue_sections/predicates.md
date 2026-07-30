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

| 缺口族 | 条数 | 是真缺口 | 说明 |
| --- | ---: | :-: | --- |
| `deliberate_refusal` | **1** | ✗ | 词表刻意设防（非缺口） |
| `overspecification_judgement` | **5** | ✓ | 缺『过度指定』判据：无法问某元素有无需求依据 |
| `minimality` | **7** | ✓ | 缺最小性谓词：无法表达『不应多出』 |
| `triggerless_edge` | **2** | ✓ | 缺『无触发 / completion 边存在』谓词 |
| `action_content` | **10** | ✓ | 缺动作内容 / 动作计数谓词 |
| `synthetic_nodes` | **1** | ✓ | 合成节点污染 cardinality，计数命题不可信 |
| `initial_edge` | **2** | ✓ | 初始边族被 initial_target 的拒答语义封死 |
| `existential` | **1** | ✓ | S 族无存在量词，『壳缺失』只能照搬参考名 |
| `exact_occupancy` | **1** | ✓ | 缺 exact occupancy 与隔离单个多余元素的计数口径 |
| **合计** | **30** | | |

其中 **29 条是真词表缺口**，1 条是词表**刻意设防**——`occupancy_after` 的 horizon 自检与 `edge_declared` 的 caveat 共同封死了「把良性多跳记成缺陷」这条路，那是设计上的护栏，不是漏洞，因此不计入缺口。

**最大的缺口落在动作 $A$ 上：`action_content` 族 10 条，占 30 条的三分之一。**这一族的形态是「非数值的动作或输出信号义务」——`Start Timer`、`Stop Timer`、`Display / Update Cooking Time` 这类。它在 19 谓词里无处落脚：effect 通道（`effect_declared` / `variable_declared` / `variable_delta_after`）要求「变量 + 符号」，而该通道在本语料恒为空；action 通道（`action_declared`）只看相位（entry/exit）不看动作名；更麻烦的是 NL 并未指定动作该挂在状态还是迁移上，**两种都正确的渲染会让同一条断言给出相反答案**。$A$ 是 $M = (S, E, V, Tr, A)$ 的一个分量，却是当前谓词面覆盖最弱的一个——这是本轮最值得记下的词表结论。

**另一个必须写明的口径依赖。** `overspecification_judgement` 族（5 条，均为 NL02 钳夹类）之所以写不出断言，是因为 19 谓词只能问「声明了什么 / 运行时会怎样」，问不了「这个元素有无需求依据」；把 `extra` 写成正面断言必然退化成闭世界禁令。本轮复跑另有一个新发现：P 族的 `invariant(scope=S, condition=active(S))` 在这几个 case 上**确实返回 `False`**（此前有害性判定没试过 P 族）。也就是说，**若允许「该状态必须保持吸收」这类闭世界命题，这 5 条即可表述**。是否允许属于分层政策，不属于谓词能力——这条边界必须由人来定，不能由脚本默认。

复跑逐条结果（153 行，含断言原文、复跑值、与批次自报值的比对）：[predcov_verified_assertions.json](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_verified_assertions-json) ｜ 五批原始判定 [批1](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result1-json)、[批2](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result2-json)、[批3](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result3-json)、[批4](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result4-json)、[批5](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_result5-json) ｜ 方法与已知坑 [predcov_BRIEF.md](https://gist.github.com/HansBug/daa977482df22711e8e0d00fc80c406c#file-predcov_brief-md) ｜ 复跑脚本 [verify_assertions.py](../verify_assertions.py)
