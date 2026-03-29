# Lower and Upper Bounds in Zone Based Abstractions of Timed Automata

- 问题一句话：经典基于最大常数的 zone extrapolation 往往过细，导致 `UPPAAL` 在某些模型上明明只关心 reachability，却仍生成过多抽象状态。
- 方法一句话：论文把“一个时钟只有一个最大常数”改成“分别维护 lower bound 与 upper bound”，用 simulation 而不是 bisimulation 来论证更粗的精确抽象，并把它落成 `DBM` 上可算的 `LU` extrapolation 与 `LU-Canonize`。
- 解决点一句话：它把 `UPPAAL` 的标准 zone normalisation 从 `M(x)` 路线推进到 `L(x)/U(x)` 路线，在保持 reachability 精确性的同时显著改善可扩展性。

## 论文定位

这篇论文在 `uppaal_tech/` 中是非常典型的 `🧱 核心算法/数据结构` 条目。它处理的是 `UPPAAL` 最核心、也最容易被忽视的一个问题：

> symbolic zone graph 想要有限，必须做 extrapolation；但 extrapolation 做得太保守，就会把可扩展性白白浪费掉。

如果说 [lpw95-real-time-model-checking](../lpw95-real-time-model-checking/) 立起了“用 zones 而不是显式 regions 做验证”的总体路线，[bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/) 把 `DBM` 和 normalisation 做成了工具级实现，那么这篇论文解决的是下一步：

1. 传统最大常数外推是否仍然太细。
2. reachability 场景是否能接受比 bisimulation 更弱、但仍完全正确的抽象依据。
3. 若答案是可以，该怎样把这种更粗抽象落到 `DBM` 算法里。

因此，这篇论文既是理论条目，也是非常实在的实现条目。

## 立足问题

这篇论文面对的问题很具体。经典 timed automata 工具通常使用基于最大常数的 extrapolation：每个 clock 配一个最大常数 `M(x)`，超过它之后的精确值就不再重要。

这种做法的问题在于：**它把上界和下界混为同一种“常数出现”看待了。**

论文开头给出的反例很有代表性。某时钟 `x` 可能在某个 guard 中出现一个极大的上界，例如 `10^6`，而真正与 reachability 有关的，可能只是另一些很小的下界或差分关系。若仍按传统 `M(x)=10^6` 去 extrapolate，那么就会额外区分大量本质上对 reachability 没有区别的 symbolic states，例如：

$$
(\ell, x - y = k)
$$

其中 $k$ 要一直区分到 `10^6`。

作者的关键观察是：

1. 若只关心 reachability，并不总需要 bisimulation 那样强的等价；
2. simulation 向下闭包已经足够保证“能到达某离散位置”这一类性质；
3. 而 simulation 往往允许更粗的抽象。

也就是说，这篇论文真正的问题意识不是“再发明一种 DBM 技巧”，而是：

> reachability 的正确性究竟需要多强的语义关系，能否因此放宽 extrapolation。

## 核心方法

这篇论文的方法主线非常清晰：**先把正确性依据从 bisimulation 改成 simulation，再把这个语义放宽翻译成 `DBM` 上可计算的 `LU` extrapolation。**

### 1. 先区分 `M(x)` 与 `L(x)/U(x)` 两种世界

经典方法给每个时钟一个最大常数：

$$
M(x)
$$

这相当于不区分该常数在模型里是以“上界”形式出现还是以“下界”形式出现。

论文则把它拆成：

$$
L(x), \qquad U(x)
$$

其中：

1. `L(x)` 是 clock `x` 在 guards / invariants 中出现的最大 lower bound；
2. `U(x)` 是 clock `x` 在 guards / invariants 中出现的最大 upper bound。

这一步的直觉很简单但非常关键：

1. 若我们在判断某 guard `x <= c` 能否满足，那么比起知道 `x` 的精确上界，很多时候更重要的是 `x` 至少已经大到哪里；
2. 相反，对 `x >= c` 这类 guard，又更关心其 upper-side 结构。

