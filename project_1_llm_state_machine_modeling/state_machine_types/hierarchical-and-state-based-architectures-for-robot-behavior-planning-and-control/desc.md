# 面向机器人行为规划与控制的层次化与状态式架构 / Hierarchical and State-based Architectures for Robot Behavior Planning and Control

## 基本信息

- 标题：Hierarchical and State-based Architectures for Robot Behavior Planning and Control
- 中文标题：面向机器人行为规划与控制的层次化与状态式架构
- 作者：Philipp Allgeuer，Sven Behnke
- 发表：*8th Workshop on Humanoid Soccer Robots, International Conference on Humanoid Robots (Humanoids)*，2013
- DOI：原文未给出
- 链接：https://www.ais.uni-bonn.de/~pallgeuer/papers/WorkshopHSR_2013_behaviours.pdf
- 形式主义：`State Controller Library / Behavior Control Framework`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：机器人行为控制框架 / `HFSM` 与 inhibition-based behavior architecture
- 工具/实现获取方式：原文明确给出 `State Controller Library` 与 `Behavior Control Framework` 项目页和开源代码入口，均为跨平台 `C++` 框架。
- 标准/格式获取方式：承载方式主要是 `C++` 类库、state controller、state queue、behavior layers、inhibition tree、virtual actuators/sensors 和 `ROS` 接口层；原文未给 XML/JSON 标准。

## 简报

这篇论文不是再发明一种新自动机，而是把机器人高层行为控制拆成两条互补基础设施线。`State Controller Library` 负责带参数的顺序状态队列与未来动作规划，`Behavior Control Framework` 负责多行为并发激活、层级组织和 inhibition-based 切换。作者明确把两者设计成可串联使用：底层动作序列用 `SC Library`，上层复杂行为竞争与协调用 `BC Framework`。

- 形式主义定位：机器人行为控制的运行时框架家族，而不是新的理论状态机本体。
- 构造方式简述：`SC Library` 以 state instances + state queue 组织顺序和规划；`BC Framework` 以 behaviors + layers + inhibition tree 组织并发和切换。
- 基础设施与场景简述：依托跨平台 `C++`、状态参数、行为层、虚拟 actuator/sensor、`ROS` interface layer，服务 humanoid soccer 与一般实时机器人行为控制。

```text
机器人任务需求 -> SC Library 顺序状态规划 / BC Framework 行为抑制层 -> C++ runtime + ROS interface -> 实时机器人控制
```

## 形式主义定义与核心对象

### 定义对象

论文实际上给出两套基础对象：

1. `SC Library` 的 state controller、state instances、state queue 与 state parameters。
2. `BC Framework` 的 behaviors、behavior layers、inhibition tree、virtual actuators/sensors 与 behavior manager。

### 核心抽象

对 `SC Library`，可保守整理为：

$$
SC = (S, s_0, Q, P, \delta)
$$

上式中的符号逐项解释如下：

1. `S` 是可绑定到 controller 的状态类型集合。
2. `s_0` 是初始状态实例。
3. `Q` 是动态维护的 state queue。
4. `P` 是 state parameters 集合，用于定制状态实例。
5. `\delta` 是由状态实例在运行时通过修改队列实现的后继关系。

论文把状态队列明确写成“desired future states”的有序列表，因此可进一步写成：

$$
Q_t = \langle \sigma_1,\ldots,\sigma_k \rangle
$$

其中：

1. `Q_t` 是时刻 `t` 的队列内容。
2. `\sigma_i` 是某个具体 state instance。
3. 这些实例是单次使用的，可带不同参数。

对 `BC Framework`，可保守整理为：

$$
BC = (\mathcal{L}, B, I, A, R)
$$

上式中的符号逐项解释如下：

1. `\mathcal{L}` 是 behavior layers 集合。
2. `B` 是 behaviors 集合。
3. `I` 是编译后的 inhibition tree。
4. `A` 是 virtual actuators/sensors 网络。
5. `R` 是 behavior manager 的 step routine。

### 一个最小例子与通俗解释

论文给了两个非常典型的最小例子。

对 `SC Library`：

