# 面向任务编程与任务控制的图形化工具 RAFCON / RAFCON: A Graphical Tool for Task Programming and Mission Control

## 基本信息

- 标题：RAFCON: A Graphical Tool for Task Programming and Mission Control
- 中文标题：面向任务编程与任务控制的图形化工具 RAFCON
- 作者：Sebastian G. Brunner, Franz Steinmetz, Rico Belder, Andreas Dömel
- 发表：In *RoboCup 2016: Robot World Cup XX*, Lecture Notes in Computer Science, pp. 347-355, 2017（当前 `paper.pdf` 为 arXiv 预印本）
- DOI：`10.1007/978-3-319-68792-6_29`
- 链接：https://doi.org/10.1007/978-3-319-68792-6_29
- 形式主义：`RAFCON`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：图形任务编程 / 机器人 mission control 载体
- 工具/实现获取方式：原文明确给出 `RAFCON` 的 Python core、GTK+ GUI、library state、remote monitoring 与 API，但未在论文中提供公开仓库链接。
- 标准/格式获取方式：承载方式是 `RAFCON` 图形状态机模型、状态类型、outcome/transition/data flow 结构；原文未给出独立行业交换标准。

## 简报

`RAFCON` 解决的不是“如何合成任务计划”，而是“已经知道大致要做什么之后，如何把复杂机器人系统的离散任务控制真正组织起来”。它以层次化、并发化状态机为核心，用 GUI 支持大规模任务图、库复用、调试、错误恢复和远程观察，让视觉、导航、操作等异构模块在同一 mission-control 载体里协同运行。

- 形式主义定位：面向复杂机器人任务协调的图形化层次状态机执行框架。
- 构造方式简述：以 execution / hierarchy / concurrency / library 四类状态、outcome 驱动 transition、数据端口与 data flow 联合构造。
- 基础设施与场景简述：依托 Python execution engine、GTK+ GUI、library manager、远程订阅和 step / step-back 调试，服务服务机器人、空间机器人和竞赛任务。

```text
机器人任务需求 -> RAFCON hierarchical state machine -> Python execution engine + GUI -> 远程监控 / 调试 / 任务执行
```

## 形式主义定义与核心对象

### 定义对象

论文把 `RAFCON` 的状态机定义成“带层次、并发、库复用和数据流的任务状态机”。状态既是控制流节点，也是和外部 middleware 交互的执行入口。

### 核心抽象

结合正文对 core framework 的定义，可保守整理出：

$$
R = (S, s_0, \tau, O, T, P_{in}, P_{out}, F)
$$

上式中的符号逐项解释如下：

1. `S` 是状态集合。
2. `s_0 \in S` 是根状态或执行入口。
3. `\tau : S \to \{\mathrm{Execution}, \mathrm{Hierarchy}, \mathrm{Concurrency}, \mathrm{Library}\}` 给出状态类型。
4. `O` 是 outcome 集合。
5. `T \subseteq S \times O \times S` 是基于 outcome 的迁移关系。
6. `P_{in}`、`P_{out}` 分别是输入数据端口和输出数据端口集合。
7. `F \subseteq P_{out} \times P_{in}` 是 data flow 连接关系。

论文明确区分四类状态：

$$
\tau(s) \in \{\mathrm{Execution}, \mathrm{Hierarchy}, \mathrm{Concurrency}_{pre}, \mathrm{Concurrency}_{barrier}, \mathrm{Library}\}
$$

其中：

1. `Execution` 状态包含用户定义的 `execute` 函数，直接连接机器人模块。
2. `Hierarchy` 状态包含子状态并定义固定 start state。
3. `Concurrency_pre` 表示 preemptive concurrency，任一子状态完成就停止其他子状态。
4. `Concurrency_barrier` 表示 barrier concurrency，等待全部子状态结束。
5. `Library` 状态用于封装和复用整台子状态机。

### 一个最小例子与通俗解释

论文图 2 给了一个很典型的最小例子：自主体探索未知环境，直到定位到红球，或者计时器抢占执行。

