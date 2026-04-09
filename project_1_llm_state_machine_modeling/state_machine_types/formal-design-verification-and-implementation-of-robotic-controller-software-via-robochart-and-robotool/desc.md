# 通过 RoboChart 与 RoboTool 实现机器人控制软件的形式化设计、验证与实现 / Formal design, verification and implementation of robotic controller software via RoboChart and RoboTool

## 基本信息

- 标题：Formal design, verification and implementation of robotic controller software via RoboChart and RoboTool
- 中文标题：通过 RoboChart 与 RoboTool 实现机器人控制软件的形式化设计、验证与实现
- 作者：Wei Li, Pedro Ribeiro, Alvaro Miyazawa, Richard Redpath, Ana Cavalcanti, Kieran Alden, Jim Woodcock, Jon Timmis
- 发表：*Autonomous Robots*, 48(6), 2024
- DOI：`10.1007/s10514-024-10163-7`
- 链接：https://doi.org/10.1007/s10514-024-10163-7
- 形式主义：`RoboChart / RoboTool`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：设计-验证-实现工具链 / 代码生成
- 工具/实现获取方式：原文明确给出 `RoboTool` 站点 `https://robostar.cs.york.ac.uk/robotool/`，并说明工具由 Eclipse plug-ins、图形/文本编辑器、验证集成和 C++ API 代码生成组成。
- 标准/格式获取方式：承载方式是 `RoboChart` metamodel、图形/文本表示、`CSP-M/tock-CSP` 语义、生成的 C++ API、Gazebo/ROS 桥接代码；原文未给独立行业交换标准。

## 简报

如果说 2019 年的 `RoboChart` 论文回答的是“这种机器人状态机 DSL 是什么”，那这篇 2024 论文回答的就是“它怎么真正走完设计、验证、仿真和部署”。论文把 `RoboChart` 的 metamodel、RoboTool 的编辑与检查机制、C++ 软件架构、`Sense -> Execute -> Actuate` 控制循环、channel 通信、timer 服务以及 code generation 全部串起来，给出了一条从状态机设计直接到可运行机器人控制软件的闭环。

- 形式主义定位：面向机器人控制软件工程的 state-machine DSL + toolchain，而不是仅供分析的抽象模型。
- 构造方式简述：以 module / robotic platform / controller / state machine 建模，再由 RoboTool 生成 `CSP` 验证语义与 C++ API。
- 基础设施与场景简述：依托 Eclipse/EMF/Xtext/Sirius/Xtend、`FDR`、generated C++ architecture、Gazebo/ROS bridge，服务 exploration task、obstacle avoidance 与 simulation/deployment。

```text
机器人需求 -> RoboChart design model -> RoboTool validation + CSP verification -> generated C++ API -> simulation / deployment
```

## 形式主义定义与核心对象

### 定义对象

论文给出的核心对象包括：

1. module：把 robotic platform 与 controllers 绑定成完整机器人控制系统。
2. robotic platform：抽象 sensors、actuators、events、variables 和 operations。
3. controller：组织一个或多个 state machines。
4. state machine：定义控制决策。
5. generated software architecture：把模型映射为 `Module`、`RoboticPlatform`、`Controller`、`StateMachine`、`Channel`、`Timer` 等 C++ 类。

### 核心抽象

结合论文第 3 节与第 4 节，可把 RoboChart 设计模型保守整理为：

$$
R = (P, C, M, I, E, V, O, K)
$$

上式中的符号逐项解释如下：

1. `P` 是 robotic platform 集合。
2. `C` 是 controller 集合。
3. `M` 是 state machine 集合。
4. `I` 是 interfaces 集合。
5. `E` 是 events 集合。
6. `V` 是 variables 与 type declarations。
7. `O` 是 operations 与 functions。
8. `K` 是 clocks 与时间原语集合。

若聚焦单个 state machine，则仍可保守写成：

$$
m = (S, J, s_0, Tr, E, V, O, C)
$$

其中：

1. `S` 是状态集合。
2. `J` 是 junction 集合。
3. `s_0 \in J` 是初始 junction。
4. `Tr` 是转移集合。
5. `E` 是 machine 使用的事件。
6. `V` 是局部变量。
7. `O` 是操作调用。
8. `C` 是时钟集合。

### 一个最小例子与通俗解释

