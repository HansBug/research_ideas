# Waiter Robots Conveying Drinks - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把服务机器人送餐动作写成 `SMACH` 状态机，既有基于载荷的策略切换，也有 `Cruise / Throttle / Brake / terminal docking` 的局部时序约束，足以形成高质量 `HSM + T1` 样本。

## 备注

- 当前 `paper_content.txt` 第 8-10 页同时保留了正式稿与 peer-review 版的重复段落，但状态机、时序参数和控制语义一致；本次只引用可稳定对应正文含义的文本。

## 条目 1: Payload-Aware Motion-Strategy Supervisor

- 控制对象：通用控制与服务机器人领域的送饮料 waiter robot 运动策略监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个服务机器人运动控制器，用 `ROS SMACH` 在“空载返回、送固体食物、送液体饮料”三种策略之间切换，并通过 `Cruise/Throttle/Brake` 局部状态调整速度和靠近目标的精细对接动作。
- 判断：算。对象是实际 waiter robot 的运动监督器，原文给出了状态机实现文件、策略切换 hub、速度状态以及 `0.5 s / 1 ms / 1 s` 的工程级时序参数，不是抽象算法说明。

### 1. 原文摘录

#### 摘录 A

- 出处：第 8 页，`3. Designing the Waiter Robot Motion Behaviors`，`paper_content.txt` 第 433-457 行
> To compute at a lower rate, a loop counter is applied to model the time discretization using basic delays and counters. Assume transition time of 0.5 s to peak acceleration and publish command every 1 ms ... the time response of the transient velocity is benchmarked at 1 s.
>
> The utility of a waiter robot increases if it is able to move normally without load, transit to moving slowly and safely when carrying drinks or food ... Each of the three velocity profiles experimented with can be regarded as a type of behavior: step-velocity profile as moving with no tray, ramp-velocity profile with carrying food tray, and S-velocity profile with carrying food with drink trays.
>
> ... VelProSMACH_V2.py is the implementation of the state machines for the waiter robot.

#### 摘录 B

- 出处：第 8-9 页，`3.1 Motion Behavioral Strategies`，`paper_content.txt` 第 493-521 行
> The state machine is designed to link the “linguistic” outcomes to different states. These outcomes can be designed as event handlers to transit into discrete states under various circumstances.
>
> The “Dock” state is the interface to ROS navigation node and decisions are made here to nullify the move base commands and switch into other move commands as a motion strategy hub. It may transit to various states depending on the payload e.g., of the food or drinks. For one case, the robot would move with the S-velocity profile while carrying drinks to a table, then subsequently deliver the remaining food with a ramp velocity profile and then return to the start point with step velocity profile ...
>
> ... when the food is ready ... solid food to be using Strategy 2 while liquid and semi-liquid food to be on Strategy 3. When returning to a waiting position in the restaurant, the robot transits back into Strategy 1.
>
> The respective “Cruise” states enable the robot to switch its motion state by deciding whether to increase or decrease its speeds ... based on the current speed, the remaining distance to the goal or obstacles.

#### 摘录 C

- 出处：第 10-11 页，`3.2 Reactive and Non-Reactive States for a Multispeed Design`，`paper_content.txt` 第 549-576, 609-610 行
> The cruise state requires and generates low discretization of desired speed (i.e., 0.1, 0.2, and 0.3 m/s) and current speed system level ... With a twist command and the goal position, the robot will increase speed (throttle) toward a higher speed. Likewise, when the robot’s goal position or if an obstacle is near, the robot reduces speed (brake).
>
> The throttle and brake states in S-velocity are used to generate linear acceleration and linear deceleration ... The loop thresholds are also set to maintain the magnitude of the maximum acceleration, acceleration period, and outcome velocity. Note that the smooth throttle and smooth brake states will not be interrupted or transit into other states during the acceleration period ... The robot will only be reactive again after the completion of the S-velocity profile.
>
> When the robot approaches its goal point, the waiter robot transits into a terminal state where it uses small step-up and step-down velocities to reach the docking point as accurate as possible.

#### 摘录 D

- 出处：第 11 页，`Results`，`paper_content.txt` 第 621-626 行
> Tables 2 and 3 show the specific data for docking and performance in conveying water in cups for the two programs; MoveBase control and VelProSMACH_V2 respectively. The mean docking radius improved from 329.6 mm for the step-velocity to 233.8 mm for the S-velocity ... In addition, the S-velocity profile did not result in any liquid spillage, while the step-velocity resulted in spillage in all 20 runs.

### 2. 基于原文整理后的自然语言描述

The waiter robot controller is implemented as `VelProSMACH_V2.py`, a `ROS SMACH` state-machine design that treats `step`, `ramp`, and `S-velocity` motion profiles as three payload-dependent behaviors rather than as one undifferentiated speed controller. At the top of the hierarchy, the `Dock` state works as a motion-strategy hub: it suppresses normal `move_base` commands, inspects the current task or payload, sends liquid or semi-liquid orders into `Strategy 3`, sends solid-food orders into `Strategy 2`, and returns to `Strategy 1` when the robot is travelling back to the waiting position. Inside each strategy, the `Cruise` states form a lower-level decision layer that uses current speed, remaining distance, goal position, and nearby obstacles to decide whether the robot should keep speed, throttle up, or brake down. The paper makes this local behavior explicitly time-aware by setting a `0.5 s` transition to peak acceleration, publishing commands every `1 ms`, and benchmarking the transient response at about `1 s`. It further states that the smooth `throttle` and `brake` states in the `S-velocity` profile are non-reactive during the acceleration period, so they cannot be interrupted until the jerk-limited phase is completed. When the goal is finally approached, the controller enters a terminal docking state that uses smaller step-up and step-down velocities for precise alignment, and the reported experiments show that this state-machine-driven `S-velocity` mode improves docking accuracy and eliminates beverage spillage compared with plain step-velocity control.

### 3. 逐句溯源

1. 句子 1：The waiter robot controller is implemented as `VelProSMACH_V2.py`, a `ROS SMACH` state-machine design that treats `step`, `ramp`, and `S-velocity` motion profiles as three payload-dependent behaviors rather than as one undifferentiated speed controller.
   对应摘录：A
2. 句子 2：At the top of the hierarchy, the `Dock` state works as a motion-strategy hub: it suppresses normal `move_base` commands, inspects the current task or payload, sends liquid or semi-liquid orders into `Strategy 3`, sends solid-food orders into `Strategy 2`, and returns to `Strategy 1` when the robot is travelling back to the waiting position.
   对应摘录：B
3. 句子 3：Inside each strategy, the `Cruise` states form a lower-level decision layer that uses current speed, remaining distance, goal position, and nearby obstacles to decide whether the robot should keep speed, throttle up, or brake down.
   对应摘录：B, C
4. 句子 4：The paper makes this local behavior explicitly time-aware by setting a `0.5 s` transition to peak acceleration, publishing commands every `1 ms`, and benchmarking the transient response at about `1 s`.
   对应摘录：A
5. 句子 5：It further states that the smooth `throttle` and `brake` states in the `S-velocity` profile are non-reactive during the acceleration period, so they cannot be interrupted until the jerk-limited phase is completed.
   对应摘录：C
6. 句子 6：When the goal is finally approached, the controller enters a terminal docking state that uses smaller step-up and step-down velocities for precise alignment, and the reported experiments show that this state-machine-driven `S-velocity` mode improves docking accuracy and eliminates beverage spillage compared with plain step-velocity control.
   对应摘录：C, D
