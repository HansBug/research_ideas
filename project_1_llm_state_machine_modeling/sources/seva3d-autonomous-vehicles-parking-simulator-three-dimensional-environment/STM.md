# SEVA3D: Autonomous Vehicles Parking Simulator in a three-dimensional environment - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然以仿真平台为背景，但把并联泊车与 pull-out 控制器的状态、传感器布局、动作指令和实验结果都写得很完整。

## 条目 1: Parallel-parking search-enter-align supervisor
- 控制对象：智慧停车与自动泊车领域的并联泊车监督控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于五个声呐传感器的自动并联泊车控制器，用有限状态自动机驱动车辆完成搜位、外部定位、倒车入位、内部调整、对齐停车与出库。
- 判断：算。对象是明确的 autonomous parking controller，原文给出了控制器状态、传感器触发条件、速度/转向动作、pull-out 子自动机和实验结果。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，摘要与系统目标，行 14-20, 92-121
> The developed system can automatically drive a vehicle
> ... autonomous parking in a parallel parking space.
> The controller was implemented using a rule-based finite state automaton
> ...
> The control system implemented in SEVA3D accomplishes the parking of vehicles,
> controlling them in an autonomous way using a finite state automaton (FSA).

#### 摘录 B
- 出处：第 4-6 页，传感器与停车 FSA 说明，行 303-317, 399-451
> The simulated sonar sensors allow to estimate the distance between the vehicle and the obstacles
> ...
> the five sensors used were distributed in strategic positions of the vehicle
> ...
> In SEVA3D, the vehicle control in an autonomous parking task is accomplished by a Finite State Automaton (FSA).
> ...
> Stopped ... Searching for parking space ... Positioning outside ... Entering ... Positioning inside ... Aligning
> ...
> when the sensor V[2] detects the sidewalk curb the state changes to Positioning inside
> ...
> when the sensor V[3] detects the sidewalk curb or the sensor V[1] detects a close obstacle (distance under 30 cm)
> the state changes to Aligning

#### 摘录 C
- 出处：第 6-8 页，pull-out 与实验结果，行 438-451, 497-551
> The following states were defined:
> Preparing pull out ... Pull out ... Returning
> ...
> different simulations were accomplished with success
> ...
> In all these experiments, SEVA3D was capable to correctly park the vehicle,
> with an average distance from the curb of 26.16 cm and a standard deviation of 5.92 cm
> ...
> the proposed method is stable, safe and robust.

### 2. 基于原文整理后的自然语言描述

The SEVA3D parking controller uses five strategically placed sonar sensors to perceive nearby parked cars and the sidewalk curb, then issues acceleration and steering commands to a non-holonomic vehicle model through a rule-based finite state automaton. Its parking automaton starts from `Stopped`, enters `Searching for parking space`, moves to `Positioning outside` once a candidate space is found, then executes `Entering`, `Positioning inside`, and `Aligning` until the car is properly parked and returns to `Stopped`. State transitions are triggered by concrete sensor events, such as detecting the curb with `V[2]` or `V[3]`, or detecting a close obstacle with `V[1]` when the rear distance falls below `30 cm`. The same controller family also includes a pull-out automaton with `Preparing pull out`, `Pull out`, and `Returning`, and simulation experiments report successful parking across varied initial positions and scenarios, with an average curb distance of about `26.16 cm`.

### 3. 逐句溯源

1. 句子 1：The SEVA3D parking controller uses five strategically placed sonar sensors to perceive nearby parked cars and the sidewalk curb, then issues acceleration and steering commands to a non-holonomic vehicle model through a rule-based finite state automaton.
   对应摘录：A, B
2. 句子 2：Its parking automaton starts from `Stopped`, enters `Searching for parking space`, moves to `Positioning outside` once a candidate space is found, then executes `Entering`, `Positioning inside`, and `Aligning` until the car is properly parked and returns to `Stopped`.
   对应摘录：B
3. 句子 3：State transitions are triggered by concrete sensor events, such as detecting the curb with `V[2]` or `V[3]`, or detecting a close obstacle with `V[1]` when the rear distance falls below `30 cm`.
   对应摘录：B
4. 句子 4：The same controller family also includes a pull-out automaton with `Preparing pull out`, `Pull out`, and `Returning`, and simulation experiments report successful parking across varied initial positions and scenarios, with an average curb distance of about `26.16 cm`.
   对应摘录：C
