# Autonomous Driving in Urban Environments: Boss and the Urban Challenge - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `Boss` 的城市自动驾驶行为执行层拆成 `road / intersection / zone` 三类上下文，并给出了 precedence、yield window、gridlock timeout 和 recovery escalation，足以形成高质量 `🚗` 方向 HSM 样本。

## 条目 1: Three-Context Urban Driving Behavioral Executive

- 控制对象：汽车与道路车辆领域的城市自动驾驶行为执行器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是 `Boss` 自动驾驶车辆位于 mission planner 与 motion planner 之间的行为执行层，用来在道路、交叉口和 zone/parking 场景下切换不同子行为，并在阻塞、yield、gridlock 与失败时升级恢复策略。
- 判断：算。对象是实际城市自动驾驶系统的高层行为控制器，原文明确给出分层上下文、子行为职责、时窗计算、1 秒 hysteresis、15 秒 gridlock timeout 与多级 recovery 规则，不是泛泛的架构概述。

### 1. 原文摘录

#### 摘录 A

- 出处：第 2 页，Abstract
> A three-layer planning system combines mission, behavioral, and motion planning to drive in urban environments. The mission planning layer considers which street to take to achieve a mission goal. The behavioral layer determines when to change lanes and precedence at intersections and performs error recovery maneuvers.

#### 摘录 B

- 出处：第 20-21 页，Section 6 `Behavioral subsystem`
> The behavioral architecture is based on the concept of identifying a set of driving contexts, each of which requires the vehicle to focus on a reduced set of environmental features. At the highest level of this design, the three contexts are road, intersection, and zone, and their corresponding behaviors are, respectively, lane driving, intersection handling, and achieving a zone pose. ... two subbehaviors making up the auxiliary goal selection behavior ... play a crucial role not only in standard operation but also in error recovery.

#### 摘录 C

- 出处：第 21-23 页，Section 6.1 `Intersections and Yielding`
> The precedence estimator is most directly responsible for the system’s adherence to the Urban Challenge rules ... including obeying precedence, not entering an intersection when another vehicle is in it, and being able to merge into and across moving traffic. ... This state is used as a gate condition in the transition manager and triggers the issuance of the motion goal to proceed through the intersection.
>
> Precedence between any two exit way points is determined first by whether the exit way points are stop lines. ... Among stop line exit way points, precedence is determined by arrival times, where earlier arrivals have precedence over later arrivals.

#### 摘录 D

- 出处：第 24-25 页，Section 6.1.2 `Yielding`
> Trequired = Taction + Tdelay + Tspacing ... In the case of merging into a lane, the required window is extended to include the acceleration time, if necessary, as Trequired = max(Taction, Taccelerate) + Tdelay + Tspacing. ... The yield window for the overall intersection action is considered to be instantaneously open when Tcurrent > Trequired for all yield lanes. ... all yield windows must be continuously open for at least 1 s before yield clearance is passed to the rest of the system.

#### 摘录 E

- 出处：第 25-30 页，Section 6.1.3 `Gridlock Management` / Section 6.3 `Error Recovery`
> Gridlock management comes into effect once the system determines that Boss has precedence at the current intersection and begins with a 15-s timeout to give the problematic vehicle an opportunity to clear. If still gridlocked after 15 s, the current intersection action is marked as locally high cost, and the mission planner is allowed to determine whether an alternate path to goal exists.
>
> Success resets recovery level to zero ... Failure sets the recovery level to one greater than the maximum of the cached and current recovery level. ... the robot must move a minimum distance toward the goal over some span of time. If it does not, the current goal is treated as a failure, and the recovery level is incremented.

### 2. 基于原文整理后的自然语言描述

The `Boss` behavioral executive is a hierarchical urban-driving supervisor that sits between mission planning and motion planning and dispatches different subbehaviors according to the current driving context. At the top level it classifies operation into `road`, `intersection`, and `zone`, which are implemented respectively by lane driving, intersection handling, and zone-pose achievement, while an auxiliary goal-selection branch coordinates execution and recovery. Inside the intersection context, the controller uses a precedence estimator and transition manager to gate when the vehicle may proceed, ordering stop-line exits by modified arrival times and checking whether the intersection is clear. For moving-traffic merges, it computes a required temporal window from `Taction`, `Tdelay`, `Tspacing`, and, when needed, `Taccelerate`, and it only accepts yield clearance after all relevant windows stay open for at least `1 s`. If the post-intersection path remains blocked for `15 s`, the executive escalates from nominal behavior to rerouting or generalized-pose recovery, while a cached recovery level governs how aggressively later shimmy/jimmy/shake/bake maneuvers are chosen.

### 3. 逐句溯源

1. 句子 1：The `Boss` behavioral executive is a hierarchical urban-driving supervisor that sits between mission planning and motion planning and dispatches different subbehaviors according to the current driving context.
   对应摘录：A, B
2. 句子 2：At the top level it classifies operation into `road`, `intersection`, and `zone`, which are implemented respectively by lane driving, intersection handling, and zone-pose achievement, while an auxiliary goal-selection branch coordinates execution and recovery.
   对应摘录：B
3. 句子 3：Inside the intersection context, the controller uses a precedence estimator and transition manager to gate when the vehicle may proceed, ordering stop-line exits by modified arrival times and checking whether the intersection is clear.
   对应摘录：C
4. 句子 4：For moving-traffic merges, it computes a required temporal window from `Taction`, `Tdelay`, `Tspacing`, and, when needed, `Taccelerate`, and it only accepts yield clearance after all relevant windows stay open for at least `1 s`.
   对应摘录：D
5. 句子 5：If the post-intersection path remains blocked for `15 s`, the executive escalates from nominal behavior to rerouting or generalized-pose recovery, while a cached recovery level governs how aggressively later shimmy/jimmy/shake/bake maneuvers are chosen.
   对应摘录：E
