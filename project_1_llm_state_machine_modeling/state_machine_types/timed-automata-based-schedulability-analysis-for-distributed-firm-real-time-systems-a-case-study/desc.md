# 面向分布式 firm 实时系统的基于定时自动机的可调度性分析：一个案例研究 / Timed-automata based schedulability analysis for distributed firm real-time systems: a case study

## 基本信息

- 标题：Timed-automata based schedulability analysis for distributed firm real-time systems: a case study
- 中文标题：面向分布式 firm 实时系统的基于定时自动机的可调度性分析：一个案例研究
- 作者：Thi Thieu Hoa Le，Luigi Palopoli，Roberto Passerone，Yusi Ramadian
- 发表：*International Journal on Software Tools for Technology Transfer*，15(3):211-228，2013
- DOI：`10.1007/s10009-012-0245-y`
- 链接：https://doi.org/10.1007/s10009-012-0245-y
- 形式主义：`Timed Automata / Distributed Firm RTS Schedulability Model`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：分布式实时系统可调度性分析 / 定时自动机应用建模
- 工具/实现获取方式：原文使用 `UPPAAL` 建模和 point-wise verification；未给单独公开仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata、shared variables、broadcast synchronisation 和 integer-clock encoding；无统一交换标准。

## 简报

这篇论文不是在提出新的时间自动机分支，而是在展示经典 `Timed Automata` 主干到底能不能吃下“工业复杂度”的分布式 firm 实时系统。作者用一个异构通信系统 `HCS` 案例，把 server、device、network medium、NAC、buffers 和 clock-synchronisation protocol 都压成 `TA` 网络，检查 buffer overrun、hard/firm deadline 和设计参数 `L_m, L_n` 的可行区间。

- 形式主义定位：这是经典 `Timed Automata` 在 distributed firm real-time system 上的高质量应用侧证，重点是“分布式通信 + firm deadline + schedulability region”。
- 构造方式简述：先把 server / device / medium / NAC / buffer 建成 `12` 个 timed automata，再在 `UPPAAL` 中加入 integer-clock 编码，对 `L_m, L_n` 做 point-wise feasibility verification。
- 基础设施与场景简述：依托 `UPPAAL`、PTP clock synchronisation、广播同步和缓冲区模型，服务工业嵌入式通信系统的可调度性分析。

```text
通信系统结构与时序参数 -> timed automata network -> deadline / buffer properties -> feasible (Lm, Ln) region
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. server、device、network medium、NAC 和 buffers。
2. PTP 同步消息 `S/F/DQ/DP/A` 及其优先级。
3. 状态机中的 clocks、shared variables 和 broadcast synchronisations。
4. 设计参数 `L_m` 与 `L_n`。
5. `Error` 位置、hard deadline 与 firm deadline 约束。

### 核心抽象

原文先给出 timed automata 的通用语义：位置集合 `L`、时钟集合 `X_c`、状态变量集合 `X_s`、带 guard/update 的边和 invariant。对本文系统，可保守写成：

$$
\mathcal{N}(L_m, L_n) = A_1 \parallel \cdots \parallel A_{12}
$$

上式中的符号逐项解释如下：

1. `A_1, \ldots, A_{12}` 是 server、device、medium、NAC、buffer 等 timed automata。
2. `L_m` 是 network medium 的处理延迟参数。
3. `L_n` 是 NAC 的处理延迟参数。
4. 并行组合后得到整套 distributed RTS 的时序模型。

论文把一个参数点 `(L_m, L_n)` 的可行性收束成是否能避免任何 `Error` 位置，可保守整理为：

$$
\mathrm{Feasible}(L_m, L_n) \iff A[]\, \neg \mathrm{Error}
$$

上式中的符号逐项解释如下：

1. `\mathrm{Error}` 统一代表 buffer overrun 或 deadline violation 等坏位置。
2. 若对所有执行都无法到达 `Error`，则该参数点是可行设计点。

论文还给出一个很有代表性的最坏音频延迟近似式：

$$
delay_{worst}^A \approx 10 \times P_a + 10 \times L_n + \left(10 \times P_a / P_s + 1\right) \times L_n
$$

这个式子用来解释为什么某些 `(L_m, L_n)` 点会使低优先级音频包违反 deadline。

### 一个最小例子与通俗解释

一个最小例子是低优先级音频包 `A` 的传输：

1. server 周期性产生音频消息并放入 buffer。
2. medium 总是优先发高优先级同步包和延迟应答包。
3. `A` 包如果在 medium 和 NAC 的队列里排太久，就会错过播放时间。
4. 一旦 device 上的 deadline-checker 发现 `t_play < current time`，自动机就进入 `Error`。

通俗地说，这个模型像“给整条分布式消息链都装上秒表”，然后问：在给定链路时延和处理时延下，最慢的那类消息还能不能准时到。

### 运行 / 接受 / 转移语义

原文强调两类同步：

1. regular synchronisation，需要发送和接收同时发生；
2. broadcast synchronisation，发送方总能发出，所有已使能的接收方同步接收。

系统模型中的消息流主要由 broadcast + shared variables 驱动。为了在 `UPPAAL` 中记录发送/到达时间，作者还引入 integer-clock encoding，把连续时钟值投影到整数时刻与奇偶日期位上。

论文的 point-wise verification 做法是：

1. 固定 `L_m` 与 `L_n`；
2. 检查系统是否走到 `Error`；
3. 将参数平面上的点标成 `+`、`×` 或 `□`，分别表示可行、deadline violation、buffer overrun。

### 语义边界

这篇论文也很诚实地展示了 `TA` 路线的边界：

1. `UPPAAL` 不能直接把 clock 值读到变量里，所以作者不得不引入 integer-clock encoding。
2. 参数分析主要是 point-wise 而非真正的符号参数综合。
3. 模型规模一大就需要离散化和额外编码技巧。
4. 它证明了经典 `TA` 仍有工业实用性，但不是说大规模异构系统就能无代价建模。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统网络 | `$\mathcal{N}(L_m, L_n) = A_1 \parallel \cdots \parallel A_{12}$` | 用多个 `TA` 组合分布式通信系统。 |
| 参数可行性 | `$\mathrm{Feasible}(L_m, L_n) \iff A[]\,\neg \mathrm{Error}$` | 以 `Error` 是否可达定义可调度区域。 |
| 最坏音频延迟 | `$delay_{worst}^A \approx 10 P_a + 10 L_n + (10 P_a/P_s + 1)L_n$` | 给出参数与 deadline 风险的近似关系。 |
| 死锁避免条件 | `$P_s \ge 3 L_m$` | 同步周期至少要容纳一对 `S/F` 包和等待时间。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | server、device、medium、NAC、buffer 都是显式自动机。 |
| 事件 / 触发 | 强支持 | packet release、arrival、transmission、deadline miss 都是核心事件。 |
| 守卫 / 数据 | 强支持 | guard、shared variables、queue 状态和整数时间变量广泛使用。 |
| 层次 | 不支持 | 模型主体是平面 network。 |
| 并发 / 同步 | 强支持 | 多组件通过 regular/broadcast sync 并发交互。 |
| 时间约束 | 强支持 | deadline、buffering delay、period、offset 都是一等对象。 |
| 连续动态 / 随机性 | 不支持 | 系统是离散通信时序模型。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 可直接做 schedulability/feasibility 检查。 |

## 构造方式与承载格式

### 建模入口

建模入口是：

1. 把系统组件切分成 server、device、medium、NAC、buffer 等模块。
2. 为每个模块编写 timed automaton。
3. 用 shared variables 和 broadcast synchronisation 连接消息流。
4. 在参数平面上逐点验证 `Error` 是否可达。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` timed automata templates。
2. 消息包结构体与共享变量。
3. integer-clock encoding。
4. reachability / safety 查询。

