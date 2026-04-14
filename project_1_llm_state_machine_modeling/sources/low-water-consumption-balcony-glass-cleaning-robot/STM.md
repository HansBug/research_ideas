# Design and Implementation of a Low-Water-Consumption Robotic System for Cleaning Residential Balcony Glass Walls - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把住宅阳台玻璃清洁机器人写成五态事件驱动监督器，并给出 `e0-e5 / ef` 触发、PID 电流闭环、`<50 ms` fault interrupt 和 `200 ms` watchdog 保护，能稳定支撑双 A。

## 条目 1: Low-water balcony-glass cleaning supervisor with fault-interrupt recovery

- 控制对象：楼宇机电与建筑维护领域的住宅阳台玻璃清洁机器人事件驱动监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向住宅阳台玻璃清洁的机器人监督器，用 `S0-S4` 五个状态协调归零、润湿、刷洗、回收和故障保护。
- 判断：算。对象是真实建筑维护机器人控制器，不是机械结构说明；原文明确给出了 nominal 状态、`e0-e5 / ef` 事件、current spike / low fluid / watchdog 等 fault guard，以及实验场景中的状态映射。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9-10 页，`Control Logic and Deterministic State Transition`，`paper_content.txt` 第 438-489 行
> The AWCS control algorithm is implemented as a formal event-driven Finite State Machine (FSM).
> S0 (Homing/Initialization) ... S1 (Wetting) ... S2 (Scrubbing) ... S3 (Vacuuming/Recovery) ... S4 (Emergency/Fault).
> e0 (Start) ... e1 (Home Confirmed) ... e2 (Fluid Ready) ... e3 (Path Complete) ... e4 (Cycle Success) ...
> e5 (Mechanical Fault) ... ef (Asynchronous Fault) ... force an immediate transition to the safety state S4 from any active operational phase.

#### 摘录 B

- 出处：第 15-16 页，`Experimental Validation Scenarios and FSM Performance`，`paper_content.txt` 第 624-670 行
> The operational reliability, deterministic behavior, and safety mechanisms of the AWCS were validated through five controlled experimental scenarios.
> Scenario 1 ... entered the S0 (Homing/Initialization) state.
> Scenario 2 ... deterministic transitions between S1 (Wetting) and S2 (Scrubbing) ... stable torque regulation.
> Scenario 3 ... transitioned via e3 to S3 (Vacuuming/Recovery) ... recovery efficiency exceeding 90%.
> Scenario 4 ... generated an asynchronous interrupt (ef), forcing an immediate transition to S4 (Emergency/Fault) within <50 ms.
> Scenario 5 ... triggered an ef transition to S4 ... preventing pump dry-running.

#### 摘录 C

- 出处：第 20 页，`Logic-Driven Failsafe Protocols`，`paper_content.txt` 第 921-930 行
> The control architecture integrates multi-sensor feedback to trigger immediate transitions to the S4 (Emergency/Fault) state if operational thresholds are exceeded:
> Spatial Boundary Detection ...
> Torque and Stall Protection (ACS712) ...
> Protocol Latency Monitoring (Watchdog Timer) ... Latency exceeding 200 ms triggers a safe-stop mode.
> Dry-Run Prevention ... low-fluid conditions.

### 2. 基于原文整理后的自然语言描述

The balcony-glass cleaning robot is supervised by a five-state EFSM whose nominal cycle is `S0 Homing/Initialization → S1 Wetting → S2 Scrubbing → S3 Vacuuming/Recovery`, with `S4 Emergency/Fault` reachable as a high-priority interrupt state from any active phase. The transition events are explicit and operational: `e0` starts homing, `e1` confirms the reference position, `e2` signals sufficient wetting for scrubbing, `e3` marks end-of-track and launches recovery, and `e4` closes a successful cycle back to home or idle. During `S2`, the DC 775 scrubbing motor runs under PID-based PWM current control so the discrete supervisor remains coupled to continuous torque regulation instead of only sequencing actuators. Fault management is also stateful and timed: mechanical over-torque, track-boundary violation, low-fluid detection, or watchdog latency beyond `200 ms` force an interrupt to `S4`, and the experiments show the asynchronous failsafe can halt the system within `<50 ms`.

### 3. 逐句溯源

1. 句子 1：The balcony-glass cleaning robot is supervised by a five-state EFSM whose nominal cycle is `S0 Homing/Initialization → S1 Wetting → S2 Scrubbing → S3 Vacuuming/Recovery`, with `S4 Emergency/Fault` reachable as a high-priority interrupt state from any active phase.
   对应摘录：A
2. 句子 2：The transition events are explicit and operational: `e0` starts homing, `e1` confirms the reference position, `e2` signals sufficient wetting for scrubbing, `e3` marks end-of-track and launches recovery, and `e4` closes a successful cycle back to home or idle.
   对应摘录：A
3. 句子 3：During `S2`, the DC 775 scrubbing motor runs under PID-based PWM current control so the discrete supervisor remains coupled to continuous torque regulation instead of only sequencing actuators.
   对应摘录：A, B
4. 句子 4：Fault management is also stateful and timed: mechanical over-torque, track-boundary violation, low-fluid detection, or watchdog latency beyond `200 ms` force an interrupt to `S4`, and the experiments show the asynchronous failsafe can halt the system within `<50 ms`.
   对应摘录：A, B, C
