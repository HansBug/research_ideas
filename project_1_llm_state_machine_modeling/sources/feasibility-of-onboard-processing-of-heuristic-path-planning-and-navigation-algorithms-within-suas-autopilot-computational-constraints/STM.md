# Feasibility of Onboard Processing of Heuristic Path Planning and Navigation Algorithms within SUAS Autopilot Computational Constraints - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文最终把 SUAS 目标跟踪启发式控制写成三态 FSM，并结合 `Jthreshold` 与 slant-range 条件给出清晰的状态切换与缓冲参数，适合作为航空航天方向的在线启发式监督样本。

## 条目 1: Three-State Heuristic Stand-off Tracking FSM

- 控制对象：航空航天与飞行控制领域的 SUAS 移动目标启发式跟踪控制器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 SUAS 跟踪移动地面目标的在线启发式控制器，用 `Initial State Check / Standard Target Tracking / Low Range Target Tracking / High Range Target Tracking` 等状态在 slant range 偏差与 `J_i` 变化下切换不同跟踪强度。
- 判断：算。对象是实际 UAV autopilot 上执行的目标跟踪逻辑，而不是离线最优控制分析；原文给出了 revised FSM 图、阈值参数、状态切换动机以及飞行中三态均被实际进入的验证结论。

### 1. 原文摘录

#### 摘录 A

- 出处：第 6 页，Abstract，`paper_content.txt` 第 188-193 行
> Finally, a state-based heuristic navigation strategy is designed, developed, and tested that approximates optimal path solutions and can be used for real-time execution. A 66% improvement in mean performance is achieved over default target tracking methods.

#### 摘录 B

- 出处：第 29-30 页，Methodology，`paper_content.txt` 第 1002-1003、1037-1041 行
> Finally, a finite state machine approach to path planning is constructed with design based on analysis of flights flown at the aforementioned best settings. ... In order to develop navigation logic in the form of a finite state machine that is responsive to real-time SUAS conditions, the existing performance is examined to identify which states warrant alternative behavior.

#### 摘录 C

- 出处：第 58 页，Figure `29: Revised Finite State Machine`，回 PDF 图面核对
> `Initial State Check`; `Standard Target Tracking`; `Low Range Target Tracking`; `High Range Target Tracking`.

#### 摘录 D

- 出处：第 57-60 页，FSM second iteration / validation，`paper_content.txt` 第 1653-1668、1685-1694 行
> A second iteration FSM was proposed that, when appropriate, attempted to diminish the effects of this scenario by scaling the level of effort being used to maintain slant range. ... The second iteration FSM was implemented on the APM with `Jthreshold = 0.003` and control effort buffer set to `35 m` ... While the profile shows that the best setting for state transition conditions may require further experimentation, it does validate that all three states were entered at various points throughout the course of flight.

### 2. 基于原文整理后的自然语言描述

The paper implements a real-time heuristic tracking controller as a small finite-state machine instead of relying only on one static follow-me policy. The revised FSM begins with `Initial State Check` and then spends most of the mission in `Standard Target Tracking`, which represents the nominal loiter-based tracking behavior. When slant-range and `J_i` conditions indicate that the aircraft has fallen too far inside the desired orbit, the controller switches to `Low Range Target Tracking`; when the aircraft has overrun the target and remains too far outside the desired stand-off, it switches to `High Range Target Tracking`. The second-iteration design makes these switches with an explicit `Jthreshold = 0.003` and a `35 m` control-effort buffer around the desired `150 m` radius, so the alternate states are only entered when the deviation is meaningful rather than on every small oscillation. Flight profiling later confirms that all three tracking states were actually visited, and the paper argues that the two alternate states help return the SUAS to low `J_i` and low slant-range error conditions.

### 3. 逐句溯源

1. 句子 1：The paper implements a real-time heuristic tracking controller as a small finite-state machine instead of relying only on one static follow-me policy.
   对应摘录：A, B
2. 句子 2：The revised FSM begins with `Initial State Check` and then spends most of the mission in `Standard Target Tracking`, which represents the nominal loiter-based tracking behavior.
   对应摘录：C, D
3. 句子 3：When slant-range and `J_i` conditions indicate that the aircraft has fallen too far inside the desired orbit, the controller switches to `Low Range Target Tracking`; when the aircraft has overrun the target and remains too far outside the desired stand-off, it switches to `High Range Target Tracking`.
   对应摘录：C, D
4. 句子 4：The second-iteration design makes these switches with an explicit `Jthreshold = 0.003` and a `35 m` control-effort buffer around the desired `150 m` radius, so the alternate states are only entered when the deviation is meaningful rather than on every small oscillation.
   对应摘录：D
5. 句子 5：Flight profiling later confirms that all three tracking states were actually visited, and the paper argues that the two alternate states help return the SUAS to low `J_i` and low slant-range error conditions.
   对应摘录：D