1. 守门员开始时把 `Wait for Button`、`Walk to Pose`、`Monitor Ball` 三个状态实例压入队列。
2. 走到目标位后，系统不需要让 `Walk to Pose` 知道自己之后要做什么，因为后继状态已经排在队列里。
3. 若中途环境变化，当前状态可以清空或重排未来队列。

对 `BC Framework`：

1. `Search for Ball`、`Go Behind Ball`、`Kick Ball` 等 behaviors 同处一层。
2. 这些行为之间通过 chaining / non-chaining inhibitions 定义优先关系。
3. 当 `Kick Ball` 的前提满足时，它自动抑制走位行为；踢完后，走位行为又自动恢复。

通俗地说，`SC Library` 像“能提前排任务清单的状态机”，而 `BC Framework` 像“按当前情境动态压制或放行行为的竞争调度器”。

### 运行 / 接受 / 转移语义

`SC Library` 的顺序控制可保守写成：

$$
Q_{t+1} = \mathrm{update}(Q_t,\sigma_t)
$$

上式中的符号逐项解释如下：

1. `Q_t` 是当前队列。
2. `\sigma_t` 是当前执行的状态实例。
3. `\mathrm{update}` 表示状态实例对队列做的 push、prepend、clear、remove 或 reorder。
4. 这说明“状态转移”不再只是固定表，而是对未来状态序列的运行时编辑。

`BC Framework` 的抑制求精是论文中最有代表性的形式化点，可保守整理为：

$$
a_j' = a_j \cdot \prod_{i \in Inh(j)} (1-a_i)
$$

上式中的符号逐项解释如下：

1. `a_j` 是行为 `j` 请求的 activation level。
2. `Inh(j)` 是抑制行为 `j` 的行为集合。
3. `a_j'` 是经抑制传播后的真实 activation level。
4. 论文明确举例说明，若某行为激活度为 `0.7`，它会把被抑制行为的激活度乘以 `0.3`。

### 语义边界

边界也很清楚：

1. `SC Library` 不天然支持同层多基本行为并发激活。
2. `BC Framework` 适合中高复杂度控制，但并不替代细粒度顺序状态实现。
3. 两者都强调运行时效率和工程集成，而不是形式证明。
4. 目标是机器人行为控制，不是通用交换标准。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
| --- | --- | --- |
| `SC Library` 骨架 | `$SC = (S, s_0, Q, P, \delta)$` | 状态类型、队列、参数和队列更新共同定义顺序控制。 |
| 状态队列 | `$Q_t = \langle \sigma_1,\ldots,\sigma_k \rangle$` | 未来动作序列被显式维护。 |
| 队列更新 | `$Q_{t+1} = \mathrm{update}(Q_t,\sigma_t)$` | 当前状态能直接改写未来计划。 |
| `BC Framework` 骨架 | `$BC = (\mathcal{L}, B, I, A, R)$` | 行为层、抑制树和数据接口组成并发行为框架。 |
| 抑制求精 | `$a_j' = a_j \cdot \prod_{i \in Inh(j)} (1-a_i)$` | 真实激活度由抑制关系乘法求精得到。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
| --- | --- | --- |
| 状态 / 模式 | 很强 | `SC Library` 直接面向 `FSM/HFSM` 与状态实例。 |
| 事件 / 触发 | 中等支持 | `SC Library` 更偏控制循环与条件；`BC` 更偏持续激活度求精。 |
| 守卫 / 数据 | 强支持 | state parameters、virtual actuators/sensors 和条件激活都很关键。 |
| 层次 | 强支持 | `HFSM`、behavior layers 和可嵌套 controller 都存在。 |
| 并发 / 同步 | 强支持 | `BC Framework` 可同层多行为并发激活并加权聚合输出。 |
| 时间约束 | 强支持 | 两者都面向 timed loop / real-time control loop 设计。 |
| 连续动态 / 随机性 | 不支持本体、支持外接 | 连续控制由外部子系统承载，框架负责高层离散协调。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 重点是运行时控制、开源代码和系统集成。 |

### 形式化问题与性质

