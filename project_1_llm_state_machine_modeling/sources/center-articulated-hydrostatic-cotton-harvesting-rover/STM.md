# Center-Articulated Hydrostatic Cotton Harvesting Rover Using Visual-Servoing Control and a Finite State Machine - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把棉花采摘车的视觉感知、车体前后调整、机械臂上下调整和采摘动作整理成六状态七迁移 FSM，并给出了显式坐标 guard 与采摘阈值。

## 条目 1: Cotton-boll detection and harvesting supervisor
- 控制对象：中心铰接式棉花采摘车的视觉伺服任务监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个棉花采摘车在棉行内根据最近棉铃位置决定前后移动、上下调臂和执行采摘的任务级状态机。
- 判断：算。对象是真实农业采摘系统的监督控制器，不是纯视觉检测流程；原文给出了状态闭环、guard 条件、变量名和数值阈值。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> Each cotton-harvesting rover would need to accomplish three motions: the rover must move forward/backward, turn left/right, and the robotic manipulator must move to harvest cotton bolls.
>
> Controlling these actions can involve several complex states and transitions. However, using the robot operating system (ROS)-independent finite state machine (SMACH), adaptive and optimal control can be achieved.

#### 摘录 B
- 出处：第 13-14 页，Section 2.9 `Finite State Machine`
> Robot tasks and actions were categorized as states, and state "transitions" were modeled in a task-level architecture to create the rover actions required to harvest cotton bolls.
>
> The state machine had six necessary states and seven transitions.
>
> After every state, the system reverted to state 0 (get the image) and searched for cotton bolls.
>
> If a cotton boll was found, the system would calculate the distance of the boll from the manipulator in three-dimensional space (X,Y,Z).

#### 摘录 C
- 出处：第 14 页，Section 2.9 `Finite State Machine`
> If the boll was lined up horizontally, then the system would get the manipulator to move up or down relative to the position of the manipulator to the boll.
>
> If the boll was at the same level, then the system would harvest it.
>
> If the boll was in the front or back, the system would send a signal for the rover to move forward or back, using the PID control.
>
> If the system failed to see any bolls, the rover proceeded to pass over the cotton rows.

#### 摘录 D
- 出处：第 11 页，Algorithm 1 `Algorithm describing the detection of cotton bolls`
> IF (Yb > Ym) transition e (move forward);
>
> IF (Yb < Ym) transition e (move backward);
>
> IF (Yb = Ym and Zm > Zb) transition b (move the arm up);
>
> IF (Yb = Ym and Zm < Zb) transition c (move the arm down);
>
> IF (Yb = Ym and Zm = Zb and Xm - Xb < 37 cm) transition d (pick the boll).

### 2. 基于原文整理后的自然语言描述

The cotton-harvesting rover uses a task-level `SMACH` finite state machine that repeatedly returns to an image-acquisition state, searches for cotton bolls, and then chooses the next action according to the spatial relationship between the detected boll and the manipulator. After each cycle starts from `get image`, the controller computes the nearest boll position `(Xb, Yb, Zb)` and compares it against the current end-effector position `(Xm, Ym, Zm)`. If the boll lies ahead of or behind the manipulator in the row direction, the supervisor commands the rover to move forward or backward with PID control until the longitudinal offset is corrected. Once the boll is horizontally aligned, the controller decides between `move the arm up` and `move the arm down` according to the sign of the vertical mismatch, and only when both `Y` and `Z` are aligned does it evaluate the final harvest guard `Xm - Xb < 37 cm`. If that distance threshold is satisfied, the FSM enters the harvest action to pick the boll; otherwise the rover keeps traversing the cotton rows and re-enters the image state to continue the loop.

### 3. 逐句溯源

1. 句子 1：The cotton-harvesting rover uses a task-level `SMACH` finite state machine that repeatedly returns to an image-acquisition state, searches for cotton bolls, and then chooses the next action according to the spatial relationship between the detected boll and the manipulator.
   对应摘录：A, B
2. 句子 2：After each cycle starts from `get image`, the controller computes the nearest boll position `(Xb, Yb, Zb)` and compares it against the current end-effector position `(Xm, Ym, Zm)`.
   对应摘录：B, D
3. 句子 3：If the boll lies ahead of or behind the manipulator in the row direction, the supervisor commands the rover to move forward or backward with PID control until the longitudinal offset is corrected.
   对应摘录：C, D
4. 句子 4：Once the boll is horizontally aligned, the controller decides between `move the arm up` and `move the arm down` according to the sign of the vertical mismatch, and only when both `Y` and `Z` are aligned does it evaluate the final harvest guard `Xm - Xb < 37 cm`.
   对应摘录：C, D
5. 句子 5：If that distance threshold is satisfied, the FSM enters the harvest action to pick the boll; otherwise the rover keeps traversing the cotton rows and re-enters the image state to continue the loop.
   对应摘录：B, C, D
