# A Compact, Lightweight Robotic Ankle-Foot Prosthesis: Featuring a Powered Polycentric Design - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 powered polycentric ankle-foot prosthesis 的 `ambulation-mode FSM -> stance1/stance2/swing FSM -> low-level control` 三层链路写得清楚，可直接作为层次化踝足假肢控制样本。

## 条目 1: Hierarchical three-phase controller for walking and stair ascent in the powered polycentric ankle-foot prosthesis
- 控制对象：多心踝足主动假肢在 walking / stair ascent 两种模式下运行的分层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 powered ankle-foot prosthesis 的分层控制架构，上层决定 ambulation mode，中层运行 `stance 1 / stance 2 / swing` 三态机，底层在支撑期用 torque control、摆动期用 minimum-jerk position control。
- 判断：算。对象是真实踝足假肢控制器，原文给出了层次结构、状态集合、GRF/角度/角速度 guard、以及 swing duration 如何按上一支撑相时长自适应。

### 1. 原文摘录

#### 摘录 A
- 出处：第 10 页，Section `Control System`
> The proposed control system is based on a hierarchical architecture. At the highest level, a finite-state machine determines which ambulation mode the user wants to perform. For each ambulation mode, a different midlevel controller is implemented. Finally, at the lowest level, a position controller and a torque controller are used in the swing and stance phases, respectively.

#### 摘录 B
- 出处：第 10 页，Section `Control System`
> The walking- and stair-ascent controllers are conceptually divided into stance and swing. In the stance phase, we impose a virtual impedance ... Furthermore, we divide stance into two energetically passive phases and use the transition between these two phases to inject positive energy into the gait cycle. A finite-state machine is used to transition between stances 1 and 2 and the swing phase. The same finite-state machine is used for walking and stair ascent, although with different transition conditions and impedance parameters. In the swing phase, we use a minimum-jerk controller ... The duration of the swing trajectory is automatically adjusted to the user’s cadence based on the duration of the previous stance phase.

#### 摘录 C
- 出处：第 25 页，Figure `Figure 8`
> A block diagram of the finite-state machine used for walking and stair ascent. In stance 1, the prosthesis absorbs the impact with the ground, storing and dissipating energy as necessary. For the prosthesis to transition to stance 2, the ankle position must be greater than that of a specific dorsiflexed position, and the ankle velocity must be positive. The prosthesis injects net-positive energy into the gait cycle during stance 2. When the instrumented pyramid detects that the GRF is lower than 5% of the user’s body weight, the controller transitions to swing mode. In swing, a minimum-jerk trajectory is executed ... When the GRF exceeds 5% of the user’s body weight, the finite-state machine transitions to stance 1, initiating a new gait cycle.

### 2. 基于原文整理后的自然语言描述

The powered polycentric ankle-foot prosthesis is controlled by a hierarchical architecture in which a top-level FSM selects the ambulation mode, a mid-level gait controller executes the mode-specific phase logic, and low-level torque or position loops realize the commanded ankle behavior. For both walking and stair ascent, the mid-level controller uses the same three-state skeleton: `stance 1`, `stance 2`, and `swing`. In `stance 1`, the device mainly absorbs impact and stores energy; the transition to `stance 2` requires the ankle to pass a dorsiflexed position threshold while ankle velocity is positive; and `stance 2` is where the prosthesis injects net-positive energy into the gait cycle. The controller switches from stance to swing when the instrumented pyramid reports GRF below `5%` body weight, and it returns to `stance 1` when GRF rises above the same threshold. During `swing`, the prosthesis abandons impedance rendering and instead executes a minimum-jerk ankle trajectory whose duration is adapted online from the duration of the previous stance phase, so the same FSM can accommodate cadence variation while reusing different parameter sets for walking and stair ascent.

### 3. 逐句溯源

1. 句子 1：The powered polycentric ankle-foot prosthesis is controlled by a hierarchical architecture in which a top-level FSM selects the ambulation mode, a mid-level gait controller executes the mode-specific phase logic, and low-level torque or position loops realize the commanded ankle behavior.
   对应摘录：A
2. 句子 2：For both walking and stair ascent, the mid-level controller uses the same three-state skeleton: `stance 1`, `stance 2`, and `swing`.
   对应摘录：B, C
3. 句子 3：In `stance 1`, the device mainly absorbs impact and stores energy; the transition to `stance 2` requires the ankle to pass a dorsiflexed position threshold while ankle velocity is positive; and `stance 2` is where the prosthesis injects net-positive energy into the gait cycle.
   对应摘录：C
4. 句子 4：The controller switches from stance to swing when the instrumented pyramid reports GRF below `5%` body weight, and it returns to `stance 1` when GRF rises above the same threshold.
   对应摘录：C
5. 句子 5：During `swing`, the prosthesis abandons impedance rendering and instead executes a minimum-jerk ankle trajectory whose duration is adapted online from the duration of the previous stance phase, so the same FSM can accommodate cadence variation while reusing different parameter sets for walking and stair ascent.
   对应摘录：B, C
