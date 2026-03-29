# Efficient Guiding Towards Cost-Optimality in UPPAAL

- 问题一句话：传统 `UPPAAL` 只能找可达解，不能高效找 reachability 的最小代价解。
- 方法一句话：为 `UPTA` 定义 symbolic cost states、基于 `DBM` 的 cost 表示，以及类 `Dijkstra` 的 minimum-cost 搜索与 branch-and-bound 剪枝。
- 解决点一句话：把 `UPPAAL` 从“能找到可行 trace”推进到“能系统寻找 cost-optimal trace”。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进/扩展` 条目，也是 `UPPAAL` 非常早期、但极关键的一条扩展主线：**priced / cost-optimal timed analysis**。它前接 [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/) 所呈现的 reachability-centered 工具箱，后面则一路通向 priced timed automata、expected cost、`Stratego` 等优化方向。

如果把 `UPPAAL` 早期主线压成一句话，那么 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 解决的是“怎样验证可达性”，而这篇论文解决的是“**当目标状态可达时，怎样以最小代价到达它**”。这两者看似只差一个优化目标，实际却会把状态表示、搜索顺序、剪枝规则都整体改写。

## 立足问题

这篇论文的起点非常现实：很多 scheduling 问题并不满足于“找到一个可行计划”，而是希望找到**时间、资源或能耗意义上更优的计划**。早期 `UPPAAL` 的 reachability verification 虽然能回答“goal state 是否可达”，也能给出一条 trace，但它默认没有内建“最优性”概念。

作者在引言里明确指出了 verification algorithm 和 scheduling algorithm 的差别：

1. **verification**
   - 目标是尽量高效地遍历整个状态空间，判断是否满足性质。
2. **scheduling / optimization**
   - 目标是尽快找到最优或近优解，并尽早剪掉不可能更优的分支。

因此，论文真正想解决的不是一般的“优化问题”，而是三个非常具体的技术瓶颈：

1. 怎样在 timed automata 的 symbolic exploration 中引入**累积代价**。
2. 怎样让这种代价表示仍然能用 `DBM` 风格数据结构高效实现。
3. 怎样重新设计 `Waiting` 的搜索顺序，使得最优解不必等遍历完整个状态空间后才知道。

这说明它不是在现有 `UPPAAL` 上加一个 post-processing 评分器，而是要把“cost-optimality”变成 reachability 内核的一部分。

## 核心方法

这篇论文的方法主线非常清楚：**先扩模型，再扩 symbolic state，再扩搜索顺序，最后再加 branch-and-bound 风格的剪枝与启发式。**

### 1. 先把 timed automata 扩成带 location/transition prices 的模型

论文先从 `LPTA` 和其子类 `UPTA` 出发。linearly priced timed automata 在 timed automata 上加入两种价格：

1. **location price / rate**
   - 在某 location 中 delay $d$ 时间，代价增加 $d \cdot p$。
2. **transition price**
   - 执行离散动作时额外付出固定代价。

于是，一条 execution trace 的总成本被定义为所有 delay cost 与 action cost 的累加。对应的 concrete problem 是：

$$
\min \{ \mathrm{cost}(\pi) \mid \pi \text{ reaches a goal state} \}.
$$

这一步看似简单，但它已经让验证对象不再只是“是否到达”，而变成“以多大代价到达”。

### 2. 把 ordinary symbolic state `(l, Z)` 升级成 symbolic cost state `(l, C)`

论文最关键的动作，是不再满足于 zone 只表示“哪些 valuations 可达”，而是让 symbolic state 同时携带“这些 valuations 的最小已知代价”。

于是状态对象从：

$$
(l, Z)
$$

变成：

$$
(l, C)
$$

其中 $C$ 是一个 cost function：

$$
C : \mathbb{R}^C \to \mathbb{R}_{\ge 0} \cup \{ \infty \}.
$$

其含义是：若 $C(u) < \infty$，则 concrete state $(l, u)$ 可以以代价 $C(u)$ 到达。换句话说，symbolic state 不仅压缩了一批 valuations，还为每个 valuation 记录了当前最优代价。

作者进一步定义了 cost function 上的基本操作：

1. `delay(C, p)`
2. `reset r(C)`
3. `guard restriction g(C)`
4. `increment C + k`
5. 比较关系 $D \preceq C$

其中最重要的是比较关系：

$$
D \preceq C \iff \forall u,\ D(u) \le C(u).
$$

这决定了覆盖判定的语义：如果某个已探索 symbolic cost state 在同一 location 上对所有 valuations 都不比新状态更贵，那么新状态就是冗余的。

### 3. 给出 cost-aware 的 symbolic semantics

在这个新状态表示上，论文把 timed symbolic semantics 重写为两类转移：

1. **delay transition**
   - 对 cost function 做时间流逝与 rate 累积。
2. **action transition**
   - 对满足 guard 的 valuation 做 reset，并叠加离散动作价格。

这不是抽象比喻，而是明确把 cost 演化纳入 symbolic semantics。其结果是：

1. support 仍然对应一个 zone；
2. 但 zone 里的每个 valuation 还带有最小已知代价。

因此，reachability 已经被系统改写成 minimum-cost reachability，而不是在 reachability 结束后再回头求最短路径。

### 4. 对 `UPTA` 专门设计可由 `DBM` 实现的 cost 表示

如果 cost function 不能高效存储，上面那套定义就只是漂亮语义。论文最硬的贡献之一，是证明对于 `UPTA` 这类足够重要的子类，cost representation 可以重新落回 `DBM` 路线。

作者把 `UPTA` 分成两种情况处理：

#### 4.1 rate 为 `0`

这时 cost 不会随时间连续增长，整个 zone 内所有 valuations 可以共享同一个常数代价，于是 cost state 可表示为：

$$
(Z, c)
$$

#### 4.2 rate 为 `1`

这时作者引入一个额外“代价时钟” $\delta$，把 cost 编到扩展 zone 中。核心直觉是：

1. 时间流逝一单位，$\delta$ 也同步增长一单位；
2. 所以 cost 可以作为一个额外 clock dimension 来编码。

于是 rate-1 的 uniformly priced timed automata 可以用“带额外维度的 `DBM`”表示，而 termination 仍可通过只对原 clocks 做 normalization 来保证，不能去碰 $\delta$ 这一维。

这是整篇论文非常漂亮的一点：它没有为 optimization 另起一套完全不同的数据结构，而是尽量把新问题折回 `UPPAAL` 最擅长的 symbolic zone machinery。

### 5. 用 minimum-cost order 把搜索顺序改成 `Dijkstra` 风格

如果仍按普通 BFS/DFS 搜索，即使能比较代价，也往往得探索完整状态空间才能确认最优解。论文的第二个核心改动就是重写 `Waiting` 的取点规则。

作者提出 minimum-cost order (`MC order`)：

1. 每次从 `Waiting` 取出 `min(C)` 最小的 symbolic cost state；
2. 一旦第一次取出 goal state，就可以终止；
3. 此时得到的就是全局最优解。

这和 `Dijkstra` 的关系并不是口头类比，而是方法同构：

1. 都维护一批“已知可达但未完全展开”的候选；
2. 都优先展开当前最小代价候选；
3. 都利用“后续代价不会变小”的单调性保证首次命中目标就是最优。

论文甚至进一步证明：在所有“按状态代价决定探索顺序”的策略里，优先选最小 `min(C)` 的策略在 explored symbolic states 数量上是最优的。也就是说，这不只是一个好启发式，而是该类搜索策略中的最佳顺序。

### 6. 再加入 `MC+` 与 branch-and-bound 风格剪枝

仅有 `MC` 还不够，因为：

1. 许多状态会有相同的 `min(C)`；
2. 纯 `MC` 对 remaining cost 没有前瞻能力；
3. 某些大状态空间场景仍然太慢。

所以论文进一步引入：

1. **remaining-cost lower bound estimate**
2. **MC+ order**
3. **upper-bound based pruning**

其核心思想很接近 A* 与 branch-and-bound：

1. 对每个 symbolic cost state 估计从当前状态到 goal 的最小剩余代价；
2. 用 `min(C) + h(l, C)` 来排序；
3. 一旦已经找到某个上界解，就可以删掉那些即使继续搜索也不可能打破当前上界的状态。

作者特别强调，这些 heuristic 可以来自：

1. 用户对目标结构的了解；
2. 由更粗抽象网络得到的 lower bound；
3. 对调度问题结构的经验性判断。

这一步很重要，因为它说明 `UPPAAL` 这里走的不是“纯理论最优搜索”，而是主动吸收 scheduling / branch-and-bound 社群的经验，把 verification 和 optimization 两条方法学接在一起。

## 解决了什么问题

这篇论文真正解决了 `UPPAAL` 早期一个非常关键的能力缺口。

### 1. 它让 `UPPAAL` 第一次系统支持 reachability 的 cost-optimality

之前 `UPPAAL` 可以告诉你“能否达到 goal”，现在它能进一步告诉你“最小代价是多少，以及一条最优 trace 长什么样”。

### 2. 它把 optimization 做进了 symbolic core，而不是外接后处理

这意味着：

1. 覆盖判定本身变成 cost-aware；
2. 搜索顺序本身变成 optimization-aware；
3. 数据结构本身也为 optimization 重构。

这比“先列出若干 trace 再选最好”强得多。

### 3. 它开辟了后续 priced / expected-cost / strategy optimization 主线

从今天回看，这篇论文几乎就是后面以下方向的开端：

1. priced timed automata；
2. expected cost；
3. strategy synthesis / optimization；
4. `Stratego` 风格 controller optimization。

### 4. 它也保留了清楚边界

作者并没有宣称“一般 LPTA 都能像 UPTA 一样高效”。相反，论文明确承认：

1. 对完整 `LPTA`，region-based 解法很低效；
2. 这里真正高效可实现的核心结果是针对 `UPTA`；
3. 启发式下界需要用户保证保守性，否则最优性可能受影响。

这种边界意识使整篇工作非常扎实。

## 与 UPPAAL 技术线的关系

这篇论文是 `UPPAAL` 从 pure verification 向 optimization 迈出的第一大步。

### 它接在谁之后

它直接接在：

1. [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/)
   - 提供 symbolic reachability 核心。
2. [llpy97-compact-data-structure](../llpy97-compact-data-structure/)
   - 提供更成熟的 `DBM` 工程基础。
3. [lpy97-uppaal-nutshell](../lpy97-uppaal-nutshell/)
   - 明确早期 `UPPAAL` 的工具整体形态。

### 它往后影响了谁

它往后最直接影响的是：

1. [david14-minimal-expected-cost](../david14-minimal-expected-cost/)
2. [david15-uppaal-stratego](../david15-uppaal-stratego/)
3. [jensen22-monte-carlo-tree-search-priced-timed-automata](../jensen22-monte-carlo-tree-search-priced-timed-automata/)

### 它更靠近哪条主线

它最靠近的是：

1. `priced timed automata`
2. `optimal scheduling`
3. `cost-guided search`
4. `branch-and-bound inside UPPAAL`

## 实现与材料

1. **内容详细程度**
   - 当前总账给它记为 `🟩 较完整`，我认同这个判断。
   - 原因是论文已经把模型、语义对象、比较关系、`DBM` 实现技巧、`MC / MC+` 搜索以及实验收益讲得相当完整。
2. **实现可获取程度**
   - 当前总账记为 `🟥 暂未获取实现源码`，这个口径应保持。
   - 论文只说明算法实现进了 experimental `Uppaal` 版本，但当前没有稳定、公开、可核的对应源码线。
3. **材料质量**
   - `paper_content.txt` 足够支撑重建核心方法。
   - 若后续要继续抠代价时钟编码和 heuristic 定义细节，建议再回 PDF 对公式版面做核对。

## 对本研究的启发

这篇论文对当前博士研究的启发非常直接：很多 formal verification 闭环任务，最终都不会停在“存在/不存在”，而会自然走向“**哪条更优、哪条更可实现、哪条修复代价更小**”。

具体来说：

1. 后续若要做模型修复，完全可以把“修复代价”做成类似这里的 optimization object，而不只是人工比较候选。
2. symbolic state 不必只携带可达性信息，也可以携带质量指标、代价指标或风险指标。
3. 搜索顺序本身就是方法设计的重要部分，不应把它当作实现细节。
4. 如果 LLM 参与状态机修复或场景生成，这种“verification core + heuristic guidance”的结构很值得借鉴。
