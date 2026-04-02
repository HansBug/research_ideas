# 面向 ROS 可验证机器人应用的分布式 Petri 网 / Distributed Petri Nets for Model-Driven Verifiable Robotic Applications in ROS

## 基本信息

- 标题：Distributed Petri Nets for Model-Driven Verifiable Robotic Applications in ROS
- 中文标题：面向 ROS 可验证机器人应用的分布式 Petri 网
- 作者：Sebastian Ebert, Johannes Mey, René Schöne, Sebastian Götz, Uwe Aßmann
- 发表：*Innovations in Systems and Software Engineering*, 20(4), pp. 531-557, 2024
- DOI：`10.1007/s11334-024-00570-5`
- 链接：https://doi.org/10.1007/s11334-024-00570-5
- 形式主义：`Distributed Petri Nets / DiNeROS`
- 主类：🕸️
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：ROS 建模验证工具链 / 分布式 Petri 网应用
- 工具/实现获取方式：原文给出 `DiNeROS` 工具链站点、`Petri Net Engine`、`Petri Net Flattener`、`Trace Visualizer`、`Net Analyzer` 等组件，并公开说明其基于 `JastAdd`、`PNML` 与 `TINA`。
- 标准/格式获取方式：系统模型以扩展 `PNML` 为输入，落地到 `PNM` 后由 `TINA` 分析；基础 Petri 网定义遵循 `ISO/IEC 15909`。

## 简报

这篇论文不是简单“用 Petri 网描述一个机器人任务”，而是把整个 ROS 分布式应用开发链都压成分布式 Petri 网。作者提出 `DiNeROS`，把一个 ROS 应用分成 `SyM`、`RTM` 和 `PNM` 三层：`SyM` 负责用扩展 Petri 网建模 topics、services、signals 和 node nets，`RTM` 负责每个 ROS node 的运行时 Petri 网，`PNM` 则把扩展元素全部还原成基础 Petri 网，以便用 `TINA` 做状态空间分析、overflow 检测和 trace 调试。

- 形式主义定位：虽然论文有明显的工具链色彩，但主对象仍是 `Petri Nets` 如何承载 ROS 分布式控制和通信，因此归到 `Petri` 并发主干，而不是单纯工具载体。
- 构造方式简述：从扩展 `PNML` 的系统模型出发，经 splitter / flattener 变成 `RTM` 与 `PNM`，再生成 ROS packages 和运行时引擎。
- 基础设施与场景简述：依托 `PNML`、`TINA`、`ROS` 和 `DiNeROS` 自身工具链，案例是两台工业机械臂在共享工作区内协同分拣物体。

