# PLC Driven Conveyor and Bottle Filling System - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把输送带定位、定时灌装、末端停瓶和启停锁存都写成了可追溯的 `PLC` 顺序控制链，是一条细节密度很高的瓶装灌装样本。

## 条目 1: Sensor-Timed Conveyor Bottle-Filling Sequence Controller

- 控制对象：工业自动化与离散制造领域的输送带瓶装定位与定时灌装顺序控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 `PLC` 驱动的瓶装输送与灌装控制器，用主锁存、两只光电传感器、输送带电机、水泵和定时器来完成启停、定位、灌装、输出和循环。
- 判断：算。对象是实际灌装生产单元顺序控制器，而不是普通 `PLC` 教学综述；原文直接给出了输入输出定义、各 rung 功能、七步算法和完整的工作流程说明。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1、4-5 页，Abstract 与 Section 3.1.1/3.1.2，`paper_content.txt` 第 16-22、158-186 行
> The system is programmed through ladder logic using WPL Soft, with a photoelectric sensor used to detect bottles on the conveyor and accurately initiate the filling process ... the PLC to control both bottle positioning and the filling mechanism ...
>
> Start Push Button ... initiates the process ... Stop Push Button ... halt both the conveyor and pump operations ...
>
> Photoelectric Sensor 1 ... detects the presence of a bottle as it moves into the filling position ... instructing it to stop the conveyor and activate the filling pump.
>
> Photoelectric Sensor 2 ... detects when a filled bottle reaches the end of the line ... sends a signal to the PLC to stop the conveyor until the next cycle begins ...

#### 摘录 B

- 出处：第 15-16 页，`Working of ladder diagram / Algorithm of ladder diagram`，`paper_content.txt` 第 521-559 行
> In Rung 1 ... Start push Button, stop push Button, and Master Coil ... The Master Coil is latched ...
>
> In Rung 2 ... When the master coil is activates in rung 1, which starts the conveyor motor in rung 2.
>
> In Rung 3 ... Whenever sensor 1 is activated which stops the conveyor, starts timer and water pump. Run the pump till the predetermined time.
>
> In Rung 4 ... When the sensor 2 activates ... conveyor stops.
>
> STEP 1 : Press the start Push Button.
> STEP 2 : Then the motor starts and the conveyor moves forward.
> STEP 3 : If the proximity sensor1 detects the presence of bottle, then the conveyor will stop and water pump activates.
> STEP 4 : Water pump fills the bottle for predetermined amount of time.
> STEP 5 : After fill of bottle water pump turns OFF and conveyor turn ON again.
> STEP 6: If the proximity sensor2 ... detects the presence of bottle, conveyor stops.
> STEP 7 : Repeat the procedure.

#### 摘录 C

- 出处：第 19 页，`Working of the project`，`paper_content.txt` 第 617-639 行
> The process begins when the Start Push Button is pressed, activating the Master Coil and latching the system on. The conveyor starts moving ...
>
> Sensor 1 ... detects the presence of a bottle ... the PLC ... triggers Timer 0. As soon as Sensor 1 is activated, the conveyor stops ...
>
> During this time, the Pump is activated ... Once Timer 0 completes ... stopping the pump ...
>
> After the bottle is filled, the conveyor restarts ... At the end of the conveyor, Sensor 2 detects the filled bottle. This sensor’s signal stops the conveyor ... The system will continue this automated cycle until the Stop Push Button is pressed ...

### 2. 基于原文整理后的自然语言描述

The bottle-filling unit is a PLC-driven sequential controller for a conveyor, filling station, and unloading point rather than a generic bottling setup description. When the start push button is pressed, a latched master coil enables the conveyor motor and moves empty bottles forward until `Sensor 1` detects a bottle at the filling position. That detection stops the conveyor, starts `Timer 0`, and activates the pump for the predefined filling interval; when the timer completes, the pump turns off and the conveyor restarts. The filled bottle then travels to the end of the line, where `Sensor 2` stops the conveyor for unloading, and the machine repeats the cycle until the stop push button breaks the master latch and halts the whole process.

### 3. 逐句溯源

1. 句子 1：The bottle-filling unit is a PLC-driven sequential controller for a conveyor, filling station, and unloading point rather than a generic bottling setup description.
   对应摘录：A
2. 句子 2：When the start push button is pressed, a latched master coil enables the conveyor motor and moves empty bottles forward until `Sensor 1` detects a bottle at the filling position.
   对应摘录：A, B, C
3. 句子 3：That detection stops the conveyor, starts `Timer 0`, and activates the pump for the predefined filling interval; when the timer completes, the pump turns off and the conveyor restarts.
   对应摘录：B, C
4. 句子 4：The filled bottle then travels to the end of the line, where `Sensor 2` stops the conveyor for unloading, and the machine repeats the cycle until the stop push button breaks the master latch and halts the whole process.
   对应摘录：A, B, C
