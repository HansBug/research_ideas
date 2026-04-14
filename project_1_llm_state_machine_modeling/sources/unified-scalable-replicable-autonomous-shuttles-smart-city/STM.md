# A Unified, Scalable and Replicable Approach to Development, Implementation and HIL Evaluation of Autonomous Shuttles for Use in a Smart City - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次、显式时钟、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 unified autonomous shuttle 的高层驾驶监督器写成带子状态与 `after(...)` 定时转移的规则式 `FSM`，是很强的系统级 HSM 样本。

## 备注

- 当前 `paper.pdf` 为公开 `SmartShuttle` final report 中附带的 SAE `2019-01-0493` 论文页切分版，正文页码与内容完整保留，便于按单论文路径入账。

## 条目 1: Rule-Based Shuttle Driving FSM with Intersection / Light / Obstacle / E-stop

- 控制对象：汽车与道路车辆控制领域的统一架构 autonomous shuttle 规则式驾驶监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、显式时钟、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个统一 autonomous vehicle/shuttle 架构中的规则式驾驶监督器，用感知输入在自定位、路径跟随、跟车、路口、信号灯、障碍物和急停之间切换。
- 判断：算。对象是实际自治车辆高层监督控制器，原文明确给出状态集合、触发输入、子状态、定时等待和急停接管逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Introduction，`paper_content.txt` 第 63-71 行
> In this paper, the unified architecture is introduced for high speed passengers vehicle and low speed smart shuttle. To meet the requirement for supervisory controller, a rule-based decision making framework is proposed here for decision making. This decision making framework processes sensor information and actuator information to generate supervisory control commands for different scenarios that the vehicles will meet during autonomous driving.

#### 摘录 B

- 出处：第 2 页，`Unified Architecture and Library`，`paper_content.txt` 第 151-160 行
> Decision making part has blocks that use all the information available to the computers such as localization, perception to determine the autonomous driving state in a finite state machine implementation of decision making.

#### 摘录 C

- 出处：第 3-4 页，`Decision Making Framework`，`paper_content.txt` 第 222-230、267-324 行
> Figure 4 shows the diagram of our decision-making framework as a Finite State Machine (FSM).
> ...
> This FSM process has six driving states that will occur in urban driving and one emergency state.
> ...
> Intersection: The intersection state will be triggered ... If a stop sign is detected, the ego-vehicle will automatically wait for a few seconds and then do the crossing traffic check.
> ...
> When left turn is needed, we will wait for 2 seconds and do crossing traffic detection.
> ...
> Traffic light state ... Red light state is on when red light signal and yellow light signal is received. Then, the vehicle will stop and wait for several seconds then check the red light signal again. Green light state is triggered if green light signal is received.
> ...
> Obstacle ... In this paper, obstacle avoidance maneuver is doing the brake and stop
> ...
> Emergency stop ... if the emergency button is pushed or steering wheel, brake pedal or throttle pedal are touched by the human driver

#### 摘录 D

- 出处：第 5 页，State Flow chart，`paper_content.txt` 第 403-460 行
> Carfollow_Path_Following
> entry: drive = 2;
> Path_Following
> entry: drive = 1;
> ...
> intersection ... WAIT ... entry: drive = 0; check_cross = 1; ... after(3,sec)
> ...
> Traffic_light ... WAIT ... entry: drive = 0; ... [traffic_light_red == 1]
> ...
> Obs ... WAIT ... entry: drive = 0; check_obs = 1 ... after(3,sec)
> E_stop
> entry: drive = 0;

### 2. 基于原文整理后的自然语言描述

Within the unified autonomous-vehicle architecture, a rule-based supervisory state machine selects high-level driving modes from localization, perception, and actuator-related inputs such as desired path, traffic-light signals, road signs, lead-vehicle detection, and obstacles. The machine starts with self-localization and then spends most of its time in path following, which contains a nested car-follow mode that switches the drive command from ordinary path following to `drive = 2` whenever a vehicle appears in front. When an intersection or stop sign is detected, the controller enters an intersection state, waits a few seconds, checks cross traffic, and only returns to path following when the crossing lane is clear; a left turn similarly adds a `2 s` wait before the cross-traffic decision. When a traffic light is near, the supervisor enters a traffic-light state whose red-light branch stops the shuttle, waits, and re-checks the signal before releasing a green-light branch back to path following. Obstacle handling performs a brake-and-stop maneuver on a single-lane route, and an emergency-stop state can preempt every other state whenever the e-stop is pressed or the human driver touches the steering wheel, brake pedal, or throttle pedal, returning control to safe manual intervention.

### 3. 逐句溯源

1. 句子 1：Within the unified autonomous-vehicle architecture, a rule-based supervisory state machine selects high-level driving modes from localization, perception, and actuator-related inputs such as desired path, traffic-light signals, road signs, lead-vehicle detection, and obstacles.
   对应摘录：A, B, C
2. 句子 2：The machine starts with self-localization and then spends most of its time in path following, which contains a nested car-follow mode that switches the drive command from ordinary path following to `drive = 2` whenever a vehicle appears in front.
   对应摘录：C, D
3. 句子 3：When an intersection or stop sign is detected, the controller enters an intersection state, waits a few seconds, checks cross traffic, and only returns to path following when the crossing lane is clear; a left turn similarly adds a `2 s` wait before the cross-traffic decision.
   对应摘录：C, D
4. 句子 4：When a traffic light is near, the supervisor enters a traffic-light state whose red-light branch stops the shuttle, waits, and re-checks the signal before releasing a green-light branch back to path following.
   对应摘录：C, D
5. 句子 5：Obstacle handling performs a brake-and-stop maneuver on a single-lane route, and an emergency-stop state can preempt every other state whenever the e-stop is pressed or the human driver touches the steering wheel, brake pedal, or throttle pedal, returning control to safe manual intervention.
   对应摘录：C, D
