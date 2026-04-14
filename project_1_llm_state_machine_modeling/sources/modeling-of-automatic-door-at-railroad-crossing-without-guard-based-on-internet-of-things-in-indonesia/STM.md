# Modeling of Automatic Door at Railroad Crossing Without Guard Based on Internet of Things in Indonesia - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `sensor1 到车 -> 关门 -> 显示等待时间 -> sensor2 离车 -> 开门` 主链和 `4.5 s` 微缩时序都写得很清楚，原文与描述都能稳定维持双 A。

## 条目 1: Dual-sensor waiting-time railway-crossing gate controller

- 控制对象：轨道交通与铁路控制领域的双 TCRT-5000 传感器列车到达/离开检测、等待时间显示与道口开闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向无值守铁路平交口的 IoT 门控系统，用两只 `TCRT-5000` 传感器分别负责来车检测与离车确认，再由 Arduino 和微型舵机执行关门、开门与等待时间显示。
- 判断：算。对象是真实道口门控控制器，原文明确给出了两只传感器的分工、开闭门动作、速度/等待时间显示，以及 `4.5 s` 微缩时序分解，不是只停留在硬件清单或平台介绍。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 46-58 行
> This study aims to create a sensor-based automatic door model and Internet of Things (IoT). The design of a miniature model of automatic railroad doorstop using SG90 9g micro servo with TCRT-5000 sensor based on Arduino Uno ATmega 328 microcontroller. The sensor is used to detect the position of the train, in miniatures that have been made using 2 TCRT-5000 sensors. The function of each sensor is to detect the arrival of the train, activate the speed and detection system that the train has passed through the doorstop. Miniature door bars are driven by 9g SG90 micro servo. Computer monitors in miniatures can function properly, which is capable of displaying train speed and waiting time for train arrival.

#### 摘录 B

- 出处：第 2 页，`2.1 Prototype Design`，`paper_content.txt` 第 88-94 行
> Placement of the sensor position on the actual train doorstop with a train speed of 90 km/h and the time of the doorstop closes the desired 4.5 minutes, with a 1-minute division of time the doorstop closes the alarm ON, 2.5 minutes after the doorstop closes the train passes, and 1 minute after the train passes sensor 2, the doorstop will open again.

#### 摘录 C

- 出处：第 5-7 页，`3.1 Hardware Designing / 4. Analysis and Discussion`，`paper_content.txt` 第 184-189、216-224 行
> TCRT-5000 sensor as a sensor for detecting train arrivals and when the train has passed through the doorstop, sensor identification will be received by Wemos D1 mini which will then be transmitted wifi to the Arduino Uno ATmega328 microcontroller which is received as info the train will pass through the crossing door. Then Arduino Uno will order a micro servo to close the crossing door.
>
> The functions of each sensor are as follows, sensor 1 as an input for the closing gate, sensor 2 as input for opening the door, and determining the waiting time for the arrival of the train. The position of the sensor is based on the time desired to process the door bar will close until the door bar opens.

#### 摘录 D

- 出处：第 7-9 页，`4.1 Functional Test / 5. Conclusion`，`paper_content.txt` 第 240-245、313-328 行
> Table 1 shows the results of system performance when the train is detected on sensor 1 and sensor 2.
> Train Position Door Cross Status
> Sensor 1 Close
> Sensor 2 Open
>
> The miniature design of automatic railroad doorstop uses SG90 9g micro servo with TCRT-5000 sensor based on Arduino Uno ATmega 328 microcontroller. The sensor is used to detect the position of the train, in miniatures that have been made using 2 TCRT-5000 sensors. ... The 4.5 seconds is the process of starting the door from closing, closing until the train passes. The time division is that the a1 sensor detects the coming train and 1 second the door bar closes, the a2 sensor detects the train 1 second to the time the train bar is open and 1 second after the doorstop closes the train will pass.

### 2. 基于原文整理后的自然语言描述

The controller uses two `TCRT-5000` sensors to organize the railway crossing into an arrival-triggered closing phase and a departure-triggered reopening phase. When `sensor 1` detects an incoming train, the detection information is transferred to the Arduino-based controller, which commands the `SG90` servo to close the barrier and starts the waiting-time display for road users. The paper explicitly assigns `sensor 2` to the reopening side of the logic, so once the train has passed the crossing and reaches the second sensor, the controller opens the barrier again. In the miniature implementation, the full close-pass-open cycle is timed as `4.5 s`: after `a1` detects the train, the bar closes in `1 s`, the train reaches `a2`, and the bar reopens `1 s` later, while the real-scale design target corresponds to a `4.5 minute` warning-and-passage window. Besides the barrier motion, the same controller also computes train speed and shows the waiting time for train arrival on the monitor.

### 3. 逐句溯源

1. 句子 1：The controller uses two `TCRT-5000` sensors to organize the railway crossing into an arrival-triggered closing phase and a departure-triggered reopening phase.
   对应摘录：A, C, D
2. 句子 2：When `sensor 1` detects an incoming train, the detection information is transferred to the Arduino-based controller, which commands the `SG90` servo to close the barrier and starts the waiting-time display for road users.
   对应摘录：A, C, D
3. 句子 3：The paper explicitly assigns `sensor 2` to the reopening side of the logic, so once the train has passed the crossing and reaches the second sensor, the controller opens the barrier again.
   对应摘录：A, C, D
4. 句子 4：In the miniature implementation, the full close-pass-open cycle is timed as `4.5 s`: after `a1` detects the train, the bar closes in `1 s`, the train reaches `a2`, and the bar reopens `1 s` later, while the real-scale design target corresponds to a `4.5 minute` warning-and-passage window.
   对应摘录：B, D
5. 句子 5：Besides the barrier motion, the same controller also computes train speed and shows the waiting time for train arrival on the monitor.
   对应摘录：A, C
