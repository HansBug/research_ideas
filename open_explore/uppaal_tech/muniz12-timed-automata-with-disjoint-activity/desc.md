# Timed Automata with Disjoint Activity

- 问题一句话：对时分复用这类周期系统，很多 timed automata 在每个周期内本来按先后分段活动，但普通并行组合仍然会制造大量无意义 interleaving。
- 方法一句话：定义 periodic cyclic timed automata、activity 与 sequentialisable 条件，再用 concatenation `\cdot` 和带 overclock 的 sequential composition `#` 把并行产品压成顺序化自动机。
- 解决点一句话：把这类系统在 `Uppaal` 中的验证复杂度从随组件数二次增长降到线性级。

## 论文定位

这篇论文属于 `⚡ 改进与扩展`，但它不是一般意义上的“再做一点状态削减”，而是在 timed automata 语义层面识别出一类特殊而很常见的系统结构：**组件虽然并行存在，但在每个周期内它们的真实动作区间几乎不重叠**。典型例子就是 TDMA、time-triggered architecture、无线传感器轮询协议等。

它和后面的 [muniz20-urgent-partial-order-reduction-extended-timed-automata](./../muniz20-urgent-partial-order-reduction-extended-timed-automata/) 有明显继承关系：

1. 本文抓的是“周期系统中的顺序活动窗口”；
2. 后者抓的是“零时间紧迫区间里的独立动作”。

两者都不是改 timed automata 的基本语义，而是在现有语义里识别某种常见结构，然后借此减少 `UPPAAL` 里必须探索的组合爆炸。

## 立足问题

作者面对的问题来自一类很典型的工业系统：多个组件在名义上并行运行，但由于通信协议或时间表约束，它们在每个周期内其实是轮流活跃的。例如第 `i` 个传感器只在第 `i` 个时隙里发送，别的时刻只是等待。

然而标准 timed automata 的并行组合仍会把这些组件全部放进 product 里。结果有两个代价：

1. 位置空间做笛卡尔积；
2. 在共享周期边界附近产生大量 interleaving 与边组合。

对这类系统来说，真正浪费的不是“组件太多”，而是**分析方法没看到它们的活动其实是错开的**。

作者因此瞄准了一个很具体的问题：若两个 timed automata 在每个周期内的 activity intervals 是严格分离的，那么是否能把它们的并行产品改写成一种更接近串行执行的结构，同时保持需要的验证性质不变。

注意，这里不能只做经验性“先跑 A 再跑 B”的简化。因为作者要保住的是：

1. reachability 性质；
2. leads-to 一类基于状态可达的验证目标；
3. 与 `UPPAAL` 一致的 timed semantics。

所以本文并不是在做 heuristic scheduling，而是在找一个**可证明正确的顺序化变换**。

## 核心方法

这篇论文的方法主线非常完整：先定义一类 periodic cyclic timed automata，再定义 activity 与 sequentialisable 条件，接着给出两层组合算子 `\cdot` 与 `#`，最后证明它们与原并行组合之间的 bisimulation / weak bisimulation 关系。

### 1. 先把“周期返回初始点”的 timed automata 形式化

作者先定义 periodic cyclic timed automata。直观上，这类 automaton 具有：

1. 初始位置会在每个周期反复被访问；
2. 周期长度固定为 `pt`；
3. 每个周期内存在唯一的“结束位置”再回到起点。

为了把这件事说清楚，论文定义了：

1. start configurations
2. restart configurations
3. final configurations

这些对象的作用是把“每一轮周期什么时候正式开始、什么时候即将结束”精确定义出来，而不是只靠直觉说“模型看起来像周期性的”。

### 2. 用 `Active(A)` 抽出 automaton 在时间轴上真正发生动作的点

接着，作者把一个 timed automaton 的活动点定义为：在某个 computation 中发生 action transition 的那些时间点集合 `Active(A)`。这一步很关键，因为本文后面判断“能不能顺序化”，不看 location 数量，也不看有没有共享动作，而是看**真实动作发生的时间区间是否错开**。

对于某个周期 `p` 内的活动区间，若两个 automata 满足：

$$
\sup(Active_p(A_1)) < \inf(Active_p(A_2))
$$

那么意味着在该周期内部，`A_1` 的动作严格发生在 `A_2` 之前。作者把满足这类条件、且共享同一周期长度的 automata 称为 sequentialisable。

### 3. 对 sequentialisable automata，先定义 concatenation `A_1 \cdot A_2`

一旦知道两个 automata 在周期内活动区间严格分离，就能观察到：

1. 在 `A_1` 活动时，`A_2` 其实一直停在初始位置；
2. 在 `A_2` 活动时，`A_1` 已经到达本周期末端位置；
3. 只有在周期边界的 restart 区域，两者才可能同时处于“切换”态。

这意味着，普通并行 product 中大量“两个位置都要同时记住”的状态，其实并不总是必要。于是作者先定义 concatenation `A_1 \cdot A_2`：

1. 在前半段保留 `A_1` 的位置，固定 `A_2` 在初始位置；
2. 在后半段保留 `A_2` 的位置，固定 `A_1` 在最终位置；
3. 只在 restart 区域保留双位置组合。

