# PLC Based Intelligent Traffic Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文直接说明了传感器检测、优先级判断、相位顺序与中断/定时两类触发条件，可作为干净的交通灯控制样本。

## 条目 1: Priority-Based Signal Phasing with Sensor Interrupts
- 控制对象：PLC 智能交通信号控制器

### 0. 条目识别与判定

- 一句话说明：这是道路交通信号控制领域的智能交通灯控制器，用于根据车辆检测结果决定各方向相位优先级和放行时长。
- 判断：算。对象是实际交通灯控制系统，原文给出了传感器检测、优先级计算和相位开放顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 26-32 行
> The PLC checks the status of the sensors. The system resolution is depend on the output provided by the sensors, Then PLC checks the priorities and then provide output signal to the traffic lights poles for ON or OFF the Red, yellow or Green lights and ON time is depend on the specific priorities. The roads are opened in that manner that east road, west road, north road and then south road is open.

#### 摘录 B
- 出处：第 1 页，Section 2.1 Traffic Control System，`paper_content.txt` 第 83-100 行
> The ability to collect the information of the busy tracks by sensors and providing the output to PLC. The ability to take decision against the information and change the time according to the priorities. ... The signal phases and cycle length are depend on the traffic flow on the desired track. The system responds to interrupts or timing base system and open the desired signal according to the priority requirement.

### 2. 基于原文整理后的自然语言描述

The PLC traffic controller reads the lane sensors, evaluates the resulting priorities, and drives the red, yellow, and green outputs accordingly. The sequence of road opening follows a defined phase order, and the ON time of each signal depends on the current priority level. The controller can therefore change its cycle length from traffic-flow information and open the desired signal either on interrupt conditions or on the timing base system.

### 3. 逐句溯源

1. 句子 1：The PLC traffic controller reads the lane sensors, evaluates the resulting priorities, and drives the red, yellow, and green outputs accordingly.
   对应摘录：A
2. 句子 2：The sequence of road opening follows a defined phase order, and the ON time of each signal depends on the current priority level.
   对应摘录：A
3. 句子 3：The controller can therefore change its cycle length from traffic-flow information and open the desired signal either on interrupt conditions or on the timing base system.
   对应摘录：B
