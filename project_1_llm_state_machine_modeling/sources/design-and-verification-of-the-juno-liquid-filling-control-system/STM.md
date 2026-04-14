# Design and Verification of the JUNO Liquid Filling Control System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然也写 PID 与硬件选型，但 FOC 系统的顺序控制、阈值前置条件、overflow/refill 触发和独立 interlock 逻辑都足够具体，可直接形成 `🌡️` 方向过程控制 EFSM 样本。

## 条目 1: Sequential Filling-Overflow-Circulation Supervisor

- 控制对象：过程与环境控制领域的 JUNO 液体 filling/overflow/circulation 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 JUNO FOC 系统的过程监督控制器，用 PLC、阈值判断、顺序控制和安全联锁来管理液体 filling、overflow/refill 与 online circulation。
- 判断：算。对象是实际大体积液体处理系统的监督控制器，原文明确写出 detection/control/safety 分层、顺序控制的前置条件、联锁动作和 overflow/refill 的阈值触发，不是单纯 PID 调参或实验平台介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction
> The FOC system is responsible for LS filling, overflowing or refilling, and online circulation for LS re-purification. ... The system implements advanced control strategies, including ... sequential logic, and safety interlocks, to achieve closed-loop control of critical parameters such as flow rate, liquid level, and pressure.

#### 摘录 B

- 出处：第 6-7 页，Section 2.1 `System requirement`
> The system is designed to maintain deviations within 1% between the setpoint and feedback value in a closed-loop control. Pumps shall maintain rotational speed stability within ±0.2% of setpoint with ≤10 seconds standby activation. ... safety interlock mechanisms [are required] to mitigate risks to detectors during abnormal conditions. ... a "dual-confirmation" protocol [is used] to prevent hazardous operations caused by mistakes.

#### 摘录 C

- 出处：第 8-11 页，Section 3.1-3.2 `Architecture of the control logic`
> The control system employs a closed-loop control framework through three functional layers: detection, control, and monitoring & safety. ... State-machine-based sequential control enforces step-by-step execution, such as initiating LS exchanging only after tank level and temperature thresholds are met. ... Boolean logic interlocks provide additional protection, triggering actions such as shutting down pumps automatically if pressure goes beyond the safety limits.
>
> For instance, LS exchanging initiation requires the storage tank to reach a preset level while meeting both the LS temperature specifications and calibration house pressure threshold, with the system only ramping up exchange speed after verifying stable low-flow filling to ensure detector safety.

#### 摘录 D

- 出处：第 11-13 页，Section 4 `Test and performance`
> The joint test ... verified two operational modes: (1) LS transfer during LS filling ... and (2) continuous purification recirculation. ... automatic pump control [was] triggered by tank level thresholds.
>
> Overflowing test evaluated two key operational modes: (1) overflowing testing ... verifying automatic replenishment when CD/overflow tank levels dropped below lower thresholds, and (2) overfill protection validation, where overflow valves automatically redirected excess LS back to storage after exceeding upper level limits.

### 2. 基于原文整理后的自然语言描述

The JUNO FOC controller is a supervisory EFSM for three coordinated operating modes: detector filling, overflow/refill compensation, and online liquid circulation. Its control logic is layered into detection, algorithmic control, and monitoring-and-safety functions, and within the control layer it combines PID loops with state-machine-based sequential control and Boolean interlocks rather than relying on continuous regulation alone. Sequential execution is guarded by process variables: LS exchange may begin only after tank-level, liquid-temperature, and calibration-house-pressure thresholds are simultaneously satisfied, and the system ramps from verified low-flow filling to higher-speed transfer only after the safe preconditions are confirmed. The same supervisor also handles overflow behavior by automatically replenishing when tank levels drop below lower thresholds and redirecting excess liquid back to storage when upper limits are exceeded. Independent safety logic, standby timing requirements, and automatic pump shutdown on pressure-limit violation make this a threshold- and mode-driven process controller rather than a pure feedback loop.

### 3. 逐句溯源

1. 句子 1：The JUNO FOC controller is a supervisory EFSM for three coordinated operating modes: detector filling, overflow/refill compensation, and online liquid circulation.
   对应摘录：A, D
2. 句子 2：Its control logic is layered into detection, algorithmic control, and monitoring-and-safety functions, and within the control layer it combines PID loops with state-machine-based sequential control and Boolean interlocks rather than relying on continuous regulation alone.
   对应摘录：C
3. 句子 3：Sequential execution is guarded by process variables: LS exchange may begin only after tank-level, liquid-temperature, and calibration-house-pressure thresholds are simultaneously satisfied, and the system ramps from verified low-flow filling to higher-speed transfer only after the safe preconditions are confirmed.
   对应摘录：C
4. 句子 4：The same supervisor also handles overflow behavior by automatically replenishing when tank levels drop below lower thresholds and redirecting excess liquid back to storage when upper limits are exceeded.
   对应摘录：D
5. 句子 5：Independent safety logic, standby timing requirements, and automatic pump shutdown on pressure-limit violation make this a threshold- and mode-driven process controller rather than a pure feedback loop.
   对应摘录：B, C