论文先用 obstacle avoidance 例子说明建模，再用 exploration case study 说明完整工具链：

1. robotic platform 声明 `Move`、`obstacle` 等服务。
2. controller 引用 `StmMovement` 等状态机。
3. state machine 用 `Moving`、`Turning` 等状态描述决策逻辑。
4. RoboTool 检查 interfaces 是否完整、模型是否 well-formed，并生成验证语义。
5. 同一设计模型进一步生成 C++ 代码，并接入 Gazebo/ROS 做仿真与部署。

通俗地说，这篇论文把 `RoboChart` 从“能分析的状态机”推进成“能直接长成软件骨架的状态机”。

### 运行 / 接受 / 转移语义

在 generated software architecture 中，论文把整体控制循环固定为：

$$
\mathrm{Cycle} = \mathrm{Sense};\ \mathrm{Execute}^{*};\ \mathrm{Actuate}
$$

上式中的符号逐项解释如下：

1. `\mathrm{Sense}` 由 robotic platform 读取环境和硬件输入。
2. `\mathrm{Execute}^{*}` 反复执行控制器，直到没有 transition 可继续推进。
3. `\mathrm{Actuate}` 把输出写回执行器。

单个状态执行则由状态状态位驱动，论文给出 `senter`、`sactive`、`sexit`、`sinactive` 四种状态，可保守表示为：

$$
\mathrm{status}(s) \in \{\mathrm{senter}, \mathrm{sactive}, \mathrm{sexit}, \mathrm{sinactive}\}
$$

上式中的符号逐项解释如下：

1. `senter` 表示进入状态并执行 entry action。
2. `sactive` 表示状态处于激活态并尝试 child states / transitions。
3. `sexit` 表示退出状态并执行 exit action。
4. `sinactive` 表示该状态当前未激活。

状态转移的生成执行可保守写成：

