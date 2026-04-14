# CAR PARKING SYSTEM DESIGN IN VHDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车入口门禁控制明确写成了 `IDLE / WAIT_PASSWORD / RIGHT_PASS / WRONG_PASSWORD / STOP` 状态链，并给出了前后传感器、密码判定与 `4` 个时钟周期等待语义，足以形成停车方向的双 A 样本。

## 条目 1: Password-and-Sensor Parking Entry FSM

- 控制对象：智慧停车与车位管理领域的停车场入口门禁与跟车阻塞控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 `VHDL + Quartus` 实现的停车场入口控制器，用前后传感器、密码输入、门禁开关和红绿灯提示管理车辆放行、重试与跟车阻塞。
- 判断：算。对象是实际停车门禁控制系统而不是 HMI 或计费流程；原文直接写出命名状态、输入输出端子、`4` 周期密码等待和 `STOP` 阻塞逻辑，可以稳定恢复成 FSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 28 页，`3.3 Developing Diagram and Interface Signal of Car Parking System`，`paper_content.txt` 第 726-748 行
> With the information given in above the inputs and outputs for the system can be accumulate through the interface known as State Machine ... The inputs include the clock to set the time, the reset and the sensors ... Front Sensor ... Back Sensor ... Password 1 ... Password 2 ... Green LED ... FSM turns to RIGHT_PASS state ... Red LED ... Wrong pass state and if the next car is coming before parking the current car then Red LED will be blinking.

#### 摘录 B

- 出处：第 29 页，`3.4 State Diagram of Car Parking System`，`paper_content.txt` 第 758-774 行
> The state diagram of car parking system is shown in Figure 3.4 ... First State: At first the FSM is in IDLE position. When any car enters and senses by the front sensor the FSM turns into the next state. Second State: FSM changed to WAIT_PASSWORD state for 4 cycles. In this state the car will input the password. If the password which is entered by the driver is right then the gate is opened ... FSM express RIGHT_PASS and blink the Green LED. Third State: If the driver enters a wrong password the FSM swings to WRONG_PASSWORD state and blink the Red LED.

#### 摘录 C

- 出处：第 30-33 页，`3.4 State Diagram of Car Parking System`、`3.5.2 The Gate` 与 `3.5.4 The Exit`，`paper_content.txt` 第 779-783、809-812、823-830 行
> When password is right the car gets into the parking zone and identified by the back sensor. If there is another car coming to park the FSM turns into STOP state and blink the Red LED ... The FSM comes back to the IDLE state after the car passes the gate and gets into the car park.
>
> First connect with Altera, enter password for open the gate. If password =1 is correct relay will active to open the gate otherwise have to give password=2 ... Then car can enter into the parking lot and a signal give to rely to close the gate.
>
> Wait until the previous car is parked. And continue the process again ... The Finite State Machine (FSM) of Intelligent Car Parking System will be used as a reference in writing the VHDL code.

### 2. 基于原文整理后的自然语言描述

The proposed parking-entry controller is an explicit VHDL FSM driven by `Clock`, `Reset`, `Front Sensor`, `Back Sensor`, `Password 1`, and `Password 2`, with `Green LED`, `Red LED`, and display outputs tied to the current control state. When a vehicle is detected by the front sensor, the machine leaves `IDLE` and enters `WAIT_PASSWORD`, where the driver is given `4` cycles to enter the password. A valid password drives the controller to `RIGHT_PASS` so the gate opens and the green LED blinks for entry, while an invalid password drives `WRONG_PASSWORD` with blinking red indication until the secret word is entered correctly. After the vehicle is recognized by the back sensor, the controller uses `STOP` to hold following vehicles with red blinking, closes the gate after entry, and returns to `IDLE` once the previous car has been parked and the cycle can restart.

### 3. 逐句溯源

1. 句子 1：The proposed parking-entry controller is an explicit VHDL FSM driven by `Clock`, `Reset`, `Front Sensor`, `Back Sensor`, `Password 1`, and `Password 2`, with `Green LED`, `Red LED`, and display outputs tied to the current control state.
   对应摘录：A
2. 句子 2：When a vehicle is detected by the front sensor, the machine leaves `IDLE` and enters `WAIT_PASSWORD`, where the driver is given `4` cycles to enter the password.
   对应摘录：B
3. 句子 3：A valid password drives the controller to `RIGHT_PASS` so the gate opens and the green LED blinks for entry, while an invalid password drives `WRONG_PASSWORD` with blinking red indication until the secret word is entered correctly.
   对应摘录：A, B, C
4. 句子 4：After the vehicle is recognized by the back sensor, the controller uses `STOP` to hold following vehicles with red blinking, closes the gate after entry, and returns to `IDLE` once the previous car has been parked and the cycle can restart.
   对应摘录：A, C
