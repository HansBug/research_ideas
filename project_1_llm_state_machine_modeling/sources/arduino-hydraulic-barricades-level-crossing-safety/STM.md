# Application of Arduino-based Control System Hydraulic Barricades to Improve Safety at Level Crossing Safety - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把列车检测、栏门同步、`0°/30°` 伺服位姿与 `2 s` 动作时间写得清楚，可形成一条到发检测驱动的道口防闯入控制链。

## 条目 1: Train-Detection Barricade Deployment Synchronized with Gate Closure

- 控制对象：铁路平交道口的 Arduino 栏门与液压路障联动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个平交道口安全控制器，用红外传感器检测列车接近，并联动道口门栏与液压路障的升起/落下动作来阻止车辆闯入。
- 判断：算。对象是实际铁路道口子系统，原文不仅给出“检测到列车 -> 关门/升障”的控制链，还给出 `0° / 30°` 位姿和 `2 s` 同步动作时间。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，`Abstract / Introduction`，`paper_content.txt` 第 20-35 行、第 95-101 行
> This study aims to develop a servo-driven barricade system using an Arduino Uno microcontroller and infrared sensors to enhance safety at level crossings by preventing vehicle crossings during train passages ... Findings indicate that the system consistently detected train arrivals with 100% sensor accuracy and actuated barricades within 2 seconds.
>
> we want to solve these problems by creating an automatic barricade that is connected to the level crossing gate ... when the train is read on the infrared sensor ... we created an Arduino-based automatic barricade to improve security at level crossings.

#### 摘录 B

- 出处：第 4-6 页，`Methods / Results`，`paper_content.txt` 第 164-170 行、第 236-249 行
> Programming was done in Arduino C++ to manage sensor readings, servo motion (tilting from 0° to 30°), LED signals, and a 2-second delay to synchronize with crossing gates.
>
> Table 2. Servo Motor Test Results ... Open 30° ... Close 0° ... The SG90 servo motor responded accurately to commands, moving the barricade to a 30° angle when open and returning to 0° when closed ... with an average transition time of 2 seconds between positions.

#### 摘录 C

- 出处：第 5-7 页，`Results`，`paper_content.txt` 第 216-224 行、第 287-294 行
> when the sensor detected the presence of a train, the gate closed and the automatic barricade lifted to block the vehicle.
>
> with sensors placed 10 cm before the guard post and station ... 30 cycles of testing with a model train, achieving 98% reliability in triggering gate closure and barricade lift ... The miniature testing validated the system’s ability to coordinate gate and barricade movements.

### 2. 基于原文整理后的自然语言描述

The level-crossing controller monitors train arrival through infrared sensors and uses the Arduino as the central unit for coordinating both the conventional gate and the additional hydraulic barricade. Once a train is detected, the control logic closes the crossing gate and drives the SG90 actuator so the barricade lifts from its `0°` resting position toward the `30°` blocking position. The movement is explicitly synchronized with the crossing gate through a programmed `2 s` delay or transition window. In the miniature setup, the same sensor-triggered logic is reused with sensors placed ahead of the guard post and station so that gate closure and barricade deployment occur together before vehicles can enter the protected zone.

### 3. 逐句溯源

1. 句子 1：The level-crossing controller monitors train arrival through infrared sensors and uses the Arduino as the central unit for coordinating both the conventional gate and the additional hydraulic barricade.
   对应摘录：A, C
2. 句子 2：Once a train is detected, the control logic closes the crossing gate and drives the SG90 actuator so the barricade lifts from its `0°` resting position toward the `30°` blocking position.
   对应摘录：B, C
3. 句子 3：The movement is explicitly synchronized with the crossing gate through a programmed `2 s` delay or transition window.
   对应摘录：A, B
4. 句子 4：In the miniature setup, the same sensor-triggered logic is reused with sensors placed ahead of the guard post and station so that gate closure and barricade deployment occur together before vehicles can enter the protected zone.
   对应摘录：C
