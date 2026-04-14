# An Intelligent Auto Parking System for Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文对自动泊车系统从感知、可停判定、轨迹参数选择到路径跟踪与 steering motor 执行的控制链路写得较完整，两个条目都已可保住主要建模关键件。

## 条目 1: Parking assistant control pipeline
- 控制对象：自动泊车辅助系统中的感知、判定、轨迹生成与执行控制链路
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 B
- 出处：第 1-2 页，`1. Introduction`，行 34-45, 77-88
> The automatic parking aims to enhance the comfort and safety of driving in constrained environments where much attention
> and experience is required to steer the car. The parking
> maneuver is achieved by means of coordinated control of the steering angle and speed which takes into account the actual
> situation in the environment to ensure collision-free motion
> within the available space.
> In the proposed system geometric constaints
> are directly considered to design a collision-free trajectory,
> therefore system does not need to recursively detect collisions
> while parking. Also usage human-like intelligent fuzzy logic -
> based algorithm allows choosing trajectory that is the optimal
> for current environment conditions

#### 摘录 C
- 出处：第 4-5 页，`3.2. Design of Fuzzy Logic System`，行 323-348
> As it was mentioned above, the first input of the fuzzy
> system is the velocity of the vehicle.
> The second input of fuzzy system is chosen to be the
> distance to the top obstacle (DT).
> The third input in the system is the starting point Lp
> (coordinate x of initial point for vehicle).
> The output of the fuzzy system is the radius R1
> ...
> The output of Fuzzy Logic Controller is the set of radiuses
> (R1, R2), which give us desired trajectory for parking.

### 2. 基于原文整理后的自然语言描述

The parking assistant system first uses sensors to measure obstacle distances, current vehicle velocity, and detect a parking space so the actual parking environment can be evaluated. After receiving the data, the system builds a map, estimates the current relative vehicle position, and checks whether parking is possible under the geometric constraints of the current slot. If parking is possible, the vehicle stops and the control block generates a collision-free parking trajectory together with the desired steering law, where the fuzzy-logic trajectory module takes vehicle velocity, top-obstacle distance `DT`, and starting point `Lp` as inputs and produces the trajectory radii `(R1, R2)`. A path-tracking controller then uses steering-angle and wheel-speed feedback with the vehicle dynamic model to estimate the vehicle position at each time sample and drives the steering motor according to the angle, speed, and time parameters of the steering law, while the graphical interface continues to cooperate with the driver.

### 3. 逐句溯源

1. 句子 1：The parking assistant system first uses sensors to measure obstacle distances, current vehicle velocity, and detect a parking space so the actual parking environment can be evaluated.
   对应摘录：A, B
2. 句子 2：After receiving the data, the system builds a map, estimates the current relative vehicle position, and checks whether parking is possible under the geometric constraints of the current slot.
   对应摘录：A, B
3. 句子 3：If parking is possible, the vehicle stops and the control block generates a collision-free parking trajectory together with the desired steering law, where the fuzzy-logic trajectory module takes vehicle velocity, top-obstacle distance `DT`, and starting point `Lp` as inputs and produces the trajectory radii `(R1, R2)`.
   对应摘录：A, B, C
4. 句子 4：A path-tracking controller then uses steering-angle and wheel-speed feedback with the vehicle dynamic model to estimate the vehicle position at each time sample and drives the steering motor according to the angle, speed, and time parameters of the steering law, while the graphical interface continues to cooperate with the driver.
   对应摘录：A

## 条目 2: Feasibility check and trajectory-selection sequence
- 控制对象：自动泊车系统中的可停判定与轨迹参数选择逻辑
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

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

#### 摘录 B
- 出处：第 5 页，`3.2. Design of Fuzzy Logic System`，行 309-347
> if velocity is low it means that we can follow the trajectory
> with relatively big curvature and we can choose smaller radius
> for trajectory; comparatively high velocity means that
> following the trajectory with relatively big curvature will be poor and it’s better to choose bigger radius for trajectory.
> The second input of fuzzy system is chosen to be the
> distance to the top obstacle (DT). If the distance to the top
> obstacle is small (DT = small), we need to choose big radius R1
> of the trajectory in order to avoid collision with top obstacle
> The third input in the system is the starting point Lp.
> If the starting point Lp is close, we need to choose small radius R1
> ...
> in case when the starting point Lp is far, we need to choose big radius R1

