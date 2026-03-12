# PLC Controlling Program of an Elevator - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确写出了电梯同向优先、到层开门、关门等待以及障碍/超载重开门的离散控制链路。

## 条目 1: Direction-Priority Door Cycle
- 控制对象：楼宇机电领域的五层电梯 PLC 控制程序

### 0. 条目识别与判定
- 一句话说明：这是一个多层电梯控制程序，用于响应轿厢内外呼叫、按同向优先策略调度轿厢，并在到层后执行开门、关门与安全等待。
- 判断：算。对象是实际电梯控制软件，原文对呼叫处理、方向调度、门控与安全传感器响应给出了完整顺序描述。

### 1. 原文摘录

#### 摘录 A
- 出处：第 19 页，Section 3.2, 行 657-668
> The elevator is designed to move between four floors. Initially, the car is at the first floor, meaning that the it is at the very start of the operation. If the elevator is at another floor from the beginning, it makes no problem for the program. Signals from call buttons will activate the movement of the car.
>
> It will move in a power saving order, which means that if the car is moving in one direction and there is another call to an opposite direction, it will respond to all the calls in the initial direction before responding to the latter. For example, if the elevator just went up from floor 1 to floor 3 and there are two more calls to floor 5 and floor 1, it will continue moving up to floor 5.

#### 摘录 B
- 出处：第 19-20 页，Section 3.2, 行 670-687
> The elevator finishes a call when the call signal matches the floor level sensor. For example, a call to the second floor is finished when the signal from that floor’s level sensor is high and a floor call was made. Then, all the call signal to the second floor is reset to 0. The door is then opened for a fixed period then closed before the car moves to another floor. The car can only resume moving when the door is fully closed. When the Open button is pressed, the door is reopened if it is closing, if it is still opened then the open time is reset. There is also a fixed period after the door is fully closed again to wait for the Open button signal before the car moves again.
>
> If there is an obstacle between the doors or the elevator is overloaded, then the door is remained opened or reopened if is closing.

### 2. 基于原文整理后的自然语言描述

Call buttons activate the elevator car, and the controller serves all requests in the current travel direction before switching to opposite-direction calls. A call is completed when the floor-level sensor of the requested floor becomes active, after which the corresponding call memory is reset and the door is opened for a fixed period before closing. The car resumes movement only after the door is fully closed, while the open button, obstacle sensor, and overload sensor can reopen the door or keep it open.

### 3. 逐句溯源

1. 句子 1：Call buttons activate the elevator car, and the controller serves all requests in the current travel direction before switching to opposite-direction calls.
   对应摘录：A
2. 句子 2：A call is completed when the floor-level sensor of the requested floor becomes active, after which the corresponding call memory is reset and the door is opened for a fixed period before closing.
   对应摘录：B
3. 句子 3：The car resumes movement only after the door is fully closed, while the open button, obstacle sensor, and overload sensor can reopen the door or keep it open.
   对应摘录：B
