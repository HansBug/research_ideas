# Rehabilitation of an Old Traditional Elevator Based on PLC Techniques - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了楼层请求、位置传感和门锁联动，还明确写出 same-floor 不动作、维护模式切换与 `RR` 延时指示链，可直接整理为电梯控制描述。

## 条目 1: Floor Request, Motion, and Door Interlock Control
- 控制对象：PLC 改造后的三层电梯控制系统
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟡 B（细节较充实）
- 描述细节充实度：🟡 B（细节较充实）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的电梯 PLC 控制系统，用于处理楼层请求、根据位置传感决定上下行，并在运行期间锁定楼层门。
- 判断：算。对象是实际电梯控制系统，原文给出了请求输入、方向控制、传感器停梯和门锁联动规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2-3 页，Section 2.1 Hardware Task，`paper_content.txt` 第 89-101, 117-120 行
> The control system based on PLC techniques is accomplished by realizing six major components: PLC, AC motor and its actuators, push buttons, level sensors, display unit and elevator's cabin. Positioning level sensors are used to determine the elevator's position and the requesting push buttons are used as inputs by users. The number of each floor will be displayed on the display units as outputs. The PLC evaluates the user's request by the push button signal and the elevator's position by the level sensors to drive the elevator's motor up or down.
>
> The schematics of the control system of old elevator consist of three groups of sensors ... sensors ES and EI were swapped with two inductive proximity sensors and sensors of type CP were swapped with photo sensors. In part (b) only sensors of type CPC were swapped with reed switch sensors.
>
> Upper extra-run contact `ES`; Lower extra-run contact `EI`; Preliminary approaching Contact `CP`.

#### 摘录 B
- 出处：第 10-11 页，Program / Experimental Results / Flowchart，`paper_content.txt` 第 403-405, 428-429, 447-463, 481-489 行
> Figures (16) and (17) show a section of the program which controls the relation between the cabin's and the floors' requesting push-buttons and the retractile shoe for safety purposes by locking the doors of all the floors during the elevator's movement and allows the only door of the floor at which the cabin is landed to be opened.
>
> Figure (18) shows the segment of the program that controls the signaling circuits of the elevator as an interactive system with human beings and the alarm circuit in case of emergency. ... "Engaged" indication lamp controlled by the OFF delay timer (RR).
>
> Maintenance ... Fig. 19 The Maintenance and the Reverser Section of the Program.
>
> When pressing push button A1 or B1 of the ground floor; the motor will run until the cabin reaches the required position and activates the sensor to stop the motor, but if the cabin is in the required floor; the motor will not be operated. Also by pressing push button A3 or B3 of the second floor; the motor will run either in the forward or in the reversed direction depending on its position, when the cabin reaches the required position; a sensor will be activated and stops the motor. The motor of the elevator will not run if the cabin is in the required floor as mentioned before; subsequently this concept works for other floors too.
>
> Press either A1/A2/A3 or B1/B2/B3 ... Motor will run in the appreciated direction ... The cabinet will ascend or descend ... Is sensor actuated? ... Motor Stops ... The cabinet reaches the desired floor.

### 2. 基于原文整理后的自然语言描述

The PLC-based three-floor elevator evaluates cabin buttons `A1/A2/A3` and floor buttons `B1/B2/B3` together with level sensors, extra-run sensors `ES/EI`, and approach or door sensors to decide the motor direction and the current cabin position. During movement, the retractile shoe locks the doors of all floors, only the landed floor door may open, the `PRESENT` indicators follow the position sensors, and the parallel `ENGAGED` lamps are driven through the `RR` off-delay timer. When a request is issued, the motor runs upward or downward until the corresponding arrival sensor is actuated; if the cabin is already at the requested floor, the motor is not operated. If the `INT` maintenance switch opens, the normal request circuits are isolated and the cabin can instead be moved upward or downward by maintenance push buttons.

### 3. 逐句溯源

1. 句子 1：The PLC-based three-floor elevator evaluates cabin buttons `A1/A2/A3` and floor buttons `B1/B2/B3` together with level sensors, extra-run sensors `ES/EI`, and approach or door sensors to decide the motor direction and the current cabin position.
   对应摘录：A
2. 句子 2：During movement, the retractile shoe locks the doors of all floors, only the landed floor door may open, the `PRESENT` indicators follow the position sensors, and the parallel `ENGAGED` lamps are driven through the `RR` off-delay timer.
   对应摘录：B
3. 句子 3：When a request is issued, the motor runs upward or downward until the corresponding arrival sensor is actuated; if the cabin is already at the requested floor, the motor is not operated.
   对应摘录：B
4. 句子 4：If the `INT` maintenance switch opens, the normal request circuits are isolated and the cabin can instead be moved upward or downward by maintenance push buttons.
   对应摘录：B
