# Simulation and Modelling of 3-Floor Elevator System using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三层电梯 PLC 的楼层请求、方向优先、门开闭定时、开门重置和障碍/超载门保持写成了一条完整控制链，足够形成 `🏢` 方向的双 A 条目。

## 条目 1: Direction-Priority Elevator Door-Cycle PLC Controller

- 控制对象：楼宇机电与电梯控制领域的三层电梯 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向三层电梯的 PLC 顺序控制器，利用楼层请求、楼层传感、门状态与障碍/超载条件来管理电梯运行与门周期。
- 判断：算。对象是真实电梯控制系统，原文虽未把所有状态名写成抽象符号表，但明确给出输入类别、方向优先调度、门开闭定时、开门按钮重置与障碍/超载保持开门等可直接整理成状态机的控制逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`2.1 Sequence of Operation / 2.4 Design of System`，`paper_content.txt` 第 142-147、197-200 行
> The inputs observed are 6 signals namely Car Location, Floor Buttons, Car Buttons, Car Movement (Direction), Door Status, and Signal Triggers.
>
> Ladder logic allows us to control door openings, travel direction, and time. Call buttons will move the car.

#### 摘录 B

- 出处：第 5 页，`2.5 Working of the Simulation`，`paper_content.txt` 第 240-253 行
> The first floor marks the beginning of the operation for the car.
>
> The car is started by push buttons. It moves in an order that maximises the amount of power saved, so if the car is moving in one direction and another call comes in, it will respond to all of the calls in the first direction before it responds to any calls in the second direction.
>
> After having been opened for a predetermined amount of time, the door is then closed in preparation for moving to the next level.

#### 摘录 C

- 出处：第 5 页，`2.5 Working of the Simulation`，`paper_content.txt` 第 253-260 行
> When the door is shut, the car is able to move forward once more. If the door is closing, pressing the Open button will reopen it, and if it is already open, it will reset the amount of time it has been open.
>
> When the passenger door is shut, the vehicle remains stationary until it receives a signal from the Open button. In the event that there is a barrier or that the elevator is too full, the door will either remain open or reopen.

#### 摘录 D

- 出处：第 5 页，`3. Result and Discussion`，`paper_content.txt` 第 274-291 行
> The operation begins with pressing the button for the desired flow, and if the elevator is already on that floor, the motor will start running according to it; for example, if the elevator is located below the desired floor, it will rotate in a clockwise direction, but if it is located above the desired floor, it will rotate in a counter clockwise direction.
>
> ... additional safety measures like sounding the alarm when the weight of the lift reaches the pre determined maximum level or when the door is unable to close due to some obstacles.

### 2. 基于原文整理后的自然语言描述

The three-floor elevator controller is implemented as a PLC-based extended state machine whose control variables include car location, floor requests, movement direction, door status, and signal triggers. The controller starts from the first floor, accepts push-button requests, and follows a direction-priority policy: once the car is moving in one direction, it clears all pending calls in that direction before serving calls in the opposite direction. Its door cycle is not implicit but explicitly governed by control logic, because the door is opened for a predetermined duration, then closed before the car is allowed to resume motion toward the next floor. During that cycle, pressing the `Open` button while the door is closing forces a reopen, pressing it while the door is already open resets the open duration, and obstacle or overload conditions keep the door open or reopen it instead of allowing the car to continue. The motion branch also checks whether the requested floor lies above or below the current one, so the motor direction changes accordingly and the car remains stopped whenever the passenger door is shut and no new opening condition is granted.

### 3. 逐句溯源

1. 句子 1：The three-floor elevator controller is implemented as a PLC-based extended state machine whose control variables include car location, floor requests, movement direction, door status, and signal triggers.
   对应摘录：A
2. 句子 2：The controller starts from the first floor, accepts push-button requests, and follows a direction-priority policy: once the car is moving in one direction, it clears all pending calls in that direction before serving calls in the opposite direction.
   对应摘录：B
3. 句子 3：Its door cycle is not implicit but explicitly governed by control logic, because the door is opened for a predetermined duration, then closed before the car is allowed to resume motion toward the next floor.
   对应摘录：B
4. 句子 4：During that cycle, pressing the `Open` button while the door is closing forces a reopen, pressing it while the door is already open resets the open duration, and obstacle or overload conditions keep the door open or reopen it instead of allowing the car to continue.
   对应摘录：C
5. 句子 5：The motion branch also checks whether the requested floor lies above or below the current one, so the motor direction changes accordingly and the car remains stopped whenever the passenger door is shut and no new opening condition is granted.
   对应摘录：C, D
