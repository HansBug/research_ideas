# On-The-Fly Symbolic Algorithm for Timed ATL with Abstractions

- 问题一句话：多方实时系统上的 `TATL` 验证既比 `TCTL` 更强，也比双人 timed game 更复杂，而现有 `Uppaal Tiga` 只能覆盖其中一部分且效率受 inclusion checking 约束。
- 方法一句话：论文把 `TATL` 在 timed multiplayer games 上的判定编码进 `EADG`，为顶点定义 `Forceable / Unavoidable` 值函数，再把 `Tiga` 风格 inclusion checking 一般化为 vertex merge，最后提出 expansion abstraction 直接消除 zone inclusion 检查。
- 解决点一句话：它给出了首个面向 `TATL` 的 on-the-fly symbolic `Uppaal` 算法，并把相关实现推进到比朴素方法快近两个数量级、比原 `Tiga` 更强且更快。

## 论文定位

这篇论文在 `uppaal_tech/` 中属于 `⚡ 改进与扩展`，而且是近年 `Uppaal` 理论与算法线上非常新的一个核心节点。它不是去讲一般 ATL，也不是普通 timed game synthesis，而是在回答：

1. 如何对 **timed multiplayer games** 做 on-the-fly symbolic verification；
2. 如何处理 `TATL` 这种带 coalition quantifier、timed until 和 freeze operator 的逻辑；
3. 如何把 `Tiga` 时代的 inclusion checking 和现代 `EADG` 框架真正统一起来。

这意味着它同时连接了三条线：

1. timed games / `Tiga`
2. timed logics / `TCTL -> TATL`
3. `EADG` 风格的 on-the-fly symbolic algorithms

## 立足问题

多方实时系统的验证比经典 timed automata 明显更难。原因不只是状态空间大，而是问题本身更丰富：

1. 组件不再只有“系统 vs 环境”两方，可能有多个玩家；
2. 玩家之间可能结盟形成 coalition；
3. 逻辑不只是 reachability / safety，而是带 nested coalition quantifier 的 branching-time property；
4. 时间约束还可以通过 freeze operator 与 timed until 进一步细化。

如果只用 `Uppaal Tiga`，能处理的主要还是双人 timed games 上的一部分公式。很多更一般的 `TATL` 性质超出了它原生能力。

另一方面，若退回传统 bottom-up model checking，又会面临两个老问题：

1. 需要先处理大量其实与当前 query 无关的 reachable states；
2. 对复杂逻辑和大模型来说，前向铺满整个状态空间的代价很高。

因此，本文真正盯住的缺口是：**能否为 `TATL` 构造一个真正 on-the-fly、symbolic、可并入 `Uppaal` 的求解框架，同时还把性能做上去。**

## 核心方法

整篇论文的方法非常系统：先定义 timed multiplayer games 与 `TATL` 语义，再把判定问题编码到 `EADG`，随后引入 vertex merge，把 inclusion checking 一般化，最后用 expansion abstraction 把这类 merge 进一步“提前内化”。

### 1. 用 `TMG` 与 `TATL` 给问题对象定出完整形式语义

论文首先用 `Timed Multiplayer Games` (`TMG`) 表示模型。它本质上仍然是 timed automaton，但动作集合被按玩家划分：

$$ A = A_1 \uplus \cdots \uplus A_N $$

策略是 memoryless 的 state-to-action 映射，而 coalition `S` 的策略 profile 决定一组 outcomes。

在逻辑层，文章处理的是带 freeze operator 的 `TATL`。例如：

$$ \langle\!\langle S \rangle\!\rangle (\varphi_1 \; U \; \varphi_2) $$

以及定时版：

$$ z . \langle\!\langle S \rangle\!\rangle ((\varphi_1 \land z \le k) \; U \; \varphi_2) $$

也就是说，论文一开始就站在比 `TCTL` 和双人 games 更强的对象上。

### 2. 用 `EADG` 而不是直接状态枚举，组织 on-the-fly 判定

核心算法框架不是直接在 state graph 上做普通 fixed-point，而是使用 `Extended Abstract Dependency Graph` (`EADG`)。

在这套框架里，每个顶点表示一个子问题；对本文而言，顶点形如：

$$ \langle R, \varphi \rangle $$

