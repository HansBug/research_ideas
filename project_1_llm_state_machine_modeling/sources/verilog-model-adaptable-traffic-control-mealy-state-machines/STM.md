# A Verilog Model of Adaptable Traffic Control System Using Mealy State Machines - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把五条主路、十个信号灯、负载自适应时长和应急优先都写进了 Mealy 交通灯状态表，细节充足且有明显 `FSM + T1` 价值。

## 条目 1: Five-Road Adaptive Mealy Traffic-Light Controller

- 控制对象：道路交通信号控制领域的五路口自适应交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个基于 Verilog 和 Mealy 状态机的交通灯控制器，管理五条主路拆分后的十个信号灯，并根据车流负载和应急车辆优先请求改变绿灯持续时间与放行顺序。
- 判断：算。对象是真实交通信号控制器，原文明确给出了道路结构、输入开关、时序状态表、负载调时规则和应急优先中断恢复逻辑。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 4-9 行
> In this paper an efficient traffic control system is designed using Mealy finite state machines ... The sensors are added as input to the controller for emergency conditions like ambulance etc. This system is also capable to change the timings of traffic signals according to the density of vehicles on the roads ... The design of adaptable traffic control system is carried out for a chowk consisting of five roads ...

#### 摘录 B

- 出处：第 1-2 页，`Introduction / Roads Structure`，`paper_content.txt` 第 18-22、87-96 行
> In this paper, we have developed a real traffic control system using Mealy state machines ...
>
> Fig. 1 shows structure of any chowk consisting of five main roads and each road is divided into two main roads (straight and cross). We are using ten traffic signals L1, L2,...L10 ... There are four sensors on roads SW1, SW2, SW3 and SW4 for emergency conditions ... Whenever any one of the sensors output is enabled, appropriate traffic starts to continue ...
>
> TL and TS are two inputs for controlling the green signal ON timings. When TS is enabled, ON timing of green light will reduce to halve. When TL is enabled, ON timing of green light will be doubled.

#### 摘录 C

- 出处：第 2 页，`State Table`，`paper_content.txt` 第 97-130 行
> Initially before resetting the TLC, red lights of all traffic signals L1-L10 are ON.
>
> After resetting the TLC, yellow light of signal L1 & L5 are ON ...
>
> After a delay of four seconds, green lights of traffic signals L1 & L5 are ON ...
>
> After eight seconds ... green light on L2 and L6 ...
>
> ... green light on the signals L4 and L8 ...
>
> ... green light of signal L9 ...
>
> ... green light of signal L10 is ON and remains ON for eight seconds ...
>
> The sequence repeats until the reset of TLC or any one of the emergency switches are enabled.
>
> Whenever there is emergency vehicle on the road ... the sequence is allowed to continue from a position where it was stopped. There is priority queue for the emergency switches.

#### 摘录 D

- 出处：第 3 页，`Pins Description`，`paper_content.txt` 第 159-176 行
> Input Signal Description
> CLK System Clock
> RESET Reset Input
> SW1 Emergency switch on Road 1 and 5
> ...
> TS When enabled, Green signal ON timing halved
> TL When enabled, Green signal ON timing doubled
>
> Output Signal Description
> L15 <2:0> Traffic Lights on Road 1 and 5 (Straight)
> ...
> SEG_a-SEG_g Seven segment display for timing representations

### 2. 基于原文整理后的自然语言描述

The traffic-light controller is implemented as a Mealy finite-state machine for a five-road chowk, where each main road is split into straight and cross traffic and the whole junction is represented by ten traffic signals. In the normal cycle, the machine begins from an all-red condition, enters a yellow preparation phase for `L1/L5`, then advances through a timed sequence of green and yellow phases that successively serve `L1/L5`, `L2/L6`, `L3/L7`, `L4/L8`, `L9`, and `L10`. The controller is not fixed-time only, because the `TS` and `TL` inputs can halve or double the green duration according to traffic load. It is also not purely cyclic, because four emergency switches `SW1-SW4` can interrupt the sequence, force the corresponding road to proceed, and then resume the normal cycle from the state where it was paused, with a first-arrival priority queue among active emergency requests. The input and output interface is explicit in the paper, including `CLK`, `RESET`, the emergency switches, the timing modifiers, grouped lamp outputs, and a seven-segment timing display.

### 3. 逐句溯源

1. 句子 1：The traffic-light controller is implemented as a Mealy finite-state machine for a five-road chowk, where each main road is split into straight and cross traffic and the whole junction is represented by ten traffic signals.
   对应摘录：A, B
2. 句子 2：In the normal cycle, the machine begins from an all-red condition, enters a yellow preparation phase for `L1/L5`, then advances through a timed sequence of green and yellow phases that successively serve `L1/L5`, `L2/L6`, `L3/L7`, `L4/L8`, `L9`, and `L10`.
   对应摘录：C
3. 句子 3：The controller is not fixed-time only, because the `TS` and `TL` inputs can halve or double the green duration according to traffic load.
   对应摘录：B, D
4. 句子 4：It is also not purely cyclic, because four emergency switches `SW1-SW4` can interrupt the sequence, force the corresponding road to proceed, and then resume the normal cycle from the state where it was paused, with a first-arrival priority queue among active emergency requests.
   对应摘录：B, C, D
5. 句子 5：The input and output interface is explicit in the paper, including `CLK`, `RESET`, the emergency switches, the timing modifiers, grouped lamp outputs, and a seven-segment timing display.
   对应摘录：D
