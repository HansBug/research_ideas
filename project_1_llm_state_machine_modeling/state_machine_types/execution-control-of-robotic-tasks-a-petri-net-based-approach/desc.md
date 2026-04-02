# 机器人任务执行控制：一种基于 Petri 网的方法 / Execution Control of Robotic Tasks: A Petri Net-Based Approach

## 基本信息

- 标题：Execution Control of Robotic Tasks: A Petri Net-Based Approach
- 中文标题：机器人任务执行控制：一种基于 Petri 网的方法
- 作者：Massimo Caccia, Paolo Coletta, Gabriele Bruzzone, Giulio Veruggio
- 发表：*Control Engineering Practice*, 13(8):959-971, 2005
- DOI：`10.1016/j.conengprac.2004.10.005`
- 链接：https://doi.org/10.1016/j.conengprac.2004.10.005
- 形式主义：`Controlled Petri Net / Task-Variable Graph Execution Control`
- 主类：🕸️
- 描述客体：🏭
- 所属领域：🌡️
- 论文角色：海洋机器人任务执行控制 / `Petri Net` 应用建模
- 工具/实现获取方式：原文明确实现了 `gcpetrinetgenerator` 与 `gceexecutioncontroller`，并在 `Romeo` `ROV` 的 guidance/control 任务上测试；未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 task-variable graph、controlled `Petri Net`、goal vector 与 reconfiguration search；无独立交换标准。

## 简报

这篇论文关注的不是运动规划本身，而是“执行层”这一常被忽略却极关键的部分：规划层和决策层可能不断提出任务切换请求，但底层 guidance/control tasks 之间存在写冲突、依赖链和控制层级关系，如果只靠人工记住一长串 activate/deactivate 顺序，复杂机器人系统很快就会失控。作者因此把执行控制问题压成受约束的 `Petri Net` 重配置问题，让控制器根据 task-variable graph 自动求出一组合法的 firing transitions。

- 形式主义定位：这是 `Petri Nets` 在机器人执行控制与任务重配置中的应用条目，核心是 controlled `PN` 而非一般工作流网。
- 构造方式简述：先把任务状态表示成 `R/I/In` places 和 `A/D/S/F` transitions，再从 task-variable graph 推导规则 `(1)-(4)` 约束，最后添加 controlling net 并用 backward search 求 firing vector。
- 基础设施与场景简述：依托 `Romeo` `ROV`、task-variable graph、controlled `Petri Net` 与重配置搜索算法，服务海洋机器人 guidance/control tasks 的在线执行控制。

