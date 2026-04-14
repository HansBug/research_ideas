# Design an Intelligent Traffic Light Controller - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四路口交通灯的九状态基础灯序、空路缩短、特殊道路请求抢占和拥堵延绿都写成了可直接复原的控制链，足以形成双 A 样本。

## 条目 1: Nine-State Traffic-Light FSM with Sensor, Priority, and Load Extensions

- 控制对象：道路交通信号领域的四路口交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 FPGA/VHDL 的四路口交通灯控制器，负责管理基础灯序、空路缩短、特殊道路请求抢占和拥堵道路延绿。
- 判断：算。对象是真实路口信号控制器，原文明确给出九个基础状态、对应灯色输出、`5 s / 60 s / 59 s` 等时间条件，以及 motion sensor、special request 和 loaded road 三类增强 guard。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3 页，`2.1 Regular Traffic Light Controller Design / Table 1`，`paper_content.txt` 第 86-110 行
> Designing with VHDL provides the ability to use state machine to implement complex algorithms.
>
> Within the state machine the design is executed by jumping from one state to another for finite number of states. The regular controller has been designed with nine states as shown in Table 1.
>
> Traffic 4 Traffic 3 Traffic 2 Traffic 1 Description State Code state
> Yellow Yellow Yellow Yellow All Standby STANDBY 0
> Red Red Red Green Traffic 1 Green ONE_G 1
> Red Red Red Yellow Traffic 1 Yellow ONE_Y 2
> Red Red Green Red Traffic 2 Green TWO_G 3
> Red Red Yellow Red Traffic 2 Yellow TWO_Y 4
> Red Green Red Red Traffic 3 Green THREE_G 5
> Red Yellow Red Red Traffic 3 Yellow THREE_Y 6
> Green Red Red Red Traffic 4 Green FOUR_G 7
> Yellow Red Red Red Traffic 4 yellow FOUR_Y 8

#### 摘录 B

- 出处：第 5 页，`2.2.1 Using Motion Sensor / 2.2.2 Request for a Special Road`，`paper_content.txt` 第 165-181 行
> The motion sensor is functioning continuously by giving a logic '1' when there are no vehicles, and logic '0' when there are vehicles present. After the traffic light-1 became green and the cars start in moving the motion sensor checks whether the road is vacant or used by the vehicles. If there are no cars on the road, the sensor gives logic '0' to indicate the light-1 to change from green to yellow which takes five seconds, then from yellow to traffic-2 green.
>
> When the traffic light at any road is green and the controller receives a special request from any other road, it will directly turning the current road light from green to yellow. Then it jumps to the requested line by turning the light to green.

#### 摘录 C

- 出处：第 6 页，`2.2.3 Loaded Road Request`，`paper_content.txt` 第 207-230 行
> In this approach, a special sensor is places away from traffic light (let’s say fifty meters away from the TLC on that road). If the time of the green phase in any road is end, but it is still loaded with so many cars, the sensor indicates that to the controller to display the green light for another time period. Consequently, the traffic light reduces the load on that road.
>
> (ONE_LOADED = 1' & WAIT_TIME =59S) & COUT_L<=1
> (TWO_LOADED = 1' & WAIT_TIME =59S) & COUT_L<=1

### 2. 基于原文整理后的自然语言描述

The intelligent traffic-light controller is implemented as a VHDL state machine for a four-road intersection, and its regular operating cycle is organized into nine named states from `STANDBY` through `ONE_G / ONE_Y / TWO_G / TWO_Y / THREE_G / THREE_Y / FOUR_G / FOUR_Y`. In the base sequence each state maps directly to a complete red-yellow-green output pattern for the four approaches, so the controller has an explicit phase table rather than only an informal timing description. The motion-sensor extension observes whether the currently served road is vacant and, if the road becomes empty, forces the active green phase to change to yellow for `5` seconds and then hands control to the next road. On top of that base cycle, the controller can preempt the current green phase for a special-road request and can keep a heavily loaded road green for another period when the load sensor is active near the end of the phase around `59` seconds.

### 3. 逐句溯源

1. 句子 1：The intelligent traffic-light controller is implemented as a VHDL state machine for a four-road intersection, and its regular operating cycle is organized into nine named states from `STANDBY` through `ONE_G / ONE_Y / TWO_G / TWO_Y / THREE_G / THREE_Y / FOUR_G / FOUR_Y`.
   对应摘录：A
2. 句子 2：In the base sequence each state maps directly to a complete red-yellow-green output pattern for the four approaches, so the controller has an explicit phase table rather than only an informal timing description.
   对应摘录：A
3. 句子 3：The motion-sensor extension observes whether the currently served road is vacant and, if the road becomes empty, forces the active green phase to change to yellow for `5` seconds and then hands control to the next road.
   对应摘录：B
4. 句子 4：On top of that base cycle, the controller can preempt the current green phase for a special-road request and can keep a heavily loaded road green for another period when the load sensor is active near the end of the phase around `59` seconds.
   对应摘录：B, C
