# A Complete Framework for a Behavioral Planner with Automated Vehicles: A Car-Sharing Fleet Relocation Approach - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把车共享重定位 follower 的 `waiting / de-parking / joining / platoon-following / parking` 周期写成 FSM，并补了 leader-follower 的消息字段与触发条件。

## 条目 1: Parking-Joining-Following Relocation Cycle

- 控制对象：智慧停车与车共享重定位场景中的自动驾驶 follower 行为规划器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向车共享车队重定位的 follower 行为规划器，用离散 maneuver 状态组织出车、并入车队、跟驰、驶入新车位与循环等待。
- 判断：算。对象是实际自动驾驶车辆的行为控制器，原文明确给出 FSM 状态集合、状态转移条件以及 leader-follower 的消息交互内容。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，Section 2.1 Overview / Figure 2，行 175-206
> When the leader vehicle (in blue) approaches the parking spot of the AV (1), a signal is sent to the AV (in orange) to start the platoon merging process. For that purpose, the AV will perform a de-parking maneuver, followed by a merging maneuver. Once the AV has merged with the platoon, it operates in vehicle-following mode (2). The platoon will continue to pick up the different vehicles until the relocation parking spot defined by the global planner is approached (3). In this case, the AV (in orange) will perform a de-merging maneuver, followed by a parking maneuver.
>
> As the aforementioned functionality is well structured and the transition flags are clear, a Finite State Machine (FSM) is defined, in which each maneuver is defined using a state, as can be seen in Figure 2. There are five maneuvers a relocated vehicle can be in: platoon-following, parking, waiting, de-parking, and joining.
>
> The aforementioned state machine is designed to reproduce the cycle of AVs in car-sharing applications. To implement it, basic V2V communication was assumed to exist between the leader and the follower AVs. This way, the initial state of an AV is waiting in a parking spot (Figure 1 (1)), broadcasting a communication message containing its position, state, and ID. Once the leader approaches, it will receive the broadcast message and will communicate with the AV if joining is possible, determining a platoon position at the end of the platoon. Note that joining may not be possible if other vehicles are blocking the AV for the de-parking maneuvers.
>
> In order to join the platoon, the AV enters the de-parking state and will orient itself with the nearest lane. Depending on the relative position for the rest of the platoon, a joining process will be required (if the platoon is in another lane or the distance to the platoon is more than the desired platoon inter-vehicle distance), activating this state. Once the AV achieves to the desired distance to the last member of the platoon, the vehicle is considered merged, and the follower AV sends a message to the leader so that the platoon list can be updated. Then, the AV enters the following state. In this state, each AV calculates its control values, making use of the position and velocity of the preceding vehicle. When the desired parking spot is reached, the leader will signal the last vehicle on the platoon to park, by entering the parking state and jumping to the waiting state once finished to start the cycle again.

#### 摘录 B

- 出处：第 5 页，Section 2.1 Overview / messaging system，行 220-229
> The proposed basic messaging system is centralized by the leader, which is responsible for managing the platoon. Since, in this case scenario, the leader of the platoon is driven by a human driver, possible wrong decisions due to communication mistakes are not considered in this paper. Messages are sent broadcast with enough information for each follower to interpret. Each message contains the following information:
> • Vehicle state: This number represents if the follower is in the platoon or parked in a parking spot.
> • Platoon position: This is the relative position of the vehicle in the platoon.
> • Parking spot: If an AV follower is to be parked, the leader of the platoon sends the position of the parking spot to the assigned AV follower.

### 2. 基于原文整理后的自然语言描述

The follower behavioral planner is organized as a five-state FSM with `waiting`, `de-parking`, `joining`, `platoon-following`, and `parking`, and it reproduces the relocation cycle of a parked autonomous vehicle in a car-sharing fleet. A vehicle starts in `waiting` at its parking spot, broadcasts its position, state, and ID, and only leaves that state when an approaching leader contacts it and confirms that joining the platoon is possible. It then performs `de-parking`, aligns with the nearest lane, and enters `joining` whenever the platoon is in another lane or still farther away than the desired inter-vehicle spacing; once the desired distance to the last platoon vehicle is reached, the follower reports completion to the leader and transitions into `platoon-following`, where it uses the predecessor's position and velocity for control. When the leader designates a relocation parking spot, the follower receives that parking-spot assignment in the broadcast message, enters `parking`, and finally returns to `waiting` so that the relocation cycle can start again.

### 3. 逐句溯源

1. 句子 1：The follower behavioral planner is organized as a five-state FSM with `waiting`, `de-parking`, `joining`, `platoon-following`, and `parking`, and it reproduces the relocation cycle of a parked autonomous vehicle in a car-sharing fleet.
   对应摘录：A
2. 句子 2：A vehicle starts in `waiting` at its parking spot, broadcasts its position, state, and ID, and only leaves that state when an approaching leader contacts it and confirms that joining the platoon is possible.
   对应摘录：A
3. 句子 3：It then performs `de-parking`, aligns with the nearest lane, and enters `joining` whenever the platoon is in another lane or still farther away than the desired inter-vehicle spacing; once the desired distance to the last platoon vehicle is reached, the follower reports completion to the leader and transitions into `platoon-following`, where it uses the predecessor's position and velocity for control.
   对应摘录：A
4. 句子 4：When the leader designates a relocation parking spot, the follower receives that parking-spot assignment in the broadcast message, enters `parking`, and finally returns to `waiting` so that the relocation cycle can start again.
   对应摘录：A, B
