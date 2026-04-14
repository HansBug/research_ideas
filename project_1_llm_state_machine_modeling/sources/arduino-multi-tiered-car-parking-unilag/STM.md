# An Arduino-Based Automated Multi-Tiered Car Parking System for University of Lagos and Expected Financial Gains - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 RFID 校验、车位占用检测、满位禁止入场、入口/出口开闸和计数更新的完整停车场门禁控制链。

## 条目 1: RFID-Validated Entry/Exit and Occupancy Counter Parking Controller

- 控制对象：多层停车场的入口/出口门禁与车位占用监控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 Arduino 停车场门禁控制器，用 RFID 卡、红外车位传感器、LCD、LED 和入口/出口舵机实现授权放行、满位封锁和进出计数。
- 判断：算。对象是实际停车场控制系统，原文给出了合法/非法卡判定、满位逻辑、入口/出口开闸动作以及计数器增减链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / 2.1 Design of the Entry/Exit Point Control System`，`paper_content.txt` 第 13-19 行、第 82-87 行
> A prototype of Arduino-based automated two-tiered car park was designed and produced which allows entry/exit to only authorized users with radio frequency identification (RFID) cards. A liquid crystal display (LCD) shows the available number of parking spaces and locations.
>
> In the proposed system, a user will be issued a RFID Card properly documented to serve a dual purpose - ensures the holder has satisfied requirements for accessing the park to avoid unauthorised parking and allows exit after validation as a means of checking theft.

#### 摘录 B

- 出处：第 5 页，`Sensor Section`，`paper_content.txt` 第 196-199 行
> Each parking space is equipped with an IR sensor that sends messages to the Arduino to check if a car is already parked and with the LCD module visually displays a vacant space. When all spaces are engaged, the Arduino will not enable the servo motor to open the entrance gate anymore and “FULL” will be displayed.

#### 摘录 C

- 出处：第 9-10 页，`4.2 Test-running the System / 4.3 Entry and Exit Sequences`，`paper_content.txt` 第 405-418 行、第 436-437 行
> When a valid RFID card was swiped, the LCD displayed “Access Allowed” ... the LCD displayed “Access Denied” when an invalid RFID card was used ... The availability of space is indicated by the LED’s at the entrance ... when the first floor is fully occupied; the “red LED” turns on while the “green LED” turns off.
>
> When the driver places a valid RFID card on the reader, the entrance gate opens, the car enters the park and the counter increases by one ... when a car is about to leave the car park the driver places a valid card on the reader, the exit gate opens, the car leaves and the counter decreases by one.

### 2. 基于原文整理后的自然语言描述

The parking controller starts by validating the driver’s RFID card and immediately distinguishes between authorized entry and denied access on the LCD. Occupancy information from six IR sensors is used to track whether parking spaces are vacant, and once all spaces are engaged the Arduino blocks the entrance servo and displays `FULL` instead of opening the gate. If a valid card is presented while capacity is available, the entrance gate opens and the parking counter increments as the vehicle enters. When a valid card is presented at departure, the exit gate opens and the counter decrements so the available-space display can be updated for the next vehicle.

### 3. 逐句溯源

1. 句子 1：The parking controller starts by validating the driver’s RFID card and immediately distinguishes between authorized entry and denied access on the LCD.
   对应摘录：A, C
2. 句子 2：Occupancy information from six IR sensors is used to track whether parking spaces are vacant, and once all spaces are engaged the Arduino blocks the entrance servo and displays `FULL` instead of opening the gate.
   对应摘录：B, C
3. 句子 3：If a valid card is presented while capacity is available, the entrance gate opens and the parking counter increments as the vehicle enters.
   对应摘录：A, C
4. 句子 4：When a valid card is presented at departure, the exit gate opens and the counter decrements so the available-space display can be updated for the next vehicle.
   对应摘录：C