```text
task-variable graph -> task-state Petri net -> rules (1)-(4) / controlling net -> goal vector -> firing-vector search -> safe task reconfiguration
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. 任务集合 `T` 与变量集合 `V`。
2. 估计变量 `EV` 与控制变量 `CV`。
3. 每个任务的三态 `R / I / In` 离散执行表示。
4. 来自 task-variable graph 的冲突与依赖约束。
5. 由原始网和 controlling net 组成的受控 `Petri Net`。
6. 目标向量、firing vector 与 reconfiguration search。

### 核心抽象

论文首先把单个任务表示成任务状态网。对于未包含初始化阶段的任务，place invariant 是：

$$
x(R) + x(I) = 1
$$

对于包含初始化阶段的任务，place invariant 是：

$$
x(R) + x(I) + x(In) = 1
$$

上式中的符号逐项解释如下：

1. `R` 是 running 状态 place。
2. `I` 是 idle 状态 place。
3. `In` 是 initialization 状态 place。
4. `x(\cdot)` 表示该 place 上的 token 数。
5. 这些 invariant 保证每个任务任意时刻只处于一种执行状态。

原文最关键的执行层正确性来自规则 `(1)-(4)`。其中 no concurrent writing 可整理为：

$$
\forall v \in EV,\ \sum_{t \in T,\ v \in EO(t)} x_t(R) \le 1
$$

上式中的符号逐项解释如下：

1. `EV` 是估计变量集合。
2. `EO(t)` 是任务 `t` 输出的估计变量集合。
3. `x_t(R)` 表示任务 `t` 当前是否处于 running。
4. 该规则要求同一变量不能被多个运行中的任务同时写入。

对应地，no concurrent tracking 可压缩成：

$$
\forall v \in CV,\ \sum_{t \in CT,\ v \in CI(t)} x_t(R) \le 1
$$

这里是根据原文 task-variable 约束结构做的保守整理，其中：

1. `CV` 是控制变量集合。
2. `CT` 是控制任务集合。
3. `CI(t)` 表示任务 `t` 所跟踪的控制变量集合。
4. 该约束保证任意时刻同一控制变量只由一条控制策略接管。

论文还要求“被消费的估计必须有人完整写出、被写出的控制必须有人完整跟踪”。为了表达重配置目标，原文定义了 goal vector，满足条件写成：

$$
x \wedge x^\ast = x^\ast,\quad x \ge 0
$$

上式中的符号逐项解释如下：

1. `x` 是当前或候选 marking。
2. `x^\ast` 是目标 marking 向量。
3. `\wedge` 表示按元素取与。
4. `x \ge 0` 表示 marking 必须可容许，也就是没有负 token。

当目标建立后，执行控制器需要找到 firing vector `f_g`，使得：

$$
x_g = x_0 + D f_g
$$

上式中的符号逐项解释如下：

1. `x_0` 是当前 marking。
2. `D` 是原始 `Petri Net` 的 transition matrix。
3. `f_g` 是要执行的 firing vector。
4. `x_g` 是目标 marking。
5. 整个重配置问题因此变成“在约束满足前提下，找一组能把当前网状态推到目标状态的 firing transitions”。

### 一个最小例子与通俗解释

论文在 `Romeo` 海洋机器人 steering system 上给出了很直观的例子：

1. 决策层想让 `xRefOp` 这个高层 guidance task 进入 `RUNNING`。
2. 但它不能直接启动，因为它依赖 `xSensor`、`psiSensor`、`xGuid`、`xCntrl`、`TrActuator` 等多个上下游任务状态。
3. 执行控制器先看 task-variable graph，再看控制 `Petri Net` 里的约束，自动生成一组 activate 序列。
4. 若某条候选路径会造成冲突写入或控制链断裂，它就不会被选为 admissible solution。

通俗地说，这套方法像“给机器人任务切换加了一个离散事件交通警察”，所有任务开停都先经过它判定是否会撞车、断链或抢同一控制权。

### 运行 / 接受 / 转移语义

这篇论文的运行语义有两个层面：

1. 单个任务层面：
   - `A` 激活把任务从 `I` 推向 `R` 或 `In`。
   - `D` 停用把任务从运行态拉回 `I`。
   - 若存在初始化，则 `S/F` 分别表示初始化成功或失败。
2. 系统层面：
   - 所有任务状态组合成一个全局 marking。
   - 规则 `(1)-(4)` 通过 controlling net 被硬编码为 marking 约束。
   - 每次外部事件或重配置命令到来，执行控制器搜索一组 firing transitions，把当前 marking 推到满足目标的合法 marking。

论文对 reconfiguration 的关键假设是：对于 guidance/control tasks，可把相关 transitions 当作瞬时且可同时 firing。这样重配置求解可集中到 firing vector 搜索，而不必再处理复杂的 firing order。

### 语义边界

这篇论文的边界主要体现在：

1. 它建模的是执行层离散一致性，不是底层连续控制器本体。
2. task-variable graph 必须事先明确，系统不能是完全未知结构。
3. 对 guidance/control tasks 采用瞬时 firing 假设，这简化了搜索但限制了适用场景。
4. 重点是在线重配置和安全切换，不是一般 `PN` 理论判定边界。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 未初始化任务 invariant | `$x(R) + x(I) = 1$` | 每个任务只会处于 idle 或 running 之一。 |
| 含初始化任务 invariant | `$x(R) + x(I) + x(In) = 1$` | 把初始化阶段也纳入可观测执行状态。 |
| no concurrent writing | `$\forall v \in EV,\ \sum x_t(R) \le 1$` | 任意估计变量不能被多个任务同时写。 |
| no concurrent tracking | `$\forall v \in CV,\ \sum x_t(R) \le 1$` | 任意控制变量只允许一条控制策略接管。 |
| 目标满足条件 | `$x \wedge x^\ast = x^\ast,\ x \ge 0$` | 当前 marking 至少覆盖目标 places，且仍合法。 |
| 重配置状态方程 | `$x_g = x_0 + D f_g$` | 搜索 firing vector，把系统从当前状态推向目标状态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 每个任务都有显式 `R/I/In` 离散状态。 |
| 事件 / 触发 | 强支持 | activate/deactivate、成功/失败和重配置命令都是核心事件。 |
| 守卫 / 数据 | 强支持 | task-variable graph 结构决定依赖和互斥。 |
| 层次 | 部分支持 | guidance/control hierarchy 通过 tracking 约束体现。 |
| 并发 / 同步 | 强支持 | 多任务并发、资源冲突和重配置本身就是主体。 |
| 时间约束 | 弱支持 | 关注实时执行控制，但主体不是显式时钟网。 |
| 连续动态 / 随机性 | 弱支持 | 连续控制存在于下层，被本条目抽象成任务状态。 |
| 可执行 / 可验证性 | 强执行 | 可以直接生成控制 `PN` 并在线选择 reconfiguration 解。 |

### 形式化问题与性质

1. 论文真正补的是“任务切换次序如何自动保证安全”这一执行层问题。
2. `Petri Net` 在这里承担的是并发约束编码器和重配置求解骨架。
3. task-variable graph 让模型直接与机器人控制架构连上，而不是停留在抽象资源网。
4. 因而它是 `Petri Nets` 主干在机器人执行控制方向上一条很稳的应用路线。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先列出机器人执行层任务与共享变量。
2. 建立 task-variable graph，标出谁读谁写。
3. 把每个任务翻译成 `R/I/In` 状态网。
4. 根据规则 `(1)-(4)` 自动生成 controlling net。
5. 每次给定 goal vector 后，搜索 firing vector。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. task-variable graph。
2. 任务状态 `Petri Net`。
3. controlling net。
4. goal vector 与 firing vector 搜索结果。

### 交换与互操作

互操作重点在：

1. 任务 I/O 关系如何从控制架构转成网约束。
2. 原始网与 controlling net 如何组合成最终执行控制器。
3. 外部 mission command 如何通过 goal vector 驱动重配置。

## 配套基础设施

- 建模/编辑工具：原文实现了 `gcpetrinetgenerator` 与 `gceexecutioncontroller`。
- 解析/交换/元模型支持：task-variable graph 提供稳定的结构入口，但无统一交换标准。
- 仿真/执行支持：在 `Romeo` `ROV` 的 guidance/control system 上执行。
- 验证/分析支持：通过 `Petri Net` 约束与解搜索检查重配置是否可行。
- 代码生成/转换支持：支持从 task-variable graph 自动生成 controlled `Petri Net`。
- 标准化或社区生态：依托 `Petri Nets`、离散事件监督控制与海洋机器人执行架构研究线。

## 适用场景与需求前提

### 适用场景

适合海洋机器人、移动机器人或其他拥有多任务控制链、频繁重配置需求和明显任务依赖关系的执行控制场景。

### 需求前提

1. 任务与变量关系可抽成 task-variable graph。
2. 执行控制问题主要表现为任务冲突、依赖和重配置，而不是连续优化。
3. 任务状态能被有限离散状态表示。
4. 系统可以接受 `Petri Net` 层面的自动控制器生成与搜索。

### 不适用或高成本场景

若系统任务边界极不清晰，或者连续动态本身才是主要难点，仅做执行层 `Petri Net` 建模就不足以支撑全系统分析。

## 与相邻形式主义的关系

相对 [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)，本文不是一般 `PN` 教程，而是直接面向机器人执行控制；相对 [A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)，本文更强调 task-variable 依赖、控制层级和任务重配置；相对 [Task Planning and Formal Control of Robotic Assembly Systems: A Petri Net-Based Approach](../task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md)，本文更偏执行层控制器生成，而非装配任务规划本身。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里已经隐含“谁依赖谁、谁不能同时运行、谁必须接管哪个控制变量”时，`Petri Net` 是非常自然的目标形式主义。

### 作为目标形式主义还是中间表示

对执行控制与任务重配置，它可以直接作为目标形式主义；对更大系统，它也可作为连接规划层与底层控制层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应单独识别任务 I/O 关系，而不只是任务名称。
2. 互斥、依赖和层级唯一性很适合直接写成网约束。
3. 若后续要做自动修复，firing vector 搜索失败本身就能提供很强的诊断证据。

## 重要的相关工作

- [Petri Nets: Properties, Analysis and Applications](../petri-nets-properties-analysis-and-applications/desc.md)：本文所有任务状态与 marking 约束都建立在标准 `Petri Net` 主干上。
- [A Petri Net On-Line Controller for the Coordination of Multiple Mobile Robots](../a-petri-net-on-line-controller-for-the-coordination-of-multiple-mobile-robots/desc.md)：同样面向机器人在线控制，但对象更偏多机器人资源协调。
- [Task Planning and Formal Control of Robotic Assembly Systems: A Petri Net-Based Approach](../task-planning-and-formal-control-of-robotic-assembly-systems-a-petri-net-based-approach/desc.md)：同属机器人 `Petri Net` 应用线，但重心更偏装配任务规划。

## 文献分类总结

- 这是一篇 `🕸️` 类应用型条目，核心贡献是把机器人执行控制压成 controlled `Petri Net` 的重配置问题。
- 它描述的是多任务并发、资源与控制链关系，因此客体记为 `🏭`；论文语境面向海洋机器人与执行控制架构，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它非常适合支撑“从任务依赖需求生成并发网模型”的这条主线，并为后续验证与修复提供直接的结构化入口。
