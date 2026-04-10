# An Architecture for Onboard Flight Control of a Sub-Gram Piezo-Actuated Aerial Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把超轻压电扑翼飞行器的 ramp-up、liftoff、full control、landing 和 ramp-down 顺序写成了带明确电压与持续时间的 8 态机载 FSM。

## 条目 1: Eight-state onboard flight-phase FSM

- 控制对象：航空航天与飞行控制领域的超轻压电扑翼飞行器机载飞行阶段控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 sub-gram piezo-actuated aerial vehicle 的 onboard flight supervisor，用固定的 ramp-up、liftoff、control-on、landing 和 ramp-down 序列保护高压致动器并切换到底层姿态控制任务。
- 判断：算。对象是实际机载飞行控制链，正文直接给出了状态集合、进入信号、每个状态的电压/时长和通知给底层 controller 的 mode，而不是只谈硬件架构。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Abstract`
> A finite state machine (FSM) combined with a cascaded PID control architecture was developed for stabilization and maneuvering, utilizing real-time feedback from external motion capture systems operating at 240 Hz.

#### 摘录 B

- 出处：第 27 页，`3.1.2 Finite State Machine (FSM) Task`
> The Finite-State Machine (FSM) task is responsible for managing system behavior and ensuring the safe operation of piezo actuators through methodical state transitions. ... The FSM and flyController transition through several defined states and modes.

#### 摘录 C

- 出处：第 28 页，`FSM States and Transitions`
> Idle State ... No actuator commands are issued until a start signal is received.
>
> Offset Ramp ... linearly increasing to the baseline offset voltage of 130 V.
>
> Amplitude Ramp ... ramps the amplitude from 0 to the nominal value of 140 V.
>
> Liftoff ... activates the altitude and attitude control loops ... This phase lasts approximately 100 ms.
>
> Control On ... enables the lateral controller and sets the desired setpoint.
>
> Landing ... safely decreasing actuation levels ... After 500 ms, the FSM advances to amplitude ramp-down.

#### 摘录 D

- 出处：第 29 页，`Table 3.1 / Table 3.2`
> OFFSET_RAMP Offset to 130V
> AMP_RAMP Amp to 140V
> LIFTOFF ... LIFTOFF
> CONTROL_ON ... CONTROL_ON
> LAND ... LAND
> AMP_RAMP_D Amp to 0V RESET
> OFFSET_RAMP_D Offset to 0V, Turn off Bias
>
> Controller Mode Action
> IDLE Estimate the initial position
> LIFTOFF Altitude and Attitude control switched on
> CONTROL_ON Lateral control also switched on
> LAND Ramp ΔAmp and ΔOffset to 0v

### 2. 基于原文整理后的自然语言描述

The onboard flight supervisor is a fixed-sequence eight-state FSM that moves through `Idle`, `Offset Ramp`, `Amplitude Ramp`, `Liftoff`, `Control On`, `Landing`, `Amplitude Ramp-Down`, and `Offset Ramp-Down`. Its early states are dedicated to actuator-safe startup: the offset is ramped from `0` to `130 V`, then the amplitude is ramped from `0` to `140 V`, and only after these electrical preconditions are met does the controller hand over to active flight modes. In `Liftoff`, the lower-level controller turns on altitude and attitude loops for about `100 ms`, after which `Control On` enables lateral control and normal setpoint tracking. When an end signal is received, the FSM enters `Landing`, commands an autonomous ramp-down for about `500 ms`, then executes amplitude-to-zero and offset-to-zero shutdown steps before returning to `Idle`. Because both the state order and the embedded durations are explicit in the paper, this is a high-quality `FSM + T1` flight-phase control case rather than a loose mission narrative.

### 3. 逐句溯源

1. 句子 1：The onboard flight supervisor is a fixed-sequence eight-state FSM that moves through `Idle`, `Offset Ramp`, `Amplitude Ramp`, `Liftoff`, `Control On`, `Landing`, `Amplitude Ramp-Down`, and `Offset Ramp-Down`.
   对应摘录：B, C, D
2. 句子 2：Its early states are dedicated to actuator-safe startup: the offset is ramped from `0` to `130 V`, then the amplitude is ramped from `0` to `140 V`, and only after these electrical preconditions are met does the controller hand over to active flight modes.
   对应摘录：C, D
3. 句子 3：In `Liftoff`, the lower-level controller turns on altitude and attitude loops for about `100 ms`, after which `Control On` enables lateral control and normal setpoint tracking.
   对应摘录：A, C, D
4. 句子 4：When an end signal is received, the FSM enters `Landing`, commands an autonomous ramp-down for about `500 ms`, then executes amplitude-to-zero and offset-to-zero shutdown steps before returning to `Idle`.
   对应摘录：C, D
5. 句子 5：Because both the state order and the embedded durations are explicit in the paper, this is a high-quality `FSM + T1` flight-phase control case rather than a loose mission narrative.
   对应摘录：A, B, C, D