### 交换与互操作

互操作重点在：

1. 从系统结构图到 timed automata network 的模块化映射；
2. 从参数点验证结果回写到设计者可读的可行区区域图；
3. 在普通 `TA` 语义下兼容 distributed communication 与 firm deadlines。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：原文无统一交换标准，主要是 `UPPAAL` 模板。
- 仿真/执行支持：重心在验证而非运行时部署。
- 验证/分析支持：point-wise feasibility verification、deadline/buffer analysis。
- 代码生成/转换支持：原文未给代码生成。
- 标准化或社区生态：依托 `UPPAAL` 和工业实时时序验证工具线。

## 适用场景与需求前提

### 适用场景

适合分布式嵌入式通信系统、firm real-time system、带同步协议和多级缓冲的工业实时系统。

### 需求前提

1. 系统组件和消息流需要能拆成有限自动机。
2. 关键时序参数如处理延迟、周期、offset 需要明确。
3. 关注点是可调度性、deadline miss 与 buffer overrun。
4. 允许用 point-wise 方式探索设计参数空间。

### 不适用或高成本场景

若需求核心在连续物理动力学、概率网络拥塞或超大规模开放系统，这种经典 `TA` network 会快速面临状态膨胀。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文是标准 `TA` 主干的工业落地案例，没有再引入参数化、冻结时钟或博弈结构；相对 [Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata](../timed-verification-of-the-generic-architecture-of-a-memory-circuit-using-parametric-timed-automata/desc.md)，这里分析的是 grounded design points 而不是 `PTA` 参数综合；相对 [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)，两者都说明 `TA` 能处理工业复杂度，但本文更偏 distributed firm RTS 的通信时序和缓冲区分析。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：如果需求里已经有明确的通信链路、处理节点和 firm deadline，经典 `TA` 仍然是一个足够强、且工具成熟的目标后端。

### 作为目标形式主义还是中间表示

对 schedulability / response-time analysis 任务，它可以直接作为目标形式主义；对更高层控制需求，它也适合作为验证中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要把 packet type、buffer、priority、deadline 分开建模。
2. 若系统包含 clock synchronisation，必须提前决定是直接时钟语义还是整数编码近似。
3. 参数探索不一定都要走 `PTA`，point-wise verification 也是一种稳定工程路线。

### 现实限制

当系统规模扩大时，LLM 自动生成的模型如果不做模块化切分，会很容易超过工具的可验证边界。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文全部模型都建立在经典 `TA` 语义上。
- [Automatic Verification of Component-Based Real-Time CORBA Applications](../automatic-verification-of-component-based-real-time-corba-applications/desc.md)：同属工业复杂实时系统的 `TA` 应用线。
- [Timed Verification of the Generic Architecture of a Memory Circuit Using Parametric Timed Automata](../timed-verification-of-the-generic-architecture-of-a-memory-circuit-using-parametric-timed-automata/desc.md)：与本文形成 grounded analysis vs parameter synthesis 的对照。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：⏱️
- 形式主义：`Timed Automata / Distributed Firm RTS Schedulability Model`
- 论文角色：分布式实时系统可调度性分析 / 定时自动机应用建模
- 核心功能：分析 distributed firm RTS 在不同 `L_m, L_n` 下的 deadline 与 buffer 可行性
- 关键特性：modular TA network、broadcast sync、integer-clock encoding、point-wise feasibility map
- 构造方式：server/device/medium/NAC/buffer 自动机构造 + 参数点验证
- 基础设施：`UPPAAL`，原文未提供独立公开仓库
- 适用场景：分布式通信式嵌入式实时系统
- 需求前提：消息流、周期、延迟和 deadline 需可显式结构化
- 状态：🟢