#### 摘录 C
- 出处：第 5 页，`3.2. Design of Fuzzy Logic System`，行 347-372
> instead of absolute value of starting point Lp,
> relative difference for Lp (0-100) % of ∆Lpmax was chosen as
> the third input of controller.
> The output of the fuzzy system is the radius R1, but since
> range for R1 defined as a constant values and
> minimum/maximum values for R1 change depending on the
> information about parking environment, fuzzy logic system
> may choose incorrect values for R1 which are not satisfied non-
> collision conditions, that’s why relative difference of R1 an
> R1max is used as output of fuzzy system.
> The method of defuzzification is centroid.
> The output of Fuzzy Logic Controller is the set of radiuses
> (R1, R2), which give us desired trajectory for parking.

#### 摘录 D
- 出处：第 5 页，`3.2. Design of Fuzzy Logic System`，行 373-381
> Table 1. Fuzzy rules for case when DT is “ big”
> Velocity delLp Low High
> Close Small Medium
> Average Medium Big
> Far Big Big
> Table 2. Fuzzy rules for case when DT is “ small”
> Velocity delLp Low High
> Close Medium Big
> Average Medium Big
> Far Big Big

### 2. 基于原文整理后的自然语言描述

The trajectory-generation controller gathers ultrasonic sensor data, computes the parking-lot dimensions `(L, DB, DT)`, builds the map, and calculates feasible sets of turning radii `(R1, R2)` together with their minimum/maximum bounds and the admissible starting-point margins `(Lpmin, Lpmax)`. Parking is accepted only when the computed radius bounds satisfy `Rimax > Rimin` and the current starting point is also feasible. If parking is impossible because the current starting point is wrong, the system commands the car to move backward or forward according to the current position; if parking is impossible because the turning radii are unacceptable, it searches for a new parking slot. When parking is feasible, the controller chooses `R1` with a Mamdani fuzzy system using vehicle velocity `V`, top-obstacle distance `DT`, and the relative starting-point difference `∆Lpr` as inputs, then computes `R2`, estimates the trajectory parameters `(s1, s2)`, and generates the steering-angle law. The fuzzy rules explicitly bias the choice toward larger radii when `DT` is small or velocity is high, while for `DT = big` and a close start point the controller can still choose `small` or `medium` radii depending on the velocity case.

### 3. 逐句溯源

1. 句子 1：The trajectory-generation controller gathers ultrasonic sensor data, computes the parking-lot dimensions `(L, DB, DT)`, builds the map, and calculates feasible sets of turning radii `(R1, R2)` together with their minimum/maximum bounds and the admissible starting-point margins `(Lpmin, Lpmax)`.
   对应摘录：A
2. 句子 2：Parking is accepted only when the computed radius bounds satisfy `Rimax > Rimin` and the current starting point is also feasible.
   对应摘录：A
3. 句子 3：If parking is impossible because the current starting point is wrong, the system commands the car to move backward or forward according to the current position; if parking is impossible because the turning radii are unacceptable, it searches for a new parking slot.
   对应摘录：A
4. 句子 4：When parking is feasible, the controller chooses `R1` with a Mamdani fuzzy system using vehicle velocity `V`, top-obstacle distance `DT`, and the relative starting-point difference `∆Lpr` as inputs, then computes `R2`, estimates the trajectory parameters `(s1, s2)`, and generates the steering-angle law.
   对应摘录：A, B, C
5. 句子 5：The fuzzy rules explicitly bias the choice toward larger radii when `DT` is small or velocity is high, while for `DT = big` and a close start point the controller can still choose `small` or `medium` radii depending on the velocity case.
   对应摘录：B, D
