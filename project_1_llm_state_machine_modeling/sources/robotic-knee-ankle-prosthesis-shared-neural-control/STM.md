# Stand-Up, Squat, Lunge, and Walk With a Robotic Knee and Ankle Prosthesis Under Shared Neural Control - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 robotic knee-ankle prosthesis 的 shared neural controller 压成 `Stance / Swing` 两态 `FSM`，并给出 `50 N` 接地阈值、阈值切换条件、EMG 增益律和 ankle-knee coupling，可直接作为高质量 `EFSM + T0` 样本。

## 条目 1: Two-state shared-neural supervisor for the robotic knee-ankle prosthesis
- 控制对象：机器人膝踝假肢的 shared neural high-level controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向主动膝踝假肢的 shared neural supervisor，用 `Stance / Swing` 两态骨架统一支撑 walking、sit-to-stand、squat、lunge 和 quiet standing。
- 判断：算。对象是真实机器人假肢控制器，不是动作分类实验；原文明确给出高层两态 FSM、转移阈值、EMG 驱动 knee torque 和 knee-ankle coupling 关系。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Results / ambulation circuit，行 191-200
> The robotic prosthesis seamlessly switched between two different states— `Stance` and `Swing`.
>
> For all ambulation activities, the actions of the robotic knee and ankle prosthesis during `Stance` were controlled by the subject’s residual biceps femoris EMG using the proposed shared neural controller, whereas the actions of the robotic knee and ankle during `Swing` were controlled using an indirect volitional controller.
>
> The ankle and knee angle trajectories did not show discontinuities at the transitions between different activities or controller states.

#### 摘录 B
- 出处：第 8 页，Section `V.A. Shared Neural Control`，行 502-520
> At the high-level, we use a finite state-machine ... This finite-state machine comprises two different states— `Stance` and `Swing`.
>
> When the prosthesis contacts the ground, as detected by the ground reaction force exceeding `50 N`, the finite-state machine enters `Stance`.
>
> From `Stance`, the finite-state machine transitions to `Swing` if the shank position and shank velocity are below thresholds while the knee position is below a threshold.
>
> `Stance` controller is used for standing up, sitting down, squatting, lunging, quiet standing, as well as for the `Stance` phase of walking.

#### 摘录 C
- 出处：第 8 页，Section `V.A. Shared Neural Control`，行 521-539
> The knee joint extension torque is controlled using proportional EMG control ...
>
> The EMG signal from the biceps femoris ... is multiplied by a position-dependent gain to obtain the desired knee torque.
>
> The position-dependent gain is calculated using a linear curve with an offset (`G0 = 30°`, `G1 = 0.625`) ... resulting in higher sensitivity of the desired torque to the EMG signal for more flexed knee joint angles.

#### 摘录 D
- 出处：第 8 页，Section `V.A. Shared Neural Control`，行 540-559
> The ankle joint is controlled using an impedance-based control strategy ... with variable equilibrium position.
>
> The ankle equilibrium position changes as a function of the measured knee position based on the linear relationship ... `θ_eq,ankle = k θ_knee` for `θ_knee ≥ 0`, `θ_eq,ankle = 0` for `θ_knee < 0`.
>
> The equilibrium angle of the ankle reaches a maximum of `12°` when the knee joint is flexed at `90°`.

### 2. 基于原文整理后的自然语言描述

The robotic knee-ankle prosthesis uses an extended two-state supervisor with `Stance` and `Swing`, and the same high-level skeleton is reused across walking, sit-to-stand, squat, lunge, and quiet standing. The state machine enters `Stance` when ground contact is detected with vertical ground reaction force above `50 N`, and it switches to `Swing` when shank position, shank velocity, and knee position fall below fixed thresholds. In `Stance`, the knee is driven by residual-biceps-femoris EMG through a position-dependent gain law with `G0 = 30°` and `G1 = 0.625`, so larger knee flexion angles increase the sensitivity of the commanded extension torque. The ankle is not controlled independently of the knee state; instead, its impedance controller uses a knee-coupled equilibrium angle `θ_eq,ankle = k θ_knee` that stays neutral for negative knee angles and reaches about `12°` dorsiflexion at `90°` knee flexion. Because this two-state machine can switch across multiple activities without discontinuous angle trajectories, the sample is a compact but information-rich prosthesis `EFSM` rather than a single-activity gait detector.

### 3. 逐句溯源

1. 句子 1：The robotic knee-ankle prosthesis uses an extended two-state supervisor with `Stance` and `Swing`, and the same high-level skeleton is reused across walking, sit-to-stand, squat, lunge, and quiet standing.
   对应摘录：A, B
2. 句子 2：The state machine enters `Stance` when ground contact is detected with vertical ground reaction force above `50 N`, and it switches to `Swing` when shank position, shank velocity, and knee position fall below fixed thresholds.
   对应摘录：B
3. 句子 3：In `Stance`, the knee is driven by residual-biceps-femoris EMG through a position-dependent gain law with `G0 = 30°` and `G1 = 0.625`, so larger knee flexion angles increase the sensitivity of the commanded extension torque.
   对应摘录：C
4. 句子 4：The ankle is not controlled independently of the knee state; instead, its impedance controller uses a knee-coupled equilibrium angle `θ_eq,ankle = k θ_knee` that stays neutral for negative knee angles and reaches about `12°` dorsiflexion at `90°` knee flexion.
   对应摘录：D
5. 句子 5：Because this two-state machine can switch across multiple activities without discontinuous angle trajectories, the sample is a compact but information-rich prosthesis `EFSM` rather than a single-activity gait detector.
   对应摘录：A, B, D
