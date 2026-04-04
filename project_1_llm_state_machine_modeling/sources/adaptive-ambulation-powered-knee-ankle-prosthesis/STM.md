# Powered Knee and Ankle Prosthesis Control for Adaptive Ambulation at Variable Speeds, Inclines, and Uneven Terrains - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 powered knee-ankle prosthesis 的 `stance / swing` `FSM`、`GRF` guard、state-specific knee/ankle torque laws，以及基于 toe-off ankle angle 的 minimum-jerk swing timing，可直接作为 `EFSM + T0` 样本。

## 条目 1: Stance-swing adaptive supervisor for the powered knee-ankle prosthesis
- 控制对象：powered knee and ankle prosthesis 的 adaptive ambulation controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 powered knee-ankle prosthesis 的两态 gait supervisor，它用 `GRF` 在 `stance / swing` 之间切换，并在 `stance` 内按 knee velocity、thigh angle、shank angle 与 walking speed 计算 torque/damping，在 `swing` 内按 toe-off joint state 生成 minimum-jerk trajectory。
- 判断：算。对象是真实膝踝主动假肢控制器，不是单纯轨迹优化方法；原文完整保住了离散相位切换、guard、state-specific torque law 和 swing-duration adaptation。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `II. Methods / A. Controller`
> A finite-state machine switches from stance to swing when the vertical ground reaction force (GRF) measures below `40 N` ... and swing to stance when the GRF measures above `120 N`.

#### 摘录 B
- 出处：第 3-4 页，Section `A. Controller`
> During stance, we determine the desired knee torque as the sum of two components: a virtual damping torque and a virtual biarticular torque ... Different damping coefficient values are used for extension and flexion ... `BFlex` depends on the global orientation of the residual thigh ... allowing the prosthetic knee joint to flex and initiate swing in late stance.

#### 摘录 C
- 出处：第 4-5 页，Section `A. Controller`
> In stance, we define the desired ankle torque using an impedance-inspired controller ... `TAnkle = TShank + TB` ... `TShank` pushes the shank back to a vertical position regardless of the ankle position ... both dorsiflexion damping `BDF` and plantarflexion damping `BPF` depend on an online estimate of the walking speed.

#### 摘录 D
- 出处：第 5 页，Section `A. Controller`
> During swing, we define the desired positions of the knee and ankle joints using a minimum-jerk optimizer ... the desired swing duration is adapted online when the controller transitions from stance to swing based on the position of the ankle at the transition ... `Tswing = Kswing · θAnkleTO`.

### 2. 基于原文整理后的自然语言描述

The adaptive powered knee-ankle prosthesis is organized around a two-state gait supervisor that switches between `stance` and `swing` using explicit vertical-`GRF` thresholds of `40 N` and `120 N`. Inside `stance`, the knee torque is not fixed but is computed as the sum of a velocity-dependent damping term and a virtual biarticular term, with flexion damping modulated by global thigh orientation so the knee stays stable in early stance and then releases toward swing in late stance. The ankle is controlled by an impedance-inspired law `TAnkle = TShank + TB`, where shank orientation defines a virtual restoring stiffness and speed-dependent dorsiflexion/plantarflexion damping injects more or less stance energy as walking speed changes. When the machine enters `swing`, the controller switches from torque laws to joint-position generation and creates smooth knee/ankle references with a minimum-jerk optimizer. The swing duration is itself adapted online from the ankle angle at toe-off, so cadence changes, terrain changes, and incline changes all feed back into the same discrete `stance / swing` supervisor without hand-tuned mode thresholds.

### 3. 逐句溯源

1. 句子 1：The adaptive powered knee-ankle prosthesis is organized around a two-state gait supervisor that switches between `stance` and `swing` using explicit vertical-`GRF` thresholds of `40 N` and `120 N`.
   对应摘录：A
2. 句子 2：Inside `stance`, the knee torque is not fixed but is computed as the sum of a velocity-dependent damping term and a virtual biarticular term, with flexion damping modulated by global thigh orientation so the knee stays stable in early stance and then releases toward swing in late stance.
   对应摘录：B
3. 句子 3：The ankle is controlled by an impedance-inspired law `TAnkle = TShank + TB`, where shank orientation defines a virtual restoring stiffness and speed-dependent dorsiflexion/plantarflexion damping injects more or less stance energy as walking speed changes.
   对应摘录：C
4. 句子 4：When the machine enters `swing`, the controller switches from torque laws to joint-position generation and creates smooth knee/ankle references with a minimum-jerk optimizer.
   对应摘录：D
5. 句子 5：The swing duration is itself adapted online from the ankle angle at toe-off, so cadence changes, terrain changes, and incline changes all feed back into the same discrete `stance / swing` supervisor without hand-tuned mode thresholds.
   对应摘录：D
