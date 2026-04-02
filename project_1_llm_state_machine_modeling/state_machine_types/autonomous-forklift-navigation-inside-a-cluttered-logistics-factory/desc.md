# 面向拥挤物流工厂的自主叉车导航状态机 / Autonomous Forklift Navigation Inside a Cluttered Logistics Factory

## 基本信息

- 标题：Autonomous Forklift Navigation Inside a Cluttered Logistics Factory
- 中文标题：面向拥挤物流工厂的自主叉车导航状态机
- 作者：Eric Lucet, Antoine Lucazeau, Jason Chemin
- 发表：*Proceedings of the 21st International Conference on Informatics in Control, Automation and Robotics (ICINCO 2024)*, pp. 327-335
- DOI：`10.5220/0013067600003822`
- 链接：https://doi.org/10.5220/0013067600003822
- 形式主义：`Forklift Navigation FSM`
- 主类：📦
- 描述客体：🎛️
- 所属领域：🏭
- 论文角色：工厂物流叉车导航 / planner-controller switching `FSM`
- 工具/实现获取方式：原文直接给出 road network、modified `A*` local planner、`CLMPC` controller、`ROS Gazebo` 仿真和 `TwinswHeel facTHory` 叉车原型；未给公开仓库。
- 标准/格式获取方式：原文没有独立交换标准，主要承载方式是 road-network map、corridor constraints、`FSM` supervisor 与 `ROS/Gazebo` 软件栈。

## 简报

这篇论文把物流工厂里的自主叉车导航做成了一个很典型的**离散 supervisor + 连续控制器**组合：上层 `FSM` 只管 `Rotate / Move / Avoid` 三个 operating modes 的切换，下层则由 global path、modified `A*` local planner 和 `CLMPC` 负责具体路径与控制约束。

- 形式主义定位：面向狭窄工厂 corridor 的导航监督状态机，用于协调规划器与路径跟踪控制器。
- 构造方式简述：先在已有 road network 上做全局选路，再由 `FSM` 决定何时旋转、跟踪和避障，连续控制层用 corridor-constrained `CLMPC` 保证安全。
- 基础设施与场景简述：依托 `ROS Gazebo`、真实 forklift droid、激光 / 视觉感知和动态 corridor 约束，服务纸卷/纸箱在印刷工厂内的自动搬运。

```text
运输任务 -> road network global path -> FSM( Rotate / Move / Avoid ) -> A* / CLMPC -> 工厂叉车执行
```

## 形式主义定义与核心对象

### 定义对象

论文中的关键对象包括：

1. 全局 road network。
2. modified `A*` local path planner。
3. `CLMPC` path-tracking controller。
4. navigation corridors 与 dynamic corridor。
5. `Rotate / Move / Avoid` 三态 `FSM`。
6. `TwinswHeel facTHory` forklift droid。

### 核心抽象

按论文结构，可把高层 supervisor 保守整理为：

$$
\mathcal{F} = (Q, q_0, \Sigma, \delta, \mathcal{N}, \mathcal{C})
$$

上式中的符号逐项解释如下：

1. `Q = \{\mathrm{Rotate}, \mathrm{Move}, \mathrm{Avoid}\}` 是状态集合。
2. `q_0` 是初始状态，通常由任务起点与姿态决定。
3. `\Sigma` 是 obstacle detection、alignment complete、corridor clear 等事件集合。
4. `\delta` 是三态之间的转移关系。
5. `\mathcal{N}` 是全局 road network。
6. `\mathcal{C}` 是 corridor 约束集合。

论文直接给出了 `CLMPC` 预测模型：

$$
Y = A y_0 + B U + C
$$

上式中的符号逐项解释如下：

1. `Y` 是预测状态向量。
2. `y_0` 是当前误差状态。
3. `U` 是未来控制输入向量。
4. `A` 与 `B` 是状态矩阵。
5. `C` 是由路径曲率 `c_m` 导出的项。

论文还给出了 corridor 边界约束的一类形式：

$$
-\delta_r < y \pm D \sin \theta \pm \frac{W}{2}\cos \theta < \delta_l
$$