其中 `R` 是 symbolic state，`\varphi` 是 `TATL` 子公式。整个求值域则选成：

$$ \langle Fed(Q), \subseteq, \emptyset \rangle $$

也就是说，每个顶点的值不是布尔值，而是“在当前 symbolic state 中，哪些具体状态满足该公式”的 federation。

这一步很重要，因为它把 timed symbolic representation 与 on-the-fly dependency solving 真正接到了一起。

### 3. `Forceable / Unavoidable` 把 coalition 语义压成可计算的值函数

为了让 `TATL` 的 coalition quantifier 能在 `EADG` 中运作，论文定义了两个关键 helper：

1. `Forceable_S`
2. `Unavoidable_S`

直觉上：

1. `Forceable_S(W_{\varphi_1}, W_{\varphi_2}, W)`
   - 表示 coalition `S` 能强制系统在保持 `\varphi_1` 的同时，经 delay 或动作走向 `W_{\varphi_2}` 或下一层目标 `W`。
2. `Unavoidable_S(...)`
   - 表示 coalition 的对手无法避免系统满足相应目标。

然后，不同公式的 EADG 值函数都按公式形态机械生成。例如对于 until：

$$ \langle R, \langle\!\langle S \rangle\!\rangle (\varphi_1 U \varphi_2) \rangle $$

其值函数就用 `Forceable_S` 把：

1. 当前满足 `\varphi_1` 的集合；
2. 当前满足 `\varphi_2` 的集合；
3. 各离散 action 后继上继续满足整个公式的集合；

拼起来。

这一步让 `TATL` 判定真正落成一套 symbolic value propagation 过程，而不只是语义定义。

### 4. 正确性依赖于 symbolic operators 都落在 zones / federations 上

论文没有在抽象层停太久，而是明确指出其操作对象是 zones / federations。它使用：

1. timed successors `W^\uparrow`
2. timed predecessors `W^\downarrow`
3. reset `W[Y]`
4. free clock `W \# x`
5. `Pred_a`、`Post_a`
6. `Pred_\lambda`

这些操作都能落在 `DBM` / federation 级表示上。因此 `EADG` 里的各类值函数虽然看起来高层，但最终都能靠 `Uppaal` 已有的 symbolic timed-state machinery 执行。

### 5. 先把 `TATL` 编码进 `EADG`，再证明编码正确

在定义完顶点与值函数后，论文证明：

$$ \langle \ell, \nu \rangle \models \varphi \iff \langle \ell, \nu \rangle \in \alpha^{G}_{\min}(\langle R, \varphi \rangle) $$

也就是说，`EADG` 上的最小不动点赋值准确对应 `TATL` 语义。与此同时，文章还给出 unsatisfied-state 的对偶编码，让负例也能提前终止，而不必总是等正例传播完。

### 6. 把 `Tiga` 风格 inclusion checking 一般化为 vertex merge

这是论文的第二个大贡献。`Uppaal Tiga` 传统上已经会做 inclusion checking：若一个 symbolic state 被另一个包含，较小的那个往往没必要单独探索。

本文把这一经验上升为 `EADG` 中的一般概念：**vertex merge**。若存在 derive function `f` 使得：

$$ v_1 \preceq_f v_2 $$

则可以把 `v_1` merge 到 `v_2`，并用 `f` 改写依赖它的值函数。对 timed symbolic domain 来说，最关键的特例就是交集型 derivation：

$$ f_R(W) = W \cap R $$

若 `R \subseteq R'`，则：

$$ \langle R, \varphi \rangle \preceq_{f_R} \langle R', \varphi \rangle $$

这正是传统 inclusion checking 在新框架里的抽象表达。

### 7. expansion abstraction 进一步把 zone inclusion 检查直接“做没了”

如果说 vertex merge 是把 inclusion checking 一般化，那么 expansion abstraction 就更激进：它直接把每个顶点在生成时扩张到该 location 的 invariant 区域。

形式上：

$$ X(\langle \ell, Z, \varphi \rangle) = \langle \ell, J I(\ell) K, \varphi \rangle $$

直觉是：若某个 location-formula 对将来很可能迟早会被探索到更大的 symbolic state 覆盖，不如一开始就直接用最大那块 `J I(\ell) K` 表示它。这样做后：

