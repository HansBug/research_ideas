# Reusable and Reliable Flight-Control Software for a Fail-Safe and Cost-Efficient Cubesat Mission: Design and Implementation - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文提供了 Masat-1 的 operational modes、触发条件和 safe mode 策略，证据较分散但可整理为 CubeSat 控制逻辑样本。

## 条目 1: Closed-mode CONOPS and safe-mode fallback in Masat-1
- 控制对象：Masat-1 CubeSat 飞控软件中的任务/故障管理逻辑

### 0. 条目识别与判定

- 一句话说明：这是航天器飞控软件领域的 CubeSat operational-mode controller，用于在 INIT、SAFE、CRITICAL、IDLE、ECLIPSE 和 SUN-VIS 等模式之间切换，并在异常时把卫星带入 safe mode。
- 判断：算，但属于航天器任务管理/故障管理级样本。对象是实际卫星飞控软件，原文给出了 closed-mode CONOPS、状态触发条件和 safe mode 行为。

### 1. 原文摘录

#### 摘录 A
- 出处：第 18-19 页，Concept of Operations (CONOPS)，行 1060-1098
> The first step to define a spacecraft concept of operations is the freezing of the mission operational modes ...
>
> We decided to adopt a closed mode of concepts to ensure the deterministic behavior of the spacecraft. Therefore, Masat-1 operating modes are ruled by a finite state machine. During each state, we plan procedures to be executed given occurring events, such as the low battery level, sun eclipse, ground visibility or errors.
>
> Switching between the Masat-1 operational mode is ruled by four factors: (i) ground telecommand received; (ii) automatic onboard transition when a task or satellite initialization is completed; (iii) the battery charge is under the nominal level; or (iv) an automatic FDIR reconfiguration order upon some anomalies detected.

#### 摘录 B
- 出处：第 19-20 页，对 INIT/SAFE/CRITICAL/IDLE/SUN-VIS modes 的说明，行 1114-1160
> Thereafter, the Masat-1 shall enter safe mode during which the satellite is totally commandable.
>
> Safe mode is entered after INIT mode, upon ground command or after a system fault/failure event.
>
> Critical mode is entered when the battery charge level is under 86%.
>
> IDLE mode is a temporary mode that the Masat-1 switches to, after exiting safe mode or when the payload and communication operations are over. Depending on the sun visibility status, the satellite will switch to Sun-Vis or eclipse mode.
>
> Sun-Vis mode is designed to execute the mission’s secondary objectives

#### 摘录 C
- 出处：第 25-27 页，对 safety monitor 与 safe mode 的说明，行 1417-1425、1511-1515
> Upon the detection of anomalies, events are raised and are handled through a decision matrix ... the safety monitor sends signals to the flight planner to switch to safe mode.
>
> This mode was implemented to maintain the spacecraft in a safe-guarding configuration when major anomalies occur, and it will remain in this state until next contact with the ground segment.
>
> the control logic of the spacecraft is based on a finite state machine implemented at the application layer. When coupled with a closed mode CONOPS, this will ensure the deterministic behavior of the spacecraft.

### 2. 基于原文整理后的自然语言描述

Masat-1 adopts a closed-mode concept of operations in which the spacecraft operating modes are ruled by a finite state machine and state changes are triggered by ground telecommands, task completion, low battery level, and automatic FDIR reconfiguration events. After initialization, the spacecraft enters safe mode, and from there it may move through Critical, IDLE, Eclipse, and Sun-Vis modes depending on battery level, sun visibility, and mission activity. When anomalies are detected, the safety monitor raises events and signals the flight planner to switch the spacecraft into safe mode, where it remains in a safeguarding configuration until the next ground contact.

### 3. 逐句溯源

1. 句子 1：Masat-1 adopts a closed-mode concept of operations in which the spacecraft operating modes are ruled by a finite state machine and state changes are triggered by ground telecommands, task completion, low battery level, and automatic FDIR reconfiguration events.
   对应摘录：A
2. 句子 2：After initialization, the spacecraft enters safe mode, and from there it may move through Critical, IDLE, Eclipse, and Sun-Vis modes depending on battery level, sun visibility, and mission activity.
   对应摘录：B
3. 句子 3：When anomalies are detected, the safety monitor raises events and signals the flight planner to switch the spacecraft into safe mode, where it remains in a safeguarding configuration until the next ground contact.
   对应摘录：C
