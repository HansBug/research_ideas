# 资源最优调度中的加价时间自动机 / Resource-Optimal Scheduling Using Priced Timed Automata

## 基本信息

- 标题：Resource-Optimal Scheduling Using Priced Timed Automata
- 中文标题：资源最优调度中的加价时间自动机
- 作者：Jacob Illum Rasmussen，Kim G. Larsen，K. Subramani
- 发表：*Tools and Algorithms for the Construction and Analysis of Systems*，`LNCS 2988`，Springer，2004
- DOI：`10.1007/978-3-540-24730-2_19`
- 链接：https://doi.org/10.1007/978-3-540-24730-2_19
- 形式主义：`Priced Timed Automata / Energy-Optimal Task Graph Scheduling Model`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：资源优化调度 / `Priced Timed Automata` 分支代表应用条目
- 工具/实现获取方式：原文明确在 `Uppaal` 中实现 symbolic minimum-cost reachability，并将线性规划子问题替换为 network simplex / min-cost flow 求解；未提供独立公开仓库。
- 标准/格式获取方式：承载方式是 `PTA` 元组、`Uppaal` 风格 automata 组合和 task-graph-to-PTA 构造；原文未给统一交换标准。

## 简报

这篇论文对本文库的最大价值，不只是“又做了一个调度案例”，而是把 `Timed Automata` 明确推进到了一个稳定可挂树的新分支：`Priced Timed Automata`。作者要解决的是带能耗目标的 task graph scheduling：任务要分配到异构处理器和共享总线上执行，既要满足 precedence 和 deadline，又要最小化处理器与总线的总能耗。普通 `TA` 只能表示“能否在时限内到达”；论文则在位置和边上显式附加 price，从而把 reachability 直接提升成 minimum-cost reachability。

- 形式主义定位：这是 `Timed Automata -> Priced Timed Automata` 的代表应用条目，重点是“时钟约束 + 成本率 + 最优调度”。
- 构造方式简述：先把 energy task graph 写成 `(T, P, pre, \delta, \kappa, \pi, \tau, d)`，再为每个 task、processor 和 bus 构造一个 `PTA`，最后通过并行组合和最小代价可达性求最优调度。
- 基础设施与场景简述：依托 `Uppaal`、symbolic zone-based minimum-cost reachability 和 network simplex 优化，服务嵌入式处理器/总线上的能耗敏感调度。

