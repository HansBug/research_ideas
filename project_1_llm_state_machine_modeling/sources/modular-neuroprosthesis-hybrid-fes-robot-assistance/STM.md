# A new modular neuroprosthesis suitable for hybrid FES-robot applications and tailored assistance - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 gait sub-phase 级 preset `FSM`、`standard mode / cross mode` 两种 assistance 策略，以及 muscle-group 到 gait phase 的显式输出映射，可直接作为混合 `FES-robot` 辅助控制样本。

## 条目 1: Preset gait-phase stimulation supervisor for hybrid FES-robot assistance
- 控制对象：面向 hybrid `FES-robot` gait assistance 的模块化 neuroprosthesis 预设监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个根据 gait event 把步态切成多个 sub-phase，并对不同肌群在不同阶段施加预定义电刺激的混合 `FES-robot` 高层监督控制器。
- 判断：算。对象是真实 neuroprosthesis 控制算法，不是设备配置流程；原文明确给出 gait sub-phase、事件触发、状态到肌群输出映射，以及 `cross mode` 的跨腿事件驱动变体，足以恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 9 页，Figure 3B / Section describing the gait event algorithm
> This algorithm relied on adaptive thresholds to segment the gait into support, pre-swing, swing-up and swing-down sub-phases ... the algorithm detects four events shown in Fig. 3B: heel contact, heel off, toe off and maximum knee flexion during swing.

#### 摘录 B
- 出处：第 9 页，Section describing the preset finite state machine
> This was done in order to implement a preset one-sided finite state machine type open-loop control algorithm ... It is named as the standard mode ... and consists of a predefined state machine that ipsilaterally assists the musculature based on angular information from the ipsilateral hip, knee and ankle joints. ... gluteus maximus and quadriceps are assisted during the stance phase ... Tensor fasciae latae assistance was predefined during the swing ... Hamstrings assistance was predefined in the swing-up ... The gastrocnemius muscles are assisted in the toe-off phase ... the tibialis anterior is assisted in the swing ...

#### 摘录 C
- 出处：第 9-10 页，Section describing `cross mode`
> The control algorithm integrates a variant of the standard state machine that we call cross mode, which consists of assisting the ipsilateral leg using the gait events of the contralateral side. ... for this study was only adapted for gastrocnemius ... contralateral heel contact was used to start the assistance and was stopped with ipsilateral toe-off.

### 2. 基于原文整理后的自然语言描述

The modular neuroprosthesis uses a preset finite-state-machine style supervisor that segments gait into `support`, `pre-swing`, `swing-up`, and `swing-down` sub-phases from four detected gait events: `heel contact`, `heel off`, `toe off`, and `maximum knee flexion during swing`. In its `standard mode`, the controller assists the ipsilateral leg using ipsilateral hip, knee, and ankle angles, and maps each gait sub-phase to muscle-specific stimulation outputs rather than issuing a single generic pulse train. The output mapping is explicit: `gluteus maximus` and `quadriceps` are stimulated during `stance`, `tensor fasciae latae` during `swing`, `hamstrings` during `swing-up`, `gastrocnemius` during `toe-off`, and `tibialis anterior` during `swing`. The controller also defines a `cross mode` variant in which the ipsilateral leg is assisted from contralateral gait events. For the gastrocnemius case, `cross mode` starts assistance at contralateral `heel contact` and stops it at ipsilateral `toe-off`, so the stimulation is advanced relative to the short pre-swing interval.

### 3. 逐句溯源

1. 句子 1：The modular neuroprosthesis uses a preset finite-state-machine style supervisor that segments gait into `support`, `pre-swing`, `swing-up`, and `swing-down` sub-phases from four detected gait events: `heel contact`, `heel off`, `toe off`, and `maximum knee flexion during swing`.
   对应摘录：A
2. 句子 2：In its `standard mode`, the controller assists the ipsilateral leg using ipsilateral hip, knee, and ankle angles, and maps each gait sub-phase to muscle-specific stimulation outputs rather than issuing a single generic pulse train.
   对应摘录：B
3. 句子 3：The output mapping is explicit: `gluteus maximus` and `quadriceps` are stimulated during `stance`, `tensor fasciae latae` during `swing`, `hamstrings` during `swing-up`, `gastrocnemius` during `toe-off`, and `tibialis anterior` during `swing`.
   对应摘录：B
4. 句子 4：The controller also defines a `cross mode` variant in which the ipsilateral leg is assisted from contralateral gait events.
   对应摘录：C
5. 句子 5：For the gastrocnemius case, `cross mode` starts assistance at contralateral `heel contact` and stops it at ipsilateral `toe-off`, so the stimulation is advanced relative to the short pre-swing interval.
   对应摘录：C
