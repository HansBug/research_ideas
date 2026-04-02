# 基于有限状态机的自主造林机械控制系统设计与实现 / Design and Implementation of a Control System for an Autonomous Reforestation Machine Using Finite State Machines

## 基本信息

- 标题：Design and Implementation of a Control System for an Autonomous Reforestation Machine Using Finite State Machines
- 中文标题：基于有限状态机的自主造林机械控制系统设计与实现
- 作者：Morgan Rossander, Håkan Lideskog
- 发表：*Forests*, 14(7):1340, 2023
- DOI：`10.3390/f14071340`
- 链接：https://doi.org/10.3390/f14071340
- 形式主义：`SMACH Mission Supervisor / AutoPlant`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：任务监督器 / 应用控制系统
- 工具/实现获取方式：原文明确说明任务监督器运行在 `ROS Melodic` 上，使用 `SMACH`、`MoveIt`、`RViz`、`URDF` 和若干 action clients；正文未提供公开代码仓库。
- 标准/格式获取方式：承载方式是 `SMACH` 层次状态机、`ROS` actions/services、状态类与 client interface、自定义模拟器和数字孪生模型；原文未给独立 XML/JSON 标准。

## 简报

这篇论文虽然场景极具体，但它补出的状态机载体证据非常完整：作者把自主造林机的多子系统协同任务压成一个 `SMACH` mission supervisor，统一协调底盘移动、吊机、植苗器、plant planner、拍照与障碍检测。状态机不是孤立示意图，而是被放进 `ROS` action/service、`URDF` 数字孪生、`MoveIt` 运动规划和低复杂度模拟器的完整链路里。对本 collection 来说，这正是“特定领域应用型状态机如何落成真实控制系统”的好样本。

- 形式主义定位：面向自主造林机械任务协调的 `SMACH` 层次监督状态机，而不是新的林业专用自动机理论。
- 构造方式简述：将机器作业流程拆成顶层 superstates 和 client actions，再用 `SMACH` submachines、status variables 和 outcomes 组织控制流。
- 基础设施与场景简述：依托 `ROS`、`SMACH`、`MoveIt`、`RViz/URDF`、custom simulator 和 action clients，服务真实林地中的自主植苗作业。

```text
造林作业需求 -> SMACH mission supervisor -> ROS actions/services + submachines -> digital twin / simulator / MoveIt -> 真实机器执行
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. mission supervisor：顶层 `FSM`，负责任务协调。
2. action clients：对 drive、crane、planter、plant planner、photo 等子系统的统一调用接口。
3. superstates / submachines：顶层状态图中的层次化状态机。
4. outcomes：各客户端动作完成后返回的执行结果。
5. status variables：如 `has_seedling`、`new_site` 这类系统级布尔状态。
6. digital twin / simulator：用于中间验证和运行态可视化的环境模型。

### 核心抽象

结合论文的顶层状态图与 client-action 结构，可保守整理该 mission supervisor 为：

$$
M = (S, s_0, C, O, T, V)
$$

上式中的符号逐项解释如下：

1. `S` 是 mission supervisor 的状态集合。
2. `s_0 \in S` 是初始状态。
3. `C` 是可调用的 client action 集合，例如 `NEXT_POS`、`DOCK`、`GET_POSITION`、`PLANT`。
4. `O` 是各 action client 返回的 outcome 集合，例如成功、失败、结束或需要转移到其他状态。
5. `T \subseteq S \times O \times \Phi(V) \times S` 是转移关系，其中 `\Phi(V)` 是对 status variables 的条件判断。
6. `V` 是系统级状态变量集合，原文明确给出 `has_seedling` 与 `new_site`。

顶层状态机的单步推进可保守写成：

$$
(s, \nu) \xrightarrow{o} (s', \nu') \iff (s, o, \phi(\nu), s') \in T
$$

上式中的符号逐项解释如下：

1. `s`、`s'` 是当前和下一状态。
2. `\nu`、`\nu'` 是转移前后的 status variables 赋值。
3. `o \in O` 是 action client 的返回 outcome。
4. `\phi(\nu)` 是基于 `has_seedling`、`new_site` 等变量的守卫条件。

