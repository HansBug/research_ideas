# Powered Knee and Ankle Prosthesis with Adaptive Control Enables Climbing Stairs with Different Stair Heights, Cadences, and Gait Patterns - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文明确给出 stair-climbing powered knee-ankle prosthesis 的 `Stance / Swing` 两态 FSM、`40/120 N` `GRF` guard，以及由 thigh angle/velocity/vertical acceleration 与 knee-at-contact jointly 决定的 swing/stance law，可直接作为 `EFSM + T0` 双 A 样本。

## 条目 1: Two-state stair-ascent supervisor for the adaptive powered knee-ankle prosthesis
- 控制对象：powered knee and ankle prosthesis 的 adaptive stair-ascent controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 stair-climbing powered knee-ankle prosthesis 的两态监督控制器，它以 `GRF` 切换 `Stance / Swing`，在 `Swing` 中跟随 residual thigh motion 生成 joint-angle reference，在 `Stance` 中按接触时膝角自适应 torque-angle law。
- 判断：算。对象是真实膝踝主动假肢 stair controller，不是单纯生物力学分析；原文明确给出了两态骨架、阈值 guard、state-specific 位置/力矩控制律和 stair-height adaptation 逻辑。

### 1. 原文摘录

#### 摘录 A
- 出处：第 6-7 页，Figure `3` and related text
> The proposed controller uses a finite-state machine with two states (i.e., `Stance` and `Swing`) ... When the ground reaction force (`GRF`) is lower than a predefined threshold (`GRF SwingTHS`) the stair controller is in `Swing`. Whenever the ground reaction force (`GRF`) is higher than a fixed threshold (`GRF StanceTHS`), the prosthesis controller transitions from `Swing` to `Stance`.

#### 摘录 B
- 出处：第 4 页，Section `II. Controller`
> The first term `θknee1des` is proportional to the orientation of the user's thigh ... The second term `θknee2des` is proportional to the positive angular velocity of the user's thigh ... The third term determining the desired knee position in `Swing` ... depends on the vertical acceleration of the user's thigh ... Thus, the proposed `Swing` controller captures the initial vertical movement of the hip and translates that movement into a desired flexion of the prosthesis knee joint.

#### 摘录 C
- 出处：第 4-5 页，Section `II. Controller`
> The desired angular position of the ankle joint `θankledes` in `Swing` is the sum of two terms ... This term is zero for thigh angles lower than zero. When the thigh angle is between `0°` and `20°`, the desired ankle angle is proportional to the thigh orientation angle. For thigh angles greater than `30°`, the desired ankle angle is equal to the shank orientation angle ... The second term ... depends on the vertical acceleration of the user's thigh ...

#### 摘录 D
- 出处：第 5-6 页，Section `II. Controller`
> In `Stance`, we use a torque controller that increases the assistance provided to the user ... the desired torque-angle relationship is not fixed but changes as a function of the knee position when the controller switches from `Swing` to `Stance` `θknee0` ... larger knee extension torque is produced when the powered prosthesis transitions between `Swing` and `Stance` at a larger knee flexion angle ... if the powered prosthesis transitions ... with the knee fully extended ... the desired torque is defined solely by the impedance component, which stabilizes the knee joint and prevents it from collapsing.

#### 摘录 E
- 出处：第 14 页，Table `I`
> `GRF StanceTHS 120 N` ... `GRF SwingTHS 40 N`.

### 2. 基于原文整理后的自然语言描述

The stair-ascent controller for the powered knee-ankle prosthesis is organized around a two-state supervisor that switches between `Stance` and `Swing` with fixed `GRF` thresholds of `40 N` and `120 N`. In `Swing`, the desired knee motion is generated from three residual-limb signals at once, because thigh orientation, positive thigh angular velocity, and thigh vertical acceleration are all mapped into the commanded prosthesis knee flexion. The ankle swing reference is adapted in the same supervisor: thigh angle sets the main foot-orientation schedule, shank angle takes over once the thigh is high enough, and vertical thigh acceleration contributes an additional correction term. When the controller re-enters `Stance`, it switches from position tracking to a torque controller whose knee torque-angle relationship is selected from the knee angle measured at the `Swing -> Stance` transition, so stair height and gait pattern directly change the energy injected into the step. The result is still a compact finite-state controller, but it preserves explicit phase switching, sensor-threshold guards, state-specific low-level laws, and cadence-dependent stair-climbing adaptation inside a single `Stance / Swing` EFSM.

### 3. 逐句溯源

1. 句子 1：The stair-ascent controller for the powered knee-ankle prosthesis is organized around a two-state supervisor that switches between `Stance` and `Swing` with fixed `GRF` thresholds of `40 N` and `120 N`.
   对应摘录：A, E
2. 句子 2：In `Swing`, the desired knee motion is generated from three residual-limb signals at once, because thigh orientation, positive thigh angular velocity, and thigh vertical acceleration are all mapped into the commanded prosthesis knee flexion.
   对应摘录：B
3. 句子 3：The ankle swing reference is adapted in the same supervisor: thigh angle sets the main foot-orientation schedule, shank angle takes over once the thigh is high enough, and vertical thigh acceleration contributes an additional correction term.
   对应摘录：C
4. 句子 4：When the controller re-enters `Stance`, it switches from position tracking to a torque controller whose knee torque-angle relationship is selected from the knee angle measured at the `Swing -> Stance` transition, so stair height and gait pattern directly change the energy injected into the step.
   对应摘录：D
5. 句子 5：The result is still a compact finite-state controller, but it preserves explicit phase switching, sensor-threshold guards, state-specific low-level laws, and cadence-dependent stair-climbing adaptation inside a single `Stance / Swing` EFSM.
   对应摘录：A, B, C, D
