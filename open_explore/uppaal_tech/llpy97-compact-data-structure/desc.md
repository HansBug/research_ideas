# Efficient Verification of Real-Time Systems: Compact Data Structure and State-Space Reduction

- 问题一句话：DBM 存储大且状态空间膨胀。
- 方法一句话：最小约束 DBM 压缩结合基于控制结构的 on-the-fly 状态保存削减。
- 解决点一句话：降低 `UDBM/UPPAAL` 内存与搜索成本。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🧱 核心算法/数据结构` 条目，也是 `UPPAAL` 技术线里很典型的一篇“**不再证明可判定，而是直接解决内存与空间瓶颈**”的工作。它接在 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 之后，说明早期 `UPPAAL` 的核心问题已经从“能不能做实时模型检查”转向“**怎么把它做得足够省空间，才能扛住工业级系统**”。

从时间线看，这篇论文有两个非常清晰的位置：

1. 它承接了 `Uppaal` 早期 symbolic reachability 语义。
2. 它把后来的 `DBM / passed-list / loop-covering / control-structure reduction` 这些工程内核问题，第一次系统化地拆开处理。

与 [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/) 相比，这篇论文更像一篇“把 `DBM` 真正压到工程成本上去看”的关键桥梁；与 [behrmann03-real-time-data-structures](../behrmann03-real-time-data-structures/) 相比，它又更聚焦于 `DBM` 紧凑化与 reachability 保存策略，而不是更广的数据结构版图。

## 立足问题

这篇论文的问题意识非常直接：即使早期 `Uppaal` 已经能做 timed automata 的 reachability analysis，但一到真实规模网络上，**空间成本**立刻成为最大障碍。

作者在摘要和引言里强调，空间开销主要来自两部分：

1. **控制结构本身**
   - symbolic state 必须记住 automata 网络当前落在哪些控制节点。
2. **时钟估值的约束表示**
   - clock valuations 不是单个值，而是一个约束系统，通常用 `DBM` 表示。

问题在于，标准 `DBM` 虽然 canonical、便于 inclusion test，但它的表示天然是 $O(n^2)$ 的：每一对 clocks 的差分上界都显式存一条。对 reachability 算法来说，这有两个连锁后果：

1. 每个 symbolic state `(l, D)` 本身就很大。
2. `Passed` 列表里可能要保存绝大多数可达 symbolic states，于是大状态乘大量状态，内存直接爆炸。

所以这篇论文盯住的不是一般意义上的 state explosion，而是更具体的两个问题：

1. **每个状态能不能更小。**
2. **必须保存的状态能不能更少。**

这两个问题看起来相近，但作者非常明确地把它们拆成了两条正交路线：

1. **local reduction**
   - 压缩单个约束对象。
2. **global reduction**
   - 减少需要放进 `Passed` 的 symbolic state 数量。

这就是全文最核心的问题结构。

## 核心方法

这篇论文的方法可以压成一句话：**同时对“状态的表示大小”和“状态的保存数量”做削减，而且两者正交。** 具体来说，作者提出了两套可以组合的机制。

### 1. 先固定 reachability 的基本算法对象：symbolic states `(l, D)`

全文工作的前提，是早期 `Uppaal` 风格的 symbolic reachability 算法。算法维护：

1. `Waiting`
   - 待展开的 symbolic states。
2. `Passed`
   - 已保存、用于覆盖判定的 symbolic states。

状态形式为：

$$
(l, D),
$$

其中 $l$ 是控制节点（或控制向量），$D$ 是 clock-constraint system。reachability 本身并不新，真正的问题是：

1. `Passed` 里最后会堆很多状态。
2. inclusion checking 又要求这些状态的约束表示尽量规范。

这就迫使作者必须同时思考“表示”和“保存策略”。

### 2. 第一条线：把 DBM 从 canonical form 进一步压成最小约束系统

作者首先处理的是**单个 clock-constraint system 的冗余**。标准 `DBM` 很适合 canonical closure，但 canonical 之后仍可能保留大量冗余边。

核心思想是：如果若干差分约束可以由其他约束经最短路推出来，那它们就不必显式保存。于是作者把一个 DBM 看成带权有向图：

1. 顶点是 clocks 加一个零时钟 `0`。
2. 边权表示差分约束：

$$
x - y \le m.
$$

闭包之后，图中的最短路径就对应“最紧”的隐含约束。于是作者的问题被重写成：

> 给定一个带权有向图，能不能构造一张**边数最少**但 shortest-path closure 不变的图。

这一步非常漂亮，因为它把 `DBM` 压缩转成了标准图论问题。论文先在 zero-cycle free graph 上证明：所有冗余边都可以删掉；再推广到一般 negative-cycle free 图，引入零环等价类与 quotient / expansion 操作，最终得到最小约束图。

作者给出的总结构造可以压成：

$$
G^R = \bigl((G / {\equiv})^R\bigr)^+.
$$

其中：

1. $G / {\equiv}$ 是按 zero-equivalence classes 做 quotient。
2. $(\cdot)^R$ 是在 zero-cycle free quotient graph 上做 shortest-path reduction。
3. $(\cdot)^+$ 再把结果展开回原图。

它最终得到的不是“某种更松的近似表示”，而是：

1. 与原约束系统**等价**；
2. 仍然是**canonical**；
3. 并且显式约束数量**最小**。

作者还强调，这个最小化过程仍然保持在 $O(n^3)$ 时间内。也就是说，它不是为了省空间把时间复杂度炸掉，而是继续和 DBM closure 同一个量级。

### 3. 第二条线：不再保存所有 symbolic states，而只保存覆盖所有动态环的状态

如果说第一条线解决的是“每个状态太大”，第二条线解决的就是“状态太多”。

作者从有限图 reachability 的直觉出发：为了保证终止，其实不需要保存所有访问过的节点，只需要确保**每个循环至少有一个被记住的节点**。于是，在 timed symbolic reachability 中，他们定义了：

1. **dynamic loop**
   - 符号状态层面的环。
2. **statical loop**
   - 控制结构层面的环。
3. **entry nodes**
   - 从环外进入环内的位置。
4. **covering states**
   - 在 on-the-fly 搜索中，首次进入某类 entry 结构的关键 symbolic states。

核心观察是：每个 dynamic loop 必然在控制结构上投影到某个 statical loop，而每个 statical loop 必有 entry node。于是只要把保存策略改成“保存能覆盖所有 dynamic loops 的 covering states”，就足以保证终止。

论文给出的关键定理是：

$$
\text{every dynamic loop contains at least one covering state.}
$$

这意味着 `Passed` 列表不必再保存所有状态，只需保存这类足以卡住所有循环的关键状态。

从方法层看，这一步很值得细看，因为它不是简单的启发式剪枝，而是：

1. 先做 static control-structure analysis；
2. 再在线判断某个 symbolic state 是否是 covering state；
3. 最后把保存策略收紧到这些状态上。

也就是说，它不是“探索时碰运气少存点”，而是**把终止性条件显式化并编码进保存规则**。

### 4. 两条线是正交的，可以直接叠加

作者在摘要中就强调这两条线“essentially orthogonal”。这不是宣传语，而是因为它们作用在两个不同层级：

1. **compact data structure**
   - 缩小每个 `D`。
2. **control-structure reduction**
   - 缩小需要进入 `Passed` 的 `(l, D)` 个数。

于是组合后的收益是乘法式的，而不是相互覆盖。实验也确实显示：

1. `CDSC` 单独使用，空间大幅下降。
2. `CSR` 单独使用，也有显著节省。
3. `CDSC & CSR` 联用时，空间节省最明显，达到 `75% - 94%`。

这说明作者并不是只做了两个零散优化，而是把 `UPPAAL` 的 reachability storage problem 按层拆开，并给了两套可以叠加的系统解法。

## 解决了什么问题

这篇论文真正解决了 `UPPAAL` 早期内核里两个非常现实、也非常硬的瓶颈。

### 1. 它让 clock constraints 变得更“值得保存”

reachability 算法里最大的内存坑之一就是 `Passed`。如果每个状态都用满 DBM 存，哪怕 canonical，也未必经济。这篇论文把单个约束系统继续压缩到最小约束数，使 inclusion checking 仍然可做，但单状态成本显著下降。

### 2. 它把“必须保存哪些状态”从经验问题变成了结构化问题

很多状态空间优化工作只谈搜索顺序或去重条件，而作者在这里更进一步：直接问“为了终止，到底哪些状态必须留”。这把 `Passed` list 的设计从经验主义推进成了有静态分析支撑的规则。

### 3. 它把 `UPPAAL` 从“能跑的验证器”继续推进到“开始考虑规模经济”的验证器

如果 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 解决的是 `Uppaal` 该怎么验证，那么这篇论文解决的就是：**`Uppaal` 该怎么省内存、怎么扛住更大系统。**

### 4. 它也明确没有解决什么

这篇论文主要聚焦：

1. reachability 风格 symbolic verification；
2. DBM / clock constraints；
3. state storage policy。

它还没有进入：

1. 更广的非凸表示；
2. priced timed automata；
3. specification theory；
4. testing / games / SMC。

但恰恰因为它聚焦，所以它成了后面很多路线的底层支撑。

## 与 UPPAAL 技术线的关系

这篇论文和 `UPPAAL` 技术线的关系非常紧，几乎可以看成 `UDBM` 思维方式的早期显性成型。

### 它接在谁之后

它直接接在：

1. [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/)
   - 先把实时 symbolic model checking 与 `Uppaal` 工具骨架立起来。
2. 更早的 [dill89-timing-assumptions](../dill89-timing-assumptions/) 与 [ad90-timed-automata](../ad90-timed-automata/)
   - 提供 difference constraints / timed automata 的理论背景。

### 它往后影响了谁

它往后最直接影响的是：

1. [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/)
   - 对 `DBM` 语义、操作和实现做 thesis 级系统化整理。
2. [behrmann02-uppaal-implementation-secrets](../behrmann02-uppaal-implementation-secrets/)
   - 继续把底层表示和工程技巧讲透。
3. [behrmann03-real-time-data-structures](../behrmann03-real-time-data-structures/)
   - 扩展到更广的数据结构与算法专题。

### 它更靠近哪条主线

它最靠近：

1. `DBM / canonical closure / shortest path reduction`
2. `symbolic state storage`
3. `UPPAAL` 内核的数据结构与搜索策略

而不是后来的 `Tiga / SMC / Stratego / ECDAR` 分支。

## 实现与材料

1. **内容详细程度**
   - 当前总账给它记为 `🟢 复现级`，我认为基本成立。
   - 原因是论文把问题、算法对象、图论化最小化构造、loop-covering 保存策略和实验结果都写得相当细，已经接近可以指导实现。
2. **实现可获取程度**
   - 当前总账记为 `🟩 核心实现源码线直达`，合理。
   - 虽然不是论文同期源码快照，但 [UDBM](https://github.com/UPPAALModelChecker/UDBM) 这条官方源码线和本文主题的关系非常直接。
3. **材料质量**
   - `paper_content.txt` 质量很好，GitHub 可读性也足够。
   - 图 1、图 3、图 4 和性能表对理解方法尤其关键。

## 对本研究的启发

这篇论文对当前博士研究至少有四点直接启发。

### 1. “状态怎么表示”本身就是方法，不是实现细节

如果未来要让 LLM 生成的状态机进入验证闭环，就必须把中间表示设计当作方法学问题处理，而不是事后优化。

### 2. 要同时优化“单状态大小”和“保存状态数量”

很多自动化系统只盯一个维度，但作者展示了这两个层级是可以正交优化的。对本仓库后续的验证剖面和修复闭环，这个分层思路非常重要。

### 3. 终止性条件值得显式建模

与其默认保守地保留所有状态，不如先问：**为了终止和正确性，到底哪些状态必须保留。** 这对后续做反例驱动修复、场景搜索和 profile-based verification 都有借鉴意义。

### 4. 静态结构信息可以直接反哺动态搜索

作者用 control-structure analysis 指导 on-the-fly 保存策略，这一点对当前博士研究非常有价值：需求结构、状态机层级结构、事件依赖结构，都可能被拿来指导后续验证和修复搜索，而不只是作为输入原样交给模型检查器。
