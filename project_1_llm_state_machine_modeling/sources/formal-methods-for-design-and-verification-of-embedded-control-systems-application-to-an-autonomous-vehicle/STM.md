# Formal Methods for Design and Verification of Embedded Control Systems: Application to an Autonomous Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不只是抽象讲 formal methods，而是把 `Gcdrive` 执行接口的急停仲裁明确写成 `Unknown / Paused / Disabled / Running / Resuming / Shifting` FSM，并带 `5 sec` resume timeout，适合作为车辆安全仲裁样本。

## 条目 1: Gcdrive E-Stop Arbitration FSM with Resume Timeout

- 控制对象：汽车与道路车辆控制领域的 Alice 自动驾驶车辆 `Gcdrive` 执行接口与急停仲裁控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 DARPA Urban Challenge 自动驾驶车辆 Alice 中 `Gcdrive` 的 actuation interface 状态机，用于仲裁 Path Follower 与 DARPA 发来的 `estop pause / run / disable` 命令并安全控制油门、制动和换挡。
- 判断：算。对象是实际自动驾驶车辆的执行接口控制器，而不是纯形式化示例；原文直接给出状态图、状态动作、超时条件、外部命令集和要满足的安全性质。

### 1. 原文摘录

#### 摘录 A

- 出处：第 31 页，Figure `4.3` 与相邻正文，`paper_content.txt` 第 1077-1112 行
> `Disabled (D) - depress brakes - send trans disable - reject all directives`; `Paused (P) - depress brakes - reject all directives except steering`; `Resuming (Re) - start timer on entry - transition after 5 sec`; `Running (Ru) - normal operating state - process all directives`; `Shifting (S) - reject all directives - transition when shift is completed`. ... Gcdrive takes independent commands from Path Follower and DARPA ... Commands from DARPA include estop pause, estop run and estop disable.

#### 摘录 B

- 出处：第 31-32 页，Section `4.3 Verification of Gcdrive Finite State Machine`，`paper_content.txt` 第 1104-1111 行
> An estop pause command should cause the vehicle to be brought quickly and safely to a rolling stop. An estop run command resumes the operation of the vehicle. An estop disable command is used to stop the vehicle and put it in the disable mode. A vehicle that is in the disable mode may not restart in response to an estop run command.

#### 摘录 C

- 出处：第 32 页，global variables，`paper_content.txt` 第 1116-1133 行
> `state ∈ {DISABLED (D), PAUSED (P), RUNNING (Ru), RESUMING (Re), SHIFTING (S)}` ... `estop ∈ {DISABLE (0), PAUSE (1), RUN (2)}` ... `timer ∈ {0,1,2,3,4,5}` keeps track of the time after which the latest estop run command is received.

#### 摘录 D

- 出处：第 33 页，desired properties，`paper_content.txt` 第 1147-1168 行
> If DARPA sends an estop disable command, Gcdrive state will eventually stay at `DISABLED` and `Acceleration Module` will eventually command full brake forever. ... If DARPA sends an estop pause command while the vehicle is not disabled, eventually Gcdrive state will be `PAUSED`. ... If the current state is `RESUMING`, eventually the state will be `RUNNING` or DARPA will send an estop disable or pause command. ... If the current state is `DISABLED, PAUSED, RESUMING or SHIFTING`, `acc = -1`.

### 2. 基于原文整理后的自然语言描述

The `Gcdrive` actuation interface is implemented as a finite-state safety arbitration machine between Path Follower commands and DARPA emergency-stop commands. Its explicit states are `Disabled`, `Paused`, `Running`, `Resuming`, and `Shifting`, with an `Unknown` start state shown in the figure, and each state defines concrete actuator behavior such as braking, transmission disable, directive rejection, or normal directive processing. The external trigger alphabet is also explicit: DARPA may send `estop pause`, `estop run`, or `estop disable`, and the controller must react by forcing a rolling stop, resuming operation, or entering a non-restartable disable mode. The machine carries a local timer because `Resuming` starts a timer on entry and transitions after `5 sec`, so the resume path is not instantaneous but governed by an engineering timeout. The safety properties written below the FSM make the control consequences precise: `DISABLED`, `PAUSED`, `RESUMING`, and `SHIFTING` all require full braking, `DISABLED` also forces gear zero, and a disable command eventually locks the machine in the disabled state. This makes the FSM a concrete vehicle-side execution and emergency arbitration controller rather than a purely formal toy example.

### 3. 逐句溯源

1. 句子 1：The `Gcdrive` actuation interface is implemented as a finite-state safety arbitration machine between Path Follower commands and DARPA emergency-stop commands.
   对应摘录：A, B
2. 句子 2：Its explicit states are `Disabled`, `Paused`, `Running`, `Resuming`, and `Shifting`, with an `Unknown` start state shown in the figure, and each state defines concrete actuator behavior such as braking, transmission disable, directive rejection, or normal directive processing.
   对应摘录：A
3. 句子 3：The external trigger alphabet is also explicit: DARPA may send `estop pause`, `estop run`, or `estop disable`, and the controller must react by forcing a rolling stop, resuming operation, or entering a non-restartable disable mode.
   对应摘录：A, B
4. 句子 4：The machine carries a local timer because `Resuming` starts a timer on entry and transitions after `5 sec`, so the resume path is not instantaneous but governed by an engineering timeout.
   对应摘录：A, C
5. 句子 5：The safety properties written below the FSM make the control consequences precise: `DISABLED`, `PAUSED`, `RESUMING`, and `SHIFTING` all require full braking, `DISABLED` also forces gear zero, and a disable command eventually locks the machine in the disabled state.
   对应摘录：D
