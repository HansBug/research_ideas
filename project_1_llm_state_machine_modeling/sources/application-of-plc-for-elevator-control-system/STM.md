# Application of PLC for Elevator Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 `SOURCES.md` 盘点：是
- 提取条目数：1
- 简要判断：论文直接给出了“呼梯到目标层后电机正反转并在限位信号处停靠”的 PLC 电梯控制逻辑。

## 条目 1: Level-Call Driven Elevator Motion
- 控制对象：楼宇机电领域的 PLC 电梯控制系统

### 0. 条目识别与判定
- 一句话说明：这是一个单轿厢电梯控制器，用于根据楼层呼叫驱动轿厢上行或下行，并在目标层由限位开关反馈停靠。
- 判断：算。对象是实际电梯控制系统，原文直接描述了呼梯、正反转、位置反馈和停层逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Section 2, 行 98-109
> The working principle of PLC for elevator control system functions in the similar manner as that the elevator we use in our daily life. The motion of the elevator that people normally use is controlled by a stepper motor. It consists of a pulley which helps in upward and downward movement of the lift. The position feedback is provided by the limit switches. The principle of this set up is; whenever the cabinet is called to any level, the motor either runs in forward or reverse direction and then stops at the level indicated. The indication of the level or the position of the cabinet is given by the limit switches which act as a sensor and gives the signal indicating that the cabinet has reached the required position.

### 2. 基于原文整理后的自然语言描述

When the elevator cabinet is called to a target level, the PLC drives the motor in either the forward or reverse direction to move the lift upward or downward. Limit switches provide position feedback and indicate when the cabinet has reached the required level, at which point the motor stops.

### 3. 逐句溯源

1. 句子 1：When the elevator cabinet is called to a target level, the PLC drives the motor in either the forward or reverse direction to move the lift upward or downward.
   对应摘录：A
2. 句子 2：Limit switches provide position feedback and indicate when the cabinet has reached the required level, at which point the motor stops.
   对应摘录：A
