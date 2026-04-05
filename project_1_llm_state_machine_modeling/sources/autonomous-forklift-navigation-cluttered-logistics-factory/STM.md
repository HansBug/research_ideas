# Autonomous Forklift Navigation Inside a Cluttered Logistics Factory - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把工厂物流叉车的走廊导航与避障行为明确落成 `Rotate / Move / Avoid` 三状态 FSM，并说明何时切入局部规划、何时等待障碍消失再恢复，是一条完整的工业导航监督控制链。

## 条目 1: Rotate-Move-Avoid Forklift Navigation FSM
- 控制对象：工业自动化与离散制造领域的工厂物流叉车走廊导航与避障控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于拥挤物流工厂中自主叉车导航的高层行为状态机，用旋转对齐、走廊跟踪和障碍绕行三个模式协调局部规划与路径跟踪。
- 判断：算。对象是真实叉车导航控制器而不是单独的路径规划算法；原文给出明确状态集合、转移条件、状态职责和动态障碍恢复逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract
> A finite-state machine (FSM) architecture ensures transitions between the different operating modes of a robot during a mission, including obstacle avoidance.

#### 摘录 B
- 出处：第 8 页，Section `4.2.3 State Transition`
> Finally, the robot’s behavior is handled by a finite state machine (FSM).
> When the robot navigates through a corridor, it operates within three main states: Rotate, Move, and Avoid. The Rotate state aligns the robot with the corridor’s general direction by executing a pure rotation before initiating movement. Next, the Move state is dedicated to the robot following of the path at the center of the corridor, using the CLMPC without further path planning. If the robot detects an obstacle in the path, it transitions to the Avoid state. In this state, both the local planner and the CLMPC are used to navigate around obstacles safely. In order to leave the Avoid state, the FSM waits for obstacles to be cleared.

#### 摘录 C
- 出处：第 8-9 页，Section `4.2.3 State Transition`
> Figure 14 displays the robot’s path, indicating the different FSM states during an obstacle avoidance case.
>
> ... a dynamic obstacle intermittently blocked the remaining gap for a period of time ... The purpose of this test was to check that the robot would respond to dynamic challenges, stop in front of an impassable obstacle and, once the moving obstacle had been removed, could resume its avoidance process.

### 2. 基于原文整理后的自然语言描述

The forklift navigation supervisor is a three-state FSM that coordinates corridor alignment, nominal path following, and obstacle avoidance inside a cluttered logistics factory. In `Rotate`, the vehicle performs a pure rotation to align itself with the general corridor direction before it begins forward motion. Once aligned, the controller switches to `Move`, where the forklift follows the path centered in the corridor using the CLMPC controller alone, without invoking additional local path planning. When an obstacle appears in the intended path, the FSM transfers control to `Avoid`, where a local planner and CLMPC are used together to generate and track a safe bypass maneuver. The return condition is also explicit: the machine does not leave `Avoid` until the obstacle has been cleared, and in the dynamic-obstacle experiment the robot is expected to stop in front of an impassable blockage and resume the avoidance process only after the moving obstacle disappears.

### 3. 逐句溯源

1. 句子 1：The forklift navigation supervisor is a three-state FSM that coordinates corridor alignment, nominal path following, and obstacle avoidance inside a cluttered logistics factory.
   对应摘录：A, B
2. 句子 2：In `Rotate`, the vehicle performs a pure rotation to align itself with the general corridor direction before it begins forward motion.
   对应摘录：B
3. 句子 3：Once aligned, the controller switches to `Move`, where the forklift follows the path centered in the corridor using the CLMPC controller alone, without invoking additional local path planning.
   对应摘录：B
4. 句子 4：When an obstacle appears in the intended path, the FSM transfers control to `Avoid`, where a local planner and CLMPC are used together to generate and track a safe bypass maneuver.
   对应摘录：B
5. 句子 5：The return condition is also explicit: the machine does not leave `Avoid` until the obstacle has been cleared, and in the dynamic-obstacle experiment the robot is expected to stop in front of an impassable blockage and resume the avoidance process only after the moving obstacle disappears.
   对应摘录：B, C
