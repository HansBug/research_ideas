# Hybrid State System Development for Autonomous Vehicle Control in Urban Scenarios - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶控制器写成 `HC` 离散状态机与 `LC` 连续控制器耦合的 `HSS`，还把 `Road` 元状态的能力演化拆成一串可追溯 `FSM` graft，能稳定形成 `HSM + T0 + 连续耦合` 样本。

## 条目 1: Urban-road meta-state and obstacle-passing supervisor

- 控制对象：汽车与道路车辆控制领域的城市自动驾驶 `HSS` 高层元状态与道路障碍绕行监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是 `OSU-ACT` 城市场景自动驾驶车的高层 `HSS` 控制器，用元状态管理 `Road / Intersection / U-Turn / Parking Zone` 等环境，并在 `Road` 子机内部处理 waypoint 跟踪、阻塞车辆等待、借道绕行和车道分隔规则切换。
- 判断：算。对象是实际自动驾驶车辆的高层决策控制器，原文明确区分离散 `HC` 与连续 `LC`，并用层次 `FSM` 组织元状态及其内部 `Road` 子机；虽然与现有 urban-challenge 条目邻近，但该样本更强调 `HSS` 耦合与 capability grafting，而不是重复已有 mission supervisor 文本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / `2.1 The HSS layout`，`paper_content.txt` 第 15-20, 83-94 行
> This paper analyzes a hybrid-state-system-based controller for an autonomous vehicle in urban traffic ...
>
> The Ohio-State University Autonomous City Transport utilizes a discrete-state system, based on a finite state machine for high-level decision making and a continuous-state controller for low-level lateral and longitudinal control.
>
> The controller for OSU-ACT is layered into a Low-level Controller (LC), and a High-level Controller (HC) ... The HC is responsible for the conscious-level decisions such as lane changes, obeying the speed limits and handling intersections, while the LC handles the subconscious control of steering to stay in the lane and throttle/brake control to maintain the speed.

#### 摘录 B

- 出处：第 3 页，对 high-level meta-state 的说明，`paper_content.txt` 第 182-194 行
> Since the most basic classification of the high-level controller capabilities is dependent on the structure of the environment, a number of meta-states are defined to cover these basic situations.
>
> Depending on the position of the vehicle and the mission, the high-level controller is in one of these meta-states, the list of which includes the following:
> Mission Start
> Mission End
> Road
> Intersection
> U-Turn
> Parking Zone
>
> This overall list of meta-states are connected in a FSM, while each meta-state is a FSM in itself.

#### 摘录 C

- 出处：第 4-5 页，`Road` meta-state development stages I-II，`paper_content.txt` 第 239-274 行
> A series of snapshots from the development of an example controller for the “road” meta-state, which is an FSM in itself, will be illustrated in this subsection.
>
> The first stage is the most basic capability associated with the road situation, the general waypoint following ...
>
> At this stage, a single waypoint following state, with connections into and out of this meta-state is sufficient ...
>
> The second stage involves adding the capabilities related to external stimuli. The case example here is a blocking obstacle on the followed path ... a generic stop-and-wait capability is required.
>
> This capability is grafted into the existing state machine by means of adding two new states and a new event ... The existing state trajectory of S1 -> S2 -> S3 is still available in the absence of an obstacle and the new trajectory S1 -> S2 -> S4 -> S5 -> S3 works in parallel to the existing system.

#### 摘录 D

- 出处：第 5-6 页，`Road` meta-state development stages III-IV，`paper_content.txt` 第 289-319, 334-345 行
> For the next stage, the world model is expanded to include a second lane ... Under the rule set of DUC, this situation requires a complete stop, followed a lane-change pass around obstacles, if the passing lane is free of obstacles.
>
> The new state, S6 forms an alternate trajectory, S1 -> S2 -> S4 -> S5 -> S6 -> S3 ...
>
> For the final stage ... Depending on the direction of travel on the passing lane, or equivalently the lane divider being broken or solid, the autonomous vehicle needs to perform either a complete stop and pass, or a non-stop lane change.
>
> The added capability is handled by the new graft, S7 ... S7 is inserted into an existing state trajectory passing from S2 to S4 ...
>
> The major difference between the two types of grafts is that the extension graft preserves existing state trajectories ... On the other hand, insertion grafts are placed in serial connection, severing existing state trajectories.

### 2. 基于原文整理后的自然语言描述

The OSU autonomous-vehicle controller is organized as a hybrid state system in which a discrete high-level controller supervises a continuous low-level steering and throttle/brake controller. At the top decision layer, the high-level machine switches among the environment-dependent meta-states `Mission Start`, `Mission End`, `Road`, `Intersection`, `U-Turn`, and `Parking Zone`, and each of these meta-states is itself a finite-state machine rather than a single opaque mode. The paper then exposes the internal design of the `Road` submachine as an evolving control graph: the core path is a waypoint-following trajectory, then a blocking-obstacle stop-and-wait branch is grafted in as an extension with the alternate path `S1 -> S2 -> S4 -> S5 -> S3`. When the world model is expanded to a second lane, a new state `S6` adds the complete-stop-then-pass capability, and the final `S7` insertion distinguishes whether the lane divider is solid or broken so that the vehicle chooses between `complete stop and pass` and `non-stop lane change`. Because the high-level FSM is explicitly coupled to a continuous low-level controller through the `Phi` and `Psi` interfaces, the paper is a layered HSM sample whose discrete phases remain tightly tied to continuous vehicle motion.

### 3. 逐句溯源

1. 句子 1：The OSU autonomous-vehicle controller is organized as a hybrid state system in which a discrete high-level controller supervises a continuous low-level steering and throttle/brake controller.
   对应摘录：A
2. 句子 2：At the top decision layer, the high-level machine switches among the environment-dependent meta-states `Mission Start`, `Mission End`, `Road`, `Intersection`, `U-Turn`, and `Parking Zone`, and each of these meta-states is itself a finite-state machine rather than a single opaque mode.
   对应摘录：B
3. 句子 3：The paper then exposes the internal design of the `Road` submachine as an evolving control graph: the core path is a waypoint-following trajectory, then a blocking-obstacle stop-and-wait branch is grafted in as an extension with the alternate path `S1 -> S2 -> S4 -> S5 -> S3`.
   对应摘录：C
4. 句子 4：When the world model is expanded to a second lane, a new state `S6` adds the complete-stop-then-pass capability, and the final `S7` insertion distinguishes whether the lane divider is solid or broken so that the vehicle chooses between `complete stop and pass` and `non-stop lane change`.
   对应摘录：D
5. 句子 5：Because the high-level FSM is explicitly coupled to a continuous low-level controller through the `Phi` and `Psi` interfaces, the paper is a layered HSM sample whose discrete phases remain tightly tied to continuous vehicle motion.
   对应摘录：A, D
