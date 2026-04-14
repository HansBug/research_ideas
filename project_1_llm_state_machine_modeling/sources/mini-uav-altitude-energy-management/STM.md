# A Rule-Based Energy Management Technique Considering Altitude Energy for a Mini UAV with a Hybrid Power System Consisting of Battery and Solar Cell - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把太阳能小型 VTOL UAV 的 rule-based EMS 写成三种功率分配 case，并把 `Ppv / Pload / SOC / Palt` 与飞行模式功率需求连接起来，可作为航空能源管理 EFSM 样本。

## 条目 1: Altitude-aware hybrid-power UAV energy manager

- 控制对象：航空航天与飞行控制领域的小型 VTOL UAV 混合动力能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向太阳能小型 VTOL UAV 的 rule-based energy manager，用太阳能、 battery 和 altitude energy 的可用性来分配飞行功率需求。
- 判断：算。对象是实际 UAV 混合动力系统控制器，原文给出了三种功率管理 case、关键变量 `Ppv / Pload / SOC / Palt`、最高高度约束和飞行模式功率需求来源。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 34-49 行
> In this study, a solar-powered mini VTOL (vertical take-off and landing) UAV with a wingspan of 1.8 m and weight of 3.3 kg is developed and a model of the system consisting of solar cells, a battery, a super capacitor, and a DC/DC converter is created in MATLAB/Simulink software (R2023b). Additionally, state machine control (SMC), a rule-based (RB) energy management strategy (EMS), has been applied to this model. While the power obtained from the sun is divided among the other energy components, the durability of the UAV is increased, and the excess energy is stored as altitude energy to be used when necessary.

#### 摘录 B

- 出处：第 7-8 页，`2.6 Power Management Algorithm`，`paper_content.txt` 第 468-487 行与第 535-548 行
> In this study, the demand power of the solar-powered mini VTOL UAV is shared between the solar cells and battery with rule-based energy management. In other words, the SMC is implemented in this study. Figure 7 shows this energy management algorithm. In addition, the cases of the energy management algorithm are listed below.
>
> Case 1: The maximum power (Ppv) of solar cells is higher than the demand power (Pload). Since the battery state of charge (SOC) is higher than the maximum battery charge, the battery does not need to be charged. Here, excess altitude (Palt) energy can be stored as potential energy. ... the maximum altitude is determined as 25 m.
>
> Case 2: Solar cells power meets demand power. Battery state of charge (SOC) is sufficient.
>
> Case 3: Demand power (Pload) is higher than the maximum power from the solar cells. The solar cells cannot meet the power demand alone; the part lacks solar energy is covered by the battery (Pbatt). When solar energy and battery energy are exhausted, the stored altitude energy (Palt) powers the system.

#### 摘录 C

- 出处：第 8 页，`2.7 Demand Power Calculation` 与 Results，`paper_content.txt` 第 550-583 行
> In Figure 8, the load profile has been drawn for the solar-powered mini VTOL UAV used in the hybrid power system. The thrust power requirement of the UAV depends on the flight modes of UAV, such as takeoff, climb, cruise, endurance, descent, and landing.
>
> Energy management has been applied to the system shown in Figure 1, which consists of an 8 Ah li-po battery, 7 F capacitance supercapacitor, and 107 W power solar cell pack. ... The state machine control function was written with a function block in the Matlab/Simulink environment.

### 2. 基于原文整理后的自然语言描述

The retained controller is a rule-based energy manager for a solar-powered mini VTOL UAV, not a pure aerodynamic sizing calculation. It divides the instantaneous demand power among solar cells, the battery, and altitude energy according to a three-case state-machine strategy. In `Case 1`, if available solar power `Ppv` is greater than load demand `Pload` and the battery `SOC` is already above the maximum charge threshold, the controller avoids charging the battery and stores the surplus as potential altitude energy up to the `25 m` altitude limit. In `Case 2`, when solar power meets the demanded power and the battery charge is sufficient, the controller keeps the system supplied without invoking the battery or altitude-energy fallback. In `Case 3`, when `Pload` exceeds available solar power, the deficit is first covered by battery power `Pbatt`, and if both solar and battery energy are exhausted, stored altitude energy `Palt` powers the system. Because the demanded load profile is calculated from UAV flight modes such as takeoff, climb, cruise, endurance, descent, and landing, the result is an EFSM-like hybrid-power supervisor driven by flight-phase power demand and continuous energy variables.

### 3. 逐句溯源

1. 句子 1：The retained controller is a rule-based energy manager for a solar-powered mini VTOL UAV, not a pure aerodynamic sizing calculation.
   对应摘录：A, B
2. 句子 2：It divides the instantaneous demand power among solar cells, the battery, and altitude energy according to a three-case state-machine strategy.
   对应摘录：A, B
3. 句子 3：In `Case 1`, if available solar power `Ppv` is greater than load demand `Pload` and the battery `SOC` is already above the maximum charge threshold, the controller avoids charging the battery and stores the surplus as potential altitude energy up to the `25 m` altitude limit.
   对应摘录：B
4. 句子 4：In `Case 2`, when solar power meets the demanded power and the battery charge is sufficient, the controller keeps the system supplied without invoking the battery or altitude-energy fallback.
   对应摘录：B
5. 句子 5：In `Case 3`, when `Pload` exceeds available solar power, the deficit is first covered by battery power `Pbatt`, and if both solar and battery energy are exhausted, stored altitude energy `Palt` powers the system.
   对应摘录：B
6. 句子 6：Because the demanded load profile is calculated from UAV flight modes such as takeoff, climb, cruise, endurance, descent, and landing, the result is an EFSM-like hybrid-power supervisor driven by flight-phase power demand and continuous energy variables.
   对应摘录：C
