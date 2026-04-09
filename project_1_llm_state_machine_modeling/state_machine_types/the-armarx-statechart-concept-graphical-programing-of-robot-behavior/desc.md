# ArmarX 状态图概念：机器人行为的图形化编程 / The ArmarX Statechart Concept: Graphical Programing of Robot Behavior

## 基本信息

- 标题：The ArmarX Statechart Concept: Graphical Programing of Robot Behavior
- 中文标题：ArmarX 状态图概念：机器人行为的图形化编程
- 作者：Mirko Wächter，Simon Ottenhaus，Manfred Kröhnert，Nikolaus Vahrenkamp，Tamim Asfour
- 发表：*Frontiers in Robotics and AI*，3:33，2016
- DOI：`10.3389/frobt.2016.00033`
- 链接：https://doi.org/10.3389/frobt.2016.00033
- 形式主义：`ArmarX Statecharts / editor / distributed execution groups`
- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：面向复杂机器人行为的分布式 statechart 语言骨架与图形工具链
- 工具/实现获取方式：原文明确描述 `ArmarX` framework、statechart editor、statechart viewer、dependency resolver 和组件元数据生成机制；但未给出稳定公开仓库链接。
- 标准/格式获取方式：状态图定义保存在定制的 XML-based format 中，并伴随代码生成、profiles、cloning 和 runtime statechart groups 机制。

## 简报

这篇论文补的不是单个机器人技能，而是一种“怎样把复杂机器人高层行为做成可复用、可分布、可图形编排的 statechart 框架”。`ArmarX` 在 Harel statecharts 的基础上强化了显式数据流、远程状态、运行时重构和跨机器人 skill transfer，使状态图真正成为机器人软件环境里的高层编排载体。

- 形式主义定位：面向机器人任务控制的领域化 statechart 概念与执行载体，不是纯理论状态机变体。
- 构造方式简述：状态以模板存在，真正执行的是被实例化的 sub-states；transition 既定义 control flow 也定义 data flow；statechart groups 支持跨进程和跨主机部署。
- 基础设施与场景简述：依托 statechart editor、custom XML、code generator、viewer、component dependency resolver 和 profiles/cloning，服务复杂机器人技能的图形化开发与迁移复用。

