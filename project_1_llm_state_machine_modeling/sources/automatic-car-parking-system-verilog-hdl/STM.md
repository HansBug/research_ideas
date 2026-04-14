# Implementation of Automatic Car Parking System Using Verilog HDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场入口门禁、密码校验、车位信息输出和入场锁门逻辑写成了 `idle / wait password / parking` 主链，输入、状态和失败回退都可直接追溯，满足双 A。

## 条目 1: Idle-WaitPassword-Parking Gate Controller

- 控制对象：智慧停车与车位管理领域的密码门禁与车位引导控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向停车场入口/出口的离散门禁控制器，用车辆到达传感器、密码校验、出口占用与空位信息共同驱动 `idle -> wait password -> parking` 的入场控制链。
- 判断：算。对象是停车控制系统本身，不是单纯 FPGA 教学；原文明确列出入口触发、密码校验、两次失败回退、门锁/开门和空位显示逻辑，足以形成一条可追溯的 EFSM 样本。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 17-22 行
> In the entrance of the parking system, there is a sensor which is activated to detect a vehicle coming. Once the sensor is triggered, a password is requested to open the gate. If the entered password is correct, the gate would open to let the vehicle get in. Otherwise, the gate is still locked. If the current car is getting in the car park being detected by the exit sensor and another the car comes, the door will be locked and requires the coming cars to enter passwords.

#### 摘录 B

- 出处：第 6 页，Section 3 `Proposed System`，`paper_content.txt` 第 323-334 行
> A sensor is at the entrance of the parking system which is activated to detect a vehicle coming. When a car enters in, a password is needed. If the password entered is correct the gate will open or else it will be locked. This is also the same for the exit process. And with the help of ultrasonic sensor the distance is measured in which the next car is available, the number of vacant slots and the number of cars parked already will be given in the form of a message.

#### 摘录 C

- 出处：第 7 页，Section 3.2 `Car Parking System`，`paper_content.txt` 第 386-413 行
> In the entrance of the parking system, there is a sensor which is activated to detect a vehicle coming.
>
> Once the sensor is activated, a password is request to open the gate.
>
> Till that time the car will be in the idle state. Before entering the sensor entrance the current state will be in idle.
>
> In the sensor entrance it ask the password if it is wait password then it will be idle state.
>
> If it is correct password then it goes into parking.
>
> If it is wrong password then it give another chance and ask password again ... if it is wrong password then again it goes to idle state.
>
> It give 2 chances for password.
>
> If the entered password is correct, the gate would open to let the vehicle get in.

### 2. 基于原文整理后的自然语言描述

The proposed parking controller supervises entry to a parking lot with a stateful gate-access workflow rather than a pure vacancy counter. When the entrance sensor detects an arriving vehicle, the machine leaves the passive waiting condition and enters a password-check phase in which the car remains blocked until authentication succeeds. The paper explicitly names `idle`, `wait password`, and `parking` as the visible control stages: before detection the current state is `idle`, sensor activation triggers the password request, and a correct password moves the controller into `parking`, where the gate opens and the car is admitted. If the password is wrong, the controller grants one more attempt; if the second attempt also fails, it returns to `idle` with the gate still locked. In parallel with this gate logic, the system also reports the next available slot distance, the number of vacant spaces, and the number of parked cars, so the controller is an extended state machine that combines gate access with slot-status outputs.

### 3. 逐句溯源

1. 句子 1：The proposed parking controller supervises entry to a parking lot with a stateful gate-access workflow rather than a pure vacancy counter.
   对应摘录：A, B
2. 句子 2：When the entrance sensor detects an arriving vehicle, the machine leaves the passive waiting condition and enters a password-check phase in which the car remains blocked until authentication succeeds.
   对应摘录：A, C
3. 句子 3：The paper explicitly names `idle`, `wait password`, and `parking` as the visible control stages: before detection the current state is `idle`, sensor activation triggers the password request, and a correct password moves the controller into `parking`, where the gate opens and the car is admitted.
   对应摘录：C
4. 句子 4：If the password is wrong, the controller grants one more attempt; if the second attempt also fails, it returns to `idle` with the gate still locked.
   对应摘录：C
5. 句子 5：In parallel with this gate logic, the system also reports the next available slot distance, the number of vacant spaces, and the number of parked cars, so the controller is an extended state machine that combines gate access with slot-status outputs.
   对应摘录：B
