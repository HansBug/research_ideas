# A Control System of Elevators by Using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文直接描述了双梯分区响应、到呼叫层开门、计时关门和继续去目标层的顺序，结构很干净。

## 条目 1: Selective Dual-Elevator Dispatch with Timed Door Operation
- 控制对象：双电梯五层选择性调度控制系统

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的双电梯 PLC 调度系统，用于按楼层分区响应呼叫、到层后开关门，并继续前往乘客目标层。
- 判断：算。对象是实际电梯控制系统，原文明确给出了楼层分配、传感检测、计时开门和继续运行顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 12-20 行
> PLC is used as a controller for an elevator system that has two elevators with five floors. The PLC will control vertical movement of the two elevators either moving up or down simultaneously with only one PLC. The PLC also control opened and closed door process after the elevator had reached each level. The automation of this elevator process consists in providing technological means for its selective operation and control.

#### 摘录 B
- 出处：第 4 页，Section 2.4 Sequence of the Flowchart，`paper_content.txt` 第 297-309 行
> When the keypad of each level is pressed, one of the elevators responds. Elevator A responds to keypad pressed only at level 1, 2 and 3. Elevator B responds to keypad pressed only at level 4 and 5. Then each elevator will go to the called level and performed opened door operation. After the timer for the passengers to enter the elevator is off, the elevator will closed the door and continue to go to desired level and performed opened and closed door operation again.

### 2. 基于原文整理后的自然语言描述

The PLC controls two elevators serving five floors and manages both the vertical movement and the door-opening/closing process after each arrival. A call from levels 1 to 3 is assigned to Elevator A, while a call from levels 4 to 5 is assigned to Elevator B as part of the selective operation scheme. After the selected elevator reaches the called level, it opens the door, waits for the timed passenger-entry interval to expire, closes the door, and then continues to the passenger's desired level where the door operation is repeated.

### 3. 逐句溯源

1. 句子 1：The PLC controls two elevators serving five floors and manages both the vertical movement and the door-opening/closing process after each arrival.
   对应摘录：A
2. 句子 2：A call from levels 1 to 3 is assigned to Elevator A, while a call from levels 4 to 5 is assigned to Elevator B as part of the selective operation scheme.
   对应摘录：B
3. 句子 3：After the selected elevator reaches the called level, it opens the door, waits for the timed passenger-entry interval to expire, closes the door, and then continues to the passenger's desired level where the door operation is repeated.
   对应摘录：B
