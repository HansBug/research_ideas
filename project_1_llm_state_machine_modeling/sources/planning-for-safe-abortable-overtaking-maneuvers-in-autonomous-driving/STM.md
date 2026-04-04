# Planning for Safe Abortable Overtaking Maneuvers in Autonomous Driving - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：FSM（有限状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把超车行为规划明确写成 `Lane Keeping / Follow / Overtake / Abort` 四态 FSM，并把感知事件、回退条件和同一套 MPC 轨迹生成链条都落到了正文里。

## 条目 1: Lane-Keep Follow-Overtake-Abort Planner FSM

- 控制对象：双向道路场景中的自动驾驶车辆超车行为与轨迹规划器
- 状态机类型：FSM（有限状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向真实道路超车任务的自动驾驶行为规划器，用四态离散机动链决定保持车道、跟车、超车或中止回退，并把状态输出交给同一套轨迹规划器。
- 判断：算。对象是实际自动驾驶车辆的行为控制器，原文直接给出状态集合、事件触发条件、状态内参考量定义，以及一次“超车后中止再重试”的完整运行链。

### 1. 原文摘录

#### 摘录 A

- 出处：第 3-4 页，`III.B.2 Rule-Based Finite State Machines`，`paper_content.txt` 第 251-329 行
> The approach for the selection of the maneuver was kept simple by using an FSM since this study primarily focuses on the planning of overtaking and aborting maneuvers. ... The planner state machine `M` is written as: `M = (H, Σ, δ, s0)`, where `H = {L, F, O, A}` is the set of states corresponding to maneuvers, `Σ` is the set of input symbols corresponding to perceptual events triggering state transitions, `δ` is the state transition function, and `s0` is the initial state.
>
> `L` - Lane Keeping ... `F` - Follow Lead Vehicle ... `O` - Overtaking ... `A` - Aborting ... State transitions are triggered by perceptual events corresponding to input symbols `Σ = {σ1, σ2, σ3, σ4, σ5}`. ... `σ1` when the EV detects a vehicle less than a fixed distance away ... `σ2` when situations are favourable for overtaking ... `σ3` when overtaking is successfully completed ... `σ4` when potential collision before completion of the overtake is predicted ... `σ5` the aborting of the overtake maneuver is complete such that the EV has merged back to the lane behind the LV.

#### 摘录 B

- 出处：第 6 页，`IV. Experimental Evaluation / Figure 6`，`paper_content.txt` 第 482-500 行
> At `t = 0s`, the EV is at rest and accelerates to attain the desired speed ... When the EV detects the LV as it falls into its sensing range, the EV decelerates to match the velocity of LV ... and follows while keeping a safe distance. At `t = 9.9s` overtaking is initiated. ... At `t = 12.8s` abort is initiated due to potential collision event suggesting unsafe overtake conditions. The EV rapidly decelerates ... and safely merge back to lane again while keeping a safe distance from the LV. After a successful merge, the EV again switches to follow mode. At `t = 23.7s`, the overtake is again attempted ... When the EV is at a safe distance in front of the LV it merges to the lane and resumes lane keeping mode.

### 2. 基于原文整理后的自然语言描述

The overtaking planner is organized as a four-state FSM with `L`, `F`, `O`, and `A`, corresponding to lane keeping, following a lead vehicle, overtaking, and aborting the pass. Each state supplies its own maneuver-specific reference pose and velocity to the same trajectory-generation stack, so the planner does not swap controllers when it switches between cruising, following, passing, and merging back. The transitions are triggered by perceptual events such as detecting a lead vehicle in sensing range, finding favorable overtaking conditions, successfully passing the lead vehicle, predicting a collision during the pass, and completing the merge-back behind the lead vehicle. In the reported run, the ego vehicle starts in lane keeping, enters follow mode after detecting the lead vehicle, initiates overtaking, aborts at `t = 12.8 s` under unsafe predicted conditions, returns to follow mode, reattempts the pass, and finally resumes lane keeping after safely merging ahead of the lead vehicle.

### 3. 逐句溯源

1. 句子 1：The overtaking planner is organized as a four-state FSM with `L`, `F`, `O`, and `A`, corresponding to lane keeping, following a lead vehicle, overtaking, and aborting the pass.
   对应摘录：A
2. 句子 2：Each state supplies its own maneuver-specific reference pose and velocity to the same trajectory-generation stack, so the planner does not swap controllers when it switches between cruising, following, passing, and merging back.
   对应摘录：A
3. 句子 3：The transitions are triggered by perceptual events such as detecting a lead vehicle in sensing range, finding favorable overtaking conditions, successfully passing the lead vehicle, predicting a collision during the pass, and completing the merge-back behind the lead vehicle.
   对应摘录：A
4. 句子 4：In the reported run, the ego vehicle starts in lane keeping, enters follow mode after detecting the lead vehicle, initiates overtaking, aborts at `t = 12.8 s` under unsafe predicted conditions, returns to follow mode, reattempts the pass, and finally resumes lane keeping after safely merging ahead of the lead vehicle.
   对应摘录：B
