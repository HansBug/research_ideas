# A Biomechanical Comparison of Proportional Electromyography Control to Biological Torque Control Using a Powered Hip Exoskeleton - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 hip exoskeleton 的 biological-torque controller 写成四态 gait-phase supervisor，并明确给出 `hip angle / GRF` guard、状态内输出律与 `15% BW` 阈值，可直接作为高质量 `EFSM + T0` 样本。

## 条目 1: Four-state biological-torque supervisor for the powered hip exoskeleton
- 控制对象：气动 hip exoskeleton 的 biological torque profile gait controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向动力髋外骨骼的 gait-phase 监督控制器，用 hip angle 和 vertical GRF 识别步态阶段，再切换 extension/flexion torque assistance。
- 判断：算。对象是真实外骨骼控制器，不是纯生物力学分析流程；原文明确给出四个状态、状态内输出规律以及相位切换 guard。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3 页，Section `Controller Design / State Machine Controller`，行 219-224
> The first control strategy was a state machine controller that provided an exoskeleton torque profile similar to a standard biological hip torque profile.
>
> The state machine controller used mechanical signals from the hip angle and ground reaction force to calculate gait phase and apply an appropriate torque profile. It had four states to control joint torque levels.

#### 摘录 B
- 出处：第 4 页，Figure `2` caption，行 229-232
> Early stance phase (detected at the heel contact event) activated a hip extension torque. A transition to mid stance occurred at approximately 20% of the gait cycle. Mid stance was unpowered. A transition to late stance occurred at approximately 35% of the gait cycle. Late stance activated a hip flexion torque. Toe off triggered a transition to swing phase which was not actuated.
>
> A threshold trigger switched the states between stance and swing phase (15% of body weight). Mid stance was triggered based on a decrease from the first peak in the ground reaction force profile. Late stance was triggered based on an increase in the ground reaction force profile from the trough.

#### 摘录 C
- 出处：第 4 页，Section `State 1—Early Stance`，行 243-249
> The maximum hip flexion angle occurs at heel contact. This parameter varies slightly per subject but was approximately 30°.
>
> The current hip angle is read by a goniometer. The output is 0 if the hip angle is negative (in extension).
>
> The pneumatic actuator is powered at 100% at the beginning of the phase and linearly decreases to 0 with hip angle as the hip extends during stance.

#### 摘录 D
- 出处：第 4-5 页，Section `State 3—Late Stance`，行 253-274
> During the third state, from approximately 35–60% of the gait cycle, the exoskeleton provided active hip flexion assistance with a supply signal linearly related to the subject’s weight on the stance leg.
>
> The maximum vertical force was set at the beginning of the experiment and was different based on the subject’s weight (approximately 1.2 times body weight).
>
> The supply pressure scales linearly with applied weight. Thus, the state has a large flexion torque applied during the beginning with the rise of the second peak of vertical ground reaction force and drops off as the person takes weight off the leg and transitions into swing.

### 2. 基于原文整理后的自然语言描述

The powered hip exoskeleton uses an extended four-state gait-phase supervisor with `Early Stance`, `Mid Stance`, `Late Stance`, and `Swing`, where hip angle and vertical ground reaction force jointly determine the active state. Heel contact enters `Early Stance`, and the controller applies hip extension assistance that starts at full scale and decreases linearly to zero as the hip extends from an initial flexed posture of about `30°` toward neutral. `Mid Stance` is explicitly unpowered, after which `Late Stance` applies hip flexion assistance proportional to stance-leg vertical force, with the reference peak set around `1.2` body weight and the output fading as the subject unloads the leg. `Swing` is also unpowered, and the transition logic is explicit rather than implicit: stance-versus-swing uses a `15%` body-weight GRF threshold, the `Early Stance -> Mid Stance` transition uses a `5%` drop from the first GRF peak, and `Mid Stance -> Late Stance` uses a `5%` rise from the trough. This makes the sample a variable-driven `EFSM` with state-specific output laws, not just a descriptive gait timeline.

### 3. 逐句溯源

1. 句子 1：The powered hip exoskeleton uses an extended four-state gait-phase supervisor with `Early Stance`, `Mid Stance`, `Late Stance`, and `Swing`, where hip angle and vertical ground reaction force jointly determine the active state.
   对应摘录：A, B
2. 句子 2：Heel contact enters `Early Stance`, and the controller applies hip extension assistance that starts at full scale and decreases linearly to zero as the hip extends from an initial flexed posture of about `30°` toward neutral.
   对应摘录：B, C
3. 句子 3：`Mid Stance` is explicitly unpowered, after which `Late Stance` applies hip flexion assistance proportional to stance-leg vertical force, with the reference peak set around `1.2` body weight and the output fading as the subject unloads the leg.
   对应摘录：B, D
4. 句子 4：`Swing` is also unpowered, and the transition logic is explicit rather than implicit: stance-versus-swing uses a `15%` body-weight GRF threshold, the `Early Stance -> Mid Stance` transition uses a `5%` drop from the first GRF peak, and `Mid Stance -> Late Stance` uses a `5%` rise from the trough.
   对应摘录：B
5. 句子 5：This makes the sample a variable-driven `EFSM` with state-specific output laws, not just a descriptive gait timeline.
   对应摘录：A, C, D
