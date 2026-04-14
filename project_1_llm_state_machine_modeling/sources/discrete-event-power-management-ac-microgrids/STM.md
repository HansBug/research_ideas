# A Discrete-Event Based Power Management System Framework for AC Microgrids - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `AC microgrid` 的 `BESS / Genset / WT / PV / loads` 全部抽象成离散事件对象，再用并行的 decentralized supervisors 实现 `grid-connected / islanded / peak shaving / voltage support / load shedding`，能够稳定支撑双 A 样本。

## 条目 1: Decentralized AC-microgrid service supervisor

- 控制对象：过程与环境控制领域的 `AC microgrid` 功率管理监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `BESS + Genset + WT + PV + critical/noncritical loads` 的离散事件功率管理监督器，用分布式 supervisor 协调并网/离网、峰值削减、电压支撑与负载切除。
- 判断：算。对象是真实微电网的 PMS，原文不仅给出组件状态机和规格自动机，还把 reduced supervisors 显式落成了 `Stateflow` 可执行状态机，包含离散状态、事件、guard 和输出命令。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 43-53 行
> This paper presents a practical framework for the design and real-time implementation of a Power Management System (PMS) for microgrids based on Supervisory Control Theory (SCT) for discrete-event systems. A detailed step-by-step methodology is provided, which covers the entire process from defining discrete events, modeling microgrid components, synthesizing supervisory controllers, and realizing them in MATLAB (R2024b) Stateflow. This methodology is applied to a case study ... Unlike previous works ... the proposed PMS addresses the following functionalities: (i) grid-connected and islanded operation; (ii) peak shaving; (iii) voltage support; (iv) load shedding.

#### 摘录 B

- 出处：第 7-8 页，`3.2 Model Microgrid Components` 与 Table 3，`paper_content.txt` 第 338-350、780-788 行
> The second step of the methodology is to model the n plant components (DERs) as automata Gi. Each operational mode is described as a state within the automaton ... the behavior of a BESS can be abstracted into operational modes corresponding to three distinct states: (i) Standby; (ii) Charging; (iii) Discharging ...
>
> The BESS operating model is designed for taking into account charging, discharging and standby mode without power injection.
>
> G3: Genset ... 1: Genset at standby mode 2: Genset at nominal mode ... The Genset is modeled with two states and two events.

#### 摘录 C

- 出处：第 17-18 页，`4.4 Specifications` 与 `3.5 PMS Supervisors Realization in MATLAB Stateflow`，`paper_content.txt` 第 383-405、914-956 行
> The final step of the methodology involves the creation of reduced decentralized supervisors ZR_i, which are computed in the last step as state machines in MATLAB Stateflow.
>
> If the SOC falls below the LL level, then Genset must inject nominal power into the microgrid to recharge the BESS. Since SOC returns to normal range, Genset is lead to Standby mode ...
>
> If the voltage at the POI falls within the low limit (L), the voltage support function of the WT system must be activated ... If the POI voltage drops below the Low Low Level (LL), the Genset must operate at its nominal mode ...
>
> When the user enables the peak shaving function ... If the grid power is at a low level (L) ... the BESS must start charging ... When the grid power is at a high level (H) ... the BESS must go to discharge mode. If the grid power is in the normal range (N) ... the BESS must go to standby mode.

### 2. 基于原文整理后的自然语言描述

The proposed PMS treats the AC microgrid as a discrete-event plant composed of `BESS`, `Genset`, `WT`, `PV`, breakers, and controllable load connections, and models each subsystem as an automaton with explicit operating states. In the resulting supervisor, the `BESS` itself switches among `Standby`, `Charging`, and `Discharging`, while the `Genset` switches between `Standby` and `Nominal`, and the wind system changes between constant-power-factor and voltage-support operation. On top of those component machines, decentralized supervisors run in parallel and observe discretized measurements such as `SOC_LL / SOC_L / SOC_N / SOC_H` and `V_L / V_LL / V_N` to enforce service-level policies. Low-SOC management starts the generator in nominal mode and keeps the system there until the battery returns to the normal band; voltage-support management first activates wind-turbine support and then escalates to nominal generator support when the POI voltage falls below the low-low region. Peak-shaving management adds a third rule set that charges the battery when contracted grid power is low, discharges it when grid power is high, and returns it to standby in the normal band. The supervisors are finally realized as executable `Stateflow` state machines, so the paper exposes not only state names but also the discrete events and output commands that drive the microgrid.

### 3. 逐句溯源

1. 句子 1：The proposed PMS treats the AC microgrid as a discrete-event plant composed of `BESS`, `Genset`, `WT`, `PV`, breakers, and controllable load connections, and models each subsystem as an automaton with explicit operating states.
   对应摘录：A, B
2. 句子 2：In the resulting supervisor, the `BESS` itself switches among `Standby`, `Charging`, and `Discharging`, while the `Genset` switches between `Standby` and `Nominal`, and the wind system changes between constant-power-factor and voltage-support operation.
   对应摘录：B, C
3. 句子 3：On top of those component machines, decentralized supervisors run in parallel and observe discretized measurements such as `SOC_LL / SOC_L / SOC_N / SOC_H` and `V_L / V_LL / V_N` to enforce service-level policies.
   对应摘录：A, C
4. 句子 4：Low-SOC management starts the generator in nominal mode and keeps the system there until the battery returns to the normal band; voltage-support management first activates wind-turbine support and then escalates to nominal generator support when the POI voltage falls below the low-low region.
   对应摘录：C
5. 句子 5：Peak-shaving management adds a third rule set that charges the battery when contracted grid power is low, discharges it when grid power is high, and returns it to standby in the normal band.
   对应摘录：C
6. 句子 6：The supervisors are finally realized as executable `Stateflow` state machines, so the paper exposes not only state names but also the discrete events and output commands that drive the microgrid.
   对应摘录：A, C
