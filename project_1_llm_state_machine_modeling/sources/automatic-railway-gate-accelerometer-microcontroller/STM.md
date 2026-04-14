# Automatic Railway Gate System for Commuter Line Train Based on Sensor Accelerometer and Microcontroller - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把加速度阈值触发、SMS 命令下发、道口关闭、延时后重开这条控制链写得完整，而且给出了不同部署距离对应的显式延时。

## 条目 1: Accelerometer-triggered GSM railway crossing gate controller
- 控制对象：基于加速度传感器、GSM 通信和 Arduino 的铁路平交口自动门控系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是轨道交通与铁路控制领域的 level-crossing gate controller，用轨道振动阈值检测列车到来，再通过 GSM 命令驱动道口关闭并在延时后重开。
- 判断：算。对象是实际铁路道口门控系统，原文明确给出了两套系统的职责、阈值触发、消息序列、开闭门动作和 35/50/70 秒的显式定时。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-2 页，Abstract 与 Introduction，对系统结构的说明，行 20-38、96-105
> This study will design an automatic railroad gate closing system ... The Accelerometer sensor is system one as a vibration detector of a passing train, and Arduino UNO or system two will give commands or control the train gate to open and close automatically.
> ...
> The sensor threshold will be used as a set point on the microcontroller to output the servo motor, buzzer, and LED on the second system so the system can automatically open and close the railroad crossing gates.
> Communication to give commands between systems one and two is via GSM mode.

#### 摘录 B
- 出处：第 5-8 页，Section 2.3 与 3.1-3.2，对事件序列的说明，行 224-235、286-315
> The parameter or event as an indicator of success in this test is the time in seconds:
> (1) the commuter railroad gate will close,
> (2) the commuter railroad gate will close correctly,
> (3) the commuter line train crosses,
> (4) the commuter line train has finished passing, and
> (5) the gate of the commuter train cross will open.
> ...
> If the vibration value has reached a certain point (set point), Arduino UNO will give a command to SIM800L ... to send a message to SIM800L on the system 2.
> After SIM800L sends the first command message (closes the gate), then the system will delay some time to send the second command message, which is to open the automatic crossbar and turn off the LED and Buzzer.
> ...
> SIM800L on system two will receive a message ... and forward it to Arduino UNO.
> Arduino UNO ... will give the Stepper Motor, LED, and Buzzer commands to light up, and the bar will automatically close.
> Then the bar automatically opens if SIM800L has received the second command message.

#### 摘录 C
- 出处：第 8-9 页，Section 3.3.2，对阈值和延时的说明，行 344-360
> when the ADXL345 sensor reading reaches more than 13 m/s2, SIM800L communicates directly with the automatic bar (system 2) by sending the message "LIHT ON", and then the doorstop will automatically close
> ...
> After the "LIGHT ON" command is sent, Arduino will delay 35 seconds for testing the 200m sensor distance from the automatic bar, 50 seconds delay for testing the sensor distance 450m from the automatic bar, and 70 seconds delay for testing the 650m sensor distance from the automatic bar.
> After a delay of the specified time the SIM800L will give a message again, but this time to open the automatic bar with the message "LIGHT OFF".

#### 摘录 D
- 出处：第 1 页，Abstract，对测试结果与推荐距离的说明，行 29-38
> Variations in time intervals of 200m, 450m, and 650m were carried out to obtain the time difference between the closing of the train gate completely and the time when the train passed at the gate crossing with standard time.
> ...
> at a range of 650 meters for 36.7 seconds the value of g is 10.02 m/s2.
> The results of the study recommend placement with a distance between systems of 650 meters.

### 2. 基于原文整理后的自然语言描述

The railway crossing controller is split into two coordinated subsystems: system 1 uses an accelerometer to detect train-induced rail vibration, and system 2 uses Arduino, GSM, a stepper motor, an LED, and a buzzer to operate the gate. When the vibration value reaches the configured set point, system 1 sends a first GSM message to system 2 so that the gate closes and the warning LED and buzzer are activated. After that first command, the controller waits for a deployment-dependent delay and then sends a second message that turns the LED and buzzer off and reopens the crossbar. The paper makes the timing explicit: after the `LIGHT ON` close-gate command, the reopen delay is `35 s` for `200 m`, `50 s` for `450 m`, and `70 s` for `650 m`, and the close command is triggered once the ADXL345 reading exceeds `13 m/s2`. Field testing evaluates the ordered event chain of gate close, correct gate close, train crossing, train departure, and gate reopening, and recommends the `650 m` placement because it gives the closest standard time gap.

### 3. 逐句溯源

1. 句子 1：The railway crossing controller is split into two coordinated subsystems: system 1 uses an accelerometer to detect train-induced rail vibration, and system 2 uses Arduino, GSM, a stepper motor, an LED, and a buzzer to operate the gate.
   对应摘录：A, B
2. 句子 2：When the vibration value reaches the configured set point, system 1 sends a first GSM message to system 2 so that the gate closes and the warning LED and buzzer are activated.
   对应摘录：A, B, C
3. 句子 3：After that first command, the controller waits for a deployment-dependent delay and then sends a second message that turns the LED and buzzer off and reopens the crossbar.
   对应摘录：B, C
4. 句子 4：The paper makes the timing explicit: after the `LIGHT ON` close-gate command, the reopen delay is `35 s` for `200 m`, `50 s` for `450 m`, and `70 s` for `650 m`, and the close command is triggered once the ADXL345 reading exceeds `13 m/s2`.
   对应摘录：C
5. 句子 5：Field testing evaluates the ordered event chain of gate close, correct gate close, train crossing, train departure, and gate reopening, and recommends the `650 m` placement because it gives the closest standard time gap.
   对应摘录：B, D
