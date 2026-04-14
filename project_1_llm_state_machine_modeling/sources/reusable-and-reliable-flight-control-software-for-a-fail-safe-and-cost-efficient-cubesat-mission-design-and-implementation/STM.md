# Reusable and Reliable Flight-Control Software for a Fail-Safe and Cost-Efficient Cubesat Mission: Design and Implementation - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文提供了 Masat-1 的 operational modes、触发条件和 safe mode 策略，证据较分散但可整理为 CubeSat 控制逻辑样本。

## 条目 1: Closed-mode CONOPS and safe-mode fallback in Masat-1
- 控制对象：Masat-1 CubeSat 飞控软件中的任务/故障管理逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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
- 出处：第 18-20 页，Concept of Operations，对 mode machine、trigger 与 INIT/SAFE/CRITICAL/IDLE/SUN-VIS/ECLIPSE/COMMUNICATION 的说明，行 1092-1209
> We decided to adopt a closed mode of concepts to ensure the deterministic behavior of the spacecraft. Therefore, Masat-1 operating modes are ruled by a finite state machine.
>
> Switching between the Masat-1 operational mode is ruled by four factors: (i) ground telecommand received; (ii) automatic onboard transition when a task or satellite initialization is completed; (iii) the battery charge is under the nominal level; or (iv) an automatic FDIR reconfiguration order upon some anomalies detected.
>
> The boot counter is then updated ... The antenna system deployment mechanism is designed to be executed 45 min after launch ... three attempts to redeploy the antenna were planned ... After a successful deployment, the COM, ADCS system and the payload were initialized ... Thereafter, the Masat-1 shall enter safe mode
>
> Safe mode is entered after INIT mode, upon ground command or after a system fault/failure event.
>
> Critical mode is entered when the battery charge level is under 86%.
>
> IDLE mode is a temporary mode ... Depending on the sun visibility status, the satellite will switch to Sun-Vis or eclipse mode.
>
> Sun-Vis mode is designed to execute the mission’s secondary objectives ... A periodic beacon is sent at the rate of 60 s.
>
> Communication mode is designed to downlink Masat-1 housekeeping and payload data ... the spacecraft is totally commandable in this mode ... the flight-control software shall also run a battery level check periodically, and it will switch the spacecraft to critical mode if the battery level falls under 86%.

#### 摘录 C
- 出处：第 20-21 页，对 mode 内动作与 mission mode 的说明，行 1210-1255
> During safe mode, the following vital functions must be ensured:
> Maintain power supply: the payload is turned off, only vital subsystems are operational, and the beaconing rate is reduced from 60 to 120 s
> Maintain link to ground whenever possible: the satellite receiver shall be always ON waiting for GS command
> Maintain nadir pointing attitude whenever possible
>
> Eclipse mode ... no payload operations or communication with the ground is possible ... the payload is turned off and the ADCS is switched to low power mode
>
> Mission mode: payload-related tasks, namely image acquisition upon delayed commands, image compression and persisting in memory, are carried out in this mode ... The beaconing rate is reduced to 120 s.

#### 摘录 D
- 出处：第 24-27 页，对 application layer FSM 与 hierarchical FDIR 的说明，行 1377-1535
> a service-oriented pattern coupled with a finite state machine to execute Masat-1 mission functionalities in a deterministic manner.
>
> the control logic of the spacecraft is based on a finite state machine implemented at the application layer. When coupled with a closed mode CONOPS, this will ensure the deterministic behavior of the spacecraft.
>
> the “flight planner” ... is in charge of the execution of vital functions/ground commands to ensure the spacecraft integrity and safety
>
> Upon the detection of anomalies, events are raised and are handled through a decision matrix ... the safety monitor sends signals to the flight planner to switch to safe mode.
>
> This mode was implemented to maintain the spacecraft in a safe-guarding configuration when major anomalies occur, and it will remain in this state until next contact with the ground segment.

### 2. 基于原文整理后的自然语言描述

Masat-1 uses a closed-mode concept of operations in which an application-layer finite state machine drives the spacecraft operating modes and the procedures executed in each mode. The machine starts in `INIT`, where the boot counter is updated, antenna deployment is delayed 45 minutes after launch with up to three redeployment attempts, COM/ADCS/payload are initialized, and the spacecraft then enters `SAFE`; subsequent mode transitions are triggered only by ground telecommands, automatic completion of initialization or tasks, battery level dropping below nominal, or automatic FDIR reconfiguration after anomalies. `SAFE` is entered after `INIT`, on ground command, or after a system fault/failure, keeps only vital functions active with reduced beaconing and receiver-on commandability, and stays in a safeguarding configuration until the next ground contact. `CRITICAL` is entered when the battery charge level falls below 86% and turns the payload off while reducing subsystem power until the battery returns to a nominal level; `IDLE` is a temporary mode after safe-mode exit or completion of payload and communication work, and from there the spacecraft branches by sun visibility into `SUN-VIS` or `ECLIPSE`. `SUN-VIS` executes secondary objectives with a 60-second beacon and nadir-pointing standby operations, `ECLIPSE` disables payload and communication activity while keeping low-power housekeeping functions, `MISSION` performs delayed image acquisition, compression, and storage with a 120-second beacon, and `COMMUNICATION` makes the spacecraft fully commandable for real-time or stored downlink while periodically checking battery level and falling back to `CRITICAL` if power again drops below 86%. When anomalies are detected, the safety monitor raises events to the flight planner, and the flight planner forces a switch into `SAFE` according to the hierarchical FDIR logic.

### 3. 逐句溯源

1. 句子 1：Masat-1 uses a closed-mode concept of operations in which an application-layer finite state machine drives the spacecraft operating modes and the procedures executed in each mode.
   对应摘录：A, B, D
2. 句子 2：The machine starts in `INIT`, where the boot counter is updated, antenna deployment is delayed 45 minutes after launch with up to three redeployment attempts, COM/ADCS/payload are initialized, and the spacecraft then enters `SAFE`; subsequent mode transitions are triggered only by ground telecommands, automatic completion of initialization or tasks, battery level dropping below nominal, or automatic FDIR reconfiguration after anomalies.
   对应摘录：B
3. 句子 3：`SAFE` is entered after `INIT`, on ground command, or after a system fault/failure, keeps only vital functions active with reduced beaconing and receiver-on commandability, and stays in a safeguarding configuration until the next ground contact.
   对应摘录：B, C, D
4. 句子 4：`CRITICAL` is entered when the battery charge level falls below 86% and turns the payload off while reducing subsystem power until the battery returns to a nominal level; `IDLE` is a temporary mode after safe-mode exit or completion of payload and communication work, and from there the spacecraft branches by sun visibility into `SUN-VIS` or `ECLIPSE`.
   对应摘录：B, C
5. 句子 5：`SUN-VIS` executes secondary objectives with a 60-second beacon and nadir-pointing standby operations, `ECLIPSE` disables payload and communication activity while keeping low-power housekeeping functions, `MISSION` performs delayed image acquisition, compression, and storage with a 120-second beacon, and `COMMUNICATION` makes the spacecraft fully commandable for real-time or stored downlink while periodically checking battery level and falling back to `CRITICAL` if power again drops below 86%.
   对应摘录：B, C
6. 句子 6：When anomalies are detected, the safety monitor raises events to the flight planner, and the flight planner forces a switch into `SAFE` according to the hierarchical FDIR logic.
   对应摘录：D
