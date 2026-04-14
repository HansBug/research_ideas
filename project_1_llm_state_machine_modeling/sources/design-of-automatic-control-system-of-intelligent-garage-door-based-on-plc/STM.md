# Design of Automatic Control System of Intelligent Garage Door Based on PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🧰 需清洗样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把智能车库门的自动/手动切换、内外传感器触发、限位、防夹光栅与高/中/低速开闭动作写成了明确的 I/O 表和动作记录，足以形成高细节门控 EFSM 样本。

## 条目 1: Auto/manual garage-door controller with anti-pinch and staged speed switching

- 控制对象：楼宇机电与电梯控制领域的智能车库门自动/手动与防夹控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🧰 清洗后保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个由 Mitsubishi FX2N PLC 控制的智能车库门系统，支持自动/手动模式、内外传感器触发、限位停机、防夹回开和分档速度切换。
- 判断：算。原文不仅给出控制对象和组件，还给出完整 I/O 分配表与动作结果表，能够直接支撑 `mode + sensor + guard + output` 级别的状态机抽取。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This article studies the use of PLC ladder diagram programming to control the switch of the smart garage door. The system uses Mitsubishi FX series FX2N-16MR PLC ... equipped with buzzer, and the inside and outside of the garage are used as indicators, and finally a complete intelligent garage door control system is designed.

#### 摘录 B

- 出处：第 2 页，Section 2
> When the car enters the garage, when the car travels to a certain distance from the garage, the owner presses the door open button on the wireless remote switch remote control, the receiver will send the door open signal to the PLC, and then the PLC controls the garage door to open. ... the lights in the garage will be turned on after the smart garage door is fully opened, and at the same time, the lights outside the garage will be turned off.

#### 摘录 C

- 出处：第 4 页，Table 1 I/O port allocation
> Inputs X0 emergency stop; X1 Hand/Automatic transfer switch; X2 Sensor switch (inside); X3 Sensor switch (outside); X4 Anti-pinch grating (normally closed); X5 Lower limit; X6 Open limit; X7 Opening/closing medium speed; X10 Door closing low speed / door opening high speed; X11 Open the door manually; X12 Manual closing; X13 Door closing high speed / door opening low speed; X14 Abnormal reset.

#### 摘录 D

- 出处：第 4 页，Table 1 I/O port allocation
> Outputs Y1 Open the door manually; Y2 Manual closing; Y3 Open/close door at medium speed; Y4 Open/close door low speed; Y5 Open/close door high speed; Y6 Automatic door opening light flashes; Y7 Auto close light flashes; Y10 Door open/close reminder; Y11 Fault warning light; Y12 Automatic door opening; Y13 Automatic closing; Y14 Abnormal stop.

#### 摘录 E

- 出处：第 5 页，Table 2 Action result
> X1 ON The program jumps to automatic, the automatic door starts automatically. X2, X3 ON Y12 automatic door opening, Y6 automatic door opening light flashing action. X4 OFF Y13 automatically closes and stops, Y12 automatically opens the door.

#### 摘录 F

- 出处：第 5 页，Table 2 Action result
> X5 ON Y13 automatic door closing stops, Y7 door closing light stops flashing. X6 ON Y12 automatic door closing stops, Y6 door closing light stops flashing.

#### 摘录 G

- 出处：第 5 页，Table 2 Action result
> X11 ON When X1 is OFF, Y1 manually opens door. X12 ON When X1 is OFF, Y2 manually closes the door. X14 ON Exception elimination.

### 2. 基于原文整理后的自然语言描述

The intelligent garage-door controller has an explicit mode switch between manual and automatic operation. In automatic mode, a vehicle approach or departure detected by the inside or outside sensors causes the PLC to enter the automatic opening branch, energize `Y12`, and flash the opening indicator `Y6`. During motion, the controller supervises multiple guards: the anti-pinch grating must remain normal, otherwise a closing action is interrupted and the door immediately re-enters the automatic opening branch. The open and lower limits terminate the corresponding opening or closing actions, while the controller also chooses medium, low, or high speed outputs through `Y3`, `Y4`, and `Y5` according to the configured door-motion stage. In manual mode, the same door can be opened or closed directly through `X11` and `X12`, and any abnormal condition can be cleared through the reset input `X14`.

### 3. 逐句溯源

1. 句子 1：The intelligent garage-door controller has an explicit mode switch between manual and automatic operation.
   对应摘录：C, E, G
2. 句子 2：In automatic mode, a vehicle approach or departure detected by the inside or outside sensors causes the PLC to enter the automatic opening branch, energize `Y12`, and flash the opening indicator `Y6`.
   对应摘录：B, C, D, E
3. 句子 3：During motion, the controller supervises multiple guards: the anti-pinch grating must remain normal, otherwise a closing action is interrupted and the door immediately re-enters the automatic opening branch.
   对应摘录：C, D, E
4. 句子 4：The open and lower limits terminate the corresponding opening or closing actions, while the controller also chooses medium, low, or high speed outputs through `Y3`, `Y4`, and `Y5` according to the configured door-motion stage.
   对应摘录：C, D, F
5. 句子 5：In manual mode, the same door can be opened or closed directly through `X11` and `X12`, and any abnormal condition can be cleared through the reset input `X14`.
   对应摘录：C, D, G
