# Autonomous vehicles for micro-mobility - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 motion planner 的 `Forward / Follow / StopSign / StopSignWait` 状态、速度目标更新、距离触发 guard 和 `3 seconds` 停牌等待都写得足够完整，可直接作为道路行为监督样本。

## 条目 1: OpenPlanner Forward-Follow-StopSign Motion Planner

- 控制对象：微型自动驾驶车辆的道路行为与速度规划监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是汽车与道路车辆控制领域的 motion-planning supervisor，用 `FSM` 在 `Forward`、`Follow`、`StopSign` 与 `StopSignWait` 等状态间切换，并结合速度、路段限速、制动距离和 stop line/obstacle 距离生成目标速度。
- 判断：算。对象是实际自动驾驶运动规划控制器，原文给出了状态名、状态内变量、转移触发和局部等待时间，不是只描述算法框架。

### 1. 原文摘录

#### 摘录 A

- 出处：第 8 页，`motion planner`，`paper_content.txt` 第 383-392 行
> Finally, in the motion planner module, traffic rules and obstacle avoidance strategies are enforced while the ego-vehicle uses the reference trajectory provided by the global planner to reach its destination; the Finite State Machine (FSM) associated with this process is shown in Fig.10(b).
>
> To enable robust navigation while enforcing speed limits, following other vehicles, and making planned stops, various modifications were performed to the Forward, Follow, and StopSign states.

#### 摘录 B

- 出处：第 8-9 页，`SpeedKeeping / Obstacles and Planned Stops`，`paper_content.txt` 第 397-407 行、第 459-497 行
> This state specifically considers the vehicle’s current speed, speed limits, and the DBW enable signal to generate a target speed. The target speed converges to the speed limit imposed by the road segment unless there is a maximum speed set for the entire mission.
>
> For both strategies, the decision-making process is initiated by identifying the distance to the waypoint of interest ... for vehicle following, wp corresponds to the waypoint closest to the rear of the object of interest ... and for planned stops, wp corresponds to the center of the stopline ... the same kinematics formulation can be applied.

#### 摘录 C

- 出处：第 9 页，`state transition triggers`，`paper_content.txt` 第 498-518 行
> one must first determine the state transition logic to be able to enter the Follow and StopSign states.
>
> By measuring initial speed, final speed, and distance traversed, an estimate for average acceleration can be identified: abrake. This constant can jointly be applied ... to approximate the distance required to reach vf given the ego-vehicle speed vego. This distance denotes dtrigger ... The state transition logic is then triggered when dtrigger > dtarget.
>
> specific to the StopSign state, once the vehicle performs a complete stop, the StopSignWait state is entered for three seconds ... before continuing.

### 2. 基于原文整理后的自然语言描述

The micro-mobility motion planner uses a finite-state supervisor in which `Forward` handles nominal progress under road speed limits, while `Follow` and `StopSign` are entered when another vehicle or a planned stop becomes relevant along the reference trajectory. Inside `Forward`, the controller computes a target speed from the vehicle's current speed, the segment speed limit, any mission-wide cap, and the drive-by-wire enable signal so that re-engagement does not create controller windup. For both `Follow` and `StopSign`, the planner estimates the trajectory distance `dtarget` to the obstacle rear point or stop line, computes a braking-based trigger distance `dtrigger`, and enters the corresponding state when `dtrigger > dtarget`. Once the vehicle has fully stopped at a stop sign, the supervisor enters `StopSignWait` for `three seconds` and only then releases the vehicle to continue.

### 3. 逐句溯源

1. 句子 1：The micro-mobility motion planner uses a finite-state supervisor in which `Forward` handles nominal progress under road speed limits, while `Follow` and `StopSign` are entered when another vehicle or a planned stop becomes relevant along the reference trajectory.
   对应摘录：A, B, C
2. 句子 2：Inside `Forward`, the controller computes a target speed from the vehicle's current speed, the segment speed limit, any mission-wide cap, and the drive-by-wire enable signal so that re-engagement does not create controller windup.
   对应摘录：B
3. 句子 3：For both `Follow` and `StopSign`, the planner estimates the trajectory distance `dtarget` to the obstacle rear point or stop line, computes a braking-based trigger distance `dtrigger`, and enters the corresponding state when `dtrigger > dtarget`.
   对应摘录：B, C
4. 句子 4：Once the vehicle has fully stopped at a stop sign, the supervisor enters `StopSignWait` for `three seconds` and only then releases the vehicle to continue.
   对应摘录：C
