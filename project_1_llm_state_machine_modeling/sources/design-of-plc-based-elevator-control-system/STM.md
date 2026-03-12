# Design of PLC based Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对四层 PLC 电梯的呼梯、开门等待、关门、运行到目标层等顺序描述比较完整，可直接整理为自然语言控制逻辑。

## 条目 1: Four-floor PLC elevator service sequence
- 控制对象：四层 PLC 电梯的呼梯与送达控制逻辑

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电与电梯控制领域的 PLC 电梯控制器，用于接收楼层按钮请求、响应呼梯、控制轿厢门并将轿厢送到目标层。
- 判断：算。对象是实际电梯控制系统，原文直接给出了请求处理、开门等待、关门和移动到目标层的行为链路。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`II. PROPOSED SYSTEM DESIGN`，行 41-48
> In this PLC -based elevator control system, two supply voltages 5V and 12V are used. Proximity sensors, Arduino
> UNO, display and relay modules are supplied by 5V. Motors, call buttons, LED drivers and relays are supplied by 12V.I n this
> thesis, there are four sensors, eight displays and nine push button, 12V DC motor in total. Proximit y sensor is applied to al l floor
> elevators. When the elevator car reaches on sensor, the system will run in PLC and start working. As soon as the des ired floor is
> pressed with push button, display will show the desired floor at the panel of elevator. When the ele vator car is reached to t he caller,
> the do or of elevator car will open. After waiting for 3 seconds, the close switch is pressed. After that t he elevator car will move  to
> the input desired floor. When the elevator car is reached to the desired floor, the door of elevator  car will open for 3 seco nds. And
> then the close switch is pressed.

#### 摘录 B
- 出处：第 2 页，`III. BLOCK DIAGRAM OF PLC-BASED ELEVATOR CONTROL SYSTEM`，行 50-55
> The programmable logic controller is designed as eight inputs and six outputs  as shown in Fig. 1 . The eight inputs are four call
> buttons and four sensors. Relays, motors and displays are output. 220V power supply is used to run the whole process. 5V power
> supply is used for Arduino UNO, display, sensors and motors (for door close and open). 12V power sup ply is for display driver ,
> relays and motors (for up and down m otions).  Sensors and displays are used at the input section. Motors and relays are used at the
> output section. The whole system is controlled with the PLC. PLC receives the input signal from the proximity sensors and
> transmits the signals to the outputs (r elays and motors).

### 2. 基于原文整理后的自然语言描述

The PLC-based elevator controller receives floor-button requests and sensor inputs and uses relays and motors to drive door opening, door closing, and up-down motion. When a floor request is entered, the panel displays the requested floor, the car travels to the caller, opens the door for three seconds, closes the door, and then moves to the requested destination floor. After the car reaches the destination floor, the door opens again for three seconds and is then closed.

### 3. 逐句溯源

1. 句子 1：The PLC-based elevator controller receives floor-button requests and sensor inputs and uses relays and motors to drive door opening, door closing, and up-down motion.
   对应摘录：B
2. 句子 2：When a floor request is entered, the panel displays the requested floor, the car travels to the caller, opens the door for three seconds, closes the door, and then moves to the requested destination floor.
   对应摘录：A
3. 句子 3：After the car reaches the destination floor, the door opens again for three seconds and is then closed.
   对应摘录：A
