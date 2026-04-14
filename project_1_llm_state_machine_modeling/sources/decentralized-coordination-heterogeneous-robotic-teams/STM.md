# From Design to Deployment: Decentralized Coordination of Heterogeneous Robotic Teams - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出七状态 progressive task allocation FSM，还把 barrier consensus、消息交互和 `BARRIER_TIMEOUT = 600` 的恢复逻辑写清楚，是很强的 swarm-coordination 控制样本。

## 条目 1: Barrier-synchronized progressive task-allocation FSM

- 控制对象：通用控制与机器人任务领域的异构机器人团队去中心化任务分配监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于 heterogeneous aerial/ground robot team 的 seven-state progressive task-allocation controller，通过 barrier consensus 和消息交互把空闲机器人逐步吸纳进任务编队。
- 判断：算。对象是实际 deployed multi-robot behavior law，而不是 Buzz 语言教程或中间件框架；原文给出了状态名、进入条件、邻居请求/批准逻辑，以及超时恢复和同步 barrier。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，Section `2.4.1 Barrier`，`paper_content.txt` 第 423-440、491-499 行
> ... to create swarm-level state machines, where all robots agree on the current state of the swarm (or sub-swarm). For this purpose, we designed a barrier mechanism ...
>
> BARRIER_TIMEOUT = 600 # Timeout value in ~steps
>
> ... if it reaches the swarm size, the robot checks all values to ensure every unit is ready to go to the next state ... Otherwise, after a timeout (timeIn equals BARRIER_TIMEOUT), the robot resumes its previous behavior.

#### 摘录 B

- 出处：第 8 页，Figure `5` 说明，`paper_content.txt` 第 563-567 行
> The behavior law of the progressive task allocation algorithm represented as a finite state machine. Every robot joining the mission will experience states TurnedOff, TakeOff, Free, Asking, Joining and Joined. Before switching to state Free, and Lock the robots wait for consensus in a transition barrier state.

#### 摘录 C

- 出处：第 8-9 页，Section `3.1.1 Algorithm`，`paper_content.txt` 第 603-629 行
> The behavior law is represented as a finite state machine ... It consists of seven states: Turned Off, Take Off, Free, Asking, Joining, Joined and Lock.
>
> ... In state Free, the robot will circle around the edge of the mission zone ... and search for a proper task ...
>
> When such a task is found ... the Free robot will transit to state Asking, sending a message to request for the task. Once the request is approved ... the robot transits to state Joining ... With the knowledge of its Joined parent and of its own task position, the robot will compute its target GPS coordinates and navigate to it.

#### 摘录 D

- 出处：第 9 页，Section `3.1.2 Simulations`，`paper_content.txt` 第 639-649、671-672 行
> ... the algorithm and its robustness to imperfect communication.
>
> ... Without packet lost the simulated fleet converge in <30 s while with a packet drop rate of 90%, the robots take almost 45 s.
>
> The most significant output of this set of simulations is that consensus is always reached, even with large packet drop probability.

### 2. 基于原文整理后的自然语言描述

The progressive task-allocation behavior in ROSBuzz is governed by a seven-state FSM that moves heterogeneous UAVs and rovers from powered-off units into a synchronized mission formation. After mission start, robots move from `Turned Off` to `Take Off` and then through a consensus barrier before either acting as the root joined robot or entering `Free`, where they circle the mission edge and search for admissible tasks via neighbor interactions. When a free robot finds a task whose predecessors are visible, it enters `Asking`, waits for approval from `Joining` and `Joined` robots, and then transitions to `Joining`, where it computes the target GPS position and navigates to the assigned task. Once the robot reaches its target it becomes `Joined`, while `Lock` and the barrier states are used to synchronize safe swarm-wide transitions. The barrier itself is timed: robots share candidate outgoing states in virtual stigmergy, switch only when all values agree, and fall back to a safe resume behavior if `BARRIER_TIMEOUT = 600` expires, so the controller is a timed coordination FSM rather than an untimed abstract protocol.

### 3. 逐句溯源

1. 句子 1：The progressive task-allocation behavior in ROSBuzz is governed by a seven-state FSM that moves heterogeneous UAVs and rovers from powered-off units into a synchronized mission formation.
   对应摘录：B, C
2. 句子 2：After mission start, robots move from `Turned Off` to `Take Off` and then through a consensus barrier before either acting as the root joined robot or entering `Free`, where they circle the mission edge and search for admissible tasks via neighbor interactions.
   对应摘录：B, C
3. 句子 3：When a free robot finds a task whose predecessors are visible, it enters `Asking`, waits for approval from `Joining` and `Joined` robots, and then transitions to `Joining`, where it computes the target GPS position and navigates to the assigned task.
   对应摘录：C
4. 句子 4：Once the robot reaches its target it becomes `Joined`, while `Lock` and the barrier states are used to synchronize safe swarm-wide transitions.
   对应摘录：B, C
5. 句子 5：The barrier itself is timed: robots share candidate outgoing states in virtual stigmergy, switch only when all values agree, and fall back to a safe resume behavior if `BARRIER_TIMEOUT = 600` expires, so the controller is a timed coordination FSM rather than an untimed abstract protocol.
   对应摘录：A, D
