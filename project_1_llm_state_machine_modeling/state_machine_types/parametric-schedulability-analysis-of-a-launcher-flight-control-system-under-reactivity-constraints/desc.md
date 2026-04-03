# 发射器飞控系统在反应性约束下的参数化可调度性分析 / Parametric Schedulability Analysis of a Launcher Flight Control System under Reactivity Constraints

## 基本信息

- 标题：Parametric Schedulability Analysis of a Launcher Flight Control System under Reactivity Constraints
- 中文标题：发射器飞控系统在反应性约束下的参数化可调度性分析
- 作者：Etienne Andre，Emmanuel Coquard，Laurent Fribourg，Jawher Jerray，David Lesens
- 发表：*Fundamenta Informaticae*，Volume 182，Number 1，2021
- DOI：`10.3233/FI-2021-2065`
- 链接：https://doi.org/10.3233/FI-2021-2065
- 形式主义：`Parametric Stopwatch Automata / Launcher Flight-Control Scheduling Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：参数综合 / `Parametric Stopwatch Automata` 代表应用条目
- 工具/实现获取方式：原文明确使用 `IMITATOR` 建模与综合，并将结果与 `Cheddar`、`Uppaal` 等工具对比；当前目录保存的是作者公开版本 / `arXiv:2112.07548`。
- 标准/格式获取方式：承载方式是 `PSA` 网络、observer-style reactivity automata 和 `IMITATOR` 输入模型；无统一交换标准。

## 简报

这篇论文是这轮最有扩树价值的一篇之一，因为它不只是“把参数塞进时间自动机”，而是明确写出了 `parametric stopwatch automata` 这一组合分支：一方面需要参数化 deadline / offset / WCET，另一方面又必须保留线程被抢占时的执行进度，所以单独的 `PTA` 或单独的 `SWA` 都不够。作者用 `PSA` 对火箭飞控中的 `Navigation / Guidance / Control / Monitoring` 线程调度和 reactivity 约束做统一建模，然后用 `IMITATOR` 合成满足 schedulability 的参数区域。

- 形式主义定位：这是 `Timed Automata -> Stopwatch Automata` 与 `Parametric Timed Automata` 的交汇条目，正文显式使用 `Parametric Stopwatch Automata` 作为建模对象。
- 构造方式简述：把系统写成 processings `P`、threads `T`、reactivities `R`，再分别为 processing activation、thread、FPS scheduler 和每条 reactivity 构造 `PSA`，最后做 reachability synthesis。
- 基础设施与场景简述：依托 `IMITATOR`、observer-style reactivity automata 和 compositional verification，服务空间发射器飞控软件的参数综合。

```text
processings / threads / reactivities -> activation / thread / scheduler / observer PSA -> reachability synthesis -> 可调度参数区域
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. real-time system `S = \{P, T, R\}`。
2. 线程五元组 `(PT_i, OT_i, DT_i, MAF_i, P_i)`。
3. reactivity 约束 `r_i = ((p_{i1} \to \cdots \to p_{ik}), DR_i)`。
4. `Parametric Stopwatch Automata (PSA)`。
5. `IMITATOR` 上的 reachability synthesis。

### 核心抽象

论文把系统可调度性的核心约束写成：

$$
r_i = ((p_{i1} \to p_{i2} \to \cdots \to p_{ik}), DR_i)
$$

上式中的符号逐项解释如下：

1. `p_{i1}, \ldots, p_{ik}` 是一条 reactivity 链上的 processings。
2. `p_{i1} \to \cdots \to p_{ik}` 表示数据必须沿这条 precedence path 传递。
3. `DR_i` 是这条 reactivity 的最大允许端到端时延。

论文给出的 `PSA` 定义是：

$$
A = (\Sigma, L, \ell_0, X, P, I, S, E)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是有限动作集合。
2. `L` 是有限位置集合。
3. `\ell_0` 是初始位置。
4. `X` 是时钟集合。
5. `P` 是参数集合。
6. `I` 为位置不变式。
7. `S` 是 stop function，给每个位置分配一组被暂停的 clocks。
8. `E` 是边集合，每条边带 guard、action、reset 和目标位置。

### 一个最小例子与通俗解释

论文中最直观的例子是 `Navigation -> Control` 或 `Navigation -> Monitoring` 这类 reactivity：

