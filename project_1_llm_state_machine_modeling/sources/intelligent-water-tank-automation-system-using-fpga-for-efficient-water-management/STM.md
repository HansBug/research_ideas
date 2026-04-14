# Intelligent Water Tank Automation System using FPGA for Efficient Water Management - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把水箱自动控制器的 ADC 阈值、三态 FSM、泵继电器输出、LED 水位反馈和手动复位都写成了清晰的 FPGA 控制链，足以形成双 A 样本。

## 条目 1: ADC-Threshold Pump Relay and LED Water-Tank FSM

- 控制对象：过程与环境控制领域的水箱液位自动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 DE10-Nano FPGA 的水箱液位控制器，用水位传感器、ADC、继电器、泵和 LED 反馈来执行阈值触发的补水控制。
- 判断：算。对象是真实水箱自动控制系统，原文明确给出硬件组成、`25% / 90%` 阈值、`Idle / Pump ON / Pump OFF` 三态 FSM、LED 编码以及人工复位行为。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5 页，`3.1 Hardware Components / 3.2 Control Logic Design`，`paper_content.txt` 第 135-159 行
> The system comprises:
> DE10-Nano FPGA Board ... Water Level Sensor ... ADC (MCP3208) ... Relay Module ... DC Motor Pump ... LED Display ... Manual Override Switch.
>
> The control logic, implemented in Verilog, processes 12-bit ADC data to generate control signals. The FPGA operates at a 50 MHz clock, divided to produce a 1 MHz SPI clock. The logic compares water level data against thresholds to control the relay and LEDs, with a manual override resetting the system to a safe state.

#### 摘录 B

- 出处：第 6 页，`3.3 Threshold-Based Algorithm / 3.4 FSM Design`，`paper_content.txt` 第 169-180 行
> Pump ON, if VADC < Vlow = 1000 (25%)
> State = Pump OFF, if VADC > Vhigh = 3600 (90%)
> No Change, otherwise
>
> LED out =
> 7′b0000001, if V < 1000
> 7′b0000111, if 1000 ≤ VADC ≤ 3600
> 7′b1111111, if VADC > 3600
>
> The system operates via a finite state machine (FSM) with three states: Idle, Pump ON, and Pump OFF. Transitions are based on water level thresholds and manual override.

#### 摘录 C

- 出处：第 7-8 页，`4.1 Simulation / 4.3 Hardware Prototype`，`paper_content.txt` 第 195-203、223-232 行
> Key scenarios tested included:
> Low water level (VADC = 500): Pump ON, LED = 7’b0000001.
> Medium water level (VADC = 2000): Pump OFF, LED = 7’b0000111.
> High water level (VADC = 4000): Pump OFF, LED = 7’b1111111.
> Manual override: Reset signal forcing Idle state.
>
> The hardware prototype was assembled using the DE10-Nano board, MCP3208 ADC, water level sensor, relay module, DC motor pump, LEDs, and a 9V battery.
> The prototype was tested in a 10-liter tank ... The pump activated at 25% (2.5 liters) and deactivated at 90% (9 liters), with LEDs accurately reflecting levels. The manual override switch effectively reset the system to Idle state.

### 2. 基于原文整理后的自然语言描述

The water-tank automation controller combines a DE10-Nano FPGA, a resistive water-level sensor, an MCP3208 ADC, a relay-driven pump, a seven-LED level display, and a manual override switch into a threshold-based control loop. Its Verilog logic reads 12-bit ADC values through SPI and compares them against `Vlow = 1000` at `25%` tank capacity and `Vhigh = 3600` at `90%` capacity to decide whether the pump should turn on, turn off, or keep its previous state. The controller is organized as a three-state FSM with `Idle`, `Pump ON`, and `Pump OFF`, and it also maps the measured level to three explicit LED output patterns for low, medium, and full water conditions. The reported simulation and tank tests confirm that the pump turns on around `2.5` liters, turns off around `9` liters, and returns to `Idle` whenever the manual override reset is activated.

### 3. 逐句溯源

1. 句子 1：The water-tank automation controller combines a DE10-Nano FPGA, a resistive water-level sensor, an MCP3208 ADC, a relay-driven pump, a seven-LED level display, and a manual override switch into a threshold-based control loop.
   对应摘录：A, C
2. 句子 2：Its Verilog logic reads 12-bit ADC values through SPI and compares them against `Vlow = 1000` at `25%` tank capacity and `Vhigh = 3600` at `90%` capacity to decide whether the pump should turn on, turn off, or keep its previous state.
   对应摘录：A, B
3. 句子 3：The controller is organized as a three-state FSM with `Idle`, `Pump ON`, and `Pump OFF`, and it also maps the measured level to three explicit LED output patterns for low, medium, and full water conditions.
   对应摘录：B
4. 句子 4：The reported simulation and tank tests confirm that the pump turns on around `2.5` liters, turns off around `9` liters, and returns to `Idle` whenever the manual override reset is activated.
   对应摘录：C
