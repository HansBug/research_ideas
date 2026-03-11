# Traffic Light Control System for Emergency Vehicles Using Radio Frequency - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了正常灯序、RF 触发抢占、应急灯序执行以及恢复正常序列的控制过程。

## 条目 1: RF-Triggered Emergency Sequence Override
- 控制对象：道路交通信号领域的应急车辆无线优先控制器

### 0. 条目识别与判定
- 一句话说明：这是一个基于 RF 发射器/接收器的交通灯控制器，用于在应急车辆发送无线信号时抢占当前灯序，为指定方向开绿灯并在结束后恢复正常循环。
- 判断：算。对象是实际交通灯控制系统，正文直接区分了 normal sequence 和 emergency mode sequence。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 16-24
> This system was designed to be operated when it received signal from emergency vehicles based on radio frequency (RF) transmission ... microcontroller to change the sequence back to the normal sequence before the emergency mode was triggered. ... function with the sequence mode of traffic light when emergency vehicles passing by an intersection and changing the sequence back to the normal sequence before the emergency mode was triggered.

#### 摘录 B
- 出处：第 8 页，Normal Sequence, 行 272-276
> The sequence of the traffic lights started as green light of traffic light 1 and red light of other traffic lights are on. The duration for this mode lasted for 30 seconds unless the RF receiver triggers any signal from the transmitter to override the sequence.

#### 摘录 C
- 出处：第 8-9 页，Emergency Mode Sequence, 行 308-318
> The emergency mode is triggered when the RF receiver received the transmitted signal from the RF transmitter to override the normal sequence ... The emergency sequence mode started when the yellow of traffic light 1 is on for 2 seconds. Then the green of traffic light 4 is on for 10 seconds and then the yellow light of the same traffic light is turned on for 2 seconds.

### 2. 基于原文整理后的自然语言描述

In normal operation, the controller keeps traffic light 1 green and the other traffic lights red for 30 seconds unless an RF signal arrives from an emergency vehicle. When the RF receiver gets the transmitted signal, the controller overrides the normal sequence and enters the emergency mode sequence. In the illustrated case, the controller first turns traffic light 1 yellow for 2 seconds, then turns traffic light 4 green for 10 seconds, and then turns traffic light 4 yellow for 2 seconds before returning to the normal sequence.

### 3. 逐句溯源

1. 句子 1：In normal operation, the controller keeps traffic light 1 green and the other traffic lights red for 30 seconds unless an RF signal arrives from an emergency vehicle.
   对应摘录：B
2. 句子 2：When the RF receiver gets the transmitted signal, the controller overrides the normal sequence and enters the emergency mode sequence.
   对应摘录：A, C
3. 句子 3：In the illustrated case, the controller first turns traffic light 1 yellow for 2 seconds, then turns traffic light 4 green for 10 seconds, and then turns traffic light 4 yellow for 2 seconds before returning to the normal sequence.
   对应摘录：A, C
