# A Sequence and Supervisory Control System for Onboard Mission Management of an Unmanned Helicopter - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 UAV mission management 写成了一个有顶层安全流转、`Mission Mode / Command Mode` 复合状态、truth table 与 mission grammar 约束的 state-chart supervisor，控制链完整且非常适合建模任务。

## 条目 1: Mission-mode / command-mode UAV sequence supervisor

- 控制对象：航空航天与飞行/空管控制领域的 `Mission Mode / Command Mode` 无人直升机任务监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个运行在无人直升机上的 onboard mission-management supervisor，用顶层 state chart 统一管理人工/自动控制切换、任务序列执行、直接命令执行和输入合法性约束。
- 判断：算。对象是实际飞行任务管理控制器，不是纯架构口号；原文直接给出了顶层复合状态、`Stand By / Slow Down / Mission Mode / Command Mode` 流转、任务序列语法约束和 operator overrule 安全链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Overview，`paper_content.txt` 第 8-13 行
> Two main components, a Sequence Control System and a Supervisory Control System, form the Mission Management System ...
>
> Events and commands sent by a remote operator or an onboard component can be integrated into the system ...
>
> Second, a truth table of valid external commands assures that only permitted commands are accepted by the event handling. Finally, a grammar-based plausibility check avoids illegal behavior commands within a mission plan.

#### 摘录 B

- 出处：第 5 页，`4.2 Event-based Model`，`paper_content.txt` 第 228-249 行
> The Sequence Control System is shown in Figure 3. It has two hierarchical levels where the top level models the procedural flow for a safe operation. The two composite states, "Mission Mode" and "Command Mode", model mission plan processing and direct command execution respectively.
>
> ... another idle state "Stand By" lets the UAV hover at its current position ... The state "Slow Down" is necessary to assure a smooth changeover into "Stand By" ...
>
> For each behavior there exists a termination condition which transits into the command parser "Parse Command" ...
>
> The grammar implemented in this context defines production rules ... Its root is defined by "<mission>" which basically enforces every mission to start with a take-off behavior and end with a land.

#### 摘录 C

- 出处：第 7-8 页，Conclusion，`paper_content.txt` 第 288-291 行
> The Mission Management System implements several operational safety features. First, an operator can overrule autonomous actions anytime. Second, the system provides a stand by state which also serves as a fall-back state in case of errors. Third, the user input is checked against plausibility rules using a truth table and an EBNF grammar.
>
> He has the possibility to intercept any running behavior by different kinds of commands ... a single behavior (e.g. land) or a complex behavior command sequence.

### 2. 基于原文整理后的自然语言描述

The retained control object is the top-level Sequence Control System of an unmanned-helicopter mission manager, whose job is to safely mediate between prearranged mission execution and direct operator or onboard commands. At the top layer, the controller distinguishes two composite states, `Mission Mode` for mission-plan processing and `Command Mode` for direct-command execution, while `Stand By` and `Slow Down` provide the safe fallback path for stopping autonomous activity and stabilizing the aircraft before hover. Inside mission execution, each behavior terminates by returning to `Parse Command`, which fetches the next behavior command from the mission plan. That mission plan is itself constrained by an EBNF grammar whose root `<mission>` requires every mission to begin with `take-off` and end with `land`, while a truth table filters the valid external commands. The resulting UAV supervisor is therefore a layered HSM rather than a flat command parser, because mission sequencing, direct control, safe fallback, and input admissibility are all embedded in one state-chart-driven control object.

### 3. 逐句溯源

1. 句子 1：The retained control object is the top-level Sequence Control System of an unmanned-helicopter mission manager, whose job is to safely mediate between prearranged mission execution and direct operator or onboard commands.
   对应摘录：A, B
2. 句子 2：At the top layer, the controller distinguishes two composite states, `Mission Mode` for mission-plan processing and `Command Mode` for direct-command execution, while `Stand By` and `Slow Down` provide the safe fallback path for stopping autonomous activity and stabilizing the aircraft before hover.
   对应摘录：B, C
3. 句子 3：Inside mission execution, each behavior terminates by returning to `Parse Command`, which fetches the next behavior command from the mission plan.
   对应摘录：B
4. 句子 4：That mission plan is itself constrained by an EBNF grammar whose root `<mission>` requires every mission to begin with `take-off` and end with `land`, while a truth table filters the valid external commands.
   对应摘录：A, B
5. 句子 5：The resulting UAV supervisor is therefore a layered HSM rather than a flat command parser, because mission sequencing, direct control, safe fallback, and input admissibility are all embedded in one state-chart-driven control object.
   对应摘录：A, B, C
