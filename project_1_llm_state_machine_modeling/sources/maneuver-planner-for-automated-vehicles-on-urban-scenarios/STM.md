# Maneuver Planner for Automated Vehicles on Urban Scenarios - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市驾驶中的监管信号处理写成 `Go / Yield / Try / Aware` 四态 FSM，并用信号类型、让行线距离、车流 gap 与行人占用条件驱动状态切换。

## 条目 1: Go-Yield-Try-Aware Regulatory-Signal FSM

- 控制对象：城市自动驾驶机动规划器中的监管信号处理模块
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个城市路口/行人过街场景下的自动驾驶监管信号处理器，用四个离散状态组织让行、必须停车和行人过街信号的处理逻辑。
- 判断：算。对象是实际自动驾驶车辆的机动规划模块，原文明确给出 FSM 状态集合、状态转移条件表，以及不同信号类型下的状态更新规则。

### 1. 原文摘录

#### 摘录 A

- 出处：第 4 页，`C. Regulatory signal handling / Fig. 4 / Table I`，`paper_content.txt` 第 288-367 行
> A finite state machine with four possible states `S = {Go, Yield, Try, Aware}` is used to comply with the aforementioned regulatory signal behaviors. ... The initial state is `S0 = Go`, and the future states are obtained according to the state-change conditions defined in Table I. ... Each signal is described using three variables: the type of signal, the unique id on the digital map, and the distance from the EV to the yielding line.
>
> State transition conditions for the regulatory signal FSM include the signal type `RW / MS / PC`, the distance to the yielding line, the gap with respect to traffic, and the pedestrian-free timers.

#### 摘录 B

- 出处：第 4 页，`C. Regulatory signal handling`，`paper_content.txt` 第 368-382 行
> When the current traffic-regulation state is `Sk = Go`, if the signal type is `RW`, the new state is `Sk+1 = try`. In this state, the trajectory generator tries to find a feasible speed profile that allows the EV to merge before a vehicle with higher priority, or to stop on the yielding line if it is not possible.
>
> If `Sk = Go` and the signal type is `MS`, then `Sk+1 = yield`, leading the speed profile of each path candidate to always stop before reaching the yielding line. Lastly, if `Sk = Go` and the signal type is `PC` then `Sk+1 = aware`; in this state, the trajectory generator reduces the speed before crossing the signal. If `Sk = aware` and there is a pedestrian detected on the crossing zone, then `Sk+1 = yield`, and the EV will stop before the yielding line.

### 2. 基于原文整理后的自然语言描述

The urban maneuver planner contains a four-state regulatory-signal FSM with `Go`, `Yield`, `Try`, and `Aware` to manage right-of-way, must-stop, and pedestrian-crossing signals. The machine starts in `Go` and updates its state according to the signal type, signal identifier, distance to the yielding line, acceptable traffic gap, and pedestrian-related timers. When a right-of-way signal is found, the planner enters `Try` and searches for a speed profile that either merges before higher-priority traffic or stops at the yielding line if that is not possible. When a must-stop signal is detected, the planner goes directly to `Yield`, and when a pedestrian-crossing signal is detected it first enters `Aware` to reduce speed, then escalates to `Yield` if a pedestrian is present in the crossing zone so that the ego vehicle stops before the yielding line.

### 3. 逐句溯源

1. 句子 1：The urban maneuver planner contains a four-state regulatory-signal FSM with `Go`, `Yield`, `Try`, and `Aware` to manage right-of-way, must-stop, and pedestrian-crossing signals.
   对应摘录：A
2. 句子 2：The machine starts in `Go` and updates its state according to the signal type, signal identifier, distance to the yielding line, acceptable traffic gap, and pedestrian-related timers.
   对应摘录：A
3. 句子 3：When a right-of-way signal is found, the planner enters `Try` and searches for a speed profile that either merges before higher-priority traffic or stops at the yielding line if that is not possible.
   对应摘录：B
4. 句子 4：When a must-stop signal is detected, the planner goes directly to `Yield`, and when a pedestrian-crossing signal is detected it first enters `Aware` to reduce speed, then escalates to `Yield` if a pedestrian is present in the crossing zone so that the ego vehicle stops before the yielding line.
   对应摘录：B
