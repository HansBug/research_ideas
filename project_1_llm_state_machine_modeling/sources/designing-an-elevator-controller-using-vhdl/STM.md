# Designing an Elevator Controller Using VHDL - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了四层电梯控制器的输入总线、方向与门控输出、`STOP_UP/GOING_UP/CONT_UP/STOP_DN/GOING_DN/CONT_DN` 六个状态以及多组请求场景，足以构成双 A 的 `🏢` 样本。

## 条目 1: Four-Storey Request-Serving Elevator FSM

- 控制对象：楼宇机电与电梯控制领域的四层电梯请求服务控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向四层建筑的电梯控制器，用楼层位置、楼层请求和上下行请求驱动电机方向、运行使能和门开闭，并通过六个离散状态管理上下行服务。
- 判断：算。对象是真实电梯控制器，原文不只是泛讲 VHDL 建模，而是明确列出了输入输出信号、六个状态名和多个请求场景下的状态迁移链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-24 行
> This project aims to design an elevator controller for a four-storey building ... The controller has 4 bus inputs ... CUR_FLR to indicate the current floor ... REQ_FLR ... REQ_UP and REQ_DN ... There are outputs to run and direct the elevator's motor.

#### 摘录 B

- 出处：第 7 页，`Fig 3 / Fig 4 / Fig 5`，`paper_content.txt` 第 262-273 行
> The elevator's car at the Ground Floor ... with no requests. Stays at the current floor (State=STOP_UP).
>
> ... request to exit at First Floor ... Start at STOP_UP then GOING_UP then STOP_UP again when it reaches the requested floor.
>
> Request to the Second Floor ... Starts at STOP_UP then GOING_UP then CONT_UP then STOP_UP again when it reached the requested floor ...

#### 摘录 C

- 出处：第 8-9 页，`Fig 7 / Fig 8 / Fig 9`，`paper_content.txt` 第 288-319 行
> Starts at STOP_UP goes all the way through GOING_UP and CONT_UP to stop at the requested floor (Third Floor 1000) ... then ... pressed the up button at the Ground Floor. The elevator goes down to the ground floor ... it changes to STOP_DN then GOING_DN then CONT_DN ...
>
> ... it starts at STOP_UP then checks for requests above, moves to GOING_UP and CONT_UP to STOP_UP at requested floor then checks again for request ... If there are no requests above and there is a request below, moves to STOP_DN ...
>
> STATES
> STOP_UP  GOING_UP  CONT_UP  STOP_DN  GOING_DN  CONT_DN

#### 摘录 D

- 出处：第 9 页，`Fig 9`，`paper_content.txt` 第 310-316 行
> A request from Ground Floor to exit at Third Floor and while the elevator on the move, a request to go up at First Floor to exit at Second Floor.
>
> Ground Floor (STOP_UP) moves up (GOING_UP) stops at First Floor (STOP_UP) to pickup a passenger going up ... first request to exit at Third Floor still active and the elevator moves to GOING_UP and stops the Third Floor STOP_UP

### 2. 基于原文整理后的自然语言描述

The elevator controller for the four-storey building is modeled as a finite-state machine driven by floor-position inputs, destination requests, and up/down call requests, with outputs for motor direction, motor run, and door actuation. In the idle case, the car can remain at the current floor in `STOP_UP`, but once a request arrives above the car, the controller transitions through `GOING_UP` and, when needed for higher floors, `CONT_UP` before returning to `STOP_UP` at the served floor. Symmetrically, when there is no pending request above and a lower-floor request appears, the controller switches to `STOP_DN`, then moves through `GOING_DN` and `CONT_DN` until the lower request is served. The paper also shows that the controller can interrupt a longer upward mission to stop at an intermediate floor, pick up another passenger, and then resume serving the original upper request. Together, the six named states form a concrete service-policy FSM rather than a vague “elevator works correctly” hardware demo.

### 3. 逐句溯源

1. 句子 1：The elevator controller for the four-storey building is modeled as a finite-state machine driven by floor-position inputs, destination requests, and up/down call requests, with outputs for motor direction, motor run, and door actuation.
   对应摘录：A
2. 句子 2：In the idle case, the car can remain at the current floor in `STOP_UP`, but once a request arrives above the car, the controller transitions through `GOING_UP` and, when needed for higher floors, `CONT_UP` before returning to `STOP_UP` at the served floor.
   对应摘录：B, C
3. 句子 3：Symmetrically, when there is no pending request above and a lower-floor request appears, the controller switches to `STOP_DN`, then moves through `GOING_DN` and `CONT_DN` until the lower request is served.
   对应摘录：C
4. 句子 4：The paper also shows that the controller can interrupt a longer upward mission to stop at an intermediate floor, pick up another passenger, and then resume serving the original upper request.
   对应摘录：D
5. 句子 5：Together, the six named states form a concrete service-policy FSM rather than a vague “elevator works correctly” hardware demo.
   对应摘录：A, B, C
