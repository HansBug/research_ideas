# Design & Construction of A Closed Loop Traffic Light Control System - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三路口闭环交通灯的车道检测、优先 token 分配、倒计时显示和“无车提前让出相位”写成了完整的感知-配时-切换控制链。

## 条目 1: Lane-Priority Token Traffic Light Controller
- 控制对象：道路交通信号控制领域的闭环车道优先交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向三路口的闭环交通灯控制器，利用红外反馈感知各车道车辆数量，为当前有车道分配通行 token、驱动倒计时显示，并在车道变空时提前终止该相位。
- 判断：算。对象是明确的交通信号控制系统，原文同时给出了反馈传感、车道优先、time slot、token termination 和显示/信号输出链，足以整理成 `EFSM + T1` 样本。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Introduction
> A closed loop traffic light control system is an intelligent traffic light control that gives priority to lanes that has got more traffic without waiting other lanes endlessly.

#### 摘录 B
- 出处：第 6-8 页，Traffic Movement Feedback / Microcontroller Unit / Driver
> This section comprise of set of infrared transceiver circuit which is meant to sense the presence of vehicle at the lanes and feed the information back to the microcontroller in form of switching action.
>
> It takes the informations from the feedback section, determines the time for each lane, controls the lane and as well drives the time display.
>
> The driver software ... determines what the microcontroller must do. This ranges from sensing and analysing the feedbacks, controlling the traffic light, setting the time for lane passage, terminating and allowing token when necessary, the conversion of time into seven segment displayable format and the driving of the seven segment display.

#### 摘录 C
- 出处：第 8-9 页，Result Discussion
> For each token given to a lane, the last countdown time before the token is terminated indicates the extra time gain to allow other lane a token since this time would have been wasted for non-availability of vehicles in the lane with the token.
>
> The feedback system senses non-availability of vehicles and terminates the token for other lanes. A lane would be allowed all the token only if there is much vehicles to consume all the time.

### 2. 基于原文整理后的自然语言描述

The closed-loop traffic-light controller continuously monitors each lane through infrared feedback circuits and sends the detection result to a microcontroller. The microcontroller allocates a passage token to one lane at a time, computes the corresponding countdown duration, drives the red/yellow/green lamps, and updates the seven-segment time display for the active lane. If the feedback shows that the currently served lane has no remaining vehicles, the controller terminates that token early and reassigns the saved time to another waiting lane instead of consuming the full default slot. Only when a lane still has enough vehicles to use the whole countdown does the controller keep the full token until the timer expires. This makes the control chain an input-driven and timer-governed lane-priority traffic-signal EFSM rather than a fixed open-loop phase rotator.

### 3. 逐句溯源

1. 句子 1：The closed-loop traffic-light controller continuously monitors each lane through infrared feedback circuits and sends the detection result to a microcontroller.
   对应摘录：B
2. 句子 2：The microcontroller allocates a passage token to one lane at a time, computes the corresponding countdown duration, drives the red/yellow/green lamps, and updates the seven-segment time display for the active lane.
   对应摘录：B
3. 句子 3：If the feedback shows that the currently served lane has no remaining vehicles, the controller terminates that token early and reassigns the saved time to another waiting lane instead of consuming the full default slot.
   对应摘录：A, C
4. 句子 4：Only when a lane still has enough vehicles to use the whole countdown does the controller keep the full token until the timer expires.
   对应摘录：C
5. 句子 5：This makes the control chain an input-driven and timer-governed lane-priority traffic-signal EFSM rather than a fixed open-loop phase rotator.
   对应摘录：A, B, C