上式中的符号逐项解释如下：

1. `y` 是相对参考路径的横向偏差。
2. `D` 表示前端或后端到控制点的纵向距离，如 `D_f` 或 `D_r`。
3. `\theta` 是叉车相对路径方向的朝向误差。
4. `W` 是车体宽度。
5. `\delta_l` 和 `\delta_r` 分别是左右 corridor 容差。

### 一个最小例子与通俗解释

最小例子是从工厂的 `site A` 把纸箱运到 `site B`：

1. global planner 先在 road network 上选出一条可行路线。
2. 机器人进入 `Rotate`，把车身姿态对准当前 corridor。
3. 然后进入 `Move`，仅用 `CLMPC` 沿 corridor 中心跟踪路径。
4. 若前方 corridor 中出现静态或动态障碍，则切到 `Avoid`。
5. 在 `Avoid` 中，local planner + `CLMPC` 联合生成绕障路径。
6. 障碍清除后，再切回 `Move` 继续前进。

通俗地说，这个模型像一个“叉车导航挡位器”：高层并不直接算所有控制量，而是只决定“先转正、再直走、遇障就绕”，具体怎么走由控制器和局部规划器负责。

### 运行 / 接受 / 转移语义

其高层转移语义可以写成：

$$
(q_t, \sigma_t, n_t, c_t) \xrightarrow{\delta} q_{t+1}
$$

上式中的符号逐项解释如下：

1. `q_t` 是当前 operating mode。
2. `\sigma_t` 是当前事件，如 obstacle detected 或 corridor cleared。
3. `n_t` 是当前全局/局部路径信息。
4. `c_t` 是当前 corridor 约束。
5. `q_{t+1}` 是下一 operating mode。

### 语义边界

这个模型的边界包括：

1. 它服务的是结构化室内 corridor 导航，不是开放环境自动驾驶。
2. 高层 `FSM` 只协调 planning / tracking modes，不负责复杂任务规划。
3. 对地图、corridor 和 forklift 几何尺寸有较强依赖。
4. 动态环境过于复杂时，需要更强的 local planner 和更快控制频率。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| supervisor 骨架 | `$\mathcal{F} = (Q, q_0, \Sigma, \delta, \mathcal{N}, \mathcal{C})$` | `FSM` 负责协调模式切换，不直接替代规划器和控制器。 |
| 三态集合 | `$Q = \{\mathrm{Rotate}, \mathrm{Move}, \mathrm{Avoid}\}$` | 叉车的关键 operating modes 被清楚离散化。 |
| 预测模型 | `$Y = A y_0 + B U + C$` | `CLMPC` 在状态机之下提供可约束的连续控制。 |
| corridor 约束 | `$-\delta_r < y \pm D \sin \theta \pm \frac{W}{2}\cos \theta < \delta_l$` | 叉车前后端和宽度都被纳入安全边界约束。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 强支持 | `Rotate / Move / Avoid` 三态明确。 |
| 事件 / 触发 | 强支持 | obstacle detection、alignment completion、corridor clear 等触发转移。 |
| 守卫 / 数据 | 强支持 | corridor 约束、车体几何和路径信息都作为 guards。 |
| 层次 | 弱支持 | 高层 supervisor 较简单。 |
| 并发 / 同步 | 弱支持 | 重点是单车导航。 |
| 时间约束 | 弱支持 | 有 prediction horizon，但无离散时钟自动机语义。 |
| 连续动态 / 随机性 | 中等支持 | 连续部分由 `CLMPC` 负责，高层仍是离散模式切换。 |
| 可执行 / 可验证性 | 强执行、有限验证 | 仿真与实机都验证了效果，但非形式验证体系。 |

### 形式化问题与性质

1. 论文最有价值的点，是把 planner-controller interaction 变成显式 `FSM` 监督关系。
2. corridor constraints 说明“车体几何 + 安全边界”应直接进入状态机上下文。
3. predictive safety stop 说明状态机不只是切模式，也承载安全决策入口。
4. 对 `project_1` 来说，这类条目很适合抽取“离散 mode supervisor + 连续控制器”组合模式。

