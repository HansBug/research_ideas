# Autonomous Control for Miniaturized Mobile Robots in Unknown Pipe Networks - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把管网巡检机器人的自主探索明确写成 `13` 状态有限状态机，并给出状态集合、全局探索规则、状态动作映射和两种闭环控制模式，足以形成双 A 的机器人监督控制样本。

## 条目 1: Joey Pipe-Network Exploration Supervisor
- 控制对象：通用控制与形式化工具领域的 Joey 微型管网巡检机器人自主探索控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向未知管网自主巡检的移动机器人高层探索控制器，用局部传感器状态驱动转向、直行、避障、死路回退和岔路选择。
- 判断：算。对象是真实机器人控制器而不是纯导航算法背景；原文直接把控制策略实现为有限状态机，给出了状态集合、探索规则、状态动作表和闭环控制职责。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，Section `3.1 Autonomous navigation strategy`
> To overcome the challenges described in section 2.3 and to ensure the execution of Task 1 described in section 2.2, we propose a computationally cheap, autonomous control strategy based on a finite state machine. By considering all possible events that a Joey may encounter within a sewer pipe network, we defined 13 robot states. We assume that the robot can confirm its current state using its sensor readings. Given its current state, the robot will call the corresponding high-level decision-making protocol to operate autonomously.
>
> These states include: Straight center and straight sided ... Sided ... Left corner and right corner ... Crash left and crash right ... Flip-risk ... Dead-end ... T junction, left branch, right branch ... Open space or manhole ... Cross.

#### 摘录 B
- 出处：第 6 页，Section `3.1 Autonomous navigation strategy`
> As stated in section 1, the control inputs do not involve any simultaneous localization and mapping (SLAM) or other video or acoustic input. Instead, range and odometry sensors must suffice to confirm the robot state, and knowledge of the current state ... must suffice to follow the pre-defined high-level directives. The strategy is to exhaustively cover the given pipe network and return safely to the starting point.
>
> there are two basic pre-defined directives for robot to operate:
> - Rule 1: At junctions, turn into the furthest right direction.
> - Rule 2: At dead-end, turn around to return to the previous junction.
>
> In straight pipes or at a left branch, the robot uses closed-loop speed control ... Other robot states require fine robot maneuver; thus, the robot uses closed-loop position control for the left and right wheel-leg control.

#### 摘录 C
- 出处：第 12 页，`TABLE 1 High level control actions following state estimation`
> State number State Action
> 3 Sided robot turns away from obstacles or pipe walls using fine step steering and closed-loop position control
> 4 Left corner robot turns left 90° while maintaining its center near the center of the junction
> 5 Crash left robot turns 30° backwards to previous turning direction, then re-evaluates its state and makes decision according to the new state
> 7 Cross robot turns 90° to the right while maintaining its center near the center of the junction
> 10 Right branch robot moves forwards a certain distance, turns right an angle of 45°, then, reassesses its state
> 11 Dead-end robot turns around by 180° and adjusts its position to the center of pipe while maintaining its pitch and roll angles low to avoid flip risk
> 12 Flip risk robot steps slowly backwards or forwards depending on its pitch and roll value to escape the flip risk
> 13 Open space robot approaches slowly, reassesses its state (and optionally, monitors conditions)

### 2. 基于原文整理后的自然语言描述

The Joey pipe-inspection controller is implemented as a finite-state exploration supervisor that uses only range, odometry, and orientation sensing to recognize `13` discrete robot states in an unknown pipe network. Its state set covers nominal travel states such as `Straight center` and `straight sided`, maneuvering and risk states such as `Sided`, `Crash left/right`, and `Flip-risk`, and topological states such as `Dead-end`, `T junction`, `left/right branch`, `Open space or manhole`, and `Cross`. Once the current state is confirmed, the robot follows two global exploration directives: at junctions it always turns into the furthest-right direction, and at a dead-end it turns around to return to the previous junction so the whole network can be exhaustively covered without SLAM. The state-action table then refines those directives into concrete maneuvers, for example turning `90°` at a left corner or cross, moving forward and then turning `45°` at a right branch, turning `180°` and re-centering at a dead-end, and backing or advancing slowly to escape a flip-risk state. Control execution is also mode-dependent: straight pipes and left-branch travel use closed-loop speed control for fast coverage, whereas the other states switch to fine closed-loop position control to handle steering, obstacle avoidance, and junction negotiation.

### 3. 逐句溯源

1. 句子 1：The Joey pipe-inspection controller is implemented as a finite-state exploration supervisor that uses only range, odometry, and orientation sensing to recognize `13` discrete robot states in an unknown pipe network.
   对应摘录：A, B
2. 句子 2：Its state set covers nominal travel states such as `Straight center` and `straight sided`, maneuvering and risk states such as `Sided`, `Crash left/right`, and `Flip-risk`, and topological states such as `Dead-end`, `T junction`, `left/right branch`, `Open space or manhole`, and `Cross`.
   对应摘录：A
3. 句子 3：Once the current state is confirmed, the robot follows two global exploration directives: at junctions it always turns into the furthest-right direction, and at a dead-end it turns around to return to the previous junction so the whole network can be exhaustively covered without SLAM.
   对应摘录：B
4. 句子 4：The state-action table then refines those directives into concrete maneuvers, for example turning `90°` at a left corner or cross, moving forward and then turning `45°` at a right branch, turning `180°` and re-centering at a dead-end, and backing or advancing slowly to escape a flip-risk state.
   对应摘录：C
5. 句子 5：Control execution is also mode-dependent: straight pipes and left-branch travel use closed-loop speed control for fast coverage, whereas the other states switch to fine closed-loop position control to handle steering, obstacle avoidance, and junction negotiation.
   对应摘录：B
