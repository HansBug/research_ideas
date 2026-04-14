# CyberLimb: a novel robotic prosthesis concept with shared and intuitive control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `CyberLimb` 的上肢 prosthesis 任务逻辑明确写成同时调度 gripper 与 wrist 的 `FSM`，并给出 headband 阈值、自动 leveling 模式和 task-specific 自动序列，可直接作为高质量 `HSM + T0` 样本。

## 条目 1: Parallel wrist-gripper shared-control supervisor for the CyberLimb prosthesis
- 控制对象：`CyberLimb` 经桡假肢的 wrist-gripper shared-control task supervisor
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向经桡假肢的 shared-control 任务监督器，用 finite-state task logic 并行调度 wrist 与 gripper，再通过 headband、手机 UI 和 task-specific functions 驱动具体动作。
- 判断：算。对象是真实假肢控制系统，不是比赛流程本身；原文明确给出 FSM、输入变量、模式切换、自动 leveling 行为和自动任务序列。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract / Methods，行 16-21
> Our design consists of a soft robotic-based two finger gripper controlled by a force-sensing resistor (FSR) headband interface, automatic arm angle dependent wrist flexion and extension, and manual forearm supination and pronation for a shared control system.
>
> The gripper is incorporated with FSR sensors to relay haptic information to the pilot based on the output of a neural network model that estimates geometries and objects material.

#### 摘录 B
- 出处：第 10 页，Section `Software and control architecture`，行 518-532
> High-level task control translates user inputs into commanded joint angles based on the state of the prosthesis. The core unit of task control is a finite state machine handling the desired angles of the gripper and the wrist in parallel.
>
> The desired angles are calculated based on current joint angles `θ∈R²`, shaft orientation `qIMU∈C⁴` and the control mode ...
>
> A trajectory smoothing and safety unit avoids signal jumps and ensures a maximal rate of change in the output signal.

#### 摘录 C
- 出处：第 10 页，Section `Software and control architecture`，行 533-554
> The primary commands that control the finite state machine are sent from the smartphone app—the central user interface.
>
> Initial thresholds for the gripper and wrist are set ... Additionally, the FSR headband threshold is set either automatically or manually ...
>
> To choose the FSR headband mode ... the button “Temple OFF” needs to be pressed. In this mode, the grasping and opening of the gripper is toggled by exceeding the calibrated threshold for the force measured by the FSR sensor.

#### 摘录 D
- 出处：第 11 页，Section `Software and control architecture`，行 564-582
> The wrist may be passively controlled by the pilot through an automatic control scheme or adjusted to be rigid.
>
> In “Horizontal Leveling” mode, the wrist will automatically adjust to keep the wrist horizontally leveled at all times to support object manipulation. In “Max Leveling” mode, the wrist is in maximum extension and rotates to maximum flexion if the prosthesis roll angle defined through `qIMU` exceeds `±90°`.
>
> Additional task-specific functions such as “Scissors” or “Haptic Task” trigger a sequence of automatic wrist and gripper movements to solve the corresponding task.

### 2. 基于原文整理后的自然语言描述

CyberLimb uses a hierarchical shared-control supervisor whose high-level finite-state task logic computes wrist and gripper commands in parallel instead of treating the prosthesis as a single serial actuator. The system combines a two-finger soft robotic gripper, an FSR headband interface, automatic arm-angle-dependent wrist flexion and extension, manual forearm pronation and supination, and gripper FSRs used for haptic inference. At the control level, the FSM derives desired wrist and gripper angles from current joint angles, IMU shaft orientation, and the active control mode, while a smoothing and safety block limits abrupt command changes. The smartphone UI first calibrates the gripper, wrist, and headband thresholds, then selects the operational mode: in `Temple OFF` headband mode jaw-triggered FSR events toggle grasping, and the same UI can activate task-specific functions. Automatic wrist behaviors are explicit control modes rather than informal heuristics: `Horizontal Leveling` keeps the wrist level, `Max Leveling` flips between extreme wrist positions when roll exceeds `±90°`, and `Scissors` or `Haptic Task` launch predefined wrist-gripper action sequences.

### 3. 逐句溯源

1. 句子 1：CyberLimb uses a hierarchical shared-control supervisor whose high-level finite-state task logic computes wrist and gripper commands in parallel instead of treating the prosthesis as a single serial actuator.
   对应摘录：B
2. 句子 2：The system combines a two-finger soft robotic gripper, an FSR headband interface, automatic arm-angle-dependent wrist flexion and extension, manual forearm pronation and supination, and gripper FSRs used for haptic inference.
   对应摘录：A
3. 句子 3：At the control level, the FSM derives desired wrist and gripper angles from current joint angles, IMU shaft orientation, and the active control mode, while a smoothing and safety block limits abrupt command changes.
   对应摘录：B
4. 句子 4：The smartphone UI first calibrates the gripper, wrist, and headband thresholds, then selects the operational mode: in `Temple OFF` headband mode jaw-triggered FSR events toggle grasping, and the same UI can activate task-specific functions.
   对应摘录：C, D
5. 句子 5：Automatic wrist behaviors are explicit control modes rather than informal heuristics: `Horizontal Leveling` keeps the wrist level, `Max Leveling` flips between extreme wrist positions when roll exceeds `±90°`, and `Scissors` or `Haptic Task` launch predefined wrist-gripper action sequences.
   对应摘录：D
