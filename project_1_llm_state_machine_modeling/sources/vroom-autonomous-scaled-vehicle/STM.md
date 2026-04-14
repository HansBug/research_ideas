# How to Win Bosch Future Mobility Challenge: Design and Implementation of the VROOM Autonomous Scaled Vehicle - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出以 `Lane Keeping` 为中心的高层 `FSM`，还把 `Parking`、`Overtake`、`Intersection` 等子流程展开，并补上了基于检测循环延迟的反应时间约束。

## 条目 1: Lane-Keeping-Centered Behavior Hierarchy

- 控制对象：汽车与道路车辆控制领域的缩比自动驾驶车高层行为监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是 `VROOM` 缩比无人车的软件决策层，用高层状态机管理 `Lane Keeping`、`Intersection`、`Roundabout`、`Parking`、`Overtake`、`Stop`、`Acceleration/Deceleration` 等行为，并把转向与速度控制连续地耦合到各个离散阶段。
- 判断：算。对象是实际无人车控制栈的高层监督器，原文同时给出顶层行为选择机、停车与超车子流程、基于传感器和检测延迟的 guard，以及与连续转向控制的连接关系，足以诚实判为 `HSM + T1`。

### 1. 原文摘录

#### 摘录 A

- 出处：第 14-15 页，`4.3 Logic Implementation`，`paper_content.txt` 第 727-775 行
> The selection of the vehicle’s actions based on the perception results, as previously mentioned, is governed by a Finite State Machine (FSM), which is depicted in Figure 7.
>
> Figure 7. Finite State Machine (FSM) governing the vehicle’s high-level behavior selection. The default state is Lane Keeping, from which the system transitions to task-specific states. After completing each maneuver, the system reverts to the Lane-Keeping state to maintain continuous, stable navigation.
>
> There, it is clear that all FSM states either begin or end in the Lane-Keeping state, as this is designated as the vehicle’s default state. Deviations from this state occur only when specific path flags (e.g., approaching intersections or roundabouts), environmental conditions, or obstacles are present.
>
> When multiple perception flags are simultaneously triggered, the system follows a predefined priority hierarchy to ensure that the most critical actions are performed first.
>
> • Priority 1—Pedestrians ...
> • Priority 2—Vehicles ...
> • Priority 3—Traffic Signs/Lights ...
> • Priority 4—Path Flags ...
>
> This hierarchical design ensures that the vehicle can effectively react to multiple environmental stimuli while maintaining a clear, structured decision-making process.

#### 摘录 B

- 出处：第 21 页，感知结果与反应判据，`paper_content.txt` 第 1012-1034 行
> Subsequently, the classification results guide the vehicle’s actions:
> • Traffic Sign: The vehicle adheres to traffic rules and responds accordingly ...
> • Traffic Light: The vehicle receives the state of the detected traffic light from the traffic lights server and acts accordingly.
> • Pedestrian: If a pedestrian is within the lane, the algorithm treats it as an obstacle, causing the vehicle to decelerate or stop ...
> • Vehicle: If the lane on the left is dotted and the vehicle’s speed exceeds that of the vehicle ahead, an overtaking maneuver is initiated. Otherwise, the vehicle follows without further action.
>
> The agent requires an object to be detected at least n times within m consecutive detection loops before initiating a reaction ... The detection process has a latency ranging between 50 ms and 100 ms ... the optimal values for n and m were determined to be 4 and 6, respectively. This means that the vehicle must detect the obstacle for at least 0.3 ± 0.1 s ... before reacting.

#### 摘录 C

- 出处：第 23-24 页，`4.4.6 Parking Navigation`，`paper_content.txt` 第 1085-1145 行
> The task of parking involves navigating a designated parking area ... The objective is to park in a free space and exit without any collisions.
>
> The parking spot detection process is initiated as soon as the vehicle identifies the parking spot sign. Upon detecting the sign, the car begins tracking its position via odometry ...
>
> By combining these detections, the system is able to determine which slots are occupied and which are free ...
>
> Once a free parking space is detected, the vehicle positions itself in an initial location ... The parking trajectory is computed using a Quintic Polynomial Planner ... After the initial parking maneuver, a single correction move is executed ...
>
> Figure 18. Flowchart of the Parking module, outlining the sequential decision-making and control steps used to identify a free parking spot, compute a trajectory, and execute the maneuver.

#### 摘录 D

