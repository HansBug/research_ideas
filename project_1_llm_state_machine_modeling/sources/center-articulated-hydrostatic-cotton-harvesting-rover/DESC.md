# 采用视觉伺服与有限状态机的中心铰接式棉花采摘车 / Center-Articulated Hydrostatic Cotton Harvesting Rover Using Visual-Servoing Control and a Finite State Machine

## 基本信息

- **标题**：Center-Articulated Hydrostatic Cotton Harvesting Rover Using Visual-Servoing Control and a Finite State Machine
- **中文标题**：采用视觉伺服与有限状态机的中心铰接式棉花采摘车
- **作者**：Kadeghe Fue，Wesley Porter，Edward Barnes，Changying Li，Glen Rains
- **单位**：
  - College of Engineering, University of Georgia
  - Department of Entomology, University of Georgia
  - Department of Crop and Soil Sciences, University of Georgia
  - Cotton Incorporated
- **发表**：Electronics，2020
- **DOI**：10.3390/electronics9081226
- **链接**：https://doi.org/10.3390/electronics9081226

### 代码/仓库获取方式

- 原文未提供独立公开代码仓库。
- 论文明确说明系统使用 `ROS`、`SMACH`、`YOLO` 检测和视觉伺服控制，但更重要的是把 rover/manipulator 的任务状态机和决策算法完整写了出来。

### 数据集/案例获取方式

- 原文未单独发布用于本任务的数据集。
- 论文给出了中心铰接采摘车在真实棉田中的检测、对准、移动和采摘流程，可直接作为一个具备明确控制逻辑的 source case。

## 简报

这篇论文解决的是**棉花采摘车如何边沿行移动、边根据视觉检测结果调整车体和二维机械臂，最终完成棉铃采摘**的问题。输入是当前视频帧、YOLO 检测结果、棉铃三维坐标和末端执行器坐标，方法是用 `SMACH` 实现一个六状态七迁移的任务级有限状态机，输出是 `get image -> detect boll -> move forward/backward -> move arm up/down -> pick boll` 的采摘控制链。

- **输入**：current video frame、YOLO boll detections、point cloud depth、end-effector position、RTK-GNSS/PID row-following 信号。
- **方法**：`ROS + SMACH` 的 task-level FSM，结合视觉伺服、逆运动学和基于坐标差值的迁移判定。
- **输出**：重新取图、检测最近棉铃、前后移动车体、上下移动机械臂、满足距离阈值后执行采摘的完整逻辑。
- **一句话评价**：这是高质量的 `EFSM + T0` 农业采摘样本，guard 条件、动作类型和回到取图的闭环都很明确。

## 控制系统与状态机证据

### 控制对象

论文对象是中心铰接式棉花采摘车上的任务监督控制器。它负责根据视觉检测到的棉铃位置，决定何时继续行进、何时调整机械臂高度、何时触发采摘动作，以及在未检测到棉铃时如何继续沿棉行前进。

### 状态机组织方式

原文把该控制器明确写成基于 `SMACH` 的 task-level `finite state machine`。虽然图中的状态名较工程化，但正文已经给出其核心动作集合：

1. `get image`
2. `move forward`
3. `move backward`
4. `move the arm up`
5. `move the arm down`
6. `pick the boll`

这些动作通过 `7` 条迁移连接，并在每次动作后回到重新取图的入口状态形成闭环。

### 关键控制链

论文给出的采摘逻辑非常明确：

- 每轮循环先获取新图像并检测棉铃，随后选取最近棉铃并计算其三维位置 `(Xb, Yb, Zb)`。
- 若 `Yb > Ym` 或 `Yb < Ym`，系统就触发 rover 前进或后退，把车体移动到与棉铃纵向对齐的位置。
- 当纵向已对齐时，再根据 `Zm > Zb` 或 `Zm < Zb` 决定机械臂上移或下移。
- 只有当 `Yb = Ym`、`Zm = Zb` 且 `Xm - Xb < 37 cm` 时，状态机才允许进入 `pick the boll` 迁移执行采摘。

## 与本研究的关系

### 对 `project_1` 的直接价值

- 它给的是**真实农业机器人采摘监督控制器**，不是单纯视觉识别或机械结构论文。
- 原文已经把观测变量、guard 条件和动作选择规则写成近似可执行伪代码，非常适合提取成带显式 guard 的自然语言状态机样本。
- 对“感知坐标差 -> 动作决策 -> 回到感知入口”的闭环式 FSM 建模很有代表性。

### 可直接借鉴之处

- 可以直接借鉴每轮动作后返回 `get image` 再次感知的闭环设计。
- 可以直接借鉴 `Y/Z` 坐标比较驱动前后移动和上下调整的 guard 写法。
- 可以直接借鉴 `Xm - Xb < 37 cm` 这种明确数值阈值触发采摘动作的表达方式。

### 局限性

- 论文的重点之一仍是视觉检测与机械结构设计，环境建图和多机协同不是主体。
- 时间语义主要是循环顺序，不是显式 clock 或 timer。
- 图中的状态名主要靠正文解释，工程可读性强于形式化记号统一性。

## 文献分类总结

- **文献类型**：真实农业采摘机器人控制案例论文
- **控制对象**：棉花采摘车的视觉伺服任务监督控制器
- **状态机画像**：`EFSM + T0`
- **证据强度**：动作状态、guard 条件、阈值与循环入口都明确，可支撑 `🟢 A`
- **与本研究关系**：高价值 source sample，适合补充农业采摘、视觉闭环 guard 决策与移动平台-机械臂协同样本
