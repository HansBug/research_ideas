# Modeling of Automatic Sprinkler Irrigation Process Using Finite State Machine (FSM) and Proportional Integral Derivative (PID) Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把喷灌 supervisory controller 的 Stateflow chart、状态集合和完整 transition table 一起给出，包含 `after(2,sec)` 与 `after(0.05,sec)` 等显式时间 guard，足够形成 `🌡️` 方向的双 A 条目。

## 条目 1: Soil-Moisture-Gated Pump and Sprinkler Supervisor
- 控制对象：过程与环境控制领域的土壤湿度驱动喷灌监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个根据土壤湿度阈值驱动水泵与喷头启停的喷灌 supervisory FSM，用 `Stateflow` 把土壤、泵、喷头和作物水分阶段联成一套状态转换逻辑。
- 判断：算。对象是真实灌溉控制器，原文明确给出状态来源、Stateflow 语义、主输入输出和 transition/action 表，不是只讲 PID 连续控制。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract / Section 2.2
> Automatic control logic was designed using the finite state machine (FSM) concept to act as a supervisory controller for the real-time automatic irrigation system.
>
> The main input to the automatic controller is the soil moisture ... Conversely, the output is the supplied voltage to the motor driven pump.

#### 摘录 B
- 出处：第 3 页，Section 2.2 / Fig. 3
> the following states were adopted for the automatic controller as shown in Figure 3.
>
> the automatic controller used Stateflow chart to represent relationships among inputs, outputs and states of FSM representation of the irrigation system.

#### 摘录 C
- 出处：第 4 页，Table 1
> `SoilMoisture - PumpStart` `after(2,sec)[Soilmoisture<= soilLL] {Voltage = volt1}`
>
> `SprinklerOff - SprinklerOn [Soilmoisture<= soilLL] {Voltage = volt1}`
>
> `SprinklerOn - SprinklerOff [Soilmoisture>= soilHH] {Voltage = volt2}`

#### 摘录 D
- 出处：第 4 页，Table 1
> `Wilting - Saturation [Soilmoisture>= soilHH] {Voltage = volt2}`
>
> `Saturation - Wilting [Soilmoisture<= soilLL] {Voltage = volt1}`
>
> `Soil - PumpStop after(0.05, sec)[Soilmoisture>= soilHH] {Voltage = volt2}`

### 2. 基于原文整理后的自然语言描述

The irrigation controller is an extended supervisory state machine whose primary condition variable is measured soil moisture and whose output action is the voltage sent to the pump drive. The paper explicitly implements the supervisor in Stateflow and organizes the process around soil, pump, sprinkler, wilting, saturation, and plant-uptake related states instead of leaving the watering cycle implicit. When the measured moisture stays below the low threshold `soilLL` for `2 sec`, the machine leaves `SoilMoisture` for `PumpStart` and energizes the pump with `Voltage = volt1`; the sprinkler branch similarly turns from `SprinklerOff` to `SprinklerOn` under low-moisture conditions. Once the measured moisture rises to the high threshold `soilHH`, the controller de-energizes watering by switching `SprinklerOn -> SprinklerOff` and then, after `0.05 sec`, moving `Soil -> PumpStop` with `Voltage = volt2`. The same threshold variables also drive agronomic state changes such as `Wilting <-> Saturation`, so the controller couples actuator control with explicit moisture-regime states rather than acting as a bare on/off relay.

### 3. 逐句溯源

1. 句子 1：The irrigation controller is an extended supervisory state machine whose primary condition variable is measured soil moisture and whose output action is the voltage sent to the pump drive.
   对应摘录：A
2. 句子 2：The paper explicitly implements the supervisor in Stateflow and organizes the process around soil, pump, sprinkler, wilting, saturation, and plant-uptake related states instead of leaving the watering cycle implicit.
   对应摘录：B
3. 句子 3：When the measured moisture stays below the low threshold `soilLL` for `2 sec`, the machine leaves `SoilMoisture` for `PumpStart` and energizes the pump with `Voltage = volt1`; the sprinkler branch similarly turns from `SprinklerOff` to `SprinklerOn` under low-moisture conditions.
   对应摘录：C
4. 句子 4：Once the measured moisture rises to the high threshold `soilHH`, the controller de-energizes watering by switching `SprinklerOn -> SprinklerOff` and then, after `0.05 sec`, moving `Soil -> PumpStop` with `Voltage = volt2`.
   对应摘录：C, D
5. 句子 5：The same threshold variables also drive agronomic state changes such as `Wilting <-> Saturation`, so the controller couples actuator control with explicit moisture-regime states rather than acting as a bare on/off relay.
   对应摘录：D
