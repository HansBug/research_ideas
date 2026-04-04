# 递归状态机的分析 / Analysis of Recursive State Machines

## 基本信息

- 标题：Analysis of Recursive State Machines
- 中文标题：递归状态机的分析
- 作者：Rajeev Alur, Michael Benedikt, Kousha Etessami, Patrice Godefroid, Thomas Reps, Mihalis Yannakakis
- 发表：*ACM Transactions on Programming Languages and Systems*, 27(4):786-818, 2005
- DOI：`10.1145/1075382.1075387`
- 链接：https://www.cis.upenn.edu/~alur/toplas2005.pdf
- 形式主义：`Recursive State Machines (RSM)`，并系统比较其与 `HSM`、pushdown systems、Boolean programs 的关系
- 主类：🧩 经典离散状态机
- 对象类型：🧱 模型本体
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🧮 形式语言与自动机理论
- 论文角色：journal full version / 表达力与判定边界整理
- 工具/实现获取方式：原文未提供工程实现；机器可处理入口是 component tuple、global state `\langle b_1,\ldots,b_r,u\rangle`、Datalog-style summary relation 与 `LTL/CTL^*` model-checking construction。
- 标准/格式获取方式：原文没有 DSL 或交换标准，核心承载方式是 component machines、boxes、entry / exit interfaces、call-return 栈语义与 flat pushdown-style transition system。

## 简报

这篇 `TOPLAS` 版本不是简单重发 2001 年 `CAV` 论文，而是把 `RSM` 的家族位置彻底讲透了：一方面，它把 `RSM` 明确定位成 `Statecharts` 风格层次状态机的递归变体；另一方面，它把 `RSM` 与 pushdown systems、context-free processes、Boolean programs 的关系全部写成可比较的 formal model，并补齐 `LTL`、`CTL*`、bounded / unbounded recursion-depth cycle detection 这些 conference 版还没完全展开的结果。对当前演化树来说，它不是新开一根枝，而是把 `RSM` 节点稳定成“层次状态机线接到 call-return / pushdown 线”的标准 journal 依据。

- 形式主义定位：`HSM` 的递归 generalization，也是 hierarchical-state-machine family 与 pushdown / recursive-control family 的标准桥接点。
- 构造方式简述：系统由若干 component machine 组成；组件内有普通节点和 boxes；进入 box 对应 call，沿 return ports 退出对应 return。
- 基础设施与场景简述：纯理论条目，但形式化给出 reachability、cycle detection、`LTL/Buchi` 与 single-exit `CTL*` model checking 路线，并系统比较 `RSM` 与 pushdown / Boolean-program families。

```text
hierarchical control + recursive call -> components + boxes + entry/exit -> stack-based global states -> reachability / cycle / LTL / CTL* checking
```

## 形式主义定义与核心对象

### 定义对象

原文把 `RSM` 明确定义成“允许递归调用的层次状态机”。它强调的不是程序语法，而是一个更直观的 state-machine 视图：组件里既可以走普通边，也可以通过 box 调用另一个组件，并在返回时回到对应 return port。

### 核心抽象

原文把一个 `RSM` 写成：

$$
A = \langle A_1,\ldots,A_k \rangle
$$

其中每个 component machine 可整理为：

$$
A_i = (N_i \cup B_i, Y_i, En_i, Ex_i, \delta_i)
$$

上式中的符号逐项解释如下：

1. `N_i` 是普通节点集合。
2. `B_i` 是 boxes 集合。
3. `Y_i : B_i \to \{1,\ldots,k\}` 指出某个 box 调用哪个组件。
4. `En_i \subseteq N_i` 是 entry nodes。
5. `Ex_i \subseteq N_i` 是 exit nodes。
6. `\delta_i` 是局部转移关系，边既可以连普通节点，也可以连到某个 box 的 call / return port。

### 一个最小例子与通俗解释

一个最小例子可以是“递归处理括号表达式”的控制流：

1. 顶层组件 `A_1` 在读到 `(` 时通过 box 调用 `A_1` 自己。
2. 被调组件处理到某个 exit node 后，通过 return port 回到外层继续。
3. 整体运行状态不再只是一个普通 node，而是“调用栈上的 boxes + 当前 node”。

