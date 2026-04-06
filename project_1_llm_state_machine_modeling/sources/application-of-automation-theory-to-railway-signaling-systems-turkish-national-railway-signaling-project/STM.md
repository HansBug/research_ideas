# The Application of Automation Theory to Railway Signaling Systems: The Turkish National Railway Signaling Project - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：资源互斥, 显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然用 Petri net 表达组件模型，但 route request、signal aspect、switch lock 和 `7 s` 超时错误链都足够明确，可以稳定抽成带定时 guard 的铁路联锁样本。

## 条目 1: Route-request and seven-second switch-locking controller

- 控制对象：土耳其铁路联锁系统中的进路请求与道岔锁闭控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：资源互斥, 显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个铁路联锁控制器，用 `TCC` 路由请求、道岔位置、信号灯色和轨道占用条件决定进路是否建立，并在道岔超时不到位时进入错误状态。
- 判断：算。对象是实际铁路信号/联锁系统中的主控制链，原文给出了请求接受/拒绝、特定 route 的 guard 条件、道岔 normal/reverse 位置以及 `7 s` 超时转错误的明确规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`2.2 The Interlocking System / 2.3 Signals / 2.4 Switches / 2.6 Level Crossing`，`paper_content.txt` 第 153-159, 169-179, 187-215 行
> The interlocking system can be considered as decision-making software because it checks the incoming requests from the TCC and compares these requests with the actual situation of the railway field equipments. An incoming request is accepted, if all safety criteria are met, or rejected if there are any conflicts or the request is improper.
>
> Red color means that the next block is occupied, so the train must stop. Yellow color means that the next block is free but not the block after that ... Green color means at least the next two blocks are free ...
>
> Switches have two location indications named normal and reverse. In case of a route request or a manual request from the TCC, switches are controlled by the interlocking system.
>
> Normally when there is no route reservation or route request, the interlocking system send inactive signal to level crossing barriers to keep it open and allow road traffic. After a route reservation ... to close the barriers of the level crossing and to activate the flashing red lights ...

#### 摘录 B

- 出处：第 4 页，`interlocking table` 说明，`paper_content.txt` 第 426-435 行
> Some of the possible route requests (e.g. 001DT-1ST, 001DT-2ST), related signal colors with these possible route requests and the required conditions of the other railway field components (to be able to reserve the route) are defined in this table. For example, if route 001DT-2ST is requested switches 51, 53 and 55 have to be in normal position, signals 52DB, 52DA have to be red and entrance signal of this route 52B can be green (if the next signal 2BA is yellow), yellow (if the next signal 2BA is red) or yellow-red (if the block 2ST is occupied by another train).

#### 摘录 C

- 出处：第 4-5 页，`4.2 Modeling of the Railway Field Components`，`paper_content.txt` 第 527-549, 619-636 行
> Since the routes given in Figure 7 intersect with each other, only one route reservation can be made in order to prevent collisions. More than one route reservation can be made when there is no intersection between the routes.
>
> At the beginning, switches are assumed to be on initial position (P5). After an incoming position command or a route request from TCC, switch moves to the desired position (normal or reverse) and stays there until a new position command or route request is received (the interlocking software locks the switch electronically). If the switch did not reach to desired position in a predetermined time, which is assumed as 7 sec for Turkish State Railways, it is considered as an error and the token moves to place PE.
>
> Railway track circuits are modeled just single places with one input and one output because only one train can occupy a track circuit at the same time ... the interlocking system counts the entrance and the exit of trains onto track circuits which also allows detecting unexpected occupation of track circuits.

### 2. 基于原文整理后的自然语言描述

The Turkish railway interlocking is the decision-making software between the `TCC` and the field equipment: it receives route or manual switch requests, compares them with the current state of switches, signals, track circuits, and level-crossing devices, and accepts the request only if all safety criteria are satisfied. For the example route `001DT-2ST`, the controller requires switches `51`, `53`, and `55` to be in `normal`, signals `52DB` and `52DA` to stay red, and then chooses the entrance signal `52B` aspect according to the next signal and the occupancy of block `2ST`. Intersecting routes are mutually exclusive, so only one conflicting reservation may be active at a time, while track circuits also enforce the fact that only one train may occupy a section. At the switch level, each point starts from its initial position, moves to `normal` or `reverse` after a route or manual command, and is electronically locked there until a new command arrives. If the commanded switch does not reach the desired position within `7 s`, the controller enters an error condition by moving the token to place `PE`, which makes the route-establishment chain explicitly time-guarded rather than purely combinational.

### 3. 逐句溯源

1. 句子 1：The Turkish railway interlocking is the decision-making software between the `TCC` and the field equipment: it receives route or manual switch requests, compares them with the current state of switches, signals, track circuits, and level-crossing devices, and accepts the request only if all safety criteria are satisfied.
   对应摘录：A
2. 句子 2：For the example route `001DT-2ST`, the controller requires switches `51`, `53`, and `55` to be in `normal`, signals `52DB` and `52DA` to stay red, and then chooses the entrance signal `52B` aspect according to the next signal and the occupancy of block `2ST`.
   对应摘录：B
3. 句子 3：Intersecting routes are mutually exclusive, so only one conflicting reservation may be active at a time, while track circuits also enforce the fact that only one train may occupy a section.
   对应摘录：C
4. 句子 4：At the switch level, each point starts from its initial position, moves to `normal` or `reverse` after a route or manual command, and is electronically locked there until a new command arrives.
   对应摘录：A, C
5. 句子 5：If the commanded switch does not reach the desired position within `7 s`, the controller enters an error condition by moving the token to place `PE`, which makes the route-establishment chain explicitly time-guarded rather than purely combinational.
   对应摘录：C
