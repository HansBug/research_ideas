# 开放路径多 AGV 系统的 Petri 网模型 / A Petri Net Model for an Open Path Multi-AGV System

## 基本信息

- 标题：A Petri Net Model for an Open Path Multi-AGV System
- 中文标题：开放路径多 AGV 系统的 Petri 网模型
- 作者：Davide Giglio
- 发表：*Proceedings of the 11th International Conference on Informatics in Control, Automation and Robotics*, pp. 734-745, 2014
- DOI：`10.5220/0005054807340745`
- 链接：https://doi.org/10.5220/0005054807340745
- 形式主义：`Coloured Petri Net (CPN) for Open-Path Multi-AGV Systems`
- 主类：🕸️ Petri 网与并发网模型
- 对象类型：🧪 应用/案例
- 描述客体：🏭 并发过程 / 资源流
- 所属领域：🏭 工业控制与自动化
- 论文角色：仓储多 AGV 并发建模 / CPN 应用
- 工具/实现获取方式：原文说明该 `CPN` 已被用于构建 discrete-event simulator，并用于分析调度、deadlock prevention 与 recovery；未给出公开仓库。
- 标准/格式获取方式：承载方式是 coloured Petri nets、meta-cell 结构、monitor places 与 timed transitions；原文未给出独立交换标准。

## 简报

这篇论文把自由行驶的 forklift AGV 仓储系统压成一张能够同时表达动作序列、安全距离、deadlock prevention 和 deadlock recovery 的 `CPN`。重点不是单台车的状态切换，而是多个 AGV 在开放路径仓库里同时取货、转向、进出 aisle 时如何安全并发、如何避免互锁，以及必要时如何通过恢复动作把系统从 deadlock 中拉回来。

- 形式主义定位：面向仓储物流并发任务的 `Petri Net` 应用条目，而不是 guided-path AGV 的普通流程图。
- 构造方式简述：以 cell、lane、drop-off area 和 AGV state 为 places，以 basic actions 为 transitions，并用 colours 表示载荷类型、方向和占用状态。
- 基础设施与场景简述：依托 `CPN`、monitor places、deadlock recovery transitions 与 discrete-event simulation，服务 automated distribution warehouse 中的多 AGV 调度与安全分析。

```text
warehouse layout + AGV basic actions -> coloured Petri net -> safety/occupancy/deadlock monitors -> simulation + scheduling/deadlock analysis
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象展开：

1. 开放路径仓库中的 cell、storage lane 和 drop-off area。
2. forklift AGV 的位置、方向和载荷状态。
3. `move straight / rotate / turn / pick-up / drop-off` 等基本动作。
4. 物理占用与虚拟占用带来的安全距离约束。
5. 用于 deadlock prevention / recovery 的监控结构。

### 核心抽象

原文直接给出了 coloured Petri net 的九元组：

$$
CPN = (P, T, A, \Sigma, V, C, G, E, I)
$$

上式中的符号逐项解释如下：

1. `P` 是 place 集合。
2. `T` 是 transition 集合。
3. `A` 是有向弧集合。
4. `\Sigma` 是颜色集集合。
5. `V` 是带类型变量集合。
6. `C` 为每个 place 指派颜色集。
7. `G` 为每个 transition 指派 guard。
8. `E` 为每条弧指派 arc expression。
9. `I` 为每个 place 指派初始标识表达式。

论文还把系统 places 写成：

$$
P = \{p_i, s_i, l_a, d_b \mid i = 1,\ldots,N;\ a = 1,\ldots,L;\ b = 1,\ldots,D\}
$$

上式中的符号逐项解释如下：

1. `p_i` 表示第 `i` 个 cell 上 AGV forks extremities 的存在。
2. `s_i` 表示第 `i` 个 cell 的安全占用状态。
3. `l_a` 表示第 `a` 个 storage lane。
4. `d_b` 表示第 `b` 个 drop-off area。
5. `N/L/D` 分别是 cells、storage lanes 和 drop-off areas 的数量。

### 一个最小例子与通俗解释

原文最直观的例子是单辆 forklift AGV 在一个 cell 上的 basic actions：

1. AGV 处在 `c61`，朝向 north。
2. 它可以 `move straight` 到前方 cell，也可以 `rotate 90°` 改变朝向，还可能在特定位置执行 `turn left/right`。
3. 每次动作之前，都必须检查目标 cell 以及邻近安全区域没有被其他 AGV 物理或虚拟占用。
4. 一旦进入存取货位置，还会触发 pick-up 或 drop-off 相关子结构。

通俗地说，这张 `CPN` 像一个“仓库地面上的并发交通图”：token 既代表 AGV，也代表货物和安全占用信息。只有在位置、方向、载荷和安全条件都满足时，某个动作 transition 才能真正触发。

### 运行 / 接受 / 转移语义

`CPN` 的标准 firing 语义可保守写成：

$$
M[t\rangle M'
$$

上式中的符号逐项解释如下：

1. `M` 是当前 marking。
2. `t` 是某个已使能的 transition。
3. `M'` 是 firing 后的新 marking。
4. 其含义是：当 basic action 的 guard 与 arc expressions 都满足时，AGV、载荷和占用状态一起更新。

