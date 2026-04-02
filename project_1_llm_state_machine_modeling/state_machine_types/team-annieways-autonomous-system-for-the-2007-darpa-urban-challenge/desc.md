# AnnieWAY 并发层次状态机 / Team AnnieWAY's Autonomous System for the 2007 DARPA Urban Challenge

## 基本信息

- 标题：Team AnnieWAY's Autonomous System for the 2007 DARPA Urban Challenge
- 中文标题：AnnieWAY 面向 DARPA Urban Challenge 的并发层次状态机系统
- 作者：Soren Kammel, Julius Ziegler, Benjamin Pitzer, Moritz Werling, Tobias Gindele, Daniel Jagzent, Joachim Schroder, Michael Thuy, Matthias Goebl, Felix von Hundelshausen, Oliver Pink, Christian Frese, Christoph Stiller
- 发表：*Journal of Field Robotics*, 25(9):615-639, 2008
- DOI：`10.1002/rob.20252`
- 链接：https://doi.org/10.1002/rob.20252
- 形式主义：`AnnieWAY CHSM`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🌡️
- 论文角色：自动驾驶行为规划器 / 面向交通规则的并发层次状态机
- 工具/实现获取方式：原文直接给出 `VW Passat` 车体、64 线激光雷达、`DGPS/INS`、低层 ECU、`CAN` 总线和行为规划软件结构；未给公开代码仓库。
- 标准/格式获取方式：原文明确使用 `UML state chart` 表示并发层次状态机，但未提供独立交换格式或开放 DSL。

## 简报

这篇论文最值得收入 `state_machine_types/` 的地方，不是整车感知或控制算法本身，而是把城市自动驾驶的行为层清楚压成了一套 `Concurrent Hierarchical State Machine`。高层 mission planner 给出路网边序列，`CHSM` 再依据交通场景、优先权和 `MTC` 检查结果切换 `Drive / Intersection / Zone / Replan / Recover` 等状态，最后输出一段 path stub 给闭环控制器。

- 形式主义定位：面向城市道路驾驶任务的并发层次行为状态机，是自动驾驶软件栈中的行为监督层。
- 构造方式简述：上层从 route graph 输入任务，状态机根据场景识别和 `MTC` 结果切状态，每个状态负责生成一段局部路径。
- 基础设施与场景简述：依托 `VW Passat + lidar + DGPS/INS + ECU + CAN/Ethernet`，服务 `DARPA Urban Challenge` 里的城市交通规则遵循、路口通行、停车区导航和全局恢复。

```text
任务路线 -> 场景评估 / MTC -> CHSM 行为状态 -> path stub -> 低层轨迹跟踪与避障
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 路网 mission plan 与边序列。
2. 场景评估模块给出的 intersection / zone / blockade / queue 等情境。
3. 行为层 `Concurrent Hierarchical State Machine`。
4. `Moving Traffic Check (MTC)` 安全判定。
5. `Drive`、`Intersection`、`Zone`、`Replan`、`GlobalRecover` 等主状态及其子状态。
6. 输出给低层控制器的 path stub。

### 核心抽象

按论文结构，可把 AnnieWAY 的行为层保守整理为：

$$
\mathcal{A} = (Q, q_0, \Sigma, \delta, G, \Pi, \Gamma)
$$

上式中的符号逐项解释如下：

1. `Q` 是行为状态集合，包括主状态和层次化子状态。
2. `q_0` 是激活后的初始状态。
3. `\Sigma` 是由场景评估、任务进度和恢复信号组成的事件集合。
4. `\delta` 是层次状态转移关系。
5. `G` 是 mission planner 给出的道路图与边序列。
6. `\Pi` 是当前感知到的交通场景与冲突空间信息。
7. `\Gamma` 是把当前状态变成 path stub 的路径生成器。

论文在 moving traffic 检查里给出了优先车辆到达冲突点的时间估计：

$$
t_{BP} = \frac{d_{BP}}{v_B}
$$

上式中的符号逐项解释如下：

1. `t_{BP}` 是优先车辆到达冲突点所需时间。
2. `d_{BP}` 是优先车辆到冲突点的距离。
3. `v_B` 是优先车辆速度。

结合论文中的 `MTC` 机制，行为层的保守转移语义可写成：

$$
\delta(q, \pi, \mu) = q'
$$

上式中的符号逐项解释如下：

1. `q` 是当前行为状态。
2. `\pi` 是当前交通场景与路权信息。
3. `\mu` 是 `MTC` 判定结果。
4. `q'` 是下一个状态。

