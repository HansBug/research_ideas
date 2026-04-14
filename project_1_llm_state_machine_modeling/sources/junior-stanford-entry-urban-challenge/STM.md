# Junior: The Stanford Entry in the Urban Challenge - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：原文把城市自动驾驶高层行为监督器写成包含正常驾驶与异常恢复分支的 13 状态 FSM，并明确说明 top level 与 lower driving levels 的层次关系，足以形成双 A 的 HSM 样本。

## 条目 1: Urban Driving State-and-Exception Supervisor
- 控制对象：汽车与道路车辆领域的城市自动驾驶高层行为监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 DARPA Urban Challenge 自动驾驶车辆 `Junior` 的顶层行为状态机，用命名驾驶状态和异常恢复状态协调路口、停车场、掉头、拥堵脱困与任务完成流程。
- 判断：算。对象是实际自动驾驶车辆的高层决策与行为监督器，原文不只给出状态图，还逐个解释各状态职责、异常状态触发条件以及 top level 与 lower driving levels 的层次关系。

### 1. 原文摘录

#### 摘录 A
- 出处：第 21-22 页，`Figure 21` 前后的状态总述，`paper_content.txt` 第 586-594 行
> Figure 21 shows the finite state machine (FSM) that is used to switch between different driving states, and that invokes
> exceptions to overcome stuckness. This FSM possesses 13 states (of which 11 are shown; 2 are omitted for clarity).
> LOCATE VEHICLE: This is the initial state of the vehicle. Before it can start driving, the robot estimates its initial position on
> the RNDF, and starts road driving or parking lot navigation, whichever is appropriate.
> FORWARD DRIVE: This state corresponds to forward driving, lane keeping and obstacle avoidance.

#### 摘录 B
- 出处：第 22-23 页，`Figure 21` 的状态解释，`paper_content.txt` 第 602-636 行
> STOPSIGNWAIT: This state is invoked when the robot waits at a stop sign to handle intersection precedence.
> CROSSINTERSECTION: Here the robot waits if it is safe to cross an intersection ... The state also handles driving until Junior has
> exited the intersection.
> UTURN DRIVE ... UTURN STOP ...
> CROSSDIVIDER: This state enables Junior to cross the yellow line ...
> PARKING NAVIGATE: Normal parking lot driving.
> TRAFFIC JAM: In this state, the robot uses the general-purpose hybrid A* planner to get around a road blockage.
> ESCAPE: This state is the same as TRAFFIC JAM, only more extreme.
> BADRNDF ... MISSION COMPLETE.

#### 摘录 C
- 出处：第 24 页，top-level / lower-level 关系说明，`paper_content.txt` 第 639-645 行
> For simplicity, Figure 21 omits ESCAPE and TRAFFIC JAM. Nearly all states have transitions to ESCAPE and TRAFFIC JAM.
> At the top level, the FSM transitions between the normal driving states, such as lane keeping and parking lot navigation.
> Transitions to lower driving levels (exceptions) are initiated by the stuckness detectors.
> Most of those transitions invoke a “wait period” before the corresponding exception behavior is invoked.
> The FSM returns to normal behavior after the successful execution of a robotic behavior.

#### 摘录 D
- 出处：第 24 页，异常恢复示例，`paper_content.txt` 第 647-650 行
> For a blocked lane, the vehicle considers crossing into the opposite lane. If the opposite lane is also blocked, a U-turn is initiated,
> the internal RNDF is modified accordingly, and dynamic programming is run to regenerate the RNDF value function.

### 2. 基于原文整理后的自然语言描述

Junior uses a top-level hierarchical behavior FSM to switch among ordinary urban-driving states and lower-level exception handlers instead of relying on one flat motion policy. The machine contains 13 states, including normal states such as `LOCATE VEHICLE`, `FORWARD DRIVE`, `STOPSIGNWAIT`, `CROSSINTERSECTION`, `PARKING NAVIGATE`, `UTURN DRIVE`, `UTURN STOP`, and `CROSSDIVIDER`, together with exception or terminal states such as `TRAFFIC JAM`, `ESCAPE`, `BADRNDF`, and `MISSION COMPLETE`. The vehicle begins in `LOCATE VEHICLE`, estimates its initial position on the RNDF, and then enters road driving or parking-lot navigation as appropriate. Nearly all normal states can transfer to `TRAFFIC JAM` or `ESCAPE`, where the controller invokes hybrid A* based recovery behavior to get around a blockage or extract the robot from a jam. The paper explicitly states that the top level transitions among normal driving states, while stuckness detectors trigger lower driving levels and the FSM returns to normal behavior after successful recovery.

### 3. 逐句溯源

1. 句子 1：Junior uses a top-level hierarchical behavior FSM to switch among ordinary urban-driving states and lower-level exception handlers instead of relying on one flat motion policy.
   对应摘录：A, C
2. 句子 2：The machine contains 13 states, including normal states such as `LOCATE VEHICLE`, `FORWARD DRIVE`, `STOPSIGNWAIT`, `CROSSINTERSECTION`, `PARKING NAVIGATE`, `UTURN DRIVE`, `UTURN STOP`, and `CROSSDIVIDER`, together with exception or terminal states such as `TRAFFIC JAM`, `ESCAPE`, `BADRNDF`, and `MISSION COMPLETE`.
   对应摘录：A, B
3. 句子 3：The vehicle begins in `LOCATE VEHICLE`, estimates its initial position on the RNDF, and then enters road driving or parking-lot navigation as appropriate.
   对应摘录：A
4. 句子 4：Nearly all normal states can transfer to `TRAFFIC JAM` or `ESCAPE`, where the controller invokes hybrid A* based recovery behavior to get around a blockage or extract the robot from a jam.
   对应摘录：B, C, D
5. 句子 5：The paper explicitly states that the top level transitions among normal driving states, while stuckness detectors trigger lower driving levels and the FSM returns to normal behavior after successful recovery.
   对应摘录：C
