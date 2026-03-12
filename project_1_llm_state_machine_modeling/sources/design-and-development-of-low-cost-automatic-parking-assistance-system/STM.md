# Design and Development of Low Cost Automatic Parking Assistance System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把 APAS 拆成探索和泊车两阶段，并明确写出传感、条件检查、执行器与路径切换点的控制角色。

## 条目 1: Two-Phase Parking Assistance Control
- 控制对象：智慧停车领域的自动泊车辅助控制器

### 0. 条目识别与判定
- 一句话说明：这是一个低成本自动泊车辅助系统，用于先探索空车位并确认尺寸，再按照规划轨迹控制车辆完成泊车。
- 判断：算。对象是实际泊车控制器，原文明确给出了阶段划分、输入、条件检查和执行控制职责。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction, 行 55-63
> In APAS the parking slot availability is explored by the system and then the parking is done on its own, thus minimizing driver involvement. APAS operates in two phases namely exploration and parking. In exploration phase, the system evaluates the length and width of parking slot for parking and confirms. In the parking phase the system guides the vehicle to along a suitable trajectory and park in the identified slot without collision.

#### 摘录 B
- 出处：第 2 页，functional block description, 行 101-104, 121-134
> APAS has sub-functions like gathering the driver inputs from switches, reading the sensor data, checking the necessary conditions, actuating the motors etc. ... Sensor blocks collect the sensor data ... This makes the system to work as closed loop and to add correction factors if there is an error inside the system. ... Once the parking path is designed for that specific vehicle, parking path shifting points are identified. This helps the controller to take decision while parking the vehicle.

### 2. 基于原文整理后的自然语言描述

The automatic parking assistance system first explores whether a parking slot is available and then performs the parking maneuver on its own. During the exploration phase, the controller evaluates the slot length and width and confirms whether parking is possible. During the parking phase, the controller uses driver-input switches, sensor data, condition checking, motor actuation, and parking-path shifting points to guide the vehicle along a suitable trajectory into the identified slot without collision.

### 3. 逐句溯源

1. 句子 1：The automatic parking assistance system first explores whether a parking slot is available and then performs the parking maneuver on its own.
   对应摘录：A
2. 句子 2：During the exploration phase, the controller evaluates the slot length and width and confirms whether parking is possible.
   对应摘录：A
3. 句子 3：During the parking phase, the controller uses driver-input switches, sensor data, condition checking, motor actuation, and parking-path shifting points to guide the vehicle along a suitable trajectory into the identified slot without collision.
   对应摘录：A, B
