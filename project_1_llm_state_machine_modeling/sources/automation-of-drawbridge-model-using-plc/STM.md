# Automation of Drawbridge Model using by PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把来船检测、清桥、封闭道路、开桥、通船和复位道路交通写成了完整闭环，是通用桥梁机电控制里非常干净的双 A `EFSM + T0` 样本。

## 条目 1: Ship-detected drawbridge opening and barrier controller

- 控制对象：通用控制与桥梁机电领域的船舶检测、路障封闭与桥体升降控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个用 `PLC + proximity sensor + ultrasonic sensor + DC motor + servo motor + signal pole` 构成的自动开桥与道路封控控制器。
- 判断：算。对象是实际桥梁交通控制系统，原文明确写出了船舶到达、桥面检测、关路障、开桥、船过桥、关桥和恢复道路放行的顺序链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 17-26 行
> The main objective of this project is to allow passage to huge gigantic cargo ships ... The idea is to automate the process of ship detection, opening or closing of a bridge, controlling the signals and road barriers. ... With the help of Ultrasonic sensor, Proximity sensor the arrival and leaving of the system is Monitored and bridge is operated accordingly.

#### 摘录 B

- 出处：第 2 页，`Introduction`，`paper_content.txt` 第 68-71 行
> Proximity sensor is used to know the ship position. ... Ship is detected by Proximity sensor which is placed at certain distance from the bridge. Sensor output provides input to the PLC and it’ll drive DC motor, Servo motor and Signal Poles according to programming.

#### 摘录 C

- 出处：第 5-7 页，`System Components & Design / Traffic Control System`，`paper_content.txt` 第 196-217 行、第 252-262 行、第 292-300 行
> In this model two 24V PNP proximity sensors are used for detecting arrival and leaving of ship.
>
> In this project two ultrasonic sensors along with their receivers are used to detect the traffic on the bridge. ... Servo motor is used to opening and closing of bridge according to signal of proximity and ultrasonic sensor.
>
> When ship will be detected it sends high to low pulse to PLC ... As soon as PLC gets high to low signal it drives the DC to close road barriers and signal changes from green to red. Then after PLC drives Servo motor to open the bridge ... As soon as ship passes through the bridge ... PLC first drives Servo motor in reverse direction until bridge is totally closed. Then road barrier will be opened and signal changes from red to green.

### 2. 基于原文整理后的自然语言描述

The drawbridge controller begins in a road-open state with the bridge deck closed, the road barriers open, and vehicle green active. When the arrival proximity sensor detects a ship, the PLC checks the bridge deck with ultrasonic sensing, clears traffic, closes the road barriers, and changes the vehicle signal from green to red. It then drives the bridge-opening actuator and keeps monitoring the ship path until the departure sensor confirms that the vessel has passed. After departure, the controller reverses the bridge actuator to close the span, reopens the road barriers, restores vehicle green, and returns the ship side to red.

### 3. 逐句溯源

1. 句子 1：The drawbridge controller begins in a road-open state with the bridge deck closed, the road barriers open, and vehicle green active.
   对应摘录：A, B, C
2. 句子 2：When the arrival proximity sensor detects a ship, the PLC checks the bridge deck with ultrasonic sensing, clears traffic, closes the road barriers, and changes the vehicle signal from green to red.
   对应摘录：A, C
3. 句子 3：It then drives the bridge-opening actuator and keeps monitoring the ship path until the departure sensor confirms that the vessel has passed.
   对应摘录：B, C
4. 句子 4：After departure, the controller reverses the bridge actuator to close the span, reopens the road barriers, restores vehicle green, and returns the ship side to red.
   对应摘录：C
