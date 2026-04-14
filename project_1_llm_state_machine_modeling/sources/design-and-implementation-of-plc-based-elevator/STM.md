# Design and Implementation of PLC based Elevator - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把呼梯输入锁存、正反转行驶、楼层停靠、门机 `5` 秒延时关闭和火警就近下行停靠写得足够完整，但整体画像与现有 `G4` 电梯调度簇高度同构，更适合作为降采样补充。

## 条目 1: Cabin travel, door-cycle, and fire-return elevator controller

- 控制对象：楼宇机电与电梯控制领域的 PLC 电梯呼梯、行驶、开关门与火警回落控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4）

### 0. 条目识别与判定

- 一句话说明：这是一个以 `PLC` 为核心的自动电梯控制器，围绕呼梯按钮、楼层检测、门机电机和火警传感器组织轿厢的正反转、停靠、开门、延时关门与火警回落逻辑。
- 判断：算。对象是实际电梯控制器，原文不仅给出输入锁存和楼层停靠规则，还明确写出门机打开/关闭链、`5` 秒延时以及火警触发后的最近下行楼层停靠规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4-5 页，`4.1 Logic for getting input from call buttons and to latch`，`paper_content.txt` 第 374-407 行
> As an initial move the ladder logic has to be developed for receiving the input signal from the call buttons and the same is used with the program to get the corresponding output based on this input. Once the PLC receives the signal the corresponding bit will be latched.
>
> ... when a particular switch from the corresponding floor has been pressed the program in the PLC gets activated and the relevant bit will be latched. The latching will be there until that bit has been unlatched by another bit.

#### 摘录 B

- 出处：第 5 页，`4.2 Logic for motor operation and to get signal from the floor sensors`，`paper_content.txt` 第 422-448 行
> The next step of receiving the input signal is to make the motor to operate either in forward or in reverse direction and the logic has been developed correspondingly.
>
> ... The motor operation is purely based on the input that the PLC gets from the call buttons... Based on the desired input and corresponding floor the PLC will make the motor to stop.
>
> The output of LDR sensor for finding the floor is connected with the input terminal %I00007 of the PLC. In order to reduce the number of inputs counter has been used, corresponding to the counting in the counter the PLC will make the motor to stop.

#### 摘录 C

- 出处：第 5-6 页，`4.3 Logic for door opening` 与 `4.4 Logic for door closing`，`paper_content.txt` 第 450-493 行
> Once the operation of the elevator motor ceases the logic has to be developed in such a way that it facilitates the door opening... Based on the inputs from the call buttons, the floor sensors and the program downloaded in the PLC the door will open and close.
>
> Figure 6 describes the operation of door motor. According to our logic when both the forward and reverse motoring of the elevator motor stops the door opening logic gets latched... this latching will make the door opening motor to stop. This operation will initiate the next process of door closing.
>
> Figure 7 describes the operation of door closing... The ON-Delay Timer will be activated this will provide a delay of 5 seconds before the door closes. After the delay the door motor starts to rotate in the reverse direction... At the end of door closing the sensor will give a signal to the PLC this will stop the door motor.

#### 摘录 D

- 出处：第 6 页，`4.5 Fire sensor logic`，`paper_content.txt` 第 499-509 行
> As a safety measure a fire sensor has been fitted with the elevator cabin...
>
> Once this input has been activated the PLC will initiate reverse motoring and also it is designed to stop the elevator in the nearest down floor.

### 2. 基于原文整理后的自然语言描述

The elevator controller first latches each floor-call input in the PLC so that every request remains pending until another bit explicitly unlatches it. Once a request is active, the cabin motor is driven either forward or reverse according to the requested floor, and the floor-sensor input `%I00007` is counted so the PLC can stop the cabin exactly at the target level. After cabin motion stops, the door-opening logic latches `%Q00003` and keeps the door motor running until the full-open sensor `%I00011` is triggered. Door closing does not start immediately: the PLC activates an ON-delay timer, waits `5` seconds, and then drives `%Q00004` in reverse until the closing sensor `%I00012` stops the door motor. If the fire sensor `%I00015` is activated, the controller abandons the normal trip sequence, forces reverse motoring, and stops the elevator at the nearest down floor.

### 3. 逐句溯源

1. 句子 1：The elevator controller first latches each floor-call input in the PLC so that every request remains pending until another bit explicitly unlatches it.
   对应摘录：A
2. 句子 2：Once a request is active, the cabin motor is driven either forward or reverse according to the requested floor, and the floor-sensor input `%I00007` is counted so the PLC can stop the cabin exactly at the target level.
   对应摘录：B
3. 句子 3：After cabin motion stops, the door-opening logic latches `%Q00003` and keeps the door motor running until the full-open sensor `%I00011` is triggered.
   对应摘录：C
4. 句子 4：Door closing does not start immediately: the PLC activates an ON-delay timer, waits `5` seconds, and then drives `%Q00004` in reverse until the closing sensor `%I00012` stops the door motor.
   对应摘录：C
5. 句子 5：If the fire sensor `%I00015` is activated, the controller abandons the normal trip sequence, forces reverse motoring, and stops the elevator at the nearest down floor.
   对应摘录：D
