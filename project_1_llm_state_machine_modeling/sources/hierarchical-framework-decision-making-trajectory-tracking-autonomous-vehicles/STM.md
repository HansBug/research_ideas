# A Hierarchical Framework of Decision Making and Trajectory Tracking Control for Autonomous Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高速公路自动驾驶的行为决策层明确落成 `car following / free driving / left lane change / right lane change` 四状态 `Stateflow` FSM，并交代输入、状态集合、转移条件数量以及与规划控制链的接口。

## 条目 1: Four-State Highway Behavior-Planning FSM
- 控制对象：汽车与道路车辆控制领域的高速公路自动驾驶高层行为决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个位于自动驾驶分层架构顶层的四状态行为规划 FSM，用来在高速公路场景下在跟车、自由行驶和左右换道之间选择当前驾驶行为。
- 判断：算。对象是真实自动驾驶系统的高层决策控制器而不是单纯轨迹优化模块；原文明确给出状态集合、输入信息、换道安全判据、转移条件数量以及输出如何驱动后续规划模块。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `2. Overall Structure of the Framework`，行 121-149
> A typical driving scenario is shown in Figure 1. ... The road considered in this paper has three lanes by default and the driving behavior is an element from a finite set {car following, free driving, left lane change, right lane change}. ... The framework is a hierarchical structure which consists of a sensor system, decision-making module, trajectory-planning module and control module. ... The decision-making module is implemented by an FSM, which is responsible for adopting reasonable driving behavior according to the relationship between the EV and the surrounding vehicles. The relative distance and velocity are used to judge whether the adjacent lane is safe, which is the criterion for potentially changing lanes. After the reasonable decision signal is made, the target vehicle is also available and the decision signal is sent to the planning module ...

#### 摘录 B
- 出处：第 3-4 页，Section `3. Decision-Making Procedure`，行 152-183
> The decision-making procedure is implemented using an FSM algorithm in Stateflow to make reasonable and safe driving-behavior decisions according to the relationship between the EV and the other surrounding vehicles. The FSM is shown in Figure 3; the input to the FSM is the surrounding vehicles' information and the output is the desired driving state based on the current driving conditions. ... There are four driving states (car following, free driving, left lane change and right lane change) and six transition conditions (c1, c2, c3, c4, c5 and c6) in Figure 3. ... The target vehicle described in the transition condition c1 means the front vehicle under different driving states ... The output state of the FSM will be transmitted into the following trajectory planning module.

### 2. 基于原文整理后的自然语言描述

The autonomous-vehicle decision layer is a four-state FSM that selects one behavior from `car following`, `free driving`, `left lane change`, and `right lane change` for a three-lane highway scenario. Its inputs are the positions, velocities, and related surrounding-vehicle information needed to judge whether the adjacent lanes are safe, and the lane-change decision is explicitly tied to safe-distance checks derived from the surrounding traffic relationship. Once a state is selected, the decision module also identifies the target vehicle associated with that maneuver and sends the resulting driving state to the downstream trajectory-planning module. The rest of the framework then generates a local path and speed profile and tracks them with LQR lateral control and PID-based longitudinal control. The paper further states that the `Stateflow` machine contains four driving states and six transition conditions, so the maneuver planner is described as a concrete supervisory FSM rather than a loose policy narrative.

### 3. 逐句溯源

1. 句子 1：The autonomous-vehicle decision layer is a four-state FSM that selects one behavior from `car following`, `free driving`, `left lane change`, and `right lane change` for a three-lane highway scenario.
   对应摘录：A, B
2. 句子 2：Its inputs are the positions, velocities, and related surrounding-vehicle information needed to judge whether the adjacent lanes are safe, and the lane-change decision is explicitly tied to safe-distance checks derived from the surrounding traffic relationship.
   对应摘录：A, B
3. 句子 3：Once a state is selected, the decision module also identifies the target vehicle associated with that maneuver and sends the resulting driving state to the downstream trajectory-planning module.
   对应摘录：A, B
4. 句子 4：The rest of the framework then generates a local path and speed profile and tracks them with LQR lateral control and PID-based longitudinal control.
   对应摘录：A
5. 句子 5：The paper further states that the `Stateflow` machine contains four driving states and six transition conditions, so the maneuver planner is described as a concrete supervisory FSM rather than a loose policy narrative.
   对应摘录：B
