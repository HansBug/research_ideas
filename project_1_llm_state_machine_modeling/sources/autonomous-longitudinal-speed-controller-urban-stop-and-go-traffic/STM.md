# LONGITUDINAL VEHICLE SPEED CONTROLLER FOR AUTONOMOUS DRIVING IN URBAN STOP-AND-GO TRAFFIC SITUATIONS - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市 stop-and-go 跟驰与并入行为写成了 `Cruise / Approach / Follow / Emergency Brake / Hard Braking` 五态纵向监督控制器，并给出每个状态的阈值和控制器切换逻辑。

## 条目 1: Cruise-Approach-Follow-Hard-Braking longitudinal supervisor

- 控制对象：汽车与道路车辆控制领域的城市 stop-and-go 自主跟驰纵向监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是自动驾驶跟驰车辆的纵向 supervisory controller，用 `Longitudinal FSM` 管理 `Cruise`、接近、跟随和两级制动状态，并在 `Follow` 状态切换到底层 close-following 控制器。
- 判断：算。对象是真实道路车辆纵向控制链，原文明确给出状态集合、进入条件、距离阈值、速度设定与控制器接管关系，不是纯控制律性能分析。

### 1. 原文摘录

#### 摘录 A

- 出处：第 30-31 页，`Longitudinal FSM`，`paper_content.txt` 第 745-760 行
> For the implementation of the supervisory control, we have developed a longitudinal FSM which controls the desired speed of the vehicle in different states of a merging as well as a platooning maneuver.
>
> An FSM is the best way to deal with the above maneuvers as a follower vehicle goes through different distinct states before it gets locked into following the leader vehicle.
>
> A longitudinal FSM is used to control the desired speed of vehicles in a convoy in different stages of a vehicle following maneuver. The FSM switches from one state to the other using a rule base which is pre-defined.

#### 摘录 B

- 出处：第 34-39 页，`3.1 Cruise State / 3.2 Approach State / 3.3 Follow State / 3.4 Emergency Brake State / 3.5 Hard Braking State`，`paper_content.txt` 第 830-921 行
> This is the default state ... The cruise speed used is 25 mph if the vehicle is within the urban limits. The cruise speed is 45 mph if the vehicle is beyond the urban limits and on a highway.
>
> A vehicle enters this state only if it cites a leader within the approaching limits ... The approaching limit is set to 90 m ... In this state, the follower keeps its velocity slightly higher than the leader so that it can approach it smoothly.
>
> The follower vehicle enters this state when it is within the following distance ... chosen to be 8.5 m ... The follower will try and further reduce the gap ... till it reduces to a threshold value ... chosen to be 4 m.
>
> The follower vehicle enters this state if the following distance becomes too low ... 1.5 m ... If the following distance decreases below 0.5 m, then the Hard Braking State is entered ... We have taken `ΔV2 = 2 mph` for our simulations.

#### 摘录 C

- 出处：第 40 页，`Figure 20 FSM State Transition in a Approach and Follow Maneuver`，`paper_content.txt` 第 954-958 行
> the follower vehicle transitions from the Cruise state into the Approach state after the following distance is reduces below 90 m. Another State Transition occurs when the following distance reduces below 8.5 m from Approach state to Follow State. In the Follow state the following distance keeps reducing till it reaches the desired following distance of 4 m.

### 2. 基于原文整理后的自然语言描述

The supervisory controller organizes urban stop-and-go following as a five-state longitudinal FSM containing `Cruise`, `Approach`, `Follow`, `Emergency Brake`, and `Hard Braking`. `Cruise` assigns urban or highway reference speed and decides whether the vehicle is acting as a leader or follower, while `Approach` commands a slightly higher speed than the leader so the gap shrinks smoothly when the leader enters the sensing range. Once the leader is inside the `8.5 m` following band, the system switches to `Follow` and hands speed control to one of the close-following controllers until the gap reaches the desired `4 m` threshold. If spacing drops below `1.5 m`, the FSM enters `Emergency Brake`, and if it falls below `0.5 m` it escalates to `Hard Braking`; when the gap opens again the controller returns through `Approach` or back to `Cruise` depending on sensing range. Because each discrete state selects a different continuous velocity-control law but the transition logic itself is threshold-driven rather than timer-driven, the case is a `T0` longitudinal FSM with continuous coupling.

### 3. 逐句溯源

1. 句子 1：The supervisory controller organizes urban stop-and-go following as a five-state longitudinal FSM containing `Cruise`, `Approach`, `Follow`, `Emergency Brake`, and `Hard Braking`.
   对应摘录：A, B
2. 句子 2：`Cruise` assigns urban or highway reference speed and decides whether the vehicle is acting as a leader or follower, while `Approach` commands a slightly higher speed than the leader so the gap shrinks smoothly when the leader enters the sensing range.
   对应摘录：B
3. 句子 3：Once the leader is inside the `8.5 m` following band, the system switches to `Follow` and hands speed control to one of the close-following controllers until the gap reaches the desired `4 m` threshold.
   对应摘录：B, C
4. 句子 4：If spacing drops below `1.5 m`, the FSM enters `Emergency Brake`, and if it falls below `0.5 m` it escalates to `Hard Braking`; when the gap opens again the controller returns through `Approach` or back to `Cruise` depending on sensing range.
   对应摘录：B
5. 句子 5：Because each discrete state selects a different continuous velocity-control law but the transition logic itself is threshold-driven rather than timer-driven, the case is a `T0` longitudinal FSM with continuous coupling.
   对应摘录：A, B, C
