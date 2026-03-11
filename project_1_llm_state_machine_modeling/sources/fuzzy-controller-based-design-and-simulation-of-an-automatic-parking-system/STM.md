# Fuzzy Controller-Based Design and Simulation of an Automatic Parking System - STM 提取记录

## 盘点结论
- 评级：🟡 可整理
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文给出了典型的“位置/方向检测 - 模糊推理 - 转角输出 - 再检测”的闭环泊车控制链，但显式离散状态名不强。

## 条目 1: Iterative Parking Steering Control
- 控制对象：智慧停车领域的自动泊车控制器

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

### 2. 基于原文整理后的自然语言描述

The automatic parking controller takes vehicle position and vehicle direction angle as its main inputs and produces wheel steering angle as the control output. It analyzes the parking lot model and repeatedly sends the inferred steering command to the vehicle motion model so that the vehicle follows a target trajectory. After each operation, the sensor detects position and direction again, and the procedure continues until the detected state matches the parking goal.

### 3. 逐句溯源

1. 句子 1：The automatic parking controller takes vehicle position and vehicle direction angle as its main inputs and produces wheel steering angle as the control output.
   对应摘录：A
2. 句子 2：It analyzes the parking lot model and repeatedly sends the inferred steering command to the vehicle motion model so that the vehicle follows a target trajectory.
   对应摘录：A
3. 句子 3：After each operation, the sensor detects position and direction again, and the procedure continues until the detected state matches the parking goal.
   对应摘录：B
