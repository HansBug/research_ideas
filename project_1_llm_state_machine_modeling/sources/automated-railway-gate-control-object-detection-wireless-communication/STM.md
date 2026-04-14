# Automated Railway Gate Control and Object Detection using Wireless Communication - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把无人值守平交口写成“RF 来车关门 / IR 障碍延时判定 / XBee 停车信号 / RF 离车开门”的完整控制链，输入、动作和联动对象都够具体。

## 条目 1: Obstacle-Triggered Railway Gate and Signal-Stop Controller
- 控制对象：无人值守铁路平交口的自动门控与障碍告警控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向无人值守 level crossing 的铁路门控控制器，用 RF 发射器识别列车前后端、用 IR 传感器和延时器判定轨道障碍，并通过 `XBee` 联动铁路信号灯停车告警。
- 判断：算。对象是明确的 railway crossing controller，原文给出了 gate side 与 signal side 两个协同控制环节，而不是只停留在器件框图。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 10-16 行
> In this paper, our aim is to implement automatic railway gate control system at unmanned railway level crossings to prevent accidents ... The system also checks for any obstacle that gets stuck in the track and communicates with the railway signal to change it appropriately to alert and stop the train.

#### 摘录 B
- 出处：第 2 页，`Proposed Method`，`paper_content.txt` 第 58-63 行
> In proposed method, the ultrasonic sensors and GSM technology are replaced with RF transmitter/receiver pair to identify the approaching train, IR sensors for obstacle detection and XBee transceivers are employed for communicating with the railway signal.

#### 摘录 C
- 出处：第 5 页，`Results and Discussions`，`paper_content.txt` 第 442-481 行
> The RF receiver 1 fixed at the railway gate detects the RF transmitter signal code fixed in the train’s front end ... it sends a control signal to the DC motor driver through the microcontroller and closes the gate. After closing the gate, the Object detecting IR transceiver circuit is switched ON and starts checking for any obstacle (vehicle) on the track. The immovable obstacle is identified by setting a delay timer to the IR detector. If any immovable obstacle is present on the track, the IR sensor generates a voltage ... and it activates the XBee transceiver at the gate.
>
> The XBee transceiver 1 fixed at the gate communicates ... to the railway signal ... receives the data and changes the signal (LED) and alerts the train to stop.
>
> If there is no obstacle, the train passes through the level crossing. The RF transmitter 2 attached with the back end of the train sends a signal code to the RF receiver fixed with the gate ... the microcontroller unit at the gate sends control signal to the DC motor driver and the gate opens.

### 2. 基于原文整理后的自然语言描述

The unmanned railway-crossing controller starts by listening for the front-end RF code of an approaching train and, once it is received, commands the gate motor driver through the microcontroller to close the barrier. After the barrier is closed, the gate-side controller switches on the obstacle-detection IR transceiver and uses a delay-timer check to distinguish a stuck or immovable object from transient interruption on the track. If that obstacle branch is activated, the gate-side `XBee` transmitter sends the hazard message to the signal-side controller, which changes the railway signal indication and alerts the train to stop. If no obstacle is present, the train is allowed to pass normally, and when the rear-end RF code is later received, the controller reverses the motor action and reopens the gate. This gives the paper a clear `EFSM + T1` structure because gate motion depends not only on train position events but also on an obstacle branch guarded by timed persistence and wireless inter-controller communication.

### 3. 逐句溯源

1. 句子 1：The unmanned railway-crossing controller starts by listening for the front-end RF code of an approaching train and, once it is received, commands the gate motor driver through the microcontroller to close the barrier.
   对应摘录：A, B, C
2. 句子 2：After the barrier is closed, the gate-side controller switches on the obstacle-detection IR transceiver and uses a delay-timer check to distinguish a stuck or immovable object from transient interruption on the track.
   对应摘录：C
3. 句子 3：If that obstacle branch is activated, the gate-side `XBee` transmitter sends the hazard message to the signal-side controller, which changes the railway signal indication and alerts the train to stop.
   对应摘录：A, B, C
4. 句子 4：If no obstacle is present, the train is allowed to pass normally, and when the rear-end RF code is later received, the controller reverses the motor action and reopens the gate.
   对应摘录：C
5. 句子 5：This gives the paper a clear `EFSM + T1` structure because gate motion depends not only on train position events but also on an obstacle branch guarded by timed persistence and wireless inter-controller communication.
   对应摘录：A, B, C
