# Odin: Team VictorTango's Entry in the DARPA Urban Challenge - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Odin` 的 driving behaviors 写成按 `normal road / intersection / parking lot` 情境切换的层次 FSM，并把 road、intersection、parking 内部的 driver 组合与 replan/parking handoff 交代得很具体。

## 条目 1: Winner-Takes-All Driving Behaviors with Parking and Replan Interrupts

- 控制对象：汽车与道路车辆领域的城市自动驾驶分层 driving behaviors 控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `Odin` 在 Urban Challenge 中的行为层控制器，用层次 FSM 先判断处于普通道路、交叉口还是停车区，再在对应上下文里选择 Route、Passing、Blockage、Precedence、Merge、Left Turn 或 Zone/Parking 等下级行为。
- 判断：算。对象是实际自动驾驶车辆的行为决策控制层，原文明确说明分层 FSM、Winner-Takes-All 选择机制、不同 driving context 下的 driver 组合，以及 parking/replan handoff 的具体逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，Section 2.1 `System Architecture and Communications`
> Urban Challenge vehicles must maintain knowledge of intent, precedence, and timing. ... VictorTango’s software structure employs a novel Hybrid Deliberative-Reactive paradigm. ... the scope of a behavioral control component can be moved from low-level reflexes to higher-level decision making for solving complex, temporal problems.

#### 摘录 B

- 出处：第 16-17 页，Section 2.3.2 `Driving Behaviors`
> To address the situational awareness problem, a system of hierarchical finite state machines is used. Such a system allows Driving Behaviors to distinguish between intersection, parking lot, and normal road scenarios. ... A finite state machine is used to classify the situation, and each individual behavior can be viewed as a lower-level, nested state machine. ... a modified Winner-Takes-All approach because all behavior outputs are broken down into one of several categories.

#### 摘录 C

- 出处：第 17 页，Section `Passing and Blocked Roads`
> Odin runs three behaviors, the Route Driver, the Passing Driver, and the Blockage Driver. ... The Passing Driver is concerned with getting around slow moving or disabled vehicles. ... If all RNDF defined lanes are removed from the list and at least one of these lanes is an oncoming lane, then the Blockage Driver commands a dynamic replan. ... all behaviors are reset while a new route is generated.

#### 摘录 D

- 出处：第 18 页，Section `Intersections`
> To handle intersections, Odin uses three drivers (Precedence, Merge, and Left Turn) in the Approaching Stop, Stop, Approaching Exit, and Exit situations. ... The Precedence Driver activates when Odin stops at junctions with more than one stop sign. ... The Merge Driver activates at intersections where Odin must enter or cross lanes of moving traffic ... The Left Turn Driver activates when Odin’s desired lane branch ... crosses over oncoming traffic lanes.

#### 摘录 E

- 出处：第 18-19 页，Section `Parking Lot Navigation`
> In the route building stage of Driving Behaviors, Odin performs a guided Dijkstra search to select control points for navigating toward the parking spot and reversing out of the spot. ... If the path is blocked, the Zone Driver can disconnect a segment of the graph and choose a different set of control points. The parking maneuver is signaled to Motion Planning by enabling the stop flag and providing a desired heading on the parking checkpoint. To reverse out of the spot, the direction is constrained to be only in reverse, and a target point is placed in order to position Odin for the next parking spot or zone exit.

### 2. 基于原文整理后的自然语言描述

The `Odin` driving-behavior controller is organized as a hierarchical finite-state system that first classifies the current situation into normal-road, intersection, or parking-lot contexts and then activates lower-level behaviors appropriate to that context. Its action selection is implemented as a modified Winner-Takes-All mechanism, so the behavior integrator chooses one active winner for each driver category rather than blending incompatible commands. On normal roads, the nested behavior set is `Route Driver + Passing Driver + Blockage Driver`, where passing handles slow or disabled vehicles and blockage can remove lanes and trigger a dynamic replan that resets all behaviors. At intersections, separate `Precedence`, `Merge`, and `Left Turn` drivers take over in approach, stop, exit, and crossing situations so the vehicle can wait for its turn, monitor moving traffic, and safely handle left-turn conflicts. In parking zones, the controller switches to a graph-guided mode that uses Dijkstra-selected control points, lets the zone driver reroute around blocked segments, signals parking by stop flag plus desired heading, and constrains the backing-out maneuver to reverse-only repositioning toward the next spot or exit.

### 3. 逐句溯源

1. 句子 1：The `Odin` driving-behavior controller is organized as a hierarchical finite-state system that first classifies the current situation into normal-road, intersection, or parking-lot contexts and then activates lower-level behaviors appropriate to that context.
   对应摘录：A, B
2. 句子 2：Its action selection is implemented as a modified Winner-Takes-All mechanism, so the behavior integrator chooses one active winner for each driver category rather than blending incompatible commands.
   对应摘录：B
3. 句子 3：On normal roads, the nested behavior set is `Route Driver + Passing Driver + Blockage Driver`, where passing handles slow or disabled vehicles and blockage can remove lanes and trigger a dynamic replan that resets all behaviors.
   对应摘录：C
4. 句子 4：At intersections, separate `Precedence`, `Merge`, and `Left Turn` drivers take over in approach, stop, exit, and crossing situations so the vehicle can wait for its turn, monitor moving traffic, and safely handle left-turn conflicts.
   对应摘录：D
5. 句子 5：In parking zones, the controller switches to a graph-guided mode that uses Dijkstra-selected control points, lets the zone driver reroute around blocked segments, signals parking by stop flag plus desired heading, and constrains the backing-out maneuver to reverse-only repositioning toward the next spot or exit.
   对应摘录：E
