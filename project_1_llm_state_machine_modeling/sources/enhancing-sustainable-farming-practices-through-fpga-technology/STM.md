# Enhancing Sustainable Farming Practices through FPGA Technology - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `soil_moisture_monitor` 的双状态 FSM、双阈值 guard、复位逻辑和 RTL 实现都写得较完整，可直接作为环境控制领域的双 A 样本。

## 条目 1: Dry-Wet Threshold Irrigation Pump FSM
- 控制对象：基于 FPGA 的土壤湿度灌溉泵控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是过程与环境控制领域的 FPGA 灌溉控制器，利用 `DRY_THRESHOLD` 与 `WET_THRESHOLD` 两个阈值，在 `DRY` 和 `WET` 两个状态之间切换，并驱动水泵开关。
- 判断：算。对象是实际自动灌溉控制模块，原文明确给出输入、输出、阈值、状态集合、转移条件、复位逻辑和 RTL 结构，不是泛化的农业背景介绍。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4-5 页，`4.2 Soil Moisture Monitoring / 4.2.1 Inputs and Outputs / 4.2.2 Moisture Thresholds`，`paper_content.txt` 第 168-170 行、第 183-196 行
> The soil_moisture_monitor module is a crucial component of an automated irrigation system that intelligently controls a water pump based on the soil moisture levels detected by a sensor.
>
> The moisture level input (`moisture_level`) is a 10-bit digital value ... The output signal (`water_pump`) is a digital control signal that directly activates or deactivates the water pump.
>
> The module employs two predefined moisture thresholds: `DRY_THRESHOLD` and `WET_THRESHOLD`. The `DRY_THRESHOLD` indicates the moisture level below which the soil is considered dry and in need of watering. Conversely, the `WET_THRESHOLD` signifies the moisture level above which the soil is deemed sufficiently wet, at which point the irrigation should stop.

#### 摘录 B
- 出处：第 5 页，`4.2.3 Finite State Machine (FSM)`，`paper_content.txt` 第 197-215 行
> The `soil_moisture_monitor` module's core features a finite state machine (FSM) ... comprising two states: DRY (noted as `1'b0`) and WET (noted as `1'b1`).
>
> In the DRY state ... it activates the water pump by setting the `water_pump` output to `1` ... if it detects that the level exceeds the `WET_THRESHOLD`, it transitions to the WET state, turning off the pump by setting `water_pump` to `0`.
>
> if the system finds itself in the WET state and the moisture level subsequently drops below the `DRY_THRESHOLD`, it transitions back to the DRY state ... The FSM updates its state based on the current moisture readings on the rising edge of the clock signal.

#### 摘录 C
- 出处：第 6-7 页，`5.1 Irrigation Control System / Figure 5`，`paper_content.txt` 第 233-252 行、第 260-262 行
> The irrigation control system presented herein continuously monitors soil moisture levels ... The input `moisture_level[9:0]` represents a 10-bit digital signal ... comparator blocks such as RTL_LT and RTL_GT determine whether the moisture level is below or above the thresholds.
>
> The comparators drive the state transitions ... The design uses multiplexer blocks to select the next state of the control logic. The `state_reg` block stores the current state of the system ...
>
> The final output `water_pump` activates the irrigation system when soil moisture falls below the predefined threshold, and deactivates it once sufficient moisture is detected.

### 2. 基于原文整理后的自然语言描述

The `soil_moisture_monitor` controller is an FPGA-based irrigation EFSM that reads a `10-bit` `moisture_level` input and drives a binary `water_pump` output according to two predefined thresholds. Its control core is a two-state machine with states `DRY` and `WET`. In `DRY`, the controller considers the soil too dry and turns the pump on; once the measured moisture exceeds `WET_THRESHOLD`, it transitions to `WET` and switches the pump off to stop irrigation. In `WET`, the machine stays idle until the moisture value falls below `DRY_THRESHOLD`, at which point it returns to `DRY` and reactivates the pump. The state is updated on the rising edge of the clock, reset initializes the FSM to `DRY`, and the RTL implementation explicitly uses comparators, multiplexers, and a `state_reg` block to realize next-state selection and pump control.

### 3. 逐句溯源

1. 句子 1：The `soil_moisture_monitor` controller is an FPGA-based irrigation EFSM that reads a `10-bit` `moisture_level` input and drives a binary `water_pump` output according to two predefined thresholds.
   对应摘录：A
2. 句子 2：Its control core is a two-state machine with states `DRY` and `WET`.
   对应摘录：B
3. 句子 3：In `DRY`, the controller considers the soil too dry and turns the pump on; once the measured moisture exceeds `WET_THRESHOLD`, it transitions to `WET` and switches the pump off to stop irrigation.
   对应摘录：B
4. 句子 4：In `WET`, the machine stays idle until the moisture value falls below `DRY_THRESHOLD`, at which point it returns to `DRY` and reactivates the pump.
   对应摘录：B
5. 句子 5：The state is updated on the rising edge of the clock, reset initializes the FSM to `DRY`, and the RTL implementation explicitly uses comparators, multiplexers, and a `state_reg` block to realize next-state selection and pump control.
   对应摘录：B, C
