# Autonomous Behavior Intelligence Control of Self-Evolution Mobile Robot for High-Voltage Transmission Line in Complex Smart Grid - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把高压输电线路维护机器人写成“层次行为规划 + 三套任务 `FSM` + 断点恢复状态序列”的完整控制体系，原文细节和实测回路都足够强。

## 备注

- 当前 `paper_content.txt` 中存在少量连字/抽取噪声，例如 `IK_he` 这类字符替换，但状态向量、事件列表、流程图标题和实验结论均可稳定追溯，不影响本次条目抽取。

## 条目 1: Multitask Transmission-Line Maintenance Behavior Supervisor

- 控制对象：通用控制与电力运维机器人领域的高压输电线路多任务维护行为监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向高压输电线路绝缘子更换、引流板螺栓紧固和阻尼器更换的多任务维护机器人控制体系，用层次行为规划组织共享移动平台、双机械臂、末端执行器和任务级 `FSM`。
- 判断：算。对象是实际带原型机和现场试验的电力维护机器人控制系统，正文既给出状态向量与状态转移函数，也把三项操作任务分别展开成明确的 `FSM`，并补上了异常恢复链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 19-33, 58-63 行
> ... this paper proposes a new configuration of a reconfigurable power robot with terminal functions and its autonomous operation behavior control method for the three typical tasks which are the high-voltage transmission line insulators, drainage plates, and dampers maintenance.
>
> Through the analysis and planning of the robot operation behavior, the robot finite state machine (FSM) model in the three operation states has been established. Through the introduction of the state transfer function in the FSM, the automatic switching control between the robot key operation states can be realized ...
>
> ... the robot motion behavior during the operation can be divided into a combination of multiple basic behaviors ... The finite state machine (FSM) model is used to realize the management and control of the combined behavior ...

#### 摘录 B

- 出处：第 6-7 页，状态向量与层次行为规划，`paper_content.txt` 第 229-258, 266-270 行
> Table 4: Robot state vector.
> ...
> 4 Walking mechanism 0: walking; 1: stop
> 5 Insulator clamping mechanism state ... 0: clamping; 1: release
> 8 Drainage plate bolt tightening mechanism state ... 0: tightening; 1: loosen
> 9 Damper clamping mechanism state ... 0: clamping; 1: release
> 10 Damper bolt tightening mechanism 0: clamping; 1: release
>
> Table 5: The robot’s effective state vector value.
> S0 Initial state
> S1 Insulator steel cap clamping state
> S2 Clamping state of bowl head hanging plate
> S3 W pin rolling out status
> S4 Alignment of drainage plate bolts
> S5 Alignment of drainage plate nut
> S6 Damper clamping state
> S7 Damper bolt alignment state
> ...
>
> Therefore, the whole process of completing different tasks on the power transmission line by the robot represented by the basic behavior and combined behavior of the robot can be obtained as shown in Figure 6.

#### 摘录 C

- 出处：第 8-9 页，`4. Robot Operation FSM and Autonomous Control System Design`，`paper_content.txt` 第 311-365 行
> ... the robot motion planning decision can be made through the behavior database and FSM model ...
>
> 4.1. FSM Design for Insulator Replacement Operation ... The robot FSM design for insulator replacement is shown in Figure 8. The operation can be divided into nineteen states, which are triggered by nineteen events ... (7) the robot moves forward at a low speed; (8) the robot walking wheel touches the suspension clamp ... (12) push out W pin; (13) clamping of the insulator; (14) push out the ball head; (15) replace the insulator ...
>
> 4.2. FSM Design for Drainage Plate Bolt Tightening Operation ... The operation can be divided into eighteen states, which are triggered by eighteen events ... (13) operation manipulator 1 fixes the bolt head; (14) operation manipulator 2 tightens the nut ...
>
> 4.3. FSM Design for Damper Replacement Operation ... The operation can be divided into nineteen states, which are triggered by nineteen events ... (9) bolt align; (10) align success; (11) align fail; (12) fix bolt head success; (13) fix bolt head fail ... (16) manipulator 2 tightens the nut; (17) operation is completed ...

#### 摘录 D

- 出处：第 10-11 页，断点恢复与状态参数序列，`paper_content.txt` 第 420-426 行
> Therefore, the robot is required to have the ability to self-recover behavior after the system restarts ... the state parameter sequence is added on the basis of the robot behavior motion planning sequence and stored in the robot database system to store the robot real-time status information, including the number of steps in the running action sequence, the execution status of this step, the hall sensor light potential information, count value of the motor executed in this step, and tilt sensor information.
>
> After the robot restarts from the breakpoint, it first recognizes the step and status in the state parameter sequence and then combines the motor count value and sensor information value to complete the continuation of the action planning sequence.