也就是说，不同方向的约束在 reachability 上的“有用信息”并不对称。

### 2. 用 simulation preorder 替换 bisimulation 作为抽象正确性依据

接下来论文从语义层重新立基。传统最大常数抽象通常通过 bisimulation 证明正确；论文则指出，对于 reachability，simulation 已经足够。

作者定义了一个 `LU-preorder`：

$$
\nu' \preceq_{LU} \nu
$$

其核心含义是：

1. 若某 clock 的值往“只会让系统更容易满足 future upper-bound constraints”的方向变化，就可视作 simulation 上更小或更可覆盖；
2. 这种比较分别依据 `L(x)` 与 `U(x)` 来决定。

证明策略也非常干净：

1. 先证明该关系是 simulation relation；
2. 再利用“simulation 保持 reachability”；
3. 从而说明基于该 preorder 的向下闭包 abstraction 对 reachability 仍 sound / complete。

这一步的贡献很大，因为它把 timed abstraction 的正确性论证，从“等价类必须强到能保全部行为”改成了“只要足够保住 reachability 就行”。

### 3. 定义比经典 `M`-abstraction 更粗的 `a_{LU}`

在语义上，作者定义了基于 `LU-preorder` 的抽象，也就是把一个 valuation set 向 `\preceq_{LU}` 下闭包。

其结论是：

1. 该抽象比传统 `M`-abstraction 更粗；
2. 但对 reachability 仍保持 sound / complete。

这说明“lower/upper 分离”不是拍脑袋启发式，而是确实能在语义上产生更小但仍精确的状态空间。

不过作者也明确承认，单纯这个集合论定义还不够，因为它未必保持 convexity，也就不方便继续用 `DBM` 做工具实现。

### 4. 把语义抽象落成 `DBM` 上的 `Extra_{LU}` 系列 operator

因此，论文真正困难也最关键的一步，是把上面的语义抽象翻译成 zone / `DBM` 上的可计算 extrapolation。

作者提出一组 `DBM`-level operator，最终重点落在：

$$
a_{Extra_{LU}^+}
$$

直观理解就是：

1. 它不是直接计算最粗的语义闭包；
2. 而是寻找一个仍由 zone 表示、仍可高效操作、且被语义 `LU` 抽象所包住的 `DBM` 外推；
3. 因此兼顾了正确性、有限性和实现性。

文章的证明结构也很有层次：

1. 先给出若干 extrapolation 之间的包含关系；
2. 再证明最大的那个 `LU`-style extrapolation 仍落在语义 `a_{LU}` 之内；
3. 最终得到它 sound、complete、finite 且 effectively computable。

这条链条其实非常像把“抽象语义想法”一步步压缩成“可部署到 `UPPAAL` 里的 operator”。

### 5. 利用 `LU-form` 改写 `DBM` normal form 计算

论文并不止步于“状态更少”。作者进一步发现：一旦 clock 被区分成 lower-bounded 与 upper-bounded，`DBM` 的很多项天然就是 `+\infty`，无需真的存。

于是作者定义：

1. `Low = {i | x_i is lower bounded}`
2. `Up = {i | x_i is upper bounded}`

并指出对应 `DBM` 可以只保留：

$$
O(|Low| \cdot |Up|)
$$

数量级的有效约束，而不必维持完整的 $O(n^2)$ 矩阵。

在此基础上，论文提出 `LU-Canonize` 替代普通 `Canonize`。核心思想是：

1. 若 `DBM` 已经处于 `LU-form`；
2. 则 Floyd-Warshall 的很多循环分支其实没必要跑；
3. 因而 normal form 计算可以直接按 lower/upper 非对称结构裁剪。

这一步非常关键，因为它说明 `LU` 路线不仅减少 symbolic states，也减少单个 successor computation 的成本。

### 6. 在 `UPPAAL` 中做原型实现并与经典外推、convex hull 近似比较

论文最后把 location-based `LU` extrapolation 原型实现进 `UPPAAL 3.4.2`，并配合 `LU-Canonize` 做实验。

