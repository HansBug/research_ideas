# Case Study: A Bio-Inspired Control Algorithm for a Robotic Foot-Ankle Prosthesis Provides Adaptive Control of Level Walking and Stair Ascent - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T0（无关键时间语义）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把足踝假肢控制器写成“BiOM gait state machine + phase-dependent virtual muscle activations”，明确给出 gait states、阶段性输出和跨地形不改参的切换逻辑，可直接作为 `EFSM + T0` 样本。

## 条目 1: Phase-dependent virtual-muscle supervisor for the robotic foot-ankle prosthesis
- 控制对象：机器人 foot-ankle prosthesis 的 BiOM gait-state supervisor 与 WFH virtual-muscle controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T0（无关键时间语义）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向机器人足踝假肢的 gait-stage controller，它复用 BiOM 的离散步态状态机，并在各阶段按虚拟前后肌群激活模式生成 ankle torque。
- 判断：算。对象是真实动力足踝假肢控制器，不是纯实验分析；原文明确给出状态划分、状态内激活输出、输入传感器以及 level walking 与 stair ascent 间的无重配置切换。

### 1. 原文摘录

#### 摘录 A
- 出处：第 4 页，Section `BiOM T2 Prosthesis Platform`，行 37-47
> three rate gyroscopes. The BiOM stock controller employs a
> state-based approach to command ankle torques using a set
> of algorithms that are implemented in speciﬁc stages of the
> walking gait cycle (early swing, late swing, early stance, mid-
> stance, late stance). Previous studies demonstrate that the BiOM
> prosthesis signiﬁcantly outperforms passive-elastic prostheses,
> and permits metabolic energy costs, preferred walking velocities
> and biomechanical patterns over level terrain that are similar to
> those of people without amputation.

#### 摘录 B
- 出处：第 5 页，Table `1`，行 24-33
> Act(A2) Activation, AM Stage 2 (Equation 1) 0.93, 0.63 User preference
> Act(A3) Activation, AM Stage 3 (Equation 1) 0.28, 0.48 User preference
> Act(A4) Activation, AM Stage 4 (Equation 1) 0.31, 0.51 User preference
> Act(A5) Activation, AM Stage 5 (Equation 1) 0 [8]
> Act(A6) Activation, AM Stage 6 (Equation 1) 0 [8]
> Act(P2) Activation, PM Stage 2 (Equation 1) 0 [8]
> Act(P3) Activation, PM Stage 3 (Equation 1) 0 [8]
> Act(P4) Activation, PM Stage 4 (Equation 1) 0 [8]
> Act(P5) Activation, PM Stage 5 (Equation 1) 0 [8]
> Act(P6) Activation, PM Stage 6 (Equation 1) 0.44, 0.69 User preference

#### 摘录 C
- 出处：第 6 页，Section `Implementation of the WFH Control Algorithm`，行 11-20
> The WFH control algorithm uses the BiOM state machine
> only to provide phase-dependent activation (0–100% of maximal
> isometric muscle force, P0) of the anterior and posterior muscles
> that approximates biological muscle activation patterns. The
> anterior muscle group is active (∼60–90% P0) during early swing,
> late swing (∼30–50% P0), and early stance (∼30–50% P0) and
> the posterior muscle group is only active (∼40–70% P0) during
> powered plantar ﬂexion. The activation levels were adjusted to
> user preference during tuning sessions preceding experimental
> trials.

#### 摘录 D
- 出处：第 11 页，Figure `7` caption，行 2-5
> FIGURE 7 | Adaptability of the WFH control algorithm. ... The subject
> ﬁrst takes two strides on level ground, then ascends four stairs on the prosthetic side, and ﬁnally takes two level strides at the top of the stairs. For
> the WFH controller, there is no change in muscle activation or other parameters during transitions from level walking to stair ascent and back to level walking.

### 2. 基于原文整理后的自然语言描述

The robotic foot-ankle prosthesis is controlled by an extended gait supervisor that reuses the BiOM state machine as a discrete phase skeleton for ankle torque generation. The discrete stages cover `early swing`, `late swing`, `early stance`, `mid-stance`, and `late stance`, and the WFH algorithm maps each state to virtual anterior and posterior muscle activations rather than to a single fixed torque law. The anterior virtual muscle is activated strongly in early swing and more moderately in late swing and early stance, while the posterior virtual muscle stays inactive until the powered plantar-flexion portion of the gait. These state-dependent activations drive a muscle-model-based torque command using ankle-angle sensing, and the same discrete controller remains active when the user moves from level walking to stair ascent and back without changing muscle activations or other controller parameters.

### 3. 逐句溯源

1. 句子 1：The robotic foot-ankle prosthesis is controlled by an extended gait supervisor that reuses the BiOM state machine as a discrete phase skeleton for ankle torque generation.
   对应摘录：A, C
2. 句子 2：The discrete stages cover `early swing`, `late swing`, `early stance`, `mid-stance`, and `late stance`, and the WFH algorithm maps each state to virtual anterior and posterior muscle activations rather than to a single fixed torque law.
   对应摘录：A, C
3. 句子 3：The anterior virtual muscle is activated strongly in early swing and more moderately in late swing and early stance, while the posterior virtual muscle stays inactive until the powered plantar-flexion portion of the gait.
   对应摘录：B, C
4. 句子 4：These state-dependent activations drive a muscle-model-based torque command using ankle-angle sensing, and the same discrete controller remains active when the user moves from level walking to stair ascent and back without changing muscle activations or other controller parameters.
   对应摘录：A, C, D
