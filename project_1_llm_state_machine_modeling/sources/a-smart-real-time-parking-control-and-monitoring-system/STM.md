# A Smart Real-Time Parking Control and Monitoring System - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：Resource-flow（资源流/并发网模型）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：资源互斥
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：动态分配、预约、到位检测、图像校验、云端核位与错位告警链已经较完整，属于非趋同资源流样本。

## 条目 1: Parking slot allocation and slot verification workflow
- 控制对象：智能停车场的车位分配与核验控制子系统
- 状态机类型：Resource-flow（资源流/并发网模型）
- 时间级别：T0（无关键时间语义）
- 结构标签：资源互斥
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 C
- 出处：第 6-7 页，System workflow，对 monitoring / processing / cloud-side verification 的说明，行 329-343
> The developed smart real-time parking control and monitoring system works as
> follows: when a car parks in a parking slot, the monitoring unit detects its presence using
> either the range-ﬁnder sensor or the motion sensor. The monitoring unit then captures an
> image of the parked vehicle and transmits it directly to the processing unit. The processing
> unit checks the quality of the image and requests a replacement if the received image is
> of poor quality. Then, it detects the car’s plate number and sends this information associated
> with the parking slot number, time, and date to the cloud-side unit. The cloud-side unit
> veriﬁes if the car is in the right parking slot and sends a notiﬁcation to check the driver’s record to ensure that they have parked in the correct
> slot. If the driver has parked in the wrong slot, a notiﬁcation message will be sent to both
> the driver’s mobile application account and the administrator. On the other hand, when a
> visitor requests a parking slot, the mobile application sends a request to the Firebase cloud
> server, which approves the request.

#### 摘录 D
- 出处：第 9 页，Reservation scenarios，对 employee / visitor allocation flow 的说明，行 525-541
> In the ﬁrst scenario, the system distributes slot information to employees according to
> their ofﬁcial work hours or shift hours, using a priority queue data structure. Then, the
> employee parks in the assigned slot. The system checks if the employee has occupied the
> correct slot; if not, an alert will be sent to both the employee and the administrator.
> The second scenario is related to the visitor actor. First, the visitor requests a parking
> slot. Then, the system checks the availability and sends the slot information to the visitor.

### 2. 基于原文整理后的自然语言描述

The parking management system provides dynamic parking-slot distribution, a pre-booking mechanism for a specific slot and time, verification that a car is parked in its correct slot, and the ability to inquire about the location of a car. For employees, slot information is distributed according to official work hours or shift hours, while visitors request a slot and the system checks availability before sending the allocation back to the visitor. When a car parks in a slot, the monitoring unit detects its presence with either a motion sensor or a range-finder sensor, captures a vehicle image, and sends it to the processing unit, which checks image quality, requests a replacement if needed, detects the license-plate number, and records the slot number, time, and date in the cloud-side unit. The cloud side verifies whether the car occupies the assigned slot, and if the driver has parked in the wrong slot the system sends an alert to both the driver and the administrator.

### 3. 逐句溯源

1. 句子 1：The parking management system provides dynamic parking-slot distribution, a pre-booking mechanism for a specific slot and time, verification that a car is parked in its correct slot, and the ability to inquire about the location of a car.
   对应摘录：A, B
2. 句子 2：For employees, slot information is distributed according to official work hours or shift hours, while visitors request a slot and the system checks availability before sending the allocation back to the visitor.
   对应摘录：A, D
3. 句子 3：When a car parks in a slot, the monitoring unit detects its presence with either a motion sensor or a range-finder sensor, captures a vehicle image, and sends it to the processing unit, which checks image quality, requests a replacement if needed, detects the license-plate number, and records the slot number, time, and date in the cloud-side unit.
   对应摘录：C
4. 句子 4：The cloud side verifies whether the car occupies the assigned slot, and if the driver has parked in the wrong slot the system sends an alert to both the driver and the administrator.
   对应摘录：C, D
