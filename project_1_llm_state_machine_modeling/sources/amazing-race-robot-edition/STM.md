# The Amazing RaceTM: Robot Edition - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把室内寻人问路、方向执行与寻门确认明确组织成顶层五态监督器，并进一步补出 `WANDER` 与 `FOLLOW DIRECTIONS` 的内部子状态机，足以形成双 A 的服务机器人分层控制样本。

## 条目 1: Ask-for-Directions Hierarchical Navigation Supervisor

- 控制对象：通用机器人与移动服务机器人领域的室内寻人问路与寻门任务监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向未知办公楼环境的服务机器人高层任务控制器，负责按“找人问路、执行方向、找门确认”的顺序完成 room-finding 任务。
- 判断：算。对象是真实机器人系统的高层离散监督器，而不是仅有导航算法或对话模块；原文明确给出顶层五个行为状态，以及 `WANDER` 和 `FOLLOW DIRECTIONS` 的内部子状态机与恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Introduction，`paper_content.txt` 第 64-76 行
> Because the robot has no prior knowledge about the goal location nor the structure of the environment, it must seek a person for assistance. ... We present a novel finite-state-machine (FSM) system design that makes these logical steps to accomplish this task. Our hypothesis is that this problem requires a specific set of abilities that are invoked in a particular order, equivalent to an FSM.

#### 摘录 B

- 出处：第 2 页，Section `II.B Architecture`，`paper_content.txt` 第 163-190 行
> Our architecture is a finite-state machine illustrated in Figure 1. ... Given a goal description, the initial state is `WANDER` ... Once a person is found, the robot enters the `APPROACH PERSON` state ... it initiates a conversation with them in the `HOLD CONVERSATION` state. ... a transition to the `FOLLOW DIRECTIONS` state is made. ... The robot then enters the `NAVIGATE DOOR` state which involves detecting doors and driving up to them to inspect their door tags.

#### 摘录 C

- 出处：第 5-6 页，Section `III.A WANDER` / Figure `5a`，`paper_content.txt` 第 436-516 行
> `WANDER` is the initial state of the system ... `WANDER` has five substates: `MAKE DECISION`, `ROTATE RECOVERY`, `ROTATE`, `DRIVE FORWARD`, and `DRIVE THROUGH INTERSECTION`. ... Maintaining visitation times allows the robot to explore the environment in a thorough manner, preferring to visit areas in the map that it has not seen or that it has seen least recently. ... These substates can be modeled as a FSM as shown in Figure 5a.

#### 摘录 D

- 出处：第 11-12 页，Section `III.D FOLLOW DIRECTIONS` / Figure `5b`，`paper_content.txt` 第 1061-1111 行
> `FOLLOW DIRECTIONS` state has five substates: `MAKE DECISION`, `DRIVE FORWARD`, `ROTATE`, `DRIVE THROUGH INTERSECTION`, and `COMPLETE`. ... `FOLLOW DIRECTIONS` maintains a step counter ... When the goal action is `goal-F`, `goal-L`, or `goal-R`, the robot has reached the same hallway as the goal and must look for it. Thus the robot will transition to the `NAVIGATE DOOR` state. When the goal action is `person` ... the robot will transition to the `WANDER` state.

### 2. 基于原文整理后的自然语言描述

The room-finding robot is organized as a hierarchical navigation supervisor whose top-level states are `WANDER`, `APPROACH PERSON`, `HOLD CONVERSATION`, `FOLLOW DIRECTIONS`, and `NAVIGATE DOOR`. The machine first searches for an approachable person, then conducts spoken dialogue to obtain directions, and only after a complete instruction set is assembled does it hand control to the direction-execution layer. Inside `WANDER`, a nested FSM manages exploration with `MAKE DECISION`, `ROTATE RECOVERY`, `ROTATE`, `DRIVE FORWARD`, and `DRIVE THROUGH INTERSECTION`, and it uses hallway visitation times plus dead-end recovery turns to keep exploration thorough but not purely exhaustive. Inside `FOLLOW DIRECTIONS`, another nested FSM maintains a step counter and executes the plan through `MAKE DECISION`, `DRIVE FORWARD`, `ROTATE`, `DRIVE THROUGH INTERSECTION`, and `COMPLETE`, so each instruction is consumed in order rather than being flattened into one monolithic path follower. Once the goal action indicates that the robot has reached the correct hallway, the supervisor transitions to `NAVIGATE DOOR` to inspect door tags; if the plan only reaches another person waypoint, it falls back to `WANDER` and re-enters the ask-for-directions loop.

### 3. 逐句溯源

1. 句子 1：The room-finding robot is organized as a hierarchical navigation supervisor whose top-level states are `WANDER`, `APPROACH PERSON`, `HOLD CONVERSATION`, `FOLLOW DIRECTIONS`, and `NAVIGATE DOOR`.
   对应摘录：A, B
2. 句子 2：The machine first searches for an approachable person, then conducts spoken dialogue to obtain directions, and only after a complete instruction set is assembled does it hand control to the direction-execution layer.
   对应摘录：A, B
3. 句子 3：Inside `WANDER`, a nested FSM manages exploration with `MAKE DECISION`, `ROTATE RECOVERY`, `ROTATE`, `DRIVE FORWARD`, and `DRIVE THROUGH INTERSECTION`, and it uses hallway visitation times plus dead-end recovery turns to keep exploration thorough but not purely exhaustive.
   对应摘录：C
4. 句子 4：Inside `FOLLOW DIRECTIONS`, another nested FSM maintains a step counter and executes the plan through `MAKE DECISION`, `DRIVE FORWARD`, `ROTATE`, `DRIVE THROUGH INTERSECTION`, and `COMPLETE`, so each instruction is consumed in order rather than being flattened into one monolithic path follower.
   对应摘录：D
5. 句子 5：Once the goal action indicates that the robot has reached the correct hallway, the supervisor transitions to `NAVIGATE DOOR` to inspect door tags; if the plan only reaches another person waypoint, it falls back to `WANDER` and re-enters the ask-for-directions loop.
   对应摘录：B, D
