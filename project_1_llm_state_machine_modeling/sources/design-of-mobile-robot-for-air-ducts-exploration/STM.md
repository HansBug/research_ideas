# Design of a Mobile Robot for Air Ducts Exploration - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（普通离散状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对通风管道巡检机器人的五状态导航 FSM、异常分支和恢复动作写得比较清楚，可直接作为机器人高层离散控制样本。

## 条目 1: Five-state exploration and recovery FSM for an air-duct robot
- 控制对象：通风管道巡检机器人的高层导航与恢复控制器
- 状态机类型：FSM（普通离散状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是移动机器人导航领域的 high-level exploration controller，用于在目标推进、洞口处理、返航和恢复之间切换，保证机器人在通风管道网络里安全完成探索。
- 判断：算。对象是实际巡检机器人高层控制器，原文明确给出了状态集合、异常触发、状态动作和恢复分支。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，`Figure 8 / State Sa:Snooze`
> Figure 8. Finite state machine describing the high level behavior of the robot during the navigation.
>
> The states are: Snooze (Sa), Navigate (Sb), Hole Area (Sc), Return (Sd), Recovery (Se).
>
> The Snooze state is an abstraction that models the intermittent stops between two consecutive instances of the Navigate state.

#### 摘录 B
- 出处：第 10 页，`State Sb:Navigate / State Sc:Hole Area / State Sd:Return`
> The Navigate state is the most crucial state in the FSM ... the robot attempts to reach the target goal computed by the navigation algorithm ...
>
> The robot is stuck ... the state changes to Recovery.
>
> The robot detects a trapdoor opening/hole in which case the state changes to Hole Area.
>
> When the exploration is deemed complete ... the state changes to Return.
>
> On reaching [Hole Area], the robot runs a procedure that marks as dangerous the cells ... considers the associated duct section as a dead-end and turns around to continue to the next goal in the exploration stack.

#### 摘录 C
- 出处：第 10-11 页，`State Se:Recovery`
> The Recovery state handles both cases where the robot is stuck or a dead-end has been reached.
>
> When the robot is stuck, rotate_recovery ... rotates the robot 360 deg ... in an attempt to clear and free neighboring cells ...
>
> The recovery action for a dead-end is to backtrack the robot by a few centimeters, perform an in place rotation of 180 deg, after which the robot proceeds to the next goal position in the exploration stack.
>
> Before the robot is backtracked, the sweeping arm is retracted close to the robot ...

### 2. 基于原文整理后的自然语言描述

The air-duct exploration robot uses a five-state high-level FSM with `Snooze`, `Navigate`, `Hole Area`, `Return`, and `Recovery` to supervise navigation inside the duct network. `Snooze` models the intermittent stop between two navigation attempts while the duct-navigation node refreshes the custom costmap and computes the next goal pose. In `Navigate`, the robot follows the current target goal, but if it gets stuck or reaches a dead-end it transitions to `Recovery`, if it detects a trapdoor opening it transitions to `Hole Area`, and if the exploration criteria report completion it transitions to `Return`. `Hole Area` marks the reachable part of the detected hole as dangerous in the costmaps, treats the duct section as a dead-end, and either turns around toward the next exploration goal or moves to `Return` when the exploration stack is empty. `Recovery` distinguishes between two abnormal cases: it invokes `rotate_recovery` to spin and clear local costmaps when the robot is stuck, or it retracts the sweeping arm, backtracks a short distance, rotates 180 degrees, and resumes with the next goal when a dead-end has been reached.

### 3. 逐句溯源

1. 句子 1：The air-duct exploration robot uses a five-state high-level FSM with `Snooze`, `Navigate`, `Hole Area`, `Return`, and `Recovery` to supervise navigation inside the duct network.
   对应摘录：A
2. 句子 2：`Snooze` models the intermittent stop between two navigation attempts while the duct-navigation node refreshes the custom costmap and computes the next goal pose.
   对应摘录：A
3. 句子 3：In `Navigate`, the robot follows the current target goal, but if it gets stuck or reaches a dead-end it transitions to `Recovery`, if it detects a trapdoor opening it transitions to `Hole Area`, and if the exploration criteria report completion it transitions to `Return`.
   对应摘录：B
4. 句子 4：`Hole Area` marks the reachable part of the detected hole as dangerous in the costmaps, treats the duct section as a dead-end, and either turns around toward the next exploration goal or moves to `Return` when the exploration stack is empty.
   对应摘录：B
5. 句子 5：`Recovery` distinguishes between two abnormal cases: it invokes `rotate_recovery` to spin and clear local costmaps when the robot is stuck, or it retracts the sweeping arm, backtracks a short distance, rotates 180 degrees, and resumes with the next goal when a dead-end has been reached.
   对应摘录：C
