# Design of a Solar Power System for a Four-Way Intersection Traffic Light Based on Time Scheduling Using PLC - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把三组时段计划、各方向精确的红黄绿配时和 PLC 梯形图中的定时器失效条件一起写成了可追溯的交通灯控制链。

## 条目 1: Time-Scheduled Solar Traffic-Light Cycle Controller

- 控制对象：道路交通信号控制领域的时段调度型四路口交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 PLC 交通灯调度控制器，用三个时段计划和各方向流量统计结果决定四路口每一相位的绿灯、黄灯和全红缓冲时长。
- 判断：算。对象是实际交通灯控制系统，原文不仅给出不同时段的配时表，还明确写了梯形图定时器、切换条件和高峰时段寄存器触发。

### 1. 原文摘录

#### 摘录 A

- 出处：第 5-6 页，`Vehicle Density for Specific Periods / Design of Time Scheduling on Traffic Lights`，`paper_content.txt` 第 387-458 行
> 1.Traffic Condition Type A (07:00–08:00) ... Southbound receives 20 seconds, Northbound 11 seconds, Eastbound 11 seconds, and Westbound 19 seconds of green light.
>
> 2.12:00–13:00: Southbound receives 16 seconds, Northbound 11 seconds, Eastbound 12 seconds, and Westbound 18 seconds.
>
> 3.16:00–17:00: Southbound receives 48 seconds, Northbound 30 seconds, Eastbound 29 seconds, and Westbound 75 seconds.
>
> 16:00–17:00 South 147 3 48 1 199 ... West 120 3 75 1 199.

#### 摘录 B

- 出处：第 6 页，`Testing the Ladder Diagram for the Traffic Light / Traffic Volume Type C Condition`，`paper_content.txt` 第 463-507 行
> Figure 3 illustrates the system state when the green light is active. ... This timer controls the duration of the green light as per the defined schedule.
>
> Once the timer T0 reaches its preset duration ... the circuit, cutting off the current flow and deactivating the green light.
>
> At 16:00, contact D102 is activated to extend the green light duration ... By 17:00, contact RTC is deactivated, and the system reverts to its default configuration.

### 2. 基于原文整理后的自然语言描述

The controller organizes the four-way intersection around three daily schedules, covering the morning period `07:00–08:00`, the normal period `12:00–13:00`, and the heavy-traffic period `16:00–17:00`. For each schedule it assigns explicit red, yellow, green, and all-red durations to every approach; under the heavy-traffic schedule, for example, South runs with `147 s` red, `3 s` yellow, `48 s` green, and `1 s` all-red, while West receives the longest green phase at `75 s`. These time plans are implemented in the PLC ladder program through a timer branch in which green remains active while the timer is running and is cut off once `T0` reaches its preset value. During the peak `16:00–17:00` window, contact `D102` extends the green timing for the active schedule, and once the real-time clock reaches `17:00` the PLC disables that override and returns to the default configuration.

### 3. 逐句溯源

1. 句子 1：The controller organizes the four-way intersection around three daily schedules, covering the morning period `07:00–08:00`, the normal period `12:00–13:00`, and the heavy-traffic period `16:00–17:00`.
   对应摘录：A
2. 句子 2：For each schedule it assigns explicit red, yellow, green, and all-red durations to every approach; under the heavy-traffic schedule, for example, South runs with `147 s` red, `3 s` yellow, `48 s` green, and `1 s` all-red, while West receives the longest green phase at `75 s`.
   对应摘录：A
3. 句子 3：These time plans are implemented in the PLC ladder program through a timer branch in which green remains active while the timer is running and is cut off once `T0` reaches its preset value.
   对应摘录：B
4. 句子 4：During the peak `16:00–17:00` window, contact `D102` extends the green timing for the active schedule, and once the real-time clock reaches `17:00` the PLC disables that override and returns to the default configuration.
   对应摘录：B
