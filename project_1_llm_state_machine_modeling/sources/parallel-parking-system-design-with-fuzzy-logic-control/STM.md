# Parallel Parking System Design with Fuzzy Logic Control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：倒车轨迹分段逻辑已可进主样本，轨迹跟踪与模糊转向修正也已不再停留在摘要级。

## 条目 1: Reverse parking stroke with maximum-steer then straightening
- 控制对象：自动泊车系统中的倒车入位轨迹执行逻辑
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 C
- 出处：第 4-5 页，`Parking Trajectory Design`，行 219-230
> Radius is an important variable in designing a parking trajectory.
> Therefore, before designing the trajectory, it is necessary to first
> test the minimum radius of the test car. By using equation (1)
> where θ comes from the reading of the GY -25 heading sensor.
> The method of testing the turning radius is to run the car in reverse
> and the steering angle is 45 °. The turning radius is the largest
> coordinate value for the x -axis. The prototype test car received a
> maximum x value of 44.2 cm. Based on the data above, the
> turning radius that will be used in the parking trajectory design is
> 44.2 cm.  After the car follows the quarter -circle trajectory, the car moves
> backward following the straight -line trajectory.

### 2. 基于原文整理后的自然语言描述

The automatic parking system uses a designed reference trajectory so that the car can enter the parking space in the correct direction. For garage parking, the vehicle first reverses with the steering turned to the maximum angle so that it follows a circular path, and on the prototype this phase uses a constant steering angle of 45° and a reverse speed of 0.13 m/s. The turning radius used in the trajectory design is 44.2 cm. After the car follows the quarter-circle segment, the steering returns to 0 and the car continues reversing along a short straight-line segment to the parking end point.

### 3. 逐句溯源

1. 句子 1：The automatic parking system uses a reference parking trajectory so that the car enters the parking space in the correct direction.
   对应摘录：A
2. 句子 2：For garage parking, the vehicle first reverses with the steering turned to the maximum angle so that it follows a circular path, and on the prototype this phase uses a constant steering angle of 45° and a reverse speed of 0.13 m/s.
   对应摘录：A, B
3. 句子 3：The turning radius used in the trajectory design is 44.2 cm.
   对应摘录：C
4. 句子 4：After the car follows the quarter-circle segment, the steering returns to 0 and the car continues reversing along a short straight-line segment to the parking end point.
   对应摘录：A, B, C

## 条目 2: Fuzzy steering correction during parking
- 控制对象：自动泊车系统中的轨迹跟踪与转向修正控制
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟠 C（只有主链）
- 描述细节充实度：🟠 C（只有主链）
- 数据集角色：🧰 清洗后保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 B
- 出处：第 5-6 页，fuzzy controller design，对 input memberships / output steering angle 的说明，行 267-272, 327-331
> Based on the system block diagram in Figure 4, fuzzy logic
> control uses 1 input and 1 output. The input is the difference
> between the facing direction read by the gyro sensor and the
> facing direction setpoint at that point. Facing error is processed to
> determine fuzzy logic (fuzzyfication). In this stu dy, the facing
> error uses 3 membership, namely Negative (N), Neutral (Z) and
> Positive (P).
> Due to the fuzzy logic control Sugeno method
> the output is in the form of numeric values. Inference engi ne and
> defuzzyfication are combined. The result of this system is the
> steering angle. The steering system uses a servo motor with a
> 180° range of motion.

#### 摘录 C
- 出处：第 6-7 页，testing results，对 fuzzy correction effect 的说明，行 436-452
> In phase 2 testing the car will park towards the end point
> following the designed trajectory. The difference in the direction
> that is read by the GY25 sensor with the facing direction should
> be pro cessed with fuzzy logic control to get the steering angle.
> From the parking trajectory graph in Figure 10, it can be
> concluded that the parking system can follow the trajectory that
> has been des igned. The use of fuzzy logic control to control the
> direction of the car is able to reduce the error value facing the
> direction and position at the end point significantly. From table 4
> the average error value for the position is x = 1.25 cm, y = 0.59
> cm and the direction error is 1.59 °.

### 2. 基于原文整理后的自然语言描述

To drive the car to the parking destination, the controller uses sensor input to estimate the car coordinates and compares the current vehicle position with the designed parking trajectory. Its single control input is the difference between the facing direction read by the gyro sensor and the trajectory-facing direction at the current point. This facing error is fuzzified into three memberships, Negative, Neutral, and Positive, processed by a Sugeno fuzzy controller, and defuzzified into the steering-angle command for the servo motor. In the reported phase-2 test, this fuzzy steering correction reduced the average final errors to `x = 1.25 cm`, `y = 0.59 cm`, and `1.59°` in facing direction.

### 3. 逐句溯源

1. 句子 1：To drive the car to the parking destination, the controller uses sensor input to estimate the car coordinates and compares the current vehicle position with the designed parking trajectory.
   对应摘录：A
2. 句子 2：Its single control input is the difference between the facing direction read by the gyro sensor and the trajectory-facing direction at the current point.
   对应摘录：A, B
3. 句子 3：This facing error is fuzzified into three memberships, Negative, Neutral, and Positive, processed by a Sugeno fuzzy controller, and defuzzified into the steering-angle command for the servo motor.
   对应摘录：B
4. 句子 4：In the reported phase-2 test, this fuzzy steering correction reduced the average final errors to `x = 1.25 cm`, `y = 0.59 cm`, and `1.59°` in facing direction.
   对应摘录：C
