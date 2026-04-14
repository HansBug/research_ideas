# Design of a PLC Based Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚写出了无请求停层开门、自动开关门、上/下行指示和 hall/car call 优先处理等电梯控制需求。

## 条目 1: Idle-Open and Auto-Door Elevator Workflow
- 控制对象：楼宇机电领域的 PLC 电梯控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个楼宇电梯控制器，用于采集 car-call、hall-call 和楼层传感器输入，并输出方向灯、到层灯以及门开关控制。
- 判断：算。对象是实际电梯控制系统，原文明确给出一组面向功能实现的离散控制要求。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section A-C, 行 108-143
> In PLC, the input signals are operational modes, safety control signals, car-calls, hall-calls, floor sensors, levelling sensors, door opening and close signals. All the functions of the elevator control systems are realized using the PLC programs, the functions includes registration, displaying the messages about the floors, monitoring the safety system, monitoring the door opening and closing, prioritizing the hall-call, and car-calls.
>
> This section presents the problems which are needed to solve through the ladder diagram. Ladder diagram is used to realize the many functionalities of the elevator control system. Some of the functionalities are, program should be written to make the display on which indicates the upward or downward movement, the door of the elevator should be programmed to open and close automatically, when the elevator has no request it remains at its current floor with its door opened, floor lamp should glow within the lift to indicate the current position.

#### 摘录 B
- 出处：第 2-4 页，`Flow Chart / Ladder Program / Fire Sensor Ladder Logic`，行 173-183, 192-209, 224-234
> The flow chart consists of three threads first thread checks
> the status of the push button within the lift and also
> status of push buttons in different floors, and also the
> management of the request queues are also monitored
> in the first thread. Second thread sets the current position of the lift to
> proper value taking input from the queue. Third thread
> is responsible for the upward and downward moment of
> the elevator car. If the current position of the elevator
> cabin is less than the first element of the queue then the
> elevator cabin should move in upward direction. If the
> current position of the elevator cabin is greater than the
> first element of the queue the elevator cabin should
> move in the downward direction.
> ...
> This program performs the two functions,
> -Make the elevator response the normal down hall-calls
> when it is moving down, and when a down hall-call is
> served, its registration is cancelled.
> -When the elevator is moving up, the corresponding
> floors down hall-call it passing by is not served and the
> registration is remained.
> ...
> The input terminal will detect the fire, and as the output
> the elevator will stops to the nearest down floor.

### 2. 基于原文整理后的自然语言描述

The PLC elevator controller takes operational-mode, safety, car-call, hall-call, floor-sensor, levelling-sensor, door, and fire-switch signals as inputs, and it outputs hall-call lamps, car-call lamps, door opening/closing commands, and up/down movement indications. Its logic is organized as three concurrent threads: one monitors car calls, hall calls, and the request queue, one updates the current position of the lift, and one compares the current position with the first queue element to decide upward or downward motion. The controller automatically opens and closes the door, keeps the elevator at its current floor with the door open when there is no request, and keeps the floor lamp indicating the current position. It also preserves opposite-direction hall calls instead of serving them while the car is moving the other way, and if the fire input is detected the elevator is guided to the nearest down floor.

### 3. 逐句溯源

1. 句子 1：The PLC elevator controller takes operational-mode, safety, car-call, hall-call, floor-sensor, levelling-sensor, door, and fire-switch signals as inputs, and it outputs hall-call lamps, car-call lamps, door opening/closing commands, and up/down movement indications.
   对应摘录：A
2. 句子 2：Its logic is organized as three concurrent threads: one monitors car calls, hall calls, and the request queue, one updates the current position of the lift, and one compares the current position with the first queue element to decide upward or downward motion.
   对应摘录：B
3. 句子 3：The controller automatically opens and closes the door, keeps the elevator at its current floor with the door open when there is no request, and keeps the floor lamp indicating the current position.
   对应摘录：A
4. 句子 4：It also preserves opposite-direction hall calls instead of serving them while the car is moving the other way, and if the fire input is detected the elevator is guided to the nearest down floor.
   对应摘录：B
