# YASMIN：面向 ROS 2 的另一套状态机库 / YASMIN: Yet Another State MachINe library for ROS 2

## 基本信息

- 标题：YASMIN: Yet Another State MachINe library for ROS 2
- 中文标题：YASMIN：面向 ROS 2 的另一套状态机库
- 作者：Miguel Ángel González-Santamarta, Francisco Javier Rodríguez-Lera, Camino Fernández-Llamas, Francisco Martín Rico, Vicente Matellán Olivera
- 发表：2022 年短文 / 预印本（当前 `paper.pdf` 为 arXiv 版本；后续版本发表于 *ROBOT2022: Fifth Iberian Robotics Conference*）
- DOI：`10.1007/978-3-031-21062-4_43`
- 链接：https://arxiv.org/abs/2205.13284
- 形式主义：`YASMIN`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`ROS 2` 状态机库 / 运行时载体
- 工具/实现获取方式：原文明确给出 `YASMIN` GitHub 仓库、Python/C++ 实现和 web viewer。
- 标准/格式获取方式：承载方式是 `ROS 2` 中的 Python/C++ API、hierarchical state machine、shared blackboard 与 web viewer；原文未给 XML/JSON 标准。

## 简报

`YASMIN` 解决的是 `ROS 2` 时代的一个空缺：`ROS 1` 里有 `SMACH`、`SMACC`，但 `ROS 2` 缺少足够直接、足够轻量的状态机库。它的设计重点不是重新讨论状态机理论，而是给机器人开发者一个原生支持 `ROS 2`、同时兼顾 Python/C++、黑板共享和可视化调试的 `FSM/HFSM` 库。

- 形式主义定位：面向 `ROS 2` 机器人行为设计的 `FSM/HFSM` library，而不是新的通用形式化语言。
- 构造方式简述：以 state、transition、nested state machine 和 shared blackboard 组织行为，再辅以默认状态与 web viewer。
- 基础设施与场景简述：依托 Python/C++ library、GitHub 仓库、viewer 与 `MERLIN2` 集成，服务导航、waypoint checking、planner executor 等 `ROS 2` 机器人行为层。

```text
ROS 2 行为需求 -> YASMIN states / transitions / nested state machines -> shared blackboard + viewer -> ROS 2 actions / services / task execution
```

## 形式主义定义与核心对象

### 定义对象

`YASMIN` 的建模对象很直接：

1. state：执行某个动作或调用某个下层系统。
2. transition：基于 outcome 在 states 间跳转。
3. nested state machine：把复杂行为分层组织。
4. blackboard：在 states 与 nested state machines 之间共享数据。

### 核心抽象

论文没有给严格数学定义，这里根据文中对 `FSM/HFSM`、blackboard 和 nested state machines 的描述做保守整理：

$$
Y = (S, s_0, T, B, O, H)
$$

上式中的符号逐项解释如下：

1. `S` 是 state 集合。
2. `s_0 \in S` 是初始 state。
3. `T \subseteq S \times O \times S` 是基于 outcome 的 transition 关系。
4. `B` 是 shared blackboard。
5. `O` 是 outcomes 集合。
6. `H` 表示 nested state machines 的层次关系。

单个 state 的执行可保守写成：

