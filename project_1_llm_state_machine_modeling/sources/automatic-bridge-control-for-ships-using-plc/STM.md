# Automatic Bridge Control for Ships Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把船舶到达检测、路障与信号切换、桥体开闭、水位侧条件和紧急停机组织成一条完整的 PLC 开桥控制链，原文足以支撑双 A 条目。

## 条目 1: Ship-triggered bridge and barrier control cycle

- 控制对象：通用控制与交通基础设施领域的船舶触发开桥、栏杆联动与信号切换控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个可开启桥梁的 PLC 控制器，用船舶红外检测、道路栏杆、桥体执行器、红绿信号、水位监测和紧急停机来协调水路与道路通行切换。
- 判断：算。对象是真实交通基础设施控制系统，不是硬件拼装说明；原文明确给出了来船检测、栏杆与桥体动作、开闭桥切换、水位监测和 emergency stop。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract`，`paper_content.txt` 第 11-30 行
> The idea is to automate the process of ship detection, opening or closing of a bridge, controlling the signals and road barriers. ... Some Sensors such as IR Sensor, Ultrasonic Sensor are used to provide input to the system and servo motor serves as an actuator. ... With the help of IR Sensor the arrival and leaving of the ship is monitored and bridge is operated accordingly and Ultrasonic sensor is used to detect the level of the water.

#### 摘录 B

- 出处：第 1 页，`Introduction`，`paper_content.txt` 第 46-68 行
> To overcome this problem humans have built a bridge that can open and close. The river can thus be used for two type of transportation, namely road and water. ... A PLC monitors inputs, makes decisions based on its program, and controls outputs to automate a process. ... Ship is detected by IR sensor which is placed on the edges of bridge. Sensor output provides input to the PLC and it’ll control opening of bridge using Servo motor and road barrier according to programming. ... The sensor checks the presence of Ship and level of the water.

#### 摘录 C

- 出处：第 3-4 页，`IR Sensor / Road Barrier / Signal / Proposed System`，`paper_content.txt` 第 184-190、247-264、268-280 行
> IR sensor is used to check the presence of ships. ... When ship is detected by IR sensor it will send the signal to the PLC to open the bridge and when ship is not detected by IR sensor it will send the signal to the PLC to close the bridge.
>
> Road barrier is used to indicate vehicle to stop. When ship would be detected, red light would be ON to indicate vehicle to stop because bridge will be about to open ... after that bridge is closed then Green lights is turned ON again ...
>
> Firstly the system will start using start switch then IR Sensors is used to detect the ship. If ship is sensed by the sensor it gives the high pulse to the PLC. According to the sensor output, PLC will control the servo motor as well as road barrier. ... Water level monitoring circuit will continuously monitor the level of water ... If in case of emergency situation occurs then emergency stop switch will used to stop the system.

### 2. 基于原文整理后的自然语言描述

The bridge controller is a PLC-based traffic-switching system that coordinates ship passage, road barriers, bridge motion, signal lights, water-level monitoring, and an emergency-stop path. Once the system is armed by the start switch, an IR sensor at the bridge edge detects an arriving ship and sends a high pulse to the PLC, which then commands the barrier and bridge actuators according to the programmed sequence. During this ship-arrival branch, the road barrier changes the road side to red so vehicles stop while the bridge is about to open, and the same IR logic later tells the PLC to close the bridge again once the ship is no longer detected. After the closure branch completes, the road signal returns to green and road traffic is released, so the overall controller alternates the infrastructure between road-open and ship-open conditions. Throughout the cycle, an ultrasonic water-level circuit keeps monitoring the water state, and the emergency-stop switch provides an immediate stop branch for abnormal situations.

### 3. 逐句溯源

1. 句子 1：The bridge controller is a PLC-based traffic-switching system that coordinates ship passage, road barriers, bridge motion, signal lights, water-level monitoring, and an emergency-stop path.
   对应摘录：A, B, C
2. 句子 2：Once the system is armed by the start switch, an IR sensor at the bridge edge detects an arriving ship and sends a high pulse to the PLC, which then commands the barrier and bridge actuators according to the programmed sequence.
   对应摘录：B, C
3. 句子 3：During this ship-arrival branch, the road barrier changes the road side to red so vehicles stop while the bridge is about to open, and the same IR logic later tells the PLC to close the bridge again once the ship is no longer detected.
   对应摘录：A, C
4. 句子 4：After the closure branch completes, the road signal returns to green and road traffic is released, so the overall controller alternates the infrastructure between road-open and ship-open conditions.
   对应摘录：C
5. 句子 5：Throughout the cycle, an ultrasonic water-level circuit keeps monitoring the water state, and the emergency-stop switch provides an immediate stop branch for abnormal situations.
   对应摘录：A, B, C
