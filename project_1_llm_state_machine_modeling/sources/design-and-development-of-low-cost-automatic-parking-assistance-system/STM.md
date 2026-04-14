# Design and Development of Low Cost Automatic Parking Assistance System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：层次、连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把 APAS 拆成探索和泊车两阶段，并明确写出传感、条件检查、执行器与路径切换点的控制角色。

## 条目 1: Two-Phase Parking Assistance Control
- 控制对象：智慧停车领域的自动泊车辅助控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：层次、连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个低成本自动泊车辅助系统，用于先探索空车位并确认尺寸，再按照规划轨迹控制车辆完成泊车。
- 判断：算。对象是实际泊车控制器，原文明确给出了阶段划分、输入、条件检查和执行控制职责。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Introduction, 行 55-63
> In APAS the parking slot availability is explored by the system and then the parking is done on its own, thus minimizing driver involvement. APAS operates in two phases namely exploration and parking. In exploration phase, the system evaluates the length and width of parking slot for parking and confirms. In the parking phase the system guides the vehicle to along a suitable trajectory and park in the identified slot without collision.

#### 摘录 B
- 出处：第 1-4 页，Abstract / Functional block description / Flow diagram，行 14-20, 101-104, 180-218
> stepper motor mounted ultrasonic sensor to scan the obstacles. 3-point unequal rotating radius algorithm is used to identify parking path shifting points and parking trajectory. Path shifting control algorithm based on timing and distance traversed is developed using MPLAB IDE. ... APAS has sub-functions like gathering the driver inputs from switches, reading the sensor data, checking the necessary conditions, actuating the motors etc. ... Once the parking path is designed for that specific vehicle, parking path shifting points are identified. This helps the controller to take decision while parking the vehicle. ... Overall travelled distance ... Time taken ... detailed breakup is shown in Table 3. Control logic is developed based on the parking pattern and algorithm chosen. Parking path shifting points found from the graph are coded to control the parking process.

### 2. 基于原文整理后的自然语言描述

The automatic parking assistance system is organized into two top-level phases: exploration and parking. During exploration, a stepper-motor-mounted ultrasonic sensor scans the candidate slot, the controller evaluates the slot length and width, makes the parking-slot fitment decision, and computes the three-point unequal-rotating-radius trajectory together with the parking-path shifting points. During the parking phase, driver-input switches, sensor data, condition checking, and motor actuation are coordinated so that the vehicle follows the designed path from the identified shifting points into the selected slot without collision. The implemented control logic encodes these shifting points together with the associated travelled distances and timing values so that the prototype can execute the parking maneuver and later be corrected in closed loop when steering or path errors appear.

### 3. 逐句溯源

1. 句子 1：The automatic parking assistance system is organized into two top-level phases: exploration and parking.
   对应摘录：A
2. 句子 2：During exploration, a stepper-motor-mounted ultrasonic sensor scans the candidate slot, the controller evaluates the slot length and width, makes the parking-slot fitment decision, and computes the three-point unequal-rotating-radius trajectory together with the parking-path shifting points.
   对应摘录：A, B
3. 句子 3：During the parking phase, driver-input switches, sensor data, condition checking, and motor actuation are coordinated so that the vehicle follows the designed path from the identified shifting points into the selected slot without collision.
   对应摘录：A, B
4. 句子 4：The implemented control logic encodes these shifting points together with the associated travelled distances and timing values so that the prototype can execute the parking maneuver and later be corrected in closed loop when steering or path errors appear.
   对应摘录：B
