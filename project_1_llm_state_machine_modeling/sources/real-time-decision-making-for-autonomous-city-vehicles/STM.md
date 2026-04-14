# Real-Time Decision Making for Autonomous City Vehicles - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶决策模块里的 driving maneuver 统一抽象成确定有限自动机，明确给出 `q0 / qr_i / qF / qE`、事件集合和多阶段 maneuver 分解，足够形成双 A 条目。

## 条目 1: Multi-Phase Driving Maneuver DFA
- 控制对象：汽车与道路车辆控制领域的城市自动驾驶高层 maneuver 决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定
- 一句话说明：这是一个面向城市交通环境的自动驾驶 maneuver supervisor，用统一的 DFA 结构管理不同 driving maneuver 的启动、执行、终止与中止。
- 判断：算。对象是实际自动驾驶车辆的决策控制器，不是单纯架构综述；原文直接给出了 automaton 组成、输入事件、Run-state 语义和 overtaking 的多阶段实例。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Abstract / Section 2
> This paper addresses the topic of real-time decision making by autonomous city vehicles.
>
> Based on the information provided by the Perception subsystem, the Real-Time Decision Making & Driving Maneuver Control subsystem makes driving decisions. This software subsystem decides about the activation and the execution of the most appropriate driving maneuver.

#### 摘录 B
- 出处：第 4 页，Section 4
> Their operational behavior is designed using deterministic finite automata ... as follows: a start state `q0`, `2` final states `{qF, qE}`, a set of Run states `Qrun={qr1, qr2, ..., qrn}`, and a set of input symbols `Σ={Run, Stop, Restart, Error}`.

#### 摘录 C
- 出处：第 4-5 页，Section 4 / Fig. 4
> The start state `q0` is the waiting or idle state ... The Run states `qr1, qr2, ..., qrn` perform the maneuvering of the vehicle ... The automaton enters the error state `qE` if certain preconditions are not met.
>
> The overtaking maneuver is decomposed into five phases. In the finite automaton each phase is represented by a Run state.

#### 摘录 D
- 出处：第 5 页，Section 4
> `Run`: request to begin the execution of the driving maneuver.
>
> `Stop`: request to stop the execution of the driving maneuver.
>
> `Restart`: request to restart the driving maneuver.
>
> `Error`: some error occurred, which makes the continued execution of the driving maneuver impossible.

### 2. 基于原文整理后的自然语言描述

The decision-making module is organized around a deterministic finite automaton template that every driving maneuver must follow. Each maneuver starts in idle state `q0`, executes through one or more phased Run states `qr1...qrn`, and ends either in successful completion `qF` or abort state `qE`. The event alphabet is explicit as `Run`, `Stop`, `Restart`, and `Error`, so maneuver activation, interruption, reset, and failure are all modeled as first-class discrete transitions rather than hidden controller internals. While the paper uses this structure generically for different maneuvers, it also gives a concrete overtaking example in which the maneuver is decomposed into five phases and each phase is mapped to one Run state. During each Run state, the controller checks World Model availability and safety preconditions before continuing execution, and unmet preconditions force the automaton into `qE`.

### 3. 逐句溯源

1. 句子 1：The decision-making module is organized around a deterministic finite automaton template that every driving maneuver must follow.
   对应摘录：A, B
2. 句子 2：Each maneuver starts in idle state `q0`, executes through one or more phased Run states `qr1...qrn`, and ends either in successful completion `qF` or abort state `qE`.
   对应摘录：B, C
3. 句子 3：The event alphabet is explicit as `Run`, `Stop`, `Restart`, and `Error`, so maneuver activation, interruption, reset, and failure are all modeled as first-class discrete transitions rather than hidden controller internals.
   对应摘录：B, D
4. 句子 4：While the paper uses this structure generically for different maneuvers, it also gives a concrete overtaking example in which the maneuver is decomposed into five phases and each phase is mapped to one Run state.
   对应摘录：C
5. 句子 5：During each Run state, the controller checks World Model availability and safety preconditions before continuing execution, and unmet preconditions force the automaton into `qE`.
   对应摘录：C
