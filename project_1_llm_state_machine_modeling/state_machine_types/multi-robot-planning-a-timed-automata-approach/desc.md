# 多机器人规划的定时自动机方法 / Multi-Robot Planning: A Timed Automata Approach

## 基本信息

- 标题：Multi-Robot Planning: A Timed Automata Approach
- 中文标题：多机器人规划的定时自动机方法
- 作者：Michael Melholt Quottrup, Thomas Bak, Roozbeh Izadi-Zamanabadi
- 发表：*Proceedings of the 2004 IEEE International Conference on Robotics and Automation (ICRA 2004)*, pp. 4417-4422, 2004
- DOI：`10.1109/ROBOT.2004.1302413`
- 链接：https://doi.org/10.1109/ROBOT.2004.1302413
- 形式主义：`Timed Automata / UPPAAL Network for Multi-Robot Planning`
- 主类：⏱️
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：多机器人运动规划 / timed automata 应用建模
- 工具/实现获取方式：原文明确使用 `UPPAAL` 建模、分析和验证，并给出环境、机器人、控制三个 process template 的构造方式。
- 标准/格式获取方式：承载方式是 `UPPAAL` timed automata network、二维网格数组、同步 channel 与 `CTL` 查询；原文未提供独立交换标准。

## 简报

这篇论文的价值，不是“把机器人路径规划翻译成一个搜索问题”这么简单，而是展示了如何把多机器人在共享工作空间里的动作、时间和碰撞约束，一起压进 `UPPAAL` 的 timed automata network。作者故意不追求高保真连续轨迹，而是先假设每个机器人已有底层 feedback controller，使它们受限地在平面网格上移动，然后把高层协同规划变成时钟约束、同步通道和 `CTL` 查询问题。

- 形式主义定位：面向多机器人高层运动协调的 `Timed Automata` 应用框架，而不是几何连续轨迹优化器。
- 构造方式简述：先将平面环境离散成 Cartesian grid，再为 obstacles、robots、controls 分别建 automata，最后在 `UPPAAL` 中组合并验证。
- 基础设施与场景简述：依托 `UPPAAL`、timed automata process templates、同步 channels、`A[]`/`E<>` 查询，服务多机器人 door passing、maze swap 等协调规划问题。

```text
环境与任务需求 -> 网格离散化 -> obstacle / robot / control automata -> UPPAAL network -> CTL queries -> 可行高层运动计划
```

## 形式主义定义与核心对象

### 定义对象

论文的直接对象包括：

1. 环境分区与静态障碍模型。
2. 机器人 timed automaton。
3. 控制 timed automaton。
4. 基于同步通道的多机器人网络。
5. 安全性与可达性 `CTL` 性质。

### 核心抽象

论文首先采用标准 timed automaton 元组：

$$
A = (L, l_0, E, I, V)
$$

上式中的符号逐项解释如下：

1. `L` 是控制位置集合。
2. `l_0` 是初始控制位置。
3. `E` 是边集合，每条边都带 guard、action、clock reset 和目标位置。
4. `I` 为每个位置赋予 invariant。
5. `V` 为每个位置赋予原子命题集合。

环境被离散成网格。论文给出工作空间分区：

$$
X = \bigcup C_{\varepsilon_1}(z_i)
$$

上式中的符号逐项解释如下：

1. `X` 是原始平面环境。
2. `C_{\varepsilon_1}(z_i)` 是以 `z_i` 为中点、分辨率为 `\varepsilon_1` 的网格单元。
3. 整个环境由有限个互不相交的网格 cell 覆盖。

扣除障碍后，机器人真正可活动的空间是：

$$
W = X \setminus \bigcup_{m=1}^{M} O(z_i)
$$

上式中的符号逐项解释如下：

1. `W` 是 obstacle-free workspace。
2. `O(z_i)` 表示位于某些 cell 的静态障碍。
3. `M` 是障碍物数量。

### 一个最小例子与通俗解释

论文给了两个很典型的例子：

