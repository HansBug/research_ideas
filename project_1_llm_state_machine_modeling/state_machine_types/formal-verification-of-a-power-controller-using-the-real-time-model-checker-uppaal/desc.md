# 使用实时时间模型检查器 UPPAAL 形式化验证电源控制器 / Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL

## 基本信息

- 标题：Formal Verification of a Power Controller Using the Real-Time Model Checker UPPAAL
- 中文标题：使用实时时间模型检查器 UPPAAL 形式化验证电源控制器
- 作者：Klaus Havelund，Kim Guldstrand Larsen，Arne Skou
- 发表：收录于 *Formal Methods for Real-Time and Probabilistic Systems*，pp. 277-298，1999
- DOI：`10.1007/3-540-48778-6_17`
- 链接：https://doi.org/10.1007/3-540-48778-6_17
- 形式主义：`Timed Automata / UPPAAL Network for Power-Down Controller Verification`
- 主类：⏱️ 时间/时钟自动机
- 对象类型：🧪 应用/案例
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：⏱️ 实时与嵌入式系统
- 论文角色：工业实时控制器案例 / `UPPAAL` 定时自动机应用建模
- 工具/实现获取方式：原文直接基于 `UPPAAL` 建模并验证 B&O 的电源控制协议，使用 observer、flag、auxiliary variable 等技巧表达性质；论文未提供独立公开代码仓库。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、共享变量、channels 与查询公式；原文未给统一交换标准。

## 简报

这篇论文是 `UPPAAL` 早期最典型的工业应用之一。对象不是抽象协议教材，而是 Bang & Olufsen 音视频设备中的 power-down controller。系统必须在数据链路空闲时进入待机、在有数据或中断到来时安全唤醒，同时还不能丢失 link interrupts。作者把 IOP、drivers、interrupt handlers、Timer 和 environment 都压成 `UPPAAL` 网络，并专门设计了“单处理器 time slicing + timed transitions + prioritized interrupts”的建模技巧。最终验证不仅确认了部分设计，还直接找出 3 个设计错误，并逼出了中断频率上界。

- 形式主义定位：这是 `Timed Automata` 主干上的应用型条目，重点不是提出新 automata 家族，而是展示如何把硬实时控制协议稳地落成 `UPPAAL` 可检模型。
- 构造方式简述：把 IOP、driver、interrupt handler 等离散控制过程建成 timed automata，用 Timer 模板累积时间消耗，再用优先级变量 `cur` 模拟中断抢占。
- 基础设施与场景简述：依托 `UPPAAL`、observer 模板、flag/debt 变量和工业电源管理协议，服务于硬实时嵌入式控制、低功耗唤醒和中断安全分析。

```text
power-down protocol rules + timed transitions + interrupt priorities -> UPPAAL automata network -> reachability / safety checks -> design errors and interrupt-frequency bound
```

## 形式主义定义与核心对象

### 定义对象

论文里的核心对象包括：

1. `UPPAAL` timed automata network。
2. 表示时间消耗的 Timer automaton。
3. IOP、driver、interrupt handler 与 interrupt generator 等组件自动机。
4. 共享整型变量和 clocks。
5. 用于性质验证的 observer、flag 与 debt 变量技巧。

### 核心抽象

论文虽然以 `UPPAAL` 图形模型为主，但其单个 automaton 可保守整理为：

$$
A = \langle L, l_0, C, \Sigma, E, Inv \rangle
$$

上式中的符号逐项解释如下：

1. `L` 是离散位置集合。
2. `l_0 \in L` 是初始位置。
3. `C` 是 clocks 集合。
4. `\Sigma` 是同步动作集合，如 `a! / a?` 这类 channel 同步。
5. `E` 是带 guards、同步动作、reset 和赋值的迁移集合。
6. `Inv` 是位置不变式，限制在某位置允许停留的最长时间。

论文中的系统是多个 automata 的并行组合，可保守写成：

$$
\mathcal{N} = A_{Timer} \parallel A_{IOP} \parallel A_{LSL\ Driver} \parallel A_{AP\ Handler} \parallel A_{LSL\ Handler} \parallel A_{IntGen} \parallel \cdots
$$

上式中的符号逐项解释如下：

1. `A_{Timer}` 负责把“某条边要消耗多少时间”转成可同步的时间推进机制。
2. `A_{IOP}` 是主电源控制逻辑。
3. 其他 automata 分别代表外设驱动、中断处理器和环境输入。
4. `\parallel` 表示 `UPPAAL` 中按 channels 和共享变量组合的 timed automata network。

