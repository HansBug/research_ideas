# Controlling Knee Swing Initiation and Ankle Plantarflexion With an Active Prosthesis on Level and Inclined Surfaces at Variable Walking Speeds - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 active knee-ankle prosthesis 的 `4` 态 walking state machine、mechanical sensor guards，以及 late-stance 内部按 ankle angle / shank force 连续调制的 impedance law，可直接作为 `EFSM + T0` 双 A 样本。

## 条目 1: Four-state walking controller for coordinated knee swing initiation and ankle plantarflexion
- 控制对象：active knee and ankle prosthesis 的四态 gait-phase controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 active knee-ankle prosthesis 的四态步态控制器，它用 shank force、ankle dorsiflexion 和 knee flexion velocity 触发 gait-phase 切换，并在 stance 内连续调度 ankle/knee impedance 与 equilibrium angle。
- 判断：算。对象是真实主动膝踝假肢控制器，不是离线步态分析；原文明确给出了四个离散状态、状态切换 guard，以及各状态中的 state-specific impedance law。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Figure `1`
> State machine of walking consisting of `4` finite states (`early-mid stance`, `late stance`, `swing flexion` and `swing extension`). Onboard mechanical sensor thresholds were used to switch between states ... to detect heel strike and toe off, thresholds of the axial shank force were used ... ankle dorsiflexion thresholds ... knee flexion velocity thresholds ...

#### 摘录 B
- 出处：第 3-4 页，Section `B. Impedance-Based State Machine`
> The state machine used in this study consisted of two states within stance ... and two states within swing ... Within this framework ... joint impedances were not constrained to be constant within a given state ... the four new algorithms modulated respective impedance parameters as functions of joint angle or axial shank force.

#### 摘录 C
- 出处：第 4 页，Section `C. Rate-Based Prosthesis Control Algorithms`
> increasing ankle stiffness ... during controlled dorsiflexion ... as a linear function of ankle angle ... decreasing knee stiffness ... during late stance was facilitated. This modulation was specified as a linear function of decreasing axial shank force ... knee swing initiation and powered ankle plantarflexion were controlled by changes of their equilibrium positions ... as linear functions of decreasing shank force during late stance.

#### 摘录 D
- 出处：第 4-5 页，Figure `2` caption and following paragraph
> final equilibrium angle of the ankle is set to `-12°` ... final equilibrium angle of the knee is set to `-45°` ... changes of the equilibrium angles occur sooner and at a faster rate for increasing walking speed ... Swing flexion and swing extension states did not contain any of these algorithms ... in swing flexion, the knee equilibrium angle was held constant ... In swing extension, knee equilibrium angle was constant at `0°`.

### 2. 基于原文整理后的自然语言描述

The active knee-ankle prosthesis uses a four-state walking controller with `Early-Mid Stance`, `Late Stance`, `Swing Flexion`, and `Swing Extension` as its discrete gait phases. State transitions are driven by onboard mechanical thresholds rather than by fixed timing, using axial shank-force thresholds for heel strike and toe-off, ankle-dorsiflexion thresholds for the stance-to-stance transition, and knee-flexion-velocity thresholds for the switch from swing flexion to swing extension. Inside stance, the controller does not keep impedance constant: ankle stiffness increases as a function of ankle angle, while knee stiffness, knee equilibrium angle, and ankle equilibrium angle are modulated as functions of decreasing axial shank force in late stance. That shank-unloading rule is also what initiates powered ankle plantarflexion and knee swing initiation, so the continuous parameter adaptation is embedded inside the discrete stance states rather than handled by a separate optimizer. Once the machine enters `Swing Flexion` or `Swing Extension`, those rate-based stance algorithms are turned off and the knee equilibrium is held at its flexed value or reset to `0°`, respectively.

### 3. 逐句溯源

1. 句子 1：The active knee-ankle prosthesis uses a four-state walking controller with `Early-Mid Stance`, `Late Stance`, `Swing Flexion`, and `Swing Extension` as its discrete gait phases.
   对应摘录：A, B
2. 句子 2：State transitions are driven by onboard mechanical thresholds rather than by fixed timing, using axial shank-force thresholds for heel strike and toe-off, ankle-dorsiflexion thresholds for the stance-to-stance transition, and knee-flexion-velocity thresholds for the switch from swing flexion to swing extension.
   对应摘录：A
3. 句子 3：Inside stance, the controller does not keep impedance constant: ankle stiffness increases as a function of ankle angle, while knee stiffness, knee equilibrium angle, and ankle equilibrium angle are modulated as functions of decreasing axial shank force in late stance.
   对应摘录：B, C
4. 句子 4：That shank-unloading rule is also what initiates powered ankle plantarflexion and knee swing initiation, so the continuous parameter adaptation is embedded inside the discrete stance states rather than handled by a separate optimizer.
   对应摘录：C, D
5. 句子 5：Once the machine enters `Swing Flexion` or `Swing Extension`, those rate-based stance algorithms are turned off and the knee equilibrium is held at its flexed value or reset to `0°`, respectively.
   对应摘录：D