1. 三台机器人通过一扇门，目标是都能到达各自 goal position 且互不碰撞。
2. 两台机器人在 maze 里交换位置，必须同时避免静态障碍和彼此冲突。

通俗地说，这个模型像“给每台机器人发一个会计时的格子地图副本”：机器人每走一格都要满足最短和最长耗时、目标格当前未被占用，以及控制器确实发出了相应同步信号。这样一来，是否会撞车、是否能按时到达，就能直接交给模型检查器问。

### 运行 / 接受 / 转移语义

论文中的机器人 process template 用时钟 `c` 约束“移动一步需要花的时间”，其典型 invariant 是：

$$
c < c_{max}
$$

而完成一步移动时，需要满足：

$$
c_{min} < c < c_{max}
$$

上式中的符号逐项解释如下：

1. `c` 是当前移动所用时钟。
2. `c_{min}` 是完成一步所需的最短时间。
3. `c_{max}` 是允许驻留的最长时间。

系统最关键的碰撞避免条件，是移动前目标格为空。以向右移动为例，可保守整理成：

$$
z_1 < hSize \land partX[z_1 + 1][z_2] = 0
$$

其中：

1. `z_1,z_2` 是机器人当前网格坐标。
2. `hSize` 是横向边界。
3. `partX` 是全局 occupancy array。
4. 目标格为 `0` 表示无人占用。

论文最终把规划问题写成 `UPPAAL` 查询。例如 reachability 可写成：

$$
E\langle\rangle\ \bigwedge_{i=1}^{N} robot_i \in goal_i
$$

安全性可写成：

$$
A[]\ \neg collision
$$

### 语义边界

这篇论文的边界很明确：

1. 它假设机器人底层已有 feedback controller，能保证“按格移动”的抽象成立。
2. 连续几何被离散成 grid，路径形状本身不是研究重点。
3. 重点是 timed reachability 和 coordination，而不是概率不确定性。
4. 工作空间里障碍主要是静态的，感知与地图构建不在主体内。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 单个定时自动机 | `$A = (L, l_0, E, I, V)$` | 机器人、控制器、障碍都可写成 timed automata。 |
| 环境网格化 | `$X = \bigcup C_{\varepsilon_1}(z_i)$` | 平面环境先被离散成有限 cell。 |
| 可活动空间 | `$W = X \setminus \bigcup O(z_i)$` | 障碍通过网格占用关系进入模型。 |
| 移动时间约束 | `$c_{min} < c < c_{max}$` | 每一步移动有最短与最长持续时间。 |
| 占用约束 | `$partX[z_1 + 1][z_2] = 0$` | 机器人只允许进入空 cell。 |
| 安全 / 可达性 | `$A[]\,\neg collision$`, `$E\langle\rangle goal$` | 直接用 `CTL` 问碰撞避免和目标可达。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | 机器人停、上、下、左、右移动等模式都有显式位置。 |
| 事件 / 触发 | 强支持 | `moveRight/moveLeft/moveUp/moveDown` 通过同步通道触发。 |
| 守卫 / 数据 | 强支持 | occupancy array、边界条件和 clocks 共同决定转移。 |
| 层次 | 弱支持 | 以 process templates 并发组合为主，不是层次状态机。 |
| 并发 / 同步 | 强支持 | 多机器人同步与共享网格占用是主体。 |
| 时间约束 | 强支持 | 每一步移动都由时钟约束和 invariants 控制。 |
| 连续动态 / 随机性 | 不支持 | 连续运动被抽象掉，随机性也未建模。 |
| 可执行 / 可验证性 | 强验证 | `UPPAAL` 可直接做 symbolic model checking。 |

### 形式化问题与性质

1. 这篇论文把多机器人协调问题切成“离散网格 + timing constraints + synchronization”三块，便于用 timed automata 直接求解。
2. 它不是简单避障，而是把动作持续时间和占用关系都纳入验证。
3. `UPPAAL` 在这里既是模型检查器，也是高层运动计划生成器。
4. 对 timed automata 主干来说，它是很典型的物理系统应用样例，而不是协议或调度样例。

