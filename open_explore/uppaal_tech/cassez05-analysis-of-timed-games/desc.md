# Efficient On-the-fly Algorithms for the Analysis of Timed Games

- 问题一句话：timed game automata 虽然早已可判定，但已有求解方法多依赖昂贵的 backward fixpoint 或预先构造时间抽象商图，缺少真正高效的 on-the-fly 算法。
- 方法一句话：论文把 Liu-Smolka 的有限状态局部算法做成 timed symbolic 版本，用 zones 维护 simulation graph 上的部分 winning 信息，并通过前向探索和回传依赖关系交错求解 reachability / safety games。
- 解决点一句话：它给出了第一套真正 forward、zone-based、fully on-the-fly 的 timed games 求解算法，并把 timed games 从“理论可做”推进到“工具可算”。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `🧱 核心算法/数据结构` 与 `🎮 博弈/控制扩展` 的交界位置，是 `UPPAAL` 技术线里 timed games 分支真正立起来的一篇核心论文。

它之前，timed game automata 的问题已经被证明可判定，但主要方法存在两种痛点：

1. **backward fixpoint**
   - 理论上可行，但很难做到真正局部、真正早停。
2. **先构造时间抽象商图再做有限博弈求解**
   - 正确，但预处理极其昂贵，很难说是 on-the-fly。

因此，这篇论文的重要性非常高。它之于 timed games，差不多相当于早年 `UPPAAL` 对 timed automata reachability 的作用：把“能证明”变成“能前向地算”。

## 立足问题

这篇论文立足的问题，是 why timed games 一直缺少一个像 `UPPAAL` reachability 那样实用的前向 symbolic 算法。

作者在引言里说得很明白：对于普通 timed automata，`Kronos` 和 `UPPAAL` 之所以成功，很大程度就在于 forward symbolic on-the-fly exploration。它允许：

1. 只围绕初始状态附近展开；
2. 一旦性质已能确定就提前终止；
3. 利用 zones 高效处理 dense-time。

但 timed games 的求解并不一样。reachability 的 simulation graph 本身太抽象，若直接把 symbolic states 当成有限图节点来做有限博弈，往往会得出错误结论。论文一开始就用一个小例子说明：

1. 纯 simulation graph 会把某初始状态误判为 uncontrollable；
2. 若换成 time-abstracted quotient graph，又能判对；
3. 但 quotient graph 预处理太重，失去 on-the-fly 意义。

也就是说，论文真正要解决的是：

> 能否像 `UPPAAL` 做 reachability 那样，一边前向探索 symbolic state-space，一边就地求出哪些部分是 winning，而无需先构造完整时间抽象商图。

这要求算法同时具备：

1. zone-based efficiency；
2. local / on-the-fly termination；
3. 对 winning status 的逐步细化能力；
4. 对 controller / environment 对抗语义的正确处理。

## 核心方法

这篇论文的方法非常漂亮，本质上是把**有限状态局部博弈算法**提升成**带 zones 的 timed symbolic 博弈算法**。

### 1. 先回顾 timed game automata 与经典 backward 求解

论文从 `Timed Game Automata` 出发。模型与 timed automata 类似，但动作被分成：

1. controllable actions；
2. uncontrollable actions。

reachability game 的目标是：控制方是否能保证无论环境如何走，最终都进入目标位置 `Goal`。这类问题经典解法是 backward 计算 controllable predecessors。

作者并没有否认 backward 路线，而是先把它作为对照：它是正确的，但不是他们想要的那类真正 local / forward / early-stopping 算法。

### 2. 先在 untimed finite games 上实例化 Liu-Smolka 算法

为了说明思想，论文先把 Liu-Smolka 的局部算法实例化到 untimed reachability games。

该算法维护：

1. `Passed`
   - 已见状态；
2. `Waiting`
   - 待探索边；
3. `Win[q]`
   - 某有限状态当前是否已知 winning；
4. `Depend[q]`
   - 哪些前驱依赖 `q` 的 winning status 变化。

算法的关键味道是：

1. 先局部 forward 探索；
2. 一旦某节点被证成 winning，就通过 `Depend` 回传影响；
3. 因此不需要先把整图完全构出来。

这一部分是 timed extension 的模板。

### 3. 在 timed symbolic 场景里，把单点 winning 改成 zone 内部分 winning

timed case 最难的一点在于：symbolic state 不再是单个离散点，而是：

$$
S = (\ell, Z)
$$

其中 `Z` 是一个 zone。

对这样的 `S`，你不能只说“整个 `S` winning”或“整个 `S` losing”，因为同一 symbolic state 内不同 valuation 可能有不同的博弈结果。因此论文的关键升级是：

1. 不再用布尔量 `Win[q]`；
2. 而是用一个集合：

$$
Win[S] \subseteq S
$$

它表示在当前已知信息下，`S` 中哪部分 valuation 已经确定是 winning。

这是整篇论文最核心的思想之一。它等于承认：

1. zones 是分析单位；
2. 但 winning 信息在 zone 内部可能是逐步长出来的，而不是一次全有全无。

### 4. 交错做 forward exploration 与 backward propagation

由此，作者提出 `SOTFTR` 算法。它有两个交织过程：

1. **forward**
   - 探索 simulation graph 上新的 symbolic states 和边；
