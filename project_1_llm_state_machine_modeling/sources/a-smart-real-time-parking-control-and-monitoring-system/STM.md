# A Smart Real-Time Parking Control and Monitoring System - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：停车位分配、预约和到位核验逻辑较清楚，但更偏管理控制层而非底层执行控制。

## 条目 1: Parking slot allocation and slot verification workflow
- 控制对象：智能停车场的车位分配与核验控制子系统

### 0. 条目识别与判定

- 一句话说明：这是智能停车管理领域的 parking slot allocation and verification subsystem，用于为员工和访客分配停车位、处理预约，并在车辆到位时核验是否停入正确车位。
- 判断：算，但属于停车控制系统的管理控制层样本。对象是真实停车控制系统的一个离散控制子系统，原文给出了分配、预约、到位核验和违停识别等明确处理链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 1，对 smart real-time parking slot management system 的描述，行 95-101
> This paper discusses the design and development of a smart real-time parking slot
> management system, where the parking slots for an organization’s employees and visitors
> are deﬁned by an intelligent mobile application. Allocating parking spaces for employees is
> carried out dynamically, as parking spaces for employees are determined according to work
> shifts where the staff receives their parking slots through the application. On the other
> hand, visitors need to request an appointment to be allocated a parking slot. When the car
> arrives at its predeﬁned parking slot, the parking slot’s camera captures a picture of a car

#### 摘录 B
- 出处：第 4 页，Section 1，对 optimal solution/control mechanism 的要求总结，行 196-199
> The optimal solution should provide (1) dynamic parking slot distribution, (2) a
> mechanism for pre-booking a parking slot, and (3) a mechanism to ensure that the car
> is parked in the correct slot. (4) inquire about the location of any car at any time. The
> ﬁrst two represent control of the parking system, while the third, and fourth pertain to

### 2. 基于原文整理后的自然语言描述

The parking management system dynamically distributes parking slots, provides a mechanism for pre-booking a specific slot, and ensures that a car is parked in the correct slot. Employee parking spaces are assigned according to work shifts, while visitors request an appointment in order to be allocated a parking slot. When a car arrives at its predefined slot, the slot camera captures the plate and the system checks whether the vehicle is parked in the correct place.

### 3. 逐句溯源

1. 句子 1：The parking management system dynamically distributes parking slots, provides a mechanism for pre-booking a specific slot, and ensures that a car is parked in the correct slot.
   对应摘录：A, B
2. 句子 2：Employee parking spaces are assigned according to work shifts, while visitors request an appointment in order to be allocated a parking slot.
   对应摘录：A
3. 句子 3：When a car arrives at its predefined slot, the slot camera captures the plate and the system checks whether the vehicle is parked in the correct place.
   对应摘录：A, B
