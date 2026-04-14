# PLC Controlling Program of an Elevator - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确写出了电梯同向优先、到层开门、关门等待以及障碍/超载重开门的离散控制链路。

## 条目 1: Direction-Priority Door Cycle
- 控制对象：楼宇机电领域的五层电梯 PLC 控制程序
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 同向优先电梯调度与门控）

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

#### 摘录 C
- 出处：第 30-32 页，`3.4.3 Elevator direction assignment`，行 890-937
> one direction (upward or downward) before responding to the remaining
> calls. To do this, two input memories are made (‘’up_memory’’ and
> ‘’down_memory’’) to represent the current direction of the elevator car.
> ...
> ‘’up_memory” memory output is set by an AND operation between
> “motor_up’’ and the OR operation of “F2_sensor’’, ‘’F3_sensor’’ and
> ‘’F4_sensor’’. This means that if the system responds to the upward signal
> and the elevator goes to floor 2, 3 or 4 then the car is assigned with the
> upward direction. The output is reset ... if the car reaches
> the fifth floor ... Likewise, the car is assigned to the downward direction if there is a
> downward signal at floors 2, 3, 4. The ‘’down_memory’’ output is reset
> when the car comes down to floor 1.

#### 摘录 D
- 出处：第 41-43 页，`3.4.6 Closing door / 3.4.7 Open button, overload sensor and obstacle sensor operation`，行 1072-1135
> Whenever an open-end signal is set (‘’door_openedF(n)’’), an on-delay
> timer ... represents the time the door remains opened. After that, output Q
> of the timer makes the following instructions:
> - ‘’door_motor’’ is reset to close the door.
> - Input memory ‘’door_closing’’ is assigned to block ‘’door_motor’’
> from being set in the previous network.
> - Another timer is set to represents the time it takes the door to fully
> close. After that ‘’door_closed’’ is assigned.
> ...
> When the Open button is reset after three second ... the timer in
> previous network is initialized again.
> In the second scenario, when the door is closing ... if the open button is pressed then the door is reopened.
> ...
> In all scenarios the three second timer cannot be activated if there is a
> signal from either the obstacle or the overload sensor. The door will then
> be remained opened until both signals are false.
> ...
> the operation keeps the door opened until both obstacle and overload sensor
> signals are False, then the open button is reset after three seconds.

### 2. 基于原文整理后的自然语言描述

The elevator starts from floor 1 by default but can also start from any other floor, and every car call or floor call activates movement while the controller keeps a same-direction service order until the current direction has been cleared. This direction priority is memorized explicitly by `up_memory` and `down_memory`: the upward memory is latched while the car is moving up through floors 2-4 and is reset at floor 5, whereas the downward memory is latched while the car is moving down through floors 2-4 and is reset at floor 1. A call is completed when the request matches the floor-level sensor of the target floor, after which the corresponding call memory is reset, the door is opened for a fixed dwell interval, the door is then closed, and the car is allowed to move again only after `door_closed` becomes true and the post-close waiting period for the Open button has expired. The door logic also keeps explicit `door_opened`, `door_closing`, and `door_closed` memories, resets the open timer when the Open button is pressed while the door is already open, reopens the door if Open is pressed during closing, and blocks the three-second open-button reset whenever the obstacle or overload sensor remains active.

### 3. 逐句溯源

1. 句子 1：The elevator starts from floor 1 by default but can also start from any other floor, and every car call or floor call activates movement while the controller keeps a same-direction service order until the current direction has been cleared.
   对应摘录：A, B
2. 句子 2：This direction priority is memorized explicitly by `up_memory` and `down_memory`: the upward memory is latched while the car is moving up through floors 2-4 and is reset at floor 5, whereas the downward memory is latched while the car is moving down through floors 2-4 and is reset at floor 1.
   对应摘录：C
3. 句子 3：A call is completed when the request matches the floor-level sensor of the target floor, after which the corresponding call memory is reset, the door is opened for a fixed dwell interval, the door is then closed, and the car is allowed to move again only after `door_closed` becomes true and the post-close waiting period for the Open button has expired.
   对应摘录：B, D
4. 句子 4：The door logic also keeps explicit `door_opened`, `door_closing`, and `door_closed` memories, resets the open timer when the Open button is pressed while the door is already open, reopens the door if Open is pressed during closing, and blocks the three-second open-button reset whenever the obstacle or overload sensor remains active.
   对应摘录：B, D
