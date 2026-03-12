# An Intelligent Auto Parking System for Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文对自动泊车系统从环境感知到轨迹生成、路径跟踪、转向执行的控制链路写得很完整，也明确给出了“可停/不可停”和起始位置修正的决策流程。

## 条目 1: Parking assistant control pipeline
- 控制对象：自动泊车辅助系统中的感知、判定、轨迹生成与执行控制链路

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车载控制领域的自动泊车辅助系统，用于检测车位、判断可泊入性、生成转向轨迹并驱动转向电机执行泊车。
- 判断：算。对象是实际自动泊车系统，输入、阶段化处理和执行输出在原文中都给出了清晰描述。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，`1. Introduction`，行 53-72
> Basic parking assistant system (PAS) architecture is given in
> Fig 1. At first, the sensors are used for receiving information
> about the environment (Part I in Fig 1). It measures the distance
> to the obstacles, current car velocity and detects parking space.
> The next step after receiving data is map building and current
> relative vehicle position estimation (Part II, a). Based on map
> building the system checks the possibility of parking the car. If
> the parking is considered possible, the car should stop so that the
> control block can generate the parking trajectory using a
> particular algorithm. Trajectory generation algorithm generates
> desired trajectory and converts it to desired law for steering angle
> (Part II, b). Path tracking control part is using the desired
> law for steering angle generated on the previous step as an
> input to calculate desired position of the car at a given time
> sample. Data from steering angle sensor and wheel speed sensor
> is used for position estimation based on the dynamic model of
> the car.
> Next, the position of vehicle is changed by the means of
> changing steering angle, which is controlled by steering motor.
> Tracking controller manages the steering motor motion,
> depending on the angle, speed and time parameters of steering law.
> Part IV is responsible for graphic user interface, since every parking system is working together with driver.

### 2. 基于原文整理后的自然语言描述

The parking assistant system first uses sensors to measure obstacle distances, current vehicle velocity, and detect a parking space. After receiving the data, the system builds a map, estimates the current relative vehicle position, and checks whether parking is possible. If parking is possible, the vehicle stops and the control block generates a parking trajectory together with the desired steering law. A path-tracking controller then uses steering-angle and wheel-speed feedback to estimate the vehicle position and drives the steering motor according to the angle, speed, and time parameters of the steering law, while the graphical interface cooperates with the driver.

### 3. 逐句溯源

1. 句子 1：The parking assistant system first uses sensors to measure obstacle distances, current vehicle velocity, and detect a parking space.
   对应摘录：A
2. 句子 2：After receiving the data, the system builds a map, estimates the current relative vehicle position, and checks whether parking is possible.
   对应摘录：A
3. 句子 3：If parking is possible, the vehicle stops and the control block generates a parking trajectory together with the desired steering law.
   对应摘录：A
4. 句子 4：A path-tracking controller then uses steering-angle and wheel-speed feedback to estimate the vehicle position and drives the steering motor according to the angle, speed, and time parameters of the steering law, while the graphical interface cooperates with the driver.
   对应摘录：A

## 条目 2: Feasibility check and trajectory-selection sequence
- 控制对象：自动泊车系统中的可停判定与轨迹参数选择逻辑

### 0. 条目识别与判定

- 一句话说明：这是智慧停车与车载控制领域的轨迹生成控制器，用于根据传感器信息判断当前车位和起始位置是否可泊入，并在可行时生成两段圆弧轨迹参数与转向规律。
- 判断：算。对象是实际自动泊车控制流程，原文清楚描述了不可停分支、起始位置修正分支和可停后的参数计算链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，`3.1. Trajectory generation algorithm using Fuzzy Logic`，行 276-305
> The proposed trajectory generation system with fuzzy logic
> works as follows. At first, the information from the ultrasonic
> sensors is being gathered and fed to the host PC, where it is
> further processed in the next step of the algorithm. Based on the
> sensor information obtained at the previous step, the algorithm
> calculates parking lot sizes (L, DB, DT in Fig. 4) and builds the
> map. Next, the algorithm calculates the feasible solution sets of
> the turning radiuses R1, R2 and their corresponding minimum and
> maximum boundaries, along with the sets of starting points margins
> based on the environment parameters and parking lot sizes obtained earlier.
> The algorithm checks if the parking is possible or not; the
> parking is considered possible based on two conditions.
> If this inequality holds, the algorithm proceeds with
> verification of the feasibility of the current starting point, and the
> parking is considered possible if the latter is true. If the parking is
> considered impossible due to the wrong starting point, the
> algorithm generates the command to move the car backward or
> forward, depending on the current position. However, if the
> parking is considered impossible due to the unacceptability of the
> turning radiuses, we need to find a new parking slot. If the
> parking is considered possible, the algorithm selects the radius R1
> using fuzzy logic controller based on the following parameters:
> vehicle velocity (V), distance to the top obstacle (DT) and the
> starting point (Lp). After that, the algorithm calculates R2 using
> equation (3). Finally, the system estimates all parameters for
> trajectory (s1 and s2) and generates the law for steering angle.

### 2. 基于原文整理后的自然语言描述

The trajectory-generation controller gathers ultrasonic sensor data, computes the parking-lot dimensions, and builds the map of the current environment. It then calculates feasible sets of turning radii and starting-point margins and checks whether parking is possible. If parking is impossible because the current starting point is wrong, the system commands the car to move backward or forward according to the current position; if parking is impossible because the turning radii are unacceptable, the system searches for a new parking slot. When parking is considered possible, the controller selects radius R1 with a fuzzy logic controller based on vehicle velocity, distance to the top obstacle, and starting point, then calculates R2, estimates the trajectory parameters, and generates the steering-angle law.

### 3. 逐句溯源

1. 句子 1：The trajectory-generation controller gathers ultrasonic sensor data, computes the parking-lot dimensions, and builds the map of the current environment.
   对应摘录：A
2. 句子 2：It then calculates feasible sets of turning radii and starting-point margins and checks whether parking is possible.
   对应摘录：A
3. 句子 3：If parking is impossible because the current starting point is wrong, the system commands the car to move backward or forward according to the current position; if parking is impossible because the turning radii are unacceptable, the system searches for a new parking slot.
   对应摘录：A
4. 句子 4：When parking is considered possible, the controller selects radius R1 with a fuzzy logic controller based on vehicle velocity, distance to the top obstacle, and starting point, then calculates R2, estimates the trajectory parameters, and generates the steering-angle law.
   对应摘录：A
