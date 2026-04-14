# Synthesis of Controller for Railway–Level Crossing Devices Using Petri Nets and State Machine - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文先把道口 warning / closing / opening 过程写成带 `8 s`、`6 s` 和 `30-90 s` lead time 的控制链，再用 simple time Petri net 和四状态 state machine 实现，控制主链和恢复链都比较完整。

## 条目 1: Four-state timed railway crossing controller

- 控制对象：轨道交通与铁路控制领域的四状态定时铁路道口控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个自动铁路平交道口控制器，用 approach-section 传感器、危险区退出检测和定时延迟组织 waiting / closing / maintenance / opening 四个控制状态。
- 判断：算。对象是实际铁路道口门控控制器，原文不只给 Petri net 理论，而是明确写出 warning 触发、`8 s` 降栏、`6 s` 抬栏、预警时间和四状态控制图。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6-7 页，`3.1 Warning users of roads`，`paper_content.txt` 第 163-183 行
> rail vehicle approaching the crossing ... will launch controller ... resulting in the inclusion of red light on the road signals and turning on sirens sound signal,
>
> after 8 seconds' delay, electric drives that leave the bars dams are activated,
>
> ... closure of the dams in the horizontal position ...
>
> if during the warning process a rail vehicle on the second track is detected, the closure process will be continued.
>
> after max. 6 seconds from the exit of the rail vehicle from the sensor track of the crossing danger zone, lights on the road signalling are switched off and lifting of bars dams begins ...

#### 摘录 B

- 出处：第 7 页，`3.1 Warning users of roads`，`paper_content.txt` 第 184-201 行
> starting the warning process and closing the crossing must be performed with the appropriate lead time.
>
> t0 = tn + tzp + t0p
>
> ... cannot be less than 30 s ... no more than 90 seconds.

#### 摘录 C

- 出处：第 8-9 页，`5. Simple time Petri net of automation crossing devices`，`paper_content.txt` 第 223-249 行
> a simple time net for these devices is developed. This net highlights two fundamental processes: the process of moving the rail vehicle and the control-supervising process of automation railway crossing devices.
>
> p7 – message "close" crossing devices ... p9 – status of crossing devices is "close" ... p14 – message "open" crossing devices ... p16 – status of crossing devices is "open"
>
> TM12 – making process of closing ... TM14 – making process of opening ... appropriate static times are assigned.

#### 摘录 D

- 出处：第 10 页，`6. State machine diagram of the controller`，`paper_content.txt` 第 253-274 行
> The state diagram ... takes the following four states:
> waiting,
> closing,
> maintenance,
> opening.

### 2. 基于原文整理后的自然语言描述

The controller starts its warning sequence when the train enters the approach section: it activates road red lights and the siren, waits `8 s`, and then commands the barrier drives to lower the gates, with closure verified when the barriers reach the horizontal position. The reopening chain is equally explicit: after the train exits the danger zone, the system waits at most `6 s`, switches off the road-warning lights, and begins lifting the barriers until the vertical position is verified. The warning lead time is not arbitrary, because the paper defines a pre-warning variable `t0 = tn + tzp + t0p` and constrains it to the engineering range `30 s < t0 < 90 s`. Under the hood, the controller is modeled with a simple time Petri net that separates train motion from control supervision and uses explicit close/open message and status places, while the executable controller state machine reduces this behavior to four states: `waiting`, `closing`, `maintenance`, and `opening`. The paper also preserves an exception-style continuation rule, namely that if a rail vehicle on the second track is detected during warning, the closure process continues rather than reopening the crossing.

### 3. 逐句溯源

1. 句子 1：The controller starts its warning sequence when the train enters the approach section: it activates road red lights and the siren, waits `8 s`, and then commands the barrier drives to lower the gates, with closure verified when the barriers reach the horizontal position.
   对应摘录：A
2. 句子 2：The reopening chain is equally explicit: after the train exits the danger zone, the system waits at most `6 s`, switches off the road-warning lights, and begins lifting the barriers until the vertical position is verified.
   对应摘录：A
3. 句子 3：The warning lead time is not arbitrary, because the paper defines a pre-warning variable `t0 = tn + tzp + t0p` and constrains it to the engineering range `30 s < t0 < 90 s`.
   对应摘录：B
4. 句子 4：Under the hood, the controller is modeled with a simple time Petri net that separates train motion from control supervision and uses explicit close/open message and status places, while the executable controller state machine reduces this behavior to four states: `waiting`, `closing`, `maintenance`, and `opening`.
   对应摘录：C, D
5. 句子 5：The paper also preserves an exception-style continuation rule, namely that if a rail vehicle on the second track is detected during warning, the closure process continues rather than reopening the crossing.
   对应摘录：A
