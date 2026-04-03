# Stateflow-Based Energy Management Strategy for Hybrid Energy System to Mitigate Load Shedding - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、层次、并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合能源系统的 EMS 明确建成 Stateflow 层次状态机，并给出了 `Grid_Connected_Mode / Islanded_Mode` 及其子状态、守卫条件和每小时定时迭代逻辑。

## 条目 1: Grid-Connected vs Islanded HES Operation in Stateflow
- 控制对象：面向负荷削减场景的混合能源系统能量管理器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、层次、并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个带电网、光伏、储能和柴油机的混合能源系统 EMS，用于在 `Grid_Connected_Mode` 与 `Islanded_Mode` 间切换，并在负荷削减时按 SOC 和供电缺口调度 PV、ESU 与发电机。
- 判断：算。对象是实际能源控制系统，原文明确给出 super-state、child-state、AND/OR 组合、CFT 守卫条件、每小时时步和 inter-state / intra-state 转移语义。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 48-59
> This study investigates the potential application of Stateflow (SF) to design an energy management strategy (EMS) for a renewable-based hybrid energy system (HES). The SF is an extended finite state machine ... The HES comprises photovoltaics (PV), energy storage units (ESU) and a diesel generator (Gen), integrated with the power grid that experiences a regular load shedding condition ... The EMS optimizes the energy production and utilization during both modes of HES operation, i.e., grid-connected mode and the islanded mode.

#### 摘录 B
- 出处：第 6-7 页，Section 2.3 `Implementing EMS Using STATEFLOW`，行 272-316
> The EMS controls the energy flow among different sources, i.e., PV, ESU, and Gen, with the load ... The HES can be modeled in SF where the states represent different modes of operation for HES.
>
> The state diagram is hierarchical with both AND and OR compositions ... The HES_Operation ... has OR composition with two child states: Grid_Connected_Mode and Islanded_Mode ... Grid_Connected_Mode has AND composition of two child-states, i.e., PV_Mode and the Grid_Mode, whereas the Islanded_Mode contains two child states, RES_Mode and Gen_Mode, with OR composition.
>
> The chart utilizes two types of transitions: inter-state and the intra-state ... It has a temporal logic operator (timer) to represent the for-loop construct.

#### 摘录 C
- 出处：第 12-14 页，Section 4 `Execution of SF Chart and Operation Modes of HES` / Table 3，行 482-567
> Initially, the SF chart ... defaults into Grid_Connected_Mode. Due to the AND composition, its child-states PV_Mode and Grid_Mode are executed simultaneously ...
>
> if P_Grid = 0 is valid, the inter-state transition is activated ...
>
> During the inter-state transition, the event load_shedding is broadcasted, and therefore, the state Islanded_Mode becomes active ...
>
> if PV power is available, it is used to charge the ESU and contribute to the load ... If SOCC < SOCU, charging the ESU is the first priority ...
>
> The Islanded_Mode is triggered when load shedding occurs ... the load demand is met either by the ESU and PV, or if necessary, using a diesel generator ...
>
> Islanded_Mode / RES_Mode: `P_PV + P_ESU > P_Load`
>
> Islanded_Mode / Gen_Mode: `P_PV + P_ESU < P_Load`

### 2. 基于原文整理后的自然语言描述

The hybrid-energy-system EMS is modeled in Stateflow as a hierarchical chart whose root state `HES_Operation` switches between `Grid_Connected_Mode` and `Islanded_Mode`. `Grid_Connected_Mode` is the default state and contains parallel child behavior for `PV_Mode` and `Grid_Mode`, so PV power can be routed either to the ESU or to the load while grid surplus can also charge the ESU. When the guard `P_Grid = 0` becomes true, an inter-state transition broadcasts `load_shedding` and activates `Islanded_Mode`, whereas the ordinary hourly loop otherwise re-enters `Grid_Connected_Mode` through the timer-driven intra-state transition. Inside `Islanded_Mode`, the controller chooses between `RES_Mode` and `Gen_Mode` according to whether `P_PV + P_ESU` is greater than or less than `P_Load`, and it then further dispatches PV, ESU, `Gen1`, and `Gen2` to keep the load energized. The chart therefore combines mode switching, SOC-dependent charging priority, parallel child execution, and explicit per-hour temporal iteration in one HSM controller.

### 3. 逐句溯源

1. 句子 1：The hybrid-energy-system EMS is modeled in Stateflow as a hierarchical chart whose root state `HES_Operation` switches between `Grid_Connected_Mode` and `Islanded_Mode`.
   对应摘录：A, B
2. 句子 2：`Grid_Connected_Mode` is the default state and contains parallel child behavior for `PV_Mode` and `Grid_Mode`, so PV power can be routed either to the ESU or to the load while grid surplus can also charge the ESU.
   对应摘录：B, C
3. 句子 3：When the guard `P_Grid = 0` becomes true, an inter-state transition broadcasts `load_shedding` and activates `Islanded_Mode`, whereas the ordinary hourly loop otherwise re-enters `Grid_Connected_Mode` through the timer-driven intra-state transition.
   对应摘录：B, C
4. 句子 4：Inside `Islanded_Mode`, the controller chooses between `RES_Mode` and `Gen_Mode` according to whether `P_PV + P_ESU` is greater than or less than `P_Load`, and it then further dispatches PV, ESU, `Gen1`, and `Gen2` to keep the load energized.
   对应摘录：A, C
5. 句子 5：The chart therefore combines mode switching, SOC-dependent charging priority, parallel child execution, and explicit per-hour temporal iteration in one HSM controller.
   对应摘录：B, C
