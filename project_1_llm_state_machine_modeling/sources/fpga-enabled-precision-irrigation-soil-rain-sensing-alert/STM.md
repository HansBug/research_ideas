# Revolutionary FPGA-Enabled Precision Irrigation Framework with Integrated Soil-Rain Sensing and Real-Time Alert Mechanisms - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了雨量/土壤湿度输入、雨天停灌告警、干土无雨启动水泵、七段显示、继电器定时和去抖等完整控制链，可形成双 A 过程与环境控制样本。

## 条目 1: Soil-Rain Guarded Pump and Alert Controller

- 控制对象：过程与环境控制领域的土壤湿度、雨量感知、灌溉水泵与告警控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 FPGA 和 Verilog 的精准灌溉控制器，根据雨量传感器和土壤湿度传感器组合决定停灌、开泵、显示状态和蜂鸣告警。
- 判断：算。原文虽然不是形式化状态图，但明确给出输入组合、guard、输出动作、继电器定时和测试情形，足以整理成 `EFSM + T1` 的控制系统自然语言描述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 14-27 行
> The system employs a high-resolution rain sensor to detect precipitation dynamics and a calibrated soil moisture sensor to assess soil hydration levels, interfaced with an FPGA platform for robust decision-making. The control logic, implemented via Verilog HDL, dynamically adjusts irrigation based on environmental inputs: upon rain detection, a buzzer activates, and a seven-segment display indicates "r-on," halting irrigation, while dry soil conditions trigger the water pump when moisture falls below a threshold, ensuring efficient resource management. The FPGA's parallel processing capability enhances response latency, achieving sub-millisecond decision cycles ... Experimental validation on a prototype demonstrates a 35% reduction in water wastage ... with a reliability index of 98.7%.

#### 摘录 B

- 出处：第 5 页，`3.4 Flow Chart / 3.5 Working Principle`，`paper_content.txt` 第 148-157 行
> The flow chart outlines the decision-making process, beginning with sensor readings. It checks for rain and soil moisture, activates the pump if conditions warrant, or triggers alerts otherwise. This ensures optimal water usage and prevents over-irrigation.
>
> The system operates on binary logic from the sensors: high for detection (rain or moisture present). The FPGA evaluates these combinations - activating the pump only if the soil is dry (low moisture) and no rain is detected. Otherwise, it halts irrigation, activates the buzzer during rain, and updates the display. This logic prioritizes water conservation and automation.

#### 摘录 C

- 出处：第 5 页，`3.6 Control Logic / 4.1 RTL Implementation`，`paper_content.txt` 第 158-173 行
> Control logic is implemented in Verilog HDL, with modules for sensor processing, display multiplexing, relay de-bouncing, and buzzer tone generation. Debouncing ensures stable relay operation, while parallel FPGA processing achieves sub-millisecond latency.
>
> Overall Code Module: Integrates all submodules, defining inputs (clk, reset, soil_in, rain_in) and outputs (an[3:0], cath[7:0], relay_out, buzzer). It uses internal wires such as alarm_trigger and pump_on.
>
> Rain/Logic Module: Handles decision logic and display control. It sets alarm_trigger based on sensor combinations and multiplexes the seven-segment display to show "r-on" or "rOFF," using a clock divider for segmentation.
>
> Relay Module: Controls the pump with parameters for clock frequency, on-duration (2 seconds), and debounce time (1000 ms). It includes debouncing logic to filter noise and a counter for timed relay activation (active-low).
>
> Buzzer Module: Generates a 1 kHz square wave when triggered, using a 17-bit counter on a 100 MHz clock.

#### 摘录 D

- 出处：第 7 页，`5.1 Simulation Testing / 5.2 Hardware Testing`，`paper_content.txt` 第 205-217 行
> Testbenches simulated various sensor inputs - rain detected (high), soil dry (low), etc. Waveforms confirmed correct display outputs ("r-on"/"rOFF"), buzzer activation, and relay toggling. Timing analysis showed sub-1 ms latency with no glitches after debouncing.
>
> Lab Tests: Controlled environments simulated rain (by dripping water on the sensor) and soil conditions (dry/wet probes). The system accurately activated the pump only when the soil was dry and no rain was detected, with the buzzer sounding during rain. Reliability reached 98.7%, and water savings were 35% compared to manual methods.
>
> Field Tests: Conducted over a 7-day period on a small farm plot. The system successfully prevented over-irrigation during two rain events.

### 2. 基于原文整理后的自然语言描述

The FPGA irrigation controller reads binary rain and soil-moisture inputs and uses those guard combinations to decide whether the system is in a rain-alert halt condition, a dry-soil watering condition, or a non-watering monitoring condition. If rain is detected, the controller halts irrigation, raises `alarm_trigger`, sounds the buzzer, and multiplexes the seven-segment display to show `r-on`; if the soil is dry and no rain is detected, it sets `pump_on` and drives the relay output so the water pump is activated. The RTL design exposes `clk`, `reset`, `soil_in`, and `rain_in` as inputs and `relay_out`, `buzzer`, `an[3:0]`, and `cath[7:0]` as outputs, while the relay module filters sensor noise with a 1000 ms debounce and uses a timed 2 s relay activation counter, and the buzzer module generates a 1 kHz alert from a 100 MHz clock. Simulations and prototype tests cover rain-high, soil-dry, wet-soil, and field-rain scenarios, confirming `r-on`/`rOFF` display updates, buzzer activation, relay toggling, sub-1 ms response after debouncing, and pump activation only under dry-soil and no-rain conditions.

### 3. 逐句溯源

1. 句子 1：The FPGA irrigation controller reads binary rain and soil-moisture inputs and uses those guard combinations to decide whether the system is in a rain-alert halt condition, a dry-soil watering condition, or a non-watering monitoring condition.
   对应摘录：A, B
2. 句子 2：If rain is detected, the controller halts irrigation, raises `alarm_trigger`, sounds the buzzer, and multiplexes the seven-segment display to show `r-on`; if the soil is dry and no rain is detected, it sets `pump_on` and drives the relay output so the water pump is activated.
   对应摘录：A, B, C
3. 句子 3：The RTL design exposes `clk`, `reset`, `soil_in`, and `rain_in` as inputs and `relay_out`, `buzzer`, `an[3:0]`, and `cath[7:0]` as outputs, while the relay module filters sensor noise with a 1000 ms debounce and uses a timed 2 s relay activation counter, and the buzzer module generates a 1 kHz alert from a 100 MHz clock.
   对应摘录：C
4. 句子 4：Simulations and prototype tests cover rain-high, soil-dry, wet-soil, and field-rain scenarios, confirming `r-on`/`rOFF` display updates, buzzer activation, relay toggling, sub-1 ms response after debouncing, and pump activation only under dry-soil and no-rain conditions.
   对应摘录：D