$$
\mathrm{TryTransitions}(s) = \mathrm{true} \Rightarrow \mathrm{Execute}(s') 
$$

其中：

1. `\mathrm{TryTransitions}(s)` 检查当前活动状态的 enabled transitions。
2. 若存在可执行转移，则切换到目标状态 `s'` 并继续执行。
3. 若不存在，则保留在当前状态并执行 during action。

### 语义边界

这篇论文中的 `RoboChart / RoboTool` 边界也很清楚：

1. 它聚焦离散控制软件，不直接替代连续控制律设计工具。
2. 代码生成主要面向当前的软件架构和 C++ API，不是“任意平台一键导出”。
3. 目前主要支持一个 controller、一个 state machine 的 simulation/deployment 主线。
4. 强项是结构清晰、可验证、可生成，而不是最大化语言自由度。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 系统骨架 | `$R = (P, C, M, I, E, V, O, K)$` | 平台、控制器、状态机、接口、操作和时钟共同构成设计模型。 |
| machine 骨架 | `$m = (S, J, s_0, Tr, E, V, O, C)$` | 单机层面仍然是层次状态机加事件/变量/操作。 |
| 软件主循环 | `$\mathrm{Cycle}=\mathrm{Sense};\mathrm{Execute}^{*};\mathrm{Actuate}$` | 生成代码中的控制周期被固定下来。 |
| 状态执行位 | `$\mathrm{status}(s)\in\{\mathrm{senter},\mathrm{sactive},\mathrm{sexit},\mathrm{sinactive}\}$` | generated runtime 对状态推进有明确执行协议。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | self-contained hierarchical state machine 是核心。 |
| 事件 / 触发 | 强支持 | 支持 synchronous / asynchronous communications。 |
| 守卫 / 数据 | 强支持 | rich data modelling、pre/postconditions、functions、typed events。 |
| 层次 | 强支持 | 模块、控制器、状态机、复合状态多层组织。 |
| 并发 / 同步 | 支持 | 语言支持多 machine 与同步/异步通信，当前生成主线仍较保守。 |
| 时间约束 | 强支持 | budgets、deadlines、clocks 为语言原生构件。 |
| 连续动态 / 随机性 | 不支持 | 连续部分依赖其他工具或联合仿真。 |
| 可执行 / 可验证性 | 强支持 | 既能验证，又能生成运行时架构和代码。 |

### 形式化问题与性质

1. 论文最重要的推进是把 `RoboChart` 的“形式语义”真正接到了“生成软件架构”上。
2. `Sense -> Execute -> Actuate` 让设计模型和生成代码之间有了稳定、可解释的执行协议。
3. 使用 channel 作为通信中介，是为后续 correctness proof 服务的架构选择，而不只是工程习惯。
4. 这篇工作把 `RoboChart` 变成了真正的 model-based engineering 路线，而不只是 verification front-end。

## 构造方式与承载格式

### 建模入口

建模入口包括：

1. 用 graphical/textual editor 定义 package、module、platform、controller 和 state machine。
2. 通过 interface 组织 operations 与 events。
3. 用 clocks、guards、actions 和 composite states 建模行为。
4. 在 RoboTool 中即时接受 validation 和 typing 检查。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. EMF metamodel。
2. Xtext textual language。
3. Sirius graphical diagrams。
4. 自动生成的 `CSP-M/tock-CSP` 语义。
5. 自动生成的 C++ API 和类层次。

### 交换与互操作

互操作重点在：

1. 平台与控制器通过 interface 和 events/variables/operations 解耦。
2. 与 `FDR` 等 formal verification tools 集成。
3. 通过 Gazebo/ROS bridge 把生成代码接入主流机器人环境。

## 配套基础设施

- 建模/编辑工具：`RoboTool`，基于 Eclipse、EMF、Xtext、Sirius。
- 解析/交换/元模型支持：完整 metamodel、scope/type/well-formedness 检查。
- 仿真/执行支持：生成 C++ 软件架构，支持 simulation 与 deployment。
- 验证/分析支持：生成 `CSP` 语义并与 `FDR` 集成。
- 代码生成/转换支持：Xtend 模板、C++ API、hardware abstraction、channels、timers。
- 标准化或社区生态：研究型 DSL，但工具链完整，已形成稳定工程栈。

## 适用场景与需求前提

### 适用场景

适合既要做高层机器人控制设计，又要在同一条链路上完成验证、仿真和代码生成的场景，尤其适合 exploration、inspection、obstacle avoidance 等可抽象成模块化状态机的软件控制问题。

### 需求前提

1. 控制逻辑可抽成层次状态机和显式平台接口。
2. 团队接受 model-based engineering 与专用 DSL。
3. 需要把验证结果直接回馈到设计与实现。
4. 愿意沿着给定软件架构生成 C++ 代码并对接机器人平台。

### 不适用或高成本场景

若团队只需要轻量脚本状态机，`RoboChart` 全工具链可能偏重；若系统核心在连续控制器设计，也需要与其他建模/仿真技术联合使用。

## 与相邻形式主义的关系

相对 2019 年的 `RoboChart` 基础论文，这篇工作补的是 design-to-code/toolchain；相对 `FlexBE`、`RAFCON` 这类运行时行为框架，它更强调形式验证与生成语义；相对 `RobotML`、`GenoM`、`Stateflow`，它的优势在语义、验证和专用生成架构三者联动。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文非常重要，因为它证明“需求到状态机”这件事最终可以落到“状态机到可运行控制软件”这一工程终点，而不是停在图模型层面。

### 作为目标形式主义还是中间表示

在高可信机器人软件场景中，它可以直接作为目标形式主义；在更广泛的闭环里，它也是一个很强的验证与实现中间表示。

### 对需求到模型生成的启发

1. 目标语言若想真正用于软件工程，必须同时给出 metamodel、validation、formal semantics 和 code generation。
2. generated software architecture 不能是黑盒，最好像文中这样有明确类图和执行协议。
3. 若后续要做“生成-验证-修复”闭环，`Sense -> Execute -> Actuate` 这种稳定执行骨架非常有价值。

## 重要的相关工作

- 2019 年 `RoboChart` 论文：给出 DSL 本体和形式语义基础。
- `RobotML`、`GenoM`、`Stateflow`、`Behavior Trees`：都是机器人软件工程中的邻近路线。
- `FDR`、`CSP`、Gazebo/ROS：分别提供验证与运行时基础设施。

## 文献分类总结

- 这是一篇 `📦` 类高价值条目，重点在把机器人状态机 DSL 打造成完整的设计-验证-实现工具链。
- 其描述客体是机器人控制软件逻辑，因此记为 `🎛️`；论文语境面向机器人/CPS 工程，因此记为 `🌡️`。
- 对 `project_1` 来说，它提供了“状态机如何从形式模型长成软件骨架”的直接证据。
