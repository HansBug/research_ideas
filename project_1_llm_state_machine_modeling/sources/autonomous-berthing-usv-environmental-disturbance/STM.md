# Model Reference Adaptive Control-Based Autonomous Berthing of an Unmanned Surface Vehicle under Environmental Disturbance - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：显式时钟
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 USV 靠泊过程显式拆成 parallel/finger 两类状态机，并给出距离阈值、方向切换、低速 docking 与 `3 s` 完成判定，控制主链清楚且可追溯。

## 条目 1: Parallel/finger autonomous berthing supervisor

- 控制对象：通用控制与无人船靠泊领域的自主靠泊监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：显式时钟
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 underactuated small USV 的高层 berthing supervisor，用 parallel-type 和 finger-type 两套状态机组织 approach、alignment tracking 和 final docking。
- 判断：算。对象是真实无人船靠泊控制器，不是纯连续控制推导；原文明确给出状态集合、距离 guard、倒车/减速动作和“误差维持 3 秒”完成判定。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract，行 15-25
> A state-machine approach is proposed to solve state transitions in the berthing step.
> ... a systematic approach for the autonomous berthing of a USV is proposed.
> ... an accurate and stable docking of small USVs became achievable.

#### 摘录 B

- 出处：第 3-4 页，Section `2. Berthing Path Planning`，行 163-182
> Figure 3 shows the state machines of the parallel and finger types ...
> The parallel-type docking starts from the approach state.
> ... if the distance between the USV and the destination is smaller than the length of the USV, it proceeds to the next state—the alignment tracking state.
> ... if the distance to the docking target point is smaller than the length of the USV, the docking process proceeds to the next state, i.e., the docking state.
> If the distance error from the berthing arrival point does not exceed 10% of the USV’s length and lasts for more than 3 s, docking is judged to be completed.

#### 摘录 C

- 出处：第 4-5 页，Section `2. Berthing Path Planning`，行 193-206
> The finger-type approach is also the same state as À ...
> ... the docking process transitions to the next state. The forward-alignment tracking state ...
> ... That is the back-alignment tracking state ...
> ... the docking state ...
> When the distance error from the final destination to the USV does not exceed 10% of the USV’s length for more than 3 s, berthing is judged to be completed.

#### 摘录 D

- 出处：第 5-6 页，Section `3. Control System`，行 207-233
> For a USV to accurately berth, it is necessary to accurately follow the planned path.
> ... path tracking was performed using vector-field path following ...
> The heading angle of the USV was controlled through a PID controller ... In this study, the adaptive gain was tuned through adaptive control ...

### 2. 基于原文整理后的自然语言描述

The paper models autonomous USV berthing as an explicit state-transition process rather than as a single monolithic controller, and it provides two separate supervisors for `parallel` and `finger` docking layouts. In the parallel type, the machine moves from `approach` to `alignment tracking` when the vessel reaches the path-turning point, then enters `docking` once the docking target is within one USV length, and finally declares success only if the residual position error stays within `10%` of the vessel length for more than `3 s`. The finger type uses a richer sequence: `approach -> forward-alignment tracking -> back-alignment tracking -> docking`, so that the vessel can first swing into a backward berthing posture and then retreat into the final target. These state transitions are guarded by geometric distances such as `dA / dF / dC / d0` and by the time-based completion condition, while the low-level path following and heading regulation are delegated to vector-field guidance plus PID/MRAC control. The result is an EFSM-like docking supervisor that cleanly separates route-stage logic from continuous steering and thrust control.

### 3. 逐句溯源

1. 句子 1：The paper models autonomous USV berthing as an explicit state-transition process rather than as a single monolithic controller, and it provides two separate supervisors for `parallel` and `finger` docking layouts.
   对应摘录：A, B, C
2. 句子 2：In the parallel type, the machine moves from `approach` to `alignment tracking` when the vessel reaches the path-turning point, then enters `docking` once the docking target is within one USV length, and finally declares success only if the residual position error stays within `10%` of the vessel length for more than `3 s`.
   对应摘录：B
3. 句子 3：The finger type uses a richer sequence: `approach -> forward-alignment tracking -> back-alignment tracking -> docking`, so that the vessel can first swing into a backward berthing posture and then retreat into the final target.
   对应摘录：C
4. 句子 4：These state transitions are guarded by geometric distances such as `dA / dF / dC / d0` and by the time-based completion condition, while the low-level path following and heading regulation are delegated to vector-field guidance plus PID/MRAC control.
   对应摘录：B, C, D
5. 句子 5：The result is an EFSM-like docking supervisor that cleanly separates route-stage logic from continuous steering and thrust control.
   对应摘录：A, D