### 一个最小例子与通俗解释

一个最小例子是 AnnieWAY 从 stop road 接近十字路口并左转：

1. 车辆在 `DriveOnLane` 中沿当前车道前进。
2. 检测到路口后进入 `IntersectionApproach`。
3. 若本车在 stop road 上，则转到 `IntersectionStop` 并在停止线前停车。
4. 状态机进入 `IntersectionWait`，登记其他已在等待区内的车辆。
5. 只有当 `MTC` 对所有优先车辆都给出安全结果时，才进入 `IntersectionDriveInside`。
6. 如果本车在优先路上但仍需让行左转，则进入 `IntersectionPrioStop`，待安全后再转弯。

通俗地说，这个模型像一个“会懂交通规则的层次化挡位器”：它不直接求所有控制量，而是把“正常行驶、路口等待、停车区导航、重规划、恢复”拆成不同状态，每个状态只负责一种交通语境下的局部行为。

### 运行 / 接受 / 转移语义

其运行语义可保守写成：

$$
(q_t, g_t, \pi_t, \mu_t) \xrightarrow{\delta} (q_{t+1}, \gamma_t)
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前行为状态。
2. `g_t` 是当前 route graph 上的任务上下文。
3. `\pi_t` 是当前场景评估结果。
4. `\mu_t` 是 `MTC` 判断和优先权检查结果。
5. `q_{t+1}` 是下一行为状态。
6. `\gamma_t` 是输出给闭环控制器的局部 path stub。

### 语义边界

这个模型的边界包括：

