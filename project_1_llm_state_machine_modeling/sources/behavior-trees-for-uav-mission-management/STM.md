# Behavior Trees for UAV Mission Management - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以行为树为主，但 mission management 模块的任务状态、激活/退出和中断逻辑写得比较明确，可整理为 UAV 控制构件级样本。

## 条目 1: Task activation and interruption logic for UAV mission management
- 控制对象：无人机任务管理模块

### 0. 条目识别与判定

- 一句话说明：这是无人机任务管理领域的 UAV mission management module，用于通过任务树驱动 autopilot mode、payload actions 和任务中断/切换。
- 判断：算，但属于控制软件构件级样本。对象是实际 UAV control loop 上方的 mission management module，原文明确给出了任务执行接口、状态返回值以及中断时的激活/退出逻辑。

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
- 出处：第 6-7 页，Transient Behaviors，对中断与内部状态的说明，行 220-279
> Providing tasks with entry and exit hooks by using transient behaviors. This extension narrows the gap between current BT features and state machine features expected by the user.
>
> Suppose a remote sensing mission has to be aborted due to a system failure. One would wish to deactivate the power-consuming cameras during execution of the fallback behavior.
>
> A task must thus be provided with an internal status, which can at least be Idle or Running. If a currently Idle sub-task needs to be executed by its superior node, the currently Running sub-task needs to be deactivated first and the sub-task to be ticked needs to be activated.
>
> Each task starts out with an Idle status ... A transient task immediately returns either Success or Failure ... A non-transient task, however, will enter the new status Activating ... The actual activation is performed through the superior composite task.

### 2. 基于原文整理后的自然语言描述

The UAV mission management module organizes control behavior as a hierarchy of operational modes in which tasks can engage autopilot modes, switch payloads, and execute other mission actions. The mission plan is executed by ticking the root task, and each task reports whether it has succeeded, failed, or is still running. To support safe interruption and fallback behavior, tasks carry internal execution status such as Idle, Running, and Activating, so that a currently running task can be deactivated before another task is activated when the mission manager needs to abort or redirect the mission.

### 3. 逐句溯源

1. 句子 1：The UAV mission management module organizes control behavior as a hierarchy of operational modes in which tasks can engage autopilot modes, switch payloads, and execute other mission actions.
   对应摘录：A
2. 句子 2：The mission plan is executed by ticking the root task, and each task reports whether it has succeeded, failed, or is still running.
   对应摘录：A
3. 句子 3：To support safe interruption and fallback behavior, tasks carry internal execution status such as Idle, Running, and Activating, so that a currently running task can be deactivated before another task is activated when the mission manager needs to abort or redirect the mission.
   对应摘录：B
