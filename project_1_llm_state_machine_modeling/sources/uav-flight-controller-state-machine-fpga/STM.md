# Design, Development and Implementation of a UAV flight controller based on a State Machine approach using a FPGA embedded system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 fixed-wing UAV 的 CPU flight-mode machine、传感器触发条件和 emergency parachute sequence 全部写成可执行状态表，是清晰的飞行监督控制样本。

## 条目 1: Twelve-State UAV Flight-Mode and Emergency Supervisor

- 控制对象：固定翼无人机飞控中的模式切换与紧急降落监督器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行控制领域的 fixed-wing UAV flight supervisor，用 CPU 状态机在起飞、爬升、下降、转弯、巡航和紧急模式间切换，并由并行 emergency module 监测异常后强制执行降落/降伞链。
- 判断：算。对象是实际飞控控制器，原文给出了状态表、输入触发条件、各状态的控制输出，以及异常持续 `3 seconds` 后切换到 emergency 的完整处理链，而不是只谈 FPGA 架构性能。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 27-49 行
> This article presents the development of a fixed-wing UAV flight controller ... The flight controller is based on a state machine system that migrates from state to state depending on the stimulus received from sensors like accelerometers, tachometers, compass, pitot, GPS, etc. Another feature developed in this project is an emergency system that provides enough intelligence and robustness to secure the integrity of the aircraft in case a problem occurs during missions.

#### 摘录 B

- 出处：第 3 页，`CPU` / `Table 1`，`paper_content.txt` 第 225-319 行
> Code number State Inputs Outputs
>
> 00 Takeoff-Free State ... Actuators controlled by user with no compensation
> 01 Climb ...
> 02 Descent ...
> 03 Turn Right ...
> 04 Turn Left ...
> 05 Climb Right ...
> 06 Climb Left ...
> 07 Descent Right ...
> 08 Descent Left ...
> 09 Cruise 1 ...
> 10 Cruise 2 - Changeable Speed ...
> 11 Emergency se = 1 OR Emergency detected by sensors ... Parachute and actuators emergency sequence activated

#### 摘录 C

- 出处：第 3-4、6 页，`Emergency System` 与 `Emergency System Simulation`，`paper_content.txt` 第 331-370、585-615 行
> If any of the five emergency conditions are activated, a three seconds timer will be activated in the emergency system block. ... If the variable that has been activated does not return to its normal value, a flag is set on high in the control unit by the emergency system module. This high value will cause the control unit to change its current state to emergency state.
>
> The next sequence will be executed once the emergency state is on:
> Brushless motor off
> All servomotors change the control surfaces positions back to neutral position.
> Three seconds timer is activated in order to wait for the UAV’s own aerodynamics stabilize it
> Parachute releasing mechanism is activated
> All servo motors are turned off
>
> The CPU receives the alarm signal and immediately changes its current state to the emergency state ...

### 2. 基于原文整理后的自然语言描述

The UAV flight controller is organized as a sensor-driven finite state machine whose CPU distinguishes `Takeoff-Free`, `Climb`, `Descent`, `Turn Right`, `Turn Left`, `Climb Right`, `Climb Left`, `Descent Right`, `Descent Left`, `Cruise 1`, `Cruise 2`, and `Emergency`. These states are selected from explicit input combinations involving reset, pilot switches `sw1/sw2`, elevator and aileron commands, and the emergency signal `se`, and each state maps to a different compensation policy for pitch, roll, speed, or direct user control. In parallel with that CPU state machine, the emergency subsystem watches for five abnormal conditions and starts a `three seconds` confirmation timer so transient sensor misreadings do not trigger an unnecessary fail-safe transition. If the abnormal condition persists, the subsystem raises the alarm flag, forces the CPU into `Emergency`, turns off the brushless motor, neutralizes the control surfaces, waits another `three seconds` for aerodynamic stabilization, releases the parachute, and finally turns off the servomotors.

### 3. 逐句溯源

1. 句子 1：The UAV flight controller is organized as a sensor-driven finite state machine whose CPU distinguishes `Takeoff-Free`, `Climb`, `Descent`, `Turn Right`, `Turn Left`, `Climb Right`, `Climb Left`, `Descent Right`, `Descent Left`, `Cruise 1`, `Cruise 2`, and `Emergency`.
   对应摘录：A, B
2. 句子 2：These states are selected from explicit input combinations involving reset, pilot switches `sw1/sw2`, elevator and aileron commands, and the emergency signal `se`, and each state maps to a different compensation policy for pitch, roll, speed, or direct user control.
   对应摘录：B
3. 句子 3：In parallel with that CPU state machine, the emergency subsystem watches for five abnormal conditions and starts a `three seconds` confirmation timer so transient sensor misreadings do not trigger an unnecessary fail-safe transition.
   对应摘录：A, C
4. 句子 4：If the abnormal condition persists, the subsystem raises the alarm flag, forces the CPU into `Emergency`, turns off the brushless motor, neutralizes the control surfaces, waits another `three seconds` for aerodynamic stabilization, releases the parachute, and finally turns off the servomotors.
   对应摘录：B, C
