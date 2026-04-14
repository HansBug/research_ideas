# Modeling of Automatic Sprinkler Irrigation Process Using Finite State Machine (FSM) and Proportional Integral Derivative (PID) Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把喷灌监督控制器的状态集合、阈值 guard、泵/喷头动作和 `after(2,sec)`、`after(0.05,sec)` 两个工程定时都写成了可直接恢复的 Stateflow 逻辑。

## 条目 1: Soil-Moisture Supervisory Irrigation FSM
- 控制对象：过程控制领域的喷灌灌溉监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个以土壤湿度为输入、以泵电机驱动电压为输出的喷灌监督控制器，负责在枯萎阈值和饱和阈值之间切换泵、喷头和土壤过程状态。
- 判断：算。对象是实际灌溉过程控制器，原文直接给出了状态集合、输入输出语义、阈值 guard、定时迁移和启停动作。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，`State Machines (FSM) / Figure 2`，`paper_content.txt` 第 117-135 行
> The flow chart s hown in Figure 2 shows the steps used in the design of the automatic control logic for the irrigation system. In order to define states for the automatic control logic, it is important to consider the process of soil water dynamics which clearly define the states of the controller.
>
> The mechanics of soil water movement and soil moisture growth are very complex processes ... The states that could be easily identified include but not limited to the following: Soil moisture content state (ii) Soil condition state (iii) Saturation state (iv) Wilting point state (v) Plant water uptake state (vi) Pump state (vii) Sprinkler state (viii) Leaching state (ix) Runoff state, etc.

#### 摘录 B
- 出处：第 3-4 页，`Figure 3 . FSM states, attributes and transitions`，`paper_content.txt` 第 142-183 行
> The first seven states are considered and some are combined together to form basic operating modes for the system. Using state flow chart semantics in Simulink, the following states were adopted for the automatic controller as shown in Figure 3.
>
> As one of the sequential logic approach, the automatic controller used Stateflow chart to rep resent relationships among inputs, outputs and states of FSM representation of the irrigation system. The resulting chart in Figure 3 describes the logic necessary to control the behaviour of the system under study. Generally in state machine models, the n ext state is a function of the current state and its inputs ...
>
> The main input to the automatic controller is the soil moisture which is measured by a sensor through a direct feedback to the unit. It is this value which the controller monitors to determine when to energize and de -energize the centrifugal pump to releas e water to soil via the sprinkler. Conversely, the output is the supplied voltage to the motor driven pump at every time step.
>
> once the sensor detects soil moisture value less than the stipulated soil wilting point, there is a major transition from the soil -moisture state to the pump- start state. Along this transition, there is an introduction of a temporal logic meant to delay the supply of voltage to the pump electric motor by about 2 seconds.

#### 摘录 C
- 出处：第 4 页，`Table 1 . Transitions for automatic control logic`，`paper_content.txt` 第 199-215 行
> Transitions  Transition Conditions  Transition Actions
> To SoilMoisture (default)  None  Transit
> PlantUptake - Leftover  [Soilmoisture>= soilHH]  {Voltage = volt2}
> Leftover - PlantUptake [Soilmoisture<= soilLL]  {Voltage = volt1}
> To PlantUptake  None  Transit
> SoilMoisture - PumpStart  after(2,sec)[Soilmoisture<= soilLL]  {Voltage = volt1}
> To SprinklerOff  None  Transit
> SprinklerOff - SprinklerOn  [Soilmoisture<= soilLL]  {Voltage = volt1}
> SprinklerOn - SprinklerOff  [Soilmoisture>= soilHH]  {Voltage = volt2}
> PumpStart - Soil [Soilmoisture>= soilHH]  {Voltage = volt2}
> To Wilting  None  Transit
> Wilting - Saturation  [Soilmoisture>= soilHH]...  {Voltage = volt2}
> Saturation - Wilting  [Soilmoisture<= soilLL]...  {Voltage = volt1}
> Soil - PumpStop  after(0.05, sec)[Soilmoisture>= soilHH]  {Voltage = volt2}
> PumpStop - Soil [Soilmoisture<= soilLL]  {Voltage = volt1}
> Soil - SoilMoisture  [Soilmoisture<= soilLL]...  {Voltage = volt1}

### 2. 基于原文整理后的自然语言描述

The sprinkler-irrigation controller is a Stateflow-based supervisory EFSM that organizes the irrigation process around soil-moisture, soil-condition, saturation, wilting, plant-uptake, pump, and sprinkler-related states. Its main input is the measured soil-moisture feedback, while its effective output is the drive voltage sent to the motor-driven centrifugal pump, so the next state is chosen from the current state and the current moisture-related inputs rather than from a fixed time script. When the measured moisture drops below the low threshold `soilLL`, the controller leaves `SoilMoisture` and enters `PumpStart` only after `after(2,sec)` to confirm the reading, then enables watering through `SprinklerOff -> SprinklerOn`, `Leftover -> PlantUptake`, and related soil/wilting states with voltage actions such as `volt1`. When the moisture reaches the upper threshold `soilHH`, transitions such as `SprinklerOn -> SprinklerOff`, `Wilting -> Saturation`, and `Soil -> PumpStop after(0.05,sec)` reduce or stop watering with `volt2`, so the model contains both threshold-driven switching and explicit timed stop confirmation.

### 3. 逐句溯源

1. 句子 1：The sprinkler-irrigation controller is a Stateflow-based supervisory EFSM that organizes the irrigation process around soil-moisture, soil-condition, saturation, wilting, plant-uptake, pump, and sprinkler-related states.
   对应摘录：A, B
2. 句子 2：Its main input is the measured soil-moisture feedback, while its effective output is the drive voltage sent to the motor-driven centrifugal pump, so the next state is chosen from the current state and the current moisture-related inputs rather than from a fixed time script.
   对应摘录：B
3. 句子 3：When the measured moisture drops below the low threshold `soilLL`, the controller leaves `SoilMoisture` and enters `PumpStart` only after `after(2,sec)` to confirm the reading, then enables watering through `SprinklerOff -> SprinklerOn`, `Leftover -> PlantUptake`, and related soil/wilting states with voltage actions such as `volt1`.
   对应摘录：B, C
4. 句子 4：When the moisture reaches the upper threshold `soilHH`, transitions such as `SprinklerOn -> SprinklerOff`, `Wilting -> Saturation`, and `Soil -> PumpStop after(0.05,sec)` reduce or stop watering with `volt2`, so the model contains both threshold-driven switching and explicit timed stop confirmation.
   对应摘录：C
