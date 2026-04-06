# Synthesis of Self-Checking Circuits for Train Route Traffic Control at Intermediate Stations with Control of Calculations Based on Weight-Based Sum Codes - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然落脚在自检 FPGA 实现，但 route preparation / route locking / protective / pre-failure 的状态表、输入输出向量和 `6 s` 释放规则都足够具体，可稳定形成铁路联锁正例。

## 条目 1: Route preparation-locking-protection controller with pre-failure states

- 控制对象：中间站列车进路控制中的 route preparation / locking / protection 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路中间站进路控制状态机，用 departure/destination、股道占用、道岔位置和锁闭状态决定进路准备、锁闭、信号开放以及 protective state 转移。
- 判断：算。对象是真实联锁主控制链，不是纯形式化编码技巧；原文给出了 route 概念、进路表、状态表、保护态与 `6 s` 释放规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-3 页，Abstract / Section `2 Research Objective`
> Unlike existing solutions, this proposal considers the pre-failure states of railway automation and remote control units during the finite-state machine synthesis stage.
>
> A = <X, S, Z, S1, φ, χ>
>
> Φ is a set of efficient and serviceable states, Ψ is a set of pre-failure serviceable states, Ω is a set of inoperable protective states, and ∆ is a set of inoperable dangerous states.

#### 摘录 B

- 出处：第 4-6 页，Section `4 Requirements for the Operating Logic of Railway Trackside Equipment`
> When setting a route, the navigation and security switches are locked to exclude conflicting (secant) routes. Once the route is locked, a permissive indication is activated at the signal that locks the route.
>
> There are only 12 train routes and 12 shunting routes for the station shown in Figure 1. Each route can be defined as a system state in which control signals are transmitted to trackside automation equipment and remote control mechanical devices.
>
> The first section in the train route is released when the approach section is released, this section is occupied, the next section is occupied, and this section is released and remains free for at least 6 s.

#### 摘录 C

- 出处：第 7-8 页，Section `5 Principles of Forming the Transition Graph for an FSM`
> For each individual route, a graph is created that includes the following states:
> - Initial state
> - Route preparation state
> - Route locking state
> - Protective state
> - A state of the system in which one or more of the control devices go into a pre-failure state.
>
> Table 4 shows the system states when the route is locked in an even bottleneck.

#### 摘录 D

- 出处：第 8-13 页，Table 4 / Section `6 FPGA-Based FSM Synthesis`
> Q1 — The route is released
>
> Q2...Q13 — Route track preparation
>
> Q14...Q25 — Route locking
>
> Q26 — Protective state
>
> The operation of the FSM during the route setting, locking, and return to the initial state is demonstrated in Figure 5.
>
> the transition of the system to a protective state is also possible when setting a route. A route's switch losing control serves as an example.

### 2. 基于原文整理后的自然语言描述

The railway station controller is modeled as an FSM-based route-control system whose inputs include route type, departure point, destination point, section occupancy, switch positions, and switch-locking conditions, and whose outputs are switch states plus the permissive or forbidding aspects of the governing signals. In the operating logic, every train or shunting route becomes a system state candidate: setting a route first prepares the route, then locks the required switches and sections to exclude conflicting routes, and only after those safety conditions are satisfied does the controller activate the permissive signal for that route. The transition-graph construction rule explicitly requires an `initial` state, a `route preparation` state, a `route locking` state, a `protective` state, and additional pre-failure states whenever one or more controlled devices degrade. For the example intermediate station, the state table instantiates this pattern as `Q1` for released, `Q2-Q13` for route preparation, `Q14-Q25` for route locking, and `Q26` for the protective state. Route release is not instantaneous: after train movement, the first section is only released when the approach and next-section occupancy conditions have been seen and the relevant section remains free for at least `6 s`, while inconsistent input data or a switch losing control during route establishment can force the FSM into the protective state before later returning to the initial released state.

### 3. 逐句溯源

1. 句子 1：The railway station controller is modeled as an FSM-based route-control system whose inputs include route type, departure point, destination point, section occupancy, switch positions, and switch-locking conditions, and whose outputs are switch states plus the permissive or forbidding aspects of the governing signals.
   对应摘录：A, D
2. 句子 2：In the operating logic, every train or shunting route becomes a system state candidate: setting a route first prepares the route, then locks the required switches and sections to exclude conflicting routes, and only after those safety conditions are satisfied does the controller activate the permissive signal for that route.
   对应摘录：B, C
3. 句子 3：The transition-graph construction rule explicitly requires an `initial` state, a `route preparation` state, a `route locking` state, a `protective` state, and additional pre-failure states whenever one or more controlled devices degrade.
   对应摘录：A, C
4. 句子 4：For the example intermediate station, the state table instantiates this pattern as `Q1` for released, `Q2-Q13` for route preparation, `Q14-Q25` for route locking, and `Q26` for the protective state.
   对应摘录：D
5. 句子 5：Route release is not instantaneous: after train movement, the first section is only released when the approach and next-section occupancy conditions have been seen and the relevant section remains free for at least `6 s`, while inconsistent input data or a switch losing control during route establishment can force the FSM into the protective state before later returning to the initial released state.
   对应摘录：B, D
