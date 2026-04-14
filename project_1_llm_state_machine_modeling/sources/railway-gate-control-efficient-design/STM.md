# Railway Gate Control: An Efficient Design - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟 / 协议交互
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `XBee 到车/离车检测 -> SG1/SG2 信号 -> 栏杆动作 -> 车辆占道抑制 -> LCD 状态` 组织成一条完整门控链，并给出原型里的显式延时。

## 条目 1: XBee-based railway gate controller with SG1/SG2 vehicle-presence interlock

- 控制对象：轨道交通与铁路控制领域的 `XBee` 来离车检测、`SG1/SG2` 信号与车辆占道联锁门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟、协议交互
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `Arduino Mega/Uno + XBee + SG1/SG2 + IR vehicle sensor + LCD` 的铁路道口门控系统，用无线来离车报文驱动关门/开门，并在车辆仍占道时通过信号抑制列车继续通过。
- 判断：算。对象是真实道口控制器，原文不仅给出硬件表，还明确说明到车、离车、车辆占道和状态显示之间的顺序关系，以及 `2 s` 原型延时和小于 `1 s` 的无线传输特征。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 48-59 行
> Railway transportation is one of the most important land vehicles in the country. A train station scenario consists of a gate which is located two kilometers. The gatekeeper controls the gate based on information from railway station master regarding the presence of train. ... The main objective of this work is to develop an automatic railway gate control using Arduino Atmega microcontroller. ... One unit of Xbee wireless acted as a transmitter to send a signal for the train arrival, and two units of Xbee are used as receivers of the signal from the transmitter. ... The whole control system status using microcontroller is displayed on the LCD screen.

#### 摘录 B

- 出处：第 2-3 页，`Introduction / Working Operation / Table 1`，`paper_content.txt` 第 69-73、93-148 行
> Xbee wireless sensors are used as a train sensor and rail sensor. This sensor can be used for detect the train arrival and the signal will send to microcontroller to turn operation of motor and the gate will be close. Meanwhile, the rail sensor for departure of the train will send the signal to microcontroller to turn operation of motor and the gate will be open. IR sensor is used for the vehicle presence sensor.
>
> Train Sensor (TX1) ... can transmit the data to rail sensor RX1 when the train moves to level crossing, or ... to rail sensor RX2 when the train crossing the level crossing.
> ...
> Rail Signal (SG1) ... is the first signal placed at the side of the rail. SG1 is still given a YELLOW light to inform the train driver.
> ...
> Rail Signal (SG2) ... is the second signal placed at the side of the track to inform the train driver when the gate is closing or opening. if any vehicle or obstacle: signal SG2 is RED light.

#### 摘录 C

- 出处：第 5-6 页，`Experimental Result and Analysis`，`paper_content.txt` 第 194-200、226-235 行
> Data transmission from Xbee3 (TX1) to Xbee1 (RX1) or Xbee2 (RX2) occurred through wireless communication ... when the Xbee3 was transmitted to Xbee1, the character 'A' was represented in Uart/Serial Data for 'Arriving', which is it shows the train move to level crossing.
>
> The process of data transmission from Xbee3 (TX1) to Xbee1 (RX1) was less than 1 second to ensure the Xbee1 receives the signal without any disturbance and is related with the speed of the train. ... the coding for 'train move' in Arduino Uno was set to '2 seconds delay' before the train moving.

#### 摘录 D

- 出处：第 7-8 页，`System condition when there is vehicle at level crossing / Discussion`，`paper_content.txt` 第 258-267、284-306 行
> The system failure could determine by detection of the status of the system which is displayed on LCD display with ‘TRAIN STANDBY’ status, and gate still opened ...
>
> Since there is no vehicle, signals SG1 given a YELLOW signal to signal that the train is in the control zone automatic gates. If the road user sensor indicates the presence of vehicle, the signal for train, SG2 should be made RED in order to slow down the train to avoid collision. Then the obstacle should be warned to clear the path.
>
> The system is very efficient because of some features as follows; ... Provide SG1 with YELLOW signal as a warning to train that it was in the automatic railway gate control zone ... Provide SG2 after SG1, as a signal to the train on the presence of vehicle on a level crossing. ... L1 and L2 indicated the road users with RED signals immediately upon receiving the information about the presence of the train.

### 2. 基于原文整理后的自然语言描述

The railway gate controller uses `XBee3` on the train as a wireless transmitter and `RX1/RX2` near the track as the arrival and departure receivers that drive the gate logic. When the train enters the control zone, the arrival message is sent from `TX1` to `RX1`, the Arduino-based gate controller starts the closing process, `SG1` gives a yellow warning to the train, and the road-side lights warn users that the train is approaching. After the train has crossed the level crossing, the departure message is sent to `RX2`, which makes the controller reopen the gate and return the system toward its normal state. In the prototype, the train motion is intentionally delayed by `2 s` before starting, and the wireless transmission from `TX1` to `RX1` is reported to take less than `1 s`, so the open/close chain has explicit local timing. If the IR vehicle-presence sensor still detects an obstacle on the crossing, `SG2` is forced to red so the train is slowed or held while the LCD reports the system state such as `TRAIN STANDBY`.

### 3. 逐句溯源

1. 句子 1：The railway gate controller uses `XBee3` on the train as a wireless transmitter and `RX1/RX2` near the track as the arrival and departure receivers that drive the gate logic.
   对应摘录：A, B
2. 句子 2：When the train enters the control zone, the arrival message is sent from `TX1` to `RX1`, the Arduino-based gate controller starts the closing process, `SG1` gives a yellow warning to the train, and the road-side lights warn users that the train is approaching.
   对应摘录：A, B, D
3. 句子 3：After the train has crossed the level crossing, the departure message is sent to `RX2`, which makes the controller reopen the gate and return the system toward its normal state.
   对应摘录：B
4. 句子 4：In the prototype, the train motion is intentionally delayed by `2 s` before starting, and the wireless transmission from `TX1` to `RX1` is reported to take less than `1 s`, so the open/close chain has explicit local timing.
   对应摘录：C
5. 句子 5：If the IR vehicle-presence sensor still detects an obstacle on the crossing, `SG2` is forced to red so the train is slowed or held while the LCD reports the system state such as `TRAIN STANDBY`.
   对应摘录：B, D
