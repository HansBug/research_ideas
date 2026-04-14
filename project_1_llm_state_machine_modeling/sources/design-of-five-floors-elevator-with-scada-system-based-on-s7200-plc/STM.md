# Design of Five Floors Elevator with SCADA System Based on S7200 PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把五层电梯的 hall call / car call、方向判定、自动开关门与 SCADA 监控链写得比较完整，可以稳定整理成双 A 的五层电梯顺序控制样本。

## 条目 1: Five-floor SCADA elevator request-and-door-cycle controller

- 控制对象：五层 PLC/SCADA 电梯的呼梯、方向判定与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（G4 电梯 door-cycle / direction-priority）

### 0. 条目识别与判定

- 一句话说明：这是一个五层电梯 PLC 控制器，用 hall button、cab request、floor sensor 与 limit switch 组织呼梯、方向切换、到层停靠和自动门控。
- 判断：算。对象是实际楼宇机电控制系统，原文直接给出了外呼/内选按钮、空闲保持、队列首元素方向判定、门开关与 SCADA 监视链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`4.4 Buttons / 5. Problems to be solved through ladder diagram`，`paper_content.txt` 第 116-149 行
> Hall buttons are on a panel on the outside of the elevator shafts and are used by potential passengers to call an elevator cab to the floor that the pressed summon button is located on. Floor request buttons ... each cab has 5 floors request buttons labeled 1 through 5 ... There is button on the interior panel of each cab. A passenger can press this button to open the elevator doors or keep pressing it to keep them open, but only when the elevator cab is stopped at a floor.
>
> ... the door of the elevator should be programmed to open and close automatically. When the elevator has no request it remains at its current floor with its door closed ... the input signals are operational modes, safety control signals, car-calls, hall-calls, floor sensors, leveling sensors, door opening and close signals. ... the functions includes registration ... monitoring the door opening and closing, prioritizing the hall call, and car calls.

#### 摘录 B

- 出处：第 4 页，`7. Hall Call Request / 8. Up and down control signal identification`，`paper_content.txt` 第 191-213 行
> There are two kinds of calls in the elevator they are hall call and car call. When the passenger presses the button in the control panel which is outside the elevator cabin that is the hall call. When the passenger presses the button on the control panel which is inside the elevator car that is the car call.
>
> ... when the user press the button sends out the down signal to inform the PLC to control the elevator to run to the floor where the passenger at.
>
> ... when the passenger press the button sends out the up request signal to inform the PLC to take the elevator for the floor where the passenger at.
>
> The combination of hall call and car calls are used to decide the elevator movement in upward or downward direction. If the current position of the elevator is less than the first element of the queue then the elevator will move in the upward direction.

#### 摘录 C

- 出处：第 5-6 页，`11. Supervisory control and data acquisition systems (SCADA) / 12. Results and Discussion / 13. Conclusion`，`paper_content.txt` 第 236-287 行
> SCADA allows operators to ... Monitor the elevator status. Interact with and control the elevator ... Access history Record for maintenance and faults checking.
>
> When you push the button for the first floor ... the motor runs till the cabinet reaches its required position and activates the limit switch which enables the motor to stop and if the cabinet is already in the required position then the motor won't get activated again ... for the second floor ... the motor runs either in forward or reversed condition according to its position till the cabinet reaches its required position and activates the limit switch which enables the motor to stop ...
>
> ... the required inputs and outputs of elevator for moving forward and reverse, door opening and closing and motor operation have been included in the logic and interpreted.

### 2. 基于原文整理后的自然语言描述

The five-floor elevator controller receives both `hall call` requests from the corridor panels and `car call` requests from the cabin panel, while also accepting a door-open hold command that is valid only when the cab is already stopped at a floor. When there is no pending request, the controller keeps the cab at its current floor with the door closed and the current-floor indication active. Once calls are registered, the PLC combines hall-call and car-call information into a queue, compares the current position with the first queued request, and drives the cab upward when the current floor is below that first queued target, otherwise driving in the reverse direction toward the requested floor. Arrival is confirmed by the floor/limit-switch signal, which stops the motor and prevents a redundant restart when the cab is already at the requested position. Around this motion chain, the same PLC logic also controls automatic door opening and closing, direction lamps, floor displays, and the SCADA/HMI layer used for monitoring status, operator interaction, and maintenance-fault history.

### 3. 逐句溯源

1. 句子 1：The five-floor elevator controller receives both `hall call` requests from the corridor panels and `car call` requests from the cabin panel, while also accepting a door-open hold command that is valid only when the cab is already stopped at a floor.
   对应摘录：A, B
2. 句子 2：When there is no pending request, the controller keeps the cab at its current floor with the door closed and the current-floor indication active.
   对应摘录：A
3. 句子 3：Once calls are registered, the PLC combines hall-call and car-call information into a queue, compares the current position with the first queued request, and drives the cab upward when the current floor is below that first queued target, otherwise driving in the reverse direction toward the requested floor.
   对应摘录：A, B
4. 句子 4：Arrival is confirmed by the floor/limit-switch signal, which stops the motor and prevents a redundant restart when the cab is already at the requested position.
   对应摘录：C
5. 句子 5：Around this motion chain, the same PLC logic also controls automatic door opening and closing, direction lamps, floor displays, and the SCADA/HMI layer used for monitoring status, operator interaction, and maintenance-fault history.
   对应摘录：A, C
