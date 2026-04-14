# Design of a Six-Lift, Ten-Level Elevator System Based on PLC and WinCC - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了六梯十层系统的模块化 PLC 群控链，覆盖初始化、上下行/变速、开关门、维护/超载和最短距离派梯，并明确写出 `50 ms`、`5 s` 等工程定时，足以形成楼宇机电方向的双 A 样本。

## 条目 1: Six-Lift Group and Door-Speed Supervisor
- 控制对象：楼宇机电与电梯控制领域的六梯十层群控电梯运行监督器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定
- 一句话说明：这是一个用 PLC 和 WinCC 实现的多电梯群控系统，上层按模块组织初始化、门控、维护、超载和派梯策略，下层按方向、速度和门状态执行具体动作。
- 判断：算。对象是实际多梯系统的运行控制器，原文不仅说明了模块划分，还给出了初始化规则、门控事件、速度阶段、维护/超载逻辑和最短距离派梯公式。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1-4 页，Abstract / `3.1 Elevator Initialization Module`，`paper_content.txt` 第 8-14 行、第 108-120 行
> ... the modular design of the PLC program is then discussed, detailing each module, including the initialization module, elevator up-and-down operation and speed control module, elevator door control module, and group control module ... when the target initialization floor is above the fifth floor, the elevator will move upward; otherwise, it will move downward ... contacts the first or second limit switches, the elevator's floor is set to the eleventh or ground floor. After that, the elevator moves to the target floor to complete initialization ...

#### 摘录 B
- 出处：第 5-7 页，`Elevator Up-and-Down Operation and Speed Control Module`，`paper_content.txt` 第 165-210 行
> ... When the elevator is not overloaded, under maintenance, and the floor door lock signals are in position ... the elevator will activate the up or down contactor ... Approximately 50 ms later, the elevator enters the first acceleration state ... Before the elevator reaches its stop position, a change-speed signal is sent by the lower leveling sensor ... the 1A contactor is first closed according to the time principle. Then, the 2A-4A contactors are closed in sequence according to the time principle ...

#### 摘录 C
- 出处：第 7-9 页，`Elevator Door Control / Maintenance and Overload Modules`，`paper_content.txt` 第 224-277 行
> ... When the elevator system receives an operational signal and reaches the designated floor, it will open the door ... After a five-second delay, the door-closing program begins ... an infrared light curtain anti-collision device is used ... Door Opening Events ... jammed or overloaded ... maintenance ... During maintenance, the elevator will stop accepting signals ... After maintenance is completed, the elevator will automatically execute the initialization program ... If the weight inside the cabin exceeds the rated weight, the elevator's door-opening relay is activated to prevent the door from closing ...

#### 摘录 D
- 出处：第 10-11 页，`Shortest Distance Scheduling Algorithm`，`paper_content.txt` 第 316-366 行
> ... the shortest distance is not the straight-line distance ... but rather the shortest distance that takes into account the elevator’s current direction of travel and any internal call floors ... If the up-call button on the 7th floor is pressed ... the elevator on the 5th floor only needs to travel two floors ... the elevator on the 9th floor needs to descend to the 3rd floor before traveling upwards to the 7th floor ... Using these two piecewise functions, the actual distances of six elevators ... are calculated, and the elevator with the shortest distance is selected to respond to the signal.

### 2. 基于原文整理后的自然语言描述

The paper organizes the six-lift controller as a hierarchical PLC program composed of initialization, travel-and-speed, door, maintenance/overload, and group-control modules rather than as a single flat sequence. At startup, the controller first determines the initialization direction from the target floor: if the target is above the fifth floor the car overshoots upward, otherwise it moves downward, uses the top or bottom limit switches to reset floor position, and only then returns to the target floor to complete initialization. During normal service, the motion module requires that overload, maintenance, and door-lock conditions all be satisfied before energizing the up or down contactor, and the drive chain then enters explicit speed stages, including a first acceleration stage after about `50 ms`, high-speed travel, low-speed leveling, and sequential braking through contactors `1A` to `4A`. The door controller opens at the target floor, starts closing after a `5 s` delay, halts closing when the infrared curtain detects an obstruction, and is further overridden by maintenance and overload logic, both of which can force door opening and suspend normal signal acceptance. At the group-control level, external hall calls are assigned by a shortest-distance scheduler that does not use naive geometric distance, but instead computes an actual service distance from current floor, motion direction, and queued travel, then dispatches whichever elevator minimizes that direction-aware cost.

### 3. 逐句溯源

1. 句子 1：The paper organizes the six-lift controller as a hierarchical PLC program composed of initialization, travel-and-speed, door, maintenance/overload, and group-control modules rather than as a single flat sequence.
   对应摘录：A
2. 句子 2：At startup, the controller first determines the initialization direction from the target floor: if the target is above the fifth floor the car overshoots upward, otherwise it moves downward, uses the top or bottom limit switches to reset floor position, and only then returns to the target floor to complete initialization.
   对应摘录：A
3. 句子 3：During normal service, the motion module requires that overload, maintenance, and door-lock conditions all be satisfied before energizing the up or down contactor, and the drive chain then enters explicit speed stages, including a first acceleration stage after about `50 ms`, high-speed travel, low-speed leveling, and sequential braking through contactors `1A` to `4A`.
   对应摘录：B
4. 句子 4：The door controller opens at the target floor, starts closing after a `5 s` delay, halts closing when the infrared curtain detects an obstruction, and is further overridden by maintenance and overload logic, both of which can force door opening and suspend normal signal acceptance.
   对应摘录：C
5. 句子 5：At the group-control level, external hall calls are assigned by a shortest-distance scheduler that does not use naive geometric distance, but instead computes an actual service distance from current floor, motion direction, and queued travel, then dispatches whichever elevator minimizes that direction-aware cost.
   对应摘录：D
