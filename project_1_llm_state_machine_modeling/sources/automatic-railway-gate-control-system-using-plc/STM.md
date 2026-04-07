# Automatic Railway Gate Control System Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 IR 传感器触发、红绿灯联动、关闸保持与列车离站开闸链写得直接清楚，可以形成一条可追溯的道口门控控制链。

## 条目 1: IR-Sensed Railway Gate Close-and-Reopen Controller

- 控制对象：铁路道口的栏杆门控与道路信号联动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是轨道交通与铁路控制领域的道口门控控制器，用 `IR sensor` 检测列车接近/离开，并驱动道路信号与栏杆开闭。
- 判断：算。对象是实际铁路道口控制系统，原文明确给出了到达检测、红灯与关闸动作、离站检测、绿灯与开闸恢复，以及 PLC 到电机执行链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 21-27 行、第 37-42 行
> Whenever train touches base at the IR sensor, caution is activated at the railway crossing so that the general population get instruction that entryway will be shut. At that point the control module initiates and shuts the gates on either side of the track. Once the train crosses, this module naturally lifts the gate. For mechanical operation of a gate DC adapted engines are utilized. We are using PLC as a main control unit.
>
> ... the arrival of the train is detected by the sensing element placed on the track at a precise distance from the gate. This sensing element detects the approaching train and consequently controls the operation of the gate. ... This reduces the time that gate is closed as compared to the gates operated manually.

#### 摘录 B

- 出处：第 3 页，`III. Description and Working`，`paper_content.txt` 第 79-92 行
> The proposed system uses infrared sensors to detect the trains crossing the road and motor to control traffic light and the opening or closing of gates. The system uses two sensors to detect the arrival of the train and a second sensor to detect the leaves of the train. When the arrival of the train is sensed, signals are provided to the traffic indicating the arrival of the train on the road such as the signal turns red and the motor operates to close the gate. When the second sensor detects the train, then the signal turns green and the motor operates to open the gate. The gate remains closed until the train completely moves away from the crossing road.

#### 摘录 C

- 出处：第 3-4 页，`III. Description and Working / V. System Architecture`，`paper_content.txt` 第 88-92 行、第 128-130 行
> When the PLC receives the signal from the sensor, then it produces the output based on ladder program which is fed to stepper motor driver for closing the gate.
>
> ... the signal from the sensor will play major role in complete process as an initial state the signal is sent to PLC then it produces the output base on our ladder program then it is fed to drive the DC motor.

### 2. 基于原文整理后的自然语言描述

The railway crossing controller uses a PLC plus infrared sensors to supervise a simple arrival-close-departure-open gate sequence. When the first sensor detects an approaching train, the controller warns road users, turns the road signal red, and drives the gate motor so the barriers close on both sides of the track. The crossing then remains closed while the train occupies the protected zone. After the departure sensor confirms that the train has moved away, the PLC changes the road signal to green and drives the motor in the opening direction so the gate returns to its open state.

### 3. 逐句溯源

1. 句子 1：The railway crossing controller uses a PLC plus infrared sensors to supervise a simple arrival-close-departure-open gate sequence.
   对应摘录：A, B, C
2. 句子 2：When the first sensor detects an approaching train, the controller warns road users, turns the road signal red, and drives the gate motor so the barriers close on both sides of the track.
   对应摘录：A, B, C
3. 句子 3：The crossing then remains closed while the train occupies the protected zone.
   对应摘录：B
4. 句子 4：After the departure sensor confirms that the train has moved away, the PLC changes the road signal to green and drives the motor in the opening direction so the gate returns to its open state.
   对应摘录：A, B