1. `SC Library` 的关键创新是把“后继状态”从静态转移表改成可运行时编辑的未来状态队列。
2. `BC Framework` 的关键创新是用 inhibition tree 和激活度乘法，把很多显式转移压缩成更紧凑的行为竞争机制。
3. 两套框架叠加后，既保留局部顺序，又保留全局并发和上下文切换能力。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 用 `C++` 定义状态类、行为类和参数结构。
2. 在 `SC Library` 中把状态绑定到 state controller。
3. 在 `BC Framework` 中声明 behavior layers、inhibitions 和数据接口。
4. 通过 `ROS` interface layer 接入机器人系统其他节点。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `C++` 状态类与行为类。
2. state queue 与 state parameters。
3. inhibition tree。
4. virtual actuators / sensors。
5. `ROS` interface layer。

### 交换与互操作

这条路线的互操作重点在于：

1. 两个框架都强调与现有机器人代码无缝集成。
2. `BC Framework` 通过 interface layers 可跨进程、跨 loop rate 工作。
3. `ROS` 接口层把行为控制器接进现有 topics / services 体系。

## 配套基础设施

- 建模/编辑工具：以 `C++` 框架代码为主，不依赖单独图形编辑器。
- 解析/交换/元模型支持：无独立交换标准，核心是状态/行为类与运行时对象骨架。
- 仿真/执行支持：跨平台 `C++` runtime、timed loop、`ROS` interface layer。
- 验证/分析支持：论文主打执行效率与结构清晰度，不主打 formal verification。
- 代码生成/转换支持：不是核心，重点是直接作为运行时框架使用。
- 标准化或社区生态：作者明确给出 `SC Library`、`BC Framework` 和 `NimbRo` 开源代码入口。

## 适用场景与需求前提

### 适用场景

适合 humanoid soccer、服务机器人、移动操作机器人等需要高层离散行为协调、局部动作序列规划和实时控制循环的场景。

### 需求前提

1. 系统已有稳定的低层感知和控制组件。
2. 高层行为可拆成离散状态或独立行为模块。
3. 团队接受 `C++` 框架式实现，而不是图形化 DSL。
4. 若使用 `BC Framework`，行为间优先关系能合理抽成 inhibition tree。

### 不适用或高成本场景

如果任务更适合纯行为树、纯规划器或需要强形式证明，这两套框架就不是最直接的入口。

## 与相邻形式主义的关系

相对 [ros-commander-behavior-creation-for-home-robots/desc.md](../ros-commander-behavior-creation-for-home-robots/desc.md)，本文更偏运行时框架骨架，而不是图形化 `HFSM` 行为编辑器；相对 [the-armarx-statechart-concept-graphical-programing-of-robot-behavior/desc.md](../the-armarx-statechart-concept-graphical-programing-of-robot-behavior/desc.md)，本文更轻量、更代码化，不强调分布式 statechart 编辑器；相对 [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)，本文更早、也更强调 queue planning 与 inhibition-based behavior control。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目提醒我们：面向机器人软件时，高层状态机不一定只是一张图，也可以落成带未来状态队列、行为抑制树和多 loop rate 接口的执行基础设施。

### 作为目标形式主义还是中间表示

它更适合作为工程执行载体，而不是通用中间表示。

### 对需求到模型生成的启发

1. 需求中的“先做 A，再做 B，若中途环境变化则改计划”非常适合 state queue 模式。
2. 需求中的“若条件 X 更紧急，则压制其他行为”很适合 inhibition tree 模式。
3. 生成系统若面向机器人运行时，最好同时生成数据接口和行为优先关系，而不是只生硬输出状态图。

### 现实限制

它高度工程化、强依赖 `C++/ROS` 代码组织，对标准化交换和形式验证支持较弱。

## 重要的相关工作

1. [ros-commander-behavior-creation-for-home-robots/desc.md](../ros-commander-behavior-creation-for-home-robots/desc.md)：图形化 `HFSM` 行为构建路线。
2. [rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md](../rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md)：更强 GUI 导向的机器人任务编排路线。
3. [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)：更现代、更轻量的 `ROS 2` 状态机运行时。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文核心贡献是两套可直接运行的机器人行为控制框架，明显属于运行时基础设施而不是单纯应用案例。
