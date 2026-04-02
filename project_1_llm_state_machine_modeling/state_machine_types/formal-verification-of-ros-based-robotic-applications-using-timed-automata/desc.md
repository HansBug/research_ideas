# 使用定时自动机验证 ROS 机器人应用 / Formal Verification of ROS-Based Robotic Applications Using Timed-Automata

## 基本信息

- 标题：Formal Verification of ROS-Based Robotic Applications Using Timed-Automata
- 中文标题：使用定时自动机验证 ROS 机器人应用
- 作者：Raju Halder, Jose Proenca, Nuno Macedo, Andre Santos
- 发表：*2017 IEEE/ACM 5th International FME Workshop on Formal Methods in Software Engineering (FormaliSE)*, 2017
- DOI：`10.1109/FormaliSE.2017.9`
- 链接：https://doi.org/10.1109/FormaliSE.2017.9
- 形式主义：`Timed Automata Network for ROS Communication`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：ROS 通信验证 / 定时自动机应用建模
- 工具/实现获取方式：原文直接分析公开的 `Kobuki` ROS 源码，并使用 `UPPAAL` 建立 timed automata 模型；Kobuki 仓库入口在文中给出，`UPPAAL` 模型在附录中展开。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata、ROS publisher/subscriber queues、callback queue 和 timeout 参数；没有单独交换标准。

## 简报

这篇论文关心的是 ROS 应用里的“通信参数什么时候会把机器人搞坏”。作者不是从任务级状态机入手，而是直接把 ROS 节点、topic 队列、callback queue、`spinOnce`、传输时延和 callback 执行时间压成 timed automata network，然后用 `UPPAAL` 检查 queue overflow、传感器消息丢失和高优先级控制器长期饿死低优先级控制器等问题。

- 形式主义定位：它属于 `Timed Automata` 应用条目，核心对象是 ROS 通信与处理时序，而不是新的 ROS DSL。
- 构造方式简述：从源码提取发布周期、`spin` 周期、传输延迟、callback 时间和 queue size 等参数，再映射成发布者、订阅者、信道、队列和 callback queue 的 timed automata。
- 基础设施与场景简述：工具链是 `ROS` + `UPPAAL`，案例是 `Kobuki` 的 Safety Controller 与 Multiplexer。

```text
ROS source code + queue/time parameters -> timed automata network -> UPPAAL queries -> queue safety / message loss / starvation diagnosis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. ROS 中的 publisher、subscriber、channel 和 callback queue。
2. 发布周期、`spinOnce` 周期、信道传输时间和 callback 执行时间。
3. 队列容量与溢出语义。
4. `Kobuki` 的 SafetyController 与 Multiplexer。
5. 用 `UPPAAL` 表达的安全性、可达性和 leadsto 性质。

### 核心抽象

原文先给出 clock constraint 的文法：

$$
g ::= true \mid x \sim n \mid x-y \sim n \mid g \land g
$$

上式中的符号逐项解释如下：

1. `$x,y \in C$` 是时钟变量。
2. `$n \in \mathbb{N}$` 是常数。
3. `$\sim \in \{>, \ge, =, <, \le\}$` 是比较关系。
4. `$g \land g$` 表示多个时钟约束的合取。

Timed automaton 本体被定义为：

$$
TA = \langle L, l_0, \Sigma, C, T, Inv \rangle
$$

上式中的符号逐项解释如下：

1. `$L$` 是位置集合。
2. `$l_0$` 是初始位置。
3. `$\Sigma$` 是动作字母表。
4. `$C$` 是时钟集合。
5. `$T \subseteq L \times CC(C) \times \Sigma \times 2^C \times L$` 是转移集合。
6. `$Inv : L \to CC(C)$` 为每个位置赋予不变式。

对 ROS 场景，论文实际建模的是一个 timed automata network。可保守整理为：

$$
\mathcal{N}_{ROS} = \langle \{P_i\}, S, Ch, Q, CBQ, \theta \rangle
$$

上式中的符号逐项解释如下：

1. `$\{P_i\}$` 是发布者和订阅者节点的 automata。
2. `$S$` 是订阅者 `spinOnce` 调度 automaton。
3. `$Ch$` 是 topic 传输信道 automaton。
4. `$Q$` 表示 publisher / subscriber queues。
5. `$CBQ$` 是 callback queue automaton。
6. `$\theta$` 收纳发布周期、`spin` 周期、传输上下界和 callback 时间等参数。

### 一个最小例子与通俗解释

论文先用一个 sender/receiver 小例子讲 timed automata，然后再落到 ROS：

1. 发送端每隔一段时间发 `send!`。
2. 接收端在满足时间约束后通过 `send?` 收到消息。
3. 两边再通过 `ack!/ack?` 同步完成一次交互。
4. 在 ROS 场景里，只要把 sender/receiver 替换成 publisher、channel、subscriber queue 和 callback queue，就得到完整的通信网络。

通俗地说，这个模型像一个“把 ROS 消息栈拆开来看”的时序状态机：消息先放进发布队列，再经过 topic 通道，再进入订阅队列，再进 callback queue，最后才被 `spinOnce` 真正处理。

### 运行 / 接受 / 转移语义

论文把 timed automata 的运行语义写成“位置 + 时钟 + 同步动作”。对单个 automaton，可保守写成：

$$
(l, \nu) \xrightarrow{d} (l, \nu + d)
$$

$$
(l, \nu) \xrightarrow{a} (l', \nu[C := 0])
$$

上式中的符号逐项解释如下：

1. `$l,l'$` 是源/目标位置。
2. `$\nu$` 是当前时钟赋值。
3. `$d$` 是时间延迟，要求当前位置不变式在整个延迟期间成立。
4. `$a$` 是同步动作，如 `publish!`、`spinOnce!`、`getMsgs!`。
5. `$\nu[C := 0]$` 表示对被 reset 的时钟清零。