论文对安全状态还引入了三值 cell interpretation：

$$
State(cell) \in \{O, V, A\}
$$

上式中的符号逐项解释如下：

1. `O` 表示 cell 被物理占用。
2. `V` 表示 cell 被虚拟占用，即因安全距离不可进入。
3. `A` 表示 cell 当前可用。
4. 这套三值状态直接决定某个 AGV 能否执行下一步 movement。

### 语义边界

这篇论文的边界如下：

1. 它主要处理仓储级任务流、通道占用与 deadlock，而不是车辆连续运动控制。
2. 开放路径假设意味着 AGV 可以自由穿行 aisle，但仍被离散 cell 抽象。
3. 模型重点是安全和调度，不是视觉感知或全局路径优化算法细节。
4. 即使加入 timed transitions，时间也主要服务 recovery 逻辑，不是完整实时控制语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `CPN` 骨架 | `$CPN = (P, T, A, \Sigma, V, C, G, E, I)$` | 用颜色、guard 与弧表达式表达多 AGV 行为。 |
| 系统 place 集合 | `$P = \{p_i, s_i, l_a, d_b\}$` | 同时覆盖 AGV 位置、安全占用和货物位置。 |
| firing 语义 | `$M[t\rangle M'$` | basic action 触发后，系统 marking 整体更新。 |
| cell 安全状态 | `$State(cell) \in \{O, V, A\}$` | 物理占用、虚拟占用和可用三值控制 AGV 可达性。 |
| deadlock 恢复 | `recovery transitions enabled by deadlock markings` | 当检测到互锁标识时，系统可切换到恢复动作。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | places/markings 直接表达 AGV、货物和 cell 状态。 |
| 事件 / 触发 | 强支持 | 基本动作由 transitions 精确表达。 |
| 守卫 / 数据 | 强支持 | colours、guard 和 arc expressions 是模型主体。 |
| 层次 | 部分支持 | 通过 meta-cell 与局部 CPN 复用结构实现弱层次。 |
| 并发 / 同步 | 强支持 | 多 AGV 并发与相互制约正是模型核心。 |
| 时间约束 | 部分支持 | 主要在 deadlock recovery 中引入 timed transitions。 |
| 连续动态 / 随机性 | 不支持 | 运动被完全离散化到 cells 与 basic actions。 |
| 可执行 / 可验证性 | 强分析 | 可做调度分析、deadlock prevention/recovery 与 simulation。 |

### 形式化问题与性质

1. 论文最有价值的地方是把“开放路径 AGV 安全通行”转成了可分析的并发网结构。
2. `O/V/A` 三值安全状态让安全距离约束在网结构里变得非常直接。
3. deadlock prevention 与 deadlock recovery 都被写进同一张 `CPN`，而不是停留在外部策略描述。
4. 对 `Petri` 主干来说，这是一个典型的“资源流 + 并发交通 + 安全约束”应用样板。

## 构造方式与承载格式

### 建模入口

建模入口可以概括为：

