# A Hierarchical Control System for Autonomous Driving towards Urban Challenges - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市道路自动驾驶决策层清楚拆成 `Mission FSM + Control FSM` 两级结构，并给出了模式集合、转移条件和优先级。

## 条目 1: Two-Stage Mission-and-Control FSM for Urban Driving
- 控制对象：城市道路自动驾驶车辆的高层决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶车辆的高层决策机，用于在 `Ready / SAG / Change-Lane / E-stop / avoid obstacle` 等任务状态之间切换，并在每个任务态内部驱动对应的控制子状态。
- 判断：算。对象是实际自动驾驶车辆的决策层控制器，原文明确说明两级 FSM 结构、各顶层状态及嵌套子状态、转移条件和优先级。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 19-32
> This paper focuses on how to efficiently solve the hierarchical control system of a self-driving car into practice ... we propose the decision making for motion planning by applying a two-stage Finite State Machine to manipulate mission planning and control states ... the proposed framework can operate efficiently in the urban scenario.

#### 摘录 B
- 出处：第 4-5 页，Section 2.1 `The Decision-Making Mechanism Based on Two-Stage FSM` / Table 1 / Figure 2，行 177-235
> The Decision-Making Mechanism (DMM) ... employs FSM to handle the mission planning and behavior on-road driving. The first DMM called the Mission FSM (M-FSM) ... The second DMM named the Control FSM (C-FSM) mimics the vehicle’s status on the road.
>
> M-FSM is categorized into five classes: Ready, Stop-and-Go (SAG), Change-Lane (CL), E-stop, avoid obstacle mode. In particular, the M-FSM consists of a C-FSM that manages the control states of the vehicle.
>
> The CL mode consists of two control states lane-keeping and lane-changing ... The obstacle avoiding mode activates when the obstacles have been detected lying on the path.
>
> Condition `10, 20, 30, 40`: emergency circumstances; `23`: demanding to change the path; `41`: un-complete obstacle avoiding mission, and the time for the mission is over; `32, 42`: completely performs the lane-changing and obstacle-avoidance mission.

#### 摘录 C
- 出处：第 5 页，Figure 2 及其说明，行 210-235
> Each state in FSM requires a resource that is updated over time in the ROS nodes of perception. The use of priority and flag of each state is to prevent access to the same resources. The priority level of the E-stop mode is highest, following by the obstacle avoiding mode, the CL mode, and the SAG mode.
>
> Figure 2. Decision mechanism based on Mission-Finite State Machines (M-FSM) while the inside of M-FSM describes Control FSM (C-FSM).

### 2. 基于原文整理后的自然语言描述

The urban-driving decision mechanism is organized as a two-stage hierarchy in which a top-level `Mission FSM` selects the current driving mission and an inner `Control FSM` represents the vehicle’s immediate on-road control state. The top layer contains five mission classes: `Ready`, `Stop-and-Go`, `Change-Lane`, `E-stop`, and `avoid obstacle`, and the `Change-Lane` mission further contains the control states `lane-keeping` and `lane-changing`. Transition guards are explicitly enumerated: emergency perception triggers conditions `10/20/30/40`, condition `23` requests a path change, condition `41` means the obstacle-avoidance mission timed out before completion, and conditions `32/42` denote successful completion of the lane-change or obstacle-avoidance mission. The controller uses per-state flags and priorities to serialize access to shared resources, with `E-stop` at the highest priority, followed by obstacle avoidance, lane changing, and stop-and-go. This gives the vehicle a hierarchical mission-to-control state machine that can switch missions while preserving a more local driving substate.

### 3. 逐句溯源

1. 句子 1：The urban-driving decision mechanism is organized as a two-stage hierarchy in which a top-level `Mission FSM` selects the current driving mission and an inner `Control FSM` represents the vehicle’s immediate on-road control state.
   对应摘录：A, B, C
2. 句子 2：The top layer contains five mission classes: `Ready`, `Stop-and-Go`, `Change-Lane`, `E-stop`, and `avoid obstacle`, and the `Change-Lane` mission further contains the control states `lane-keeping` and `lane-changing`.
   对应摘录：B
3. 句子 3：Transition guards are explicitly enumerated: emergency perception triggers conditions `10/20/30/40`, condition `23` requests a path change, condition `41` means the obstacle-avoidance mission timed out before completion, and conditions `32/42` denote successful completion of the lane-change or obstacle-avoidance mission.
   对应摘录：B
4. 句子 4：The controller uses per-state flags and priorities to serialize access to shared resources, with `E-stop` at the highest priority, followed by obstacle avoidance, lane changing, and stop-and-go.
   对应摘录：C
5. 句子 5：This gives the vehicle a hierarchical mission-to-control state machine that can switch missions while preserving a more local driving substate.
   对应摘录：A, B, C
