# Design and Construction of Automatic Railway Crossing Gate Control Using Proximity and Infrared Sensors Based on Omron CP1E E30-SDRA PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口 arrival/departure 检测、下杆、限位保持和离站反转抬杆链写成了完整输入-动作-输出序列，可作为铁路门控双 A 样本。

## 条目 1: Arrival-limit-departure railway crossing gate controller

- 控制对象：基于 Omron PLC 的铁路道口栏杆门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路平交口自动门控控制器，用 proximity/infrared arrival-departure 传感器、PLC、PWM、电机、限位开关、蜂鸣器和 LED 完成下杆保持与抬杆恢复。
- 判断：算。对象是实际铁路道口门控系统，原文直接说明 arrival sensor、departure sensor、limit switch、motor、buzzer 和 LED 的联动次序。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 16-24 行
> The prototype of the automatic railway crossing controller uses proximity and infrared sensors to detect the arrival and departure of trains. When the infrared or proximity sensor detects the arrival of a train, the Programmable Logic Controller (PLC) activates Pulse Width Modulation (PWM), buzzer, and Light Emitting Diode (LED), so that the crossing motor goes down. After the crossing touches the limit switch, the motor stops and the buzzer and Light Emitting Diode (LED) remain on. The infrared or proximity sensor detects the departure of the train so that it reverses the motor so that the crossing goes up, then turns off the buzzer and Light Emitting Diode (LED).

#### 摘录 B

- 出处：第 1-2 页，Introduction，`paper_content.txt` 第 33-45 行
> This research focuses on designing and constructing an automatic railway crossing gate control system utilizing proximity and infrared sensors, managed by the Omron CP1E E30-SDRA Programmable Logic Controller (PLC).
>
> Proximity sensors detect the presence of trains and trigger the gate mechanism accordingly. ... Meanwhile, infrared sensors serve to enhance safety by providing an additional layer of detection.

#### 摘录 C

- 出处：第 4 页，`3.1 How The Design and Construction of Automatic Train Doorstops Works / 3.2 Flow Chart Diagram`，`paper_content.txt` 第 121-130 行
> The hardware uses two types of sensors, namely infrared sensors and proximity sensors such as train arrival and departure sensors, DC motors to open and close door covers, buzzers and LED alarms such as train alarms. The CP1E-E30 SDR-A PLC processes sensor signals and can open and close doors and provide warnings to the train.
>
> After the departure sensor detects a train passing, the DC motor then reverses direction to raise the barrier.

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller monitors train arrival and departure through proximity and infrared sensors and uses the Omron PLC as the central event-processing unit. When an approaching train is detected, the PLC activates PWM, the buzzer, and the LED alarm and drives the crossing motor downward so the barrier closes. Once the barrier reaches the limit switch, the motor stops while the warning outputs remain active to hold the closed state during train passage. After the departure sensor detects that the train has passed, the PLC reverses the motor direction to raise the barrier and then turns the buzzer and LED off, yielding an arrival-close-hold-depart-reopen control cycle.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller monitors train arrival and departure through proximity and infrared sensors and uses the Omron PLC as the central event-processing unit.
   对应摘录：A, B, C
2. 句子 2：When an approaching train is detected, the PLC activates PWM, the buzzer, and the LED alarm and drives the crossing motor downward so the barrier closes.
   对应摘录：A
3. 句子 3：Once the barrier reaches the limit switch, the motor stops while the warning outputs remain active to hold the closed state during train passage.
   对应摘录：A
4. 句子 4：After the departure sensor detects that the train has passed, the PLC reverses the motor direction to raise the barrier and then turns the buzzer and LED off, yielding an arrival-close-hold-depart-reopen control cycle.
   对应摘录：A, C