1. 一个 hierarchy state 作为上层任务容器。
2. 其中一个 execution state 负责探索 / 导航。
3. 并行区域里一个分支监视“是否已找到红球”，另一个分支监视超时。
4. 一旦成功定位或计时器触发，对应 outcome 会驱动整个任务图转向下一个阶段或中止。

通俗地说，`RAFCON` 像“给机器人任务做的一套可放大缩小的流程地图”。每个状态可以写代码、挂数据端口、走正常路径或错误恢复路径，大任务还能被拆成很多可复用子图。

### 运行 / 接受 / 转移语义

论文给出的核心运行语义很直接：若状态以某个 outcome 结束，则沿该 outcome 所连接的 transition 前进。可保守压成：

$$
(s, o) \in S \times O,\ T(s, o) = s'
\Rightarrow
\text{next}(s) = s'
$$

其中：

1. `s` 是当前状态。
2. `o` 是当前状态的退出 outcome。
3. `T(s,o)=s'` 表示该 outcome 指向下一个 sibling state 或 parent outcome。
4. `next(s)=s'` 表示 execution engine 下一步进入 `s'`。

对层次和并发状态，执行语义还包括：

$$
\tau(s)=\mathrm{Hierarchy} \Rightarrow \text{enter}(s)=start(s)
$$

$$
\tau(s)=\mathrm{Concurrency}_{pre} \Rightarrow \exists i,\ finished(c_i) \Rightarrow \forall j \neq i,\ preempt(c_j)
$$

上式中的符号逐项解释如下：

1. `start(s)` 是 hierarchy state 的固定入口子状态。
2. `c_i` 是某个 concurrency state 的子状态。
3. `finished(c_i)` 表示某个子状态先完成。
4. `preempt(c_j)` 表示 preemptive concurrency 会停止其他并行子状态。

### 语义边界

`RAFCON` 的边界也很清楚：

1. 它面向任务编排和 mission control，不是 planner 语言。
2. 它强依赖 execution state 中的用户代码与外部 middleware。
3. 它支持并发和数据流，但不提供显式时钟自动机或连续动力学语义。
4. 它的优势是工程执行与调试，不是理论可判定性。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 模型骨架 | `$R = (S, s_0, \tau, O, T, P_{in}, P_{out}, F)$` | 同时编码控制流、状态类型和数据流。 |
| outcome 驱动迁移 | `$T(s,o)=s' \Rightarrow \text{next}(s)=s'$` | 状态退出后根据 outcome 决定下一步。 |
| 层次入口 | `$\tau(s)=\mathrm{Hierarchy} \Rightarrow \text{enter}(s)=start(s)$` | hierarchy state 有固定 start state。 |
| preemptive 并发 | `$\exists i,\ finished(c_i) \Rightarrow \forall j \neq i,\ preempt(c_j)$` | preemptive concurrency 的一个子状态完成即可终止其他分支。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 四类核心状态构成任务控制骨架。 |
| 事件 / 触发 | 强支持 | outcome、外部模块返回、定时器和错误都可驱动迁移。 |
| 守卫 / 数据 | 强支持 | 数据端口、全局变量、执行上下文和用户代码共同参与。 |
| 层次 | 强支持 | hierarchy state 是核心特性。 |
| 并发 / 同步 | 强支持 | 原生支持 preemptive / barrier concurrency。 |
| 时间约束 | 部分支持 | 通过 timer state 或外部逻辑实现，不是显式 clock 模型。 |
| 连续动态 / 随机性 | 不支持 | 连续行为在外部模块中实现。 |
| 可执行 / 可验证性 | 强支持 | 直接运行于 execution engine，并支持 step、step back、remote monitoring。 |

### 形式化问题与性质

1. `RAFCON` 把 logic flow 和 data flow 明确分离，降低了大任务图的可视化复杂度。
2. `Library state` 让整台子状态机可重用，这一点比普通 flat FSM 更贴近工程任务库。
3. `execute_backwards` 和 remote-control 语义说明它非常强调调试和运行时可观察性。
4. 它是强工程化状态机框架，而不是单纯“图形前端”。

