# FPGA-Based Smart Parking Management System with Real-Time Slot Monitoring and Entry/Exit Detection - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场的出入场检测、四车位占用计数、显示反馈和状态转换写成了一个明确的三态 FPGA 控制器，原文足以形成双 A 样本。

## 条目 1: Idle-Entry-Exit Slot-Monitoring Parking Controller

- 控制对象：智慧停车领域的停车场出入场与车位占用监测控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Artix-7 FPGA 的停车场控制器，用六个红外传感器管理四个停车位以及入口/出口检测，并驱动 LCD、7 段数码管和车位 LED 显示。
- 判断：算。对象是实际停车场监测与门禁信息控制系统，原文明确给出 `IR1–IR6` 输入、占用/空位计数规则、`Idle / Entry / Exit` 三态 FSM，以及相应的显示与状态更新逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`3 SYSTEM ARCHITECTURE / 3.1 System Overview`，`paper_content.txt` 第 103-110 行
> The Smart Parking System leverages an Artix-7 FPGA to automate parking management with high precision and efficiency.
>
> The system monitors four parking slots and entry/exit points using six IR sensors. The FPGA processes sensor inputs, updates occupancy counters, and controls a 16x2 LCD (displays slot counts), a 2-digit 7-segment display (shows entry/exit indicators), and four LEDs (indicate slot status). The design uses Verilog HDL with parameterized registers and FSMs for synchronous operation.

#### 摘录 B

- 出处：第 4-5 页，`3.3 Flow Chart / 3.4 Finite State Machine (FSM)`，`paper_content.txt` 第 145-167 行
> The operational flow chart is:
> 1.Initialize: Set O = 0, A = 4, LEDs OFF, LCD to “O=0; A=4”.
> 2.Monitor IR5 (entry): If LOW, display “et”, wait for slot IR (IR1–IR4) to go LOW.
> 3.Update Slot: Set corresponding LED ON, increment O, decrement A, update LCD.
> 4.Monitor IR6 (exit): If LOW, display “ei”, wait for slot IR to go HIGH.
> 5.Update Slot: Set LED OFF, decrement O, increment A, update LCD.
> 6.Return to monitoring.
>
> The FSM in the parking counter module manages entry/exit detection with three states:
> Idle: Monitors IR5 and IR6. Transitions to Entry if IR5 = LOW, or Exit if IR6 = LOW.
> Entry: Displays “et” on 7-segment, increments O when a slot IR goes LOW. Returns to Idle after slot update.
> Exit: Displays “ei” on 7-segment, decrements O when a slot IR goes HIGH. Returns to Idle.

#### 摘录 C

- 出处：第 5-7 页，`4.1 Verilog Modules / 5 TESTING AND RESULTS`，`paper_content.txt` 第 172-190、217-225 行
> parking counter: Inputs: 6-bit IR sensor signals, clock (50 MHz), reset. Outputs: 4-bit LED signals, 8-bit 7-segment data, 4-bit digit select. Uses a clock divider (fclk seg = fclk/106) for multiplexing. FSM manages entry/exit logic. Counter logic: O = Σ4 (1−IRi), A = 4 − O.
>
> Simulations were conducted using Xilinx Vivado. Testbenches simulated:
> Sequential slot occupancy: IR1–IR4 set LOW one-by-one, verifying O increments and LCD updates.
> Entry/exit scenarios: IR5 LOW triggers “et”, IR6 LOW triggers “ei”, with accurate counter updates.
> Edge Case Test: Rapid toggling of IR5 and IR6, and simultaneous slot changes, were tested to evaluate system stability. No glitches occurred, with response times under 1 ms.

### 2. 基于原文整理后的自然语言描述

The FPGA parking controller monitors four parking slots and two gate-side event points with six IR sensors, and it drives a 16x2 LCD, a 2-digit 7-segment display, and four slot LEDs while maintaining occupancy `O` and availability `A`. After initialization the system sets `O = 0` and `A = 4`, turns the LEDs off, and displays the empty-lot summary on the LCD. Its parking-counter FSM then stays in `Idle` until the entry sensor `IR5` or exit sensor `IR6` is activated, moves to `Entry` to display `et` and wait for a slot sensor to go LOW so it can light the corresponding LED and increment occupancy, or moves to `Exit` to display `ei` and wait for a slot sensor to go HIGH so it can clear the LED and decrement occupancy. The underlying Verilog module defines this logic over six sensor inputs and uses the explicit counter equations `O = Σ4 (1−IRi)` and `A = 4 − O`, and the reported tests confirm correct slot-by-slot updates and sub-millisecond response without glitches.

### 3. 逐句溯源

1. 句子 1：The FPGA parking controller monitors four parking slots and two gate-side event points with six IR sensors, and it drives a 16x2 LCD, a 2-digit 7-segment display, and four slot LEDs while maintaining occupancy `O` and availability `A`.
   对应摘录：A, C
2. 句子 2：After initialization the system sets `O = 0` and `A = 4`, turns the LEDs off, and displays the empty-lot summary on the LCD.
   对应摘录：B
3. 句子 3：Its parking-counter FSM then stays in `Idle` until the entry sensor `IR5` or exit sensor `IR6` is activated, moves to `Entry` to display `et` and wait for a slot sensor to go LOW so it can light the corresponding LED and increment occupancy, or moves to `Exit` to display `ei` and wait for a slot sensor to go HIGH so it can clear the LED and decrement occupancy.
   对应摘录：B
4. 句子 4：The underlying Verilog module defines this logic over six sensor inputs and uses the explicit counter equations `O = Σ4 (1−IRi)` and `A = 4 − O`, and the reported tests confirm correct slot-by-slot updates and sub-millisecond response without glitches.
   对应摘录：C
