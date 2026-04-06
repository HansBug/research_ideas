# Synthesis & Simulation Model of Parallel Lift Controller Using Verilog - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（局部工程定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三梯并行调度、最近梯选择、门控开闭计时和障碍保持开门逻辑写成了明确的 controller flow，虽然是短文，但输入、寄存器、定时与服务闭环都够支撑双 A。

## 条目 1: Nearest-Elevator Dispatch and Door-Timer Controller

- 控制对象：楼宇机电与电梯控制领域的三梯并行调度与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（局部工程定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向八层建筑三部并行电梯的主控制器，用 `idle acknowledgement -> hall-call registration -> nearest-elevator dispatch -> door-timed service -> idle reset` 这条链组织调度与门控。
- 判断：算。对象是真实电梯调度控制器，原文不只讲 HDL 设计，而是明确给出三梯并行、最近梯优先、楼层/目的层寄存器、门控定时和障碍保持开门这几项核心控制逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 11-22 行
> To do that, a Three-Lift Controller is modeled. In the proposed design a VERILOG RTL code is developed to control the lift movement based on the request it will get. For that a finite state machine is developed to know from which state to state the controller is changing based on the requests from the end user ... the real-time three-lift controller will be modeled with Verilog HDL code using Finite-State machine (FSM) model.

#### 摘录 B

- 出处：第 1-2 页，Principle of Elevator Controller，`paper_content.txt` 第 49-69 行、第 61-65 行
> Elevator controller is an elementary system consisting of elevator serving 8 floors ... The floors also have call buttons to call for the service of the elevator system.
>
> Two timers, one for the elevator's moving up or down, and the other as a time delay before opening/closing the door.
>
> When you press a floor button ... clock 2 counts from 3 to 0 before the door closes and moves to the desired floor ... After reaching the desired floor, counter 2 counts from 3 to 0 again before the door opens.
>
> If an obstruction is detected when door is about to close, it remains open.

#### 摘录 C

- 出处：第 2 页，Section 3 `STATE FLOW`，`paper_content.txt` 第 77-88 行
> Elevator Idling Block: Three parallel elevator are signalling continuously signal acknowledge to the driver controller. At reset or after completion of task by each elevator, each of them will acknowledge an idle signal to controller.
>
> User Signal Request Call: ... signal request is send to controller ... Depending upon current status of all three elevators, the elevator nearer to user input floor will act, and controller passes it control to that elevator. Rest of two elevators will have low priority and only the nearest elevator to user will assign the highest priority.

#### 摘录 D

- 出处：第 3 页，Section 3 `User Activated Block`，`paper_content.txt` 第 96-107 行
> The status register related to user floor will update on each floor checking about the floor from where the call has made.
>
> Acknowledging the user in floor, elevator stops and idle state goes active. Control system drives the door motor, hence opening operation is performed. Door barrier sensors and door opening/closing time is regulated by clock circuit used in our Verilog code.
>
> User will update the request final floor from inside the elevator; this will update the final requested floor register ... control system will close the door and ... do analysis about the direction and destination floor.
>
> On reaching to its final floor, elevator stops and current status register of elevator resets to idle state. Control system opens the door, thus user exits.

### 2. 基于原文整理后的自然语言描述

The paper describes a three-lift master controller that manages hall calls, elevator selection, motion, and door service as a single extended state machine rather than as isolated hardware blocks. Each elevator repeatedly acknowledges an `idle` condition to the controller at reset or after task completion; when a hall-call request arrives, the request is stored and the controller chooses the nearest elevator, assigning it the highest priority while the other two cars remain lower-priority alternatives. Once activated, the selected elevator travels toward the caller floor, updates the user-floor status register floor by floor, and stops to open the door when it reaches the pickup location. Door handling is explicitly time-governed: one clock regulates movement, another clock delays door closing and door opening, and if an obstruction is detected when the door is about to close, the controller keeps the door open. After the passenger enters a destination floor, the controller writes the final-floor register, computes direction and destination, closes the door, serves the trip, and finally resets the elevator back to `idle` when the passenger exits.

### 3. 逐句溯源

1. 句子 1：The paper describes a three-lift master controller that manages hall calls, elevator selection, motion, and door service as a single extended state machine rather than as isolated hardware blocks.
   对应摘录：A, B
2. 句子 2：Each elevator repeatedly acknowledges an `idle` condition to the controller at reset or after task completion; when a hall-call request arrives, the request is stored and the controller chooses the nearest elevator, assigning it the highest priority while the other two cars remain lower-priority alternatives.
   对应摘录：C
3. 句子 3：Once activated, the selected elevator travels toward the caller floor, updates the user-floor status register floor by floor, and stops to open the door when it reaches the pickup location.
   对应摘录：D
4. 句子 4：Door handling is explicitly time-governed: one clock regulates movement, another clock delays door closing and door opening, and if an obstruction is detected when the door is about to close, the controller keeps the door open.
   对应摘录：B, D
5. 句子 5：After the passenger enters a destination floor, the controller writes the final-floor register, computes direction and destination, closes the door, serves the trip, and finally resets the elevator back to `idle` when the passenger exits.
   对应摘录：D
