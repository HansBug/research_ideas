# Pneumatic Quasi-Passive Actuation for Soft Assistive Lower Limbs Exoskeleton - STM 提取记录

## 盘点结论
- 评级：🟢 直接可用
- 文件级角色：💎 含核心样本
- 代表状态机类型：EFSM（扩展状态机）
- 代表时间级别：T1（工程定时 / 局部定时）
- 结构标签概况：-（无代表标签）
- 是否计入 [SUMMARY.md](../SUMMARY.md) 盘点：是
- 提取条目数：1
- 简要判断：论文把 `XoSoft` 的 clutch scheduler 写成六相 gait `FSM`，明确列出触发事件、输入输出、gait-percentage engagement/disengagement 和按上一周期重算的 segment duration，可直接作为高质量 `EFSM + T1` 样本。

## 条目 1: Six-phase clutch scheduler for the XoSoft quasi-passive exoskeleton
- 控制对象：`XoSoft` 软式下肢外骨骼的 quasi-passive clutch coordination controller
- 状态机类型：EFSM（扩展状态机）
- 时间级别：T1（工程定时 / 局部定时）
- 结构标签：-（无额外结构标签）
- 原文细节充实度：🟢 A（细节完备）
- 描述细节充实度：🟢 A（细节完备）
- 数据集角色：💎 核心保留
- 趋同标签：✨ 未见强趋同

### 0. 条目识别与判定

- 一句话说明：这是一个面向 `XoSoft` quasi-passive 下肢外骨骼的 gait-phase scheduler，用 shoe sensors 和 knee angle 识别六个步态阶段，并切换 clutch 的 storing/releasing 行为。
- 判断：算。对象是真实外骨骼控制器，不是纯机构设计；原文明确给出状态机、离散事件、输入输出以及按 gait 百分比配置的局部定时策略。

### 1. 原文摘录

#### 摘录 A
- 出处：第 7 页，Section `Control Algorithm`，行 502-514
> The main control algorithm provides the segmentation of the gait cycle, which is shown in Figures 5, 6 as a logic state of a Finite State Machine (FSM). In correspondence of each state, the clutches can be set or reset.
>
> The system tracks the gait phases sequence, using the foot contact data and knee angle, to determine when to engage, disengage or keep the clutch current state. The inputs to the stateflow are the foot contact signal and knee angle. The outputs of the stateflow are the on-off clutch activation signals.

#### 摘录 B
- 出处：第 7 页，Figure `5` caption，行 518-520
> Control flow of the FSM, in which the events (`heelstrike`, `flatfoot`, `frontfoot`, `toeoff`, `positive speed inflection` and `negative speed inflection`) determining the state changes are reported.

#### 摘录 C
- 出处：第 8 页，Section `Gait Segmentation and Assistance Strategy`，行 543-558
> Based on the data from the shoe insole sensors and the IMUs, the controller is able to determine the six gait phases that form the finite state machine (FSM) (`early stance`, `mid stance`, `late stance`, `early swing`, `mid swing`, and `late swing`).
>
> The control designer ... may select the point, expressed as a percentage, of gait when the actuation should engage and disengage. The control system then processes this information to determine the correct timing to switch the actuator state. For every subsequent gait cycle, each duration of each segment is regenerated based on the previous gait’s total time.

#### 摘录 D
- 出处：第 8 页，Section `Assistance Examples`，行 559-569
> The actuator needs to store energy to be able to provide assistance. In Figure 7A, an example of hip flexion actuation is presented. The first vertical line represents the instant of TBC engagement (at about 15% of the gait cycle).
>
> Naturally, the storing phase ends with the minimum angle reached by the joint (at about 50%), then the releasing phase starts.
>
> The releasing phase will terminate as soon as the initial joint angle (instant of engagement) has been reached or as soon as the TBC is disengaged by the controller. In this example, the releasing phase ends at approx. the 75% of the gait cycle.

### 2. 基于原文整理后的自然语言描述

The XoSoft quasi-passive exoskeleton uses an extended six-phase gait supervisor that segments each stride into `early stance`, `mid stance`, `late stance`, `early swing`, `mid swing`, and `late swing` from shoe-contact events and knee-angle information. The FSM is explicit about its event alphabet: `heelstrike`, `flatfoot`, `frontfoot`, `toeoff`, `positive speed inflection`, and `negative speed inflection` trigger state changes, while the state outputs are clutch on/off activation signals. Rather than commanding a continuous target trajectory, the controller maps each phase to clutch engagement, disengagement, or hold behavior for the selected assisted joint and motion. A local timing layer is built in, because the designer chooses actuation windows as gait percentages and the controller regenerates each segment duration from the previous gait-cycle total time. This timing logic directly shapes the storing and releasing phases of assistance, for example enabling hip-flexion support to engage near `15%` of gait, store energy until the minimum joint angle near `50%`, and release until either the initial angle is recovered or the clutch is disengaged near `75%`.

### 3. 逐句溯源

1. 句子 1：The XoSoft quasi-passive exoskeleton uses an extended six-phase gait supervisor that segments each stride into `early stance`, `mid stance`, `late stance`, `early swing`, `mid swing`, and `late swing` from shoe-contact events and knee-angle information.
   对应摘录：A, C
2. 句子 2：The FSM is explicit about its event alphabet: `heelstrike`, `flatfoot`, `frontfoot`, `toeoff`, `positive speed inflection`, and `negative speed inflection` trigger state changes, while the state outputs are clutch on/off activation signals.
   对应摘录：A, B
3. 句子 3：Rather than commanding a continuous target trajectory, the controller maps each phase to clutch engagement, disengagement, or hold behavior for the selected assisted joint and motion.
   对应摘录：A, C
4. 句子 4：A local timing layer is built in, because the designer chooses actuation windows as gait percentages and the controller regenerates each segment duration from the previous gait-cycle total time.
   对应摘录：C
5. 句子 5：This timing logic directly shapes the storing and releasing phases of assistance, for example enabling hip-flexion support to engage near `15%` of gait, store energy until the minimum joint angle near `50%`, and release until either the initial angle is recovered or the clutch is disengaged near `75%`.
   对应摘录：D