通俗地说，`RSM` 像“会把调用现场压栈的层次状态机”。普通 `HSM` 只有展开复用，没有无界递归；`RSM` 则把 hierarchy 真正推进成 call-return stack semantics。

### 运行 / 接受 / 转移语义

原文把 global state 定义为：

$$
\langle b_1,\ldots,b_r,u \rangle \in B^*N
$$

上式中的符号逐项解释如下：

1. `b_1,\ldots,b_r` 是当前调用栈上的 boxes。
2. `u` 是当前最内层组件里的普通节点。
3. `B^*` 表示 box 序列，因此全局状态空间一般是无限的。
4. `N` 是所有普通节点的并集。

原文的关键 call / return 语义可压成：

$$
\langle b_1,\ldots,b_r,u \rangle \xrightarrow{\sigma} \langle b_1,\ldots,b_r,b',e \rangle
$$

表示从当前节点 `u` 经 box `b'` 调用被调组件的 entry `e`；

以及

$$
\langle b_1,\ldots,b_r,u \rangle \xrightarrow{\sigma} \langle b_1,\ldots,b_{r-1},u' \rangle
$$

表示当前节点 `u` 已经位于某个被调组件的 exit，因此弹栈并回到上一层节点 `u'`。

### 语义边界

`RSM` 的边界很清楚：

1. 它仍是 sequential family，不含并发。
2. 它仍是离散 family，不含 clocks、连续变量或概率。
3. 它的增强点只在 recursion，不在 data / guard / timed syntax。
4. 由于 global state space 无限，它天然更接近 pushdown process，而不再是 plain finite hierarchy。

### 关键性质与判定边界

原文首先给出 `RSM` 与相关模型的定位：它等价关联 pushdown systems，又是比 Boolean programs 更直接的 visual recursive-control model。

在判定边界上，原文给出 reachability 与 cycle detection 的核心复杂度：

$$
\mathrm{Reachability}(\mathrm{RSM}),\ \mathrm{CycleDetection}(\mathrm{RSM}) \in O(n\theta^2)
$$

并且空间复杂度为：

$$
O(n\theta)
$$

其中：

1. `n` 是机器总大小。
2. `\theta` 是各组件 `\min(\#entries,\#exits)` 的最大值。

对 linear-time 性质，文中给出 `LTL/Buchi` 的乘积构造；对 branching-time，单出口 `RSM` 的 `CTL*` data complexity 仍可保持线性于模型大小。journal 版额外强调了“bounded-call-stack cycle”与“unbounded-call-stack cycle”的区分，这也是该版本比 conference 版更完整的地方。

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | components + nodes + boxes。 |
| 事件 / 触发 | 强支持 | 带标签边驱动局部跳转与 call / return。 |
| 守卫 / 数据 | 弱支持 | 原文主体不引入变量，但讨论了向布尔变量扩展的可能。 |
| 层次 | 强支持 | 通过 components / boxes 给出 hierarchy。 |
| 并发 / 同步 | 不支持 | 明确是 sequential。 |
| 时间约束 | 不支持 | 无 clocks。 |
| 连续动态 / 随机性 | 不支持 | 纯离散。 |
| 可执行 / 可验证性 | 强理论支持 | reachability、cycle、`LTL/Buchi`、single-exit `CTL*`。 |

### 形式化问题与性质

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 家族总元组 | `$A=\langle A_1,\ldots,A_k\rangle$` | 组件化递归机器。 |
| 组件元组 | `$A_i=(N_i\cup B_i,Y_i,En_i,Ex_i,\delta_i)$` | `RSM` 的局部骨架。 |
| 全局状态 | `$\langle b_1,\ldots,b_r,u\rangle \in B^*N$` | 调用栈 + 当前 node。 |
| 复杂度参数 | `$\theta=\max_i \min(|En_i|,|Ex_i|)$` | 入口 / 出口接口宽度。 |
| reach / cycle | `$O(n\theta^2)$` | journal 版的核心判定边界。 |

