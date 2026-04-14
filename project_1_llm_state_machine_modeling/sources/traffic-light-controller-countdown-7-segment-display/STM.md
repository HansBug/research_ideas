# Traffic Light Controller Displaying Countdown using 7-segment Display - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把路口相位、倒计时显示、行人全停延时和 `S0-S5` 的状态推进都写成了明确的 Verilog 交通灯控制链，足以形成 `FSM + T1` 双 A 样本。

## 条目 1: Countdown Traffic Light and Pedestrian Delay Controller
- 控制对象：道路交通信号控制领域的倒计时显示与行人全停延时交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个针对东西向/南北向十字路口的交通灯控制器，通过 `S0-S5` 六个状态和倒计时显示控制两组红黄绿灯，并为斑马线行人预留全停延时。
- 判断：算。对象是明确的 traffic light controller，不是单纯 HDL 语法示例；原文同时给出了状态顺序、秒级倒计时、灯色编码、7 段数码管输出和行人全停时间。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页，Abstract，`paper_content.txt` 第 15-30 行
> The main objective of the work is to simulate and synthesize the functionality to demonstrate Traffic Light Controller using state machines and to display countdown waiting for timer using 7 segment displays. ... This system is implemented using a state machine which is going to shift each state to next state when counter value waits up to a fixed time. ... The system also considers delay unit for pedestrian.

#### 摘录 B
- 出处：第 3-4 页，`Road structure / State machine and state table`，`paper_content.txt` 第 132-149、162-170 行
> The road structure has also shown zebra crossings for pedestrians so system has provided 2 seconds time period in which both the signals will be off to allow pedestrians to use roads. ... As an initial condition state S0, Light A[2:0] will be on so green light in East-West direction will be ON for 7 seconds ... after counting of 7 seconds ... shift to next state S1 ... After that the counter will display only 2 seconds of time delay and signals will be turned into next state S2 which has both Lights A[2:0] and Lights B[2:0] in STOP situation. Further the system goes to next state S3 ... Similarly, flow will be continued ... switch to next states S4, S5 respectively. ... After resetting, the system will again start from the state S0.

#### 摘录 C
- 出处：第 5 页，`Logic Synthesis`，`paper_content.txt` 第 197-210 行
> The expected functionality of this project system includes the traffic lights should change after every fixed interval of time and count down time should be displayed on 7 Segment Display. ... We programmed the logic in Verilog by considering two lights for signals as A[2:0], B[2:0] with RYG coding ... Another part includes assigning the values to lights A, B as output for any particular state. Further at the end we came up with task which converts 4 digits count value into 7 digits value to send to 7-seg display unit as output.

### 2. 基于原文整理后的自然语言描述

The traffic-light controller models a two-direction intersection as a fixed-sequence FSM with explicit countdown semantics. Its state progression starts from `S0`, keeps East-West green for `7` seconds, moves through a yellow phase and an all-stop `2`-second pedestrian window, then mirrors the same logic for the North-South direction across states `S3-S5`. The timer value is not hidden inside the implementation because the paper explicitly states that the counter both drives state changes and feeds a `7-segment` display, while `A[2:0]` and `B[2:0]` encode the red-yellow-green outputs for each phase. Since the phase order, reset behavior, pedestrian delay, and countdown display are all explicit, this is a clean `FSM + T1` traffic-signal sample.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller models a two-direction intersection as a fixed-sequence FSM with explicit countdown semantics.
   对应摘录：A, B
2. 句子 2：Its state progression starts from `S0`, keeps East-West green for `7` seconds, moves through a yellow phase and an all-stop `2`-second pedestrian window, then mirrors the same logic for the North-South direction across states `S3-S5`.
   对应摘录：B
3. 句子 3：The timer value is not hidden inside the implementation because the paper explicitly states that the counter both drives state changes and feeds a `7-segment` display, while `A[2:0]` and `B[2:0]` encode the red-yellow-green outputs for each phase.
   对应摘录：A, B, C
4. 句子 4：Since the phase order, reset behavior, pedestrian delay, and countdown display are all explicit, this is a clean `FSM + T1` traffic-signal sample.
   对应摘录：A, B, C
