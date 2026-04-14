# Design of Traffic Light based on FPGA - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文篇幅不长，但把四状态固定轮转、`39 / 4 / 20 / 4` 秒相位时序、`1 Hz` 分频与倒计时显示链直接写成可复原的 timed traffic FSM；只是与库内已有定时交通灯样本相邻较近，更适合降采样保留。

## 条目 1: Four-state countdown traffic-light cycle controller

- 控制对象：道路交通信号控制领域的 FPGA 四状态倒计时交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向十字路口的 FPGA 交通灯控制器，用四个显式状态和倒计时计数器驱动东西向、南北向的轮转放行。
- 判断：算。对象是实际交通灯控制器，原文明确给出了状态集合、各状态信号输出、相位持续时间、`1 Hz` 频率与倒计时实现思路，不只是板级展示结论。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，`2 TRAFFIC SIGNAL CONTROL TASKS`，`paper_content.txt` 第 22-37 行
> The intersection traffic light designed in this paper has the function of indicating the opening and stopping. Red, green and yellow signal lights and digital tube displays are installed at each entrance.
>
> When the east-west direction is open ... the green light in the east-west direction is bright for 39 seconds, then the yellow light is on for 4 seconds ... When the north-south direction is open ... the green light in the north-south direction is bright for 20 seconds, then the yellow light is on for 4 seconds ... Loop in turn.
>
> There is a set of countdown monitors in both the east and west directions to show the passage time and the forbidden time.

#### 摘录 B

- 出处：第 2 页，`4.2 Traffic Signal and Digital Tube Display Circuit Design - Control Circuit`，`paper_content.txt` 第 70-85 行
> Using state machine to complete the signal light off and digital tube counting design, it can be divided into 4 states, namely: east and west green light, north and south red light (S1); east and west yellow light, north and south red light (S2); east and west red light, north and south Green light (S3); red light, north and south yellow light (S4).
>
> Program design idea: first design a 68-ary addition counter, and then design the 39-digit, 4-ary, 20-digit subtraction counter to achieve the display count of the digital tube; at the same time, complete the design of the signal light on and off in each state.

#### 摘录 C

- 出处：第 1-2 页，Introduction 与 `4.1 Frequency Division Circuit Design`，`paper_content.txt` 第 15-19 行与第 47-51 行
> In addition to the basic traffic function, the system also has a countdown function, which simulates the actual traffic intersection.
>
> The frequency of the DE1-SOC development board is 50MHZ. This design requires 1HZ frequency, so the process design and if...else statement are used to complete the crossover design.

### 2. 基于原文整理后的自然语言描述

The controller realizes a fixed four-state traffic cycle for an orthogonal intersection rather than an implicit lamp-blinking sequence. Its four named states are `S1` east-west green / north-south red, `S2` east-west yellow / north-south red, `S3` east-west red / north-south green, and `S4` east-west red / north-south yellow, so the discrete signal configuration of each phase is explicit in the paper. The timing semantics are equally explicit: east-west traffic receives `39 s` of green followed by `4 s` of yellow, north-south traffic receives `20 s` of green followed by `4 s` of yellow, and the controller loops through that order continuously. A `1 Hz` clock derived from the `50 MHz` FPGA clock, together with a `68`-count master counter and dedicated countdown counters, drives both the phase changes and the seven-segment displays. As a result, the paper exposes a complete timed FSM for a countdown traffic controller, even though the controller itself is structurally simpler than richer sensor- or priority-driven traffic-light samples already in the library.

### 3. 逐句溯源

1. 句子 1：The controller realizes a fixed four-state traffic cycle for an orthogonal intersection rather than an implicit lamp-blinking sequence.
   对应摘录：A, B
2. 句子 2：Its four named states are `S1` east-west green / north-south red, `S2` east-west yellow / north-south red, `S3` east-west red / north-south green, and `S4` east-west red / north-south yellow, so the discrete signal configuration of each phase is explicit in the paper.
   对应摘录：B
3. 句子 3：The timing semantics are equally explicit: east-west traffic receives `39 s` of green followed by `4 s` of yellow, north-south traffic receives `20 s` of green followed by `4 s` of yellow, and the controller loops through that order continuously.
   对应摘录：A
4. 句子 4：A `1 Hz` clock derived from the `50 MHz` FPGA clock, together with a `68`-count master counter and dedicated countdown counters, drives both the phase changes and the seven-segment displays.
   对应摘录：B, C
5. 句子 5：As a result, the paper exposes a complete timed FSM for a countdown traffic controller, even though the controller itself is structurally simpler than richer sensor- or priority-driven traffic-light samples already in the library.
   对应摘录：A, B, C
