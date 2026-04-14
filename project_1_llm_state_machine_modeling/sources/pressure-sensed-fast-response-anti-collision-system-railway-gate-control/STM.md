# Pressure Sensed Fast Response Anti-Collision System for Automated Railway Gate Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把道口门在列车到达、45°检测、90°闭锁、障碍停机和列车离开后回开的完整控制链写清楚了，足以形成双 A 样本。

## 条目 1: Pressure-Sensed 45° Hold Railway Gate Controller

- 控制对象：轨道交通与铁路控制领域的带防碰撞检测的铁路道口门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于 `PIC16F84A` 的铁路道口控制器，用 `IR-1 / IR-2` 检测列车到达与离开，并在门体下落到 `45°` 时用压力开关判断是否有车辆卡在轨道上。
- 判断：算。对象是实际铁路平交口门控系统，原文明确给出到达检测、45°中间检查、90°关门、压力传感器停机、紧急灯告警和离站回开的连续控制链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`Abstract / Introduction`，`paper_content.txt` 第 21-30、41-51 行
> This paper presents an innovative project design of a pressure sensor based swift response anti-collision system for an automatic railway gate control.
>
> The novelty of this project based paper is the use of pressure switch which has been integrated in this anti-collision system for the railway.
>
> By employing the automatic gate control at the railway level crossing the arrival of the trains are detected by the IR sensors placed on either side of the gate. Once the arrival is sensed, the sensed signal is sent to the microcontroller and it checks the possible presence of any vehicle between the gates, again using sensor. Once no vehicle is sensed in between the railway gate then the motor is activated and the gates are closed. But if any obstacle is sensed it is indicated to the train drivers and necessary steps are taken according to solve the emergency problems. When the train is passed through using the same process gate is opened.

#### 摘录 B

- 出处：第 3-4 页，`Proposed implementation planning / Algorithm`，`paper_content.txt` 第 101-120、128-139 行
> If we consider the train is coming from the left side of the track then if the train touches the IR-1 (Receiver) it will send the signal to the Microcontroller and the microcontroller pass this signal to the motor driver controller.
>
> When the gate is closing down it will stop and check at 45° for any presence of the vehicle from the pressure sensor. If no vehicle gets stuck at the level crossing, then our Microcontroller will allow the gate to be closed at 90°. If the microcontroller could sense any presence of the vehicle at the level crossing it will send signal to the motor and it will stop at 45°. It will also give an emergency signal to train driver so that the driver of the train could take necessary actions to avoid the collision.
>
> The departures of the train are sensed then go to Step-8 otherwise goes to Step-6. Open the gate.

#### 摘录 C

- 出处：第 8-9 页，`4.2 Results in Three Different Cases`，`paper_content.txt` 第 306-310、317-322、335-339 行
> As the gate will always check at 45° it would always be closed as we can see from the figure. When the train is coming we need to close the push button named as Close. So the gate will be closing down and at 45° it will check for the presence of any vehicle that gets stuck. If any object is not found then the gate it is closed properly.
>
> To show the departure of the train from the level crossing we need to open the CLOSE button and close the OPEN button. As soon as we close this button, it will send signal to the Microcontroller and motor will rotate in clock wise position so that the gate can open and allow the vehicle to pass through the level crossing.
>
> So the gate is closing down it will check at 45° and it will get a signal of any living object that gets stuck at the level crossing of the rail-line. So our Microcontroller will give signal to the motor to Stop and send this emergency signal to the train driver making the emergency light ON.

### 2. 基于原文整理后的自然语言描述

The railway crossing controller uses two IR train-detection sensors and a `PIC16F84A` microcontroller to automate gate closure and reopening at a level crossing without relying on a human gatekeeper. When an approaching train activates `IR-1`, the controller commands the motor driver to start the closing sequence, but the gate does not drop blindly to the final shut position. Instead, the controller enforces an intermediate check at `45°`, where a pressure switch is used to test whether a vehicle or other object is trapped on the crossing. If the crossing is clear, the gate continues down to `90°` and remains closed until the departure side is sensed through `IR-2`; if an obstacle is detected, the controller stops the motor at `45°` and raises an emergency indication for the train driver. After the train clears the crossing, the departure event triggers the reverse motor direction so that the gate reopens and road traffic can resume.

### 3. 逐句溯源

1. 句子 1：The railway crossing controller uses two IR train-detection sensors and a `PIC16F84A` microcontroller to automate gate closure and reopening at a level crossing without relying on a human gatekeeper.
   对应摘录：A
2. 句子 2：When an approaching train activates `IR-1`, the controller commands the motor driver to start the closing sequence, but the gate does not drop blindly to the final shut position.
   对应摘录：B
3. 句子 3：Instead, the controller enforces an intermediate check at `45°`, where a pressure switch is used to test whether a vehicle or other object is trapped on the crossing.
   对应摘录：B, C
4. 句子 4：If the crossing is clear, the gate continues down to `90°` and remains closed until the departure side is sensed through `IR-2`; if an obstacle is detected, the controller stops the motor at `45°` and raises an emergency indication for the train driver.
   对应摘录：B, C
5. 句子 5：After the train clears the crossing, the departure event triggers the reverse motor direction so that the gate reopens and road traffic can resume.
   对应摘录：A, C
