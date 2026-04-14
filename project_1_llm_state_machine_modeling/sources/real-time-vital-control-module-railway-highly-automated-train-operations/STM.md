# A real-time vital control module to increase capabilities of railway control systems in highly automated train operations - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 VCM 安全监督器明确写成 Stateflow FSM 到 RTOS 任务的落地链，给出了任务分工、通信周期、硬截止时间和危险场景下的制动介入时序，是高质量铁路监督控制样本。

## 条目 1: VCM application-logic safety supervisor

- 控制对象：面向高等级自动驾驶列车的车载 Vital Control Module 安全监督控制逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是铁路自动运行场景中的车载安全监督器，负责轮询 ATO/里程计/ETCS/紧急制动设备并在超时、失效或危险工况下触发隔离与制动动作。
- 判断：算。对象是真实铁路控制系统中的安全关键车载控制核心，原文不仅说明“用了 FSM”，还把任务拆分、通信周期、优先级、硬截止时间和危险场景响应时延写得很具体。

### 1. 原文摘录

#### 摘录 A

- 出处：Section 1，`paper_content.txt` 第 116-121 行
> The VCM application logic has been conceptualized, developed, and verified as a Finite State Machine (FSM) using the Simulink/Stateflow tool and a model-based approach. Subsequently, the application logic has been exported for implementation on the target system ... The target implementation was carried out by exporting the FSM as scheduled RTOS tasks.

#### 摘录 B

- 出处：Section 2.2，`paper_content.txt` 第 376-389 行
> Task A is designed to dynamically query other on-board subsystems ... Task A assesses the status of the FSMs composing the application logic by analyzing the dedicated status flags. ... Task B checks ATO-OB responses, on-board equipment working and elaborates the speed and position estimations from odometer sensor data; Task C manages procedures to control ETCS-OB and EB systems.

#### 摘录 C

- 出处：Section 4，`paper_content.txt` 第 581-590 行，第 673-687 行
> the interval between consecutive VCM to/from ATO-OB messages is set to 40 ms (+ 4 ms to account for transmission delay). ... this constraint determines the period of Task A ... while maintaining a hard deadline of 2 ms. ... Task C is responsible for activating the emergency brake system (EB) control and ETCS-OB isolation and insertion procedures ... the period and the deadline of Task C must be the same as that of Task B, i.e., 2 ms.

#### 摘录 D

- 出处：Section 5，`paper_content.txt` 第 874-902 行
> Results show that the longest intervention time of the VCM ... consists of 12 ms (worst case). ... the scenarios with the fastest EB intervention time (i.e., 2 ms) are the detection of the failure mode of ATO ... and the expiration of the ATO vitality and operator vigilance timeouts ... in the worst case, the proposed architecture can issue an emergency braking in 536 ms ... still below the expected specification ... of 1 s.

### 2. 基于原文整理后的自然语言描述

The VCM application logic is modeled as a Stateflow finite-state machine and deployed as scheduled RTOS tasks that supervise onboard ATO, odometry, ETCS, and emergency-brake equipment for unsupervised railway operation. Task A queries other subsystems and checks FSM status flags on a `40 ms` communication cycle, Task B validates ATO responses and estimates speed and position, and Task C sequentially handles ETCS isolation or insertion plus emergency-brake actuation with the same `2 ms` period and deadline as Task B. This makes the controller a `T1` railway EFSM with explicit engineering timing rather than a vague safety monitor, because message intervals, priorities, deadlines, and braking flags are all part of the control logic. In hazardous scenarios the architecture reacts in `2-12 ms` at module level, and even the worst composed braking intervention remains about `536 ms`, below the `1 s` specification.

### 3. 逐句溯源

1. 句子 1：The VCM application logic is modeled as a Stateflow finite-state machine and deployed as scheduled RTOS tasks that supervise onboard ATO, odometry, ETCS, and emergency-brake equipment for unsupervised railway operation.
   对应摘录：A, B
2. 句子 2：Task A queries other subsystems and checks FSM status flags on a `40 ms` communication cycle, Task B validates ATO responses and estimates speed and position, and Task C sequentially handles ETCS isolation or insertion plus emergency-brake actuation with the same `2 ms` period and deadline as Task B.
   对应摘录：B, C
3. 句子 3：This makes the controller a `T1` railway EFSM with explicit engineering timing rather than a vague safety monitor, because message intervals, priorities, deadlines, and braking flags are all part of the control logic.
   对应摘录：A, B, C
4. 句子 4：In hazardous scenarios the architecture reacts in `2-12 ms` at module level, and even the worst composed braking intervention remains about `536 ms`, below the `1 s` specification.
   对应摘录：D