$$
\mathrm{exec}(s, B) = (o, B')
$$

其中：

1. `s` 是当前 state。
2. `B` 是进入该 state 时的 blackboard。
3. `o \in O` 是 state 返回的 outcome。
4. `B'` 是 state 执行后更新过的 blackboard。

下一状态选择则是：

$$
T(s, o) = s'
$$

这表示当前 state 返回 outcome `o` 后，运行时转到下一 state `s'`。对 nested state machine 而言，blackboard 继续共享而不是复制。

### 一个最小例子与通俗解释

论文给出的 viewer 示例里，一个机器人行为被拆成几个状态机：

1. `NAVIGATION` 状态机负责导航。
2. `CHECK WP` 状态机负责 waypoint 检查。
3. `MERLIN2 EXECUTOR` 状态机负责计划执行。
4. 更上层的 `EMO2NODE` 负责高层目标，例如“检查 1 号 waypoint”。
5. 所有这些状态机通过黑板共享数据，并能在 viewer 中观察当前执行位置。

通俗地说，`YASMIN` 让开发者可以把“导航、检查点、执行计划、生成目标”这些部分都写成一层层嵌套的状态机，而不是把所有逻辑塞在一个 ROS node 里。

### 运行 / 接受 / 转移语义

`YASMIN` 的运行时核心可以压成：

$$
(s, B) \xrightarrow{} (T(s,o), B')
\quad \text{if } \mathrm{exec}(s,B)=(o,B')
$$

上式中的符号逐项解释如下：

1. `s` 是当前 state。
2. `B` 是当前 blackboard。
3. `\mathrm{exec}(s,B)` 返回 outcome `o` 和更新后的 `B'`。
4. `T(s,o)` 给出下一个 state。
5. 整个控制流仍是典型 outcome-driven state machine。

对层次状态机，论文强调 nested state machines 与 states 共享 blackboard，因此可保守写成：

$$
B_{\mathrm{child}} = B_{\mathrm{parent}}
$$

这表示子状态机与父状态机默认共享同一黑板语义，而不是做独立上下文复制。

### 语义边界

`YASMIN` 的边界也很清楚：

1. 它是 `ROS 2` library，不是严格的形式语义论文。
2. 它强调开发便利性和集成，而不是 formal verification。
3. 时间与连续动态依赖外部 `ROS 2` 节点和系统实现。
4. 它主要解决“如何实现和调试机器人行为层”而不是“如何证明模型正确”。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 库骨架 | `$Y = (S, s_0, T, B, O, H)$` | `YASMIN` 同时组织 state、transition、blackboard 和层次结构。 |
| state 执行 | `$\mathrm{exec}(s,B)=(o,B')$` | 当前状态读写黑板并返回 outcome。 |
| outcome 转移 | `$T(s,o)=s'$` | outcome 决定后继状态。 |
| 黑板共享 | `$B_{\mathrm{child}}=B_{\mathrm{parent}}$` | 嵌套状态机默认共享同一黑板。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 明确面向 `FSM/HFSM`。 |
| 事件 / 触发 | 支持 | 通过 state outcome 和外部 `ROS 2` 行为结果驱动。 |
| 守卫 / 数据 | 强支持 | shared blackboard 是核心数据通道。 |
| 层次 | 强支持 | 明确支持 nested state machines。 |
| 并发 / 同步 | 未强调 | 当前短文主要讲 state hierarchy、viewer 和集成。 |
| 时间约束 | 不支持 | 原文未提供显式时间建模语义。 |
| 连续动态 / 随机性 | 不支持 | 交给下层 `ROS 2` 组件。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 与 `ROS 2` 深度集成、带 viewer；formal verification 未覆盖。 |

### 形式化问题与性质

1. `YASMIN` 的重点是把 `ROS 2` 行为实现重新拉回到清晰的 `FSM/HFSM` 结构。
2. shared blackboard 提供了一种比大量 topic/service 回调更直接的数据组织方式。
3. 它把 Python 和 C++ 两条实现路线同时保留，兼顾快速原型和系统部署。
4. viewer 的加入说明它把“运行时可观察性”作为核心卖点，而不只是一个代码库。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. Python / C++ API 创建 states 和 transitions。
2. 组合 nested state machines。
3. 通过 blackboard 定义共享上下文。
4. 借助默认 states 加速与 `ROS 2` 的任务整合。

### 机器可处理承载方式

机器可处理承载主要是：

1. `YASMIN` Python/C++ library。
2. shared blackboard。
3. web viewer。

### 交换与互操作

`YASMIN` 不强调独立交换格式；互操作主要体现在：

1. 与 `ROS 2` actions / services / nodes 集成。
2. 作为 `MERLIN2` 等更大认知架构中的执行层组件。
3. 通过 viewer 暴露运行时状态，便于远程监控与调试。

## 配套基础设施

- 建模/编辑工具：Python/C++ API，原文未强调专用图形编辑器。
- 解析/交换/元模型支持：无独立元模型标准，主要靠库 API。
- 仿真/执行支持：原生运行于 `ROS 2`。
- 验证/分析支持：web viewer 负责运行时观察；正式验证未给出。
- 代码生成/转换支持：不是论文重点，重在直接编程集成。
- 标准化或社区生态：GitHub 开源仓库明确，面向 `ROS 2` 社区。

## 适用场景与需求前提

### 适用场景

适合 `ROS 2` 服务机器人、导航/任务执行、认知架构执行层等需要快速搭建层次状态机的场景。

### 需求前提

1. 系统已经基于 `ROS 2`。
2. 行为逻辑适合用 `FSM/HFSM` 拆解。
3. 需要共享上下文数据，而不是只靠松散消息通信。
4. 需要轻量可视化调试。

### 不适用或高成本场景

若团队更偏行为树、planner 或形式验证模型，`YASMIN` 可能不是最佳选择；若需求涉及严格时间验证，它目前的支撑也不够。

## 与相邻形式主义的关系

相对 `SMACH`，它面向 `ROS 2` 而不是 `ROS 1`；相对 `SMACHA`，它是运行库而不是生成器；相对 `RAFCON`，它没有强调大型图形任务编辑器，但更轻量、更贴近 `ROS 2` 开发流程。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目说明“状态机作为机器人行为层主承载”在 `ROS 2` 时代仍然是现实需求，而且工具形态正在从大型专用环境转向轻量库 + viewer。

### 作为目标形式主义还是中间表示

对 `ROS 2` 机器人行为开发，它更适合作为直接目标载体；对一般需求到模型流程，它也可以是实现层目标之一。

### 对需求到模型生成的启发

1. LLM 生成状态机时，不一定非得输出完整 DSL 文件，也可以输出针对库 API 的结构化骨架。
2. shared blackboard 说明状态机生成往往还要同时生成数据共享方案。
3. viewer / introspection 也是自动化落地时的重要配套能力。

## 重要的相关工作

- `SMACH`、`SMACC`：是 `YASMIN` 直接对标的上一代 / 同代状态机库。
- `MERLIN2`：论文明确把 `YASMIN` 放在其执行层中使用。
- `RAFCON`、`SMACHA`：同样面向机器人行为控制，但在 GUI、生成和运行库三条路径上各自取舍不同。

## 文献分类总结

- 这是一篇 `📦` 类现代运行库条目，重点在 `ROS 2` 行为层状态机基础设施。
- 其描述客体是机器人任务与行为控制，因此记为 `🎛️`；领域落在机器人/CPS，因此记为 `🌡️`。
- 对 `project_1` 来说，它补上了“现代轻量状态机库”这一条新生态支线，便于和 `SMACH / RAFCON / XABSL` 对照。
