# Next-Gen Railway Crossings with IoT Solutions for Enhanced Safety and Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 IoT 道口门控系统明确写成 `Idle -> Train Approaching -> Gate Closing -> Train Crossing -> Train Departure -> Gate Opening` 六状态 FSM，并给出传感器、LED、蜂鸣器和 servo 动作链。

## 条目 1: Vibration-sensed six-state crossing gate supervisor

- 控制对象：轨道交通与铁路控制领域的 IoT 铁路平交口闸门控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 NodeMCU、Firebase、双振动传感节点和 gate node 的铁路平交口闸门监督控制器，用列车到达/离开振动事件驱动闸门闭合与重开。
- 判断：算。对象是真实铁路 crossing gate control，而不是单纯 IoT 架构介绍；原文直接定义了 FSM 状态、状态事件和对应的 servo / LED / buzzer 动作。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 26-36 行
> This study provides an IoT-based railroad crossing system, which can improve safety using a combination of the NodeMCU, vibration sensors, and Firebase to control the gates in real time.
>
> ... The system will comprise three interconnected nodes namely two vibration sensor nodes that will be located at strategic points along the track and a gate node that has the leadership of a servo motor, a buzzer and LED indicators. Sensor data of the presence of a train is sent to the gate node when it has been recognized by the firebase, which closes the gate automatically and sends alert notifications. When the train takes off, the second sensor is utilized to open the system again.

#### 摘录 B

- 出处：第 6-8 页，`3.2 Formal Gate Control Algorithm`，`paper_content.txt` 第 242-284 行
> To ensure reliable decision-making and system behaviour ... we implement a Finite State Machine (FSM) for managing the railway gate operation.
>
> The FSM consists of the following states:
> •State 1: Idle (Gate Open) ... Gate remains open. LED remains OFF. Buzzer remains OFF.
> •State 2: Train Approaching (First Sensor Triggered) ... Send "Train Approaching" signal via NodeMCU to Firebase. LED turns ON. Buzzer sounds intermittently.
> •State 3: Gate Closing ... The servo motor activates to close the gate.
> •State 4: Train Crossing (Gate Closed) ... Continuous monitoring of second vibration sensor (Sensor B) ...
> •State 5: Train Departure (Second Sensor Triggered) ... Send "Train Passed" signal via NodeMCU to Firebase.
> •State 6: Gate Opening ... Servo motor activates to open the gate ... System resets to Idle.

#### 摘录 C

- 出处：第 8 页，`Table 2. State Transition Table for Gate Control System`，`paper_content.txt` 第 285-293 行
> Current State Event Next State Action
> Idle Train detected by Sensor A Train Approaching Turn on LED, sound buzzer, prepare gate
> Train Approaching Gate close command sent Gate Closing Start servo motor to close gate
> Gate Closing Gate closed confirmed Train Crossing Maintain gate closed, monitor crossing
> Train Crossing Train detected by Sensor B Train Departure Prepare gate opening, turn off buzzer
> Train Departure Gate open command sent Gate Opening Start servo motor to open gate
> Gate Opening Gate opened confirmed Idle Reset system, turn off LED and buzzer

### 2. 基于原文整理后的自然语言描述

The railway-crossing controller is a six-state FSM built around two vibration-sensor nodes and a gate node connected through NodeMCU and Firebase. In `Idle`, the gate stays open and both LED and buzzer remain off. When Sensor A detects an approaching train, the controller enters `Train Approaching`, publishes the approach signal through Firebase, turns the LED on, and sounds the buzzer before handing over to `Gate Closing`, where the servo motor closes the barrier. Once the gate-closed condition is confirmed, the machine enters `Train Crossing` and waits for Sensor B on the departure side. The departure event triggers `Train Departure`, after which `Gate Opening` drives the servo in the opposite direction, turns off the LED and buzzer, and resets the system to `Idle`. Because the paper gives both the narrative state list and a tabular transition relation, the original source preserves a complete crossing-gate supervisor rather than only a prose description of automation hardware.

### 3. 逐句溯源

1. 句子 1：The railway-crossing controller is a six-state FSM built around two vibration-sensor nodes and a gate node connected through NodeMCU and Firebase.
   对应摘录：A, B
2. 句子 2：In `Idle`, the gate stays open and both LED and buzzer remain off.
   对应摘录：B
3. 句子 3：When Sensor A detects an approaching train, the controller enters `Train Approaching`, publishes the approach signal through Firebase, turns the LED on, and sounds the buzzer before handing over to `Gate Closing`, where the servo motor closes the barrier.
   对应摘录：A, B, C
4. 句子 4：Once the gate-closed condition is confirmed, the machine enters `Train Crossing` and waits for Sensor B on the departure side.
   对应摘录：B, C
5. 句子 5：The departure event triggers `Train Departure`, after which `Gate Opening` drives the servo in the opposite direction, turns off the LED and buzzer, and resets the system to `Idle`.
   对应摘录：A, B, C
6. 句子 6：Because the paper gives both the narrative state list and a tabular transition relation, the original source preserves a complete crossing-gate supervisor rather than only a prose description of automation hardware.
   对应摘录：B, C
