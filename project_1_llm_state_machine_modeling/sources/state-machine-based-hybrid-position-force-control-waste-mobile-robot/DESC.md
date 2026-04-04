# 面向垃圾分拣移动机器人的状态机驱动位置/力混合控制架构 / State Machine-Based Hybrid Position/Force Control Architecture for a Waste Management Mobile Robot with 5DOF Manipulator

## 基本信息

- **标题**：State Machine-Based Hybrid Position/Force Control Architecture for a Waste Management Mobile Robot with 5DOF Manipulator
- **中文标题**：面向垃圾分拣移动机器人的状态机驱动位置/力混合控制架构
- **作者**：Ionel-Alexandru Gal，Alexandra-Cătălina Ciocîrlan，Mihai Mărgăritescu
- **单位**：
  - Institute of Solid Mechanics of Romanian Academy
  - National Institute of Research and Development for Mechatronics and Measurement Technique
- **发表**：Applied Sciences，2021
- **DOI**：10.3390/app11094222
- **链接**：https://doi.org/10.3390/app11094222

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文把 `SmHPFC` 的主状态机、子状态机、状态表和回收任务算法写到了可直接提取的程度，可作为控制系统案例直接使用。

### 数据集/案例获取方式

- 原文未提供单独数据集。
- 论文给出了垃圾分拣移动机器人 5DOF 机械臂的 pick-and-drop 任务链、状态切换与控制模式切换逻辑，适合直接作为 source paper 收纳。

## 简报

这篇论文解决的是**垃圾分拣移动机器人上的 5DOF 机械臂如何在同一任务中切换位置控制与力控制来完成抓取和投放**的问题。输入是目标类型、目标位姿、目标抓取力、位置误差和力误差，方法是把经典 hybrid position/force control 外包一层分层状态机 `SmHPFC`，输出是 `Main/Homing -> Position Control -> Force Control -> Drop -> New Task` 的完整 pick-and-drop 监督控制链。

- **输入**：object type、target coordinates、gripper rotation、reference force、position error、force error、emergency stop。
- **方法**：基于 `state machine + S-matrix` 的混合位置/力控制切换架构，包含 homing、position control、force control 三组子状态机。
- **输出**：目标定位、对准、抓取、抬升、移送到回收托盘、开爪投放与异常停止控制链。
- **一句话评价**：这是高质量的 `HSM + T0` 机械臂任务控制样本，主状态表、子状态机和抓取/投放流程都足够完整。

## 控制系统与状态机证据

### 控制对象

论文对象是垃圾分拣移动机器人上的 5DOF 机械臂控制器。它负责决定系统何时执行 homing、何时采用位置控制对准目标、何时切换到力控制闭合夹爪，以及何时恢复位置控制并把物体投放到回收托盘。

### 状态机组织方式

原文把该控制器明确写成 `state machine-based hybrid position/force control architecture (SmHPFC)`。主结构包含：

1. `Si1 Main`
2. `Si2 Main/Homing`
3. `Si3 All`
4. `SC1 Main`
5. `SC2 Main/Force Control`
6. `SC3 Main/Force Control`
7. `SC4 Main/Position Control/Force Control`
8. `SC5 Position Control`
9. `SES Position Control/Force Control`

同时又细分出：

1. `Homing` 子状态机
2. `Position Control` 子状态机
3. `Force Control` 子状态机

### 关键控制链

论文给出的任务链很完整：

- 系统上电后先依次对五个 DOF 执行 `Homing`，完成后进入稳定态 `Si3`。
- 收到新任务后，先在 `SC1` 用位置控制完成 `XOY` 平面定位与夹爪朝向对准。
- 随后转入 `SC2/SC3`，继续完成 `OZ` 方向定位并把 gripper 控制从 position 切到 force，通过更新 `S-matrix` 执行抓取。
- 力控制稳定持物后，系统抬起目标并移向回收托盘，再在 `SC4/SC5` 切回位置控制、开爪丢弃物体，最后回到可接受新任务的状态。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实机器人执行机构监督控制器**，不是泛泛的控制理论论文。
- 原文同时保留了状态名、状态层次、状态含义、抓取力/位置误差和控制模式切换逻辑，特别适合提取成带 guard 的自然语言状态机样本。
- 对“任务链驱动的 position-control / force-control 切换”这一类复杂执行器控制尤其有价值。

### 可直接借鉴之处

- 可以直接借鉴主状态机 + 子状态机的层次建模方式。
- 可以直接借鉴 `定位 -> 纵向对准 -> 力控抓取 -> 抬升移送 -> 开爪投放` 的典型抓取链。
- 可以直接借鉴 `S-matrix` 更新触发控制模式切换的写法。

### 局限性

- 论文较强调控制架构本身，低层环境感知与目标检测细节不是主体。
- 时间语义主要体现为顺序阶段与稳定条件，不是显式 timer 约束。
- 机械臂动作与任务流程很清楚，但移动底盘部分并不是本文核心。

## 文献分类总结

- **文献类型**：真实机器人执行机构控制案例论文
- **控制对象**：垃圾分拣移动机器人 5DOF 机械臂监督控制器
- **状态机画像**：`HSM + T0`
- **证据强度**：主状态表、子状态机与 pick-and-drop 全流程明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充机械臂抓取任务链、控制模式切换和执行器监督控制样本
