# On-Board Software Development for a 3U CubeSat - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 SharjahSat-1 的八模 mission software、LEOP 等待与超时逻辑、payload/transmit task handoff 以及 autonomous fallback 写得完整，可直接形成高质量 CubeSat 模式管理样本。

## 条目 1: SharjahSat-1 Eight-Mode Mission Software Manager

- 控制对象：SharjahSat-1 CubeSat 的 mission software operation-mode manager
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 3U CubeSat SharjahSat-1 的顶层 mission software manager，用于在 `LEOP / Nominal / Sun-pointing / Safe / Camera Operation / iXRD Operation / Transmit / Autonomous` 八个运行模式之间切换，并通过多个 FreeRTOS task 协调 ADCS、payload、telemetry、beacon 与通信恢复。
- 判断：算。对象是实际 nanosatellite 的机载主控制链，原文明确给出了八个模式的职责、进入与退出条件、`90 minutes / 15 minutes / 3 weeks` 等时间阈值，以及 task-level handoff 机制。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Overview`
> SharjahSat-1 utilizes different operating modes in the mission, such as start-up, normal, safe, recovery; which are switched by a state machine. These various modes incorporate different mission critical parameters as well as attitude control specifications based on the status of other subsystems, especially battery.

#### 摘录 B

- 出处：第 3-4 页，`3.1 Operation Modes`
> There are 8 fundamental operation modes of SharjahSat-1 on the highest level, implemented using 5 different tasks.
>
> LEOP Mode ... waits for 90 minutes ... The LEOP mode ends when a command to end it is received from the ground, or when a timeout of 3 weeks is reached.
>
> Nominal ... The registry is checked to see if a mission is scheduled from the ground station. If there’s one in 15 minutes, the payload or transmit task is notified and the nominal task is suspended.

#### 摘录 C

- 出处：第 4 页，`3.1 Operation Modes`
> The battery voltage is read to check if it fell under a configurable threshold. If that’s the case, switch to safe mode.
>
> The time of last command received from the ground is read to check if a pre-determined time (3 weeks) have passed without a TC. In this case, it is assumed to be an issue with the communication link, and the autonomous mode is activated.
>
> Safe Mode ... no payload operation can be performed. The battery voltage is checked periodically and the last pointing mode is restored when the value exceeds another configurable threshold.

#### 摘录 D

- 出处：第 4-5 页，`3.1 Operation Modes / 3.2 Tasks`
> Camera Operation Mode ... used when there’s 15 minutes or less remaining to an observation mission. The ADCS is used to track the target coordinates on Earth. When the time is reached, photos are taken and the last pointing mode is restored.
>
> Transmit Mode ... The ADCS points the satellite towards the coordinates of the ground station. The beacon and telemetry logging are stopped.
>
> Autonomous Task ... Spawned or resumed from the Nominal Task if the last received telecommand is 3 weeks old. Handles the Autonomous Mode as described above. If a command is received, immediately resumes Nominal Task and suspends itself.

### 2. 基于原文整理后的自然语言描述

The SharjahSat-1 mission software uses a top-level eight-mode state machine with `LEOP`, `Nominal`, `Sun-pointing`, `Safe`, `Camera Operation`, `iXRD Operation`, `Transmit`, and `Autonomous`, and these modes are executed through dedicated FreeRTOS tasks. `LEOP` is the startup mode after launch: it records first boot, waits `90 minutes`, deploys antennas, starts ADCS detumbling, and terminates only when ground control ends it or a `3-week` timeout is reached. In `Nominal`, the controller periodically checks whether a mission is scheduled within `15 minutes`, whether battery voltage has fallen below the safe threshold, and whether no telecommand has been received for `3 weeks`, in which case it suspends the nominal task and hands control to payload, transmit, safe, or autonomous behavior as required. `Safe` disables payload operation and stretches housekeeping intervals until battery voltage recovers above the restore threshold, while `Camera Operation`, `iXRD Operation`, and `Transmit` use ADCS pointing plus task-level handoff to execute scheduled observation or downlink actions and then restore the previous pointing mode. If uplink silence lasts three weeks, `Autonomous` takes over, performs daily payload operation and periodic downlink attempts, and immediately yields back to `Nominal` once a command is received, so the overall controller combines timed startup, battery-guarded degradation, scheduled mission execution, and communication-loss recovery in one explicit flight-software manager.

### 3. 逐句溯源

1. 句子 1：The SharjahSat-1 mission software uses a top-level eight-mode state machine with `LEOP`, `Nominal`, `Sun-pointing`, `Safe`, `Camera Operation`, `iXRD Operation`, `Transmit`, and `Autonomous`, and these modes are executed through dedicated FreeRTOS tasks.
   对应摘录：A, B
2. 句子 2：`LEOP` is the startup mode after launch: it records first boot, waits `90 minutes`, deploys antennas, starts ADCS detumbling, and terminates only when ground control ends it or a `3-week` timeout is reached.
   对应摘录：B
3. 句子 3：In `Nominal`, the controller periodically checks whether a mission is scheduled within `15 minutes`, whether battery voltage has fallen below the safe threshold, and whether no telecommand has been received for `3 weeks`, in which case it suspends the nominal task and hands control to payload, transmit, safe, or autonomous behavior as required.
   对应摘录：B, C
4. 句子 4：`Safe` disables payload operation and stretches housekeeping intervals until battery voltage recovers above the restore threshold, while `Camera Operation`, `iXRD Operation`, and `Transmit` use ADCS pointing plus task-level handoff to execute scheduled observation or downlink actions and then restore the previous pointing mode.
   对应摘录：C, D
5. 句子 5：If uplink silence lasts three weeks, `Autonomous` takes over, performs daily payload operation and periodic downlink attempts, and immediately yields back to `Nominal` once a command is received, so the overall controller combines timed startup, battery-guarded degradation, scheduled mission execution, and communication-loss recovery in one explicit flight-software manager.
   对应摘录：C, D
