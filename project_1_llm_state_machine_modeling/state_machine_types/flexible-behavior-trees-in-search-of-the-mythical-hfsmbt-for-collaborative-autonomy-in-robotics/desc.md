# 灵活行为树：寻找协作自治机器人中的神话级 HFSMBTH / Flexible Behavior Trees: In search of the mythical HFSMBTH for Collaborative Autonomy in Robotics

## 基本信息

- 标题：Flexible Behavior Trees: In search of the mythical HFSMBTH for Collaborative Autonomy in Robotics
- 中文标题：灵活行为树：寻找协作自治机器人中的神话级 HFSMBTH
- 作者：Joshua M. Zutell，David C. Conner，Philipp Schillinger
- 发表：*CoRR*，abs/2203.05389，2022
- DOI：`10.48550/ARXIV.2203.05389`
- 链接：https://arxiv.org/abs/2203.05389
- 形式主义：`FlexBE HFSM / BehaviorTree.CPP / flexible_behavior_trees`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：`FlexBE` 与 `BT` 混合执行基础设施 / `ROS 2` 协作自治桥接包
- 工具/实现获取方式：原文明确给出 `flexible_behavior_trees`、`FlexBE` 和 demo 仓库入口，并说明其基于 `BehaviorTree.CPP` 与 `ROS 2 navigation2` BT server。
- 标准/格式获取方式：承载方式是 `FlexBE` `HFSM`、`BehaviorTree.CPP`、按名称加载的 BT `XML` 文件，以及 `BtLoad/BtExecute` actions 与对应 `FlexBE` states；原文未给独立中立标准。

## 简报

这篇论文的重点不是再证明 `BT` 和 `HFSM` 谁更强，而是给出一套真正可运行的混合基础设施。作者在 `FlexBE` 的 `HFSM` 之上新增 `flexible_behavior_trees` 包，把 BT 作为可嵌入子树接进 `FlexBE`，从而同时保留 `FlexBE` 的 collaborative autonomy、preemptive transitions 和 operator interaction，以及 `BT` 的模块化子行为表达。

- 形式主义定位：`HFSM + BT` 混合执行载体，而不是新的独立理论状态机家族。
- 构造方式简述：`FlexBE HFSM -> BtLoad/BtExecute actions -> BT server -> XML-encoded Behavior Trees`。
- 基础设施与场景简述：依托 `FlexBE`、`BehaviorTree.CPP`、`ROS 2 navigation2` 和自定义 actions/states，服务协作自治、导航和人机共管机器人行为。

```text
FlexBE HFSM -> BtLoad / BtExecute bridge -> BT server + XML BTs -> collaborative autonomy robot behavior
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `FlexBE` 的 `HFSM` 与 collaborative autonomy 机制。
2. 由名称索引的 BT 行为库。
3. 基于 `BehaviorTree.CPP` 的 BT server。
4. `BtLoad` 与 `BtExecute` 两类自定义 `ROS 2` actions。
5. `BtLoaderState`、`BtExecuteState`、`BtExecuteGoalState` 三个 `FlexBE` 状态实现。

### 核心抽象

结合论文结构，可把这一混合执行器保守整理为：

$$
\mathcal{H} = (Q, q_0, \mathcal{B}, \delta, \Gamma)
$$

上式中的符号逐项解释如下：

1. `Q` 是 `FlexBE` `HFSM` 的状态集合。
2. `q_0` 是初始状态。
3. `\mathcal{B}` 是按行为名索引的 BT 集合。
4. `\delta` 是 `HFSM` 层的状态转移关系。
5. `\Gamma` 是 `HFSM` 与 BT server 之间的 action interface 集合。

论文明确给出了桥接动作集，因此可写成：

$$
\Gamma = \{\mathrm{BtLoad}, \mathrm{BtExecute}\}
$$

上式中的符号逐项解释如下：

1. `\mathrm{BtLoad}` 负责把 BT `XML` 文件加载进 server。
2. `\mathrm{BtExecute}` 负责触发指定 BT 行为名的执行。
3. 这两个动作就是 `HFSM` 与 BT 子系统的最小桥。

BT 加载与执行还可保守写成：

$$
\mathrm{Load}(xml_i) = b_i \in \mathcal{B},\quad \mathrm{Exec}(q,b_i,\eta) \to (o,\eta')
$$

其中：

1. `xml_i` 是某个 BT 的 `XML` 文件。
2. `b_i` 是被 server 按名称登记的 BT 行为。
3. `q` 是当前 `FlexBE` 状态。
4. `\eta` 与 `\eta'` 是执行前后的用户数据或目标参数。
5. `o \in \{Success, Failure, Running\}` 是 BT 返回结果。

