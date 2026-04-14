# A Finite State Machine Guidance Architecture for Autonomous Rendezvous with Arbitrarily Elliptic Targets - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把航天器自主交会 guidance layer 明确建成 WSE/SSE 双主状态的分层 FSM，并给出 hold point、TTL 和 drift threshold 等工程定时语义。

## 条目 1: WSE-SSE Layered Guidance FSM for Autonomous Rendezvous
- 控制对象：航天器自主交会任务的 guidance software
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是自主交会任务中的机载 guidance layer，用于在 `WSE` 与 `SSE` 两个主状态、各自的控制子模块以及 waiting / TTL 逻辑之间切换，从而安全地逼近目标航天器。
- 判断：算。对象是实际航天器交会控制软件，原文明确给出主状态、分层结构、子控制模块、漂移阈值、hold duration 和 temporal transition logic。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页与第 3 页，Abstract / Introduction，行 25-39, 116-145
> This paper details the design of a guidance architecture, in the form of a layered, finite state machine, meant to enable safe and autonomous rendezvous operations ...
>
> This approach defines the behavior of the chaser spacecraft using a state machine model, characterized by a set of predefined modes and transitions between them ...
>
> At the highest level, this study implements guidance software that switches between a Walking Safe Ellipse (WSE) and a Stationary Safe Ellipse (SSE) state, based on the estimated value of the relative drift between satellites.

#### 摘录 B
- 出处：第 16-17 页，Section 4 `finite state machine guidance` / Figure 4-5，行 996-1078
> the realization of the FSM is based on the autonomous maneuvering capability of the chaser to switch between two main states: a Walking Safe Ellipse (WSE) and a Stationary Safe Ellipse (SSE) state ...
>
> At the upper layer, three truth tables command the high-level behavior of the agent: the Timeline Manager ... whereas the WSE/SSE status analyzes the current relative orbit ...
>
> Decisions from the timeline manager determine the transitions between the main states of the FSM ...
>
> Classification from the WSE/SSE status truth tables is used to inform decisions in the control layer ...
>
> Transitions to the stand-by (or waiting) states are triggered by completion of a selected maneuver scheme ...
>
> “Compute drift” provides the necessary aδa to reach the next hold point in a prescribed time ... triggered by temporal transition logic (TTL).

#### 摘录 C
- 出处：第 27 页，Table 9 `Common simulation data`，行 1424-1437
> FSM relative E/I separation phase threshold `5 deg`
>
> FSM SSE relative drift threshold `1 m`
>
> FSM WSE maximum relative drift `100 m`
>
> FSM WSE minimum relative drift `3 m`
>
> FSM WSE nominal drift period between waypoints `5 orbits`

### 2. 基于原文整理后的自然语言描述

The autonomous-rendezvous guidance software is organized as a layered HSM whose two main states are `Walking Safe Ellipse (WSE)` and `Stationary Safe Ellipse (SSE)`, selected according to the estimated relative drift between the chaser and the target. Above the control layer, a `Timeline Manager` truth table checks whether the spacecraft is inside or outside the next hold point and a `WSE/SSE` status layer classifies the current relative orbit so that the proper maneuver family can be selected. Inside the control layer, both `WSE` and `SSE` expand into subordinate modes such as `stand-by`, `safe sizing`, `station keeping`, `shape control`, and `compute drift`, and maneuver completion returns the machine to waiting states. The machine therefore does not just switch geometry modes; it also schedules when to move or stop, computes the drift needed to hit the next hold point, and re-invokes drift computation if the target SSE slot has not been reached within the prescribed TTL window. The timing side is explicit: the guidance uses hold durations and thresholds such as `aδa_thr = 1 m`, `aδa_min = 3 m`, `aδa_max = 100 m`, and a nominal drifting period of `5 orbits`.

### 3. 逐句溯源

1. 句子 1：The autonomous-rendezvous guidance software is organized as a layered HSM whose two main states are `Walking Safe Ellipse (WSE)` and `Stationary Safe Ellipse (SSE)`, selected according to the estimated relative drift between the chaser and the target.
   对应摘录：A, B
2. 句子 2：Above the control layer, a `Timeline Manager` truth table checks whether the spacecraft is inside or outside the next hold point and a `WSE/SSE` status layer classifies the current relative orbit so that the proper maneuver family can be selected.
   对应摘录：B
3. 句子 3：Inside the control layer, both `WSE` and `SSE` expand into subordinate modes such as `stand-by`, `safe sizing`, `station keeping`, `shape control`, and `compute drift`, and maneuver completion returns the machine to waiting states.
   对应摘录：B
4. 句子 4：The machine therefore does not just switch geometry modes; it also schedules when to move or stop, computes the drift needed to hit the next hold point, and re-invokes drift computation if the target SSE slot has not been reached within the prescribed TTL window.
   对应摘录：B
5. 句子 5：The timing side is explicit: the guidance uses hold durations and thresholds such as `aδa_thr = 1 m`, `aδa_min = 3 m`, `aδa_max = 100 m`, and a nominal drifting period of `5 orbits`.
   对应摘录：C
