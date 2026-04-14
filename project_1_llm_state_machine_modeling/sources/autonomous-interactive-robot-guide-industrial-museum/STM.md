# Development of an Autonomous and Interactive Robot Guide for Industrial Museum Environments Using IoT and AI Technologies - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把工业博物馆导览机器人控制器明确写成五态 `FSM`，并补齐了 `goal_status`、retry 阈值、dock/undock 服务和实地运行结果，适合直接作为通用服务机器人样本。

## 条目 1: Dock-Undock-Navigate Tour Orchestrator

- 控制对象：通用控制与服务机器人领域的工业博物馆导览机器人任务编排器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个运行在 `ROS 2 Orchestrator` 中的导览机器人任务控制器，用 `Idle / Undock / Navigate / Dock / Done` 五态串联导览开始、脱离充电座、执行导航、回站停靠和任务结束。
- 判断：算。对象是实际导览机器人控制子系统，不是仅有感知或对话模块的系统集成论文；原文完整列出了状态名、转移条件、失败回退、`goal_status` 反馈和实地导览结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 9 页，`Robot control`，`paper_content.txt` 第 327-349 行
> The robot control subsystem is organized around a finite state machine (FSM) as seen in Figure 6 implemented within the ROS 2 Orchestrator. This FSM defines the robot’s operational flow through five main states: Idle, Undock, Navigate, Dock, and Done.
>
> • Idle: Initial waiting state where the system decides the next action depending on whether the mission has just started, a navigation goal remains, or all goals have been completed.
> • Undock: Triggered at the beginning of a mission, this state commands the robot to disengage from the docking station using a service client. Upon success, the FSM transitions to navigation; on failure, it returns to the docking sequence.
> • Navigate: In this state, the robot publishes navigation goals through a dedicated ROS topic ... If the goal succeeds, the FSM resets retries and transitions back to Idle ... If it fails, the system retries navigation up to a maximum threshold before aborting the mission and returning to Dock.
> • Dock: Commands the robot to return to and connect with its docking station.
> • Done: Final state where the FSM halts execution ...

#### 摘录 B

- 出处：第 9-10 页，`Robot control / Orchestrator`，`paper_content.txt` 第 340-368 行
> During this state, the FSM invokes the ROS 2 go_to_pose routine, which incorporates dynamic obstacle avoidance by recalculating the path whenever new obstacles such as visitors entering the robot’s trajectory. This reactive behavior allows the robot to adapt to changing conditions in real time, maintaining both safety and mission continuity during autonomous tours.
>
> The Orchestrator acts as the core decision-making unit: it runs the FSM, manages retries, and coordinates ROS services and topics. It communicates asynchronously with docking and undocking services, navigation modules, and the MQTT communication layer, ensuring that high-level logic is directly linked to concrete robot actions. This design makes the system modular and fault-tolerant, since each transition explicitly manages success and failure cases, allowing the robot to react adaptively to operational conditions.

#### 摘录 C

- 出处：第 14, 17 页，初步实验与整体实现结果，`paper_content.txt` 第 487-490, 550-555 行
> Preliminary trials demonstrated successful undocking, trajectory execution, and docking sequences. Furthermore, the robot achieved consistent navigation performance in the presence of visitors and staff, confirming the feasibility of autonomous tours.
>
> Overall, the preliminary implementation successfully demonstrated core functionalities of the proposed system in a real museum environment. The robot achieved autonomous navigation along the predefined exhibition route, performing docking, undocking, and waypoint tracking with reliable performance under moderate visitor activity. Throughout the tests, the navigation system consistently executed its routes successfully, maintaining stable localization and obstacle avoidance.

### 2. 基于原文整理后的自然语言描述

The museum guide robot is controlled by a five-state mission orchestrator implemented as an explicit `FSM` inside the `ROS 2 Orchestrator`. At the top of the workflow, `Idle` decides whether a tour is starting, whether waypoints remain, or whether the mission is already complete; `Undock` then uses a docking service to release the robot from the station, and `Dock` performs the symmetric return-and-connect operation at the end of the route. The central `Navigate` state publishes goals over a ROS topic and waits for `/goal_status` feedback, resetting the retry counter on success and otherwise repeating navigation until a failure threshold is reached, at which point the mission aborts back to `Dock`. This means the state machine is not a plain flat tour script but an `EFSM` whose transitions depend on goal feedback, retry counts, and service outcomes. During navigation, the same state invokes `go_to_pose` with dynamic obstacle avoidance so that visitors entering the route trigger path recalculation instead of hard mission failure. The implementation results then confirm the full control loop by reporting successful undocking, waypoint execution, docking, localization, and obstacle avoidance in the real museum environment.

### 3. 逐句溯源

1. 句子 1：The museum guide robot is controlled by a five-state mission orchestrator implemented as an explicit `FSM` inside the `ROS 2 Orchestrator`.
   对应摘录：A
2. 句子 2：At the top of the workflow, `Idle` decides whether a tour is starting, whether waypoints remain, or whether the mission is already complete; `Undock` then uses a docking service to release the robot from the station, and `Dock` performs the symmetric return-and-connect operation at the end of the route.
   对应摘录：A
3. 句子 3：The central `Navigate` state publishes goals over a ROS topic and waits for `/goal_status` feedback, resetting the retry counter on success and otherwise repeating navigation until a failure threshold is reached, at which point the mission aborts back to `Dock`.
   对应摘录：A
4. 句子 4：This means the state machine is not a plain flat tour script but an `EFSM` whose transitions depend on goal feedback, retry counts, and service outcomes.
   对应摘录：A, B
5. 句子 5：During navigation, the same state invokes `go_to_pose` with dynamic obstacle avoidance so that visitors entering the route trigger path recalculation instead of hard mission failure.
   对应摘录：B
6. 句子 6：The implementation results then confirm the full control loop by reporting successful undocking, waypoint execution, docking, localization, and obstacle avoidance in the real museum environment.
   对应摘录：C