1. `Navigation` 在某个 thread 中完成后，数据不会立刻传给后续 processing，而是要等到 thread period 末尾才发送。
2. 下一条 thread 也不是立刻读取，而是在它自己的激活点读取。
3. 如果只用“两个 processing 的完成时刻差”去算 latency，会低估真实反应时间。
4. 因此作者为每条 reactivity 单独造了 observer automaton，让它监听 thread start / end、processing start / end，并用局部时钟测真正的端到端时间。

通俗地说，这篇论文在做的不是“参数化一个 clock guard”，而是“参数化整个多线程飞控时序骨架，同时保留抢占暂停和线程间确定性通信”。

### 运行 / 接受 / 转移语义

论文给出的 `PSA` 语义包含两类迁移：

$$
(\ell, w) \xrightarrow{e} (\ell', w')
$$

$$
(\ell, w) \xrightarrow{d} (\ell, w \%+ d_{\neg S(\ell)})
$$

上式中的符号逐项解释如下：

1. 第一式是 discrete transition：若存在边 `e = (\ell, g, a, R, \ell')` 且当前赋值满足 `g`，就跳到 `\ell'` 并重置 `R` 中的时钟。
2. 第二式是 delay transition：在位置 `\ell` 上延时 `d`，但 `S(\ell)` 中的时钟会被冻结，其他时钟继续前进。
3. `w` 是当前时钟赋值，`w'` 是 reset 后的新赋值。

论文对 schedulability 的定义是：

$$
S \text{ is schedulable } \iff \left(
\forall t_i \in T,\ \text{each instance of } t_i \text{ ends before } DT_i
\right) \land \left(
\forall r_i \in R,\ \text{the end of the last thread instance in } r_i \text{ occurs before } DR_i
\right)
$$

这一定义虽然在原文中是自然语言分条列出，但逻辑上就是“线程 deadline 满足”与“reactivity bound 满足”的合取。

### 语义边界

这篇论文也清楚写出边界：

1. 一般 `PTA` / `PSA` 的参数可达性问题在理论上高度不可判定。
2. 文章能给出有用结果，是因为模型保持了强结构化和高度模块化。
3. 其方法特别依赖 observer-style reactivity automata；反应性约束编码是主要复杂源。
4. 若把更多不确定性、更多线程或更复杂分配策略一起放进模型，求解成本会迅速飙升。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| reactivity 约束 | `$r_i = ((p_{i1} \to \cdots \to p_{ik}), DR_i)$` | 把端到端时延需求写成显式 precedence + latency 上界。 |
| `PSA` 元组 | `$A = (\Sigma, L, \ell_0, X, P, I, S, E)$` | 在 `PTA` 上进一步加入 stop function。 |
| delay 语义 | `$(\ell, w) \xrightarrow{d} (\ell, w \%+ d_{\neg S(\ell)})$` | 只有未被 stop 的时钟继续前进。 |
| schedulability 条件 | `thread deadlines` 与 `reactivity bounds` 的合取 | 不仅检查任务 deadline，还显式检查 end-to-end reactivity。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | processing activation、thread、scheduler、observer 都有显式位置。 |
| 事件 / 触发 | 强支持 | `actT1`、`startNavigation`、`endT1` 等同步动作很完整。 |
| 守卫 / 数据 | 强支持 | guards 中同时出现 clocks、parameters 和 thread timing constants。 |
| 层次 | 中等支持 | 不是显式层次状态机，但模型是高度模块化组合。 |
| 并发 / 同步 | 强支持 | 多个 automata 通过同步动作共同推进。 |
| 时间约束 | 强支持 | periods、offsets、deadlines、WCET、reactivity bounds 全都显式建模。 |
| 连续动态 / 随机性 | 不支持 | 问题完全落在离散线程调度和端到端时延上。 |
| 可执行 / 可验证性 | 强支持 | `IMITATOR` 直接做参数综合与 reachability synthesis。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先把系统规格写成 `P`、`T`、`R` 三部分。
2. 为每个 processing activation 建一个周期激活 automaton。
3. 为每个 thread 建一个带 stopwatches 的执行 automaton，再为 FPS scheduler 建一个独立 automaton。
4. 为每条 reactivity 建一个 observer automaton，最后整体交给 `IMITATOR`。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `IMITATOR` 输入语言下的 `PSA` 网络。
2. processing activation / thread / scheduler / reactivity 四类 automata。
3. 参数化 offsets、deadlines 与 context switch time。
4. reachability synthesis 输出的参数约束区域。

