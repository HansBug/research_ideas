# 面向轮式移动机器人的异步有限状态控制器设计与实现 / Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots

## 基本信息

- 标题：Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots
- 中文标题：面向轮式移动机器人的异步有限状态控制器设计与实现
- 作者：Alessandro Bozzi, Simone Graffione, Roberto Sacile, Enrico Zero
- 发表：*Actuators*, 11(11):330, 2022
- DOI：`10.3390/act11110330`
- 链接：https://doi.org/10.3390/act11110330
- 形式主义：`Asynchronous WMR FSM Controller`
- 主类：📦
- 描述客体：🎛️
- 所属领域：⏱️
- 论文角色：移动机器人控制器 / 事件驱动 FSM
- 工具/实现获取方式：原文明确说明控制算法在 `Simulink/Stateflow` 上设计，并通过 `STMicroelectronics Matlab package` 部署到 `STM Nucleo F411RE`；论文未提供独立代码仓库。
- 标准/格式获取方式：承载方式是 `Stateflow` 流程图、`Simulink` block、超声/循迹/编码器传感信号以及 `PWM` 输出；没有单独交换标准。

## 简报

这篇论文的重点不是提出新的自动机理论，而是把一个三车道避障场景压成可在真实小车上跑起来的异步 `FSM` 控制器。作者把“跟踪当前车道”和“遇障换道”拆成状态图中的显式状态，再用超声距离、循迹传感器和轮编码器作为转移条件与控制输入，最终部署到 `STM32` 板上。对本 collection 来说，它提供了一个很典型的“事件驱动状态机 + 低层控制律 + 传感器守卫”组合样本。

- 形式主义定位：面向三车道避障任务的 event-based `FSM` controller，而不是通用移动机器人规划框架。
- 构造方式简述：在 `Stateflow` 中把 lane following 与 lane changing 写成状态图，再把传感器量映射到 guard 与控制输出。
- 基础设施与场景简述：依托 `Simulink/Stateflow`、`STM Nucleo`、超声传感器、循迹传感器、编码器和 `PWM` 驱动，服务嵌入式移动机器人教学与原型验证。

```text
道路/障碍需求 -> Stateflow FSM -> guard + PID/P controller -> PWM outputs -> WMR lane following / lane change
```

## 形式主义定义与核心对象

### 定义对象

论文中的核心对象包括：

1. `S`：车辆控制状态集合，如 `Follow right lane`、`Check middle lane`、`Follow middle lane`、`STOP` 等。
2. `d`：超声传感器测得的障碍距离。
3. `\theta`：由左右轮编码器推算的车辆航向角。
4. `u`：电机 `PWM` 控制输出。
5. line-tracking control：负责保持当前车道的 `PID` 控制器。
6. line change control：负责换道转角的高增益比例控制器。
7. guard conditions：基于障碍距离和航向角的状态转移条件。
8. `Stateflow` chart：控制器的机器可处理承载方式。

### 核心抽象

结合论文给出的状态图、传感器输入和控制输出，可保守整理该控制器为：

$$
W = (S, s_0, \theta, d, u, T)
$$

上式中的符号逐项解释如下：

1. `S` 是控制状态集合。
2. `s_0` 是初始状态，对应车辆从右侧车道启动。
3. `\theta` 是车辆当前航向。
4. `d` 是前向障碍距离测量。
5. `u` 是施加给左右电机和超声舵机的控制输出。
6. `T` 是由 guard conditions 定义的状态转移关系。

原文给出了两个关键物理量的计算公式。超声测距满足：

$$
d = \frac{vt}{2}
$$

上式中的符号逐项解释如下：

1. `v` 是空气中的声速，论文取 `343 m/s`。
2. `t` 是超声往返传播时间。
3. `d` 是传感器到障碍物的距离。

车辆换道时的航向更新满足：

$$
\theta(k+1) = \theta(k) + \frac{D_R(k) - D_L(k)}{L}
$$

上式中的符号逐项解释如下：

1. `\theta(k)` 与 `\theta(k+1)` 分别是当前与下一时刻航向角。
2. `D_R(k)`、`D_L(k)` 是右轮与左轮在采样时刻 `k` 的位移。
3. `L` 是左右轮间距。

