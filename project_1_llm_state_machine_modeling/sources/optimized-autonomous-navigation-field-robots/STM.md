# Optimized autonomous navigation for field robots: extended results and practical deployment - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然主体包含导航算法细节，但把 FarmBeast 的 `ROS SMACH` 导航状态机、行间跟随、行尾判定和转向完成条件都写清楚了，足以形成一条完整的农业机器人监督控制样本。

## 条目 1: Row-following-turning-realignment navigation supervisor

- 控制对象：通用控制与形式化工具领域的 FarmBeast 田间机器人行间导航监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是农业田间移动机器人在作物行之间自主导航的顶层监督控制器，用 `initialization / row following / turning / realignment` 等离散状态管理行内居中、行尾判定与换行转向。
- 判断：算。对象是实际 field robot 的导航控制器，原文明确说明了 `ROS SMACH` FSM、主要状态、从行内跟随到行尾转向的切换条件，以及转向完成的姿态比较规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`Control architecture State Machine Implementation`
> The navigation logic is governed by a finite-state machine (FSM) implemented in ROS using the SMACH library. This structure enables flexible control across different navigation states, including row following, turning, and obstacle avoidance ...
>
> The sequence begins with initialization, followed by row navigation until the row is completed. The robot then performs a two-phase turn: first a 90° rotation, then a forward movement based on odometry, and finally another 90° turn into the next row.

#### 摘录 B

- 出处：第 6 页，Figure 5 图注
> Finite-state machine (FSM) design for FarmBeast navigation, implemented in ROS SMACH. The diagram illustrates transitions between states: initialization, row following, turning, and realignment. This modular control structure enables flexible adaptation to different field layouts and supports advanced navigation tasks used at the Field Robot Event.

#### 摘录 C

- 出处：第 7 页，行间跟随与行尾判定
> During motion, the algorithm calculates the center point of each subset by averaging the X and Y coordinates ...
>
> If one side lacks a sufficient number of points ... the center from the opposite side is mirrored across the robot's coordinate axis ...
>
> If neither side provides sufficient data to calculate a center point ... the system concludes that the robot has reached the end of the row and initiates the turning procedure.
>
> The center lies within a narrow forward band -> no correction required ... to the left -> robot corrects by steering right ... to the right -> robot corrects by steering left.

#### 摘录 D

- 出处：第 8-9 页，`Turning`
> These equations calculate the quaternion representing the desired rotation, typically 90°, -90° or 180°.
>
> To perform the turn, the current quaternion is stored at the start of the turn.
>
> Finally, the current quaternion is compared to the target quaternion during the turn. ... the algorithm checks when the orientations are sufficiently close, falling within the defined margin of ε.

### 2. 基于原文整理后的自然语言描述

The FarmBeast navigation controller is implemented as a ROS `SMACH` finite-state machine that supervises field traversal through states such as `initialization`, `row following`, `turning`, and `realignment`, with obstacle avoidance also integrated as part of the navigation logic. Its top-level sequence is explicit: after initialization, the robot follows a crop row until the row is considered complete, then executes a two-phase turn consisting of a `90°` rotation, an odometry-based forward move, and a second `90°` rotation into the next row. The row-following state itself is guard-rich rather than a black box: it computes left and right crop-row centers, mirrors one side when only the opposite row is visible, and uses the resulting center position to choose between going straight, steering right, or steering left. If neither side yields a valid center across several iterations, the supervisor concludes that the robot has reached the row end and triggers the turning state. Turn completion is also state-controlled, because the controller stores the initial quaternion, computes a target orientation such as `90°`, `-90°`, or `180°`, and exits the turn only when the live quaternion falls within an `ε`-margin of the target.

### 3. 逐句溯源

1. 句子 1：The FarmBeast navigation controller is implemented as a ROS `SMACH` finite-state machine that supervises field traversal through states such as `initialization`, `row following`, `turning`, and `realignment`, with obstacle avoidance also integrated as part of the navigation logic.
   对应摘录：A, B
2. 句子 2：Its top-level sequence is explicit: after initialization, the robot follows a crop row until the row is considered complete, then executes a two-phase turn consisting of a `90°` rotation, an odometry-based forward move, and a second `90°` rotation into the next row.
   对应摘录：A
3. 句子 3：The row-following state itself is guard-rich rather than a black box: it computes left and right crop-row centers, mirrors one side when only the opposite row is visible, and uses the resulting center position to choose between going straight, steering right, or steering left.
   对应摘录：C
4. 句子 4：If neither side yields a valid center across several iterations, the supervisor concludes that the robot has reached the row end and triggers the turning state.
   对应摘录：C
5. 句子 5：Turn completion is also state-controlled, because the controller stores the initial quaternion, computes a target orientation such as `90°`, `-90°`, or `180°`, and exits the turn only when the live quaternion falls within an `ε`-margin of the target.
   对应摘录：D