```text
任务图与资源约束 -> task / processor / bus PTA -> symbolic minimum-cost reachability -> 最优 schedule
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. `Priced Timed Automata` 本体，即在 `TA` 的位置和边上附加价格。
2. energy task graph `(T, P, pre, \delta, \kappa, \pi, \tau, d)`。
3. task、processor、bus 三类自动机模板。
4. symbolic priced zones 与 minimum-cost reachability。
5. 以 deadline 为约束、以能耗为目标的最优调度问题。

### 核心抽象

原文给出的 `Priced Timed Automata` 定义是：

$$
A = (L, l_0, E, I, P)
$$

上式中的符号逐项解释如下：

1. `L` 是有限位置集合。
2. `l_0` 是初始位置。
3. `E \subseteq L \times B(C) \times Act \times 2^C \times L` 是边集合，包含 guard、action、reset 和目标位置。
4. `I : L \to B(C)` 为位置不变式。
5. `P : (L \cup E) \to \mathbb{N}` 为价格函数，给位置和边分别赋予单位时间价格或离散跳转价格。

论文用于应用建模的 energy task graph 定义是：

$$
G = (T, P, pre, \delta, \kappa, \pi, \tau, d)
$$

上式中的符号逐项解释如下：

1. `T` 是任务集合。
2. `P` 是处理器集合。
3. `pre : T \to 2^T` 给出每个任务的前驱。
4. `\delta : T \times P \hookrightarrow \mathbb{N}` 是任务在处理器上的执行时间。
5. `\kappa : T \to \mathbb{N}` 是任务结果在总线上的传输时间。
6. `\pi` 是处理器和总线在工作状态下的单位能耗率。
7. `\tau` 是处理器和总线在空闲状态下的单位能耗率。
8. `d` 是 deadline。

### 一个最小例子与通俗解释

论文第一页就给了一个最小例子：`t_1`、`t_2`、`t_3` 三个任务，`p_1`、`p_2` 两个处理器和一条总线。

1. `t_1` 只能在 `p_1` 上执行，`t_2` 只能在 `p_2` 上执行。
2. `t_3` 依赖 `t_1` 与 `t_2` 的结果，可以在任一处理器上执行。
3. 如果先在 `p_1 / p_2` 并行执行 `t_1 / t_2`，再把 `t_2` 的结果经总线发给 `p_1` 去执行 `t_3`，总能耗是 `138`。
4. 若换成把 `t_1` 的结果发给 `p_2` 再执行 `t_3`，总能耗会变成 `141`。

通俗地说，经典 `TA` 只会回答“能不能在 16 个时间单位内做完”；而 `PTA` 会进一步回答“在这些可行方案里，哪一种更省电”。

### 运行 / 接受 / 转移语义

原文给出的 `PTA` 语义包含两类带价格的迁移：

$$
(l, u) \xrightarrow{\delta, p} (l, u + d)
$$

$$
(l, u) \xrightarrow{e, p} (l', u')
$$

上式中的符号逐项解释如下：

1. 第一式表示 delay transition：若在 `d` 时间内始终满足 `I(l)`，就可以在位置 `l` 上延时 `d`，其价格为 `p = d \cdot P(l)`。
2. 第二式表示 discrete transition：若边 `e = (l, g, a, r, l')` 的 guard 成立，则可跳到 `l'` 并将 `r` 中的时钟复位，其价格为 `p = P(e)`。
3. `u` 是当前时钟赋值，`u' = u[r \to 0]`。

论文对 feasible schedule 的代价定义是：

$$
Cost(S) = \sum_{p_k \in P} (\pi_k \cdot proc(p_k) + \tau_k \cdot idle(p_k)) + \pi_{bus} \cdot proc(bus) + \tau_{bus} \cdot idle(bus)
$$

上式中的符号逐项解释如下：

1. `proc(p_k)` 是处理器 `p_k` 的忙碌时间。
2. `idle(p_k)` 是处理器 `p_k` 的空闲时间。
3. `\pi_k` 与 `\tau_k` 分别是忙碌和空闲时的单位能耗率。
4. 总线 `bus` 也按同样方式计价。

论文进一步把最优调度问题还原成：在由 task / processor / bus 自动机构成的全局 `PTA` 中，求“所有任务都完成”这一目标位置的 minimum-cost reachability。

### 语义边界

这篇论文的边界也很明确：

1. 它面向的是固定 task graph、固定处理器集合和单总线结构。
2. 任务不可抢占；论文的 schedule 约束显式要求处理器/总线一次只服务一个任务且不中断。
3. 重点是线性能耗率和最优可达代价，不处理概率、连续动力学或复杂数据状态。
4. 论文提升的是“可达代价分析效率”，而不是重新定义更强的底层时钟语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `PTA` 元组 | `$A = (L, l_0, E, I, P)$` | 在经典 `TA` 上加入位置/边价格。 |
| energy task graph | `$G = (T, P, pre, \delta, \kappa, \pi, \tau, d)$` | 统一描述任务、资源、传输和能耗。 |
| schedule 代价 | `$Cost(S) = \sum_{p_k \in P} (\pi_k proc(p_k) + \tau_k idle(p_k)) + \pi_{bus} proc(bus) + \tau_{bus} idle(bus)$` | 把调度目标明确写成能耗最小。 |
| 目标问题 | `minimum-cost reachability` | 从“到达目标”升级到“以最小代价到达目标”。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | task / processor / bus 都有显式离散位置。 |
| 事件 / 触发 | 强支持 | 任务开始、完成、总线传输和同步是核心。 |
| 守卫 / 数据 | 中等支持 | 重点是 clock guards 和共享变量，不靠复杂数据结构。 |
| 层次 | 不支持 | 模型主体是平面 automata 网络。 |
| 并发 / 同步 | 强支持 | 多个 task automata 与资源 automata 通过 channel/flag 同步。 |
| 时间约束 | 强支持 | deadline、执行时间、总线传输时间是主体。 |
| 连续动态 / 随机性 | 不支持 | 只处理离散资源调度与显式 clocks。 |
| 可执行 / 可验证性 | 强支持 | 支持 symbolic minimum-cost reachability。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 列出 task graph 的前驱关系和每个任务可运行的处理器。
2. 为每个 task、processor 和 bus 分别生成一个 `PTA`。
3. 用共享变量 `fin`、`act`、`res`、`d` 连接全局状态。
4. 以“所有 `fin[ti] = 1`”作为目标条件做最小代价可达性分析。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `Uppaal` 风格的 automata 网络。
2. `priced zones` 与 symbolic state space。
3. task / processor / bus 三类模板化构造。
4. branch-and-bound 的 minimum-cost reachability。

### 交换与互操作

这篇论文不关心 XML/JSON 交换标准；它的核心贡献在于：

1. 把 task graph 规格系统化映射到 `PTA`；
2. 把能耗目标嵌入 automaton 的位置/边价格；
3. 把 reachability 求解器内部的 LP 子问题压缩成 min-cost flow。

## 配套基础设施

- 建模/编辑工具：`Uppaal`。
- 解析/交换/元模型支持：原文未给通用元模型或交换文件标准。
- 仿真/执行支持：重点不在执行，而在 symbolic minimum-cost reachability。
- 验证/分析支持：branch-and-bound + priced zones + min-cost flow / network simplex。
- 代码生成/转换支持：支持从 energy task graph 自动构造成 task / processor / bus `PTA` 网络。
- 标准化或社区生态：属于 `Timed Automata` 工具线上的 cost/optimization 分支，生态集中在 `Uppaal CORA` 一类工具谱系，而非交换标准。

## 适用场景与需求前提

### 适用场景

适合能明确写成 task graph、资源占用和 deadline 的嵌入式调度问题，尤其是处理器/总线能耗也必须联合优化的场景。

### 需求前提

1. 任务依赖关系必须可写成有限前驱图。
2. 执行时间、总线传输时间和 deadline 必须可显式给出。
3. 资源代价要能写成位置/边上的线性 price rate。
4. 系统接受非抢占式调度抽象。

### 不适用或高成本场景

若系统依赖抢占恢复、概率执行时间、连续能量模型或动态资源增减，这篇论文的 `PTA` 建模就会失真或需要额外扩展。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文不是增加新的时钟约束表达式，而是把“时间”扩展成“时间 + 代价”的联合可达性问题，因此可以稳定挂到 `Timed Automata` 下的 `Priced Timed Automata` 分支；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，这里解决的是成本优化而不是可抢占执行进度冻结；相对 [Scheduling of Multi-Product Batch Plants Using Reachability Analysis of Timed Automata Models](../scheduling-of-multi-product-batch-plants-using-reachability-analysis-of-timed-automata-models/desc.md)，这篇论文更明确地把 `Priced Timed Automata` 本体和 task-graph-to-PTA 构造写成了正式定义。

## 与本研究的关系

### 对 Project 1 的价值

它说明：如果需求里除了 deadline 之外还包含能耗、资源占用或运行成本，单纯输出经典 `TA` 还不够，应该优先考虑 `Priced Timed Automata` 这类量化分支。

### 作为目标形式主义还是中间表示

对资源最优调度和能耗分析问题，它可以直接作为目标形式主义；对一般控制系统需求，它更适合作为“验证/优化后端”的增强型中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要区分“时间约束”和“优化目标”。
2. 处理器、总线、能耗率都可以直接映射成自动机位置/边价格。
3. 若目标是“找最优方案”，则输出模型不仅要可验，还要能表达代价。

### 现实限制

`PTA` 的最大难点不在建图，而在状态空间和 cost analysis 的复杂度；自动化生成如果不做结构化缩减，很容易把求解器压垮。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文所有 clocks、guards 和 invariants 都建立在经典 `TA` 语义上。
- [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)：同样做调度，但沿着 `Stopwatch` 分支解决抢占问题。
- [Timed Controller Synthesis: An Industrial Case Study](../timed-controller-synthesis-an-industrial-case-study/desc.md)：同属 `Timed Automata` 主干的优化/综合路线，但那篇转向了 controller/environment 博弈。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：⏱️ 实时与嵌入式系统
- 形式主义：`Priced Timed Automata / Energy-Optimal Task Graph Scheduling Model`
- 论文角色：资源优化调度 / `Priced Timed Automata` 分支代表应用条目
- 核心功能：把带能耗目标的 task graph scheduling 还原成 `PTA` 最小代价可达性
- 关键特性：位置/边价格、task / processor / bus 模板、priced zones、minimum-cost reachability
- 构造方式：energy task graph -> task / processor / bus `PTA` -> symbolic branch-and-bound
- 基础设施：`Uppaal` + min-cost flow / network simplex 优化
- 适用场景：能耗敏感的嵌入式处理器/总线调度
- 需求前提：任务依赖、资源占用、deadline 与 price rate 需可显式结构化
- 状态：🟢
