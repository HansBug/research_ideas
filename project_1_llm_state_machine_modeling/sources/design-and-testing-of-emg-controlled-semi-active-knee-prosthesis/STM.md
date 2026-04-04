# Design and Testing of an Emg-Controlled Semi-Active Knee Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 semi-active transfemoral knee prosthesis 的 five-state gait FSM、`450 a.u.` `EMG` threshold、`10 ms` smoothing、`0.9-1.0 s` swing reference、`185 ms` relock latency 与 conservative-stance fail-safe，可直接作为 `EFSM + T1` 双 A 样本。

## 条目 1: EMG-triggered gait-phase supervisor for the semi-active knee prosthesis
- 控制对象：semi-active transfemoral knee prosthesis 的 gait-phase supervisory controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 semi-active transfemoral knee prosthesis 的离散 gait-phase supervisor，它以 `EMG + IMU` 作为输入，用五态步态有限状态机决定何时维持被动承重、何时进入 swing 参考轨迹，并在故障时强制回 conservative stance。
- 判断：算。对象是真实膝假肢控制器，不是单纯机械结构或 bench 测试流程；原文明确给出了状态机骨架、输入阈值、swing 轨迹、时延指标和异常回退链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `2.2. Design and Materials`
> Given these premises, we propose a system in which a surface EMG sensor placed over the rectus femoris ... and an inertial unit ... provide dual-channel feedback. Analog-to-digital conversion (`1 kHz`, `10-bit`) and threshold detection (`450 a.u.`; `10 ms` moving-average window) are implemented on an STM32 Cortex-M microcontroller ... A five-state finite state machine performs gait phase identification.

#### 摘录 B
- 出处：第 6-7 页，Section `2.2. Design and Materials`
> The knee joint was designed to exhibit a quasi-energy-neutral stance locking behavior. In the stance phase, the joint geometry and internal damping are configured such that the limb can support body weight with the motor de-energized ... Active torque is therefore only required during transitions and swing motion ... During bench tests, the transition from an actively driven state to the quasi energy-neutral stance configuration required on the order of `185 ms` on average.

#### 摘录 C
- 出处：第 10 页，Section `2.3. Safety and Fail-Safe Mechanisms`
> Battery undervoltage was monitored ... when the supply voltage fell below a predefined threshold, the motor driver was disabled and the knee reverted to a passive, high-damping configuration ... A hardware watchdog timer was configured ... If the control loop failed to update within a specified interval, the watchdog reset the microcontroller ... In the event of a loss of EMG or IMU signal, the finite-state machine was forced into a conservative stance state, inhibiting transitions to swing until valid measurements were restored.

#### 摘录 D
- 出处：第 10-11 页，Section `2.4. Mathematical Modeling`
> To generate kinematic reference trajectories during the swing phase, a fifth-order polynomial approximation was used with zero initial and terminal velocity and acceleration conditions ... `t ∈ [0, T]`, where `T = 0.9–1 s` ... For the swing-phase trajectory, the desired knee angle `θ(t)` was defined by a fifth-order polynomial ... sufficient to enforce boundary conditions on angle, angular velocity and angular acceleration at the beginning and end of the swing phase.

#### 摘录 E
- 出处：第 19 页，Section `4. Experimental Validation and Discussion`
> Across `40` EMG-angle pairs, the mean EMG-to-motion latency was `185 ms` with a standard deviation of `24 ms` ... This value falls within the physiologically acceptable latency range (less than `200 ms`).

### 2. 基于原文整理后的自然语言描述

The semi-active transfemoral knee prosthesis is governed by a five-state gait supervisor that samples rectus-femoris EMG and IMU feedback on an STM32, smooths EMG with a `10 ms` moving-average window, and triggers intent when the calibrated signal exceeds `450 a.u.`. During load-bearing phases the machine keeps the knee in a quasi-energy-neutral stance configuration with the motor de-energized, and it only re-engages actuation for transitions and swing motion, with the driven-to-stance relock taking about `185 ms`. When the supervisor enters swing, it switches from passive support logic to a fifth-order knee reference trajectory with zero boundary velocity and acceleration and a commanded swing duration of `0.9-1.0 s`. The timing budget is explicit at the control level as well, because the design targets sub-`100 ms` EMG-to-PWM response and the measured EMG-to-motion latency remains below `200 ms`. Safety handling is embedded in the same supervisory logic: undervoltage forces a passive high-damping mode, control-loop timing violations trigger a watchdog reset with zero torque, and loss of EMG or IMU input forces a conservative stance state that blocks further transitions to swing.

### 3. 逐句溯源

1. 句子 1：The semi-active transfemoral knee prosthesis is governed by a five-state gait supervisor that samples rectus-femoris EMG and IMU feedback on an STM32, smooths EMG with a `10 ms` moving-average window, and triggers intent when the calibrated signal exceeds `450 a.u.`.
   对应摘录：A
2. 句子 2：During load-bearing phases the machine keeps the knee in a quasi-energy-neutral stance configuration with the motor de-energized, and it only re-engages actuation for transitions and swing motion, with the driven-to-stance relock taking about `185 ms`.
   对应摘录：B
3. 句子 3：When the supervisor enters swing, it switches from passive support logic to a fifth-order knee reference trajectory with zero boundary velocity and acceleration and a commanded swing duration of `0.9-1.0 s`.
   对应摘录：D
4. 句子 4：The timing budget is explicit at the control level as well, because the design targets sub-`100 ms` EMG-to-PWM response and the measured EMG-to-motion latency remains below `200 ms`.
   对应摘录：A, E
5. 句子 5：Safety handling is embedded in the same supervisory logic: undervoltage forces a passive high-damping mode, control-loop timing violations trigger a watchdog reset with zero torque, and loss of EMG or IMU input forces a conservative stance state that blocks further transitions to swing.
   对应摘录：C
