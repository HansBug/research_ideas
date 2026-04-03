# 面向城市道路场景的层次化自动驾驶控制系统 / A Hierarchical Control System for Autonomous Driving towards Urban Challenges

## 基本信息

- **标题**：A Hierarchical Control System for Autonomous Driving towards Urban Challenges
- **中文标题**：面向城市道路场景的层次化自动驾驶控制系统
- **作者**：Nam Dinh Van，Muhammad Sualeh，Dohyeong Kim，Gon-Woo Kim
- **单位**：Intelligent Robotics Laboratory, Department of Control and Robot Engineering, Chungbuk National University, Korea
- **发表**：Applied Sciences, 2020, 10(10): 3543
- **DOI**：10.3390/app10103543
- **链接**：https://doi.org/10.3390/app10103543

### 代码/仓库获取方式

- 原文未提供公开仓库链接。
- 论文说明系统已基于 ROS 落地，并给出决策、局部规划和控制的实现细节，但未单独公开工程代码。

### 数据集/案例获取方式

- 原文未提供外部数据集下载链接。
- 论文案例来自城市道路 proving ground 的实车试验场景，相关状态机、控制结构和实验环境在正文中描述。

## 简报

这篇论文解决的是**自动驾驶车辆如何在城市道路复杂场景下把决策、局部规划和控制整合为一套可运行的层次化控制系统**。输入是环境感知结果、任务信息与全局路径，方法是在高层使用两级 FSM 驱动 mission planning 与 control states，输出是车辆在换道、避障、启停与紧急停车场景中的决策逻辑和控制行为。

- **输入**：感知到的周围目标轨迹、任务信息、HD map 与全局路径。
- **方法**：`Mission FSM + Control FSM` 两级决策机制，配合 local path planning 和底层控制器。
- **输出**：城市路况下的自动驾驶决策与控制逻辑。
- **一句话评价**：这是一条很干净的 `HSM + T0` 样本，尤其适合补“任务态 + 子控制态”这种层次结构。

## 控制系统与状态机证据

### 任务层与控制层

论文直接把决策层拆成两级：

1. **Mission FSM**：决定车辆当前执行哪类任务。
2. **Control FSM**：在任务内部决定更细粒度的控制状态。

Mission FSM 明确包含 `Ready / Stop-and-Go / Change-Lane / E-stop / avoid obstacle` 五类状态，其中 `Change-Lane` 又含 `lane-keeping / lane-changing` 等子状态。

### 转移条件

论文给出的 Table 1 非常适合直接抽成状态机守卫，例如：

- `10 / 20 / 30 / 40`：感知层检测到紧急情况
- `23`：请求变更路径
- `41`：避障任务超时但未完成
- `32 / 42`：换道或避障任务完成

这使得它不是仅有模式名，而是真正具备可建模的转移条件。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 提供了真实自动驾驶控制器的离散决策层样本。
- 层次结构非常清晰，适合做 `HSM` 方向的训练样本。
- 与当前仓库中的 PLC/交通灯/铁路类样本相比，它补充了城市道路任务规划语义。

### 可借鉴之处

- 可以直接借鉴“mission state + nested control state”的结构化描述方式。
- 可以直接借鉴带编号的 transition condition table 写法。
- 可以直接借鉴优先级逻辑，如 `E-stop > obstacle avoidance > lane change > SAG`。

### 局限性

- 低层路径规划和控制部分仍然带有连续优化与控制内容，抽取时必须聚焦高层 FSM。
- 某些状态名和条件编码依赖 Figure 2 + Table 1 联合阅读，不像需求文档那样全文本化。
- 时间语义不强，更适合作为 `T0` 样本而不是强时间约束样本。

## 文献分类总结

- **文献类型**：真实自动驾驶控制案例论文
- **控制对象**：城市道路自动驾驶车辆高层决策器
- **状态机画像**：`HSM + T0 + 层次`
- **证据强度**：状态集合、嵌套关系与转移条件都很明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，用于补齐层次式决策控制样本
