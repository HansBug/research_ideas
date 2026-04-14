# Reaching and Grasping a Glass of Water by Locked-In ALS Patients through a BCI-Controlled Humanoid Robot - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 BCI 辅助人形机器人明确写成 `wait / wander / grasp / give` 四态有限状态机，并给出高层 `grasp / give` 指令如何触发自主感知、寻路、抓取和递送链条，足以构成双 A 的医疗辅助机器人样本。

## 条目 1: Wait-wander-grasp-give assistive humanoid controller
- 控制对象：医疗辅助机器人领域的 BCI 人形机器人抓取与递送自主控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 locked-in ALS 患者辅助取水任务的人形机器人控制器，用脑机接口选择 `grasp` 或 `give` 目标级命令，再由机器人自己的有限状态机完成定位、接近、抓取与递送。
- 判断：算。对象是真实 assistive robot controller 而不是实验界面脚本；原文清楚写出有限状态机状态、目标级命令和自主行为序列。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5-6 页，Figure `1` 与系统描述
> The robot starts in the wait state. When a command is sent, the robot enter in wander mode to acquire the position of the glass (grasp) or the user (give) with landmarks and reaching it/him by the shortest path. After the object/user has been reached, he acts accordingly to grasp or give state. In grasp state, the robot will bend over and take the glass, in give state it will bend over and offers the glass to the user.

#### 摘录 B
- 出处：第 6 页，Figure `2` 说明
> The Robotic System is composed of an AI Module which translates the received commands in actions of the Nao Robot. There, a Finite State Machine generates the corresponding sequence of behaviors to be actuated by the robot.

#### 摘录 C
- 出处：第 8 页，`The Robot System`
> An autonomous mode based on a Finite State Machine allowing the user to control the robot at the goal level (e.g., to grasp an object). ... For each scenario, an autonomous system based on a Finite State Machine was developed to implement two complex actions: Grasp an object; Give an object.

### 2. 基于原文整理后的自然语言描述

The BCI-controlled assistive robot uses a four-state behavior machine consisting of `wait`, `wander`, `grasp`, and `give`. The user does not micromanage each motion primitive; instead, a goal-level `grasp` or `give` command is selected through the BCI, and the AI module maps that command into a state-machine-driven sequence of autonomous robot behaviors. After leaving `wait`, the robot enters `wander` to localize the glass or the user with landmarks and to approach the target along a shortest path. Once the target is reached, the controller branches into either `grasp`, where the robot bends and picks up the glass, or `give`, where it bends and offers the glass to the user. The paper further contrasts this autonomous FSM mode with a low-level teleoperated mode, making the autonomous state machine the core mechanism that upgrades the interface from direction-by-direction driving to goal-level assistance.

### 3. 逐句溯源

1. 句子 1：The BCI-controlled assistive robot uses a four-state behavior machine consisting of `wait`, `wander`, `grasp`, and `give`.
   对应摘录：A
2. 句子 2：The user does not micromanage each motion primitive; instead, a goal-level `grasp` or `give` command is selected through the BCI, and the AI module maps that command into a state-machine-driven sequence of autonomous robot behaviors.
   对应摘录：B, C
3. 句子 3：After leaving `wait`, the robot enters `wander` to localize the glass or the user with landmarks and to approach the target along a shortest path.
   对应摘录：A
4. 句子 4：Once the target is reached, the controller branches into either `grasp`, where the robot bends and picks up the glass, or `give`, where it bends and offers the glass to the user.
   对应摘录：A, C
5. 句子 5：The paper further contrasts this autonomous FSM mode with a low-level teleoperated mode, making the autonomous state machine the core mechanism that upgrades the interface from direction-by-direction driving to goal-level assistance.
   对应摘录：C
