# Development of an Automated Railway Level Crossing Gate Control System using PLC - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出了铁路道口门控系统的到达/离开侧传感布置与障碍物检测职责，但门控状态迁移主要以系统级说明呈现，仍需轻度整理。

## 条目 1: Sensor-Based Railway Crossing Gate Control
- 控制对象：铁路道口平交口的 PLC 门控系统

### 0. 条目识别与判定
- 一句话说明：这是轨道交通领域的铁路道口门控控制器，用于在列车接近和离开道口时驱动栏杆开闭，并在道口存在障碍物时维持安全防护。
- 判断：算。对象是实际铁路平交口控制系统，原文给出了列车到达/离开检测、障碍物检测和门控自动化目标。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，行 18-25
> The existing conventional railway crossing gate control system in Bangladesh is being operated manually which causes increasing amount of accidents at the crossings due to the carelessness in manual operation. Also, manual mechanism is time consuming. The gate controlling mechanism should be carried out ensuring safety to the road users and guarantying less time during gate opening and closing process. In this work, a prototype road and rail line model with automated railway level crossing gate controlling mechanism has been designed and implemented. At the train’s level crossing arrival and departure side, a set of photoelectric sensors are strategically placed. Also for detecting any obstacles, reflective type photoelectric sensors are used strategically.

#### 摘录 B
- 出处：第 2 页，Introduction，行 110-116
> This work designs and develops an automated railway level crossing gate control system using Reflective type photo electric sensor and programmable logic control that avoids the time-consuming process of level crossing gate opening and closing mechanism and ensures safety to the road users reducing accidents. The principle is to develop a feasible, low-cost prototype level crossing gate controlling and obstacle detection system for application in Bangladesh.

### 2. 基于原文整理后的自然语言描述

The automated railway level-crossing controller replaces manual gate operation with a PLC-based mechanism in order to reduce unsafe and time-consuming gate handling. Photoelectric sensors are placed at the arrival and departure sides of the crossing to detect train movement, and reflective photoelectric sensors are used to detect obstacles at the crossing. The controller is intended to automate gate opening and closing while preserving road-user safety and reducing crossing accidents.

### 3. 逐句溯源

1. 句子 1：The automated railway level-crossing controller replaces manual gate operation with a PLC-based mechanism in order to reduce unsafe and time-consuming gate handling.
   对应摘录：A, B
2. 句子 2：Photoelectric sensors are placed at the arrival and departure sides of the crossing to detect train movement, and reflective photoelectric sensors are used to detect obstacles at the crossing.
   对应摘录：A
3. 句子 3：The controller is intended to automate gate opening and closing while preserving road-user safety and reducing crossing accidents.
   对应摘录：A, B
