# Simulation of a PLC-based Car Parking System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然篇幅不长，但把六车位计数、入口检测、3 秒门禁定时、满位锁闭和出口回收容量写成了完整的 ladder 逻辑主链。

## 条目 1: Six-Slot Counted Entry Gate with Full-Lot Lockout
- 控制对象：智慧停车与车位管理领域的六车位计数停车门禁控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 LADSIM/PLC 停车门禁控制器，用于依据六个车位状态、入口车辆检测和计数结果决定入口门是否开放，并在满位时锁闭入口。
- 判断：算。对象是实际停车控制系统的 PLC 顺序逻辑，原文明确给出了车位传感、入口传感、定时器、计数器、满位灯和出口回收容量逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Experimental Setup / Block Diagram，`paper_content.txt` 第 133-167 行
> This experiment involves simulation with LADSIM of a car park with 6 cars capacity. There are six cars space at the car parking ground and six LDRs were then placed on each car space to detect the presence of a car over it ... The presence of a car waiting to enter the car parking will be detected by a set of IR sensor placed at the main gate ... In a situation where the data provided by the LDR shows the possibility of available space for car parking and at the same time IR sensor detects the presence of car waiting to get parked, the PLC will then direct the main parking gate to open ... if the data provided by the LDR shows the possibility of fully and completely occupied parking space, at that moment the PLC stops the main gate from opening.

#### 摘录 B
- 出处：第 2-3 页，Results and Discussion，`paper_content.txt` 第 171-223 行
> when a car breaks the beam, an accumulator (Acc) display for the timer increase in 0.1 second step and, after 3 seconds, the DN bit is then set ... the T1/DN is then permanently set and thereafter no other car is allowed through.
>
> the Counter 1 (C1) in the ‘count up’ mode such that every time the entrance barrier beam is broken it triggers the counter, and preset to 6 to represent the total capacity of the car park, when the C1/UP bit is set, i.e. 6 is reached, the Full light (OP2) turns on ... the exit beam [triggers] the same counter but this time in the ‘count down’ mode.
>
> To resolve these problem cars was prevented from entering the car park when it was full. Thus, a condition was added to the first rung that the full display was not on.

### 2. 基于原文整理后的自然语言描述

The simulated PLC parking controller monitors six LDR slot sensors and an IR sensor at the entrance gate to decide whether a waiting car may enter the car park. If at least one slot is free and the IR sensor detects a car at the entrance, the PLC opens the main gate and admits the vehicle; if all six slots are occupied, it keeps the gate closed and directs the driver to another parking area. After an entering car breaks the beam, a `3 seconds` timer is started, and once the timer done bit is set the ladder logic unlatches the gate output so that no following car can pass through immediately. A count-up counter tracks the occupied capacity up to six cars, turns on the Full light when the preset is reached, keeps the Spaces light on while capacity remains available, and uses the exit beam in count-down mode to release capacity again. When the authors found that a seventh car could still enter, they added a full-display condition to the first rung so that entry is locked out whenever the car park is already full.

### 3. 逐句溯源

1. 句子 1：The simulated PLC parking controller monitors six LDR slot sensors and an IR sensor at the entrance gate to decide whether a waiting car may enter the car park.
   对应摘录：A
2. 句子 2：If at least one slot is free and the IR sensor detects a car at the entrance, the PLC opens the main gate and admits the vehicle; if all six slots are occupied, it keeps the gate closed and directs the driver to another parking area.
   对应摘录：A
3. 句子 3：After an entering car breaks the beam, a `3 seconds` timer is started, and once the timer done bit is set the ladder logic unlatches the gate output so that no following car can pass through immediately.
   对应摘录：B
4. 句子 4：A count-up counter tracks the occupied capacity up to six cars, turns on the Full light when the preset is reached, keeps the Spaces light on while capacity remains available, and uses the exit beam in count-down mode to release capacity again.
   对应摘录：B
5. 句子 5：When the authors found that a seventh car could still enter, they added a full-display condition to the first rung so that entry is locked out whenever the car park is already full.
   对应摘录：B
