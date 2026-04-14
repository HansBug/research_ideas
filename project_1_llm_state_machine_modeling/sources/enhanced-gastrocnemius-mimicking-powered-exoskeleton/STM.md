# Enhanced gastrocnemius-mimicking lower limb powered exoskeleton robot - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文给出了 `EGME` 在 level walking 与 squat task 上的显式 `FSM`、步态相位驱动的 `force-position` 并联控制，以及 `squatting / squat holding / stand-up` 三段支撑力调度，可直接作为相位识别型外骨骼控制样本。

## 条目 1: Phase-aware gait-and-squat controller for the gastrocnemius-mimicking exoskeleton
- 控制对象：`EGME` 下肢动力外骨骼的相位识别监督控制器
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个依据步态与 squat 阶段识别结果，在不同相位下切换 `force-position` 权重、阻抗参数和自适应支撑力的下肢外骨骼监督控制器。
- 判断：算。对象是真实外骨骼控制器，不是实验流程；原文明确给出 FSM 相位划分、相位到输出控制策略的映射、状态相关参数以及 squat 支撑力调度规则，足以恢复完整控制主链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 3-4 页，Section `Objectives of the EGME function`
> During the early single-leg stance phase ... the EGME should apply an upward thrust ... and uses the results from Eq. (3) as the target for position tracking to achieve extension. In the mid-stance phase of single-leg support ... the EGME provides thrust under near-isometric conditions ... In the late single-leg stance phase, the EGME adopts the same thrust pattern as in the mid-stance phase ... In the pre-swing phase ... the EGME rapidly shortens and applies tensile force, with power and energy output to the leg maintained throughout the entire pre-swing phase.

#### 摘录 B
- 出处：第 4-5 页，Section `Control scheme`
> To effectively distinguish the different phases in the tasks of level walking and squat task, this study employs a finite state machine (FSM). By defining distinct states and transition rules between states, the FSM accurately captures the dynamic changes from one phase to another within the gait cycle. ... this study employs a force-position parallel control strategy ... and dynamically adjusts the weighting of the two based on gait phase recognition through the FSM ... u = αFi + βlp ... Ks = Ks0 + γFref during the stance phase and Ks = 0.05Ks0 during the swing phase ... During the isometric contraction phase, α >> β, while during the Quasi-Isotonic phase, α << β.

#### 摘录 C
- 出处：第 7 页，Section `Control scheme`
> During the squatting phase, the Fsq gradually increases, compensating for the additional braking load on the muscles. In the squat holding phase (isometric phase) ... the EGME offers stable support ... Here, Fsq stabilizes ... During the stand-up phase ... the EGME provides an assistive force ... Fsq gradually decreases to prevent abrupt force variations ...

#### 摘录 D
- 出处：第 8 页，Section `Experimental protocol`
> The experiment was divided into five distinct phases: standing, squatting, squat holding, standing up, and standing.

### 2. 基于原文整理后的自然语言描述

The EGME exoskeleton uses an FSM to separate both level walking and squat tasks into discrete motion phases, so that the controller can switch behavior when the wearer moves from one biomechanical regime to another. For walking, the state-dependent logic follows gastrocnemius function across `early single-leg stance`, `mid-stance`, `late single-leg stance`, and `pre-swing`: the exoskeleton alternates between extension-oriented position tracking, near-isometric thrust generation, and rapid shortening with tensile output to help initiate swing. The control law combines impedance-based force control and position control as `u = αFi + βlp`, and the FSM changes both the weighting coefficients and the underlying stiffness/damping parameters, with stance using higher `Ks/Ds`, swing using reduced gains, and isometric versus quasi-isotonic phases favoring force-dominant versus position-dominant assistance. For squat assistance, the same supervisor introduces an adaptive support force `Fsq` into the loop. `Fsq` ramps up during `squatting`, stays stable during `squat holding`, and gradually ramps down during `stand-up`, which lets the exoskeleton unload body weight while avoiding abrupt force changes.

### 3. 逐句溯源

1. 句子 1：The EGME exoskeleton uses an FSM to separate both level walking and squat tasks into discrete motion phases, so that the controller can switch behavior when the wearer moves from one biomechanical regime to another.
   对应摘录：B, D
2. 句子 2：For walking, the state-dependent logic follows gastrocnemius function across `early single-leg stance`, `mid-stance`, `late single-leg stance`, and `pre-swing`: the exoskeleton alternates between extension-oriented position tracking, near-isometric thrust generation, and rapid shortening with tensile output to help initiate swing.
   对应摘录：A
3. 句子 3：The control law combines impedance-based force control and position control as `u = αFi + βlp`, and the FSM changes both the weighting coefficients and the underlying stiffness/damping parameters, with stance using higher `Ks/Ds`, swing using reduced gains, and isometric versus quasi-isotonic phases favoring force-dominant versus position-dominant assistance.
   对应摘录：B
4. 句子 4：For squat assistance, the same supervisor introduces an adaptive support force `Fsq` into the loop.
   对应摘录：C
5. 句子 5：`Fsq` ramps up during `squatting`, stays stable during `squat holding`, and gradually ramps down during `stand-up`, which lets the exoskeleton unload body weight while avoiding abrupt force changes.
   对应摘录：C, D
