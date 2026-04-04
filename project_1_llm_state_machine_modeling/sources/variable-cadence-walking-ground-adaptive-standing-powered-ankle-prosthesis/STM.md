# Variable Cadence Walking and Ground Adaptive Standing with a Powered Ankle Prosthesis - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 powered ankle prosthesis 的 `walking FSM + standing FSM + supervisory controller` 及其角度/角速度/载荷近似条件写得非常完整，可直接作为 activity-mode supervisor 样本。

## 条目 1: Hierarchical walking-standing supervisor for the powered ankle prosthesis
- 控制对象：动力踝关节假肢在变步频行走与地形自适应站立之间切换的高层监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个 powered ankle prosthesis 的分层监督器，上层在 `walking` 与 `ground-adaptive standing` 两个活动模式之间切换，下层分别运行四态步行控制和两态站立控制。
- 判断：算。对象是真实下肢假肢控制器，原文明确给出了每个活动模式下的状态集合、阈值触发、状态内阻抗输出，以及 supervisory controller 的跨模式跳转条件。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `B. Impedance-Based Control Design`
> Similar to the structure described by the authors for the control of a transfemoral prosthesis [28], the ankle control system consists of a finite-state machine (FSM) for each activity (e.g., walking, standing), where the behavior within each state is characterized by passive stiffness and damping terms ... Transitions between finite states are triggered by pre-selected thresholds in sensor measurements. A supervisory controller selects which FSM (i.e., activity mode) is active based on the current activity mode and controller state, as well as sensor data.

#### 摘录 B
- 出处：第 4-5 页，Section `C. Walking Activity Mode Controller`
> In the walking activity mode controller, the ankle behavior over a gait cycle can be characterized by four basic functions, which map directly to states in the FSM ... During the early stance phase of gait (state 3), the joint behaves essentially as a damper ... The powered prosthesis emulates a nonlinear spring during middle stance (state 0) ... Late stance (state 1) is initiated when the ankle is dorsiflexed past a predetermined angle ... Once push-off is complete ... the controller enters early swing (state 2) ... Late swing (state 3) begins once the ankle has reached equilibrium ... Late stance (state 1) will terminate automatically, based on either an angle or time condition ... Cadence is measured by recording the time between each heel strike ... The controller switches between appropriate cadence regimes with a 2 step/min hysteresis.

#### 摘录 C
- 出处：第 6 页，Section `D. Ground Adaptive Standing Activity Mode Controller`
> A powered prosthesis also benefits from a ground adaptive standing controller ... comprised of two impedance-based finite states: a support state and a conformal damping state ... The controller executes a transition from the support state to the conformal damping state if the angular velocity of the foot is greater than 30 deg/s while the ankle angle is within 1.5 deg of the equilibrium position ... The controller transitions from the conformal damping phase to the support phase if the estimated foot angular velocity and foot angular acceleration are both approximately zero ... A new equilibrium position is established at each transition from conformal damping to support ... as the mean of the estimated ground slope during the 50 ms prior to the transition ... or as the mean of the ankle angle during the 50 ms prior to the transition.

#### 摘录 D
- 出处：第 6-7 页，Section `E. Supervisory Controller`
> A supervisory controller ... determines which of the two activity controllers, walking or standing, should be active ... The transition to the walking controller can only be made from the support state (state 0) of the standing controller to the late stance state (state 1) of the walking controller ... Switching from the walking controller to the standing controller takes place from middle stance (walking) to support (standing). While in middle stance (state 0), if the absolute angular velocity of the shank is near zero ... for 0.5 s, the controller transitions into the support state of the standing controller.

### 2. 基于原文整理后的自然语言描述

The powered ankle prosthesis is organized as a hierarchical controller in which a supervisory layer selects between a walking FSM and a ground-adaptive standing FSM according to sensor-derived activity conditions. Inside walking mode, one gait cycle is decomposed into four states: `early stance`, `middle stance`, `late stance`, and `early swing/late swing`, with transitions driven by ankle angle, ankle angular velocity, foot angular velocity, and cadence-dependent thresholds. Each walking state renders a different impedance behavior, including damping for heel contact, a nonlinear stiffening spring for middle stance support, a plantarflexion-biased push-off state for powered energy delivery, and a return-to-neutral swing state. Inside standing mode, the prosthesis alternates between `support` and `conformal damping`, using foot velocity, foot acceleration, and 50 ms averages of ground slope or ankle angle to set the equilibrium angle that makes the foot conform to inclines or relaxed postures. The supervisory controller then bridges the two FSMs in a state-aware way: standing can jump into late stance to initiate walking, while walking falls back to standing only after the shank remains nearly stationary for 0.5 s in middle stance.

### 3. 逐句溯源

1. 句子 1：The powered ankle prosthesis is organized as a hierarchical controller in which a supervisory layer selects between a walking FSM and a ground-adaptive standing FSM according to sensor-derived activity conditions.
   对应摘录：A, D
2. 句子 2：Inside walking mode, one gait cycle is decomposed into four states: `early stance`, `middle stance`, `late stance`, and `early swing/late swing`, with transitions driven by ankle angle, ankle angular velocity, foot angular velocity, and cadence-dependent thresholds.
   对应摘录：B
3. 句子 3：Each walking state renders a different impedance behavior, including damping for heel contact, a nonlinear stiffening spring for middle stance support, a plantarflexion-biased push-off state for powered energy delivery, and a return-to-neutral swing state.
   对应摘录：B
4. 句子 4：Inside standing mode, the prosthesis alternates between `support` and `conformal damping`, using foot velocity, foot acceleration, and 50 ms averages of ground slope or ankle angle to set the equilibrium angle that makes the foot conform to inclines or relaxed postures.
   对应摘录：C
5. 句子 5：The supervisory controller then bridges the two FSMs in a state-aware way: standing can jump into late stance to initiate walking, while walking falls back to standing only after the shank remains nearly stationary for 0.5 s in middle stance.
   对应摘录：D
