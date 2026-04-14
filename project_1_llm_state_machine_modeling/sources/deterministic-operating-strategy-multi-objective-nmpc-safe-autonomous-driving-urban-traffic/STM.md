# Deterministic Operating Strategy for Multi-objective NMPC for Safe Autonomous Driving in Urban Traffic - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把城市自动驾驶的 `NMPC` 运行序列写成 `XP / PF / PU / SS / NP / ND` 六状态 FSM，并给出 `t1-t7` 条件、优先级顺序和与连续优化问题的耦合方式，足以形成双 A 的驾驶模式监督样本。

## 条目 1: XP-PF-PU-SS-NP-ND Urban Driving Supervisor
- 控制对象：汽车与道路车辆控制领域的城市自动驾驶 NMPC 模式监督器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向城市交通的自动驾驶模式监督器，用有限状态机在停车区驶出、正常跟车、慢速跟停、完全静止、入库和终止停车之间切换 `NMPC` 目标与约束。
- 判断：算。对象是实际自动驾驶系统中的高层运行模式控制器；原文不仅给出状态集合和 `t1-t7` 条件，还明确说明不同状态怎样修改 `NMPC` 约束、权重和优先级。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6 页，`Figure 8` 与其下方说明
> The FSM depicted in Figure 8 incorporates the aforementioned driving sequences, with the addition of the state (Standstill), which gets activated when the ego-vehicle drives with a very slow speed v<=0.5 [m/s] to avoid infeasible and aggressive system controls, and the final state (End) which promptly stops the ego-vehicle upon reaching its destination. Also, the conditions for switching between the FSM modes are portrayed in Table 1 with the symbols ti, such that a currently active state remains unchanged when all of its exit conditions are not satisfied.
>
> XP Exit Parking, PF Path Following, PU Pulling Up, SS Standstill, NP Enter Parking, ND End.

#### 摘录 B
- 出处：第 6-8 页，`Exit Parking / Path Following / Pulling Up / Standstill / Enter Parking`
> Exit Parking (XP) ... the condition for leaving the parking area t1 is fulfilled when s >= sXP ... revised to be ... t1 is only fulfilled after passing the transitioning phase threshold sXP;h.
>
> The transition t2 to NP ... implies that we are close to our destination B ...
> The transition t3 to PU denotes that the ego-vehicle travels much slower than the speed limit either due to following a slow leading road user or approaching a traffic jam.
>
> the transition t4 to PF ... t5 to SS ...
> t5 := ... (v <= 0.5 [m/s]) ^ (a <= 0 [m/s2])
>
> t6 := (srel >= sSF + sSF;h) _ (OinLN = /0)
>
> the transition t7 to the final state ND ... (sf - s <= sND -> t7 = 1)

#### 摘录 C
- 出处：第 7-8 页，状态与 `NMPC` 耦合说明
> Path Following (PF). This is the core urban driving sequence, where the ego-vehicle travels with an admissible speed and tries to maximize the traveled distance to its destination ... the turning curvature is restricted more than XP ...
>
> Pulling Up (PU). This sequence is not only suitable for following slow road users or approaching stationary ones, but can also be used for stopping at traffic lights ...
>
> Finally, it is worth mentioning that the proposed FSM architecture is loosely coupled with the NMPC ...

### 2. 基于原文整理后的自然语言描述

The urban-driving supervisor is a six-state FSM with `Exit Parking (XP)`, `Path Following (PF)`, `Pulling Up (PU)`, `Standstill (SS)`, `Enter Parking (NP)`, and `End (ND)` states that organizes the operating strategy of a multi-objective NMPC controller. The machine starts in `XP`, where the vehicle leaves the parking area under tighter speed and curvature assumptions, and only switches to `PF` after passing the relaxed parking-exit threshold `sXP;h`. In `PF`, the highest-priority exit is `t2` toward `NP` when the destination region is near, while `t3` sends the system to `PU` when the ego vehicle is much slower than the speed limit because of a slow leader or an approaching traffic jam. `PU` then either returns to `PF` through `t4` when speed recovers, or enters `SS` through `t5` when the vehicle is already decelerating and its speed drops to at most `0.5 m/s`; `SS` returns to `PU` only when the safety gap reopens or the leading object disappears. The supervisor is tightly coupled to the NMPC problem formulation because each state changes the admissible speed, turning curvature, safety weighting, or stopping behavior, and the final `NP -> ND` transition directly triggers prompt deceleration at the destination.

### 3. 逐句溯源

1. 句子 1：The urban-driving supervisor is a six-state FSM with `Exit Parking (XP)`, `Path Following (PF)`, `Pulling Up (PU)`, `Standstill (SS)`, `Enter Parking (NP)`, and `End (ND)` states that organizes the operating strategy of a multi-objective NMPC controller.
   对应摘录：A
2. 句子 2：The machine starts in `XP`, where the vehicle leaves the parking area under tighter speed and curvature assumptions, and only switches to `PF` after passing the relaxed parking-exit threshold `sXP;h`.
   对应摘录：B, C
3. 句子 3：In `PF`, the highest-priority exit is `t2` toward `NP` when the destination region is near, while `t3` sends the system to `PU` when the ego vehicle is much slower than the speed limit because of a slow leader or an approaching traffic jam.
   对应摘录：B
4. 句子 4：`PU` then either returns to `PF` through `t4` when speed recovers, or enters `SS` through `t5` when the vehicle is already decelerating and its speed drops to at most `0.5 m/s`; `SS` returns to `PU` only when the safety gap reopens or the leading object disappears.
   对应摘录：A, B
5. 句子 5：The supervisor is tightly coupled to the NMPC problem formulation because each state changes the admissible speed, turning curvature, safety weighting, or stopping behavior, and the final `NP -> ND` transition directly triggers prompt deceleration at the destination.
   对应摘录：B, C
