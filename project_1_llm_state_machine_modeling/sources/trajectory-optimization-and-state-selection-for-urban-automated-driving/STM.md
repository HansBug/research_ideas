# Trajectory optimization and state selection for urban automated driving - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶纵向行为模式明确分成 `track / stop / cruise / adjust`，并给出基于前车位置、速度、加速度与道路限速的模式选择流程，足以支撑双 A。

## 条目 1: Cruise-Adjust-Track-Stop Urban Driving Mode Selector
- 控制对象：城市场景自动驾驶车辆的轨迹规划模式选择器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是汽车与道路车辆领域的自动驾驶行为规划器，用离散模式来切换 `cruise / adjust / track / stop` 四类纵向行为，并与连续轨迹生成耦合。
- 判断：算。对象是实际自动驾驶系统中的低层行为模式选择器，不是单纯的轨迹优化公式；原文直接给出模式集合、选择流程、进入条件和典型场景下的状态切换链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-4 页，`2.1 Decision-making system / 3.4 Distance pattern generation / Figure 4`，`paper_content.txt` 第 48-49 行、第 101-103 行、第 129-133 行
> In our automated vehicle system, the decision-making system consists of multi-level of behavior planners ... a route navigation (high level), a driving permission planning according to traffic rules (middle level) and a trajectory planning (low level).
>
> The distance pattern has the role of velocity profile according to the surrounding objects. Distance keeping and velocity keeping behaviors are generated depending on the distance to the leading vehicle and so on. In [6], track mode, stop mode and cruise mode was proposed as primitive behavior patterns.
>
> Figure 4 indicates a flowchart of the mode selection. Leading vehicle is extracted for each offset pattern. Suitable mode candidates are extracted based on the position, velocity and acceleration for the ego-vehicle and the leading vehicle. Trajectories is generated according to each mode.

#### 摘录 B
- 出处：第 4-5 页，`3.4.1-3.4.4`，`paper_content.txt` 第 135-159 行、第 167-180 行
> The track mode generates distance keeping profile for the preceding vehicle ... keeps a vehicular gap Ddes(t1) between the ego-vehicle and the preceding vehicle while aligning the velocity and the acceleration.
>
> To park the vehicle at the stop line or the destination, the stop model generates a deceleration profile ...
>
> The cruise mode keeps the ego-velocity to the given velocity stgt ...
>
> When the preceding vehicle is at a long distance, the adjust mode gradually reduces the vehicular gap to Ddes(t1) ...

#### 摘录 C
- 出处：第 6 页，`4.2 Results / Figure 8`，`paper_content.txt` 第 254-257 行
> In the following scenario, the preceding vehicle starts to decelerate after 10 s and stops ... While the gap is increasing, the ego-vehicle drives the cruise mode to keep the target velocity. When the preceding vehicle starts decelerating, the ego-vehicle gradually reduces the gap using the adjust mode. The track mode then accurately controls the gap.
>
> On the other hand, the preceding vehicle parks by the side of the road in the overtaking scenario. ... the ego-vehicle smoothly controls the lateral offset and velocity during overtaking.

### 2. 基于原文整理后的自然语言描述

The urban automated-driving planner is organized as a multi-level controller in which the low-level trajectory planner selects discrete longitudinal behavior modes while generating continuous trajectories in the Frenet frame. Its mode set includes `track`, `stop`, `cruise`, and the newly introduced `adjust` mode, and the selection flow first extracts a leading vehicle for each offset pattern and then filters suitable mode candidates using the ego vehicle's and leader's position, velocity, and acceleration. `Track` is the distance-keeping mode that maintains the desired inter-vehicle gap while aligning velocity and acceleration, `stop` decelerates to a stop line or destination, and `cruise` keeps the road target speed when there is no close preceding vehicle. `Adjust` is inserted between velocity keeping and distance keeping so that a long vehicular gap can be reduced smoothly before the controller hands over to `track`. In the reported following scenario, the controller transitions from `cruise` to `adjust` and then to `track` as the leader slows down, while in the overtaking scenario it coordinates lateral offset and longitudinal velocity according to the selected maneuver.

### 3. 逐句溯源

1. 句子 1：The urban automated-driving planner is organized as a multi-level controller in which the low-level trajectory planner selects discrete longitudinal behavior modes while generating continuous trajectories in the Frenet frame.
   对应摘录：A
2. 句子 2：Its mode set includes `track`, `stop`, `cruise`, and the newly introduced `adjust` mode, and the selection flow first extracts a leading vehicle for each offset pattern and then filters suitable mode candidates using the ego vehicle's and leader's position, velocity, and acceleration.
   对应摘录：A, B
3. 句子 3：`Track` is the distance-keeping mode that maintains the desired inter-vehicle gap while aligning velocity and acceleration, `stop` decelerates to a stop line or destination, and `cruise` keeps the road target speed when there is no close preceding vehicle.
   对应摘录：B
4. 句子 4：`Adjust` is inserted between velocity keeping and distance keeping so that a long vehicular gap can be reduced smoothly before the controller hands over to `track`.
   对应摘录：B
5. 句子 5：In the reported following scenario, the controller transitions from `cruise` to `adjust` and then to `track` as the leader slows down, while in the overtaking scenario it coordinates lateral offset and longitudinal velocity according to the selected maneuver.
   对应摘录：C
