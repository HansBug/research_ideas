# CONTROL AND MONITORING SYSTEM OF ELEVATORS USING INDUSTRIAL PLC SYSTEM - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文不仅给出了三梯竞争分配的队列与方向规则，还把速度分档、减速停靠、开关门与队列清空逻辑写成了连续的工程控制链，适合入库为楼宇机电方向的双 A 电梯样本。

## 条目 1: Queue-Based Three-Elevator Dispatch and Motion Controller

- 控制对象：楼宇机电与电梯控制领域的三梯竞争调度与轿厢运行控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个基于工业 `PLC + SCADA` 的三梯控制系统，用队列、方向和等待时间竞争分配外呼，再用速度分档、减速停靠和 `6 s` 门操作时序管理轿厢运行。
- 判断：算。对象是真实电梯群控与单梯执行控制，而不是单纯 SCADA 监控界面；原文连续给出了外呼分配、内呼入队、速度阈值、停靠协议和队列更新逻辑，能稳定组织成 EFSM。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract 与 Introduction，`paper_content.txt` 第 12-17、47-56 行
> This paper presents the development of a control and monitoring system for elevators in a building based on Programmable Logic Controller (PLC) ... The results of the programmable PLC technology solutions in one hundred and three-story elevator control are discussed.
>
> This paper presents a project based on Micro850 PLC ... to control and monitoring in real time the competition among three elevators in a building with 103 floors ... Any of three elevators should be able to pick a passenger, however, the decision of which will do it should be a result of a competition among the elevators and the efficiency is considered to support the decision.

#### 摘录 B

- 出处：第 2-3 页，`4.1 Calling from outside the elevator`，`paper_content.txt` 第 172-200、205-209 行
> The programming of the elevator system was divided into 3 sections: (1) when somebody calls the elevator from outside the system needs to determine which elevator should pick the person up based on the floor called and the desired direction ... (3) it is structured how the elevator should operate, its speed, when to stop, where to go, open the door, close the doors ...
>
> Each elevator has its own queue of floors where it needs to go and the direction to where the person that called wants to go. Thus, each elevator calculates based on its own queue the time it will take to reach that call, the one with the lowest time is the selected one to respond to it.
>
> After the attendance time of all three elevators are estimated, the called floor is assigned to the elevator with the lowest attendance time.

#### 摘录 C

- 出处：第 3-4 页，`4.2 Calling from inside the elevator` 与 `4.3 Elevator Functions`，`paper_content.txt` 第 247-305、325-327 行
> In case the queue is empty, the desired floor is allocated as first ... the challenge of this task is to identify where to allocate the desired floor in the elevator queue ... the actual position of the elevator, the direction in which the elevator is moving and to which floor the person wants to go.
>
> The elevator structure has the objective of controlling the motor as necessary ... it is verified if the floor is above its current position or below and then the flag of its direction is set. Also, is verified the distance between the destination and starting point to determine the maximum speed the elevator will travel.
>
> While the motor is operating, the elevator keeps updating its current position ... When a certain threshold for the distance is reached the stop protocol begins ... After stopping on the desired floor, the motor is put on hold until the opening and closing time of the door is past and the present floor is removed from the queue. If the queue is empty the direction of the elevator is set to zero ...
>
> Maximum speed below 20 floors: 3m/s ... Maximum speed above 20 floors: 5m/s ... Time for opening and closing doors: 6s

#### 摘录 D

- 出处：第 4-5 页，`5.2 Results of Field Trials`，`paper_content.txt` 第 363-368、392-399 行
> As expected, the elevator queue put all floor called with the same direction as the first call with higher priority and taking into account their disposition. As for the calls with the opposite calling direction, they were allocated at the decrescent order, as the direction is downward ...
>
> As expected, the second calling was attributed to the Elevator 2 because of the time Elevator 1 had to stay waiting for the closing and opening of the doors. As the calling direction was different, the Floor 5 went to the Elevator 3, because it had to be the last call in all elevators queue ...

### 2. 基于原文整理后的自然语言描述

The proposed elevator system is a PLC-and-SCADA controller for three competing elevators in a `103`-floor building rather than a single-car demo, and each car maintains its own queue together with the travel direction associated with each pending call. For an outside hall call, every elevator estimates the service time from its current queue, current position, direction, pending stops, and door-operation overhead, and the hall call is assigned to the elevator with the lowest attendance time. For an inside-car request, the controller inserts the requested floor into the existing queue according to the current motion direction and relative floor ordering instead of always appending it blindly. Once a floor is assigned, the car sets its travel direction, selects `3 m/s` for trips below `20` floors or `5 m/s` for trips of `20` floors or more, decelerates with a stop protocol as the remaining distance falls below a threshold, holds on the destination floor through the `6 s` door opening/closing interval, removes the served floor from the queue, and returns to zero-direction idle only when the queue becomes empty.

### 3. 逐句溯源

1. 句子 1：The proposed elevator system is a PLC-and-SCADA controller for three competing elevators in a `103`-floor building rather than a single-car demo, and each car maintains its own queue together with the travel direction associated with each pending call.
   对应摘录：A, B
2. 句子 2：For an outside hall call, every elevator estimates the service time from its current queue, current position, direction, pending stops, and door-operation overhead, and the hall call is assigned to the elevator with the lowest attendance time.
   对应摘录：B, D
3. 句子 3：For an inside-car request, the controller inserts the requested floor into the existing queue according to the current motion direction and relative floor ordering instead of always appending it blindly.
   对应摘录：C
4. 句子 4：Once a floor is assigned, the car sets its travel direction, selects `3 m/s` for trips below `20` floors or `5 m/s` for trips of `20` floors or more, decelerates with a stop protocol as the remaining distance falls below a threshold, holds on the destination floor through the `6 s` door opening/closing interval, removes the served floor from the queue, and returns to zero-direction idle only when the queue becomes empty.
   对应摘录：C
