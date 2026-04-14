# Model Of Metal Sorting Conveyor System Using Siemens S7-1200 PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把金属分拣输送线的传送、感应、停带、顶出和定时复位过程写成了 PLC+定时器控制链，能形成双 A 的离散制造样本。

## 条目 1: Inductive-Sensed Metal-Rejection Conveyor Supervisor

- 控制对象：工业自动化与离散制造领域的金属分拣输送带与电磁顶出控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Siemens `S7-1200 PLC` 的金属分拣输送线控制器，使用电感式接近传感器识别金属，并通过电磁推杆/翻板把目标物从主输送线上剔除。
- 判断：算。对象是实际工业分拣控制系统，原文给出传感器、输送机、电磁执行器、PLC 程序和定时器控制的完整链路。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 10-15 行
> This research therefore designed and developed an automated sorting metal object of a conveyor belt.
>
> The developed automated sorting machine is able to incorporate flexibility and separate species of metal objects ... as defined by the regulation of the Programmable Logic Controllers (PLC) with an inductive proximity sensor to detect a value range of objects.
>
> The result obtained shows that steel/metal is sorted into correct position with time of 10s.

#### 摘录 B

- 出处：第 1 页，Introduction，`paper_content.txt` 第 33-50 行
> Automation System for sorting metal objects conveyor is developed in Programmable Logic Controller PLC.
>
> The project mainly focuses on sorting different metallic objects which is available in inductive sensor, solenoid and DC geared motors interfaced with Programmable Logic Controller (PLC).
>
> A DC motor is used for the flipper which is used for pushing the object from one conveyor to other conveyor line and also the rejection bin.
>
> The sensor in the middle of the conveyor lines will segregate the objects and send the signal to the PLC ...

#### 摘录 C

- 出处：第 3-4 页，`HARDWARE IMPLEMENTATION / SOFTWARE DEVELOPMENT`，`paper_content.txt` 第 291-329 行
> the main is S7-1200 PLC and its acts the controller in the system. The conveyor motor is running until the sensor detects the metal. The sensor is inductive proximity sensor. When the sensor detected the metal, the electrical solenoid is reject it from the conveyor.
>
> the program can be start by pressing the start button ... the pilot light is turn on that means the system is starting. And conveyor is running.
>
> When the sensor detects the metal object, the conveyor is stopped. And the solenoid is energized by PLC. The arm from solenoid is extended to remove the metal from the conveyor line. After that, the conveyor is restarting.
>
> the operation time of solenoid is controlled by the timer. The energized time and DE energized time of the solenoid is set by two timer ...

### 2. 基于原文整理后的自然语言描述

The sorting controller is built around a Siemens `S7-1200 PLC` and an inductive proximity sensor that distinguishes metal objects on a conveyor line. Under normal running conditions the conveyor keeps moving workpieces such as bottles, small boxes, or packages toward the sensing point, and the PLC waits for the metal-detection signal coming from the middle of the line. Once metal is detected, the PLC stops the conveyor, energizes the solenoid-driven rejection mechanism or flipper, and extends the actuator to remove the object into the rejection path before restarting the conveyor. The paper also states that the solenoid’s energized and de-energized durations are governed by two timers, so the rejection cycle is not only event-driven but also locally timed.

### 3. 逐句溯源

1. 句子 1：The sorting controller is built around a Siemens `S7-1200 PLC` and an inductive proximity sensor that distinguishes metal objects on a conveyor line.
   对应摘录：A, B, C
2. 句子 2：Under normal running conditions the conveyor keeps moving workpieces such as bottles, small boxes, or packages toward the sensing point, and the PLC waits for the metal-detection signal coming from the middle of the line.
   对应摘录：B, C
3. 句子 3：Once metal is detected, the PLC stops the conveyor, energizes the solenoid-driven rejection mechanism or flipper, and extends the actuator to remove the object into the rejection path before restarting the conveyor.
   对应摘录：B, C
4. 句子 4：The paper also states that the solenoid’s energized and de-energized durations are governed by two timers, so the rejection cycle is not only event-driven but also locally timed.
   对应摘录：A, C
