# Speed Optimized Implementation for Three Lift Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：正文把双梯请求分配、开关门、20 秒停门和阻挡回开链写得很细，虽然标题写 `three lift`，但详细设计部分能稳定支撑一条 A 级电梯群控 EFSM 样本。

## 备注

- 标题与摘要多处写 `three elevator / three lift`，但第 `III` 节开始的详细设计、状态图和测试案例主要展开的是 `two elevators on two floors` 的控制链；本条按正文详细设计部分提取，不按标题字面扩展。

## 条目 1: Priority-Scheduled Dual-Elevator Door-and-Motion Controller

- 控制对象：楼宇机电领域的双梯双层请求分配、开关门与运动控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向双梯双层场景的群控电梯控制器，用优先楼层、门计时器、阻挡传感器和请求位置来分配哪台电梯开门、上行或下行。
- 判断：算。对象是实际电梯控制器及其群控逻辑，原文明确给出了控制输入、门控计时、优先规则、六状态单梯状态机和多组测试序列。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 29-37 行
> Elevator controller controls the entire operation of the three elevator system. The proximity sensors located to sense the positions of the cars, provide the current state storing it in register. The obstruction sensors provide the status of obstruction. The elevator controller also reads the requests ... If the door of any elevator is open, the timer signals from the elevator keep the controller informed of being busy. The control state machine receives all these signals. ... The FSM then generates control signals for the next position and movement of the elevators.

#### 摘录 B

- 出处：第 3 页，Section III `Designing of Elevator`，`paper_content.txt` 第 158-191 行
> The building has two elevators that move between two floors. ... Normally an elevator will move when instructed to do so by the control, opening the door for 20 second. After the waiting of 20 second the door might be closed. If any obstruction detected, the door will open. ... Elevator1 has a priority for the first floor request and the elevator2 for the request from second floor. ... the respective timer needs to be triggered to high state and the obstruction should be 0.

#### 摘录 C

- 出处：第 5-6 页，Section III-E `State Diagram`，`paper_content.txt` 第 355-424 行
> The figure 4 shows the state diagram for single elevator controller. Initially, the elevator is at its priority floor with closed doors. ... Whenever the elevator is in moving state, it does not receive any request and at the next clock cycle opens the door at the destination floor. When doors of an elevator are open, it gets closed only when the related signal has gone low, the timer out is high ... and the obstruction signal is low. ... S0 is the initial state ... Once the up button in first floor is pressed ... transition S1. ... U1 will leads to state S2 (Move from 1 to 2). After reaching second floor, elevator door should get open represented by state S3. If no obstruction and timer is set to HIGH, signal goes to close door state S4. ... D1 ... leads to moving from 2 to 1 state S5.

#### 摘录 D

- 出处：第 6-7 页，Section IV `Test Case Analysis`，`paper_content.txt` 第 502-520 行
> From the above test cases, it is observed that the elevator controller follows the principle of assigning the request to the elevator that would keep the user in wait state for lesser time. ... When obstruction is LOW and timer2 is HIGH, door should get closed (011). After closing, by pressing down button elevator2 will move from second to first floor (101) and get the door open (001) by reaching the destination.

### 2. 基于原文整理后的自然语言描述

The elevator group controller continuously reads elevator positions, request flip-flops, door-obstruction sensors, and timer signals so that it can decide which car is available and where it should move next. In the detailed design section, the concrete system is a two-elevator, two-floor controller with default priority floors: `elevator1` starts at floor 1, `elevator2` starts at floor 2, and each door closes only when its timer is high and obstruction is absent. The single-elevator core is modeled as a six-state Moore machine in which `S0` is the closed-door initial state, `S1` is first-floor open-door servicing, `S2` is upward travel, `S3` is second-floor open-door servicing, `S4` is post-service closed-door waiting, and `S5` is downward travel back to floor 1. Transitions are triggered by floor requests, internal `U1 / D1` commands, arrival at the destination floor, timer expiration, and obstruction clearance. At the group level, the controller uses both floor priority and service-time minimization: when both cars are candidates, the floor-priority rule applies, but a free nearer elevator can still take the request to reduce waiting time.

### 3. 逐句溯源

1. 句子 1：The elevator group controller continuously reads elevator positions, request flip-flops, door-obstruction sensors, and timer signals so that it can decide which car is available and where it should move next.
   对应摘录：A
2. 句子 2：In the detailed design section, the concrete system is a two-elevator, two-floor controller with default priority floors: `elevator1` starts at floor 1, `elevator2` starts at floor 2, and each door closes only when its timer is high and obstruction is absent.
   对应摘录：B, C
3. 句子 3：The single-elevator core is modeled as a six-state Moore machine in which `S0` is the closed-door initial state, `S1` is first-floor open-door servicing, `S2` is upward travel, `S3` is second-floor open-door servicing, `S4` is post-service closed-door waiting, and `S5` is downward travel back to floor 1.
   对应摘录：C
4. 句子 4：Transitions are triggered by floor requests, internal `U1 / D1` commands, arrival at the destination floor, timer expiration, and obstruction clearance.
   对应摘录：B, C
5. 句子 5：At the group level, the controller uses both floor priority and service-time minimization: when both cars are candidates, the floor-priority rule applies, but a free nearer elevator can still take the request to reduce waiting time.
   对应摘录：B, D