2. **back-propagation**
   - 当某些 symbolic states 内新的 winning 子区间被识别出来时，把信息沿 `Depend` 回传到前驱。

核心数据结构变成：

1. `Passed`
   - 已见 symbolic states；
2. `Waiting`
   - 待处理 symbolic transitions；
3. `Win[S]`
   - 当前已知 winning subset；
4. `Depend[S]`
   - 哪些前驱边依赖 `S` 未来可能新增的 winning information。

这个设计使算法能够：

1. 不等完整状态空间展开完；
2. 也不等某 symbolic state 内所有 valuation 一次性分类完；
3. 只要初始状态已落入某个 `Win[S0]` 就可提前停。

这就是真正的 on-the-fly。

### 5. 用 `Pred_t` 与 unions of zones 处理博弈前驱

在普通 timed reachability 中，forward successor 通常还是单个 zone；但博弈里要算 controllable predecessors 时，问题复杂得多。

作者指出，计算 timed game predecessors 会自然产生 unions of zones。这意味着：

1. `Win[S]` 往往不是单个 zone；
2. 算法必须能处理 zone unions；
3. `Pred_t` 的定义要能在基本 zone operations 上实现。

这一步是 timed games 真正比普通 reachability 更难的地方。论文后续给出：

1. how to represent unions of zones；
2. 如何在其上计算 controllable predecessor；
3. 如何保持算法整体仍然高效。

也就是说，这篇论文并不是简单把已有 reachability engine 套个 game 外壳，而是认真处理了 winning set 非凸化的问题。

### 6. 加入三类关键优化

论文第 5 节继续加入优化，这些优化很关键，因为它们决定算法是否只是“可行”，还是“真能跑”。

#### 6.1 Zone inclusion

像普通 `UPPAAL` 一样，用 inclusion check 减少前向探索步数，避免在 simulation graph 上重复扩张无效 symbolic states。

#### 6.2 Bad / losing pruning

作者指出，若某些状态已经知道 controller 输了，就没必要继续做某些昂贵探索。这让 losing information 也成为剪枝依据，而不仅是 winning information。

#### 6.3 Time-optimal winning strategies

这是非常漂亮的一步。论文不只问“是否能赢”，还问“最短多久能保证赢”。其做法是引入额外 clock `z` 并逐步判定最小时间界 `t*`，从而找到 time-optimal winning strategy。

这一步把 timed games 与此前 `UPPAAL` 在 optimal scheduling 上的兴趣自然接上了。

### 7. 原型实现与实验

论文最后展示实验实现结果，表明：

1. 基于 zones 的 timed games 求解在实践上是可行的；
2. 多项优化对性能帮助明显；
3. 即便从理论上讲 zones 比 regions“更粗更难分析”，实践上它依然是对的方向。

作者明确写出，基于 zones 的实现表现“very encouraging”。这为后面的 `UPPAAL-Tiga` 直接铺平了道路。

## 解决了什么问题

这篇论文解决的是 timed games 领域长期存在的一个“算法断层”问题。

### 1. 它第一次给出了真正 forward 的 timed games 求解算法

此前 timed games 有理论、有 backward 解、有 expensive quotient 路线，但缺少真正 `UPPAAL` 风格的前向局部算法。这篇把这个缺口补上了。

### 2. 它解决了 symbolic state 内 winning 信息并不齐一的问题

用 `Win[S] \subseteq S` 而不是布尔 winning 标签，是一个非常关键的 conceptual breakthrough。

### 3. 它把 timed game solving 推向 controller synthesis 可落地的方向

特别是 time-optimal winning strategies 这一节，已经明显在朝后续 controller synthesis tool 迈进。

## 与 UPPAAL 技术线的关系

这篇论文在 `UPPAAL` 技术线中是 timed games 分支的奠基条目。

### 它接在谁之后

它建立在：

1. 普通 `UPPAAL` reachability engine 的 forward symbolic 思想；
2. 之前关于 optimality / scheduling 的 symbolic search 经验；
3. timed game automata 的 decidability 与 backward predecessor 理论。

### 它往后影响了谁

它直接影响：

1. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/)
   - 工具化成熟版。
2. 后续 timed games / partial observability / control synthesis 分支。

### 它更靠近哪条主线

它最靠近：

1. timed games；
2. controller synthesis；
3. zone-based on-the-fly algorithms；
4. winning strategy computation。

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟩 较完整`。
   - 问题、算法骨架、数据结构、优化和实验都讲到了，已经足够重建其主要思路。
2. **实现可获取程度**
   - 适合评为 `🟥 源码未见明确公开`。
   - 论文提到的是 experimental implementation，而非一个当时已经成熟公开可获取的标准工具版本。
3. **材料质量**
   - `paper_content.txt` 很适合作为 timed games 主条目；若后续要细化 `UPPAAL-Tiga` 线，必须反复回读这篇。

## 对本研究的启发

这篇论文对当前博士研究的启发在于：**当分析目标从“判断性质”升级到“为控制方找策略”时，原有 symbolic engine 不必推倒重来，但其语义对象必须变得更细。**

可直接借鉴的点有：

1. 闭环系统里“一个符号状态内部不同元素的结论不同”是常态，不能强行全有全无。
2. 依赖关系回传与部分已知信息传播，是避免整图预展开的关键。
3. 若未来要做“验证-修复-控制建议”一体化，timed games 这类思路很值得持续关注。
