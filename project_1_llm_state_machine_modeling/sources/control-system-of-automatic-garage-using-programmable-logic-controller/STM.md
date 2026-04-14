# Control system of automatic garage using programmable logic controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把基于 PLC 的车库门禁、RFID 识别、车位分配、门机开闭、计时计费和满位阻断链写成了较完整的工程控制闭环。

## 条目 1: RFID-Guided Garage Entry/Exit and Slot-Allocation Controller
- 控制对象：智慧停车领域的 PLC 车库门禁与车位分配控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个基于 Siemens S7-1200、RFID、IR 车位传感器、步进电机和 SCADA 的自动车库控制器，负责识别车辆、判空分配、开闭入口/出口闸门并记录停车时长。
- 判断：算。对象是实际停车场门禁与车位管理控制系统，原文直接给出了输入设备、逻辑分层、计时/计数机制、开闸 guard 和满位阻断分支。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，`2. PROPOSED AUTOMATIC GARAGE CONTROL SYSTEM`，`paper_content.txt` 第 111-131 行
> The hardware comprises PLC ... infrared sensor, smoke sensor, RFID ... LEDs and stepper motor . ... The software part includes PLC for building ladder logics and SCADA screen is used for displaying. IR sensors are used to detect the presence of a vehicle in various slots within the infrared range ...
>
> There are 2 RFID’s in the project. One at the entrance and the other at the exit side. ... The PLC kit is programmed through the ladder logic for specific operations. The ladder logic designing consists of three parts:
>  Main logic: connecting the LED’s, RFID ’s, Motor’s and the sensors to work with respect to each other.
>  RFID logic: both the RFID’s are connected and designed for comparison of values and flowingly they give the output.
>  Motor logic: both the motors are designed in a way that the gates open when there is an absence of slot in the parking area.
>  Car parking: if there is space then only allotment of slots takes place otherwise gate doesn’t open and the LED’s glow in the di rection of movement of the car.

#### 摘录 B
- 出处：第 3-4 页，`3. PROGRAMMABLE LOGIC CONTROLLER [PLC] / 4. RFID`，`paper_content.txt` 第 162-167 行、第 204-220 行
> The function of a timer is that it keeps the output on for a certain length of time. The timers used in PLC are T -ON, T-OFF, TP. The T -ON timer switches on after a certain time specified. The T -OFF timer switches off after certain time and the TP remains on for a certain period. Counter s are used for counting items.
>
> In this project we are using two RFID’s i.e., one for entry level for detection of the vehicle RFID number and the other for the exit level for noting down the outgoing vehicle. Through this proce ss, the parking time could be calculated and thus the parking fee could also be calculated. ... These constant values are used during the initialization of RFID’s by assigning it to the comparators to compare . For example, the cons tant value of Car_1 is 1023 so, it lies within a range of 950 and 1070.

#### 摘录 C
- 出处：第 5-8 页，`6. HARDWARE IMPLEMENTATION / 7. SOFTWARE IMPLEMENTATION`，`paper_content.txt` 第 263-271 行、第 290-344 行
> The signals from the IR sensors of all the 4 parking are ... sent to the PLC kit. Also, the signal from the RFID is sent to the microcontroller, which in turn sends it to PLC. According to the ladder logic designed in the PLC, the PLC will allow the opening and closing of the gate ... The command for the motor to operate is given only when the RFID detects the car and there are empty slots available based on the output of IR sensor.
>
> The entire software part of the project is implemented through TIA software, which supports both PLC and SCADA. We have separately designed the logic for the working of motor, RFID, car timing and the main ladder logic circuit. In Figure 9. I0.0 to I0.3 are from th e IR sensors which detect the presence of car in corresponding parking slots ... Results in the opening and closing of the gate. Similar ladder logic is designed for the 2nd stepper motor at the exit side also. RFID logic: The ladder logic is designed based on the calculations of the constant value corresponding to a voltage level of the car. 2 comparators are used in the ladder logic for each car. Whenever the calculated value of the car lies between the comparators range it is stored in a memory. The memory for each car is connected in parallel, which means whenever any 1 of the car is detected and an empty slot is available (main logic circuit) the PLC commands the moto r to operate ...

### 2. 基于原文整理后的自然语言描述

The garage controller integrates IR slot sensors, smoke sensing, RFID readers, stepper-motor gate actuators, and a SCADA display around a Siemens S7-1200 PLC, so its state updates are driven by both occupancy variables and device-identification signals. Its ladder logic is explicitly split into `main logic`, `RFID logic`, `motor logic`, and `car parking` logic, and the controller allocates a slot and issues gate commands only when a vehicle identity is recognized and at least one slot is empty. The PLC uses timers and counters to keep outputs active for defined periods and to maintain parking-time information for billing, while the RFID path compares analog tag values against per-car comparator ranges before storing a match in memory and authorizing movement. If no slot is available the gate does not open and LEDs indicate the blocked direction, whereas on both entry and exit sides the corresponding motor is driven only when the combined RFID and IR-sensor guards are satisfied.

### 3. 逐句溯源

1. 句子 1：The garage controller integrates IR slot sensors, smoke sensing, RFID readers, stepper-motor gate actuators, and a SCADA display around a Siemens S7-1200 PLC, so its state updates are driven by both occupancy variables and device-identification signals.
   对应摘录：A
2. 句子 2：Its ladder logic is explicitly split into `main logic`, `RFID logic`, `motor logic`, and `car parking` logic, and the controller allocates a slot and issues gate commands only when a vehicle identity is recognized and at least one slot is empty.
   对应摘录：A, C
3. 句子 3：The PLC uses timers and counters to keep outputs active for defined periods and to maintain parking-time information for billing, while the RFID path compares analog tag values against per-car comparator ranges before storing a match in memory and authorizing movement.
   对应摘录：B, C
4. 句子 4：If no slot is available the gate does not open and LEDs indicate the blocked direction, whereas on both entry and exit sides the corresponding motor is driven only when the combined RFID and IR-sensor guards are satisfied.
   对应摘录：A, C
