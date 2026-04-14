# Microgrid Operation With Load Shedding and Battery Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把微电网的优先级负荷切除与重连逻辑实现成了带 `undervoltage / reset / clock / delay / reconnect threshold` 的 Moore FSM，状态和 I/O 都足够具体。

## 条目 1: Moore load-shedding controller with undervoltage delay and reconnect

- 控制对象：过程与环境控制领域的微电网优先级负荷切除与重连控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是微电网 `load shedding scheme` 的主控制器，按 bus undervoltage、reset、clock 和 breaker close 条件决定何时切除最低优先级负载、何时延时重测、何时重连。
- 判断：算。对象是具体微电网保护/恢复控制器，原文明确说明 `Moore FSM` 结构、输入输出、时钟触发、idle state、delay、重连阈值和最高优先级负载保留策略。

### 1. 原文摘录

#### 摘录 A

- 出处：第 26-27 页，`Chapter 4`，`paper_content.txt` 第 2920-2994 行
> A Finite State Machine (FSM) was chosen ... A Moore FSM was selected and designed with two inputs and five outputs.
>
> The first input comes from either the main system as an undervoltage signal or from the energy storage system when the backup batteries are unable to meet the demand of the microgrid. The second input is a reset signal that will set all the outputs to their default position.
>
> The FSM was created inside a program Simulink ... The current state and next state logic connect via a resettable flip-flop ... The flip-flop operates on an external clock/pulse-generator.

#### 摘录 B

- 出处：第 28-29 页，`Figure 4.1 / Chapter 4 Summary`，`paper_content.txt` 第 3121-3168、3455-3460 行
> The first problem is that the load shedding scheme would shed loads based off a priority list. The second problem is that it would shed load only after bus voltages had fallen below a certain tolerance level. The third problem is that once a load has been shed, a delay needs to be implemented so a false load shed signal is not sent ...
>
> Once a load has been shed a delay is asserted before bus voltages are measured again.
>
> We want this controller program to measure voltage and if the bus voltages fall below a set tolerance level then shed the lowest priority load on the list of loads. It should then delay before it measures bus voltages again so a false trip signal is not sent.

#### 摘录 C

- 出处：第 30-31 页与第 36 页，`5.0 I/O Ports of the Component / Chapter 6`，`paper_content.txt` 第 3225-3309、3728-3759 行
> We want this pseudo hardware to measure voltage, and if the bus voltages fall below a set tolerance level then shed the lowest priority load on the list of loads ... Once a load has been shed a delay is implemented before measures bus voltages are processed so a false trip signal is not sent.
>
> The “CLK” input is the clock signal that determines when the load-shedding controller will process the programmed code ... The reset input ... will be forced into state zero, (idle state). The “LOADSHED” input is the signal that tells the load-shedding controller to shed load when the undervoltage conditions are met.
>
> The most critical load, Meter `U_V1`, ... will never be shed ... The load-shedding controller was set to trigger an undervoltage event at a per-unit voltage of below `0.90` and reconnect a load to the microgrid at `0.93` per-unit voltage.

### 2. 基于原文整理后的自然语言描述

The thesis implements the microgrid load-shedding scheme as a Moore FSM with an `undervoltage` trigger, a `reset` input, and outputs that drive breaker controllers. The logic is built from a truth table and next-state/output logic, then executed through a resettable flip-flop on an external clock so it can be ported into real-time `RSCAD` hardware. At runtime the controller monitors bus voltages, sheds the lowest-priority load when the monitored buses fall below the configured tolerance, and inserts a delay before measuring again so transient dips do not trigger repeated false trips. The reset input forces the software back to `state zero` (`idle state`), while the same component also decides when shed loads may be reconnected to the power system. In the reported settings the controller triggers undervoltage action below `0.90 p.u.`, allows reconnection at `0.93 p.u.`, and keeps the highest-priority `U_V1` load online as long as possible, so this is a `T1` clocked FSM rather than a generic heuristic rule list.

### 3. 逐句溯源

1. 句子 1：The thesis implements the microgrid load-shedding scheme as a Moore FSM with an `undervoltage` trigger, a `reset` input, and outputs that drive breaker controllers.
   对应摘录：A, C
2. 句子 2：The logic is built from a truth table and next-state/output logic, then executed through a resettable flip-flop on an external clock so it can be ported into real-time `RSCAD` hardware.
   对应摘录：A
3. 句子 3：At runtime the controller monitors bus voltages, sheds the lowest-priority load when the monitored buses fall below the configured tolerance, and inserts a delay before measuring again so transient dips do not trigger repeated false trips.
   对应摘录：B, C
4. 句子 4：The reset input forces the software back to `state zero` (`idle state`), while the same component also decides when shed loads may be reconnected to the power system.
   对应摘录：C
5. 句子 5：In the reported settings the controller triggers undervoltage action below `0.90 p.u.`, allows reconnection at `0.93 p.u.`, and keeps the highest-priority `U_V1` load online as long as possible, so this is a `T1` clocked FSM rather than a generic heuristic rule list.
   对应摘录：C
