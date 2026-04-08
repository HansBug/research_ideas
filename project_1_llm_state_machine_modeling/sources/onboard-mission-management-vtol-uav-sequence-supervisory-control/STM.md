# Onboard Mission Management for a VTOL UAV Using Sequence and Supervisory Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 VTOL UAV 的机载任务管理拆成 `Mission Mode / Command Mode / Mission Controller Off / Stand By / Slow Down / Parse Command` 等层次状态，并用监督层接管 `Fly Home` 等高层目标，足以形成稳定的双 A HSM 样本。

## 条目 1: Mission-Mode / Command-Mode VTOL UAV Supervisor

- 控制对象：VTOL 无人机的机载任务执行与监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是航空航天与飞行控制领域的 VTOL UAV 机载 mission supervisor，用分层状态图管理 mission-plan 处理、直接命令执行、悬停待机、减速切换与高层 deliberate behaviors。
- 判断：算。对象是真实无人机任务管理控制器，原文明确给出了层次状态、事件优先级、行为结束回跳、命令解析和监督层的 `Fly Home / Search and Track` 高层任务。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，`Fig. 3 / The Sequence Control System`，`paper_content.txt` 第 381-403 行
> The UML model of the Sequence Control System is shown in Figure 3. It has two hierarchical levels where the top level models the procedural flow for a safe operation.
>
> The two composite states, ”Mission Mode” and ”Command Mode”, model mission plan processing and direct command execution respectively.
>
> Every state of the top level has a transition to the ”Mission Controller Off” ...
>
> another idle state ”Stand By” lets the UAV hover at its current position ...
>
> The state ”Slow Down” is necessary to assure a smooth changeover into ”Stand By” ...
>
> For each behavior there exists a termination condition, which transits into the command parser ”Parse Command”.

#### 摘录 B

- 出处：第 7-8 页，`The Supervisory Control System`，`paper_content.txt` 第 406-423 行
> The Supervisory Control System is responsible for taking high level decisions based on internal and external events.
>
> It is responsible for managing requests from the UAV operator ... as well as reacting to a loss of the data link.
>
> It can command the Sequence Control System via the same type of commands that a remote operator can send ...
>
> the Supervisor retains planning capabilities, and recognizes associated high-level mission objectives (e.g. "Fly Home").
>
> it implements two high-level behaviors, “fly home” and “search and track object”.

#### 摘录 C

- 出处：第 8-9 页，`Fly Home / Search and Track / Abstract System Testing`，`paper_content.txt` 第 468-489 行
> The Fly Home behavior provides the vehicle with the capability of returning autonomously to the starting point of a given mission.
>
> The Search and Track behavior can be used to find and track a moving object on the ground.
>
> In the modelling stage a set of errors can occur ... isolated or unreachable states, as well as, missing or erroneous triggers and guards.
>
> The system with greatest deepness is the Sequence Control System ... This implies 346 test sequences for the Sequence Control System.

### 2. 基于原文整理后的自然语言描述

The VTOL UAV mission manager is organized as a hierarchical sequence controller whose top level distinguishes `Mission Mode` from `Command Mode` and provides global exits to `Mission Controller Off`, `Stand By`, and `Slow Down`. Inside `Mission Mode`, deliberate behaviors are executed one at a time, and each behavior terminates by returning control to `Parse Command`, which reads the next command from the current mission plan. `Command Mode` can be entered from inside `Mission Mode` whenever payload-directed or operator-driven direct commands must override the ordinary mission sequence. Above that layer, a Supervisory Control System observes internal and external events, reacts to data-link loss, and issues higher-level commands such as `Fly Home` or `Search and Track Object` to the sequence layer. The resulting controller is therefore a genuine HSM for onboard UAV mission management rather than a flat list of waypoints or a pure planning framework.

### 3. 逐句溯源

1. 句子 1：The VTOL UAV mission manager is organized as a hierarchical sequence controller whose top level distinguishes `Mission Mode` from `Command Mode` and provides global exits to `Mission Controller Off`, `Stand By`, and `Slow Down`.
   对应摘录：A
2. 句子 2：Inside `Mission Mode`, deliberate behaviors are executed one at a time, and each behavior terminates by returning control to `Parse Command`, which reads the next command from the current mission plan.
   对应摘录：A
3. 句子 3：`Command Mode` can be entered from inside `Mission Mode` whenever payload-directed or operator-driven direct commands must override the ordinary mission sequence.
   对应摘录：A
4. 句子 4：Above that layer, a Supervisory Control System observes internal and external events, reacts to data-link loss, and issues higher-level commands such as `Fly Home` or `Search and Track Object` to the sequence layer.
   对应摘录：B, C
5. 句子 5：The resulting controller is therefore a genuine HSM for onboard UAV mission management rather than a flat list of waypoints or a pure planning framework.
   对应摘录：A, B, C
