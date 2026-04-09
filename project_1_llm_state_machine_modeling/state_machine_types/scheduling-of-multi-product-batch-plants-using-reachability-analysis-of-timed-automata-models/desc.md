# 用时间自动机可达性分析做多产品批处理工厂排产 / Scheduling of Multi-Product Batch Plants Using Reachability Analysis of Timed Automata Models

## 基本信息

- 标题：Scheduling of Multi-Product Batch Plants Using Reachability Analysis of Timed Automata Models
- 中文标题：用时间自动机可达性分析做多产品批处理工厂排产
- 作者：Subanatarajan Subbiah，Sebastian Panek，Sebastian Engell，Olaf Stursberg
- 发表：*Proceedings of the Fourth International Conference on Informatics in Control, Automation and Robotics*，SciTePress，2007
- DOI：`10.5220/0001627501410148`
- 链接：https://doi.org/10.5220/0001627501410148
- 形式主义：`Priced Timed Automata / Multi-Product Batch Plant Scheduling Model`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：工业排产 / `Timed Automata` 到 `Priced Timed Automata` 的应用条目
- 工具/实现获取方式：原文给出 cost-optimal symbolic reachability 与多种 reduction technique，但未提供独立公开仓库；模型与语义采用 `Uppaal` 风格组合 automata。
- 标准/格式获取方式：承载方式是 `RTN -> TA/PTA` 结构映射、symbolic reachability graph 和 shortest-path-style 搜索；无统一交换标准。

## 简报

这篇论文的意义在于，它把 process industries 里很传统的 batch scheduling 问题，改写成了一个对本文库更有价值的结构：`RTN` 规格先翻译成同步的 `Timed Automata`，再通过价格扩展和 cost-optimal symbolic reachability 直接求排产。也就是说，作者不再把调度问题只看成 `MILP`，而是明确说明“配方、资源和等待区间”可以落到自动机网络上，并且能用立即调度 / 非惰性 reduction 去削减状态空间。

- 形式主义定位：这是 `Timed Automata` 在工业排产上的强应用条目，同时也为 `Priced Timed Automata` 分支补了早期工业挂接依据。
- 构造方式简述：先用 `RTN` 描述 recipe、resources 和 place interval，再把它们翻译成同步 `TA`；若引入成本函数，则进一步落到 `Priced TA` 语义和 cost-optimal symbolic reachability。
- 基础设施与场景简述：依托 symbolic reachability graph、zone abstraction 和 immediate / non-lazy reductions，服务 multi-product batch plant 的近优排产。

