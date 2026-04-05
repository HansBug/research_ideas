# Automated Parking System Using PLC Technology - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场可用车位判断、入口/出口门禁、继电器正反转驱动和限位停机链条写成了完整的 PLC 工程控制对象。

## 条目 1: Vacancy-Sensed Dual-Gate Parking Supervisor
- 控制对象：智慧停车与车位管理领域的双门禁停车场可用车位监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 PLC 停车场控制器，用于持续监测空位、决定入口/出口闸门是否动作，并通过继电器和限位开关完成闸门开闭。
- 判断：算。对象是实际停车控制系统，原文明确给出了可用车位检测、车辆到门检测、闸门开闭、满位锁闭和电机停机逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 25-38 行
> A prototype system was designed using a programmable logic controller (PLC), incorporating a display screen located outside the parking area to monitor vacant spaces and provide drivers with real-time information on their locations. The system features two gates - one for entry and another for exit - along with two sensors to detect the presence of vehicles and multiple sensors to identify available parking spots. When space is available, the system triggers the gate to open, and if the parking facility is full, the PLC signals the gate to remain closed, marking the lot as fully occupied.

#### 摘录 B
- 出处：第 7-10 页，Practical Implementation / Wiring Diagram，`paper_content.txt` 第 222-247、320-329 行
> Entry and exit gates are designed using DC motor with two limit switches ... Four relays were used to control the opening and closing of the gates.
>
> A Photoelectric sensor was used to sense the presence of a vehicle in front of the gates ... Sensors (limit switches and Photoelectric sensors) were used to determine if the parking space was vacant or not.
>
> If R1 is energized ... motor 1 is running forward representing opening action for the gate1 ... If R2 is energized ... the motor 1 is running reverse representing closing action for gate 1 ... limit switch is attached respectively to gate 1 and gate 2 in order to serve the stop action of motor1 movement by sending signal to PLC.

#### 摘录 C
- 出处：第 11 页，Results and Discussion，`paper_content.txt` 第 346-350 行
> The system was designed so that the gate automatically opens if parking is available, and if the lot is full, the PLC sends a signal to close the entrance gate and mark the space as reserved.

### 2. 基于原文整理后的自然语言描述

The parking controller supervises both the entry gate and the exit gate and keeps the outside display updated with vacancy information collected from parking-space sensors. When a vehicle is detected in front of a gate, the PLC checks whether any parking space is vacant; if space is available it commands the corresponding DC gate motor to open, otherwise it keeps the entrance gate closed and marks the lot as full. The gate motors are driven through relays that select forward rotation for opening and reverse rotation for closing. Limit switches stop the motor automatically at the end positions so that each gate returns to a stable open or closed state without manual intervention.

### 3. 逐句溯源

1. 句子 1：The parking controller supervises both the entry gate and the exit gate and keeps the outside display updated with vacancy information collected from parking-space sensors.
   对应摘录：A, B
2. 句子 2：When a vehicle is detected in front of a gate, the PLC checks whether any parking space is vacant; if space is available it commands the corresponding DC gate motor to open, otherwise it keeps the entrance gate closed and marks the lot as full.
   对应摘录：A, B, C
3. 句子 3：The gate motors are driven through relays that select forward rotation for opening and reverse rotation for closing.
   对应摘录：B
4. 句子 4：Limit switches stop the motor automatically at the end positions so that each gate returns to a stable open or closed state without manual intervention.
   对应摘录：B
