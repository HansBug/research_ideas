# Multi-robot cooperation for lunar In-Situ resource utilization - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 lunar ISRU 六车协作系统组织成 central task planner + per-rover FSM + nested excavator-arm FSM，并写明电量阈值、停车/倾倒消息交互和 excavation timeout，是非常强的复杂任务监督样本。

## 条目 1: Multi-rover mission supervisor with nested excavation FSM

- 控制对象：通用控制与机器人任务领域的月面 ISRU 多机器人协同任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 lunar volatile collection mission 的 multi-rover supervisor，外层用 per-rover FSM 管理 scout / excavator / hauler 行为，内层对 Excavator arm 再嵌套一套 manipulation FSM。
- 判断：算。对象是实际 lunar ISRU 机器人队伍的任务控制系统，而不是比赛叙事或任务流程图；原文给出了共有状态、专有状态、嵌套 arm FSM、任务间消息交互，以及电量与 timeout 触发的恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 12-13 页，Section `5` 与 Figure `6`，`paper_content.txt` 第 911-955、1003-1008 行
> The framework for the autonomous operation ... consisted of a central task planner and volatile map, and decentralized finite state machines (FSMs) to control individual robots.
>
> Most of the FSM states were common ... “Initialization”, “Planning”, “Traverse”, “Localization Recovery” and “Emergency Charging” ...
>
> The remaining FSM states were specific ... “Volatile Handling” ... “Excavation” ... “Parking” and “Dumping” ...
>
> ... For the Excavator, another FSM was nested to control the manipulator behavior.

#### 摘录 B

- 出处：第 12-15 页，Section `5.2-5.3`，`paper_content.txt` 第 1024-1034、1105-1134 行
> In the “Planning” state, the robot requested a waypoint from the task planner node ... transitioned to traverse. In the “Traverse” state, the rover drives from one waypoint to another ...
>
> ... If the rover was experiencing immobility issues, the recovery state was triggered ...
>
> ... Once the Excavator arrives at the excavation site, it activates the “Excavation” state ...
>
> The digging process ends once one of the following conditions applies: the volatile is fully captured, the volatile clods cannot be found anymore, a maximum number of scoops is reached (set to 12), or the entire process reaches a timeout (about 20 min in simulation time).

#### 摘录 C

- 出处：第 15 页，Section `5.3.4 Excavation state machine`，`paper_content.txt` 第 1174-1193 行
> ... it enabled a secondary state machine to actuate the arm ...
>
> Its states, namely, “HomeArm”, “Search”, “LowerArm”, “Scoop”, “ExtendArm”, and “Drop”, had predefined actions associated with them ...
>
> ... Once it finds the Hauler, it scoops material and checks if volatile is detected in the Excavator’s bucket. If there is, it proceeds to an “Extend” state ... and finally, to a “Drop” state ...

#### 摘录 D

- 出处：第 12、15-18 页，Section `5.2-5.4`，`paper_content.txt` 第 935-940、1200-1224、1245-1279、1324-1345 行
> The “Emergency Charging” state was activated immediately if the rover battery dropped under 30%.
>
> ... The excavation process begins when the Excavator identifies a suitable parking spot ... sends this information to the Hauler ... The Hauler then informs the Excavator ... Once the Hauler has reached the target side waypoint, it relays a message ...
>
> ... the Hauler activates its “Parking” state ...
>
> ... To avoid interference between two haulers wanting to dump its bin at the same time, we implemented a simple “semaphore” ...
>
> After dumping the contents, the Hauler proceeds to the charging station to refill its batteries and execute Homing ...

### 2. 基于原文整理后的自然语言描述

The lunar ISRU autonomy stack is organized as a hierarchical multi-rover supervisor built from a central task planner plus one FSM per rover. At the outer layer, all rover types share `Initialization`, `Planning`, `Traverse`, `Localization Recovery`, and `Emergency Charging`, where planning requests new goals, traverse executes navigation, recovery handles stuck or homing situations, and emergency charging is triggered as soon as the battery falls below `30%`. Each rover type then extends this common skeleton with mission-specific states: Scouts use `Volatile Handling`, Excavators use `Excavation`, and Haulers use `Parking` plus `Dumping`. Inside `Excavation`, the Excavator enables a second FSM for the arm, whose states `HomeArm`, `Search`, `LowerArm`, `Scoop`, `ExtendArm`, and `Drop` implement the repeated search-scoop-transfer cycle toward the Hauler bin. The cooperative mission is explicitly message-driven, because the Excavator selects the parking side, commands the Hauler approach, verifies the parked bin position, may request re-parking, and the Hauler later requests dumping permission through a semaphore. The excavation loop also has concrete termination guards, including complete capture, failed rediscovery, a maximum of `12` scoops, and an overall timeout of about `20 min`, so this is a full HSM-style mission supervisor rather than a loose rover workflow.

### 3. 逐句溯源

1. 句子 1：The lunar ISRU autonomy stack is organized as a hierarchical multi-rover supervisor built from a central task planner plus one FSM per rover.
   对应摘录：A
2. 句子 2：At the outer layer, all rover types share `Initialization`, `Planning`, `Traverse`, `Localization Recovery`, and `Emergency Charging`, where planning requests new goals, traverse executes navigation, recovery handles stuck or homing situations, and emergency charging is triggered as soon as the battery falls below `30%`.
   对应摘录：A, B, D
3. 句子 3：Each rover type then extends this common skeleton with mission-specific states: Scouts use `Volatile Handling`, Excavators use `Excavation`, and Haulers use `Parking` plus `Dumping`.
   对应摘录：A
4. 句子 4：Inside `Excavation`, the Excavator enables a second FSM for the arm, whose states `HomeArm`, `Search`, `LowerArm`, `Scoop`, `ExtendArm`, and `Drop` implement the repeated search-scoop-transfer cycle toward the Hauler bin.
   对应摘录：C
5. 句子 5：The cooperative mission is explicitly message-driven, because the Excavator selects the parking side, commands the Hauler approach, verifies the parked bin position, may request re-parking, and the Hauler later requests dumping permission through a semaphore.
   对应摘录：D
6. 句子 6：The excavation loop also has concrete termination guards, including complete capture, failed rediscovery, a maximum of `12` scoops, and an overall timeout of about `20 min`, so this is a full HSM-style mission supervisor rather than a loose rover workflow.
   对应摘录：B