### 一个最小例子与通俗解释

论文的最小可理解例子就是“从右车道出发，前方遇障后换到中间车道”：

1. 车辆处于 `Follow right lane`。
2. 若前向超声检测到 `d < 0.5 m`，转入 `Check middle lane`。
3. 若判定中间车道可用，则执行换道控制并进入 `Follow middle lane`。
4. 随后继续沿中间车道前进，直到再次遇到障碍。

通俗地说，这个控制器像“给小车装了一个有明确交通规则的状态图”：平时跟线走，离障碍太近就看相邻车道，能换就换，换完再回到正常跟踪状态。

### 运行 / 接受 / 转移语义

论文明确说明状态转移由“障碍距离 + 航向角”共同触发，因此可保守写成：

$$
(s_k, \theta_k, d_k) \xrightarrow{} (s_{k+1}, \theta_{k+1}) \iff (d_k < d_{\mathrm{th}} \lor \mathrm{aligned}(\theta_k)) \land (s_k, s_{k+1}) \in T
$$

上式中的符号逐项解释如下：

1. `s_k` 与 `s_{k+1}` 是当前和下一状态。
2. `d_{\mathrm{th}}` 是障碍检测阈值，原文设为 `0.5 m`。
3. `\mathrm{aligned}(\theta_k)` 表示车辆转角已满足当前换道完成条件。
4. `T` 是 `Stateflow` 图上允许的状态转移。

控制器输出可保守表示为：

$$
u_k =
\begin{cases}
\mathrm{PID}(e_k), & s_k \in S_{\mathrm{follow}} \\
\mathrm{P}_{\mathrm{turn}}(\theta_k), & s_k \in S_{\mathrm{change}}
\end{cases}
$$

上式中的符号逐项解释如下：

1. `e_k` 是循迹传感器给出的偏差。
2. `S_{\mathrm{follow}}` 是正常车道跟踪状态集合。
3. `S_{\mathrm{change}}` 是换道状态集合。
4. 论文明确说明正常跟踪用 `PID`，换道用 bounded proportional controller。

### 语义边界

这套 `FSM` 的边界很清楚：

1. 它针对的是三车道、静态障碍、近距离换道场景。
2. 它不做全局路径规划，也不处理复杂交通交互。
3. 状态转移依赖论文中的简化假设，例如外侧车道遇障时默认中间车道可用。
4. 它是嵌入式 event-based controller，而不是高层 mission planner。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 控制器骨架 | `$W = (S, s_0, \theta, d, u, T)$` | 状态、传感器量、控制输出和转移关系共同构成控制器。 |
| 超声测距 | `$d = vt/2$` | 障碍物检测直接驱动 guard。 |
| 航向更新 | `$\theta(k+1) = \theta(k) + (D_R(k)-D_L(k))/L$` | 换道控制依赖编码器估计的航向变化。 |
| 状态转移 | `$(s_k,\theta_k,d_k) \to (s_{k+1},\theta_{k+1})$` | 遇障与姿态条件共同决定下一状态。 |
| 双控制律 | `$u_k = \mathrm{PID}(e_k)$` 或 `$u_k = \mathrm{P}_{\mathrm{turn}}(\theta_k)$` | 跟踪与换道使用不同控制律。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 车道跟踪、车道检查、换道和停止都被显式建模为状态。 |
| 事件 / 触发 | 强支持 | 超声距离阈值和姿态条件直接触发转移。 |
| 守卫 / 数据 | 强支持 | guard 依赖距离、航向和车道可用性假设。 |
| 层次 | 不支持 | 论文展示的是平面 `FSM`，没有层次语义。 |
| 并发 / 同步 | 弱支持 | 传感与控制并行存在，但 `FSM` 本体是单活跃状态。 |
| 时间约束 | 中等支持 | 存在采样周期和离散时间更新，但无显式时钟自动机。 |
| 连续动态 / 随机性 | 弱支持 | 连续运动通过控制律体现，但不进入状态机语义核。 |
| 可执行 / 可验证性 | 强执行、弱形式验证 | 已部署到真实小车；验证主要是仿真和实车实验。 |

### 形式化问题与性质

