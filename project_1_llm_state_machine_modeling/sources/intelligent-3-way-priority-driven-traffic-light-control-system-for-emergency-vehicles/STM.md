# Intelligent 3-Way Priority-Driven Traffic Light Control System for Emergency Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了 RFID 检测、优先判定、放行绿灯和恢复常规灯序的完整应急优先控制链。

## 条目 1: RFID-Based Emergency Priority Sequence
- 控制对象：道路交通信号领域的三路口应急车辆优先控制器

### 0. 条目识别与判定
- 一句话说明：这是一个基于 RFID 的三路口交通灯控制器，用于在检测到应急车辆接近时为其分配优先级、开放绿灯并在车辆通过后恢复常规时序。
- 判断：算。对象是实际交通灯控制系统，原文直接给出了检测、赋权、绿灯放行和恢复正常序列的控制链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract, 行 27-38
> The purpose of the system was to facilitate the operation of a 3-way traffic control light and provide priority to emergency vehicles using a Radio Frequency Identification (RFID) sensor ... The implemented prototype utilizes RFID transmission, operates in conjunction with the sequential mode of traffic lights to alter the traffic light sequence accordingly and reverts the traffic lights back to their normal sequence after the emergency vehicle has passed the traffic lights.

#### 摘录 B
- 出处：第 3-4 页，system overview, 行 150-164
> Each emergency vehicle is equipped with an RFID tag that transmits a unique identifier. It provides the capability for priority detection when an emergency vehicle approaches an intersection. The RFID reader at the traffic light detects the RFID tag and identifies the vehicle as an emergency vehicle requiring priority access ... ensuring that the vehicle receives a green signal at the traffic light, allowing it to pass through the intersection without delay.

### 2. 基于原文整理后的自然语言描述

The three-way traffic-light controller uses RFID technology to detect an approaching emergency vehicle at the intersection. When the traffic-light RFID reader identifies the vehicle's RFID tag, the controller assigns priority to that vehicle and changes the signal so that the emergency approach receives green. After the emergency vehicle passes through the intersection, the traffic lights revert to their normal sequential mode.

### 3. 逐句溯源

1. 句子 1：The three-way traffic-light controller uses RFID technology to detect an approaching emergency vehicle at the intersection.
   对应摘录：A, B
2. 句子 2：When the traffic-light RFID reader identifies the vehicle's RFID tag, the controller assigns priority to that vehicle and changes the signal so that the emergency approach receives green.
   对应摘录：B
3. 句子 3：After the emergency vehicle passes through the intersection, the traffic lights revert to their normal sequential mode.
   对应摘录：A
