# MERLIN 服务机器人认知架构 / MERLIN a Cognitive Architecture for Service Robots

## 基本信息

- 标题：MERLIN a Cognitive Architecture for Service Robots
- 中文标题：MERLIN 服务机器人认知架构
- 作者：Miguel Á. González-Santamarta, Francisco J. Rodríguez-Lera, Claudia Álvarez-Aparicio, Ángel M. Guerrero-Higueras, Camino Fernández-Llamas
- 发表：*Applied Sciences*, 10(17):5989, 2020
- DOI：`10.3390/app10175989`
- 链接：https://doi.org/10.3390/app10175989
- 形式主义：`MERLIN`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：认知架构 / 规划-执行状态机桥接
- 工具/实现获取方式：原文明确依赖 `ROSPlan`、`SMACH`、`SMACH Viewer`、`ROS actionlib` 与若干 `ROS` nodes；论文没有稳定给出独立 `MERLIN` 仓库入口，但上游工具链本身是公开可获取的。
- 标准/格式获取方式：原文直接使用 `PDDL` domain/problem、`SMACH` 的 `State/Container`、`ROS` messages 与 `actionlib`、以及 `UML/SysML` 类图/通信图来承载架构；没有单独定义新的 XML/JSON 交换标准。

## 简报

这篇论文最重要的价值，不是重新发明一种通用自动机理论，而是把“长期任务规划”和“可中断的机器人行为执行”固定成一条明确的软件架构链路。作者把 `ROSPlan` 负责的 `PDDL` 规划、`SMACH` 负责的状态机执行，以及任务级目标调度和反应式设备接口，压成一个四层结构的 `ROS` 认知架构 `MERLIN`。对本 collection 来说，它补的是一种很典型的状态机落地方式：状态机不一定自己做规划，但它可以成为 planner 和机器人能力层之间的执行骨架。

- 形式主义定位：面向服务机器人长期任务控制的 hybrid architecture，其中状态机承担 mission / executor / action 三层行为骨架。
- 构造方式简述：上层用 `PDDL + ROSPlan` 生成计划，中层用 `Executor FSM` 驱动计划执行，下层用 `SMACH` action `FSM` 包装具体机器人动作。
- 基础设施与场景简述：依托 `ROSPlan`、`SMACH`、`actionlib`、`SMACH Viewer` 与 `ROS` nodes，服务复杂家居/服务机器人任务。

