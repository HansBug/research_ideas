# Development and Implementation of Automated Planning in CubeSats - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 MOCI CubeSat 的六模 mission-operations 链、进入条件、退出条件和调度中断规则写得较完整，可直接作为 CubeSat 地面计划与机载 mode manager 的双 A 样本。

## 条目 1: MOCI Mission-Mode Scheduler and Executor

- 控制对象：MOCI CubeSat 的 mission mode scheduler 与机载模式执行控制链
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 CubeSat 任务规划领域中 MOCI 卫星的顶层运行模式管理器，用于在 `Cruise / Power Generation / Scan / Data Processing / Data Downlink / Safe` 六个模式之间按人工命令、排程命令、任务完成和异常触发进行切换，并配合地面 MASS 计划器发出的定时任务执行。
- 判断：算。对象是实际 CubeSat mission operations 的主控制链，原文明确给出了模式集合、切换触发类型、扫描/处理/下传的进入与退出条件，以及 `50 min / 75 min / 60 min / 20 degrees / 75%` 这类工程约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 8 页，`Introduction to MOCI / Introduction to Operational Rules`
> Ground station controllers may command the satellite to assume five separate nominal operational modes defined as follows: Cruise Mode, a power positive idle state; Power Generation Mode, a power positive idle state used when maximum charging capabilities are required; Scan Mode, a target tracking mode used to collect images of the Earth’s surface; Data Processing Mode, the primary computational mode to process collected imagery; and Data Downlink Mode, the science communication mode for transmitting processed data over S-Band radio. In addition to these nominal modes of operation, there is also Safe Mode which can be used by the satellite to autonomously identify and prevent non-nominal operations within the software or hardware.

#### 摘录 B

- 出处：第 8-9 页，`Introduction to Operational Rules / Table 3`
> There are generally four initial conditions that will trigger a transition between modes: a manual command from the ground station, a scheduled command from the scheduler’s queue, the completion of a task, and an automated transition to Safe Mode because of an anomaly.
>
> Cruise mode has the simplest operational rules. Since the satellite is in an idle state in this mode, this mode is always the current state when no task needs to be done on the satellite.

#### 摘录 C

- 出处：第 9 页，`Table 4: Scan Mode Rules`
> A scan of a ground target should not be considered within 50 minutes of a ground station pass in order to maximize available antenna time.
>
> A scan should only be scheduled to start at five minutes prior to a pass directly over a target.
>
> Battery state-of-charge should be over 75%. This is also verified by FSW.
>
> There should be available storage onboard for collected data. This is also verified by FSW.

#### 摘录 D

- 出处：第 10 页，`Table 5 / Table 6 / Table 7 / MASS to MOCI Pipeline`
> A processing period should not be considered within 75 minutes of a ground station pass in order to maximize available antenna time.
>
> A processing period should not be considered within 75 minutes of the start of a priority target pass.
>
> The processing takes longer than 60 minutes. In this case, the processing state is again saved for later completion.
>
> The satellite is passing the ground station with an elevation above 20 degrees.
>
> Once onboard, the scheduler begins timed interrupts for the beginning of each task. Once these interrupts execute, all the needed checks occur for the desired mode transition and the task begins.

### 2. 基于原文整理后的自然语言描述

The MOCI mission software is organized as a six-mode operational FSM with `Cruise`, `Power Generation`, `Scan`, `Data Processing`, `Data Downlink`, and `Safe`, and the scheduler moves between these modes in response to manual commands, queued scheduled commands, task completion, or anomaly-driven entry into `Safe`. `Cruise` acts as the default idle state when no other activity is pending, while `Scan` may begin only when the target window is valid, the pass starts about five minutes before overflight, the battery state of charge stays above `75%`, storage is available, and the scan is not scheduled within `50 minutes` of a ground-station pass. `Data Processing` is similarly guarded by mission timing and power checks: it should start after eclipse-to-sunlight transition, must stay outside the `75-minute` windows before a station pass or a priority target pass, requires stored images and sufficient battery, and is forced to save state and exit if processing exceeds `60 minutes`. `Data Downlink` may run only when the spacecraft is above `20 degrees` elevation over the ground station, there is stored data to send, and battery energy is sufficient for the session. MASS converts these mode decisions into parameterized schedules, uploads them to the satellite, and the onboard scheduler starts each approved task through timed interrupts, so the overall controller is a timed mission-mode executor rather than a loose planning guideline.

### 3. 逐句溯源

1. 句子 1：The MOCI mission software is organized as a six-mode operational FSM with `Cruise`, `Power Generation`, `Scan`, `Data Processing`, `Data Downlink`, and `Safe`, and the scheduler moves between these modes in response to manual commands, queued scheduled commands, task completion, or anomaly-driven entry into `Safe`.
   对应摘录：A, B
2. 句子 2：`Cruise` acts as the default idle state when no other activity is pending, while `Scan` may begin only when the target window is valid, the pass starts about five minutes before overflight, the battery state of charge stays above `75%`, storage is available, and the scan is not scheduled within `50 minutes` of a ground-station pass.
   对应摘录：B, C
3. 句子 3：`Data Processing` is similarly guarded by mission timing and power checks: it should start after eclipse-to-sunlight transition, must stay outside the `75-minute` windows before a station pass or a priority target pass, requires stored images and sufficient battery, and is forced to save state and exit if processing exceeds `60 minutes`.
   对应摘录：D
4. 句子 4：`Data Downlink` may run only when the spacecraft is above `20 degrees` elevation over the ground station, there is stored data to send, and battery energy is sufficient for the session.
   对应摘录：D
5. 句子 5：MASS converts these mode decisions into parameterized schedules, uploads them to the satellite, and the onboard scheduler starts each approved task through timed interrupts, so the overall controller is a timed mission-mode executor rather than a loose planning guideline.
   对应摘录：D