## 构造方式与承载格式

### 建模入口

建模入口主要有三类：

1. 图形状态机编辑器中直接拖放状态与连接。
2. execution state 中编写 Python `execute` 函数。
3. 通过 API 进行程序化状态机生成或与逻辑 planner 集成。

### 机器可处理承载方式

原文强调两类可处理对象：

1. state machine 本体，包括状态、outcome、transition、port 和 data flow。
2. execution state 中的 Python 代码。

### 交换与互操作

`RAFCON` 没有给出独立 XML/JSON 标准；互操作重点在于：

1. execution state 与其他 middleware 的 Python 接口。
2. 可远程订阅运行中的状态机并接收状态 / 数据端口值。
3. API 可与 planner 或任务生成器对接。

## 配套基础设施

- 建模/编辑工具：GTK+ 图形界面、state editor、library manager、state machine tree、global variable manager、execution history。
- 解析/交换/元模型支持：GUI 与 core 分离，采用 MVC 架构；原文未给独立元模型标准。
- 仿真/执行支持：Python execution engine、连续执行 / 单步 / step over / step into / step back。
- 验证/分析支持：论文重心不是 formal verification，但提供很强的运行时监控与调试能力。
- 代码生成/转换支持：提供 API，可程序化生成状态机并与 planner 集成。
- 标准化或社区生态：依托机器人任务编程和 DLR 场景，工程生态偏研究与应用型。

## 适用场景与需求前提

### 适用场景

适合服务机器人、空间机器人、竞赛机器人和其他需要统一编排导航、视觉、操作、恢复逻辑的复杂任务控制场景。

### 需求前提

1. 任务可分解为有限个离散状态或技能。
2. 各技能可以通过 Python / middleware 调用实现。
3. 需要层次化拆分、大量复用和远程监控。
4. 错误恢复与人工观察是重要需求。

### 不适用或高成本场景

若系统核心问题是连续控制律验证、严格实时逻辑证明或极轻量脚本控制，`RAFCON` 不是最直接选择。

## 与相邻形式主义的关系

相对 `SMACH`，它更强调图形化、数据流和大规模任务可视化；相对 `MissionLab` 一类老工具，它更强调现代 GUI、远程监控和协作开发；相对通用 `Statecharts`，它把机器人任务工程中的执行代码、库复用和调试工具纳入同一框架。

## 与本研究的关系

### 对 Project 1 的价值

`RAFCON` 提供了一个非常直接的应用证据：在真实机器人系统里，层次状态机不仅要“能表达逻辑”，还要能管理数据端口、库复用、调试与远程控制。

### 作为目标形式主义还是中间表示

在机器人任务执行场景里，它可以直接作为目标载体；在更一般的研究链中，它也适合作为从抽象状态机到 mission-control 工件的后端表示。

### 对需求到模型生成的启发

1. 生成状态机时应同时生成复用边界，而不是只生成平面状态。
2. outcome 与错误恢复路径是执行级状态机的重要组成部分。
3. 若目标系统需要大规模维护，图形层次与数据流分离会显著影响可用性。

## 重要的相关工作

- `SMACH`、`MissionLab`、`ROS Commander`：论文明确把这些已有机器人任务工具作为比较对象。
- `Statecharts / SyncCharts`：`RAFCON` 的 hierarchy / concurrency 明显借鉴了这些强状态机方言。
- `SpaceBotCamp 2016` 案例：说明 `RAFCON` 不是纸面 GUI，而是支撑过 `750+` 状态、`1200+` transition 的真实任务系统。

## 文献分类总结

- 这篇条目本质上是 `📦` 类的工程执行载体论文，核心价值在“如何把大规模机器人任务装进可编辑、可调试、可监控的层次状态机工具里”。
- 建模对象主要是机器人任务控制逻辑，因此记为 `🎛️`；应用语境落在机器人与空间系统，因此记为 `🌡️`。
- 对 `project_1` 而言，它是“状态机落地形态”而非“表达力边界”方面的高价值案例。
