# Automatic Car Parking and Controlling System Using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把停车场入口/出口闸门、车位计数、满位/空位指示和定时关门逻辑写得足够完整，但与现有 PLC 停车门禁样本相似度较高。

## 条目 1: Entry-Exit Gate Cycle with Occupancy Counter
- 控制对象：智慧停车领域的 PLC 停车场入口/出口门禁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个基于 LOGO! PLC、红外传感器、闸门电机、计数器和 LED 指示的停车场入口/出口控制器，负责判断剩余车位、定时开闭闸门并维护进出车辆数。
- 判断：算。对象是实际停车场门禁控制系统，原文明确给出了输入传感器、闸门动作、计数更新、容量 guard、定时关闭和满位/空位输出。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract，`paper_content.txt` 第 16-29 行
> In this paper, the automation process of an automatic car parking system is designed using a fully functional ladder logic based LOGO!12/24 RC , which is a small programmable logic controller (PLC). Infrared sensor (IR) electronic sensors were installed at the entr ance and departure gates to sense the car those are waiting for either entry or exit. After that it gives the input signals to PLC to count the number of vehicles entering and leaving the park respectively.
>
> The developed system automatically can monitor an d restrict the vehicles inside the parking space. The number of cars available in the park will be the difference of the number of vehicles entering and the number of vehicles leaving. When a car approaches to the entry gate, PLC will decide whether any sp ace is available or not. If no space is available, the PLC will then send signal to entry gate to keep the gate closed and turn on the indication “Car Park Full”. If there is space in the park, the entry gate will open to allow the car to enter the park. S imilarly, at the time of exit, the PLC will send signal to the exit gate to open and allow the car to leave the park after paid the parking payment.

#### 摘录 B
- 出处：第 2-3 页，`A. System Design / B. Hardware Equipment`，`paper_content.txt` 第 58-60 行、第 66-81 行
> Figure 1 present the system design which consists of Programmable Logic Controller (PLC LOGO! 12/24 RC), LADSIM (Ladder logic simulator), LED display, DC motor and IR sensors. Here, PLC acted as the brain of this system because it controlled all the operations with the external devices.
>
> programmable logic controller was used as a black box with a number of inputs from, and a number of outputs to, the outside world. It can make decisions easier, store data, convert codes, do timing cycles, and do simple arithmetic analysis. ... LOGO! functions include inputs, outputs, timers, counters, flags and shift registers. ... photoelectric sensors (IR) were used ... two DC motors were used to open and close the barrier for entry and exit of the cars ... LED d isplay were used to display the status of the parking system. It indicates whether the parking space is available or not.

#### 摘录 C
- 出处：第 3 页，`C. Software Design`，`paper_content.txt` 第 95-104 行
> The software design of this system was develop ed based on the following two logics, 1) motor opens the entry gate when a car is at the entry barrier and the car parking space is not full. A timer starts to count the number of vehicles (with increment) when the entry gate is opened. Then, automatically the entry gate becomes close when the time is over. Finally LED indicates the “Full” signal, if the counter is at maximum level, and 2) the motor opens the exit gate when a car is at the exit barrier. The timer starts to count the number of vehicles (with decrement) when the exit gate is open. Then the exit gate becomes close when the time is over. Finally, the LED indicates “Empty” symbol when the counter is at minimum.

### 2. 基于原文整理后的自然语言描述

The parking controller uses a LOGO! PLC, entry and exit IR sensors, gate motors, timers, counters, and LED status outputs to manage admission and departure in a bounded parking lot. When a car reaches the entry barrier, the controller checks whether the occupancy counter is still below capacity; if space exists it opens the entry gate, starts a timed entry cycle, increments the vehicle count, and closes the gate again when the timer expires. If the lot is full, it keeps the entry gate closed and raises the `Car Park Full` indication so the driver must leave or wait for a vacancy instead of entering the controlled area. At the exit barrier it opens the exit gate after the departure condition is met, runs a second timed cycle that decrements the occupancy counter, closes the gate when the exit timer finishes, and turns on the `Empty` indication when the count reaches its minimum.

### 3. 逐句溯源

1. 句子 1：The parking controller uses a LOGO! PLC, entry and exit IR sensors, gate motors, timers, counters, and LED status outputs to manage admission and departure in a bounded parking lot.
   对应摘录：A, B
2. 句子 2：When a car reaches the entry barrier, the controller checks whether the occupancy counter is still below capacity; if space exists it opens the entry gate, starts a timed entry cycle, increments the vehicle count, and closes the gate again when the timer expires.
   对应摘录：A, C
3. 句子 3：If the lot is full, it keeps the entry gate closed and raises the `Car Park Full` indication so the driver must leave or wait for a vacancy instead of entering the controlled area.
   对应摘录：A, C
4. 句子 4：At the exit barrier it opens the exit gate after the departure condition is met, runs a second timed cycle that decrements the occupancy counter, closes the gate when the exit timer finishes, and turns on the `Empty` indication when the count reaches its minimum.
   对应摘录：A, C
