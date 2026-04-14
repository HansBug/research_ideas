# Finite state machine control for aircraft electrical distribution system - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无显式时间约束）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把飞机电气分配系统在发电机故障下的重构逻辑写成了 `SOC + 负载功率` 驱动的五态控制链，并明确给出各状态的供电、充电与 shedding 作用。

## 条目 1: Five-state EPS reconfiguration supervisor under generator fault

- 控制对象：航空航天与飞行/空管控制领域的飞机电气分配系统重构与 shedding 监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无显式时间约束）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是更电飞机 `EPS` 的重构控制链，依据负载功率请求和电池 `SOC` 选择 `STATE 1-5`，并决定电池充放电、非关键负载切除和接触器切换。
- 判断：算。对象是具体飞机电力分配控制器，原文没有停留在电网概述，而是给出 `FSM + LTL/Stateflow` 控制逻辑、输入输出变量、五态定义以及发电机故障后的状态切换行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`4 Logic description`，`paper_content.txt` 第 148-178 行
> A third method, based on finite state machine (FSM) in combination with knowledge-based method and LTL is proposed in the next section.
>
> From the previous section, it is possible to understand that the EPS can be seen as a reactive system ... the use of FSM is considered as a suitable solution to improve the EPS management.
>
> In an FSM, the behaviour of the system can be modelled as a set of states and transitions between states ... The simulations have been performed in the Simulink environment, through the use of the Stateflow function, which combines FSM and LTL operations.

#### 摘录 B

- 出处：第 3 页，`5 From the theory to the model`，`paper_content.txt` 第 181-223 行
> The system that has been built and simulated represents a de-icing and avionics system of a civil aircraft.
>
> The model is composed of a series of resistors ... while the avionics is represented by vital loads (V) and non-essential loads (N) that can be disconnected in case of emergency. In parallel, a high-voltage battery is connected through a bi-directional power electronic boost converter.
>
> a set of input variables will be defined ... and a set of output variables ... will show the states of the system (configurations), and the condition that needs to be applied to pass from a state to another.
>
> After the fault, the system moves to the STATE 3 ... the logic calculates the value of the power that the battery has to deliver in order to help the generator ... The STATE 5 is implemented when the power request is ≥115 kW. In this case the logic will apply the Shedding ... the system ... shifts to the STATE 1, or ... to the STATE 4.

#### 摘录 C

- 出处：第 4-5 页，`Table 1 Logic operations of the system / 6 EPS control simulations`，`paper_content.txt` 第 243-285 行
> Table 1 shows how the behaviour of the EPS depends on the requested power from the load `PL` and the state of charge (SOC) of the battery...
>
> `STATE 1`: generator is supplying the loads and charging the battery.
>
> `STATE 2`: generator is supplying the loads. The battery is disconnected.
>
> `STATE 3`: generator and the battery are supplying the loads.
>
> `STATE 4`: generator is supplying the loads and charging the battery. The shedding is activated.
>
> `STATE 5`: generator and the battery are supplying the loads. The shedding is activated.
>
> From 200 to 400 s ... the control systems move to `STATE 5`, using the battery to help the generator until the lower limit of the SOC, and once the battery is discharged the system moves to the `STATE 4`.

### 2. 基于原文整理后的自然语言描述

The paper models the aircraft electrical power system as a reactive EFSM in Stateflow where the controller monitors requested load power and battery `SOC` to choose an EPS configuration. The controlled plant is an `HV270DC` de-icing and avionics network with generators, vital/non-essential loads, contactors, and a bidirectional battery converter. After a generator fault the logic first moves to `STATE 3` when the battery assists the generator, changes to `STATE 5` when demand reaches the high-power region and shedding must be activated, and later falls back to `STATE 1` or `STATE 4` depending on surplus power and low `SOC`. Table 1 defines the five states explicitly as charging-only, battery-disconnected, battery-assist, charge-with-shedding, and assist-with-shedding configurations. Because state selection is driven by continuous power and `SOC` variables while the controlled electrical network still has continuous power-flow dynamics, the case is best treated as a `T0` EFSM with continuous coupling.

### 3. 逐句溯源

1. 句子 1：The paper models the aircraft electrical power system as a reactive EFSM in Stateflow where the controller monitors requested load power and battery `SOC` to choose an EPS configuration.
   对应摘录：A, B
2. 句子 2：The controlled plant is an `HV270DC` de-icing and avionics network with generators, vital/non-essential loads, contactors, and a bidirectional battery converter.
   对应摘录：B
3. 句子 3：After a generator fault the logic first moves to `STATE 3` when the battery assists the generator, changes to `STATE 5` when demand reaches the high-power region and shedding must be activated, and later falls back to `STATE 1` or `STATE 4` depending on surplus power and low `SOC`.
   对应摘录：B, C
4. 句子 4：Table 1 defines the five states explicitly as charging-only, battery-disconnected, battery-assist, charge-with-shedding, and assist-with-shedding configurations.
   对应摘录：C
5. 句子 5：Because state selection is driven by continuous power and `SOC` variables while the controlled electrical network still has continuous power-flow dynamics, the case is best treated as a `T0` EFSM with continuous coupling.
   对应摘录：B, C
