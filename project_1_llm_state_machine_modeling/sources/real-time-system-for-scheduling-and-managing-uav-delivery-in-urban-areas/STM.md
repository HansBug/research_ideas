# A Real-Time System for Scheduling and Managing UAV Delivery in Urban Areas - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：并行、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把 UAV 与 AGV 的协同配送流程写成两个并行 FSM，并补了主控节点、命令接口和完整往返配送周期，适合作为飞行执行管理双 A 样本。

## 条目 1: UAV-AGV Delivery Cycle Coordination

- 控制对象：航空与无人机配送领域的 UAV-AGV 协同执行管理器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：并行、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向城市 UAV 配送机场的执行管理器，用并行的 UAV FSM、AGV FSM 和主控节点来组织装载、转运、起飞、投递、返航和回收。
- 判断：算。对象是实际 UAV 配送系统中的执行控制层，原文明确给出 UAV 与 AGV 的状态集合、命令集合、条件检查以及完整配送周期，不是泛化的调度综述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`Management Nodes`，`paper_content.txt` 第 196-221 行
> AGV Management Node: All AGVs are managed through a combination of multithreading and finite state machines (FSMs). Each AGV is controlled by an independent FSM thread that updates its state at a fixed frequency ... UA V Management Node: Similarly, the UA V management node adopts multithreading and FSMs ... Master Management Node: As the core of the system, the master node connects the scheduling layer with the execution layer. It subscribes to AGV and UA V status updates, provides the aggregated information to the scheduler for decision-making, and distributes scheduling results to the corresponding management nodes for execution.

#### 摘录 B

- 出处：第 3 页，`UAV Finite state machine`，`paper_content.txt` 第 222-240 行
> The UA V operates through six states: Ready, where it remains idle at the airport awaiting loading; On Car, indicating it has been mounted on an AGV; Waiting Go, where it awaits the takeoff command after loading cargo; Flying Go, when it is en route to the unloading station; Waiting Back, where it waits for the return command after unloading; and Flying Back, during which it flies back to the airport.
>
> The UA V responds to three main commands: Delivery, which triggers takeoff to the delivery point; Release Cargo, which initiates cargo unloading (only allowed when landed); and Load Cargo, which loads goods onto the UA V. State transitions rely on four condition checks: Landed ... On Car ... Get Cargo ... Retrieved ...

#### 摘录 C

- 出处：第 3-4 页，`AGV Finite state machine`，`paper_content.txt` 第 241-265 行
> The AGV is designed with four working states ... Waiting GoGW ... Waiting Pickup ... Waiting Working ... Waiting GoAW ...
>
> The AGV executes four main commands: UAV GetCargo ... UAV Receive ... UAV Retrieve ... and UAV Charge ...
>
> AGV state transitions depend on three condition checks: Have UAV ... InGW ... and InAW ...

#### 摘录 D

- 出处：第 4 页，`State Transition Process`，`paper_content.txt` 第 277-294 行
> Initially, the UA V is in the Ready state and the AGV in Waiting Pickup. The AGV moves to the GW area and, upon receiving the UAV Receive command, loads the UA V, transitioning the UA V to On Car and the AGV to Waiting Working. Next, both receive the cargo loading command. Once loading is complete, the UA V enters Waiting Go, and the AGV changes to Waiting GoAW. The AGV transports the UA V to the AW area, where it issues the Delivery command. The UA V takes off, flies to the unloading station, and upon arrival, receives the unload command and enters Waiting Back. The AGV then sends another Delivery command for the UA V to return. After landing back at the airport, the UA V re-enters On Car, and the AGV transitions to Waiting GoGW. It carries the UA V to the GW area for reloading, completing one delivery cycle.

### 2. 基于原文整理后的自然语言描述

The delivery execution layer is organized as two parallel FSMs coordinated by a master node: one FSM manages the UAV lifecycle and the other manages the AGV that shuttles the UAV between the ground-work and aviation-work areas. The UAV FSM uses six states—`Ready`, `On Car`, `Waiting Go`, `Flying Go`, `Waiting Back`, and `Flying Back`—and reacts to `Delivery`, `Release Cargo`, and `Load Cargo` commands under the guards `Landed`, `On Car`, `Get Cargo`, and `Retrieved`. In parallel, the AGV FSM uses `Waiting Pickup`, `Waiting Working`, `Waiting GoAW`, and `Waiting GoGW` together with transport and service commands such as `UAV Receive`, `UAV GetCargo`, `UAV Retrieve`, and `UAV Charge`, while the master node exchanges status updates and scheduling decisions with both machines. A complete cycle starts from `Ready + Waiting Pickup`, moves through loading and ground transfer to `Waiting Go + Waiting GoAW`, sends the UAV into outbound flight, switches to unloading and return, and finally brings the UAV back onto the AGV for reloading in the ground-work area. This gives a concrete airport-delivery execution controller with explicit command channels, synchronized vehicle states, and a fully traceable outbound-and-return loop.

### 3. 逐句溯源

1. 句子 1：The delivery execution layer is organized as two parallel FSMs coordinated by a master node: one FSM manages the UAV lifecycle and the other manages the AGV that shuttles the UAV between the ground-work and aviation-work areas.
   对应摘录：A, C
2. 句子 2：The UAV FSM uses six states—`Ready`, `On Car`, `Waiting Go`, `Flying Go`, `Waiting Back`, and `Flying Back`—and reacts to `Delivery`, `Release Cargo`, and `Load Cargo` commands under the guards `Landed`, `On Car`, `Get Cargo`, and `Retrieved`.
   对应摘录：B
3. 句子 3：In parallel, the AGV FSM uses `Waiting Pickup`, `Waiting Working`, `Waiting GoAW`, and `Waiting GoGW` together with transport and service commands such as `UAV Receive`, `UAV GetCargo`, `UAV Retrieve`, and `UAV Charge`, while the master node exchanges status updates and scheduling decisions with both machines.
   对应摘录：A, C
4. 句子 4：A complete cycle starts from `Ready + Waiting Pickup`, moves through loading and ground transfer to `Waiting Go + Waiting GoAW`, sends the UAV into outbound flight, switches to unloading and return, and finally brings the UAV back onto the AGV for reloading in the ground-work area.
   对应摘录：D
5. 句子 5：This gives a concrete airport-delivery execution controller with explicit command channels, synchronized vehicle states, and a fully traceable outbound-and-return loop.
   对应摘录：A, B, C, D
