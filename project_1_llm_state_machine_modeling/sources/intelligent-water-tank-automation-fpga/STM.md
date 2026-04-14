# Intelligent Water Tank Automation System using FPGA for Efficient Water Management - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把水位采样、阈值比较、泵启停和手动复位统一写成三状态 FSM，并补了测试场景与硬件原型结果，足以形成 `FSM + T0` 双 A 样本。

## 条目 1: Threshold-Based Water Tank Pump Controller
- 控制对象：过程与环境控制领域的水位阈值驱动补水与手动复位控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个运行在 `DE10-Nano` FPGA 上的水箱自动补水控制器，读取 ADC 水位值后依据低/高阈值切换 `Idle`、`Pump ON` 和 `Pump OFF` 三个状态，并允许人工复位到安全态。
- 判断：算。对象是明确的 water tank automation controller，不是泛化 IoT 方案综述；原文给出了状态集合、阈值、LED 输出编码、手动复位和原型测试场景。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract / Proposed Solution，`paper_content.txt` 第 17-26、60-71 行
> The system executes real-time, threshold-driven logic to modulate pump operations, preempting overflow and mitigating dry-run scenarios. A visually intuitive LED array delivers instantaneous water level feedback, augmented by a manual override mechanism for enhanced user agency. ... Threshold logic activates the pump at 25% and deactivates at 90% water levels, ensuring optimal resource use.

#### 摘录 B
- 出处：第 5-6 页，`Control Logic Design / Threshold-Based Algorithm / FSM Design`，`paper_content.txt` 第 156-180 行
> The control logic, implemented in Verilog, processes 12-bit ADC data to generate control signals. The FPGA operates at a 50 MHz clock, divided to produce a 1 MHz SPI clock. The logic compares water level data against thresholds to control the relay and LEDs, with a manual override resetting the system to a safe state. ... Pump ON, if VADC < Vlow = 1000 (25%) ... Pump OFF, if VADC > Vhigh = 3600 (90%) ... The system operates via a finite state machine (FSM) with three states: Idle, Pump ON, and Pump OFF. Transitions are based on water level thresholds and manual override.

#### 摘录 C
- 出处：第 7-8 页，`Simulation / Hardware Prototype`，`paper_content.txt` 第 195-203、231-232 行
> Key scenarios tested included: Low water level (VADC = 500): Pump ON ... Medium water level (VADC = 2000): Pump OFF ... High water level (VADC = 4000): Pump OFF ... Manual override: Reset signal forcing Idle state. Simulation results confirmed correct state transitions and output signals ... The prototype demonstrated reliable operation, with no overflow or dry-run conditions. The manual override switch effectively reset the system to Idle state, ensuring user control.

### 2. 基于原文整理后的自然语言描述

The water-tank controller reads a 12-bit ADC measurement of tank level and uses a three-state FSM to govern pump behavior. Its nominal logic is threshold-based: when `VADC < 1000` the controller enters `Pump ON`, when `VADC > 3600` it forces `Pump OFF`, and otherwise it preserves the current decision while driving a three-level LED indication of water status. The paper also adds a manual override that resets the controller back to `Idle`, so the control chain is not just a one-shot comparator but an explicit supervisory automaton with a safe-state transition. Because the thresholds, state names, LED outputs, and tested low/medium/high-water scenarios are all written out in the text, this is a strong `FSM + T0` water-level sample.

### 3. 逐句溯源

1. 句子 1：The water-tank controller reads a 12-bit ADC measurement of tank level and uses a three-state FSM to govern pump behavior.
   对应摘录：B
2. 句子 2：Its nominal logic is threshold-based: when `VADC < 1000` the controller enters `Pump ON`, when `VADC > 3600` it forces `Pump OFF`, and otherwise it preserves the current decision while driving a three-level LED indication of water status.
   对应摘录：A, B
3. 句子 3：The paper also adds a manual override that resets the controller back to `Idle`, so the control chain is not just a one-shot comparator but an explicit supervisory automaton with a safe-state transition.
   对应摘录：A, B, C
4. 句子 4：Because the thresholds, state names, LED outputs, and tested low/medium/high-water scenarios are all written out in the text, this is a strong `FSM + T0` water-level sample.
   对应摘录：B, C