## 构造方式与承载格式

### 建模入口

建模入口十分清楚：

1. 先对环境做网格离散化。
2. 再为静态障碍、机器人和控制器分别建立 process template。
3. 用全局数组维护 occupancy。
4. 最后在 `UPPAAL` 中实例化多个 robots/controls/obstacles 并提问性质。

### 机器可处理承载方式

原文直接使用的承载方式包括：

1. `UPPAAL` timed automata templates。
2. 二维整数数组 `partX`。
3. 同步通道 `moveRight/moveLeft/moveUp/moveDown`。
4. `A[]`、`E<>` 查询。

### 交换与互操作

互操作重点在：

1. robots 和 controls 通过 complementary synchronization labels 协调。
2. 所有 robots 通过共享 occupancy array 间接耦合。
3. 环境、机器人、控制器三类模型在 `UPPAAL` 里统一分析。

## 配套基础设施

- 建模/编辑工具：`UPPAAL`。
- 解析/交换/元模型支持：使用 `UPPAAL` 网络模型、全局数组和 channel；无独立交换格式。
- 仿真/执行支持：重点是 symbolic exploration，不是运行时执行器。
- 验证/分析支持：`CTL` 查询、reachability、safety、diagnostic traces。
- 代码生成/转换支持：原文未提供。
- 标准化或社区生态：依托 timed automata 与 `UPPAAL` 成熟研究生态。

## 适用场景与需求前提

### 适用场景

适合网格化移动、共享通道/门口、窄空间交换位置、仓储/场地运输这类多机器人高层协调任务。

### 需求前提

1. 机器人运动可抽象成网格中的离散步进。
2. 每一步的持续时间有稳定上下界。
3. 共享空间占用关系是主要安全约束。
4. 目标可表达为 reachability / liveness 查询。

### 不适用或高成本场景

如果问题主要由连续几何、复杂动力学、动态障碍或大尺度地图决定，仅用这种网格 timed automata 会损失太多细节。

## 与相邻形式主义的关系

相对 [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)，本文是典型应用展开；相对 [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)，它把 timed automata 从协议验证转向多机器人规划；相对 [Modelling and Verification of Timed Robotic Controllers](../modelling-and-verification-of-timed-robotic-controllers/desc.md)，它不设计新 DSL，而是直接用 `UPPAAL` 的 timed network 做高层规划。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明，当需求里已经有“时序边界 + 离散占用约束 + 并发协调”时，`Timed Automata` 可以直接作为高层规划和验证的目标形式主义。

### 作为目标形式主义还是中间表示

对多机器人高层协调问题，它可以直接作为目标形式主义；对更复杂机器人系统，也很适合作为验证导向的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时应显式保留时间上下界，而不是只保留动作顺序。
2. occupancy / resource exclusion 这类约束非常适合直接转成全局变量和 guards。
3. 若希望 LLM 生成可验证模型，应优先生成环境离散化、机器人模板和控制模板三层结构。

## 重要的相关工作

- [A Theory of Timed Automata](../a-theory-of-timed-automata/desc.md)：本文的理论母体。
- [Modelling and Analysis of a Commercial Field Bus Protocol](../modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md)：同样使用 `UPPAAL`，但对象是工业协议。
- [Modelling and Verification of Timed Robotic Controllers](../modelling-and-verification-of-timed-robotic-controllers/desc.md)：展示 timed 状态机在机器人控制 DSL 中的另一条路线。

## 文献分类总结

- 这是一篇 `⏱️` 类高价值应用条目，核心是用 timed automata network 解决多机器人高层运动规划与验证。
- 其描述客体是控制与反应式逻辑，因此记为 `🎛️`；论文语境面向物理机器人协同，因此记为 `🌡️`。
- 对 `project_1` 来说，它补的是“时间/时钟自动机如何直接承载多机器人规划问题”的主干证据。
