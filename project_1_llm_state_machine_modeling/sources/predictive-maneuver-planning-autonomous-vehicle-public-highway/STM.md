# Predictive Maneuver Planning for an Autonomous Vehicle in Public Highway Traffic - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速公路机动规划写成 lane/speed 双参考的 maneuver automaton，并把 `cruising / following / leading / lane change`、参考速度规则与强制换道条件一起接到同一套预测轨迹规划器上，能稳定形成高质量 `EFSM + T0` 样本。

## 条目 1: Predictive Reference-Speed and Lane-Maneuver Automaton

- 控制对象：汽车与道路车辆控制领域的高速公路自动驾驶巡航、跟车、领车与换道预测机动监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个把离散机动自动机和连续 MPC 轨迹规划耦合起来的高速公路行为决策器，用每车道的参考速度规则和全局车道选择来决定巡航、跟车、领车还是换道。
- 判断：算。对象是实际自动驾驶车辆的机动规划控制器，原文明确给出 FSM 场景集合、机动集合、参考速度赋值规则、触发强制换道的 guard，以及与碰撞约束耦合的轨迹规划关系。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，系统架构描述，`paper_content.txt` 第 187-199 行
> “finite state machines”
>
> “cruising, following, leading and lane change”

#### 摘录 B

- 出处：第 5-6 页，`IV.A-B`，`paper_content.txt` 第 441-459, 499-510 行
> “rule-based switch”
>
> “vt,r,l = vt,ref”

#### 摘录 C

- 出处：第 6 页，`Reference Speed Adjustment`，`paper_content.txt` 第 527-549 行
> “forced lane change”

### 2. 基于原文整理后的自然语言描述

The highway maneuver planner is organized as a hybrid maneuver automaton in which each lane carries discrete candidate maneuvers and an associated reference speed that is later optimized together with the trajectory. At the assigner level, the paper explicitly stores scenario-based FSMs whose highway machine contains `cruising`, `following`, `leading`, and `lane change`, while the continuous predictive-trajectory-guidance layer solves the motion states and maneuver references over the horizon. For a given lane, cruising means tracking the desired cruise speed, whereas following or leading reassigns the lane reference speed to the detected front or rear vehicle; these rule-based speed switches are generated at every prediction step before the lane-selection optimization is solved. If the currently assigned reference speed falls outside the acceptable speed band around the cruise target, the controller activates a forced lane change toward an empty adjacent lane or the lane whose assigned speed is closest to the desired cruise speed. The same supervisor is then constrained by tightened collision-avoidance ellipses and speed-headway bounds, so the discrete maneuver choice remains directly coupled to safety-aware trajectory generation.

### 3. 逐句溯源

1. 句子 1：The highway maneuver planner is organized as a hybrid maneuver automaton in which each lane carries discrete candidate maneuvers and an associated reference speed that is later optimized together with the trajectory.
   对应摘录：A, B；`paper_content.txt` 第 187-199, 441-460 行。
2. 句子 2：At the assigner level, the paper explicitly stores scenario-based FSMs whose highway machine contains `cruising`, `following`, `leading`, and `lane change`, while the continuous predictive-trajectory-guidance layer solves the motion states and maneuver references over the horizon.
   对应摘录：A；`paper_content.txt` 第 192-201 行。
3. 句子 3：For a given lane, cruising means tracking the desired cruise speed, whereas following or leading reassigns the lane reference speed to the detected front or rear vehicle; these rule-based speed switches are generated at every prediction step before the lane-selection optimization is solved.
   对应摘录：B；`paper_content.txt` 第 452-460, 499-510, 573-585 行。
4. 句子 4：If the currently assigned reference speed falls outside the acceptable speed band around the cruise target, the controller activates a forced lane change toward an empty adjacent lane or the lane whose assigned speed is closest to the desired cruise speed.
   对应摘录：C；`paper_content.txt` 第 523-549 行。
5. 句子 5：The same supervisor is then constrained by tightened collision-avoidance ellipses and speed-headway bounds, so the discrete maneuver choice remains directly coupled to safety-aware trajectory generation.
   对应摘录：B；`paper_content.txt` 第 598-639 行。
