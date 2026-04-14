# An Autonomous Navigation Framework for Holonomic Mobile Robots in Confined Agricultural Environments - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把温室全向移动机器人的任务控制明确组织成 `WAIT_FOR_GOAL / PLAN_EXEC / VISUAL_SERVOING` 层次状态机，并写清了行首对齐、行内巡检、回退与失败返初始化链。

## 条目 1: Greenhouse row-inspection navigation supervisor
- 控制对象：温室全向移动机器人的高层导航与巡检监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个温室移动机器人在 headland 与 crop row 之间切换时使用的层次任务状态机，用于调度 mission 装载、waypoint 导航、rail alignment 和行内巡检。
- 判断：算。对象是真实农业机器人平台上的任务监督控制器，不是单纯感知或导航算法流程；原文给出了主状态块、子状态和失败回退链，足以恢复高层控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> Our approach utilizes the heating system rails to navigate through the crop rows using a single stereo camera for perception and a LiDAR sensor for accurate distance measurements. A finite state machine orchestrates the sequence of required actions, enabling fully automated task execution.

#### 摘录 B
- 出处：第 9-10 页，Section 3.4 `Overall Navigation Pipeline`
> The initial stage in the pipeline commences with robot initialization, encompassing the acquisition of both the greenhouse occupancy grid map and the user's mission instructions, which specify the rows to be inspected.
>
> The navigation of the robotic platform towards the target row first requires the navigation within the headland, at one of the pre-known targets on the map.
>
> The next step is to perform the robot alignment with the corridor rails ... in order to prepare for the in-row forward navigation task, which follows.
>
> The robot iteratively performs all the required inspection tasks within the operating row and, once these targets are completed, the robot performs in-row backward navigation in order to place itself back on the headland.

#### 摘录 C
- 出处：第 10 页，Section 3.4 / Figure 8
> The robot initialization is equivalent to the WAIT_FOR_GOAL state.
>
> When a mission is provided to the robot, there is a transition to the PLAN_EXEC block, which contains the headland planning that is performed by the Timed Elastic Band (TEB) Local Planner.
>
> When that block finishes successfully, there is a transition to the VISUAL_SERVOING block, which is responsible for the in-row processes.

#### 摘录 D
- 出处：第 10 页，Section 3.4 / Figure 8
> Specifically, the robot performs the TARGET_ALIGNMENT phase once, followed by an iterative process between the states TRAVERSE_FORWARD, INSPECT and TRAVERSE_BACKWARD.
>
> When the in-row task is completed, the FSM returns to the WAIT_FOR_GOAL state again.
>
> It must be noted that any failure that may occur throughout the entire operation returns to a common state, which is reported as invalid, aborted, or a failure, and then to the initialization state.

### 2. 基于原文整理后的自然语言描述

The greenhouse robot supervisor is organized as a hierarchical state machine whose top-level flow begins in `WAIT_FOR_GOAL`, where the system loads the greenhouse occupancy grid and the user-specified row mission. Once a mission is available, the controller enters `PLAN_EXEC` to drive through the headland toward the waypoint of the target corridor using the TEB-based navigation block. After successful arrival, control transfers to the `VISUAL_SERVOING` block, which first executes `TARGET_ALIGNMENT` so that the platform is aligned with the corridor rails before entering in-row motion. The in-row process then iterates through `TRAVERSE_FORWARD`, `INSPECT`, and `TRAVERSE_BACKWARD` until the inspection targets of the current row are completed and the robot is placed back on the headland. Any invalid, aborted, or failed action routes execution to a common failure outcome and then back to the initialization state, so completion and recovery are both explicit in the control loop.

### 3. 逐句溯源

1. 句子 1：The greenhouse robot supervisor is organized as a hierarchical state machine whose top-level flow begins in `WAIT_FOR_GOAL`, where the system loads the greenhouse occupancy grid and the user-specified row mission.
   对应摘录：A, B, C
2. 句子 2：Once a mission is available, the controller enters `PLAN_EXEC` to drive through the headland toward the waypoint of the target corridor using the TEB-based navigation block.
   对应摘录：B, C
3. 句子 3：After successful arrival, control transfers to the `VISUAL_SERVOING` block, which first executes `TARGET_ALIGNMENT` so that the platform is aligned with the corridor rails before entering in-row motion.
   对应摘录：B, C, D
4. 句子 4：The in-row process then iterates through `TRAVERSE_FORWARD`, `INSPECT`, and `TRAVERSE_BACKWARD` until the inspection targets of the current row are completed and the robot is placed back on the headland.
   对应摘录：B, D
5. 句子 5：Any invalid, aborted, or failed action routes execution to a common failure outcome and then back to the initialization state, so completion and recovery are both explicit in the control loop.
   对应摘录：D
