# BEATLE -- Self-Reconfigurable Aerial Robot: Design, Control and Experimental Validation - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 BEATLE 的空中重构运动规划器写成了由多个 `Sub-FSM` 组成的分层重构流程，并明确给出了相对位姿约束、误差回退和装配完成后的参数更新。

## 条目 1: Hierarchical In-Flight Reconfiguration Planner
- 控制对象：BEATLE 空中模块化机器人在飞行中执行对接/分离的重构运动规划器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是空中自重构机器人领域的重构运动规划器，用来协调 leader/follower 模块在飞行中的相对定位、接触建立、对接锁定和反向拆解。
- 判断：算。对象是实际 BEATLE 原型的重构控制链，原文明确给出了 `Sub-FSM` 层次结构、单次装配动作的三阶段划分、相对位姿约束、误差阈值触发的回退以及装配完成后的结构参数更新。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 16-25
> "motion planner" based on a finite state machine

#### 摘录 B
- 出处：第 5-6 页，Section IV / Figure 6，行 384-389、427-435
> "individual state" ... "Sub-FSM"

#### 摘录 C
- 出处：第 6 页，Section IV，行 436-458
> "Approach" ... "Alignment" ... "Assembly"

### 2. 基于原文整理后的自然语言描述

The BEATLE reconfiguration planner is organized as a hierarchical FSM in which the overall motion planner chains multiple `Sub-FSM`s and each sub-FSM handles one unitary aerial assembly action. Inside one unitary action, the follower module is first guided to satisfy a desired relative distance and orientation with respect to the leader, then moves toward the leader to establish contact while continuously checking pose error. If the pose error grows beyond the allowed threshold during contact approach, the controller falls back to the alignment phase and retries the maneuver instead of continuing into an unsafe dock. After successful contact, the planner enters the assembly phase, activates the docking mechanism, and updates the number and arrangement of interconnected modules. The same phase chain is executed in reverse order for disassembly, so the controller covers both in-flight merging and separation.

### 3. 逐句溯源

1. 句子 1：The BEATLE reconfiguration planner is organized as a hierarchical FSM in which the overall motion planner chains multiple `Sub-FSM`s and each sub-FSM handles one unitary aerial assembly action.
   对应摘录：A, B
2. 句子 2：Inside one unitary action, the follower module is first guided to satisfy a desired relative distance and orientation with respect to the leader, then moves toward the leader to establish contact while continuously checking pose error.
   对应摘录：C
3. 句子 3：If the pose error grows beyond the allowed threshold during contact approach, the controller falls back to the alignment phase and retries the maneuver instead of continuing into an unsafe dock.
   对应摘录：C
4. 句子 4：After successful contact, the planner enters the assembly phase, activates the docking mechanism, and updates the number and arrangement of interconnected modules.
   对应摘录：C
5. 句子 5：The same phase chain is executed in reverse order for disassembly, so the controller covers both in-flight merging and separation.
   对应摘录：A, C
