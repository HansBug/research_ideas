# Fuzzy Controller-Based Design and Simulation of an Automatic Parking System - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 文件级角色：💎 含核心样本
- 代表状态机类型：Hybrid（混成状态机）
- 代表时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了“位置/方向检测 - 模糊推理 - 转角输出 - 再检测”的闭环，还补出了连续迭代方程、输入输出隶属集规模和停止条件，已能支撑较完整的混成控制样本。

## 条目 1: Iterative Parking Steering Control
- 控制对象：智慧停车领域的自动泊车控制器
- 状态机类型：Hybrid（混成状态机）
- 时间级别：T3（混成时间 / 连续时间耦合）
- 结构标签：连续耦合
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个自动泊车控制器，用于根据车辆位置和方向角持续计算转向角，并反复修正轨迹直到达到目标停车位。
- 判断：算，但属于控制闭环级样本。对象是实际自动泊车控制器，不过控制逻辑更多体现为迭代决策而非显式状态名。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Methodology, 行 124-139
> In our proposed system, while the vehicle speed is kept constant, the emphasis is on analyzing variations in the wheel steering angle. By examining the vehicle’s trajectory, we identify two primary input variables: the vehicle position and the vehicle direction angle. The wheel steering angle serves as the primary output variable in controlling the vehicle trajectory. These inputs and outputs are synergized through a fuzzy controller, forming the foundational rule base of the Fuzzy Inference System (FIS). ... Firstly, the vehicle motion is analyzed and modeled, the input and output variables are determined, the vehicle motion equations are analyzed, and the relationship between them is found. Then, the parking lot model is constructed ... Finally, ... the value obtained by the fuzzy inference system is sent to the vehicle motion model to run according to a certain trajectory, and the vehicle position and parking space position are continuously judged until the end of the program.

#### 摘录 B
- 出处：第 7 页，Fuzzy control loop, 行 258-266
> When the vehicle position and direction angle are detected by the sensor, its value is crisp input. The fuzzy system needs to fuzzification the crisp input ... obtain the crisp output according to the output membership function and defuzzification method. Finally, transfer the crisp output value—wheel steering angle to the equipment for operation. After the operation, the vehicle sensor will detect the vehicle position and direction angle again, and compare it with the target. If it is consistent with the goal, the procedure will be ended; If not, continue ...

#### 摘录 C
- 出处：第 6-8 页，`3.3 Vehicle Dynamic Model / 3.5 Fuzzy System Structure Design / 3.6 Membership Function`，行 220-305
> In this scheme design, the vehicle speed is set as a constant value s and the
> wheel steering angle is set β while it will be controlled as the output of the fuzzy
> controller. ... this is an iterative process.
> ...
> the vehicle direction angle α and the steering angle β will be determined by the vehicle continuous iterative updating; the location of the vehicle will also vary according to α and β.
> ...
> x (the horizon position of the vehicle) and α (the angle of the vehicle contract with the parking area) as the input of the fuzzy controller, β (the angle of the steering wheel) as the output of the fuzzy controller.
> Variable x has 5 fuzzy sets, variable α has 7 fuzzy sets, variable β has 7 fuzzy sets.

### 2. 基于原文整理后的自然语言描述

The automatic parking controller keeps the vehicle speed as a constant value `s`, uses vehicle position `x` and direction angle `α` as its fuzzy inputs, and generates wheel steering angle `β` as the control output. The controller updates the pose iteratively through the vehicle motion equations, so each new steering command changes the position and direction of the vehicle along the planned parking path. In the fuzzy layer, the controller uses 5 fuzzy sets for `x`, 7 fuzzy sets for `α`, and 7 fuzzy sets for `β`, then applies fuzzification, rule-based inference, and defuzzification to obtain the next steering command. After every actuation, the sensors detect position and direction again and compare them with the target; if the goal has been reached the process ends, otherwise the fuzzy cycle continues.

### 3. 逐句溯源

1. 句子 1：The automatic parking controller keeps the vehicle speed as a constant value `s`, uses vehicle position `x` and direction angle `α` as its fuzzy inputs, and generates wheel steering angle `β` as the control output.
   对应摘录：A, C
2. 句子 2：The controller updates the pose iteratively through the vehicle motion equations, so each new steering command changes the position and direction of the vehicle along the planned parking path.
   对应摘录：A, C
3. 句子 3：In the fuzzy layer, the controller uses 5 fuzzy sets for `x`, 7 fuzzy sets for `α`, and 7 fuzzy sets for `β`, then applies fuzzification, rule-based inference, and defuzzification to obtain the next steering command.
   对应摘录：B, C
4. 句子 4：After every actuation, the sensors detect position and direction again and compare them with the target; if the goal has been reached the process ends, otherwise the fuzzy cycle continues.
   对应摘录：B
