# Dynamic Modeling and Control of High-Speed Automated Vehicles for Lane Change Maneuver - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接说明 lane-change maneuver flow 可由 `FSM` 表示，并给出纵向 segment、横向 segment、lane-keeping segment、`tp = 8s` 和 `tlat = 3s` 等阶段与时间信息，可抽成高速换道阶段监督器。

## 条目 1: Segment-Based High-Speed Lane-Change Maneuver FSM

- 控制对象：汽车与道路车辆控制领域的高速自动驾驶换道阶段监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个高速自动驾驶换道 maneuver 的高层阶段 FSM，用纵向调整、横向进入目标车道和目标车道保持等状态管理 MPC 连续控制问题。
- 判断：算。虽然论文主体包含车辆动力学和 MPC，但原文明确给出 `finite state machine` 与换道阶段，并且阶段内还有固定预测时域和横向运动时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section 2.3
> To capture the lane change maneuver properties of adjusting the longitudinal position and velocity prior to initializing the lateral motion of the maneuver, a multi-segment lane change process model is proposed.
>
> In the first segment, termed as the longitudinal segment, the ego vehicle E adjusts its longitudinal distance, position or relative velocity ...
>
> In the second segment, termed as lateral segment, E starts the lateral motion and enters into the target lane.
>
> In the third segment, termed as lane-keeping segment, E adjusts its relative velocity and distance to the preceding vehicle while following the target lane.

#### 摘录 B

- 出处：第 5 页，Section 2.3
> A fixed prediction horizon for the lane change process is used, i.e. tp = 8s.
>
> A finite state machine (FSM), as shown in Fig. 5, can be applied to represent the lane change maneuver flow. There are five states in this FSM, each representing a stage of the lane change maneuver.
>
> The goal state of the FSM is lane-keeping segment in target lane. Lane-keeping segment in current lane is also deemed as a goal state for traffic situations in case the lane change maneuver is suspended.

#### 摘录 C

- 出处：第 5-6 页，Section 3.1
> Assuming the lateral motion of lane change maneuver is performed with a sinusoidal acceleration ... tlat can be conservatively deemed as 3 s.
>
> In terms of longitudinal trajectory planning, E must be able to traverse the previously defined three segments while maintaining safety margins to all relevant surrounding vehicles.

### 2. 基于原文整理后的自然语言描述

The lane-change controller uses a high-level FSM to supervise a continuous high-speed automated-vehicle maneuver. The flow begins in lane-keeping in the current lane and may either stay there if the lane change is suspended or proceed into a longitudinal segment. In the longitudinal segment, the ego vehicle adjusts distance, position, and relative speed to find a safe target-lane gap while staying within the current-lane safety corridor. The controller then enters the lateral segment, where the vehicle starts lateral motion, traverses into the target lane, and must satisfy safety bounds with respect to leading and following vehicles in both lanes. Once the lateral segment finishes, the FSM reaches lane-keeping in the target lane, where the vehicle adjusts relative velocity and distance to the preceding target-lane vehicle. The maneuver is not a timeless label sequence: the paper fixes `tp = 8s` for the prediction horizon and uses `tlat = 3s` as a conservative lateral-motion duration, while the MPC handles continuous dynamics inside each discrete stage.

### 3. 逐句溯源

1. 句子 1：The lane-change controller uses a high-level FSM to supervise a continuous high-speed automated-vehicle maneuver.
   对应摘录：B, C
2. 句子 2：The flow begins in lane-keeping in the current lane and may either stay there if the lane change is suspended or proceed into a longitudinal segment.
   对应摘录：B
3. 句子 3：In the longitudinal segment, the ego vehicle adjusts distance, position, and relative speed to find a safe target-lane gap while staying within the current-lane safety corridor.
   对应摘录：A, C
4. 句子 4：The controller then enters the lateral segment, where the vehicle starts lateral motion, traverses into the target lane, and must satisfy safety bounds with respect to leading and following vehicles in both lanes.
   对应摘录：A, C
5. 句子 5：Once the lateral segment finishes, the FSM reaches lane-keeping in the target lane, where the vehicle adjusts relative velocity and distance to the preceding target-lane vehicle.
   对应摘录：A, B
6. 句子 6：The maneuver is not a timeless label sequence: the paper fixes `tp = 8s` for the prediction horizon and uses `tlat = 3s` as a conservative lateral-motion duration, while the MPC handles continuous dynamics inside each discrete stage.
   对应摘录：B, C
