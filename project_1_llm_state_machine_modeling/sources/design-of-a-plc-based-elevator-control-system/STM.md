# Design of a PLC Based Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚写出了无请求停层开门、自动开关门、上/下行指示和 hall/car call 优先处理等电梯控制需求。

## 条目 1: Idle-Open and Auto-Door Elevator Workflow
- 控制对象：楼宇机电领域的 PLC 电梯控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个楼宇电梯控制器，用于采集 car-call、hall-call 和楼层传感器输入，并输出方向灯、到层灯以及门开关控制。
- 判断：算。对象是实际电梯控制系统，原文明确给出一组面向功能实现的离散控制要求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section A-C, 行 108-143
> In PLC, the input signals are operational modes, safety control signals, car-calls, hall-calls, floor sensors, levelling sensors, door opening and close signals. All the functions of the elevator control systems are realized using the PLC programs, the functions includes registration, displaying the messages about the floors, monitoring the safety system, monitoring the door opening and closing, prioritizing the hall-call, and car-calls.
>
> This section presents the problems which are needed to solve through the ladder diagram. Ladder diagram is used to realize the many functionalities of the elevator control system. Some of the functionalities are, program should be written to make the display on which indicates the upward or downward movement, the door of the elevator should be programmed to open and close automatically, when the elevator has no request it remains at its current floor with its door opened, floor lamp should glow within the lift to indicate the current position.

### 2. 基于原文整理后的自然语言描述

The PLC elevator controller takes operational-mode, safety, car-call, hall-call, floor-sensor, levelling-sensor, and door signals as inputs. It prioritizes hall and car calls, drives the up/down indication display, and controls the door to open and close automatically. When no request is pending, the elevator remains at its current floor with the door open and the floor lamp indicating the current position.

### 3. 逐句溯源

1. 句子 1：The PLC elevator controller takes operational-mode, safety, car-call, hall-call, floor-sensor, levelling-sensor, and door signals as inputs.
   对应摘录：A
2. 句子 2：It prioritizes hall and car calls, drives the up/down indication display, and controls the door to open and close automatically.
   对应摘录：A
3. 句子 3：When no request is pending, the elevator remains at its current floor with the door open and the floor lamp indicating the current position.
   对应摘录：A
