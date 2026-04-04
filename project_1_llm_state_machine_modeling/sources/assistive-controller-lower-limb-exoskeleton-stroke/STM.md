# An Assistive Controller for a Lower-Limb Exoskeleton for Rehabilitation after Stroke, and Preliminary Assessment Thereof - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：HSM（层次状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：层次
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把卒中康复外骨骼的 gait assistance controller 明确写成三主状态、六子状态的 FSM，并给出 heel strike、角速度与局部时间驱动的切换逻辑，可直接抽成高质量层次状态机描述。

## 条目 1: Gait-assistance controller for a post-stroke lower-limb exoskeleton
- 控制对象：卒中康复下肢外骨骼的步态辅助监督控制器
- 状态机类型：HSM（层次状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：层次
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向卒中偏瘫患者 gait rehabilitation 的层次外骨骼控制器，用三大 gait state 和六个 sub-state 调度 swing assist、double-support 过渡与 stance knee stabilization。
- 判断：算。对象是真实下肢外骨骼 gait assistance controller，不是康复训练流程；原文给出了状态层次、切换事件和状态内局部时间变量，足以恢复可建模的高层控制链。

### 1. 原文摘录

#### 摘录 A
- 出处：第 2 页，Section II.A `Control States and Notation`
> The exoskeleton controller is governed by a finite state machine consisting of three states, as illustrated in Fig. 1.
>
> Each state is comprised of two sub-states, as follows: sub-states 1a and 1b correspond to the portions of swing in which the affected knee is in a state of flexion and extension respectively; sub-states 2a and 2b correspond to double-support following heel strike of the affected leg and unaffected leg, respectively; and sub-states 3a and 3b correspond to the portions of swing in which the unaffected knee is in a state of flexion and extension, respectively.

#### 摘录 B
- 出处：第 5 页，Section II.F `Structure of the State Machine`
> The switching conditions that describe movement between the finite states of the state machine are shown in Fig. 2.
>
> In particular, switching between sub-states 1a and 1b, or 3a and 3b, is based on a change in the sign of the knee angular velocity in the affected and unaffected swing leg, respectively.

#### 摘录 C
- 出处：第 6 页，Section II.F `Structure of the State Machine`
> The controller switches from single-support to double-support states via detection of heel strike of the respective swing leg.
>
> Finally, the controller switches from double-support to swing (i.e., out of 2a or 2b) when the angular velocity of the respective thigh exceeds a given threshold.

#### 摘录 D
- 出处：第 4-5 页，Section II.D `Feedforward Movement Assistance during Swing`
> In order to provide additional assistance without dictating joint trajectories, the controller allows the user to initiate a given movement, then supplements that movement with a brief torque pulse at the respective joint.
>
> where ... `T_kf`, `T_hf`, `T_ke` ... are the torque pulse amplitude and duration ... and `t_a` and `t_b` are the length of time since the controller entered sub-states 1a and 1b.

### 2. 基于原文整理后的自然语言描述

The post-stroke lower-limb exoskeleton is organized as a hierarchical gait-assistance state machine with three top-level phases: affected-limb swing, double support, and unaffected-limb swing. Each top-level phase is split into two sub-states so that knee flexion and extension during swing, and the two double-support cases following affected or unaffected heel strike, are explicitly distinguished in the control logic. Transitions inside the swing phases are triggered by sign changes in the corresponding knee angular velocity, while transitions from swing to double support are triggered by heel-strike detection of the active swing leg. The controller leaves `2a` or `2b` and re-enters swing when the angular velocity of the corresponding thigh exceeds a threshold, which provides the event guard for the next gait phase. Inside the swing sub-states, the controller also uses local elapsed-time variables after state entry to apply brief torque pulses, so the high-level gait phases and the within-state timed assist actions are coupled in a single supervisory loop.

### 3. 逐句溯源

1. 句子 1：The post-stroke lower-limb exoskeleton is organized as a hierarchical gait-assistance state machine with three top-level phases: affected-limb swing, double support, and unaffected-limb swing.
   对应摘录：A
2. 句子 2：Each top-level phase is split into two sub-states so that knee flexion and extension during swing, and the two double-support cases following affected or unaffected heel strike, are explicitly distinguished in the control logic.
   对应摘录：A
3. 句子 3：Transitions inside the swing phases are triggered by sign changes in the corresponding knee angular velocity, while transitions from swing to double support are triggered by heel-strike detection of the active swing leg.
   对应摘录：B, C
4. 句子 4：The controller leaves `2a` or `2b` and re-enters swing when the angular velocity of the corresponding thigh exceeds a threshold, which provides the event guard for the next gait phase.
   对应摘录：C
5. 句子 5：Inside the swing sub-states, the controller also uses local elapsed-time variables after state entry to apply brief torque pulses, so the high-level gait phases and the within-state timed assist actions are coupled in a single supervisory loop.
   对应摘录：D
