# Automatic Railway Gate Control System Using 8051micro Controller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把两侧 `IR` 传感器、`5 seconds` 预警延时、蜂鸣器和电机正反转门控写成了清楚的铁路平交口控制链，足以形成 `EFSM + T1` 双 A 样本。

## 条目 1: IR-Triggered 5-Second Railway Gate Closure Controller
- 控制对象：轨道交通与铁路控制领域的 IR 传感器触发式平交口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个用 `8051` 微控制器实现的无人值守铁路平交口控制器，通过前后侧 `IR` 传感器驱动蜂鸣预警、栅栏关闭、列车通过保持和通过后重开门。
- 判断：算。对象是实际 railway gate controller，不是器件综述；原文给出了传感器布置、`5 seconds` 延时、门机方向切换以及代码级传感-电机映射。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 14-28 行
> The objective of this paper is to provide an automatic railway gate at a level crossing replacing the gates operated by the gatekeeper. ... By employing the automatic railway gate control at the level crossing the arrival of the train is detected by the sensor placed near to the gate. Hence, the time for which it is closed is less compared to the manually operated gates ... This type of gates can be employed in an unmanned level crossing where the chances of accidents are higher and reliable operation is required.

#### 摘录 B
- 出处：第 2 页，Introduction，`paper_content.txt` 第 62-74 行
> Present work is designed using 8051 microcontroller to avoid railway accidents happening at unattended railway gates ... We have Automatic Railway Gate Control System considered 5 seconds for this paper. Sensors are fixed at 1km on both sides of the gate. We call the sensor along the train direction as ‘foreside sensor’ and the other as ‘after side sensor’. When foreside receiver gets activated, the gate motor is turned on in one direction and the gate is closed and stays closed until the train crosses the gate and reaches aft side sensors. When aft side receiver gets activated motor turns in opposite direction and gate opens and motor stops. Buzzer will immediately sound at the fore side receiver activation and gate will close after 5 seconds ...

#### 摘录 C
- 出处：第 5-6 页，`Complier And Source Code Used / Hardware Circuit`，`paper_content.txt` 第 141-205 行
> Microcontrollers will combine other devices such as ... A timer module to allow the microcontroller to perform tasks for certain time periods ... while (1) { if (led1==1){ drive1=1; drive2=0; delay (100); drive1=0; drive2=0; loop1: if (led2!=0x1) goto loop1; drive1=0; drive2=1; delay (100); drive1=0; drive2=0; }}} ... If the sensor I detects the arrival of the train, microcontroller starts the motor with the help of motor driver in order to close the gate. The gate remains closed as the train passes the crossing. When the train crosses the gate and reaches second sensor. It detects the train and the microcontroller will open the gate.

### 2. 基于原文整理后的自然语言描述

The level-crossing controller watches two `IR` sensor positions around the gate and uses them as the main guards for barrier motion. When the foreside sensor detects an approaching train, the controller activates the buzzer immediately, waits for the configured warning interval, and then drives the motor in the closing direction so the gate remains shut while the train occupies the crossing. The barrier is reopened only after the aft-side sensor is triggered, at which point the motor direction is reversed and then stopped again. The implementation section reinforces the same chain in code by mapping the first sensor to forward drive, waiting in a loop for the second sensor, and then commanding backward drive. Because the paper makes the sensor placement, `5 seconds` warning delay, gate-close hold condition, and reopen trigger all explicit, this is a strong `EFSM + T1` railway-gate sample.

### 3. 逐句溯源

1. 句子 1：The level-crossing controller watches two `IR` sensor positions around the gate and uses them as the main guards for barrier motion.
   对应摘录：A, B
2. 句子 2：When the foreside sensor detects an approaching train, the controller activates the buzzer immediately, waits for the configured warning interval, and then drives the motor in the closing direction so the gate remains shut while the train occupies the crossing.
   对应摘录：B, C
3. 句子 3：The barrier is reopened only after the aft-side sensor is triggered, at which point the motor direction is reversed and then stopped again.
   对应摘录：B, C
4. 句子 4：The implementation section reinforces the same chain in code by mapping the first sensor to forward drive, waiting in a loop for the second sensor, and then commanding backward drive.
   对应摘录：C
5. 句子 5：Because the paper makes the sensor placement, `5 seconds` warning delay, gate-close hold condition, and reopen trigger all explicit, this is a strong `EFSM + T1` railway-gate sample.
   对应摘录：A, B, C