### 一个最小例子与通俗解释

论文给出的导航示例很直观：

1. `FlexBE` 行为先用普通状态做计划准备、用户确认或其他上层逻辑。
2. 需要执行导航子任务时，`BtExecuteState` 发起一个 BT 行为。
3. BT 内部再通过 `Fallback`、`Sequence` 等结构管理局部导航控制。
4. 若用户需要接管或调整自治级别，仍然通过 `FlexBE` 的 collaborative autonomy 机制完成。

通俗地说，这套方案像是“在大状态机里面嵌一棵能反复重评估的行为树”。大框架负责脚本、监督和人与机器协作，小子树负责局部灵活策略。

### 运行 / 接受 / 转移语义

论文明确指出 `BtExecute` 运行时会持续返回 active nodes、机器人位置和执行时长，因此可保守写成：

$$
\mathrm{Exec}(q,b,\eta) \to (o,\eta')
$$

上式中的符号逐项解释如下：

1. `q` 是当前 `FlexBE` 状态。
2. `b` 是被执行的 BT。
3. `\eta` 是初始 user data 或目标参数。
4. `o` 是 BT 的结果状态。
5. `\eta'` 是执行后的新 user data 或反馈信息。

从 `HFSM` 视角，桥接状态可保守整理为：

$$
q \in \{\mathrm{BtLoaderState}, \mathrm{BtExecuteState}, \mathrm{BtExecuteGoalState}\}
$$

其中：

1. `BtLoaderState` 负责预加载相关 BT。
2. `BtExecuteState` 负责按名称执行 BT。
3. `BtExecuteGoalState` 负责给导航类 BT 加入一个或多个 `PoseStamped` 目标。

### 语义边界

这条路线的边界有：

1. 它没有提出新的可验证混合自动机，只是把现有 `HFSM` 与 `BT` 基础设施拼接起来。
2. `BT` 与 `HFSM` 仍各自保留原有语义和限制。
3. 强项是 collaborative autonomy 和工程复用，不是严格形式分析。
4. 整体强依赖 `ROS 2`、`FlexBE` 和 `BehaviorTree.CPP` 生态。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
| --- | --- | --- |
| 混合骨架 | `$\mathcal{H} = (Q, q_0, \mathcal{B}, \delta, \Gamma)$` | `HFSM` 状态、BT 库和桥接动作共同构成混合执行器。 |
| 桥接动作 | `$\Gamma = \{\mathrm{BtLoad}, \mathrm{BtExecute}\}$` | `HFSM` 与 BT server 的最小接口。 |
| BT 加载 | `$\mathrm{Load}(xml_i) = b_i$` | `XML` 文件被登记为具名 BT 行为。 |
| BT 执行 | `$\mathrm{Exec}(q,b_i,\eta) \to (o,\eta')$` | `HFSM` 状态可直接调用 BT 并接收结果。 |
| 桥接状态 | `$q \in \{\mathrm{BtLoaderState}, \mathrm{BtExecuteState}, \mathrm{BtExecuteGoalState}\}$` | `FlexBE` 侧暴露了三种标准桥接状态。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
| --- | --- | --- |
| 状态 / 模式 | 很强 | 外层 `HFSM` 和内层 `BT` 双层离散结构并存。 |
| 事件 / 触发 | 强支持 | `FlexBE` preemption、BT ticks、ROS actions 都参与控制。 |
| 守卫 / 数据 | 强支持 | `FlexBE` user data、BT feedback 和 goal 参数都被显式传递。 |
| 层次 | 强支持 | `HFSM` 自带层次，BT 也支持子树组合。 |
| 并发 / 同步 | 中等支持 | 重点是桥接与监督，不主打复杂并发语义。 |
| 时间约束 | 不突出 | 论文关心行为控制，不是显式 timed verification。 |
| 连续动态 / 随机性 | 不支持本体、支持外接 | 连续控制留给机器人下层导航与控制组件。 |
| 可执行 / 可验证性 | 强执行、弱验证 | 开源包、demo 和 collaborative autonomy 很强； formal verification 不是重点。 |

### 形式化问题与性质

1. 论文的真正贡献是把 `BT` 嵌入 `FlexBE` 的工程接口做成标准化 action/state 组合。
2. 它并不试图用 `BT` 取代 `HFSM`，而是把两者各自的优势固定成明确分工。
3. `XML` BT 文件、具名行为库和 `PoseStamped` 目标接口，使这套桥接足够可复用。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 用 `FlexBE` 设计外层 `HFSM` 行为。
2. 用 `BehaviorTree.CPP` / `navigation2` 风格定义 BT `XML`。
3. 通过 `BtLoaderState` 预加载 BT。
4. 通过 `BtExecuteState` 或 `BtExecuteGoalState` 从 `HFSM` 中调用对应 BT。

### 机器可处理承载方式

机器可处理承载方式包括：

1. `FlexBE` `HFSM` 定义。
2. BT `XML` 文件。
3. `BtLoad/BtExecute` `ROS 2` actions。
4. `BtLoaderState`、`BtExecuteState`、`BtExecuteGoalState` 三种桥接状态。

### 交换与互操作

互操作重点在：

1. BT server 兼容 `ROS 2 navigation2` 风格。
2. `FlexBE` 保持 collaborative autonomy 和 UI / mirror / onboard executive 架构。
3. `BehaviorTree.CPP` 负责 BT 执行内核。
4. `ROS 2` actions 负责 `HFSM` 与 BT 之间的参数和反馈交换。

## 配套基础设施

- 建模/编辑工具：`FlexBE UI`、`FlexBE` mirror / onboard behavior executive。
- 解析/交换/元模型支持：BT `XML`、具名行为装载、`ROS 2` actions。
- 仿真/执行支持：`BehaviorTree.CPP`、`navigation2` BT server、`ROS 2` demos、Turtlebot 仿真与真机。
- 验证/分析支持：论文更偏执行与人机共管，不主打形式验证。
- 代码生成/转换支持：不是核心；重点在包级桥接与运行时整合。
- 标准化或社区生态：依托 `FlexBE`、`ROS 2`、`navigation2` 和 `BehaviorTree.CPP` 开源生态。

## 适用场景与需求前提

### 适用场景

适合需要协作自治、操作员可干预、高层脚本化行为与局部灵活策略并存的机器人任务，例如导航、搜索与复杂任务执行。

### 需求前提

1. 系统已基于 `ROS 2` 或可接近该生态。
2. 高层行为适合 `HFSM` 表达，局部策略适合 `BT` 表达。
3. 团队重视 collaborative autonomy 与运行时可接管性。
4. BT 行为可以整理为可按名称加载的 `XML` 资源。

### 不适用或高成本场景

如果系统并不使用 `FlexBE/ROS 2`，或高层和局部控制都更适合统一表示成单一模型，这条桥接路线会显得偏重。

## 与相邻形式主义的关系

相对 [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)，本文更强调 `HFSM + BT` 混合和 collaborative autonomy，而不是轻量纯状态机库；相对 [rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md](../rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md)，它不主打图形任务图编辑器，而主打 `FlexBE` 生态内的桥接基础设施；相对 [ros-commander-behavior-creation-for-home-robots/desc.md](../ros-commander-behavior-creation-for-home-robots/desc.md)，它把 `HFSM` 与 `BT` 做了更细粒度混合，而不是只输出 `HFSM -> runtime`。

## 与本研究的关系

### 对 Project 1 的价值

这篇条目说明，面向机器人软件时，状态机不必独占高层控制；它完全可以作为总控骨架，把局部 `BT` 子策略纳入一个更可解释、可监督的框架。

### 作为目标形式主义还是中间表示

更像机器人执行栈中的目标基础设施，而不是通用中间表示。

### 对需求到模型生成的启发

1. 需求生成不一定非得输出单一形式主义，完全可以做“外层状态机 + 内层行为树”的分层产物。
2. 人机协作任务里，preemption、blocked transitions 和 adjustable autonomy 应当被当作一等需求对象。
3. 若要让生成结果可落地，桥接动作、参数接口和行为资源命名都需要显式设计。

### 现实限制

它非常依赖具体工具生态，且更多是运行时桥接基础设施，不直接提供形式语义保证。

## 重要的相关工作

1. [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)：较轻量的 `ROS 2` 状态机运行时。
2. [rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md](../rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md)：机器人任务编排与执行的另一条基础设施路线。
3. [ros-commander-behavior-creation-for-home-robots/desc.md](../ros-commander-behavior-creation-for-home-robots/desc.md)：家用机器人 `HFSM` 图形编辑与运行时路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体围绕 `flexible_behavior_trees` 这个 `ROS 2` 桥接包及其 actions/states/server 架构，明显属于执行基础设施条目。