```text
ROS application requirements -> SyM (extended Petri net) -> RTM / PNM -> TINA verification + ROS package generation -> verifiable distributed robotic application
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. 基础 Petri 网及其 marking / enabling 语义。
2. 扩展到 ROS 的 `System Model (SyM)`、`Runtime Model (RTM)` 与 `Petri Net Model (PNM)`。
3. `topic channel`、`service channel`、`signal` 与 `node net`。
4. 运行时的 balloon token、handler、signal clause。
5. 基于 `TINA` 的 overflow、dead transition、signal defect 分析。

### 核心抽象

论文以 `ISO/IEC 15909` 为基础，把 Petri 网写成：

$$
PN = \langle P, T, F, RP, RT, PG \rangle
$$

上式中的符号逐项解释如下：

1. `$P$` 是 place 集合。
2. `$T$` 是 transition 集合。
3. `$F \subseteq (P \times T) \cup (T \times P)$` 是流关系。
4. `$RP$` 与 `$RT$` 分别是 reference places 和 reference transitions。
5. `$PG$` 是 pages 集合，用于组织层次结构。

marking 被定义为：

$$
M_i = [m_1(i), \dots, m_n(i)]
$$

上式中的符号逐项解释如下：

1. `$n$` 是 place 数量。
2. `$m_k(i)$` 是第 `$k$` 个 place 在时刻 `$i$` 的 token 数。
3. `$M_i$` 描述整个系统在该时刻的离散控制状态。

transition 的使能条件可保守写成：

$$
t\ \text{enabled in}\ M_i \iff \forall p \in \bullet t,\ M_i(p) \ge 1
$$

上式中的符号逐项解释如下：

1. `$\bullet t$` 是 transition `$t$` 的输入 place 集合。
2. 使能后 firing 会从输入 place 消耗 token，并在输出 place 生成 token。

对 `DiNeROS` 的整体建模链，结合原文可保守整理为：

$$
SyM \longrightarrow \{RTM_k\}_{k=1}^{N} \longrightarrow PNM
$$

上式中的符号逐项解释如下：

1. `$SyM$` 是全局系统模型，显式引入 topics、services、signals 和 node nets。
2. `$RTM_k$` 是第 `$k$` 个 ROS node 的运行时 Petri 网。
3. `$PNM$` 是把扩展构造全部下沉为基础 Petri 网后的验证模型。

### 一个最小例子与通俗解释

论文案例是两台机械臂在共享工作区协同分拣：

1. `selector` 根据物体颜色把 token 发往不同 controller。
2. 两个 robot controller 通过 service 请求共享工作区访问权。
3. place `PStateGet` 中只有一个 token，因此同一时刻只有一台机械臂能进入共享区。
4. pick / place 服务访问共享 safety model；若传感器发现人进入，则 token 进入 `PUnsafe`，执行中止。

通俗地说，这个模型像一个“把 ROS 系统拆成好多会传 token 的节点网”。topic 就是广播 token 的通道，service 是带请求/响应的同步通道，而共享资源互斥则天然对应 place 里只有一个 token。

### 运行 / 接受 / 转移语义

原文给了三类关键通信语义。

对 topic channel：

$$
M \xrightarrow{topic} M'
$$

其效果是：从一个 publisher-side input place 中取走一个 token，并把它复制到每个 subscriber-side output place。

对 service channel：

$$
request \leadsto response
$$

其效果是：client 端发出请求 token 后阻塞，直到 server-side response place 提供响应 token，再返回给对应 client。

对 signals，论文把输入信号子句写成可分析的逻辑门控，保守压缩为：

$$
IC = \bigwedge_i s_i \ \lor \ \bigvee_j s_j \ \lor \ \neg s_k
$$

上式中的符号逐项解释如下：

1. `$IC$` 是 input signal clause。
2. `$s_i$` 是二值输入信号。
3. `$\land,\lor,\neg$` 分别表示与、或、非。
4. 这些子句会被转换成基础 Petri 网中的门控结构，因此它们的可满足性也能进入模型检查。

### 语义边界

这篇论文的边界如下：

1. 它主要保证离散工作流、通信和资源控制，而非连续控制律正确性。
2. 手写 handler / callback 仍可能注入错误，因此模型正确不等于实现全部正确。
3. 当前工作主要基于 ROS 1 的通用子集，尚未把 ROS 2 QoS 正式纳入语义核心。
4. 状态空间仍会爆炸，因此很多分析依赖 partial state space 与 reduction。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 基础 PN | `$PN = \langle P, T, F, RP, RT, PG \rangle$` | 建模链最终仍落回标准 Petri 网对象。 |
| marking | `$M_i = [m_1(i), \dots, m_n(i)]$` | 系统状态由 token 分布刻画。 |
| 使能条件 | `$t$ enabled `iff` $\forall p \in \bullet t,\ M_i(p) \ge 1$` | transition firing 由输入 token 决定。 |
| MDD 链 | `$SyM \to \{RTM_k\} \to PNM$` | 全局模型先拆 node，再降到基础 Petri 网做验证。 |
| overflow 检测 | `enabled(T_{Drop})` | 只要某个 topic queue 的 overflow transition 可使能，就存在消息丢失风险。 |
| dead node 检测 | `matchCount = NumTransitions(node_fragment)` | 若 node 内全部 transition 都是 dead transitions，则整个 node 实际无用。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | marking 精确表示 ROS 各 node / channel / service 的离散工作流。 |
| 事件 / 触发 | 强支持 | topic 消息、service request/response、signal 变化都是显式事件。 |
| 守卫 / 数据 | 强支持 | signal clauses、容量限制和 balloon tokens 都进入模型。 |
| 层次 | 强支持 | pages、node nets、SyM/RTM/PNM 三层结构很清晰。 |
| 并发 / 同步 | 强支持 | 分布式 ROS nodes、本地工作流和通信通道天然并发。 |
| 时间约束 | 弱支持 | 本文主体仍是基础 Petri 网，明确的实时语义留待未来 `Time Petri Nets`。 |
| 连续动态 / 随机性 | 不支持 | 重点是离散控制和通信。 |
| 可执行 / 可验证性 | 强执行、强验证 | 既能生成 ROS packages，又能用 `TINA` 做状态空间和 trace 分析。 |

### 形式化问题与性质

1. 论文的关键点在于把“ROS 的结构、通信和工作流”放到同一个 Petri 网框架里。
2. `SyM` 负责建模可读性，`PNM` 负责可验证性，`RTM` 负责运行时执行，这三个层次分工很清楚。
3. 共享资源互斥、消息队列溢出、死节点和错误 signal clauses 都能在同一分析链上检查。
4. 对 `Petri` 主干来说，这篇论文说明现代 ROS 分布式机器人应用完全可以用并发网模型做系统级工程承载。

## 构造方式与承载格式

### 建模入口

建模流程可以概括为：

1. 先在扩展 `PNML` 中建 `SyM`。
2. 用 `topic channel`、`service channel`、`signal`、`node net` 表达 ROS 结构。
3. 经 `Splitter` 生成每个 node 的 `RTM`。
4. 经 `Flattener` 生成基础 `PNM`，再交给 `TINA` 分析。

### 机器可处理承载方式

原文的机器可处理承载方式包括：

1. 扩展 `PNML` 的系统模型。
2. 运行时 `RTM` 和 `Petri Net Engine`。
3. 降阶后的基础 `PNM`。
4. `TINA` 工具的 reachability graph、partial state space 和 trace。

### 交换与互操作

互操作是本文重心之一：

1. topics 被建模成广播 token 的 channel。
2. services 被建模成成对 request/response 通道。
3. signals 让非 Petri 外部组件也能作为可分析门控输入进入模型。
4. 生成的 ROS packages 把验证过的工作流与手写业务逻辑边界清晰分开。

## 配套基础设施

- 建模/编辑工具：`DiNeROS`、扩展 `PNML`。
- 解析/交换/元模型支持：`JastAdd`、`PNML`、ISO/IEC 15909。
- 仿真/执行支持：`Petri Net Engine`、自动生成的 ROS packages。
- 验证/分析支持：`TINA`、`sift`、`reduce`、`pathto` 与 Net Analyzer。
- 代码生成/转换支持：`Petri Net Splitter`、`Petri Net Flattener`、`Petri Net Package Generator`。
- 标准化或社区生态：依托 `ROS`、`PNML` 和 `TINA` 生态。

## 适用场景与需求前提

### 适用场景

适合结构复杂、节点分布式、通信显式、需要把工作流、通信和资源互斥一起建模的 ROS 机器人系统，尤其是工业协作和多部件协同控制。

### 需求前提

1. 应用可分解为有限 node nets 和显式 topics / services。
2. 关键逻辑可被 token 流和资源位置表达。
3. 开发团队愿意接受模型驱动的 package 生成和运行时约束。
4. 验证重点在消息丢失、死节点、互斥、信号门控等离散问题。

### 不适用或高成本场景

如果系统核心依赖高保真连续控制、复杂最优控制或极大规模状态空间，单靠基础 Petri 网与 partial state space 会很快吃紧。

## 与相邻形式主义的关系

相对 [formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，本文更强调结构/通信/工作流统一建模，而不是实时参数验证；相对 [modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，本文把 Petri 网推进到了完整 ROS 工具链与运行时层；相对 [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)，它不是轻量状态机库，而是更重的并发网式模型驱动验证框架。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常直接地说明：对于分布式机器人系统，如果需求里有“节点划分、topic/service 通信、共享资源、外部信号门控”，Petri 网可能比传统 FSM 更适合作为系统级目标形式主义。

### 作为目标形式主义还是中间表示

对分布式 ROS 应用，它可以直接作为目标形式主义；对一般控制系统状态机生成，它也适合作为并发通信层的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要识别 node、topic、service、resource 和 signal 五类对象。
2. 外部系统接口最好在模型层显式写成 signals，而不是只在代码里隐式读取。
3. 生成链应当把“可验证工作流”和“手写业务实现”分层隔离。

### 现实限制

真正的系统安全仍受手写 handlers / callbacks 影响；同时，状态空间增长仍是大规模应用上的主要瓶颈。

## 重要的相关工作

### 奠基或前身工作

1. 原文明确建立在标准 `Petri Nets`、`PNML` 与 `TINA` 之上。
2. 论文还回顾了既有 Petri-net-based ROS approaches 和 model-based ROS approaches。

### 同类型或同家族工作

1. 该文是作者之前 `DiNeROS` 工作的扩展版，强化了转换与分析能力。
2. topic/service/signal 三类交互对象的统一建模，是其和一般 ROS workflow 工具的主要差异。

### 标准 / 格式 / 工具链工作

1. `PNML` 是关键机读承载。
2. `TINA` 是核心验证后端。
3. `Petri Net Engine` 和 package generator 让模型真正落到 ROS 运行时。

### 与本研究关系最紧的工作

1. 它为 `project_1` 提供了一个很强的证据：模型本体、验证和运行时可以被同一种并发形式主义贯穿。
2. 对后续“生成-验证-修复”闭环，`SyM/RTM/PNM` 三层结构很有启发性。

## 文献分类总结

- 主类：🕸️
- 描述客体：🎛️
- 所属领域：🌡️
- 形式主义：`Distributed Petri Nets / DiNeROS`
- 论文角色：ROS 建模验证工具链 / 分布式 Petri 网应用
- 核心功能：统一描述 ROS 结构、通信和工作流，并落到可验证 / 可执行的 Petri 网链路
- 关键特性：node nets、topics/services、signals、PNML、TINA、runtime models
- 构造方式：`SyM -> RTM -> PNM` 模型驱动转换
- 基础设施：`DiNeROS`、`PNML`、`TINA`、`ROS`
- 适用场景：分布式 ROS 机器人应用、共享资源控制、消息与工作流协同验证
- 需求前提：系统结构和交互对象需可显式建模
- 状态：🟢
