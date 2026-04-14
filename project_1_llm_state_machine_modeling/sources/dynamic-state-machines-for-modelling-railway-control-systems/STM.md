# Dynamic State Machines for Modelling Railway Control Systems - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行, 协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然提出的是 `DSTM` 语言，但真正落地的对象是 `ERTMS/ETCS` 里的 `RBC` 通信管理过程，原文把连接建立、会话建立、行车授权、紧急停车与任务结束链写得足够细，还显式给出了并发管理多列车实例和抢占式 join。

## 条目 1: RBC communication-management hierarchical supervisor

- 控制对象：轨道交通与铁路控制领域的 `Radio Block Centre` 通信建立、会话建立与行车授权管理监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行, 协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `ERTMS/ETCS` 高速区 `RBC` 的通信管理控制器，用于在列车进入受控区域后处理连接请求、会话建立、分发 `Movement Authority`、响应 `CTC` 紧急停车命令并在任务结束时完成会话收尾。
- 判断：算。对象不是工具流程，而是实际铁路控制系统里的 vital core 功能；原文明确把该功能拆成分层状态机、动态实例化的列车管理流程、消息协议步骤以及紧急/结束分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 24-29, 35-40, 85-91 行
> This paper introduces a novel class of hierarchical state machines, called Dynamic STate Machines (DSTMs), and proposes an approach for modelling and validating railway control systems, based on the new specification language.
>
> Key features of DSTM are recursive execution, parallelism, parameter passing, abortion transition, and communication through global variables and channels, but its main peculiarity resides in the semantics of fork and join operators which allows for dynamic instantiation of machines (processes).
>
> The language and the proposed approach are illustrated and motivated by applying them to a specific functionality of the Radio Block Centre, the vital core of the ERTMS/ETCS Control System.

#### 摘录 B

- 出处：第 6 页，RBC communication management procedure，`paper_content.txt` 第 268-286 行
> Step 1: communication establishment ... RBC may accept only connection requests from a limited number of trains ... RBC sends to the train a connection accepted notification ... If the new connection request exceeds the bound, RBC refuses the connection ...
>
> Step 2: session establishment ... RBC authorizes the train to start the mission procedure ... The Session Established message is a structured message containing an area field used by RBC to distinguish between a train that needs to start its mission (L0 area) and a train coming from outside a high-speed area (L1 area) ... If a message different from the expected one is received during this protocol, the session establishment procedure aborts and the communication with the train is closed.
>
> Step 3: management of train movement RBC periodically sends the Movement Authority (MA) to each train and checks for the reception of commands from the Centralized Traffic Control (CTC), where a human operator may raise alarms requiring the train to stop. In this case an Unconditional Emergency Stop (UES) message is sent to the train. When the train successfully ends its trip, RBC performs the End of Mission (EoM) procedure.

#### 摘录 C

- 出处：第 9 页，对 `M_CommunicationEstablishment` 的并发说明，`paper_content.txt` 第 445-461 行
> The asynchronous fork transition T04 creates a loop ... The idea is that when process M_CommunicationEstablishment performs the asynchronous fork T04, it continues its execution in parallel with the activated process M_ManageTrain.
>
> Being still active, process M_CommunicationEstablishment might fire transition T03 again, and a second activation of machine M_ManageTrain would occur.
>
> In the example, the number of activations of machine M_ManageTrain that can be concurrently active is at most 4 ... one can activate an arbitrary number of processes and each activation can be endowed with a private communication channel.

#### 摘录 D

- 出处：第 10 页，对 `M_MovAuth` 的 preemptive join 说明，`paper_content.txt` 第 469-482 行
> Let us now consider machine M_MovAuth in Fig. 3.
>
> ... transitions T07 and T10 enter the join pseudonodes ... graphically representing the fact that those transitions perform a preemptive synchronization of the processes involved in their respective join.
>
> In particular, when process M_CentralControl terminates at its exit node ues, transition T07 fires and the execution of process M_PeriodicMA is interrupted. As a consequence, termination of the process M_CentralControl ... leads to the subsequent activation of process M_EmergencyManagement.
>
> Similarly, termination of process M_PeriodicMA leads to the termination of the process M_CentralControl and to the activation of process M_EndOfMission.

### 2. 基于原文整理后的自然语言描述

The retained control object is the `RBC` communication-management supervisor, the vital railway-control function that handles a train from the moment it requests access to the radio channel until the mission is ended or emergency stopping is required. Its top-level procedure is explicitly organized into three mission phases: `communication establishment`, where the RBC accepts or refuses a request according to channel capacity; `session establishment`, where the train is classified as `L0` or `L1`, the correct start/entry procedure is selected, and any unexpected message aborts the session; and `management of train movement`, where the RBC periodically issues `Movement Authority`, listens for `CTC` alarms, sends `UES` when necessary, and finally triggers `End of Mission`. The implementation is not flat: `M_CommunicationEstablishment` asynchronously forks per-train `M_ManageTrain` instances, keeps accepting further requests in parallel, and uses private channels to distinguish the active train sessions. Inside `M_MovAuth`, preemptive joins coordinate `CentralControl` and `PeriodicMA`, so a central alarm interrupts periodic authority updates and activates `EmergencyManagement`, while normal completion of periodic movement handling interrupts the other branch and activates `EndOfMission`. Taken together, the paper exposes a genuinely hierarchical railway supervisor whose control semantics combine protocol phases, parallel session handling, and explicit emergency-preemption logic.

### 3. 逐句溯源

1. 句子 1：The retained control object is the `RBC` communication-management supervisor, the vital railway-control function that handles a train from the moment it requests access to the radio channel until the mission is ended or emergency stopping is required.
   对应摘录：A, B
2. 句子 2：Its top-level procedure is explicitly organized into three mission phases: `communication establishment`, where the RBC accepts or refuses a request according to channel capacity; `session establishment`, where the train is classified as `L0` or `L1`, the correct start/entry procedure is selected, and any unexpected message aborts the session; and `management of train movement`, where the RBC periodically issues `Movement Authority`, listens for `CTC` alarms, sends `UES` when necessary, and finally triggers `End of Mission`.
   对应摘录：B
3. 句子 3：The implementation is not flat: `M_CommunicationEstablishment` asynchronously forks per-train `M_ManageTrain` instances, keeps accepting further requests in parallel, and uses private channels to distinguish the active train sessions.
   对应摘录：A, C
4. 句子 4：Inside `M_MovAuth`, preemptive joins coordinate `CentralControl` and `PeriodicMA`, so a central alarm interrupts periodic authority updates and activates `EmergencyManagement`, while normal completion of periodic movement handling interrupts the other branch and activates `EndOfMission`.
   对应摘录：D
5. 句子 5：Taken together, the paper exposes a genuinely hierarchical railway supervisor whose control semantics combine protocol phases, parallel session handling, and explicit emergency-preemption logic.
   对应摘录：A, B, C, D
