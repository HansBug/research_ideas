# 小型无人机自主搜索与跟踪一体化系统 / An Integrated System for Autonomous Search and Track with a Small Unmanned Aerial Vehicle

## 基本信息

- **标题**：An Integrated System for Autonomous Search and Track with a Small Unmanned Aerial Vehicle
- **中文标题**：小型无人机自主搜索与跟踪一体化系统
- **作者**：Anjan Chakrabarty，Robert A. Morris，Xavier Bouyssounouse，Rusty Hunt
- **单位**：
  - Stinger Ghaffarian Technologies Inc.
  - NASA Ames Research Center
- **发表**：AIAA Information Systems-AIAA Infotech @ Aerospace，2017
- **DOI**：10.2514/6.2017-0671
- **链接**：https://doi.org/10.2514/6.2017-0671

### 代码/仓库获取方式

- 原文围绕 `ROS` 与 `SMACH` 实现 search-and-track autonomy，但未给出独立公开仓库链接。
- 论文明确说明系统运行在 `Parrot AR.Drone` 平台之上，并集成 `human detector`、`face detector`、`CMT tracker` 与 `IBVS` 控制器，可直接作为任务控制案例阅读。

### 数据集/案例获取方式

- 原文未提供单独下载的数据集。
- 论文给出了 simulation 与 indoor flight test 的任务链、状态切换、追踪置信度回退和安全监控逻辑，可直接作为单案例 source paper 使用。

## 简报

这篇论文解决的是**小型无人机如何在无人值守条件下完成起飞、搜索、确认目标并持续跟踪**的问题。输入是通信链路、剩余电量、人体检测器、面部检测器和 tracker 置信度，方法是用 `SMACH` 组织一个带并发监控的层次状态机，输出是 `TAKEOFF -> SEARCH -> INVESTIGATE -> TRACK` 的完整任务控制链。

- **输入**：battery level、communication status、human detector、face detector、tracker confidence。
- **方法**：基于 `ROS/SMACH` 的层次并发状态机，加上 `CMT` 跟踪器与 `IBVS` 视觉伺服控制。
- **输出**：自主起飞、搜索、确认、跟踪、失跟回搜和低电量/失联受控降落控制链。
- **一句话评价**：这是很标准的 `HSM + T0` 航空任务控制样本，主状态、并发监控、回退条件和跟踪保持逻辑都足够明确。

## 控制系统与状态机证据

### 控制对象

论文对象是 `Parrot AR.Drone` 小型无人机上的 search-and-track autonomy controller。它负责在 mission 中决定何时起飞、何时执行自旋或航点搜索、何时切入目标确认，以及何时进入持续跟踪或中止任务。

### 状态机组织方式

原文把高层控制明确写成 `Hierarchical Finite State Machine`，并使用 `SMACH` 承载。主链包括：

1. `MONITOR`
2. `TAKEOFF`
3. `SEARCH`
4. `INVESTIGATE`
5. `TRACK`

其中 `MONITOR` 是并发运行的安全子状态机，持续检查通信和电量；`SEARCH` 又区分 `SPIN SEARCH` 与 `WAY POINT search` 两种搜索子策略。

### 关键控制链

论文把主控制链写得很清楚：

- `MONITOR` 持续运行，只要通信异常或电池低于安全阈值就触发 mission abort 和 controlled land。
- 系统确认可以继续后进入 `TAKEOFF`，随后立刻切入 `SEARCH`。
- `SEARCH` 中只要人体检测器命中目标，就进入 `INVESTIGATE` 悬停确认。
- `INVESTIGATE` 中需要 human detector 与 face detector 同时为真，确认后再初始化 tracker 并切到 `TRACK`。
- `TRACK` 期间若 tracker confidence 低于阈值，则回退到 `SEARCH`；若重新获得目标，则可直接跳回 `TRACK`。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实无人机任务监督器**，不是单纯视觉算法论文。
- 状态机中的输入、守卫、状态动作和回退链都可直接转写成自然语言状态机描述样本。
- `MONITOR` 并发安全链对后续研究异常恢复和 fail-safe 建模也很有价值。

### 可直接借鉴之处

- 可以直接借鉴 `MONITOR` 并发安全子状态机与主任务状态机并行运行的表达。
- 可以直接借鉴 `SEARCH -> INVESTIGATE -> TRACK` 这种“先发现、再确认、再持续跟踪”的监督控制模板。
- 可以直接借鉴 tracker confidence 下降后回退 `SEARCH` 的回环式任务控制链。

### 局限性

- 论文重点仍有一部分落在视觉跟踪与 `IBVS` 控制实现，低层连续控制细节较多。
- `SEARCH` 的低层路径规划只给出 `SPIN SEARCH` 与 `WAY POINT search` 的任务意图，没有展开更细航迹优化算法。
- 时间语义主要体现在任务顺序和安全阈值，不是显式定时器驱动。

## 文献分类总结

- **文献类型**：真实无人机任务控制案例论文
- **控制对象**：小型无人机 search-and-track autonomy controller
- **状态机画像**：`HSM + T0`
- **证据强度**：主状态、并发监控、目标确认和失跟回退链都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充空中平台任务监督与异常中止类控制样本
