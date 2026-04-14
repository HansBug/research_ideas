# Fault Tolerant Train Door Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把列车电动门的开门、关门、障碍回退、重复关门和停用退化链写成了带阈值与时间要求的完整 fault-tolerant controller。

## 条目 1: Fault-tolerant train-door open-close-retry controller

- 控制对象：轨道交通与铁路控制领域的电动列车车门开闭、故障回退与重试控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向电动列车门的闭环 fault-tolerant controller，用 PWM、方向信号、编码器、电流阈值和开闭到位传感器管理 normal open/close、obstruction reopen、retry close 和 out-of-service 退化处理。
- 判断：算。对象是真实列车门控制器，原文直接给出了正常门循环、时间目标、传感器条件、电流阈值和故障重试链，而不是只谈诊断或维护。

### 1. 原文摘录

#### 摘录 A

- 出处：第 40 页，`Project requirements`
> The door opening time should be 3.5 sec or less ... The door closing time should be between 3.5 and 4.0 sec ... Quick obstruction detection that, when detected, releases the door by a minimum of 50 mm.

#### 摘录 B

- 出处：第 48-49 页，`Controller functionality`
> The pulse width is changed from zero to approximately 87.5% where the motor works with the maximum desired speed assuring the required door opening time of approximately 3 seconds. The closing time is a bit longer and lasts 3.6 seconds with a pulse width of 75%.
>
> The controller uses encoder signals to always set itself to the same start conditions, which is the door fully open. When the power is on, the controller opens the door fully if the door is in any other position and then it becomes ready to use.

#### 摘录 C

- 出处：第 52 页，`Development stages`
> After the controller is powered up and the program starts, the door is fully open ... Then the program waits for the user buttons to be pressed. ... Once the button is pressed, the microcontroller sets the direction pin respectively and the door movement is started. When the door movement is finished, the program algorithm goes back to the main loop and awaits the next task.

#### 摘录 D

- 出处：第 53-54 页，`Fault tolerance implementation / Overcurrent monitoring and obstruction detection`
> Detectable faults: a) Over current monitoring and obstruction detection; b) Supply voltage changes; c) Pushbutton malfunction detection ... d) Increased friction detection while the door is in normal operation detected through a longer opening / closing time ... e) Door not fully closed or not fully open ... f) Door velocity changes; g) Motor optical encoder malfunction; h) PWM signal fault detection.
>
> There are two thresholds. The first value corresponds to approximately 2.4 A. ... If the result is in between the first and second (2.7 A) threshold value then a potential fault has been detected ... If the average value falls above the second threshold, then a potential obstruction or serious fault has been detected. In this case, the door will be reopened for a short distance (approximately 100 mm, defined in the program). The controller will perform further three attempts to close the door. If all attempts are unsuccessful, the controller will stop operation and report a fault on the LCD. The door is then out of service.

### 2. 基于原文整理后的自然语言描述

The train-door controller first normalizes the mechanism to a fully open reference position and then waits in its main loop for an open or close button request. When a request arrives, it drives the motor through a PWM-based close or open profile, with opening calibrated around `3 seconds` at about `87.5%` duty and closing around `3.6 seconds` at about `75%` duty, while continuously sampling encoder, infrared, current, and voltage feedback. The control logic therefore behaves as an EFSM whose transitions depend not only on direction commands and end-position sensors but also on measured door position, motion time, velocity deviations, and diagnostic flags such as pushbutton, encoder, PWM, or supply faults. During closing, current between about `2.4 A` and `2.7 A` is treated as an increased-friction warning, while current above the higher threshold is treated as obstruction or serious failure, causing the controller to reopen the door by about `100 mm` and retry closing up to three times. If the retries still fail, the controller reports the fault and takes the door out of service while keeping the degraded-safe outcome explicit.

### 3. 逐句溯源

1. 句子 1：The train-door controller first normalizes the mechanism to a fully open reference position and then waits in its main loop for an open or close button request.
   对应摘录：B, C
2. 句子 2：When a request arrives, it drives the motor through a PWM-based close or open profile, with opening calibrated around `3 seconds` at about `87.5%` duty and closing around `3.6 seconds` at about `75%` duty, while continuously sampling encoder, infrared, current, and voltage feedback.
   对应摘录：A, B
3. 句子 3：The control logic therefore behaves as an EFSM whose transitions depend not only on direction commands and end-position sensors but also on measured door position, motion time, velocity deviations, and diagnostic flags such as pushbutton, encoder, PWM, or supply faults.
   对应摘录：C, D
4. 句子 4：During closing, current between about `2.4 A` and `2.7 A` is treated as an increased-friction warning, while current above the higher threshold is treated as obstruction or serious failure, causing the controller to reopen the door by about `100 mm` and retry closing up to three times.
   对应摘录：D
5. 句子 5：If the retries still fail, the controller reports the fault and takes the door out of service while keeping the degraded-safe outcome explicit.
   对应摘录：D
