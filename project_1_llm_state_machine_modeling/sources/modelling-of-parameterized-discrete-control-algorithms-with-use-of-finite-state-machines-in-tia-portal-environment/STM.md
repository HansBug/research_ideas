# Modelling of Parameterized Discrete Control Algorithms With Use of Finite State Machines in TIA Portal Environment - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把十字路口交通灯控制器直接建成 `s1-s7` 七状态 FSM，并给出了每个状态的灯色输出、`T1-T6` 定时器和 `OE` 停机回退条件，是一个非常干净的 `FSM + T1` PLC 样本。

## 条目 1: Seven-State Crossroads Traffic-Light FSM in TIA Portal
- 控制对象：TIA Portal 上实现的双向十字路口交通灯控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个以十字路口红黄绿灯相位为对象的七状态 Moore 型 FSM，状态间迁移由 `T1-T6` 六个定时脉冲和 `OE` 使能信号控制。
- 判断：算。对象是明确的离散控制器而不是建模示例；原文给出了状态集合、状态输出表、状态图、具体时长和 PLC/TIA Portal 落地方式，足够直接用于状态机建模数据。

### 1. 原文摘录

#### 摘录 A
- 出处：第 1 页 Abstract / Section I
> This work illustrates usage of Finite State Machines modelling technique to solve a control problem with parameterized external variables.
>
> The FSM model describes the state of an object by specifying the values of particular system variables or parameters at certain moments or intervals of time.

#### 摘录 B
- 出处：第 2-3 页 Section II / Table I / Table II
> In FSM description of the object control algorithm there can be identified seven states s1 to s7.
>
> Each state has individual set of active outputs.
>
> The presented system changes the FSM states on the timing conditions. Therefore it was necessary to introduce timing signals T1 to T6.
>
> If OE is active, the FSM once started performs the control algorithm in infinite loop. Deactivation of the OE causes the algorithm to change the FSM state to s7 and to reset all output signals.

#### 摘录 C
- 出处：第 4-5 页 Section IV `LAD Implementation`
> When the signal is active, the "Start" signal initiates transition of the system to the s1 state.
>
> When the time elapses, the timer disables its output ... equivalent to putting the system into s2 state.
>
> The s3 state is initiated by negative edge detection on "Time Pulse for State 2.Q".
>
> "Time Pulse for State4" ... puts the system into s4 state.
>
> The s5 state is controlled by "Time Pulse for State5" timer.
>
> The next state, s6, is initiated by negative edge of "Time Pulse for State5.Q".
>
> When "Time Pulse for State6" disables its Q output, negative edge detection contact initiates "Time Pulse for State 1" timer and the operation cycle is repeated.

### 2. 基于原文整理后的自然语言描述

The TIA Portal traffic-light controller is modeled as a seven-state finite state machine `s1` through `s7`, where each state corresponds to a fixed lamp configuration for the two intersecting traffic flows. In the nominal cycle, `s1` enables `Green A / Red B`, `s2` switches to `Yellow A / Red B`, `s3` enables `Red A / Yellow B / Red B`, `s4` enables `Red A / Green B`, `s5` enables `Red A / Yellow B`, and `s6` enables `Red A / Yellow A / Red B`; `s7` is the disabled reset state with all outputs off. State advancement is governed by six explicit timer pulses, with the paper’s verification setup using `T1 = 5 s`, `T2 = 2 s`, `T3 = 2 s`, `T4 = 5 s`, `T5 = 2 s`, and `T6 = 2 s`, and each new timer being triggered by the negative edge of the previous state’s timer output. The controller runs in an infinite loop only when the `OE` signal is active, and deactivating `OE` forces an immediate transition to `s7` and resets all lights. Because the paper provides both the state/output tables and the PLC LAD implementation sequence, the whole phase-control chain is directly reconstructable as a timed FSM.

### 3. 逐句溯源

1. 句子 1：The TIA Portal traffic-light controller is modeled as a seven-state finite state machine `s1` through `s7`, where each state corresponds to a fixed lamp configuration for the two intersecting traffic flows.
   对应摘录：A, B
2. 句子 2：In the nominal cycle, `s1` enables `Green A / Red B`, `s2` switches to `Yellow A / Red B`, `s3` enables `Red A / Yellow B / Red B`, `s4` enables `Red A / Green B`, `s5` enables `Red A / Yellow B`, and `s6` enables `Red A / Yellow A / Red B`; `s7` is the disabled reset state with all outputs off.
   对应摘录：B
3. 句子 3：State advancement is governed by six explicit timer pulses, with the paper’s verification setup using `T1 = 5 s`, `T2 = 2 s`, `T3 = 2 s`, `T4 = 5 s`, `T5 = 2 s`, and `T6 = 2 s`, and each new timer being triggered by the negative edge of the previous state’s timer output.
   对应摘录：B, C
4. 句子 4：The controller runs in an infinite loop only when the `OE` signal is active, and deactivating `OE` forces an immediate transition to `s7` and resets all lights.
   对应摘录：B
5. 句子 5：Because the paper provides both the state/output tables and the PLC LAD implementation sequence, the whole phase-control chain is directly reconstructable as a timed FSM.
   对应摘录：B, C