1. 它是自动驾驶行为层，不是完整的感知-定位-控制统一形式主义。
2. 它依赖场景评估、冲突空间估计和低层控制的正确性。
3. `CHSM` 主要负责离散行为决策，连续轨迹跟踪与紧急避障由下层承担。
4. 它针对 `DARPA Urban Challenge` 场景优化，并不直接覆盖开放世界驾驶中的长尾语义。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| 行为层骨架 | `$\mathcal{A} = (Q, q_0, \Sigma, \delta, G, \Pi, \Gamma)$` | 明确把任务图、场景评估和路径输出压进同一行为层。 |
| 路权时间估计 | `$t_{BP} = d_{BP} / v_B$` | 用来判断优先车辆是否会占用冲突空间。 |
| 安全转移 | `$\delta(q, \pi, \mu) = q'$` | 状态转移依赖场景与 `MTC` 结果，而不是死板脚本。 |
| 层次复用 | `$\mathrm{Drive} \supset \{\mathrm{DriveOnLane}, \mathrm{LaneChange}, \mathrm{DriveKTurn}\}$` | 用父状态复用共同行为，减少状态冗余。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Drive`、`Intersection`、`Zone`、`Replan`、`Recover` 等层次明确。 |
| 事件 / 触发 | 强支持 | intersection ahead、queue ahead、goal reached、lane free 等直接触发转移。 |
| 守卫 / 数据 | 强支持 | 路权、冲突空间、`MTC`、路网边序列都进入 guard。 |
| 层次 | 强支持 | 典型 `CHSM`，父状态与子状态职责清楚。 |
| 并发 / 同步 | 中等支持 | 论文强调 concurrent hierarchical state machine，但并发主要服务复杂驾驶语境组织。 |
| 时间约束 | 中等支持 | 依赖到达时间、停止等待与 hysteresis，但不是显式 timed automata。 |
| 连续动态 / 随机性 | 中等支持 | 连续车辆动力学在下层存在，高层仍是离散行为监督。 |
| 可执行 / 可验证性 | 强执行、有限验证 | 真车竞赛验证充分，但未走形式验证路线。 |

### 形式化问题与性质

1. 论文把自动驾驶行为规划从“规则集合”整理成了可层次化组织的显式状态机。
2. `MTC` 让状态切换不仅看交通规则，还看时空安全窗口。
3. path stub 输出说明高层状态机与下层轨迹跟踪之间有清晰接口。
4. 对 `project_1` 来说，这类条目特别适合抽“需求语句 -> 交通情境状态 -> 安全守卫 -> 局部路径输出”。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. mission planner 先在道路图上给出边序列。
2. 场景评估模块识别当前是车道、路口、停车区还是阻塞恢复。
3. `CHSM` 依据场景和 `MTC` 切换状态。
4. 当前状态负责生成 path stub 并交给控制器。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. `UML state chart` 形式的层次状态图。
2. graph-based mission route。
3. 场景评估模块输出的 conflict situation / conflict space 描述。
4. 传给闭环控制器的 path stub 与 waypoint 序列。

### 交换与互操作

互操作重点在：

1. mission planner 给状态机提供边序列目标。
2. perception / situation assessment 给状态机提供交通场景。
3. `CHSM` 给低层控制与避障提供路径段。
4. 低层 avoidance system 在必要时可覆盖状态机输出。

## 配套基础设施

- 建模/编辑工具：论文直接使用 `UML state chart` 描述主状态与子状态。
- 解析/交换/元模型支持：mission route graph、场景评估模块、path stub 接口。
- 仿真/执行支持：`VW Passat Variant`、64 线激光雷达、2D 激光、`DGPS/INS`、ECU。
- 验证/分析支持：`DARPA Urban Challenge 2007` 的真实竞赛场景与多类驾驶机动。
- 代码生成/转换支持：原文未给自动代码生成链，主要是软件架构与实时实现。
- 标准化或社区生态：依托自动驾驶研究、`UML` 状态图和 Karlsruhe/TUM 的车辆平台生态。

## 适用场景与需求前提

### 适用场景

适合城市道路自动驾驶中的行为层规划，尤其是需要把交通规则、路口让行、停车区导航、重规划和恢复策略压成少量高层模式的场景。

### 需求前提

1. 任务可先压成道路图上的路由问题。
2. 感知系统能给出稳定的交通参与者和路权场景。
3. 连续控制和局部避障有独立下层可以承接。
4. 需要用少量离散行为模式封装复杂交通策略。

### 不适用或高成本场景

如果场景语义极开放、地图不稳定、感知误差很大，或行为策略需要大规模学习式重规划，这种 `CHSM` 会面临维护成本和状态爆炸压力。

## 与相邻形式主义的关系

它本质上是 `UML/Statechart` 风格层次状态机在自动驾驶行为层的工程化落地。相对普通 `FSM`，它显式利用层次与恢复子状态来控制复杂场景；相对行为树，它更强调基于交通语境的稳定 mode switch；相对 `SMACH/RAFCON` 这类任务状态机，它更贴近道路交通规则与路权推理。

## 与本研究的关系

### 对 Project 1 的价值

它非常适合作为“复杂控制需求如何被压成层次状态机”的高质量样本，尤其适合抽取交通法规、让行关系和恢复策略这类高价值守卫。

### 作为目标形式主义还是中间表示

对自动驾驶行为层来说，它可以直接作为目标形式主义；对更大的机器人系统来说，它更适合作为上层任务监督器的中间表示。

### 对需求到模型生成的启发

1. 交通规则可直接转成状态守卫和优先权分支。
2. `MTC` 说明安全判定最好显式建成状态转移条件。
3. 层次状态能显著减轻复杂交通任务的平铺爆炸。
4. path stub 输出接口提示状态机应与连续控制层解耦。

### 现实限制

该模型严重依赖高质量感知、地图和场景解释；如果这些输入不稳，层次状态机再精细也无法独立保证行为正确。

## 重要的相关工作

- `DARPA Grand Challenge 2005/2007`：论文直接依托其竞赛场景与规则集。
- `Cognitive Automobiles` 项目：AnnieWAY 的软件架构与研究主线来源。
- 车辆动态避障与闭环轨迹跟踪工作：作为 `CHSM` 下游执行层前提。
- `UML Statecharts` / 层次状态机路线：为该行为层提供了结构化表达基础。

## 文献分类总结

- 这是一篇 `📦` 类应用型状态机条目，核心价值是自动驾驶行为层 `CHSM` 的工程组织，而不是提出新的理论自动机。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；语境是城市自动驾驶 `CPS`，因此领域记为 `🌡️`。
- 对 `project_1` 来说，它补的是“复杂交通需求如何被层次化状态机稳定承载”的关键证据。
