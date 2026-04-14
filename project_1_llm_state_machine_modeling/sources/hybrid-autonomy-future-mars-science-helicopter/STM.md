# Hybrid Autonomy Framework for a Future Mars Science Helicopter - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把火星科学直升机的 mission autonomy 明确组织成 mission-phase FSM，并给出每个 phase 绑定的 BT、Healthguard 事件触发和紧急着陆回退链，是一条完整的航空航天任务监督控制样本。

## 条目 1: Mission-Phase FSM-BT Supervisor for Mars Science Helicopter
- 控制对象：航空航天与飞行控制领域的火星科学直升机任务自治监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向未来火星科学直升机的高层 mission autonomy 控制器，用 mission-phase FSM 组织飞行阶段，并在各阶段内激活对应的行为树与故障响应。
- 判断：算。对象是论文主贡献里的真实飞行器自治监督器；原文明确给出状态集合、事件来源、状态类实现、Healthguard 触发以及进入 `EmergencyLand` 的回退链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Introduction / Contributions，行 104-145
> To address these challenges, this paper presents a hybrid autonomy framework for deep-space aerial exploration, integrating FSMs and BTs. The FSM provides structured, deterministic state transitions, while BTs enable modular, reactive task execution ... The framework operates on an event-driven behavior adaptation mechanism ... By continuously monitoring vehicle state, battery levels, and onboard anomalies, the system triggers adaptive mission reconfiguration or fail-safe actions as needed. ... A two-tier decision-making architecture, where the Autonomy module orchestrates mission execution, while the Healthguard continuously monitors system health and triggers adaptive responses.

#### 摘录 B
- 出处：第 4 页，Architecture description，行 317-359
> Each state represents a mission phase — Idle, Init, Takeoff, Mission, Land, Terminate or EmergencyLand — and is implemented as a separate class derived from an abstract base state class ... Transitions are triggered deterministically by predefined events ... External events such as BatteryLow or BatteryCritical are emitted by the Healthguard ... Each state defines explicit transitions for a subset of such events ... The FSM is validated offline to ensure that all states are reachable and that from each state, a path to a final state exists. ... Each state's logic is governed by its corresponding Behavior Tree, which the FSM activates based on the mission phase ... The FSM can execute, pause, abort, or reset BTs based on mission needs.

#### 摘录 C
- 出处：第 5 页，Figure `4` and related text，行 405-420
> Fig. 4. High-level FSM governing mission phases (top) and integrated BTs managing task execution within each phase (bottom). ... The FSM is shown in schematic form: green arrows represent transitions upon successful BT execution ... while red arrows capture transitions triggered by failure or system-level events such as safety violations or health events. ... Figure 4 illustrates the core FSM-BT control structure, showing the primary states: Idle, Init, PreChecks, Takeoff, Mission, Land, EmergencyLand, and Terminate. ... If one of these actions also fails, the behavior tree will return a Failure status, causing a transition to the EmergencyLand state.

### 2. 基于原文整理后的自然语言描述

The Mars science helicopter autonomy stack is organized as a mission-phase state machine whose phases include `Idle`, `Init`, `PreChecks`, `Takeoff`, `Mission`, `Land`, `EmergencyLand`, and `Terminate`. Each mission phase is implemented as its own state class, and transitions are fired deterministically by predefined internal or external events, including behavior-tree success or failure signals and `Healthguard` events such as `BatteryLow` and `BatteryCritical`. This makes the controller hierarchical: the top layer is the FSM, while each active phase owns a corresponding behavior tree that can be executed, paused, aborted, or reset by the state machine. The paper further states that the FSM is offline-validated for reachability and for the existence of a path from every state to a final state. Failure handling is explicit as well, because unsuccessful takeoff or landing procedures can propagate `Failure` back to the FSM and force a transition into `EmergencyLand`.

### 3. 逐句溯源

1. 句子 1：The Mars science helicopter autonomy stack is organized as a mission-phase state machine whose phases include `Idle`, `Init`, `PreChecks`, `Takeoff`, `Mission`, `Land`, `EmergencyLand`, and `Terminate`.
   对应摘录：B, C
2. 句子 2：Each mission phase is implemented as its own state class, and transitions are fired deterministically by predefined internal or external events, including behavior-tree success or failure signals and `Healthguard` events such as `BatteryLow` and `BatteryCritical`.
   对应摘录：A, B
3. 句子 3：This makes the controller hierarchical: the top layer is the FSM, while each active phase owns a corresponding behavior tree that can be executed, paused, aborted, or reset by the state machine.
   对应摘录：A, B
4. 句子 4：The paper further states that the FSM is offline-validated for reachability and for the existence of a path from every state to a final state.
   对应摘录：B
5. 句子 5：Failure handling is explicit as well, because unsuccessful takeoff or landing procedures can propagate `Failure` back to the FSM and force a transition into `EmergencyLand`.
   对应摘录：C
