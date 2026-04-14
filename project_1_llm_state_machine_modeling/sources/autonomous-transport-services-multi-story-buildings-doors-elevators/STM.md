# On realizing autonomous transport services in multi story buildings with doors and elevators - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把楼宇运输机器人的 `Drive To Navpoint / Ride Elevator / Pass Door / Press Button` 行为层写成可复用层次控制链，并明确了门梯交互中的时间限制、礼让规则与重试恢复。

## 条目 1: Hierarchical Elevator-and-Door Transport Service

- 控制对象：多楼层建筑运输服务机器人在门禁与电梯场景中的高层行为控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个部署在养老院与办公楼中的移动服务机器人行为层控制器，用层次化行为链组织跨楼层导航、呼梯乘梯、按键操作、门状态识别、开门与穿门。
- 判断：算。对象是实际服务机器人控制系统，原文明确给出上层行为层与下层技能层的分工，以及 `Ride Elevator`、`Pass Door`、`Press Button` 等子行为的进入条件、执行动作、时间限制与失败重试链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，Section 3.1.3 Operating the elevator，行 287-359
> Based on the data in the maps, we implemented the fundamental Drive To Navpoint Behavior, which checks whether the destination is on the same floor and activates the Ride Elevator Behavior if necessary. First, the area in front of the elevator is analyzed for other people who might be waiting for a ride. They get precedence, and in this case the robot drives to a waiting position. Once the way is free, the robot places itself in front of the elevator door and activates the Press Button Behavior to call the elevator. When the door opens, the cabin is analyzed for people inside. If there are passengers in the elevator, the robot gives way and starts over with the call elevator procedure afterwards. In the case of an empty cabin, the robot enters the elevator as quickly as possible, which was a tough challenge as the door only stays open for 6 s. When the elevator stops at the target floor, the robot leaves the cabin. In case the elevator stops at another floor, the robot starts over with the dial target floor procedure. This repetition of dialing is also triggered, if the elevator does not move after a button has been pushed.

#### 摘录 B

- 出处：第 6-7 页，Section 3.1.4 Opening doors，行 406-475
> Opening and passing through doors is governed by the Pass Door Behavior, that initially approaches a coarse observation position, from where the door’s current state and exact position is analyzed. Depending on the observed opening state of the door, specialized subordinate behaviors (unlatch door, pull/push door, or simply pass through the open door) are activated, each of which is responsible for bringing the door to the next more open state (closed -> unlatched -> partly open -> fully open). Other external disturbances at the door, such as people opening the door from the other side, can be compensated by the supervising Pass Door Behavior. This triggers retry mechanisms for the individual strategies. A repetition is also triggered if the gripper slips off the handle while manipulating the door. If the door could not be opened after three retries or restarts of the behaviors, it is highly likely, that the robot is falsely localized or the door might be locked and required human intervention.

### 2. 基于原文整理后的自然语言描述

The transport-service robot is organized as a hierarchical behavior controller in which `Drive To Navpoint` activates `Ride Elevator` whenever the destination lies on another floor and activates `Pass Door` whenever the planned path intersects a closed door. In the elevator branch, the robot yields to waiting people, calls the elevator through `Press Button`, checks whether the cabin is empty, enters within the 6-second door-open window, selects the target floor, and redials if the elevator stops at the wrong floor or does not move after button pressing. In the door branch, the supervisor first estimates the door state and then invokes subordinate behaviors that advance the door through `closed -> unlatched -> partly open -> fully open`, while choosing unlatching, pulling, pushing, or direct passage according to the observed opening state. Disturbances such as people opening the door from the other side or gripper slips trigger retries and behavior restarts, and after three failed attempts the controller escalates to human intervention instead of looping indefinitely.

### 3. 逐句溯源

1. 句子 1：The transport-service robot is organized as a hierarchical behavior controller in which `Drive To Navpoint` activates `Ride Elevator` whenever the destination lies on another floor and activates `Pass Door` whenever the planned path intersects a closed door.
   对应摘录：A, B
2. 句子 2：In the elevator branch, the robot yields to waiting people, calls the elevator through `Press Button`, checks whether the cabin is empty, enters within the 6-second door-open window, selects the target floor, and redials if the elevator stops at the wrong floor or does not move after button pressing.
   对应摘录：A
3. 句子 3：In the door branch, the supervisor first estimates the door state and then invokes subordinate behaviors that advance the door through `closed -> unlatched -> partly open -> fully open`, while choosing unlatching, pulling, pushing, or direct passage according to the observed opening state.
   对应摘录：B
4. 句子 4：Disturbances such as people opening the door from the other side or gripper slips trigger retries and behavior restarts, and after three failed attempts the controller escalates to human intervention instead of looping indefinitely.
   对应摘录：B
