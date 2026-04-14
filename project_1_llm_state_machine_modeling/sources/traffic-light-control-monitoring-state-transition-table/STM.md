# INTELLIGENT TRAFFIC LIGHT CONTROL AND MONITORING USING STATE TRANSITION TABLE (STT) - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 T 型路口交通灯写成带队列检测的 12 状态 ASM/STT 控制器，并给出状态表、输出线和 `6/2/6/18 s` 定时链。

## 条目 1: Queue-aware twelve-state T-junction traffic-light supervisor

- 控制对象：道路交通信号控制领域的 T 型路口队列感知交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 T 型路口的交通灯监督控制器，用 12 状态 ASM/STT 表示三方向红黄绿切换，并利用队列检测器提前结束当前相位、切到下一有车方向。
- 判断：算。对象是实际交通灯控制系统，不是单纯硬件设计教程；原文直接给出了 12 个状态、输入 qualifier、15 条输出线以及秒级定时与 queue-clear 跳转条件。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，`paper_content.txt` 第 18-28 行
> In this paper, the design of a system that utilizes and efficiently manages traffic light controllers is presented. ... The system designed featured a queue detecting device. The advantage of this is that unlike the conventional traffic light system, it does not necessary have to give right of way to a route when there is no queue within a given range rather it apportions right of way to the next route if there is a queue. It also combines a thorough initial hardware design approach leading to the State Transition Table (STT) before generating the corresponding software that has just one statement per link path in the STT.

#### 摘录 B

- 出处：第 4-6 页，`ASM chart / State assignment / State Transition Table`，`paper_content.txt` 第 116-121、135-151、169 行
> The Algorithmic State Machine (ASM) chart of figure 4 shows the control flow ... The conditional output HCLRT is used to clear the timing for the present sequence and move to the next when no queue is detected.
>
> In the ASM chart ... N, NE and LF are used in differentiate the traffic light line in each of the three directions ... Thus the ASM chart of fig 4 has twelve states.
>
> The information contained in an ASM chart ... can be represented as a flat table ... The qualifiers T, QE, QLE QN, and the present states D, C, B, A would constitute the input needed for this operation. Similarly, there are 15 output lines ... HAMBLE, HREDN, HREDE, HREDLE, HAMBN, HGRNN, HR2, HAMBE, HGRNE, HR1, HGRNLE.

#### 摘录 C

- 出处：第 10 页，`3.2.4 Traffic Timing Signal t`，`paper_content.txt` 第 480-491 行
> Each set of traffic control lights has duration as follows 6 seconds of amber for the direction about to hand-over right of way, 2 seconds of red in the direction about to handover right of way, 6 seconds of amber in the direction about to receive right of way, 18 seconds of green to the direction that has the right of way.
>
> Since 1 count is achieved every 2 seconds. T stays low for 3 counts (i.e. 6 seconds), then goes high for 1 count (i.e. 2 seconds) and goes low again for 3 counts (i.e. 6 seconds) and finally goes high for 9 counts (i.e. 18 seconds). When the queue in the direction that has right of way is finished before 18 seconds, HCLRT is generated to restart the timing cycle for another direction otherwise, the counter restarts by itself when it reaches 18 seconds ...

### 2. 基于原文整理后的自然语言描述

The controller for the T-junction is an EFSM derived from an ASM chart and flattened into a State Transition Table, so the traffic-signal logic is represented as a discrete machine rather than as an informal phase narrative. Its machine has `12` states and uses qualifier inputs such as `T`, `QE`, `QLE`, and `QN` together with four present-state bits to decide the next state and the corresponding red/amber/green output lines for the three directions. The timing chain is explicit: each direction that is about to give up right of way spends `6 s` in amber, then `2 s` in red clearance, the receiving direction holds `6 s` in amber, and the granted direction keeps green for `18 s`. Those durations are implemented through a 4-bit counter whose signal `T` changes after `3`, `1`, `3`, and `9` counts of `2 s` each. The queue-detection extension makes the controller adaptive instead of purely cyclic, because when the active direction becomes empty before the full `18 s` green expires, the conditional output `HCLRT` clears the current timing cycle and advances the right of way to the next queued branch.

### 3. 逐句溯源

1. 句子 1：The controller for the T-junction is an EFSM derived from an ASM chart and flattened into a State Transition Table, so the traffic-signal logic is represented as a discrete machine rather than as an informal phase narrative.
   对应摘录：A, B
2. 句子 2：Its machine has `12` states and uses qualifier inputs such as `T`, `QE`, `QLE`, and `QN` together with four present-state bits to decide the next state and the corresponding red/amber/green output lines for the three directions.
   对应摘录：B
3. 句子 3：The timing chain is explicit: each direction that is about to give up right of way spends `6 s` in amber, then `2 s` in red clearance, the receiving direction holds `6 s` in amber, and the granted direction keeps green for `18 s`.
   对应摘录：C
4. 句子 4：Those durations are implemented through a 4-bit counter whose signal `T` changes after `3`, `1`, `3`, and `9` counts of `2 s` each.
   对应摘录：C
5. 句子 5：The queue-detection extension makes the controller adaptive instead of purely cyclic, because when the active direction becomes empty before the full `18 s` green expires, the conditional output `HCLRT` clears the current timing cycle and advances the right of way to the next queued branch.
   对应摘录：A, B, C
