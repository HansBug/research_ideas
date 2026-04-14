# A NOVEL APPROACH OF LIFT CONTROL IN AUTOMATIC CAR PARKING USING PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把多层停车升降机的手动/自动模式、方向决策、层数计数、慢速接近、停层确认和错误分支写成了完整 PLC 控制链，足以形成双 A 样本。

## 条目 1: Multi-Level Parking Lift Auto/Manual Positioning Controller

- 控制对象：智慧停车领域的 PLC 多层停车升降机定位与存取控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用于多层自动停车库的升降机控制器，用 PLC、VFD、叉臂/托盘位置传感器和安全互锁来执行停车托盘的手动点动与自动层间搬运。
- 判断：算。对象是明确的停车设备升降机控制子系统，原文直接给出了模式划分、方向与层数决策、传感器 guard、慢速接近、停层确认和错误输出。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract 与 `1. INTRODUCTION`，`paper_content.txt` 第 13-20 行、第 58-72 行
> In this paper a novel approach for lift control is proposed in fully automatic Level Car Parking System which used to take cars in/out of system & park the cars. Entire system is controlled using a Programmable Logic Controller (PLC). As speed control is required for multiple speed setting & proper stopping accuracy, the lift will be driven by the VFD (Variable Frequency Drive) for speed control. The pallet position on lift, accurate positioning between lift-level & safety interlocks are sensed from dedicated sensor.
>
> In this paper, automatic control of lift in automatic car parking system is proposed. The total system is having two lifts, three level transfer mechanisms. A single PLC (BECKHOFF PLC) is used to control the entire parking system. For accurate speed control lift is operated with VFD. ... The flow sequences are designed according to system sequence for lift for manual mode & auto mode operations. The lift will be given command to go to specific level depending upon the storage pallet or parked car location in system.

#### 摘录 B

- 出处：第 1-2 页，`2. OVERVIEW DIAGRAM OF LIFT / 3. ELECTRICAL WIRING DIAGRAM OF VFD`，`paper_content.txt` 第 76-104 行、第 109-127 行
> The lift positions feedback are obtained from dedicated sensors. ... Fork sensor. This sensor is fixed and the dogs are mounted at each slat location. When input from this sensor is received the lift speed will be reduced. ... Slat Position confirmation sensor ... used to confirm that the lift has reached the correct position and the transfer of pallet to be done is safe. ... Pallet position on Lift ... During the Auto mode this sensor is used to insure the pallet position confirmation on the pallet ... Safety sensors: If the lift pallet not engaged properly during up/down movements, then Height/AntiLift sensors cut and stop the operation of Lift. The over travel sensors used to alarm the system that lift is going above the safe position limits.
>
> The control signals received from the PLC to VFD are Commands as Forward, Backward, slow speed, high speed, & reset. Also PLC receives feedback from VFD in terms of Run & Fault status signals.

#### 摘录 C

- 出处：第 3 页，`4. OPERATIONAL SEQUENCE`，`paper_content.txt` 第 145-189 行
> There are two types of sequences manual mode sequence and auto mode sequence.
>
> Manual Mode: a) The lift manual mode operation is inching. b) The lift inched with spring action button in up or down direction for maintenance work. c) Facility to change the speed will not be given. d) The speed in the manual/maintenance mode is slow speed. e) All manual mode actions are done from the HMI or from teach pendant.
>
> Auto Mode: a) lift is always waiting for command in auto mode ... b) The command given to the lift is in terms of direction and number of levels to move. c) depending upon the command direction lift starts to move respective direction d) Once slow sensor(fork sensor) is sensed the speed of the VFD is made slow. e) As soon as the stop sensor(fork sensor) is sensed the lift stops. f) The level position sensors are checked to ensure that the lift is stopped correctly. If there is a level difference, then the level confirmation sensor will not be sensed and error will be given.
>
> Then Number of levels to move = destination level no – source level no ... Since the number of levels to move < 0 so the direction is be up and the level counter is initialized to 1. ... Here no of levels is positive, it means that lift has given down command & two levels to move.

### 2. 基于原文整理后的自然语言描述

The parking lift controller is built around a Beckhoff PLC and a VFD, and it uses fork sensors, pallet-position sensors, level-confirmation sensors, and safety interlocks to move parking pallets between three transfer levels. The controller separates manual and automatic modes: in manual mode the lift is driven by inching commands from the HMI or teach pendant at fixed slow speed for maintenance, while in automatic mode it waits for a command that specifies both direction and the number of levels to move. Once an automatic command is accepted, the PLC computes the signed level difference, selects upward or downward travel, initializes a movement counter, drives the VFD in the chosen direction, slows down when the fork sensor is detected, and stops when the stop sensor is reached. After stopping, it checks the level-position and level-confirmation sensors to verify accurate alignment, and if the confirmation sensor is missing the controller raises an error instead of allowing pallet transfer. Safety sensors additionally cut the lift when pallet engagement is unhealthy or when over-travel conditions appear, so the resulting sample is a complete EFSM with nominal movement, manual maintenance, and error-stop branches.

### 3. 逐句溯源

1. 句子 1：The parking lift controller is built around a Beckhoff PLC and a VFD, and it uses fork sensors, pallet-position sensors, level-confirmation sensors, and safety interlocks to move parking pallets between three transfer levels.
   对应摘录：A, B
2. 句子 2：The controller separates manual and automatic modes: in manual mode the lift is driven by inching commands from the HMI or teach pendant at fixed slow speed for maintenance, while in automatic mode it waits for a command that specifies both direction and the number of levels to move.
   对应摘录：A, C
3. 句子 3：Once an automatic command is accepted, the PLC computes the signed level difference, selects upward or downward travel, initializes a movement counter, drives the VFD in the chosen direction, slows down when the fork sensor is detected, and stops when the stop sensor is reached.
   对应摘录：B, C
4. 句子 4：After stopping, it checks the level-position and level-confirmation sensors to verify accurate alignment, and if the confirmation sensor is missing the controller raises an error instead of allowing pallet transfer.
   对应摘录：B, C
5. 句子 5：Safety sensors additionally cut the lift when pallet engagement is unhealthy or when over-travel conditions appear, so the resulting sample is a complete EFSM with nominal movement, manual maintenance, and error-stop branches.
   对应摘录：B