作者证明这个 `\cdot` 算子与原并行组合之间是 bisimilar，因此 reachability / safety 类状态性质可以安全转移过来。

### 4. 进一步用 overclock 定义更强的 sequential composition `#`

仅有 `\cdot` 还不够。作者注意到，在周期边界附近仍会出现一个 diamond-like 结构：多个组件在回到起始点时，会围绕“各自 master clock reset 的先后顺序”产生零时间 interleaving。

这些 interleaving 的本质问题是：时钟名字不同，但行为几乎同步。为此作者引入 **overclock** `\hat{o}`，用于统一代替多个 sequential timed automata 的 master clocks。

对应地，顺序组合 `A_1 # A_2` 的核心想法是：

1. 保留前半段 `A_1` 的活动；
2. 再保留后半段 `A_2` 的活动；
3. 把周期边界那串只因多时钟 reset 顺序不同而产生的 diamond collapse 掉；
4. 用单个 overclock 跟踪公共周期进度。

这样得到的 `#` 比 `\cdot` 更强，因为它不只减少位置积，还消除了周期间零时长 reset interleaving。

### 5. 通过 bisimulation / weak bisimulation 保住验证语义

作者分别证明：

1. 对 sequentialisable timed automata，`A_1 \cdot A_2` 与 `A_1 \parallel A_2` bisimilar。
2. 对更强的 sequential timed automata，`A_1 # A_2` 与并行产品 weak-bisimilar。

这意味着：

1. reachability 性质可保留；
2. 常见的 leads-to / deadlock 风格性质可继续在转换后模型上验证；
3. 你不是换了个近似模型，而是在等价或弱等价意义下做了结构压缩。

### 6. 复杂度收益来自 outgoing/enabled edges 的数量变化

论文不仅给语义证明，还解释了为什么它确实会更快。对于具有唯一 outgoing edge per location 的 sequentialisable 组件，在普通并行组合里，一个非周期边界配置仍可能看到来自多个组件的 outgoing edges；而在顺序化后，这些地方往往只剩下**一个**真正 relevant 的 outgoing / enabled edge。

因此，状态探索时每一步要考虑的分支数会从“和组件数相关”下降到常数级，这正是从二次到线性复杂度收益的来源。

### 7. 用真实 fire alarm system 展示工业可扩展性

论文最后用一个真实 fire alarm system case study 收尾。系统里有上百个传感器，本来如果每个传感器都带自己的 clock 并直接并行组合，`UPPAAL` 很快就撑不住。作者通过模型优化与 sequential composition，把这类系统推到了百级组件规模。

这里特别重要的一点是：作者不是仅用 toy example，而是拿匿名工业系统说明这个方法在大规模周期系统上确实有效。

## 解决了什么问题

这篇论文解决的，是一种非常具体却又非常普遍的冗余：**对于周期内分段活动的系统，标准并行组合会人为制造大量不必要的 product 与 interleaving**。

第一，它给出了“何时可以顺序化”的形式条件，而不是靠人工经验拍脑袋。

第二，它给出了两层变换：

1. `\cdot` 用于减少大部分无意义位置积；
2. `#` 进一步用 overclock 消掉周期边界上的零时间 diamond。

第三，它证明这些变换在需要的性质上是正确的，因此可以放心把原模型换成顺序化模型去跑 `UPPAAL`。

第四，它在 fire alarm case 上展示出明显的验证时间改善，并使百级组件规模变得可分析。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里最靠近“结构化状态压缩”这一支：

1. 它继承早期 `DBM/zone` 核心验证引擎；
2. 但把注意力放到模型活动结构，而非纯数据结构；
3. 它和后来的 urgency-based POR 一样，都试图从模型行为时序里榨出更多独立性。

它特别适合和下面几条线连读：

1. `UPPAAL` tutorial / implementation paper：理解原始组合语义；
2. 本文：识别 sequential activity；
3. `urgent partial order reduction`：在更一般的紧迫区间里继续削减 interleavings。

## 实现与材料

从内容详细程度看，这篇论文适合标 `🟩 较完整`。因为：

1. 定义层给得很系统；
2. `Active / sequentialisable / concatenation / overclock / #` 都逐层展开；
3. 还有复杂度直觉和工业案例。

若只从论文重写算法，难点主要在：

1. 如何在具体工具里识别满足条件的 sequential automata；
2. 如何做实际模型预处理与模板生成。

从实现可获取程度看，更适合标 `🟧 仅可执行/可使用版本可得`。论文明确说作者用 `Uppaal` 实现了 approach，但目前没有看到这条 `disjoint activity / sequential composition` 的独立公开源码仓库。

## 对本研究的启发

对当前博士研究，这篇论文最值得迁移的是：**状态机规模膨胀不一定来自真实并发，也可能来自验证器没有识别“表面并发、实则顺序”的结构**。

可直接迁移的想法有三点：

1. 对 LLM 生成的控制系统状态机，可以进一步分析“哪些模块虽然并列出现，但动作时间窗根本不重叠”。
2. 若能识别这种结构，验证阶段就不必盲目做全并发展开。
3. overclock 的思路说明：有时不是删状态，而是把多份等价时间进度变量统一成一个更高层的表示。