1. 先把仓库 layout 离散成 cells、lanes 和 drop-off areas。
2. 为 AGV 定义朝向、载荷和 basic actions。
3. 用 `CPN` 的 colours 编码 AGV/货物/cell 状态。
4. 再叠加 monitor places 和 recovery structures 处理 deadlock。

### 机器可处理承载方式

原文体现出的机器可处理承载方式包括：

1. coloured Petri net 图结构。
2. meta-cell 复用建模。
3. guard 与 arc expression。
4. 用于调度和仿真的 discrete-event simulator。

### 交换与互操作

互操作重点不在开放交换标准，而在模型复用：

1. meta-cell 结构让不同 cell 的局部模型可以重用。
2. `CPN` 既服务结构分析，也服务 simulation。
3. deadlock monitor 与 nominal motion net 可组合成同一仓储任务模型。

## 配套基础设施

- 建模/编辑工具：原文未绑定特定 `CPN` 编辑器。
- 解析/交换/元模型支持：依托 `CPN` 结构本身与自定义 colours/expressions，未提供外部标准。
- 仿真/执行支持：论文明确说明该模型已用于构建 discrete-event simulator。
- 验证/分析支持：deadlock prevention、deadlock recovery、调度与性能分析。
- 代码生成/转换支持：原文未提供自动控制代码生成。
- 标准化或社区生态：依托 coloured Petri nets 与 AGV 调度研究线，工程标准化较弱。

## 适用场景与需求前提

### 适用场景

适合 distribution warehouse、forklift AGV 车队、开放路径物流场景，以及重点问题在多车安全通行与互锁控制的系统。

### 需求前提

1. 仓储环境可以离散成有限 cell 网络。
2. AGV 行为可以分解成有限 basic actions。
3. 安全约束能写成相邻 cell 占用与虚拟占用规则。
4. 系统更关心并发和 deadlock，而不是连续轨迹最优性。

### 不适用或高成本场景

若场景高度依赖连续避障、复杂视觉感知或不可枚举的自由空间规划，仅靠这种 cell-level `CPN` 抽象会过粗。

## 与相邻形式主义的关系

相对 [Coloured Petri Nets](../coloured-petri-nets/desc.md)，本文是明确的物流应用落地；相对 [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)，它更聚焦仓储交通与 deadlock；相对 [Autonomous Forklift Navigation Inside a Cluttered Logistics Factory](../autonomous-forklift-navigation-inside-a-cluttered-logistics-factory/desc.md)，本文不是 `FSM` planner switching，而是把多车资源竞争直接交给 `CPN`。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文说明：当需求主体是“资源流 + 多车并发 + 安全距离 + deadlock”，Petri 网往往比普通状态机更贴合问题骨架。

### 作为目标形式主义还是中间表示

对仓储 AGV 协同这类问题，它完全可以作为目标形式主义；对一般控制系统，它也适合作为并发交通子系统的中间表示。

### 对需求到模型生成的启发

1. 需求抽取时要把位置资源、占用状态、基本动作和安全约束分开建模。
2. `O/V/A` 这类有限离散安全状态非常适合做 LLM 生成的 guard 骨架。
3. deadlock prevention 与 recovery 不应只写在备注里，而应该进模型主体。

### 现实限制

论文没有把路径规划、感知和低层控制统一纳入 `CPN`，因此更适合作为任务/资源层模型。

## 重要的相关工作

- [Coloured Petri Nets](../coloured-petri-nets/desc.md)：给出颜色网本体。
- [Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets](../modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md)：另一条多机器人 `Petri` 任务建模路线。
- [Long-Run Multi-Robot Planning under Uncertain Action Durations for Persistent Tasks](../long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md)：展示 `Petri` 家族如何继续走向 stochastic planning。

## 文献分类总结

- 这是一篇 `🕸️` 类高价值应用条目，核心是用 `CPN` 对开放路径多 AGV 仓储系统的安全通行与 deadlock 处理做统一建模。
- 其描述客体是并发过程与资源流，因此记为 `🏭`；论文语境落在仓储自动化，因此记为 `🏭`。
- 对 `project_1` 来说，它补充了一个典型事实：当控制问题的本体是“多体占用与资源竞争”时，Petri 网往往比离散状态机更自然。
