# Parallel Parking System Design with Fuzzy Logic Control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：论文同时给出了自动泊车中的倒车轨迹分段逻辑和基于轨迹偏差的转向控制闭环，能提取出两类子控制逻辑。

## 条目 1: Reverse parking stroke with maximum-steer then straightening
- 控制对象：自动泊车系统中的倒车入位轨迹执行逻辑

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与自动泊车领域的轨迹执行子过程，用于按预设泊车轨迹控制车辆先大角度倒车，再回正转向进入车位。
- 判断：算。对象是实际自动泊车系统中的倒车控制子过程，具有明确的阶段推进和阶段切换。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，`Parking Trajectory Design`，行 182-193
> Designing a parking trajectory based on the empty parking spaces
> detected by the prototype is an important ste p in designing an
> automatic parking lot. The parking trajectory is used as a
> reference for an automatic parking system so that the car can park
> in the right direction.
> For garage parking, the steering is turned to the maximum angle
> then the vehicle backs up will create a circular motion trajectory
> when parking. [9] Then the vehicle continues to reverse with
> normal steering until the minimum distance the door can be
> opened. The entire transverse reverse parking stroke forms a
> quarter circle trajectory and a  short straight line at the end of the
> quarter circle

#### 摘录 B
- 出处：第 6 页，`Testing The Parking System without Fuzzy Logic Control`，行 381-385
> In phase 1 the car will park with a constant steering angle (45 °)
> and a reverse speed of 0.13m / s. when the turning process is
> compl ete the steering will return to angle 0 constantly. The car
> goes to the parking space on the orders of the operator.

### 2. 基于原文整理后的自然语言描述

The automatic parking system uses a reference parking trajectory so that the car enters the parking space in the correct direction. During the reverse parking stroke, the steering is first turned to the maximum angle so that the car follows a circular trajectory, and after the turning process is complete the steering returns to zero while the car continues reversing along a short straight segment into the parking space.

### 3. 逐句溯源

1. 句子 1：The automatic parking system uses a reference parking trajectory so that the car enters the parking space in the correct direction.
   对应摘录：A
2. 句子 2：During the reverse parking stroke, the steering is first turned to the maximum angle so that the car follows a circular trajectory, and after the turning process is complete the steering returns to zero while the car continues reversing along a short straight segment into the parking space.
   对应摘录：A, B

## 条目 2: Fuzzy steering correction during parking
- 控制对象：自动泊车系统中的轨迹跟踪与转向修正控制

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与自动泊车领域的转向闭环控制器，用于比较当前朝向与目标轨迹朝向，并输出需要执行的转向角。
- 判断：算。对象是自动泊车控制器的核心执行环节，输入、处理和输出都很清楚。

### 1. 原文摘录

#### 摘录 A
- 出处：第 5 页，控制框图描述，行 247-256
> In order for the test car to go to the parking destination point
> according to the trajectory design, the motor and car steering
> wheel are controlled based on the data sent from the system input.
> the data from the sensor is processed by microcontroller to g et the
> coordinates of the car. The car coordinates are obtained from the
> car coordinates compared with the parking trajectory design. The
> difference between the current facing direction and the direction
> facing the trajectory is processed using Sugeno's fu zzy logic
> control to get the value of the steering angle that must be
> executed.

### 2. 基于原文整理后的自然语言描述

To drive the car to the parking destination, the controller uses sensor input to estimate the car coordinates and compares the current vehicle position with the designed parking trajectory. The difference between the current facing direction and the trajectory-facing direction is then processed by Sugeno fuzzy logic control to compute the steering angle that must be executed.

### 3. 逐句溯源

1. 句子 1：To drive the car to the parking destination, the controller uses sensor input to estimate the car coordinates and compares the current vehicle position with the designed parking trajectory.
   对应摘录：A
2. 句子 2：The difference between the current facing direction and the trajectory-facing direction is then processed by Sugeno fuzzy logic control to compute the steering angle that must be executed.
   对应摘录：A
