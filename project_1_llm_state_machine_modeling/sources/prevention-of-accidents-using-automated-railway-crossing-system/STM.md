# Prevention of Accidents using Automated Railway Crossing System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 1.5 km 预告警、落杆、门间障碍检查、减速/停车和列车离开后的开杆链路写成了可追溯的铁路道口控制逻辑，能形成双 A 样本。

## 条目 1: IR-Guided Obstacle-Checked Railway Crossing Controller

- 控制对象：轨道交通与铁路控制领域的自动铁路道口门控与障碍检查控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Arduino Nano 和 IR 传感器的铁路道口控制器，在列车接近时关闭栏杆并报警，在检测到门间障碍时减速或停车列车，在列车离开后重新开杆。
- 判断：算。对象是实际 railway crossing controller，原文直接给出了传感器布设、驱动器/电机、障碍检查和开闭门数据流。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`III. PROPOSED SYSTEM`，`paper_content.txt` 第 145-159 行
> The proposed system detects the train by using IR sensors. The DC motor is driven by using a L293d (motor driver) and an Arduino Nano with Atmega328P microcontroller is used to control the device.
>
> The arrival of the train is detected by an IR sensor which is placed 1.5km away from the railway gate, then the microcontroller will issue a command to close the gate with an alarm/siren.
>
> Upon receiving the information about the arrival of the train the system checks for obstacles that are preventing the closure of gates, then the micro-controller will issue a command to the railway signal which alerts the train and the speed of the train is mechanically decreased or if the gap is implausibly less the train is stopped.

#### 摘录 B

- 出处：第 3 页，系统组件说明，`paper_content.txt` 第 163-188 行
> For opening and closing of the gates, a L293D motor driver is used to run the gate motor in both forward and backward direction.
>
> 1)To identify the arrival as well as the departure of the train.
> 2)A L293D motor driver and DC motor are used to operate the railway gates.
> 3)Alert the vehicles near the railway gate about the arrival of the train using an alarm.
> 4)To control the Red, Green, Yellow signal lights at railway crossing.
>
> The sensors act as an input unit placed at a quite a distance from the ends of railway gates. These sensors are responsible for the detection of arrival and departure of trains.

#### 摘录 C

- 出处：第 4 页，`Flow chart depicting dataflow`，`paper_content.txt` 第 232-241 行
> Once the train is detected the command passes to the microcontroller. The system checks for obstacles when the IR sensor detects the train. If obstacles are found, then the train is slowed down and the alarm starts ringing. If no obstacle is detected, then the gates are closed. After the departure of the train, the gates are opened.

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller uses IR sensors placed away from the gate ends to detect both train arrival and departure, and it is coordinated by an Arduino Nano with an `ATmega328P` microcontroller. When the arrival sensor located about `1.5 km` before the gate detects the train, the controller starts the alarm and issues a closing command to the gate motor through the `L293D` driver. Before completing the closure path, the same controller checks whether a vehicle or another obstacle is blocking the gates; if an obstacle is present it alerts the train by railway signal and mechanically slows or stops the train instead of blindly closing the crossing. If no obstacle is detected, the gates are closed normally, and once the departure event is sensed the controller opens the gates again.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller uses IR sensors placed away from the gate ends to detect both train arrival and departure, and it is coordinated by an Arduino Nano with an `ATmega328P` microcontroller.
   对应摘录：A, B
2. 句子 2：When the arrival sensor located about `1.5 km` before the gate detects the train, the controller starts the alarm and issues a closing command to the gate motor through the `L293D` driver.
   对应摘录：A, B
3. 句子 3：Before completing the closure path, the same controller checks whether a vehicle or another obstacle is blocking the gates; if an obstacle is present it alerts the train by railway signal and mechanically slows or stops the train instead of blindly closing the crossing.
   对应摘录：A, C
4. 句子 4：If no obstacle is detected, the gates are closed normally, and once the departure event is sensed the controller opens the gates again.
   对应摘录：B, C