为了在单处理器上表达 time slicing，论文专门引入 Timer 组件，并验证了如下时间累积性质：

$$
A[]\ ((A.d \land B.d) \Rightarrow (19 \le gc \land gc \le 24))
$$

以及带中断版本：

$$
A[]\ ((A.d \land B.d \land Interrupt.d) \Rightarrow (26 \le gc \land gc \le 31))
$$

上式中的符号逐项解释如下：

1. `A[]` 表示所有可达状态上恒成立。
2. `A.d`、`B.d`、`Interrupt.d` 表示相应 automata 已到达“时间全部消耗完成”的结束位置。
3. `gc` 是从不复位的全局时钟。
4. 第一式验证无中断时总耗时区间。
5. 第二式验证加入中断后总耗时区间。

论文还强调 `UPPAAL` 基本查询形式：

$$
A[]\ p \qquad E\Diamond p
$$

上式中的符号逐项解释如下：

1. `A[] p` 表示所有可达状态都满足性质 `p`。
2. `E\Diamond p` 表示存在一条执行最终达到满足 `p` 的状态。
3. 当原始自然语言性质不能直接写成这两种形式时，作者通过 observer、flag 或 debt 变量把它们转写成可检目标。

### 一个最小例子与通俗解释

论文先用一个简化示例解释建模技巧：

1. 两个进程 `A` 和 `B` 共用一个处理器，它们的边各自需要消耗 `2`、`5`、`7-12` 等时间。
2. 如果没有中断，Timer 负责在各进程之间切换并累计全局耗时。
3. 如果出现 interrupt handler，则通过变量 `cur` 提高中断处理器优先级，禁止低优先级进程继续前进。
4. 然后用 `A[] ...` 性质检查总时长和是否出现坏情况。

通俗地说，这像“把软件调度器、中断控制器和业务状态机一起搬进同一张 timed automata 图里，再让 `UPPAAL` 穷举所有可能抢占顺序”。这比手工估 worst-case interrupt trace 更稳，因为异常 interleaving 也会被系统枚举到。

### 运行 / 接受 / 转移语义

论文直接解释了 `UPPAAL` 的两类状态迁移：

1. delay transitions：
   - 只要当前位置 invariant 没被破坏，时间就可以流逝。
   - 所有 clocks 同步增加。
2. action transitions：
   - 当 guards 成立且同步条件满足时，对应边被触发。
   - 触发时会执行 clock resets 和整数变量赋值。

若某节点被标为 committed，则：

1. 该状态下不允许继续延时。
2. 下一步 action transition 必须涉及被 committed 的组件。
3. 这就能稳定表达“必须原子地连走几步”的协议片段。

### 语义边界

这篇论文的边界主要在于：

1. 模型主要是离散实时协议层，不含连续物理动力学。
2. 时间消耗是通过 Timer 组件显式编码的，而不是语言原生带 duration edge。
3. 中断优先级通过共享变量 `cur` 建模，属于工程化编码技巧。
4. 论文目标是验证控制协议逻辑，不是生成可执行控制器代码。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单个 timed automaton 骨架 | `$A = \langle L, l_0, C, \Sigma, E, Inv \rangle$` | 表达 guard、同步、重置和不变式。 |
| 网络组合 | `$\mathcal{N} = A_{Timer} \parallel A_{IOP} \parallel \cdots$` | 把 power-down controller 与环境并起来。 |
| 全局安全性质 | `$A[]\ p$` | 所有可达状态都满足性质 `p`。 |
| 可达性性质 | `$E\Diamond p$` | 某坏/好状态是否可达。 |
| 无中断总时长检查 | `$A[] ((A.d \land B.d) \Rightarrow (19 \le gc \land gc \le 24))$` | 验证 time slicing 下的总时延区间。 |
| 含中断总时长检查 | `$A[] ((A.d \land B.d \land Interrupt.d) \Rightarrow (26 \le gc \land gc \le 31))$` | 验证 interrupt priority 加入后的总时延区间。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | standby、active、check interrupts 等阶段都被显式建模。 |
| 事件 / 触发 | 强支持 | 数据到达、中断产生、唤醒/休眠命令都是核心事件。 |
| 守卫 / 数据 | 强支持 | guards、共享变量和 aux variables 一起使用。 |
| 层次 | 不支持 | 主体是并行 network，不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多 automata 通过 channels 与共享变量并行同步。 |
| 时间约束 | 强支持 | clocks、invariants、Timer 组件和全局时钟是核心。 |
| 连续动态 / 随机性 | 不支持 | 完全是离散实时系统。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 直接支持 reachability 和 safety 验证。 |

