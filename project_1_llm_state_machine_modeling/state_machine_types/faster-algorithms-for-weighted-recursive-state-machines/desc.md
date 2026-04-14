# 加权递归状态机的更快算法 / Faster Algorithms for Weighted Recursive State Machines

## 基本信息

- 标题：Faster Algorithms for Weighted Recursive State Machines
- 中文标题：加权递归状态机的更快算法
- 作者：Krishnendu Chatterjee、Bernhard Kragl、Samarth Mishra、Andreas Pavlogiannis
- 发表：*Programming Languages and Systems* (`ESOP 2017`, `LNCS 10201`), pp. 287-313, 2017
- DOI：`10.1007/978-3-662-54434-1_11`
- 链接：https://arxiv.org/pdf/1701.04914.pdf
- 形式主义：`Weighted Recursive State Machines (WRSM)`
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：模型扩展 / semiring-weighted recursive-state-machine branch
- 工具/实现获取方式：原文提到 prototype implementation，并与 `WALi` 风格 `weighted pushdown systems` 工具线及 `SLAM/SDV` benchmarks 对比。
- 标准/格式获取方式：原文没有 DSL、XML 或交换标准；核心承载方式是 semiring definition、weighted module tuple、configuration automata 与 distance queries。

## 简报

这篇论文虽然标题强调“更快算法”，但它最值得文库保留的地方其实是第一部分的 formal model：作者把 `RSM` 明确推广成“边带 semiring 权值的递归状态机”，并把 `WRSM` 写成一个足够独立、足以挂树的模型 family。对当前层次状态机支线来说，这很重要，因为它为 `RSM` 主枝补出了一条以前还没有正式命名节点的 quantitative / semiring 方向。

- 形式主义定位：`RSM` 主枝上的 semiring-weighted quantitative 扩展。
- 构造方式简述：保留 modules、boxes、entry/exit 与 call/return 栈语义，只把每条转移再标上 semiring 权值。
- 基础设施与场景简述：原文把 `Boolean semiring` reachability、dataflow semiring、configuration automata、entry-to-exit summaries 放在同一框架中，足以把 `WRSM` 固定成 stable family。

```text
RSM skeleton + semiring weights -> weighted configurations / computations -> configuration distance / node distance / interprocedural analysis
```

## 形式主义定义与核心对象

### 定义对象

原文研究的是 interprocedural analysis，但它没有只停留在某个算法上，而是先把“什么叫加权递归状态机”写成完整的 formal tuple。模型要描述的对象，是带 call/return hierarchy 的递归控制流，并且每条路径上还要累计某种 semiring-valued property。

### 核心抽象

原文先固定 idempotent semiring：

$$
\mathcal S=(D,\oplus,\otimes,\overline 0,\overline 1)
$$

上式中的符号逐项解释如下：

1. `D` 是权值域。
2. `\oplus` 是不同路径结果的 combine 运算。
3. `\otimes` 是单条路径上沿转移累计的 product 运算。
4. `\overline 0` 与 `\overline 1` 分别是加法零元与乘法单位元。

随后原文正式定义：

$$
R=\langle M_1,\ldots,M_k\rangle
$$

其中每个 module 写成：

$$
M_i=\langle B_i,Y_i,N_i,\delta_i,w_i\rangle
$$

上式中的符号逐项解释如下：

1. `B_i` 是 boxes。
2. `Y_i:B_i\to\{1,\ldots,k\}` 指定 box 调用哪个 module。
3. `N_i` 是节点集合，并被划分成 internal / entry / exit / call / return 五类节点。
4. `\delta_i` 是 module 内的转移关系。
5. `w_i:\delta_i\to D` 给每条转移赋 semiring weight。

这正是 `RSM` 的结构骨架加上 semiring weight function，因此可以自然视作 `WRSM`。

### 一个最小例子与通俗解释

一个最小例子可以是：