## 构造方式与承载格式

### 建模入口

建模入口主要包括：

1. 用工厂 road network 提供全局导航骨架。
2. 用 local planner 处理局部绕障。
3. 用 `FSM` 组织 operating modes。
4. 用 `CLMPC` 在 corridor 约束下执行连续跟踪。

### 机器可处理承载方式

原文直接给出的承载方式包括：

1. road network 图。
2. `FSM` operating modes。
3. `A*` 局部路径表示。
4. `CLMPC` 状态与约束矩阵。

### 交换与互操作

互操作重点在：

1. global planner 提供粗路径。
2. `FSM` 决定何时启用 rotate / follow / avoid。
3. local planner 与 `CLMPC` 在 `Avoid` 状态联用。
4. `ROS Gazebo` 与实机原型共同承担验证。

## 配套基础设施

- 建模/编辑工具：road-network map、navigation stack 配置、`FSM` supervisor。
- 解析/交换/元模型支持：local path、dynamic corridor 和 `CLMPC` 状态/约束模型。
- 仿真/执行支持：`ROS Gazebo`、真实 `TwinswHeel facTHory` forklift、激光与视觉系统。
- 验证/分析支持：多种障碍场景下的 simulated / real experiments，对比 `A*` 与 `TEB`。
- 代码生成/转换支持：原文未强调自动代码生成，主要是算法和 supervisor 集成。
- 标准化或社区生态：依托 ROS / industrial AMR / logistics robotics 生态。

## 适用场景与需求前提

### 适用场景

适合工厂、仓储、印刷车间等 corridor 结构清晰、叉车几何约束明显、且需要稳定避障和路径跟踪的物流场景。

### 需求前提

1. 存在可用的全局路网。
2. corridor 边界和 forklift 几何尺寸可建模。
3. 障碍物可被本地感知系统及时检测。
4. 高层只需有限 operating modes 即可表达导航逻辑。

### 不适用或高成本场景

若环境缺少稳定 corridor 结构、动态障碍过多或车速要求远高于文中设置，该 `FSM + A* + CLMPC` 组合会面临明显扩展压力。

## 与相邻形式主义的关系

相对纯导航栈，它增加了显式 `FSM` supervisor；相对自动驾驶多层行为状态机，它更窄、更任务化，只处理狭窄工厂导航；相对纯 `FSM` 变道控制器，它更强调规划器与控制器的协同切换，而不是直接对车辆动作做全离散控制。

## 与本研究的关系

### 对 Project 1 的价值

这篇论文很好地展示了如何从工业物流需求中抽出少量 operating modes，再把连续控制留给下层。

### 作为目标形式主义还是中间表示

它更适合作为中高层目标形式主义，即连续导航系统之上的 supervisor 状态机。

### 对需求到模型生成的启发

1. 需求里“何时旋转、何时跟踪、何时绕障”非常适合直接抽成状态。
2. 车体几何和 corridor 约束应作为 guard 或附属约束对象建模。
3. planner / controller switching 是一种稳定可复用的需求模式。
4. safety stop 最好作为显式状态机行为，而不是隐式嵌在控制器里。

### 现实限制

它仍然依赖现成规划器、地图和感知系统；状态机本身不解决全局物流调度和复杂多车协同。

## 重要的相关工作

- `CLMPC` 相关先前工作：论文明确从已有控制器路线做适配。
- `A*` 与 `TEB`：文中直接比较的局部规划路线。
- forklift 几何与工业 AMR 导航研究：作为 use case 背景。
- `ROS Gazebo`：构成从仿真到实机迁移的基础设施。

## 文献分类总结

- 这是一篇 `📦` 类应用监督器条目，重点是工厂叉车导航中 planner / controller 的状态机切换。
- 它主要描述控制 / 反应式逻辑，因此记为 `🎛️`；场景属于工业物流与自动化，因此领域记为 `🏭`。
- 对 `project_1` 来说，它补的是“工业物流导航如何抽象成少量 operating modes 并与连续控制器衔接”。
