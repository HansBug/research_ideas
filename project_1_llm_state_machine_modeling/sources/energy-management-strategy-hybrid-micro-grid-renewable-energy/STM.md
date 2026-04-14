# Energy management strategy for a hybrid micro-grid system using renewable energy - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把混合微电网 EMS 明确实现为 Stateflow 逻辑系统，围绕 `PG/PL/SOC/utility availability` 给出四个运行情形和对应输出，细节足够形成高质量过程控制样本。

## 条目 1: Four-Scenario Micro-Grid EMS with SOC-Governed Battery Switching

- 控制对象：混合微电网的能量管理控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个为 `PV + wind + battery + diesel + utility grid` 混合微电网分配供能路径的 EMS，用总发电功率、负载需求、SOC 阈值和并网可用性决定电池、并网和柴油机的切换。
- 判断：算。对象是真实能量管理控制器，不是纯优化框架；原文给出四种情形、具体不等式、SOC `20%/100%` 阈值、Stateflow ON/OFF 语义和 utility/diesel 切换规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 17-27 行
> The main objective of this work was to develop an energy management strategy that controls the flow of energy between the hybrid micro-grid system and the load connected directly as well as the load connected to the utility grid using MATLAB/Simulink software.
>
> The second objective was to control the charging and discharging of the battery.
>
> ... this algorithm ensures the state of charge (SOC) of battery to remain in the admissible limits (between 20 and 100%).

#### 摘录 B

- 出处：第 8-9 页，`3 Energy management strategy for the developed hybrid micro-grid`，`paper_content.txt` 第 279-323 行
> When there was an excess of power generation, the battery was charged; when there was not enough power generation to meet the load demand, the battery was discharged.
>
> According to the developed energy management system (EMS), the power generation was supplied the load demand through four scenarios ...
>
> Case 2: ... the surplus was used to charge the battery. ... until its SOC reached the maximum value.
>
> Case 3: ... the battery was discharged until its SOC reached the minimum point.
>
> Case 4: When the battery reached its minimum value ... the load demand was provided by the help of the generator or the utility grid based on the availability of the utility grid.
>
> (10) SOC≤20%=Charge battery
>
> (11) SOC>20%=Discharge battery

#### 摘录 C

- 出处：第 10 页，`4 Simulation results`，`paper_content.txt` 第 327-347 行
> ... when the utility grid was not available, then the diesel generator was switched on to supply the load.
>
> ... it was specified that the battery could be charged when the available power was ≥ 20% of the total production ...
>
> The Stateflow logical programming environment was used to design the energy management system algorithm.
>
> The operational mode of Stateflow environment refers to a logical system that can be either 0 or 1. When the output of the flow chart reads 1, it signifies the system is operational (ON), and when it reads 0, it means the system is OFF.

### 2. 基于原文整理后的自然语言描述

The hybrid micro-grid EMS is modeled as a Stateflow-based EFSM that continuously compares total generated power `PG`, load demand `PL`, battery state of charge, and utility-grid availability to choose one of four operating scenarios. When renewable generation is sufficient, the controller supplies the load directly, and if generation exceeds demand it routes the surplus into the battery until SOC reaches `100%`, after which excess power is exported to the utility grid. When generation drops below demand while SOC remains above the minimum threshold, the EMS discharges the battery to support the load and keeps doing so until SOC falls to `20%`. Once the battery reaches that minimum value, the controller disconnects the battery and hands the load to the utility grid when the grid is available or switches on the diesel generator when the grid is unavailable. The same logic also specifies that low-SOC recovery charging is only allowed when renewable output is at least `20%` of total production, and every subsystem output is represented in Stateflow as an explicit `ON/OFF` logical state.

### 3. 逐句溯源

1. 句子 1：The hybrid micro-grid EMS is modeled as a Stateflow-based EFSM that continuously compares total generated power `PG`, load demand `PL`, battery state of charge, and utility-grid availability to choose one of four operating scenarios.
   对应摘录：A, B, C
2. 句子 2：When renewable generation is sufficient, the controller supplies the load directly, and if generation exceeds demand it routes the surplus into the battery until SOC reaches `100%`, after which excess power is exported to the utility grid.
   对应摘录：B
3. 句子 3：When generation drops below demand while SOC remains above the minimum threshold, the EMS discharges the battery to support the load and keeps doing so until SOC falls to `20%`.
   对应摘录：A, B
4. 句子 4：Once the battery reaches that minimum value, the controller disconnects the battery and hands the load to the utility grid when the grid is available or switches on the diesel generator when the grid is unavailable.
   对应摘录：B, C
5. 句子 5：The same logic also specifies that low-SOC recovery charging is only allowed when renewable output is at least `20%` of total production, and every subsystem output is represented in Stateflow as an explicit `ON/OFF` logical state.
   对应摘录：B, C