### 交换与互操作

论文没有统一交换标准；它的主要价值在于：

1. 把飞控调度问题系统化翻译成 `PSA` 网络；
2. 把 reactivities 也变成可组合的 observer automata；
3. 使调度验证与参数综合落在同一形式化骨架上。

## 配套基础设施

- 建模/编辑工具：`IMITATOR`。
- 解析/交换/元模型支持：无统一 XML/JSON 标准。
- 仿真/执行支持：重点不在仿真，而在参数综合与 reachability synthesis。
- 验证/分析支持：`IMITATOR`；文中还与 `Cheddar`、`Uppaal` 做结果对比。
- 代码生成/转换支持：支持把飞控 processings / threads / reactivities 翻译成 `PSA` 网络，但未给自动代码生成器。
- 标准化或社区生态：属于 `IMITATOR` / parametric timed verification 工具线。

## 适用场景与需求前提

### 适用场景

适合具有多线程周期调度、可抢占执行、未知或待综合的 timing constants，以及明确 end-to-end reactivity 要求的高保证实时系统。

### 需求前提

1. 线程结构、processings 分配和 reactivities 必须可显式列出。
2. 关键时序量要能抽象成参数而不是复杂函数。
3. 抢占必须保留“执行进度暂停/恢复”语义。
4. 系统规模仍要允许参数综合工具在可接受时间内终止。

### 不适用或高成本场景

若参数过多、线程过多或 observer 过于复杂，`PSA` 综合会很快变重；论文也明确展示了 reactivity observers 带来的额外代价。

## 与相邻形式主义的关系

相对 [Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata](../timed-verification-of-the-generic-architecture-of-a-memory-circuit-using-parametric-timed-automata/desc.md)，这里不仅参数化了 timing constants，还必须表达 preemption/resume，因此从 `PTA` 走到了 `PSA`；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，这里保留了 stopwatches 的抢占表达能力，同时新增了 parameters；相对 [A Modeling Framework for Schedulability Analysis of Distributed Avionics Systems](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)，两者都做可调度性分析，但本文把 `SWA` 进一步推进到参数综合与 reactivity observers。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文几乎直接回答了“当需求里既有抢占，又有未知时间常数，又有端到端反应性约束时，目标形式主义该选什么”这个问题：答案往往不再是普通 `TA`，而是 `Parametric Stopwatch Automata`。

### 作为目标形式主义还是中间表示

对 timing-parameter synthesis 问题，它可以直接作为目标形式主义；对一般需求自动建模，它也很适合作为高保真验证/综合中间表示。

### 对需求到模型生成的启发

1. 文本中的 `offset / deadline / WCET / reaction time` 是天然参数槽位。
2. 线程间确定性通信会改变真实 latency，不能只看 processing 完成时刻。
3. 若需求强调 preemption 和参数综合，就要同时考虑 `Stopwatch` 与 `Parametric` 两个维度。

### 现实限制

`PSA` 的表达力很强，但代价是分析复杂度也更高；后续若走这条路线，必须高度依赖 modular modeling 和 compositional checking。

## 重要的相关工作

- [Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata](../timed-verification-of-the-generic-architecture-of-a-memory-circuit-using-parametric-timed-automata/desc.md)：提供 `Parametric Timed Automata` 的主干参照。
- [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)：提供 `Stopwatch Automata` 的主干参照。
- [A Modeling Framework for Schedulability Analysis of Distributed Avionics Systems](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)：展示非参数化 `SWA` 在复杂实时架构中的工程化落地。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`Parametric Stopwatch Automata / Launcher Flight-Control Scheduling Model`
- 论文角色：参数综合 / `Parametric Stopwatch Automata` 代表应用条目
- 核心功能：对飞控线程调度与反应性约束进行参数化可调度性综合
- 关键特性：parameters + stopwatches、observer-style reactivities、FPS scheduler、`IMITATOR`
- 构造方式：processings / threads / reactivities -> activation / thread / scheduler / observer `PSA`
- 基础设施：`IMITATOR`
- 适用场景：带参数综合和端到端反应性约束的高保证实时系统
- 需求前提：线程结构、未知时序常数与抢占语义需可结构化表达
- 状态：🟢
