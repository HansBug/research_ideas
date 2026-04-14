# Traffic Light Control System for Emergency Vehicles Using Radio Frequency - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟、协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了正常灯序、RF 触发抢占、应急灯序执行以及恢复正常序列的控制过程。

## 条目 1: RF-Triggered Emergency Sequence Override
- 控制对象：道路交通信号领域的应急车辆无线优先控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互、显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G2 应急车辆交通灯优先）

### 0. 条目识别与判定
- 一句话说明：这是一个基于 RF 发射器/接收器的交通灯控制器，用于在应急车辆发送无线信号时抢占当前灯序，为指定方向开绿灯并在结束后恢复正常循环。
- 判断：算。对象是实际交通灯控制系统，正文直接区分了 normal sequence 和 emergency mode sequence。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 16-24
> This system was designed to be operated when it received signal from emergency vehicles based on radio frequency (RF) transmission ... microcontroller to change the sequence back to the normal sequence before the emergency mode was triggered. ... function with the sequence mode of traffic light when emergency vehicles passing by an intersection and changing the sequence back to the normal sequence before the emergency mode was triggered.

#### 摘录 B
- 出处：第 8 页，Normal Sequence, 行 272-283
> The sequence of the traffic lights started as green light of traffic light 1 and red light of other traffic lights are on. The duration for this mode lasted for 30 seconds unless the RF receiver triggers any signal from the transmitter to override the sequence. ... Then, the green light of traffic light 1 is off and the yellow light of the same traffic light is on for 2 seconds. ... The same thing happened to the traffic light 3 and traffic light 4 after an interval of the yellow light of each traffic light is on for 2 seconds.

#### 摘录 C
- 出处：第 6-9 页，RF transmitter / Emergency Mode Sequence，行 229-247, 308-321
> A set of four push-on switches is used in the RF transmitter circuit. Each switch labeled with number 1, 2, 3, and 4 to indicate which traffic light at the intersection. These switch need to be push (switch on) in order to trigger the emergency sequence mode of the traffic light intersection. ... The emergency mode is triggered when the RF receiver received the transmitted signal from the RF transmitter to override the normal sequence. For example, an ambulance arrives at the traffic light 4 and the green light of the traffic light 1 is on ... the yellow of traffic light 1 is on for 2 seconds. Then the green of traffic light 4 is on for 10 seconds and then the yellow light of the same traffic light is turned on for 2 seconds.

#### 摘录 D
- 出处：第 9 页，Emergency Mode Sequence，行 319-321
> The emergency sequence mode is ended when the sequence of the traffic light is back to the normal sequence which the green light of traffic light 1 is turned back on for the remaining time before the emergency sequence mode is triggered.

### 2. 基于原文整理后的自然语言描述

In normal operation, the controller cycles the four-way intersection so that each traffic light gets a 30-second green interval followed by a 2-second yellow interval before the next light takes its turn. The RF transmitter has four push-on switches, one for each traffic light, and pressing a switch sends a coded 434 MHz signal to the RF receiver to override the current sequence. In the illustrated emergency case, if traffic light 1 is currently green and switch 4 is pressed, the controller first turns traffic light 1 yellow for 2 seconds, then turns traffic light 4 green for 10 seconds, and then turns traffic light 4 yellow for 2 seconds. After the emergency sequence ends, the controller returns to the normal sequence and restores traffic light 1 for the remaining time that was left before the override.

### 3. 逐句溯源

1. 句子 1：In normal operation, the controller cycles the four-way intersection so that each traffic light gets a 30-second green interval followed by a 2-second yellow interval before the next light takes its turn.
   对应摘录：B
2. 句子 2：The RF transmitter has four push-on switches, one for each traffic light, and pressing a switch sends a coded 434 MHz signal to the RF receiver to override the current sequence.
   对应摘录：C
3. 句子 3：In the illustrated emergency case, if traffic light 1 is currently green and switch 4 is pressed, the controller first turns traffic light 1 yellow for 2 seconds, then turns traffic light 4 green for 10 seconds, and then turns traffic light 4 yellow for 2 seconds.
   对应摘录：C
4. 句子 4：After the emergency sequence ends, the controller returns to the normal sequence and restores traffic light 1 for the remaining time that was left before the override.
   对应摘录：D
