# 用可逆块细胞自动机表示可逆细胞自动机 / Representing Reversible Cellular Automata with Reversible Block Cellular Automata

## 基本信息

- 标题：Representing Reversible Cellular Automata with Reversible Block Cellular Automata
- 中文标题：用可逆块细胞自动机表示可逆细胞自动机
- 作者：Jérôme Durand-Lose
- 发表：*Discrete Models: Combinatorics, Computation, and Geometry (DM-CCG 2001) / Discrete Mathematics & Theoretical Computer Science Proceedings AA*, 145-154, 2001
- DOI：`10.46298/dmtcs.2297`
- 链接：https://dmtcs.episciences.org/2297/pdf
- 形式主义：`Reversible Block Cellular Automata / Partitioning Cellular Automata`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🖼️ 网格 / 图案对象
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：理论扩展
- 工具/实现获取方式：原文未提供软件实现；机器可处理入口是 ordinary reversible `CA`、block permutation、reversible block `CA` 与表示构造。
- 标准/格式获取方式：原文没有 DSL / XML / 交换标准，核心承载方式是 `CA` / `BP` 元组、块分区、局部置换 `e` 与 representation theorem。

## 简报

这篇论文的关键贡献，是把“reversible `CA` 为什么难设计、而 block / partitioning `CA` 为什么容易可逆”之间的差距，用一个结构分解定理直接打通：任意 reversible `CA` 都能被表示成若干 block permutations 的组合。对当前文库来说，它非常适合作为 [computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md](../computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md) 之后的后继节点，因为它把 reversible `CA` 的父分支进一步整理成更接近结构电路和块置换的子家族。

- 形式主义定位：`Reversible / Injective Cellular Automata` 下面的 block / partitioning 子分支。
- 构造方式简述：先给 ordinary `CA` 标准 tuple，再定义 block permutation `BP`，最后证明任意 reversible `CA` 都能写成共享同一块置换的有限个 `BP` 组合。
- 基础设施与场景简述：原文是纯理论工作，但 `CA` / `BP` 定义、reversibility 语义、representation theorem 和与 Margolus neighborhood 的关系都很清楚，足以独立挂树。

```text
reversible CA -> block partition + block permutation -> reversible block CA -> structural representation
```

## 形式主义定义与核心对象

### 定义对象

论文同时关心两类对象：

1. ordinary `d`-dimensional cellular automata。
2. block permutation / block cellular automata。

重点不是引入一种新应用模型，而是证明后者足够表达前者中的 reversible 子类。

### 核心抽象

原文把 ordinary cellular automaton 定义为：

$$
A = (d, S, r, f)
$$

上式中的符号逐项解释如下：

1. `d` 是维度。
2. `S` 是有限状态集。
3. `r` 是半径。
4. `f : S^{(2r+1)^d} \to S` 是局部函数。

若 `c \in C_S^d` 是配置，则全局函数 `G_A` 由局部邻域同步诱导。

block permutation 则写成：

$$
B = (d, S, w, o, e)
$$

上式中的符号逐项解释如下：

1. `w` 是块宽度。
2. `o` 是块分区原点。
3. `V = \llbracket 0, w-1 \rrbracket^d` 是单个 block 的体积坐标集合。
4. `e : S^V \to S^V` 是 block 上的置换。

若把位置 `i` 分解成 `i = a \cdot w + b`，其中 `b \in V`，则 block permutation 的全局作用可压成：

$$
T(c)(i) = e(c|_{a \cdot w + V})(b)
$$

这说明：整张格点先被切成规则 block，再对每个 block 同时施加同一个局部置换 `e`。

### 一个最小例子与通俗解释

最简单的一维 block permutation 例子，是把配置按宽度 `2` 划成成对 block，然后对每个 block 交换两个位置：

$$
e(x_0,x_1) = (x_1,x_0)
$$

这样全局上就是把每一对相邻 cell 对调。因为每个 block 上做的是置换，所以整个更新天然可逆。

通俗地说，block `CA` 像“把整张格子切成很多小方块，再在每个小方块里同时做同一个可逆洗牌动作”。这比直接设计 ordinary reversible `CA` 容易得多，因为局部可逆性直接由 block permutation 给出。

### 运行 / 接受 / 转移语义

这里同样不是语言接受模型，而是 configuration 演化模型。核心语义是：

$$
c \mapsto G_A(c)
$$

或

$$
c \mapsto T(c)
$$

原文强调：

$$
A \text{ is reversible } \iff G_A \text{ is bijective and has a CA inverse}
$$

而 block permutation 则天然可逆，因为只要对同一 partition 使用 `e^{-1}` 即可。

### 语义边界

这条分支的边界主要是：

1. 它仍是格点动力系统，而不是词语言自动机。
2. 核心增强点不在非均匀邻域，而在 block partition 与 block permutation。
3. 文中明确说明这里的 block / partitioning `CA` 不等于 Morita 的 partitioned `CA`。

### 关键性质与判定边界

论文的核心结果，是任意 `d` 维 reversible `CA` 都能表示成有限个 block permutations 的组合。原文给出了显式的 `d+1` 构造，可压成：

$$
G_A = T_{o_d} \circ \cdots \circ T_{o_1} \circ T_{o_0}
$$

上式中的符号逐项解释如下：

