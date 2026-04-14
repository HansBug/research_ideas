# Sensor-Guided Assembly of Segmented Structures with Industrial Robots - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把分段复合板装配流程明确组织成三步循环状态机，并补足了人工接管、异常中断、暂停回放、重规划恢复和前后步回跳逻辑，可直接作为制造装配方向的 `FSM + T0` 双 A 样本。

## 条目 1: Pause-resume segmented-panel assembly process controller

- 控制对象：工业自动化与离散制造领域的分段复合板装配流程监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向大型分段复合板装配的工业机器人流程监督器，以 `panel pick-up -> transport -> placement` 三主态为核心，并围绕用户步进、自动运行、异常中断、人工接管和恢复重规划组织整条装配流程。
- 判断：算。对象是实际工业机器人装配流程控制器，不是单纯 ROS 架构说明；原文明确写出三大装配步骤、状态机负责的 step transition、用户接口交互、异常中断后的回到已知状态、暂停/回放/恢复和人工跳转到前后步骤的语义。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 47-60 行
> This paper presents a robotic assembly methodology for the manufacturing of large segmented composite structures. The approach addresses three key steps in the assembly process: panel localization and pick-up, panel transport, and panel placement. ... A finite state machine governs the process flow and user interface. It allows process interruption and return to the previous known state in case of error condition or when secondary operations are needed.

#### 摘录 B

- 出处：第 4 页，`3. Problem Statement and Solution Approach`，`paper_content.txt` 第 181-200 行
> Our example demonstration process consists of three main steps ... 1. Panel Localization and Pick-up ... 2. Panel Transport ... 3. Panel Placement ... The process repeats indefinitely as long as there are panels available for pick-up and there is space in the assembly nest. The user can step through the stages or run the process autonomously. The process can be interrupted by the user or under exception conditions ... The user can manually operate the system and then continue the automatic operation by moving to the subsequent or previous steps.
>
> Our solution implementation involves these steps: 1. Construct a state machine describing the transition between the steps in the assembly process and the interaction with the operator and the occurrence of exception condition.

#### 摘录 C

- 出处：第 7 页，`4. Software Architecture`，`paper_content.txt` 第 329-339 行
> The state machine for the overall assembly process is shown in Figure 4. The state transition is executed in either safe teleoperation or autonomous mode with vision and force guidance. We design the user interface to allow the user to interact with the state machine. The user can step through the operations, run the process autonomously in a supervisory mode, or interrupt and take over in the safe teleoperation mode. ... The progression between states may be paused at any point if intervention is needed. The step can then be played back or resumed by replanning the trajectory without restarting the whole process.

#### 摘录 D

- 出处：第 8 页，Figure 4 caption，`paper_content.txt` 第 353-355 行
> The state transition diagram of the assembly process allow continuous operation to assemble incoming panels to the existing panels. It also allows operator to pause for manual operations and resume after completion. The operator can also manually transition the system to a different state.

### 2. 基于原文整理后的自然语言描述

The retained controller is an industrial-robot assembly process supervisor whose core loop consists of three explicit process states: `Panel Localization and Pick-up`, `Panel Transport`, and `Panel Placement`. These states are not only a narrative sequence: the paper states that a finite state machine is constructed specifically to govern transitions between them, to manage operator interaction, and to handle exception conditions while the loop repeats for incoming panels. The supervisory logic also distinguishes operation modes, because the same state transitions may execute in autonomous vision-and-force-guided mode or in safe teleoperation mode when the operator interrupts and takes over. Interruption handling is part of the control semantics rather than a UI afterthought: the user may pause progression at any point, perform secondary manual operations, play back or resume the interrupted step by replanning the trajectory, or manually move the process to a subsequent or previous state. The resulting process controller is therefore a concrete manufacturing FSM that binds process stage, operator authority, and recovery behavior into a single pause-resume assembly workflow.

### 3. 逐句溯源

1. 句子 1：The retained controller is an industrial-robot assembly process supervisor whose core loop consists of three explicit process states: `Panel Localization and Pick-up`, `Panel Transport`, and `Panel Placement`.
   对应摘录：A, B
2. 句子 2：These states are not only a narrative sequence: the paper states that a finite state machine is constructed specifically to govern transitions between them, to manage operator interaction, and to handle exception conditions while the loop repeats for incoming panels.
   对应摘录：A, B
3. 句子 3：The supervisory logic also distinguishes operation modes, because the same state transitions may execute in autonomous vision-and-force-guided mode or in safe teleoperation mode when the operator interrupts and takes over.
   对应摘录：C
4. 句子 4：Interruption handling is part of the control semantics rather than a UI afterthought: the user may pause progression at any point, perform secondary manual operations, play back or resume the interrupted step by replanning the trajectory, or manually move the process to a subsequent or previous state.
   对应摘录：A, B, C, D
5. 句子 5：The resulting process controller is therefore a concrete manufacturing FSM that binds process stage, operator authority, and recovery behavior into a single pause-resume assembly workflow.
   对应摘录：A, B, C, D
