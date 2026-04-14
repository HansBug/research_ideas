# Modeling and Verification of Agent based Adaptive Traffic Signal using Symbolic Model Verifier - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把四相位自适应交通灯明确转成 FSM，并补出 `weighted round-robin`、`Tthr`、入口/出口计数器、`CV=min(Tcal,Tthr)` 与 wait-time counter，属于非常完整的交通信号 EFSM 样本。

## 条目 1: Weighted round-robin adaptive signal controller

- 控制对象：道路交通信号控制领域的加权轮转自适应交通灯控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个四方向路口的自适应 signal controller，用主代理和八个监测代理根据实时排队长度决定哪一路变绿以及持续多久。
- 判断：算。对象是明确的交通信号控制器而不是纯验证流程；原文给出了状态集合、相位轮转顺序、计数器变量、阈值 `Tthr`、权重计算、wait-time counter 以及 FSM 到 NuSMV 的映射。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> In this paper we have considered a scenario of adaptive traffic signal across the intersection of two roads ... we have shown how we can transform this scenario into a Finite State Machine (FSM). Once the system is transformed into a FSM, we have verified the specifications specified in Computational Tree Logic (CTL) using NuSMV as a model checking tool.

#### 摘录 B

- 出处：第 2-3 页，Section `3 Detail Design of Agent Based Adaptive Traffic Signal`
> Each one of the four combinations will get a chance in a weighted round-robin fashion.
>
> Tthr: maximum duration for which any green light can be turned ON.
>
> The master maintains a counter for each Entry/Exit Agents ... the master will determine the weight of the next (determined by round-robin) green signal by subtracting the number of exit count from the entry count for that particular lane.
>
> If this value is less than the Tthr, then a weight of n*tv is allocated to that green signal otherwise a weight of Tthr is assigned to it.

#### 摘录 C

- 出处：第 4 页，Section `5.1 State Transition Diagram`
> The state transition diagram of the adaptive traffic scenario is shown in Fig.3. Initially, we assume that the system begins its execution from signal post labeled as NORTH ... The system proceeds in a weighted round-robin fashion as NORTH, WEST, SOUTH, EAST, NORTH and so on.
>
> Turn = 0 corresponds to green light of signal post at NORTH ... Turn = 3 corresponds to green light of signal post at EAST.
>
> The counter value (CV) is calculated as CV = min{Tcal, Tthr}. Once the counter value is determined, it keeps on decrementing ... Once the counter value becomes zero, the turn moves on to the next signal.
>
> Moving further, each state has wait time counter.

### 2. 基于原文整理后的自然语言描述

The adaptive traffic controller is modeled as a four-phase EFSM that rotates `NORTH -> WEST -> SOUTH -> EAST` in a weighted round-robin order rather than using a fixed green-time cycle. Each phase duration is computed by a master agent from the real-time queue estimate of the next lane, using entry and exit counters together with the threshold `Tthr`, so the active signal receives `CV = min(Tcal, Tthr)` before its counter starts decrementing. The state variable `Turn` determines which signal is green, while the counters and queue-length arithmetic extend the flat phase machine with lane-specific data and dynamic weight assignment. In addition, each state maintains a wait-time counter to measure how long a signal stays red before turning green again, which makes waiting-time bounds part of the controller semantics instead of an external metric. The result is a timed traffic-signal EFSM whose discrete phase order, counter updates, and threshold-capped green allocation are all explicitly recoverable from the paper.

### 3. 逐句溯源

1. 句子 1：The adaptive traffic controller is modeled as a four-phase EFSM that rotates `NORTH -> WEST -> SOUTH -> EAST` in a weighted round-robin order rather than using a fixed green-time cycle.
   对应摘录：A, C
2. 句子 2：Each phase duration is computed by a master agent from the real-time queue estimate of the next lane, using entry and exit counters together with the threshold `Tthr`, so the active signal receives `CV = min(Tcal, Tthr)` before its counter starts decrementing.
   对应摘录：B, C
3. 句子 3：The state variable `Turn` determines which signal is green, while the counters and queue-length arithmetic extend the flat phase machine with lane-specific data and dynamic weight assignment.
   对应摘录：B, C
4. 句子 4：In addition, each state maintains a wait-time counter to measure how long a signal stays red before turning green again, which makes waiting-time bounds part of the controller semantics instead of an external metric.
   对应摘录：C
5. 句子 5：The result is a timed traffic-signal EFSM whose discrete phase order, counter updates, and threshold-capped green allocation are all explicitly recoverable from the paper.
   对应摘录：A, B, C
