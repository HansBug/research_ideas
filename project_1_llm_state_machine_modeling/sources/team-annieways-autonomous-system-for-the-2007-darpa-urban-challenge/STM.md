# Team AnnieWAY's autonomous system for the 2007 DARPA Urban Challenge - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶行为决策层直接实现为 `Concurrent Hierarchical State Machine`，并详细展开了主状态族、恢复逻辑和路口处理分支，是高质量的道路车辆 HSM 样本。

## 条目 1: Concurrent Urban-Driving Behavior State Machine
- 控制对象：汽车与道路车辆领域的城市自动驾驶行为决策控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次, 并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `DARPA Urban Challenge` 参赛车辆 AnnieWAY 的高层行为规划器，用并发层次状态机在 `Drive / Intersection / Zone / Replan / GlobalRecover / Pause` 等行为之间切换。
- 判断：算。对象是实际自动驾驶车辆的行为决策器，原文不仅给出 CHSM 总体结构，还把路口进入、排队、停车、让行、恢复与重规划分支展开到可直接抽取的程度。

### 1. 原文摘录

#### 摘录 A
- 出处：第 15-16 页，`Maneuver Planning / Figure 10`（对应 `paper_content.txt` 第 463-524 行）
> The maneuver planner is implemented as a Concurrent Hierarchical State Machine (CHSM) with every state representing a driving behavior.
>
> Figure 10 shows the UML state chart of the machine's main level, with important sub-states annotated as well.
>
> ...DriveOnLane ...DriveStop ...DriveKTurn ...LaneChange ...DriveRecover ...IntersectionApproach ...IntersectionQueue ...IntersectionStop ...IntersectionWait ...IntersectionDriveInside ...ZoneApproach ...ZoneParking ...ZoneDriveToExit ...Replan ...GlobalRecover ...Pause

#### 摘录 B
- 出处：第 16 页，`Figure 10` 说明（对应 `paper_content.txt` 第 508-524 行）
> The state Drive comprises all regular driving maneuvers on normal roads. It has several sub-states that cover different situations like following the course of a lane (DriveOnLane), making a k-turn (DriveKTurn) or changing the lane (LaneChange). All behavior at intersections is handled by the Intersection state.
>
> The navigation in unstructured environments and parking maneuvers is controlled by the state Zone and its sub-states.
>
> In some situation it becomes necessary for the robot to replan its route, e.g when the road ahead is blocked. This is triggered by the state Replan ... If all situation dependent recovery handling fails, a global recovery state is invoked to navigate back on track.

#### 摘录 C
- 出处：第 20-21 页，`9.3 Integration into the state machine / Figure 14`（对应 `paper_content.txt` 第 637-695 行）
> When the vehicle approaches the intersection, the hierarchical state machine changes into the sub-state Intersection with the entry state IntersectionApproach. This state is active until the vehicle enters the intersection unless another traffic participant is perceived on the same lane between AnnieWAY and the intersection. In this case IntersectionQueue is activated until the other vehicle has passed the intersection and the lane is free.
>
> In IntersectionApproach ... the state transition splits up into (a) IntersectionStop if AnnieWAY is on a stop road, (b) IntersectionPrioDriveInside if AnnieWAY is on a priority road and no other vehicle has the right of way, (c) or IntersectionPrioStop if AnnieWAY is situated on a priority road, but needs to yield the right of way.
>
> In case (a) AnnieWAY stops at the stop line and changes into the state IntersectionWait ... the state machine changes to IntersectionDriveInside ... In case (c) in IntersectionPrioStop AnnieWAY stops before crossing the opposing lane, waits until the MTC confirms that no danger comes from priority vehicles anymore, and turns left.

### 2. 基于原文整理后的自然语言描述

The AnnieWAY maneuver planner is implemented as a `Concurrent Hierarchical State Machine (CHSM)` that sits below mission planning and selects concrete urban-driving behaviors from the current route and traffic situation. At the main level the planner organizes behavior into top-level states such as `Drive`, `Intersection`, `Zone`, `Replan`, `GlobalRecover`, and `Pause`, with specialized substates including `DriveOnLane`, `LaneChange`, `DriveKTurn`, `IntersectionApproach`, `IntersectionQueue`, `IntersectionStop`, `IntersectionWait`, `IntersectionDriveInside`, `ZoneParking`, and `ZoneDriveToExit`. When the vehicle approaches an intersection, the HSM enters `IntersectionApproach`; if another vehicle is queued ahead it switches to `IntersectionQueue`, otherwise it branches into `IntersectionStop`, `IntersectionPrioDriveInside`, or `IntersectionPrioStop` depending on road priority and right-of-way. From `IntersectionStop`, AnnieWAY stops at the stop line, waits in `IntersectionWait`, and advances to `IntersectionDriveInside` only after other waiting vehicles have cleared and the `Moving Traffic Check (MTC)` verifies safe merge conditions. More generally, blocked-road situations trigger `Replan`, lack of progress activates per-state recovery handling, and failed local recovery escalates to `GlobalRecover` to navigate the car back on track.

### 3. 逐句溯源

1. 句子 1：The AnnieWAY maneuver planner is implemented as a `Concurrent Hierarchical State Machine (CHSM)` that sits below mission planning and selects concrete urban-driving behaviors from the current route and traffic situation.
   对应摘录：A
2. 句子 2：At the main level the planner organizes behavior into top-level states such as `Drive`, `Intersection`, `Zone`, `Replan`, `GlobalRecover`, and `Pause`, with specialized substates including `DriveOnLane`, `LaneChange`, `DriveKTurn`, `IntersectionApproach`, `IntersectionQueue`, `IntersectionStop`, `IntersectionWait`, `IntersectionDriveInside`, `ZoneParking`, and `ZoneDriveToExit`.
   对应摘录：A, B
3. 句子 3：When the vehicle approaches an intersection, the HSM enters `IntersectionApproach`; if another vehicle is queued ahead it switches to `IntersectionQueue`, otherwise it branches into `IntersectionStop`, `IntersectionPrioDriveInside`, or `IntersectionPrioStop` depending on road priority and right-of-way.
   对应摘录：C
4. 句子 4：From `IntersectionStop`, AnnieWAY stops at the stop line, waits in `IntersectionWait`, and advances to `IntersectionDriveInside` only after other waiting vehicles have cleared and the `Moving Traffic Check (MTC)` verifies safe merge conditions.
   对应摘录：C
5. 句子 5：More generally, blocked-road situations trigger `Replan`, lack of progress activates per-state recovery handling, and failed local recovery escalates to `GlobalRecover` to navigate the car back on track.
   对应摘录：B
