# Design and clinical implementation of an open-source bionic leg - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 `standing / level-ground / ramp / stair` 多模态 controller、walking 下 `4` 个 gait subphases、standing 下 `2` 个接触态，以及每态的 impedance law 调度方式，可直接作为 `HSM + T0` powered-prosthesis 样本。

## 条目 1: Ambulation-mode and gait-subphase supervisor for the open-source bionic leg
- 控制对象：open-source powered knee-ankle prosthesis 的 high-level ambulation-mode controller
- 状态机类型：HSM（层次状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：🪞 邻近相似

### 0. 条目识别与判定

- 一句话说明：这是一个面向 powered knee-ankle bionic leg 的层次监督控制器，在顶层切换 standing、level-ground、ramp、stair 等 ambulation modes，并在 mode 内再以 gait subphase `FSM` 调度 knee/ankle impedance。
- 判断：算。对象是真实主动膝踝假肢控制器；原文给出了 mode-specific impedance control、四相 gait `FSM`、standing 双态控制以及 state-dependent impedance law。

### 1. 原文摘录

#### 摘录 A
- 出处：第 11 页，Section `Clinical testing`，行 905-917
> We implemented locomotion controllers for standing, level-ground walking, ramp ascent/descent and stair ascent/descent using impedance control; the impedance parameters for each ambulation mode regulated the current to the knee and ankle motors on the basis of the desired torque.
>
> The three tunable impedance parameters for each joint were virtual stiffness `k_j`, virtual equilibrium angle `θ0_j` and virtual damping coefficient `b_j`. The desired joint torque was converted to the desired motor torque using the transmission ratio, and the desired motor current was calculated using equation (3).

#### 摘录 B
- 出处：第 11 页，Section `Clinical testing`，行 918-923
> Within our tuning process, a finite-state machine divided all gait activities (except for standing) into four subphases: `early-to-mid stance`, `late stance`, `swing flexion` and `swing extension`; simple logic on the basis of mechanical sensors within the prosthesis (for example, joint encoders and load sensor) enabled progression through the state machine.
>
> The standing mode controller used only two states—the first was relatively stiff to support the weight of the body when the prosthesis was in contact with the ground and the second enabled the leg to swing freely when it was not in contact with the ground.

#### 摘录 C
- 出处：第 11 页，Section `Clinical testing`，行 920-923
> For `60%` of the states (across all ambulation modes), we held impedance parameters at tuned but constant values. For the remaining `40%` of the states, we modulated the impedance parameters according to ... values from the previous state ... ankle angle ... knee angle ... or modifying joint impedance as a function of decreasing or increasing prosthesis load. These control strategies were used to reduce the number of independent parameters ... and improve transitions between different types of activities.

### 2. 基于原文整理后的自然语言描述

The open-source bionic leg uses a hierarchical supervisory controller in which the top level selects an ambulation mode such as `standing`, `level-ground walking`, `ramp ascent/descent`, or `stair ascent/descent`, and each mode applies knee and ankle impedance control through joint-specific virtual stiffness, equilibrium angle, and damping parameters. Inside every locomotion mode except standing, a gait-phase finite-state machine refines control into four subphases: `early-to-mid stance`, `late stance`, `swing flexion`, and `swing extension`, with progression driven by simple mechanical sensing from prosthesis encoders and the load sensor. Standing is treated separately as a two-state controller, where ground contact selects a stiff support state and loss of contact releases the leg into a free-swing state. Most states keep constant tuned impedance parameters, but a substantial subset modulates impedance according to previous-state values, ankle angle, knee angle, or increasing/decreasing prosthesis load so that transitions between activities remain smooth. This preserves both the mode hierarchy and the intra-mode gait-state machine, making the sample a clear `HSM + T0` powered-prosthesis controller rather than a single flat impedance law.

### 3. 逐句溯源

1. 句子 1：The open-source bionic leg uses a hierarchical supervisory controller in which the top level selects an ambulation mode such as `standing`, `level-ground walking`, `ramp ascent/descent`, or `stair ascent/descent`, and each mode applies knee and ankle impedance control through joint-specific virtual stiffness, equilibrium angle, and damping parameters.
   对应摘录：A
2. 句子 2：Inside every locomotion mode except standing, a gait-phase finite-state machine refines control into four subphases: `early-to-mid stance`, `late stance`, `swing flexion`, and `swing extension`, with progression driven by simple mechanical sensing from prosthesis encoders and the load sensor.
   对应摘录：B
3. 句子 3：Standing is treated separately as a two-state controller, where ground contact selects a stiff support state and loss of contact releases the leg into a free-swing state.
   对应摘录：B
4. 句子 4：Most states keep constant tuned impedance parameters, but a substantial subset modulates impedance according to previous-state values, ankle angle, knee angle, or increasing/decreasing prosthesis load so that transitions between activities remain smooth.
   对应摘录：C
5. 句子 5：This preserves both the mode hierarchy and the intra-mode gait-state machine, making the sample a clear `HSM + T0` powered-prosthesis controller rather than a single flat impedance law.
   对应摘录：A, B, C
