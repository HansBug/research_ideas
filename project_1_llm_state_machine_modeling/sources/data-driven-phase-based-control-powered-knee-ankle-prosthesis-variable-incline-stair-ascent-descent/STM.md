# Data-Driven Phase-Based Control of a Powered Knee-Ankle Prosthesis for Variable-Incline Stair Ascent and Descent - STM 提取记录

## 盘点结论

- 评级：🟢 直接可用
- 文件级角色：🪫 主要用于降采样池
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：连续耦合
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 variable-incline stair ascent/descent HKIC 控制器的 phase selection 明确写成 `S1-S5` FSM，并给出 `FS / MHE / TO / MHF` 与大腿速度阈值 guard，可提取为双 A 样本；因与既有膝踝假肢相位簇相近，归入降采样保留。

## 条目 1: Five-state stair ascent/descent HKIC phase supervisor for a powered knee-ankle prosthesis

- 控制对象：医疗设备与生命支持控制领域的主动膝踝假肢楼梯上下行 HKIC 相位监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：连续耦合
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：🪫 降采样保留
- 趋同标签：🔁 强趋同（膝踝假肢步态相位）

### 0. 条目识别与判定

- 一句话说明：这是一个用于主动膝踝假肢楼梯上行和下行的五态相位监督器，在 `S1-S3` 支撑相和 `S4-S5` 摆动相之间切换 stance/swing phase variable，并驱动 HKIC 阻抗与运动学输出。
- 判断：算。对象是真实主动假肢控制器；原文明确给出 `S1-S5` 状态、`FS`、`MHE`、`TO`、`MHF`、大腿角与速度阈值、`10 ms / 40 ms` 滤波检测，以及状态相关的 stance impedance 和 swing kinematic control。

### 1. 原文摘录

#### 摘录 A

- 出处：第 1 页，Abstract
> This work presents a phase-based hybrid kinematic and impedance controller (HKIC) that allows for semi-volitional, biomimetic stair ascent and descent at a variety of step heights. We define a unified phase variable for both stair ascent and descent that utilizes lower-limb geometry to adjust to different users and step heights. ... Experiments with above-knee amputee participants (N=2) validate that our HKIC controller produces biomimetic ascent and descent joint kinematics, kinetics, and work across four step height configurations.

#### 摘录 B

- 出处：第 3 页，Section `III. Unified Stair Phase Variable`
> An FSM governs changes between phase variable definitions at biologically-inspired thresholds, such as maximum hip extension (MHE) or toe-off (TO). Fig. S1 shows the state transition criteria, with states S1 through S3 corresponding to stance and states S4 and S5 corresponding to swing. The redundant state in stance, S2, acts as a threshold to prevent premature MHE detection ... The feed-forward state S5 is a notable addition to our state machine from our previous stair ascent controller.

#### 摘录 C

- 出处：第 3-4 页，Section `Stance Phase Variable Definition`
> Our FSM begins in S1 after FS is detected. ... The FSM stays in S1 as thigh angle decreases until a threshold s1->2 = 0.85 * sMHE_st is reached ... MHE detection is only done in S2, where we employ a fast (10 ms) and slow (40 ms) simple moving average minima detection algorithm ... After MHE occurs, the FSM transitions to S3 for the remainder of stance. ... After the loss of FC, the stance phase estimate is saturated at 1 for the remainder of the gait cycle (during S4 and S5).

#### 摘录 D

- 出处：第 4 页，Section `Swing Phase Variable Definition`
> Following TO, the FSM transitions from S3 to S4 ... The FSM transitions from S4 to S5 at thigh velocity of theta_dot_th <= 0.75 rad/s and theta_th greater than or equal to theta_th_4->5. ... After transitioning from S4 to S5, a feed-forward phase definition ... is used ... At FS, the state machine transitions from S5 to S1 and the process repeats for the next stair stride.

#### 摘录 E

- 出处：第 4-5 页，Sections `Swing Kinematic Controller` and `Stance Impedance Model`
> Time-based interpolation between tau_st and tau_sw is performed at each FS and TO to ensure a smooth transition ... we build a polynomial-based piecewise-linear impedance model for both the knee and ankle during stair ascent and descent. The model is parameterized by the user's completion fraction of the stance phase s_st and the stairstep height gamma ...

### 2. 基于原文整理后的自然语言描述

The powered knee-ankle prosthesis uses a five-state EFSM to supervise a hybrid kinematic and impedance controller for both stair ascent and stair descent across variable step heights. `S1`, `S2`, and `S3` are stance states: the FSM starts in `S1` after foot strike, moves to `S2` only after the stance phase crosses `0.85 * sMHE_st`, detects `MHE` in `S2` using fast `10 ms` and slow `40 ms` moving-average minima filters, and then switches to `S3` for the rest of stance. After loss of foot contact or toe-off, the machine enters `S4`, where the swing phase variable follows the rising thigh-angle trajectory until a guard combining thigh velocity `<= 0.75 rad/s` and a thigh-angle threshold triggers `S5`. `S5` is a feed-forward swing state that prevents premature phase saturation and returns to `S1` at the next foot strike. The state-selected phase estimates feed two different low-level outputs: stance states parameterize stair-height-dependent knee and ankle impedance, while swing states drive kinematic joint tracking, with interpolation at foot strike and toe-off smoothing the transitions.

### 3. 逐句溯源

1. 句子 1：The powered knee-ankle prosthesis uses a five-state EFSM to supervise a hybrid kinematic and impedance controller for both stair ascent and stair descent across variable step heights.
   对应摘录：A, B
2. 句子 2：`S1`, `S2`, and `S3` are stance states: the FSM starts in `S1` after foot strike, moves to `S2` only after the stance phase crosses `0.85 * sMHE_st`, detects `MHE` in `S2` using fast `10 ms` and slow `40 ms` moving-average minima filters, and then switches to `S3` for the rest of stance.
   对应摘录：B, C
3. 句子 3：After loss of foot contact or toe-off, the machine enters `S4`, where the swing phase variable follows the rising thigh-angle trajectory until a guard combining thigh velocity `<= 0.75 rad/s` and a thigh-angle threshold triggers `S5`.
   对应摘录：C, D
4. 句子 4：`S5` is a feed-forward swing state that prevents premature phase saturation and returns to `S1` at the next foot strike.
   对应摘录：B, D
5. 句子 5：The state-selected phase estimates feed two different low-level outputs: stance states parameterize stair-height-dependent knee and ankle impedance, while swing states drive kinematic joint tracking, with interpolation at foot strike and toe-off smoothing the transitions.
   对应摘录：A, E
