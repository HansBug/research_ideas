# VHDL IMPLEMENTATION FOR FSM BASED APPROACH OF TRAFFIC LIGHT CONTROLLER - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把双向交通灯的常规/测试/待机三模式、四个主交通相位和对应定时条件写成了标准 timed FSM，可直接形成双 A 样本。

## 条目 1: Timed RG-RY-GR-YR Traffic-Light FSM with Test and Standby Modes

- 控制对象：道路交通信号领域的双向交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 VHDL 的双向交通灯状态机控制器，用 `regular / test / standby` 三种运行模式管理 `RG / RY / GR / YR` 四个主相位和对应定时输出。
- 判断：算。对象是真实交通灯控制器，原文明确给出运行模式、状态名、`30 s / 5 s / 45 s / 1 s` 等相位时长、输入信号和输出灯色。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2-3 页，`2. FSM FOR TRAFFIC LIGHT CONTROLLER`，`paper_content.txt` 第 145-150、164-180 行
> Traffic light system is a best way to manage traffic in cities. It helps in avoiding accidents and manage rules and regulation for the vehicles as well as humans. Traffic light controller is a main part of traffic control system.
>
> Three modes of operation: regular, test, and standby.
>
> In regular mode: Four states of operation, called RG, RY, GR, and YR, each with an independent time duration.
>
> In test mode: Allow all preprogrammed times to be overwritten with a small value, such that the system can be easily tested during maintenance (1 second per state).
>
> In standby mode: the system should activate the yellow lights in both directions, remaining so while the standby signal is active.

#### 摘录 B

- 出处：第 3 页，`2.1 Simulation`，`paper_content.txt` 第 191-201 行
> The state diagram for traffic light controller is shown in the figure. Also, in this, the time values change with the state and with the operating mode (regular or test). Note that all transitions are timed only. The inputs are clk, stby, and, test, while the output are r1, y1, g1, r2, y2 and g2 (red, yellow, and green lights in directions 1 and 2). A VHDL code for this FSM obeying the modified template introduced in this section. The time values were specified using GENERIC declaration.

#### 摘录 C

- 出处：第 3 页，`Table 1: Table depicting Operating Modes of TLC`，`paper_content.txt` 第 211-220 行
> STATE OPERATING MODES
>
> RG Timer: timeRG(30s)  timeTEST(1s)
>
> RY Timer: timeRY(5s)   timeTEST(1s)
>
> GR Timer: timeGR(45s)  timeTEST(1s)
>
> YR Timer: timeYR(5s)   timeTEST(1s)

### 2. 基于原文整理后的自然语言描述

The traffic-light controller is modeled as a timed VHDL finite state machine for a two-way intersection, and it explicitly distinguishes three operating modes: `regular`, `test`, and `standby`. In its regular operating path the controller cycles through four main traffic states, `RG`, `RY`, `GR`, and `YR`, each of which represents a complete red-yellow-green pattern for the two directions and each of which owns an independent duration. All transitions are timed rather than event-jumped, so the controller advances according to the phase timer under the `clk` input while still allowing the `test` and `stby` signals to switch the operating regime. In test mode the same state sequence is preserved but every phase duration is collapsed to `1 s` for maintenance, whereas standby mode forces yellow lights in both directions and holds that warning state while the standby signal remains active. The design therefore gives a compact but fully specified FSM with explicit state names, output lines, mode guards, and engineering time values.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller is modeled as a timed VHDL finite state machine for a two-way intersection, and it explicitly distinguishes three operating modes: `regular`, `test`, and `standby`.
   对应摘录：A, B
2. 句子 2：In its regular operating path the controller cycles through four main traffic states, `RG`, `RY`, `GR`, and `YR`, each of which represents a complete red-yellow-green pattern for the two directions and each of which owns an independent duration.
   对应摘录：A
3. 句子 3：All transitions are timed rather than event-jumped, so the controller advances according to the phase timer under the `clk` input while still allowing the `test` and `stby` signals to switch the operating regime.
   对应摘录：B
4. 句子 4：In test mode the same state sequence is preserved but every phase duration is collapsed to `1 s` for maintenance, whereas standby mode forces yellow lights in both directions and holds that warning state while the standby signal remains active.
   对应摘录：A, C
5. 句子 5：The design therefore gives a compact but fully specified FSM with explicit state names, output lines, mode guards, and engineering time values.
   对应摘录：A, B, C