#### 摘录 E

- 出处：第 13-15 页，`Field Operation Experiment`，`paper_content.txt` 第 572-606, 642-644 行
> ... in the process of insulator replacement ... the free state-insulator-bowl head hanging plate, clamping-steel cap, W pin-pushing, ball head-pushing, a series of smooth states and behavior transition, and the robot insulator replacement operation can be successfully completed. Due to the intelligent behavior control, the actual operation steps of insulator replacement have reduced from nineteen steps of FSM theoretical model to six ...
>
> ... during the maintenance operation of the drainage plate, a series of state and behavior transitions smoothly from the robot nut alignment-bolt head alignment-nut-fixing bolt head, and the robot drainage plate fastening operation is successfully completed ... the actual operation steps of drainage plate tightening have reduced from eighteen steps of FSM theoretical model to four ...
>
> ... in the process of replacement of the damper, a series of state and behavior transitions smoothly by bolt alignment-tightening the bolt-line clamp alignment-line clamp clamping, and the robot damper replacement operation is successfully completed ... the actual operation steps of damper replacement have reduced from nineteen steps of FSM theoretical model to four.
>
> ... the robot finite state machine model for three different tasks has been designed and a hierarchical architecture, finite state machine model of the robot autonomous behavior control method, has been proposed.

### 2. 基于原文整理后的自然语言描述

The retained control object is a hierarchical autonomous-behavior supervisor for a reconfigurable high-voltage transmission-line maintenance robot that must support three distinct operations: insulator replacement, drainage-plate bolt tightening, and damper replacement. At the representation level, the paper defines actuator- and mechanism-level state variables for walking, arm motion, clamping, bolt tightening, and pitch control, and then maps them into effective symbolic states such as `S0` through `S15`, including insulator, drainage, and damper-related checkpoints. On top of that state vocabulary, the planning layer uses a behavior database and task-specific `FSM` models to drive three concrete workflows: the insulator task exposes `19` states and `19` events, the drainage-plate task exposes `18` states, and the damper task exposes `19` states including explicit `align success/fail` and `fix bolt head success/fail` branches. This makes the system hierarchical rather than flat, because the overall robot behavior is decomposed into basic and combined behaviors, while each maintenance task is governed by its own dedicated `FSM`. The controller also includes an explicit self-recovery mechanism: a state-parameter sequence stores the current step number, execution status, hall-sensor information, motor count, and tilt data so that, after an industrial-computer restart, the robot can resume the action plan from the recorded breakpoint. The field-operation section then closes the loop by showing that the practical execution compresses the theoretical `19/18/19`-step models into smoother main chains of `6/4/4` steps for the three tasks while still preserving named state transitions such as `free state -> bowl head clamping -> steel cap clamping -> W pin pushing` and `nut alignment -> bolt head alignment -> nut-fixing`.

### 3. 逐句溯源

1. 句子 1：The retained control object is a hierarchical autonomous-behavior supervisor for a reconfigurable high-voltage transmission-line maintenance robot that must support three distinct operations: insulator replacement, drainage-plate bolt tightening, and damper replacement.
   对应摘录：A, E
2. 句子 2：At the representation level, the paper defines actuator- and mechanism-level state variables for walking, arm motion, clamping, bolt tightening, and pitch control, and then maps them into effective symbolic states such as `S0` through `S15`, including insulator, drainage, and damper-related checkpoints.
   对应摘录：B
3. 句子 3：On top of that state vocabulary, the planning layer uses a behavior database and task-specific `FSM` models to drive three concrete workflows: the insulator task exposes `19` states and `19` events, the drainage-plate task exposes `18` states, and the damper task exposes `19` states including explicit `align success/fail` and `fix bolt head success/fail` branches.
   对应摘录：C
4. 句子 4：This makes the system hierarchical rather than flat, because the overall robot behavior is decomposed into basic and combined behaviors, while each maintenance task is governed by its own dedicated `FSM`.
   对应摘录：A, B, E
5. 句子 5：The controller also includes an explicit self-recovery mechanism: a state-parameter sequence stores the current step number, execution status, hall-sensor information, motor count, and tilt data so that, after an industrial-computer restart, the robot can resume the action plan from the recorded breakpoint.
   对应摘录：D
6. 句子 6：The field-operation section then closes the loop by showing that the practical execution compresses the theoretical `19/18/19`-step models into smoother main chains of `6/4/4` steps for the three tasks while still preserving named state transitions such as `free state -> bowl head clamping -> steel cap clamping -> W pin pushing` and `nut alignment -> bolt head alignment -> nut-fixing`.
   对应摘录：E
