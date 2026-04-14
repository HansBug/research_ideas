# A ROS-Based GNC Architecture for Autonomous Surface Vehicle Based on a New Multimission Management Paradigm - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把自主水面艇的 mission manager 直接落成可中断、可并发、带优先级重排的层次状态机，并明确写出 `Ready / Run / Interrupted / Terminated` 外层状态和电量驱动的 recharge 抢占逻辑。

## 条目 1: Priority-Switched Multimission Manager for ASV
- 控制对象：通用控制与自主水面艇领域的多任务管理与切换监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用于自主水面艇长期任务运行的高层 mission management 控制器，负责在多个 mission 之间按优先级切换，并在 mission 内部执行嵌套或并发任务状态机。
- 判断：算。对象是真实 ASV 软件架构中的 high-level manager；原文明确说明 mission 用状态机建模、给出外层状态集合、说明中断与恢复策略，并给出电池阈值触发 recharge mission 抢占的控制逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Introduction，行 65-80
> ... a multimission paradigm is introduced that enables the possibility to design an autonomous switching mechanism between simultaneous active missions. ... a multimission manager module allows one to select in real time, which mission has to be performed according to the assumed priorities, by switching between the active ones. ... each robot's behavior is modeled by using a state machine where the inner states represent single tasks. ... The aim of this module is to provide an intelligent way to perform high-level mission management ...

#### 摘录 B
- 出处：第 9 页，Section `4.1 Mission Modeling`，行 404-429
> An intuitive tool suitable for modeling missions as a sequence of tasks is given by finite state machines. Each task defines a state ... The hierarchical state machine reported in Figure 9 can be used to allow missions to be interrupted by implementing a priority-based switching mechanism. ... Ready ... Run ... This state contains a nested state machine that specifies the tasks to reach the mission goal. ... Interrupted ... The interrupted mission can restart from the beginning or from the last task executed ... Terminated ... The RUN state contains nested state machines that represent the main tasks that compose a mission. These tasks can be organized in a sequential way, or they can be executed concurrently if there is no conflict in the use of the actuators.

#### 摘录 C
- 出处：第 9 页，Section `4.2 Mission Management`，行 433-449
> These missions can be time-fixed scheduled or dynamically scheduled using a priority-based mechanism. Then, the manager module selects in real time which mission has to be performed with respect to their priority, by switching between the active ones. ... The mission_manager node is in charge of the decision-making mechanism used to perform dynamic mission scheduling. ... an energy consumption estimation can be done for each mission ... if the battery level is under a safe threshold, the vehicle can increase the priority of a recharging mission with the aim to interrupt the current mission and go back to the home position.

### 2. 基于原文整理后的自然语言描述

The ASV multimission manager is a hierarchical state machine that keeps each mission in one of four outer states: `Ready`, `Run`, `Interrupted`, or `Terminated`. A mission enters `Run` only when it becomes the highest-priority active mission, and the `Run` state contains a nested task state machine that drives the concrete job sequence needed to accomplish that mission. The paper explicitly states that the nested tasks may be executed sequentially or concurrently when they do not conflict over actuators, so the mission model includes both hierarchy and parallelism. If a higher-priority mission appears, the current mission is preempted into `Interrupted`, from which it may restart either from the beginning or from the last completed task according to policy settings. Priority levels are also recomputed against vehicle conditions, and a low-battery threshold can raise a recharging mission to interrupt the current mission and send the vehicle back to a home position.

### 3. 逐句溯源

1. 句子 1：The ASV multimission manager is a hierarchical state machine that keeps each mission in one of four outer states: `Ready`, `Run`, `Interrupted`, or `Terminated`.
   对应摘录：A, B
2. 句子 2：A mission enters `Run` only when it becomes the highest-priority active mission, and the `Run` state contains a nested task state machine that drives the concrete job sequence needed to accomplish that mission.
   对应摘录：B, C
3. 句子 3：The paper explicitly states that the nested tasks may be executed sequentially or concurrently when they do not conflict over actuators, so the mission model includes both hierarchy and parallelism.
   对应摘录：B
4. 句子 4：If a higher-priority mission appears, the current mission is preempted into `Interrupted`, from which it may restart either from the beginning or from the last completed task according to policy settings.
   对应摘录：B, C
5. 句子 5：Priority levels are also recomputed against vehicle conditions, and a low-battery threshold can raise a recharging mission to interrupt the current mission and send the vehicle back to a home position.
   对应摘录：C