```text
robot components -> ArmarX statechart groups / remote states -> graphical editor + explicit data mapping -> distributed execution / monitoring / reuse
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. state templates 与 instantiated sub-states。
2. transitions、events 与 transition-level parameter mapping。
3. statechart groups 与 remote states。
4. graphical editor、viewer、profiles 和 cloning。
5. 与外部机器人组件的接口绑定。

### 核心抽象

结合论文第 3 节对内部结构的描述，可把 `ArmarX` 状态图保守整理为：

$$
A = (\mathcal{G}, S, Sub, E, T, M, R)
$$

上式中的符号逐项解释如下：

1. `\mathcal{G}` 是 statechart groups 集合，每个 group 可部署在不同进程或主机上。
2. `S` 是 state templates 集合。
3. `Sub` 是作为父状态子节点出现的 sub-state 实例集合。
4. `E` 是可触发 transitions 的事件集合。
5. `T` 是 transitions 集合。
6. `M` 是 transition-level parameter mappings 集合，负责数据流。
7. `R` 是 remote-state / dynamic-remote-state 引用关系。
8. 这组元组是根据论文结构做的保守归纳。

论文对 transition 给出了非常直接的结构说明，可压成：

$$
\tau = (s_{\mathrm{src}}, e, s_{\mathrm{dst}}, \mu)
$$

上式中的符号逐项解释如下：

1. `s_{\mathrm{src}}` 是源 sub-state。
2. `e` 是与该 transition 绑定的事件。
3. `s_{\mathrm{dst}}` 是目标 sub-state。
4. `\mu` 是 parameter mapping，定义数据如何在迁移时从前一状态传给后一状态。
5. 这是对论文 “transition comprises source state, destination state, associated event, and a data mapping” 的符号化整理。

论文还强调 transition 只能发生在同一父状态的 sub-states 之间，可写成约束：

$$
\tau \in T \Rightarrow \mathrm{parent}(s_{\mathrm{src}}) = \mathrm{parent}(s_{\mathrm{dst}})
$$

上式中的符号逐项解释如下：

1. `\tau` 是一条合法 transition。
2. `\mathrm{parent}(\cdot)` 返回某个 sub-state 的父状态。
3. 含义是：为了保持模块化和数据封装，ArmarX 不允许跨父层级随意连边。

### 一个最小例子与通俗解释

可以把 `ArmarX` 想成“给机器人技能画流程图，但流程图里的每一步都能跨进程执行”：

1. 顶层状态 `PickObject` 下面有 `MoveArm`、`VisualServo`、`CloseHand` 三个 sub-states。
2. `MoveArm -> VisualServo` 的 transition 不只写“到下一步”，还显式写位姿参数怎么映射过去。
3. `VisualServo` 可以是远程状态，部署在靠近视觉组件的主机上。
4. 如果视觉伺服失败，失败事件沿层次结构往上冒泡，父状态可立即做恢复分支。

通俗地说，`ArmarX` 把状态图做成了“机器人高层技能总线”。控制流、数据流、组件依赖和分布式部署都被显式写进同一套图里。

### 运行 / 接受 / 转移语义

运行语义核心包括：

1. events 只能触发同父层级 sub-states 之间的 transitions。
2. transitions 不只是换状态，同时触发 parameter mapping 执行数据搬运。
3. 每个 statechart level 的事件处理是串行化的，以避免并发重复触发同一 transition。
4. distributed groups 和 remote states 允许行为在多进程、多主机间展开，但对上层仍保持统一 statechart 抽象。

### 语义边界

边界也很明确：

1. 论文有意删减了 Harel statecharts 的部分特性，如 inter-level transitions 和 history connector。
2. 它强调的是机器人软件工程可用性，而不是最大表达力。
3. 由于允许插入 arbitrary user code，完整形式验证并不是这条线的当前强项。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 状态图骨架 | `$A = (\mathcal{G}, S, Sub, E, T, M, R)$` | `ArmarX` 把分组部署、状态模板、实例化子状态、事件、连边和数据流统一进一套结构。 |
| transition 结构 | `$\tau = (s_{\mathrm{src}}, e, s_{\mathrm{dst}}, \mu)$` | 每条边既定义控制流，也定义数据流。 |
| 模块化约束 | `$\mathrm{parent}(s_{\mathrm{src}})=\mathrm{parent}(s_{\mathrm{dst}})$` | 不允许跨父层级乱连边，以维持封装和可复用性。 |
| 分布式执行 | `$g \in \mathcal{G} \mapsto \text{process/host}$` | statechart groups 可直接映射到不同进程或主机。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | 以状态模板和 sub-state 实例为核心。 |
| 事件 / 触发 | 很强 | transitions 全部由事件驱动。 |
| 守卫 / 数据 | 很强 | parameter mapping、条件事件和组件接口是核心增强。 |
| 层次 | 很强 | sub-states、wrapping statecharts、remote states 都建立在层次结构上。 |
| 并发 / 同步 | 中等支持 | 强调分布式部署，但刻意限制了部分 Harel 式并发特性。 |
| 时间约束 | 不突出 | 重点是高层机器人行为组织，不是时钟验证。 |
| 连续动态 / 随机性 | 不支持 | 连续控制放在外部组件或 user code 中。 |
| 可执行 / 可验证性 | 很强 | editor、viewer、dependency resolver、profiles 和 testing hooks 构成成熟执行基础设施。 |

### 形式化问题与性质

1. 这篇论文真正补的是“机器人 statechart 如何同时承载 control flow、data flow 和 deployment”。
2. 显式 data mapping 是它相对许多机器人状态机框架的关键差异。
3. distributed groups 使它比单进程 GUI statechart 更接近真实机器人系统架构。

## 构造方式与承载格式

### 建模入口

典型入口是：

1. 在 statechart editor 中创建 statechart groups 和 states。
2. 为 states 定义 input/output parameters。
3. 通过 transitions 连接 sub-states 并配置 parameter mapping。
4. 绑定外部组件依赖并生成代码骨架。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 自定义 XML-based statechart format；
2. group / profile / cloning 配置；
3. 由 editor 生成的类型安全代码骨架；
4. 运行时 statechart viewer 和 execution metadata。

### 交换与互操作

这条线的互操作重点在于：

1. statechart 通过组件元数据与外部机器人组件对接；
2. remote states 让跨进程调用在前端图里仍然看起来像普通子状态；
3. profiles 和 cloning 让同一技能可迁移到不同机器人。

## 配套基础设施

- 建模/编辑工具：图形化 statechart editor，支持结构、事件、参数和 mapping 编辑。
- 解析/交换/元模型支持：custom XML、component metadata、profiles、cloning。
- 仿真/执行支持：`ArmarX` runtime、statechart groups、remote states、statechart viewer。
- 验证/分析支持：论文更偏运行时监控、测试 hooks 和 fault recovery，而非通用模型检查。
- 代码生成/转换支持：生成类型安全接口和与组件绑定的代码骨架。
- 标准化或社区生态：依托 `ArmarX` 机器人开发环境本身，而不是中立交换标准。

## 适用场景与需求前提

### 适用场景

适合 humanoid/service robot 的高层任务编排、分布式组件协调、技能复用与跨机器人迁移。

### 需求前提

1. 机器人系统已经有较稳定的组件化中层能力。
2. 高层任务能拆成离散技能与明确事件。
3. 数据交接需要显式可追踪，而不是隐含共享黑板即可。
4. 系统愿意接受图形 editor、profiles 和 runtime viewer 这套工具链。

### 不适用或高成本场景

如果系统极度轻量、只需单进程脚本式状态切换，或核心问题在连续控制而非高层行为编排，`ArmarX` 的框架成本会偏高。

## 与相邻形式主义的关系

相对 [coordinating-robotic-tasks-and-systems-with-rfsm-statecharts/desc.md](../coordinating-robotic-tasks-and-systems-with-rfsm-statecharts/desc.md)，`ArmarX` 更强调显式 data flow 与 distributed deployment；相对 [rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md](../rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md)，两者都面向机器人任务图形编排，但 `ArmarX` 更强调 remote states、profiles 和 framework-level component binding；相对 [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)，`YASMIN` 更轻量，而 `ArmarX` 明显更重、更强调分布式和编辑器生态。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合提醒我们：若未来状态机输出要直接落到机器人软件，不仅要生成状态和边，还要生成参数映射、组件依赖和部署分组。

### 作为目标形式主义还是中间表示

更像面向机器人软件工程的目标 DSL / 执行载体，而不是纯形式验证中间表示。

### 对需求到模型生成的启发

1. 数据流不应被藏在状态代码里，最好显式挂在 transition 上。
2. “同一技能在不同机器人上复用”需要 profiles 和 cloning 这类显式机制。
3. 高层行为模型应当和组件依赖解析绑在一起，否则很难真正落地。

### 现实限制

这条路线工程性很强，但形式验证能力相对间接，而且专用工具链耦合度较高。

## 重要的相关工作

1. [coordinating-robotic-tasks-and-systems-with-rfsm-statecharts/desc.md](../coordinating-robotic-tasks-and-systems-with-rfsm-statecharts/desc.md)：`Orocos` 生态下的受限 statechart DSL。
2. [rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md](../rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md)：机器人任务编排的另一条图形工具路线。
3. [yasmin-yet-another-state-machine/desc.md](../yasmin-yet-another-state-machine/desc.md)：更轻量的 `ROS 2` 状态机运行时。

## 文献分类总结

- 主类：🔣 DSL / 专用建模语言
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 归类理由：论文主体篇幅集中在 `ArmarX` 状态图骨架、图形编辑器、运行时分组和复用机制，属于带明确语言骨架的机器人 statechart 基础设施条目。
