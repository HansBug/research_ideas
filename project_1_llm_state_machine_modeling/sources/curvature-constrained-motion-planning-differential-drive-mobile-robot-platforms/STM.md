# Curvature-Constrained Motion Planning Method for Differential-Drive Mobile Robot Platforms - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（任务级显式时序）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把差速移动机器人的航点跟踪控制明确写成 `Align / Goto / Pause` 三态事件驱动 FSM，并给出以 `εθ / εd / tpause / κmax` 为核心的转移与动作规则，能够稳定支撑双 A。

## 条目 1: Align-Goto-Pause curvature-constrained waypoint follower
- 控制对象：通用控制与机器人任务领域的差速移动机器人曲率约束航点跟踪控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（任务级显式时序）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向差速移动机器人的航点跟踪执行器，用 `Align / Goto / Pause` 三态控制航向校正、前向推进和任务停顿，并通过曲率上界保证机器人不做原地急转。
- 判断：算。对象是真实机器人执行控制器而不是纯路径规划数学稿；原文直接给出 finite-state machine、状态动作、状态转移阈值和算法伪代码。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页摘要
> The controller integrates an explicit curvature limit into a finite-state machine, ensuring smooth heading transitions without in-place rotation. The overall architecture integrates GNSS-RTK and IMU localization, modular ROS 2 nodes for trajectory execution, and a supervisory interface developed in Foxglove Studio for intuitive mission planning.

#### 摘录 B
- 出处：第 7 页，Section `2.5 Curvature-Constrained Control Framework`
> The control strategy is implemented as an event-driven finite-state machine composed of three operational states: Align, Goto, and Pause. In the Align state, the robot gradually adjusts its heading toward the next waypoint while moving at a reduced speed ... Once the heading error falls below a predefined tolerance, the system transitions to the Goto state ... When a waypoint with zero assigned speed is reached, the controller switches to the Pause state, halts the robot, executes any pending service commands, and resumes motion after a parameterized delay.

#### 摘录 C
- 出处：第 8 页，Algorithm `1` 与 Table `1`
> The state machine transitions are triggered by distance and heading thresholds, ensuring deterministic progress along the waypoint sequence.
>
> if state = ALIGN then ... if |∆θ| < εθ then state ← GOTO ...
>
> else if state = GOTO then ... if d < εd then if vw = 0 then state ← PAUSE ...
>
> else if state = PAUSE then stop motors; execute task service; wait tpause ; state ← ALIGN;

### 2. 基于原文整理后的自然语言描述

The waypoint-following controller for the differential-drive robot is implemented as a three-state event-driven finite-state machine with states `Align`, `Goto`, and `Pause`. In `Align`, the robot turns toward the next waypoint by following a curvature-bounded forward arc at reduced speed rather than rotating in place. Once the wrapped heading error falls below the heading threshold `εθ`, the controller transitions to `Goto`, where the robot advances toward the waypoint while continuously clipping curvature by `κmax` so that the commanded angular velocity remains kinematically feasible. When the robot enters the waypoint-radius threshold `εd`, the controller either advances to the next waypoint or, if the waypoint carries zero assigned speed, enters `Pause`. In `Pause`, the robot stops the motors, executes any pending service command, waits for `tpause`, and then re-enters `Align` to continue the mission.

### 3. 逐句溯源

1. 句子 1：The waypoint-following controller for the differential-drive robot is implemented as a three-state event-driven finite-state machine with states `Align`, `Goto`, and `Pause`.
   对应摘录：B
2. 句子 2：In `Align`, the robot turns toward the next waypoint by following a curvature-bounded forward arc at reduced speed rather than rotating in place.
   对应摘录：A, B
3. 句子 3：Once the wrapped heading error falls below the heading threshold `εθ`, the controller transitions to `Goto`, where the robot advances toward the waypoint while continuously clipping curvature by `κmax` so that the commanded angular velocity remains kinematically feasible.
   对应摘录：B, C
4. 句子 4：When the robot enters the waypoint-radius threshold `εd`, the controller either advances to the next waypoint or, if the waypoint carries zero assigned speed, enters `Pause`.
   对应摘录：B, C
5. 句子 5：In `Pause`, the robot stops the motors, executes any pending service command, waits for `tpause`, and then re-enters `Align` to continue the mission.
   对应摘录：C
