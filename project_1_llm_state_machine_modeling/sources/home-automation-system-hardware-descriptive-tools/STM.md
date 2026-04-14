# A Home Automation System Design Using Hardware Descriptive Tools - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把家居门禁、防盗/火警、温度和照度调节写成了一个有显式状态名、阈值条件和输出动作的优先扫描控制器，能稳定落成 `EFSM + T0` 样本。

## 条目 1: Priority-Ordered Door, Alarm, and Climate Home Controller
- 控制对象：楼宇与家居自动化场景下的门禁、安全告警与环境调节控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Mealy state machine 的家居控制器，按优先顺序处理前门安全、火警、温度调节和照度调节，并把对应告警器、空调、加热器和照明输出联动起来。
- 判断：算。对象是实际 home automation controller，不是单纯 HDL 教学流程；原文给出了状态名、输入阈值、输出动作以及 current/next-state 映射。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 10-34 行
> This device had been modelled such that it takes care of home intrusion detection and avoidance, while it also controls other home environment factors such as temperature and smoke detection. A sequential pattern of controlling the door, burglar alarm, fire alarm, temperature and luminosity is followed in a priority order. The solution uses the hardware design system concepts of a state machine to design a Mealy system that is simulated in Verilog HDL using Xilinx and ModelSim.

#### 摘录 B
- 出处：第 4-5 页，`Flow Diagram / State Diagrams`，`paper_content.txt` 第 302-360 行
> The first state is the start state, in this state all the inputs and outputs are set to 0.
>
> Front door state: In this state the status of the front door is checked ... if the input from the magnetic sensor on the front door is 0 (LO) that indicates the door is closed, while if it is 1 (HI) then the door is open.
>
> Fire alarm state: The sensor here is the smoke detector ... if it detects smoke then the input it sends is a 1 ... it triggers a buzzer and goes to the next state which is the temperature state.
>
> Temperature controller state ... If it goes below 50°F, then the system turns on the heater and if temperature goes beyond 70°F, then the air conditioner is turned on ... Luminosity control state ... if lum_sen > 00001111, then decrease the current through the light source else if lum_sen < 00001111, then increase the current through the light source.
>
> Current and next states ... Start → fdoor, Fdoor → fire, Fire → t_cool, t_cool → t_heat, t_heat → l_dim, l_dim → l_bright, l_bright → start.

#### 摘录 C
- 出处：第 7-9 页，`Results / Conclusion`，`paper_content.txt` 第 612-676 行
> This is the simulation output when the burglar alarm goes off ... when d_sen is set to “1” (HIGH), this sets b_alrm to “1” (HIGH).
>
> This is the simulation output when the fire alarm goes off ... when f_sen is set to “1” (HIGH), this sets f_alrm to “1” (HIGH).
>
> The temperature control module controls the operation of both the cooler and the heater ... when temp_sen is greater than 1000110 then the cooler is turned on ... and when temp_sen is lower than 1000110 then heater is turned on.
>
> The order of checking the devices based on the priority is followed and also the display shows the state the system is in.

### 2. 基于原文整理后的自然语言描述

The home controller is organized as a priority-ordered Mealy machine that repeatedly scans security and environment functions in a fixed sequence instead of treating each appliance as an isolated block. Starting from `start`, it checks the front-door sensor and associated burglar-alarm output, then moves through fire detection, temperature regulation, and luminosity regulation before returning to the initial state. Within those states, guard conditions are defined over concrete sensor values: smoke drives the fire buzzer branch, temperatures below `50°F` enable heating, temperatures above `70°F` enable cooling, and the light sensor threshold `00001111` selects whether lamp current should be increased or decreased. The simulation section confirms the same control chain by showing `d_sen` driving `b_alrm`, `f_sen` driving `f_alrm`, and `temp_sen` switching between cooler and heater outputs while the display reports the active state.

### 3. 逐句溯源

1. 句子 1：The home controller is organized as a priority-ordered Mealy machine that repeatedly scans security and environment functions in a fixed sequence instead of treating each appliance as an isolated block.
   对应摘录：A, B
2. 句子 2：Starting from `start`, it checks the front-door sensor and associated burglar-alarm output, then moves through fire detection, temperature regulation, and luminosity regulation before returning to the initial state.
   对应摘录：B
3. 句子 3：Within those states, guard conditions are defined over concrete sensor values: smoke drives the fire buzzer branch, temperatures below `50°F` enable heating, temperatures above `70°F` enable cooling, and the light sensor threshold `00001111` selects whether lamp current should be increased or decreased.
   对应摘录：B
4. 句子 4：The simulation section confirms the same control chain by showing `d_sen` driving `b_alrm`, `f_sen` driving `f_alrm`, and `temp_sen` switching between cooler and heater outputs while the display reports the active state.
   对应摘录：C