1. `Main` module 调用 `Check` module。
2. 若把每条边的权值取布尔 semiring，就得到 ordinary reachability。
3. 若把权值换成 dataflow 函数组合或最短路代价，就得到 interprocedural dataflow / distance analysis。

通俗地说，`WRSM` 就像“给 `RSM` 的每条边加一个可组合的数值或代数标签”。递归结构还是原来的 box / call / return，只是现在路径除了“能不能到”之外，还能积累代价、信息流或其他代数性质。

### 运行 / 接受 / 转移语义

原文的 configuration 写成：

$$
\langle u,S\rangle
$$

上式中的符号逐项解释如下：

1. `u` 是当前节点。
2. `S` 是当前 stack，也就是 box 序列。
3. `\langle u,S\rangle` 是带调用上下文的执行状态。

一条 computation `\pi` 的权值由路径上的转移权值累计得到：

$$
\otimes(\pi)=\bigotimes_{i=1}^{n-1} w(c_i,c_{i+1})
$$

上式中的符号逐项解释如下：

1. `\pi=c_1,\ldots,c_n` 是一条 computation。
2. `w(c_i,c_{i+1})` 是第 `i` 步转移的 semiring weight。
3. 整条路径的权值由 `\otimes` 沿路径累计。

而一组 computations 的总体权值由 `\oplus` 汇总。

### 语义边界

原文给出了几个特别值得保留的模型边界：

1. `SESE RSM`：每个 module single-entry / single-exit。
2. 一般 `MEME RSM`：允许 multi-entry / multi-exit。
3. semiring 需要是 idempotent finite-height semiring，才能保证算法框架稳定工作。

因此 `WRSM` 不是随便“在图边上挂个数”，而是有一套明确的代数与递归结构前提。

### 关键性质与判定边界

原文把几个核心查询对象写得很清楚，其中最适合保留下来的一个是 configuration distance：

$$
d(R,c)=\bigoplus_{\pi\in\Pi(R,c)} \otimes(\pi)
$$

上式中的符号逐项解释如下：

1. `c` 是目标 configuration。
2. `\Pi(R,c)` 是所有从起始集合到达 `c` 的 computations。
3. `\otimes(\pi)` 是单条 computation 的路径权值。
4. `d(R,c)` 是所有这类 computations 的 semiring-sum。

这说明 `WRSM` 并不是普通 `RSM` 外面包一层算法，而是把“可达性 / 数据流 / 代价”统一成一个 semiring-valued model family。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | modules、boxes、entry/exit、call/return 全部保留。 |
| 事件 / 触发 | 弱支持 | 原文主轴是 interprocedural control-flow，不强调事件接口。 |
| 守卫 / 数据 | 通过权值间接支持 | 数据流或可达性信息可编码进 semiring weight。 |
| 层次 | 强支持 | recursive module hierarchy 是模型本体。 |
| 并发 / 同步 | 不支持 | 讨论的是 sequential recursive family。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 核心新增是 semiring weights，而非概率或连续流。 |
| 可执行 / 可验证性 | 强理论支持 | node distance、configuration distance、superconfiguration distance 都被统一建模。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| semiring | `$\mathcal S=(D,\oplus,\otimes,\overline 0,\overline 1)$` | 统一不同 quantitative path property 的代数骨架。 |
| `WRSM` 骨架 | `$R=\langle M_1,\ldots,M_k\rangle$` | 递归状态机的加权版本。 |
| module tuple | `$M_i=\langle B_i,Y_i,N_i,\delta_i,w_i\rangle$` | 把 weight function 纳入 `RSM` 本体。 |
| configuration | `$\langle u,S\rangle$` | 保留调用栈上下文。 |
| configuration distance | `$d(R,c)=\bigoplus_{\pi\in\Pi(R,c)}\otimes(\pi)$` | `WRSM` 最核心的查询对象之一。 |

## 构造方式与承载格式

### 建模入口