比较对象包括：

1. 经典 non-location-based extrapolation；
2. 经典 location-based extrapolation；
3. `LU` location-based extrapolation；
4. convex hull approximation。

实验结果表明：

1. 在 `Fischer` 和 `CSMA/CD` 等模型上，`LU` extrapolation 明显更能扩规模；
2. 其速度有时已经接近 convex hull 这种 over-approximation；
3. 但 `LU` 仍然是 exact 的；
4. 对更复杂控制结构的工业案例，收益相对有限，这说明它并不是万能优化，而是更适合那些瓶颈主要来自 clock bounds 的模型。

作者还观察到：`LU-Canonize` 本身就能再带来大约 `20%` 左右加速。

## 解决了什么问题

这篇论文解决了 `UPPAAL` zone abstraction 路线中的一个核心瓶颈。

### 1. 它把“最大常数外推过细”这个问题正面解决了

此前大家都知道 region 太细、zone 更实用，但 zone 自己的 extrapolation 仍可能过细。这篇论文第一次系统说明：问题不在 zone 本身，而在于 `M(x)` 口径太保守。

### 2. 它给 reachability 引入了更合适的正确性依据

通过 simulation 而非 bisimulation，作者证明 reachability 可以容忍更粗抽象。这一转向非常重要，因为它提供了之后许多更激进外推与剪枝策略的语义模板。

### 3. 它把“更粗抽象”真正做成了工具里能跑的 `DBM` 算法

若只有语义 preorder，没有 `Extra_{LU}` 与 `LU-Canonize`，这篇论文就只是理论想法；而它真正有价值的地方在于，作者把理论改进直接变成了 `UPPAAL` 原型里的性能收益。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线里很像一个“**外推精化升级点**”。

### 它接在谁之后

它直接接在：

1. [bengtsson02-clocks-dbms-states](../bengtsson02-clocks-dbms-states/)
   - 已经把 `DBM`、normalisation 和 difference constraints 问题做得非常扎实。
2. [by04-semantics-algorithms-tools](../by04-semantics-algorithms-tools/)
   - 以教材化方式总结了 regions / zones / `DBM` 主线。

### 它往后影响了谁

它往后明显影响：

1. 之后所有依赖 extrapolation 性能的 `UPPAAL` 分支；
2. [jensen23-dynamic-extrapolation-extended-timed-automata](../jensen23-dynamic-extrapolation-extended-timed-automata/)
   - 这种继续围绕 extrapolation 精细化的更晚工作；
3. cost / scheduling 路线中那些高度依赖 zone operations 的条目。

### 它更靠近哪条主线

它最靠近：

1. zone abstraction；
2. `DBM` canonicalization；
3. reachability-preserving exact extrapolation；
4. `UPPAAL` 状态空间压缩。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 原因是语义动机、`LU-preorder`、`DBM` operator、实现优化和实验全都讲到了，已经足够重建方法主线。
2. **实现可获取程度**
   - 适合评为 `🟨 部分实现源码可得`。
   - 论文明确在 `UPPAAL 3.4.2` 原型中实现了 location-based `LU` extrapolation 与 `LU-Canonize`，但该历史原型与当前公开代码并非严格一一对应；不过实现思想显然进入了后续工具线。
3. **材料质量**
   - `paper_content.txt` 信息质量很好，适合拿来作为 `LU` extrapolation 的主条目。

## 对本研究的启发

这篇论文对当前博士研究的启发很直接：**一个闭环平台想扩规模，不能只盯着更大算力，还要问“我们是不是在维持某种其实不必要的过细表示”。**

具体可借鉴的点有：

1. 当目标只需保证某类性质时，应反问自己是否真的需要最强等价关系。
2. 表示层的非对称信息常常有价值，不能一味做“统一上界”的对称设计。
3. 语义放宽若不落实到数据结构与核心算子上，就无法真正转化为系统收益。
4. 这篇论文也说明，exact 方法并不一定就比 over-approximation 慢，关键看抽象口径是否选对。