### 一个最小例子与通俗解释

论文顶层图的核心循环非常清楚：

1. `Standby` 等待启动。
2. `Move` 把机器移动到下一个工作位置，并把 `new_site` 置为真。
3. `Transfer & map generation` 在吊机转运和建图之间协同，为下一株树获取工作区信息。
4. `Select plant position` 让 plant planner 给出新的种植点。
5. `Plant` 执行吊机放置、整地、植苗和拍照等步骤。

通俗地说，这个 mission supervisor 像“给一台造林机器人配了一个总调度员”：总调度员自己不直接控制液压缸和种植器，但它知道该先让谁工作、失败后应该回退到哪里、以及什么时候该重选种植点。

### 运行 / 接受 / 转移语义

依据论文描述，state 自身大多不直接包含底层逻辑，而是通过统一 interface 调用 client：

$$
\mathrm{exec}(s) = \mathrm{call}(c_s) \to o_s
$$

上式中的符号逐项解释如下：

1. `c_s \in C` 是状态 `s` 关联的 client action。
2. `o_s \in O` 是该 client 返回的 outcome。
3. mission supervisor 主要根据 `o_s` 决定后继转移。

顶层循环中最关键的系统变量更新可保守写成：

$$
\nu' = \mathrm{update}(\nu, o_s)
$$

上式中的符号逐项解释如下：

1. `\nu` 是当前的系统状态变量集合。
2. `o_s` 可能改变 `has_seedling` 或 `new_site`。
3. 这些变量用于避免把纯系统状态再膨胀成额外的显式状态节点。

### 语义边界

这个 mission supervisor 的边界相当明确：

1. 它描述的是任务级协调，不是低层液压、感知或运动学细节。
2. 时间主要通过 action duration 和 `ROS` 系统节拍体现，而不是显式时间自动机。
3. 它依赖多个外部 client，因此状态机本体并不封装所有算法。
4. 其主要价值在于多子系统作业流程编排，而不是跨领域复用的理论新模型。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 监督器骨架 | `$M = (S, s_0, C, O, T, V)$` | 任务调度由状态、clients、outcomes 和变量共同决定。 |
| outcome 驱动转移 | `$(s,\nu)\xrightarrow{o}(s',\nu')$` | 控制流取决于客户端执行结果。 |
| 客户端调用 | `$\mathrm{exec}(s)=\mathrm{call}(c_s)\to o_s$` | 大多数状态都是对底层子系统动作的封装调用。 |
| 变量更新 | `$\nu'=\mathrm{update}(\nu,o_s)$` | `has_seedling` 和 `new_site` 这类系统条件被显式保留。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | mission supervisor 明确使用层次 `FSM`。 |
| 事件 / 触发 | 强支持 | 由 clients 返回的 outcomes 和状态变量共同驱动。 |
| 守卫 / 数据 | 支持 | 通过 `has_seedling`、`new_site` 等变量减少状态图复杂度。 |
| 层次 | 强支持 | 顶层状态包含 submachines。 |
| 并发 / 同步 | 支持 | 原文明确提到 `SMACH` 支持 parallel state execution。 |
| 时间约束 | 弱支持 | 运行节拍、动作时长和仿真时间被考虑，但无显式时钟语义。 |
| 连续动态 / 随机性 | 不支持 | 连续控制由 crane、drive 等底层 clients 负责。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 真实机器运行、数字孪生和模拟器都很完善；形式验证不在主线。 |

### 形式化问题与性质

