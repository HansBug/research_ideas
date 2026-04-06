# Efficiency Through Automation: A Single System for Multiple Railway Guard Posts - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：并行
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把“一套 PLC/HMI 同时监管五个道口”的检测、关闸、复开、车辆滞留报警和手动回退机制写得很完整，是 `🚆` 方向少见的并行监督样本。

## 条目 1: Five-post railway crossing HMI and buzzer supervisor

- 控制对象：轨道交通与铁路控制领域的五岗并行铁路道口监控与门控监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：并行
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个由 `PLC + HMI + infrared sensor + servo motor + buzzer` 组成的多道口铁路门控监督系统，用一套设备同时管理五个 guard post。
- 判断：算。对象是实际铁路道口控制器，原文明确写出列车检测、关闸/开闸、车辆滞留报警、五岗并行输出映射，以及传感器失效时的 HMI 手动关闭机制。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 26-39 行
> One System for Multiple Railway Crossing Guard Posts ... This tool is equipped with several main components, namely PLC, HMI, Infrared Sensor, and servo motor. The crossing gate is fully controlled by PLC and HMI as a monitoring system for all components in real-time ... the infrared sensor also works to give orders so that the Servo Motor as a crossing door can be immediately closed and opened ... equipped with an infrared sensor that functions to detect the presence of vehicles in the middle of the railroad crossing.

#### 摘录 B

- 出处：第 2 页，Introduction，`paper_content.txt` 第 101-105 行
> To solve this problem, we created PAK SUMA: Innovation of Railway Door Crossing, One Tool for Five Guard Posts ... we can run five guard stations with the tools we create. This doorstop can set the time so that it will automatically close if a train passes and open if the train does not pass. It also can alert guard officers and train users when there are still people standing in the middle of the train tracks after the gates are closed.

#### 摘录 C

- 出处：第 4-5 页，`System Flowchart` / `Wiring Diagram`，`paper_content.txt` 第 161-170, 182-205 行
> Once the microcontroller has processed the sensor's data, it will send it to the output when infrared sensor 1 detects a passing train. When the train approaches the railroad crossing, the servo motor rotates, closing the railroad crossing. It then rotates to reopen the railroad crossing. A manual mechanism is also included with this tool, allowing the train doorstop to be closed manually via an HMI if the sensor were to unexpectedly become defective.
>
> Infrared sensor 1 as a train detection component ... Infrared sensor 2 is used as a detector if there are vehicles that are still at the railroad crossing when the crossbar is closed ... Pins R1 to R5 drive the servo motors and pins R6 to R10 connect to the buzzer.

#### 摘录 D

- 出处：第 6-7 页，`Results and Discussion`，`paper_content.txt` 第 323-328, 359-376, 385-390 行
> The system will be in the standby position ... If the train detection sensor is not working, we can immediately turn on the manual railroad crossing system by directly pressing the push on the HMI screen.
>
> The railroad gate will be closed when the sensor detects a train ... and open when the sensor does not detect a train.
>
> The buzzer will activate when the railroad gate is closed and the sensor determines that there are still vehicles at the railroad crossing. Less than two seconds pass before the buzzer responds ... Test-2 ... There is a vehicle ... Closed ... 1.40 Second ... Buzzer on ... Test-4 ... 1.26 Second ... Buzzer on.

### 2. 基于原文整理后的自然语言描述

The railway-crossing supervisor uses one PLC/HMI installation to monitor and control five guard posts in parallel, with infrared train detection, servo-driven barriers, and buzzer outputs assigned across multiple crossing channels. For each post, `infrared sensor 1` detects an approaching train and causes the controller to rotate the servo so the railroad crossing closes, then reopens the crossing after the train has passed. `Infrared sensor 2` checks whether a vehicle is still inside the crossing while the crossbar is closed, and in that case the buzzer is activated to warn drivers and officers. The design also keeps a manual fallback path: if the train-detection sensor fails, the operator can close the crossing directly from the HMI screen. In the reported prototype tests, train detection closes or opens the crossbar as expected, and vehicle-detection tests trigger the buzzer within `1.40` seconds and `1.26` seconds only when a vehicle remains on a closed crossing.

### 3. 逐句溯源

1. 句子 1：The railway-crossing supervisor uses one PLC/HMI installation to monitor and control five guard posts in parallel, with infrared train detection, servo-driven barriers, and buzzer outputs assigned across multiple crossing channels.
   对应摘录：A, B, C
2. 句子 2：For each post, `infrared sensor 1` detects an approaching train and causes the controller to rotate the servo so the railroad crossing closes, then reopens the crossing after the train has passed.
   对应摘录：A, C, D
3. 句子 3：`Infrared sensor 2` checks whether a vehicle is still inside the crossing while the crossbar is closed, and in that case the buzzer is activated to warn drivers and officers.
   对应摘录：A, C, D
4. 句子 4：The design also keeps a manual fallback path: if the train-detection sensor fails, the operator can close the crossing directly from the HMI screen.
   对应摘录：C, D
5. 句子 5：In the reported prototype tests, train detection closes or opens the crossbar as expected, and vehicle-detection tests trigger the buzzer within `1.40` seconds and `1.26` seconds only when a vehicle remains on a closed crossing.
   对应摘录：D
