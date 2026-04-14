# State Transitions Logical Design for Hybrid Energy Generation with Renewable Energy Sources in LNG Ship - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 LNG 船混合供能 EMS 的输入变量、输出变量、12 个有限状态以及每个状态的守卫条件和行为说明，足以直接形成一条高细节 EFSM 样本。

## 条目 1: Twelve-State EMS for LNG-Ship Hybrid Power Dispatch
- 控制对象：LNG 船混合供能系统的能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 LNG 船电力系统的 EMS，用于根据 `PL / Ppv / Pw / SoC / eng*_Pmax` 等输入在 12 个状态之间切换，并调度 RES、LNG、DG1、DG2 与电池的供能顺序。
- 判断：算。对象是实际船舶供能控制器，原文不是泛泛讨论能量管理，而是把状态、输入、输出、守卫条件与各状态动作写成了完整的 FSM 逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 34-47
> This paper presents a new control method to balance LNG ship load demands and power generation from RES ... The Energy Management System (EMS) is designed and implemented in a Finite State Machine structure using the logical design of state transitions.

#### 摘录 B
- 出处：第 8-10 页，Section 3 `Control System for Energy Management`，行 423-468
> The EMS controls the operation of ships’ power system modules PVs, WECs, LNG, DGs, Batteries, vs. time, applying commands for cut-in and cut-out of the generating units and loads ... The EMS is designed and implemented in a Finite State Machine FSM structure ... The EMS receives the input variables (Table 1), connects, or disconnects the generating units, and upon call completion returns the output variables (Table 2).
>
> Electric power demands are met by setting levels and conditions for decisions for transitions between finite states ... We identified 12 (twelve) finite states.

#### 摘录 C
- 出处：第 10-12 页，Table 3 `EMS States and Transitions` / Section 3.3，行 530-675
> State 1_1 ... `Ppv + Pw ≥ PL` and `SoC < 0.95` ... all ship power demands are covered from RES ... residual power from RES is directed for batteries charging.
>
> State 2_1 ... `Ppv + Pw < PL`, `eng3_Pmax > PL - Ppv - Pw`, `SoC > 0.5` ... missing power can be covered by LNG engine (standby for activation) ... EMS assigns missing power on batteries discharge.
>
> State 2_2 ... `SoC < 0.5` ... activates LNG engine and requests an additional amount of power `Pgmax / 5` for batteries charging.
>
> State 2_7 ... all internal engines are insufficient ... this state is illegal and shall never occur ... lack of power is covered from batteries discharge.
>
> Transition between states happens according to defined logical conditions based on the level of power demands and available power generation.

### 2. 基于原文整理后的自然语言描述

The LNG-ship EMS is an EFSM whose inputs include load demand `PL`, renewable contributions `Ppv` and `Pw`, engine capacity bounds `eng1_Pmax / eng2_Pmax / eng3_Pmax`, and battery state of charge `SoC`, and whose outputs request power from `DG1`, `DG2`, `LNG`, battery discharge, battery charging, or spare dissipation. The controller enumerates twelve finite states and uses guard conditions over demand, generation, and battery thresholds to decide which power sources are enabled. In `State 1_1` and `State 1_2`, renewable power already covers the ship load, so the EMS either charges the battery if `SoC < 0.95` or marks the residual renewable power as spare once the battery is sufficiently full. In `State 2_1` to `State 2_6`, the EMS escalates through a prioritized dispatch chain: it first checks whether renewables plus battery discharge suffice, then activates LNG, then adds `DG1`, then adds `DG2`, and when `SoC < 0.5` it requests extra generation margins to recharge the battery while serving the load. `State 2_7` is the illegal overload state in which even all thermal units plus RES are insufficient, and the paper explicitly treats it as a never-should-happen completion state of the machine.

### 3. 逐句溯源

1. 句子 1：The LNG-ship EMS is an EFSM whose inputs include load demand `PL`, renewable contributions `Ppv` and `Pw`, engine capacity bounds `eng1_Pmax / eng2_Pmax / eng3_Pmax`, and battery state of charge `SoC`, and whose outputs request power from `DG1`, `DG2`, `LNG`, battery discharge, battery charging, or spare dissipation.
   对应摘录：A, B
2. 句子 2：The controller enumerates twelve finite states and uses guard conditions over demand, generation, and battery thresholds to decide which power sources are enabled.
   对应摘录：B, C
3. 句子 3：In `State 1_1` and `State 1_2`, renewable power already covers the ship load, so the EMS either charges the battery if `SoC < 0.95` or marks the residual renewable power as spare once the battery is sufficiently full.
   对应摘录：C
4. 句子 4：In `State 2_1` to `State 2_6`, the EMS escalates through a prioritized dispatch chain: it first checks whether renewables plus battery discharge suffice, then activates LNG, then adds `DG1`, then adds `DG2`, and when `SoC < 0.5` it requests extra generation margins to recharge the battery while serving the load.
   对应摘录：C
5. 句子 5：`State 2_7` is the illegal overload state in which even all thermal units plus RES are insufficient, and the paper explicitly treats it as a never-should-happen completion state of the machine.
   对应摘录：C