1. 每个 `location-formula` 对只保留一个 zone；
2. inclusion checking / vertex merging 基本变成冗余；
3. 图更小，且省掉昂贵的 zone inclusion 判断。

论文随后证明该 abstraction 保持正确性。于是它不只是 heuristic，而是被理论保证的 domain-specific optimization。

### 8. 在 `Uppaal` 中实现，并用 benchmark 显示近两个数量级优势

最后，论文把算法做进 `Uppaal`，并比较：

1. 不做 merge 的朴素 `EADG`
2. inclusion-based merge (`Incl`)
3. expansion abstraction (`Expand`)
4. 原生 `Tiga`

结果表明：

1. inclusion checking 相比 naive 版本能快一个数量级以上；
2. expansion abstraction 对难例又再快接近一个数量级；
3. 在 `Tiga` 可处理的那部分 query 上，`Incl+Unsat` 与 `Tiga` 相当；
4. 把 `Expand` 也移植进 `Tiga` 后，`Tiga` 本身还能再快接近一个数量级。

这说明本文不只是扩逻辑表达力，还反向改进了经典 `Tiga` 路线。

## 解决了什么问题

这篇论文一口气解决了几件长期悬着的问题。

第一，它给出了面向 timed multiplayer games 的 `TATL` on-the-fly symbolic 算法，使 `Uppaal` 能处理明显强于原 `Tiga` 能力范围的逻辑。

第二，它把 `Tiga` 里长期存在但未在一般框架中抽象清楚的 inclusion checking，上升成 `EADG` 里的 vertex merge 理论。

第三，它提出 expansion abstraction，在保持正确性的前提下，把这类昂贵 merge 的很大一部分直接消掉，显著提升性能。

第四，它证明近年的 `Uppaal` 理论工作并没有停留在零几年的 timed games，而是在继续推进更强逻辑、更一般参与方结构和更现代的 symbolic algorithm 设计。

## 与 `UPPAAL` 技术线的关系

### 它接在谁之后

它直接接在：

1. [cassez05-analysis-of-timed-games](../cassez05-analysis-of-timed-games/)
2. [behrmann07-uppaal-tiga](../behrmann07-uppaal-tiga/)
3. 更一般的 `EADG` on-the-fly model checking 框架工作
4. [jensen23-dynamic-extrapolation-extended-timed-automata](../jensen23-dynamic-extrapolation-extended-timed-automata/)
   - 代表 `Uppaal` 近年继续深挖 symbolic timed analysis 的背景

### 它往后影响了谁

它的后续影响至少包括：

1. `Uppaal` 中更强 ATL / game verification 支持；
2. 对原 `Tiga` 的直接性能改进；
3. 更一般的“用 domain-specific abstraction 替换昂贵 symbolic inclusion checks”的设计思路。

### 它更靠近哪条主线

它最靠近：

1. timed games / ATL
2. symbolic dependency-graph algorithms
3. modern `Uppaal` abstraction optimization

## 实现与材料

1. **内容详细程度**
   - 这篇论文适合评为 `🟢 复现级`。
   - `TMG/TATL` 语义、`EADG` 编码、vertex merge、expansion abstraction、算法伪码和 benchmark 都写得相当充分。
2. **实现可获取程度**
   - 更适合评为 `🟢 论文对应实现源码直达`。
   - 论文明确给出 reproducibility package `10.5281/zenodo.15195408`，并说明算法将进入后续 `Uppaal` 发布版本，这已经属于非常强的实现可追踪性。
3. **材料价值**
   - 它是当前文库里理解 `Uppaal` 近年仍在如何推进核心 symbolic algorithm 的关键新条目。

## 对本研究的启发

对当前博士研究，这篇论文非常值得重视。

第一，它说明“更强逻辑 + on-the-fly + abstraction”完全可以兼得，前提是把问题编码成合适的依赖图结构，而不是直接死磕全局状态空间。

第二，vertex merge 与 expansion abstraction 的思想很适合迁移到模型修复、验证场景生成这类任务里：很多候选状态或候选场景其实存在包含关系，若能提前合并，自动化流程会更稳。

第三，这篇论文证明了 `Uppaal` 团队直到 `2025` 仍在推进非常核心的理论与算法工作，而不是只剩工具维护。对你后续继续沿 `UPPAAL` 主线深挖技术演进，非常关键。
