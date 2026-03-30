# UPPAAL-SMC: Statistical Model Checking for Priced Timed Automata

- 问题一句话：经典 `UPPAAL` 的穷举式 symbolic verification 很难覆盖随机、代价和混杂行为，而 `UPPAAL` 也缺少一条统一的统计模型检查工具线。
- 方法一句话：论文为 `NPTA/PTA` 定义了自然的 stochastic semantics，让组件独立抽取 delay 并进行 race，再在此基础上提供 hypothesis testing、probability estimation/comparison、expected value 与 `WMTL<=` monitor-based 检查。
- 解决点一句话：它把 `UPPAAL-SMC` 从一组分散想法推进成可交互、可视化、可分布式扩展的正式工具分支。

## 论文定位

这篇论文在 `uppaal_tech/` 中最适合放在 `⚡ 改进与扩展`，但它同时带着很强的工具里程碑性质。与 [david11-statistical-model-checking-real-time](../david11-statistical-model-checking-real-time/) 和 [david11-smc-priced-timed-automata](../david11-smc-priced-timed-automata/) 相比，本文不只是再讲一个统计算法，而是开始系统展示：

1. `UPPAAL-SMC` 的随机语义是什么；
2. 用户能问哪些统计问题；
3. GUI / plot / distributed execution / monitor construction 怎样落地。

所以它是 `UPPAAL-SMC` 从“理论能力”走向“完整工具分支”的关键条目。

## 立足问题

传统 `UPPAAL` 的强项是 symbolic exhaustive verification，但它有非常清楚的边界：

1. 若模型带概率与随机性，经典 reachability / TCTL 不再够；
2. 若系统规模很大、行为太丰富，穷举搜索会很快失控；
3. 若用户关心的是概率、期望代价、性能分布或混杂系统的统计行为，那么单纯 yes/no model checking 并不回答真正的问题。

与此同时，real-time systems 里又确实不断出现这类需求：

1. 某性质在给定时间或代价界内满足的概率有多大；
2. 两个设计方案哪个更可能提前完成；
3. 某个系统平均要花多少能量、多少时间；
4. 混杂系统或 priced system 的行为是否还能以一种“足够自然”的随机语义来分析。

于是核心问题变成了：**如何在不放弃 timed automata 建模习惯的前提下，把随机与代价分析真正做进 `UPPAAL`。**

这件事的难点不止一个：

1. 单个组件的随机延迟怎么定义；
2. 多组件组合后，整体概率语义如何自然诱导出来；
3. 支持哪些统计查询；
4. 怎么把这些查询做成真正可用的工具，而不是命令行原型。

## 核心方法

这篇论文的方法主干可以拆成四层：先定义 `NPTA/PTA` 的随机语义，再把统计问题分成若干标准查询模式，然后通过 monitor PTA 支持更丰富的时序逻辑，最后用若干工程优化把它做成可用工具。

### 1. 给 `NPTA/PTA` 定义自然的 stochastic semantics

论文最核心的第一步，是给网络化 priced timed automata 定义随机语义。它没有要求用户给整个 product 手工指定复杂全局分布，而是采用更自然的局部生成机制：

1. 每个组件在当前状态独立抽取一个 delay；
2. 若 delay 有上界，用 uniform distribution；
3. 若可无限停留，则用 exponential distribution；
4. 组件之间进行 race，抽到最小 delay 的组件获胜并触发输出。

也就是说，系统的随机行为来自“组件各自独立抽时间，然后竞争谁先行动”。这一步非常漂亮，因为它让用户仍然按 timed automata 的局部组件视角建模，而全局复杂随机行为则由组合自动诱导。

论文特别强调，这种单组件语义虽然简单，但多个组件通过 message passing 组合后，可以自然产生非常复杂的 stochastic behavior。这是 `UPPAAL-SMC` 最吸引人的地方之一。

### 2. 把统计问题压成三类标准查询，再补 expected value

在随机语义建立后，论文把用户真正会问的问题分成几类。

第一类是 **hypothesis testing**。例如：

$$ \Pr[\text{bound}](\Diamond \varphi) \ge p $$

也就是“某性质在给定 bound 内满足的概率是否至少为阈值 `p`”。

第二类是 **probability estimation**。不再问是否超过某阈值，而是直接估计：

$$ \Pr[\text{bound}](\Diamond \varphi) $$

第三类是 **probability comparison**。比较两个事件或两个设计哪一个概率更大。

此外，工具还支持 **expected value** 查询，例如在若干 runs 上统计某个表达式的最小值、最大值或平均表现。这样 `UPPAAL-SMC` 就不再只是概率验证器，而是一个更广义的 stochastic performance analyzer。

### 3. 用成熟统计程序而不是“伪随机试一试”

本文并不是“跑几次 simulation 然后看个大概”。在统计算法层，它明确采用了：

1. Wald sequential hypothesis testing
2. Chernoff-Hoeffding 型概率估计界
3. 扩展 Wald testing 用于 probability comparison

这意味着工具输出的不是裸频率，而是带着显式错误概率和置信度的统计结论。也正因为如此，它能给出“yes/no + error bound”“估计区间”“对比结果”等更正式的答复。

