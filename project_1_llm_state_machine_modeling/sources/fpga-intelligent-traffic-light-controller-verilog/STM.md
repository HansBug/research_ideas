# FPGA Implementation of an Intelligent Traffic Light Controller (I-TLC) in Verilog - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：原文完整写出了四状态 Moore 交通灯控制器、`TS/TL/ST` 定时链和侧路车辆触发条件，足以形成双 A 的交通信号样本。

## 条目 1: Four-State Main-and-Side-Road Traffic Controller
- 控制对象：道路交通信号领域的主路-侧路自适应交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个四向路口的 Moore 型交通灯控制器，用主路优先、侧路传感触发和双定时器 `TL/TS` 共同管理绿灯与黄灯切换。
- 判断：算。对象是实际交通信号控制器，原文明确给出四个状态、输入/输出信号、长短定时器、状态停留条件和主路-侧路服务循环。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，`IV. WORKING OF THE I-TLC SYSTEM / A. WORKING PRINCIPLE`，`paper_content.txt` 第 147-175 行
> This paper introduces an interval timer system consisting of TS, which produces a shorter duration timing pulse, and TL, which
> generates a longer duration pulse, in response to a start timer (ST). TS is employed for timing the ’Amber’ lights, while TL is
> utilized for timing the ’Green’ lights.
> Input Signal Description
> Reset Returns the Finite State Machine (FSM) to its initial state
> C The sensor identifies the presence of vehicles, if any, on the side road.
> TS Short duration pulse
> TL Long duration pulse
> Output Signal Description
> MG, MY, MR Assert green/Amber/red lights on Main Road
> SG, SY, SR Assert green/Amber/red on Side road
> ST Start timer -either a short or long interval

#### 摘录 B
- 出处：第 2 页，`B. STATE DIAGRAM / TABLE III`，`paper_content.txt` 第 177-194 行
> In the Moore finite state machine model, the output is linked solely to the current state.
> Therefore, for the Traffic Light Controller (TLC) system examined in this paper, four distinct scenarios, each representing a
> unique state of the FSM model, have been elucidated.
> State Description
> S0 Main road Green and Side road Red
> S1 Main road Yellow and Side road Red
> S2 Side road Green and Main road Red
> S3 Side road Yellow and Main road Red

#### 摘录 C
- 出处：第 2-3 页，`B. STATE DIAGRAM`，`paper_content.txt` 第 196-228 行
> S0 is considered to be the default state or the initial state. It is defined as the state when main road light is ‘Green’ and the side
> road light is ‘Red’. The FSM stays in the S0 state if TL has not expired yet or no vehicle is detected on the side road by the sensor.
> While being in the S0 state, if both, TL has expired and a vehicle is also detected on the side road, a transition is made from
> state S0 to state S1.
> The FSM remains in the state S1 until the short timer (TS) reaches its expiration. Upon TS expiration, the FSM transitions
> from state S1 to state S2, where the main road light is ’Red,’ and the side road light is ’Green’.
> When in state S2, the Finite State Machine (FSM) remains in that state as long as TL is active and there is still a vehicle on
> the side road. However, if TL has elapsed or there are no vehicles detected on the side road, the FSM transitions from S2 to S3.
> When in state S3, the traffic lights on the side road are Amber, and those on the main road are ’Red.’ ... if TS has elapsed, a
> transition occurs from S3 back to the initial state S0.

### 2. 基于原文整理后的自然语言描述

The I-TLC is a Moore traffic-light controller that serves a main road and a side road through four named states rather than through an implicit timing loop. It uses `TL` as the long green timer, `TS` as the short amber timer, and `ST` as the signal that starts the corresponding interval whenever the controller restarts timing. In `S0`, the main road remains green and the side road remains red until both the long timer has expired and the side-road sensor `C` reports waiting traffic, after which the FSM moves to `S1` for the main-road amber phase. When the short timer expires, the controller enters `S2` to give the side road green, stays there while `TL` is active and vehicles are still present, and then transfers to `S3` when the green interval ends or the side road clears. After the amber interval on the side road finishes in `S3`, the controller returns to `S0`, thereby closing a complete sensor-driven main-road/side-road service cycle.

### 3. 逐句溯源

1. 句子 1：The I-TLC is a Moore traffic-light controller that serves a main road and a side road through four named states rather than through an implicit timing loop.
   对应摘录：B
2. 句子 2：It uses `TL` as the long green timer, `TS` as the short amber timer, and `ST` as the signal that starts the corresponding interval whenever the controller restarts timing.
   对应摘录：A
3. 句子 3：In `S0`, the main road remains green and the side road remains red until both the long timer has expired and the side-road sensor `C` reports waiting traffic, after which the FSM moves to `S1` for the main-road amber phase.
   对应摘录：A, C
4. 句子 4：When the short timer expires, the controller enters `S2` to give the side road green, stays there while `TL` is active and vehicles are still present, and then transfers to `S3` when the green interval ends or the side road clears.
   对应摘录：C
5. 句子 5：After the amber interval on the side road finishes in `S3`, the controller returns to `S0`, thereby closing a complete sensor-driven main-road/side-road service cycle.
   对应摘录：C