论文在 ROS 场景上最直接检查的是队列不溢出：

$$
Pr_1: A[] \neg Q_{1!1}.Overflow
$$

$$
Pr_2: A[] \neg Q_{2!1}.Overflow
$$

$$
Pr_3: A[] \neg Q_{3\,1}.Overflow
$$

上式中的符号逐项解释如下：

1. `$A[]$` 表示所有执行路径上始终成立。
2. `$Q_{1!1}, Q_{2!1}, Q_{3\,1}$` 分别是两个 publisher queue 与一个 subscriber queue。
3. `Overflow` 表示队列已满且发生替换旧消息的错误位置。

在 `Kobuki` 上，论文又写出两类代表性性质：

$$
WheelLeft:on \land SafetyControllerUpdate:spinLoc \leadsto wheel\_leftdropped
$$

$$
E<> RandomCmdVelCallback:PassMsg
$$

上式中的符号逐项解释如下：

1. 第一个式子表示：左轮下坠信号出现并触发一次 `spinOnce` 后，系统最终必须把对应状态变量置真。
2. 第二个式子表示：存在某条执行路径，使 `RandomWalker` 的速度消息真正穿过 Multiplexer 并传给底盘。

### 语义边界

这篇论文的边界主要有四点：

1. 它建模 ROS 通信与调度，不建模底盘连续动力学。
2. 物理动作被抽成消息和 callback 效果，不分析控制律本身正确性。
3. 关键参数来自静态代码阅读，当前抽取过程并未自动化。
4. 模型更适合抓“通信/时序导致的系统性 bug”，而不是复杂任务语义错误。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 时钟约束 | `$g ::= true \mid x \sim n \mid x-y \sim n \mid g \land g$` | 消息处理与传输时间由时钟守卫表达。 |
| 定时自动机 | `$TA = \langle L, l_0, \Sigma, C, T, Inv \rangle$` | ROS 构件最终被压成 timed automata。 |
| 队列安全 | `$A[] \neg Q.Overflow$` | 检查给定参数下队列是否会溢出。 |
| 传感器可达性 | `$WheelLeft:on \land spinLoc \leadsto wheel\_leftdropped$` | 轮下坠传感器消息不能在队列中被悄悄覆盖。 |
| 控制指令活性 | `$E<> RandomCmdVelCallback:PassMsg$` | 低优先级控制器的消息是否还能传到底盘。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 发布者、订阅者、队列、callback queue 都是显式 automata。 |
| 事件 / 触发 | 强支持 | `publish!/?`、`spinOnce!/?`、`getMsgs!/?` 等同步动作是一等对象。 |
| 守卫 / 数据 | 强支持 | guard 里直接编码队列容量、时间窗口和优先级。 |
| 层次 | 部分支持 | 组件级分层明显，但核心仍是平面 timed automata network。 |
| 并发 / 同步 | 强支持 | 多 publisher、多 queue、多 callback 通过同步动作并发运行。 |
| 时间约束 | 强支持 | 发布周期、超时、callback 时间和传输延迟全是主体。 |
| 连续动态 / 随机性 | 不支持 | 不处理连续动力学与概率行为。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 直接检查多类实时性质。 |

### 形式化问题与性质

1. 论文的关键贡献是把 ROS 的“中间件参数”变成可验证的时序对象。
2. queue overflow 在这里不是实现细节，而是 timed automata 中的显式错误状态。
3. `Kobuki` 案例说明，高优先级控制器和 timeout 组合可能让低优先级控制器永久饿死。
4. 对 `Timed Automata` 主干来说，这篇论文展示了从机器人中间件源码到 timed model 的一条工程化路线。

## 构造方式与承载格式

### 建模入口

建模步骤可以概括为：

1. 从 ROS 源码抽取发布周期、`spin` 周期、queue size、timeout 和 callback 时间。
2. 为 publisher、subscriber、channel、queue 和 callback queue 分别建 timed automata。
3. 用同步动作把消息流链接起来。
4. 在 `UPPAAL` 中写查询，搜索参数空间里的坏组合。