```text
任务目标 -> Mission FSM -> ROSPlan 生成 plan -> Executor FSM -> Action FSMs -> Reactive services
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. Mission layer：负责生成机器人目标并向下游发送 `PDDL` goals。
2. Planning layer：由 `ROSPlan` 与 `Executor` 构成，负责任务规划和计划执行。
3. Executive layer：把具体机器人动作实现为可监控的 action `FSM`。
4. Reactive layer：封装导航、语音、目标识别等反应式能力。
5. `Goal Dispatcher`：任务级目标分发器。
6. `MerlinSM`：能够与 `ROSPlan` 交互的核心状态机类。
7. `MerlinActionSM`：具体 action 的基础状态机类。
8. `MerlinAction`：连接 `ROSPlan` 与动作状态机的桥接类。
9. `Knowledge base`：由 `ROSPlan` 维护的世界知识。
10. `PDDL` domain / problem / goals / plan：规划层的机器可处理表示。

### 核心抽象

基于原文给出的四层架构、`ROSPlan` 组件和 `SMACH` 状态机类图，可保守整理 `MERLIN` 为：

$$
\mathcal{M} = (G, K, \Pi, A, F_M, F_P, \{F_a\}_{a \in A}, R)
$$

上式中的符号逐项解释如下：

1. `G` 是 Mission layer 产生的目标集合。
2. `K` 是 `ROSPlan` knowledge base 中维护的世界知识。
3. `\Pi` 是 Planning layer 产生的计划集合，每个计划由动作序列组成。
4. `A` 是可执行动作集合，例如导航、识别、语音交互等。
5. `F_M` 是 Mission layer 的目标分发状态机。
6. `F_P` 是 Planning layer 中负责执行 `ROSPlan` 的 `Executor FSM`。
7. `F_a` 是每个动作 `a` 对应的 `SMACH` action `FSM`。
8. `R` 是 Reactive layer 中的传感器/执行器服务集合。

原文明确把 planning 与 behavior 连接成一条执行链，因此其核心运行流程可保守写成：

$$
g \in G \xrightarrow{F_M} \mathrm{dispatch}(g) \xrightarrow{F_P(K)} \pi = \langle a_1, \ldots, a_n \rangle \xrightarrow{F_{a_1}; \cdots ; F_{a_n}} R
$$

上式中的符号逐项解释如下：

1. `g` 是一个待执行目标。
2. `\mathrm{dispatch}(g)` 表示 Mission layer 把目标送入 Planning layer。
3. `F_P(K)` 表示 `Executor FSM` 基于当前知识库调用 `ROSPlan` 生成计划。
4. `\pi = \langle a_1, \ldots, a_n \rangle` 是由若干动作组成的计划。
5. `F_{a_1}; \cdots ; F_{a_n}` 表示这些动作不是裸函数调用，而是分别由动作状态机执行。
6. `R` 表示底层反应式服务被这些 action `FSM` 调用。

### 一个最小例子与通俗解释

论文用餐厅/服务机器人任务来说明 `MERLIN` 的工作方式。可以把它理解成下面这个最小链路：

1. Mission layer 产生“把订单送给吧台”这个目标。
2. Planning layer 根据 `PDDL` domain/problem 把它展开成一个 plan。
3. Executive layer 中的某个 `MerlinActionSM` 负责执行 `order_to_barman` 这一步。
4. 该 action `FSM` 再去调用导航、语音、识别等 Reactive services。

通俗地说，`MERLIN` 像一个“分层总调度系统”：最上层决定想做什么，中间层决定先做哪几步，最下层的状态机负责把每一步真正做完，并在失败时回传结果、取消或重规划。

### 运行 / 接受 / 转移语义

论文虽然没有给出统一数学语义，但对 action `FSM` 的构造接口给得很清楚。可保守整理单个动作状态机为：

$$
F_a = (S_a, s_a^0, O_a, T_a)
$$

上式中的符号逐项解释如下：

1. `S_a` 是动作 `a` 的状态集合。
2. `s_a^0` 是其初始状态。
3. `O_a` 是动作执行可能产生的 outcomes，例如成功、失败、前置条件不满足等。
4. `T_a \subseteq S_a \times O_a \times S_a` 是由 outcomes 驱动的转移关系。

对 Planning layer 而言，`Executor` 的关键语义是“若计划失败则删除旧目标并重规划”，可保守表示为：

$$
\mathrm{exec}(\pi, K) =
\begin{cases}
\mathrm{success}, & \text{若 } F_{a_i} \text{ 依次完成} \\
\mathrm{replan}(K), & \text{若某一步失败}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `\pi` 是当前计划。
2. `K` 是当前知识库。
3. 若所有动作状态机顺利执行，则当前目标完成。
4. 若某一步失败，则 `Executor` 触发重规划，而不是简单停止。

### 语义边界

`MERLIN` 的边界很明确：

1. 它是一套 service robot software architecture，不是新的自动机理论。
2. 规划语义依赖 `PDDL + ROSPlan`，状态机语义依赖 `SMACH`。
3. Reactive layer 的具体算法不属于 `MERLIN` 本体，只是被它组织和调用。
4. 它非常适合“planner + executor + behavior layer”架构，但不适合作为纯粹轻量级单层 `FSM`。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 架构骨架 | `$\mathcal{M} = (G, K, \Pi, A, F_M, F_P, \{F_a\}, R)$` | `MERLIN` 是目标、知识、计划、动作状态机和反应式服务的组合架构。 |
| 目标到计划 | `$g \xrightarrow{F_M} \pi = \langle a_1, \ldots, a_n \rangle$` | Mission layer 把目标交给 Planning layer 生成动作序列。 |
| 动作执行单元 | `$F_a = (S_a, s_a^0, O_a, T_a)$` | 每个机器人动作由可监控 outcome 的状态机执行。 |
| 失败处理 | `$\mathrm{exec}(\pi, K) = \mathrm{replan}(K)$` | `Executor` 在失败时会重规划，而不是静态卡死。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | Mission、Executor、Action 三层都使用 `FSM`。 |
| 事件 / 触发 | 强支持 | `actionlib`、`ROS` service/topic 反馈和 action outcomes 共同驱动转移。 |
| 守卫 / 数据 | 强支持 | `PDDL` knowledge base、goals、action outcomes 都是关键数据。 |
| 层次 | 强支持 | 明确分为 Mission / Planning / Executive / Reactive 四层。 |
| 并发 / 同步 | 中等支持 | `SMACH` 支持并发容器，但论文主线仍是 layered control。 |
| 时间约束 | 弱支持 | 关注长期任务与取消/切换，但无显式 timed automata 语义。 |
| 连续动态 / 随机性 | 不支持 | 连续控制留给 reactive services。 |
| 可执行 / 可验证性 | 强执行、弱形式验证 | 软件架构和执行链路很完整，但验证主要是实验而非模型检查。 |

### 形式化问题与性质

1. 论文真正解决的是“怎样把 planner 和 `FSM` 行为层正常接起来”，而不是单独优化规划器或单独写一张行为图。
2. `Executor` 作为独立 `FSM` 很关键，它把 `ROSPlan` 从“会算 plan”变成“会在机器人上安全执行 plan”。
3. `MerlinActionSM` 和 `MerlinAction` 的桥接设计，使每个动作都能被 planner 调度、被 actionlib 取消、被 `SMACH Viewer` 观察。
4. 对长期交互任务来说，目标取消和重规划是它比“单层任务图”更有价值的地方。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 用 `PDDL` 写 domain、problem 和 goals。
2. 用 Mission layer 的 `FSM` 组织目标分发。
3. 用 Planning layer 的 `Executor FSM` 封装 `ROSPlan` 执行流程。
4. 用 `SMACH` 为每个 action 建立 `FSM`。
5. 用 Reactive layer 接入导航、语音、视觉等底层能力。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `PDDL` domain / problem / plan。
2. `SMACH` 的 `State` / `Container`。
3. `MerlinSM`、`MerlinActionSM`、`MerlinAction` 这组状态机类。
4. `ROS` services、topics 与 `actionlib`。
5. `UML` 类图和通信图。

### 交换与互操作

互操作重点在：

1. Mission layer 通过 `actionlib` 向 `Executor` 发送目标。
2. Planning layer 通过 `ROSPlan` 在 `PDDL` 与动作执行之间切换。
3. Executive layer 通过 `MerlinAction` 把 `ROSPlan` action 和 `SMACH` action `FSM` 绑在一起。
4. Reactive layer 以普通 `ROS` node/service 的方式对上提供能力。

## 配套基础设施

- 建模/编辑工具：原文直接依赖 `SMACH`、`SMACH Viewer`、`ROSPlan` 与 `ROS`。
- 解析/交换/元模型支持：`PDDL`、`ROS` messages、`actionlib` 和 `UML/SysML` 描述共同构成机器可处理承载。
- 仿真/执行支持：论文在服务机器人场景中实际部署并做了与 naïve approach 的对比。
- 验证/分析支持：主要通过实验评估任务完成率、切换与取消效果；形式验证不是主线。
- 代码生成/转换支持：`ROSPlan` 生成 plan，`MerlinAction` 和 `SMACH` 负责执行桥接；论文未强调自动代码生成。
- 标准化或社区生态：上游生态强，`MERLIN` 自身更像对 `ROSPlan + SMACH` 的架构化封装。

## 适用场景与需求前提

### 适用场景

适合服务机器人、助老助残机器人、竞赛型任务机器人等需要同时具备长期任务规划、任务切换、动作取消和底层能力复用的系统。

### 需求前提

1. 任务目标能够整理为 `PDDL` goals。
2. 底层能力能够封装成 planner 可以调用的 actions。
3. 团队接受 `ROS` 中间件与 `ROSPlan/SMACH` 生态。
4. 系统需要在 deliberative planning 和 reactive behavior 之间显式桥接。

### 不适用或高成本场景

如果系统只需要一个轻量单层 `FSM`，或者根本不使用 planning，那么 `MERLIN` 会显得偏重；它更适合真正存在长期任务、目标切换和行为封装需求的机器人。

## 与相邻形式主义的关系

相对纯 `ROSPlan`，`MERLIN` 多了中间的执行与行为层桥接；相对纯 `SMACH`，它多了 `PDDL` 规划和知识库驱动；相对 `SMACC`、`YASMIN` 这类运行时库，它更强调 cognitive architecture 和 planner integration，而不是单独提供一个状态机 API。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文补出了一个很实用的事实：如果后续要做“需求到状态机自动建模”，生成结果不一定直接就是最低层执行图，它也可以是 planner 下方、action 上方的一层可监控状态机骨架。

### 作为目标形式主义还是中间表示

`MERLIN` 更适合作为特定 `ROS` 生态下的目标执行架构，而不是统一中间表示。

### 对需求到模型生成的启发

1. 需求里“目标”“动作”“取消”“重规划”应分别落到不同层，而不是全塞进一张扁平状态图。
2. planner 与 state machine 之间需要显式桥接层，否则自动生成结果难以执行。
3. Action 级状态机是很自然的需求抽取粒度，因为它正好对应可监控、可取消的行为单元。

## 重要的相关工作

- `ROSPlan`：提供 `PDDL` 规划与知识库能力。
- `SMACH`：提供层次状态机执行层。
- `SMACC`：文中提到的替代方案，代表更偏 `C++` 的状态机实现路线。
- `BICA`：作者团队此前使用过的行为架构，对比说明了为什么转向 `ROSPlan + SMACH`。

## 文献分类总结

- 这是一篇 `📦` 类规划-执行桥接条目，重点是把 `ROSPlan` 和 `SMACH` 组织成可长期运行的 service robot 认知架构。
- 它描述的核心客体是机器人任务控制逻辑，因此记为 `🎛️`；语境是服务机器人/CPS 执行架构，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“自动生成的状态机如何嵌入 planner-driven 机器人软件架构”的中间层证据。
