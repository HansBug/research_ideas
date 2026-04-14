# A microservice based control architecture for mobile robots in safety-critical applications - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把安全关键配送机器人的任务流程、人工接管、等待恢复和全局错误场景写成了可中断的分层 HFSM，并明确展示了并发特征节点和定时等待分支。

## 条目 1: Operator-overridable autonomous-ride mission controller

- 控制对象：通用控制与移动机器人领域的可人工接管自主配送任务控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向公共空间配送机器人的 `HFSM + microservices` 任务控制架构，用 `Mission Control` 编排自主行驶、人工接管、延时恢复和全局错误恢复等高层行为。
- 判断：算。对象是实际移动机器人高层控制器而不是泛软件框架；原文给出了状态定义、父子状态继承、全局 error scenario、人工接管事件、等待计时器以及在真实配送机器人项目中的 13 状态实现。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / 2.1 Hierarchical finite state machines`，`paper_content.txt` 第 1-21、111-154 行
> This paper presents the concept of a safety-critical Robot Control Architecture for mobile robots based on microservices and a Hierarchical Finite State Machine.
>
> HFSMs allow for nested states or states that are made up of a number of child states. ... child states can inherit characteristics such as functionality or transitions.

#### 摘录 B

- 出处：第 5-6 页，`3.1 States and transitions / Listing 1`，`paper_content.txt` 第 446-461、462-475 行
> The list of required or active features is part of the state definition ... In this example, these are autonomous_ride, horn, localization and teleoperation.
>
> As this approach is based on a HFSM, it allows states to be made up of one or more child states. ... Child states inherit the active_features from their parent state ...

#### 摘录 C

- 出处：第 6 页，`3.2 Error scenarios`，`paper_content.txt` 第 500-550 行
> this architecture introduces a global error state and error scenarios.
>
> an error scenario ... will force the system to assume a new state, namely the error state.
>
> implicit transitions are created going from each non-error state into the error state, using the error scenario’s trigger.
>
> The global error state ... will only leave the error state once all error scenarios have been resolved.

#### 摘录 D

- 出处：第 8-9 页，`4. Case study`，`paper_content.txt` 第 687-739 行
> The presented RCA is implemented in a dedicated ROS node and controls a total of 18 feature ROS nodes providing the functionality of 22 features. ... The final SMD is made up of 13 states, 21 transitions and 2 error scenarios.
>
> in autonomous_ride and all of its child states, the features internal_monitoring, horn, localization and teleoperation are active. Its initial child state is drive_to_coordinates.
>
> When the operator presses the button to take control of the robot, an event with the trigger operator_took_control is sent, causing Mission Control to transition to autonomous_ride_paused ... activating remote_navigation.
>
> an event with the trigger operator_gave_up_control is published causing Mission Control to transition to the state wait ... The active delay feature causes the Delay node to start a time ... This event causes Mission Control to transition to drive_to_coordinates.

### 2. 基于原文整理后的自然语言描述

The mission controller is a hierarchical state machine for a public-space delivery robot in which each state is defined as a set of concurrently active microservice features rather than as one monolithic procedure. Parent states can own child states and pass their `active_features` down the hierarchy, so a state such as `autonomous_ride` keeps monitoring, horn, localization, and teleoperation active while its initial child `drive_to_coordinates` performs the concrete navigation step. The architecture also defines a global error state with error scenarios that implicitly create transitions from every non-error state into the error state and keep the robot there until all active faults are resolved. In the real TaBuLa-LOG deployment, the final SMD contains `13` states, `21` transitions, and `2` error scenarios, and the autonomous-ride chain can be interrupted at any point by the operator. When `operator_took_control` is raised, the controller pauses autonomous ride and activates `remote_navigation`; when `operator_gave_up_control` is published, it moves to `wait`, uses the `Delay` feature as a timer, and then returns to `drive_to_coordinates` to resume autonomous motion.

### 3. 逐句溯源

1. 句子 1：The mission controller is a hierarchical state machine for a public-space delivery robot in which each state is defined as a set of concurrently active microservice features rather than as one monolithic procedure.
   对应摘录：A, B
2. 句子 2：Parent states can own child states and pass their `active_features` down the hierarchy, so a state such as `autonomous_ride` keeps monitoring, horn, localization, and teleoperation active while its initial child `drive_to_coordinates` performs the concrete navigation step.
   对应摘录：B, D
3. 句子 3：The architecture also defines a global error state with error scenarios that implicitly create transitions from every non-error state into the error state and keep the robot there until all active faults are resolved.
   对应摘录：C
4. 句子 4：In the real TaBuLa-LOG deployment, the final SMD contains `13` states, `21` transitions, and `2` error scenarios, and the autonomous-ride chain can be interrupted at any point by the operator.
   对应摘录：D
5. 句子 5：When `operator_took_control` is raised, the controller pauses autonomous ride and activates `remote_navigation`; when `operator_gave_up_control` is published, it moves to `wait`, uses the `Delay` feature as a timer, and then returns to `drive_to_coordinates` to resume autonomous motion.
   对应摘录：D
