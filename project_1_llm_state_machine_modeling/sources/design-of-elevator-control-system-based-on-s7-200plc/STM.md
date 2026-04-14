# Design of Elevator Control System Based on S7-200PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文对四层电梯的楼层请求、请求灯点亮、到层触发、`3 s` 开门延时与 `6 s` 关门等待链写得完整，可直接形成双 A 电梯控制样本。

## 条目 1: Four-floor request-light and door-delay elevator controller

- 控制对象：四层 S7-200 PLC 电梯的请求响应与门控控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个四层电梯 PLC 控制器，用楼层按钮、楼层到位输入、内部继电器和定时器实现请求灯点亮、到层开门、等待和关门离层。
- 判断：算。对象是实际电梯控制系统，原文明确给出输入点 `I1.1 / I1.0 / I0.2`、内部位 `M2.1 / M2.2 / M5.0`、输出 `Q1.1 / Q1.2 / Q0.4 / Q0.5` 与 `T37 / T38` 定时链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1-2 页，Abstract / Introduction，`paper_content.txt` 第 15-18 行、第 35-43 行
> This design develops a four-floor elevator control system based on S7-200PLC. It realizes the following functions: the second and third floors support both upward and downward request functions ... the elevator automatically opens its door after arriving at each floor and closes the door automatically 6 seconds later.
>
> This paper designs a four-floor elevator control system based on the S7-200 PLC ... including the accurate indication of indicator lights when arriving at each floor, the realization of the up and down request functions ... and the function of opening the door for 6 seconds and then automatically closing it.

#### 摘录 B

- 出处：第 4 页，`4.2. Ladder diagram design for partial functions`，`paper_content.txt` 第 119-134 行
> (1) 2nd floor up request signal: When the up button on the 2nd floor is pressed, the normally open contact I1.1 closes, and M2.2 outputs 1 ... Q1.1 to output 1, that is, the 2nd floor up signal light is on.
>
> (2) 2nd floor down request signal: When the down button on the 2nd floor is pressed, the normally open contact I1.0 closes, and M2.1 outputs 1 ... Q1.2 to output 1, that is, the 2nd floor down signal light is on.
>
> (3) 2nd floor arrival signal: When the elevator arrives at the 2nd floor, the normally open contact I0.2 closes ... Timer T37 starts timing for 3 seconds ... Q0.4 outputs 1, indicating that the elevator door opens. At the same time, timer T38 starts timing for the door opening. After 6 seconds ... Q0.4 outputs 0 ... and Q0.5 outputs 1.

#### 摘录 C

- 出处：第 5-6 页，`5. System function test / 6. Conclusion`，`paper_content.txt` 第 141-157 行
> The main function to be verified is whether the elevator can successfully arrive at the current floor and open/close its doors after an up/down request is issued from that floor.
>
> When a passenger sends an upward or downward request on a certain floor, the elevator can successfully arrive at that floor, automatically open the elevator door after 3 seconds, and automatically close the elevator door after 6 seconds.

### 2. 基于原文整理后的自然语言描述

The four-floor elevator controller accepts directional requests from floor buttons and latches the corresponding request lamps through internal memory bits such as `M2.2` and `M2.1`. When the car reaches the requested floor, the floor-arrival input closes, the controller checks that the matching request is active, and then starts a `3 s` timer before opening the door on `Q0.4`. Once the door has opened, a second timer keeps the door-open phase active for `6 s`, after which the controller turns `Q0.4` off and drives the leave-floor output on `Q0.5`. The paper therefore gives a complete request-arrival-open-wait-close-depart sequence with explicit PLC inputs, internal bits, outputs, and timer guards.

### 3. 逐句溯源

1. 句子 1：The four-floor elevator controller accepts directional requests from floor buttons and latches the corresponding request lamps through internal memory bits such as `M2.2` and `M2.1`.
   对应摘录：A, B
2. 句子 2：When the car reaches the requested floor, the floor-arrival input closes, the controller checks that the matching request is active, and then starts a `3 s` timer before opening the door on `Q0.4`.
   对应摘录：B, C
3. 句子 3：Once the door has opened, a second timer keeps the door-open phase active for `6 s`, after which the controller turns `Q0.4` off and drives the leave-floor output on `Q0.5`.
   对应摘录：A, B, C
4. 句子 4：The paper therefore gives a complete request-arrival-open-wait-close-depart sequence with explicit PLC inputs, internal bits, outputs, and timer guards.
   对应摘录：A, B, C
