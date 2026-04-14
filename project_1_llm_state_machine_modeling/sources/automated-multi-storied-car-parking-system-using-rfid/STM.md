# Automated Multi-storied Car Parking System Using RFID - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 RFID 门禁判定、楼层分配、升降机占用与回位链条写得较完整，能够整理出一个从鉴权到入位再到回到地面待命的停车控制样本。

## 条目 1: RFID Access, Floor Allocation, and Lift Return Cycle

- 控制对象：智慧停车领域的多层立体停车场门禁与升降机调度控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以 RFID 卡鉴权、楼层容量判断、报警反馈和升降机传送为核心的多层立体停车控制器。
- 判断：算。对象是实际停车控制系统，原文明确给出合法卡校验、空位分配、升降机忙闲判断、报警条件以及升降机到位与回地面的完整操作链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`Introduction / Figure 1`，`paper_content.txt` 第 58-65 行
> Figure 1 shows overall block diagrams for car parking system. System is composed of a lift to carrying car and three floors building. There are three cars can be kept in one floor as maximum. So, maximum capacity can be nine for three floors.
>
> If lift is free, car is carried to first floor. If first floor is full, second floor is automatically chosen by system. If lift is busy, an alarm indicated that access is stopped.
>
> For accessing the floors, user must enter valid predefined security card number with RFID. If number is granted, green LED will light on and car will be carried to floor.

#### 摘录 B

- 出处：第 6-7 页，`System design / Figure 6`，`paper_content.txt` 第 212-220 行、第 227-244 行
> The RFID System consists of a reader, and RFID tags. ... When an RFID Parking Management System user’s car approaches the gate, the induction and communication between RFID tag inside the car and antenna of RFID system is automatically established. Then the reader of RFID system translates the signal information to the digital content. Figure 6 presents the work flowchart of the RFID system.
>
> START ... Reader has received the signal from the RFID tag ... RFID will judge the validity of card ... Card = Registered ... Make entry in the registration form ... Display information in registration form ... The output is displayed an LCD ... Assign the parking lot ... END

#### 摘录 C

- 出处：第 8 页，`RFID card control system`，`paper_content.txt` 第 266-269 行
> RFID reader reads the ID number from the RFID tag. Then, the reader sends the ID number to the PIC for checking with the database. If the ID number is valid, the user will be selected the room number with the mobile phone. And then, the car is presented that the room number will be showed at LCD and 7-segments. If the ID number is invalid, the alarm will be opened.

#### 摘录 D

- 出处：第 14 页，`Test Result for Automated Car Parking System`，`paper_content.txt` 第 617-621 行
> After all sensors and motor supply are connected properly, system is power up. The lift is kept on the ground floor of the system. When a small object (car) is placed on the lift, the lift is moving upward until room 1 at floor 1 IR sensor is detected ... After sensor is detected ... the lift motor is stopped. After object is removed from the lift ... the lift goes down to the ground floor and stay standby until the next car is arrived over the lift.

### 2. 基于原文整理后的自然语言描述

The parking controller is an RFID-gated EFSM that begins with a card-validation stage at the entrance, where the reader captures the tag ID, the PIC checks it against the database, and only a registered vehicle is allowed to proceed. After successful authentication, the system records the entry, shows the assigned room or slot information on the LCD and seven-segment display, and maps the car to an available parking place. The allocation logic is capacity-aware: the lift first tries the first floor, moves to higher floors when the lower level is full, and blocks new access with an alarm when the lift resource is busy. Once a car is placed on the lift, the motor drives the lift upward until the target IR sensor is triggered, then stops for unloading; after the car leaves the platform, the lift returns to the ground floor and stays in standby for the next arrival. This creates a complete authenticate-assign-lift-deliver-return cycle with explicit busy, full, valid, and invalid branches.

### 3. 逐句溯源

1. 句子 1：The parking controller is an RFID-gated EFSM that begins with a card-validation stage at the entrance, where the reader captures the tag ID, the PIC checks it against the database, and only a registered vehicle is allowed to proceed.
   对应摘录：A, B, C
2. 句子 2：After successful authentication, the system records the entry, shows the assigned room or slot information on the LCD and seven-segment display, and maps the car to an available parking place.
   对应摘录：B, C
3. 句子 3：The allocation logic is capacity-aware: the lift first tries the first floor, moves to higher floors when the lower level is full, and blocks new access with an alarm when the lift resource is busy.
   对应摘录：A, C
4. 句子 4：Once a car is placed on the lift, the motor drives the lift upward until the target IR sensor is triggered, then stops for unloading; after the car leaves the platform, the lift returns to the ground floor and stays in standby for the next arrival.
   对应摘录：D
5. 句子 5：This creates a complete authenticate-assign-lift-deliver-return cycle with explicit busy, full, valid, and invalid branches.
   对应摘录：A, B, C, D
