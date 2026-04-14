# Implementation of Automatic Gate Control for Railroad Switch and Anti-Collision - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把列车接近告警、落杆、门间障碍检测、开杆和对控制室/司机广播的链路写得较清楚，并给出了额外的换轨与防撞保护上下文，能形成双 A 的铁路道口保护样本。

## 条目 1: Crossing-Gate and Obstacle-Broadcast Protection Controller

- 控制对象：轨道交通与铁路控制领域的道口门控与障碍广播保护控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个铁路平交口保护系统，使用超声波传感器、蜂鸣器、伺服门机与无线广播模块，在列车接近、门间障碍出现和列车离开时执行不同的门控与告警动作。
- 判断：算。对象是实际 railway crossing protection controller，不是纯方法流程；原文明确给出列车接近、落杆、障碍广播、列车通过后开杆等具体控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，问题与系统组成说明，`paper_content.txt` 第 88-99 行
> This paper describes controlling method of railway gates accurately by automation technique at crossing, and making use of sensors and actuators. Main sensors and actuators used in this paper are notably IR sensors or ultrasonic sensor and buzzers, LED display, servo motors respectively ... The above mentioned problems are solved by Anti-collision system using ultrasonic sensor and motor, which gives the information to the pilot.

#### 摘录 B

- 出处：第 3 页，`Working of an automatic railway gate controlling system`，`paper_content.txt` 第 201-239 行
> By using this system at the level crossing the arrival or departure can be determine using Ultrasonic sensor. The opening or closing of the level crossing gates automatically with the help of microcontroller and servo motors. Warning signals are given near roads using Buzzer sound.
>
> The ultrasonic sensors are used on sides of gate at about 4km from crossing. As soon as train arrival is detected, the detected signal is sent to microcontroller. Based on that signal, the microcontroller will turn on buzzer for warning ... and sends the actuation information for closing the gate to the servo motors.
>
> If no obstacle is sensed between the crossing gates, the train passes as usual. Another sensor which is on either side of gate detects the departure of the train ... it sends the actuation signal for opening the gate.

#### 摘录 C

- 出处：第 4-5 页，`Anti-collision system / flow of Anti-collision system`，`paper_content.txt` 第 346-372、385-392 行
> IR sensor is placed at 3km from the anti-collision system, once IR sensor senses the coming of the train, it transfer the information to the controller to activate the anti-collision system.
>
> An anti-collision system is made using ultrasonic sensor and servo motor, where ultrasonic sensor senses the obstacles on the track and the servo motor is used to rotate the ultrasonic sensor for 0 to 180 degree.
>
> If the obstacle is present on the track it will send the information about the obstacle on the track using nRF24L01 transceiver, to the present train on that track as well as nearest control room.
>
> Step 1: If train enters the specified range turns on the anti-collision system via LED indication.
> Step 2: If the obstacles present on railway track ... ultrasonic sensor senses for the obstacles on the track ...

### 2. 基于原文整理后的自然语言描述

The railway-crossing protection controller combines level-crossing gate automation with obstacle-broadcast protection by coordinating sensors, buzzers, servo motors, and wireless messaging. When a train is detected about `4 km` before the crossing, the microcontroller turns on the road-warning buzzer and commands the servo-driven gates to close, then broadcasts the gate-closed status to the control room and the loco-pilot. If a vehicle or another obstacle is trapped between the crossing gates, the ultrasonic sensing path raises an obstacle report instead of treating the passage as clear; the broader anti-collision subsystem activates around `3 km` before the protected zone and can rotate its ultrasonic sensor through `0` to `180` degrees to scan the track and transmit the obstacle message through `nRF24L01`. After the train departs and the side sensor detects clearance, the controller issues the opening actuation and restores the crossing to its open state.

### 3. 逐句溯源

1. 句子 1：The railway-crossing protection controller combines level-crossing gate automation with obstacle-broadcast protection by coordinating sensors, buzzers, servo motors, and wireless messaging.
   对应摘录：A, B, C
2. 句子 2：When a train is detected about `4 km` before the crossing, the microcontroller turns on the road-warning buzzer and commands the servo-driven gates to close, then broadcasts the gate-closed status to the control room and the loco-pilot.
   对应摘录：B
3. 句子 3：If a vehicle or another obstacle is trapped between the crossing gates, the ultrasonic sensing path raises an obstacle report instead of treating the passage as clear; the broader anti-collision subsystem activates around `3 km` before the protected zone and can rotate its ultrasonic sensor through `0` to `180` degrees to scan the track and transmit the obstacle message through `nRF24L01`.
   对应摘录：B, C
4. 句子 4：After the train departs and the side sensor detects clearance, the controller issues the opening actuation and restores the crossing to its open state.
   对应摘录：B