### 机器可处理承载方式

原文使用的承载方式包括：

1. `UPPAAL` timed automata templates。
2. 表示队列容量和 callback 数量的内部变量。
3. 表示传输和处理时延的时钟。
4. 表示安全性和活性要求的 `TCTL` / `UPPAAL` 查询。

### 交换与互操作

互操作重点不是标准交换格式，而是“ROS 源码参数 -> timed model”的映射：

1. ROS topic 和 callback 机制被重写为同步动作。
2. `callAvailable()` 和 `spinOnce()` 被建模成独立 automata。
3. `Kobuki` 公开源码提供了参数来源，`UPPAAL` 提供验证后端。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：参数来自 ROS 源码静态分析，原文未提供通用元模型。
- 仿真/执行支持：依赖真实 ROS / Kobuki 软件栈。
- 验证/分析支持：`UPPAAL`，检查 queue safety、消息丢失和控制活性。
- 代码生成/转换支持：原文没有自动代码生成，但给出了从源码参数到 automata 的建模方法。
- 标准化或社区生态：依托 `ROS` 和 `UPPAAL` 两条成熟生态。

## 适用场景与需求前提

### 适用场景

适合 ROS 机器人应用中那些“通信栈参数本身就可能导致系统异常”的场景，尤其是多 topic、多 callback、有限队列和优先级控制混合的系统。

### 需求前提

1. 应用采用类似 ROS 的明确 topic / callback / queue 架构。
2. 关键时序参数可从源码或配置中抽取。
3. 风险可以被表达成 queue overflow、消息丢失、超时或 starvation。
4. 系统行为能接受有限状态 + 时钟抽象。

### 不适用或高成本场景

若系统的主要风险来自连续动力学、感知算法精度或复杂分布式数据语义，而不是消息调度和时序参数，这种 timed automata 抽象就不够。

## 与相邻形式主义的关系

相对 [a-theory-of-timed-automata/desc.md](../a-theory-of-timed-automata/desc.md)，本文不是理论定义，而是 ROS 中间件级落地；相对 [timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md](../timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md)，它建模的不是日志窗口，而是软件通信路径；相对 [modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，两者都关注实时通信，但本文更强调机器人应用中的 queue / callback 行为。

## 与本研究的关系

### 对 Project 1 的价值

它说明：如果未来要从需求自动生成控制模型，仅仅生成任务级状态机不够，还要能把运行时通信约束、队列容量和 timeout 一并建模。

### 作为目标形式主义还是中间表示

对实时通信与中间件参数验证，它可以直接作为目标形式主义；对一般机器人控制任务，它更适合作为“执行平台时序约束”的中间表示。

### 对需求到模型生成的启发

1. 需求抽取应当覆盖 message rate、queue size、timeout、callback time 等非功能时序要素。
2. ROS 式系统的 bug 很多来自通信层，而不是显式任务状态遗漏。
3. 如果要闭环到验证，`UPPAAL` 风格的 timed automata 是很自然的后端。

### 现实限制

当前方法仍需人工从源码提取参数，且对真实机器人动力学和感知误差没有直接保证。

## 重要的相关工作

### 奠基或前身工作

1. 原文直接建立在 timed automata 与 `UPPAAL` 上。
2. 文中回顾了用 `SPIN` 验证 `Care-O-bot` 等机器人系统的相关尝试。

### 同类型或同家族工作

1. 文章把 ROS 应用验证和实时参数分析结合起来，而不是只做高层决策规则验证。
2. 它和工业协议、SCADA 攻击检测等 timed automata 应用同属“从具体系统抽象出可验证时间模型”的路线。

### 标准 / 格式 / 工具链工作

1. `UPPAAL` 是核心验证工具。
2. `ROS` / `Kobuki` 是核心应用与实现载体。

### 与本研究关系最紧的工作

1. 它提示 `project_1` 后续若面向 ROS/CPS 落地，需要把平台通信状态也纳入状态机抽取范围。
2. 它提供了“需求参数 -> timed model -> 性质查询”的完整实例。

## 文献分类总结

- 主类：⏱️
- 描述客体：🎛️
- 所属领域：🌡️
- 形式主义：`Timed Automata Network for ROS Communication`
- 论文角色：ROS 通信验证 / 定时自动机应用建模
- 核心功能：把 ROS 节点通信、队列和 callback 时序压成可验证的 timed automata network
- 关键特性：显式队列、同步动作、时钟约束、`UPPAAL` 查询、参数敏感验证
- 构造方式：源码参数抽取 + `UPPAAL` timed automata templates
- 基础设施：`ROS`、`Kobuki`、`UPPAAL`
- 适用场景：机器人中间件时序分析、queue safety、priority starvation 检查
- 需求前提：topic / callback 结构明确，关键时序参数可提取
- 状态：🟢
