# Fuzzy State Machine Energy Management Strategy for Hybrid Electric UAVs with PV/Fuel Cell/Battery Power System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `PV / fuel cell / battery` 的优先级、`5` 个离散状态和 `SOC + Pd` 驱动的模糊输出都写得很完整，是一条标准的混合供能 `EFSM` 样本。

## 条目 1: Five-State PV-FC-Battery EMS with Fuzzy Fuel-Cell Dispatch

- 控制对象：混合电动无人机的光伏-燃料电池-电池能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `PV + FC + B` 混合动力无人机的在线能量管理状态机，用 `PpvMax`、`PD`、`Pd`、`SOC` 和 `Pchrg` 等变量决定光伏、燃料电池和电池之间的功率分配。
- 判断：算。对象是真实 UAV 供能控制器，正文给出了优先级规则、五个离散状态、变量阈值、动作输出和模糊子控制器。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，能量管理目标，`paper_content.txt` 第 106-122 行
> (i) The PV panel has the top priority to discharge.
>
> (ii) The battery ... makes up for surplus demand power.
>
> (iii) The fuel cell generally has the lowest output priority to save the fuel for longer endurance.
>
> (iv) The DC bus demand power is always satisfied by the three kinds of power sources.

#### 摘录 B

- 出处：第 4-5 页，`Implementation of Fuzzy State Machine`，`paper_content.txt` 第 166-192 行
> The FSM strategy used to determine the output of the PV panel and fuel cell has five states.
>
> State 1 ... The PV panel alone is selected to satisfy the power demand.
>
> State 4 ... the fuzzy logical control algorithm is used to decide the desired output of fuel cell PF.
>
> State 5 ... the fuel cell will output the desired power.

#### 摘录 C

- 出处：第 5 页，模糊逻辑输入输出，`paper_content.txt` 第 193-224 行
> The fuzzy logical control has two input variables and one output variable, where the surplus demand power Pd and the state of charge SOC are the input variables and the desired fuel cell power is the output variable.
>
> The battery SOC is categorized into three different statuses called low (L), middle (M), and high (H).

### 2. 基于原文整理后的自然语言描述

The proposed UAV energy manager is an extended state machine that coordinates photovoltaic generation, a fuel cell, and a battery under a fixed priority policy: `PV` is used first, the battery absorbs deficits or fast fluctuations, and the fuel cell is kept as the lowest-priority source to preserve endurance. Its discrete supervisor contains `five` states driven by the relation between `PpvMax`, `PD`, `Pd`, `Pchrg`, and `SOC`. In the first three states, the controller decides whether the PV alone should satisfy the demand, satisfy the demand while charging the battery, or satisfy both the demand and the maximum battery charge limit. In states `4` and `5`, the controller still drives the PV at maximum available power but hands fuel-cell dispatch to a fuzzy sub-controller. That fuzzy layer takes `Pd` and `SOC` as inputs, classifies `SOC` into `low / middle / high`, and outputs the desired fuel-cell power `PF`, while battery power is recovered from the balance equation rather than commanded separately.

### 3. 逐句溯源

1. 句子 1：The proposed UAV energy manager is an extended state machine that coordinates photovoltaic generation, a fuel cell, and a battery under a fixed priority policy: `PV` is used first, the battery absorbs deficits or fast fluctuations, and the fuel cell is kept as the lowest-priority source to preserve endurance.
   对应摘录：A
2. 句子 2：Its discrete supervisor contains `five` states driven by the relation between `PpvMax`, `PD`, `Pd`, `Pchrg`, and `SOC`.
   对应摘录：B, C
3. 句子 3：In the first three states, the controller decides whether the PV alone should satisfy the demand, satisfy the demand while charging the battery, or satisfy both the demand and the maximum battery charge limit.
   对应摘录：B
4. 句子 4：In states `4` and `5`, the controller still drives the PV at maximum available power but hands fuel-cell dispatch to a fuzzy sub-controller.
   对应摘录：B
5. 句子 5：That fuzzy layer takes `Pd` and `SOC` as inputs, classifies `SOC` into `low / middle / high`, and outputs the desired fuel-cell power `PF`, while battery power is recovered from the balance equation rather than commanded separately.
   对应摘录：A, C
