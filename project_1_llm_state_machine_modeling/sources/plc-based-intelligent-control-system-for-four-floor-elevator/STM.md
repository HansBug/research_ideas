# PLC-Based Intelligent Control System for Four-Floor Elevator - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接把电梯控制逻辑概括成 `Ascending / Descending / Stopped` 状态机，并补充了门阻挡与超载约束。

## 条目 1: Ascending-Descending-Stopped State Machine
- 控制对象：楼宇机电领域的四层电梯 PLC 控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个四层电梯控制器，用于管理车内外呼叫、方向优先调度、门控、安全联锁以及手动/自动运行。
- 判断：算。对象是实际电梯控制系统，原文明确点名状态机状态和状态转移条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Section 2.2 Control Logic Strategy, 行 66-92
> The PLC program implements all elevator control logics, processes the inputs, and drives the outputs accordingly. The system is connected to the following components: Car Motor: Two outputs control the drive motor direction (Up and Down). Door Actuators: One output controls the door mechanism (opening and closing of both cabin and landing doors). Floor Sensors: Each floor has a sensor (limit switch) that signals the car’s arrival; these reset the current floor variable in the PLC. Obstruction Sensor: A sensor at the door detects whether the doorway is blocked, inhibiting door closing. Overload Sensor: A weight (load) sensor in the cabin signals if the car is overloaded; if true, the program disallows motion until cleared. Car Call Buttons set car-call requests and Hall Call Buttons set hall-call requests in PLC.
>
> The PLC logic maintains a state machine that processes these inputs and controls the outputs. Key features include: Collective Call Scheduling: When moving in one direction, the elevator serves all requests in that direction before reversing. For example, if the car is travelling up and there are pending requests above the current floor, it continues upward until they are cleared and then changes direction. Direction State Machine: The program has three states: Ascending, Descending, and Stopped. Transitions depend on pending calls and the current state.

### 2. 基于原文整理后的自然语言描述

The controller manages motor direction, door actuation, floor sensing, obstruction detection, overload interlocking, and both car-call and hall-call requests. It maintains a three-state direction machine with Ascending, Descending, and Stopped states, and it serves all requests in the current direction before reversing. Door closing is inhibited by a doorway obstruction, and car motion is disallowed while the cabin remains overloaded.

### 3. 逐句溯源

1. 句子 1：The controller manages motor direction, door actuation, floor sensing, obstruction detection, overload interlocking, and both car-call and hall-call requests.
   对应摘录：A
2. 句子 2：It maintains a three-state direction machine with Ascending, Descending, and Stopped states, and it serves all requests in the current direction before reversing.
   对应摘录：A
3. 句子 3：Door closing is inhibited by a doorway obstruction, and car motion is disallowed while the cabin remains overloaded.
   对应摘录：A