- 出处：第 24-26 页，`4.4.7 Overtake Procedure`，`paper_content.txt` 第 1116-1204 行
> The Overtake process executes a loop that monitors if the distance to any object in the vehicle’s lane decreases ... If the object is not a pedestrian and there is a dotted line on the left, the Overtake maneuver is initiated. This maneuver consists of three phases: changing to the left lane, driving in that lane until the object is surpassed, and then returning to the right lane.
>
> The Change Lane maneuver itself has three distinct phases. To initiate a left lane change, a negative steering angle is applied ... In the first phase ... Once these angles surpass a threshold, the vehicle reaches the boundary between lanes ...
>
> During the second phase, the vehicle crosses the dotted line into the adjacent lane ... In the third phase, the vehicle nears the center of the new lane ... At this stage, control is handed back to the Lane-Keeping algorithm.
>
> While driving in the left lane, the rear camera is activated ... If the overtaken vehicle is detected at a safe distance behind, the final lane change back to the right is initiated ...
>
> Figure 20. Finite State Machine (FSM) representing the overtake procedure. The process monitors obstacles ahead and, when conditions allow, transitions through lane change, overtaking, and reintegration phases.

### 2. 基于原文整理后的自然语言描述

The `VROOM` scaled autonomous vehicle uses a hierarchical behavior supervisor whose top machine keeps `Lane Keeping` as the default state and dispatches the vehicle into task-specific modes such as `Intersection`, `Roundabout`, `Parking`, `Overtake`, `Stop`, `Acceleration`, and `Deceleration` whenever the relevant perception flags become active. This top layer is not a loose collection of modules: the paper explicitly states that all maneuvers begin or end in `Lane Keeping`, and that competing triggers are resolved through a fixed priority order in which pedestrians dominate vehicles, vehicles dominate signs and lights, and path flags are considered last. The same decision logic is also time-aware at engineering scale, because reactions are gated by repeated detections over `n = 4` hits within `m = 6` loops, with `50-100 ms` loop latency, so the vehicle only reacts after approximately `0.3 ± 0.1 s` of consistent evidence. Beneath the top state selector, the `Parking` module forms a nested sequential controller that initializes odometry tracking after the parking sign is seen, combines object and corner detection to determine whether a slot is free, computes a quintic parking trajectory, executes the maneuver, applies a correction move, and then exits the parking space. The `Overtake` branch is another nested submachine: it is enabled only when a slower obstacle is ahead and a dotted left lane is available, then passes through left-lane entry, left-lane traversal, and right-lane reintegration phases whose boundaries are determined by steering thresholds and lane-boundary recognition. Because the supervisor continuously hands steering authority between these discrete phases and the lane-keeping controller, the paper provides a high-confidence `HSM + T1` automotive sample with both layered task logic and continuous-motion coupling.

### 3. 逐句溯源

1. 句子 1：The `VROOM` scaled autonomous vehicle uses a hierarchical behavior supervisor whose top machine keeps `Lane Keeping` as the default state and dispatches the vehicle into task-specific modes such as `Intersection`, `Roundabout`, `Parking`, `Overtake`, `Stop`, `Acceleration`, and `Deceleration` whenever the relevant perception flags become active.
   对应摘录：A
2. 句子 2：This top layer is not a loose collection of modules: the paper explicitly states that all maneuvers begin or end in `Lane Keeping`, and that competing triggers are resolved through a fixed priority order in which pedestrians dominate vehicles, vehicles dominate signs and lights, and path flags are considered last.
   对应摘录：A
3. 句子 3：The same decision logic is also time-aware at engineering scale, because reactions are gated by repeated detections over `n = 4` hits within `m = 6` loops, with `50-100 ms` loop latency, so the vehicle only reacts after approximately `0.3 ± 0.1 s` of consistent evidence.
   对应摘录：B
4. 句子 4：Beneath the top state selector, the `Parking` module forms a nested sequential controller that initializes odometry tracking after the parking sign is seen, combines object and corner detection to determine whether a slot is free, computes a quintic parking trajectory, executes the maneuver, applies a correction move, and then exits the parking space.
   对应摘录：C
5. 句子 5：The `Overtake` branch is another nested submachine: it is enabled only when a slower obstacle is ahead and a dotted left lane is available, then passes through left-lane entry, left-lane traversal, and right-lane reintegration phases whose boundaries are determined by steering thresholds and lane-boundary recognition.
   对应摘录：B, D
6. 句子 6：Because the supervisor continuously hands steering authority between these discrete phases and the lane-keeping controller, the paper provides a high-confidence `HSM + T1` automotive sample with both layered task logic and continuous-motion coupling.
   对应摘录：A, D
