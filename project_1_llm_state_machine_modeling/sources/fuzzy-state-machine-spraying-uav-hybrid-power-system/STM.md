# Energy Management Strategy Based on Fuzzy Logic and State Machine for Spraying UAV Hybrid Power System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把喷洒无人机混合供能 `EMS` 明确写成四态状态机，并把 `hovering` 功率阈值、fuzzy `replenish/discharge` 信号与燃料电池/电池功率分配直接绑定，可稳定抽出 `EFSM + T0` 主链。

## 条目 1: Four-state FC-battery EMS for spraying UAV

- 控制对象：喷洒无人机燃料电池-电池混合供能能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（混合能源管理）

### 0. 条目识别与判定

- 一句话说明：这是一个面向农业喷洒无人机的混合供能 `EMS`，用状态机决定燃料电池独供、电池充电补能和电池放电补峰等模式，并让 fuzzy controller 在高负载时给出电池功率方向与幅值。
- 判断：算。对象是真实无人机混合供能控制器，不是单纯能量优化背景；原文直接给出四个状态、各状态触发条件和燃料电池/电池的功率分工。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-23 行
> Hybrid power systems increase the autonomy of electric vehicles, including UAVs, for agricultural spraying tasks. ... A State Machine and Fuzzy Logic approach accomplishes power control management. ... the simulation results indicate that the state machine facilitates transitions between power sources and, in convergence with fuzzy logic techniques, can adequately control the energy of the UAV and thereby increase the autonomy of operation.

#### 摘录 B

- 出处：第 2 页，Introduction，`paper_content.txt` 第 104-114 行
> Despite the existing literature on UAV energy management, studies on the EMS for spraying UAVs ... still need to be completed. For this reason, the proposal involves designing an EMS by implementing a fuzzy state machine control. This system aims to facilitate proper energy management in a hybrid system that combines a fuel cell and a battery in UAVs. The focus is on ensuring efficient energy management at different stages of UAV operation, considering changing power requirements and characteristics of energy sources ...

#### 摘录 C

- 出处：第 8 页，Section `4.3. State Machine`，`paper_content.txt` 第 690-726 行
> This control strategy operates based on four states:
> State 1: This occurs when the power demand is lower than required for hovering. ... the battery does not need to release or receive energy. Supplying all the necessary power falls entirely on the Fuel Cell.
> State 2: ... a fuzzy logic controller becomes operational when the power demand exceeds the hovering capacity. This controller determines the intensity and direction of the battery Power (Pb). Positive powers indicate discharge ... while negative powers signal recharge ...
> State 3: The fuzzy logic controller issues a replenish signal in this state. Besides fulfilling the Power Demand (PD), the fuel cell must provide additional power to recharge the battery.
> State 4: When the fuzzy logic controller issues a discharge signal, the fuel cell is activated at its maximum power. The battery ... engages to cover the remaining difference ...

### 2. 基于原文整理后的自然语言描述

The spraying-UAV energy-management controller supervises a hybrid fuel-cell and battery powertrain through four discrete operating states tied to the demanded flight power. When demand is below the hovering requirement, the controller stays in `State 1` and assigns the entire load to the fuel cell while the battery neither charges nor discharges. When demand exceeds the hovering threshold, `State 2` activates a fuzzy controller that computes the battery power magnitude and sign, so positive `Pb` discharges the battery and negative `Pb` recharges it. `State 3` corresponds to a replenish command in which the fuel cell must satisfy the current demand and simultaneously charge the battery, whereas `State 4` corresponds to a discharge command in which the fuel cell is driven to maximum power and the battery covers the remaining deficit. The supervisor is therefore an extended state machine rather than a flat mode list, because its transitions depend on continuous power-demand and fuzzy-control signals while its outputs are explicit source-allocation commands to the fuel cell and battery.

### 3. 逐句溯源

1. 句子 1：The spraying-UAV energy-management controller supervises a hybrid fuel-cell and battery powertrain through four discrete operating states tied to the demanded flight power.
   对应摘录：A, B, C
2. 句子 2：When demand is below the hovering requirement, the controller stays in `State 1` and assigns the entire load to the fuel cell while the battery neither charges nor discharges.
   对应摘录：C
3. 句子 3：When demand exceeds the hovering threshold, `State 2` activates a fuzzy controller that computes the battery power magnitude and sign, so positive `Pb` discharges the battery and negative `Pb` recharges it.
   对应摘录：C
4. 句子 4：`State 3` corresponds to a replenish command in which the fuel cell must satisfy the current demand and simultaneously charge the battery, whereas `State 4` corresponds to a discharge command in which the fuel cell is driven to maximum power and the battery covers the remaining deficit.
   对应摘录：C
5. 句子 5：The supervisor is therefore an extended state machine rather than a flat mode list, because its transitions depend on continuous power-demand and fuzzy-control signals while its outputs are explicit source-allocation commands to the fuel cell and battery.
   对应摘录：A, B, C
