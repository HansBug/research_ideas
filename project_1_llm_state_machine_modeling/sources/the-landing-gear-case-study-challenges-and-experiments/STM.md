# The landing gear case study: challenges and experiments - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对起落架伸出/收回基本序列、飞行员手柄、指示灯和模拟开关行为都有清晰描述。

## 条目 1: Extend-retract sequencing and cockpit indication in the landing gear system
- 控制对象：飞机起落架及其数字控制软件

### 0. 条目识别与判定

- 一句话说明：这是航空起落架控制领域的 landing gear system，用于根据飞行员 Up/Down handle 指令协调门、起落架、液压与指示灯的伸放/回收过程。
- 判断：算。对象是实际飞机起落架控制系统，原文直接给出了 landing/retraction sequence、pilot interface、传感/灯光反馈以及模拟开关时序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The landing gear case study: brief overview，对基本 sequence 与手柄/灯光的说明，行 87-105
> a basic landing sequence are: (1) open the doors of the landing gear boxes, (2) extend the landing gears and (3) close the doors. Similarly, after taking off, the corresponding basic retraction sequence to be performed are: (1) open the doors, (2) retract the landing gears and (3) close the doors. From ... the pilot can interrupt each sequence at any time and at any point to start the other sequence.
>
> of gears, an Up/Down handle is provided to the pilot. When the handle is switched to “Up” the retracting landing gear sequence is executed, when the handle is switched to “Down” the extending landing gear sequence is executed.
>
> Three lights inform the pilot of the current position of the gears and the doors, and of the current health state of the system and its equipments: (1) one green light “gears are locked down”, (2) one orange light “gears manoeuvring”, (3) one red light “landing gear system failure”.

#### 摘录 B
- 出处：第 4-5 页，Analogical switch，对开关闭合与重新打开时序的说明，行 213-218
> The switch is closed each time the “Up/Down” handle is moved by the pilot, and it remains closed for 20 s. After this duration, the switch automatically becomes open. Because of inertial reasons, the transition from the two states closed and open takes a given amount of time: (1) 0.8 s from open to closed, and (2) 1.2 s from closed to open. In the closed position, the switch transmits the electrical order from the digital part to the general electro-valve.

### 2. 基于原文整理后的自然语言描述

The landing gear system executes a basic extension sequence of opening the doors, extending the gears, and closing the doors, and after takeoff it executes the corresponding retraction sequence of opening the doors, retracting the gears, and closing the doors. The pilot commands these sequences with an Up/Down handle, where switching to Up triggers the retracting sequence and switching to Down triggers the extending sequence, and either sequence may be interrupted to start the opposite one. The cockpit feedback indicates whether the gears are locked down, maneuvering, or in system failure, and each handle movement closes the analogical switch for a limited period so that the digital part can transmit the electrical order to the general electro-valve.

### 3. 逐句溯源

1. 句子 1：The landing gear system executes a basic extension sequence of opening the doors, extending the gears, and closing the doors, and after takeoff it executes the corresponding retraction sequence of opening the doors, retracting the gears, and closing the doors.
   对应摘录：A
2. 句子 2：The pilot commands these sequences with an Up/Down handle, where switching to Up triggers the retracting sequence and switching to Down triggers the extending sequence, and either sequence may be interrupted to start the opposite one.
   对应摘录：A
3. 句子 3：The cockpit feedback indicates whether the gears are locked down, maneuvering, or in system failure, and each handle movement closes the analogical switch for a limited period so that the digital part can transmit the electrical order to the general electro-valve.
   对应摘录：A, B
