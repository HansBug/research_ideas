# Automated Railway Crossing System Using Multi-Sensor Integration for Enhanced Safety - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口栏杆控制写成了完整的多传感器事件链，覆盖关门、障碍保持、开门、手动旁路和急停，足够支撑双 A 提取。

## 条目 1: Obstacle-Aware Railway Crossing Gate Supervisor

- 控制对象：轨道交通与铁路控制领域的多传感器道口门控与告警控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个以 Arduino Nano 为主控、用多组 IR 传感器控制铁路道口栏杆、道路信号灯、蜂鸣器和控制室告警灯的安全控制系统。
- 判断：算。对象是实际道口控制系统，正文给出了接近、关门、障碍保持、开门、手动控制和急停的可追溯控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 27-35 行
> our project proposes a cutting-edge automated gate control system for railways that opens and closes the rail crossing gates automatically whenever a train is approaching. The system is equipped with advanced features such as obstacle detection, manual control override, and an emergency stop mechanism. ... the suggested system offers a safe and intelligent solution

#### 摘录 B

- 出处：第 2 页，Section 1 `Introduction`，`paper_content.txt` 第 62-78 行
> 1) Automated Detection: Multiple IR sensors detect train arrival and departure to trigger gate control.
> 2) Obstacles Detection under Gate: An IR sensor beneath the gate halts closure if any obstacle is detected.
> 3) Manual control Buttons: Dedicated buttons simulate IR triggers for emergency manual control.
> 4) Emergency Stop Button: In case of emergencies, an emergency stop button can instantly halt system activities.
> ...
> 6) Control Room Indicators: LED indicators in a central control room identify which gate is malfunctioning or facing delays

#### 摘录 C

- 出处：第 5 页，Section 3.4 `Operational Flowchart`，`paper_content.txt` 第 263-278 行
> IR1 & IR2: When both sensors are sensing the train at the gate, the gate will slowly close, the red LED will glow, and the buzzer will beep.
> IR3 & IR4: When both sensors are detecting the train at the exit point, then the gate opens slowly, the red LED is off, the buzzer is off, and the green LED is on.
> IR5 (Obstacle Detection): Activated when the gate is closing. If any object (vehicle or human) is detected under the gate, it halts immediately, and both red LEDs and the control room light start blinking along with the buzzer until the path is cleared.
> Manual Operation: Button 1 simulates IR1 and IR2 to close the gate manually. Button 2 simulates IR3 and IR4 to open the gate.
> Emergency Stop: Pressing this switch instantly shuts down all system operations. Pressing again restarts it.

#### 摘录 D

- 出处：第 6 页，Section 3.4 / 4 `Operational Flowchart / Prototype Design`，`paper_content.txt` 第 286-304 行
> It starts with the power-up of Arduino and initializing the output devices as well as sensors. IR sensors are used to detect incoming trains, trigger the buzzer, lower the crossbar via a servo motor, and turn on the red traffic light. If it finds a stranded vehicle on the track, it triggers an emergency alert. After the train has passed, the system lifts the crossbar, releases alarms, and returns to standby mode, ever vigilant for incoming train signals.
>
> The detection of train arrival and departure by the IR sensor reliably closed and opened the gate successfully. Obstacle detection (IR5) reacts immediately when an obstacle is detected, stopping the gate from closing and triggering an alarm. Manual and emergency controls operate as intended

### 2. 基于原文整理后的自然语言描述

The crossing controller initializes its sensors and outputs in a standby mode and then waits for the train-detection IR sensors to signal an approaching train. When `IR1` and `IR2` detect the train at the gate, the controller closes the barrier, turns on the red traffic indication, and sounds the buzzer. While the barrier is closing, `IR5` acts as an obstacle guard: if a vehicle or person is detected under the gate, closure halts immediately and both the red LEDs and the control-room indicator keep blinking with the buzzer until the path is clear. When `IR3` and `IR4` detect the train at the exit point, the controller opens the gate, turns the red indication and buzzer off, and enables the green clearance light. The same control chain can be invoked manually through close/open buttons, and an emergency-stop button can shut down all system activity until it is pressed again to restart.

### 3. 逐句溯源

1. 句子 1：The crossing controller initializes its sensors and outputs in a standby mode and then waits for the train-detection IR sensors to signal an approaching train.
   对应摘录：A, B, D
2. 句子 2：When `IR1` and `IR2` detect the train at the gate, the controller closes the barrier, turns on the red traffic indication, and sounds the buzzer.
   对应摘录：B, C, D
3. 句子 3：While the barrier is closing, `IR5` acts as an obstacle guard: if a vehicle or person is detected under the gate, closure halts immediately and both the red LEDs and the control-room indicator keep blinking with the buzzer until the path is clear.
   对应摘录：B, C, D
4. 句子 4：When `IR3` and `IR4` detect the train at the exit point, the controller opens the gate, turns the red indication and buzzer off, and enables the green clearance light.
   对应摘录：C, D
5. 句子 5：The same control chain can be invoked manually through close/open buttons, and an emergency-stop button can shut down all system activity until it is pressed again to restart.
   对应摘录：B, C
