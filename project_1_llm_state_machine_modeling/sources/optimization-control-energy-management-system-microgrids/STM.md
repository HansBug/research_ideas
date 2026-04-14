# Optimization and Control of an Energy Management System for Microgrids - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文在 microgrid `EMS` 章节直接给出了 `Grid-connected / Grid-only / Islanding / Synchronization / Outage` 五主模式及其 switch-breaker 状态变量，构成了完整 mode-switch FSM。

## 条目 1: Five-mode microgrid EMS switch-breaker supervisor

- 控制对象：过程与环境控制领域的并网微电网 EMS 模式切换控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 grid-connected microgrid 的中央 EMS controller，用 transfer switch、EMS breaker 和 grid power indicator 的组合状态管理 `grid-connected`、`grid-only`、`islanding`、`synchronization` 和 `outage` 五类运行模式。
- 判断：算。对象是真实微电网模式切换控制器，原文明确写出了 operating modes、switch/breaker state variables 和每个模式的控制职责，而不是只给经济优化结果。

### 1. 原文摘录

#### 摘录 A

- 出处：第 107-109 页，`5.5 Central Control Unit / Controller Implementation`
> In this thesis, the operation of a grid-connected microgrid with EMS is classified into five main operating modes.
>
> Grid-connected mode ... the microgrid operates in grid connected mode.
>
> Grid-only mode ... the controller would open the breaker connecting the EMS to the microgrid.
>
> Islanding mode ... EMS could detect the incident and open the grid transfer switch. The microgrid is isolated from the utility grid.

#### 摘录 B

- 出处：第 109 页，`Controller Implementation`
> Synchronization mode: This is a transition from the islanding to grid connected mode. ... EMS would ensure that the magnitude, frequency and phase of the microgrid and grid are the same.
>
> Outage mode: This system enters this mode when both utility grid and EMS battery packs are out of power. In this mode, the EMS control unit is still active and monitors the system with reserved power.

#### 摘录 C

- 出处：第 109-110 页，`finite state machine controller`
> To implement the above functionality, a finite state machine controller is designed as shown in Figure 5.13. The state variables are the state of utility grid transfer switch, EMS breaker and grid power indicator.
>
> Utility grid transfer switch has three states, Closed(C), Fault opening(F), and Manual opening(M).
>
> The EMS breaker has the same three states. Grid power indicator has two values: Grid has power and stable(Y), grid is power off or unstable(N).

#### 摘录 D

- 出处：第 110 页，`Figure 5.13 state encoding`
> Each blue box in Figure 5.13 represents a state of the microgrid. The three letters represent the state of EMS breaker, grid transfer switch and grid power indicators respectively. For example, CFN means EMS breaker is closed, grid transfer switch is at fault condition and grid has no power. The red circles represent the modes of the system, which include groups of states with similar meaning.

### 2. 基于原文整理后的自然语言描述

The microgrid EMS is not described as a vague priority policy but as a finite state machine controller with five main operating modes: `Grid-connected`, `Grid-only`, `Islanding`, `Synchronization`, and `Outage`. These modes are realized over explicit switch-topology states whose variables are the utility-grid transfer switch, the EMS breaker, and the grid-power indicator, with discrete values such as `C/F/M` for the switches and `Y/N` for grid stability. In `Grid-only`, the controller isolates the EMS path when the battery or inverter is faulty or under service; in `Islanding`, it opens the transfer switch and lets the EMS inverter govern voltage and frequency; in `Synchronization`, it waits until microgrid and utility magnitude, frequency, and phase align before reconnection. `Outage` keeps the control unit alive on reserved power so it can watch for power return and select the proper recovery mode. Because the paper explicitly names both the high-level modes and the underlying configuration states, this is a detailed microgrid mode-switch FSM rather than a generic EMS overview.

### 3. 逐句溯源

1. 句子 1：The microgrid EMS is not described as a vague priority policy but as a finite state machine controller with five main operating modes: `Grid-connected`, `Grid-only`, `Islanding`, `Synchronization`, and `Outage`.
   对应摘录：A, B, C
2. 句子 2：These modes are realized over explicit switch-topology states whose variables are the utility-grid transfer switch, the EMS breaker, and the grid-power indicator, with discrete values such as `C/F/M` for the switches and `Y/N` for grid stability.
   对应摘录：C, D
3. 句子 3：In `Grid-only`, the controller isolates the EMS path when the battery or inverter is faulty or under service; in `Islanding`, it opens the transfer switch and lets the EMS inverter govern voltage and frequency; in `Synchronization`, it waits until microgrid and utility magnitude, frequency, and phase align before reconnection.
   对应摘录：A, B
4. 句子 4：`Outage` keeps the control unit alive on reserved power so it can watch for power return and select the proper recovery mode.
   对应摘录：B
5. 句子 5：Because the paper explicitly names both the high-level modes and the underlying configuration states, this is a detailed microgrid mode-switch FSM rather than a generic EMS overview.
   对应摘录：C, D
