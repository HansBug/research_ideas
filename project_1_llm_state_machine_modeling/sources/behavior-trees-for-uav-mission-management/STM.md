# Behavior Trees for UAV Mission Management - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以行为树为主，但 mission management 模块的任务状态、激活/退出和中断逻辑写得比较明确，可整理为 UAV 控制构件级样本。

## 条目 1: Task activation and interruption logic for UAV mission management
- 控制对象：无人机任务管理模块
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是无人机任务管理领域的 UAV mission management module，用于通过行为树任务层驱动 autopilot mode、payload actions、waypoint 循环和任务中断/切换。
- 判断：算，但属于控制软件构件级样本。对象是实际 UAV control loop 上方的 mission management module，原文明确给出了任务执行接口、状态返回值、激活/退出语义以及示例 mission plan。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Behavior Trees，对任务接口与 mission-management role 的说明，行 86-105
> Behavior Trees (BTs) are similar to Hierarchical Finite State Machines (HFSMs) in that they build on a hierarchy of operational modes.
>
> A task is a self-contained goal-directed behavior ... One of the simplest tasks within a UAV mission management system could be to engage a specific autopilot mode, e.g. flight level change.
>
> A complete behavior tree is executed by ticking its top-most (root) task ... When ticked, a task returns one of three status return codes: It can be finished with Success, aborted in a Failure or be Running.
>
> Actions are pieces of custom code ... such as engaging autopilot modes, switching payloads, or taking photographs.

#### 摘录 B
- 出处：第 6-10 页，Transient Behaviors / Demonstration of Application，对 activation/deactivation、internal status 与示例 mission plan 的说明，行 220-357
> Providing tasks with entry and exit hooks by using transient behaviors. This extension narrows the gap between current BT features and state machine features expected by the user.
>
> Suppose a remote sensing mission has to be aborted due to a system failure. One would wish to deactivate the power-consuming cameras during execution of the fallback behavior.
>
> A task must thus be provided with an internal status, which can at least be Idle or Running. If a currently Idle sub-task needs to be executed by its superior node, the currently Running sub-task needs to be deactivated first and the sub-task to be ticked needs to be activated.
>
> A transient task immediately returns either Success or Failure ... A non-transient task, however, will enter the new status Activating ... The actual activation is performed through the superior composite task.
>
> if the second sub-task returns Activating ... the selector thus deactivates its currently running sub-task action2 and activates the higher priority sub-task action1.
>
> The plan describes a take-off (T/O) procedure and a repeated set of waypoints to be flown subsequently ... the first part of the plan is to reach a given altitude ... if the plan is activated in the flying aircraft, no take-off is executed ... The “fly” action is deactivated first, then the “advance” action is ticked ... If the advance task fails, the internal pointer is “reset” to the first waypoint.

### 2. 基于原文整理后的自然语言描述

The UAV mission management module organizes control behavior as a hierarchy of tasks whose root task is ticked every cycle, propagating execution through composite nodes to leaf actions that can engage autopilot modes, switch payloads, or trigger mission actions such as taking photographs. Each task returns `Success`, `Failure`, or `Running`, while sequences require all subtasks to succeed in order and selectors choose among prioritized alternatives, so the tree encodes mission logic as a hierarchy of operational modes rather than as flat explicit transitions. To support safe interruption and cleanup, the paper extends behavior trees with transient and non-transient tasks, internal statuses `Idle`, `Activating`, and `Running`, and entry/exit hooks so that a currently running task can be deactivated before a higher-priority or fallback task is activated. Under this semantics, transient tasks immediately return `Success` or `Failure` and remain idle, whereas non-transient tasks first return `Activating`, are formally activated by the superior task, and later request deactivation by returning `Success` or `Failure`, which avoids chattering when preconditions are checked ahead of a running action. The demonstration mission plan first checks whether the aircraft is already above the required altitude and otherwise performs takeoff, and then loops over waypoint following by checking whether the current waypoint is reached, flying to it, advancing to the next waypoint, and resetting to the first waypoint when the last waypoint has been completed.

### 3. 逐句溯源

1. 句子 1：The UAV mission management module organizes control behavior as a hierarchy of tasks whose root task is ticked every cycle, propagating execution through composite nodes to leaf actions that can engage autopilot modes, switch payloads, or trigger mission actions such as taking photographs.
   对应摘录：A
2. 句子 2：Each task returns `Success`, `Failure`, or `Running`, while sequences require all subtasks to succeed in order and selectors choose among prioritized alternatives, so the tree encodes mission logic as a hierarchy of operational modes rather than as flat explicit transitions.
   对应摘录：A
3. 句子 3：To support safe interruption and cleanup, the paper extends behavior trees with transient and non-transient tasks, internal statuses `Idle`, `Activating`, and `Running`, and entry/exit hooks so that a currently running task can be deactivated before a higher-priority or fallback task is activated.
   对应摘录：B
4. 句子 4：Under this semantics, transient tasks immediately return `Success` or `Failure` and remain idle, whereas non-transient tasks first return `Activating`, are formally activated by the superior task, and later request deactivation by returning `Success` or `Failure`, which avoids chattering when preconditions are checked ahead of a running action.
   对应摘录：B
5. 句子 5：The demonstration mission plan first checks whether the aircraft is already above the required altitude and otherwise performs takeoff, and then loops over waypoint following by checking whether the current waypoint is reached, flying to it, advancing to the next waypoint, and resetting to the first waypoint when the last waypoint has been completed.
   对应摘录：B