1. 这篇论文把低层传感器处理、控制律和状态图真正绑到了一起，而不是只画一张抽象流程图。
2. 跟踪与换道使用不同控制律，是很典型的“状态决定控制器”模式。
3. `Stateflow + Simulink + STM32` 这条链路说明该模型能直接下沉到嵌入式执行层。
4. 其弱点同样明显：场景假设较强，状态逻辑主要针对预设道路结构。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 在 `Stateflow` 中画出跟踪/检查/换道状态图。
2. 把超声、循迹和编码器量映射为状态机输入。
3. 把 `PID` 与 `P` 控制器挂到不同状态的动作代码中。
4. 通过 `Simulink` 部署到 `STM Nucleo`。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `Stateflow` chart。
2. `Simulink` blocks。
3. 传感器 look-up table 与离散时间方程。
4. 电机 `PWM` 输出和舵机控制。

### 交换与互操作

互操作重点在：

1. 传感器数据先被转换成可供状态机消费的离散量。
2. 状态机输出的是电机和舵机的 `PWM` 命令。
3. `Stateflow` 模型直接通过厂商工具链部署到 `STM32` 微控制器。

## 配套基础设施

- 建模/编辑工具：`Simulink`、`Stateflow`、`STMicroelectronics Matlab package`。
- 解析/交换/元模型支持：以 `Stateflow/Simulink` 工程文件为主，未提供独立标准格式。
- 仿真/执行支持：既有 `Simulink` 仿真，也有真实小车验证。
- 验证/分析支持：通过 zig-zag 和 double left lane change 两个场景做比对。
- 代码生成/转换支持：支持从 `Simulink/Stateflow` 下发到 `STM Nucleo`。
- 标准化或社区生态：依赖 `MathWorks` 与 `STM32` 工具链，工程可执行性强但开放互操作性弱。

## 适用场景与需求前提

### 适用场景

适合教学型移动机器人、受限道路结构中的低成本避障实验、嵌入式事件驱动控制原型验证。

### 需求前提

1. 场景可抽成有限个离散驾驶模式。
2. 障碍规避主要由局部感知而非全局规划完成。
3. 控制目标允许用简单 `PID/P` 控制器实现。
4. 团队接受 `Stateflow` 和厂商部署链。

### 不适用或高成本场景

若需要复杂车流交互、动态障碍预测、多传感器融合规划或更弱假设环境，这个 `FSM` 会明显不够；它更适合受控实验环境中的嵌入式控制教学与原型。

## 与相邻形式主义的关系

相对通用 `Stateflow` 语义论文，这篇更像具体控制器实例；相对高层 mission supervisor，它下沉到传感器守卫和 `PWM` 输出；相对行为树或 planner，它更强调“先把明确的离散换道逻辑写稳”。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文补出了一个很有代表性的样本：需求中的“障碍距离阈值”“换道角度”“车道状态”可以直接映射成状态、guard 和动作，而无需先引入复杂规划器。

### 作为目标形式主义还是中间表示

它更适合作为特定嵌入式控制任务的目标执行载体，不适合作为通用中间表示。

### 对需求到模型生成的启发

1. 对局部机动任务，`FSM` 比 planner 更直接。
2. 自动生成时要同时抽取离散状态和配套控制律，而不是只抽图。
3. 传感器阈值、姿态条件和动作完成判据都应显式落成 guard。

## 重要的相关工作

- `Stateflow`：承载状态图和部署链。
- `Simulink`：负责集成控制器与硬件接口。
- `PID` / bounded proportional controller：分别对应跟踪与换道控制。
- 移动机器人 MPC / fuzzy / adaptive control：论文中作为对比路线出现。

## 文献分类总结

- 这是一篇 `📦` 类移动机器人事件驱动控制条目，重点是把离散 lane-change 逻辑、传感器守卫和低层控制器压成可部署 `FSM`。
- 它描述的核心客体是控制/反应式逻辑，因此记为 `🎛️`；语境偏实时嵌入式控制实现，因此领域记为 `⏱️`。
- 对 `project_1` 来说，它补的是“面向具体机动问题的状态机控制器如何直接落入微控制器执行”的实例证据。
