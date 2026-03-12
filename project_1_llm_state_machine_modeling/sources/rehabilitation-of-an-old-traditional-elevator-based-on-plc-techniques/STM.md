# Rehabilitation of an Old Traditional Elevator Based on PLC Techniques - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文清楚给出了楼层请求、位置传感、门锁联动和到层停止逻辑，可直接整理为电梯控制描述。

## 条目 1: Floor Request, Motion, and Door Interlock Control
- 控制对象：PLC 改造后的三层电梯控制系统

### 0. 条目识别与判定

- 一句话说明：这是楼宇机电控制领域的电梯 PLC 控制系统，用于处理楼层请求、根据位置传感决定上下行，并在运行期间锁定楼层门。
- 判断：算。对象是实际电梯控制系统，原文给出了请求输入、方向控制、传感器停梯和门锁联动规则。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section 2.1 Hardware Task，`paper_content.txt` 第 89-93 行
> The control system based on PLC techniques is accomplished by realizing six major components: PLC, AC motor and its actuators, push buttons, level sensors, display unit and elevator's cabin. Positioning level sensors are used to determine the elevator's position and the requesting push buttons are used as inputs by users. ... The PLC evaluates the user's request by the push button signal and the elevator's position by the level sensors to drive the elevator's motor up or down.

#### 摘录 B
- 出处：第 10-11 页，Program / Experimental Results，`paper_content.txt` 第 403-405, 458-463 行
> Figures (16) and (17) show a section of the program which controls the relation between the cabin's and the floors' requesting push-buttons and the retractile shoe for safety purposes by locking the doors of all the floors during the elevator's movement and allows the only door of the floor at which the cabin is landed to be opened.
>
> When pressing push button A1 or B1 of the ground floor; the motor will run until the cabin reaches the required position and activates the sensor to stop the motor, but if the cabin is in the required floor; the motor will not be operated. ... the motor will run either in the forward or in the reversed direction depending on its position, when the cabin reaches the required position; a sensor will be activated and stops the motor.

### 2. 基于原文整理后的自然语言描述

The PLC elevator controller reads floor request push buttons together with the level sensors to decide whether the cabin must move upward or downward. During elevator motion, the program locks the doors of all floors and allows only the door of the floor where the cabin has landed to be opened. When a floor request is issued, the motor runs in the required direction until the corresponding position sensor is activated, and no motion is commanded if the cabin is already at the requested floor.

### 3. 逐句溯源

1. 句子 1：The PLC elevator controller reads floor request push buttons together with the level sensors to decide whether the cabin must move upward or downward.
   对应摘录：A
2. 句子 2：During elevator motion, the program locks the doors of all floors and allows only the door of the floor where the cabin has landed to be opened.
   对应摘录：B
3. 句子 3：When a floor request is issued, the motor runs in the required direction until the corresponding position sensor is activated, and no motion is commanded if the cabin is already at the requested floor.
   对应摘录：B
