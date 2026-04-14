# A Bigraph-Based Digital Twin for Multi-UAV Landing Management - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅说明 AeroCtrl 采用 state-machine architecture，还把软件生命周期与 UAV 飞行生命周期做成正交耦合的双区域状态机，并给出可触发的状态迁移接口，足以作为 `HSM + T0` 双 A 样本。

## 条目 1: Orthogonally coupled AeroCtrl flight-service state machine

- 控制对象：航空航天与飞行/空管控制领域的多 UAV 着陆数字孪生中的 AeroCtrl 控制服务
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 multi-UAV landing digital twin 中的单机控制服务 AeroCtrl，它把 OSGi 软件生命周期与 UAV 运行生命周期并列建模，并通过 REST/ROS2 接口把抽象状态迁移落实到真实起飞、降落和导航动作。
- 判断：算。对象是实际 UAV controller service，不是单纯 bigraph 方法描述；原文明确写出状态机架构、双生命周期区域、正交耦合约束和可调用的状态迁移接口。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 48-59 行
> To address these limitations, this paper proposes a bigraph-based digital twin framework that unifies modeling, execution, and synchronization for the management of landing operations involving multiple UAVs. ... The model is linked to physical execution through modular APIs and a state-machine-based control service, enabling runtime cyber–physical synchronization. ... the framework is instantiated on the Crazyflie platform ...

#### 摘录 B

- 出处：第 11 页，`3.4.2. AeroCtrl`，`paper_content.txt` 第 459-471 行
> The AeroCtrl is a UAV controller implemented as a web service structured around a state-machine architecture. It defines and manages core UAV skills such as take-off, landing, and navigation between Cartesian coordinates while exposing all state transitions through web endpoints for external interaction. ...
>
> The system follows a standard OSGi software lifecycle (from installation to activation and eventual uninstallation) in parallel with a UAV operational lifecycle (idle, hovering, flying, landing). These two regions are orthogonally coupled: physical actions are permitted only when the software is active, and transitions between flight states are strictly ordered.

#### 摘录 C

- 出处：第 11-12 页，`3.5. Execution by Cyber–Physical Synchronization`，`paper_content.txt` 第 479-500 行
> In the design of the AeroCtrl service ... we assign each UAV a dedicated port and a separate web service instance. This allows HTTP requests to trigger state transitions in the UAV’s state machine—for example, POST requests can invoke activate_idle, begin_takeoff, or begin_landing—so that the UAV’s physical actions are immediately synchronized with its state machine ...
>
> ... allowing operators to observe the complete state machine, including the current state (e.g., Idle, Hovering, Flying, Landing) and its historical state transitions.

### 2. 基于原文整理后的自然语言描述

The retained controller is the AeroCtrl service used in the digital twin to execute individual UAV actions during multi-UAV landing management. It is not a flat flight-only automaton: the controller is organized as two orthogonally coupled regions, one for the OSGi software lifecycle and one for the UAV operational lifecycle, so the machine behaves as a hierarchical/parallel state machine rather than a single linear FSM. In the operational region, the UAV moves through states such as `Idle`, `Hovering`, `Flying`, and `Landing`, while the software region constrains whether these physical transitions are even legal, because flight actions are allowed only when the software is active. The paper also ties those transitions to concrete interfaces: REST endpoints such as `activate_idle`, `begin_takeoff`, and `begin_landing` trigger state changes, and the resulting actions are executed through ROS2 commands while the web monitor exposes both the current state and the transition history. As a result, the state machine is directly embedded into the cyber–physical execution chain, coupling verified landing rules with live UAV control and monitoring.

### 3. 逐句溯源

1. 句子 1：The retained controller is the AeroCtrl service used in the digital twin to execute individual UAV actions during multi-UAV landing management.
   对应摘录：A, B
2. 句子 2：It is not a flat flight-only automaton: the controller is organized as two orthogonally coupled regions, one for the OSGi software lifecycle and one for the UAV operational lifecycle, so the machine behaves as a hierarchical/parallel state machine rather than a single linear FSM.
   对应摘录：B
3. 句子 3：In the operational region, the UAV moves through states such as `Idle`, `Hovering`, `Flying`, and `Landing`, while the software region constrains whether these physical transitions are even legal, because flight actions are allowed only when the software is active.
   对应摘录：B, C
4. 句子 4：The paper also ties those transitions to concrete interfaces: REST endpoints such as `activate_idle`, `begin_takeoff`, and `begin_landing` trigger state changes, and the resulting actions are executed through ROS2 commands while the web monitor exposes both the current state and the transition history.
   对应摘录：C
5. 句子 5：As a result, the state machine is directly embedded into the cyber–physical execution chain, coupling verified landing rules with live UAV control and monitoring.
   对应摘录：A, B, C