### 形式化问题与性质

1. 作者解决的不是“怎么发明 timed automata”，而是“怎样把工业协议里真正麻烦的 timed transitions 和 interrupts 编成 timed automata”。
2. Observer 技巧把许多非局部自然语言需求压回 `A[] not bad` 这种 `UPPAAL` 可接受形式。
3. 论文最终发现 3 个设计错误，并指出必须限制 AP interrupt 频率，这说明模型不是装饰，而是真改设计。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先整理协议规则和组件交互。
2. 给 IOP、driver、interrupt handlers、environment 分别画 automata。
3. 用 Timer 模板表达 time-consuming transitions 和单处理器 time slicing。
4. 用 `cur` 变量表达中断抢占优先级。
5. 把自然语言性质翻成 `UPPAAL` 查询、observer 或辅助变量检查。

### 机器可处理承载方式

原文直接使用的机器可处理承载方式包括：

1. `UPPAAL` automata network。
2. channels、committed states、urgent channels。
3. clocks 与 shared integers。
4. `A[]` / `E<>` 查询和 observer automata。

### 交换与互操作

互操作重点在：

1. Timer automaton 如何和业务 automata 同步，确保 duration 被精确消耗。
2. interrupt handlers 如何通过共享优先级变量打断其他进程。
3. observer 如何把跨多个节点的时序性质编进统一状态空间。

## 配套基础设施

- 建模/编辑工具：`UPPAAL` 图形建模与模拟界面。
- 解析/交换/元模型支持：原文直接使用 `UPPAAL` 模型与查询语言，无额外交换格式。
- 仿真/执行支持：支持模型级仿真与 diagnostic trace 可视化。
- 验证/分析支持：支持 reachability、safety、observer-based checking。
- 代码生成/转换支持：原文未给自动代码生成链。
- 标准化或社区生态：依托 `UPPAAL` 与实时系统验证生态。

## 适用场景与需求前提

### 适用场景

适合有硬实时预算、单处理器调度、优先级抢占和中断安全要求的嵌入式控制协议。

### 需求前提

1. 系统关键逻辑能抽成有限控制状态。
2. 时间需求可写成 guards、invariants 或 duration 区间。
3. 中断和调度策略可通过有限优先级变量表达。
4. 目标是验证协议安全性，而非连续控制性能。

### 不适用或高成本场景

如果系统核心难点在连续动力学、概率故障或海量数据路径，单纯 `UPPAAL` 协议抽象会过于粗粒度。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文是典型工业落地案例；相对 [Timed Automata Approach to CAN Verification](../timed-automata-approach-to-can-verification/desc.md)，这里的重点是单处理器 power-down protocol 与 interrupts，而不是总线仲裁；相对 [Formal Verification of ROS-Based Robotic Applications Using Timed-Automata](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)，这里更靠近早期嵌入式协议验证而不是现代机器人中间件。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求里出现“某中断不能丢”“进入 standby 前必须完成某检查”“总耗时不能超界”时，生成的状态机不仅要含 clocks，还要显式保留调度和优先级。

### 作为目标形式主义还是中间表示

对硬实时协议验证，它可以直接作为目标形式主义；对更大控制系统，它也适合作为中间实时验证模型。

### 对需求到模型生成的启发

1. 自然语言里的 interrupt、priority、standby、wake-up 规则可以稳定落成 timed automata network。
2. 非局部时序需求往往需要 observer 或辅助变量，不应只指望局部 guard。
3. “时间消耗发生在 transition 上”并不妨碍生成 timed automata，只要额外引入 Timer 模板。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：定时自动机奠基条目。
- [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：工业通信协议上的 `UPPAAL` 应用。
- [Timed Automata Approach to CAN Verification](../timed-automata-approach-to-can-verification/desc.md)：总线时序与 deadline 分析。
- [Formal Verification of ROS-Based Robotic Applications Using Timed-Automata](../formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md)：机器人中间件时序验证。

## 文献分类总结

- 这是一篇 `⏱️` 类应用型条目，核心价值是展示了 `UPPAAL` 如何处理工业控制协议中的 timed transitions 和 prioritized interrupts。
- 它描述的是 power controller 这种反应式控制逻辑，因此记为 `🎛️`；研究语境是硬实时嵌入式系统，因此记为 `⏱️`。
- 对 `project_1` 来说，这篇论文最有价值的地方在于它证明了：中断、调度、待机/唤醒规则完全可以进入状态机模型，而不是只能留在实现层。