1. 先按 procedures / functions 划分 modules。
2. 再给 modules 内部控制流建 ordinary `RSM`。
3. 最后选择合适 semiring，并给每条边赋 weight。

### 机器可处理承载方式

主要包括：

1. semiring definition；
2. weighted module tuple；
3. stack-based configuration semantics；
4. configuration automata 与 summaries。

### 交换与互操作

1. 向上承接 [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md) 的 `RSM`。
2. 在 quantitative 方向与 [weighted-automata-algorithms/desc.md](../weighted-automata-algorithms/desc.md) 的 semiring 传统互补。
3. 与 weighted pushdown systems 保持线性等价，但 `WRSM` 更保留 component / entry / exit 参数。

## 配套基础设施

- 建模/编辑工具：原文提到 prototype implementation，并与 `WALi` 风格框架比较。
- 解析/交换/元模型支持：核心是 weighted module tuple、configuration automata 与 summaries。
- 仿真/执行支持：可按 configuration relation 直接执行。
- 验证/分析支持：configuration distance、superconfiguration distance、node distance、context-bounded concurrent extensions。
- 代码生成/转换支持：原文不讨论代码生成。
- 标准化或社区生态：属于 interprocedural analysis / weighted pushdown / recursive-state-machine 三个社区的交叉点。

## 适用场景与需求前提

### 适用场景

适合：

1. interprocedural reachability。
2. semiring-style dataflow analysis。
3. 需要在递归控制流上做 weighted path reasoning 的场景。

### 需求前提

1. 系统核心是 recursive control flow。
2. 待分析性质能写成 semiring combine / product。
3. 过程接口数虽可多入口多出口，但仍须是有限的。

### 不适用或高成本场景

如果需求本质是概率或博弈递归系统，应转向 `RMC/RMDP/RCSG`；如果仅是平面 weighted automata，则不必引入递归 hierarchy。

## 与相邻形式主义的关系

相对 ordinary `RSM`，`WRSM` 的新增点是 semiring weight；相对 weighted pushdown systems，它保留了 module、entry、exit 和 box 这些更适合挂树的结构参数；相对 weighted automata，它又额外拥有 call/return hierarchy。

## 与本研究的关系

### 对 Project 1 的价值

它为 `RSM` 主枝补出了一条此前还没有正式命名节点的 quantitative family，使层次状态机演化树不只停在 deterministic / probabilistic / open / context-labeling 这几条线。

### 作为目标形式主义还是中间表示

更适合作为高表达力理论中间表示，尤其适合那些需求本身带代价、摘要函数或数据流累计语义的递归控制问题。

### 对需求到模型生成的启发

如果需求里的重点不是“是否可达”，而是“路径总代价 / 数据流效果 / 可达摘要”，LLM 不应只生成 ordinary `RSM`，而应进一步判断是否需要 `WRSM`。

## 重要的相关工作

1. [analysis-of-recursive-state-machines-toplas/desc.md](../analysis-of-recursive-state-machines-toplas/desc.md)：ordinary `RSM` 母线。
2. [weighted-automata-algorithms/desc.md](../weighted-automata-algorithms/desc.md)：semiring-weighted finite-state baseline。
3. [pebble-weighted-automata-and-weighted-logics/desc.md](../pebble-weighted-automata-and-weighted-logics/desc.md)：quantitative automata 在另一条主干上的扩展。

## 文献分类总结

- 这篇论文属于 `🧩 经典离散状态机`。
- 这篇论文的对象类型是 `🧱 模型本体`。
- 这篇论文描述的客体是 `🎛️ 控制 / 反应式逻辑`。
- 这篇论文所属领域是 `🧮 形式语言与自动机理论`。

它最适合挂到当前演化树的 `Statecharts -> HSM -> uHSM -> RSM` 之下，作为 `Weighted Recursive State Machines (WRSM)` 这条新 quantitative 子枝的代表条目。
