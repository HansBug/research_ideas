# Design and Formal Verification of a Safe Stop Supervisor for an Automated Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 parking-to-parking 任务 supervisor 的层次架构、路径切换、SSTP/AEB 故障回退和 Stateflow FSM 都写得很清楚，是自动驾驶高层异常恢复链里的强样本。

## 条目 1: Parking-to-Parking Safe-Stop Mission Supervisor

- 控制对象：自动驾驶车辆 parking-to-parking 任务中的高层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个自动驾驶任务 supervisor，用来协调 `SPP / UPP / TP / SSTP / AEB`，保证车辆在停车场 A 到停车场 B 的运输任务中只在故障时触发 safe stop 或 emergency stop。
- 判断：算。对象是车辆高层监督控制器本身，不是单纯验证流程；原文明确给出了层次架构、标称任务链、故障回退逻辑、LTL 需求和 Stateflow/Promela 状态机实现。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract，`paper_content.txt` 第 22-40 行
> This paper describes the design and formal verification of a supervisor to manage all requirements for mode switching between nominal planners, and additional requirements for switching to a safe stop trajectory planner that acts as the fallback routine. ... Simulations and experiments show that the vehicle is able to autonomously drive in a safe manner between two parking lots and can successfully come to a safe stop upon GPS sensor failure.

#### 摘录 B

- 出处：第 3-4 页，Section II `System Architecture`，`paper_content.txt` 第 147-155, 197-255 行
> The system is built in a hierarchical way, where the Supervisor is the top-most and central software node.
>
> The Trajectory Planner (TP) receives a path from the Supervisor ... The purpose of the Safe Stop Trajectory Planner (SSTP) function is to provide a collision free trajectory ... The Controller receives reference trajectories simultaneously from both the Trajectory Planner and the Safe Stop Trajectory Planner. ... The Controller may also be commanded by the Supervisor to stop as quickly as possible. This mode will be referred to as Automatic Emergency Brake (AEB).

#### 摘录 C

- 出处：第 4 页，Section III `Supervisor Design`，`paper_content.txt` 第 257-300 行
> During a nominal parking-to-parking mission ... The Supervisor first acquires the current position and the goal position from the Localization component. ... The Supervisor requests the UPP to create a path from the current position to Tp1. ... When the RCV moves close to Tp2, the UPP is requested by the Supervisor to create a path between Tp2 and the goal position. ... If a failure occurs and the nominal operational conditions are disrupted, then the Supervisor activates the SSTP to reach a minimal risk condition. If the SSTP fails, the Supervisor activates the AEB.

#### 摘录 D

- 出处：第 4-6 页，Section III-A/B `Formal requirements / Modeling in Stateflow`，`paper_content.txt` 第 306-327, 402-419 行
> missionComplete: The supervisor and the four concurrent control functions shall never stop at invalid end states. ... 5) safeStop: If the vehicle stops safely along the road, then an error must have occurred and the SSTP must have executed successfully. 6) unsafeStop: If the vehicle stops with emergency braking, then an error must have occurred and the SSTP must have failed.
>
> To solve the transport mission, an FSM which governs the operation of the Supervisor component is proposed in Figure 3. ... Stateflow ... is used for this purpose. A state consists of a name, an entry section, and an exit section. ... The Stateflow model is automatically translated to C++ code by MATLAB code generation tools.

#### 摘录 E

- 出处：第 7 页，Section IV-B `RCV Experiment`，`paper_content.txt` 第 516-523, 541-548 行
> The colors represent the active state of the FSM. ... nominal planner switching between UPP and SPP was handled seamlessly.
>
> WaitingForGoal / WaitForTransforms / CallForPlan / ParkingToRoad / SafeStop

### 2. 基于原文整理后的自然语言描述

The safe-stop supervisor is the top-most node in a hierarchical autonomous-driving architecture that coordinates localization, structured and unstructured path planning, trajectory planning, and the fallback stopping functions. For a nominal parking-to-parking mission, it acquires the current and goal positions, requests `SPP` for the structured road path and transition points, requests `UPP` for the parking-lot segments, and hands the concatenated paths to `TP` as the vehicle progresses from parking lot A to parking lot B. If nominal conditions are violated by GPS, `SPP`, or `UPP` failures, the supervisor commands `SSTP` to generate a minimal-risk stop; if `SSTP` fails, it escalates to `AEB`. The requirements explicitly constrain this recovery chain: safe roadside stopping must correspond to an error plus successful `SSTP`, while emergency stop must correspond to an error plus failed `SSTP`. The proposed supervisor is implemented as a Stateflow FSM and then translated to C++ for ROS integration. In the demonstrated scenario, the active supervisor states include `WaitingForGoal`, `WaitForTransforms`, `CallForPlan`, `ParkingToRoad`, and `SafeStop`, which shows a concrete task-level state chain rather than a purely abstract requirement set.

### 3. 逐句溯源

1. 句子 1：The safe-stop supervisor is the top-most node in a hierarchical autonomous-driving architecture that coordinates localization, structured and unstructured path planning, trajectory planning, and the fallback stopping functions.
   对应摘录：A, B
2. 句子 2：For a nominal parking-to-parking mission, it acquires the current and goal positions, requests `SPP` for the structured road path and transition points, requests `UPP` for the parking-lot segments, and hands the concatenated paths to `TP` as the vehicle progresses from parking lot A to parking lot B.
   对应摘录：A, C
3. 句子 3：If nominal conditions are violated by GPS, `SPP`, or `UPP` failures, the supervisor commands `SSTP` to generate a minimal-risk stop; if `SSTP` fails, it escalates to `AEB`.
   对应摘录：B, C
4. 句子 4：The requirements explicitly constrain this recovery chain: safe roadside stopping must correspond to an error plus successful `SSTP`, while emergency stop must correspond to an error plus failed `SSTP`.
   对应摘录：D
5. 句子 5：The proposed supervisor is implemented as a Stateflow FSM and then translated to C++ for ROS integration.
   对应摘录：D
6. 句子 6：In the demonstrated scenario, the active supervisor states include `WaitingForGoal`, `WaitForTransforms`, `CallForPlan`, `ParkingToRoad`, and `SafeStop`, which shows a concrete task-level state chain rather than a purely abstract requirement set.
   对应摘录：E