```text
RTN 配方与资源网络 -> 同步 TA/PTA 模型 -> symbolic reachability graph -> 最优或近优排产
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. recipe task network (`RTN`) 中的 task、state 和 place。
2. 标准 `Timed Automata` 元组与其 `Priced TA` 扩展。
3. 由 jobs、resources 和 additional constraints 组成的同步 automata 网络。
4. symbolic state / zone abstraction。
5. 基于 cost-optimal reachability 的排产求解。

### 核心抽象

原文给出的 `TA` 定义是：

$$
TA = (L, l_0, F, C, E, inv)
$$

上式中的符号逐项解释如下：

1. `L` 是有限位置集合。
2. `l_0` 是初始位置。
3. `F` 是终止位置集合。
4. `C` 是时钟集合。
5. `E \subseteq L \times \Phi(C) \times Act \times \mathcal{P}(C) \times L` 是边集合。
6. `inv` 为位置不变式。

论文随后把它扩展成 `Priced TA` 的语义状态空间：

$$
(Q, (l_0, u_0, 0), \Delta)
$$

上式中的符号逐项解释如下：

1. `Q \subseteq L \times \mathbb{R}^{|C|} \times \mathbb{R}_{\ge 0}` 是状态空间。
2. `(l, u, p)` 中，`l` 是当前位置，`u` 是时钟赋值向量，`p` 是累积成本。
3. `\Delta` 是 time transition 与 discrete transition 的无限迁移关系。

### 一个最小例子与通俗解释

论文的直觉起点不是单个控制器，而是一个多产品批处理工厂：

1. 每个工艺步骤要占用设备、消耗时间，并可能在等待区暂存中间产物。
2. `RTN` 里的 place 还可以带时间区间 `[0, Y]`，表示 token 最多只能在这里停留 `Y` 时间。
3. 这些 recipe / resource / waiting constraints 会被翻译成一组同步 `TA`。
4. 然后从“尚未开始任何 job”的初始状态，搜索到“所有 job 完成”的目标状态，代价最小的那条路径就是排产结果。

通俗地说，这像是把传统甘特图倒过来做：不是先猜一张时间表再验证，而是先把工厂规则编码成自动机，再让 reachability 搜索自己长出一张最便宜的排程。

### 运行 / 接受 / 转移语义

原文给出的 `Priced TA` 语义是两类迁移：

$$
(l, u, p) \xrightarrow{\tau} (l, u + \mathbf{1}\tau, p + P(L) \cdot \tau)
$$

$$
(l, u, p) \xrightarrow{a} (l', u', p + P(e))
$$

上式中的符号逐项解释如下：

1. 第一式是 time transition：在 `\tau` 时间内若不变式一直成立，就让所有时钟前进，并按位置价格累计成本。
2. 第二式是 discrete transition：若边 `e = (l, g, a, r, l')` 的 guard 成立，则跳转到 `l'`，并复位 `r` 中的时钟。
3. `\mathbf{1}` 是与时钟数相同维度的全 `1` 向量。
4. `P(L)` 是当前位置的 cost rate，`P(e)` 是边的离散成本。

论文进一步说明，symbolic semantics 里会把具体时钟赋值 `u` 换成 zone `Z`，从而形成可枚举的 symbolic reachability graph；cost-optimal reachability 的目标，就是在这个 graph 上找从初始 symbolic state 到目标 symbolic state 的 cheapest path。

### 语义边界

这篇论文的边界主要有四点：

1. 它依赖 recipe 和 resource 约束可以先落成 `RTN`。
2. 为避免搜索爆炸，论文大量依赖 immediate schedules、ordinary / strict non-laziness 等 reduction。
3. 成本与时间都被写成显式 clocks + price rate，而不是更复杂的连续过程模型。
4. 它服务的是工业排产，不是一般控制合成；模型对象更偏 jobs / resources / buffer 而非控制状态机本体。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `TA` 元组 | `$TA = (L, l_0, F, C, E, inv)$` | 工业排产模型先落到标准时间自动机。 |
| `Priced TA` 语义状态 | `$(Q, (l_0, u_0, 0), \Delta)$` | 在状态中显式累积成本。 |
| delay 迁移 | `$(l, u, p) \xrightarrow{\tau} (l, u + \mathbf{1}\tau, p + P(L)\tau)$` | 时间流逝同时积累位置成本。 |
| discrete 迁移 | `$(l, u, p) \xrightarrow{a} (l', u', p + P(e))$` | 离散跳转可附加边成本。 |
| 求解目标 | `cost-optimal reachability` | 最优排产转成 reachability graph 上的最短路径问题。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | jobs、resources、buffer/waiting places 都有显式模式。 |
| 事件 / 触发 | 强支持 | 资源分配、作业开始/结束、token 转移都是核心事件。 |
| 守卫 / 数据 | 中等支持 | 重点是时钟守卫和共享资源状态。 |
| 层次 | 不支持 | 模型主体是平面 automata 组合。 |
| 并发 / 同步 | 强支持 | 多 automata 通过同步动作一起推进。 |
| 时间约束 | 强支持 | 任务处理时间、等待上界和 deadline 都显式建模。 |
| 连续动态 / 随机性 | 不支持 | 不建模连续物理量或随机加工时间。 |
| 可执行 / 可验证性 | 强支持 | symbolic reachability + reduction techniques 是主线。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 先写出 `RTN` 中的 tasks、states、places 和资源关系。
2. 把每个 job / resource / waiting constraint 翻译成同步 `TA`。
3. 若需要成本优化，再附加 `P : L \cup E \to \mathbb{R}_{\ge 0}`。
4. 通过 symbolic reachability graph 搜索目标状态。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `RTN` 配方/资源网络。
2. `TA` / `Priced TA` 网络。
3. zones 与 symbolic states。
4. cost-optimal reachability 算法及其 reduction。

### 交换与互操作

这篇论文没有定义统一交换格式；它的互操作价值主要在：

1. `RTN -> TA/PTA` 的结构化翻译；
2. 从 automata path 回写为具体 schedule；
3. 用 reduction techniques 让工业实例仍可被 reachability 方法处理。

## 配套基础设施

- 建模/编辑工具：原文未给专用图形编辑器，但模型语法与 `Uppaal` 风格同步 automata 一致。
- 解析/交换/元模型支持：无 XML/JSON 标准，主要是论文中的 `RTN -> automata` 构造。
- 仿真/执行支持：重点不在仿真，而在 symbolic reachability 和 path reconstruction。
- 验证/分析支持：cost-optimal reachability、immediate schedules、non-laziness、zone abstraction。
- 代码生成/转换支持：支持从 `RTN` 结构自动映射到 TA/PTA 模型。
- 标准化或社区生态：更接近 process scheduling + timed automata 的交叉研究线，而非通用工程标准。

## 适用场景与需求前提

### 适用场景

适合多产品批处理工厂、共享设备生产线和其他可以明确写成工艺步骤、资源互斥与等待上界的工业排产问题。

### 需求前提

1. 工艺路线必须可写成有限 `RTN`。
2. 资源冲突和处理时长要能显式离散化。
3. 优化目标要能写成 cost-optimal reachability。
4. 系统接受 symbolic graph search，而不是只依赖解析式调度公式。

### 不适用或高成本场景

若工艺高度连续、成本非线性、资源动态变化很强，或模型难以落成 `RTN`，这条 `TA/PTA` 排产路线就会变得很重。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文保留了经典 `TA` 的 clocks/guards/invariants 主骨架，但把工业 recipe / resource 约束系统性挂接到同步 automata 网络上；相对 [Resource-Optimal Scheduling Using Priced Timed Automata](../resource-optimal-scheduling-using-priced-timed-automata/desc.md)，这篇论文更贴近 process industries 的建模入口，并明确展示了 `RTN -> TA/PTA` 的工业映射；相对 [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)，这里处理的是非抢占式批处理排产，而不是执行进度冻结问题。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求天然长在“工艺步骤 + 资源竞争 + 时间窗”上时，不需要强行先写 `MILP`；完全可以先生成结构更透明的 timed-automata family 模型。

### 作为目标形式主义还是中间表示

对工业排产与资源调度问题，它可以直接作为目标形式主义；对一般控制系统自动建模，它更适合作为“资源/工艺约束后端”。

### 对需求到模型生成的启发

1. 文本中的 recipe、buffer 和 waiting upper bound 应优先抽成结构化节点。
2. 自动生成不应只产出状态图，还要显式标明 resource allocation 与 synchronization。
3. 若需求含代价优化，应同步考虑是否升级为 `Priced TA`。

### 现实限制

这类模型对状态空间缩减技巧依赖很强，因此如果后续 LLM 生成模型结构过于松散，reachability graph 会迅速爆炸。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文所有 clocks、guards、invariants 都直接继承经典 `TA`。
- [Resource-Optimal Scheduling Using Priced Timed Automata](../resource-optimal-scheduling-using-priced-timed-automata/desc.md)：同样沿着 cost-optimal reachability 路线，但更明确地稳定化了 `Priced Timed Automata` 分支定义。
- [Preemptive Job-Shop Scheduling Using Stopwatch Automata](../preemptive-job-shop-scheduling-using-stopwatch-automata/desc.md)：同属调度应用，但对抢占问题采用了 `Stopwatch` 分支。

## 文献分类总结

- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 形式主义：`Priced Timed Automata / Multi-Product Batch Plant Scheduling Model`
- 论文角色：工业排产 / `Timed Automata` 到 `Priced Timed Automata` 的应用条目
- 核心功能：把多产品批处理工厂排产转成同步 `TA/PTA` 的 cost-optimal reachability
- 关键特性：`RTN -> TA` 映射、priced semantics、zones、immediate / non-lazy reductions
- 构造方式：recipe / resource network -> synchronized automata -> symbolic reachability graph
- 基础设施：symbolic reachability engine + reduction techniques，原文未公开独立工具仓库
- 适用场景：多产品批处理工厂、共享设备生产线和工业排产
- 需求前提：工艺路线、资源互斥、等待区间和成本目标需可结构化离散化
- 状态：🟢