## 构造方式与承载格式

### 建模入口

1. 先按过程 / 子任务划分 components。
2. 给每个 component 指定 finite entry / exit interface。
3. 再用 boxes 表达对子过程的调用。
4. 最后用 ordinary edges 接好内部 flow、calls 与 returns。

### 机器可处理承载方式

机器可处理承载方式主要就是：

1. component tuple；
2. boxes 到 components 的映射；
3. stack-based global-state semantics；
4. summary relation 与 product-construction verification route。

### 交换与互操作

它与当前文库中两条主线直接互操作：

1. 向上承接 [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md) 的 `HSM`。
2. 向旁边连接 pushdown / Boolean-program / context-free process families。

## 配套基础设施

- 建模/编辑工具：原文未提供。
- 解析/交换/元模型支持：核心是 component / box / port / stack semantics。
- 仿真/执行支持：可直接按 global transition system 运行。
- 验证/分析支持：reachability、cycle detection、`LTL/Buchi`、single-exit `CTL*`。
- 代码生成/转换支持：原文未讨论。
- 标准化或社区生态：研究型 family，主要与 pushdown / program-analysis 社区互证。

## 适用场景与需求前提

### 适用场景

适合：

1. 递归过程控制流与 call-return 行为建模。
2. 想把层次状态机支线接到 pushdown / context-free 语义。
3. 需要显式比较 hierarchy 与 recursion 在复杂度上的代价。

### 需求前提

1. 并发不是核心难点。
2. 递归调用才是结构复杂度来源。
3. 接口可抽成有限 entries / exits。

### 不适用或高成本场景

如果系统根本不需要 recursion，只做有限层次复用，则普通 `HSM` 更轻；如果还要并发同步或 scope labeling，应转向 `CHSM / CRSM / CDHSM / SHSM` 等邻近支线。

## 与相邻形式主义的关系

相对 `HSM`，`RSM` 允许 recursion；相对 pushdown system，`RSM` 更直接保留 state-machine / component interface 直觉；相对 [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)，它还没有把 scope-dependent labeling 纳入本体。

## 与本研究的关系

### 对 Project 1 的价值

它说明 `Statecharts -> HSM` 这条线并不会只停在 hierarchy，而是会自然继续演化到 recursive control / pushdown semantics。这对后续从需求中识别“递归流程”非常重要。

### 作为目标形式主义还是中间表示

更适合作为高表达力中间表示与理论对照基线，而不是工程团队直接维护的主语言。

### 对需求到模型生成的启发

如果需求文本里已明确出现“过程自调用 / 递归子流程 / 返回后继续上一层”这类结构，把它压成 plain `FSM` 或普通 `HSM` 都会丢失关键信息；`RSM` 才是更自然的目标 family。

### 现实限制

它没有工程标准，global state space 也不再有限，因此更适合作为 formal intermediate representation，而不是工业建模前端。

## 重要的相关工作

### 奠基或前身工作

- [model-checking-of-hierarchical-state-machines/desc.md](../model-checking-of-hierarchical-state-machines/desc.md)
- [statecharts-a-visual-formalism-for-complex-systems/desc.md](../statecharts-a-visual-formalism-for-complex-systems/desc.md)

### 同类型或同家族工作

- [analysis-of-recursive-state-machines/desc.md](../analysis-of-recursive-state-machines/desc.md)：2001 `CAV` 会议版奠基条目。
- [hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md](../hierarchical-and-recursive-state-machines-with-context-dependent-properties/desc.md)：把 scope-dependent labeling 引入 `RSM`。
- [modular-strategies-for-recursive-game-graphs/desc.md](../modular-strategies-for-recursive-game-graphs/desc.md)：把 `RSM` 推向 game / controller-synthesis 方向。

## 文献分类总结

- 这篇论文是 `RSM` 节点的标准 journal full version。
- 它严格属于 `🧩 + 🧱 + 🧮` 的模型本体条目，不是 DSL 或应用案例。
- 在当前演化树里，它最适合作为 `RSM` 节点的长期挂接依据，并补强 `uHSM -> RSM` 这一桥段的 formal-family 边界。
