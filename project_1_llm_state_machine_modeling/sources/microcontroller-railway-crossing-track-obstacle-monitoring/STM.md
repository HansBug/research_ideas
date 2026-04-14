# Microcontroller-Based Automatic Railway Crossing Control and Track Obstacle Monitoring System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口门控、红绿灯/蜂鸣提醒、障碍停车与 GSM 告警写成完整传感器驱动事件链，足以支撑铁路平交口双 A 样本。

## 条目 1: Sensor-triggered crossing controller with obstacle-stop GSM alert

- 控制对象：轨道交通与铁路控制领域的铁路平交口闸门与障碍告警控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Arduino 的铁路道口自动门控控制器，用两侧 IR 传感器检测列车到达/离开，并用车头超声波检测障碍、触发停车和 GSM 告警。
- 判断：算。对象是真实平交口控制链，不是单纯装置说明；原文明确给出了到达、关门、报警、离开、开门以及障碍停车/告警的输入输出链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / System Description，`paper_content.txt` 第 11-20、52-59 行
> This paper proposes replacing manual operations with an automated railway gate system utili sing Arduino, Sensors, Servo Motors, Buzzers and GSM modules ... When a train approaches, the gate closes automatically ... Once the train departs, the gate reopens ... The system employs infrared sensors to mo nitor train arrival and departure, ultrasonic sensors for obstacle detection, and Arduino to manage gate operation and messaging.
>
> As soon as a train is sensed to be incoming, the sys tem switches the traffic indicator to red and ensures the gate remains closed until the railway crossing is clear. Upon detecting the train’s departure, the controller changes the traffic light to green and activates the servo motor to open the gate.

#### 摘录 B

- 出处：第 4 页，`Fig 3 Flow chart for automatic railway gate control`，`paper_content.txt` 第 113-118 行
> At the beginning, the train module which consists of two (IR) transmitter -receiver sensors to detect both the arrival and departure of the train s. When a train approaches, the t rain sensor -1 is triggered, sending a ‘HIGH’ signal. This activates the Buzzer and Light indicat ors to alert road users, and the gate is ‘CLOSED’ by the servo motor. Once the tra in depart s the crossing, then the train sensor -1 deactivates, and the train sensor -2 is triggered, and its output goes ‘HIGH’. This signal turns ‘OFF’ the Buzzer and Light indicators, and the gate is ‘OPENED’ by the servo motor, allowing normal traffic flow.

#### 摘录 C

- 出处：第 4-5 页，`Fig 4 Flowchart for obstacle detection system` / Prototype evaluation，`paper_content.txt` 第 121-123、137-142、153-154 行
> In the system, an ultrasonic sensor is mounted at the front of the train to detect any obstacles on the track. If an obstacle is detected, the sensor’s output becomes ‘HIGH’, prompting the train to stop. Simultaneously, a notification about the obstacle is sent to predefined number with the help of the GSM module at the nearby railway station, and the gate automatically closes via ...
>
> For gate operation, IR sensors are positioned 35 cm on each side of the cro ssing. When the toy train triggers the first sensor, the system activates a RED LED to warn the traffic and closes the gate by using the servo motor. The gate reopens and the LED tur ns off once the train’s departure is sensed by the second IR sensor.
>
> In the obstacle detection part, the ultrasonic sensor sensed the obstacle, and t he train stops as soon as the obstacle detection message is conveyed to the nearby railway station, as well as to the train operator.

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller is an Arduino-based EFSM whose main event sources are two IR train sensors around the crossing and an ultrasonic obstacle sensor mounted on the train. When the arrival-side IR sensor goes `HIGH`, the controller turns on the buzzer and warning lights, switches the road signal to red, and drives the servo motor to close the gate. The protected crossing state persists until the departure-side IR sensor is triggered, at which point the buzzer and lights are turned off, the road signal returns to green, and the servo reopens the barrier. In parallel with that arrival/departure loop, the obstacle-monitoring branch watches the ultrasonic sensor, and whenever it reports an obstacle the train is stopped immediately, the gate is forced closed, and a GSM alert is sent to the nearby railway station or train operator. The prototype description also fixes the sensor layout by placing the two IR sensors `35 cm` from the crossing on each side, so the paper preserves both the logical transition chain and its concrete engineering realization.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller is an Arduino-based EFSM whose main event sources are two IR train sensors around the crossing and an ultrasonic obstacle sensor mounted on the train.
   对应摘录：A, B, C
2. 句子 2：When the arrival-side IR sensor goes `HIGH`, the controller turns on the buzzer and warning lights, switches the road signal to red, and drives the servo motor to close the gate.
   对应摘录：A, B
3. 句子 3：The protected crossing state persists until the departure-side IR sensor is triggered, at which point the buzzer and lights are turned off, the road signal returns to green, and the servo reopens the barrier.
   对应摘录：A, B
4. 句子 4：In parallel with that arrival/departure loop, the obstacle-monitoring branch watches the ultrasonic sensor, and whenever it reports an obstacle the train is stopped immediately, the gate is forced closed, and a GSM alert is sent to the nearby railway station or train operator.
   对应摘录：C
5. 句子 5：The prototype description also fixes the sensor layout by placing the two IR sensors `35 cm` from the crossing on each side, so the paper preserves both the logical transition chain and its concrete engineering realization.
   对应摘录：C
