# Intelligent Traffic Light Based on PLC Control - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三种工作模式、峰值/常规检测周期、流量比判断和倒计时闪烁都写成了可追溯的 PLC 交通灯控制链。

## 条目 1: Peak-Adaptive Day-Night Traffic Signal Supervisor

- 控制对象：道路交通信号控制领域的四路口峰时自适应交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 PLC 的交通灯监督控制器，用内部时钟和流量计数结果在智能、常规和夜间模式之间切换，并据此决定不同方向的绿灯时长和倒计时提醒。
- 判断：算。对象是实际交通信号控制系统，原文明确给出模式集合、流量检测周期、基于计数器比值的绿灯分配规则，以及末 3 秒闪烁倒计时。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`2. Function Description / 3. Design ideas`，`paper_content.txt` 第 71-96 行
> On the basis of the original signal light, it is optimized to use direct line and left-turn sections, while adding countdown alarm and flashing warning.
>
> The work mode is divided into intelligent working mode, routine work mode and night work mode.
>
> the signal acquisition frequency is set in the peak segment for every 10 minutes. The normal segment is a cycle every 20 minutes ... In the evening, the sensor module stops working, and the traffic light realizes the signal output of traffic lights and the countdown display function in the night working mode.

#### 摘录 B

- 出处：第 5 页，`5.1 main program design / 5.3 Countdown program design`，`paper_content.txt` 第 148-169 行
> In a vehicle testing cycle ... C1 and C2 flow, calculating the ratio of the relationship ... if AC4 integer value is greater than 1 ... set the AC show green light time to 33 s, finally to the countdown 3 s flashing reminder.
>
> If the total value of AC4 is zero, then the AC is less than BD to the traffic flow, and the AC to the green signal time is 13s ... Red light show time for 33 s, BD to red light show time for 13 s, green light shows that time is 33 s.
>
> Respectively set two groups countdown digital display ... green light left bottom 3 s ... digital tube display by multiple combination to realize the countdown timer function.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller separates operation into `intelligent`, `routine`, and `night` modes according to the PLC internal clock and the current time period. During daytime operation it samples traffic flow every `10` minutes in peak periods and every `20` minutes in normal periods, then selects the control mode that should govern the next signal cycle. In intelligent mode the PLC compares the AC-side and BD-side vehicle counters and uses their ratio to choose the green duration: when the AC-side ratio exceeds the configured threshold, AC receives `33 s` of green; otherwise AC receives `13 s` and BD keeps the longer green phase. In both cases the active green phase ends with a `3 s` flashing countdown reminder, while night mode disables the sensing branch and keeps only timed signal output plus countdown display.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller separates operation into `intelligent`, `routine`, and `night` modes according to the PLC internal clock and the current time period.
   对应摘录：A
2. 句子 2：During daytime operation it samples traffic flow every `10` minutes in peak periods and every `20` minutes in normal periods, then selects the control mode that should govern the next signal cycle.
   对应摘录：A
3. 句子 3：In intelligent mode the PLC compares the AC-side and BD-side vehicle counters and uses their ratio to choose the green duration: when the AC-side ratio exceeds the configured threshold, AC receives `33 s` of green; otherwise AC receives `13 s` and BD keeps the longer green phase.
   对应摘录：B
4. 句子 4：In both cases the active green phase ends with a `3 s` flashing countdown reminder, while night mode disables the sensing branch and keeps only timed signal output plus countdown display.
   对应摘录：A, B
