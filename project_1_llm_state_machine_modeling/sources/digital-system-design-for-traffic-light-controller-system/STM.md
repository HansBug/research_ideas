# Digital System Design for Traffic Light Controller System: A Systematic Approach - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向十字路口交通灯拆成 `TIME_COUNTER + FSM` 两个模块，并给出 `1 Hz` 时钟、`29/4/2` 定时量、六状态与复位条件，足够形成双 A 的定时 FSM 样本。

## 条目 1: Six-State Timed Two-Street Traffic-Light FSM
- 控制对象：道路交通信号领域的双街口交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向十字路口 `street_a / street_b` 的六状态交通灯 FSM，利用 `1 Hz` 主时钟和独立 `TIME_COUNTER` 驱动绿灯、黄灯和全红过渡。
- 判断：算。对象是明确的交通灯控制器而不是教学流程，原文给出了输入输出接口、定时参数、状态数、部分状态名和复位状态。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract（对应 `paper_content.txt` 第 15-22 行）
> At first, the specification and requirements of traffic light controller are stated. Then, the system architecture based on finite state machine (FSM) are conducted. Finally, the way of using HDL as well as the test-bench simulation are given in detail.

#### 摘录 B
- 出处：第 2 页，`A. Problem statement`（对应 `paper_content.txt` 第 88-97 行）
> We will consider the traffic light in a crossroad where the considered system includes two traffic lights for street A and street B. Each light has three types of light signals: RED, YELLOW, and GREEN. ... clk is the main clock system assumed 1Hz frequency; rst_n is the reset signal to initialize our system; street_a and street_b are the output signals for light control.

#### 摘录 C
- 出处：第 3 页，`B. FSM modules analysis`（对应 `paper_content.txt` 第 119-140 行）
> TIME_COUNTER is for timing, which count the pre-defined clocks such as 29 clocks for GREEN_TIME, 4 clocks for YELLOW_TIME, and 2 clocks for RED_TIME.
>
> FSM shows the transition between finite states, we will have six states: AG_BR, AY_BR, and so on. The transitions between those states, and the condition of transitions are also given, and a note for an assumption is that the reset state is AR_BR1 (both lights are red).

### 2. 基于原文整理后的自然语言描述

The traffic-light controller models a two-street crossroads as a six-state finite state machine whose outputs are the lamp configurations of `street_a` and `street_b`. The controller is clocked by a `1 Hz` main clock, accepts `rst_n` as a reset input, and drives the two traffic-light output buses through a separate `TIME_COUNTER` plus `FSM` architecture. The timing submodule counts three explicit dwell lengths: `29` clocks for green, `4` clocks for yellow, and `2` clocks for red-to-red transition intervals. At the FSM layer, the paper names states such as `AG_BR`, `AY_BR`, and reset state `AR_BR1`, and explains that the six states are connected by explicitly defined transition conditions. Together these details form a timed crossroads signal cycle in which the light phases are advanced by fixed counters rather than ad hoc combinational logic.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller models a two-street crossroads as a six-state finite state machine whose outputs are the lamp configurations of `street_a` and `street_b`.
   对应摘录：B, C
2. 句子 2：The controller is clocked by a `1 Hz` main clock, accepts `rst_n` as a reset input, and drives the two traffic-light output buses through a separate `TIME_COUNTER` plus `FSM` architecture.
   对应摘录：B, C
3. 句子 3：The timing submodule counts three explicit dwell lengths: `29` clocks for green, `4` clocks for yellow, and `2` clocks for red-to-red transition intervals.
   对应摘录：C
4. 句子 4：At the FSM layer, the paper names states such as `AG_BR`, `AY_BR`, and reset state `AR_BR1`, and explains that the six states are connected by explicitly defined transition conditions.
   对应摘录：C
5. 句子 5：Together these details form a timed crossroads signal cycle in which the light phases are advanced by fixed counters rather than ad hoc combinational logic.
   对应摘录：A, B, C