1. `G_A` 是原 reversible `CA` 的全局函数。
2. `T_{o_j}` 是不同 origin `o_j` 上的 block permutation。
3. 这些 `T_{o_j}` 共享同一块置换骨架，只是分区原点不同。

原文结论的意义非常直接：

1. reversible `CA` 不是只能靠“全局看起来像双射”来理解；
2. 它们可以被结构化地拆回 block permutation 基元；
3. 这为 reversible circuit / partitioning implementation 提供了稳定中间层。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个格点取有限离散状态，block 内部做有限置换。 |
| 事件 / 触发 | 不适用 | 由同步离散步推进。 |
| 守卫 / 数据 | 不支持 | 无一般变量守卫；增强点在块划分与置换。 |
| 层次 | 不支持 | 不是层次状态图。 |
| 并发 / 同步 | 强支持 | 所有 block 同步更新。 |
| 时间约束 | 部分支持 | 只有离散时步，无显式时钟。 |
| 连续动态 / 随机性 | 不支持 | 纯离散确定性。 |
| 可执行 / 可验证性 | 强理论支持 | reversibility、representation 和 partition compatibility 都很明确。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| ordinary `CA` | `$A=(d,S,r,f)$` | reversible `CA` 父分支的普通骨架。 |
| block permutation | `$B=(d,S,w,o,e)$` | 引入 partitioning / Margolus 风格块置换基元。 |
| block 语义 | `$T(c)(i)=e(c|_{a\cdot w + V})(b)$` | 说明 block `CA` 怎样从局部置换提升为全局更新。 |
| 可逆性 | `$e$ permutation $\Rightarrow T$ reversible` | block 路线的核心简化点。 |
| 表示定理 | `$G_A = T_{o_d}\circ\cdots\circ T_{o_0}$` | 说明任意 reversible `CA` 都能结构化分解。 |

## 构造方式与承载格式

### 建模入口

建模时首先要决定：

1. 是否要把 ordinary reversible `CA` 转换成 block / partitioning 视角。
2. 块宽度 `w` 和原点 `o` 怎样选。
3. 关心的是 ordinary `CA` 的理论表达，还是可逆块结构的实现友好性。

### 机器可处理承载方式

原文的机器可处理承载方式是 `CA` / `BP` 元组、block 体积 `V`、局部置换 `e` 与组合表示式，不是工程交换文件。

### 交换与互操作

它与以下对象互操作最自然：

1. reversible / injective ordinary `CA`。
2. Margolus neighborhood / partitioning cellular automata。
3. reversible circuitry 与结构化实现讨论。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 ordinary `CA`、`BP` 与 `R-BCA` 的元组定义。
- 仿真/执行支持：block permutation 可直接逐步执行。
- 验证/分析支持：reversibility、representation theorem 与 compatibility proof 是原文重点。
- 代码生成/转换支持：原文未给出工具，但理论上非常贴近结构化实现。
- 标准化或社区生态：属于 reversible `CA` 与 partitioning / Margolus neighborhood 理论的经典交叉点。

## 适用场景与需求前提

### 适用场景

适用于需要把 ordinary reversible `CA` 结构化分解为 block-based primitive、或需要更容易设计和检查可逆局部规则的场景。

### 需求前提

1. 对象必须是格点系统。
2. 需求核心是可逆性与结构化表示，而不是一般非可逆动力学。
3. 接受 block partition 带来的分区原点与块宽度设计。

### 不适用或高成本场景

如果需求核心是非均匀局部邻域、有限拓扑或 shift-dynamics 语义，这个分支不是最佳入口；如果只是一般 `CA` 仿真，也没有必要额外引入 block decomposition。

## 与相邻形式主义的关系

相对 [computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md](../computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md)，它不再强调通用性，而是强调结构表示；相对 [cellular-automata/desc.md](../cellular-automata/desc.md)，它把 `CA` 主线进一步收束到 block / partitioning reversible 子家族；相对 [local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md)，它研究的是另一种可逆化路径，不依赖有限非均匀拓扑。

## 与本研究的关系

### 对 Project 1 的价值

它为演化树补出了 `Reversible / Injective Cellular Automata -> Reversible Block Cellular Automata / Partitioning Cellular Automata` 这层后继节点，使细胞自动机支线的 reversible 方向不再只停留在父节点。

### 作为目标形式主义还是中间表示

它更适合作为谱系节点和结构分解中间层，而不是控制系统需求建模的直接终点；但它很适合文库中的“家族演化树”与“构造方式”整理。

## 重要的相关工作

1. [computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md](../computation-universality-of-one-dimensional-reversible-injective-cellular-automata/desc.md)：本条目的直接父节点。
2. [cellular-automata/desc.md](../cellular-automata/desc.md)：更高一层的 `CA` 主节点。
3. [local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md](../local-and-global-reversibility-of-finite-inhomogeneous-cellular-automaton/desc.md)：另一条与 reversibility 相邻、但结构不同的 `CA` 分支。

## 文献分类总结

- 这是一篇 `🧱 模型本体` 条目，因为它给出了稳定的 `BP` / `R-BCA` 结构定义和表示定理。
- 它应挂在 `Reversible / Injective Cellular Automata` 之下，作为 block / partitioning 子家族。
- 它不是 DSL、工具或应用论文，而是 classic automata theory 中非常典型的结构分解条目。
