# Automatic Washing Machine Control System Based on PLC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：2
- 简要判断：论文把全自动洗衣机的进水、洗涤、排水、漂洗和脱水顺序写得较完整，可以拆成两个高质量的机电控制逻辑样本。

## 条目 1: Water-Level-Regulated Filling Sequence
- 控制对象：全自动洗衣机的进水控制逻辑

### 0. 条目识别与判定
- 一句话说明：这是家电控制场景下的洗衣机 PLC 控制器，用于根据设定水位自动开关进水电磁阀并完成进水阶段。
- 判断：算。对象是实际洗衣机控制系统，原文明确给出了水位检测、阀门开启和到设定值后关闭的顺序。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The main working principle of washing machine，行 81-90
> drying time and water level parameters and press the start button. At this time, the water level sensor detects whether there is water in the barrel or whether the water level meets the standard. If there is no water or the water level does not meet the standard, it will be fed back to the control. The system control system outputs the signal to the water injection solenoid valve. At this time, the water injection solenoid valve opens and water injection. As the water level rises. When the user's set value is reached, the water level sensor is transmitted to the control system again. The control system outputs the signal, closes the water injection solenoid valve, and completes the water injection process.

### 2. 基于原文整理后的自然语言描述

After the user sets the drying time and water-level parameters and presses the start button, the PLC checks whether the barrel already contains enough water. If the water level does not meet the standard, the controller opens the water-injection solenoid valve and starts filling. When the sensed water level reaches the user's set value, the controller closes the solenoid valve and completes the filling process.

### 3. 逐句溯源

1. 句子 1：After the user sets the drying time and water-level parameters and presses the start button, the PLC checks whether the barrel already contains enough water.
   对应摘录：A
2. 句子 2：If the water level does not meet the standard, the controller opens the water-injection solenoid valve and starts filling.
   对应摘录：A
3. 句子 3：When the sensed water level reaches the user's set value, the controller closes the solenoid valve and completes the filling process.
   对应摘录：A

## 条目 2: Wash-Rinse-Dehydrate Cycle
- 控制对象：全自动洗衣机的洗涤、排水、漂洗和脱水顺序控制

### 0. 条目识别与判定
- 一句话说明：这是全自动洗衣机的程序循环控制器，用于按固定顺序驱动电机正反转、排水、漂洗和高速脱水。
- 判断：算。对象是实际洗衣机控制系统，原文直接给出了 procedure-driven 的 forward/stop/reverse、drainage、rinsing 和 dehydration 链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，The main working principle of washing machine，行 91-105
> Then, the control system then supplies power to the motor drive circuit, and the motor starts to operate, and according to the different procedures, it rotates forward, stops, reverses and cycles in sequence according to a certain time pattern. ... After the number of washes set by the user is completed, the output signal of the control system is provided to the leakage solenoid valve, and the drain solenoid valve is opened to start the drainage process. After the drainage is completed, it enters the rinsing mode. After meeting the setter's rinsing mode, the water level controller gives the control system a signal, and then the control system controls the motor to rotate at high speed in one direction and starts the dehydration process. After the dehydration time is completed, the control system gives a signal and the drain solenoid valve is closed.

### 2. 基于原文整理后的自然语言描述

After filling is completed, the controller powers the motor-drive circuit and executes the washing procedure by rotating the motor forward, stopping it, reversing it, and repeating the sequence according to a timed pattern. Once the programmed number of washes has been completed, the controller opens the drain solenoid valve and starts the drainage process. After drainage, the machine enters rinsing mode, and once the rinsing condition is satisfied, the controller drives the motor at high speed in one direction for dehydration before closing the drain valve at the end of the dehydration time.

### 3. 逐句溯源

1. 句子 1：After filling is completed, the controller powers the motor-drive circuit and executes the washing procedure by rotating the motor forward, stopping it, reversing it, and repeating the sequence according to a timed pattern.
   对应摘录：A
2. 句子 2：Once the programmed number of washes has been completed, the controller opens the drain solenoid valve and starts the drainage process.
   对应摘录：A
3. 句子 3：After drainage, the machine enters rinsing mode, and once the rinsing condition is satisfied, the controller drives the motor at high speed in one direction for dehydration before closing the drain valve at the end of the dehydration time.
   对应摘录：A
