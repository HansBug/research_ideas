# Decision-making System based on Finite State Machine for Low-speed Autonomous Vehicles in the Park - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把园区低速自动驾驶决策层明确写成七态 FSM，并给出了跟车、变道等待、局部规划与障碍距离阈值的切换规则，可直接作为车辆方向的 `FSM + T0` 双 A 样本。

## 条目 1: Seven-state park-driving decision supervisor

- 控制对象：汽车与道路车辆控制领域的园区低速自动驾驶决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向园区低速自动驾驶车辆的七态决策监督器，围绕状态估计、定速巡航、跟车、选道、局部规划、停车等待和车辆控制在静态障碍场景下组织变道与通行逻辑。
- 判断：算。对象是真实自动驾驶决策控制系统，不是单纯规划算法背景；原文直接列出了 `7` 个 FSM 状态、各状态职责、前车距离规则、对向来车等待规则以及 `Xob` 障碍距离阈值驱动的变道/等待分支。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 3-14 行
> In this paper, a decision-making model is devised based on finite state machine (FSM), a local path planner is designed based on Bézier curve and the lateral and longitudinal control method is realized on GAC Aion LX. This decision-making system for low speed automatic driving in the park is tested. Results demonstrate its accuracy and reliability.

#### 摘录 B

- 出处：第 2 页，`III. Decision-making system based on FSM`，`paper_content.txt` 第 108-129 行
> The FSM that is used to switch between different driving states is shown in Figure 2. There are 7 individual states in the FSM, which correspond to the following conditions.
>
> StateEstimator ... filters out the useless information.
> StopAndWait ... wait for pedestrians and other cars in the opposite lane passing when lane changing.
> DistanceKeeping ... determine the necessary safety gaps between two vehicles and adjust the speed of the autonomous vehicle accordingly.
> ConstantSpeed ... the autonomous vehicle goes at the default speed which is 3m/s.
> LaneChoosing ... determine the optimal lane to be in at any instant and evaluate whether it is feasible.
> LocalPlanner ... path planning based on Bézier curve is used in this state to merge into a lane proposed by lane choosing.
> VehicleController ... is used for path tracking.

#### 摘录 C

- 出处：第 2 页，`A. Distance Keeping` 与 `B. Lane Choosing`，`paper_content.txt` 第 131-156 行
> This behavior aims to make the actual distance not less than the desired distance between the autonomous vehicle and the vehicle in front. The following area is divided into Collision Avoidance Area and Vehicle Following Area according to actual d ... In Vehicle Following Area, the autonomous vehicle governs the speed according to the distance change in the past second ... In Collision Avoidance Area, vd = 0.
>
> In this paper, overtaking other cars on the road isn’t considered. Hence, Lane Changing is only considered when avoiding static obstacles. Firstly, consider whether there are incoming vehicles in the opposite lane when encountering obstacles. If there are incoming vehicles in the opposite lane, stop and wait until the vehicles pass. Secondly, return to the original lane if passable, for staying in the opposite lane may cause accident.

#### 摘录 D

- 出处：第 3 页，`C. Local Planner`，`paper_content.txt` 第 194-222 行
> Generally, the controller tracks the pre-defined path until coming across obstacles. This paper proposes a local planner to deal with lane changing in the park based on a fixed tracking path ... If Xob > 12, Local planner will ignore this object ... If 8 <= Xob <= 12, Local planner will plan path to change lane ... However, the behavior will turn to StopAndWait if Xob < 8, because the path won’t meet the vehicle dynamics constraints.

### 2. 基于原文整理后的自然语言描述

The retained controller is a park-driving decision supervisor that explicitly switches the autonomous vehicle among seven states: `StateEstimator`, `ConstantSpeed`, `DistanceKeeping`, `LaneChoosing`, `LocalPlanner`, `StopAndWait`, and `VehicleController`. The control loop first filters localization, lane, obstacle, and drivability information in `StateEstimator`, then keeps cruising at the default `3 m/s` in `ConstantSpeed` or regulates headway in `DistanceKeeping` when a front vehicle enters the following or collision-avoidance area. Obstacle handling is also stateful rather than descriptive: `LaneChoosing` only considers lane change for static obstacles, checks whether opposite-lane traffic is present, and sends the vehicle to `StopAndWait` until the opposite lane clears when necessary. Once a feasible bypass exists, `LocalPlanner` generates a Bézier lane-change path and `VehicleController` tracks it, with the obstacle longitudinal coordinate `Xob` acting as a concrete guard: obstacles farther than `12` meters are ignored, obstacles in the `8-12` meter band trigger lane-change planning, and obstacles closer than `8` meters force the machine back to `StopAndWait`. Taken together, the paper exposes a concrete automotive FSM whose guards are built from obstacle distance, traffic occupancy, and headway evolution, and whose actions are cruise, follow, wait, replan, and path tracking.

### 3. 逐句溯源

1. 句子 1：The retained controller is a park-driving decision supervisor that explicitly switches the autonomous vehicle among seven states: `StateEstimator`, `ConstantSpeed`, `DistanceKeeping`, `LaneChoosing`, `LocalPlanner`, `StopAndWait`, and `VehicleController`.
   对应摘录：B
2. 句子 2：The control loop first filters localization, lane, obstacle, and drivability information in `StateEstimator`, then keeps cruising at the default `3 m/s` in `ConstantSpeed` or regulates headway in `DistanceKeeping` when a front vehicle enters the following or collision-avoidance area.
   对应摘录：B, C
3. 句子 3：Obstacle handling is also stateful rather than descriptive: `LaneChoosing` only considers lane change for static obstacles, checks whether opposite-lane traffic is present, and sends the vehicle to `StopAndWait` until the opposite lane clears when necessary.
   对应摘录：B, C
4. 句子 4：Once a feasible bypass exists, `LocalPlanner` generates a Bézier lane-change path and `VehicleController` tracks it, with the obstacle longitudinal coordinate `Xob` acting as a concrete guard: obstacles farther than `12` meters are ignored, obstacles in the `8-12` meter band trigger lane-change planning, and obstacles closer than `8` meters force the machine back to `StopAndWait`.
   对应摘录：B, D
5. 句子 5：Taken together, the paper exposes a concrete automotive FSM whose guards are built from obstacle distance, traffic occupancy, and headway evolution, and whose actions are cruise, follow, wait, replan, and path tracking.
   对应摘录：A, B, C, D
