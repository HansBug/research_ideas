# Advanced Traffic Signal Monitoring using Programmable Logic Controller (PLC) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四向环岛交通灯的正常轮转、行人请求、优先放行和高密度延时扩展拆成四个周期，并给出 `30 s / 10 s / 45 s` 等定时规则，足够形成 `🚦` 方向的双 A 条目。

## 条目 1: Four-Cycle Traffic Controller with Pedestrian and Priority Override

- 控制对象：道路交通信号领域的四向环岛交通灯 PLC 控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向四向环岛的 PLC 交通灯控制器，把正常轮换、行人放行、紧急优先和高密度延时扩展做成四类可切换周期。
- 判断：算。对象是真实交通灯控制系统，原文不仅明确列出四个 cycle，还把行人请求只在主绿灯结束后触发、优先模式持续到停止按钮、以及高密度场景把绿灯从 `30` 秒延长到 `45` 秒等 guard 与 timer 写得比较完整。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，`3.2 Objective`，`paper_content.txt` 第 118-145 行
> This project aims towards the development of more automated and advanced traffic monitoring system controlled by plc. Three main problems can be resolved by our project.
>
> If the waiting area of the pedestrian is empty, the traffic monitoring system will not glow the pedestrian LED and hence no hindrance in a normal cycle.
>
> Secondly in case of priority or emergency vehicles ... that lane is glowed until the vehicles pass.
>
> In such cases the time of the green light is increased for the lane in which there is traffic density.

#### 摘录 B

- 出处：第 2 页，`4.2 Working`，`paper_content.txt` 第 166-187 行
> If the number of vehicles is increased on one side, he will increase the time of the timer.
>
> In an emergency case or priority case, a police man directly pressed the start push button on the priority side, gave a green signal and all other signals would remain red until he pressed the stop push button.
>
> In case of a pedestrian cycle, this will be allowed only when a police man sees a man who doesn't cross the road ... The pedestrian signal will start only when the main signal green light is over.

#### 摘录 C

- 出处：第 3 页，`7. Simulation`，`paper_content.txt` 第 255-296 行
> In our project/system there are four cycle which are explained below: -
>
> 1. Normal Cycle: - ... the GREEN light of lane 1 will start for thirty seconds ... For transition lane 1 and lane 2 glows yellow signal for ten seconds ... After ten seconds, the green signal glows in lane 2 for thirty seconds ...
>
> 2. Pedestrian Cycle: - ... the cycle moves from a normal cycle to a pedestrian cycle for 10 seconds, and after ten seconds they will move back to a normal cycle.
>
> 3. Priority Cycle: - This cycle can disrupt or stop all other cycles ... gave a priority or green signal for that direction, until we pressed the stop priority push button ...
>
> 4. High Density Cycle: - ... it will move from 30 to 45 seconds when we press the high density push button.

#### 摘录 D

- 出处：第 3 页，`7.1 Implementation`，`paper_content.txt` 第 298-309 行
> In our program we use input push buttons, output, binary, MOV and timer. A timer is used to glow the set of sequence accordingly in time. The program is reset using the end timer to continue running. MOV is used to extend the timer time. ... Therefore, we are dividing our program into four parts/cycles.

### 2. 基于原文整理后的自然语言描述

The roundabout traffic controller is implemented as a PLC-based extended state machine with four explicit operating cycles: a normal cycle, a pedestrian cycle, a priority cycle, and a high-density cycle. In the normal cycle, each lane receives a `30` second green interval and the transition between adjacent lanes inserts a `10` second yellow phase before control moves to the next lane. Pedestrian requests do not interrupt an ongoing green immediately; instead, the controller waits until the current main green finishes, then switches to a `10` second pedestrian-only phase in which vehicle lanes remain red. Emergency or priority mode overrides every other cycle by forcing the requested lane to stay green and all others red until the operator presses the stop button, while high-density mode extends the green timer from `30` to `45` seconds for the selected approach. This is a usable `EFSM + T1` sample because the paper explicitly names the control modes, the push-button triggers, and the timer values that govern each phase transition.

### 3. 逐句溯源

1. 句子 1：The roundabout traffic controller is implemented as a PLC-based extended state machine with four explicit operating cycles: a normal cycle, a pedestrian cycle, a priority cycle, and a high-density cycle.
   对应摘录：C, D
2. 句子 2：In the normal cycle, each lane receives a `30` second green interval and the transition between adjacent lanes inserts a `10` second yellow phase before control moves to the next lane.
   对应摘录：C
3. 句子 3：Pedestrian requests do not interrupt an ongoing green immediately; instead, the controller waits until the current main green finishes, then switches to a `10` second pedestrian-only phase in which vehicle lanes remain red.
   对应摘录：B, C
4. 句子 4：Emergency or priority mode overrides every other cycle by forcing the requested lane to stay green and all others red until the operator presses the stop button, while high-density mode extends the green timer from `30` to `45` seconds for the selected approach.
   对应摘录：A, B, C
5. 句子 5：This is a usable `EFSM + T1` sample because the paper explicitly names the control modes, the push-button triggers, and the timer values that govern each phase transition.
   对应摘录：A, C, D