1. 这篇论文证明了 `SMACH` 不只适合室内移动机器人，也能承担大型液压作业机械的 mission supervision。
2. 通过 status variables 而不是显式节点来保存系统状态，是控制图复杂度管理上的一个实用技巧。
3. 论文把数字孪生、仿真和真实机器执行都接到了同一状态机链路上，说明其承载能力不只是“能画图”。
4. 时序实验发现 crane 占用了约 `70%` 的作业时间，这反过来说明状态机分解还能暴露系统瓶颈。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 先识别实际作业序列和所需 client actions。
2. 把顶层流程写成 `SMACH` 状态机。
3. 对复杂阶段拆成 submachines。
4. 用统一 interface class 封装各 client 的 `ROS` 通信。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `SMACH` 状态类和层次状态机。
2. `ROS` action/service 调用。
3. interface class。
4. `URDF` 数字孪生。
5. Python 编写的低复杂度模拟器。

### 交换与互操作

互操作重点在：

1. 状态机通过 `ROS` actions/services 调用 drive、crane、planter 等 clients。
2. `MoveIt` 负责机械臂运动规划。
3. `RViz` 和 `smach_viewer` 提供运行态反馈与调试观察。

## 配套基础设施

- 建模/编辑工具：`SMACH` 提供层次状态机构造与 introspection。
- 解析/交换/元模型支持：`ROS` action/service、`tf`、`URDF` 和 `RViz` 共同提供系统互连基础。
- 仿真/执行支持：有真实机器、数字孪生和 Python 低复杂度模拟器三套执行环境。
- 验证/分析支持：通过仿真对比、时序实验和 `smach_viewer` 做运行分析；形式验证未涉及。
- 代码生成/转换支持：不强调自动代码生成，主要是 Python + `ROS` 直接实现。
- 标准化或社区生态：高度依赖 `ROS` 和 `SMACH` 生态，工具成熟但载体特定于该软件栈。

## 适用场景与需求前提

### 适用场景

适合需要在真实作业机械上协调移动平台、机械臂、规划器、执行器和传感器的 mission-level 任务控制，尤其是农业、林业和野外移动作业场景。

### 需求前提

1. 任务可以拆成清晰的顺序和局部并行阶段。
2. 子系统能够通过 `ROS` actions/services 暴露统一接口。
3. 运行时需要基于 outcomes 做异常回路和重试。
4. 团队接受用数字孪生和模拟器作为状态机中间验证环节。

### 不适用或高成本场景

若目标是轻量库级复用、与 `ROS` 解耦，或需要强形式验证，那么该方案就偏重；它首先是一套真实林业机器的应用控制系统。

## 与相邻形式主义的关系

相对 `FlexBE`、`RAFCON` 这类更强调图形编辑和任务编排的框架，它更贴近“直接用原生 `SMACH` 做工业应用监督器”；相对 `SMACHA`，它不是代码生成器，而是一个完整实例化的监督状态机应用；相对 `RoboChart`，它更偏执行协调而非形式验证。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文补出了一个非常实在的结论：即便模型本体并不新，只要状态机能稳定协调多个异构子系统、接入数字孪生并运行在真实机器上，它就已经是高价值的目标载体证据。

### 作为目标形式主义还是中间表示

它更适合作为具体 `ROS/SMACH` 生态下的目标执行载体，不适合作为统一中间表示。

### 对需求到模型生成的启发

1. 面向复杂机械系统时，状态机生成结果应显式保留 subsystem outcomes。
2. 除状态图外，还要同时生成 interface 层和调试/可视化入口。
3. 系统级布尔变量是控制图压缩的重要手段，需求抽取阶段就应识别出来。

## 重要的相关工作

- `SMACH`：是 mission supervisor 的直接运行时载体。
- `MoveIt`：负责 crane 运动规划。
- `ROS` 数字孪生链路：`URDF`、`RViz`、`tf` 和 action/service 是整套方案成立的关键基础设施。

## 文献分类总结

- 这是一篇 `📦` 类应用控制系统条目，重点在 `SMACH` 监督状态机如何真正协调自主造林机的多子系统作业流程。
- 其描述客体是作业控制逻辑，因此记为 `🎛️`；论文面向真实林业机械/CPS 系统，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“特定领域状态机监督器如何接入真实机器和数字孪生”的工程证据。
