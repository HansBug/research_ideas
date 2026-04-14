# Algorithmic Approaches to Enhance Safety in Autonomous Vehicles: Minimizing Lane Changes and Merging - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文虽然是算法与仿真导向，但直接公开了 `Idle / Waiting / Moving Left / Moving Right` 四态、布尔 guard、回退条件和伪代码断言，足够形成一条紧凑但完整的自动驾驶换道决策 FSM。

## 条目 1: MLCA four-state lane-change decision controller

- 控制对象：自动驾驶车辆的 MLCA 换道决策控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个根据是否需要换道、是否允许继续等待以及左右相邻车道是否存在安全 gap，在 `Idle / Waiting / Moving Left / Moving Right` 间切换的自动驾驶决策 FSM。
- 判断：算。对象是自动驾驶高层 lane-change decision controller，而不是纯交通仿真指标；原文直接给出状态图、Boolean trigger 语义、状态转移条件和伪代码约束。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，摘要，`paper_content.txt` 第 14-30 行
> This paper proposes the Minimizing Lane Change Algorithm (MLCA), a finite-state-machine controller that defers non-safety-critical lane changes to maintain lane stability ... Compared to the LC2017 and MOBIL models, MLCA achieved a 35% reduction in lane-change events and a 28% decrease in collision occurrences ...

#### 摘录 B

- 出处：第 3 页，Figure 1 及图注，`paper_content.txt` 第 221-231 行
> Finite-state machine diagram for AV lane-change decision logic.
>
> States: Idle (no active request), Waiting (evaluating safety gaps), Moving Left/Right (executing lane-change maneuver). Boolean triggers: N (lane-change needed), W (waiting timeout), L/R (safe gap on left/right). Solid arrows indicate conditional transitions; loops represent state persistence or fallback logic based on gap availability or timeout.

#### 摘录 C

- 出处：第 3-4 页，Section `B. MLCA Algorithm` 与 `Algorithm 1`，`paper_content.txt` 第 261-288, 302-344 行
> The algorithm defines four distinct operational states: Idle, Waiting, Moving Left, and Moving Right. The transitions between states are dictated by a set of Boolean variables: N (Need to Move), W (Can Wait), L (Left Side Empty), and R (Right Side Empty).
>
> A transition occurs from the Idle state to the Waiting state if there is a need to move AND the AV can wait (N AND W). Similarly, the AV transitions to the Moving Left or Moving Right states if movement is necessary AND the respective adjacent lane is clear (N AND L or N AND R).
>
> ... if current_state = WAITING then if N ∧ (L ∨ R) then current_state ← IDLE ...
>
> Assert: ¬N => current_state = IDLE ... current_state = MOVING LEFT => (N ∧ L) ... current_state = MOVING RIGHT => (N ∧ R).

### 2. 基于原文整理后的自然语言描述

The MLCA controller is a finite-state movement-decision machine for an autonomous vehicle in a multi-lane environment, and it defines four states: `Idle`, `Waiting`, `Moving Left`, and `Moving Right`. Its guards are four Boolean variables: `N` for whether a lane change is needed, `W` for whether the vehicle can keep waiting, and `L` and `R` for whether the left or right neighbouring lane currently offers a safe gap. From `Idle`, the controller goes to `Waiting` on `N ∧ W`, to `Moving Left` on `N ∧ L`, and to `Moving Right` on `N ∧ R`, which means lane changes are deferred unless they are both necessary and currently feasible. In `Waiting`, once the request is withdrawn or a neighbouring gap becomes available for re-evaluation, the machine falls back to `Idle`; the two motion states persist only while the corresponding need-and-gap condition remains true and otherwise also return to `Idle`. Together with the pseudocode assertions `¬N => IDLE`, `MOVING LEFT => N∧L`, and `MOVING RIGHT => N∧R`, the paper exposes a compact but complete autonomous-driving lane-change FSM whose purpose is to minimize unnecessary merges and preserve lane stability.

### 3. 逐句溯源

1. 句子 1：The MLCA controller is a finite-state movement-decision machine for an autonomous vehicle in a multi-lane environment, and it defines four states: `Idle`, `Waiting`, `Moving Left`, and `Moving Right`.
   对应摘录：A, B, C
2. 句子 2：Its guards are four Boolean variables: `N` for whether a lane change is needed, `W` for whether the vehicle can keep waiting, and `L` and `R` for whether the left or right neighbouring lane currently offers a safe gap.
   对应摘录：B, C
3. 句子 3：From `Idle`, the controller goes to `Waiting` on `N ∧ W`, to `Moving Left` on `N ∧ L`, and to `Moving Right` on `N ∧ R`, which means lane changes are deferred unless they are both necessary and currently feasible.
   对应摘录：A, C
4. 句子 4：In `Waiting`, once the request is withdrawn or a neighbouring gap becomes available for re-evaluation, the machine falls back to `Idle`; the two motion states persist only while the corresponding need-and-gap condition remains true and otherwise also return to `Idle`.
   对应摘录：B, C
5. 句子 5：Together with the pseudocode assertions `¬N => IDLE`, `MOVING LEFT => N∧L`, and `MOVING RIGHT => N∧R`, the paper exposes a compact but complete autonomous-driving lane-change FSM whose purpose is to minimize unnecessary merges and preserve lane stability.
   对应摘录：A, C
