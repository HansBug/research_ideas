# Automatic Washing Machine Control System Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：2
- 简要判断：论文把全自动洗衣机的进水、洗涤、排水、漂洗和脱水顺序写得较完整，可以拆成两个高质量的机电控制逻辑样本。

## 条目 1: Water-Level-Regulated Filling Sequence
- 控制对象：全自动洗衣机的进水控制逻辑
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是家电控制场景下的洗衣机 PLC 控制器，用于根据设定水位自动开关进水电磁阀并完成进水阶段。
- 判断：算。对象是实际洗衣机控制系统，原文明确给出了水位检测、阀门开启和到设定值后关闭的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The main working principle of washing machine，行 81-90
> drying time and water level parameters and press the start button. At this time, the water level sensor detects whether there is water in the barrel or whether the water level meets the standard. If there is no water or the water level does not meet the standard, it will be fed back to the control. The system control system outputs the signal to the water injection solenoid valve. At this time, the water injection solenoid valve opens and water injection. As the water level rises. When the user's set value is reached, the water level sensor is transmitted to the control system again. The control system outputs the signal, closes the water injection solenoid valve, and completes the water injection process.

#### 摘录 B
- 出处：第 3-4 页，PLC program，行 183-194
> use the mov command to design the water inlet time for high, medium and low water levels, respectively: low water level 2 minutes; medium water level 3 minutes; high water level 4 minutes. ... Before pressing the start button (X0), you need to select one. Similarly, set the dehydration time, and use the buttons ... to control dehydration for 5 minutes, dehydration for 10 minutes and dehydration for 15 minutes respectively.

### 2. 基于原文整理后的自然语言描述

Before starting the washing machine, the user selects one of the low, medium, or high water-level settings, which the PLC program maps to different inlet durations. After the start button is pressed, the PLC checks through the water-level sensor whether the barrel already contains enough water. If the sensed level is below the selected standard, the controller opens the water-injection solenoid valve and starts filling. When the sensed water level reaches the user's set value, the controller closes the solenoid valve and completes the filling process.

### 3. 逐句溯源

1. 句子 1：Before starting the washing machine, the user selects one of the low, medium, or high water-level settings, which the PLC program maps to different inlet durations.
   对应摘录：B
2. 句子 2：After the start button is pressed, the PLC checks through the water-level sensor whether the barrel already contains enough water.
   对应摘录：A
3. 句子 3：If the sensed level is below the selected standard, the controller opens the water-injection solenoid valve and starts filling.
   对应摘录：A
4. 句子 4：When the sensed water level reaches the user's set value, the controller closes the solenoid valve and completes the filling process.
   对应摘录：A

## 条目 2: Wash-Rinse-Dehydrate Cycle
- 控制对象：全自动洗衣机的洗涤、排水、漂洗和脱水顺序控制
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是全自动洗衣机的程序循环控制器，用于按固定顺序驱动电机正反转、排水、漂洗和高速脱水。
- 判断：算。对象是实际洗衣机控制系统，原文直接给出了 procedure-driven 的 forward/stop/reverse、drainage、rinsing 和 dehydration 链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The main working principle of washing machine，行 91-105
> Then, the control system then supplies power to the motor drive circuit, and the motor starts to operate, and according to the different procedures, it rotates forward, stops, reverses and cycles in sequence according to a certain time pattern. ... After the number of washes set by the user is completed, the output signal of the control system is provided to the leakage solenoid valve, and the drain solenoid valve is opened to start the drainage process. After the drainage is completed, it enters the rinsing mode. After meeting the setter's rinsing mode, the water level controller gives the control system a signal, and then the control system controls the motor to rotate at high speed in one direction and starts the dehydration process. After the dehydration time is completed, the control system gives a signal and the drain solenoid valve is closed.

#### 摘录 B
- 出处：第 3-5 页，PLC program / Water inlet procedure，行 191-214
> use the buttons X10, X11, and X13 to control dehydration for 5 minutes, dehydration for 10 minutes and dehydration for 15 minutes respectively. Then use the INC command to set the number of washings and rinsing times. ... Press the stop button (X1) to pause the washing machine. Pressing the full stop button (X2) can terminate the washing machine. ... after the water inlet is completed according to the requirements, the motor will rotate 30S forward, 3S pause, and continue to reverse 30S, so that the washing machine can complete the first washing process.

### 2. 基于原文整理后的自然语言描述

After filling is completed, the controller powers the motor-drive circuit and executes the washing procedure by rotating the motor forward for 30 seconds, pausing for 3 seconds, reversing for 30 seconds, and repeating the sequence according to the programmed count. The user sets the washing count, rinsing count, and dehydration duration through dedicated buttons, while stop and full-stop buttons respectively pause or terminate the process. Once the programmed number of washes has been completed, the controller opens the drain solenoid valve and starts the drainage process before entering rinsing mode. After the rinsing condition is satisfied, the controller drives the motor at high speed in one direction for the selected dehydration interval and then closes the drain valve; when the whole program is finished, the buzzer sounds and the power is cut off.

### 3. 逐句溯源

1. 句子 1：After filling is completed, the controller powers the motor-drive circuit and executes the washing procedure by rotating the motor forward for 30 seconds, pausing for 3 seconds, reversing for 30 seconds, and repeating the sequence according to the programmed count.
   对应摘录：A, B
2. 句子 2：The user sets the washing count, rinsing count, and dehydration duration through dedicated buttons, while stop and full-stop buttons respectively pause or terminate the process.
   对应摘录：B
3. 句子 3：Once the programmed number of washes has been completed, the controller opens the drain solenoid valve and starts the drainage process before entering rinsing mode.
   对应摘录：A
4. 句子 4：After the rinsing condition is satisfied, the controller drives the motor at high speed in one direction for the selected dehydration interval and then closes the drain valve; when the whole program is finished, the buzzer sounds and the power is cut off.
   对应摘录：A, B