### 4. 用 monitor PTA 支持完整 `WMTL<=`

如果只支持 reachability 概率，那 `UPPAAL-SMC` 的表达力还是有限。论文进一步说明，为了支持完整的 `WMTL<=`，工具会先把性质构造为 deterministic under- / over-approximation monitoring PTA，再把这些 monitors 与原模型并行组合。

也就是说，更复杂的时序性质并不是在模拟器外层硬编码，而是继续沿用 `UPPAAL` 一贯的 automata-based 思路：

1. 先把性质变成 automaton；
2. 再并到系统模型里；
3. 最后仍然跑统一的 SMC 算法。

这一步让逻辑表达力和底层随机语义保持在同一技术框架里，而不是两张皮。

### 5. 图形化输出不是附属品，而是工作流的一部分

论文非常重视 GUI / plotting。工具不只给文字答案，还支持：

1. frequency histogram
2. probability density / cumulative distribution
3. value monitoring
4. 多组统计结果叠加比较

这说明作者很清楚 `SMC` 与经典 model checking 不同：用户常常不是想要一个终结性证明，而是想理解系统的概率分布、时间分布和成本分布。图形化不是锦上添花，而是主工作流的一部分。

### 6. 分布式执行与若干性能优化把它推向可用规模

为了让 `SMC` 真能跑大一些的模型，论文还讨论了若干非常实用的工程手段：

1. distributed SMC
2. query / bound detection
3. early termination
4. delay reuse
5. 依赖分析减少无谓重抽样

特别是 delay reuse 的思路很像 `UPPAAL` 一贯的工程风格：一旦系统某些选择在当前步没有被其他同步、clock rate、guard 或 update 破坏，就复用上一步已采样的结果，避免不必要的重新抽样。

这说明 `UPPAAL-SMC` 不是“把统计学接上去就完了”，而是认真对待了 simulation-heavy workload 的性能瓶颈。

## 解决了什么问题

这篇论文最重要的贡献，是让 `UPPAAL` 正式长出一条 stochastic / statistical / priced 的工具主线。

第一，它给网络化 PTA 定义了一套相当自然、建模成本低的随机语义。用户不需要自己全局拼概率空间，局部组件 race 就足够诱导复杂全局行为。

第二，它把 `SMC` 真正做成了一个统一工具，而不是零散的单算法集合。概率检验、估计、比较、期望值和 `WMTL<=` 都能进同一工作流。

第三，它显著拓宽了 `UPPAAL` 可处理的问题类型：从“是否可达 / 是否满足”扩展到“满足的概率多大 / 平均代价多少 / 分布长什么样”。

第四，它为后续 `distributed SMC`、`SHS`、`Stratego`、GPU-SMC 等方向提供了稳固底座。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [david11-statistical-model-checking-real-time](../david11-statistical-model-checking-real-time/)
2. [david11-smc-priced-timed-automata](../david11-smc-priced-timed-automata/)
3. [bulychev11-distributed-parametric-statistical-model-checking](../bulychev11-distributed-parametric-statistical-model-checking/)

前者给出概念与早期算法，本文则把它们整合成正式的 `UPPAAL-SMC` 分支呈现。

### 它往后影响了谁

它往后明显影响：

1. [david12-statistical-model-checking-stochastic-hybrid-systems](../david12-statistical-model-checking-stochastic-hybrid-systems/)
2. [david15-uppaal-smc-tutorial](../david15-uppaal-smc-tutorial/)
3. [david15-uppaal-stratego](../david15-uppaal-stratego/)
4. [muniz24-gpu-accelerating-smc-extended-timed-automata](../muniz24-gpu-accelerating-smc-extended-timed-automata/)

### 它更靠近哪条主线

它最靠近：

1. `SMC`
2. stochastic / priced timed systems
3. monitor-based temporal property checking

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 随机语义、查询类型、monitor PTA 和工程优化都讲得比较清楚，已经足以让人理解 `UPPAAL-SMC` 是如何运作的；不过某些底层实现仍然更像 tool-paper 粒度，而不是完整内部设计文档。
2. **实现可获取程度**
   - 更适合评为 `🟧 仅可执行/可使用版本可得`。
   - `UPPAAL-SMC` 的工具线、教程与下载入口都非常明确，但当前没有找到与本文版本精确对应的开源主引擎源码仓库。
3. **材料价值**
   - 它非常适合作为 `SMC` 主线的正式工具入口，尤其适合拿来理解从语义到 query 到 GUI 的完整闭环。

## 对本研究的启发

这篇论文对当前博士研究有三点很直接的启发。

第一，**随机语义不一定要从全局直接规定，可以由局部组件规则自动诱导出来**。这对后续若要给状态机模型引入环境不确定性、噪声或行为分布，非常有参考价值。

第二，统计查询的分类方式很值得借鉴。概率阈值判断、概率估计、方案比较、期望值分析，本质上对应的是不同研究问题，不能混成一个“随机验证”标签。

第三，工具层的 plot / monitor / distributed execution 说明：若未来你的验证闭环要真的可用，输出不应该只是一句“通过 / 不通过”，还应包括可观察、可解释的分布与性能画像。
